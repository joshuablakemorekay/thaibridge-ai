"""The quiz and listening routes: a Flask Blueprint, registered in app.py.

  /exercise/<topic>         a vocabulary topic: word table, quizzes, Say it
  /api/quiz/<topic>         one reading or listening question (?listen=true)
  /api/listening/<conv_id>  the comprehension questions for a conversation
  /api/drill/<kind>         one tone or consonant-class drill question
  /api/check_answer         mark an answer and pay its XP (rate-limited)

Like auth.py it never imports app.py: content comes from the data modules,
access and plans from access.py and plans.py, and the deal-mark-pay machinery
from questions.py.
"""

import random

from flask import Blueprint, current_app, jsonify, render_template, request, session, url_for
from flask_login import current_user

import learning_path
import listening
import thai_audio
from access import EARNED_UNLOCK_LEVEL, SECTION_REQUIREMENTS, active_tier, check_section_access, earned_unlock_offer
from beginner_mode import get_vocab_with_mode
from extensions import limiter, rate_limit_key
from plans import PRONUNCIATION_LIVE, pronunciation_testers
from questions import issue_question, meaning_options, pay_drill_answer, redeem_question
from sentence_content import CONVERSATIONS
from tones import TONES_AND_CLASSES
from vocabulary import CULTURAL_STORIES, VOCABULARY

bp = Blueprint('quizzes', __name__)


# A quiz topic whose lock is named differently from the topic itself. Before
# this map, /exercise/buddhist_formal checked a section called
# 'exercise_buddhist_formal', which has no requirements — so a paid quiz was
# open to everyone, and nothing looked wrong. The key stays 'exercise_formal'
# because it may already be saved as a learner's earned-unlock choice.
EXERCISE_SECTION_NAMES = {'buddhist_formal': 'exercise_formal'}


# Quiz topics left open to everyone on purpose, each with the reason.
# tests/test_exercise_locks.py fails if any other topic has no lock.
# (Theravada Dhamma vocabulary was considered and locked, 2026-10-27: it is
# language tooling built on the teaching, which the policy says is paid; the
# Dhamma itself stays free on /theravada.)
OPEN_EXERCISE_TOPICS = {}


def can_use_pronunciation():
    """Whether to offer 🎤 Say it. A Thai Master (Pro) feature, and while it is
    hidden (see PRONUNCIATION_LIVE) only for the named testers. Developer mode
    always sees it. It runs entirely in the browser, so this only decides
    whether the button is offered."""
    if session.get('user_progress', {}).get('is_developer', False):
        return True
    if active_tier() != 'pro':
        return False
    if PRONUNCIATION_LIVE:
        return True
    return (current_user.is_authenticated
            and current_user.username.lower() in pronunciation_testers())


def exercise_section(category):
    """The SECTION_REQUIREMENTS key that locks /exercise/<category>."""
    return EXERCISE_SECTION_NAMES.get(category, f'exercise_{category}')


