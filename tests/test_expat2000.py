"""Expat2000 — the free set-up guide for expats and digital nomads.

Like Survival Thai, its job is to be a front door, so most tests here check
that nothing stands between a brand-new visitor and the page. The rest guard
the two things most likely to rot: the facts (which go stale) and the Thai
(which must keep the same shape as the rest of the course).
"""
import re

import pytest

import app as app_module
import expat2000


@pytest.fixture
def client():
    return app_module.app.test_client()


class TestItIsActuallyFree:
    def test_a_brand_new_visitor_can_read_it(self, client):
        assert client.get('/expat2000').status_code == 200

    def test_the_page_is_the_guide_not_a_locked_notice(self, client):
        # locked.html also returns 200, so check real content is there.
        body = client.get('/expat2000').get_data(as_text=True)
        assert 'EXPAT' in body
        assert 'วีซ่า' in body
        assert 'Destination Thailand Visa' in body

    def test_it_is_free_and_needs_no_alphabet(self):
        requirement = app_module.SECTION_REQUIREMENTS['expat2000']
        assert requirement['tier'] == 'free'
        assert requirement['level'] == 1
        assert requirement['requires_alphabet'] is False

    def test_the_home_page_points_at_it(self, client):
        assert 'href="/expat2000"' in client.get('/').get_data(as_text=True)

    def test_it_is_in_the_top_menu_on_every_page(self, client):
        # The top menu lives in base.html, so any other page proves it.
        body = client.get('/survival').get_data(as_text=True)
        nav = body.split('id="main-nav"', 1)[1].split('</ul>', 1)[0]
        assert 'href="/expat2000"' in nav


class TestTheContent:
    def test_every_mission_has_know_do_and_say(self):
        for mission in expat2000.MISSIONS:
            assert mission['know'], mission['key']
            assert mission['do'], mission['key']
            assert mission['say'], mission['key']

    def test_every_phrase_has_all_three_parts(self):
        for phrase in expat2000.all_phrases():
            assert phrase['thai'], phrase
            assert phrase['paiboon'], phrase['thai']
            assert phrase['english'], phrase['thai']

    def test_checklist_ids_are_unique(self):
        """Ticks are saved by id in the visitor's browser. A duplicate would
        tick two boxes at once."""
        tasks = expat2000.all_tasks()
        assert len(tasks) == len(set(tasks))

    def test_mission_keys_are_safe_anchors(self):
        # Used as #anchors and in a CSS selector by the page's script.
        for mission in expat2000.MISSIONS:
            assert re.fullmatch(r'[a-z][a-z0-9-]*', mission['key'])

    def test_every_linked_source_exists(self):
        for mission in expat2000.MISSIONS:
            for key in mission['links']:
                assert key in expat2000.OFFICIAL_LINKS, key

    def test_official_sources_are_government_sites(self):
        """The page leans on these as the authority, so they must be the real
        thing — never a look-alike agency site."""
        for link in expat2000.OFFICIAL_LINKS.values():
            assert re.match(r'https://[a-z.]+\.go\.th/', link['url']), link['url']


class TestTheFactsStayHonest:
    def test_it_does_not_promise_the_old_60_day_stay(self):
        """Visa-free stays dropped from 60 to 30 days on 15 September 2026.
        Most guides online still say 60, which is how it could creep back in."""
        visas = ' '.join(expat2000.MISSIONS_BY_KEY['visas']['know'])
        assert '30 days' in visas
        assert '60 days to 30' in visas

    def test_the_last_checked_date_is_shown(self, client):
        body = client.get('/expat2000').get_data(as_text=True)
        assert expat2000.LAST_CHECKED in body


class TestTheAudioStrings:
    def test_no_templates_or_either_or_forms_are_recorded(self):
        for text in expat2000.thai_strings():
            assert '...' not in text and '/' not in text

    def test_the_audio_script_knows_about_this_page(self):
        import importlib.util, pathlib
        path = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'generate_thai_phrase_audio.py'
        spec = importlib.util.spec_from_file_location('gen_audio', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert 'expat2000' in module.PAGES
