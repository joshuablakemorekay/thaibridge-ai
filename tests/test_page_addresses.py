"""Phase 0 safety net for the website work: no page address may disappear.

ThaiBridge is about to gain a public "website" layout alongside the learner
"app" layout. Every address below is somebody's bookmark, a Google result, a
link in an ad or a Stripe return page, so moving or deleting one silently is
the most expensive mistake that work could make.

ROUTES_ON_2026_11_18 is the full list of addresses the app answered on that
day. A test fails if any of them stops being registered. Adding NEW routes is
fine; removing or renaming one needs a deliberate redirect and an edit here.

PUBLIC_PAGES must open for a brand-new, logged-out visitor (a locked preview
still counts: it returns 200 and is what search engines see).
"""
import pytest

import app as app_module

ROUTES_ON_2026_11_18 = [
    '/',
    '/about',
    '/account-deleted',
    '/addon/instant-access/stripe',
    '/addon/success',
    '/alphabet',
    '/api/ai/chat',
    '/api/ai/clear',
    # /api/ai/explain, /generate and /hint removed 2026-11-21 on purpose: unused
    # by any page and unguarded spend (see the note in app.py). POST-only, so
    # no bookmark or search result ever pointed at them.
    '/api/ai/status',
    '/api/beginner_convert',
    '/api/cancel-reason',
    '/api/categories',
    '/api/check_answer',
    '/api/complete_alphabet',
    '/api/drill/<kind>',
    '/api/grammar',
    '/api/lessons',
    '/api/listening/<conv_id>',
    '/api/meditation',
    '/api/path/placement',
    '/api/path/reset',
    '/api/path/review',
    '/api/path/start',
    '/api/quiz/<category>',
    '/api/review',
    '/api/review/snooze',
    '/api/sentence-builder',
    '/api/sentence-builder/check',
    '/api/theravada',
    '/api/user_stats',
    '/api/vocabulary/<category>',
    '/bob-buddhism-overview',
    '/bob-fear-article',
    '/bob-writings',
    '/business-thai',
    '/calendar',
    '/change-password',
    '/chanting',
    '/chanting/chant/<chant_id>',
    '/chanting/chant/<chant_id>/body',
    '/chanting/contents',
    '/chanting/page/<int:page>',
    '/chanting/pages',
    '/chat',
    '/contact',
    '/culture',
    '/dana',
    '/dana/thanks',
    '/delete-account',
    '/developer-login',
    '/developer-logout',
    '/dhamma-and-culture',
    '/dhamma-talk/<slug>',
    '/dictionary',
    '/exercise/<category>',
    '/expat2000',
    '/forgot-password',
    '/formality',
    '/gender-examples',
    '/grammar',
    '/instructions',
    '/journal',
    '/journal/<slug>',
    '/learn',
    '/lesson/<int:lesson_id>',
    '/lessons',
    '/login',
    '/logout',
    '/meditation',
    '/monk-mode',
    '/monk/lesson/<topic>',
    '/monk/lessons',
    '/monk/pronunciation',
    '/paiboon',
    '/paypal/success',
    '/policies',
    '/practising-anywhere',
    '/premium',
    '/privacy',
    '/progress',
    '/read_write',
    '/register',
    '/reset-password/<token>',
    '/reviews/private',
    '/search',
    '/sentences',
    '/set-gender/<gender>',
    '/set-monk-accent/<accent>',
    '/set-monk-direction/<direction>',
    '/set-monk-mode/off',
    '/signup',
    '/stripe/webhook',
    '/subscribe/<tier>',
    '/subscribe/<tier>/paypal',
    '/subscribe/<tier>/stripe',
    '/subscribe/cancel',
    '/subscribe/cancel-subscription',
    '/subscribe/success',
    '/subscription-goodbye',
    '/survival',
    '/theravada',
    '/tones-classes',
    '/tour-guide',
    '/unlock/earned/<section_id>',
    '/vowels_syllables',
]

PUBLIC_PAGES = [
    '/',
    '/about',
    '/premium',
    '/policies',
    '/privacy',
    '/contact',
    '/instructions',
    '/expat2000',
    '/journal',
    '/calendar',
    '/culture',
    '/theravada',
    '/practising-anywhere',
    '/dhamma-and-culture',
    '/chanting',
    '/chanting/contents',
    '/meditation',
    '/bob-writings',
    '/alphabet',
    '/paiboon',
    '/survival',
    '/learn',
    '/lessons',
    '/grammar',
    '/sentences',
    '/dictionary',
    '/tour-guide',
    '/business-thai',
    '/chat',
    '/search',
    '/login',
    '/signup',
    '/formality',
    '/gender-examples',
    '/read_write',
    '/tones-classes',
    '/vowels_syllables',
]


def _current_routes():
    return {r.rule for r in app_module.app.url_map.iter_rules() if r.endpoint != "static"}


def test_no_page_address_has_disappeared():
    missing = sorted(set(ROUTES_ON_2026_11_18) - _current_routes())
    assert not missing, f"These addresses no longer exist: {missing}"


@pytest.mark.parametrize("path", PUBLIC_PAGES)
def test_a_logged_out_visitor_can_open(path):
    response = app_module.app.test_client().get(path)
    assert response.status_code == 200, f"{path} returned {response.status_code}"
