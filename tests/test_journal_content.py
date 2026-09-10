"""The journal's file contract, checked.

`content/journal/README.md` states three rules: which fields are required,
that `slug` must be unique because it becomes the URL, and which block types
exist. Nothing enforced any of them, and each fails quietly rather than
loudly:

  * two entries sharing a slug — the second silently wins the lookup, so the
    first is unreachable while its card on the index still links to it, and
    the reader lands on somebody else's entry;
  * an entry with no slug — its card links to a URL that 404s;
  * an entry with no title — a blank heading, rendered without complaint;
  * a mistyped block type — the template's final `{% else %}` renders it as an
    ordinary paragraph, so `"heding"` loses its heading and says nothing.

None of these would break a build or raise in a log. The point of writing
them down here is that a rule nobody checks is a rule that has already been
broken somewhere you have not looked yet.
"""
import glob
import json
import os

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOURNAL_DIR = os.path.join(REPO, "content", "journal")

# From the README's documented shape. A plain string in `blocks` is shorthand
# for an ordinary paragraph, which the loader turns into type 'p'.
KNOWN_BLOCK_TYPES = {"p", "heading", "quote", "pali", "th"}
REQUIRED_FIELDS = ("slug", "date", "title", "blocks")

ENTRY_PATHS = sorted(glob.glob(os.path.join(JOURNAL_DIR, "*.json")))


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def test_there_are_entries_to_check():
    """Guard on the guard: globbing an empty directory passes every test
    below without reading a thing."""
    assert ENTRY_PATHS, f"no journal entries found in {JOURNAL_DIR}"


@pytest.mark.parametrize("path", ENTRY_PATHS, ids=os.path.basename)
def test_entry_is_valid_json(path):
    """The loader skips a malformed file with a warning so one typo cannot
    take /journal down — which is the right behaviour live, and exactly why
    a broken entry would otherwise just quietly stop appearing."""
    load(path)


@pytest.mark.parametrize("path", ENTRY_PATHS, ids=os.path.basename)
def test_entry_has_the_required_fields(path):
    entry = load(path)
    missing = [f for f in REQUIRED_FIELDS if not str(entry.get(f, "")).strip()
               and entry.get(f) != 0]
    assert not missing, f"{os.path.basename(path)} is missing: {', '.join(missing)}"


@pytest.mark.parametrize("path", ENTRY_PATHS, ids=os.path.basename)
def test_entry_blocks_use_known_types(path):
    """A plain string is fine — that is the documented shorthand. A dict with
    a type the template does not know renders as a paragraph and loses
    whatever it was meant to be."""
    entry = load(path)
    faults = []
    for i, block in enumerate(entry.get("blocks", [])):
        if isinstance(block, str):
            continue
        if not isinstance(block, dict):
            faults.append(f"blocks[{i}] is {type(block).__name__}, not a string or object")
            continue
        kind = block.get("type", "p")
        if kind not in KNOWN_BLOCK_TYPES:
            faults.append(f"blocks[{i}] has type {kind!r}")
        if not str(block.get("text", "")).strip():
            faults.append(f"blocks[{i}] has no text")
    assert not faults, f"{os.path.basename(path)}: " + "; ".join(faults)


def test_slugs_are_unique():
    """The slug becomes the URL. Two entries sharing one means the loader's
    slug lookup keeps only the last, and the other becomes unreachable while
    still being listed."""
    seen = {}
    clashes = []
    for path in ENTRY_PATHS:
        slug = load(path).get("slug")
        if slug in seen:
            clashes.append(f"{slug!r} in both {seen[slug]} and {os.path.basename(path)}")
        seen[slug] = os.path.basename(path)
    assert not clashes, "duplicate slugs: " + "; ".join(clashes)


@pytest.mark.parametrize("path", ENTRY_PATHS, ids=os.path.basename)
def test_slug_is_url_safe(path):
    """It goes straight into a path with no escaping, so anything needing to
    be encoded would produce a link that does not match its own route."""
    slug = load(path).get("slug", "")
    assert slug == slug.strip(), f"{slug!r} has surrounding whitespace"
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    bad = sorted(set(slug) - allowed)
    assert not bad, f"{slug!r} contains {bad} — lowercase, digits and hyphens only"


@pytest.mark.parametrize("path", ENTRY_PATHS, ids=os.path.basename)
def test_date_is_iso(path):
    """Entries are sorted by a plain string comparison on this field, so a
    date in another format does not error — it just sorts to the wrong place
    and the journal quietly stops being newest-first."""
    from datetime import datetime
    date = load(path).get("date", "")
    datetime.strptime(date, "%Y-%m-%d")
