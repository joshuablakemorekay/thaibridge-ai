"""Tests for check_pages — does the app page match the printed page?

The script exists because nothing compared the batch files to what was
written, and two pages went live showing half of what the book prints. So
these tests are almost entirely about it FAILING: a checker that cannot be
made to fail is indistinguishable from one that never looks, and this repo has
already had one of those.
"""
import json
import os
import sys
import types

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import chanting                                            # noqa: E402
from check_pages import check, is_completion                # noqa: E402


def verse(n, pali='ปะฏิสังขา', english='y', **kw):
    v = {'number': n, 'pali': pali, 'pali_roman': 'x', 'thai': '',
         'paiboon': '', 'english': english}
    v.update(kw)
    return v


def app(chants, page_blocks=()):
    """A stand-in for the chanting module holding just a fixture book.

    It borrows the REAL build_page_index, which takes its data as arguments,
    so these tests exercise the same placement logic the app serves.
    """
    return types.SimpleNamespace(
        CHANTS=chants,
        build_page_index=lambda: chanting.build_page_index(chants,
                                                           list(page_blocks)))


def batch_file(tmp_path, pages, chants, name='batch-002-002.json'):
    path = tmp_path / name
    path.write_text(json.dumps({
        'batch': {'depth': 'DATA-ONLY',
                  'manifest': [c['id'] for c in chants],
                  'pages': pages},
        'chants': chants,
        'batch_status': {},
    }, ensure_ascii=False), encoding='utf-8')
    return [str(path)]


def row(page=2, chant='a', verses='1-2', **kw):
    r = {'page': page, 'file': 'IMG_0001.PNG', 'chant': chant,
         'verses': verses, 'starts_here': True, 'note': ''}
    r.update(kw)
    return r


class TestItPasses:

    def test_a_page_that_matches_its_photograph(self, tmp_path):
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1), verse(2)]}]
        files = batch_file(tmp_path, [row()], chants)

        faults, counts = check(app(chants), files)

        assert not faults
        assert counts['verses'] == 2

    def test_a_block_the_app_shows_is_accounted_for(self, tmp_path):
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1)]}]
        blocks = [{'page': 2, 'blocks': [{'type': 'heading', 'thai': 'ระเบียบ',
                                          'english': 'The Order'}]}]
        files = batch_file(tmp_path, [row(verses='1', blocks=[
            {'type': 'heading', 'thai': 'ระเบียบ', 'english': 'The Order'}])],
            chants)

        faults, _ = check(app(chants, blocks), files)

        assert not faults

    def test_a_page_recorded_by_blocks_alone_counts_as_recorded(self, tmp_path):
        """Page 63 — the notes to the evening service, and no chant on it.

        A blocks-only page makes no verse claim, so counting claims alone
        reported it as having no batch record while its blocks were being
        compared and passing. `unrecorded` is the one number here meant to
        stay still, so a fully read page turning up in it teaches everyone
        to stop reading it.
        """
        block = {'type': 'item', 'number': 'ก', 'thai': 'ข้อความ',
                 'english': 'text'}
        files = batch_file(tmp_path,
                           [row(page=63, chant='', verses='none',
                                blocks=[block])],
                           [])

        faults, counts = check(app([], [{'page': 63, 'blocks': [block]}]),
                               files)

        assert not faults
        assert counts['blocks'] == 1
        assert 63 not in counts['unrecorded']


