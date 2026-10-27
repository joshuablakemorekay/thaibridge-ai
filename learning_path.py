"""The Personalized Learning Path (IEP) — a learner's own plan, on the Progress page.

WHAT MAKES IT AN IEP AND NOT JUST A LIST
----------------------------------------
A school IEP (Individualized Education Program) has three working parts, and
this copies all three rather than borrowing the name:

  1. A STARTING POINT — what the learner can already do. Here: a six-question
     check, one question per vocabulary topic, that seeds the per-topic scores.
  2. MEASURABLE TARGETS — not "get better at Thai" but "score 80% on 10
     Festival answers". Two or three a week, each one checkable from data the
     app already records, so "met" is a fact, not a feeling.
  3. REGULAR REVIEW — after a week (or sooner, once every target is met) the
     learner reviews it: the week is written to their history with how many
     targets were met, and a fresh set is drawn from where they are now.

WHY RULES AND NOT AI
--------------------
Every number here comes from the learner's own record — pages opened, quiz
answers per topic, XP — run through fixed rules. That makes the plan free to
run, instant, and testable, and it means two learners with the same record get
the same plan. The AI tutor is still one tap away for anything a rule cannot do.

"LEARNING STYLE"
----------------
The card promises a plan built around the learner's learning style. The idea
that people are "visual" or "auditory" learners does not hold up in research,
so the plan asks something it can honestly use instead: how the learner likes
to PRACTISE (listening, reading or speaking). That changes which quiz the
accuracy target uses and what the path puts first.

STORAGE
-------
Everything lives in the session's user_progress dict, so it is saved to the
account by progress.py with no schema change, and works (cookie-only) for a
visitor who has not signed up. The session is a cookie with a ~4KB ceiling,
which is why the plan is stored in short keys and the history is capped.

This module is pure: it is handed the progress dict, a can_open(section_id)
function and the outline, and never touches Flask, so the tests can drive it
with plain dicts.
"""

from datetime import date, timedelta

# ---- What the learner chooses ---------------------------------------------

# Each goal is an ORDER of sections, most useful first. Sections a goal does not
# name still appear on the path, after these, in the outline's own order — so
# the whole curriculum is always on it, just ranked for this learner. `topics`
# is the order the vocabulary quizzes are tried in when no score says otherwise.
GOALS = {
    'travel': {
        'label': 'Travel in Thailand',
        'path': ['survival', 'alphabet', 'paiboon', 'learn', 'tour_guide',
                 'culture', 'exercise_isan_dialect', 'formality', 'sentences',
                 'tones_classes'],
        'topics': ['everyday', 'festivals', 'nature', 'isan_dialect',
                   'buddhist_formal', 'theravada_dhamma'],
    },
    'living': {
        'label': 'Live or work in Thailand',
        'path': ['survival', 'alphabet', 'paiboon', 'learn', 'tones_classes',
                 'vowels_syllables', 'read_write', 'grammar', 'sentences',
                 'formality', 'register', 'gender_examples', 'business_thai'],
        'topics': ['everyday', 'festivals', 'nature', 'isan_dialect',
                   'buddhist_formal', 'theravada_dhamma'],
    },
    'temple': {
        'label': 'Temple life and the Dhamma',
        'path': ['alphabet', 'paiboon', 'theravada', 'chanting', 'meditation',
                 'practising_anywhere', 'dhamma_and_culture', 'exercise_formal',
                 'register', 'formality', 'read_write'],
        'topics': ['theravada_dhamma', 'buddhist_formal', 'festivals',
                   'everyday', 'nature', 'isan_dialect'],
    },
    'reading': {
        'label': 'Read and write Thai',
        'path': ['alphabet', 'paiboon', 'vowels_syllables', 'read_write',
                 'tones_classes', 'learn', 'grammar', 'sentences'],
        'topics': ['everyday', 'nature', 'festivals', 'buddhist_formal',
                   'theravada_dhamma', 'isan_dialect'],
    },
    'conversation': {
        'label': 'Hold a conversation',
        'path': ['survival', 'alphabet', 'paiboon', 'learn', 'tones_classes',
                 'sentences', 'grammar', 'formality', 'register',
                 'gender_examples', 'lessons'],
        'topics': ['everyday', 'festivals', 'nature', 'isan_dialect',
                   'buddhist_formal', 'theravada_dhamma'],
    },
}

PRACTICE = {
    'listening': 'Listening — hearing Thai and picking out what it means',
    'reading':   'Reading — seeing the words written down',
    'speaking':  'Speaking — trying it out loud and chatting',
}

# Minutes a day -> how many targets a week. A 10-minute learner gets two they
# can actually meet; more time adds an XP target sized to it. The XP numbers sit
# well under the daily drill cap (200), so they are reachable on any plan.
MINUTES = {10: 0, 20: 60, 30: 120}

