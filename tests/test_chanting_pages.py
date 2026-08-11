"""Tests for build_page_index — turning chants back into printed pages.

These matter more than most tests in this project because there is no data to
eyeball yet: every chant currently in the book predates page numbers, so the
page view is exercised only by what is written here until the first photographed
batch lands.

The thing being protected: a verse records a page number ONLY where the page
turns, and everything after it is carried forward. So a single mistake in the
carry-forward silently moves every following verse onto the wrong page, and the
result still looks like perfectly good data. A monk calls out a page, the room
turns to it, and the person on their phone is reading the wrong words.
"""
import collections
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chanting import (  # noqa: E402
    build_page_index, chant_page_spans, check_page_blocks, check_variants,
    contents_for_front_page, contents_stretches, describe_coverage,
    describe_pages, page_coverage)


def verse(number, page=None):
    """A verse with only the keys the page index looks at."""
    v = {'number': number, 'pali': f'line {number}', 'english': f'meaning {number}'}
    if page:
        v['page'] = page
    return v


def chant(chant_id, page_start, verses):
    return {'id': chant_id, 'title_english': chant_id, 'page_start': page_start,
            'verses': verses}


def index(chants):
    """The page index for these chants and no page blocks.

    Explicit because the two halves of the data describe each other: asking
    for the index of a handful of test chants while the real PAGE_BLOCKS is
    still in scope builds a book that is half fixture and half chanting.py.
    """
    return build_page_index(chants, [])


def test_a_chant_on_a_single_page():
    pages, unpaginated = index([
        chant('metta', 47, [verse(1), verse(2), verse(3)]),
    ])

    assert unpaginated == []
    assert [p['page'] for p in pages] == [47]
    entry = pages[0]['entries'][0]
    assert entry['starts_here'] is True
    assert [v['number'] for v in entry['verses']] == [1, 2, 3]


def test_verses_carry_forward_until_the_page_turns():
    """Only verse 4 records a page, so 1-3 stay on 47 and 4-5 move to 48."""
    pages, _ = index([
        chant('metta', 47, [verse(1), verse(2), verse(3), verse(4, page=48), verse(5)]),
    ])

    assert [p['page'] for p in pages] == [47, 48]
    assert [v['number'] for v in pages[0]['entries'][0]['verses']] == [1, 2, 3]
    assert [v['number'] for v in pages[1]['entries'][0]['verses']] == [4, 5]


def test_a_continued_page_does_not_repeat_the_title():
    """The title is printed once, on the page the chant opens on."""
    pages, _ = index([
        chant('metta', 47, [verse(1), verse(2, page=48)]),
    ])

    assert pages[0]['entries'][0]['starts_here'] is True
    assert pages[1]['entries'][0]['starts_here'] is False


def test_one_page_holding_the_end_of_one_chant_and_the_start_of_the_next():
    """The commonest page in a chanting book, and the reason a page is not a chant."""
    pages, _ = index([
        chant('metta', 47, [verse(1), verse(2, page=48)]),
        chant('karaniya', 48, [verse(1), verse(2)]),
    ])

    assert [p['page'] for p in pages] == [47, 48]
    shared = pages[1]['entries']
    assert len(shared) == 2
    # In the order they appear down the page: the chant ending, then the one
    # beginning. A page that listed them the other way round would not match
    # the book a reader is holding.
    assert shared[0]['chant']['id'] == 'metta'
    assert shared[0]['starts_here'] is False
    assert shared[1]['chant']['id'] == 'karaniya'
    assert shared[1]['starts_here'] is True


def test_a_title_at_the_foot_of_a_page_with_its_verses_overleaf():
    """The chant still occupies its opening page, showing a title and nothing else."""
    pages, _ = index([
        chant('metta', 47, [verse(1, page=48), verse(2)]),
    ])

    assert [p['page'] for p in pages] == [47, 48]
    assert pages[0]['entries'][0]['verses'] == []
    assert pages[0]['entries'][0]['starts_here'] is True
    assert [v['number'] for v in pages[1]['entries'][0]['verses']] == [1, 2]


def test_chants_without_a_page_are_returned_not_guessed():
    """A plausible page is worse than no page: it is wrong in public, mid-chant."""
    pages, unpaginated = index([
        chant('metta', 47, [verse(1)]),
        {'id': 'older', 'title_english': 'older', 'verses': [verse(1)]},
    ])

    assert [p['page'] for p in pages] == [47]
    assert [c['id'] for c in unpaginated] == ['older']


def test_pages_come_back_in_book_order_whatever_order_the_file_is_in():
    """File order is not book order — page_start is what places a chant."""
    pages, _ = index([
        chant('third', 90, [verse(1)]),
        chant('first', 12, [verse(1)]),
        chant('second', 47, [verse(1)]),
    ])

    assert [p['page'] for p in pages] == [12, 47, 90]


def test_a_gap_in_the_book_is_left_as_a_gap():
    """Pages 48-52 are simply not there yet; nothing invents them."""
    pages, _ = index([
        chant('metta', 47, [verse(1)]),
        chant('karaniya', 53, [verse(1)]),
    ])

    assert [p['page'] for p in pages] == [47, 53]


class TestChantsAreInTheOrderThePagePrintsThem:
    """Two chants on one page must appear the way down the page they are set.

    Entries arrive in the order chants sit in CHANTS, which is book order
    right up until a chant is ADDED after its neighbours — apply_batch appends
    a new chant to the end of the file, so it lands at the foot of its page
    however early in the book it is printed. Ādiyasutta, numbered 13, rendered
    beneath Pabbatopama, numbered 14, on page 30.

    A reader following a service reads down the page. Two chants the wrong way
    round is the same class of error as a wrong page number, just quieter.
    """

    def numbered(self, chant_id, page_start, book_number, verses):
        return {'id': chant_id, 'title_english': chant_id,
                'page_start': page_start, 'book_number': book_number,
                'verses': verses}

    def test_the_books_numbering_settles_the_order(self):
        pages, _ = build_page_index([
            self.numbered('later', 30, 14, [verse(1)]),
            self.numbered('earlier', 30, 13, [verse(1)]),
        ], [])
        assert [e['chant']['id'] for e in pages[0]['entries']] == ['earlier', 'later']

    def test_a_chant_continuing_onto_the_page_still_comes_first(self):
        """It is the top of the page, and its number is lower anyway."""
        pages, _ = build_page_index([
            self.numbered('runs-on', 29, 12, [verse(1), verse(2, page=30)]),
            self.numbered('starts-here', 30, 13, [verse(1)]),
        ], [])
        page30 = next(p for p in pages if p['page'] == 30)
        assert [e['chant']['id'] for e in page30['entries']] == ['runs-on', 'starts-here']

    def test_without_numbers_the_existing_order_is_left_alone(self):
        """Most of the morning service is unnumbered; nothing beats file order."""
        pages, _ = build_page_index([
            chant('second-in-file', 30, [verse(1)]),
            chant('first-in-file', 30, [verse(1)]),
        ], [])
        assert [e['chant']['id'] for e in pages[0]['entries']] == [
            'second-in-file', 'first-in-file']

    def test_one_chant_missing_its_number_leaves_the_page_untouched(self):
        """Sorting on a partial signal would be worse than not sorting."""
        pages, _ = build_page_index([
            self.numbered('numbered', 31, 14, [verse(1)]),
            chant('unnumbered', 31, [verse(1)]),
        ], [])
        assert [e['chant']['id'] for e in pages[0]['entries']] == [
            'numbered', 'unnumbered']

    def test_the_real_page_30_reads_as_the_book_sets_it(self):
        pages, _ = build_page_index()
        page30 = next(p for p in pages if p['page'] == 30)
        assert [e['chant']['id'] for e in page30['entries'] if e['kind'] == 'chant'] == [
            'saccapanavidhyanurupa-gatha', 'adiyasutta-gatha', 'pabbatopama-gatha']


