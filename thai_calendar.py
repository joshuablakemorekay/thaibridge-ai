"""The /calendar page: one year of Thai, Buddhist and Christian/Western dates,
shown either as a Gregorian calendar or as the Buddhist-Era calendar Thais use.

Why a TABLE of Wan Phra dates and not an algorithm
---------------------------------------------------
Buddhist holy days follow the Thai lunar calendar (ปฏิทินจันทรคติ), whose leap
months and leap days are set by rule-of-thumb astronomy that even Thai sites
disagree about at the edges. Getting one wrong would put Makha Bucha on the
wrong day, so the source of truth is the published list of every วันพระ for
each year, copied from calendar.kapook.com/<BE year>/buddhistholyday.

Everything else lunar is WORKED OUT from that list, not typed in:
  - each Wan Phra is one of four moon phases, in a fixed order
    (waxing 8 -> full -> waning 8 -> new), so its phase follows from the gaps;
  - every other day's moon day (ขึ้น 3 ค่ำ, แรม 9 ค่ำ...) is counted from the
    new or full moon before it;
  - the lunar MONTH comes from counting full moons from one known anchor,
    with the 8th month repeated in a leap-month year (LEAP_MONTH_YEARS).
That means the big holy days (Makha, Visakha, Asanha, Ok Phansa, Loy Krathong)
are derived too, and the tests check them against the official dates.

Adding a year: paste its Wan Phra list into WAN_PHRA, add it to
CHINESE_NEW_YEAR, add its BE year to LEAP_MONTH_YEARS if the 8th month is
doubled, and add the official holy days to the test.
"""
from datetime import date, timedelta
import calendar as _cal

# --------------------------------------------------------------------------
# Source data
# --------------------------------------------------------------------------

# Every วันพระ, as (month, day), from calendar.kapook.com. Kapook also lists
# Khao Phansa (the day after Asanha Bucha) as a holy day; that day is NOT a
# moon phase, so _phases() drops any date one day after the one before it.
WAN_PHRA = {
    2026: [(1, 3), (1, 11), (1, 18), (1, 26), (2, 2), (2, 10), (2, 16), (2, 24),
           (3, 3), (3, 11), (3, 18), (3, 26), (4, 2), (4, 10), (4, 16), (4, 24),
           (5, 1), (5, 9), (5, 16), (5, 24), (5, 31), (6, 8), (6, 14), (6, 22),
           (6, 29), (7, 7), (7, 14), (7, 22), (7, 29), (8, 6), (8, 13), (8, 21),
           (8, 28), (9, 5), (9, 11), (9, 19), (9, 26), (10, 4), (10, 11),
           (10, 19), (10, 26), (11, 3), (11, 9), (11, 17), (11, 24), (12, 2),
           (12, 9), (12, 17), (12, 24)],
    2027: [(1, 1), (1, 7), (1, 15), (1, 22), (1, 30), (2, 6), (2, 14), (2, 21),
           (3, 1), (3, 7), (3, 15), (3, 22), (3, 30), (4, 6), (4, 14), (4, 21),
           (4, 29), (5, 5), (5, 13), (5, 20), (5, 28), (6, 4), (6, 12), (6, 19),
           (6, 27), (7, 3), (7, 11), (7, 18), (7, 19), (7, 26), (8, 2), (8, 10),
           (8, 17), (8, 25), (8, 31), (9, 8), (9, 15), (9, 23), (9, 30), (10, 8),
           (10, 15), (10, 23), (10, 29), (11, 6), (11, 13), (11, 21), (11, 28),
           (12, 6), (12, 13), (12, 21), (12, 27)],
    2028: [(1, 4), (1, 11), (1, 19), (1, 26), (2, 3), (2, 10), (2, 18), (2, 24),
           (3, 3), (3, 10), (3, 18), (3, 25), (4, 2), (4, 9), (4, 17), (4, 23),
           (5, 1), (5, 8), (5, 16), (5, 23), (5, 31), (6, 7), (6, 15), (6, 21),
           (6, 29), (7, 6), (7, 7), (7, 14), (7, 21), (7, 29), (8, 5), (8, 13),
           (8, 19), (8, 27), (9, 3), (9, 11), (9, 18), (9, 26), (10, 3),
           (10, 11), (10, 17), (10, 25), (11, 1), (11, 9), (11, 16), (11, 24),
           (12, 1), (12, 9), (12, 15), (12, 23), (12, 30)],
}

