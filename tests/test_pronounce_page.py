"""Who sees 🎤 Say it (Pronunciation Analysis), and where it is advertised.

It is a Thai Master (Pro) feature, and HIDDEN until a native speaker has tested
it: only developer mode and the usernames in PRONUNCIATION_TESTERS see it,
until PRONUNCIATION_LIVE turns it on for every Pro learner. While hidden, it is
not advertised anywhere — no Premium card, no Pro feature line, no "this is
part of Pro" note — because it is not on sale yet.
"""

import os
from types import SimpleNamespace

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import app as app_module  # noqa: E402
import quizzes  # noqa: E402  (the /exercise route and its Pro check live here)

SAY_IT = 'id="pronounceStart"'
SCRIPT = "/static/js/pronounce.js?v="
PRO_NOTE = 'part of <a href="/premium">Thai Master (Pro)</a>'


def exercise_page(monkeypatch, tier, live=False, username=None, testers=""):
    monkeypatch.setattr(quizzes, "check_section_access", lambda section: (True, ""))
    monkeypatch.setattr(quizzes, "active_tier", lambda: tier)
    monkeypatch.setattr(quizzes, "PRONUNCIATION_LIVE", live)
    monkeypatch.setenv("PRONUNCIATION_TESTERS", testers)
    monkeypatch.setattr(quizzes, "current_user", SimpleNamespace(
        is_authenticated=username is not None, username=username or ""))
    return app_module.app.test_client().get("/exercise/festivals").get_data(as_text=True)


def test_hidden_from_pro_learners_until_reviewed(monkeypatch):
    html = exercise_page(monkeypatch, "pro")
    assert SAY_IT not in html and SCRIPT not in html


def test_a_named_tester_on_pro_sees_it(monkeypatch):
    html = exercise_page(monkeypatch, "pro", username="KruNid", testers="someone, krunid")
    assert SAY_IT in html and SCRIPT in html
    assert "const PRON_WORDS = [" in html


def test_a_tester_needs_pro_too(monkeypatch):
    html = exercise_page(monkeypatch, "basic", username="krunid", testers="krunid")
    assert SAY_IT not in html


def test_live_means_every_pro_learner(monkeypatch):
    assert SAY_IT in exercise_page(monkeypatch, "pro", live=True)


@pytest.mark.parametrize("tier", ["free", "basic"])
def test_other_plans_are_told_it_is_pro_once_live(monkeypatch, tier):
    html = exercise_page(monkeypatch, tier, live=True)
    assert SAY_IT not in html and SCRIPT not in html
    assert PRO_NOTE in html


def test_not_advertised_while_hidden(monkeypatch):
    assert PRO_NOTE not in exercise_page(monkeypatch, "free")
    monkeypatch.setattr(app_module, "PRONUNCIATION_LIVE", False)
    premium = app_module.app.test_client().get("/premium").get_data(as_text=True)
    assert "Pronunciation Analysis" not in premium


def test_premium_card_appears_once_live(monkeypatch):
    monkeypatch.setattr(app_module, "PRONUNCIATION_LIVE", True)
    premium = app_module.app.test_client().get("/premium").get_data(as_text=True)
    assert "🎤 Pronunciation Analysis" in premium


def test_privacy_page_explains_the_microphone():
    html = app_module.app.test_client().get("/privacy").get_data(as_text=True)
    assert 'id="microphone"' in html
    assert "never receives or stores your voice" in html