@bp.route('/exercise/<category>')
def exercise(category):
    # Check category-specific access
    section = exercise_section(category)
    has_access, message = check_section_access(section)
    if not has_access:
        return render_template('locked.html',
                             section=section,
                             message=message,
                             requirements=SECTION_REQUIREMENTS.get(section, {}),
                             earned_unlock_offered=earned_unlock_offer(section),
                             earned_unlock_level=EARNED_UNLOCK_LEVEL,
                             user_progress=session['user_progress'])
    
    beginner_mode = request.args.get('beginner', 'false').lower() == 'true'
    
    if category not in VOCABULARY:
        return f"Category '{category}' not found. <a href='/learn'>Back to Learn</a>", 404
    
    vocab_list = get_vocab_with_mode(VOCABULARY[category], beginner_mode)
    story = CULTURAL_STORIES.get(category)
    
    session['current_vocab'] = vocab_list
    session['current_category'] = category
    session['beginner_mode'] = beginner_mode

    # thai -> MP3 URL for every word in this category (only ones with a clip).
    # Covers both the vocab table and the JS quiz, which draw the same words.
    # Keyed on the raw VOCABULARY word, whose 'thai' is unchanged by beginner
    # mode (that only rewrites the romanisation), so the keys stay stable.
    audio_map = {
        w['thai']: url_for('static', filename=thai_audio.audio_static_path(w['thai']))
        for w in VOCABULARY[category]
        if thai_audio.audio_exists(current_app.static_folder, w['thai'])
    }

    return render_template('exercise.html', category=category, vocab=vocab_list,
                         story=story, beginner_mode=beginner_mode,
                         audio_map=audio_map,
                         listening_ready=len(audio_map) >= LISTENING_MIN_WORDS,
                         can_pronounce=can_use_pronunciation(),
                         pronunciation_live=PRONUNCIATION_LIVE,
                         pron_words=[{'thai': w['thai'], 'paiboon': w['paiboon'],
                                      'english': w['english'], 'audio': audio_map[w['thai']]}
                                     for w in vocab_list if w['thai'] in audio_map])


@bp.route('/api/quiz/<category>')
def get_quiz(category):
    beginner_mode = request.args.get('beginner', 'false').lower() == 'true'
    
    if category not in VOCABULARY:
        return jsonify({'error': f'Invalid category: {category}'}), 400
    
    vocab_list = get_vocab_with_mode(VOCABULARY[category], beginner_mode)

    if request.args.get('listen', 'false').lower() == 'true':
        return _listening_question(vocab_list, category)

    word = random.choice(vocab_list)

    wrong = [v['paiboon'] for v in vocab_list if v['paiboon'] != word['paiboon']]
    wrong = random.sample(wrong, min(3, len(wrong)))
    options = wrong + [word['paiboon']]
    random.shuffle(options)
    
    return jsonify({
        'thai': word['thai'],
        'english': word['english'],
        # No 'correct_answer' — that is the whole point. The browser gets an id
        # and the server keeps what it means.
        'question_id': issue_question(word['paiboon'],
                                      learning_path.question_suffix(category)),
        'options': options,
        'beginner_mode': beginner_mode
    })


# A listening question needs this many words with a recording behind it, or the
# "pick the meaning" choice is too small to be a test. The exercise page reads
# the same number to decide whether to offer the Listen button at all.
LISTENING_MIN_WORDS = 4


def listening_words(vocab_list):
    """The words in a category that have a recorded clip, so can be heard."""
    return [w for w in vocab_list
            if thai_audio.audio_exists(current_app.static_folder, w['thai'])]


def _listening_question(vocab_list, category):
    """Hear a word, pick its English meaning.

    The Thai is not shown on the page until the learner has answered — that is
    the whole exercise — but it still travels in the JSON so the result card can
    show it afterwards. The marking stays server-side, same as the reading quiz.
    """
    heard = listening_words(vocab_list)
    if len(heard) < LISTENING_MIN_WORDS:
        return jsonify({'error': 'Not enough recorded words here to listen to yet.'}), 404

    word = random.choice(heard)
    return jsonify({
        'thai': word['thai'],
        'paiboon': word['paiboon'],
        'audio': url_for('static', filename=thai_audio.audio_static_path(word['thai'])),
        'question_id': issue_question(
            word['english'], learning_path.question_suffix(category, listening=True)),
        'options': meaning_options(word, vocab_list),
    })


@bp.route('/api/listening/<conv_id>')
def get_listening_questions(conv_id):
    """The comprehension questions for one Sentences-page conversation.

    Gated like the page they belong to, since the questions give away what the
    dialogue says. Each answer is kept server-side behind a question id and
    marked by /api/check_answer, so it pays drill XP under the same daily cap.
    """
    if not check_section_access('sentences')[0]:
        return jsonify({'error': 'This conversation is locked.'}), 403
    questions = listening.QUESTIONS.get(conv_id)
    if conv_id not in CONVERSATIONS or not questions:
        return jsonify({'error': f'No listening questions for {conv_id}.'}), 404

    dealt = []
    for q in questions:
        options = q['wrong'] + [q['answer']]
        random.shuffle(options)
        dealt.append({'question': q['question'], 'options': options,
                      'question_id': issue_question(q['answer'])})
    return jsonify({'questions': dealt})


