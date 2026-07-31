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

## Verse breakdown — make it a book people can read and chant from

Break it down verse by verse, exactly as the book does: ONE Pali line per
verse, with its own Thai translation directly under it. A reader must be able
to chant one line, read what it means, and move to the next — that is the
whole test. Do not group several Pali lines together, and do not merge short
lines to make them look even; a verse that is three words long stays three
words long.

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

## Working notes — inside the JSON, not around it

Show your working, but put it in the `working_notes` object of the JSON rather
than as prose before or after it. That keeps the whole reply one pasteable
thing. Keep each note to a sentence or two:

1. **invitation** — present or absent. If absent, say so explicitly and say you
   have not written one.
2. **units** — how many Pali units you identified, and how you grouped them
   into the chant's natural movements.
3. **ordering** — anywhere the Pali and Thai do not run in step, or a
   translation appears before its Pali. Say you have kept my text as pasted and
   only noted the mismatch.
4. **conventions** — if anything I pasted uses a different romanisation from
   the Paiboon+ table above (RTGS spellings such as `sangkhaan`, `phrɔ́`,
   `thîang`), say so and confirm you have used the table, not my sample. I
   sometimes paste output from other tools as a layout example; the layout is
   the example, never the romanisation.

Then produce the entry.

## Reproduce oddities, don't tidy them

If the source has a missing space, a doubled comma, an unusual spacing or an
inconsistent particle, reproduce it exactly and add a ⚠️ CHECK saying what
looks odd. Silent tidying is the failure this whole prompt exists to prevent.

## Where the checks go

Every one goes in the top-level `checks` array, and every one names the verse
it belongs to via its `verse` number — or `null` if it concerns the chant as a
whole (a missing invitation, an uncertain title). A check that does not say
which verse it is about cannot be acted on.

Raise a check for: anything OCR-garbled or possibly mistyped, a spelling that
differs from standard editions, Pali and Thai running out of step, a missing
invitation or title, an inferred line break, an attributed source, and any
typographic oddity you reproduced rather than tidied.

The closing sentence counting them is the most useful line in the reply — it
tells me how much verifying this chant needs before it goes in the app.

## Output format — one JSON object

Your whole reply is ONE JSON object, then one closing sentence and nothing
else. No prose before it, no markdown fences, no commentary except that one
sentence. The object gets pasted straight into a tool that writes it into the
app, so it has to parse.

Two formatting rules that matter more than they look:

- **Every value on ONE line.** Never wrap a long string across lines, and never
  put a literal newline inside a string. Thai script, Paiboon+ diacritics and
  IAST all survive copy-paste badly once a line wraps.
- **The checks go in their own top-level array**, not inline. Each one names
  the verse it belongs to so nothing floats free.

{
  "working_notes": {
    "invitation": "<present, or absent and therefore not written>",
    "units": "<how many Pali units, and how you grouped them>",
    "ordering": "<any place the Pali and Thai do not run in step, or none>",
    "conventions": "<any romanisation conflict in what I pasted, or none>"
  },
  "title_thai": "<the chant's title in Thai script>",
  "title_pali": "<the title in IAST, or \"\" if the book gives none>",
  "title_english": "<the traditional English title>",
  "source": "<canonical source. If compiled from several places, start with \"Composite.\" and say which verses come from where. Use \"\" if you are not certain — do not guess.>",
  "when_chanted": "<one sentence on when it is recited>",
  "summary": "<one sentence, max 30 words, for the index card>",
  "background": ["<paragraph>", "<paragraph>"],
  "meaning": ["<paragraph>", "<paragraph>", "<paragraph>"],
  "invitation": {
    "pali": "<Thai script, or \"\" if the book gives none>",
    "pali_roman": "<IAST, or \"\">",
    "english": "<meaning, or \"\">"
  },
  "verses": [
    {
      "number": 1,
      "section": "<สังขาร: The Three Characteristics — only on the FIRST verse of a section; omit the key otherwise>",
      "pali": "<ONE Pali line, Thai script>",
      "pali_roman": "<the same line, IAST>",
      "thai": "<its Thai translation>",
      "paiboon": "<Paiboon+ of the thai line only>",
      "english": "<its meaning>"
    }
  ],
  "checks": [
    {"verse": 6, "issue": "<what looks wrong and what to compare it against>"},
    {"verse": null, "issue": "<a check about the chant as a whole>"}
  ]
}

`background` and `meaning` are arrays — one string per paragraph. `checks` is
empty (`[]`) only if genuinely nothing needs verifying, which is rare.

After the JSON, add nothing except one plain sentence counting the checks:

  "Six things need your eye against the physical book."

## Sections — name them the way the book thinks

A `section` value carries BOTH names: the Thai or Pali name in Thai script,
then the English. So:

  "section": "สังขาร: The Three Characteristics"
  "section": "มะระณัสสะติ: The Recollection of Death"
  "section": "กายะคะตาสะติ: Reflection on the Body"

Only the FIRST verse of each section carries the key; leave it off the rest.

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

I'm pasting the JSON object from stage 1 — the whole reply is fine, the
trailing sentence after the closing brace is just a note to me; ignore it.

Its keys already match the dict keys one for one —
title_thai, title_pali, title_english, source, when_chanted, summary,
background, meaning, invitation, verses — so map them straight across. Each
verse keeps its 'number', and its 'section' where it has one.

Two keys do NOT go in as-is:
  working_notes  → ignore. It is Josh's reading aid, not data.
  checks         → turn each entry into a ⚠️ code comment. A check with a
                   "verse" number goes directly above that verse; a check with
                   "verse": null goes at the top of the chant dict. NEVER drop
                   one silently — they are what Josh still has to verify
                   against the physical book. Tell me how many you carried
                   across when you report back.

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
