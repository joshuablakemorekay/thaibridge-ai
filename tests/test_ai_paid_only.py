"""The AI is for paying plans only (decided with Josh, 2026-11-21).

Every AI reply is paid for out of Josh's own pocket. Before this, a signed-out
visitor got 5 tutor messages and 5 Dhamma questions a day, counted in a cookie
that clearing cookies reset, and three unused endpoints reached the AI with no
plan check at all. These tests pin all three holes shut. None of them reaches
the real API: an AI call here would itself be the bug.
"""
import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as appmod  # noqa: E402
from app import app  # noqa: E402


class FakeAgent:
    model = "claude-test"

    def __init__(self):
        self.calls = 0

    def chat(self, **kwargs):
        self.calls += 1
        return {"success": True, "response": "stubbed", "mode": kwargs.get("mode"),
                "tokens_used": {"input": 1, "output": 1}}


@pytest.fixture
def agent(monkeypatch):
    fake = FakeAgent()
    monkeypatch.setattr(appmod, "ai_agent", fake)
    return fake


def send(client, mode="tutor"):
    return client.post("/api/ai/chat", json={"message": "hello", "mode": mode}).get_json()


@pytest.mark.parametrize("mode", ["tutor", "buddhist"])
def test_a_signed_out_visitor_gets_no_ai(agent, mode):
    body = send(app.test_client(), mode)
    assert body["gate"] == "plan_required"
    assert body["signed_in"] is False
    assert "sign in" in body["message"].lower()
    assert agent.calls == 0


def test_a_session_that_claims_pro_is_not_an_account(agent, make_client):
    """The tier in the session is just a cookie. Without an account behind it,
    it buys nothing."""
    client = make_client(subscription_tier="pro", is_developer=False)
    assert send(client)["gate"] == "plan_required"
    assert agent.calls == 0


@pytest.mark.parametrize("mode", ["tutor", "buddhist"])
def test_a_free_account_gets_no_ai(agent, ai_client, mode):
    body = send(ai_client("free"), mode)
    assert body["gate"] == "plan_required"
    assert body["signed_in"] is True
    assert agent.calls == 0


def test_the_refusal_is_recorded_for_the_conversion_question(agent, ai_client):
    """It costs nothing, but "do people who hit this wall subscribe?" needs it."""
    client = ai_client("free")
    send(client)
    with app.app_context():
        rows = appmod.AiUsage.query.filter_by(user_id=client.user_id).all()
    assert [r.outcome for r in rows] == ["blocked_plan"]


@pytest.mark.parametrize("tier", ["basic", "pro"])
def test_paying_plans_get_an_answer(agent, ai_client, tier):
    assert send(ai_client(tier))["success"] is True
    assert agent.calls == 1


def test_the_chat_page_tells_a_free_visitor_up_front(agent):
    with app.test_request_context():
        status = appmod.ai_limits_status()
    assert status["plan_required"] is True and status["signed_in"] is False


@pytest.mark.parametrize("path", ["/api/ai/hint", "/api/ai/explain", "/api/ai/generate"])
def test_the_unguarded_endpoints_are_gone(agent, path):
    r = app.test_client().post(path, json={"question": "q", "topic": "t"})
    assert r.status_code == 404
