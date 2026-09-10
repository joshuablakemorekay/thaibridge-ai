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
import glob
import json
import os
import re
import unicodedata

import pytest

import ai_agent
import app
import register_levels
import survival
import thai_consonants
import thai_reading
import thai_registers

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def json_paiboon():
    """The same fields, in the content files loaded at runtime.

    These are the ones no grep over the .py files will ever find. A missing
    tone mark on ขอโทษ sat in a monk lesson for months for exactly that
    reason — the data is real, and it lived somewhere nothing looked.
    """
    out = []
    pattern = os.path.join(REPO, "content", "**", "*.json")
    for path in sorted(glob.glob(pattern, recursive=True)):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        walk_paiboon(data, os.path.relpath(path, REPO), out)
    return out


JSON_PAIBOON = json_paiboon()

ALL_PAIBOON = (
    module_paiboon(app)
    + module_paiboon(survival)
    + module_paiboon(thai_reading)
    + module_paiboon(thai_registers)
    + module_paiboon(register_levels)
    + JSON_PAIBOON
)


def test_the_walker_actually_found_the_data():
    """A guard on the guard. If a refactor renames these structures, the checks
    below would pass by finding nothing at all, which is the worst kind of
    green."""
    assert len(ALL_PAIBOON) > 500, f"only found {len(ALL_PAIBOON)} paiboon fields"
    # Counted separately: the content files are found by globbing a directory
    # rather than by importing a module, so they can go missing without any
    # import error to say so, and the rest of the total would hide it.
    assert len(JSON_PAIBOON) > 100, f"only found {len(JSON_PAIBOON)} in content/"


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


# ── One word, one reading ────────────────────────────────────────────────
#
# The audit's most productive check, made permanent. It is what found ตรง
# written three ways (dtroŋ, troŋ, droŋ), ห้อง long in three places and short
# in two, and a missing tone on ขอโทษ. None of those are `ng`, so the check
# above would never have caught them, and without this one today's fixes are
# free to drift straight back.
#
# The imported dictionary is excluded. Its 4,894 entries come from a third
# party and carry their own romanisation — kh, a superscript ʰ, an IPA length
# mark — so measuring them against house style produces 131 findings about
# somebody else's transcription rather than about this app's teaching.
IMPORTED_CORPORA = {"YAITRON_ENTRIES"}

# ณ is a letter AND a word. 'n' is the consonant's sound on the alphabet
# chart; 'ná' is the preposition meaning "at". One glyph, two different
# things, so this was never a disagreement.
NOT_ONE_WORD = {"ณ"}

# Four readings that evidence in this repo cannot settle — they need an ear,
# not a rule. Sent to the teacher alongside the vowel rows.
#   ศรัทธา    sà-rát-taa / sàt-taa   — is the ร sounded?
#   สวดมนต์   sùat-mon / sùuat mon   — and ดวงอาทิตย์ duaŋ / duuaŋ: this app
#   ดวงอาทิตย์                         writes อัว as 'ua' in the vowel table but
#                                     'uua' in its examples, and that has to be
#                                     decided once for every word at a time.
#   เสวย      sà-wəəi / sà-wə̌əi      — royal vocabulary, irregular tone.
AWAITING_TEACHER_WORDS = {"ศรัทธา", "สวดมนต์", "ดวงอาทิตย์", "เสวย"}


def readings_by_word():
    """Every Thai string mapped to the set of readings given for it."""
    found = {}
    def collect(node):
        if isinstance(node, dict):
            thai, paiboon = node.get("thai"), node.get("paiboon")
            if (isinstance(thai, str) and isinstance(paiboon, str)
                    and thai.strip() and paiboon.strip()):
                found.setdefault(thai, set()).add(paiboon)
            for value in node.values():
                collect(value)
        elif isinstance(node, (list, tuple)):
            for item in node:
                collect(item)

    for module in (app, survival, thai_reading, thai_registers, register_levels):
        for name in dir(module):
            if name.isupper() and name not in IMPORTED_CORPORA:
                collect(getattr(module, name))
    for path in sorted(glob.glob(os.path.join(REPO, "content", "**", "*.json"),
                                 recursive=True)):
        with open(path, encoding="utf-8") as fh:
            collect(json.load(fh))
    return found


def disagreements(words):
    """Words whose readings differ by more than hyphenation.

    Hyphen and space are treated as the same character throughout, because
    whether a hyphen joins syllables inside a word is an open style question
    here and not a correctness one. Twelve words differ only that way.
    """
    out = {}
    for thai, readings in words.items():
        if thai in NOT_ONE_WORD:
            continue
        bare = {r.replace("-", " ").strip() for r in readings}
        if len(bare) > 1:
            out[thai] = sorted(readings)
    return out


ALL_DISAGREEMENTS = disagreements(readings_by_word())


def test_each_word_has_one_reading():
    """ตรง was written dtroŋ, troŋ and droŋ in three different places, and a
    learner meeting two of them has no way to know which to trust."""
    faults = {k: v for k, v in ALL_DISAGREEMENTS.items()
              if k not in AWAITING_TEACHER_WORDS}
    assert not faults, (
        f"{len(faults)} word(s) romanised more than one way:\n  "
        + "\n  ".join(f"{k} -> {v}" for k, v in sorted(faults.items()))
    )


@pytest.mark.parametrize("word", sorted(AWAITING_TEACHER_WORDS))
def test_words_awaiting_the_teacher_still_disagree(word):
    """Same purpose as the vowel-row version: if one of these is settled and
    left on the list, it silently stops being checked from then on."""
    assert word in ALL_DISAGREEMENTS, (
        f"{word} now has one reading — remove it from AWAITING_TEACHER_WORDS "
        f"so it is checked from here on"
    )


