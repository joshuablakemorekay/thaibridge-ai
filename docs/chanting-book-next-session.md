# Chanting book — next session

Paste-ready brief for picking this work up cold. Updated 2026-08-24 after page
112 went in.

## Read first, in this order

1. `docs/chanting-book-photo-map.md` — the brief, read it fully
2. `prompts/chanting-book-batch/README.md` — the two-stage workflow
3. `C:\Users\joshk\OneDrive\Documents\Documents\Digital Chanting Book\chanting-book-batch-prompts.pdf`
   — the Stage 1 and Stage 2 prompts. **Read it before any fresh page read.**

## State — verify with git, don't take this file's word

- **Pages 1–112 are in and unbroken**, plus 217–221. **149 chants and 2,196
  verses in the Thai-script run**, and **NOTHING IS LEFT OPEN** — there is no
  `‼ CONTINUES` marker anywhere in `chanting.py`. `/chanting` derives its own coverage
  line, so it is never stale — read it rather than this bullet.
- ⚠️ **A SECOND SESSION IS WORKING IN THIS SAME CLONE**, on the ROMAN-SCRIPT
  pages (317, 318). It has `chanting.py`, `scripts/check_render.py`,
  `templates/chanting_page.html` and `tests/test_chanting_pages.py` open. Page
  94, 95 and 96's data is applied and verified but their `chanting.py` changes
  are NOT committed, because one file cannot be split between two sessions'
  commits — see below.
- ⚠️ **TEST RESULTS ARE MOMENTARILY UNRELIABLE while the other session is
  writing.** Page 96's run showed two failures that vanished on a re-run seconds
  later — they were mid-write on `chanting.py`. **Re-run before believing a red
  suite**, and check whether the failing names are theirs
  (`mahasamayasutta-roman`) before investigating anything.
- 11 of the 17 pre-page chants are verified against their photographs.
- Pages 92 to 112 were applied 2026-08-24/27; pages 83 to 91 on 2026-08-23; pages 78 to 82 on 2026-08-22; pages 75 to 77 on 2026-08-21;
  pages 69 to 74 on 2026-08-19; pages 66–68 over the days before them; 61–65 on
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

## Next: page 113, `IMG_0378` — ⚠️ A CHANT IS OPEN

The offset is **265** since page 86 and has held for 87–112, so page 113 *should*
be `IMG_0378`. **Five more changes are still expected before page 207.**

**⚠️ `aggappasada-suttam` IS OPEN and carries a `‼ CONTINUES` marker.** Two
paragraphs are in — the nidāna and the FIRST of the four foremost faiths (the
Tathāgata). **Resume at verse 3.** Page 112 ends at a **sentence** boundary, so
there is no `[…]` to complete: just append. Three faiths remain — the Path,
dispassion, and the Sangha — then a closing and probably a colophon.

## ⚠️⚠️ A VERSE THAT SPANS A PAGE TURN CAN ONLY LIVE ON ONE PAGE

Page 112 hit this for the first time and it cost an hour. **Read this before
completing any cut verse that is also a chant's LAST verse.**

The model says a verse takes `page` only where the printed page turns, so a
completing verse normally has none and renders on the page its paragraph
**began** on. That is fine — until the completing verse is also the last one and
the chant's **colophon and citation are printed on the far side of the turn**.
Then leaving the page off puts the colophon and citation on the EARLY page and
the later page shows nothing of the chant at all. `check_render` catches it.

**What to do:** mark the completing verse with the LATER page. Page 112 now
carries the paragraph, its colophon and its citation, exactly as the book does.
**The cost is real and must be recorded**: the earlier page no longer shows the
few lines of that verse the book prints there. Batch-111 keeps the cut text
quoted in a check so nothing is lost, and claims only verse 1 on its page row.

**A proper fix exists and is not done:** let `closing` carry its own page, or let
`build_page_index` emit a closing-only entry. Both touch shared template and
script code, so they were left for Josh.


## 🧾 The ฬ tally, and which places rest on what

Fifteen places now. **Four were read at the book by Josh** (85, 95, 99, 102);
the rest are the rule applied. Page 111's `สัมมุฬโห` is the best-supported of
the rule-applications — the app already holds `อะสัมมุฬโห`, the same word
negated, **from Josh's own typing** at `mettanisamsa-sutta` v19, so the book's
own spelling of its own word agrees. It is still recorded as a rule-application,
because this page has not been checked.

If a spot-check is ever wanted, `สัมมุฬโห` on page 111 is now the cheapest one
to confirm, since a disagreement there would also contradict something already
typed from the book.


## ‼ A colophon that does not agree with its own noun

Page 110 prints **`มัคคะวิภังคะสุตตัง นิฏฐิตา`** — `นิฏฐิตา` is **feminine**,
but `สุตตัง` is neuter and takes `นิฏฐิตัง`, which is what every other `สุตตัง`
colophon in this book prints.

It is not a house style. Four lines below on the SAME sheet,
`อัฏฐังคิกะมัคคะคาถา นิฏฐิตา` is **correct**, because `คาถา` is feminine — and
page 62 got the same agreement right. So the book is simply inconsistent here.
Both reproduced as printed; **do not "fix" the ending.**


## ‼ Right action is given in its MONASTIC form

Page 109's third abstention is `อะพ์รัห์มะจะริยา` — unchastity — where the lay
formulation has `กาเมสุมิจฉาจารา`, sexual misconduct. **Three abstentions, not
four.** That is not an omission: it is the version for those gone forth, and this
is a monastic chanting book. Reproduced as printed, and recorded because the
missing fourth item looks like a dropped line.


## 📐 The prose unit is whatever the SHEET offers — check the indents first

Pages 106–108 are three answers to the same question and all three are right:

