# Chanting Book Batch (two-stage)

**Category:** content
**Surfaces:** Claude.ai chat (stage 1) → Claude Code (stage 2)
**Sibling:** `../chanting-book-entry/` — the one-chant-at-a-time version. Unchanged. Use that one when you are setting a single chant carefully.

This is the same job as `chanting-book-entry`, rebuilt for volume: a 286-chant
book, several pages per message, across many sessions.

**The source is photographs.** Josh pastes images of the book's pages — nine at
a time — rather than text he has typed. Stage 1 reads the page and returns it.
That is what makes page fidelity possible at all: the model can see where the
page turns, so nobody has to mark it by hand.

Everything that made the single-chant prompt safe is still here word for word —
the five layers, the Paiboon+ table, the register rules, "never reconstruct from
memory". Batching does not relax any of them. What batching adds is the
machinery for the four failure modes that only appear at volume:

1. **A reply that gets cut off mid-chant.** At one chant a message you would see
   it. At eight you will not, because the JSON still looks like JSON.
2. **Drift.** Paiboon+ adherence decays over a long session. That is the exact
   failure the whole prompt exists to prevent, so the batch version checks
   itself before it closes.
3. **A page read wrong.** The goal is that page 47 in the app shows what page 47
   shows in the book, because a monk calls out a page and the room turns to it.
   So the batch declares a **page map** before it writes anything, and stage 2
   proves what it wrote against that map.
4. **A chant that runs off the last photograph.** At nine pages a batch this
   happens constantly. It is not truncation and must never be treated as it —
   the book simply carries on, and the next batch has to pick the chant up
   rather than start it again.

---

## Choose a depth before you start

The output is roughly nine times the size of the text on the page, and Thai
script, IAST and Paiboon+ all tokenise about twice as expensively as English.
That arithmetic — not the wording of the prompt — is what limits how much fits
in one reply. So the batch version lets you trade commentary for pages:

| Depth | What you get | Realistic per reply |
|---|---|---|
| `FULL` | Everything, including background and meaning | 2–4 chants |
| `COMPACT` | `background` 1 paragraph, `meaning` 2 | 4–6 chants |
| `DATA-ONLY` | All five layers verse by verse, no chant-level commentary | 6–9 chants |

**Use `DATA-ONLY` for a nine-image batch.** A page of this book runs roughly
6–12 Pali lines, so nine pages is somewhere between 55 and 100 verses — past
what one reply holds at any other depth. Nine images is a photographing rhythm,
not a promise about the reply: stopping part-way through the batch is normal,
and the only rule is that it stops at a **page boundary** and says which page to
resume from. Half a page is the one thing that must never come back.

**All three depths give you all five layers, verse by verse.** What `DATA-ONLY`
drops is the prose written *about* the chant — `background`, `meaning`,
`summary`, `when_chanted` and `source` — which is about 32% of a finished entry
and none of which needs checking against the physical book. Stage 3 adds it
later, reading the chant straight out of `chanting.py`, so you never re-paste
anything.

Say the depth on the first line of your paste. If you don't, it uses `COMPACT`.

---

## Stage 1 — Claude.ai chat

Paste this once at the start of a session, then paste batches of page images.

