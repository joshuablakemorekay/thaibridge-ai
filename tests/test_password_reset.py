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

import accounts  # noqa: E402
from app import app, db, User  # noqa: E402

OLD_PASSWORD = "OldPass123"
NEW_PASSWORD = "NewPass456"


@pytest.fixture(autouse=True)
def outbox():
    """Every email the app hands off, as (to, subject, text), instead of a
    background thread trying to send it."""
    sent = []
    with patch.object(accounts, "send_in_background", side_effect=lambda *m: sent.append(m)):
        yield sent


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
    with patch.object(accounts, "send_reset_email",
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


def test_link_uses_the_public_address_when_set(user, monkeypatch):
    monkeypatch.setenv("PUBLIC_BASE_URL", "https://thaibridge-ai.smoald.com")
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
    with patch.object(accounts, "PASSWORD_RESET_MAX_AGE", -1):
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

def test_no_resend_key_logs_instead_of_sending(monkeypatch, caplog):
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    with patch("accounts.httpx.post") as post:
        accounts.send_email("a@example.com", "Subject", "https://x/reset-password/t")
    post.assert_not_called()
    assert "https://x/reset-password/t" in caplog.text   # the link is still findable


def test_a_resend_failure_is_swallowed(monkeypatch):
    monkeypatch.setenv("RESEND_API_KEY", "re_test")
    with patch("accounts.httpx.post", side_effect=RuntimeError("Resend is down")) as post:
        accounts.send_email("a@example.com", "Subject", "Body")   # must not raise
    assert post.called


def test_forgot_password_never_waits_for_resend(user, outbox, monkeypatch):
    """The reply must not wait on the send, or its timing would reveal which
    emails have accounts even though the text is identical."""
    monkeypatch.setenv("RESEND_API_KEY", "re_test")
    with patch("accounts.httpx.post") as post:
        r = app.test_client().post("/forgot-password", json={"email": user["email"]})
    assert r.status_code == 200
    post.assert_not_called()                  # nothing sent inside the request…
    assert [m[0] for m in outbox] == [user["email"]]   # …it was handed to the background


def test_reset_and_change_both_tell_the_owner(user, outbox):
    _, link = request_reset(app.test_client(), user["email"])
    app.test_client().post(path_of(link), json={"password": NEW_PASSWORD,
                                                "confirm_password": NEW_PASSWORD})
    c = app.test_client()
    c.post("/login", json={"identifier": user["username"], "password": NEW_PASSWORD})
    c.post("/change-password", json={"current_password": NEW_PASSWORD,
                                     "new_password": "Third789x",
                                     "confirm_password": "Third789x"})
    notices = [m for m in outbox if m[1] == "Your ThaiBridge AI password was changed"]
    assert len(notices) == 2 and all(m[0] == user["email"] for m in notices)
    assert "/forgot-password" in notices[0][2]


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


# ── Signing out everywhere ────────────────────────────────────────────────

def is_signed_in(client):
    return "Change password" in client.get("/progress").get_data(as_text=True)


def remember_cookie_only(client):
    """Drop the session cookie, as if the browser had been closed, so only the
    long-lived remember-me cookie is left to sign this device in."""
    client.delete_cookie("session")
    return client


def test_changing_password_signs_out_other_devices_but_not_this_one(user):
    phone, laptop = logged_in(user), logged_in(user)
    assert is_signed_in(phone) and is_signed_in(laptop)

    laptop.post("/change-password", json={"current_password": OLD_PASSWORD,
                                          "new_password": NEW_PASSWORD,
                                          "confirm_password": NEW_PASSWORD})
    assert is_signed_in(laptop)
    assert not is_signed_in(phone)


def test_changing_password_also_kills_remember_me_cookies(user):
    tablet = remember_cookie_only(logged_in(user))
    assert is_signed_in(tablet)          # the remember-me cookie alone is enough…

    logged_in(user).post("/change-password", json={"current_password": OLD_PASSWORD,
                                                   "new_password": NEW_PASSWORD,
                                                   "confirm_password": NEW_PASSWORD})
    assert not is_signed_in(remember_cookie_only(tablet))   # …until the password changes


def test_a_reset_signs_out_every_other_device(user):
    phone = logged_in(user)
    resetter = app.test_client()
    _, link = request_reset(resetter, user["email"])
    resetter.post(path_of(link), json={"password": NEW_PASSWORD,
                                       "confirm_password": NEW_PASSWORD})
    assert is_signed_in(resetter)
    assert not is_signed_in(phone)


def test_cookies_from_before_versions_still_work(user):
    """A bare user id is what every cookie held before this shipped. It must
    count as version 0, or deploying it would sign everybody out."""
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.session_version = 0
        db.session.commit()
    old = app.test_client()
    with old.session_transaction() as s:
        s["_user_id"] = str(user["id"])
        s["_fresh"] = True
    assert is_signed_in(old)


def test_a_malformed_session_id_is_just_signed_out():
    c = app.test_client()
    with c.session_transaction() as s:
        s["_user_id"] = "not-a-number:x"
    assert not is_signed_in(c)


def test_a_signed_out_device_keeps_what_it_earns_as_a_guest(user):
    """The dead login is cleared once, on the first page after the change.
    Before, it came back on every page and wiped the guest's progress each time."""
    phone = logged_in(user)
    logged_in(user).post("/change-password", json={"current_password": OLD_PASSWORD,
                                                   "new_password": NEW_PASSWORD,
                                                   "confirm_password": NEW_PASSWORD})
    assert not is_signed_in(phone)
    assert phone.get_cookie("remember_token") is None
    with phone.session_transaction() as s:
        assert "_user_id" not in s
        s["user_progress"] = {**s.get("user_progress", {}), "xp": 42}

    phone.get("/")
    with phone.session_transaction() as s:
        assert s["user_progress"]["xp"] == 42


def test_changing_password_keeps_progress_earned_this_visit(user):
    """Re-signing-in after a password change must not reload the saved copy of
    progress over the session, or anything not yet saved would be rewound."""
    c = logged_in(user)
    with c.session_transaction() as s:
        # Reassigned, not edited in place: an in-place edit of a nested dict
        # doesn't mark the session as changed, so it would never be saved.
        s["user_progress"] = {**s["user_progress"], "xp": 500}
    c.post("/change-password", json={"current_password": OLD_PASSWORD,
                                     "new_password": NEW_PASSWORD,
                                     "confirm_password": NEW_PASSWORD})
    with c.session_transaction() as s:
        assert s["user_progress"]["xp"] == 500


def test_logging_in_restores_saved_progress(user):
    """auth.py never touches progress; app.py restores it on the login signal."""
    with app.app_context():
        u = db.session.get(User, user["id"])
        u.progress = {"xp": 321, "level": 3}
        db.session.commit()
    c = logged_in(user)
    with c.session_transaction() as s:
        assert s["user_progress"]["xp"] == 321
