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

# One voice per accent. British is the original and stays the default: the IPA
# in the lesson files is RP, and every MP3 generated before the accent toggle
# was Sonia. American is the addition.
VOICES = {
    "uk": "en-GB-SoniaNeural",
    "us": "en-US-JennyNeural",
}
DEFAULT_ACCENT = "uk"

# Slightly slower than default — these are learners hearing a word for the
# first time, and the point is to make every final consonant audible.
RATE = "-15%"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(REPO_ROOT, "content", "monk")
AUDIO_ROOT = os.path.join(REPO_ROOT, "static", "audio", "en")


def audio_dir_for(accent):
    """Each accent gets its own folder, so one can never overwrite the other."""
    return os.path.join(AUDIO_ROOT, accent)


# The filename rule is shared with the web app (see monk_audio.py) so that the
# names this script writes and the names the template links to can never drift
# apart. Import it rather than keeping a second copy here.
sys.path.insert(0, REPO_ROOT)
from monk_audio import slugify  # noqa: E402


def collect_entries(topic_filter=None, accent=DEFAULT_ACCENT):
    """Every (slug, spoken_text) pair across the monk lesson files.

    Deduplicated — 'food' appears in more than one lesson but only needs one
    audio file.

    The slug always comes from the BASE english text, even when the accent has
    its own wording. So 'aeroplane' and 'airplane' share the filename
    aeroplane.mp3, one in the uk folder and one in the us folder, and the app
    can look up either with a single key. What changes per accent is the text
    that gets SPOKEN, not the name of the file it lands in.
    """
    seen = {}
    for path in sorted(glob.glob(os.path.join(CONTENT_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            lesson = json.load(f)

        if topic_filter and lesson.get("topic") != topic_filter:
            continue

        # Drill lines (tongue twisters) sit inside drill_sections but carry the
        # same 'english' field, so they join the normal entry flow.
        drills = [
            d
            for sec in lesson.get("drill_sections", [])
            for d in sec.get("drills", [])
        ]

        # The alternative wordings in 'one idea, several words' are ordinary
        # single entries too — a monk choosing between 'suffering' and 'stress'
        # needs to hear both, not just read them.
        choices = [
            o
            for s in lesson.get("word_choices", {}).get("sets", [])
            for o in s.get("options", [])
        ]

        for entry in (
            lesson.get("vocab", []) + lesson.get("phrases", []) + drills + choices
        ):
            english = (entry.get("english") or "").strip()
            if not english:
                continue
            # Filename comes from the base wording; the voice says the wording
            # for THIS accent, so the American file for 'aeroplane' actually
            # says 'airplane'.
            source = english
            if accent == "us" and entry.get("english_us"):
                source = entry["english_us"].strip()
            # Strip a parenthetical gloss — '(respectfully)' is a note to the
            # reader, not something we want the voice to read aloud.
            spoken = re.sub(r"\s*\([^)]*\)", "", source).strip()
            # An entry like 'to give thanks / rejoice in merit' offers two
            # wordings; speak the first.
            spoken = spoken.split("/")[0].strip()
            if not spoken:
                continue
            seen.setdefault(slugify(english), spoken)

        # Whole reading passages. Keyed off the passage id, never its text —
        # the slug of a 200-word passage would be meaningless, and the template
        # asks for exactly the same key: monk_audio_url('passage ' ~ p.id).
        # The gloss/slash stripping above is for single entries and must NOT
        # run here: a passage's parentheses and slashes are real prose.
        for p in lesson.get("passages", []):
            pid = (p.get("id") or "").strip()
            text = (p.get("text") or "").strip()
            if pid and text:
                seen.setdefault(slugify("passage " + pid), text)

    return seen


async def synthesize(text, out_path, voice):
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=RATE)
    await communicate.save(out_path)


async def main_async(args):
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        print("edge-tts is not installed. Run:  pip install edge-tts")
        return 1

    accents = list(VOICES) if args.accent == "all" else [args.accent]

    total_failed = 0
    for accent in accents:
        # Collected per accent, not once up front: the spoken text differs
        # where an entry has its own english_us wording.
        entries = collect_entries(args.topic, accent)
        if not entries:
            print("No entries found. Check --topic matches a 'topic' field.")
            return 1

        voice = VOICES[accent]
        audio_dir = audio_dir_for(accent)
        os.makedirs(audio_dir, exist_ok=True)

        print("\n=== {} ({}) ===".format(accent.upper(), voice))
        made = skipped = failed = 0
        for slug, spoken in sorted(entries.items()):
            out_path = os.path.join(audio_dir, slug + ".mp3")

            if os.path.exists(out_path) and not args.force:
                skipped += 1
                continue

            try:
                await synthesize(spoken, out_path, voice)
            except Exception as e:
                failed += 1
                print("  FAIL {}: {}".format(slug, e))
                # Don't leave a half-written file behind for the app to serve.
                if os.path.exists(out_path):
                    os.remove(out_path)
                continue

            # Deliberately outside the try above. Only the synthesis call is
            # allowed to count as a failure — when the progress message itself
            # was in there, a console that couldn't print 'nibbāna' raised
            # UnicodeEncodeError, the handler ran, and it deleted the good MP3
            # that had just been written.
            made += 1
            print("  ok   {}  <- {}".format(slug + ".mp3", spoken))

        print(
            "{} generated, {} already existed, {} failed. Voice: {}".format(
                made, skipped, failed, voice
            )
        )
        print("Files in: {}".format(audio_dir))
        total_failed += failed

    return 1 if total_failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="regenerate existing files")
    parser.add_argument("--topic", help="only one topic, e.g. alms_round")
    parser.add_argument(
        "--accent",
        choices=list(VOICES) + ["all"],
        default=DEFAULT_ACCENT,
        help="which accent to generate (default: uk)",
    )
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
