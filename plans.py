"""What each plan includes and costs: the price list and the numbers it quotes.

SUBSCRIPTION_TIERS is the price list every page reads. The AI allowances, Pro's
fair-use ceiling and the Pronunciation switch live beside it because the plans'
feature lists quote them, so changing a number here changes the page too.

Only the NUMBERS live here. The code that spends the AI allowances (the pools,
which modes are free) stays in app.py, which imports these names back.
"""

import os


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
# 15 was set on 2026-06-06, when the tutor ran on Haiku. On Sonnet 5.5 a
# message costs about three times as much, and Thai Reader subscribers were
# getting exactly what Free got — paying bought no extra tutor at all. Free is
# now a real taste (5), and Thai Reader keeps the old 15. Settled with Josh
# 2026-10-14. Dhamma questions are a separate pool and are not affected.
FREE_AI_DAILY_LIMIT = 5                        # tutor messages/day, free tier


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
            f'✓ AI Thai tutor — {FREE_AI_DAILY_LIMIT} messages a day',
            f'✓ Dhamma Q&A — {FREE_DHAMMA_DAILY_LIMIT} questions a day, on its own allowance',
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
