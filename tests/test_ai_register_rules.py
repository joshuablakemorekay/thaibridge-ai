"""The AI tutor must teach the same politeness rules the Sentences page shows.

Found the hard way: asked "when I hand something to a monk, do I say ให้ or
ถวาย?", the live tutor answered ให้ — twice, in two modes — and told the learner
ถวาย was for elders and royalty. That is the exact reverse of the monastic note
on the Sentences page, which calls swapping ถวาย for ให้ "the single most common
mistake a learner makes at a temple". The tutor was not being stupid; nothing
in its prompt had ever mentioned registers, so it answered from memory.

The fix keeps one copy of the rules in thai_registers.py and has the prompt
import it. These tests pin both halves: that every mode's prompt carries the
rules, and that the rules name the same words the page's own notes rely on —
so a rule cannot be softened in one place and stay strict in the other.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ai_agent  # noqa: E402
import thai_registers  # noqa: E402

MODES = ('conversation', 'tutor', 'generator', 'cultural', 'buddhist', 'helper')


@pytest.fixture(scope='module')
def agent():
    # No real key: get_system_prompt is pure string-building and never calls out.
    return ai_agent.ThaiLearningAI(api_key='test-key-not-used')


@pytest.mark.parametrize('mode', MODES)
def test_every_mode_carries_the_register_rules(agent, mode):
    prompt = agent.get_system_prompt(mode, {'level': 1, 'xp': 0})
    assert thai_registers.REGISTER_RULES_FOR_AI in prompt


def test_rules_say_thawai_is_for_monks_and_hai_is_not():
    rules = thai_registers.REGISTER_RULES_FOR_AI
    # The one line the live tutor got backwards.
    assert 'ถวาย' in rules and 'ให้' in rules
    thawai = rules.index('ถวาย')
    assert 'MONK' in rules[thawai:thawai + 80].upper(), (
        'ถวาย must be tied to the monk in the same breath, not left for the '
        'model to guess which word goes with whom')


def test_rules_cover_every_word_the_monastic_notes_use():
    """If a monastic note on the page leans on a word, the tutor must know it."""
    rules = thai_registers.REGISTER_RULES_FOR_AI
    for word in ('ถวาย', 'นิมนต์', 'อาตมา', 'โยม', 'เจริญพร', 'พระอาจารย์'):
        assert word in rules, f'{word} is taught on the page but not to the tutor'


def test_rules_forbid_a_casual_form_to_a_monk():
    rules = thai_registers.REGISTER_RULES_FOR_AI
    assert 'no casual form' in rules.lower()


def test_rules_read_from_one_place_only():
    """The prompt must import the rules, not paste a second copy that can drift."""
    src = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'ai_agent.py'), encoding='utf-8').read()
    assert 'from thai_registers import REGISTER_RULES_FOR_AI' in src
    assert src.count('ถวาย') == 0, (
        'ai_agent.py should not carry its own copy of the monk vocabulary')
