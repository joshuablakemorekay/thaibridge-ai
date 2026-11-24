"""Paid content must not leak through a side door (added 2026-11-24).

Every paid page carried its lock, but a few addresses next to them did not:
each single lesson (/lesson/<id>) opened in full while the Lessons list was
locked, three unused data feeds handed out the whole paid vocabulary, grammar
guide and lessons, and the quiz and drill feeds dealt paid questions (and paid
XP) without asking. These tests come at each one as a brand-new free visitor.
"""
import pytest

from app import app, LESSONS

FREE_VISITOR = dict(subscription_tier="free", is_developer=False, full_unlock=False,
                    level=1, xp=0)


@pytest.fixture
def free_client(make_client):
    return make_client(**FREE_VISITOR)


@pytest.mark.parametrize("lesson_id", [l["id"] for l in LESSONS])
def test_every_single_lesson_is_locked_for_a_free_visitor(free_client, lesson_id):
    page = free_client.get(f"/lesson/{lesson_id}").get_data(as_text=True)
    lesson = next(l for l in LESSONS if l["id"] == lesson_id)
    taught = [s["thai"] for kind in ("short", "long") for s in lesson["sentences"][kind]]
    assert taught, "the lesson should teach something, or this test checks nothing"
    for thai in taught:
        assert thai not in page


def test_a_subscriber_can_still_read_a_lesson(unlocked_client):
    lesson = LESSONS[0]
    page = unlocked_client.get(f"/lesson/{lesson['id']}").get_data(as_text=True)
    assert lesson["sentences"]["short"][0]["thai"] in page


@pytest.mark.parametrize("address", ["/api/lessons", "/api/grammar",
                                     "/api/vocabulary/festivals"])
def test_the_old_data_feeds_are_gone(free_client, address):
    assert free_client.get(address).status_code == 404


@pytest.mark.parametrize("address", ["/api/quiz/festivals",
                                     "/api/quiz/festivals?listen=true",
                                     "/api/drill/classid"])
def test_paid_quiz_and_drill_feeds_are_locked(free_client, address):
    response = free_client.get(address)
    assert response.status_code == 403
    assert "question_id" not in (response.get_json() or {})


@pytest.mark.parametrize("address", ["/api/quiz/festivals", "/api/drill/classid"])
def test_paid_quiz_and_drill_feeds_still_work_for_subscribers(unlocked_client, address):
    assert "question_id" in unlocked_client.get(address).get_json()
