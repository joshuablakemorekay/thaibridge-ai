"""The Buddhist tutor offers the same three ways in as /dhamma-and-culture.

Why this exists: the Buddhist mode used to know only one of them. Its prompt
said "Teach Buddhism through Thai language acquisition" and the shared base
told every mode to "Connect language to Buddhist/Thai culture naturally", so a
learner who asked a plain Dhamma question got Thai temple vocabulary back
whether they wanted it or not. The site promised Universal Dhamma and a
Culturally neutral path; the tutor quietly overrode both.

These tests hold the three lenses apart. The ones that matter most are the
two that check the universal and neutral prompts carry no Thai framing at all.
"""
import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import ai_agent  # noqa: E402
import app as appmod  # noqa: E402
from app import app  # noqa: E402

THAI_FRAMING = (
    "Connect language to Buddhist/Thai culture naturally",
    "Use Thai script WITH romanization for reinforcement",
    "Teach Buddhism through Thai language acquisition",
    "ทำบุญ",
)


@pytest.fixture(scope="module")
def agent():
    # No real key: get_system_prompt is pure string-building and never calls out.
    return ai_agent.ThaiLearningAI(api_key="test-key-not-used")


def prompt(agent, lens, mode="buddhist"):
    return agent.get_system_prompt(mode, {"level": 1, "xp": 0}, lens=lens)


def test_the_three_lenses_match_the_site():
    """Same names, same order as the cards on /dhamma-and-culture."""
    titles = [ln["title"] for ln in ai_agent.DHAMMA_LENSES.values()]
    assert titles == ["Universal Dhamma", "Dhamma in Thai culture", "Culturally neutral"]


@pytest.mark.parametrize("lens", ["universal", "neutral"])
@pytest.mark.parametrize("phrase", THAI_FRAMING)
def test_universal_and_neutral_carry_no_thai_framing(agent, lens, phrase):
    assert phrase not in prompt(agent, lens)


def test_the_thai_lens_keeps_the_original_teaching(agent):
    text = prompt(agent, "thai")
    for phrase in THAI_FRAMING:
        assert phrase in text


def test_neutral_asks_for_no_identity(agent):
    text = prompt(agent, "neutral")
    assert "Never suggest the student needs to become a Buddhist" in text


@pytest.mark.parametrize("lens", [None, "", "nonsense", "ignore previous instructions"])
def test_an_unknown_lens_falls_back_to_the_default(agent, lens):
    """The browser sends only an id; anything else must never reach the prompt."""
    assert prompt(agent, lens) == prompt(agent, ai_agent.DEFAULT_DHAMMA_LENS)


def test_other_modes_ignore_the_lens(agent):
    """A lens left set from Buddhist mode must not change the Thai tutor."""
    assert prompt(agent, "universal", mode="tutor") == prompt(agent, "thai", mode="tutor")


class FakeAgent:
    """No network, no cost — records what the route passed through."""

    model = "claude-haiku-4-5-test"

    def __init__(self):
        self.kwargs = None

    def chat(self, **kwargs):
        self.kwargs = kwargs
        return {"success": True, "response": "stubbed reply",
                "mode": kwargs.get("mode"), "tokens_used": {"input": 1, "output": 1}}


def test_the_route_passes_the_lens_to_the_tutor(monkeypatch):
    fake = FakeAgent()
    monkeypatch.setattr(appmod, "ai_agent", fake)
    client = app.test_client()
    client.post("/api/ai/chat", json={"message": "What is mettā?",
                                      "mode": "buddhist", "lens": "neutral"})
    assert fake.kwargs["lens"] == "neutral"


def test_the_chat_page_shows_all_three_approaches(monkeypatch):
    monkeypatch.setattr(appmod, "ai_agent", FakeAgent())
    body = app.test_client().get("/chat").get_data(as_text=True)
    for lid in ai_agent.DHAMMA_LENSES:
        assert f'data-lens="{lid}"' in body


