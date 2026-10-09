"""Sentence builder drill for the Sentences page.

The learner sees an English sentence and taps Thai word tiles into the right
order. It is the one exercise on the page where they make a sentence rather
than read one, and it drills exactly the patterns the page teaches: กำลัง /
แล้ว / จะ, ไม่ and its friends, and questions.

Tiles are split by hand, not by a word-cutting library, because Thai has no
spaces and an automatic split that cut a word wrongly would teach the wrong
thing. Every sentence here has ONE natural order: anything with a movable time
word (พรุ่งนี้, เมื่อวาน) is left out, because the marker can only accept one
answer.

Placeholders let one entry serve both speakers:
    {I}  ผม / ดิฉัน          the speaker's "I"
    {p}  ครับ / ค่ะ          statement particle
    {q}  ครับ / คะ           question particle (women's rises: คะ, not ค่ะ)

DRAFT Thai — not yet checked by a native speaker, like the rest of the
Sentences page.
"""

import random

SPEAKER_WORDS = {
    'male': {'{I}': 'ผม', '{p}': 'ครับ', '{q}': 'ครับ'},
    'female': {'{I}': 'ดิฉัน', '{p}': 'ค่ะ', '{q}': 'คะ'},
}

# The on-tile romanisation, same spelling as the rest of the page.
ROMANISATION = {
    'ผม': 'pǒm', 'ดิฉัน': 'dì-chǎn', 'ครับ': 'kráp', 'ค่ะ': 'kâ', 'คะ': 'ká',
    'คุณ': 'kun', 'เขา': 'kǎo',
    'กำลัง': 'gam-laŋ', 'แล้ว': 'lɛ́ɛo', 'จะ': 'jà', 'ยัง': 'yaŋ',
    'ไม่': 'mâi', 'ได้': 'dâi', 'ไหม': 'mǎi', 'หรือ': 'rʉ̌ʉ',
    'กิน': 'gin', 'ข้าว': 'kâao', 'ทำงาน': 'tam ŋaan', 'เสร็จ': 'sèt',
    'อ่าน': 'àan', 'หนังสือ': 'nǎŋ-sʉ̌ʉ', 'เรียน': 'riian',
    'ภาษาไทย': 'paa-sǎa tai', 'ไป': 'bpai', 'มา': 'maa',
    'เมืองไทย': 'mʉaŋ-tai', 'เผ็ด': 'pèt', 'พูด': 'pûut', 'ไทย': 'tai',
    'ชื่อ': 'chʉ̂ʉ', 'อะไร': 'à-rai', 'ไหน': 'nǎi',
}

