"""The Digital Chanting Book — Pali, Thai, Paiboon and English, verse by verse.

The data lives here rather than in a template on purpose: the same structure
renders the web page today and can generate a printed chanting book later.
Adding a chant means appending one dict to CHANTS — nothing else changes.

Every chant follows the SAME shape, so that between them the six questions a
reader actually has are always answered in the same order:

  * `title_thai` / `title_pali` / `title_roman` / `title_english`
                        — what is this chant? `title_pali` is the title in
                          IAST and is empty where the book prints none;
                          `title_roman` is the THAI title romanised, so a
                          reader who cannot read Thai script can still find
                          the chant in a printed book. A chant whose title is
                          Pali-in-Thai-script needs only `title_pali`.
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

    {
        'id': 'sankhara-contemplation',
        'title_thai': 'บทพิจารณาสังขาร',
        # Josh's source prints no Pali title for this chant, so there is none
        # here. The template skips the line rather than showing a blank.
        'title_pali': '',
        # The Thai title romanised, so a reader who cannot read Thai script can
        # still find this chant in a printed book. Josh's own romanisation,
        # kept verbatim — it is neither Pali IAST nor Paiboon+, and does not
        # need to be either: its whole job is to be findable.
        'title_roman': 'Botpijārana Saṅkhāra',
        # Named by its opening line, the way chants are traditionally
        # identified. It matches verse 1's `pali_roman` exactly.
        'title_english': 'Reflection on Conditioned Phenomena (Sabbe saṅkhārā aniccā)',
        # ⚠️ UNVERIFIED: attributed by Claude, not taken from Josh's book.
        # Verses 1–3 answer to Dhammapada 277–279 and the closing verse to
        # Dhammapada 41; the middle lines are the traditional death-recollection
        # formula. Josh to confirm what his book prints, or clear this field.
        'source': 'Dhammapada 277–279, 41',
        'group': 'General chanting',

        'summary': (
            "Reflections on impermanence, unsatisfactoriness and not-self, "
            "ending with the body laid on the ground like a discarded log."
        ),

        # Taken from the heading Josh pasted: ทุกเวลาทำวัตรเช้าและเข้านอน
        'when_chanted': 'At every morning chanting service and before sleeping.',

        'background': [
            "These verses gather three teachings the Buddha returned to "
            "throughout his life. The first lines are the summary of the three "
            "characteristics — that all conditioned things are impermanent, "
            "unsatisfactory, and that all things without exception are "
            "not-self.",

            "The closing verse comes from a different occasion, when the "
            "Buddha spoke of the body's fate once consciousness has departed: "
            "it lies on the ground as useless as a discarded piece of "
            "firewood. Thai temples place these together so that the "
            "reflection moves from a general truth to the practitioner's own "
            "body.",
        ],

        'meaning': [
            "The chant walks deliberately from the abstract to the personal. "
            "It begins with all conditioned things, narrows to the certainty "
            "of death, and ends with this body, on this ground.",

            "The middle verses are recited in the first person on purpose — my "
            "life is uncertain, my death is certain — because the teaching is "
            "not that people die but that I will.",

            "It is chanted morning and night rather than at funerals, so that "
            "the reflection becomes ordinary rather than reserved for grief. "
            "The intention is not gloom but urgency: a life seen as short is a "
            "life less easily wasted.",
        ],

        # Josh's source carries no invitation line, so there is none.
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },

        # One Pali line per verse, so the chant can be read straight down
        # the page the way it is chanted. `section` starts a new movement.
        'verses': [
            {
                'section': 'Reflection on impermanence',
                'number': 1,
                'pali': 'สัพเพ สังขารา อะนิจจา',
                'pali_roman': 'Sabbe saṅkhārā aniccā',
                'thai': 'สังขารคือร่างกายจิตใจ, และรูปธรรมนามธรรม ทั้งหมดทั้งสิ้น, มันไม่เที่ยง, เกิดขึ้นแล้วดับไป มีแล้ว หายไป',
                'paiboon': 'sǎŋ-kǎan kʉʉ râaŋ-gaai jìt-jai, lɛ́ rûup-bpà-tam naam-má-tam táŋ-mòt táŋ-sîn, man mâi tîaŋ, gə̀ət-kʉ̂n lɛ́ɛo dàp bpai mii lɛ́ɛo hǎai bpai',
                'english': 'All conditioned things — body and mind, and all material and mental phenomena without exception — are impermanent. Having arisen they cease; having been, they vanish.',
            },
            {
                'number': 2,
                'pali': 'สัพเพ สังขารา ทุกขา',
                'pali_roman': 'Sabbe saṅkhārā dukkhā',
                'thai': 'สังขารคือร่างกายจิตใจ, และรูปธรรมนามธรรม ทั้งหมดทั้งสิ้น, มันเป็นทุกข์ทนได้ยากเพราะเกิดขึ้นแล้ว, แก่ เจ็บ ตายไป',
                'paiboon': 'sǎŋ-kǎan kʉʉ râaŋ-gaai jìt-jai, lɛ́ rûup-bpà-tam naam-má-tam táŋ-mòt táŋ-sîn, man bpen túk ton dâai yâak prɔ́ gə̀ət-kʉ̂n lɛ́ɛo, gɛ̀ɛ jèp dtaai bpai',
                'english': 'All conditioned things — body and mind, and all material and mental phenomena without exception — are suffering, hard to bear, because having arisen they age, sicken and die.',
            },
            {
                'number': 3,
                'pali': 'สัพเพ ธัมมา อะนัตตา',
                'pali_roman': 'Sabbe dhammā anattā',
                'thai': 'สิ่งทั้งหลายทั้งปวง, ทั้งที่เป็นสังขารและมิใช่สังขาร ทั้งหมดทั้งสิ้น, ไม่ใช่ตัวไม่ใช่ตน, ไม่ควรถือว่าเรา ว่า ของเรา ว่าตัวว่าตนของเรา',
                'paiboon': 'sìŋ táŋ-lǎai táŋ-bpuaŋ, táŋ tîi bpen sǎŋ-kǎan lɛ́ mí-châi sǎŋ-kǎan táŋ-mòt táŋ-sîn, mâi-châi dtua mâi-châi dton, mâi kuan tʉ̌ʉ wâa rao wâa kɔ̌ɔŋ rao wâa dtua wâa dton kɔ̌ɔŋ rao',
                'english': 'All things whatsoever, conditioned and unconditioned alike, are not self. They should not be held to as "I", as "mine", or as "my self".',
            },
            {
                'section': 'Reflection on life and death',
                'number': 4,
                'pali': 'อะธุวัง ชีวิตัง',
                'pali_roman': 'Adhuvaṃ jīvitaṃ',
                'thai': 'ชีวิตเป็นของไม่ยั่งยืน',
                'paiboon': 'chii-wít bpen kɔ̌ɔŋ mâi yâŋ-yʉʉn',
                'english': 'Life is not enduring.',
            },
            {
                'number': 5,
                'pali': 'ธุวัง มะระณัง',
                'pali_roman': 'Dhuvaṃ maraṇaṃ',
                'thai': 'ความตายเป็นของยั่งยืน',
                'paiboon': 'kwaam-dtaai bpen kɔ̌ɔŋ yâŋ-yʉʉn',
                'english': 'Death is enduring.',
            },
            {
                'number': 6,
                'pali': 'อะวัสสัง มะยา มะริตัพพัง',
                'pali_roman': 'Avassaṃ mayā maritabbaṃ',
                'thai': 'อันเราจะพึงตายเป็นแน่',
                'paiboon': 'an rao jà pʉŋ dtaai bpen nɛ̂ɛ',
                'english': 'It is certain that I must die.',
            },
            {
                'number': 7,
                'pali': 'ชีวิตัง เม อะนิยะตัง',
                'pali_roman': 'Jīvitaṃ me aniyataṃ',
                'thai': 'ชีวิตของเรา เป็นของไม่เที่ยง',
                'paiboon': 'chii-wít kɔ̌ɔŋ rao bpen kɔ̌ɔŋ mâi tîaŋ',
                'english': 'My life is uncertain.',
            },
            {
                'number': 8,
                'pali': 'มะระณะปะริโยสานัง เม ชีวิตัง',
                'pali_roman': 'Maraṇapariyosānaṃ me jīvitaṃ',
                'thai': 'ชีวิตของเรา มีความตายเป็นที่สุดรอบ',
                'paiboon': 'chii-wít kɔ̌ɔŋ rao mii kwaam-dtaai bpen tîi-sùt rɔ̂ɔp',
                'english': 'My life has death as its end.',
            },
            {
                'number': 9,
                'pali': 'มะระณัง เม นิยะตัง',
                'pali_roman': 'Maraṇaṃ me niyataṃ',
                'thai': 'ความตายของเรา เป็นของเที่ยง',
                'paiboon': 'kwaam-dtaai kɔ̌ɔŋ rao bpen kɔ̌ɔŋ tîaŋ',
                'english': 'My death is certain.',
            },
            {
                'section': 'Reflection on the body',
                'number': 10,
                'pali': 'อะจิรัง วะตะ อะยัง กาโย',
                'pali_roman': 'Aciraṃ vata ayaṃ kāyo',
                'thai': 'ร่างกายนี้หนอ, เป็นภาวะที่ตั้งอยู่ไม่นานเลย',
                'paiboon': 'râaŋ-gaai níi nɔ̌ɔ, bpen paa-wá tîi dtâŋ yùu mâi naan ləəi',
                'english': 'This body, alas, is a thing that does not remain long.',
            },
            {
                'number': 11,
                'pali': 'ปะฐะวิง อะธิเสสสะติ',
                'pali_roman': 'Paṭhaviṃ adhisessati',
                'thai': 'จักนอนทับบนแผ่นดิน',
                'paiboon': 'jàk nɔɔn táp bon pɛ̀n-din',
                'english': 'It will lie upon the earth.',
            },
            {
                'number': 12,
                # ฉุฑโท exactly as Josh's source prints it, so the
                # romanisation follows it letter for letter.
                'pali': 'ฉุฑโท อะเปตะวิญญาโณ',
                'pali_roman': 'Chuḍdo apetaviññāṇo',
                'thai': 'ครั้นปราศจากวิญญาณ, อันเขาทิ้งเสียแล้ว',
                'paiboon': 'krán bpràat-sà-jàak win-yaan, an kǎo tíŋ sǐa lɛ́ɛo',
                'english': 'Once bereft of consciousness, cast aside.',
            },
            {
                'number': 13,
                'pali': 'นิรัตถัง วะ กะลิงคะรัง',
                'pali_roman': 'Niratthaṃ va kaliṅgaraṃ',
                'thai': 'ประดุจดังว่าท่อนไม้และท่อนฟืน ซึ่งไร้ประโยชน์ แล้วนั้นแล',
                'paiboon': 'bprà-dùt daŋ wâa tɔ̂n-máai lɛ́ tɔ̂n-fʉʉn sʉ̂ŋ rái bprà-yòot lɛ́ɛo nán-lɛɛ',
                'english': 'Just like a log of wood or firewood, which is without use.',
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
