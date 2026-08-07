#!/usr/bin/env python3
"""check_batch.py — Stage 1 of the chanting-book workflow, checked by a script.

Reads a batch file written by Stage 1 and reports every way it fails the rules
the prompt sets for itself.

    python scripts/check_batch.py prompts/chanting-book-batch/batches/batch-014-014.json
    python scripts/check_batch.py prompts/chanting-book-batch/batches/*.json
    python scripts/check_batch.py --all          # every batch file in the folder

Why this exists
---------------
Stage 2 has had `apply_batch.py` since the third batch, because a hand-written
step that runs forty times can silently half-succeed. Stage 1 had nothing. Its
self-checks — the Paiboon+ drift scan, the page map reconciliation, the
diacritic sweep — were re-improvised each session from the prompt, which means
they were only ever as good as that session's reconstruction of them.

That is not hypothetical either. Improvised checkers produced three false
results in a single afternoon: one reported "0 checks written" when all twelve
were present, because the script had been copied through a shell that re-encoded
the ‼ marker; one reported a duplicate citation that was really a CSS rule; one
reported the page out of order because it searched for text by first occurrence
and the book legitimately prints the same line three times.

None of those were data errors. All three cost time and two of them looked
exactly like real failures. A check that cries wolf is worse than no check,
because the next real failure gets waved through.

What it checks
--------------
The rules come from the prompt, and each is a separate function so it can be
tested against a case that is known to break it:

  * Paiboon+ has not drifted back towards RTGS — the failure the whole
    romanisation convention exists to prevent, and the one that decays over a
    long session.
  * No `pali` value has been romanised, and no `pali_roman` carries Thai. These
    two corruptions cannot be spotted downstream.
  * Every verse carries all five layer KEYS. A missing key is a fault; an empty
    value is a fact about what the book printed.
  * A layer the book did not print is empty rather than invented — if `thai` is
    empty then `paiboon` must be too, because Paiboon+ romanises the Thai and
    there is no Thai to romanise.
  * The manifest matches the entries, and the page map agrees with both: every
    claimed verse exists, and every verse falls in exactly one page row.
  * Page numbers ascend.
  * The same Pali word is not romanised two ways — unless the batch DECLARES
    the pair, with its reason, in `batch_status.diacritic_exceptions`.
  * A DATA-ONLY batch does not carry the commentary it is meant to defer.
  * Nothing has a raw newline inside a string value.

Every problem names the chant and verse it belongs to, so it can be found.
"""
from __future__ import annotations

import argparse
import glob
import json
import pathlib
import re
import sys
import unicodedata

REPO = pathlib.Path(__file__).resolve().parent.parent
BATCHES = REPO / "prompts" / "chanting-book-batch" / "batches"

LAYERS = ("pali", "pali_roman", "thai", "paiboon", "english")
# Paiboon+ uses k, t, p and ŋ. None of these can legitimately appear.
RTGS_TELLS = ("kh", "th", "ph", "ng")
# Fields a DATA-ONLY batch defers to stage 3 rather than writing now.
COMMENTARY = ("background", "meaning", "summary", "when_chanted", "source")

THAI = re.compile(r"[฀-๿]")
LATIN = re.compile(r"[A-Za-z]")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def verse_range(spec: str) -> set[int]:
    """'1-6' -> {1..6}; '7' -> {7}. Same grammar apply_batch reads."""
    lo, _, hi = spec.partition("-")
    return set(range(int(lo), int(hi or lo) + 1))


def skeleton(word: str) -> str:
    """A romanised word with its diacritics stripped, for comparing spellings.

    `paṇṇarasī` and `pannarasi` share a skeleton; if both appear, one of them
    is a slip. Two genuinely different words can share one too — `va` and `vā`
    both mean 'or' and sit in the same printed line — which is why a batch may
    declare a pair rather than being forced to corrupt one of them.
    """
    return "".join(ch for ch in unicodedata.normalize("NFD", word.lower())
                   if not unicodedata.combining(ch))


def paiboon_values(chant: dict):
    """Every Paiboon+ string on a chant, with a label saying where it is."""
    for key in ("invitation", "closing"):
        block = chant.get(key) or {}
        if block.get("paiboon"):
            yield f"{key}", block["paiboon"]
    for verse in chant.get("verses", []):
        if verse.get("paiboon"):
            yield f"verse {verse.get('number')}", verse["paiboon"]


# ---------------------------------------------------------------------------
# The checks. Each returns a list of problems; empty means it passed.
# ---------------------------------------------------------------------------

