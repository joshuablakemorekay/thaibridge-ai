"""Tests for the Personalized Learning Path (IEP) on the Progress page (added 2026-10-27).

Two halves. The rules in learning_path.py are driven with plain dicts, so each
rule — ordering, targets, "met", the review — is pinned on its own. Then the
routes are walked end to end with the test client: set goals, take the starting
check, answer quizzes, review the week.
"""

import os
from datetime import date, timedelta

import pytest

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, VOCABULARY, _outline_sections  # noqa: E402
import learning_path as lp  # noqa: E402

TODAY = date(2026, 10, 27)

SECTIONS = [
    {'id': 'alphabet', 'title': 'Thai Alphabet', 'url': '/alphabet', 'level': 1},
    {'id': 'survival', 'title': 'Survival Thai', 'url': '/survival', 'level': 1},
    {'id': 'theravada', 'title': 'Theravada Dharma', 'url': '/theravada', 'level': 1},
    {'id': 'read_write', 'title': 'Read & Write', 'url': '/read_write', 'level': 2},
    {'id': 'exercise_festivals', 'title': 'Festival Vocabulary',
     'url': '/exercise/festivals', 'level': 2},
]


def open_all(section_id):
    return True, 'No restrictions'


def progress(**extra):
    return {'xp': 0, 'sections_visited': [], **extra}


def active_plan(goal='travel', practice='reading', minutes=20, prog=None):
    prog = prog if prog is not None else progress()
    plan = lp.new_plan(goal, practice, minutes)
    path = lp.build_path(plan, prog, SECTIONS, open_all)
    lp.start_week(plan, prog, path, lambda t: True, TODAY)
    return plan, prog


# ---- The rules --------------------------------------------------------------

def test_bad_choices_make_no_plan():
    assert lp.new_plan('fame', 'reading', 20) is None
    assert lp.new_plan('travel', 'osmosis', 20) is None
    assert lp.new_plan('travel', 'reading', 5) is None


def test_goal_puts_its_own_sections_first():
    temple = lp.build_path(lp.new_plan('temple', 'listening', 10), progress(), SECTIONS, open_all)
    travel = lp.build_path(lp.new_plan('travel', 'listening', 10), progress(), SECTIONS, open_all)
    assert [s['id'] for s in temple][:2] == ['alphabet', 'theravada']
    assert travel[0]['id'] == 'survival'


def test_every_section_stays_on_the_path():
    path = lp.build_path(lp.new_plan('temple', 'listening', 10), progress(), SECTIONS, open_all)
    assert sorted(s['id'] for s in path) == sorted(s['id'] for s in SECTIONS)


def test_reading_practice_brings_the_script_forward():
    path = lp.build_path(lp.new_plan('travel', 'reading', 10), progress(), SECTIONS, open_all)
    ids = [s['id'] for s in path]
    assert ids.index('read_write') == ids.index('alphabet') + 1


def test_states_done_next_locked():
    def can_open(section_id):
        return (section_id != 'read_write', 'Requires Level 2')
    path = lp.build_path(lp.new_plan('travel', 'speaking', 10),
                         progress(sections_visited=['survival']), SECTIONS, can_open)
    state = {s['id']: s for s in path}
    assert state['survival']['state'] == 'done'
    assert state['alphabet']['state'] == 'next'
    assert state['read_write']['state'] == 'locked'
    assert state['read_write']['why_locked'] == 'Requires Level 2'
    assert [s['state'] for s in path].count('next') == 1


def test_a_quiz_topic_is_done_only_once_mastered():
    nearly = progress(topic_stats={'festivals': [7, 10, 0, 0]})
    mastered = progress(topic_stats={'festivals': [8, 10, 0, 0]})
    for prog, expected in ((nearly, False), (mastered, True)):
        path = lp.build_path(None, prog, SECTIONS, open_all)
        festivals = next(s for s in path if s['id'] == 'exercise_festivals')
        assert (festivals['state'] == 'done') is expected


def test_minutes_set_the_number_of_targets():
    for minutes, count in ((10, 2), (20, 3), (30, 3)):
        plan, _ = active_plan(minutes=minutes)
        assert len(plan['targets']) == count, minutes