| page | what the sheet does | unit used |
|---|---|---|
| 106 | one paragraph, only line 1 indented | the **full stop** |
| 107 | two paragraphs, both openers indented | the **full stop** inside each |
| 108 | **five** paragraphs, all five openers indented | the **paragraph** |

So: **measure the indents before choosing.** Where the book paragraphs its prose,
the paragraph is the unit; where it does not, the sentence is the only unit on
offer. Do not carry a decision across from the previous page — the same chant
style is set differently on different sheets.

## ✅ `นานาวิเธหุปาเยภิ` is NOT a misprint

Page 108's `บทขัด` verse 7 ends in **ภิ** where `-ehi` is expected. Read at 7×;
the letter is unmistakably ภ. **Pali has two instrumental plural endings, `-ehi`
and `-ebhi`, and both are canonical** — so `upāyebhi` is correct and must not be
"corrected" to `หิ`. Recorded because it looks exactly like the kind of slip a
later pass would tidy away.


## ⚠️ อะภิณหะปัจจะเวกขะณะ — FOUR spellings of one title across two sheets

Now settled and closed, but recorded because it is the clearest case in the run
of the book disagreeing with itself, and nothing was harmonised:

| where | prints |
|---|---|
| p106 `บทขัด` title | `อะภิณหะ` … `ปาฐะ` |
| p106 `บทขัด` verse 2 | `อะภิณ์หัง` |
| p106 numbered title (17.) | `อะภิณ์หะ` … `ปาฐะ` |
| p106 prose, ×8 | `อะภิณหัง` |
| **p107 colophon** | `อะภิณหะ` … **`ปาโฐ`** |

The **colophon agrees with the สารบัญ and the heading does not** — which is why
the numbered chant is one of the titles the contents test cannot see.

## 🔗 Joining a cut line keeps exposing punctuation the page break hid

Twice now, and worth expecting a third time. Page 104's join showed the two
halves of item 2 differing by a comma; page 107's shows `ปาปะกัง วา ตัสสะ` with
NO comma where page 106's same formula has one. **When you complete a cut verse,
re-read BOTH halves against their sheets** — the difference is only visible once
the sentence is whole.


## ⚠️ Page 106: ONE WORD, THREE SPELLINGS, ONE PAGE

This sheet is the worst case so far for the book contradicting itself, and every
form is reproduced as printed:

| where | prints |
|---|---|
| `บทขัด` **title** | `อะภิณหะ` — bare ณ |
| `บทขัด` **verse 2** | `อะภิณ์หัง` — with the cluster mark |
| numbered **title** (17.) | `อะภิณ์หะ` — with the mark |
| the **prose**, 8 times | `อะภิณหัง` — bare, throughout |

And separately, `พ์ยาธิ` / `พยาธิ`: verse 3 sets the pair as
`พ์ยาธิธัมโมมหิ พยาธิง` — mark on the first, none on the second — while verse 9
sets both WITH the mark. Each read at 5–6× before being written down.

**Do not harmonise any of it.** The lesson is the same one page 102's
`ตุย์หัง` / `ตุยหัง` taught: the cluster mark is not applied consistently by this
printer, and a tidy-up would be inventing a book that does not exist.

## ✂️ A hyphen can split a word across the COLUMN GUTTER

New on page 106 and worth knowing. In the `บทขัด`'s row 5, the LEFT column ends
`เตสัมปะกาสะกัง ธัมมะ-` and the RIGHT column of the same row opens `ปะริยายัง`.
Read across, the word is `ธัมมะปะริยายัง`. Rejoined, exactly as page 102's seven
line-break hyphens were — but check for this at the gutter as well as at line
ends from now on.


## ✅ The Thai-colophon bug is FIXED — and the two kinds are different

`templates/chanting_page.html` now gates the closing block on
`closing.pali OR closing.thai`, with the pali line conditional, so a **Thai**
colophon renders without having to be duplicated into `pali`. The eleven
doubled colophons on pages 38–47 are corrected and each prints once.

**But note which mechanism a จบ line belongs in — they are NOT the same:**

| what it closes | where it goes | example |
|---|---|---|
| **one chant** | `closing` on that chant | `จบพระวิภังค์` closes the Vibhaṅga, page 40 |
| **a whole section** | `service_closing` on the PAGE ROW | `จบสิบสองตำนาน` closes the Twelve Tamnan, page 103 |

Page 103's line closes the SECTION, so `มงคลจักรวาฬใหญ่` itself gets **no**
colophon — the same treatment page 41 gave `จบสวดแจงเท่านี้`. Its optical centre
measures x 984 against 977 and 982 for the sheet's two bold titles, which is how
it was identified as a centred heading rather than body text.


## ❗ This section cites AUTHORS, not the canon — and its numbering RESTARTS

Two findings that arrived together on pages 100 and 101, and both will keep
mattering.

**1. `source_printed` now holds two different kinds of thing.** Every footnote up
to page 97 was a Tipitaka reference (`สํ.ส. 15/320`). Pages 100 and 101 both
print an AUTHOR instead:

| page | chant | the footnote says |
|---|---|---|
| 100 | `ระตะนัตตะยัปปะภาวาภิยาจะนะคาถา` | `พระราชนิพนธ์ในพระบาทสมเด็จพระจอมเกล้าเจ้าอยู่หัว` — King Mongkut |
| 101 | `สุขาภิยาจะนะคาถา` | `สมเด็จพระพุทธโฆษาจารย์ (ฉิม) วัดมหาธาตุ รจนา` — Somdet Phra Buddhaghosacariya (Chim) |

Two in a row is not a one-off: these are **Siamese compositions, not canon**, so
an author IS their source. Both go in `source_printed` — the template renders it
as a plain footnote under a rule, with no wording of its own, which is exactly
what the page prints. Expect more of them through this section.

**2. ⚠️ `book_number` IS NOT UNIQUE, AND MUST NOT BE MADE UNIQUE.** The book
restarts its numbering by section, so:

- printed `13` = `อาทิยะสุตตะคาถา` (page 30) **and** `ระตะนัตตะยัปปะภาวาภิยาจะนะคาถา` (page 100)
- printed `14` = `ปัพพะโตปะมะคาถา` (earlier) **and** `สุขาภิยาจะนะคาถา` (page 101)

Both pages print the number, so both keep it. Any future test asserting a unique
`book_number` would be asserting something **the book does not do**.

## 📏 Measure indents against a FITTED BASELINE, not a fixed threshold

Page 100 made this unavoidable and it is the right method from now on. That
sheet's block left edge **drifts 65px down the page** — 478 at the top row, 541
at the bottom — because the page curves away from the camera. A fixed threshold
calls the lower half indented and is simply wrong. (Page 94 was the earlier
version of this mistake, where page 83's absolute `x >= 760` reported all 26
rows as indented.)

**What to do:** take the left edge of every row, fit a straight line through the
rows you believe are NOT indented, then look at the residuals. On page 100 the
fit was `x = 0.0343*y + 464`; rows 2–22 sat on it within 8px and verse 1 stood
**+138** clear. That is an unambiguous answer, and it takes one short script.

## 🐛 OPEN BUG — 11 Thai colophons are printed TWICE (pages 38-47)

Found 2026-08-24 when Josh said he could see no paiboon anywhere. **Not fixed —
raised with him and left for his call.**

The book prints `จบพระวิภังค์` ("Here ends the Vibhanga") as ONE centred line
closing the chant. The app renders it as two:

    จบพระวิภังค์          <- layer-pali
    จบพระวิภังค์          <- layer-thai   (the same line again)
    jop pra-wi-pang        <- paiboon

**Why it happened:** `templates/chanting_page.html` gates the whole closing block
on `chant.closing.pali`, so a Thai-only colophon would not render at all unless
its text were ALSO put in `pali`. Duplicating it was the only way to make it show.

**The 11**, all in the สวดแจง section: `phra-winai-sangkhep`,
`phra-sut-sangkhep`, `phra-sangkhani`, `phra-wiphang`, `phra-thatukatha`,
`phra-pukkhalabanyat`, `phra-kathawatthu`, `phra-yamaka`, `phra-mahapatthan`,
`thammasangkhani-matika-patho`, `mongkhon-chakkrawan-noi`. The other 41 closings
are Pali (`…นิฏฐิตา`) with `thai` empty and are CORRECT — do not touch them.

**The fix, when Josh says go:** widen the template condition to
`chant.closing.pali or chant.closing.thai`, render the pali line only when there
is one, then move those 11 lines out of `pali` into `thai` alone. Open question
he has not answered: whether a Thai colophon should keep its `paiboon` (my
inclination: yes, it is Thai the book prints).

⚠️ This also means the app's ONLY genuine five-layer content is pages 217-221
(59 lines). The 16 "paiboon lines" on pages 10-47 are mostly these duplicates.

## ❗ The book has a SECOND, TRANSLATED pass — it starts around page 191–193

Sampled 2026-08-24 after Josh asked why no page carries a `paiboon` line. The
answer is that this book is printed in **two passes over the same material**:

| pages | what is printed | layers filled |
|---|---|---|
| 1 – ~190 | the chants in **Pali only** | `pali`, `pali_roman`, `english` |
| ~193 – 221+ | the same chants again, **สวดแปล** — Pali line, Thai translation beneath | all five |

`IMG_0462` is a divider page: bold **`บทสวดมนต์`**, with
**`ทำวัตรเช้าแปล`** showing through from its reverse. Pages 120, 155 and 189
were checked in the untranscribed middle and are Pali only; 194, 195, 200, 212,
217 and 218 all carry the translation. **The exact boundary page still needs
reading off the sheet** — it was narrowed by sampling, not measured.

**Do not read “no Thai translation is printed” on pages 67–98 as a fact about the
book.** It is a fact about the FIRST pass. `thai` and `paiboon` are empty there
because the page prints no Thai, exactly as the prompt requires — and they will
start filling by themselves once the run reaches the translated section.

⚠️ **DECIDE BEFORE PAGE ~193, NOT AFTER.** The translated section covers chants
the app ALREADY HAS from the first pass. Keeping the book exactly as printed
means they become SECOND ENTRIES — the book prints them twice, so the app shows
them twice — rather than back-filling `thai` into the existing entry. That is
Josh's call and it changes how every page from there on is applied.

## ⚠️ Two sessions, one `chanting.py` — what happened on page 94

A second Claude session is working the **roman-script** end of the book (pages
317, 318) in this same clone. When page 94 was applied, `chanting.py` held both
sessions' work at once, plus that session's changes to `check_render.py`, the
page template and a test.

**Page 94 was applied and fully verified — four checks green, suite 1,324, page
renders correctly — but its `chanting.py` change was left UNCOMMITTED.** Only
`batch-094-094.json` and the docs were committed. Committing the shared file
would have swept the other session's in-progress chant into a "page 94" commit
under the wrong message, without the template and test changes that go with it.

**So the docs may read one page ahead of what `chanting.py` has committed.** The
data is regenerable at any time: `python scripts/apply_batch.py
prompts/chanting-book-batch/batches/batch-094-094.json`.

**The durable fix is a git worktree** so the two sessions stop sharing a working
tree. Offer it before starting another long run alongside someone else.

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

## ⚠️ Page 93 — the book's own typesetting speaks to the ส์ question

Page 93's **second footnote** reads `โกฏฺิโย อยํ หิ อิตฺถีลิงฺคํ` and it is set
with the **PHINTHU** (`◌ฺ`, U+0E3A) — the subscript dot — on `ฏ`, on `ต` and on
`ง`.

**The body of this book never uses phinthu.** It marks its clusters with the
small mark ABOVE, as in `สัก์ยะปุตตัสสะ` on verse 7 of this very page.

