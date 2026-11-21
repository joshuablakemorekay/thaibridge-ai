"""What each plan includes and costs: the price list and the numbers it quotes.

SUBSCRIPTION_TIERS is the price list every page reads. The AI allowances, Pro's
fair-use ceiling and the Pronunciation switch live beside it because the plans'
feature lists quote them, so changing a number here changes the page too.

Only the NUMBERS live here. The code that spends the AI allowances (the pools,
which modes are free) stays in app.py, which imports these names back.
"""

import os


# AI limits. Since 2026-11-21 the AI is for PAYING plans only: Thai Reader gets
# the Tutor and Dhamma modes with a daily allowance, Pro gets every mode up to a
# fair-use ceiling. Free gets none. Every reply is paid for out of Josh's own
# pocket, there were no subscribers yet to cover it, and the old free taste
# (5 tutor + 5 Dhamma a day, counted in the session cookie) could be reset by
# clearing cookies, so it was an open tap on the API bill. Settled with Josh
# 2026-11-21. The Dhamma PAGES stay free to everyone; only asking the AI a
# question needs a plan.
#
# The allowances are counted in the ai_usage table per account now, not in
# the session (app._ai_usage_today), so clearing cookies resets nothing.
#
# History: Thai Reader's 15 was set on 2026-06-06 on Haiku; Free was a taste of
# 5 from 2026-10-14 until it was removed.
FREE_AI_DAILY_LIMIT = 0                        # Free has no AI (see above)


BASIC_AI_DAILY_LIMIT = 15                      # tutor messages/day, Thai Reader


# The Dhamma gets its OWN daily allowance, drawn from a separate counter.
#
# Sharing one pool quietly broke the promise made just above. Tutor and Dhamma
# both spent the same 15, so a learner who drilled Thai vocabulary all morning
# and then asked a question about the precepts was told to come back tomorrow
# or upgrade. The teaching was never behind the paywall, but the question about
# it sat behind a language-study budget — the same line, reached by a side
# door.
#
# This is added ON TOP of the tutor allowance rather than reserved out of it.
# Reserving would have cut everyone's tutor allowance (then 15) to 10 to fund a
# fix for a promise we had already made; nobody should lose something so that
# we can keep our word. At about 0.85p a message on Sonnet 5.5 it is about 4p
# a day for someone who exhausts it daily, which almost nobody will.
#
# The name is older than the paid-only rule: this is now the daily Dhamma
# allowance for Thai Reader. (Pro has no pools, just the fair-use ceiling.)
FREE_DHAMMA_DAILY_LIMIT = 5


# Pro is "unlimited" in the sense that matters to a learner, but not literally:
# without a ceiling, one subscriber could run up more in API costs than they pay.
# Was 150 on Haiku 4.5 at 0.285p a message. Sonnet 5.5 (2026-10-09) costs about
# 0.85p for a fresh message and 0.3p for a cached follow-up in the same chat, so
# 150 a day could cost more than the £16.58 a month annual Pro brings in. At 75,
# a learner who maxes it out every day costs about £10 a month on a realistic mix
# of fresh and follow-up messages, so Pro stays profitable. 75 is also the floor
# test_the_ceiling_is_far_above_the_free_allowance sets (five times free), so
# Pro stays clearly worth paying for. The Anthropic Console spend limit is the
# hard backstop if anyone ever finds a pattern that costs more.
#
# Anyone who reaches it is not studying, and the reply says so kindly and
# invites them to get in touch rather than treating them as an abuser.
PRO_FAIR_USE_DAILY = 75


# Pronunciation Analysis (🎤 Say it) is built but HIDDEN until a native speaker
# has tried it (docs/pronunciation-review-*.xlsx): it cannot yet tell the mid
# tone from the low one, and it should not be sold in Pro before someone who
# hears Thai tones natively says its scores are fair. Two Render settings:
#   PRONUNCIATION_TESTERS  usernames (comma-separated) who see it meanwhile,
#                          so the reviewer can test it on their Pro account
#   PRONUNCIATION_LIVE=1   on for every Pro learner, with its Premium card and
#                          Pro feature line
# Render restarts the app when a setting changes, so no code change is needed.
PRONUNCIATION_LIVE = os.environ.get('PRONUNCIATION_LIVE', '').strip() == '1'


def pronunciation_testers():
    raw = os.environ.get('PRONUNCIATION_TESTERS', '')
    return {name.strip().lower() for name in raw.split(',') if name.strip()}


# Subscription tiers
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'FREE Explorer (FREE)',
        'price': 0,
        'features': [
            '✓ Thai alphabet — chart, flashcards & quiz',
            '✓ Theravada Buddhism teachings',
            '✓ Dhamma talks, in Thai and English wherever a translation exists',
            '✓ Pra Kru Bob Dhamma articles',
            '✓ Guided meditation sessions, timer & techniques',
            '✓ ThaiBridge Spelling guide',
            '✓ Progress tracking & levelling',
        ],
        'max_level_access': 5,
    },
    'basic': {
        'name': 'Thai Reader (Basic)',
        'price': 9.99,
        # Annual is priced at ten months, so a year up front saves two. It is a
        # separate number rather than a computed discount because the round
        # figure is the offer — £99 reads as a price, £99.90 reads as arithmetic.
        'price_year': 99.00,
        'features': [
            '✓ Everything in FREE',
            '✓ Vowels, syllables & Read & Write Script',
            '✓ Tones & consonant classes',
            '✓ Vocabulary, grammar & lessons',
            '✓ Sentences & conversations, with audio',
            '✓ Culture, formality, register & gender guides',
            '✓ Themed exercise sets',
            '✓ Tour Guide & Business Thai',
            f'✓ AI Thai tutor — {BASIC_AI_DAILY_LIMIT} messages a day',
            f'✓ AI Dhamma Q&A — {FREE_DHAMMA_DAILY_LIMIT} questions a day, on its own allowance',
            '✓ 2x points multiplier',
        ],
        'max_level_access': 7,
        'points_multiplier': 2,
    },
    'pro': {
        'name': 'Thai Master (Pro)',
        'price': 19.99,
        'price_year': 199.00,
        'features': [
            '✓ Everything in Thai Reader',
            f'✓ Unlimited AI chat — every mode, fair use up to {PRO_FAIR_USE_DAILY}/day',
            '✓ AI conversation partner with roleplay scenarios',
            '✓ Culture AI Q&A',
            '✓ AI exercise generator',
            '✓ AI translator, English to Thai and back',
            *(['✓ Pronunciation Analysis — see your tone next to the model\'s']
              if PRONUNCIATION_LIVE else []),
            '✓ Thai–English dictionary',
            '✓ 3x points multiplier',
            '✓ Priority support',
        ],
        'max_level_access': 10,
        'points_multiplier': 3,
    }
}
