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


def collect_sentences():
    """Every Thai string on the Sentences page — the conversation dialogues and
    the sentence-pattern examples (which are nested per gender)."""
    import app
    found = []
    _walk_thai(app.CONVERSATIONS, found)
    _walk_thai(app.SENTENCE_PATTERNS, found)
    _walk_thai(app.CONVERSATIONAL_PHRASES, found)
    return found


def collect_read_write():
    """Every Thai string on the Read & Write Thai Script page — the syllables,
    the dharma words and every word of the Jataka story. thai_reading already
    lists these in one place, so this just hands that list over."""
    import thai_reading
    return thai_reading.all_thai_strings()


def collect_tones_classes():
    """The Tones & Consonant Classes page.

    Deliberately NOT a blanket walk of TONES_AND_CLASSES: two kinds of 'thai'
    values there must be skipped —
      * the 44 bare consonant letters (they reuse the Alphabet's own name
        recordings on the page, so a lone-letter clip would be redundant), and
      * the tone marks, which are bare combining marks (' ่') with nothing to
        pronounce.
    So we collect only the class names and the example/drill SYLLABLES, which
    are what the page's play buttons actually point at."""
    import app
    d = app.TONES_AND_CLASSES
    found = []
    for cls in d['classes']:
        found.append(cls['thai'])          # the class name, e.g. อักษรกลาง
        _walk_thai(cls['examples'], found)  # its worked-example syllables
    for key in ('sound_pairs', 'dead_syllables', 'leading_h', 'contrast_pairs'):
        _walk_thai(d[key], found)          # demo/example syllables only (marks live elsewhere)
    _walk_thai(d['drills'], found)          # the practice-drill syllables
    return found


def collect_paiboon():
    """The Paiboon Romanization guide.

    Only the vowel forms (อะ, อา, อี …) need new clips — they are clean,
    pronounceable อ-carrier forms shown in the vowels table. The consonant rows
    reuse the Alphabet recordings (the template splits the ข/ค-style groups and
    looks each letter up), the tone markers are bare combining marks with
    nothing to say, and the tones table is romanisation only. The
    vowel_examples data is not rendered on the page, so it is left out too."""
    import app
    return [v['thai'] for v in app.PAIBOON_GUIDE['vowels']]


def collect_grammar():
    """The Grammar guide — every pronounceable Thai string in GRAMMAR.

    The route and this collector share app.grammar_thai_strings(), which already
    de-dupes and drops Latin notation ('คุณ + name'), so there is nothing to
    filter here."""
    import app
    return app.grammar_thai_strings()


# The registry of wired-up pages. Add a line here to bring a new page online.
PAGES = {
    'vowels': collect_vowels,
    'sentences': collect_sentences,
    'read_write': collect_read_write,
    'tones_classes': collect_tones_classes,
    'paiboon': collect_paiboon,
    'grammar': collect_grammar,
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
