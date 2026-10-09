"""The Sentences page's production practice: off-script links, answering
questions, and the sentence builder drill.

The page used to show finished sentences only. These tests pin the parts that
make a learner produce Thai themselves.
"""
import pytest

from ai_agent import ROLEPLAY_SCENARIOS
from app import CONVERSATIONS


@pytest.fixture
def sentences_html(unlocked_client):
    html = unlocked_client.get('/sentences').get_data(as_text=True)
    assert 'Section Locked' not in html, 'the gate is still shut'
    return html


# ── Off-script links ───────────────────────────────────────────────────────

def test_every_conversation_with_a_roleplay_links_to_it(sentences_html):
    shared = set(CONVERSATIONS) & set(ROLEPLAY_SCENARIOS)
    assert shared, 'no conversation matches a roleplay — the ids have drifted'
    for conv_id in shared:
        assert f'/chat?scenario={conv_id}"' in sentences_html


def test_conversations_without_a_roleplay_get_no_link(sentences_html):
    # Temple, alms and meditation were kept out of the tutor on purpose
    # (monastic register), so they must not grow a link to a scene that
    # doesn't exist.
    for conv_id in set(CONVERSATIONS) - set(ROLEPLAY_SCENARIOS):
        assert f'/chat?scenario={conv_id}"' not in sentences_html


def test_chat_page_reads_the_scenario_parameter(unlocked_client):
    html = unlocked_client.get('/chat?scenario=restaurant').get_data(as_text=True)
    assert "params.get('scenario')" in html
    assert 'data-scenario="restaurant"' in html


# ── Answering questions ────────────────────────────────────────────────────

from app import SENTENCE_PATTERNS  # noqa: E402

ANSWER_PATTERNS = SENTENCE_PATTERNS['answering']['patterns']
ALL_PAIRS = [
    (p['key'], side, ex)
    for p in ANSWER_PATTERNS
    for side in ('male', 'female')
    for ex in p['examples'][side]
]


@pytest.mark.parametrize('key,side,ex', ALL_PAIRS)
def test_every_pair_has_a_question_a_yes_and_a_no(key, side, ex):
    for part in ('q', 'yes', 'no'):
        assert ex[part]['thai'] and ex[part]['paiboon'] and ex[part]['english']


@pytest.mark.parametrize('key,side,ex', ALL_PAIRS)
def test_particles_match_the_speaker(key, side, ex):
    # Women ask with คะ (high) and answer with ค่ะ (falling) — mixing them up
    # is exactly the mistake this section should not model.
    if side == 'male':
        assert all(ex[p]['thai'].endswith('ครับ') for p in ('q', 'yes', 'no'))
    else:
        assert ex['q']['thai'].endswith('คะ')
        assert ex['yes']['thai'].endswith('ค่ะ') and ex['no']['thai'].endswith('ค่ะ')


@pytest.mark.parametrize('key,side,ex', ALL_PAIRS)
def test_every_no_answer_is_negated(key, side, ex):
    assert 'ไม่' in ex['no']['thai']


def test_both_genders_get_the_same_number_of_examples():
    for p in ANSWER_PATTERNS:
        assert len(p['examples']['male']) == len(p['examples']['female']), p['key']


def test_answering_section_is_on_the_page(sentences_html):
    assert 'id="answering"' in sentences_html
    for p in ANSWER_PATTERNS:
        assert p['examples']['male'][0]['no']['thai'] in sentences_html
