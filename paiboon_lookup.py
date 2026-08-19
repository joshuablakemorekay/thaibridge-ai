"""The Paiboon lookup — a search box over the romanisation this app already has.

WHAT THIS IS NOT
----------------
It is not a transliterator. There is no rule that turns arbitrary Thai into
Paiboon here, and there deliberately isn't one:

  * A live AI call would cost money per lookup and can be subtly wrong. The
    person reaching for a romanisation lookup is a beginner — exactly the
    person who cannot tell a hallucinated tone mark from a correct one. Getting
    a tone wrong is not a typo in Thai, it is a different word.
  * A rule-based engine sounds tractable until you meet the irregulars: silent
    ห, implicit vowels, ร as a vowel, the ฤ/ฦ letters, loanword spellings that
    ignore the tone rules outright. It would be wrong often, and wrong quietly.

So this searches the corpus we have ALREADY WRITTEN AND REVIEWED. Every hit is
romanisation a human put there on purpose. The tool finds a few thousand
entries rather than all of Thai, and that honest limit is the whole design:
a miss says "not in the corpus", never a confident guess.

HOW THE CORPUS IS GATHERED
--------------------------
Nearly every Thai datum in this codebase is a dict carrying both a `thai` and a
`paiboon` key — 900-odd in app.py alone, plus the chanting book and the
registers. Rather than enumerate those structures by hand (a list that would go
stale the first time someone adds a section), `_walk` recurses through a
module's data and picks up ANY dict with both keys. New content joins the
lookup automatically.

The Alphabet is the exception and gets its own adapter: `thai_consonants.py`
predates the convention and names its fields `char` / `name` / `meaning`.

SEARCHING WITHOUT THE DIACRITICS
--------------------------------
This is the part that makes the tool usable. Paiboon writes "delicious" as
à-rɔ̀i — a grave accent, an open-o, a hyphen. Nobody types that. They type
"aroi". So every entry is indexed under a FOLDED form (see `fold`) with the
tone marks stripped, the IPA-ish letters flattened to ASCII and the hyphens
removed, and the query is folded the same way before matching. The display
always shows the real, fully-marked romanisation — folding is for finding, not
for teaching.
"""
import unicodedata
from dataclasses import dataclass, field

# Paiboon borrows four vowel letters from the IPA that no keyboard has. Folding
# them to their nearest ASCII spelling is what lets "aroi" find "à-rɔ̀i" and
# "phuea" find "pʉ̂a". The values are the letters a learner actually reaches for,
# not a linguistically tidy mapping.
_LETTER_FOLDS = {
    'ɔ': 'o',    # open o, as in ɔɔ ("or")
    'ɛ': 'e',    # ae, as in ɛɛ
    'ɯ': 'u',    # the unrounded u
    'ʉ': 'u',    # same sound, the other glyph Paiboon uses for it
    'ə': 'e',    # oe, as in ləəi
    'ŋ': 'ng',   # eng — spelled out, because that is how it is typed
    'ʔ': '',     # glottal stop: written in some sources, never typed
}

# Combining marks live in this Unicode block. Paiboon's tones are all here once
# the string is decomposed: à á â ǎ become a + U+0300 / U+0301 / U+0302 / U+030C.
_COMBINING_START = 0x0300
_COMBINING_END = 0x036F


def fold(text):
    """Reduce a Paiboon string (or a query) to bare searchable ASCII.

    Tone marks off, IPA letters flattened, separators dropped, lower-cased. The
    hyphens and spaces go because syllable breaks are a presentation choice the
    searcher cannot be expected to guess: "khopkhun", "khop khun" and
    "kɔ̀p-kun" all have to reach the same row.
    """
    if not text:
        return ''
    # NFD splits 'à' into 'a' + combining grave, so the marks can be dropped
    # without also losing the letter they sit on.
    decomposed = unicodedata.normalize('NFD', text.lower())
    out = []
    for ch in decomposed:
        if _COMBINING_START <= ord(ch) <= _COMBINING_END:
            continue                      # a tone mark — strip it
        if ch in _LETTER_FOLDS:
            out.append(_LETTER_FOLDS[ch])
            continue
        if ch in '-– _.,:;!?()/':
            continue                      # separators and stray punctuation
        out.append(ch)
    return ''.join(out)


