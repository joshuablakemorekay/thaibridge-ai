"""The Digital Chanting Book — Pali, Thai, Paiboon and English, verse by verse.

The data lives here rather than in a template on purpose: the same structure
renders the web page today and can generate a printed chanting book later.
Adding a chant means appending one dict to CHANTS — nothing else changes.

Every chant follows the SAME shape, so that between them the six questions a
reader actually has are always answered in the same order:

  * `title_thai` / `title_pali` / `title_roman` / `title_english`
                        — what is this chant? `title_pali` is the title in
                          IAST and is empty where the book prints none;
                          `title_roman` is the THAI title in PAIBOON, so a
                          reader who cannot read Thai script can still say it
                          and find the chant in a printed book. A chant whose
                          title is Pali-in-Thai-script needs only `title_pali`.
                          The two are not interchangeable and a title takes
                          whichever fits what the words ARE: Pali titles are
                          not Thai and cannot be written in Paiboon, Thai
                          titles are not Pali and IAST cannot write their
                          tones. Both must agree with `_CONTENTS_ROMAN`, which
                          is what the contents page prints, and a test holds
                          them to it — a reader arriving at one chant by two
                          routes must not be shown two spellings of its name.
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

A verse may also carry `variants` — a list, and almost always absent. This is
the book's own footnote offering a DIFFERENT READING of one word in that line,
which is a thing a scholarly chanting book does and a thing nothing else in
this file could hold. Page 26 prints ...พ์รัห์มะจาริโน. with a superscript ๒,
and the note at the foot of the page reads พ์รัห์มจาระโย: the same word, spelt
another way, offered as an alternative. Until this field existed there was
nowhere to put it, so it was recorded in a comment and shown to nobody.

It sits on the VERSE and not on the chant, for the reason the photo map gives
about footnotes generally: a footnote belongs to the line its marker sits on.
Two chants can share a page and each have their own, and a variant filed
against the chant rather than the line would leave a reader hunting for which
word it meant.

Each entry carries four keys, and the split between them is the usual one —
what the book prints, and what this app added:

  * `marker`        — the superscript as PRINTED, in whatever numerals the page
                      uses (๒ on page 26). Footnote numbers restart at 1 on
                      every page, so this is only ever meaningful beside its
                      own page.
  * `word`          — the word in this verse's `pali` that the marker sits on,
                      copied from it character for character. It is checked:
                      `check_variants` refuses a `word` that is not in the line,
                      because a variant pointing at the wrong word is the same
                      class of error as a chant on the wrong page.
  * `reading`       — what the footnote prints, character for character. The
                      book's text, never tidied to look more like `word`. On
                      page 26 the two do not even carry the same marks, and
                      that disagreement is the fact being recorded.
  * `reading_roman` — IAST of `reading`, written HERE and not by the book,
                      exactly as `pali_roman` is. Optional: leave it out rather
                      than guess at a form you cannot read confidently.

A variant is NOT a correction and must never be applied to the line. `pali`
stays exactly as the page prints it; the variant sits beside it and says the
book knows of another reading.

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
        'title_roman': 'bòt pí-jaa-rá-naa sǎŋ-kǎan',
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
        # Footnote 1 at the foot of page 28.
        'source': 'ขุ.ขุ. 25/51',
        'group': 'General chanting',
        'page_start': 27,

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
            # Verified against IMG_0289.PNG (page 27) and IMG_0290.PNG (page
            # 28) on 2026-08-08. Two columns, two pādas to a printed line, read
            # left column then right. Seventeen lines and the นิฏฐิตา formula.
            #
            # ‼ CORRECTED: the thirty-four pādas were entered one to a line;
            #              the page prints seventeen lines of two. Only the line
            #              division changed — no word or mark was altered.
            # ‼ CORRECTED: source was ขุ.ขุ. 25/89, ขุ.อุ. 25/221 — that is page
            #              27's footnote, whose marker sits on the last line of
            #              the Devatābhisammantanagāthā above, not on this chant.
            #              This chant's own marker is on its last line and points
            #              to page 28's footnote 1, ขุ.ขุ. 25/51.
            # ‼ RESOLVED: the six section headings previously here were my
            #             grouping. Neither page prints any; they are removed.
            {
                'number': 1,
                'pali': 'สัพเพ สังขารา อะนิจจาติ ยะทา ปัญญายะ ปัสสะติ',
                'pali_roman': 'sabbe saṅkhārā aniccāti yadā paññāya passati',
                'thai': '',
                'paiboon': '',
                'english': (
                    "All conditioned things are impermanent — when one sees "
                    "this with wisdom,"
                ),
            },
            {
                'number': 2,
                'pali': 'อะถะ นิพพินทะติ ทุกเข เอสะ มัคโค วิสุทธิยา.',
                'pali_roman': 'atha nibbindati dukkhe esa maggo visuddhiyā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "then one turns away from suffering. This is the path to "
                    "purity."
                ),
            },
            {
                'number': 3,
                'pali': 'สัพเพ สังขารา ทุกขาติ ยะทา ปัญญายะ ปัสสะติ',
                'pali_roman': 'sabbe saṅkhārā dukkhāti yadā paññāya passati',
                'thai': '',
                'paiboon': '',
                'english': (
                    "All conditioned things are suffering — when one sees "
                    "this with wisdom,"
                ),
            },
            {
                'number': 4,
                'pali': 'อะถะ นิพพินทะติ ทุกเข เอสะ มัคโค วิสุทธิยา.',
                'pali_roman': 'atha nibbindati dukkhe esa maggo visuddhiyā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "then one turns away from suffering. This is the path to "
                    "purity."
                ),
            },
            {
                'number': 5,
                'pali': 'สัพเพ ธัมมา อะนัตตาติ ยะทา ปัญญายะ ปัสสะติ',
                'pali_roman': 'sabbe dhammā anattāti yadā paññāya passati',
                'thai': '',
                'paiboon': '',
                'english': (
                    "All things are not-self — when one sees this with "
                    "wisdom,"
                ),
            },
            {
                'number': 6,
                'page': 28,
                'pali': 'อะถะ นิพพินทะติ ทุกเข เอสะ มัคโค วิสุทธิยา.',
                'pali_roman': 'atha nibbindati dukkhe esa maggo visuddhiyā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "then one turns away from suffering. This is the path to "
                    "purity."
                ),
            },
            {
                'number': 7,
                'pali': 'อัปปะกา เต มะนุสเสสุ เย ชะนา ปาระคามิโน',
                'pali_roman': 'appakā te manussesu ye janā pāragāmino',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Few are they among men, those people who go to the far "
                    "shore;"
                ),
            },
            {
                'number': 8,
                'pali': 'อะถายัง อิตะรา ปะชา ตีระเมวานุธาวะติ.',
                'pali_roman': 'athāyaṃ itarā pajā tīramevānudhāvati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "while the rest of this generation runs up and down "
                    "along the near bank."
                ),
            },
            {
                'number': 9,
                'pali': 'เย จะ โข สัมมะทักขาเต ธัมเม ธัมมานุวัตติโน',
                'pali_roman': 'ye ca kho sammadakkhāte dhamme dhammānuvattino',
                'thai': '',
                'paiboon': '',
                'english': (
                    "But those who, in the Dhamma rightly declared, live in "
                    "accordance with that Dhamma —"
                ),
            },
            {
                'number': 10,
                'pali': 'เต ชะนา ปาระเมสสันติ มัจจุเธยยัง สุทุตตะรัง.',
                'pali_roman': 'te janā pāramessanti maccudheyyaṃ suduttaraṃ.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "those people will reach the far shore, crossing the "
                    "realm of death, so hard to cross."
                ),
            },
            {
                'number': 11,
                'pali': 'กัณหัง ธัมมัง วิปปะหายะ สุกกัง ภาเวถะ ปัณฑิโต',
                'pali_roman': 'kaṇhaṃ dhammaṃ vippahāya sukkaṃ bhāvetha paṇḍito',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Abandoning the dark state, let the wise one develop the "
                    "bright;"
                ),
            },
            {
                'number': 12,
                'pali': 'โอกา อะโนกะมาคัมมะ วิเวเก ยัตถะ ทูระมัง.',
                'pali_roman': 'okā anokamāgamma viveke yattha dūramaṃ.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "coming from home to homelessness, into seclusion, where "
                    "delight is hard to find."
                ),
            },
            {
                'number': 13,
                'pali': 'ตัตราภิระติมิจเฉยยะ หิต์วา กาเม อะกิญจะโน',
                'pali_roman': 'tatrābhiratimiccheyya hitvā kāme akiñcano',
                'thai': '',
                'paiboon': '',
                'english': (
                    "There let him seek his delight, having left sensual "
                    "pleasures, owning nothing;"
                ),
            },
            {
                'number': 14,
                'pali': 'ปะริโยทะเปยยะ อัตตานัง จิตตักเลเสหิ ปัณฑิโต.',
                'pali_roman': 'pariyodapeyya attānaṃ cittaklesehi paṇḍito.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "let the wise one cleanse himself of the defilements of "
                    "the mind."
                ),
            },
            {
                'number': 15,
                'pali': 'เยสัง สัมโพธิยังเคสุ สัมมา จิตตัง สุภาวิตัง',
                'pali_roman': 'yesaṃ sambodhiyaṅgesu sammā cittaṃ subhāvitaṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Those whose minds, in the factors of awakening, are "
                    "rightly and well developed;"
                ),
            },
            {
                'number': 16,
                'pali': 'อาทานะปะฏินิสสัคเค อะนุปาทายะ เย ระตา',
                'pali_roman': 'ādānapaṭinissagge anupādāya ye ratā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "who in the relinquishing of grasping, without clinging, "
                    "take delight —"
                ),
            },
            {
                'number': 17,
                'pali': 'ขีณาสะวา ชุติมันโต เต โลเก ปะรินิพพุตาติ.',
                'pali_roman': 'khīṇāsavā jutimanto te loke parinibbutāti.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "with taints destroyed, radiant, they are wholly "
                    "quenched in the world."
                ),
            },
            {
                'number': 18,
                'pali': 'ติลักขะณาทิคาถา นิฏฐิตา.',
                'pali_roman': 'tilakkhaṇādigāthā niṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The verses on the three characteristics and others are "
                    "ended."
                ),
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
        # ‼ RESOLVED: footnote 2 IS a variant reading, and it is now on the
        #             verse whose marker it belongs to — verse 2, in
        #             `variants`. The verse it was guessed at here ("verse 4")
        #             was the old one-pāda-to-a-line numbering, before the
        #             pādas were joined to match the page. The disagreement
        #             between the two transcriptions of the footnote is carried
        #             as a ‼ CHECK down beside the verses.

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
        'book_number': 7,
        'page_start': 26,

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
            # Verified against IMG_0288.PNG (page 26) on 2026-08-08. The page
            # sets this chant in two columns, two pādas to a printed line, read
            # left column then right. It occupies the foot of page 26 under the
            # heading 7. เทวะตาทิสสะทักขิณานุโมทะนาคาถา and closes there.
            #
            # ‼ CORRECTED: the twelve pādas were entered one to a line. The page
            #              prints six lines of two pādas each. Only the line
            #              division changed — no word or mark was altered.
            # ‼ CORRECTED: pali พ์รัห์มะจาริโน → พ์รัห์มะจาริโน. — the page
            #              closes the second line with a full stop, which the
            #              paste dropped.
            # ‼ RESOLVED: the two section headings previously here were my
            #             grouping. The page prints none; they have been removed.
            # ‼ RESOLVED: the superscript ๒ after พ์รัห์มะจาริโน. on page 26
            #             now has somewhere to live. It is on verse 2 below, in
            #             `variants`, where the marker actually sits.
            # ‼ CHECK [IMG_0288.PNG]: the footnote has been written down twice
            #         in this file and the two do not agree. The chant-level
            #         note, taken from the pasted text, reads พร้ห์มจาระโย with
            #         mai tho. The verified page read of 2026-08-08 reads
            #         พ์รัห์มจาระโย with thanthakhat, matching the verse above
            #         it. `variants` carries the page read, because that one
            #         came from the photograph — but ONE of the two is a
            #         mistranscription of a single mark, and only the book
            #         settles which. Worth a look while page 26 is open.
            {
                'number': 1,
                'pali': 'ยัส์มิง ปะเทเส กัปเปติ วาสัง ปัณฑิตะชาติโย',
                'pali_roman': 'yasmiṃ padese kappeti vāsaṃ paṇḍitajātiyo',
                'thai': '',
                'paiboon': '',
                'english': (
                    "In whatever place he makes his dwelling, one of wise "
                    "nature,"
                ),
            },
            {
                'number': 2,
                'pali': 'สีละวันเตตถะ โภเชต์วา สัญญะเต พ์รัห์มะจาริโน.',
                'pali_roman': 'sīlavantettha bhojetvā saññate brahmacārino.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "having fed there the virtuous, the restrained, the "
                    "farers in the holy life,"
                ),
                # The book's own footnote ๒, keyed to the last word of this
                # line. It offers another reading; it does not correct this
                # one, so the line above stands exactly as page 26 prints it.
                'variants': [
                    {
                        'marker': '๒',
                        'word': 'พ์รัห์มะจาริโน',
                        'reading': 'พ์รัห์มจาระโย',
                        # -jāro is not a form this reader can vouch for, and a
                        # guessed romanisation of a variant would be a second
                        # invention on top of a disputed transcription. Left
                        # out until the word is settled against the book.
                        'reading_roman': '',
                    },
                ],
            },
            {
                'number': 3,
                'pali': 'ยา ตัตถะ เทวะตา อาสุง ตาสัง ทักขิณะมาทิเส',
                'pali_roman': 'yā tattha devatā āsuṃ tāsaṃ dakkhiṇamādise',
                'thai': '',
                'paiboon': '',
                'english': (
                    "whatever devas there may be in that place, to them let "
                    "him dedicate the offering."
                ),
            },
            {
                'number': 4,
                'pali': 'ตา ปูชิตา ปูชะยันติ มานิตา มานะยันติ นัง',
                'pali_roman': 'tā pūjitā pūjayanti mānitā mānayanti naṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "They, being honoured, give honour in return; being held "
                    "in regard, they hold him in regard."
                ),
            },
            {
                'number': 5,
                'pali': 'ตะโต นัง อะนุกัมปันติ มาตา ปุตตังวะ โอระสัง',
                'pali_roman': 'tato naṃ anukampanti mātā puttaṃva orasaṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Thereafter they show him compassion, as a mother "
                    "towards her own-born son."
                ),
            },
            {
                'number': 6,
                'pali': 'เทวะตานุกัมปิโต โปโส สะทา ภัท์รานิ ปัสสะติ.',
                'pali_roman': 'devatānukampito poso sadā bhadrāni passati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The person to whom the devas are compassionate sees "
                    "always what is auspicious."
                ),
            },
            {
                'number': 7,
                'pali': 'เทวะตาทิสสะทักขิณานุโมทะนาคาถา นิฏฐิตา.',
                'pali_roman': 'devatādissadakkhiṇānumodanāgāthā niṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The verses of rejoicing in offerings dedicated to the "
                    "devas are ended."
                ),
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
        # Footnote 1 at the foot of page 27. Its marker sits on this
        # chant's last line, อัปปะมัตตา.
        'source': 'ขุ.ขุ. 25/89, ขุ.อุ. 25/221',
        'group': 'General chanting',
        'page_start': 27,

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
            # Verified against IMG_0289.PNG (page 27) on 2026-08-08. Printed in
            # a SINGLE column, one pāda to a line — unlike the Tilakkhaṇādi
            # gāthā directly below it on the same page. The line division here
            # was already right and is unchanged.
            #
            # ‼ RESOLVED: the five section headings previously here were my
            #             grouping. The page prints none; they are removed.
            {
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
        # Verified against the photographs IMG_0490.PNG (page 220) and
        # IMG_0491.PNG (page 221) on 2026-08-08. The Pali, the Thai and the
        # line division now follow the printed page. What remains flagged
        # below is what the page itself leaves open.
        #
        # ‼ RESOLVED: the Thai is printed as a block beneath each Pali line —
        #             confirmed. For stanza 1 the block covers two Pali lines
        #             and my split of it is noted at the verse.
        # ‼ RESOLVED: the four section headings previously in this entry
        #             (ปัตติทานะ, สัพเพ สัตตา, นิเวทะนา, อาหาระ) are not
        #             printed anywhere on the page and have been removed.
        # ‼ CHECK: the page prints the invitation inside brackets —
        #          (หันทะ มะยัง … เส.) — and this entry stores it unbracketed,
        #          as every other chant in the book does. The same question is
        #          raised at the Bhārasuttagāthā. It wants one decision for the
        #          whole book rather than a change here.
        # ‼ CHECK: source left empty. No footnote or attribution appears on
        #          either page. The title names a king victorious in the three
        #          worlds; I have not inferred a canonical reference from that.
        # ‼ CHECK: The Thai translation is expansive rather than literal
        #          throughout — three-word Pali pādas receive full sentences.
        #          My English renders the Pali, with the Thai's additions
        #          folded in. Where the two differ in scope, the Pali governs.

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
        # Pages 220-221, from the book's own สารบัญ and confirmed on
        # the page itself.
        'page_start': 220,

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
            "the Tāvatiṃsa heaven and the potency of its rewards. The page "
            "sets two pādas to a printed line and prints the Thai as a "
            "block beneath, so the two layers run in step stanza by "
            "stanza rather than pāda by pāda.",
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
            # Verified against IMG_0490.PNG (page 220). The page sets the Pali
            # in two columns, two pādas to a printed line, and prints the Thai
            # as a block beneath. Reading is left column then right column:
            # confirmed by the canonical Pali and by the Thai gloss order in
            # lines 3 to 7.
            #
            # ‼ CORRECTED: the two halves of lines 1, 2 and 3 were transposed.
            #              The pasted source read the page's right column
            #              before its left. The page reads ยังกิญจิ then
            #              กัตตัพพัง, กาเยนะ then ติทะเส, สัญญิโน then
            #              อะสัญญิโน — all three now follow the page.
            {
                'number': 1,
                'pali': 'ยังกิญจิ กุสะลัง กัมมัง, กัตตัพพัง กิริยัง มะมะ,',
                'pali_roman': 'yaṅkiñci kusalaṃ kammaṃ, kattabbaṃ kiriyaṃ mama,',
                'thai': 'กิจที่ควรจะกระทำ, คือกุศลกรรมสิ่งใดสิ่งหนึ่ง,',
                'paiboon': 'gìt tîi kuan jà grà-tam, kʉʉ gù-sǒn-lá-gam sìŋ dai sìŋ nʉ̀ŋ,',
                'english': (
                    "Whatever wholesome action there may be, the deed that is "
                    "to be done by me,"
                ),
            },
            # ‼ CHECK: the page prints ONE Thai block beneath both line 1 and
            #          line 2 — it belongs to the whole four-pāda stanza, not
            #          to either line. Splitting it at this point is mine, made
            #          where the Thai turns from the deed to the doing of it.
            #          The book does not divide it.
            {
                'number': 2,
                'pali': 'กาเยนะ วาจา มะนะสา, ติทะเส สุคะตัง กะตัง,',
                'pali_roman': 'kāyena vācā manasā, tidase sugataṃ kataṃ,',
                'thai': 'อันสัตว์พึงกระทำด้วยกาย วาจา ใจ เป็นของของตนนั้น, ข้าพเจ้าก็ได้สะสมบำเพ็ญแล้ว มีอยู่, กุศลกรรม ทั้งปวงเหล่านั้น ข้าพเจ้าก็ได้กระทำแล้ว, ให้เป็นไป ในเหล่าไตรทศเทพยดาทั้งหลาย, คือมีอานุภาพ วิบาก สมบัติกล้า, ควรจะนำให้อุบัติบังเกิดในดาวดึงสาลัยทิพยสถาน,',
                'paiboon': 'an sàt pʉŋ grà-tam dûay gaai waa-jaa jai bpen kɔ̌ɔŋ kɔ̌ɔŋ dton nán, kâa-pá-jâao gɔ̂ dâai sà-sǒm bam-pen lɛ́ɛo mii yùu, gù-sǒn-lá-gam táŋ-bpuaŋ lào nán kâa-pá-jâao gɔ̂ dâai grà-tam lɛ́ɛo, hâi bpen bpai nai lào dtrai-tót têep-pá-yá-daa táŋ-lǎai, kʉʉ mii aa-nú-pâap wí-bàak sǒm-bàt glâa, kuan jà nam hâi ù-bàt baŋ-gə̀ət nai daao-dʉŋ-sǎa-lai típ-pá-yá-sà-tǎan,',
                'english': (
                    "by body, by speech and by mind — such as a being should "
                    "do and hold as their own: these I have gathered and "
                    "fulfilled, and all those wholesome actions I have indeed "
                    "performed, done such that it leads well among the thirty "
                    "devas, that is, having such power and strength of "
                    "resultant fortune as should bring about rebirth in the "
                    "heavenly abode of Tāvatiṃsa,"
                ),
            },
            # ‼ RESOLVED: the old note here said the Thai named those with
            #             saññā before those without, "the reverse of the Pali
            #             order". The Thai was never reversed — the Pali was.
            #             The page prints สัญญิโน first, matching the Thai.
            # ‼ CORRECTED: thai  ดำรง อยู่ → ดำรงอยู่. One word, broken by the
            #              page's line wrap.
            {
                'number': 3,
                'pali': 'เย สัตตา สัญญิโน อัตถิ, เย จะ สัตตา อะสัญญิโน,',
                'pali_roman': 'ye sattā saññino atthi, ye ca sattā asaññino,',
                'thai': 'สัตว์ทั้งหลายเหล่าใดที่มีสัญญาก็ดี, สัตว์ทั้งหลายเหล่าใดที่มิใช่สัตว์มีสัญญา ดำรงอยู่สักว่ารูปอย่างเดียวก็ดี,',
                'paiboon': 'sàt táŋ-lǎai lào dai tîi mii sǎn-yaa gɔ̂ dii, sàt táŋ-lǎai lào dai tîi mí-châi sàt mii sǎn-yaa dam-roŋ yùu sàk wâa rûup yàaŋ diao gɔ̂ dii,',
                'english': (
                    "and whatever beings there are that possess perception, "
                    "and whatever beings are without perception, subsisting "
                    "as mere form alone,"
                ),
            },
            # ‼ CORRECTED: thai  ครบ ถ้วน → ครบถ้วน. One word, broken by the
            #              page's line wrap.
            {
                'number': 4,
                'pali': 'กะตัง ปุญญะผะลัง มัยหัง, สัพเพ ภาคี ภะวันตุ เต.',
                'pali_roman': 'kataṃ puññaphalaṃ mayhaṃ, sabbe bhāgī bhavantu te.',
                'thai': 'ผลแห่งบุญที่ข้าพเจ้าได้ก่อสร้างแล้วทั้งปวงเหล่านี้, ขอสัตว์ทั้งหลายทั้งหมดครบถ้วนทุกหมู่เหล่า, จงเป็นผู้มีส่วนได้เสวยซึ่งผลแห่งบุญนั้น ๆ,',
                'paiboon': 'pǒn hɛ̀ŋ bun tîi kâa-pá-jâao dâai gɔ̀ɔ-sâaŋ lɛ́ɛo táŋ-bpuaŋ lào níi, kɔ̌ɔ sàt táŋ-lǎai táŋ-mòt króp-tûan túk mùu lào, joŋ bpen pûu mii sùan dâai sà-wə̌əy sʉ̂ŋ pǒn hɛ̀ŋ bun nán nán,',
                'english': (
                    "all this fruit of merit that I have built up — may all "
                    "beings, every group of them complete, be sharers in that "
                    "fruit of merit."
                ),
            },
            # ‼ CORRECTED: thai  ผลแห่งบุญอัน ข้าพเจ้า → ผลแห่งบุญอันข้าพเจ้า.
            #              Broken by the page's line wrap, not a space.
            # ‼ RESOLVED: the old note asked why this Thai line ended with no
            #             punctuation. The page ends it with a comma, as the
            #             lines around it.
            {
                'number': 5,
                'pali': 'เย ตัง กะตัง สุวิทิตัง, ทินนัง ปุญญะผะลัง มะยา,',
                'pali_roman': 'ye taṃ kataṃ suviditaṃ, dinnaṃ puññaphalaṃ mayā,',
                'thai': 'บุญที่ข้าพเจ้าได้กระทำแล้วนั้น, สัตว์ทั้งหลายเหล่าใดได้รู้แจ้งแล้ว, ผลแห่งบุญอันข้าพเจ้าได้ให้แล้วแก่สัตว์ทั้งหลายเหล่านั้น,',
                'paiboon': 'bun tîi kâa-pá-jâao dâai grà-tam lɛ́ɛo nán, sàt táŋ-lǎai lào dai dâai rúu jɛ̂ɛŋ lɛ́ɛo, pǒn hɛ̀ŋ bun an kâa-pá-jâao dâai hâi lɛ́ɛo gɛ̀ɛ sàt táŋ-lǎai lào nán,',
                'english': (
                    "Those who have come to know well what has been done — to "
                    "them the fruit of merit has been given by me."
                ),
            },
            # ‼ CORRECTED: thai  อนุโมทนาเกิด → อนุโมทนาเถิด. The old entry
            #              read เกิด from the paste and flagged that เถิด was
            #              expected as a hortative. The page prints เถิด.
            # ‼ CORRECTED: thai  ผู้ทรง เทวฤทธานุภาพ → ผู้ทรงเทวฤทธานุภาพ.
            #              Broken by the page's line wrap, not a space.
            # ‼ CORRECTED: paiboon  gə̀ət → tə̀ət. Follows the เถิด correction.
            {
                'number': 6,
                'pali': 'เย จะ ตัตถะ นะ ชานันติ, เทวา เตสัง นิเวทะยุง.',
                'pali_roman': 'ye ca tattha na jānanti, devā tesaṃ nivedayuṃ.',
                'thai': 'สัตว์ทั้งหลายเหล่าใดที่ยังไม่รู้ซึ่งผลแห่งบุญนั้น มีอยู่แล้วไซร้, ขอเทพเจ้าผู้ทรงเทวฤทธานุภาพทั้งหลาย, พึงบอกแก่สัตว์เหล่านั้น ให้รู้แล้วและอนุโมทนาเถิด,',
                'paiboon': 'sàt táŋ-lǎai lào dai tîi yaŋ mâi rúu sʉ̂ŋ pǒn hɛ̀ŋ bun nán mii yùu lɛ́ɛo sái, kɔ̌ɔ têep-pá-jâao pûu soŋ tee-wá-rít-taa-nú-pâap táŋ-lǎai, pʉŋ bɔ̀ɔk gɛ̀ɛ sàt lào nán hâi rúu lɛ́ɛo lɛ́ à-nú-moo-tá-naa tə̀ət,',
                'english': (
                    "And if there be those who do not know of it, may the "
                    "devas, bearing their divine might, announce it to those "
                    "beings, that they may know and rejoice."
                ),
            },
            # ‼ CORRECTED: thai  ดำรงอยู่ ด้วยอาหาร → ดำรงอยู่ด้วยอาหาร.
            #              Broken by the page's line wrap, not a space.
            {
                'number': 7,
                'pali': 'สัพเพ โลกัมหิ เย สัตตา, ชีวันตาหาระเหตุกา,',
                'pali_roman': 'sabbe lokamhi ye sattā, jīvantāhārahetukā,',
                'thai': 'สัตว์ทั้งหลายในโลกสันนิวาส บรรดาที่มีอาหารเป็นเหตุ, ย่อมเป็นอยู่และดำรงอยู่ด้วยอาหาร เป็นเครื่องหล่อเลี้ยงรูปกายนี้แล้ว,',
                'paiboon': 'sàt táŋ-lǎai nai lôok sǎn-ní-wâat ban-daa tîi mii aa-hǎan bpen hèet, yɔ̂m bpen yùu lɛ́ dam-roŋ yùu dûay aa-hǎan bpen krʉ̂aŋ lɔ̀ɔ líaŋ rûup-bpà-gaai níi lɛ́ɛo,',
                'english': (
                    "All beings in this world of dwelling together, all who "
                    "have nutriment as their cause, who live and are sustained "
                    "by food as that which nourishes this bodily form,"
                ),
            },
            # Page 220 ends here. Verified against IMG_0491.PNG (page 221),
            # which carries the closing line and then begins
            # คำแผ่เมตตาให้แก่ตนเอง.
            #
            # ‼ RESOLVED: the old note asked whether a ฯ closes the chant and
            #             whether the final Thai line really ends unpunctuated.
            #             The page prints เจตะสาติ. with a full stop and no ฯ,
            #             and ends the Thai ฉะนี้แล. with a full stop.
            {
                'number': 8,
                'page': 221,
                'pali': 'มะนุญญัง โภชะนัง สัพเพ, ละภันตุ มะมะ เจตะสาติ.',
                'pali_roman': 'manuññaṃ bhojanaṃ sabbe, labhantu mama cetasāti.',
                'thai': 'สัตว์ทั้งหลายทั้งหมดเหล่านั้น, จงเป็นผู้ได้ซึ่งโภชนะอันอุดมประณีต, เป็นที่เจริญแห่งจิต สำเร็จด้วยบุญฤทธิ์ ตามจิตของข้าพเจ้าจำนงเกื้อหนุนซึ่งความสุขประโยชน์ ด้วยประการฉะนี้แล.',
                'paiboon': 'sàt táŋ-lǎai táŋ-mòt lào nán, joŋ bpen pûu dâai sʉ̂ŋ poo-chá-ná an ù-dom bprà-nîit, bpen tîi jà-rəən hɛ̀ŋ jìt sǎm-rèt dûay bun-yá-rít dtaam jìt kɔ̌ɔŋ kâa-pá-jâao jam-noŋ gʉ̂a-nǔn sʉ̂ŋ kwaam sùk bprà-yòot dûay bprà-gaan chà-níi lɛɛ.',
                'english': (
                    "may all those beings obtain food that is excellent and "
                    "refined, food that gladdens the mind, accomplished by the "
                    "power of merit, according to my own intention in support "
                    "of their welfare and happiness. So it is."
                ),
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
        'book_number': 3,
        'page_start': 22,
        'layout': 'prose',
        'source_printed': 'องฺ เอกาทสก. 24/370-371',

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
        #          line breaks whatever. Every division into twenty verse
        #          lines of two pādas each is mine, made at the metrical
        #          boundaries the repeated refrain makes visible. The stanza
        #          count of ten is therefore also my inference. This affects
        #          every verse and is the most important thing to check
        #          against the page.
        # ‼ CHECK: No invitation line is present. I have not written one.
        # ‼ CHECK: source left empty. The book text you pasted gives no
        #          footnote or attribution. I have not supplied a reference.
        # Verified against IMG_0285.PNG (page 23) on 2026-08-08. The whole
        # chant fits on that one page: twenty lines set in two columns, two
        # pādas to a line read left column then right, then the นิฏฐิตา
        # formula and a footnote. The pāda pairing is confirmed correct.
        # ‼ RESOLVED: the 'stray double quotation mark' after ทุพภะตีติ. is a
        #             superscript footnote marker, not punctuation. Removed,
        #             and the footnote it points to is now the source.
        # ‼ RESOLVED: the ten-stanza count was right — twenty printed lines,
        #             each stanza closing on the โย มิตตานัง refrain.
        # ‼ RESOLVED: the section heading previously in this entry was my
        #             grouping. The page prints none; it has been removed.
        # ‼ CORRECTED: pali ปูชั่ง → ปูชัง (pūjàṃ → pūjaṃ). The mai ek was a
        #              paste artefact; the page prints ปูชัง.
        # ‼ CORRECTED: pali นิโครระมิวะ → นิโค์รธะมิวะ (nigorraramiva →
        #              nigrodhamiva). The page prints นิโค์รธะมิวะ, giving
        #              'like a banyan tree' — which the simile requires.
        # ‼ RESOLVED: วิรุฬหะ, not วิรุพหะ. The photograph could not separate
        #             พ from ฬ at that size; Josh read it off the physical book
        #             on 2026-08-08 and confirmed ฬ, which is what the entry
        #             already had. Nothing changed — the line is now settled
        #             rather than merely unchallenged.
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
        # Footnote printed at the foot of page 23.
        'source': 'ขุ.ชา. เตมิย. 401/154',
        'group': 'General chanting',
        'page_start': 23,

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
                'number': 1,
                'pali': 'พะหุตัพภักโข ภะวะติ วิปปะวุตโถ สะกัง ฆะรา',
                'pali_roman': 'bahutabbhakkho bhavati vippavuttho sakaṃ gharā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "He has abundant food, though dwelling far from his own "
                    "house;"
                ),
            },
            {
                'number': 2,
                'pali': 'พะหูนัง อุปะชีวันติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'bahūnaṃ upajīvanti yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "many live in dependence upon him — he who does not "
                    "betray his friends."
                ),
            },
            {
                'number': 3,
                'pali': 'ยัง ยัง ชะนะปะทัง ยาติ นิคะเม ราชะธานิโย',
                'pali_roman': 'yaṃ yaṃ janapadaṃ yāti nigame rājadhāniyo',
                'thai': '',
                'paiboon': '',
                'english': (
                    "To whatever country he goes, to market towns or royal "
                    "cities,"
                ),
            },
            {
                'number': 4,
                'pali': 'สัพพัตถะ ปูชิโต โหติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'sabbattha pūjito hoti yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "everywhere he is honoured — he who does not betray his "
                    "friends."
                ),
            },
            {
                'number': 5,
                'pali': 'นาสสะ โจรา ปะสะหันติ นาติมัญเญติ ขัตติโย',
                'pali_roman': 'nāssa corā pasahanti nātimaññeti khattiyo',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Thieves do not overpower him, the noble does not "
                    "despise him,"
                ),
            },
            {
                'number': 6,
                'pali': 'สัพเพ อะมิตเต ตะระติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'sabbe amitte tarati yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "he overcomes all enemies — he who does not betray his "
                    "friends."
                ),
            },
            # ‼ CHECK: สะฆะรัง transliterated faithfully as sagharaṃ. Some
            #          editions read สะคะรัง or set it as สะ ฆะรัง. Kept as
            #          printed.
            {
                'number': 7,
                'pali': 'อะกุทโธ สะฆะรัง เอติ สะภายะ ปะฏินันทิโต',
                'pali_roman': 'akuddho sagharaṃ eti sabhāya paṭinandito',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Unangered he comes to his home, he is welcomed in the "
                    "assembly,"
                ),
            },
            {
                'number': 8,
                'pali': 'ญาตีนัง อุตตะโม โหติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'ñātīnaṃ uttamo hoti yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "he is foremost among his kin — he who does not betray "
                    "his friends."
                ),
            },
            {
                'number': 9,
                'pali': 'สักกัต์วา สักกะโต โหติ คะรุ โหติ สะคาระโว',
                'pali_roman': 'sakkatvā sakkato hoti garu hoti sagāravo',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Having honoured, he is honoured, being reverent, he is "
                    "held in respect,"
                ),
            },
            {
                'number': 10,
                'pali': 'วัณณะกิตติภะโต โหติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'vaṇṇakittibhato hoti yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "he bears praise and renown — he who does not betray his "
                    "friends."
                ),
            },
            # ‼ CHECK: ปูชั่ง carries mai ek, which does not occur in Pali
            #          written in Thai script; the word is ปูชัง (pūjaṃ).
            #          Transliterated faithfully as pūjàṃ with the tone mark
            #          shown, rather than substituting. Almost certainly a
            #          mistyping and one of the clearest errors in the chant.
            {
                'number': 11,
                'pali': 'ปูชะโก ละภะเต ปูชัง วันทะโก ปะฏิวันทะนัง',
                'pali_roman': 'pūjako labhate pūjaṃ vandako paṭivandanaṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Honouring, he obtains honour, saluting, he receives "
                    "salutation,"
                ),
            },
            {
                'number': 12,
                'pali': 'ยะโสกิตติญจะ ปัปโปติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'yasokittiñca pappoti yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "he attains fame and renown — he who does not betray his "
                    "friends."
                ),
            },
            # ‼ CHECK: อัคคิยะถา is printed solid, where the sense requires
            #          อัคคิ ยะถา, fire as. Reproduced as pasted; check whether
            #          the book separates them.
            {
                'number': 13,
                'pali': 'อัคคิยะถา ปัชชะละติ เทวะตาวะ วิโรจะติ',
                'pali_roman': 'aggiyathā pajjalati devatāva virocati',
                'thai': '',
                'paiboon': '',
                'english': (
                    "He blazes forth as does a fire, he shines as does a "
                    "deva,"
                ),
            },
            # ‼ CHECK: อัชชะหิโต transliterated faithfully as ajjahito.
            #          Standard editions read อะชะหิโต (ajahito), not forsaken,
            #          with a single ช. Kept as printed.
            {
                'number': 14,
                'pali': 'สิริยา อัชชะหิโต โหติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'siriyā ajjahito hoti yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "he is not forsaken by good fortune — he who does not "
                    "betray his friends."
                ),
            },
            {
                'number': 15,
                'pali': 'คาโว ตัสสะ ปะชายันติ เขตเต วุตตัง วิรูหะติ',
                'pali_roman': 'gāvo tassa pajāyanti khette vuttaṃ virūhati',
                'thai': '',
                'paiboon': '',
                'english': (
                    "His cattle bear their young, what is sown in the field "
                    "grows up,"
                ),
            },
            # ‼ CHECK: ผะละมัสนาติ transliterated faithfully as phalamasnāti.
            #          Standard editions read ผะละมัสนาติ or ผะละมัสสะนาติ
            #          (phalamasnāti / phalamassanāti); the printed form is
            #          retained rather than adjusted.
            {
                'number': 16,
                'pali': 'วุตตานัง ผะละมัสนาติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'vuttānaṃ phalamasnāti yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "he enjoys the fruit of what was sown — he who does not "
                    "betray his friends."
                ),
            },
            # ‼ CHECK: ทะริโต transliterated faithfully as darito. Standard
            #          editions read ทะริโต from darī, a cleft or chasm.
            #          Flagged because the sense depends on it and the English
            #          I supplied assumes that reading.
            {
                'number': 17,
                'pali': 'ทะริโต ปัพพะตาโต วา รุกขะโต ปะติโต นะโร',
                'pali_roman': 'darito pabbatāto vā rukkhato patito naro',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Fallen from a chasm or a mountain, or a man fallen from "
                    "a tree,"
                ),
            },
            {
                'number': 18,
                'pali': 'จุโต ปะติฏฐัง ละภะติ โย มิตตานัง นะ ทุพภะติ.',
                'pali_roman': 'cuto patiṭṭhaṃ labhati yo mittānaṃ na dubbhati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "though he fall, he finds a footing — he who does not "
                    "betray his friends."
                ),
            },
            # ‼ CHECK: วิรุฬหะมูละสันตานัง and its simile run across verses
            #          19–20, but the Pali order places the banyan's roots
            #          first and the wind second, while my English inverts them
            #          for sense. The pairing is by meaning; the Pali order is
            #          the book's. (The verse numbers read 37–38 here until the
            #          pādas were joined two to a line; the note itself stands.)
            # ‼ RESOLVED: Josh read this line off the physical book on
            #             2026-08-08. It is วิรุฬหะ with ฬ — the พ the
            #             photograph seemed to show was the camera, not the
            #             page. The reading below was already right.
            {
                'number': 19,
                'pali': 'วิรุฬหะมูละสันตานัง นิโค์รธะมิวะ มาลุโต',
                'pali_roman': 'viruḷhamūlasantānaṃ nigrodhamiva māluto',
                'thai': '',
                'paiboon': '',
                'english': (
                    "As the wind cannot overpower a banyan whose spreading "
                    "roots have grown,"
                ),
            },
            # ‼ RESOLVED: the 'stray double quotation mark' after ทุพภะตีติ.
            #             was a superscript footnote marker, not punctuation —
            #             see the chant-level note. It has been removed and the
            #             footnote it pointed at is this chant's `source`.
            {
                'number': 20,
                'pali': 'อะมิตตา นัปปะสะหันติ โย มิตตานัง นะ ทุพภะตีติ.',
                'pali_roman': 'amittā nappasahanti yo mittānaṃ na dubbhatīti.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "so enemies do not overpower him — he who does not "
                    "betray his friends."
                ),
            },
            {
                'number': 21,
                'pali': 'เมตตานิสังสะคาถา นิฏฐิตา.',
                'pali_roman': 'mettānisaṃsagāthā niṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The verses on the benefits of loving-kindness are "
                    "ended."
                ),
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
        'page_start': 217,

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
            'pali': 'หันทะ มะยัง ท์วัตติงสาการะปาฐัง ภะณามะ เส.',
            'pali_roman': 'handa mayaṃ dvattiṃsākārapāṭhaṃ bhaṇāma se.',
            'thai': '',
            'paiboon': '',
            'english': 'Now let us recite the passage on the thirty-two parts.',
        },

        'verses': [
            # Verified against IMG_0487.PNG (page 217) and IMG_0488.PNG
            # (page 218) on 2026-08-08.
            #
            # ‼ RESOLVED: the thirty-two parts are set in two columns, one
            #             part per cell, read left cell then right cell.
            #             That gives the canonical order throughout. The
            #             old notes at ยะกะนัง / ปิหะกัง / อันตัง saying
            #             'kept as printed, standard editions differ' were
            #             reading the columns down instead of across.
            # ‼ RESOLVED: parts 1-10 were grouped two to a verse (โลมา นะขา,
            #             ทันตา ตะโจ …) because the grouping crossed the
            #             column boundary. Each part is its own cell on the
            #             page and is now its own line.
            # ‼ CORRECTED: verse 3 pali อะโฮ → อะโธ (aho → adho). The page
            #              prints อะโธ, as the Thai เบื้องต่ำ requires. The
            #              old note called this the clearest error in the
            #              chant and it is now settled from the page.
            # ‼ CORRECTED: closing line pali ป่าทะตะลา → ปาทะตะลา. The mai
            #              ek was a paste artefact; the page prints ปาทะตะลา,
            #              matching the same line in the opening.
            # ‼ CHECK: the page prints เขโพ (khepo) for the twenty-eighth part
            #          where standard editions read เขโฬ (kheḷo, saliva). The
            #          Thai gloss น้ำลาย is right either way. Reproduced as the
            #          page prints it; the พ/ฬ swap looks like a reprint fault.
            # ‼ CHECK: verse 5 Thai reads ต่างๆ with the mai yamok. The
            #          Paiboon+ renders the repetition in full as dtàaŋ dtàaŋ,
            #          consistent with the treatment of นั้น ๆ elsewhere.
            # ‼ CHECK: verse 6 อิมัส์มิง carries thanthakhat over ส์.
            #          Transliterated as imasmiṃ, the standard form; the mark
            #          placement varies across this book.
            {
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
            {
                'number': 3,
                'pali': 'อะโธ เกสะมัตถะกา,',
                'pali_roman': 'adho kesamatthakā,',
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
            {
                'number': 5,
                'pali': 'ปูโร นานัปปะการัสสะ อะสุจิโน,',
                'pali_roman': 'pūro nānappakārassa asucino,',
                'thai': 'เต็มไปด้วยของไม่สะอาด มีประการต่างๆ',
                'paiboon': 'dtem bpai dûay kɔ̌ɔŋ mâi sà-àat mii bprà-gaan dtàaŋ dtàaŋ',
                'english': 'full of impurities of various kinds.',
            },
            {
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
            {
                'number': 8,
                'pali': 'โลมา',
                'pali_roman': 'lomā',
                'thai': 'ขนทั้งหลาย,',
                'paiboon': 'kǒn táŋ-lǎai,',
                'english': 'hairs of the body,',
            },
            {
                'number': 9,
                'pali': 'นะขา',
                'pali_roman': 'nakhā',
                'thai': 'เล็บทั้งหลาย,',
                'paiboon': 'lép táŋ-lǎai,',
                'english': 'nails,',
            },
            {
                'number': 10,
                'pali': 'ทันตา',
                'pali_roman': 'dantā',
                'thai': 'ฟันทั้งหลาย,',
                'paiboon': 'fan táŋ-lǎai,',
                'english': 'teeth,',
            },
            {
                'number': 11,
                'pali': 'ตะโจ',
                'pali_roman': 'taco',
                'thai': 'หนัง,',
                'paiboon': 'nǎŋ,',
                'english': 'skin,',
            },
            {
                'number': 12,
                'pali': 'มังสัง',
                'pali_roman': 'maṃsaṃ',
                'thai': 'เนื้อ,',
                'paiboon': 'nʉ́a,',
                'english': 'flesh,',
            },
            {
                'number': 13,
                'pali': 'นะหารู',
                'pali_roman': 'nahārū',
                'thai': 'เอ็นทั้งหลาย,',
                'paiboon': 'en táŋ-lǎai,',
                'english': 'sinews,',
            },
            {
                'number': 14,
                'pali': 'อัฏฐี',
                'pali_roman': 'aṭṭhī',
                'thai': 'กระดูกทั้งหลาย,',
                'paiboon': 'grà-dùuk táŋ-lǎai,',
                'english': 'bones,',
            },
            {
                'number': 15,
                'pali': 'อัฏฐิมิญชัง',
                'pali_roman': 'aṭṭhimiñjaṃ',
                'thai': 'เยื่อในกระดูก,',
                'paiboon': 'yʉ̂a nai grà-dùuk,',
                'english': 'marrow of the bones,',
            },
            {
                'number': 16,
                'pali': 'วักกัง',
                'pali_roman': 'vakkaṃ',
                'thai': 'ไต,',
                'paiboon': 'dtai,',
                'english': 'kidney,',
            },
            {
                'number': 17,
                'page': 218,
                'pali': 'หะทะยัง',
                'pali_roman': 'hadayaṃ',
                'thai': 'หัวใจ,',
                'paiboon': 'hǔa-jai,',
                'english': 'heart,',
            },
            {
                'number': 18,
                'pali': 'ยะกะนัง',
                'pali_roman': 'yakanaṃ',
                'thai': 'ตับ,',
                'paiboon': 'dtàp,',
                'english': 'liver,',
            },
            {
                'number': 19,
                'pali': 'กิโลมะกัง',
                'pali_roman': 'kilomakaṃ',
                'thai': 'พังผืด,',
                'paiboon': 'paŋ-pʉ̀ʉt,',
                'english': 'membranes,',
            },
            {
                'number': 20,
                'pali': 'ปิหะกัง',
                'pali_roman': 'pihakaṃ',
                'thai': 'ม้าม,',
                'paiboon': 'máam,',
                'english': 'spleen,',
            },
            {
                'number': 21,
                'pali': 'ปัปผาสัง',
                'pali_roman': 'papphāsaṃ',
                'thai': 'ปอด,',
                'paiboon': 'bpɔ̀ɔt,',
                'english': 'lungs,',
            },
            {
                'number': 22,
                'pali': 'อันตัง',
                'pali_roman': 'antaṃ',
                'thai': 'ไส้ใหญ่,',
                'paiboon': 'sâi yài,',
                'english': 'large intestine,',
            },
            {
                'number': 23,
                'pali': 'อันตะคุณัง',
                'pali_roman': 'antaguṇaṃ',
                'thai': 'ไส้น้อย,',
                'paiboon': 'sâi nɔ́ɔy,',
                'english': 'small intestine,',
            },
            {
                'number': 24,
                'pali': 'อุทะริยัง',
                'pali_roman': 'udariyaṃ',
                'thai': 'อาหารใหม่,',
                'paiboon': 'aa-hǎan mài,',
                'english': 'undigested food,',
            },
            {
                'number': 25,
                'pali': 'กะรีสัง',
                'pali_roman': 'karīsaṃ',
                'thai': 'อาหารเก่า,',
                'paiboon': 'aa-hǎan gào,',
                'english': 'digested food,',
            },
            {
                'number': 26,
                'pali': 'ปิตตัง',
                'pali_roman': 'pittaṃ',
                'thai': 'น้ำดี,',
                'paiboon': 'nám dii,',
                'english': 'bile,',
            },
            {
                'number': 27,
                'pali': 'เสมหัง',
                'pali_roman': 'semhaṃ',
                'thai': 'น้ำเสลด,',
                'paiboon': 'nám sà-lèet,',
                'english': 'phlegm,',
            },
            {
                'number': 28,
                'pali': 'ปุพโพ',
                'pali_roman': 'pubbo',
                'thai': 'น้ำหนอง,',
                'paiboon': 'nám nɔ̌ɔŋ,',
                'english': 'pus,',
            },
            {
                'number': 29,
                'pali': 'โลหิตัง',
                'pali_roman': 'lohitaṃ',
                'thai': 'น้ำเลือด,',
                'paiboon': 'nám lʉ̂at,',
                'english': 'blood,',
            },
            {
                'number': 30,
                'pali': 'เสโท',
                'pali_roman': 'sedo',
                'thai': 'น้ำเหงื่อ,',
                'paiboon': 'nám ŋʉ̀a,',
                'english': 'sweat,',
            },
            {
                'number': 31,
                'pali': 'เมโท',
                'pali_roman': 'medo',
                'thai': 'น้ำมันข้น,',
                'paiboon': 'nám-man kôn,',
                'english': 'solid fat,',
            },
            {
                'number': 32,
                'pali': 'อัสสุ',
                'pali_roman': 'assu',
                'thai': 'น้ำตา,',
                'paiboon': 'nám-dtaa,',
                'english': 'tears,',
            },
            {
                'number': 33,
                'pali': 'วะสา',
                'pali_roman': 'vasā',
                'thai': 'น้ำมันเหลว,',
                'paiboon': 'nám-man lěeo,',
                'english': 'liquid fat,',
            },
            {
                'number': 34,
                'pali': 'เขโพ',
                'pali_roman': 'khepo',
                'thai': 'น้ำลาย,',
                'paiboon': 'nám-laai,',
                'english': 'spittle,',
            },
            {
                'number': 35,
                'pali': 'สิงฆานิกา',
                'pali_roman': 'siṅghānikā',
                'thai': 'น้ำมูก,',
                'paiboon': 'nám-mûuk,',
                'english': 'mucus,',
            },
            {
                'number': 36,
                'pali': 'ละสิกา',
                'pali_roman': 'lasikā',
                'thai': 'น้ำไขข้อ,',
                'paiboon': 'nám kǎi kɔ̂ɔ,',
                'english': 'fluid of the joints,',
            },
            {
                'number': 37,
                'pali': 'มุตตัง',
                'pali_roman': 'muttaṃ',
                'thai': 'น้ำมูตร,',
                'paiboon': 'nám mûut,',
                'english': 'urine,',
            },
            {
                'number': 38,
                'pali': 'มัตถะเก มัตถะลุงคัง,',
                'pali_roman': 'matthake matthaluṅgaṃ,',
                'thai': 'เยื่อมันสมองในกะโหลกศีรษะ,',
                'paiboon': 'yʉ̂a man sà-mɔ̌ɔŋ nai gà-lòok sǐi-sà,',
                'english': 'and the brain within the skull.',
            },
            {
                'number': 39,
                'pali': 'เอวะมะยัง เม กาโย,',
                'pali_roman': 'evamayaṃ me kāyo,',
                'thai': 'กายของเรานี้อย่างนี้,',
                'paiboon': 'gaai kɔ̌ɔŋ rao níi yàaŋ níi,',
                'english': 'Thus is this body of mine,',
            },
            {
                'number': 40,
                'pali': 'อุทธัง ปาทะตะลา,',
                'pali_roman': 'uddhaṃ pādatalā,',
                'thai': 'เบื้องบนแต่พื้นเท้าขึ้นมา,',
                'paiboon': 'bʉ̂aŋ bon dtɛ̀ɛ pʉ́ʉn táo kʉ̂n maa,',
                'english': 'from the soles of the feet upward,',
            },
            {
                'number': 41,
                'pali': 'อะโธ เกสะมัตถะกา,',
                'pali_roman': 'adho kesamatthakā,',
                'thai': 'เบื้องต่ำแต่ปลายผมลงไป,',
                'paiboon': 'bʉ̂aŋ dtàm dtɛ̀ɛ bplaai pǒm loŋ bpai,',
                'english': 'from the crown of the hair downward,',
            },
            {
                'number': 42,
                'pali': 'ตะจะปะริยันโต,',
                'pali_roman': 'tacapariyanto,',
                'thai': 'มีหนังหุ้มอยู่เป็นที่สุดรอบ,',
                'paiboon': 'mii nǎŋ hûm yùu bpen tîi-sùt rɔ̂ɔp,',
                'english': 'bounded all round by skin,',
            },
            {
                'number': 43,
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
        # ‼ CHECK: source left empty. No footnote is visible in either crop.
        # Verified against IMG_0488.PNG (page 218) and IMG_0489.PNG (page
        # 219) on 2026-08-08. This chant is set ONE pāda to a line with its
        # Thai in the right-hand column beside it — NOT two pādas to a line
        # like the Tilokavijaya and Bhaddekaratta gāthās. A pāda-pairing pass
        # briefly joined these eight lines into four; that was wrong and has
        # been undone. The two-column layout in this book is not always two
        # pādas of Pali — here the right column is the translation.
        # ‼ RESOLVED: the crops did show the whole chant. It ends at
        #             ปะรินิพพุโต. on page 219, followed by คาถาโพธิบาท. No
        #             closing ฯ and no นิฏฐิตา formula.
        # ‼ RESOLVED: the two section headings previously in this entry were
        #             my grouping, are not printed on either page, and have
        #             been removed.
        # ‼ CHECK: This chant appeared in truncated typed form at the tail of
        #          your previous paste, and the two versions differ in two
        #          places — see the checks on verse 2. Where they differ
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
        'page_start': 218,

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
            # Page 218 ends here; the chant finishes on 219.
            {
                'number': 5,
                'page': 219,
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
        # ‼ CHECK: These verses were first entered one Pali pāda to a line.
        #          They are now paired two pādas to a line, which is how the
        #          book sets the Ariyadhanagāthā and the Pattidānagāthā. Only
        #          the line division changed — not a word, mark or space of
        #          the text itself. Confirm the pairing against the page.

        'id': 'pabbatopama-gatha',
        'title_thai': 'ปัพพะโตปะมะคาถา',
        'title_pali': 'Pabbatopamagāthā',
        # The book prints no separate romanised Thai title, so this
        # stays empty and the template falls back to `title_pali`.
        'title_roman': '',
        'title_english': 'The Verses on the Simile of the Mountain',
        'source': '',
        'group': 'General chanting',
        'book_number': 14,
        'page_start': 30,
        'source_printed': 'ส.ส. 15/148',

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
                'pali': 'ยะถาปิ เสลา วิปุลา นะภัง อาหัจจะ ปัพพะตา',
                'pali_roman': 'yathāpi selā vipulā nabhaṃ āhacca pabbatā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Just as vast rocks, mountains reaching to the sky,"
                ),
            },
            # ‼ CHECK: จะตุททิสา transliterated as catuddisā. Standard editions
            #          agree; flagged only because the preceding word
            #          นิปโปเถนตา is spelled variously across editions
            #          (nippothentā / nipphothentā) and the pair should be
            #          checked together.
            {
                'number': 2,
                'pali': 'สะมันตา อะนุปะริเยยยุง นิปโปเถนตา จะตุททิสา.',
                'pali_roman': 'samantā anupariyeyyuṃ nippothentā catuddisā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "should advance from every side, grinding down the four "
                    "quarters —"
                ),
            },
            {
                'section': 'ชะรา จะ มัจจุ จะ: Ageing and Death',
                'number': 3,
                'pali': 'เอวัง ชะรา จะ มัจจุ จะ อะธิวัตตันติ ปาณิโน',
                'pali_roman': 'evaṃ jarā ca maccu ca adhivattanti pāṇino',
                'thai': '',
                'paiboon': '',
                'english': (
                    "just so do ageing and death roll over living beings:"
                ),
            },
            # ‼ CHECK: พ์ราห์มะเณ carries thanthakhat over พ์ and ห์. Chant 4
            #          gave พ์รัห์มะจาริโน and the Mettānisaṃsasuttaṃ gave
            #          พรห์มะโลกูปะโค — three spellings of the same element
            #          across the book. Transliterated as brāhma- throughout.
            # ‼ CHECK: This line ends with no punctuation, where stanzas 1 and
            #          3 close with a full stop. Reproduced as pasted.
            {
                'number': 4,
                'pali': 'ขัตติเย พ์ราห์มะเณ เวสเส สุทเท จัณฑาละปุกกุเส',
                'pali_roman': 'khattiye brāhmaṇe vesse sudde caṇḍālapukkuse',
                'thai': '',
                'paiboon': '',
                'english': (
                    "nobles, brahmins, merchants, servants, outcastes and "
                    "refuse-workers."
                ),
            },
            {
                'number': 5,
                'pali': 'นะ กิญจิ ปะริวัชเชติ สัพพะเมวาภิมัททะติ',
                'pali_roman': 'na kiñci parivajjeti sabbamevābhimaddati',
                'thai': '',
                'paiboon': '',
                'english': (
                    "They spare nothing whatever, they crush down all alike."
                ),
            },
            # ‼ CHECK: หัตถี่นัง carries mai ek, again impossible in Pali; the
            #          word is หัตถีนัง (hatthīnaṃ). Reproduced as pasted. The
            #          same fault as verse 7 and as ป่าทะตะลา in the
            #          Dvattiṃsākāra — mai ek intruding into Pali is now a
            #          recurring fault in this source.
            # ‼ CHECK: The footnote line 1. ขุ.สุ. 25/360-361 2. ส.ส. 15/315-6
            #          is printed between this verse and the next, as a page-
            #          foot footnote falling where the page broke. I kept it
            #          out of the verses and put both references in the source
            #          field. Two markers are given but I cannot tell from the
            #          paste which lines carry them; check whether both belong
            #          to this chant.
            {
                'number': 6,
                'pali': 'นะ ตัตถะ หัตถีนัง ภูมิ นะ ระถานัง นะ ปัตติยา.',
                'pali_roman': 'na tattha hatthīnaṃ bhūmi na rathānaṃ na pattiyā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "There is no ground there for elephants, none for "
                    "chariots, none for infantry."
                ),
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
            # ‼ CHECK: ว่า carries mai ek, which does not occur in Pali written
            #          in Thai script; the word is วา (vā). Transliterated
            #          faithfully as vàa with the tone mark shown rather than
            #          substituted. Clear mistyping.
            {
                'number': 7,
                'page': 31,
                'pali': 'นะ จาปิ มันตะยุทเธนะ สักกา เชตุง ธะเนนะ วา',
                'pali_roman': 'na cāpi mantayuddhena sakkā jetuṃ dhanena vā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Nor yet by battle of spells, nor by wealth, can they be "
                    "conquered."
                ),
            },
            # ‼ CHECK: ตัสมา is written without thanthakhat. Chant 8 printed
            #          the same word both with and without the mark.
            #          Transliterated as tasmā either way.
            # ‼ CHECK: A full stop falls here, mid-stanza in the interleaved
            #          reading, after สัมปัสสัง อัตถะมัตตะโน. If the book
            #          punctuates by couplet rather than by stanza this is
            #          expected; if not, it may indicate my ordering is wrong.
            #          Worth checking alongside the ordering question.
            {
                'section': 'สัทธัง นิเวสะเย: Where Faith Is Placed',
                'number': 8,
                'pali': 'ตัส์มา หิ ปัณฑิโต โปโส สัมปัสสัง อัตถะมัตตะโน.',
                'pali_roman': 'tasmā hi paṇḍito poso sampassaṃ atthamattano.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Therefore a wise person, seeing what is good for "
                    "himself,"
                ),
            },
            {
                'number': 9,
                'pali': 'พุทเธ ธัมเม จะ สังเฆ จะ ธีโร สัทธัง นิเวสะเย',
                'pali_roman': 'buddhe dhamme ca saṅghe ca dhīro saddhaṃ nivesaye',
                'thai': '',
                'paiboon': '',
                'english': (
                    "in the Buddha, the Dhamma and the Saṅgha — let the "
                    "steadfast one settle his faith."
                ),
            },
            # ‼ CHECK: ธัมมะจาริ has a short final ิ where standard editions
            #          read ธัมมะจารี (dhammacārī). Transliterated faithfully
            #          as dhammacāri.
            {
                'number': 10,
                'pali': 'โย ธัมมะจารี กาเยนะ วาจายะ อุทะ เจตะสา',
                'pali_roman': 'yo dhammacārī kāyena vācāya uda cetasā',
                'thai': '',
                'paiboon': '',
                'english': (
                    "Whoever lives by Dhamma in body, in speech, or in mind,"
                ),
            },
            # ‼ CHECK: A stray apostrophe follows the full stop: ปะโมทะติ.'.
            #          The same artefact has now appeared at the close of
            #          chants 8, 9, the Mettānisaṃsasuttaṃ and the
            #          Mettānisaṃsagāthā. Five occurrences; reproduced as
            #          pasted rather than tidied.
            {
                'number': 11,
                'pali': 'อิเธวะ นัง ปะสังสันติ เปจจะ สัคเค ปะโมทะติ.',
                'pali_roman': 'idheva naṃ pasaṃsanti pecca sagge pamodati.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "him they praise here in this very life, and hereafter "
                    "he rejoices in heaven."
                ),
            },
            # ‼ CHECK: The closing formula ends with no full stop, where every
            #          other นิฏฐิตา line in the book has one. Reproduced as
            #          pasted.
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 12,
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
        'page_start': 31,
        'source_printed': 'อง. จตุกุก. 21/74 อง. ปัญจก. 22/59',

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
        'source': '',
        'group': 'General chanting',
        'book_number': 15,
        'page_start': 31,
        'layout': 'prose',
        'source_printed': 'ขุ.อุ. 25/74-5-6, วิ. มหา. 4/2-3-4',

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
                'pali': 'ชาติปัจจะยา ชะรามะระณัง โสกะปะริเทวะทุกขะโทมะนัสสุปายาสา สัมภะวันติ,',
                'pali_roman': 'jātipaccayā jarāmaraṇaṃ sokaparidevadukkhadomanassupāyāsā sambhavanti,',
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
                'pali': 'เอวะเมตัสสะ เกวะลัสสะ ทุกขักขันธัสสะ สะมุทะโย โหติ.',
                'pali_roman': 'evametassa kevalassa dukkhakkhandhassa samudayo hoti.',
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
                'page': 32,
                'pali': 'อะวิชชายะเต์ววะ อะเสสะวิราคะนิโรธา สังขาระนิโรโธ,',
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
                'pali': 'ผัสสะนิโรธา เวทะนานิโรโธ,',
                'pali_roman': 'phassanirodhā vedanānirodho,',
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
                'pali': 'ชาตินิโรธา ชะรามะระณัง โสกะปะริเทวะทุกขะโทมะนัสสุปายาสา นิรุชฌันติ,',
                'pali_roman': 'jātinirodhā jarāmaraṇaṃ sokaparidevadukkhadomanassupāyāsā nirujjhanti,',
                'thai': '',
                'paiboon': '',
                'english': (
                    "from the cessation of birth, ageing-and-death, sorrow, "
                    "lamentation, pain, grief and despair cease."
                ),
            },
            {
                'number': 24,
                'pali': 'เอวะเมตัสสะ เกวะลัสสะ ทุกขักขันธัสสะ นิโรโธ โหติ.',
                'pali_roman': 'evametassa kevalassa dukkhakkhandhassa nirodho hoti.',
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
        'page_start': 32,

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
                'pali': 'สูโรวะ โอภาสะยะมันตะลิกขันติ.',
                'pali_roman': 'sūrova obhāsayamantalikkhanti.',
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
        # ‼ CHECK: These verses were first entered one Pali pāda to a line.
        #          They are now paired two pādas to a line, which is how the
        #          book sets the Ariyadhanagāthā and the Pattidānagāthā. Only
        #          the line division changed — not a word, mark or space of
        #          the text itself. Confirm the pairing against the page.
        # ‼ CHECK: A bare 33 appears between verse 8 and the closing formula.
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
        'book_number': 16,
        'page_start': 33,
        'source_printed': 'ม.อุ. 14/348',

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
                'pali': 'อะตีตัง นาน์วาคะเมยยะ นัปปะฏิกังเข อะนาคะตัง',
                'pali_roman': 'atītaṃ nānvāgameyya nappaṭikaṅkhe anāgataṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "One should not run back after the past, nor place hope "
                    "in what has not yet come;"
                ),
            },
            # ‼ CHECK: ยะทะตีตัมปะหีนันตัง is printed solid, running together
            #          ยะทะตีตัง, ปะหีนัง and ตัง. Transliterated as one word
            #          following the print; confirm the book does not space it.
            {
                'number': 2,
                'pali': 'ยะทะตีตัมปะหีนันตัง อัปปัตตัญจะ อะนาคะตัง.',
                'pali_roman': 'yadatītampahīnantaṃ appattañca anāgataṃ.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "for what is past is left behind, and the future is not "
                    "yet arrived."
                ),
            },
            {
                'section': 'ปัจจุปปันนัง: Seeing the Present',
                'number': 3,
                'pali': 'ปัจจุปปันนัญจะ โย ธัมมัง ตัตถะ ตัตถะ วิปัสสะติ',
                'pali_roman': 'paccuppannañca yo dhammaṃ tattha tattha vipassati',
                'thai': '',
                'paiboon': '',
                'english': (
                    "But whoever sees the present state clearly, there in "
                    "each case as it is —"
                ),
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
                'number': 4,
                'pali': 'อะสังหิรัง อะสังกุปปัง ตัง วิทธา มะนุพ์รูหะเย.',
                'pali_roman': 'asaṃharaṃ asaṃkuppaṃ taṃ viddhā manubrūhaye',
                'thai': '',
                'paiboon': '',
                'english': (
                    "unshakeable, unwavering: knowing that, let him "
                    "cultivate it."
                ),
            },
            {
                'section': 'อัชเชวะ กิจจะมาตัปปัง: The Urgency of Today',
                'number': 5,
                'pali': 'อัชเชวะ กิจจะมาตัปปัง โก ชัญญา มะระณัง สุเว',
                'pali_roman': 'ajjeva kiccamātappaṃ ko jaññā maraṇaṃ suve',
                'thai': '',
                'paiboon': '',
                'english': (
                    "The effort is to be made this very day; who knows "
                    "whether death comes tomorrow?"
                ),
            },
            # ‼ CHECK: สังคะรันเตนะ transliterated as saṅgarantena. Standard
            #          editions read สงฺคราม- or สงฺคเรน in this line depending
            #          on recension, and the sense of bargaining with Death
            #          rests on the reading. Kept as printed.
            {
                'number': 6,
                'pali': 'นะ หิ โน สังคะรันเตนะ มะหาเสเนนะ มัจจุนา.',
                'pali_roman': 'na hi no saṅgarantena mahāsenena maccunā.',
                'thai': '',
                'paiboon': '',
                'english': (
                    "For there is no bargaining with Death and his great "
                    "army."
                ),
            },
            # ‼ CHECK: วิหาริมาตาปิง is printed solid, a sandhi of วิหาริง
            #          อาตาปิง. Transliterated as vihārimātāpiṃ. Some editions
            #          read วิหารึ (vihāriṃ) with nikkhahit; the printed form
            #          is retained.
            {
                'section': 'ภัทเทกะรัตโต: The Auspicious Single Night',
                'number': 7,
                'pali': 'เอวัง วิหาริมาตาปิง อะโหรัตตะมะตันทิตัง',
                'pali_roman': 'evaṃ vihārimātāpiṃ ahorattamatanditaṃ',
                'thai': '',
                'paiboon': '',
                'english': (
                    "One who dwells thus, ardent, untiring by day and by "
                    "night —"
                ),
            },
            # ‼ CHECK: A stray apostrophe follows the full stop: มุนีติ.'. The
            #          artefact has now appeared at the close of seven chants
            #          in this run. Reproduced as pasted rather than tidied.
            {
                'number': 8,
                'pali': 'ตัง เว ภัทเทกะรัตโตติ สันโต อาจิกขะเต มุนีติ.',
                'pali_roman': "taṃ ve bhaddekarattoti santo ācikkhate munīti.'",
                'thai': '',
                'paiboon': '',
                'english': (
                    "him indeed, as one of the auspicious single night, the "
                    "peaceful sage declares."
                ),
            },
            # ‼ CHECK: The closing formula ends with no full stop, as with
            #          chants 14 and 15. Reproduced as pasted.
            {
                'section': 'นิฏฐิตา: The Closing Formula',
                'number': 9,
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
        'title_roman': 'kam buu-chaa prá-rát-dtà-ná-dtrai',
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
        'title_roman': 'kam ná-mát-sà-gaan prá-rát-dtà-ná-dtrai',
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
        'title_roman': 'kam chəən buu-chaa lɛ́ sùat ná-moo',
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
        'title_pali': 'Ratanattayappaṇāmagāthā',
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
        'title_pali': 'Saṃvegaparikittanapāṭha',
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
        'title_pali': 'Taṅkhaṇikapaccavekkhaṇapāṭho',
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
        'title_pali': 'Pattidānagāthā',
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
        'title_roman': 'kam bprà-gàat u-boo-sòt',
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
        'title_roman': 'kam aa-râat-tá-naa u-boo-sòt-sǐin',
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
        'title_roman': 'u-boo-sòt-sǐin',
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
                'printed_number': 1,
                'pali': 'ปาณาติปาตา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'pāṇātipātā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from taking life.',
            },
            {
                'number': 2,
                'printed_number': 2,
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
                'printed_number': 3,
                'pali': 'อะพ์รัห์มะจะริยา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'abrahmacariyā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from unchastity.',
            },
            {
                'number': 4,
                'printed_number': 4,
                'pali': 'มุสาวาทา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'musāvādā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from false speech.',
            },
            {
                'number': 5,
                'printed_number': 5,
                'pali': 'สุราเมระยะมัชชะปะมาทัฏฐานา เวระมะณี สิกขาปะทัง สะมาทิยามิ.',
                'pali_roman': 'surāmerayamajjapamādaṭṭhānā veramaṇī sikkhāpadaṃ samādiyāmi.',
                'thai': '',
                'paiboon': '',
                'english': 'I undertake the training rule to abstain from distilled and fermented drink, which is the basis of heedlessness.',
            },
            {
                'number': 6,
                'printed_number': 6,
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
                'printed_number': 7,
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
                'printed_number': 8,
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
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0276.PNG]: The book prints NO title for this line. The
        #   id and English title are mine; title_thai and title_pali are left
        #   empty rather than invented. It is set as its own chant because the
        #   book separates it from what follows with a prose instruction, and
        #   because Pali cannot live in a page block — blocks carry Thai and
        #   English only.
        # ‼ CHECK [IMG_0276.PNG]: Pali only — no Thai translation is printed
        #   anywhere on page 13, so thai and paiboon are empty throughout and
        #   english_unverified is set.
        'id': 'imani-attha-sikkhapadani',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Charge to Guard the Eight Precepts',
        'page_start': 13,
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
            # ‼ CHECK [IMG_0276.PNG]: 'กัต๎วา' carries the yamakkan mark ๎,
            #   reproduced as printed rather than normalised to กัตวา. Same
            #   word and same treatment as on page 10.
            {
                'number': 1,
                'pali': 'อิมานิ อัฏฐะ สิกขาปะทานิ อุโปสะถะสีละวะเสนะ สาธุกัง กัต๎วา อัปปะมาเทนะ รักขิตัพพานิ.',
                'pali_roman': 'imāni aṭṭha sikkhāpadāni uposathasīlavasena sādhukaṃ katvā appamādena rakkhitabbāni.',
                'thai': '',
                'paiboon': '',
                'english': 'These eight training rules, well undertaken as the virtue of the Uposatha, are to be guarded with heedfulness.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0276.PNG]: The book prints no title. The id and English
        #   title are mine. This is the well-known two-line gatha on sila,
        #   spoken by the elder after the assembly's āma bhante.
        'id': 'silena-sugatim-yanti',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Verse on Virtue',
        'page_start': 13,
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
            # ‼ CHECK [IMG_0276.PNG]: TWO COLUMNS — first pairing, for you to
            #   confirm against the page. Left half 'สีเลนะ สุคะติง ยันติ'
            #   joined to right half 'สีเลนะ โภคะสัมปะทา' as ONE verse. The
            #   honest test passes: the left column alone reads as unfinished
            #   half-lines, so the right column completes them.
            {
                'number': 1,
                'pali': 'สีเลนะ สุคะติง ยันติ สีเลนะ โภคะสัมปะทา',
                'pali_roman': 'sīlena sugatiṃ yanti sīlena bhogasampadā',
                'thai': '',
                'paiboon': '',
                'english': 'By virtue beings go to a good destination; by virtue is prosperity attained;',
            },
            # ‼ CHECK [IMG_0276.PNG]: 'ตัส๎มา' carries the yamakkan mark ๎,
            #   reproduced as printed rather than normalised to ตัสมา.
            {
                'number': 2,
                'pali': 'สีเลนะ นิพพุติง ยันติ ตัส๎มา สีลัง วิโสธะเย.',
                'pali_roman': 'sīlena nibbutiṃ yanti tasmā sīlaṃ visodhaye.',
                'thai': '',
                'paiboon': '',
                'english': 'by virtue they go to peace. Therefore let virtue be purified.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0276.PNG]: The invitation 'หันทะ มะยัง
        #   สะระณะคะมะนานุสสะระณะคาถาโย ภะณามะ เส.' IS printed, but inside the
        #   prose paragraph above rather than on its own line. It is left in
        #   that block and the invitation field left empty, so the page does
        #   not print it twice. Say if you would rather it were lifted into
        #   the field.
        # ‼ CHECK [IMG_0276.PNG]: The book prints the title in Thai script
        #   only. title_pali carries the IAST form and title_roman is left
        #   empty, per the rule for a title that is Pali written in Thai
        #   script.
        'id': 'sarana-gamananussarana-gatha',
        'title_thai': 'สะระณะคะมะนานุสสะระณะคาถา',
        'title_pali': 'Saraṇagamanānussaraṇagāthā',
        'title_roman': '',
        'title_english': 'Verses Recollecting the Going for Refuge',
        'page_start': 13,
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
            # ‼ CHECK [IMG_0276.PNG]: TWO COLUMNS — first pairing, for you to
            #   confirm against the page. Left half 'อะหัง พุทธัญจะ ธัมมัญจะ'
            #   joined to right half 'สังฆัญจะ สะระณัง คะโต' as ONE verse. The
            #   honest test passes: the left column alone reads as unfinished
            #   half-lines. All six verses are read the same way.
            # ‼ CHECK [IMG_0276.PNG]: Footnote marker 1 sits on คะโต at the
            #   end of this verse. The footnote is an EDITORIAL note about the
            #   gendered form (คะโต for a layman, คะตา for a laywoman), not a
            #   citation, so it is carried as a page footnote block and NOT as
            #   source_printed.
            {
                'number': 1,
                'pali': 'อะหัง พุทธัญจะ ธัมมัญจะ สังฆัญจะ สะระณัง คะโต',
                'pali_roman': 'ahaṃ buddhañca dhammañca saṅghañca saraṇaṃ gato',
                'thai': '',
                'paiboon': '',
                'english': 'I have gone to the Buddha, the Dhamma and the Saṅgha as refuge,',
            },
            # ‼ CHECK [IMG_0276.PNG]: Footnote marker 2 sits on อุปาสะกัตตัง
            #   at the start of this verse — the second footnote on the page,
            #   also an editorial note about the gendered form.
            {
                'number': 2,
                'pali': 'อุปาสะกัตตัง เทเสสิง ภิกขุสังฆัสสะ สัมมุขา.',
                'pali_roman': 'upāsakattaṃ desesiṃ bhikkhusaṅghassa sammukhā.',
                'thai': '',
                'paiboon': '',
                'english': 'and declared myself a lay follower in the presence of the Saṅgha of bhikkhus.',
            },
            {
                'number': 3,
                'pali': 'เอตัง เม สะระณัง เขมัง เอตัง สะระณะมุตตะมัง',
                'pali_roman': 'etaṃ me saraṇaṃ khemaṃ etaṃ saraṇamuttamaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'This is my safe refuge, this is the supreme refuge;',
            },
            {
                'number': 4,
                'pali': 'เอตัง สะระณะมาคัมมะ สัพพะทุกขา ปะมุจจะเย',
                'pali_roman': 'etaṃ saraṇamāgamma sabbadukkhā pamuccaye',
                'thai': '',
                'paiboon': '',
                'english': 'coming to this refuge, one is freed from all suffering.',
            },
            {
                'number': 5,
                'pali': 'ยะถาพะลัง จะเรยยาหัง สัมมาสัมพุทธะสาสะนัง',
                'pali_roman': 'yathābalaṃ careyyāhaṃ sammāsambuddhasāsanaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'As far as my strength allows, may I practise the teaching of the Perfectly Self-Awakened One,',
            },
            # ‼ CHECK [IMG_0276.PNG]: SPELLING, needs the physical page. The
            #   book appears to print 'ทุกะนิสสะระณัสเสวะ' where standard
            #   editions read 'ทุกขะนิสสะระณัสเสวะ' (dukkha-, with the doubled
            #   kh). I have reproduced what I read and romanised it faithfully
            #   as 'dukanissaraṇasseva' rather than silently correcting it to
            #   the standard form. Either the book differs here or I have
            #   misread the photograph — please check.
            {
                'number': 6,
                'pali': 'ทุกะนิสสะระณัสเสวะ ภาคี อัสสัง อะนาคะเต.',
                'pali_roman': 'dukanissaraṇasseva bhāgī assaṃ anāgate.',
                'thai': '',
                'paiboon': '',
                'english': 'and may I share in the escape from suffering in time to come.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0277.PNG]: SINGLE COLUMN, checked deliberately because
        #   page 13 was two-column throughout and the switch is exactly the
        #   kind that goes unnoticed. Each line here is a complete centred
        #   line: 'กาเยนะ วาจายะ วะ เจตะสา วา' is a whole clause, not a half
        #   one, and reading straight down gives continuous sensible Pali.
        #   Confirm against the page.
        # ‼ CHECK [IMG_0277.PNG]: NO SECTION HEADINGS ADDED. The chant divides
        #   naturally into three stanzas — one for the Buddha, one for the
        #   Dhamma, one for the Saṅgha, beginning at verses 1, 5 and 9. The
        #   book prints no headings over them, only a space, so none have been
        #   written; adding them would put words on the page that the book
        #   does not print. Say if you would rather have them for the study
        #   view.
        # ‼ CHECK [IMG_0277.PNG]: The title คำขอขมาพระรัตนตรัย is THAI, not
        #   Pali in Thai script, so title_pali is empty and title_roman
        #   carries the romanised Thai for findability. This is the same
        #   treatment as คำประกาศอุโบสถ on page 10.
        # ‼ CHECK [IMG_0277.PNG]: Pali only — no Thai translation printed, so
        #   thai and paiboon are empty on every verse and english_unverified
        #   is set. The English is a working translation for this edition.
        # ‼ CHECK [IMG_0277.PNG]: WORD REJOINED ACROSS A HYPHEN, in the
        #   closing prose block below this chant rather than in the chant
        #   itself. The book breaks 'เบญจางคประดิษฐ์' as 'ด้วยเบญจางค-' at the
        #   end of one line and 'ประดิษฐ์' at the start of the next. That
        #   hyphen is justification, not spelling, so the word is recorded
        #   whole and the hyphen dropped.
        'id': 'kham-kho-khama-phra-rattanatrai',
        'title_thai': 'คำขอขมาพระรัตนตรัย',
        'title_pali': '',
        'title_roman': 'kam kɔ̌ɔ kà-maa prá-rát-dtà-ná-dtrai',
        'title_english': 'The Request for Forgiveness from the Triple Gem',
        'page_start': 14,
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
            # ‼ CHECK [IMG_0277.PNG]: The opening line 'กาเยนะ วาจายะ วะ
            #   เจตะสา วา' is printed three times in full, once at the head of
            #   each stanza, and is entered three times as verses 1, 5 and 9
            #   rather than marked as a repeat. Same treatment as the นะโม on
            #   page 2.
            {
                'number': 1,
                'pali': 'กาเยนะ วาจายะ วะ เจตะสา วา',
                'pali_roman': 'kāyena vācāya va cetasā vā',
                'thai': '',
                'paiboon': '',
                'english': 'By body, by speech, or by mind,',
            },
            {
                'number': 2,
                'pali': 'พุทเธ กุกัมมัง ปะกะตัง มะยา ยัง',
                'pali_roman': 'buddhe kukammaṃ pakataṃ mayā yaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'whatever wrong has been done by me towards the Buddha —',
            },
            {
                'number': 3,
                'pali': 'พุทโธ ปะฏิคคัณหะตุ อัจจะยันตัง',
                'pali_roman': 'buddho paṭiggaṇhatu accayantaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'may the Buddha accept that transgression,',
            },
            {
                'number': 4,
                'pali': 'กาลันตะเร สังวะริตุง วะ พุทเธ.',
                'pali_roman': 'kālantare saṃvarituṃ va buddhe.',
                'thai': '',
                'paiboon': '',
                'english': 'that in time to come I may be restrained towards the Buddha.',
            },
            {
                'number': 5,
                'pali': 'กาเยนะ วาจายะ วะ เจตะสา วา',
                'pali_roman': 'kāyena vācāya va cetasā vā',
                'thai': '',
                'paiboon': '',
                'english': 'By body, by speech, or by mind,',
            },
            {
                'number': 6,
                'pali': 'ธัมเม กุกัมมัง ปะกะตัง มะยา ยัง',
                'pali_roman': 'dhamme kukammaṃ pakataṃ mayā yaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'whatever wrong has been done by me towards the Dhamma —',
            },
            {
                'number': 7,
                'pali': 'ธัมโม ปะฏิคคัณหะตุ อัจจะยันตัง',
                'pali_roman': 'dhammo paṭiggaṇhatu accayantaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'may the Dhamma accept that transgression,',
            },
            {
                'number': 8,
                'pali': 'กาลันตะเร สังวะริตุง วะ ธัมเม.',
                'pali_roman': 'kālantare saṃvarituṃ va dhamme.',
                'thai': '',
                'paiboon': '',
                'english': 'that in time to come I may be restrained towards the Dhamma.',
            },
            {
                'number': 9,
                'pali': 'กาเยนะ วาจายะ วะ เจตะสา วา',
                'pali_roman': 'kāyena vācāya va cetasā vā',
                'thai': '',
                'paiboon': '',
                'english': 'By body, by speech, or by mind,',
            },
            {
                'number': 10,
                'pali': 'สังเฆ กุกัมมัง ปะกะตัง มะยา ยัง',
                'pali_roman': 'saṅghe kukammaṃ pakataṃ mayā yaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'whatever wrong has been done by me towards the Saṅgha —',
            },
            {
                'number': 11,
                'pali': 'สังโฆ ปะฏิคคัณหะตุ อัจจะยันตัง',
                'pali_roman': 'saṅgho paṭiggaṇhatu accayantaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'may the Saṅgha accept that transgression,',
            },
            {
                'number': 12,
                'pali': 'กาลันตะเร สังวะริตุง วะ สังเฆ.',
                'pali_roman': 'kālantare saṃvarituṃ va saṅghe.',
                'thai': '',
                'paiboon': '',
                'english': 'that in time to come I may be restrained towards the Saṅgha.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0278.PNG]: CONTINUES. The heading reads สารุปปะ 26
        #   สิกขาบท but only 23 are printed on this page, so rules 24-26 are
        #   on page 16 and have NOT been written from memory. Rule 23 is the
        #   going half of a pair; its sitting half should be rule 24.
        # ‼ CHECK [IMG_0278.PNG]: ENGLISH NEEDS A VINAYA CHECK. These are
        #   Pali-only, so the English is a working translation for this
        #   edition. Four terms carry established renderings I would not want
        #   to guess at: อุกขิตตะกายะ (ukkhittakāya), อุชชัคฆิกายะ
        #   (ujjagghikāya), ขัมภะกะโต (khambhakato) and โอคุณฐิโต (oguṇṭhito).
        #   Worth comparing against a Vinaya translation before print.
        # ‼ CHECK [IMG_0278.PNG]: The numbers 1-23 are the book's own
        #   numbering of the rules and match the verse numbers exactly. They
        #   are not chant numbers and not footnote markers.
        # ‼ CHECK [IMG_0278.PNG]: Built from a table of stems rather than
        #   transcribed twenty-three times, because every rule ends in the
        #   same อันตะระฆะเร … สิกขา กะระณียา and a typo in the twentieth
        #   repetition is what nobody spots. Verify a few at random against
        #   the page, especially 9-12 and 21-23.
        'id': 'sekhiyavatta',
        'title_thai': 'เสขิยวัตร',
        'title_pali': 'Sekhiyavatta',
        'title_roman': '',
        'title_english': 'The Sekhiya Rules of Training',
        'page_start': 15,
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
            # ‼ CHECK [IMG_0278.PNG]: The section heading สารุปปะ 26 สิกขาบท
            #   is the BOOK's own, printed under the title, not one I have
            #   grouped. It is set on verse 1 only, per the section rule.
            {
                'number': 1,
                'section': 'สารุปปะ 26 สิกขาบท: Sāruppa — the twenty-six training rules on proper deportment',
                'printed_number': 1,
                'pali': 'ปะริมัณฑะลัง นิวาเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'parimaṇḍalaṃ nivāsessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will wear the lower robe wrapped evenly all round': this is a training to be observed.",
            },
            {
                'number': 2,
                'printed_number': 2,
                'pali': 'ปะริมัณฑะลัง ปารุปิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'parimaṇḍalaṃ pārupissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will put on the upper robe wrapped evenly all round': this is a training to be observed.",
            },
            {
                'number': 3,
                'printed_number': 3,
                'pali': 'สุปะฏิจฉันโน อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'supaṭicchanno antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses well covered': this is a training to be observed.",
            },
            {
                'number': 4,
                'printed_number': 4,
                'pali': 'สุปะฏิจฉันโน อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'supaṭicchanno antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses well covered': this is a training to be observed.",
            },
            {
                'number': 5,
                'printed_number': 5,
                'pali': 'สุสังวุโต อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'susaṃvuto antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses well restrained': this is a training to be observed.",
            },
            {
                'number': 6,
                'printed_number': 6,
                'pali': 'สุสังวุโต อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'susaṃvuto antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses well restrained': this is a training to be observed.",
            },
            {
                'number': 7,
                'printed_number': 7,
                'pali': 'โอกขิตตะจักขุ อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'okkhittacakkhu antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses with eyes lowered': this is a training to be observed.",
            },
            {
                'number': 8,
                'printed_number': 8,
                'pali': 'โอกขิตตะจักขุ อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'okkhittacakkhu antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses with eyes lowered': this is a training to be observed.",
            },
            {
                'number': 9,
                'printed_number': 9,
                'pali': 'นะ อุกขิตตะกายะ อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ukkhittakāya antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses not with the robes hitched up': this is a training to be observed.",
            },
            {
                'number': 10,
                'printed_number': 10,
                'pali': 'นะ อุกขิตตะกายะ อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ukkhittakāya antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses not with the robes hitched up': this is a training to be observed.",
            },
            {
                'number': 11,
                'printed_number': 11,
                'pali': 'นะ อุชชัคฆิกายะ อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ujjagghikāya antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses not laughing loudly': this is a training to be observed.",
            },
            {
                'number': 12,
                'printed_number': 12,
                'pali': 'นะ อุชชัคฆิกายะ อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ujjagghikāya antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses not laughing loudly': this is a training to be observed.",
            },
            {
                'number': 13,
                'printed_number': 13,
                'pali': 'อัปปะสัทโท อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'appasaddo antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses making little noise': this is a training to be observed.",
            },
            {
                'number': 14,
                'printed_number': 14,
                'pali': 'อัปปะสัทโท อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'appasaddo antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses making little noise': this is a training to be observed.",
            },
            {
                'number': 15,
                'printed_number': 15,
                'pali': 'นะ กายัปปะจาละกัง อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na kāyappacālakaṃ antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses not swaying the body': this is a training to be observed.",
            },
            {
                'number': 16,
                'printed_number': 16,
                'pali': 'นะ กายัปปะจาละกัง อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na kāyappacālakaṃ antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses not swaying the body': this is a training to be observed.",
            },
            {
                'number': 17,
                'printed_number': 17,
                'pali': 'นะ พาหุปปะจาละกัง อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na bāhuppacālakaṃ antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses not swinging the arms': this is a training to be observed.",
            },
            {
                'number': 18,
                'printed_number': 18,
                'pali': 'นะ พาหุปปะจาละกัง อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na bāhuppacālakaṃ antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses not swinging the arms': this is a training to be observed.",
            },
            {
                'number': 19,
                'printed_number': 19,
                'pali': 'นะ สีสัปปะจาละกัง อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sīsappacālakaṃ antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses not wagging the head': this is a training to be observed.",
            },
            {
                'number': 20,
                'printed_number': 20,
                'pali': 'นะ สีสัปปะจาละกัง อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sīsappacālakaṃ antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses not wagging the head': this is a training to be observed.",
            },
            {
                'number': 21,
                'printed_number': 21,
                'pali': 'นะ ขัมภะกะโต อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na khambhakato antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses not with arms akimbo': this is a training to be observed.",
            },
            {
                'number': 22,
                'printed_number': 22,
                'pali': 'นะ ขัมภะกะโต อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na khambhakato antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will sit among the houses not with arms akimbo': this is a training to be observed.",
            },
            {
                'number': 23,
                'printed_number': 23,
                'pali': 'นะ โอคุณฐิโต อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na oguṇṭhito antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will go among the houses not with the head covered': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0279.PNG]: The chant is now COMPLETE at twenty-six,
            #   matching the heading สารุปปะ 26 สิกขาบท on page 15. The
            #   CONTINUES marker should come off.
            {
                'number': 24,
                'page': 16,
                'printed_number': 24,
                'pali': 'นะ โอคุณฐิโต อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na oguṇṭhito antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not sit among the houses with the head covered': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0279.PNG]: อุกกุฏิกายะ (ukkuṭikāya) and
            #   ปัลลัตถิกายะ (pallatthikāya) in rule 26 are both technical
            #   postures. The English is a working translation; worth checking
            #   against a Vinaya translation before print, along with the four
            #   flagged on page 15.
            {
                'number': 25,
                'printed_number': 25,
                'pali': 'นะ อุกกุฏิกายะ อันตะระฆะเร คะมิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ukkuṭikāya antaraghare gamissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not go among the houses walking on the heels or on tiptoe': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0279.PNG]: Footnote marker 1 sits at the end of
            #   this rule, and its footnote 'วิ. มหา 2/531-542' is printed at
            #   the FOOT of the page, below the Bhojana rules. It is carried
            #   as a page footnote block there, where the book prints it, not
            #   as source_printed on this chant — see the check on the Bhojana
            #   entry.
            {
                'number': 26,
                'printed_number': 26,
                'pali': 'นะ ปัลลัตถิกายะ อันตะระฆะเร นิสีทิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na pallatthikāya antaraghare nisīdissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not sit among the houses lolling or clasping the knees': this is a training to be observed.",
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0279.PNG]: The book prints NO title for this group,
        #   only the heading โภชะนะปะฏิสังยุต 30 สิกขาบท, which is carried as
        #   the section on verse 1. title_thai and title_pali are left empty;
        #   title_english is the app's own.
        # ‼ CHECK [IMG_0279.PNG]: CONTINUES. The heading says 30 and 18 are
        #   printed here, so rules 19-30 are on page 17 and have not been
        #   written from memory.
        # ‼ CHECK [IMG_0279.PNG]: Rules 1-8 were generated from a table of
        #   four stems paired with receiving and eating, as page 15's were;
        #   9-18 were transcribed individually because each differs. Spot-
        #   check 1-8 against the page.
        'id': 'sekhiya-bhojanapatisamyutta',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Sekhiya Rules — Bhojanapaṭisaṃyutta',
        'page_start': 16,
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
            # ‼ CHECK [IMG_0279.PNG]: DECISION NEEDED — WHY THIS IS A SEPARATE
            #   CHANT. The book prints เสขิยวัตร once as a title on page 15
            #   and then group headings under it, so structurally the Sekhiyas
            #   are ONE chant in four groups. But the NUMBERING RESTARTS at 1
            #   for each group, and a chant dict numbers its verses uniquely.
            #   Kept as one chant, this rule would render as verse 27 where
            #   the book prints 1 — and the printed number is what a reader
            #   follows. So each group is its own chant, numbered as the book
            #   numbers it. The cost is that เสขิยวัตร appears in the index as
            #   several entries rather than one. Please confirm.
            {
                'number': 1,
                'section': 'โภชะนะปะฏิสังยุต 30 สิกขาบท: Bhojanapaṭisaṃyutta — the thirty training rules on receiving and eating almsfood',
                'printed_number': 1,
                'pali': 'สักกัจจัง ปิณฑะปาตัง ปะฏิคคะเหสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'sakkaccaṃ piṇḍapātaṃ paṭiggahessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will receive almsfood attentively': this is a training to be observed.",
            },
            {
                'number': 2,
                'printed_number': 2,
                'pali': 'ปัตตะสัญญี ปิณฑะปาตัง ปะฏิคคะเหสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'pattasaññī piṇḍapātaṃ paṭiggahessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will receive almsfood with attention on the bowl': this is a training to be observed.",
            },
            {
                'number': 3,
                'printed_number': 3,
                'pali': 'สะมะสูปะกัง ปิณฑะปาตัง ปะฏิคคะเหสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'samasūpakaṃ piṇḍapātaṃ paṭiggahessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will receive almsfood with a due proportion of curry': this is a training to be observed.",
            },
            {
                'number': 4,
                'printed_number': 4,
                'pali': 'สะมะติตติกัง ปิณฑะปาตัง ปะฏิคคะเหสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'samatittikaṃ piṇḍapātaṃ paṭiggahessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will receive almsfood level with the rim': this is a training to be observed.",
            },
            {
                'number': 5,
                'printed_number': 5,
                'pali': 'สักกัจจัง ปิณฑะปาตัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'sakkaccaṃ piṇḍapātaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will eat almsfood attentively': this is a training to be observed.",
            },
            {
                'number': 6,
                'printed_number': 6,
                'pali': 'ปัตตะสัญญี ปิณฑะปาตัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'pattasaññī piṇḍapātaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will eat almsfood with attention on the bowl': this is a training to be observed.",
            },
            {
                'number': 7,
                'printed_number': 7,
                'pali': 'สะปะทานัง ปิณฑะปาตัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'sapadānaṃ piṇḍapātaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will eat almsfood in order, without picking and choosing': this is a training to be observed.",
            },
            {
                'number': 8,
                'printed_number': 8,
                'pali': 'สะมะสูปะกัง ปิณฑะปาตัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'samasūpakaṃ piṇḍapātaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will eat almsfood with a due proportion of curry': this is a training to be observed.",
            },
            {
                'number': 9,
                'printed_number': 9,
                'pali': 'นะ ถูปะโต โอมัททิต๎วา ปิณฑะปาตัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na thūpato omadditvā piṇḍapātaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat almsfood having pressed it down from the top': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0279.PNG]: Rules 10 and 11 run onto a second
            #   printed line through justification only, not as couplets. Kept
            #   as one verse each. The yamakkan appears in พ์ยัญชะนัง and
            #   ภิยโยกัม๎ยะตัง here, and in วิญญาเปต๎วา (11), โอมัททิต๎วา (9),
            #   มุขะท๎วารัง (15) and พ์ยาหะริสสามีติ (17) — all reproduced as
            #   printed.
            {
                'number': 10,
                'printed_number': 10,
                'pali': 'นะ สูปัง วา พ์ยัญชะนัง วา โอทะเนนะ ปะฏิจฉาเทสสามิ ภิยโยกัม๎ยะตัง อุปาทายาติ สิกขา กะระณียา.',
                'pali_roman': 'na sūpaṃ vā byañjanaṃ vā odanena paṭicchādessāmi bhiyyokamyataṃ upādāyāti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not cover up curry or condiment with rice out of a wish for more': this is a training to be observed.",
            },
            {
                'number': 11,
                'printed_number': 11,
                'pali': 'นะ สูปัง วา โอทะนัง วา อะคิลาโน อัตตะโน อัตถายะ วิญญาเปต๎วา ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sūpaṃ vā odanaṃ vā agilāno attano atthāya viññāpetvā bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I, not being ill, will not eat curry or rice having asked for it for myself': this is a training to be observed.",
            },
            {
                'number': 12,
                'printed_number': 12,
                'pali': 'นะ อุชฌานะสัญญี ปะเรสัง ปัตตัง โอโลเกสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ujjhānasaññī paresaṃ pattaṃ olokessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not look at others' bowls finding fault': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0279.PNG]: กะวะฬัง (13) and กะวะเฬ (15) use ฬ,
            #   romanised kabaḷaṃ / kabaḷe with the retroflex ḷ, following the
            #   Thai letter rather than the kavaḷa spelling some editions use.
            {
                'number': 13,
                'printed_number': 13,
                'pali': 'นาติมะหันตัง กะวะฬัง กะริสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'nātimahantaṃ kabaḷaṃ karissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not make too large a mouthful': this is a training to be observed.",
            },
            {
                'number': 14,
                'printed_number': 14,
                'pali': 'ปะริมัณฑะลัง อาโลปัง กะริสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'parimaṇḍalaṃ ālopaṃ karissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will make the morsel round': this is a training to be observed.",
            },
            {
                'number': 15,
                'printed_number': 15,
                'pali': 'นะ อะนาหะเฏ กะวะเฬ มุขะท๎วารัง วิวะริสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na anāhaṭe kabaḷe mukhadvāraṃ vivarissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not open the mouth before the morsel is brought to it': this is a training to be observed.",
            },
            {
                'number': 16,
                'printed_number': 16,
                'pali': 'นะ ภุญชะมาโน สัพพัง หัตถัง มุเข ปักขิปิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na bhuñjamāno sabbaṃ hatthaṃ mukhe pakkhipissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not put the whole hand into the mouth while eating': this is a training to be observed.",
            },
            {
                'number': 17,
                'printed_number': 17,
                'pali': 'นะ สะกะวะเฬนะ มุเขนะ พ์ยาหะริสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sakabaḷena mukhena byāharissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not speak with a mouthful in the mouth': this is a training to be observed.",
            },
            {
                'number': 18,
                'printed_number': 18,
                'pali': 'นะ ปิณฑุกเขปะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na piṇḍukkhepakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat tossing up balls of food': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0280.PNG]: READING CALL, PLEASE CONFIRM — ฬ or พ. I
            #   have read this as 'กะวะฬาวัจเฉทะกัง' with ฬ. At this
            #   resolution the book's ฬ is hard to tell from พ, and my first
            #   reading of the glyph was พ. Three things decided it for ฬ: the
            #   same root is printed กะวะฬัง in rule 13 on page 16, where the
            #   letter is clear; standard editions read kabaḷāvacchedakaṃ; and
            #   the SAME ambiguous glyph appears twice more on this page, in
            #   รูฬ๎หัสสะ at Dhammadesana rules 5 and 6, both places where ฬ
            #   is expected. If the book really prints พ, all three are wrong
            #   together. Worth a retake of this page at higher magnification.
            {
                'number': 19,
                'page': 17,
                'printed_number': 19,
                'pali': 'นะ กะวะฬาวัจเฉทะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na kabaḷāvacchedakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat biting off mouthfuls': this is a training to be observed.",
            },
            {
                'number': 20,
                'printed_number': 20,
                'pali': 'นะ อะวะคัณฑะการะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na avagaṇḍakārakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat stuffing out the cheeks': this is a training to be observed.",
            },
            {
                'number': 21,
                'printed_number': 21,
                'pali': 'นะ หัตถะนิทธูนะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na hatthaniddhūnakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat shaking the hand about': this is a training to be observed.",
            },
            {
                'number': 22,
                'printed_number': 22,
                'pali': 'นะ สิตถาวะการะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sitthāvakārakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat scattering rice grains': this is a training to be observed.",
            },
            {
                'number': 23,
                'printed_number': 23,
                'pali': 'นะ ชิวหานิจฉาระกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na jivhānicchārakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat putting out the tongue': this is a training to be observed.",
            },
            {
                'number': 24,
                'printed_number': 24,
                'pali': 'นะ จะปุจะปุการะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na capucapukārakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat making a chomping sound': this is a training to be observed.",
            },
            {
                'number': 25,
                'printed_number': 25,
                'pali': 'นะ สุรุสุรุการะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na surusurukārakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat making a slurping sound': this is a training to be observed.",
            },
            {
                'number': 26,
                'printed_number': 26,
                'pali': 'นะ หัตถะนิลเลหะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na hatthanillehakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat licking the hands': this is a training to be observed.",
            },
            {
                'number': 27,
                'printed_number': 27,
                'pali': 'นะ ปัตตะนิลเลหะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na pattanillehakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat licking the bowl': this is a training to be observed.",
            },
            {
                'number': 28,
                'printed_number': 28,
                'pali': 'นะ โอฏฐะนิลเลหะกัง ภุญชิสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na oṭṭhanillehakaṃ bhuñjissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not eat licking the lips': this is a training to be observed.",
            },
            {
                'number': 29,
                'printed_number': 29,
                'pali': 'นะ สามิเสนะ หัตเถนะ ปานียะถาละกัง ปะฏิคคะเหสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sāmisena hatthena pānīyathālakaṃ paṭiggahessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not accept a drinking-water vessel with a hand soiled by food': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0280.PNG]: The chant is now COMPLETE at thirty,
            #   matching the heading โภชะนะปะฏิสังยุต 30 สิกขาบท on page 16.
            #   The CONTINUES marker should come off. Footnote marker 1 sits
            #   here.
            # ‼ CHECK [IMG_0280.PNG]: THE FOOTNOTE REFERENCE LOOKS ODD.
            #   Footnote 1 on this page reads 'วิ. มหา. 252-557'. Page 16's
            #   footnote read 'วิ. มหา 2/531-542' — volume 2, sections 531-542
            #   — so a reference continuing from it would be expected to read
            #   '2/543-557'. The printed form has been reproduced exactly and
            #   NOT normalised. Either the book prints it this way or I have
            #   misread the slash; the same retake that settles the ฬ/พ
            #   question would settle this.
            {
                'number': 30,
                'printed_number': 30,
                'pali': 'นะ สะสิตถะกัง ปัตตะโธวะนัง อันตะระฆะเร ฉัฑเฑสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sasitthakaṃ pattadhovanaṃ antaraghare chaḍḍessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not throw out bowl-rinsing water containing rice grains among the houses': this is a training to be observed.",
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0280.PNG]: CONTINUES. The heading says 16 and 7 are
        #   printed here, so rules 8-16 are on page 18 and have not been
        #   written from memory.
        'id': 'sekhiya-dhammadesanapatisamyutta',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Sekhiya Rules — Dhammadesanāpaṭisaṃyutta',
        'page_start': 17,
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
            # ‼ CHECK [IMG_0280.PNG]: Separate chant for the same reason as
            #   the Bhojana group on page 16: the book RESTARTS its numbering
            #   at each Sekhiya group, and a chant numbers its verses
            #   uniquely. This is the third of four groups. No chant title is
            #   printed, only the heading ธัมมะเทสะนาปะฏิสังยุต 16 สิกขาบท,
            #   carried as the section on this verse.
            # ‼ CHECK [IMG_0280.PNG]: Footnote marker 2 sits on the word สิกขา
            #   in this rule, not at the end of the line. Its footnote is
            #   partly a citation and partly an editorial note — it says most
            #   chanters use เทสิสสามีติ in place of the printed เทเสสสามีติ.
            #   Because it carries instruction it is kept as a page footnote
            #   block rather than source_printed, per the rule that an
            #   editorial note is never filed as a citation.
            # ‼ CHECK [IMG_0280.PNG]: The book prints เทเสสสามีติ
            #   (desessāmīti). Reproduced as printed; the variant เทสิสสามีติ
            #   mentioned in footnote 2 is NOT substituted.
            {
                'number': 1,
                'section': 'ธัมมะเทสะนาปะฏิสังยุต 16 สิกขาบท: Dhammadesanāpaṭisaṃyutta — the sixteen training rules on teaching the Dhamma',
                'printed_number': 1,
                'pali': 'นะ ฉัตตะปาณิสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na chattapāṇissa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is with a sunshade in hand': this is a training to be observed.",
            },
            {
                'number': 2,
                'printed_number': 2,
                'pali': 'นะ ทัณฑะปาณิสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na daṇḍapāṇissa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is with a staff in hand': this is a training to be observed.",
            },
            {
                'number': 3,
                'printed_number': 3,
                'pali': 'นะ สัตถะปาณิสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na satthapāṇissa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is with a knife in hand': this is a training to be observed.",
            },
            {
                'number': 4,
                'printed_number': 4,
                'pali': 'นะ อาวุธะปาณิสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na āvudhapāṇissa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is with a weapon in hand': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0280.PNG]: ฬ or พ again — 'ปาทุการูฬ๎หัสสะ' here
            #   and 'อุปาหะนารูฬ๎หัสสะ' in rule 6. Read as ฬ๎ห for the same
            #   reasons given on the Bhojana entry's verse 19 check. All three
            #   readings on this page stand or fall together.
            {
                'number': 5,
                'printed_number': 5,
                'pali': 'นะ ปาทุการูฬ๎หัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na pādukārūḷhassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is wearing wooden sandals': this is a training to be observed.",
            },
            {
                'number': 6,
                'printed_number': 6,
                'pali': 'นะ อุปาหะนารูฬ๎หัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na upāhanārūḷhassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is wearing shoes': this is a training to be observed.",
            },
            {
                'number': 7,
                'printed_number': 7,
                'pali': 'นะ ยานะคะตัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na yānagatassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is in a vehicle': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0281.PNG]: The chant is now COMPLETE at sixteen,
            #   matching the heading ธัมมะเทสะนาปะฏิสังยุต 16 สิกขาบท on page
            #   17. The CONTINUES marker should come off.
            {
                'number': 8,
                'page': 18,
                'printed_number': 8,
                'pali': 'นะ สะยะนะคะตัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na sayanagatassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is lying down': this is a training to be observed.",
            },
            {
                'number': 9,
                'printed_number': 9,
                'pali': 'นะ ปัลลัตถิกายะ นิสินนัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na pallatthikāya nisinnassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is sitting clasping the knees': this is a training to be observed.",
            },
            {
                'number': 10,
                'printed_number': 10,
                'pali': 'นะ เวฐิตะสีสัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na veṭhitasīsassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is with the head wrapped': this is a training to be observed.",
            },
            {
                'number': 11,
                'printed_number': 11,
                'pali': 'นะ โอคุณฐิตะสีสัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na oguṇṭhitasīsassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not teach Dhamma to someone who is not ill and who is with the head covered': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0281.PNG]: WORD REJOINED ACROSS A HYPHEN. The book
            #   breaks เทเสสสามีติ as 'เทเสส-' at the end of one line and
            #   'สามีติ' at the start of the next. That hyphen is
            #   justification, not spelling, so the word is recorded whole.
            # ‼ CHECK [IMG_0281.PNG]: Rules 12, 13, 15 and 16 each contrast
            #   two positions — ground against seat, low against high, behind
            #   against in front, off the path against on it. The second half
            #   is always the person being taught. Check the pairs read the
            #   right way round.
            {
                'number': 12,
                'printed_number': 12,
                'pali': 'นะ ฉะมายัง นิสีทิต๎วา อาสะเน นิสินนัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na chamāyaṃ nisīditvā āsane nisinnassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not, sitting on the ground, teach Dhamma to someone who is not ill and is sitting on a seat': this is a training to be observed.",
            },
            {
                'number': 13,
                'printed_number': 13,
                'pali': 'นะ นีเจ อาสะเน นิสีทิต๎วา อุจเจ อาสะเน นิสินนัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na nīce āsane nisīditvā ucce āsane nisinnassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not, sitting on a low seat, teach Dhamma to someone who is not ill and is sitting on a high seat': this is a training to be observed.",
            },
            {
                'number': 14,
                'printed_number': 14,
                'pali': 'นะ ฐิโต นิสินนัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ṭhito nisinnassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not, standing, teach Dhamma to someone who is not ill and is sitting': this is a training to be observed.",
            },
            {
                'number': 15,
                'printed_number': 15,
                'pali': 'นะ ปัจฉะโต คัจฉันโต ปุระโต คัจฉันตัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na pacchato gacchanto purato gacchantassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not, walking behind, teach Dhamma to someone who is not ill and is walking in front': this is a training to be observed.",
            },
            {
                'number': 16,
                'printed_number': 16,
                'pali': 'นะ อุปปะเถนะ คัจฉันโต ปะเถนะ คัจฉันตัสสะ อะคิลานัสสะ ธัมมัง เทเสสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na uppathena gacchanto pathena gacchantassa agilānassa dhammaṃ desessāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I will not, walking off the path, teach Dhamma to someone who is not ill and is walking on the path': this is a training to be observed.",
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0281.PNG]: The book prints no Thai translation anywhere
        #   on page 18, so thai and paiboon are empty and english_unverified
        #   is set.
        'id': 'sekhiya-pakinnaka',
        'title_thai': '',
        'title_pali': '',
        'title_roman': '',
        'title_english': 'The Sekhiya Rules — Pakiṇṇaka',
        'page_start': 18,
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
            # ‼ CHECK [IMG_0281.PNG]: The fourth and last Sekhiya group, and
            #   the one that closes the set: 26 + 30 + 16 + 3 = 75, the
            #   standard count. Separate chant for the same reason as the
            #   second and third — the book restarts its numbering at each
            #   group. No chant title is printed, only the heading ปกิณณะกะ 3
            #   สิกขาบท, carried as the section here.
            {
                'number': 1,
                'section': 'ปกิณณะกะ 3 สิกขาบท: Pakiṇṇaka — the three miscellaneous training rules',
                'printed_number': 1,
                'pali': 'นะ ฐิโต อะคิลาโน อุจจารัง วา ปัสสาวัง วา กะริสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na ṭhito agilāno uccāraṃ vā passāvaṃ vā karissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I, not being ill, will not defecate or urinate standing': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0281.PNG]: ฬ or พ, twice more — 'เขฬัง' (kheḷaṃ,
            #   spittle) in rules 2 and 3. Read as ฬ on the same grounds as
            #   the three on page 17. That makes FIVE instances of this glyph
            #   across two pages, all in positions where ฬ is expected and
            #   never one where พ would make sense, which is itself evidence
            #   that this book's ฬ simply photographs like พ. One retake would
            #   settle all five.
            {
                'number': 2,
                'printed_number': 2,
                'pali': 'นะ หะริเต อะคิลาโน อุจจารัง วา ปัสสาวัง วา เขฬัง วา กะริสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na harite agilāno uccāraṃ vā passāvaṃ vā kheḷaṃ vā karissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I, not being ill, will not defecate, urinate or spit on living greenery': this is a training to be observed.",
            },
            # ‼ CHECK [IMG_0281.PNG]: Footnote 1 on this page reads 'วิ. มหา
            #   2/558-570' — with the slash and volume number, exactly the
            #   form page 16's footnote used. That makes page 17's 'วิ. มหา.
            #   252-557' look more likely to be a misreading of '2/543-557' on
            #   my part than something the book prints. Worth checking both at
            #   once.
            {
                'number': 3,
                'printed_number': 3,
                'pali': 'นะ อุทะเก อะคิลาโน อุจจารัง วา ปัสสาวัง วา เขฬัง วา กะริสสามีติ สิกขา กะระณียา.',
                'pali_roman': 'na udake agilāno uccāraṃ vā passāvaṃ vā kheḷaṃ vā karissāmīti sikkhā karaṇīyā.',
                'thai': '',
                'paiboon': '',
                'english': "'I, not being ill, will not defecate, urinate or spit in water': this is a training to be observed.",
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0282.PNG]: FIRST CHANT WITH A BOOK NUMBER. The book
        #   prints '1.' before the title, so book_number is 1. This is the
        #   book's own chant numbering, not a page number and not a verse
        #   number, and it has not been derived by counting.
        # ‼ CHECK [IMG_0282.PNG]: CONTINUES. Reflections 9 and 10 are on page
        #   20 and have not been written from memory of the canon.
        # ‼ CHECK [IMG_0282.PNG]: Pali only — no Thai translation printed on
        #   this page, so thai and paiboon are empty and english_unverified is
        #   set. Worth watching whether page 20 prints a คำแปล for it, as page
        #   10 did for the Uposatha announcement.
        'id': 'dasadhamma-sutta',
        'title_thai': 'ทะสะธัมมะสุตตัง',
        'title_pali': 'Dasadhammasuttaṃ',
        'title_roman': '',
        'title_english': 'The Discourse on the Ten Things',
        'book_number': 1,
        'page_start': 19,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'closing': {
            'pali': 'ทะสะธัมมะสุตตัง นิฏฐิตัง.',
            'pali_roman': 'dasadhammasuttaṃ niṭṭhitaṃ.',
            'thai': '',
            'paiboon': '',
            'english': 'The Discourse on the Ten Things is ended.',
        },
        'verses': [
            # ‼ CHECK [IMG_0282.PNG]: The nidana is the standard Savatthi
            #   opening. Reproduced as printed, including ตัต๎ระ with the
            #   yamakkan and the commas the book sets, rather than normalised
            #   to a standard edition's punctuation.
            {
                'number': 1,
                'pali': 'เอวัมเม สุตัง, เอกัง สะมะยัง ภะคะวา, สาวัตถิยัง วิหะระติ, เชตะวะเน อะนาถะปิณฑิกัสสะ อาราเม, ตัต๎ระ โข ภะคะวา ภิกขู อามันเตสิ ภิกขะโวติ, ภะทันเตติ เต ภิกขู ภะคะวะโต ปัจจัสโสสุง, ภะคะวา เอตะทะโวจะ.',
                'pali_roman': 'evamme sutaṃ, ekaṃ samayaṃ bhagavā, sāvatthiyaṃ viharati, jetavane anāthapiṇḍikassa ārāme, tatra kho bhagavā bhikkhū āmantesi bhikkhavoti, bhadanteti te bhikkhū bhagavato paccassosuṃ, bhagavā etadavoca.',
                'thai': '',
                'paiboon': '',
                'english': "Thus have I heard. At one time the Blessed One was dwelling at Savatthi, in Jeta's Grove, Anathapindika's park. There the Blessed One addressed the bhikkhus: 'Bhikkhus.' 'Venerable sir,' those bhikkhus replied. The Blessed One said this:",
            },
            {
                'number': 2,
                'pali': 'ทะสะ อิเม ภิกขะเว ธัมมา ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพา. กะตะเม ทะสะ.',
                'pali_roman': 'dasa ime bhikkhave dhammā pabbajitena abhiṇhaṃ paccavekkhitabbā. katame dasa.',
                'thai': '',
                'paiboon': '',
                'english': 'There are these ten things, bhikkhus, that one who has gone forth should reflect on again and again. What ten?',
            },
            # ‼ CHECK [IMG_0282.PNG]: NUMBERING OFFSET, worth a decision. The
            #   book numbers the ten reflections 1-10, but the sutta opens
            #   with two unnumbered lines — the nidana and 'katame dasa' —
            #   which are chanted and so must be verses. That makes the book's
            #   item 1 into verse 3, and every item is offset by two. Book
            #   view hides verse numbers so nothing shows there, but the
            #   verse-by-verse study view prints them and they will not match
            #   the page. The same offset will hit every numbered list that
            #   follows a preamble.
            {
                'number': 3,
                'printed_number': 1,
                'pali': 'เววัณณิยัมหิ อัชฌูปะคะโตติ ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'vevaṇṇiyamhi ajjhūpagatoti pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'I have come to a state of being without caste': this should be reflected on again and again by one who has gone forth.",
            },
            {
                'number': 4,
                'printed_number': 2,
                'pali': 'ปะระปะฏิพัทธา เม ชีวิกาติ ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'parapaṭibaddhā me jīvikāti pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'My life is dependent on others': this should be reflected on again and again by one who has gone forth.",
            },
            # ‼ CHECK [IMG_0282.PNG]: WORDS REJOINED ACROSS HYPHENS, two of
            #   them. Item 3 breaks ปัจจะเวกขิตัพพัง as 'ปัจจะเวก-' /
            #   'ขิตัพพัง', and item 7 breaks กัมมะปะฏิสะระโณ as 'กัมมะปะฏิ-'
            #   / 'สะระโณ'. Both hyphens are justification, not spelling, so
            #   both words are recorded whole.
            {
                'number': 5,
                'printed_number': 3,
                'pali': 'อัญโญ เม อากัปโป กะระณีโยติ ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'añño me ākappo karaṇīyoti pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'My bearing should be other than it was': this should be reflected on again and again by one who has gone forth.",
            },
            {
                'number': 6,
                'printed_number': 4,
                'pali': 'กัจจิ นุ โข เม อัตตา สีละโต นะ อุปะวะทะตีติ ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'kacci nu kho me attā sīlato na upavadatīti pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'Does my own conscience reproach me as to virtue?': this should be reflected on again and again by one who has gone forth.",
            },
            {
                'number': 7,
                'printed_number': 5,
                'pali': 'กัจจิ นุ โข มัง อะนุวิจจะ วิญญู สะพ์รัห์มะจารี สีละโต นะ อุปะวะทันตีติ ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'kacci nu kho maṃ anuvicca viññū sabrahmacārī sīlato na upavadantīti pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'Do my wise companions in the holy life, having examined me, reproach me as to virtue?': this should be reflected on again and again by one who has gone forth.",
            },
            {
                'number': 8,
                'printed_number': 6,
                'pali': 'สัพเพหิ เม ปิเยหิ มะนาเปหิ นานาภาโว วินาภาโวติ, ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'sabbehi me piyehi manāpehi nānābhāvo vinābhāvoti, pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'There is a parting and a separation from all that is dear and pleasing to me': this should be reflected on again and again by one who has gone forth.",
            },
            {
                'number': 9,
                'printed_number': 7,
                'pali': 'กัมมัสสะโกมหิ กัมมะทายาโท กัมมะโยนิ กัมมะพันธุ กัมมะปะฏิสะระโณ, ยัง กัมมัง กะริสสามิ กัล๎ยาณัง วา ปาปะกัง วา, ตัสสะ ทายาโท ภะวิสสามีติ, ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'kammassakomhi kammadāyādo kammayoni kammabandhu kammapaṭisaraṇo, yaṃ kammaṃ karissāmi kalyāṇaṃ vā pāpakaṃ vā, tassa dāyādo bhavissāmīti, pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'I am the owner of my kamma, heir to my kamma, born of my kamma, kindred to my kamma, abide supported by my kamma; whatever kamma I shall do, good or bad, of that I shall be the heir': this should be reflected on again and again by one who has gone forth.",
            },
            {
                'number': 10,
                'printed_number': 8,
                'pali': 'กะถัมภูตัสสะ เม รัตตินทิวา วีติปะตันตีติ ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'kathaṃbhūtassa me rattindivā vītipatantīti pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'How do the days and nights pass for me?': this should be reflected on again and again by one who has gone forth.",
            },
            # ‼ CHECK [IMG_0283.PNG]: The sutta is now COMPLETE at ten
            #   reflections, matching 'กะตะเม ทะสะ' on page 19. The CONTINUES
            #   marker should come off. Verses 11 and 12 carry printed_number
            #   9 and 10 — the book's own numbers — while verse 13 carries
            #   none, because the closing sentence is printed unnumbered.
            {
                'number': 11,
                'page': 20,
                'printed_number': 9,
                'pali': 'กัจจิ นุ โขหัง สุญญาคาเร อะภิระมามีติ ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'kacci nu khohaṃ suññāgāre abhiramāmīti pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'Do I delight in empty dwellings?': this should be reflected on again and again by one who has gone forth.",
            },
            # ‼ CHECK [IMG_0283.PNG]: WORDS REJOINED ACROSS HYPHENS, two of
            #   them: อะละมะริยะญาณะทัสสะนะวิเสโส breaks as '…ทัสสะนะ-' /
            #   'วิเสโส' in verse 12, and ปัจจะเวกขิตัพพาติ breaks as
            #   'ปัจจะเวก-' / 'ขิตัพพาติ' in verse 13. Both hyphens are
            #   justification, not spelling.
            {
                'number': 12,
                'printed_number': 10,
                'pali': 'อัตถิ นุ โข เม อุตตะริมะนุสสะธัมมา อะละมะริยะญาณะทัสสะนะวิเสโส, อะธิคะโต โสหัง ปัจฉิเม กาเล สะพ์รัห์มะจารีหิ ปุฏโฐ นะ มังกุ ภะวิสสามีติ, ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพัง.',
                'pali_roman': 'atthi nu kho me uttarimanussadhammā alamariyañāṇadassanaviseso, adhigato sohaṃ pacchime kāle sabrahmacārīhi puṭṭho na maṅku bhavissāmīti, pabbajitena abhiṇhaṃ paccavekkhitabbaṃ.',
                'thai': '',
                'paiboon': '',
                'english': "'Have I attained any superior human state, any distinction of knowledge and vision worthy of the noble ones, such that in my last days, when questioned by my companions in the holy life, I shall not be embarrassed?': this should be reflected on again and again by one who has gone forth.",
            },
            # ‼ CHECK [IMG_0283.PNG]: Footnote marker 1 sits here, and the
            #   footnote reads 'อง ทสก. 24/24-5' — Aṅguttara-nikāya, Dasaka-
            #   nipāta. The marker is unambiguous, so the prompt would put it
            #   in `source_printed`; it is carried as a page footnote block
            #   instead, because the template renders source_printed as a line
            #   labelled with the chant's title and the book prints '1. อง
            #   ทสก. 24/24-5' under a rule. Same treatment as pages 12 and
            #   16-18. NOTE: page 6's chant still uses source_printed and so
            #   still renders the app's form — the one page left inconsistent.
            {
                'number': 13,
                'pali': 'อิเม โข ภิกขะเว ทะสะ ธัมมา, ปัพพะชิเตนะ อะภิณ๎หัง ปัจจะเวกขิตัพพาติ, อิทะมะโวจะ ภะคะวา, อัตตะมะนา เต ภิกขู ภะคะวะโต ภาสิตัง อะภินันทุนติ.',
                'pali_roman': 'ime kho bhikkhave dasa dhammā, pabbajitena abhiṇhaṃ paccavekkhitabbāti, idamavoca bhagavā, attamanā te bhikkhū bhagavato bhāsitaṃ abhinandunti.',
                'thai': '',
                'paiboon': '',
                'english': "These, bhikkhus, are the ten things that one who has gone forth should reflect on again and again. This is what the Blessed One said. Gladdened, those bhikkhus delighted in the Blessed One's words.",
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0283.PNG]: CONTINUES. The passage sets out the Buddha
        #   as foremost of beings and dispassion as foremost of dhammas; the
        #   parallel for the Sangha is not on this page, so the rest is on
        #   page 21 and has not been written from memory.
        # ‼ CHECK [IMG_0283.PNG]: Book number 2, printed as '2.' before the
        #   title. The second numbered chant in the book.
        'id': 'parittakarana-patha',
        'title_thai': 'ปะริตตะกะระณะปาฐะ',
        'title_pali': 'Parittakaraṇapāṭha',
        'title_roman': '',
        'title_english': 'The Passage for Making a Protection',
        'book_number': 2,
        'page_start': 20,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'closing': {
            'pali': 'ปะริตตะกะระณะปาโฐ นิฏฐิโต',
            'pali_roman': 'parittakaraṇapāṭho niṭṭhito',
            'thai': '',
            'paiboon': '',
            'english': 'Here ends the Text for Making a Protection.',
        },
        'verses': [
            # ‼ CHECK [IMG_0283.PNG]: SINGLE COLUMN, checked deliberately. The
            #   centred stanza at verse 2 has short lines that could be
            #   mistaken for column halves, but each is a complete pada and
            #   the surrounding prose runs the full measure.
            {
                'number': 1,
                'pali': 'ยาวะตา สัตตา อะปะทา วา ท๎วิปะทา วา จะตุปปะทา วา พะหุปปะทา วา, รูปิโน วา อะรูปิโน วา, สัญญิโน วา อะสัญญิโน วา, เนวะสัญญีนาสัญญิโน วา, ตะถาคะโต เตสัง อัคคะมักขายะติ อะระหัง สัมมาสัมพุทโธ, เย โข พุทเธ ปะสันนา อัคเค เต ปะสันนา, อัคเค โข ปะนะ ปะสันนานัง อัคโค วิปาโก.',
                'pali_roman': 'yāvatā sattā apadā vā dvipadā vā catuppadā vā bahuppadā vā, rūpino vā arūpino vā, saññino vā asaññino vā, nevasaññīnāsaññino vā, tathāgato tesaṃ aggamakkhāyati arahaṃ sammāsambuddho, ye kho buddhe pasannā agge te pasannā, agge kho pana pasannānaṃ aggo vipāko.',
                'thai': '',
                'paiboon': '',
                'english': 'As far as there are beings — footless, two-footed, four-footed or many-footed, with form or formless, percipient or non-percipient or neither-percipient-nor-non-percipient — the Tathagata, the Worthy One, the Perfectly Self-Awakened One, is declared the foremost of them. Those who have confidence in the Buddha have confidence in the foremost, and for those with confidence in the foremost the result is foremost.',
            },
            # ‼ CHECK [IMG_0283.PNG]: FIVE PRINTED LINES KEPT AS ONE VERSE,
            #   with the line breaks written as \n. The book sets this as a
            #   centred five-line stanza between two prose paragraphs, and the
            #   breaks are the verse's own, not justification. Say if you
            #   would rather have five verses — it would change the numbering
            #   of everything after it.
            {
                'number': 2,
                'pali': 'ยังกิญจิ วิตตัง อิธะ วา หุรัง วา\nสัคเคสุ วา ยัง ระตะนัง ปะณีตัง\nนะ โน สะมัง อัตถิ ตะถาคะเตนะ\nอิทัมปิ พุทเธ ระตะนัง ปะณีตัง\nเอเตนะ สัจเจนะ สุวัตถิ โหตุ.',
                'pali_roman': 'yaṅkiñci vittaṃ idha vā huraṃ vā\nsaggesu vā yaṃ ratanaṃ paṇītaṃ\nna no samaṃ atthi tathāgatena\nidampi buddhe ratanaṃ paṇītaṃ\netena saccena suvatthi hotu.',
                'thai': '',
                'paiboon': '',
                'english': 'Whatever wealth there is here or beyond, or whatever excellent treasure is in the heavens, there is none equal to the Tathagata. This too is an excellent treasure in the Buddha. By this truth may there be well-being.',
            },
            # ‼ CHECK [IMG_0283.PNG]: WORD REJOINED ACROSS A HYPHEN:
            #   อัคคะมักขายะติ breaks as 'อัคคะมัก-' / 'ขายะติ'.
            #   Justification, not spelling.
            {
                'number': 3,
                'pali': 'ยาวะตา ธัมมา สังขะตา วา อะสังขะตา วา, วิราโค เตสัง อัคคะมักขายะติ, ยะทิทัง มะทะนิมมะทะโน ปิปาสะวินะโย อาละยะสะมุคฆาโต วัฏฏูปัจเฉโท ตัณหักขะโย วิราโค นิโรโธ นิพพานัง, เย โข วิราคะธัมเม ปะสันนา, อัคเค เต ปะสันนา, อัคเค โข ปะนะ ปะสันนานัง อัคโค วิปาโก.',
                'pali_roman': 'yāvatā dhammā saṅkhatā vā asaṅkhatā vā, virāgo tesaṃ aggamakkhāyati, yadidaṃ madanimmadano pipāsavinayo ālayasamugghāto vaṭṭūpacchedo taṇhakkhayo virāgo nirodho nibbānaṃ, ye kho virāgadhamme pasannā, agge te pasannā, agge kho pana pasannānaṃ aggo vipāko.',
                'thai': '',
                'paiboon': '',
                'english': 'As far as there are things conditioned or unconditioned, dispassion is declared the foremost of them — that is, the crushing of pride, the removal of thirst, the uprooting of clinging, the cutting off of the round, the destruction of craving, dispassion, cessation, nibbana. Those who have confidence in the Dhamma of dispassion have confidence in the foremost, and for those with confidence in the foremost the result is foremost.',
            },
            {
                'number': 4,
                'page': 21,
                'pali': 'ขะยัง วิราคัง อะมะตัง ปะณีตัง\nยะทัชฌะคา สัก์ยะมุนี สะมาหิโต\nนะ เตนะ ธัมเมนะ สะมัตถิ กิญจิ\nอิทัมปิ ธัมเม ระตะนัง ปะณีตัง\nเอเตนะ สัจเจนะ สุวัตถิ โหตุ.',
                'pali_roman': 'khayaṃ virāgaṃ amataṃ paṇītaṃ\nyadajjhagā sakyamunī samāhito\nna tena dhammena samatthi kiñci\nidampi dhamme ratanaṃ paṇītaṃ\netena saccena suvatthi hotu.',
                'thai': '',
                'paiboon': '',
                'english': 'Cessation, dispassion, the deathless, the sublime — which the Sakyan sage, composed, attained: there is nothing whatever equal to that Dhamma. This too is a precious jewel in the Dhamma. By this truth may there be well-being.',
            },
            # ‼ CHECK [IMG_0283a.PNG]: The prose passage breaks อัคคะมักขายะติ
            #   across the line end as อัคคะมัก- / ขายะติ. Rejoined and the
            #   hyphen dropped, per the rule that a justified line break is
            #   typesetting and not spelling. The same break occurs in verse
            #   7.
            {
                'number': 5,
                'pali': 'ยาวะตา ธัมมา สังขะตา, อะริโย อัฏฐังคิโก มัคโค เตสัง อัคคะมักขายะติ. เสยยะถีทัง: สัมมาทิฏฐิ สัมมาสังกัปโป, สัมมาวาจา สัมมากัมมันโต สัมมาอาชีโว, สัมมาวายาโม สัมมาสะติ สัมมาสะมาธิ. เย โข อะริยะมัคคะธัมเม ปะสันนา อัคเค เต ปะสันนา, อัคเค โข ปะนะ ปะสันนานัง อัคโค วิปาโก.',
                'pali_roman': 'yāvatā dhammā saṅkhatā, ariyo aṭṭhaṅgiko maggo tesaṃ aggamakkhāyati. seyyathīdaṃ: sammādiṭṭhi sammāsaṅkappo, sammāvācā sammākammanto sammāājīvo, sammāvāyāmo sammāsati sammāsamādhi. ye kho ariyamaggadhamme pasannā agge te pasannā, agge kho pana pasannānaṃ aggo vipāko.',
                'thai': '',
                'paiboon': '',
                'english': 'Of whatever states are conditioned, the noble eightfold path is declared the foremost of them — that is to say: right view, right intention, right speech, right action, right livelihood, right effort, right mindfulness, right concentration. Those who have confidence in the states of the noble path have confidence in the foremost; and for those who have confidence in the foremost, the result is foremost.',
            },
            # ‼ CHECK [IMG_0283a.PNG]: The page prints อิทัมปิ สังเฆ ระตะนัง
            #   ปะณีตัง — saṅghe — in the yaṃ buddhaseṭṭho stanza, where
            #   standard editions of the Ratanasutta read ธัมเม, dhamme. The
            #   word is set large and is not in doubt: ส ั ง เ ฆ, checked at
            #   maximum magnification. Reproduced as printed and NOT
            #   corrected. This one is worth your eye, because it changes
            #   which of the Three Jewels the verse is about.
            # ‼ CHECK [IMG_0283a.PNG]: A single small dot sits after วิชชะติ
            #   on the third line, separated by a clear space, where no other
            #   line of the stanza carries punctuation. It may be a full stop
            #   or it may be a speck on the paper. NOT reproduced — putting a
            #   stop into the middle of a chanted stanza on the strength of a
            #   possible speck is the worse error. Please glance at it.
            {
                'number': 6,
                'pali': 'ยัมพุทธะเสฏโฐ ปะริวัณณะยี สุจิง\nสะมาธิมานันตะริกัญญะมาหุ\nสะมาธินา เตนะ สะโม นะ วิชชะติ\nอิทัมปิ สังเฆ ระตะนัง ปะณีตัง\nเอเตนะ สัจเจนะ สุวัตถิ โหตุ.',
                'pali_roman': 'yaṃ buddhaseṭṭho parivaṇṇayī suciṃ\nsamādhimānantarikaññamāhu\nsamādhinā tena samo na vijjati\nidampi saṅghe ratanaṃ paṇītaṃ\netena saccena suvatthi hotu.',
                'thai': '',
                'paiboon': '',
                'english': 'That purity which the best of Buddhas extolled, the concentration they call immediate — no equal to that concentration is found. This too is a precious jewel in the Sangha. By this truth may there be well-being.',
            },
            {
                'number': 7,
                'pali': 'ยาวะตา สังฆา วา คะณา วา, ตะถาคะตะสาวะกะสังโฆ เตสัง อัคคะมักขายะติ, ยะทิทัง: จัตตาริ ปุริสะยุคานิ อัฏฐะ ปุริสะปุคคะลา. เย โข สังเฆ ปะสันนา, อัคเค เต ปะสันนา, อัคเค โข ปะนะ ปะสันนานัง อัคโค วิปาโก.',
                'pali_roman': 'yāvatā saṅghā vā gaṇā vā, tathāgatasāvakasaṅgho tesaṃ aggamakkhāyati, yadidaṃ: cattāri purisayugāni aṭṭha purisapuggalā. ye kho saṅghe pasannā, agge te pasannā, agge kho pana pasannānaṃ aggo vipāko.',
                'thai': '',
                'paiboon': '',
                'english': "Of whatever communities or assemblies there are, the Sangha of the Tathāgata's disciples is declared the foremost of them — that is to say: the four pairs of persons, the eight kinds of individuals. Those who have confidence in the Sangha have confidence in the foremost; and for those who have confidence in the foremost, the result is foremost.",
            },
            {
                'number': 8,
                'pali': 'เย ปุคคะลา อัฏฐะสะตัง ปะสัฏฐา\nจัตตาริ เอตานิ ยุคานิ โหนติ.\nเต ทักขิเณยยา สุคะตัสสะ สาวะกา\nเอเตสุ ทินนานิ มะหัปผะลานิ\nอิทัมปิ สังเฆ ระตะนัง ปะณีตัง\nเอเตนะ สัจเจนะ สุวัตถิ โหตุ.',
                'pali_roman': 'ye puggalā aṭṭhasataṃ pasatthā\ncattāri etāni yugāni honti.\nte dakkhiṇeyyā sugatassa sāvakā\netesu dinnāni mahapphalāni\nidampi saṅghe ratanaṃ paṇītaṃ\netena saccena suvatthi hotu.',
                'thai': '',
                'paiboon': '',
                'english': 'Those eight persons, praised by the good, who are these four pairs — they are the disciples of the Fortunate One, worthy of offerings; what is given to them bears great fruit. This too is a precious jewel in the Sangha. By this truth may there be well-being.',
            },
            # ‼ CHECK [IMG_0283a.PNG]: This stanza STRADDLES the page turn: เย
            #   สุปปะยุตตา, นิกกามิโน and เต ปัตติปัตตา อะมะตัง วิคัยหะ are on
            #   page 21; ลัทธา มุธา, อิทัมปิ สังเฆ and เอเตนะ สัจเจนะ are on
            #   page 22. Filed on 21, the page it starts on, so the reading
            #   view will show the whole stanza a page early. Nothing else
            #   fits the data model.
            # ‼ CHECK [IMG_0283a.PNG]: ทัฬเหนะ with ฬ — this one IS legible in
            #   the photograph, the tall ascender of ฬ is clear. Recorded as
            #   read.
            {
                'number': 9,
                'pali': 'เย สุปปะยุตตา มะนะสา ทัฬเหนะ\nนิกกามิโน โคตะมะสาสะนัมหิ\nเต ปัตติปัตตา อะมะตัง วิคัยหะ\nลัทธา มุธา นิพพุติง ภุญชะมานา\nอิทัมปิ สังเฆ ระตะนัง ปะณีตัง\nเอเตนะ สัจเจนะ สุวัตถิ โหตุ.',
                'pali_roman': 'ye suppayuttā manasā daḷhena\nnikkāmino gotamasāsanamhi\nte pattipattā amataṃ vigayha\nladdhā mudhā nibbutiṃ bhuñjamānā\nidampi saṅghe ratanaṃ paṇītaṃ\netena saccena suvatthi hotu.',
                'thai': '',
                'paiboon': '',
                'english': "Those who, well applied with a firm mind, are free of desire in Gotama's dispensation — they have reached attainment, plunged into the deathless, and enjoy the peace they have won at no cost. This too is a precious jewel in the Sangha. By this truth may there be well-being.",
            },
            # ‼ CHECK [IMG_0284.PNG]: ‼ READING HAZARD. The photograph shows
            #   อะวิรุพหิฉันทา, with what looks like พ. It has been written
            #   here as อะวิรุฬหิฉันทา with ฬ, and that is a JUDGEMENT, not a
            #   reading. Two things justify it and both are in your hands
            #   already: (1) you read page 23 line 19 off the physical book on
            #   2026-08-08 and confirmed วิรุฬหะ with ฬ, where this same
            #   photograph set shows พ at maximum magnification; (2) the app's
            #   own อะสัมมุฬโห, four lines down this very page, was typed by
            #   you from the book with ฬ — and the photograph shows พ there
            #   too. So the camera renders ฬ as พ in this typeface, twice
            #   proven. PLEASE CONFIRM THIS ONE WORD AT THE BOOK; it is a
            #   chanted line and one character decides it.
            {
                'number': 10,
                'page': 22,
                'pali': 'ขีณัง ปุราณัง นะวัง นัตถิ สัมภะวัง\nวิรัตตะจิตตายะติเก ภะวัส์มิง\nเต ขีณะพีชา อะวิรุฬหิฉันทา\nนิพพันติ ธีรา ยะถายัมปะทีโป\nอิทัมปิ สังเฆ ระตะนัง ปะณีตัง\nเอเตนะ สัจเจนะ สุวัตถิ โหตุ.',
                'pali_roman': 'khīṇaṃ purāṇaṃ navaṃ natthi sambhavaṃ\nvirattacittāyatike bhavasmiṃ\nte khīṇabījā avirūḷhichandā\nnibbanti dhīrā yathāyampadīpo\nidampi saṅghe ratanaṃ paṇītaṃ\netena saccena suvatthi hotu.',
                'thai': '',
                'paiboon': '',
                'english': 'The old is destroyed, no new becoming arises; their minds are dispassionate towards future existence. With their seeds destroyed and no desire for growth, the wise go out like this lamp. This too is a precious jewel in the Sangha. By this truth may there be well-being.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0286.PNG]: TWO COLUMNS on both pages, read across the
        #   row. First pairing on page 24: นิธิง นิเธติ ปุริโส (left) +
        #   คัมภีเร อุทะกันติเก (right) = verse 1. Reading down the left
        #   column alone gives a run of unfinished half-lines, which is the
        #   honest test and it fails, so the page is two columns.
        # ‼ CHECK [IMG_0287.PNG]: The citation reads ขุ.ขุ. เตมิย. — Khuddaka-
        #   nikāya, Khuddakapāṭha, but with เตมิย (Temiya) attached, which is
        #   a Jātaka name and reads oddly beside ขุ.ขุ. Page 23's footnote has
        #   the same เตมิย against ขุ.ชา. Reproduced verbatim in both places;
        #   not expanded and not corrected. Worth knowing whether the book is
        #   using เตมิย as a volume marker.
        'id': 'nidhikanda-gatha',
        'title_thai': 'นิธิกัณฑะคาถา',
        'title_pali': 'Nidhikaṇḍagāthā',
        'title_roman': '',
        'title_english': 'The Verses on the Treasure Store',
        'book_number': 5,
        'page_start': 24,
        'source_printed': 'ขุ.ขุ. เตมิย. 2/11',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'closing': {
            'pali': 'นิธิกัณฑะคาถา นิฏฐิตา.',
            'pali_roman': 'nidhikaṇḍagāthā niṭṭhitā.',
            'thai': '',
            'paiboon': '',
            'english': 'Here end the Verses on the Treasure Store.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'นิธิง นิเธติ ปุริโส คัมภีเร อุทะกันติเก',
                'pali_roman': 'nidhiṃ nidheti puriso gambhīre udakantike',
                'thai': '',
                'paiboon': '',
                'english': "A man buries a store of treasure deep down, at the water's edge,",
            },
            {
                'number': 2,
                'pali': 'อัตเถ กิจเจ สะมุปปันเน อัตถายะ เม ภะวิสสะติ.',
                'pali_roman': 'atthe kicce samuppanne atthāya me bhavissati.',
                'thai': '',
                'paiboon': '',
                'english': 'thinking: when a need or a duty arises, it will serve my purpose.',
            },
            # ‼ CHECK [IMG_0286.PNG]: ‼ READING HAZARD, same as page 22. The
            #   photograph shows ปีพิตัสสะ with what looks like พ; written
            #   here as ปีฬิตัสสะ with ฬ. Same justification as elsewhere in
            #   this batch — the camera cannot render ฬ in this typeface,
            #   proven twice against your own readings. PLEASE CONFIRM AT THE
            #   BOOK.
            {
                'number': 3,
                'pali': 'ราชะโต วา ทุรุตตัสสะ โจระโต ปีฬิตัสสะ วา',
                'pali_roman': 'rājato vā duruttassa corato pīḷitassa vā',
                'thai': '',
                'paiboon': '',
                'english': 'If he is denounced by a king, or oppressed by a thief,',
            },
            {
                'number': 4,
                'pali': 'อิณัสสะ วา ปะโมกขายะ ทุพภิกเข อาปะทาสุ วา',
                'pali_roman': 'iṇassa vā pamokkhāya dubbhikkhe āpadāsu vā',
                'thai': '',
                'paiboon': '',
                'english': 'or for release from a debt, or in famine, or in calamity —',
            },
            {
                'number': 5,
                'pali': 'เอตะทัตถายะ โลกัส์มิง นิธิ นามะ นิธิยยะติ.',
                'pali_roman': 'etadatthāya lokasmiṃ nidhi nāma nidhiyyati.',
                'thai': '',
                'paiboon': '',
                'english': 'it is for such purposes in the world that what is called a treasure store is buried.',
            },
            {
                'number': 6,
                'pali': 'ตาวัสสุนิหิโต สันโต คัมภีเร อุทะกันติเก',
                'pali_roman': 'tāvassunihito santo gambhīre udakantike',
                'thai': '',
                'paiboon': '',
                'english': "Yet however well it lies buried, deep down at the water's edge,",
            },
            {
                'number': 7,
                'pali': 'นะ สัพโพ สัพพะทา เยวะ ตัสสะ ตัง อุปะกัปปะติ',
                'pali_roman': 'na sabbo sabbadā yeva tassa taṃ upakappati',
                'thai': '',
                'paiboon': '',
                'english': 'not all of it, and not at all times, serves him when he needs it.',
            },
            {
                'number': 8,
                'pali': 'นิธิ วา ฐานา จะวะติ สัญญา วาสสะ วิมุยหะติ.',
                'pali_roman': 'nidhi vā ṭhānā cavati saññā vāssa vimuyhati.',
                'thai': '',
                'paiboon': '',
                'english': 'The store shifts from its place, or his memory of it is confounded.',
            },
            {
                'number': 9,
                'pali': 'นาคา วา อะปะนาเมนติ ยักขา วาปิ หะรันติ นัง',
                'pali_roman': 'nāgā vā apanāmenti yakkhā vāpi haranti naṃ',
                'thai': '',
                'paiboon': '',
                'english': 'Nāgas carry it away, or yakkhas make off with it,',
            },
            {
                'number': 10,
                'pali': 'อัปปิยา วาปิ ทายาทา อุทธะรันติ อะปัสสะโต.',
                'pali_roman': 'appiyā vāpi dāyādā uddharanti apassato.',
                'thai': '',
                'paiboon': '',
                'english': 'or heirs he has no love for dig it up while he is not looking.',
            },
            {
                'number': 11,
                'pali': 'ยะทา ปุญญักขะโย โหติ สัพพะเมตัง วินัสสะติ.',
                'pali_roman': 'yadā puññakkhayo hoti sabbametaṃ vinassati.',
                'thai': '',
                'paiboon': '',
                'english': 'And when his merit is exhausted, the whole of it is lost.',
            },
            # ‼ CHECK [IMG_0286.PNG]: The book marks a new stanza here by
            #   indenting the line rather than by any heading or blank line.
            #   The same indent appears at verse 18 and at verse 1 under the
            #   title. That indent is the ONLY stanza division the page gives,
            #   and there is nowhere in the data model to keep it — `section`
            #   would require inventing a name the book does not print, so
            #   none has been added. Three stanza openings are therefore lost.
            #   Say if you would rather they were marked.
            {
                'number': 12,
                'pali': 'ยัสสะ ทาเนนะ สีเลนะ สัญญะเมนะ ทะเมนะ จะ',
                'pali_roman': 'yassa dānena sīlena saññamena damena ca',
                'thai': '',
                'paiboon': '',
                'english': 'But the one who, by giving and by virtue, by restraint and by self-mastery,',
            },
            {
                'number': 13,
                'pali': 'นิธิ สุนิหิโต โหติ อิตถิยา ปุริสัสสะ วา',
                'pali_roman': 'nidhi sunihito hoti itthiyā purisassa vā',
                'thai': '',
                'paiboon': '',
                'english': 'has a treasure store well laid up — a woman or a man alike —',
            },
            {
                'number': 14,
                'pali': 'เจติยัมหิ จะ สังเฆ วา ปุคคะเล อะติถีสุ วา',
                'pali_roman': 'cetiyamhi ca saṅghe vā puggale atithīsu vā',
                'thai': '',
                'paiboon': '',
                'english': 'in a shrine, or in the Sangha, in a person, or in guests,',
            },
            {
                'number': 15,
                'pali': 'มาตะริ ปิตะริ วาปิ อะโถ เชฏฐัมหิ ภาตะริ',
                'pali_roman': 'mātari pitari vāpi atho jeṭṭhamhi bhātari',
                'thai': '',
                'paiboon': '',
                'english': 'in a mother, in a father, or in an elder brother —',
            },
            {
                'number': 16,
                'pali': 'เอโส นิธิ สุนิหิโต อะเชยโย อะนุคามิโก',
                'pali_roman': 'eso nidhi sunihito ajeyyo anugāmiko',
                'thai': '',
                'paiboon': '',
                'english': 'that is a store well laid up, unassailable, and it follows him.',
            },
            {
                'number': 17,
                'pali': 'ปะหายะ คะมะนีเยสุ เอตัง อาทายะ คัจฉะติ.',
                'pali_roman': 'pahāya gamanīyesu etaṃ ādāya gacchati.',
                'thai': '',
                'paiboon': '',
                'english': 'Leaving behind what must be left, he takes this with him when he goes.',
            },
            {
                'number': 18,
                'pali': 'อะสาธาระณะมัญเญสัง อะโจระหะระโณ นิธิ',
                'pali_roman': 'asādhāraṇamaññesaṃ acoraharaṇo nidhi',
                'thai': '',
                'paiboon': '',
                'english': 'A store no one else shares, that no thief can carry off —',
            },
            {
                'number': 19,
                'pali': 'กะยิราถะ ธีโร ปุญญานิ โย นิธิ อะนุคามิโก.',
                'pali_roman': 'kayirātha dhīro puññāni yo nidhi anugāmiko.',
                'thai': '',
                'paiboon': '',
                'english': 'let the wise make merit, the store that follows after.',
            },
            {
                'number': 20,
                'pali': 'เอสะ เทวะมะนุสสานัง สัพพะกามะทะโท นิธิ',
                'pali_roman': 'esa devamanussānaṃ sabbakāmadado nidhi',
                'thai': '',
                'paiboon': '',
                'english': 'This is the store that gives gods and men everything they wish for;',
            },
            {
                'number': 21,
                'pali': 'ยัง ยัง เทวาภิปัตเถนติ สัพพะเมเตนะ ลัพภะติ.',
                'pali_roman': 'yaṃ yaṃ devābhipatthenti sabbametena labbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'whatever they long for, all of it is obtained by this.',
            },
            {
                'number': 22,
                'pali': 'สุวัณณะตา สุสะระตา สุสัณฐานัง สุรูปะตา',
                'pali_roman': 'suvaṇṇatā susaratā susaṇṭhānaṃ surūpatā',
                'thai': '',
                'paiboon': '',
                'english': 'A fair complexion, a fine voice, good proportion, beauty of form,',
            },
            {
                'number': 23,
                'pali': 'อาธิปัจจัง ปะริวาโร สัพพะเมเตนะ ลัพภะติ.',
                'pali_roman': 'ādhipaccaṃ parivāro sabbametena labbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'sovereignty, a retinue — all of it is obtained by this.',
            },
            {
                'number': 24,
                'pali': 'ปะเทสะรัชชัง อิสสะริยัง จักกะวัตติสุขัง ปิยัง',
                'pali_roman': 'padesarajjaṃ issariyaṃ cakkavattisukhaṃ piyaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'Kingship over a region, lordship, the dear happiness of a wheel-turning monarch,',
            },
            {
                'number': 25,
                'pali': 'เทวะรัชชัมปิ ทิพเพสุ สัพพะเมเตนะ ลัพภะติ.',
                'pali_roman': 'devarajjampi dibbesu sabbametena labbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'and even sovereignty among the gods in the heavens — all of it is obtained by this.',
            },
            {
                'number': 26,
                'page': 25,
                'pali': 'มานุสสิกา จะ สัมปัตติ เทวะโลเก จะ ยา ระติ',
                'pali_roman': 'mānussikā ca sampatti devaloke ca yā rati',
                'thai': '',
                'paiboon': '',
                'english': 'Human good fortune, and whatever delight there is in the world of the gods,',
            },
            {
                'number': 27,
                'pali': 'ยา จะ นิพพานะสัมปัตติ สัพพะเมเตนะ ลัพภะติ.',
                'pali_roman': 'yā ca nibbānasampatti sabbametena labbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'and the attainment of Nibbāna itself — all of it is obtained by this.',
            },
            {
                'number': 28,
                'pali': 'มิตตะสัมปะทะมาคัมมะ โยนิโส เจ ปะยุญชะโต',
                'pali_roman': 'mittasampadamāgamma yoniso ce payuñjato',
                'thai': '',
                'paiboon': '',
                'english': 'Coming upon the blessing of good friends, if one applies oneself wisely,',
            },
            {
                'number': 29,
                'pali': 'วิชชาวิมุตติวะสีภาโว สัพพะเมเตนะ ลัพภะติ.',
                'pali_roman': 'vijjāvimuttivasībhāvo sabbametena labbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'mastery in knowledge and release — all of it is obtained by this.',
            },
            {
                'number': 30,
                'pali': 'ปะฏิสัมภิทา วิโมกขา จะ ยา จะ สาวะกะปาระมี',
                'pali_roman': 'paṭisambhidā vimokkhā ca yā ca sāvakapāramī',
                'thai': '',
                'paiboon': '',
                'english': 'The analytical knowledges, the liberations, and the perfection of a disciple,',
            },
            {
                'number': 31,
                'pali': 'ปัจเจกะโพธิ พุทธะภูมิ สัพพะเมเตนะ ลัพภะติ.',
                'pali_roman': 'paccekabodhi buddhabhūmi sabbametena labbhati.',
                'thai': '',
                'paiboon': '',
                'english': 'solitary awakening, and the ground of a Buddha — all of it is obtained by this.',
            },
            {
                'number': 32,
                'pali': 'เอวัง มะหัตถิกา เอสา ยะทิทัง ปุญญะสัมปะทา',
                'pali_roman': 'evaṃ mahatthikā esā yadidaṃ puññasampadā',
                'thai': '',
                'paiboon': '',
                'english': 'So greatly profitable is this, the blessing of merit;',
            },
            # ‼ CHECK [IMG_0287.PNG]: The superscript 1 sits on the last word
            #   of THIS chant, กะตะปุญญะตันติ., and the footnote at the foot
            #   of page 25 reads ขุ.ขุ. เตมิย. 2/11 — so it is this chant's
            #   citation and not that of ธัมมะคาระวาทิคาถา, which merely
            #   begins on the same page. Recorded as source_printed. The
            #   numbers 2/11 are printed with an underline; the underline is
            #   typography and is not reproduced.
            {
                'number': 33,
                'pali': 'ตัส์มา ธีรา ปะสังสันติ ปัณฑิตา กะตะปุญญะตันติ.',
                'pali_roman': 'tasmā dhīrā pasaṃsanti paṇḍitā katapuññatanti.',
                'thai': '',
                'paiboon': '',
                'english': 'and therefore the steadfast and the wise praise the making of merit.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0288.PNG]: This chant has no footnote and no citation
        #   marker on either page. Page 25's footnote belongs to Nidhikaṇḍa
        #   above it and page 26's to Devatādissa below it. `source_printed`
        #   is therefore left off rather than borrowed from a neighbour — the
        #   fault this book has already made twice.
        # ‼ CHECK [IMG_0287.PNG]: Verses 13-14 (ธัมโม หะเว รักขะติ ธัมมะจาริง
        #   / ธัมโม สุจิณโณ สุขะมาวะหาติ.) are printed again word for word on
        #   page 29 inside Saccapānavidhyānurūpagāthā, verses 3-4 of that
        #   chant. Two chants in this book quoting the same couplet. Set in
        #   both places, as the book does; not treated as a repeat.
        'id': 'dhammagaravadi-gatha',
        'title_thai': 'ธัมมะคาระวาทิคาถา',
        'title_pali': 'Dhammagāravādigāthā',
        'title_roman': '',
        'title_english': 'The Verses on Reverence for the Dhamma',
        'book_number': 6,
        'page_start': 25,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'closing': {
            'pali': 'ธัมมะคาระวาทิคาถา นิฏฐิตา.',
            'pali_roman': 'dhammagāravādigāthā niṭṭhitā.',
            'thai': '',
            'paiboon': '',
            'english': 'Here end the Verses on Reverence for the Dhamma.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'เย จะ อะตีตา สัมพุทธา เย จะ พุทธา อะนาคะตา',
                'pali_roman': 'ye ca atītā sambuddhā ye ca buddhā anāgatā',
                'thai': '',
                'paiboon': '',
                'english': 'Those fully awakened ones who have been, and those Buddhas yet to come,',
            },
            {
                'number': 2,
                'pali': 'โย เจตะระหิ สัมพุทโธ พะหุนนัง โสกะนาสะโน.',
                'pali_roman': 'yo cetarahi sambuddho bahunnaṃ sokanāsano.',
                'thai': '',
                'paiboon': '',
                'english': 'and he who is fully awakened now, destroyer of the sorrow of many —',
            },
            {
                'number': 3,
                'pali': 'สัพเพ สัทธัมมะคะรุโน วิหะริงสุ วิหาติ จะ',
                'pali_roman': 'sabbe saddhammagaruno vihariṃsu vihāti ca',
                'thai': '',
                'paiboon': '',
                'english': 'all of them dwelt, and dwell, revering the true Dhamma;',
            },
            {
                'number': 4,
                'pali': 'อะถาปิ วิหะริสสันติ เอสา พุทธานะ ธัมมะตา.',
                'pali_roman': 'athāpi viharissanti esā buddhāna dhammatā.',
                'thai': '',
                'paiboon': '',
                'english': 'and so too they will dwell. This is the nature of Buddhas.',
            },
            {
                'number': 5,
                'pali': 'ตัส์มา หิ อัตตะกาเมนะ มะหัตตะมะภิกังขะตา',
                'pali_roman': 'tasmā hi attakāmena mahattamabhikaṅkhatā',
                'thai': '',
                'paiboon': '',
                'english': 'Therefore one who loves himself, who aspires to greatness,',
            },
            {
                'number': 6,
                'pali': 'สัทธัมโม คะรุกาตัพโพ สะรัง พุทธานะ สาสะนัง.',
                'pali_roman': 'saddhammo garukātabbo saraṃ buddhāna sāsanaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'should revere the true Dhamma, remembering the teaching of the Buddhas.',
            },
            {
                'number': 7,
                'pali': 'ทุททะทัง ทะทะมานานัง ทุกกะรัง กัมมะกุพพะตัง',
                'pali_roman': 'duddadaṃ dadamānānaṃ dukkaraṃ kammakubbataṃ',
                'thai': '',
                'paiboon': '',
                'english': 'Of those who give what is hard to give, who do what is hard to do,',
            },
            {
                'number': 8,
                'pali': 'อะสันโต นานุกุพพันติ สะตัง ธัมโม ทุรันวะโย.',
                'pali_roman': 'asanto nānukubbanti sataṃ dhammo duranvayo.',
                'thai': '',
                'paiboon': '',
                'english': 'the bad do not follow suit; the way of the good is hard to follow.',
            },
            {
                'number': 9,
                'pali': 'ตัส์มา สะตัญจะ อะสะตัญจะ นานา โหติ อิโต คะติ',
                'pali_roman': 'tasmā satañca asatañca nānā hoti ito gati',
                'thai': '',
                'paiboon': '',
                'english': 'And so the destination from here differs for the good and for the bad:',
            },
            {
                'number': 10,
                'pali': 'อะสันโต นิระยัง ยันติ สันโต สัคคะปะรายะนา.',
                'pali_roman': 'asanto nirayaṃ yanti santo saggaparāyanā.',
                'thai': '',
                'paiboon': '',
                'english': 'the bad go to hell; the good have heaven as their destination.',
            },
            {
                'number': 11,
                'pali': 'นะ หิ ธัมโม อะธัมโม จะ อุโภ จะ สะมะวิปากิโน',
                'pali_roman': 'na hi dhammo adhammo ca ubho ca samavipākino',
                'thai': '',
                'paiboon': '',
                'english': 'For Dhamma and what is against Dhamma do not ripen alike:',
            },
            {
                'number': 12,
                'pali': 'อะธัมโม นิระยัง เนติ, ธัมโม ปาเปติ สุคะติง.',
                'pali_roman': 'adhammo nirayaṃ neti, dhammo pāpeti sugatiṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'what is against Dhamma leads to hell; Dhamma brings one to a good destination.',
            },
            # ‼ CHECK [IMG_0287.PNG]: THE SETTING CHANGES HERE, mid-chant,
            #   with no heading and no blank line. Verses 1-12 are two
            #   columns, two pādas to a line; verses 13-20 are centred single-
            #   column, ONE pāda to a line; verses 21-30 go back to two
            #   columns. The change of line length is the only signal. It has
            #   been followed rather than smoothed, so the verse units are
            #   deliberately uneven.
            {
                'number': 13,
                'pali': 'ธัมโม หะเว รักขะติ ธัมมะจาริง',
                'pali_roman': 'dhammo have rakkhati dhammacāriṃ',
                'thai': '',
                'paiboon': '',
                'english': 'Dhamma indeed protects the one who lives by Dhamma;',
            },
            {
                'number': 14,
                'pali': 'ธัมโม สุจิณโณ สุขะมาวะหาติ.',
                'pali_roman': 'dhammo suciṇṇo sukhamāvahāti.',
                'thai': '',
                'paiboon': '',
                'english': 'Dhamma well practised brings happiness.',
            },
            # ‼ CHECK [IMG_0288.PNG]: The single-column setting carries over
            #   the page turn and runs for six more lines at the top of page
            #   26 before reverting to two columns at verse 21. Confirm the
            #   first pairing after the change: จันทะนัง ตะคะรัง วาปิ (left) +
            #   อุปปะลัง อะถะ วัสสิกี (right) = verse 21.
            {
                'number': 15,
                'page': 26,
                'pali': 'เอสานิสังโส ธัมเม สุจิณเณ',
                'pali_roman': 'esānisaṃso dhamme suciṇṇe',
                'thai': '',
                'paiboon': '',
                'english': 'This is the benefit of Dhamma well practised:',
            },
            {
                'number': 16,
                'pali': 'นะ ทุคคะติง คัจฉันติ ธัมมะจารี.',
                'pali_roman': 'na duggatiṃ gacchanti dhammacārī.',
                'thai': '',
                'paiboon': '',
                'english': 'one who lives by Dhamma does not go to a bad destination.',
            },
            {
                'number': 17,
                'pali': 'นะ ปุปผะคันโธ ปะฏิวาตะเมติ',
                'pali_roman': 'na pupphagandho paṭivātameti',
                'thai': '',
                'paiboon': '',
                'english': 'The scent of flowers does not travel against the wind,',
            },
            {
                'number': 18,
                'pali': 'นะ จันทะนัง ตะคะระมัลลิกา วา.',
                'pali_roman': 'na candanaṃ tagaramallikā vā.',
                'thai': '',
                'paiboon': '',
                'english': 'nor sandalwood, nor tagara, nor jasmine.',
            },
            {
                'number': 19,
                'pali': 'สะตัญจะ คันโธ ปะฏิวาตะเมติ',
                'pali_roman': 'satañca gandho paṭivātameti',
                'thai': '',
                'paiboon': '',
                'english': 'But the fragrance of the good does travel against the wind;',
            },
            {
                'number': 20,
                'pali': 'สัพพา ทิสา สัปปุริโส ปะวายะติ.',
                'pali_roman': 'sabbā disā sappuriso pavāyati.',
                'thai': '',
                'paiboon': '',
                'english': 'a true person perfumes every quarter.',
            },
            {
                'number': 21,
                'pali': 'จันทะนัง ตะคะรัง วาปิ อุปปะลัง อะถะ วัสสิกี',
                'pali_roman': 'candanaṃ tagaraṃ vāpi uppalaṃ atha vassikī',
                'thai': '',
                'paiboon': '',
                'english': 'Sandalwood or tagara, the blue lotus, or the jasmine —',
            },
            {
                'number': 22,
                'pali': 'เอเตสัง คันธะชาตานัง สีละคันโธ อะนุตตะโร.',
                'pali_roman': 'etesaṃ gandhajātānaṃ sīlagandho anuttaro.',
                'thai': '',
                'paiboon': '',
                'english': 'of all these kinds of fragrance, the fragrance of virtue is unsurpassed.',
            },
            # ‼ CHECK [IMG_0288.PNG]: The page prints ตะคะระจันทะนิ, ending in
            #   -นิ where standard editions read -นี (tagaracandanī).
            #   Reproduced as printed, not lengthened.
            {
                'number': 23,
                'pali': 'อัปปะมัตโต อะยัง คันโธ ย์วายัง ตะคะระจันทะนิ',
                'pali_roman': 'appamatto ayaṃ gandho yvāyaṃ tagaracandani',
                'thai': '',
                'paiboon': '',
                'english': 'Slight is this fragrance, that of tagara and sandalwood;',
            },
            {
                'number': 24,
                'pali': 'โย จะ สีละวะตัง คันโธ วาติ เทเวสุ อุตตะโม.',
                'pali_roman': 'yo ca sīlavataṃ gandho vāti devesu uttamo.',
                'thai': '',
                'paiboon': '',
                'english': 'but the fragrance of the virtuous blows even among the gods, and is supreme.',
            },
            {
                'number': 25,
                'pali': 'เตสัง สัมปันนะสีลานัง อัปปะมาทะวิหารินัง',
                'pali_roman': 'tesaṃ sampannasīlānaṃ appamādavihārinaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'Of those perfect in virtue, who dwell in heedfulness,',
            },
            {
                'number': 26,
                'pali': 'สัมมะทัญญา วิมุตตานัง มาโร มัคคัง นะ วินทะติ.',
                'pali_roman': 'sammadaññā vimuttānaṃ māro maggaṃ na vindati.',
                'thai': '',
                'paiboon': '',
                'english': 'liberated by right knowledge, Māra cannot find the path.',
            },
            {
                'number': 27,
                'pali': 'ยะถา สังการะธานัส์มิง อุชฌิตัส์มิง มะหาปะเถ',
                'pali_roman': 'yathā saṅkāradhānasmiṃ ujjhitasmiṃ mahāpathe',
                'thai': '',
                'paiboon': '',
                'english': 'Just as on a rubbish heap, cast aside beside the highway,',
            },
            {
                'number': 28,
                'pali': 'ปะทุมัง ตัตถะ ชาเยถะ สุจิคันธัง มะโนระมัง.',
                'pali_roman': 'padumaṃ tattha jāyetha sucigandhaṃ manoramaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'a lotus may spring up, sweet-scented and delighting the heart —',
            },
            {
                'number': 29,
                'pali': 'เอวัง สังการะภูเตสุ อันธะภูเต ปุถุชชะเน',
                'pali_roman': 'evaṃ saṅkārabhūtesu andhabhūte puthujjane',
                'thai': '',
                'paiboon': '',
                'english': 'so among those who have become as rubbish, among blind ordinary folk,',
            },
            {
                'number': 30,
                'pali': 'อะติโรจะติ ปัญญายะ สัมมาสัมพุทธะสาวะโกติ.',
                'pali_roman': 'atirocati paññāya sammāsambuddhasāvakoti.',
                'thai': '',
                'paiboon': '',
                'english': 'the disciple of the Fully Awakened One shines out in wisdom.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0291.PNG]: The closing วิหาระทานะคาถา นิฏฐิตา is
        #   printed with NO full stop, where every other closing in this batch
        #   ends in one. Reproduced as printed rather than regularised.
        # ‼ CHECK [IMG_0291.PNG]: Two columns throughout. First pairing: สีตัง
        #   อุณ์หัง ปะฏิหันติ (left) + ตะโต วาฬะมิคานิ จะ (right) = verse 1.
        'id': 'viharadana-gatha',
        'title_thai': 'วิหาระทานะคาถา',
        'title_pali': 'Vihāradānagāthā',
        'title_roman': '',
        'title_english': 'The Verses on the Gift of a Dwelling',
        'book_number': 11,
        'page_start': 29,
        'source_printed': 'วิ.จู. 7/87-88-121-2',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'closing': {
            'pali': 'วิหาระทานะคาถา นิฏฐิตา',
            'pali_roman': 'vihāradānagāthā niṭṭhitā',
            'thai': '',
            'paiboon': '',
            'english': 'Here end the Verses on the Gift of a Dwelling.',
        },
        'verses': [
            # ‼ CHECK [IMG_0291.PNG]: ‼ READING HAZARD, third instance in this
            #   batch. The photograph shows วาพะมิคานิ with what looks like พ;
            #   written here as วาฬะมิคานิ with ฬ, on the same evidence as the
            #   other two. PLEASE CONFIRM AT THE BOOK — this is a chanted line
            #   and one character decides it.
            {
                'number': 1,
                'pali': 'สีตัง อุณ์หัง ปะฏิหันติ ตะโต วาฬะมิคานิ จะ',
                'pali_roman': 'sītaṃ uṇhaṃ paṭihanti tato vāḷamigāni ca',
                'thai': '',
                'paiboon': '',
                'english': 'It keeps off cold and heat, and beasts of prey as well,',
            },
            {
                'number': 2,
                'pali': 'สิริงสะเป จะ มะกะเส สิสิเร จาปิ วุฏฐิโย.',
                'pali_roman': 'siriṃsape ca makase sisire cāpi vuṭṭhiyo.',
                'thai': '',
                'paiboon': '',
                'english': 'creeping things and mosquitoes, and the cold-season rains.',
            },
            {
                'number': 3,
                'pali': 'ตะโต วาตาตะโป โฆโร สัญชาโต ปะฏิหัญญะติ',
                'pali_roman': 'tato vātātapo ghoro sañjāto paṭihaññati',
                'thai': '',
                'paiboon': '',
                'english': 'And the fierce wind and heat, once arisen, are kept off by it —',
            },
            {
                'number': 4,
                'pali': 'เลนัตถัญจะ สุขัตถัญจะ ฌายิตุง จะ วิปัสสิตุง.',
                'pali_roman': 'lenatthañca sukhatthañca jhāyituṃ ca vipassituṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'for the sake of shelter and of ease, and in order to meditate and to see clearly.',
            },
            {
                'number': 5,
                'pali': 'วิหาระทานัง สังฆัสสะ อัคคัง พุทเธหิ วัณณิตัง',
                'pali_roman': 'vihāradānaṃ saṅghassa aggaṃ buddhehi vaṇṇitaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'The gift of a dwelling to the Sangha is praised by the Buddhas as foremost.',
            },
            {
                'number': 6,
                'pali': 'ตัส์มา หิ ปัณฑิโต โปโส สัมปัสสัง อัตถะมัตตะโน.',
                'pali_roman': 'tasmā hi paṇḍito poso sampassaṃ atthamattano.',
                'thai': '',
                'paiboon': '',
                'english': 'Therefore a wise man, seeing his own good,',
            },
            {
                'number': 7,
                'pali': 'วิหาเร การะเย รัมเม วาสะเยตถะ พะหุสสุเต',
                'pali_roman': 'vihāre kāraye ramme vāsayettha bahussute',
                'thai': '',
                'paiboon': '',
                'english': 'should have pleasant dwellings built and settle the deeply learned there.',
            },
            {
                'number': 8,
                'pali': 'เตสัง อันนัญจะ ปานัญจะ วัตถะเสนาสะนานิ จะ.',
                'pali_roman': 'tesaṃ annañca pānañca vatthasenāsanāni ca.',
                'thai': '',
                'paiboon': '',
                'english': 'To them food and drink, and robes and lodgings,',
            },
            {
                'number': 9,
                'pali': 'ทะเทยยะ อุชุภูเตสุ วิปปะสันเนนะ เจตะสา',
                'pali_roman': 'dadeyya ujubhūtesu vippasannena cetasā',
                'thai': '',
                'paiboon': '',
                'english': 'he should give to those grown upright, with a mind made clear.',
            },
            {
                'number': 10,
                'pali': 'เต ตัสสะ ธัมมัง เทเสนติ สัพพะทุกขาปะนูทะนัง.',
                'pali_roman': 'te tassa dhammaṃ desenti sabbadukkhāpanūdanaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'They teach him the Dhamma that dispels all suffering;',
            },
            # ‼ CHECK [IMG_0291.PNG]: The superscript 1 sits on the last word
            #   of this chant and the footnote reads วิ.จู. 7/87-88-121-2,
            #   with the numerals underlined. Recorded as source_printed; the
            #   underline is typography and is not reproduced. The reference
            #   has an unusual shape — four numbers rather than the
            #   volume/page pair the other footnotes use — and is reproduced
            #   exactly rather than reformatted.
            {
                'number': 11,
                'pali': 'ยัง โส ธัมมะมิธัญญายะ ปะรินิพพาต์ยะนาสะโวติ.',
                'pali_roman': 'yaṃ so dhammamidhaññāya parinibbātyanāsavoti.',
                'thai': '',
                'paiboon': '',
                'english': 'and having understood that Dhamma here, he attains final Nibbāna, free of the taints.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0291.PNG]: CONTINUES. The chant runs off the foot of
        #   page 29 and is NOT finished here. Verse 10 is the last complete
        #   line on the page. Do not write the rest.
        # ‼ CHECK [IMG_0291.PNG]: The title สัจจะปานะวิธ์ยานุรูปะคาถา is
        #   unusual and its thanthakhat cluster วิธ์ยา is hard to parse. The
        #   สารบัญ prints the same form at page 29, so the two agree.
        #   title_pali is a straight transliteration and may not be the form a
        #   standard edition would use.
        'id': 'saccapanavidhyanurupa-gatha',
        'title_thai': 'สัจจะปานะวิธ์ยานุรูปะคาถา',
        'title_pali': 'Saccapānavidhyānurūpagāthā',
        'title_roman': '',
        'title_english': 'The Verses Befitting the Drinking of Truth',
        'book_number': 12,
        'page_start': 29,
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'source_printed': 'ขุ.สุ. 25/360-361',
        'closing': {
            'pali': 'สัจจะปานะวิธ์ยานุรูปะคาถา นิฏฐิตา',
            'pali_roman': 'saccapānavidhyānurūpagāthā niṭṭhitā',
            'thai': '',
            'paiboon': '',
            'english': 'Here end the Verses Befitting the Drinking of Truth.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'สัจจัง เว อะมะตา วาจา เอสะ ธัมโม สะนันตะโน',
                'pali_roman': 'saccaṃ ve amatā vācā esa dhammo sanantano',
                'thai': '',
                'paiboon': '',
                'english': 'Truth indeed is deathless speech; this is the ancient law.',
            },
            {
                'number': 2,
                'pali': 'สัจเจ อัตเถ จะ ธัมเม จะ อะหุ สันโต ปะติฏฐิตา.',
                'pali_roman': 'sacce atthe ca dhamme ca ahu santo patiṭṭhitā.',
                'thai': '',
                'paiboon': '',
                'english': 'In truth, in what is good, and in Dhamma the good stand established.',
            },
            # ‼ CHECK [IMG_0291.PNG]: THE SETTING CHANGES TWICE inside this
            #   chant: two columns for verses 1-2, then four CENTRED single-
            #   column lines (verses 3-6), then two columns again from verse
            #   7. Followed as printed.
            {
                'number': 3,
                'pali': 'สัทธีธะ วิตตัง ปุริสัสสะ เสฏฐัง',
                'pali_roman': 'saddhīdha vittaṃ purisassa seṭṭhaṃ',
                'thai': '',
                'paiboon': '',
                'english': "Faith is a man's best wealth here;",
            },
            # ‼ CHECK [IMG_0291.PNG]: ธัมโม สุจิณโณ สุขะมาวะหาติ is printed
            #   here WITHOUT a full stop, where the same line closes
            #   Dhammagāravādigāthā on page 25 WITH one. Both reproduced as
            #   printed. The couplet at verses 3-4 here is the same couplet as
            #   verses 13-14 of that chant, quoted again.
            {
                'number': 4,
                'pali': 'ธัมโม สุจิณโณ สุขะมาวะหาติ',
                'pali_roman': 'dhammo suciṇṇo sukhamāvahāti',
                'thai': '',
                'paiboon': '',
                'english': 'Dhamma well practised brings happiness;',
            },
            {
                'number': 5,
                'pali': 'สัจจัง หะเว สาธุตะรัง ระสานัง',
                'pali_roman': 'saccaṃ have sādhutaraṃ rasānaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'truth is indeed the sweetest of flavours;',
            },
            {
                'number': 6,
                'pali': 'ปัญญาชีวีชีวิตะมาหุ เสฏฐัง.',
                'pali_roman': 'paññājīvījīvitamāhu seṭṭhaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'and the life of one living by wisdom they call the best.',
            },
            {
                'number': 7,
                'pali': 'สัททะหาโน อะระหะตัง ธัมมัง นิพพานะปัตติยา',
                'pali_roman': 'saddahāno arahataṃ dhammaṃ nibbānapattiyā',
                'thai': '',
                'paiboon': '',
                'english': 'Having faith in the Dhamma of the arahants, for the attainment of Nibbāna,',
            },
            {
                'number': 8,
                'pali': 'สุสสูสัง ละภะเต ปัญญัง อัปปะมัตโต วิจักขะโณ.',
                'pali_roman': 'sussūsaṃ labhate paññaṃ appamatto vicakkhaṇo.',
                'thai': '',
                'paiboon': '',
                'english': 'one who listens well gains wisdom — heedful and discerning.',
            },
            {
                'number': 9,
                'pali': 'ปะฏิรูปะการี ธุระวา อุฏฐาตา วินทะเต ธะนัง',
                'pali_roman': 'paṭirūpakārī dhuravā uṭṭhātā vindate dhanaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'Doing what is fitting, bearing the burden, rising to the task, one finds wealth;',
            },
            {
                'number': 10,
                'pali': 'สัจเจนะ กิตติง ปัปโปติ ทะทัง มิตตานิ คันถะติ.',
                'pali_roman': 'saccena kittiṃ pappoti dadaṃ mittāni ganthati.',
                'thai': '',
                'paiboon': '',
                'english': 'by truth one wins renown; by giving one binds friends.',
            },
            {
                'number': 11,
                'page': 30,
                'pali': 'ยัสเสเต จะตุโร ธัมมา สัทธัสสะ ฆะระเมสิโน',
                'pali_roman': 'yassete caturo dhammā saddhassa gharamesino',
                'thai': '',
                'paiboon': '',
                'english': 'In the faithful householder in whom these four things are found —',
            },
            {
                'number': 12,
                'pali': 'สัจจัง ธัมโม ธิติ จาโค สะ เว เปจจะ นะ โสจะติ.',
                'pali_roman': 'saccaṃ dhammo dhiti cāgo sa ve pecca na socati.',
                'thai': '',
                'paiboon': '',
                'english': 'truth, Dhamma, steadfastness, generosity — he indeed does not grieve when he has passed on.',
            },
            {
                'number': 13,
                'pali': 'อิงฆะ อัญเญปิ ปุจฉัสสุ ปุถู สะมะณะพ์ราห์มะเณ',
                'pali_roman': 'iṅgha aññepi pucchassu puthū samaṇabrāhmaṇe',
                'thai': '',
                'paiboon': '',
                'english': 'Come now, ask others also, the many ascetics and brahmins,',
            },
            # ‼ CHECK [IMG_0292.PNG]: Superscript 1 sits on this last line and
            #   points at the page's footnote ขุ.สุ. 25/360-361, now
            #   source_printed. The marker is on THIS chant's line, not on the
            #   chant below.
            {
                'number': 14,
                'pali': 'ยะทิ สัจจา ทะมา จาคา ขันต์ยา ภิยโยธะ วิชชะตีติ.',
                'pali_roman': 'yadi saccā damā cāgā khantyā bhiyyodha vijjatīti.',
                'thai': '',
                'paiboon': '',
                'english': 'whether anything greater than truth, self-control, generosity and patience is found here.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0292.PNG]: NEW CHANT, not previously in the app.
        #   Numbered 13 in the book, printed between Saccapanavidhyanurupa and
        #   Pabbatopama.
        # ‼ CHECK [IMG_0292.PNG]: TWO COLUMNS. First pairing read as ภุตตา
        #   โภคา ภะฏา ภัจจา (left) + วิติณณา อาปะทาสุ เม (right).
        # ‼ CHECK [IMG_0292.PNG]: English is a working translation made for
        #   this edition — the book prints none — so english_unverified is
        #   set. The title especially wants your eye: Adiya is rendered here
        #   as 'what is to be taken up', which is the sense of the sutta
        #   rather than a settled English title.
        'id': 'adiyasutta-gatha',
        'title_thai': 'อาทิยะสุตตะคาถา',
        'title_pali': 'Ādiyasuttagāthā',
        'title_roman': '',
        'title_english': 'The Verses of the Discourse on What is to be Taken Up',
        'book_number': 13,
        'page_start': 30,
        'source_printed': 'ส.ส. 15/315-6',
        'group': 'General chanting',
        'english_unverified': True,
        'invitation': {
            'pali': '',
            'pali_roman': '',
            'thai': '',
            'paiboon': '',
            'english': '',
        },
        'closing': {
            'pali': 'อาทิยะสุตตะคาถา นิฏฐิตา',
            'pali_roman': 'ādiyasuttagāthā niṭṭhitā',
            'thai': '',
            'paiboon': '',
            'english': 'Here end the Verses of the Ādiya Sutta.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'ภุตตา โภคา ภะฏา ภัจจา วิติณณา อาปะทาสุ เม',
                'pali_roman': 'bhuttā bhogā bhaṭā bhaccā vitiṇṇā āpadāsu me',
                'thai': '',
                'paiboon': '',
                'english': 'My wealth has been enjoyed, my dependants supported, adversities have been overcome by me;',
            },
            {
                'number': 2,
                'pali': 'อุทธัคคา ทักขิณา ทินนา อะโธ ปัญจะ พะลี กะตา.',
                'pali_roman': 'uddhaggā dakkhiṇā dinnā atho pañca balī katā.',
                'thai': '',
                'paiboon': '',
                'english': 'offerings leading upward have been given, and the five oblations made.',
            },
            {
                'number': 3,
                'pali': 'อุปัฏฐิตา สีละวันโต สัญญะตา พ์รัห์มะจาริโน',
                'pali_roman': 'upaṭṭhitā sīlavanto saññatā brahmacārino',
                'thai': '',
                'paiboon': '',
                'english': 'The virtuous have been waited upon, the restrained who live the holy life.',
            },
            {
                'number': 4,
                'pali': 'ยะทัตถัง โภคะมิจเฉยยะ ปัณฑิโต ฆะระมาวะสัง.',
                'pali_roman': 'yadatthaṃ bhogamiccheyya paṇḍito gharamāvasaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'That purpose for which a wise man dwelling at home would wish for wealth —',
            },
            {
                'number': 5,
                'pali': 'โส เม อัตโถ อะนุปปัตโต กะตัง อะนะนุตาปิยัง',
                'pali_roman': 'so me attho anuppatto kataṃ ananutāpiyaṃ',
                'thai': '',
                'paiboon': '',
                'english': 'that purpose I have attained; what I have done brings no remorse.',
            },
            {
                'number': 6,
                'pali': 'เอตัง อะนุสสะรัง มัจโจ อะริยะธัมเม ฐิโต นะโร,',
                'pali_roman': 'etaṃ anussaraṃ macco ariyadhamme ṭhito naro,',
                'thai': '',
                'paiboon': '',
                'english': 'A mortal who recalls this, a man standing firm in the noble Dhamma,',
            },
            # ‼ CHECK [IMG_0292.PNG]: Superscript 2 on this last line points
            #   at the page's footnote ส.ส. 15/315-6, now source_printed.
            {
                'number': 7,
                'pali': 'อิเธวะ นัง ปะสังสันติ เปจจะ สัคเค ปะโมทะตีติ.',
                'pali_roman': 'idheva naṃ pasaṃsanti pecca sagge pamodatīti.',
                'thai': '',
                'paiboon': '',
                'english': 'him they praise here and now, and hereafter he rejoices in heaven.',
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CHECK [IMG_0296.PNG]: NEW CHANT, and NOT FINISHED. The page prints
        #   it as far as the question katame satta and the answer runs onto
        #   page 34, so `continues` is set. Nothing beyond what the photograph
        #   shows has been written, however well known the seven factors are.
        # ‼ CHECK [IMG_0296.PNG]: READING HAZARD, AND WORSE HERE THAN ANYWHERE
        #   SO FAR. Four words in this chant turn on the lo-chula/pho
        #   distinction this typeface cannot photograph: veluvane at verse 2,
        #   balhagilano at verse 3, and balha at verse 11. Every earlier
        #   instance had the app's own text as a second witness; this chant is
        #   NEW, so the photograph is the ONLY source and there is nothing to
        #   check it against. They are written with lo chula because standard
        #   Pali requires it — Veluvana is the Bamboo Grove and balha means
        #   severe — but each is a JUDGEMENT, not a reading. Needs the
        #   physical book before this chant can be trusted.
        # ‼ CHECK [IMG_0296.PNG]: layout is prose. The passage is set as
        #   continuous justified text filling the measure, not as lines. The
        #   clause division records what it is made of; the app reassembles it
        #   into a block.
        # ‼ CHECK [IMG_0296.PNG]: English is a working translation made for
        #   this edition and english_unverified is set. The title especially:
        #   the book gives no English, and this is the standard name for the
        #   discourse rather than a settled rendering.
        'id': 'mahakassapa-bojjhanga-suttam',
        'title_thai': 'มะหากัสสะปะโพชฌังคะสุตตัง',
        'title_pali': 'Mahākassapabojjhaṅgasuttaṃ',
        'title_roman': '',
        'title_english': 'The Discourse on the Factors of Awakening, to Mahākassapa',
        'book_number': 17,
        'page_start': 33,
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
        'closing': {
            'pali': 'มะหากัสสะปะโพชฌังคะสุตตัง นิฏฐิตัง.',
            'pali_roman': 'mahākassapabojjhaṅgasuttaṃ niṭṭhitaṃ.',
            'thai': '',
            'paiboon': '',
            'english': 'Here ends the Discourse on the Factors of Awakening, to Mahākassapa.',
        },
        'verses': [
            {
                'number': 1,
                'pali': 'เอวัมเม สุตัง.',
                'pali_roman': 'evamme sutaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'Thus have I heard.',
            },
            {
                'number': 2,
                'pali': 'เอกัง สะมะยัง ภะคะวา, ราชะคะเห วิหะระติ, เวฬุวะเน กะลันทะกะนิวาเป.',
                'pali_roman': 'ekaṃ samayaṃ bhagavā, rājagahe viharati, veḷuvane kalandakanivāpe.',
                'thai': '',
                'paiboon': '',
                'english': "At one time the Blessed One was dwelling at Rājagaha, in the Bamboo Grove, the squirrels' feeding place.",
            },
            {
                'number': 3,
                'pali': 'เตนะ โข ปะนะ สะมะเยนะ, อายัส์มา มะหากัสสะโป ปิปผะลิคุหายัง วิหะระติ, อาพาธิโก ทุกขิโต พาฬ์หะคิลาโน.',
                'pali_roman': 'tena kho pana samayena, āyasmā mahākassapo pipphaliguhāyaṃ viharati, ābādhiko dukkhito bāḷhagilāno.',
                'thai': '',
                'paiboon': '',
                'english': 'Now at that time the venerable Mahākassapa was dwelling in the Pipphali Cave, afflicted, suffering, gravely ill.',
            },
            {
                'number': 4,
                'pali': 'อะถะโข ภะคะวา สายัณหะสะมะยัง ปะฏิสัลลานา วุฏฐิโต, เยนายัส์มา มะหากัสสะโป, เตนุปะสังกะมิ,',
                'pali_roman': 'athakho bhagavā sāyaṇhasamayaṃ paṭisallānā vuṭṭhito, yenāyasmā mahākassapo, tenupasaṅkami,',
                'thai': '',
                'paiboon': '',
                'english': 'Then the Blessed One, rising from seclusion towards evening, went to where the venerable Mahākassapa was;',
            },
            {
                'number': 5,
                'pali': 'อุปะสังกะมิต์วา ปัญญัตเต อาสะเน นิสีทิ,',
                'pali_roman': 'upasaṅkamitvā paññatte āsane nisīdi,',
                'thai': '',
                'paiboon': '',
                'english': 'having approached, he sat down on the seat made ready,',
            },
            {
                'number': 6,
                'pali': 'นิสัชชะ โข ภะคะวา อายัส์มันตัง มะหากัสสะปัง เอตะทะโวจะ.',
                'pali_roman': 'nisajja kho bhagavā āyasmantaṃ mahākassapaṃ etadavoca.',
                'thai': '',
                'paiboon': '',
                'english': 'and seated, the Blessed One said this to the venerable Mahākassapa:',
            },
            # ‼ CHECK [IMG_0296.PNG]: The exchange is a dialogue and the book
            #   prints no quotation marks at all — the Buddha asks at verses 7
            #   to 9 and Mahakassapa answers at 10 to 12. The English adds
            #   quotation marks to make that readable, which is an editorial
            #   decision and not in the book.
            {
                'number': 7,
                'pali': 'กัจจิ เต กัสสะปะ ขะมะนียัง, กัจจิ ยาปะนียัง,',
                'pali_roman': 'kacci te kassapa khamanīyaṃ, kacci yāpanīyaṃ,',
                'thai': '',
                'paiboon': '',
                'english': '"I hope you are bearing up, Kassapa; I hope you are keeping going;',
            },
            {
                'number': 8,
                'pali': 'กัจจิ ทุกขา เวทะนา ปะฏิกกะมันติ, โน อะภิกกะมันติ,',
                'pali_roman': 'kacci dukkhā vedanā paṭikkamanti, no abhikkamanti,',
                'thai': '',
                'paiboon': '',
                'english': 'I hope your painful feelings are subsiding and not increasing,',
            },
            {
                'number': 9,
                'pali': 'ปะฏิกกะโมสานัง ปัญญายะติ, โน อะภิกกะโมติ.',
                'pali_roman': 'paṭikkamosānaṃ paññāyati, no abhikkamoti.',
                'thai': '',
                'paiboon': '',
                'english': 'and that their subsiding, not their increase, is apparent."',
            },
            {
                'number': 10,
                'pali': 'นะ เม ภันเต ขะมะนียัง, นะ ยาปะนียัง,',
                'pali_roman': 'na me bhante khamanīyaṃ, na yāpanīyaṃ,',
                'thai': '',
                'paiboon': '',
                'english': '"I am not bearing up, venerable sir; I am not keeping going;',
            },
            {
                'number': 11,
                'pali': 'พาฬ์หา เม ทุกขา เวทะนา อะภิกกะมันติ, โน ปะฏิกกะมันติ,',
                'pali_roman': 'bāḷhā me dukkhā vedanā abhikkamanti, no paṭikkamanti,',
                'thai': '',
                'paiboon': '',
                'english': 'my painful feelings are severe and increasing, not subsiding,',
            },
            {
                'number': 12,
                'pali': 'อะภิกกะโมสานัง ปัญญายะติ, โน ปะฏิกกะโมติ.',
                'pali_roman': 'abhikkamosānaṃ paññāyati, no paṭikkamoti.',
                'thai': '',
                'paiboon': '',
                'english': 'and their increase, not their subsiding, is apparent."',
            },
            {
                'number': 13,
                'pali': 'สัตติเม กัสสะปะ โพชฌังคา, มะยา สัมมะทักขาตา ภาวิตา พะหุลีกะตา,',
                'pali_roman': 'sattime kassapa bojjhaṅgā, mayā sammadakkhātā bhāvitā bahulīkatā,',
                'thai': '',
                'paiboon': '',
                'english': '"Kassapa, these seven factors of awakening, rightly declared by me, developed and made much of,',
            },
            # ‼ CHECK [IMG_0296.PNG]: The page prints the paiyannoi character
            #   after sangvattanti, which marks an abbreviation or a pause in
            #   Thai typesetting. Reproduced as printed in `pali`; the
            #   romanisation renders it as a full stop, since IAST has no
            #   equivalent. Worth confirming what the book intends by it.
            {
                'number': 14,
                'pali': 'อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตันติ ฯ',
                'pali_roman': 'abhiññāya sambodhāya nibbānāya saṃvattanti.',
                'thai': '',
                'paiboon': '',
                'english': 'lead to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 15,
                'pali': 'กะตะเม สัตตะ.',
                'pali_roman': 'katame satta.',
                'thai': '',
                'paiboon': '',
                'english': 'Which seven?"',
            },
            # ‼ CHECK [IMG_0297.PNG]: Item 1 ends with ฯ where items 2 to 7
            #   all end with a full stop, though the wording is identical.
            #   Reproduced as printed rather than made uniform. Worth a glance
            #   at the page to confirm the book really does differ here.
            # ‼ CHECK [IMG_0297.PNG]: Each numbered item is one verse, so the
            #   formula mayā sammadakkhāto ... saṃvattati sits whole inside
            #   verse 16. On page 33 the same formula was split across verses
            #   13 and 14 at the comma. The two pages therefore break the same
            #   words differently. Nothing is missing either way, but if you
            #   want them consistent it is verses 13-14 that would need
            #   rejoining, and that is your call, not mine.
            {
                'number': 16,
                'page': 34,
                'printed_number': 1,
                'pali': 'สะติสัมโพชฌังโค โข กัสสะปะ มะยา สัมมะทักขาโต ภาวิโต พะหุลีกะโต, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตะติ ฯ',
                'pali_roman': 'satisambojjhaṅgo kho kassapa mayā sammadakkhāto bhāvito bahulīkato, abhiññāya sambodhāya nibbānāya saṃvattati.',
                'thai': '',
                'paiboon': '',
                'english': '"The factor of awakening that is mindfulness, Kassapa, rightly declared by me, developed and made much of, leads to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 17,
                'printed_number': 2,
                'pali': 'ธัมมะวิจะยะสัมโพชฌังโค โข กัสสะปะ มะยา สัมมะทักขาโต ภาวิโต พะหุลีกะโต, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตะติ.',
                'pali_roman': 'dhammavicayasambojjhaṅgo kho kassapa mayā sammadakkhāto bhāvito bahulīkato, abhiññāya sambodhāya nibbānāya saṃvattati.',
                'thai': '',
                'paiboon': '',
                'english': 'The factor of awakening that is investigation of states, Kassapa, rightly declared by me, developed and made much of, leads to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 18,
                'printed_number': 3,
                'pali': 'วิริยะสัมโพชฌังโค โข กัสสะปะ มะยา สัมมะทักขาโต ภาวิโต พะหุลีกะโต, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตะติ.',
                'pali_roman': 'vīriyasambojjhaṅgo kho kassapa mayā sammadakkhāto bhāvito bahulīkato, abhiññāya sambodhāya nibbānāya saṃvattati.',
                'thai': '',
                'paiboon': '',
                'english': 'The factor of awakening that is energy, Kassapa, rightly declared by me, developed and made much of, leads to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 19,
                'printed_number': 4,
                'pali': 'ปีติสัมโพชฌังโค โข กัสสะปะ มะยา สัมมะทักขาโต ภาวิโต พะหุลีกะโต, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตะติ.',
                'pali_roman': 'pītisambojjhaṅgo kho kassapa mayā sammadakkhāto bhāvito bahulīkato, abhiññāya sambodhāya nibbānāya saṃvattati.',
                'thai': '',
                'paiboon': '',
                'english': 'The factor of awakening that is rapture, Kassapa, rightly declared by me, developed and made much of, leads to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 20,
                'printed_number': 5,
                'pali': 'ปัสสัทธิสัมโพชฌังโค โข กัสสะปะ มะยา สัมมะทักขาโต ภาวิโต พะหุลีกะโต, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตะติ.',
                'pali_roman': 'passaddhisambojjhaṅgo kho kassapa mayā sammadakkhāto bhāvito bahulīkato, abhiññāya sambodhāya nibbānāya saṃvattati.',
                'thai': '',
                'paiboon': '',
                'english': 'The factor of awakening that is tranquillity, Kassapa, rightly declared by me, developed and made much of, leads to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 21,
                'printed_number': 6,
                'pali': 'สะมาธิสัมโพชฌังโค โข กัสสะปะ มะยา สัมมะทักขาโต ภาวิโต พะหุลีกะโต, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตะติ.',
                'pali_roman': 'samādhisambojjhaṅgo kho kassapa mayā sammadakkhāto bhāvito bahulīkato, abhiññāya sambodhāya nibbānāya saṃvattati.',
                'thai': '',
                'paiboon': '',
                'english': 'The factor of awakening that is concentration, Kassapa, rightly declared by me, developed and made much of, leads to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 22,
                'printed_number': 7,
                'pali': 'อุเปกขาสัมโพชฌังโค โข กัสสะปะ มะยา สัมมะทักขาโต ภาวิโต พะหุลีกะโต, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตะติ.',
                'pali_roman': 'upekkhāsambojjhaṅgo kho kassapa mayā sammadakkhāto bhāvito bahulīkato, abhiññāya sambodhāya nibbānāya saṃvattati.',
                'thai': '',
                'paiboon': '',
                'english': 'The factor of awakening that is equanimity, Kassapa, rightly declared by me, developed and made much of, leads to direct knowledge, to full awakening, to Nibbāna.',
            },
            {
                'number': 23,
                'pali': 'อิเม โข กัสสะปะ สัตตะ โพชฌังคา มะยา สัมมะทักขาตา ภาวิตา พะหุลีกะตา, อะภิญญายะ สัมโพธายะ นิพพานายะ สังวัตตันตีติ.',
                'pali_roman': 'ime kho kassapa satta bojjhaṅgā mayā sammadakkhātā bhāvitā bahulīkatā, abhiññāya sambodhāya nibbānāya saṃvattantīti.',
                'thai': '',
                'paiboon': '',
                'english': 'These seven factors of awakening, Kassapa, rightly declared by me, developed and made much of, lead to direct knowledge, to full awakening, to Nibbāna."',
            },
            {
                'number': 24,
                'pali': 'ตัคฆะ ภะคะวา โพชฌังคา ตัคฆะ สุคะตะ โพชฌังคาติ.',
                'pali_roman': 'taggha bhagavā bojjhaṅgā taggha sugata bojjhaṅgāti.',
                'thai': '',
                'paiboon': '',
                'english': '"Assuredly, Blessed One, they are factors of awakening; assuredly, Well-Farer, they are factors of awakening."',
            },
            {
                'number': 25,
                'pali': 'อิทะมะโวจะ ภะคะวา.',
                'pali_roman': 'idamavoca bhagavā.',
                'thai': '',
                'paiboon': '',
                'english': 'This the Blessed One said.',
            },
            {
                'number': 26,
                'pali': 'อัตตะมะโน อายัส์มา มะหากัสสะโป ภะคะวะโต ภาสิตัง อะภินันทิ.',
                'pali_roman': 'attamano āyasmā mahākassapo bhagavato bhāsitaṃ abhinandi.',
                'thai': '',
                'paiboon': '',
                'english': 'Gladdened, the venerable Mahākassapa delighted in the words of the Blessed One.',
            },
            # ‼ CHECK [IMG_0297.PNG]: (ลากเสียง) — "draw the sound out" — is
            #   an instruction to the chanter printed inline in brackets, not
            #   part of the Pali. Kept inline exactly where the book prints
            #   it, as the prompt requires. It means this verse's pali line
            #   contains a Thai word, so pali_roman renders that bracket in
            #   Paiboon+ rather than IAST. If you would rather it were carried
            #   some other way, say so and I will move it.
            {
                'number': 27,
                'pali': 'วุฏฐะหิ จายัส์มา มะหากัสสะโป ตัมหา อาพาธา, ตะถาปะหีโน จายัส์มะโต มะหากัสสะปัสสะ โส (ลากเสียง) อาพาโธ อะโหสีติ.',
                'pali_roman': 'vuṭṭhahi cāyasmā mahākassapo tamhā ābādhā, tathāpahīno cāyasmato mahākassapassa so (lâak sǐiaŋ) ābādho ahosīti.',
                'thai': '',
                'paiboon': '',
                'english': "And the venerable Mahākassapa rose up from that illness, and in that way the venerable Mahākassapa's illness was abandoned.",
            },
        ],
    },
    {
        # ‼ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
        #   when_chanted and source still to be written. Verses are complete.
        # ‼ CONTINUES: last verse here is 4; the rest is not in the app yet.
        # ‼ CHECK [IMG_0297.PNG]: This discourse and the Mahākassapa one on
        #   page 33 share almost all their wording, differing in the elder's
        #   name and the place. It is NOT a repeat — the book prints it as its
        #   own chant under its own number 18 — so it is set in full.
        # ‼ CHECK [IMG_0297.PNG]: No Thai translation is printed, so
        #   english_unverified is true and the English is a working
        #   translation made for this edition.
        'id': 'mahamoggallana-bojjhanga-suttam',
        'title_thai': 'มะหาโมคคัลลานะโพชฌังคะสุตตัง',
        'title_pali': 'Mahāmoggallānabojjhaṅgasuttaṃ',
        'title_roman': '',
        'title_english': 'The Discourse on the Factors of Awakening, to Mahāmoggallāna',
        'book_number': 18,
        'page_start': 34,
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
                'pali': 'เอวัมเม สุตัง.',
                'pali_roman': 'evamme sutaṃ.',
                'thai': '',
                'paiboon': '',
                'english': 'Thus have I heard.',
            },
            {
                'number': 2,
                'pali': 'เอกัง สะมะยัง ภะคะวา, ราชะคะเห วิหะระติ, เวฬุวะเน กะลันทะกะนิวาเป.',
                'pali_roman': 'ekaṃ samayaṃ bhagavā, rājagahe viharati, veḷuvane kalandakanivāpe.',
                'thai': '',
                'paiboon': '',
                'english': "At one time the Blessed One was dwelling at Rājagaha, in the Bamboo Grove, the squirrels' feeding place.",
            },
            {
                'number': 3,
                'pali': 'เตนะ โข ปะนะ สะมะเยนะ, อายัส์มา มะหาโมคคัลลาโน คิชฌะกูเฏ ปัพพะเต วิหะระติ, อาพาธิโก ทุกขิโต พาฬ์หะคิลาโน.',
                'pali_roman': 'tena kho pana samayena, āyasmā mahāmoggallāno gijjhakūṭe pabbate viharati, ābādhiko dukkhito bāḷhagilāno.',
                'thai': '',
                'paiboon': '',
                'english': "Now at that time the venerable Mahāmoggallāna was dwelling on the Vulture's Peak, afflicted, suffering, gravely ill.",
            },
            # ‼ CHECK [IMG_0297.PNG]: The page ends mid-sentence after อะถะโข,
            #   so verse 4 belongs to page 34 where it starts and is marked
            #   with the gap marker. Page 35 completes it; the next batch
            #   supplies verse 4 in full rather than starting a new verse.
            {
                'number': 4,
                'pali': 'อะถะโข […]',
                'pali_roman': 'athakho […]',
                'thai': '',
                'paiboon': '',
                'english': 'Then […]',
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
    # ── Page 13 ─────────────────────────────────────────────────────────
    # The page alternates instruction and Pali all the way down: the elder
    # speaks, the assembly answers, the elder speaks again. Each instruction
    # is anchored after the chant it follows, so the alternation survives.
    {
        'page': 13,
        'blocks': [
            {
                'type': 'prose',
                'thai': 'พระเถระว่าต่อไปแต่ลำพังดังนี้.',
                'english': 'The elder continues alone, as follows.',
                'english_unverified': True,
            },
        ],
    },
    {
        'page': 13,
        'after': 'imani-attha-sikkhapadani',
        'blocks': [
            {
                'type': 'prose',
                'thai': 'อุบาสกอุบาสิการับพร้อมกันว่า อามะ ภันเต.',
                'english': (
                    'The laymen and laywomen answer together: āma bhante — '
                    '\'yes, venerable sir\'.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': 'พระเถระว่าต่อไปแต่ลำพังดังนี้.',
                'english': 'The elder continues alone, as follows.',
                'english_unverified': True,
            },
        ],
    },
    # The invitation to the closing gatha is printed INSIDE this paragraph
    # rather than on a line of its own, so it stays here and the chant's
    # `invitation` field is left empty. Lifting it out would print it twice.
    {
        'page': 13,
        'after': 'silena-sugatim-yanti',
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'เป็นอันเสร็จพิธีสมาทานอุโบสถศีลเท่านี้ ต่อจากนี้ พระเถระ '
                    'เริ่มแสดงพระธรรมเทศนา พุทธบริษัททั้งบรรพชิตและคฤหัสถ์ '
                    'ตั้งใจฟังโดยเคารพ เพื่อให้สำเร็จเป็นกุศลส่วนธรรมสวนมัยต่อไป '
                    'พอแสดงพระธรรมเทศนาจบลง หัวหน้าอุบาสกกล่าวเชิญแสดงสาธุการว่า '
                    'หันทะ มะยัง สาธุการัง กะโรมะ เส. อุบาสกอุบาสิกา '
                    'นอกนี้รับพร้อมกันว่า สาธุ สาธุ สาธุ 3 หน '
                    'แล้วหัวหน้าอุบาสกกล่าวเชิญสวด สะระณะคะมะนานุสสะระณะคาถา '
                    'ต่อท้ายดังนี้ หันทะ มะยัง สะระณะคะมะนานุสสะระณะคาถาโย '
                    'ภะณามะ เส.'
                ),
                'english': (
                    'With this the ceremony of undertaking the Uposatha '
                    'precepts is complete. After it the elder begins the '
                    'Dhamma talk, and the Buddhist assembly, both those gone '
                    'forth and the householders, listen attentively and '
                    'respectfully, so that the merit of hearing the Dhamma '
                    'may be accomplished. When the talk has ended, the '
                    'leading layman gives the invitation to make the '
                    'acclamation: handa mayaṃ sādhukāraṃ karoma se. The other '
                    'laymen and laywomen answer together sādhu, sādhu, sādhu '
                    'three times. Then the leading layman gives the '
                    'invitation to chant the Saraṇagamanānussaraṇagāthā as a '
                    'closing, thus: handa mayaṃ saraṇagamanānussaraṇagāthāyo '
                    'bhaṇāma se.'
                ),
                'english_unverified': True,
            },
            {
                'type': 'prose',
                'thai': 'อุบาสกอุบาสิกานอกนี้สวดพร้อมกัน หยุดตามจุดลูกน้ำดังนี้.',
                'english': (
                    'The other laymen and laywomen chant together, pausing at '
                    'the commas, as follows.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # Both footnotes are EDITORIAL — which word a laywoman substitutes — and
    # neither is a citation, so neither goes in `source_printed`. Page 8
    # carries an identical note about คะโต/คะตา; footnote numbers restart on
    # every page, so these are page 13's own 1 and 2.
    {
        'page': 13,
        'after': 'sarana-gamananussarana-gatha',
        'blocks': [
            {
                'type': 'footnote',
                'marker': '1',
                'thai': 'คะโต สำหรับอุบาสก ถ้าอุบาสิกาใช้ คะตา',
                'english': 'gato is for a layman; a laywoman uses gatā.',
                'english_unverified': True,
            },
            {
                'type': 'footnote',
                'marker': '2',
                'thai': 'อุปาสะกัตตัง สำหรับอุบาสก ถ้าอุบาสิกาใช้ อุปาสิกัตตัง',
                'english': (
                    'upāsakattaṃ is for a layman; a laywoman uses '
                    'upāsikattaṃ.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # ── Page 14 ─────────────────────────────────────────────────────────
    # One paragraph under the chant, closing the whole morning observance
    # for a Dhamma-hearing day. It ends a SERVICE, but it is prose rather
    # than a จบ… line, so it is an ordinary block and not a
    # `service_closing` — that key is for the centred จบ formula.
    #
    # ‼ CHECK [IMG_0277.PNG]: 'เบญจางคประดิษฐ์' is printed broken across a
    #   line as 'ด้วยเบญจางค-' / 'ประดิษฐ์'. The hyphen is justification and
    #   not spelling, so the word is recorded whole.
    {
        'page': 14,
        'after': 'kham-kho-khama-phra-rattanatrai',
        'blocks': [
            {
                'type': 'prose',
                'thai': (
                    'พระเถระที่แสดงพระธรรมเทศนา ลงจากธรรมาสน์ นั่ง ณ '
                    'เถราสนะรออยู่จน อุบาสกอุบาสิกา สวด '
                    'สะระณะคะมะนานุสสะระณะคาถา จบ เมื่อสวดจบแล้ว พระภิกษุ '
                    'สามเณรทั้งหมด นั่งคุกเข่าท่าพรหมประนมมือกราบพระรัตนตรัย '
                    'ด้วยเบญจางคประดิษฐ์ 3 หน อุบาสกอุบาสิกาก็กราบพระรัตนตรัย '
                    '3 หน เช่นเดียวกัน '
                    'เป็นอันเสร็จพิธีในภาคเช้าในวันธรรมสวนะเพียงเท่านี้.'
                ),
                'english': (
                    'The elder who gave the Dhamma talk comes down from the '
                    'Dhamma seat and sits on the elders\' seat, waiting until '
                    'the laymen and laywomen have finished chanting the '
                    'Saraṇagamanānussaraṇagāthā. When the chanting is done, '
                    'all the bhikkhus and sāmaṇeras kneel in the brahma '
                    'posture with palms joined and bow to the Triple Gem with '
                    'the fivefold prostration three times. The laymen and '
                    'laywomen likewise bow to the Triple Gem three times. '
                    'With this the morning observance on a Dhamma-hearing day '
                    'is complete.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # ── Page 16 ─────────────────────────────────────────────────────────
    # The page's only footnote, printed below the Bhojana rules although its
    # marker belongs to Saruppa rule 26 above them. Anchored where the book
    # prints it, not where the marker sits.
    #
    # A canonical citation, so it would normally be `source_printed` on the
    # chant. It is a footnote block instead, for the same reason page 12's
    # was: `source_printed` renders as a line labelled with the chant's
    # title, and the book prints '1. วิ. มหา 2/531-542'. No english — a
    # reference is reproduced, never translated or expanded.
    {
        'page': 16,
        'after': 'sekhiya-bhojanapatisamyutta',
        'blocks': [
            {
                'type': 'footnote',
                'marker': '1',
                'thai': 'วิ. มหา 2/531-542',
                'english': '',
            },
        ],
    },
    # ── Page 17 ─────────────────────────────────────────────────────────
    # Two footnotes. The first is a plain citation. The SECOND is mixed —
    # it cites, and then tells the chanter that most people say เทสิสสามีติ
    # where the book prints เทเสสสามีติ. Because it carries instruction it
    # is a footnote block and never `source_printed`, which the app prints
    # as a bare citation.
    #
    # ‼ CHECK [IMG_0280.PNG]: footnote 1 reads 'วิ. มหา. 252-557' where
    #   page 16's read 'วิ. มหา 2/531-542'. A reference continuing from 542
    #   would be expected to read '2/543-557'. Reproduced as printed.
    {
        'page': 17,
        'after': 'sekhiya-dhammadesanapatisamyutta',
        'blocks': [
            {
                'type': 'footnote',
                'marker': '1',
                'thai': 'วิ. มหา. 252-557',
                'english': '',
            },
            {
                'type': 'footnote',
                'marker': '2',
                'thai': 'วิ. มหา. เล่ม 2 558 ส่วนมากสวดใช้คำว่า เทสิสสามีติ',
                'english': (
                    'Vinaya, Mahavagga, volume 2, 558. Most chanters use the '
                    'word desissāmīti in place of the printed desessāmīti.'
                ),
                'english_unverified': True,
            },
        ],
    },
    # ── Page 18 ─────────────────────────────────────────────────────────
    # The Sekhiya set closes on this page: 26 + 30 + 16 + 3 = 75.
    #
    # This footnote prints '2/558-570', with the slash and volume number,
    # exactly as page 16's did — which is why page 17's '252-557' is more
    # likely a misreading of '2/543-557' than something the book prints.
    {
        'page': 18,
        'after': 'sekhiya-pakinnaka',
        'blocks': [
            {
                'type': 'footnote',
                'marker': '1',
                'thai': 'วิ. มหา 2/558-570',
                'english': '',
            },
        ],
    },
    # ── Page 20 ─────────────────────────────────────────────────────────
    # The citation keyed to the Dasadhamma Sutta's last line. Its marker is
    # unambiguous, so the prompt would put it in `source_printed` — but the
    # template renders that as a line labelled with the chant's title, and
    # the book prints '1. อง ทสก. 24/24-5' under a rule. Same treatment as
    # pages 12 and 16-18.
    {
        'page': 20,
        'after': 'parittakarana-patha',
        'blocks': [
            {
                'type': 'footnote',
                'marker': '1',
                'thai': 'อง ทสก. 24/24-5',
                'english': '',
            },
        ],
    },
    # ── Page 19 ─────────────────────────────────────────────────────────
    # A new DIVISION of the book opens here. Pages 1-18 were the services
    # themselves; from here the book gives the suttas and passages chanted
    # within them, and starts numbering its chants.
    #
    # Both headings belong to the division, not to the chant below them,
    # which is why they are page blocks rather than the chant's title.
    {
        'page': 19,
        'blocks': [
            {
                'type': 'heading',
                'thai': 'พระสูตร ปาฐะ และคาถา',
                'english': 'Suttas, Passages and Verses',
                'english_unverified': True,
            },
            {
                'type': 'heading',
                'thai': 'ที่กำหนดสวดในภาคเช้า',
                'english': 'appointed for chanting in the morning',
                'english_unverified': True,
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



# The romanised line under each contents title — the way in for a reader who
# cannot read Thai script, of whom this book asks a great deal: it prints 286
# titles and not one letter of Latin anywhere.
#
# TWO SYSTEMS, and which one a title gets is a fact about the title, not a
# style choice. Most of these are PALI written in Thai script and take IAST
# (Ratanattayappaṇāmagāthā). The rest are ordinary THAI — คำบูชา…, บทขัด… —
# and are not Pali at all, so IAST would misrepresent what the words are;
# those take Paiboon, which is what the rest of the app teaches and which
# carries the tones IAST cannot write.
#
# The 109 Pali entries are GENERATED, by scripts/romanise_contents.py, which
# transliterates the Thai mechanically and refuses to guess: it calls a title
# Pali only when every syllable is shaped the way Pali spells them. Run
# `python scripts/romanise_contents.py --check` to see where this table and
# the script disagree — a disagreement is a hand correction, and it should be
# possible to say why each one is there. There is exactly one today
# (เสขิยวัตร), and the reason is written above it.
#
# Verified against the 19 chants already carrying a `title_pali`: the script
# reproduces all 19 exactly, which is the only independent check there is on
# the other 90.
#
# The 177 Thai entries are WRITTEN BY HAND, because Paiboon needs tone rules
# and word boundaries that cannot be read off the spelling. They are checked
# for well-formedness only — `paiboon_faults` in the same script says whether
# each is a possible Paiboon syllable, which catches a typo but cannot catch a
# wrong reading.
#
# ⚠ Every reading here is an UNREVIEWED DRAFT, like the `pali_roman` verse
# layers. Josh to check them against the physical book.
#
# The book itself prints NONE of this. It is an addition for readers of this
# app, and it is the only thing on the contents page that is: the lines, their
# order, their wording and their page numbers are the book's own.
# The Pali titles, in IAST. Generated by scripts/romanise_contents.py.
_CONTENTS_PALI_ROMAN = {
    'ระตะนัตตะยัปปะณามะคาถา':
        'Ratanattayappaṇāmagāthā',
    'สังเวคะปะริกิตตะนะปาฐะ':
        'Saṃvegaparikittanapāṭha',
    'ตังขะณิกะปัจจะเวกขะณะปาโฐ':
        'Taṅkhaṇikapaccavekkhaṇapāṭho',
    'สะระณะคะมะนานุสสะระณะคาถา':
        'Saraṇagamanānussaraṇagāthā',

    # The one title here that is NOT generated. The book spells this Pali word
    # in Thai orthography rather than the phonetic style it uses for Pali
    # everywhere else, so the script refuses it (ยว and ตร are not Pali
    # clusters, and a Pali word cannot end in ร) and would produce Sekhiyvatr.
    # The word is Pali all the same, and the chant's own title_pali has read it
    # as Sekhiyavatta since long before this table. `--check` reports it as a
    # disagreement; this comment is the answer.
    'เสขิยวัตร':
        'Sekhiyavatta',
    'ทะสะธัมมะสุตตัง':
        'Dasadhammasuttaṃ',
    'ปะริตตะกะระณะปาโฐ':
        'Parittakaraṇapāṭho',
    'เมตตานิสังสะสุตตัง':
        'Mettānisaṃsasuttaṃ',
    'เมตตานิสังสะคาถา':
        'Mettānisaṃsagāthā',
    'นิธิกัณฑะคาถา':
        'Nidhikaṇḍagāthā',
    'ธัมมะคาระวาทิคาถา':
        'Dhammagāravādigāthā',
    'เทวะตาทิสสะทักขิณานุโมทะนาคาถา':
        'Devatādissadakkhiṇānumodanāgāthā',
    'เทวะตาภิสัมมันตะนะคาถา':
        'Devatābhisammantanagāthā',
    'ติลักขะณาทิคาถา':
        'Tilakkhaṇādigāthā',
    'เขมาเขมะสะระณะคะมะนะปะริทีปิกาคาถา':
        'Khemākhemasaraṇagamanaparidīpikāgāthā',
    'วิหาระทานะคาถา':
        'Vihāradānagāthā',
    'สัจจะปานะวิธ์ยานุรูปะคาถา':
        'Saccapānavidhyānurūpagāthā',
    'อาทิยะสุตตะคาถา':
        'Ādiyasuttagāthā',
    'ปัพพะโตปะมะคาถา':
        'Pabbatopamagāthā',
    'อริยะธะนะคาถา':
        'Ariyadhanagāthā',
    'ปะฏิจจะสะมุปปาทะปาโฐ':
        'Paṭiccasamuppādapāṭho',
    'พุทธะอุทานะคาถา':
        'Buddhaudānagāthā',
    'ภัทเทกะรัตตะคาถา':
        'Bhaddekarattagāthā',
    'มะหากัสสะปะโพชฌังคะสุตตัง':
        'Mahākassapabojjhaṅgasuttaṃ',
    'มะหาโมคคัลลานะโพชฌังคะสุตตัง':
        'Mahāmoggallānabojjhaṅgasuttaṃ',
    'มะหาจุนทะโพชฌังคะสุตตัง':
        'Mahācundabojjhaṅgasuttaṃ',
    'ธัมมะสังคะณีมาติกาปาโฐ':
        'Dhammasaṅgaṇīmātikāpāṭho',
    'วิปัสสะนาภูมิปาโฐ':
        'Vipassanābhūmipāṭho',
    'ชะยะมังคะลัฏฐะกะคาถา':
        'Jayamaṅgalaṭṭhakagāthā',
    'ชะยะปะริตตะคาถา':
        'Jayaparittagāthā',
    'กาละทานะสุตตะคาถา':
        'Kāladānasuttagāthā',
    'สังคะหะวัตถุคาถา':
        'Saṅgahavatthugāthā',
    'โมกขุปายะคาถา':
        'Mokkhupāyagāthā',
    'ระตะนัตตะยัปปะภาวะสิทธิคาถา':
        'Ratanattayappabhāvasiddhigāthā',
    'พุทธะมังคะละคาถา':
        'Buddhamaṅgalagāthā',
    'สีลุทเทสะปาโฐ':
        'Sīluddesapāṭho',
    'อะตีตะปัจจะเวกขะณะปาโฐ':
        'Atītapaccavekkhaṇapāṭho',
    'ธาตุปะฏิกูละปัจจะเวกขะณะปาโฐ':
        'Dhātupaṭikūlapaccavekkhaṇapāṭho',
    'อุทิสสะนาธิฏฐานะคาถา':
        'Udissanādhiṭṭhānagāthā',
    'โอวาทะปาติโมกขาทิปาโฐ':
        'Ovādapātimokkhādipāṭho',
    'ปุพพะภาคะนะมะการะปาโฐ':
        'Pubbabhāganamakārapāṭho',
    'สะระณะคะมะนะปาโฐ':
        'Saraṇagamanapāṭho',
    'นะมะการะสิทธิคาถา':
        'Namakārasiddhigāthā',
    'นะโมการะอัฏฐะกะคาถา':
        'Namokāraaṭṭhakagāthā',
    'มังคะละสุตตัง ปะฐะมัง':
        'Maṅgalasuttaṃ paṭhamaṃ',
    'ระตะนะสุตตัง ทุติยัง':
        'Ratanasuttaṃ dutiyaṃ',
    'กะระณียะเมตตะสุตตัง ตะติยัง':
        'Karaṇīyamettasuttaṃ tatiyaṃ',
    'ขันธะปะริตตัง จะตุตถัง':
        'Khandhaparittaṃ catutthaṃ',
    'ฉัททันตะปะริตตัง':
        'Chaddantaparittaṃ',
    'โมระปะริตตัง ปัญจะมัง':
        'Moraparittaṃ pañcamaṃ',
    'วัฏฏะกะปะริตตัง ฉัฏฐัง':
        'Vaṭṭakaparittaṃ chaṭṭhaṃ',
    'ธะชัคคะปะริตตัง ธะชัคคะสุตตัง สัตตะมัง':
        'Dhajaggaparittaṃ dhajaggasuttaṃ sattamaṃ',
    'อาฏานาฏิยะปะริตตัง อัฏฐะมัง':
        'Āṭānāṭiyaparittaṃ aṭṭhamaṃ',
    'อังคุลิมาละปะริตตัง นะวะมัง':
        'Aṅgulimālaparittaṃ navamaṃ',
    'โพชฌังคะปะริตตัง ทะสะมัง':
        'Bojjhaṅgaparittaṃ dasamaṃ',
    'อะภะยะปะริตตัง เอกาทะสะมัง':
        'Abhayaparittaṃ ekādasamaṃ',
    'เทวะตาอุยโยชะนะคาถา':
        'Devatāuyyojanagāthā',
    'ชะยะปะริตตัง ท์วาทะสะมัง':
        'Jayaparittaṃ dvādasamaṃ',
    'ระตะนัตตะยัปปะภาวาภิยาจะนะคาถา':
        'Ratanattayappabhāvābhiyācanagāthā',
    'สุขาภิยาจะนะคาถา':
        'Sukhābhiyācanagāthā',
    'ทะสะนาถะกะระณะธัมมะสุตตัง':
        'Dasanāthakaraṇadhammasuttaṃ',
    'อะภิณ์หะปัจจะเวกขะณะปาโฐ':
        'Abhiṇhapaccavekkhaṇapāṭho',
    'มัคคะวิภังคะสุตตัง':
        'Maggavibhaṅgasuttaṃ',
    'อัฏฐังคิกะมัคคะคาถา':
        'Aṭṭhaṅgikamaggagāthā',
    'กะระณียากะระณียะสุตตัง':
        'Karaṇīyākaraṇīyasuttaṃ',
    'อัคคัปปะสาทะสุตตัง':
        'Aggappasādasuttaṃ',
    'ฉะสาราณียะธัมมะสุตตัง':
        'Chasārāṇīyadhammasuttaṃ',
    'ภิกขุอะปะริหานิยะธัมมะสุตตัง':
        'Bhikkhuaparihāniyadhammasuttaṃ',
    'ปะหานะภาวะนาสุตตัง':
        'Pahānabhāvanāsuttaṃ',
    'จะตุรัปปะมัญญาปาโฐ':
        'Caturappamaññāpāṭho',
    'ธัมมะนิยามะสุตตัง':
        'Dhammaniyāmasuttaṃ',
    'อะนัตตะลักขะณะสุตตัง':
        'Anattalakkhaṇasuttaṃ',
    'อาทิตตะปะริยายะสุตตัง':
        'Ādittapariyāyasuttaṃ',
    'สะติปัฏฐานะปาโฐ':
        'Satipaṭṭhānapāṭho',
    'มะหาสะติปัฏฐานะสุตตะปาโฐ':
        'Mahāsatipaṭṭhānasuttapāṭho',
    'ธัมมะจักกัปปะวัตตะนะสุตตัง':
        'Dhammacakkappavattanasuttaṃ',
    'ปุพพะภาคะมะนะการะปาโฐ':
        'Pubbabhāgamanakārapāṭho',
    'มังคะละสุตตัง':
        'Maṅgalasuttaṃ',
    'ระตะนะสุตตัง':
        'Ratanasuttaṃ',
    'กะระณียะเมตตะสุตตัง':
        'Karaṇīyamettasuttaṃ',
    'ขันธะปะริตตัง':
        'Khandhaparittaṃ',
    'อาฏานาฏิยะปะริตตัง':
        'Āṭānāṭiyaparittaṃ',
    'อังคุลิมาละปะริตตัง':
        'Aṅgulimālaparittaṃ',
    'โพชฌังคะปะริตตัง':
        'Bojjhaṅgaparittaṃ',
    'อะภะยะปะริตตัง':
        'Abhayaparittaṃ',
    'ชะยะปะริตตัง':
        'Jayaparittaṃ',
    'มะหาสะมะยะสุตตัง':
        'Mahāsamayasuttaṃ',
    'คิริมานันทะสุตตัง':
        'Girimānandasuttaṃ',
    'โลกะธัมมะสุตตัง':
        'Lokadhammasuttaṃ',
    'พุทธาภิถุติ':
        'Buddhābhithuti',
    'ธัมมาภิถุติ':
        'Dhammābhithuti',
    'สังฆาภิถุติ':
        'Saṅghābhithuti',
    'ปัตติทานะคาถา':
        'Pattidānagāthā',
    'สัพพะปัตติทานะคาถา':
        'Sabbapattidānagāthā',
    'ปัฏฐะนะฐะปะนะคาถา':
        'Paṭṭhanaṭhapanagāthā',
    'เขมาเขมะสะระณะทีปิกะคาถา':
        'Khemākhemasaraṇadīpikagāthā',
    'อะภิณหะปัจจะเวกขะณะ ๕':
        'Abhiṇhapaccavekkhaṇa 5',
    'ท์วัตติงสาการะปาโฐ':
        'Dvattiṃsākārapāṭho',
    'ภาระสุตตะคาถา':
        'Bhārasuttagāthā',
    'ติโลกะวิชะยะราชะปัตติทานะคาถา':
        'Tilokavijayarājapattidānagāthā',
    'อะภิณหะปัจจะเวกขะณะ':
        'Abhiṇhapaccavekkhaṇa',
    'พุทธานุสสะติ':
        'Buddhānussati',
    'พุทธาภิคีติ':
        'Buddhābhigīti',
    'ธัมมานุสสะติ':
        'Dhammānussati',
    'ธัมมาภิคีติ':
        'Dhammābhigīti',
    'สังฆานุสสะติ':
        'Saṅghānussati',
    'สังฆาภิคีติ':
        'Saṅghābhigīti',
    'อุณ์หิสสะวิชะยะคาถา':
        'Uṇhissavijayagāthā',
    'อัคคัปปะสาทะสุตตะคาถา':
        'Aggappasādasuttagāthā',
    'โภชะนะทานุโมทะนาคาถา':
        'Bhojanadānumodanāgāthā',
}


# The Thai titles, in Paiboon. Written by hand — Paiboon needs tone rules
# and word boundaries that cannot be read off the spelling.
_CONTENTS_PAIBOON = {
    'ทำวัตรเช้า':
        'tam-wát cháao',
    'คำบูชาพระรัตนตรัย':
        'kam buu-chaa prá-rát-dtà-ná-dtrai',
    'คำนมัสการพระรัตนตรัย':
        'kam ná-mát-sà-gaan prá-rát-dtà-ná-dtrai',
    'คำเชิญบูชาและสวดนะโม':
        'kam chəən buu-chaa lɛ́ sùat ná-moo',
    'คำอธิบายประกอบทำวัตรเช้า':
        'kam à-tí-baai bprà-gɔ̀ɔp tam-wát cháao',
    'คำประกาศอุโบสถ':
        'kam bprà-gàat u-boo-sòt',
    'คำอาราธนาอุโบสถศีล':
        'kam aa-râat-tá-naa u-boo-sòt-sǐin',
    'อุโบสถศีล':
        'u-boo-sòt-sǐin',
    'คำขอขมาพระรัตนตรัย':
        'kam kɔ̌ɔ kà-maa prá-rát-dtà-ná-dtrai',
    'สารุปปะ ๒๖ สิกขาบท':
        'sǎa-rúp-bpà 26 sìk-kǎa-bòt',
    'โภชชะนะปะฏิสังยุต ๓๐ สิกขาบท':
        'poot-chá-ná-bpà-dtì-sǎŋ-yút 30 sìk-kǎa-bòt',
    'ธัมมะเทสะนาปะฏิสังยุต ๑๖ สิกขาบท':
        'tam-má-têe-sà-naa-bpà-dtì-sǎŋ-yút 16 sìk-kǎa-bòt',
    'ปะกิณณะกะ ๓ สิกขาบท':
        'bpà-gin-ná-gà 3 sìk-kǎa-bòt',
    'พระสูตร ปาฐะ และคาถาที่กำหนดสวดในภาคเช้า':
        'prá-sùut bpaa-tà lɛ́ kaa-tǎa tîi gam-nòt sùat nai pâak cháao',
    'สวดแจง':
        'sùat jɛɛŋ',
    'พระวินัยสังเขป':
        'prá-wí-nai sǎŋ-kèep',
    'พระสูตรสังเขป':
        'prá-sùut sǎŋ-kèep',
    'พระอภิธรรมสังเขป':
        'prá-à-pí-tam sǎŋ-kèep',
    'พระสังคะณี':
        'prá-sǎŋ-ká-nii',
    'พระวิภังค์':
        'prá-wí-paŋ',
    'พระธาตุกะถา':
        'prá-tâat-gà-tǎa',
    'พระปุคคะละบัญญัติ':
        'prá-púk-ká-lá-ban-yàt',
    'พระกะถาวัตถุ':
        'prá-gà-tǎa-wát-tù',
    'พระยะมะกะ':
        'prá-yá-má-gà',
    'พระมะหาปัฏฐาน':
        'prá-má-hǎa-bpàt-tǎan',
    'ถวายพรพระ':
        'tà-wǎai pɔɔn prá',
    'มงคลจักรวาฬน้อย':
        'moŋ-kon jàk-grà-waan nɔ́ɔi',
    'ทำวัตรเย็น':
        'tam-wát yen',
    'ระเบียบทำวัตรสวดมนต์ ภาคเย็น':
        'rá-bìiap tam-wát sùat-mon pâak yen',
    'คาถาบูชาพระรัตนตรัย':
        'kaa-tǎa buu-chaa prá-rát-dtà-ná-dtrai',
    'คำเชิญบูชาสวดนะโม และพระพุทธคุณ':
        'kam chəən buu-chaa sùat ná-moo lɛ́ prá-pút-tá-kun',
    'บทขัดสิกขาบท ๑๐':
        'bòt-kàt sìk-kǎa-bòt 10',
    'สิกขาบท ๑๐':
        'sìk-kǎa-bòt 10',
    'บทขัดนาสะนังคะ':
        'bòt-kàt naa-sà-naŋ-ká',
    'นาสะนังคะ ๑๐ สิกขาบท':
        'naa-sà-naŋ-ká 10 sìk-kǎa-bòt',
    'บทขัดทัณฑะกรรม':
        'bòt-kàt tan-tá-gam',
    'ทัณฑะกรรม ๕ สิกขาบท':
        'tan-tá-gam 5 sìk-kǎa-bòt',
    'คำอธิบายประกอบทำวัตรเย็น':
        'kam à-tí-baai bprà-gɔ̀ɔp tam-wát yen',
    'คำเชิญบูชาพระรัตนตรัยพิเศษ':
        'kam chəən buu-chaa prá-rát-dtà-ná-dtrai pí-sèet',
    'คาถาอาราธนาธรรม':
        'kaa-tǎa aa-râat-tá-naa tam',
    'คำถวายดอกไม้ ธูป เทียน ในวันวิสาขบูชา':
        'kam tà-wǎai dɔ̀ɔk-máai tûup tiian nai wan wí-sǎa-kà-buu-chaa',
    'สะระภัญญะคาถา สำหรับสวดในวันวิสาขบูชา':
        'sà-rá-pan-yá-kaa-tǎa sǎm-ràp sùat nai wan wí-sǎa-kà-buu-chaa',
    'คำถวายดอกไม้ ธูป เทียน ในวันอัฏฐมีบูชา':
        'kam tà-wǎai dɔ̀ɔk-máai tûup tiian nai wan àt-tà-mii-buu-chaa',
    'สะระภัญญะคาถา สำหรับสวดในวันอัฏฐมีบูชา':
        'sà-rá-pan-yá-kaa-tǎa sǎm-ràp sùat nai wan àt-tà-mii-buu-chaa',
    'คำถวายดอกไม้ ธูป เทียน ในวันมาฆบูชา':
        'kam tà-wǎai dɔ̀ɔk-máai tûup tiian nai wan maa-ká-buu-chaa',
    'สะระภัญญะคาถา สำหรับสวดในวันมาฆบูชา':
        'sà-rá-pan-yá-kaa-tǎa sǎm-ràp sùat nai wan maa-ká-buu-chaa',
    'บทขัดโอวาทะปาติโมกขาทิปาฐะ':
        'bòt-kàt oo-waa-tà-bpaa-dtì-môok-kǎa-tí-bpaa-tà',
    'คำถวายดอกไม้ ธูป เทียน ในวันอาสาฬหบูชา':
        'kam tà-wǎai dɔ̀ɔk-máai tûup tiian nai wan aa-sǎan-hà-buu-chaa',
    'พระสูตร พระปริตร ปาฐะ และคาถาที่กำหนดสวดในภาคเย็น':
        'prá-sùut prá-bpà-rìt bpaa-tà lɛ́ kaa-tǎa tîi gam-nòt sùat nai pâak yen',
    'บทขัดชุมนุมเทวดา':
        'bòt-kàt chum-num tee-wá-daa',
    'บทขัดต้นตำนาน':
        'bòt-kàt dtôn-dtam-naan',
    'บทขัดมังคะละสุตตัง':
        'bòt-kàt maŋ-ká-lá-sùt-dtaŋ',
    'บทขัดระตะนะสุตตัง':
        'bòt-kàt rá-dtà-ná-sùt-dtaŋ',
    'บทขัดกะระณียะเมตตะสุตตัง':
        'bòt-kàt gà-rá-nii-yá-mêet-dtà-sùt-dtaŋ',
    'บทขัดขันธะปะริตตัง ฉัททันตะปะริตัง':
        'bòt-kàt kǎn-tá-bpà-rít-dtaŋ chàt-tan-dtà-bpà-rí-dtaŋ',
    'บทขัดโมระปะริตตัง':
        'bòt-kàt moo-rá-bpà-rít-dtaŋ',
    'บทขัดวัฏฏะกะปะริตตัง':
        'bòt-kàt wát-dtà-gà-bpà-rít-dtaŋ',
    'บทขัดธะชัคคะสุตตัง':
        'bòt-kàt tá-chák-ká-sùt-dtaŋ',
    'บทขัดอาฏานาฏิยะปะริตตัง':
        'bòt-kàt aa-dtaa-naa-dtì-yá-bpà-rít-dtaŋ',
    'บทขัดอังคุลิมาละปะริตตัง':
        'bòt-kàt aŋ-kú-lí-maa-lá-bpà-rít-dtaŋ',
    'บทขัดโพชฌังคะปะริตตัง':
        'bòt-kàt poot-chaŋ-ká-bpà-rít-dtaŋ',
    'บทขัดอะภะยะปะริตตัง':
        'bòt-kàt à-pá-yá-bpà-rít-dtaŋ',
    'บทขัดชะยะปะริตตัง':
        'bòt-kàt chá-yá-bpà-rít-dtaŋ',
    'มงคลจักรวาฬใหญ่':
        'moŋ-kon jàk-grà-waan yài',
    'บทขัดทะสะนาถะกะระณะธัมมะสุตตัง':
        'bòt-kàt tá-sà-naa-tà-gà-rá-ná-tam-má-sùt-dtaŋ',
    'บทขัดอะภิณ์หะปัจจะเวกขะณะปาฐะ':
        'bòt-kàt à-pin-hà-bpàt-jà-wêek-kà-ná-bpaa-tà',
    'บทขัดมัคคะวิภังคะสุตตัง':
        'bòt-kàt mák-ká-wí-paŋ-ká-sùt-dtaŋ',
    'บทขัดกะระณียากะระณียะสุตตัง':
        'bòt-kàt gà-rá-nii-yaa-gà-rá-nii-yá-sùt-dtaŋ',
    'บทขัดอัคคัปปะสาทะสุตตัง':
        'bòt-kàt àk-kàp-bpà-sǎa-tà-sùt-dtaŋ',
    'บทขัดฉะสาราณียะธัมมะสุตตัง':
        'bòt-kàt chà-sǎa-raa-nii-yá-tam-má-sùt-dtaŋ',
    'บทขัดภิกขุอะปะริหานิยะธัมมะสุตตัง':
        'bòt-kàt pík-kù-à-bpà-rí-hǎa-ní-yá-tam-má-sùt-dtaŋ',
    'บทขัดปะหานะภาวะนาสุตตัง':
        'bòt-kàt bpà-hǎa-ná-paa-wá-naa-sùt-dtaŋ',
    'บทขัดจะตุรัปปะมัญญาปาฐะ':
        'bòt-kàt jà-dtù-ràp-bpà-man-yaa-bpaa-tà',
    'บทขัดธัมมะนิยามะสุตตัง':
        'bòt-kàt tam-má-ní-yaa-má-sùt-dtaŋ',
    'บทขัดอะนัตตะลักขะณะสุตตัง':
        'bòt-kàt à-nát-dtà-lák-kà-ná-sùt-dtaŋ',
    'บทขัดอาทิตตะปะริยายะสุตตัง':
        'bòt-kàt aa-tít-dtà-bpà-rí-yaa-yá-sùt-dtaŋ',
    'บทขัดสะติปัฏฐานะปาฐะ':
        'bòt-kàt sà-dtì-bpàt-tǎa-ná-bpaa-tà',
    'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันโกน วันพระ เวลาเย็น':
        'prá-sùut prá-bpà-rìt prá-bpaa-tà tîi gam-nòt sùat nai wan goon wan prá wee-laa yen',
    'บทขัดธัมมะจักกัปปะวัตตะนะสุตตัง':
        'bòt-kàt tam-má-jàk-gàp-bpà-wát-dtà-ná-sùt-dtaŋ',
    'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันขึ้นหรือแรม ๘ ค่ำ เวลาเย็น':
        'prá-sùut prá-bpà-rìt prá-bpaa-tà tîi gam-nòt sùat nai wan kʉ̂n rʉ̌ʉ rɛɛm 8 kâm wee-laa yen',
    'ธะชัคคะปะริตตัง (แบบย่อ)':
        'tá-chák-ká-bpà-rít-dtaŋ (bɛ̀ɛp yɔ̂ɔ)',
    'พระสูตรที่กำหนดสวดในวันขึ้น ๑๔ ค่ำ เวลาเย็น':
        'prá-sùut tîi gam-nòt sùat nai wan kʉ̂n 14 kâm wee-laa yen',
    'บทขัดมะหาสะมะยะสุตตัง':
        'bòt-kàt má-hǎa-sà-má-yá-sùt-dtaŋ',
    'พระสูตรที่กำหนดสวดในวันแรม ๗ ค่ำ เวลาเย็น':
        'prá-sùut tîi gam-nòt sùat nai wan rɛɛm 7 kâm wee-laa yen',
    'พระสูตรที่กำหนดสวดในวันแรม ๑๓ ค่ำหรือ ๑๔ ค่ำ เวลาเย็น':
        'prá-sùut tîi gam-nòt sùat nai wan rɛɛm 13 kâm rʉ̌ʉ 14 kâm wee-laa yen',
    'บทขัดโลกะธัมมะสุตตัง':
        'bòt-kàt loo-gà-tam-má-sùt-dtaŋ',
    'บทสวดมนต์ ทำวัตรเช้า-เย็น แปล':
        'bòt sùat-mon tam-wát cháao-yen bplɛɛ',
    'ทำวัตรเช้า แปล':
        'tam-wát cháao bplɛɛ',
    'ปุพพะภาคะนะมะการ':
        'pùp-pá-paa-ká-ná-má-gaan',
    'พุทธชัยมงคลคาถา (ถวายพรพระ)':
        'pút-tá-chai-moŋ-kon-kaa-tǎa (tà-wǎai pɔɔn prá)',
    'คาถาโพธิบาท':
        'kaa-tǎa poo-tí-bàat',
    'คาถามงคลจักรวาฬแปดทิศ':
        'kaa-tǎa moŋ-kon jàk-grà-waan bpɛ̀ɛt tít',
    'คำแผ่เมตตาให้แก่ตนเอง':
        'kam pɛ̀ɛ mêet-dtaa hâi gɛ̀ɛ dton-eeŋ',
    'คำแผ่เมตตาให้ผู้อื่น':
        'kam pɛ̀ɛ mêet-dtaa hâi pûu-ʉ̀ʉn',
    'บทพิจารณาสังขาร':
        'bòt pí-jaa-rá-naa sǎŋ-kǎan',
    'ทำวัตรเย็นแปล':
        'tam-wát yen bplɛɛ',
    'นมัสการพระอรหันต์ ๘ ทิศ':
        'ná-mát-sà-gaan prá-à-rá-han 8 tít',
    'พระคาถาชินบัญชร':
        'prá-kaa-tǎa chin-ná-ban-chɔɔn',
    'ยอดพระกัณฑ์ไตรปิฎก':
        'yɔ̂ɔt prá-gan dtrai-bpì-dòk',
    'ภาคปกิณกะ':
        'pâak bpà-gin-ná-gà',
    'คำอาราธนาศีล ๕ ปรกติ':
        'kam aa-râat-tá-naa sǐin 5 bpròk-gà-dtì',
    'คำอาราธนาศีล ๕ พิเศษ คือ นิจศีล':
        'kam aa-râat-tá-naa sǐin 5 pí-sèet kʉʉ nít-jà-sǐin',
    'คำอาราธนาศีล ๘ ปรกติ':
        'kam aa-râat-tá-naa sǐin 8 bpròk-gà-dtì',
    'คำอาราธนาศีล ๘ พิเศษ คืออุโบสถศีล':
        'kam aa-râat-tá-naa sǐin 8 pí-sèet kʉʉ u-boo-sòt-sǐin',
    'คำอาราธนาสวดพระปริตร':
        'kam aa-râat-tá-naa sùat prá-bpà-rìt',
    'คำอาราธนาแสดงธรรม':
        'kam aa-râat-tá-naa sà-dɛɛŋ tam',
    'คำอาราธนาแสดงธรรมอย่างพิสดาร':
        'kam aa-râat-tá-naa sà-dɛɛŋ tam yàaŋ pít-sà-daan',
    'คำบังสุกุลศพหรืออัฐิ':
        'kam baŋ-sù-gun sòp rʉ̌ʉ àt-tì',
    'คำบังสุกุลคนเป็น':
        'kam baŋ-sù-gun kon bpen',
    'คำขอขมาโทษพระรัตนตรัย':
        'kam kɔ̌ɔ kà-maa tôot prá-rát-dtà-ná-dtrai',
    'คำขอขมาโทษแด่พระมหาเถระ':
        'kam kɔ̌ɔ kà-maa tôot dɛ̀ɛ prá-má-hǎa-těe-rá',
    'คำรับขมาโทษของพระมหาเถระ':
        'kam ráp kà-maa tôot kɔ̌ɔŋ prá-má-hǎa-těe-rá',
    'คำอนุโมทนาของพระมหาเถระ':
        'kam à-nú-moo-tá-naa kɔ̌ɔŋ prá-má-hǎa-těe-rá',
    'คาถาจุดเทียนชัย':
        'kaa-tǎa jùt tiian-chai',
    'คาถาดับเทียนชัย':
        'kaa-tǎa dàp tiian-chai',
    'อธิบายระเบียบสวดมนต์ในพิธีต่าง ๆ':
        'à-tí-baai rá-bìiap sùat-mon nai pí-tii dtàaŋ-dtàaŋ',
    'ระเบียบสวดมนต์งานพิธีมงคล':
        'rá-bìiap sùat-mon ŋaan pí-tii moŋ-kon',
    'ระเบียบสวดมนต์งานพิธีมงคลอื่น ๆ':
        'rá-bìiap sùat-mon ŋaan pí-tii moŋ-kon ʉ̀ʉn-ʉ̀ʉn',
    'ระเบียบสวดเจ็ดตำนานอย่างเต็มที่':
        'rá-bìiap sùat jèt dtam-naan yàaŋ dtem-tîi',
    'ระเบียบสวดเจ็ดตำนานอย่างปานกลาง':
        'rá-bìiap sùat jèt dtam-naan yàaŋ bpaan-glaaŋ',
    'ระเบียบสวดเจ็ดตำนานอย่างย่อ':
        'rá-bìiap sùat jèt dtam-naan yàaŋ yɔ̂ɔ',
    'ระเบียบสวดถวายพรพระก่อนฉัน':
        'rá-bìiap sùat tà-wǎai pɔɔn prá gɔ̀ɔn chǎn',
    'ระเบียบสวดในงานพิธีอวมงคล':
        'rá-bìiap sùat nai ŋaan pí-tii à-wá-moŋ-kon',
    'อธิบายระเบียบสวดมนต์พิเศษ':
        'à-tí-baai rá-bìiap sùat-mon pí-sèet',
    'ระเบียบสวดมนต์นพเคราะห์':
        'rá-bìiap sùat-mon nóp-pá-krɔ́',
    'ระเบียบถวายพรพระ':
        'rá-bìiap tà-wǎai pɔɔn prá',
    'ระเบียบอนุโมทนา':
        'rá-bìiap à-nú-moo-tá-naa',
    'อนุโมทนาวิธี':
        'à-nú-moo-tá-naa-wí-tii',
    'มงคลจักรวาฬน้อย (ย่อ)':
        'moŋ-kon jàk-grà-waan nɔ́ɔi (yɔ̂ɔ)',
    'ติโรกุฑฑะกัณฑะปัจฉิมภาค':
        'dtì-roo-kút-tá-gan-tá-bpàt-chǐm-má-pâak',
    'อาฏานาฏิยะปะริตตัง (ย่อ)':
        'aa-dtaa-naa-dtì-yá-bpà-rít-dtaŋ (yɔ̂ɔ)',
    'ระเบียบบังสุกุล':
        'rá-bìiap baŋ-sù-gun',
    'คาถาศราทธพรต':
        'kaa-tǎa sà-râat-tá-pá-rót',
    'คำอธิบายประกอบ':
        'kam à-tí-baai bprà-gɔ̀ɔp',
    'ภาคผนวก':
        'pâak pà-nùak',
    'วิธีบรรพชาอุปสมบทแบบอุกาสะ':
        'wí-tii ban-pá-chaa ù-bpà-sǒm-bòt bɛ̀ɛp u-gaa-sà',
    'วิธีบรรพชาอุปสมบทแบบเอสาหัง':
        'wí-tii ban-pá-chaa ù-bpà-sǒm-bòt bɛ̀ɛp ee-sǎa-hǎŋ',
    'คำขอบรรพชานาคคู่':
        'kam kɔ̌ɔ ban-pá-chaa nâak-kûu',
    'คำขอนิสสัยนาคคู่':
        'kam kɔ̌ɔ nít-sǎi nâak-kûu',
    'คำขออุปสมบทพร้อมกัน':
        'kam kɔ̌ɔ ù-bpà-sǒm-bòt prɔ́ɔm-gan',
    'คำบอกอนุศาสน์':
        'kam bɔ̀ɔk à-nú-sǎat',
    'แบบสวดกรรมวาจาในอุปสมบทกรรม สำหรับนาคเดี่ยว':
        'bɛ̀ɛp sùat gam-má-waa-jaa nai ù-bpà-sǒm-bòt-gam sǎm-ràp nâak-dìiao',
    'คำสมมติตนเพื่อสอนซ้อม':
        'kam sǒm-mút dton pʉ̂a sɔ̌ɔn-sɔ́ɔm',
    'คำสอนซ้อม':
        'kam sɔ̌ɔn-sɔ́ɔm',
    'คำเรียกอุปสัมปทาเปกขะเข้ามา':
        'kam rîiak ù-bpà-sǎm-bpá-taa-bpèek-kà kâo-maa',
    'คำพระอุปัชฌายะกล่าวเผดียงสงฆ์':
        'kam prá-ù-bpàt-chaa-yá glàao pà-diiaŋ sǒŋ',
    'คำสมมติตนเพื่อถามอันตรายิกธรรม':
        'kam sǒm-mút dton pʉ̂a tǎam an-dtà-raa-yí-gà-tam',
    'คำถามอันตรายิกธรรม':
        'kam tǎam an-dtà-raa-yí-gà-tam',
    'กรรมวาจาอุปสมบท':
        'gam-má-waa-jaa ù-bpà-sǒm-bòt',
    'คำสวดสมมติและคำสอนซ้อม (นาคคู่)':
        'kam sùat sǒm-mút lɛ́ kam sɔ̌ɔn-sɔ́ɔm (nâak-kûu)',
    'คำขอเรียกอุปสัมปทาเปกขะเข้ามา':
        'kam kɔ̌ɔ rîiak ù-bpà-sǎm-bpá-taa-bpèek-kà kâo-maa',
    'คำสมมติตนและคำถามอันตรายิกธรรม':
        'kam sǒm-mút dton lɛ́ kam tǎam an-dtà-raa-yí-gà-tam',
    'คำพระอุปัชฌาย์กล่าวเผดียงสงฆ์':
        'kam prá-ù-bpàt-chaa glàao pà-diiaŋ sǒŋ',
    'คำสวดกรรมวาจาอุปสมบท':
        'kam sùat gam-má-waa-jaa ù-bpà-sǒm-bòt',
    'คำขอบวชชี':
        'kam kɔ̌ɔ bùat chii',
    'คำอาราธนาศีล ๘':
        'kam aa-râat-tá-naa sǐin 8',
    'คำนมัสการพระพุทธเจ้า':
        'kam ná-mát-sà-gaan prá-pút-tá-jâo',
    'คำสมาทานศีล':
        'kam sà-maa-taan sǐin',
    'วิธีแสดงอาบัติ':
        'wí-tii sà-dɛɛŋ aa-bàt',
    'คำพินทุผ้า':
        'kam pin-tù pâa',
    'คำอธิษฐาน':
        'kam à-tít-tǎan',
    'คำเสียสละ':
        'kam sǐia-sà-là',
    'คำคืน':
        'kam kʉʉn',
    'คำวิกัปป์':
        'kam wí-gàp',
    'คำถอน':
        'kam tɔ̌ɔn',
    'คำอธิษฐานเข้าพรรษา':
        'kam à-tít-tǎan kâo-pan-sǎa',
    'คำปวารณาออกพรรษา':
        'kam bpà-waa-rá-naa ɔ̀ɔk-pan-sǎa',
    'คำสัตตาหะ':
        'kam sàt-dtaa-hà',
    'คำอนุโมทนากฐิน':
        'kam à-nú-moo-tá-naa gà-tǐn',
    'คำลาสิกขา':
        'kam laa-sìk-kǎa',
    'คำแสดงตนเป็นอุบาสก':
        'kam sà-dɛɛŋ dton bpen ù-baa-sòk',
    'กิจวัตร ๑๐ อย่าง':
        'gìt-jà-wát 10 yàaŋ',
    'คำอปโลกน์กฐิน แบบ ๒ รูป':
        'kam à-bpà-lòok gà-tǐn bɛ̀ɛp 2 rûup',
    'คำอปโลกน์กฐิน แบบ ๔ รูป':
        'kam à-bpà-lòok gà-tǐn bɛ̀ɛp 4 rûup',
    'แบบกรรมวาจาสวดให้ผ้ากฐิน':
        'bɛ̀ɛp gam-má-waa-jaa sùat hâi pâa gà-tǐn',
    'คำอธิษฐานผ้ากฐิน':
        'kam à-tít-tǎan pâa gà-tǐn',
}


# The two together, which is what the contents page reads. Kept as two
# dicts above rather than one flat table because WHICH SYSTEM a reading is
# in has to survive into the template — the contents page colours the line
# by it — and sniffing the string cannot tell you: Sekhiyavatta is IAST
# and carries no diacritic at all, so it would be filed as Thai.
_CONTENTS_ROMAN = {**_CONTENTS_PALI_ROMAN, **_CONTENTS_PAIBOON}

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
    The same goes for the romanised title: a chant's `title_pali` or
    `title_roman` wins over the table, so a reader is never given two spellings
    of one title depending on which page they came in by.
    Both lookups are built once here rather than searched per row: at 301 rows
    against a book heading for 286 chants, a linear scan per row is ~86,000
    comparisons to answer a question a dict answers outright.
    """
    if chants is None:
        chants = CHANTS

    chant_id_by_title = {}
    english_by_title = {}
    roman_by_title = {}
    roman_fallback_by_title = {}
    for chant in chants:
        title = chant.get('title_thai')
        if not title:
            continue
        chant_id_by_title.setdefault(title, chant['id'])
        if chant.get('title_english'):
            english_by_title.setdefault(title, chant['title_english'])
        if chant.get('title_pali'):
            roman_by_title.setdefault(title, chant['title_pali'])
        if chant.get('title_roman'):
            roman_fallback_by_title.setdefault(title, chant['title_roman'])

    return [
        {
            'front_page': front,
            'level': level,
            'title': title,
            'title_english': english_by_title.get(
                title, _CONTENTS_ENGLISH.get(title, '')),
            # title_pali, then the table, then title_roman — in that order for
            # a reason. `title_pali` is IAST and is the same system the table
            # uses, so it can be trusted first. `title_roman` is older and
            # mixed: four Pali titles carry an undiacriticked romanisation
            # (Ratanattayappanamagatha), which reads as a different word from
            # the Ratanattayappaṇāmagāthā the rest of the contents shows. It is
            # kept as a last resort, because a rough romanisation still beats a
            # Thai-only line, but it must not outrank a proper one.
            'title_roman': (
                roman_by_title.get(title)
                or _CONTENTS_ROMAN.get(title)
                or roman_fallback_by_title.get(title, '')),
            # WHICH system that reading is in, named with the CHANT_LAYERS key
            # so the contents page can colour the line the same as the layer it
            # corresponds to without a second mapping in between. Taken from
            # which table the title is in, never sniffed from the reading:
            # Sekhiyavatta is IAST and carries no diacritic at all.
            'roman_system': (
                'pali_roman' if title in _CONTENTS_PALI_ROMAN else 'paiboon'),
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
    stretches = contents_stretches(chants)
    rows = build_contents(chants, front_page=number)
    return [dict(row,
                 in_app=row['page'] in have,
                 pages=[p for p in stretches.get(row['page'], [row['page']])
                        if p in have])
            for row in rows], entered


def contents_stretches(chants=None):
    """Every page a contents line covers, keyed by the page it starts on.

    The สารบัญ names where each chant BEGINS, so a page it merely continues
    onto is named nowhere in the book's own contents. Pages 5 and 21 are both
    like this: entered, openable, and invisible on the contents page, which
    is how a reader ends up believing they are missing.

    A line's stretch runs from its own page up to where the NEXT line begins,
    which is the book's own structure rather than an assumption about chants —
    it works even where a line could not be matched to a chant in the app, as
    Parittakaraṇapāṭho on page 20 could not.

    This adds no line the book does not print. The สารบัญ text, its order and
    its numbers are untouched; only the app's own navigation beside a line
    learns about the pages that line runs across.
    """
    listed = sorted({row['page'] for row in build_contents(chants)
                     if row['page']})
    stretches = {}
    for position, page in enumerate(listed):
        following = listed[position + 1] if position + 1 < len(listed) else None
        stretches[page] = (list(range(page, following)) if following
                           else [page])
    return stretches


#: The last page the book's own สารบัญ names. Used only to say how far the
#: printed book runs; the app never derives a page's existence from it.
BOOK_LAST_PAGE = 308


def _runs(numbers):
    """Consecutive numbers collapsed into (first, last) pairs.

    [1, 2, 3, 7, 8] -> [(1, 3), (7, 8)]. Shared so that a chant's span and the
    book's coverage are described by the same rule and cannot disagree.
    """
    runs = []
    for number in sorted(set(numbers)):
        if runs and number == runs[-1][1] + 1:
            runs[-1][1] = number
        else:
            runs.append([number, number])
    return [(first, last) for first, last in runs]


def chant_page_spans(chants=None, page_blocks=None):
    """Every page each chant is printed on, in order.

    The index card shows where a chant BEGINS, which is not the same as where
    it is. Parittakaraṇapāṭha starts on page 20 and runs to 22, so pages 21 and
    22 appeared nowhere on the index even though both are entered and both
    open — and page 5 was invisible the same way, being the second half of a
    chant that starts on 4. A reader could only reach them by typing the number
    and hoping.

    Read out of the page index rather than from `page_start` plus an
    assumption, so a chant is listed on exactly the pages it was really placed
    on and cannot claim one it does not reach.
    """
    pages, _ = build_page_index(chants, page_blocks)
    spans = {}
    for page in pages:
        for entry in page['entries']:
            if entry['kind'] == 'chant':
                spans.setdefault(entry['chant']['id'], []).append(page['page'])
    return spans


def page_coverage(chants=None, page_blocks=None):
    """Which body pages are in, as runs of consecutive pages.

    [1, 2, 3, 7, 8] -> [(1, 3), (7, 8)].

    The landing page invites a reader to type any page number the monk calls
    out, and until this existed it said nothing about which numbers would
    work. Most would not: 34 pages of 308 are in. Someone mid-service typing
    112 and getting "not added yet" learns that at the worst possible moment.

    Runs rather than a count, because a count cannot say the one thing that
    matters here. "34 pages" reads as 1 to 34 and is wrong twice over: the
    app's pages stop at 29 and then resume in the two-hundreds. Only the runs
    say where the book actually opens.

    Derived from the page index every time rather than recorded anywhere, so
    it cannot drift from what the app will really serve — the failure a
    hand-maintained "pages 1-20 so far" line makes certain.
    """
    pages, _ = build_page_index(chants, page_blocks)
    return _runs(page['page'] for page in pages)


def describe_pages(numbers):
    """A chant's pages as English: '4–5', '20–22', or '27' for one.

    Takes the numbers rather than runs, because that is what a caller holding
    a chant's span has.
    """
    return describe_coverage(_runs(numbers))


def describe_coverage(runs):
    """The runs as English: '1-29 and 217-221'. Empty string for none.

    A single-page run prints as one number, not '5-5', because the book is
    read by people and that is how a page is named.
    """
    parts = [str(first) if first == last else f"{first}–{last}"
             for first, last in runs]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return f"{', '.join(parts[:-1])} and {parts[-1]}"


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


def check_variants(chants=None):
    """Return a list of problems with the verse `variants`, empty when sound.

    A variant reading is a footnote about ONE WORD on ONE LINE, and the only
    thing that makes it readable is that the reader can see which word. So the
    check that matters is that `word` actually occurs in the line it is filed
    against — a variant hung on the wrong verse would render as a note about a
    word that is not there, which is a puzzle rather than a note.

    That is the same fault the photo map records twice over: a footnote taken
    by the chant nearest the foot of the page rather than the one its marker
    sits on, and this very footnote filed against verse 4 when the pādas were
    one to a line. Both were caught by eye, months apart. This catches them on
    import.

    `reading` is checked only for being present and different from `word`. A
    variant that repeats the word it varies is a transcription slip — it says
    the book printed a footnote to tell you nothing.
    """
    if chants is None:
        chants = CHANTS

    problems = []
    for chant in chants:
        for verse in chant['verses']:
            for index, variant in enumerate(verse.get('variants', ())):
                where = (f"{chant['id']} verse {verse.get('number')}, "
                         f"variant {index}")
                word = variant.get('word')
                if not word:
                    problems.append(f'{where}: names no word')
                # Either chanted layer may be the one the book printed — part
                # of this book sets its Pali in roman letters and leaves `pali`
                # empty — so the word is looked for in both rather than in
                # whichever one this half of the book happens to use.
                elif word not in (verse.get('pali') or '') and \
                        word not in (verse.get('pali_roman') or ''):
                    problems.append(
                        f"{where}: '{word}' is not in this verse, so the "
                        f"variant is filed against the wrong line"
                    )
                if not variant.get('reading'):
                    problems.append(f'{where}: no `reading`, so it says nothing')
                elif variant.get('reading') == word:
                    problems.append(
                        f'{where}: `reading` repeats `word` unchanged')
                if not variant.get('marker'):
                    problems.append(f'{where}: no printed marker')
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

        # Down-page order, where the book itself settles it. Entries arrive in
        # the order the chants sit in CHANTS, which is book order right up
        # until a chant is ADDED later than its neighbours — a new chant is
        # appended to the end of the file, so it lands at the bottom of its
        # page however early in the book it is printed. Ādiyasutta, numbered
        # 13, rendered beneath Pabbatopama, numbered 14, on page 30.
        #
        # The book's own numbering is the answer where every chant on the page
        # carries one, because a book does not print its chants out of numeric
        # order. Where any of them does not — most of the morning service is
        # unnumbered — nothing is known that beats the existing order, so it
        # is left exactly as it was.
        numbers = [entry['chant'].get('book_number') for entry in chant_entries]
        if len(chant_entries) > 1 and all(n is not None for n in numbers):
            chant_entries.sort(key=lambda entry: entry['chant']['book_number'])
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
