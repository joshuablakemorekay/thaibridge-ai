"""Server-issued questions: deal one, mark the answer, pay the XP.

Every drill that awards XP goes through here — the vocabulary and listening
quizzes, the tone drills, the Learning Path's starting check and the Sentences
tile builder — so the anti-cheating rule and the daily XP cap are written once.

Moved out of app.py so the quiz Blueprint and app.py can share it without
either importing the other.
"""

import hashlib
import hmac
import random
import uuid

from flask import current_app, session

from progress import init_user_progress
from rewards import DRILL_XP_DAILY_CAP, POINT_REWARDS, add_xp, drill_xp_today


# ── Server-issued drill questions ────────────────────────────────────────────
#
# A drill used to send the correct answer to the browser and then trust the
# browser to send it back: /api/check_answer received BOTH halves and compared
# them to each other. That is not a check, and it paid XP — which mattered more
# once levelling started earning a free paid section.
#
# So the server issues each question with an id and remembers what the answer
# was. It remembers it as an HMAC, not as text, because Flask's session cookie
# is SIGNED BUT NOT ENCRYPTED — it is base64, and anyone can read their own.
# Storing the answer there would just move the leak from the response body into
# the cookie. An HMAC needs the secret key to produce, so a browser can neither
# read the answer out of it nor forge one for an answer of its choosing.
#
# Redeeming consumes the id, so one question can be scored exactly once. A
# scripted loop can still send guesses; it just cannot send the same correct
# guess twice, and cannot know which guess is correct before sending it.
_PENDING_ANSWER_LIMIT = 30   # plenty for a drill session, and keeps the cookie small


def _answer_token(question_id, answer):
    """A value that proves what the answer was without revealing it."""
    return hmac.new(
        current_app.secret_key.encode() if isinstance(current_app.secret_key, str) else current_app.secret_key,
        f"{question_id}:{answer}".encode(),
        hashlib.sha256,
    ).hexdigest()


def issue_question(answer, suffix=''):
    """Register the answer to a question about to be sent out; return its id.

    `suffix` tags the id with the quiz topic (learning_path.question_suffix), so
    a marked answer can be counted against that topic for the Learning Path.
    """
    question_id = uuid.uuid4().hex + suffix
    pending = dict(session.get('pending_answers') or {})
    pending[question_id] = _answer_token(question_id, answer)
    # Oldest first out. Dicts keep insertion order, so this drops the questions
    # a learner has long since scrolled past rather than the one in front of them.
    while len(pending) > _PENDING_ANSWER_LIMIT:
        pending.pop(next(iter(pending)))
    session['pending_answers'] = pending
    session.modified = True
    return question_id


def redeem_question(question_id, answer, options=None):
    """Mark an answer against the question the server actually issued.

    Returns (scored, is_correct, correct_answer). `scored` is False when there
    is no matching outstanding question — an expired one, a replayed one, or a
    drill the server never issued. Those still get marked by the caller, but
    they must never pay XP: the server has no idea whether they are true.

    `correct_answer` is recovered by testing the options against the stored
    token, so the right answer can be shown after a guess without it ever having
    been stored in readable form.
    """
    pending = dict(session.get('pending_answers') or {})
    token = pending.pop(question_id, None)
    if token is None:
        return False, False, None

    session['pending_answers'] = pending
    session.modified = True

    is_correct = hmac.compare_digest(token, _answer_token(question_id, answer))

    correct_answer = answer if is_correct else None
    if not is_correct:
        for option in (options or []):
            if hmac.compare_digest(token, _answer_token(question_id, option)):
                correct_answer = option
                break
    return True, is_correct, correct_answer


def meaning_options(word, vocab_list):
    """The right English meaning plus up to three others, shuffled.

    Deduplicated on the English, because two words can share a meaning and a
    duplicate button would be "wrong" while saying the same thing.
    """
    wrong = list(dict.fromkeys(
        v['english'] for v in vocab_list if v['english'] != word['english']))
    options = random.sample(wrong, min(3, len(wrong))) + [word['english']]
    random.shuffle(options)
    return options


def pay_drill_answer(is_correct, scored):
    """Count one marked drill answer and pay its XP, under the daily cap.

    Shared by every drill that marks answers, so the cap and the counters
    can't drift apart between them. `scored` must be False for anything the
    server didn't issue itself: those are counted but never paid.
    """
    # Gamification: Award points for correct answers
    init_user_progress()
    user = session['user_progress']
    xp_earned = 0
    new_level = user['level']
    level_up = False
    capped = False
    
    if is_correct and scored:
        remaining = max(0, DRILL_XP_DAILY_CAP - drill_xp_today())
        if remaining > 0:
            result = add_xp(min(POINT_REWARDS['quiz_correct'], remaining),
                            'Correct answer')
            xp_earned = result.get('points_earned', 0)
            new_level = result.get('level')
            level_up = result.get('level_up', False)
            # Count what was actually paid, multiplier included, so a Pro
            # subscriber's 3x does not quietly buy three times the ceiling.
            user['drill_xp_today'] = user.get('drill_xp_today', 0) + xp_earned
        else:
            capped = True

    if is_correct:
        user['correct_answers'] = user.get('correct_answers', 0) + 1
        user['words_learned'] = user.get('words_learned', 0) + 1
    
    user['total_answers'] = user.get('total_answers', 0) + 1
    user['quizzes_completed'] = user.get('quizzes_completed', 0) + 1
    session.modified = True

    return {
        'xp_earned': xp_earned,
        'daily_cap_reached': capped,
        # False when the server did not issue this question, so the marking is
        # the browser's word and no XP was paid for it.
        'scored': scored,
        'new_level': new_level,
        # True when this answer crossed a level, so the page can celebrate it.
        'level_up': level_up,
        'total_xp': user['xp']
    }
