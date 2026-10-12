"""Short commentary for the PRINTED chanting book.

The app shows each chant's full Historical background and Meaning and
purpose (chanting.py). Printed in full they made the book far too long, so
the print edition (scripts/build_chanting_print.py) uses these instead:
two or three sentences per section, keeping where the chant comes from and
what it means.

Kept in its own file rather than as extra fields in chanting.py, because
chanting.py holds 305 chants of verified Pali and editing every one of
them is exactly the kind of change that file's workflow avoids. The app
never reads this file.

Written from the full text in chanting.py, never from outside sources, so
the short version says nothing the long one does not.

    SHORT[chant_id] = {'background': '...', 'meaning': '...'}

A chant with no entry here prints its full text.
"""

SHORT = {
}
