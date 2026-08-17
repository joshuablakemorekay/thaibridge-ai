"""Tests for check_render — does the RENDERED page read like the printed page?

Mostly about it FAILING. This project already had one checker that could not be
made to fail, and `check_batch`'s docstring records what improvised versions of
THIS pass cost: three false results in one afternoon. So each test below either
breaks a page deliberately, or pins a case that used to be reported as broken
and was not.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

from check_render import (check, expected, first_claimed,  # noqa: E402
                          flatten, present, visible_text, walk)


def verse(n, pali):
    return {'number': n, 'pali': pali, 'pali_roman': 'x',
            'thai': '', 'paiboon': '', 'english': 'y'}


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


class FakeClient:
    """Serves one canned page, so a render fault can be created on purpose."""

    def __init__(self, body, status=200):
        self.body = body
        self.status = status

    def get(self, path):
        page = int(path.rsplit('/', 1)[1])
        body = self.body(page) if callable(self.body) else self.body
        return type('R', (), {'status_code': self.status,
                              'data': body.encode('utf-8')})()


class TestVisibleText:

    def test_script_and_style_bodies_are_dropped(self):
        """They hold Thai in string literals, so leaving them in lets a check
        pass on text no reader can see."""
        html = "<style>.a{content:'ก'}</style><p>ข</p><script>var x='ค'</script>"
        text = visible_text(html)

        assert 'ข' in text
        assert 'ก' not in text and 'ค' not in text

    def test_whitespace_is_flattened_on_both_sides(self):
        """A couplet break is a \\n in the data and markup on the page."""
        assert flatten('อะ\nบะ') == 'อะ บะ'
        assert 'อะ บะ' in visible_text('<p>อะ<br>\n   บะ</p>')


class TestTheWalk:

    def test_lines_in_printed_order_pass(self):
        assert walk('ก ข ค', [('a', 'ก'), ('b', 'ข'), ('c', 'ค')]) == []

    def test_a_line_the_page_never_shows_is_caught(self):
        problems = walk('ก ค', [('a', 'ก'), ('b', 'ข')])

        assert any('MISSING from the page entirely' in p for p in problems)

    def test_a_line_shown_out_of_order_is_caught(self):
        """The failure a presence check cannot see."""
        problems = walk('ข ก', [('a', 'ก'), ('b', 'ข')])

        assert any('out of order' in p for p in problems)

    def test_a_line_the_book_prints_twice_is_matched_twice(self):
        """Page 67 prints ตัสสะ ภะคะวะโต, as two separate units."""
        assert walk('ก ข ก', [('v1', 'ก'), ('v2', 'ข'), ('v3', 'ก')]) == []

    def test_a_short_unit_inside_a_longer_one_is_not_a_duplicate(self):
        """พุทโธ, is a verse of its own AND sits inside สัมมาสัมพุทโธ, on the
        same page. Counting hits calls one of them a duplicate; walking does
        not."""
        assert walk('สัมมาสัมพุทโธ, พุทโธ,',
                    [('v1', 'สัมมาสัมพุทโธ,'), ('v2', 'พุทโธ,')]) == []

    def test_a_cut_line_is_not_expected_to_render_verbatim(self):
        """The app holds the completed line, which lives on the later page."""
        assert walk('', [('v9', 'สะเทวะเก โลเก […]')]) == []


class TestPresence:

    def test_a_block_the_page_drops_is_caught(self):
        """Losing a block entirely has happened to this project twice."""
        problems = present('ก', [('prose block 0', 'ข')])

        assert any('MISSING' in p for p in problems)

    def test_a_block_out_of_position_is_not_a_fault(self):
        """Its anchor is decided by apply_batch, which has its own tests."""
        assert present('ข ก', [('prose block 0', 'ก')]) == []


class TestExpected:

    def test_a_continuation_does_not_expect_the_title_again(self):
        """The book does not reprint a title on a page a chant runs onto."""
        chants = [{'id': 'a', 'title_thai': 'ชื่อ', 'verses': [verse(2, 'ข')]}]
        pages = [{'page': 3, 'chant': 'a', 'verses': '2', 'starts_here': False}]

        runs, _ = expected({'batch': {'pages': pages}, 'chants': chants}, 3)

        assert [label for label, _ in runs[0]] == ['a v2']

    def test_a_line_an_earlier_page_began_is_not_expected_here(self):
        """It renders on the page it STARTS on. Five pages were wrongly
        reported before this rule was applied."""
        chants = [{'id': 'a', 'verses': [verse(11, 'ข')]}]
        pages = [{'page': 47, 'chant': 'a', 'verses': '11',
                  'starts_here': False}]

        runs, _ = expected({'batch': {'pages': pages}, 'chants': chants}, 47,
                           {('a', 11): 46})

        assert runs == []

    def test_first_claimed_takes_the_lowest_page(self, tmp_path):
        files = batch_file(tmp_path,
                           [{'page': 47, 'chant': 'a', 'verses': '11'},
                            {'page': 46, 'chant': 'a', 'verses': '10-11'}],
                           [{'id': 'a', 'verses': [verse(11, 'ข')]}])

        assert first_claimed(files)[('a', 11)] == 46


class TestEndToEnd:

    def test_a_page_that_renders_what_the_book_prints_passes(self, tmp_path):
        chants = [{'id': 'a', 'title_thai': 'ชื่อ',
                   'verses': [verse(1, 'ก'), verse(2, 'ข')]}]
        files = batch_file(tmp_path, [{'page': 2, 'chant': 'a',
                                       'verses': '1-2', 'starts_here': True}],
                           chants)

        faults, counts = check(FakeClient('<p>ชื่อ</p><p>ก</p><p>ข</p>'), files)

        assert faults == {}
        assert counts == {'pages': 1, 'strings': 3}

    def test_a_page_that_drops_a_verse_fails(self, tmp_path):
        chants = [{'id': 'a', 'title_thai': 'ชื่อ',
                   'verses': [verse(1, 'ก'), verse(2, 'ข')]}]
        files = batch_file(tmp_path, [{'page': 2, 'chant': 'a',
                                       'verses': '1-2', 'starts_here': True}],
                           chants)

        faults, _ = check(FakeClient('<p>ชื่อ</p><p>ก</p>'), files)

        assert any('MISSING' in p for p in faults[2])

    def test_a_page_that_will_not_load_is_reported_not_skipped(self, tmp_path):
        chants = [{'id': 'a', 'title_thai': 'ชื่อ', 'verses': [verse(1, 'ก')]}]
        files = batch_file(tmp_path, [{'page': 2, 'chant': 'a',
                                       'verses': '1', 'starts_here': True}],
                           chants)

        faults, _ = check(FakeClient('boom', status=500), files)

        assert any('HTTP 500' in p for p in faults[2])


def test_every_real_page_renders_what_the_book_prints():
    """The whole point, run against the real book and the real templates.

    Kept as a test as well as a script for the same reason `check_pages` is: a
    page that starts rendering something other than what its photograph
    recorded now breaks the suite, rather than waiting for somebody to run a
    checker by hand. This is the only check in the repo that opens the page a
    reader actually meets.
    """
    import glob

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root)
    import app as flaskapp

    files = sorted(glob.glob(os.path.join(
        root, 'prompts', 'chanting-book-batch', 'batches', '*.json')))
    faults, counts = check(flaskapp.app.test_client(), files)

    assert counts['pages'] > 50, 'the batch files stopped being rendered'
    assert not faults, '\n'.join(f'page {p}: {q}'
                                 for p, qs in sorted(faults.items())
                                 for q in qs)
