"""Tests for the three-volume plan, the occasion and day guides, and the
Amaravati chants (Pra Kru Bob's request, 2026-11-12).

What these protect: that splitting the book into volumes never loses or
doubles a chant and never changes the temple book's order; that every chant
a guide points to exists, so a reader is never sent to a missing page; and
that the Amaravati chants stay out of chanting.CHANTS, which is the temple
book alone. None of this runs Chrome.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import chanting  # noqa: E402
import chanting_amaravati  # noqa: E402
import chanting_volumes as plan  # noqa: E402
import build_chanting_print as build  # noqa: E402

ALL_IDS = {c['id'] for c in chanting.CHANTS} | {c['id'] for c in chanting_amaravati.AMARAVATI_CHANTS}


def _volume_books():
    return build.make_books(volumes=True)


def test_every_part_has_a_volume():
    parts = build.number_parts(build.book_parts())
    numbers = {p['number'] for p in parts if p.get('number')}
    assert numbers == set(plan.PART_VOLUME)
    assert set(plan.PART_VOLUME.values()) <= {v['number'] for v in plan.VOLUMES}


def test_volumes_hold_every_chant_exactly_once():
    ids = [c['id'] for b in _volume_books() for p in b['parts'] for c in p['chants']]
    assert sorted(ids) == sorted(c['id'] for c in chanting.CHANTS)


def test_each_volume_keeps_the_temple_order():
    order = [c['id'] for c in chanting.chants_in_book_order()]
    for book in _volume_books():
        ids = [c['id'] for p in book['parts'] for c in p['chants']]
        assert ids == sorted(ids, key=order.index), book['key']


def test_split_part_is_marked_continued():
    books = {b['volume']['number']: b for b in _volume_books()}
    first = [p for p in books[1]['parts'] if p['number'] == 7]
    rest = [p for p in books[2]['parts'] if p['number'] == 7]
    assert first and rest
    assert not first[0]['continued'] and rest[0]['continued']
    assert rest[0]['chants'][0]['id'] in plan.SPLITS


def test_pra_kru_bobs_chants_are_in_volume_one():
    vol1 = {c['id'] for p in _volume_books()[0]['parts'] for c in p['chants']}
    for cid in ('mangala-suttam-pathamam', 'bojjhanga-parittam-dasamam',
                'jayamangala-atthaka-gatha', 'pattidana-gatha', 'thammasangkhani-matika-patho'):
        assert cid in vol1, cid


def test_owen_and_amaravati_each_in_one_volume():
    books = _volume_books()
    assert sum(bool(b['owen_chants']) for b in books) == 1
    assert sum(bool(b['amaravati_chants']) for b in books) == 1


def test_one_volume_edition_is_unchanged_in_order():
    (book,) = build.make_books(volumes=False)
    ids = [c['id'] for p in book['parts'] for c in p['chants']]
    assert ids == [c['id'] for c in chanting.chants_in_book_order()]


def test_guides_point_only_at_real_chants():
    named = plan.occasion_chant_ids() + [d['chant'] for d in plan.DAY_CHANTS]
    named += [cid for _, ids in plan.DAILY_ORDER for cid in ids]
    named += list(plan.SPLITS) + list(plan.CHANT_VOLUME)
    assert [cid for cid in named if cid not in ALL_IDS] == []


def test_day_chants_cover_the_week_with_the_traditional_numbers():
    times = {d['day']: d['times'] for d in plan.DAY_CHANTS}
    assert times == {'Sunday': 6, 'Monday': 15, 'Tuesday': 8, 'Wednesday (day)': 17,
                     'Wednesday (night)': 12, 'Thursday': 19, 'Friday': 21, 'Saturday': 10}


def test_day_chant_first_lines_are_in_their_chant():
    for d in plan.DAY_CHANTS:
        chant = chanting.get_chant(d['chant'])
        text = ' '.join(v.get('pali_roman') or '' for v in chant['verses'])
        assert d['first_line'] in text, d['day']


def test_every_occasion_names_its_source():
    for group in plan.OCCASIONS:
        for item in group['items']:
            assert item['chants'] and item['source'], item['occasion']


def test_amaravati_chants_stay_out_of_the_temple_book():
    temple = {c['id'] for c in chanting.CHANTS}
    for chant in chanting_amaravati.AMARAVATI_CHANTS:
        assert chant['id'] not in temple
        assert chant['id'].startswith('amaravati-')


def test_amaravati_lines_have_thai_script():
    for chant in chanting_amaravati.AMARAVATI_CHANTS:
        assert '[?]' not in chant['leader']['pali']
        for group in chant['groups']:
            assert len(group['pali_thai']) == len(group['pali'])
            assert all(t and '[?]' not in t for t in group['pali_thai']), group['pali']


def test_index_lists_every_chant_once():
    books = _volume_books()
    ids = [e['id'] for e in build.index_entries(books)]
    assert len(ids) == len(set(ids))
    expected = len(chanting.CHANTS) + len(build.OWEN_CHANTS) + len(chanting_amaravati.AMARAVATI_CHANTS)
    assert len(ids) == expected
