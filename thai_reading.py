"""Reading content for the Read & Write Thai Script page — the single source
of truth for the "Learn to Read" half, the way thai_consonants.py is for the
Alphabet page.

Reading Thai is not "sound the letters left to right". A vowel can be written
BEFORE, AFTER, ABOVE, BELOW or WRAPPED AROUND its consonant, yet you always say
the consonant first. That one rule is the thing this data teaches, so the
syllables here are grouped by where the vowel sits, not by difficulty.

Three stages build towards real reading fluency:

  1. SYLLABLES  — one consonant + one vowel, grouped by vowel position, so the
     learner meets "the vowel is not always after the letter" head on.
  2. WORDS      — short real words, themed on dharma vocabulary (merit, giving,
     kamma …) so the vocabulary is useful the moment it is learned.
  3. STORIES    — a short, graded Jataka tale to read as connected text, one
     tappable word at a time. This is the payoff: reading actual Thai.

Two conventions, both borrowed from thai_consonants.py:

  * `paiboon` is the Paiboon romanisation, kept beside the Thai so the page and
    any future audio build script read the same romanisation.
  * A vowel shown on its own uses the dotted-circle placeholder ◌ (U+25CC) to
    stand in for "any consonant", the way Thai teaching materials print it.

⚠️  DRAFT THAI — every Thai string in the WORDS and STORIES sections below is a
first draft awaiting review by Josh and teacher Paiboon before it goes live.
The dharma content especially must be checked. Nothing here is final.
"""

# The dotted circle that stands in for "the consonant goes here" when a vowel
# is shown on its own. Printed in every Thai primer for exactly this purpose.
PLACEHOLDER = '◌'  # ◌


# ── Stage 1: syllables, grouped by where the vowel is written ──────────────
#
# Each group has a key used in the page, a human label (English + Thai teaching
# term), a one-line rule, and a few worked syllables. Every syllable spells out
# the trap: the `read_order` note says which piece you SAY first, which is not
# always the piece written first.

def _syl(thai, paiboon, english, consonant, vowel_form, note):
    return {
        'thai': thai,             # the whole syllable, e.g. 'ไป'
        'paiboon': paiboon,       # 'bpai'
        'english': english,       # 'to go'
        'consonant': consonant,   # the consonant letter, e.g. 'ป'
        'vowel_form': vowel_form, # the vowel with placeholder, e.g. 'ไ◌'
        'note': note,             # how to read it in the right order
    }


VOWEL_POSITIONS = [
    {
        'key': 'after',
        'label': 'Vowel AFTER the consonant',
        'thai_term': 'สระหลัง',
        'rule': 'The easy case: say the consonant, then the vowel, left to right.',
        'syllables': [
            _syl('มา', 'maa', 'to come', 'ม', '◌' + 'า',
                 'Say ม (m) then the า (aa): "maa". Written order = spoken order.'),
            _syl('กา', 'gaa', 'crow', 'ก', '◌' + 'า',
                 'ก (g) then า (aa): "gaa".'),
            _syl('ดำ', 'dam', 'black', 'ด', '◌' + 'ำ',
                 'ด (d) then ำ (am): "dam". ำ already includes the final m sound.'),
        ],
    },
    {
        'key': 'before',
        'label': 'Vowel BEFORE the consonant',
        'thai_term': 'สระหน้า',
        'rule': 'The vowel is written to the LEFT, but you still say the consonant first.',
        'syllables': [
            _syl('ไป', 'bpai', 'to go', 'ป', 'ไ' + '◌',
                 'You SEE ไ first, but you SAY ป (bp) first: "bpai", not "ai-bp".'),
            _syl('เธอ', 'thəə', 'you (friendly)', 'ธ', 'เ' + '◌' + 'อ',
                 'เ is written before ธ, but ธ (th) is spoken first: "thəə".'),
            _syl('โต', 'dtoo', 'big / to grow', 'ต', 'โ' + '◌',
                 'โ sits on the left; ต (dt) is still said first: "dtoo".'),
        ],
    },
    {
        'key': 'above',
        'label': 'Vowel ABOVE the consonant',
        'thai_term': 'สระบน',
        'rule': 'The vowel floats on top. Say the consonant, then the vowel.',
        'syllables': [
            _syl('กิน', 'gin', 'to eat', 'ก', '◌' + 'ิ',
                 'ก (g), then the ิ (i) sitting on top, then the น (n): "gin".'),
            _syl('ดี', 'dii', 'good', 'ด', '◌' + 'ี',
                 'ด (d) then the ี (ii) above it: "dii".'),
            _syl('มือ', 'mʉʉ', 'hand', 'ม', '◌' + 'ือ',
                 'ม (m) then the ือ (ʉʉ) above and after: "mʉʉ".'),
        ],
    },
    {
        'key': 'below',
        'label': 'Vowel BELOW the consonant',
        'thai_term': 'สระล่าง',
        'rule': 'The vowel hangs underneath. Consonant first, then the vowel.',
        'syllables': [
            _syl('หมู', 'mǔu', 'pig', 'ม', '◌' + 'ู',
                 'Read ม (m) then the ู (uu) hanging below: "mǔu". (ห is a silent tone helper.)'),
            _syl('ครู', 'khruu', 'teacher', 'ค', '◌' + 'ู',
                 'ค+ร blend then the ู (uu) below: "khruu".'),
            _syl('ดุ', 'dù', 'fierce', 'ด', '◌' + 'ุ',
                 'ด (d) then the short ุ (u) below: "dù".'),
        ],
    },
    {
        'key': 'around',
        'label': 'Vowel WRAPPING AROUND the consonant',
        'thai_term': 'สระรอบ',
        'rule': 'The trickiest case: parts of the vowel sit on BOTH sides. Read the consonant in the middle first.',
        'syllables': [
            _syl('เขา', 'kǎo', 'he / she / mountain', 'ข', 'เ' + '◌' + 'า',
                 'The vowel is เ…า wrapped around ข. Say ข (k) first: "kǎo".'),
            _syl('เมือง', 'mʉang', 'town / city', 'ม', 'เ' + '◌' + 'ือ',
                 'เ…ือ wraps around ม. Consonant in the middle first: "mʉang".'),
            _syl('เกาะ', 'gɔ̀', 'island', 'ก', 'เ' + '◌' + 'าะ',
                 'เ…าะ wraps around ก. Say ก (g) first: "gɔ̀".'),
        ],
    },
]


