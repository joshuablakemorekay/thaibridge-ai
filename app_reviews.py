"""The in-app review prompt: ask learners how ThaiBridge is going, and keep the answers privately.

Who gets asked: signed-in learners who have reached Level 3 (REVIEW_MIN_LEVEL).
By then they have used the app properly, so the answer means something. A
brand-new sign-up would be rating a first impression.

Where: a card on the Progress page, which is where a learner goes to see how
far they've come. That's a natural moment to ask.

"Not now" hides the card for REVIEW_SNOOZE_DAYS. Once they've sent a review the
card is gone for good. Nobody is asked twice.

Nothing collected here appears on the site. Josh reads them at /reviews/private
(developer mode only). Later, quotes may go on the home or pricing page, but
only from reviews whose writer ticked "happy for you to show this".

Like the other modules this never imports app.py. app.py calls init_app(app).
"""

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
