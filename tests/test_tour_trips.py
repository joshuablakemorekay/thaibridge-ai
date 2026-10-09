"""Tour Guide trips — short journeys played in Thai.

Most of these guard the CONTENT, because the player is plain JavaScript walking
over tour_trips.TRIPS: if the data is well-formed, the page works. A missing
right answer or a stop index past the end of the route would strand a learner
mid-trip with no way forward, and nothing else would catch it.
"""
import os
import re

import pytest

import tour_trips

REGIONS = {'North', 'Central', 'Northeast', 'East', 'South', 'West'}
_HAS_THAI = re.compile('[฀-๿]')


class TestTheTripsAreFinishable:
    def test_every_region_has_a_trip(self):
        """The six regions the Tourism Authority of Thailand uses, each covered
        at least once (the North has two: Chiang Mai and Chiang Rai)."""
        assert {t['region'] for t in tour_trips.TRIPS} == REGIONS

    def test_the_trips_josh_asked_for_are_there(self):
        assert 'chiang-rai' in tour_trips.TRIPS_BY_KEY
        bangkok = tour_trips.TRIPS_BY_KEY['bangkok-river']
        assert any('Sampheng' in sc['place'] for sc in bangkok['scenes'])
        krabi = tour_trips.TRIPS_BY_KEY['railay']
        assert any('Khlong Thom' in sc['place'] for sc in krabi['scenes'])

    def test_keys_are_unique(self):
        keys = [t['key'] for t in tour_trips.TRIPS]
        assert len(keys) == len(set(keys))

    @pytest.mark.parametrize('trip', tour_trips.TRIPS, ids=lambda t: t['key'])
    def test_every_scene_can_be_passed(self, trip):
        """A 'miss' sends the learner back to try again. A scene where every
        answer is a miss would be a dead end."""
        for scene in trip['scenes']:
            verdicts = [c['verdict'] for c in scene['choices']]
            assert 'good' in verdicts, scene['title']
            assert set(verdicts) <= {'good', 'ok', 'miss'}, scene['title']

    @pytest.mark.parametrize('trip', tour_trips.TRIPS, ids=lambda t: t['key'])
    def test_every_scene_sits_on_the_route(self, trip):
        assert 4 <= len(trip['stops']) <= 6, 'more than six stops will not fit on a phone'
        for scene in trip['scenes']:
            assert 0 <= scene['stop'] < len(trip['stops']), scene['title']
        assert {sc['stop'] for sc in trip['scenes']} == set(range(len(trip['stops']))),             'every stop on the route should have at least one scene'

    @pytest.mark.parametrize('trip', tour_trips.TRIPS, ids=lambda t: t['key'])
    def test_the_tutor_link_points_at_a_real_roleplay(self, trip):
        """The end of each trip links to /chat?scenario=<id>. An id the chat page
        does not know is silently ignored, which would look like a broken link."""
        from ai_agent import ROLEPLAY_SCENARIOS
        assert trip['tutor'] in ROLEPLAY_SCENARIOS


class TestPhotos:
    STATIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

    @pytest.mark.parametrize('trip', tour_trips.TRIPS, ids=lambda t: t['key'])
    def test_every_trip_has_a_photo_on_disk(self, trip):
        path = os.path.join(self.STATIC, *trip['photo']['file'].split('/'))
        assert os.path.getsize(path) > 10_000, 'missing or empty photo'
        assert os.path.getsize(path) < 400_000, 'shrink it: this loads on phones'

    @pytest.mark.parametrize('trip', tour_trips.TRIPS, ids=lambda t: t['key'])
    def test_every_photo_is_credited_under_a_reusable_licence(self, trip):
        """CC BY and BY-SA allow reuse WITH credit; NC (non-commercial) does not
        fit a paid app, and ND is fine to show but is a trap for the next edit."""
        photo = trip['photo']
        for field in ('alt', 'artist', 'license', 'license_url', 'source'):
            assert photo[field].strip(), field
        assert photo['license'].startswith(('CC BY', 'CC0', 'Public domain'))
        assert 'NC' not in photo['license'] and 'ND' not in photo['license']
        assert photo['source'].startswith('https://commons.wikimedia.org/')


class TestPoliteEndings:
    def test_a_woman_asks_with_ka_high_and_answers_with_ka_falling(self):
        """The ค่ะ / คะ split is the classic mistake; the trips teach it."""
        assert tour_trips.fill_particles('เท่าไหร่{q}', 'female') == 'เท่าไหร่คะ'
        assert tour_trips.fill_particles('ไม่เผ็ด{s}', 'female') == 'ไม่เผ็ดค่ะ'
        assert tour_trips.fill_particles('lót dâi mǎi {q}', 'female', paiboon=True) == 'lót dâi mǎi ká'

    def test_a_man_uses_krap_for_both(self):
        assert tour_trips.fill_particles('เท่าไหร่{q}', 'male') == 'เท่าไหร่ครับ'
        assert tour_trips.fill_particles('ไม่เผ็ด{s}', 'male') == 'ไม่เผ็ดครับ'

    @pytest.mark.parametrize('trip', tour_trips.TRIPS, ids=lambda t: t['key'])
    def test_thai_and_paiboon_carry_the_same_markers(self, trip):
        """If the Thai has a {q} and the Paiboon a {s}, a woman would see คะ
        written above kâ, teaching the very mistake this is meant to prevent."""
        for scene in trip['scenes']:
            for c in scene['choices']:
                assert re.findall(r'\{[sq]\}', c['thai']) == re.findall(r'\{[sq]\}', c['paiboon']), c['thai']

    def test_questions_take_the_question_marker(self):
        """A learner line ending in ไหม is a question, so it must be {q}."""
        for trip in tour_trips.TRIPS:
            for scene in trip['scenes']:
                for c in scene['choices']:
                    assert 'ไหม{s}' not in c['thai'], c['thai']


class TestAudio:
    def test_learner_lines_are_recorded_for_each_speaker(self):
        strings = tour_trips.thai_strings()
        assert 'เท่าไหร่ครับ' in strings
        assert 'เท่าไหร่คะ' in strings

    def test_no_unfilled_markers_or_blanks_reach_the_recorder(self):
        for thai in tour_trips.thai_strings():
            assert '{' not in thai and '...' not in thai, thai
            assert _HAS_THAI.search(thai), thai


class TestThePage:
    def test_the_trips_are_on_the_tour_guide_page(self, unlocked_client):
        body = unlocked_client.get('/tour-guide').get_data(as_text=True)
        for trip in tour_trips.TRIPS:
            assert trip['title'] in body
        assert 'id="trip-player"' in body

    def test_the_phrasebook_is_still_there(self, unlocked_client):
        """The trips were added above the word list, not instead of it."""
        body = unlocked_client.get('/tour-guide').get_data(as_text=True)
        assert 'id="phrasebook"' in body
        assert 'แท็กซี่' in body

    def test_the_photo_credits_are_printed(self, unlocked_client):
        body = unlocked_client.get('/tour-guide').get_data(as_text=True)
        for trip in tour_trips.TRIPS:
            assert trip['photo']['source'] in body

    def test_it_welcomes_more_than_tourists(self, unlocked_client):
        body = unlocked_client.get('/tour-guide').get_data(as_text=True)
        assert 'anyone exploring Thailand' in body

    def test_the_page_stays_paid(self):
        """Adding trips did not change who can open the page."""
        import app as app_module
        assert app_module.SECTION_REQUIREMENTS['tour_guide']['tier'] == 'basic'
