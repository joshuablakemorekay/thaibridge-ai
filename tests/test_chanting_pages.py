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
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chanting import build_page_index, check_page_blocks  # noqa: E402


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


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
