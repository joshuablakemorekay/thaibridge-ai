"""
rerun_paiboon.py — Targeted re-run script for entries flagged by fix_paiboon.py.

Reads needs_rerun.tsv and re-generates Paiboon romanization using an improved
prompt, then patches the fixed output file.

ESTIMATED COST:
  ~80 entries × ~35 tokens input + ~15 tokens output = negligible (~$0.002)

USAGE:
  python rerun_paiboon.py
"""

import csv
import os
import time

import anthropic

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
RERUN_FILE   = os.path.join(BASE_DIR, "data", "needs_rerun.tsv")
FIXED_FILE   = os.path.join(BASE_DIR, "data", "yaitron_dictionary_paiboon_fixed.tsv")

MODEL        = "claude-haiku-4-5-20251001"
MAX_TOKENS   = 30
BATCH_DELAY  = 2.0

# ── Improved prompt ────────────────────────────────────────────────────────
# Key improvements over original:
#   - Explicit tone mark requirement on EVERY syllable
#   - Loanword handling instructions
#   - Abbreviation skip instruction
#   - More examples covering edge cases

IMPROVED_PROMPT = """\
You are an expert in Paiboon Thai romanization. Convert the Thai word or phrase below \
into Paiboon romanization using EXACTLY these rules — no exceptions, no alternatives.

CONSONANTS:
  ก → g   ข/ค/ฅ/ฆ → k   ง → ng   จ → j   ช/ฉ/ฌ → ch
  ซ/ส/ศ/ษ → s   ด/ฎ → d   ต/ฏ → dt   ท/ธ/ถ/ฐ/ฑ/ฒ → t
  น/ณ → n   บ → b   ป → bp   พ/ผ/ภ → p   ฟ/ฝ → f
  ม → m   ย/ญ → y   ร → r   ล/ฬ → l   ว → w   ห/ฮ → h
  Final ง → ng

VOWELS (short / long — double the letter for long):
  อะ/อา → a / aa     อิ/อี → i / ii     อึ/อือ → ʉ / ʉʉ
  อุ/อู → u / uu     เอะ/เอ → e / ee    แอะ/แอ → ɛ / ɛɛ
  โอะ/โอ → o / oo   เอาะ/ออ → ɔ / ɔɔ  เออะ/เออ → ə / əə
  เอีย → ia          เอือ → ʉa           อัว → ua
  ใ/ไ → ai           เอา → ao            อาว → aao

TONES — REQUIRED on EVERY syllable (do not omit even for mid tone):
  Mid tone  → no mark   (e.g. gaa, dii, bpen)
  Low tone  → grave  à  (e.g. gàa, nàm)
  Falling   → circumflex â  (e.g. mâi, kâao)
  High tone → acute  á  (e.g. máa, náam)
  Rising    → caron  ǎ  (e.g. sǎam, mǎi)

TONE CLASSES — needed to determine tone:
  Mid class consonants: ก จ ด ต ฎ ฏ บ ป อ
  High class consonants: ข ฃ ฉ ฐ ฑ ฒ ถ ผ ฝ ศ ษ ส ห
  Low class consonants: all others

SYLLABLE SEPARATOR: hyphen between syllables.
SPACES between separate words in multi-word phrases.

SPECIAL CASES:
  LOANWORDS: Thai loanwords from English still require correct Paiboon vowel
    length and tone marks based on how Thai speakers actually pronounce them.
    e.g. ไวน์ → wâin  (not wai)   ไมล์ → maai  (long vowel)
  ABBREVIATIONS: If the input is clearly a Thai abbreviation or acronym
    (e.g. กน. ชม. มท), respond with exactly: [ABBREV]
  SINGLE CHARACTERS used as abbreviations (เ, ก, ต etc. alone): respond [ABBREV]

EXAMPLES:
  กา → gaa          ปลา → bplaa        ขอบคุณ → kɔ̀ɔp-kun
  สวัสดี → sà-wàt-dii   เด็ก → dèk      ผึ้ง → pʉ̂ng
  ทหาร → tá-hǎan    ภิกษุ → pík-sù    เสือ → sʉ̌a
  ม้า → máa          หนู → nǔu          ระวัง → rá-waŋ
  มวน → muan → CORRECT OUTPUT: muan (mid-class ม, short vowel, no final = mid tone)
  เตา → dtao → CORRECT OUTPUT: dtao (mid-class ต, falling vowel pattern)
  โรย → rooy → CORRECT OUTPUT: rooy (low-class ร, rising tone on long vowel)
  เณร → neen → CORRECT OUTPUT: neen (low-class ณ, long vowel)

Thai word/phrase to convert: {thai}

Respond with ONLY the Paiboon romanization or [ABBREV]. No explanation, no Thai script.\
"""


def load_rerun(path: str) -> list[dict]:
    entries = []
    if not os.path.exists(path):
        print(f"No re-run file found at {path}. Run fix_paiboon.py first.")
        return entries
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            entries.append({
                "english": row["english"].strip(),
                "thai":    row["thai"].strip(),
            })
    return entries


def get_paiboon(client: anthropic.Anthropic, thai: str) -> str:
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": IMPROVED_PROMPT.format(thai=thai)}],
        )
        return msg.content[0].text.strip()
    except Exception as exc:
        print(f"  [error] {thai!r}: {exc}")
        return ""


def patch_fixed_file(updates: dict[str, str]) -> None:
    """Overwrite paiboon values in the fixed TSV for matching thai entries."""
    with open(FIXED_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    patched = 0
    for row in rows:
        thai = row["thai"].strip()
        if thai in updates and updates[thai]:
            row["paiboon"] = updates[thai]
            patched += 1

    with open(FIXED_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["english", "thai", "paiboon"])
        for row in rows:
            writer.writerow([row["english"], row["thai"], row["paiboon"]])

    print(f"  Patched {patched} entries in {FIXED_FILE}")


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        env_path = os.path.join(BASE_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY not found.")

    client  = anthropic.Anthropic(api_key=api_key)
    entries = load_rerun(RERUN_FILE)

    if not entries:
        return

    print(f"\nRe-running {len(entries)} flagged entries with improved prompt...\n")

    updates = {}
    for i, entry in enumerate(entries, 1):
        thai    = entry["thai"]
        result  = get_paiboon(client, thai)
        updates[thai] = result
        print(f"  [{i:>3}/{len(entries)}] {thai} → {result}")

        if i % 50 == 0:
            print(f"\n  Pausing {BATCH_DELAY}s...\n")
            time.sleep(BATCH_DELAY)

    patch_fixed_file(updates)
    print(f"\nDone. {len(entries)} entries re-processed.\n")


if __name__ == "__main__":
    main()
