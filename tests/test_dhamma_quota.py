"""The Dhamma has its own daily AI allowance, separate from the Thai tutor's.

Why this exists at all: the site's position is that the teaching is free, and
that charging for the follow-up question would be selling the Dhamma. But tutor
and Dhamma used to spend the same 15 messages, so someone who drilled Thai
vocabulary all morning and then asked about the precepts was told to come back
tomorrow or upgrade. The paywall was never in front of the teaching — it had
just grown a side door.

These tests hold that door shut. The one that matters most is
`test_the_tutor_cannot_eat_the_dhamma_allowance`: everything else is detail.
"""
import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as appmod  # noqa: E402
from app import app  # noqa: E402


class FakeAgent:
    """No network, no cost — the suite must never reach the real API."""

    model = "claude-haiku-4-5-test"

    def __init__(self):
        self.calls = 0

    def chat(self, **kwargs):
        self.calls += 1
        return {
            "success": True,
            "response": "stubbed reply",
            "mode": kwargs.get("mode"),
            "tokens_used": {"input": 10, "output": 20},
        }


@pytest.fixture
def agent(monkeypatch):
    fake = FakeAgent()
    monkeypatch.setattr(appmod, "ai_agent", fake)
    return fake


def send(client, mode="tutor", message="hello"):
    return client.post("/api/ai/chat", json={"message": message, "mode": mode})


class TestThePoolsAreSeparate:
    def test_the_tutor_cannot_eat_the_dhamma_allowance(self, agent, monkeypatch):
        """The whole point. Spend every tutor message, then ask a Dhamma
        question — it must be answered, not refused."""
        monkeypatch.setattr(appmod, "FREE_AI_DAILY_LIMIT", 2)
        client = app.test_client()

        for _ in range(3):
            send(client, mode="tutor")          # 2 answered, 1 refused

        response = send(client, mode="buddhist").get_json()
        assert response["success"] is True, (
            "a Dhamma question was refused because the Thai tutor had spent the "
            "day's messages — this is the bug the split exists to prevent")

    def test_the_dhamma_cannot_eat_the_tutor_allowance(self, agent, monkeypatch):
        # The mirror. The pools are independent in both directions, otherwise
        # the fix just moves the problem.
        monkeypatch.setattr(appmod, "FREE_DHAMMA_DAILY_LIMIT", 1)
        client = app.test_client()

        for _ in range(3):
            send(client, mode="buddhist")

        assert send(client, mode="tutor").get_json()["success"] is True

    def test_the_dhamma_pool_still_has_a_ceiling(self, agent, monkeypatch):
        """Free does not mean unmetered. The cap is the honest cost of running
        the model; it is the UPSELL that has no place here, not the limit."""
        monkeypatch.setattr(appmod, "FREE_DHAMMA_DAILY_LIMIT", 2)
        client = app.test_client()

        outcomes = [send(client, mode="buddhist").get_json()["success"]
                    for _ in range(3)]
        assert outcomes == [True, True, False]

    def test_the_tutor_allowance_was_not_reduced_to_pay_for_this(self):
        """The Dhamma pool is added on top, not carved out. Nobody should lose
        something so the site can keep a promise it had already made."""
        assert appmod.FREE_AI_DAILY_LIMIT == 15


class TestWhatTheLearnerIsTold:
    def test_running_out_of_dhamma_questions_does_not_sell_anything(
            self, agent, monkeypatch):
        """An upsell here would be the site charging for the Dhamma in all but
        name. The refusal may explain the cost; it may not ask for money."""
        monkeypatch.setattr(appmod, "FREE_DHAMMA_DAILY_LIMIT", 1)
        client = app.test_client()
        send(client, mode="buddhist")

        body = send(client, mode="buddhist").get_json()
        assert body["success"] is False
        assert body["pool"] == "dhamma"
        message = body["message"].lower()
        assert "upgrade" not in message
        assert "pro" not in message.split()

    def test_running_out_of_tutor_messages_points_at_the_dhamma_first(
            self, agent, monkeypatch):
        """Someone with Dhamma questions still in hand should be told so before
        being shown a price — otherwise the nudge reads as a trick."""
        monkeypatch.setattr(appmod, "FREE_AI_DAILY_LIMIT", 1)
        client = app.test_client()
        send(client, mode="tutor")

        message = send(client, mode="tutor").get_json()["message"]
        assert "Dhamma" in message
        assert message.index("Dhamma") < message.index("Pro")


class TestTheCountersThemselves:
    def test_each_pool_counts_in_its_own_session_key(self, agent):
        client = app.test_client()
        send(client, mode="tutor")
        send(client, mode="buddhist")

        with client.session_transaction() as session:
            usage = session["ai_usage"]
        assert usage["count"] == 1     # tutor
        assert usage["dhamma"] == 1

    def test_a_session_from_before_the_split_still_works(self, agent):
        """An old session has no 'dhamma' key. It must not KeyError, and the
        learner must not lose the tutor tally they have already spent today."""
        client = app.test_client()
        with client.session_transaction() as session:
            session["ai_usage"] = {
                "date": appmod.datetime.now().strftime("%Y-%m-%d"),
                "count": 4,
            }

        assert send(client, mode="buddhist").get_json()["success"] is True
        with client.session_transaction() as session:
            usage = session["ai_usage"]
        assert usage["count"] == 4, "today's tutor tally was reset"
        assert usage["dhamma"] == 1

    def test_the_limits_are_read_from_the_constants_not_a_copy(self, monkeypatch):
        """AI_POOLS stores the constant's NAME, not its value. Storing the
        value made the dict a second source of truth that silently won."""
        monkeypatch.setattr(appmod, "FREE_DHAMMA_DAILY_LIMIT", 99)
        assert appmod.ai_pool_limit("dhamma") == 99


class TestWhatThePageIsToldUpFront:
    def test_the_status_reports_both_pools(self):
        with app.test_request_context():
            status = appmod.ai_limits_status()
        assert status["pools"]["tutor"]["limit"] == appmod.FREE_AI_DAILY_LIMIT
        assert status["pools"]["dhamma"]["limit"] == appmod.FREE_DHAMMA_DAILY_LIMIT

    def test_the_superseded_flat_keys_are_gone(self):
        """The first cut kept daily_limit/used_today/remaining alongside the
        pools, so "nothing but this file has to learn a new shape". That was
        already untrue when it shipped: the only reader, chat.html, moved to
        pools in the same commit. A compatibility shim with nothing to be
        compatible with is just a second way to say the same thing wrong."""
        with app.test_request_context():
            status = appmod.ai_limits_status()
        for dead in ("daily_limit", "used_today", "remaining"):
            assert dead not in status, f"{dead} is superseded by pools"

    def test_the_page_is_told_which_modes_are_dhamma(self):
        """So the hint can follow the mode without hardcoding 'buddhist' in
        JavaScript as well as in Python."""
        with app.test_request_context():
            status = appmod.ai_limits_status()
        assert "buddhist" in status["dhamma_modes"]
