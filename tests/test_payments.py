"""
Tests for the payment history table (added 2026-09-11).

The User row only ever held a learner's CURRENT standing — tier, status,
period end, full_unlock. A renewal overwrote the date, a cancellation wiped
the tier, and a dāna gift never reached the database at all. So "what has
this person paid?" was unanswerable without logging into Stripe.

Payment is a mirror the app can read, written by the same handlers that grant
the access. Stripe is stubbed throughout: the webhook signature check is
patched to hand back a ready-made event, and no test reaches the network.

Run with:  pytest tests/test_payments.py -v
"""

import os
import uuid
from unittest.mock import patch

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as A  # noqa: E402
from app import app, db, Payment, User  # noqa: E402


@pytest.fixture(autouse=True)
def clean_payments():
    with app.app_context():
        Payment.query.delete()
        db.session.commit()
    yield
    with app.app_context():
        Payment.query.delete()
        db.session.commit()


@pytest.fixture
def user():
    """A real User row, so the FK has something to point at. Removed after."""
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"pay_{tag}", email=f"pay_{tag}@example.com",
                 password_hash="x", stripe_customer_id=f"cus_{tag}")
        db.session.add(u)
        db.session.commit()
        uid, cus = u.id, u.stripe_customer_id
    yield {"id": uid, "customer": cus}
    with app.app_context():
        Payment.query.filter_by(user_id=uid).delete()
        User.query.filter_by(id=uid).delete()
        db.session.commit()


def post_event(client, event):
    """Deliver one Stripe event to the webhook with the signature check stubbed."""
    with patch.object(A, "STRIPE_WEBHOOK_SECRET", "whsec_fake"), \
         patch("app.stripe.Webhook.construct_event", return_value=event), \
         patch("app.stripe.api_key", None):   # no Subscription.retrieve calls
        return client.post("/stripe/webhook", data=b"{}",
                           headers={"Stripe-Signature": "t=1,v1=fake"})


def rows():
    with app.app_context():
        return Payment.query.order_by(Payment.id).all()


def checkout_event(session_id, **obj):
    return {"type": "checkout.session.completed",
            "data": {"object": {"id": session_id, **obj}}}


# ---------------------------------------------------------------------------
# Each way money moves leaves exactly one row
# ---------------------------------------------------------------------------

def test_a_new_subscription_is_recorded_with_its_amount(user):
    ev = checkout_event("cs_sub_1", customer=user["customer"],
                        metadata={"user_id": str(user["id"]), "tier": "pro"},
                        amount_total=999, currency="gbp")
    assert post_event(app.test_client(), ev).status_code == 200
    r = rows()
    assert len(r) == 1
    assert (r[0].kind, r[0].tier, r[0].amount_pence, r[0].currency) == \
        ("subscription", "pro", 999, "gbp")
    assert r[0].user_id == user["id"]
    assert r[0].provider == "stripe"
    assert r[0].provider_ref == "cs_sub_1"


def test_the_instant_access_pass_is_recorded_as_an_addon(user):
    ev = checkout_event("cs_addon_1", customer=user["customer"],
                        metadata={"user_id": str(user["id"]), "addon": "full_unlock"},
                        amount_total=999, currency="gbp")
    post_event(app.test_client(), ev)
    r = rows()
    assert len(r) == 1
    assert r[0].kind == "addon"
    assert r[0].tier is None
    with app.app_context():
        assert db.session.get(User, user["id"]).full_unlock is True


def test_a_renewal_invoice_is_recorded(user):
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.subscription_tier, u.stripe_subscription_id = "basic", "sub_1"
        db.session.commit()
    ev = {"type": "invoice.paid",
          "data": {"object": {"id": "in_2", "subscription": "sub_1",
                              "customer": user["customer"],
                              "billing_reason": "subscription_cycle",
                              "amount_paid": 499, "currency": "gbp"}}}
    post_event(app.test_client(), ev)
    r = rows()
    assert len(r) == 1
    assert (r[0].kind, r[0].tier, r[0].amount_pence) == ("renewal", "basic", 499)


