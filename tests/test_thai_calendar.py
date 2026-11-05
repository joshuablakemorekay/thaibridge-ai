"""The /calendar page and the moon maths behind it.

The holy days are WORKED OUT from the Wan Phra table, so the strongest test
is checking them against the dates Thailand actually announced.
"""
from datetime import date

import pytest

import app as app_module
import thai_calendar as cal


@pytest.fixture
def client():
    return app_module.app.test_client()


def find(year, english):
    return [e['date'] for e in cal.events(year) if e['english'] == english]


class TestTheWanPhraTable:
    def test_every_gap_fits_the_moon_cycle(self):
        # _phases() raises on a gap that doesn't fit, i.e. a typo in the table.
        phases = cal._phases()
        assert len(phases) == sum(len(v) for v in cal.WAN_PHRA.values()) - 2  # 2 Khao Phansa days

    def test_the_phases_go_round_in_order(self):
        seq = [p for _, p in sorted(cal._phases().items())]
        for a, b in zip(seq, seq[1:]):
            assert cal.PHASES.index(b) == (cal.PHASES.index(a) + 1) % 4

    def test_every_day_of_every_year_has_a_moon_day(self):
        days = cal.lunar_days()
        assert date(cal.YEARS[0], 1, 1) in days and date(cal.YEARS[-1], 12, 31) in days
        assert all(1 <= m['day'] <= 15 for m in days.values())


class TestOfficialDates:
    # 2569 / 2026: government holiday calendar. 2570 / 2027: Bank of Thailand
    # announcement 37/2569.
    @pytest.mark.parametrize('year, english, expected', [
        (2026, 'Makha Bucha Day', date(2026, 3, 3)),
        (2026, 'Visakha Bucha Day', date(2026, 5, 31)),
        (2026, 'Atthami Bucha Day', date(2026, 6, 8)),
        (2026, 'Asanha Bucha Day', date(2026, 7, 29)),
        (2026, 'Khao Phansa (Rains Retreat begins)', date(2026, 7, 30)),
        (2026, 'Ok Phansa (Rains Retreat ends)', date(2026, 10, 26)),
        (2026, 'Loy Krathong', date(2026, 11, 24)),
        (2027, 'Makha Bucha Day', date(2027, 2, 21)),
        (2027, 'Visakha Bucha Day', date(2027, 5, 20)),
        (2027, 'Asanha Bucha Day', date(2027, 7, 18)),
        (2027, 'Khao Phansa (Rains Retreat begins)', date(2027, 7, 19)),
    ])
    def test_holy_day(self, year, english, expected):
        assert find(year, english) == [expected]

    def test_2569_has_two_eighth_months(self):
        days = cal.lunar_days()
        assert days[date(2026, 3, 3)]['label_th'] == 'ขึ้น 15 ค่ำ เดือน 4'     # Makha in month 4
        assert days[date(2026, 7, 30)]['label_th'] == 'แรม 1 ค่ำ เดือน 8 หลัง'  # as announced

    def test_an_ordinary_year_keeps_makha_in_month_3(self):
        assert cal.lunar_days()[date(2027, 2, 21)]['label_th'] == 'ขึ้น 15 ค่ำ เดือน 3'


class TestChristianDates:
    @pytest.mark.parametrize('year, expected', [
        (2026, date(2026, 4, 5)), (2027, date(2027, 3, 28)), (2028, date(2028, 4, 16))])
    def test_easter(self, year, expected):
        assert cal.easter(year) == expected

    def test_advent_sunday_2026(self):
        assert find(2026, 'Advent Sunday') == [date(2026, 11, 29)]


class TestViews:
    def test_buddhist_view_leaves_out_christian_events(self):
        v = cal.month_view(2026, 12, 'buddhist')
        assert v['events'] and all(e['category'] != 'christian' for e in v['events'])

    def test_gregorian_view_has_christmas_and_fathers_day(self):
        names = [e['english'] for e in cal.month_view(2026, 12, 'gregorian')['events']]
        assert 'Christmas Day' in names and "Father's Day (Thailand)" in names

    def test_out_of_range_months_are_clamped(self):
        assert cal.clamp(2019, 5) == (cal.YEARS[0], 1)
        assert cal.clamp(2099, 5) == (cal.YEARS[-1], 12)


class TestPage:
    @pytest.mark.parametrize('view', ['gregorian', 'buddhist'])
    def test_page_loads_for_a_guest(self, client, view):
        r = client.get('/calendar?view={}&year=2026&month=4'.format(view))
        assert r.status_code == 200
        assert 'Songkran' in r.get_data(as_text=True) or 'สงกรานต์' in r.get_data(as_text=True)

    def test_buddhist_view_shows_the_be_year_and_moon_days(self, client):
        body = client.get('/calendar?view=buddhist&year=2026&month=3').get_data(as_text=True)
        assert 'พ.ศ. 2569' in body and 'ขึ้น 15 ค่ำ เดือน 4' in body

    def test_gregorian_view_shows_easter(self, client):
        body = client.get('/calendar?year=2026&month=4').get_data(as_text=True)
        assert 'Easter Sunday' in body

    def test_bad_query_values_fall_back_to_today(self, client):
        assert client.get('/calendar?year=abc&month=x').status_code == 200

    def test_culture_page_links_to_the_calendar(self):
        with open('templates/culture.html', encoding='utf-8') as f:
            assert 'href="/calendar"' in f.read()
