# Chanting book — page to photograph map

The book was photographed in one pass: 333 PNGs in
`OneDrive\Pictures\Digital Chanting Book`, `IMG_0250.PNG` – `IMG_0594.PNG`.

**Filename order matches page order, but there is no fixed offset.** Some pages
were shot twice and the spare shot later deleted, so the gap between the file
number and the page number grows as you go through the book. Do not calculate a
filename — look it up here, or read the page number off the top of the photo.

`IMG_0250` – `IMG_0263` are the cover and front matter. Body page 1 starts at
`IMG_0264`.

## Verified anchors

Every row below was read directly off the page number printed at the top of the
photograph.

| page | photo | offset |
|-----:|-------|-------:|
| 1 | IMG_0264 | 263 |
| 15 | IMG_0278 | 263 |
| 16 | IMG_0279 | 263 |
| 17 | IMG_0280 | 263 |
| 18 | IMG_0281 | 263 |
| 19 | IMG_0282 | 263 |
| 20 | IMG_0283 | 263 |
| 21 | **IMG_0283a** | — (re-shot; suffixed to sort in place) |
| 22 | IMG_0284 | 262 |
| 23 | IMG_0285 | 262 |
| 26 | IMG_0288 | 262 |
| 27 | IMG_0289 | 262 |
| 28 | IMG_0290 | 262 |
| 30 | IMG_0292 | 262 |
| 31 | IMG_0294 | 263 |
| 32 | IMG_0295 | 263 |
| 33 | IMG_0296 | 263 |
| 34 | IMG_0297 | 263 |
| 51 | IMG_0314 | 263 |
| 52 | IMG_0315 | 263 |
| 53 | **IMG_0316** | 263 (a Photos-app screen capture — see below) |
| 54 | IMG_0317 | 263 |
| 59 | IMG_0322 | 263 |
| 60 | IMG_0323 | 263 |
| 61 | IMG_0324 | 263 |
| 62 | IMG_0325 | 263 |
| 63 | IMG_0326 | 263 |
| 64 | IMG_0327 | 263 |
| 65 | IMG_0328 | 263 |
| 68 | IMG_0331 | 263 |
| 207 | IMG_0477 | 270 |
| 213 | IMG_0483 | 270 |
| 215 | IMG_0485 | 270 |
| 217 | IMG_0487 | 270 |
| 218 | IMG_0488 | 270 |
| 220 | IMG_0490 | 270 |
| 221 | IMG_0491 | 270 |
| 222 | IMG_0492 | 270 |
| 223 | IMG_0493 | 270 |

The offset is 262–263 through the low pages and 270 by page 207, so seven pages
somewhere between 68 and 207 were shot twice. Those stretches are unmapped.

Pages 35–50 went in without being added here, and they all sat at offset 263 —
the same as pages 31–34 and 51. Pages 55–58 went in the same way. So the offset
holds **unbroken from 31 to 65**, now anchored at both ends of that run and at
every page from 59 to 65. That is a reason to expect the next filename, never a
reason to trust it: read the page number off the top of the photograph as
always.

## One photograph is a screen capture — `IMG_0316.PNG` (page 53)

It is a picture of the Photos app rather than of the page: a back arrow, a
"4 of 4" caption and an Adjust / Filters / Rotate / Delete toolbar are all in
the frame, and the toolbar sits over the foot of the sheet.

**It was checked and it hides nothing.** The toolbar covers only the blank lower
margin, and the left column beside it is clear and holds no ink, so page 53
really does end at ธัมมัสสาหัส์มิ ทาโส วะ. Recorded here so nobody has to prove
that twice — but a clean re-shot would remove the doubt, and it is the one
photograph in this stretch worth retaking.

## Page 21 was re-shot — `IMG_0283a.PNG`

Page 21 was missed in the original pass (`IMG_0283` is page 20, `IMG_0284` is
page 22) and was re-shot on 2026-08-08. It arrived as `IMG_0600.PNG` at the end
of the folder and has been **renamed `IMG_0283a.PNG` so it sorts into its right
place** between pages 20 and 22. Folder order is page order again.

The suffix was used rather than renumbering: there is no free integer between
0283 and 0284, and shifting everything from 0284 up would invalidate every
`IMG_xxxx` reference already written into `chanting.py` and this document.

**⚠ One trap it introduces.** A naive `re.search(r'(\d+)', name)` reads
`IMG_0283a` as **283**, colliding with page 20. Any script that maps filenames
to pages must sort on the full stem and not assume one file per integer. Do the
same for future re-shoots: give them the previous page's number plus a letter.

Missing file numbers elsewhere (255, 293, 337, 350, 394–396, 398–399, 450,
587–588) are deleted duplicate shots, not missing pages — page 30 is present as
`IMG_0292` despite `IMG_0293` being absent. **A filename gap does not mean a
missing page, and a missing page leaves no gap** — page 21 was invisible in the
gap list. Only reading the page numbers finds this class of miss.

## The 17 chants entered before the page pass

Chants 1–17 in `CHANTS` were transcribed from pasted text rather than from the
photographs, and had no `page_start`. Page numbers below come from the book's
own สารบัญ (already in `CONTENTS`) and the photos are the verified map above.

