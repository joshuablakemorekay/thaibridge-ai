"""The tutor is handed checked facts from the app's own lessons.

tutor_reference exists because the accuracy exam caught Sonnet 5.5 calling ด a
low-class consonant, a fact this codebase already records correctly. These
tests pin that the right facts reach the tutor, and that the universal and
neutral Dhamma lenses — which promise answers without Thai — get none.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

import ai_agent  # noqa: E402
import paiboon_lookup  # noqa: E402
import tutor_reference  # noqa: E402

E = paiboon_lookup.Entry
INDEX = [
    E('ตัว', 'dtuua', 'body / classifier', 'Vowels'),
    E('คน', 'kon', 'people', 'Read & Write'),
    E('ขอบคุณ', 'kɔ̀ɔp-kun', 'Thank you', 'Survival Thai'),
    E('บุญ', 'bun', 'merit', 'Read & Write'),
]


def test_consonant_classes_come_from_the_alphabet_data():
    sheet = tutor_reference.consonant_classes()
    middle = next(line for line in sheet.splitlines() if line.startswith('- Middle'))
    low = next(line for line in sheet.splitlines() if line.startswith('- Low'))
    for letter in 'ดบจป':          # the four a model filed under low class
        assert letter in middle and letter not in low


def test_every_mode_carries_the_consonant_classes():
    agent = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    for mode in ('conversation', 'tutor', 'generator', 'cultural', 'buddhist', 'helper'):
        assert tutor_reference.consonant_classes() in agent.get_system_prompt(mode, {})


def test_thai_in_the_question_finds_its_entries():
    found = [e.thai for e in tutor_reference.entries_for('Can ตัว count คน?', INDEX)]
    assert found == ['ตัว', 'คน']


def test_words_inside_a_longer_thai_run_are_found():
    """Thai has no spaces: คนสองตัว holds both คน and ตัว."""
    found = {e.thai for e in tutor_reference.entries_for('คนสองตัว', INDEX)}
    assert found == {'ตัว', 'คน'}


def test_english_in_the_question_finds_its_entries():
    found = [e.thai for e in tutor_reference.entries_for('How do I say thank you?', INDEX)]
    assert found == ['ขอบคุณ']


def test_nothing_matching_gives_no_reference():
    assert tutor_reference.reference_for('What is the weather like?', INDEX) == ''


def test_the_chanting_draft_is_left_out(monkeypatch):
    monkeypatch.setattr(paiboon_lookup, 'get_index', lambda: INDEX + [
        E('นะโม', 'ná-moo', 'homage', 'Chanting book')])
    assert tutor_reference.entries_for('นะโม') == []


# ── What the tutor actually sends ─────────────────────────────────────────

class _Messages:
    def create(self, **kw):
        self.request = kw
        return type('R', (), {
            'content': [type('B', (), {'type': 'text', 'text': 'ok'})()],
            'usage': type('U', (), {'input_tokens': 1, 'output_tokens': 1})(),
            'stop_reason': 'end_turn'})()


@pytest.fixture
def agent(monkeypatch):
    monkeypatch.setattr(paiboon_lookup, 'get_index', lambda: INDEX)
    a = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    a.client = type('C', (), {'messages': _Messages()})()
    return a


def _sent(agent):
    return agent.client.messages.request['messages'][-1]['content']


def test_the_reference_rides_with_the_question(agent):
    agent.chat('s1', 'Explain ตัว', mode='tutor')
    content = _sent(agent)
    assert 'REFERENCE' in content[0]['text'] and 'dtuua' in content[0]['text']
    assert content[1]['text'] == 'Explain ตัว'


@pytest.mark.parametrize('lens', ['universal', 'neutral', None])
def test_thai_free_lenses_get_no_reference(agent, lens):
    agent.chat('s2', 'What is merit?', mode='buddhist', lens=lens)
    assert _sent(agent) == 'What is merit?'


def test_the_thai_lens_gets_the_reference(agent):
    agent.chat('s3', 'What is merit?', mode='buddhist', lens='thai')
    assert 'bun' in _sent(agent)[0]['text']


def test_a_broken_lookup_costs_the_reference_not_the_answer(agent, monkeypatch):
    def boom():
        raise RuntimeError('index failed')
    monkeypatch.setattr(paiboon_lookup, 'get_index', boom)
    assert agent.chat('s4', 'Explain ตัว', mode='tutor')['success'] is True
    assert _sent(agent) == 'Explain ตัว'
