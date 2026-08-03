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

    {
        # ‼ CHECK: The invitation reads ธาตุปะฏิกูละปัจจะเวกขะณะปารัง. ปารัง
        #          looks like an OCR slip for ปาฐัง (pāṭhaṃ), which would agree
        #          with the title ปาโฐ. Reproduced as pasted and romanised
        #          faithfully as pāraṃ; compare the printed invitation line.
        # ‼ CHECK: source left empty. The book text you pasted gives no
        #          canonical attribution, and I have not supplied one from
        #          memory. If the book prints a source line, it needs adding by
        #          hand.
        # ‼ CHECK: The rubric for the second movement reads ขณะรับบิณฑบาต) with
        #          a closing parenthesis but no opening one, unlike the other
        #          three. Check whether the book prints ( there.

        'id': 'dhatupatikula-paccavekkhana',
        'title_thai': 'ธาตุปะฏิกูละปัจจะเวกขะณะปาโฐ',
        'title_pali': 'Dhātupaṭikūlapaccavekkhaṇapāṭho',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Reflection on the Elements and on Repulsiveness',
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        'summary': (
            "A fourfold reflection at the moment of receiving robe, almsfood, "
            "lodging and medicine: requisite and user alike are mere elements, "
            "empty of self, made foul by the body."
        ),

        'when_chanted': (
            "Recited over the four requisites — robe, almsfood, lodging and "
            "medicinal support — at the time of receiving or using them, and "
            "included in the evening chanting of many Thai monasteries."
        ),

        'background': [
            "Monastic training requires that the four requisites be received "
            "and used with reflection rather than appetite, and the chanting "
            "books preserve more than one formula for doing so. This one takes "
            "the elemental line: whatever is received is analysed into bare "
            "elements arising according to conditions, and the same analysis "
            "is turned at once upon the person receiving it, so that neither "
            "the gift nor the recipient is left standing as a solid thing.",

            "The text is built as a single reflection repeated four times, "
            "with only the name of the requisite and the grammatical number "
            "changing — จีวร and เสนาสนะ taking plural forms, บิณฑบาต and "
            "คิลานเภสัชบริขาร taking singular. The book marks each repetition "
            "with a rubric in parentheses naming the moment at which it is "
            "used. A reader who learns the first movement has effectively "
            "learned all four.",
        ],

        'meaning': [
            "The opening line sets the frame: what lies here is only "
            "element-matter, ยะถาปัจจะยัง, proceeding as its causes and "
            "conditions proceed. Nothing is denied existence; what is denied "
            "is that the thing possesses any nature of its own beyond the "
            "conditions currently sustaining it. The Thai renders this with "
            "สักว่าธาตุตามธรรมชาติ, merely elements after the manner of "
            "nature.",

            "The reflection then extends to the one who uses the requisite. He "
            "too is ธาตุมัตตะโก, mere elements; นิสสัตโต, not an enduring "
            "being; นิชชีโว, not a soul or person; สุญโญ, empty of the meaning "
            "of selfhood. The force of the passage lies in this symmetry. It "
            "is not that the robe is impersonal while the wearer remains a "
            "self; the same analysis is applied to both sides of the "
            "transaction, and the act of using ceases to be an encounter "
            "between a person and a possession.",

            "The closing movement turns to repulsiveness, and does so with a "
            "precision worth noticing. The requisites are said to be "
            "อะชิคุจฉะนียานิ, not repulsive in themselves — cloth, food, "
            "shelter and medicine are not by nature foul. It is contact with "
            "this body, perpetually decaying, that renders them so. The "
            "reflection therefore locates the impurity where the training "
            "places it: not in the world, but in the body that meets the "
            "world.",
        ],

        'invitation': {
            'pali': 'หันทะ มะยัง ธาตุปะฏิกูละปัจจะเวกขะณะปารัง ภะณามะ เส.',
            'pali_roman': (
                "handa mayaṃ dhātupaṭikūlapaccavekkhaṇapāraṃ bhaṇāma se."
            ),
            'thai': '',
            'paiboon': '',
            'english': (
                "Now let us recite the passage on the elements and on "
                "repulsiveness."
            ),
        },

        'verses': [
            # ‼ CORRECTED: thai  เนื่องนิจ → เนืองนิจ. เนื่องนิจ (mai ek) is a
            #              slip for เนืองนิจ "constantly"; verses 10 and 19
            #              print it correctly. Verify against the printed page.
            # ‼ CORRECTED: thai  ตามเหตุตาม ปัจจัย → ตามเหตุตามปัจจัย. Stray
            #              space inside ปัจจัย closed up; verses 10, 19 and 28
            #              print it unbroken. Verify against the printed page.
            # ‼ CORRECTED: paiboon  nʉ̂aŋ nít → nʉaŋ nít. Follows the เนืองนิจ
            #              correction. Verify against the printed page.
            {
                'section': 'ขณะรับจีวร: While Receiving the Robe',
                'number': 1,
                'pali': 'ยะถาปัจจะยัง ปะวัตตะมานัง ธาตุมัตตะเมเวตัง,',
                'pali_roman': 'yathāpaccayaṃ pavattamānaṃ dhātumattamevetaṃ,',
                'thai': 'สิ่งเหล่านี้ นี่เป็นสักว่าธาตุตามธรรมชาติเท่านั้น, กำลังเป็นไปตามเหตุตามปัจจัยอยู่เนืองนิจ,',
                'paiboon': 'sìŋ lào níi nîi bpen sàk wâa tâat dtaam tam-má-châat tâo-nán, gam-laŋ bpen bpai dtaam hèet dtaam bpàt-jai yùu nʉaŋ nít,',
                'english': 'These things here are merely elements after the manner of nature, proceeding continually according to their causes and conditions,',
            },
            {
                'number': 2,
                'pali': 'ยะทิทัง จีวะรัง, ตะทุปะภุญชะโก จะ ปุคคะโล,',
                'pali_roman': 'yadidaṃ cīvaraṃ, tadupabhuñjako ca puggalo,',
                'thai': 'สิ่งเหล่านี้คือจีวร, และคนผู้ใช้สอยจีวรนั้น,',
                'paiboon': 'sìŋ lào níi kʉʉ jii-wɔɔn, lɛ́ kon pûu chái sɔ̌ɔy jii-wɔɔn nán,',
                'english': 'that is to say, this robe, and the person who makes use of it,',
            },
            # ‼ CHECK: Pali and Thai are printed run together with no space:
            #          ธาตุมัตตะโก,เป็นสักว่าธาตุตามธรรมชาติ,. I split them at
            #          the comma into layers 1 and 3. The same run-together
            #          occurs at verses 12, 21 and 30.
            {
                'number': 3,
                'pali': 'ธาตุมัตตะโก,',
                'pali_roman': 'dhātumattako,',
                'thai': 'เป็นสักว่าธาตุตามธรรมชาติ,',
                'paiboon': 'bpen sàk wâa tâat dtaam tam-má-châat,',
                'english': 'are merely elements after the manner of nature,',
            },
            {
                'number': 4,
                'pali': 'นิสสัตโต,',
                'pali_roman': 'nissatto,',
                'thai': 'มิได้เป็นสัตวะอันยั่งยืน,',
                'paiboon': 'mí dâai bpen sàt-dtà-wá an yâŋ-yʉʉn,',
                'english': 'not an enduring being,',
            },
            # ‼ CORRECTED: thai  ชีวะ อันเป็น → ชีวะอันเป็น. Stray space closed
            #              up; verses 14, 23 and 32 print ชีวะอันเป็น. Verify
            #              against the printed page.
            {
                'number': 5,
                'pali': 'นิชชีโว,',
                'pali_roman': 'nijjīvo,',
                'thai': 'มิได้เป็นชีวะอันเป็นบุรุษบุคคล,',
                'paiboon': 'mí dâai bpen chii-wá an bpen bù-rùt bùk-kon,',
                'english': 'not a soul that is a man or an individual,',
            },
            {
                'number': 6,
                'pali': 'สุญโญ,',
                'pali_roman': 'suñño,',
                'thai': 'ว่างเปล่าจากความหมายแห่งความเป็นตัวตน,',
                'paiboon': 'wâaŋ bplào jàak kwaam-mǎai hɛ̀ŋ kwaam bpen dtua dton,',
                'english': 'empty of all meaning of selfhood,',
            },
            {
                'number': 7,
                'pali': 'สัพพานิ ปะนะ อิมานิ จีวะรานิ อะชิคุจฉะนียานิ,',
                'pali_roman': 'sabbāni pana imāni cīvarāni ajigucchanīyāni,',
                'thai': 'ก็จีวรทั้งหมดนี้ ไม่เป็นของน่าเกลียดมาแต่เดิม,',
                'paiboon': 'gɔ̂ jii-wɔɔn táŋ-mòt níi mâi bpen kɔ̌ɔŋ nâa glìat maa dtɛ̀ɛ dəəm,',
                'english': 'and all these robes are not from the first things of repulsiveness,',
            },
            # ‼ CORRECTED: pali  ปิต์วา → ปัตวา. ปิต์วา is a slip for ปัตวา;
            #              verses 17, 26 and 35 print ปัตวา, as do standard
            #              editions. Verify against the printed page.
            # ‼ CORRECTED: pali_roman  pitvā → patvā. Follows the ปัตวา
            #              correction. Verify against the printed page.
            {
                'number': 8,
                'pali': 'อิมัง ปูติกายัง ปัตวา',
                'pali_roman': 'imaṃ pūtikāyaṃ patvā',
                'thai': 'ครั้นมาถูกเข้ากับกายอันเน่าอยู่เป็นนิจนี้แล้ว,',
                'paiboon': 'krán maa tùuk kâo gàp gaai an nâo yùu bpen nít níi lɛ́ɛo,',
                'english': 'but having come into contact with this body, which is perpetually foul,',
            },
            # ‼ CHECK: Ends with a comma and no ฯ, where the parallel closing
            #          lines at verses 18 and 27 end with ฯ. The Thai line
            #          likewise carries no closing punctuation.
            {
                'number': 9,
                'pali': 'อะติวิยะ ชิคุจฉะนียานิ ชายันติ,',
                'pali_roman': 'ativiya jigucchanīyāni jāyanti,',
                'thai': 'ย่อมกลายเป็นของน่าเกลียดอย่างยิ่งไปด้วยกัน',
                'paiboon': 'yɔ̂m glaai bpen kɔ̌ɔŋ nâa glìat yàaŋ-yîŋ bpai dûay-gan',
                'english': 'they too become exceedingly repulsive.',
            },
            # ‼ CHECK: Thai ends with a full stop (เนืองนิจ.) where the
            #          parallel lines end with a comma. Reproduced as pasted.
            {
                'section': 'ขณะรับบิณฑบาต: While Receiving Almsfood',
                'number': 10,
                'pali': 'ยะถาปัจจะยัง ปะวัตตะมานัง ธาตุมัตตะเมเวตัง,',
                'pali_roman': 'yathāpaccayaṃ pavattamānaṃ dhātumattamevetaṃ,',
                'thai': 'สิ่งเหล่านี้ นี่เป็นสักว่าธาตุตามธรรมชาติเท่านั้น, กำลังเป็นไปตามเหตุตามปัจจัยอยู่เนืองนิจ.',
                'paiboon': 'sìŋ lào níi nîi bpen sàk wâa tâat dtaam tam-má-châat tâo-nán, gam-laŋ bpen bpai dtaam hèet dtaam bpàt-jai yùu nʉaŋ nít.',
                'english': 'These things here are merely elements after the manner of nature, proceeding continually according to their causes and conditions.',
            },
            # ‼ CHECK: Thai reads คือบิณฑบาต และคน with no comma after บิณฑบาต,
            #          where verses 2 and 20 place a comma there. Reproduced as
            #          pasted.
            {
                'number': 11,
                'pali': 'ยะทิทัง ปิณฑะปาโต, ตะทุปะภุญชะโก จะ ปุคคะโล,',
                'pali_roman': 'yadidaṃ piṇḍapāto, tadupabhuñjako ca puggalo,',
                'thai': 'สิ่งเหล่านี้คือบิณฑบาต และคนบริโภคบิณฑบาตนั้น,',
                'paiboon': 'sìŋ lào níi kʉʉ bin-tá-bàat lɛ́ kon bɔɔ-rí-pôok bin-tá-bàat nán,',
                'english': 'that is to say, this almsfood, and the person who consumes it,',
            },
            {
                'number': 12,
                'pali': 'ธาตุมัตตะโก,',
                'pali_roman': 'dhātumattako,',
                'thai': 'เป็นสักว่าธาตุตามธรรมชาติ,',
                'paiboon': 'bpen sàk wâa tâat dtaam tam-má-châat,',
                'english': 'are merely elements after the manner of nature,',
            },
            {
                'number': 13,
                'pali': 'นิสสัตโต,',
                'pali_roman': 'nissatto,',
                'thai': 'มิได้เป็นสัตวะอันยั่งยืน,',
                'paiboon': 'mí dâai bpen sàt-dtà-wá an yâŋ-yʉʉn,',
                'english': 'not an enduring being,',
            },
            {
                'number': 14,
                'pali': 'นิชชีโว,',
                'pali_roman': 'nijjīvo,',
                'thai': 'มิได้เป็นชีวะอันเป็นบุรุษบุคคล,',
                'paiboon': 'mí dâai bpen chii-wá an bpen bù-rùt bùk-kon,',
                'english': 'not a soul that is a man or an individual,',
            },
            {
                'number': 15,
                'pali': 'สุญโญ,',
                'pali_roman': 'suñño,',
                'thai': 'ว่างเปล่าจากความหมายแห่งความเป็นตัวตน,',
                'paiboon': 'wâaŋ bplào jàak kwaam-mǎai hɛ̀ŋ kwaam bpen dtua dton,',
                'english': 'empty of all meaning of selfhood,',
            },
            {
                'number': 16,
                'pali': 'สัพโพ ปะนายัง ปิณฑะปาโต อะชิคุจฉะนีโย,',
                'pali_roman': 'sabbo panāyaṃ piṇḍapāto ajigucchanīyo,',
                'thai': 'ก็บิณฑบาตทั้งหมดนี้ ไม่เป็นของน่าเกลียดมาแต่เดิม,',
                'paiboon': 'gɔ̂ bin-tá-bàat táŋ-mòt níi mâi bpen kɔ̌ɔŋ nâa glìat maa dtɛ̀ɛ dəəm,',
                'english': 'and all this almsfood is not from the first a thing of repulsiveness,',
            },
            # ‼ CHECK: Pali and Thai are printed run together with no space:
            #          ปัตวา,ครั้นมาถูกเข้า. I split them at the comma. The
            #          same run-together occurs at verse 35.
            {
                'number': 17,
                'pali': 'อิมัง ปูติกายัง ปัตวา,',
                'pali_roman': 'imaṃ pūtikāyaṃ patvā,',
                'thai': 'ครั้นมาถูกเข้ากับกายอันเน่าอยู่เป็นนิจนี้แล้ว,',
                'paiboon': 'krán maa tùuk kâo gàp gaai an nâo yùu bpen nít níi lɛ́ɛo,',
                'english': 'but having come into contact with this body, which is perpetually foul,',
            },
            # ‼ CHECK: The ฯ at the end of the Pali line has been rendered as a
            #          full stop in pali_roman, since IAST has no equivalent
            #          mark. Same treatment at verse 27.
            {
                'number': 18,
                'pali': 'อะติวิยะ ชิคุจฉะนีโย ชายะติ ฯ',
                'pali_roman': 'ativiya jigucchanīyo jāyati.',
                'thai': 'ย่อมกลายเป็นของน่าเกลียดอย่างยิ่งไปด้วยกัน',
                'paiboon': 'yɔ̂m glaai bpen kɔ̌ɔŋ nâa glìat yàaŋ-yîŋ bpai dûay-gan',
                'english': 'it too becomes exceedingly repulsive.',
            },
            # ‼ CHECK: Thai lacks the comma after เท่านั้น and has no closing
            #          punctuation at all, unlike the parallel lines at verses
            #          1, 10 and 28. Reproduced as pasted.
            {
                'section': 'ขณะรับเสนาสนะ: While Receiving Lodging',
                'number': 19,
                'pali': 'ยะถาปัจจะยัง ปะวัตตะมานัง ธาตุมัตตะเมเวตัง,',
                'pali_roman': 'yathāpaccayaṃ pavattamānaṃ dhātumattamevetaṃ,',
                'thai': 'สิ่งเหล่านี้ นี่เป็นสักว่าธาตุตามธรรมชาติเท่านั้น กำลังเป็นไปตามเหตุตามปัจจัยอยู่เนืองนิจ',
                'paiboon': 'sìŋ lào níi nîi bpen sàk wâa tâat dtaam tam-má-châat tâo-nán gam-laŋ bpen bpai dtaam hèet dtaam bpàt-jai yùu nʉaŋ nít',
                'english': 'These things here are merely elements after the manner of nature, proceeding continually according to their causes and conditions,',
            },
            # ‼ CHECK: Pali reads ยะทิทัง เสนาสะนัง ตะทุปะภุญชะโก with no comma
            #          after เสนาสะนัง, where verses 2 and 29 have one.
            #          Reproduced as pasted.
            {
                'number': 20,
                'pali': 'ยะทิทัง เสนาสะนัง ตะทุปะภุญชะโก จะ ปุคคะโล,',
                'pali_roman': 'yadidaṃ senāsanaṃ tadupabhuñjako ca puggalo,',
                'thai': 'สิ่งเหล่านี้คือเสนาสนะ, และบุคคลผู้ใช้สอยเสนาสนะนั้น,',
                'paiboon': 'sìŋ lào níi kʉʉ sěe-naa-sà-ná, lɛ́ bùk-kon pûu chái sɔ̌ɔy sěe-naa-sà-ná nán,',
                'english': 'that is to say, this lodging, and the person who makes use of it,',
            },
            {
                'number': 21,
                'pali': 'ธาตุมัตตะโก,',
                'pali_roman': 'dhātumattako,',
                'thai': 'เป็นสักว่าธาตุตามธรรมชาติ,',
                'paiboon': 'bpen sàk wâa tâat dtaam tam-má-châat,',
                'english': 'are merely elements after the manner of nature,',
            },
            # ‼ CORRECTED: thai  มีได้ → มิได้. มีได้ is a slip for มิได้ "is
            #              not"; verses 4, 13 and 31 print มิได้. Verify
            #              against the printed page.
            # ‼ CORRECTED: paiboon  mii dâai → mí dâai. Follows the มิได้
            #              correction. Verify against the printed page.
            {
                'number': 22,
                'pali': 'นิสสัตโต,',
                'pali_roman': 'nissatto,',
                'thai': 'มิได้เป็นสัตวะอันยั่งยืน,',
                'paiboon': 'mí dâai bpen sàt-dtà-wá an yâŋ-yʉʉn,',
                'english': 'not an enduring being,',
            },
            {
                'number': 23,
                'pali': 'นิชชีโว,',
                'pali_roman': 'nijjīvo,',
                'thai': 'มิได้เป็นชีวะอันเป็นบุรุษบุคคล,',
                'paiboon': 'mí dâai bpen chii-wá an bpen bù-rùt bùk-kon,',
                'english': 'not a soul that is a man or an individual,',
            },
            {
                'number': 24,
                'pali': 'สุญโญ,',
                'pali_roman': 'suñño,',
                'thai': 'ว่างเปล่าจากความหมายแห่งความเป็นตัวตน,',
                'paiboon': 'wâaŋ bplào jàak kwaam-mǎai hɛ̀ŋ kwaam bpen dtua dton,',
                'english': 'empty of all meaning of selfhood,',
            },
            {
                'number': 25,
                'pali': 'สัพพานิ ปะนะ อิมานิ เสนาสะนานิ อะชิคุจฉะนียานิ,',
                'pali_roman': 'sabbāni pana imāni senāsanāni ajigucchanīyāni,',
                'thai': 'ก็เสนาสนะทั้งหมดนี้ ไม่เป็นของน่าเกลียดมาแต่เดิม,',
                'paiboon': 'gɔ̂ sěe-naa-sà-ná táŋ-mòt níi mâi bpen kɔ̌ɔŋ nâa glìat maa dtɛ̀ɛ dəəm,',
                'english': 'and all these lodgings are not from the first things of repulsiveness,',
            },
            # ‼ CHECK: The source breaks this line as อิมัง / ปูติกายัง ปัตวา,
            #          across two lines. I joined it with a single space;
            #          confirm the book prints it as one line.
            {
                'number': 26,
                'pali': 'อิมัง ปูติกายัง ปัตวา,',
                'pali_roman': 'imaṃ pūtikāyaṃ patvā,',
                'thai': 'ครั้นมาถูกเข้ากับกายอันเน่าอยู่เป็นนิจนี้แล้ว,',
                'paiboon': 'krán maa tùuk kâo gàp gaai an nâo yùu bpen nít níi lɛ́ɛo,',
                'english': 'but having come into contact with this body, which is perpetually foul,',
            },
            {
                'number': 27,
                'pali': 'อะติวิยะ ชิคุจฉะนียานิ ชายันติ ฯ',
                'pali_roman': 'ativiya jigucchanīyāni jāyanti.',
                'thai': 'ย่อมกลายเป็นของน่าเกลียดอย่างยิ่งไปด้วยกัน',
                'paiboon': 'yɔ̂m glaai bpen kɔ̌ɔŋ nâa glìat yàaŋ-yîŋ bpai dûay-gan',
                'english': 'they too become exceedingly repulsive.',
            },
            # ‼ CHECK: Thai has เนื่องนิจ again, matching verse 1 but differing
            #          from verses 10 and 19. Reproduced as pasted.
            # ‼ CORRECTED: thai  เนื่องนิจ → เนืองนิจ. Same slip as verse 1.
            #              Verify against the printed page.
            # ‼ CORRECTED: paiboon  nʉ̂aŋ nít → nʉaŋ nít. Follows the เนืองนิจ
            #              correction. Verify against the printed page.
            {
                'section': 'ขณะรับคิลานเภสัช: While Receiving Medicinal Support',
                'number': 28,
                'pali': 'ยะถาปัจจะยัง ปะวัตตะมานัง ธาตุมัตตะเมเวตัง,',
                'pali_roman': 'yathāpaccayaṃ pavattamānaṃ dhātumattamevetaṃ,',
                'thai': 'สิ่งเหล่านี้ นี่เป็นสักว่าธาตุตามธรรมชาติเท่านั้น, กำลังเป็นไปตามเหตุตามปัจจัยอยู่เนืองนิจ,',
                'paiboon': 'sìŋ lào níi nîi bpen sàk wâa tâat dtaam tam-má-châat tâo-nán, gam-laŋ bpen bpai dtaam hèet dtaam bpàt-jai yùu nʉaŋ nít,',
                'english': 'These things here are merely elements after the manner of nature, proceeding continually according to their causes and conditions,',
            },
            # ‼ CORRECTED: thai  เภสัชบริบาร → เภสัชบริขาร. บริบาร is a slip
            #              for บริขาร (parikkhāra, "requisite"). Verify against
            #              the printed page.
            # ‼ CORRECTED: thai  เภสัชบริชาร → เภสัชบริขาร. บริชาร is a second,
            #              different slip for บริขาร in the same line. Verify
            #              against the printed page.
            # ‼ CORRECTED: paiboon  bɔɔ-rí-baan → bɔɔ-rí-kǎan. Follows the
            #              บริขาร correction. Verify against the printed page.
            # ‼ CORRECTED: paiboon  bɔɔ-rí-chaan → bɔɔ-rí-kǎan. Follows the
            #              บริขาร correction. Verify against the printed page.
            {
                'number': 29,
                'pali': 'ยะทิทัง คิลานะปัจจะยะเภสัชชะปะริกขาโร, ตะทุปะภุญชะโก จะ ปุคคะโล,',
                'pali_roman': 'yadidaṃ gilānapaccayabhesajjaparikkhāro, tadupabhuñjako ca puggalo,',
                'thai': 'สิ่งเหล่านี้คือเภสัชบริขารอันเกื้อกูลแก่คนไข้, และคนผู้บริโภคเภสัชบริขารนั้น,',
                'paiboon': 'sìŋ lào níi kʉʉ pee-sàt bɔɔ-rí-kǎan an gʉ̂a-guun gɛ̀ɛ kon-kâi, lɛ́ kon pûu bɔɔ-rí-pôok pee-sàt bɔɔ-rí-kǎan nán,',
                'english': 'that is to say, this medicinal requisite that supports the sick, and the person who makes use of it,',
            },
            {
                'number': 30,
                'pali': 'ธาตุมัตตะโก,',
                'pali_roman': 'dhātumattako,',
                'thai': 'เป็นสักว่าธาตุตามธรรมชาติ,',
                'paiboon': 'bpen sàk wâa tâat dtaam tam-má-châat,',
                'english': 'are merely elements after the manner of nature,',
            },
            {
                'number': 31,
                'pali': 'นิสสัตโต,',
                'pali_roman': 'nissatto,',
                'thai': 'มิได้เป็นสัตวะอันยั่งยืน,',
                'paiboon': 'mí dâai bpen sàt-dtà-wá an yâŋ-yʉʉn,',
                'english': 'not an enduring being,',
            },
            {
                'number': 32,
                'pali': 'นิชชีโว,',
                'pali_roman': 'nijjīvo,',
                'thai': 'มิได้เป็นชีวะอันเป็นบุรุษบุคคล,',
                'paiboon': 'mí dâai bpen chii-wá an bpen bù-rùt bùk-kon,',
                'english': 'not a soul that is a man or an individual,',
            },
            {
                'number': 33,
                'pali': 'สุญโญ,',
                'pali_roman': 'suñño,',
                'thai': 'ว่างเปล่าจากความหมายแห่งความเป็นตัวตน,',
                'paiboon': 'wâaŋ bplào jàak kwaam-mǎai hɛ̀ŋ kwaam bpen dtua dton,',
                'english': 'empty of all meaning of selfhood,',
            },
            # ‼ CORRECTED: thai  คิลานเภสัชบริการ → คิลานเภสัชบริขาร. บริการ
            #              ("service") is a slip for บริขาร (parikkhāra); the
            #              Pali line reads ปะริกขาโร. Verify against the
            #              printed page.
            # ‼ CORRECTED: paiboon  bɔɔ-rí-gaan → bɔɔ-rí-kǎan. Follows the
            #              บริขาร correction. Verify against the printed page.
            {
                'number': 34,
                'pali': 'สัพโพ ปะนายัง คิลานะปัจจะยะเภสัชชะปะริกขาโร อะชิคุจฉะนีโย,',
                'pali_roman': 'sabbo panāyaṃ gilānapaccayabhesajjaparikkhāro ajigucchanīyo,',
                'thai': 'ก็คิลานเภสัชบริขารทั้งหมดนี้ ไม่เป็นของน่าเกลียดมาแต่เดิม,',
                'paiboon': 'gɔ̂ kí-laa-ná-pee-sàt bɔɔ-rí-kǎan táŋ-mòt níi mâi bpen kɔ̌ɔŋ nâa glìat maa dtɛ̀ɛ dəəm,',
                'english': 'and all this medicinal support is not from the first a thing of repulsiveness,',
            },
            {
                'number': 35,
                'pali': 'อิมัง ปูติกายัง ปัตวา,',
                'pali_roman': 'imaṃ pūtikāyaṃ patvā,',
                'thai': 'ครั้นมาถูกเข้ากับกายอันเน่าอยู่เป็นนิจนี้แล้ว,',
                'paiboon': 'krán maa tùuk kâo gàp gaai an nâo yùu bpen nít níi lɛ́ɛo,',
                'english': 'but having come into contact with this body, which is perpetually foul,',
            },
            # ‼ CHECK: Ends with a comma rather than ฯ, unlike verses 18 and
            #          27, and the Thai adds ดังนี้ which the other three
            #          movements do not have. Both reproduced as pasted.
            {
                'number': 36,
                'pali': 'อะติวิยะ ชิคุจฉะนีโย ชายะติ,',
                'pali_roman': 'ativiya jigucchanīyo jāyati,',
                'thai': 'ย่อมกลายเป็นของน่าเกลียดอย่างยิ่งไปด้วยกัน ดังนี้,',
                'paiboon': 'yɔ̂m glaai bpen kɔ̌ɔŋ nâa glìat yàaŋ-yîŋ bpai dûay-gan daŋ-níi,',
                'english': 'it too becomes exceedingly repulsive. So it is.',
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — Pali only. Every thai and paiboon field is empty. I have
        #          not supplied a translation from memory. This is the third
        #          consecutive chant in this state.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It carries no
        #          authority from the source and should be treated as
        #          provisional.
        # ‼ CHECK: No invitation line is present. I have not written one.
        #          Confirm the book prints none.
        # ‼ CHECK: The book prints no section headings. All six sections and
        #          their names are my grouping by subject, not the book's.
        # ‼ CHECK: The heading is numbered 9. in the source, taken as the
        #          book's chant number and left out of title_thai, as with
        #          chants 7 and 8.

        'id': 'tilakkhanadi-gatha',
        'title_thai': 'ติลักขะณาทิคาถา',
        'title_pali': 'Tilakkhaṇādigāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses on the Three Characteristics and Others',
        'source': 'ขุ.ขุ. 25/89, ขุ.อุ. 25/221',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "Verses on the three characteristics, the few who cross to the far "
            "shore, the abandoning of the dark for the bright, and those "
            "wholly quenched in the world."
        ),

        'when_chanted': (
            "Chanted among the daily reflections, and often as the Pali "
            "counterpart to the vernacular reflection on conditioned things."
        ),

        'background': [
            "The title names the three characteristics first and then adds "
            "ādi, and others — the book is signalling that this is a "
            "compilation rather than a single passage. The opening three "
            "stanzas give the triple formula in its canonical verse form; what "
            "follows moves through several further subjects, each complete in "
            "itself.",

            "This is the Pali of which บทพิจารณาสังขาร gives the opening in "
            "Thai. A reader working through the book will meet the same three "
            "lines twice: once glossed at length in the vernacular for "
            "reflection, and once here in metre for chanting. The footnote "
            "points to two places in the Khuddaka Nikāya.",

            "The book prints no Thai rendering for this chant, so it stands at "
            "two of the five layers: the Pali as it is chanted, and a working "
            "English translation supplied for this edition rather than taken "
            "from the book.",
        ],

        'meaning': [
            "The first movement states each characteristic in turn and then "
            "repeats an identical refrain: when one sees this with wisdom, one "
            "turns away from suffering; this is the path to purity. The "
            "repetition is the point. Nothing is added by the second and third "
            "statements except the substitution of one word, and the reciter "
            "arrives three times at the same door.",

            "The second movement changes the image to a crossing. Few among "
            "men reach the far shore; the rest of this generation runs up and "
            "down along the near bank. Those who follow the Dhamma in the "
            "Dhamma rightly declared are the ones who will cross beyond the "
            "realm of death, so very hard to cross. The verse offers no method "
            "here, only a division between those who go and those who circle.",

            "The third movement gives the instruction. Abandoning the dark "
            "state, let the wise develop the bright; coming from home to "
            "homelessness, in seclusion where delight is hard to find. The "
            "Pali is candid about the difficulty — the place where one should "
            "seek delight is precisely the place where delight does not "
            "naturally arise. Having left sensual pleasures and owning "
            "nothing, one cleanses oneself of the defilements of mind.",

            "The closing stanza describes the finished work rather than "
            "prescribing it. Those whose minds are rightly developed in the "
            "factors of awakening, who delight in the relinquishing of "
            "grasping without clinging, whose taints are destroyed and who are "
            "radiant — they are wholly quenched in the world. The verse ends "
            "not with an instruction but with a state, and the chant closes "
            "there.",
        ],

        # The book prints no invitation line, so every field stays
        # empty; the template checks `invitation.pali` and skips it.
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },

        'verses': [
            # ‼ CHECK: The first three stanzas are printed with blank lines
            #          after their first and third lines, so each four-line
            #          stanza appears as two pairs. This spacing does not occur
            #          in stanzas 4 onward. Reproduced by keeping the lines as
            #          separate verses; check whether the book sets these
            #          stanzas differently from the rest.
            {
                'section': 'ติลักขะณะ: The Three Characteristics',
                'number': 1,
                'pali': 'สัพเพ สังขารา อะนิจจาติ',
                'pali_roman': 'sabbe saṅkhārā aniccāti',
                'thai': '',
                'paiboon': '',
                'english': 'All conditioned things are impermanent —',
            },
            {
                'number': 2,
                'pali': 'ยะทา ปัญญายะ ปัสสะติ',
                'pali_roman': 'yadā paññāya passati',
                'thai': '',
                'paiboon': '',
                'english': 'when one sees this with wisdom,',
            },
            {
                'number': 3,
                'pali': 'อะถะ นิพพินทะติ ทุกเข',
                'pali_roman': 'atha nibbindati dukkhe',
                'thai': '',
                'paiboon': '',
                'english': 'then one turns away from suffering.',
            },
            {
                'number': 4,
                'pali': 'เอสะ มัคโค วิสุทธิยา.',
                'pali_roman': 'esa maggo visuddhiyā.',
                'thai': '',
                'paiboon': '',
                'english': 'This is the path to purity.',
            },
            {
                'number': 5,
                'pali': 'สัพเพ สังขารา ทุกขาติ',
                'pali_roman': 'sabbe saṅkhārā dukkhāti',
                'thai': '',
                'paiboon': '',
                'english': 'All conditioned things are suffering —',
            },
            {
                'number': 6,
                'pali': 'ยะทา ปัญญายะ ปัสสะติ',
                'pali_roman': 'yadā paññāya passati',
                'thai': '',
                'paiboon': '',
                'english': 'when one sees this with wisdom,',
            },
            {
                'number': 7,
                'pali': 'อะถะ นิพพินทะติ ทุกเข',
                'pali_roman': 'atha nibbindati dukkhe',
                'thai': '',
                'paiboon': '',
                'english': 'then one turns away from suffering.',
            },
            {
                'number': 8,
                'pali': 'เอสะ มัคโค วิสุทธิยา.',
                'pali_roman': 'esa maggo visuddhiyā.',
                'thai': '',
                'paiboon': '',
                'english': 'This is the path to purity.',
            },
            {
                'number': 9,
                'pali': 'สัพเพ ธัมมา อะนัตตาติ',
                'pali_roman': 'sabbe dhammā anattāti',
                'thai': '',
                'paiboon': '',
                'english': 'All things are not-self —',
            },
            # ‼ CHECK: The footnote 1. ขุ.ขุ. 25/89, ขุ.อุ. 25/221 is printed
            #          between this line and the next, in the middle of the
            #          third stanza. I read it as a page-foot footnote falling
            #          at a page break and kept it out of the verses, placing
            #          it in the source field. Verify that it belongs to this
            #          chant and not to a neighbouring one, and check which
            #          line carries the footnote marker.
            {
                'number': 10,
                'pali': 'ยะทา ปัญญายะ ปัสสะติ',
                'pali_roman': 'yadā paññāya passati',
                'thai': '',
                'paiboon': '',
                'english': 'when one sees this with wisdom,',
            },
            # ‼ CHECK: The refrain reads ทุกเข in all three stanzas, including
            #          the anattā stanza. Consistent within this text and
            #          standard, but worth confirming against the page since it
            #          is the line most often mis-set.
            {
                'number': 11,
                'pali': 'อะถะ นิพพินทะติ ทุกเข',
                'pali_roman': 'atha nibbindati dukkhe',
                'thai': '',
                'paiboon': '',
                'english': 'then one turns away from suffering.',
            },
            {
                'number': 12,
                'pali': 'เอสะ มัคโค วิสุทธิยา.',
                'pali_roman': 'esa maggo visuddhiyā.',
                'thai': '',
                'paiboon': '',
                'english': 'This is the path to purity.',
            },
            {
                'section': 'ปาระคามิโน: Those Who Go Beyond',
                'number': 13,
                'pali': 'อัปปะกา เต มะนุสเสสุ',
                'pali_roman': 'appakā te manussesu',
                'thai': '',
                'paiboon': '',
                'english': 'Few are they among men,',
            },
            {
                'number': 14,
                'pali': 'เย ชะนา ปาระคามิโน',
                'pali_roman': 'ye janā pāragāmino',
                'thai': '',
                'paiboon': '',
                'english': 'those people who go to the far shore;',
            },
            {
                'number': 15,
                'pali': 'อะถายัง อิตะรา ปะชา',
                'pali_roman': 'athāyaṃ itarā pajā',
                'thai': '',
                'paiboon': '',
                'english': 'while the rest of this generation',
            },
            {
                'number': 16,
                'pali': 'ตีระเมวานุธาวะติ.',
                'pali_roman': 'tīramevānudhāvati.',
                'thai': '',
                'paiboon': '',
                'english': 'runs up and down along the near bank.',
            },
            {
                'number': 17,
                'pali': 'เย จะ โข สัมมะทักขาเต',
                'pali_roman': 'ye ca kho sammadakkhāte',
                'thai': '',
                'paiboon': '',
                'english': 'But those who, in the Dhamma rightly declared,',
            },
            {
                'number': 18,
                'pali': 'ธัมเม ธัมมานุวัตติโน',
                'pali_roman': 'dhamme dhammānuvattino',
                'thai': '',
                'paiboon': '',
                'english': 'live in accordance with that Dhamma —',
            },
            {
                'number': 19,
                'pali': 'เต ชะนา ปาระเมสสันติ',
                'pali_roman': 'te janā pāramessanti',
                'thai': '',
                'paiboon': '',
                'english': 'those people will reach the far shore,',
            },
            {
                'number': 20,
                'pali': 'มัจจุเธยยัง สุทุตตะรัง.',
                'pali_roman': 'maccudheyyaṃ suduttaraṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'crossing the realm of death, so hard to cross.',
            },
            {
                'section': 'กัณหัง ธัมมัง: The Dark and the Bright',
                'number': 21,
                'pali': 'กัณหัง ธัมมัง วิปปะหายะ',
                'pali_roman': 'kaṇhaṃ dhammaṃ vippahāya',
                'thai': '',
                'paiboon': '',
                'english': 'Abandoning the dark state,',
            },
            {
                'number': 22,
                'pali': 'สุกกัง ภาเวถะ ปัณฑิโต',
                'pali_roman': 'sukkaṃ bhāvetha paṇḍito',
                'thai': '',
                'paiboon': '',
                'english': 'let the wise one develop the bright;',
            },
            {
                'number': 23,
                'pali': 'โอกา อะโนกะมาคัมมะ',
                'pali_roman': 'okā anokamāgamma',
                'thai': '',
                'paiboon': '',
                'english': 'coming from home to homelessness,',
            },
            # ‼ CHECK: วิเวเก ยัตถะ ทูระมัง — ทูระมัง transliterated faithfully
            #          as dūramaṃ. Some editions read ทูระมา or set the word
            #          differently. I kept the printed form rather than
            #          substituting.
            {
                'number': 24,
                'pali': 'วิเวเก ยัตถะ ทูระมัง.',
                'pali_roman': 'viveke yattha dūramaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'into seclusion, where delight is hard to find.',
            },
            {
                'section': 'ปะริโยทะเปยยะ อัตตานัง: The Cleansing of the Mind',
                'number': 25,
                'pali': 'ตัตราภิระติมิจเฉยยะ',
                'pali_roman': 'tatrābhiratimiccheyya',
                'thai': '',
                'paiboon': '',
                'english': 'There let him seek his delight,',
            },
            # ‼ CHECK: หิต์วา carries thanthakhat over ต์. Transliterated
            #          faithfully as hitvā.
            {
                'number': 26,
                'pali': 'หิต์วา กาเม อะกิญจะโน',
                'pali_roman': 'hitvā kāme akiñcano',
                'thai': '',
                'paiboon': '',
                'english': 'having left sensual pleasures, owning nothing;',
            },
            {
                'number': 27,
                'pali': 'ปะริโยทะเปยยะ อัตตานัง',
                'pali_roman': 'pariyodapeyya attānaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'let the wise one cleanse himself',
            },
            # ‼ CHECK: จิตตักเลเสหิ transliterated faithfully as cittaklesehi.
            #          Some editions read cittakilesehi with the vowel present.
            #          I kept the printed form.
            {
                'number': 28,
                'pali': 'จิตตักเลเสหิ ปัณฑิโต.',
                'pali_roman': 'cittaklesehi paṇḍito.',
                'thai': '',
                'paiboon': '',
                'english': 'of the defilements of the mind.',
            },
            {
                'section': 'สัมโพธิยังคะ: The Factors of Awakening',
                'number': 29,
                'pali': 'เยสัง สัมโพธิยังเคสุ',
                'pali_roman': 'yesaṃ sambodhiyaṅgesu',
                'thai': '',
                'paiboon': '',
                'english': 'Those whose minds, in the factors of awakening,',
            },
            {
                'number': 30,
                'pali': 'สัมมา จิตตัง สุภาวิตัง',
                'pali_roman': 'sammā cittaṃ subhāvitaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'are rightly and well developed;',
            },
            {
                'number': 31,
                'pali': 'อาทานะปะฏินิสสัคเค',
                'pali_roman': 'ādānapaṭinissagge',
                'thai': '',
                'paiboon': '',
                'english': 'who in the relinquishing of grasping,',
            },
            # ‼ CHECK: The final stanza runs to six lines where every other
            #          stanza in the chant has four. Reproduced as pasted; this
            #          may be two stanzas set without a break, or a genuine
            #          six-line unit. My section covers all six.
            {
                'number': 32,
                'pali': 'อะนุปาทายะ เย ระตา',
                'pali_roman': 'anupādāya ye ratā',
                'thai': '',
                'paiboon': '',
                'english': 'without clinging, take delight —',
            },
            {
                'number': 33,
                'pali': 'ขีณาสะวา ชุติมันโต',
                'pali_roman': 'khīṇāsavā jutimanto',
                'thai': '',
                'paiboon': '',
                'english': 'with taints destroyed, radiant,',
            },
            # ‼ CORRECTED: pali  ปะรินิพพุตาติ.' → ปะรินิพพุตาติ.. Stray
            #              apostrophe after the full stop removed (an OCR
            #              artefact). Verify against the printed page.
            # ‼ CORRECTED: pali_roman  parinibbutāti.' → parinibbutāti..
            #              Follows the apostrophe removal. Verify against the
            #              printed page.
            {
                'number': 34,
                'pali': 'เต โลเก ปะรินิพพุตาติ.',
                'pali_roman': 'te loke parinibbutāti.',
                'thai': '',
                'paiboon': '',
                'english': 'they are wholly quenched in the world.',
            },
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 35,
                'pali': 'ติลักขะณาทิคาถา นิฏฐิตา.',
                'pali_roman': 'tilakkhaṇādigāthā niṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': 'The verses on the three characteristics and others are ended.',
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