YEARS = sorted(WAN_PHRA)

# One full moon whose lunar month is known: 3 Jan 2026 is ขึ้น 15 ค่ำ เดือน 2
# (Makha Bucha, 3 Mar 2026, is the full moon of month 4 two moons later).
ANCHOR_FULL_MOON = date(2026, 1, 3)
ANCHOR_MONTH = 2

# BE years whose lunar calendar has two 8th months (อธิกมาส, "เดือน 8 สองหน").
# 2569 is one: Khao Phansa 2569 is "แรม 1 ค่ำ เดือน 8 หลัง". In such a year
# Makha Bucha moves to month 4 and Visakha Bucha to month 7.
LEAP_MONTH_YEARS = {2569}

# Chinese New Year follows the Chinese lunar calendar, not the Thai one.
CHINESE_NEW_YEAR = {2026: date(2026, 2, 17), 2027: date(2027, 2, 6),
                    2028: date(2028, 1, 26)}

BE_OFFSET = 543  # Buddhist Era year = Gregorian year + 543

THAI_MONTHS = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
               'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
THAI_WEEKDAYS = ['อา.', 'จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.']      # Sunday first
ENGLISH_WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

# The three kinds of event; the Buddhist view leaves out 'christian'.
CATEGORIES = {
    'buddhist': 'Buddhist',
    'thai': 'Thai',
    'christian': 'Christian & Western',
}

# --------------------------------------------------------------------------
# Moon days
# --------------------------------------------------------------------------

# The four Wan Phra phases in the order they always come, and the gap (in
# days) from each phase to the NEXT one. Waning 8 -> new moon is 6 days in a
# 29-day month (new moon is แรม 14 ค่ำ) and 7 in a 30-day month (แรม 15 ค่ำ).
PHASES = ['waxing8', 'full', 'waning8', 'new']
GAP_TO_NEXT = {'waxing8': {7}, 'full': {8}, 'waning8': {6, 7}, 'new': {8}}
MOON_ICON = {'waxing8': '🌓', 'full': '🌕', 'waning8': '🌗', 'new': '🌑'}
PHASE_ENGLISH = {'waxing8': 'First-quarter moon', 'full': 'Full moon',
                 'waning8': 'Last-quarter moon', 'new': 'New moon'}


def _all_wan_phra():
    """Every listed holy day, oldest first, as dates (Khao Phansa removed)."""
    days = sorted(date(y, m, d) for y, md in WAN_PHRA.items() for m, d in md)
    kept = []
    for d in days:
        if kept and (d - kept[-1]).days == 1:
            continue                      # Khao Phansa, not a moon phase
        kept.append(d)
    return kept


def _phases():
    """{date: phase} for every Wan Phra.

    3 Jan 2026 is a full moon, which fixes where the cycle starts; after that
    each phase is simply the next one in PHASES. A gap that doesn't fit the
    phase means the table has a typo, so it raises rather than guess.
    """
    days = _all_wan_phra()
    start = PHASES.index('full') - days.index(ANCHOR_FULL_MOON)
    out = {}
    for i, d in enumerate(days):
        phase = PHASES[(start + i) % 4]
        if i + 1 < len(days):
            gap = (days[i + 1] - d).days
            if gap not in GAP_TO_NEXT[phase]:
                raise ValueError('Wan Phra table: {} ({}) is {} days before the '
                                 'next holy day'.format(d, phase, gap))
        out[d] = phase
    return out


def _full_moon_months():
    """{full-moon date: (lunar month, is_second_eighth)}.

    Count full moons from the anchor. After month 8, a leap-month year repeats
    8 (the "second 8th", เดือน 8 หลัง) before going on to 9. The BE year of a
    month is the Gregorian year of its full moon + 543, which is right for
    month 8 — the only month that matters for the leap check.
    """
    fulls = sorted(d for d, p in _phases().items() if p == 'full')
    i0 = fulls.index(ANCHOR_FULL_MOON)
    out = {ANCHOR_FULL_MOON: (ANCHOR_MONTH, False)}
    month, second = ANCHOR_MONTH, False
    for d in fulls[i0 + 1:]:
        if month == 8 and not second and (d.year + BE_OFFSET) in LEAP_MONTH_YEARS:
            second = True
        else:
            month, second = month % 12 + 1, False
        out[d] = (month, second)
    month, second = ANCHOR_MONTH, False
    for d in reversed(fulls[:i0]):
        # Walking backwards; no leap year falls before the anchor in the table.
        month = (month - 2) % 12 + 1
        out[d] = (month, False)
    return out