# ── Stage 2: dharma-themed words ───────────────────────────────────────────
#
# Real, high-frequency Buddhist vocabulary. Useful the moment it is learned,
# and it primes the reader for the story below.

def _word(thai, paiboon, english):
    return {'thai': thai, 'paiboon': paiboon, 'english': english}


DHARMA_WORDS = [
    _word('บุญ',    'bun',        'merit'),
    _word('ทาน',    'thaan',      'giving / alms'),
    _word('กรรม',   'gam',        'kamma (action & its result)'),
    _word('ธรรมะ',  'tham-má',    'the Dhamma; the teaching'),
    _word('เมตตา',  'mêet-dtaa',  'loving-kindness'),
    _word('ใจ',     'jai',        'heart / mind'),
    _word('สุข',    'sùk',        'happiness / ease'),
    _word('สงบ',    'sà-ngòp',    'peaceful / calm'),
    _word('พระ',    'phrá',       'monk / a Buddha image'),
    _word('วัด',    'wát',        'temple / monastery'),
]


# ── Stage 3: a short graded Jataka tale ────────────────────────────────────
#
# A heavily simplified retelling of the Mahākapi Jātaka (the Great Monkey), in
# which the Bodhisatta, born as a monkey king, gives his own life to save his
# troop. Kept to very short sentences so a beginner can read it one word at a
# time. Each sentence is a list of tokens {thai, paiboon, english} so the page
# can gloss any word on tap.
#
# ⚠️ DRAFT: Thai and romanisation below are a first pass for Josh + Paiboon to
# correct before this is shown to learners.

def _tok(thai, paiboon, english):
    return {'thai': thai, 'paiboon': paiboon, 'english': english}


STORIES = [
    {
        'key': 'monkey-king',
        'title_en': 'The Kind Monkey King',
        'title_th': 'ราชาลิงผู้ใจดี',
        'source': 'A simplified retelling of the Mahākapi Jātaka.',
        'moral_en': 'A true leader gives, even at the cost of self — the perfection of giving (dāna).',
        'draft': True,
        'sentences': [
            [
                _tok('นานมาแล้ว', 'naan maa láew', 'long ago'),
                _tok('มี', 'mii', 'there was'),
                _tok('ลิง', 'ling', 'a monkey'),
                _tok('ตัวหนึ่ง', 'dtua nʉ̀ng', 'one (of them)'),
            ],
            [
                _tok('ลิง', 'ling', 'the monkey'),
                _tok('อยู่', 'yùu', 'lived'),
                _tok('ใน', 'nai', 'in'),
                _tok('ป่า', 'bpàa', 'the forest'),
            ],
            [
                _tok('เขา', 'kǎo', 'he'),
                _tok('เป็น', 'bpen', 'was'),
                _tok('ราชา', 'raa-chaa', 'the king'),
                _tok('ของ', 'kɔ̌ɔng', 'of'),
                _tok('ฝูง', 'fǔung', 'the troop'),
            ],
            [
                _tok('วันหนึ่ง', 'wan nʉ̀ng', 'one day'),
                _tok('คน', 'kon', 'people'),
                _tok('มา', 'maa', 'came'),
                _tok('ล่า', 'lâa', 'to hunt'),
            ],
            [
                _tok('ราชาลิง', 'raa-chaa ling', 'the monkey king'),
                _tok('ช่วย', 'chûay', 'helped'),
                _tok('ฝูง', 'fǔung', 'the troop'),
                _tok('ของเขา', 'kɔ̌ɔng kǎo', 'of his'),
            ],
            [
                _tok('เขา', 'kǎo', 'he'),
                _tok('เสียสละ', 'sǐa-sà-là', 'sacrificed himself'),
                _tok('เพื่อ', 'phʉ̂a', 'for'),
                _tok('ฝูง', 'fǔung', 'the troop'),
            ],
        ],
    },
]


# Convenience: every distinct Thai string on the page that a recording could be
# made for. The audio build script (scripts/generate_thai_phrase_audio.py) can
# read this so the Read tab's play buttons and the generated MP3s never drift.
def all_thai_strings():
    """Every Thai string on the Read tab, de-duplicated, in reading order."""
    seen = set()
    out = []

    def add(text):
        if text and text not in seen:
            seen.add(text)
            out.append(text)

    for group in VOWEL_POSITIONS:
        for s in group['syllables']:
            add(s['thai'])
    for w in DHARMA_WORDS:
        add(w['thai'])
    for story in STORIES:
        for sentence in story['sentences']:
            for tok in sentence:
                add(tok['thai'])
    return out
