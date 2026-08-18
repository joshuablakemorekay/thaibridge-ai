"""
Tests for the dāna (voluntary gift) route (added 2026-08-18).

Two of these cover bugs that were real, not hypothetical — both were found by
exercising the route rather than reading it:

  * Stripe rejects `custom_unit_amount` inside inline `price_data` (it only
    exists on a saved Price). The first version of the "other amount" path used
    it and would have 500'd on every custom gift.
  * `Decimal("inf")` is valid input to Decimal and then raises OverflowError on
    int(), which is NOT caught by the obvious `except (InvalidOperation,
    ValueError)`. A crafted form turned into a 500.

The rest guard the principle rather than the plumbing: a gift must grant
NOTHING. The moment a donation confers a tier, XP or an unlock it stops being
dāna and becomes a price, which is the exact line the free Dhamma content
exists to hold.

Stripe is mocked throughout — these tests must never make a network call or
create real Checkout Sessions.

Run with:  pytest tests/test_dana.py -v
"""

import os
import pytest
from unittest.mock import patch
from werkzeug.datastructures import MultiDict

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, db, DANA  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
    with app.test_client() as c:
        yield c


class FakeSession:
    """Stands in for a Stripe Checkout Session."""
    url = "https://checkout.stripe.com/c/pay/cs_test_fake"


@pytest.fixture
def stripe_create():
    """Patch Session.create and hand back the mock so tests can read the kwargs
    the route sent. Also forces a key to be set, so the route doesn't take the
    'payments not configured' branch just because the dev machine has no key."""
    with patch("app.stripe.checkout.Session.create", return_value=FakeSession()) as m:
        with patch("app.stripe.api_key", "sk_test_fake"):
            yield m


def amount_sent(mock):
    """Pence on the single line item of the last create() call."""
    kwargs = mock.call_args.kwargs
    return kwargs["line_items"][0]["price_data"]["unit_amount"]


# ---------------------------------------------------------------------------
# Amounts that should be accepted
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("typed,expected_pence", [
    ("3", 300),
    ("25", 2500),
    ("7.35", 735),        # Decimal, not float — 7.35*100 in binary float is 734.99...
    ("£12", 1200),   # a pasted "£12" should not be a validation failure
    ("1", 100),           # the floor itself is allowed
    ("500", 50000),       # so is the ceiling
])
def test_valid_amounts_reach_stripe_in_exact_pence(client, stripe_create, typed, expected_pence):
    resp = client.post("/dana", data=MultiDict([("amount", typed)]))
    assert resp.status_code == 303
    assert amount_sent(stripe_create) == expected_pence


def test_preset_click_wins_over_the_empty_typed_field(client, stripe_create):
    """The preset buttons and the typed input share the name `amount`, so a
    preset click submits BOTH its value and an empty string. Picking by
    position would be at the mercy of DOM order; the route takes the first
    non-empty value instead."""
    resp = client.post("/dana", data=MultiDict([("amount", "3"), ("amount", "")]))
    assert resp.status_code == 303
    assert amount_sent(stripe_create) == 300


def test_the_gift_is_a_one_off_payment_tagged_as_dana(client, stripe_create):
    """`kind: dana` is what stops the webhook treating a gift as a purchase."""
    client.post("/dana", data=MultiDict([("amount", "10")]))
    kwargs = stripe_create.call_args.kwargs
    assert kwargs["mode"] == "payment"          # never a subscription
    assert kwargs["metadata"] == {"kind": "dana"}


def test_giving_does_not_require_an_account(client, stripe_create):
    """Requiring a login would make dāna an upsell. A logged-out visitor must
    get all the way to Stripe."""
    resp = client.post("/dana", data=MultiDict([("amount", "5")]))
    assert resp.status_code == 303
    # Nothing was prefilled, because we know nothing about them.
    kwargs = stripe_create.call_args.kwargs
    assert "customer" not in kwargs and "customer_email" not in kwargs


# ---------------------------------------------------------------------------
# Amounts that should be turned away — without a 500
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", [
    "0.99",        # under the floor
    "500.01",      # over the ceiling
    "0", "-5",     # nothing, and negative
    "abc", "", "  ", "£", "1,000",
    "1e9",         # parses, but far over the ceiling
    "1e-9",        # parses, but rounds to 0p
    "nan",         # valid Decimal, ValueError on int()
    "inf", "-inf", "Infinity",   # valid Decimal, OverflowError on int()
    "3; DROP TABLE users",
])
def test_bad_amounts_are_turned_away_not_crashed(client, stripe_create, bad):
    resp = client.post("/dana", data=MultiDict([("amount", bad)]))
    assert resp.status_code == 302, f"{bad!r} should redirect, got {resp.status_code}"
    assert resp.headers["Location"].endswith("/premium#dana")
    stripe_create.assert_not_called()          # and no charge was ever started