def fold_loose(text):
    """A blunter fold for the fallback band, forgiving the two spellings that
    otherwise hide the commonest phrases in the language.

    `fold` alone is not enough, because Paiboon spells vowels in a way that no
    self-taught learner types:

      * LENGTH. ขอบคุณ is kɔ̀ɔp-kun — a doubled ɔɔ. Everyone types "kop kun".
      * QUALITY. Paiboon's `ii` is the sound English writes "ee", and its `uu`
        is the sound English writes "oo". สวัสดี is sà-wàt-dii; every beginner
        alive types "sawatdee".

    So: collapse any run of a repeated letter to one (length), then merge e into
    i and o into u (quality). "sawatdee" and "sà-wàt-dii" both land on
    "sawatdi"; "kop kun" and "kɔ̀ɔp-kun" both land on "kupkun".

    This deliberately over-merges — "pèt" (spicy) and "pìt" (wrong) collapse
    together. That is why it is only ever consulted AFTER the precise folds
    have had their turn, and why its hits rank last: a real match is never
    pushed down by a fuzzy one, and a searcher who would otherwise have seen
    nothing gets a near miss to choose from.
    """
    tight = fold(text)
    if not tight:
        return ''
    # RTGS first, before the vowels are touched. Thailand's official
    # romanisation — the one on every road sign, passport and Wikipedia page —
    # writes the aspirated stops as kh/ph/th, where Paiboon writes plain k/p/t.
    # A learner who has only ever seen "Phuket" and "khop khun" is spelling
    # from the signage, and without this they find nothing at all.
    for digraph, plain in (('kh', 'k'), ('ph', 'p'), ('th', 't')):
        tight = tight.replace(digraph, plain)
    # Then merge each voiced stop into its voiceless partner. Thai finals are
    # unreleased, so ขอบ is heard somewhere between "khop" and "khob" and gets
    # written both ways; and Paiboon's own bp/dt digraphs for บ/ต are a
    # notation almost nobody reproduces — "bpai" and "pai", "dtòk" and "tok".
    # Merging the pairs makes all of those spellings land together.
    for voiced, voiceless in (('b', 'p'), ('d', 't'), ('g', 'k')):
        tight = tight.replace(voiced, voiceless)
    collapsed = []
    for ch in tight:
        if not collapsed or collapsed[-1] != ch:
            collapsed.append(ch)
    return ''.join(collapsed).replace('e', 'i').replace('o', 'u')


@dataclass(frozen=True)
class Entry:
    """One row of the lookup: a Thai string and the romanisation we ship for it.

    The three folded forms are computed ONCE here, at index-build time, and
    stored. They were properties in the first cut, which quietly meant folding
    the entire corpus — over a thousand rows, three ways — on every single
    search. Precomputing turns a search back into plain string comparisons.
    """
    thai: str
    paiboon: str
    english: str
    source: str          # human label for where it came from, shown in results

    # Derived, never passed in: see __post_init__.
    folded: str = field(init=False)
    folded_loose: str = field(init=False)
    folded_english: str = field(init=False)

    def __post_init__(self):
        # The dataclass is frozen so that entries can live in sets during
        # de-duplication; object.__setattr__ is the sanctioned way to fill
        # derived fields on a frozen instance.
        object.__setattr__(self, 'folded', fold(self.paiboon))
        object.__setattr__(self, 'folded_loose', fold_loose(self.paiboon))
        object.__setattr__(self, 'folded_english', fold(self.english))