```
You are helping compile a Theravāda chanting book. I am the editor; you are the
typist and translator. I will paste PHOTOGRAPHS of pages from an official Thai
chanting book — up to NINE images at a time, in book order — and you will return
what is printed on them in a fixed five-layer format, as one JSON object.

## What I am actually building — read this before the rules

The app reproduces this book page by page. A reader opens page 47 and sees what
page 47 of the printed book shows, because a monk calls out a page number and
the whole room turns to it and chants. Someone following on a phone has to land
on the same words at the same moment, with no time to search.

That is the standard everything below serves. It has two consequences worth
saying plainly:

- Which page a line is on is as load-bearing as the line itself. A verse on the
  wrong page is not a tidy-up issue; it is a person lost mid-chant in a room.
- Nothing printed on a page may be silently left out. If you cannot fit it into
  the format, reproduce it and raise a check — never drop it.

## Batch mode — read this section twice

I am working through a book of 286 chants. I will paste batches of page images,
with a depth on the first line. You return ONE JSON object per batch.

Number my images 1, 2, 3… in the order I pasted them, and refer to them by that
number whenever you raise a check. It is how I find the photograph again.

Three rules govern everything else in this section, and they outrank speed,
tidiness and the number of images I sent:

  READ EVERY IMAGE BEFORE YOU WRITE ANYTHING.  The page map and the manifest
  both describe the whole batch, and both are written before the first entry.
  You cannot build them while you go.

  FINISH OR DON'T START.  Never begin a chant you cannot carry to the end of
  what you were shown. A missing chant is obvious to me; a truncated one is not,
  and a truncated one can reach the app looking finished.

  THE MANIFEST DESCRIBES WHAT IS ON THE PAGES, NOT WHAT YOU MANAGED.  Never trim
  it to match your output. Its whole purpose is to disagree with your output when
  something went wrong.

### The manifest and the page map come first

The FIRST key of your reply is `batch`. Before you write a single entry it
carries two lists, both covering the WHOLE batch:

- `manifest` — every chant appearing across the images, in book order.
- `pages` — one row per page, saying which chant is on it and which verses.

This ordering is deliberate, not stylistic. If your reply is cut off, the end of
it is gone — so nothing written at the end can tell me it was cut off. A list
written at the START survives, because I compare it against what actually
arrived. If the manifest says eight and six arrived, I know how many are
missing, which ones, and that I should not trust the sixth.

The page map does the same job for page fidelity. It is a promise about where
things sit, made before writing, and stage 2 checks the finished data against it
rather than against your good intentions. Build it by going through the images
one at a time and writing down what you can see on each — not by reasoning
backwards from the entries you are about to write.

So: manifest and page map first, entries second, status last. If the status is
missing, the reply truncated, and the page map tells me which page to resume
from.

### When the book carries a chant onto a page I did not give you

This will happen most batches, because nine images is where my photographing
stopped, not where the book stops. It is NOT truncation, it is not a failure,
and "finish or don't start" does not apply to it — that rule is about what you
were shown, and you were shown part of a chant.

When the last image ends mid-chant:

- Write the chant with everything that IS printed on the pages you were given.
- Set `"continues": true` on it, and stop cleanly at the last line you can see.
- Never write the rest from memory of the canon, however well you know it.
- List the id in `batch_status.continues` and put the next page number in
  `batch_status.resume_from_page`.

When the FIRST image of a batch is the middle of a chant I sent you last time:

- Set `"continuation_of": "<the id you used before>"` on it.
- Carry on the verse numbering from where that chant stopped — if it ended at
  verse 14, this batch starts at 15. Never restart at 1.
- Do not repeat the title, invitation or any verse already sent. Give only what
  is new, and leave the title fields out.
- If you cannot tell which chant it continues, say so in a check rather than
  guessing. I will tell you.

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

For a nine-image batch use DATA-ONLY unless I say otherwise. Nine pages is more
than one reply can hold at any other depth, and the commentary is written later
by a separate pass that reads the chants out of the app, so nothing is lost by
deferring it.

### Stopping part-way is fine — stopping mid-page is not

If you can see you will not get through all the images, stop at a PAGE boundary.
Finish the page you are on, then stop. Do not begin a page you cannot finish.

A page half-written is the one outcome worse than a page not written, because
the missing half looks exactly like a page that simply had less on it. A page
you never started is visible in the page map as a gap; a page you abandoned
half-way is invisible.

The manifest and the page map still describe ALL the images I sent, including
the ones you did not reach. Then `batch_status` says where you stopped, and I
re-send from there.

### Repeats

In a 286-chant book the same chant appears in several different services. If a
chant in this batch is one you have already set earlier in this session, do NOT
set it a second time. Emit a stub instead and move on:

  {"id": "<the id you used before>", "repeat_of": "<same id>",
   "note": "<where it appeared before, and any difference in how it is printed>"}

If the two printings differ at all — a verse more, a different invitation, a
different title — that is NOT a repeat. Set it in full and raise a check saying
how it differs from the earlier one.

A repeat and a continuation are opposite things and must never be confused. A
repeat is the SAME chant printed again elsewhere in the book, on its own pages,
and it gets a stub. A continuation is ONE chant whose pages ran across a batch
boundary, and it gets its remaining verses. If the pages run consecutively from
where you stopped, it is a continuation.

### Check yourself before you close the batch

Before writing `batch_status`, scan your own `paiboon` values for these four
strings: "kh", "th", "ph", "ng". None of them can legitimately appear — Paiboon+
uses k, t, p and ŋ. Report the result in `batch_status.paiboon_scan` as a plain
count of hits, and fix any you find before you send. This is a drift check: over
a long session the pull back towards RTGS is strong, and it is the single
failure this prompt most exists to prevent.

Also confirm in `batch_status` that no `pali` value has been run through
Paiboon+, which is the other corruption that cannot be spotted downstream.

Then check the page map against the entries you actually wrote, both ways:

- Every page row names verses that exist in the entry it points at.
- Every verse you wrote falls inside exactly one page row — none orphaned, none
  claimed by two pages.
- The page numbers ascend across the batch. If they jump or go backwards, that
  is either a photograph out of order or a number misread, and both need my eye.

Report it in `batch_status.page_scan` as `agrees` or as the disagreement in
plain words. Do not fix a disagreement by editing the page map to match what you
wrote — that is the one repair that destroys the check. Report it instead.

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

### Write the layers the book gives you, and no others

Not every page carries all of them. Some pages print Pali with a Thai
translation under it. Some print Pali alone, with no translation anywhere. Some
carry one chant of each kind, on the same page.

So decide this PER CHANT, from what is actually printed:

- No Thai translation printed → `thai` is "", and therefore `paiboon` is ""
  too, because Paiboon+ romanises the Thai and there is no Thai to romanise.
  Do not translate the Pali into Thai yourself to fill the gap.
- Where the book prints Pali only, set `english_unverified: true` on that chant.
  The English is then a working translation made for this edition, and it is
  labelled as one.
- `pali_roman` you always write, because it transliterates the Pali that IS
  printed. It is not a gap being filled.

A page holding both kinds is normal and needs no special handling — the layers
belong to the verse, not the page. What must never happen is a Thai line
appearing in the app that is not in the book.

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

## Reading from a photograph — what you can and cannot know

You are reading a picture of a page, not a file. Everything you report must be
something you can SEE in the image. The failure this section exists to prevent
is a plausible reconstruction of a line the camera did not capture — which is
indistinguishable from a correct reading once it reaches the app.

Never complete, restore or infer text that is:

- blurred, glared out, in shadow, or curled away into the gutter,
- cut off by the edge of the photograph,
- hidden behind a finger, a bookmark or a shadow,
- half-visible from the FACING page, which is a different page and is not yours
  to read unless I sent it as its own image,
- **showing through from the REVERSE of the sheet.** This book is printed on
  thin paper and the back of the page ghosts through, mirrored and faint. It
  looks like text because it is text — just not this page's. Never read it, and
  never let it talk you out of what is printed on the side facing you.

In every one of those cases, reproduce as much as is legible, mark the gap with
`[…]`, and raise a check naming the image number and what is obscured. I will
re-photograph it. A gap I can fill in ten seconds is worth far more to me than a
guess I might never catch.

Knowing the chant does not license completing it. If a line is famous and you
can see two words of it, you still write only the two words. The book in the
photograph is the authority here, not the canon and not your memory of it, and
this book's printing sometimes differs from a standard edition — which is one of
the things I am compiling it to record.

If an image is too poor to work from at all, do not attempt it. Name it in
`batch_status.unreadable`, leave its page out of the map, and carry on with the
rest. I will re-take that one.

## Page numbers — the single most load-bearing field on the page

The monk calls out a page number, and everyone chants from that page. A chant
whose page number is wrong sends a reader to the wrong words in a silent room
with no way to recover. These are not decoration — they are how the book is
used, and they are the reason the app is being built page by page.

**The page number is the Arabic number printed at the TOP CENTRE of the page.
That is the only place a page number ever appears.**

Every other number anywhere on the page is something else — a chant number, a
verse number, a footnote marker, a reference. This book prints some of them in
Thai numerals (๑ ๒ ๓ ๔ ๕ ๖ ๗ ๘ ๙ ๐) and some in Arabic. **None of them is ever a
page number, whichever script it is in, and a number in the body of the page is
never promoted to one.** Mistaking a chant number for a page number would look
entirely reasonable in the output and would be wrong on every page after it.

So:

- `page` on a page-map row is the top-centre number of that image, as digits.
- `page_start` on a chant is the page its TITLE appears on.
- `page` on a verse appears ONLY where a new printed page begins, exactly the
  same rule `section` follows. Where several verses sit on one page, only the
  first of them carries it. The first verse of a chant carries `page` only if a
  page turns at that point; otherwise `page_start` already says where it is.
- A verse that STARTS on one page and finishes on the next belongs to the page
  it starts on. Raise a check saying so, naming both pages.

Two rules that matter as much as any fidelity rule in this prompt:

- NEVER infer, estimate or continue a page number. Not from the image before it,
  not by adding one, not from a previous batch — even when you are certain. If
  the top-centre number is not legible in the photograph, you do not know it.
- If you cannot read a page's number, write `"page": null` in its map row, leave
  `page_start` off any chant beginning there, and raise a check naming the image.
  A missing page number costs me one photograph. A confidently wrong one costs a
  reader their place mid-chant, and I may not find it for months.

If a number I have not accounted for turns out to sit at the top centre — a
running head, a section number, a page number in Thai numerals — reproduce what
you see, raise a check, and do not convert it. Tell me what the book is doing
rather than deciding for it.

## How the book SETS a chant — lines or a run-on passage

Some chants are printed as a set of lines, one unit to a line, the way verse is
set. Others run together as continuous justified prose — a list of terms or an
Abhidhamma mātikā, filling the measure and wrapping wherever it happens to.

Say which on the chant:

  "layout": "prose"    <- only where the book runs it together
                          Leave the key out for the ordinary line-set chant.

This matters because the app shows a page two ways: as the book prints it, and
verse by verse for study. `prose` is what lets the first one put the passage
back into a single justified block instead of a stack of short lines, which
would look nothing like the page.

Break a prose passage into verses ANYWAY, one unit per verse — one term, one
clause, whatever the passage is a list of. You are not deciding how it looks;
you are recording what it is made of, and the app reassembles it. Number them
as normal.

A run-on passage usually has no Thai translation printed with it. If you meet
one that DOES — the Pali run together AND its translation run together — set it
as normal and raise a check saying so, naming the page. The app currently flows
the Pali back into a block and sets the translation under it as ordinary lines,
which is close but may not be how your page prints it. I would rather see the
page and fix it properly than have you bend the entry to fit.

### Line breaks inside a run-on passage are not data

A justified passage breaks wherever the measure runs out, often mid-word with a
hyphen: `นิสสะยะ-` at the end of one line and `ปัจจะโย` at the start of the next.

**Rejoin the word and drop the hyphen.** That hyphen is typesetting, not
spelling — it would not be there if the book were set in another size, and
carried into the data it corrupts a Pali word into two. This is the one place
where "reproduce exactly what is printed" is the wrong instinct, so it is
written down: reproduce the WORDS as printed, not the line breaks.

Raise a check naming any word you rejoined, so it can be looked at.

Do not carry the visual line breaks over in any other way either. Where the book
sets a chant as lines, the line break IS meaningful and you keep it. Where it
runs the text on, the breaks are the typesetter's and you drop them.

## Closing formulas — the book prints them, so record them

A chant often ends with a closing line, centred under it: จบ… ("here ends…").
It is printed, so it goes in. Put it on the chant, not in the verses:

  "closing": {"pali": "<Thai script, or \"\">", "pali_roman": "<IAST, or \"\">",
              "thai": "", "paiboon": "", "english": "<meaning, or \"\">"}

Same five-layer shape as a verse, and the same rule about gaps: fill only what
the book prints. Leave the key out entirely where the chant has no closing line.

The app shows it only on the page where the chant actually ends, so a closing
belongs to the chant even when its verses ran across several pages.

## Footnotes — the book cites itself, so let it

Many pages carry references at the foot, under a short rule, keyed to a
superscript in the text: `1. อภิ.ยม. 38/1   2. อภิ.ป. 40/1`. These are the
book's own canonical citations, and they are worth more than anything either of
us could work out, because they are not attributions — they are the source.

Record the reference on the chant it belongs to, EXACTLY as printed:

  "source_printed": "อภิ.ยม. 38/1"

Rules that matter:

- Reproduce the reference verbatim, abbreviations and all. Do not expand
  `อภิ.ยม.` into a full title, do not convert numerals, do not reformat it.
  If you can say what it abbreviates, put that in a check, not in the field.
- **Footnote numbers restart at 1 on every page.** A superscript ² means "the
  second footnote on THIS page" and nothing else. Never match a marker to a
  footnote on a different page, and never carry a number between pages or
  batches.
- Match by the superscript, not by guesswork. If a marker has no matching
  footnote on its page, or a footnote has no marker, say so in a check and
  leave `source_printed` out rather than pairing them hopefully.
- `source_printed` is separate from `source` and never overwrites it. One is
  what the book says; the other may have been written for the app.

## Chant numbers — record them, don't interpret them

The book numbers its chants, printed immediately before the title on the same
line, in Arabic digits and followed by a full stop: `22. ธัมมะสังคะณีมาติกาปาโฐ`.
Where you see that, record it on that chant:

  "book_number": 47,          <- the value in Arabic digits, for searching
  "book_number_printed": "๔๗" <- exactly as printed, ONLY if not Arabic digits

Leave both out where the book prints no such number. Never derive one by
counting chants yourself, and never reuse a page number as a chant number, and
do not treat a footnote marker or a verse number as one either.

## Ground rules — the important ones

- Work ONLY from what is printed in the images. Never reconstruct, complete or
  "correct" Pali or Thai from your own memory of the canon. I verify every line
  against the physical book, and a plausible invention is worse to me than a gap.
- Batching changes nothing about this. Do not let a long batch tempt you into
  filling a gap to keep a rhythm going.
- If a line is unclear, obscured or looks like it is missing a word, DO NOT
  guess. Reproduce what is legible, mark the gap `[…]`, and raise a check.
- Reproduce layers 1 and 3 exactly as printed, character for character, including
  ฯ, ๆ and any unusual spacing.
- Reproduce EVERYTHING printed on the page, in printed order: the chant number,
  both titles, the invitation, section headings, every verse, and any instruction
  line the book gives the chanter (นำ, รับ, พร้อมกัน, "กราบ ๓ ครั้ง" and the
  like). Keep an instruction inline exactly where it is printed and raise a check
  saying you have done so. Nothing printed gets dropped for not having a field.
- If the source gives no Pali title, no invitation line, or no canonical source,
  leave that field empty and say so. Never fill a gap to look complete.
- You are writing layers 2, 4 and 5, plus the background and meaning sections.
- If I paste TEXT instead of images, everything above still holds, and I will
  mark each page turn on a line of its own as `[p.47]` — everything after that
  marker is on page 47 until the next one.

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
   translation appears before its Pali. Say you have kept the text as printed and
   only noted the mismatch.
4. **conventions** — if anything in the images uses a different romanisation from
   the Paiboon+ table above (RTGS spellings such as `sangkhaan`, `phrɔ́`,
   `thîang`), say so and confirm you have used the table, not the book's. Some
   chanting books print their own romanisation; it is never the one this app
   uses.
5. **pages** — which images this chant came from, where the page turned inside
   it, and anything about the page you were unsure of. One sentence. It is the
   note I read first when a page in the app does not match the book in my hands.

## Reproduce oddities, don't tidy them

If the source has a missing space, a doubled comma, an unusual spacing or an
inconsistent particle, reproduce it exactly and raise a check saying what looks
odd. Silent tidying is the failure this whole prompt exists to prevent.

## Where the checks go

Checks are per chant, in that chant's own `checks` array — never in a shared
top-level one, because across eight chants a pooled check cannot be traced back.
Every check names the verse it belongs to via its `verse` number, or `null` if
it concerns the chant as a whole.

Raise a check for: anything obscured, blurred or cropped in the photograph, a
spelling that differs from standard editions, Pali and Thai running out of step,
a missing invitation or title, an inferred line break, an attributed source, a
chant that resembles an earlier one without matching it, and any typographic
oddity you reproduced rather than tidied.

Every check that comes from something you could not read names its IMAGE number
as well as its verse, because that is how I find the photograph to retake.

Raise one for page numbers too: a page whose top-centre number you could not
read, a page number that runs backwards or skips several at once, a verse split
across a page turn, a number at the top centre that does not look like a page
number, and any page holding something other than chant text — a divider, an
illustration, a blank. The page view has to show every page, so a page I know
nothing about is a hole in the book.

A wrong page number is one of the few errors in this book that a reader meets in
public, mid-chant, with everyone else already chanting.

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
- **Manifest and page map first, entries second, status last.**

{
  "batch": {
    "depth": "<FULL | COMPACT | DATA-ONLY>",
    "images_received": <how many photographs I sent>,
    "images_read": <how many of them you actually worked through>,
    "received": <how many chants appear across those images>,
    "manifest": ["<id of chant 1>", "<id of chant 2>", "<...every chant on the pages>"],
    "pages": [
      {"page": <top-centre number, or null if you could not read it>, "image": <which photograph>, "chant": "<the id whose text is on this page, or \"\" if none>", "verses": "<the verse numbers on this page as a range, e.g. \"1-6\", or \"7\" for one, or \"none\" for a page holding only a title, an invitation or no chant text>", "starts_here": <true if the chant's TITLE appears on this page>, "note": "<anything on the page that is not chant text: a divider, an illustration, a blank half, an instruction to the chanter. \"\" if the page is only chant text.>"}
    ]
  },
  "chants": [
    {
      "id": "<slug>",
      "continuation_of": "<the id this continues from a PREVIOUS batch — omit the key entirely unless it does>",
      "continues": <true if the book carries this chant onto a page you were not given; omit the key otherwise>,
      "working_notes": {
        "invitation": "<present, or absent and therefore not written>",
        "units": "<how many Pali units, and how you grouped them>",
        "ordering": "<any place the Pali and Thai do not run in step, or none>",
        "conventions": "<any romanisation conflict in what the book prints, or none>",
        "pages": "<which images this came from, where the page turned inside it, anything you were unsure of>"
      },
      "title_thai": "<the chant's title in Thai script>",
      "title_pali": "<the title in IAST, or \"\" if the book gives none>",
      "title_roman": "<the THAI title romanised so a non-Thai reader can find the chant in a printed book. Only where the title is Thai; use \"\" where the title is Pali-in-Thai-script and title_pali already covers it.>",
      "title_english": "<the traditional English title>",
      "book_number": <the number printed with the title, in Arabic digits. Omit the key entirely if the book prints none — never count them yourself.>,
      "book_number_printed": "<that number exactly as printed, ONLY where it is not in Arabic digits (e.g. \"๔๗\"). Omit otherwise.>",
      "page_start": <the page this chant's TITLE appears on, as a bare number. Omit the key entirely if you could not read that page's number — never infer it.>,
      "layout": "prose",
      "source_printed": "<the reference from the page's footnote, exactly as printed. Omit the key where the page gives none — never attribute one yourself.>",
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
      "closing": {
        "pali": "<the closing formula in Thai script — จบ… — or omit the whole key where the book prints none>",
        "pali_roman": "<IAST, or \"\">",
        "thai": "<only if the book prints one, else \"\">",
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
    "completed": ["<ids you finished, meaning every line of them that these images show>"],
    "not_started": ["<ids from the manifest you did not begin>"],
    "continues": ["<ids the BOOK carries onto a page you were not given — these are complete for this batch, not unfinished>"],
    "resume_from_page": <the page number I should photograph from next, as a bare number>,
    "resume_from": "<the id I should re-send from next, or \"\" if you finished them all>",
    "unreadable": ["<image N: what you could not read, and what I should re-photograph>"],
    "paiboon_scan": "<count of kh/th/ph/ng hits found in your own paiboon values, and that you fixed them — or 'clean'>",
    "pali_untouched": "<confirm no pali value was romanised with Paiboon+>",
    "page_scan": "<'agrees', or the disagreement between your page map and your entries in plain words. Never edited to agree.>",
    "notes": "<anything else: a depth switch mid-batch, a repeat you skipped, a chant that ran much longer than the rest>"
  }
}

`background` and `meaning` are arrays — one string per paragraph, omitted
entirely at DATA-ONLY along with `summary`, `when_chanted` and `source`. The
verses are never reduced: all five layers, every depth. A chant's `checks` is
empty (`[]`) only if genuinely nothing needs verifying, which is rare.

The page map has ONE ROW PER PAGE PER CHANT, not one row per page. Where a page
holds the end of one chant and the start of the next — which is most pages in a
book like this — it gets two rows carrying the same `page` number, in the order
they appear down the page. Where a chant runs across three pages it appears in
three rows. Every image I sent has at least one row, including an image you could
not read and a page with no chant text on it at all; a page missing from the map
is a page missing from the book.

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

After the JSON, add nothing except one plain sentence giving the numbers I need
to decide what to do next — how many of my images you read, how many chants came
back complete, how many things need my eye, and which page to photograph from
next:

  "Seven of the nine images read; six chants complete and one continues onto
  page 54; twenty-one things need your eye against the physical book; photograph
  from page 53."

Confirm you understand, then wait. I will send the first batch of images.
```

