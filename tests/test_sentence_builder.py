"""The Build the Sentence drill on /sentences.

Two halves: the sentence data (pure, no Flask) and the API that deals and
marks questions without ever handing the browser the right order.
"""
import random

import pytest

import sentence_builder as sb


# ── The sentences ──────────────────────────────────────────────────────────

@pytest.mark.parametrize('sentence', sb.SENTENCES, ids=lambda s: s['english'])
def test_every_tile_has_a_romanisation(sentence):
    for speaker in sb.SPEAKER_WORDS:
        for tile in sb.tiles_for(sentence, speaker):
            assert sb.ROMANISATION.get(tile), f'no romanisation for {tile!r}'


@pytest.mark.parametrize('sentence', sb.SENTENCES, ids=lambda s: s['english'])
def test_particles_follow_the_speaker(sentence):
    male, female = (sb.answer_text(sb.tiles_for(sentence, s)) for s in ('male', 'female'))
    assert male.endswith('ครับ')
    # Women end a question on คะ (high) but a statement on ค่ะ (falling).
    assert female.endswith('คะ' if '{q}' in sentence['tiles'] else 'ค่ะ')


def test_no_two_sentences_share_an_answer():
    # The marker recovers the right answer by matching strings, so two
    # sentences with the same text would make the reveal ambiguous.
    # Alternative orders count too: one sentence's alternative must never be
    # another sentence's answer, or canonical() would mark it as the wrong one.
    for speaker in sb.SPEAKER_WORDS:
        answers = sb.all_answers(speaker)
        assert len(answers) == len(set(answers))
        everything = [a for s in sb.SENTENCES for a in sb.accepted(s, speaker)]
        assert len(everything) == len(set(everything))


# ── Challenge level ────────────────────────────────────────────────────────

CHALLENGE = [s for s in sb.SENTENCES if sb.level_of(s) == 'challenge']


def test_there_is_a_real_challenge_pool():
    assert len(CHALLENGE) >= 12
    starter_len = max(len(s['tiles']) for s in sb.SENTENCES if sb.level_of(s) == 'starter')
    # Longer on average than anything at starter level.
    assert sum(len(s['tiles']) for s in CHALLENGE) / len(CHALLENGE) > starter_len - 1


def test_every_sentence_has_a_known_level():
    assert {sb.level_of(s) for s in sb.SENTENCES} == set(sb.LEVELS)


def test_each_level_only_deals_its_own_sentences():
    rng = random.Random(3)
    for level in sb.LEVELS:
        assert {sb.level_of(sb.deal('female', level, rng)['sentence'])
                for _ in range(100)} == {level}


@pytest.mark.parametrize('sentence', [s for s in sb.SENTENCES if s.get('alternates')],
                         ids=lambda s: s['english'])
def test_alternatives_use_exactly_the_same_tiles(sentence):
    for alt in sentence['alternates']:
        assert sorted(alt) == sorted(sentence['tiles'])
        assert alt != sentence['tiles']


@pytest.mark.parametrize('sentence', [s for s in sb.SENTENCES if s.get('alternates')],
                         ids=lambda s: s['english'])
def test_an_alternative_order_maps_to_the_main_one(sentence):
    for speaker in sb.SPEAKER_WORDS:
        main = sb.answer_text(sb.tiles_for(sentence, speaker))
        for alt in sentence['alternates']:
            assert sb.canonical(sb.answer_text(sb.tiles_for(sentence, speaker, alt))) == main


def test_canonical_leaves_a_wrong_answer_wrong():
    assert sb.canonical('ครับไปผม') == 'ครับไปผม'


def test_didnt_and_cant_use_the_same_tiles_in_a_different_order():
    # The pair exists to teach that word order changes the meaning.
    didnt = next(s for s in sb.SENTENCES if s['english'] == "I didn't go.")
    cant = next(s for s in sb.SENTENCES if s['english'] == "I can't go.")
    assert sorted(didnt['tiles']) == sorted(cant['tiles'])
    assert didnt['tiles'] != cant['tiles']


def test_a_dealt_question_is_never_already_solved():
    # Not in the main order, and not in any accepted alternative either.
    rng = random.Random(1)
    for level in sb.LEVELS:
        for _ in range(300):
            q = sb.deal('male', level, rng)
            dealt = sb.answer_text([t['thai'] for t in q['tiles']])
            assert dealt not in sb.accepted(q['sentence'], 'male')
            assert sorted(dealt) == sorted(q['answer'])