TONE_OPTIONS = ['Mid', 'Low', 'Falling', 'High', 'Rising']


@bp.route('/api/drill/<kind>')
def get_drill_question(kind):
    """Issue one tones/consonant-classes drill question.

    These four drills used to be dealt entirely in the browser: the pool was
    rendered into the page and the widget marked itself, then told
    /api/check_answer what the answer had been. Same flaw as the vocabulary
    quiz, so the same fix — the server picks the question and keeps the answer.
    """
    drills = TONES_AND_CLASSES['drills']

    if kind == 'classid':
        pool = [
            {'thai': consonant['thai'], 'sub': consonant['name'], 'answer': group['label']}
            for group in TONES_AND_CLASSES['classes']
            for consonant in group['consonants']
            if not consonant.get('obsolete')
        ]
        options = ['MID', 'HIGH', 'LOW']
    elif kind == 'tone_calc':
        level = request.args.get('level', type=int) or 0
        source = drills['tone_calc']
        # level 0 is the mixed set; anything else filters to that stage.
        if level:
            source = [q for q in source if q['level'] == level]
        pool = [{'thai': q['thai'], 'sub': f"{q['class']} class", 'answer': q['tone']}
                for q in source]
        options = TONE_OPTIONS
    elif kind in ('contrast', 'leading_h'):
        pool = [{'thai': q['thai'], 'sub': q['english'], 'answer': q['tone']}
                for q in drills[kind]]
        options = TONE_OPTIONS
    else:
        return jsonify({'error': f'Unknown drill: {kind}'}), 404

    if not pool:
        return jsonify({'error': 'No questions here yet.'}), 404

    question = random.choice(pool)
    return jsonify({
        'question_id': issue_question(question['answer']),
        'thai': question['thai'],
        'sub': question['sub'],
        'options': options,
    })


@bp.route('/api/check_answer', methods=['POST'])
@limiter.limit("120 per hour; 600 per day", key_func=rate_limit_key)
def check_answer():
    """Score one drill answer and pay the XP for it.

    This endpoint cannot verify anything. The drills are built in the browser,
    so the page already holds the answer and the request carries BOTH halves of
    the comparison — a script can send a matching pair as easily as a learner
    can answer correctly. That is not fixable without rebuilding the drills
    server-side, so the reward is bounded instead: DRILL_XP_DAILY_CAP a day,
    plus the rate limit above. Marking still works past the cap; only the XP
    stops, because a learner who wants to keep drilling should be able to.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    # A question the server issued can be marked properly. Anything else is
    # marked on the browser's say-so and must not pay: client-built drills, a
    # question already scored, or one that aged out of the pending list.
    question_id = data.get('question_id')
    scored, is_correct, correct_answer = redeem_question(
        question_id, data.get('answer'), data.get('options')
    ) if question_id else (False, False, None)

    if not scored:
        is_correct = data.get('answer') == data.get('correct')
        correct_answer = data.get('correct')

    payment = pay_drill_answer(is_correct, scored)

    # Only a server-issued question counts toward a topic's score: the Learning
    # Path sets its targets from these, so they must be as honest as the XP.
    topic, by_ear = learning_path.topic_from_question(question_id)
    if scored and topic:
        learning_path.record_answer(session['user_progress'], topic, is_correct, by_ear)
        session.modified = True

    return jsonify({
        'correct': is_correct,
        'message': 'ถูกต้อง! (Correct!)' if is_correct else f"ไม่ถูกต้อง. Answer: {correct_answer or ''}",
        'correct_answer': correct_answer,
        **payment,
    })
