"""Politeness registers for the Sentences page.

The Sentences page teaches one line per situation, and every one of them is
written in the polite register — full pronoun, ครับ/ค่ะ on the end. That is the
right *first* thing to learn, but it is not how most Thai is actually spoken,
and a learner who only ever hears it sounds like a textbook.

This module hangs one or two extra rungs off each of those lines:

    Formal   ผมขอข้าวผัดหนึ่งจานครับ   pronoun + ครับ/ค่ะ
    Neutral  ขอข้าวผัดจานนึงครับ       pronoun dropped, particle kept
    Casual   ข้าวผัดจานนึง             particle dropped too

The single test for which rung you are on is: is ครับ/ค่ะ still there? Yes is
neutral, no is casual. Neutral is where most real speech lives and is safe with
anybody, which is why it is worth learning hardest. Casual is not rude — rude is
a further step (กู/มึง) this app deliberately does not teach — but it only ever
goes sideways or downwards: to friends your own age, to siblings, to children.
Never upward to a stranger, to staff, or to anyone senior.

Monastic is NOT a rung on that ladder. It swaps the vocabulary rather than the
ending (ถวาย not ให้, นิมนต์ not ชวน, อาตมา and โยม for the pronouns), and it
already sits at the formal end by definition. So the two dialogues with a monk in
them get a monastic note in the third slot instead of a casual form, because a
casual form there would be modelling the one thing you must not do.

Keyed by the exact formal Thai string so that nothing in app.py has to change and
a reviewer can diff this file on its own. Every Thai string here is a DRAFT and
has not yet been checked by a native speaker.
"""

# A line where the neutral rung is identical to the formal one — usually because
# there was no pronoun to drop in the first place.
SAME = {'same': True}

LEVELS = {
    # 'formal' is not a rung the module generates — it is the label for the main
    # line already on the page. It lives here so the template's Formal chip takes
    # its wording and colour from the same place as the rungs below it. ORDER
    # does not include it, so nothing here renders an extra row.
    'formal': {
        'label': 'Formal',
        'thai_name': 'ภาษาสุภาพ',
        'colour': '#4B0082',
        'blurb': 'Full pronoun, ครับ/ค่ะ on the end. This is the main line.',
    },
    'neutral': {
        'label': 'Neutral',
        'thai_name': 'ภาษาทั่วไป',
        'colour': '#228B22',
        'blurb': 'Pronoun dropped, ครับ/ค่ะ kept. Safe with anyone.',
    },
    'casual': {
        'label': 'Casual',
        'thai_name': 'ภาษาพูด',
        'colour': '#FF8C00',
        'blurb': 'Particle dropped too. Friends, siblings, people you know well.',
    },
    'monastic': {
        'label': 'Monastic',
        'thai_name': 'ภาษาพระสงฆ์',
        'colour': '#FF9933',
        'blurb': 'A different vocabulary, not a lower rung. No casual form exists.',
    },
}


