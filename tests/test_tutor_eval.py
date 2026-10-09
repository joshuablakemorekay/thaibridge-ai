"""The tutor's accuracy exam must itself be trustworthy.

scripts/tutor_eval.py asks the real tutor every question in
evals/tutor_accuracy.yaml and checks the answers. A broken check is worse than
none: one that can never fail reports a mistake as fixed. These tests run the
checks against answers we already know are right or wrong, offline and free.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                'scripts'))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import tutor_eval  # noqa: E402
import ai_agent  # noqa: E402

CASES = tutor_eval.load_cases()
MODES = {'conversation', 'tutor', 'generator', 'cultural', 'buddhist', 'helper'}


def by_id(case_id):
    return next(c for c in CASES if c['id'] == case_id)


# ── The exam file ─────────────────────────────────────────────────────────

def test_case_ids_are_unique():
    ids = [c['id'] for c in CASES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("case", CASES, ids=lambda c: c['id'])
def test_every_case_is_well_formed(case):
    assert case['mode'] in MODES
    assert case['question'].strip()
    assert case.get('why', '').strip(), "every case records why it exists"
    if case['mode'] == 'buddhist':
        assert case.get('lens') in ai_agent.DHAMMA_LENSES
    assert case.get('must_include') or case.get('must_not_include') \
        or case.get('no_thai_script'), "a case with no checks passes anything"


def test_reply_limits_match_the_app():
    """The script copies these to avoid importing app (which hits the live DB)."""
    import app as appmod
    assert tutor_eval.REPLY_TOKENS == appmod.AI_REPLY_TOKENS
    assert tutor_eval.REPLY_TOKENS_BY_MODE == appmod.AI_REPLY_TOKENS_BY_MODE


# ── The checks catch the mistakes they were written for ───────────────────

def test_a_correct_answer_passes():
    answer = ("The three grounds of merit are dāna (generosity), sīla (ethical "
              "conduct) and bhāvanā (meditation).")
    assert tutor_eval.check(by_id('merit-grounds'), answer, 'end_turn') == []


def test_any_of_accepts_each_spelling():
    for word in ('dana', 'generosity'):
        answer = f"{word}, sila and bhavana"
        assert tutor_eval.check(by_id('merit-grounds'), answer, 'end_turn') == []


def test_the_real_haiku_mistake_fails():
    answer = "The three roots of merit are dāna, sīla and bhāvanā."
    assert 'contains: three roots' in tutor_eval.check(by_id('merit-grounds'), answer, 'end_turn')


def test_counting_people_with_tua_fails():
    answer = "คนหนึ่งตัว (kon nʉ̀ŋ dtua) = one person"
    failures = tutor_eval.check(by_id('classifier-tua'), answer, 'end_turn')
    assert 'contains: คนหนึ่งตัว' in failures


def test_thai_in_a_universal_answer_fails():
    answer = "Merit (บุญ) comes from dāna, sīla and bhāvanā."
    assert 'contains Thai script' in tutor_eval.check(by_id('merit-grounds'), answer, 'end_turn')


def test_a_cut_off_answer_fails():
    answer = "dāna, sīla and bhāvanā are"
    assert 'cut off mid-sentence' in tutor_eval.check(by_id('merit-grounds'), answer, 'max_tokens')


@pytest.mark.parametrize("bad, good", [
    ("คุณ (khun)", "คุณ (kun)"),
    ("พระ (phrá)", "พระ (prá)"),
    ("ที่ (thîi)", "ที่ (tîi)"),
    ("ผู้หญิง (pûu-yǐng)", "ผู้หญิง (pûu-yǐŋ)"),
    ("ชื่อ (chûe)", "ชื่อ (chʉ̂ʉ)"),
])
def test_spelling_rule_breaks_are_caught(bad, good):
    assert tutor_eval.spelling_breaks(bad)
    assert tutor_eval.spelling_breaks(good) == []


@pytest.mark.parametrize("gloss", ["หิว (hungry)", "ฟ้า (blue)", "เช้า (morning)"])
def test_an_english_meaning_in_brackets_is_not_a_broken_spelling(gloss):
    """Sonnet wrote หิว (hungry); the first cut of this check failed it for 'ng'."""
    assert tutor_eval.spelling_breaks(gloss) == []


def test_english_glosses_in_brackets_are_not_romanisations():
    """A bracket of English after Thai is a gloss; 'this' must not count as 'th'."""
    assert tutor_eval.spelling_breaks("นี้ (this one, near the speaker)") == []
