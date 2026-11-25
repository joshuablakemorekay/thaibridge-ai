"""Sign-ups remember which ad brought them.

The ad links carry ?utm_source=... but the learner never signs up on the page
they land on. These tests follow a visitor from the ad, around the site, to the
sign-up form, and check the tag arrives on the account — and that a visitor
with no tag, or a junk tag, does no harm.
"""
import uuid

import pytest

import signup_source
from app import app
from models import User, db

PASSWORD = "TestPass123"


def sign_up(client):
    username = f"src_{uuid.uuid4().hex[:10]}"
    result = client.post("/signup", json={
        "username": username, "email": f"{username}@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    }).get_json()
    assert result["success"], result
    with app.app_context():
        return db.session.query(User).filter_by(username=username).one()


def test_tag_survives_browsing_before_sign_up():
    client = app.test_client()
    client.get("/?utm_source=tiktok&utm_campaign=understand-every-chant")
    client.get("/chanting")
    client.get("/signup")
    user = sign_up(client)
    assert user.signup_source == "tiktok"
    assert user.signup_campaign == "understand-every-chant"


def test_first_tag_wins():
    """A later ad click in the same session does not steal the sign-up."""
    client = app.test_client()
    client.get("/?utm_source=tiktok")
    client.get("/?utm_source=facebook&utm_campaign=other")
    user = sign_up(client)
    assert user.signup_source == "tiktok"
    assert user.signup_campaign is None


def test_no_tag_leaves_the_columns_empty():
    client = app.test_client()
    client.get("/")
    user = sign_up(client)
    assert user.signup_source is None
    assert user.signup_campaign is None


@pytest.mark.parametrize("raw, stored", [
    ("TikTok", "tiktok"),
    ("  Facebook ", "facebook"),
    ("x.com", "x.com"),
    ("<script>alert(1)</script>", "scriptalert1script"),
    ("a" * 200, "a" * signup_source.MAX_LENGTH),
    ("!!!", None),
    ("", None),
    (None, None),
])
def test_clean(raw, stored):
    assert signup_source.clean(raw) == stored


def test_junk_tag_is_not_remembered():
    client = app.test_client()
    client.get("/?utm_source=%21%21%21")
    user = sign_up(client)
    assert user.signup_source is None


def test_counts_groups_by_source_and_campaign():
    client = app.test_client()
    client.get("/?utm_source=youtube-test-count&utm_campaign=c1")
    first = sign_up(client)
    client = app.test_client()
    client.get("/?utm_source=youtube-test-count&utm_campaign=c1")
    sign_up(client)
    with app.app_context():
        rows = signup_source.counts(since=first.created_at)
    assert ("youtube-test-count", "c1", 2) in rows


def test_tiktok_short_address_forwards_with_its_tag():
    # Links in TikTok captions can't be tapped, so the caption gives the
    # short, typeable jaiway.smoald.com/tiktok instead of a long ?utm_ link.
    client = app.test_client()
    response = client.get("/tiktok")
    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        "/tour-guide?utm_source=tiktok&utm_campaign=caption")
    client.get(response.headers["Location"])
    client.get("/signup")
    user = sign_up(client)
    assert user.signup_source == "tiktok"
    assert user.signup_campaign == "caption"
