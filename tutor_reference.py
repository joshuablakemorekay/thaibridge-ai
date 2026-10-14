"""Checked material the AI tutor is handed, so it answers from this app's own
lessons instead of from memory.

Why it exists: on 2026-10-09 the accuracy exam (evals/tutor_accuracy.yaml)
caught Sonnet 5.5 calling ด a low-class consonant, and an earlier model
counting people with ตัว. Both facts are already written down, correctly, in
this codebase. A model answering from memory will sometimes be wrong; one
handed the checked fact alongside the question very rarely is. It also keeps
the tutor and the pages saying the same thing, so fixing a lesson fixes the
tutor too.

Two kinds of material, placed differently on purpose:

  * consonant_classes() never changes, so it goes in the system prompt, where
    it is cached and costs almost nothing per message.
  * reference_for() depends on the question, so it rides along with that one
    message. Putting it in the system prompt would change the prompt every
    message and throw the cache away.

The entries come from paiboon_lookup's index — every Thai/romanisation pair the
app already ships — minus the chanting book, whose romanisation that module
itself describes as still an unreviewed draft in places.
"""
import re

import thai_consonants

THAI_RUN = re.compile(r'[฀-๿]+')
ENGLISH_WORD = re.compile(r"[a-z]+(?:'[a-z]+)?")

# Enough to cover the words in one question; more would bury the answer.
MAX_ENTRIES = 8
# Sources left out of the reference. See the module docstring.
UNREVIEWED_SOURCES = {'Chanting book'}
# Words that never make a useful lookup on their own.
_STOPWORDS = {'a', 'an', 'the', 'i', 'you', 'to', 'do', 'how', 'what', 'is', 'in',
              'of', 'and', 'or', 'say', 'mean', 'means', 'my', 'me', 'it', 'can',
              'does', 'please', 'thai', 'word', 'for', 'with', 'on', 'at', 'be'}

CLASS_ORDER = (thai_consonants.CLASS_MIDDLE, thai_consonants.CLASS_HIGH,
               thai_consonants.CLASS_LOW)


def consonant_classes():
    """All 44 consonants by class, straight from the Alphabet page's data."""
    lines = ["CONSONANT CLASSES (checked, from ThaiBridge's Alphabet page). "
             "These are facts: never contradict them."]
    for cls in CLASS_ORDER:
        letters = ' '.join(c['char'] for c in thai_consonants.by_class(cls))
        lines.append(f"- {thai_consonants.CLASS_LABELS[cls]}: {letters}")
    return '\n'.join(lines)


# Spellings Josh has confirmed for words the lessons do not teach yet, found
# when the tutor got one wrong. They only reach the tutor (its lookup and its
# answer check), never a lesson page. When a word here is added to a lesson,
# take it out of this list. Format: Thai → (spelling, meaning, when and who).
CONFIRMED_SPELLINGS = {
    'บริบท': ('bɔɔ-rí-bòt', 'context', 'Josh, 2026-10-14: the tutor wrote boo-rì-bàt'),
}


def _index():
    # Imported here, not at the top: building the index imports app, and app
    # imports the AI agent, so a top-level import would be circular.
    import paiboon_lookup
    lessons = [e for e in paiboon_lookup.get_index() if e.source not in UNREVIEWED_SOURCES]
    taught = {e.thai for e in lessons}
    return lessons + [paiboon_lookup.Entry(thai, spelling, meaning, 'Confirmed by Josh')
                      for thai, (spelling, meaning, _) in CONFIRMED_SPELLINGS.items()
                      if thai not in taught]


def _english_phrases(text):
    """Every 1–5 word run in `text`, longest first, skipping filler words."""
    words = ENGLISH_WORD.findall(text.lower())
    phrases = []
    for size in range(min(5, len(words)), 0, -1):
        for i in range(len(words) - size + 1):
            run = words[i:i + size]
            if all(w in _STOPWORDS for w in run):
                continue
            phrases.append(' '.join(run))
    return phrases


def entries_for(question, index=None):
    """The checked entries that match the Thai or English in `question`."""
    import paiboon_lookup
    index = _index() if index is None else index
    found = []

    for run in THAI_RUN.findall(question):
        found += [e for e in index if e.thai == run]
        # Thai has no spaces, so a run is often several words. The longest
        # known pieces inside it come next; one letter alone is never a word
        # worth looking up.
        found += sorted((e for e in index if len(e.thai) >= 2 and e.thai != run
                         and e.thai in run), key=lambda e: -len(e.thai))

    for phrase in _english_phrases(question):
        folded = paiboon_lookup.fold(phrase)
        found += [e for e in index if e.folded_english and e.folded_english == folded]

    unique, seen = [], set()
    for e in found:
        if e.thai not in seen:
            seen.add(e.thai)
            unique.append(e)
    return unique[:MAX_ENTRIES]


