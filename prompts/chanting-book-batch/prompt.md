# Chanting Book Batch (two-stage)

**Category:** content
**Surfaces:** Claude.ai chat (stage 1) → Claude Code (stage 2)
**Sibling:** `../chanting-book-entry/` — the one-chant-at-a-time version. Unchanged. Use that one when you are setting a single chant carefully.

This is the same job as `chanting-book-entry`, rebuilt for volume: a 286-chant
book, several chants per message, across many sessions.

Everything that made the single-chant prompt safe is still here word for word —
the five layers, the Paiboon+ table, the register rules, "never reconstruct from
memory". Batching does not relax any of them. What batching adds is the
machinery for the two failure modes that only appear at volume:

1. **A reply that gets cut off mid-chant.** At one chant a message you would see
   it. At eight you will not, because the JSON still looks like JSON.
2. **Drift.** Paiboon+ adherence decays over a long session. That is the exact
   failure the whole prompt exists to prevent, so the batch version checks
   itself before it closes.

---

## Choose a depth before you start

The output is roughly nine times the size of what you paste in, and Thai script,
IAST and Paiboon+ all tokenise about twice as expensively as English. That
arithmetic — not the wording of the prompt — is what limits how many chants fit
in one reply. So the batch version lets you trade commentary for chants:

| Depth | What you get | Realistic per reply |
|---|---|---|
| `FULL` | Everything, including background and meaning | 2–4 chants |
| `COMPACT` | `background` 1 paragraph, `meaning` 2 | 4–6 chants |
| `DATA-ONLY` | All five layers verse by verse, no chant-level commentary | 6–9 chants |

**All three depths give you all five layers, verse by verse.** What `DATA-ONLY`
drops is the prose written *about* the chant — `background`, `meaning`,
`summary`, `when_chanted` and `source` — which is about 32% of a finished entry
and none of which needs checking against the physical book. Stage 3 adds it
later, reading the chant straight out of `chanting.py`, so you never re-paste
anything.

Say the depth on the first line of your paste. If you don't, it uses `COMPACT`.

---

## Stage 1 — Claude.ai chat

Paste this once at the start of a session, then paste batches of chants.

