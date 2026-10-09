"""Sentence builder drill for the Sentences page.

The learner sees an English sentence and taps Thai word tiles into the right
order. It is the one exercise on the page where they make a sentence rather
than read one, and it drills exactly the patterns the page teaches: กำลัง /
แล้ว / จะ, ไม่ and its friends, and questions.

Tiles are split by hand, not by a word-cutting library, because Thai has no
spaces and an automatic split that cut a word wrongly would teach the wrong
thing.

Two levels. STARTER sentences are short and have one natural order. CHALLENGE
sentences are longer and join ideas (แต่, เพราะ, ถ้า…ก็, หลังจาก, ตอนที่, ที่,
ว่า …) — and a long Thai sentence can often be said more than one way round
("after I eat, I'll call you" / "I'll call you after I eat"). Those list the
other correct orders under 'alternates', and the marker accepts any of them.

Placeholders let one entry serve both speakers:
    {I}  ผม / ดิฉัน          the speaker's "I"
    {p}  ครับ / ค่ะ          statement particle
    {q}  ครับ / คะ           question particle (women's rises: คะ, not ค่ะ) —
                             also after นะ, where women say นะคะ

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
    # Challenge words
    'อยาก': 'yàak', 'แต่': 'dtɛ̀ɛ', 'มี': 'mii', 'เวลา': 'wee-laa',
    'เพราะ': 'prɔ́', 'สบาย': 'sà-baai', 'ถ้า': 'tâa', 'ฝน': 'fǒn', 'ตก': 'dtòk',
    'ก็': 'gɔ̂ɔ', 'อยู่': 'yùu', 'บ้าน': 'bâan', 'โทร': 'too', 'หา': 'hǎa',
    'หลังจาก': 'lǎŋ-jàak', 'ร้าน': 'ráan', 'ที่': 'tîi', 'เรา': 'rao',
    'เมื่อวาน': 'mʉ̂a waan', 'อร่อย': 'à-rɔ̀i', 'มาก': 'mâak', 'คิด': 'kít',
    'ว่า': 'wâa', 'พรุ่งนี้': 'prûŋ níi', 'ตอนที่': 'dtɔɔn-tîi',
    'ทุกวัน': 'túk wan', 'สอง': 'sɔ̌ɔŋ', 'ปี': 'bpii', 'ช่วย': 'chûai',
    'ช้าๆ': 'cháa-cháa', 'หน่อย': 'nɔ̀ɔi', 'เคย': 'kəəi',
    'เชียงใหม่': 'chiaŋ-mài', 'อาหาร': 'aa-hǎan', 'กว่า': 'gwàa',
    'อังกฤษ': 'aŋ-grìt', 'ต้อง': 'dtɔ̂ŋ', 'ตื่น': 'dtʉ̀ʉn', 'เช้า': 'cháao',
    'ครอบครัว': 'krɔ̂ɔp-kruua', 'ของ': 'kɔ̌ɔŋ', 'กี่': 'gìi', 'คน': 'kon',
    'ด้วยกัน': 'dûai-gan', 'นะ': 'ná',
}

LEVELS = ('starter', 'challenge')

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

    # ── Challenge: longer sentences that join ideas ──
    {'level': 'challenge', 'topic': 'แต่', 'english': "I want to go, but I don't have time.",
     'tiles': ['{I}', 'อยาก', 'ไป', 'แต่', 'ไม่', 'มี', 'เวลา', '{p}']},
    {'level': 'challenge', 'topic': 'เพราะ', 'english': "I'm not going to work because I'm not well.",
     'tiles': ['{I}', 'ไม่', 'ไป', 'ทำงาน', 'เพราะ', 'ไม่', 'สบาย', '{p}'],
     'tip': 'ไม่สบาย — literally "not comfortable" — is the everyday way to say you\'re ill.'},
    {'level': 'challenge', 'topic': 'ถ้า…ก็', 'english': "If it rains, I'll stay at home.",
     'tiles': ['ถ้า', 'ฝน', 'ตก', '{I}', 'ก็', 'จะ', 'อยู่', 'บ้าน', '{p}'],
     'tip': 'ก็ sits after the subject of the second half: ผมก็จะ…'},
    {'level': 'challenge', 'topic': 'หลังจาก', 'english': "I'll call you after I eat.",
     'tiles': ['{I}', 'จะ', 'โทร', 'หา', 'คุณ', 'หลังจาก', 'กิน', 'ข้าว', '{p}'],
     'alternates': [['หลังจาก', 'กิน', 'ข้าว', '{I}', 'จะ', 'โทร', 'หา', 'คุณ', '{p}']]},
    {'level': 'challenge', 'topic': 'ที่', 'english': 'The restaurant we went to yesterday was really good.',
     'tiles': ['ร้าน', 'ที่', 'เรา', 'ไป', 'เมื่อวาน', 'อร่อย', 'มาก', '{p}'],
     'tip': 'The noun comes first, then ที่ and the description: ร้าน ที่เราไปเมื่อวาน.'},
    {'level': 'challenge', 'topic': 'ว่า', 'english': 'I think it will rain tomorrow.',
     'tiles': ['{I}', 'คิด', 'ว่า', 'พรุ่งนี้', 'ฝน', 'จะ', 'ตก', '{p}'],
     'alternates': [['{I}', 'คิด', 'ว่า', 'ฝน', 'จะ', 'ตก', 'พรุ่งนี้', '{p}']]},
    {'level': 'challenge', 'topic': 'ตอนที่', 'english': 'When I was in Thailand, I studied Thai every day.',
     'tiles': ['ตอนที่', '{I}', 'อยู่', 'เมืองไทย', '{I}', 'เรียน', 'ภาษาไทย', 'ทุกวัน', '{p}'],
     'alternates': [['{I}', 'เรียน', 'ภาษาไทย', 'ทุกวัน', 'ตอนที่', '{I}', 'อยู่', 'เมืองไทย', '{p}']],
     'tip': 'No past tense needed — ตอนที่ (when) already sets the time.'},
    {'level': 'challenge', 'topic': 'มา…แล้ว', 'english': "I've been learning Thai for two years.",
     'tiles': ['{I}', 'เรียน', 'ภาษาไทย', 'มา', 'สอง', 'ปี', 'แล้ว', '{p}'],
     'tip': 'Verb + มา + length of time + แล้ว = "have been doing it for…".'},
    {'level': 'challenge', 'topic': 'เคย', 'english': "I've never been to Chiang Mai.",
     'tiles': ['{I}', 'ไม่', 'เคย', 'ไป', 'เชียงใหม่', '{p}'],
     'tip': 'เคย + verb = have ever done it. ไม่เคย = never.'},
    {'level': 'challenge', 'topic': 'กว่า', 'english': 'Thai food is spicier than English food.',
     'tiles': ['อาหาร', 'ไทย', 'เผ็ด', 'กว่า', 'อาหาร', 'อังกฤษ', '{p}'],
     'tip': 'Adjective + กว่า = more … than. The thing that is "more" comes first.'},
    {'level': 'challenge', 'topic': 'ต้อง', 'english': 'I have to get up early tomorrow.',
     'tiles': ['พรุ่งนี้', '{I}', 'ต้อง', 'ตื่น', 'เช้า', '{p}'],
     'alternates': [['{I}', 'ต้อง', 'ตื่น', 'เช้า', 'พรุ่งนี้', '{p}']]},
    {'level': 'challenge', 'topic': 'questions', 'english': 'Could you speak a bit more slowly, please?',
     'tiles': ['ช่วย', 'พูด', 'ช้าๆ', 'หน่อย', 'ได้', 'ไหม', '{q}'],
     'tip': 'ช่วย … หน่อย softens a request — the most useful phrase a learner can know.'},
    {'level': 'challenge', 'topic': 'questions', 'english': 'Where did you go yesterday?',
     'tiles': ['เมื่อวาน', 'คุณ', 'ไป', 'ไหน', 'มา', '{q}'],
     'alternates': [['คุณ', 'ไป', 'ไหน', 'มา', 'เมื่อวาน', '{q}']],
     'tip': 'ไปไหนมา = "went where (and came back)" — the มา shows the trip is over.'},
    {'level': 'challenge', 'topic': 'questions', 'english': 'How many people are in your family?',
     'tiles': ['ครอบครัว', 'ของ', 'คุณ', 'มี', 'กี่', 'คน', '{q}'],
     'tip': 'กี่ (how many) always comes with a classifier — here คน, for people.'},
    {'level': 'challenge', 'topic': 'ถ้า', 'english': "If you have time, let's go and eat together.",
     'tiles': ['ถ้า', 'คุณ', 'มี', 'เวลา', 'ไป', 'กิน', 'ข้าว', 'ด้วยกัน', 'นะ', '{q}'],
     'tip': 'นะ makes a suggestion friendly. Women say นะคะ, men นะครับ.'},
]


def level_of(sentence):
    return sentence.get('level', 'starter')


def tiles_for(sentence, speaker, order=None):
    """The sentence's tiles in the main order (or `order`), for one speaker."""
    words = SPEAKER_WORDS[speaker]
    return [words.get(tile, tile) for tile in (order or sentence['tiles'])]