_CACHE = {}


def lunar_days():
    """{date: moon-day dict} for every day the table covers.

    Each value: waxing (True/False), day (1-15), month (1-12), second_eighth,
    phase (one of PHASES, or None), and the Thai/English labels.
    """
    if 'days' in _CACHE:
        return _CACHE['days']
    phases = _phases()
    months = _full_moon_months()
    fulls = sorted(months)
    news = sorted(d for d, p in phases.items() if p == 'new')
    out = {}
    first, last = date(YEARS[0], 1, 1), date(YEARS[-1], 12, 31)
    d = first
    while d <= last:
        # The month is that of the full moon in the same waxing-to-waning
        # cycle: the next full moon if we're waxing, the last one if waning.
        prev_new = max((n for n in news if n < d), default=None)
        prev_full = max((f for f in fulls if f <= d), default=None)
        next_full = min((f for f in fulls if f >= d), default=None)
        waxing = (prev_full is None or (prev_new is not None and prev_new > prev_full)
                  or d == next_full)
        if waxing and next_full is not None:
            day = 15 - (next_full - d).days
            month, second = months[next_full]
        elif waxing:                       # past the last full moon in the table
            day = (d - prev_new).days
            month, second = months[prev_full]
            month, second = month % 12 + 1, False
        else:
            day = (d - prev_full).days
            month, second = months[prev_full]
        month_th = 'เดือน {}{}'.format(month, ' หลัง' if second else '')
        month_en = 'month {}{}'.format(month, ' (second)' if second else '')
        out[d] = {
            'waxing': waxing, 'day': day, 'month': month,
            'second_eighth': second, 'phase': phases.get(d),
            'short_th': '{} {}'.format('ขึ้น' if waxing else 'แรม', day),
            'label_th': '{} {} ค่ำ {}'.format('ขึ้น' if waxing else 'แรม', day, month_th),
            'label_en': '{} {}, lunar {}'.format('Waxing' if waxing else 'Waning',
                                                 day, month_en),
        }
        d += timedelta(days=1)
    _CACHE['days'] = out
    return out


def _full_moon_of(year, month, second=False):
    """The Gregorian date of the full moon of a lunar month, in that year."""
    for d, (m, s) in _full_moon_months().items():
        if d.year == year and m == month and s == second:
            return d
    return None


# --------------------------------------------------------------------------
# Events
# --------------------------------------------------------------------------

