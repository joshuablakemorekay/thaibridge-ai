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


def test_it_is_titled_as_the_help_page(page):
    assert "<title>Help: how to use ThaiBridge AI" in page


def test_every_section_follows_the_four_part_shape(page):
    """What it's for · Where to start · Step by step · In short, in every
    guide section after the overview, so each one reads the same way."""
    for anchor in ["chanting", "account", "learning-path", "buddhism",
                   "ai-tutor", "levels", "plans", "monk-mode"]:
        start = page.index(f'id="{anchor}"')
        end = page.find('<div class="card"', start + 1)
        section = page[start:end if end != -1 else None]
        for part in ["What it's for", "Where to start", "Step by step", "In short:"]:
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


def test_no_developer_layout_table(page):
    """The page-layout table was a note for builders, not learners."""
    assert "Full-width tool" not in page


def test_every_link_on_the_page_leads_somewhere(page):
    client = app.test_client()
    paths = sorted({href.split("#")[0] for href in re.findall(r'href="(/[^"]*)"', page)} - {""})
    assert paths
    broken = [p for p in paths if client.get(p).status_code == 404]
    assert not broken, f"links to missing pages: {broken}"


def test_footer_and_menu_both_say_help(page):
    assert '<a href="/instructions">ℹ️ Help</a>' in page
    assert '<a href="/instructions">Help</a> •' in page
