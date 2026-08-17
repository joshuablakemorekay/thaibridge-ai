"""
Tests for the developer-mode gate (added 2026-08-17).

Developer mode bypasses every access check in the app — alphabet, level and
subscription tier. It used to fall back to the password "changeme" when
DEVELOPER_PASSWORD was unset, which meant an unconfigured deployment handed the
entire paid course to anyone who had read the source. It failed *open*, and
silently: a working login looks the same either way.

These tests pin the corrected behaviour — no password configured means the door
does not exist — because that is precisely the kind of regression nothing else
would notice.

Run with:  pytest tests/test_developer_mode.py -v
"""

import os
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as appmod  # noqa: E402
from app import app  # noqa: E402


@pytest.fixture
def developer_mode_unconfigured(monkeypatch):
    """Simulate a deployment with no DEVELOPER_PASSWORD set."""
    monkeypatch.setattr(appmod, "DEVELOPER_MODE_ENABLED", False)
    monkeypatch.setattr(appmod, "DEVELOPER_PASSWORD_HASH", None)


# ---------------------------------------------------------------------------
# Fails closed when unconfigured
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("configured", [None, "", "   ", "\t\n"])
def test_no_password_configured_means_developer_mode_is_off(configured):
    """The behaviour that matters, tested against the logic rather than the
    module constant.

    Reading the constant instead looked equivalent and wasn't: this machine has
    DEVELOPER_PASSWORD set, so the constant is correct here no matter what the
    code does with an unset one. Putting the 'changeme' default back left every
    test green. Calling the function directly is the only version that fails.
    """
    enabled, password_hash = appmod._developer_credentials(configured)
    assert enabled is False
    assert password_hash is None


def test_the_old_default_password_is_gone():
    """'changeme' was the fallback. With nothing configured there must be no
    valid password at all — least of all that one."""
    import hashlib
    enabled, password_hash = appmod._developer_credentials(None)
    assert not enabled
    assert password_hash != hashlib.sha256(b"changeme").hexdigest()


def test_a_configured_password_is_hashed_not_stored():
    enabled, password_hash = appmod._developer_credentials("hunter2")
    import hashlib
    assert enabled is True
    assert password_hash == hashlib.sha256(b"hunter2").hexdigest()
    assert "hunter2" not in (password_hash or "")


def test_unconfigured_deployment_refuses_every_password(developer_mode_unconfigured):
    """No password set means no way in — not 'any password works', and not
    'the documented default works'."""
    client = app.test_client()
    for attempt in ("", "changeme", "password", "admin"):
        response = client.post("/developer-login", data={"password": attempt})
        assert response.status_code == 403, f"{attempt!r} was not refused"
        assert response.get_json()["success"] is False


def test_unconfigured_deployment_does_not_even_show_the_form(developer_mode_unconfigured):
    client = app.test_client()
    response = client.get("/developer-login")
    assert response.status_code == 302, "the login form should not be reachable"


def test_unconfigured_deployment_grants_no_access(developer_mode_unconfigured):
    """The real risk was never the form — it was the bypass behind it."""
    client = app.test_client()
    client.post("/developer-login", data={"password": "changeme"})
    with client.session_transaction() as s:
        assert s.get("user_progress", {}).get("is_developer") is not True


# ---------------------------------------------------------------------------
# Still works when it IS configured
# ---------------------------------------------------------------------------

def test_a_wrong_password_is_rejected_when_configured():
    """Guard against 'fixed' meaning 'broken for everyone'."""
    client = app.test_client()
    response = client.post("/developer-login",
                           data={"password": "definitely-not-the-password"})
    assert response.get_json()["success"] is False
    with client.session_transaction() as s:
        assert s.get("user_progress", {}).get("is_developer") is not True


def test_the_correct_password_still_unlocks_developer_mode(monkeypatch):
    """The one path that must keep working. Uses a known password rather than
    the real one, so the test never needs the live secret."""
    import hashlib
    secret = "a-known-test-password"
    monkeypatch.setattr(appmod, "DEVELOPER_MODE_ENABLED", True)
    monkeypatch.setattr(appmod, "DEVELOPER_PASSWORD_HASH",
                        hashlib.sha256(secret.encode()).hexdigest())

    client = app.test_client()
    response = client.post("/developer-login", data={"password": secret})
    assert response.get_json()["success"] is True
    with client.session_transaction() as s:
        assert s["user_progress"]["is_developer"] is True