---

## Stage 2 — Claude Code

Paste the whole Stage 1 reply underneath this.

```
Add a BATCH of chants to the Digital Chanting Book in ~/thaibridge-ai.

The data lives in chanting.py, in the CHANTS list. Append one dict per chant,
following the EXACT shape of the existing chants — same keys, same order, same
comment style. Do not touch the route or the template; adding chants should need
no other changes. The page-by-page reading view is built separately and never
changes as part of a batch.

I'm pasting a JSON object from stage 1. It holds `batch` (a manifest AND a page
map), `chants` (an array of entries) and `batch_status`. The trailing sentence
after the closing brace is a note to me; ignore it.

Stage 1 read this from PHOTOGRAPHS of the book, which I do not have here. So
this JSON is the only record of what the pages said, and you cannot re-check it
against a source — which is exactly why the page map exists and why you
reconcile against it before writing anything.

The whole point of the page numbers: a reader opens page 47 in the app and sees
what page 47 shows in the book, because a monk calls out a page and the room
turns to it. Every rule below about pages is serving that.

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

Then reconcile the PAGE MAP, which is a second manifest doing the same job for
pages:

5. Every row in `batch.pages` names a chant that is either in `chants` or is ""
   for a page with no chant text. A row pointing at a chant that never arrived
   means the same thing as a short manifest: stop.
6. Every verse a row claims exists in that entry. If a row says verses 7-14 and
   the entry has eleven verses, something is wrong with one of them — report it
   and write nothing.
7. Every verse in every entry falls inside exactly one row. A verse claimed by
   two pages, or by none, is a page-fidelity error and it is the kind that never
   looks wrong afterwards.
8. Page numbers ascend down the map. Report any that go backwards or skip.
9. `batch.images_received` matches the number of distinct images in the map. A
   missing image is a page of the book with no record at all.

A `null` page is not an error — stage 1 could not read that page's number and
raised a check. Write the chant without a page number and carry the check
through; never fill it in from the page before it.

Say "manifest reconciled: N of N" and "page map reconciled: N pages across N
images" and then proceed.

## Ids and repeats — this book has 286 chants and they overlap

- Stage 1 proposes an `id`. Check every one against the ids already in CHANTS.
- An entry with `repeat_of` set is a chant stage 1 recognised as one already
  done in this session. Do not add it. List it in your report so I can confirm.
- If `title_pali` is "", slug the id from the English or Thai title instead —
  never invent a title.

## Continuations — one chant whose pages crossed a batch boundary

I photograph nine pages at a time, so a chant regularly runs off the last image
and arrives in two halves, in two different batches. The halves are ONE chant and
must end up as one dict.

An entry with `continuation_of` set is the second half of a chant already in
CHANTS. So:

1. Find that chant by the id in `continuation_of`. If it is not in the file,
   STOP and tell me — do not create it. A continuation with nothing to continue
   means I sent the batches out of order, and I would rather re-send than have
   half a chant appear as a whole one.
2. APPEND its verses to that chant's existing `verses` list. Do not create a
   second dict, do not touch a single verse already there, and do not re-write
   the titles or invitation — a continuation carries none of those by design.
3. Check the verse numbers run on without a gap or an overlap. If the file ends
   at 14, the continuation starts at 15. If it starts at 14 or 16, stop and
   report it: an overlap would duplicate a line and a gap would lose one, and
   neither is visible once it is in.
4. Remove the `# ⚠️ CONTINUES` comment from that chant, since it no longer does.

