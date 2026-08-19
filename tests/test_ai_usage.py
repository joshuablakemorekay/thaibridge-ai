"""
Tests for AI usage logging (added 2026-08-17).

ai_agent returns token counts on every call and, until this table existed,
app.py discarded them — so the spend, the traffic, and whether cap-hitters
subscribe were all unanswerable. This is also the only gap of its kind that
cannot be filled in later: a month that was not recorded is gone.

The AI agent is stubbed throughout. These tests must never reach the real API —
a test suite that quietly spends money is its own kind of bug, and one of
today's already did.

Run with:  pytest tests/test_ai_usage.py -v
"""

import os
import uuid
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as appmod  # noqa: E402
from app import app, db, AiUsage, User, utcnow  # noqa: E402

PASSWORD = "UsagePass123"


class FakeAgent:
    """Stands in for the real agent: same shape, no network, no cost."""

    model = "claude-haiku-4-5-test"

    def __init__(self, success=True, tokens=(120, 340)):
        self.success, self.tokens = success, tokens
        self.calls = 0

    def chat(self, **kwargs):
        self.calls += 1
        if not self.success:
            return {"success": False, "error_type": "APIError"}
        return {
            "success": True,
            "response": "stubbed reply",
            "mode": kwargs.get("mode"),
            "tokens_used": {"input": self.tokens[0], "output": self.tokens[1]},
        }


@pytest.fixture
def agent(monkeypatch):
    fake = FakeAgent()
    monkeypatch.setattr(appmod, "ai_agent", fake)
    return fake


@pytest.fixture(autouse=True)
def clean_usage():
    """Each test starts with an empty table and leaves one behind."""
    with app.app_context():
        AiUsage.query.delete()
        db.session.commit()
    yield
    with app.app_context():
        AiUsage.query.delete()
        db.session.commit()


def rows():
    with app.app_context():
        return AiUsage.query.order_by(AiUsage.id).all()


def send(client, message="hello", mode="tutor"):
    return client.post("/api/ai/chat", json={"message": message, "mode": mode})


# ---------------------------------------------------------------------------
# The spend
# ---------------------------------------------------------------------------

def test_a_successful_call_records_its_tokens(agent):
    send(app.test_client())
    r = rows()
    assert len(r) == 1
    assert r[0].outcome == "ok"
    assert r[0].input_tokens == 120
    assert r[0].output_tokens == 340
    assert r[0].model == "claude-haiku-4-5-test"
    assert r[0].feature == "chat"
    assert r[0].mode == "tutor"


def test_cost_can_be_worked_out_from_what_is_stored(agent):
    """The point of storing tokens and the model rather than a cash figure:
    the sum is done at read time, so old rows stay correct when prices move."""
    c = app.test_client()
    for _ in range(3):
        send(c)
    with app.app_context():
        total_in = db.session.query(db.func.sum(AiUsage.input_tokens)).scalar()
        total_out = db.session.query(db.func.sum(AiUsage.output_tokens)).scalar()
    assert (total_in, total_out) == (360, 1020)
    # Haiku 4.5 list rates, applied now rather than baked into the rows.
    usd = (total_in * 1.00 + total_out * 5.00) / 1_000_000
    assert 0 < usd < 0.01


# ---------------------------------------------------------------------------
# The traffic
# ---------------------------------------------------------------------------

def test_a_signed_out_visitor_is_counted_without_being_identified(agent):
    send(app.test_client())
    r = rows()[0]
    assert r.user_id is None
    assert r.session_key, "signed-out use must still be groupable per visitor"


def test_a_signed_in_user_is_attributed(agent):
    username = f"u{uuid.uuid4().hex[:10]}"
    c = app.test_client()
    c.post("/signup", json={"username": username, "email": f"{username}@example.com",
                            "password": PASSWORD, "confirm_password": PASSWORD})
    try:
        send(c)
        with app.app_context():
            user = User.query.filter_by(username=username).first()
            row = AiUsage.query.first()
            assert row.user_id == user.id
    finally:
        with app.app_context():
            u = User.query.filter_by(username=username).first()
            if u:
                db.session.delete(u)
                db.session.commit()


