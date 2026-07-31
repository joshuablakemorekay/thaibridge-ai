"""The Digital Chanting Book — Pali, Thai, Paiboon and English, verse by verse.

The data lives here rather than in a template on purpose: the same structure
renders the web page today and can generate a printed chanting book later.
Adding a chant means appending one dict to CHANTS — nothing else changes.

Every chant follows the SAME shape, so that between them the six questions a
reader actually has are always answered in the same order:

  * `title_thai` / `title_pali` / `title_english`
                        — what is this chant?
  * `source`            — where does it come from? (Dhammapada, Khuddakapāṭha,
                          Suttanipāta or another canonical text)
  * `when_chanted`      — when is it chanted in Theravāda practice?
  * `background`        — why was it taught? The historical setting, or the
                          origin of the chant if it was composed later.
  * `meaning`           — what does it mean, and why is it still chanted?
  * `invitation` + `verses`
                        — how do I chant it?

`background` and `meaning` are LISTS of paragraphs rather than one long string,
so the page and a printed edition can space them the same way without either
one having to split text apart.

Each verse carries up to five layers, and they are NOT interchangeable:

  * `pali`       — the Pali, written in THAI SCRIPT. This is what is actually
                   chanted, and it is what Thai chanting books print. It is
                   Pali, not Thai: do NOT run it through Paiboon.
  * `pali_roman` — the SAME Pali in Latin script with Pali diacritics (IAST:
                   ā ī ū ṃ ṅ ñ ṭ ḍ ṇ ḷ). This is how a non-Thai reader chants
                   it. It is romanised Pali, NOT Paiboon — the two systems
                   share no conventions and must never be mixed.
  * `thai`       — the THAI TRANSLATION of that Pali. This is ordinary Thai
                   and is never chanted; it is there for meaning.
  * `paiboon`    — Paiboon romanisation of `thai` ONLY. It helps an English
                   speaker read the Thai translation aloud. It is a
                   ThaiBridge addition, not a standard chanting-book layer.
  * `english`    — the meaning in English.

Both chanted layers (`pali`, `pali_roman`) keep their couplet line break as a
literal "\\n"; the template renders it with `white-space: pre-line` so the two
scripts break in the same place and can be read side by side down the page.

⚠️ The `paiboon` AND `pali_roman` values below are UNREVIEWED DRAFTS. Josh to
check both against the physical chanting book before any printed use.

Where the romanised Pali could go either way it follows THIS book rather than a
standard edition — e.g. `cetiyāni` (not `cetyāni`), and `ariyañca aṭṭhaṅgikaṃ`
as two words rather than the sandhi form `ariyañcaṭṭhaṅgikaṃ` — because that is
how the Thai script reads once Josh's OCR corrections were applied. The layers
have to agree with each other line for line, which matters more here than
matching any one printed edition.
"""

