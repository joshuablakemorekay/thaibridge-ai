"""The Dhamma path stays open to a non-Thai visitor (added 2026-08-19).

A learner who came for Buddhism told us the site felt like Thai culture was the
price of admission. The permissions were already right — every Buddhism page is
free, level 1, with no alphabet prerequisite — but nothing on screen said so,
and the home page actively said the opposite ("pass the quiz to unlock the
site").

The copy has been fixed. These tests guard the promise underneath it, because
copy and permissions can drift apart again silently: the wording is only honest
for as long as the gates stay open.

Run with:  pytest tests/test_dhamma_open_to_all.py -v
"""

import os
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, SECTION_REQUIREMENTS  # noqa: E402

# Everything a visitor here for Buddhism alone needs to reach. Paiboon is on the
# list because the chanting book prints it — it is the key to notation already
# on a free page, not a language lesson.
DHAMMA_SECTIONS = [
    "theravada",
    "meditation",
    "chanting",
    "paiboon",
    "dhamma_and_culture",
    "practising_anywhere",
]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.mark.parametrize("section", DHAMMA_SECTIONS)
def test_the_dhamma_pages_ask_for_no_thai_and_no_money(section):
    """The three ways a page can be shut: level, tier, and the alphabet quiz."""
    requirements = SECTION_REQUIREMENTS[section]
    assert requirements["level"] == 1, f"{section} now needs levelling up"
    assert requirements["tier"] == "free", f"{section} has moved behind a paywall"
    assert not requirements.get("requires_alphabet", False), (
        f"{section} now demands the Thai alphabet first — which is exactly the "
        "barrier the explanation page tells visitors does not exist"
    )


@pytest.mark.parametrize("path", [
    "/theravada",
    "/meditation",
    "/chanting",
    "/paiboon",
    "/dhamma-and-culture",
    "/practising-anywhere",
])
def test_a_logged_out_stranger_can_read_them(client, path):
    """No account, no progress, no Thai. The end-to-end version of the above."""
    response = client.get(path)
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # locked.html renders this heading. A bare "locked" would also match the
    # footer's dictionary tooltip, which is on every page including this one.
    assert "<h1>Section Locked</h1>" not in body, f"{path} served the locked page"


def test_the_home_page_no_longer_claims_the_alphabet_unlocks_everything(client):
    """The single sentence that told a Dhamma visitor to learn Thai first."""
    body = client.get("/").get_data(as_text=True)
    assert "unlock the site" not in body


def test_the_home_page_offers_a_way_in_that_is_not_the_alphabet(client):
    body = client.get("/").get_data(as_text=True)
    assert "What are you here to learn?" in body
    assert "/theravada" in body, "no Dhamma door on the home page"


# ── The culturally neutral path stays named on the front page ─────────────
#
# Added 2026-08-19 after it went missing once. A hero draft promised freedom in
# general terms — "find your own way to bring the teachings into your life" —
# and dropped the option of practising without adopting any cultural identity
# at all. The objection at the time was to the phrase "follow no culture at
# all", which contradicts what /dhamma-and-culture argues (no Buddhism sits
# anywhere culture-free). That was an objection to six words, but it took the
# option with it, and nothing failed. A general promise of freedom is not the
# same as naming the option, so the naming is what these tests pin down.


def test_the_home_page_names_the_culturally_neutral_path(client):
    """Not "you are free" in the abstract — the actual option, in words."""
    body = client.get("/").get_data(as_text=True)
    assert "without adopting any particular cultural identity" in body, (
        "the home page no longer offers practising the Dhamma without taking "
        "on a culture — the promise is only kept for as long as it is named"
    )


def test_the_home_page_offers_the_thai_expression_too(client):
    """The other branch. Neither one is allowed to swallow the other."""
    body = client.get("/").get_data(as_text=True)
    assert "Theravada tradition" in body
    assert "honoured" in body, (
        "Thai heritage must read as something given, not as the thing being "
        "declined — see prompts/hero-copy-rewrite/REASONING.md"
    )


def test_the_home_page_does_not_claim_a_culture_free_buddhism(client):
    """The wording /dhamma-and-culture spends a section arguing against."""
    body = client.get("/").get_data(as_text=True)
    assert "no culture at all" not in body


