"""
Tests for lifetime-value (LTV) tracking, added 2026-11-18.

Four gaps stopped the app measuring LTV properly:
  1. no "last active" day, so drifting learners were invisible
  2. no cancellation date or reason
  3. no record of when a learner reached Level 3
  4. payments didn't say monthly or annual

Plus scripts/ltv_report.py, which reads all of it. Stripe is stubbed
throughout, and no test reaches the network.

Run with:  pytest tests/test_ltv_tracking.py -v
"""

import importlib.util
import os
import uuid
from datetime import date, datetime, timedelta
from unittest.mock import patch

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as A  # noqa: E402
from app import app, db, Payment, User  # noqa: E402
from models import utcnow  # noqa: E402  (naive UTC, as the columns store it)

PASSWORD = "LtvPass12345"


@pytest.fixture
def user():
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"ltv_{tag}", email=f"ltv_{tag}@example.com",
                 password_hash="x", stripe_customer_id=f"cus_{tag}")
        u.set_password(PASSWORD)
        db.session.add(u)
        db.session.commit()
        uid, cus, name = u.id, u.stripe_customer_id, u.username
    yield {"id": uid, "customer": cus, "username": name}
    with app.app_context():
        Payment.query.filter_by(user_id=uid).delete()
        User.query.filter_by(id=uid).delete()
        db.session.commit()


def signed_in(info):
    c = app.test_client()
    r = c.post("/login", json={"identifier": info["username"], "password": PASSWORD})
    assert r.status_code == 200, r.get_data(as_text=True)
    return c


def get_user(uid):
    with app.app_context():
        u = db.session.get(User, uid)
        db.session.expunge(u)
        return u


def post_event(event):
    with patch.object(A, "STRIPE_WEBHOOK_SECRET", "whsec_fake"), \
         patch("app.stripe.Webhook.construct_event", return_value=event), \
         patch("app.stripe.api_key", None):
        return app.test_client().post("/stripe/webhook", data=b"{}",
                                      headers={"Stripe-Signature": "t=1,v1=fake"})


def unix(dt):
    return int((dt - datetime(1970, 1, 1)).total_seconds())


# ---------------------------------------------------------------------------
# 1. Last active day
# ---------------------------------------------------------------------------

def test_using_the_site_stamps_today(user):
    assert get_user(user["id"]).last_active_on is None
    signed_in(user).get("/")
    assert get_user(user["id"]).last_active_on == date.today()


def test_an_old_last_active_day_moves_forward(user):
    with app.app_context():
        db.session.get(User, user["id"]).last_active_on = date.today() - timedelta(days=40)
        db.session.commit()
    signed_in(user).get("/")
    assert get_user(user["id"]).last_active_on == date.today()


# ---------------------------------------------------------------------------
# 3. Level 3 date
# ---------------------------------------------------------------------------

def _xp_for_level(level):
    from progress import XP_LEVELS
    return XP_LEVELS[level]


def test_reaching_level_3_is_stamped_once(user):
    import activity
    with app.test_request_context():
        from flask_login import login_user
        u = db.session.get(User, user["id"])
        login_user(u)
        activity.mark_level3(2, 3)
        first = u.level3_reached_at
        assert first is not None
        activity.mark_level3(2, 3)          # a second crossing changes nothing
        assert u.level3_reached_at == first
        db.session.rollback()


def test_levels_that_dont_cross_3_leave_it_alone(user):
    import activity
    with app.test_request_context():
        from flask_login import login_user
        u = db.session.get(User, user["id"])
        login_user(u)
        activity.mark_level3(1, 2)
        activity.mark_level3(3, 4)
        assert u.level3_reached_at is None
        db.session.rollback()


def test_add_xp_past_level_3_records_it(user):
    from rewards import add_xp
    with app.test_request_context():
        from flask import session
        from flask_login import login_user
        u = db.session.get(User, user["id"])
        login_user(u)
        session["user_progress"] = {"xp": _xp_for_level(3) - 1, "level": 2}
        session["user_progress"].update({k: v for k, v in {
            "subscription_tier": "free", "is_developer": False}.items()})
        with patch("rewards.active_tier", return_value="free"):
            add_xp(5)
        assert u.level3_reached_at is not None
        db.session.rollback()


