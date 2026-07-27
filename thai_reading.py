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
  3. STORIES    — short, graded tales to read as connected text, one tappable
     word at a time. This is the payoff: reading actual Thai.

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


# ── Stage 3: short graded tales ────────────────────────────────────────────
#
# Heavily simplified retellings, kept to very short sentences so a beginner can
# read them one word at a time. Each sentence is a list of tokens
# {thai, paiboon, english} so the page can gloss any word on tap.
#
# TWO SHAPES OF STORY, set by the 'format' key, because they teach two different
# stages of reading:
#
#   'tokens'   (default, no key needed) — a GRADED READER. Retold in the plainest
#              Thai that still carries the arc: one idea per sentence, 3–6 words,
#              vocabulary reused from the Words stage above. Every word is its own
#              tappable button with a gloss. This is for a learner still decoding.
#
#   'passages' — REAL THAI, unsimplified, in numbered paragraphs with the English
#              hidden underneath until tapped. No per-word glossing: at this level
#              the job is to read a whole paragraph aloud (or copy it out) and
#              only then check yourself. Carries the register a beginner text
#              cannot — ทรง, พระหัตถ์, มิได้ — which is the point.
#
# Order matters — the page shows them in this order and the first is the default,
# so they run easiest-first.
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
    {
        'key': 'matuposaka',
        'format': 'passages',
        'title_en': 'The Matuposaka Jataka — The Elephant Who Fed His Mother',
        'title_th': 'มาตุโปสกชาดก',
        'title_paiboon': 'mâa-dtù-bpoo-sà-gà chaa-dòk',
        'subtitle_th': 'ชาดกว่าด้วยพญาช้างผู้เลี้ยงดูมารดา',
        'source': 'Jataka Tale No. 455, from the Pali Canon (Khuddaka Nikaya) '
                  '— a past-life story of the Buddha.',
        'moral_en': 'Even before enlightenment, the Bodhisatta would not eat while '
                    'his blind mother went hungry.',
        'instruction': 'Read each Thai paragraph aloud, or copy it out by hand, '
                       'before you reveal the English underneath.',
        'draft': True,
        'passages': [
            {
                'number': '๑',
                'thai': 'กาลครั้งหนึ่งนานมาแล้ว ในป่าเทือกเขาหิมพานต์ '
                        'มีพญาช้างเผือกผู้งดงามตัวหนึ่ง '
                        'เป็นจ่าฝูงของช้างถึงแปดหมื่นเชือก '
                        'ช้างทุกตัวในป่านั้นเคารพยำเกรงพญาช้างเผือก '
                        'มิใช่ด้วยความกลัว แต่เพราะคุณสมบัติของพญาช้าง '
                        'คือความอดทน ความยุติธรรม '
                        'และความเอื้อเฟื้อแบ่งปันความหอมหวานทุกอย่างที่ป่าให้มา '
                        'ไม่ว่าจะเป็นผลไม้ป่า หน่ออ่อน '
                        'หรือน้ำเย็นจากแหล่งน้ำลึกที่สุด '
                        'พญาช้างมักหาสิ่งที่ดีที่สุดมาให้ผู้อื่นเสมอ '
                        'มิได้เก็บไว้เพื่อตนเอง',
                'english': 'Long ago, in the mountain forests of the Himalayas, '
                           'there lived a magnificent white elephant, leader of a '
                           'herd eighty thousand strong. Every elephant deferred '
                           'to him — not from fear, but for his patience, '
                           'fairness, and generosity in sharing the forest\'s '
                           'sweetness: wild fruit, tender shoots, the coolest '
                           'water. He always found the best of it for others, '
                           'never keeping it for himself.',
            },
            {
                'number': '๒',
                'thai': 'แต่มารดาของพญาช้าง ผู้ชราและอ่อนโยน ตาบอดมาหลายปีแล้ว '
                        'จึงไม่อาจออกหาอาหารด้วยตนเองได้อีก '
                        'ทุกวันพญาช้างจะเก็บผลไม้ที่สุกที่สุดเท่าที่หาได้ '
                        'แล้วฝากบริวารนำไปให้มารดา '
                        'คิดว่าเป็นเรื่องเล็กน้อยที่งวงช้างแปดหมื่นงวงย่อมทำได้ง่ายดาย',
                'english': 'But his mother, old and gentle, had been blind for '
                           'years and could no longer forage on her own. Each day '
                           'he gathered the ripest fruit he could find and sent it '
                           'to her with the herd — a small kindness, he thought, '
                           'easily done by eighty thousand trunks.',
            },
            {
                'number': '๓',
                'thai': 'แต่ความจริงหาได้เป็นเช่นนั้นไม่ '
                        'ทุกครั้งที่เดินทางไกลกลับมา ช้างผู้นำผลไม้ไปส่งก็หิวโหย '
                        'บอกตัวเองว่า "แค่คำเดียวคงไม่เป็นไร" '
                        'จนมาถึงถ้ำของมารดาก็ไม่เหลือผลไม้ให้เลยสักชิ้น '
                        'คืนแล้วคืนเล่า มารดาของพญาช้างจึงต้องอดอาหาร',
                'english': 'It wasn\'t that simple. Each time, the fruit-bearers '
                           'grew hungry on the long walk, told themselves "just '
                           'one bite," and arrived with nothing left. Night after '
                           'night, she went without.',
            },
            {
                'number': '๔',
                'thai': 'เมื่อพญาช้างทราบความจริงว่า '
                        'บริวารของตนแอบกินส่วนของมารดาไปเงียบๆ '
                        'โดยไม่รู้ว่านานเท่าใดแล้ว พญาช้างมิได้ประกาศตำหนิผู้ใด '
                        'ในความเงียบสงัดยามค่ำคืน ขณะที่ฝูงช้างหลับใหล '
                        'พญาช้างเพียงแต่จูงมารดาด้วยงวงหนีเข้าไปในป่าลึก '
                        'สู่ถ้ำลับใกล้ภูเขาจัณโฑรณะ '
                        'ริมทะเลสาบใสที่รายล้อมด้วยดอกบัว ที่นั่น '
                        'ห่างไกลจากผู้ช่วยเหลือแปดหมื่นตัวที่หวังดีแต่ไว้ใจไม่ได้ '
                        'พญาช้างเลี้ยงดูมารดาด้วยตนเอง ออกหาอาหารทุกวัน '
                        'นำน้ำมาด้วยปลายงวง '
                        'และไม่ไว้ใจให้ผู้ใดทำหน้าที่นี้แทนอีกเลย',
                'english': 'When he learned the truth — that his own herd had '
                           'quietly been eating his mother\'s share — he made no '
                           'accusation. In the stillness of night, he simply led '
                           'her deep into the forest, to a hidden cave near Mount '
                           'Caṇḍoraṇa beside a lotus-ringed lake. There, he cared '
                           'for her entirely himself.',
            },
            {
                'number': '๕',
                'thai': 'วันหนึ่ง ในป่าแห่งเดียวกันนั้น '
                        'พญาช้างได้ยินเสียงที่ไม่คาดคิด '
                        'เป็นเสียงมนุษย์แหบพร่าด้วยความอ่อนล้ากำลังร้องเรียก '
                        'พรานป่าคนหนึ่งจากเมืองพาราณสีหลงทางออกจากเส้นทางการค้า '
                        'และหลงอยู่ในป่ามาเจ็ดวันแล้ว '
                        'มั่นใจว่าตนคงต้องตายอยู่ที่นั่น พญาช้างคิดเพียงว่า '
                        '"มีผู้เดือดร้อนอยู่ตรงนี้ '
                        'ไม่สมควรปล่อยให้เขาต้องเป็นอันตรายในเมื่อเรายังช่วยได้" '
                        'พญาช้างจึงคุกเข่าลงต่ำ ให้ชายผู้นั้นเกาะจับ '
                        'แล้วพาเขาออกจากป่าอย่างปลอดภัยจนถึงเส้นทางกลับบ้าน',
                'english': 'One day he heard an unexpected sound: a human voice, '
                           'hoarse with exhaustion. A forester from Bārāṇasī had '
                           'been lost for seven days, certain he would die there. '
                           'The elephant thought only, "here is someone in '
                           'distress." He knelt down, let the man hold on, and '
                           'carried him safely to the road home.',
            },
            {
                'number': '๖',
                'thai': 'แต่พรานป่าหาได้ตอบแทนบุญคุณนี้ด้วยความกตัญญูไม่ '
                        'ขณะนั้นมีข่าวลือว่าพระราชาแห่งพาราณสีทรงสูญเสียช้างทรง'
                        'และกำลังเสาะหาช้างเชือกใหม่ที่สมควรแก่กษัตริย์ '
                        'ช้างเผือกที่มีขนาดและบุคลิกเช่นนี้หายากยิ่งกว่าสิ่งใดในแผ่นดิน '
                        'แทนที่จะเก็บเรื่องนี้ไว้เงียบๆ '
                        'พรานป่ากลับรีบไปเข้าเฝ้าพระราชา'
                        'และบอกตำแหน่งที่แน่ชัดของพญาช้างเผือกทันที',
                'english': 'The forester did not repay this with gratitude. '
                           'Knowing the king of Bārāṇasī sought a royal elephant, '
                           'he went straight to the palace and revealed exactly '
                           'where to find him.',
            },
            {
                'number': '๗',
                'thai': 'นายพรานของพระราชาเดินทางกลับไปยังทะเลสาบดอกบัว '
                        'และพบพญาช้างเผือกอยู่ตรงตำแหน่งที่พรานป่าบอกไว้ไม่ผิดเพี้ยน '
                        'ด้วยธรรมชาติแห่งตน พญาช้างมิได้ต่อสู้ขัดขืน '
                        'เพราะไม่เคยเป็นสัตว์ที่ใช้ความรุนแรง '
                        'และจะไม่เริ่มเป็นเช่นนั้นแม้เพื่อรักษาชีวิตตนเอง '
                        'พญาช้างยอมให้นำตัวไป '
                        'ประดับด้วยพวงมาลัยราวกับการจับกุมครั้งนี้เป็นเกียรติยศมิใช่การลักพา '
                        'จนถึงคอกช้างหลวงแห่งเมืองพาราณสี',
                'english': 'The king\'s hunters found him exactly where described. '
                           'True to his nature, he did not resist — he had never '
                           'been violent and would not start now. He was led away, '
                           'garlanded, all the way to the royal stables of '
                           'Bārāṇasī.',
            },
            {
                'number': '๘',
                'thai': 'ณ ที่นั่น พระราชาทรงนำอาหารเลิศรสที่สุดในแผ่นดินมาด้วยพระองค์เอง '
                        'ทั้งข้าวชั้นดี อ้อยหวาน น้ำจากขันเงิน '
                        'และทรงป้อนด้วยพระหัตถ์ของพระองค์เอง '
                        'แต่พญาช้างมิได้แตะต้องสิ่งใดเลย วันเวลาผ่านไป '
                        'พญาช้างซูบผอมลงเรื่อยๆ '
                        'แต่ก็ยังปฏิเสธอาหารทุกอย่างที่วางตรงหน้า',
                'english': 'There, the king himself brought the finest food in the '
                           'kingdom and offered it by hand. The elephant touched '
                           'none of it. Days passed; he grew thinner still, '
                           'refusing everything.',
            },
            {
                'number': '๙',
                'thai': 'พระราชาทรงฉงนพระทัยและซาบซึ้งในความทุกข์อันสงบและสง่างามนั้น'
                        'มากขึ้นทุกที '
                        'ในที่สุดจึงตรัสถามพญาช้างโดยตรงว่าเหตุใดจึงไม่ยอมกินอาหาร',
                'english': 'Puzzled and increasingly moved, the king finally asked '
                           'directly why he would not eat.',
            },
            {
                'number': '๑๐',
                'thai': 'พญาช้างทูลตอบว่า "หากปราศจากมารดาของข้าพเจ้าแล้ว '
                        'ข้าพเจ้าจะไม่ขอกินสิ่งใดเลย" แล้วพญาช้างจึงเล่าว่า '
                        'มารดาของตนตาบอดและอยู่เพียงลำพังในป่า '
                        'ไม่มีผู้ใดคอยนำทางหรือนำน้ำมาให้ '
                        'ทุกวันที่พญาช้างต้องอยู่ที่นี่ คือทุกวันที่มารดาต้องอดอยาก',
                'english': '"Without my mother," he answered, "I will not eat." He '
                           'explained: she was blind and alone, with no one to '
                           'guide her or bring her water.',
            },
            {
                'number': '๑๑',
                'thai': 'พระราชาทรงนิ่งอยู่กับถ้อยคำนั้นเป็นเวลานาน '
                        'พระองค์เคยเสาะหาช้างที่หายากที่สุดในแผ่นดิน'
                        'เพื่อเป็นช้างทรงและสัญลักษณ์แห่งอำนาจ '
                        'แต่บัดนี้ทรงตระหนักว่า '
                        'พระองค์เกือบจะขโมยสิ่งที่มีค่ายิ่งกว่าสัตว์หายากและงดงามไปเสียแล้ว '
                        'นั่นคือความกตัญญูอันสุดหัวใจของลูกที่มีต่อแม่ '
                        'และความรักที่แม่มีต่อลูก',
                'english': 'The king sat with this a long moment. He had sought the '
                           'rarest elephant as a symbol of power — and now '
                           'understood he had nearly stolen something far more '
                           'valuable: a son\'s total devotion to his mother.',
            },
            {
                'number': '๑๒',
                'thai': '"จงปล่อยพญาช้างเชือกนี้ไปเถิด" พระราชาตรัสในที่สุด '
                        '"ให้พญาช้างได้กลับไปหามารดาและหมู่ญาติของตน" '
                        'เมื่อพ้นจากโซ่ตรวนทุกเส้นแล้ว พญาช้างก็มุ่งหน้ากลับสู่ขุนเขา '
                        'และเมื่อถึงทะเลสาบเย็นใกล้ถ้ำของมารดา '
                        'ก็ดูดน้ำด้วยงวงพรมรดมารดาอย่างอ่อนโยน '
                        'เช่นเดียวกับที่เคยทำมาตลอด',
                'english': '"Let this elephant go," the king ordered, "back to his '
                           'mother and kin." Freed, he returned to the hills, and '
                           'at the cool lake near her cave, sprinkled her gently '
                           'with water, just as he always had.',
            },
            {
                'number': '๑๓',
                'thai': 'เรื่องเล่าสืบต่อกันมาว่า '
                        'พระราชามิได้เพียงปล่อยพญาช้างไปแล้วลืมเลือน '
                        'แต่ยังโปรดให้สร้างเมืองขึ้นใกล้ที่อยู่ของพญาช้างในป่า '
                        'และทรงถวายเกียรติแก่พญาช้างเรื่อยมานับแต่นั้น',
                'english': 'The story says the king did not simply forget him — a '
                           'town was built near his forest home, and he was '
                           'honored from then on.',
            },
        ],

        # Why the tale is scripture, not folklore. Bilingual because the Thai is
        # the point of the page and the English is the check underneath it.
        'scripture_note': {
            'heading_th': 'เหตุใดเรื่องนี้จึงอยู่ในพระไตรปิฎก',
            'heading_en': 'Why this story is Buddhist scripture',
            'thai': 'เรื่องนี้มิใช่เพียงนิทานพื้นบ้านว่าด้วยความเมตตาเท่านั้น '
                    'แต่เป็น "ชาดก" '
                    'หนึ่งในเรื่องราวปางก่อนของพระพุทธเจ้าที่ปรากฏในพระไตรปิฎก '
                    'เป็นเรื่องเล่าถึงชาติหนึ่งในอดีตของพระพุทธองค์เอง '
                    'ก่อนตรัสรู้เป็นเจ้าชายสิทธัตถะ',
            'english': 'This is a Jataka — a canonical past-life story of the '
                       'Buddha, told of one of his own former lives, long before '
                       'his final birth as Siddhattha Gotama.',
            'identifications': [
                {
                    'thai': 'พญาช้างเผือก คือ พระโพธิสัตว์ '
                            'ผู้ภายหลังจะตรัสรู้เป็นพระพุทธเจ้า',
                    'english': 'The elephant king is the Bodhisatta — the being '
                               'who would become the Buddha.',
                },
                {
                    'thai': 'พระราชาแห่งพาราณสี คือชาติก่อนหน้าของพระอานนท์ '
                            'พุทธอุปัฏฐาก',
                    'english': 'The king of Bārāṇasī is an earlier birth of '
                               'Ānanda, the Buddha\'s closest attendant.',
                },
                {
                    'thai': 'มารดาผู้ตาบอด คือชาติก่อนหน้าของพระนางมหามายา '
                            'พระราชมารดาของพระพุทธเจ้า',
                    'english': 'The blind mother is an earlier birth of '
                               'Mahāmāyā, the Buddha\'s own birth-mother.',
                },
            ],
        },

        # The virtues table, Thai term first — this page teaches the Thai.
        'virtues': [
            {
                'thai': 'เมตตา',
                'paiboon': 'mêet-dtaa',
                'english': 'compassion',
                'in_story_th': 'ช่วยเหลือพรานป่าโดยไม่หวังสิ่งตอบแทน',
                'in_story_en': 'He helps the lost forester expecting nothing '
                               'in return.',
            },
            {
                'thai': 'กตัญญู',
                'paiboon': 'gà-dtan-yuu',
                'english': 'filial devotion',
                'in_story_th': 'ละทิ้งฝูงและสถานะเพื่อดูแลมารดาด้วยตนเอง',
                'in_story_en': 'He leaves his herd and his status to care for '
                               'his mother himself.',
            },
            {
                'thai': 'อหิงสา',
                'paiboon': 'à-hǐng-sǎa',
                'english': 'non-violence',
                'in_story_th': 'ยอมถูกจับโดยไม่ทำร้ายผู้ใด',
                'in_story_en': 'He allows himself to be captured rather than '
                               'harm the king\'s men.',
            },
            {
                'thai': 'ปรีชาแห่งผู้ปกครอง',
                'paiboon': 'bprii-chaa hɛ̀ng phûu bpòk-krɔɔng',
                'english': 'wise rule',
                'in_story_th': 'พระราชาทรงรับฟังก่อนครอบครอง',
                'in_story_en': 'The king listens before he claims.',
            },
        ],

        'vocabulary': [
            _word('ช้างเผือก',      'cháang pʉ̀ak',      'white elephant'),
            _word('กตัญญู',         'gà-dtan-yuu',       'filial devotion, gratitude'),
            _word('เมตตา',          'mêet-dtaa',         'loving-kindness'),
            _word('ชาดก',           'chaa-dòk',          'Jataka, a past-life story of the Buddha'),
            _word('พระโพธิสัตว์',   'phrá-poo-thí-sàt',  'Bodhisatta, a being on the path to Buddhahood'),
            _word('ป่าหิมพานต์',    'bpàa hǐm-má-phaan', 'the Himalayan forest of Buddhist legend'),
            _word('ตาบอด',          'dtaa bɔ̀ɔt',        'blind'),
            _word('มารดา',          'maan-daa',          'mother (formal register)'),
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
        add(story.get('title_th'))
        # Token stories: every word is its own play button, so every word needs
        # a clip. Passage stories: only the teaching vocabulary and virtue terms
        # belong here — the paragraphs themselves are recorded too, but as their
        # own kind of clip via all_passage_strings() below.
        for sentence in story.get('sentences', []):
            for tok in sentence:
                add(tok['thai'])
        for virtue in story.get('virtues', []):
            add(virtue.get('thai'))
        for word in story.get('vocabulary', []):
            add(word['thai'])
    return out


def all_passage_strings():
    """The full text of every paragraph in a 'passages' story.

    Kept apart from all_thai_strings() because these are a different KIND of
    recording: a whole paragraph read straight through, tens of seconds long and
    a few hundred KB, rather than a one-second word. The build script exposes
    them as their own page so they can be regenerated on their own, and the
    player gives their buttons a stop (see data-audio-toggle in base.js) —
    nobody needs to stop a one-second word, but they do need to stop a paragraph.
    """
    seen = set()
    out = []
    for story in STORIES:
        for passage in story.get('passages', []):
            text = (passage.get('thai') or '').strip()
            if text and text not in seen:
                seen.add(text)
                out.append(text)
    return out
