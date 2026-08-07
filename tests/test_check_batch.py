"""Tests for check_batch — Stage 1 of the chanting-book workflow.

Stage 2 has had a tested script since the third batch. Stage 1 had nothing: its
self-checks were re-improvised from the prompt each session, so they were only
ever as good as that session's reconstruction of them.

Improvised checkers produced three false results in one afternoon — a report of
"0 checks written" when all twelve were present (a shell had re-encoded the ‼
marker), a duplicate citation that was really a CSS rule, and a page reported
out of order because the search matched by first occurrence and the book prints
the same line three times. None was a data error. A check that cries wolf is
worse than no check, because the next real failure gets waved through.

So these tests are mostly about the checks FIRING on things known to be wrong,
and staying quiet on things that only look wrong: a Pali-only chant with empty
layers, a chant the book carries onto a page not yet photographed, two different
Pali words that share a skeleton.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

from check_batch import (check_blocks, check_checks_are_readable,  # noqa: E402
                         check_depth, check_diacritics, check_layer_keys,
                         check_layers_not_invented, check_line_breaks_agree,
                         check_manifest, check_page_map, check_pages_ascend,
                         check_paiboon, check_pali_untouched,
                         check_printed_numbers, check_shape, skeleton,
                         validate, verse_range)


def verse(n=1, **kw):
    v = {'number': n, 'pali': 'อัชชะ โภนโต', 'pali_roman': 'ajja bhonto',
         'thai': '', 'paiboon': '', 'english': 'Today, venerable sirs'}
    v.update(kw)
    return v


def chant(cid='metta', verses=None, **kw):
    c = {'id': cid, 'title_thai': 'x', 'verses': verses or [verse(1)],
         'checks': [{'verse': None, 'file': 'IMG_0001.PNG', 'issue': 'look'}]}
    c.update(kw)
    return c


def batch(chants=None, pages=None, status=None, **batchkw):
    chants = chants if chants is not None else [chant()]
    b = {'depth': 'DATA-ONLY', 'manifest': [c['id'] for c in chants],
         'pages': pages if pages is not None else
         [{'page': 2, 'file': 'IMG_0001.PNG', 'chant': c['id'],
           'verses': f"1-{len(c['verses'])}" if len(c['verses']) > 1 else '1',
           'note': ''} for c in chants]}
    b.update(batchkw)
    st = {'completed': [c['id'] for c in chants], 'not_started': [],
          'continues': []}
    st.update(status or {})
    return {'batch': b, 'chants': chants, 'batch_status': st}


class TestPaiboonDrift:
    """The failure the romanisation convention most exists to prevent."""

    @pytest.mark.parametrize('bad', ['phrá', 'thâng', 'khǎn', 'thǎng'])
    def test_rtgs_spellings_are_caught(self, bad):
        b = batch([chant(verses=[verse(1, thai='พระ', paiboon=bad)])])

        assert any('Paiboon+ uses' in p for p in check_paiboon(b))

    def test_ng_is_caught_because_paiboon_uses_the_eng(self):
        b = batch([chant(verses=[verse(1, thai='ทั้ง', paiboon='tâng')])])

        assert check_paiboon(b)

    def test_correct_paiboon_passes(self):
        b = batch([chant(verses=[verse(1, thai='พระทั้งขันธ์',
                                       paiboon='prá táŋ kǎn')])])

        assert check_paiboon(b) == []

    def test_it_looks_at_the_invitation_too(self):
        """Drift does not confine itself to verses."""
        b = batch([chant(invitation={'pali': '', 'pali_roman': '', 'thai': 'x',
                                     'paiboon': 'phrá', 'english': ''})])

        assert check_paiboon(b)


class TestTheChantedLayersAreNotCorrupted:
    """Running Paiboon+ over `pali` is invisible once downstream."""

    def test_a_romanised_pali_is_caught(self):
        b = batch([chant(verses=[verse(1, pali='ajja bhonto pakkhassa')])])

        assert any('Latin' in p or 'no Thai script' in p
                   for p in check_pali_untouched(b))

    def test_thai_script_in_pali_roman_is_caught(self):
        b = batch([chant(verses=[verse(1, pali_roman='อัชชะ โภนโต')])])

        assert any('pali_roman contains Thai' in p
                   for p in check_pali_untouched(b))

    def test_an_empty_pali_is_not_an_error(self):
        """Part of the book prints its Pali in roman letters instead."""
        b = batch([chant(verses=[verse(1, pali='',
                                       pali_roman='ajja bhonto')])])

        assert check_pali_untouched(b) == []


class TestTheFiveLayers:

    def test_a_missing_layer_key_is_a_fault(self):
        v = verse(1)
        del v['paiboon']

        assert any('missing layer key' in p
                   for p in check_layer_keys(batch([chant(verses=[v])])))

    def test_an_empty_english_is_a_fault_at_every_depth(self):
        b = batch([chant(verses=[verse(1, english='')])])

        assert any('english is empty' in p for p in check_layer_keys(b))

    def test_empty_thai_and_paiboon_are_facts_not_gaps(self):
        """A Pali-only chant is complete with both empty. Most of pages 12-14."""
        b = batch([chant(verses=[verse(1, thai='', paiboon='')])])

        assert check_layer_keys(b) == []
        assert check_layers_not_invented(b) == []

    def test_paiboon_without_thai_means_something_was_invented(self):
        """Paiboon+ romanises the Thai. No Thai means nothing to romanise."""
        b = batch([chant(verses=[verse(1, thai='', paiboon='prá táŋ')])])

        assert any('nothing to romanise' in p
                   for p in check_layers_not_invented(b))


class TestTheManifest:

    def test_a_short_batch_is_caught(self):
        b = batch([chant('a')])
        b['batch']['manifest'].append('b')

        assert any('stopped early' in p or 'never arrived' in p
                   for p in check_manifest(b))

    def test_an_undeclared_chant_is_caught(self):
        b = batch([chant('a')])
        b['batch']['manifest'] = ['something-else']

        assert any('never declared' in p or 'never arrived' in p
                   for p in check_manifest(b))

    def test_a_chant_the_book_carries_onward_is_accounted_for(self):
        """`continues` is a third state, and it means COMPLETE for this batch.

        An earlier draft accepted only completed/not_started and failed both of
        the first two real batches, each of which ends on a chant the book
        carries onto a page that had not been photographed yet.
        """
        b = batch([chant('a')],
                  status={'completed': [], 'continues': ['a']})

        assert check_manifest(b) == []

    def test_a_chant_in_no_state_at_all_is_caught(self):
        b = batch([chant('a')],
                  status={'completed': [], 'not_started': [], 'continues': []})

        assert any('none of completed' in p for p in check_manifest(b))


class TestThePageMap:
    """A verse belongs to exactly one page. The errors here never look wrong."""

    def test_a_page_claiming_a_verse_that_does_not_exist(self):
        b = batch([chant('a', [verse(1)])],
                  pages=[{'page': 2, 'file': 'x', 'chant': 'a',
                          'verses': '1-4', 'note': ''}])

        assert any('no such verse' in p for p in check_page_map(b))

    def test_a_verse_claimed_by_two_pages(self):
        b = batch([chant('a', [verse(1)])],
                  pages=[{'page': 2, 'file': 'x', 'chant': 'a', 'verses': '1', 'note': ''},
                         {'page': 3, 'file': 'y', 'chant': 'a', 'verses': '1', 'note': ''}])

        assert any('claimed by pages' in p for p in check_page_map(b))

    def test_a_verse_on_no_page_at_all(self):
        b = batch([chant('a', [verse(1), verse(2)])],
                  pages=[{'page': 2, 'file': 'x', 'chant': 'a',
                          'verses': '1', 'note': ''}])

        assert any('on no page' in p for p in check_page_map(b))

    def test_a_block_only_row_claims_nothing(self):
        """Rows carrying page blocks say verses: none, and that is correct."""
        b = batch([chant('a', [verse(1)])],
                  pages=[{'page': 2, 'file': 'x', 'chant': 'a', 'verses': '1', 'note': ''},
                         {'page': 2, 'file': 'x', 'chant': '', 'verses': 'none', 'note': ''}])

        assert check_page_map(b) == []

    def test_pages_running_backwards_are_caught(self):
        b = batch(pages=[{'page': 9, 'file': 'x', 'chant': '', 'verses': 'none', 'note': ''},
                         {'page': 3, 'file': 'y', 'chant': '', 'verses': 'none', 'note': ''}])

        assert any('do not ascend' in p for p in check_pages_ascend(b))


class TestDiacriticConsistency:
    """One word romanised two ways compounds, and cannot be fixed at scale."""

    def test_the_same_word_spelled_two_ways_is_caught(self):
        b = batch([chant(verses=[
            verse(1, pali_roman='paṇṇarasī divaso'),
            verse(2, pali_roman='pannarasi divaso')])])

        assert any('romanised two ways' in p for p in check_diacritics(b))

    def test_a_declared_pair_is_allowed(self):
        """va and vā are two different Pali words, both meaning 'or'.

        They sit in the same printed line on page 14, and the Thai
        distinguishes them: วะ short, วา long.
        """
        b = batch([chant(verses=[verse(1, pali_roman='kāyena vācāya va cetasā vā')])],
                  status={'diacritic_exceptions': ['va/vā — two words, both "or"']})

        assert check_diacritics(b) == []

    def test_an_undeclared_pair_still_fails_when_another_is_declared(self):
        """Declaring one pair must not wave every other pair through."""
        b = batch([chant(verses=[
            verse(1, pali_roman='va vā paṇṇarasī'),
            verse(2, pali_roman='pannarasi')])],
            status={'diacritic_exceptions': ['va/vā — two words']})

        problems = check_diacritics(b)

        assert any('pannarasi' in p for p in problems)
        assert not any(p.count('va') and 'vā' in p and 'paṇṇarasī' not in p
                       for p in problems)

    def test_skeleton_strips_diacritics_for_comparison(self):
        assert skeleton('paṇṇarasī') == skeleton('pannarasi')
        assert skeleton('vā') == skeleton('va')


class TestTheNumbersTheBookPrints:
    """`printed_number` went in with no guard, which is the gap this closes.

    It is not `number`: one is the app's identity for a line, the other is
    what the page shows beside it, and they part company wherever a numbered
    list follows unnumbered chanted lines.
    """

    def test_a_list_numbered_as_the_book_numbers_it_passes(self):
        b = batch([chant(verses=[verse(1), verse(2),
                                 verse(3, printed_number=1),
                                 verse(4, printed_number=2)])])

        assert check_printed_numbers(b) == []

    def test_a_continuation_starting_part_way_through_passes(self):
        """Bhojana rules 19-30 arrive with the first eighteen already in."""
        b = batch([chant(verses=[verse(19, printed_number=19),
                                 verse(20, printed_number=20)])])

        assert check_printed_numbers(b) == []

    def test_the_same_number_twice_is_caught(self):
        """Both lines would render as 7, and the page shows each once."""
        b = batch([chant(verses=[verse(1, printed_number=7),
                                 verse(2, printed_number=7)])])

        assert any('same number twice' in p for p in check_printed_numbers(b))

    def test_numbers_going_backwards_are_caught(self):
        """A list running 5, 4, 6 is a pair transcribed the wrong way round."""
        b = batch([chant(verses=[verse(1, printed_number=5),
                                 verse(2, printed_number=4)])])

        assert any('ascend' in p for p in check_printed_numbers(b))

    @pytest.mark.parametrize('bad', [0, -1, '3', 3.0, None])
    def test_anything_that_is_not_a_positive_whole_number_is_caught(self, bad):
        b = batch([chant(verses=[verse(1, printed_number=bad)])])

        assert any('positive whole number' in p
                   for p in check_printed_numbers(b))

    def test_true_is_not_accepted_as_the_number_one(self):
        """bool is a subclass of int in Python, so this needs saying."""
        b = batch([chant(verses=[verse(1, printed_number=True)])])

        assert any('positive whole number' in p
                   for p in check_printed_numbers(b))

    def test_verses_the_book_does_not_number_are_skipped(self):
        """The nidana and a closing sentence carry none, and that is correct."""
        b = batch([chant(verses=[verse(1), verse(2), verse(3)])])

        assert check_printed_numbers(b) == []


class TestLineBreaksAgree:
    """A couplet break in one chanted layer is a break in the other.

    This replaced a check for "raw newlines inside string values". That check
    could never fire on what it named — JSON cannot hold a literal newline
    inside a string, so json.load raises first — and it fired on every
    legitimate couplet break instead, including the five-line ratana stanza
    on page 20, stored exactly as chanting.py has stored such breaks since
    the first chant.
    """

    def test_a_stanza_broken_the_same_way_in_both_layers_passes(self):
        b = batch([chant(verses=[verse(1, pali='อะ\nบะ\nคะ',
                                       pali_roman='a\nb\nc')])])

        assert check_line_breaks_agree(b) == []

    def test_a_break_in_one_layer_only_is_caught(self):
        """One layer typed from something other than the page."""
        b = batch([chant(verses=[verse(1, pali='อะ\nบะ', pali_roman='a b')])])

        assert any('break in the same places' in p
                   for p in check_line_breaks_agree(b))

    def test_a_verse_with_no_breaks_at_all_passes(self):
        assert check_line_breaks_agree(batch()) == []

    def test_a_roman_only_page_is_not_compared(self):
        """Part of the book prints its Pali in roman letters, so pali is ''."""
        b = batch([chant(verses=[verse(1, pali='', pali_roman='a\nb')])])

        assert check_line_breaks_agree(b) == []


class TestDepth:

    def test_a_data_only_batch_carrying_commentary_is_caught(self):
        b = batch([chant(background=['a paragraph stage 3 should have written'])])

        assert any('DATA-ONLY' in p for p in check_depth(b))

    def test_a_compact_batch_may_carry_it(self):
        b = batch([chant(background=['fine here'])], depth='COMPACT')

        assert check_depth(b) == []


class TestPageBlocks:
    """A block with no thai renders as an empty line — invisible on the page."""

    def test_a_block_with_no_thai_is_caught(self):
        b = batch(pages=[{'page': 2, 'file': 'x', 'chant': '', 'verses': 'none',
                          'note': '', 'blocks': [{'type': 'prose', 'english': 'x'}]}])

        assert any('render blank' in p for p in check_blocks(b))

    def test_a_footnote_may_have_no_english(self):
        """A canonical citation is reproduced, never translated or expanded."""
        b = batch(pages=[{'page': 12, 'file': 'x', 'chant': '', 'verses': 'none',
                          'note': '', 'blocks': [{'type': 'footnote', 'marker': '1',
                                                  'thai': 'ขุ.ขุ. 25/1-2', 'english': ''}]}])

        assert check_blocks(b) == []

    def test_a_numbered_item_without_its_number_is_caught(self):
        """The book's own numbering runs across page turns and must be kept."""
        b = batch(pages=[{'page': 9, 'file': 'x', 'chant': '', 'verses': 'none',
                          'note': '', 'blocks': [{'type': 'item', 'thai': 'x',
                                                  'english': 'y'}]}])

        assert any('no number' in p for p in check_blocks(b))


