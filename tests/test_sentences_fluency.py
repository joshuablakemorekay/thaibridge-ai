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

