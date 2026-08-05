# v4 — reading from photographs, and making the page the unit

**2026-08-05**

## The request

```
Can we update Stage 1 and if necessary, Stage 2 - As we work through the chants,
adding them to the app in batches, I want all chants added to the app Digital
Chanting Book to be laid out like the actual book. I will add all of the images
to the Claude.ai chat in batches of 9. I want the chants added to the app to look
exactly like the images from the book (with 5 layer translations) so page numbers
contain exactly the script from each image. This is important for accuracy when a
monk calls out a page number, users go to that called-out page number and find
the exact chant as to follow along chanting with the monk. This also makes it
easy for users to navigate through every single chant like a book, for example,
you open one chant and can click either next page or previous page.
```

Asked how the book prints its page numbers:

```
There is alwyas a page number at the top centre in English. All other numbers
contained within some pages are numbers for chants or something else; either in
Thai or English?
```

That answer was worth more than the question. It named the one confusion that
would have corrupted every page after it.

## What changed

**The source is now photographs, not typing.** v3 assumed Josh transcribed the
text and marked each page turn himself as `[p.47]`. He no longer does either —
he photographs nine pages and pastes the images. So the prompt gained a section
on what a camera can and cannot give you: never complete a line lost to glare, a
fold, a finger or the crop; mark the gap `[…]`; name the image number so the
photograph can be retaken. Knowing the chant does not license completing it,
because this book's printing sometimes differs from a standard edition — which is
part of why it is being recorded at all.

**Only the top-centre number is a page number.** Everything else printed on the
page — chant numbers, verse numbers, references, in Thai numerals or Arabic — is
never promoted to one. This is stated as a hard rule rather than left to
judgement because the failure is invisible: a chant number read as a page number
produces output that looks entirely reasonable and is wrong for every page after
it. Chant numbers now have their own optional `book_number`, kept in Arabic
digits for searching and never derived from a page number. Stage 1 raises a check
on the first batch describing what those numbers appear to be — Josh has not
confirmed it, so the prompt asks it to observe rather than to file confidently.

**A page map, which is the real structural change.** The batch already declared a
manifest of chants before writing any of them, so that a truncated reply stays
detectable. v4 applies the same trick to pages: one row per page per chant,
saying which verses sit on it, declared before the entries. Stage 2 rebuilds each
verse's page by carrying forward and compares it against that map, verse by
verse. Neither side may be edited to agree with the other.

That check is what "page 47 in the app is page 47 in the book" actually rests on.
Without it, one missing page marker silently moves every verse after it onto the
wrong page, and nothing downstream would look wrong.

**Continuations.** Nine images is where the photographing stopped, not where the
book stopped, so a chant runs off the last page most batches. v3 had no way to
express this: "finish or don't start" would either refuse the chant or drop it,
and a chant arriving in two halves would arrive as two chants. Now the first half
carries `continues: true` and a `⚠️ CONTINUES` comment; the second half carries
`continuation_of` and keeps counting its verses from where the first stopped.
Stage 2 appends to the existing dict and prints the seam — the last two verses
from before and the first two from after — so the join can be seen rather than
trusted. Stage 3 skips any chant still marked `CONTINUES`, because commentary
written about half a chant would describe something that does not exist, and it
would look finished.

**Resuming is now by page.** `resume_from: "pabbatopama-gatha"` is not an
instruction anyone can act on holding a book and a camera. `resume_from_page: 53`
is.

**File order stopped mattering.** New chants append to the end of `CHANTS`;
`page_start` is what says where a chant sits in the book, and the reading view
sorts on it. The alternative — physically reordering dicts into book order — is a
huge diff across verified Pali for no gain, and moving verified text around is
the risk this whole workflow exists to avoid.

## What this changed about the seventeen

The seventeen chants set before this workflow existed have **no page numbers at
all** — verified, not assumed: `page_start` is present on zero of them. Until
they have some they cannot appear in a page-by-page view, so the book would have
holes exactly where its first chants are. v3's merge rule already brings them
through the pipeline; v4 adds why it matters and one narrow exemption. `page_start`,
the per-verse `page` keys and `book_number` are *additions*, not disagreements —
there is nothing to overwrite, so "the file wins" does not apply to them.

The `⚠️ PASTE DIFFERS` marker became `⚠️ PHOTO DIFFERS`, and now records which
page it was read from. The file still wins, but for a stated reason rather than
by fiat: those seventeen were typed with the book open, and the new reading came
off a camera. Where they disagree the likelier culprit is the lens. That is a
default, not a verdict, which is why every difference is still reported.

## Evidence

The rubric gained nine criteria and went to v2 — page map declared before the
entries, rows complete, page numbers integer-or-null, every image covered, only
declared chants named, pages running forwards, resume-by-page, the page scan
reported, and continuations never restarting verse numbering. The mock fixture
was rebuilt to carry a real page map so the new criteria are exercised rather
than passing on absence. Full suite re-run: **12 prompts, 100%.**

Two criteria pass vacuously against the mock — continuation numbering and
`book_number`'s type — because the only way to exercise them would be to invent
Pali for a half-chant, which is the exact failure the prompt exists to prevent.
That is recorded in the rubric header rather than papered over.

One harness change fell out of this: `page_map_runs_forwards` needs to test that
a list is in order, and the eval sandbox exposed no `sorted`. The criterion did
not fail — it errored with `NameError`, which scores as a failure but means
something different. Rather than contort the expression around a missing name,
`scripts/eval_runner.py` now exposes the pure ordering and collection builtins.
Adding names cannot change how any existing condition evaluates, and all twelve
prompts were re-run to confirm it.

## Deferred

The page-by-page reading view itself — jump to a page, next page, previous page —
is an app change, not a prompt change, and it is deliberately kept out of the
batch prompts. Stage 2 still may not touch the route or the template. A batch
that could quietly alter how the whole book renders is a batch whose diff nobody
can read.

The data is now shaped for it: `page_start` on every chant, page turns marked
inside every chant, and a page map proving both.

```
Once all chants are in the app we can add more features to the Digital Chanting
Book page such as a search bar for finding exact page number or chant title.
```

Held, as Josh set it — along with v3's deferred browse view and alphabet index.
Search over a book that is a fifth entered would be designed against the wrong
shape.
