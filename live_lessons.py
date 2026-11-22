"""Live lessons with a real Thai teacher: register your interest.

There are no live lessons yet. Before recruiting a teacher, this asks learners
whether they'd want them, so the decision rests on real numbers rather than a
guess. Nothing is booked, promised or charged.

Where: a box on the pricing page (/premium), the page people decide to pay
from. Signed-in learners only, so every name on the list is a real account
with an email address we can reach, and nobody can stuff the count.

Josh reads the list at /live-lessons/private (developer mode only).

Like the other modules this never imports app.py. app.py calls init_app(app).
"""

from flask import Blueprint, abort, jsonify, render_template, request, session
from flask_login import current_user

from access import active_tier
from extensions import limiter, rate_limit_key
from models import LiveLessonInterest, User, db

bp = Blueprint('live_lessons', __name__)

# What kind of lesson they'd want. The labels are shown on the page and on the
# private list.
FORMATS = {
    'one_to_one': 'One-to-one',
    'group':      'Small group',
    'either':     'Either is fine',
}
# "What would a one-hour lesson be worth to you?" Optional. Comparison point:
# a Singapore school charges from SGD 60 (about £35) for one-to-one on Zoom.
PRICE_BANDS = {
    'under_15': 'Under £15',
    '15_25':    '£15–25',
    '25_35':    '£25–35',
    'over_35':  'Over £35',
}
NOTE_MAX = 500


def my_interest():
    """This visitor's row, or None (signed out, or not on the list)."""
    if not current_user.is_authenticated:
        return None
    return LiveLessonInterest.query.filter_by(user_id=current_user.id).first()


def _json_only():
    # Same rule as the site's other POST routes: a form on someone else's
    # website can't send JSON without the browser checking with us first.
    if not request.is_json:
        abort(415)
    if not current_user.is_authenticated:
        abort(401)


@bp.route('/api/live-lessons/interest', methods=['POST'])
@limiter.limit('10 per hour', key_func=rate_limit_key)
def register_interest():
    _json_only()
    data = request.get_json(silent=True) or {}

    lesson_format = data.get('lesson_format') or 'either'
    if lesson_format not in FORMATS:
        return jsonify({'success': False,
                        'message': 'Please choose one of the lesson types.'}), 400
    price_band = data.get('price_band') or None
    if price_band is not None and price_band not in PRICE_BANDS:
        return jsonify({'success': False,
                        'message': 'Please choose one of the price options.'}), 400
    note = (data.get('note') or '').strip()
    if len(note) > NOTE_MAX:
        return jsonify({'success': False,
                        'message': f'Please keep it under {NOTE_MAX} characters.'}), 400

    row = my_interest()
    if row is None:
        row = LiveLessonInterest(user_id=current_user.id)
        db.session.add(row)
    row.lesson_format = lesson_format
    row.price_band = price_band
    row.note = note or None
    row.tier_at_signup = active_tier()
    db.session.commit()

    return jsonify({'success': True,
                    'message': "Thank you, you're on the list. If live lessons "
                               "start, you'll be the first to hear."})


@bp.route('/api/live-lessons/interest/withdraw', methods=['POST'])
def withdraw_interest():
    _json_only()
    row = my_interest()
    if row is not None:
        db.session.delete(row)
        db.session.commit()
    return jsonify({'success': True,
                    'message': "Done, you're off the list."})


@bp.route('/live-lessons/private')
def private_list():
    """Everyone who registered, newest first, with counts. Developer mode only."""
    if not session.get('user_progress', {}).get('is_developer'):
        abort(404)   # 404, not 403: don't advertise that the page exists
    rows = (db.session.query(LiveLessonInterest, User.username, User.email)
            .join(User, User.id == LiveLessonInterest.user_id)
            .order_by(LiveLessonInterest.created_at.desc()).all())
    by_format = {label: sum(1 for r, _, _ in rows if r.lesson_format == key)
                 for key, label in FORMATS.items()}
    by_price = {label: sum(1 for r, _, _ in rows if r.price_band == key)
                for key, label in PRICE_BANDS.items()}
    paying = sum(1 for r, _, _ in rows if r.tier_at_signup in ('basic', 'pro'))
    return render_template('live_lessons_private.html', rows=rows,
                           formats=FORMATS, by_format=by_format,
                           prices=PRICE_BANDS, by_price=by_price, paying=paying)


def init_app(app):
    app.register_blueprint(bp)
