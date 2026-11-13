"""Every POST must be JSON (json_only.py, added 2026-11-13).

A form on another website can make a learner's browser POST here, but it can't
send JSON without ThaiBridge's permission. So refusing anything that isn't JSON
shuts out forged requests from other sites, on top of the SameSite cookie.

Run with:  pytest tests/test_json_only.py -v
"""
import re

import pytest

import json_only
from app import app


def post_routes():
    """Every route in the app that accepts POST, with a sample URL for it."""
    found = []
    for rule in app.url_map.iter_rules():
        if "POST" not in rule.methods or rule.endpoint == "static":
            continue
        url = re.sub(r"<(?:[^:>]+:)?[^>]+>", "sample", rule.rule)
        found.append((rule.endpoint, url))
    return sorted(found)


ROUTES = post_routes()
CHECKED = [(endpoint, url) for endpoint, url in ROUTES
           if endpoint not in json_only.EXEMPT_ENDPOINTS]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_the_route_list_is_real():
    # If the walk found nothing, every check below would pass by vanishing.
    assert len(CHECKED) > 20
    assert ("monk_mode", "/monk-mode") in ROUTES


@pytest.mark.parametrize("endpoint,url", CHECKED, ids=[e for e, _ in CHECKED])
def test_every_post_route_refuses_a_plain_form(client, endpoint, url):
    response = client.post(url, data={"anything": "1"})
    assert response.status_code == 415, f"{endpoint} accepted a form post"
    assert response.get_json()["success"] is False


@pytest.mark.parametrize("content_type", ["text/plain", "multipart/form-data",
                                          "application/x-www-form-urlencoded"])
def test_the_formats_another_site_can_send_are_all_refused(client, content_type):
    # These three are exactly what an HTML form or a "simple" cross-site
    # request can send without asking first. JSON written as text/plain is
    # still refused: the label is what the browser's check looks at.
    response = client.post("/monk-mode", data='{"code": "x"}',
                           headers={"Content-Type": content_type})
    assert response.status_code == 415


def test_json_is_let_through(client):
    response = client.post("/monk-mode", json={"code": "not-a-real-code"})
    assert response.status_code == 200
    assert response.get_json()["success"] is False


def test_pages_are_unaffected(client):
    assert client.get("/monk-mode").status_code == 200


def test_the_stripe_webhook_is_the_only_exception(client):
    # Stripe posts its own format and is checked by signature instead.
    assert json_only.EXEMPT_ENDPOINTS == {"stripe_webhook"}
    response = client.post("/stripe/webhook", data=b"{}",
                           headers={"Stripe-Signature": "t=1,v1=bad"})
    assert response.status_code != 415
