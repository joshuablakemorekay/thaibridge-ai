"""
Tests for progress persistence and AI rate limiting (added 2026-08-17).

Both features were verified once by hand when they were built, in scripts that
lived in a temp folder and no longer exist. That is not a check — it is a
memory. These are the same assertions made permanent, so a future change that
breaks them fails here instead of quietly shipping.

The two that matter most:

  * progress survives losing the cookie — the whole point of the feature
  * the rate-limit key is the VISITOR, not the proxy — get that wrong and every
    visitor on earth shares one quota, which takes the site down for everyone
    rather than protecting it

Run with:  pytest tests/test_progress_and_limits.py -v
"""

import os
import uuid
import pytest

# Must be set before app.py is imported (module-level guards), same as the
# other test modules. conftest.py has already popped DATABASE_URL and switched
# the rate limits off for the suite.
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import (  # noqa: E402
    app, db, User, _PROGRESS_NOT_SAVED, _rate_limit_key,
)

PASSWORD = "TestPass123"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def unique_username(prefix="t"):
    """A name no other test or earlier run can be holding.

    Deriving it from hash() looked fine and was not: a run that dies before its
    cleanup leaves the row behind, the next run picks the same name, signup
    fails on the duplicate, and the test reports a defect in code that is
    working. A test that can fail for reasons unrelated to the thing it tests is
    worse than no test, because it teaches you to ignore it.
    """
    return f"{prefix}{uuid.uuid4().hex[:10]}"


def _delete_user(username):
    with app.app_context():
        row = User.query.filter_by(username=username).first()
        if row:
            db.session.delete(row)
            db.session.commit()


@pytest.fixture
def account():
    """A registered, logged-in browser. Yields (client, username), then removes
    the user so the local database is left as it was found."""
    username = unique_username()
    client = app.test_client()
    response = client.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    }).get_json()
    # Fail loudly here rather than letting every assertion below fail obscurely.
    assert response.get("success"), f"signup failed: {response.get('message')}"
    try:
        yield client, username
    finally:
        _delete_user(username)


def award(client, points):
    """Earn XP the way the app really does, through the endpoint."""
    return client.post("/api/award_points",
                       json={"action": "test", "points": points}).get_json()


def saved_progress(username):
    with app.app_context():
        row = User.query.filter_by(username=username).first()
        return row.progress if row else None


# ---------------------------------------------------------------------------
# Progress persistence
# ---------------------------------------------------------------------------

def test_progress_reaches_the_database(account):
    client, username = account
    award(client, 250)
    stored = saved_progress(username)
    assert stored is not None, "nothing was written to the user's row"
    assert stored["xp"] == 250


def test_progress_survives_losing_the_cookie(account):
    """The feature's whole reason for existing: a new device, or cleared
    cookies, must not send a learner back to level 1."""
    client, username = account
    earned = award(client, 250)

    fresh = app.test_client()          # no cookies at all — a different browser
    with fresh.session_transaction() as s:
        assert "user_progress" not in s

    fresh.post("/login", json={"identifier": username, "password": PASSWORD})
    restored = award(fresh, 0)         # 0 points: just read the totals back

    assert restored["total_xp"] == earned["total_xp"]
    assert restored["level"] == earned["level"]


def test_authoritative_fields_are_never_saved(account):
    """Subscription tier, full_unlock and the alphabet gate have their own
    columns, and those columns are what gate access. A saved blob must never be
    able to contradict them."""
    client, username = account
    award(client, 10)
    stored = saved_progress(username)
    leaked = set(stored) & _PROGRESS_NOT_SAVED
    assert not leaked, f"these must not be persisted: {sorted(leaked)}"


def test_a_poisoned_blob_cannot_grant_a_paid_tier(account):
    """Even if a blob somehow contained a paid tier, loading it must not upgrade
    anyone. Filtering happens on the way in as well as the way out."""
    client, username = account
    award(client, 10)

    with app.app_context():
        row = User.query.filter_by(username=username).first()
        row.progress = dict(row.progress or {},
                            subscription_tier="pro", full_unlock=True,
                            alphabet_completed=True, is_developer=True)
        db.session.commit()

    fresh = app.test_client()
    fresh.post("/login", json={"identifier": username, "password": PASSWORD})
    with fresh.session_transaction() as s:
        loaded = s["user_progress"]

    assert loaded["subscription_tier"] == "free"
    assert loaded["full_unlock"] is False
    assert loaded["is_developer"] is False

    with app.app_context():
        row = User.query.filter_by(username=username).first()
        assert row.effective_tier == "free"
        assert row.full_unlock is False


# ---------------------------------------------------------------------------
# Which anonymous progress a new account is allowed to inherit
# ---------------------------------------------------------------------------

def _age_the_session(client, hours=None, last_login=None):
    """Backdate this browser's progress, as if it were earned `hours` ago.

    Reassigns the whole dict rather than editing a key inside it. Flask only
    notices top-level changes to the session, so a nested edit here is silently
    dropped — which is the same reason app.py sets session.modified by hand
    everywhere it touches user_progress. The first version of this helper edited
    in place, the backdating never reached the cookie, and two tests failed
    against code that was working perfectly.
    """
    from datetime import datetime, timedelta
    stamp = last_login if last_login is not None else (
        datetime.now() - timedelta(hours=hours)).isoformat()
    with client.session_transaction() as s:
        progress = dict(s["user_progress"])
        progress["last_login"] = stamp
        s["user_progress"] = progress