TOPIC_TITLES = {
    'festivals': 'Festival Vocabulary',
    'isan_dialect': 'Isan Dialect',
    'nature': 'Nature Vocabulary',
    'buddhist_formal': 'Buddhist Formal Vocabulary',
    'theravada_dhamma': 'Theravada Dhamma Vocabulary',
    'everyday': 'Everyday Vocabulary',
}

ACCURACY_NEED = 10       # answers in the week before an accuracy target can be met
ACCURACY_PCT = 80        # ...and the share of them that must be right
MASTERED_PCT = 80        # a topic at or above this, over ACCURACY_NEED answers, is "done"
WEEK_DAYS = 7
HISTORY_KEPT = 6         # weeks of history kept — the cookie is small

# ---- Per-topic scores -----------------------------------------------------
# topic_stats[topic] = [right, total, listen_right, listen_total]. A list, not a
# dict, purely to keep the cookie small; these helpers are the only readers.


def record_answer(progress, topic, correct, listening=False):
    """Count one marked quiz answer against its topic."""
    stats = progress.setdefault('topic_stats', {})
    row = stats.setdefault(topic, [0, 0, 0, 0])
    offset = 2 if listening else 0
    row[offset + 1] += 1
    if correct:
        row[offset] += 1


def _counts(progress, topic, listening):
    row = progress.get('topic_stats', {}).get(topic, [0, 0, 0, 0])
    return (row[2], row[3]) if listening else (row[0], row[1])


def topic_accuracy(progress, topic):
    """(right, total) across both quiz kinds."""
    row = progress.get('topic_stats', {}).get(topic, [0, 0, 0, 0])
    return row[0] + row[2], row[1] + row[3]


def topic_mastered(progress, topic):
    right, total = topic_accuracy(progress, topic)
    return total >= ACCURACY_NEED and right * 100 >= MASTERED_PCT * total


# ---- Question ids carry their topic ---------------------------------------
# A quiz question's id is "<uuid>.<topic>" (".<topic>~listen" for the Listening
# Quiz). The answer token is an HMAC over the whole id, so a learner who edits
# the topic only produces an id the server never issued — it scores nothing.

def question_suffix(topic, listening=False):
    return f".{topic}{'~listen' if listening else ''}"


def topic_from_question(question_id):
    """(topic, listening) from a question id, or (None, False) if it has none."""
    if not question_id or '.' not in question_id:
        return None, False
    tail = question_id.split('.', 1)[1]
    listening = tail.endswith('~listen')
    topic = tail[:-len('~listen')] if listening else tail
    return (topic if topic in TOPIC_TITLES else None), listening


# ---- The plan --------------------------------------------------------------

def new_plan(goal, practice, minutes, history=None):
    """A plan waiting for its starting check. Returns None for a bad choice."""
    if goal not in GOALS or practice not in PRACTICE or minutes not in MINUTES:
        return None
    return {
        'goal': goal, 'practice': practice, 'minutes': minutes,
        'status': 'placement',
        'week': 0,
        'history': list(history or [])[-HISTORY_KEPT:],
    }


def _exercise_topic(section):
    """The quiz topic behind an /exercise/<topic> section, else None."""
    url = section.get('url', '')
    return url.rsplit('/', 1)[1] if url.startswith('/exercise/') else None


def build_path(plan, progress, sections, can_open):
    """Every section, ranked for this learner, each marked done/next/open/locked.

    `sections` is the curriculum outline flattened (id, title, url, level). With
    no plan the outline order is kept, so the path still reads sensibly before
    a goal is set. A section is DONE when it has been opened — or, for a quiz
    topic, which the visit list does not record, when it is mastered.
    """
    by_id = {s['id']: s for s in sections}
    # A plan reset by "change my goals" keeps only its history and has no goal.
    if plan and plan.get('goal') not in GOALS:
        plan = None
    preferred = list(GOALS[plan['goal']]['path']) if plan else []
    if plan and plan.get('practice') == 'reading' and 'read_write' in by_id:
        # A reader wants the script early: straight after the alphabet.
        preferred = [s for s in preferred if s != 'read_write']
        at = preferred.index('alphabet') + 1 if 'alphabet' in preferred else 0
        preferred.insert(at, 'read_write')

    order = [sid for sid in preferred if sid in by_id]
    order += [s['id'] for s in sections if s['id'] not in order]

    visited = set(progress.get('sections_visited', []))
    path, next_marked = [], False
    for sid in order:
        section = by_id[sid]
        topic = _exercise_topic(section)
        opens, why_locked = can_open(sid)
        if topic and topic_mastered(progress, topic) or (not topic and sid in visited):
            state = 'done'
        elif not opens:
            state = 'locked'
        elif not next_marked:
            state, next_marked = 'next', True
        else:
            state = 'open'
        path.append({**section, 'state': state,
                     'why_locked': why_locked if state == 'locked' else ''})
    return path


