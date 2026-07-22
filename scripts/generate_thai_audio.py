"""Record the 44 Thai consonant names as MP3s.

Build-time tool. Run it once; the MP3s are committed and served as static
files, so visitors never run this and edge-tts is not in requirements.txt.

    pip install edge-tts
    python scripts/generate_thai_audio.py

Why pre-recorded files rather than the browser's speech synthesis: the Web
Speech API needs a Thai voice installed on the device. iPhones have one,
Windows desktops usually do not, and Android is a lottery. A committed MP3
sounds identical everywhere, which is the entire point of an alphabet page.

What gets spoken is the letter's full name ("กอ ไก่"), not the bare letter.
Saying a Thai consonant on its own is ambiguous; the name is how the alphabet
is actually taught and recited.

Existing files are skipped, so re-running costs nothing. --force re-records.
"""

import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thai_consonants import AUDIO_VOICE, CONSONANTS  # noqa: E402

# Slower than the default. These are single words being learned one at a time,
# not running speech, and the natural rate is too quick to copy.
RATE = '-15%'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')


async def synthesize(text, out_path):
    import edge_tts
    await edge_tts.Communicate(text, AUDIO_VOICE, rate=RATE).save(out_path)


async def main(force):
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        print('edge-tts is not installed. Run:  pip install edge-tts')
        return 1

    made = skipped = failed = 0
    print('=== Thai consonants ({}) ==='.format(AUDIO_VOICE))

    for letter in CONSONANTS:
        out_path = os.path.join(STATIC_DIR, letter['audio'].replace('/', os.sep))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        if os.path.exists(out_path) and not force:
            skipped += 1
            continue

        slug = os.path.splitext(os.path.basename(out_path))[0]
        try:
            await synthesize(letter['name_thai'], out_path)
            made += 1
            # ASCII only in the log. A Windows console is cp1252 by default and
            # raises UnicodeEncodeError the moment a Thai character reaches
            # stdout — which would abort the run after the MP3 was written.
            print('  {:<16} ok'.format(slug))
        except Exception as exc:                       # noqa: BLE001
            failed += 1
            print('  {:<16} FAILED: {}'.format(slug, ascii(exc)))

    print('\n{} made, {} already present, {} failed'.format(made, skipped, failed))
    return 1 if failed else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true',
                        help='re-record files that already exist')
    sys.exit(asyncio.run(main(parser.parse_args().force)))