CHANTS = [
    {
        'id': 'khemakhema-saranadipika',
        'title_thai': 'เขมาเขมะสะระณะทีปิกาคาถา',
        'title_pali': 'Khemākhema-saraṇadīpikā-gāthā',
        'title_english': 'Verses on the Secure and Insecure Refuge',
        'source': 'Dhammapada 188–192',
        'group': 'General chanting',

        # The one-line summary that shows on the closed card in the index.
        'summary': (
            "Five verses contrasting the refuges people run to when "
            "frightened — mountains, forests, shrines — with the only refuge "
            "that actually ends suffering."
        ),

        'when_chanted': 'After the Recollection Verses.',

        'background': [
            "During the Buddha's lifetime, many people believed that "
            "mountains, forests, sacred trees and shrines could protect them "
            "from danger. Observing this, the Buddha taught that although "
            "such places may provide temporary comfort or a sense of "
            "security, they cannot bring lasting freedom from suffering.",

            "These verses were spoken to show that true refuge is not found "
            "in external places, but in understanding and practising the "
            "Dhamma.",
        ],

        'meaning': [
            "The verses contrast ordinary refuges with the Triple Gem — the "
            "Buddha, the Dhamma and the Sangha.",

            "The Buddha explains that genuine refuge is found by "
            "understanding the Four Noble Truths and following the Noble "
            "Eightfold Path, which lead beyond suffering.",

            "These verses are traditionally chanted to reaffirm confidence in "
            "the Triple Gem and to remind practitioners that lasting safety "
            "is found through wisdom, ethical conduct and mental cultivation "
            "rather than external places or objects.",
        ],

        # The leader's invitation. Pali, so it carries no Thai and no Paiboon.
        'invitation': {
            'pali': 'หันทะ มะยัง เขมาเขมะสะระณะทีปิกาคาถาโย ภะณามะ เส',
            'pali_roman': 'Handa mayaṃ khemākhemasaraṇadīpikāgāthāyo bhaṇāma se',
            'thai': '',
            'paiboon': '',
            'english': (
                'Now let us recite the verses illuminating the secure and '
                'insecure refuges.'
            ),
        },

        'verses': [
            {
                'number': 1,
                'pali': (
                    'พะหุง เว สะระณัง ยันติ ปัพพะตานิ วะนานิ จะ\n'
                    'อารามะรุกขะเจติยานิ มะนุสสา ภะยะตัชชิตา'
                ),
                'pali_roman': (
                    'Bahuṃ ve saraṇaṃ yanti, pabbatāni vanāni ca\n'
                    'Ārāmarukkhacetiyāni, manussā bhayatajjitā'
                ),
                'thai': (
                    'มนุษย์เป็นอันมาก เมื่อเกิดมีภัยคุกคามแล้ว ก็ถือเอาภูเขาบ้าง '
                    'ป่าไม้บ้าง อาราม และรุกขเจดีย์บ้าง เป็นสรณะ'
                ),
                'paiboon': (
                    'má-nút bpen an mâak, mʉ̂a gə̀ət mii pai kúk-kaam lɛ́ɛo, '
                    'gɔ̂ tʉ̌ʉ ao puu-kǎo bâaŋ, bpàa máai bâaŋ, aa-raam '
                    'lɛ́ rúk-kà-jee-dii bâaŋ, bpen sà-rá-ná'
                ),
                'english': (
                    'Many people, when threatened by fear, go for refuge to '
                    'mountains, to forests, to parks and to tree-shrines.'
                ),
            },
            {
                'number': 2,
                'pali': (
                    'เนตัง โข สะระณัง เขมัง เนตัง สะระณะมุตตะมัง\n'
                    'เนตัง สะระณะมาคัมมะ สัพพะทุกขา ปะมุจจะติ'
                ),
                'pali_roman': (
                    'Netaṃ kho saraṇaṃ khemaṃ, netaṃ saraṇamuttamaṃ\n'
                    'Netaṃ saraṇamāgamma, sabbadukkhā pamuccati'
                ),
                'thai': (
                    'นั่นมิใช่สรณะอันเกษมเลย นั่นมิใช่สรณะอันสูงสุด '
                    'เขาอาศัยสรณะนั่นแล้ว ย่อมไม่พ้นจากทุกข์ทั้งปวงได้'
                ),
                'paiboon': (
                    'nân mí châi sà-rá-ná an gà-sěem ləəi, nân mí châi '
                    'sà-rá-ná an sǔuŋ-sùt, kǎo aa-sǎi sà-rá-ná nân lɛ́ɛo, '
                    'yɔ̂m mâi pón jàak túk táŋ-bpuaŋ dâai'
                ),
                'english': (
                    'That is not a secure refuge, that is not the supreme '
                    'refuge. Having gone to such a refuge, one is not freed '
                    'from all suffering.'
                ),
            },
            {
                'number': 3,
                'pali': (
                    'โย จะ พุทธัญจะ ธัมมัญจะ สังฆัญจะ สะระณัง คะโต\n'
                    'จัตตาริ อะริยะสัจจานิ สัมมัปปัญญายะ ปัสสะติ'
                ),
                'pali_roman': (
                    'Yo ca buddhañca dhammañca, saṅghañca saraṇaṃ gato\n'
                    'Cattāri ariyasaccāni, sammappaññāya passati'
                ),
                'thai': (
                    'ส่วนผู้ใดถือเอาพระพุทธ พระธรรม พระสงฆ์ เป็นสรณะแล้ว '
                    'เห็นอริยสัจ คือความจริงอันประเสริฐสี่ ด้วยปัญญาอันชอบ'
                ),
                'paiboon': (
                    'sùan pûu dai tʉ̌ʉ ao prá-pút, prá-tam, prá-sǒŋ bpen '
                    'sà-rá-ná lɛ́ɛo, hěn à-rí-yá-sàt kʉʉ kwaam jiŋ an '
                    'bprà-sə̀ət sìi dûai bpan-yaa an chɔ̂ɔp'
                ),
                'english': (
                    'But whoever goes for refuge to the Buddha, the Dhamma '
                    'and the Sangha sees, with right wisdom, the Four Noble '
                    'Truths:'
                ),
            },
            {
                'number': 4,
                'pali': (
                    'ทุกขัง ทุกขะสะมุปปาทัง ทุกขัสสะ จะ อะติกกะมัง\n'
                    'อะริยัญจะ อัฏฐังคิกัง มัคคัง ทุกขูปะสะมะคามินัง'
                ),
                'pali_roman': (
                    'Dukkhaṃ dukkhasamuppādaṃ, dukkhassa ca atikkamaṃ\n'
                    'Ariyañca aṭṭhaṅgikaṃ maggaṃ, dukkhūpasamagāminaṃ'
                ),
                'thai': (
                    'คือเห็นความทุกข์ เหตุให้เกิดทุกข์ ความก้าวล่วงทุกข์เสียได้ '
                    'และหนทางมีองค์แปดอันประเสริฐ เครื่องถึงความระงับทุกข์'
                ),
                'paiboon': (
                    'kʉʉ hěn kwaam túk, hèet hâi gə̀ət túk, kwaam gâao lûaŋ '
                    'túk sǐa dâai, lɛ́ hǒn-taaŋ mii oŋ bpɛ̀ɛt an bprà-sə̀ət, '
                    'krʉ̂aŋ tʉ̌ŋ kwaam rá-ŋáp túk'
                ),
                'english': (
                    'suffering, the arising of suffering, the transcending of '
                    'suffering, and the Noble Eightfold Path leading to the '
                    'stilling of suffering.'
                ),
            },
            {
                'number': 5,
                'pali': (
                    'เอตัง โข สะระณัง เขมัง เอตัง สะระณะมุตตะมัง\n'
                    'เอตัง สะระณะมาคัมมะ สัพพะทุกขา ปะมุจจะติ ฯ'
                ),
                'pali_roman': (
                    'Etaṃ kho saraṇaṃ khemaṃ, etaṃ saraṇamuttamaṃ\n'
                    'Etaṃ saraṇamāgamma, sabbadukkhā pamuccati'
                ),
                'thai': (
                    'นั่นแหละเป็นสรณะอันเกษม นั่นเป็นสรณะอันสูงสุด '
                    'เขาอาศัยสรณะนั่นแล้ว ย่อมพ้นจากทุกข์ทั้งปวงได้'
                ),
                'paiboon': (
                    'nân lɛ̀ bpen sà-rá-ná an gà-sěem, nân bpen sà-rá-ná an '
                    'sǔuŋ-sùt, kǎo aa-sǎi sà-rá-ná nân lɛ́ɛo, yɔ̂m pón jàak '
                    'túk táŋ-bpuaŋ dâai'
                ),
                'english': (
                    'That is the secure refuge, that is the supreme refuge. '
                    'Having gone to such a refuge, one is freed from all '
                    'suffering.'
                ),
            },
        ],
    },
]