| chant id | page | photo | state |
|---|---:|---|---|
| mettanisamsa-sutta | 22 | IMG_0284 | to verify |
| mettanisamsa-gatha | 23 | IMG_0285 | ✅ verified 2026-08-08 |
| devatadissa-dakkhinanumodana | 26 | IMG_0288 | ✅ verified 2026-08-08 |
| tilakkhanadi-gatha | 27–28 | IMG_0289 / IMG_0290 | ✅ verified 2026-08-08 |
| devatabhisammantana | 27 | IMG_0289 | ✅ verified 2026-08-08 |
| khemakhema-saranadipika | 28 **or** 215 | IMG_0290 / IMG_0485 | ambiguous — two similar titles |
| pabbatopama-gatha | 30 | IMG_0292 | to verify |
| ariyadhana-gatha | 31 | IMG_0294 | to verify |
| paticcasamuppada-patho | 31 | IMG_0294 | to verify |
| buddhaudana-gatha | 32 | IMG_0295 | to verify |
| bhaddekaratta-gatha | 33 | IMG_0296 | to verify |
| dhatupatikula-paccavekkhana | 61 **or** 207 | IMG_0324 / IMG_0477 | printed twice in the book |
| dvattimsakara-patha | 217–218 | IMG_0487 / IMG_0488 | ✅ verified 2026-08-08 |
| bharasutta-gatha | 218–219 | IMG_0488 / IMG_0489 | ✅ verified 2026-08-08 |
| **tilokavijaya-pattidana** | **220–221** | **IMG_0490 / IMG_0491** | **✅ verified and rebuilt 2026-08-08** |
| sankhara-contemplation | 222 | IMG_0492 | to verify |
| abhinha-paccavekkhana | 223 | IMG_0493 | to verify |

### Two to settle by eye

- **khemakhema-saranadipika** — page 28 has been read and is **Dhammapada
  188–192**, the same text as the entry, but printed under the LONG title
  `เขมาเขมะสะระณะคะมะนะปะริทีปิกาคาถา` and set as **ten lines of two pādas**.
  The entry carries the SHORT title (matching the สารบัญ's page-215 listing) and
  groups **four pādas per verse**, i.e. half as many lines. So the entry most
  likely came from the page-215 printing, not page 28. **`IMG_0485` (p215) must
  be read before touching this chant** — it decides both the title and the line
  division, and getting it wrong would reshape a chant to the wrong printing.
- **dhatupatikula-paccavekkhana** — genuinely printed twice, at 61 and 207.
  **Decided 2026-08-14: two entries, one per printing.** Page 61 was read and is
  Pali-only in four run-on paragraphs, where this entry has a Thai translation,
  about thirty short verses and parenthesised rubrics — so it cannot be the
  page-61 printing without the app showing text that page does not print. Page
  61 went in as `dhatupatikula-paccavekkhana-p61`; **this entry keeps its id and
  takes `page_start` 207**, which `IMG_0477` still has to confirm.

## Upgrade in place — never re-add

These chants already exist in `CHANTS`. When the page pass reaches their pages,
**edit the existing entry** — give it `page_start` and a `page` marker on the
verse where the page turns. Adding a fresh entry would leave two copies of the
same chant, one paginated and one not.

## What "verified" cost, for planning

Tilokavijaya took two full-page reads plus three crops. Reading only the page
number is far cheaper: crop the top ~170px of several photos, stack them into
one image, and read them in a single pass. That is how the table above was
built.

## Layout is per chant — do not infer it

The two-column setting in this book means different things in different chants,
and there is no way to tell but to look:

- **Two Pali pādas to a line**, Thai as a block beneath or absent —
  Tilokavijaya (220), Mettānisaṃsagāthā (23), Bhaddekaratta (33),
  Pabbatopama (30), Devatādissadakkhiṇānumodanā (26).
- **One Pali pāda to a line, Thai alongside in the right column** —
  Bhārasutta (218–219).
- **A two-column list, one item per cell, read left cell then right cell** —
  Dvattiṃsākāra (217–218).

A pāda-pairing pass that assumed the first of these joined Bhārasutta's eight
lines into four. That was wrong and has been undone. Check the layout on the
photograph before touching line division.

## The recurring fault in the pasted text

Wherever the book uses two columns, the paste tended to read them in the wrong
order — right cell before left, or grouping across the row boundary. It has
turned up in three chants so far (Tilokavijaya lines 1–3, Dvattiṃsākāra
throughout, and it is what the old "kept as printed, standard editions differ"
notes were actually seeing). Suspect it in any chant whose order disagrees with
the canonical text.

## The first six chants are not exempt

The pāda-pairing pass deliberately left the six earliest chants alone, on the
understanding that they had already been checked. Page 26 shows that
**Devatādissadakkhiṇānumodanāgāthā — the sixth — had the same fault**: twelve
pādas entered one to a line where the book prints six lines of two. It has been
joined.

So the remaining five early chants (Khemākhemasaraṇadīpikā, Saṅkhāra
contemplation, Dhātupaṭikūla, Tilakkhaṇādi, Abhiṇhapaccavekkhaṇa) need reading
against their pages like every other chant. Being entered early is not evidence
of being right.

## A third fault class: footnotes attributed to the wrong chant

Page 27 carries one footnote, `ขุ.ขุ. 25/89, ขุ.อุ. 25/221`, and its superscript
marker sits on the **last line of the chant above** (Devatābhisammantana). The
entry for Tilakkhaṇādi — which merely *starts* on the same page — had taken it
as its own source. Tilakkhaṇādi's real marker is on its last line, on page 28,
pointing at that page's footnote `ขุ.ขุ. 25/51`.

**A footnote belongs to the line its marker sits on, not to the chant that
happens to be nearest the foot of the page.** Two chants sharing a page will
each have their own. Check the marker, not the proximity.

## Both chants on page 27 — and they disagree

Page 27 is the clearest proof that layout cannot be inferred. It carries two
chants, one above the other:

- **Devatābhisammantana** — single column, one pāda to a line. Already correct.
- **Tilakkhaṇādi** — two columns, two pādas to a line. Needed joining, 35 → 18.

Same page, same book, opposite settings.