def reference_for(question, index=None):
    """A REFERENCE block for one question, or '' when nothing matches."""
    entries = entries_for(question, index)
    if not entries:
        return ''
    # Matching is by word, so an entry can be beside the point ("hand" the verb
    # finds มือ, the body part). Worded as a spelling list, not a word list, so
    # an irrelevant hit is ignored rather than worked into the answer.
    lines = ["REFERENCE (checked entries from ThaiBridge's own lessons, found by "
             "matching words in the question). If your answer uses any of these "
             "words, write the Thai, romanisation and meaning exactly as listed, "
             "over your memory. Ignore any that are not relevant, and never "
             "mention this list:"]
    for e in entries:
        lines.append(f"- {e.thai} ({e.paiboon})" + (f" = {e.english}" if e.english else ''))
    return '\n'.join(lines)


# ── The spelling tool ────────────────────────────────────────────────────
# reference_for() only covers words in the STUDENT'S question. On 2026-10-14
# the tutor wrote บริบท as "boo-rì-bàt" (it is bɔɔ-rí-bòt): a word it brought
# in itself, from memory. The tool lets the model look up every Thai word it
# is about to write, and check_spellings() below corrects the finished answer
# against the same lessons, so a word the app knows is never misspelt even
# when the model skips the lookup.

SPELLING_TOOL_NAME = 'look_up_thai_spelling'
# One call should cover a whole answer; more than this is a runaway call.
MAX_TOOL_WORDS = 30

SPELLING_TOOL = {
    'name': SPELLING_TOOL_NAME,
    'description': (
        "Look up Thai words in ThaiBridge's reviewed lessons before you write "
        "them. Returns the checked ThaiBridge Spelling and meaning for each "
        "word the lessons contain. For a word they do not contain, returns the "
        "known pieces inside it and every consonant's class, so you can work "
        "out the tones yourself. Call it ONCE, before writing your answer, with "
        "every Thai word and phrase your answer will use."),
    'input_schema': {
        'type': 'object',
        'properties': {
            'words': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'Thai words or short phrases, in Thai script.',
            },
        },
        'required': ['words'],
    },
}

# Tone marks and the vowels that make a syllable short, by name, for the
# tool's breakdown of a word the lessons do not have.
_TONE_MARKS = {'่': 'mai ek', '้': 'mai tho', '๊': 'mai tri', '๋': 'mai chattawa'}
_CLASS_OF = {c['char']: thai_consonants.CLASS_LABELS[c['cls']]
             for c in thai_consonants.CONSONANTS}


def _spellings(index):
    """Thai → the distinct checked spellings the lessons give it."""
    found = {}
    for e in index:
        found.setdefault(e.thai, [])
        if e.paiboon not in found[e.thai]:
            found[e.thai].append(e.paiboon)
    return found


def _letters(word):
    """'บ middle, ร low, ...' for every consonant, then any tone marks."""
    parts = [f"{ch} {_CLASS_OF[ch].lower()}" for ch in word if ch in _CLASS_OF]
    marks = [f"{ch} {_TONE_MARKS[ch]}" for ch in word if ch in _TONE_MARKS]
    text = 'consonant classes: ' + ', '.join(parts)
    if marks:
        text += '; tone marks: ' + ', '.join(marks)
    return text


def _cover(word, by_thai):
    """`word` split wholly into checked words, longest first, or None.

    Only words with one checked spelling count: a piece the lessons spell two
    ways cannot be put back together safely.
    """
    pieces, i = [], 0
    while i < len(word):
        for end in range(len(word), i + 1, -1):
            piece = word[i:end]
            if piece in by_thai and len({e.paiboon for e in by_thai[piece]}) == 1:
                pieces.append(piece)
                i = end
                break
        else:
            return None
    return pieces if len(pieces) > 1 else None