def test_the_first_invoice_is_not_counted_twice(user):
    """Stripe fires checkout.session.completed AND invoice.paid for the first
    payment of a plan. Same money, so only the session row is kept."""
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.subscription_tier, u.stripe_subscription_id = "pro", "sub_1"
        db.session.commit()
    ev = {"type": "invoice.paid",
          "data": {"object": {"id": "in_1", "subscription": "sub_1",
                              "customer": user["customer"],
                              "billing_reason": "subscription_create",
                              "amount_paid": 999, "currency": "gbp"}}}
    post_event(app.test_client(), ev)
    assert rows() == []


def test_a_dana_gift_is_recorded_but_grants_nothing():
    ev = checkout_event("cs_dana_1", metadata={"kind": "dana"},
                        amount_total=500, currency="gbp")
    with patch("app._sync_checkout_session") as sync_tier, \
         patch("app._sync_addon_session") as sync_addon:
        post_event(app.test_client(), ev)
    sync_tier.assert_not_called()
    sync_addon.assert_not_called()
    r = rows()
    assert len(r) == 1
    assert (r[0].kind, r[0].amount_pence, r[0].user_id) == ("dana", 500, None)


def test_a_logged_in_giver_is_linked_by_customer_id(user):
    ev = checkout_event("cs_dana_2", metadata={"kind": "dana"},
                        customer=user["customer"], amount_total=1000, currency="gbp")
    post_event(app.test_client(), ev)
    assert rows()[0].user_id == user["id"]


# ---------------------------------------------------------------------------
# The same money never becomes two rows
# ---------------------------------------------------------------------------

def test_a_redelivered_event_records_nothing_new(user):
    ev = checkout_event("cs_sub_1", customer=user["customer"],
                        metadata={"user_id": str(user["id"]), "tier": "pro"},
                        amount_total=999, currency="gbp")
    c = app.test_client()
    post_event(c, ev)
    post_event(c, ev)
    post_event(c, ev)
    assert len(rows()) == 1


def test_the_redirect_and_the_webhook_share_one_row(user):
    """subscribe_success syncs the same session the webhook does. Whichever
    arrives second must find the row, not make a second one."""
    cs = {"id": "cs_sub_1", "customer": user["customer"],
          "metadata": {"user_id": str(user["id"]), "tier": "pro"},
          "amount_total": 999, "currency": "gbp"}
    with app.app_context(), patch("app.stripe.api_key", None):
        A._sync_checkout_session(cs)
        A._sync_checkout_session(cs)
    assert len(rows()) == 1


def test_the_unique_constraint_holds_at_the_database(user):
    """The belt under the braces: even a direct insert cannot duplicate a ref."""
    from sqlalchemy.exc import IntegrityError
    with app.app_context():
        db.session.add(Payment(provider="stripe", provider_ref="cs_x", kind="dana"))
        db.session.commit()
        db.session.add(Payment(provider="stripe", provider_ref="cs_x", kind="dana"))
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


# ---------------------------------------------------------------------------
# Bookkeeping never breaks the grant
# ---------------------------------------------------------------------------

def test_a_recording_failure_does_not_fail_the_webhook(user):
    """The access is already committed; a bookkeeping error must not 500,
    or Stripe would retry a payment that has already been honoured."""
    ev = checkout_event("cs_sub_1", customer=user["customer"],
                        metadata={"user_id": str(user["id"]), "tier": "pro"},
                        amount_total=999, currency="gbp")
    class BrokenPayment:
        KINDS = Payment.KINDS

        class query:
            @staticmethod
            def filter_by(**_):
                raise RuntimeError("db down")

    with patch.object(A, "Payment", BrokenPayment):
        resp = post_event(app.test_client(), ev)
    assert resp.status_code == 200
    with app.app_context():
        assert db.session.get(User, user["id"]).subscription_tier == "pro"


def test_an_unknown_kind_is_refused_not_written():
    with app.app_context():
        assert A._record_payment(provider_ref="cs_y", kind="refund") is None
    assert rows() == []


# ---------------------------------------------------------------------------
# PayPal
# ---------------------------------------------------------------------------

def test_paypal_amount_is_parsed_from_the_capture_as_pence():
    result = {"purchase_units": [{"payments": {"captures": [
        {"amount": {"value": "9.99", "currency_code": "GBP"}}]}}]}
    assert A._paypal_captured_amount(result) == {"amount_pence": 999, "currency": "gbp"}


def test_paypal_amount_missing_yields_nones_not_a_crash():
    assert A._paypal_captured_amount({}) == {"amount_pence": None, "currency": None}
    assert A._paypal_captured_amount({"purchase_units": []}) == \
        {"amount_pence": None, "currency": None}