def test_neutral_learners_get_either_speaker():
    rng = random.Random(2)
    assert {sb.pick_speaker('neutral', rng) for _ in range(50)} == {'male', 'female'}


def test_explain_returns_the_tiles_in_order():
    sentence = sb.SENTENCES[0]
    tiles = sb.tiles_for(sentence, 'female')
    reveal = sb.explain(sb.answer_text(tiles))
    assert [t['thai'] for t in reveal['tiles']] == tiles


# ── The API ────────────────────────────────────────────────────────────────

def _deal(client):
    res = client.get('/api/sentence-builder')
    assert res.status_code == 200
    return res.get_json()


def _correct_order(q):
    """Work out the right order the way a learner would: from the English."""
    sentence = next(s for s in sb.SENTENCES if s['english'] == q['english'])
    return sb.tiles_for(sentence, q['speaker'])


def test_the_dealt_question_does_not_contain_the_answer(unlocked_client):
    q = _deal(unlocked_client)
    assert set(q) == {'question_id', 'english', 'speaker', 'tiles', 'level'}


def test_a_right_answer_is_marked_right_and_paid(make_client):
    client = make_client(is_developer=False)
    q = _deal(client)
    res = client.post('/api/sentence-builder/check',
                      json={'question_id': q['question_id'], 'tiles': _correct_order(q)})
    body = res.get_json()
    assert body['correct'] is True
    assert body['scored'] is True
    assert body['xp_earned'] > 0


def test_a_wrong_answer_shows_the_right_order_and_pays_nothing(unlocked_client):
    q = _deal(unlocked_client)
    wrong = list(reversed(_correct_order(q)))
    body = unlocked_client.post('/api/sentence-builder/check',
                                json={'question_id': q['question_id'], 'tiles': wrong}).get_json()
    assert body['correct'] is False
    assert body['xp_earned'] == 0
    assert [t['thai'] for t in body['correct_tiles']] == _correct_order(q)


def test_a_question_can_only_be_marked_once(unlocked_client):
    q = _deal(unlocked_client)
    payload = {'question_id': q['question_id'], 'tiles': _correct_order(q)}
    assert unlocked_client.post('/api/sentence-builder/check', json=payload).status_code == 200
    again = unlocked_client.post('/api/sentence-builder/check', json=payload)
    assert again.status_code == 409
    assert again.get_json()['expired'] is True


def test_bad_input_is_refused(unlocked_client):
    res = unlocked_client.post('/api/sentence-builder/check',
                               json={'question_id': 'x', 'tiles': 'ผมไปครับ'})
    assert res.status_code == 400


def test_the_drill_is_locked_like_the_page(make_client):
    client = make_client(is_developer=False, full_unlock=False, level=1,
                         subscription_tier='free')
    assert client.get('/api/sentence-builder').status_code == 403
    assert client.post('/api/sentence-builder/check',
                       json={'question_id': 'x', 'tiles': []}).status_code == 403


def test_the_drill_is_on_the_page(unlocked_client):
    html = unlocked_client.get('/sentences').get_data(as_text=True)
    assert 'id="sentence-builder"' in html
    assert 'id="sb-drill"' in html


def _deal_level(client, level):
    res = client.get(f'/api/sentence-builder?level={level}')
    assert res.status_code == 200
    return res.get_json()


def test_challenge_questions_come_from_the_challenge_pool(unlocked_client):
    english = {s['english'] for s in CHALLENGE}
    for _ in range(10):
        q = _deal_level(unlocked_client, 'challenge')
        assert q['level'] == 'challenge' and q['english'] in english


def test_an_unknown_level_is_refused(unlocked_client):
    assert unlocked_client.get('/api/sentence-builder?level=expert').status_code == 400


def test_an_alternative_order_is_marked_right(unlocked_client):
    # Keep dealing until a sentence with an alternative order comes up.
    for _ in range(200):
        q = _deal_level(unlocked_client, 'challenge')
        sentence = next(s for s in sb.SENTENCES if s['english'] == q['english'])
        if sentence.get('alternates'):
            break
    else:
        pytest.fail('no sentence with alternatives was dealt')
    alt = sb.tiles_for(sentence, q['speaker'], sentence['alternates'][0])
    body = unlocked_client.post('/api/sentence-builder/check',
                                json={'question_id': q['question_id'], 'tiles': alt}).get_json()
    assert body['correct'] is True
