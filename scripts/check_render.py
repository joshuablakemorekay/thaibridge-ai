#!/usr/bin/env python3
"""check_render.py — does the RENDERED page read like the printed page?

    PYTHONIOENCODING=utf-8 python scripts/check_render.py            # every page
    PYTHONIOENCODING=utf-8 python scripts/check_render.py 66 67 68   # some pages

Why this exists
---------------
`check_batch` checks a batch against itself. `check_pages` checks the DATA in
`chanting.py` against the batch files. Neither opens the page a reader actually
meets, and correct data renders badly often enough to be worth catching: a
template that prints an invitation both under the title and inside a prose
block shows it twice, and reads as a mistake in the book rather than in the app.

Until now that pass was re-improvised from the prompt every session, as a
throwaway script. `check_batch`'s own docstring says why that is not good
enough — improvised checkers produced three false results in a single
afternoon, and a check that cries wolf is worse than no check, because the next
real failure gets waved through. Every one of those false results came from
this pass. So it is written down, tested, and run like the others.

The two mistakes the throwaway versions kept making
---------------------------------------------------
Both come from asking "does this string appear exactly once?", which is the
obvious question and the wrong one.

1. **The book legitimately repeats itself.** Page 67 prints `ตัสสะ ภะคะวะโต,`
   as two separate units, and page 65 prints a chant's title inside the
   instruction paragraph above it as well as as its heading. Demanding one
   occurrence flags the book for being what it is.
2. **Short units are substrings of long ones.** `พุทโธ,` is a verse of its own
   on page 66 and also sits inside `อะภิสัมพุทโธ,` and `สัมมาสัมพุทโธ,` on the
   same page. Counting hits finds three and calls two of them duplicates.

So this does not count. It WALKS: it takes the strings the batch says the page
prints, in the order the book prints them, and consumes them from the rendered
text one after another, never searching backwards. A string that cannot be
found at or after the previous match is missing or out of order — which is the
question worth asking, and the one a count cannot answer. Repeats and
substrings both fall out of it for free, because the walk only ever moves
forward.
"""
from __future__ import annotations

import argparse
import glob
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BATCHES = REPO / "prompts" / "chanting-book-batch" / "batches"

# What stage 1 writes where a page stops mid-line. The completed line lives on
# the LATER page, so the partial one is not expected to render verbatim.
CUT = "[…]"


def flatten(text: str) -> str:
    """Collapse every run of whitespace to one space.

    Applied to BOTH sides, which is the point. A couplet break is stored as a
    `\\n` inside the Pali and reaches the page as markup, so comparing the raw
    strings says nine verses of the Jayamaṅgala are missing when every one of
    them is there. Whitespace is the one difference between the data and the
    page that carries no meaning, so it is the one difference to remove.
    """
    return re.sub(r"\s+", " ", text).strip()


def visible_text(html: str) -> str:
    """The page as a reader sees it: tags gone, entities left alone.

    Script and style bodies go first — they hold Thai in string literals on
    this app, and leaving them in lets a check pass on text nobody can read.
    """
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return flatten(text)


def first_claimed(batch_files) -> dict[tuple[str, int], int]:
    """(chant, verse) -> the LOWEST page any batch claims it on.

    A line the page break cut in half is claimed by two rows in two different
    batch files, and it belongs to the page it STARTS on — the earlier one.
    That is the rule `check_pages` enforces and the reading view depends on.

    Reading one batch at a time cannot see that: the later batch says "verse 11
    is on page 47" and is telling the truth about its own photograph, but the
    completed line renders on 46 where it began. Five pages were reported as
    dropping a verse before this existed, and every one of them was this — the
    checker was wrong and the app was right, which is the direction that
    matters, because a checker that cries wolf is worse than none.
    """
    lowest: dict[tuple[str, int], int] = {}
    for path in batch_files:
        batch = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        for row in batch["batch"]["pages"]:
            page, cid = row.get("page"), row.get("chant")
            if page is None or not cid:
                continue
            for n in verse_numbers(row.get("verses", "none")):
                key = (cid, n)
                if key not in lowest or page < lowest[key]:
                    lowest[key] = page
    return lowest