class TestChecksAreReadable:

    def test_string_checks_are_caught(self):
        """batch-009-009 wrote them as strings; apply_batch raises TypeError."""
        b = batch([chant(checks=['‼ CHECK [IMG_0272.PNG]: something'])])

        problems = check_checks_are_readable(b)

        assert any('not objects' in p for p in problems)

    def test_they_are_reported_once_per_chant_not_once_each(self):
        b = batch([chant(checks=['a', 'b', 'c', 'd'])])

        assert len(check_checks_are_readable(b)) == 1

    def test_a_check_with_no_file_is_caught(self):
        b = batch([chant(checks=[{'verse': None, 'issue': 'x'}])])

        assert any('names no image file' in p
                   for p in check_checks_are_readable(b))


class TestShapeIsCheckedFirst:
    """The other checks read these keys; a KeyError deeper down hides the cause."""

    def test_a_missing_top_level_key_is_named(self):
        assert any('chants' in p for p in check_shape({'batch': {}, 'batch_status': {}}))

    def test_an_id_that_is_not_a_slug_is_caught(self):
        b = batch([chant('Kham Prakat Ubosot')])

        assert any('not a slug' in p for p in check_shape(b))

    def test_validate_short_circuits_on_a_broken_shape(self):
        """No point reporting twelve consequences of one missing key."""
        results = validate({'batch': {}})

        assert results['shape']
        assert list(results) == ['shape']


