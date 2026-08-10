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

The third kind of entry: a merge
--------------------------------
Seventeen chants were entered before page numbers existed. When the page pass
reaches one of their pages there is nothing to add and nothing to append — the
words are already there, typed from the book — and the only thing missing is
the handful of header fields the page supplies: `page_start`, `book_number`,
`layout`, `source_printed`, a `closing`.

Such an entry is marked `merge_only` and carries NO verses, because on a merge
the file's text wins; a second copy could only be ignored, or overwrite text
read from the book by someone holding it. Merging ADDS what is absent and
overwrites nothing — the page a chant was first read from keeps the last word
on anything it already recorded.
"""
from __future__ import annotations

import argparse
import ast
import difflib
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
# What a merge may bring. Scalars first, in the order CHANT_KEYS writes them;
# `closing` is separate because it renders as a block rather than a line.
MERGE_SCALARS = ("book_number", "book_number_printed", "page_start", "layout",
                 "source_printed")


def merge_only(chant: dict) -> bool:
    """True where the entry only adds header fields to a chant already in."""
    return bool(chant.get("merge_only"))


def value_span(text: str, after: int) -> tuple[int, int]:
    """Where the value expression starting at or after `after` ends.

    `chanting.py` writes a field's value two ways. Short ones are a single
    quoted string; long ones are a parenthesised run of adjacent strings that
    the reader joins:

        'pali_roman': (
            "jātipaccayā jarāmaraṇaṃ "
            "sambhavantī,"
        ),

    Both are one Python expression, which is the only description that covers
    them. Scanning for the end of the expression rather than the end of the
    line is what lets a correction reach a wrapped value at all.
    """
    i = after
    while text[i] not in "('\"":
        i += 1
    start = i

    if text[i] != "(":
        return start, skip_string(text, i)

    depth = 0
    while True:
        if text[i] in "'\"":
            i = skip_string(text, i)      # a bracket inside a string is text
            continue
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1


def skip_string(text: str, i: int) -> int:
    """The index just past the string literal beginning at `i`."""
    quote = text[i]
    i += 1
    while True:
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == quote:
            return i + 1
        i += 1


def field_matches(window: str, field: str, value: str) -> list[tuple[int, int]]:
    """Every span in `window` where `field` currently holds exactly `value`.

    Compared by VALUE, not by source text. A correction says what the field
    reads, and how that reading happens to be laid out across lines is not
    something stage 1 can see from a photograph — nor should it have to.
    """
    spans = []
    for match in re.finditer(rf"'{re.escape(field)}':\s*", window):
        try:
            start, end = value_span(window, match.end())
            if ast.literal_eval(window[start:end]) == value:
                spans.append((start, end))
        except (SyntaxError, ValueError, IndexError):
            continue
    return spans


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
        # A merge's page row describes verses that live in the app, not in the
        # batch, so there is nothing here to reconcile it against. The row is
        # still the record of what the page prints and stays as it is.
        if merge_only(by_id[cid]):
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
        if merge_only(c) or "continuation_of" in c or "repeat_of" in c:
            continue
        if c["id"] in existing:
            problems.append(
                f"{c['id']} is already in the app — this batch has been applied "
                f"before, or the chant is a reprint that needs merging rather "
                f"than appending")

    # A merge is the mirror image of the guard above, and needs its own: the
    # one thing that must be true of it is the one thing that must NOT be true
    # of an addition. Marking a chant merge_only when it is not in the app
    # would silently write nothing at all and report success.
    for c in entries:
        if not merge_only(c):
            continue
        if c["id"] not in existing:
            problems.append(
                f"{c['id']} is marked merge_only but is not in the app — a "
                f"merge fills gaps in a chant that is already there, so this "
                f"one would need entering in full instead")
        if "continuation_of" in c:
            problems.append(
                f"{c['id']} is both merge_only and a continuation — a "
                f"continuation brings verses and a merge brings none, so one "
                f"of the two is wrong")
        if c.get("verses"):
            problems.append(
                f"{c['id']} is merge_only but carries verses — on a merge the "
                f"file's text wins, so these could only be ignored, or "
                f"overwrite text typed from the book")
        if not any(c.get(k) for k in MERGE_SCALARS) and not any(
                c.get(k) for k in ("closing", "corrections", "page_markers")):
            problems.append(
                f"{c['id']} is merge_only but brings none of "
                f"{list(MERGE_SCALARS)}, a closing, corrections or page "
                f"markers — there is nothing to merge")
        problems += check_corrections(c, existing.get(c["id"]))

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


def check_corrections(chant: dict, present: dict | None) -> list[str]:
    """Every correction must describe the text that is actually there.

    A correction says "this field currently reads X, and the page shows Y".
    If X is not what the file holds, the entry is describing a version of the
    chant that no longer exists — the batch was written against older data, or
    someone has edited it since — and applying it would either do nothing
    silently or overwrite the wrong thing. Both are worse than refusing.

    Checked against the parsed chant here, and again against the source text
    at write time, because the two can disagree: a value can be present in the
    data and written in the file in a form no literal match will find.
    """
    problems = []
    if present is None:
        return problems

    for fix in chant.get("corrections", []):
        where, field = fix.get("verse"), fix.get("field")
        for key in ("field", "from", "to", "reason"):
            if key not in fix:
                problems.append(
                    f"{chant['id']}: a correction has no {key!r} — a "
                    f"correction without its reason is unreviewable")
        if "field" not in fix:
            continue

        if where is None:
            actual = present.get(field)
        else:
            verse = next((v for v in present["verses"]
                          if v["number"] == where), None)
            if verse is None:
                problems.append(
                    f"{chant['id']}: correction names verse {where}, which "
                    f"the chant does not have")
                continue
            actual = verse.get(field)

        if actual != fix.get("from"):
            problems.append(
                f"{chant['id']} verse {where} {field}: the file does not hold "
                f"the text this correction says it does. Expected "
                f"{fix.get('from')!r}, found {actual!r}")

    for number in chant.get("page_markers", {}):
        if not any(v["number"] == int(number) for v in present["verses"]):
            problems.append(
                f"{chant['id']}: a page marker names verse {number}, which "
                f"the chant does not have")
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
    added, appended, completed, merged = [], [], [], []
    for c in batch["chants"]:
        if merge_only(c):
            fields = [k for k in MERGE_SCALARS if c.get(k)]
            if c.get("closing", {}).get("pali"):
                fields.append("closing")
            if c.get("corrections"):
                fields.append(f"{len(c['corrections'])} corrections")
            if c.get("page_markers"):
                fields.append(f"{len(c['page_markers'])} page markers")
            merged.append(f"{c['id']} ({', '.join(fields)})")
            continue
        if "continuation_of" not in c:
            added.append(c["id"])
            continue
        target = c["continuation_of"]
        here = {v["number"] for v in existing[target]["verses"]}
        for v in c["verses"]:
            (completed if v["number"] in here else appended).append((target, v["number"]))
    return {"added": added, "appended": appended, "completed": completed,
            "merged": merged}


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


def render_closing(closing: dict) -> str:
    """The จบ… formula the book prints under a finished chant.

    Its own function because it is needed in two places. A closing arrives
    with the LAST page of a chant, and a chant that runs across pages reaches
    its last page as a CONTINUATION — so the continuation path needs this as
    much as the path that writes a new chant. Without it the formula is read
    correctly by stage 1, has nowhere to go in stage 2, and is lost.
    """
    out = f"{INDENT * 2}'closing': {{\n"
    for layer in LAYERS:
        out += f"{INDENT * 3}'{layer}': {closing.get(layer, '')!r},\n"
    return out + f"{INDENT * 2}}},\n"


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
    out += f"{INDENT * 2}}},\n"
    # Only where the book prints one. The key is left off entirely otherwise,
    # so an empty closing never renders as a blank centred line.
    if chant.get("closing") and chant["closing"].get("pali"):
        out += render_closing(chant["closing"])
    out += f"{INDENT * 2}'verses': [\n"
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


def closing_is_already_a_verse(source: str, anchor: int, pali: str) -> bool:
    """True where the chant's last verse IS the closing formula.

    The จบ line is set in the same measure as the text above it, so a chant
    transcribed before closings had a field of their own took it as one more
    line. Writing the closing as well would print it twice on the page.

    The match has to tolerate a character or two. Mettānisaṃsasutta is the
    case in hand: its verse 24 reads เมตตานิสังสะสุดตัง with ด where the book
    prints สุตตัง with ต — the same line, one letter out, and an exact
    comparison would miss it and duplicate the formula.
    """
    v_open = source.index("'verses': [", anchor)
    v_close = source.index("\n        ],\n", v_open)
    lines = re.findall(r"'pali': '(.*?)',", source[v_open:v_close])
    if not lines:
        return False
    return difflib.SequenceMatcher(None, lines[-1], pali).ratio() >= 0.85


def chant_bounds(source: str, cid: str) -> tuple[int, int]:
    """Where one chant's dict starts and ends in the source.

    Every replacement below is confined to this window. A line of Pali is
    distinctive, but the book repeats whole formulas across chants — the จบ
    line, the ratana refrain — and a correction that escaped its chant would
    be almost impossible to spot afterwards.
    """
    start = source.index(f"'id': {cid!r},")
    following = source.find("\n    {\n", start)
    return start, (following if following != -1 else len(source))


def apply_corrections(source: str, chant: dict, report: dict) -> str:
    """Replace exact field values, refusing anything ambiguous.

    Matched as whole literals — `'pali': '<the line>',` — and required to
    appear EXACTLY ONCE inside the chant. Zero means the file is written in a
    form this cannot see, and more than one means it could hit either. Both
    raise rather than guess, because a correction applied to the wrong line
    would be a silent corruption of a chanted layer.
    """
    cid = chant["id"]
    for fix in chant.get("corrections", []):
        start, end = chant_bounds(source, cid)
        window = source[start:end]
        spans = field_matches(window, fix["field"], fix["from"])

        if len(spans) != 1:
            raise RuntimeError(
                f"{cid} verse {fix.get('verse')} {fix['field']}: expected the "
                f"old value exactly once inside this chant, found "
                f"{len(spans)}. Nothing written. Looked for: {fix['from']!r}")

        at, to = spans[0]
        window = window[:at] + repr(fix["to"]) + window[to:]
        source = source[:start] + window + source[end:]
        report.setdefault("corrected", []).append(
            f"{cid} v{fix.get('verse')} {fix['field']}")
    return source


def apply_page_markers(source: str, chant: dict, report: dict) -> str:
    """Mark the verse where the printed page turns.

    A chant already in the app has its verses but no record of where its page
    break falls, so `build_page_index` would put every one of them on
    `page_start`. Pabbatopama would then show eleven lines on page 30 where
    the book prints six.
    """
    cid = chant["id"]
    for number, page in sorted(chant.get("page_markers", {}).items(),
                               key=lambda kv: int(kv[0])):
        start, end = chant_bounds(source, cid)
        window = source[start:end]
        marker = f"'number': {int(number)},"

        if window.count(marker) != 1:
            raise RuntimeError(
                f"{cid}: cannot place a page marker on verse {number} — found "
                f"{window.count(marker)} matches for {marker}. Nothing written.")
        if f"'page': {page}," in window:
            continue

        at = window.index(marker)
        line_start = window.rindex("\n", 0, at) + 1
        indent = window[line_start:at]
        window = (window[:at + len(marker)] + f"\n{indent}'page': {page},"
                  + window[at + len(marker):])
        source = source[:start] + window + source[end:]
        report.setdefault("page_markers", []).append(f"{cid} v{number} -> p{page}")
    return source


def merge_into(source: str, chant: dict, report: dict) -> str:
    """Add the header fields a chant already in the app is missing.

    ADDS ONLY. Every write below is guarded by "is this absent?", so a merge
    can never overwrite: the page a chant was first read from keeps the last
    word on anything it already recorded, and this fills the gaps around it.

    The scalars go immediately after `'group'`, which is where `render_chant`
    puts them and where `page_start` already sits on the chants that have one,
    so a merged chant reads the same as one entered whole.
    """
    cid = chant["id"]
    anchor = source.index(f"'id': {cid!r},")
    head = source[anchor:source.index("'verses': [", anchor)]

    # Reversed, because each one is inserted at the SAME point — the line
    # after `'group'` — so the last written ends up first. Walking backwards
    # leaves them in CHANT_KEYS order the right way up.
    for key in reversed(MERGE_SCALARS):
        if chant.get(key) is None or f"'{key}':" in head:
            continue
        at = source.index("'group': ", anchor)
        line_end = source.index("\n", at) + 1
        source = (source[:line_end]
                  + f"{INDENT * 2}'{key}': {chant[key]!r},\n"
                  + source[line_end:])
        report.setdefault("merged", []).append(f"{cid}.{key}")
        anchor = source.index(f"'id': {cid!r},")
        head = source[anchor:source.index("'verses': [", anchor)]

    source = apply_corrections(source, chant, report)
    source = apply_page_markers(source, chant, report)
    anchor = source.index(f"'id': {cid!r},")
    head = source[anchor:source.index("'verses': [", anchor)]

    closing = chant.get("closing") or {}
    if closing.get("pali") and "'closing':" not in head:
        if closing_is_already_a_verse(source, anchor, closing["pali"]):
            report.setdefault("closings_skipped", []).append(cid)
        else:
            head_end = source.index("'verses': [", anchor)
            source = (source[:head_end]
                      + render_closing(closing).lstrip()
                      + f"{INDENT * 2}"
                      + source[head_end:])
            report.setdefault("merged", []).append(f"{cid}.closing")

    return source


def apply(batch: dict, source: str) -> tuple[str, dict]:
    """Return the new chanting.py source and a report of what was done."""
    report = {"added": [], "appended": 0, "completed": [], "markers": {}}

    for chant in batch["chants"]:
        if merge_only(chant):
            source = merge_into(source, chant, report)

    for chant in batch["chants"]:
        if merge_only(chant) or "continuation_of" not in chant:
            continue
        target = chant["continuation_of"]
        anchor = source.index(f"'id': {target!r},")

        # Some things arrive with a chant's LAST page, not its first, so a
        # chant spanning pages meets them on a CONTINUATION: the จบ formula
        # printed beneath it, and the footnote citation keyed to its final
        # line. Both are ADDED where absent and never overwritten — the
        # earlier page's reading wins on anything it already recorded.
        #
        # Titles, page_start and book_number are deliberately NOT here. They
        # belong to the page the chant STARTS on, and a continuation carries
        # none of them by design.
        head_end = source.index("'verses': [", anchor)
        head = source[anchor:head_end]

        if chant.get("source_printed") and "'source_printed':" not in head:
            source = (source[:head_end]
                      + f"'source_printed': {chant['source_printed']!r},\n"
                      + f"{INDENT * 2}" + source[head_end:])
            report["source_printed"] = report.get("source_printed", []) + [target]
            head_end = source.index("'verses': [", anchor)
            head = source[anchor:head_end]

        if chant.get("closing") and chant["closing"].get("pali"):
            if "'closing':" not in head:
                source = (source[:head_end]
                          + render_closing(chant["closing"]).lstrip()
                          + f"{INDENT * 2}"
                          + source[head_end:])
                report["closings"] = report.get("closings", []) + [target]

        v_open = source.index("'verses': [", anchor)
        v_close = source.index("\n        ],\n", v_open)
        block = source[v_open:v_close]

        per_verse: dict[int, list] = {}
        for k in chant.get("checks", []):
            if k["verse"] is not None:
                per_verse.setdefault(k["verse"], []).append(k)

        for verse in chant["verses"]:
            # The trailing newline is optional. `block` is sliced to stop at the
            # verses list's own closing bracket, so the LAST verse's `},` sits at
            # the very end with no newline after it — and a page-break stub is
            # always the last verse, which made this branch unreachable exactly
            # when it was needed. It appended a second verse 4 instead.
            existing = re.search(
                rf"\{{\n\s*'number': {verse['number']},.*?\n\s*\}},(?:\n|\Z)",
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

        # A verse number identifies a verse, so the same one twice is never a
        # thing the book can mean. Checked here rather than trusted, because the
        # duplicate this catches imported cleanly and passed the whole suite:
        # nothing downstream reads verse numbers strictly enough to notice.
        written = re.findall(r"\n\s*'number': (\d+),", block)
        repeated = sorted({n for n in written if written.count(n) > 1}, key=int)
        if repeated:
            raise RuntimeError(
                f"{target}: verse number(s) {', '.join(repeated)} appear twice "
                f"after writing. A completion was appended instead of replacing "
                f"the line it completes. Nothing has been saved.")

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

    # A merge is neither an addition nor a continuation, and must be excluded
    # here explicitly. Without the first clause it would fall through to this
    # line and be appended as a SECOND copy of a chant already in the file —
    # exactly the one-chant-becomes-two failure the script exists to prevent.
    new = [c for c in batch["chants"]
           if not merge_only(c) and "continuation_of" not in c]
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
    print(f"  merge    : {steps['merged'] or 'none'}")
    if args.dry_run:
        print("\ndry run — nothing written")
        return 0

    source, report = apply(batch, CHANTING.read_text(encoding="utf-8"))
    CHANTING.write_text(source, encoding="utf-8")
    print(f"\nwritten. added {len(report['added'])}, appended {report['appended']} "
          f"verses, completed {len(report['completed'])} line(s), merged "
          f"{len(report.get('merged', []))} field(s)")
    for field in report.get("merged", []):
        print(f"  merged {field}")
    for field in report.get("corrected", []):
        print(f"  corrected {field}")
    for marker in report.get("page_markers", []):
        print(f"  page marker {marker}")
    # Reported rather than passed over. A closing that was offered and not
    # written is a thing the batch believed and the file overruled, and it
    # should be visible without reading the diff.
    for cid in report.get("closings_skipped", []):
        print(f"  closing NOT written for {cid}: its last verse already is the "
              f"formula, and writing it would print it twice")
    for word, (before, after) in report["markers"].items():
        print(f"  {word} markers: {before} -> {after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