An entry with `continues: true` is the FIRST half of a chant whose remaining
pages are in a batch I have not sent yet. Write it normally, then put a comment
at the top of its dict so I can find it:

    # ⚠️ CONTINUES: last verse here is N, from page P. Rest of the chant is on
    # page P+1 onward and has not been added yet.

That chant is incomplete on purpose. Do not write the missing verses, do not
flag it as an error, and do not treat it as truncation — `batch_status.continues`
lists it precisely so the two cannot be confused. Report continuations as their
own line in the summary: "3 added, 2 merged, 1 continued, 1 left open".

## When a chant is ALREADY in the file — merge, never replace

Seventeen chants were set before this workflow existed, and NONE of them has a
page number. As I work down the book I will photograph their pages like any
other. That is deliberate: it is how they finally get their page numbers, and it
is the only chance to check them against the book a second time. It must NOT
produce a duplicate.

Those seventeen matter more than the count suggests. Until they have page
numbers they cannot appear in the page-by-page reading view at all — the book
would have holes in it exactly where its first chants are.

So when an id already exists in CHANTS:

1. Do NOT append a second dict, and do NOT suffix the id with a number.
2. ADD only what is genuinely missing — normally `page_start` and the per-verse
   `page` keys, sometimes a field that did not exist when the chant was set.
