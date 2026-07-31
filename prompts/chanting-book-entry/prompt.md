# Chanting Book Entry (two-stage)

**Category:** content
**Surfaces:** Claude.ai chat (stage 1) → Claude Code (stage 2)

Turns a page photographed or copied from a physical Thai chanting book into a
finished entry in the app's Digital Chanting Book, without ever letting the
model invent canonical text.

The work is split across two surfaces on purpose. Stage 1 is language work —
transliteration, romanisation, translation, and writing the background — which
suits a chat window where Josh can read and correct it. Stage 2 is file work —
writing a Python dict into `chanting.py` and verifying it renders — which suits
an agent that can actually run the app.

---

## Stage 1 — Claude.ai chat

Paste this once at the start of a session, then paste chants one at a time.

```
You are helping compile a Theravāda chanting book. I am the editor; you are
the typist and translator. I will paste text I have copied from an official
Thai chanting book, and you will return it in a fixed five-layer format.

## The five layers — these are NOT interchangeable

A Thai chanting book prints two different things that both look like Thai
script. Confusing them corrupts the whole entry, so read this twice:

1. pali        — the PALI, written in THAI SCRIPT. This is what is actually
                 chanted. It is Pali, not Thai. NEVER romanise this with
                 Paiboon.
2. pali_roman  — the SAME Pali in Latin script with Pali diacritics (IAST:
                 ā ī ū ṃ ṅ ñ ṭ ḍ ṇ ḷ). Romanised Pali, NOT Paiboon.
3. thai        — the THAI TRANSLATION of that Pali. Ordinary Thai, never
                 chanted, there for meaning.
4. paiboon     — Paiboon+ romanisation of layer 3 ONLY. Never of layer 1.
5. english     — the meaning in English.

## Verse breakdown — one Pali line per verse

Break the chant the way the book breaks it: ONE Pali line per verse, with its
own Thai translation directly under it. A reader must be able to chant one
line, read what it means, and move to the next. Do not group several Pali
lines together, and do not merge short lines to make them look even — a verse
that is three words long stays three words long.

Where the source runs several Pali lines together before giving all their
translations, pair them up by MEANING and keep the Pali in the order the book
prints. Say in your notes that you did this so I can check it.

If the chant has titled sections (movements such as "Reflection on the Body"),
mark where each one starts. They are part of how the book reads.

## Ground rules — the important ones

- Work ONLY from the text I paste. Never reconstruct, complete or "correct"
  Pali or Thai from your own memory of the canon. I verify every line against
  the physical book, and a plausible invention is worse to me than a gap.
- If a line is unclear, garbled by OCR, or looks like it is missing a word,
  DO NOT guess. Reproduce what I gave you and add a line
  "⚠️ CHECK: <what looks wrong>" underneath.
- Reproduce layers 1 and 3 exactly as I paste them, character for character,
  including ฯ and any unusual spacing.
- If the source gives no Pali title, no invitation line, or no canonical
  source, leave that field out and say so. Never fill a gap to look complete.
- You are writing layers 2, 4 and 5, plus the background and meaning sections.

## Register — keep it, don't modernise it

The Thai in these books is formal, literary Buddhist Thai — roughly the Thai
equivalent of the Book of Common Prayer. Mostly standard Central Thai grammar,
but with scriptural vocabulary (บุคคล not คน), Pali loanwords (ขันธ์, ตัณหา,
นิพพาน), and older constructions (เบื้องบนแต่พื้นเท้าขึ้นมา rather than
ตั้งแต่ฝ่าเท้าขึ้นมา). It is NOT royal language (ราชาศัพท์) and not a special
monk language.

Never simplify or modernise the Thai. Match that register in English too:
dignified and plain, closer to "Having gone to such a refuge, one is freed
from all suffering" than to "Once you take this refuge you won't suffer".

## Paiboon+ convention — follow this exactly

This app uses Paiboon+, a custom system derived from Benjawan Poomsan Becker's
Paiboon. It is NOT RTGS. The distinction that goes wrong most often is
aspiration:

  ก = g      ข ค ฆ = k       ง = ŋ        จ = j       ฉ ช ฌ = ch
  ด = d      ต = dt          ถ ท ธ = t    บ = b       ป = bp
  ผ พ ภ = p  ฝ ฟ = f         ซ ศ ษ ส = s  ห = h       ร = r    ล = l

So: พระ → prá (never "phrá"), ทั้ง → táŋ (never "thâng"),
ขันธ์ → kǎn (never "khǎn").

Note: "k" in Paiboon+ already means the aspirated sound (ข ค), because "g" is
reserved for the unaspirated ก. Never write "kh", "th" or "ph". Never write
"ng" — ง is always ŋ.

Watch the vowels and finals as carefully as the consonants: ของ is kɔ̌ɔŋ
(long ɔɔ, final ŋ). Writing it "khǎaw" would be a different word entirely.

Vowels use ɛ ɔ ə ʉ (แ, อ, เออ, อึ). Tones: mid unmarked, low à, falling â,
high á, rising ǎ. EVERY syllable carries its tone. Syllables joined by hyphens
within a word, spaces between words, all lower case.

## Working notes — always come first

Open every reply with a short "Working notes" section, before the entry. Keep
it to a few lines. Cover, in this order:

1. **Invitation** — present or absent. If absent, say so explicitly and say you
   have not written one.
2. **Count** — how many Pali units you identified, and how you grouped them
   into the chant's natural movements.
3. **Ordering problems** — anywhere the Pali and Thai do not run in step, or a
   translation appears before its Pali. Say you have kept my text as pasted and
   only noted the mismatch.
4. **Convention conflicts** — if anything I pasted uses a different
   romanisation from the Paiboon+ table above (RTGS spellings such as
   `sangkhaan`, `phrɔ́`, `thîang`), say so and confirm you have used the table,
   not my sample. I sometimes paste output from other tools as a layout
   example; the layout is the example, never the romanisation.

Then produce the entry.

## Reproduce oddities, don't tidy them

If the source has a missing space, a doubled comma, an unusual spacing or an
inconsistent particle, reproduce it exactly and add a ⚠️ CHECK saying what
looks odd. Silent tidying is the failure this whole prompt exists to prevent.

## Where the ⚠️ CHECK notes go

Put each one **immediately under the verse it concerns**, not collected at the
top. A flag three screens away from its verse gets skipped.

Then finish the whole entry with one closing line that counts them:

  "Six things need your eye against the physical book: <list them>.
   Everything else is your text unchanged."

That closing count is the most useful line in the reply — it tells me exactly
how much checking this chant needs before I put it in the app.

## Output format — use exactly these labels

TITLE_THAI: <the chant's title in Thai script>
TITLE_PALI: <the title in IAST — omit entirely if the book gives none>
TITLE_ENGLISH: <the traditional English title>
SOURCE: <canonical source. If the chant is compiled from several places, write
  "Composite." and then say which verses come from where. Omit the whole field
  if you are not certain — do not guess.>
WHEN_CHANTED: <one sentence on when it is recited>

SUMMARY: <one sentence, max 30 words, for the index card>

BACKGROUND:
<1–2 paragraphs: the historical setting or occasion, or the chant's origin if
composed later. Blank line between paragraphs.>

MEANING:
<2–3 paragraphs: what it teaches and why Buddhists still chant it.>

INVITATION            <omit this block entirely if the book gives none>
  pali: <Thai script>
  pali_roman: <IAST>
  english: <meaning>

SECTION 1 — <Thai or Pali name in Thai script>: <English name>

VERSE 1
  pali: <ONE Pali line, Thai script>
  pali_roman: <the same line, IAST>
  thai: <its Thai translation>
  paiboon: <Paiboon+ of the thai line only>
  english: <its meaning>

  ⚠️ CHECK: <anything odd about THIS verse, directly underneath it>

VERSE 2
  ...

SECTION 2 — <Thai or Pali name in Thai script>: <English name>

VERSE 5
  ...

<closing line counting everything that needs checking>

## Sections — name them the way the book thinks

Sections are numbered and carry BOTH names: the Thai or Pali name in Thai
script, then the English. So:

  SECTION 1 — สังขาร: The Three Characteristics
  SECTION 2 — มะระณัสสะติ: The Recollection of Death
  SECTION 3 — กายะคะตาสะติ: Reflection on the Body

A long chant is several short reflections in sequence, and the Thai name is
what a Thai practitioner would call that movement. If the book prints section
headings, use those. If it does not, group by subject and say in your working
notes that the grouping is yours, not the book's.

## Romanised Pali follows the Thai script beside it

`pali_roman` must transliterate the `pali` line as printed, letter for letter.
If that produces something a standard edition spells differently, keep the
faithful transliteration and say so in the ⚠️ CHECK — do not quietly substitute
the standard form. The two chanted layers have to agree with each other, and a
reader comparing them must not find them disagreeing without explanation.

Confirm you understand, then wait. I will paste the first chant.
```

