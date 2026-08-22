# Chanting book — next session

Paste-ready brief for picking this work up cold. Updated 2026-08-22 after page
79 went in.

## Read first, in this order

1. `docs/chanting-book-photo-map.md` — the brief, read it fully
2. `prompts/chanting-book-batch/README.md` — the two-stage workflow
3. `C:\Users\joshk\OneDrive\Documents\Documents\Digital Chanting Book\chanting-book-batch-prompts.pdf`
   — the Stage 1 and Stage 2 prompts. **Read it before any fresh page read.**

## State — verify with git, don't take this file's word

- **Pages 1–79 are in and unbroken**, plus 217–221. **108 chants, 1,390 verses
  reconciled against their photographs.** `/chanting` derives its own coverage
  line, so it is never stale — read it rather than this bullet.
- 11 of the 17 pre-page chants are verified against their photographs.
- Pages 78 and 79 were applied 2026-08-22; pages 75 to 77 on 2026-08-21; pages
  69 to 74 on 2026-08-19; pages 66–68 over the days before them; 61–65 on
  2026-08-14 and 2026-08-15; 55–60 on 2026-08-11 and 2026-08-12.
- **Page 77 opens a whole new part of the book** — `สิบสองตำนาน`, the Twelve
  Tamnan parittas appointed for evening chanting. Everything from here is
  paritta until the book says otherwise.

## How to work — this matters more than the tasks

**One page at a time.** Read the photograph, write the batch, apply it, show the
diff, commit, then **stop** and say the page is done. Ask before pushing and
before any commit to `main`. No `Co-Authored-By` trailer.

A page can hold more than one chant, and often three. **Read the whole page
before deciding what it contains** — page 30 was expected to be Pabbatopama
alone and turned out to hold the end of one chant, a brand-new one, and the
start of a third.

## Next: page 80, `IMG_0344` — but READ THE NUMBER off the sheet

The offset of 264 has now held for six pages, so page 80 *should* be
`IMG_0344`. Six more changes are still predicted before page 207, so read the
top-centre number.

**`namokara-atthaka-gatha` is open at verse 3, and it is NOT a cut line.** Page
79's last row is a whole printed unit, so there is no `[…]` to complete: page
80's batch is an ordinary `continuation_of` numbering **from 4**.

**The title says how many verses to expect.** `อัฏฐะกะ` means a set of eight
and only three are in, so **five more should follow on page 80**. That is a
reason to expect a continuation, not a reason to write one — and if page 80
gives a different number, the book wins and the count goes in a check.

**Expect two columns and check for a hyphen at the gutter.** These three rows
are two-column with a 140px gutter, and the first of them breaks a word across
it with a hyphen. If page 80 continues the same setting, the same thing can
happen again.

## Standing rules for every page

**Measure the layout, do not judge it.** Profile the ink across the measure
before reading a word — a gutter around x 940–1100 means two columns, ink
filling the measure with no gutter means prose, ink stopping short on both
sides means centred lines. Pages 75 and 76 were both measured this way and are
prose end to end.

**A paragraph can span a page turn, and page 75 is what taught that.** Its first
paragraph opened on page 74 at verse 58, so verse 59 must NOT carry
`para_start` — but it IS the first verse of the page-75 slice, and the template
reads `para_layout` off `paragraph[0]`. So verse 59 carries **`para_layout`
without `para_start`**. The general rule: whenever a page opens mid-paragraph in
a chant whose own `layout` disagrees, the first verse on that page needs
`para_layout` and nothing else. Where the chant's own `layout` is already right
— as on page 76, which is a prose chant throughout — nothing is needed and
declaring it would be noise.

**Check the rendered page, not just the four checks.** Page 76's trailing block
passed all four and still rendered in the wrong place. See "What page 76 taught
the tooling" below.

## What page 79 proved — a hyphen across the gutter

**The strongest evidence for a two-column reading this book has given.** The
left column of the Namokāra's first row ends `สัมมา-` **with a hyphen**, and
the right column opens `สัมพุทธัสสะ`. A hyphen at the end of a left column
cannot mean anything but "this word continues to the right", so the row is read
across and the word rejoins as `สัมมาสัมพุทธัสสะ` with the hyphen dropped as
typesetting.

Worth keeping because the two-column danger is the worst failure available on
these pages, and every other page has been settled by measuring a gutter. This
one settled itself.

**One sheet, two settings, and only a per-block profile caught it.** Page 79's
upper chant is single column (ink x 500–1260, no gutter) and its lower chant is
two (140px gutter at x 1000–1140). Profiling the page as a whole would have
blurred both. **Profile each block, not each page.**

**Two more `ส์` marks** — `ส์วากขาตะธัมมัง` and `ส์วากขาตัสเสวะ`, both at 9×,
both the ε-curl page 60 identified. Romanised `sv-`, matching all eight existing
`ส์วากขาโต` lines in the app. This is still the open question of the whole
stretch: the app holds this one word **three ways** (plain `ส`, `ส์`, `ส๎`) and
one look at the book settles every one of them.

## Raised on page 78 — one settled, two open