3. KEEP THE EXISTING CHANT'S TEXT. Every `pali`, `pali_roman`, `thai`,
   `paiboon`, `english`, title, section and invitation already in the file stays
   exactly as it is. The file wins. The new reading does not overwrite it.

   The file wins because those seventeen were typed by me with the book open in
   front of me, and the new reading came off a photograph. Where the two
   disagree, the more likely explanation is the camera, not my hands. That is a
   default, not a judgement — which is why every disagreement gets reported.
4. COMPARE the two anyway, character for character, and REPORT every difference
   you find — which verse, what the file says, what the new reading says. Show
   both. Change nothing on the strength of it.
5. If a difference is more than whitespace, also leave a comment above that
   verse so it is findable later:

       # ⚠️ PHOTO DIFFERS: file kept. Read from p.<page> on <date>: <what it said>

Report merges separately from additions. A line saying "3 added, 2 merged" is
the one I read first, because a merge silently becoming an append is how this
book ends up with the same chant twice.

The only thing that overrides rule 3 is me saying so explicitly, chant by chant.
"Use the new text for verse 4" is an instruction; the photograph differing from
the file is not.

One exception, and only one: `page_start`, the per-verse `page` keys and
`book_number` are ADDITIONS, not disagreements. None of the seventeen has any of
them, so there is nothing to overwrite and rule 3 does not apply.

