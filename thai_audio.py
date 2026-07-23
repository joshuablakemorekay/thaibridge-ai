"""Shared naming rule for Thai phrase audio — any Thai string to its MP3.

The alphabet already has its own recordings keyed on a human-readable slug
(kor-kai.mp3). This module is the GENERAL version: given an arbitrary piece of
Thai text from any page (a vowel form, an example word, a whole sentence), it
returns a stable filename for that text's recording.

Two pieces of code must agree on that filename or every play button silently
404s while nothing looks broken:

  * scripts/generate_thai_phrase_audio.py  WRITES  static/audio/th/phrases/<name>.mp3
  * the templates (via the thai_audio_url context helper)  LINK to the same file

so the rule lives here once and both sides import it.

Why a HASH and not a slug of the romanisation: Thai characters turn into
percent-encoded soup in a URL, and many different letters share one Paiboon
spelling (ข ฃ ค ฅ ฆ are all "k"), so a romanised name would collide. Hashing the
exact Thai UTF-8 bytes gives a short, ASCII, collision-free name that depends on
nothing but the Thai itself — the same lesson behind keying the alphabet clips
on the letter's codepoint, never its romanisation.
"""

import hashlib
import os

# Where the generated MP3s live, relative to the Flask static folder. Posix-style
# because it ends up in a URL. A 'phrases' subfolder keeps these general clips
# apart from the alphabet's hand-named ones in audio/th/.
AUDIO_URL_ROOT = "audio/th/phrases"


def _normalise(thai_text):
    """The exact bytes we hash and speak — trimmed, nothing else touched.

    We deliberately do NOT strip combining tone marks or spaces: 'นา' and 'น่า'
    are different words and must get different files.
    """
    return (thai_text or "").strip()


def slug(thai_text):
    """A stable, ASCII, filesystem-safe stem for any Thai string."""
    digest = hashlib.sha1(_normalise(thai_text).encode("utf-8")).hexdigest()
    return digest[:16]


def audio_filename(thai_text):
    """The MP3 filename for a Thai string."""
    return slug(thai_text) + ".mp3"


def audio_static_path(thai_text):
    """The path to hand to Flask's url_for('static', filename=...)."""
    return "{}/{}".format(AUDIO_URL_ROOT, audio_filename(thai_text))


def audio_disk_path(static_folder, thai_text):
    """Where this string's MP3 sits on disk."""
    return os.path.join(
        static_folder, "audio", "th", "phrases", audio_filename(thai_text)
    )


def audio_exists(static_folder, thai_text):
    """Has this string's MP3 actually been generated yet?

    The template asks before drawing a play button — better to show nothing than
    a button that 404s, because clips are generated page by page and most Thai
    on the site has none yet.
    """
    if not _normalise(thai_text):
        return False
    return os.path.isfile(audio_disk_path(static_folder, thai_text))