# ---------------------------------------------------------------------------
# 2. Cancellation date and reason
# ---------------------------------------------------------------------------

def _paid(uid, sub_id="sub_ltv"):
    with app.app_context():
        u = db.session.get(User, uid)
        u.subscription_tier, u.subscription_status = "basic", "active"
        u.stripe_subscription_id = sub_id
        db.session.commit()


def test_cancelling_in_the_app_records_when(user):
    _paid(user["id"])
    now = utcnow().replace(microsecond=0)
    stripe_sub = {"status": "active", "cancel_at_period_end": True,
                  "canceled_at": unix(now),
                  "current_period_end": unix(now + timedelta(days=20))}
    with patch("app.stripe.api_key", "sk_test_fake"), \
         patch("app.stripe.Subscription.modify", return_value=stripe_sub):
        signed_in(user).post("/subscribe/cancel-subscription", json={})
    assert get_user(user["id"]).canceled_at == now


def test_cancel_date_falls_back_to_now_if_stripe_omits_it(user):
    _paid(user["id"])
    stripe_sub = {"status": "active", "cancel_at_period_end": True}
    with patch("app.stripe.api_key", "sk_test_fake"), \
         patch("app.stripe.Subscription.modify", return_value=stripe_sub):
        signed_in(user).post("/subscribe/cancel-subscription", json={})
    assert get_user(user["id"]).canceled_at is not None


def test_the_goodbye_page_asks_why(user):
    _paid(user["id"])
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.subscription_status, u.canceled_at = "canceling", utcnow()
        db.session.commit()
    body = signed_in(user).get("/subscription-goodbye").get_data(as_text=True)
    assert 'action="/api/cancel-reason"' in body
    assert "I&#39;m not using it enough" in body or "I'm not using it enough" in body


def test_a_cancel_reason_is_saved(user):
    _paid(user["id"])
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.subscription_status, u.canceled_at = "canceling", utcnow()
        db.session.commit()
    r = signed_in(user).post("/api/cancel-reason",
                             json={"reason": "not_using", "comment": "  busy month  "})
    assert r.get_json()["success"] is True
    u = get_user(user["id"])
    assert (u.cancel_reason, u.cancel_comment) == ("not_using", "busy month")


def test_an_unknown_reason_is_refused(user):
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.subscription_status, u.canceled_at = "canceling", utcnow()
        db.session.commit()
    r = signed_in(user).post("/api/cancel-reason", json={"reason": "<script>"})
    assert r.status_code == 400
    assert get_user(user["id"]).cancel_reason is None


def test_someone_who_hasnt_cancelled_cant_give_a_reason(user):
    _paid(user["id"])
    r = signed_in(user).post("/api/cancel-reason", json={"reason": "other"})
    assert r.status_code == 400
    assert get_user(user["id"]).cancel_reason is None


def test_the_reason_must_be_sent_as_json(user):
    r = signed_in(user).post("/api/cancel-reason", data={"reason": "other"})
    assert r.status_code == 415


def test_resubscribing_clears_the_old_cancellation(user):
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.canceled_at, u.cancel_reason = utcnow(), "too_expensive"
        db.session.commit()
    post_event({"type": "customer.subscription.updated", "data": {"object": {
        "id": "sub_new", "customer": user["customer"], "status": "active",
        "metadata": {"user_id": str(user["id"]), "tier": "pro"}}}})
    u = get_user(user["id"])
    assert u.canceled_at is None and u.cancel_reason is None


def test_the_webhook_copies_stripes_cancel_date(user):
    when = utcnow().replace(microsecond=0) - timedelta(days=2)
    post_event({"type": "customer.subscription.deleted", "data": {"object": {
        "id": "sub_gone", "customer": user["customer"], "status": "canceled",
        "canceled_at": unix(when),
        "metadata": {"user_id": str(user["id"]), "tier": "basic"}}}})
    assert get_user(user["id"]).canceled_at == when