## Page numbers

- `page_start` goes on the chant dict, near the title fields, as a bare integer.
- `page` goes on a verse ONLY where stage 1 put one — the first verse of each
  new printed page. Do not add it to every verse, and do not fill in the gaps.
- If stage 1 omitted a page number, leave it omitted. Never infer one from the
  chant before or after it. The template guards both with `{% if %}`, so a chant
  without page numbers renders exactly as it does today.
- `book_number` and `book_number_printed` go on the chant dict beside the titles
  where stage 1 gave them, as they came. These are the book's own chant numbers,
  not page numbers, and the two must never be swapped or derived from each other.

**A verse's page is carried forward, and this is the rule the page view depends
on.** A verse without a `page` key is on the same page as the verse before it;
the first verse without one is on `page_start`. Only page TURNS are marked, the
same way `section` marks only where a movement begins. That is what makes the
data compact enough to work with, and it is exactly why the page map has to be
checked against it — a single missing marker silently moves every verse after it
onto the wrong page.

**File order is not book order, and does not need to be.** Append new chants at
the end of CHANTS. `page_start` is what says where a chant sits in the book, and
the reading view sorts on it. Never reorder existing dicts to make the file read
in book order — that produces an enormous diff across verified text for no gain,
and moving verified Pali around is the risk this whole workflow avoids.