def test_no_stripe_key_says_so_instead_of_erroring(client):
    with patch("app.stripe.api_key", None):
        resp = client.post("/dana", data=MultiDict([("amount", "10")]))
    assert resp.status_code == 503


# ---------------------------------------------------------------------------
# The principle: a gift buys nothing
# ---------------------------------------------------------------------------

def test_the_thank_you_page_grants_nothing(client):
    """Every other success route re-fetches the session from Stripe because
    something has to be granted. Nothing is granted here, so the page is safe
    to serve to anyone — including someone who just typed the URL."""
    resp = client.get("/dana/thanks")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Thank you" in body
    # No entitlement language anywhere on the page.
    for forbidden in ("unlocked", "upgraded", "your tier", "XP"):
        assert forbidden.lower() not in body.lower(), f"thank-you page promises {forbidden!r}"


def test_a_dana_webhook_event_grants_nothing(client):
    """A dāna session must branch away from BOTH sync paths. If it ever fell
    through to _sync_checkout_session, a gift would be trying to set a tier."""
    import app as A
    event = {
        "type": "checkout.session.completed",
        "data": {"object": {"id": "cs_test_dana", "metadata": {"kind": "dana"}}},
    }
    with patch.object(A, "STRIPE_WEBHOOK_SECRET", "whsec_fake"), \
         patch("app.stripe.Webhook.construct_event", return_value=event), \
         patch("app._sync_checkout_session") as sync_tier, \
         patch("app._sync_addon_session") as sync_addon:
        resp = client.post("/stripe/webhook", data=b"{}",
                           headers={"Stripe-Signature": "t=1,v1=fake"})
    assert resp.status_code == 200
    sync_tier.assert_not_called()
    sync_addon.assert_not_called()


def test_the_gift_declares_the_donation_tax_code(client, stripe_create):
    """Regression test for a real outage (2026-08-18).

    New Stripe accounts enable Managed Payments by default, which REFUSES any
    checkout session whose product has no tax_code. The live site returned 502
    on every gift until this was added, and the mocked tests above all passed
    throughout — they check the amount, and never looked at what was being sold.

    The donation code matters specifically: a gift is not the course. Sending
    the course code would have Stripe treat dāna as a taxable training sale,
    which is both wrong for VAT and wrong about what is happening.
    """
    from app import TAX_CODE_DONATION, TAX_CODE_COURSE
    client.post("/dana", data=MultiDict([("amount", "10")]))
    product = stripe_create.call_args.kwargs["line_items"][0]["price_data"]["product_data"]
    assert product["tax_code"] == TAX_CODE_DONATION
    assert product["tax_code"] != TAX_CODE_COURSE


def test_the_gift_opts_out_of_managed_payments(client, stripe_create):
    """Second half of the same 2026-08-18 outage.

    Managed Payments covers SALES OF DIGITAL PRODUCTS, and its eligible tax
    codes are all software, media and courses — Cash Donation is not among
    them, so Stripe rejected the session outright. Adding the tax code alone
    fixed the subscriptions but left dana failing with a different 502.

    The subscriptions and the Instant Access Pass deliberately stay IN Managed
    Payments: those really are course sales.
    """
    client.post("/dana", data=MultiDict([("amount", "10")]))
    assert stripe_create.call_args.kwargs["managed_payments"] == {"enabled": False}


def test_the_tax_codes_are_distinct_and_well_formed(client):
    """Two different things are being sold, so they carry two different codes.
    Collapsing them to one would silently reclassify gifts as course sales."""
    from app import TAX_CODE_DONATION, TAX_CODE_COURSE
    assert TAX_CODE_DONATION != TAX_CODE_COURSE
    for code in (TAX_CODE_DONATION, TAX_CODE_COURSE):
        assert code.startswith("txcd_"), f"{code!r} is not a Stripe tax code"


def test_presets_sit_inside_the_allowed_range(client):
    """A preset outside the floor/ceiling would render a button that always
    bounces — the two settings have to agree."""
    for amount in DANA["presets"]:
        assert DANA["min_amount"] <= amount <= DANA["max_amount"]
