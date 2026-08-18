"""Tests for the daily ceiling on drill XP (added 2026-08-18).

/api/check_answer is sent both the answer and the correct answer, and compares
them to each other — the drills are generated in the browser, so the page holds
the answer already. It therefore cannot tell a learner from a script, and no
amount of validation fixes that while the drills stay client-side.

So the reward is bounded rather than the honesty proved. These tests pin the
bound, which matters more than it used to: XP now earns a free paid section, so
farming it is farming access, not just a number.
"""

import os
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, DRILL_XP_DAILY_CAP, POINT_REWARDS  # noqa: E402


@pytest.fixture
def client():
    return app.test_client()


def answer(client, correctly=True):
    return client.post("/api/check_answer", json={
        "answer": "a", "correct": "a" if correctly else "b",
    }).get_json()


def xp(client):
    return client.get("/api/user_stats").get_json()["xp"]


def test_xp_is_paid_below_the_cap(client):
    result = answer(client)
    assert result["xp_earned"] == POINT_REWARDS["quiz_correct"]
    assert not result["daily_cap_reached"]


def test_xp_stops_exactly_at_the_cap(client):
    per_answer = POINT_REWARDS["quiz_correct"]
    for _ in range(DRILL_XP_DAILY_CAP // per_answer):
        answer(client)

    assert xp(client) == DRILL_XP_DAILY_CAP

    beyond = answer(client)
    assert beyond["xp_earned"] == 0
    assert beyond["daily_cap_reached"]
    assert xp(client) == DRILL_XP_DAILY_CAP, "the cap leaked"


def test_a_capped_learner_can_still_practise(client):
    """The cap is on the reward, not the drill. Someone revising the night
    before an exam must not be locked out of their own practice."""
    for _ in range(DRILL_XP_DAILY_CAP // POINT_REWARDS["quiz_correct"] + 3):
        answer(client)

    result = answer(client)
    assert result["correct"] is True, "marking stopped working past the cap"
    assert result["xp_earned"] == 0


def test_a_wrong_answer_never_pays(client):
    before = xp(client)
    result = answer(client, correctly=False)
    assert result["xp_earned"] == 0
    assert xp(client) == before


def test_the_allowance_comes_back_the_next_day(client):
    for _ in range(DRILL_XP_DAILY_CAP // POINT_REWARDS["quiz_correct"] + 1):
        answer(client)
    assert xp(client) == DRILL_XP_DAILY_CAP

    with client.session_transaction() as session_data:
        progress = session_data["user_progress"]
        progress["drill_xp_date"] = "2020-01-01"      # yesterday, as far as it knows
        session_data["user_progress"] = progress

    result = answer(client)
    assert result["xp_earned"] == POINT_REWARDS["quiz_correct"]


def test_the_cap_counts_xp_paid_not_answers_given(client):
    """A points multiplier must not buy a bigger ceiling: a Pro subscriber's 3x
    would otherwise be three times the daily XP, not three times per answer."""
    client.get("/api/user_stats")          # let the app lay down a full progress dict
    with client.session_transaction() as session_data:
        progress = session_data["user_progress"]
        progress["subscription_tier"] = "pro"
        session_data["user_progress"] = progress

    for _ in range(DRILL_XP_DAILY_CAP):        # far more than enough
        result = answer(client)
        if result["daily_cap_reached"]:
            break

    assert xp(client) <= DRILL_XP_DAILY_CAP + POINT_REWARDS["quiz_correct"] * 3