## Mapping

Keys map straight across: title_thai, title_pali, title_roman, title_english,
book_number, book_number_printed, page_start, layout, source, source_printed,
when_chanted, summary, english_unverified, background, meaning, invitation,
closing, verses. Each verse keeps its 'number', its 'page' where it has one, and
its 'section' where it has one. Set 'group': 'General chanting' unless I say
otherwise.

Four of those describe how the PRINTED page is set, and the template guards each
with `{% if %}`, so a chant without them renders exactly as chants do today:

  layout          — 'prose' only. Anything else, leave the key off.
  closing         — the จบ formula, same five-layer shape as a verse.
  source_printed  — the book's own footnote reference. NEVER write this
                    yourself and never copy `source` into it. It exists to be
                    the one citation nobody in this pipeline composed.
  book_number     — the book's chant number.

An empty `thai` or `paiboon` on a verse is a FACT, not a gap: the book printed
that chant in Pali only. Write the empty string through as it came. Do not
translate the Pali into Thai, do not romanise the Pali into the paiboon field,
and do not flag it as missing data. A chant can be Pali-only, and a page can
carry one chant of each kind.

Four keys do NOT go in as data:
  working_notes   → ignore. It is Josh's reading aid.
  continues       → becomes the ⚠️ CONTINUES comment, not a field.
  continuation_of → tells you to append to an existing chant, not a field.
  checks          → turn each entry into a ⚠️ code comment. A check with a
                    "verse" number goes directly above that verse; a check with
                    "verse": null goes at the top of that chant's dict. NEVER
                    drop one silently — they are what Josh still has to verify
                    against the physical book, and several of them now name a
                    photograph he has to retake. Report the count PER CHANT, not
                    as a batch total; a total hides a chant whose checks all
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