VARIANTS = {

    # ---------------------------------------------------------------
    # At a Restaurant
    # ---------------------------------------------------------------
    'สวัสดีครับ รับอะไรดีครับ': {
        'neutral': {'thai': 'รับอะไรดีครับ', 'paiboon': 'ráp à-rai dii kráp',
                    'note': 'Greeting dropped — staff usually go straight to the question.'},
        'casual': {'thai': 'เอาอะไรดี', 'paiboon': 'ao à-rai dii',
                   'note': 'เอา instead of รับ. A stall you eat at every week.'},
    },
    'ผมขอข้าวผัดหนึ่งจานครับ': {
        'neutral': {'thai': 'ขอข้าวผัดจานนึงครับ', 'paiboon': 'kɔ̌ɔ kâao pàt jaan nʉ̀ŋ kráp',
                    'note': 'Pronoun gone, and spoken Thai says จานนึง — classifier first, '
                            'นึง instead of หนึ่ง. This is what you will actually hear.'},
        'casual': {'thai': 'ข้าวผัดจานนึง', 'paiboon': 'kâao pàt jaan nʉ̀ŋ',
                   'note': 'No verb, no particle — just the order. Fine at a food stall.'},
    },
    'ดิฉันขอส้มตำค่ะ': {
        'neutral': {'thai': 'ขอส้มตำค่ะ', 'paiboon': 'kɔ̌ɔ sôm-tam kâ',
                    'note': 'ดิฉัน is quite formal for everyday use — most women drop it.'},
        'casual': {'thai': 'ส้มตำจานนึง', 'paiboon': 'sôm-tam jaan nʉ̀ŋ',
                   'note': 'Naming the dish and the quantity is a complete order.'},
    },
    'เผ็ดไหมครับ': {
        'neutral': SAME,
        'casual': {'thai': 'เผ็ดไหม', 'paiboon': 'pèt mǎi',
                   'note': 'Just the particle off.'},
    },
    'ไม่เผ็ดค่ะ': {
        'neutral': SAME,
        'casual': {'thai': 'ไม่เผ็ดนะ', 'paiboon': 'mâi pèt ná',
                   'note': 'นะ softens it so the bare answer does not sound curt.'},
    },
    'รับน้ำอะไรครับ': {
        'neutral': SAME,
        'casual': {'thai': 'เอาน้ำอะไร', 'paiboon': 'ao náam à-rai'},
    },
    'เอาน้ำเปล่าครับ': {
        'neutral': SAME,
        'casual': {'thai': 'น้ำเปล่า', 'paiboon': 'náam bplào',
                   'note': 'Naming the drink is enough.'},
    },

    # ---------------------------------------------------------------
    # Meeting Someone
    # ---------------------------------------------------------------
    'สวัสดีครับ ผมชื่อจอห์น': {
        'neutral': {'thai': 'สวัสดีครับ ผมจอห์นครับ', 'paiboon': 'sà-wàt-dii kráp, pǒm John kráp',
                    'note': 'ชื่อ dropped — "I\'m John" rather than "my name is John".'},
        'casual': {'thai': 'หวัดดี ผมจอห์น', 'paiboon': 'wàt-dii, pǒm John',
                   'note': 'หวัดดี is the clipped spoken form of สวัสดี.'},
        'warn': 'Only use the casual form with someone your own age in a relaxed setting. '
                'Meeting someone senior, keep the formal line.',
    },
    'สวัสดีค่ะ ดิฉันชื่อนิดา ยินดีที่ได้รู้จักค่ะ': {
        'neutral': {'thai': 'สวัสดีค่ะ ชื่อนิดาค่ะ ยินดีที่ได้รู้จักนะคะ',
                    'paiboon': 'sà-wàt-dii kâ, chûu Nida kâ, yin-dii tîi dâi rúu-jàk ná ká',
                    'note': 'Pronoun dropped; นะ before คะ makes it warmer.'},
        'casual': {'thai': 'หวัดดี เราชื่อนิดา ยินดีที่ได้รู้จักนะ',
                   'paiboon': 'wàt-dii, rao chûu Nida, yin-dii tîi dâi rúu-jàk ná',
                   'note': 'เรา is the friendly "I" a lot of women use with people their own age.'},
    },
    'ยินดีที่ได้รู้จักเช่นกันครับ คุณมาจากไหนครับ': {
        'neutral': {'thai': 'ยินดีเช่นกันครับ มาจากไหนครับ',
                    'paiboon': 'yin-dii chên-gan kráp, maa jàak nǎi kráp',
                    'note': 'Both the long phrase and คุณ trimmed.'},
        'casual': {'thai': 'ยินดีเหมือนกัน มาจากไหน', 'paiboon': 'yin-dii mʉ̌an gan, maa jàak nǎi',
                   'note': 'เหมือนกัน is the everyday word where เช่นกัน is the written one.'},
    },
    'ดิฉันมาจากกรุงเทพค่ะ แล้วคุณล่ะคะ': {
        'neutral': {'thai': 'มาจากกรุงเทพค่ะ แล้วคุณล่ะคะ',
                    'paiboon': 'maa jàak gruŋ-têep kâ, lɛ́ɛo kun lâ ká'},
        'casual': {'thai': 'มาจากกรุงเทพ แล้วเธอล่ะ', 'paiboon': 'maa jàak gruŋ-têep, lɛ́ɛo təə lâ',
                   'note': 'เธอ replaces คุณ between friends.'},
    },
    'ผมมาจากอเมริกาครับ': {
        'neutral': {'thai': 'มาจากอเมริกาครับ', 'paiboon': 'maa jàak à-mee-rí-gaa kráp'},
        'casual': {'thai': 'มาจากอเมริกา', 'paiboon': 'maa jàak à-mee-rí-gaa'},
    },
    'คุณพูดไทยเก่งมากเลยค่ะ': {
        'neutral': {'thai': 'พูดไทยเก่งมากเลยค่ะ', 'paiboon': 'pûut tai gèŋ mâak ləəi kâ'},
        'casual': {'thai': 'พูดไทยเก่งจัง', 'paiboon': 'pûut tai gèŋ jaŋ',
                   'note': 'จัง is the casual "so…!" particle — admiring rather than measured.'},
    },
    'ขอบคุณครับ ผมกำลังเรียนอยู่ครับ': {
        'neutral': {'thai': 'ขอบคุณครับ กำลังเรียนอยู่ครับ',
                    'paiboon': 'kɔ̀ɔp-kun kráp, gam-laŋ riian yùu kráp'},
        'casual': {'thai': 'ขอบใจ ยังเรียนอยู่', 'paiboon': 'kɔ̀ɔp-jai, yaŋ riian yùu',
                   'note': 'ขอบใจ is thanks to a friend or someone younger — never upward.'},
    },

    # ---------------------------------------------------------------
    # Shopping
    # ---------------------------------------------------------------
    'ขอดูเสื้อตัวนี้หน่อยค่ะ': {
        'neutral': SAME,
        'casual': {'thai': 'ขอดูตัวนี้หน่อย', 'paiboon': 'kɔ̌ɔ duu dtuua níi nɔ̀ɔi',
                   'note': 'เสื้อ dropped — the classifier ตัว already tells them it is clothing.'},
    },
    'ได้ครับ ขนาดอะไรครับ': {
        'neutral': {'thai': 'ได้ครับ ไซส์อะไรครับ', 'paiboon': 'dâi kráp, sái à-rai kráp',
                    'note': 'Shops say ไซส์ (from English "size"), not ขนาด.'},
        'casual': {'thai': 'ได้ ไซส์อะไร', 'paiboon': 'dâi, sái à-rai'},
    },
    'ขนาดเอ็มค่ะ ราคาเท่าไหร่คะ': {
        'neutral': {'thai': 'ไซส์เอ็มค่ะ เท่าไหร่คะ', 'paiboon': 'sái M kâ, tâo-rài ká',
                    'note': 'ราคา is understood — nobody says it out loud.'},
        'casual': {'thai': 'ไซส์เอ็ม เท่าไหร่', 'paiboon': 'sái M, tâo-rài'},
    },
    'สามร้อยบาทครับ': {
        'neutral': SAME,
        'casual': {'thai': 'สามร้อย', 'paiboon': 'sǎam rɔ́ɔi',
                   'note': 'บาท is dropped constantly — the currency is obvious.'},
    },
    'แพงไปหน่อยค่ะ ลดได้ไหมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'แพงจัง ลดได้ไหม', 'paiboon': 'pɛɛŋ jaŋ, lót dâi mǎi'},
    },
    'ลดให้สองร้อยห้าสิบบาทครับ': {
        'neutral': {'thai': 'ลดให้สองร้อยห้าสิบครับ', 'paiboon': 'lót hâi sɔ̌ɔŋ rɔ́ɔi hâa-sìp kráp'},
        'casual': {'thai': 'สองร้อยห้าสิบ', 'paiboon': 'sɔ̌ɔŋ rɔ́ɔi hâa-sìp',
                   'note': 'Just naming the new number is a complete counter-offer.'},
    },
    'โอเคค่ะ เอาค่ะ': {
        'neutral': SAME,
        'casual': {'thai': 'โอเค เอา', 'paiboon': 'oo-kee, ao'},
    },

    # ---------------------------------------------------------------
    # Asking for Directions
    # ---------------------------------------------------------------
    'ขอโทษครับ วัดพระแก้วอยู่ที่ไหนครับ': {
        'neutral': {'thai': 'ขอโทษครับ วัดพระแก้วอยู่ไหนครับ',
                    'paiboon': 'kɔ̌ɔ-tôot kráp, wát prá-gɛ̂ɛo yùu nǎi kráp',
                    'note': 'ที่ drops out of อยู่ที่ไหน in speech almost every time.'},
        'casual': {'thai': 'วัดพระแก้วอยู่ไหน', 'paiboon': 'wát prá-gɛ̂ɛo yùu nǎi'},
        'warn': 'Stopping a stranger in the street is exactly when you keep ครับ/ค่ะ. '
                'Save the casual form for asking a friend.',
    },
    'ตรงไปแล้วเลี้ยวซ้ายครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ตรงไปแล้วเลี้ยวซ้าย', 'paiboon': 'dtroŋ bpai lɛ́ɛo líao sáai'},
    },
    'ไกลไหมครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ไกลไหม', 'paiboon': 'glai mǎi'},
    },
    'ไม่ไกลครับ เดินประมาณสิบนาทีครับ': {
        'neutral': {'thai': 'ไม่ไกลครับ เดินสิบนาทีครับ',
                    'paiboon': 'mâi glai kráp, dəən sìp naa-tii kráp',
                    'note': 'ประมาณ is often left out — the number is understood as rough.'},
        'casual': {'thai': 'ไม่ไกล เดินสิบนาที', 'paiboon': 'mâi glai, dəən sìp naa-tii'},
    },
    'ขอบคุณมากครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ขอบใจนะ', 'paiboon': 'kɔ̀ɔp-jai ná',
                   'note': 'Only sideways or downwards — never to someone older who helped you.'},
    },
    'ไม่เป็นไรครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ไม่เป็นไร', 'paiboon': 'mâi bpen rai'},
    },

    # ---------------------------------------------------------------
    # Daily Routine
    # ---------------------------------------------------------------
    'เช้านี้คุณทำอะไรครับ': {
        'neutral': {'thai': 'เช้านี้ทำอะไรครับ', 'paiboon': 'cháao níi tam à-rai kráp',
                    'note': 'คุณ is usually unnecessary once you are already talking to them.'},
        'casual': {'thai': 'เช้านี้ทำอะไร', 'paiboon': 'cháao níi tam à-rai'},
    },
    'ดิฉันไปออกกำลังกายค่ะ แล้วคุณล่ะคะ': {
        'neutral': {'thai': 'ไปออกกำลังกายมาค่ะ แล้วคุณล่ะคะ',
                    'paiboon': 'bpai ɔ̀ɔk gam-laŋ gaai maa kâ, lɛ́ɛo kun lâ ká',
                    'note': 'มา on the end marks "been and come back" — very common in speech.'},
        'casual': {'thai': 'ไปออกกำลังกายมา แล้วเธอล่ะ',
                   'paiboon': 'bpai ɔ̀ɔk gam-laŋ gaai maa, lɛ́ɛo təə lâ'},
    },
    'ผมยังไม่ได้ไปครับ ผมกำลังจะไปตอนเย็นครับ': {
        'neutral': {'thai': 'ยังไม่ได้ไปครับ จะไปตอนเย็นครับ',
                    'paiboon': 'yaŋ mâi dâi bpai kráp, jà bpai dtɔɔn yen kráp',
                    'note': 'The second ผม goes, and กำลังจะ shortens to จะ.'},
        'casual': {'thai': 'ยังไม่ได้ไป จะไปตอนเย็น',
                   'paiboon': 'yaŋ mâi dâi bpai, jà bpai dtɔɔn yen'},
    },
    'ตอนนี้คุณกำลังทำอะไรอยู่คะ': {
        'neutral': {'thai': 'ตอนนี้ทำอะไรอยู่คะ', 'paiboon': 'dtɔɔn níi tam à-rai yùu ká',
                    'note': 'อยู่ on its own already carries the "-ing", so กำลัง can go.'},
        'casual': {'thai': 'ทำอะไรอยู่', 'paiboon': 'tam à-rai yùu',
                   'note': 'Two words. Probably the most-used question in Thai texting.'},
    },
    'ผมกำลังทำงานอยู่ครับ แล้วเดี๋ยวจะไปกินข้าวครับ': {
        'neutral': {'thai': 'ทำงานอยู่ครับ เดี๋ยวจะไปกินข้าวครับ',
                    'paiboon': 'tam ŋaan yùu kráp, dǐao jà bpai gin kâao kráp'},
        'casual': {'thai': 'ทำงานอยู่ เดี๋ยวไปกินข้าว',
                   'paiboon': 'tam ŋaan yùu, dǐao bpai gin kâao'},
    },
    'ไปกินด้วยกันไหมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'ไปกินกันไหม', 'paiboon': 'bpai gin gan mǎi',
                   'note': 'ด้วย drops; กัน alone carries "together".'},
    },
    'ได้ครับ ไปกันเลยครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ได้ ไปกันเลย', 'paiboon': 'dâi, bpai gan ləəi'},
    },

    # ---------------------------------------------------------------
    # Taking a Taxi
    # ---------------------------------------------------------------
    'ไปสยามพารากอนครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ไปสยามพารากอน', 'paiboon': 'bpai sà-yǎam paa-raa-gɔɔn'},
        'warn': 'Thais do drop the particle with drivers, but as a learner keep ครับ/ค่ะ — '
                'it costs you nothing and sets the tone for the whole ride.',
    },
    'ได้ครับ เชิญขึ้นเลยครับ': {
        'neutral': {'thai': 'ได้ครับ ขึ้นเลยครับ', 'paiboon': 'dâi kráp, kʉ̂n ləəi kráp',
                    'note': 'เชิญ is the formal "please do" — everyday speech just says ขึ้นเลย.'},
        'casual': {'thai': 'ได้ ขึ้นเลย', 'paiboon': 'dâi, kʉ̂n ləəi'},
    },
    'ใช้มิเตอร์ได้ไหมครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ใช้มิเตอร์ได้ไหม', 'paiboon': 'chái mí-təə dâi mǎi'},
        'warn': 'You are asking a favour of a stranger here. Keep the particle.',
    },
    'ได้ครับ รถติดนิดหน่อยนะครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ได้ รถติดนิดหน่อยนะ', 'paiboon': 'dâi, rót tìt nít-nɔ̀i ná'},
    },
    'ไม่เป็นไรครับ จอดตรงนี้ได้ไหมครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ไม่เป็นไร จอดตรงนี้ได้ไหม',
                   'paiboon': 'mâi bpen rai, jɔ̀ɔt troŋ níi dâi mǎi'},
    },
    'เท่าไหร่ครับ': {
        'neutral': SAME,
        'casual': {'thai': 'เท่าไหร่', 'paiboon': 'tâo-rài'},
    },
    'เก้าสิบบาทครับ': {
        'neutral': {'thai': 'เก้าสิบครับ', 'paiboon': 'gâo-sìp kráp'},
        'casual': {'thai': 'เก้าสิบ', 'paiboon': 'gâo-sìp'},
    },

    # ---------------------------------------------------------------
    # Bargaining at the Market
    # ---------------------------------------------------------------
    'อันนี้เท่าไหร่คะ': {
        'neutral': SAME,
        'casual': {'thai': 'นี่เท่าไหร่', 'paiboon': 'nîi tâo-rài',
                   'note': 'อันนี้ shortens to นี่ when you are pointing at the thing.'},
    },
    'สองร้อยบาทครับ': {
        'neutral': {'thai': 'สองร้อยครับ', 'paiboon': 'sɔ̌ɔŋ rɔ́ɔi kráp'},
        'casual': {'thai': 'สองร้อย', 'paiboon': 'sɔ̌ɔŋ rɔ́ɔi'},
    },
    'แพงไปหน่อยค่ะ ลดได้ไหมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'แพงจัง ลดหน่อยได้ไหม', 'paiboon': 'pɛɛŋ jaŋ, lót nɔ̀i dâi mǎi',
                   'note': 'หน่อย keeps a casual request from sounding like a demand.'},
    },
    'ลดให้ห้าสิบ เหลือร้อยห้าสิบครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ลดให้ห้าสิบ เหลือร้อยห้า',
                   'paiboon': 'lót hâi hâa-sìp, lʉ̌a rɔ́ɔi hâa',
                   'note': 'Market Thai clips 150 to ร้อยห้า — the สิบ is understood.'},
    },
    'ร้อยยี่สิบได้ไหมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'ร้อยยี่ได้ไหม', 'paiboon': 'rɔ́ɔi yîi dâi mǎi',
                   'note': 'Same clipping again: ร้อยยี่ for 120.'},
    },
    'ได้ครับ เอาไปเลย': {
        'neutral': SAME,
        'casual': {'thai': 'ได้ เอาไปเลย', 'paiboon': 'dâi, ao bpai ləəi',
                   'note': 'The vendor already dropped the particle on the second half — '
                           'a friendly sign the haggling is over.'},
    },

    # ---------------------------------------------------------------
    # Visiting a Temple (lay visitor to a lay attendant)
    # ---------------------------------------------------------------
    'ขอโทษค่ะ ต้องถอดรองเท้าไหมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'ต้องถอดรองเท้าไหม', 'paiboon': 'tɔ̂ŋ tɔ̀ɔt rɔɔŋ-táao mǎi'},
        'warn': 'Fine asking the friend you came with. Not to the temple attendant.',
    },
    'ต้องถอดครับ ก่อนเข้าในโบสถ์': {
        'neutral': SAME,
        'casual': {'thai': 'ต้องถอด ก่อนเข้าโบสถ์', 'paiboon': 'tɔ̂ŋ tɔ̀ɔt, gɔ̀ɔn kâo bòot'},
    },
    'แต่งตัวแบบนี้เข้าได้ไหมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'แต่งแบบนี้เข้าได้ไหม', 'paiboon': 'dtɛ̀ŋ bɛ̀ɛp níi kâo dâi mǎi'},
    },
    'ควรปิดไหล่กับหัวเข่าครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ปิดไหล่กับเข่าด้วยนะ', 'paiboon': 'bpìt lài gàp kào dûai ná'},
    },
    'ถ่ายรูปได้ไหมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'ถ่ายรูปได้ไหม', 'paiboon': 'tàai-rûup dâi mǎi'},
    },
    'ได้ครับ แต่อย่าหันหลังให้พระพุทธรูป': {
        'neutral': SAME,
        'casual': {'thai': 'ได้ แต่อย่าหันหลังให้พระ', 'paiboon': 'dâi, dtɛ̀ɛ yàa hǎn lǎŋ hâi prá',
                   'note': 'พระ on its own covers Buddha images as well as monks.'},
        'warn': 'The wording relaxes; the rule does not. Never turn your back on the image.',
    },

    # ---------------------------------------------------------------
    # Offering Alms — monastic register
    # ---------------------------------------------------------------
    'นิมนต์ค่ะ': {
        'monastic': {'note': 'นิมนต์ is the one verb for inviting a monk to do anything — '
                             'receive alms, sit, eat, speak. เชิญ is for people, ชวน is for '
                             'friends, and both are wrong here. There is no casual form.'},
    },
    'ดิฉันขอถวายอาหารค่ะ': {
        'neutral': {'thai': 'ขอถวายอาหารค่ะ', 'paiboon': 'kɔ̌ɔ tà-wǎai aa-hǎan kâ',
                    'note': 'The pronoun can go, exactly as everywhere else. ถวาย cannot.'},
        'monastic': {'note': 'ถวาย is "to give" when the receiver is a monk. Swapping it for ให้ '
                             'is the single most common mistake a learner makes at a temple.'},
    },
    'เจริญพร': {
        'monastic': {'note': 'A monk\'s word, not yours. Monks answer with เจริญพร where a lay '
                             'person would say ครับ/ค่ะ. A layperson never says it.'},
    },
    'ขอให้พระอาจารย์สุขภาพแข็งแรงค่ะ': {
        'neutral': {'thai': 'ขอให้พระอาจารย์สุขภาพแข็งแรงนะคะ',
                    'paiboon': 'kɔ̌ɔ hâi prá aa-jaan sùk-kà-pâap kɛ̌ŋ-rɛɛŋ ná ká',
                    'note': 'นะ is as relaxed as this gets — the title stays in full.'},
        'monastic': {'note': 'Address a monk by title (พระอาจารย์, หลวงพ่อ, หลวงพี่), never by '
                             'คุณ and never by name alone.'},
    },
    'ขอให้โยมมีความสุข มีอายุยืน': {
        'monastic': {'note': 'โยม is how a monk says "you" to a lay person. Note there is no '
                             'ครับ on the end — a monk does not use the lay politeness particles.'},
    },

    # ---------------------------------------------------------------
    # Learning Meditation from a Monk — monastic register
    # ---------------------------------------------------------------
    'กราบนมัสการครับ พระอาจารย์': {
        'monastic': {'note': 'The greeting for a monk. สวัสดีครับ is not wrong so much as '
                             'insufficient — กราบ is the bow itself, said out loud.'},
    },
    'เจริญพร โยม': {
        'monastic': {'note': 'The monk returns the greeting and names you โยม. Warm, not distant '
                             '— this is the normal register between a monk and a supporter.'},
    },
    'ผมอยากเริ่มนั่งสมาธิครับ ควรเริ่มยังไงดีครับ': {
        'neutral': {'thai': 'อยากเริ่มนั่งสมาธิครับ ควรเริ่มยังไงดีครับ',
                    'paiboon': 'yàak rə̂əm nâŋ sà-maa-tí kráp, kuan rə̂əm yaŋ-ŋai dii kráp',
                    'note': 'ผม can drop even here. ครับ absolutely cannot.'},
        'monastic': {'note': 'Speaking to a monk you keep ครับ/ค่ะ on every sentence, not just '
                             'the last one. There is no casual rung in this conversation.'},
    },
    'เริ่มจากลมหายใจ หายใจเข้าก็รู้ หายใจออกก็รู้': {
        'monastic': {'note': 'A monk teaching drops the particles entirely. That is not casual '
                             'speech — it is the plain instructional register monks use.'},
    },
    'ต้องนั่งนานไหมครับ': {
        'neutral': SAME,
        'monastic': {'note': 'Already as short as it goes, and the ครับ stays.'},
    },
    'เริ่มจากสิบนาทีก่อน แล้วค่อยๆ เพิ่มขึ้น': {
        'monastic': {'note': 'Same plain teaching register — direct, no particles, not informal.'},
    },

    # ---------------------------------------------------------------
    # Aspect markers — progressive
    # ---------------------------------------------------------------
    'ผมกำลังกินข้าว': {
        'neutral': {'thai': 'กำลังกินข้าวอยู่', 'paiboon': 'gam-laŋ gin kâao yùu',
                    'note': 'Thai drops the subject freely when it is obvious who you mean.'},
        'casual': {'thai': 'กินข้าวอยู่', 'paiboon': 'gin kâao yùu',
                   'note': 'อยู่ alone does the job of กำลัง. This is the everyday way to say it.'},
    },
    'ผมกำลังทำงาน': {
        'neutral': {'thai': 'กำลังทำงานอยู่', 'paiboon': 'gam-laŋ tam ŋaan yùu'},
        'casual': {'thai': 'ทำงานอยู่', 'paiboon': 'tam ŋaan yùu'},
    },
    'เขากำลังอ่านหนังสือ': {
        'neutral': {'thai': 'เขาอ่านหนังสืออยู่', 'paiboon': 'kǎo àan nǎŋ-sʉ̌ʉ yùu',
                    'note': 'อยู่ at the end replaces กำลัง at the front.'},
    },
    'ดิฉันกำลังกินข้าว': {
        'neutral': {'thai': 'กำลังกินข้าวอยู่', 'paiboon': 'gam-laŋ gin kâao yùu'},
        'casual': {'thai': 'กินข้าวอยู่', 'paiboon': 'gin kâao yùu'},
    },
    'ดิฉันกำลังทำงาน': {
        'neutral': {'thai': 'กำลังทำงานอยู่', 'paiboon': 'gam-laŋ tam ŋaan yùu'},
        'casual': {'thai': 'ทำงานอยู่', 'paiboon': 'tam ŋaan yùu'},
    },

    # ---------------------------------------------------------------
    # Aspect markers — completed
    # ---------------------------------------------------------------
    'ผมกินข้าวแล้ว': {
        'neutral': {'thai': 'กินข้าวแล้ว', 'paiboon': 'gin kâao lɛ́ɛo'},
        'casual': {'thai': 'กินแล้ว', 'paiboon': 'gin lɛ́ɛo',
                   'note': 'ข้าว drops too — "eaten already" is understood as a full meal.'},
    },
    'ผมทำงานเสร็จแล้ว': {
        'neutral': {'thai': 'ทำงานเสร็จแล้ว', 'paiboon': 'tam ŋaan sèt lɛ́ɛo'},
        'casual': {'thai': 'เสร็จแล้ว', 'paiboon': 'sèt lɛ́ɛo',
                   'note': 'Just "done already" — context supplies the rest.'},
    },
    'เขาไปแล้ว': {
        'neutral': SAME,
    },
    'ดิฉันกินข้าวแล้ว': {
        'neutral': {'thai': 'กินข้าวแล้ว', 'paiboon': 'gin kâao lɛ́ɛo'},
        'casual': {'thai': 'กินแล้ว', 'paiboon': 'gin lɛ́ɛo'},
    },
    'ดิฉันทำงานเสร็จแล้ว': {
        'neutral': {'thai': 'ทำงานเสร็จแล้ว', 'paiboon': 'tam ŋaan sèt lɛ́ɛo'},
        'casual': {'thai': 'เสร็จแล้ว', 'paiboon': 'sèt lɛ́ɛo'},
    },

    # ---------------------------------------------------------------
    # Aspect markers — future
    # ---------------------------------------------------------------
    'ผมจะกินข้าว': {
        'neutral': {'thai': 'จะกินข้าว', 'paiboon': 'jà gin kâao'},
        'casual': {'thai': 'จะไปกินข้าว', 'paiboon': 'jà bpai gin kâao',
                   'note': 'Adding ไป makes it sound like a plan rather than a statement.'},
    },
    'ผมจะไปเมืองไทย': {
        'neutral': {'thai': 'จะไปเมืองไทย', 'paiboon': 'jà bpai mʉaŋ-tai'},
        'casual': {'thai': 'จะไปไทย', 'paiboon': 'jà bpai tai',
                   'note': 'เมือง drops in casual speech — just ไทย.'},
    },
    'เขาจะมาพรุ่งนี้': {
        'neutral': SAME,
        'casual': {'thai': 'พรุ่งนี้เขามา', 'paiboon': 'prûŋ-níi kǎo maa',
                   'note': 'Fronting the time and dropping จะ is very natural in speech.'},
    },
    'ดิฉันจะกินข้าว': {
        'neutral': {'thai': 'จะกินข้าว', 'paiboon': 'jà gin kâao'},
        'casual': {'thai': 'จะไปกินข้าว', 'paiboon': 'jà bpai gin kâao'},
    },
    'ดิฉันจะไปเมืองไทย': {
        'neutral': {'thai': 'จะไปเมืองไทย', 'paiboon': 'jà bpai mʉaŋ-tai'},
        'casual': {'thai': 'จะไปไทย', 'paiboon': 'jà bpai tai'},
    },

    # ---------------------------------------------------------------
    # Aspect markers — combined
    # ---------------------------------------------------------------
    'ผมกำลังจะไป': {
        'neutral': {'thai': 'กำลังจะไป', 'paiboon': 'gam-laŋ jà bpai'},
        'casual': {'thai': 'จะไปแล้ว', 'paiboon': 'jà bpai lɛ́ɛo',
                   'note': 'แล้ว with จะ means "off in a moment" — the usual spoken version.'},
    },
    'ผมกินข้าวแล้วจะไป': {
        'neutral': {'thai': 'กินข้าวแล้วจะไป', 'paiboon': 'gin kâao lɛ́ɛo jà bpai'},
        'casual': {'thai': 'กินเสร็จแล้วไป', 'paiboon': 'gin sèt lɛ́ɛo bpai',
                   'note': 'เสร็จ makes the sequence clearer, and จะ drops out.'},
    },
    'ดิฉันกำลังจะไป': {
        'neutral': {'thai': 'กำลังจะไป', 'paiboon': 'gam-laŋ jà bpai'},
        'casual': {'thai': 'จะไปแล้ว', 'paiboon': 'jà bpai lɛ́ɛo'},
    },
    'ดิฉันกินข้าวแล้วจะไป': {
        'neutral': {'thai': 'กินข้าวแล้วจะไป', 'paiboon': 'gin kâao lɛ́ɛo jà bpai'},
        'casual': {'thai': 'กินเสร็จแล้วไป', 'paiboon': 'gin sèt lɛ́ɛo bpai'},
    },

    # ---------------------------------------------------------------
    # Questions — yes/no
    # ---------------------------------------------------------------
    'คุณกินข้าวไหมครับ': {
        'neutral': {'thai': 'กินข้าวไหมครับ', 'paiboon': 'gin kâao mǎi kráp'},
        'casual': {'thai': 'กินข้าวยัง', 'paiboon': 'gin kâao yaŋ',
                   'note': 'The real greeting between friends — "eaten yet?" rather than '
                           '"do you eat?". Answer กินแล้ว or ยัง.'},
    },
    'คุณพูดไทยได้ไหมครับ': {
        'neutral': {'thai': 'พูดไทยได้ไหมครับ', 'paiboon': 'pûut tai dâi mǎi kráp'},
        'casual': {'thai': 'พูดไทยได้ไหม', 'paiboon': 'pûut tai dâi mǎi'},
    },
    'คุณกินข้าวไหมคะ': {
        'neutral': {'thai': 'กินข้าวไหมคะ', 'paiboon': 'gin kâao mǎi ká'},
        'casual': {'thai': 'กินข้าวยัง', 'paiboon': 'gin kâao yaŋ'},
    },
    'คุณพูดไทยได้ไหมคะ': {
        'neutral': {'thai': 'พูดไทยได้ไหมคะ', 'paiboon': 'pûut tai dâi mǎi ká'},
        'casual': {'thai': 'พูดไทยได้ไหม', 'paiboon': 'pûut tai dâi mǎi'},
    },

    # ---------------------------------------------------------------
    # Questions — wh-
    # ---------------------------------------------------------------
    'คุณชื่ออะไรครับ': {
        'neutral': {'thai': 'ชื่ออะไรครับ', 'paiboon': 'chûu à-rai kráp'},
        'casual': {'thai': 'ชื่ออะไร', 'paiboon': 'chûu à-rai'},
    },
    'คุณไปไหนครับ': {
        'neutral': {'thai': 'ไปไหนครับ', 'paiboon': 'bpai nǎi kráp'},
        'casual': {'thai': 'ไปไหน', 'paiboon': 'bpai nǎi',
                   'note': 'Thrown out as a greeting in passing, like "alright?". '
                           'ไปธุระ ("out on an errand") is a fine non-answer.'},
    },
    'ทำไมครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ทำไมล่ะ', 'paiboon': 'tam-mai lâ',
                   'note': 'ล่ะ stops the bare question sounding like a challenge.'},
    },
    'คุณชื่ออะไรคะ': {
        'neutral': {'thai': 'ชื่ออะไรคะ', 'paiboon': 'chûu à-rai ká'},
        'casual': {'thai': 'ชื่ออะไร', 'paiboon': 'chûu à-rai'},
    },
    'คุณไปไหนคะ': {
        'neutral': {'thai': 'ไปไหนคะ', 'paiboon': 'bpai nǎi ká'},
        'casual': {'thai': 'ไปไหน', 'paiboon': 'bpai nǎi'},
    },
    'ทำไมคะ': {
        'neutral': SAME,
        'casual': {'thai': 'ทำไมล่ะ', 'paiboon': 'tam-mai lâ'},
    },

    # ---------------------------------------------------------------
    # Everyday conversation phrases
    # ---------------------------------------------------------------
    'พูดอีกทีได้ไหมครับ': {
        'neutral': SAME,
        'casual': {'thai': 'พูดอีกทีได้ไหม', 'paiboon': 'pûut ìik tii dâi mǎi'},
    },
    'พูดช้าๆ ได้ไหมครับ': {
        'neutral': SAME,
        'casual': {'thai': 'พูดช้าๆ หน่อย', 'paiboon': 'pûut cháa-cháa nɔ̀i'},
    },
    'ผมยังไม่เข้าใจครับ': {
        'neutral': {'thai': 'ยังไม่เข้าใจครับ', 'paiboon': 'yaŋ mâi kâo-jai kráp'},
        'casual': {'thai': 'ยังไม่เข้าใจ', 'paiboon': 'yaŋ mâi kâo-jai'},
    },
    'อ๋อ เข้าใจแล้วครับ': {
        'neutral': SAME,
        'casual': {'thai': 'อ๋อ เข้าใจแล้ว', 'paiboon': 'ɔ̌ɔ, kâo-jai lɛ́ɛo'},
    },
    'อันนี้ภาษาไทยพูดว่าอะไรครับ': {
        'neutral': {'thai': 'อันนี้ภาษาไทยเรียกว่าอะไรครับ',
                    'paiboon': 'an níi paa-sǎa tai rîak wâa à-rai kráp',
                    'note': 'เรียกว่า ("is called") is the more usual verb for naming a thing.'},
        'casual': {'thai': 'อันนี้ภาษาไทยเรียกว่าอะไร',
                   'paiboon': 'an níi paa-sǎa tai rîak wâa à-rai'},
    },
    'คำนี้แปลว่าอะไรครับ': {
        'neutral': SAME,
        'casual': {'thai': 'คำนี้แปลว่าอะไร', 'paiboon': 'kam níi bplɛɛ wâa à-rai'},
    },
    'แบบว่า...': {
        'casual': {'thai': 'แบบว่า...', 'paiboon': 'bɛ̀ɛp wâa...',
                   'note': 'Already casual — filler used mostly between friends.'},
    },
    'เดี๋ยวนะครับ': {
        'neutral': SAME,
        'casual': {'thai': 'เดี๋ยวนะ', 'paiboon': 'dǐao ná'},
    },
    'ขอคิดแป๊บนึงครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ขอคิดแป๊บนึง', 'paiboon': 'kɔ̌ɔ kít bpáep nʉ̀ŋ',
                   'note': 'แป๊บนึง ("a sec") is already colloquial — it never sounds formal.'},
    },
    'จริงเหรอครับ': {
        'neutral': SAME,
        'casual': {'thai': 'จริงเหรอ', 'paiboon': 'jiŋ rə̌ə'},
    },
    'โอเคครับ': {
        'neutral': SAME,
        'casual': {'thai': 'โอเค', 'paiboon': 'oo-kee'},
    },
    'ได้เลยครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ได้เลย', 'paiboon': 'dâi ləəi'},
    },
    'เยี่ยมเลยครับ': {
        'neutral': SAME,
        'casual': {'thai': 'เยี่ยมเลย', 'paiboon': 'yîam ləəi'},
    },
    'น่าสนใจนะครับ': {
        'neutral': SAME,
        'casual': {'thai': 'น่าสนใจนะ', 'paiboon': 'nâa-sǒn-jai ná'},
    },
    'ขอโทษครับ': {
        'neutral': SAME,
        'casual': {'thai': 'โทษที', 'paiboon': 'tôot tii',
                   'note': 'The friends-only version of sorry. Never to a stranger.'},
    },
    'รบกวนหน่อยครับ': {
        'neutral': SAME,
        'casual': {'thai': 'ขอโทษนะ ขอถามหน่อย', 'paiboon': 'kɔ̌ɔ-tôot ná, kɔ̌ɔ tǎam nɔ̀i',
                   'note': 'รบกวน is quite formal. Between friends you would just ask.'},
        'warn': 'รบกวน is worth keeping formal — it is the phrase that makes an imposition '
                'land politely.',
    },
}