def test_accuracy_target_goes_to_the_weakest_topic():
    prog = progress(topic_stats={'everyday': [9, 10, 0, 0], 'nature': [2, 10, 0, 0],
                                 'festivals': [5, 10, 0, 0]})
    plan, _ = active_plan(prog=prog)
    target = next(t for t in plan['targets'] if t['kind'] == 'accuracy')
    assert target['topic'] == 'nature'


def test_listening_practice_sets_a_listening_target():
    plan, _ = active_plan(practice='listening')
    target = next(t for t in plan['targets'] if t['kind'] == 'accuracy')
    assert target['listen'] is True


def test_accuracy_target_counts_only_this_weeks_answers():
    prog = progress(topic_stats={'everyday': [0, 20, 0, 0]})
    plan, _ = active_plan(prog=prog)
    target = next(t for t in plan['targets'] if t['kind'] == 'accuracy')
    assert target['topic'] == 'everyday'
    # 20 old wrong answers must not drag this week down: 9/10 is 90%.
    for correct in [True] * 9 + [False]:
        lp.record_answer(prog, 'everyday', correct)
    assert lp.target_status(target, prog)['met']


def test_accuracy_target_needs_enough_answers():
    plan, prog = active_plan()
    target = next(t for t in plan['targets'] if t['kind'] == 'accuracy')
    for _ in range(lp.ACCURACY_NEED - 1):
        lp.record_answer(prog, target['topic'], True)
    assert not lp.target_status(target, prog)['met']
    lp.record_answer(prog, target['topic'], True)
    assert lp.target_status(target, prog)['met']


def test_xp_target_counts_from_the_week_start():
    plan, prog = active_plan(minutes=20, prog=progress(xp=500))
    target = next(t for t in plan['targets'] if t['kind'] == 'xp')
    assert not lp.target_status(target, prog)['met']
    prog['xp'] = 500 + target['need']
    assert lp.target_status(target, prog)['met']


def test_review_opens_after_a_week_or_when_all_met():
    plan, prog = active_plan()
    assert not lp.review_due(plan, prog, TODAY + timedelta(days=6))
    assert lp.review_due(plan, prog, TODAY + timedelta(days=7))

    prog['sections_visited'] = [s['id'] for s in SECTIONS]
    prog['xp'] = 1000
    for t in plan['targets']:
        if t['kind'] == 'accuracy':
            for _ in range(lp.ACCURACY_NEED):
                lp.record_answer(prog, t['topic'], True, t['listen'])
    assert lp.review_due(plan, prog, TODAY)


def test_review_writes_history_and_caps_it():
    plan, prog = active_plan()
    for week in range(lp.HISTORY_KEPT + 3):
        lp.close_week(plan, prog, TODAY)
        plan['week'] += 1
    assert len(plan['history']) == lp.HISTORY_KEPT
    assert plan['history'][-1]['of'] == len(plan['targets'])


def test_review_opens_date_is_british():
    plan, _ = active_plan()
    assert lp.review_opens(plan) == '3 November'


def test_question_id_topic_round_trip():
    assert lp.topic_from_question('abc' + lp.question_suffix('nature')) == ('nature', False)
    assert lp.topic_from_question('abc' + lp.question_suffix('nature', True)) == ('nature', True)
    assert lp.topic_from_question('abc') == (None, False)
    assert lp.topic_from_question('abc.not_a_topic') == (None, False)


def test_every_quiz_topic_has_a_title():
    """A new vocabulary topic needs a TOPIC_TITLES entry or it never gets targets."""
    assert set(VOCABULARY) <= set(lp.TOPIC_TITLES)


def test_every_goal_names_only_real_sections():
    from app import SECTION_REQUIREMENTS
    for key, goal in lp.GOALS.items():
        for section_id in goal['path']:
            assert section_id in SECTION_REQUIREMENTS, f"{key}: unknown section {section_id}"


# ---- The routes, end to end -------------------------------------------------

@pytest.fixture
def client():
    return app.test_client()


def progress_of(client):
    with client.session_transaction() as s:
        return s['user_progress']


def start(client, goal='temple', practice='listening', minutes=20):
    return client.post('/api/path/start',
                       json={'goal': goal, 'practice': practice, 'minutes': minutes})


def take_check(client, right=True):
    questions = client.get('/api/path/placement').get_json()['questions']
    answers = []
    for q in questions:
        topic, _ = lp.topic_from_question(q['question_id'])
        meaning = next(w['english'] for w in VOCABULARY[topic] if w['thai'] == q['thai'])
        answers.append({'question_id': q['question_id'],
                        'answer': meaning if right else "I don't know"})
    return client.post('/api/path/placement', json={'answers': answers}).get_json()