def test_the_explanation_page_says_the_thing_it_exists_to_say(client):
    body = client.get("/dhamma-and-culture").get_data(as_text=True)
    assert "You do not need to become Thai" in body
    assert "examples, not instructions" in body


def test_the_chanting_book_tells_readers_the_thai_layers_are_optional(client):
    """Five layers of script look compulsory unless something says otherwise."""
    body = client.get("/chanting").get_data(as_text=True)
    assert "You do not need to read Thai to use this book" in body


# ── The universality of the "practise anywhere" page ──────────────────────
#
# The first draft of this page was going to illustrate lay practice with
# "practising the precepts in Britain". That is the original problem wearing a
# different flag: swapping one country for another still tells the reader the
# practice belongs somewhere in particular. The page is built from the Canon's
# own frameworks instead, and these tests keep it that way.

# Countries and peoples that could only ever appear here as "here is where you
# would do this" — i.e. as a stand-in setting for the reader's own life.
#
# SCOPE: this list is checked against /practising-anywhere ONLY, and that is
# deliberate. /about carries the author's own first-person note on preserving
# Thai and British cultural heritage, which names both countries on purpose —
# it is a statement about who wrote the app, not a claim about where practice
# belongs. Do not widen this check to the whole site to "fix" a failure; that
# would delete signed authorship to satisfy a test aimed at something else.
PAROCHIAL_SETTINGS = [
    "Britain", "British", "England", "English people", "UK",
    "America", "American", "USA", "Europe", "European",
    "Germany", "German", "France", "French", "Australia", "Australian",
    "the West", "Western world",
]


def page_content(client, path):
    """Just the page's own <main>, without the shared layout.

    base.html carries a British/American ACCENT switch for the monk audio,
    which is a real feature and not a claim about where practice belongs.
    Scanning the whole document would flag it every time.
    """
    body = client.get(path).get_data(as_text=True)
    start = body.index("<main>") + len("<main>")
    return body[start:body.index("</main>", start)]


@pytest.mark.parametrize("word", PAROCHIAL_SETTINGS)
def test_the_practice_page_names_no_country_as_the_setting(client, word):
    body = page_content(client, "/practising-anywhere")
    assert word not in body, (
        f"{word!r} appears on the page whose whole point is that the practice "
        "belongs to no country in particular"
    )


def test_the_practice_page_is_built_on_canonical_frameworks(client):
    """The frameworks are what make it universal without needing examples."""
    body = client.get("/practising-anywhere").get_data(as_text=True)
    assert "Sigālovāda" in body, "the six directions are the page's backbone"
    assert "pañca-sīla" in body
    assert "puñña-kiriya-vatthu" in body
    assert "brahmavihāras" in body


def test_the_practice_page_states_what_is_not_required(client):
    """An unstated requirement is the one a reader assumes is there."""
    body = client.get("/practising-anywhere").get_data(as_text=True)
    assert "What you do not need" in body
    assert "to speak Thai, Pali, or any language other than your own" in body


# ── Monk Mode does not assume a hemisphere ────────────────────────────────
#
# The non-Thai side of the monk track was described throughout as "Western
# monks". That was never the actual criterion — the lessons are for monks
# learning Thai, who come from Sri Lanka, Myanmar, Cambodia, Laos, Indonesia,
# India, Brazil and everywhere else. The switch is about DIRECTION, so it is
# described by direction now.

MONK_SURFACES = ["/monk-mode"]


@pytest.mark.parametrize("path", MONK_SURFACES)
def test_monk_mode_does_not_label_monks_by_where_they_are_from(client, path):
    body = client.get(path).get_data(as_text=True)
    for phrase in ["Western monk", "Western Buddhist monk", "Westerner"]:
        assert phrase not in body, (
            f"{phrase!r} is back on {path} — the criterion is which language a "
            "monk is learning, not which half of the world they live in"
        )


def test_monk_mode_still_says_who_the_track_is_for(client):
    """Removing "Western" must not remove the meaning with it."""
    body = client.get("/monk-mode").get_data(as_text=True)
    assert "Thai Buddhist monks learning English" in body
    assert "learning Thai" in body