def check_shape(batch: dict) -> list[str]:
    """The file has the three top-level keys and the entries have their keys.

    Runs first because every other check reads these, and a confusing
    KeyError three checks later is worse than saying what is missing.
    """
    problems = []
    for key in ("batch", "chants", "batch_status"):
        if key not in batch:
            problems.append(f"the file has no {key!r} key")
    if problems:
        return problems

    for key in ("depth", "manifest", "pages"):
        if key not in batch["batch"]:
            problems.append(f"batch has no {key!r}")

    for chant in batch["chants"]:
        cid = chant.get("id", "<no id>")
        if "id" not in chant:
            problems.append("a chant has no id")
        elif not SLUG.match(chant["id"]):
            problems.append(
                f"{cid}: id is not a slug — lower case, digits and hyphens "
                f"only, no diacritics")
        for key in ("verses", "checks"):
            if key not in chant:
                problems.append(f"{cid}: has no {key!r} array")
        if not chant.get("verses"):
            problems.append(f"{cid}: has no verses")

    for row in batch["batch"].get("pages", []):
        for key in ("page", "file", "chant", "verses"):
            if key not in row:
                problems.append(f"a page row has no {key!r}: {row}")
    return problems


def check_paiboon(batch: dict) -> list[str]:
    """Paiboon+ has not drifted back towards RTGS.

    The single failure the romanisation convention most exists to prevent.
    Adherence decays over a long session, so the last chant needs this as much
    as the first.
    """
    problems = []
    for chant in batch["chants"]:
        for where, value in paiboon_values(chant):
            for tell in RTGS_TELLS:
                if tell in value:
                    problems.append(
                        f"{chant['id']} {where}: paiboon contains {tell!r} — "
                        f"Paiboon+ uses k, t, p and ŋ, never kh/th/ph/ng")
    return problems


def check_pali_untouched(batch: dict) -> list[str]:
    """`pali` is the book's Thai script; `pali_roman` is IAST. Neither leaks.

    Running Paiboon+ over a `pali` value corrupts the chanted layer, and it is
    invisible once downstream — which is why it is checked here, against the
    script each field is supposed to be written in.
    """
    problems = []
    for chant in batch["chants"]:
        for verse in chant["verses"]:
            n, pali, roman = verse.get("number"), verse.get("pali", ""), verse.get("pali_roman", "")
            if pali and not THAI.search(pali):
                problems.append(
                    f"{chant['id']} verse {n}: pali has no Thai script in it")
            if pali and LATIN.search(pali):
                problems.append(
                    f"{chant['id']} verse {n}: pali contains Latin letters — "
                    f"it may have been romanised")
            if roman and THAI.search(roman):
                problems.append(
                    f"{chant['id']} verse {n}: pali_roman contains Thai script")
    return problems


def check_layer_keys(batch: dict) -> list[str]:
    """Every verse carries all five layer keys, at every depth.

    Carrying the key is not the same as carrying a value: a Pali-only chant has
    an empty `thai`, and that is correct and finished. A MISSING key is the
    fault.
    """
    problems = []
    for chant in batch["chants"]:
        for verse in chant["verses"]:
            missing = [layer for layer in LAYERS if layer not in verse]
            if missing:
                problems.append(
                    f"{chant['id']} verse {verse.get('number')}: missing layer "
                    f"key(s) {missing}")
            if "english" in verse and not verse["english"]:
                problems.append(
                    f"{chant['id']} verse {verse.get('number')}: english is "
                    f"empty — a verse without its meaning is not usable, and "
                    f"english is never dropped at any depth")
    return problems


def check_layers_not_invented(batch: dict) -> list[str]:
    """A layer the book did not print is empty, not filled in from the other side.

    `paiboon` romanises the `thai`. No Thai printed means nothing to romanise,
    so a `paiboon` beside an empty `thai` was written from the Pali or invented.
    """
    problems = []
    for chant in batch["chants"]:
        for verse in chant["verses"]:
            if verse.get("paiboon") and not verse.get("thai"):
                problems.append(
                    f"{chant['id']} verse {verse.get('number')}: paiboon is "
                    f"set but thai is empty — Paiboon+ romanises the Thai, so "
                    f"there was nothing to romanise")
    return problems


def check_manifest(batch: dict) -> list[str]:
    """The manifest describes what is on the pages, and must match what arrived."""
    problems = []
    manifest = batch["batch"]["manifest"]
    ids = [c["id"] for c in batch["chants"]]

    if len(manifest) != len(ids):
        problems.append(
            f"manifest lists {len(manifest)} chants but {len(ids)} arrived — "
            f"the run may have stopped early and the last entry may be "
            f"incomplete")
    for cid in ids:
        if cid not in manifest:
            problems.append(f"{cid} arrived but was never declared in the manifest")
    for cid in manifest:
        if cid not in ids:
            problems.append(f"{cid} was declared in the manifest but never arrived")

    # Three states, not two. A chant in `continues` is COMPLETE for this batch
    # — the book carries it onto a page that was not photographed yet — and
    # treating it as unfinished is the confusion the prompt warns about by
    # name. An earlier draft of this check accepted only the first two and
    # failed both of the first real batches.
    status = batch["batch_status"]
    accounted = (set(status.get("completed", []))
                 | set(status.get("not_started", []))
                 | set(status.get("continues", [])))
    for cid in manifest:
        if cid not in accounted:
            problems.append(
                f"{cid} is in the manifest but in none of completed, "
                f"not_started or continues")
    return problems


