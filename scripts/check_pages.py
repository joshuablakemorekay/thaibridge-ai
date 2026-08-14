"""Prove every page in the app shows what its photograph showed.

`check_batch.py` checks a batch against itself and `apply_batch.py` writes it
into the app. Nothing checked the third thing, and it is the one that matters
to a reader: that the page the app serves is the page the book prints.

That gap has already cost this book once. Stage 1 read pages 7 and 8 correctly
and recorded everything on them — a service closing, a section heading, six
numbered items, a footnote. Stage 2 had no field for any of it and wrote the
chants alone. No error was raised, no test failed, and both pages went live
showing roughly half of what the printed page shows. It was found weeks later,
by Josh reading the app beside the book.

The batch files are the permanent record of what each photograph said, so they
are what the app can be held to without opening the images again. For every
page row in every batch file this asks four questions:

  1. is the chant that row names on that page in the app at all?
  2. does the app put exactly the verses the row claims on that page?
  3. is that text identical to what the batch recorded?
  4. is every block the row declares — heading, rubric, footnote, item,
     service closing — actually on that page?

One rule needs teaching, or the report is unusable. A page break can fall
mid-line: the earlier batch records a partial verse ending `[…]` and the later
batch completes it, carrying the SAME verse number. Two rows then claim one
verse, and the app holds text that matches neither by equality. Both are
correct. The verse belongs to the page it STARTS on, and the completed line
must begin with the partial one — which this checks rather than waives.

Run it:

    PYTHONIOENCODING=utf-8 python scripts/check_pages.py

Pages the app serves with no batch record are reported but are not faults:
page 1 prints no number at all, and the pre-page chants were verified straight
from their photographs without a batch file. They are listed so the number
never quietly grows.
"""
import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

BATCHES = REPO / "prompts" / "chanting-book-batch" / "batches"
LAYERS = ("pali", "pali_roman", "thai", "paiboon", "english")
CUT = "[…]"


def verse_range(spec):
    """'1-6' -> [1..6]; '7' -> [7]. The same grammar the other scripts read."""
    lo, _, hi = spec.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def is_completion(recorded: str, written: str) -> bool:
    """True where `written` is `recorded` with the page break healed.

    Checked rather than assumed: the completed line must START with the
    partial one, minus its marker. A different line replacing a partial one
    means the two batches disagree about what the book says, which is the
    thing worth finding.
    """
    if not recorded.endswith(CUT):
        return False
    return written.startswith(recorded[:-len(CUT)].rstrip())


def collect(batch_files):
    """Every claim the batch files make: {(chant, verse): {page: text}}."""
    claims = collections.defaultdict(dict)
    blocks = collections.defaultdict(list)
    rows = 0
    for path in batch_files:
        batch = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        name = pathlib.Path(path).name
        by_id = {c["id"]: c for c in batch["chants"]}

        for row in batch["batch"]["pages"]:
            page, cid = row.get("page"), row.get("chant")
            if page is None or "NOT WRITTEN" in (row.get("note") or ""):
                continue

            declared = list(row.get("blocks") or [])
            if row.get("service_closing"):
                declared.append({"type": "service_closing",
                                 "thai": row["service_closing"]})
            for block in declared:
                blocks[page].append((name, block))

            if not cid or row.get("verses") in (None, "none"):
                continue
            rows += 1
            entry = by_id.get(cid)
            recorded = {}
            if entry and not entry.get("merge_only"):
                recorded = {v["number"]: v for v in entry.get("verses") or []}
            for n in verse_range(row["verses"]):
                claims[(cid, n)][page] = (name, recorded.get(n))
    return claims, blocks, rows


def app_placement(chanting):
    """Where the APP puts every verse, by carrying each page marker forward."""
    where, text = {}, {}
    for chant in chanting.CHANTS:
        page = chant.get("page_start")
        for verse in chant["verses"]:
            page = verse.get("page", page)
            where[(chant["id"], verse["number"])] = page
            text[(chant["id"], verse["number"])] = verse
    return where, text


def app_blocks(chanting):
    pages, _ = chanting.build_page_index()
    out = collections.defaultdict(set)
    for entry in pages:
        for item in entry["entries"]:
            if item["kind"] == "blocks":
                for block in item["blocks"]:
                    out[entry["page"]].add(block.get("thai", ""))
    return out


