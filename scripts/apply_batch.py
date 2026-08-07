#!/usr/bin/env python3
"""
apply_batch.py — Stage 2 of the chanting-book workflow, as a real script.

Reads a batch file written by Stage 1 and writes its chants into chanting.py.

    python scripts/apply_batch.py prompts/chanting-book-batch/batches/batch-009-014.json
    python scripts/apply_batch.py <batch> --dry-run     # reconcile and plan only

Why this exists rather than being written by hand each time
-----------------------------------------------------------
It was written by hand each time — three times, for the first three batches —
and the third copy reported "CONTINUES marker removed" without removing it. The
regex matched nothing, success was printed anyway, and a chant that was complete
kept a marker saying it was not. That marker is what gets grepped to find
outstanding work, so a stale one is worse than none.

Roughly forty more batches will go through this. A step that runs forty times
and can silently half-succeed belongs in a tested file, not in a scratchpad.

What it guarantees
------------------
Nothing is written until reconciliation passes. The rules come from the prompt:

  * the manifest must match the entries, or nothing is written at all;
  * every page-map row must name verses that exist in the entry it points at;
  * a continuation must append into the chant already present, never create a
    second dict — one chant becoming two is the failure the rule exists for;
  * a continuation may overwrite exactly one verse, and only when that verse
    was cut by a page break: the existing line must end in the gap marker and
    the incoming line must start with the existing line minus it. Fail either
    and it is an overlap, not a completion, and nothing is written.

Every claim it makes about what it did is checked before it is printed.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import textwrap

GAP = "[…]"
MARKER = "‼"          # the comment marker chanting.py uses
INDENT = "    "

REPO = pathlib.Path(__file__).resolve().parent.parent
CHANTING = REPO / "chanting.py"

# Chant keys written in this order, matching the dicts already in the file.
CHANT_KEYS = ("id", "title_thai", "title_pali", "title_roman", "title_english",
              "book_number", "book_number_printed", "page_start", "layout",
              "source_printed")
LAYERS = ("pali", "pali_roman", "thai", "paiboon", "english")


# ---------------------------------------------------------------------------
# Reconciliation — nothing is written until all of this passes
# ---------------------------------------------------------------------------

def reconcile(batch: dict, existing: dict) -> list[str]:
    """Return every reason this batch must not be written. Empty means safe.

    `existing` maps chant id -> chant dict already in the app.
    """
    problems = []
    entries = batch["chants"]
    by_id = {c["id"]: c for c in entries}
    manifest = batch["batch"]["manifest"]

    if len(manifest) != len(entries):
        problems.append(
            f"manifest lists {len(manifest)} chants but {len(entries)} arrived — "
            f"the run stopped early and the last entry may be incomplete")

    for c in entries:
        if c["id"] not in manifest:
            problems.append(f"{c['id']} was returned but never declared in the manifest")

    for row in batch["batch"]["pages"]:
        cid, spec = row.get("chant", ""), row.get("verses", "none")
        if not cid or spec == "none" or "NOT WRITTEN" in row.get("note", ""):
            continue
        if cid not in by_id:
            problems.append(f"page {row.get('page')} names {cid}, which never arrived")
            continue
        have = {v["number"] for v in by_id[cid]["verses"]}
        missing = sorted(verse_range(spec) - have)
        if missing:
            problems.append(
                f"page {row.get('page')} claims {cid} verses {spec}, "
                f"but the entry has no verse {missing}")

    # A chant that is NOT a continuation must not already be in the app. If it
    # is, either this batch has been applied before or the chant needs merging
    # — and appending it would make one chant into two, which is the failure
    # this whole script exists to prevent. Found by dry-running the script
    # against batch-001-003 after it had already been applied by hand: the
    # continuation guards refused it, and this one did not exist to.
    for c in entries:
        if "continuation_of" in c or "repeat_of" in c:
            continue
        if c["id"] in existing:
            problems.append(
                f"{c['id']} is already in the app — this batch has been applied "
                f"before, or the chant is a reprint that needs merging rather "
                f"than appending")

    for c in entries:
        if "continuation_of" not in c:
            continue
        target = c["continuation_of"]
        if target not in existing:
            problems.append(
                f"{c['id']} continues '{target}', which is not in the app — "
                f"the batches are being applied out of order")
            continue
        problems += check_join(c, existing[target])

    return problems


def verse_range(spec: str) -> set[int]:
    """'1-6' -> {1..6}; '7' -> {7}."""
    lo, _, hi = spec.partition("-")
    return set(range(int(lo), int(hi or lo) + 1))


def check_join(incoming: dict, present: dict) -> list[str]:
    """Verify a continuation joins on cleanly, and classify verse 1 of it."""
    here = [v["number"] for v in present["verses"]]
    arriving = [v["number"] for v in incoming["verses"]]
    overlap = sorted(set(here) & set(arriving))

    if not overlap:
        joined = here + arriving
        if joined != list(range(1, len(joined) + 1)):
            return [f"{incoming['id']}: verses do not run on — the app has "
                    f"{here[0]}-{here[-1]} and the batch brings {arriving[0]}-{arriving[-1]}"]
        return []

    # An overlap is only allowed when it is a page-break completion, and only
    # ever of one verse. Both conditions below must hold.
    if len(overlap) > 1:
        return [f"{incoming['id']}: {len(overlap)} verses overlap ({overlap}) — a "
                f"completion is one verse, so this is a duplicate batch"]

    n = overlap[0]
    old = next(v for v in present["verses"] if v["number"] == n)["pali"]
    new = next(v for v in incoming["verses"] if v["number"] == n)["pali"]
    if not old.rstrip().endswith(GAP):
        return [f"{incoming['id']} verse {n}: the app's line does not end in {GAP}, "
                f"so this is an overlap rather than a line cut by a page break"]
    if not new.startswith(old.replace(GAP, "").rstrip()):
        return [f"{incoming['id']} verse {n}: the incoming line does not extend the "
                f"existing one — a completion lengthens a line, it does not replace it"]
    return []


def plan(batch: dict, existing: dict) -> dict:
    """What applying this batch would do. Safe to call before writing."""
    added, appended, completed = [], [], []
    for c in batch["chants"]:
        if "continuation_of" not in c:
            added.append(c["id"])
            continue
        target = c["continuation_of"]
        here = {v["number"] for v in existing[target]["verses"]}
        for v in c["verses"]:
            (completed if v["number"] in here else appended).append((target, v["number"]))
    return {"added": added, "appended": appended, "completed": completed}


# ---------------------------------------------------------------------------
# Rendering — Python source in the shape chanting.py already uses
# ---------------------------------------------------------------------------

def note(text: str, indent: str) -> str:
    body = textwrap.wrap(text, width=74 - len(indent))
    return f"{indent}# {MARKER} {body[0]}\n" + "".join(f"{indent}#   {l}\n" for l in body[1:])


def render_verse(verse: dict, checks: dict, indent: str) -> str:
    out = "".join(note(f"CHECK [{k['file']}]: {k['issue']}", indent)
                  for k in checks.get(verse["number"], []))
    out += f"{indent}{{\n{indent}{INDENT}'number': {verse['number']},\n"
    # `printed_number` is the number the BOOK sets beside the line, which is
    # not always `number` — a numbered list preceded by unnumbered chanted
    # lines offsets the two. It has to be listed here or it is dropped on the
    # way in, which is the failure mode the "everything must land somewhere"
    # rule exists for.
    for key in ("page", "section", "printed_number"):
        if key in verse:
            out += f"{indent}{INDENT}'{key}': {verse[key]!r},\n"
    for layer in LAYERS:
        out += f"{indent}{INDENT}'{layer}': {verse.get(layer, '')!r},\n"
    return out + f"{indent}}},\n"


def render_chant(chant: dict) -> str:
    per_verse: dict[int, list] = {}
    for k in chant.get("checks", []):
        if k["verse"] is not None:
            per_verse.setdefault(k["verse"], []).append(k)

    out = f"{INDENT}{{\n"
    out += note("COMMENTARY PENDING: set DATA-ONLY. background, meaning, summary, "
                "when_chanted and source still to be written. Verses are complete.",
                INDENT * 2)
    if chant.get("continues"):
        out += note(f"CONTINUES: last verse here is {chant['verses'][-1]['number']}; "
                    f"the rest is not in the app yet.", INDENT * 2)
    for k in (c for c in chant.get("checks", []) if c["verse"] is None):
        out += note(f"CHECK [{k['file']}]: {k['issue']}", INDENT * 2)

    for key in CHANT_KEYS:
        if key in chant:
            out += f"{INDENT * 2}'{key}': {chant[key]!r},\n"
    out += f"{INDENT * 2}'group': 'General chanting',\n"
    if chant.get("english_unverified"):
        out += f"{INDENT * 2}'english_unverified': True,\n"

    invitation = chant.get("invitation") or {}
    out += f"{INDENT * 2}'invitation': {{\n"
    for layer in LAYERS:
        out += f"{INDENT * 3}'{layer}': {invitation.get(layer, '')!r},\n"
    out += f"{INDENT * 2}}},\n{INDENT * 2}'verses': [\n"
    for verse in chant["verses"]:
        out += render_verse(verse, per_verse, INDENT * 3)
    return out + f"{INDENT * 2}],\n{INDENT}}},\n"


# ---------------------------------------------------------------------------
# Applying
# ---------------------------------------------------------------------------

def count_markers(source: str, word: str) -> int:
    return len(re.findall(rf"# {re.escape(MARKER)} {word}", source))


def drop_marker(source: str, chant_id: str, word: str) -> str:
    """Remove a `‼ <word>` comment (and its wrapped lines) from one chant."""
    start = source.rindex(f"{INDENT}{{\n", 0, source.index(f"'id': {chant_id!r},"))
    head_end = source.index(f"'id': {chant_id!r},")
    head, rest = source[start:head_end], source[head_end:]
    kept, dropping = [], False
    for line in head.split("\n"):
        if re.search(rf"# {re.escape(MARKER)} {word}", line):
            dropping = True
            continue
        if dropping and line.strip().startswith("#   "):
            continue
        dropping = False
        kept.append(line)
    return source[:start] + "\n".join(kept) + rest


def apply(batch: dict, source: str) -> tuple[str, dict]:
    """Return the new chanting.py source and a report of what was done."""
    report = {"added": [], "appended": 0, "completed": [], "markers": {}}

    for chant in batch["chants"]:
        if "continuation_of" not in chant:
            continue
        target = chant["continuation_of"]
        anchor = source.index(f"'id': {target!r},")
        v_open = source.index("'verses': [", anchor)
        v_close = source.index("\n        ],\n", v_open)
        block = source[v_open:v_close]

        per_verse: dict[int, list] = {}
        for k in chant.get("checks", []):
            if k["verse"] is not None:
                per_verse.setdefault(k["verse"], []).append(k)

        for verse in chant["verses"]:
            existing = re.search(
                rf"\{{\n\s*'number': {verse['number']},.*?\n\s*\}},\n",
                block, re.DOTALL)
            is_completion = existing and GAP in existing.group(0)
            if is_completion:
                was = re.search(r"'pali': '(.*?)',", existing.group(0)).group(1)
                block = block.replace(
                    existing.group(0),
                    note(f"COMPLETED FROM p{verse.get('page', '?')}: this line was cut "
                         f"by the page break and is now whole. Was: {was}", INDENT * 3)
                    + render_verse(verse, per_verse, INDENT * 3))
                report["completed"].append((target, verse["number"]))
            else:
                block = block.rstrip("\n") + "\n" + render_verse(verse, per_verse, INDENT * 3).rstrip("\n")
                report["appended"] += 1

        source = source[:v_open] + block + source[v_close:]

        if not chant.get("continues"):
            before = count_markers(source, "CONTINUES")
            source = drop_marker(source, target, "CONTINUES")
            after = count_markers(source, "CONTINUES")
            # The claim is checked before it is made. This is the bug that
            # prompted the whole script: the hand-written version said it had
            # removed the marker and had not.
            report["markers"]["CONTINUES"] = (before, after)
            if after >= before:
                raise RuntimeError(
                    f"failed to remove the CONTINUES marker from {target}: "
                    f"count went {before} -> {after}. Refusing to report success.")

    new = [c for c in batch["chants"] if "continuation_of" not in c]
    if new:
        lines = source.split("\n")
        close = next(i for i, l in enumerate(lines) if l == "]")
        body = "".join(render_chant(c) for c in new).rstrip("\n")
        source = "\n".join(lines[:close] + [body] + lines[close:])
        report["added"] = [c["id"] for c in new]

    return source, report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("batch", type=pathlib.Path)
    ap.add_argument("--dry-run", action="store_true",
                    help="reconcile and show the plan, write nothing")
    args = ap.parse_args(argv)

    sys.path.insert(0, str(REPO))
    import chanting

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    existing = {c["id"]: c for c in chanting.CHANTS}

    problems = reconcile(batch, existing)
    if problems:
        print("STOP — nothing written:")
        for p in problems:
            print(f"  • {p}")
        return 1

    steps = plan(batch, existing)
    print(f"reconciled: {len(batch['chants'])} of {len(batch['batch']['manifest'])}")
    print(f"  add      : {steps['added'] or 'none'}")
    print(f"  append   : {len(steps['appended'])} verses")
    print(f"  complete : {steps['completed'] or 'none'}")
    if args.dry_run:
        print("\ndry run — nothing written")
        return 0

    source, report = apply(batch, CHANTING.read_text(encoding="utf-8"))
    CHANTING.write_text(source, encoding="utf-8")
    print(f"\nwritten. added {len(report['added'])}, appended {report['appended']} "
          f"verses, completed {len(report['completed'])} line(s)")
    for word, (before, after) in report["markers"].items():
        print(f"  {word} markers: {before} -> {after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