def check_page_map(batch: dict) -> list[str]:
    """The page map is a second manifest, doing the same job for pages.

    Every verse must fall in exactly one page row. A verse claimed by two pages,
    or by none, is a page-fidelity error — and it is the kind that never looks
    wrong afterwards, because the page still renders.
    """
    problems = []
    by_id = {c["id"]: c for c in batch["chants"]}
    claimed: dict[tuple[str, int], list] = {}

    for row in batch["batch"]["pages"]:
        cid, spec = row.get("chant", ""), row.get("verses", "none")
        if not cid or spec == "none" or "NOT WRITTEN" in row.get("note", ""):
            continue
        if cid not in by_id:
            problems.append(
                f"page {row.get('page')} names {cid}, which never arrived")
            continue
        have = {v["number"] for v in by_id[cid]["verses"]}
        for n in sorted(verse_range(spec)):
            if n not in have:
                problems.append(
                    f"page {row.get('page')} claims {cid} verse {n}, but the "
                    f"entry has no such verse")
            claimed.setdefault((cid, n), []).append(row.get("page"))

    for (cid, n), pages in sorted(claimed.items()):
        if len(pages) > 1:
            problems.append(
                f"{cid} verse {n} is claimed by pages {pages} — a verse "
                f"belongs to exactly one page")
    for chant in batch["chants"]:
        for verse in chant["verses"]:
            if (chant["id"], verse["number"]) not in claimed:
                problems.append(
                    f"{chant['id']} verse {verse['number']} is on no page in "
                    f"the map")
    return problems


def check_pages_ascend(batch: dict) -> list[str]:
    """Page numbers run forwards. A jump backwards is a photo out of order."""
    pages = [r.get("page") for r in batch["batch"]["pages"] if r.get("page") is not None]
    if pages != sorted(pages):
        return [f"page numbers do not ascend down the map: {pages} — either a "
                f"photograph is out of order or a number was misread"]
    return []


def check_diacritics(batch: dict) -> list[str]:
    """The same Pali word must not be romanised two ways across one batch.

    The commonest quality failure in editions like this, and it compounds:
    nobody notices at three pages and nobody can fix it at three hundred.

    A batch may DECLARE a pair that only looks like drift, in
    `batch_status.diacritic_exceptions`, as "va/vā — why". Declaring is
    deliberately noisy: it lands in the permanent record with its reason, and
    an UNDECLARED pair still fails, so this cannot be used to wave drift past.
    """
    declared = set()
    for entry in batch["batch_status"].get("diacritic_exceptions", []):
        pair = entry.split(" ")[0]
        declared.add("/".join(sorted(pair.split("/"))))

    spellings: dict[str, set] = {}
    for chant in batch["chants"]:
        for verse in chant["verses"]:
            text = unicodedata.normalize("NFC", verse.get("pali_roman", ""))
            for word in re.findall(r"[^\s,.;:!?()\[\]]+", text):
                spellings.setdefault(skeleton(word), set()).add(word.lower())

    problems = []
    for _, variants in sorted(spellings.items()):
        if len(variants) < 2:
            continue
        key = "/".join(sorted(variants))
        if key in declared:
            continue
        problems.append(
            f"romanised two ways in one batch: {sorted(variants)} — fix it, or "
            f"declare the pair in batch_status.diacritic_exceptions with the "
            f"reason if they are genuinely different words")
    return problems


def check_depth(batch: dict) -> list[str]:
    """A DATA-ONLY batch defers the commentary rather than half-writing it."""
    if batch["batch"].get("depth") != "DATA-ONLY":
        return []
    problems = []
    for chant in batch["chants"]:
        present = [f for f in COMMENTARY if chant.get(f)]
        if present:
            problems.append(
                f"{chant['id']}: depth is DATA-ONLY but carries {present} — "
                f"stage 3 writes those by reading the chants out of the app")
    return problems


def check_no_raw_newlines(batch: dict) -> list[str]:
    """A line break belonging to the text is written \\n, never a real newline."""
    problems = []

    def walk(node, path=""):
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{path}/{key}")
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, f"{path}[{i}]")
        elif isinstance(node, str) and "\n" in node:
            problems.append(f"raw newline inside a string value at {path}")

    walk(batch)
    return problems


