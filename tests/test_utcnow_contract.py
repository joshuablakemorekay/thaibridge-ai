"""The app's clock stays naive, and the expiry comparison it feeds stays working.

Added 2026-08-19 while clearing the datetime.utcnow() deprecation warnings.

datetime.utcnow() is deprecated, and the replacement the warning itself
recommends — datetime.now(timezone.utc) — returns a *timezone-aware* datetime.
Every db.DateTime column in app.py is naive. Comparing the two raises
TypeError, so taking the warning's advice literally would have replaced a
harmless message with a crash on the paid-subscription check.

app.utcnow() therefore drops the tzinfo on purpose. That deliberate choice
looks exactly like an oversight to the next person who reads it, which is why
it is pinned here rather than left to a comment.

Run with:  pytest tests/test_utcnow_contract.py -v
"""

import os
from datetime import datetime, timedelta, timezone

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import User, utcnow  # noqa: E402


def test_utcnow_is_naive():
    """Aware would be more correct in the abstract and wrong for this schema."""
    assert utcnow().tzinfo is None, (
        "utcnow() has become timezone-aware; every db.DateTime column in "
        "app.py is naive, so this will raise TypeError the moment it is "
        "compared against a stored value"
    )


def test_utcnow_is_actually_utc():
    """Naive is the shape, not a licence to return local time."""
    drift = abs((utcnow() - datetime.now(timezone.utc).replace(tzinfo=None)).total_seconds())
    assert drift < 5, f"utcnow() is {drift:.0f}s from UTC — it is returning local time"


@pytest.mark.parametrize("expired,expected", [
    (True, "free"),
    (False, "pro"),
])
def test_the_paid_period_comparison_still_runs(expired, expected):
    """The line that would have crashed: a stored naive date vs the clock.

    Not persisted — the comparison is pure model logic, and the point is that
    it completes at all rather than raising TypeError on mixed awareness.
    """
    user = User(
        username="clocktest",
        email="clock@example.com",
        password_hash="x",
        subscription_tier="pro",
        subscription_status="active",
        current_period_end=utcnow() + timedelta(days=-1 if expired else 1),
    )
    assert user.effective_tier == expected