So **the printer has phinthu and chooses not to use it in the chanted text.**
That is the first evidence about the `ส์วากขาโต` question that comes from the
book's own typesetting rather than from magnifying a glyph, and it is worth
weighing alongside page 60's reading of `ท์วายะ`. It does not settle which mark
the body uses — `์` or `๎` — but it does say the choice is deliberate.

## Page 93 — a third footnote whose other half cannot be shown

The same footnote gives a **reading** (`โกฏฺิโย` for the line's `โกฏะโย`) **and**
a grammatical note (that form is feminine). Only the reading has a field; the
grammar is lost.

**Third instance of the same gap**, after page 76's conditional footnote ("use
`อิมัง ปะฏิมัง` if a Buddha image is the principal") and page 77's. **A `note`
field on a variant would close all three** — one key in `apply_batch`, one line
in each of the two templates.

## Page 92 — one field cannot hold two printings

The Dhajagga Sutta's citation is printed on **both** page 90 and page 92, with
the same odd range and **different spacing**:

| page | prints |
|---|---|
| 90 | `สํ.ส. 15/320-223` — unspaced |
| 92 | `สํ. ส. 15/320-223` — spaced |

Both read at 5×. `apply_batch` **adds only and never overwrites**, so the chant
kept page 90's value and page 92's was silently not written. **That is the right
behaviour** — the first reading wins, as with any merge — but `source_printed`
is a single field and cannot hold both, so the app shows the unspaced form while
page 92 prints the spaced one. Recorded in a check rather than forced.

**The range matters more than the spacing.** `320-223` runs *downward*, where
standard references have `320-323`. That the same odd number appears on **two
separate sheets** makes it the book's consistent reading rather than one
compositor's slip — worth knowing before anyone "corrects" it.

## Page 92 — a cluster mark stranded by a line break

Line 3 ends `อิทัง วัต` and line 4 **opens with a bare `์`** before `วานะ` — the
mark belongs on the `ต` at the end of the previous line. Read at 5×: it sits
alone at the line start with clear paper around it. Rejoined as `วัต์วานะ`.

A new kind of break for this book — not a hyphen, but a **combining mark
orphaned onto the next line** — and one that would be invisible as a fault once
it was in. Watch for it wherever a line ends on a consonant that should carry a
cluster mark.

## ⚠️ para_layout goes on the first verse OF THIS PAGE, not of the batch

Page 91 got this wrong **twice** before rendering caught it, and page 75
established the rule in the first place. Worth stating exactly:

- A chant with **no chant-level `layout` key** falls back to `lines`. A prose
  chant that relies on the default renders as a stack of short lines.
- The template reads `para_layout` off **`paragraph[0]`** — the first verse of
  the group *in the slice being rendered*.
- So when a page opens **mid-paragraph**, the first verse on that page needs
  `para_layout` and **no** `para_start`.
- **The verse that needs it is the first one whose `page` is this page** — not
  the first verse in the batch. Page 91's batch opens at verse 20, but verse
  20's line *starts on page 90*, so it is not in page 91's slice at all. The fix
  had to go on verse **21**.

**None of the four checks sees this.** `check_pages` compares data to the batch,
`check_render` walks strings in printed order and does not look at grouping.
Only opening the page catches it — so open the page.

## ✅ SETTLED 2026-08-25 — THE TYPEFACE PHOTOGRAPHS ฬ AS พ. TRUST THE CANON.

**Josh read pages 85 and 99 off the physical book and both are `ฬ`.** That ends
the question this run carried for eighteen pages, and it ends it against the
reading I had been defending.

| page | photograph showed | the BOOK has |
|---|---|---|
| 85 | `อะวิรุพหิฉันทา` | **`อะวิรุฬหิฉันทา`** (*avirūḷhi*) |
| 99 ×3 | `วิรุพโห` / `วิรุพหา` | **`วิรุฬโห` / `วิรุฬหา`** (*viruḷho / viruḷhā*) |

**Why the photographic evidence was worthless, and why it looked so strong.**
Page 99 was offered as the cleanest test the book had given: the disputed letter
sat on the same line, at the same size, three words from the `พ` of
`พุทธะสาสะเน`, and at 4× the two were identical. That argument is circular. **If
the typeface renders ฬ so that it photographs as พ, then a same-line comparison
with a real พ shows a match either way.** It cannot discriminate, and every
"identical at N×" note in the batch records has the same flaw.

### THE RULE FROM NOW ON

- A bare letter that *photographs* as `พ` where **standard Pali has ḷ** is a
  **`ฬ`**. Write `ฬ`. Do not "reproduce the พ as printed" — the พ is a camera
  artefact, not what the page prints.
- The **canon is the tiebreaker**, not the glyph. This is the one place in the
  whole run where the photograph is overruled by default.
- ⚠️ **This does NOT make every พ into ฬ.** Where standard Pali genuinely has
  `b`, the letter is a real `พ`. Recorded example, do not touch it:
  `พาละมิคา` (*bālamigā*, "young beasts") in `chaddanta-parittam` v8, page 88.
- A visible **tall ascender** is still positive proof of `ฬ` (pages 76–80, and
  `เวฬุวะเน` on pages 33/34/36/71). Its **absence proves nothing**.

### ✅ ALL FOURTEEN PLACES ARE NOW ฬ — the sweep is complete

Josh confirmed **four pages** directly at the book: 85, 95, 99 and 102. The
remaining six places were changed on the strength of the rule those four
established, and are listed here so it is clear which rest on a reading and
which on the rule.

| page | chant | verse | now reads | confirmed how |
|---|---|---|---|---|
| 31 | `ปะฏิจจะสะมุปปาทะปาโฐ` | 4, 5 | `สะฬายะตะนัง` | by rule |
| 32 | `ปะฏิจจะสะมุปปาทะปาโฐ` | 16, 17 | `สะฬายะตะนะ` | by rule |
| 85 | `ระตะนะสุตตัง` | 74 | `อะวิรุฬหิฉันทา` | **read at the book** |
| 90 | `วัฏฏะกะปะริตตัง` | 8 | `โสฬะสะ` | by rule |
| 95 | `อาฏานาฏิยะปะริตตัง` | 60 | `วิรุฬหะโก` | **read at the book** |
| 97 | `โพชฌังคะปะริตตัง` | 11 | `เคลัญเญนาภิปีฬิโต` | by rule |
| 99 | `ชะยะปะริตตัง` | 13, 15, 17 | `วิรุฬโห` / `วิรุฬหา` | **read at the book** |
| 102 | `มงคลจักรวาฬใหญ่` | 1 | `ฉะฬะภิญญา` | **read at the book** |

Each had its `pali`, its `pali_roman` and its batch record changed together, and
the stale `‼ CHECK` comments that argued for `พ` have been rewritten in place —
leaving them would have had `chanting.py` narrating a conclusion its own data
contradicts.

**The app no longer contradicts itself.** `อะวิรุฬหิฉันทา` is printed on both
page 22 and page 85 and now reads the same in both.

## Page 90 — a citation that looks transposed

The footnote reads `สํ.ส. 15/320-223` — a range running **downward** from 320 to
223. Read at 4×; the digits are unambiguous. Standard references for the
Dhajagga Sutta run **15/320-323**, so this looks like a compositor swapping 3
and 2.

**Reproduced verbatim**, because the book is the authority — but flagged,
because a wrong citation is a wrong reference in a book about the Dhamma. **One
of the clearest things on the page to check.**

## Page 89 — the Mora Paritta closes with NO citation

Every paritta in this stretch has carried a footnote citation: Maṅgala (p82),
Ratana (p86), Karaṇīya-metta (p87), Khandha (p88). **The Mora Paritta has
none** — no marker and no footnote on page 88's portion or on page 89, and the
whole foot of page 89 was profiled to be sure.

`source_printed` is left OFF rather than guessed. **Worth a glance at the book**
to confirm nothing was missed at the foot of either sheet.

## Page 89 — two stanzas, two words apart

The Mora Paritta's sunrise and sunset stanzas are the same four lines with
**two words changed**: `อุเทติ`/`อะเปติ` (rises/sets) at the opening, and
`ทิวะสัง`/`รัตติง` (day/night) at the fourth line. The three-line refrain that
follows each is word for word identical.

So the page carries six verbatim-repeated lines, and that is the book, not a
paste error.

**One line is shared between two different chants for a real reason:** page 88's
Mora preface and page 89's Vaṭṭaka preface both open `ปูเรนตัมโพธิสัมภาเร` —
both are Jātaka-birth prefaces and they share the formula.

## ⚠️ Page 88 — one colophon closes TWO chants

The line printed centred at the middle of page 88 reads
`ขันธะปะริตตัง ฉัททันตะปะริตตัง นิฏฐิตัง.` — **naming both parittas**. The
Khandha Paritta ends at the top of that same sheet; the Chaddanta ends
immediately above the line.

**Recorded as the CHADDANTA's `closing`**, because that is the chant it directly
follows, and **the Khandha Paritta is deliberately left with no `closing` of its
own** even though the line names it. Attaching it to both would print the same
line twice on one page.

First colophon in the book that closes a pair. **Worth Josh's eye** — if he
would rather the Khandha Paritta also carried it, the fix is one key, but the
page would then show it twice.

## Twelve titles the contents test cannot see — pages 80, 82, 86–90, 92, 96–99

This is now the RULE for a `บทขัด`, not a run of surprises: from page 82 on,
every single one of them is spaced on the page and unspaced in the table.
Each time the page heading and the book's own สารบัญ differ, the **page** is
reproduced, and `title_thai` therefore stops being a key in
`chanting._CONTENTS_ROMAN` — so `test_the_table_and_the_chants_never_spell_one_title_two_ways`
cannot see that chant at all, and nothing will warn if its title drifts later.

| page | the page prints | the สารบัญ has |
|---|---|---|
| 80 | `บทขัดมังคะละสุตตะ` (`สุตตะ`) | `บทขัดมังคะละสุตตัง` (`สุตตัง`) |
| 82 | `บทขัด ระตะนะสุตตัง` (spaced) | `บทขัดระตะนะสุตตัง` |
| 86 | `บทขัด กะระณียะเมตตะสุตตัง` (spaced) | `บทขัดกะระณียะเมตตะสุตตัง` |
| 87 | `บทขัด ขันธะปะริตตัง ฉัททันตะปะริตตัง` (spaced, `ปะริตตัง`) | `บทขัดขันธะปะริตตัง ฉัททันตะปะริตัง` (`ปะริตัง`) |
| 88 | `บทขัด โมระปะริตตัง` (spaced) | `บทขัดโมระปะริตตัง` |
| 89 | `บทขัด วัฏฏะกะปะริตตัง` (spaced) | `บทขัดวัฏฏะกะปะริตตัง` |
| 90 | `บทขัด ธะชัคคะสุตตัง` (spaced) | `บทขัดธะชัคคะสุตตัง` |
| 92 | `บทขัด อาฏานาฏิยะปะริตตัง` (spaced) | `บทขัดอาฏานาฏิยะปะริตตัง` |
| 96 | `บทขัด อังคุลิมาละปะริตตัง` (spaced) | `บทขัดอังคุลิมาละปะริตตัง` |
| 97 | `บทขัด โพชฌังคะปะริตตัง` (spaced) | `บทขัดโพชฌังคะปะริตตัง` |
| 98 | `บทขัด อะภะยะปะริตตัง` (spaced) | `บทขัดอะภะยะปะริตตัง` |
| 99 | `บทขัด ชะยะปะริตตัง` (spaced) | `บทขัดชะยะปะริตตัง` |

Page 87's differs **twice** — the space and a doubled `ต`. Where the page and
the table disagree, `title_roman` is composed to match the PAGE rather than
taken from the table.

**One look at the สารบัญ settles all four**, and it is worth doing before the
list grows.

## Page 86 — the orphan marker stays orphaned

Page 85's last line carries a superscript **1** with no footnote on that sheet.
Page 86 has **its own** superscript 1 on verse 89 **and its own footnote** under
the rule, so the pair on page 86 is complete and internal.

**They were NOT joined.** Footnote numbers restart on every page and the
standing rule is never to match a marker to a footnote on a different sheet.
Page 85's marker is left unattached and nothing was written for it. Same shape
as the orphan across pages 57–59 — **one look at the book settles both at
once**.

The citation itself is worth noting for a different reason: this one prints
`ขุ.สุ.` with **no space** where page 82's printed `ขุ. สุ.` with one. Both
reproduced as their pages set them.

## Page 86 — a third title the contents test cannot see

`บทขัด กะระณียะเมตตะสุตตัง` is **spaced** on the page and **unspaced** in the
สารบัญ — exactly what page 82's Ratana preface did. The page is reproduced, so
`title_thai` is not a key in `_CONTENTS_ROMAN` and nothing will warn if that
title drifts. **Three titles are now in that position** (pages 80, 82, 86).

## ⚠️ Page 85 — the ฬ/พ tests disagree for the first time

Verse 74 prints **`อะวิรุพหิฉันทา`**, and this is the most consequential reading
of the run so far.

**For พ:** the letter is **bare** — no cluster mark — and at 11× beside the `พ`
of `พีชา` **on the same line** it is identical in shape and height: two humps,
no ascender at all. Pages 76, 77, 78 and 80 each showed a bare `ฬ` carrying an
obvious tall ascender at far lower magnification.

**For ฬ:** standard Pali is *avirūḷhi*, "regrowth". The printed form gives
*avirubhi-*, which is not a word, so page 79's non-word test says the reading is
wrong. And **the app already holds this identical stanza a second time** — in
`parittakarana-patha` verse 10 — spelt `อะวิรุฬหิฉันทา`, a reading the list at
the foot of this file records as **a judgement, not a reading**.

**The page is reproduced as printed**, per the standing rule, so the app now
holds the word both ways in two chants. `parittakarana-patha` was NOT touched.
**One look at the book settles both at once**, and the two entries hold the same
five lines so they can be compared side by side.

The vowel differs too — this page has a short `ุ` where editions have long *ū* —
and belongs to the same question.

## Page 85 — an orphan footnote marker

The last line carries a superscript **1** and there is **no footnote anywhere on
the sheet**: profiled the whole foot, no rule and no text between the last verse
and the page edge. `source_printed` is left OFF rather than guessed. Same shape
as the orphan across pages 57–59. See the page-86 note above.

## What page 84 caught — an indent is relative, not absolute

The first attempt to find page 84's stanza openings reused page 83's absolute
threshold (`x >= 760`) and reported **every one of the twenty-six lines as
indented**, because this sheet's whole text block sits further right than the
one before it.

**The rule: profile the block's own left edge first, then measure the indent
against that.** Page 83's body starts at x 630–640 and indents to x 720; page
84's starts at x 870–880 and indents to x 960. Both are the same ~90px indent
and neither shares a threshold with the other.

It failed loudly rather than quietly — twenty-six indents is obviously wrong —
but the same mistake with a threshold that happened to land inside the block
would have marked a few real lines and missed the rest, and nothing downstream
checks stanza grouping.

## What page 83 caught — a chant can lose its CONTINUES silently

**A chant that arrives mid-way AND leaves mid-way needs BOTH keys.**
`continuation_of` tells `apply_batch` where to append; **`continues: true`
tells it to leave the `‼ CONTINUES` marker in place.** Page 83's batch listed
the sutta in `batch_status.continues` and left `continues` off the entry, so
the marker came off and a two-thirds-entered sutta read as finished.

**Nothing caught it, and that is the point.** `check_cut_lines` only fires
where a line ends in `[…]`, and this line was whole — it was the *sentence*
that carried on. So the one existing guard on continuation was blind to
exactly the common case: a chant that continues without a cut line.

**`check_batch` now has `continues agree`**, which checks both directions —
listed-but-not-declared and declared-but-not-listed. It passes on all 83
existing batches, so no earlier page has this fault, and it was negative-tested
both ways before being trusted.

## Raised on page 83 — a letter the photograph cannot show

**`ทัฬ์เหนะ` at verse 30 is recorded with ฬ, and the image did not decide it.**
It is the marked-ฬ configuration page 76 proved unreadable — a `ฬ` carrying the
`์` cluster mark loses its ascender in this printing and cannot be told from
`พ`. The deciding test is page 79's: **`พ์` + `ห` is not a legal Pali cluster**,
so `พ` gives *dabhena*, which is not a word, while `ฬ` gives *daḷhena* — firm —
which is what `manasā daḷhena` means.

**This is the first reading in this run settled by something other than the
photograph**, and it is flagged as such in the data. Every marked `ฬ์` from here
on needs the book.

**The stanza indents are on page 83 and not on page 82.** Measured on both
sheets: page 83 indents every stanza opening by 90px, page 82 indents none.
Each page is reproduced as it prints, so the grouping looks uneven in the data
— and that unevenness is the book's, not an omission.

## Raised on page 82 — the first colophon in the whole stretch

**`มังคะละสุตตัง นิฏฐิตัง.` is printed centred under the sutta**, so that chant
takes a `closing` at last. **Every chant since page 64 has had the key left off
because the book printed none**, and the absence had begun to look like a rule
of this book rather than a fact about those pages. It is not. Look for a
centred `จบ…` or `…นิฏฐิตัง.` under every chant from here on.

**A citation carrying TWO references.** `ขุ. ขุ. 25/3 ขุ. สุ. 25/376` — the
Khuddakapāṭha and the Suttanipāta, both printings of the same sutta. Reproduced
verbatim as one string, neither split into two fields nor expanded.

**A second hyphen across a gutter**, after page 79's. The left column ends
`โรคามะนุสสะทุพภิกขะ-` and the right opens `สัมภูตันติวิธัมภะยัง`. Rejoined,
hyphen dropped. It settles that block's two-column reading on its own.

**A second title the contents test can no longer see.** The page prints
`บทขัด ระตะนะสุตตัง` with a SPACE; the สารบัญ has `บทขัดระตะนะสุตตัง` without
one. The page is reproduced, so `title_thai` is not a key in
`_CONTENTS_ROMAN` and nothing will warn if that title drifts. Page 80's
`สุตตะ`/`สุตตัง` did the same. **Two of the last three pages.**

**Three settings on one sheet** — two-column, prose-then-two-column, and
centred single column. Third page running where profiling each block separately
was the only thing that caught it.

## Raised on page 81 — the ragged gutter

**The right column starts at exactly x 1080 on all twenty rows; the left half
is ragged.** So the empty band between the columns is anywhere from 100px to
300px wide depending on how long the left half runs. Measured row by row.

That matters for the method: **a gutter is not always a fixed band.** What is
constant is where the RIGHT column starts, and that is the thing to measure.
Looking for a uniform-width gap would have found nothing here.

**The refrain `เอตัมมังคะละมุตตะมัง.` repeats nine times, verbatim**, always as
the right half of its row. Expected in a litany, and exactly the shape that
reads as a paste error.

**This title agrees with the contents, where page 80's did not.** The sutta
prints `มังคะละสุตตัง` with `สุตตัง`, matching the สารบัญ; page 80's preface
printed `บทขัดมังคะละสุตตะ` with `สุตตะ` against it. So that inconsistency sits
between a preface and its own sutta rather than running through the book.

## Raised on page 80 — a title the contents disagrees with

**The page heading and the book's own สารบัญ spell one title two different
ways.** The page prints `บทขัดมังคะละสุตตะ` ending **สุตตะ**; `CONTENTS` —
built from the สารบัญ — lists `บทขัดมังคะละสุตตัง` ending **สุตตัง**. Read at
2.3× on the bold heading: the last syllable is plainly `ตะ`.

The page is reproduced, so `title_thai` ends `สุตตะ` and `title_roman` is
composed to match (`bòt-kàt maŋ-ká-lá-sùt-dtà`) rather than taken from the
table. **One consequence worth knowing: the contents test cannot catch this
title**, because the two strings no longer match, so nothing will warn if it
drifts. Fourth spelling disagreement in nine pages, after 72, 76 and 78.

**The gutter MOVES inside one chant.** `บทขัดต้นตำนาน` has its gutter at
x 810–900 for its first four rows and at x 1060–1240 for the remaining eight,
because the metre changes half way. Each row was profiled separately at 10px
steps; profiling the block once would have shown a single smeared column and
hidden the shift entirely. **Profile rows, not blocks, wherever the line
lengths change.**

**Verses 3 and 4 of `บทขัดต้นตำนาน` carry the least certain English on the
page** — the sentence runs across both rows and the syntax is compressed even
for this book. Flagged as a working translation rather than a settled reading.

**Two more `ฬ`**, both `จักกะวาฬ-`, both proven on their own line against the
`พ` of `สัพเพสุ` sitting beside them. The method is now routine.

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

⚠️ **Page 85 turned one of these the other way.** It prints
`อะวิรุพหิฉันทา` with a bare `พ` that is indistinguishable from the `พ` beside
it, where `parittakarana-patha` verse 10 holds the identical stanza with `ฬ`.
Both are kept as their pages print them; see the page-85 section above.

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

---

# The BACKWARD pass — the roman section at the back of the book

Everything above describes the FORWARD pass, which is at page 96 and climbing.
A second pass now works **backwards from the last page**, and the two will
eventually meet. This section is its state carrier; do not read the "Next"
heading above as applying to it.

## Where it is

**Pages 312–325 are IN and unbroken**, all entered 2026-08-24:

| pages | chant | verses |
|---|---|---:|
| 312–316 | `yod-phrakantraipidok` | 86 |
| 316 | `vipassit` | 1 |
| 317–325 | `mahasamayasutta-roman` | 192 |

All three are complete and **no CONTINUES marker is left anywhere in the file**.

**Resume at page 311 = `IMG_0578`, but READ THE NUMBER off the sheet.** Page 311
is the END of the Jinapañjara — verses 9 to 15, closing `carāmi jinapañjareti`
— so the next unit is that chant, and its opening page has to be found by
reading backwards until a title appears. The offset is 267 here.

## ⚠ Two open questions for when the book is in hand

Neither blocks further work, but both are cheaper to settle now than later.

1. **Is `VIPASSIT` a title or a closing label?** It is centred, capitalised,
   with white space above and one centred line below — set exactly like the
   page-312 title, which is why it was entered as its own chant. But it carries
   no bracketed English gloss where that title does. If the book says it belongs
   to the chant above, fold it in as a `closing` and drop the separate entry.
2. **The invocation material on 314–316 cannot be checked by sense.** Heart
   syllables (`sosososasa`, `a-a-a-a-ni`, `ma-a-u`) are abbreviations where each
   letter stands for a phrase, and words like `buddhapapha`, `puyapaka`,
   `hetupova`, `vinapañca` and `kalākara kanā` have no reading to check against.
   They are transcribed exactly as set. These are the lines that most need
   the printed page.

## Read `docs/chanting-book-photo-map.md` first

It now carries three things this pass established, and they matter more than
the page count:

1. **Three pages between 224 and 316 were never photographed.** 91 contiguous
   files for 94 pages. They leave no filename gap, so only reading page numbers
   will find them.
2. **Pages 309–325 are roman-script and the สารบัญ never names them.** The
   contents cannot tell you where a chant starts down here.
3. **A chant can be in the book twice, in two scripts.** Mahāsamaya is at 175
   in Thai and 317–325 in roman. The roman one is `mahasamayasutta-roman`.

## What the roman section broke, and what now handles it

Three things assumed Thai script and had to be fixed before a roman page could
go in at all. All three are committed; they are listed so nobody re-discovers
them the hard way.

* **Book mode hid `pali_roman`**, so a roman-only sheet rendered BLANK. The
  template now shows a roman line where the book itself set it, judged by the
  page: no `pali` means there was no Thai to romanise.
* **`check_render` walked `verse["pali"]`**, which is empty here, so it reported
  `pages rendered: 0` and then printed PASS. A blank page certified correct.
  It now falls back to the roman layer, one-directionally.
* **The contents-reachability test could not hold**, because the สารบัญ stops
  at 308. It is now bounded at `BOOK_LAST_PAGE`, with a second test stopping the
  exemption creeping below 308.

## ⚠ Two sessions cannot both hold `chanting.py`

This pass ran alongside the forward pass in the SAME clone and they collided:
one file held four pages of work from two sessions and neither could commit
without dragging in the other's. It was resolved by one honest combined commit.

**"Bank the batch files and apply later" is NOT a safe way round it.** A batch
file whose verses are not in `chanting.py` makes `check_pages` AND
`check_render` fail — so the repo sits red for as long as the data is held. Nine
banked batches broke the suite exactly that way, and it went green again only
once they were applied.

If two sessions must run at once, give each a `git worktree`. Note that
`apply_batch` splices a NEW chant at the single line closing `CHANTS`
(`apply_batch.py:996`), so two sessions adding chants will conflict there every
time — verse appends to different chants merge cleanly.

## What is worth a second pair of eyes against the book

All of it is an unreviewed draft, but these are the lines with least context to
self-correct from:

* **Page 321, verses 100–105** — a dense run of proper names: Kuṭeṇḍu, Veṭeṇḍu,
  Viṭuca, Viṭuṭa, Kinnughaṇḍu, Nighaṇḍu, Opamañña, Timbarū, Suriyavaccasā.
* **The book contradicting itself**, all recorded as printed and none corrected:
  `tap` for `taṃ` on two sheets (320, 321); `viruḷho` against `viruḷhako` for
  the same Great King; `bhikkhu` against `bhikkhū` on one sheet (318); `Evam`
  against `Evaṃ`; `āmantayi` against `āmantayī`.
* **Page 320 verse 76**, where the BOLD says new unit and the SPACING says same
  block. The spacing was followed — rows inside it sit 39–51px apart where every
  real break on that sheet is 77–113px.

## Measure every sheet. The gutter changed on all of them

Five sheets, five different measures: 319 a hard right-column edge at x 1080,
320 a corridor at x 972–1188, 321 at x 963–1045, 323 at x 880–978, 324 at
x 1062–1159 — and 323 and 324 FACE EACH OTHER.

**Page 322 is the trap.** It is mixed: eight single-column rows and then fifteen
two-column ones, and a whole-page gutter scan reports NO columns on it at all,
because the wide block closes the corridor. Reading it as two-column throughout
would have folded its first eight lines into four wrong verses.

## What the Yod Phrakantraipidok stretch taught, and it is not small

Pages 312–316 are a different kind of page from anything the forward pass has
met, and three of the four hard lessons came from getting something wrong first.

**⚠ MAGNIFY BEFORE TRANSCRIBING. This is now the default for the roman
section, not a fallback.** Twice on this chant, reading at page zoom produced a
wrong answer that a crop corrected. Every sheet from 314 on was read from crops
enlarged 1.5x.

**⚠ WORD SPACES HERE ARE 6–11px, NOT 15–25px.** Page 312 was first entered with
every line RUN TOGETHER, because the gaps were measured against an absolute
expected width and nothing cleared it. The section's real word space is only
about twice its letter gap. What made it worse: the gap after each item numeral
is 52px — a DOUBLE space — so measuring against that made every ordinary space
vanish. **Count wide gaps against the LINE'S OWN median, never an absolute
width**, and sanity-check on a short line whose word count you already know.
Fixed in `1d2d91f`.

**⚠ WORDS BREAK ACROSS LINE ENDS WITH NO HYPHEN.** Four times in two sheets —
`yāvajī`/`vaṃ`, `kusalā`/`dhammā`, `sabbasiddhivijjādhā`/`raṇaṃsāvaṃ` on 315,
and `saññā`/`khandho` on 316. Page 314 used a visible hyphen for the same thing,
so both marks are in use. An unhyphenated break leaves two nonsense fragments
and **no mark to warn you**, which makes it the fault most likely to survive
into the data unnoticed. Check every line end against the next line's opening.

**A SKEWED PHOTOGRAPH DEFEATS THE VERTICAL-GAP RULE.** On page 313 the left
edge drifts 43px from head to foot and the paragraph gaps compress with it:
item 3 breaks at 71px, item 5 at only 54px, below the threshold that has grouped
every page in this project. The hanging numerals settled it. Any sheet shot at
an angle needs the grouping taken from something other than the gap.

## The book contradicts the repo on one point

`chanting.py`'s comment above `_CONTENTS_ENGLISH` says the English is "never
taken from the book, which prints no English at all". **Page 312 prints English**
— `[The Peak of Tipitaka]`, centred in square brackets under the title — and
`yod-phrakantraipidok` now carries the BOOK'S wording in `title_english` rather
than one written for the app. That comment should be softened when someone next
touches it; it is true of the Thai-script pages and false of the roman section.