# ── Aspiration ───────────────────────────────────────────────────────────
#
# This romanisation marks no aspiration: ข and ค are both k, ผ and พ are
# both p, ถ ท ธ are all t. Writing kh, ph or th is RTGS leaking in.
#
# Never scanned across the whole corpus until the monk-lesson audit, which
# is how three survived: sìk-khǎa-bòt, wí-gaan-lá-phôot and phʉ̂a. Each sat
# in a different file, and none contains ng, so no existing check saw them.
def teaching_paiboon():
    """Readings this project wrote, without the imported dictionary.

    The exclusion is the whole reason this check is possible: the Yaitron
    corpus uses kh, ph and th throughout by design, so measuring it here
    would bury three real faults under 312 false ones.
    """
    out = []
    for module in (app, survival, thai_reading, thai_registers, register_levels):
        for name in dir(module):
            if name.isupper() and name not in IMPORTED_CORPORA:
                walk_paiboon(getattr(module, name), f"{module.__name__}.{name}", out)
    return out + JSON_PAIBOON


TEACHING_PAIBOON = teaching_paiboon()


def test_the_aspiration_walker_found_the_data():
    """Guard on the guard: excluding one large structure by name is exactly
    the sort of filter that can quietly exclude everything."""
    assert len(TEACHING_PAIBOON) > 1000, (
        f"only found {len(TEACHING_PAIBOON)} readings outside the dictionary")


def test_no_reading_marks_aspiration():
    """ข = k, พ = p, ถ = t. A reading with kh, ph or th in it is written in
    RTGS, which spells three of the app's letters differently from the
    Alphabet page the learner is being taught from."""
    faults = [f"{where} → {reading}" for where, reading in TEACHING_PAIBOON
              if re.search(r"(kh|ph|th)", reading)]
    assert not faults, (
        f"{len(faults)} reading(s) mark aspiration, which this system does not:\n  "
        + "\n  ".join(faults[:20]))


# ── The AI tutor's system prompt ─────────────────────────────────────────
#
# Errors here never appear on a page. They are instructions to the model, so
# they reach the learner as something the tutor says — which is why this block
# sat wrong from the first commit until it was read line by line.
with open(os.path.join(REPO, "ai_agent.py"), encoding="utf-8") as _fh:
    AGENT_SOURCE = _fh.read()


def consonant_rules_block():
    """Just the Consonant Rules section, not the whole file.

    Scoped deliberately: the prose elsewhere legitimately contains the letters
    "ng" while explaining what ŋ sounds like, and a check over the whole file
    would either trip on that or be watered down until it caught nothing.
    """
    start = AGENT_SOURCE.index("**Consonant Rules")
    end = AGENT_SOURCE.index("**", AGENT_SOURCE.index("\n", start))
    return AGENT_SOURCE[start:end]


def test_tutor_prompt_agrees_with_the_alphabet_page():
    """The prompt taught ข = kh, พ = ph and ถ = th while the Alphabet page
    taught k, p and t, so the tutor and the chart disagreed about three
    letters — and the prompt's own examples quietly sided with the chart."""
    by_letter = {c["char"]: c["sound"] for c in thai_consonants.CONSONANTS}
    faults = []
    for line in consonant_rules_block().splitlines():
        for chunk in line.split("·"):
            if "=" not in chunk:
                continue
            left, _, right = chunk.partition("=")
            letters = [ch for ch in left if "ก" <= ch <= "ฮ"]
            words = right.strip().split()
            if not letters or not words or not words[0].isalpha():
                continue
            for letter in letters:
                expected = by_letter.get(letter)
                if expected and expected != words[0]:
                    faults.append(
                        f"prompt says {letter} = {words[0]}, "
                        f"alphabet page says {expected}")
    assert not faults, "; ".join(faults)


def test_no_anti_example_forbids_its_own_answer():
    """Six examples read like 'ครับ = kráp (NOT khrap or kráp)', telling the
    model the correct answer was also wrong. Cheap to write, near-invisible to
    review, and it degrades every reply the tutor gives."""
    faults = []
    for match in re.finditer(r"- (\S+) = ([^(]+?)\s*\(NOT ([^)]+)\)",
                             AGENT_SOURCE):
        right = match.group(2).strip()
        alternatives = [a.strip() for a in re.split(r"\bor\b", match.group(3))]
        if right in alternatives:
            faults.append(f"{match.group(1)} = {right} (NOT {match.group(3)})")
    assert not faults, ("an example forbids the answer it gives: "
                        + "; ".join(faults))


def test_tutor_prompt_examples_use_the_paiboon_alphabet():
    """The prompt instructed the model to always write ŋ and then wrote "ng"
    itself, in dtɔ̀ɔng-gaan. A rule broken by its own example teaches the
    example."""
    # Finding these is fiddlier than it looks. The prompt says «ŋ = ng sound
    # (as in "sing")» and «never write "ng"» in ordinary English, so a plain
    # search for the letters reports the rule itself. What marks a token as
    # romanisation rather than prose is a Paiboon-only character: ɔ ɛ ʉ ə ŋ or
    # a combining tone mark. A token carrying one of those AND "ng" is the
    # contradiction.
    #
    # The first version of this test looked for Thai script before the token,
    # and passed while catching nothing — dtɔ̀ɔng-gaan sits in an English
    # sentence with no Thai anywhere near it.
    paiboon_only = "ɔɛʉə" + "ŋ" + "̀́̂̌"
    faults = []
    for token in re.findall(r"[^\s,;:()\"]+", AGENT_SOURCE):
        if "ng" in token and any(ch in token for ch in paiboon_only):
            faults.append(token)
    assert not faults, ("prompt examples using 'ng' where Paiboon writes ŋ: "
                        + "; ".join(sorted(set(faults))))