**THE PAGE-77 INFERENCE WAS RIGHT, and that is worth recording as a method.**
The refuge chant was marked `‼ CONTINUES` on reasoning about how the formula is
chanted rather than on anything the photograph showed. Page 78 opens
`ทุติยัมปิ`, so it did continue. **The rule that produced the right answer:
where a chant may or may not be finished, mark it as continuing.** A stale
marker costs one line to remove; a truncated chant that reads as whole is the
failure this workflow exists to prevent.

**`สัมพัทเธ` in the title against `สัมพุทเธ` in its own body**, on one sheet.
Both read at 8× on isolated crops and stacked one above the other: the vowel is
unambiguously **above** the พ in the title (ั) and **below** it in every verse
(ุ). Standard Pali is *Sambuddhe*, so the title is the odd one. Both reproduced
as printed, which is why `title_pali` is `Sambaddhe` while every verse romanises
`Sambuddhe`. **The id follows the body — `sambuddhe`** — because an id is a
permanent handle and should not carry a probable slip.

This is now the **third page in four** to spell one word two ways: page 72 with
Pāṭimokkha (ฏ against ต), page 76 with sampuṇṇa (ณณ against ระณ), page 78 here.
Treat "it differs from the line before" as a reason to look, never as proof of a
misreading.

**Verse 12 carries a full stop that its two parallel lines lack.** The three
stanzas are identical apart from their numbers, and verses 2 and 7 end `อะหัง`
with nothing while verse 12 ends `อะหัง.`. Read at 5×; reproduced on all three.

**The first canonical citation in this stretch.** `ขุ. ขุ. มหา. 25/1`, keyed to
the last refuge, goes in as `source_printed` — pages 76 and 77 both carried
footnotes that were *editorial* and were deliberately kept out of that field.
The distinction is still the one that matters: a reference goes in the field, an
instruction to the chanter does not.

## Raised on page 77 — two decisions, and a test that earned its keep

**TWO OF THE THREE CHANTS ON THIS PAGE ARE REPRINTS, and whether the edition
should show them separately is Josh's call, not a reading.** The book prints the
Namo salutation on pages 2, 52 and now 77, and the going-for-refuge on page 12
and now 77. Each went in as its own chant, on the one-entry-per-printing rule
this book has followed since page 61 — and the readings support it, because both
page-77 printings visibly differ from the earlier ones:

| | earlier printings | page 77 |
|---|---|---|
| Namo | no title at all (`title_thai` is `''` on both) | prints `ปุพพะภาคะนะมะการะปาโฐ` |
| Namo | every line ends `.` | third line ends `ฯ` |
| refuges | page 12 separates them with **commas** | page 77 uses **full stops** |

So the app now holds three Namos and two refuge formulas. That is faithful to
the book and may still be more than the edition wants.

**`สะเมตตา` with double ต at verse 2**, where standard editions have *sametā*.
Read at 7× on an isolated crop; reproduced and transliterated `samettā` to match.

**The bracketed first line is conditional.** Verse 1 is printed in round
brackets with a superscript, and the footnote reads
`ใช้แต่ในราชพิธีและรัฐพิธี` — "used only in royal and state ceremonies". The
brackets are reproduced and the footnote is a page block at the foot, but
**nothing in the data ties the two together**: a footnote block sits at the page
foot and cannot point back at a verse. Same shape of gap as page 76's
conditional variant, and the same decision is still open.

## What page 77 taught — the tests caught three of my errors

Worth writing down because it is the first time the suite, rather than a check
script or a re-read, found the mistake:

- `ปาโฐ` was transliterated **`pāṭha`** on two titles. It is **`pāṭho`** — the
  nominative, with โ. `tests/test_contents_roman.py` romanises every Pali title
  independently and compares, so it failed on both.
- `บทขัดชุมนุมเทวดา` was romanised `bòt kàt …` with a space where the contents
  table has `bòt-kàt …` with a hyphen, and a second test refuses to let the
  contents and the chant page spell one title two ways.

**All three chants were already listed in the book's own สารบัญ, and
`CONTENTS` already held the correct romanisation of all three.** The right move
when a title is already in that table is to take the value from it rather than
compose one — check `chanting._CONTENTS_ROMAN` before writing `title_pali` or
`title_roman`.

**Run the whole suite, not just the four checks.** All four checks passed on the
version with three wrong titles in it.

## The ฬ/พ misreading, and how page 76 explained it

Worth reading before any page in this stretch, because it is the one failure
these photographs produce that looks completely convincing.

Page 76 shows both cases **on one sheet**, eleven lines apart:

- The Thai instruction paragraph at the foot prints `อาสาฬหบูชา` **bare**, and
  the ฬ ascender is unmistakable at 8×.
- Verse 15 prints `อาสาฬ์หะปุณณะมีกาลัง`, where the ฬ carries the ์ cluster
  mark — and the ascender does not survive the printing. The mark sits exactly
  where the ascender would be, and the letter is indistinguishable from พ at
  any magnification.

So the rule is narrower and more useful than "the camera cannot tell them
apart":