def _walk(node, source, found, seen):
    """Recurse through arbitrary nested data, collecting thai+paiboon dicts.

    Deliberately shape-agnostic: it does not care whether it is looking at
    TOUR_VOCAB, a chanting verse or a register variant. Anything with both keys
    is a romanisation someone reviewed, and therefore belongs in the lookup.
    """
    if isinstance(node, dict):
        thai = node.get('thai')
        paiboon = node.get('paiboon')
        # Both must be non-empty strings. Some records carry a `thai` with the
        # romanisation still to be written (and the chanting book has verses
        # that are English-only rubric); those are facts, not gaps, and they
        # simply have nothing to look up.
        if isinstance(thai, str) and isinstance(paiboon, str) and thai and paiboon:
            # De-duplicate on the FOLDED romanisation, not the raw one. The
            # corpus spells the eng inconsistently — ช้าง is written both
            # 'cháaŋ' and 'cháang' in different sections — and keying on the
            # raw string showed the same word twice in the results. Folding
            # first collapses those to one row; the first source to define it
            # wins, which is why build_index orders the sources by how well
            # reviewed they are.
            key = (thai, fold(paiboon))
            if key not in seen:
                seen.add(key)
                # 'english' is the usual key; the chanting book says 'meaning'
                # for a verse's sense, which is the same thing to a searcher.
                english = node.get('english') or node.get('meaning') or ''
                found.append(Entry(thai, paiboon,
                                   english if isinstance(english, str) else '',
                                   source))
        for value in node.values():
            _walk(value, source, found, seen)
    elif isinstance(node, (list, tuple)):
        for item in node:
            _walk(item, source, found, seen)


def _consonants(found, seen):
    """The 44 letters, which predate the thai/paiboon convention.

    `name` is already Paiboon ('gɔɔ gài'), `name_thai` the Thai ('กอ ไก่') and
    `meaning` the gloss ('chicken'). The obsolete pair ฃ/ฅ stay IN: someone
    meeting one in an old sign is precisely who needs to look it up.
    """
    import thai_consonants
    for c in thai_consonants.CONSONANTS:
        thai = c.get('name_thai')
        paiboon = c.get('name')
        if not (thai and paiboon):
            continue
        key = (thai, fold(paiboon))   # folded, to match _walk's de-duplication
        if key in seen:
            continue
        seen.add(key)
        letter = c.get('char', '')
        meaning = c.get('meaning', '')
        # The gloss names the letter as well as its picture-word, because the
        # letter itself is what the searcher is holding.
        found.append(Entry(thai, paiboon,
                           f'the letter {letter} — {meaning}'.strip(' —'),
                           'Alphabet'))


def build_index():
    """Assemble the whole searchable corpus, most-reviewed source first.

    Order matters only for de-duplication: the same word appears in several
    places, and the first writing of it wins. The Alphabet leads because those
    44 rows are the most scrutinised romanisation in the project.
    """
    found = []
    seen = set()

    _consonants(found, seen)

    # Imported lazily and individually so a broken or missing module degrades
    # to a smaller index rather than taking the whole page down.
    import app
    import thai_reading
    import thai_registers
    import chanting

    # (module, attribute, label shown against a result)
    sources = [
        (thai_reading, 'VOWEL_POSITIONS', 'Read & Write'),
        (thai_reading, 'DHARMA_WORDS', 'Read & Write'),
        (thai_reading, 'STORIES', 'Read & Write'),
        (thai_registers, 'VARIANTS', 'Politeness registers'),
        (app, 'THAI_VOWELS_32', 'Vowels'),
        (app, 'TONES_AND_CLASSES', 'Tones & classes'),
        (app, 'PAIBOON_GUIDE', 'Paiboon guide'),
        (app, 'VOCABULARY', 'Vocabulary'),
        (app, 'GRAMMAR', 'Grammar'),
        (app, 'SENTENCE_PATTERNS', 'Sentences'),
        (app, 'CONVERSATIONAL_PHRASES', 'Conversations'),
        (app, 'CONVERSATIONS', 'Conversations'),
        (app, 'LESSONS', 'Lessons'),
        (app, 'FORMALITY_LEVELS', 'Formality'),
        (app, 'GENDER_VARIANTS', 'Gendered speech'),
        (app, 'TOUR_VOCAB', 'Tour guide'),
        (app, 'BUSINESS_VOCAB', 'Business Thai'),
        (app, 'MONK_TOPICS', 'Monk Mode'),
        (app, 'MEDITATION_TECHNIQUES', 'Meditation'),
        (app, 'CULTURAL_INFO', 'Culture'),
        (app, 'CULTURAL_FEATURE_STORIES', 'Culture'),
    ]
    for module, attribute, label in sources:
        data = getattr(module, attribute, None)
        if data is not None:
            _walk(data, label, found, seen)

    # The chanting book last: it is the largest source by far (1,500+ verses)
    # and its romanisation is still an unreviewed draft in places, so anything
    # already written elsewhere should win the de-dupe over it.
    _walk(getattr(chanting, 'CHANTS', None), 'Chanting book', found, seen)

    return found


