"""Lifetime-value tracking: when a learner was last here, when they reached Level 3,
and why they cancelled.

Added 2026-11-18. Before this the app knew what each person had PAID (the
payments table) but not whether they were still learning, so it couldn't spot
someone drifting away before they cancelled, or say why people left.

Three small pieces:

  * touch_last_active() runs before each request and stamps today's date on a
    signed-in learner, at most once a day. One tiny write per learner per day,
    not one per page.
  * mark_level3() is called by add_xp the moment a learner first reaches
    Level 3, the level that earns their first free Basic section.
  * The goodbye page after cancelling asks one optional question, "what made
    you cancel?", and /api/cancel-reason saves the answer.

Nothing here is shown on the site. scripts/ltv_report.py reads it.

Like the other modules this never imports app.py. app.py calls init_app(app).
"""

from datetime import date

from flask import Blueprint, abort, current_app, jsonify, request
from flask_login import current_user

from extensions import limiter, rate_limit_key
from models import db, utcnow

bp = Blueprint('activity', __name__)

LEVEL3 = 3   # the same level as EARNED_UNLOCK_LEVEL and REVIEW_MIN_LEVEL

# What the goodbye page offers, in the order it shows them. The keys are
# stored; the words are only for the page and the report.
CANCEL_REASONS = {
    'too_expensive':   "It costs more than I want to spend",
    'not_using':       "I'm not using it enough",
    'missing_feature': "It's missing something I need",
    'learned_enough':  "I've learned what I needed",
    'other_app':       "I'm using something else instead",
    'other':           "Something else",
}
COMMENT_MAX = 1000


def touch_last_active():
    """Before each request: stamp today on a signed-in learner, once a day."""
    if request.endpoint == 'static' or not current_user.is_authenticated:
        return
    today = date.today()
    if current_user.last_active_on == today:
        return
    try:
        current_user.last_active_on = today
        db.session.commit()
    except Exception:
        # A bookkeeping hiccup must never break the page they asked for.
        db.session.rollback()
        current_app.logger.exception('Could not record last_active_on')


def mark_level3(old_level, new_level):
    """Stamp the first time a signed-in learner reaches Level 3.

    No commit here: add_xp marks the session modified, and the progress save
    at the end of the request (progress._persist_user_progress) commits the
    user row along with it."""
    if old_level >= LEVEL3 or new_level < LEVEL3:
        return
    if not current_user.is_authenticated or current_user.level3_reached_at:
        return
    current_user.level3_reached_at = utcnow()


@bp.route('/api/cancel-reason', methods=['POST'])
@limiter.limit('10 per hour', key_func=rate_limit_key)
def save_cancel_reason():
    if not request.is_json:
        abort(415)
    if not current_user.is_authenticated:
        abort(401)
    # Only someone who has actually cancelled can say why.
    if not current_user.canceled_at and current_user.subscription_status not in (
            'canceling', 'canceled'):
        return jsonify({'success': False,
                        'message': "There's no cancelled subscription on this account."}), 400

    data = request.get_json(silent=True) or {}
    reason = data.get('reason')
    if reason not in CANCEL_REASONS:
        return jsonify({'success': False,
                        'message': 'Please pick one of the options.'}), 400
    comment = (data.get('comment') or '').strip()
    if len(comment) > COMMENT_MAX:
        return jsonify({'success': False,
                        'message': f'Please keep it under {COMMENT_MAX} characters.'}), 400

    current_user.cancel_reason = reason
    current_user.cancel_comment = comment or None
    db.session.commit()
    return jsonify({'success': True,
                    'message': 'Thank you for telling us. It really helps.'})


def init_app(app):
    app.before_request(touch_last_active)
    app.register_blueprint(bp)