- **A bare ฬ can be read from the photograph.** The ascender is there.
- **A MARKED ฬ์ cannot be, ever.** It will read as พ์ every time.
- **A missing ascender is never evidence for พ.** That is what page 75 got
  wrong.

One more tell, and it is the one that should have caught page 75 before Josh
did: **พ์ห is not a legal Pali cluster.** Transliterating it gives `āsābha`,
which is not a word. If a faithful transliteration produces a non-word, the
reading is wrong — check the letter rather than recording the non-word.

## Raised on page 76 — three open, one decision needed

**A FOOTNOTE THE APP CANNOT FULLY SHOW — this one needs Josh's call.** Verse 20
carries a superscript 1 on `อิมัง ถูปัง`, and the footnote reads
`๑. ถ้ามีพระพุทธรูปเป็นประธานใช้ อิมัง ปะฏิมัง` — "if a Buddha image is the
principal object, use อิมัง ปะฏิมัง". It is an editorial note, not a citation,
so `source_printed` is correctly left off, and it is recorded as a verse
**variant**, which both templates render as "the book's footnote gives another
reading: อิมัง ปะฏิมัง". **The CONDITION is lost**, and for this footnote the
condition is the whole point — it tells a chanter *when* to say it. Either a
`condition` field on a variant plus one line in each of the two templates, or
leave it. Not decided.

**`สัมปุณณัง` at verse 14 against `สัมปุระณะ` at verse 15** — the same word,
twice on one sheet, both read at 7× on isolated crops. Standard Pali is
*sampuṇṇa* in both places. Reproduced as printed and transliterated to match,
which is why the romanised layer looks inconsistent. The clearest single thing
on the page to check.

**The pointing is now three readings to one against page 69.** Page 76 splits
`ปัต์วา,` from `อิมัง ฐานัง สัมปัตตา,`, runs `ยะถาภุจเจ คุเณ อะนุสสะรันตา,`
together, and runs `ญาตัพเพหิ คุเณหิ` together — matching the Visākha printing
on page 66 in all three places and differing from the Aṭṭhamī printing on page
69 in all three. **`IMG_0332` is now worth re-reading**; page 69 is the odd one
of three.

**`ปะฏิคคัณหาตุ` is bare for the fifth printing running** — 68, 69, 70, 71 and
now 76, against page 67's single `ปะฏิคคัณ์หาตุ`. Page 67 is looking like the
outlier rather than the rule.

**One thing to fix in the app, not in the book.** The Visākha entry's verse 56
carries `Sucirapaṇinibbutopi` as its `pali_roman` where its own `pali` reads
`สุจิระปะรินิพพุโตปิ`. Page 76's verse 22 is written correctly as
`suciraparinibbutopi`, so the two chants now disagree in the app. Nothing was
changed — different chant, and the file wins unless Josh says otherwise.

## What page 76 taught the tooling

**`apply_batch` now carries a verse's `variants`.** The field has been in
`chanting.py` since `b40c9c5` and both templates have rendered it ever since;
this loop was the only thing between a batch declaring one and the app showing
it. Same class of gap as `rubric`, `para_start` and `para_layout` before it. It
renders long-hand rather than by `repr`, and refuses a variant missing its
`marker`, `word` or `reading`.

**A trailing block needs its own page-map row.** Page 76's Thai instruction
paragraph is printed BELOW the chant, but `block_groups` anchors a non-footnote
block to the *previous* chant on the page — which, on a one-row page, is
nothing, so it rendered at the TOP. The fix is a second row for the same page
with `"chant": ""` and `"verses": "none"`, carrying the block. The block then
anchors after the chant, which is where the book prints it. Caught by reading
the rendered page, not by any of the four checks: `check_render` deliberately
checks blocks for presence only, and placement is `check_page_blocks`'s job,
which was satisfied because the anchor was *valid* — just not where the book
puts it.

## Raised on page 75 — one still open, two settled

**The ฬ/พ hazard, in a title — SETTLED, and the reading was wrong.** Above.

**STILL OPEN: the three trainings are pointed unevenly.** Verse 83 prints
`อะธิสีละสิกขาสะมาทาเน อะธิจิตตะสิกขาสะมาทาเน,` with **no comma between the
first two** and one after the second, then `อะธิปัญญาสิกขาสะมาทาเน,` with its
own. Read at 4× across the whole line. Standard editions comma all three. That
is why verse 83 holds two of the trainings and verse 84 holds one.

**SETTLED: `ปฏิจจะ` really is printed without the ะ** this book usually sets
after the ป (`ปะฏิจจะ`). Read at 8× on an isolated crop, and Josh confirmed it
from the book on 2026-08-21. Kept as printed; `paṭicca` either way, since the ะ
is orthography rather than a different word.

**`ตัส์มา` carries the small mark over the ส**, an ε-shaped curl with a tail at
5× — the same shape page 60 read on `ท์วายะ`. Recorded as ์ (U+0E4C) like
everything else in this stretch. Still part of the one open question that the
book settles in a single look.

