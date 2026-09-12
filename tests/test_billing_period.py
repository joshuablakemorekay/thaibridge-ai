"""Monthly vs yearly billing.

A tier is one product sold on two clocks. These tests pin down the three things
that can go wrong when a second clock is added: charging the wrong amount,
charging the wrong interval, and opting somebody into a year by accident.
"""
import uuid

import pytest

from app import (
    app,
    SUBSCRIPTION_TIERS,
    _billing_period,
    _tier_amount,
    _period_words,
)

PASSWORD = "TestPass123"


def unique_username(prefix="bill"):
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def signed_up_client():
    """A real logged-in user — /subscribe is behind @login_required."""
    client = app.test_client()
    username = unique_username()
    result = client.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    }).get_json()
    assert result["success"], result
    return client


# ── The prices themselves ────────────────────────────────────────────────

@pytest.mark.parametrize("tier", ["basic", "pro"])
def test_paid_tiers_have_an_annual_price(tier):
    assert SUBSCRIPTION_TIERS[tier].get("price_year")


def test_free_tier_has_no_annual_price():
    """Nothing should ever offer a year of free at a price."""
    assert not SUBSCRIPTION_TIERS["free"].get("price_year")


@pytest.mark.parametrize("tier", ["basic", "pro"])
def test_annual_saves_roughly_two_months(tier):
    """The offer is 'two months free'. This fails loudly on a typo'd price.

    A missing zero (£19.90 instead of £199.00) or an extra one both land far
    outside this band, which is the whole point of testing a number that a
    human typed.
    """
    info = SUBSCRIPTION_TIERS[tier]
    monthly_total = info["price"] * 12
    saving_in_months = (monthly_total - info["price_year"]) / info["price"]
    assert 1.8 <= saving_in_months <= 2.3, (
        f"{tier}: a year costs {info['price_year']}, which saves "
        f"{saving_in_months:.1f} months, not about 2"
    )


@pytest.mark.parametrize("tier", ["basic", "pro"])
def test_a_year_never_costs_more_than_twelve_months(tier):
    info = SUBSCRIPTION_TIERS[tier]
    assert info["price_year"] < info["price"] * 12


# ── Reading the period off the request ───────────────────────────────────

@pytest.mark.parametrize("query, expected", [
    ("?period=year", "year"),
    ("?period=month", "month"),
    ("", "month"),
    ("?period=YEAR", "month"),      # case-sensitive on purpose
    ("?period=yearly", "month"),
    ("?period=annual", "month"),
    ("?period=12", "month"),
    ("?period=", "month"),
])
def test_only_exactly_year_opts_into_annual(query, expected):
    """Anything unrecognised stays monthly — the smaller commitment.

    A stale bookmark or a hand-edited URL must not be able to talk somebody
    into twelve months.
    """
    with app.test_request_context("/subscribe/basic" + query):
        assert _billing_period() == expected


# ── What each period costs ───────────────────────────────────────────────

def test_tier_amount_picks_the_right_price():
    basic = SUBSCRIPTION_TIERS["basic"]
    assert _tier_amount(basic, "month") == basic["price"]
    assert _tier_amount(basic, "year") == basic["price_year"]


def test_tier_amount_falls_back_to_twelve_months():
    """A tier added without an annual price bills 12x, never £0."""
    invented = {"name": "Test", "price": 5.00}
    assert _tier_amount(invented, "year") == 60.00


def test_period_words():
    assert _period_words("year") == ("year", "annual")
    assert _period_words("month") == ("month", "monthly")


# ── The checkout page ────────────────────────────────────────────────────

def test_choose_page_shows_both_prices():
    """Both periods, priced the way the customer will actually be charged.

    These were £9.99 and £99.00 — the figures handed to Stripe, before it adds
    tax. Showing them here meant the plans page said £11.99 and the very next
    step of the same checkout said £9.99. The page must agree with the card
    statement, so the assertions moved to the VAT-inclusive totals.
    """
    client = signed_up_client()
    body = client.get("/subscribe/basic").get_data(as_text=True)
    assert "£11.99" in body      # £9.99 + 20% UK VAT
    assert "£118.80" in body     # £99.00 + 20% UK VAT
    assert "2 months free" in body
    # The ex-tax figures are for Stripe, and must not be shown as a price.
    assert "£9.99" not in body
    assert "£99.00" not in body


def test_choose_page_carries_the_period_into_the_pay_links(monkeypatch):
    """Every payment link on the page must keep the chosen period.

    A provider only renders a link when its keys are configured, so Stripe is
    forced on here rather than relying on the environment. The first version of
    this test read whatever links happened to render, which passed locally off
    a populated .env and failed in CI, where there are no keys and therefore no
    links at all — an empty list is not a passing case.
    """
    import re

    import app as app_module
    monkeypatch.setattr(app_module.stripe, "api_key", "sk_test_fake")

    client = signed_up_client()
    body = client.get("/subscribe/basic?period=year").get_data(as_text=True)
    pattern = r"/subscribe/basic/(?:stripe|paypal)[^\"'\s]*"
    pay_links = re.findall(pattern, body)
    assert pay_links, "no payment links rendered at all"
    for link in pay_links:
        assert link.endswith("?period=year"), link


# ── What Stripe is actually asked to charge ──────────────────────────────

@pytest.mark.parametrize("query, want_interval, want_pence", [
    ("?period=year", "year", 9900),
    ("?period=month", "month", 999),
    ("", "month", 999),
])
def test_stripe_checkout_bills_the_chosen_period(monkeypatch, query,
                                                 want_interval, want_pence):
    """The one that matters: right interval, right amount, in pence."""
    import app as app_module

    captured = {}

    class FakeSession:
        @staticmethod
        def create(**kwargs):
            captured.update(kwargs)
            return type("CS", (), {"url": "https://stripe.test/checkout"})()

    monkeypatch.setattr(app_module.stripe, "api_key", "sk_test_fake")
    monkeypatch.setattr(app_module.stripe.checkout, "Session", FakeSession)

    client = signed_up_client()
    response = client.get("/subscribe/basic/stripe" + query)
    assert response.status_code == 303

    price_data = captured["line_items"][0]["price_data"]
    assert price_data["recurring"]["interval"] == want_interval
    assert price_data["unit_amount"] == want_pence
    assert captured["metadata"]["period"] == want_interval
