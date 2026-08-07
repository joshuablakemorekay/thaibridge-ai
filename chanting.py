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
  * `page_start`        — the page this chant begins on in the physical book.
                          A monk calls out a page number, so this is how a
                          reader finds the chant he means; it shows on the
                          closed index card. Optional: a chant without it
                          renders exactly as before.
  * `when_chanted`      — when is it chanted in Theravāda practice?
  * `background`        — why was it taught? The historical setting, or the
                          origin of the chant if it was composed later.
  * `meaning`           — what does it mean, and why is it still chanted?
  * `invitation` + `verses`
                        — how do I chant it?

`background` and `meaning` are LISTS of paragraphs rather than one long string,
so the page and a printed edition can space them the same way without either
one having to split text apart.

Four keys are optional and describe how the PRINTED page sets a chant. They
exist so the page-by-page view can show a page as the book prints it, and they
are all absent from the chants entered before that view existed:

  * `page_start`      — see above.
  * `layout`          — 'prose' where the book runs the chant together as a
                        continuous passage rather than a set of lines (an
                        Abhidhamma mātikā, say). Absent means lines, which is
                        what every chant here is so far. In book layout a
                        'prose' chant flows back into one justified block; in
                        verse-by-verse it reads as numbered units like any
                        other, which is the point of having both.
  * `closing`         — the formula the book prints under a finished chant
                        (จบ…, "here ends…"), same five layers as a verse.
  * `source_printed`  — the canonical reference AS THE BOOK PRINTS IT, from
                        the page's own footnotes (e.g. 'อภิ.ยม. ๓๘/๑'). This
                        is the book citing itself, and it is worth keeping
                        separate from `source`: `source` may have been written
                        for this app, `source_printed` never is.

A page may print a chant with a Thai translation, in Pali only, or mix chants
of both kinds — so every layer below is written ONLY where the book gives it.
A Pali-only chant simply has no `thai`, and therefore no `paiboon`. Nothing
fills those in.

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
        # Named by the first word of its opening line, the way chants are
        # traditionally identified. Shortened to `Sabbe` on Josh's instruction;
        # verse 1 opens `Sabbe saṅkhārā aniccā`, so this is the opening word
        # rather than the whole opening line.
        'title_english': 'Reflection on Conditioned Phenomena (Sabbe)',
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
                'pali': 'มะระณะปะริโยสานัง เม ชีวิตัง',
                'pali_roman': 'Maraṇapariyosānaṃ me jīvitaṃ',
                'thai': 'ชีวิตของเรา มีความตายเป็นที่สุดรอบ',
                'paiboon': 'chii-wít kɔ̌ɔŋ rao mii kwaam-dtaai bpen tîi-sùt rɔ̂ɔp',
                'english': 'My life has death as its end.',
            },
            {
                'number': 8,
                'pali': 'ชีวิตัง เม อะนิยะตัง',
                'pali_roman': 'Jīvitaṃ me aniyataṃ',
                'thai': 'ชีวิตของเรา เป็นของไม่เที่ยง',
                'paiboon': 'chii-wít kɔ̌ɔŋ rao bpen kɔ̌ɔŋ mâi tîaŋ',
                'english': 'My life is uncertain.',
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

    {
        # ‼ CHECK: No invitation line is present in what you pasted. I have not
        #          written one. Confirm the book prints none.
        # ‼ CHECK: The book prints no section headings. The three sections and
        #          their names are my grouping by subject, not the book's; the
        #          third is a single line and could equally be run on to the
        #          second.
        # ‼ CHECK: source left empty. The book text you pasted gives no
        #          attribution and I have not supplied one. If the book prints
        #          a source line it needs adding by hand.
        # ‼ CHECK: The Thai line ธรรมที่ควรพิจารณาเนืองๆ under the heading is a
        #          subtitle, not part of the chant, so I placed it nowhere in
        #          the verses. Confirm the book sets it as a subtitle and not
        #          as a first line.
        # ‼ CHECK: The parenthesised forms อะนะตีตา, ทายาทา are the feminine
        #          alternatives, printed for a female reciter. I reproduced the
        #          parentheses in both the pali and pali_roman layers rather
        #          than resolving them. Check this is how you want alternatives
        #          handled in the app.

        'id': 'abhinha-paccavekkhana',
        'title_thai': 'อะภิณหะปัจจะเวกขะณะ',
        'title_pali': 'Abhiṇhapaccavekkhaṇa',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Subjects for Frequent Recollection',
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        'summary': (
            "Five things to be recollected constantly — ageing, sickness, "
            "death, separation from all that is dear, and ownership of one's "
            "own kamma."
        ),

        'when_chanted': (
            "Recited as part of the daily reflections, commonly in the evening "
            "chanting and by lay and monastic alike."
        ),

        'background': [
            "This is among the best known of the short reflections, given "
            "equally to lay people and to monastics, and the book gives it a "
            "Thai subtitle — ธรรมที่ควรพิจารณาเนืองๆ, the teachings that "
            "should be reflected upon frequently — which states its purpose "
            "plainly. The last line makes the instruction explicit: these are "
            "to be reflected upon in just this way, and often.",

            "The text carries a feature rare in a chanting book: alternative "
            "forms printed in parentheses. อะนะตีโต is the masculine form and "
            "อะนะตีตา the feminine, and likewise ทายาโท and ทายาทา. A reciter "
            "says whichever agrees with themselves. Their presence in the "
            "printed page is a sign that this reflection is meant to be spoken "
            "in the first person and meant honestly, not merely read.",
        ],

        'meaning': [
            "The first five subjects proceed by a single repeated "
            "construction: I am of such a nature, and I have not gone beyond "
            "it. Ageing, sickness and death are not presented as misfortunes "
            "that may arrive but as ธรรมดา — the ordinary way of things, what "
            "is normal. The Thai word does the same work as the Pali dhamma "
            "here: it names these not as intrusions upon life but as the "
            "constitution of it.",

            "The fifth subject shifts from the body to what surrounds it. "
            "นานาภาโว วินาภาโว — becoming otherwise, becoming separate — is "
            "rendered by the Thai as พลัดพรากจาก, to be parted from all that "
            "is loved and pleasing. The reflection does not ask the reciter to "
            "love less; it asks them to hold what they love in the knowledge "
            "that parting is already contained in the having.",

            "The sixth subject answers the first five. Where they describe "
            "what cannot be escaped, this one names what remains one's own: "
            "kamma as possession, inheritance, origin, kin and refuge. The "
            "construction is deliberate — each is a relationship one might "
            "otherwise claim with property, family or a protector, and each is "
            "here assigned to one's own action instead. The closing lines draw "
            "the consequence: whatever deed I do, fair or foul, of that I "
            "shall be the heir.",
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
            # ‼ CHECK: The Thai line ends with no punctuation, where the Pali
            #          ends with a comma. The same holds for every Thai line in
            #          this chant except verse 16. Reproduced as pasted.
            {
                'section': 'อะภิณหะปัจจะเวกขะณะ: The Five Recollections',
                'number': 1,
                'pali': 'ชะราธัมโมมหิ,',
                'pali_roman': 'jarādhammomhi,',
                'thai': 'เรามีความแก่เป็นธรรมดา',
                'paiboon': 'rao mii kwaam gɛ̀ɛ bpen tam-má-daa',
                'english': 'I am of the nature to age,',
            },
            {
                'number': 2,
                'pali': 'ชะรัง อะนะตีโต (อะนะตีตา),',
                'pali_roman': 'jaraṃ anatīto (anatītā),',
                'thai': 'จักล่วงพ้นความแก่ไปไม่ได้',
                'paiboon': 'jàk lûaŋ pón kwaam gɛ̀ɛ bpai mâi dâai',
                'english': 'I have not gone beyond ageing,',
            },
            # ‼ CHECK: Pali reads พ์ยาธิธัมโมมหิ with a thanthakhat over พ์. I
            #          transliterated faithfully as byādhi-; standard editions
            #          read byādhi with no such mark in Thai script. Same at
            #          verse 4.
            {
                'number': 3,
                'pali': 'พ์ยาธิธัมโมมหิ,',
                'pali_roman': 'byādhidhammomhi,',
                'thai': 'เรามีความเจ็บไข้เป็นธรรมดา',
                'paiboon': 'rao mii kwaam jèp kâi bpen tam-má-daa',
                'english': 'I am of the nature to sicken,',
            },
            {
                'number': 4,
                'pali': 'พ์ยาธิง อะนะตีโต (อะนะตีตา),',
                'pali_roman': 'byādhiṃ anatīto (anatītā),',
                'thai': 'จักล่วงพ้นความเจ็บไข้ไปไม่ได้',
                'paiboon': 'jàk lûaŋ pón kwaam jèp kâi bpai mâi dâai',
                'english': 'I have not gone beyond sickness,',
            },
            {
                'number': 5,
                'pali': 'มะระณะธัมโมมหิ,',
                'pali_roman': 'maraṇadhammomhi,',
                'thai': 'เรามีความตายเป็นธรรมดา',
                'paiboon': 'rao mii kwaam dtaai bpen tam-má-daa',
                'english': 'I am of the nature to die,',
            },
            {
                'number': 6,
                'pali': 'มะระณัง อะนะตีโต (อะนะตีตา),',
                'pali_roman': 'maraṇaṃ anatīto (anatītā),',
                'thai': 'จักล่วงพ้นความตายไปไม่ได้',
                'paiboon': 'jàk lûaŋ pón kwaam dtaai bpai mâi dâai',
                'english': 'I have not gone beyond death,',
            },
            # ‼ CHECK: Pali ends with a full stop, unlike the comma-terminated
            #          lines around it. This is the fifth recollection and may
            #          mark the end of a group in the book's own layout.
            # ‼ CORRECTED: thai  ทั้งหลาย ทั้งปวง → ทั้งหลายทั้งปวง. Stray
            #              space closed up in the fixed compound
            #              ทั้งหลายทั้งปวง, which บทพิจารณาสังขาร already
            #              prints solid. Verify against the printed page.
            {
                'number': 7,
                'pali': 'สัพเพหิ เม ปิเยหิ มะนาเปหิ นานาภาโว วินาภาโว.',
                'pali_roman': 'sabbehi me piyehi manāpehi nānābhāvo vinābhāvo.',
                'thai': 'เราจักต้องพลัดพรากจากของรักของชอบใจทั้งหลายทั้งปวง',
                'paiboon': 'rao jàk dtɔ̂ŋ plát prâak jàak kɔ̌ɔŋ rák kɔ̌ɔŋ chɔ̂ɔp jai táŋ-lǎai táŋ-bpuaŋ',
                'english': 'I must be parted and separated from all that is dear and pleasing to me.',
            },
            # ‼ CHECK: Thai reads เป็นของๆ ตน with a doubled mai yamok and a
            #          space before ตน. Reproduced as pasted; the Paiboon+
            #          renders the repetition as kɔ̌ɔŋ kɔ̌ɔŋ.
            {
                'section': 'กรรม: The Reflection on Kamma',
                'number': 8,
                'pali': 'กัมมัสสะโกมหิ,',
                'pali_roman': 'kammassakomhi,',
                'thai': 'เราเป็นผู้มีกรรมเป็นของๆ ตน',
                'paiboon': 'rao bpen pûu mii gam bpen kɔ̌ɔŋ kɔ̌ɔŋ dton',
                'english': 'I am the owner of my kamma,',
            },
            # ‼ CHECK: Thai reads เรามีกรรมเป็นทายาท without ผู้, where verses
            #          8, 10, 11 and 12 all read เราเป็นผู้มีกรรมเป็น.
            #          Reproduced as pasted; check whether ผู้ is dropped in
            #          the book.
            {
                'number': 9,
                'pali': 'กัมมะทายาโท,',
                'pali_roman': 'kammadāyādo,',
                'thai': 'เรามีกรรมเป็นทายาท',
                'paiboon': 'rao mii gam bpen taa-yâat',
                'english': 'I am the heir to my kamma,',
            },
            {
                'number': 10,
                'pali': 'กัมมะโยนิ,',
                'pali_roman': 'kammayoni,',
                'thai': 'เราเป็นผู้มีกรรมเป็นกำเนิด',
                'paiboon': 'rao bpen pûu mii gam bpen gam-nə̀ət',
                'english': 'I am born of my kamma,',
            },
            # ‼ CHECK: Pali reads กัมมะพันธุ with no closing comma visible in
            #          what you pasted — the comma is present. Disregard if the
            #          printed line matches; flagged because the preceding line
            #          กัมมะทายาโท, and this one differ in no other respect.
            {
                'number': 11,
                'pali': 'กัมมะพันธุ,',
                'pali_roman': 'kammabandhu,',
                'thai': 'เราเป็นผู้มีกรรมเป็นเผ่าพันธุ์',
                'paiboon': 'rao bpen pûu mii gam bpen pào-pan',
                'english': 'I am kin to my kamma,',
            },
            {
                'number': 12,
                'pali': 'กัมมะปะฏิสะระโณ,',
                'pali_roman': 'kammapaṭisaraṇo,',
                'thai': 'เราเป็นผู้มีกรรมเป็นที่พึ่งอาศัย',
                'paiboon': 'rao bpen pûu mii gam bpen tîi pʉ̂ŋ aa-sǎi',
                'english': 'I abide supported by my kamma,',
            },
            {
                'number': 13,
                'pali': 'ยัง กัมมัง กะริสสามิ,',
                'pali_roman': 'yaṃ kammaṃ karissāmi,',
                'thai': 'เราจักทำกรรมอันใดไว้',
                'paiboon': 'rao jàk tam gam an dai wái',
                'english': 'Whatever kamma I shall do,',
            },
            # ‼ CORRECTED: paiboon  gɔ̂ɔ → gɔ̂. House style: matches the
            #              romanisation already used elsewhere in this chanting
            #              book. Verify against the printed page.
            {
                'number': 14,
                'pali': 'กัล์ยาณัง วา ปาปะกัง วา,',
                'pali_roman': 'kalyāṇaṃ vā pāpakaṃ vā,',
                'thai': 'ดีก็ตาม ชั่วก็ตาม',
                'paiboon': 'dii gɔ̂ dtaam chûa gɔ̂ dtaam',
                'english': 'whether fair or foul,',
            },
            # ‼ CHECK: The Thai of this verse runs straight into the Pali of
            #          verse 16 with no break: …ของกรรมอันนั้นเอวัง อัมเหหิ…. I
            #          split them at อันนั้น / เอวัง. Verify the split point
            #          against the page.
            {
                'number': 15,
                'pali': 'ตัสสะ ทายาโท (ทายาทา) ภะวิสสามิ.',
                'pali_roman': 'tassa dāyādo (dāyādā) bhavissāmi.',
                'thai': 'เราจักเป็นผู้รับผลของกรรมอันนั้น',
                'paiboon': 'rao jàk bpen pûu ráp pǒn kɔ̌ɔŋ gam an nán',
                'english': 'of that I shall be the heir.',
            },
            # ‼ CHECK: The source breaks the Thai as อย่างนี้ / แล. across two
            #          lines, with แล. alone on the final line. I joined it
            #          with a single space; confirm the book prints it as one
            #          line.
            {
                'section': 'เอวัง: The Closing Exhortation',
                'number': 16,
                'pali': 'เอวัง อัมเหหิ อะภิณหัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'evaṃ amhehi abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': 'เราทั้งหลาย พึงพิจารณาเนืองๆ อย่างนี้ แล.',
                'paiboon': 'rao táŋ-lǎai pʉŋ pí-jaa-rá-naa nʉaŋ nʉaŋ yàaŋ níi lɛɛ.',
                'english': 'Thus should we reflect, frequently and in this way.',
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — this chant is printed in Pali only. Every thai and paiboon
        #          field is empty. I have not supplied a translation from
        #          memory. Check whether the book prints one on a facing page
        #          or in a footnote; if it does not, the entry will stand at
        #          two layers.
        # ‼ CHECK: No invitation line is present. I have not written one.
        #          Confirm the book prints none.
        # ‼ CHECK: The book prints no section headings. The two sections and
        #          their names are my grouping, not the book's; the second
        #          contains only the closing formula and could be run on to the
        #          first.
        # ‼ CHECK: The source field carries the book's own footnote 1, วิ. มหา.
        #          5/92 ที. มหา. 10/105 (Vinaya Mahāvagga and Dīgha Nikāya
        #          Mahāvagga, Thai edition volume/page). This is the book's
        #          attribution, not mine, but the two references should be
        #          checked against the printed page since they run together
        #          with no separating punctuation.
        # ‼ CHECK: The heading is numbered 7. in the source, which I have taken
        #          as the book's chant number and left out of title_thai.
        #          Confirm you want chant numbers dropped.
        # ‼ CHECK: Footnote 2 reads พร้ห์มจาระโย and is a variant reading,
        #          presumably for พ์รัห์มะจาริโน in verse 4. Its spelling is
        #          itself odd — พร้ห์ม carries mai tho where the verse has
        #          พ์รัห์ม with thanthakhat over พ์ — and the two forms do not
        #          match each other. I have kept the footnote out of the
        #          verses; check both spellings against the page.

        'id': 'devatadissa-dakkhinanumodana',
        'title_thai': 'เทวะตาทิสสะทักขิณานุโมทะนาคาถา',
        'title_pali': 'Devatādissadakkhiṇānumodanāgāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': (
            "The Verses of Rejoicing in Offerings Dedicated to the Devas"
        ),
        'source': 'วิ. มหา. 5/92 ที. มหา. 10/105',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "Verses on dedicating an offering's merit to the devas of a place: "
            "those honoured honour in return, and the one they favour sees "
            "good fortune always."
        ),

        'when_chanted': (
            "Chanted as an anumodanā, in acceptance of an offering whose merit "
            "the donor dedicates to the devas."
        ),

        'background': [
            "Anumodanā verses are spoken by the recipients of an offering "
            "rather than the givers, and each set fits a particular occasion. "
            "This one belongs to the moment when a donor establishes a "
            "dwelling or takes up residence in a place and dedicates the merit "
            "of feeding the virtuous to the devas already living there. The "
            "footnote attributes it to two places in the canon, in the Vinaya "
            "and in the Dīgha Nikāya.",

            "The book prints this chant in Pali alone, with no Thai rendering "
            "beneath. That is not unusual for anumodanā verses, which are the "
            "reciter's professional stock rather than a text for lay "
            "reflection. Here it means the chant is given with its Pali and an "
            "English translation only.",
        ],

        'meaning': [
            "The verses set out a sequence of exchange rather than a simple "
            "act of giving. A wise person settling in a place feeds the "
            "virtuous and restrained there, and dedicates that offering to "
            "whatever devas inhabit it. The offering is not made to the devas "
            "directly; it is made to the sangha and assigned to them, which is "
            "the standard mechanism of dedicated merit.",

            "What follows is reciprocity. Those honoured honour in return, "
            "ปูชิตา ปูชะยันติ; those held in regard hold in regard. The "
            "construction is deliberately symmetrical, the same verb turned "
            "back upon the giver. Then the register softens into simile: they "
            "show compassion to him as a mother to her own-born son, ปุตตังวะ "
            "โอระสัง, the word โอระส marking a child of one's own body rather "
            "than any child.",

            "The closing line states the result plainly. The person to whom "
            "the devas are well disposed sees สะทา ภัท์รานิ — auspicious "
            "things, always. This is the ordinary shape of an anumodanā: an "
            "act of generosity described, and then the good that follows from "
            "it named, so the donor hears their gift placed within a wider "
            "order.",
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
            # ‼ CHECK: ยัส์มิง carries thanthakhat over ส์. Transliterated
            #          faithfully as yasmiṃ, which is the standard form; noted
            #          only because the mark placement should be confirmed.
            {
                'section': 'เทวะตาทิสสะทักขิณานุโมทะนาคาถา: The Verses of Dedication',
                'number': 1,
                'pali': 'ยัส์มิง ปะเทเส กัปเปติ',
                'pali_roman': 'yasmiṃ padese kappeti',
                'thai': '',
                'paiboon': '',
                'english': 'In whatever place he makes',
            },
            {
                'number': 2,
                'pali': 'วาสัง ปัณฑิตะชาติโย',
                'pali_roman': 'vāsaṃ paṇḍitajātiyo',
                'thai': '',
                'paiboon': '',
                'english': 'his dwelling, one of wise nature,',
            },
            # ‼ CHECK: โภเชต์วา carries thanthakhat over ต์. Transliterated
            #          faithfully as bhojetvā.
            {
                'number': 3,
                'pali': 'สีละวันเตตถะ โภเชต์วา',
                'pali_roman': 'sīlavantettha bhojetvā',
                'thai': '',
                'paiboon': '',
                'english': 'having fed there the virtuous,',
            },
            # ‼ CORRECTED: pali  พ์รัห์มะจาริโน? → พ์รัห์มะจาริโน. Stray
            #              question mark removed — an OCR misreading of the
            #              superscript footnote marker ๒ pointing to footnote
            #              2, not punctuation. Pali chanting lines carry no
            #              question marks. Verify against the printed page.
            # ‼ CORRECTED: pali_roman  brahmacārino? → brahmacārino. Follows
            #              the question-mark removal. Verify against the
            #              printed page.
            {
                'number': 4,
                'pali': 'สัญญะเต พ์รัห์มะจาริโน',
                'pali_roman': 'saññate brahmacārino',
                'thai': '',
                'paiboon': '',
                'english': 'the restrained, the farers in the holy life,',
            },
            {
                'number': 5,
                'pali': 'ยา ตัตถะ เทวะตา อาสุง',
                'pali_roman': 'yā tattha devatā āsuṃ',
                'thai': '',
                'paiboon': '',
                'english': 'whatever devas there may be in that place,',
            },
            # ‼ CHECK: Lines 1–6 are printed with no terminal punctuation until
            #          ทักขิณะมาทิเส, which also has none. I have supplied no
            #          punctuation of my own; the full stop shown at verse 12
            #          is the book's.
            {
                'number': 6,
                'pali': 'ตาสัง ทักขิณะมาทิเส',
                'pali_roman': 'tāsaṃ dakkhiṇamādise',
                'thai': '',
                'paiboon': '',
                'english': 'to them let him dedicate the offering.',
            },
            {
                'number': 7,
                'pali': 'ตา ปูชิตา ปูชะยันติ',
                'pali_roman': 'tā pūjitā pūjayanti',
                'thai': '',
                'paiboon': '',
                'english': 'They, being honoured, give honour in return;',
            },
            {
                'number': 8,
                'pali': 'มานิตา มานะยันติ นัง',
                'pali_roman': 'mānitā mānayanti naṃ',
                'thai': '',
                'paiboon': '',
                'english': 'being held in regard, they hold him in regard.',
            },
            {
                'number': 9,
                'pali': 'ตะโต นัง อะนุกัมปันติ',
                'pali_roman': 'tato naṃ anukampanti',
                'thai': '',
                'paiboon': '',
                'english': 'Thereafter they show him compassion,',
            },
            {
                'number': 10,
                'pali': 'มาตา ปุตตังวะ โอระสัง',
                'pali_roman': 'mātā puttaṃva orasaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'as a mother towards her own-born son.',
            },
            # ‼ CHECK: โปโส is spelled with ป (unaspirated p). Standard
            #          editions read poso, so the transliteration agrees;
            #          flagged only because ผ/พ and ป are easily confused in
            #          reprints and this word governs the sense of the final
            #          couplet.
            {
                'number': 11,
                'pali': 'เทวะตานุกัมปิโต โปโส',
                'pali_roman': 'devatānukampito poso',
                'thai': '',
                'paiboon': '',
                'english': 'The person to whom the devas are compassionate',
            },
            # ‼ CHECK: ภัท์รานิ carries thanthakhat over ท์. Transliterated
            #          faithfully as bhadrāni. Some editions read ภัททานิ
            #          (bhaddāni); I have kept the printed form rather than
            #          substituting.
            {
                'number': 12,
                'pali': 'สะทา ภัท์รานิ ปัสสะติ.',
                'pali_roman': 'sadā bhadrāni passati.',
                'thai': '',
                'paiboon': '',
                'english': 'sees always what is auspicious.',
            },
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 13,
                'pali': 'เทวะตาทิสสะทักขิณานุโมทะนาคาถา นิฏฐิตา.',
                'pali_roman': 'devatādissadakkhiṇānumodanāgāthā niṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': 'The verses of rejoicing in offerings dedicated to the devas are ended.',
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — this chant is printed in Pali only. Every thai and paiboon
        #          field is empty. I have not supplied a translation from
        #          memory. Check whether the book prints one on a facing page;
        #          if not, the entry stands at two layers, as with chant 7.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It has no
        #          authority from the source and should be treated as
        #          provisional.
        # ‼ CHECK: No invitation line is present. I have not written one.
        #          Confirm the book prints none.
        # ‼ CHECK: source left empty. Chant 7 carried a footnote giving วิ.
        #          มหา. and ที. มหา. references, but nothing comparable appears
        #          here in what you pasted. Check the foot of the page for a
        #          footnote that may not have been copied.
        # ‼ CHECK: The book prints no section headings. All four sections and
        #          their names are my grouping by subject, not the book's.
        # ‼ CHECK: The heading is numbered 8. in the source. As with chant 7, I
        #          have taken this as the book's chant number and left it out
        #          of title_thai.

        'id': 'devatabhisammantana',
        'title_thai': 'เทวะตาภิสัมมันตะนะคาถา',
        'title_pali': 'Devatābhisammantanagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses of Address to the Devas',
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "An address to all beings gathered, earthbound or in the air: hear "
            "this well-spoken word, be kindly to humankind, and guard those "
            "who make offerings."
        ),

        'when_chanted': (
            "Chanted as an address to the unseen beings present at a place, "
            "commonly at the opening of a blessing ceremony or the "
            "consecration of a site."
        ),

        'background': [
            "This chant belongs with the preceding one and follows it in the "
            "book's numbering, but its posture is different. The last set "
            "dedicated merit to the devas; this one speaks to them directly. "
            "It opens by naming who is being addressed — beings gathered here, "
            "whether of the earth or of the intermediate space — and asks "
            "first for their attention rather than their favour.",

            "The preceding chant carried a canonical footnote; this one is "
            "printed with no attribution at all, and none has been supplied in "
            "its place. No Thai rendering appears beneath it either, so the "
            "chant is given here with its Pali and an English translation "
            "only.",
        ],

        'meaning': [
            "The opening stanza is an address, not a request. It calls upon "
            "whatever beings have assembled, ภุมมานิ or อันตะลิกเข — of the "
            "earth or of the air — and asks two things of them: that they be "
            "glad in mind, and that they listen respectfully to what is about "
            "to be said. The order matters. Nothing is asked of these beings "
            "until they have been greeted and their goodwill sought.",

            "The second movement states what is being offered them: a "
            "well-spoken word, something that gives rise to mindfulness in "
            "merit, free of evil, an instruction in Dhamma for those who would "
            "follow it. The gift to the devas is the teaching itself. Only "
            "after this does the verse turn, with ตัส์มา หิ, therefore — and "
            "the request follows.",

            "The request is for loving-kindness towards the human race, and "
            "specifically towards those who bear strong devotion to these "
            "beings and who carry offerings by day and by night. The final "
            "stanza gives the reason with unusual candour: human beings are of "
            "slender power, while these beings are unseen and of great might. "
            "The asymmetry is stated plainly, and the closing line draws its "
            "conclusion — therefore guard them, being heedful.",
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
            {
                'section': 'ยานีธะ ภูตานิ: The Address to the Assembled Beings',
                'number': 1,
                'pali': 'ยานีธะ ภูตานิ สะมาคะตานิ',
                'pali_roman': 'yānīdha bhūtāni samāgatāni',
                'thai': '',
                'paiboon': '',
                'english': 'Whatever beings are here assembled,',
            },
            {
                'number': 2,
                'pali': 'ภุมมานิ วา ยานิ วะ อันตะลิกเข',
                'pali_roman': 'bhummāni vā yāni va antalikkhe',
                'thai': '',
                'paiboon': '',
                'english': 'whether of the earth or those in the air,',
            },
            # ‼ CHECK: สัพเพ วะ is printed as two words. Some editions set this
            #          solid as สัพเพวะ (sabbeva). I kept the printed spacing
            #          and transliterated it as printed rather than
            #          substituting.
            {
                'number': 3,
                'pali': 'สัพเพ วะ ภูตา สุมะนา ภะวันตุ',
                'pali_roman': 'sabbe va bhūtā sumanā bhavantu',
                'thai': '',
                'paiboon': '',
                'english': 'may all those beings be glad of mind,',
            },
            {
                'number': 4,
                'pali': 'อะโถปิ สักกัจจะ สุณันตุ ภาสิตัง.',
                'pali_roman': 'athopi sakkacca suṇantu bhāsitaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'and moreover let them listen respectfully to what is spoken.',
            },
            {
                'section': 'สุภาสิตัง: The Offering of the Well-Spoken Word',
                'number': 5,
                'pali': 'สุภาสิตัง กิญจิปิ โว ภะเณมุ',
                'pali_roman': 'subhāsitaṃ kiñcipi vo bhaṇemu',
                'thai': '',
                'paiboon': '',
                'english': 'Some little that is well spoken we would utter to you,',
            },
            {
                'number': 6,
                'pali': 'ปุญเญ สะตุปปาทะกะรัง อะปาปัง',
                'pali_roman': 'puññe satuppādakaraṃ apāpaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'giving rise to mindfulness in merit, free of evil,',
            },
            {
                'number': 7,
                'pali': 'ธัมมูปะเทสัง อะนุการะกานัง',
                'pali_roman': 'dhammūpadesaṃ anukārakānaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'an instruction in Dhamma for those who would follow it.',
            },
            # ‼ CHECK: This line ends with no terminal punctuation, where
            #          verses 4, 12 and 16 each close their stanza with a full
            #          stop. Its sense also runs straight into verse 9, so the
            #          second and third stanzas may be a single eight-line
            #          stanza in the book. My section break here is an
            #          inference; verify the stanza division.
            # ‼ CORRECTED: pali  ตัสมา → ตัส์มา. The same word is spelled two
            #              ways in one chant: ตัสมา here, ตัส์มา at verse 16.
            #              The thanthakhat form matches the book's own
            #              convention for a Pali consonant cluster (พาฬ์หัง in
            #              verse 10, ยัส์มิง in the preceding chant), so verse
            #              16 is taken as correct. Both already transliterate
            #              identically as tasmā, so pali_roman is unchanged.
            #              Verify against the printed page.
            {
                'number': 8,
                'pali': 'ตัส์มา หิ ภูตานิ สะเมนตุ สัพเพ',
                'pali_roman': 'tasmā hi bhūtāni samentu sabbe',
                'thai': '',
                'paiboon': '',
                'english': 'Therefore let all beings assemble.',
            },
            {
                'section': 'เมตตา: The Exhortation to Loving-Kindness',
                'number': 9,
                'pali': 'เมตตัง กะโรถะ มานุสิยา ปะชายะ',
                'pali_roman': 'mettaṃ karotha mānusiyā pajāya',
                'thai': '',
                'paiboon': '',
                'english': 'Show loving-kindness towards the race of men,',
            },
            # ‼ CHECK: พาฬ์หัง carries thanthakhat over ฬ์. Transliterated
            #          faithfully as bāḷhaṃ; confirm the mark placement, since
            #          ฬ with thanthakhat is unusual.
            {
                'number': 10,
                'pali': 'ภูเตสุ พาฬ์หัง กะตะภัตติกายะ',
                'pali_roman': 'bhūtesu bāḷhaṃ katabhattikāya',
                'thai': '',
                'paiboon': '',
                'english': 'who bear strong devotion towards the beings,',
            },
            # ‼ CHECK: This line runs to eleven syllables against the ten or
            #          eleven of its neighbours, and เย sits between the verb
            #          and its object. Reproduced as pasted; worth checking the
            #          word order against the page in case a word has been
            #          transposed.
            {
                'number': 11,
                'pali': 'ทิวา จะ รัตโต จะ หะรันติ เย พะลิง',
                'pali_roman': 'divā ca ratto ca haranti ye baliṃ',
                'thai': '',
                'paiboon': '',
                'english': 'who by day and by night bring their offerings,',
            },
            {
                'number': 12,
                'pali': 'ปัจโจปะการัง อะภิกังขะมานา.',
                'pali_roman': 'paccopakāraṃ abhikaṅkhamānā.',
                'thai': '',
                'paiboon': '',
                'english': 'hoping for help in return.',
            },
            {
                'section': 'รักขะถะ: The Request for Protection',
                'number': 13,
                'pali': 'เต โข มะนุสสา ตะนุกานุภาวา',
                'pali_roman': 'te kho manussā tanukānubhāvā',
                'thai': '',
                'paiboon': '',
                'english': 'Those human beings are of slender power,',
            },
            {
                'number': 14,
                'pali': 'ภูตา วิเสเสนะ มะหิทธิกา จะ',
                'pali_roman': 'bhūtā visesena mahiddhikā ca',
                'thai': '',
                'paiboon': '',
                'english': 'while the beings are of especially great might,',
            },
            {
                'number': 15,
                'pali': 'อะทิสสะมานา มะนุเชหิ ญาตา',
                'pali_roman': 'adissamānā manujehi ñātā',
                'thai': '',
                'paiboon': '',
                'english': 'unseen, though known to men.',
            },
            # ‼ CORRECTED: pali  อัปปะมัตตา.' → อัปปะมัตตา.. Stray apostrophe
            #              after the full stop removed (an OCR artefact); the
            #              same artefact was removed from ติลักขะณาทิคาถา.
            #              Verify against the printed page.
            # ‼ CORRECTED: pali_roman  appamattā.' → appamattā.. Follows the
            #              apostrophe removal. Verify against the printed page.
            {
                'number': 16,
                'pali': 'ตัส์มา หิ เน รักขะถะ อัปปะมัตตา.',
                'pali_roman': 'tasmā hi ne rakkhatha appamattā.',
                'thai': '',
                'paiboon': '',
                'english': 'Therefore guard them, being heedful.',
            },
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 17,
                'pali': 'เทวะตาภิสัมมันตะนะคาถา นิฏฐิตา.',
                'pali_roman': 'devatābhisammantanagāthā niṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': 'The verses of address to the devas are ended.',
            },
        ],
    },

    {
        # ‼ CHECK: The Thai is printed as one continuous block after each group
        #          of Pali lines, not line by line. Every division of a Thai
        #          block into verse-sized portions in this entry is my
        #          inference, not the book's layout. This affects all sixteen
        #          verses and is the single most important thing to check
        #          against the page.
        # ‼ CHECK: source left empty. The book text you pasted gives no
        #          attribution and I have not supplied one. The title names a
        #          king victorious in the three worlds, but I have not inferred
        #          a canonical reference from that.
        # ‼ CHECK: The Thai translation is expansive rather than literal
        #          throughout — three-word Pali lines receive full sentences.
        #          My English renders the Pali line, with the Thai's additions
        #          folded in where they clearly belong to that line. Where the
        #          two differ in scope, the Pali governs.

        'id': 'tilokavijaya-pattidana',
        'title_thai': 'ติโลกะวิชะยะราชะปัตติทานะคาถา',
        'title_pali': 'Tilokavijayarājapattidānagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': (
            "The Verses on Dedicating Merit, of the King Victorious in the "
            "Three Worlds"
        ),
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        'summary': (
            "A dedication of all merit done by body, speech and mind to every "
            "being, percipient or not, with the wish that all obtain excellent "
            "food."
        ),

        'when_chanted': (
            "Recited as a dedication of merit, sharing the fruit of one's good "
            "actions with all beings whether they know of it or not."
        ),

        'background': [
            "Pattidāna verses give away what has just been gained. Where an "
            "anumodanā rejoices in another's gift, this chant assigns the "
            "reciter's own accumulated merit outward, and does so without "
            "reserving any portion. The title attributes the verses to a king "
            "victorious in the three worlds, though no canonical source is "
            "printed alongside them here.",

            "The Thai translation here is expansive rather than literal, a "
            "common feature of older Thai chanting books. A three-word Pali "
            "line such as ติทะเส สุคะตัง กะตัง receives a full sentence naming "
            "the Tāvatiṃsa heaven and the potency of its rewards. This means "
            "the Thai and Pali do not run in step line by line, and the two "
            "are paired here by meaning rather than by position.",
        ],

        'meaning': [
            "The opening movement gathers everything eligible for dedication: "
            "whatever wholesome action is to be done, done by body, speech and "
            "mind, and done such that it leads to the realm of the thirty. "
            "Nothing is set aside as too small or too private. The Thai adds "
            "that the reciter has already accumulated and fulfilled these, so "
            "what follows is the disposal of something actually possessed.",

            "The recipients are then defined as widely as the cosmology "
            "permits. Beings without perception and beings with perception — "
            "the Thai glosses the first as those existing as mere form alone — "
            "together exhaust the categories. May they all be sharers in the "
            "fruit of the merit I have made. The formula deliberately leaves "
            "no class of being outside the gift.",

            "A practical difficulty follows, and the verses meet it directly. "
            "Merit dedicated to those who do not know of it might seem to fall "
            "idle, so the chant asks the devas to announce it to them. This is "
            "why pattidāna verses are so often chanted aloud: the giving is "
            "completed by its being made known, and where human speech cannot "
            "reach, the devas are asked to carry it.",

            "The closing movement narrows to a single, concrete wish. All "
            "beings in the world subsist by nutriment; may they all obtain "
            "food that is agreeable. Having dedicated merit in the largest "
            "possible terms, the chant ends by asking for the plainest "
            "possible good, and the Thai adds that this is done according to "
            "the reciter's own intention, in support of their welfare and "
            "happiness.",
        ],

        'invitation': {
            'pali': 'หันทะ มะยัง ติโลกะวิชะยะราชะปัตติทานะคาถาโย ภะณามะ เส.',
            'pali_roman': (
                "handa mayaṃ tilokavijayarājapattidānagāthāyo bhaṇāma se."
            ),
            'thai': '',
            'paiboon': '',
            'english': (
                "Now let us recite the verses on dedicating merit, of the king "
                "victorious in the three worlds."
            ),
        },

        'verses': [
            {
                'section': 'ปัตติทานะ: The Dedication of Merit',
                'number': 1,
                'pali': 'กัตตัพพัง กิริยัง มะมะ,',
                'pali_roman': 'kattabbaṃ kiriyaṃ mama,',
                'thai': 'กิจที่ควรจะกระทำ,',
                'paiboon': 'gìt tîi kuan jà grà-tam,',
                'english': 'The deed that is to be done by me,',
            },
            # ‼ CORRECTED: pali  กุละลัง → กุสะลัง. กุละลัง is a slip for
            #              กุสะลัง (kusalaṃ); the Thai gloss กุศลกรรม on the
            #              same line requires it. Verify against the printed
            #              page.
            # ‼ CORRECTED: pali_roman  kulalaṃ → kusalaṃ. Follows the กุสะลัง
            #              correction. Verify against the printed page.
            {
                'number': 2,
                'pali': 'ยังกิญจิ กุสะลัง กัมมัง,',
                'pali_roman': 'yaṅkiñci kusalaṃ kammaṃ,',
                'thai': 'คือกุศลกรรมสิ่งใดสิ่งหนึ่ง,',
                'paiboon': 'kʉʉ gù-sǒn-lá-gam sìŋ dai sìŋ nʉ̀ŋ,',
                'english': 'that is to say, whatever wholesome action there may be,',
            },
            # ‼ CHECK: The Thai for this line and for verse 4 are printed in
            #          the reverse order from their Pali: the block gives the
            #          กาย วาจา ใจ sense first and the ไตรทศ sense last. I kept
            #          your Pali order and paired by meaning.
            {
                'number': 3,
                'pali': 'ติทะเส สุคะตัง กะตัง,',
                'pali_roman': 'tidase sugataṃ kataṃ,',
                'thai': 'ให้เป็นไป ในเหล่าไตรทศเทพยดาทั้งหลาย, คือมีอานุภาพ วิบากสมบัติกล้า, ควรจะนำให้อุบัติบังเกิดในดาวดึงสาลัยทิพยสถาน,',
                'paiboon': 'hâi bpen bpai nai lào dtrai-tót têep-pá-yá-daa táŋ-lǎai, kʉʉ mii aa-nú-pâap wí-bàak sǒm-bàt glâa, kuan jà nam hâi ù-bàt baŋ-gə̀ət nai daao-dʉŋ-sǎa-lai típ-pá-yá-sà-tǎan,',
                'english': 'done such that it leads well among the thirty devas — that is, having such power and strength of resultant fortune as should bring about rebirth in the heavenly abode of Tāvatiṃsa,',
            },
            # ‼ CHECK: Thai reads เป็นของของตนนั้น with ของ doubled. This may
            #          be correct (a possession of one's own) or a doubling
            #          error. Reproduced as pasted.
            # ‼ CORRECTED: thai  ทังปวง → ทั้งปวง. Missing mai tho; ทั้งปวง is
            #              printed correctly at verse 7 of this chant. Verify
            #              against the printed page.
            # ‼ CORRECTED: paiboon  taŋ bpuaŋ → táŋ-bpuaŋ. Follows the ทั้งปวง
            #              correction, matching the romanisation at verse 7.
            #              Verify against the printed page.
            # ‼ CORRECTED: paiboon  gɔ̂ɔ → gɔ̂. House style: matches the
            #              romanisation already used elsewhere in this chanting
            #              book. Verify against the printed page.
            {
                'number': 4,
                'pali': 'กาเยนะ วาจา มะนะสา,',
                'pali_roman': 'kāyena vācā manasā,',
                'thai': 'อันสัตว์พึงกระทำด้วยกาย วาจาใจ เป็นของของตนนั้น ข้าพเจ้าก็ได้สะสมบำเพ็ญแล้ว มีอยู่ กุศลกรรม ทั้งปวงเหล่านั้น ข้าพเจ้าก็ได้กระทำแล้ว,',
                'paiboon': 'an sàt pʉŋ grà-tam dûay gaai waa-jaa jai bpen kɔ̌ɔŋ kɔ̌ɔŋ dton nán kâa-pá-jâao gɔ̂ dâai sà-sǒm bam-pen lɛ́ɛo mii yùu gù-sǒn-lá-gam táŋ-bpuaŋ lào nán kâa-pá-jâao gɔ̂ dâai grà-tam lɛ́ɛo,',
                'english': 'by body, by speech and by mind — such as a being should do and hold as their own: these I have gathered and fulfilled, and all those wholesome actions I have indeed performed,',
            },
            # ‼ CHECK: The source breaks the Thai as ดำรง / อยู่ across two
            #          lines. I joined it with a single space; confirm the book
            #          prints it as one line.
            # ‼ CHECK: The Thai names those with saññā before those without,
            #          the reverse of the Pali order (อะสัญญิโน then สัญญิโน).
            #          I kept the Pali as the book prints it and paired the
            #          Thai portions by meaning, so the Thai blocks appear here
            #          in swapped order.
            # ‼ CORRECTED: paiboon  gɔ̂ɔ → gɔ̂. House style: matches the
            #              romanisation already used elsewhere in this chanting
            #              book. Verify against the printed page.
            {
                'section': 'สัพเพ สัตตา: The Sharing with All Beings',
                'number': 5,
                'pali': 'เย จะ สัตตา อะสัญญิโน,',
                'pali_roman': 'ye ca sattā asaññino,',
                'thai': 'สัตว์ทั้งหลายเหล่าใดที่มิใช่สัตว์มีสัญญา ดำรง อยู่สักว่ารูปอย่างเดียวก็ดี,',
                'paiboon': 'sàt táŋ-lǎai lào dai tîi mí-châi sàt mii sǎn-yaa dam-roŋ yùu sàk wâa rûup yàaŋ diao gɔ̂ dii,',
                'english': 'and whatever beings are without perception, subsisting as mere form alone,',
            },
            # ‼ CORRECTED: paiboon  gɔ̂ɔ → gɔ̂. House style: matches the
            #              romanisation already used elsewhere in this chanting
            #              book. Verify against the printed page.
            {
                'number': 6,
                'pali': 'เย สัตตา สัญญิโน อัตถิ,',
                'pali_roman': 'ye sattā saññino atthi,',
                'thai': 'สัตว์ทั้งหลายเหล่าใดที่มีสัญญาก็ดี,',
                'paiboon': 'sàt táŋ-lǎai lào dai tîi mii sǎn-yaa gɔ̂ dii,',
                'english': 'and whatever beings there are that possess perception,',
            },
            # ‼ CORRECTED: thai   6, → ,. Stray "6" removed — a footnote marker
            #              or page number caught by OCR, not part of the text.
            #              Only the digit is removed; the comma is kept. Verify
            #              against the printed page.
            # ‼ CORRECTED: paiboon   6, → ,. Follows the stray-digit removal.
            #              Verify against the printed page.
            {
                'number': 7,
                'pali': 'กะตัง ปุญญะผะลัง มัยหัง,',
                'pali_roman': 'kataṃ puññaphalaṃ mayhaṃ,',
                'thai': 'ผลแห่งบุญที่ข้าพเจ้าได้ก่อสร้างแล้วทั้งปวงเหล่านี้,',
                'paiboon': 'pǒn hɛ̀ŋ bun tîi kâa-pá-jâao dâai gɔ̀ɔ-sâaŋ lɛ́ɛo táŋ-bpuaŋ lào níi,',
                'english': 'all this fruit of merit that I have built up,',
            },
            # ‼ CHECK: The source breaks the Thai as ครบ / ถ้วน across two
            #          lines. I joined it with a single space; confirm the book
            #          prints ครบถ้วน as one word.
            # ‼ CHECK: Thai ends with นั้น ๆ, using the mai yamok repetition
            #          mark. The Paiboon+ renders the repetition in full as nán
            #          nán. Confirm this is how you want yamok handled.
            {
                'number': 8,
                'pali': 'สัพเพ ภาคี ภะวันตุ เต.',
                'pali_roman': 'sabbe bhāgī bhavantu te.',
                'thai': 'ขอสัตว์ทั้งหลายทั้งหมดครบ ถ้วนทุกหมู่เหล่า, จงเป็นผู้มีส่วนได้เสวยซึ่งผลแห่งบุญนั้น ๆ,',
                'paiboon': 'kɔ̌ɔ sàt táŋ-lǎai táŋ-mòt króp tûan túk mùu lào, joŋ bpen pûu mii sùan dâai sà-wə̌əy sʉ̂ŋ pǒn hɛ̀ŋ bun nán nán,',
                'english': 'may all beings, every group of them complete, be sharers in that fruit of merit.',
            },
            {
                'section': 'นิเวทะนา: The Making Known',
                'number': 9,
                'pali': 'เย ตัง กะตัง สุวิทิตัง,',
                'pali_roman': 'ye taṃ kataṃ suviditaṃ,',
                'thai': 'บุญที่ข้าพเจ้าได้กระทำแล้วนั้น, สัตว์ทั้งหลายเหล่าใดได้รู้แจ้งแล้ว,',
                'paiboon': 'bun tîi kâa-pá-jâao dâai grà-tam lɛ́ɛo nán, sàt táŋ-lǎai lào dai dâai rúu jɛ̂ɛŋ lɛ́ɛo,',
                'english': 'Those who have come to know well what has been done —',
            },
            # ‼ CHECK: The source breaks the Thai as อัน / ข้าพเจ้า across two
            #          lines. I joined it with a single space.
            # ‼ CHECK: The Thai line ends with no punctuation, where the
            #          surrounding Thai lines end with a comma. Reproduced as
            #          pasted.
            {
                'number': 10,
                'pali': 'ทินนัง ปุญญะผะลัง มะยา,',
                'pali_roman': 'dinnaṃ puññaphalaṃ mayā,',
                'thai': 'ผลแห่งบุญอัน ข้าพเจ้าได้ให้แล้วแก่สัตว์ทั้งหลายเหล่านั้น',
                'paiboon': 'pǒn hɛ̀ŋ bun an kâa-pá-jâao dâai hâi lɛ́ɛo gɛ̀ɛ sàt táŋ-lǎai lào nán',
                'english': 'to them the fruit of merit has been given by me.',
            },
            {
                'number': 11,
                'pali': 'เย จะ ตัตถะ นะ ชานันติ,',
                'pali_roman': 'ye ca tattha na jānanti,',
                'thai': 'สัตว์ทั้งหลายเหล่าใดที่ยังไม่รู้ซึ่งผลแห่งบุญนั้น มีอยู่แล้วไซร้,',
                'paiboon': 'sàt táŋ-lǎai lào dai tîi yaŋ mâi rúu sʉ̂ŋ pǒn hɛ̀ŋ bun nán mii yùu lɛ́ɛo sái,',
                'english': 'And if there be those who do not know of it,',
            },
            # ‼ CHECK: Thai ends with อนุโมทนาเกิด, which reads oddly. เถิด
            #          would be expected in this position as a hortative.
            #          Reproduced as pasted; compare the page.
            # ‼ CHECK: The source breaks the Thai as ผู้ทรง / เทวฤทธานุภาพ
            #          across two lines. I joined it with a single space.
            # ‼ CORRECTED: thai  สัตว์เล่านั้น → สัตว์เหล่านั้น. เล่า is a slip
            #              for เหล่า, which is printed correctly at verses 5,
            #              6, 9, 11 and 15 of this chant. Verify against the
            #              printed page.
            # ‼ CORRECTED: paiboon  sàt lâo nán → sàt lào nán. Follows the
            #              เหล่า correction, matching the romanisation
            #              elsewhere. Verify against the printed page.
            {
                'number': 12,
                'pali': 'เทวา เตสัง นิเวทะยุง.',
                'pali_roman': 'devā tesaṃ nivedayuṃ.',
                'thai': 'ขอเทพเจ้าผู้ทรง เทวฤทธานุภาพทั้งหลาย พึงบอกแก่สัตว์เหล่านั้น ให้รู้แล้วและอนุโมทนาเกิด,',
                'paiboon': 'kɔ̌ɔ têep-pá-jâao pûu soŋ tee-wá-rít-taa-nú-pâap táŋ-lǎai pʉŋ bɔ̀ɔk gɛ̀ɛ sàt lào nán hâi rúu lɛ́ɛo lɛ́ à-nú-moo-tá-naa gə̀ət,',
                'english': 'may the devas, bearing their divine might, announce it to those beings, that they may know and rejoice.',
            },
            {
                'section': 'อาหาระ: The Wish for Sustenance',
                'number': 13,
                'pali': 'สัพเพ โลกัมหิ เย สัตตา,',
                'pali_roman': 'sabbe lokamhi ye sattā,',
                'thai': 'สัตว์ทั้งหลายในโลกสันนิวาส บรรดาที่มีอาหารเป็นเหตุ,',
                'paiboon': 'sàt táŋ-lǎai nai lôok sǎn-ní-wâat ban-daa tîi mii aa-hǎan bpen hèet,',
                'english': 'All beings in this world of dwelling together, all who have nutriment as their cause,',
            },
            # ‼ CHECK: The source breaks the Thai as ดำรงอยู่ / ด้วยอาหาร
            #          across two lines. I joined it with a single space.
            # ‼ CORRECTED: paiboon  yɔ̂ɔm → yɔ̂m. House style: matches the
            #              romanisation already used elsewhere in this chanting
            #              book. Verify against the printed page.
            {
                'number': 14,
                'pali': 'ชีวันตาหาระเหตุกา,',
                'pali_roman': 'jīvantāhārahetukā,',
                'thai': 'ย่อมเป็นอยู่และดำรงอยู่ ด้วยอาหาร เป็นเครื่องหล่อเลี้ยงรูปกายนี้แล้ว,',
                'paiboon': 'yɔ̂m bpen yùu lɛ́ dam-roŋ yùu dûay aa-hǎan bpen krʉ̂aŋ lɔ̀ɔ líaŋ rûup-bpà-gaai níi lɛ́ɛo,',
                'english': 'who live and are sustained by food as that which nourishes this bodily form,',
            },
            {
                'number': 15,
                'pali': 'มะนุญญัง โภชะนัง สัพเพ,',
                'pali_roman': 'manuññaṃ bhojanaṃ sabbe,',
                'thai': 'สัตว์ทั้งหลายทั้งหมดเหล่านั้น, จงเป็นผู้ได้ซึ่งโภชนะอันอุดมประณีต,',
                'paiboon': 'sàt táŋ-lǎai táŋ-mòt lào nán, joŋ bpen pûu dâai sʉ̂ŋ poo-chá-ná an ù-dom bprà-nîit,',
                'english': 'may all those beings obtain food that is excellent and refined,',
            },
            # ‼ CHECK: The Pali ends with ติ (…เจตะสาติ.), the quotative marker
            #          closing the whole chant, and there is no ฯ. Reproduced
            #          as pasted; confirm no ฯ appears on the page.
            # ‼ CHECK: The final Thai line ends with no punctuation after แล,
            #          unlike the comma-terminated lines throughout. Reproduced
            #          as pasted.
            {
                'number': 16,
                'pali': 'ละภันตุ มะมะ เจตะสาติ.',
                'pali_roman': 'labhantu mama cetasāti.',
                'thai': 'เป็นที่เจริญแห่งจิต สำเร็จด้วยบุญฤทธิ์ ตามจิตของข้าพเจ้าจำนงเกื้อหนุนซึ่งความสุขประโยชน์ ด้วยประการฉะนี้แล',
                'paiboon': 'bpen tîi jà-rəən hɛ̀ŋ jìt sǎm-rèt dûay bun-yá-rít dtaam jìt kɔ̌ɔŋ kâa-pá-jâao jam-noŋ gʉ̂a-nǔn sʉ̂ŋ kwaam sùk bprà-yòot dûay bprà-gaan chà-níi lɛɛ',
                'english': 'food that gladdens the mind, accomplished by the power of merit, according to my own intention in support of their welfare and happiness. So it is.',
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — Pali only. Every thai and paiboon field is empty. I have
        #          not supplied a translation from memory. This is the fourth
        #          consecutive chant in this state.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It carries no
        #          authority from the source and should be treated as
        #          provisional.
        # ‼ CHECK: This chant is prose, not verse, and the source prints it as
        #          a continuous block. My division into 24 units follows the
        #          book's own commas and full stops, but the choice of where a
        #          unit ends is mine, not a line break in the book. This
        #          affects every verse.
        # ‼ CHECK: No invitation line is present. I have not written one.
        # ‼ CHECK: source left empty. The book text you pasted gives no
        #          footnote or attribution, unlike chants 7 and 9 which carried
        #          one. I have not supplied a reference.
        # ‼ CHECK: The book prints no section headings. All three sections and
        #          their names are my grouping, not the book's.
        # ‼ CHECK: The heading is numbered 3., where the preceding chants you
        #          sent were numbered 7, 8 and 9. This suggests a different
        #          section of the book. Worth confirming so the app's ordering
        #          does not collide.

        'id': 'mettanisamsa-sutta',
        'title_thai': 'เมตตานิสังสะสุตตัง',
        'title_pali': 'Mettānisaṃsasuttaṃ',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Discourse on the Benefits of Loving-Kindness',
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "The Buddha at Jeta's Grove lists eleven benefits to be expected "
            "from the liberation of mind through loving-kindness, well "
            "developed and firmly undertaken."
        ),

        'when_chanted': (
            "Chanted as a protective and auspicious discourse, and recited "
            "where the benefits of developing loving-kindness are to be "
            "called to mind."
        ),

        'background': [
            "This is a short discourse rather than a set of verses, and the "
            "book prints it in the standard sutta shape: the opening formula "
            "naming where it was spoken, the address to the monks, the "
            "teaching itself, and the monks' delight at the close. The "
            "setting is the one most familiar in the canon, Anāthapiṇḍika's "
            "monastery in Jeta's Grove at Sāvatthī.",

            "The teaching is built around a numbered list, and the Pali makes "
            "the count explicit twice — once as a question, กะตะเม เอกาทะสะ, "
            "which eleven, and once in the summary that closes the teaching. "
            "That structure makes the text unusually easy to verify: the "
            "benefits should number exactly eleven, and in what you pasted "
            "they do.",

            "As with the three preceding chants, no Thai rendering is "
            "printed, so this entry stands at two of the five layers and the "
            "English is my own off the Pali.",
        ],

        'meaning': [
            "The qualifying phrase before the list is longer than the list's "
            "first several items, and it is doing real work. Loving-kindness "
            "here is not a passing wish but เจโตวิมุตติ, a liberation of "
            "mind, and it must be pursued, developed, made much of, made a "
            "vehicle, made a foundation, established, consolidated and well "
            "undertaken. Only of such a practice are the eleven benefits to "
            "be expected.",

            "The benefits themselves move outward from the most private to "
            "the most far-reaching. They begin at the edges of sleep — one "
            "sleeps happily and wakes happily, and sees no evil dreams — "
            "which is where a mind's actual condition is least concealed. "
            "They then pass to how one is met: dear to human beings, dear to "
            "non-human beings, guarded by the devas.",

            "The middle items concern safety and steadiness: neither fire nor "
            "poison nor blade touches such a person, and the mind gathers "
            "itself into concentration quickly. Then the countenance grows "
            "clear, which is the only benefit visible from outside. The last "
            "two look to the end of life — one dies unconfused, and if one "
            "penetrates no higher, one fares to the Brahmā world. The list "
            "therefore runs from a single night's sleep to the disposition of "
            "the next existence, without changing its subject.",
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
            {
                'section': 'นิทานะ: The Setting',
                'number': 1,
                'pali': 'เอวัมเม สุตัง,',
                'pali_roman': 'evamme sutaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'Thus have I heard.',
            },
            {
                'number': 2,
                'pali': 'เอกัง สะมะยัง ภะคะวา,',
                'pali_roman': 'ekaṃ samayaṃ bhagavā,',
                'thai': '',
                'paiboon': '',
                'english': 'At one time the Blessed One',
            },
            {
                'number': 3,
                'pali': 'สาวัตถิยัง วิหะระติ,',
                'pali_roman': 'sāvatthiyaṃ viharati,',
                'thai': '',
                'paiboon': '',
                'english': 'was dwelling at Sāvatthī,',
            },
            {
                'number': 4,
                'pali': 'เชตะวะเน อะนาถะปิณฑิกัสสะ อาราเม,',
                'pali_roman': 'jetavane anāthapiṇḍikassa ārāme,',
                'thai': '',
                'paiboon': '',
                'english': "in Jeta's Grove, the monastery of Anāthapiṇḍika.",
            },
            {
                'number': 5,
                'pali': 'ตัตระ โข ภะคะวา ภิกขู อามันเตสิ ภิกขะโวติ,',
                'pali_roman': 'tatra kho bhagavā bhikkhū āmantesi bhikkhavoti,',
                'thai': '',
                'paiboon': '',
                'english': 'There the Blessed One addressed the monks: Monks.',
            },
            # ‼ CHECK: Pali reads กะทันเตติ. Standard editions read ภะทันเตติ
            #          (bhadanteti), the monks' respectful reply.
            #          Transliterated faithfully as kadanteti rather than
            #          substituted. Likely a mistyping.
            {
                'number': 6,
                'pali': 'กะทันเตติ เต ภิกขู ภะคะวะโต ปัจจัสโสสุง,',
                'pali_roman': 'kadanteti te bhikkhū bhagavato paccassosuṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'Venerable sir, those monks replied to the Blessed One.',
            },
            # ‼ CHECK: This unit runs from ภะคะวา เอตะทะโวจะ to สุสะมารัทธายะ
            #          with no internal comma, making it far longer than any
            #          other. Reproduced as one unit rather than split. If the
            #          book punctuates after เอตะทะโวจะ, this should become two
            #          verses.
            {
                'section': 'เอกาทะสานิสังสา: The Eleven Benefits',
                'number': 7,
                'pali': 'ภะคะวา เอตะทะโวจะ เมตตายะ ภิกขะเว เจโตวิมุตติยา อาเสวิตายะ ภาวิตายะ พะหุลีกะตายะ ยานีกะตายะ วัตถุกะตายะ อะนุฏฐิตายะ ปะริจิตายะ สุสะมารัทธายะ,',
                'pali_roman': 'bhagavā etadavoca mettāya bhikkhave cetovimuttiyā āsevitāya bhāvitāya bahulīkatāya yānīkatāya vatthukatāya anuṭṭhitāya paricitāya susamāraddhāya,',
                'thai': '',
                'paiboon': '',
                'english': 'The Blessed One said this: Monks, from the liberation of mind through loving-kindness — pursued, developed, made much of, made a vehicle, made a foundation, established, consolidated and well undertaken —',
            },
            # ‼ CHECK: เอกาทะ สานิสังสา is printed with a space mid-word; the
            #          word is เอกาทะสานิสังสา (ekādasānisaṃsā). Reproduced as
            #          pasted and transliterated with the space intact.
            {
                'number': 8,
                'pali': 'เอกาทะ สานิสังสา ปาฏิกังขา.',
                'pali_roman': 'ekāda sānisaṃsā pāṭikaṅkhā.',
                'thai': '',
                'paiboon': '',
                'english': 'eleven benefits are to be expected.',
            },
            {
                'number': 9,
                'pali': 'กะตะเม เอกาทะสะ.',
                'pali_roman': 'katame ekādasa.',
                'thai': '',
                'paiboon': '',
                'english': 'Which eleven?',
            },
            {
                'number': 10,
                'pali': 'สุขัง สุปะติ,',
                'pali_roman': 'sukhaṃ supati,',
                'thai': '',
                'paiboon': '',
                'english': 'One sleeps happily;',
            },
            {
                'number': 11,
                'pali': 'สุขัง ปะฏิพุชฌะติ.',
                'pali_roman': 'sukhaṃ paṭibujjhati.',
                'thai': '',
                'paiboon': '',
                'english': 'one wakes happily;',
            },
            # ‼ CHECK: สุปีนัง has a long ี where standard editions read
            #          สุปินัง (supinaṃ). Transliterated faithfully as supīnaṃ
            #          rather than substituted.
            {
                'number': 12,
                'pali': 'นะ ปาปะกัง สุปีนัง ปัสสะติ,',
                'pali_roman': 'na pāpakaṃ supīnaṃ passati,',
                'thai': '',
                'paiboon': '',
                'english': 'one sees no evil dreams;',
            },
            {
                'number': 13,
                'pali': 'มะนุสสานัง ปิโย โหติ,',
                'pali_roman': 'manussānaṃ piyo hoti,',
                'thai': '',
                'paiboon': '',
                'english': 'one is dear to human beings;',
            },
            {
                'number': 14,
                'pali': 'อะมะนุสสานัง ปิโย โหติ,',
                'pali_roman': 'amanussānaṃ piyo hoti,',
                'thai': '',
                'paiboon': '',
                'english': 'one is dear to non-human beings;',
            },
            # ‼ CHECK: เทวะ ตา is printed with a space mid-word; the word is
            #          เทวะตา (devatā). Reproduced as pasted, which forces the
            #          transliteration deva tā.
            {
                'number': 15,
                'pali': 'เทวะ ตา รักขันติ,',
                'pali_roman': 'deva tā rakkhanti,',
                'thai': '',
                'paiboon': '',
                'english': 'the devas guard one;',
            },
            {
                'number': 16,
                'pali': 'นาสสะ อัคคิ วา วิสัง วา สัตถัง วา กะมะติ,',
                'pali_roman': 'nāssa aggi vā visaṃ vā satthaṃ vā kamati,',
                'thai': '',
                'paiboon': '',
                'english': 'neither fire nor poison nor blade affects one;',
            },
            # ‼ CHECK: ตุวะฎัง is written with ฎ (ḍ) where standard editions
            #          read ตุวะฏัง with ฏ (ṭ). The two letters differ by a
            #          single stroke and are easily confused in reprints.
            #          Transliterated faithfully as tuvaḍaṃ.
            # ‼ CHECK: สะมาธิยะ ติ is printed with a space mid-word; the word
            #          is สะมาธิยะติ (samādhiyati). Reproduced as pasted.
            {
                'number': 17,
                'pali': 'ตุวะฎัง จิตตัง สะมาธิยะ ติ,',
                'pali_roman': 'tuvaḍaṃ cittaṃ samādhiya ti,',
                'thai': '',
                'paiboon': '',
                'english': "one's mind is quickly concentrated;",
            },
            {
                'number': 18,
                'pali': 'มุขะวัณโณ วิปปะสีทะติ,',
                'pali_roman': 'mukhavaṇṇo vippasīdati,',
                'thai': '',
                'paiboon': '',
                'english': 'the countenance grows clear;',
            },
            {
                'number': 19,
                'pali': 'อะสัมมุฬโห กาลัง กะโรติ,',
                'pali_roman': 'asammuḷho kālaṃ karoti,',
                'thai': '',
                'paiboon': '',
                'english': 'one dies unconfused;',
            },
            # ‼ CHECK: อัปปะฏิวิชฌัน โต is printed with a space mid-word; the
            #          word is อัปปะฏิวิชฌันโต (appaṭivijjhanto). Reproduced as
            #          pasted.
            # ‼ CHECK: พรห์มะโลกูปะโค carries thanthakhat over ห์ in a position
            #          that differs from chant 4's พ์รัห์มะจาริโน, where the
            #          mark sat over พ์. The same syllable is being written two
            #          ways across the book. Transliterated as brahma- in both.
            {
                'number': 20,
                'pali': 'อุตตะริง อัปปะฏิวิชฌัน โต พรห์มะโลกูปะโค โหติ.',
                'pali_roman': 'uttariṃ appaṭivijjhan to brahmalokūpago hoti.',
                'thai': '',
                'paiboon': '',
                'english': 'and, penetrating no higher, one fares to the Brahmā world.',
            },
            # ‼ CHECK: เอกา ทะสานิสังสา is printed with a space, but in a
            #          different place from verse 8's เอกาทะ สานิสังสา. The
            #          same word is broken two ways within one chant, which
            #          points to a line-wrapping artefact rather than the
            #          book's spelling. Both reproduced as pasted.
            {
                'section': 'นิคะมะนะ: The Conclusion',
                'number': 21,
                'pali': 'เมตตายะ ภิกขะเว เจโตวิมุตติยา อาเสวิตายะ ภาวิตายะ พะหุลีกะตายะ ยานีกะตายะ วัตถุกะตายะ อะนุฏฐิตายะ ปะริจิตายะ สุสะมารัทธายะ อิเม เอกา ทะสานิสังสา ปาฏิกังขาติ.',
                'pali_roman': 'mettāya bhikkhave cetovimuttiyā āsevitāya bhāvitāya bahulīkatāya yānīkatāya vatthukatāya anuṭṭhitāya paricitāya susamāraddhāya ime ekā dasānisaṃsā pāṭikaṅkhāti.',
                'thai': '',
                'paiboon': '',
                'english': 'Monks, from the liberation of mind through loving-kindness — pursued, developed, made much of, made a vehicle, made a foundation, established, consolidated and well undertaken — these eleven benefits are to be expected.',
            },
            {
                'number': 22,
                'pali': 'อิทะมะโวจะ ภะคะวา.',
                'pali_roman': 'idamavoca bhagavā.',
                'thai': '',
                'paiboon': '',
                'english': 'This the Blessed One said.',
            },
            # ‼ CHECK: ภะคะวะ โต is printed with a space mid-word; the word is
            #          ภะคะวะโต (bhagavato), which appears correctly at verse
            #          6. Reproduced as pasted.
            # ‼ CHECK: A stray double quotation mark follows the full stop:
            #          อะภินันทุนติ.". The same artefact appeared at the close
            #          of chants 8 and 9, there as a single apostrophe.
            #          Reproduced as pasted rather than tidied; it is now a
            #          pattern across three pages and may be worth one decision
            #          rather than three.
            {
                'number': 23,
                'pali': 'อัตตะมะนา เต ภิกขู ภะคะวะ โต ภาสิตัง อะภินันทุนติ."',
                'pali_roman': 'attamanā te bhikkhū bhagava to bhāsitaṃ abhinandunti."',
                'thai': '',
                'paiboon': '',
                'english': 'Gladdened, those monks delighted in the words of the Blessed One.',
            },
            # ‼ CHECK: The closing formula reads เมตตานิสังสะสุดตัง with ด,
            #          where the heading reads เมตตานิสังสะสุตตัง with ต. The
            #          same title is spelled two ways on one page.
            #          Transliterated faithfully as sudtaṃ; the heading form is
            #          the one used in title_thai.
            {
                'section': 'นิฏฐิตัง: The Closing Formula',
                'number': 24,
                'pali': 'เมตตานิสังสะสุดตัง นิฏฐิตัง.',
                'pali_roman': 'mettānisaṃsasudtaṃ niṭṭhitaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'The discourse on the benefits of loving-kindness is ended.',
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — Pali only. Every thai and paiboon field is empty. I have
        #          not supplied a translation from memory. This is the fifth
        #          consecutive chant in this state.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It carries no
        #          authority from the source and should be treated as
        #          provisional.
        # ‼ CHECK: The source prints this chant as one continuous block with no
        #          line breaks whatever. Every division into forty verse lines
        #          is mine, made at the metrical boundaries the repeated
        #          refrain makes visible. The stanza count of ten is therefore
        #          also my inference. This affects every verse and is the most
        #          important thing to check against the page.
        # ‼ CHECK: No invitation line is present. I have not written one.
        # ‼ CHECK: source left empty. The book text you pasted gives no
        #          footnote or attribution. I have not supplied a reference.
        # ‼ CHECK: I have made this one section rather than several, since
        #          every stanza closes with the same refrain and the chant does
        #          not divide by subject. The section name simply repeats the
        #          title. Say if you would rather it were grouped otherwise.
        # ‼ CHECK: The heading is numbered 4., following the 3. of the
        #          Mettānisaṃsasuttaṃ. The two clearly belong to one sequence
        #          in the book, separate from the 7, 8, 9 series sent earlier.

        'id': 'mettanisamsa-gatha',
        'title_thai': 'เมตตานิสังสะคาถา',
        'title_pali': 'Mettānisaṃsagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses on the Benefits of Loving-Kindness',
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "Ten stanzas of worldly and auspicious rewards, each closing with "
            "the same refrain: one who does not betray his friends."
        ),

        'when_chanted': (
            "Chanted following the discourse of the same name, as an "
            "auspicious recitation on the rewards of goodwill and constancy "
            "to friends."
        ),

        'background': [
            "This set of verses is paired in the book with chant 3, the "
            "Mettānisaṃsasuttaṃ, and follows immediately after it. Where the "
            "discourse gave eleven benefits in prose and attributed them to "
            "the developed liberation of mind, these verses give their "
            "benefits in metre and attribute them to something narrower and "
            "more concrete: not betraying one's friends.",

            "The construction is a refrain form. Each of the ten stanzas "
            "states three rewards and then closes with the identical line โย "
            "มิตตานัง นะ ทุพภะติ, he who does not betray his friends. The "
            "final occurrence adds the quotative ติ to close the whole. A "
            "chant of this shape is easy to recite and easy to verify, since "
            "any stanza missing its refrain is a stanza with a line missing.",

            "As with the four preceding chants, no Thai rendering is printed, "
            "so this entry stands at two of the five layers and the English "
            "is my own off the Pali.",
        ],

        'meaning': [
            "The rewards named are almost entirely of this world, and "
            "unusually practical for a chanting text. One has abundant food "
            "though far from home; many live in dependence on him; wherever "
            "he goes, to market towns or royal capitals, he is honoured. "
            "Thieves do not overpower him and nobles do not slight him. These "
            "are the goods of a person whose standing is secure.",

            "The middle stanzas turn to how such a person is received and "
            "what he receives back. Honouring, he is honoured; revered, he is "
            "held in reverence; he comes home unangered and is welcomed in "
            "the assembly. He blazes like fire and shines like a deva. The "
            "reciprocity is the argument of the chant — what is given out "
            "returns, and the verses simply itemise the forms in which it "
            "does.",

            "The last two stanzas widen to fortune and to safety. His cattle "
            "bear young, what is sown in his field grows, and he enjoys the "
            "fruit of what was sown. A man fallen from a cliff or a tree "
            "finds footing. And the simile that closes the chant: as the wind "
            "cannot overpower a banyan whose roots have spread wide, so "
            "enemies do not overpower him. The whole set rests on a single "
            "condition, stated ten times without variation.",
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
            {
                'section': 'เมตตานิสังสะคาถา: The Benefits of Loving-Kindness',
                'number': 1,
                'pali': 'พะหุตัพภักโข ภะวะติ',
                'pali_roman': 'bahutabbhakkho bhavati',
                'thai': '',
                'paiboon': '',
                'english': 'He has abundant food,',
            },
            {
                'number': 2,
                'pali': 'วิปปะวุตโถ สะกัง ฆะรา',
                'pali_roman': 'vippavuttho sakaṃ gharā',
                'thai': '',
                'paiboon': '',
                'english': 'though dwelling far from his own house;',
            },
            {
                'number': 3,
                'pali': 'พะหูนัง อุปะชีวันติ',
                'pali_roman': 'bahūnaṃ upajīvanti',
                'thai': '',
                'paiboon': '',
                'english': 'many live in dependence upon him —',
            },
            {
                'number': 4,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            {
                'number': 5,
                'pali': 'ยัง ยัง ชะนะปะทัง ยาติ',
                'pali_roman': 'yaṃ yaṃ janapadaṃ yāti',
                'thai': '',
                'paiboon': '',
                'english': 'To whatever country he goes,',
            },
            {
                'number': 6,
                'pali': 'นิคะเม ราชะธานิโย',
                'pali_roman': 'nigame rājadhāniyo',
                'thai': '',
                'paiboon': '',
                'english': 'to market towns or royal cities,',
            },
            {
                'number': 7,
                'pali': 'สัพพัตถะ ปูชิโต โหติ',
                'pali_roman': 'sabbattha pūjito hoti',
                'thai': '',
                'paiboon': '',
                'english': 'everywhere he is honoured —',
            },
            {
                'number': 8,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            {
                'number': 9,
                'pali': 'นาสสะ โจรา ปะสะหันติ',
                'pali_roman': 'nāssa corā pasahanti',
                'thai': '',
                'paiboon': '',
                'english': 'Thieves do not overpower him,',
            },
            {
                'number': 10,
                'pali': 'นาติมัญเญติ ขัตติโย',
                'pali_roman': 'nātimaññeti khattiyo',
                'thai': '',
                'paiboon': '',
                'english': 'the noble does not despise him,',
            },
            {
                'number': 11,
                'pali': 'สัพเพ อะมิตเต ตะระติ',
                'pali_roman': 'sabbe amitte tarati',
                'thai': '',
                'paiboon': '',
                'english': 'he overcomes all enemies —',
            },
            {
                'number': 12,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            # ‼ CHECK: สะฆะรัง transliterated faithfully as sagharaṃ. Some
            #          editions read สะคะรัง or set it as สะ ฆะรัง. Kept as
            #          printed.
            {
                'number': 13,
                'pali': 'อะกุทโธ สะฆะรัง เอติ',
                'pali_roman': 'akuddho sagharaṃ eti',
                'thai': '',
                'paiboon': '',
                'english': 'Unangered he comes to his home,',
            },
            {
                'number': 14,
                'pali': 'สะภายะ ปะฏินันทิโต',
                'pali_roman': 'sabhāya paṭinandito',
                'thai': '',
                'paiboon': '',
                'english': 'he is welcomed in the assembly,',
            },
            {
                'number': 15,
                'pali': 'ญาตีนัง อุตตะโม โหติ',
                'pali_roman': 'ñātīnaṃ uttamo hoti',
                'thai': '',
                'paiboon': '',
                'english': 'he is foremost among his kin —',
            },
            {
                'number': 16,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            {
                'number': 17,
                'pali': 'สักกัต์วา สักกะโต โหติ',
                'pali_roman': 'sakkatvā sakkato hoti',
                'thai': '',
                'paiboon': '',
                'english': 'Having honoured, he is honoured,',
            },
            {
                'number': 18,
                'pali': 'คะรุ โหติ สะคาระโว',
                'pali_roman': 'garu hoti sagāravo',
                'thai': '',
                'paiboon': '',
                'english': 'being reverent, he is held in respect,',
            },
            {
                'number': 19,
                'pali': 'วัณณะกิตติภะโต โหติ',
                'pali_roman': 'vaṇṇakittibhato hoti',
                'thai': '',
                'paiboon': '',
                'english': 'he bears praise and renown —',
            },
            {
                'number': 20,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            # ‼ CHECK: ปูชั่ง carries mai ek, which does not occur in Pali
            #          written in Thai script; the word is ปูชัง (pūjaṃ).
            #          Transliterated faithfully as pūjàṃ with the tone mark
            #          shown, rather than substituting. Almost certainly a
            #          mistyping and one of the clearest errors in the chant.
            {
                'number': 21,
                'pali': 'ปูชะโก ละภะเต ปูชั่ง',
                'pali_roman': 'pūjako labhate pūjàṃ',
                'thai': '',
                'paiboon': '',
                'english': 'Honouring, he obtains honour,',
            },
            {
                'number': 22,
                'pali': 'วันทะโก ปะฏิวันทะนัง',
                'pali_roman': 'vandako paṭivandanaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'saluting, he receives salutation,',
            },
            {
                'number': 23,
                'pali': 'ยะโสกิตติญจะ ปัปโปติ',
                'pali_roman': 'yasokittiñca pappoti',
                'thai': '',
                'paiboon': '',
                'english': 'he attains fame and renown —',
            },
            {
                'number': 24,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            # ‼ CHECK: อัคคิยะถา is printed solid, where the sense requires
            #          อัคคิ ยะถา, fire as. Reproduced as pasted; check whether
            #          the book separates them.
            {
                'number': 25,
                'pali': 'อัคคิยะถา ปัชชะละติ',
                'pali_roman': 'aggiyathā pajjalati',
                'thai': '',
                'paiboon': '',
                'english': 'He blazes forth as does a fire,',
            },
            {
                'number': 26,
                'pali': 'เทวะตาวะ วิโรจะติ',
                'pali_roman': 'devatāva virocati',
                'thai': '',
                'paiboon': '',
                'english': 'he shines as does a deva,',
            },
            # ‼ CHECK: อัชชะหิโต transliterated faithfully as ajjahito.
            #          Standard editions read อะชะหิโต (ajahito), not forsaken,
            #          with a single ช. Kept as printed.
            {
                'number': 27,
                'pali': 'สิริยา อัชชะหิโต โหติ',
                'pali_roman': 'siriyā ajjahito hoti',
                'thai': '',
                'paiboon': '',
                'english': 'he is not forsaken by good fortune —',
            },
            {
                'number': 28,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            {
                'number': 29,
                'pali': 'คาโว ตัสสะ ปะชายันติ',
                'pali_roman': 'gāvo tassa pajāyanti',
                'thai': '',
                'paiboon': '',
                'english': 'His cattle bear their young,',
            },
            {
                'number': 30,
                'pali': 'เขตเต วุตตัง วิรูหะติ',
                'pali_roman': 'khette vuttaṃ virūhati',
                'thai': '',
                'paiboon': '',
                'english': 'what is sown in the field grows up,',
            },
            # ‼ CHECK: ผะละมัสนาติ transliterated faithfully as phalamasnāti.
            #          Standard editions read ผะละมัสนาติ or ผะละมัสสะนาติ
            #          (phalamasnāti / phalamassanāti); the printed form is
            #          retained rather than adjusted.
            {
                'number': 31,
                'pali': 'วุตตานัง ผะละมัสนาติ',
                'pali_roman': 'vuttānaṃ phalamasnāti',
                'thai': '',
                'paiboon': '',
                'english': 'he enjoys the fruit of what was sown —',
            },
            {
                'number': 32,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            # ‼ CHECK: ทะริโต transliterated faithfully as darito. Standard
            #          editions read ทะริโต from darī, a cleft or chasm.
            #          Flagged because the sense depends on it and the English
            #          I supplied assumes that reading.
            {
                'number': 33,
                'pali': 'ทะริโต ปัพพะตาโต วา',
                'pali_roman': 'darito pabbatāto vā',
                'thai': '',
                'paiboon': '',
                'english': 'Fallen from a chasm or a mountain,',
            },
            {
                'number': 34,
                'pali': 'รุกขะโต ปะติโต นะโร',
                'pali_roman': 'rukkhato patito naro',
                'thai': '',
                'paiboon': '',
                'english': 'or a man fallen from a tree,',
            },
            {
                'number': 35,
                'pali': 'จุโต ปะติฏฐัง ละภะติ',
                'pali_roman': 'cuto patiṭṭhaṃ labhati',
                'thai': '',
                'paiboon': '',
                'english': 'though he fall, he finds a footing —',
            },
            {
                'number': 36,
                'pali': 'โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            # ‼ CHECK: วิรุฬหะมูละสันตานัง and its simile run across verses
            #          37–38, but the Pali order places the banyan's roots
            #          first and the wind second, while my English inverts them
            #          for sense. The pairing is by meaning; the Pali order is
            #          the book's.
            {
                'number': 37,
                'pali': 'วิรุฬหะมูละสันตานัง',
                'pali_roman': 'viruḷhamūlasantānaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'As the wind cannot overpower',
            },
            # ‼ CHECK: นิโครระมิวะ transliterated faithfully as nigorraramiva.
            #          Standard editions read นิโคฺรธะมิวะ (nigrodhamiva), the
            #          banyan tree. The printed form has ร ระ where ธ is
            #          expected, which looks like an OCR error. Kept as printed
            #          rather than substituted; this is the least secure line
            #          in the chant.
            {
                'number': 38,
                'pali': 'นิโครระมิวะ มาลุโต',
                'pali_roman': 'nigorraramiva māluto',
                'thai': '',
                'paiboon': '',
                'english': 'a banyan whose spreading roots have grown,',
            },
            {
                'number': 39,
                'pali': 'อะมิตตา นัปปะสะหันติ',
                'pali_roman': 'amittā nappasahanti',
                'thai': '',
                'paiboon': '',
                'english': 'so enemies do not overpower him —',
            },
            # ‼ CHECK: A stray double quotation mark follows the full stop:
            #          ทุพภะตีติ.". The same artefact has now appeared at the
            #          close of chants 8, 9 and the Mettānisaṃsasuttaṃ. Four
            #          occurrences across four pages; reproduced as pasted
            #          rather than tidied.
            {
                'number': 40,
                'pali': 'โย มิตตานัง นะ ทุพภะตีติ."',
                'pali_roman': 'yo mittānaṃ na dubbhatīti."',
                'thai': '',
                'paiboon': '',
                'english': 'he who does not betray his friends.',
            },
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 41,
                'pali': 'เมตตานิสังสะคาถา นิฏฐิตา.',
                'pali_roman': 'mettānisaṃsagāthā niṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': 'The verses on the benefits of loving-kindness are ended.',
            },
        ],
    },

    {
        # ‼ CHECK: The chant is incomplete. It stops at วักกัง, the tenth of
        #          the thirty-two parts. Twenty-two parts and any closing
        #          formula are missing. Do not put this entry in the app as a
        #          whole chant — the remainder needs pasting.
        # ‼ CHECK: The paste opens with several paragraphs of Thai commentary
        #          on items 2 to 5 of a numbered reflection, ending with the
        #          reference (อง. ปญฺจก. ๒๒๕๗/๖๖-๗๐). This belongs to the
        #          Abhiṇhapaccavekkhaṇa, the chant you sent earlier, not to
        #          this one. I have kept it entirely out of this entry. It also
        #          contains oddities of its own — บรรเท่า for บรรเทา in item 2,
        #          and a volume reference ๒๒๕๗ that does not look like a
        #          standard Aṅguttara citation — so if you want it attached to
        #          that chant it should be re-pasted and checked separately.
        # ‼ CHECK: From verse 7 onward the Pali and Thai columns have collapsed
        #          into each other in the paste, and the Thai runs in a
        #          different order from the Pali. The pasted Thai order is ผม,
        #          เล็บ, หนัง, เอ็น, เยื่อในกระดูก, then ขน, ฟัน, เนื้อ,
        #          กระดูก, ไต — an odd-then-even interleave, which is what a
        #          two-column layout does when it is read straight down. I kept
        #          your Pali in the printed order and paired each Thai term to
        #          it by meaning. Every one of verses 8 to 12 depends on that
        #          pairing and should be checked against the page.
        # ‼ CHECK: source left empty. The reference in the pasted commentary
        #          belongs to the previous chant, not to this one, so I have
        #          not carried it over.
        # ‼ CHECK: The book prints no section headings. The two sections and
        #          their names are my grouping, not the book's.
        # ‼ CHECK: The invitation reads ท์วัตติงสาการะปารัง. As in chant 1,
        #          ปารัง looks like a slip for ปาฐัง (pāṭhaṃ), which would
        #          agree with the title ปาโฐ. The same error in the same
        #          position in two different chants suggests a systematic fault
        #          in the source rather than a one-off. Reproduced as pasted
        #          and romanised faithfully as pāraṃ.
        # ‼ CHECK: This object continues the previous entry and numbers from
        #          13. Verses 13 to 34 belong to the section อัตถิ อิมัส์มิง
        #          กาเย opened at verse 6 of the first half, so they carry no
        #          section key; if the two halves are loaded separately, verse
        #          13 will have no section above it.
        # ‼ CHECK: The parts now total exactly thirty-two — ten in the first
        #          paste, twenty-two here — which matches the title. Nothing
        #          appears to have been dropped between the two pastes.
        # ‼ CHECK: The paste continues past the end of this chant into a new
        #          one, ภาระสุตตะคาถา, giving its invitation and four verses
        #          (ภารา หะเว ปัญจักขันธา through ภาระนิกเขปะนัง สุขัง). I have
        #          kept all of it out of this entry. It is also incomplete —
        #          the chant continues beyond ภาระนิกเขปะนัง สุขัง — so please
        #          re-paste it whole and I will do it as its own entry.
        # ‼ CHECK: source left empty. No footnote or attribution appears in
        #          either half of what you pasted.
        # ‼ CHECK: (raised here, not in the stage-1 notes) The two halves of
        #          this chant were supplied separately and have been merged
        #          into this one entry. The first paragraph of `background`
        #          below therefore still opens "This completes the enumeration
        #          begun in the previous paste" — wording about how the text
        #          reached us, which a reader of the finished book has no way
        #          to follow. Left exactly as written rather than reworded;
        #          it needs one sentence from Josh.

        'id': 'dvattimsakara-patha',
        'title_thai': 'ท์วัตติงสาการะปาโฐ',
        'title_pali': 'Dvattiṃsākārapāṭho',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Passage on the Thirty-Two Parts of the Body',
        # Left empty on purpose. The only reference in the pasted block
        # belongs to the preceding chant, not to this one, so it has not
        # been carried over and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        'summary': (
            "A reflection on the body from the soles of the feet up and the "
            "crown of the hair down: bounded by skin, full of impurities, and "
            "enumerated part by part."
        ),

        'when_chanted': (
            "Recited as a reflection on the body, commonly in the evening "
            "service and as a support for meditation on its constituent "
            "parts."
        ),

        'background': [
            "This is one of the oldest and most widely used reflections in "
            "the tradition, and the Thai chanting books print it in a fixed "
            "shape: a preamble that frames the body as a bounded, impure "
            "whole, followed by the enumeration of its thirty-two parts. The "
            "parts are chanted as a bare list, each with its Thai gloss "
            "beneath.",

            "This completes the enumeration begun in the previous paste. The "
            "list runs from the liver through the solid organs, then through "
            "the twelve liquids, and ends with the brain in the skull — the "
            "part that some older recensions omit, giving thirty-one, and "
            "that the Thai books consistently include.",

            "The chant then returns to its opening. The same four lines that "
            "framed the body before the list are repeated after it, with "
            "เอวะมะยัง, thus is this, in place of อะยัง โข, this indeed. The "
            "reflection is therefore circular by design: the survey is "
            "stated, the evidence is given, and the survey is stated again, "
            "now with the list standing behind it.",
        ],

        'meaning': [
            "The preamble establishes the boundaries of what is to be "
            "examined before naming anything within them. This body of mine, "
            "from the soles of the feet upward, from the crown of the hair "
            "downward, bounded all round by skin. The two directions are "
            "given so that nothing is left outside the survey, and the skin "
            "is named not as a covering but as a limit — that which encloses "
            "what follows.",

            "Only then does the judgement come: full of impurities of various "
            "kinds. The Thai keeps this in the plainest possible terms, "
            "ของไม่สะอาด, things not clean. Nothing is said about the body's "
            "ugliness in the abstract; the claim is about contents, and the "
            "list that follows is the evidence.",

            "The enumeration itself carries no adjectives. Head hair, body "
            "hair, nails, teeth, skin, flesh, sinews, bones, marrow, kidney — "
            "each named and no more. The reflection works by inventory rather "
            "than by rhetoric, and the practitioner is left to draw the "
            "conclusion from the list itself. The register of the Thai "
            "preserves this restraint exactly: เบื้องบนแต่พื้นเท้าขึ้นมา, an "
            "older construction than modern Thai would use, and no more "
            "emphatic than the Pali it renders.",

            "The second half of the list turns from what is solid to what is "
            "fluid. Bile, phlegm, pus, blood, sweat, fat, tears, grease, "
            "spittle, mucus, joint-fluid, urine. Twelve of the thirty-two "
            "parts are liquids, and the Thai marks each with น้ำ, water — "
            "น้ำดี, น้ำเหงื่อ, น้ำตา — so that the chanted list has an "
            "audible rhythm of its own in Thai that the Pali does not have.",

            "The last item is set apart by its construction. Where every "
            "other part is named in a single word, the brain is given as "
            "มัตถะเก มัตถะลุงคัง, the brain in the skull, with its location "
            "stated. The Thai expands this further to "
            "เยื่อมันสมองในกะโหลกศีรษะ. It is the innermost and least "
            "accessible of the parts, and the chant ends its inventory there.",

            "The closing recapitulation adds one word to what was said at the "
            "start: อย่างนี้, thus, in just this way. The body was described "
            "as full of impurities before the list was given; it is described "
            "so again afterwards, and the second statement rests on the first "
            "having been demonstrated part by part. Nothing new is asserted. "
            "The reflection simply asks that the same sentence be heard "
            "differently the second time.",
        ],

        # The leader's invitation. Pali, so it carries no Thai and no
        # Paiboon.
        'invitation': {
            'pali': 'หันทะ มะยัง ท์วัตติงสาการะปารัง ภะณามะ เส.',
            'pali_roman': 'handa mayaṃ dvattiṃsākārapāraṃ bhaṇāma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us recite the passage on the thirty-two parts.',
        },

        'verses': [
            {
                'section': 'อะยัง โข เม กาโย: The Body Surveyed',
                'number': 1,
                'pali': 'อะยัง โข เม กาโย,',
                'pali_roman': 'ayaṃ kho me kāyo,',
                'thai': 'กายของเรานี้แล,',
                'paiboon': 'gaai kɔ̌ɔŋ rao níi lɛɛ,',
                'english': 'This body of mine,',
            },
            {
                'number': 2,
                'pali': 'อุทธัง ปาทะตะลา,',
                'pali_roman': 'uddhaṃ pādatalā,',
                'thai': 'เบื้องบนแต่พื้นเท้าขึ้นมา,',
                'paiboon': 'bʉ̂aŋ bon dtɛ̀ɛ pʉ́ʉn táo kʉ̂n maa,',
                'english': 'from the soles of the feet upward,',
            },
            # ‼ CHECK: Pali reads อะโฮ. Standard editions read อะโธ (adho,
            #          downward), which is what the Thai เบื้องต่ำ requires —
            #          อะโฮ would mean something else entirely. Transliterated
            #          faithfully as aho rather than substituted. This is the
            #          clearest error in the chant and the ธ/ฮ confusion is a
            #          common reprint fault.
            {
                'number': 3,
                'pali': 'อะโฮ เกสะมัตถะกา,',
                'pali_roman': 'aho kesamatthakā,',
                'thai': 'เบื้องต่ำแต่ปลายผมลงไป,',
                'paiboon': 'bʉ̂aŋ dtàm dtɛ̀ɛ bplaai pǒm loŋ bpai,',
                'english': 'from the crown of the hair downward,',
            },
            {
                'number': 4,
                'pali': 'ตะจะปะริยันโต,',
                'pali_roman': 'tacapariyanto,',
                'thai': 'มีหนังหุ้มอยู่เป็นที่สุดรอบ,',
                'paiboon': 'mii nǎŋ hûm yùu bpen tîi-sùt rɔ̂ɔp,',
                'english': 'bounded all round by skin,',
            },
            # ‼ CHECK: The Thai ends with no punctuation, where the surrounding
            #          lines end with a comma. Reproduced as pasted.
            # ‼ CHECK: Thai reads ต่างๆ with the mai yamok. The Paiboon+
            #          renders the repetition in full as dtàaŋ dtàaŋ,
            #          consistent with the treatment of นั้น ๆ in chant 7.
            {
                'number': 5,
                'pali': 'ปูโร นานัปปะการัสสะ อะสุจิโน,',
                'pali_roman': 'pūro nānappakārassa asucino,',
                'thai': 'เต็มไปด้วยของไม่สะอาด มีประการต่างๆ',
                'paiboon': 'dtem bpai dûay kɔ̌ɔŋ mâi sà-àat mii bprà-gaan dtàaŋ dtàaŋ',
                'english': 'full of impurities of various kinds.',
            },
            # ‼ CHECK: อิมัส์มิง carries thanthakhat over ส์. Transliterated
            #          faithfully as imasmiṃ, which is the standard form; the
            #          mark placement should be confirmed, as it varies across
            #          this book.
            {
                'section': 'อัตถิ อิมัส์มิง กาเย: The Parts Enumerated',
                'number': 6,
                'pali': 'อัตถิ อิมัส์มิง กาเย,',
                'pali_roman': 'atthi imasmiṃ kāye,',
                'thai': 'ในร่างกายนี้มี,',
                'paiboon': 'nai râaŋ-gaai níi mii,',
                'english': 'In this body there are:',
            },
            {
                'number': 7,
                'pali': 'เกสา',
                'pali_roman': 'kesā',
                'thai': 'ผมทั้งหลาย,',
                'paiboon': 'pǒm táŋ-lǎai,',
                'english': 'hairs of the head,',
            },
            # ‼ CHECK: The Pali line prints two parts together (โลมา นะขา), and
            #          I have joined their two Thai glosses with a space to
            #          match. The Thai terms are yours as pasted; the joining
            #          is mine. Same treatment at verses 9, 10 and 11.
            {
                'number': 8,
                'pali': 'โลมา นะขา',
                'pali_roman': 'lomā nakhā',
                'thai': 'ขนทั้งหลาย, เล็บทั้งหลาย,',
                'paiboon': 'kǒn táŋ-lǎai, lép táŋ-lǎai,',
                'english': 'hairs of the body, nails,',
            },
            # ‼ CHECK: The Thai for these two parts comes from widely separated
            #          points in the pasted block — ฟันทั้งหลาย, from the tail
            #          and หนัง, from the middle — and the source prints
            #          ฟันทั้งหลาย,เนื้อ, run together with no space after the
            #          comma. Reproduced without that space where it falls, but
            #          the pairing here is the least secure in the entry.
            {
                'number': 9,
                'pali': 'ทันตา ตะโจ',
                'pali_roman': 'dantā taco',
                'thai': 'ฟันทั้งหลาย, หนัง,',
                'paiboon': 'fan táŋ-lǎai, nǎŋ,',
                'english': 'teeth, skin,',
            },
            {
                'number': 10,
                'pali': 'มังสัง นะหารู',
                'pali_roman': 'maṃsaṃ nahārū',
                'thai': 'เนื้อ, เอ็นทั้งหลาย,',
                'paiboon': 'nʉ́a, en táŋ-lǎai,',
                'english': 'flesh, sinews,',
            },
            {
                'number': 11,
                'pali': 'อัฏฐี อัฏฐิมิญชัง',
                'pali_roman': 'aṭṭhī aṭṭhimiñjaṃ',
                'thai': 'กระดูกทั้งหลาย, เยื่อในกระดูก,',
                'paiboon': 'grà-dùuk táŋ-lǎai, yʉ̂a nai grà-dùuk,',
                'english': 'bones, marrow of the bones,',
            },
            # ‼ CHECK: ไต is the last word in the paste and carries no
            #          punctuation, so it is not clear whether the chant
            #          continues on the same line in the book or breaks there.
            #          Reproduced as pasted.
            {
                'number': 12,
                'pali': 'วักกัง',
                'pali_roman': 'vakkaṃ',
                'thai': 'ไต',
                'paiboon': 'dtai',
                'english': 'kidney,',
            },
            # ‼ CHECK: The printed order runs ยะกะนัง then หะทะยัง. Standard
            #          editions give hadayaṃ before yakanaṃ. Kept as printed.
            {
                'number': 13,
                'pali': 'ยะกะนัง',
                'pali_roman': 'yakanaṃ',
                'thai': 'ตับ,',
                'paiboon': 'dtàp,',
                'english': 'liver,',
            },
            # ‼ CHECK: The Thai หัวใจ is printed before its Pali หะทะยัง, and
            #          ม้าม follows หะทะยัง ปิหะกัง run together. The columns
            #          have collapsed as they did in the first half. I kept the
            #          Pali in printed order and paired by meaning; verses 14
            #          and 15 depend on that pairing.
            {
                'number': 14,
                'pali': 'หะทะยัง',
                'pali_roman': 'hadayaṃ',
                'thai': 'หัวใจ,',
                'paiboon': 'hǔa-jai,',
                'english': 'heart,',
            },
            # ‼ CHECK: The printed order runs ปิหะกัง then กิโลมะกัง. Standard
            #          editions give kilomakaṃ before pihakaṃ. Kept as printed.
            {
                'number': 15,
                'pali': 'ปิหะกัง',
                'pali_roman': 'pihakaṃ',
                'thai': 'ม้าม,',
                'paiboon': 'máam,',
                'english': 'spleen,',
            },
            {
                'number': 16,
                'pali': 'กิโลมะกัง',
                'pali_roman': 'kilomakaṃ',
                'thai': 'พังผืด,',
                'paiboon': 'paŋ-pʉ̀ʉt,',
                'english': 'membranes,',
            },
            # ‼ CHECK: The printed order runs อันตัง then ปัปผาสัง. Standard
            #          editions give papphāsaṃ before antaṃ. Kept as printed.
            {
                'number': 17,
                'pali': 'อันตัง',
                'pali_roman': 'antaṃ',
                'thai': 'ไส้ใหญ่,',
                'paiboon': 'sâi yài,',
                'english': 'large intestine,',
            },
            {
                'number': 18,
                'pali': 'ปัปผาสัง',
                'pali_roman': 'papphāsaṃ',
                'thai': 'ปอด,',
                'paiboon': 'bpɔ̀ɔt,',
                'english': 'lungs,',
            },
            {
                'number': 19,
                'pali': 'อุทะริยัง',
                'pali_roman': 'udariyaṃ',
                'thai': 'อาหารใหม่,',
                'paiboon': 'aa-hǎan mài,',
                'english': 'undigested food,',
            },
            {
                'number': 20,
                'pali': 'อันตะคุณัง',
                'pali_roman': 'antaguṇaṃ',
                'thai': 'ไส้น้อย,',
                'paiboon': 'sâi nɔ́ɔy,',
                'english': 'small intestine,',
            },
            # ‼ CHECK: The printed order runs อุทะริยัง, อันตะคุณัง, ปิตตัง,
            #          กะรีสัง. Standard editions give antaguṇaṃ, udariyaṃ,
            #          karīsaṃ, then pittaṃ. Four consecutive parts differ from
            #          the standard sequence here; kept as printed throughout,
            #          but this cluster is worth checking as a group rather
            #          than line by line.
            {
                'number': 21,
                'pali': 'ปิตตัง',
                'pali_roman': 'pittaṃ',
                'thai': 'น้ำดี,',
                'paiboon': 'nám dii,',
                'english': 'bile,',
            },
            {
                'number': 22,
                'pali': 'กะรีสัง',
                'pali_roman': 'karīsaṃ',
                'thai': 'อาหารเก่า,',
                'paiboon': 'aa-hǎan gào,',
                'english': 'digested food,',
            },
            {
                'number': 23,
                'pali': 'เสมหัง',
                'pali_roman': 'semhaṃ',
                'thai': 'น้ำเสลด,',
                'paiboon': 'nám sà-lèet,',
                'english': 'phlegm,',
            },
            {
                'number': 24,
                'pali': 'ปุพโพ',
                'pali_roman': 'pubbo',
                'thai': 'น้ำหนอง,',
                'paiboon': 'nám nɔ̌ɔŋ,',
                'english': 'pus,',
            },
            {
                'number': 25,
                'pali': 'โลหิตัง',
                'pali_roman': 'lohitaṃ',
                'thai': 'น้ำเลือด,',
                'paiboon': 'nám lʉ̂at,',
                'english': 'blood,',
            },
            {
                'number': 26,
                'pali': 'เสโท',
                'pali_roman': 'sedo',
                'thai': 'น้ำเหงื่อ,',
                'paiboon': 'nám ŋʉ̀a,',
                'english': 'sweat,',
            },
            {
                'number': 27,
                'pali': 'เมโท',
                'pali_roman': 'medo',
                'thai': 'น้ำมันข้น,',
                'paiboon': 'nám-man kôn,',
                'english': 'solid fat,',
            },
            {
                'number': 28,
                'pali': 'อัสสุ',
                'pali_roman': 'assu',
                'thai': 'น้ำตา,',
                'paiboon': 'nám-dtaa,',
                'english': 'tears,',
            },
            {
                'number': 29,
                'pali': 'วะสา',
                'pali_roman': 'vasā',
                'thai': 'น้ำมันเหลว,',
                'paiboon': 'nám-man lěeo,',
                'english': 'liquid fat,',
            },
            # ‼ CHECK: เขโพ transliterated faithfully as khepo. Standard
            #          editions read เขโฬ (kheḷo, spittle), which is what the
            #          Thai น้ำลาย requires. ฬ misread as พ is a common reprint
            #          fault. Kept as printed.
            {
                'number': 30,
                'pali': 'เขโพ',
                'pali_roman': 'khepo',
                'thai': 'น้ำลาย,',
                'paiboon': 'nám-laai,',
                'english': 'spittle,',
            },
            # ‼ CHECK: สิงฆานิกา is spelled with น. Standard editions read
            #          สิงฆาณิกา with ณ (siṅghāṇikā). Transliterated faithfully
            #          as siṅghānikā rather than substituted.
            {
                'number': 31,
                'pali': 'สิงฆานิกา',
                'pali_roman': 'siṅghānikā',
                'thai': 'น้ำมูก,',
                'paiboon': 'nám-mûuk,',
                'english': 'mucus,',
            },
            {
                'number': 32,
                'pali': 'ละสิกา',
                'pali_roman': 'lasikā',
                'thai': 'น้ำไขข้อ,',
                'paiboon': 'nám kǎi kɔ̂ɔ,',
                'english': 'fluid of the joints,',
            },
            {
                'number': 33,
                'pali': 'มุตตัง',
                'pali_roman': 'muttaṃ',
                'thai': 'น้ำมูตร,',
                'paiboon': 'nám mûut,',
                'english': 'urine,',
            },
            # ‼ CHECK: The Thai ends with no punctuation, unlike every other
            #          part in the list, which ends with a comma. Reproduced as
            #          pasted.
            {
                'number': 34,
                'pali': 'มัตถะเก มัตถะลุงคัง,',
                'pali_roman': 'matthake matthaluṅgaṃ,',
                'thai': 'เยื่อมันสมองในกะโหลกศีรษะ',
                'paiboon': 'yʉ̂a man sà-mɔ̌ɔŋ nai gà-lòok sǐi-sà',
                'english': 'and the brain within the skull.',
            },
            # ‼ CHECK: The Thai กายของเรานี้อย่างนี้ ends with no punctuation,
            #          where the parallel opening line at verse 1 of the first
            #          half ended with a comma. Reproduced as pasted.
            {
                'section': 'เอวะมะยัง เม กาโย: The Closing Recapitulation',
                'number': 35,
                'pali': 'เอวะมะยัง เม กาโย,',
                'pali_roman': 'evamayaṃ me kāyo,',
                'thai': 'กายของเรานี้อย่างนี้',
                'paiboon': 'gaai kɔ̌ɔŋ rao níi yàaŋ níi',
                'english': 'Thus is this body of mine,',
            },
            # ‼ CHECK: ป่าทะตะลา carries mai ek, which does not occur in Pali
            #          written in Thai script; the word is ปาทะตะลา (pādatalā),
            #          and it appears correctly at verse 2 of the first half.
            #          Transliterated faithfully as pàdatalā with the tone mark
            #          shown. Clear mistyping.
            {
                'number': 36,
                'pali': 'อุทธัง ป่าทะตะลา,',
                'pali_roman': 'uddhaṃ pàdatalā,',
                'thai': 'เบื้องบนแต่พื้นเท้าขึ้นมา,',
                'paiboon': 'bʉ̂aŋ bon dtɛ̀ɛ pʉ́ʉn táo kʉ̂n maa,',
                'english': 'from the soles of the feet upward,',
            },
            # ‼ CHECK: This line reads อะโธ, correctly. The parallel line in
            #          the first half read อะโฮ, which I flagged there as an
            #          error. This paste confirms it: the same line is printed
            #          two ways in one chant, and อะโธ is the right one.
            {
                'number': 37,
                'pali': 'อะโธ เกสะมัตถะกา,',
                'pali_roman': 'adho kesamatthakā,',
                'thai': 'เบื้องต่ำแต่ปลายผมลงไป,',
                'paiboon': 'bʉ̂aŋ dtàm dtɛ̀ɛ bplaai pǒm loŋ bpai,',
                'english': 'from the crown of the hair downward,',
            },
            {
                'number': 38,
                'pali': 'ตะจะปะริยันโต,',
                'pali_roman': 'tacapariyanto,',
                'thai': 'มีหนังหุ้มอยู่เป็นที่สุดรอบ,',
                'paiboon': 'mii nǎŋ hûm yùu bpen tîi-sùt rɔ̂ɔp,',
                'english': 'bounded all round by skin,',
            },
            # ‼ CHECK: The Thai reads ต่าง ๆ อย่าง นี้แล with a space inside
            #          อย่างนี้. Reproduced as pasted. Note also that the first
            #          half printed ต่างๆ with no space before the yamok, where
            #          this one has ต่าง ๆ with a space — the same word set two
            #          ways.
            {
                'number': 39,
                'pali': 'ปูโร นานัปปะการัสสะ อะสุจิโน,',
                'pali_roman': 'pūro nānappakārassa asucino,',
                'thai': 'เต็มไปด้วยของไม่สะอาด มีประการต่าง ๆ อย่าง นี้แล',
                'paiboon': 'dtem bpai dûay kɔ̌ɔŋ mâi sà-àat mii bprà-gaan dtàaŋ dtàaŋ yàaŋ níi lɛɛ',
                'english': 'full of impurities of various kinds — thus it is.',
            },
        ],
    },

    {
        # ‼ CHECK: Layers 1 and 3 in this entry are my transcription from your
        #          two photographs, not text you pasted. Every Thai character
        #          is my reading of the printed page, which is a different kind
        #          of risk from the OCR errors in earlier chants. The whole
        #          entry needs reading against the book rather than
        #          spot-checking.
        # ‼ CHECK: The images are crops. Nothing above the title or below the
        #          final line is visible, so I cannot tell whether the book
        #          prints a closing ฯ, a นิฏฐิตา formula, a footnote, or a
        #          chant number. All are absent from the entry.
        # ‼ CHECK: source left empty. No footnote is visible in either crop.
        # ‼ CHECK: The book prints no section headings. The two sections and
        #          their names are my grouping, not the book's; they follow the
        #          two four-line stanzas as the page sets them.
        # ‼ CHECK: This chant appeared in truncated typed form at the tail of
        #          your previous paste, and the two versions differ in two
        #          places — see the checks on verses 3 and 4. Where they differ
        #          I have followed the photograph, since it is the source.
        # ‼ CHECK: (raised here, not in the stage-1 notes) The invitation is
        #          the only one in the book that carries its brackets INSIDE
        #          the text — `(หันทะ มะยัง ... เส.)` — while its romanised
        #          line has none. Every other chant stores the invitation
        #          unbracketed. Reproduced exactly as given rather than
        #          normalised, but the page will print the brackets on the
        #          Pali line and not on the romanisation beneath it, so this
        #          wants a decision either way.

        'id': 'bharasutta-gatha',
        'title_thai': 'ภาระสุตตะคาถา',
        'title_pali': 'Bhārasuttagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses of the Discourse on the Burden',
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        'summary': (
            "The five aggregates are a burden, the person their bearer; "
            "taking it up is suffering in the world, and setting it down is "
            "happiness."
        ),

        'when_chanted': (
            "Recited among the reflections on the five aggregates, and as a "
            "short teaching on clinging and its laying down."
        ),

        'background': [
            "These verses close a short discourse on the burden, in which the "
            "burden, its bearer, its taking up and its laying down are "
            "defined in turn. The chanting books print the verses alone, "
            "without the prose that precedes them, which is why the entry "
            "opens directly with ภารา หะเว.",

            "The Thai translation here is unusually colloquial in two places "
            "— เน้อ at the end of the first line and แหละ in the second are "
            "conversational particles rather than the literary vocabulary "
            "this register normally uses. Both are reproduced as printed. "
            "They give the opening a spoken, almost admonitory tone that the "
            "Pali does not itself carry.",
        ],

        'meaning': [
            "The first stanza states a proposition in four steps, each a bare "
            "equation. The five aggregates are a burden; the person is the "
            "bearer of that burden; taking the burden up is suffering in the "
            "world; setting the burden down is happiness. Nothing is argued. "
            "The verses simply name four things and let their arrangement do "
            "the work.",

            "The word ปุคคะโล in the second line has occupied commentators "
            "for a long time, since the discourse elsewhere denies a person "
            "as an ultimate entity while here naming one as the burden's "
            "bearer. The Thai renders it บุคคลแหละ, with the particle "
            "throwing emphasis onto the word — the person, precisely — rather "
            "than softening it. The verses are describing how the matter "
            "appears, not conceding a self.",

            "The second stanza describes the one who has finished. Having set "
            "down the heavy burden, he does not take up another; he has "
            "pulled out craving together with its root; he is without hunger "
            "and wholly quenched. The Thai adds พระอริยเจ้า, the noble one, "
            "naming the subject the Pali leaves implicit, and closes with "
            "ไม่มีส่วนเหลือ, with no remainder left. The sequence matters: "
            "not taking up another burden comes before the uprooting of "
            "craving, because the second is what makes the first possible.",
        ],

        # The leader's invitation. Pali, so it carries no Thai and no
        # Paiboon.
        'invitation': {
            'pali': '(หันทะ มะยัง ภาระสุตตะคาถาโย ภะณามะ เส.)',
            'pali_roman': 'handa mayaṃ bhārasuttagāthāyo bhaṇāma se.',
            'thai': '',
            'paiboon': '',
            'english': (
                "Now let us recite the verses of the discourse on the burden."
            ),
        },

        'verses': [
            # ‼ CHECK: The Thai ends with เน้อ, a colloquial spoken particle,
            #          in a text otherwise in formal literary register.
            #          Reproduced as printed rather than normalised; the
            #          Paiboon+ gives it as nə́ə.
            {
                'section': 'ภาระ: The Burden',
                'number': 1,
                'pali': 'ภารา หะเว ปัญจักขันธา,',
                'pali_roman': 'bhārā have pañcakkhandhā,',
                'thai': 'ขันธ์ทั้งห้า เป็นของหนักเน้อ,',
                'paiboon': 'kǎn táŋ hâa bpen kɔ̌ɔŋ nàk nə́ə,',
                'english': 'The five aggregates are indeed a burden,',
            },
            # ‼ CHECK: แหละ is likewise colloquial and unusual in this
            #          register. Reproduced as printed.
            {
                'number': 2,
                'pali': 'ภาระหาโร จะ ปุคคะโล,',
                'pali_roman': 'bhārahāro ca puggalo,',
                'thai': 'บุคคลแหละ เป็นผู้แบกของหนักพาไป,',
                'paiboon': 'bùk-kon lɛ̀ bpen pûu bɛ̀ɛk kɔ̌ɔŋ nàk paa bpai,',
                'english': 'and the person is the bearer who carries that burden along,',
            },
            # ‼ CHECK: The photograph reads ทุกขัง. Your earlier typed paste
            #          gave ทุกชัง, with ช. I have followed the image, which
            #          agrees with the standard reading dukkhaṃ, but the letter
            #          is worth confirming directly since ข and ช differ by one
            #          stroke at this print size.
            # ‼ CHECK: The Thai ends with a comma in the photograph. Your
            #          earlier typed paste gave a full stop after ในโลก. I have
            #          followed the image.
            # ‼ CHECK: In the photograph the Thai ทุกข์ carries a mark I could
            #          not resolve at this resolution — it may be the karan
            #          over ข์ or a print artefact. I transcribed it as ทุกข์.
            #          Check this character specifically.
            {
                'number': 3,
                'pali': 'ภาราทานัง ทุกขัง โลเก,',
                'pali_roman': 'bhārādānaṃ dukkhaṃ loke,',
                'thai': 'การแบกถือของหนัก เป็นความทุกข์ในโลก,',
                'paiboon': 'gaan bɛ̀ɛk tʉ̌ʉ kɔ̌ɔŋ nàk bpen kwaam túk nai lôok,',
                'english': 'The taking up of the burden is suffering in the world,',
            },
            {
                'number': 4,
                'pali': 'ภาระนิกเขปะนัง สุขัง,',
                'pali_roman': 'bhāranikkhepanaṃ sukhaṃ,',
                'thai': 'การสลัดของหนักทิ้งลงเสีย เป็นความสุข,',
                'paiboon': 'gaan sà-làt kɔ̌ɔŋ nàk tíŋ loŋ sǐa bpen kwaam sùk,',
                'english': 'and the setting down of the burden is happiness.',
            },
            # ‼ CHECK: นิกขิปิต์วา carries thanthakhat over ต์. Transliterated
            #          faithfully as nikkhipitvā. The same mark in the same
            #          position appeared in chant 1's ปิต์วา and in the
            #          Mettānisaṃsagāthā's สักกัต์วา.
            # ‼ CHECK: The Thai supplies พระอริยเจ้า, the noble one, where the
            #          Pali line has no explicit subject. The addition is the
            #          book's, not mine. My English follows the Pali and leaves
            #          the subject implicit; if you would rather the English
            #          track the Thai, this line needs rewording.
            {
                'section': 'นิกขิปิต์วา: The Laying Down',
                'number': 5,
                'pali': 'นิกขิปิต์วา คะรุง ภารัง,',
                'pali_roman': 'nikkhipitvā garuṃ bhāraṃ,',
                'thai': 'พระอริยเจ้า สลัดทิ้งของหนัก ลงเสียแล้ว,',
                'paiboon': 'prá à-rí-yá-jâo sà-làt tíŋ kɔ̌ɔŋ nàk loŋ sǐa lɛ́ɛo,',
                'english': 'Having set down the heavy burden,',
            },
            {
                'number': 6,
                'pali': 'อัญญัง ภารัง อะนาทิยะ,',
                'pali_roman': 'aññaṃ bhāraṃ anādiya,',
                'thai': 'ทั้งไม่หยิบฉวยเอาของหนักอันอื่น ขึ้นมาอีก,',
                'paiboon': 'táŋ mâi yìp chǔay ao kɔ̌ɔŋ nàk an ʉ̀ʉn kʉ̂n maa ìik,',
                'english': 'and taking up no other burden again,',
            },
            # ‼ CHECK: อัพพุยหะ transliterated as abbuyha. The ห here is the
            #          aspirate of the cluster -yh-, not a separate syllable;
            #          confirm the printed spelling has no vowel mark I have
            #          missed.
            {
                'number': 7,
                'pali': 'สะมูลัง ตัณหัง อัพพุยหะ,',
                'pali_roman': 'samūlaṃ taṇhaṃ abbuyha,',
                'thai': 'ก็เป็นผู้ถอนตัณหาขึ้นได้ กระทั่งราก,',
                'paiboon': 'gɔ̂ɔ bpen pûu tɔ̌ɔn dtan-hǎa kʉ̂n dâai grà-tâŋ râak,',
                'english': 'having drawn out craving together with its root,',
            },
            # ‼ CHECK: The chant ends with a full stop and no ฯ visible in the
            #          crop. Reproduced as transcribed.
            {
                'number': 8,
                'pali': 'นิจฉาโต ปะรินิพพุโต.',
                'pali_roman': 'nicchāto parinibbuto.',
                'thai': 'เป็นผู้หมดสิ่งปรารถนา ดับสนิทไม่มีส่วนเหลือ.',
                'paiboon': 'bpen pûu mòt sìŋ bpràat-tà-nǎa dàp sà-nìt mâi mii sùan lʉ̌a.',
                'english': 'he is without hunger, wholly quenched.',
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — Pali only. Every thai and paiboon field is empty. I have
        #          not supplied a translation from memory. This is the sixth
        #          chant in the run in this state.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It carries no
        #          authority from the source and should be treated as
        #          provisional.
        # ‼ CHECK: No invitation line is present. I have not written one.
        # ‼ CHECK: The book prints no section headings. All three sections and
        #          their names are my grouping by subject, not the book's.

        'id': 'pabbatopama-gatha',
        'title_thai': 'ปัพพะโตปะมะคาถา',
        'title_pali': 'Pabbatopamagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses on the Simile of the Mountain',
        'source': 'ขุ.สุ. 25/360-361, ส.ส. 15/315-6 — printed as footnotes 1 and 2 in the book, appearing mid-text in what you pasted. See checks.',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "As mountains reaching the sky would crush all before them from "
            "every quarter, so ageing and death roll over every being, sparing "
            "no rank."
        ),

        'when_chanted': (
            "Recited as a reflection on the inescapability of ageing and "
            "death, and on where a wise person places their trust in view of "
            "it."
        ),

        'background': [
            "The verses take their name from their opening simile and belong "
            "to a discourse addressed to a king. The image is of vast rocks "
            "touching the sky, advancing from all four directions and grinding "
            "down whatever lies between — a picture of something that cannot "
            "be met with force, treaty or wealth, which is precisely the point "
            "made of ageing and death in the stanzas that follow.",

            "The book gives two footnote references, one to the Sutta-nipāta "
            "and one to the Saṃyutta, which suggests the passage is either "
            "found in both places or that the two markers belong to different "
            "points on the page. Both are recorded in the source field as the "
            "book gives them.",

            "As with several preceding chants, no Thai rendering is printed, "
            "so this entry stands at two of the five layers and the English is "
            "my own off the Pali.",
        ],

        'meaning': [
            "The simile is built to exclude every escape in turn. The rocks "
            "are วิปุลา, vast; they reach the sky; they come from all four "
            "quarters; and they advance grinding everything down. Nothing is "
            "left outside their reach, and no direction offers a way out. Only "
            "after that picture is complete does the verse say เอวัง, just so "
            "— and name what the simile is about.",

            "What follows is a list of ranks: khattiya, brahmin, merchant, "
            "servant, outcaste and refuse-worker. The point of naming them is "
            "that the list makes no difference. Ageing and death spare none "
            "and crush all alike. Then three things that ordinarily do decide "
            "outcomes are dismissed in turn — there is no ground there for "
            "elephants, none for chariots, none for infantry, and no conquest "
            "by battle of spells or by wealth.",

            "The conclusion is drawn as advice rather than as lament. "
            "Therefore a wise person, seeing their own good, should settle "
            "faith in the Buddha, the Dhamma and the Saṅgha. And the one who "
            "lives by Dhamma in body, in speech and in mind is praised here in "
            "this very life and rejoices hereafter. The verses do not offer an "
            "escape from what the simile described; they offer the only thing "
            "that is not touched by it.",
        ],

        # The book prints no invitation line for this chant. The dict
        # stays with every field empty; the template checks it and skips
        # it, so an empty invitation is not the same as a missing one.
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },

        'verses': [
            # ‼ CHECK: ยะถาปี has a long ี where standard editions read ยะถาปิ
            #          (yathāpi). Transliterated faithfully as yathāpī rather
            #          than substituted.
            {
                'section': 'เสลา วิปุลา: The Simile of the Mountains',
                'number': 1,
                'pali': 'ยะถาปี เสลา วิปุลา',
                'pali_roman': 'yathāpī selā vipulā',
                'thai': '',
                'paiboon': '',
                'english': 'Just as vast rocks,',
            },
            {
                'number': 2,
                'pali': 'นะภัง อาหัจจะ ปัพพะตา',
                'pali_roman': 'nabhaṃ āhacca pabbatā',
                'thai': '',
                'paiboon': '',
                'english': 'mountains reaching to the sky,',
            },
            {
                'number': 3,
                'pali': 'สะมันตา อะนุปะริเยยยุง',
                'pali_roman': 'samantā anupariyeyyuṃ',
                'thai': '',
                'paiboon': '',
                'english': 'should advance from every side,',
            },
            # ‼ CHECK: จะตุททิสา transliterated as catuddisā. Standard editions
            #          agree; flagged only because the preceding word
            #          นิปโปเถนตา is spelled variously across editions
            #          (nippothentā / nipphothentā) and the pair should be
            #          checked together.
            {
                'number': 4,
                'pali': 'นิปโปเถนตา จะตุททิสา.',
                'pali_roman': 'nippothentā catuddisā.',
                'thai': '',
                'paiboon': '',
                'english': 'grinding down the four quarters —',
            },
            {
                'section': 'ชะรา จะ มัจจุ จะ: Ageing and Death',
                'number': 5,
                'pali': 'เอวัง ชะรา จะ มัจจุ จะ',
                'pali_roman': 'evaṃ jarā ca maccu ca',
                'thai': '',
                'paiboon': '',
                'english': 'just so do ageing and death',
            },
            {
                'number': 6,
                'pali': 'อะธิวัตตันติ ปาณิโน',
                'pali_roman': 'adhivattanti pāṇino',
                'thai': '',
                'paiboon': '',
                'english': 'roll over living beings:',
            },
            # ‼ CHECK: พ์ราห์มะเณ carries thanthakhat over พ์ and ห์. Chant 4
            #          gave พ์รัห์มะจาริโน and the Mettānisaṃsasuttaṃ gave
            #          พรห์มะโลกูปะโค — three spellings of the same element
            #          across the book. Transliterated as brāhma- throughout.
            {
                'number': 7,
                'pali': 'ขัตติเย พ์ราห์มะเณ เวสเส',
                'pali_roman': 'khattiye brāhmaṇe vesse',
                'thai': '',
                'paiboon': '',
                'english': 'nobles, brahmins, merchants,',
            },
            # ‼ CHECK: This line ends with no punctuation, where stanzas 1 and
            #          3 close with a full stop. Reproduced as pasted.
            {
                'number': 8,
                'pali': 'สุทเท จัณฑาละปุกกุเส',
                'pali_roman': 'sudde caṇḍālapukkuse',
                'thai': '',
                'paiboon': '',
                'english': 'servants, outcastes and refuse-workers.',
            },
            {
                'number': 9,
                'pali': 'นะ กิญจิ ปะริวัชเชติ',
                'pali_roman': 'na kiñci parivajjeti',
                'thai': '',
                'paiboon': '',
                'english': 'They spare nothing whatever,',
            },
            {
                'number': 10,
                'pali': 'สัพพะเมวาภิมัททะติ',
                'pali_roman': 'sabbamevābhimaddati',
                'thai': '',
                'paiboon': '',
                'english': 'they crush down all alike.',
            },
            # ‼ CHECK: หัตถี่นัง carries mai ek, again impossible in Pali; the
            #          word is หัตถีนัง (hatthīnaṃ). Reproduced as pasted. The
            #          same fault as verse 14 and as ป่าทะตะลา in the
            #          Dvattiṃsākāra — mai ek intruding into Pali is now a
            #          recurring fault in this source.
            {
                'number': 11,
                'pali': 'นะ ตัตถะ หัตถี่นัง ภูมิ',
                'pali_roman': 'na tattha hatthīnaṃ bhūmi',
                'thai': '',
                'paiboon': '',
                'english': 'There is no ground there for elephants,',
            },
            # ‼ CHECK: The footnote line 1. ขุ.สุ. 25/360-361 2. ส.ส. 15/315-6
            #          is printed between this verse and the next, as a page-
            #          foot footnote falling where the page broke. I kept it
            #          out of the verses and put both references in the source
            #          field. Two markers are given but I cannot tell from the
            #          paste which lines carry them; check whether both belong
            #          to this chant.
            {
                'number': 12,
                'pali': 'นะ ระถานัง นะ ปัตติยา.',
                'pali_roman': 'na rathānaṃ na pattiyā.',
                'thai': '',
                'paiboon': '',
                'english': 'none for chariots, none for infantry.',
            },
            # ‼ CHECK: Verses 13 to 22 are not in the order you pasted. Your
            #          paste gave five lines and then five more: นะ จาปิ /
            #          ตัสมา หิ / พุทเธ ธัมเม / โย ธัมมะจาริ / อิเธวะ นัง, then
            #          สักกา เชตุง / สัมปัสสัง / ธีโร สัทธัง / วาจายะ / เปจจะ
            #          สัคเค. I have interleaved them one from each run. The
            #          reason is that the second run cannot stand as
            #          consecutive lines — สักกา เชตุง ธะเนนะ ว่า completes the
            #          line before it rather than opening anything — and the
            #          pattern is what a two-column page gives when read down
            #          one column then the other. This is the single thing to
            #          check first: if the book sets these ten lines in one
            #          column, my order is wrong and yours is right.
            {
                'number': 13,
                'pali': 'นะ จาปิ มันตะยุทเธนะ',
                'pali_roman': 'na cāpi mantayuddhena',
                'thai': '',
                'paiboon': '',
                'english': 'Nor yet by battle of spells,',
            },
            # ‼ CHECK: ว่า carries mai ek, which does not occur in Pali written
            #          in Thai script; the word is วา (vā). Transliterated
            #          faithfully as vàa with the tone mark shown rather than
            #          substituted. Clear mistyping.
            {
                'number': 14,
                'pali': 'สักกา เชตุง ธะเนนะ ว่า',
                'pali_roman': 'sakkā jetuṃ dhanena vàa',
                'thai': '',
                'paiboon': '',
                'english': 'nor by wealth, can they be conquered.',
            },
            # ‼ CHECK: ตัสมา is written without thanthakhat. Chant 8 printed
            #          the same word both with and without the mark.
            #          Transliterated as tasmā either way.
            {
                'section': 'สัทธัง นิเวสะเย: Where Faith Is Placed',
                'number': 15,
                'pali': 'ตัสมา หิ ปัณฑิโต โปโส',
                'pali_roman': 'tasmā hi paṇḍito poso',
                'thai': '',
                'paiboon': '',
                'english': 'Therefore a wise person,',
            },
            # ‼ CHECK: A full stop falls here, mid-stanza in the interleaved
            #          reading, after สัมปัสสัง อัตถะมัตตะโน. If the book
            #          punctuates by couplet rather than by stanza this is
            #          expected; if not, it may indicate my ordering is wrong.
            #          Worth checking alongside the ordering question.
            {
                'number': 16,
                'pali': 'สัมปัสสัง อัตถะมัตตะโน.',
                'pali_roman': 'sampassaṃ atthamattano.',
                'thai': '',
                'paiboon': '',
                'english': 'seeing what is good for himself,',
            },
            {
                'number': 17,
                'pali': 'พุทเธ ธัมเม จะ สังเฆ จะ',
                'pali_roman': 'buddhe dhamme ca saṅghe ca',
                'thai': '',
                'paiboon': '',
                'english': 'in the Buddha, the Dhamma and the Saṅgha —',
            },
            {
                'number': 18,
                'pali': 'ธีโร สัทธัง นิเวสะเย',
                'pali_roman': 'dhīro saddhaṃ nivesaye',
                'thai': '',
                'paiboon': '',
                'english': 'let the steadfast one settle his faith.',
            },
            # ‼ CHECK: ธัมมะจาริ has a short final ิ where standard editions
            #          read ธัมมะจารี (dhammacārī). Transliterated faithfully
            #          as dhammacāri.
            {
                'number': 19,
                'pali': 'โย ธัมมะจาริ กาเยนะ',
                'pali_roman': 'yo dhammacāri kāyena',
                'thai': '',
                'paiboon': '',
                'english': 'Whoever lives by Dhamma in body,',
            },
            {
                'number': 20,
                'pali': 'วาจายะ อุทะ เจตะสา',
                'pali_roman': 'vācāya uda cetasā',
                'thai': '',
                'paiboon': '',
                'english': 'in speech, or in mind,',
            },
            {
                'number': 21,
                'pali': 'อิเธวะ นัง ปะสังสันติ',
                'pali_roman': 'idheva naṃ pasaṃsanti',
                'thai': '',
                'paiboon': '',
                'english': 'him they praise here in this very life,',
            },
            # ‼ CHECK: A stray apostrophe follows the full stop: ปะโมทะติ.'.
            #          The same artefact has now appeared at the close of
            #          chants 8, 9, the Mettānisaṃsasuttaṃ and the
            #          Mettānisaṃsagāthā. Five occurrences; reproduced as
            #          pasted rather than tidied.
            {
                'number': 22,
                'pali': "เปจจะ สัคเค ปะโมทะติ.'",
                'pali_roman': "pecca sagge pamodati.'",
                'thai': '',
                'paiboon': '',
                'english': 'and hereafter he rejoices in heaven.',
            },
            # ‼ CHECK: The closing formula ends with no full stop, where every
            #          other นิฏฐิตา line in the book has one. Reproduced as
            #          pasted.
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 23,
                'pali': 'ปัพพะโตปะมะคาถา นิฏฐิตา',
                'pali_roman': 'pabbatopamagāthā niṭṭhitā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The verses on the simile of the mountain are ended."
                ),
            },
        ],
    },

    {
        # ‼ CHECK: Layers 1 and 3 in this entry are my transcription from your
        #          photograph, not text you pasted. A misread character looks
        #          identical to a faithful one and I cannot flag it, so the
        #          whole entry needs reading against the book rather than spot-
        #          checking.
        # ‼ CHECK: No Thai translation layer exists on this page — both columns
        #          are Pali. Every thai and paiboon field is empty. I have not
        #          supplied a translation from memory.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It carries no
        #          authority from the source and should be treated as
        #          provisional.
        # ‼ CHECK: Each verse here is a full printed row, joining the left and
        #          right halves of the page with a single space. That is a
        #          layout judgement: the halves are two pādas of one line. If
        #          you want each pāda as its own verse the chant becomes twelve
        #          verses rather than six.
        # ‼ CHECK: The image is a crop. Nothing above the title or below the
        #          นิฏฐิตา line is visible, so I cannot tell whether the book
        #          gives this chant a number, as it did for 14 ปัพพะโตปะมะคาถา,
        #          or prints anything else on the page.
        # ‼ CHECK: No invitation line is present. I have not written one.
        # ‼ CHECK: The book prints no section headings. The three sections and
        #          their names are my grouping by subject, not the book's.

        'id': 'ariyadhana-gatha',
        'title_thai': 'อะริยะธะนะคาถา',
        'title_pali': 'Ariyadhanagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses on the Noble Wealth',
        # Left empty on purpose. The page carries a footnote marker
        # but the footnote itself falls below the crop, so no
        # attribution has been supplied from memory. See the CHECK
        # on the verse carrying the marker.
        'source': '',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "One whose faith is unshaken, whose virtue is good, who trusts the "
            "Saṅgha and sees uprightly, is called not poor, and his life is "
            "not in vain."
        ),

        'when_chanted': (
            "Recited among the reflections on the qualities that constitute a "
            "person's true wealth, and as an exhortation to the fourfold "
            "ground of faith, virtue, confidence and right view."
        ),

        'background': [
            "The noble wealth, ariyadhana, is a standard enumeration of the "
            "goods that cannot be lost to theft, fire or the state — usually "
            "given as seven, though these verses treat four of them: faith, "
            "virtue, confidence in the Saṅgha, and upright vision. The title "
            "of the chant names the whole category and the verses illustrate "
            "it.",

            "The page prints the chant in two columns, both Pali, with each "
            "printed row forming one complete line of the metre. There is no "
            "Thai translation on this page, so the entry stands at two of the "
            "five layers and the English is my own off the Pali.",
        ],

        'meaning': [
            "The first four lines build a single conditional sentence and "
            "withhold its conclusion until the end. Whose faith in the "
            "Tathāgata is unshaken and well established; whose virtue is good, "
            "dear to the noble ones and praised; who has confidence in the "
            "Saṅgha and whose seeing is upright — of such a person they say he "
            "is not poor.",

            "The force of the passage lies in that word. อะทะลิทโท, not poor, "
            "is a negation rather than a claim of riches, and it answers an "
            "assumption rather than making a boast. A person possessing none "
            "of the ordinary forms of wealth might be called destitute; these "
            "verses deny it, on the grounds of holdings of a different kind. "
            "The line that follows completes the thought without metaphor: his "
            "life is not in vain.",

            "The closing couplet turns the description into instruction. "
            "Therefore let the wise one pursue faith, virtue, confidence and "
            "the vision of Dhamma, remembering the teaching of the Buddhas. "
            "The four items are simply repeated from the first half in the "
            "same order, so the exhortation adds nothing new — it only asks "
            "that what has just been described be taken up.",
        ],

        # The book prints no invitation line for this chant. The dict
        # stays with every field empty; the template checks it and skips
        # it, so an empty invitation is not the same as a missing one.
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },

        'verses': [
            # ‼ CHECK: The first line begins indented on the page, further in
            #          than the lines below it. Reproduced as ordinary text;
            #          noted in case the indent carries meaning in the book's
            #          typography.
            {
                'section': 'อะริยะธะนะ: The Noble Wealth',
                'number': 1,
                'pali': 'ยัสสะ สัทธา ตะถาคะเต อะจะลา สุปะติฏฐิตา',
                'pali_roman': 'yassa saddhā tathāgate acalā supatiṭṭhitā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Whose faith in the Tathāgata is unshaken and well "
                    "established,"
                ),
            },
            # ‼ CHECK: กัล์ยาณัง carries thanthakhat over ล์. Transliterated
            #          faithfully as kalyāṇaṃ.
            # ‼ CHECK: This line ends with a comma where verses 4 and 6 end
            #          with a full stop and verses 1, 3 and 5 end with nothing.
            #          The punctuation is irregular across the six lines;
            #          reproduced exactly as printed rather than regularised.
            {
                'number': 2,
                'pali': 'สีลัญจะ ยัสสะ กัล์ยาณัง อะริยะกันตัง ปะสังสิตัง,',
                'pali_roman': 'sīlañca yassa kalyāṇaṃ ariyakantaṃ pasaṃsitaṃ,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "and whose virtue is good, dear to the noble ones and "
                    "praised,"
                ),
            },
            # ‼ CHECK: ยัสสัตถิ is printed solid, a sandhi of ยัสสะ อัตถิ.
            #          Transliterated as yassatthi, following the printed form.
            {
                'number': 3,
                'pali': 'สังเฆ ปะสาโท ยัสสัตถิ อุชุภูตัญจะ ทัสสะนัง',
                'pali_roman': 'saṅghe pasādo yassatthi ujubhūtañca dassanaṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "who has confidence in the Saṅgha, and whose seeing is "
                    "upright —"
                ),
            },
            # ‼ CHECK: อะโมฆันตัสสะ is printed solid, a sandhi of อะโมฆัง
            #          ตัสสะ. Transliterated as amoghantassa, following the
            #          printed form.
            {
                'number': 4,
                'pali': 'อะทะลิทโทติ ตัง อาหุ อะโมฆันตัสสะ ชีวิตัง.',
                'pali_roman': 'adaliddoti taṃ āhu amoghantassa jīvitaṃ.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "him they call not poor, and his life is not in vain."
                ),
            },
            # ‼ CHECK: ตัส์มา carries thanthakhat over ส์ here. Chant 8 printed
            #          the same word both with and without the mark and chant
            #          14 printed it without. Three settings of one word across
            #          the book; transliterated as tasmā in all cases.
            {
                'section': 'อะนุยุญเชถะ: The Exhortation',
                'number': 5,
                'pali': 'ตัส์มา สัทธัญจะ สีลัญจะ ปะสาทัง ธัมมะทัสสะนัง',
                'pali_roman': 'tasmā saddhañca sīlañca pasādaṃ dhammadassanaṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Therefore faith and virtue, confidence and the vision of "
                    "Dhamma —"
                ),
            },
            # ‼ CHECK: A superscript 2 follows the full stop after สาสะนันติ,
            #          marking a footnote. The footnote text itself is below
            #          the crop and is not in this entry, so the source field
            #          is empty even though the book evidently gives a
            #          reference. This is worth retrieving — it is the one
            #          thing on the page I know exists and cannot see.
            # ‼ CHECK: พุทธานะ transliterated as buddhāna. Standard editions
            #          read buddhāna in this metre; flagged only because the
            #          expected genitive plural buddhānaṃ differs by a final ṃ
            #          that would be easy to lose at this print size.
            {
                'number': 6,
                'pali': 'อะนุยุญเชถะ เมธาวี สะรัง พุทธานะ สาสะนันติ.',
                'pali_roman': 'anuyuñjetha medhāvī saraṃ buddhāna sāsananti.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "let the wise one pursue them, remembering the teaching of "
                    "the Buddhas."
                ),
            },
            # ‼ CHECK: The closing formula ends with no full stop, as did the
            #          นิฏฐิตา line of chant 14. Reproduced as transcribed.
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 7,
                'pali': 'อะริยะธะนะคาถา นิฏฐิตา',
                'pali_roman': 'ariyadhanagāthā niṭṭhitā',
                'thai': '',
                'paiboon': '',
                'english': 'The verses on the noble wealth are ended.',
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — Pali only. Every thai and paiboon field is empty. I have
        #          not supplied a translation from memory.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It carries no
        #          authority from the source.
        # ‼ CHECK: This chant is prose and the source prints it as continuous
        #          text. My division into 24 units follows the book's own
        #          commas, but the choice of where a unit ends is mine, not a
        #          line break in the book.
        # ‼ CHECK: Three footnote lines fall between the two vāras and are
        #          printed in the order 1, 3, 2 — ส.ส. 15/148, then ขุ.อุ.
        #          25/73-4 วิ. มหา. 4/1, then อง. จตุกก. 21/74 อง. ปญฺจก.
        #          22/59. I kept them out of the verses and recorded all three
        #          in the source field in numerical order. Which marker
        #          attaches to which line is not recoverable from the paste.
        # ‼ CHECK: The paste continues past this chant into พุทธะอุทานะคาถา, a
        #          complete chant with its own title, three stanzas, a นิฏฐิตา
        #          line and two footnote lines of its own. I have held all of
        #          it back. Re-send it and I will do it as its own entry — no
        #          need to re-type, the text you sent is complete.
        # ‼ CHECK: The two footnote lines at the very end of the paste belong
        #          to พุทธะอุทานะคาถา, not to this chant, and are duplicates of
        #          each other numbered 1 and 4 with slightly different
        #          punctuation. Held back with that chant; worth checking why
        #          one reference carries two numbers.
        # ‼ CHECK: No invitation line is present. I have not written one.

        'id': 'paticcasamuppada-patho',
        'title_thai': 'ปะฏิจจะสะมุปปาทะปาโฐ',
        'title_pali': 'Paṭiccasamuppādapāṭho',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Passage on Dependent Origination',
        'source': 'ส.ส. 15/148, อง. จตุกก. 21/74 อง. ปญฺจก. 22/59, ขุ.อุ. 25/73-4 วิ. มหา. 4/1 — printed as footnotes 1, 2 and 3, though they appear on the page in the order 1, 3, 2. See checks.',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "The twelve links stated forward, from ignorance to the whole mass "
            "of suffering, and then in reverse, from the fading of ignorance "
            "to its cessation."
        ),

        'when_chanted': (
            "Recited as a statement of the doctrine of dependent origination, "
            "in both its forward and its reverse order."
        ),

        'background': [
            "This is the doctrinal formula rather than a devotional text, and "
            "the book prints it in the two movements the tradition always "
            "pairs: the samudayavāra, the section on origination, and the "
            "nirodhavāra, the section on cessation. Each states the same "
            "twelve links, the second simply negating the first at every step.",

            "The book supplies its own headings here, which is unusual in this "
            "collection — most of the chants you have sent print none. It also "
            "gives three footnote references, placed between the two sections, "
            "pointing to the Saṃyutta, the Aṅguttara and the Udāna with a "
            "Vinaya parallel.",

            "No Thai rendering is printed, so this entry stands at two of the "
            "five layers and the English is my own off the Pali.",
        ],

        'meaning': [
            "The forward sequence names twelve conditions, each arising in "
            "dependence on the one before: ignorance, formations, "
            "consciousness, name-and-form, the six sense bases, contact, "
            "feeling, craving, clinging, becoming, birth, and then ageing-and- "
            "death together with sorrow, lamentation, pain, grief and despair. "
            "The formula does not say that one link causes the next in the "
            "ordinary sense; it says ปัจจะยา, with that as condition, which is "
            "a weaker and more exact claim.",

            "The closing line of each vāra is the one that states what the "
            "list is for: thus is the arising of this whole mass of suffering. "
            "The word เกวะลัสสะ, entire, matters — the twelve links are not a "
            "partial account to be supplemented by something else, and no "
            "cause outside the sequence is being held in reserve.",

            "The reverse order changes one thing only. From the remainderless "
            "fading away and cessation of ignorance comes the cessation of "
            "formations, and so through all twelve. Nothing is added and no "
            "method is described; the second vāra simply demonstrates that the "
            "sequence is a chain rather than a fate, since removing the first "
            "term removes every term after it. That structural point is the "
            "whole argument of the passage.",
        ],

        # The book prints no invitation line for this chant. The dict
        # stays with every field empty; the template checks it and skips
        # it, so an empty invitation is not the same as a missing one.
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },

        'verses': [
            # ‼ CHECK: The chant is numbered 15. in the source, following 14
            #          ปัพพะโตปะมะคาถา. Taken as the book's chant number and
            #          left out of title_thai.
            {
                'section': 'สมุทะยะวาระ: The Section on Origination',
                'number': 1,
                'pali': 'อะวิชชาปัจจะยา สังขารา,',
                'pali_roman': 'avijjāpaccayā saṅkhārā,',
                'thai': '',
                'paiboon': '',
                'english': 'With ignorance as condition, formations;',
            },
            {
                'number': 2,
                'pali': 'สังขาระปัจจะยา วิญญาณัง,',
                'pali_roman': 'saṅkhārapaccayā viññāṇaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'with formations as condition, consciousness;',
            },
            {
                'number': 3,
                'pali': 'วิญญาณะปัจจะยา นามะรูปัง,',
                'pali_roman': 'viññāṇapaccayā nāmarūpaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'with consciousness as condition, name-and-form;',
            },
            # ‼ CHECK: สะพายะตะนัง should read สะฬายะตะนัง (saḷāyatanaṃ), the
            #          six sense bases. ฬ has been misread as พ. This error
            #          runs through every occurrence — verses 4, 5, 16 and 17 —
            #          and I have transliterated all of them faithfully as
            #          sabāyatana- rather than substituting. Four instances of
            #          one fault; correct them as a group.
            {
                'number': 4,
                'pali': 'นามะรูปะปัจจะยา สะพายะตะนัง,',
                'pali_roman': 'nāmarūpapaccayā sabāyatanaṃ,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "with name-and-form as condition, the six sense bases;"
                ),
            },
            {
                'number': 5,
                'pali': 'สะพายะตะนะปัจจะยา ผัสโส,',
                'pali_roman': 'sabāyatanapaccayā phasso,',
                'thai': '',
                'paiboon': '',
                'english': 'with the six sense bases as condition, contact;',
            },
            {
                'number': 6,
                'pali': 'ผัสสะปัจจะยา เวทะนา,',
                'pali_roman': 'phassapaccayā vedanā,',
                'thai': '',
                'paiboon': '',
                'english': 'with contact as condition, feeling;',
            },
            {
                'number': 7,
                'pali': 'เวทะนาปัจจะยา ตัณหา,',
                'pali_roman': 'vedanāpaccayā taṇhā,',
                'thai': '',
                'paiboon': '',
                'english': 'with feeling as condition, craving;',
            },
            {
                'number': 8,
                'pali': 'ตัณหาปัจจะยา อุปาทานัง,',
                'pali_roman': 'taṇhāpaccayā upādānaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'with craving as condition, clinging;',
            },
            {
                'number': 9,
                'pali': 'อุปาทานะปัจจะยา ภะโว,',
                'pali_roman': 'upādānapaccayā bhavo,',
                'thai': '',
                'paiboon': '',
                'english': 'with clinging as condition, becoming;',
            },
            {
                'number': 10,
                'pali': 'ภะวะปัจจะยา ชาติ,',
                'pali_roman': 'bhavapaccayā jāti,',
                'thai': '',
                'paiboon': '',
                'english': 'with becoming as condition, birth;',
            },
            # ‼ CHECK: สัมภะวันตี has a long ี where standard editions read
            #          สัมภะวันติ (sambhavanti). Transliterated faithfully with
            #          the long vowel.
            {
                'number': 11,
                'pali': 'ชาติปัจจะยา ชะรามะระณัง โสกะปะริเทวะทุกขะโทมะนัสสุปายาสา สัมภะวันตี,',
                'pali_roman': (
                    "jātipaccayā jarāmaraṇaṃ sokaparidevadukkhadomanassupāyāsā "
                    "sambhavantī,"
                ),
                'thai': '',
                'paiboon': '',
                'english': (
                    "with birth as condition, ageing-and-death, sorrow, "
                    "lamentation, pain, grief and despair come to be."
                ),
            },
            # ‼ CHECK: A stray double quotation mark follows the full stop, and
            #          the same appears at verse 24. The artefact has now
            #          occurred at the close of six chants in this run.
            #          Reproduced as pasted rather than tidied.
            {
                'number': 12,
                'pali': 'เอวะเมตัสสะ เกวะลัสสะ ทุกขักขันธัสสะ สะมุทะโย โหติ."',
                'pali_roman': (
                    'evametassa kevalassa dukkhakkhandhassa samudayo hoti."'
                ),
                'thai': '',
                'paiboon': '',
                'english': (
                    "Thus is the arising of this entire mass of suffering."
                ),
            },
            # ‼ CHECK: อะวิชชายะเต็ววะ carries mai taikhu (◌็), which does not
            #          occur in Pali written in Thai script. The expected form
            #          is อะวิชชายะเต๎ววะ with yamakkan, giving avijjāyatveva.
            #          Transliterated as avijjāyatevva, following the letters
            #          as printed. The same class of fault as the intrusive mai
            #          ek in ว่า and ป่าทะตะลา earlier in the run.
            # ‼ CHECK: The section headings สมุทะยะวาระ and นิโรธะวาระ are the
            #          book's own, not my grouping. This is the first chant in
            #          the run where the source supplies them; the section
            #          values pair each with an English rendering per your
            #          convention.
            {
                'section': 'นิโรธะวาระ: The Section on Cessation',
                'number': 13,
                'pali': 'อะวิชชายะเต็ววะ อะเสสะวิราคะนิโรธา สังขาระนิโรโธ,',
                'pali_roman': (
                    "avijjāyatevva asesavirāganirodhā saṅkhāranirodho,"
                ),
                'thai': '',
                'paiboon': '',
                'english': (
                    "From the remainderless fading away and cessation of that "
                    "very ignorance, the cessation of formations;"
                ),
            },
            {
                'number': 14,
                'pali': 'สังขาระนิโรธา วิญญาณะนิโรโธ,',
                'pali_roman': 'saṅkhāranirodhā viññāṇanirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of formations, the cessation of "
                    "consciousness;"
                ),
            },
            {
                'number': 15,
                'pali': 'วิญญาณะนิโรธา นามะรูปะนิโรโธ,',
                'pali_roman': 'viññāṇanirodhā nāmarūpanirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of consciousness, the cessation of "
                    "name-and-form;"
                ),
            },
            {
                'number': 16,
                'pali': 'นามะรูปะนิโรธา สะพายะตะนะนิโรโธ,',
                'pali_roman': 'nāmarūpanirodhā sabāyatananirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of name-and-form, the cessation of the "
                    "six sense bases;"
                ),
            },
            {
                'number': 17,
                'pali': 'สะพายะตะนะนิโรธา ผัสสะนิโรโธ,',
                'pali_roman': 'sabāyatananirodhā phassanirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of the six sense bases, the cessation "
                    "of contact;"
                ),
            },
            # ‼ CHECK: เวทะนานิโรโฮ ends in ฮ where every parallel form ends in
            #          ธ; the word is เวทะนานิโรโธ (vedanānirodho).
            #          Transliterated faithfully. The same ธ/ฮ confusion
            #          produced อะโฮ for อะโธ in the Dvattiṃsākāra, so it is a
            #          recurring fault in this source.
            # ‼ CORRECTED: pali_roman  vedanāniroh[U+043E] → vedanāniroho.
            #              The final letter was a CYRILLIC small o (U+043E), not
            #              a Latin o — visually identical, but it breaks search,
            #              sorting and any audio generation keyed on this string.
            #              Not a reading from the book: it entered through the
            #              stage-1 JSON, was found during verification, and is
            #              pipeline corruption rather than evidence. The roh/rodh
            #              fault noted above is UNAFFECTED and still stands for
            #              checking against the printed page.
            {
                'number': 18,
                'pali': 'ผัสสะนิโรธา เวทะนานิโรโฮ,',
                'pali_roman': 'phassanirodhā vedanāniroho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of contact, the cessation of feeling;"
                ),
            },
            {
                'number': 19,
                'pali': 'เวทะนานิโรธา ตัณหานิโรโธ,',
                'pali_roman': 'vedanānirodhā taṇhānirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of feeling, the cessation of craving;"
                ),
            },
            {
                'number': 20,
                'pali': 'ตัณหานิโรธา อุปาทานะนิโรโธ,',
                'pali_roman': 'taṇhānirodhā upādānanirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of craving, the cessation of clinging;"
                ),
            },
            {
                'number': 21,
                'pali': 'อุปาทานะนิโรธา ภะวะนิโรโธ,',
                'pali_roman': 'upādānanirodhā bhavanirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of clinging, the cessation of "
                    "becoming;"
                ),
            },
            {
                'number': 22,
                'pali': 'ภะวะนิโรธา ชาตินิโรโธ,',
                'pali_roman': 'bhavanirodhā jātinirodho,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of becoming, the cessation of birth;"
                ),
            },
            # ‼ CHECK: นิรุชมันติ should read นิรุชฌันติ (nirujjhanti), they
            #          cease. ฌ has been misread as ม. Transliterated
            #          faithfully as nirujamanti. Without this word the line
            #          has no verb, so the reading is not in doubt — only the
            #          printed form.
            {
                'number': 23,
                'pali': 'ชาตินิโรธา ชะรามะระณัง โสกะปะริเทวะทุกขะโทมะนัสสุปายาสา นิรุชมันติ,',
                'pali_roman': (
                    "jātinirodhā jarāmaraṇaṃ sokaparidevadukkhadomanassupāyāsā "
                    "nirujamanti,"
                ),
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of birth, ageing-and-death, sorrow, "
                    "lamentation, pain, grief and despair cease."
                ),
            },
            {
                'number': 24,
                'pali': 'เอวะเมตัสสะ เกวะลัสสะ ทุกขักขันธัสสะ นิโรโธ โหติ."',
                'pali_roman': (
                    'evametassa kevalassa dukkhakkhandhassa nirodho hoti."'
                ),
                'thai': '',
                'paiboon': '',
                'english': (
                    "Thus is the cessation of this entire mass of suffering."
                ),
            },
        ],
    },

    {
        # ‼ CHECK: PROVENANCE — READ THIS FIRST. This entry did not come from
        #          stage 1. The Thai-script Pali is yours, taken from the block
        #          you pasted with the Paṭiccasamuppādapāṭho, and it has been
        #          copied character for character. But the romanised Pali, the
        #          English, the section headings, the summary, the background,
        #          the meaning and these checks are all Claude's own work, done
        #          in the absence of a stage-1 pass. Nothing here carries the
        #          authority the other entries' layers carry. If you later run
        #          this chant through stage 1, the two versions should be
        #          diffed before either is trusted.
        # ‼ CHECK: No Thai translation layer exists in what you pasted — Pali
        #          only. Every thai and paiboon field is empty; nothing has
        #          been supplied from memory.
        # ‼ CHECK: VERSE DIVISION IS A JUDGEMENT. I have set one pāda per
        #          verse, giving twelve lines plus the closing formula. The
        #          Ariyadhanagāthā was set the other way, two pādas joined per
        #          verse, on the evidence that the book prints gāthā in two
        #          columns. If this page is set in two columns the same way,
        #          this chant should be six verses plus the closing formula,
        #          not thirteen. I had no image of the page, so I followed your
        #          structure rule that short verses stay short. Say the word
        #          and I will re-split it.
        # ‼ CHECK: The three section headings are mine, not the book's, and
        #          their Thai is taken from words inside the verses themselves
        #          rather than from any heading printed on the page.
        # ‼ CHECK: No invitation line is present in what you pasted. I have not
        #          written one.
        # ‼ CHECK: The book prints two footnote lines for this chant and they
        #          are near-duplicates of each other, numbered 1 and 4: 'ขุ.อุ.
        #          25/74-5-6, วิ. มหา. 4/2-3-4' and 'ขุ. อุ. 25/74-5-6. วิ.
        #          มหา.4/2-3-4', differing only in spacing and in comma versus
        #          full stop. I have put the first in the source field and left
        #          the second out. Worth checking why one reference carries two
        #          footnote numbers.

        'id': 'buddhaudana-gatha',
        'title_thai': 'พุทธะอุทานะคาถา',
        'title_pali': 'Buddhaudānagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': "The Verses of the Buddha's Utterance of Joy",
        'source': 'ขุ.อุ. 25/74-5-6, วิ. มหา. 4/2-3-4',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "Three stanzas sharing an opening: when things become plain to the "
            "ardent meditator, doubt ends — through knowing causes, through "
            "knowing the destruction of conditions, and by standing as the sun "
            "scattering the host of Māra."
        ),

        'when_chanted': (
            "Recited as a recollection of the Buddha's awakening, the three "
            "utterances traditionally placed in the three watches of the night "
            "beneath the Bodhi tree."
        ),

        'background': [
            "These are the first three utterances of the Udāna, spoken in the "
            "days immediately following the awakening. The tradition places "
            "them in the three watches of a single night, and the book's "
            "footnote points to the Udāna together with its Vinaya parallel, "
            "where the same verses open the account of the Buddha's first "
            "weeks after enlightenment.",

            "The three stanzas are built on repetition. The first two lines "
            "are identical in all three, and the third line is identical in "
            "the first two, so what changes is only the ending — which is "
            "where each stanza's point lies. The book prints the repeated "
            "lines out in full rather than abbreviating them.",

            "No Thai rendering is printed on this page, so the entry stands at "
            "two of the five layers.",
        ],

        'meaning': [
            "The shared opening sets the condition: when things become "
            "manifest to a brahmin who is ardent and meditating. The word used "
            "for the practitioner is พ์ราห์มะณัสสะ, brahmin — not in the sense "
            "of birth or caste, but in the sense the Buddha regularly gave the "
            "word, of one who has actually done the work.",

            "The first stanza ends with knowing things together with their "
            "causes, สะเหตุธัมมัง. The second ends with knowing the "
            "destruction of those conditions, ขะยัง ปัจจะยานัง. These are the "
            "two halves of dependent origination, arising and cessation, which "
            "is why the book places these verses immediately after the "
            "Paṭiccasamuppādapāṭho — the previous chant states the formula, "
            "and this one records what it was like to see it.",

            "The third stanza changes shape. Instead of naming something "
            "known, it gives an image: he stands scattering the host of Māra, "
            "like the sun lighting up the sky. Nothing is added to the "
            "doctrine; what is added is what the knowing looks like from "
            "outside. The first two stanzas say what was understood, and the "
            "third says what such understanding does.",
        ],

        # The book prints no invitation line for this chant. The dict
        # stays with every field empty; the template checks it and skips
        # it, so an empty invitation is not the same as a missing one.
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },

        'verses': [
            # ‼ CHECK: The title พุทธะอุทานะคาถา has been transliterated as
            #          Buddhaudānagāthā, following the printed letters.
            #          Standard editions would contract this to
            #          Buddhudānagāthā. Following the book rather than the
            #          standard, as with cetiyāni elsewhere in this collection.
            {
                'section': 'สะเหตุธัมมัง: Things Together With Their Causes',
                'number': 1,
                'pali': 'ยะทา หะเว ปาตุภะวันติ ธัมมา',
                'pali_roman': 'yadā have pātubhavanti dhammā',
                'thai': '',
                'paiboon': '',
                'english': 'When indeed things become manifest',
            },
            # ‼ CHECK: พ์ราห์มะณัสสะ carries thanthakhat over พ์ and ห์, the
            #          same spelling as the Pabbatopamagāthā's พ์ราห์มะเณ. It
            #          recurs identically at verses 6 and 10. Transliterated as
            #          brāhma- throughout, consistent with the earlier chants.
            {
                'number': 2,
                'pali': 'อาตาปิโน ฌายะโต พ์ราห์มะณัสสะ',
                'pali_roman': 'ātāpino jhāyato brāhmaṇassa',
                'thai': '',
                'paiboon': '',
                'english': 'to the ardent, meditating brahmin,',
            },
            # ‼ CHECK: อะถัสสะ is printed solid, a sandhi of อะถะ and อัสสะ.
            #          Transliterated as athassa, following the printed form.
            #          It recurs at verse 7.
            {
                'number': 3,
                'pali': 'อะถัสสะ กังขา วะปะยันติ สัพพา',
                'pali_roman': 'athassa kaṅkhā vapayanti sabbā',
                'thai': '',
                'paiboon': '',
                'english': 'then all his doubts vanish away,',
            },
            {
                'number': 4,
                'pali': 'ยะโต ปะชานาติ สะเหตุธัมมัง.',
                'pali_roman': 'yato pajānāti sahetudhammaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'since he knows things together with their causes.',
            },
            # ‼ CHECK: Stanzas 2 and 3 repeat the opening lines of stanza 1 in
            #          full rather than abbreviating them, and I have
            #          reproduced every repetition in full. Check that the book
            #          does not in fact abbreviate the repeats — if it does,
            #          verses 5, 6, 9 and 10 are not printed as they stand
            #          here.
            {
                'section': 'ขะยัง ปัจจะยานัง: The Destruction of Conditions',
                'number': 5,
                'pali': 'ยะทา หะเว ปาตุภะวันติ ธัมมา',
                'pali_roman': 'yadā have pātubhavanti dhammā',
                'thai': '',
                'paiboon': '',
                'english': 'When indeed things become manifest',
            },
            {
                'number': 6,
                'pali': 'อาตาปิโน ฌายะโต พ์ราห์มะณัสสะ',
                'pali_roman': 'ātāpino jhāyato brāhmaṇassa',
                'thai': '',
                'paiboon': '',
                'english': 'to the ardent, meditating brahmin,',
            },
            {
                'number': 7,
                'pali': 'อะถัสสะ กังขา วะปะยันติ สัพพา',
                'pali_roman': 'athassa kaṅkhā vapayanti sabbā',
                'thai': '',
                'paiboon': '',
                'english': 'then all his doubts vanish away,',
            },
            {
                'number': 8,
                'pali': 'ยะโต ขะยัง ปัจจะยานัง อะเวทิ.',
                'pali_roman': 'yato khayaṃ paccayānaṃ avedi.',
                'thai': '',
                'paiboon': '',
                'english': 'since he has known the destruction of conditions.',
            },
            {
                'section': 'มาระเสนัง: The Host of Māra Scattered',
                'number': 9,
                'pali': 'ยะทา หะเว ปาตุภะวันติ ธัมมา',
                'pali_roman': 'yadā have pātubhavanti dhammā',
                'thai': '',
                'paiboon': '',
                'english': 'When indeed things become manifest',
            },
            {
                'number': 10,
                'pali': 'อาตาปิโน ฌายะโต พ์ราห์มะณัสสะ',
                'pali_roman': 'ātāpino jhāyato brāhmaṇassa',
                'thai': '',
                'paiboon': '',
                'english': 'to the ardent, meditating brahmin,',
            },
            # ‼ CHECK: วิธูปะยัง transliterated as vidhūpayaṃ. Standard
            #          editions agree, but the word is uncommon and worth a
            #          second look at this print size.
            {
                'number': 11,
                'pali': 'วิธูปะยัง ติฏฐะติ มาระเสนัง',
                'pali_roman': 'vidhūpayaṃ tiṭṭhati mārasenaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'he stands scattering the host of Māra,',
            },
            # ‼ CHECK: This line ends with a QUESTION MARK in what you pasted,
            #          where the sense is plainly a statement. It is most
            #          likely an artefact standing in for ฯ or for a full stop,
            #          as the parallel stanzas 1 and 2 both close with a full
            #          stop. Reproduced exactly as pasted rather than
            #          regularised — but this is the single most likely thing
            #          on the page to be a transcription artefact rather than
            #          the book's own printing.
            # ‼ CHECK: โอภาสะยะมันตะลิกขันติ is printed solid, a sandhi of
            #          โอภาสะยะมัง, อันตะลิกขัง and ติ. Transliterated as
            #          obhāsayamantalikkhanti, following the printed form
            #          rather than splitting it.
            {
                'number': 12,
                'pali': 'สูโรวะ โอภาสะยะมันตะลิกขันติ?',
                'pali_roman': 'sūrova obhāsayamantalikkhanti?',
                'thai': '',
                'paiboon': '',
                'english': 'like the sun illuminating the sky.',
            },
            # ‼ CHECK: The closing formula ends with no full stop, matching the
            #          นิฏฐิตา lines of the Pabbatopamagāthā and the
            #          Ariyadhanagāthā. Reproduced as pasted.
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 13,
                'pali': 'พุทธะอุทานะคาถา นิฏฐิตา',
                'pali_roman': 'buddhaudānagāthā niṭṭhitā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The verses of the Buddha's utterance of joy are ended."
                ),
            },
        ],
    },

    {
        # ‼ CHECK: No Thai translation layer exists anywhere in what you pasted
        #          — Pali only. Every thai and paiboon field is empty. I have
        #          not supplied a translation from memory.
        # ‼ CHECK: The English throughout is my own rendering of the Pali, not
        #          a translation of anything the book prints. It carries no
        #          authority from the source and should be treated as
        #          provisional.
        # ‼ CHECK: No invitation line is present. I have not written one.
        # ‼ CHECK: source left empty. Unlike chants 14 and 15, no footnote
        #          appears in what you pasted. Check the foot of the page in
        #          case one was not copied.
        # ‼ CHECK: The book prints no section headings. All four sections and
        #          their names are my grouping by subject, not the book's.
        # ‼ CHECK: A bare 33 appears between verse 16 and the closing formula.
        #          I read it as a page number and kept it out of the verses.
        #          Confirm it is not a footnote marker.

        'id': 'bhaddekaratta-gatha',
        'title_thai': 'ภัทเทกะรัตตะคาถา',
        'title_pali': 'Bhaddekarattagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses on the Auspicious Single Night',
        # Left empty on purpose: the book text gives no canonical
        # attribution and none has been supplied from memory.
        'source': '',
        'group': 'General chanting',

        # The book prints Pali only for this chant — no Thai
        # translation layer exists. The English below was written for
        # this edition rather than taken from the book, so the page
        # says so plainly instead of letting it pass as the source's.
        'english_unverified': True,

        'summary': (
            "Do not chase the past or hope for the future; see the present "
            "clearly, strive today, for who knows death tomorrow — such a one "
            "is called auspicious."
        ),

        'when_chanted': (
            "Recited as a reflection on dwelling in the present, and on the "
            "urgency of effort in view of death."
        ),

        'background': [
            "The title has occupied translators for a long time. Bhaddekaratta "
            "is literally the auspicious single night, and the verses describe "
            "the person who deserves the name rather than defining the term. "
            "The tradition treats it as naming an ideal day and night well "
            "spent, and the closing stanza gives the epithet its explanation: "
            "it is the sage at peace who so declares.",

            "These four stanzas are given in the canon within a discourse of "
            "the same name, and are followed there by a detailed exposition of "
            "what pursuing the past and hoping for the future consist in. The "
            "chanting books print the verses alone. No Thai rendering appears "
            "on this page, so the entry stands at two of the five layers and "
            "the English is my own off the Pali.",
        ],

        'meaning': [
            "The first stanza rules out two directions before naming a third. "
            "One should not run back after the past nor place hope in what has "
            "not come, and the reason given is bare fact rather than "
            "exhortation: what is past is left behind, and the future is not "
            "yet arrived. Neither is available to be lived in, which is not a "
            "moral claim but a statement about what exists.",

            "The second stanza names what is left. Whatever state is present, "
            "one sees it clearly, there where it is — ตัตถะ ตัตถะ, in each "
            "case, in each place. Two qualities are asked of that seeing: "
            "อะสังหรัง, unshakeable, and อะสังกุปปัง, unwavering. Knowing "
            "that, one should cultivate it. The instruction is not to prefer "
            "the present as a better object but to see it in a way the other "
            "two cannot be seen.",

            "The third stanza supplies the urgency, and does so with a "
            "military image. The effort is to be made today, for who knows "
            "whether death comes tomorrow — and there is no bargaining with "
            "that great host, มะหาเสเนนะ มัจจุนา, Death and his army. The word "
            "for bargaining is the language of treaty and truce, which is "
            "precisely what cannot be arranged here.",

            "The closing stanza gathers the whole into a description of a "
            "person: one who dwells thus, ardent, tireless by day and by "
            "night. Him the peaceful sage calls one of the auspicious single "
            "night. The verses never define the phrase in the abstract; they "
            "build the person first and award the name last.",
        ],

        # The book prints no invitation line for this chant. The dict
        # stays with every field empty; the template checks it and skips
        # it, so an empty invitation is not the same as a missing one.
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },

        'verses': [
            # ‼ CHECK: นาน์วาคะเมยยะ carries thanthakhat over น์.
            #          Transliterated as nānvāgameyya, following the printed
            #          form.
            {
                'section': 'อะตีตัง นาน์วาคะเมยยะ: Neither Past nor Future',
                'number': 1,
                'pali': 'อะตีตัง นาน์วาคะเมยยะ',
                'pali_roman': 'atītaṃ nānvāgameyya',
                'thai': '',
                'paiboon': '',
                'english': 'One should not run back after the past,',
            },
            {
                'number': 2,
                'pali': 'นัปปะฏิกังเข อะนาคะตัง',
                'pali_roman': 'nappaṭikaṅkhe anāgataṃ',
                'thai': '',
                'paiboon': '',
                'english': 'nor place hope in what has not yet come;',
            },
            # ‼ CHECK: ยะทะตีตัมปะหีนันตัง is printed solid, running together
            #          ยะทะตีตัง, ปะหีนัง and ตัง. Transliterated as one word
            #          following the print; confirm the book does not space it.
            {
                'number': 3,
                'pali': 'ยะทะตีตัมปะหีนันตัง',
                'pali_roman': 'yadatītampahīnantaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'for what is past is left behind,',
            },
            {
                'number': 4,
                'pali': 'อัปปัตตัญจะ อะนาคะตัง.',
                'pali_roman': 'appattañca anāgataṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'and the future is not yet arrived.',
            },
            {
                'section': 'ปัจจุปปันนัง: Seeing the Present',
                'number': 5,
                'pali': 'ปัจจุปปันนัญจะ โย ธัมมัง',
                'pali_roman': 'paccuppannañca yo dhammaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'But whoever sees the present state',
            },
            {
                'number': 6,
                'pali': 'ตัตถะ ตัตถะ วิปัสสะติ',
                'pali_roman': 'tattha tattha vipassati',
                'thai': '',
                'paiboon': '',
                'english': 'clearly, there in each case as it is —',
            },
            {
                'number': 7,
                'pali': 'อะสังหรัง อะสังกุปปัง',
                'pali_roman': 'asaṃharaṃ asaṃkuppaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'unshakeable, unwavering:',
            },
            # ‼ CHECK: ตัง วิทธา มะนุพ์รูหะเย. Standard editions read ตัง
            #          วิทฺวา (taṃ vidvā), knowing, and this line is the one
            #          most often mis-set in reprints. วิทธา would be a
            #          different word. Transliterated faithfully as viddhā
            #          rather than substituted; my English follows the standard
            #          sense, so if the printed form is right the translation
            #          needs revisiting.
            # ‼ CHECK: มะนุพ์รูหะเย carries thanthakhat over พ์ mid-word, a
            #          sandhi of ตัง อะนุพ์รูหะเย. Transliterated as
            #          manubrūhaye, following the printed form.
            {
                'number': 8,
                'pali': 'ตัง วิทธา มะนุพ์รูหะเย',
                'pali_roman': 'taṃ viddhā manubrūhaye',
                'thai': '',
                'paiboon': '',
                'english': 'knowing that, let him cultivate it.',
            },
            {
                'section': 'อัชเชวะ กิจจะมาตัปปัง: The Urgency of Today',
                'number': 9,
                'pali': 'อัชเชวะ กิจจะมาตัปปัง',
                'pali_roman': 'ajjeva kiccamātappaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'The effort is to be made this very day;',
            },
            {
                'number': 10,
                'pali': 'โก ชัญญา มะระณัง สุเว',
                'pali_roman': 'ko jaññā maraṇaṃ suve',
                'thai': '',
                'paiboon': '',
                'english': 'who knows whether death comes tomorrow?',
            },
            # ‼ CHECK: สังคะรันเตนะ transliterated as saṅgarantena. Standard
            #          editions read สงฺคราม- or สงฺคเรน in this line depending
            #          on recension, and the sense of bargaining with Death
            #          rests on the reading. Kept as printed.
            {
                'number': 11,
                'pali': 'นะ หิ โน สังคะรันเตนะ',
                'pali_roman': 'na hi no saṅgarantena',
                'thai': '',
                'paiboon': '',
                'english': 'For there is no bargaining',
            },
            {
                'number': 12,
                'pali': 'มะหาเสเนนะ มัจจุนา.',
                'pali_roman': 'mahāsenena maccunā.',
                'thai': '',
                'paiboon': '',
                'english': 'with Death and his great army.',
            },
            # ‼ CHECK: วิหาริมาตาปิง is printed solid, a sandhi of วิหาริง
            #          อาตาปิง. Transliterated as vihārimātāpiṃ. Some editions
            #          read วิหารึ (vihāriṃ) with nikkhahit; the printed form
            #          is retained.
            {
                'section': 'ภัทเทกะรัตโต: The Auspicious Single Night',
                'number': 13,
                'pali': 'เอวัง วิหาริมาตาปิง',
                'pali_roman': 'evaṃ vihārimātāpiṃ',
                'thai': '',
                'paiboon': '',
                'english': 'One who dwells thus, ardent,',
            },
            {
                'number': 14,
                'pali': 'อะโหรัตตะมะตันทิตัง',
                'pali_roman': 'ahorattamatanditaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'untiring by day and by night —',
            },
            {
                'number': 15,
                'pali': 'ตัง เว ภัทเทกะรัตโตติ',
                'pali_roman': 'taṃ ve bhaddekarattoti',
                'thai': '',
                'paiboon': '',
                'english': (
                    "him indeed, as one of the auspicious single night,"
                ),
            },
            # ‼ CHECK: A stray apostrophe follows the full stop: มุนีติ.'. The
            #          artefact has now appeared at the close of seven chants
            #          in this run. Reproduced as pasted rather than tidied.
            {
                'number': 16,
                'pali': "สันโต อาจิกขะเต มุนีติ.'",
                'pali_roman': "santo ācikkhate munīti.'",
                'thai': '',
                'paiboon': '',
                'english': 'the peaceful sage declares.',
            },
            # ‼ CHECK: The closing formula ends with no full stop, as with
            #          chants 14 and 15. Reproduced as pasted.
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 17,
                'pali': 'ภัทเทกะรัตตะคาถา นิฏฐิตา',
                'pali_roman': 'bhaddekarattagāthā niṭṭhitā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The verses on the auspicious single night are ended."
                ),
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0264.PNG]: This page carries NO printed page number.
        #   From the file sequence it precedes page 2 (IMG_0265.PNG), but that
        #   is inference, so page_start has been left off entirely. Please
        #   confirm whether the book prints a number here.
        # ‼ CHECK [IMG_0264.PNG]: The book prints three headings above this
        #   chant — ระเบียบ, ทำวัตร - สวดมนต์, ทำวัตรเช้า — which are section
        #   titles for the whole morning service, not titles of this chant.
        #   They have no field and are recorded in the page note only.
        # ‼ CHECK [IMG_0264.PNG]: The page ends with an instruction to the
        #   leader: ประธานกล่าวเชิญบูชาพระรัตนตรัยและสวด นะโม
        #   หยุดตามจุดลูกน้ำดังนี้. Reproduced in the page note; it is a
        #   rubric, not chant text.
        # ‼ CHECK [IMG_0264.PNG]: No Thai translation is printed for this
        #   chant, so thai and paiboon are empty and the English is a working
        #   translation. english_unverified is set.
        'id': 'kham-bucha-phra-ratanattaya',
        'page_start': 1,
        'title_thai': 'คำบูชาพระรัตนตรัย',
        'title_pali': '',
        'title_roman': 'Kham Bucha Phra Ratanattaya',
        'title_english': 'Words of Offering to the Triple Gem',
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            {
                'number': 1,
                'section': 'คำบูชาพระรัตนตรัย: Offering to the Triple Gem',
                'pali': 'โย โส ภะคะวา อะระหัง สัมมาสัมพุทโธ,',
                'pali_roman': 'Yo so bhagavā arahaṃ sammāsambuddho,',
                'thai': '',
                'paiboon': '',
                'english': 'That Blessed One, the Worthy One, perfectly enlightened by himself,',
            },
            # ‼ CHECK [IMG_0264.PNG]: Read as สวากขาโต. The printed form
            #   appeared to carry a mark above the ส that I could not resolve
            #   at this resolution — please check the exact spelling against
            #   the book.
            {
                'number': 2,
                'pali': 'สวากขาโต เยนะ ภะคะวะตา ธัมโม,',
                'pali_roman': 'Svākkhāto yena bhagavatā dhammo,',
                'thai': '',
                'paiboon': '',
                'english': 'the Dhamma well proclaimed by that Blessed One,',
            },
            {
                'number': 3,
                'pali': 'สุปะฏิปันโน ยัสสะ ภะคะวะโต สาวะกะสังโฆ,',
                'pali_roman': 'Supaṭipanno yassa bhagavato sāvakasaṅgho,',
                'thai': '',
                'paiboon': '',
                'english': "the Sangha of that Blessed One's disciples who have practised well,",
            },
            {
                'number': 4,
                'pali': 'ตัมมะยัง ภะคะวันตัง สะธัมมัง สะสังฆัง,',
                'pali_roman': 'Tammayaṃ bhagavantaṃ sadhammaṃ sasaṅghaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'to that Blessed One, with his Dhamma and his Sangha,',
            },
            {
                'number': 5,
                'pali': 'อิเมหิ สักกาเรหิ ยะถาระหัง อาโรปิเตหิ อะภิปูชะยามะ,',
                'pali_roman': 'Imehi sakkārehi yathārahaṃ āropitehi abhipūjayāma,',
                'thai': '',
                'paiboon': '',
                'english': 'we make offering with these gifts, set out as befits them.',
            },
            {
                'number': 6,
                'pali': 'สาธุ โน ภันเต ภะคะวา สุจิระปะรินิพพุโตปิ,',
                'pali_roman': 'Sādhu no bhante bhagavā sucira-parinibbutopi,',
                'thai': '',
                'paiboon': '',
                'english': 'Venerable sir, though the Blessed One long ago attained final Nibbāna,',
            },
            {
                'number': 7,
                'pali': 'ปัจฉิมาชะนะตานุกัมปะมานะสา,',
                'pali_roman': 'Pacchimā-janatānukampa-mānasā,',
                'thai': '',
                'paiboon': '',
                'english': 'out of compassion in mind for later generations,',
            },
            {
                'number': 8,
                'pali': 'อิเม สักกาเร ทุคคะตะปัณณาการะภูเต ปะฏิคคัณหาตุ,',
                'pali_roman': 'Ime sakkāre duggata-paṇṇākāra-bhūte paṭiggaṇhātu,',
                'thai': '',
                'paiboon': '',
                'english': 'may he accept these offerings, poor gifts though they are,',
            },
            {
                'number': 9,
                'pali': 'อัมหากัง ทีฆะรัตตัง หิตายะ สุขายะ ฯ',
                'pali_roman': 'Amhākaṃ dīgharattaṃ hitāya sukhāya.',
                'thai': '',
                'paiboon': '',
                'english': 'for our lasting welfare and happiness.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0264.PNG]: Each of the three lines is followed by the
        #   printed rubric (กราบพร้อมกัน) — 'bow together' — on its own
        #   centred line. It is an instruction to the chanters rather than
        #   chanted text, so it is recorded here and in the page note rather
        #   than inside a verse. Tell me if you would rather see it on the
        #   page.
        # ‼ CHECK [IMG_0264.PNG]: No printed page number on this page;
        #   page_start omitted. Same page as the previous chant.
        'id': 'kham-namatsakan-phra-ratanattaya',
        'page_start': 1,
        'title_thai': 'คำนมัสการพระรัตนตรัย',
        'title_pali': '',
        'title_roman': 'Kham Namatsakan Phra Ratanattaya',
        'title_english': 'Words of Salutation to the Triple Gem',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'อะระหัง สัมมาสัมพุทโธ ภะคะวา, พุทธัง ภะคะวันตัง อะภิวาเทมิ.',
                'rubric': '(กราบพร้อมกัน)',
                'pali_roman': 'Arahaṃ sammāsambuddho bhagavā, buddhaṃ bhagavantaṃ abhivādemi.',
                'thai': '',
                'paiboon': '',
                'english': 'The Blessed One is Worthy and perfectly enlightened by himself; I bow to the Buddha, the Blessed One.',
            },
            {
                'number': 2,
                'pali': 'สวากขาโต ภะคะวะตา ธัมโม, ธัมมัง นะมัสสามิ.',
                'rubric': '(กราบพร้อมกัน)',
                'pali_roman': 'Svākkhāto bhagavatā dhammo, dhammaṃ namassāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'The Dhamma is well proclaimed by the Blessed One; I pay homage to the Dhamma.',
            },
            {
                'number': 3,
                'pali': 'สุปะฏิปันโน ภะคะวะโต สาวะกะสังโฆ, สังฆัง นะมามิ.',
                'rubric': '(กราบพร้อมกัน)',
                'pali_roman': 'Supaṭipanno bhagavato sāvakasaṅgho, saṅghaṃ namāmi.',
                'thai': '',
                'paiboon': '',
                'english': "The Sangha of the Blessed One's disciples has practised well; I bow to the Sangha.",
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0265.PNG]: No Thai translation printed;
        #   english_unverified set.
        'id': 'kham-choen-bucha-lae-suat-namo',
        'title_thai': 'คำเชิญบูชาและสวดนะโม',
        'title_pali': '',
        'title_roman': 'Kham Choen Bucha lae Suat Namo',
        'title_english': 'The Invitation to Make Offering and Chant the Namo',
        'page_start': 2,
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'ยะมัมหะ โข มะยัง ภะคะวันตัง สะระณัง คะตา, อุททิสสะ ปัพพะชิตา',
                'pali_roman': 'Yamamha kho mayaṃ bhagavantaṃ saraṇaṃ gatā, uddissa pabbajitā',
                'thai': '',
                'paiboon': '',
                'english': 'That Blessed One to whom we have gone for refuge, for whose sake we have gone forth,',
            },
            # ‼ CHECK [IMG_0265.PNG]: The book writes ยัส์มิง and
            #   พ์รัห์มะจะริยัง with the mark ์ inside the word, marking a
            #   consonant cluster. Reproduced exactly as printed rather than
            #   normalised to ยัสมิง / พรัหมะจะริยัง. Please confirm the marks
            #   are where I have put them.
            {
                'number': 2,
                'pali': 'โย โน ภะคะวา สัตถา, ยัส์มิง ภะคะวะติ พ์รัห์มะจะริยัง จะรามะ,',
                'pali_roman': 'Yo no bhagavā satthā, yasmiṃ bhagavati brahmacariyaṃ carāma,',
                'thai': '',
                'paiboon': '',
                'english': 'who is our Blessed Teacher, under whom we live the holy life,',
            },
            {
                'number': 3,
                'pali': 'ตัมมะยัง ภะคะวันตัง สะธัมมัง สะสังฆัง,',
                'pali_roman': 'Tammayaṃ bhagavantaṃ sadhammaṃ sasaṅghaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'to that Blessed One, with his Dhamma and his Sangha,',
            },
            # ‼ CHECK [IMG_0265.PNG]: Same convention in อะภิปูชะยิต์วา.
            #   Reproduced as printed.
            {
                'number': 4,
                'pali': 'อิเมหิ สักกาเรหิ ยะถาระหัง อาโรปิเตหิ อะภิปูชะยิต์วา',
                'pali_roman': 'Imehi sakkārehi yathārahaṃ āropitehi abhipūjayitvā',
                'thai': '',
                'paiboon': '',
                'english': 'having made offering with these gifts, set out as befits them,',
            },
            {
                'number': 5,
                'pali': 'อะภิวาทะนัง กะริมหา,',
                'pali_roman': 'Abhivādanaṃ karimhā,',
                'thai': '',
                'paiboon': '',
                'english': 'and having paid our respects,',
            },
            {
                'number': 6,
                'pali': 'หันทะทานิ มะยัง ตัง ภะคะวันตัง วาจายะ อะภิถุตุง,',
                'pali_roman': 'Handadāni mayaṃ taṃ bhagavantaṃ vācāya abhithutuṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'let us now, in words, extol that Blessed One,',
            },
            {
                'number': 7,
                'pali': 'ปุพพะภาคะนะมะการัง กะโรมะ เส.',
                'pali_roman': 'Pubbabhāga-namakāraṃ karoma se.',
                'thai': '',
                'paiboon': '',
                'english': 'and make the preliminary salutation.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0265.PNG]: The book prints NO title for this chant. The
        #   id and English title are mine, taken from the phrase
        #   ปุพพะภาคะนะมะการัง in the invitation above it. title_thai and
        #   title_pali are left empty rather than invented.
        # ‼ CHECK [IMG_0265.PNG]: The line is printed three times in full
        #   rather than marked as a repeat, so it is entered three times.
        #   Preceded by the instruction that the deputy leader begins and the
        #   others join, three times, pausing for one breath after each.
        'id': 'pubbabhaga-namakara',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Preliminary Salutation',
        'page_start': 2,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'นะโม ตัสสะ ภะคะวะโต อะระหะโต สัมมาสัมพุทธัสสะ.',
                'pali_roman': 'Namo tassa bhagavato arahato sammāsambuddhassa.',
                'thai': '',
                'paiboon': '',
                'english': 'Homage to the Blessed One, the Worthy One, perfectly enlightened by himself.',
            },
            {
                'number': 2,
                'pali': 'นะโม ตัสสะ ภะคะวะโต อะระหะโต สัมมาสัมพุทธัสสะ.',
                'pali_roman': 'Namo tassa bhagavato arahato sammāsambuddhassa.',
                'thai': '',
                'paiboon': '',
                'english': 'Homage to the Blessed One, the Worthy One, perfectly enlightened by himself.',
            },
            {
                'number': 3,
                'pali': 'นะโม ตัสสะ ภะคะวะโต อะระหะโต สัมมาสัมพุทธัสสะ.',
                'pali_roman': 'Namo tassa bhagavato arahato sammāsambuddhassa.',
                'thai': '',
                'paiboon': '',
                'english': 'Homage to the Blessed One, the Worthy One, perfectly enlightened by himself.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0265.PNG]: RESOLVED: the page map claimed verses 1-12
        #   while this entry had 9. Stage 2 refused to write on that
        #   disagreement. Re-read from the photograph confirms nine clauses,
        #   so the map was corrected to match the page — not to match the
        #   entry. Please still confirm the count against the physical book.
        # ‼ CHECK [IMG_0265.PNG]: The book prints no title for this chant. The
        #   name is taken from the word พุทธาภิถุติง in its own invitation
        #   line; title_thai and title_pali are left empty rather than
        #   invented.
        # ‼ CHECK [IMG_0265.PNG]: The chant is followed by the printed rubric
        #   (กราบพร้อมกัน). Not entered as a verse.
        # ‼ CHECK [IMG_0265.PNG]: Two fingers appear at the bottom edge of
        #   this photograph. They do not cover any text, but the last line
        #   sits close to them — worth a glance.
        'id': 'buddhabhithuti',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'In Praise of the Buddha',
        'page_start': 2,
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': 'หันทะ มะยัง พุทธาภิถุติง กะโรมะ เส.',
            'pali_roman': 'Handa mayaṃ buddhābhithutiṃ karoma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us give praise to the Buddha.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'โย โส ตะถาคะโต อะระหัง สัมมาสัมพุทโธ,',
                'pali_roman': 'Yo so tathāgato arahaṃ sammāsambuddho,',
                'thai': '',
                'paiboon': '',
                'english': 'That Tathāgata, the Worthy One, perfectly enlightened by himself,',
            },
            {
                'number': 2,
                'pali': 'วิชชาจะระณะสัมปันโน สุคะโต โลกะวิทู,',
                'pali_roman': 'Vijjācaraṇa-sampanno sugato lokavidū,',
                'thai': '',
                'paiboon': '',
                'english': 'accomplished in knowledge and conduct, well-gone, knower of worlds,',
            },
            {
                'number': 3,
                'pali': 'อะนุตตะโร ปุริสะทัมมะสาระถิ สัตถา เทวะมะนุสสานัง พุทโธ ภะคะวา,',
                'pali_roman': 'Anuttaro purisadamma-sārathi satthā deva-manussānaṃ buddho bhagavā,',
                'thai': '',
                'paiboon': '',
                'english': 'unexcelled trainer of those who can be taught, teacher of gods and men, awakened, blessed;',
            },
            {
                'number': 4,
                'pali': 'โย อิมัง โลกัง สะเทวะกัง สะมาระกัง สะพ์รัห์มะกัง,',
                'pali_roman': 'Yo imaṃ lokaṃ sadevakaṃ samārakaṃ sabrahmakaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'who made known this world with its gods, its Māras and its Brahmās,',
            },
            {
                'number': 5,
                'pali': 'สัสสะมะณะพ์ราห์มะณิง ปะชัง สะเทวะมะนุสสัง สะยัง อะภิญญา สัจฉิกัต์วา ปะเวเทสิ,',
                'pali_roman': 'Sassamaṇa-brāhmaṇiṃ pajaṃ sadeva-manussaṃ sayaṃ abhiññā sacchikatvā pavedesi,',
                'thai': '',
                'paiboon': '',
                'english': 'this generation with its contemplatives and priests, its rulers and common people, having realised it himself through direct knowledge;',
            },
            # ‼ CHECK [IMG_0265.PNG]: อาทิกัล๎ยาณัง and its two companions
            #   carry the ๎ mark over the ล. Reproduced as printed; please
            #   confirm the character is ๎ (yamakkan) rather than ์.
            {
                'number': 6,
                'pali': 'โย ธัมมัง เทเสสิ อาทิกัล๎ยาณัง มัชเฌกัล๎ยาณัง ปะริโยสานะกัล๎ยาณัง,',
                'pali_roman': 'Yo dhammaṃ desesi ādikalyāṇaṃ majjhekalyāṇaṃ pariyosāna-kalyāṇaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'who taught the Dhamma admirable in its beginning, admirable in its middle, admirable in its end;',
            },
            {
                'number': 7,
                'pali': 'สาตถัง สะพ์ยัญชะนัง เกวะละปะริปุณณัง ปะริสุทธัง พ์รัห์มะจะริยัง ปะกาเสสิ,',
                'pali_roman': 'Sātthaṃ sabyañjanaṃ kevala-paripuṇṇaṃ parisuddhaṃ brahmacariyaṃ pakāsesi,',
                'thai': '',
                'paiboon': '',
                'english': 'who proclaimed the holy life in its meaning and its letter, entirely complete and pure;',
            },
            {
                'number': 8,
                'pali': 'ตะมะหัง ภะคะวันตัง อะภิปูชะยามิ,',
                'pali_roman': 'Tamahaṃ bhagavantaṃ abhipūjayāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'to that Blessed One I make offering,',
            },
            {
                'number': 9,
                'pali': 'ตะมะหัง ภะคะวันตัง สิระสา นะมามิ.',
                'pali_roman': 'Tamahaṃ bhagavantaṃ sirasā namāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'to that Blessed One I bow my head.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0265.PNG]: The book prints no title. The name is taken
        #   from ธัมมาภิถุติง in the invitation.
        # ‼ CHECK [IMG_0266.PNG]: Followed by the printed rubric
        #   (กราบพร้อมกัน). Not entered as a verse.
        'id': 'dhammabhithuti',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'In Praise of the Dhamma',
        'page_start': 2,
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': 'หันทะ มะยัง ธัมมาภิถุติง กะโรมะ เส.',
            'pali_roman': 'Handa mayaṃ dhammābhithutiṃ karoma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us give praise to the Dhamma.',
        },
        'verses': [
            # ‼ CHECK [IMG_0266.PNG]: Read as ส๎วากขาโต with the ๎ mark over
            #   the ส. This is the same word I read WITHOUT that mark on the
            #   unnumbered first page (verse 2 of kham-bucha-phra-
            #   ratanattaya). One of the two readings is wrong, or the book
            #   genuinely prints it both ways — please compare the two pages.
            {
                'number': 1,
                'page': 3,
                'pali': 'โย โส ส๎วากขาโต ภะคะวะตา ธัมโม, สันทิฏฐิโก อะกาลิโก เอหิปัสสิโก โอปะนะยิโก,',
                'pali_roman': 'Yo so svākkhāto bhagavatā dhammo, sandiṭṭhiko akāliko ehipassiko opanayiko,',
                'thai': '',
                'paiboon': '',
                'english': 'That Dhamma, well proclaimed by the Blessed One, visible here and now, timeless, inviting all to come and see, leading onwards,',
            },
            {
                'number': 2,
                'pali': 'ปัจจัตตัง เวทิตัพโพ วิญญูหิ,',
                'pali_roman': 'Paccattaṃ veditabbo viññūhi,',
                'thai': '',
                'paiboon': '',
                'english': 'to be known each for himself by the wise,',
            },
            {
                'number': 3,
                'pali': 'ตะมะหัง ธัมมัง อะภิปูชะยามิ, ตะมะหัง ธัมมัง สิระสา นะมามิ.',
                'pali_roman': 'Tamahaṃ dhammaṃ abhipūjayāmi, tamahaṃ dhammaṃ sirasā namāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'to that Dhamma I make offering; to that Dhamma I bow my head.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0266.PNG]: The book prints no title. The name is taken
        #   from สังฆาภิถุติง in the invitation.
        # ‼ CHECK [IMG_0266.PNG]: Followed by the rubric (กราบพร้อมกัน
        #   แล้วนั่งพับเพียบทั้งหมด) — bow together, then all sit in the side-
        #   resting posture. Not entered as a verse.
        'id': 'sanghabhithuti',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'In Praise of the Sangha',
        'page_start': 3,
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': 'หันทะ มะยัง สังฆาภิถุติง กะโรมะ เส.',
            'pali_roman': 'Handa mayaṃ saṅghābhithutiṃ karoma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us give praise to the Sangha.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'โย โส สุปะฏิปันโน ภะคะวะโต สาวะกะสังโฆ,',
                'pali_roman': 'Yo so supaṭipanno bhagavato sāvakasaṅgho,',
                'thai': '',
                'paiboon': '',
                'english': "That Sangha of the Blessed One's disciples who have practised well,",
            },
            {
                'number': 2,
                'pali': 'อุชุปะฏิปันโน ภะคะวะโต สาวะกะสังโฆ,',
                'pali_roman': 'Ujupaṭipanno bhagavato sāvakasaṅgho,',
                'thai': '',
                'paiboon': '',
                'english': 'who have practised straightforwardly,',
            },
            {
                'number': 3,
                'pali': 'ญายะปะฏิปันโน ภะคะวะโต สาวะกะสังโฆ,',
                'pali_roman': 'Ñāyapaṭipanno bhagavato sāvakasaṅgho,',
                'thai': '',
                'paiboon': '',
                'english': 'who have practised methodically,',
            },
            {
                'number': 4,
                'pali': 'สามีจิปะฏิปันโน ภะคะวะโต สาวะกะสังโฆ,',
                'pali_roman': 'Sāmīcipaṭipanno bhagavato sāvakasaṅgho,',
                'thai': '',
                'paiboon': '',
                'english': 'who have practised masterfully,',
            },
            {
                'number': 5,
                'pali': 'ยะทิทัง จัตตาริ ปุริสะยุคานิ อัฏฐะ ปุริสะปุคคะลา,',
                'pali_roman': 'Yadidaṃ cattāri purisayugāni aṭṭha purisapuggalā,',
                'thai': '',
                'paiboon': '',
                'english': 'that is, the four pairs, the eight types of noble ones —',
            },
            {
                'number': 6,
                'pali': 'เอสะ ภะคะวะโต สาวะกะสังโฆ,',
                'pali_roman': 'Esa bhagavato sāvakasaṅgho,',
                'thai': '',
                'paiboon': '',
                'english': "that is the Sangha of the Blessed One's disciples,",
            },
            {
                'number': 7,
                'pali': 'อาหุเนยโย ปาหุเนยโย ทักขิเณยโย อัญชะลีกะระณีโย,',
                'pali_roman': 'Āhuneyyo pāhuneyyo dakkhiṇeyyo añjalīkaraṇīyo,',
                'thai': '',
                'paiboon': '',
                'english': 'worthy of gifts, worthy of hospitality, worthy of offerings, worthy of respect,',
            },
            {
                'number': 8,
                'pali': 'อะนุตตะรัง ปุญญักเขตตัง โลกัสสะ,',
                'pali_roman': 'Anuttaraṃ puññakkhettaṃ lokassa,',
                'thai': '',
                'paiboon': '',
                'english': 'the unexcelled field of merit for the world;',
            },
            # ‼ CHECK [IMG_0266.PNG]: The book appears to print no comma
            #   between อะภิปูชะยามิ and ตะมะหัง here, where the two preceding
            #   chants both have one. Reproduced without it as printed rather
            #   than tidied — please confirm.
            {
                'number': 9,
                'pali': 'ตะมะหัง สังฆัง อะภิปูชะยามิ ตะมะหัง สังฆัง สิระสา นะมามิ.',
                'pali_roman': 'Tamahaṃ saṅghaṃ abhipūjayāmi, tamahaṃ saṅghaṃ sirasā namāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'to that Sangha I make offering; to that Sangha I bow my head.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ COMPLETED: this chant arrived in two halves — verses 1-4 from
        #   batch-001-003 (page 3, IMG_0266.PNG) and verses 5-16 from
        #   batch-004-006 (page 4, IMG_0267.PNG). Joined and verified to run
        #   1-16 with no gap and no repeat. It no longer continues.
        # ‼ CHECK [IMG_0266.PNG]: This is the first chant in the batch whose
        #   title the book actually prints, centred and in bold:
        #   ระตะนัตตะยัปปะณามะคาถา.
        # ‼ CHECK [IMG_0266.PNG]: The section label on verse 1 is MINE, not
        #   the book's — the book prints no heading inside this chant. Say if
        #   you would rather it were dropped.
        'id': 'ratanattayappanamagatha',
        'title_thai': 'ระตะนัตตะยัปปะณามะคาถา',
        'title_pali': '',
        'title_roman': 'Ratanattayappanamagatha',
        'title_english': 'Verses in Salutation to the Triple Gem',
        'page_start': 3,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': 'หันทะ มะยัง ระตะนัตตะยัปปะณามะคาถาโย เจวะ สังเวคะปะริกิตตะนะปาฐัญจะ ภะณามะ เส.',
            'pali_roman': 'Handa mayaṃ ratanattayappaṇāma-gāthāyo ceva saṃvega-parikittana-pāṭhañca bhaṇāma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us recite the verses in salutation to the Triple Gem, and the passage on spiritual urgency.',
        },
        'verses': [
            {
                'number': 1,
                'section': 'พุทโธ: Salutation to the Buddha',
                'pali': 'พุทโธ สุสุทโธ กะรุณามะหัณณะโว,',
                'pali_roman': 'Buddho susuddho karuṇā-mahaṇṇavo,',
                'thai': '',
                'paiboon': '',
                'english': 'The Buddha, utterly pure, a great ocean of compassion,',
            },
            # ‼ CHECK [IMG_0266.PNG]: โยจจันตะสุทธัพพะระญาณะโลจะโน is printed
            #   as one unbroken word and is long; please check my reading of
            #   it letter by letter, particularly ทธัพพะระ.
            {
                'number': 2,
                'pali': 'โยจจันตะสุทธัพพะระญาณะโลจะโน,',
                'pali_roman': 'Yoccanta-suddhabbara-ñāṇa-locano,',
                'thai': '',
                'paiboon': '',
                'english': 'whose eye of knowledge is wholly purified,',
            },
            {
                'number': 3,
                'pali': 'โลกัสสะ ปาปูปะกิเลสะฆาตะโก,',
                'pali_roman': 'Lokassa pāpūpakilesa-ghātako,',
                'thai': '',
                'paiboon': '',
                'english': "destroyer of the world's evil and defilement:",
            },
            {
                'number': 4,
                'pali': 'วันทามิ พุทธัง อะหะมาทะเรนะ ตัง.',
                'pali_roman': 'Vandāmi buddhaṃ ahamādarena taṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'I revere that Buddha with devotion.',
            },
            # ‼ CHECK [IMG_0267.PNG]: This entry CONTINUES the chant begun on
            #   page 3 in batch-001-003. Verse numbering resumes at 5, so the
            #   joined chant should run 1-16 with no gap and no repeat. Stage
            #   2 must append these to the existing dict, not create a second
            #   one.
            {
                'number': 5,
                'page': 4,
                'section': 'ธัมโม: Salutation to the Dhamma',
                'pali': 'ธัมโม ปะทีโป วิยะ ตัสสะ สัตถุโน,',
                'pali_roman': 'Dhammo padīpo viya tassa satthuno,',
                'thai': '',
                'paiboon': '',
                'english': 'The Dhamma, like a lamp of that Teacher,',
            },
            # ‼ CHECK [IMG_0267.PNG]: มัคคะปากามะตะเภทะภินนะโก is printed as
            #   one unbroken word. Reproduced as one; please confirm there is
            #   no space in it.
            {
                'number': 6,
                'pali': 'โย มัคคะปากามะตะเภทะภินนะโก,',
                'pali_roman': 'Yo maggapākāmata-bheda-bhinnako,',
                'thai': '',
                'paiboon': '',
                'english': 'divided into path, fruit and the Deathless,',
            },
            {
                'number': 7,
                'pali': 'โลกุตตะโร โย จะ ตะทัตถะทีปะโน,',
                'pali_roman': 'Lokuttaro yo ca tadattha-dīpano,',
                'thai': '',
                'paiboon': '',
                'english': 'transcendent, and that which points to its meaning:',
            },
            {
                'number': 8,
                'pali': 'วันทามิ ธัมมัง อะหะมาทะเรนะ ตัง.',
                'pali_roman': 'Vandāmi dhammaṃ ahamādarena taṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'I revere that Dhamma with devotion.',
            },
            # ‼ CHECK [IMG_0267.PNG]: สุเขตตาภ๎ยะติเขตตะสัญญิโต is a long
            #   compound with the ๎ mark over the ภ. Please check my reading
            #   letter by letter — this is the least certain line on the page.
            {
                'number': 9,
                'section': 'สังโฆ: Salutation to the Sangha',
                'pali': 'สังโฆ สุเขตตาภ๎ยะติเขตตะสัญญิโต,',
                'pali_roman': 'Saṅgho sukhettābhyatikhetta-saññito,',
                'thai': '',
                'paiboon': '',
                'english': 'The Sangha, called a field of merit surpassing all fields,',
            },
            {
                'number': 10,
                'pali': 'โย ทิฏฐะสันโต สุคะตานุโพธะโก,',
                'pali_roman': 'Yo diṭṭhasanto sugatānubodhako,',
                'thai': '',
                'paiboon': '',
                'english': 'who have seen peace, awakening after the Well-Gone One,',
            },
            {
                'number': 11,
                'pali': 'โลลัปปะหีโน อะริโย สุเมธะโส,',
                'pali_roman': 'Lolappahīno ariyo sumedhaso,',
                'thai': '',
                'paiboon': '',
                'english': 'free of craving, noble and wise:',
            },
            {
                'number': 12,
                'pali': 'วันทามิ สังฆัง อะหะมาทะเรนะ ตัง.',
                'pali_roman': 'Vandāmi saṅghaṃ ahamādarena taṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'I revere that Sangha with devotion.',
            },
            # ‼ CHECK [IMG_0267.PNG]: The section labels on verses 5, 9 and 13
            #   are MINE, not the book's. The book prints no headings inside
            #   this chant; the stanzas are separated only by their opening
            #   words. Say if you would rather they were dropped.
            {
                'number': 13,
                'section': 'อิจเจวะมะ: The Dedication',
                'pali': 'อิจเจวะเมกันตะภิปูชะเนยยะกัง,',
                'pali_roman': 'Iccevamekantabhipūjaneyyakaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'Thus this triple object, wholly worthy of offering,',
            },
            {
                'number': 14,
                'pali': 'วัตถุตตะยัง วันทะยะตาภิสังขะตัง,',
                'pali_roman': 'Vatthuttayaṃ vandayatābhisaṅkhataṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'which I have honoured with reverence —',
            },
            {
                'number': 15,
                'pali': 'ปุญญัง มะยา ยัง มะมะ สัพพุปัททะวา,',
                'pali_roman': 'Puññaṃ mayā yaṃ mama sabbupaddavā,',
                'thai': '',
                'paiboon': '',
                'english': 'by whatever merit I have made, may all my obstacles',
            },
            {
                'number': 16,
                'pali': 'มา โหนตุ เว ตัสสะ ปะภาวะสิทธิยา.',
                'pali_roman': 'Mā hontu ve tassa pabhāva-siddhiyā.',
                'thai': '',
                'paiboon': '',
                'english': 'be no more, through the power of its accomplishment.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0267.PNG]: The title is printed, centred and bold. The
        #   chant shares its invitation with ratanattayappanamagatha — one
        #   invitation on page 3 covers both — so invitation is left empty
        #   here rather than duplicated.
        # ‼ CHECK [IMG_0268.PNG]: Two fingers appear at the foot of
        #   IMG_0268.PNG. They do not cover text.
        # ‼ CHECK [IMG_0268.PNG]: Below this chant, page 5 carries about half
        #   a page of Thai instruction and three leader's invitations for the
        #   เสขิยวัตร — ฉัพพีสะติ สารุปปาสิกขาโย, สะมะติงสะ
        #   โภชะนะปะฏิสังยุตตาสิกขาโย, and โสฬะสะ
        #   ธัมมะเทสะนาปะฏิสังยุตตาสิกขาโย เจวะ ติสโส ปะกิณณะกาสิกขาโย. The
        #   เสขิยวัตร themselves are NOT printed here; the instruction says
        #   they are set out after the morning service. Recorded in the page
        #   note; no chant entered for them.
        'id': 'samvega-parikittana-patha',
        'title_thai': 'สังเวคะปะริกิตตะนะปาฐะ',
        'title_pali': '',
        'title_roman': 'Samvega-parikittana-patha',
        'title_english': 'The Passage on Spiritual Urgency',
        'page_start': 4,
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'อิธะ ตะถาคะโต โลเก อุปปันโน อะระหัง สัมมาสัมพุทโธ,',
                'pali_roman': 'Idha tathāgato loke uppanno arahaṃ sammāsambuddho,',
                'thai': '',
                'paiboon': '',
                'english': 'Here a Tathāgata has arisen in the world, worthy and perfectly enlightened by himself,',
            },
            {
                'number': 2,
                'pali': 'ธัมโม จะ เทสิโต นิยยานิโก อุปะสะมิโก ปะรินิพพานิโก สัมโพธะคามี สุคะตัปปะเวทิโต,',
                'pali_roman': 'Dhammo ca desito niyyāniko upasamiko parinibbāniko sambodhagāmī sugatappavedito,',
                'thai': '',
                'paiboon': '',
                'english': 'and a Dhamma has been taught that leads out, brings peace, leads to final Nibbāna and to awakening, made known by the Well-Gone One.',
            },
            # ‼ CHECK [IMG_0267.PNG]: สุต๎วา carries the ๎ mark over the ต.
            #   Same convention appears in verses 31, 36, 37 and 39
            #   (โอติณณาม๎หะ, อะคารัส๎มา, ตัส๎มิง, พ๎รัห๎มะจะริยัง).
            #   Reproduced as printed throughout; please confirm the mark is ๎
            #   and not ์.
            {
                'number': 3,
                'pali': 'มะยันตัง ธัมมัง สุต๎วา เอวัง ชานามะ,',
                'pali_roman': 'Mayantaṃ dhammaṃ sutvā evaṃ jānāma,',
                'thai': '',
                'paiboon': '',
                'english': 'Having heard that Dhamma, we know this:',
            },
            {
                'number': 4,
                'pali': 'ชาติปิ ทุกขา ชะราปิ ทุกขา มะระณัมปิ ทุกขัง,',
                'pali_roman': 'Jātipi dukkhā jarāpi dukkhā maraṇampi dukkhaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'birth is suffering, ageing is suffering, death is suffering,',
            },
            {
                'number': 5,
                'pali': 'โสกะปะริเทวะทุกขะโทมะนัสสุปายาสาปิ ทุกขา,',
                'pali_roman': 'Soka-parideva-dukkha-domanassupāyāsāpi dukkhā,',
                'thai': '',
                'paiboon': '',
                'english': 'sorrow, lamentation, pain, grief and despair are suffering,',
            },
            {
                'number': 6,
                'pali': 'อัปปิเยหิ สัมปะโยโค ทุกโข ปิเยหิ วิปปะโยโค ทุกโข ยัมปิจฉัง นะ ละภะติ ตัมปิ ทุกขัง,',
                'pali_roman': 'Appiyehi sampayogo dukkho piyehi vippayogo dukkho yampicchaṃ na labhati tampi dukkhaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'union with what is disliked is suffering, separation from what is liked is suffering, not getting what one wants is suffering,',
            },
            {
                'number': 7,
                'pali': 'สังขิตเตนะ ปัญจุปาทานักขันธา ทุกขา,',
                'pali_roman': 'Saṅkhittena pañcupādānakkhandhā dukkhā,',
                'thai': '',
                'paiboon': '',
                'english': 'in short, the five aggregates of clinging are suffering,',
            },
            {
                'number': 8,
                'pali': 'เสยยะถีทัง,',
                'pali_roman': 'Seyyathīdaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'namely:',
            },
            {
                'number': 9,
                'pali': 'รูปูปาทานักขันโธ,',
                'pali_roman': 'Rūpūpādānakkhandho,',
                'thai': '',
                'paiboon': '',
                'english': 'the form aggregate of clinging,',
            },
            {
                'number': 10,
                'pali': 'เวทะนูปาทานักขันโธ,',
                'pali_roman': 'Vedanūpādānakkhandho,',
                'thai': '',
                'paiboon': '',
                'english': 'the feeling aggregate of clinging,',
            },
            {
                'number': 11,
                'pali': 'สัญญูปาทานักขันโธ,',
                'pali_roman': 'Saññūpādānakkhandho,',
                'thai': '',
                'paiboon': '',
                'english': 'the perception aggregate of clinging,',
            },
            {
                'number': 12,
                'pali': 'สังขารูปาทานักขันโธ,',
                'pali_roman': 'Saṅkhārūpādānakkhandho,',
                'thai': '',
                'paiboon': '',
                'english': 'the formations aggregate of clinging,',
            },
            {
                'number': 13,
                'pali': 'วิญญาณูปาทานักขันโธ,',
                'pali_roman': 'Viññāṇūpādānakkhandho,',
                'thai': '',
                'paiboon': '',
                'english': 'the consciousness aggregate of clinging.',
            },
            {
                'number': 14,
                'pali': 'เยสัง ปะริญญายะ,',
                'pali_roman': 'Yesaṃ pariññāya,',
                'thai': '',
                'paiboon': '',
                'english': 'For the full understanding of these,',
            },
            {
                'number': 15,
                'pali': 'ธะระมาโน โส ภะคะวา,',
                'pali_roman': 'Dharamāno so bhagavā,',
                'thai': '',
                'paiboon': '',
                'english': 'the Blessed One, while still living,',
            },
            {
                'number': 16,
                'pali': 'เอวัง พะหุลัง สาวะเก วิเนติ,',
                'pali_roman': 'Evaṃ bahulaṃ sāvake vineti,',
                'thai': '',
                'paiboon': '',
                'english': 'often instructed his disciples in this way,',
            },
            # ‼ CHECK [IMG_0267.PNG]: I read a comma between อะนุสาสะนี and
            #   พะหุลา, and a space in พะหุลา ปะวัตตะติ. The line sits close
            #   to the gutter and I am not certain of either. Please check.
            {
                'number': 17,
                'pali': 'เอวัง ภาคา จะ ปะนัสสะ ภะคะวะโต สาวะเกสุ อะนุสาสะนี, พะหุลา ปะวัตตะติ,',
                'pali_roman': 'Evaṃ bhāgā ca panassa bhagavato sāvakesu anusāsanī, bahulā pavattati,',
                'thai': '',
                'paiboon': '',
                'english': 'and this was the greater part of his teaching among his disciples:',
            },
            {
                'number': 18,
                'pali': 'รูปัง อะนิจจัง,',
                'pali_roman': 'Rūpaṃ aniccaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'form is impermanent,',
            },
            {
                'number': 19,
                'pali': 'เวทะนา อะนิจจา,',
                'pali_roman': 'Vedanā aniccā,',
                'thai': '',
                'paiboon': '',
                'english': 'feeling is impermanent,',
            },
            {
                'number': 20,
                'pali': 'สัญญา อะนิจจา,',
                'pali_roman': 'Saññā aniccā,',
                'thai': '',
                'paiboon': '',
                'english': 'perception is impermanent,',
            },
            {
                'number': 21,
                'pali': 'สังขารา อะนิจจา,',
                'pali_roman': 'Saṅkhārā aniccā,',
                'thai': '',
                'paiboon': '',
                'english': 'formations are impermanent,',
            },
            {
                'number': 22,
                'pali': 'วิญญาณัง อะนิจจัง,',
                'pali_roman': 'Viññāṇaṃ aniccaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'consciousness is impermanent;',
            },
            {
                'number': 23,
                'pali': 'รูปัง อะนัตตา,',
                'pali_roman': 'Rūpaṃ anattā,',
                'thai': '',
                'paiboon': '',
                'english': 'form is not-self,',
            },
            {
                'number': 24,
                'pali': 'เวทะนา อะนัตตา,',
                'pali_roman': 'Vedanā anattā,',
                'thai': '',
                'paiboon': '',
                'english': 'feeling is not-self,',
            },
            {
                'number': 25,
                'pali': 'สัญญา อะนัตตา,',
                'pali_roman': 'Saññā anattā,',
                'thai': '',
                'paiboon': '',
                'english': 'perception is not-self,',
            },
            {
                'number': 26,
                'pali': 'สังขารา อะนัตตา,',
                'pali_roman': 'Saṅkhārā anattā,',
                'thai': '',
                'paiboon': '',
                'english': 'formations are not-self,',
            },
            {
                'number': 27,
                'pali': 'วิญญาณัง อะนัตตา,',
                'pali_roman': 'Viññāṇaṃ anattā,',
                'thai': '',
                'paiboon': '',
                'english': 'consciousness is not-self;',
            },
            {
                'number': 28,
                'pali': 'สัพเพ สังขารา อะนิจจา,',
                'pali_roman': 'Sabbe saṅkhārā aniccā,',
                'thai': '',
                'paiboon': '',
                'english': 'all formations are impermanent,',
            },
            # ‼ CHECK [IMG_0267.PNG]: Note the asymmetry the book prints and I
            #   have kept: verse 28 says สัพเพ สังขารา อะนิจจา (all formations
            #   impermanent) but there is no matching สัพเพ สังขารา ทุกขา line
            #   before verse 29. If the book prints one and I missed it, this
            #   is where it would be.
            {
                'number': 29,
                'pali': 'สัพเพ ธัมมา อะนัตตาติ,',
                'pali_roman': 'Sabbe dhammā anattāti,',
                'thai': '',
                'paiboon': '',
                'english': 'all things are not-self.',
            },
            {
                'number': 30,
                'pali': 'เต มะยัง,',
                'pali_roman': 'Te mayaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'All of us,',
            },
            {
                'number': 31,
                'page': 5,
                'pali': 'โอติณณาม๎หะ ชาติยา ชะรามะระเณนะ,',
                'pali_roman': 'Otiṇṇāmha jātiyā jarāmaraṇena,',
                'thai': '',
                'paiboon': '',
                'english': 'are beset by birth, by ageing and death,',
            },
            {
                'number': 32,
                'pali': 'โสเกหิ ปะริเทเวหิ ทุกเขหิ โทมะนัสเสหิ อุปายาเสหิ,',
                'pali_roman': 'Sokehi paridevehi dukkhehi domanassehi upāyāsehi,',
                'thai': '',
                'paiboon': '',
                'english': 'by sorrow, lamentation, pain, grief and despair,',
            },
            {
                'number': 33,
                'pali': 'ทุกโขติณณา ทุกขะปะเรตา,',
                'pali_roman': 'Dukkhotiṇṇā dukkhaparetā,',
                'thai': '',
                'paiboon': '',
                'english': 'beset by suffering, overcome by suffering.',
            },
            {
                'number': 34,
                'pali': 'อัปเปวะ นามิมัสสะ เกวะลัสสะ ทุกขักขันธัสสะ อันตะกิริยา ปัญญาเยถาติ,',
                'pali_roman': 'Appeva nāmimassa kevalassa dukkhakkhandhassa antakiriyā paññāyethāti,',
                'thai': '',
                'paiboon': '',
                'english': 'Perhaps an end to this whole mass of suffering might be found.',
            },
            {
                'number': 35,
                'pali': 'จิระปะรินิพพุตัมปิ ตัง ภะคะวันตัง อุททิสสะ อะระหันตัง สัมมาสัมพุทธัง,',
                'pali_roman': 'Cira-parinibbutampi taṃ bhagavantaṃ uddissa arahantaṃ sammāsambuddhaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'Dedicated to that Blessed One, worthy and perfectly enlightened, though long since attained to final Nibbāna,',
            },
            {
                'number': 36,
                'pali': 'สัทธา อะคารัส๎มา อะนะคาริยัง ปัพพะชิตา,',
                'pali_roman': 'Saddhā agārasmā anagāriyaṃ pabbajitā,',
                'thai': '',
                'paiboon': '',
                'english': 'we have gone forth in faith from home into homelessness,',
            },
            {
                'number': 37,
                'pali': 'ตัส๎มิง ภะคะวะติ พ๎รัห๎มะจะริยัง จะรามะ,',
                'pali_roman': 'Tasmiṃ bhagavati brahmacariyaṃ carāma,',
                'thai': '',
                'paiboon': '',
                'english': 'and live the holy life under that Blessed One,',
            },
            {
                'number': 38,
                'pali': 'ภิกขูนัง สิกขาสาชีวะสะมาปันนา,',
                'pali_roman': 'Bhikkhūnaṃ sikkhāsājīva-samāpannā,',
                'thai': '',
                'paiboon': '',
                'english': 'having taken up the training and livelihood of the bhikkhus.',
            },
            {
                'number': 39,
                'pali': 'ตัง โน พ๎รัห๎มะจะริยัง,',
                'pali_roman': 'Taṃ no brahmacariyaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'May this holy life of ours',
            },
            {
                'number': 40,
                'pali': 'อิมัสสะ เกวะลัสสะ ทุกขักขันธัสสะ อันตะกิริยายะ สังวัตตะตูติ.',
                'pali_roman': 'Imassa kevalassa dukkhakkhandhassa antakiriyāya saṃvattatūti.',
                'thai': '',
                'paiboon': '',
                'english': 'lead to the ending of this whole mass of suffering.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        #   Last verse here is 14; the rest is not in the app yet.
        # ‼ CHECK [IMG_0269.PNG]: This chant CONTINUES past the batch. The
        #   rest of the reflection on lodging and the whole fourth reflection,
        #   on medicine, are on page 7 onward. Pick it up rather than starting
        #   it again — verse numbering resumes at 15, and verse 14 needs
        #   finishing.
        # ‼ CHECK [IMG_0269.PNG]: The section labels on verses 1, 6 and 11 are
        #   MINE. The book separates the reflections by a blank line only,
        #   with no printed headings.
        
'id': 'tangkhanika-paccavekkhana-patho',
        'title_thai': 'ตังขะณิกะปัจจะเวกขะณะปาโฐ',
        'title_pali': '',
        'title_roman': 'Tangkhanika-paccavekkhana-patho',
        'title_english': 'The Reflection at the Moment of Use',
        'page_start': 6,
        'source_printed': 'นัย ม. มู ๑๒/๑๓-๘',
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': 'หันทะ มะยัง ตังขะณิกะปัจจะเวกขะณะปาฐัง ภะณามะ เส.',
            'pali_roman': 'Handa mayaṃ taṅkhaṇika-paccavekkhaṇa-pāṭhaṃ bhaṇāma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us recite the reflection made at the moment of use.',
        },
        'verses': [
            {
                'number': 1,
                'section': 'จีวะรัง: The Robe',
                'pali': 'ปะฏิสังขา โยนิโส จีวะรัง ปะฏิเสวามิ,',
                'pali_roman': 'Paṭisaṅkhā yoniso cīvaraṃ paṭisevāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'Reflecting wisely, I use the robe:',
            },
            {
                'number': 2,
                'pali': 'ยาวะเทวะ สีตัสสะ ปะฏิฆาตายะ,',
                'pali_roman': 'Yāvadeva sītassa paṭighātāya,',
                'thai': '',
                'paiboon': '',
                'english': 'only to ward off cold,',
            },
            {
                'number': 3,
                'pali': 'อุณ๎หัสสะ ปะฏิฆาตายะ,',
                'pali_roman': 'Uṇhassa paṭighātāya,',
                'thai': '',
                'paiboon': '',
                'english': 'to ward off heat,',
            },
            {
                'number': 4,
                'pali': 'ฑังสะมะกะสะวาตาตะปะสิริงสะปะสัมผัสสานัง ปะฏิฆาตายะ,',
                'pali_roman': 'Ḍaṃsa-makasa-vātātapa-siriṃsapa-samphassānaṃ paṭighātāya,',
                'thai': '',
                'paiboon': '',
                'english': 'to ward off the touch of gadflies, mosquitoes, wind, sun and creeping things,',
            },
            # ‼ CHECK [IMG_0269.PNG]: Verse 5 appears to end with no full stop
            #   and no comma, unlike the other reflections which close with
            #   จาติ. Reproduced as printed rather than tidied. Please
            #   confirm.
            {
                'number': 5,
                'pali': 'ยาวะเทวะ หิริโกปินะปะฏิจฉาทะนัตถัง',
                'pali_roman': 'Yāvadeva hirikopina-paṭicchādanatthaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'and only for the sake of modesty.',
            },
            {
                'number': 6,
                'section': 'ปิณฑะปาตัง: The Almsfood',
                'pali': 'ปะฏิสังขา โยนิโส ปิณฑะปาตัง ปะฏิเสวามิ,',
                'pali_roman': 'Paṭisaṅkhā yoniso piṇḍapātaṃ paṭisevāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'Reflecting wisely, I use the almsfood:',
            },
            # ‼ CHECK [IMG_0269.PNG]: Read as ท๎วายะ. Standard editions have
            #   davāya; the Thai script here could also be read ท๎ะวายะ at
            #   this resolution. Please check.
            {
                'number': 7,
                'pali': 'เนวะ ท๎วายะ นะ มะทายะ นะ มัณฑะนายะ นะ วิภูสะนายะ,',
                'pali_roman': 'Neva davāya na madāya na maṇḍanāya na vibhūsanāya,',
                'thai': '',
                'paiboon': '',
                'english': 'not for fun, not for indulgence, not for beautifying, not for adornment,',
            },
            {
                'number': 8,
                'pali': 'ยาวะเทวะ อิมัสสะ กายัสสะ ฐิติยา ยาปะนายะ วิหิงสุปะระติยา พ๎รัห๎มะจะริยานุคคะหายะ,',
                'pali_roman': 'Yāvadeva imassa kāyassa ṭhitiyā yāpanāya vihiṃsuparatiyā brahmacariyānuggahāya,',
                'thai': '',
                'paiboon': '',
                'english': 'but only for the maintenance and nourishment of this body, to keep it from harm, and to support the holy life,',
            },
            {
                'number': 9,
                'pali': 'อิติ ปุราณัญจะ เวทะนัง ปะฏิหังขามิ นะวัญจะ เวทะนัง นะ อุปปาเทสสามิ,',
                'pali_roman': 'Iti purāṇañca vedanaṃ paṭihaṅkhāmi navañca vedanaṃ na uppādessāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'thinking: thus I shall put an end to old feeling and not give rise to new,',
            },
            {
                'number': 10,
                'pali': 'ยาต๎รา จะ เม ภะวิสสะติ อะนะวัชชะตา จะ ผาสุวิหาโร จาติ.',
                'pali_roman': 'Yātrā ca me bhavissati anavajjatā ca phāsuvihāro cāti.',
                'thai': '',
                'paiboon': '',
                'english': 'and I shall have sustenance, blamelessness and a comfortable abiding.',
            },
            {
                'number': 11,
                'section': 'เสนาสะนัง: The Lodging',
                'pali': 'ปะฏิสังขา โยนิโส เสนาสะนัง ปะฏิเสวามิ,',
                'pali_roman': 'Paṭisaṅkhā yoniso senāsanaṃ paṭisevāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'Reflecting wisely, I use the lodging:',
            },
            {
                'number': 12,
                'pali': 'ยาวะเทวะ สีตัสสะ ปะฏิฆาตายะ,',
                'pali_roman': 'Yāvadeva sītassa paṭighātāya,',
                'thai': '',
                'paiboon': '',
                'english': 'only to ward off cold,',
            },
            {
                'number': 13,
                'pali': 'อุณ๎หัสสะ ปะฏิฆาตายะ,',
                'pali_roman': 'Uṇhassa paṭighātāya,',
                'thai': '',
                'paiboon': '',
                'english': 'to ward off heat,',
            },
            # ‼ CHECK [IMG_0269.PNG]: INCOMPLETE LINE. Verse 14 is the last
            #   thing printed on page 6 and its sentence runs over onto page
            #   7, which was not in this batch. What is on page 6 has been
            #   reproduced and the gap marked […]. The verse belongs to the
            #   page it starts on, per the page rules. It must be completed
            #   from page 7 rather than left as it stands.
            # ‼ COMPLETED FROM p7: this line was cut by the page break and is
            #   now whole. Was: ฑังสะมะกะสะวาตาตะปะสิริงสะปะสัมผัสสานัง […]
            # ‼ CHECK [IMG_0270.PNG]: VERSE 14 IS A CORRECTION, NOT AN
            #   ADDITION. The app currently holds this verse as
            #   'ฑังสะมะกะสะวาตาตะปะสิริงสะปะสัมผัสสานัง […]' because it was
            #   cut off at the foot of page 6. Page 7 shows the sentence
            #   finishing with ปะฏิฆาตายะ, so the whole verse should REPLACE
            #   what is there. This is the one place in this batch where the
            #   incoming text must win over the file.
            {
                'number': 14,
                'page': 7,
                'pali': 'ฑังสะมะกะสะวาตาตะปะสิริงสะปะสัมผัสสานัง ปะฏิฆาตายะ,',
                'pali_roman': 'Ḍaṃsa-makasa-vātātapa-siriṃsapa-samphassānaṃ paṭighātāya,',
                'thai': '',
                'paiboon': '',
                'english': 'to ward off the touch of gadflies, mosquitoes, wind, sun and creeping things,',
            },
            # ‼ CHECK [IMG_0270.PNG]: This completes the chant. It should no
            #   longer carry a CONTINUES marker once verses 14-18 are in — the
            #   joined chant runs 1-18.
            {
                'number': 15,
                'pali': 'ยาวะเทวะ อุตุปะริสสะยะวิโนทะนัง ปะฏิสัลลานารามัตถัง.',
                'pali_roman': 'Yāvadeva utuparissaya-vinodanaṃ paṭisallānārāmatthaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'and only to remove the danger of the seasons and for the enjoyment of seclusion.',
            },
            {
                'number': 16,
                'section': 'คิลานะปัจจะยะ: The Medicine',
                'pali': 'ปะฏิสังขา โยนิโส คิลานะปัจจะยะเภสัชชะปะริกขารัง ปะฏิเสวามิ,',
                'pali_roman': 'Paṭisaṅkhā yoniso gilānapaccaya-bhesajja-parikkhāraṃ paṭisevāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'Reflecting wisely, I use medicinal requisites for the sick:',
            },
            {
                'number': 17,
                'pali': 'ยาวะเทวะ อุปปันนานัง เวยยาพาธิกานัง เวทะนานัง ปะฏิฆาตายะ,',
                'pali_roman': 'Yāvadeva uppannānaṃ veyyābādhikānaṃ vedanānaṃ paṭighātāya,',
                'thai': '',
                'paiboon': '',
                'english': 'only to ward off painful feelings that have arisen,',
            },
            # ‼ CHECK [IMG_0270.PNG]: A superscript footnote marker appears
            #   after ปะระมะตายาติ. The footnote at the foot of page 7 is
            #   printed in THAI numerals: ๑. นัย ม. มู ๑๒/๑๓-๘. That is a
            #   canonical reference (Majjhima, Mūlapaṇṇāsa) with its volume
            #   and page in Thai numerals. Recorded as source_printed exactly
            #   as printed, unconverted.
            {
                'number': 18,
                'pali': 'อัพ๎ยาปัชฌะปะระมะตายาติ ฯ',
                'pali_roman': 'Abyāpajjha-paramatāyāti.',
                'thai': '',
                'paiboon': '',
                'english': 'and for the greatest freedom from affliction.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0271.PNG]: Below verse 21 the book prints
        #   จบพิธีทำวัตรเช้า, centred and bold — the end of the whole morning
        #   service, not of this chant. It has no field and is recorded in the
        #   page note.
        'id': 'pattidana-gatha',
        'title_thai': 'ปัตติทานะคาถา',
        'title_pali': '',
        'title_roman': 'Pattidana-gatha',
        'title_english': 'The Verses for Sharing Merit',
        'page_start': 7,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': 'หันทะ มะยัง ปัตติทานะคาถาโย ภะณามะ เส.',
            'pali_roman': 'Handa mayaṃ pattidāna-gāthāyo bhaṇāma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us recite the verses for sharing merit.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'ยา เทวะตา สันติ วิหาระวาสินี,',
                'pali_roman': 'Yā devatā santi vihāravāsinī,',
                'thai': '',
                'paiboon': '',
                'english': 'Whatever devas dwell in this monastery,',
            },
            {
                'number': 2,
                'pali': 'ถูเป ฆะเร โพธิฆะเร ตะหิง ตะหิง,',
                'pali_roman': 'Thūpe ghare bodhighare tahiṃ tahiṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'in the stupa, the dwelling, the Bodhi enclosure, here and there,',
            },
            {
                'number': 3,
                'pali': 'ตา ธัมมะทาเนนะ ภะวันตุ ปูชิตา,',
                'pali_roman': 'Tā dhammadānena bhavantu pūjitā,',
                'thai': '',
                'paiboon': '',
                'english': 'may they be honoured with the gift of Dhamma,',
            },
            {
                'number': 4,
                'pali': 'โสตถิง กะโรนเตธะ วิหาระมัณฑะเล,',
                'pali_roman': 'Sotthiṃ karontedha vihāramaṇḍale,',
                'thai': '',
                'paiboon': '',
                'english': 'and bring safety here within this monastery.',
            },
            {
                'number': 5,
                'pali': 'เถรา จะ มัชฌา นะวะกา จะ ภิกขะโว,',
                'pali_roman': 'Therā ca majjhā navakā ca bhikkhavo,',
                'thai': '',
                'paiboon': '',
                'english': 'Elder, middling and newly ordained bhikkhus,',
            },
            {
                'number': 6,
                'pali': 'สารามิกา ทานะปะตี อุปาสะกา,',
                'pali_roman': 'Sārāmikā dānapatī upāsakā,',
                'thai': '',
                'paiboon': '',
                'english': 'monastery helpers, donors and lay followers,',
            },
            {
                'number': 7,
                'pali': 'คามา จะ เทสา นิคะมา จะ อิสสะรา,',
                'pali_roman': 'Gāmā ca desā nigamā ca issarā,',
                'thai': '',
                'paiboon': '',
                'english': 'villages, lands, towns and their rulers —',
            },
            {
                'number': 8,
                'pali': 'สัปปาณะภูตา สุขิตา ภะวันตุ เต,',
                'pali_roman': 'Sappāṇabhūtā sukhitā bhavantu te,',
                'thai': '',
                'paiboon': '',
                'english': 'may all living beings be happy.',
            },
            {
                'number': 9,
                'pali': 'ชะลาพุชา เยปิ จะ อัณฑะสัมภะวา,',
                'pali_roman': 'Jalābujā yepi ca aṇḍasambhavā,',
                'thai': '',
                'paiboon': '',
                'english': 'Those born from the womb, and those born from eggs,',
            },
            {
                'number': 10,
                'pali': 'สังเสทะชาตา อะถะโวปะปาติกา,',
                'pali_roman': 'Saṃsedajātā athavopapātikā,',
                'thai': '',
                'paiboon': '',
                'english': 'born of moisture, or spontaneously arisen,',
            },
            {
                'number': 11,
                'pali': 'นิยยานิกัง ธัมมะวะรัง ปะฏิจจะ เต,',
                'pali_roman': 'Niyyānikaṃ dhammavaraṃ paṭicca te,',
                'thai': '',
                'paiboon': '',
                'english': 'depending on the excellent Dhamma that leads out,',
            },
            {
                'number': 12,
                'pali': 'สัพเพปิ ทุกขัสสะ กะโรนตุ สังขะยัง.',
                'pali_roman': 'Sabbepi dukkhassa karontu saṅkhayaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'may they all bring about the ending of suffering.',
            },
            # ‼ CHECK [IMG_0270.PNG]: TWO-COLUMN LAYOUT, in the Thai-script
            #   part of the book. From verse 13 the page is set in two columns
            #   and one printed ROW is one verse, split across the gutter —
            #   ฐาตุ จิรัง สะตัง ธัมโม on the left, ธัมมัทธะรา จะ ปุคคะลา on
            #   the right. I have read ACROSS each row and joined the halves
            #   with a single space. Please confirm the pairings, because
            #   reading down a column instead would give fluent and completely
            #   wrong Pali.
            # ‼ CHECK [IMG_0270.PNG]: The book prints no heading where the
            #   two-column section begins, and no blank line either — the
            #   change of layout is the only signal that something new starts.
            #   I have treated it as one chant with a section label of my own.
            #   It may well be a separate blessing verse that the book simply
            #   runs on. Worth deciding when you have the book open.
            {
                'number': 13,
                'section': 'ฐาตุ จิรัง: The Closing Blessing',
                'pali': 'ฐาตุ จิรัง สะตัง ธัมโม ธัมมัทธะรา จะ ปุคคะลา',
                'pali_roman': 'Ṭhātu ciraṃ sataṃ dhammo dhammaddharā ca puggalā',
                'thai': '',
                'paiboon': '',
                'english': 'May the Dhamma of the good stand long, and those who uphold it,',
            },
            {
                'number': 14,
                'pali': 'สังโฆ โหตุ สะมัคโค วะ อัตถายะ จะ หิตายะ จะ',
                'pali_roman': 'Saṅgho hotu samaggo va atthāya ca hitāya ca',
                'thai': '',
                'paiboon': '',
                'english': 'may the Sangha be united, for welfare and for benefit,',
            },
            {
                'number': 15,
                'pali': 'อัมเห รักขะตุ สัทธัมโม สัพเพปิ ธัมมะจาริโน',
                'pali_roman': 'Amhe rakkhatu saddhammo sabbepi dhammacārino',
                'thai': '',
                'paiboon': '',
                'english': 'may the true Dhamma protect us, and all who walk in Dhamma,',
            },
            {
                'number': 16,
                'page': 8,
                'pali': 'วุฑฒิง สัมปาปุเณยยามะ ธัมเม อะริยัปปะเวทิเต',
                'pali_roman': 'Vuḍḍhiṃ sampāpuṇeyyāma dhamme ariyappavedite',
                'thai': '',
                'paiboon': '',
                'english': 'may we attain growth in the Dhamma made known by the Noble Ones.',
            },
            {
                'number': 17,
                'pali': 'ปะสันนา โหนตุ สัพเพปิ ปาณิโน พุทธะสาสะเน',
                'pali_roman': 'Pasannā hontu sabbepi pāṇino buddhasāsane',
                'thai': '',
                'paiboon': '',
                'english': "May all living beings have faith in the Buddha's teaching,",
            },
            {
                'number': 18,
                'pali': 'สัมมา ธารัง ปะเวจฉันโต กาเล เทโว ปะวัสสะตุ',
                'pali_roman': 'Sammā dhāraṃ pavecchanto kāle devo pavassatu',
                'thai': '',
                'paiboon': '',
                'english': 'may the rain god send down showers in season,',
            },
            {
                'number': 19,
                'pali': 'วุฑฒิภาวายะ สัตตานัง สะมิทธัง เนตุ เมทะนิง',
                'pali_roman': 'Vuḍḍhibhāvāya sattānaṃ samiddhaṃ netu medaniṃ',
                'thai': '',
                'paiboon': '',
                'english': 'and bring the earth to plenty for the growth of beings.',
            },
            # ‼ CHECK [IMG_0270.PNG]: อัต๎ระชัง carries the ๎ mark over the ต.
            #   Reproduced as printed.
            {
                'number': 20,
                'pali': 'มาตาปิตา จะ อัต๎ระชัง นิจจัง รักขันติ ปุตตะกัง',
                'pali_roman': 'Mātāpitā ca atrajaṃ niccaṃ rakkhanti puttakaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'As mother and father ever protect their own child,',
            },
            {
                'number': 21,
                'pali': 'เอวัง ธัมเมนะ ราชาโน ปะชัง รักขันตุ สัพพะทา.',
                'pali_roman': 'Evaṃ dhammena rājāno pajaṃ rakkhantu sabbadā.',
                'thai': '',
                'paiboon': '',
                'english': 'so may rulers ever protect their people by Dhamma.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0271.PNG]: THIS IS A VARIANT, NOT A NEW CHANT. It is
        #   the closing of สังเวคะปะริกิตตะนะปาฐะ rewritten for lay chanters,
        #   printed inside the explanatory section คำอธิบายประกอบทำวัตรเช้า.
        #   The monastic version is already in the app as samvega-parikittana-
        #   patha, verses 35-40. Decide whether you want it as a chant of its
        #   own, folded into the parent as an alternative reading, or left out
        #   of the app entirely — I have entered it rather than dropping
        #   printed Pali, but the id and English title are mine.
        # ‼ CHECK [IMG_0271.PNG]: The rest of page 8 is ordinary Thai
        #   instruction: numbered notes about which words lay chanters
        #   substitute in สังเวคะปะริกิตตะนะปาฐะ. Not chant text; recorded in
        #   the page note.
        'id': 'samvega-parikittana-patha-lay-variant',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': "The Passage on Spiritual Urgency — lay chanters' version",
        'page_start': 8,
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            # ‼ CHECK [IMG_0271.PNG]: A superscript 1 follows คะโต. The
            #   footnote is in ARABIC numerals and is NOT a canonical citation
            #   but an editorial note: '1. คะโต สำหรับอุบาสก ถ้าอุบาสิกา ใช้
            #   คะตา' — use คะโต if you are a layman, คะตา if a laywoman.
            #   Recorded here rather than in source_printed, because
            #   source_printed is for the book citing its canon and this is
            #   the book instructing the reader.
            {
                'number': 1,
                'pali': 'จิระปะรินิพพุตัมปิ ตัง ภะคะวันตัง สะระณัง คะโต,',
                'pali_roman': 'Cira-parinibbutampi taṃ bhagavantaṃ saraṇaṃ gato,',
                'thai': '',
                'paiboon': '',
                'english': 'Having gone for refuge to that Blessed One, though long since attained to final Nibbāna,',
            },
            {
                'number': 2,
                'pali': 'ธัมมัญจะ ภิกขุสังฆัญจะ ตัสสะ ภะคะวะโต สาสะนัง,',
                'pali_roman': 'Dhammañca bhikkhusaṅghañca tassa bhagavato sāsanaṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'and to the Dhamma and the Bhikkhu Sangha, the teaching of that Blessed One,',
            },
            {
                'number': 3,
                'pali': 'ยะถาสัตติ ยะถาพะลัง มะนะสิกะโรมะ,',
                'pali_roman': 'Yathāsatti yathābalaṃ manasikaroma,',
                'thai': '',
                'paiboon': '',
                'english': 'we attend to it as far as our ability and strength allow,',
            },
            {
                'number': 4,
                'pali': 'อะนุปะฏิปัชชามะ,',
                'pali_roman': 'Anupaṭipajjāma,',
                'thai': '',
                'paiboon': '',
                'english': 'and practise accordingly.',
            },
            {
                'number': 5,
                'pali': 'สา สา โน ปะฏิปัตติ,',
                'pali_roman': 'Sā sā no paṭipatti,',
                'thai': '',
                'paiboon': '',
                'english': 'May that practice of ours',
            },
            {
                'number': 6,
                'pali': 'อิมัสสะ เกวะลัสสะ ทุกขักขันธัสสะ อันตะกิริยายะ สังวัตตะตูติ.',
                'pali_roman': 'Imassa kevalassa dukkhakkhandhassa antakiriyāya saṃvattatūti.',
                'thai': '',
                'paiboon': '',
                'english': 'lead to the ending of this whole mass of suffering.',
            },
        ],
    },
    {
        # ‼ CHECK [IMG_0272.PNG] VERSE 5: the book prints สัพพะทุกขูกะสะมะ -
        #   with ก. Checked at 6x magnification: the glyph has no ascender
        #   and is plainly ก, not ป, unlike the ป two syllables later on the
        #   same line. The expected Pali here is sabbadukkhūpasama
        #   (สัพพะทุกขูปะสะมะ), 'the stilling of all suffering'. Reproduced
        #   AS PRINTED and not corrected. Please look at this line in the
        #   physical book: either this edition prints it so, or it is a typo
        #   in this printing, and I cannot tell which.
        # ‼ CHECK [IMG_0272.PNG] VERSE 8: the book breaks
        #   ปัจฉิมาชะนะ-ตานุกัมปัง across a line with a hyphen. Rejoined to
        #   ปัจฉิมาชะนะตานุกัมปัง, as the rule for typesetter's line breaks
        #   requires. The hyphen is not reproduced.
        # ‼ CHECK [IMG_0272.PNG] VERSE 6: อานิยะติ read with a long อา. Worth
        #   a glance - อะนิยะติ would also be a plausible reading at this
        #   print size and the two differ in meaning.
        # ‼ CHECK [IMG_0272.PNG] TITLE: the book prints no title for this
        #   passage at all; it is introduced only by instruction item 5.
        #   title_thai and title_pali left EMPTY rather than invented.
        #   title_english is the app's own and will be hidden in book layout.
        # ‼ CHECK [IMG_0272.PNG] VERSE SEGMENTATION: split at the printed
        #   commas, following the book's own instruction elsewhere to
        #   หยุดตามจุดลูกน้ำ (stop at the commas). 18 units.
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written by stage 3. Verses
        #   are complete.
        # ‼ CHECK [IMG_0272.PNG] RELATION TO PAGE 2: this is the พิสดาร
        #   (elaborate) form of the invitation, used on วันธรรมสวนะ and
        #   Sundays. The ordinary form is kham-choen-bucha-lae-suat-namo on
        #   page 2. They open with the same words and then diverge - do not
        #   merge them.
        'id': 'kham-choen-bucha-phitsadan',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Elaborate Invitation to Revere the Triple Gem',
        'group': 'Morning chanting',
        'page_start': 9,
        'layout': 'prose',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'ยะมัมหะ โข มะยัง ภะคะวันตัง สะระณัง คะตา,',
                'pali_roman': 'yamamha kho mayaṃ bhagavantaṃ saraṇaṃ gatā,',
                'thai': '',
                'paiboon': '',
                'english': 'The Blessed One to whom we have gone for refuge,',
            },
            {
                'number': 2,
                'pali': 'อุททิสสะ ปัพพะชิตา โย โน ภะคะวา สัตถา,',
                'pali_roman': 'uddissa pabbajitā yo no bhagavā satthā,',
                'thai': '',
                'paiboon': '',
                'english': 'for whose sake we have gone forth, who is our Teacher,',
            },
            {
                'number': 3,
                'pali': 'ยัสสะ จะ มะยัง ภะคะวะโต ธัมมัง โรเจมะ,',
                'pali_roman': 'yassa ca mayaṃ bhagavato dhammaṃ rocema,',
                'thai': '',
                'paiboon': '',
                'english': 'and in whose Dhamma we delight -',
            },
            {
                'number': 4,
                'pali': 'ตัสสะ โข ปะนะ ภะคะวะโต โลเกกุตตะมะสัตถุภูตัสสะ,',
                'pali_roman': 'tassa kho pana bhagavato lokekuttamasatthubhūtassa,',
                'thai': '',
                'paiboon': '',
                'english': 'that Blessed One, being the supreme teacher in the world,',
            },
            {
                'number': 5,
                'pali': 'สัพพะทุกขูกะสะมะปะรินิพพานายะ ธัมมัง เทสะยะโต,',
                'pali_roman': 'sabbadukkhūkasamaparinibbānāya dhammaṃ desayato,',
                'thai': '',
                'paiboon': '',
                'english': 'who taught the Dhamma for the stilling of all suffering and for final liberation -',
            },
            {
                'number': 6,
                'pali': 'อะยัง ธัมมะวินะโย ยาวัชชะตะนาปิ ยะถากะถัญจิ อานิยะติ ปะวัตติยะติ,',
                'pali_roman': 'ayaṃ dhammavinayo yāvajjatanāpi yathākathañci āniyati pavattiyati,',
                'thai': '',
                'paiboon': '',
                'english': 'this Dhamma and Discipline is still carried on, in one way or another, even to this day.',
            },
            {
                'number': 7,
                'pali': 'ตาทิเส ธัมเม ปะสาทูปะจารายะ,',
                'pali_roman': 'tādise dhamme pasādūpacārāya,',
                'thai': '',
                'paiboon': '',
                'english': 'For the growing of confidence in such a Dhamma,',
            },
            {
                'number': 8,
                'pali': 'เตนะ ภะคะวะตา ปัจฉิมาชะนะตานุกัมปัง ปะฏิจจะ อัตตะโน อัจจะเยนะ ถูปะปะติฏฐาปะนัง อะนุมะตัง,',
                'pali_roman': 'tena bhagavatā pacchimājanatānukampaṃ paṭicca attano accayena thūpapatiṭṭhāpanaṃ anumataṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'the Blessed One, out of compassion for later generations, permitted the establishing of a shrine after his passing.',
            },
            {
                'number': 9,
                'pali': 'ตัง โข ปะนะ ภะคะวะโต อะนุมะติง อุปาทายะ,',
                'pali_roman': 'taṃ kho pana bhagavato anumatiṃ upādāya,',
                'thai': '',
                'paiboon': '',
                'english': 'Taking up that permission of the Blessed One,',
            },
            {
                'number': 10,
                'pali': 'อะยัง ปะฏิมา มะหาสุระสิงหะนาเทนะ ปะวะระราเชนะ ตัง ภะคะวันตัง อุททิสสะ กะตา ปะติฏฐาปิตา,',
                'pali_roman': 'ayaṃ paṭimā mahāsurasīhanādena pavararājena taṃ bhagavantaṃ uddissa katā patiṭṭhāpitā,',
                'thai': '',
                'paiboon': '',
                'english': 'this image was made and established by the noble prince Mahāsurasīhanāda, dedicated to that Blessed One,',
            },
            {
                'number': 11,
                'pali': 'ยาวะเทวะ ทัสสะเนนะ ตัง ภะคะวันตัง อะนุสสะริตวา ปะสาทะสังเวคะปะฏิลาภายะ เจวะ,',
                'pali_roman': 'yāvadeva dassanena taṃ bhagavantaṃ anussaritvā pasādasaṃvegapaṭilābhāya ceva,',
                'thai': '',
                'paiboon': '',
                'english': 'solely so that, seeing it and calling that Blessed One to mind, one may gain confidence and a sense of urgency,',
            },
            {
                'number': 12,
                'pali': 'ตัปปัจจะยา สัมมาปะฏิปัตติปะริปูระณัตถายะ จะ,',
                'pali_roman': 'tappaccayā sammāpaṭipattiparipūraṇatthāya ca,',
                'thai': '',
                'paiboon': '',
                'english': 'and, on that account, may fulfil the right practice.',
            },
            {
                'number': 13,
                'pali': 'มะยัญจัมหะ อิมัง ฐานัง สัมปัตตา,',
                'pali_roman': 'mayañcamha imaṃ ṭhānaṃ sampattā,',
                'thai': '',
                'paiboon': '',
                'english': 'And we, having arrived at this place,',
            },
            {
                'number': 14,
                'pali': 'อิเม สักกาเร อิมัส์มิง สีหาสะเน อาโรเปต์วา,',
                'pali_roman': 'ime sakkāre imasmiṃ sīhāsane āropetvā,',
                'thai': '',
                'paiboon': '',
                'english': 'having placed these offerings upon this lion-throne,',
            },
            {
                'number': 15,
                'pali': 'ตัสสะ ภะคะวะโต สุจิระปะรินิพพุตัสสาปิ สะโต,',
                'pali_roman': 'tassa bhagavato suciraparinibbutassāpi sato,',
                'thai': '',
                'paiboon': '',
                'english': 'to that Blessed One, though he attained final Nibbāna long ago,',
            },
            {
                'number': 16,
                'pali': 'สักการัง กะริต์วา อะภิวาทะนัง กะริมหา,',
                'pali_roman': 'sakkāraṃ karitvā abhivādanaṃ karimhā,',
                'thai': '',
                'paiboon': '',
                'english': 'have made our offering and paid our homage.',
            },
            {
                'number': 17,
                'pali': 'หันทะทานิ มะยัง ตัง ภะคะวันตัง วาจายะ อะภิถุตุง,',
                'pali_roman': 'handadāni mayaṃ taṃ bhagavantaṃ vācāya abhithutuṃ,',
                'thai': '',
                'paiboon': '',
                'english': 'Now, to praise that Blessed One in speech,',
            },
            {
                'number': 18,
                'pali': 'ปุพพะภาคะนะมะการัง กะโรมะ เส.',
                'pali_roman': 'pubbabhāganamakāraṃ karoma se.',
                'thai': '',
                'paiboon': '',
                'english': 'let us make the preliminary salutation.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0273.PNG]: THE MOST IMPORTANT CHECK ON THIS PAGE. The
        #   book prints the whole Pali passage as one prose block, then the
        #   whole คำแปล as another. The Thai is a free, expanded rendering,
        #   not a unit-for-unit translation — verse 1's Thai opens with a
        #   preamble ('ข้าพเจ้าขอประกาศเริ่มเรื่อง…') that has no Pali behind
        #   it. The 5-to-5 pairing of Pali units to Thai chunks is mine, made
        #   by meaning. Please read it against the page.
        # ‼ CHECK [IMG_0273.PNG]: The book prints no Pali title and no
        #   romanised title for this passage — only the Thai heading
        #   คำประกาศอุโบสถ. title_pali is left empty rather than invented;
        #   title_english is the app's own.
        # ‼ CHECK [IMG_0273.PNG]: No invitation (หันทะ มะยัง…) is printed for
        #   this passage. None has been written.
        # ‼ CHECK [IMG_0274.PNG]: PAGE FIDELITY: all five Pali units are on
        #   page 10, but the คำแปล block begins on page 10 and finishes on
        #   page 11. So the `thai` layer of verses 3, 4 and 5 is physically
        #   printed on page 11 while their `pali` is on page 10. The page map
        #   assigns all five verses to page 10 (the page the Pali starts on)
        #   and gives page 11 a `verses: none` row rather than claiming them
        #   twice.
        'id': 'kham-prakat-ubosot',
        'title_thai': 'คำประกาศอุโบสถ',
        'title_pali': '',
        'title_roman': 'Kham Prakat Ubosot',
        'title_english': 'The Announcement of the Uposatha',
        'page_start': 10,
        'layout': 'prose',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            # ‼ CHECK [IMG_0273.PNG]: The numeral '15' in the Thai layer is
            #   printed in Arabic digits, not Thai numerals. Reproduced as
            #   printed. Same for '8' in verses 2 and 3 and the '1' repeated
            #   after each abstention in verse 4 (which is the book's way of
            #   counting items, not a footnote marker).
            {
                'number': 1,
                'pali': 'อัชชะ โภนโต ปักขัสสะ ปัณณะระสี ทิวะโส',
                'pali_roman': 'ajja bhonto pakkhassa paṇṇarasī divaso',
                'thai': 'ข้าพเจ้าขอประกาศเริ่มเรื่อง ในการที่จะได้รักษาอุโบสถ ให้สาธุชนทราบทั่วกัน ก่อนแต่สมาทาน ณ บัดนี้ วันนี้เป็นปัณณรสีดิถีที่ 15 แห่งปักษ์',
                'paiboon': 'kâa-pá-jâo kɔ̌ɔ bprà-gàat rə̂əm rʉ̂aŋ nai gaan tîi jà dâai rák-sǎa ù-boo-sòt hâi sǎa-tú-chon sâap tûa-gan gɔ̀ɔn dtɛ̀ɛ sà-maa-taan ná bàt-níi wan-níi bpen bpan-ná-rá-sǐi dì-tǐi tîi sìp-hâa hɛ̀ŋ bpàk',
                'english': 'Venerable sirs, today is the fifteenth day of the lunar fortnight.',
            },
            # ‼ CHECK [IMG_0273.PNG]: 'อุปาสะกะอุปาสิกานัง' is printed as one
            #   unbroken run. I have romanised it 'upāsaka-upāsikānaṃ' with a
            #   hyphen for legibility, which the Thai does not have. Say if
            #   you would rather it were unhyphenated.
            {
                'number': 2,
                'pali': 'เอวะรูโป โข โภนโต ทิวะโส, พุทเธนะ ภะคะวะตา ปัญญัตตัสสะ ธัมมัสสะวะนัสสะ เจวะ ตะทัตถายะ อุปาสะกะอุปาสิกานัง อุโปสะถัสสะ จะ กาโล โหติ,',
                'pali_roman': 'evarūpo kho bhonto divaso, buddhena bhagavatā paññattassa dhammassavanassa ceva tadatthāya upāsaka-upāsikānaṃ uposathassa ca kālo hoti,',
                'thai': 'ก็แลมีนิยมเช่นนี้ เป็นกาลที่สาธุชนทั้งอุบาสกอุบาสิกาจะได้ฟังธรรม และรักษาอุโบสถพร้อมด้วยองค์ 8 ประการ เพื่อประโยชน์แก่การฟังธรรมนั้น',
                'paiboon': 'gɔ̂ɔ lɛɛ mii ní-yom chên-níi bpen gaan tîi sǎa-tú-chon táŋ ù-baa-sòk ù-baa-sì-gaa jà dâai faŋ tam lɛ́ rák-sǎa ù-boo-sòt prɔ́ɔm dûai oŋ bpɛ̀ɛt bprà-gaan pʉ̂a bprà-yòot gɛ̀ɛ gaan faŋ tam nán',
                'english': 'Such a day as this, venerable sirs, is the time appointed by the Buddha, the Blessed One, for the hearing of the Dhamma, and for that same purpose the time of the Uposatha for laymen and laywomen.',
            },
            {
                'number': 3,
                'pali': 'หันทะ มะยัง โภนโต สัพเพ อิธะ สะมาคะตา ตัสสะ ภะคะวะโต ธัมมานุธัมมะปะฏิปัตติยา ปูชะนัตถายะ อิมัญจะ รัตติง อิมัญจะ ทิวะสัง อุโปสะถัง อุปะวะสิสสามาติ,',
                'pali_roman': 'handa mayaṃ bhonto sabbe idha samāgatā tassa bhagavato dhammānudhammapaṭipattiyā pūjanatthāya imañca rattiṃ imañca divasaṃ uposathaṃ upavasissāmāti,',
                'thai': 'บัดนี้ ขอกุศลอันยิ่งใหญ่ คือ ตั้งจิตสมาทานองค์ 8 ประการแห่งอุโบสถนั้น จงเกิดมีแก่สาธุชนทั้งหลายซึ่งมาประชุมพร้อมกัน ณ ที่นี้',
                'paiboon': 'bàt-níi kɔ̌ɔ gù-sǒn an yîŋ-yài kʉʉ dtâŋ jìt sà-maa-taan oŋ bpɛ̀ɛt bprà-gaan hɛ̀ŋ ù-boo-sòt nán joŋ gə̀ət mii gɛ̀ɛ sǎa-tú-chon táŋ-lǎai sʉ̂ŋ maa bprà-chum prɔ́ɔm-gan ná tîi-níi',
                'english': 'Come then, venerable sirs, let all of us gathered here, in honour of that Blessed One and by practice in accordance with the Dhamma, keep the Uposatha for this night and this day.',
            },
            # ‼ CHECK [IMG_0274.PNG]: The Thai near the end of this verse
            #   reads 'จงสมาทานองค์ 5 ประการนั้นโดยเคารพ' — FIVE factors —
            #   where the same passage says eight everywhere else (องค์ 8
            #   ประการ in verses 2 and 3, and the eight abstentions are listed
            #   out in this very verse). Reproduced exactly as printed. This
            #   is either a misprint in the book or my misreading of the
            #   digit, and it needs the physical page. Do not let me 'correct'
            #   it.
            # ‼ CHECK [IMG_0273.PNG]: The yamakkan mark ๎ appears in กัต๎วา,
            #   กะริต๎วา and หุต๎วา, marking the consonant cluster. Reproduced
            #   as printed rather than normalised to กัตวา / กะริตวา / หุตวา.
            {
                'number': 4,
                'pali': 'กาละปะริจเฉทัง กัต๎วา ตัง ตัง เวระมะณิง อารัมมะณัง กะริต๎วา อะวิกขิตตะจิตตา หุต๎วา สักกัจจัง อุโปสะถัง สะมาทิเยยยามะ.',
                'pali_roman': 'kālaparicchedaṃ katvā taṃ taṃ veramaṇiṃ ārammaṇaṃ karitvā avikkhittacittā hutvā sakkaccaṃ uposathaṃ samādiyeyyāma.',
                'thai': 'จงตั้งจิตคิดกำหนดกาลว่า จะรักษาอุโบสถสิ้นราตรีและวันนี้ จงทำความเว้นจากโทษนั้น ๆ ให้เป็นอารมณ์ คือ เว้นจากการฆ่าสัตว์ 1 เว้นจากลักทรัพย์ 1 เว้นจากกรรมอันเป็นข้าศึกแก่พรหมจรรย์ 1 เว้นจากพูดเท็จ 1 เว้นจากดื่มน้ำเมาคือสุราและเมรัย 1 เว้นจากบริโภคอาหารในเวลาวิกาล ตั้งแต่เที่ยงแล้วไป 1 เว้นจากฟ้อนรำขับร้องประโคมดนตรีและดูการเล่นอันเป็นข้าศึกแก่กุศล และทัดทรงประดับตกแต่งร่างกายด้วยระเบียบดอกไม้ของหอมเครื่องย้อมเครื่องทา 1 เว้นจากที่นอนสูงและที่นอนใหญ่ ภายในยัดด้วยนุ่นและสำลี 1 ฉะนี้ อย่าให้จิตฟุ้งซ่านส่งไปที่อื่น จงสมาทานองค์ 5 ประการนั้นโดยเคารพ เพื่อจะบูชาสมเด็จพระผู้มีพระภาคเจ้าพระองค์นั้น ด้วยธรรมานุธรรมปฏิบัติ ตามกำลังของคฤหัสถ์ทั้งหลาย',
                'paiboon': 'joŋ dtâŋ jìt kít gam-nòt gaan wâa jà rák-sǎa ù-boo-sòt sîn raa-dtrii lɛ́ wan-níi joŋ tam kwaam wén jàak tôot nán-nán hâi bpen aa-rom kʉʉ wén jàak gaan kâa sàt nʉ̀ŋ wén jàak lák sáp nʉ̀ŋ wén jàak gam an bpen kâa-sʉ̀k gɛ̀ɛ prom-má-jan nʉ̀ŋ wén jàak pûut tét nʉ̀ŋ wén jàak dʉ̀ʉm nám-mao kʉʉ sù-raa lɛ́ mee-rai nʉ̀ŋ wén jàak bɔɔ-rí-pôok aa-hǎan nai wee-laa wí-gaan dtâŋ-dtɛ̀ɛ tîaŋ lɛ́ɛo bpai nʉ̀ŋ wén jàak fɔ́ɔn-ram kàp-rɔ́ɔŋ bprà-koom don-dtrii lɛ́ duu gaan-lên an bpen kâa-sʉ̀k gɛ̀ɛ gù-sǒn lɛ́ tát-soŋ bprà-dàp dtòk-dtɛ̀ŋ râaŋ-gaai dûai rá-bìap dɔ̀ɔk-máai kɔ̌ɔŋ-hɔ̌ɔm krʉ̂aŋ-yɔ́ɔm krʉ̂aŋ-taa nʉ̀ŋ wén jàak tîi-nɔɔn sǔuŋ lɛ́ tîi-nɔɔn yài paai-nai yát dûai nûn lɛ́ sǎm-lii nʉ̀ŋ chà-níi yàa hâi jìt fúŋ-sâan sòŋ bpai tîi-ʉ̀ʉn joŋ sà-maa-taan oŋ hâa bprà-gaan nán dooi kao-róp pʉ̂a jà buu-chaa sǒm-dèt prá-pûu-mii-prá-pâak-jâo prá-oŋ nán dûai tam-maa-nú-tam-bpà-dtì-bàt dtaam gam-laŋ kɔ̌ɔŋ ká-rʉ́-hàt táŋ-lǎai',
                'english': 'Having marked out the period of time, and having made each several abstention the object of the mind, with minds undistracted let us respectfully undertake the Uposatha.',
            },
            {
                'number': 5,
                'pali': 'อีทิสัง หิ อุโปสะถัง สัมปัตตานัง อัมหากัง ชีวิตัง มา นิรัตถะกัง โหตุ.',
                'pali_roman': 'īdisaṃ hi uposathaṃ sampattānaṃ amhākaṃ jīvitaṃ mā niratthakaṃ hotu.',
                'thai': 'ชีวิตของเราทั้งหลายที่ได้ดำรงมาจนถึงวันอุโบสถเช่นนี้ อย่าให้ล่วงไปเปล่าปราศจากประโยชน์เลย',
                'paiboon': 'chii-wít kɔ̌ɔŋ rao táŋ-lǎai tîi dâai dam-roŋ maa jon-tʉ̌ŋ wan ù-boo-sòt chên-níi yàa hâi lûaŋ bpai bplàao bpràat-sà-jàak bprà-yòot ləəi',
                'english': 'For to us who have reached such an Uposatha as this, may our life not be barren of fruit.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0274.PNG]: The book prints this in Pali only, with no
        #   Thai translation, so `thai` and `paiboon` are empty and
        #   english_unverified is set — the English is a working translation
        #   made for this edition, not the book's.
        # ‼ CHECK [IMG_0274.PNG]: No Pali title is printed, only the Thai
        #   heading คำอาราธนาอุโบสถศีล. title_pali left empty.
        # ‼ CHECK [IMG_0274.PNG]: All three repetitions are printed in full
        #   and are recorded in full. The book does not abbreviate the second
        #   and third with ฯเปฯ, so neither do I.
        'id': 'kham-aradhana-ubosot-sila',
        'title_thai': 'คำอาราธนาอุโบสถศีล',
        'title_pali': '',
        'title_roman': 'Kham Aradhana Ubosot Sila',
        'title_english': 'The Request for the Uposatha Precepts',
        'page_start': 11,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            # ‼ CHECK [IMG_0274.PNG]: The comma placement — 'มะยัง ภันเต,
            #   ติสะระเณนะ สะหะ,' — is reproduced as printed, including the
            #   comma after สะหะ.
            {
                'number': 1,
                'pali': 'มะยัง ภันเต, ติสะระเณนะ สะหะ, อัฏฐังคะสะมันนาคะตัง อุโปสะถัง ยาจามะ.',
                'pali_roman': 'mayaṃ bhante, tisaraṇena saha, aṭṭhaṅgasamannāgataṃ uposathaṃ yācāma.',
                'thai': '',
                'paiboon': '',
                'english': 'Venerable sir, we ask for the Uposatha endowed with eight factors, together with the Three Refuges.',
            },
            {
                'number': 2,
                'pali': 'ทุติยัมปิ มะยัง ภันเต, ติสะระเณนะ สะหะ, อัฏฐังคะสะมันนาคะตัง อุโปสะถัง ยาจามะ.',
                'pali_roman': 'dutiyampi mayaṃ bhante, tisaraṇena saha, aṭṭhaṅgasamannāgataṃ uposathaṃ yācāma.',
                'thai': '',
                'paiboon': '',
                'english': 'For a second time, venerable sir, we ask for the Uposatha endowed with eight factors, together with the Three Refuges.',
            },
            {
                'number': 3,
                'pali': 'ตะติยัมปิ มะยัง ภันเต, ติสะระเณนะ สะหะ, อัฏฐังคะสะมันนาคะตัง อุโปสะถัง ยาจามะ.',
                'pali_roman': 'tatiyampi mayaṃ bhante, tisaraṇena saha, aṭṭhaṅgasamannāgataṃ uposathaṃ yācāma.',
                'thai': '',
                'paiboon': '',
                'english': 'For a third time, venerable sir, we ask for the Uposatha endowed with eight factors, together with the Three Refuges.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0275.PNG]: The book prints NO title for this passage.
        #   The id and the English title are mine; title_thai and title_pali
        #   are left empty rather than invented. Same treatment as
        #   'pubbabhaga-namakara' on page 2.
        # ‼ CHECK [IMG_0275.PNG]: Grouping the นะโม (verses 1-3) together with
        #   the refuge-going (verses 4-6) as ONE chant is my reading. The book
        #   separates them only by a line break, and closes the whole with
        #   ติสะระณะคะมะนัง นิฏฐิตัง, which names only the refuge-going.
        #   Splitting them into two chants is defensible and is your call.
        # ‼ CHECK [IMG_0275.PNG]: ขุ.ขุ. abbreviates ขุททกนิกาย ขุททกปาฐะ —
        #   Khuddaka-nikāya, Khuddakapāṭha. Recorded here rather than in the
        #   field, because the reference is reproduced exactly as printed and
        #   never expanded.
        'id': 'tisarana-gamana-ubosot',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Going to the Three Refuges, for the Uposatha',
        'page_start': 12,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            # ‼ CHECK [IMG_0275.PNG]: DECISION NEEDED. Verses 1-3 are the same
            #   นะโม line already in the app as 'pubbabhaga-namakara' on page
            #   2. I have NOT treated this as a repeat, because the prompt's
            #   rule is that a printing which DIFFERS is not a repeat, and
            #   this one differs twice over: page 2 prints it with a closing
            #   full stop and page 12 does not, and here it runs straight on
            #   into the refuges as one act led by the elder rather than
            #   standing alone after its own invitation. A chant dict also
            #   carries only ONE page_start, so making it a repeat would leave
            #   page 12 in the app without the นะโม the book prints on it.
            #   Please confirm this is the right call — it will recur
            #   constantly across a book whose services overlap.
            {
                'number': 1,
                'pali': 'นะโม ตัสสะ ภะคะวะโต อะระหะโต สัมมาสัมพุทธัสสะ',
                'pali_roman': 'namo tassa bhagavato arahato sammāsambuddhassa',
                'thai': '',
                'paiboon': '',
                'english': 'Homage to the Blessed One, the Worthy One, the Perfectly Self-Awakened One.',
            },
            {
                'number': 2,
                'pali': 'นะโม ตัสสะ ภะคะวะโต อะระหะโต สัมมาสัมพุทธัสสะ',
                'pali_roman': 'namo tassa bhagavato arahato sammāsambuddhassa',
                'thai': '',
                'paiboon': '',
                'english': 'Homage to the Blessed One, the Worthy One, the Perfectly Self-Awakened One.',
            },
            {
                'number': 3,
                'pali': 'นะโม ตัสสะ ภะคะวะโต อะระหะโต สัมมาสัมพุทธัสสะ',
                'pali_roman': 'namo tassa bhagavato arahato sammāsambuddhassa',
                'thai': '',
                'paiboon': '',
                'english': 'Homage to the Blessed One, the Worthy One, the Perfectly Self-Awakened One.',
            },
            # ‼ CHECK [IMG_0275.PNG]: Each refuge round is set as ONE printed
            #   line running Buddha, Dhamma, Saṅgha, so it is kept as one
            #   verse rather than split into three. Rounds 2 and 3 wrap onto a
            #   second line through justification only.
            {
                'number': 4,
                'pali': 'พุทธัง สะระณัง คัจฉามิ, ธัมมัง สะระณัง คัจฉามิ, สังฆัง สะระณัง คัจฉามิ,',
                'pali_roman': 'buddhaṃ saraṇaṃ gacchāmi, dhammaṃ saraṇaṃ gacchāmi, saṅghaṃ saraṇaṃ gacchāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'I go to the Buddha as refuge, I go to the Dhamma as refuge, I go to the Saṅgha as refuge,',
            },
            {
                'number': 5,
                'pali': 'ทุติยัมปิ พุทธัง สะระณัง คัจฉามิ, ทุติยัมปิ ธัมมัง สะระณัง คัจฉามิ, ทุติยัมปิ สังฆัง สะระณัง คัจฉามิ,',
                'pali_roman': 'dutiyampi buddhaṃ saraṇaṃ gacchāmi, dutiyampi dhammaṃ saraṇaṃ gacchāmi, dutiyampi saṅghaṃ saraṇaṃ gacchāmi,',
                'thai': '',
                'paiboon': '',
                'english': 'For a second time I go to the Buddha as refuge, for a second time I go to the Dhamma as refuge, for a second time I go to the Saṅgha as refuge,',
            },
            # ‼ CHECK [IMG_0275.PNG]: FOOTNOTE, ONE SERVING TWO MARKERS. Page
            #   12 prints a single footnote '1. ขุ.ขุ. 25/1-2' but TWO
            #   superscript 1 markers: one here on the last refuge line, one
            #   on precept 8 of อุโบสถศีล. The range fits both halves —
            #   Khuddakapāṭha 1 is the Saraṇattaya and 2 the Sikkhāpada. It is
            #   therefore carried as ONE page footnote block, not as
            #   source_printed on each chant, which would have printed the
            #   citation twice where the book prints it once. Neither chant
            #   carries source_printed as a result — say if you would rather
            #   the citation also hung off the chants for the study view.
            {
                'number': 6,
                'pali': 'ตะติยัมปิ พุทธัง สะระณัง คัจฉามิ, ตะติยัมปิ ธัมมัง สะระณัง คัจฉามิ, ตะติยัมปิ สังฆัง สะระณัง คัจฉามิ.',
                'pali_roman': 'tatiyampi buddhaṃ saraṇaṃ gacchāmi, tatiyampi dhammaṃ saraṇaṃ gacchāmi, tatiyampi saṅghaṃ saraṇaṃ gacchāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'For a third time I go to the Buddha as refuge, for a third time I go to the Dhamma as refuge, for a third time I go to the Saṅgha as refuge.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0275.PNG]: Pali only — the book prints no Thai
        #   translation anywhere on page 12, so `thai` and `paiboon` are empty
        #   on every verse and english_unverified is set.
        'id': 'ubosot-sila',
        'title_thai': 'อุโบสถศีล',
        'title_pali': '',
        'title_roman': 'Ubosot Sila',
        'title_english': 'The Eight Uposatha Precepts',
        'page_start': 12,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'ปาณาติปาตา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'pāṇātipātā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from taking life.',
            },
            {
                'number': 2,
                'pali': 'อะทินนาทานา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'adinnādānā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from taking what is not given.',
            },
            # ‼ CHECK [IMG_0275.PNG]: 'อะพ์รัห์มะจะริยา' carries the yamakkan
            #   mark ๎ on both พ์ and ห์, reproduced as printed rather than
            #   normalised to อะพรัหมะจะริยา.
            {
                'number': 3,
                'pali': 'อะพ์รัห์มะจะริยา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'abrahmacariyā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from unchastity.',
            },
            {
                'number': 4,
                'pali': 'มุสาวาทา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'musāvādā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from false speech.',
            },
            {
                'number': 5,
                'pali': 'สุราเมระยะมัชชะปะมาทัฏฐานา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'surāmerayamajjapamādaṭṭhānā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from distilled and fermented drink, which is the basis of heedlessness.',
            },
            {
                'number': 6,
                'pali': 'วิกาละโภชะนา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'vikālabhojanā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from eating at the wrong time.',
            },
            # ‼ CHECK [IMG_0275.PNG]: The seventh precept is a single unbroken
            #   compound running to 71 Thai characters, wrapping across two
            #   printed lines mid-word. Rejoined with the hyphenation dropped,
            #   per the run-on rule. Worth a careful look — it is the longest
            #   single word in the book so far.
            {
                'number': 7,
                'pali': 'นัจจะคีตะวาทิตะวิสูกะทัสสะนะมาลาคันธะวิเลปะนะธาระณะมัณฑะนะวิภูสะนัฏฐานา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'naccagītavāditavisūkadassanamālāgandhavilepanadhāraṇamaṇḍanavibhūsanaṭṭhānā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from dancing, singing, music and unseemly shows, and from wearing garlands, scents and cosmetics, and from adornment and beautifying.',
            },
            # ‼ CHECK [IMG_0275.PNG]: Footnote marker 1 sits here, and a
            #   second marker 1 sits on the last refuge line of the chant
            #   above. One printed footnote serves both, so it is carried once
            #   as a page footnote block and neither chant carries
            #   source_printed.
            {
                'number': 8,
                'pali': 'อุจจาสะยะนะมะหาสะยะนา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'uccāsayanamahāsayanā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from a high bed and a large bed.',
            },
            # ‼ CHECK [IMG_0275.PNG]: The book numbers the precepts 1-8 but
            #   prints this closing undertaking UNNUMBERED, immediately after
            #   precept 8. It is entered as verse 9 so it is not lost; say if
            #   you would rather it were set apart from the numbered eight.
            {
                'number': 9,
                'pali': 'อิมัง อัฏฐังคะสะมันนาคะตัง, พุทธะปัญญัตตัง อุโปสะถัง, อิมัญจะ รัตติง อิมัญจะ ทิวะสัง, สัมมะเทวะ อะภิรักขิตุง สะมาทิยามิ.',
                'pali_roman': 'imaṃ aṭṭhaṅgasamannāgataṃ, buddhapaññattaṃ uposathaṃ, imañca rattiṃ imañca divasaṃ, sammadeva abhirakkhituṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake to guard well, for this night and this day, this Uposatha endowed with eight factors and appointed by the Buddha.',
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


# ── What the page prints that is not a chant ────────────────────────────────
#
# Everything above hangs off a chant, because that is how you READ this book.
# But a printed page carries material that belongs to no chant at all: a
# heading, a paragraph telling the chanter what to do next, a closing that ends
# the whole morning service rather than the chant above it, a numbered note
# about which word a layperson substitutes.
#
# That material had nowhere to live, so it was dropped. Stage 1 read it off the
# photographs and wrote it into the batch files faithfully; stage 2 had no field
# to put it in and quietly let it go. Nothing failed, and pages 7 and 8 went live
# showing their chants and about half of what the book actually prints there.
#
# It is kept separate from CHANTS rather than added as more chant fields because
# it genuinely is not part of any chant. จบพิธีทำวัตรเช้า closes the morning
# SERVICE — attaching it to ปัตติทานะคาถา above it would say that chant ends
# twice, and would be a false statement about the book.
#
# One group = a run of blocks sitting at one point on one page:
#
#   'page'   — the printed page it appears on.
#   'after'  — the id of the chant whose text it FOLLOWS down the page. Omit it
#              (or None) for material printed above every chant on the page.
#   'blocks' — what is printed there, in printed order.
#
# `after` names a chant that must actually appear on that page; an anchor that
# matches nothing raises rather than being placed somewhere plausible. This is
# the same rule the page numbers follow, for the same reason — material shown in
# the wrong place on a page is read as though it belonged there.
#
# A block is one of five things the book does, and carries only what is printed:
#
#   'heading'         — a centred section heading (คำอธิบายประกอบทำวัตรเช้า).
#   'prose'           — a paragraph of Thai. Also how the book's OWN translation
#                       of a chant is set, where it prints one as a passage
#                       under a คำแปล heading rather than line by line.
#   'item'            — a numbered instruction. `number` is as PRINTED, so it
#                       keeps the book's own numbering across a page turn: items
#                       1-2 are on page 8 and 3-5 on page 9, and they are one
#                       list, not two lists starting at 1.
#   'service_closing' — a จบ… line ending a whole service.
#   'footnote'        — a foot-of-page note. `marker` is as printed, in whatever
#                       numerals the page uses. Unlike `source_printed` this is
#                       not necessarily a citation: page 8's footnote is an
#                       editorial note about a word substitution.
#
# `thai` is what the book prints, character for character. `english` is written
# for this app and never comes from the book, so it is flagged
# `english_unverified` exactly as an app-written chant translation is — and the
# reader is told, on every page it appears on.
PAGE_BLOCKS = [
    # ── Page 1 ──────────────────────────────────────────────────────────
    # The book opens here. Three headings stacked above the first chant: the
    # book's own running head, then the section, then the service.
    #
    # ‼ CHECK [IMG_0264.PNG]: page 1 prints NO page number at all — the top of
    #   the page is blank, as books do on a page carrying a major heading. Its
    #   number comes from the สารบัญ, which lists คำบูชาพระรัตนตรัย at ๑, and
    #   from the sequence. Worth confirming against the physical book.
    {
        'page': 1,
        'blocks': [
            {
                'type': 'heading',
                'thai': 'ระเบียบ',
                'english': 'The Order of Service',
                'english_unverified': True,
            },
            {
                'type': 'heading',
                'thai': 'ทำวัตร - สวดมนต์',
                'english': 'Devotions and Chanting',
                'english_unverified': True,
            },
            {
                'type': 'heading',
                'thai': 'ทำวัตรเช้า',
                'english': 'The Morning Service',
                'english_unverified': True,
            },
        ],
    },
    {
        'page': 1,
        'after': 'kham-namatsakan-phra-ratanattaya',
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'ประธานกล่าวเชิญบูชาพระรัตนตรัยและสวด นะโม '
                    'หยุดตามจุดลูกน้ำดังนี้.'
                ),
                'english': (
                    'The leader gives the invitation to revere the Triple Gem '
                    'and to chant the Namo, pausing at the commas, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },

    # ── Page 2 ──────────────────────────────────────────────────────────
    # The morning service opens, and the book's pattern for the whole service
    # starts here: the leader invites, the deputy begins the first words, the
    # rest join. Four of the chants on pages 2-3 are given no printed title at
    # all — they are identified by their invitation and nothing else.
    {
        'page': 2,
        'after': 'kham-choen-bucha-lae-suat-namo',
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้น บทว่า นะโม นอกนั้นรับต่อพร้อมกันไปจนครบ 3 หน '
                    'จบหนึ่งหยุดหายใจครั้งหนึ่ง ดังนี้'
                ),
                'english': (
                    'The deputy leader begins the word namo, and the rest join '
                    'together for three rounds, pausing for one breath at the '
                    'end of each, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    {
        'page': 2,
        'after': 'pubbabhaga-namakara',
        'blocks': [
            {
                'type': 'prose',
                'thai': 'ประธานกล่าวเชิญสวดสรรเสริญ พระพุทธคุณ ว่า',
                'english': (
                    'The leader gives the invitation to chant the praise of '
                    'the Buddha:'
                ),
                'english_unverified': True,
            },
            {'type': 'invitation', 'chant': 'buddhabhithuti'},
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้นบทว่า โย โส นอกนั้นรับต่อพร้อมกันไป '
                    'หยุดตามจุดลูกน้ำ ดังนี้.'
                ),
                'english': (
                    'The deputy leader begins the line yo so, and the rest '
                    'join together, pausing at the commas, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    {
        'page': 2,
        'after': 'buddhabhithuti',
        'blocks': [
            {
                'type': 'rubric',
                'thai': '(กราบพร้อมกัน)',
                'english': '(bow together)',
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': 'ประธานกล่าวเชิญสวดสรรเสริญ พระธรรมคุณ ว่า',
                'english': (
                    'The leader gives the invitation to chant the praise of '
                    'the Dhamma:'
                ),
                'english_unverified': True,
            },
            {'type': 'invitation', 'chant': 'dhammabhithuti'},
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้นบทว่า โย โส นอกนั้นรับต่อพร้อมกันไป '
                    'หยุดตามจุดลูกน้ำ ดังนี้.'
                ),
                'english': (
                    'The deputy leader begins the line yo so, and the rest '
                    'join together, pausing at the commas, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },

    # ── Page 3 ──────────────────────────────────────────────────────────
    {
        'page': 3,
        'after': 'dhammabhithuti',
        'blocks': [
            {
                'type': 'rubric',
                'thai': '(กราบพร้อมกัน)',
                'english': '(bow together)',
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': 'ประธานกล่าวเชิญสวดสรรเสริญ พระสังฆคุณ ว่า',
                'english': (
                    'The leader gives the invitation to chant the praise of '
                    'the Sangha:'
                ),
                'english_unverified': True,
            },
            {'type': 'invitation', 'chant': 'sanghabhithuti'},
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้นบทว่า โย โส นอกนั้นรับต่อพร้อมกันไป '
                    'หยุดตามจุดลูกน้ำ ดังนี้.'
                ),
                'english': (
                    'The deputy leader begins the line yo so, and the rest '
                    'join together, pausing at the commas, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    {
        'page': 3,
        'after': 'sanghabhithuti',
        # The one invitation covers BOTH chants — ระตะนัตตะยัปปะณามะคาถา and
        # สังเวคะปะริกิตตะนะปาฐะ — and the book prints it inside the sentence.
        # It is held on ระตะนัตตะยัปปะณามะคาถา, which is the chant that follows
        # it here; สังเวคะปะริกิตตะนะปาฐะ has none of its own and is not on
        # this page.
        'invitation_printed_here': ['ratanattayappanamagatha'],
        'blocks': [
            {
                'type': 'rubric',
                'thai': '(กราบพร้อมกัน แล้วนั่งพับเพียบทั้งหมด)',
                'english': (
                    '(bow together, then all sit in the side-resting posture)'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'ประธานกล่าวเชิญสวด ระตะนัตตะยัปปะณามะคาถา คือคำไหว้ พระรัตนตรัย '
                    'และสังเวคะปะริกิตตะนะปาฐะ คือบทประกาศความสลดสังเวชต่อไปว่า หันทะ มะยัง '
                    'ระตะนัตตะยัปปะณามะคาถาโย เจวะ สังเวคะปะริกิตตะนะปาฐัญจะ ภะณามะ เส.'
                ),
                'english': (
                    'The leader gives the invitation to chant the '
                    'Ratanattayappanamagatha, which is the salutation to the '
                    'Triple Gem, and the Saṃvega-parikittana-patha, which is '
                    'the passage declaring spiritual urgency, saying: handa '
                    'mayaṃ ratanattayappaṇāmagāthāyo ceva '
                    'saṃvegaparikittanapāṭhañca bhaṇāma se.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้นบทว่า พุทโธ นอกนั้นรับต่อพร้อมกันไป '
                    'หยุดตามจุดลูกน้ำ ดังนี้.'
                ),
                'english': (
                    'The deputy leader begins the line buddho, and the rest '
                    'join together, pausing at the commas, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },

    # ── Page 4 ──────────────────────────────────────────────────────────
    # Nothing to add. The page carries the end of ระตะนัตตะยัปปะณามะคาถา, the
    # printed title สังเวคะปะริกิตตะนะปาฐะ and that passage — no instruction,
    # no rubric, no footnote. Recorded here so a later reader knows the page
    # was checked and found to need nothing, rather than skipped.

    # ── Page 5 ──────────────────────────────────────────────────────────
    # The service proper ends a third of the way down and the rest of the page
    # is instruction: how the เสขิยวัตร are divided and chanted across three
    # days, and the invitation for each section. Those three invitations are
    # written out rather than read off a chant, because the sections they
    # invite are set much later in the book.
    {
        'page': 5,
        'after': 'samvega-parikittana-patha',
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'ต่อไปนี้สวด เสขิยวัตร เสขิยวัตรจัดเป็น 4 หมวด คือ หมวดที่ 1 เรียกว่า '
                    'จีวะระปะฏิสังยุต มี 26 สิกขาบท หมวดที่ 2 เรียกว่า ปิณฑะปาตะปะฏิสังยุต มี 30 '
                    'สิกขาบท หมวดที่ 3 เรียกว่า ธัมมะเทสะนาปะฏิสังยุต มี 16 สิกขาบท หมวดที่ 4 '
                    'เรียกว่า ปะกิณณะกะ มี 3 สิกขาบท หมวดที่ 1 ที่ 2 สวดวันละหมวด หมวดที่ 3 ที่ 4 '
                    'มีน้อยสิกขาบท สวดรวมกันในวันเดียว ตกลงสวด 3 วัน เวียนมาขึ้นหมวดต้นครั้งหนึ่ง '
                    'บทสวดจักเรียงไว้ต่อท้ายทำวัตรเช้า ในที่นี้พึงทราบระเบียบดังต่อไปนี้'
                ),
                'english': (
                    'Next the Sekhiyavatta are chanted. They are arranged in '
                    'four sections: the first, called Cīvara-paṭisaṃyutta, has '
                    '26 training rules; the second, Piṇḍapāta-paṭisaṃyutta, '
                    'has 30; the third, Dhammadesanā-paṭisaṃyutta, has 16; the '
                    'fourth, Pakiṇṇaka, has 3. The first and second are '
                    'chanted one section a day; the third and fourth, having '
                    'few rules, are chanted together on one day. So they are '
                    'chanted over three days and then come round to the first '
                    'section again. The passages are set out after the morning '
                    'service; here the order is to be understood as follows.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': 'เมื่อจะสวดเสขิยวัตรหมวดที่ 1 ประธานกล่าวเชิญว่า',
                'english': (
                    'When the first section of the Sekhiyavatta is to be '
                    'chanted, the leader gives the invitation:'
                ),
                'english_unverified': True,
            },
            {
                'type': 'invitation',
                'pali': 'หันทะ มะยัง ฉัพพีสะติ สารุปปาสิกขาโย ภะณามะ เส.',
            },
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้นบทว่า ปะริมัณฑะลัง นอกนั้นรับต่อพร้อมกันไป'
                    'หยุดตามจุดลูกน้ำ'
                ),
                'english': (
                    'The deputy leader begins the line parimaṇḍalaṃ, and the '
                    'rest join together, pausing at the commas.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': 'เมื่อจะสวดเสขิยวัตรหมวดที่ 2 ประธานกล่าวเชิญว่า',
                'english': (
                    'When the second section is to be chanted, the leader '
                    'gives the invitation:'
                ),
                'english_unverified': True,
            },
            {
                'type': 'invitation',
                'pali': (
                    'หันทะ มะยัง สะมะติงสะ โภชะนะปะฏิสังยุตตาสิกขาโย ภะณามะ เส.'
                ),
            },
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้นบทว่า สักกัจจัง นอกนั้นรับต่อพร้อมกันไป '
                    'หยุดตามจุดลูกน้ำ'
                ),
                'english': (
                    'The deputy leader begins the line sakkaccaṃ, and the rest '
                    'join together, pausing at the commas.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': 'เมื่อจะสวดเสขิยวัตร หมวดที่ 3-4 ควบกัน ประธานกล่าวเชิญว่า',
                'english': (
                    'When the third and fourth sections are to be chanted '
                    'together, the leader gives the invitation:'
                ),
                'english_unverified': True,
            },
            {
                'type': 'invitation',
                'pali': (
                    'หันทะ มะยัง โสฬะสะ ธัมมะเทสะนาปะฏิสังยุตตาสิกขาโย เจวะ ติสโส '
                    'ปะกิณณะกาสิกขาโย จะ ภะณามะ เส.'
                ),
            },
            {
                'type': 'prose',
                'thai': (
                    'รองประธานขึ้นต้นบทว่า นะ ฉัตตะปาณิสสะ นอกนั้นรับต่อพร้อมกันไป '
                    'หยุดตามจุดลูกน้ำ'
                ),
                'english': (
                    'The deputy leader begins the line na chattapāṇissa, and '
                    'the rest join together, pausing at the commas.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'ต่อจากเสขิยวัตรสวด พระสูตร หรือปาฐะ หรือคาถา ต่างๆ '
                    'ตามที่กำหนดไว้'
                ),
                'english': (
                    'After the Sekhiyavatta, a sutta, a passage or a set of '
                    'verses is chanted, according to what has been appointed'
                ),
                'english_unverified': True,
            },
        ],
    },

    # ── Page 6 ──────────────────────────────────────────────────────────
    # The top two thirds carry on the instruction from page 5 — the sentence
    # that ends page 5 is finished by the one that opens page 6 — and then the
    # printed title of ตังขะณิกะปัจจะเวกขะณะปาโฐ. Both runs are above the only
    # chant on the page, so neither is anchored.
    {
        'page': 6,
        'invitation_printed_here': ['tangkhanika-paccavekkhana-patho'],
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'วันละ 1 สูตร หรือ 1 ปาฐะ หรือ 1 คาถา ดังที่เรียงลำดับไว้ท้ายเสขิยวัตร '
                    'มี ทะสะธัมมะสุตตะ เป็นต้น จนถึงบทสุดท้ายแล้วเวียนมาสวด ทะสะธัมมะสุตตะ '
                    'ตั้งต้นไปใหม่อีก อนึ่งการสวดพระสูตรหรือปาฐะ หรือคาถานั้น บางครั้งสวดเป็น '
                    'ทำนองสังโยค บางครั้งสวดเป็น ทำนองมคธ สุดแต่ผู้เป็นประธานจะนำสวด '
                    'ทั้งนี้เพื่อให้พระภิกษุสามเณรชำนาญทำนองสวดทั้ง 2 อย่าง ตัวอย่างเมื่อจะสวด '
                    'ทะสะธัมมะสุตตะ เป็นทำนองสังโยค ประธานขึ้นต้นบทว่า เอวัมเม สุตัง นอกนั้นรับ '
                    'เอกังสะมะยัง ฯเปฯ พร้อมกันไป เมื่อจะสวดทำนองมคธ ประธานกล่าวเชิญว่า '
                    'หันทะ มะยัง ทะสะธัมมะสุตตัง ภะณามะ เส รองประธานขึ้นต้นบทว่า เอวัมเม สุตัง '
                    'นอกนั้นรับต่อพร้อมกันไป หยุดตามจุดลูกน้ำ แต่เมื่อจะสวดพระสูตรหรือปาฐะใด '
                    'ถ้ามีสวดบทขัดของพระสูตร หรือปาฐะนั้นแล้ว ประธานไม่ต้องกล่าวคำเชิญ คือ '
                    'หันทะ มะยัง นำขึ้นต้นบทของพระสูตรหรือปาฐะนั้น ๆ เลยทีเดียว'
                ),
                'english': (
                    'One sutta, one passage or one set of verses a day, in the '
                    'order set out after the Sekhiyavatta, beginning with the '
                    'Dasadhamma-sutta and running to the last, then coming '
                    'round to the Dasadhamma-sutta and starting again. '
                    'Further, a sutta, passage or verses may be chanted '
                    'sometimes in the saṃyoga manner and sometimes in the '
                    'Magadha manner, as the leader chooses, so that bhikkhus '
                    'and sāmaṇeras become practised in both. For example, when '
                    'the Dasadhamma-sutta is to be chanted in the saṃyoga '
                    'manner, the leader begins evaṃ me sutaṃ and the rest take '
                    'up ekaṃ samayaṃ and so on together. When it is to be '
                    'chanted in the Magadha manner, the leader gives the '
                    'invitation handa mayaṃ dasadhammasuttaṃ bhaṇāma se, the '
                    'deputy begins evaṃ me sutaṃ, and the rest join, pausing '
                    'at the commas. But where a sutta or passage has its own '
                    'preparatory verses, the leader does not give the handa '
                    'mayaṃ invitation, and simply begins that sutta or passage '
                    'directly.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'ต่อจากพระสูตร หรือปาฐะหรือคาถา สวด ตังขะณิกะปัจจะเวกขะณะปาฐะ '
                    'ประธานกล่าวเชิญว่า หันทะ มะยัง ตังขะณิกะปัจจะเวกขะณะปาฐัง ภะณามะ เส '
                    'รองประธานขึ้นต้นบทว่า ปะฏิสังขา นอกนั้นรับ โยนิโส ฯเปฯ พร้อมกันไป '
                    'หยุดตามจุดลูกน้ำดังนี้.'
                ),
                'english': (
                    'After the sutta, passage or verses, the '
                    'Tangkhanika-paccavekkhana-patha is chanted. The leader '
                    'gives the invitation handa mayaṃ '
                    'taṅkhaṇikapaccavekkhaṇapāṭhaṃ bhaṇāma se; the deputy '
                    'begins the line paṭisaṅkhā, and the rest take up yoniso '
                    'and so on together, pausing at the commas, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },

    # ── Page 7 ──────────────────────────────────────────────────────────
    # Printed between the end of ตังขะณิกะปัจจะเวกขะณะปาโฐ and the title of
    # ปัตติทานะคาถา. The page's footnote (๑. นัย ม. มู ๑๒/๑๓-๘) is NOT repeated
    # here — it is already on the chant as `source_printed` and renders in the
    # page's citation footnotes.
    {
        'page': 7,
        'after': 'tangkhanika-paccavekkhana-patho',
        # This paragraph contains ปัตติทานะคาถา's invitation, so the chant's
        # own invitation line is not shown again below its title.
        'invitation_printed_here': ['pattidana-gatha'],
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'ต่อจาก ตังขะณิกะปัจจะเวกขะณะปาฐะ สวด ปัตติทานะคาถา ซึ่งเป็น'
                    'บทแผ่ส่วนบุญ ประธานกล่าวเชิญว่า หันทะ มะยัง ปัตติทานะคาถาโย '
                    'ภะณามะ เส. รองประธานขึ้นต้นบทว่า ยา เทวะตา นอกนั้นรับ สันติ '
                    'วิหาระวาสินี ฯเปฯ พร้อมกันไป หยุดตามจุดลูกน้ำดังนี้.'
                ),
                'english': (
                    'After the Tangkhanika-paccavekkhana-patho, chant the '
                    'Pattidana-gatha, which is the passage for sharing merit. '
                    'The leader gives the invitation: handa mayaṃ '
                    'pattidāna-gāthāyo bhaṇāma se. The deputy begins the line '
                    'yā devatā, and the rest join with santi vihāravāsinī and '
                    'so on, together, pausing at the commas as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },

    # ── Page 8 ──────────────────────────────────────────────────────────
    # Below the end of ปัตติทานะคาถา: the closing of the whole morning service,
    # then the explanatory section, whose numbered items run on to page 9.
    {
        'page': 8,
        'after': 'pattidana-gatha',
        'blocks': [
            {
                'type': 'service_closing',
                'thai': 'จบพิธีทำวัตรเช้า',
                'english': 'Here ends the morning chanting service',
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'เมื่อสวดบท ปัตติทานะคาถา จบลงแล้ว พึงนั่งสงบแผ่ส่วนกุศลแด่ท่าน'
                    'บรรพบุรุษบุรพาจารย์ และท่านผู้มีพระคุณอื่น ๆ ตลอดถึงสรรพสัตว์ทุกชั้นชาติ '
                    'สักครู่หนึ่ง แล้วนั่งคุกเข่ากราบพระด้วยเบญจางคประดิษฐ์ ๓ หน พร้อม ๆ กัน '
                    'ประธานสั่งเลิกประชุม เป็นอันเสร็จพิธีทำวัตรสวดมนต์ภาคเช้าเท่านี้.'
                ),
                'english': (
                    'When the Pattidana-gatha has ended, sit quietly for a '
                    'short while and share the merit with forebears and '
                    'former teachers, with others to whom gratitude is owed, '
                    'and with all beings of every kind. Then kneel and bow to '
                    'the Buddha with the fivefold prostration three times, all '
                    'together. The leader closes the assembly, and the morning '
                    'chanting service is complete.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'heading',
                'thai': 'คำอธิบายประกอบทำวัตรเช้า',
                'english': 'Notes on the morning service',
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'พิธีทำวัตรเช้านี้ใช้ได้ทั้งภิกษุสามเณร ทั้งอุบาสกอุบาสิกา แต่มีถ้อยคำที่จะพึง'
                    'เปลี่ยน ให้ถูกต้องตามเพศภาวะของตน ๆ ดังนี้'
                ),
                'english': (
                    'This morning service may be used by bhikkhus and '
                    'sāmaṇeras and by laymen and laywomen alike, but there are '
                    'words that should be changed to suit one\'s own standing, '
                    'as follows.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'item',
                'number': 1,
                'thai': (
                    'ในบท สังเวคะปะริกิตตะนะปาฐะ คำว่า เต ในประโยคว่า เต มะยัง '
                    'โอติณณาม์หะ ชาติยา ชะรามะระเณนะ สำหรับภิกษุสามเณรและอุบาสก ถ้าอุบาสิกา'
                    'สวด ให้เปลี่ยนเป็น ตา เข้าประโยคว่า ตา มะยัง'
                ),
                'english': (
                    'In the Saṃvega-parikittana-patha, the word te in the '
                    'phrase te mayaṃ otiṇṇāmha jātiyā jarāmaraṇena is for '
                    'bhikkhus, sāmaṇeras and laymen. If a laywoman is '
                    'chanting, change it to tā, giving the phrase tā mayaṃ.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'item',
                'number': 2,
                'thai': (
                    'ตั้งแต่ประโยคว่า จิระปะรินิพพุตัมปิ ตัง ภะคะวันตัง อุททิสสะ อะระ'
                    'หันตัง สัมมาสัมพุทธัง ไปจนจบนั้น สำหรับภิกษุสามเณรสวด ถ้าเป็นอุบาสกอุบาสิกา '
                    'ให้เปลี่ยนเป็นดังนี้.'
                ),
                'english': (
                    'From the phrase ciraparinibbutampi taṃ bhagavantaṃ '
                    'uddissa arahantaṃ sammāsambuddhaṃ to the end is for '
                    'bhikkhus and sāmaṇeras to chant. For laymen and laywomen '
                    'it is changed as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    {
        'page': 8,
        'after': 'samvega-parikittana-patha-lay-variant',
        'blocks': [
            # NOT a citation, so it cannot live in `source_printed`. The book
            # numbers it 1 in Arabic while page 7's is ๑ in Thai — both are the
            # first footnote on their own page, and the numerals mean nothing
            # beyond that.
            {
                'type': 'footnote',
                'marker': '1',
                'thai': 'คะโต สำหรับอุบาสก ถ้าอุบาสิกา ใช้ คะตา',
                'english': (
                    'gato is for a layman; a laywoman uses gatā.'
                ),
                'english_unverified': True,
            },
        ],
    },

    # ── Page 9 ──────────────────────────────────────────────────────────
    # Roughly 60% of this page is instruction. Items 3-5 continue the list
    # begun on page 8 — the book's own numbering runs across the page turn,
    # so they keep the printed numbers rather than restarting at 1.
    {
        'page': 9,
        'blocks': [
            {
                'type': 'item',
                'number': 3,
                'thai': (
                    'บทว่า ภิกขูนัง สิกขาสาชีวะสะมาปันนา สำหรับภิกษุสวด ถ้าสามเณรร่วม'
                    'กับภิกษุ เมื่อถึงบทนี้ให้หยุดเสีย ถ้าสวดแต่ลำพังสามเณรให้เปลี่ยนเป็น '
                    'สามะเณรานัง สิกขาสาชีวะสะมาปันนา.'
                ),
                'english': (
                    'The line bhikkhūnaṃ sikkhāsājīvasamāpannā is for bhikkhus '
                    'to chant. If sāmaṇeras are chanting together with '
                    'bhikkhus, they stop when this line is reached. If '
                    'sāmaṇeras are chanting on their own, it is changed to '
                    'sāmaṇerānaṃ sikkhāsājīvasamāpannā.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'item',
                'number': 4,
                'thai': (
                    'ถ้ามีกรณียกิจที่จำเป็นซึ่งต้องทำภายหลังอยู่มาก ปรารถนาจะทำวัตรย่อ ให้สวด'
                    'เฉพาะ ระตะนัตตะยัปปะณามะคาถา คือตั้งแต่ พุทโธ สุสุทโธ กะรุณามะหัณณะโว '
                    'ถึง มา โหนตุ เว ตัสสะ ปะภาวะสิทธิยา และประธานกล่าวเชิญว่า หันทะ มะยัง '
                    'ระตะนัตตะยัปปะณามะคาถาโย ภะณามะ เส ไม่สวด สังเวคะปะริกิตตะนะปาฐะ '
                    'คือ อิธะ ตะถาคะโต ฯเปฯ ต่อไป'
                ),
                'english': (
                    'If there is much necessary business to be done '
                    'afterwards and a shortened service is wanted, chant only '
                    'the Ratanattayappanamagatha - that is, from buddho '
                    'susuddho karuṇāmahaṇṇavo as far as mā hontu ve tassa '
                    'pabhāvasiddhiyā - and the leader gives the invitation '
                    'handa mayaṃ ratanattayappaṇāmagāthāyo bhaṇāma se. The '
                    'Saṃvega-parikittana-patha, which begins idha tathāgato '
                    'and so on, is not chanted.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'item',
                'number': 5,
                'thai': (
                    'ถ้าเป็นวันธรรมสวนะ ประจำวันพระ หรือ วันอาทิตย์ ประธานกล่าวคำเชิญ'
                    'บูชาพระรัตนตรัยและสวดนะโม อย่างพิสดารดังนี้.'
                ),
                'english': (
                    'If it is a Dhamma-listening day - an observance day or a '
                    'Sunday - the leader gives the invitation to revere the '
                    'Triple Gem and chant the Namo in the elaborate form, as '
                    'follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    {
        'page': 9,
        'after': 'kham-choen-bucha-phitsadan',
        'blocks': [
            # The sentence is NOT complete on this page; it runs on to page 10,
            # and page 9 carries only what page 9 prints.
            {
                'type': 'prose',
                'thai': (
                    'คำว่า มะหาสุระสิงหะนาเทนะ ปะวะระราเชนะ ใช้เฉพาะในพระอุโบสถวัดมหาธาตุ '
                    'ด้วยพระประธาน สมเด็จกรมพระราชวังบวรมหาสุรสิงหนาทเป็นผู้ทรงสถาปนา'
                    'ประดิษฐานไว้ ถ้านำไปใช้ในที่อื่นๆก็ให้เปลี่ยนใช้ตามนามของผู้สร้างพระประธาน'
                ),
                'english': (
                    'The words mahāsurasīhanādena pavararājena are used only '
                    'in the ordination hall of Wat Mahathat, whose principal '
                    'Buddha image was established by Somdet Krom Phra '
                    'Rachawang Bowon Maha Surasinghanat. Used anywhere else, '
                    'they should be changed to the name of whoever established '
                    'that principal image'
                ),
                'english_unverified': True,
            },
        ],
    },
    # ── Page 10 ─────────────────────────────────────────────────────────
    # Almost all of this page is instruction rather than chant text. It OPENS
    # mid-sentence: the editorial note that begins at the foot of page 9
    # finishes here, and each page carries only the half printed on it — the
    # same rule page 9's group follows from the other side. Then item 6,
    # continuing the numbered list that runs 1-2 on page 8 and 3-5 on page 9.
    {
        'page': 10,
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'หรือใช้ศัพท์สาธารณะสามัญว่า มะหาชะเน พุทธะสาสะนิเกนะ ก็ได้ เมื่อเข้า'
                    'ประโยคแล้วเป็นดังนี้ อะยัง ปะฏิมา มะหาชะเนนะ พุทธะสาสะนิเกนะ ตัง '
                    'ภะคะวันตัง อุททิสสะ กะตา ปะติฏฐาปิตา.'
                ),
                'english': (
                    'Or the ordinary general expression mahājane '
                    'buddhasāsanikena may be used instead. Put into the '
                    'sentence it runs thus: ayaṃ paṭimā mahājanena '
                    'buddhasāsanikena taṃ bhagavantaṃ uddissa katā '
                    'patiṭṭhāpitā.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'item',
                'number': 6,
                'thai': (
                    'การทำวัตรเช้าวันธรรมสวนะ ไม่มีสวดมนต์ต่อท้าย มีระเบียบปฏิบัติดังนี้ '
                    'เมื่อได้เวลา 09.00 น. ตรง ประธานนำจุดธูปเทียน นำทำวัตรเช้าเหมือน'
                    'วันปกติทุกประการ จบลงเพียง ตัง โน พ์รัห์มะจะริยัง อิมัสสะ เกวะลัสสะ '
                    'ทุกขักขันธัสสะ อันตะกิริยายะ สังวัตตะตูติ ต่อจากนั้นสามเณรสวด'
                    'สามเณรานุสิกขาทั้ง 3 บท ไม่สวดบทขัด เมื่อสามเณรสวดสามเณรานุสิกขา'
                    'จบแล้ว อุบาสกอุบาสิกาทำวัตรเช้าจบลงที่ สังเวคะปะริกิตตะนะปาฐะ '
                    'เช่นเดียวกัน'
                ),
                'english': (
                    'The morning service on a Dhamma-hearing day has no '
                    'chanting appended after it, and is conducted thus. At '
                    'exactly 09.00 the leader lights the incense and candles '
                    'and leads the morning service just as on an ordinary day, '
                    'ending only at taṃ no brahmacariyaṃ imassa kevalassa '
                    'dukkhakkhandhassa antakiriyāya saṃvattatūti. After that '
                    'the sāmaṇeras chant the three Sāmaṇerānusikkhā passages, '
                    'without the preparatory verse. When the sāmaṇeras have '
                    'finished the Sāmaṇerānusikkhā, the laymen and laywomen '
                    'likewise end their morning service at the '
                    'Saṃvega-parikittana-patha.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'เมื่ออุบาสกอุบาสิกาทำวัตรเช้าจบลงแล้ว หัวหน้าอุบาสกนั่งคุกเข่าท่าพรหม'
                    'ประนมมือ ประกาศอุโบสถเป็นลำดับต่อไป ดังนี้.'
                ),
                'english': (
                    'When the laymen and laywomen have finished the morning '
                    'service, the leading layman kneels in the brahma posture '
                    'with palms joined and makes the announcement of the '
                    'Uposatha, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # The book sets this chant's translation as a passage under its own คำแปล
    # heading, so the heading is printed and belongs to the page. Only the
    # heading is kept here: the words under it are the chant's `thai` layer,
    # and repeating them as a prose block would print the translation twice.
    {
        'page': 10,
        'after': 'kham-prakat-ubosot',
        'blocks': [
            {
                'type': 'heading',
                'thai': 'คำแปล',
                'english': 'Translation',
                'english_unverified': True,
            },
        ],
    },
    # ── Page 11 ─────────────────────────────────────────────────────────
    # Both blocks sit above the only chant printed on this page, so the group
    # carries no `after`. What page 11 ALSO prints, and the app does not show
    # here, is the tail of the คำแปล begun on page 10 — that translation is
    # the `thai` layer of a chant whose Pali is all on page 10, so the app
    # shows the whole of it there. See the page-fidelity check on the chant.
    {
        'page': 11,
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'คำบาลีว่า ปัณณะระสี ทิวะโส และคำไทยว่า วันนี้เป็นวันปัณณรสีดิถีที่ 15 '
                    'นั้น สำหรับวัน 15 ค่ำ ถ้าเป็นวัน 14 ค่ำ ให้เปลี่ยนเป็น จาตุททะสี ทิวะโส '
                    'และคำไทยว่า วันนี้เป็นวันจาตุททสีดิถีที่ 14 ถ้าเป็นวัน 8 ค่ำ ให้เปลี่ยน'
                    'เป็น อัฏฐะมี ทิวะโส คำไทยว่า วันนี้เป็นวันอัฏฐมีดิถีที่ 8'
                ),
                'english': (
                    'The Pali paṇṇarasī divaso, and the Thai "today is the '
                    'fifteenth lunar day", are for the fifteenth day of the '
                    'fortnight. On a fourteenth day they are changed to '
                    'cātuddasī divaso, and the Thai to "today is the '
                    'fourteenth lunar day". On an eighth day they are changed '
                    'to aṭṭhamī divaso, and the Thai to "today is the eighth '
                    'lunar day".'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': (
                    'เมื่อหัวหน้าอุบาสกประกาศอุโบสถจวนจะจบ พระเถระผู้เป็นประธานที่จะแสดง'
                    'ธรรมขึ้นสู่ธรรมาสน์ เมื่อหัวหน้าอุบาสกประกาศอุโบสถจบลงแล้ว '
                    'อุบาสกอุบาสิกาทั้งนั้น อาราธนาอุโบสถศีลพร้อมกันดังนี้.'
                ),
                'english': (
                    "As the leading layman's announcement of the Uposatha "
                    'nears its end, the presiding elder who is to give the '
                    'Dhamma talk ascends the Dhamma seat. When the '
                    'announcement is finished, all the laymen and laywomen '
                    'together request the Uposatha precepts, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # ── Page 12 ─────────────────────────────────────────────────────────
    # The instruction that opens the page, above both chants on it.
    {
        'page': 12,
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'พระเถระที่จะแสดงธรรมตั้งพัดให้อุโบสถศีล อุบาสกอุบาสิกาตั้งใจสมาทาน '
                    'คือว่าตามพระโดยเคารพดังนี้'
                ),
                'english': (
                    'The elder who is to give the Dhamma talk sets up his fan '
                    'to give the Uposatha precepts. The laymen and laywomen '
                    'set their minds on undertaking them, repeating after the '
                    'monk respectfully, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # Between the two chants: the elder closes the refuge-going and the
    # assembly answers. Not part of either chant — it is the book telling the
    # room what happens between them.
    {
        'page': 12,
        'after': 'tisarana-gamana-ubosot',
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'พระเถระว่า ติสะระณะคะมะนัง นิฏฐิตัง. อุบาสกอุบาสิการับพร้อมกันว่า '
                    'อามะ ภันเต. พระเถระว่านำต่อไปดังนี้.'
                ),
                'english': (
                    'The elder says tisaraṇagamanaṃ niṭṭhitaṃ — \'the going '
                    'to the three refuges is completed\'. The laymen and '
                    'laywomen answer together āma bhante — \'yes, venerable '
                    'sir\'. The elder then leads on as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # The page's only footnote. It is a canonical citation, so it would
    # normally be `source_printed` on the chant — but ONE printed footnote
    # serves TWO markers here, one on the last refuge line and one on precept
    # 8, and `source_printed` attaches per chant. Setting it on both would
    # print the citation twice on a page that prints it once. So it is kept
    # as the page's own footnote, which is also how the book sets it: a rule,
    # then the marker, then the reference. No english: a reference is
    # reproduced, never translated or expanded.
    {
        'page': 12,
        'after': 'ubosot-sila',
        'blocks': [
            {
                'type': 'footnote',
                'marker': '1',
                'thai': 'ขุ.ขุ. 25/1-2',
                'english': '',
            },
        ],
    },
]


# ── The book itself: what is printed on its cover and title pages ──────────
#
# The words only. The cover carries the ม.ธ.ส. emblem — a stupa in rays over
# the temple's initials — which is an image and is not reproduced here; the
# photographs are on file and can be added once there is somewhere to put them.
#
# `revision` appears on the title page and the half-title but NOT on the cover,
# so it is kept separate rather than folded into the edition line.
BOOK = {
    'title_thai': 'สวดมนต์ ทำวัตร เช้า เย็น',
    'title_english': 'Chanting Book: Morning and Evening Service',
    'edition_thai': 'ฉบับวัดมหาธาตุ สหราชอาณาจักร',
    'edition_english': 'The Wat Mahathat United Kingdom edition',
    'revision_thai': 'ฉบับปรับปรุง',
    'revision_english': 'Revised edition',
    'emblem_initials': 'ม.ธ.ส.',
    'english_unverified': True,
}


# ── Front matter — the pages before page 1 ─────────────────────────────────
#
# These are numbered in their OWN sequence, in Thai numerals inside brackets:
# (๓๕), (๓๖), (๓๗). The body has its own page 36, and the two are different
# pages of the same book. So front matter is never mixed into `page`, and the
# reading view reaches it by a separate route — a reader who types 36 gets the
# body's page 36, which is what a monk calling out a number means.
#
# `number` is the front-matter page as an integer, for ordering and routing.
# `printed` is exactly what the page shows, or None where the page carries no
# number at all — which the opening pages do not.
FRONT_MATTER = [
    {'number': None, 'printed': None, 'kind': 'cover', 'file': 'IMG_0250.PNG'},
    {'number': None, 'printed': None, 'kind': 'title', 'file': 'IMG_0251.PNG'},
    {'number': None, 'printed': None, 'kind': 'half_title', 'file': 'IMG_0263.PNG'},
    # ‼ CHECK [IMG_0252.PNG]: the first สารบัญ page prints NO number. The pages
    #   after it run (๓๖)…(๔๔), so this is almost certainly (๓๕) — but almost
    #   certainly is not printed, so `printed` stays None and the number is
    #   inferred only for ordering. Worth a glance at the physical book.
    {'number': 35, 'printed': None, 'kind': 'contents', 'file': 'IMG_0252.PNG'},
    {'number': 36, 'printed': '(๓๖)', 'kind': 'contents', 'file': 'IMG_0253.PNG'},
    {'number': 37, 'printed': '(๓๗)', 'kind': 'contents', 'file': 'IMG_0254.PNG'},
    {'number': 38, 'printed': '(๓๘)', 'kind': 'contents', 'file': 'IMG_0256.PNG'},
    {'number': 39, 'printed': '(๓๙)', 'kind': 'contents', 'file': 'IMG_0257.PNG'},
    {'number': 40, 'printed': '(๔๐)', 'kind': 'contents', 'file': 'IMG_0258.PNG'},
    {'number': 41, 'printed': '(๔๑)', 'kind': 'contents', 'file': 'IMG_0259.PNG'},
    {'number': 42, 'printed': '(๔๒)', 'kind': 'contents', 'file': 'IMG_0260.PNG'},
    {'number': 43, 'printed': '(๔๓)', 'kind': 'contents', 'file': 'IMG_0261.PNG'},
    {'number': 44, 'printed': '(๔๔)', 'kind': 'contents', 'file': 'IMG_0262.PNG'},
]


# ── The contents (สารบัญ), as the book prints it ───────────────────────────
#
# One row per printed line, in printed order. `level` is 'section' for the bold
# headings the book sets flush left and 'entry' for the titles indented under
# them — that is the only distinction the page makes, and it is enough to set
# the page the way the book sets it.
#
# `page` is the BODY page the line points at, as an integer, so the app can turn
# it into a link. `page_printed` is the Thai numeral the book actually shows, and
# it is what a reader sees — the integer exists to be followed, not read.
#
# `front_page` is which front-matter page the line is printed on, so a page of
# the contents can be rendered as its own page rather than as one long list.
#
# This is the most useful single table in the book: it names every chant across
# all 325 pages and where each one is. Entries whose page is not in the app yet
# render as plain text rather than links, which makes the contents an honest map
# of how much of the book has been entered.
#
# Held as tuples — (front-matter page, level, title, page as printed) — because
# 301 rows of five-key dicts is a wall nobody proof-reads, and proof-reading is
# the only check there is on a hand-transcribed index.
#
# The page is stored ONLY as the Thai numeral the book prints. The integer the
# app links on is derived from it below, so the two cannot drift. An earlier
# draft carried both by hand, which across three hundred rows is a disagreement
# waiting to happen.
_CONTENTS_LINES = [

    # ── front-matter page 35 ──
    (35, 'section', 'ทำวัตรเช้า', '๑'),
    (35, 'entry', 'คำบูชาพระรัตนตรัย', '๑'),
    (35, 'entry', 'คำนมัสการพระรัตนตรัย', '๑'),
    (35, 'entry', 'คำเชิญบูชาและสวดนะโม', '๒'),
    (35, 'entry', 'ระตะนัตตะยัปปะณามะคาถา', '๓'),
    (35, 'entry', 'สังเวคะปะริกิตตะนะปาฐะ', '๔'),
    (35, 'entry', 'ตังขะณิกะปัจจะเวกขะณะปาโฐ', '๖'),
    (35, 'entry', 'คำอธิบายประกอบทำวัตรเช้า', '๘'),
    (35, 'entry', 'คำประกาศอุโบสถ', '๑๐'),
    (35, 'entry', 'คำอาราธนาอุโบสถศีล', '๑๑'),
    (35, 'entry', 'อุโบสถศีล', '๑๒'),
    (35, 'entry', 'สะระณะคะมะนานุสสะระณะคาถา', '๑๓'),
    (35, 'entry', 'คำขอขมาพระรัตนตรัย', '๑๔'),
    (35, 'section', 'เสขิยวัตร', '๑๕'),
    (35, 'entry', 'สารุปปะ ๒๖ สิกขาบท', '๑๕'),
    (35, 'entry', 'โภชชะนะปะฏิสังยุต ๓๐ สิกขาบท', '๑๖'),
    (35, 'entry', 'ธัมมะเทสะนาปะฏิสังยุต ๑๖ สิกขาบท', '๑๗'),
    (35, 'entry', 'ปะกิณณะกะ ๓ สิกขาบท', '๑๘'),
    (35, 'section', 'พระสูตร ปาฐะ และคาถาที่กำหนดสวดในภาคเช้า', '๑๙'),
    (35, 'entry', 'ทะสะธัมมะสุตตัง', '๑๙'),
    (35, 'entry', 'ปะริตตะกะระณะปาโฐ', '๒๐'),
    (35, 'entry', 'เมตตานิสังสะสุตตัง', '๒๒'),
    (35, 'entry', 'เมตตานิสังสะคาถา', '๒๓'),
    (35, 'entry', 'นิธิกัณฑะคาถา', '๒๔'),
    (35, 'entry', 'ธัมมะคาระวาทิคาถา', '๒๕'),
    (35, 'entry', 'เทวะตาทิสสะทักขิณานุโมทะนาคาถา', '๒๖'),
    (35, 'entry', 'เทวะตาภิสัมมันตะนะคาถา', '๒๗'),
    (35, 'entry', 'ติลักขะณาทิคาถา', '๒๗'),
    (35, 'entry', 'เขมาเขมะสะระณะคะมะนะปะริทีปิกาคาถา', '๒๘'),

    # ── front-matter page 36 ──
    (36, 'entry', 'วิหาระทานะคาถา', '๒๙'),
    (36, 'entry', 'สัจจะปานะวิธ์ยานุรูปะคาถา', '๒๙'),
    (36, 'entry', 'อาทิยะสุตตะคาถา', '๓๐'),
    (36, 'entry', 'ปัพพะโตปะมะคาถา', '๓๐'),
    (36, 'entry', 'อริยะธะนะคาถา', '๓๑'),
    (36, 'entry', 'ปะฏิจจะสะมุปปาทะปาโฐ', '๓๑'),
    (36, 'entry', 'พุทธะอุทานะคาถา', '๓๒'),
    (36, 'entry', 'ภัทเทกะรัตตะคาถา', '๓๓'),
    (36, 'entry', 'มะหากัสสะปะโพชฌังคะสุตตัง', '๓๓'),
    (36, 'entry', 'มะหาโมคคัลลานะโพชฌังคะสุตตัง', '๓๔'),
    (36, 'entry', 'มะหาจุนทะโพชฌังคะสุตตัง', '๓๖'),
    (36, 'section', 'สวดแจง', '๓๘'),
    (36, 'entry', 'พระวินัยสังเขป', '๓๘'),
    (36, 'entry', 'พระสูตรสังเขป', '๓๙'),
    (36, 'section', 'พระอภิธรรมสังเขป', '๓๙'),
    (36, 'entry', 'พระสังคะณี', '๓๙'),
    (36, 'entry', 'พระวิภังค์', '๔๐'),
    (36, 'entry', 'พระธาตุกะถา', '๔๐'),
    (36, 'entry', 'พระปุคคะละบัญญัติ', '๔๐'),
    (36, 'entry', 'พระกะถาวัตถุ', '๔๐'),
    (36, 'entry', 'พระยะมะกะ', '๔๑'),
    (36, 'entry', 'พระมะหาปัฏฐาน', '๔๑'),
    (36, 'entry', 'ธัมมะสังคะณีมาติกาปาโฐ', '๔๑'),
    (36, 'entry', 'วิปัสสะนาภูมิปาโฐ', '๔๒'),
    (36, 'entry', 'ถวายพรพระ', '๔๔'),
    (36, 'entry', 'ชะยะมังคะลัฏฐะกะคาถา', '๔๔'),
    (36, 'entry', 'ชะยะปะริตตะคาถา', '๔๖'),
    (36, 'entry', 'มงคลจักรวาฬน้อย', '๔๖'),
    (36, 'entry', 'กาละทานะสุตตะคาถา', '๔๗'),
    (36, 'entry', 'สังคะหะวัตถุคาถา', '๔๘'),
    (36, 'entry', 'โมกขุปายะคาถา', '๔๘'),

    # ── front-matter page 37 ──
    (37, 'entry', 'ระตะนัตตะยัปปะภาวะสิทธิคาถา', '๔๙'),
    (37, 'section', 'ทำวัตรเย็น', '๕๑'),
    (37, 'entry', 'ระเบียบทำวัตรสวดมนต์ ภาคเย็น', '๕๑'),
    (37, 'entry', 'คาถาบูชาพระรัตนตรัย', '๕๑'),
    (37, 'entry', 'คำนมัสการพระรัตนตรัย', '๕๑'),
    (37, 'entry', 'คำเชิญบูชาสวดนะโม และพระพุทธคุณ', '๕๑'),
    (37, 'entry', 'พุทธะมังคะละคาถา', '๕๕'),
    (37, 'entry', 'สีลุทเทสะปาโฐ', '๕๖'),
    (37, 'entry', 'บทขัดสิกขาบท ๑๐', '๕๗'),
    (37, 'entry', 'สิกขาบท ๑๐', '๕๗'),
    (37, 'entry', 'บทขัดนาสะนังคะ', '๕๘'),
    (37, 'entry', 'นาสะนังคะ ๑๐ สิกขาบท', '๕๘'),
    (37, 'entry', 'บทขัดทัณฑะกรรม', '๕๙'),
    (37, 'entry', 'ทัณฑะกรรม ๕ สิกขาบท', '๕๙'),
    (37, 'entry', 'อะตีตะปัจจะเวกขะณะปาโฐ', '๖๐'),
    (37, 'entry', 'ธาตุปะฏิกูละปัจจะเวกขะณะปาโฐ', '๖๑'),
    (37, 'entry', 'อุทิสสะนาธิฏฐานะคาถา', '๖๒'),
    (37, 'entry', 'คำอธิบายประกอบทำวัตรเย็น', '๖๒'),
    (37, 'entry', 'คำเชิญบูชาพระรัตนตรัยพิเศษ', '๖๔'),
    (37, 'entry', 'คาถาอาราธนาธรรม', '๖๕'),
    (37, 'entry', 'คำถวายดอกไม้ ธูป เทียน ในวันวิสาขบูชา', '๖๖'),
    (37, 'entry', 'สะระภัญญะคาถา สำหรับสวดในวันวิสาขบูชา', '๖๗'),
    (37, 'entry', 'คำถวายดอกไม้ ธูป เทียน ในวันอัฏฐมีบูชา', '๖๘'),
    (37, 'entry', 'สะระภัญญะคาถา สำหรับสวดในวันอัฏฐมีบูชา', '๖๙'),
    (37, 'entry', 'คำถวายดอกไม้ ธูป เทียน ในวันมาฆบูชา', '๗๑'),
    (37, 'entry', 'สะระภัญญะคาถา สำหรับสวดในวันมาฆบูชา', '๗๑'),
    (37, 'entry', 'บทขัดโอวาทะปาติโมกขาทิปาฐะ', '๗๒'),
    (37, 'entry', 'โอวาทะปาติโมกขาทิปาโฐ', '๗๓'),
    (37, 'entry', 'คำถวายดอกไม้ ธูป เทียน ในวันอาสาฬหบูชา', '๗๕'),
    (37, 'section', 'พระสูตร พระปริตร ปาฐะ และคาถาที่กำหนดสวดในภาคเย็น', '๗๗'),
    (37, 'entry', 'บทขัดชุมนุมเทวดา', '๗๗'),

    # ── front-matter page 38 ──
    (38, 'entry', 'ปุพพะภาคะนะมะการะปาโฐ', '๗๗'),
    (38, 'entry', 'สะระณะคะมะนะปาโฐ', '๗๗'),
    (38, 'entry', 'นะมะการะสิทธิคาถา', '๗๘'),
    (38, 'entry', 'นะโมการะอัฏฐะกะคาถา', '๗๙'),
    (38, 'entry', 'บทขัดต้นตำนาน', '๘๐'),
    (38, 'entry', 'บทขัดมังคะละสุตตัง', '๘๐'),
    (38, 'entry', 'มังคะละสุตตัง ปะฐะมัง', '๘๑'),
    (38, 'entry', 'บทขัดระตะนะสุตตัง', '๘๒'),
    (38, 'entry', 'ระตะนะสุตตัง ทุติยัง', '๘๒'),
    (38, 'entry', 'บทขัดกะระณียะเมตตะสุตตัง', '๘๖'),
    (38, 'entry', 'กะระณียะเมตตะสุตตัง ตะติยัง', '๘๖'),
    (38, 'entry', 'บทขัดขันธะปะริตตัง ฉัททันตะปะริตัง', '๘๗'),
    (38, 'entry', 'ขันธะปะริตตัง จะตุตถัง', '๘๗'),
    (38, 'entry', 'ฉัททันตะปะริตตัง', '๘๘'),
    (38, 'entry', 'บทขัดโมระปะริตตัง', '๘๘'),
    (38, 'entry', 'โมระปะริตตัง ปัญจะมัง', '๘๘'),
    (38, 'entry', 'บทขัดวัฏฏะกะปะริตตัง', '๘๙'),
    (38, 'entry', 'วัฏฏะกะปะริตตัง ฉัฏฐัง', '๘๙'),
    (38, 'entry', 'บทขัดธะชัคคะสุตตัง', '๙๐'),
    (38, 'entry', 'ธะชัคคะปะริตตัง ธะชัคคะสุตตัง สัตตะมัง', '๙๐'),
    (38, 'entry', 'บทขัดอาฏานาฏิยะปะริตตัง', '๙๒'),
    (38, 'entry', 'อาฏานาฏิยะปะริตตัง อัฏฐะมัง', '๙๒'),
    (38, 'entry', 'บทขัดอังคุลิมาละปะริตตัง', '๙๖'),
    (38, 'entry', 'อังคุลิมาละปะริตตัง นะวะมัง', '๙๖'),
    (38, 'entry', 'บทขัดโพชฌังคะปะริตตัง', '๙๗'),
    (38, 'entry', 'โพชฌังคะปะริตตัง ทะสะมัง', '๙๗'),
    (38, 'entry', 'บทขัดอะภะยะปะริตตัง', '๙๘'),
    (38, 'entry', 'อะภะยะปะริตตัง เอกาทะสะมัง', '๙๘'),
    (38, 'entry', 'เทวะตาอุยโยชะนะคาถา', '๙๘'),
    (38, 'entry', 'บทขัดชะยะปะริตตัง', '๙๙'),
    (38, 'entry', 'ชะยะปะริตตัง ท์วาทะสะมัง', '๙๙'),

    # ── front-matter page 39 ──
    (39, 'entry', 'ระตะนัตตะยัปปะภาวาภิยาจะนะคาถา', '๑๐๐'),
    (39, 'entry', 'สุขาภิยาจะนะคาถา', '๑๐๑'),
    (39, 'entry', 'มงคลจักรวาฬใหญ่', '๑๐๒'),
    (39, 'entry', 'บทขัดทะสะนาถะกะระณะธัมมะสุตตัง', '๑๐๓'),
    (39, 'entry', 'ทะสะนาถะกะระณะธัมมะสุตตัง', '๑๐๓'),
    (39, 'entry', 'บทขัดอะภิณ์หะปัจจะเวกขะณะปาฐะ', '๑๐๖'),
    (39, 'entry', 'อะภิณ์หะปัจจะเวกขะณะปาโฐ', '๑๐๖'),
    (39, 'entry', 'บทขัดมัคคะวิภังคะสุตตัง', '๑๐๗'),
    (39, 'entry', 'มัคคะวิภังคะสุตตัง', '๑๐๘'),
    (39, 'entry', 'อัฏฐังคิกะมัคคะคาถา', '๑๑๐'),
    (39, 'entry', 'บทขัดกะระณียากะระณียะสุตตัง', '๑๑๑'),
    (39, 'entry', 'กะระณียากะระณียะสุตตัง', '๑๑๑'),
    (39, 'entry', 'บทขัดอัคคัปปะสาทะสุตตัง', '๑๑๒'),
    (39, 'entry', 'อัคคัปปะสาทะสุตตัง', '๑๑๒'),
    (39, 'entry', 'บทขัดฉะสาราณียะธัมมะสุตตัง', '๑๑๔'),
    (39, 'entry', 'ฉะสาราณียะธัมมะสุตตัง', '๑๑๔'),
    (39, 'entry', 'บทขัดภิกขุอะปะริหานิยะธัมมะสุตตัง', '๑๑๕'),
    (39, 'entry', 'ภิกขุอะปะริหานิยะธัมมะสุตตัง', '๑๑๖'),
    (39, 'entry', 'บทขัดปะหานะภาวะนาสุตตัง', '๑๑๗'),
    (39, 'entry', 'ปะหานะภาวะนาสุตตัง', '๑๑๗'),
    (39, 'entry', 'บทขัดจะตุรัปปะมัญญาปาฐะ', '๑๑๘'),
    (39, 'entry', 'จะตุรัปปะมัญญาปาโฐ', '๑๑๘'),
    (39, 'entry', 'บทขัดธัมมะนิยามะสุตตัง', '๑๑๙'),
    (39, 'entry', 'ธัมมะนิยามะสุตตัง', '๑๑๙'),
    (39, 'entry', 'บทขัดอะนัตตะลักขะณะสุตตัง', '๑๒๐'),
    (39, 'entry', 'อะนัตตะลักขะณะสุตตัง', '๑๒๑'),
    (39, 'entry', 'บทขัดอาทิตตะปะริยายะสุตตัง', '๑๒๔'),
    (39, 'entry', 'อาทิตตะปะริยายะสุตตัง', '๑๒๔'),
    (39, 'entry', 'บทขัดสะติปัฏฐานะปาฐะ', '๑๒๖'),
    (39, 'entry', 'สะติปัฏฐานะปาโฐ', '๑๒๗'),
    (39, 'entry', 'มะหาสะติปัฏฐานะสุตตะปาโฐ', '๑๒๘'),

    # ── front-matter page 40 ──
    (40, 'section', 'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันโกน วันพระ เวลาเย็น', '๑๕๙'),
    (40, 'entry', 'บทขัดธัมมะจักกัปปะวัตตะนะสุตตัง', '๑๕๙'),
    (40, 'entry', 'ธัมมะจักกัปปะวัตตะนะสุตตัง', '๑๕๙'),
    (40, 'section', 'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันขึ้นหรือแรม ๘ ค่ำ เวลาเย็น', '๑๖๔'),
    (40, 'entry', 'บทขัดชุมนุมเทวดา', '๑๖๔'),
    (40, 'entry', 'ปุพพะภาคะมะนะการะปาโฐ', '๑๖๔'),
    (40, 'entry', 'สะระณะคะมะนะปาโฐ', '๑๖๔'),
    (40, 'entry', 'นะมะการะสิทธิคาถา', '๑๖๕'),
    (40, 'entry', 'นะโมการะอัฏฐะกะคาถา', '๑๖๖'),
    (40, 'entry', 'มังคะละสุตตัง', '๑๖๖'),
    (40, 'entry', 'ระตะนะสุตตัง', '๑๖๗'),
    (40, 'entry', 'กะระณียะเมตตะสุตตัง', '๑๖๙'),
    (40, 'entry', 'ขันธะปะริตตัง', '๑๖๙'),
    (40, 'entry', 'ธะชัคคะปะริตตัง (แบบย่อ)', '๑๖๙'),
    (40, 'entry', 'อาฏานาฏิยะปะริตตัง', '๑๗๐'),
    (40, 'entry', 'อังคุลิมาละปะริตตัง', '๑๗๑'),
    (40, 'entry', 'โพชฌังคะปะริตตัง', '๑๗๑'),
    (40, 'entry', 'อะภะยะปะริตตัง', '๑๗๒'),
    (40, 'entry', 'เทวะตาอุยโยชะนะคาถา', '๑๗๒'),
    (40, 'entry', 'ชะยะปะริตตัง', '๑๗๒'),
    (40, 'section', 'พระสูตรที่กำหนดสวดในวันขึ้น ๑๔ ค่ำ เวลาเย็น', '๑๗๕'),
    (40, 'entry', 'บทขัดมะหาสะมะยะสุตตัง', '๑๗๕'),
    (40, 'entry', 'มะหาสะมะยะสุตตัง', '๑๗๕'),
    (40, 'section', 'พระสูตรที่กำหนดสวดในวันแรม ๗ ค่ำ เวลาเย็น', '๑๘๓'),
    (40, 'entry', 'คิริมานันทะสุตตัง', '๑๘๓'),
    (40, 'section', 'พระสูตรที่กำหนดสวดในวันแรม ๑๓ ค่ำหรือ ๑๔ ค่ำ เวลาเย็น', '๑๘๗'),
    (40, 'entry', 'บทขัดโลกะธัมมะสุตตัง', '๑๘๗'),
    (40, 'entry', 'โลกะธัมมะสุตตัง', '๑๘๗'),
    (40, 'section', 'บทสวดมนต์ ทำวัตรเช้า-เย็น แปล', '๑๙๑'),
    (40, 'entry', 'ทำวัตรเช้า แปล', '๑๙๓'),
    (40, 'entry', 'คำบูชาพระรัตนตรัย', '๑๙๓'),

    # ── front-matter page 41 ──
    (41, 'entry', 'ปุพพะภาคะนะมะการ', '๑๙๕'),
    (41, 'entry', 'พุทธาภิถุติ', '๑๙๕'),
    (41, 'entry', 'ธัมมาภิถุติ', '๑๙๖'),
    (41, 'entry', 'สังฆาภิถุติ', '๑๙๗'),
    (41, 'entry', 'ระตะนัตตะยัปปะณามะคาถา', '๑๙๘'),
    (41, 'entry', 'พุทธชัยมงคลคาถา (ถวายพรพระ)', '๒๐๓'),
    (41, 'entry', 'ตังขะณิกะปัจจะเวกขะณะปาโฐ', '๒๐๕'),
    (41, 'entry', 'ธาตุปะฏิกูละปัจจะเวกขะณะปาโฐ', '๒๐๗'),
    (41, 'entry', 'ปัตติทานะคาถา', '๒๑๐'),
    (41, 'entry', 'สัพพะปัตติทานะคาถา', '๒๑๒'),
    (41, 'entry', 'ปัฏฐะนะฐะปะนะคาถา', '๒๑๓'),
    (41, 'entry', 'เขมาเขมะสะระณะทีปิกะคาถา', '๒๑๕'),
    (41, 'entry', 'อะภิณหะปัจจะเวกขะณะ ๕', '๒๑๖'),
    (41, 'entry', 'ท์วัตติงสาการะปาโฐ', '๒๑๗'),
    (41, 'entry', 'ภาระสุตตะคาถา', '๒๑๘'),
    (41, 'entry', 'คาถาโพธิบาท', '๒๑๙'),
    (41, 'entry', 'คาถามงคลจักรวาฬแปดทิศ', '๒๑๙'),
    (41, 'entry', 'ติโลกะวิชะยะราชะปัตติทานะคาถา', '๒๒๐'),
    (41, 'entry', 'คำแผ่เมตตาให้แก่ตนเอง', '๒๒๑'),
    (41, 'entry', 'คำแผ่เมตตาให้ผู้อื่น', '๒๒๑'),
    (41, 'entry', 'บทพิจารณาสังขาร', '๒๒๒'),
    (41, 'entry', 'อะภิณหะปัจจะเวกขะณะ', '๒๒๓'),
    (41, 'entry', 'ทำวัตรเย็นแปล', '๒๒๔'),
    (41, 'entry', 'คำบูชาพระรัตนตรัย', '๒๒๔'),
    (41, 'entry', 'ปุพพะภาคะนะมะการ', '๒๒๕'),
    (41, 'entry', 'พุทธานุสสะติ', '๒๒๖'),
    (41, 'entry', 'พุทธาภิคีติ', '๒๒๖'),
    (41, 'entry', 'ธัมมานุสสะติ', '๒๒๘'),
    (41, 'entry', 'ธัมมาภิคีติ', '๒๒๙'),
    (41, 'entry', 'สังฆานุสสะติ', '๒๓๑'),
    (41, 'entry', 'สังฆาภิคีติ', '๒๓๒'),

    # ── front-matter page 42 ──
    (42, 'entry', 'อะตีตะปัจจะเวกขะณะปาโฐ', '๒๓๔'),
    (42, 'entry', 'นมัสการพระอรหันต์ ๘ ทิศ', '๒๓๖'),
    (42, 'entry', 'อุณ์หิสสะวิชะยะคาถา', '๒๓๗'),
    (42, 'entry', 'พระคาถาชินบัญชร', '๒๓๗'),
    (42, 'entry', 'อุทิสสะนาธิฏฐานะคาถา', '๒๓๙'),
    (42, 'entry', 'ยอดพระกัณฑ์ไตรปิฎก', '๒๔๑'),
    (42, 'section', 'ภาคปกิณกะ', '๒๔๗'),
    (42, 'entry', 'คำอาราธนาศีล ๕ ปรกติ', '๒๔๙'),
    (42, 'entry', 'คำอาราธนาศีล ๕ พิเศษ คือ นิจศีล', '๒๔๙'),
    (42, 'entry', 'คำอาราธนาศีล ๘ ปรกติ', '๒๔๙'),
    (42, 'entry', 'คำอาราธนาศีล ๘ พิเศษ คืออุโบสถศีล', '๒๕๐'),
    (42, 'entry', 'คำอาราธนาสวดพระปริตร', '๒๕๐'),
    (42, 'entry', 'คำอาราธนาแสดงธรรม', '๒๕๐'),
    (42, 'entry', 'คำอาราธนาแสดงธรรมอย่างพิสดาร', '๒๕๐'),
    (42, 'entry', 'คำบังสุกุลศพหรืออัฐิ', '๒๕๒'),
    (42, 'entry', 'คำบังสุกุลคนเป็น', '๒๕๒'),
    (42, 'entry', 'คำขอขมาโทษพระรัตนตรัย', '๒๕๒'),
    (42, 'entry', 'คำขอขมาโทษแด่พระมหาเถระ', '๒๕๓'),
    (42, 'entry', 'คำรับขมาโทษของพระมหาเถระ', '๒๕๓'),
    (42, 'entry', 'คำอนุโมทนาของพระมหาเถระ', '๒๕๓'),
    (42, 'entry', 'คาถาจุดเทียนชัย', '๒๕๔'),
    (42, 'entry', 'คาถาดับเทียนชัย', '๒๕๔'),
    (42, 'entry', 'อธิบายระเบียบสวดมนต์ในพิธีต่าง ๆ', '๒๕๖'),
    (42, 'entry', 'ระเบียบสวดมนต์งานพิธีมงคล', '๒๕๖'),
    (42, 'entry', 'ระเบียบสวดมนต์งานพิธีมงคลอื่น ๆ', '๒๕๘'),
    (42, 'entry', 'ระเบียบสวดเจ็ดตำนานอย่างเต็มที่', '๒๕๙'),
    (42, 'entry', 'ระเบียบสวดเจ็ดตำนานอย่างปานกลาง', '๒๖๑'),
    (42, 'entry', 'ระเบียบสวดเจ็ดตำนานอย่างย่อ', '๒๖๑'),
    (42, 'entry', 'ระเบียบสวดถวายพรพระก่อนฉัน', '๒๖๔'),
    (42, 'entry', 'ระเบียบสวดในงานพิธีอวมงคล', '๒๖๔'),
    (42, 'entry', 'อธิบายระเบียบสวดมนต์พิเศษ', '๒๖๖'),

    # ── front-matter page 43 ──
    (43, 'entry', 'ระเบียบสวดมนต์นพเคราะห์', '๒๖๘'),
    (43, 'entry', 'ระเบียบถวายพรพระ', '๒๗๐'),
    (43, 'entry', 'ระเบียบอนุโมทนา', '๒๗๑'),
    (43, 'entry', 'อนุโมทนาวิธี', '๒๗๒'),
    (43, 'entry', 'มงคลจักรวาฬน้อย (ย่อ)', '๒๗๒'),
    (43, 'entry', 'อัคคัปปะสาทะสุตตะคาถา', '๒๗๓'),
    (43, 'entry', 'ติโรกุฑฑะกัณฑะปัจฉิมภาค', '๒๗๓'),
    (43, 'entry', 'โภชะนะทานุโมทะนาคาถา', '๒๗๓'),
    (43, 'entry', 'อาฏานาฏิยะปะริตตัง (ย่อ)', '๒๗๔'),
    (43, 'entry', 'ระเบียบบังสุกุล', '๒๗๔'),
    (43, 'entry', 'คาถาศราทธพรต', '๒๗๕'),
    (43, 'entry', 'คำอธิบายประกอบ', '๒๗๖'),
    (43, 'section', 'ภาคผนวก', '๒๗๗'),
    (43, 'entry', 'วิธีบรรพชาอุปสมบทแบบอุกาสะ', '๒๗๙'),
    (43, 'entry', 'วิธีบรรพชาอุปสมบทแบบเอสาหัง', '๒๘๔'),
    (43, 'entry', 'คำขอบรรพชานาคคู่', '๒๘๙'),
    (43, 'entry', 'คำขอนิสสัยนาคคู่', '๒๙๐'),
    (43, 'entry', 'คำขออุปสมบทพร้อมกัน', '๒๙๐'),
    (43, 'entry', 'คำบอกอนุศาสน์', '๒๙๐'),
    (43, 'entry', 'แบบสวดกรรมวาจาในอุปสมบทกรรม สำหรับนาคเดี่ยว', '๒๙๓'),
    (43, 'entry', 'คำสมมติตนเพื่อสอนซ้อม', '๒๙๓'),
    (43, 'entry', 'คำสอนซ้อม', '๒๙๓'),
    (43, 'entry', 'คำเรียกอุปสัมปทาเปกขะเข้ามา', '๒๙๔'),
    (43, 'entry', 'คำพระอุปัชฌายะกล่าวเผดียงสงฆ์', '๒๙๔'),
    (43, 'entry', 'คำสมมติตนเพื่อถามอันตรายิกธรรม', '๒๙๕'),
    (43, 'entry', 'คำถามอันตรายิกธรรม', '๒๙๕'),
    (43, 'entry', 'กรรมวาจาอุปสมบท', '๒๙๕'),
    (43, 'entry', 'คำสวดสมมติและคำสอนซ้อม (นาคคู่)', '๒๙๖'),
    (43, 'entry', 'คำขอเรียกอุปสัมปทาเปกขะเข้ามา', '๒๙๗'),
    (43, 'entry', 'คำสมมติตนและคำถามอันตรายิกธรรม', '๒๙๗'),
    (43, 'entry', 'คำพระอุปัชฌาย์กล่าวเผดียงสงฆ์', '๒๙๗'),

    # ── front-matter page 44 ──
    (44, 'entry', 'คำสวดกรรมวาจาอุปสมบท', '๒๙๗'),
    (44, 'entry', 'คำขอบวชชี', '๒๙๙'),
    (44, 'entry', 'คำอาราธนาศีล ๘', '๒๙๙'),
    (44, 'entry', 'คำนมัสการพระพุทธเจ้า', '๓๐๐'),
    (44, 'entry', 'คำสมาทานศีล', '๓๐๑'),
    (44, 'entry', 'วิธีแสดงอาบัติ', '๓๐๒'),
    (44, 'entry', 'คำพินทุผ้า', '๓๐๒'),
    (44, 'entry', 'คำอธิษฐาน', '๓๐๒'),
    (44, 'entry', 'คำเสียสละ', '๓๐๒'),
    (44, 'entry', 'คำคืน', '๓๐๒'),
    (44, 'entry', 'คำวิกัปป์', '๓๐๒'),
    (44, 'entry', 'คำถอน', '๓๐๒'),
    (44, 'entry', 'คำอธิษฐานเข้าพรรษา', '๓๐๓'),
    (44, 'entry', 'คำปวารณาออกพรรษา', '๓๐๓'),
    (44, 'entry', 'คำสัตตาหะ', '๓๐๓'),
    (44, 'entry', 'คำอนุโมทนากฐิน', '๓๐๓'),
    (44, 'entry', 'คำลาสิกขา', '๓๐๓'),
    (44, 'entry', 'คำแสดงตนเป็นอุบาสก', '๓๐๓'),
    (44, 'entry', 'กิจวัตร ๑๐ อย่าง', '๓๐๔'),
    (44, 'entry', 'คำอปโลกน์กฐิน แบบ ๒ รูป', '๓๐๕'),
    (44, 'entry', 'คำอปโลกน์กฐิน แบบ ๔ รูป', '๓๐๖'),
    (44, 'entry', 'แบบกรรมวาจาสวดให้ผ้ากฐิน', '๓๐๘'),
    (44, 'entry', 'คำอธิษฐานผ้ากฐิน', '๓๐๘'),
    (44, 'entry', 'คำอนุโมทนากฐิน', '๓๐๘'),
]



# The English name for each contents line, keyed by the Thai title and
# deduplicated — the book lists several chants more than once, in the
# morning service, again in the evening, and again in the translated
# section, and one gloss serves all of them.
#
# Titles belonging to a chant already in CHANTS are deliberately ABSENT:
# the builder reads title_english off the chant itself, so the index and
# the chant page can never give a reader two different names for the same
# thing. Everything here is written for this app, never taken from the
# book, which prints no English at all.
_CONTENTS_ENGLISH = {
    'ทำวัตรเช้า':
        'The Morning Service',
    'คำอธิบายประกอบทำวัตรเช้า':
        'Notes on the morning service',
    'คำประกาศอุโบสถ':
        'The Uposatha Announcement',
    'คำอาราธนาอุโบสถศีล':
        'Requesting the Uposatha precepts',
    'อุโบสถศีล':
        'The Uposatha Precepts',
    'สะระณะคะมะนานุสสะระณะคาถา':
        'Verses recollecting the going for refuge',
    'คำขอขมาพระรัตนตรัย':
        'Asking pardon of the Triple Gem',
    'เสขิยวัตร':
        'The Sekhiya Training Rules',
    'สารุปปะ ๒๖ สิกขาบท':
        'Proper conduct — 26 training rules',
    'โภชชะนะปะฏิสังยุต ๓๐ สิกขาบท':
        'Concerning almsfood — 30 training rules',
    'ธัมมะเทสะนาปะฏิสังยุต ๑๖ สิกขาบท':
        'Concerning teaching the Dhamma — 16 training rules',
    'ปะกิณณะกะ ๓ สิกขาบท':
        'Miscellaneous — 3 training rules',
    'พระสูตร ปาฐะ และคาถาที่กำหนดสวดในภาคเช้า':
        'Suttas, passages and verses appointed for the morning',
    'ทะสะธัมมะสุตตัง':
        'The Ten Dhammas Sutta',
    'ปะริตตะกะระณะปาโฐ':
        'The passage for making a protection chant',
    'นิธิกัณฑะคาถา':
        'Verses on the Hidden Treasure',
    'ธัมมะคาระวาทิคาถา':
        'Verses on reverence for the Dhamma',
    'เขมาเขมะสะระณะคะมะนะปะริทีปิกาคาถา':
        'Verses showing the secure and the insecure refuge',
    'วิหาระทานะคาถา':
        'Verses on the gift of a dwelling',
    'สัจจะปานะวิธ์ยานุรูปะคาถา':
        'Verses befitting a pledge of truth',
    'อาทิยะสุตตะคาถา':
        'Verses from the Ādiya Sutta — the right use of wealth',
    'อริยะธะนะคาถา':
        'Verses on the noble treasures',
    'มะหากัสสะปะโพชฌังคะสุตตัง':
        'The Mahākassapa Bojjhaṅga Sutta',
    'มะหาโมคคัลลานะโพชฌังคะสุตตัง':
        'The Mahāmoggallāna Bojjhaṅga Sutta',
    'มะหาจุนทะโพชฌังคะสุตตัง':
        'The Mahācunda Bojjhaṅga Sutta',
    'สวดแจง':
        'The Suat Jaeng — chanting the summary of the Canon',
    'พระวินัยสังเขป':
        'The Vinaya in summary',
    'พระสูตรสังเขป':
        'The Suttas in summary',
    'พระอภิธรรมสังเขป':
        'The Abhidhamma in summary',
    'พระสังคะณี':
        'The Dhammasaṅgaṇī',
    'พระวิภังค์':
        'The Vibhaṅga',
    'พระธาตุกะถา':
        'The Dhātukathā',
    'พระปุคคะละบัญญัติ':
        'The Puggalapaññatti',
    'พระกะถาวัตถุ':
        'The Kathāvatthu',
    'พระยะมะกะ':
        'The Yamaka',
    'พระมะหาปัฏฐาน':
        'The Mahāpaṭṭhāna',
    'ธัมมะสังคะณีมาติกาปาโฐ':
        'The Dhammasaṅgaṇī mātikā passage',
    'วิปัสสะนาภูมิปาโฐ':
        'The passage on the ground of insight',
    'ถวายพรพระ':
        'Offering blessings to the Buddha',
    'ชะยะมังคะลัฏฐะกะคาถา':
        'The Eight Verses of Victory and Blessing',
    'ชะยะปะริตตะคาถา':
        'The Victory Protection verses',
    'มงคลจักรวาฬน้อย':
        'The Lesser Universal Blessing',
    'กาละทานะสุตตะคาถา':
        'Verses from the Kāladāna Sutta — giving at the right time',
    'สังคะหะวัตถุคาถา':
        'Verses on the grounds of kindness',
    'โมกขุปายะคาถา':
        'Verses on the way to liberation',
    'ระตะนัตตะยัปปะภาวะสิทธิคาถา':
        'Verses on the accomplishing power of the Triple Gem',
    'ทำวัตรเย็น':
        'The Evening Service',
    'ระเบียบทำวัตรสวดมนต์ ภาคเย็น':
        'The order of the evening service',
    'คาถาบูชาพระรัตนตรัย':
        'Verses of homage to the Triple Gem',
    'คำเชิญบูชาสวดนะโม และพระพุทธคุณ':
        'The invitation to revere, chant the Namo, and praise the Buddha',
    'พุทธะมังคะละคาถา':
        'The Buddha Blessing verses',
    'สีลุทเทสะปาโฐ':
        'The passage setting out the precepts',
    'บทขัดสิกขาบท ๑๐':
        'Preparatory verses for the ten training rules',
    'สิกขาบท ๑๐':
        'The ten training rules',
    'บทขัดนาสะนังคะ':
        'Preparatory verses for the Nāsanaṅga',
    'นาสะนังคะ ๑๐ สิกขาบท':
        'The Nāsanaṅga — ten grounds for expulsion',
    'บทขัดทัณฑะกรรม':
        'Preparatory verses for the Daṇḍakamma',
    'ทัณฑะกรรม ๕ สิกขาบท':
        'The Daṇḍakamma — five grounds for penalty',
    'อะตีตะปัจจะเวกขะณะปาโฐ':
        'The passage reflecting on requisites already used',
    'อุทิสสะนาธิฏฐานะคาถา':
        'Verses dedicating merit and making a resolve',
    'คำอธิบายประกอบทำวัตรเย็น':
        'Notes on the evening service',
    'คำเชิญบูชาพระรัตนตรัยพิเศษ':
        'The special invitation to revere the Triple Gem',
    'คาถาอาราธนาธรรม':
        'Verses requesting a Dhamma teaching',
    'คำถวายดอกไม้ ธูป เทียน ในวันวิสาขบูชา':
        'Offering flowers, incense and candles on Visākha Pūjā',
    'สะระภัญญะคาถา สำหรับสวดในวันวิสาขบูชา':
        'Saraphañña verses for chanting on Visākha Pūjā',
    'คำถวายดอกไม้ ธูป เทียน ในวันอัฏฐมีบูชา':
        'Offering flowers, incense and candles on Aṭṭhamī Pūjā',
    'สะระภัญญะคาถา สำหรับสวดในวันอัฏฐมีบูชา':
        'Saraphañña verses for chanting on Aṭṭhamī Pūjā',
    'คำถวายดอกไม้ ธูป เทียน ในวันมาฆบูชา':
        'Offering flowers, incense and candles on Māgha Pūjā',
    'สะระภัญญะคาถา สำหรับสวดในวันมาฆบูชา':
        'Saraphañña verses for chanting on Māgha Pūjā',
    'บทขัดโอวาทะปาติโมกขาทิปาฐะ':
        'Preparatory verses for the Ovāda-pāṭimokkha passage',
    'โอวาทะปาติโมกขาทิปาโฐ':
        'The Ovāda-pāṭimokkha — the Buddha’s summary exhortation',
    'คำถวายดอกไม้ ธูป เทียน ในวันอาสาฬหบูชา':
        'Offering flowers, incense and candles on Āsāḷha Pūjā',
    'พระสูตร พระปริตร ปาฐะ และคาถาที่กำหนดสวดในภาคเย็น':
        'Suttas, protection chants, passages and verses appointed for the evening',
    'บทขัดชุมนุมเทวดา':
        'Preparatory verses inviting the devas to assemble',
    'ปุพพะภาคะนะมะการะปาโฐ':
        'The preliminary passage of homage',
    'สะระณะคะมะนะปาโฐ':
        'The passage of going for refuge',
    'นะมะการะสิทธิคาถา':
        'Verses on the power of paying homage',
    'นะโมการะอัฏฐะกะคาถา':
        'The Eight Verses of the Namo',
    'บทขัดต้นตำนาน':
        'Preparatory verses opening the Tamnan sequence',
    'บทขัดมังคะละสุตตัง':
        'Preparatory verses for the Maṅgala Sutta',
    'มังคะละสุตตัง ปะฐะมัง':
        'The Maṅgala Sutta — the first',
    'บทขัดระตะนะสุตตัง':
        'Preparatory verses for the Ratana Sutta',
    'ระตะนะสุตตัง ทุติยัง':
        'The Ratana Sutta — the second',
    'บทขัดกะระณียะเมตตะสุตตัง':
        'Preparatory verses for the Karaṇīya Mettā Sutta',
    'กะระณียะเมตตะสุตตัง ตะติยัง':
        'The Karaṇīya Mettā Sutta — the third',
    'บทขัดขันธะปะริตตัง ฉัททันตะปะริตัง':
        'Preparatory verses for the Khandha and Chaddanta protections',
    'ขันธะปะริตตัง จะตุตถัง':
        'The Khandha Paritta — the fourth',
    'ฉัททันตะปะริตตัง':
        'The Chaddanta Paritta',
    'บทขัดโมระปะริตตัง':
        'Preparatory verses for the Mora Paritta',
    'โมระปะริตตัง ปัญจะมัง':
        'The Mora Paritta — the fifth',
    'บทขัดวัฏฏะกะปะริตตัง':
        'Preparatory verses for the Vaṭṭaka Paritta',
    'วัฏฏะกะปะริตตัง ฉัฏฐัง':
        'The Vaṭṭaka Paritta — the sixth',
    'บทขัดธะชัคคะสุตตัง':
        'Preparatory verses for the Dhajagga Sutta',
    'ธะชัคคะปะริตตัง ธะชัคคะสุตตัง สัตตะมัง':
        'The Dhajagga Paritta, the Dhajagga Sutta — the seventh',
    'บทขัดอาฏานาฏิยะปะริตตัง':
        'Preparatory verses for the Āṭānāṭiya Paritta',
    'อาฏานาฏิยะปะริตตัง อัฏฐะมัง':
        'The Āṭānāṭiya Paritta — the eighth',
    'บทขัดอังคุลิมาละปะริตตัง':
        'Preparatory verses for the Aṅgulimāla Paritta',
    'อังคุลิมาละปะริตตัง นะวะมัง':
        'The Aṅgulimāla Paritta — the ninth',
    'บทขัดโพชฌังคะปะริตตัง':
        'Preparatory verses for the Bojjhaṅga Paritta',
    'โพชฌังคะปะริตตัง ทะสะมัง':
        'The Bojjhaṅga Paritta — the tenth',
    'บทขัดอะภะยะปะริตตัง':
        'Preparatory verses for the Abhaya Paritta',
    'อะภะยะปะริตตัง เอกาทะสะมัง':
        'The Abhaya Paritta — the eleventh',
    'เทวะตาอุยโยชะนะคาถา':
        'Verses taking leave of the devas',
    'บทขัดชะยะปะริตตัง':
        'Preparatory verses for the Jaya Paritta',
    'ชะยะปะริตตัง ท์วาทะสะมัง':
        'The Jaya Paritta — the twelfth',
    'ระตะนัตตะยัปปะภาวาภิยาจะนะคาถา':
        'Verses appealing to the power of the Triple Gem',
    'สุขาภิยาจะนะคาถา':
        'Verses appealing for happiness',
    'มงคลจักรวาฬใหญ่':
        'The Greater Universal Blessing',
    'บทขัดทะสะนาถะกะระณะธัมมะสุตตัง':
        'Preparatory verses for the Dasanāthakaraṇadhamma Sutta',
    'ทะสะนาถะกะระณะธัมมะสุตตัง':
        'The Sutta on the ten qualities that make a refuge',
    'บทขัดอะภิณ์หะปัจจะเวกขะณะปาฐะ':
        'Preparatory verses for the passage of frequent recollection',
    'อะภิณ์หะปัจจะเวกขะณะปาโฐ':
        'The passage of frequent recollection',
    'บทขัดมัคคะวิภังคะสุตตัง':
        'Preparatory verses for the Maggavibhaṅga Sutta',
    'มัคคะวิภังคะสุตตัง':
        'The Maggavibhaṅga Sutta — the path analysed',
    'อัฏฐังคิกะมัคคะคาถา':
        'Verses on the Noble Eightfold Path',
    'บทขัดกะระณียากะระณียะสุตตัง':
        'Preparatory verses for the Karaṇīyākaraṇīya Sutta',
    'กะระณียากะระณียะสุตตัง':
        'The Sutta on what should and should not be done',
    'บทขัดอัคคัปปะสาทะสุตตัง':
        'Preparatory verses for the Aggappasāda Sutta',
    'อัคคัปปะสาทะสุตตัง':
        'The Sutta on the highest confidence',
    'บทขัดฉะสาราณียะธัมมะสุตตัง':
        'Preparatory verses for the Chasāraṇīyadhamma Sutta',
    'ฉะสาราณียะธัมมะสุตตัง':
        'The Sutta on the six memorable qualities',
    'บทขัดภิกขุอะปะริหานิยะธัมมะสุตตัง':
        'Preparatory verses for the Bhikkhu-aparihāniyadhamma Sutta',
    'ภิกขุอะปะริหานิยะธัมมะสุตตัง':
        'The Sutta on the conditions of a bhikkhu’s non-decline',
    'บทขัดปะหานะภาวะนาสุตตัง':
        'Preparatory verses for the Pahānabhāvanā Sutta',
    'ปะหานะภาวะนาสุตตัง':
        'The Sutta on abandoning and developing',
    'บทขัดจะตุรัปปะมัญญาปาฐะ':
        'Preparatory verses for the four boundless states',
    'จะตุรัปปะมัญญาปาโฐ':
        'The passage on the four boundless states',
    'บทขัดธัมมะนิยามะสุตตัง':
        'Preparatory verses for the Dhammaniyāma Sutta',
    'ธัมมะนิยามะสุตตัง':
        'The Sutta on the certainty of the Dhamma',
    'บทขัดอะนัตตะลักขะณะสุตตัง':
        'Preparatory verses for the Anattalakkhaṇa Sutta',
    'อะนัตตะลักขะณะสุตตัง':
        'The Sutta on the characteristic of not-self',
    'บทขัดอาทิตตะปะริยายะสุตตัง':
        'Preparatory verses for the Ādittapariyāya Sutta',
    'อาทิตตะปะริยายะสุตตัง':
        'The Fire Sermon',
    'บทขัดสะติปัฏฐานะปาฐะ':
        'Preparatory verses for the Satipaṭṭhāna passage',
    'สะติปัฏฐานะปาโฐ':
        'The passage on the foundations of mindfulness',
    'มะหาสะติปัฏฐานะสุตตะปาโฐ':
        'The Mahāsatipaṭṭhāna Sutta passage',
    'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันโกน วันพระ เวลาเย็น':
        'Suttas, protections and passages appointed for the eve of the observance day and the observance day itself, in the evening',
    'บทขัดธัมมะจักกัปปะวัตตะนะสุตตัง':
        'Preparatory verses for the Dhammacakkappavattana Sutta',
    'ธัมมะจักกัปปะวัตตะนะสุตตัง':
        'The Setting in Motion of the Wheel of the Dhamma',
    'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันขึ้นหรือแรม ๘ ค่ำ เวลาเย็น':
        'Suttas, protections and passages appointed for the eighth day of the waxing or waning moon, in the evening',
    'ปุพพะภาคะมะนะการะปาโฐ':
        'The preliminary passage of homage',
    'มังคะละสุตตัง':
        'The Maṅgala Sutta',
    'ระตะนะสุตตัง':
        'The Ratana Sutta',
    'กะระณียะเมตตะสุตตัง':
        'The Karaṇīya Mettā Sutta',
    'ขันธะปะริตตัง':
        'The Khandha Paritta',
    'ธะชัคคะปะริตตัง (แบบย่อ)':
        'The Dhajagga Paritta — short form',
    'อาฏานาฏิยะปะริตตัง':
        'The Āṭānāṭiya Paritta',
    'อังคุลิมาละปะริตตัง':
        'The Aṅgulimāla Paritta',
    'โพชฌังคะปะริตตัง':
        'The Bojjhaṅga Paritta',
    'อะภะยะปะริตตัง':
        'The Abhaya Paritta',
    'ชะยะปะริตตัง':
        'The Jaya Paritta',
    'พระสูตรที่กำหนดสวดในวันขึ้น ๑๔ ค่ำ เวลาเย็น':
        'The Sutta appointed for the fourteenth day of the waxing moon, in the evening',
    'บทขัดมะหาสะมะยะสุตตัง':
        'Preparatory verses for the Mahāsamaya Sutta',
    'มะหาสะมะยะสุตตัง':
        'The Mahāsamaya Sutta — the great assembly',
    'พระสูตรที่กำหนดสวดในวันแรม ๗ ค่ำ เวลาเย็น':
        'The Sutta appointed for the seventh day of the waning moon, in the evening',
    'คิริมานันทะสุตตัง':
        'The Girimānanda Sutta',
    'พระสูตรที่กำหนดสวดในวันแรม ๑๓ ค่ำหรือ ๑๔ ค่ำ เวลาเย็น':
        'The Sutta appointed for the thirteenth or fourteenth day of the waning moon, in the evening',
    'บทขัดโลกะธัมมะสุตตัง':
        'Preparatory verses for the Lokadhamma Sutta',
    'โลกะธัมมะสุตตัง':
        'The Sutta on the worldly conditions',
    'บทสวดมนต์ ทำวัตรเช้า-เย็น แปล':
        'The morning and evening services, with translation',
    'ทำวัตรเช้า แปล':
        'The Morning Service, translated',
    'ปุพพะภาคะนะมะการ':
        'The preliminary homage',
    'พุทธาภิถุติ':
        'In praise of the Buddha',
    'ธัมมาภิถุติ':
        'In praise of the Dhamma',
    'สังฆาภิถุติ':
        'In praise of the Sangha',
    'พุทธชัยมงคลคาถา (ถวายพรพระ)':
        'The Buddha’s Victory Blessing verses — offering blessings',
    'สัพพะปัตติทานะคาถา':
        'Verses dedicating merit to all beings',
    'ปัฏฐะนะฐะปะนะคาถา':
        'Verses establishing an aspiration',
    'เขมาเขมะสะระณะทีปิกะคาถา':
        'Verses showing the secure and the insecure refuge',
    'อะภิณหะปัจจะเวกขะณะ ๕':
        'The five subjects for frequent recollection',
    'คาถาโพธิบาท':
        'Verses at the foot of the Bodhi tree',
    'คาถามงคลจักรวาฬแปดทิศ':
        'Verses of universal blessing in the eight directions',
    'คำแผ่เมตตาให้แก่ตนเอง':
        'Spreading loving-kindness to oneself',
    'คำแผ่เมตตาให้ผู้อื่น':
        'Spreading loving-kindness to others',
    'ทำวัตรเย็นแปล':
        'The Evening Service, translated',
    'พุทธานุสสะติ':
        'Recollection of the Buddha',
    'พุทธาภิคีติ':
        'The chant in praise of the Buddha',
    'ธัมมานุสสะติ':
        'Recollection of the Dhamma',
    'ธัมมาภิคีติ':
        'The chant in praise of the Dhamma',
    'สังฆานุสสะติ':
        'Recollection of the Sangha',
    'สังฆาภิคีติ':
        'The chant in praise of the Sangha',
    'นมัสการพระอรหันต์ ๘ ทิศ':
        'Homage to the arahants of the eight directions',
    'อุณ์หิสสะวิชะยะคาถา':
        'The Uṇhissavijaya verses',
    'พระคาถาชินบัญชร':
        'The Jinapañjara — the Victor’s Armour',
    'ยอดพระกัณฑ์ไตรปิฎก':
        'The Crown Section of the Tipiṭaka',
    'ภาคปกิณกะ':
        'Miscellaneous section',
    'คำอาราธนาศีล ๕ ปรกติ':
        'Requesting the ordinary five precepts',
    'คำอาราธนาศีล ๕ พิเศษ คือ นิจศีล':
        'Requesting the special five precepts, kept permanently',
    'คำอาราธนาศีล ๘ ปรกติ':
        'Requesting the ordinary eight precepts',
    'คำอาราธนาศีล ๘ พิเศษ คืออุโบสถศีล':
        'Requesting the special eight precepts, the Uposatha precepts',
    'คำอาราธนาสวดพระปริตร':
        'Requesting the chanting of the protection verses',
    'คำอาราธนาแสดงธรรม':
        'Requesting a Dhamma talk',
    'คำอาราธนาแสดงธรรมอย่างพิสดาร':
        'Requesting a Dhamma talk, elaborate form',
    'คำบังสุกุลศพหรืออัฐิ':
        'The paṃsukūla for a body or relics',
    'คำบังสุกุลคนเป็น':
        'The paṃsukūla for the living',
    'คำขอขมาโทษพระรัตนตรัย':
        'Asking pardon of the Triple Gem',
    'คำขอขมาโทษแด่พระมหาเถระ':
        'Asking pardon of a senior elder',
    'คำรับขมาโทษของพระมหาเถระ':
        'A senior elder’s acceptance of the apology',
    'คำอนุโมทนาของพระมหาเถระ':
        'A senior elder’s expression of rejoicing',
    'คาถาจุดเทียนชัย':
        'Verses for lighting the victory candle',
    'คาถาดับเทียนชัย':
        'Verses for extinguishing the victory candle',
    'อธิบายระเบียบสวดมนต์ในพิธีต่าง ๆ':
        'Notes on the order of chanting at the various ceremonies',
    'ระเบียบสวดมนต์งานพิธีมงคล':
        'The order of chanting at auspicious ceremonies',
    'ระเบียบสวดมนต์งานพิธีมงคลอื่น ๆ':
        'The order of chanting at other auspicious ceremonies',
    'ระเบียบสวดเจ็ดตำนานอย่างเต็มที่':
        'The Seven Tamnan in full',
    'ระเบียบสวดเจ็ดตำนานอย่างปานกลาง':
        'The Seven Tamnan, middle length',
    'ระเบียบสวดเจ็ดตำนานอย่างย่อ':
        'The Seven Tamnan in brief',
    'ระเบียบสวดถวายพรพระก่อนฉัน':
        'The order of offering blessings before the meal',
    'ระเบียบสวดในงานพิธีอวมงคล':
        'The order of chanting at funeral ceremonies',
    'อธิบายระเบียบสวดมนต์พิเศษ':
        'Notes on the special chanting orders',
    'ระเบียบสวดมนต์นพเคราะห์':
        'The order of chanting for the nine planets',
    'ระเบียบถวายพรพระ':
        'The order of offering blessings',
    'ระเบียบอนุโมทนา':
        'The order of rejoicing in merit',
    'อนุโมทนาวิธี':
        'The method of rejoicing in merit',
    'มงคลจักรวาฬน้อย (ย่อ)':
        'The Lesser Universal Blessing — short form',
    'อัคคัปปะสาทะสุตตะคาถา':
        'Verses from the Aggappasāda Sutta',
    'ติโรกุฑฑะกัณฑะปัจฉิมภาค':
        'The Tirokuḍḍa Kaṇḍa — closing portion',
    'โภชะนะทานุโมทะนาคาถา':
        'Verses rejoicing in the gift of food',
    'อาฏานาฏิยะปะริตตัง (ย่อ)':
        'The Āṭānāṭiya Paritta — short form',
    'ระเบียบบังสุกุล':
        'The order of the paṃsukūla',
    'คาถาศราทธพรต':
        'Verses for the memorial offering',
    'คำอธิบายประกอบ':
        'Accompanying notes',
    'ภาคผนวก':
        'Appendix',
    'วิธีบรรพชาอุปสมบทแบบอุกาสะ':
        'The going forth and ordination — the Ukāsa form',
    'วิธีบรรพชาอุปสมบทแบบเอสาหัง':
        'The going forth and ordination — the Esāhaṃ form',
    'คำขอบรรพชานาคคู่':
        'Requesting the going forth — for a pair of candidates',
    'คำขอนิสสัยนาคคู่':
        'Requesting dependence — for a pair of candidates',
    'คำขออุปสมบทพร้อมกัน':
        'Requesting ordination together',
    'คำบอกอนุศาสน์':
        'Delivering the admonition',
    'แบบสวดกรรมวาจาในอุปสมบทกรรม สำหรับนาคเดี่ยว':
        'The formal act of ordination — for a single candidate',
    'คำสมมติตนเพื่อสอนซ้อม':
        'Appointing oneself to instruct the candidate',
    'คำสอนซ้อม':
        'Instructing the candidate',
    'คำเรียกอุปสัมปทาเปกขะเข้ามา':
        'Calling the candidate forward',
    'คำพระอุปัชฌายะกล่าวเผดียงสงฆ์':
        'The preceptor’s announcement to the Sangha',
    'คำสมมติตนเพื่อถามอันตรายิกธรรม':
        'Appointing oneself to ask the disqualifying questions',
    'คำถามอันตรายิกธรรม':
        'The disqualifying questions',
    'กรรมวาจาอุปสมบท':
        'The formal act of ordination',
    'คำสวดสมมติและคำสอนซ้อม (นาคคู่)':
        'The appointment and instruction — for a pair of candidates',
    'คำขอเรียกอุปสัมปทาเปกขะเข้ามา':
        'Asking to call the candidates forward',
    'คำสมมติตนและคำถามอันตรายิกธรรม':
        'The appointment and the disqualifying questions',
    'คำพระอุปัชฌาย์กล่าวเผดียงสงฆ์':
        'The preceptor’s announcement to the Sangha',
    'คำสวดกรรมวาจาอุปสมบท':
        'Chanting the formal act of ordination',
    'คำขอบวชชี':
        'Requesting ordination as a nun',
    'คำอาราธนาศีล ๘':
        'Requesting the eight precepts',
    'คำนมัสการพระพุทธเจ้า':
        'Homage to the Buddha',
    'คำสมาทานศีล':
        'Undertaking the precepts',
    'วิธีแสดงอาบัติ':
        'The method of confessing an offence',
    'คำพินทุผ้า':
        'Marking a robe',
    'คำอธิษฐาน':
        'Words of determination',
    'คำเสียสละ':
        'Words of relinquishment',
    'คำคืน':
        'Words of returning',
    'คำวิกัปป์':
        'Words of shared ownership',
    'คำถอน':
        'Words of withdrawal',
    'คำอธิษฐานเข้าพรรษา':
        'Determining to enter the Rains Retreat',
    'คำปวารณาออกพรรษา':
        'The invitation at the end of the Rains Retreat',
    'คำสัตตาหะ':
        'The seven-day leave',
    'คำอนุโมทนากฐิน':
        'Rejoicing in the Kaṭhina',
    'คำลาสิกขา':
        'Words of disrobing',
    'คำแสดงตนเป็นอุบาสก':
        'Declaring oneself a lay follower',
    'กิจวัตร ๑๐ อย่าง':
        'The ten regular duties',
    'คำอปโลกน์กฐิน แบบ ๒ รูป':
        'Announcing the Kaṭhina — the form for two bhikkhus',
    'คำอปโลกน์กฐิน แบบ ๔ รูป':
        'Announcing the Kaṭhina — the form for four bhikkhus',
    'แบบกรรมวาจาสวดให้ผ้ากฐิน':
        'The formal act for bestowing the Kaṭhina cloth',
    'คำอธิษฐานผ้ากฐิน':
        'Determining the Kaṭhina cloth',
}

THAI_DIGITS = '๐๑๒๓๔๕๖๗๘๙'


def thai_number(printed):
    """Turn the Thai numerals the book prints into an integer.

    The book numbers everything this way, so this is what lets a page the app
    can link to be worked out from the page a reader actually sees. Raises on
    anything that is not a Thai numeral rather than guessing — a contents line
    pointing at the wrong page is the same failure as a chant on the wrong one.
    """
    return int(''.join(str(THAI_DIGITS.index(ch)) for ch in printed))


def build_contents(chants=None, front_page=None):
    """The contents as the app uses it.

    Each printed line gains three things the book does not print: the page as
    an integer so a link can be built, an English name, and the id of the chant
    it names where that chant is in the app — which is what lets a reader go
    straight to the chant rather than to the page it happens to start on.

    `front_page` narrows it to one printed page of the contents, which is what
    the reading view ever wants.

    A chant's own `title_english` wins wherever there is one, so the index and
    the chant page cannot end up calling the same thing two different names.
    Both lookups are built once here rather than searched per row: at 301 rows
    against a book heading for 286 chants, a linear scan per row is ~86,000
    comparisons to answer a question a dict answers outright.
    """
    if chants is None:
        chants = CHANTS

    chant_id_by_title = {}
    english_by_title = {}
    for chant in chants:
        title = chant.get('title_thai')
        if not title:
            continue
        chant_id_by_title.setdefault(title, chant['id'])
        if chant.get('title_english'):
            english_by_title.setdefault(title, chant['title_english'])

    return [
        {
            'front_page': front,
            'level': level,
            'title': title,
            'title_english': english_by_title.get(
                title, _CONTENTS_ENGLISH.get(title, '')),
            'page_printed': printed,
            'page': thai_number(printed),
            'chant_id': chant_id_by_title.get(title),
        }
        for front, level, title, printed in _CONTENTS_LINES
        if front_page is None or front == front_page
    ]


CONTENTS = build_contents()


def contents_for_front_page(number, chants=None, page_blocks=None):
    """The contents lines printed on one front-matter page, ready to render.

    Each line gains `in_app`: True where the body page it points at has been
    entered and can therefore be linked. False is not a gap in the book — it is
    a page of the book that is not in the app yet, and saying so plainly is the
    point. A contents entry that looked like a link and went nowhere would be a
    worse lie than one that is honestly plain text.

    Returns (rows, entered) — the lines, and the body pages that are in, so a
    caller that wants both does not rebuild the page index to get the second.
    """
    pages, _ = build_page_index(chants, page_blocks)
    entered = sorted(page['page'] for page in pages)
    have = set(entered)
    rows = build_contents(chants, front_page=number)
    return [dict(row, in_app=row['page'] in have) for row in rows], entered


def get_chant(chant_id):
    """Return one chant by id, or None."""
    return next((c for c in CHANTS if c['id'] == chant_id), None)


def check_page_blocks(chants=None, page_blocks=None):
    """Return a list of problems with PAGE_BLOCKS, empty when it is sound.

    This is where a bad anchor is caught. `build_page_index` deliberately does
    not raise — a typo must not be able to take the chanting book down at
    request time — so the strictness lives here instead, and a test runs it
    over the real data. That keeps the guarantee (nothing is placed on a page
    it was not printed on) without making every reader depend on it.

    Checks that every `after` names a chant actually printed on that page, and
    that every block carries the keys its type is rendered from. A block whose
    `thai` is missing would render as an empty line: present in the data,
    invisible on the page, and impossible to spot by reading the file.
    """
    if chants is None:
        chants = CHANTS
    if page_blocks is None:
        page_blocks = PAGE_BLOCKS

    pages, _ = build_page_index(chants, page_blocks=[])
    chants_on_page = {
        page['page']: {entry['chant']['id'] for entry in page['entries']}
        for page in pages
    }
    # Built once. It was inside the group loop, which is invisible at thirty
    # chants and is a rebuild per group across a 286-chant book.
    by_id = {chant['id']: chant for chant in chants}

    problems = []
    for group in page_blocks:
        page = group.get('page')
        anchor = group.get('after')
        if anchor is not None and anchor not in chants_on_page.get(page, set()):
            problems.append(
                f"page {page}: blocks anchored after '{anchor}', which is not "
                f"printed on that page"
            )
        for named in group.get('invitation_printed_here', ()):
            if named not in chants_on_page.get(page, set()):
                problems.append(
                    f"page {page}: invitation_printed_here names '{named}', "
                    f"which is not printed on that page"
                )
        for index, block in enumerate(group.get('blocks', [])):
            where = f"page {page}, block {index} ({block.get('type')})"

            # An invitation block carries no text of its own — it names a
            # chant and the words are read back off it. So what has to be
            # true is that the chant exists, is on this page, and has an
            # invitation to show; otherwise the block renders as nothing and
            # the page silently loses the line that starts the chant.
            if block.get('type') == 'invitation':
                named = block.get('chant')
                if not named:
                    # Written out in full because the chant it invites is not
                    # on this page to read it off.
                    if not block.get('pali'):
                        problems.append(
                            f'{where}: neither names a chant nor prints a line')
                    continue
                source = by_id.get(named)
                if source is None:
                    problems.append(f'{where}: names no chant that exists')
                elif not (source.get('invitation') or {}).get('pali'):
                    problems.append(
                        f"{where}: '{named}' has no invitation to print")
                elif named not in chants_on_page.get(page, set()):
                    problems.append(
                        f"{where}: '{named}' is not printed on that page")
                continue

            if not block.get('thai'):
                problems.append(f'{where}: no `thai`, so it renders as nothing')
            if block.get('type') == 'item' and block.get('number') is None:
                problems.append(f'{where}: a numbered item with no number')
            if block.get('english') and not block.get('english_unverified'):
                problems.append(
                    f'{where}: English that does not say it was written for '
                    f'this app'
                )
    return problems


def build_page_index(chants=None, page_blocks=None):
    """Regroup the book's verses by the printed page they appear on.

    The chants are stored chant by chant, which is how you read one. A monk
    calls out a page, which is how you chant along with everyone else — so the
    same data has to be readable both ways round, and this turns one into the
    other.

    A verse carries `page` ONLY where the printed page turns, exactly as
    `section` marks only where a movement begins. So a verse without one is on
    the same page as the verse before it, and the first is on the chant's
    `page_start`. Carrying that forward reproduces the printed page: whatever
    the book prints there, which is often the end of one chant followed by the
    beginning of the next.

    Returns (pages, unpaginated):

      pages       — ordered list of {'page': int, 'entries': [...]}, in the
                    order they appear down the page. An entry is one of two
                    kinds, told apart by `kind`:

                      'chant'  — {'chant', 'starts_here', 'verses'};
                                 `starts_here` meaning the chant's title is
                                 printed on this page, so the title and
                                 invitation belong here and not on the pages
                                 it continues onto.
                      'blocks' — {'blocks': [...]}, the page's own material:
                                 headings, instruction paragraphs, numbered
                                 items, a service closing, footnotes.

      unpaginated — chants with no `page_start`, which cannot be placed.

    Chants without a page number are RETURNED rather than guessed at. Putting
    one on a plausible page would send a reader to the wrong words in a silent
    room, which is the one error in this book that is met in public.

    A page may hold blocks and no chant at all — a page of instruction between
    two services is a real page of the book, and a reader who turns to it should
    find what is printed there rather than a gap.
    """
    if chants is None:
        chants = CHANTS
    if page_blocks is None:
        page_blocks = PAGE_BLOCKS

    placed = [c for c in chants if c.get('page_start')]
    unpaginated = [c for c in chants if not c.get('page_start')]

    pages = {}      # page number -> {chant id -> entry}, insertion-ordered
    for chant in sorted(placed, key=lambda c: c['page_start']):
        current = chant['page_start']

        def entry_for(page):
            """The entry this chant owns on `page`, created on first use."""
            page_entries = pages.setdefault(page, {})
            if chant['id'] not in page_entries:
                page_entries[chant['id']] = {
                    'chant': chant,
                    # The title page is the one the chant starts on. Every
                    # other page it runs across is a continuation, and repeating
                    # the title on those would be a thing the book does not do.
                    'starts_here': page == chant['page_start'],
                    'verses': [],
                }
            return page_entries[chant['id']]

        # Claim the opening page before walking the verses. A chant whose title
        # sits at the foot of a page with its first verse overleaf still has to
        # appear on that page — with its title and nothing else, which is
        # exactly what the book shows.
        entry_for(current)

        for verse in chant['verses']:
            if verse.get('page'):
                current = verse['page']
            entry_for(current)['verses'].append(verse)

    # Group the page's own material by the page it is printed on, so each page
    # can be assembled in one pass below.
    groups_by_page = {}
    for group in page_blocks:
        groups_by_page.setdefault(group['page'], []).append(group)

    # Built once for the whole book rather than once per page. Only invitation
    # blocks read it, so at thirty chants the difference is nothing — across 286
    # chants and 325 pages it is the same dict built ninety thousand times.
    by_id = {chant['id']: chant for chant in chants}

    built = []
    for page in sorted(set(pages) | set(groups_by_page)):
        chant_entries = list(pages.get(page, {}).values())
        groups = groups_by_page.get(page, [])

        # An anchor naming a chant that is not on this page has nowhere exact
        # to go, so it falls to the foot of the page rather than vanishing.
        # This is NOT the place that error gets caught — `check_page_blocks`
        # is, and a test runs it over the real data. Raising here instead
        # would take the whole chanting book down at request time over a typo
        # in one anchor, which is a far worse failure than one run of prose
        # sitting low on one page.
        on_this_page = {entry['chant']['id'] for entry in chant_entries}
        orphaned = [group for group in groups
                    if group.get('after') is not None
                    and group.get('after') not in on_this_page]

        # A chant whose invitation the book does not print where the app puts
        # it. Two ways that happens, and both mean the same thing here: do not
        # show it a second time under the title.
        #
        #   'invitation_printed_here' — the invitation is inside a sentence,
        #       part of the prose rather than a line of its own (page 7).
        #   an 'invitation' block — the book prints it on its own line, but
        #       with an instruction either side of it, so it has to sit in the
        #       run of blocks to keep the printed order (pages 2-3).
        #
        # The invitation stays on the chant either way: the by-title view needs
        # it, and a printed edition will. An invitation block names the chant
        # and the text is read back off it, so there is only ever one copy.
        invitation_in_prose = set()
        for group in groups:
            invitation_in_prose.update(group.get('invitation_printed_here', ()))
            for block in group.get('blocks', ()):
                if block.get('type') == 'invitation' and block.get('chant'):
                    invitation_in_prose.add(block['chant'])

        by_id = {chant['id']: chant for chant in chants}

        def resolved(blocks):
            """Fill an invitation block from the chant it names.

            Copied rather than written back, so PAGE_BLOCKS stays the data as
            authored and repeated renders cannot accumulate anything.
            """
            out = []
            for block in blocks:
                if block.get('type') == 'invitation':
                    if block.get('chant'):
                        source = by_id.get(block['chant']) or {}
                        invitation = source.get('invitation') or {}
                    else:
                        # An invitation for a chant that is NOT on this page —
                        # page 5 gives the ones for the เสขิยวัตร sections,
                        # which the book sets much later. There is nothing to
                        # read it off, so the line is written out here.
                        invitation = {
                            key: block.get(key, '')
                            for key in ('pali', 'pali_roman', 'thai',
                                        'paiboon', 'english')
                        }
                    block = dict(block, invitation=invitation)
                out.append(block)
            return out

        entries = []
        # Printed above every chant on the page.
        entries.extend({'kind': 'blocks', 'blocks': resolved(group['blocks'])}
                       for group in groups if group.get('after') is None)
        for entry in chant_entries:
            entry['kind'] = 'chant'
            entry['invitation_in_block'] = entry['chant']['id'] in invitation_in_prose
            entries.append(entry)
            entries.extend({'kind': 'blocks', 'blocks': resolved(group['blocks'])}
                           for group in groups if group.get('after') == entry['chant']['id'])
        entries.extend({'kind': 'blocks', 'blocks': resolved(group['blocks'])}
                       for group in orphaned)

        built.append({'page': page, 'entries': entries})

    return built, unpaginated
