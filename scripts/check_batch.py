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
  * A line the page break cut in half is well formed: both chanted layers agree
    it was cut, the chant is listed as continuing, and the cut falls on the
    last verse. Without this a `[…]` can be written that nothing will ever
    complete, and the app keeps the ellipsis for good.
  * A `merge_only` entry — one that only hands stage 2 the header fields a
    chant already in the app is missing — brings something, and brings no
    verses. Every verse-walking check above skips it, because there are
    legitimately none to walk.

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
# The two layers that REPRODUCE the page rather than gloss it. Where a page
# break cuts a line, these two must agree about it; `english` need not, because
# the gloss of half a sentence is not half the gloss of the whole one.
CHANTED_LAYERS = ("pali", "pali_roman")
# What stage 1 writes where a page stops mid-line. `check_pages` spells it the
# same way, and the two must not drift apart.
CUT = "[…]"
# Paiboon+ uses k, t, p and ŋ. None of these can legitimately appear.
RTGS_TELLS = ("kh", "th", "ph", "ng")
# Fields a DATA-ONLY batch defers to stage 3 rather than writing now.
COMMENTARY = ("background", "meaning", "summary", "when_chanted", "source")
# What a merge entry is allowed to bring. A merge carrying none of these adds
# nothing, and belongs out of the batch rather than in it.
MERGEABLE = ("page_start", "book_number", "book_number_printed", "layout",
             "source_printed", "closing", "corrections", "page_markers")

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


def merge_only(chant: dict) -> bool:
    """True where the entry ADDS to a chant already in the app.

    Seventeen chants were set before page numbers existed. When the page pass
    reaches one of their pages, the batch's job is to hand stage 2 the few
    things the app is missing — `page_start`, `book_number`, `source_printed`,
    a `closing` — and nothing else. Restating the verses would be worse than
    useless: the merge rule says the file's text wins, so a second copy could
    only ever be ignored or, if anyone got the rule wrong, overwrite text Josh
    typed with the book in front of him.

    So a merge entry legitimately has no `verses`, and every check below that
    walks verses has to know that. Without this the validator demanded a copy
    of exactly the text the workflow exists to protect.
    """
    return bool(chant.get("merge_only"))


def verses_of(chant: dict) -> list:
    """The entry's verses, or none for a merge. Never raises."""
    return chant.get("verses") or []


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
        if "checks" not in chant:
            problems.append(f"{cid}: has no 'checks' array")

        if merge_only(chant):
            if not any(chant.get(key) for key in MERGEABLE):
                problems.append(
                    f"{cid}: merge_only but carries none of {list(MERGEABLE)} "
                    f"— a merge that adds nothing to the app has no reason to "
                    f"be in the batch")
            if chant.get("verses"):
                problems.append(
                    f"{cid}: merge_only but carries verses — on a merge the "
                    f"file's text wins, so these could only be ignored, or "
                    f"overwrite text typed from the book")
        else:
            if "verses" not in chant:
                problems.append(f"{cid}: has no 'verses' array")
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


def check_latin_only(batch: dict) -> list[str]:
    """A romanised layer holds Latin letters and nothing that merely looks Latin.

    Cyrillic а, о, е and с are pixel-identical to their Latin twins in most
    fonts. One in a `pali_roman` value is invisible on screen, survives every
    other check here, breaks any search for the word, and stays in the data
    for good. Two got in during one session — jīvitindriyupacchedа and
    jegucchо, on consecutive pages — and only a scan for the character class
    found them.

    Checked on the romanised layers only. `pali` and `thai` are Thai script by
    design, and `paiboon` carries ɔ ɛ ə ʉ ŋ, which are Latin letters proper.
    """
    problems = []
    for chant in batch["chants"]:
        for verse in verses_of(chant):
            for field in ("pali_roman", "paiboon"):
                for char in verse.get(field, ""):
                    if not char.isalpha():
                        continue
                    if "LATIN" in unicodedata.name(char, ""):
                        continue
                    problems.append(
                        f"{chant['id']} verse {verse.get('number')}: {field} "
                        f"contains {char!r} (U+{ord(char):04X}, "
                        f"{unicodedata.name(char, 'unnamed')}), which is not a "
                        f"Latin letter — it only looks like one"
                    )
    return problems