def test_paypal_amount_goes_through_decimal_not_float():
    """Money is parsed as Decimal — a non-numeric string is caught as
    InvalidOperation rather than crashing the success page."""
    bad = {"purchase_units": [{"payments": {"captures": [
        {"amount": {"value": "nine ninety-nine", "currency_code": "GBP"}}]}}]}
    assert A._paypal_captured_amount(bad) == {"amount_pence": None, "currency": None}
    # 0.29 * 100 is 28.999999999999996 in float; Decimal has no such drift.
    exact = {"purchase_units": [{"payments": {"captures": [
        {"amount": {"value": "0.29", "currency_code": "GBP"}}]}}]}
    assert A._paypal_captured_amount(exact)["amount_pence"] == 29


# ---------------------------------------------------------------------------
# The receipts view on /progress
# ---------------------------------------------------------------------------

PASSWORD = "ReceiptPass123"


def signed_in(user_id):
    """A client logged in as the given user row, via the real /login route."""
    with app.app_context():
        u = db.session.get(User, user_id)
        u.set_password(PASSWORD)
        db.session.commit()
        identifier = u.username
    c = app.test_client()
    r = c.post("/login", json={"identifier": identifier, "password": PASSWORD})
    assert r.status_code == 200, r.get_data(as_text=True)
    return c


def add_payment(**fields):
    with app.app_context():
        db.session.add(Payment(provider="stripe", **fields))
        db.session.commit()


def test_a_learner_sees_their_own_receipts(user):
    add_payment(provider_ref="cs_r1", kind="subscription", tier="pro",
                amount_pence=999, currency="gbp", user_id=user["id"])
    add_payment(provider_ref="cs_r2", kind="addon",
                amount_pence=1499, currency="gbp", user_id=user["id"])
    body = signed_in(user["id"]).get("/progress").get_data(as_text=True)
    assert "Receipts" in body
    assert "Thai Master (Pro) — new subscription" in body
    assert "Instant Access Pass" in body
    assert "£9.99" in body and "£14.99" in body
    assert "cs_r1" in body and "cs_r2" in body


def test_someone_elses_payments_never_appear(user):
    add_payment(provider_ref="cs_other", kind="dana", amount_pence=500,
                currency="gbp", user_id=None)
    body = signed_in(user["id"]).get("/progress").get_data(as_text=True)
    assert "cs_other" not in body


def test_no_payments_means_no_receipts_section(user):
    body = signed_in(user["id"]).get("/progress").get_data(as_text=True)
    assert "Receipts" not in body


def test_a_visitor_without_an_account_gets_no_receipts_section():
    body = app.test_client().get("/progress").get_data(as_text=True)
    assert "Receipts" not in body


def test_a_missing_amount_shows_a_dash_not_a_crash(user):
    add_payment(provider_ref="paypal_x", kind="subscription", tier="basic",
                amount_pence=None, currency=None, user_id=user["id"])
    resp = signed_in(user["id"]).get("/progress")
    assert resp.status_code == 200
    assert "Thai Reader (Basic) — new subscription" in resp.get_data(as_text=True)


def test_the_currency_symbol_follows_the_currency():
    with app.app_context():
        assert Payment(amount_pence=999, currency="gbp").amount_display == "£9.99"
        assert Payment(amount_pence=1250, currency="usd").amount_display == "$12.50"
        assert Payment(amount_pence=700, currency="thb").amount_display == "THB 7.00"
        assert Payment(amount_pence=None).amount_display is None


def test_receipts_in_the_same_second_keep_a_stable_order(user):
    """Two rows can share a timestamp (webhook and redirect land together).
    The later insert must always render first, not whichever the DB felt like."""
    from datetime import datetime
    same = datetime(2026, 9, 11, 12, 0, 0)
    add_payment(provider_ref="cs_first", kind="subscription", tier="pro",
                amount_pence=999, currency="gbp", user_id=user["id"], created_at=same)
    add_payment(provider_ref="in_second", kind="renewal", tier="pro",
                amount_pence=999, currency="gbp", user_id=user["id"], created_at=same)
    body = signed_in(user["id"]).get("/progress").get_data(as_text=True)
    assert body.index("in_second") < body.index("cs_first")