class TestTheContentsReachesContinuationPages:
    """A สารบัญ line offers every page it runs across, not just its first.

    The book's contents names where a chant BEGINS. Pages 5 and 21 are second
    halves, so the book names them nowhere — and the app, faithfully
    reproducing the contents, offered no way to them either. They were
    entered, openable by number, and invisible on the one page whose whole job
    is saying what is in.

    The fix must not add a line the book does not print. It adds buttons
    beside lines that are already there, which is app navigation and not the
    book's text.
    """

    def test_a_lines_stretch_runs_to_where_the_next_line_starts(self):
        stretches = contents_stretches()
        assert stretches[4] == [4, 5]
        assert stretches[20] == [20, 21]

    def test_a_line_whose_next_starts_immediately_covers_one_page(self):
        stretches = contents_stretches()
        assert stretches[22] == [22]

    def test_every_entered_page_is_reachable_from_some_contents_line(self):
        """The whole point, checked against the real book.

        A page the app serves but no contents line reaches is a page a reader
        can only find by guessing its number.
        """
        entered = {page['page'] for page in build_page_index()[0]}
        reachable = set()
        for front in (35, 36, 37, 38, 39, 40, 41, 42, 43, 44):
            rows, _ = contents_for_front_page(front)
            reachable |= {p for row in rows for p in row['pages']}
        assert not entered - reachable

    def test_a_button_is_never_offered_for_a_page_that_is_not_in(self):
        """The honesty rule the contents page already had, kept.

        A stretch is arithmetic over the book's numbering and happily spans
        pages nobody has entered. Only the ones actually served may appear.
        """
        entered = {page['page'] for page in build_page_index()[0]}
        for front in (35, 36, 37, 38, 39, 40, 41, 42, 43, 44):
            rows, _ = contents_for_front_page(front)
            for row in rows:
                assert set(row['pages']) <= entered


class TestAChantShowsEveryPageItCovers:
    """The index must not hide a page just because no chant starts on it.

    Pages 5 and 21 are both the second half of a chant that begins on the page
    before. Listing only `page_start` made them invisible on the index while
    being perfectly openable by number — which is the mismatch Josh found.
    """

    def test_a_chant_on_one_page_lists_that_page(self):
        spans = chant_page_spans([chant('metta', 47, [verse(1)])], [])
        assert spans['metta'] == [47]

    def test_a_chant_running_over_a_page_turn_lists_both(self):
        spans = chant_page_spans(
            [chant('metta', 47, [verse(1), verse(2, page=48)])], [])
        assert spans['metta'] == [47, 48]

    def test_a_chant_crossing_two_turns_lists_all_three(self):
        """Parittakaraṇapāṭha's real shape: starts 20, ends 22."""
        spans = chant_page_spans([chant('paritta', 20, [
            verse(1), verse(2, page=21), verse(3, page=22)])], [])
        assert spans['paritta'] == [20, 21, 22]

    def test_an_unpaginated_chant_has_no_span(self):
        spans = chant_page_spans(
            [{'id': 'x', 'title_english': 'x', 'verses': [verse(1)]}], [])
        assert 'x' not in spans

    def test_a_span_reads_as_a_range(self):
        assert describe_pages([4, 5]) == '4–5'
        assert describe_pages([20, 21, 22]) == '20–22'
        assert describe_pages([27]) == '27'

    def test_every_entered_page_is_reachable_from_some_chant_or_block(self):
        """The point of the change, checked against the real book.

        Every page the app serves must be findable on the index — either a
        chant is printed across it, or it is a page of the book's own material.
        A page reachable only by guessing its number is the fault this closes.
        """
        pages, _ = build_page_index()
        covered = {p for span in chant_page_spans().values() for p in span}
        blocks_only = {page['page'] for page in pages
                       if not any(e['kind'] == 'chant' for e in page['entries'])}
        for page in pages:
            assert page['page'] in covered or page['page'] in blocks_only, (
                f"page {page['page']} is served but appears on no chant card")


class TestSayingHowMuchOfTheBookIsIn:
    """The landing page tells a reader which numbers will work.

    It invites any page the monk called out, and most are not in yet. The
    danger is not the gap — it is a summary that sounds continuous when it is
    not, because someone acts on it mid-service.
    """

    def test_consecutive_pages_collapse_into_one_run(self):
        runs = page_coverage([
            chant('a', 1, [verse(1)]),
            chant('b', 2, [verse(1)]),
            chant('c', 3, [verse(1)]),
        ], [])
        assert runs == [(1, 3)]

    def test_a_gap_starts_a_new_run(self):
        """The whole point: 1-3 and 9 must never render as 1-9."""
        runs = page_coverage([
            chant('a', 1, [verse(1)]),
            chant('b', 2, [verse(1)]),
            chant('c', 3, [verse(1)]),
            chant('d', 9, [verse(1)]),
        ], [])
        assert runs == [(1, 3), (9, 9)]

    def test_a_chant_with_no_page_is_not_counted_as_coverage(self):
        """An unpaginated chant is in the app but on no page of the book."""
        runs = page_coverage([
            chant('a', 1, [verse(1)]),
            {'id': 'b', 'title_english': 'b', 'verses': [verse(1)]},
        ], [])
        assert runs == [(1, 1)]

    def test_a_single_page_is_named_not_ranged(self):
        assert describe_coverage([(5, 5)]) == '5'

    def test_two_runs_read_as_english(self):
        assert describe_coverage([(1, 29), (217, 221)]) == '1–29 and 217–221'

    def test_three_runs_keep_the_final_and(self):
        assert describe_coverage([(1, 2), (7, 8), (20, 20)]) == '1–2, 7–8 and 20'

    def test_nothing_in_says_nothing_rather_than_an_empty_range(self):
        assert describe_coverage([]) == ''

    def test_the_real_book_reports_runs_that_actually_open(self):
        """Every run's endpoints must be pages the app will really serve.

        A summary is only worth printing if it is true of the thing it
        summarises, so this checks it against the page index rather than
        against a hand-written expectation that would need editing every
        time a page lands.
        """
        served = {page['page'] for page in build_page_index()[0]}
        for first, last in page_coverage():
            assert first in served and last in served
            assert set(range(first, last + 1)) <= served


def test_the_real_book_still_builds():
    """Whatever is in chanting.py today must not raise.

    The docstring used to say the book had no pages yet. That stopped being
    true the day the first photographed batch landed, which is exactly the
    kind of comment that quietly turns into a lie about the code.
    """
    pages, unpaginated = build_page_index()

    assert isinstance(pages, list)
    assert isinstance(unpaginated, list)
    # Every placed page holds at least one chant, or the view would render blank.
    for page in pages:
        assert page['entries']