**Page 63 was the first page in the book with no chant on it at all** — the
whole sheet is `คำอธิบายประกอบทำวัตรเย็น`, so its batch has an EMPTY manifest
and everything on it is a block. `check_batch`, `apply_batch` and `check_pages`
all handle that now; `check_pages` needed one fix to stop reporting such a page
as unrecorded. More pages like it are coming.

**A block's `number` can be a Thai letter.** Page 63's sub-notes ก and ข go in
as `'number': 'ก'`, and the template renders them exactly as printed. Do not
convert them to digits.

### Settled since: a prose chant with paragraphs

The gap the last brief flagged is closed. `para_start` on a verse plus
`verse_paragraphs` in `chanting.py` (commit `c3b38e6`) splits a prose chant into
the paragraphs the BOOK sets it in. Page 61 used it second and renders four
justified blocks; page 64's passage has no paragraph break at all and correctly
renders as one group of 37.

### Settled on page 73: a chant set BOTH ways

`layout` is chant-level and can only say prose OR lines. Page 73 needed both in
one chant, so a paragraph may now override it with **`para_layout`** — `'prose'`
or `'lines'` — declared on the verse that opens the group, beside `para_start`.
`apply_batch` carries it through and the CSS keys on the paragraph rather than
the chant container.

**The fallback is the safety.** A paragraph that says nothing takes the chant's
own `layout`, so every chant entered before this renders exactly as it did —
proved by rendering all 77 pages both ways and diffing the visible text, and by
checking the class lands on the same 61 paragraphs and no others.

So: declare `para_layout` on every group of a mixed chant rather than relying on
the default, because the default is right only by luck when a chant changes.

Pages 222 and 223 sit beside 217–221 which are already in, so they are a cheap
excursion whenever wanted.

## A rubric printed inside a chant goes on the VERSE

Pages 53 and 54 both print หมอบลงพร้อมกัน… between verse 14 and verse 15 of a
hymn. A page block cannot go there — `build_page_index` can only put blocks
between whole chants — so it rides on verse 14 as `'rubric'`, which the template
renders under that line. Same mechanism as page 1's (กราบพร้อมกัน).

`apply_batch` carries a verse `rubric` through, so declare it on the verse in
the batch file and it lands. Do not try to force it into `batch.pages.blocks`.

## The tooling, and what it will and won't do

`check_batch.py` then `apply_batch.py --dry-run` then apply, then
`check_pages.py` and `check_render.py`. All need `PYTHONIOENCODING=utf-8` on
Windows or they die on the first Thai character.

`check_batch` also knows about `[…]` now. A line the page break cut in half has
to be well formed — both chanted layers agree it was cut, the chant is listed
in `batch_status.continues`, and the cut falls on the last verse. All three
were confirmed to pass silently before, and page 68 was written with a real
`[…]` that nothing looked at.

Three kinds of entry:

- **new** — a chant not in the app. Appended.
- **continuation** — `continuation_of`, bringing later verses of a chant already
  started. Carries on the verse numbering; never restarts at 1.
- **merge** — `merge_only: true`, for a chant already in the app in full. Brings
  `page_start`, `book_number`, `layout`, `source_printed`, a `closing`,
  `corrections` and `page_markers`, and **no verses**.

`corrections` overwrite text already in the app and are matched on the whole
literal, required to appear exactly once inside that chant, or they raise and
write nothing. `page_markers` record where a printed page turns inside a chant
already in the file — **without one, every verse lands on `page_start`** and the
page shows far more than the book prints. That was missed once already, on
Saccapāna verse 11.

### Then `check_pages.py`, which is the one that answers Josh's question

`scripts/check_pages.py` reconciles EVERY batch file against the app: does each
page show the chants, the verses and the blocks its photograph recorded, with
the same text. It is the third check, and the only one that asks whether the app
page matches the printed page — `check_batch` checks a batch against itself and
`apply_batch` only writes. Run it after every page. It also runs as a test
(`tests/test_check_pages.py`), so a page going out of step with its photograph
breaks the suite instead of waiting to be noticed.

It knows one rule worth knowing yourself: a line cut by a page break belongs to
the page it STARTS on, and the completed line must begin with the partial one.
The `english` layer is exempt from that prefix test — the gloss of half a
sentence is not the start of the gloss of the whole one.

### And `check_render.py`, which opens the page a reader meets

`scripts/check_render.py` is the fourth check and the only one that renders.
`check_batch` checks a batch against itself, `check_pages` checks the DATA
against the batch, and neither looks at the HTML — but correct data renders
badly often enough to matter, and a dropped block or a verse in the wrong order
is invisible to all three of the others.

It **walks** rather than counts: it takes each chant's strings in printed order
and consumes them from the rendered text, never searching backwards. That is
deliberate. Counting occurrences is the obvious approach and it is wrong twice
over — the book legitimately prints the same line twice (page 67's
`ตัสสะ ภะคะวะโต,`), and short units sit inside longer ones (`พุทโธ,` inside
`สัมมาสัมพุทโธ,` on page 66). Every false alarm the throwaway versions of this
check produced came from counting.

