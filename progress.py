"""A learner's progress: where it starts, how it is saved, and what level it is.

Progress (XP, level, streak, achievements, settings such as Monk Mode) is
worked on in the session cookie and saved to User.progress, so it survives
cleared cookies and a second device. This module owns that round trip:

  * init_user_progress()  — the starting values for a new visitor;
  * save_user_progress()  — session → database, filtered (see below);
  * load_user_progress()  — database → session at login;
  * get_user_level() and get_xp_for_next_level() — the XP table's maths.

What progress UNLOCKS — the section gates, subscriptions, the earned
unlock — stays in app.py. Those rules are tied to billing
and to each other, and moving them would only move the tangle.

Like every other module this never imports app.py. app.py calls init_app(app)
once, which saves progress after each request and restores it on login.
"""

from datetime import datetime, timedelta

from flask import current_app, session
from flask_login import current_user, user_logged_in

from models import db


# Points required for each level
XP_LEVELS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5500,
    9: 8000,
    10: 12000,
}


def get_user_level(xp):
    """Calculate user level based on XP"""
    for level in sorted(XP_LEVELS.keys(), reverse=True):
        if xp >= XP_LEVELS[level]:
            return level
    return 1

def get_xp_for_next_level(current_level):
    """Get XP required for next level"""
    if current_level >= max(XP_LEVELS.keys()):
        return None
    return XP_LEVELS[current_level + 1]


# The two learning directions Monk Mode supports.
MONK_DIRECTIONS = {'learn_thai', 'learn_english'}
MONK_DIRECTION_DEFAULT = 'learn_thai'   # a monk learning Thai

# The two English accents the learn_english side can be shown in.
# British is the default because the whole existing system was built to it: the
# IPA, the respellings and every generated MP3 (en-GB-SoniaNeural) are RP. The
# American column is an addition on top, not a replacement.
#
# Most entries sound the same in both accents, so content stores ONE respelling
# plus an override ONLY where they actually differ (see monk_respell below).
# That keeps ~100 of the 140 entries single-valued and, more importantly, keeps
# the number of lines Josh has to review down to the ones that genuinely change.
MONK_ACCENTS = {'uk', 'us'}
MONK_ACCENT_DEFAULT = 'uk'


def init_user_progress():
    """Initialize user progress in session if not exists"""
    if 'user_progress' not in session:
        session['user_progress'] = {
            'xp': 0,
            'level': 1,
            'subscription_tier': 'free',
            'subscription_expires': None,
            'is_developer': False,
            'monk_mode': False,   # opens the free monk lesson track only (code-gated)
            'monk_direction': MONK_DIRECTION_DEFAULT,   # 'learn_thai' or 'learn_english'
            'monk_accent': MONK_ACCENT_DEFAULT,   # 'uk' or 'us' (English-side accent)
            'full_unlock': False,  # optional paid add-on (on top of Pro): skips the level grind
            'sections_unlocked': ['home', 'alphabet', 'theravada'],
            'sections_visited': [],
            'achievements_earned': [],
            'quizzes_completed': 0,
            'quiz_perfect_count': 0,
            'words_learned': 0,
            'correct_answers': 0,
            'total_answers': 0,
            'login_streak': 1,
            'last_login': datetime.now().isoformat(),
            'daily_points_earned': 0,
            'alphabet_completed': False,
            'alphabet_completed_at': None,
        }
        session.modified = True

# Keys that are deliberately NOT written to User.progress.
#
# The first five have real columns on User, and those columns are the source of
# truth — persisting them here too would let a stale saved blob hand someone a
# subscription or unlock the alphabet. is_developer is different: it is kept out
# because a privileged flag should be re-earned with the password each session,
# never restored from storage. user_id and username are identity, set at login.
_PROGRESS_NOT_SAVED = {
    'subscription_tier', 'subscription_expires', 'full_unlock',
    'earned_unlock_section',
    'alphabet_completed', 'alphabet_completed_at',
    'is_developer', 'user_id', 'username',
}

