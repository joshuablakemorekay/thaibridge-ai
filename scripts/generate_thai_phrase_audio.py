"""Record Thai phrases from the site's data as MP3s, page by page.

Build-time tool. Run it once per page's worth of content; the MP3s are committed
and served as static files, so visitors never run this and edge-tts stays out of
requirements.txt.

    pip install edge-tts
    python scripts/generate_thai_phrase_audio.py            # all wired-up pages
    python scripts/generate_thai_phrase_audio.py --page vowels
    python scripts/generate_thai_phrase_audio.py --force    # re-record everything

What gets spoken is the raw Thai script (อา, น้า, สวัสดี), never the Paiboon
romanisation — a native Thai voice reads Thai, and the romanisation is only ever
the on-screen guide for the human. Files are named by thai_audio.slug (a hash of
the Thai), so the app and this script always agree on the filename.

Adding a new page = add a collector to PAGES below. Each collector returns the
list of Thai strings that page shows; the runner dedupes across everything.
"""

import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import thai_audio  # noqa: E402
from thai_consonants import AUDIO_VOICE  # same Thai voice as the alphabet  # noqa: E402

# Slower than default: these are learning clips, said one at a time, and the
# natural rate is too quick to copy. Matches the alphabet recordings.
RATE = '-15%'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')


def _walk_thai(obj, out):
    """Collect every value stored under a 'thai' key, however deeply nested."""
    if isinstance(obj, dict):
        thai = obj.get('thai')
        if isinstance(thai, str) and thai.strip():
            out.append(thai.strip())
        for value in obj.values():
            _walk_thai(value, out)
    elif isinstance(obj, list):
        for item in obj:
            _walk_thai(item, out)


def collect_vowels():
    """Every Thai string on the Vowels & Syllables page."""
    import app  # imported lazily so a single-page run does not pay for it twice
    found = []
    _walk_thai(app.THAI_VOWELS_32, found)
    return found


# The registry of wired-up pages. Add a line here to bring a new page online.
PAGES = {
    'vowels': collect_vowels,
}


async def synthesize(text, out_path):
    import edge_tts
    await edge_tts.Communicate(text, AUDIO_VOICE, rate=RATE).save(out_path)


async def main(pages, force):
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        print('edge-tts is not installed. Run:  pip install edge-tts')
        return 1

    # Dedupe across every selected page: two pages sharing a word share its file.
    phrases = []
    seen = set()
    for name in pages:
        for thai in PAGES[name]():
            key = thai_audio.slug(thai)
            if key not in seen:
                seen.add(key)
                phrases.append(thai)

    print('=== Thai phrases ({}) — {} unique from: {} ==='.format(
        AUDIO_VOICE, len(phrases), ', '.join(pages)))

    made = skipped = failed = 0
    out_dir = os.path.join(STATIC_DIR, 'audio', 'th', 'phrases')
    os.makedirs(out_dir, exist_ok=True)

    for thai in phrases:
        out_path = thai_audio.audio_disk_path(STATIC_DIR, thai)
        stem = thai_audio.slug(thai)

        if os.path.exists(out_path) and not force:
            skipped += 1
            continue

        try:
            await synthesize(thai, out_path)
            made += 1
            # ASCII only in the log — a Windows console is cp1252 and raises
            # UnicodeEncodeError the moment a Thai character reaches stdout,
            # which would abort the run right after the MP3 was written.
            print('  {} ok'.format(stem))
        except Exception as exc:                       # noqa: BLE001
            failed += 1
            print('  {} FAILED: {}'.format(stem, ascii(exc)))

    print('\n{} made, {} already present, {} failed'.format(made, skipped, failed))
    return 1 if failed else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', choices=sorted(PAGES), action='append',
                        help='limit to one page (repeatable); default is all')
    parser.add_argument('--force', action='store_true',
                        help='re-record files that already exist')
    args = parser.parse_args()
    selected = args.page or sorted(PAGES)
    sys.exit(asyncio.run(main(selected, args.force)))
