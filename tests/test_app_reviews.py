"""The in-app review prompt (app_reviews.py).

Who sees the card on /progress, what saving a review stores, that a second
send updates rather than duplicates, and that the private list stays private.

Run with:  pytest tests/test_app_reviews.py -v
"""
import uuid
from datetime import date, timedelta

import pytest

from app import app
from app_reviews import REVIEW_SNOOZE_DAYS, SNOOZE_KEY
from models import AppReview, User, db
from flask import session

import progress
from tests.conftest import UNLOCKED_PROGRESS

CARD = b'id="review-prompt"'


@pytest.fixture
def account():
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"rv_{tag}", email=f"rv_{tag}@example.com", password_hash="x")
        db.session.add(u)
        db.session.commit()
        uid, version = u.id, u.session_version or 0
    yield {"id": uid, "login_id": f"{uid}:{version}"}
    with app.app_context():
        AppReview.query.filter_by(user_id=uid).delete()
        User.query.filter_by(id=uid).delete()
        db.session.commit()


def fresh_progress():
    """A new learner's full progress dict, so /progress has every field it shows."""
    with app.test_request_context():
        progress.init_user_progress()
        return dict(session["user_progress"])


def client_for(account=None, **overrides):
    app.config["TESTING"] = True
    client = app.test_client()
    with client.session_transaction() as s:
        s["user_progress"] = {**fresh_progress(), **UNLOCKED_PROGRESS,
                              "level": 3, "xp": 300, **overrides}
        if account:
            s["_user_id"] = account["login_id"]
            s["_fresh"] = True
    return client


def saved(uid):
    with app.app_context():
        return AppReview.query.filter_by(user_id=uid).all()


# --- who is asked -------------------------------------------------------------

def test_level_3_account_sees_the_card(account):
    assert CARD in client_for(account).get("/progress").data


def test_below_level_3_is_not_asked(account):
    assert CARD not in client_for(account, level=2, xp=150).get("/progress").data


def test_signed_out_visitor_is_not_asked():
    assert CARD not in client_for().get("/progress").data


def test_not_now_hides_it_then_it_comes_back(account):
    recent = date.today().isoformat()
    assert CARD not in client_for(account, **{SNOOZE_KEY: recent}).get("/progress").data
    old = (date.today() - timedelta(days=REVIEW_SNOOZE_DAYS + 1)).isoformat()
    assert CARD in client_for(account, **{SNOOZE_KEY: old}).get("/progress").data


def test_snooze_route_records_the_date(account):
    client = client_for(account)
    assert client.post("/api/review/snooze", json={}).status_code == 200
    with client.session_transaction() as s:
        assert s["user_progress"][SNOOZE_KEY] == date.today().isoformat()


# --- what is saved ------------------------------------------------------------

def test_review_is_saved_and_the_card_goes(account):
    client = client_for(account)
    r = client.post("/api/review", json={"rating": 4, "comment": "  Very useful  ",
                                         "can_publish": True, "display_name": "Sam, Leeds"})
    assert r.get_json()["success"]
    [row] = saved(account["id"])
    assert (row.rating, row.comment, row.can_publish, row.display_name) == \
        (4, "Very useful", True, "Sam, Leeds")
    assert row.level_at_review == 3
    assert CARD not in client.get("/progress").data


def test_publishing_is_off_unless_ticked(account):
    client_for(account).post("/api/review", json={"rating": 2})
    [row] = saved(account["id"])
    assert row.can_publish is False and row.comment is None


def test_sending_twice_updates_one_row(account):
    client = client_for(account)
    client.post("/api/review", json={"rating": 5})
    client.post("/api/review", json={"rating": 3})
    assert [r.rating for r in saved(account["id"])] == [3]


@pytest.mark.parametrize("rating", [0, 6, "x", None])
def test_bad_ratings_are_refused(account, rating):
    r = client_for(account).post("/api/review", json={"rating": rating})
    assert r.status_code == 400
    assert saved(account["id"]) == []


def test_overlong_comment_is_refused(account):
    r = client_for(account).post("/api/review", json={"rating": 5, "comment": "a" * 1001})
    assert r.status_code == 400


def test_signed_out_cannot_post():
    assert client_for().post("/api/review", json={"rating": 5}).status_code == 401


def test_form_posts_are_refused(account):
    # Only JSON is accepted: a form on another site can't send it unchecked.
    r = client_for(account).post("/api/review", data={"rating": "5"})
    assert r.status_code == 415


# --- the private list ---------------------------------------------------------

def test_private_list_is_hidden_from_learners(account):
    assert client_for(account, is_developer=False).get("/reviews/private").status_code == 404


def test_private_list_shows_every_review_to_the_developer(account):
    client_for(account).post("/api/review", json={"rating": 1, "comment": "Too hard"})
    page = client_for(is_developer=True).get("/reviews/private")
    assert page.status_code == 200
    assert b"Too hard" in page.data
