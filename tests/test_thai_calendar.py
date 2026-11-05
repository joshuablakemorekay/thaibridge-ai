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


def cell(view, day):
    """The month-grid cell for a date."""
    return next(c for week in view['weeks'] for c in week
                if c['in_month'] and c['date'] == day)


class TestMultiDayBars:
    """Songkran is ONE bar over three days, named once, not three squeezed
    copies of its name."""

    def pieces(self, day):
        v = cal.month_view(2026, 4, 'gregorian')
        return [e for e in cell(v, day)['events'] if e['english'].startswith('Songkran')]

    def test_the_bar_joins_across_its_days(self):
        (first,), (middle,), (last,) = (self.pieces(date(2026, 4, d)) for d in (13, 14, 15))
        assert (first['joins_prev'], first['joins_next']) == (False, True)
        assert (middle['joins_prev'], middle['joins_next']) == (True, True)
        assert (last['joins_prev'], last['joins_next']) == (True, False)

    def test_it_is_named_once_and_spans_three_cells(self):
        named = [p for d in (13, 14, 15) for p in self.pieces(date(2026, 4, d)) if p['named']]
        assert len(named) == 1 and named[0]['span'] == 3

    def test_a_bar_that_wraps_to_a_new_week_is_named_again(self):
        # No real event crosses a weekend yet, so a made-up Fri–Mon one.
        e = cal._ev(date(2026, 4, 17), 'thai', 'Test', end=date(2026, 4, 20))  # Fri – Mon
        sunday = cal._bar_piece(e, date(2026, 4, 19), date(2026, 4, 30))
        assert sunday['named'] and sunday['joins_prev'] and sunday['span'] == 2

    def test_a_season_is_marked_on_its_first_day_only(self):
        v = cal.month_view(2026, 10, 'gregorian')
        days = [c['date'] for w in v['weeks'] for c in w if c['in_month']
                and any(e['english'] == 'Kathina season' for e in c['events'])]
        assert days == [date(2026, 10, 27)]

    def test_wan_phra_is_a_moon_not_an_event(self):
        v = cal.month_view(2026, 4, 'gregorian')
        assert not any(e['thai'] == 'วันพระ' for e in v['events'])
        assert cell(v, date(2026, 4, 2))['moon']['phase'] == 'full'


class TestYearView:
    def test_twelve_months_and_every_wan_phra(self):
        v = cal.year_view(2026, 'gregorian')
        assert [m['month'] for m in v['months']] == list(range(1, 13))
        assert v['wan_phra_count'] == sum(1 for d, p in cal._phases().items() if d.year == 2026)

    def test_a_day_shows_one_dot_per_kind_of_event(self):
        april = cal.year_view(2026, 'gregorian')['months'][3]
        sixth = next(c for w in april['weeks'] for c in w if c['in_month'] and c['date'].day == 6)
        assert sixth['kinds'] == ['thai', 'christian']        # Chakri Day + Easter Monday

    def test_buddhist_year_leaves_out_christian_events(self):
        v = cal.year_view(2026, 'buddhist')
        assert v['events'] and all(e['category'] != 'christian' for e in v['events'])


class TestNavigation:
    def test_year_layout_page_loads_with_every_month_linked(self, client):
        body = client.get('/calendar?layout=year&year=2027').get_data(as_text=True)
        assert 'Every event in 2027' in body
        for m in range(1, 13):
            assert 'view=gregorian&year=2027&month={}"'.format(m) in body

    def test_buddhist_year_uses_thai_month_names(self, client):
        body = client.get('/calendar?view=buddhist&layout=year&year=2026').get_data(as_text=True)
        assert 'พ.ศ. 2569' in body and 'เมษายน' in body and 'Christmas' not in body

    def test_there_is_a_today_button_and_a_month_picker(self, client):
        body = client.get('/calendar?year=2027&month=4').get_data(as_text=True)
        assert '>Today</a>' in body
        assert '<option value="4" selected>April</option>' in body
        assert '<option value="2027" selected>' in body

    def test_year_layout_moves_a_year_at_a_time(self, client):
        body = client.get('/calendar?layout=year&year=2027&month=4').get_data(as_text=True)
        assert 'layout=year&year=2026' in body and 'layout=year&year=2028' in body

    def test_today_is_marked_for_screen_readers(self, client):
        body = client.get('/calendar').get_data(as_text=True)
        today = date.today()
        if cal.YEARS[0] <= today.year <= cal.YEARS[-1]:
            assert 'aria-current="date"' in body

    def test_the_grid_fits_a_phone_without_sideways_scrolling(self, client):
        """base.js gives every table a 480px minimum on phones; seven days
        must fit on the screen, so the calendar opts out."""
        body = client.get('/calendar').get_data(as_text=True)
        assert '.table-scroll .cal-grid { min-width: 0; }' in body