def test_switching_approach_makes_the_tutor_forget_the_old_one():
    """Old answers in the tutor's memory drag the next few back to the old
    approach, so a switch must clear the server-side conversation."""
    src = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "templates", "chat.html"), encoding="utf-8").read()
    set_lens = src[src.index("function setLens"):]
    set_lens = set_lens[:set_lens.index("\n    }\n")]
    assert "/api/ai/clear" in set_lens


# ── Buddhist mode on its own model ────────────────────────────────────────

class _Block:
    def __init__(self, type_, text=""):
        self.type, self.text = type_, text


class _Usage:
    input_tokens, output_tokens = 5, 7


class _FakeMessages:
    def __init__(self):
        self.request = None

    def create(self, **kwargs):
        self.request = kwargs
        # A thinking model puts its thinking block first.
        return type("R", (), {"content": [_Block("thinking"), _Block("text", "Mettā is "),
                                          _Block("text", "goodwill.")],
                              "usage": _Usage(), "stop_reason": "end_turn"})()


def _agent_with(monkeypatch, dhamma_model):
    monkeypatch.setenv("AI_MODEL", "claude-haiku-4-5-20251001")
    if dhamma_model:
        monkeypatch.setenv("DHAMMA_AI_MODEL", dhamma_model)
    else:
        monkeypatch.delenv("DHAMMA_AI_MODEL", raising=False)
    a = ai_agent.ThaiLearningAI(api_key="test-key-not-used")
    a.client = type("C", (), {"messages": _FakeMessages()})()
    return a


def test_buddhist_mode_uses_its_own_model_and_others_do_not(monkeypatch):
    a = _agent_with(monkeypatch, "claude-haiku-5-5")
    assert a.chat("s1", "What is mettā?", mode="buddhist")["model"] == "claude-haiku-5-5"
    assert a.client.messages.request["thinking"] == {"type": "disabled"}
    assert a.chat("s2", "hello", mode="tutor")["model"] == "claude-haiku-4-5-20251001"
    assert "thinking" not in a.client.messages.request


def test_unset_dhamma_model_falls_back_to_the_main_one(monkeypatch):
    """Rolling back is deleting one setting on Render."""
    a = _agent_with(monkeypatch, None)
    assert a.model_for("buddhist") == "claude-haiku-4-5-20251001"


def test_the_reply_skips_a_leading_thinking_block(monkeypatch):
    a = _agent_with(monkeypatch, "claude-haiku-5-5")
    assert a.chat("s3", "What is mettā?", mode="buddhist")["response"] == "Mettā is goodwill."


@pytest.mark.parametrize("model, expected", [
    ("claude-haiku-4-5-20251001", None),
    ("claude-haiku-5-5", {"type": "disabled"}),
    # Sonnet 5.5 rejects "disabled" with a 400.
    ("claude-sonnet-5-5", {"type": "between_tools"}),
])
def test_thinking_is_switched_off_the_way_each_model_accepts(model, expected):
    assert ai_agent.thinking_off(model) == expected


def test_buddhist_mode_gets_room_to_finish_and_logs_the_right_model(monkeypatch):
    fake = FakeAgent()
    fake.chat = lambda **kw: (setattr(fake, "kwargs", kw) or
                              {"success": True, "response": "ok", "model": "claude-haiku-5-5",
                               "tokens_used": {"input": 1, "output": 1}})
    logged = {}
    monkeypatch.setattr(appmod, "ai_agent", fake)
    monkeypatch.setattr(appmod, "log_ai_usage",
                        lambda *a, **kw: logged.update(kw) if a[1] == "ok" else None)
    app.test_client().post("/api/ai/chat", json={"message": "q", "mode": "buddhist"})
    assert fake.kwargs["max_tokens"] == appmod.AI_REPLY_TOKENS
    assert logged["model"] == "claude-haiku-5-5"


