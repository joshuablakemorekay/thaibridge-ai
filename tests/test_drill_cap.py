"""Tests for the daily ceiling on drill XP (added 2026-08-18).

/api/check_answer is sent both the answer and the correct answer, and compares
them to each other — the drills are generated in the browser, so the page holds
the answer already. It therefore cannot tell a learner from a script, and no
amount of validation fixes that while the drills stay client-side.

So the reward is bounded rather than the honesty proved. These tests pin the
bound, which matters more than it used to: XP now earns a free paid section, so
farming it is farming access, not just a number.
"""

import os
import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, DRILL_XP_DAILY_CAP, POINT_REWARDS, VOCABULARY  # noqa: E402

CATEGORY = "festivals"


@pytest.fixture
def client():
    return app.test_client()


def answer(client, correctly=True):
    """Take one real drill question and answer it.

    Goes through /api/quiz so the question is server-issued — the endpoint no
    longer pays XP for anything else. The expected answer is looked up in the
    source data rather than read from the response, because the response
    deliberately no longer contains it.
    """
    question = client.get(f"/api/quiz/{CATEGORY}").get_json()
    expected = next(word["paiboon"] for word in VOCABULARY[CATEGORY]
                    if word["thai"] == question["thai"])
    given = expected if correctly else next(
        option for option in question["options"] if option != expected)

    return client.post("/api/check_answer", json={
        "question_id": question["question_id"],
        "answer": given,
        "options": question["options"],
    }).get_json()


def xp(client):
    return client.get("/api/user_stats").get_json()["xp"]


def test_xp_is_paid_below_the_cap(client):
    result = answer(client)
    assert result["xp_earned"] == POINT_REWARDS["quiz_correct"]
    assert not result["daily_cap_reached"]


