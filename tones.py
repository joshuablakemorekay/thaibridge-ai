"""The five Thai tones and the consonant-class tone rules.

TONE_REFERENCE is the one set of real example words both the Tones page and the
ThaiBridge Spelling guide teach from. TONES_AND_CLASSES is everything on
/tones-classes, including the drills /api/drill/<kind> deals from.

Data only, moved out of app.py so other modules can use it without importing
app.py. app.py imports these names back unchanged.
"""

# The five tones, taught with ONE set of real words. Both the Tones page and the
# ThaiBridge Spelling guide read this, so they cannot drift apart again (they
# had: one said the rising tone starts "mid-low", the other "low"). The words
# are the classic kh- set — same consonant sound, same vowel, five different
# words — so the only thing that changes when you play them is the tone. The
# old examples (gaa, gàa, gâa…) were not words at all, so they had no meaning
# and nothing a Thai voice could say. High and rising are described by where
# they START, because "slightly rising" for high and "like a question" for
# rising made the two sound the same to English ears.
TONE_REFERENCE = [
    {'name': 'Mid', 'symbol': 'no mark', 'thai': 'คา', 'paiboon': 'kaa', 'english': 'to be stuck',
     'description': 'Level, in the middle of your normal speaking voice. Hold it flat.',
     'tip': 'Like a calm, flat "hmm" - one steady note.'},
    {'name': 'Low', 'symbol': 'à', 'thai': 'ข่า', 'paiboon': 'kàa', 'english': 'galangal',
     'description': 'Starts below your normal voice and stays low and level.',
     'tip': 'Like a deep, flat "oh" when you are unimpressed - drop down and stay there.'},
    {'name': 'Falling', 'symbol': 'â', 'thai': 'ค่า', 'paiboon': 'kâa', 'english': 'value, cost',
     'description': 'Starts high, then drops sharply.',
     'tip': 'Like a firm "No!" - begin up high and come straight down.'},
    {'name': 'High', 'symbol': 'á', 'thai': 'ค้า', 'paiboon': 'káa', 'english': 'to trade',
     'description': 'Starts above your normal voice and stays high, tense, often lifting a touch at the end.',
     'tip': 'Like an excited, high "Hi!" - start high and keep it up; never dip first.'},
    {'name': 'Rising', 'symbol': 'ǎ', 'thai': 'ขา', 'paiboon': 'kǎa', 'english': 'leg',
     'description': 'Starts LOW, dips a little, then climbs up high.',
     'tip': 'Like a surprised "Really?" - start low and let it climb.'},
]


