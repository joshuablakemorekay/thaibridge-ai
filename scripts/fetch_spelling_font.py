"""Download the ThaiBridge Spelling font into static/fonts/.

    python scripts/fetch_spelling_font.py

ThaiBridge Spelling needs letters beyond plain English: ɛ ɔ ʉ ə ŋ, the
rising-tone ǎ ǐ ǒ ǔ ě, and tone marks sitting on ɛ ɔ ʉ ə. Roboto Mono, which
the app used to set the spelling in, does not contain ɛ ɔ ʉ ǎ at all, so the
browser borrowed them from Consolas or whatever the phone had — mid-word, in
a different typeface, with the tone marks set badly.

Noto Sans Mono has every one of them (checked against the font's own
character map, not Google's CSS, which claims letters a font does not have).
It is cut to exactly the characters below (`text=`) — about 10KB — and saved
here, then served by the app as its own family, 'ThaiBridge Spelling'. The
print build (scripts/build_chanting_print.py) uses the same file, so screen
and paper draw the spelling from one font.

There is one face only. Noto Sans Mono has no italic, so where the spelling
is italic (the chanting book) the browser slants this face — as it already
slanted Roboto Mono, which was never loaded in italic either.

Noto Sans Mono is under the SIL Open Font License 1.1, which allows this.
Only needs running again if the spelling ever gains a new letter — and the
script refuses to save a font missing any of CHARS.
"""
import io
import os
import re
import sys
import urllib.parse
import urllib.request

from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, 'static', 'fonts', 'thaibridge-spelling.woff2')

# Everything ThaiBridge Spelling can contain: printable ASCII, the
# tone-marked vowels as single characters, the extra vowels and ŋ in both
# cases, and the four tone marks as combining characters.
CHARS = (
    ''.join(chr(c) for c in range(0x20, 0x7F))
    + 'àáâǎèéêěìíîǐòóôǒùúûǔ'
    + 'ÀÁÂǍÈÉÊĚÌÍÎǏÒÓÔǑÙÚÛǓ'
    + 'ɛɔʉəŋƐƆɄƏŊ'
    + '̀́̂̌'
)
CSS_URL = ('https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@400'
           '&text=' + urllib.parse.quote(CHARS))
# A modern browser's user agent, or Google Fonts answers with an old format.
# The plain request below gets TrueType instead, which fontTools can read
# without extra packages — that copy is only used for the coverage check.
WOFF2_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/155.0 Safari/537.36')


def fetch(url, agent=None):
    headers = {'User-Agent': agent} if agent else {}
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers),
                                  timeout=30).read()


def font_url(css):
    match = re.search(r'src:\s*url\(([^)]+)\)', css)
    if not match:
        sys.exit('Google Fonts sent no font.')
    return match.group(1)


def main():
    truetype = fetch(font_url(fetch(CSS_URL).decode('utf-8')))
    cmap = TTFont(io.BytesIO(truetype)).getBestCmap()
    missing = [c for c in CHARS if ord(c) not in cmap]
    if missing:
        sys.exit(f'The font is missing {"".join(missing)!r} — nothing saved.')

    woff2 = fetch(font_url(fetch(CSS_URL, WOFF2_AGENT).decode('utf-8')), WOFF2_AGENT)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'wb') as f:
        f.write(woff2)
    print(f'{OUT_PATH} ({len(woff2):,} bytes), all {len(CHARS)} characters present')


if __name__ == '__main__':
    main()