# The index is built once per process and reused. It is derived from module
# constants that cannot change at runtime, so there is nothing to invalidate.
_INDEX = None


def get_index():
    global _INDEX
    if _INDEX is None:
        _INDEX = build_index()
    return _INDEX


# Ranking bands. A searcher typing an exact word wants that word at the top,
# not a chant verse that happens to contain it.
_RANK_EXACT = 0
_RANK_PREFIX = 1
_RANK_CONTAINS = 2


def _rank(haystack, needle):
    """Which band a hit falls into, or None if it is not a hit at all."""
    if not haystack or not needle:
        return None
    if haystack == needle:
        return _RANK_EXACT
    if haystack.startswith(needle):
        return _RANK_PREFIX
    if needle in haystack:
        return _RANK_CONTAINS
    return None


def search(query, limit=40):
    """Find entries matching `query`, best first.

    Three things are searched at once, because a learner arrives holding any
    one of them: the Thai script (pasted from a sign or a chat), the
    romanisation (typed loosely, without tones), or the English.

    Thai is matched raw — folding is meaningless for it — while romanisation
    and English are matched folded. Results are ordered by how tight the match
    is, then by the length of the entry, so the single word beats the sentence
    that contains it.
    """
    query = (query or '').strip()
    if not query:
        return []

    folded_query = fold(query)
    loose_query = fold_loose(query)
    has_thai = any('฀' <= ch <= '๿' for ch in query)

    # Every field is scored, and the BAND (exact / prefix / contains) is the
    # primary sort key, with the field's precision only breaking ties inside a
    # band.
    #
    # Field-major ordering was the first attempt and it ranked badly: searching
    # "chang" put three long sentences above ช้าง itself, because "dì-chǎn
    # gam-laŋ …" folds to "dichangamlang", which happens to CONTAIN "chang"
    # across a syllable boundary, and any tight-fold hit outranked the loose
    # exact match on the word. An incidental substring is never a better answer
    # than an exact one, whichever fold found it — hence band first.
    scored = []
    found_something_precise = False

    for entry in get_index():
        precise = []
        # Thai takes the raw query: someone pasting ไม่เผ็ด means those glyphs,
        # and folding Thai script would be meaningless.
        if has_thai:
            band = _rank(entry.thai, query)
            if band is not None:
                precise.append((band, 0))
        for field_precision, haystack in enumerate(
                (entry.folded, entry.folded_english), start=1):
            band = _rank(haystack, folded_query)
            if band is not None:
                precise.append((band, field_precision))

        loose_band = _rank(entry.folded_loose, loose_query)
        if precise:
            found_something_precise = True
        scored.append((entry, min(precise) if precise else None, loose_band))

    hits = []
    for entry, precise, loose_band in scored:
        candidates = []
        if precise is not None:
            candidates.append(precise)
        if loose_band is not None:
            # The fuzzy band is allowed to CONTRIBUTE an exact or prefix hit
            # always — that is what rescues ช้าง when a long sentence happens to
            # contain "chang" as a substring and would otherwise outrank it.
            #
            # Its substring hits are a different matter: they are the noisy
            # ones. Searching "aroi" turned up two long price sentences,
            # because "rɔ́ɔi" (hundred) sits inside them and survives the fuzzy
            # merge. So a loose SUBSTRING only counts when nothing precise was
            # found anywhere — a genuine last resort, rather than five results
            # where three were wanted.
            if loose_band <= _RANK_PREFIX or not found_something_precise:
                candidates.append((loose_band, 3))
        if candidates:
            band, field_precision = min(candidates)
            # Shorter entries first within a band: someone searching "aroi"
            # wants the word อร่อย, not the sentence that happens to contain it.
            hits.append((band, field_precision, len(entry.thai), entry))

    hits.sort(key=lambda h: h[:3])
    return [entry for *_, entry in hits[:limit]]
