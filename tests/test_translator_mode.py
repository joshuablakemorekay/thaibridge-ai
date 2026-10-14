"""The Translator is a Pro chat mode.

It is locked for Free and Basic by the same rule as Conversation and Culture:
any mode not in FREE_AI_ALLOWED_MODES. Nothing in the gate names it, so these
tests pin that it stays off the free list and that Pro gets through, rather
than trusting a set nobody re-reads. No test here reaches the real API.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import ai_agent  # noqa: E402
import app as appmod  # noqa: E402
from app import app  # noqa: E402


@pytest.fixture(autouse=True)
def quiet(monkeypatch):
    monkeypatch.setattr(appmod, 'log_ai_usage', lambda *a, **kw: None)


def test_translator_is_not_on_the_free_list():
    assert 'translator' not in appmod.FREE_AI_ALLOWED_MODES


@pytest.mark.parametrize('tier', ['free', 'basic'])
def test_free_and_basic_are_shown_the_lock(tier):
    with app.test_request_context('/api/ai/chat'):
        blocked = appmod._ai_chat_gate(tier, 'translator')
        body = blocked.get_json()
    assert body['gate'] == 'mode_locked'
    assert 'Translator' in body['message']


def test_pro_gets_through():
    with app.test_request_context('/api/ai/chat'):
        assert appmod._ai_chat_gate('pro', 'translator') is None


def test_the_chat_page_offers_the_mode_and_its_caution():
    page = app.test_client().get('/chat').get_data(as_text=True)
    assert 'data-mode="translator"' in page
    assert 'id="translator-note"' in page
    assert 'may not be perfect' in page


def test_the_prompt_is_the_translator_not_the_tutor_fallback():
    """An unknown mode silently falls back to the tutor prompt."""
    agent = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    prompt = agent.get_system_prompt('translator', {})
    assert 'MODE: TRANSLATOR' in prompt
    assert 'MODE: INTELLIGENT TUTORING SYSTEM' not in prompt
