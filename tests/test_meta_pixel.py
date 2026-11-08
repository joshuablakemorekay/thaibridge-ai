"""The Meta Pixel: offered behind a cookie banner, never loaded without consent.

The page can't run JavaScript in these tests, so they check what the server
controls: the banner and Pixel ID are on the page, Meta's script is NOT linked
directly (it is only fetched by the consent code after "Accept"), and a sign-up
queues exactly one CompleteRegistration event that is handed to the next page
and then forgotten.

Run with:  pytest tests/test_meta_pixel.py -v
"""
import re
import uuid

import meta_pixel
from app import app

PASSWORD = "TestPass123"


def client():
    app.config["TESTING"] = True
    return app.test_client()


def events_on(html):
    match = re.search(r"var EVENTS = (\[.*?\]);", html)
    assert match, "the Pixel script is missing from the page"
    return match.group(1)


def test_banner_and_pixel_id_are_on_every_page():
    html = client().get("/about").get_data(as_text=True)
    assert 'id="tb-consent"' in html
    assert meta_pixel.PIXEL_ID in html
    assert "Cookie choices" in html


def test_meta_script_is_not_loaded_before_consent():
    """No <script src=...fbevents.js>: the loader only runs inside loadPixel()."""
    html = client().get("/about").get_data(as_text=True)
    assert '<script src="https://connect.facebook.net' not in html
    assert "if (choice === 'granted') loadPixel();" in html


def test_sign_up_fires_complete_registration_once():
    c = client()
    username = f"px_{uuid.uuid4().hex[:10]}"
    result = c.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    }).get_json()
    assert result["success"], result

    first = events_on(c.get("/about").get_data(as_text=True))
    assert "CompleteRegistration" in first
    assert username not in first          # no personal details go to Meta

    second = events_on(c.get("/about").get_data(as_text=True))
    assert second == "[]"


def test_purchase_is_sent_in_pounds():
    with app.test_request_context():
        from flask import session
        meta_pixel.queue_purchase(799, "gbp", event_id="cs_test_1")
        event = session[meta_pixel.QUEUE_KEY][0]
    assert event == {"name": "Purchase", "event_id": "cs_test_1",
                     "params": {"value": 7.99, "currency": "GBP"}}


def test_purchase_with_no_amount_is_skipped():
    with app.test_request_context():
        from flask import session
        meta_pixel.queue_purchase(None, "gbp")
        assert meta_pixel.QUEUE_KEY not in session