def test_progress_page_shows_setup_before_a_plan(client):
    html = client.get('/progress').get_data(as_text=True)
    assert 'Personalized Learning Path (IEP)' in html
    assert 'Build my plan' in html


def test_start_rejects_bad_choices(client):
    assert start(client, goal='fame').status_code == 400


def test_full_flow_start_check_targets(client):
    assert start(client).get_json()['ok']
    assert 'your starting check' in client.get('/progress').get_data(as_text=True)

    result = take_check(client, right=True)
    assert result['right'] == len(VOCABULARY)

    plan = progress_of(client)['learning_path']
    assert plan['status'] == 'active' and plan['week'] == 1
    assert 'Week 1 targets' in client.get('/progress').get_data(as_text=True)


def test_starting_check_pays_no_xp(client):
    start(client)
    take_check(client, right=True)
    assert progress_of(client)['xp'] == 0


def test_starting_check_can_be_skipped(client):
    start(client)
    client.post('/api/path/placement', json={'answers': []})
    assert progress_of(client)['learning_path']['status'] == 'active'


def test_quiz_answers_count_toward_their_topic(client):
    question = client.get('/api/quiz/nature').get_json()
    meaning = next(w['paiboon'] for w in VOCABULARY['nature'] if w['thai'] == question['thai'])
    client.post('/api/check_answer', json={'question_id': question['question_id'],
                                           'answer': meaning, 'options': question['options']})
    assert progress_of(client)['topic_stats']['nature'][:2] == [1, 1]


def test_listening_answers_count_separately(client):
    question = client.get('/api/quiz/nature?listen=true').get_json()
    client.post('/api/check_answer', json={'question_id': question['question_id'],
                                           'answer': 'wrong', 'options': question['options']})
    assert progress_of(client)['topic_stats']['nature'] == [0, 0, 0, 1]


def test_a_retagged_question_counts_nothing(client):
    """Editing the topic in the id gives an id the server never issued."""
    question = client.get('/api/quiz/nature').get_json()
    forged = question['question_id'].replace('.nature', '.festivals')
    client.post('/api/check_answer', json={'question_id': forged, 'answer': 'x',
                                           'options': question['options']})
    assert 'festivals' not in progress_of(client).get('topic_stats', {})


def test_review_is_refused_mid_week(client):
    start(client)
    take_check(client)
    assert client.post('/api/path/review').status_code == 400


def test_review_after_a_week_moves_on(client):
    start(client)
    take_check(client)
    with client.session_transaction() as s:
        s['user_progress']['learning_path']['week_start'] = (
            date.today() - timedelta(days=7)).isoformat()
        s.modified = True   # a nested edit is invisible to Flask otherwise
    assert client.post('/api/path/review').get_json()['ok']
    plan = progress_of(client)['learning_path']
    assert plan['week'] == 2
    assert plan['history'][0]['week'] == 1


def test_changing_goals_keeps_the_history(client):
    start(client)
    take_check(client)
    with client.session_transaction() as s:
        s['user_progress']['learning_path']['week_start'] = (
            date.today() - timedelta(days=7)).isoformat()
        s.modified = True   # a nested edit is invisible to Flask otherwise
    client.post('/api/path/review')
    client.post('/api/path/reset')
    html = client.get('/progress').get_data(as_text=True)
    assert 'Build my plan' in html and 'Past weeks' in html

    start(client, goal='reading')
    assert len(progress_of(client)['learning_path']['history']) == 1


def test_cookie_stays_well_under_the_browser_limit(client):
    """The session is a cookie (~4KB max). A full plan plus a busy quiz session
    must leave headroom, or the browser silently drops it and the learner is
    logged out with their progress gone."""
    start(client)
    take_check(client)
    with client.session_transaction() as s:
        s['user_progress']['learning_path']['history'] = [
            {'week': n, 'ended': '2026-10-27', 'met': 2, 'of': 3}
            for n in range(lp.HISTORY_KEPT)]
        s['user_progress']['sections_visited'] = [
            section['id'] for section in _outline_sections()]
        s.modified = True
    for _ in range(35):
        client.get('/api/quiz/festivals')
    client.get('/progress')
    assert len(client.get_cookie('session').value) < 3800
