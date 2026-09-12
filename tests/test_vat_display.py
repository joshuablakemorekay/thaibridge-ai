"""
Tests that the advertised price is the price charged (rewritten 2026-09-12).

The history is worth keeping, because it went wrong twice, in opposite
directions.

First, prices were tax-EXCLUSIVE: £9.99 went to Stripe, Stripe added 20% on
top, and the learner was charged £11.99 having been shown £9.99. For UK
consumer sales the advertised price has to be the total payable, so that was
wrong.

The first fix displayed the inclusive figure instead — £11.99 on the page.
Honest, but it made every price ugly, and £99 a year became £118.80, losing a
round number that had been chosen on purpose.

So prices are now tax-INCLUSIVE at source: `tax_behavior: 'inclusive'` on each
price_data, meaning £9.99 is what the card is charged and Stripe works the VAT
out inside it. Pages show the stored figure directly, because that figure is
now the truth.

What these guard:

  1. Both products actually declare inclusive pricing to Stripe. Without it,
     Stripe reverts to adding tax on top and the original bug is back with
     nothing on screen to show for it.
  2. Pages show the stored price unchanged — no arithmetic between the data
     and the customer.
  3. Dāna stays out of it: a gift carries a Cash Donation code, buys nothing,
     and is not a sale.

Run with:  pytest tests/test_vat_display.py -v
"""

import os
import re
from pathlib import Path

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import (  # noqa: E402
    INSTANT_ACCESS_ADDON,
    SUBSCRIPTION_TIERS,
    TAX_CODE_DONATION,
)

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
SOURCE = (ROOT / "app.py").read_text(encoding="utf-8")


# ── What we tell Stripe ──────────────────────────────────────────────────

def test_both_products_declare_inclusive_pricing():
    """Without this flag Stripe adds VAT on top and the page understates.

    Counts code lines only — the comment block above the prices quotes the
    same literal, and counting that too would let the flag be deleted from
    the code while the test still passed.
    """
    code_lines = [
        ln for ln in SOURCE.splitlines()
        if "'tax_behavior': 'inclusive'" in ln and not ln.lstrip().startswith("#")
    ]
    assert len(code_lines) == 2, (
        "expected inclusive pricing on both the subscription and the "
        f"Instant Access Pass, found {len(code_lines)}: {code_lines}"
    )


def test_dana_is_given_no_tax_behaviour():
    """A gift is not a sale, so tax behaviour does not apply to it."""
    start = SOURCE.index("TAX_CODE_DONATION,")
    dana_block = SOURCE[start:start + 1200]
    assert "tax_behavior" not in dana_block
    assert TAX_CODE_DONATION == "txcd_90000001"


# ── What the pages show ──────────────────────────────────────────────────

def test_pages_show_the_stored_price_unchanged(make_client):
    """The learner sees exactly the figure in SUBSCRIPTION_TIERS."""
    html = make_client().get("/premium").get_data(as_text=True)

    assert "£9.99" in html, "Basic should advertise its stored price"
    assert "£19.99" in html, "Pro should advertise its stored price"
    assert "VAT included" in html, "the page should say the price includes tax"

    # Figures from the abandoned exclusive-pricing approach must not reappear.
    assert "£11.99" not in html
    assert "£23.99" not in html


def _signed_up_client():
    """A real logged-in user — /subscribe sits behind @login_required."""
    import uuid

    from app import app as flask_app

    client = flask_app.test_client()
    username = f"vat{uuid.uuid4().hex[:10]}"
    result = client.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": "TestPass123!", "confirm_password": "TestPass123!",
    }).get_json()
    assert result["success"], result
    return client


def test_checkout_page_agrees_with_the_plans_page(make_client):
    """The two steps of one flow must not quote different prices.

    This is the bug that actually shipped: /premium said £11.99 while the very
    next page said £9.99, because the earlier fix went template by template.
    """
    plans = make_client().get("/premium").get_data(as_text=True)
    choose = _signed_up_client().get("/subscribe/basic").get_data(as_text=True)

    assert "£9.99" in plans
    for price in ("£9.99", "£99.00"):
        assert price in choose, f"{price} missing from the billing-period page"


def test_no_template_does_arithmetic_on_a_price():
    """Prices reach the page as stored — no filter, no multiplication.

    Any transformation between the data and the customer is a chance for the
    page and the card statement to disagree, which is what happened twice.
    """
    price_vars = [
        "tier.price", "tier_info.price", "tier_info.price_year",
        "addon.price", "group.price", "monthly_amount", "yearly_amount",
    ]
    banned = ["inc_vat", "* 1.2", "*1.2"]

    offenders = []
    for path in sorted(TEMPLATES.rglob("*.html")):
        for expr in re.findall(r"\{\{(.*?)\}\}", path.read_text(encoding="utf-8"), re.S):
            if any(v in expr for v in price_vars) and any(b in expr for b in banned):
                offenders.append(f"{path.name}: {{{{{expr.strip()}}}}}")

    assert not offenders, (
        "these transform a price before showing it:\n  " + "\n  ".join(offenders)
    )


def test_the_round_numbers_survived():
    """The annual prices are offers, not arithmetic — £99, not £118.80."""
    assert SUBSCRIPTION_TIERS["basic"]["price"] == 9.99
    assert SUBSCRIPTION_TIERS["pro"]["price"] == 19.99
    assert SUBSCRIPTION_TIERS["basic"]["price_year"] == 99.00
    assert SUBSCRIPTION_TIERS["pro"]["price_year"] == 199.00
    assert INSTANT_ACCESS_ADDON["price"] == 14.99
