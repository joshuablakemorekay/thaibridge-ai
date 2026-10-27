"""Vocabulary topics, and the cultural story that goes with some of them.

VOCABULARY drives /exercise/<topic>: the topic's word table, its quiz, the
Listening Quiz and the Learning Path's starting check. CULTURAL_STORIES hangs a
short story off a topic page.

Data only — no Flask and no imports — moved out of app.py so that any module
(a Blueprint, a script, a test) can use it without importing app.py, which
would be a circular import. app.py imports these names back unchanged.
"""

VOCABULARY = {
    'festivals': [
        {'thai': 'สงกรานต์', 'paiboon': 'sǒŋ-graan', 'english': 'Songkran (Thai New Year)', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'ลอยกระทง', 'paiboon': 'loi grà-toŋ', 'english': 'Loy Krathong Festival', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันวิสาขบูชา', 'paiboon': 'wan wí-sǎa-ká-boo-chaa', 'english': 'Visakha Bucha Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'บุญบั้งไฟ', 'paiboon': 'bun bâŋ fai', 'english': 'Rocket Festival (Isan)', 'category': 'festivals', 'formality': 'casual'},
        {'thai': 'วันขึ้นปีใหม่', 'paiboon': 'wan kʉ̂n bpii mài', 'english': "New Year's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันเข้าพรรษา', 'paiboon': 'wan kâo pan-sǎa', 'english': 'Buddhist Lent Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'วันออกพรรษา', 'paiboon': 'wan ɔ̀ɔk pan-sǎa', 'english': 'End of Buddhist Lent', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'วันมาฆบูชา', 'paiboon': 'wan maa-ká-boo-chaa', 'english': 'Makha Bucha Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'วันอาสาฬหบูชา', 'paiboon': 'wan aa-sǎan-há-boo-chaa', 'english': 'Asanha Bucha Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'ตรุษจีน', 'paiboon': 'dtrùt jiin', 'english': 'Chinese New Year', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันพ่อ', 'paiboon': 'wan pɔ̂ɔ', 'english': "Father's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันแม่', 'paiboon': 'wan mɛ̂ɛ', 'english': "Mother's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันเด็ก', 'paiboon': 'wan dèk', 'english': "Children's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันครู', 'paiboon': 'wan kruu', 'english': "Teacher's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันจักรี', 'paiboon': 'wan jàk-grii', 'english': 'Chakri Day', 'category': 'festivals', 'formality': 'royal'},
        {'thai': 'วันฉัตรมงคล', 'paiboon': 'wan chàt-moŋ-kon', 'english': 'Coronation Day', 'category': 'festivals', 'formality': 'royal'},
        {'thai': 'วันพืชมงคล', 'paiboon': 'wan pʉ̂ʉt-moŋ-kon', 'english': 'Royal Ploughing Ceremony', 'category': 'festivals', 'formality': 'royal'},
        {'thai': 'ผีตาโขน', 'paiboon': 'pǐi dtaa kǒon', 'english': 'Phi Ta Khon (masked festival, Loei)', 'category': 'festivals', 'formality': 'casual'},
        {'thai': 'เทศกาลกินเจ', 'paiboon': 'têet-sà-gaan gin jee', 'english': 'Vegetarian Festival', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'งานบุญ', 'paiboon': 'ŋaan bun', 'english': 'Merit-making ceremony', 'category': 'festivals', 'formality': 'neutral'},
    ],
    
    'isan_dialect': [
        {'thai': 'สบายดีบ่', 'paiboon': 'sà-baai dii bɔ̀ɔ', 'english': 'How are you? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'กินข้าวแล้วบ่', 'paiboon': 'gin kâao lɛ́ɛo bɔ̀ɔ', 'english': 'Have you eaten? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'แซบหลาย', 'paiboon': 'sɛ̂ɛp lǎai', 'english': 'Very delicious (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'บักหุ่ง', 'paiboon': 'bàk hùŋ', 'english': 'Papaya (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'อีหลี', 'paiboon': 'ii-lǐi', 'english': 'Really? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'บ่เป็นหยัง', 'paiboon': 'bɔ̀ɔ bpen yǎŋ', 'english': "No problem (Isan)", 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'เว้า', 'paiboon': 'wáo', 'english': 'To speak (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'ม่วน', 'paiboon': 'mûan', 'english': 'Fun (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'โตน', 'paiboon': 'dtoon', 'english': 'Waterfall (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'คัก', 'paiboon': 'kák', 'english': 'Very/really (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'แม่นบ่', 'paiboon': 'mɛ̂ɛn bɔ̀ɔ', 'english': 'Is that right? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'เฮ็ด', 'paiboon': 'hét', 'english': 'To do (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'บ่มี', 'paiboon': 'bɔ̀ɔ mii', 'english': "Don't have (Isan)", 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'อยู่ไส', 'paiboon': 'yùu sǎi', 'english': 'Where? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'ไผ', 'paiboon': 'pǎi', 'english': 'Who? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'สิ', 'paiboon': 'sì', 'english': 'Will (Isan future)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'แหน่', 'paiboon': 'nɛ̀ɛ', 'english': 'Emphasis particle (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'หมู่', 'paiboon': 'mùu', 'english': 'You all (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'เด้อ', 'paiboon': 'dəə', 'english': 'Polite particle (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'ข้อย', 'paiboon': 'kɔ̂ɔi', 'english': 'I/me (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
    ],
    
    'nature': [
        {'thai': 'ดอกบัว', 'paiboon': 'dɔ̀ɔk bua', 'english': 'Lotus flower', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ต้นโพธิ์', 'paiboon': 'dtôn poo', 'english': 'Bodhi tree', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ช้าง', 'paiboon': 'cháaŋ', 'english': 'Elephant', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'มะพร้าว', 'paiboon': 'má-práao', 'english': 'Coconut', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'น้ำตก', 'paiboon': 'nám dtòk', 'english': 'Waterfall', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ภูเขา', 'paiboon': 'puu-kǎo', 'english': 'Mountain', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'แม่น้ำ', 'paiboon': 'mɛ̂ɛ náam', 'english': 'River', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ทะเล', 'paiboon': 'tá-lee', 'english': 'Sea/Ocean', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ป่า', 'paiboon': 'bpàa', 'english': 'Forest', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ดอกไม้', 'paiboon': 'dɔ̀ɔk mái', 'english': 'Flower', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ต้นไม้', 'paiboon': 'dtôn mái', 'english': 'Tree', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'นก', 'paiboon': 'nók', 'english': 'Bird', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ปลา', 'paiboon': 'bplaa', 'english': 'Fish', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ผีเสื้อ', 'paiboon': 'pǐi sʉ̂a', 'english': 'Butterfly', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ดวงจันทร์', 'paiboon': 'duaŋ jan', 'english': 'Moon', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ดวงอาทิตย์', 'paiboon': 'duaŋ aa-tít', 'english': 'Sun', 'category': 'nature', 'formality': 'literary'},
        {'thai': 'ดาว', 'paiboon': 'daao', 'english': 'Star', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ฝน', 'paiboon': 'fǒn', 'english': 'Rain', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ลม', 'paiboon': 'lom', 'english': 'Wind', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'เมฆ', 'paiboon': 'mêek', 'english': 'Cloud', 'category': 'nature', 'formality': 'neutral'},
    ],
    
    'buddhist_formal': [
        {'thai': 'พระพุทธเจ้า', 'paiboon': 'prá-pút-tá-jâo', 'english': 'The Buddha', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'พระสงฆ์', 'paiboon': 'prá-sǒŋ', 'english': 'Buddhist monks', 'category': 'buddhist_formal', 'formality': 'monastic'},
        {'thai': 'ทำบุญ', 'paiboon': 'tam-bun', 'english': 'Make merit', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'วัด', 'paiboon': 'wát', 'english': 'Temple', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'สวดมนต์', 'paiboon': 'sùat-mon', 'english': 'Chant prayers', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'กราบ', 'paiboon': 'gràap', 'english': 'Prostrate', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'พระธรรม', 'paiboon': 'prá-tam', 'english': 'The Dhamma', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'พระไตรปิฎก', 'paiboon': 'prá-dtrai-bpì-dòk', 'english': 'Tripitaka', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'นิพพาน', 'paiboon': 'níp-paan', 'english': 'Nibbāna (Nirvana)', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'สังสารวัฏ', 'paiboon': 'sǎŋ-sǎa-rá-wát', 'english': 'Samsara', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'กรรม', 'paiboon': 'gam', 'english': 'Karma', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'ศีล', 'paiboon': 'sǐin', 'english': 'Precepts (Sila)', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'สมาธิ', 'paiboon': 'sà-maa-tí', 'english': 'Concentration (Samadhi)', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'ปัญญา', 'paiboon': 'bpan-yaa', 'english': 'Wisdom (Panna)', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'อริยสัจสี่', 'paiboon': 'à-rí-yá-sàt sìi', 'english': 'Four Noble Truths', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'มรรคมีองค์แปด', 'paiboon': 'mák mii oŋ bpɛ̀ɛt', 'english': 'Eightfold Path', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'บิณฑบาต', 'paiboon': 'bin-tá-bàat', 'english': 'Alms round', 'category': 'buddhist_formal', 'formality': 'monastic'},
        {'thai': 'อุโบสถ', 'paiboon': 'ù-boo-sòt', 'english': 'Ordination hall', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'เจดีย์', 'paiboon': 'jee-dii', 'english': 'Stupa/Pagoda', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'พระพุทธรูป', 'paiboon': 'prá-pút-tá-rûup', 'english': 'Buddha statue', 'category': 'buddhist_formal', 'formality': 'formal'},
    ],
    
    'theravada_dhamma': [
        {'thai': 'ทุกข์', 'paiboon': 'túk', 'english': 'Suffering (Dukkha)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สมุทัย', 'paiboon': 'sà-mú-tai', 'english': 'Origin of suffering', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'นิโรธ', 'paiboon': 'ní-rôot', 'english': 'Cessation (Nirodha)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'มรรค', 'paiboon': 'mák', 'english': 'Path (Magga)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'อนิจจัง', 'paiboon': 'à-nít-jaŋ', 'english': 'Impermanence (Anicca)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'อนัตตา', 'paiboon': 'à-nát-dtaa', 'english': 'Non-self (Anatta)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'ไตรลักษณ์', 'paiboon': 'dtrai-lák', 'english': 'Three Marks', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'ปฏิจจสมุปบาท', 'paiboon': 'bpà-dtìt-jà-sà-mùp-bàat', 'english': 'Dependent Origination', 'category': 'theravada_dhamma', 'formality': 'technical'},
        {'thai': 'ขันธ์ห้า', 'paiboon': 'kǎn hâa', 'english': 'Five Aggregates', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สติ', 'paiboon': 'sà-dtì', 'english': 'Mindfulness (Sati)', 'category': 'theravada_dhamma', 'formality': 'neutral'},
        {'thai': 'สัมมาทิฏฐิ', 'paiboon': 'sǎm-maa-tít-tì', 'english': 'Right View', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาสังกัปปะ', 'paiboon': 'sǎm-maa-sǎŋ-gàp-bpà', 'english': 'Right Intention', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาวาจา', 'paiboon': 'sǎm-maa-waa-jaa', 'english': 'Right Speech', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมากัมมันตะ', 'paiboon': 'sǎm-maa-gam-man-dtà', 'english': 'Right Action', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาอาชีวะ', 'paiboon': 'sǎm-maa-aa-chii-wá', 'english': 'Right Livelihood', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาวายามะ', 'paiboon': 'sǎm-maa-waa-yaa-má', 'english': 'Right Effort', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาสติ', 'paiboon': 'sǎm-maa-sà-dtì', 'english': 'Right Mindfulness', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาสมาธิ', 'paiboon': 'sǎm-maa-sà-maa-tí', 'english': 'Right Concentration', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'วิปัสสนา', 'paiboon': 'wí-bpàt-sà-naa', 'english': 'Insight (Vipassana)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'เมตตา', 'paiboon': 'mêet-dtaa', 'english': 'Loving-kindness (Metta)', 'category': 'theravada_dhamma', 'formality': 'formal'},
    ],
    
    'everyday': [
        {'thai': 'สวัสดี', 'paiboon': 'sà-wàt-dii', 'english': 'Hello/Goodbye', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ขอบคุณ', 'paiboon': 'kɔ̀ɔp-kun', 'english': 'Thank you', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ขอโทษ', 'paiboon': 'kɔ̌ɔ-tôot', 'english': 'Sorry/Excuse me', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ใช่', 'paiboon': 'châi', 'english': 'Yes', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ไม่ใช่', 'paiboon': 'mâi châi', 'english': 'No (not so)', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ไม่เป็นไร', 'paiboon': 'mâi bpen rai', 'english': "It's okay", 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เท่าไหร่', 'paiboon': 'tâo-rài', 'english': 'How much?', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'อร่อย', 'paiboon': 'à-rɔ̀i', 'english': 'Delicious', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ร้อน', 'paiboon': 'rɔ́ɔn', 'english': 'Hot', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เย็น', 'paiboon': 'yen', 'english': 'Cold/Cool', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'น้ำ', 'paiboon': 'náam', 'english': 'Water', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ข้าว', 'paiboon': 'kâao', 'english': 'Rice/Food', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'บ้าน', 'paiboon': 'bâan', 'english': 'House/Home', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'รถ', 'paiboon': 'rót', 'english': 'Car/Vehicle', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'คน', 'paiboon': 'kon', 'english': 'Person', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เงิน', 'paiboon': 'ŋəən', 'english': 'Money', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'วันนี้', 'paiboon': 'wan níi', 'english': 'Today', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'พรุ่งนี้', 'paiboon': 'prûŋ níi', 'english': 'Tomorrow', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เมื่อวาน', 'paiboon': 'mʉ̂a waan', 'english': 'Yesterday', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ตอนนี้', 'paiboon': 'dtɔɔn níi', 'english': 'Now', 'category': 'everyday', 'formality': 'neutral'},
    ],
}


# Short cultural stories, each pointing at somewhere you can practise what it
# teaches.
#
# ⚠️ `practice` is EXPLICIT on purpose. The Culture page used to build that link
# by guessing — it treated the dict key as a vocabulary category and rendered
# "/exercise/<key>". That silently broke for 'schwa_words', which is about
# loanword pronunciation and has no vocabulary category, so the link led
# straight to the 404 in the /exercise route. Saying where each story goes,
# rather than inferring it from a key that means two things at once, removes the
# whole class of bug — and lets a story point somewhere that isn't an exercise.
# `_assert_story_links_resolve()` below checks every one of these at startup.

CULTURAL_STORIES = {
    'festivals': {
        'practice': {'href': '/exercise/festivals', 'label': 'Festival vocabulary'},
        'title': 'The Legend of Loy Krathong',
        'story': '''Long ago in Sukhothai, Nang Noppamas crafted a floating vessel from banana leaves, 
decorated with flowers and candles. She set it on the water as an offering to the Water Goddess.
The King declared it an annual tradition. Today, Thai people release krathongs to let go of negativity.''',
        'lesson': 'Gratitude for nature, forgiveness, and letting go.',
    },
    'nature': {
        'practice': {'href': '/exercise/nature', 'label': 'Nature vocabulary'},
        'title': 'The Elephant and the Bodhi Tree',
        'story': '''A wise elephant found a struggling Bodhi sapling during drought. Every day he carried 
water to nourish it. Years later, when the elephant grew old, the tree provided shade and its roots 
found water for a spring. The elephant spent his final days in peace beneath the tree.''',
        'lesson': 'Kindness returns to us. All beings are interconnected.',
    },
    'buddhist_formal': {
        'practice': {'href': '/exercise/buddhist_formal',
                     'label': 'Buddhist formal vocabulary'},
        'title': 'The First Sermon at Deer Park',
        'story': '''After enlightenment, the Buddha walked to Deer Park to teach his five former companions.
He delivered the Dhammacakkappavattana Sutta, teaching the Middle Way and Four Noble Truths.
Kondanna immediately understood and became the first enlightened disciple.''',
        'lesson': 'The Middle Way, Four Noble Truths, and the Dhamma is available to all.',
    },
    'theravada_dhamma': {
        'practice': {'href': '/exercise/theravada_dhamma',
                     'label': 'Theravada Dhamma vocabulary'},
        'title': "Angulimala's Transformation",
        'story': '''Angulimala was a terrifying bandit who had killed 999 people. The Buddha intercepted him,
walking calmly though Angulimala could not catch him. "I have stopped harming beings. It is you 
who have not stopped," said the Buddha. These words pierced Angulimala's heart, and he became a monk,
eventually attaining enlightenment.''',
        'lesson': 'Transformation is possible for anyone through the power of compassion.',
    },
    'schwa_words': {
        # No vocabulary category exists for loanwords, and inventing one would
        # be inventing Thai. The story is really about the ə / əə vowels, so it
        # points at the page that actually teaches them.
        'practice': {'href': '/paiboon',
                     'label': 'The ThaiBridge Spelling guide — the ə / əə vowels'},
        'title': 'Modern Thailand and Global Connection',
        'story': '''Modern Thai has absorbed many English loanwords, especially in technology, business, and 
education. These words often use the schwa sound (ə/əə) - that "uh" sound from English. When foreign monks 
first arrived in Bangkok, they noticed shopkeepers saying "เบอร์" (bəə - number) and "เทอม" (təəm - term). 
Thai people have skillfully adapted foreign words while maintaining their own language's beauty. This shows 
Thailand's openness to the world while preserving cultural identity.''',
        'lesson': 'Language evolves through cultural exchange. Learning both traditional and modern vocabulary shows respect for Thai culture.',
    },
}
