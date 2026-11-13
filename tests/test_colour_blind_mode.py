"""Learning Support's "Colour-blind friendly colours" option.

The quizzes mark right answers green and wrong ones red, the pair that
red-green colour blindness can't separate. The option swaps them for blue and
orange. These tests check the toggle is wired end to end (panel checkbox,
the before-paint script, base.js), that the swapped colours stay readable,
and that every quiz selector the CSS recolours still exists, so renaming a
class on a quiz page can't quietly switch the feature off for that page.
"""
import pathlib
import re
from pathlib import Path

import pytest

from app import app

ROOT = Path(__file__).resolve().parent.parent
BASE_CSS = (ROOT / "static/css/base.css").read_text(encoding="utf-8")
BASE_JS = (ROOT / "static/js/base.js").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def home():
    return app.test_client().get("/").get_data(as_text=True)


def test_the_panel_offers_the_option(home):
    assert 'id="rs-colour"' in home
    assert "Colour-blind friendly colours" in home


def test_a_saved_choice_applies_before_the_page_paints(home):
    """Without this the quiz would flash green/red on every page load.

    The early script is a file now (inline scripts were moved out for the
    Content-Security-Policy). It still has to load in the <head>, before the
    body paints, so check where the page loads it as well as what it does."""
    head = home.split("</head>")[0]
    assert "js/pages/reading-support-early.js" in head
    early = (pathlib.Path(__file__).resolve().parent.parent
             / "static" / "js" / "pages" / "reading-support-early.js").read_text(encoding="utf-8")
    assert "if (s.colour)  el.classList.add('rs-colour');" in early


def test_base_js_saves_and_resets_the_option():
    options = re.search(r"var OPTIONS = \[([^\]]*)\]", BASE_JS).group(1)
    assert "'colour'" in options


def test_the_help_page_explains_it():
    page = app.test_client().get("/instructions").get_data(as_text=True)
    assert "Colour-blind friendly colours" in page


# ── Contrast ──────────────────────────────────────────────────────────────

def _luminance(hex_colour):
    raw = hex_colour.lstrip("#")
    channels = [int(raw[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
              for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(a, b):
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def _palette():
    block = re.search(r"html\.rs-colour \{([^}]*)\}", BASE_CSS).group(1)
    return dict(re.findall(r"--(cb-[a-z-]+):\s*(#[0-9A-Fa-f]{6})", block))


@pytest.mark.parametrize("ink", ["cb-good", "cb-bad"])
@pytest.mark.parametrize("paper", ["#FFFFFF", "cb-good-bg", "cb-bad-bg"])
def test_the_swapped_colours_pass_aa(ink, paper):
    """They are used as text on pale tints and as backgrounds for white text."""
    colours = _palette()
    paper_hex = colours.get(paper, paper)
    ratio = _contrast(colours[ink], paper_hex)
    assert ratio >= 4.5, f"{ink} on {paper} is {ratio:.2f}:1, below AA"


# ── Coverage ──────────────────────────────────────────────────────────────

# Each class the colour-blind CSS targets, and the file that defines it.
QUIZ_SELECTORS = {
    ".abc-option.is-correct": "static/css/alphabet.css",
    ".abc-option.is-wrong": "static/css/alphabet.css",
    ".abc-feedback.is-correct": "static/css/alphabet.css",
    ".abc-feedback.is-wrong": "static/css/alphabet.css",
    ".abc-result-verdict.is-pass": "static/css/alphabet.css",
    ".abc-result-verdict.is-fail": "static/css/alphabet.css",
    ".opt-btn.correct": "templates/tones_classes.html",
    ".opt-btn.wrong": "templates/tones_classes.html",
    ".listen-option.is-right": "templates/sentences.html",
    ".listen-option.is-wrong": "templates/sentences.html",
    ".sb-result.right": "templates/sentences.html",
    ".sb-result.wrong": "templates/sentences.html",
    ".qa-yes .qa-label": "templates/sentences.html",
    ".qa-no .qa-label": "templates/sentences.html",
    ".pron-heard.is-right": "templates/exercise.html",
    "#quizContent": "templates/exercise.html",
}


@pytest.mark.parametrize("selector, source", QUIZ_SELECTORS.items())
def test_every_recoloured_selector_is_still_real(selector, source):
    assert f"html.rs-colour {selector}" in BASE_CSS, f"{selector} not recoloured"
    text = (ROOT / source).read_text(encoding="utf-8")
    if selector.startswith("#"):
        assert f'id="{selector[1:]}"' in text, f"{selector} gone from {source}"
    else:
        assert selector in text, f"{selector} gone from {source}"


def test_chanting_spelling_layer_turns_blue_in_colour_blind_mode():
    """Green ThaiBridge Spelling and clay Pali (Romanised) are both italic
    Latin text, and look almost the same with red-green colour blindness."""
    import chanting
    layer = next(l for l in chanting.CHANT_LAYERS if l["key"] == "paiboon")
    assert layer["colour"].startswith("var(--cb-paiboon,")
    assert "cb-paiboon" in _palette()


def test_calendar_christian_marks_change_shape():
    """Purple and blue dots are too alike to rely on, so shape does the work."""
    text = (ROOT / "templates/calendar.html").read_text(encoding="utf-8")
    assert "html.rs-colour .dot-christian { background: transparent;" in text
    assert "html.rs-colour .cal-grid .cal-ev.cat-christian,\n" in text
    assert "html.rs-colour .cal-legend .cat-christian::before { background: transparent;" in text


def test_phone_bars_use_strong_colours_for_everyone():
    """The pale tints scored 8.1 apart even with normal colour vision."""
    text = (ROOT / "templates/calendar.html").read_text(encoding="utf-8")
    phone = text.split("Phones, for everyone")[1]
    for rule in (".cal-grid .cal-ev.cat-buddhist { background: #E08A00; }",
                 ".cal-grid .cal-ev.cat-christian { background: #2E7DB5; }"):
        assert "        " + rule in phone


def test_listening_answers_show_a_tick_or_cross():
    """These were the one quiz that marked answers by colour alone."""
    text = (ROOT / "templates/sentences.html").read_text(encoding="utf-8")
    assert '.listen-option.is-right::after { content: " ✓"' in text
    assert '.listen-option.is-wrong::after { content: " ✗"' in text