```
You are helping compile a Theravāda chanting book. I am the editor; you are the
typist and translator. I will paste text I have copied from an official Thai
chanting book — SEVERAL chants at a time — and you will return them in a fixed
five-layer format, as one JSON object containing an array.

## Batch mode — read this section twice

I am working through a book of 286 chants. I will paste batches, numbered, with
a depth on the first line. You return ONE JSON object per batch.

Two rules govern everything else in this section, and they outrank speed,
tidiness and my stated chant count:

  FINISH OR DON'T START.  Never begin a chant you cannot complete. A missing
  chant is obvious to me; a truncated one is not, and a truncated one can reach
  the app looking finished.

  THE MANIFEST DESCRIBES WHAT I GAVE YOU, NOT WHAT YOU MANAGED.  Never trim it
  to match your output. Its whole purpose is to disagree with your output when
  something went wrong.

### The manifest comes first

The FIRST key of your reply is `batch`. It names every chant I pasted, in the
order I pasted them, before you write a single entry.

This ordering is deliberate, not stylistic. If your reply is cut off, the end of
it is gone — so nothing written at the end can tell me it was cut off. A count
written at the START survives, because I compare it against how many entries
actually arrived. If the manifest says eight and six arrived, I know how many
are missing, which ones, and that I should not trust the sixth.

So: manifest first, entries second, status last. If the status is missing, the
reply truncated, and the manifest tells me where to resume.

### Depth

I put one of these on the first line of my paste:

  FULL       — every field, as the single-chant prompt produces.
  COMPACT    — background 1 paragraph, meaning 2. Everything else in full.
  DATA-ONLY  — omit background, meaning, summary, when_chanted and source.
               Keep EVERYTHING else, including all five layers of every verse:
               pali, pali_roman, thai, paiboon AND english, plus sections,
               titles, invitation and checks. This is the verse-by-verse half
               of the job; the chant-level commentary comes later.

Every depth gives all five layers on every verse. `english` is never dropped —
a verse without its meaning is not usable, and the layers are read together.

If I give no depth, use COMPACT. Never quietly change depth mid-batch. If you
switch — because entries are running longer than expected — say so in
`batch_status.notes` and name the chant where you switched.

### Repeats

In a 286-chant book the same chant appears in several different services. If a
chant in this batch is one you have already set earlier in this session, do NOT
set it a second time. Emit a stub instead and move on:

  {"id": "<the id you used before>", "repeat_of": "<same id>",
   "note": "<where it appeared before, and any difference in how it is printed>"}

If the two printings differ at all — a verse more, a different invitation, a
different title — that is NOT a repeat. Set it in full and raise a check saying
how it differs from the earlier one.

### Check yourself before you close the batch

Before writing `batch_status`, scan your own `paiboon` values for these four
strings: "kh", "th", "ph", "ng". None of them can legitimately appear — Paiboon+
uses k, t, p and ŋ. Report the result in `batch_status.paiboon_scan` as a plain
count of hits, and fix any you find before you send. This is a drift check: over
a long session the pull back towards RTGS is strong, and it is the single
failure this prompt most exists to prevent.

Also confirm in `batch_status` that no `pali` value has been run through
Paiboon+, which is the other corruption that cannot be spotted downstream.

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

Break it down verse by verse, exactly as the book does: ONE Pali line per verse,
with its own Thai translation directly under it. A reader must be able to chant
one line, read what it means, and move to the next — that is the whole test. Do
not group several Pali lines together, and do not merge short lines to make them
look even; a verse that is three words long stays three words long.

Where the source runs several Pali lines together before giving all their
translations, pair them up by MEANING and keep the Pali in the order the book
prints. Say in that chant's notes that you did this so I can check it.

If the chant has titled sections (movements such as "Reflection on the Body"),
mark where each one starts. They are part of how the book reads.

## Page numbers — treat these as carefully as the Pali

The monk calls out a page number, and everyone chants from that page. A chant
whose page number is missing or wrong is one a person cannot find in the room,
so these are not decoration — they are how the book is used.

I mark pages in my paste with a line of its own:

    [p.47]

Everything after that marker is on page 47, until the next marker. So:

- `page_start` on the chant is the page it BEGINS on — the marker in force when
  its title appears.
- `page` on a verse appears ONLY where a new printed page begins, exactly the
  same rule `section` follows. The first verse of a chant carries `page` only if
  a page turns at that point; otherwise `page_start` already says where it is.
- Where several verses sit on one page, only the first of them carries `page`.

Two rules that matter as much as any fidelity rule in this prompt:

- NEVER infer, estimate or continue a page number. If I did not mark it, you do
  not know it. A page number that looks plausible and is wrong sends a reader to
  the wrong page while everyone else is chanting.
- If a chant has no `[p.…]` marker at all, leave `page_start` out entirely and
  raise a check saying the page is unmarked. Do not guess from the chant before
  it, and do not carry a number forward from a previous batch.

Page numbers are digits as the book prints them. If my book numbers a page in
Thai numerals (๔๗) reproduce what I pasted and raise a check rather than
converting it.

## Ground rules — the important ones

- Work ONLY from the text I paste. Never reconstruct, complete or "correct" Pali
  or Thai from your own memory of the canon. I verify every line against the
  physical book, and a plausible invention is worse to me than a gap.
- Batching changes nothing about this. Do not let a long batch tempt you into
  filling a gap to keep a rhythm going.
- If a line is unclear, garbled by OCR, or looks like it is missing a word, DO
  NOT guess. Reproduce what I gave you and raise a check.
- Reproduce layers 1 and 3 exactly as I paste them, character for character,
  including ฯ and any unusual spacing.
- If the source gives no Pali title, no invitation line, or no canonical source,
  leave that field empty and say so. Never fill a gap to look complete.
- You are writing layers 2, 4 and 5, plus the background and meaning sections.

## Register — keep it, don't modernise it

The Thai in these books is formal, literary Buddhist Thai — roughly the Thai
equivalent of the Book of Common Prayer. Mostly standard Central Thai grammar,
but with scriptural vocabulary (บุคคล not คน), Pali loanwords (ขันธ์, ตัณหา,
นิพพาน), and older constructions (เบื้องบนแต่พื้นเท้าขึ้นมา rather than
ตั้งแต่ฝ่าเท้าขึ้นมา). It is NOT royal language (ราชาศัพท์) and not a special
monk language.

Never simplify or modernise the Thai. Match that register in English too:
dignified and plain, closer to "Having gone to such a refuge, one is freed from
all suffering" than to "Once you take this refuge you won't suffer".

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

Watch the vowels and finals as carefully as the consonants: ของ is kɔ̌ɔŋ (long
ɔɔ, final ŋ). Writing it "khǎaw" would be a different word entirely.

Vowels use ɛ ɔ ə ʉ (แ, อ, เออ, อึ). Tones: mid unmarked, low à, falling â, high
á, rising ǎ. EVERY syllable carries its tone. Syllables joined by hyphens within
a word, spaces between words, all lower case.

## Working notes — one set per chant, inside that chant

Each entry carries its own `working_notes`. Keep each note to a sentence or two:

1. **invitation** — present or absent. If absent, say so explicitly and say you
   have not written one.
2. **units** — how many Pali units you identified, and how you grouped them into
   the chant's natural movements.
3. **ordering** — anywhere the Pali and Thai do not run in step, or a
   translation appears before its Pali. Say you have kept my text as pasted and
   only noted the mismatch.
4. **conventions** — if anything I pasted uses a different romanisation from the
   Paiboon+ table above (RTGS spellings such as `sangkhaan`, `phrɔ́`, `thîang`),
   say so and confirm you have used the table, not my sample. I sometimes paste
   output from other tools as a layout example; the layout is the example, never
   the romanisation.

## Reproduce oddities, don't tidy them

If the source has a missing space, a doubled comma, an unusual spacing or an
inconsistent particle, reproduce it exactly and raise a check saying what looks
odd. Silent tidying is the failure this whole prompt exists to prevent.

## Where the checks go

Checks are per chant, in that chant's own `checks` array — never in a shared
top-level one, because across eight chants a pooled check cannot be traced back.
Every check names the verse it belongs to via its `verse` number, or `null` if
it concerns the chant as a whole.

Raise a check for: anything OCR-garbled or possibly mistyped, a spelling that
differs from standard editions, Pali and Thai running out of step, a missing
invitation or title, an inferred line break, an attributed source, a chant that
resembles an earlier one without matching it, and any typographic oddity you
reproduced rather than tidied.

Raise one for page numbers too: a chant with no `[p.…]` marker at all, a page
number that runs backwards or skips several at once, a marker landing
mid-sentence, or a page written in Thai numerals. A wrong page number is one of
the few errors in this book that a reader meets in public, mid-chant.

## Ids

Propose the `id` yourself: the Pali title slugged — lower case, hyphens, no
diacritics (`ariyadhana-gatha`, `mettanisamsa-sutta`). Where the book gives no
Pali title, slug the English. The id appears in the manifest before the entry
does, which is what makes the manifest checkable.

## Output format — one JSON object

Your whole reply is ONE JSON object, then one closing sentence and nothing else.
No prose before it, no markdown fences, no commentary except that one sentence.
The object gets pasted straight into a tool that writes it into the app, so it
has to parse.

Two formatting rules that matter more than they look:

- **Every value on ONE line.** Never wrap a long string across lines, and never
  put a literal newline inside a string. Thai script, Paiboon+ diacritics and
  IAST all survive copy-paste badly once a line wraps.
- **Manifest first, entries second, status last.**

{
  "batch": {
    "depth": "<FULL | COMPACT | DATA-ONLY>",
    "received": <how many chants I pasted>,
    "manifest": ["<id of chant 1>", "<id of chant 2>", "<...every one I pasted>"]
  },
  "chants": [
    {
      "id": "<slug>",
      "working_notes": {
        "invitation": "<present, or absent and therefore not written>",
        "units": "<how many Pali units, and how you grouped them>",
        "ordering": "<any place the Pali and Thai do not run in step, or none>",
        "conventions": "<any romanisation conflict in what I pasted, or none>"
      },
      "title_thai": "<the chant's title in Thai script>",
      "title_pali": "<the title in IAST, or \"\" if the book gives none>",
      "title_roman": "<the THAI title romanised so a non-Thai reader can find the chant in a printed book. Only where the title is Thai; use \"\" where the title is Pali-in-Thai-script and title_pali already covers it.>",
      "title_english": "<the traditional English title>",
      "page_start": <the page number this chant BEGINS on, as a bare number. Omit the key entirely if I did not mark one — never infer it.>,
      "source": "<canonical source. If compiled from several places, start with \"Composite.\" and say which verses come from where. Use \"\" if you are not certain — do not guess. Omit at DATA-ONLY.>",
      "when_chanted": "<one sentence on when it is recited. Omit at DATA-ONLY.>",
      "summary": "<one sentence, max 30 words, for the index card. Omit at DATA-ONLY.>",
      "english_unverified": <true if the book prints this chant in Pali only, with no Thai translation, so the English is a working translation made for this edition; otherwise omit the key>,
      "background": ["<paragraph>", "<paragraph>"],
      "meaning": ["<paragraph>", "<paragraph>", "<paragraph>"],
      "invitation": {
        "pali": "<Thai script, or \"\">",
        "pali_roman": "<IAST, or \"\">",
        "thai": "<the Thai translation of the invitation, or \"\">",
        "paiboon": "<Paiboon+ of that thai line, or \"\">",
        "english": "<meaning, or \"\">"
      },
      "verses": [
        {
          "number": 1,
          "page": <the page number, ONLY on the first verse of a new printed page; omit the key otherwise. Never inferred.>,
          "section": "<สังขาร: The Three Characteristics — only on the FIRST verse of a section; omit the key otherwise>",
          "pali": "<ONE Pali line, Thai script>",
          "pali_roman": "<the same line, IAST>",
          "thai": "<its Thai translation>",
          "paiboon": "<Paiboon+ of the thai line only>",
          "english": "<its meaning. Present at EVERY depth — never omitted.>"
        }
      ],
      "checks": [
        {"verse": 6, "issue": "<what looks wrong and what to compare it against>"},
        {"verse": null, "issue": "<a check about the chant as a whole>"}
      ]
    }
  ],
  "batch_status": {
    "completed": ["<ids you finished in full>"],
    "not_started": ["<ids from the manifest you did not begin>"],
    "resume_from": "<the id I should re-paste from next, or \"\" if you finished them all>",
    "paiboon_scan": "<count of kh/th/ph/ng hits found in your own paiboon values, and that you fixed them — or 'clean'>",
    "pali_untouched": "<confirm no pali value was romanised with Paiboon+>",
    "notes": "<anything else: a depth switch mid-batch, a repeat you skipped, a chant that ran much longer than the rest>"
  }
}

`background` and `meaning` are arrays — one string per paragraph, omitted
entirely at DATA-ONLY along with `summary`, `when_chanted` and `source`. The
verses are never reduced: all five layers, every depth. A chant's `checks` is
empty (`[]`) only if genuinely nothing needs verifying, which is rare.

## Sections — name them the way the book thinks

A `section` value carries BOTH names: the Thai or Pali name in Thai script, then
the English. So:

  "section": "สังขาร: The Three Characteristics"
  "section": "มะระณัสสะติ: The Recollection of Death"
  "section": "กายะคะตาสะติ: Reflection on the Body"

Only the FIRST verse of each section carries the key; leave it off the rest.

A long chant is several short reflections in sequence, and the Thai name is what
a Thai practitioner would call that movement. If the book prints section
headings, use those. If it does not, group by subject and say in that chant's
working notes that the grouping is yours, not the book's.

## Romanised Pali follows the Thai script beside it

`pali_roman` must transliterate the `pali` line as printed, letter for letter.
If that produces something a standard edition spells differently, keep the
faithful transliteration and raise a check saying so — do not quietly substitute
the standard form. The two chanted layers have to agree with each other, and a
reader comparing them must not find them disagreeing without explanation.

## The closing sentence

After the JSON, add nothing except one plain sentence giving the two numbers I
need to decide what to do next — how many chants came back complete, and how
many things need my eye:

  "Six of the eight are complete; twenty-one things need your eye against the
  physical book; resume from pabbatopama-gatha."

Confirm you understand, then wait. I will paste the first batch.
```

