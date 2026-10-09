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


def _index():
    # Imported here, not at the top: building the index imports app, and app
    # imports the AI agent, so a top-level import would be circular.
    import paiboon_lookup
    return [e for e in paiboon_lookup.get_index() if e.source not in UNREVIEWED_SOURCES]


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