# ── No one is described by what they are not ──────────────────────────────
#
# "Foreigner" became "non-Thai", which was politer and structurally the same
# move — both define a reader by not belonging. Nearly every sentence carrying
# the label already addressed the reader as "you", so the label was redundant
# and was dropped rather than renamed. These pages must not grow it back.

OTHERING_LABELS = ["foreigner", "Foreigner", "non-Thai", "Non-Thai"]

# Culture and Formality are Basic-tier, so a logged-out client is served the
# locked page — and a locked page trivially passes a "this word is absent"
# test. These have to be checked with the content actually on screen.
LEARNER_FACING_PAGES = ["/culture", "/formality", "/monk-mode", "/"]


@pytest.mark.parametrize("path", LEARNER_FACING_PAGES)
@pytest.mark.parametrize("label", OTHERING_LABELS)
def test_no_page_defines_a_reader_by_what_they_are_not(unlocked_client, path, label):
    client = unlocked_client
    assert label not in page_content(client, path), (
        f"{label!r} is back on {path} — say \"you\", or say what someone is "
        "learning, rather than naming what they are not"
    )


def test_the_etiquette_guidance_still_addresses_the_reader(unlocked_client):
    """Dropping the label must not drop the guidance with it."""
    body = page_content(unlocked_client, "/culture")
    assert "Guidelines for Learners" in body
    assert "wai" in body.lower()


# ── Culture is a choice, and one of the choices is "none" ─────────────────
#
# The second round of feedback went past "you do not have to be Thai". It asked
# for something the page did not offer at all: the option of practising the
# Dhamma without taking on ANY culture or tradition, including the reader's own.
# Every sentence on the page said "in your own culture", which quietly assumes
# a reader who wants to belong somewhere.

def test_the_explanation_page_offers_belonging_to_no_culture_at_all(client):
    body = page_content(client, "/dhamma-and-culture")
    assert "Culturally neutral" in body, "the third way in is missing"
    # The sentence wraps in the template, so match the tail of it rather than
    # a span that a line break sits inside.
    assert "cultural identity or tradition" in body


def test_the_practice_page_lists_culture_itself_as_optional(client):
    """The "what you do not need" list is where a reader checks for the catch."""
    body = page_content(client, "/practising-anywhere")
    assert "including no culture at all" in body
    assert "or to call yourself anything" in body


# ── Four layers, not two ──────────────────────────────────────────────────
#
# The page used to set the Dhamma against Thai culture, two columns, equal
# weight. That comparison was right as far as it went and hid two further
# distinctions: HOW the teaching was carried here (Theravada — a chain of
# transmission, not a set of customs) and what the reader chooses to do with
# any of it.

LAYERS = [
    "The core Dhamma",
    "The Theravada tradition",
    "Thai Buddhist culture",
    "What you do with any of it",
]


@pytest.mark.parametrize("layer", LAYERS)
def test_the_page_keeps_the_four_layers_apart(client, layer):
    assert layer in page_content(client, "/dhamma-and-culture")


def test_theravada_is_described_as_transmission_not_as_a_culture(client):
    """A reader who thinks Theravada IS a culture has the same objection back."""
    body = page_content(client, "/dhamma-and-culture")
    assert "Not the teaching, but the vessel that carried it" in body
    assert "transmission and preservation" in body


# ── The three approaches, and that they are not exclusive ────────────────

APPROACHES = ["Universal Dhamma", "Dhamma in Thai culture", "Culturally neutral"]


@pytest.mark.parametrize("approach", APPROACHES)
def test_all_three_approaches_are_offered(client, approach):
    assert approach in page_content(client, "/dhamma-and-culture")


def test_the_approaches_are_stated_not_to_be_exclusive(client):
    """Three doors read as three boxes to be sorted into unless it says so."""
    assert "They are not exclusive." in page_content(client, "/dhamma-and-culture")


def test_the_signup_page_does_not_promise_only_a_language_course(client):
    """The one line everyone passes through on the way in."""
    body = client.get("/signup").get_data(as_text=True)
    assert "begin your Thai language journey" not in body
    assert "the Thai language" in body and "Dhamma" in body