---

## Stage 2 — Claude Code

Paste the whole Stage 1 reply underneath this.

```
Add a BATCH of chants to the Digital Chanting Book in ~/thaibridge-ai.

The data lives in chanting.py, in the CHANTS list. Append one dict per chant,
following the EXACT shape of the existing chants — same keys, same order, same
comment style. Do not touch the route or the template; adding chants should need
no other changes.

I'm pasting a JSON object from stage 1. It holds `batch` (a manifest), `chants`
(an array of entries) and `batch_status`. The trailing sentence after the
closing brace is a note to me; ignore it.

## Reconcile the manifest BEFORE you write anything

This is the first thing you do, and nothing else happens until it passes.

1. Count the ids in `batch.manifest`. Count the entries in `chants`.
2. If they do not match, DO NOT WRITE ANY OF THEM. Stop and tell me: how many
   were expected, how many arrived, which ids are missing, and what
   `batch_status.resume_from` says. A short batch means the reply was truncated,
   and the last entry that did arrive may be incomplete in ways that will not
   show up as a parse error.
3. If they match, check `batch_status.completed` lists every manifest id too.
   Report any disagreement between the three before continuing.
4. Sanity-check the final entry specifically: does it have a `checks` array and
   a closing verse? A truncation that happens to land on valid JSON shows up
   here.

Say "manifest reconciled: N of N" and then proceed.

## Ids and repeats — this book has 286 chants and they overlap

- Stage 1 proposes an `id`. Check every one against the ids already in CHANTS.
- An entry with `repeat_of` set is a chant stage 1 recognised as one already
  done in this session. Do not add it. List it in your report so I can confirm.
- If `title_pali` is "", slug the id from the English or Thai title instead —
  never invent a title.

## When a chant is ALREADY in the file — merge, never replace

Seventeen chants were set before this workflow existed. As I work down the book
I will reach their pages and paste them again like any other. That is
deliberate: it is how they get their page numbers, and it is the only chance to
check them against the book a second time. It must NOT produce a duplicate.

So when an id already exists in CHANTS:

1. Do NOT append a second dict, and do NOT suffix the id with a number.
2. ADD only what is genuinely missing — normally `page_start` and the per-verse
   `page` keys, sometimes a field that did not exist when the chant was set.
3. KEEP THE EXISTING CHANT'S TEXT. Every `pali`, `pali_roman`, `thai`,
   `paiboon`, `english`, title, section and invitation already in the file stays
   exactly as it is. The file wins. My pasted text does not overwrite it.
4. COMPARE the two anyway, character for character, and REPORT every difference
   you find — which verse, what the file says, what my paste says. Show both.
   Change nothing on the strength of it.
5. If a difference is more than whitespace, also leave a comment above that
   verse so it is findable later:

       # ⚠️ PASTE DIFFERS: file kept. Re-paste on <date> read: <what mine said>

Report merges separately from additions. A line saying "3 added, 2 merged" is
the one I read first, because a merge silently becoming an append is how this
book ends up with the same chant twice.

The only thing that overrides rule 3 is me saying so explicitly, chant by chant.
"Use the new text for verse 4" is an instruction; my paste differing from the
file is not.

## Page numbers

- `page_start` goes on the chant dict, near the title fields, as a bare integer.
- `page` goes on a verse ONLY where stage 1 put one — the first verse of each
  new printed page. Do not add it to every verse, and do not fill in the gaps.
- If stage 1 omitted a page number, leave it omitted. Never infer one from the
  chant before or after it. The template guards both with `{% if %}`, so a chant
  without page numbers renders exactly as it does today.

## Mapping

Keys map straight across: title_thai, title_pali, title_roman, title_english,
page_start, source, when_chanted, summary, english_unverified, background,
meaning, invitation, verses. Each verse keeps its 'number', its 'page' where it
has one, and its 'section' where it has one. Set 'group': 'General chanting'
unless I say otherwise.

Two keys do NOT go in as data:
  working_notes  → ignore. It is Josh's reading aid.
  checks         → turn each entry into a ⚠️ code comment. A check with a
                   "verse" number goes directly above that verse; a check with
                   "verse": null goes at the top of that chant's dict. NEVER
                   drop one silently — they are what Josh still has to verify
                   against the physical book. Report the count PER CHANT, not as
                   a batch total; a total hides a chant whose checks all
                   vanished.

## Depth — a DATA-ONLY batch is deliberately incomplete

Read `batch.depth`.

- FULL / COMPACT — every field should be present. If one is missing, say so
  rather than writing the chant without it.
- DATA-ONLY — background, meaning, summary, when_chanted and source are absent
  ON PURPOSE. Do NOT write them yourself, do not leave a placeholder, and do not
  flag them as errors. Write the chant without them and put one comment at the
  top of the dict:

      # ⚠️ COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary,
      # when_chanted and source still to be written. Verses are complete.

  The template guards each of those with `{% if %}`, so the chant renders fine
  without them — every verse still shows all five layers, and only the chant's
  context is missing. Grep for COMMENTARY PENDING to find them all later.

At EVERY depth, every verse must carry all five layers — pali, pali_roman, thai,
paiboon and english. A verse missing its english is a fault at any depth, not a
depth setting. Stop and tell me rather than writing it.

## Structure rules

- ONE Pali line per verse, exactly as the JSON gives them. Never merge verses
  and never split one. Short verses stay short — a chant is read straight down
  the page, one line chanted then understood.
- 'section' marks where a new titled movement begins. Only the first verse of a
  section carries it; the template renders it as a heading above that verse.
- Empty strings are meaningful, not missing data. If every field of 'invitation'
  is "", keep the dict with its empty fields; the template checks it and skips
  it. If 'source' is "", leave it "". Do not fill any of them in to look
  complete.
- If you attribute a source yourself, mark it with a ⚠️ UNVERIFIED comment.

## Fidelity rules — these matter more than tidiness

- Copy every Pali, Thai, Paiboon and English string across CHARACTER FOR
  CHARACTER. Do not fix, tidy, re-space or "improve" any of it. If something
  looks wrong, add it unchanged and tell me afterwards.
- Do NOT convert the Paiboon into another romanisation. This app uses Paiboon+:
  ŋ never "ng", and k/t/p never "kh"/"th"/"ph".
- Watch the encoding: Thai script plus IAST diacritics plus Paiboon+ characters
  (ɛ ɔ ə ʉ ŋ). Nothing should end up as ? or mojibake.

## Then verify before telling me it's done

Run these with PYTHONIOENCODING=utf-8 set, or Thai output will crash on Windows.

1. `python -c "import chanting"` — it must import cleanly.
2. Confirm len(CHANTS) grew by exactly the number of NEW chants — not the number
   of entries in the batch. A merge must not change the count. If the count
   moved by more than that, a merge became an append and there is now a
   duplicate: stop and tell me.
3. Confirm every id is unique. Two dicts with the same id is the failure this
   whole merge rule exists to prevent, so check it explicitly rather than
   assuming.
4. For EACH chant, compare the Thai and Pali you wrote against my pasted block
   and report character counts both ways. Per chant, not summed — a batch total
   can balance while two chants are individually wrong.
5. For each MERGED chant, prove the existing text is untouched: dump its verses,
   titles and invitation before and after, and report the diff as empty. The
   only permitted change is keys being added.
6. Re-scan the written file for "kh", "th", "ph" and "ng" inside paiboon values
   only, and report the count. Stage 1 checks itself; this checks stage 1.
7. Check the page numbers read sensibly: within a chant they must not go
   backwards, and `page_start` must match the first `page` if the chant has one.
   Report anything odd rather than adjusting it.
8. Render the page and confirm each new chant shows the right verse count, its
   section headings, its page markers and its layers, and that existing chants
   are unchanged.

Report TWO tables. Added chants: id, page_start, verses in, verses written,
checks carried, char match y/n. Merged chants: id, what you added, how many
differences you found, and whether the existing text was left intact. I read the
tables, not the prose.

Do not commit. I'll review the batch first.

Here is the batch:

[paste the whole stage 1 reply here — the JSON object and its closing sentence]
```