def easter(year):
    """Western Easter Sunday (the Anonymous Gregorian algorithm — exact)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def _nth_weekday(year, month, weekday, n):
    """The nth (1-based) weekday (Mon=0) of a month."""
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _ev(day, category, english, thai=None, note=None, end=None):
    return {'date': day, 'end': end, 'category': category, 'english': english,
            'thai': thai, 'note': note}


def events(year):
    """Every event in a Gregorian year, sorted by date."""
    leap = (year + BE_OFFSET) in LEAP_MONTH_YEARS
    ev = []

    # ---- Buddhist (lunar, worked out from the Wan Phra table) ----
    makha = _full_moon_of(year, 4 if leap else 3)
    visakha = _full_moon_of(year, 7 if leap else 6)
    asanha = _full_moon_of(year, 8, second=leap)
    ok_phansa = _full_moon_of(year, 11)
    loy = _full_moon_of(year, 12)
    if makha:
        ev.append(_ev(makha, 'buddhist', 'Makha Bucha Day', 'วันมาฆบูชา',
                      'The Buddha’s teaching to 1,250 arahants who came '
                      'without being called.'))
    if visakha:
        ev.append(_ev(visakha, 'buddhist', 'Visakha Bucha Day', 'วันวิสาขบูชา',
                      'The Buddha’s birth, awakening and passing away.'))
        ev.append(_ev(visakha + timedelta(days=8), 'buddhist', 'Atthami Bucha Day',
                      'วันอัฏฐมีบูชา', 'The Buddha’s cremation, eight days '
                      'after Visakha Bucha.'))
    if asanha:
        ev.append(_ev(asanha, 'buddhist', 'Asanha Bucha Day', 'วันอาสาฬหบูชา',
                      'The Buddha’s first teaching, to the five ascetics.'))
        ev.append(_ev(asanha + timedelta(days=1), 'buddhist',
                      'Khao Phansa (Rains Retreat begins)', 'วันเข้าพรรษา',
                      'Monks stay in one monastery for the three months of '
                      'the rains.'))
    if ok_phansa:
        ev.append(_ev(ok_phansa, 'buddhist', 'Ok Phansa (Rains Retreat ends)',
                      'วันออกพรรษา'))
        ev.append(_ev(ok_phansa + timedelta(days=1), 'buddhist', 'Tak Bat Devo',
                      'วันตักบาตรเทโว', 'Alms-giving for the Buddha’s return '
                      'from teaching in the heavens.'))
        if loy:
            ev.append(_ev(ok_phansa + timedelta(days=1), 'buddhist',
                          'Kathina season', 'เทศกาลทอดกฐิน',
                          'A month for offering robes to monks after the Rains.',
                          end=loy))
    for d, phase in _phases().items():
        if d.year == year:
            ev.append(_ev(d, 'buddhist', 'Wan Phra — ' + PHASE_ENGLISH[phase].lower(),
                          'วันพระ', None))

    # ---- Thai ----
    ev += [
        _ev(date(year, 1, 1), 'thai', "New Year's Day", 'วันขึ้นปีใหม่'),
        _ev(_nth_weekday(year, 1, 5, 2), 'thai', "Children's Day", 'วันเด็ก',
            'The second Saturday of January.'),
        _ev(date(year, 1, 16), 'thai', "Teachers' Day", 'วันครู'),
        _ev(date(year, 4, 6), 'thai', 'Chakri Day', 'วันจักรี',
            'Founding of the Chakri dynasty, 1782.'),
        _ev(date(year, 4, 13), 'thai', 'Songkran (Thai New Year)', 'สงกรานต์',
            'Water blessings, family visits and merit-making.',
            end=date(year, 4, 15)),
        _ev(date(year, 5, 1), 'thai', 'Labour Day', 'วันแรงงาน'),
        _ev(date(year, 5, 4), 'thai', 'Coronation Day', 'วันฉัตรมงคล'),
        _ev(date(year, 6, 3), 'thai', "Queen Suthida's Birthday"),
        _ev(date(year, 7, 28), 'thai', "King Vajiralongkorn's Birthday"),
        _ev(date(year, 8, 12), 'thai', "Mother's Day (Thailand)", 'วันแม่',
            'The birthday of Queen Mother Sirikit.'),
        _ev(date(year, 10, 13), 'thai', 'King Bhumibol Memorial Day'),
        _ev(date(year, 10, 23), 'thai', 'Chulalongkorn Day', 'วันปิยมหาราช'),
        _ev(date(year, 12, 5), 'thai', "Father's Day (Thailand)", 'วันพ่อ',
            'The birthday of King Bhumibol.'),
        _ev(date(year, 12, 10), 'thai', 'Constitution Day', 'วันรัฐธรรมนูญ'),
        _ev(date(year, 12, 31), 'thai', "New Year's Eve", 'วันสิ้นปี'),
    ]
    if year in CHINESE_NEW_YEAR:
        ev.append(_ev(CHINESE_NEW_YEAR[year], 'thai', 'Chinese New Year', 'ตรุษจีน'))
    if loy:
        ev.append(_ev(loy, 'thai', 'Loy Krathong', 'ลอยกระทง',
                      'Floating krathong on rivers under the full moon of '
                      'the 12th lunar month.'))

    # ---- Christian & Western ----
    e = easter(year)
    christmas = date(year, 12, 25)
    advent = christmas - timedelta(days=christmas.isoweekday() % 7 + 21)
    ev += [
        _ev(date(year, 1, 6), 'christian', 'Epiphany'),
        _ev(date(year, 2, 14), 'christian', "Valentine's Day"),
        _ev(e - timedelta(days=46), 'christian', 'Ash Wednesday',
            note='The start of Lent.'),
        _ev(e - timedelta(days=21), 'christian', 'Mothering Sunday (UK)'),
        _ev(e - timedelta(days=7), 'christian', 'Palm Sunday'),
        _ev(e - timedelta(days=2), 'christian', 'Good Friday'),
        _ev(e, 'christian', 'Easter Sunday'),
        _ev(e + timedelta(days=1), 'christian', 'Easter Monday'),
        _ev(e + timedelta(days=39), 'christian', 'Ascension Day'),
        _ev(e + timedelta(days=49), 'christian', 'Pentecost'),
        _ev(_nth_weekday(year, 6, 6, 3), 'christian', "Father's Day (UK & US)"),
        _ev(date(year, 10, 31), 'christian', 'Halloween'),
        _ev(date(year, 11, 1), 'christian', "All Saints' Day"),
        _ev(date(year, 11, 2), 'christian', "All Souls' Day"),
        _ev(advent, 'christian', 'Advent Sunday',
            note='Four Sundays before Christmas.'),
        _ev(date(year, 12, 24), 'christian', 'Christmas Eve'),
        _ev(christmas, 'christian', 'Christmas Day'),
        _ev(date(year, 12, 26), 'christian', 'Boxing Day'),
    ]
    order = list(CATEGORIES)
    ev.sort(key=lambda x: (x['date'], order.index(x['category']), x['english']))
    return ev


# --------------------------------------------------------------------------
# The month grid the template draws
# --------------------------------------------------------------------------

def month_view(year, month, mode):
    """Everything the template needs for one month.

    mode 'gregorian' shows every event; 'buddhist' shows Thai and Buddhist
    events only, with Thai names, the BE year and each day's moon day.
    """
    buddhist = mode == 'buddhist'
    wanted = ('buddhist', 'thai') if buddhist else tuple(CATEGORIES)
    first, last = date(year, month, 1), date(year, month, _cal.monthrange(year, month)[1])
    month_events = [e for e in events(year) if e['category'] in wanted
                    and e['date'] <= last and (e['end'] or e['date']) >= first]

    moons = lunar_days()
    by_day = {}
    for e in month_events:
        # A month-long season (Kathina) would fill every cell; it goes in the
        # list under the grid instead, marked on its first day only.
        if e['end'] and (e['end'] - e['date']).days > 7:
            if first <= e['date'] <= last:
                by_day.setdefault(e['date'], []).append(e)
            continue
        d = max(e['date'], first)
        while d <= min(e['end'] or e['date'], last):
            by_day.setdefault(d, []).append(e)
            d += timedelta(days=1)

    weeks = []
    for week in _cal.Calendar(firstweekday=6).monthdatescalendar(year, month):
        weeks.append([{
            'date': d, 'in_month': d.month == month,
            'moon': moons.get(d),
            # Wan Phra shows as the moon icon; leave it out of the cell's
            # event list so a cell doesn't fill with "Wan Phra" four times.
            'events': [e for e in by_day.get(d, []) if e['thai'] != 'วันพระ'],
        } for d in week])

    month_moons = [moons[d] for d in sorted(moons) if first <= d <= last]
    lunar_months = []
    for m in month_moons:
        key = (m['month'], m['second_eighth'])
        if key not in lunar_months:
            lunar_months.append(key)

    return {
        'year': year, 'month': month, 'mode': mode,
        'be_year': year + BE_OFFSET,
        'month_name': _cal.month_name[month],
        'thai_month': THAI_MONTHS[month - 1],
        'weekdays': THAI_WEEKDAYS if buddhist else ENGLISH_WEEKDAYS,
        'weeks': weeks,
        'events': [e for e in month_events if e['thai'] != 'วันพระ'],
        'wan_phra': [(d, moons[d]) for d in sorted(moons)
                     if first <= d <= last and moons[d]['phase']],
        'lunar_months': ['เดือน {}{}'.format(m, ' หลัง' if s else '')
                         for m, s in lunar_months],
        'leap_year': (year + BE_OFFSET) in LEAP_MONTH_YEARS,
    }


def spellings(event_list):
    """{thai: ThaiBridge Spelling} for the events' Thai names that the site
    already teaches. Names it doesn't teach get no romanisation rather than
    an unreviewed one."""
    import paiboon_lookup                 # late: it indexes the whole app
    out = {}
    for thai in {e['thai'] for e in event_list if e['thai']}:
        match = next((h for h in paiboon_lookup.search(thai, limit=40)
                      if h.thai == thai), None)
        if match:
            out[thai] = match.paiboon
    return out


def clamp(year, month):
    """Keep a requested month inside the years the table covers."""
    if year < YEARS[0]:
        return YEARS[0], 1
    if year > YEARS[-1]:
        return YEARS[-1], 12
    return year, min(max(month, 1), 12)


def neighbours(year, month):
    """(previous (y, m) or None, next (y, m) or None) within the table."""
    prev = (year, month - 1) if month > 1 else (year - 1, 12)
    nxt = (year, month + 1) if month < 12 else (year + 1, 1)
    return (prev if prev[0] >= YEARS[0] else None,
            nxt if nxt[0] <= YEARS[-1] else None)