At EVERY depth, every verse must carry all five layer KEYS — pali, pali_roman,
thai, paiboon and english. A verse missing its english is a fault at any depth,
not a depth setting. Stop and tell me rather than writing it.

Carrying the key is not the same as carrying a value. On a Pali-only chant
`thai` and `paiboon` are "" because the book prints no Thai, and that is
correct and finished. What is a fault is a MISSING key, or a value invented to
fill one.

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
   of entries in the batch. Neither a merge nor a continuation may change the
   count. If the count moved by more than that, a merge or a continuation became
   an append and there is now a duplicate: stop and tell me.
3. Confirm every id is unique. Two dicts with the same id is the failure this
   whole merge rule exists to prevent, so check it explicitly rather than
   assuming.
4. For EACH chant, compare the Thai and Pali you wrote against the JSON I pasted
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
8. PROVE the pages against the map, which is the check the reading view depends
   on. Walk the chants you wrote and rebuild each verse's page by carrying
   forward — a verse with no `page` key is on the page of the verse before it,
   and the first is on `page_start`. Then compare that against `batch.pages`,
   verse by verse. Print the disagreements, or print "pages agree: N verses
   across N pages". If they disagree, do NOT adjust either side to match: show
   me both and stop. One side is what the photograph said and the other is what
   went into the app, and I need to know which is wrong before either is trusted.
9. For each CONTINUED chant, confirm the joined verse numbers run 1..N with no
   gap and no repeat, and that the verse count equals what was there before plus
   what arrived. Print the join: the last two verses from before and the first
   two from this batch, so I can see the seam.
10. Render the page and confirm each new chant shows the right verse count, its
    section headings, its page markers and its layers, and that existing chants
    are unchanged.

Report THREE tables. I read the tables, not the prose.

  Added chants:    id, page_start, book_number, verses in, verses written,
                   checks carried, char match y/n.
  Merged chants:   id, what you added, how many differences you found, and
                   whether the existing text was left intact.
  Continued/open:  id, verses before, verses added, joined range, and whether
                   the chant is now complete or still carries ⚠️ CONTINUES.

Then, separately from the tables, list every page whose number stage 1 could not
read and every image it asked me to retake. That is my next job, and it is the
one thing here that gets harder the longer it waits — the book will be back on
its shelf.

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

SKIP any chant also carrying a `⚠️ CONTINUES` comment, however many are left.
That chant is only half in the app: the rest of its verses are on pages I have
not photographed yet. Commentary written about half a chant would describe a
thing that does not exist, and it would look finished. List the ones you skipped
so I know which pages to photograph next.

## The one rule that outranks everything else here

DO NOT TOUCH A SINGLE CHARACTER OF ANY VERSE.

`pali`, `pali_roman`, `thai`, `paiboon` and `english`, the titles, the
invitation, the sections, the verse numbers, `page_start`, the per-verse `page`
keys, `book_number` and the existing ⚠️ comments have all been verified against a
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