class TestItCatchesTheThingsThatWentWrongBefore:

    def test_a_block_the_page_prints_and_the_app_drops(self, tmp_path):
        """Pages 7 and 8, exactly: recorded by stage 1, written nowhere."""
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1)]}]
        files = batch_file(tmp_path, [row(verses='1', service_closing='จบพิธีทำวัตรเช้า')],
                           chants)

        faults, _ = check(app(chants), files)

        assert any('does not show' in p for p in faults[2])

    def test_a_verse_the_app_puts_on_another_page(self, tmp_path):
        """A page marker one verse out moves every verse after it."""
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1), verse(2, page=3)]}]
        files = batch_file(tmp_path, [row(verses='1-2')], chants)

        faults, _ = check(app(chants), files)

        assert any('the app puts it on page 3' in p for p in faults[2])

    def test_a_verse_the_page_prints_and_the_app_lacks(self, tmp_path):
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1)]}]
        files = batch_file(tmp_path, [row(verses='1-2')], chants)

        faults, _ = check(app(chants), files)

        assert any('not in the app at all' in p for p in faults[2])

    def test_text_that_drifted_from_the_record(self, tmp_path):
        """The batch recorded one line; the app holds another."""
        recorded = [{'id': 'a', 'verses': [verse(1, pali='ยัส์มิง ปะเทเส')],
                     'checks': []}]
        in_app = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1, pali='ยัส์มิง ปะเทเส กัปเปติ')]}]
        files = batch_file(tmp_path, [row(verses='1')], recorded)

        faults, _ = check(app(in_app), files)

        assert any('differs from what this page recorded' in p
                   for p in faults[2])


class TestALineCutByAPageBreak:
    """The rule that makes the report readable, and it is checked not waived."""

    def test_a_completed_line_belongs_to_the_page_it_starts_on(self, tmp_path):
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1, pali='ฑังสะมะกะสะ ปะฏิฆาตายะ,',
                                    english='to ward off the touch,')]}]
        cut = [dict(v) for v in chants[0]['verses']]
        cut[0]['pali'] = 'ฑังสะมะกะสะ […]'
        cut[0]['english'] = 'to ward off […]'
        files = batch_file(tmp_path, [row(page=2, verses='1')],
                           [{'id': 'a', 'verses': cut, 'checks': []}])
        later = batch_file(tmp_path, [row(page=3, verses='1')], chants,
                           name='batch-003-003.json')

        faults, _ = check(app(chants), files + later)

        assert not faults

    def test_a_completion_that_does_not_continue_the_line_is_a_fault(self, tmp_path):
        """A different line replacing a partial one means the two batches
        disagree about what the book says, which is worth finding."""
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1, pali='something entirely other')]}]
        cut = [verse(1, pali='ฑังสะมะกะสะ […]')]
        files = batch_file(tmp_path, [row(page=2, verses='1')],
                           [{'id': 'a', 'verses': cut, 'checks': []}])

        faults, _ = check(app(chants), files)

        assert any('does not continue it' in p for p in faults[2])

    def test_two_pages_claiming_one_whole_verse_is_an_overlap(self, tmp_path):
        chants = [{'id': 'a', 'page_start': 2, 'title_thai': 'x',
                   'verses': [verse(1)]}]
        files = batch_file(tmp_path, [row(page=2, verses='1')], chants)
        later = batch_file(tmp_path, [row(page=3, verses='1')], chants,
                           name='batch-003-003.json')

        faults, _ = check(app(chants), files + later)

        assert any('two batches overlap' in p for p in faults[2])

    @pytest.mark.parametrize('recorded,written,expected', [
        ('นะ […]', 'นะ เหวัง วัตตัพเพ.', True),
        ('นะ […]', 'เหวัง วัตตัพเพ.', False),
        ('นะ เหวัง', 'นะ เหวัง วัตตัพเพ.', False),   # never cut, never healed
    ])
    def test_what_counts_as_healing_a_cut_line(self, recorded, written, expected):
        assert is_completion(recorded, written) is expected


def test_the_real_book_matches_its_own_photographs():
    """The whole point, run against the real data.

    Kept as a test as well as a script so it cannot rot: a page going out of
    step with its photograph now breaks the suite rather than waiting for
    somebody to run a checker by hand.
    """
    import glob

    files = sorted(glob.glob(os.path.join(
        ROOT, 'prompts', 'chanting-book-batch', 'batches', '*.json')))
    faults, counts = check(chanting, files)

    assert counts['rows'] > 80, 'the batch files stopped being read'
    assert not faults, '\n'.join(f'page {p}: {q}'
                                 for p, qs in sorted(faults.items())
                                 for q in qs)