class TestThePagesOwnMaterial:
    """A printed page carries more than chants, and the app has to carry it too.

    Written after pages 7 and 8 went live showing their chant text and about
    half of what the book actually prints there. The missing half was never
    lost by accident: stage 1 read it off the photographs correctly and wrote
    it into the batch file, and stage 2 had no field to put it in. Nothing
    raised, no test failed, and the pages looked finished.

    So these tests are about the material that belongs to the PAGE rather than
    to any chant — a heading, an instruction, a closing that ends a whole
    service, a numbered note — and about it landing in the right place among
    the chants, which is the only place it means anything.
    """

    def blocks(self, page, after=None, blocks=None):
        group = {'page': page, 'blocks': blocks or [
            {'type': 'prose', 'thai': 'ข้อความ'},
        ]}
        if after is not None:
            group['after'] = after
        return group

    def test_material_printed_above_the_chant_comes_first(self):
        pages, _ = build_page_index(
            [chant('metta', 47, [verse(1)])],
            [self.blocks(47)],
        )

        assert [e['kind'] for e in pages[0]['entries']] == ['blocks', 'chant']

    def test_material_printed_below_a_chant_follows_it(self):
        pages, _ = build_page_index(
            [chant('metta', 47, [verse(1)])],
            [self.blocks(47, after='metta')],
        )

        assert [e['kind'] for e in pages[0]['entries']] == ['chant', 'blocks']

    def test_it_lands_after_the_right_chant_on_a_shared_page(self):
        """The commonest page in this book holds two chants. An instruction
        printed between them belongs between them, not at the foot."""
        pages, _ = build_page_index(
            [chant('metta', 47, [verse(1)]), chant('karaniya', 47, [verse(1)])],
            [self.blocks(47, after='metta')],
        )

        assert [e['kind'] for e in pages[0]['entries']] == ['chant', 'blocks', 'chant']
        assert pages[0]['entries'][0]['chant']['id'] == 'metta'
        assert pages[0]['entries'][2]['chant']['id'] == 'karaniya'

    def test_a_page_of_pure_instruction_is_still_a_page(self):
        """A reader who turns to it should find what is printed there.

        Pages 9 and 10 are mostly instruction, so a page holding no chant at
        all is ordinary rather than a special case.
        """
        pages, _ = build_page_index(
            [chant('metta', 47, [verse(1)])],
            [self.blocks(48)],
        )

        assert [p['page'] for p in pages] == [47, 48]
        assert [e['kind'] for e in pages[1]['entries']] == ['blocks']

    def test_an_anchor_that_matches_no_chant_on_the_page_is_caught(self):
        """The whole point of the anchor is WHERE on the page it goes.

        Caught by the checker rather than by raising mid-render. Raising there
        was the first attempt and it was wrong: PAGE_BLOCKS and CHANTS
        describe each other, so any disagreement between them — a renamed
        chant id, a fixture holding one and not the other — took the entire
        chanting book down with a 500. One typo should not cost every reader
        the whole book, so the strictness moved to a check that runs over the
        real data in the suite, where a typo costs a red build instead.
        """
        problems = check_page_blocks(
            [chant('metta', 47, [verse(1)])],
            [self.blocks(47, after='karaniya')],
        )

        assert len(problems) == 1
        assert 'not printed on that page' in problems[0]

    def test_a_stranded_anchor_still_renders_rather_than_vanishing(self):
        """Belt and braces for the case the checker is meant to prevent.

        If it ever does happen live, the words go to the foot of the page they
        were assigned to. Wrong place on the right page beats gone.
        """
        pages, _ = build_page_index(
            [chant('metta', 47, [verse(1)])],
            [self.blocks(47, after='karaniya')],
        )

        assert [e['kind'] for e in pages[0]['entries']] == ['chant', 'blocks']

    def test_the_real_page_blocks_are_sound(self):
        """The check that actually protects the book, run on the book."""
        assert check_page_blocks() == []

    def test_the_book_still_builds_with_whatever_blocks_are_in_it_today(self):
        pages, _ = build_page_index()
        for page in pages:
            assert page['entries']
            for entry in page['entries']:
                assert entry['kind'] in ('chant', 'blocks')


class TestThePagesOwnMaterialOnScreen:
    """The same material, rendered. Every block type the book actually uses."""

    PAGE = [
        {'type': 'service_closing', 'thai': 'จบพิธีทำวัตรเช้า',
         'english': 'Here ends the morning service', 'english_unverified': True},
        {'type': 'prose', 'thai': 'เมื่อสวดบทจบลงแล้ว',
         'english': 'When the chant has ended', 'english_unverified': True},
        {'type': 'heading', 'thai': 'คำอธิบายประกอบทำวัตรเช้า',
         'english': 'Notes on the morning service'},
        {'type': 'item', 'number': 3, 'thai': 'บทว่า ภิกขูนัง',
         'english': 'The line beginning bhikkhūnaṃ', 'english_unverified': True},
        {'type': 'footnote', 'marker': '1', 'thai': 'คะโต สำหรับอุบาสก'},
    ]

    @pytest.fixture()
    def page(self, monkeypatch):
        import copy

        import app as flask_app
        import chanting as chanting_module

        only = copy.deepcopy(chanting_module.CHANTS[0])
        only['id'] = 'only'
        only['page_start'] = 8

        monkeypatch.setattr(chanting_module, 'CHANTS', [only])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS',
                            [{'page': 8, 'after': 'only', 'blocks': self.PAGE}])
        return flask_app.app.test_client().get(
            '/chanting/page/8', follow_redirects=True).get_data(as_text=True)

    def test_every_block_reaches_the_page(self, page):
        for block in self.PAGE:
            assert block['thai'] in page, f"{block['type']} was dropped"

    def test_the_service_closing_is_not_lost_this_time(self, page):
        """The one that was already being read correctly and thrown away."""
        assert 'จบพิธีทำวัตรเช้า' in page
        assert 'block-service-closing' in page

    def test_a_numbered_item_keeps_the_books_own_number(self, page):
        """Items 1-2 are on page 8 and 3-5 on page 9: one list across a page
        turn. Renumbering per page would make it two lists starting at 1."""
        assert '>3.<' in page.replace(' ', '').replace('\n', '')

    def test_the_thai_and_english_are_layered_like_everything_else(self, page):
        """So the layer toggles work on them, and book mode shows the Thai
        alone — which is exactly what the printed page carries."""
        assert 'layer layer-thai' in page
        assert 'layer layer-english' in page

    def test_whose_english_this_is_gets_said(self, page):
        assert 'working translation made for this edition' in page

    def test_it_gets_said_once_and_not_above_every_paragraph(self, page):
        """Three of the five blocks carry unverified English. Saying it three
        times would bury the page the notice is meant to caveat."""
        assert page.count('The book prints this part of the page in Thai only') == 1

    def test_a_footnote_that_is_not_a_citation_still_has_somewhere_to_go(self, page):
        """source_printed holds canonical references. Page 8's footnote is an
        editorial note about a word substitution, and would be a lie there."""
        assert 'คะโต สำหรับอุบาสก' in page
        assert 'block-footnote' in page

    def test_the_citation_footnotes_still_work_alongside_blocks(self, page):
        """A blocks entry has no `chant`, and the footnote loop reads through
        one. It raised UndefinedError before the loop was guarded."""
        assert 'Digital Chanting Book' in page
        assert 'of the chanting book' in page