# The layers a reader can switch on and off, in the order they appear on the
# page. `key` matches the verse dict.
#
# `colour` is the SINGLE source of truth for that layer's colour: the template
# generates the text colour, the left rule and the toggle swatch from this one
# value, so they cannot drift apart. To recolour a layer, change it here only.
#
# The two chanted layers sit in a warm family (they are the same Pali in two
# scripts); the three meaning layers are cool or neutral, so a glance tells you
# whether you are looking at something to chant or something to understand.
#
# `note` is the short label under each toggle; `description` is the fuller
# sentence used in "How to use this chanting book" and in the printed edition's
# front matter.
CHANT_LAYERS = [
    {
        'key': 'pali', 'label': 'Pali (Thai script)',
        'note': 'What is chanted', 'colour': 'var(--royal-burgundy)',
        'description': 'The original chant as recited in Thai Theravāda temples.',
    },
    {
        'key': 'pali_roman', 'label': 'Pali (Romanised)',
        'note': 'The same, in our script', 'colour': 'var(--isan-clay)',
        'description': 'The same Pali written in the Latin alphabet to aid pronunciation.',
    },
    {
        'key': 'thai', 'label': 'Thai translation',
        'note': 'The meaning, in Thai', 'colour': 'var(--deep-purple)',
        'description': (
            'The meaning in Thai. In many Thai temples, this is also recited '
            'after the Pali.'
        ),
    },
    {
        'key': 'paiboon', 'label': 'Thai (Paiboon)',
        'note': 'Read the Thai aloud', 'colour': 'var(--bodhi-green)',
        'description': (
            'The Thai translation romanised for readers who cannot yet read '
            'Thai script.'
        ),
    },
    {
        'key': 'english', 'label': 'English translation',
        'note': 'The meaning, in English', 'colour': '#555555',
        'description': 'The meaning in English.',
    },
]


# Front matter. It opens the web page and will open the printed edition too,
# which is the point: one book, two formats.
HOW_TO_USE = {
    'welcome': (
        'Welcome to the Digital Chanting Book. Each chant is presented in '
        'five optional layers to support both learning and practice.'
    ),
    'closing': (
        'Show only the layers you need. As your confidence grows, try '
        'chanting directly from the Pali while using the translations to '
        'deepen your understanding.'
    ),
    'layout': (
        'where it comes from, when it is chanted, its historical background, '
        'its meaning and purpose, and then the chant itself.'
    ),
}


# The standard sections every chant carries, in the order they are shown. The
# template loops over this rather than hard-coding each heading, so a new
# section is added in one place and appears on every chant at once.
#
# `collapsible` sections open on a tap: they keep the chant itself close to the
# top for someone who just wants to chant, without hiding the context from
# someone who wants to understand it.
CHANT_SECTIONS = [
    {'key': 'background', 'heading': 'Historical background', 'collapsible': True},
    {'key': 'meaning',    'heading': 'Meaning and purpose',   'collapsible': True},
]


def get_chant(chant_id):
    """Return one chant by id, or None."""
    return next((c for c in CHANTS if c['id'] == chant_id), None)