def check_pali_untouched(batch: dict) -> list[str]:
    """`pali` is the book's Thai script; `pali_roman` is IAST. Neither leaks.

    Running Paiboon+ over a `pali` value corrupts the chanted layer, and it is
    invisible once downstream — which is why it is checked here, against the
    script each field is supposed to be written in.
    """
    problems = []
    for chant in batch["chants"]:
        for verse in verses_of(chant):
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
        for verse in verses_of(chant):
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
        for verse in verses_of(chant):
            if verse.get("paiboon") and not verse.get("thai"):
                problems.append(
                    f"{chant['id']} verse {verse.get('number')}: paiboon is "
                    f"set but thai is empty — Paiboon+ romanises the Thai, so "
                    f"there was nothing to romanise")
    return problems


def check_printed_numbers(batch: dict) -> list[str]:
    """The numbers the BOOK prints beside its lines are sane.

    `printed_number` is separate from `number`: the app's own identity for a
    line versus what the page shows beside it. They part company wherever a
    numbered list follows unnumbered chanted lines — the Dasadhamma Sutta's
    nidana makes the book's item 1 into verse 3.

    It went in with no guard at all, which is the same gap this whole script
    exists to close: a key nothing validates is a key that can be quietly
    wrong. Three things must hold, and each has a way of going wrong that the
    page would not make obvious:

      * a positive whole number — the book numbers from 1, never 0 or a string;
      * no repeats inside one chant — two lines printed '7.' means one of them
        was mis-transcribed, and both would render as 7;
      * ascending in verse order — a list that runs 5, 4, 6 is a pair swapped.

    Not checked: that the numbers start at 1. A continuation legitimately
    arrives carrying 19-30, because the first eighteen went in with the
    previous page.
    """
    problems = []
    for chant in batch["chants"]:
        seen, previous = {}, None
        for verse in verses_of(chant):
            if "printed_number" not in verse:
                continue
            n, where = verse["printed_number"], verse.get("number")

            if not isinstance(n, int) or isinstance(n, bool) or n < 1:
                problems.append(
                    f"{chant['id']} verse {where}: printed_number is {n!r} — "
                    f"it must be a positive whole number")
                continue
            if n in seen:
                problems.append(
                    f"{chant['id']}: verses {seen[n]} and {where} both carry "
                    f"printed_number {n} — the book cannot print the same "
                    f"number twice in one list")
            seen[n] = where
            if previous is not None and n <= previous:
                problems.append(
                    f"{chant['id']} verse {where}: printed_number {n} follows "
                    f"{previous} — the book's numbers ascend down the page")
            previous = n
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
        # A merge's page row describes verses that are already in the app, not
        # in the batch. There is nothing here to check them against, and
        # demanding they be present would demand the copy merge_only exists to
        # avoid. The row still stands as the record of what the page prints.
        if merge_only(by_id[cid]):
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
        for verse in verses_of(chant):
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
        for verse in verses_of(chant):
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


def check_line_breaks_agree(batch: dict) -> list[str]:
    """A couplet break in `pali` is a couplet break in `pali_roman` too.

    This replaced a check for "raw newlines inside string values", which was
    unfalsifiable in both directions: JSON cannot hold a literal newline
    inside a string at all — `json.load` raises before any check runs — so it
    could never catch what it named, and it fired on every legitimate couplet
    break instead. It flagged the five-line ratana stanza on page 20, which
    is stored exactly as `chanting.py` has stored such breaks since the first
    chant.

    What IS worth checking is that the two chanted layers break in the same
    places. They are the same words in two scripts, so a break present in one
    and missing from the other means one of them was typed from something
    other than the page.
    """
    problems = []
    for chant in batch["chants"]:
        for verse in verses_of(chant):
            pali, roman = verse.get("pali", ""), verse.get("pali_roman", "")
            if not pali or not roman:
                continue
            if pali.count("\n") != roman.count("\n"):
                problems.append(
                    f"{chant['id']} verse {verse.get('number')}: pali breaks "
                    f"into {pali.count(chr(10)) + 1} lines but pali_roman "
                    f"into {roman.count(chr(10)) + 1} — the two chanted "
                    f"layers must break in the same places")
    return problems