---

## Stage 3 — Claude Code, the commentary pass

Run this after a `DATA-ONLY` run, once the verses are in and verified. It needs
nothing pasted: the chants are already in `chanting.py`, so it reads them from
there. Give it a number of chants to do, or it will pick a sensible few.

```
Write the missing commentary for chants in the Digital Chanting Book in
~/thaibridge-ai.

Some chants were set at DATA-ONLY depth: their verses are complete and verified,
but the chant-level prose was deferred. They are marked with a comment reading
"⚠️ COMMENTARY PENDING" at the top of the dict. Your job is to fill in what that
comment lists, and nothing else.

Do the first N you find, N being the number I gave you — or 5 if I gave none.
Work through them in file order so we can go straight down the book.

## The one rule that outranks everything else here

DO NOT TOUCH A SINGLE CHARACTER OF ANY VERSE.

`pali`, `pali_roman`, `thai`, `paiboon` and `english`, the titles, the
invitation, the sections, the verse numbers, `page_start`, the per-verse `page`
keys and the existing ⚠️ check comments have all been verified against a
physical book already. They are finished work. You are adding keys to a dict,
not editing one.

The page numbers deserve a line of their own: they are the only field a reader
meets in public, mid-chant, with a monk calling out a page. A page number you
"corrected" is worse than one left alone, whatever it looks like from here.

This is not a style preference. Verified Pali that quietly changes is the single
worst outcome this whole workflow is built to prevent, and it would not look
wrong afterwards. If you think a verse is mistaken, say so in your report and
leave it exactly as it is.

## What to write

For each chant, add these five keys, in this position and this order — matching
the existing chants in the file, which are the shape to copy:

  summary       — ONE sentence, max 30 words, for the closed index card. What
                  this chant is, plainly, to someone who has not met it.
  when_chanted  — ONE sentence on when it is recited in Theravāda practice.
  source        — the canonical source. Read the rules below before writing it.
  background    — a LIST of paragraphs. Why was it taught? The historical
                  setting, or the origin of the chant if composed later.
  meaning       — a LIST of paragraphs. What does it mean, and why is it still
                  chanted?

`background` and `meaning` are lists of strings, one per paragraph, never one
long string — the page and a printed edition space them from that structure.
Two or three paragraphs each is right. Do not pad them to look thorough.

## Where your material comes from

Work from the chant that is in front of you in the file. It has the Pali, the
Thai and the English of every verse, which is what the commentary is about.

You may use general knowledge of Theravāda practice and of the Pali canon for
context — that is what `background` is for, and it is why this pass is a writing
job rather than a transcription one. But there is a hard line:

- NEVER quote, reconstruct or "restore" any Pali or Thai that is not already in
  the file. Not a line, not a phrase, not a word. If a point would need a verse
  the chant does not contain, make the point without it or leave it out.
- NEVER contradict the chant in front of you because a standard edition differs.
  The file follows Josh's physical book. Where they disagree, the book wins, and
  you say so in your report rather than editing anything.

## `source` — the field most likely to go wrong

Attributing a canonical source is exactly where a confident invention slips
through, because a plausible reference looks identical to a real one.

- If you are certain, write it (`Dhammapada 188–192`, `Khuddakapāṭha 5`).
- If it is assembled from several places, start with `Composite.` and say which
  parts come from where.
- If you are NOT certain, write `""`. An empty source is honest and the template
  simply omits it. A wrong one is a false citation in a book about the Dhamma.
- Any source YOU attribute, rather than one already in the file, gets a comment
  directly above it:

      # ⚠️ UNVERIFIED SOURCE: attributed by Claude, not taken from Josh's book.

  Never write that comment above a source that was already there.

## Register — this is the part that has to match

The app's existing chants set the register, so read two or three finished ones
before you write anything. Dignified and plain. Closer to "Having gone to such a
refuge, one is freed from all suffering" than "Once you take this refuge you
won't suffer". No devotional inflation, no self-help framing, no exclamation
marks, and no addressing the reader as "you".

Write for someone intelligent who does not know Buddhism. Explain a Pali term
the first time it appears in that chant's prose, then use it.

## When you are done with each chant

Replace the whole COMMENTARY PENDING comment — do not leave it sitting above a
chant that now has its commentary. That marker is how Josh finds the remaining
work, so a stale one is worse than none.

If you could only do part of a chant — say the source is genuinely unknowable —
leave a narrowed marker instead of removing it:

    # ⚠️ COMMENTARY PENDING: source only. Could not attribute with confidence.

## Then verify before telling me it's done

Run with PYTHONIOENCODING=utf-8 set, or Thai output will crash on Windows.

1. `python -c "import chanting"` — it must import cleanly.
2. PROVE the verses are untouched. Before you edit, dump every verse of every
   chant to a file; after you edit, dump them again and diff the two. Report the
   diff as empty. Do the same for the titles and the invitation. If ANYTHING
   shows up in that diff, stop and show me — do not tidy it away.
3. Confirm len(CHANTS) is unchanged and every id is unchanged.
4. Confirm background and meaning are lists of strings for every chant you
   touched, not bare strings.
5. Count COMMENTARY PENDING markers before and after, and report both numbers.
   The drop should equal the number of chants you completed.
6. Render the page and confirm each chant now shows its context sections, and
   that the chants you did NOT touch look exactly as they did.

Report as a table: id, paragraphs written for background, paragraphs for
meaning, source written or left empty, marker cleared y/n.

Then tell me, separately from the table, anything you noticed but did not act
on — a verse that looks wrong, a chant whose source you could not place, a
duplicate of one earlier in the file.

Do not commit. I'll read the prose before it goes in.
```
