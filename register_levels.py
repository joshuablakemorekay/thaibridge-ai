"""The nine registers of Thai — data for templates/register.html.

⚠️ UNREVIEWED DRAFT. Every Thai line, romanisation and gloss below was written
by Claude and has NOT been checked by a native speaker or a teacher. It is not
wired to the /register route yet (that route redirects to /formality) precisely
so this cannot reach a learner before it has been read. Do not ship it until
Josh and his teacher have been through it.

Not to be confused with thai_registers.py, which is a different thing with a
confusingly similar name: that module holds the THREE politeness variants
(formal / neutral / casual) generated under each sentence on /sentences. This
module is the NINE-level formality scale taught as a reference on /register —
a taxonomy to read about, not a transformation applied to sentences.

Romanisation follows Paiboon as used elsewhere in the app: doubled vowels for
length (aa, ii, ɔɔ), and tone marks mid (a), low (à), falling (â), high (á),
rising (ǎ). Where the existing Paiboon index disagrees with itself, the
consistent spelling is used here and the divergence noted in the review sheet.

Shape each entry must keep — templates/register.html reads exactly these keys:

    level, name, thai, icon, color, description, usage_context,
    social_notes, examples[{thai, paiboon, english, note|polite}], warning

plus `sub_level_a`/`sub_level_b` on 'casual' and `cultural_notes` on 'vulgar'.
"""

