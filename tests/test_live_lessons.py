"""Live lessons: register your interest (live_lessons.py).

There are no live lessons yet; the box on /premium measures demand. These
tests pin what the box shows to whom, that registering twice still counts
once, that "take me off" really removes the row, and that the list stays
private.

Run with:  pytest tests/test_live_lessons.py -v
"""
import uuid

import pytest

from app import app
from models import LiveLessonInterest, User, db

BOX = 'id="live-lessons"'


@pytest.fixture
def account():
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"ll_{tag}", email=f"ll_{tag}@example.com", password_hash="x")
        db.session.add(u)
        db.session.commit()
        uid, version = u.id, u.session_version or 0
    yield {"id": uid, "login_id": f"{uid}:{version}"}
    with app.app_context():
        LiveLessonInterest.query.filter_by(user_id=uid).delete()
        User.query.filter_by(id=uid).delete()
        db.session.commit()


def client_for(account=None, developer=False):
    app.config["TESTING"] = True
    client = app.test_client()
    with client.session_transaction() as s:
        if account:
            s["_user_id"] = account["login_id"]
            s["_fresh"] = True
        if developer:
            s["user_progress"] = {"is_developer": True}
    return client


def saved(uid):
    with app.app_context():
        return LiveLessonInterest.query.filter_by(user_id=uid).all()


def register(client, **body):
    return client.post("/api/live-lessons/interest", json=body)


def test_a_signed_out_visitor_is_asked_to_sign_in():
    page = client_for().get("/premium").get_data(as_text=True)
    assert BOX in page
    assert 'id="live-lessons-form"' not in page
    assert "to register your interest" in page


def test_the_box_never_promises_lessons_that_do_not_exist():
    page = client_for().get("/premium").get_data(as_text=True)
    assert "We don't offer live lessons yet" in page
    assert "Nothing is" in page and "booked or charged" in page


def test_a_signed_in_learner_sees_the_form(account):
    page = client_for(account).get("/premium").get_data(as_text=True)
    assert 'id="live-lessons-form"' in page


def test_registering_saves_one_row_with_the_plan_at_the_time(account):
    client = client_for(account)
    r = register(client, lesson_format="group", price_band="15_25",
                 note="  evenings UK time ")
    assert r.get_json()["success"] is True
    [row] = saved(account["id"])
    assert row.lesson_format == "group"
    assert row.note == "evenings UK time"
    assert row.price_band == "15_25"
    assert row.tier_at_signup == "free"


def test_registering_twice_updates_rather_than_counting_twice(account):
    client = client_for(account)
    register(client, lesson_format="group")
    register(client, lesson_format="one_to_one")
    rows = saved(account["id"])
    assert [r.lesson_format for r in rows] == ["one_to_one"]


def test_once_registered_the_page_says_so(account):
    client = client_for(account)
    register(client, lesson_format="group")
    page = client.get("/premium").get_data(as_text=True)
    assert "on the list (small group)" in page
    assert 'id="live-lessons-withdraw"' in page
    assert 'id="live-lessons-form"' not in page


def test_the_price_question_is_optional(account):
    register(client_for(account), lesson_format="group")
    [row] = saved(account["id"])
    assert row.price_band is None


def test_take_me_off_the_list_deletes_the_row(account):
    client = client_for(account)
    register(client)
    r = client.post("/api/live-lessons/interest/withdraw", json={})
    assert r.get_json()["success"] is True
    assert saved(account["id"]) == []


@pytest.mark.parametrize("body, problem", [
    ({"lesson_format": "weekly-podcast"}, "lesson types"),
    ({"note": "x" * 501}, "500 characters"),
    ({"price_band": "free"}, "price options"),
])
def test_bad_input_is_refused(account, body, problem):
    r = register(client_for(account), **body)
    assert r.status_code == 400
    assert problem in r.get_json()["message"]
    assert saved(account["id"]) == []


def test_signed_out_and_form_posts_are_refused():
    client = client_for()
    assert register(client).status_code == 401
    assert client.post("/api/live-lessons/interest",
                       data={"lesson_format": "group"}).status_code == 415


def test_the_list_is_private(account):
    assert client_for(account).get("/live-lessons/private").status_code == 404


def test_the_developer_sees_the_list(account):
    register(client_for(account), lesson_format="group", price_band="25_35",
             note="temple Thai")
    page = client_for(developer=True).get("/live-lessons/private").get_data(as_text=True)
    assert "temple Thai" in page
    assert "ll_" in page
    assert "£25–35" in page
