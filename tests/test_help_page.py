"""The Help page (/instructions) is the user guide.

What matters is that it never tells a learner something the app does not do:
every price, limit and level on it must be the one the app enforces, and every
link on it must lead somewhere. These tests read the real constants rather
than restating them, so changing a price can never leave the guide behind.
"""
import re

import pytest

import app as app_module
from app import (
    ALPHABET_QUIZ_PASS_MARK,
    BASIC_AI_DAILY_LIMIT,
    EARNED_UNLOCK_LEVEL,
    FREE_AI_DAILY_LIMIT,
    FREE_DHAMMA_DAILY_LIMIT,
    INSTANT_ACCESS_ADDON,
    PRO_FAIR_USE_DAILY,
    SECTION_REQUIREMENTS,
    SUBSCRIPTION_TIERS,
    XP_LEVELS,
    app,
)


@pytest.fixture
def page():
    response = app.test_client().get("/instructions")
    assert response.status_code == 200
    return response.get_data(as_text=True)


# The page's original text, before the guide sections were added around it.
# Every sentence must still be there, word for word: the guide was meant to add
# to the page, never to cost it anything it already said.
ORIGINAL_SENTENCES = [
    "A quick guide to finding your way around.",
    "Getting started in 3 steps",
    # Two original lines were corrected on purpose (2026-10-20, Josh agreed):
    # Tones needs Level 3 + Thai Reader, so it is no beginner's starting point,
    # and the tutor gained a seventh mode, Translator, on 2026-10-14.
    "the Alphabet and ThaiBridge Spelling are good places to begin.",
    "seven modes of help",
    "Learn tones early — it really matters",
    "If you learn tones from the very beginning, correct pronunciation becomes a habit",
    "What you can do",
    "themed word sets with practice quizzes",
    "a Samatha &amp; Vipassana timer",
    "Monk Mode is a <strong>free track for monks and nuns</strong>",
    "It starts switched off.",
    "font designed so similar letters can't be mistaken for each other.",
    "It highlights as you point at it, and only that part is read.",
    "The line underneath the button always tells you what to do next",
    "tables fill the space when there's room and scroll sideways when there isn't",
    "How the pages are laid out",
    "Matching each page to its purpose keeps things clear",
]


@pytest.mark.parametrize("sentence", ORIGINAL_SENTENCES)
def test_the_original_page_text_is_kept_word_for_word(page, sentence):
    # Line breaks in the template are only layout, so compare with runs of
    # whitespace collapsed; every word and character must still match.
    assert sentence in " ".join(page.split())


def test_every_section_follows_the_four_part_shape(page):
    """What it's for · Where to start · Step by step · In short, in every
    guide section after the overview, so each one reads the same way."""
    for anchor in ["approach", "chanting", "account", "learning-path",
                   "buddhism", "ai-tutor", "levels", "plans"]:
        start = page.index(f'id="{anchor}"')
        end = page.find('<div class="card"', start + 1)
        section = page[start:end if end != -1 else None]
        for part in ["Where to start", "Step by step", "In short:"]:
            assert part in section, f"{anchor} is missing '{part}'"


def test_prices_come_from_the_tiers(page):
    for tier in ("basic", "pro"):
        info = SUBSCRIPTION_TIERS[tier]
        assert f"£{info['price']:.2f} a month" in page
        assert f"£{info['price_year']:.0f} a year" in page
    assert f"£{INSTANT_ACCESS_ADDON['price']:.2f}" in page


def test_limits_and_levels_come_from_the_app(page):
    assert f"Free {FREE_AI_DAILY_LIMIT} a day" in page
    assert f"Thai Reader {BASIC_AI_DAILY_LIMIT} a day" in page
    assert f"{FREE_DHAMMA_DAILY_LIMIT} questions a day" in page
    assert f"up to\n        {PRO_FAIR_USE_DAILY} messages a day" in page
    assert f"Level {EARNED_UNLOCK_LEVEL}</strong>" in page
    assert f"({XP_LEVELS[EARNED_UNLOCK_LEVEL]} XP)" in page
    assert f"({ALPHABET_QUIZ_PASS_MARK} of the" in page


def test_a_changed_limit_shows_up_without_editing_the_template(monkeypatch):
    monkeypatch.setattr(app_module, "FREE_AI_DAILY_LIMIT", 9)
    body = app.test_client().get("/instructions").get_data(as_text=True)
    assert "Free 9 a day" in body


def test_learning_path_levels_and_plans_match_the_gates(page):
    plan = {"free": "Free", "basic": "Thai Reader", "pro": "Thai Master"}
    rows = re.findall(r'<td><a href="(/[^"]*)">[^<]+</a></td>\s*<td>Level (\d+)</td>\s*<td>([^<]+)</td>', page)
    assert len(rows) >= 15, "the learning path table has gone missing"
    urls = {url for url, _, _ in rows}
    assert {"/alphabet", "/paiboon", "/survival", "/sentences", "/dictionary"} <= urls
    by_url = {
        "/alphabet": "alphabet", "/paiboon": "paiboon", "/survival": "survival",
        "/learn": "learn", "/tones-classes": "tones_classes", "/sentences": "sentences",
        "/dictionary": "dictionary",
    }
    for url, level, tier_word in rows:
        if url in by_url:
            req = SECTION_REQUIREMENTS[by_url[url]]
            assert int(level) == req["level"], url
            assert tier_word == plan[req["tier"]], url


def test_the_learning_support_anchor_survives(page):
    """base.html's Learning Support box links to /instructions#learning-support."""
    assert 'id="learning-support"' in page


def test_every_link_on_the_page_leads_somewhere(page):
    client = app.test_client()
    paths = sorted({href.split("#")[0] for href in re.findall(r'href="(/[^"]*)"', page)} - {""})
    assert paths
    broken = [p for p in paths if client.get(p).status_code == 404]
    assert not broken, f"links to missing pages: {broken}"


def test_the_guide_links_to_the_original_cards(page):
    for anchor in ("monk-mode", "learning-support", "tips"):
        assert f'href="#{anchor}"' in page
        assert f'id="{anchor}"' in page