class TestTheInvitationIsPrintedOnce:
    """The line that starts a chant, and the two places the book puts it.

    The app has always shown an invitation under the chant's title. The book
    mostly does not: it sets an instruction, then the invitation, then another
    instruction, then the verses — so reproducing the page means the
    invitation has to sit in the run of blocks. Showing it in both places puts
    it on the page twice, which is the bug this guards.

    The words themselves are never copied into PAGE_BLOCKS. A block names the
    chant and the invitation is read back off it, so there is one copy and it
    cannot drift.
    """

    def build(self, monkeypatch, blocks, page=47):
        import copy

        import app as flask_app
        import chanting as chanting_module

        only = copy.deepcopy(chanting_module.CHANTS[0])
        only['id'] = 'only'
        only['page_start'] = page
        only['invitation'] = {'pali': 'หันทะ มะยัง อิทัง ภะณามะ เส.',
                              'pali_roman': '', 'thai': '', 'paiboon': '',
                              'english': ''}

        monkeypatch.setattr(chanting_module, 'CHANTS', [only])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS',
                            [{'page': page, 'after': 'only', 'blocks': blocks}])
        return flask_app.app.test_client().get(
            f'/chanting/page/{page}', follow_redirects=True).get_data(as_text=True)

    def test_an_invitation_block_is_filled_from_the_chant_it_names(self, monkeypatch):
        page = self.build(monkeypatch, [{'type': 'invitation', 'chant': 'only'}])
        assert 'หันทะ มะยัง อิทัง ภะณามะ เส.' in page

    def test_and_then_it_is_not_also_shown_under_the_title(self, monkeypatch):
        page = self.build(monkeypatch, [{'type': 'invitation', 'chant': 'only'}])
        assert page.count('หันทะ มะยัง อิทัง ภะณามะ เส.') == 1

    def test_without_a_block_it_still_shows_under_the_title(self, monkeypatch):
        """The ordinary case, and proof the suppression is not unconditional."""
        page = self.build(monkeypatch, [{'type': 'prose', 'thai': 'ข้อความ'}])
        assert page.count('หันทะ มะยัง อิทัง ภะณามะ เส.') == 1

    def test_an_invitation_for_a_chant_set_elsewhere_is_written_out(self, monkeypatch):
        """Page 5 gives the invitations for the เสขิยวัตร sections, which the
        book sets far later. There is no chant on the page to read them off."""
        page = self.build(monkeypatch, [
            {'type': 'invitation', 'pali': 'หันทะ มะยัง ฉัพพีสะติ ภะณามะ เส.'},
        ])

        assert 'หันทะ มะยัง ฉัพพีสะติ ภะณามะ เส.' in page
        # And it does not suppress the page's own chant invitation.
        assert 'หันทะ มะยัง อิทัง ภะณามะ เส.' in page

    def test_a_block_that_neither_names_nor_prints_is_caught(self):
        problems = check_page_blocks(
            [chant('metta', 47, [verse(1)])],
            [{'page': 47, 'after': 'metta',
              'blocks': [{'type': 'invitation'}]}],
        )

        assert any('neither names a chant nor prints a line' in p
                   for p in problems)

    def test_a_rubric_printed_between_verses_shows_between_them(self, monkeypatch):
        """Page 1 sets (กราบพร้อมกัน) under EACH of the three salutations.

        A block can only sit between whole chants, so a direction printed
        between two lines of one chant has nowhere to go — it lives on the
        verse above it instead. Recorded in the data from the first batch with
        a note asking whether it should be shown, and it should.
        """
        import copy

        import app as flask_app
        import chanting as chanting_module

        chant = copy.deepcopy(chanting_module.CHANTS[0])
        chant['id'] = 'bows'
        chant['page_start'] = 70
        for verse in chant['verses'][:3]:
            verse['rubric'] = '(กราบพร้อมกัน)'

        monkeypatch.setattr(chanting_module, 'CHANTS', [chant])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        page = flask_app.app.test_client().get(
            '/chanting/page/70', follow_redirects=True).get_data(as_text=True)

        assert page.count('(กราบพร้อมกัน)') == 3
        assert 'verse-rubric' in page

    def test_a_page_offers_a_way_back_to_the_contents(self):
        """The page view was a one-way trip: you could reach a page from the
        contents and had no way back to it."""
        import app as flask_app
        page = flask_app.app.test_client().get(
            '/chanting/page/2', follow_redirects=True).get_data(as_text=True)

        assert '/chanting/contents' in page

    def test_a_rubric_reaches_the_page(self, monkeypatch):
        """(กราบพร้อมกัน) — bow together. Recorded in the data from the start
        with a note asking whether it should be shown. It should."""
        page = self.build(monkeypatch, [
            {'type': 'rubric', 'thai': '(กราบพร้อมกัน)'},
        ])

        assert '(กราบพร้อมกัน)' in page
        assert 'block-rubric' in page


class TestTheHeadingsAreTheBooksOwn:
    """Four chants in the morning service are given no printed title at all.

    The book names them only by their invitation. The app needs to call them
    something in the index and in verse-by-verse, so it falls back to the
    English title — but printing that as a heading in book layout invents a
    line the page does not have.
    """

    def build(self, monkeypatch, mutate):
        import copy

        import app as flask_app
        import chanting as chanting_module

        chant = copy.deepcopy(chanting_module.CHANTS[0])
        chant['page_start'] = 60
        chant['title_english'] = 'In Praise of the Buddha'
        mutate(chant)

        monkeypatch.setattr(chanting_module, 'CHANTS', [chant])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        return flask_app.app.test_client().get(
            '/chanting/page/60', follow_redirects=True).get_data(as_text=True)

    def test_an_untitled_chant_gets_a_heading_book_layout_can_drop(self, monkeypatch):
        def untitled(chant):
            chant['title_thai'] = ''
            chant['title_pali'] = ''

        page = self.build(monkeypatch, untitled)
        assert 'In Praise of the Buddha' in page      # still there to study by
        assert 'page-app-title' in page               # and marked as ours

    def test_a_title_the_book_does_print_is_not_marked(self, monkeypatch):
        page = self.build(monkeypatch, lambda c: None)
        assert 'page-chant-title page-app-title' not in page