REGISTER_LEVELS = {

    # ── 1 ─────────────────────────────────────────────────────────────────
    'monastic': {
        'level': 1,
        'name': 'Monastic Language',
        'thai': 'ภาษาพระ',
        'icon': '🙏',
        'color': '#FF9933',
        'description': (
            'The vocabulary used by monks and used towards them. It is not '
            '"more polite" ordinary Thai — it is a separate set of words for '
            'the same everyday actions, so that eating, sleeping, falling ill '
            'and dying each have a monastic form.'
        ),
        'usage_context': (
            'In temples, when speaking with or about monks, and throughout '
            'chanting and Dhamma teaching.'
        ),
        'social_notes': (
            'A monk calls himself อาตมา and calls the layperson he is speaking '
            'to โยม. Laypeople do not use อาตมา about themselves, and monks do '
            'not use ผม in this setting.'
        ),
        'examples': [
            {
                'thai': 'อาตมาจะไปวัด',
                'paiboon': 'àat-dtà-maa jà bpai wát',
                'english': 'I will go to the temple.',
                'note': 'อาตมา is the pronoun a monk uses for himself. A layperson never uses it.',
            },
            {
                'thai': 'นิมนต์ครับ',
                'paiboon': 'ní-mon kráp',
                'english': 'Please, venerable sir.',
                'note': 'นิมนต์ replaces เชิญ ("please, do go ahead") when the invitation is to a monk.',
            },
            {
                'thai': 'พระฉันข้าวแล้วหรือยังครับ',
                'paiboon': 'prá chǎn kâao lɛ́ɛo rʉ̌ʉ yang kráp',
                'english': 'Has the venerable eaten yet?',
                'note': 'ฉัน is the monastic word for eating. กิน would be wrong here.',
            },
            {
                'thai': 'นมัสการครับ',
                'paiboon': 'ná-mát-sà-gaan kráp',
                'english': 'I pay my respects.',
                'note': 'The monastic greeting, in place of สวัสดี.',
            },
        ],
        'warning': (
            '⚠️ The commonest mistake is using กิน for a monk or ฉัน for a '
            'layperson. Both land wrong: one is too plain, the other claims a '
            'status you do not have.'
        ),
    },

    # ── 2 ─────────────────────────────────────────────────────────────────
    'royal': {
        'level': 2,
        'name': 'Royal Language',
        'thai': 'ราชาศัพท์',
        'icon': '👑',
        'color': '#D4AF37',
        'description': (
            'A distinct vocabulary for the monarchy, drawn largely from Pali, '
            'Sanskrit and Khmer. As with monastic language it substitutes '
            'whole words rather than adding politeness: royalty do not กิน or '
            'นอน, they เสวย and บรรทม.'
        ),
        'usage_context': (
            'Royal news bulletins, ceremonies, official announcements, and '
            'writing about the royal family.'
        ),
        'social_notes': (
            'Thais learn to recognise this at school and hear it daily on the '
            'evening news, but very few ever have cause to produce it.'
        ),
        'examples': [
            {
                'thai': 'ทรงพระเจริญ',
                'paiboon': 'song prá jà-rəən',
                'english': 'Long may he/she live.',
                'note': 'The standard acclamation. ทรง marks the verb that follows as royal.',
            },
            {
                'thai': 'เสวย',
                'paiboon': 'sà-wə̌əi',
                'english': 'to eat (royal)',
                'note': 'Replaces กิน / รับประทาน entirely.',
            },
            {
                'thai': 'บรรทม',
                'paiboon': 'ban-tom',
                'english': 'to sleep (royal)',
                'note': 'Replaces นอน.',
            },
            {
                'thai': 'ข้าพระพุทธเจ้า',
                'paiboon': 'kâa-prá-pút-tá-jâo',
                'english': 'I (addressing the monarch)',
                'note': 'The most deferential first person in the language.',
            },
        ],
        'warning': (
            '⚠️ Recognise this register; do not improvise in it. Thailand’s '
            'lèse-majesté law (Section 112) makes speech about the monarchy a '
            'criminal matter, and getting the forms wrong in public is a real '
            'risk rather than a social embarrassment. Read it, do not write it.'
        ),
    },

    # ── 3 ─────────────────────────────────────────────────────────────────
    'obsolete': {
        'level': 3,
        'name': 'Archaic & Ceremonial',
        'thai': 'ภาษาโบราณ',
        'icon': '📜',
        'color': '#8D6E63',
        'description': (
            'Older Thai that has fallen out of speech but survives where '
            'language is deliberately preserved: legal documents, formal '
            'invitations, inscriptions, temple texts and historical drama.'
        ),
        'usage_context': (
            'Contracts and statutes, engraved plaques, wedding and ordination '
            'invitations, period television.'
        ),
        'social_notes': (
            'Encountering these in a document is normal; using them in speech '
            'sounds theatrical, and is sometimes played for comedy.'
        ),
        'examples': [
            {
                'thai': 'ณ',
                'paiboon': 'ná',
                'english': 'at (a place)',
                'note': 'Still standard on invitations and plaques where ที่ would be used in speech.',
            },
            {
                'thai': 'อนึ่ง',
                'paiboon': 'à-nʉ̀ng',
                'english': 'furthermore; moreover',
                'note': 'Opens an additional clause in legal and official writing.',
            },
            {
                'thai': 'ข้า / เอ็ง',
                'paiboon': 'kâa / eng',
                'english': 'I / you (archaic)',
                'note': 'Heard constantly in historical drama, never in a modern conversation.',
            },
        ],
        'warning': (
            '⚠️ These are for reading, not speaking. Dropping ณ or เอ็ง into '
            'conversation is the equivalent of saying "hitherto" and "thou" at '
            'a bus stop.'
        ),
    },

    # ── 4 ─────────────────────────────────────────────────────────────────
    'literary': {
        'level': 4,
        'name': 'Literary & Poetic',
        'thai': 'ภาษาวรรณคดี',
        'icon': '✒️',
        'color': '#7E57C2',
        'description': (
            'An elevated vocabulary for poetry, song and literary prose, again '
            'mostly Sanskrit and Pali in origin. Many everyday things have a '
            'poetic twin used for beauty and metre.'
        ),
        'usage_context': (
            'Poetry, song lyrics, novels, speeches and anywhere language is '
            'meant to be admired as well as understood.'
        ),
        'social_notes': (
            'Thai popular song leans on this register heavily, so learners '
            'meet it far earlier through music than through books.'
        ),
        'examples': [
            {
                'thai': 'บุปผา',
                'paiboon': 'bùp-pǎa',
                'english': 'flower',
                'note': 'Poetic twin of ดอกไม้ (dɔ̀ɔk-máai).',
            },
            {
                'thai': 'นภา',
                'paiboon': 'ná-paa',
                'english': 'sky',
                'note': 'Poetic twin of ท้องฟ้า (tɔ́ɔng-fáa).',
            },
            {
                'thai': 'ดวงใจ',
                'paiboon': 'duang-jai',
                'english': 'beloved; heart',
                'note': 'Literally "orb of the heart" — everywhere in love songs.',
            },
        ],
        'warning': (
            '⚠️ Lovely in a verse, peculiar in a conversation. Ordering บุปผา '
            'at a flower stall would be understood, and would be remembered.'
        ),
    },

    # ── 5 ─────────────────────────────────────────────────────────────────
    'technical': {
        'level': 5,
        'name': 'Academic & Technical',
        'thai': 'ภาษาวิชาการ',
        'icon': '🔬',
        'color': '#0288D1',
        'description': (
            'The register of textbooks, research, medicine, law and official '
            'reports. Built from long Pali and Sanskrit compounds, which is '
            'what makes it precise and also what makes it heavy.'
        ),
        'usage_context': (
            'Academic writing, professional documents, news analysis, lectures.'
        ),
        'social_notes': (
            'Because the roots are shared, a learner who knows Buddhist Pali '
            'terms often finds this vocabulary easier than expected.'
        ),
        'examples': [
            {
                'thai': 'วิเคราะห์',
                'paiboon': 'wí-krɔ́',
                'english': 'to analyse',
                'note': 'From Sanskrit; the everyday equivalent would be a phrase, not a word.',
            },
            {
                'thai': 'สมมติฐาน',
                'paiboon': 'sǒm-mút-dtì-tǎan',
                'english': 'hypothesis',
                'note': 'สมมติ (supposed) + ฐาน (base).',
            },
            {
                'thai': 'ปรากฏการณ์',
                'paiboon': 'bpraa-gòt-dtà-gaan',
                'english': 'phenomenon',
                'note': 'The -การณ์ ending marks an abstract noun, as -tion does in English.',
            },
        ],
        'warning': (
            '⚠️ Precise on the page, stilted in the mouth. Using this register '
            'in casual conversation reads as pompous rather than educated.'
        ),
    },

    # ── 6 ─────────────────────────────────────────────────────────────────
    'formal': {
        'level': 6,
        'name': 'Formal',
        'thai': 'ภาษาทางการ',
        'icon': '🎩',
        'color': '#388E3C',
        'description': (
            'Careful, respectful spoken and written Thai for occasions with '
            'distance in them: meetings, officialdom, customer service, and '
            'speaking to someone notably senior.'
        ),
        'usage_context': (
            'Business, government offices, formal letters, addressing elders '
            'and people of higher rank.'
        ),
        'social_notes': (
            'Full pronouns are kept rather than dropped, particles are never '
            'omitted, and verbs take their formal forms.'
        ),
        'examples': [
            {
                'thai': 'กระผมขอเรียนเชิญท่านครับ',
                'paiboon': 'grà-pǒm kɔ̌ɔ rian chəən tân kráp',
                'english': 'I would like to invite you, sir.',
                'note': 'กระผม is a more deferential ผม; ท่าน a more deferential คุณ.',
            },
            {
                'thai': 'รับประทานอาหาร',
                'paiboon': 'ráp-bprà-taan aa-hǎan',
                'english': 'to have a meal',
                'note': 'The formal form of กิน. ทาน is the everyday middle ground.',
            },
            {
                'thai': 'ขอบพระคุณครับ',
                'paiboon': 'kɔ̀ɔp prá kun kráp',
                'english': 'Thank you (formal).',
                'note': 'พระ inserted into ขอบคุณ raises it a level.',
            },
        ],
        'warning': (
            '⚠️ Safe almost everywhere, but sustained formality with friends '
            'creates distance — it can read as coldness rather than respect.'
        ),
    },

    # ── 7 ─────────────────────────────────────────────────────────────────
    'neutral': {
        'level': 7,
        'name': 'Neutral / Polite',
        'thai': 'ภาษาสุภาพ',
        'icon': '💬',
        'color': '#00897B',
        'description': (
            'Standard polite everyday Thai: the register of shops, offices, '
            'taxis, classrooms and most conversations between adults who are '
            'not close friends.'
        ),
        'usage_context': (
            'Daily life with strangers, colleagues, shopkeepers — the default '
            'setting for almost every situation a visitor meets.'
        ),
        'social_notes': (
            'Marked above all by keeping ครับ (men) or ค่ะ/คะ (women) on the '
            'end. Those particles do more politeness work than any other '
            'single feature of the language.'
        ),
        'examples': [
            {
                'thai': 'สวัสดีครับ',
                'paiboon': 'sà-wàt-dii kráp',
                'english': 'Hello.',
                'note': 'Works as both hello and goodbye, at any hour.',
            },
            {
                'thai': 'ผมกินข้าวแล้วครับ',
                'paiboon': 'pǒm gin kâao lɛ́ɛo kráp',
                'english': 'I have eaten.',
                'note': 'ผม for a male speaker; a woman would say ดิฉัน (dì-chǎn) or ฉัน (chǎn).',
            },
            {
                'thai': 'ขอบคุณครับ',
                'paiboon': 'kɔ̀ɔp-kun kráp',
                'english': 'Thank you.',
                'note': 'Add มาก (mâak) for "thank you very much".',
            },
        ],
        'warning': (
            '✅ This is the one to learn first. If you are unsure which '
            'register a situation calls for, this is almost never wrong.'
        ),
    },

    # ── 8 ─────────────────────────────────────────────────────────────────
    'casual': {
        'level': 8,
        'name': 'Casual / Colloquial',
        'thai': 'ภาษาพูด',
        'icon': '😊',
        'color': '#FB8C00',
        'description': (
            'How friends, classmates and family actually talk: particles '
            'dropped, pronouns swapped for nicknames, sentences shortened, '
            'and questions marked by tone rather than by a question word.'
        ),
        'usage_context': (
            'Close friends, people your own age, family, and social media.'
        ),
        'social_notes': (
            'Being spoken to casually is a compliment — it says the distance '
            'has closed. Offering it too early does the opposite.'
        ),
        'examples': [
            {
                'thai': 'ไปไหน',
                'paiboon': 'bpai nǎi',
                'english': 'Where are you going?',
                'polite': 'ไปไหนครับ',
            },
            {
                'thai': 'กินข้าวยัง',
                'paiboon': 'gin kâao yang',
                'english': 'Eaten yet?',
                'polite': 'ทานข้าวหรือยังครับ',
            },
            {
                'thai': 'เออ',
                'paiboon': 'əə',
                'english': 'Yeah.',
                'polite': 'ครับ / ค่ะ',
            },
        ],
        'sub_level_a': {
            'name': 'Relaxed with friends',
            'note': (
                'Friendly and unremarkable between equals. Pronouns soften, '
                'particles come and go, and nicknames replace names.'
            ),
            'examples': [
                'เรา (rao) — I, among friends',
                'แก (gɛɛ) — you, affectionate',
                'ไง (ngai) — tag: "…you know?"',
            ],
        },
        'sub_level_b': {
            'name': 'Blunt',
            'note': (
                'Not obscene, but abrupt enough to sting if the closeness is '
                'not already there. Common between young men and in banter.'
            ),
            'examples': [
                'ว่ะ (wâ) — rough sentence particle',
                'เว้ย (wə́əi) — "oi!", calling someone',
                'มั้ย for ไหม — clipped question particle',
            ],
        },
        'warning': (
            '⚠️ Wait to be spoken to this way before speaking this way. Going '
            'casual first with someone older or senior is the single easiest '
            'way for a learner to give offence without knowing it.'
        ),
    },

    # ── 9 ─────────────────────────────────────────────────────────────────
    'vulgar': {
        'level': 9,
        'name': 'Vulgar',
        'thai': 'ภาษาหยาบ',
        'icon': '⚠️',
        'color': '#D32F2F',
        'description': (
            'Coarse pronouns and swearing. Included so you can recognise it '
            'and understand what has happened when you hear it — not so you '
            'can use it.'
        ),
        'usage_context': (
            'Anger and insult; also, confusingly, warm intimacy between very '
            'old friends.'
        ),
        'social_notes': (
            'กู and มึง are the marker of this register. Between lifelong '
            'friends they signal that no politeness is needed between us; '
            'anywhere else they are a slap.'
        ),
        'examples': [
            {
                'thai': 'กู',
                'paiboon': 'guu',
                'english': 'I (vulgar)',
                'note': 'Between close friends, a sign of intimacy. To a stranger, an insult.',
            },
            {
                'thai': 'มึง',
                'paiboon': 'mʉng',
                'english': 'you (vulgar)',
                'note': 'The partner of กู. The two travel together.',
            },
            {
                'thai': 'ไอ้ / อี',
                'paiboon': 'âi / ii',
                'english': 'derogatory prefixes (male / female)',
                'note': 'Prefixed to a name. Insulting from a stranger, teasing between friends.',
            },
        ],
        'cultural_notes': (
            'กู and มึง were once ordinary, neutral pronouns — they appear as '
            'plain first and second person in old Thai texts, and only drifted '
            'to vulgarity over centuries as politer alternatives arrived. That '
            'history is why they can still carry affection: they are old and '
            'plain, not invented as insults. Around monks, elders, teachers, '
            'officials or strangers, none of that history helps.'
        ),
        'warning': (
            '⚠️ Learn to recognise these; do not use them. A learner using กู '
            'or มึง does not sound fluent, it sounds hostile — and the excuse '
            '"I heard my friend say it" will not travel to the person you say '
            'it to. Stronger obscenities exist and are deliberately not '
            'listed here.'
        ),
    },
}