def _weakest_topic(plan, progress, can_open_topic):
    """The quiz topic most worth a target this week, or None if none can open.

    Weakest first: a topic with answers below the mastery line, lowest score
    first. Failing that, the first untried topic in the goal's own order. If
    everything open is already mastered, the lowest-scoring one anyway — there
    is always something to sharpen.
    """
    topics = [t for t in GOALS[plan['goal']]['topics'] if can_open_topic(t)]
    if not topics:
        return None

    def score(topic):
        right, total = topic_accuracy(progress, topic)
        return right / total if total else None

    tried = [t for t in topics if score(t) is not None and not topic_mastered(progress, t)]
    if tried:
        return min(tried, key=score)
    untried = [t for t in topics if score(t) is None]
    if untried:
        return untried[0]
    return min(topics, key=score)


def start_week(plan, progress, path, can_open_topic, today):
    """Draw this week's targets from where the learner is now."""
    targets = []

    # Quiz topics are left to the accuracy target, so the page to visit is the
    # first open, unfinished section that is not one.
    next_up = next((s for s in path if s['state'] in ('next', 'open')
                    and not _exercise_topic(s)), None)
    if next_up:
        targets.append({'kind': 'visit', 'section': next_up['id'],
                        'title': next_up['title'], 'url': next_up['url']})

    topic = _weakest_topic(plan, progress, can_open_topic)
    if topic:
        listening = plan['practice'] == 'listening'
        right, total = _counts(progress, topic, listening)
        targets.append({'kind': 'accuracy', 'topic': topic, 'listen': listening,
                        'start': [right, total]})

    xp_need = MINUTES[plan['minutes']] or (60 if len(targets) < 2 else 0)
    if xp_need:
        targets.append({'kind': 'xp', 'need': xp_need, 'start': progress.get('xp', 0)})

    plan.update(status='active', targets=targets,
                week=plan.get('week', 0) + 1, week_start=today.isoformat())
    return plan


def target_status(target, progress):
    """{'met': bool, 'label': str, 'detail': str, 'url': str} for one target."""
    kind = target['kind']
    if kind == 'visit':
        met = target['section'] in progress.get('sections_visited', [])
        return {'met': met, 'label': f"Work through {target['title']}",
                'detail': 'Done' if met else 'Not opened yet', 'url': target['url']}

    if kind == 'accuracy':
        right, total = _counts(progress, target['topic'], target['listen'])
        right -= target['start'][0]
        total -= target['start'][1]
        pct = round(right * 100 / total) if total else 0
        met = total >= ACCURACY_NEED and right * 100 >= ACCURACY_PCT * total
        quiz = 'Listening Quiz' if target['listen'] else 'quiz'
        return {'met': met,
                'label': (f"Score {ACCURACY_PCT}% or more over {ACCURACY_NEED} "
                          f"{TOPIC_TITLES[target['topic']]} {quiz} answers"),
                'detail': (f"{total} answered this week, {pct}% right"
                           if total else 'No answers yet this week'),
                'url': f"/exercise/{target['topic']}"}

    gained = max(0, progress.get('xp', 0) - target['start'])
    return {'met': gained >= target['need'],
            'label': f"Earn {target['need']} XP this week",
            'detail': f"{min(gained, target['need'])} of {target['need']} so far",
            'url': ''}


def review_due(plan, progress, today):
    """A week is up, or every target is already met."""
    if not plan or plan.get('status') != 'active':
        return False
    started = date.fromisoformat(plan['week_start'])
    if today - started >= timedelta(days=WEEK_DAYS):
        return True
    targets = plan.get('targets', [])
    return bool(targets) and all(target_status(t, progress)['met'] for t in targets)


def review_opens(plan):
    """The day the weekly review opens, written the British way: '3 November'."""
    if not plan or not plan.get('week_start'):
        return ''
    opens = date.fromisoformat(plan['week_start']) + timedelta(days=WEEK_DAYS)
    return f"{opens.day} {opens:%B}"


def close_week(plan, progress, today):
    """Write the week to the history. The caller then calls start_week."""
    statuses = [target_status(t, progress) for t in plan.get('targets', [])]
    plan['history'] = (plan.get('history', []) + [{
        'week': plan['week'],
        'ended': today.isoformat(),
        'met': sum(s['met'] for s in statuses),
        'of': len(statuses),
    }])[-HISTORY_KEPT:]
    return plan