# The order the rungs are shown in on the page.
ORDER = ('neutral', 'casual', 'monastic')


def variants_for(thai):
    """The extra register rungs for one formal line, ready to render.

    Returns a list of dicts, each carrying the level's label/colour alongside the
    variant itself, so the template does not have to look anything up. A line
    with no entry here returns an empty list and renders exactly as before.
    """
    entry = VARIANTS.get(thai)
    if not entry:
        return []
    out = []
    for key in ORDER:
        variant = entry.get(key)
        if not variant:
            continue
        row = dict(LEVELS[key])
        row['key'] = key
        row.update(variant)
        out.append(row)
    return out


def warning_for(thai):
    """The 'careful where you use this' note for a line, or None."""
    entry = VARIANTS.get(thai)
    return entry.get('warn') if entry else None


def all_thai_strings():
    """Every new Thai string in this module — for the audio build script.

    Only the variants that actually differ: a SAME rung reuses the formal line's
    recording, and a monastic note has no Thai of its own.
    """
    out, seen = [], set()
    for entry in VARIANTS.values():
        for key in ORDER:
            variant = entry.get(key)
            if not isinstance(variant, dict):
                continue
            thai = variant.get('thai')
            if thai and thai not in seen:
                seen.add(thai)
                out.append(thai)
    return out