# One skill that teaches consonant classes and tone rules together, because
# classes only exist to work out tones. The reference content is adapted from
# GRAMMAR['consonant_classes'] and topped up with the live/dead-syllable rules,
# the leading-ห rule, contrast pairs and the four practice drills.
# NOTE ON OBSOLETE LETTERS: ฃ (high) and ฅ (low) are shown in the reference
# chart with 'obsolete': True so the template can grey them out and the drills
# can skip them. Never include an obsolete letter as a drill question.
TONES_AND_CLASSES = {
    'core_concept': {
        'title': 'How Thai tones actually work',
        'summary': "Thai tones aren't written directly on the page. You calculate them from three things: (1) the consonant class, (2) whether the syllable is live or dead, and (3) the tone mark (if any). The consonant class is the primary factor — get that first and everything else follows.",
        'formula': 'Consonant class  +  Live / Dead syllable  +  Tone mark  =  The tone you say',
        'live_dead': "A LIVE syllable ends in a long vowel or a sonorant sound (m, n, ng, y, w). A DEAD syllable ends in a short vowel or a hard stop sound (p, t, k). Live and dead syllables follow different tone rules.",
        'shortcut': "Teaching shortcut: you only need to memorise the 20 MID + HIGH consonants. Everything else (all 24 of them) is LOW class by elimination.",
        'cant_hear': [
            "Not hearing the difference yet is normal — almost every learner starts here, and most people who call themselves tone-deaf can learn to hear speech tones with practice.",
            "You don't have to hear a tone to get it right. The spelling tells you: find the consonant class, check for a tone mark, and the chart gives you the tone. Read the word, then say the shape on purpose.",
            "Each tone name on this page has a small line showing its pitch shape — flat, low, falling, high or rising. Watch the line while you listen.",
            "Practise with pairs, not single words. Play two words one after the other (the pairs on the 'Leading ห & Pairs' tab) and listen only for which one goes up or down.",
            "Context does a lot of work. Thai people understand learners with shaky tones far more often than you'd fear.",
        ],
    },

    # Ordered MID → HIGH → LOW: mid is the most regular and is learned first.
    'classes': [
        {
            'label': 'MID',
            'name': 'Mid Class',
            'thai': 'อักษรกลาง',
            'paiboon': 'àk-sɔ̌ɔn glaaŋ',
            'colour': 'mid',
            'count': 9,
            'headline': 'Learn these first — the most regular, and the only class that can make all 5 tones.',
            'tone_rules': 'No tone mark on a live syllable = MID tone. Tone marks then give you LOW, FALLING, HIGH or RISING. The most predictable class.',
            'memory_tip': 'Just 9 letters — the small, well-behaved group. Memorise these and the 11 high-class letters, and every other letter is low by elimination.',
            'consonants': [
                {'thai': 'ก', 'paiboon': 'g', 'name': 'gɔɔ gài (chicken)'},
                {'thai': 'จ', 'paiboon': 'j', 'name': 'jɔɔ jaan (plate)'},
                {'thai': 'ฎ', 'paiboon': 'd', 'name': 'dɔɔ chá-daa (headdress)'},
                {'thai': 'ฏ', 'paiboon': 'dt', 'name': 'dtɔɔ bpà-dtàk (goad)'},
                {'thai': 'ด', 'paiboon': 'd', 'name': 'dɔɔ dèk (child)'},
                {'thai': 'ต', 'paiboon': 'dt', 'name': 'dtɔɔ dtào (turtle)'},
                {'thai': 'บ', 'paiboon': 'b', 'name': 'bɔɔ bai-mái (leaf)'},
                {'thai': 'ป', 'paiboon': 'bp', 'name': 'bpɔɔ bplaa (fish)'},
                {'thai': 'อ', 'paiboon': 'ʔ', 'name': 'ʔɔɔ àaŋ (basin)'},
            ],
            'examples': [
                {'thai': 'ปา', 'paiboon': 'bpaa', 'tone': 'Mid', 'english': 'throw'},
                {'thai': 'ป่า', 'paiboon': 'bpàa', 'tone': 'Low', 'english': 'forest'},
                {'thai': 'ป้า', 'paiboon': 'bpâa', 'tone': 'Falling', 'english': 'aunt'},
                {'thai': 'ป๊า', 'paiboon': 'bpáa', 'tone': 'High', 'english': 'papa'},
            ],
        },
        {
            'label': 'HIGH',
            'name': 'High Class',
            'thai': 'อักษรสูง',
            'paiboon': 'àk-sɔ̌ɔn sǔuŋ',
            'colour': 'high',
            'count': 11,
            'headline': 'No tone mark = RISING tone. Only 3 possible tones.',
            'tone_rules': 'No tone mark on a live syllable = RISING tone. Tone marks give you only LOW or FALLING. High class can never make a high tone by itself.',
            'memory_tip': 'Mostly the breathy / aspirated sounds. ฃ is obsolete — you will never meet it in real writing.',
            'consonants': [
                {'thai': 'ข', 'paiboon': 'k', 'name': 'kɔɔ kài (egg)'},
                {'thai': 'ฃ', 'paiboon': 'k', 'name': 'kɔɔ kùat (bottle)', 'obsolete': True},
                {'thai': 'ฉ', 'paiboon': 'ch', 'name': 'chɔɔ chǐŋ (cymbal)'},
                {'thai': 'ฐ', 'paiboon': 't', 'name': 'tɔɔ tǎan (base)'},
                {'thai': 'ถ', 'paiboon': 't', 'name': 'tɔɔ tǔŋ (bag)'},
                {'thai': 'ผ', 'paiboon': 'p', 'name': 'pɔɔ pʉ̌ŋ (bee)'},
                {'thai': 'ฝ', 'paiboon': 'f', 'name': 'fɔɔ fǎa (lid)'},
                {'thai': 'ศ', 'paiboon': 's', 'name': 'sɔɔ sǎa-laa (pavilion)'},
                {'thai': 'ษ', 'paiboon': 's', 'name': 'sɔɔ rʉʉ-sǐi (hermit)'},
                {'thai': 'ส', 'paiboon': 's', 'name': 'sɔɔ sʉ̌a (tiger)'},
                {'thai': 'ห', 'paiboon': 'h', 'name': 'hɔɔ hìip (chest)'},
            ],
            'examples': [
                {'thai': 'ขา', 'paiboon': 'kǎa', 'tone': 'Rising', 'english': 'leg'},
                {'thai': 'ข่า', 'paiboon': 'kàa', 'tone': 'Low', 'english': 'galangal'},
                {'thai': 'ข้า', 'paiboon': 'kâa', 'tone': 'Falling', 'english': 'I (archaic)'},
                {'thai': 'สอง', 'paiboon': 'sɔ̌ɔŋ', 'tone': 'Rising', 'english': 'two'},
            ],
        },
        {
            'label': 'LOW',
            'name': 'Low Class',
            'thai': 'อักษรต่ำ',
            'paiboon': 'àk-sɔ̌ɔn dtàm',
            'colour': 'low',
            'count': 24,
            'headline': '⚠️ The tone marks act DIFFERENTLY here — this is the most common learner error.',
            'tone_rules': "No tone mark on a live syllable = MID tone. But watch the marks: ไม้เอก ( ่ ) gives FALLING (not low!) and ไม้โท ( ้ ) gives HIGH. That is the opposite of what beginners expect.",
            'memory_tip': 'The big group (24 letters). You do not memorise it — anything that is not one of the 20 mid/high letters is low. 14 come in high/low pairs; 10 are single sounds (the sonorants ง ญ ณ น ม ย ร ล ว ฬ).',
            'consonants': [
                # Paired (14) — share a sound with a high-class partner
                {'thai': 'ค', 'paiboon': 'k', 'name': 'kɔɔ kwaai (buffalo)', 'group': 'paired'},
                {'thai': 'ฅ', 'paiboon': 'k', 'name': 'kɔɔ kon (person)', 'group': 'paired', 'obsolete': True},
                {'thai': 'ฆ', 'paiboon': 'k', 'name': 'kɔɔ rá-kaŋ (bell)', 'group': 'paired'},
                {'thai': 'ช', 'paiboon': 'ch', 'name': 'chɔɔ cháaŋ (elephant)', 'group': 'paired'},
                {'thai': 'ซ', 'paiboon': 's', 'name': 'sɔɔ sôo (chain)', 'group': 'paired'},
                {'thai': 'ฌ', 'paiboon': 'ch', 'name': 'chɔɔ chəə (tree)', 'group': 'paired'},
                {'thai': 'ฑ', 'paiboon': 't', 'name': 'tɔɔ mon-too (Montho)', 'group': 'paired'},
                {'thai': 'ฒ', 'paiboon': 't', 'name': 'tɔɔ pûu-tâo (old man)', 'group': 'paired'},
                {'thai': 'ท', 'paiboon': 't', 'name': 'tɔɔ tá-hǎan (soldier)', 'group': 'paired'},
                {'thai': 'ธ', 'paiboon': 't', 'name': 'tɔɔ toŋ (flag)', 'group': 'paired'},
                {'thai': 'พ', 'paiboon': 'p', 'name': 'pɔɔ paan (tray)', 'group': 'paired'},
                {'thai': 'ฟ', 'paiboon': 'f', 'name': 'fɔɔ fan (teeth)', 'group': 'paired'},
                {'thai': 'ภ', 'paiboon': 'p', 'name': 'pɔɔ sǎm-phao (sailboat)', 'group': 'paired'},
                {'thai': 'ฮ', 'paiboon': 'h', 'name': 'hɔɔ nók-hûuk (owl)', 'group': 'paired'},
                # Single (10) — the sonorants, no high-class partner
                {'thai': 'ง', 'paiboon': 'ŋ', 'name': 'ŋɔɔ ŋuu (snake)', 'group': 'single'},
                {'thai': 'ญ', 'paiboon': 'y', 'name': 'yɔɔ yǐŋ (woman)', 'group': 'single'},
                {'thai': 'ณ', 'paiboon': 'n', 'name': 'nɔɔ neen (novice)', 'group': 'single'},
                {'thai': 'น', 'paiboon': 'n', 'name': 'nɔɔ nǔu (mouse)', 'group': 'single'},
                {'thai': 'ม', 'paiboon': 'm', 'name': 'mɔɔ máa (horse)', 'group': 'single'},
                {'thai': 'ย', 'paiboon': 'y', 'name': 'yɔɔ yák (giant)', 'group': 'single'},
                {'thai': 'ร', 'paiboon': 'r', 'name': 'rɔɔ rʉa (boat)', 'group': 'single'},
                {'thai': 'ล', 'paiboon': 'l', 'name': 'lɔɔ liŋ (monkey)', 'group': 'single'},
                {'thai': 'ว', 'paiboon': 'w', 'name': 'wɔɔ wɛɛn (ring)', 'group': 'single'},
                {'thai': 'ฬ', 'paiboon': 'l', 'name': 'lɔɔ jù-laa (kite)', 'group': 'single'},
            ],
            'examples': [
                {'thai': 'คา', 'paiboon': 'kaa', 'tone': 'Mid', 'english': 'stuck'},
                {'thai': 'ค่า', 'paiboon': 'kâa', 'tone': 'Falling', 'english': 'value'},
                {'thai': 'ค้า', 'paiboon': 'káa', 'tone': 'High', 'english': 'trade'},
                {'thai': 'ช้าง', 'paiboon': 'cháaŋ', 'tone': 'High', 'english': 'elephant'},
            ],
        },
    ],

    # Same-sound pairs: consonants that sound identical but sit in different
    # classes, so the very same syllable comes out as a different tone. This is
    # the clearest proof that the CLASS — not the letter's sound — drives the tone.
    'sound_pairs': {
        'title': 'Same sound, different class → different tone',
        'note': "Several consonants sound identical but live in different classes. With no tone mark, the HIGH-class letter gives a RISING tone while its LOW-class twin gives a MID tone — same sound, different tone, just because of the class.",
        'demo': {
            'high': {'thai': 'ขา', 'paiboon': 'kǎa', 'tone': 'Rising', 'english': 'leg'},
            'low':  {'thai': 'คา', 'paiboon': 'kaa', 'tone': 'Mid', 'english': 'stuck'},
        },
        'pairs': [
            {'sound': 'k',  'high': 'ข', 'low': 'ค'},
            {'sound': 'ch', 'high': 'ฉ', 'low': 'ช'},
            {'sound': 't',  'high': 'ถ', 'low': 'ท'},
            {'sound': 'p',  'high': 'ผ', 'low': 'พ'},
            {'sound': 'f',  'high': 'ฝ', 'low': 'ฟ'},
            {'sound': 's',  'high': 'ส', 'low': 'ซ'},
            {'sound': 'h',  'high': 'ห', 'low': 'ฮ'},
        ],
    },

    # How to actually get good at this — the study plan and elimination tricks
    # that used to live in the Grammar page's consonant-class section.
    'mastery': {
        'title': 'How to master this',
        'steps': [
            'Memorise the 9 MID consonants first — the smallest and most regular group.',
            'Learn the 11 HIGH consonants (mostly the breathy, aspirated sounds).',
            'Everything left over is LOW class (24 letters) — you get it by elimination.',
            'Practise on real words so you recognise the patterns instead of reciting them.',
            'Run the drills below until the tone comes out automatically.',
        ],
        'mnemonic': 'MID = ก จ ฎ ฏ ด ต บ ป อ (just 9 — make a silly sentence to lock them in). HIGH = the breathy group. LOW = everything else.',
        'sonorant_tip': 'The flowing sounds — ง ญ ณ น ม ย ร ล ว ฬ — are ALL low class. No nasal or flowing sound is ever mid or high, so that is an instant way to rule classes out.',
    },

    # LIVE-syllable tone chart. Columns are the five mark states; rows are the
    # three classes. A dash means that combination is not used.
    'tone_chart_live': {
        'title': 'Live-syllable tone chart',
        'note': "Read across: pick the class row, then the tone mark column. Notice how the LOW row breaks the pattern — that mismatch is where most reading mistakes come from.",
        'columns': ['No mark', 'ไม้เอก  ่', 'ไม้โท  ้', 'ไม้ตรี  ๊', 'ไม้จัตวา  ๋'],
        'rows': [
            {'label': 'MID', 'colour': 'mid', 'tones': ['Mid', 'Low', 'Falling', 'High', 'Rising']},
            {'label': 'HIGH', 'colour': 'high', 'tones': ['Rising', 'Low', 'Falling', '–', '–']},
            {'label': 'LOW', 'colour': 'low', 'tones': ['Mid', 'Falling', 'High', '–', '–']},
        ],
    },

    'dead_syllables': {
        'title': 'Dead syllables (short vowel or a p / t / k stop ending)',
        'rules': [
            {'classes': 'MID & HIGH class', 'result': 'LOW tone', 'example': {'thai': 'จะ', 'paiboon': 'jà', 'english': 'will (short vowel = dead)'}},
            {'classes': 'LOW class, SHORT vowel', 'result': 'HIGH tone', 'example': {'thai': 'คะ', 'paiboon': 'ká', 'english': 'yes/polite (female)'}},
            {'classes': 'LOW class, LONG vowel', 'result': 'FALLING tone', 'example': {'thai': 'มาก', 'paiboon': 'mâak', 'english': 'a lot / very'}},
        ],
    },

    'leading_h': {
        'title': 'The silent leading ห',
        'rule': "Put a silent ห in front of a single low-class consonant (the sonorants ง ญ น ม ย ร ล ว) and that consonant now follows HIGH-class rules. The ห is not pronounced — it only changes the tone.",
        'pairs': [
            {'plain': {'thai': 'มา', 'paiboon': 'maa', 'tone': 'Mid', 'english': 'come'},
             'led':   {'thai': 'หมา', 'paiboon': 'mǎa', 'tone': 'Rising', 'english': 'dog'}},
            {'plain': {'thai': 'นา', 'paiboon': 'naa', 'tone': 'Mid', 'english': 'rice field'},
             'led':   {'thai': 'หนา', 'paiboon': 'nǎa', 'tone': 'Rising', 'english': 'thick'}},
        ],
    },

    'contrast_pairs': {
        'title': 'Minimal pairs — where the class changes the tone',
        'note': 'Same-ish spelling, different consonant class, completely different tone and meaning. This is why the class matters.',
        'pairs': [
            {'a': {'thai': 'คา', 'paiboon': 'kaa', 'class': 'LOW', 'mark': 'none', 'tone': 'Mid', 'english': 'stuck'},
             'b': {'thai': 'ข่า', 'paiboon': 'kàa', 'class': 'HIGH', 'mark': 'ไม้เอก ่', 'tone': 'Low', 'english': 'galangal'}},
            {'a': {'thai': 'มา', 'paiboon': 'maa', 'class': 'LOW', 'mark': 'none', 'tone': 'Mid', 'english': 'come'},
             'b': {'thai': 'หมา', 'paiboon': 'mǎa', 'class': 'HIGH (via leading ห)', 'mark': 'none', 'tone': 'Rising', 'english': 'dog'}},
            {'a': {'thai': 'กา', 'paiboon': 'gaa', 'class': 'MID', 'mark': 'none', 'tone': 'Mid', 'english': 'crow'},
             'b': {'thai': 'ไก่', 'paiboon': 'gài', 'class': 'MID', 'mark': 'ไม้เอก ่', 'tone': 'Low', 'english': 'chicken'}},
        ],
    },

    'reference_tones': TONE_REFERENCE,
    'tone_marks': [
        {'thai': ' ่', 'name': 'ไม้เอก (mai ek)', 'effect': 'Mid/High → low · Low → falling'},
        {'thai': ' ้', 'name': 'ไม้โท (mai tho)', 'effect': 'Mid/High → falling · Low → high'},
        {'thai': ' ๊', 'name': 'ไม้ตรี (mai tri)', 'effect': 'Mid class → high (rare)'},
        {'thai': ' ๋', 'name': 'ไม้จัตวา (mai jattawa)', 'effect': 'Mid class → rising (rare)'},
    ],

    # ── Practice drill pools (consumed by the template's JS) ──────────────
    # Drill 1 (class ID) is built in the template from the 'classes' lists,
    # skipping obsolete letters. Drills 2–4 use these explicit pools. Every
    # question's 'tone' is the correct answer sent to /api/check_answer.
    'drills': {
        # Drill 2 — read a syllable, pick the resulting tone. 'level' drives the
        # progression: 1 = mid class only, 2 = high, 3 = low, then mixed.
        'tone_calc': [
            {'thai': 'ปา', 'tone': 'Mid', 'class': 'MID', 'level': 1, 'english': 'throw'},
            {'thai': 'ป่า', 'tone': 'Low', 'class': 'MID', 'level': 1, 'english': 'forest'},
            {'thai': 'ป้า', 'tone': 'Falling', 'class': 'MID', 'level': 1, 'english': 'aunt'},
            {'thai': 'กา', 'tone': 'Mid', 'class': 'MID', 'level': 1, 'english': 'crow'},
            {'thai': 'ไก่', 'tone': 'Low', 'class': 'MID', 'level': 1, 'english': 'chicken'},
            {'thai': 'ขา', 'tone': 'Rising', 'class': 'HIGH', 'level': 2, 'english': 'leg'},
            {'thai': 'ข่า', 'tone': 'Low', 'class': 'HIGH', 'level': 2, 'english': 'galangal'},
            {'thai': 'ข้า', 'tone': 'Falling', 'class': 'HIGH', 'level': 2, 'english': 'I (archaic)'},
            {'thai': 'สอง', 'tone': 'Rising', 'class': 'HIGH', 'level': 2, 'english': 'two'},
            {'thai': 'คา', 'tone': 'Mid', 'class': 'LOW', 'level': 3, 'english': 'stuck'},
            {'thai': 'ค่า', 'tone': 'Falling', 'class': 'LOW', 'level': 3, 'english': 'value'},
            {'thai': 'ค้า', 'tone': 'High', 'class': 'LOW', 'level': 3, 'english': 'trade'},
            {'thai': 'มา', 'tone': 'Mid', 'class': 'LOW', 'level': 3, 'english': 'come'},
        ],
        # Drill 3 — contrast pairs: show one member, pick its tone.
        'contrast': [
            {'thai': 'คา', 'tone': 'Mid', 'english': 'stuck (low class, no mark)'},
            {'thai': 'ข่า', 'tone': 'Low', 'english': 'galangal (high class + ไม้เอก)'},
            {'thai': 'กา', 'tone': 'Mid', 'english': 'crow (mid class, no mark)'},
            {'thai': 'ไก่', 'tone': 'Low', 'english': 'chicken (mid class + ไม้เอก)'},
        ],
        # Drill 4 — leading ห: pick the tone. Rising means the ห did its job.
        'leading_h': [
            {'thai': 'หมา', 'tone': 'Rising', 'english': 'dog (ห + ม)'},
            {'thai': 'มา', 'tone': 'Mid', 'english': 'come (plain ม)'},
            {'thai': 'หนา', 'tone': 'Rising', 'english': 'thick (ห + น)'},
            {'thai': 'นา', 'tone': 'Mid', 'english': 'rice field (plain น)'},
            {'thai': 'หญิง', 'tone': 'Rising', 'english': 'woman (ห + ญ)'},
        ],
    },
}
