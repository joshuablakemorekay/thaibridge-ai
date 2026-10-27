"""Every vocabulary quiz is locked, unless it is left open on purpose.

Added 2026-10-27 after finding three paid quizzes open to everyone, logged out
included: /exercise/<topic> checks a section named after the topic, and two
topics had no section by that name (one was named differently, one never had
one). Nothing errored — the access check treats an unknown section as "no
restrictions" — so it went unnoticed. These tests make that impossible to
repeat silently.
"""

import os

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import (app, VOCABULARY, SECTION_REQUIREMENTS, OPEN_EXERCISE_TOPICS,  # noqa: E402
                 exercise_section)


def test_every_quiz_topic_has_a_lock_or_a_reason():
    for topic in VOCABULARY:
        if topic in OPEN_EXERCISE_TOPICS:
            continue
        assert exercise_section(topic) in SECTION_REQUIREMENTS, (
            f"/exercise/{topic} has no lock: add 'exercise_{topic}' to SECTION_REQUIREMENTS, "
            "or list it in OPEN_EXERCISE_TOPICS with the reason")


def test_open_topics_are_real_topics():
    assert set(OPEN_EXERCISE_TOPICS) <= set(VOCABULARY)


@pytest.mark.parametrize("topic", ["buddhist_formal", "everyday", "theravada_dhamma", "festivals"])
def test_a_logged_out_visitor_meets_the_lock(topic):
    html = app.test_client().get(f"/exercise/{topic}").get_data(as_text=True)
    assert "Section Locked" in html
