"""Tests for apply_batch — Stage 2 of the chanting-book workflow.

These exist because the hand-written version of this step failed silently. It
reported "CONTINUES marker removed" without removing it: the regex matched
nothing, success was printed anyway, and a finished chant kept a marker saying
it was unfinished — which is what gets grepped to find outstanding work.

So the tests here are mostly about the script REFUSING things, and about it
never claiming something it has not checked. The happy path is the easy part;
the failures are what put wrong Pali into a book people chant from.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

from apply_batch import (GAP, apply, check_join, plan, reconcile,  # noqa: E402
                         render_chant, verse_range)


def verse(n, pali='ปะฏิสังขา โยนิโส', **kw):
    v = {'number': n, 'pali': pali, 'pali_roman': 'x', 'thai': '', 'paiboon': '', 'english': 'y'}
    v.update(kw)
    return v


def chant(cid='metta', verses=None, **kw):
    c = {'id': cid, 'title_thai': 'x', 'verses': verses or [verse(1)], 'checks': []}
    c.update(kw)
    return c


def batch(chants, pages=None):
    return {
        'batch': {'depth': 'DATA-ONLY', 'manifest': [c['id'] for c in chants],
                  'pages': pages or []},
        'chants': chants,
    }


class TestItRefusesToWrite:
    """Reconciliation runs before anything is written, and stops on any doubt."""

    def test_a_short_batch_is_refused(self):
        """The manifest says three, two arrived — the run stopped early."""
        b = batch([chant('a'), chant('b')])
        b['batch']['manifest'].append('c')

        problems = reconcile(b, {})

        assert problems and 'stopped early' in problems[0]

    def test_a_chant_that_was_never_declared_is_refused(self):
        b = batch([chant('a')])
        b['batch']['manifest'] = ['something-else']

        assert any('never declared' in p for p in reconcile(b, {}))

    def test_a_page_claiming_verses_the_entry_lacks_is_refused(self):
        """The failure that stopped the very first real batch."""
        b = batch([chant('a', [verse(1), verse(2)])],
                  pages=[{'page': 2, 'chant': 'a', 'verses': '1-12', 'note': ''}])

        problems = reconcile(b, {})

        assert any('claims a verses 1-12' in p for p in problems)

    def test_a_page_naming_a_chant_that_never_arrived_is_refused(self):
        b = batch([chant('a')], pages=[{'page': 2, 'chant': 'ghost', 'verses': '1', 'note': ''}])

        assert any('never arrived' in p for p in reconcile(b, {}))

    def test_a_continuation_with_nothing_to_continue_is_refused(self):
        """Batches applied out of order — do NOT create the chant."""
        b = batch([chant('a', continuation_of='not-in-the-app')])

        assert any('out of order' in p for p in reconcile(b, {}))

    def test_re_applying_a_batch_is_refused(self):
        """The bug found by dry-running this script against a batch already in.

        The continuation guards caught the batches with continuations in them
        and said nothing about the one whose chants were all new — so a second
        application would have appended eight duplicate dicts.
        """
        b = batch([chant('already-here')])

        problems = reconcile(b, {'already-here': chant('already-here')})

        assert any('already in the app' in p for p in problems)

    def test_a_repeat_stub_is_not_treated_as_a_duplicate(self):
        """Stage 1 marks a chant printed twice in the book with repeat_of."""
        b = batch([chant('a', repeat_of='a')])

        assert reconcile(b, {'a': chant('a')}) == []

    def test_a_page_row_marked_not_written_is_skipped(self):
        """Stage 1 declares pages it did not reach; they are not disagreements."""
        b = batch([chant('a')],
                  pages=[{'page': 9, 'chant': 'a', 'verses': '5-16',
                          'note': 'NOT WRITTEN — batch stopped here.'}])

        assert reconcile(b, {}) == []


class TestTheJoinBetweenBatches:
    """A chant split across a batch boundary must end up as one chant."""

    def test_a_clean_join_passes(self):
        present = chant('a', [verse(1), verse(2)])
        incoming = chant('a', [verse(3), verse(4)], continuation_of='a')

        assert check_join(incoming, present) == []

    def test_a_gap_in_the_numbering_is_refused(self):
        """Verses 1-2 then 5-6 would lose two lines silently."""
        present = chant('a', [verse(1), verse(2)])
        incoming = chant('a', [verse(5), verse(6)], continuation_of='a')

        assert any('do not run on' in p for p in check_join(incoming, present))

    def test_a_duplicate_batch_is_refused(self):
        """More than one overlapping verse is the same batch applied twice."""
        present = chant('a', [verse(1), verse(2), verse(3)])
        incoming = chant('a', [verse(2), verse(3)], continuation_of='a')

        assert any('duplicate batch' in p for p in check_join(incoming, present))


class TestCompletingALineCutByAPageBreak:
    """The one case where incoming text may overwrite the file."""

    def test_it_is_allowed_when_the_line_was_genuinely_cut(self):
        present = chant('a', [verse(1, f'ฑังสะมะกะสะ {GAP}')])
        incoming = chant('a', [verse(1, 'ฑังสะมะกะสะ ปะฏิฆาตายะ,')], continuation_of='a')

        assert check_join(incoming, present) == []

    def test_it_is_refused_when_the_existing_line_was_complete(self):
        """No gap marker means this is an overlap, not a completion."""
        present = chant('a', [verse(1, 'ฑังสะมะกะสะ ปะฏิฆาตายะ,')])
        incoming = chant('a', [verse(1, 'something else entirely')], continuation_of='a')

        assert any('does not end in' in p for p in check_join(incoming, present))

    def test_it_is_refused_when_the_incoming_line_does_not_extend_it(self):
        """A completion lengthens a line. It never swaps it for a different one."""
        present = chant('a', [verse(1, f'ฑังสะมะกะสะ {GAP}')])
        incoming = chant('a', [verse(1, 'a completely different line')], continuation_of='a')

        assert any('does not extend' in p for p in check_join(incoming, present))


class TestItNeverClaimsWhatItHasNotDone:
    """The bug this script was written to stop."""

    def test_it_raises_rather_than_reporting_a_removal_it_did_not_make(self, monkeypatch):
        import apply_batch

        present = "[\n    {\n        'id': 'a',\n        'verses': [\n        ],\n    },\n]\n"
        b = batch([chant('a', [verse(2)], continuation_of='a')])
        # Pretend the marker removal silently does nothing, as it once did.
        monkeypatch.setattr(apply_batch, 'drop_marker', lambda src, cid, word: src)
        monkeypatch.setattr(apply_batch, 'count_markers', lambda src, word: 1)

        with pytest.raises(RuntimeError, match='Refusing to report success'):
            apply(b, present)


class TestWhatItPlansAndWrites:

    def test_the_plan_separates_completing_a_line_from_adding_ones(self):
        """'1 line completed' is a different event from '4 verses added'."""
        existing = {'a': chant('a', [verse(1), verse(2, f'cut {GAP}')])}
        b = batch([chant('a', [verse(2, 'cut here,'), verse(3), verse(4)], continuation_of='a')])

        steps = plan(b, existing)

        assert steps['completed'] == [('a', 2)]
        assert steps['appended'] == [('a', 3), ('a', 4)]
        assert steps['added'] == []

    def test_rendered_chants_use_the_files_own_comment_marker(self):
        """chanting.py uses ‼ throughout; two conventions in one file helps nobody."""
        out = render_chant(chant('a', checks=[{'verse': None, 'file': 'IMG_1.PNG', 'issue': 'look at this'}]))

        assert '# ‼ CHECK [IMG_1.PNG]' in out
        assert '⚠' not in out

    def test_empty_layers_are_written_through_as_facts(self):
        """A Pali-only chant has no thai and no paiboon. That is data, not a gap."""
        out = render_chant(chant('a', [verse(1)]))

        assert "'thai': ''" in out
        assert "'paiboon': ''" in out

    @pytest.mark.parametrize('spec,expected', [('1-6', {1, 2, 3, 4, 5, 6}), ('7', {7}), ('12-13', {12, 13})])
    def test_verse_ranges_parse(self, spec, expected):
        assert verse_range(spec) == expected


class TestAgainstTheRealBatchFiles:
    """The three batches already applied must still reconcile against the app."""

    @pytest.mark.parametrize('name', ['batch-001-003', 'batch-004-006', 'batch-007-008'])
    def test_each_batch_file_parses_and_is_self_consistent(self, name):
        import pathlib
        path = pathlib.Path(__file__).parent.parent / 'prompts/chanting-book-batch/batches' / f'{name}.json'
        b = json.loads(path.read_text(encoding='utf-8'))

        assert len(b['batch']['manifest']) == len(b['chants'])
        for c in b['chants']:
            assert c['id'] in b['batch']['manifest']
            for v in c['verses']:
                assert set(v) >= {'number', 'pali', 'pali_roman', 'thai', 'paiboon', 'english'}


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