# ---------------------------------------------------------------------------
# 4. Monthly or annual on each payment
# ---------------------------------------------------------------------------

def test_a_new_annual_subscription_is_marked_year(user):
    post_event({"type": "checkout.session.completed", "data": {"object": {
        "id": f"cs_{uuid.uuid4().hex[:8]}", "customer": user["customer"],
        "metadata": {"user_id": str(user["id"]), "tier": "pro", "period": "year"},
        "amount_total": 9900, "currency": "gbp"}}})
    with app.app_context():
        assert Payment.query.filter_by(user_id=user["id"]).one().billing_period == "year"


def test_a_renewal_reads_its_period_from_the_invoice(user):
    _paid(user["id"], sub_id="sub_inv")
    post_event({"type": "invoice.paid", "data": {"object": {
        "id": f"in_{uuid.uuid4().hex[:8]}", "subscription": "sub_inv",
        "customer": user["customer"], "billing_reason": "subscription_cycle",
        "amount_paid": 499, "currency": "gbp",
        "lines": {"data": [{"price": {"recurring": {"interval": "month"}}}]}}}})
    with app.app_context():
        assert Payment.query.filter_by(user_id=user["id"]).one().billing_period == "month"


def test_a_renewal_without_a_period_borrows_the_last_subscriptions(user):
    _paid(user["id"], sub_id="sub_inv2")
    with app.app_context():
        db.session.add(Payment(provider="stripe", provider_ref=f"cs_{uuid.uuid4().hex[:8]}",
                               kind="subscription", user_id=user["id"],
                               billing_period="year"))
        db.session.commit()
    post_event({"type": "invoice.paid", "data": {"object": {
        "id": f"in_{uuid.uuid4().hex[:8]}", "subscription": "sub_inv2",
        "customer": user["customer"], "billing_reason": "subscription_cycle",
        "amount_paid": 9900, "currency": "gbp"}}})
    with app.app_context():
        renewal = Payment.query.filter_by(user_id=user["id"], kind="renewal").one()
        assert renewal.billing_period == "year"


def test_a_nonsense_period_is_not_stored(user):
    with app.app_context():
        A._record_payment(provider_ref=f"cs_{uuid.uuid4().hex[:8]}", kind="subscription",
                          user=db.session.get(User, user["id"]), billing_period="fortnight")
        assert Payment.query.filter_by(user_id=user["id"]).one().billing_period is None


# ---------------------------------------------------------------------------
# The report
# ---------------------------------------------------------------------------

def _load_report():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "ltv_report.py")
    spec = importlib.util.spec_from_file_location("ltv_report", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_report_adds_up_ltv_per_source(user):
    report_mod = _load_report()
    tag = f"src{uuid.uuid4().hex[:6]}"
    since = utcnow() - timedelta(minutes=5)
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.signup_source, u.signup_campaign = tag, "test"
        u.last_active_on = date.today()
        u.level3_reached_at = utcnow()
        u.cancel_reason = "too_expensive"
        for kind, pence, period in (("subscription", 499, "month"),
                                    ("renewal", 499, "month"),
                                    ("addon", 1499, None)):
            db.session.add(Payment(provider="stripe", provider_ref=f"x_{uuid.uuid4().hex[:8]}",
                                   kind=kind, user_id=u.id, amount_pence=pence,
                                   currency="gbp", billing_period=period))
        # A gift is not a sale and must not count as LTV.
        db.session.add(Payment(provider="stripe", provider_ref=f"x_{uuid.uuid4().hex[:8]}",
                               kind="dana", user_id=u.id, amount_pence=5000, currency="gbp"))
        db.session.commit()
        report = report_mod.build_report(User, Payment, since=since)

    row = next(r for r in report["rows"] if r["source"] == tag)
    assert row["signups"] == 1 and row["payers"] == 1
    assert row["revenue_pence"] == 499 + 499 + 1499
    assert row["ltv_signup_pence"] == row["ltv_payer_pence"] == 2497
    assert row["level3"] == 1 and row["active"] == 1
    assert report["reasons"]["too_expensive"] >= 1
    assert report["periods"]["month"] >= 2