class TestTheBooksOwnContents:
    """สารบัญ — the book's index, reproduced and made navigable.

    Two things are being protected. The first is the numbering: front matter
    runs (๓๕)…(๔๔) in its OWN sequence, and the body has a page 36 of its own.
    A monk calls out a number meaning the body, so the two must never share a
    route or a reader ends up on a contents page mid-service.

    The second is honesty. A contents line whose page is not in the app yet is
    printed as plain text rather than as a link, because a link that goes
    nowhere is a worse lie than a visible gap — and it makes this page a true
    map of how much of the book has been entered.
    """

    def read(self, **params):
        import app as flask_app
        return flask_app.app.test_client().get(
            '/chanting/contents', query_string=params,
            follow_redirects=True).get_data(as_text=True)

    def test_the_contents_page_renders(self):
        page = self.read()
        assert 'สารบัญ' in page
        assert chanting_module().BOOK['title_thai'] in page

    def test_front_matter_numbering_is_not_the_body_numbering(self):
        """(๓๖) and page 36 are different pages of the same book."""
        import app as flask_app

        client = flask_app.app.test_client()
        body = client.get('/chanting/page/36', follow_redirects=True).get_data(as_text=True)

        # The body route answers about the BODY page, whatever front matter exists.
        # Checked against the front matter's own bracketed number rather than the
        # word สารบัญ: every page carries a nav link reading "Contents (สารบัญ)",
        # so the old assertion only held while page 36 was missing and the route
        # served nothing. It would have gone on passing for that reason alone.
        assert '(๓๖)' not in body
        assert 'มะหาจุนทะโพชฌังคะสุตตัง' in body

    def test_a_page_that_is_in_the_app_gets_a_button(self):
        page = self.read()
        assert 'toc-btn' in page
        assert '/chanting/page/' in page

    def test_a_chant_that_is_in_the_app_can_be_opened_directly(self):
        """The page and the chant are different destinations.

        A page is for chanting along when a number is called out; the chant is
        for reading it. Sending someone to the page when they wanted the chant
        is not a small thing when the chant starts half way down.
        """
        page = self.read()
        assert 'Open chant' in page

        chanting = chanting_module()
        linked = {r['chant_id'] for r in chanting.CONTENTS if r['chant_id']}
        assert linked, 'no contents line resolves to a chant'
        for chant_id in linked:
            assert chanting.get_chant(chant_id), f'{chant_id} does not exist'

    def test_every_line_carries_an_english_name(self):
        """The index is unreadable to a non-Thai reader without it."""
        missing = [r['title'] for r in chanting_module().CONTENTS
                   if not r['title_english']]
        assert not missing, f'{len(missing)} lines have no English: {missing[:3]}'

    def test_the_english_never_disagrees_with_the_chant_page(self):
        """A chant's own title_english wins wherever there is one, so the index
        and the chant page cannot call the same thing two different names."""
        chanting = chanting_module()
        for row in chanting.CONTENTS:
            if not row['chant_id']:
                continue
            chant = chanting.get_chant(row['chant_id'])
            if chant.get('title_english'):
                assert row['title_english'] == chant['title_english']

    def test_the_page_number_is_shown_in_both_scripts(self):
        """A reader who cannot read Thai numerals still has to find the page a
        monk just called out."""
        page = self.read()
        assert 'toc-page-thai' in page
        assert 'toc-page-arabic' in page

    def test_a_page_not_entered_yet_stays_plain_text(self):
        """The whole value of the page: it says what is missing."""
        page = self.read()
        assert 'not-in-app' in page

    def test_every_link_points_at_a_page_that_actually_exists(self):
        """A contents entry linking to a page that 404s would be the one bug
        this page could plausibly ship with."""
        import re

        import app as flask_app

        client = flask_app.app.test_client()
        page = self.read()
        targets = set(re.findall(r'href="/chanting/page/(\d+)"', page))
        assert targets, 'no links at all — the linking is not working'

        entered = {p['page'] for p in chanting_module().build_page_index()[0]}
        for target in targets:
            assert int(target) in entered, f'contents links to page {target}, which is not in'

    def test_an_unknown_front_page_falls_back_rather_than_erroring(self):
        assert 'สารบัญ' in self.read(p='999')
        assert 'สารบัญ' in self.read(p='not-a-number')

    def test_the_contents_runs_forwards(self):
        """A book's contents never goes backwards.

        This is the cheapest check there is on 301 hand-transcribed page
        numbers: a misread Thai numeral almost always lands out of order, and
        out of order is something a machine can see even though it cannot read
        the page. It caught nothing on the first run, which is the result you
        want and is only meaningful because the check would have caught it.
        """
        rows = chanting_module().CONTENTS
        backwards = [(a['title'], a['page'], b['title'], b['page'])
                     for a, b in zip(rows, rows[1:]) if b['page'] < a['page']]

        assert not backwards, f'contents goes backwards at: {backwards[:3]}'

    def test_the_linked_page_is_derived_from_the_printed_one(self):
        """The Thai numeral is what the book prints and the only source of
        truth; the integer exists to be followed. An earlier draft carried
        both by hand, which across 301 rows is a disagreement waiting."""
        chanting = chanting_module()
        for row in chanting.CONTENTS:
            assert row['page'] == chanting.thai_number(row['page_printed'])

    def test_thai_numerals_convert(self):
        thai_number = chanting_module().thai_number
        assert thai_number('๑') == 1
        assert thai_number('๒๘') == 28
        assert thai_number('๓๐๘') == 308

    def test_a_number_that_is_not_thai_raises_rather_than_guessing(self):
        with pytest.raises(ValueError):
            chanting_module().thai_number('28')

    def test_every_contents_page_renders(self):
        chanting = chanting_module()
        for front in chanting.FRONT_MATTER:
            if front['kind'] != 'contents':
                continue
            page = self.read(p=front['number'])
            assert 'สารบัญ' in page
            assert 'toc-row' in page, f"front page {front['number']} rendered no lines"

    def test_the_contents_is_reachable_from_the_index(self):
        import app as flask_app
        index = flask_app.app.test_client().get(
            '/chanting', follow_redirects=True).get_data(as_text=True)
        assert '/chanting/contents' in index


def chanting_module():
    import chanting
    return chanting


class TestTheNumbersTheBookPrints:
    """The book numbers some lines and not others, and the app must agree.

    Book layout used to show no numbers at all, so a numbered list in the book
    — the eight precepts, the seventy-five sekhiyas, the ten reflections —
    rendered as an unnumbered one on exactly the pages where the number is how
    a chanter keeps their place.

    Two numbers exist and they are not the same thing. `number` is the app's
    own identity for a line, shown in verse-by-verse. `printed_number` is what
    the BOOK sets beside it, shown in book layout. They differ wherever a
    numbered list follows unnumbered chanted lines.
    """

    def test_the_two_numbers_are_allowed_to_disagree(self):
        """The Dasadhamma Sutta's nidana pushes the book's item 1 to verse 3.

        Asserted as a RELATIONSHIP rather than a snapshot of the verses: an
        earlier version pinned the last verse to (10, 8) and failed the
        moment page 20 legitimately extended the chant to thirteen.
        """
        from chanting import CHANTS
        chant = next(c for c in CHANTS if c['id'] == 'dasadhamma-sutta')
        numbered = {v['number']: v.get('printed_number') for v in chant['verses']}

        assert numbered[1] is None, 'the nidana is not numbered in the book'
        assert numbered[2] is None, "'katame dasa' is not numbered either"

        # The ten reflections are verses 3-12, offset by two throughout.
        for verse_number in range(3, 13):
            assert numbered[verse_number] == verse_number - 2

        # The sutta's closing sentence is printed without a number.
        assert numbered[13] is None

    @staticmethod
    def page(number):
        import app as flask_app
        return flask_app.app.test_client().get(
            f'/chanting/page/{number}', follow_redirects=True).get_data(as_text=True)

    def test_book_layout_shows_the_books_number_and_hides_the_apps(self):
        html = self.page(19)

        # Both are in the markup; CSS decides which one a reader sees.
        assert 'class="verse-number-printed"' in html
        assert '.page-body.view-book .verse-number { display: none; }' in html
        assert '.verse-number-printed { display: none; }' in html
        assert '.page-body.view-book .verse-number-printed {' in html

    def test_a_verse_the_book_does_not_number_shows_nothing(self):
        """Nothing may be printed where the page prints nothing."""
        import re
        verses = re.findall(r'<div class="verse">(.*?)</div>', self.page(19), re.S)

        assert 'verse-number-printed' not in verses[0]
        assert 'verse-number-printed' not in verses[1]
        assert '<span class="verse-number-printed">1.</span>' in verses[2]

    def test_the_chant_number_is_on_the_title_line_as_the_book_sets_it(self):
        """The book prints '1. ทะสะธัมมะสุตตัง'; CHANT 1 is the app's own label."""
        html = self.page(19)

        assert '<span class="chant-number-printed">1.</span>' in html
        assert '.page-body.view-book .page-chant-number { display: none; }' in html

    def test_a_chant_the_book_does_not_number_gets_no_number(self):
        """Most chants have no book_number, and none may be invented.

        Checked against the markup rather than the whole document: the CSS
        rule that hides the class lives in the <style> block, so the class
        NAME is on every page whether or not anything uses it.
        """
        markup = self.page(14).split('</style>')[-1]

        assert '<span class="chant-number-printed">' not in markup


