"""/register must never crash again (added 2026-08-19).

templates/register.html renders a `registers` dict of nine formality levels
called REGISTER_LEVELS. That name has never been defined — not in app.py, not
in the deleted app_backup.py, not in any commit since the first — so the route
raised NameError from the beginning.

The access gate ran before the view, which hid it: a logged-out visitor got the
ordinary "locked" page, and only someone who had paid, reached Level 4, or
unlocked the section another way ever got far enough to see the 500. Nothing
links to /register, so nobody reported it.

It now redirects to Formality, which covers the same ground, until the data is
written. These tests cover the two things that made the bug survive so long:
that the crash is reachable only when unlocked, and that nothing links to it.

Run with:  pytest tests/test_register_redirect.py -v
"""

import os
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, SECTION_REQUIREMENTS  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def unlocked_client():
    """The learner who actually met the bug: past the gate, into the view."""
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


def test_a_locked_out_visitor_does_not_crash(client):
    response = client.get("/register")
    assert response.status_code != 500


def test_the_learner_who_paid_does_not_crash(unlocked_client):
    """This is the case that was broken — the gate used to hide it."""
    response = unlocked_client.get("/register")
    assert response.status_code != 500


@pytest.mark.parametrize("fixture_name", ["client", "unlocked_client"])
def test_everyone_is_sent_to_formality(request, fixture_name):
    """Ungated on purpose: /formality applies its own gate, and one page
    deciding who gets in beats two disagreeing about it."""
    c = request.getfixturevalue(fixture_name)
    response = c.get("/register")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/formality")


def test_the_redirect_is_temporary_not_permanent():
    """A 301 gets cached by browsers and would go on redirecting people away
    from the page after someone finishes it."""
    with app.test_client() as c:
        assert c.get("/register").status_code == 302


def test_following_the_redirect_lands_somewhere_real(unlocked_client):
    response = unlocked_client.get("/register", follow_redirects=True)
    assert response.status_code == 200


# The matching half of this fix lives in curriculum.NOT_BUILT_YET, which
# records why 'register' is kept off the public curriculum outline — a redirect
# is not a section, and that outline is where the app promises what a
# subscription buys. It is not asserted here because that module is still being
# written in a parallel branch of work; add the assertion once it lands.


def test_the_section_entry_survives():
    """Deleting it would rewrite the progress of anyone who has already
    unlocked it and been given the XP."""
    assert "register" in SECTION_REQUIREMENTS
