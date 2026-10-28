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


# ── Photos: a menu or sign for the Translator to read ─────────────────────

import base64  # noqa: E402

# Not real images, only the right first bytes: photo_block checks the
# signature and the size, and never decodes the picture itself.
JPEG = base64.b64encode(b'\xff\xd8\xff\xe0' + b'\x00' * 32).decode()
PNG = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 32).decode()
WEBP = base64.b64encode(b'RIFF\x00\x00\x00\x00WEBP' + b'\x00' * 32).decode()


@pytest.mark.parametrize('media_type,data', [
    ('image/jpeg', JPEG), ('image/png', PNG), ('image/webp', WEBP)])
def test_a_real_photo_becomes_an_image_block(media_type, data):
    block = ai_agent.photo_block({'media_type': media_type, 'data': data})
    assert block == {'type': 'image', 'source': {
        'type': 'base64', 'media_type': media_type, 'data': data}}


@pytest.mark.parametrize('photo', [
    None,
    'just a string',
    {'media_type': 'image/gif', 'data': JPEG},             # type not allowed
    {'media_type': 'image/png', 'data': JPEG},             # says PNG, is JPEG
    {'media_type': 'image/jpeg', 'data': 'not base64!!'},
    {'media_type': 'image/jpeg', 'data': ''},
    {'media_type': 'image/webp',
     'data': base64.b64encode(b'RIFF\x00\x00\x00\x00WAVE').decode()},
    {'media_type': 'image/jpeg', 'data': base64.b64encode(
        b'\xff\xd8\xff' + b'\x00' * ai_agent.MAX_PHOTO_BYTES).decode()},
])
def test_anything_else_is_refused(photo):
    with pytest.raises(ValueError):
        ai_agent.photo_block(photo)


def test_the_photo_goes_in_front_of_the_question():
    agent = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    photo = ai_agent.photo_block({'media_type': 'image/jpeg', 'data': JPEG})
    _, _, messages = agent._start_turn('s', 'What does this say?', 'translator',
                                       None, None, None, history=[], photo=photo)
    content = messages[-1]['content']
    assert content[0] == photo
    assert any(b.get('type') == 'text' and 'What does this say?' in b['text']
               for b in content[1:])


def test_other_modes_never_send_a_photo():
    """The route refuses first; this is the second lock behind it."""
    agent = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    photo = ai_agent.photo_block({'media_type': 'image/jpeg', 'data': JPEG})
    _, _, messages = agent._start_turn('s', 'hello', 'tutor',
                                       None, None, None, history=[], photo=photo)
    assert 'image' not in str(messages[-1]['content'])


def test_the_translator_prompt_says_how_to_read_a_photo():
    agent = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    prompt = agent.get_system_prompt('translator', {})
    assert 'PHOTOS' in prompt
    assert 'say so instead of guessing' in prompt


class FakeAgent:
    """No network, no cost: records what the route passed through."""

    model = 'claude-test'

    def __init__(self):
        self.kwargs = None

    def chat(self, **kwargs):
        self.kwargs = kwargs
        return {'success': True, 'response': 'stubbed', 'mode': kwargs.get('mode'),
                'tokens_used': {'input': 1, 'output': 1}}


@pytest.fixture
def pro_route(monkeypatch):
    fake = FakeAgent()
    monkeypatch.setattr(appmod, 'ai_agent', fake)
    monkeypatch.setattr(appmod, 'active_tier', lambda: 'pro')
    return fake


def test_the_route_sends_a_photo_with_more_room_to_answer(pro_route):
    r = app.test_client().post('/api/ai/chat', json={
        'message': '', 'mode': 'translator',
        'photo': {'media_type': 'image/jpeg', 'data': JPEG}})
    assert r.status_code == 200
    assert pro_route.kwargs['photo']['type'] == 'image'
    assert pro_route.kwargs['message'] == ai_agent.DEFAULT_PHOTO_MESSAGE
    assert pro_route.kwargs['max_tokens'] == appmod.AI_PHOTO_REPLY_TOKENS


def test_a_typed_message_keeps_the_usual_limit(pro_route):
    app.test_client().post('/api/ai/chat', json={'message': 'hello', 'mode': 'translator'})
    assert pro_route.kwargs['photo'] is None
    assert pro_route.kwargs['max_tokens'] == appmod.AI_REPLY_TOKENS


def test_the_route_refuses_a_photo_outside_the_translator(pro_route):
    r = app.test_client().post('/api/ai/chat', json={
        'message': 'hi', 'mode': 'tutor',
        'photo': {'media_type': 'image/jpeg', 'data': JPEG}})
    assert r.status_code == 400
    assert pro_route.kwargs is None


def test_the_route_refuses_a_broken_photo(pro_route):
    r = app.test_client().post('/api/ai/chat', json={
        'message': '', 'mode': 'translator',
        'photo': {'media_type': 'image/png', 'data': JPEG}})
    assert r.status_code == 400
    assert pro_route.kwargs is None


def test_free_users_see_the_pro_lock_not_a_photo_error(monkeypatch):
    monkeypatch.setattr(appmod, 'active_tier', lambda: 'free')
    r = app.test_client().post('/api/ai/chat', json={
        'message': '', 'mode': 'translator',
        'photo': {'media_type': 'image/jpeg', 'data': JPEG}})
    assert r.get_json()['gate'] == 'mode_locked'


def test_the_chat_page_has_the_photo_button():
    page = app.test_client().get('/chat').get_data(as_text=True)
    assert 'id="photo-btn"' in page
    assert 'id="photo-input"' in page
    # The photo is when someone relies on the answer for something serious.
    assert 'visa forms, medical or bank letters' in page
