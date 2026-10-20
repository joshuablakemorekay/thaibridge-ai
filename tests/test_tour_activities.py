"""Things to do in Thailand — the Tour Guide page's booking section.

The money side is what needs guarding: an affiliate link must always be
labelled (UK advertising rules), an empty id must never leave a broken
"?partner_id=" in a link, and the temple route must stay commission-free.
"""
import os
import re

import pytest

import tour_activities
import tour_trips

_HAS_THAI = re.compile('[฀-๿]')


@pytest.fixture
def affiliate_ids(monkeypatch):
    """Pretend every programme has approved us, without touching the real ids."""
    for key, info in tour_activities.AFFILIATES.items():
        fake = 'https://skyscanner.pxf.io/c/1/2/3' if info['param'] is None else 'TEST' + key.upper()
        monkeypatch.setitem(info, 'id', fake)


class TestTheLinks:
    def test_without_an_id_a_link_is_plain(self, monkeypatch):
        monkeypatch.setitem(tour_activities.AFFILIATES['getyourguide'], 'id', '')
        link = tour_activities.booking_link('getyourguide', 'https://www.getyourguide.com/s/?q=Krabi')
        assert link == {'url': 'https://www.getyourguide.com/s/?q=Krabi',
                        'partner': 'GetYourGuide', 'affiliate': False}

    def test_an_id_is_added_to_the_existing_query(self, affiliate_ids):
        link = tour_activities.booking_link('getyourguide', 'https://www.getyourguide.com/s/?q=Krabi')
        assert link['url'] == 'https://www.getyourguide.com/s/?q=Krabi&partner_id=TESTGETYOURGUIDE'
        assert link['affiliate'] is True

    def test_an_id_on_a_link_with_no_query(self, affiliate_ids):
        link = tour_activities.booking_link('12go', 'https://12go.asia/en/travel/chiang-mai/pai')
        assert link['url'] == 'https://12go.asia/en/travel/chiang-mai/pai?z=TEST12GO'

    def test_skyscanner_wraps_the_page_in_the_impact_link(self, affiliate_ids):
        page = 'https://www.skyscanner.net/flights-to/th/cheap-flights-to-thailand.html'
        link = tour_activities.booking_link('skyscanner', page)
        assert link['url'].startswith('https://skyscanner.pxf.io/c/1/2/3?u=https%3A%2F%2Fwww.skyscanner.net')

    def test_every_link_names_a_known_partner(self):
        for a in tour_activities.ACTIVITIES:
            for partner, label, url in a['links']:
                assert partner == 'info' or partner in tour_activities.AFFILIATES, a['key']
                assert label.strip() and url.startswith('https://'), a['key']

    def test_the_temple_route_never_earns_commission(self, affiliate_ids):
        """Josh's call: nobody earns from a visit to a temple."""
        temples = tour_activities.ACTIVITIES_BY_KEY['temples']
        assert all(link['partner'] == '' and not link['affiliate']
                   for link in tour_activities.links_for(temples))

    def test_the_activities_josh_asked_for_are_there(self):
        keys = set(tour_activities.ACTIVITIES_BY_KEY)
        assert {'flights', 'temples', 'climbing', 'diving', 'sea-fishing', 'freshwater-fishing',
                'hiking', 'wildlife', 'road-trip', 'off-road', 'quad-biking'} <= keys

    def test_temple_route_links_to_real_trips(self):
        for key in tour_activities.ACTIVITIES_BY_KEY['temples']['trips']:
            assert key in tour_trips.TRIPS_BY_KEY


class TestPhotosAndPhrases:
    STATIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

    @pytest.mark.parametrize('a', tour_activities.ACTIVITIES, ids=lambda a: a['key'])
    def test_every_photo_is_on_disk_and_credited(self, a):
        photo = a['photo']
        path = os.path.join(self.STATIC, *photo['file'].split('/'))
        assert 10_000 < os.path.getsize(path) < 400_000
        assert photo['license'].startswith(('CC BY', 'CC0', 'Public domain'))
        assert 'NC' not in photo['license'] and 'ND' not in photo['license']
        assert photo['artist'].strip() and photo['alt'].strip()
        assert photo['source'].startswith('https://commons.wikimedia.org/')

    @pytest.mark.parametrize('a', tour_activities.ACTIVITIES, ids=lambda a: a['key'])
    def test_every_phrase_is_thai_with_a_spelling_and_a_meaning(self, a):
        assert a['phrases']
        for thai, paiboon, english in a['phrases']:
            assert _HAS_THAI.search(thai) and not _HAS_THAI.search(paiboon), thai
            assert paiboon.strip() and english.strip(), thai
            assert 'ng' not in paiboon, 'ThaiBridge Spelling writes ŋ, not ng'


class TestThePage:
    def test_the_activities_are_on_the_page(self, unlocked_client):
        body = unlocked_client.get('/tour-guide').get_data(as_text=True)
        assert 'id="things-to-do"' in body
        assert 'Play it first' in body, 'the temple route links to the trips here'
        for a in tour_activities.ACTIVITIES:
            assert a['title'] in body
            assert a['photo']['source'] in body

    def test_no_commission_note_while_no_programme_has_approved(self, unlocked_client, monkeypatch):
        for info in tour_activities.AFFILIATES.values():
            monkeypatch.setitem(info, 'id', '')
        body = unlocked_client.get('/tour-guide').get_data(as_text=True)
        assert 'affiliate-note' not in body
        assert 'rel="sponsored' not in body

    def test_affiliate_links_are_labelled(self, unlocked_client, affiliate_ids):
        body = unlocked_client.get('/tour-guide').get_data(as_text=True)
        assert 'class="affiliate-note"' in body
        links = re.findall(r'<a class="activity-link"[^>]*>.*?</a>', body, re.S)
        sponsored = [l for l in links if 'rel="sponsored' in l]
        assert sponsored, 'expected some affiliate links'
        for link in sponsored:
            assert 'ad-label' in link, link

    def test_the_policies_page_explains_booking_links(self):
        import app as appmod
        body = appmod.app.test_client().get('/policies').get_data(as_text=True)
        assert 'Booking links' in body and 'affiliate' in body


class TestFreeToRead:
    """The trips stay paid; the travel ideas are on the locked page too, so
    people without a plan, and search engines, can find the booking links."""

    @pytest.fixture
    def free_client(self, make_client):
        return make_client(subscription_tier='free', is_developer=False, full_unlock=False,
                           level=1, xp=0)

    def test_the_locked_tour_guide_page_shows_the_activities(self, free_client):
        body = free_client.get('/tour-guide').get_data(as_text=True)
        assert '<h1>Section Locked</h1>' in body, 'the trips must stay paid'
        assert 'id="things-to-do"' in body
        assert 'id="trip-player"' not in body
        for a in tour_activities.ACTIVITIES:
            assert a['title'] in body
            assert a['photo']['source'] in body, 'photo credits must come along'

    def test_no_play_it_first_links_where_there_are_no_trips(self, free_client):
        body = free_client.get('/tour-guide').get_data(as_text=True)
        assert 'Play it first' not in body

    def test_other_locked_pages_do_not_show_it(self, free_client):
        body = free_client.get('/business-thai').get_data(as_text=True)
        assert '<h1>Section Locked</h1>' in body
        assert 'id="things-to-do"' not in body
