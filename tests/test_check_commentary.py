"""Tests for check_commentary — did the commentary pass leave the verses alone?

Mostly about it FAILING. Every check in this file exists because the throwaway
version of it caught something real during the Stage 3 pass, so each test below
either breaks a chant deliberately in the way that actually happened, or pins a
case that looks like a failure and is not.

The last two tests run against the real `chanting.py`. They are the invariant
the pass established — all 305 chants carrying the five commentary fields — and
without them nothing stops chant 306 arriving without any.
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_commentary import (  # noqa: E402
    against, own_text, prose, script, shape, strip_commentary)


def chant(**overrides):
    """A chant with commentary that passes every check."""
    base = {
        'id': 'metta',
        'title_thai': 'เมตตา',
        'verses': [{'number': 1, 'pali': 'สัพเพ สัตตา', 'thai': '', 'english': 'all beings'}],
        'summary': 'A short chant.',
        'when_chanted': 'Chanted in the evening.',
        'source': '',
        'background': ['Where it came from.'],
        'meaning': ['What it means.', 'Why it is chanted.'],
    }
    base.update(overrides)
    return base


# ── shape ────────────────────────────────────────────────────────────────

def test_a_complete_chant_is_clean():
    assert shape([chant()]) == []


def test_an_empty_source_is_allowed_because_honest():
    """`source: ''` is the correct answer 297 times out of 305.

    A citation that cannot be given honestly is left empty on purpose, so an
    empty string must never be reported as a missing field. Getting this wrong
    would make the check nag about the one decision the pass was most careful
    about.
    """
    assert shape([chant(source='')]) == []


def test_a_missing_field_is_caught():
    broken = chant()
    del broken['when_chanted']
    assert any('when_chanted' in p for p in shape([broken]))


def test_background_as_one_string_is_caught():
    """The field is a LIST of paragraphs, and a bare string renders as one.

    Easy to write by hand and invisible on the page until somebody looks for
    the paragraph breaks the printed edition is supposed to space from.
    """
    problems = shape([chant(background='One long string.')])
    assert any('background' in p for p in problems)


def test_an_empty_paragraph_inside_a_list_is_caught():
    problems = shape([chant(meaning=['Real paragraph.', '   '])])
    assert any('paragraph 2' in p for p in problems)


def test_an_empty_list_is_caught():
    assert any('meaning' in p for p in shape([chant(meaning=[])]))


# ── script ───────────────────────────────────────────────────────────────

def test_lao_codepoints_are_caught():
    """This happened. Lao ຳ and ຺ look exactly like Thai ํ and ฺ.

    Two of them reached a Pali citation and would have sat there as a corrupt
    reference in a book whose whole point is getting Thai right.
    """
    bad = chant(source='อํ. จตุก຺ก. 21/44')
    problems, _ = script([bad], whole_file='')
    assert any('LAO' in p for p in problems)


def test_thai_that_is_nowhere_in_the_file_is_caught():
    """Also happened, three times — a word typed with the wrong character.

    It matches nothing in the book, which is exactly what makes it findable.
    """
    bad = chant(meaning=['The chant says เวระมณี here.'])
    problems, _ = script([bad], whole_file='')
    assert any('nowhere in the file' in p for p in problems)


def test_thai_quoted_from_its_own_chant_is_clean():
    good = chant(meaning=['It opens สัพเพ สัตตา, all beings.'])
    problems, _ = script([good], whole_file='')
    assert problems == []


def test_thai_quoted_from_elsewhere_is_reported_but_not_an_error():
    """A heading recorded in a CHECK comment is legitimate to quote.

    The book prints service headings above a chant that belong to the page and
    not to the text, so they live in comments. Quoting one is right; treating
    it as an error would have made the check unusable.
    """
    other = chant(meaning=['The book prints จบพิธีทำวัตรเช้า below it.'])
    problems, elsewhere = script([other], whole_file='# จบพิธีทำวัตรเช้า, centred')
    assert problems == []
    assert elsewhere and elsewhere[0][1] == 'จบพิธีทำวัตรเช้า'


# ── the verses-untouched proof ───────────────────────────────────────────

def test_stripping_leaves_the_verses_and_removes_the_prose():
    stripped = strip_commentary([chant()])[0]
    assert 'verses' in stripped and 'title_thai' in stripped
    assert not any(k in stripped for k in
                   ('summary', 'when_chanted', 'source', 'background', 'meaning'))


def test_the_real_book_is_unchanged_since_before_stage_3():
    """The whole safety argument of the commentary pass, as one assertion.

    `5d53f50~1` is the commit before the first Stage 3 batch landed. Every
    non-commentary field of every chant must still be identical to it: no
    verse, title, page number, invitation, section label or rubric moved while
    77,000 words of prose were written around them.
    """
    import chanting
    assert against('5d53f50~1', chanting.CHANTS) == []


def test_every_chant_in_the_real_book_has_its_commentary():
    """305 of 305, and nothing else keeps it that way.

    The pass finished with every chant carrying all five fields. This is what
    stops the next chant being added without them and nobody noticing until a
    reader opens a card with no context in it.
    """
    import chanting
    assert shape(chanting.CHANTS) == []
    assert len(chanting.CHANTS) == 305


def test_no_lao_and_no_untraceable_thai_in_the_real_book():
    import chanting
    whole_file = open(
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     'chanting.py'), encoding='utf-8').read()
    problems, _ = script(chanting.CHANTS, whole_file)
    assert problems == []


def test_prose_and_own_text_do_not_overlap():
    """The two halves must stay separate or the Thai check proves nothing.

    If `own_text` ever picked up the commentary, every quoted word would match
    itself and the check would pass on anything.
    """
    written = prose(chant(meaning=['mentions เมตตา']))
    printed = own_text(chant(meaning=['mentions เมตตา']))
    assert 'mentions' in written and 'mentions' not in printed
