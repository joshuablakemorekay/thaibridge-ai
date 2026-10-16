"""
Tests for forgotten-password reset and logged-in password change (2026-10-16).

Before these, a learner who forgot their password had no way back in short of
Josh editing the live database. The reset link is a signed, timed token that
also carries a fingerprint of the current password hash, so it works once and
dies the moment the password changes. No email is sent here: the send function
is patched, and the link it would have sent is captured instead.

Run with:  pytest tests/test_password_reset.py -v
"""

import os
import uuid
from unittest.mock import patch
from urllib.parse import urlparse

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as A  # noqa: E402
from app import app, db, User  # noqa: E402

OLD_PASSWORD = "OldPass123"
NEW_PASSWORD = "NewPass456"


@pytest.fixture
def user():
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"pw_{tag}", email=f"pw_{tag}@example.com")
        u.set_password(OLD_PASSWORD)
        db.session.add(u)
        db.session.commit()
        info = {"id": u.id, "username": u.username, "email": u.email}
    yield info
    with app.app_context():
        User.query.filter_by(id=info["id"]).delete()
        db.session.commit()


def request_reset(client, email):
    """POST the forgot-password form; return (response, link that would be emailed)."""
    sent = []
    with patch.object(A, "send_password_reset_email",
                      side_effect=lambda u, link: sent.append(link)):
        r = client.post("/forgot-password", json={"email": email})
    return r, (sent[0] if sent else None)


def path_of(link):
    return urlparse(link).path


def can_log_in(password, identifier):
    r = app.test_client().post("/login", json={"identifier": identifier, "password": password})
    return r.status_code == 200


# ── Asking for a link ─────────────────────────────────────────────────────

def test_login_page_links_to_forgot_password():
    assert 'href="/forgot-password"' in app.test_client().get("/login").get_data(as_text=True)


def test_known_and_unknown_emails_get_the_same_reply(user):
    client = app.test_client()
    known, link = request_reset(client, user["email"].upper())   # case doesn't matter
    unknown, no_link = request_reset(client, "nobody-here@example.com")
    assert link is not None and no_link is None
    assert known.status_code == unknown.status_code == 200
    assert known.get_json() == unknown.get_json()


def test_link_uses_the_public_address_when_set(user):
    with patch.object(A, "PUBLIC_BASE_URL", "https://thaibridge-ai.smoald.com"):
        _, link = request_reset(app.test_client(), user["email"])
    assert link.startswith("https://thaibridge-ai.smoald.com/reset-password/")


# ── Using the link ────────────────────────────────────────────────────────

def test_reset_sets_the_new_password_and_logs_in(user):
    client = app.test_client()
    _, link = request_reset(client, user["email"])
    assert "Choose a new password" in client.get(path_of(link)).get_data(as_text=True)

    r = client.post(path_of(link), json={"password": NEW_PASSWORD,
                                         "confirm_password": NEW_PASSWORD})
    assert r.status_code == 200 and r.get_json()["success"]
    assert can_log_in(NEW_PASSWORD, user["username"])
    assert not can_log_in(OLD_PASSWORD, user["username"])
    # Logged in by the reset itself: the change-password box shows on /progress.
    assert "Change password" in client.get("/progress").get_data(as_text=True)


def test_link_works_only_once(user):
    client = app.test_client()
    _, link = request_reset(client, user["email"])
    client.post(path_of(link), json={"password": NEW_PASSWORD, "confirm_password": NEW_PASSWORD})

    again = app.test_client()
    assert "expired or has already been used" in again.get(path_of(link)).get_data(as_text=True)
    r = again.post(path_of(link), json={"password": "Another789", "confirm_password": "Another789"})
    assert r.status_code == 400
    assert can_log_in(NEW_PASSWORD, user["username"])


def test_expired_link_is_refused(user):
    _, link = request_reset(app.test_client(), user["email"])
    with patch.object(A, "PASSWORD_RESET_MAX_AGE", -1):
        r = app.test_client().post(path_of(link), json={"password": NEW_PASSWORD,
                                                        "confirm_password": NEW_PASSWORD})
    assert r.status_code == 400
    assert can_log_in(OLD_PASSWORD, user["username"])


def test_tampered_link_is_refused(user):
    _, link = request_reset(app.test_client(), user["email"])
    r = app.test_client().post(path_of(link) + "x", json={"password": NEW_PASSWORD,
                                                         "confirm_password": NEW_PASSWORD})
    assert r.status_code == 400


@pytest.mark.parametrize("password, confirm, expected", [
    ("short1", "short1", "at least 8 characters"),
    ("nonumbers", "nonumbers", "one letter and one number"),
    ("Mismatch123", "Mismatch124", "do not match"),
])
def test_reset_keeps_the_signup_password_rules(user, password, confirm, expected):
    _, link = request_reset(app.test_client(), user["email"])
    r = app.test_client().post(path_of(link), json={"password": password,
                                                    "confirm_password": confirm})
    assert r.status_code == 400 and expected in r.get_json()["message"]
    assert can_log_in(OLD_PASSWORD, user["username"])


# ── Sending the email ─────────────────────────────────────────────────────

def test_no_resend_key_logs_the_link_instead_of_sending(user):
    with app.app_context(), patch.object(A, "RESEND_API_KEY", None), \
         patch("app.httpx.post") as post:
        A.send_password_reset_email(db.session.get(User, user["id"]), "https://x/reset-password/t")
    post.assert_not_called()


def test_resend_failure_never_reaches_the_user(user):
    with patch.object(A, "RESEND_API_KEY", "re_test"), \
         patch("app.httpx.post", side_effect=RuntimeError("Resend is down")) as post:
        r = app.test_client().post("/forgot-password", json={"email": user["email"]})
    assert post.called
    assert r.status_code == 200 and r.get_json()["success"]


# ── Changing it while logged in ───────────────────────────────────────────

def logged_in(user):
    c = app.test_client()
    c.post("/login", json={"identifier": user["username"], "password": OLD_PASSWORD})
    return c


def test_change_password_needs_the_current_one(user):
    r = logged_in(user).post("/change-password", json={
        "current_password": "WrongPass1", "new_password": NEW_PASSWORD,
        "confirm_password": NEW_PASSWORD})
    assert r.status_code == 400
    assert can_log_in(OLD_PASSWORD, user["username"])


def test_change_password_works(user):
    r = logged_in(user).post("/change-password", json={
        "current_password": OLD_PASSWORD, "new_password": NEW_PASSWORD,
        "confirm_password": NEW_PASSWORD})
    assert r.status_code == 200 and r.get_json()["success"]
    assert can_log_in(NEW_PASSWORD, user["username"])


def test_change_password_cancels_an_outstanding_reset_link(user):
    _, link = request_reset(app.test_client(), user["email"])
    logged_in(user).post("/change-password", json={
        "current_password": OLD_PASSWORD, "new_password": NEW_PASSWORD,
        "confirm_password": NEW_PASSWORD})
    r = app.test_client().post(path_of(link), json={"password": "Another789",
                                                    "confirm_password": "Another789"})
    assert r.status_code == 400


def test_change_password_requires_login():
    r = app.test_client().post("/change-password", json={})
    assert r.status_code in (302, 401)
