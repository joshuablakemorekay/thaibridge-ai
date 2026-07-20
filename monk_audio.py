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
AUDIO_URL_DIR = "audio/en"


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


def audio_static_path(english):
    """The path to hand to Flask's url_for('static', filename=...)."""
    return "{}/{}".format(AUDIO_URL_DIR, audio_filename(english))


def audio_exists(static_folder, english):
    """Has this entry's MP3 actually been generated yet?

    Only 1 of the 10 topics has audio so far, so the template asks this before
    drawing a play button — better to show nothing than a button that fails.
    """
    if not english:
        return False
    return os.path.isfile(
        os.path.join(static_folder, "audio", "en", audio_filename(english))
    )
