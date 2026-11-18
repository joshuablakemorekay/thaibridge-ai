"""Phase 3c of the website work: public previews of locked course sections.

section_previews.py describes what each paid section teaches, shown on the
locked page above the unlock requirements. These tests keep the previews
honest: every one belongs to a real locked section at a real address, the
numbers it quotes match the course, and it never makes a promise the house
rules forbid.
"""
import re

import pytest

import app as app_module
from section_previews import SECTION_PREVIEWS


@pytest.fixture
def visitor():
    return app_module.app.test_client()


@pytest.mark.parametrize('section_id', sorted(SECTION_PREVIEWS))
def test_each_preview_is_for_a_paid_section_at_its_own_address(visitor, section_id):
    preview = SECTION_PREVIEWS[section_id]
    assert app_module.SECTION_REQUIREMENTS[section_id]['tier'] != 'free'
    html = visitor.get(preview['path']).get_data(as_text=True)
    assert '<h1>' + preview['name'].replace('&', '&amp;') + '</h1>' in html, preview['path']
    for point in preview['points']:
        assert point.replace('&', '&amp;').replace('"', '&#34;') in html


@pytest.mark.parametrize('section_id', sorted(SECTION_PREVIEWS))
def test_preview_text_fits_a_search_result_and_keeps_the_house_rules(section_id):
    preview = SECTION_PREVIEWS[section_id]
    assert 60 <= len(preview['summary']) <= 175
    assert 2 <= len(preview['points']) <= 4
    text = (preview['summary'] + ' '.join(preview['points'])).lower()
    # Audio is text-to-speech: never call it real or native.
    assert not re.search(r'\b(real|native)[- ](audio|recording|voice)', text)
    assert 'unlimited' not in text


def test_the_lesson_count_matches_the_curriculum():
    assert '15 ' in SECTION_PREVIEWS['lessons']['summary']
    assert len(app_module.LESSONS) == 15


def test_a_learner_with_access_never_sees_the_preview(make_client):
    html = make_client().get('/lessons').get_data(as_text=True)
    assert 'class="section-preview"' not in html