def test_xp_stops_exactly_at_the_cap(client):
    per_answer = POINT_REWARDS["quiz_correct"]
    for _ in range(DRILL_XP_DAILY_CAP // per_answer):
        answer(client)

    assert xp(client) == DRILL_XP_DAILY_CAP

    beyond = answer(client)
    assert beyond["xp_earned"] == 0
    assert beyond["daily_cap_reached"]
    assert xp(client) == DRILL_XP_DAILY_CAP, "the cap leaked"


def test_a_capped_learner_can_still_practise(client):
    """The cap is on the reward, not the drill. Someone revising the night
    before an exam must not be locked out of their own practice."""
    for _ in range(DRILL_XP_DAILY_CAP // POINT_REWARDS["quiz_correct"] + 3):
        answer(client)

    result = answer(client)
    assert result["correct"] is True, "marking stopped working past the cap"
    assert result["xp_earned"] == 0


def test_a_wrong_answer_never_pays(client):
    before = xp(client)
    result = answer(client, correctly=False)
    assert result["xp_earned"] == 0
    assert xp(client) == before


def test_the_allowance_comes_back_the_next_day(client):
    for _ in range(DRILL_XP_DAILY_CAP // POINT_REWARDS["quiz_correct"] + 1):
        answer(client)
    assert xp(client) == DRILL_XP_DAILY_CAP

    with client.session_transaction() as session_data:
        progress = session_data["user_progress"]
        progress["drill_xp_date"] = "2020-01-01"      # yesterday, as far as it knows
        session_data["user_progress"] = progress

    result = answer(client)
    assert result["xp_earned"] == POINT_REWARDS["quiz_correct"]


def test_the_cap_counts_xp_paid_not_answers_given(client):
    """A points multiplier must not buy a bigger ceiling: a Pro subscriber's 3x
    would otherwise be three times the daily XP, not three times per answer."""
    client.get("/api/user_stats")          # let the app lay down a full progress dict
    with client.session_transaction() as session_data:
        progress = session_data["user_progress"]
        progress["subscription_tier"] = "pro"
        session_data["user_progress"] = progress

    for _ in range(DRILL_XP_DAILY_CAP):        # far more than enough
        result = answer(client)
        if result["daily_cap_reached"]:
            break

    assert xp(client) <= DRILL_XP_DAILY_CAP + POINT_REWARDS["quiz_correct"] * 3


# ---------------------------------------------------------------------------
# The answer never leaves the server
# ---------------------------------------------------------------------------

def test_the_quiz_does_not_tell_the_browser_the_answer(client):
    """The original bug: /api/quiz sent correct_answer, and check_answer then
    trusted the browser to send it back."""
    question = client.get(f"/api/quiz/{CATEGORY}").get_json()
    assert "correct_answer" not in question
    assert "question_id" in question


def test_the_answer_is_not_readable_in_the_session_cookie(client):
    """Flask signs the session cookie but does not encrypt it — anyone can
    base64-decode their own. So the answer is stored as an HMAC, never as text."""
    question = client.get(f"/api/quiz/{CATEGORY}").get_json()
    expected = next(word["paiboon"] for word in VOCABULARY[CATEGORY]
                    if word["thai"] == question["thai"])

    with client.session_transaction() as session_data:
        pending = session_data["pending_answers"]
    assert expected not in str(pending), "the answer is sitting in the cookie"


def test_an_unissued_question_is_marked_but_never_paid(client):
    """The old shape still works so client-built drills keep marking — it just
    cannot pay, because the server has no idea whether it is true."""
    result = client.post("/api/check_answer", json={
        "answer": "a", "correct": "a",
    }).get_json()

    assert result["correct"] is True
    assert result["scored"] is False
    assert result["xp_earned"] == 0


def test_a_question_can_only_be_scored_once(client):
    """Otherwise one correct answer is a replayable XP tap."""
    question = client.get(f"/api/quiz/{CATEGORY}").get_json()
    expected = next(word["paiboon"] for word in VOCABULARY[CATEGORY]
                    if word["thai"] == question["thai"])
    payload = {"question_id": question["question_id"], "answer": expected,
               "options": question["options"]}

    first = client.post("/api/check_answer", json=payload).get_json()
    second = client.post("/api/check_answer", json=payload).get_json()

    assert first["xp_earned"] == POINT_REWARDS["quiz_correct"]
    assert second["scored"] is False, "the same question scored twice"
    assert second["xp_earned"] == 0


def test_a_wrong_answer_is_told_what_the_right_one_was(client):
    """Recovered by testing the options against the stored token, so the answer
    can be shown after a guess without ever having been stored readably."""
    question = client.get(f"/api/quiz/{CATEGORY}").get_json()
    expected = next(word["paiboon"] for word in VOCABULARY[CATEGORY]
                    if word["thai"] == question["thai"])
    wrong = next(o for o in question["options"] if o != expected)

    result = client.post("/api/check_answer", json={
        "question_id": question["question_id"], "answer": wrong,
        "options": question["options"],
    }).get_json()

    assert result["correct"] is False
    assert result["correct_answer"] == expected


# ---------------------------------------------------------------------------
# The tones drills — same fix, four more drills
# ---------------------------------------------------------------------------

DRILLS = ["classid", "tone_calc", "contrast", "leading_h"]


@pytest.mark.parametrize("kind", DRILLS)
def test_every_tones_drill_issues_a_question_without_its_answer(client, kind):
    question = client.get(f"/api/drill/{kind}").get_json()
    assert "question_id" in question
    assert question["thai"] and question["options"]
    assert "answer" not in question
    assert "tone" not in question


@pytest.mark.parametrize("kind", DRILLS)
def test_every_tones_drill_can_be_marked_and_paid(client, kind):
    """Brute-forcing the options here is the test doing what a learner does —
    one of them is right, and only the server knows which."""
    paid = 0
    for _ in range(8):
        question = client.get(f"/api/drill/{kind}").get_json()
        for option in question["options"]:
            result = client.post("/api/check_answer", json={
                "question_id": question["question_id"],
                "answer": option,
                "options": question["options"],
            }).get_json()
            if result["correct"]:
                paid = result["xp_earned"]
                break
            # A consumed question cannot be retried, so draw a fresh one.
            question = client.get(f"/api/drill/{kind}").get_json()
        if paid:
            break
    assert paid == POINT_REWARDS["quiz_correct"]


def test_an_unknown_drill_is_a_404(client):
    assert client.get("/api/drill/not_a_drill").status_code == 404


def test_the_tone_level_filter_still_narrows_the_pool(client):
    """Level 1 is the mid-class stage. If the filter broke, a beginner would be
    shown high- and low-class syllables they have not been taught yet."""
    seen = set()
    for _ in range(25):
        seen.add(client.get("/api/drill/tone_calc?level=1").get_json()["sub"])
    assert seen == {"MID class"}, f"level 1 leaked other classes: {seen}"
