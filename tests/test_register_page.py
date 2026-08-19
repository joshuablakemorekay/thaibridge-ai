"""/register serves the nine formality registers (added 2026-08-19).

History worth keeping, because it explains what these tests are guarding:
templates/register.html renders a `registers` dict called REGISTER_LEVELS, and
that name was never defined — not in app.py, not in the deleted app_backup.py,
not in any commit since the first. The route raised NameError from the
beginning. The access gate ran before the view, so a logged-out visitor got the
ordinary "locked" page and only someone who had paid or reached Level 4 ever
saw the 500. Nothing linked to it, so nobody reported it.

The data now exists in register_levels.py and the page renders.

Run with:  pytest tests/test_register_page.py -v
"""

import html
import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import curriculum  # noqa: E402
import register_levels  # noqa: E402
from app import app, SECTION_REQUIREMENTS  # noqa: E402

REGISTERS = register_levels.REGISTER_LEVELS

# The order the template hard-codes, monastic (1) down to vulgar (9).
EXPECTED_ORDER = [
    "monastic", "royal", "obsolete", "literary", "technical",
    "formal", "neutral", "casual", "vulgar",
]

# Every key templates/register.html reads on each register.
REQUIRED_FIELDS = [
    "level", "name", "thai", "icon", "color", "description",
    "usage_context", "social_notes", "examples", "warning",
]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def unlocked_client():
    """The learner who met the original crash: past the gate, into the view."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess["user_progress"] = {
                "xp": 9999, "level": 10, "subscription_tier": "basic",
                "is_developer": False, "monk_mode": False, "full_unlock": True,
                "alphabet_completed": True,
                "sections_unlocked": [], "sections_visited": [],
            }
        yield c


def test_the_learner_who_paid_gets_the_page_not_a_crash(unlocked_client):
    """The regression this whole file exists for."""
    response = unlocked_client.get("/register")
    assert response.status_code == 200


def test_a_locked_out_visitor_gets_the_locked_page_not_a_crash(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_all_nine_registers_reach_the_page(unlocked_client):
    body = unlocked_client.get("/register").get_data(as_text=True)
    for key in EXPECTED_ORDER:
        # Escaped, because Jinja autoescapes: "Archaic & Ceremonial" reaches
        # the page as "Archaic &amp; Ceremonial".
        name = html.escape(REGISTERS[key]["name"])
        assert name in body, f"{key} missing from the page"


def test_the_registers_are_a_complete_ladder_of_nine():
    assert list(REGISTERS) == EXPECTED_ORDER
    assert [r["level"] for r in REGISTERS.values()] == list(range(1, 10))


@pytest.mark.parametrize("key", EXPECTED_ORDER)
def test_each_register_carries_every_field_the_template_reads(key):
    """A missing key renders as empty in Jinja rather than raising, so a hole
    here would ship as a blank paragraph nobody noticed."""
    register = REGISTERS[key]
    missing = [f for f in REQUIRED_FIELDS if f not in register]
    assert not missing, f"{key} is missing {missing}"
    assert register["examples"], f"{key} has no examples"
    for example in register["examples"]:
        for field in ("thai", "paiboon", "english"):
            assert field in example, f"{key} example missing {field}"
        assert "note" in example or "polite" in example, (
            f"{key} example {example['thai']!r} has neither note nor polite form")


def test_the_casual_register_keeps_its_two_sub_levels():
    """8A and 8B are rendered by their own blocks in the template."""
    casual = REGISTERS["casual"]
    for key in ("sub_level_a", "sub_level_b"):
        assert key in casual
        for field in ("name", "note", "examples"):
            assert field in casual[key], f"{key} missing {field}"


def test_the_vulgar_register_keeps_its_background_note():
    """Its own block in the template, and the part that explains why these
    words can carry affection as well as insult."""
    assert REGISTERS["vulgar"].get("cultural_notes")


def test_the_section_is_on_the_curriculum_outline_now_it_is_built():
    assert "register" in SECTION_REQUIREMENTS
    assert "register" not in curriculum.NOT_BUILT_YET



def test_the_page_invites_corrections(unlocked_client):
    """Register varies by region, age and setting more than most of the
    language, so a route for corrections belongs here permanently — not as a
    notice to be removed once someone has signed it off."""
    body = unlocked_client.get("/register").get_data(as_text=True)
    assert "corrections are welcome" in body
    assert "/contact" in body


def test_the_royal_register_still_carries_its_legal_warning(unlocked_client):
    """The one register where a learner's mistake is a legal matter rather
    than a social one. This warning is not decoration."""
    body = unlocked_client.get("/register").get_data(as_text=True)
    assert "112" in body
    assert "Read it, do not write it." in body
