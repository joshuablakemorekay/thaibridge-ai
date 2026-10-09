# app.py at 740f71b, lines 503-696
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
    'grammar': {'level': 3, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    # Consonant classes + tone rules. Its content was moved here from the Grammar
    # page, so it's gated the same way — Basic tier, level 3.
    'tones_classes': {'level': 3, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'culture': {'level': 3, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
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
    # /api/ai/chat route, and Monk Mode never lifts the AI cap.
    'dictionary': {'level': 8, 'tier': 'pro', 'points_reward': 50, 'requires_alphabet': True},
    'premium': {'level': 10, 'tier': 'pro', 'points_reward': 100, 'requires_alphabet': True},
}

# Freemium AI limits. Free & Basic get the Tutor mode plus Dhamma, capped at a
# few messages a day between them. Pro unlocks every mode with no cap. Dhamma is
# free because the teachings on this site are free — charging for the follow-up
# question would be selling the Dhamma, the same line we refused to cross when
# Meditation went back to the free tier. The daily cap isn't a toll on the
# teaching, it's the honest cost of running the model. The daily counter lives in
# the SESSION (not the DB) on purpose — it needs no schema change and also works
# for logged-out visitors. It's a soft limit (a determined user could clear
# cookies to reset it), which is fine for a portfolio/demo app. Defined here,
# above SUBSCRIPTION_TIERS, so the Free tier's feature list can quote the real
# number instead of a hardcoded one that goes stale.
FREE_AI_DAILY_LIMIT = 15                       # messages/day for free & basic tiers

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
FREE_AI_ALLOWED_MODES = {'tutor', 'buddhist'}  # AI modes free & basic can use

# Pro is "unlimited" in the sense that matters to a learner, but not literally:
# without a ceiling, one subscriber could run up more in API costs than they pay.
# At 0.285p worst case per message (a full 500-token reply on top of the ~1,100
# token system prompt), 150 a day is £12.84 a month against £19.99 of revenue —
# still profitable even if someone maxes it out every single day of the month.
#
# The number is chosen to be invisible: ten times the free allowance, and roughly
# three times what a genuinely heavy day of study looks like. Anyone who reaches
# it is not studying, and the reply says so kindly and invites them to get in
# touch rather than treating them as an abuser.
PRO_FAIR_USE_DAILY = 150

# Subscription tiers
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free Explorer (Free)',
        'price': 0,
        'features': [
            '✓ Thai alphabet — chart, flashcards & quiz',
            '✓ Theravada Buddhism teachings',
            '✓ Dhamma talks in Thai & English',
            '✓ Pra Kru Bob Dhamma articles',
            '✓ Guided meditation sessions, timer & techniques',
            f'✓ AI Tutor & Dhamma Q&A — {FREE_AI_DAILY_LIMIT} messages a day',
            '✓ Paiboon romanization guide',
            '✓ Progress tracking & levelling',
        ],
        'max_level_access': 5,
    },
    'basic': {
        'name': 'Thai Reader (Basic)',
        'price': 9.99,
        'features': [
            '✓ Everything in Free',
            '✓ Vowels, syllables & Read & Write Script',
            '✓ Tones & consonant classes',
            '✓ Vocabulary, grammar & lessons',
            '✓ Sentences & conversations, with audio',
            '✓ Culture, formality, register & gender guides',
            '✓ Themed exercise sets',
            '✓ Tour Guide & Business Thai',
            '✓ 2x points multiplier',
        ],
        'max_level_access': 7,
        'points_multiplier': 2,
    },
    'pro': {
        'name': 'Thai Master (Pro)',
        'price': 19.99,
        'features': [
            '✓ Everything in Thai Reader',
            f'✓ Unlimited AI chat — every mode, fair use up to {PRO_FAIR_USE_DAILY}/day',
            '✓ AI conversation partner with roleplay scenarios',
            '✓ Culture AI Q&A',
            '✓ AI exercise generator',
            '✓ Thai–English dictionary',
            '✓ 3x points multiplier',
            '✓ Priority support',
        ],
        'max_level_access': 10,
        'points_multiplier': 3,
    }
}

# Optional one-time add-on sold on top of Thai Master (Pro): the Instant Access
# Pass flips full_unlock, skipping the level gates so every section
# opens instantly. Built with inline Stripe pricing (no dashboard product needed).
INSTANT_ACCESS_ADDON = {
    'name': 'Instant Access Pass',
    'price': 14.99,
    'blurb': 'A one-time unlock for Thai Master members — open every section instantly, with no levelling.',
}

# app.py at 740f71b, lines 1426-1482
def check_section_access(section_id):
    """Check whether the current user can open a section.

    Three independent gates, checked in order: alphabet completion, level/XP,
    and subscription tier. Developer mode bypasses all of them.

    Monk Mode waives ONLY the subscription-tier gate — every content section
    becomes free — while still requiring alphabet completion and the right
    level. Monks earn their way up by levelling like everyone else; they just
    never hit the paywall. (The AI usage cap is enforced separately in the
    chat route, so Monk Mode never makes the costly AI tutor unlimited.)
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

    # Gate 3 — subscription tier (payment). Monk Mode waives THIS, and only
    # this, free of charge. Everyone else is held to their real tier.
    if tier_still_owed(requirements['tier'], user):
        # ...unless this is the one section they opened by levelling. It waives
        # payment for that section alone and never the level gate above it.
        if earned_unlock_spent_on() == section_id:
            return True, "Opened with your earned unlock"
        tier_name = SUBSCRIPTION_TIERS[requirements['tier']]['name']