def check_cut_lines(batch: dict) -> list[str]:
    """A line the page break cut in half has to be able to find its other half.

    Where a page stops mid-unit, stage 1 marks the partial line with `[…]` and
    the next batch carries the SAME verse number with the line whole.
    `apply_batch` replaces the verse and `check_pages` proves the completion
    starts with the partial — but only if the partial is well formed, and until
    now nothing checked that. All three failures below were confirmed to pass
    silently before this existed.

    Three ways it goes wrong, all invisible afterwards:

    1. `pali` is cut and `pali_roman` is not, or the reverse. The two chanted
       layers then disagree about where the page break fell, and `check_pages`
       holds the uncut one to a prefix test it was never given the text for.
    2. The chant is not listed in `batch_status.continues`. Nothing will ever
       be sent to complete the line, and the app keeps a `[…]` for good — a
       reader meets an ellipsis mid-chant and there is no record it is owed.
    3. The cut verse is not the LAST of its chant. A page break can only fall
       at the end of what was shown, so a `[…]` anywhere else is a marker left
       in by hand rather than a real cut.

    `english` is deliberately not held to rule 1. The gloss of half a sentence
    is not half the gloss of the whole one — `check_pages` exempts it for the
    same reason — so it may carry the marker or not.
    """
    problems = []
    for chant in batch["chants"]:
        verses = verses_of(chant)
        last = verses[-1]["number"] if verses else None
        continues = set(batch["batch_status"].get("continues", []))

        for verse in verses:
            n = verse.get("number")
            cut = [layer for layer in CHANTED_LAYERS
                   if verse.get(layer, "").rstrip().endswith(CUT)]
            if not cut:
                continue

            uncut = [layer for layer in CHANTED_LAYERS
                     if verse.get(layer) and layer not in cut]
            if uncut:
                problems.append(
                    f"{chant['id']} verse {n}: {cut} end in {CUT} but {uncut} "
                    f"do not — the two chanted layers disagree about where the "
                    f"page break fell")
            if chant["id"] not in continues:
                problems.append(
                    f"{chant['id']} verse {n}: ends in {CUT} but the chant is "
                    f"not in batch_status.continues — nothing will be sent to "
                    f"complete it and the app would keep the {CUT} for good")
            if n != last:
                problems.append(
                    f"{chant['id']} verse {n}: ends in {CUT} but is not the "
                    f"last verse ({last} is) — a page break can only cut the "
                    f"line the page stopped on")
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


def check_corrections_are_reviewable(batch: dict) -> list[str]:
    """A correction says what it changes, to what, and why.

    Corrections overwrite a chanted layer that is already in the app, which
    makes them the most dangerous thing a batch can carry. The guard against
    misuse is not machinery — stage 2 already refuses anything ambiguous — it
    is that every one arrives with its reason attached and can be read back
    later by someone holding the book.

    A correction that changes nothing is caught here too. It means the batch
    was written against a copy of the file that has since moved on, and the
    rest of that entry should be distrusted.
    """
    problems = []
    for chant in batch["chants"]:
        for fix in chant.get("corrections", []):
            if not isinstance(fix, dict):
                problems.append(
                    f"{chant['id']}: a correction is {type(fix).__name__}, "
                    f"not an object")
                continue
            for key in ("verse", "field", "from", "to", "reason"):
                if key not in fix:
                    problems.append(
                        f"{chant['id']}: a correction has no {key!r}")
            if fix.get("from") == fix.get("to"):
                problems.append(
                    f"{chant['id']} verse {fix.get('verse')} "
                    f"{fix.get('field')}: the correction changes nothing — "
                    f"'from' and 'to' are identical")
            if not str(fix.get("reason", "")).strip():
                problems.append(
                    f"{chant['id']} verse {fix.get('verse')}: a correction "
                    f"has an empty reason, so nobody can review it")

        for number, page in (chant.get("page_markers") or {}).items():
            if not str(number).isdigit():
                problems.append(
                    f"{chant['id']}: page marker key {number!r} is not a "
                    f"verse number")
            if not isinstance(page, int) or page < 1:
                problems.append(
                    f"{chant['id']}: page marker for verse {number} is "
                    f"{page!r} — a page is a positive whole number")
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
    ("latin only", check_latin_only),
    ("five layer keys", check_layer_keys),
    ("layers not invented", check_layers_not_invented),
    ("printed numbers", check_printed_numbers),
    ("manifest", check_manifest),
    ("page map", check_page_map),
    ("pages ascend", check_pages_ascend),
    ("diacritics", check_diacritics),
    ("depth", check_depth),
    ("line breaks agree", check_line_breaks_agree),
    ("cut lines", check_cut_lines),
    ("page blocks", check_blocks),
    ("checks readable", check_checks_are_readable),
    ("corrections reviewable", check_corrections_are_reviewable),
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
    # Every problem this script reports may contain IAST or Thai, and a Windows
    # console is cp1252 by default — so the report crashed on the first line
    # carrying a macron, taking the exit code with it. A checker that dies while
    # naming a fault is worse than one that finds nothing.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

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