class TestTheMarkupHoldsTogether:
    """Both chanting pages must close every <style> and <script> they open.

    Written because they did not. Moving the shared CSS into a partial dropped
    one closing </style>, and the effect was brutally disproportionate: the
    browser read the whole rest of the document as CSS text and rendered a
    blank page. The server still returned 200 with 305KB of correct HTML, every
    other test still passed, and the page was simply empty.

    An unclosed tag is invisible to anything that checks status codes or
    substrings, which is most of what a test suite does. So check the tags.
    """

    def rendered(self, path):
        import app as flask_app
        return flask_app.app.test_client().get(path, follow_redirects=True).get_data(as_text=True)

    @pytest.mark.parametrize('path', ['/chanting', '/chanting/pages'])
    def test_every_style_and_script_tag_is_closed(self, path):
        page = self.rendered(path)

        assert page.count('<style') == page.count('</style>'), \
            f'{path}: unclosed <style> — the browser will eat the page as CSS'
        assert page.count('<script') == page.count('</script>'), \
            f'{path}: unclosed <script> — the browser will eat the page as code'

    @pytest.mark.parametrize('path', ['/chanting', '/chanting/pages'])
    def test_the_body_actually_has_the_page_in_it(self, path):
        """The blank page still returned 200. Status codes prove nothing here.

        The three alternatives are the three states /chanting/pages can be in,
        and it has now been in two of them: it showed the empty state while no
        chant had a page number, and now redirects to a real page since the
        first batch landed. The test asserted only the first two and failed the
        day real pages arrived — which is the assertion being too specific
        about a passing phase, not the page breaking.
        """
        page = self.rendered(path)

        assert 'Digital Chanting Book' in page
        # Content that lives AFTER the style blocks, so it is missing exactly
        # when a stylesheet has swallowed the document.
        assert ('Chanting along' in page              # the index's way in
                or 'no page numbers yet' in page      # the empty state
                or 'of the chanting book' in page)    # a real page


class TestHowThePageIsSet:
    """The book does not print every page the same way, so neither can we.

    Shaped after a real page: a chant the book runs together as continuous
    prose, printed in Pali with no Thai translation, closed by a จบ formula,
    with its canonical reference in a footnote at the foot of the page.
    """

    @pytest.fixture()
    def client(self, monkeypatch):
        import copy

        import app as flask_app
        import chanting as chanting_module

        prose = copy.deepcopy(chanting_module.CHANTS[0])
        prose['id'] = 'mahapatthana'
        prose['page_start'] = 41
        prose['layout'] = 'prose'
        prose['source_printed'] = 'อภิ.ป. 40/1'
        prose['closing'] = {'pali': 'จบ' + prose['title_thai'], 'pali_roman': '',
                            'thai': '', 'paiboon': '', 'english': ''}
        # Pali only, as that page prints it: no Thai, so no Paiboon either.
        for verse in prose['verses']:
            verse['thai'] = ''
            verse['paiboon'] = ''

        # A second chant starting on the same page and running past it, so the
        # closing and the footnote must NOT appear for it here.
        runs_on = copy.deepcopy(chanting_module.CHANTS[1])
        runs_on['id'] = 'runs-on'
        runs_on['page_start'] = 41
        runs_on['source_printed'] = 'อภิ.ยม. 38/1'
        runs_on['closing'] = {'pali': 'จบ' + runs_on['title_thai'], 'pali_roman': '',
                              'thai': '', 'paiboon': '', 'english': ''}
        runs_on['verses'][1]['page'] = 42

        monkeypatch.setattr(chanting_module, 'CHANTS', [prose, runs_on])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        return flask_app.app.test_client()

    def read(self, client, url):
        return client.get(url, follow_redirects=True).get_data(as_text=True)

    def test_both_ways_of_seeing_the_page_are_offered(self, client):
        page = self.read(client, '/chanting/page/41')
        assert 'As the book prints it' in page
        assert 'Verse by verse' in page

    def test_book_layout_is_what_you_land_on(self, client):
        """The page exists for chanting along, so it opens as the book."""
        assert 'page-body view-book' in self.read(client, '/chanting/page/41')

    def test_a_prose_chant_is_marked_so_it_can_flow_back_together(self, client):
        page = self.read(client, '/chanting/page/41')
        assert 'page-chant is-prose' in page

    def test_a_page_can_mix_a_pali_only_chant_with_a_translated_one(self, client):
        """The commonest way to corrupt this book is to fill in a gap.

        Page 41 carries both kinds: a Pali-only chant and one verse of a chant
        that does have a Thai translation. Counting the rendered layers is what
        proves the Pali-only chant contributed none of them — a substring check
        cannot, because the layer names also appear in the stylesheet.
        """
        page = self.read(client, '/chanting/page/41')

        assert page.count('class="layer layer-pali"') == 8   # 7 prose + 1 translated
        # Exactly the one verse that has a translation, and not a line more.
        assert page.count('class="layer layer-thai"') == 1
        assert page.count('class="layer layer-paiboon"') == 1

    def test_the_closing_formula_shows_where_the_chant_ends(self, client):
        page = self.read(client, '/chanting/page/41')
        assert 'chant-closing' in page

    def test_a_chant_running_onto_the_next_page_is_not_closed_early(self, client):
        """Its จบ belongs on page 42, where it actually finishes."""
        import chanting as chanting_module
        runs_on = chanting_module.CHANTS[1]

        assert runs_on['closing']['pali'] not in self.read(client, '/chanting/page/41')
        assert runs_on['closing']['pali'] in self.read(client, '/chanting/page/42')

    def test_the_books_own_reference_is_shown_as_a_footnote(self, client):
        page = self.read(client, '/chanting/page/41')
        assert 'page-footnotes' in page
        assert 'อภิ.ป. 40/1' in page

    def test_a_reference_belongs_to_the_page_the_chant_ends_on(self, client):
        """Footnote numbering restarts per page in the book, so it cannot roam."""
        assert 'อภิ.ยม. 38/1' not in self.read(client, '/chanting/page/41')
        assert 'อภิ.ยม. 38/1' in self.read(client, '/chanting/page/42')


