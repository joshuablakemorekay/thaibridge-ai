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
    for speaker in sb.SPEAKER_WORDS:
        answers = sb.all_answers(speaker)
        assert len(answers) == len(set(answers))


def test_didnt_and_cant_use_the_same_tiles_in_a_different_order():
    # The pair exists to teach that word order changes the meaning.
    didnt = next(s for s in sb.SENTENCES if s['english'] == "I didn't go.")
    cant = next(s for s in sb.SENTENCES if s['english'] == "I can't go.")
    assert sorted(didnt['tiles']) == sorted(cant['tiles'])
    assert didnt['tiles'] != cant['tiles']


def test_a_dealt_question_is_never_already_solved():
    rng = random.Random(1)
    for _ in range(300):
        q = sb.deal('male', rng)
        dealt = sb.answer_text([t['thai'] for t in q['tiles']])
        assert dealt != q['answer']
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
    assert set(q) == {'question_id', 'english', 'speaker', 'tiles'}


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