# ---------------------------------------------------------------------------
# The conversion question
# ---------------------------------------------------------------------------

def test_a_blocked_mode_is_recorded_with_no_cost(agent):
    """Blocked requests are the conversion data. Logging only successes would
    lose the answer to 'do people who hit a wall upgrade?'"""
    send(app.test_client(), mode="cultural")      # Pro-only
    r = rows()
    assert len(r) == 1
    assert r[0].outcome == "blocked_mode"
    assert (r[0].input_tokens, r[0].output_tokens) == (0, 0)
    assert agent.calls == 0, "a blocked request must never reach the model"


def test_hitting_the_daily_cap_is_recorded(agent, monkeypatch):
    monkeypatch.setattr(appmod, "FREE_AI_DAILY_LIMIT", 2)
    c = app.test_client()
    for _ in range(4):
        send(c)
    outcomes = [r.outcome for r in rows()]
    assert outcomes.count("ok") == 2
    assert outcomes.count("blocked_cap") == 2


def test_the_tier_is_recorded_as_it_was_at_the_time(agent):
    send(app.test_client())
    assert rows()[0].tier == "free"


# ---------------------------------------------------------------------------
# Reliability
# ---------------------------------------------------------------------------

def test_a_failed_call_is_recorded(monkeypatch):
    """The agent catches its own API errors and returns them, so no exception
    reaches the route. Without an explicit branch these vanish from the record."""
    monkeypatch.setattr(appmod, "ai_agent", FakeAgent(success=False))
    send(app.test_client())
    r = rows()
    assert len(r) == 1 and r[0].outcome == "error"


# ---------------------------------------------------------------------------
# The two rules that matter most
# ---------------------------------------------------------------------------

def test_nothing_the_user_typed_is_stored(agent):
    """No question, no answer. Someone asking about their own practice in the
    Dhamma mode should not have it filed away."""
    secret = "please never store this sentence"
    send(app.test_client(), message=secret)
    row = rows()[0]
    stored = " ".join(str(getattr(row, c.name)) for c in AiUsage.__table__.columns)
    assert secret not in stored
    assert "stubbed reply" not in stored


def test_a_database_failure_never_breaks_the_reply(agent, monkeypatch):
    """The reply has already been generated and paid for by this point. Losing a
    row is cheap; turning a billed answer into a 500 is not.

    Breaks the database commit rather than replacing log_ai_usage wholesale. The
    first version of this test swapped out the function itself, which sailed past
    the very try/except it was meant to exercise and 'failed' against a scenario
    that cannot happen.
    """
    def explode(*a, **k):
        raise RuntimeError("database on fire")
    monkeypatch.setattr(db.session, "commit", explode)

    response = send(app.test_client())
    assert response.status_code == 200
    assert response.get_json()["success"] is True


# ---------------------------------------------------------------------------
# The id that makes per-visitor counting possible
# ---------------------------------------------------------------------------

def test_a_visitor_keeps_the_same_session_id_across_messages(agent):
    """Found while building this: the id was read with a default and never
    stored, so every request invented a new one. That broke usage grouping — and
    silently broke conversation memory too, because ai_agent keys its history on
    the same value, so every message began a fresh conversation.
    """
    c = app.test_client()
    send(c, message="first")
    send(c, message="second")
    keys = {r.session_key for r in rows()}
    assert len(keys) == 1, f"same visitor produced {len(keys)} different ids"
    assert None not in keys


def test_two_visitors_get_different_session_ids(agent):
    send(app.test_client(), message="a")
    send(app.test_client(), message="b")
    keys = {r.session_key for r in rows()}
    assert len(keys) == 2, "separate visitors must not share an id"


# ---------------------------------------------------------------------------
# The Pro fair-use ceiling
# ---------------------------------------------------------------------------