def _signup(client, username):
    return client.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    }).get_json()


def test_xp_earned_this_visit_survives_signing_up():
    """The reason the carry-over exists: try the quiz, then register, keep it."""
    client = app.test_client()
    award(client, 90)
    _age_the_session(client, hours=1)
    username = unique_username("fresh")
    try:
        assert _signup(client, username)["success"]
        assert award(client, 0)["total_xp"] == 90
    finally:
        _delete_user(username)


def test_a_stale_cookie_does_not_land_on_a_new_account():
    """What went wrong in practice: a two-day-old cookie reappeared on a brand
    new account, which looked exactly like a database that had failed to clear —
    and on a shared computer would hand one person another's progress."""
    client = app.test_client()
    award(client, 145)
    _age_the_session(client, hours=48)
    username = unique_username("stale")
    try:
        assert _signup(client, username)["success"]
        assert award(client, 0)["total_xp"] == 0, "stale progress was inherited"
    finally:
        _delete_user(username)


def test_progress_of_unknown_age_is_not_inherited():
    """Anything unreadable counts as stale — inheriting progress you cannot date
    is the outcome worth avoiding."""
    client = app.test_client()
    award(client, 70)
    _age_the_session(client, last_login="not a timestamp")
    username = unique_username("bad")
    try:
        _signup(client, username)
        assert award(client, 0)["total_xp"] == 0
    finally:
        _delete_user(username)


def test_a_returning_user_keeps_their_saved_progress_however_old(account):
    """The age check must only ever apply to accounts with nothing saved. A
    long-standing user logging in after a month away must not be reset."""
    client, username = account
    award(client, 200)

    returning = app.test_client()
    award(returning, 5)                       # some unrelated browsing
    _age_the_session(returning, hours=72)     # on a long-stale session
    returning.post("/login", json={"identifier": username, "password": PASSWORD})
    assert award(returning, 0)["total_xp"] == 200


def test_logged_out_visitors_still_earn_xp():
    """The site works without an account and must keep doing so — no user row
    means no persistence, exactly as before."""
    anon = app.test_client()
    assert award(anon, 40)["total_xp"] == 40


def test_signing_up_does_not_cost_you_the_xp_you_already_earned():
    """Earn XP while browsing, then register: a new account has no saved
    progress, so the session must carry over rather than be reset."""
    client = app.test_client()
    award(client, 120)
    username = unique_username("carry")
    client.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    })
    try:
        assert award(client, 0)["total_xp"] == 120
    finally:
        _delete_user(username)


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

def test_rate_limit_key_prefers_the_cloudflare_header():
    """Render serves through Cloudflare, so remote_addr is a proxy. Keying on it
    would give every visitor one shared quota."""
    with app.test_request_context("/", headers={
        "CF-Connecting-IP": "9.9.9.9",
        "X-Forwarded-For": "1.1.1.1, 2.2.2.2",
    }):
        assert _rate_limit_key() == "9.9.9.9"


def test_rate_limit_key_falls_back_to_forwarded_for():
    with app.test_request_context("/", headers={
        "X-Forwarded-For": "1.1.1.1, 2.2.2.2",
    }):
        assert _rate_limit_key() == "1.1.1.1"


def test_rate_limit_key_falls_back_to_remote_addr():
    with app.test_request_context("/"):
        assert _rate_limit_key() is not None


def test_two_visitors_get_separate_buckets():
    """The failure this guards against is subtle: if the key were the proxy,
    both calls would return the same string and one visitor could lock out
    everybody else."""
    with app.test_request_context("/", headers={"CF-Connecting-IP": "203.0.113.1"}):
        first = _rate_limit_key()
    with app.test_request_context("/", headers={"CF-Connecting-IP": "198.51.100.1"}):
        second = _rate_limit_key()
    assert first != second


def test_a_rate_limited_response_is_json_the_chat_window_can_read():
    """The AI routes speak JSON. Flask's default 429 is an HTML page, which
    would reach the user as a parse error rather than a readable message."""
    from app import _rate_limit_exceeded
    from werkzeug.exceptions import TooManyRequests

    with app.test_request_context("/api/ai/chat"):
        payload, status = _rate_limit_exceeded(TooManyRequests())
        data = payload.get_json()

    assert status == 429
    assert data["success"] is False
    assert data["gate"] == "rate_limited"     # what the frontend branches on
    assert data["message"]                    # what the human reads


def test_the_429_handler_is_actually_registered():
    """The handler above is only useful if Flask will call it. Asserting the
    function in isolation would pass even if it were never wired up."""
    from werkzeug.exceptions import TooManyRequests
    assert app.error_handler_spec[None][429] or \
        any(429 in spec for spec in app.error_handler_spec.get(None, {}) if spec), \
        "no 429 handler registered"
    with app.test_request_context("/api/ai/chat"):
        handler = app._find_error_handler(TooManyRequests(), [])
    assert handler is not None, "Flask would fall back to the HTML error page"
