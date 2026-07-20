"""Generate native English audio for the Monk Mode lessons.

This is a BUILD-TIME script. You run it once on your own machine, it writes MP3
files into static/audio/en/, and you commit those files. The live app never
runs this script and never calls a text-to-speech service — it just serves the
MP3s as ordinary static files. So if this script (or the service behind it)
ever breaks, the website is completely unaffected.

Why edge-tts: it uses Microsoft's neural voices, it is free, and it needs no
API key or signup. Because we only need it at build time, there is no secret to
manage on Render and no per-play cost.

Setup (once):

    pip install edge-tts

Usage:

    python scripts/generate_english_audio.py              # only missing files
    python scripts/generate_english_audio.py --force      # regenerate everything
    python scripts/generate_english_audio.py --topic alms_round

Each entry's audio filename comes from a slug of its English text, so the same
phrase always maps to the same file and re-running is safe.
"""

import argparse
import asyncio
import glob
import sys

# Pāli words like 'nibbāna' and 'pāṭimokkha' can't be printed by the default
# Windows console codepage (cp1252), and an unprintable progress message used to
# be enough to abort a file. Match what app.py does and force UTF-8 output.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import json
import os
import re

# British RP, to match the IPA already in the lesson files.
VOICE = "en-GB-SoniaNeural"

# Slightly slower than default — these are learners hearing a word for the
# first time, and the point is to make every final consonant audible.
RATE = "-15%"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(REPO_ROOT, "content", "monk")
AUDIO_DIR = os.path.join(REPO_ROOT, "static", "audio", "en")


# The filename rule is shared with the web app (see monk_audio.py) so that the
# names this script writes and the names the template links to can never drift
# apart. Import it rather than keeping a second copy here.
sys.path.insert(0, REPO_ROOT)
from monk_audio import slugify  # noqa: E402


def collect_entries(topic_filter=None):
    """Every (english_text, slug) pair across the monk lesson files.

    Deduplicated — 'food' appears in more than one lesson but only needs one
    audio file.
    """
    seen = {}
    for path in sorted(glob.glob(os.path.join(CONTENT_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            lesson = json.load(f)

        if topic_filter and lesson.get("topic") != topic_filter:
            continue

        for entry in lesson.get("vocab", []) + lesson.get("phrases", []):
            english = (entry.get("english") or "").strip()
            if not english:
                continue
            # Strip a parenthetical gloss — '(respectfully)' is a note to the
            # reader, not something we want the voice to read aloud.
            spoken = re.sub(r"\s*\([^)]*\)", "", english).strip()
            # An entry like 'to give thanks / rejoice in merit' offers two
            # wordings; speak the first.
            spoken = spoken.split("/")[0].strip()
            if not spoken:
                continue
            seen.setdefault(slugify(english), spoken)

    return seen


async def synthesize(text, out_path):
    import edge_tts

    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(out_path)


async def main_async(args):
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        print("edge-tts is not installed. Run:  pip install edge-tts")
        return 1

    entries = collect_entries(args.topic)
    if not entries:
        print("No entries found. Check --topic matches a 'topic' field.")
        return 1

    os.makedirs(AUDIO_DIR, exist_ok=True)

    made = skipped = failed = 0
    for slug, spoken in sorted(entries.items()):
        out_path = os.path.join(AUDIO_DIR, slug + ".mp3")

        if os.path.exists(out_path) and not args.force:
            skipped += 1
            continue

        try:
            await synthesize(spoken, out_path)
        except Exception as e:
            failed += 1
            print("  FAIL {}: {}".format(slug, e))
            # Don't leave a half-written file behind for the app to serve.
            if os.path.exists(out_path):
                os.remove(out_path)
            continue

        # Deliberately outside the try above. Only the synthesis call is allowed
        # to count as a failure — when the progress message itself was in there,
        # a console that couldn't print 'nibbāna' raised UnicodeEncodeError, the
        # handler ran, and it deleted the good MP3 that had just been written.
        made += 1
        print("  ok   {}  <- {}".format(slug + ".mp3", spoken))

    print(
        "\n{} generated, {} already existed, {} failed. Voice: {}".format(
            made, skipped, failed, VOICE
        )
    )
    print("Files in: {}".format(AUDIO_DIR))
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="regenerate existing files")
    parser.add_argument("--topic", help="only one topic, e.g. alms_round")
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