def check_blocks(batch: dict) -> list[str]:
    """Page blocks carry what the app renders them from.

    A block whose `thai` is missing renders as an empty line: present in the
    data, invisible on the page, impossible to spot by reading the file. An
    empty `english` is allowed only on a footnote, because a canonical citation
    is reproduced and never translated.
    """
    problems = []
    for row in batch["batch"]["pages"]:
        for i, block in enumerate(row.get("blocks", [])):
            where = f"page {row.get('page')} block {i} ({block.get('type')})"
            if not block.get("type"):
                problems.append(f"{where}: has no type")
            if not block.get("thai"):
                problems.append(f"{where}: has no thai — it would render blank")
            if not block.get("english") and block.get("type") != "footnote":
                problems.append(f"{where}: has no english")
            if block.get("type") == "item" and block.get("number") is None:
                problems.append(
                    f"{where}: a numbered instruction with no number — the "
                    f"book's own numbering runs across page turns and must be "
                    f"kept")
    return problems


def check_checks_are_readable(batch: dict) -> list[str]:
    """Checks are objects stage 2 can read, and each names its photograph.

    A check must be `{"verse": n|null, "file": "IMG_x.PNG", "issue": "..."}`.
    batch-009-009.json wrote them as pre-formatted strings instead, and
    `apply_batch.render_chant` raises TypeError on that shape — so the file
    kept as the permanent record of page 9 cannot be re-applied by the tool
    that is supposed to read it. That is why this check tests the type before
    the contents rather than assuming a dict and crashing.

    The filename matters as much as the text: it is what lets a photograph be
    found and retaken, and several checks exist only to ask for exactly that.
    """
    problems = []
    for chant in batch["chants"]:
        # Reported once per chant with a count. Seven identical lines saying
        # the same thing about the same entry is how a real second problem
        # gets scrolled past.
        wrong = [c for c in chant.get("checks", []) if not isinstance(c, dict)]
        if wrong:
            kinds = sorted({type(c).__name__ for c in wrong})
            problems.append(
                f"{chant['id']}: {len(wrong)} of {len(chant['checks'])} checks "
                f"are {'/'.join(kinds)}, not objects — apply_batch raises "
                f"TypeError on this shape, so the batch cannot be applied")
        for check in chant.get("checks", []):
            if not isinstance(check, dict):
                continue
            if not check.get("file"):
                problems.append(
                    f"{chant['id']}: a check names no image file — the "
                    f"filename is what makes a photograph findable")
            if "issue" not in check:
                problems.append(f"{chant['id']}: a check has no issue text")
            if "verse" not in check:
                problems.append(
                    f"{chant['id']}: a check has no verse key (use null for a "
                    f"check about the chant as a whole)")
    return problems


CHECKS = (
    ("shape", check_shape),
    ("paiboon drift", check_paiboon),
    ("pali untouched", check_pali_untouched),
    ("five layer keys", check_layer_keys),
    ("layers not invented", check_layers_not_invented),
    ("manifest", check_manifest),
    ("page map", check_page_map),
    ("pages ascend", check_pages_ascend),
    ("diacritics", check_diacritics),
    ("depth", check_depth),
    ("no raw newlines", check_no_raw_newlines),
    ("page blocks", check_blocks),
    ("checks readable", check_checks_are_readable),
)


def validate(batch: dict) -> dict[str, list[str]]:
    """Run every check. Returns name -> problems, empty lists where it passed.

    `shape` runs first and short-circuits: the rest read keys it verifies, and
    a KeyError deep in another check hides what is actually wrong.
    """
    results = {}
    shape = check_shape(batch)
    results["shape"] = shape
    if shape:
        return results
    for name, fn in CHECKS[1:]:
        results[name] = fn(batch)
    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def report(path: pathlib.Path, results: dict[str, list[str]]) -> bool:
    """Print one file's results. Returns True if it passed."""
    failed = {n: p for n, p in results.items() if p}
    print(f"=== {path.name} ===")
    for name, _ in CHECKS:
        if name not in results:
            continue
        problems = results[name]
        mark = "FAIL" if problems else " ok "
        print(f"  [{mark}] {name}")
        for problem in problems:
            print(f"         - {problem}")
    print(f"  {'PASS' if not failed else f'{sum(len(p) for p in failed.values())} PROBLEM(S)'}\n")
    return not failed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("batch", nargs="*", type=pathlib.Path)
    ap.add_argument("--all", action="store_true",
                    help="check every batch file in the batches folder")
    args = ap.parse_args(argv)

    paths = list(args.batch)
    if args.all:
        paths += [pathlib.Path(p) for p in sorted(glob.glob(str(BATCHES / "batch-*.json")))]
    if not paths:
        ap.error("give a batch file, or --all")

    ok = True
    for path in paths:
        try:
            batch = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"=== {path.name} ===\n  [FAIL] does not parse: {exc}\n")
            ok = False
            continue
        ok &= report(path, validate(batch))

    print("all batches pass" if ok else "SOME BATCHES HAVE PROBLEMS")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