class TestAgainstTheRealBatchFiles:
    """Every batch already applied must pass, or the checker is wrong."""

    import pathlib
    BATCHES = pathlib.Path(__file__).parent.parent / 'prompts/chanting-book-batch/batches'

    @pytest.mark.parametrize('name', [
        'batch-001-003', 'batch-004-006', 'batch-007-008',
        'batch-010-011', 'batch-012-012', 'batch-013-013', 'batch-014-014'])
    def test_a_shipped_batch_passes_every_check(self, name):
        b = json.loads((self.BATCHES / f'{name}.json').read_text(encoding='utf-8'))

        failed = {n: p for n, p in validate(b).items() if p}

        assert failed == {}, f'{name}: {failed}'

    def test_batch_009_is_known_to_be_unreadable_by_stage_2(self):
        """Not a bug in the checker — a real defect in a file already shipped.

        Page 9 is live, so it went in another way, but the file kept as the
        permanent record of what those photographs said is in a shape
        apply_batch cannot read. Pinned here so that fixing the file makes this
        test fail loudly rather than passing silently.
        """
        b = json.loads((self.BATCHES / 'batch-009-009.json').read_text(encoding='utf-8'))

        failed = {n: p for n, p in validate(b).items() if p}

        assert list(failed) == ['checks readable']


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
