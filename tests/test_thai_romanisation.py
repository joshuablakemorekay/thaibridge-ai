"""Guards for the Thai romanisation, added after the 2026-09-10 audit.

That audit found the same word romanised two ways in five places, the velar
nasal written `ng` in twenty-six, and a vowel table whose example words did not
contain the vowel they were illustrating. Every one of those was a slow drift
away from a house style this project had already written down.

The romanisation was fixed by hand. Nothing stopped it drifting again, which is
the actual bug — `tests/test_contents_roman.py` asserts the `ng` rule, but only
for the chanting contents, so the teaching data was never covered.

These tests close that gap. They cannot tell you a reading is *right* — only a
native speaker can — but they can tell you it is written in the system this app
claims to use, and that a vowel row demonstrates its own vowel.
"""
import unicodedata

import pytest

import app
import register_levels
import thai_consonants
import thai_reading
import thai_registers

# Combining marks that say nothing about WHICH vowel a letter is: the four tone
# marks, which sit on top, and the dot below, which this table uses on the row
# itself to mark a short vowel but which example words do not carry.
COMBINING = {"̀", "́", "̂", "̌", "̣"}


def strip_tones(text):
    return "".join(c for c in unicodedata.normalize("NFD", text)
                   if c not in COMBINING)


def walk_paiboon(node, path="", found=None):
    """Every string stored under a 'paiboon' key, anywhere in a structure."""
    if found is None:
        found = []
    if isinstance(node, dict):
        for key, value in node.items():
            where = f"{path}.{key}"
            if key == "paiboon" and isinstance(value, str):
                found.append((where, value))
            else:
                walk_paiboon(value, where, found)
    elif isinstance(node, (list, tuple)):
        for i, item in enumerate(node):
            walk_paiboon(item, f"{path}[{i}]", found)
    return found


def module_paiboon(module):
    out = []
    for name in dir(module):
        if name.isupper():
            walk_paiboon(getattr(module, name), f"{module.__name__}.{name}", out)
    return out


ALL_PAIBOON = (
    module_paiboon(app)
    + module_paiboon(thai_reading)
    + module_paiboon(thai_registers)
    + module_paiboon(register_levels)
)


def test_the_walker_actually_found_the_data():
    """A guard on the guard. If a refactor renames these structures, the checks
    below would pass by finding nothing at all, which is the worst kind of
    green."""
    assert len(ALL_PAIBOON) > 500, f"only found {len(ALL_PAIBOON)} paiboon fields"


def test_paiboon_fields_use_the_paiboon_alphabet():
    """Paiboon writes ŋ, never ng. A field using 'ng' is some other
    romanisation wearing Paiboon's clothes — the exact drift the audit found in
    twenty-six places, including all ten in the 44-consonant chart.

    Collected into one assertion rather than parametrised over all 6,000-odd
    fields: a rule this broad should report every offender at once, and one
    test id per data row would drown the suite.
    """
    faults = [f"{where} → {reading}" for where, reading in ALL_PAIBOON
              if "ng" in reading]
    assert not faults, (
        f"{len(faults)} paiboon field(s) use 'ng' where Paiboon writes \u014b:\n  "
        + "\n  ".join(faults[:20])
    )


@pytest.mark.parametrize("letter", thai_consonants.CONSONANTS,
                         ids=lambda c: c["slug"])
def test_consonant_names_and_sounds_use_the_paiboon_alphabet(letter):
    """The letter's name and its sound are both shown to the learner — the
    sound appears on the card as 'sounds like "…"'. ง carried 'ng' there long
    after its name had been corrected."""
    assert "ng" not in letter["name"], f'{letter["char"]} name → {letter["name"]}'
    assert "ng" not in letter["sound"], f'{letter["char"]} sound → {letter["sound"]}'


# ── The vowel table ──────────────────────────────────────────────────────
#
# Six rows are wrong ON PURPOSE. Fixing them needs Thai that appears nowhere
# else in this codebase, so the audit escalated them to a native speaker rather
# than inventing replacements: docs/vowel-review-2026-09-10.md.
#
# Delete a number from this set the moment its row is corrected. The test
# directly below makes sure the set cannot quietly rot into an excuse.
AWAITING_TEACHER = {20, 24, 25, 29, 30, 32}

# Of those six, these are the ones this check can actually prove wrong. Rows 24
# and 25 (เอียะ, เอือะ) are held too, but their fault is that the example is the
# LONG form of the same vowel, and with the length dot stripped the check cannot
# see the difference. They are excluded above and listed here so nobody reads
# their absence below as a clean bill of health.
DETECTABLY_BROKEN = {20, 29, 30, 32}

VOWEL_ROWS = (app.THAI_VOWELS_32["long_vowels"]
              + app.THAI_VOWELS_32["short_vowels"])


def demonstrates_its_own_vowel(row):
    """Does the example word's reading actually contain the row's vowel?

    Returns None if it does, or a string explaining the fault. Tone marks are
    stripped first, since they sit above the vowel and say nothing about which
    vowel it is.
    """
    vowel = strip_tones(row["paiboon"])
    example = strip_tones(row["example_word"]["paiboon"])
    if vowel not in example:
        return f'{example!r} does not contain {vowel!r}'
    # A short row must not be illustrated by a long vowel. This is what caught
    # แอะ (short) being demonstrated with แก้ว (gɛ̂ɛo, long).
    if row["type"] == "short" and len(vowel) == 1 and vowel * 2 in example:
        return f'{example!r} is long, but the row is short'
    return None


@pytest.mark.parametrize("row", [r for r in VOWEL_ROWS
                                 if r["number"] not in AWAITING_TEACHER],
                         ids=lambda r: f'{r["number"]}-{r["thai"]}')
def test_each_vowel_row_demonstrates_its_own_vowel(row):
    """The bug this whole class of test exists for: a row teaching เอว whose
    example word was แถว, which is แอว — so the learner met the wrong vowel
    under the right heading."""
    fault = demonstrates_its_own_vowel(row)
    assert fault is None, f'row {row["number"]} ({row["thai"]}): {fault}'


@pytest.mark.parametrize("number", sorted(DETECTABLY_BROKEN))
def test_rows_awaiting_the_teacher_are_still_actually_broken(number):
    """Stops AWAITING_TEACHER becoming a permanent excuse.

    If a row in that set starts passing, somebody has fixed it and forgotten to
    take it off the list — at which point the row silently stops being checked.
    This test fails until the number is removed.
    """
    row = next(r for r in VOWEL_ROWS if r["number"] == number)
    fault = demonstrates_its_own_vowel(row)
    assert fault is not None, (
        f'row {number} ({row["thai"]}) now looks correct — remove {number} from '
        f'AWAITING_TEACHER so it is checked from here on'
    )
