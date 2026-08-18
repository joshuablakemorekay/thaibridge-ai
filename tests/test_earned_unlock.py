"""Tests for the earned unlock (added 2026-08-18).

The problem it exists to solve: every free-tier section is level 1, so XP a
free learner earned unlocked nothing whatsoever. The progress bar filled toward
a reward that did not exist. Reaching Level 3 now earns one Thai Reader section
of their choosing, permanently and free.

The rules worth protecting are the narrow ones — it opens ONE section, only a
Basic one, only a section whose level they already meet, and it never waives
the level gate for anything.
"""

import os
import uuid
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import (  # noqa: E402
    app, db, User, EARNED_UNLOCK_LEVEL, SECTION_REQUIREMENTS,
)

PASSWORD = "TestPass123"

# Level 2, Basic — reachable at EARNED_UNLOCK_LEVEL, so spendable.
SPENDABLE = "read_write"
# Level 5, Basic — too high to spend on at level 3.
TOO_HIGH = "sentences"
# Pro, never spendable.
PRO_ONLY = "dictionary"


@pytest.fixture
def account():
    username = f"eu{uuid.uuid4().hex[:10]}"
    client = app.test_client()
    response = client.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    }).get_json()
    assert response.get("success"), f"signup failed: {response.get('message')}"
    try:
        yield client, username
    finally:
        with app.app_context():
            row = User.query.filter_by(username=username).first()
            if row:
                db.session.delete(row)
                db.session.commit()


def set_level(client, level):
    """Put this browser at a level."""
    client.get("/")                       # make sure a session exists to edit
    with client.session_transaction() as session_data:
        progress = session_data.setdefault("user_progress", {})
        progress["level"] = level
        session_data["user_progress"] = progress


def pass_the_alphabet(username):
    """Clear gate 1 for real.

    The alphabet gate reads the User column, not the session, so a cookie edit
    will not do it — which is the point of that column.
    """
    with app.app_context():
        row = User.query.filter_by(username=username).first()
        row.alphabet_completed = True
        db.session.commit()


def spent_on(username):
    with app.app_context():
        return User.query.filter_by(username=username).first().earned_unlock_section


def test_the_fixture_sections_are_still_shaped_as_the_tests_assume():
    """If someone re-levels these, the tests below would pass vacuously."""
    assert SECTION_REQUIREMENTS[SPENDABLE]["tier"] == "basic"
    assert SECTION_REQUIREMENTS[SPENDABLE]["level"] <= EARNED_UNLOCK_LEVEL
    assert SECTION_REQUIREMENTS[TOO_HIGH]["level"] > EARNED_UNLOCK_LEVEL
    assert SECTION_REQUIREMENTS[PRO_ONLY]["tier"] == "pro"


def test_the_offer_appears_once_the_level_is_reached(account):
    client, _ = account
    set_level(client, EARNED_UNLOCK_LEVEL)
    page = client.get(f"/{SPENDABLE}").get_data(as_text=True)
    assert "You've earned an unlock" in page


def test_no_offer_below_the_level(account):
    client, _ = account
    set_level(client, EARNED_UNLOCK_LEVEL - 1)
    page = client.get(f"/{SPENDABLE}").get_data(as_text=True)
    assert "You've earned an unlock" not in page


def test_claiming_opens_the_section(account):
    client, username = account
    pass_the_alphabet(username)
    set_level(client, EARNED_UNLOCK_LEVEL)

    client.post(f"/unlock/earned/{SPENDABLE}")
    assert spent_on(username) == SPENDABLE

    response = client.get(f"/{SPENDABLE}")
    assert response.status_code == 200
    assert "Section Locked" not in response.get_data(as_text=True)


def test_it_opens_that_section_and_no_other(account):
    """The whole design: one door, not the tier."""
    client, username = account
    pass_the_alphabet(username)
    set_level(client, EARNED_UNLOCK_LEVEL)
    client.post(f"/unlock/earned/{SPENDABLE}")

    other = client.get("/grammar").get_data(as_text=True)
    assert "Section Locked" in other


def test_it_cannot_be_spent_twice(account):
    client, username = account
    set_level(client, EARNED_UNLOCK_LEVEL)
    client.post(f"/unlock/earned/{SPENDABLE}")
    client.post("/unlock/earned/grammar")
    assert spent_on(username) == SPENDABLE, "a second claim moved the unlock"


def test_it_cannot_be_spent_above_your_level(account):
    """Otherwise the one unlock is burned on a door the level gate keeps shut."""
    client, username = account
    set_level(client, EARNED_UNLOCK_LEVEL)
    client.post(f"/unlock/earned/{TOO_HIGH}")
    assert spent_on(username) is None


def test_it_cannot_be_spent_on_a_pro_section(account):
    client, username = account
    set_level(client, 10)
    client.post(f"/unlock/earned/{PRO_ONLY}")
    assert spent_on(username) is None


def test_it_cannot_be_claimed_below_the_level(account):
    client, username = account
    set_level(client, EARNED_UNLOCK_LEVEL - 1)
    client.post(f"/unlock/earned/{SPENDABLE}")
    assert spent_on(username) is None


def test_a_signed_out_visitor_cannot_claim_one():
    """It lives in a column, not a cookie — otherwise clearing cookies mints
    a fresh section every time."""
    client = app.test_client()
    client.get("/")
    set_level(client, EARNED_UNLOCK_LEVEL)
    response = client.post(f"/unlock/earned/{SPENDABLE}")
    assert response.status_code in (302, 401)
    assert "/login" in response.headers.get("Location", "")


def test_a_poisoned_progress_blob_cannot_grant_one(account):
    """The browser must not be able to hand itself an unlock by editing the
    session, the way it could if this were a progress key."""
    client, username = account
    with client.session_transaction() as session_data:
        progress = session_data["user_progress"]
        progress["earned_unlock_section"] = TOO_HIGH
        session_data["user_progress"] = progress

    page = client.get(f"/{TOO_HIGH}").get_data(as_text=True)
    assert "Section Locked" in page
    assert spent_on(username) is None