It deliberately does NOT police two things, because they are decided elsewhere
and have their own tests: which of two chants renders first (`build_page_index`
sorts by the book's chant numbering) and where a block sits (`block_groups`
anchors it). It checks blocks for presence only.

Runs as a test too (`tests/test_check_render.py`), so a page that starts
rendering the wrong thing breaks the suite.

## Raised on pages 61–65 — all open, all need the book

**The chant printed twice, and the app now holds it twice on purpose.**
Dhātupaṭikūlapaccavekkhaṇa is printed at page 61 AND page 207 — the สารบัญ
lists both. The pre-existing `dhatupatikula-paccavekkhana` has a Thai
translation, ~30 short verses and parenthesised rubrics; page 61 has none of
that, being Pali-only in four run-on paragraphs. Josh chose two entries, one per
printing, on the condition the app shows exactly what each page shows. So page
61 is `dhatupatikula-paccavekkhana-p61`, and the old entry takes `page_start`
207 when that page is read. **`IMG_0477` (page 207) has still not been read**,
so which printing the old entry came from is inference from its shape.

**The same chant name is spelt three ways in three places.** `อุทิสสะ` in the
book's own สารบัญ (so, in `CONTENTS`), `อุททิสสะ` on page 62's title and
colophon, `อุททิสะ` in page 63's sub-note ก. All read at 5–7×, all reproduced,
none reconciled. One look settles all three.

**Page 64 verse 24 is the ฬ/พ hazard on a chanted line.** The page reads
`โอพารกา` / `โอพาริเกนะ`; the canon has *oḷārikā* / *oḷārikena*, and the sense
of the clause — beings who need something tangible, which is why the stūpa was
allowed — favours the canon. The glyph was compared at 16× against a known พ on
the same page and matched, but the photo map already records that this exact
comparison cannot settle ฬ from พ. Reproduced as it appears. The first word also
appears to lack the ิ the second has, so the book may be inconsistent too.

**Vowels the book shortens where standard editions lengthen them.** Page 61
verse 14 prints `นีชชีโว` with a long ี where its other three paragraphs print
`นิชชีโว` — declared as a diacritic exception, since the book itself differs
from itself. Page 62 prints `หินา` and `วิริยัมหินา` short where editions have
*hīnā* and *vīriyamhinā*. All kept as printed.

**Two chants on pages 64–65 have no colophon**, unlike pages 60, 61 and 62.
Checked against both pages; the `closing` key is left off rather than composed.

## Raised on page 72 — the book contradicts itself on one sheet

**Pāṭimokkha is spelt two ways on page 72.** The Māgha Saraphañña prints
`ปาฏิโมกขัง` with ฏ at its verses 9 and 18. The chant directly beneath it is
titled `โอวาทะปาติโมกขาทิปาฐะ` and prints `ปาติโมกขัสสะ` at its verse 2 — both
with ต. All four read at 3× on isolated crops. Same word, same sheet, two
spellings, all reproduced as printed. This is the clearest single-page evidence
yet of how much this printer varies, and it is worth remembering the next time a
spelling looks like an error: **the book is not always consistent with itself,
so "it differs from the line before" is not evidence of a misreading.**

**`บทขัด` is a section, not a chant and not a block.** It is printed centred
below the title and above the first verse, naming the prefatory verse. It rides
on verse 1 as a `section` and the template renders it as a heading. A page block
could not go there — `build_page_index` can only put blocks between whole
chants.

**The first explanatory paragraph in this run went in as a page block**, and it
is declared on the SECOND page-map row rather than the first. That is what makes
`block_groups` anchor it after the chant above it, which is where the book
prints it; declaring it on the first row would have lifted it to the top of the
page. It names the chant in **bold** mid-sentence, which `PAGE_BLOCKS` has no
field for — the words are kept and only the weight is lost.

**The three Saraphañña sets are not the same length.** Visākha and Aṭṭhamī both
run to thirty verses; the Māgha one ends at twenty. That is the book, not a page
missed — its last line closes with `ตาทิโนติ.`, the quotative plus a full stop.

## Raised on page 71 — three chants on one sheet

**The Māgha offering is not a variant of the other two, and that is settled by
reading it.** Visākha (p66) and Aṭṭhamī (p68) share almost every word. The Māgha
one shares only its closing petition — the rest recounts the fourfold assembly
and the Ovāda-pāṭimokkha. It is set in full as its own chant, not stubbed as a
repeat, and its English is written fresh rather than copied across. Āsāḷha, the
fourth, is still to come.

**Two readings in the Māgha Saraphañña differ from the canon.** Verse 4 prints
`มาฆะทานัง` where the sense wants `มาคะธานัง` — *māgadhānaṃ*, "of the
Magadhans", which is whose hill-fort Rājagaha is. Verse 5 prints `เวฬุวันนัมหิ`
with a doubled น where editions have *veḷuvanamhi*. Both reproduced as printed.
The first is the one to look at: six other words on that page begin `มาฆะ`, so
a compositor's eye slipping is a plausible account of it.

