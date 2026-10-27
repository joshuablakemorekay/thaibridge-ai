"""Tests for Listen & answer on the Sentences page conversations (added 2026-10-27).

Each conversation can be played with its words hidden, then answered: the
questions come from listening.py, are dealt and marked by the server, and are
locked with the Sentences page itself (they give away what the dialogue says).
Split out of test_listening_quiz.py, which covers the single-word quiz.
"""

import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as app_module  # noqa: E402
import listening  # noqa: E402


@pytest.fixture
def client():
    return app_module.app.test_client()


@pytest.fixture
def open_sentences(monkeypatch):
    monkeypatch.setattr(app_module, "check_section_access", lambda section: (True, ""))


def test_every_conversation_has_listening_questions():
    """A new conversation needs questions here, or it gets no Listen mode."""
    assert set(listening.QUESTIONS) == set(app_module.CONVERSATIONS)


def test_question_sets_are_well_formed():
    for conv_id, questions in listening.QUESTIONS.items():
        assert len(questions) >= 3, conv_id
        for q in questions:
            options = q["wrong"] + [q["answer"]]
            assert len(q["wrong"]) == 3, (conv_id, q["question"])
            assert len(set(options)) == 4, f"duplicate option in {conv_id}: {q['question']}"


def test_listening_questions_are_locked_with_the_page(client, monkeypatch):
    monkeypatch.setattr(app_module, "check_section_access", lambda section: (False, "Locked"))
    assert client.get("/api/listening/restaurant").status_code == 403


def test_unknown_conversation_is_refused(client, open_sentences):
    assert client.get("/api/listening/no_such_chat").status_code == 404


def test_listening_answers_are_marked_by_the_server(client, open_sentences):
    dealt = client.get("/api/listening/taxi").get_json()["questions"]
    assert "answer" not in dealt[0]
    fare = next(q for q in dealt if "fare" in q["question"])
    result = client.post("/api/check_answer", json={
        "question_id": fare["question_id"], "answer": "90 baht",
        "options": fare["options"]}).get_json()
    assert result["correct"] and result["scored"]


def test_sentences_page_plays_each_conversation_as_one_sequence(client, open_sentences):
    html = client.get("/sentences").get_data(as_text=True)
    assert html.count('onclick="toggleConvListening(') == len(app_module.CONVERSATIONS)
    restaurant_lines = len(app_module.CONVERSATIONS["restaurant"]["dialogue"])
    sequences = [chunk.split('"', 1)[0] for chunk in html.split('data-audio-sequence="')[1:]]
    assert len(sequences[0].split()) == restaurant_lines
