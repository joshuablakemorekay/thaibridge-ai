"""Tests for finding a chant by name on the Digital Chanting Book index.

The search itself runs in the browser — the whole index is already on the page,
so filtering it there is instant. What Python can protect is everything the
search stands on, and that is where it would actually break:

* every chant must carry at least one name a reader can TYPE. Ninety-eight
  chants have no romanised title and twenty-four have no Thai one, so "it has a
  title" is not the same question as "it can be found";
* the names must survive folding — lower-cased, stripped of Pali diacritics and
  of spaces and hyphens — because that is how a reader types them. A title that
  folds away to nothing is a chant nobody can reach;
* the box, its live count and its empty state must all be in the page.

`fold` here mirrors the browser's. Two copies of one rule is a real cost, paid
on purpose: without it nothing checks that the DATA can be typed at all, and
that is the half that changes every time a page is entered from a photograph.
"""
import os
import re
import sys
import unicodedata

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chanting  # noqa: E402


def fold(text):
    """Lower case, no accents, no punctuation — what the reader actually types.

    The same two steps as the browser: decompose, drop the combining marks
    (so "Khemākhema" becomes "khemakhema"), then keep only digits, plain
    letters and Thai. Thai script comes through whole; its vowels and tone
    marks are letters in their own right, not accents to be stripped.
    """
    decomposed = unicodedata.normalize('NFD', text or '')
    without_accents = ''.join(c for c in decomposed
                              if not unicodedata.combining(c))
    return re.sub(r'[^0-9a-z฀-๿]+', '', without_accents.lower())


def names(chant):
    """Every name of this chant a reader might type, folded."""
    return [fold(chant.get(key, '')) for key in
            ('title_thai', 'title_pali', 'title_roman', 'title_english')
            ] + [fold(chant['id'])]


def test_fold_lets_a_reader_type_pali_without_the_diacritics():
    # Nobody types ā or ṇ on a phone. This is the whole reason for folding.
    assert fold('Khemākhema-saraṇadīpikā-gāthā') == 'khemakhemasaranadipikagatha'
    assert 'saranadipika' in fold('Khemākhema-saraṇadīpikā-gāthā')


def test_fold_ignores_spaces_and_hyphens():
    # The book hyphenates; a reader types spaces. Both must land in one place.
    assert fold('Karaṇīya Metta Sutta') == fold('karaniya-metta-sutta')


def test_fold_keeps_thai_whole():
    # A Thai title folds to itself: nothing in it is an accent to be dropped.
    title = 'เขมาเขมะสะระณะทีปิกาคาถา'
    assert fold(title) == title


@pytest.mark.parametrize('chant', chanting.CHANTS,
                         ids=[c['id'] for c in chanting.CHANTS])
def test_every_chant_can_be_found_by_something_typeable(chant):
    """No chant may be reachable only by scrolling past the other 304."""
    assert any(names(chant)), (
        f"{chant['id']} has no name a reader could type"
    )


def test_a_known_chant_is_found_by_part_of_its_name():
    """The promise the box makes: type part of a name, get that chant."""
    def matches(term):
        wanted = fold(term)
        return [c['id'] for c in chanting.CHANTS
                if any(wanted in name for name in names(c) if name)]

    assert 'khemakhema-saranadipika' in matches('saranadipika')
    assert 'khemakhema-saranadipika' in matches('Saraṇadīpikā')
    assert matches('metta'), 'nothing found for "metta"'


def test_the_search_box_is_on_the_index_page(unlocked_client):
    page = unlocked_client.get('/chanting').get_data(as_text=True)
    assert 'id="chant-search"' in page
    assert 'id="chant-find"' in page
    # The count is announced rather than just drawn, so a reader using a screen
    # reader hears how many chants are left without leaving the box.
    assert 'id="chant-search-count"' in page
    assert 'role="status"' in page
    # And the empty state names somewhere else to look, because the book holds
    # more chants than the app has entered yet.
    assert 'id="chant-search-empty"' in page


def test_the_box_is_hidden_until_its_javascript_has_run(unlocked_client):
    """Without JavaScript the page is what it always was — every chant, listed.

    A search box that takes a name and does nothing would be worse than none.
    """
    page = unlocked_client.get('/chanting').get_data(as_text=True)
    assert '<div class="chant-search" id="chant-search" hidden>' in page
    assert 'panel.hidden = false;' in page
