"""
fix_paiboon.py — Post-processing script to clean up quality issues in
yaitron_dictionary_paiboon.tsv without re-running the full generation.

WHAT IT DOES:
  1. Flags Thai abbreviations (กน., ชม., etc.) — marks paiboon as [ABBREV]
  2. Fixes known loanword errors (hardcoded corrections)
  3. Flags entries with no diacritics as [NEEDS_REVIEW] for targeted re-run
  4. Removes entries where Claude returned a sentence instead of romanization

USAGE:
  python fix_paiboon.py

OUTPUT:
  data/yaitron_dictionary_paiboon_fixed.tsv  — cleaned dictionary
  data/needs_rerun.tsv                        — entries to re-run with better prompt
"""

import csv
import os
import re

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE  = os.path.join(BASE_DIR, "data", "yaitron_dictionary_paiboon.tsv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "yaitron_dictionary_paiboon_fixed.tsv")
RERUN_FILE  = os.path.join(BASE_DIR, "data", "needs_rerun.tsv")

# ── Known loanword corrections ─────────────────────────────────────────────
# Format: thai_word → correct_paiboon
LOANWORD_FIXES = {
    "ไบต์": "bait",       # BYTE
    "ไมล์": "maai",       # mile
    "ไวน์": "wain",       # wine
    "บิต":  "bìt",        # BIT
    "รอม":  "rɔɔm",       # ROM
    "เบรก": "brèek",      # brake
    "เลนส์": "leens",     # lens
    "โพลล์": "poo",       # poll
    "ไฟล์": "fai",        # file (actually correct vowel, needs tone)
    "ฮิต":  "hít",        # hit
}

# ── Abbreviation detection ─────────────────────────────────────────────────
def is_abbreviation(thai: str) -> bool:
    """Detect Thai abbreviations and acronyms."""
    # Ends with a Thai full stop or contains dots
    if re.search(r'\.$', thai.strip()):
        return True
    # Contains slash (like บ/ช)
    if "/" in thai:
        return True
    # Thai ๆ repetition marker or ฯ abbreviation marker
    if "ฯ" in thai:
        return True
    # Very short — 1–2 Thai characters with no vowels (likely acronym)
    thai_chars = re.sub(r'[^\u0E00-\u0E7F]', '', thai)
    vowel_pattern = r'[ะาิีึืุูเแโใไ็่้๊๋]'
    if len(thai_chars) <= 3 and not re.search(vowel_pattern, thai):
        return True
    return False

# ── Bad response detection ─────────────────────────────────────────────────
def is_bad_response(paiboon: str) -> bool:
    """Detect entries where Claude returned a sentence instead of romanization."""
    if len(paiboon) > 60:
        return True
    if paiboon.startswith("I ") or paiboon.startswith('"I '):
        return True
    if "need to" in paiboon or "appears to be" in paiboon:
        return True
    return False

# ── Diacritic check ────────────────────────────────────────────────────────
def has_diacritics(paiboon: str) -> bool:
    """Check if romanization has proper Paiboon tone/vowel markers."""
    return bool(re.search(r'[áàâǎɛɔʉəŋ]', paiboon))

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    stats = {
        "total": 0,
        "loanword_fixed": 0,
        "abbrev_flagged": 0,
        "bad_response_cleared": 0,
        "needs_rerun": 0,
        "ok": 0,
    }

    rerun_entries = []

    with open(INPUT_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out, delimiter="\t", lineterminator="\n")
        writer.writerow(["english", "thai", "paiboon"])

        for row in rows:
            stats["total"] += 1
            english = row["english"].strip()
            thai    = row["thai"].strip()
            paiboon = row.get("paiboon", "").strip()

            # 1. Fix known loanwords first
            if thai in LOANWORD_FIXES:
                paiboon = LOANWORD_FIXES[thai]
                stats["loanword_fixed"] += 1

            # 2. Flag abbreviations
            elif is_abbreviation(thai):
                paiboon = "[ABBREV]"
                stats["abbrev_flagged"] += 1

            # 3. Clear bad Claude responses (sentences returned instead of romanization)
            elif is_bad_response(paiboon):
                paiboon = ""
                stats["bad_response_cleared"] += 1
                rerun_entries.append({"english": english, "thai": thai, "paiboon": ""})

            # 4. Flag missing diacritics for re-run
            elif paiboon and not has_diacritics(paiboon):
                rerun_entries.append({"english": english, "thai": thai, "paiboon": paiboon})
                stats["needs_rerun"] += 1
                # Keep existing value for now — re-run script will overwrite

            else:
                stats["ok"] += 1

            writer.writerow([english, thai, paiboon])

    # Write re-run list
    with open(RERUN_FILE, "w", encoding="utf-8", newline="") as rf:
        writer2 = csv.writer(rf, delimiter="\t", lineterminator="\n")
        writer2.writerow(["english", "thai", "current_paiboon"])
        for e in rerun_entries:
            writer2.writerow([e["english"], e["thai"], e["paiboon"]])

    # Report
    print("\n── fix_paiboon.py results ──────────────────────────")
    print(f"  Total entries processed : {stats['total']:,}")
    print(f"  Loanwords fixed         : {stats['loanword_fixed']}")
    print(f"  Abbreviations flagged   : {stats['abbrev_flagged']}")
    print(f"  Bad responses cleared   : {stats['bad_response_cleared']}")
    print(f"  Flagged for re-run      : {stats['needs_rerun']}")
    print(f"  Already correct         : {stats['ok']:,}")
    print(f"\n  Output : {OUTPUT_FILE}")
    print(f"  Re-run : {RERUN_FILE}")
    print("────────────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
