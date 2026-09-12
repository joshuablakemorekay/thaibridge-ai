"""
Tests for VAT-inclusive price display (added 2026-09-11).

Stripe adds tax on TOP of the figures in SUBSCRIPTION_TIERS, so the plans page was
advertising £9.99 while checkout took £11.99. For consumer sales in the UK
the advertised price has to be the total payable, so every product price now
renders through the `inc_vat` filter.

Two things these guard:

  1. The displayed figure matches the penny Stripe actually charges. If the
     two ever drift, the page is lying about the price again.
  2. Dāna is NOT touched. A gift carries a Cash Donation tax code, buys
     nothing, and is not a product - applying VAT to it would be wrong.

Run with:  pytest tests/test_vat_display.py -v
"""

import os
from decimal import Decimal, ROUND_HALF_UP

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import (  # noqa: E402
    INSTANT_ACCESS_ADDON,
    SUBSCRIPTION_TIERS,
    UK_VAT_RATE,
    price_inc_vat,
)


def stripe_would_charge(amount):
    """Reimplement Stripe's arithmetic independently.

    Stripe works in whole pence: it takes the tax-exclusive unit_amount,
    applies the rate, rounds the tax to a penny, then adds it. Written out
    the long way on purpose - if this simply called price_inc_vat it would
    agree with itself and prove nothing.
    """
    pence = int(round(float(amount) * 100))
    tax = (Decimal(pence) * UK_VAT_RATE).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return Decimal(pence + int(tax)) / 100


# Every real price on the site, monthly and annual, plus the add-on.
REAL_PRICES = [
    SUBSCRIPTION_TIERS["basic"]["price"],
    SUBSCRIPTION_TIERS["basic"]["price_year"],
    SUBSCRIPTION_TIERS["pro"]["price"],
    SUBSCRIPTION_TIERS["pro"]["price_year"],
    INSTANT_ACCESS_ADDON["price"],
]


@pytest.mark.parametrize("amount", REAL_PRICES)
def test_display_matches_what_stripe_charges(amount):
    """The number on the page is the number on the card statement."""
    assert price_inc_vat(amount) == stripe_would_charge(amount)


def test_known_values():
    """The headline prices, spelled out, so a rate change fails loudly."""
    assert price_inc_vat(9.99) == Decimal("11.99")
    assert price_inc_vat(19.99) == Decimal("23.99")
    assert price_inc_vat(14.99) == Decimal("17.99")
    assert price_inc_vat(99.00) == Decimal("118.80")
    assert price_inc_vat(199.00) == Decimal("238.80")


def test_free_tier_is_untouched():
    """Nothing times 1.2 is still nothing - FREE must not become £0.00."""
    assert SUBSCRIPTION_TIERS["free"]["price"] == 0
    assert price_inc_vat(0) == Decimal("0.00")


def test_returns_exact_decimal_not_float():
    """Money never rides on a float; the filter hands back Decimal pence."""
    result = price_inc_vat(9.99)
    assert isinstance(result, Decimal)
    assert result.as_tuple().exponent == -2


def test_plans_page_shows_the_inclusive_price(make_client):
    """The learner sees £11.99, not the £9.99 we hand Stripe."""
    client = make_client()
    html = client.get("/premium").get_data(as_text=True)

    assert "11.99" in html, "plans page should advertise the VAT-inclusive price"
    assert "23.99" in html, "Pro should advertise the VAT-inclusive price"
    assert "VAT included" in html, "the page must say the price includes tax"

    # The ex-tax figures are for Stripe, and must not be shown as a price.
    assert "£9.99" not in html
    assert "£19.99" not in html


def test_dana_amounts_are_not_vat_adjusted(make_client):
    """A gift is not a product. The buttons stay the round numbers offered."""
    client = make_client()
    html = client.get("/premium").get_data(as_text=True)

    # The dāna buttons post the plain pound amount; VAT must never touch them.
    assert 'name="amount" value="5"' in html or "dana-btn" in html
    for inflated in ("£6.00", "£12.00", "£24.00"):
        assert inflated not in html, f"dāna appears VAT-inflated: {inflated}"


def test_no_template_renders_a_raw_product_price():
    """No page may print a price variable without the inc_vat filter.

    This exists because of how the VAT fix went wrong the first time: prices
    were corrected template by template, and subscribe_choose.html was missed.
    The plans page then advertised £11.99 while the very next step in the same
    checkout said £9.99 — worse than the original bug, because it looks like a
    trick rather than a mistake.

    Scanning the templates catches the whole class of it: add a new page that
    shows a price, forget the filter, and this fails.
    """
    import re
    from pathlib import Path

    templates = Path(__file__).resolve().parent.parent / "templates"

    # Variables that carry a tax-exclusive product price.
    price_vars = [
        "tier.price", "tier_info.price", "tier_info.price_year",
        "addon.price", "group.price",
        "monthly_amount", "yearly_amount",
    ]

    offenders = []
    for path in sorted(templates.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        # Every {{ ... }} that mentions a price variable must pipe to inc_vat.
        for expr in re.findall(r"\{\{(.*?)\}\}", text, re.S):
            if not any(v in expr for v in price_vars):
                continue
            if "inc_vat" in expr:
                continue
            offenders.append(f"{path.name}: {{{{{expr.strip()}}}}}")

    assert not offenders, (
        "these render a tax-exclusive price straight to the page:\n  "
        + "\n  ".join(offenders)
    )