def answer_text(tiles):
    """The form an answer is marked in: the tiles run together, as Thai is written."""
    return ''.join(tiles)


def accepted(sentence, speaker):
    """Every order of this sentence that counts as right, as answer text."""
    orders = [sentence['tiles']] + sentence.get('alternates', [])
    return {answer_text(tiles_for(sentence, speaker, o)) for o in orders}


def canonical(answer):
    """Map an accepted alternative order onto the sentence's main order.

    Questions are issued against the main order only, so an answer in a
    different-but-correct order is turned into the main one before marking.
    Anything that isn't an accepted order comes back unchanged (and fails).
    """
    for sentence in SENTENCES:
        for speaker in SPEAKER_WORDS:
            if answer in accepted(sentence, speaker):
                return answer_text(tiles_for(sentence, speaker))
    return answer


def all_answers(speaker):
    """Every sentence's main answer for this speaker.

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


def deal(gender, level='starter', rng=random):
    """One question at this level: the sentence, its speaker, its tiles shuffled.

    Re-shuffles until the tiles are in no accepted order, so the learner never
    gets a question that is already answered.
    """
    pool = [s for s in SENTENCES if level_of(s) == level]
    sentence = rng.choice(pool)
    speaker = pick_speaker(gender, rng)
    correct = tiles_for(sentence, speaker)
    right = accepted(sentence, speaker)
    shuffled = list(correct)
    while answer_text(shuffled) in right:
        rng.shuffle(shuffled)
    return {
        'sentence': sentence,
        'speaker': speaker,
        'answer': answer_text(correct),
        'tiles': [{'thai': t, 'roman': ROMANISATION.get(t, '')} for t in shuffled],
    }