**`ปะฏิคคัณหาตุ` is bare for the FOURTH page running** — 68, 69, 70 and 71 all
bare against page 67's `ปะฏิคคัณ์หาตุ`.

**A fifth divergence between the Saraphañña twins**, and the second that looks
like a slip in the earlier reading rather than a real difference. Page 71 ends
the Aṭṭhamī chant `อายานัญจาภิวุฑฒิยา.` with a full stop; the app holds the
Visākha twin's verse 30 without one. It is the last line of a chant, where a
stop is what you would expect. Nothing on page 68 was changed.

**`เวฬุวะเน` really is ฬ, and this is the one case where the photograph can say
so.** The photo map's warning that these images cannot tell ฬ from พ still
stands generally — but ฬ carries a tall ascender that พ does not, and at 4× it
is plainly there. Recorded on the strength of the ascender, with the canonical
reading agreeing rather than deciding.

⚠️ **This holds only in the direction it was used.** Page 75 turned the same
test around — no ascender, therefore พ — and was wrong. Seeing an ascender can
settle a letter as ฬ; not seeing one settles nothing.

## Raised on page 70 — the twins disagree in four letters

Page 70 is twenty-six two-column rows of one chant and nothing else, and its
verses 11–28 are the Visākha Saraphañña's verses 11–28. Across those eighteen
shared verses the two printings diverge in exactly four places:

| verse | page 70 (Aṭṭhamī) | pages 67–68 (Visākha) | which is standard |
|---|---|---|---|
| 9 | `อะนุกาเลนะ` *anukālena* | `อะนุกาเรนะ` *anukārena* | either is a word |
| 12 | `กะโรนตา` *karontā* | `กะโรนาตา` *karonātā* | **page 70** |
| 15 | `เอกัตถะ` *ekattha* | `เอกัตตะ` *ekatta* | **page 70** |
| 26 | `…มานะสาธุ` (runs on) | `…มานะสา.` (stops) | **pages 67–68** |

Each was read at 4× on an isolated crop. In two of the four page 70 carries the
standard form and the earlier reading does not, which makes **`IMG_0330` and
`IMG_0331` worth a second look alongside the book** — these may be reading slips
on the earlier pages rather than real differences between the printings.
Nothing on those pages was changed. Verse 26 matters most of the four: with
`สาธุ` the sentence runs on into the petition, and with `มานะสา.` it stops.

**Two spellings on page 70 differ from standard editions and both look
deliberate.** Verse 3 prints `สัพพะคัมธานัง` with ม where editions have
`คันธานัง`; verse 5 prints `พัตติงสะ` (*battiṃsa*) where editions have
*dvattiṃsa* — and *battiṃsa* is an attested Pali form, so that one is the book
choosing a variant rather than erring. Both reproduced as printed.

**`ปะฏิคคัณหาตุ` is bare for the third page running** — 68, 69 and 70 all bare
against page 67's `ปะฏิคคัณ์หาตุ`. Three against one on the same word in the
same formula.

## Raised on page 69 — all open, all need the book

**The two parallel offerings are pointed differently in four places, and the
difference is now confirmed from both sides.** Visākha runs across pages 66–67
and Aṭṭhamī across 68–69, and they print the same sentences with different
commas. Page 69 takes a full stop at `โลกะวิทู.` where page 66 takes a comma;
it merges `…ปัต์วา อิมัง ฐานัง สัมปัตตา,` into one unit where the twin keeps
two; it splits `ยะถาภุจเจ คุเณ,` from `อะนุสสะรันตา,` where the twin runs them
together; and it makes three units of `สุจิระปะรินิพพุโตปิ, / ญาตัพเพหิ, /
คุเณหิ อะตีตารัมมะณะตายะ ปัญญายะมาโน,` where the twin has two — separating
`ญาตัพเพหิ` from the `คุเณหิ` it agrees with. Every comma was read on an
isolated 3× crop. All four are reproduced as each page prints them, and all four
are one look away from settled.

**`ปะฏิคคัณหาตุ` is bare again, and it is now two against one.** Page 67 prints
it `ปะฏิคคัณ์หาตุ` WITH the small mark and the app holds it that way; pages 68
and 69 both print it bare. So the live question on this word is no longer which
of the two marks the printer cuts, but **whether he sets one at all** — which is
the same thing page 60 found on `อุณหัสสะ`. Worth knowing because the omission
is exactly what a reader would "correct" without noticing.

**The Aṭṭhamī chant names the Visākha full moon.** Page 69 verse 43 prints
`อิมัง วิสาขะปุณณะมีกาลัง,` just as the Visākha twin does. It is not an error:
Aṭṭhamī is the eighth day reckoned FROM that full moon, and what actually
differs is the next unit — `สะรีรัชฌาปะนะกาละ` (the time of the cremation of
the body) where the twin has `ชาติสัมโพธินิพพานะกาละ`. Recorded because it
reads as a mistake to anyone who does not know why it is there.