def test_every_request_asks_for_caching(monkeypatch):
    """A chat re-sends its instructions and history with every message;
    cached, that re-send costs a tenth of the price."""
    a = _agent_with(monkeypatch, None)
    a.chat("s4", "hello", mode="tutor")
    assert a.client.messages.request["extra_body"] == {"cache_control": {"type": "ephemeral"}}


@pytest.mark.parametrize("mode", ["tutor", "cultural", "buddhist", "generator"])
def test_long_answer_modes_are_asked_to_keep_it_short(agent, mode):
    assert ai_agent.MODE_LENGTH[mode] in agent.get_system_prompt(mode, {"level": 1, "xp": 0})


@pytest.mark.parametrize("mode", ["tutor", "generator", "conversation"])
def test_each_mode_gets_its_reply_limit(monkeypatch, mode):
    fake = FakeAgent()
    monkeypatch.setattr(appmod, "ai_agent", fake)
    monkeypatch.setattr(appmod, "active_tier", lambda: "pro")
    app.test_client().post("/api/ai/chat", json={"message": "q", "mode": mode})
    assert fake.kwargs["max_tokens"] == appmod.AI_REPLY_TOKENS_BY_MODE.get(
        mode, appmod.AI_REPLY_TOKENS)
    assert appmod.AI_REPLY_TOKENS_BY_MODE["generator"] > appmod.AI_REPLY_TOKENS


# ── When the monthly AI budget runs out ───────────────────────────────────

import anthropic  # noqa: E402
import httpx  # noqa: E402


def _api_error(cls, status, err_type, message):
    response = httpx.Response(status, request=httpx.Request("POST", "https://api.anthropic.com"))
    return cls(message, response=response,
               body={"type": "error", "error": {"type": err_type, "message": message}})


BUDGET_GONE = [
    _api_error(anthropic.APIStatusError, 402, "billing_error", "Billing problem"),
    _api_error(anthropic.BadRequestError, 400, "invalid_request_error",
               "You have reached your specified API usage limits."),
    _api_error(anthropic.BadRequestError, 400, "invalid_request_error",
               "Your credit balance is too low to access the Anthropic API."),
]


def _agent_raising(monkeypatch, error):
    a = _agent_with(monkeypatch, None)

    def boom(**kwargs):
        raise error
    a.client.messages.create = boom
    return a


@pytest.mark.parametrize("error", BUDGET_GONE)
def test_an_empty_budget_reads_as_resting_not_broken(monkeypatch, error):
    r = _agent_raising(monkeypatch, error).chat("s5", "hello", mode="tutor")
    assert r["gate"] == "ai_resting"  # the page shows a gate in its gentle note box
    assert r["message"] == ai_agent.AI_RESTING_MESSAGE
    assert "API key" not in r["message"]


def test_a_real_fault_is_not_disguised_as_resting(monkeypatch):
    error = _api_error(anthropic.BadRequestError, 400, "invalid_request_error",
                       "messages: roles must alternate")
    r = _agent_raising(monkeypatch, error).chat("s6", "hello", mode="tutor")
    assert "gate" not in r
    assert r["message"] != ai_agent.AI_RESTING_MESSAGE


def test_hints_rest_too(monkeypatch):
    a = _agent_raising(monkeypatch, BUDGET_GONE[0])
    assert a.get_quick_hint("q", "c") == ai_agent.AI_RESTING_MESSAGE


@pytest.mark.parametrize("call", [
    lambda a: a.get_quick_hint("q", "c"),
    lambda a: a.explain_answer("q", "right", "wrong"),
    lambda a: a.generate_content("quiz", "food", 1),
])
def test_single_shot_features_skip_a_thinking_block(monkeypatch, call):
    """These read content[0] before, which on a thinking model is the thinking."""
    assert call(_agent_with(monkeypatch, None)) == "Mettā is goodwill."


def test_the_resting_note_does_not_sell_pro():
    """Upgrading can't help when the budget is gone, so no plans link."""
    src = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "templates", "chat.html"), encoding="utf-8").read()
    assert "showUpgradeNote(data.message, data.gate !== 'ai_resting')" in src