def check(chanting, batch_files):
    claims, declared_blocks, rows = collect(batch_files)
    where, text = app_placement(chanting)
    shown = app_blocks(chanting)
    served = {e["page"] for e in chanting.build_page_index()[0]}

    faults = collections.defaultdict(list)
    verses = 0

    for page, entries in sorted(declared_blocks.items()):
        for name, block in entries:
            if block.get("thai") not in shown.get(page, set()):
                faults[page].append(
                    f"{name}: the page prints a {block.get('type')} block the "
                    f"app does not show — {block.get('thai', '')[:60]!r}")

    for (cid, n), by_page in sorted(claims.items()):
        # A verse claimed by two pages is a line the page break cut in half.
        # It belongs to the page it starts on, so the lowest page wins — but
        # only if the earlier record really is a partial line.
        pages = sorted(by_page)
        starts_on = pages[0]
        if len(pages) > 1:
            first = by_page[starts_on][1]
            recorded = (first or {}).get("pali", "")
            if not recorded.endswith(CUT):
                faults[starts_on].append(
                    f"{cid} verse {n} is claimed by pages {pages}, and page "
                    f"{starts_on} did not record it as cut off — two batches "
                    f"overlap and one of them is wrong")
                continue

        if (cid, n) not in where:
            faults[starts_on].append(
                f"{cid} verse {n} is printed on this page but is not in the "
                f"app at all")
            continue
        if where[(cid, n)] != starts_on:
            faults[starts_on].append(
                f"{cid} verse {n} is printed on this page but the app puts it "
                f"on page {where[(cid, n)]}")
            continue

        for page in pages:
            name, recorded = by_page[page]
            if not recorded:
                continue
            verses += 1
            for layer in LAYERS:
                want, got = recorded.get(layer, ""), text[(cid, n)].get(layer, "")
                if want == got:
                    continue
                if is_completion(want, got):
                    continue
                # The prefix test is only honest on a layer that is
                # REPRODUCED. `english` is composed, and the gloss of half a
                # sentence is not the beginning of the gloss of the whole one
                # — Pali and English do not order their words alike. So a
                # partial english is accepted as superseded, while pali,
                # pali_roman and thai are still held to continuing the line
                # the page actually printed.
                if want.endswith(CUT) and layer == "english":
                    continue
                if want.endswith(CUT):
                    faults[page].append(
                        f"{name}: {cid} verse {n} {layer} was cut off here and "
                        f"what the app holds does not continue it\n"
                        f"        page {page}: {want!r}\n"
                        f"        app:    {got!r}")
                else:
                    faults[page].append(
                        f"{name}: {cid} verse {n} {layer} differs from what "
                        f"this page recorded\n        page {page}: {want!r}\n"
                        f"        app:    {got!r}")

    return faults, {"rows": rows, "verses": verses,
                    "blocks": sum(len(v) for v in declared_blocks.values()),
                    "recorded_pages": len(declared_blocks | {
                        p: None for p in {pg for _, pg in
                                          [(k, p) for k, v in claims.items()
                                           for p in v]}}),
                    "served": len(served),
                    # A page is RECORDED if any batch file describes it, and a
                    # page can be described entirely by blocks. Page 63 is the
                    # first: it holds the notes to the evening service and no
                    # chant, so it makes no verse claim and counting claims
                    # alone reported it as having no record at all. That is
                    # the one number here meant to stay still, so a fully read
                    # page appearing in it would teach everyone to ignore it.
                    "unrecorded": sorted(served
                                         - {p for v in claims.values() for p in v}
                                         - set(declared_blocks))}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("batches", nargs="*",
                    help="batch files to check (default: all of them)")
    args = ap.parse_args(argv)

    # Reconfigured for the same reason check_batch does it: a Windows console
    # is cp1252, and a report that dies while naming a Thai fault is worse
    # than one that finds nothing.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass

    import chanting

    files = args.batches or sorted(glob.glob(str(BATCHES / "*.json")))
    faults, counts = check(chanting, files)

    print(f"page rows reconciled : {counts['rows']}")
    print(f"verses compared      : {counts['verses']}")
    print(f"blocks compared      : {counts['blocks']}")
    print(f"pages the app serves : {counts['served']}")
    print(f"served with no batch record: {counts['unrecorded'] or 'none'}")

    if not faults:
        print("\nPASS — every page shows the chants, verses and blocks its "
              "photograph recorded")
        return 0

    print(f"\nFAIL — {sum(len(v) for v in faults.values())} disagreements on "
          f"{len(faults)} pages")
    for page in sorted(faults):
        print(f"\n  page {page}")
        for problem in faults[page]:
            print(f"    - {problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