**One thing to fix in the file rather than in the book.** The Visākha twin's
verse 56 carries `Sucirapaṇinibbutopi` as its `pali_roman` where its own `pali`
reads `สุจิระปะรินิพพุโตปิ` — *parinibbutopi*, with an r. It looks like a
transliteration slip in existing data rather than anything the book did. Nothing
was changed, because the rule is that the file wins and only Josh overrides it
chant by chant.

## Four things waiting on Josh — ask, don't guess

**The orphan footnote across pages 57, 58 and 59.** Page 57 prints a marker ๑
with no footnote under it. Page 58 prints a footnote `1. วิ.มหา. 4/170` with no
marker anywhere in its body — every line end checked at 3×. Page 59 then prints
**both**: a marker ¹ on its last verse and `1. วิ.มหา. 4/171` at its foot. So 59
is the intact version of what 57 and 58 each have half of, and 4/170 and 4/171
are consecutive references in the same Vinaya volume.

That is evidence the note on 58 belongs to the marker on 57, carried over to the
next page's foot. It is **not** proof, because footnote numbers restart on every
page and the rule is not to pair across pages. Nothing was changed. Page 59's
own footnote is filed as `source_printed` on its chant; pages 57 and 58 have
`source_printed` left off entirely, and 58's note sits as a page block. One look
at the book settles all three at once.

**สวากขาโต, and which mark goes over the ส.** Page 51 prints it TWICE with a
mark above the ส, and at high magnification that mark is the same shape as the
thanthakhat in ประดิษฐ์ four lines above it, in the same face and size — so page
51 was read as **ส์วากขาโต**. The app now holds this one word three ways:
plain `สวากขาโต` (page 1, and the page-1 นมัสการ), `ส์วากขาโต` and `ส๎วากขาโต`.
Two of the three must be wrong. One look at the book settles the whole word
everywhere, and it is a chanted line, so it is worth doing early.

Pages 52–53 widened it from one word to a **class**. The same small mark turns
up over the ล of กัล์ยาโณ, the ธ of พุทธ์วา, the ส of พุทธัสสาหัส์มิ and the ส of
ส์วากขาตะตา — and the app already holds the first of those the other way, as
กัล๎ยาณัง with U+0E4E in `buddhabhithuti`. So the question is not "which mark on
this word" but **which of the two marks this book's printer uses**, U+0E4C
(thanthakhat ์) or U+0E4E (yamakkan ๎). One answer fixes every one of them, and
they are all chanted lines. Everything entered on pages 51–60 uses ์.

**Page 60 is the best evidence so far, and it points at ์ (U+0E4C).** It carries
the mark five times — อะปัจจะเวกขิต์วา, ท์วายะ, พ์รัห์มะ, ยาต์รา, อัพ์ยา — and on
ท์วายะ it stands alone at the start of a line with nothing crowding it. At 11×
it is an ε-shaped curl with a tail, not the crescent of yamakkan. That is a
photograph reading well, not a verdict: it says what the printer cuts, and the
book in Josh's hands is still what settles กัล๎ยาณัง. Nothing was changed on it.

**Page 60 also found the opposite case.** The book prints **อุณหัสสะ with no
mark at all**, where standard editions have อุณ๎หัสสะ. Both occurrences were
checked at high magnification and neither is marked; both are stored unmarked.
Worth knowing that this printer omits the mark as well as cutting it, because
the omission is exactly what a reader would "correct" without noticing.

**The ฬ/พ hazard.** These photographs cannot tell ฬ from พ, and the failure is
not confined to body-text size. Proven **three times** against Josh's own
readings from the book: page 23 line 19, อะสัมมุฬโห on page 22, and — on
2026-08-21 — the chant TITLE อาสาฬหบูชา on page 75, which had been read as
อาสาพหบูชา at 6× in bold display type.

**A missing ascender is not evidence for พ.** That is what page 75 got wrong.
The presence of an ascender can still say ฬ, as it did for `เวฬุวะเน` on page
71; its absence says nothing at all. Ask the book.

Words written with ฬ as a **judgement, not a reading**:

- อะวิรุฬหิฉันทา — page 22
- ปีฬิตัสสะ — page 24
- วาฬะมิคานิ — page 29

**And the one that matters most.** Paṭiccasamuppāda writes the sense-bases word
as สะพายะตะนัง with พ at verses 4, 5, 16 and 17, and the photograph appears to
agree. Standard Pali is *saḷāyatana*, with ฬ. **Page 75 makes this likelier
still**: three photographic readings of this letter have now been overturned by
the book, all of them in the same direction — ฬ lost to พ. Josh's instruction to
"let the
photo win" was given for paste damage and **must not be applied here** — the
photograph is precisely what cannot settle this, and applying it would fix four
wrong readings permanently. Left untouched pending the book.

## Eight chants still print their colophon as a chanted verse

A closing formula — `<title> นิฏฐิตา.` — is printed as a centred colophon, and
the app has a `closing` field that renders it that way. Twenty-eight chants use
it. But **eight of the pre-page chants hold that line as their last VERSE**, so
the app numbers it and lists it as though it were chanted:

Tilakkhaṇādi (p27), Devatābhisammantana (p27), Mettānisaṃsasutta (p22),
Mettānisaṃsagāthā (p23), Pabbatopama (p30), Ariyadhana (p31), Buddhaudāna (p32),
Bhaddekaratta (p33).

Devatādissa was the ninth and is fixed — `IMG_0288.PNG` shows its colophon set
exactly like the one above it, which the app already held as a `closing`. The
other eight were left alone deliberately: their pages are on the "to verify"
list in the photo map, and **the page is the only thing that can say which page
the colophon is printed on.** Pabbatopama proves why — page 30 runs its verses
to the very foot, so its colophon is on page 31, and the app currently shows it
on 30. Fix them as each page is read, not in a sweep.

## Settled — do not re-open

- **Page 59 repeats itself, and the book is what repeats.** Its last line prints
  `ประธานกล่าวเชิญชวนว่า หันทะ มะยัง ทะสะนาถะกะระณะธัมมะสุตตะ` for the second
  time in three lines. Page 60's first line completes that sentence, so the
  duplication is the compositor's, not an artefact of the page turn. Page 59's
  text stays exactly as printed.
- Page 23 line 19 is **วิรุฬหะ** (Josh, against the physical book).
- Variant readings **do** get a field; it exists as of `b40c9c5`.
- **Pages 5 and 21 are on both the index and the contents**, as of `a97326d`
  and `169777f`. An earlier version of this file said their absence was "not a
  fault and settled". That was wrong and Josh was right to push back: the
  *book* names neither, because both are pages a chant continues onto rather
  than starts on — but the *app* could still reach them, and now does. A chant
  card shows every page it runs across (`pages 4–5`, `pages 20–22`), and a
  contents line offers a button for every page in its stretch.
- **`/chanting` states its coverage** — "Pages 1–31 and 217–221 are in so far",
  as runs rather than a count, because a count reads as a continuous range.

## Things learned the hard way, worth not relearning

- **A new chant is appended to the end of `CHANTS`**, so it lands at the foot of
  its page whatever its number. Down-page order is now settled by the book's own
  chant numbering where every chant on a page has one — but nothing orders the
  unnumbered ones, so check a multi-chant page renders top to bottom correctly.
- **A pre-page chant's `source` may cite the wrong chant entirely.**
  Pabbatopama's named page 30's two footnotes, which belong to the two chants
  above it. Suspect any `source` naming more than one reference.
- **Not every missing chant is one of the seventeen.** Ādiyasutta, numbered 13,
  had simply never been entered, between two chants that were both already in.
- **A Render deploy usually takes about a minute but has taken 15.** Check with
  `render deploys list srv-d8k5ucm7r5hc738qhcb0 -o json --confirm` rather than
  polling the live page and guessing.
- **The English of a reprinted text is copied from the earlier printing**, not
  written again. The evening service reprints a great deal of the morning one,
  and two glosses of the same Pali that differ in wording read as two different
  lines. Pages 52 and 54 take their English straight from the app's pages 2 and
  3 wherever the Pali matches, and note in a check where it does not.

## Two faults in `apply_batch`, fixed 2026-08-11

Both were cosmetic and both misreported rather than miswrote, which is why they
survived so long — the data was right every time.

- **`# ‼ COMPLETED FROM p?`** wrote a literal `?`. It read `verse['page']`, but
  a completing verse correctly has no `page` key: the line belongs to the page
  it STARTS on, which is the earlier one. The page it arrived FROM now comes
  from `page_of()`, which asks the batch's own page map and takes the later of
  the two rows claiming that verse. The four existing comments were backfilled
  to p35, p41, p47 and p52, each confirmed against the comment beside it.
- **`CONTINUES markers: n -> n` was counted around the removal only**, so a
  batch that finished one chant and opened another reported `1 -> 0` of a file
  that still held one. It is now counted over the whole run. The guard that
  refuses to claim a removal it did not make is unchanged and still local.

## Batch 9 is readable again — and what it turned up

`check_batch --all` used to fail on one file: the page-9 batch, whose checks
were written as plain strings before the shape was settled. Its six checks are
now objects, the seventh was dropped (it was a `‼ COMMENTARY PENDING` marker,
which `apply_batch` writes from `depth` and is not a check at all), and the
three that name a verse have been moved in `chanting.py` to sit above the verse
they are about instead of floating at the top of an eighteen-verse chant.

**Page 9 renders byte for byte identically** — proved by hashing it before and
after — and it already matches the book: instruction items 3, 4 and 5, then the
eighteen verses, then the closing editorial note, in that order, each once.

**But "readable" is not "safe to re-apply".** Diffing the file against what
`render_chant` would now produce turned up one real difference beyond the
comments: `kham-choen-bucha-phitsadan` carries `'group': 'Morning chanting'` and
the renderer hard-codes `'General chanting'`. Re-applying would quietly
downgrade it. Nothing reads `group` today — it is the only chant of 81 that does
not say `General chanting`, so it is an outlier rather than a treasure — but the
lesson generalises: **before re-applying any batch, diff it against the file
first.** The file wins, and the renderer does not know that.
