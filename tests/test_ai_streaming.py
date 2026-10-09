"""The tutor's reply can arrive as it is written.

A Sonnet answer takes several seconds; sent in one piece, the chat page sat on
"AI is thinking" for all of it. These tests pin the streamed path: the lines it
sends, that it spends exactly one message from the allowance, and that a
refusal before any text (an empty budget, say) still costs the visitor nothing.
No test here reaches the real API.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import ai_agent  # noqa: E402
import app as appmod  # noqa: E402
from app import app  # noqa: E402

DONE = {'type': 'done', 'success': True, 'response': 'Hello there', 'model': 'claude-sonnet-5-5',
        'stop_reason': 'end_turn',
        'tokens_used': {'input': 4, 'output': 3, 'cache_write': 10, 'cache_read': 20}}


class FakeAgent:
    model = 'claude-sonnet-5-5'

    def __init__(self, failure=None, break_midway=False):
        self.failure, self.break_midway = failure, break_midway

    def model_for(self, mode):
        return self.model

    def start_chat_stream(self, **kwargs):
        if self.failure:
            return None, self.failure

        def events():
            yield {'type': 'text', 'text': 'Hello '}
            if self.break_midway:
                raise ConnectionError('dropped')
            yield {'type': 'text', 'text': 'there'}
            yield DONE
        return events(), None


@pytest.fixture
def logged(monkeypatch):
    calls = []
    monkeypatch.setattr(appmod, 'log_ai_usage', lambda *a, **kw: calls.append((a, kw)))
    return calls


def ask(agent, monkeypatch, mode='tutor'):
    monkeypatch.setattr(appmod, 'ai_agent', agent)
    client = app.test_client()
    r = client.post('/api/ai/chat', json={'message': 'hi', 'mode': mode, 'stream': True})
    return client, r


def lines(response):
    return [json.loads(l) for l in response.get_data(as_text=True).splitlines() if l.strip()]


def test_the_reply_arrives_as_lines(monkeypatch, logged):
    _, r = ask(FakeAgent(), monkeypatch)
    assert r.mimetype == 'application/x-ndjson'
    events = lines(r)
    assert [e['text'] for e in events if e['type'] == 'text'] == ['Hello ', 'there']
    assert events[-1]['type'] == 'done' and 'pools' in events[-1]


def test_one_message_is_spent_and_logged_with_its_cache_tokens(monkeypatch, logged):
    client, r = ask(FakeAgent(), monkeypatch)
    lines(r)  # the stream has to be read for the 'done' line to run
    with client.session_transaction() as s:
        assert s['ai_usage']['count'] == 1
    ok = [kw for a, kw in logged if a[1] == 'ok']
    assert ok and ok[0]['cache_read_tokens'] == 20 and ok[0]['model'] == 'claude-sonnet-5-5'


def test_a_refusal_is_an_ordinary_answer_and_costs_nothing(monkeypatch, logged):
    refused = {'success': False, 'gate': 'ai_resting', 'error_type': 'out_of_budget',
               'message': ai_agent.AI_RESTING_MESSAGE}
    client, r = ask(FakeAgent(failure=refused), monkeypatch)
    assert r.is_json and r.get_json()['gate'] == 'ai_resting'
    with client.session_transaction() as s:
        assert s.get('ai_usage', {}).get('count', 0) == 0


def test_a_dropped_connection_says_so(monkeypatch, logged):
    _, r = ask(FakeAgent(break_midway=True), monkeypatch)
    events = lines(r)
    assert events[0] == {'type': 'text', 'text': 'Hello '}
    assert events[-1]['type'] == 'error'
    assert any(a[1] == 'error' for a, _ in logged)


def test_the_allowance_gates_still_apply(monkeypatch, logged):
    """Streaming must not be a way round the free-tier mode lock."""
    _, r = ask(FakeAgent(), monkeypatch, mode='generator')
    assert r.is_json and r.get_json()['gate'] == 'mode_locked'


# ── The agent's side ──────────────────────────────────────────────────────

class _Stream:
    text_stream = iter(['Mettā ', 'is goodwill.'])

    def get_final_message(self):
        usage = type('U', (), {'input_tokens': 4, 'output_tokens': 5,
                               'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 9})()
        return type('M', (), {'usage': usage, 'stop_reason': 'end_turn'})()


class _Manager:
    def __init__(self, error=None):
        self.error, self.closed = error, False

    def __enter__(self):
        if self.error:
            raise self.error
        return _Stream()

    def __exit__(self, *exc):
        self.closed = True


def _agent(manager):
    a = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    a.client = type('C', (), {'messages': type('M', (), {
        'stream': lambda self, **kw: manager})()})()
    return a


def test_the_agent_streams_and_remembers_the_reply():
    manager = _Manager()
    a = _agent(manager)
    events, failure = a.start_chat_stream('s1', 'What is mettā?', mode='tutor')
    assert failure is None
    out = list(events)
    assert [e['text'] for e in out if e['type'] == 'text'] == ['Mettā ', 'is goodwill.']
    assert out[-1]['tokens_used']['cache_read'] == 9
    assert a.conversations['s1'][-1] == {'role': 'assistant', 'content': 'Mettā is goodwill.'}
    assert manager.closed


def test_a_refused_stream_fails_before_any_text():
    import anthropic
    import httpx
    error = anthropic.APIStatusError(
        'Billing problem', response=httpx.Response(402, request=httpx.Request('POST', 'https://x')),
        body={'type': 'error', 'error': {'type': 'billing_error', 'message': 'Billing problem'}})
    events, failure = _agent(_Manager(error)).start_chat_stream('s2', 'hi', mode='tutor')
    assert events is None and failure['gate'] == 'ai_resting'