class TestItAdaptsToWhateverThePagePrints:
    """A page carries whatever the book put on it, and the app follows.

    Pali with a Thai translation, Pali alone, a mixture on one page, a chant
    titled only in Pali — none of these is a special case to be handled, and
    none of them may cause the app to invent the missing half.
    """

    def build(self, monkeypatch, mutate):
        import copy

        import app as flask_app
        import chanting as chanting_module

        chant = copy.deepcopy(chanting_module.CHANTS[0])
        chant['page_start'] = 60
        mutate(chant)
        monkeypatch.setattr(chanting_module, 'CHANTS', [chant])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        return flask_app.app.test_client().get(
            '/chanting/page/60', follow_redirects=True).get_data(as_text=True)

    def test_a_translated_chant_shows_both_scripts(self, monkeypatch):
        page = self.build(monkeypatch, lambda c: None)
        assert 'class="layer layer-pali"' in page
        assert 'class="layer layer-thai"' in page

    def test_a_pali_only_chant_shows_no_thai_at_all(self, monkeypatch):
        def strip_thai(chant):
            for verse in chant['verses']:
                verse['thai'] = ''
                verse['paiboon'] = ''
            chant['invitation'] = {'pali': '', 'pali_roman': '', 'thai': '',
                                   'paiboon': '', 'english': ''}

        page = self.build(monkeypatch, strip_thai)
        assert 'class="layer layer-pali"' in page
        assert 'class="layer layer-thai"' not in page
        assert 'class="layer layer-paiboon"' not in page

    def test_a_pali_only_chant_says_whose_english_it_is(self, monkeypatch):
        """Not a disclaimer for its own sake — the book has nothing to check
        that English against, and the reader should know which is which."""
        def pali_only(chant):
            for verse in chant['verses']:
                verse['thai'] = ''
            chant['english_unverified'] = True

        assert 'working translation made for this edition' in self.build(monkeypatch, pali_only)

    def test_the_unverified_notice_shows_on_a_continuation_page_too(self, monkeypatch):
        """It sat inside the starts_here branch until page 5 went live.

        A reader landing mid-chant got our English translation with nothing
        saying it was ours. A disclaimer that only appears on the page you did
        not open is not a disclaimer.
        """
        import copy

        import app as flask_app
        import chanting as chanting_module

        chant = copy.deepcopy(chanting_module.CHANTS[0])
        chant['page_start'] = 60
        chant['english_unverified'] = True
        chant['verses'][2]['page'] = 61          # the chant runs onto page 61
        monkeypatch.setattr(chanting_module, 'CHANTS', [chant])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        client = flask_app.app.test_client()

        opening = client.get('/chanting/page/60', follow_redirects=True).get_data(as_text=True)
        carried_on = client.get('/chanting/page/61', follow_redirects=True).get_data(as_text=True)

        assert 'working translation made for this edition' in opening
        assert 'working translation made for this edition' in carried_on

    def test_a_chant_titled_only_in_pali_gets_no_empty_heading(self, monkeypatch):
        def pali_title(chant):
            chant['title_thai'] = ''
            chant['title_pali'] = 'Khemākhema-gāthā'

        page = self.build(monkeypatch, pali_title)
        assert 'Khemākhema-gāthā' in page
        # The Pali title is promoted into the heading rather than repeated
        # underneath an empty line where the Thai title would have been.
        assert page.count('Khemākhema-gāthā') == 1

    def test_a_prose_chant_with_a_translation_keeps_its_thai_out_of_the_flow(self, monkeypatch):
        """Only the Pali flows back into a block.

        If the Thai flowed too, the two scripts would interleave a unit at a
        time inside one paragraph. The rule that does the flowing must name
        the Pali layer and nothing else.
        """
        import pathlib

        template = pathlib.Path('templates/chanting_page.html').read_text(encoding='utf-8')
        flow_rule = template[template.index('.is-prose .verse-body .verse .layer-pali'):]
        flow_rule = flow_rule[:flow_rule.index('}')]

        assert 'layer-thai' not in flow_rule

        # And the markup still carries both layers, so verse-by-verse is whole.
        page = self.build(monkeypatch, lambda c: c.update(layout='prose'))
        assert 'page-chant is-prose' in page
        assert 'class="layer layer-thai"' in page


class TestThePageRoutes:
    """The reading view itself: what a reader gets when they type a number.

    Uses two real chants out of the book with page numbers added, so the view
    is exercised against actual Pali and Thai rather than stubs.
    """

    @pytest.fixture()
    def client(self, monkeypatch):
        import copy

        import app as flask_app
        import chanting as chanting_module

        first = copy.deepcopy(chanting_module.CHANTS[0])
        second = copy.deepcopy(chanting_module.CHANTS[1])
        third = copy.deepcopy(chanting_module.CHANTS[2])

        # 47 -> 48 mid-chant, a second chant starting on 48, then a jump to 53.
        # That covers a page turn, a shared page and a gap in one book.
        first['page_start'] = 47
        first['verses'][2]['page'] = 48
        second['page_start'] = 48
        third['page_start'] = 53

        monkeypatch.setattr(chanting_module, 'CHANTS', [first, second, third])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        return flask_app.app.test_client()

    def read(self, client, url):
        return client.get(url, follow_redirects=True).get_data(as_text=True)

    def test_the_entry_point_opens_the_book_at_its_first_page(self, client):
        assert client.get('/chanting/pages').headers['Location'].endswith('/chanting/page/47')

    def test_the_jump_box_opens_the_page_asked_for(self, client):
        assert client.get('/chanting/pages?p=48').headers['Location'].endswith('/chanting/page/48')

    def test_a_page_shows_the_chant_printed_on_it(self, client):
        import chanting as chanting_module
        assert chanting_module.CHANTS[0]['title_thai'] in self.read(client, '/chanting/page/47')

    def test_a_shared_page_shows_both_chants_and_repeats_neither_title(self, client):
        page = self.read(client, '/chanting/page/48')
        assert page.count('page-chant"') == 2
        # The chant carried over from 47 is marked as continued rather than
        # given a second title, because the printed page does not repeat it.
        assert 'continued' in page

    def test_next_and_previous_reach_the_pages_either_side(self, client):
        page = self.read(client, '/chanting/page/48')
        assert '/chanting/page/47' in page
        assert '/chanting/page/53' in page

    def test_the_first_and_last_pages_do_not_offer_a_way_off_the_end(self, client):
        assert 'First page' in self.read(client, '/chanting/page/47')
        assert 'Last page' in self.read(client, '/chanting/page/53')

    def test_skipping_a_gap_says_so(self, client):
        """Next goes 48 -> 53, and the reader is told rather than left to assume."""
        assert 'are not in the app yet' in self.read(client, '/chanting/page/48')

    def test_a_page_not_entered_yet_helps_rather_than_404s(self, client):
        """The reader typed the number they were given. An error page is no use."""
        response = client.get('/chanting/page/50')
        assert response.status_code == 200

        page = response.get_data(as_text=True)
        assert 'has not been added yet' in page
        # Offers the nearest pages either side of the one asked for.
        assert '/chanting/page/48' in page
        assert '/chanting/page/53' in page

    def test_a_page_beyond_the_book_still_helps(self, client):
        page = self.read(client, '/chanting/page/999')
        assert 'has not been added yet' in page
        assert '/chanting/page/53' in page

    def test_the_empty_book_says_so_instead_of_breaking(self, monkeypatch):
        """Today's real state: every chant predates page numbers."""
        import app as flask_app
        import chanting as chanting_module

        monkeypatch.setattr(chanting_module, 'CHANTS',
                            [{'id': 'x', 'title_english': 'x', 'verses': []}])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        page = flask_app.app.test_client().get(
            '/chanting/pages', follow_redirects=True).get_data(as_text=True)

        assert 'no page numbers yet' in page


