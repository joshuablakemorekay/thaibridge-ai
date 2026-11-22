"""
Tests for the moves from thaibridge-ai.smoald.com (2026-11-08) and
thaibridge.smoald.com (2026-11-22) to jaiway.smoald.com.

The old address stays live, because ads, TikTok links and the printed chanting
book proof all point at it. Page visits there are sent on to the same page on
the new address. Form posts and Stripe webhooks are NOT redirected, because a
POST can't safely follow a redirect: those are answered where they land.

Run with:  pytest tests/test_domain_redirect.py -v
"""

import os

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app  # noqa: E402

OLD = "thaibridge-ai.smoald.com"
OLD2 = "thaibridge.smoald.com"
NEW = "jaiway.smoald.com"


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_old_address_sends_page_visits_to_new_address():
    r = client().get("/chanting", base_url=f"https://{OLD}")
    assert r.status_code == 301
    assert r.headers["Location"] == f"https://{NEW}/chanting"


def test_tracking_links_keep_their_utm_tags():
    r = client().get("/?utm_source=tiktok&utm_campaign=chant", base_url=f"https://{OLD}")
    assert r.status_code == 301
    assert r.headers["Location"] == f"https://{NEW}/?utm_source=tiktok&utm_campaign=chant"


def test_plain_home_page_has_no_stray_question_mark():
    r = client().get("/", base_url=f"https://{OLD}")
    assert r.headers["Location"] == f"https://{NEW}/"


def test_posts_on_old_address_are_not_redirected():
    # A Stripe webhook still pointing at the old address must reach the app.
    r = client().post("/stripe/webhook", data=b"{}", base_url=f"https://{OLD}")
    assert r.status_code != 301


def test_new_address_is_left_alone():
    r = client().get("/", base_url=f"https://{NEW}")
    assert r.status_code != 301


def test_render_address_is_left_alone():
    r = client().get("/", base_url="https://thaibridge-ai.onrender.com")
    assert r.status_code != 301


def test_second_old_address_also_sends_visits_to_new_address():
    r = client().get("/chanting?x=1", base_url=f"https://{OLD2}")
    assert r.status_code == 301
    assert r.headers["Location"] == f"https://{NEW}/chanting?x=1"


def test_posts_on_second_old_address_are_not_redirected():
    # The Stripe webhook pointed here until it was moved to the new address.
    r = client().post("/stripe/webhook", data=b"{}", base_url=f"https://{OLD2}")
    assert r.status_code != 301
