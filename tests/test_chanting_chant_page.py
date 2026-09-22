"""Tests for a chant's own page, and for the index no longer carrying chants.

The index used to render all 305 chants in full inside closed cards. It was a
4.9MB page, and the whole book was downloaded to read one chant of it — on
whatever signal a temple has. Now:

* a chant has a page of its own, which is also a link that can be sent to
  someone;
* the index holds the cards and fetches a chant the first time one is opened;
* a reader with no JavaScript follows the card's link to that same page.

What these tests protect is the part that is easy to undo by accident: that the
index stays light, that the fallback link is real rather than decorative, and
that the fragment the browser fetches is a chant and not a whole web page
(dropping one of those into a card would put a second copy of the site inside
it).
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chanting  # noqa: E402


SAMPLE = chanting.CHANTS[0]


def test_a_chant_has_a_page_of_its_own(unlocked_client):
    page = unlocked_client.get(
        f"/chanting/chant/{SAMPLE['id']}").get_data(as_text=True)

    assert SAMPLE['title_thai'] in page
    # The chant itself, not just its title and summary.
    assert SAMPLE['verses'][0]['pali'] in page
    assert 'chant-body' in page


def test_an_unknown_chant_is_a_404(unlocked_client):
    assert unlocked_client.get('/chanting/chant/not-a-chant').status_code == 404
    assert unlocked_client.get(
        '/chanting/chant/not-a-chant/body').status_code == 404


def test_the_fragment_is_a_chant_and_not_a_whole_page(unlocked_client):
    """What the index drops into a card must be the chant alone.

    The browser checks for this too before trusting what came back, because a
    lapsed gate answers with a page rather than a chant.
    """
    fragment = unlocked_client.get(
        f"/chanting/chant/{SAMPLE['id']}/body").get_data(as_text=True)

    assert fragment.lstrip().startswith('<div class="chant-body">')
    assert SAMPLE['verses'][0]['pali'] in fragment
    for whole_page_marker in ('<html', '<nav', '<body'):
        assert whole_page_marker not in fragment, (
            f'the fragment carries {whole_page_marker} — that is a page, '
            'not a chant'
        )


def test_the_index_no_longer_carries_the_chants(unlocked_client):
    index = unlocked_client.get('/chanting').get_data(as_text=True)

    # The cards are all there...
    assert index.count('class="chant-card"') == len(chanting.CHANTS)
    # ...and every one of them knows where to get its chant.
    # (the attribute as written on a card, not the script that reads it)
    assert index.count('data-chant-url="') == len(chanting.CHANTS)
    # ...but the words are not in the page.
    assert SAMPLE['verses'][0]['pali'] not in index
    assert 'class="verse"' not in index


def test_every_card_links_to_a_chant_that_exists(unlocked_client):
    """The fallback link is what a reader without JavaScript follows.

    A card whose link 404s would leave that reader with no way to the chant at
    all, which is worse than the page being heavy.
    """
    index = unlocked_client.get('/chanting').get_data(as_text=True)

    for chant in chanting.CHANTS:
        assert f"/chanting/chant/{chant['id']}" in index, (
            f"{chant['id']} has no link out of its card"
        )

    # Spot-check that such a link really is served, rather than only built.
    last = chanting.CHANTS[-1]['id']
    assert unlocked_client.get(f'/chanting/chant/{last}').status_code == 200


def test_the_index_stays_light(unlocked_client):
    """A guard, not a measurement.

    Putting the chant body back into the card would look harmless in a diff
    and quietly return the page to 4.9MB. 1MB is far above what the cards need
    (about 550KB today) and far below what all 305 chants would cost.
    """
    size = len(unlocked_client.get('/chanting').data)

    assert size < 1_000_000, (
        f'the chanting index is {size/1024:.0f}KB — something has put the '
        'chants back into it'
    )


WITH_CLOSING = [c for c in chanting.CHANTS
                if c.get('closing')
                and (c['closing'].get('pali') or c['closing'].get('thai'))]


def test_the_book_still_has_chants_that_end_with_a_closing():
    """If this ever hits zero the tests below stop proving anything."""
    assert len(WITH_CLOSING) > 50


@pytest.mark.parametrize('chant', WITH_CLOSING, ids=[c['id'] for c in WITH_CLOSING])
def test_a_chant_shows_the_closing_the_book_prints_under_it(chant):
    """จบ… — the line that ends a chant.

    The page-by-page view has always printed it. Reading the chant by title
    did not, so for 72 chants the ending was simply missing for anyone who
    came in that way. It is the same markup in both views now.
    """
    from flask import render_template

    import app as flask_app

    with flask_app.app.test_request_context():
        html = render_template('partials/chant_body.html', chant=chant,
                               sections=chanting.CHANT_SECTIONS, spans={})

    assert 'chant-closing' in html
    printed = chant['closing'].get('pali') or chant['closing'].get('thai')
    assert printed in html


def test_a_chant_with_no_closing_prints_none(unlocked_client):
    """Only where the book prints one — an empty formula is not a blank line."""
    without = next(c for c in chanting.CHANTS if not c.get('closing'))
    page = unlocked_client.get(
        f"/chanting/chant/{without['id']}").get_data(as_text=True)

    # The markup, not the stylesheet — every chant page carries the CSS rule.
    assert 'class="verse chant-closing"' not in page


@pytest.mark.parametrize('route', ['/chanting/chant/{}', '/chanting/chant/{}/body'])
def test_both_chant_routes_render_the_same_words(unlocked_client, route):
    """One template, so the page and the fragment cannot drift apart."""
    chant = chanting.CHANTS[3]
    served = unlocked_client.get(
        route.format(chant['id'])).get_data(as_text=True)

    assert chant['verses'][0]['pali'] in served