class TestVariantReadings:
    """The book's footnotes offering another spelling of one word.

    The thing being protected is not the rendering — it is the ATTACHMENT. A
    variant filed against the wrong verse renders as a note about a word that
    is not on the line, and this book has already made that mistake twice by
    hand: once by giving a chant the footnote of the chant above it, and once
    by pointing page 26's footnote at verse 4 when it belongs to verse 2.
    Neither looked wrong afterwards.
    """

    def verse_with(self, variant, pali='สัญญะเต พ์รัห์มะจาริโน.'):
        return {'number': 2, 'pali': pali, 'pali_roman': 'saññate brahmacārino.',
                'english': 'the farers in the holy life,',
                'variants': [variant]}

    def book(self, verse_dict):
        return [{'id': 'devata', 'title_english': 'devata', 'page_start': 26,
                 'verses': [verse_dict]}]

    SOUND = {'marker': '๒', 'word': 'พ์รัห์มะจาริโน',
             'reading': 'พ์รัห์มจาระโย', 'reading_roman': ''}

    def test_a_sound_variant_passes(self):
        assert check_variants(self.book(self.verse_with(self.SOUND))) == []

    def test_the_real_book_is_sound(self):
        assert check_variants() == []

    def test_a_variant_on_the_wrong_verse_is_caught(self):
        """The failure this check exists for: the note is real, the word is
        not on this line, and the reader is left hunting."""
        problems = check_variants(self.book(
            self.verse_with(self.SOUND, pali='ยา ตัตถะ เทวะตา อาสุง')))

        assert len(problems) == 1
        assert 'filed against the wrong line' in problems[0]

    def test_a_variant_found_in_the_roman_layer_passes(self):
        """Part of this book prints its Pali in roman letters, leaving `pali`
        empty. A variant there is on `pali_roman` and is not misfiled."""
        verse_dict = self.verse_with(
            dict(self.SOUND, word='brahmacārino'), pali='')

        assert check_variants(self.book(verse_dict)) == []

    def test_a_reading_that_repeats_the_word_is_caught(self):
        """A footnote that changes nothing is a transcription slip, not a
        variant — the book would not print one."""
        problems = check_variants(self.book(self.verse_with(
            dict(self.SOUND, reading='พ์รัห์มะจาริโน'))))

        assert any('repeats `word`' in p for p in problems)

    def test_an_empty_reading_is_caught(self):
        problems = check_variants(self.book(self.verse_with(
            dict(self.SOUND, reading=''))))

        assert any('says nothing' in p for p in problems)

    def test_a_missing_marker_is_caught(self):
        """The marker is what ties the note to the page it was printed on;
        footnote numbers restart at 1 on every page."""
        problems = check_variants(self.book(self.verse_with(
            dict(self.SOUND, marker=''))))

        assert any('no printed marker' in p for p in problems)


class TestVariantReadingsOnScreen:
    """Rendered — in both views, because a reader arrives by either."""

    @pytest.fixture()
    def views(self, monkeypatch):
        import copy

        import app as flask_app
        import chanting as chanting_module

        only = copy.deepcopy(chanting_module.CHANTS[0])
        only['id'] = 'only'
        only['page_start'] = 26
        only['verses'][0]['variants'] = [
            {'marker': '๒', 'word': only['verses'][0]['pali'],
             'reading': 'อีกอย่างหนึ่ง', 'reading_roman': 'aññathā'},
        ]

        monkeypatch.setattr(chanting_module, 'CHANTS', [only])
        monkeypatch.setattr(chanting_module, 'PAGE_BLOCKS', [])
        client = flask_app.app.test_client()
        return {
            'page': client.get('/chanting/page/26',
                               follow_redirects=True).get_data(as_text=True),
            'chant': client.get('/chanting',
                                follow_redirects=True).get_data(as_text=True),
        }

    def test_the_reading_reaches_the_page_view(self, views):
        assert 'อีกอย่างหนึ่ง' in views['page']
        assert 'verse-variant' in views['page']

    def test_the_reading_reaches_the_chant_view(self, views):
        assert 'อีกอย่างหนึ่ง' in views['chant']
        assert 'verse-variant' in views['chant']

    def test_the_printed_marker_is_shown_as_the_book_prints_it(self, views):
        """Thai numerals on a page that uses them; never converted."""
        assert '๒' in views['page']

    def test_the_romanisation_is_shown_where_there_is_one(self, views):
        assert 'aññathā' in views['page']

    def test_it_is_not_dressed_as_a_sixth_layer(self, views):
        """Nobody chants a variant. If it ever picks up a `layer-` class it
        joins the layer toggles and starts reading as a line of the chant."""
        marked = views['page'].split('verse-variant')[1].split('</p>')[0]
        assert 'layer-' not in marked


class TestEveryVerseDictIsTheSameShape:
    """A verse dict must lead with `'number'`, however it was written.

    This is a file-format test rather than a behaviour test, and it earned its
    place the hard way. Twenty-seven verse dicts were written by hand before
    `apply_batch` existed and led with `'section'`; the 1,128 the tool has
    written since lead with `'number'`. Both parse, both render identically, and
    nothing in the app can tell the difference.

    What could not tell the difference was a migration that matched verse dicts
    by position — moving eight colophons out of the verses and into `closing`.
    It assumed `'number'` came first, so on five chants it matched the wrong
    dict and deleted a real chanted line, leaving the numbering reading
    21, 22, 24. Nothing failed; it was caught by reading the numbers.

    So the shape is pinned. One order means a tool may key on the first line of
    a verse dict, and the class of silent, invisible edit that caused goes away.
    """

    def source(self):
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(here, 'chanting.py'), encoding='utf-8') as f:
            return f.read()

    def test_no_verse_dict_leads_with_a_key_other_than_number(self):
        import re

        leads = collections.Counter(
            re.findall(r"\n            \{\n                '(\w+)':", self.source()))
        wrong = {k: n for k, n in leads.items() if k not in ('number', 'type')}

        assert not wrong, (
            "verse dicts leading with something other than 'number': "
            f"{wrong}. render_verse writes 'number' first, so a dict that "
            "does not is a second shape in one file — and a tool matching on "
            "position will silently pick the wrong verse.")

    def test_section_always_follows_the_number_it_belongs_to(self):
        import re

        src = self.source()

        assert not re.findall(r"'section':[^\n]*\n                'number':", src), \
            "a 'section' key sits above its own 'number'"
        assert re.findall(r"'number': \d+,\n                'section':", src), \
            "no 'section' found after a 'number' at all — the pattern this " \
            "test relies on has changed, so it is no longer checking anything"


class TestEveryDeclaredBlockReachedThePage:
    """A block stage 1 recorded must actually be on the page it belongs to.

    This is the check that was missing when `apply_batch` silently dropped
    every page block it was given. Stage 1 read the headings and footnotes off
    the photographs, `check_batch` passed them, the batch files recorded them —
    and seventeen of them across pages 30 to 40 were printed in the book and
    absent from the app, with nothing anywhere reporting a problem.

    The batch files are the record of what each photograph said, so they are
    the right thing to hold the app to.
    """

    def declared(self):
        import json
        import pathlib

        found = []
        folder = pathlib.Path('prompts/chanting-book-batch/batches')
        for path in sorted(folder.glob('*.json')):
            batch = json.loads(path.read_text(encoding='utf-8'))
            for row in batch['batch']['pages']:
                if row.get('page') is None:
                    continue
                for block in row.get('blocks') or []:
                    if block.get('thai'):
                        found.append((row['page'], block.get('type'),
                                      block.get('marker'), block['thai'],
                                      path.name))
                # A service closing is recorded as a page-map KEY rather than
                # a block, so a sweep that only read `blocks` would have the
                # same blind spot the applier had, and miss it for the same
                # reason. Page 41's จบสวดแจงเท่านี้ was exactly that case.
                if row.get('service_closing'):
                    found.append((row['page'], 'service_closing', None,
                                  row['service_closing'], path.name))
        return found

    def test_the_batches_declare_blocks_at_all(self):
        """Guards the guard: an empty sweep would pass the test below."""
        assert len(self.declared()) > 20

    def test_every_declared_block_is_in_the_app(self):
        in_app = {
            (group.get('page'), block.get('type'), block.get('marker'),
             block.get('thai'))
            for group in chanting_module().PAGE_BLOCKS
            for block in group.get('blocks', [])
        }
        missing = [
            f"page {page} ({source}): {kind} {thai[:40]}"
            for page, kind, marker, thai, source in self.declared()
            if (page, kind, marker, thai) not in in_app
        ]
        assert not missing, (
            'blocks recorded from the photographs but never written into '
            'PAGE_BLOCKS, so the page shows less than the book prints:\n  '
            + '\n  '.join(missing))


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
