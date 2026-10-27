"""Points: what each action earns, the daily drill cap, and awarding XP.

add_xp() applies the visitor's plan multiplier, so it reads the plan through
access.active_tier(); the XP-to-level maths stays in progress.py.

Moved out of app.py so routes in their own modules can award XP without
importing app.py. app.py imports these names back.
"""

from datetime import datetime

from flask import session

from access import active_tier
from plans import SUBSCRIPTION_TIERS
from progress import get_user_level, init_user_progress


# Ceiling on XP earned from practice drills in one day.
#
# The drills are generated in the browser, so the answer is already on the page
# and /api/check_answer cannot tell a learner from a script — nothing it is
# sent can prove the question was really faced. Verifying harder is not the
# answer; bounding the reward is. 200 is twenty correct answers, comfortably
# more than a real sitting, and it caps a scripted run at a couple of days'
# honest work rather than an instant level 10.
#
# This matters more since levelling started earning a free paid section: XP is
# no longer only a score, it opens a door. The counter lives in user_progress
# rather than a bare session key so it is saved with the rest of a learner's
# progress and a cookie wipe does not hand back a fresh allowance.
DRILL_XP_DAILY_CAP = 200


# Points awarded for different actions
POINT_REWARDS = {
    'quiz_correct': 10,
    'quiz_perfect': 50,
    'first_visit': 5,
    'daily_login': 15,
    'complete_lesson': 30,
    'unlock_section': 25,
}


def drill_xp_today():
    """Today's drill-XP tally for this learner, resetting at midnight."""
    init_user_progress()
    user = session['user_progress']
    today = datetime.now().strftime('%Y-%m-%d')
    if user.get('drill_xp_date') != today:
        user['drill_xp_date'] = today
        user['drill_xp_today'] = 0
        session.modified = True
    return user.get('drill_xp_today', 0)


def add_xp(points, action_description=""):
    """Add XP to user and check for level up"""
    init_user_progress()
    user = session['user_progress']

    tier = active_tier()
    multiplier = SUBSCRIPTION_TIERS[tier].get('points_multiplier', 1)
    points = int(points * multiplier)
    
    old_level = user['level']
    user['xp'] += points
    user['level'] = get_user_level(user['xp'])
    
    level_up = user['level'] > old_level
    
    session.modified = True
    
    return {
        'points_earned': points,
        'total_xp': user['xp'],
        'level': user['level'],
        'level_up': level_up,
        'action': action_description
    }
