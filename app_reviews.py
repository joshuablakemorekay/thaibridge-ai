"""The in-app review prompt: ask learners how Jaiway is going, and keep the answers privately.

Who gets asked: signed-in learners who have reached Level 3 (REVIEW_MIN_LEVEL).
By then they have used the app properly, so the answer means something. A
brand-new sign-up would be rating a first impression.

Where: a card on the Progress page, which is where a learner goes to see how
far they've come. That's a natural moment to ask.

"Not now" hides the card for REVIEW_SNOOZE_DAYS. Once they've sent a review the
card is gone for good. Nobody is asked twice.

Josh reads every review at /reviews/private (developer mode only).

The public page, /reviews, switches itself on once PUBLIC_MIN_QUOTES learners
have ticked "You can show my review". Until then it is a 404 and nothing links
to it. Once live it shows:
  * the average and the star counts from EVERY review, low ones included.
    UK law (DMCC Act 2024) bans showing only the good ones, and an honest
    average is the point of the page anyway.
  * the words of ONLY the learners who said yes, every one of them, newest
    first. No hand-picking: a 2-star review they let us show is shown too.

Like the other modules this never imports app.py. app.py calls init_app(app).
"""

import time
from datetime import date, timedelta

from flask import Blueprint, abort, jsonify, render_template, request, session
from flask_login import current_user

from access import active_tier
from extensions import limiter, rate_limit_key
from models import AppReview, User, db

bp = Blueprint('app_reviews', __name__)

REVIEW_MIN_LEVEL   = 3     # the same level that earns the free Thai Reader unlock
REVIEW_SNOOZE_DAYS = 30    # how long "Not now" hides the card
COMMENT_MAX        = 1000
NAME_MAX           = 60
PUBLIC_MIN_QUOTES  = 3     # showable reviews needed before /reviews goes live
SUMMARY_CACHE_SECS = 600   # the footer link asks on every page, so remember for 10 min

# Saved in the learner's progress (so it follows them to another device):
# the date they last pressed "Not now", as YYYY-MM-DD.
SNOOZE_KEY = 'review_prompt_snoozed_on'


def should_ask(progress):
    """Whether the Progress page shows the review card to this visitor."""
    if not current_user.is_authenticated:
        return False
    if (progress or {}).get('level', 1) < REVIEW_MIN_LEVEL:
        return False
    snoozed = (progress or {}).get(SNOOZE_KEY)
    if snoozed:
        try:
            if date.today() < date.fromisoformat(snoozed) + timedelta(days=REVIEW_SNOOZE_DAYS):
                return False
        except ValueError:
            pass   # an unreadable date counts as no snooze
    return AppReview.query.filter_by(user_id=current_user.id).first() is None


def _json_only():
    # The site's other POST routes take JSON for the same reason. A form on
    # someone else's website can't send JSON without the browser checking with
    # us first, so this blocks forged submissions without needing tokens.
    if not request.is_json:
        abort(415)
    if not current_user.is_authenticated:
        abort(401)


@bp.route('/api/review', methods=['POST'])
@limiter.limit('10 per hour', key_func=rate_limit_key)
def submit_review():
    _json_only()
    data = request.get_json(silent=True) or {}

    try:
        rating = int(data.get('rating'))
    except (TypeError, ValueError):
        rating = 0
    if not 1 <= rating <= 5:
        return jsonify({'success': False,
                        'message': 'Please choose a star rating from 1 to 5.'}), 400

    comment = (data.get('comment') or '').strip()
    if len(comment) > COMMENT_MAX:
        return jsonify({'success': False,
                        'message': f'Please keep it under {COMMENT_MAX} characters.'}), 400
    display_name = (data.get('display_name') or '').strip()[:NAME_MAX]

    review = AppReview.query.filter_by(user_id=current_user.id).first()
    if review is None:
        review = AppReview(user_id=current_user.id)
        db.session.add(review)
    review.rating = rating
    review.comment = comment or None
    review.can_publish = bool(data.get('can_publish'))
    review.display_name = display_name or None
    review.level_at_review = session.get('user_progress', {}).get('level')
    review.tier_at_review = active_tier()
    db.session.commit()

    return jsonify({'success': True,
                    'message': 'Thank you, that really helps.'})


@bp.route('/api/review/snooze', methods=['POST'])
def snooze_review():
    _json_only()
    progress = session.get('user_progress')
    if progress is not None:
        progress[SNOOZE_KEY] = date.today().isoformat()
        session.modified = True   # saved to the account after the request
    return jsonify({'success': True})


def _summary(rows_ratings):
    ratings = list(rows_ratings)
    return {
        'total':   len(ratings),
        'average': round(sum(ratings) / len(ratings), 1) if ratings else None,
        'counts':  {stars: ratings.count(stars) for stars in range(5, 0, -1)},
    }


_cache = {'at': 0.0, 'value': None}


def public_summary():
    """The headline numbers for the footer link, or None while /reviews is off.

    Remembered for SUMMARY_CACHE_SECS so every page view doesn't query the
    database. A new review can take up to 10 minutes to change the link.
    """
    now = time.monotonic()
    if _cache['at'] and now - _cache['at'] < SUMMARY_CACHE_SECS:
        return _cache['value']
    showable = AppReview.query.filter_by(can_publish=True).count()
    value = None
    if showable >= PUBLIC_MIN_QUOTES:
        value = _summary(r for (r,) in db.session.query(AppReview.rating))
    _cache.update(at=now, value=value)
    return value


def clear_summary_cache():
    _cache.update(at=0.0, value=None)


@bp.route('/reviews')
def public_reviews():
    """What learners say: the honest average, and the quotes they let us show."""
    shown = (AppReview.query.filter_by(can_publish=True)
             .order_by(AppReview.created_at.desc()).all())
    if len(shown) < PUBLIC_MIN_QUOTES:
        abort(404)
    summary = _summary(r for (r,) in db.session.query(AppReview.rating))
    return render_template('reviews.html', shown=shown, **summary)


@bp.route('/reviews/private')
def private_reviews():
    """Every review, newest first, with the average. Developer mode only."""
    if not session.get('user_progress', {}).get('is_developer'):
        abort(404)   # 404, not 403: don't advertise that the page exists
    rows = (db.session.query(AppReview, User.username)
            .join(User, User.id == AppReview.user_id)
            .order_by(AppReview.created_at.desc()).all())
    ratings = [r.rating for r, _ in rows]
    average = round(sum(ratings) / len(ratings), 1) if ratings else None
    counts = {stars: ratings.count(stars) for stars in range(5, 0, -1)}
    return render_template('reviews_private.html', rows=rows,
                           average=average, counts=counts)


def init_app(app):
    app.register_blueprint(bp)

    @app.context_processor
    def _reviews_link():
        try:
            return {'reviews_summary': public_summary()}
        except Exception:   # never let the footer take a page down
            return {'reviews_summary': None}
