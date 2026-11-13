"""Learners can delete their own account (auth.delete_account, added 2026-11-13).

Settled with Josh: payments are kept but unlinked (UK tax law), AI usage is
unlinked, a review is deleted, and a plan that will still renew has to be
cancelled first.

Run with:  pytest tests/test_account_deletion.py -v
"""
import uuid
from unittest.mock import patch

import pytest

from app import AiUsage, Payment, app
from models import AppReview, User, db

PASSWORD = "TestPass123"


def make_user(**fields):
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"del_{tag}", email=f"del_{tag}@example.com", **fields)
        u.set_password(PASSWORD)
        db.session.add(u)
        db.session.commit()
        return {"id": u.id, "login": f"{u.id}:{u.session_version or 0}",
                "email": u.email, "username": u.username, "tag": tag}


@pytest.fixture
def account():
    """A learner with a payment, two AI usage rows and a review."""
    info = make_user()
    with app.app_context():
        db.session.add(Payment(user_id=info["id"], provider="stripe",
                               provider_ref=f"cs_{info['tag']}", kind="subscription",
                               tier="basic", amount_pence=999, currency="gbp"))
        for _ in range(2):
            db.session.add(AiUsage(user_id=info["id"], feature="chat", outcome="ok"))
        db.session.add(AppReview(user_id=info["id"], rating=4, comment="Lovely"))
        db.session.commit()
    yield info
    with app.app_context():
        Payment.query.filter_by(provider_ref=f"cs_{info['tag']}").delete()
        AiUsage.query.filter_by(user_id=info["id"]).delete()
        AppReview.query.filter_by(user_id=info["id"]).delete()
        User.query.filter_by(id=info["id"]).delete()
        db.session.commit()


def signed_in(info):
    app.config["TESTING"] = True
    client = app.test_client()
    with client.session_transaction() as s:
        s["_user_id"] = info["login"]
        s["_fresh"] = True
    return client


def delete(client, password=PASSWORD, confirm="DELETE"):
    with patch("accounts.send_deleted_email") as email:
        response = client.post("/delete-account", json={"password": password, "confirm": confirm})
    return response, email


def user_exists(uid):
    with app.app_context():
        return db.session.get(User, uid) is not None


# --- what must stop a deletion ------------------------------------------------

def test_a_wrong_password_deletes_nothing(account):
    response, email = delete(signed_in(account), password="not-it")
    assert response.status_code == 400
    assert user_exists(account["id"])
    email.assert_not_called()


def test_the_confirm_word_is_required(account):
    response, _ = delete(signed_in(account), confirm="yes")
    assert response.status_code == 400
    assert "DELETE" in response.get_json()["message"]
    assert user_exists(account["id"])


def test_the_confirm_word_is_not_case_sensitive(account):
    response, _ = delete(signed_in(account), confirm="  delete ")
    assert response.get_json()["success"] is True


def test_a_renewing_subscription_must_be_cancelled_first():
    info = make_user(subscription_tier="basic", subscription_status="active",
                     stripe_subscription_id="sub_renewing")
    try:
        response, _ = delete(signed_in(info))
        assert response.status_code == 400
        assert "cancel your subscription first" in response.get_json()["message"]
        assert user_exists(info["id"])
    finally:
        with app.app_context():
            User.query.filter_by(id=info["id"]).delete()
            db.session.commit()


def test_a_cancelled_plan_with_time_left_can_be_deleted():
    info = make_user(subscription_tier="basic", subscription_status="canceling",
                     stripe_subscription_id="sub_ending")
    response, _ = delete(signed_in(info))
    assert response.get_json()["success"] is True
    assert not user_exists(info["id"])


def test_signed_out_visitors_are_sent_to_log_in():
    client = app.test_client()
    response = client.post("/delete-account", json={"password": PASSWORD, "confirm": "DELETE"})
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


# --- what a deletion does -----------------------------------------------------

def test_the_account_and_review_are_gone(account):
    response, _ = delete(signed_in(account))
    assert response.get_json() == {"success": True, "redirect": "/account-deleted"}
    assert not user_exists(account["id"])
    with app.app_context():
        assert AppReview.query.filter_by(user_id=account["id"]).count() == 0


def test_payments_are_kept_but_no_longer_say_who_paid(account):
    delete(signed_in(account))
    with app.app_context():
        payment = Payment.query.filter_by(provider_ref=f"cs_{account['tag']}").one()
        assert payment.user_id is None
        assert payment.amount_pence == 999       # the record itself is intact


def test_ai_usage_is_kept_but_unlinked(account):
    with app.app_context():
        ids = [r.id for r in AiUsage.query.filter_by(user_id=account["id"])]
    delete(signed_in(account))
    with app.app_context():
        rows = AiUsage.query.filter(AiUsage.id.in_(ids)).all()
        assert len(rows) == 2 and all(r.user_id is None for r in rows)
        AiUsage.query.filter(AiUsage.id.in_(ids)).delete()
        db.session.commit()


def test_other_learners_are_untouched(account):
    other = make_user()
    try:
        delete(signed_in(account))
        assert user_exists(other["id"])
    finally:
        with app.app_context():
            User.query.filter_by(id=other["id"]).delete()
            db.session.commit()


def test_the_browser_is_signed_out(account):
    client = signed_in(account)
    delete(client)
    with client.session_transaction() as s:
        assert "_user_id" not in s and "user_progress" not in s
    assert client.get("/progress").status_code == 200   # still works, as a visitor


def test_a_confirmation_email_goes_to_the_old_address(account):
    _, email = delete(signed_in(account))
    email.assert_called_once_with(account["email"], account["username"])


def test_the_goodbye_page_renders():
    page = app.test_client().get("/account-deleted").get_data(as_text=True)
    assert "Your account has been deleted" in page


# --- the Progress page --------------------------------------------------------

def test_progress_offers_the_delete_form(account):
    page = signed_in(account).get("/progress").get_data(as_text=True)
    assert 'action="/delete-account"' in page and "data-json-post" in page


def test_progress_asks_a_subscriber_to_cancel_first():
    info = make_user(subscription_tier="basic", subscription_status="active",
                     stripe_subscription_id="sub_renewing2")
    try:
        page = signed_in(info).get("/progress").get_data(as_text=True)
        assert 'id="delete-account"' in page
        assert 'action="/delete-account"' not in page
        assert "subscription that will renew" in page
    finally:
        with app.app_context():
            User.query.filter_by(id=info["id"]).delete()
            db.session.commit()


def test_every_table_that_points_at_an_account_is_handled():
    """On Postgres, deleting a user that another row still points at fails.
    delete_account handles exactly these three tables. A new table with a link
    to users must be added there (unlink or delete), or this test fails."""
    linked = {table.name for table in db.metadata.tables.values()
              for fk in table.foreign_keys if fk.column.table.name == "users"}
    assert linked == {"payments", "ai_usage", "app_reviews"}
