"""Shared naming rules for the Monk Mode English audio.

Two very different pieces of code need to agree on exactly one thing: what an
English phrase's MP3 file is called.

  * scripts/generate_english_audio.py  writes  static/audio/en/<slug>.mp3
  * templates/monk_lesson_detail.html  links to static/audio/en/<slug>.mp3

If those two ever disagree — even by one character — the page still renders
perfectly and every play button silently 404s. That is a horrible bug to spot,
because nothing looks broken. So the rule lives here, once, and both sides
import it rather than each keeping their own copy.
"""

import os
import re

# Where the generated MP3s live, relative to the Flask static folder. Kept as a
# posix-style path because it ends up in a URL, not on disk.
#
# The accent is a SUBFOLDER rather than part of the filename ('audio/en/uk/x.mp3'
# not 'audio/en/x.uk.mp3') so that the two voices stay physically separate: a
# regeneration of one accent can never half-overwrite the other, and 'how many
# US files am I missing?' is answerable with a directory listing.
AUDIO_URL_ROOT = "audio/en"
AUDIO_ACCENTS = ("uk", "us")
AUDIO_ACCENT_DEFAULT = "uk"


def _accent_dir(accent):
    """Validate an accent and return its URL-style directory.

    Falls back to British rather than raising: an unknown accent should show
    the default audio, not 500 a lesson page.
    """
    if accent not in AUDIO_ACCENTS:
        accent = AUDIO_ACCENT_DEFAULT
    return "{}/{}".format(AUDIO_URL_ROOT, accent)


def slugify(text):
    """Turn an English phrase into a stable, filesystem-safe filename stem.

    'to give thanks / rejoice in merit' -> 'to-give-thanks-rejoice-in-merit'

    Note this runs on the entry's FULL english text, parenthetical glosses and
    all — '(respectfully)' included. The generator strips those before speaking
    them aloud, but keeps them in the filename so that two entries which differ
    only by their gloss still get their own file.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60]


def audio_filename(english):
    """The MP3 filename for an entry's English text."""
    return slugify(english) + ".mp3"


def audio_static_path(english, accent=AUDIO_ACCENT_DEFAULT):
    """The path to hand to Flask's url_for('static', filename=...)."""
    return "{}/{}".format(_accent_dir(accent), audio_filename(english))


def audio_disk_path(static_folder, english, accent=AUDIO_ACCENT_DEFAULT):
    """Where this entry's MP3 sits on disk."""
    if accent not in AUDIO_ACCENTS:
        accent = AUDIO_ACCENT_DEFAULT
    return os.path.join(
        static_folder, "audio", "en", accent, audio_filename(english)
    )


def audio_exists(static_folder, english, accent=AUDIO_ACCENT_DEFAULT):
    """Has this entry's MP3 actually been generated yet, in this accent?

    The template asks before drawing a play button — better to show nothing
    than a button that 404s. This matters more now than it did with one accent:
    the US set is generated separately, so a US file can legitimately be missing
    while its UK twin exists.
    """
    if not english:
        return False
    return os.path.isfile(audio_disk_path(static_folder, english, accent))
