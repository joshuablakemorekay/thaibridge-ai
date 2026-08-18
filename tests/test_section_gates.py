"""Tests for what a locked section TELLS a learner (added 2026-08-18).

check_section_access checks three gates in order and returns the first failure.
That is fine for deciding access and was misleading as a message: a free
learner looking at a Level 5, Basic-tier section was told only "Requires Level
5", so the honest reading was "earn this and it's yours". It was not — there
was a subscription behind it that the message never mentioned, and they would
only find out after doing all the work.
"""

import os
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from flask import session  # noqa: E402
from app import app, check_section_access, SECTION_REQUIREMENTS  # noqa: E402


def access(section_id, **overrides):
    """Ask the gate what it would say, for a made-up learner."""
    progress = {
        "xp": 0, "level": 1, "subscription_tier": "free",
        "is_developer": False, "monk_mode": False, "full_unlock": False,
        "alphabet_completed": True, "sections_unlocked": [], "sections_visited": [],
    }
    progress.update(overrides)
    with app.test_request_context():
        session["user_progress"] = progress
        return check_section_access(section_id)


# 'sentences' is Level 5 + Basic — both gates apply, which is the whole point.
LEVEL_AND_TIER = "sentences"


def test_the_section_is_still_gated_by_both_things():
    """Guards the fixture above: if someone re-levels this section the tests
    below would pass for the wrong reason."""
    requirements = SECTION_REQUIREMENTS[LEVEL_AND_TIER]
    assert requirements["level"] > 1 and requirements["tier"] != "free"


def test_a_free_learner_is_told_about_the_payment_not_just_the_level():
    allowed, message = access(LEVEL_AND_TIER)
    assert not allowed
    assert "Level 5" in message
    assert "Thai Reader" in message, f"the paywall is still hidden: {message!r}"
    assert "9.99" in message


def test_a_subscriber_below_the_level_is_told_only_the_level():
    """Basic already paid — quoting them a price they have settled would be
    nonsense."""
    allowed, message = access(LEVEL_AND_TIER, subscription_tier="basic")
    assert not allowed
    assert "Level 5" in message
    assert "Thai Reader" not in message


def test_a_monk_below_the_level_is_never_quoted_a_price():
    """Monk Mode waives payment entirely, so a monk owes only the level."""
    allowed, message = access(LEVEL_AND_TIER, monk_mode=True)
    assert not allowed
    assert "Level 5" in message
    assert "£" not in message


def test_the_payment_message_still_stands_alone_at_the_right_level():
    """Level met, tier not — gate 3, unchanged behaviour."""
    allowed, message = access(LEVEL_AND_TIER, level=5)
    assert not allowed
    assert "Thai Reader" in message


def test_a_paid_up_learner_at_the_right_level_gets_in():
    allowed, _ = access(LEVEL_AND_TIER, level=5, subscription_tier="basic")
    assert allowed
