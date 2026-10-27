"""Tests for the Listening Quiz on the vocabulary exercise pages (added 2026-10-27).

/api/quiz/<category>?listen=true deals a "hear it, pick the meaning" question:
the learner gets a clip and four English meanings, and the server keeps the
answer, exactly like the reading quiz. These tests pin the parts that would
fail quietly — a clip that 404s, a duplicate meaning, an answer leaked early.
"""

import os
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, VOCABULARY, POINT_REWARDS  # noqa: E402
from quizzes import LISTENING_MIN_WORDS, listening_words  # noqa: E402

CATEGORY = "festivals"


@pytest.fixture
def client():
    return app.test_client()


def listen(client, category=CATEGORY):
    return client.get(f"/api/quiz/{category}?listen=true")


def meaning_of(thai, category=CATEGORY):
    return next(w["english"] for w in VOCABULARY[category] if w["thai"] == thai)


def test_question_points_at_a_clip_that_exists(client):
    question = listen(client).get_json()
    clip = client.get(question["audio"])
    assert clip.status_code == 200, f"{question['audio']} is not a real file"


def test_options_hold_the_meaning_once_and_never_repeat(client):
    for _ in range(20):
        question = listen(client).get_json()
        options = question["options"]
        assert len(options) == len(set(options)), f"duplicate meaning in {options}"
        assert options.count(meaning_of(question["thai"])) == 1


def test_the_answer_is_not_sent_with_the_question(client):
    question = listen(client).get_json()
    assert "english" not in question
    assert "correct_answer" not in question


def test_right_meaning_is_marked_correct_and_paid(client):
    question = listen(client).get_json()
    result = client.post("/api/check_answer", json={
        "question_id": question["question_id"],
        "answer": meaning_of(question["thai"]),
        "options": question["options"],
    }).get_json()
    assert result["correct"] and result["scored"]
    assert result["xp_earned"] == POINT_REWARDS["quiz_correct"]


def test_wrong_meaning_is_shown_the_right_one(client):
    question = listen(client).get_json()
    right = meaning_of(question["thai"])
    wrong = next(o for o in question["options"] if o != right)
    result = client.post("/api/check_answer", json={
        "question_id": question["question_id"],
        "answer": wrong,
        "options": question["options"],
    }).get_json()
    assert not result["correct"]
    assert result["correct_answer"] == right


def test_every_topic_with_enough_clips_offers_listening():
    """If this fails after adding a topic, record its audio before shipping it."""
    # listening_words() finds the clips through Flask's current_app, which a
    # request normally provides; outside one, the app context stands in.
    with app.app_context():
        for category, words in VOCABULARY.items():
            assert len(listening_words(words)) >= LISTENING_MIN_WORDS, (
                f"'{category}' has too few recorded words for the Listening Quiz")


def test_unknown_topic_is_refused(client):
    assert listen(client, "no_such_topic").status_code == 400