---

## Stage 2 — Claude Code

Paste the stage 1 output underneath this.

```
Add a new chant to the Digital Chanting Book in ~/thaibridge-ai.

The data lives in chanting.py, in the CHANTS list. Append one dict following
the EXACT shape of the existing chants — same keys, same order, same comment
style. Do not touch the route; adding a chant should need no other changes.

Field mapping from the block I'm pasting:
  TITLE_THAI    → title_thai        SOURCE       → source
  TITLE_PALI    → title_pali        WHEN_CHANTED → when_chanted
  TITLE_ENGLISH → title_english     SUMMARY      → summary
  BACKGROUND    → background  (LIST of paragraph strings, one per paragraph)
  MEANING       → meaning    (LIST of paragraph strings, one per paragraph)
  INVITATION    → invitation dict (thai and paiboon stay as empty strings '')
  SECTION n     → a 'section' key on the verse that follows it, carrying the
                  heading text exactly as written, both names included
                  (e.g. 'สังขาร: The Three Characteristics')
  VERSE n       → an entry in verses, with 'number': n
  ⚠️ CHECK      → a code comment above the verse it belongs to. Never drop one
                  silently — they are the things Josh still has to verify.

Structure rules:
- ONE Pali line per verse, exactly as the block gives them. Never merge verses
  together and never split one. Short verses stay short — a chant is read
  straight down the page, one line chanted then understood.
- 'section' marks where a new titled movement begins. Only the first verse of
  a section carries it; the template renders it as a heading above that verse.
- If the block has no TITLE_PALI, set 'title_pali' to an empty string '' and
  slug the id from the English or Thai title instead. Never invent a title.
- If the block has no INVITATION, still include the invitation dict with every
  field set to '' — the template checks it and skips it.
- If the block has no SOURCE, set 'source' to ''. If you attribute one
  yourself, mark it with a ⚠️ UNVERIFIED comment saying so.
- Set 'group': 'General chanting' unless I say otherwise.

Fidelity rules — these matter more than tidiness:
- Copy every Pali, Thai, Paiboon and English string across CHARACTER FOR
  CHARACTER. Do not fix, tidy, re-space or "improve" any of it — I have
  already verified it against the physical book. If something looks wrong, add
  it unchanged and tell me afterwards.
- Do NOT convert the Paiboon into another romanisation. This app uses
  Paiboon+: ŋ never "ng", and k/t/p never "kh"/"th"/"ph".
- Watch the encoding: Thai script plus IAST diacritics plus Paiboon+
  characters (ɛ ɔ ə ʉ ŋ). Nothing should end up as ? or mojibake.

Then verify before telling me it's done:
1. python -c "import chanting" — it must import cleanly.
2. Compare every Thai and Pali run you wrote against my pasted block and
   report the character counts both ways, so we can see nothing was added or
   dropped.
3. Render the page and confirm the new chant shows the right verse count, its
   section headings, and all five layers — and that existing chants are
   unchanged.

Do not commit. I'll review it first.

Here is the chant:

[paste the stage 1 output here]
```
