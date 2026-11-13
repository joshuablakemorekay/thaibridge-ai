"""
Tests for going live with Stripe (2026-11-05).

Two things a customer must never see on the live site:
1. A "test mode — no real money" notice while real money is being taken.
2. Stripe's raw error text (request ids, customer ids) when checkout fails.

The mode comes from the key prefix, so these tests patch STRIPE_LIVE /
PAYPAL settings rather than real keys. No test reaches Stripe.

Run with:  pytest tests/test_payment_mode.py -v
"""

import os
from unittest.mock import patch

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as A  # noqa: E402
from app import app  # noqa: E402

NOTICE = "test / sandbox"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def premium_page(client, *, stripe_live, paypal_mode="sandbox", paypal_keys=False):
    ids = ("id", "secret") if paypal_keys else ("", "")
    with patch.object(A, "STRIPE_LIVE", stripe_live), \
         patch.object(A, "PAYPAL_MODE", paypal_mode), \
         patch.object(A, "PAYPAL_CLIENT_ID", ids[0]), \
         patch.object(A, "PAYPAL_CLIENT_SECRET", ids[1]):
        return client.get("/premium").get_data(as_text=True)


def test_the_test_notice_shows_with_test_keys(client):
    assert NOTICE in premium_page(client, stripe_live=False)


def test_the_test_notice_is_gone_once_stripe_is_live(client):
    assert NOTICE not in premium_page(client, stripe_live=True)


def test_sandbox_paypal_keeps_the_notice_even_with_live_stripe(client):
    """Live Stripe beside a sandbox PayPal button is still partly pretend."""
    page = premium_page(client, stripe_live=True, paypal_keys=True)
    assert NOTICE in page


def test_live_paypal_and_live_stripe_hide_the_notice(client):
    page = premium_page(client, stripe_live=True, paypal_mode="live", paypal_keys=True)
    assert NOTICE not in page


@pytest.mark.parametrize("key,live", [
    ("sk_live_abc", True), ("rk_live_abc", True),
    ("sk_test_abc", False), ("", False), (None, False),
])
def test_the_key_prefix_decides_the_mode(key, live):
    assert A.stripe_key_is_live(key) is live


def test_a_stripe_failure_shows_a_friendly_message_not_stripe_internals(client):
    boom = Exception("Request req_I05oruwlcDTiGR: No such customer: 'cus_VRJocJAXVTgkqe'")
    with patch("app.stripe.api_key", "sk_test_x"), \
         patch("app.stripe.checkout.Session.create", side_effect=boom):
        resp = client.post("/dana", json={"amount": "3"})
    body = resp.get_data(as_text=True)
    assert resp.status_code == 502
    assert resp.get_json()["message"] == A.CHECKOUT_FAILED_MESSAGE
    assert "req_" not in body and "cus_" not in body