@pytest.fixture
def pro_account():
    """A signed-in Pro subscriber. Yields (client, user_id)."""
    username = f"p{uuid.uuid4().hex[:10]}"
    client = app.test_client()
    client.post("/signup", json={"username": username, "email": f"{username}@example.com",
                                 "password": PASSWORD, "confirm_password": PASSWORD})
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        user.subscription_tier = "pro"
        user.subscription_status = "active"
        db.session.commit()
        user_id = user.id
    try:
        yield client, user_id
    finally:
        with app.app_context():
            AiUsage.query.filter_by(user_id=user_id).delete()
            u = db.session.get(User, user_id)
            if u:
                db.session.delete(u)
            db.session.commit()


def seed_usage(user_id, n, outcome="ok", days_ago=0):
    """Put n rows straight into the table, bypassing the route."""
    from datetime import timedelta
    when = utcnow() - timedelta(days=days_ago)
    with app.app_context():
        for _ in range(n):
            db.session.add(AiUsage(user_id=user_id, feature="chat", mode="tutor",
                                   outcome=outcome, input_tokens=10, output_tokens=10,
                                   created_at=when, tier="pro"))
        db.session.commit()


def test_a_pro_user_under_the_ceiling_gets_through(agent, pro_account):
    client, user_id = pro_account
    seed_usage(user_id, appmod.PRO_FAIR_USE_DAILY - 1)
    assert send(client).get_json()["success"] is True


def test_a_pro_user_at_the_ceiling_is_stopped(agent, pro_account):
    client, user_id = pro_account
    seed_usage(user_id, appmod.PRO_FAIR_USE_DAILY)
    body = send(client).get_json()
    assert body["success"] is False
    assert body["gate"] == "fair_use"
    assert agent.calls == 0, "a blocked request must never reach the model"


def test_hitting_the_ceiling_is_recorded(agent, pro_account):
    client, user_id = pro_account
    seed_usage(user_id, appmod.PRO_FAIR_USE_DAILY)
    send(client)
    with app.app_context():
        blocked = AiUsage.query.filter_by(user_id=user_id,
                                          outcome="blocked_fairuse").count()
    assert blocked == 1


def test_only_successful_calls_count_towards_the_ceiling(agent, pro_account):
    """Nobody should lose allowance to a request that failed or was blocked."""
    client, user_id = pro_account
    seed_usage(user_id, appmod.PRO_FAIR_USE_DAILY, outcome="error")
    assert send(client).get_json()["success"] is True


def test_yesterdays_messages_do_not_count(agent, pro_account):
    """The ceiling is per day. Without the date filter it would be a lifetime
    cap, and a long-standing subscriber would eventually be locked out for good."""
    client, user_id = pro_account
    seed_usage(user_id, appmod.PRO_FAIR_USE_DAILY, days_ago=1)
    assert send(client).get_json()["success"] is True


def test_another_users_messages_do_not_count(agent, pro_account):
    client, user_id = pro_account
    other = f"o{uuid.uuid4().hex[:10]}"
    c2 = app.test_client()
    c2.post("/signup", json={"username": other, "email": f"{other}@example.com",
                             "password": PASSWORD, "confirm_password": PASSWORD})
    with app.app_context():
        other_id = User.query.filter_by(username=other).first().id
    try:
        seed_usage(other_id, appmod.PRO_FAIR_USE_DAILY)
        assert send(client).get_json()["success"] is True
    finally:
        with app.app_context():
            AiUsage.query.filter_by(user_id=other_id).delete()
            u = db.session.get(User, other_id)
            if u:
                db.session.delete(u)
            db.session.commit()


def test_the_ceiling_is_far_above_the_free_allowance(agent):
    """A sanity check on the number itself: if these ever converge, Pro has
    stopped being worth paying for."""
    assert appmod.PRO_FAIR_USE_DAILY >= appmod.FREE_AI_DAILY_LIMIT * 5