def expected(batch: dict, page: int,
             lowest: dict[tuple[str, int], int] | None = None
             ) -> tuple[list[list[tuple[str, str]]], list[tuple[str, str]]]:
    """What the page prints: ordered runs, plus loose strings.

    Returns `(runs, loose)`. Each RUN is a sequence that must appear on the
    page in that order; `loose` must appear somewhere on the page at all.

    The split is the point, and it is a claim about what this check owns:

    * **Within a chant, order is meaning.** Title, then verses in numeric
      order, then the colophon. A verse out of place is a reader chanting the
      wrong line, and nothing else in the pipeline looks at the rendered page
      to catch it. So each chant is one run.
    * **Between chants, order is settled elsewhere.** `build_page_index` sorts
      the chants on a page by the book's own chant numbering where every one
      of them carries it, and leaves file order alone where they do not. That
      rule is deliberate, documented, and tested where it lives. Re-deriving
      it here would put a second copy of it in a checker — and a checker that
      disagrees with the thing it checks is worse than no checker, because the
      next real failure gets waved through as another false alarm.
    * **Blocks are checked for presence, not position.** Their anchor is
      decided by `apply_batch.block_groups` from the page-map row, by a rule
      with its own tests. Losing a block entirely is the failure that has
      actually happened to this project — twice — and that is what this
      catches.

    The TEXT throughout comes from the batch, which is the record of what the
    photograph said, so this asks whether the app agrees with the PAGE rather
    than with itself.
    """
    by_id = {c["id"]: c for c in batch["chants"]}
    runs: list[list[tuple[str, str]]] = []
    loose: list[tuple[str, str]] = []

    for row in batch["batch"]["pages"]:
        if row.get("page") != page or "NOT WRITTEN" in (row.get("note") or ""):
            continue

        for i, block in enumerate(row.get("blocks") or []):
            if block.get("thai"):
                loose.append((f"{block.get('type')} block {i}", block["thai"]))
        if row.get("service_closing"):
            loose.append(("service closing", row["service_closing"]))

        cid = row.get("chant")
        entry = by_id.get(cid) if cid else None
        if not entry or entry.get("merge_only"):
            continue

        run: list[tuple[str, str]] = []
        # A continuation carries no title by design, and the book does not
        # reprint one on a page a chant merely runs onto.
        if row.get("starts_here") and entry.get("title_thai"):
            run.append((f"{cid} title", entry["title_thai"]))
        wanted = verse_numbers(row.get("verses", "none"))
        for verse in entry.get("verses") or []:
            n = verse["number"]
            if n not in wanted or not verse.get("pali"):
                continue
            # A line this page finishes but an earlier page began renders
            # where it began. Claiming it here would report the app for
            # following its own rule.
            if lowest and lowest.get((cid, n), page) < page:
                continue
            run.append((f"{cid} v{n}", verse["pali"]))
        # The colophon shows only on the page where the chant actually ends,
        # which is the page holding its last verse.
        closing = (entry.get("closing") or {}).get("pali")
        if closing and entry.get("verses") \
                and entry["verses"][-1]["number"] in wanted:
            run.append((f"{cid} closing", closing))
        if run:
            runs.append(run)

    return runs, loose


def verse_numbers(spec: str) -> set[int]:
    """'11-30' -> {11..30}; '7' -> {7}; 'none' -> empty."""
    if not spec or spec == "none":
        return set()
    lo, _, hi = spec.partition("-")
    return set(range(int(lo), int(hi or lo) + 1))


def cut(text: str) -> bool:
    """A line the page break stopped mid-way through.

    The app holds the COMPLETED version, which lives on the later page, so the
    partial text is not expected to render verbatim here. `check_pages` proves
    the two halves join.
    """
    return text.rstrip().endswith(CUT)


def walk(rendered: str, run: list[tuple[str, str]]) -> list[str]:
    """Consume one chant's strings from `rendered` in order.

    The cursor only moves forward, which is the whole design. A line the book
    genuinely prints twice is matched twice; a line that is a substring of an
    earlier one is matched at its own place; and a line the template emits out
    of order fails, because by the time it is looked for the cursor has
    already passed it. Counting occurrences answers none of those correctly,
    which is why the throwaway versions of this check kept crying wolf.
    """
    problems, cursor = [], 0
    for label, raw in run:
        text = flatten(raw)
        if cut(text):
            continue
        at = rendered.find(text, cursor)
        if at == -1:
            problems.append(
                f"{label}: " + ("out of order — it is on the page, but above "
                                "the line that should precede it"
                                if text in rendered else
                                "MISSING from the page entirely")
                + f" — {text[:60]!r}")
            continue
        cursor = at + len(text)
    return problems


def present(rendered: str, loose: list[tuple[str, str]]) -> list[str]:
    """Everything the page prints outside a chant has to be somewhere on it."""
    problems = []
    for label, raw in loose:
        text = flatten(raw)
        if not cut(text) and text not in rendered:
            problems.append(f"{label}: MISSING from the page entirely "
                            f"— {text[:60]!r}")
    return problems


def check(client, batch_files, pages=None):
    faults: dict[int, list[str]] = {}
    checked, strings = set(), 0
    lowest = first_claimed(batch_files)

    for path in batch_files:
        batch = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        name = pathlib.Path(path).name
        seen = {row.get("page") for row in batch["batch"]["pages"]}
        for page in sorted(p for p in seen if p is not None):
            if pages and page not in pages:
                continue
            runs, loose = expected(batch, page, lowest)
            if not runs and not loose:
                continue
            response = client.get(f"/chanting/page/{page}")
            if response.status_code != 200:
                faults.setdefault(page, []).append(
                    f"{name}: page returned HTTP {response.status_code}")
                continue
            rendered = visible_text(response.data.decode("utf-8"))
            problems = [p for run in runs for p in walk(rendered, run)]
            problems += present(rendered, loose)
            for problem in problems:
                faults.setdefault(page, []).append(f"{name}: {problem}")
            checked.add(page)
            strings += sum(len(r) for r in runs) + len(loose)

    return faults, {"pages": len(checked), "strings": strings}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pages", nargs="*", type=int,
                    help="page numbers to check (default: every page a batch "
                         "file describes)")
    args = ap.parse_args(argv)

    # Same reason check_batch and check_pages do it: a Windows console is
    # cp1252, and a report that dies while naming a Thai fault is worse than
    # one that finds nothing.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass

    sys.path.insert(0, str(REPO))
    import app as flaskapp

    files = sorted(glob.glob(str(BATCHES / "*.json")))
    faults, counts = check(flaskapp.app.test_client(), files,
                           set(args.pages) or None)

    print(f"pages rendered  : {counts['pages']}")
    print(f"strings walked  : {counts['strings']}")

    if not faults:
        print("\nPASS — every page renders what the book prints, in printed "
              "order")
        return 0

    print(f"\nFAIL — {sum(len(v) for v in faults.values())} problems on "
          f"{len(faults)} pages")
    for page in sorted(faults):
        print(f"\n  page {page}")
        for problem in faults[page]:
            print(f"    - {problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
