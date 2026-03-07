"""
generate_paiboon.py — One-time script to add Paiboon romanization to the
Yaitron dictionary using the Anthropic Claude API.

ESTIMATED COST (claude-haiku-4-5, cheapest capable model):
  Input:  4,894 entries × ~25 tokens = ~122,350 tokens → ~$0.03
  Output: 4,894 entries × ~10 tokens = ~48,940 tokens  → ~$0.06
  Total:  ~$0.09 USD

ESTIMATED TIME:
  ~98 batches of 50, ~1–2s per API call, 2s delay between batches
  Expected: 20–40 minutes

RESUME SUPPORT:
  If interrupted, re-run the script — it skips entries already in the
  output file and picks up from where it left off.

USAGE:
  python generate_paiboon.py

REQUIRES:
  pip install anthropic
  ANTHROPIC_API_KEY set in environment or .env file
"""

import csv
import os
import time

import anthropic

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE  = os.path.join(BASE_DIR, "data", "yaitron_dictionary.tsv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "yaitron_dictionary_paiboon.tsv")

# ── Settings ───────────────────────────────────────────────────────────────
BATCH_SIZE   = 50          # entries per batch before sleeping
BATCH_DELAY  = 2.0         # seconds to sleep between batches
MODEL        = "claude-haiku-4-5-20251001"   # cheapest model, good for simple lookups
MAX_TOKENS   = 30          # romanization is never more than ~20 tokens


def load_input(path: str) -> list[dict]:
    """Read english/thai pairs from the input TSV."""
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 2:
                en, th = parts[0].strip(), parts[1].strip()
                if en and th:
                    entries.append({"english": en, "thai": th})
    return entries


def load_done(path: str) -> set[str]:
    """Return the set of Thai words that already have a non-empty paiboon value."""
    done = set()
    if not os.path.exists(path):
        return done
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("thai") and row.get("paiboon", "").strip():
                done.add(row["thai"])
    return done


PAIBOON_PROMPT = """\
You are an expert in Paiboon Thai romanization. Convert the Thai word or phrase below \
into Paiboon romanization using EXACTLY these rules — no exceptions, no alternatives.

CONSONANTS:
  ก → g   ข/ค/ฅ/ฆ → k   ง → ng   จ → j   ช/ฉ/ฌ → ch
  ซ/ส/ศ/ษ → s   ด/ฎ → d   ต/ฏ → dt   ท/ธ/ถ/ฐ/ฑ/ฒ → t
  น/ณ → n   บ → b   ป → bp   พ/ผ/ภ → p   ฟ/ฝ → f
  ม → m   ย/ญ → y   ร → r   ล/ฬ → l   ว → w   ห/ฮ → h
  Final ง → ng (e.g. waŋ not wang)

VOWELS (short / long — double the letter for long):
  อะ/อา → a / aa     อิ/อี → i / ii     อึ/อือ → ʉ / ʉʉ
  อุ/อู → u / uu     เอะ/เอ → e / ee    แอะ/แอ → ɛ / ɛɛ
  โอะ/โอ → o / oo   เอาะ/ออ → ɔ / ɔɔ  เออะ/เออ → ə / əə
  เอีย → ia          เอือ → ʉa           อัว → ua
  ใ/ไ/ไ้ → ai        เอา → ao            อาว → aao

TONES (diacritic on the main vowel):
  Mid tone  → no mark   (e.g. gaa)
  Low tone  → à         (e.g. gàa)
  Falling   → â         (e.g. gâa)
  High tone → á         (e.g. gáa)
  Rising    → ǎ         (e.g. gǎa)

SYLLABLE SEPARATOR: hyphen between syllables, e.g. sà-wàt-dii, rá-waŋ, bpà-dtàk
SPACES between separate words in multi-word phrases.

EXAMPLES (Thai → Paiboon):
  กา → gaa        ปลา → bplaa      ขอบคุณ → kɔ̀ɔp-kun
  สวัสดี → sà-wàt-dii   เด็ก → dèk     ผึ้ง → pʉ̂ng
  ทหาร → tá-hǎan   ภิกษุ → pík-sù   เสือ → sʉ̌a
  ม้า → máa        หนู → nǔu        ระวัง → rá-waŋ

Thai word/phrase to convert: {thai}

Respond with ONLY the Paiboon romanization. No explanation, no Thai script, no extra text.\
"""


def get_paiboon(client: anthropic.Anthropic, thai: str) -> str:
    """Ask Claude for the Paiboon romanization of a single Thai word."""
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": PAIBOON_PROMPT.format(thai=thai)}],
        )
        return msg.content[0].text.strip()
    except Exception as exc:
        print(f"    [error] {thai!r}: {exc}")
        return ""


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Try loading from .env manually
        env_path = os.path.join(BASE_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    if not api_key:
        raise SystemExit(
            "ANTHROPIC_API_KEY not found. Set it in your environment or .env file."
        )

    client = anthropic.Anthropic(api_key=api_key)

    entries = load_input(INPUT_FILE)
    done    = load_done(OUTPUT_FILE)

    total   = len(entries)
    pending = [e for e in entries if e["thai"] not in done]

    print(f"Total entries : {total:,}")
    print(f"Already done  : {total - len(pending):,}")
    print(f"Remaining     : {len(pending):,}")
    if not pending:
        print("Nothing to do — output file is complete.")
        return

    # Load completed rows to carry forward, then rewrite the file from scratch.
    # This avoids duplicate rows when re-processing previously empty entries.
    completed: dict[str, dict] = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                th = row.get("thai", "").strip()
                pb = row.get("paiboon", "").strip()
                if th and pb:
                    completed[th] = row

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out, delimiter="\t", lineterminator="\n")
        writer.writerow(["english", "thai", "paiboon"])
        # Write already-completed rows first
        for row in completed.values():
            writer.writerow([row["english"], row["thai"], row["paiboon"]])

        processed  = 0
        start_time = time.time()

        for i, entry in enumerate(pending):
            # Progress indicator
            done_count = (total - len(pending)) + processed + 1
            if processed % 10 == 0:
                elapsed = time.time() - start_time
                rate    = processed / elapsed if elapsed > 0 else 0
                eta_s   = (len(pending) - processed) / rate if rate > 0 else 0
                eta_min = int(eta_s // 60)
                eta_sec = int(eta_s % 60)
                eta_str = f"{eta_min}m {eta_sec}s" if processed > 0 else "calculating..."
                print(
                    f"  Processing {done_count:,}/{total:,} "
                    f"({done_count / total * 100:.1f}%)  ETA: {eta_str}",
                    end="\r",
                    flush=True,
                )

            paiboon = get_paiboon(client, entry["thai"])
            writer.writerow([entry["english"], entry["thai"], paiboon])
            out.flush()   # write immediately so resume works after interruption
            processed += 1

            # Batch delay
            if processed % BATCH_SIZE == 0:
                batch_num = processed // BATCH_SIZE
                total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE
                print(
                    f"\n  Batch {batch_num}/{total_batches} complete. "
                    f"Pausing {BATCH_DELAY}s...                    "
                )
                time.sleep(BATCH_DELAY)

    elapsed = time.time() - start_time
    print(f"\n\nDone! Processed {processed:,} entries in {elapsed / 60:.1f} minutes.")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