# Grouped by what they practise, in the order the page teaches it.
SENTENCES = [
    # กำลัง — happening now
    {'english': "I'm eating.", 'tiles': ['{I}', 'กำลัง', 'กิน', 'ข้าว', '{p}'], 'topic': 'กำลัง'},
    {'english': "I'm working.", 'tiles': ['{I}', 'กำลัง', 'ทำงาน', '{p}'], 'topic': 'กำลัง'},
    {'english': 'He is reading a book.', 'tiles': ['เขา', 'กำลัง', 'อ่าน', 'หนังสือ', '{p}'], 'topic': 'กำลัง'},
    {'english': "I'm studying Thai.", 'tiles': ['{I}', 'กำลัง', 'เรียน', 'ภาษาไทย', '{p}'], 'topic': 'กำลัง'},
    # แล้ว — already done
    {'english': "I've already eaten.", 'tiles': ['{I}', 'กิน', 'ข้าว', 'แล้ว', '{p}'], 'topic': 'แล้ว'},
    {'english': 'He has already gone.', 'tiles': ['เขา', 'ไป', 'แล้ว', '{p}'], 'topic': 'แล้ว'},
    {'english': "I've finished work.", 'tiles': ['{I}', 'ทำงาน', 'เสร็จ', 'แล้ว', '{p}'], 'topic': 'แล้ว'},
    # จะ — will
    {'english': 'I will go to Thailand.', 'tiles': ['{I}', 'จะ', 'ไป', 'เมืองไทย', '{p}'], 'topic': 'จะ'},
    {'english': 'I will study Thai.', 'tiles': ['{I}', 'จะ', 'เรียน', 'ภาษาไทย', '{p}'], 'topic': 'จะ'},
    {'english': 'He will come.', 'tiles': ['เขา', 'จะ', 'มา', '{p}'], 'topic': 'จะ'},
    {'english': "I'm about to go.", 'tiles': ['{I}', 'กำลัง', 'จะ', 'ไป', '{p}'], 'topic': 'จะ'},
    # ไม่ — saying no
    {'english': "I'm not going.", 'tiles': ['{I}', 'ไม่', 'ไป', '{p}'], 'topic': 'ไม่'},
    {'english': "It isn't spicy.", 'tiles': ['ไม่', 'เผ็ด', '{p}'], 'topic': 'ไม่'},
    {'english': "I didn't go.", 'tiles': ['{I}', 'ไม่', 'ได้', 'ไป', '{p}'], 'topic': 'ไม่',
     'tip': 'ไม่ได้ BEFORE the verb = didn\'t. After it (ไปไม่ได้) = can\'t.'},
    {'english': "I can't go.", 'tiles': ['{I}', 'ไป', 'ไม่', 'ได้', '{p}'], 'topic': 'ไม่',
     'tip': 'ไม่ได้ AFTER the verb = can\'t. Before it (ไม่ได้ไป) = didn\'t.'},
    {'english': "I haven't eaten yet.", 'tiles': ['{I}', 'ยัง', 'ไม่', 'ได้', 'กิน', 'ข้าว', '{p}'], 'topic': 'ไม่'},
    # Questions
    {'english': 'Are you going?', 'tiles': ['คุณ', 'ไป', 'ไหม', '{q}'], 'topic': 'questions'},
    {'english': 'Can you speak Thai?', 'tiles': ['คุณ', 'พูด', 'ไทย', 'ได้', 'ไหม', '{q}'], 'topic': 'questions'},
    {'english': "What's your name?", 'tiles': ['คุณ', 'ชื่อ', 'อะไร', '{q}'], 'topic': 'questions'},
    {'english': 'Where are you going?', 'tiles': ['คุณ', 'ไป', 'ไหน', '{q}'], 'topic': 'questions'},
    {'english': 'Have you eaten yet?', 'tiles': ['คุณ', 'กิน', 'ข้าว', 'แล้ว', 'หรือ', 'ยัง', '{q}'], 'topic': 'questions'},
]


def tiles_for(sentence, speaker):
    """The sentence's tiles in the correct order, for a male or female speaker."""
    words = SPEAKER_WORDS[speaker]
    return [words.get(tile, tile) for tile in sentence['tiles']]


def answer_text(tiles):
    """The form an answer is marked in: the tiles run together, as Thai is written."""
    return ''.join(tiles)


def all_answers(speaker):
    """Every correct answer for this speaker.

    The marker can only recover the right answer after a wrong guess by
    testing candidates against the stored token, so it tests these.
    """
    return [answer_text(tiles_for(s, speaker)) for s in SENTENCES]


def explain(answer):
    """The tiles (with romanisation) and any tip for a correct answer string."""
    for sentence in SENTENCES:
        for speaker in SPEAKER_WORDS:
            tiles = tiles_for(sentence, speaker)
            if answer_text(tiles) == answer:
                return {'tiles': [{'thai': t, 'roman': ROMANISATION.get(t, '')} for t in tiles],
                        'tip': sentence.get('tip')}
    return {'tiles': [], 'tip': None}


def pick_speaker(gender, rng=random):
    """The learner's own gender, or a random one for 'neutral'."""
    return gender if gender in SPEAKER_WORDS else rng.choice(sorted(SPEAKER_WORDS))


def deal(gender, rng=random):
    """One question: the sentence, its speaker, and its tiles shuffled.

    Re-shuffles until the tiles are out of order, so the learner never gets a
    question that is already answered.
    """
    sentence = rng.choice(SENTENCES)
    speaker = pick_speaker(gender, rng)
    correct = tiles_for(sentence, speaker)
    shuffled = list(correct)
    while answer_text(shuffled) == answer_text(correct):
        rng.shuffle(shuffled)
    return {
        'sentence': sentence,
        'speaker': speaker,
        'answer': answer_text(correct),
        'tiles': [{'thai': t, 'roman': ROMANISATION.get(t, '')} for t in shuffled],
    }
