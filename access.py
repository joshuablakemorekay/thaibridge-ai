"""Who can open what: the section gates, plans, the alphabet and the earned unlock.

check_section_access() is the one question every gated page asks. It runs
three gates in order (alphabet, level, plan), and this module holds everything
those gates read: SECTION_REQUIREMENTS, the visitor's active plan, the Instant
Access Pass, alphabet completion and the free earned-unlock section.

Moved out of app.py so routes in their own modules (Blueprints) can ask the
same question without importing app.py. app.py imports these names back.
"""

from flask import session
from flask_login import current_user

from plans import SUBSCRIPTION_TIERS
from progress import init_user_progress


# Section unlock requirements (level and/or subscription tier)
SECTION_REQUIREMENTS = {
    # ── FREE for everyone (whether Monk Mode is on or off) ────────────────
    # The free foundation: the Theravada Dhamma teachings — the Dhamma itself
    # is freely given.
    # Every other content section sits behind a paid tier (see below), on TOP
    # of its level/XP requirement.
    #
    # Meditation moved to 'basic' for a while, on the reasoning that the page had
    # grown from a bare timer into practice *tooling*. It is back here now: sitting
    # in meditation is not tooling, it is the practice the teachings are for, and
    # splitting "the Dhamma is free but learning to practise it costs £9.99" was a
    # line that could not be defended. Dhamma Talks sit here for the same reason.
    'home': {'level': 1, 'tier': 'free', 'points_reward': 0},
    # The alphabet is free on purpose. It is the prerequisite for every
    # section below, so charging for it would put the whole site behind the
    # paywall with no way in.
    'alphabet': {'level': 1, 'tier': 'free', 'points_reward': 100, 'requires_alphabet': False},
    # Survival Thai is the free tier's answer to "I want to SPEAK Thai". Free
    # and, crucially, requires_alphabet=False: every other language section
    # demands the alphabet quiz first, which is the right prerequisite for
    # reading and the wrong one for saying hello. Gating a starter set behind
    # 44 consonants is how a beginner leaves.
    'survival': {'level': 1, 'tier': 'free', 'points_reward': 60, 'requires_alphabet': False},
    # Expat2000 is free and alphabet-free for the same reason: it is found by
    # people searching "Thailand DTV visa", and the course is what they
    # discover on the way. A paywall here would just send them back to Google.
    'expat2000': {'level': 1, 'tier': 'free', 'points_reward': 40, 'requires_alphabet': False},
    # The page that separates the universal teaching from the Thai
    # expression of it. It is the answer to "do I have to become Thai to
    # learn Buddhism here?", so it must never itself be behind a gate.
    'dhamma_and_culture': {'level': 1, 'tier': 'free', 'points_reward': 0, 'requires_alphabet': False},
    # The practice itself, with no culture attached — the Canon's own lay
    # frameworks. Free and ungated for the same reason as the page above it.
    'practising_anywhere': {'level': 1, 'tier': 'free', 'points_reward': 0, 'requires_alphabet': False},
    'theravada': {'level': 1, 'tier': 'free', 'points_reward': 40},
    'meditation': {'level': 1, 'tier': 'free', 'points_reward': 40},
    # Chanting sits with the other Dhamma pages: the chants and their
    # translations are not ours to sell, and there is no alphabet
    # prerequisite — you do not need to read Thai to chant along.
    'chanting': {'level': 1, 'tier': 'free', 'points_reward': 40},
    # Paiboon was Basic for a while, filed with the Learn menu it sits in. It is
    # free now because the free pages already USE it: the chanting layers and the
    # meditation techniques print Paiboon on screen. Charging for the guide meant
    # showing a free reader "kam buu-chaa" and then selling them the key to it —
    # a notation key is not a lesson, it is the legend on the map.
    # ...and with no alphabet prerequisite, for the same reason it is free. The
    # pages that print Paiboon — chanting and meditation — have no alphabet gate
    # themselves ("you do not need to read Thai to chant along"), so requiring
    # the 44 consonants before the KEY to the notation kept the door shut for
    # exactly the reader it was freed for.
    'paiboon': {'level': 1, 'tier': 'free', 'points_reward': 10, 'requires_alphabet': False},

    # ── BASIC — Thai Reader (£9.99) ─────────────────────────────────
    # The structured language-learning content (the rest of the Learn menu,
    # Culture, and the exercises). Still gated by level/XP as well as the tier.
    # Vocabulary sits in the Learn menu alongside the sections below, so it carries
    # the same alphabet prerequisite. It also earns XP on unlock like every one of
    # its siblings — a 0 reward made its locked page read "+0 XP upon unlock" while
    # the rest promised something.
    'learn': {'level': 1, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'exercise_festivals': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_isan_dialect': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'vowels_syllables': {'level': 2, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'read_write': {'level': 2, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'exercise_nature': {'level': 3, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_formal': {'level': 3, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_everyday': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_theravada_dhamma': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'grammar': {'level': 3, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    # Consonant classes + tone rules. Its content was moved here from the Grammar
    # page, so it's gated the same way — Basic tier, level 3.
    'tones_classes': {'level': 3, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    # Culture is the one gated section that never needed the alphabet. It is
    # about the wai, temple manners and festivals — roughly two-thirds English
    # prose, and every Thai word on it is printed with its romanisation. Asking
    # someone to name 35 of 44 consonants before they may read about bowing
    # gated an English page behind a script exam. Level 3 and the Basic tier
    # still apply, so the progression and the paywall are untouched; only the
    # prerequisite that did no teaching work is gone.
    'culture': {'level': 3, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': False},
    'lessons': {'level': 4, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},
    'register': {'level': 4, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'formality': {'level': 4, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'gender_examples': {'level': 4, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'sentences': {'level': 5, 'tier': 'basic', 'points_reward': 35, 'requires_alphabet': True},
    'greetings_wai': {'level': 5, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},
    'classifiers': {'level': 5, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},
    'tour_guide': {'level': 4, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'business_thai': {'level': 5, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},

    # ── PRO — Thai Master (£19.99) ───────────────────────────────────────
    # The premium power tools. Unlimited AI is enforced separately in the
    # /api/ai/chat route.
    'dictionary': {'level': 8, 'tier': 'pro', 'points_reward': 50, 'requires_alphabet': True},
    # No requires_alphabet here, deliberately. /premium is the PRICING page: it
    # carries no @require_access, so the flag never fired — but it read as "pass
    # a quiz before you may see our prices", and it would have become true the
    # day someone added the decorator for consistency. The entry itself stays,
    # because the tier and level are quoted elsewhere.
    'premium': {'level': 10, 'tier': 'pro', 'points_reward': 100},
}


def active_tier():
    """The subscription tier to enforce RIGHT NOW — the single source of truth.

    For a logged-in user this comes from the DATABASE (User.effective_tier,
    which already accounts for expiry and cancellation). For an anonymous
    visitor we fall back to the session (which is 'free' by default).
    """
    if current_user.is_authenticated:
        return current_user.effective_tier
    return session.get('user_progress', {}).get('subscription_tier', 'free')


def has_full_unlock():
    """Whether the current visitor holds the one-time 'Instant Access Pass'
    add-on. For a logged-in user the DATABASE is the source of truth; anonymous
    visitors fall back to the session copy."""
    if current_user.is_authenticated:
        return bool(getattr(current_user, 'full_unlock', False))
    return session.get('user_progress', {}).get('full_unlock', False)


# ── The earned unlock ────────────────────────────────────────────────────────
# One paid section, opened by levelling instead of by paying.
#
# Every free-tier section is level 1, so XP earned on the free content unlocked
# nothing at all: a free learner watched a progress bar fill toward a reward
# that did not exist. This gives it one. On reaching EARNED_UNLOCK_LEVEL a
# learner may open a single Thai Reader section, permanently, for nothing.
#
# Level 3 is 250 XP and the free sections are worth roughly 360 between them,
# so it is reached by finishing what is already free rather than by grinding
# drills. Deliberately ONE section, deliberately Basic only, and deliberately
# limited to sections whose level they have already met — a door held open, not
# a tier given away. The section they pick is the one they wanted most, which
# makes it the best possible thing for them to have read before seeing a price.
EARNED_UNLOCK_LEVEL = 3


EARNED_UNLOCK_TIER = 'basic'


def earned_unlock_spent_on():
    """The section this learner spent their earned unlock on, or None.

    Signed-out visitors never have one. Claiming it requires an account, because
    an entitlement kept in a cookie is one that clearing cookies mints again —
    a new free section per browser wipe.
    """
    if current_user.is_authenticated:
        return current_user.earned_unlock_section
    return None


def earned_unlock_status():
    """What to tell this learner about their earned unlock, for the dashboard.

    The progress page is where the XP bar lives, so it is where the bar's
    destination has to be named. Without this the reward was only discoverable
    by chance — you found out you had one by opening a locked section and seeing
    the button.
    """
    spent = earned_unlock_spent_on()
    if spent:
        return {
            'state': 'spent',
            'section': spent,
            'section_name': spent.replace('_', ' ').title(),
        }
    user = session.get('user_progress') or {}
    if user.get('level', 1) >= EARNED_UNLOCK_LEVEL:
        return {'state': 'available', 'section': None, 'section_name': None}
    return {
        'state': 'locked',
        'level': EARNED_UNLOCK_LEVEL,
        'section': None,
        'section_name': None,
    }


def earned_unlock_offer(section_id):
    """Can this learner open `section_id` with their earned unlock right now?

    Requires the level they have reached to already cover the section. Offering
    a Level 5 section to a Level 3 learner would spend their one unlock on a
    door that stays shut behind the level gate.
    """
    if earned_unlock_spent_on():
        return False
    user = session.get('user_progress') or {}
    if user.get('level', 1) < EARNED_UNLOCK_LEVEL:
        return False
    requirements = SECTION_REQUIREMENTS.get(section_id)
    if not requirements or requirements['tier'] != EARNED_UNLOCK_TIER:
        return False
    if user.get('level', 1) < requirements['level']:
        return False
    return tier_still_owed(requirements['tier'], user)


def tier_still_owed(required_tier, user):
    """Does this user still have to pay for a section on `required_tier`?

    Pulled out of gate 3 so gate 2 can ask the same question without repeating
    the hierarchy. Monk Mode does not change the answer — it opens the monk
    track only, never a paid section.
    """
    tier_hierarchy = {'free': 0, 'basic': 1, 'pro': 2}
    return tier_hierarchy[active_tier()] < tier_hierarchy[required_tier]


def check_section_access(section_id):
    """Check whether the current user can open a section.

    Three independent gates, checked in order: alphabet completion, level/XP,
    and subscription tier. Developer mode bypasses all of them.

    Monk Mode plays no part here: it opens the monk track (its own routes)
    and leaves every section below gated exactly as it is with Monk Mode off.
    """
    init_user_progress()
    user = session['user_progress']

    # Developer mode bypasses everything
    if user.get('is_developer', False):
        return True, "Developer Access"

    if section_id not in SECTION_REQUIREMENTS:
        return True, "No restrictions"

    requirements = SECTION_REQUIREMENTS[section_id]

    # The optional "full unlock" add-on (a paid extra on top of Thai Master)
    # removes the progression grind: it skips the alphabet and level gates so
    # everything opens instantly. It never touches the tier gate (it's sold on
    # top of Pro, which already grants tier access) nor the AI usage cap.
    full_unlock = has_full_unlock()

    # Gate 1 — alphabet completion (skipped by the full-unlock add-on)
    if not full_unlock and requirements.get('requires_alphabet', False):
        if not check_alphabet_completion():
            return False, "Complete Thai Alphabet first"

    # Gate 2 — level / XP (skipped by the full-unlock add-on)
    #
    # The message names the payment as well, when one is still owed. The gates
    # are checked in order and only the FIRST failure was ever reported, so a
    # free learner looking at Level 5 Sentences was told "Requires Level 5",
    # could grind all the way there, and only then discover a paywall behind
    # it. The dashboard has always quoted both; the section itself did not.
    if not full_unlock and user['level'] < requirements['level']:
        message = f"Requires Level {requirements['level']}"
        if tier_still_owed(requirements['tier'], user):
            tier = SUBSCRIPTION_TIERS[requirements['tier']]
            message += f" + {tier['name']} (£{tier['price']:.2f}/mo)"
        return False, message

    # Gate 3 — subscription tier (payment). Everyone is held to their real tier.
    if tier_still_owed(requirements['tier'], user):
        # ...unless this is the one section they opened by levelling. It waives
        # payment for that section alone and never the level gate above it.
        if earned_unlock_spent_on() == section_id:
            return True, "Opened with your earned unlock"
        tier_name = SUBSCRIPTION_TIERS[requirements['tier']]['name']
        return False, f"Requires {tier_name} subscription"

    return True, "Access granted"


def check_alphabet_completion():
    """Has this visitor passed the alphabet?

    Same split as active_tier() and has_full_unlock(): for a logged-in user the
    DATABASE is the source of truth, because the alphabet gates every other
    section and must survive a cleared cookie or a move to another device.
    Anonymous visitors have nowhere to persist it, so they fall back to the
    session and lose it when the cookie goes.

    A logged-in user's session copy is refreshed on the way past, so anything
    reading session['user_progress'] directly sees the truth too.
    """
    init_user_progress()
    user = session['user_progress']

    if current_user.is_authenticated:
        done = bool(getattr(current_user, 'alphabet_completed', False))
        if user.get('alphabet_completed') != done:
            user['alphabet_completed'] = done
            session.modified = True
        return done

    return user.get('alphabet_completed', False)