def save_user_progress():
    """Mirror the session's progress dict onto the logged-in user's row.

    Assigns a brand-new dict rather than mutating the existing one: SQLAlchemy
    spots an attribute assignment, but an in-place edit of a JSON column goes
    unnoticed and would never be written.
    """
    if not current_user.is_authenticated:
        return
    progress = session.get('user_progress')
    if not progress:
        return
    current_user.progress = {k: v for k, v in progress.items()
                             if k not in _PROGRESS_NOT_SAVED}
    db.session.commit()

# How long anonymous progress stays adoptable. Someone who tries the alphabet
# quiz in the morning and signs up that evening keeps their XP; a cookie from
# yesterday is treated as belonging to a different visit — which on a shared
# monastery or library machine may well mean a different person.
ANONYMOUS_PROGRESS_MAX_AGE = timedelta(hours=12)


def _anonymous_progress_is_stale():
    """True when the progress in this session is too old to belong to this visit.

    last_login is written once when a session's progress is created and never
    updated anywhere, which makes it an accurate "when did this browser start
    earning" stamp. Anything unreadable or missing counts as stale: inheriting
    progress of unknown age is the outcome worth avoiding.
    """
    progress = session.get('user_progress') or {}
    started = progress.get('last_login')
    if not started:
        return True
    try:
        age = datetime.now() - datetime.fromisoformat(started)
    except (TypeError, ValueError):
        return True
    return age > ANONYMOUS_PROGRESS_MAX_AGE


def _restore_saved_progress(sender, user, **extra):
    """Every login — /login, /signup, a password reset — goes through
    login_user() in auth.py, which sends this signal. Restoring progress here
    keeps the gamification out of the account routes entirely.

    Skipped when this session already belongs to the same user: changing a
    password re-issues the cookies of a learner who is already signed in, and
    reloading the saved copy then could rewind progress the session holds."""
    if session.get('user_progress', {}).get('user_id') == user.id:
        return
    load_user_progress(user)


def load_user_progress(user):
    """Seed the session from the database when a user logs in.

    The database wins over whatever is already in the session. Someone can
    browse and earn XP logged out, then sign in — and their real, saved progress
    has to be the one that survives, not the anonymous cookie they happened to
    arrive with. Defaults are laid down first so a saved blob written before a
    new counter existed still gets that counter.

    A user with no saved progress yet (their first login since this shipped)
    keeps the session they have, which is then written on the way out.
    """
    # A brand-new account inherits whatever this browser was carrying — that is
    # how trying the quiz before registering keeps its XP. But only from THIS
    # visit. Without the age check a two-day-old cookie resurrects itself onto a
    # fresh account, which looks exactly like a database that failed to clear,
    # and on a shared computer hands one person another's progress.
    if not user.progress and _anonymous_progress_is_stale():
        session.pop('user_progress', None)

    init_user_progress()
    if user.progress:
        # Filtered on the way in as well as on the way out. Nothing should ever
        # write these keys, so this is belt-and-braces — but it means a blob
        # from an older version, a hand-edited row, or a future bug still can't
        # put a misleading tier in front of the user. Access is gated on the
        # columns either way (active_tier), so this is about not showing someone
        # "Pro" in the interface while the database says free.
        session['user_progress'].update(
            {k: v for k, v in user.progress.items() if k not in _PROGRESS_NOT_SAVED}
        )
    session['user_progress']['user_id']  = user.id
    session['user_progress']['username'] = user.username
    session.modified = True


def _persist_user_progress(response):
    """Save progress at the end of any request that changed it.

    One hook instead of a save call at each of the ~30 places that touch
    user_progress: they all already set session.modified, so that flag is the
    signal. Wrapped in try/except because a database hiccup must not turn a
    working page into a 500 — the worst case is one lost XP update, and the
    next request writes it again.
    """
    try:
        if session.modified and current_user.is_authenticated:
            save_user_progress()
    except Exception:
        db.session.rollback()
        current_app.logger.exception('Could not save user progress')
    return response


def init_app(app):
    """Save progress after every request that changed it, and restore the saved
    copy whenever someone logs in."""
    app.after_request(_persist_user_progress)
    user_logged_in.connect(_restore_saved_progress, app)