def look_up(words, index=None):
    """The tool's answer, as text, for a list of Thai words."""
    index = _index() if index is None else index
    by_thai = {}
    for e in index:
        by_thai.setdefault(e.thai, []).append(e)

    if not isinstance(words, list):
        words = [words]
    words = [w.strip() for w in words if isinstance(w, str) and w.strip()]
    unique = list(dict.fromkeys(words))[:MAX_TOOL_WORDS]
    if not unique:
        return 'No Thai words were given.'

    lines = []
    for word in unique:
        if word in by_thai:
            entries = by_thai[word]
            spelled = ' or '.join(dict.fromkeys(e.paiboon for e in entries))
            meaning = next((e.english for e in entries if e.english), '')
            lines.append(f"- {word} = {spelled}" + (f" ({meaning})" if meaning else '')
                         + ' — CHECKED, write exactly this')
            continue
        cover = _cover(word.replace(' ', ''), by_thai)
        if cover:
            lines.append(f"- {word} = {' '.join(by_thai[p][0].paiboon for p in cover)} "
                         f"(made of checked words: {' + '.join(cover)}) — write exactly this")
            continue
        pieces = sorted({e.thai for e in index if len(e.thai) >= 2 and e.thai in word},
                        key=lambda t: -len(t))
        known = '; '.join(f"{t} = {by_thai[t][0].paiboon}" for t in pieces[:6])
        line = f"- {word} = NOT IN THE LESSONS. "
        if known:
            line += f"Known pieces: {known}. "
        line += (f"Work it out syllable by syllable ({_letters(word)}): class, "
                 "vowel length, live or dead ending and tone mark decide each tone.")
        lines.append(line)
    # Said here, last thing before the model writes, because a rule in the
    # system prompt alone did not stop it: 2 answers in 5 opened with the
    # tone working ("ยัง: low class ย, short vowel ... so mid tone").
    lines.append("Now write your answer to the student's message. Do any tone "
                 "working in your head: the answer starts with the answer itself "
                 "and never shows the working, unless the student asked for it.")
    return '\n'.join(lines)


# "ไทย (tai)", "**ไทย** (tai)" or "“ไทย” (tai)": a Thai word or phrase,
# then its spelling in brackets. Phrases may contain spaces between Thai words.
_PAIR = re.compile(r'([฀-๿]+(?: [฀-๿]+)*)([*"“”\']*)(\s*)\(([^()\n]{1,80})\)')
# A bracket that is more than one romanisation: alternatives, a gloss.
_NOT_ONE_SPELLING = re.compile(r'[/,;:=]')


def _syllables(spelling):
    return [s for s in re.split(r'[-~\s]+', spelling.strip()) if s]


def _same_word(written, checked):
    """True when `written` is a misspelling of `checked`, not some other text.

    A bracket after Thai is usually its romanisation, but it can be a gloss,
    "ครับ (male)", or a word count. Correct only a bracket with the same number
    of syllables starting with the same sound, so a gloss is never overwritten.
    """
    import paiboon_lookup
    a, b = _syllables(written), _syllables(checked)
    if len(a) != len(b):
        return False
    first_a, first_b = paiboon_lookup.fold_loose(a[0])[:1], paiboon_lookup.fold_loose(b[0])[:1]
    return bool(first_a) and first_a == first_b


def check_spellings(text, index=None):
    """Correct every spelling in `text` the lessons know, and say what changed.

    Returns (corrected text, [(thai, written, checked), ...]). A word with two
    different checked spellings is left alone: the lessons disagree, so there
    is nothing safe to correct it to.
    """
    import unicodedata
    index = _index() if index is None else index
    spellings = _spellings(index)
    by_thai = {}
    for e in index:
        by_thai.setdefault(e.thai, []).append(e)
    fixes = []

    def fix(match):
        thai, stars, space, written = match.groups()
        start = match.start()
        # Part of a list of alternatives, "ครับ/ค่ะ (kráp/kâ)".
        if start and text[start - 1] == '/':
            return match.group(0)
        checked = spellings.get(thai)
        if checked is None:
            # A phrase the lessons do not have whole, made of words they do:
            # ขอบคุณค่ะ is ขอบคุณ + ค่ะ, so it is spelled kɔ̀ɔp-kun kâ.
            cover = _cover(thai.replace(' ', ''), by_thai)
            checked = [' '.join(by_thai[p][0].paiboon for p in cover)] if cover else None
        if (len(thai) < 2 or not checked or len(checked) != 1
                or _NOT_ONE_SPELLING.search(written)):
            return match.group(0)
        right = checked[0]
        bare = written.strip().strip('*')
        if unicodedata.normalize('NFC', bare).lower() == unicodedata.normalize('NFC', right).lower():
            return match.group(0)
        if not _same_word(bare, right):
            return match.group(0)
        fixes.append((thai, bare, right))
        return f"{thai}{stars}{space}({written.replace(bare, right)})"

    return _PAIR.sub(fix, text), fixes
