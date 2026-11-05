"""Site search — the box under the top menu, and the /search results page.

One query, two kinds of answer, because a visitor arrives holding one of two
things:

  * the NAME of something ("grammar", "meditation", "refund") — answered from
    the list of pages. The learning sections come from curriculum.build_outline,
    the same list the Premium page shows, so a new section is searchable the
    day it is added and nothing here can drift out of step with it.
  * a WORD ("hello", "sawat", or สวัสดี pasted from a chat) — answered by
    paiboon_lookup.search, the lookup that already powers the free box on
    /paiboon. Reusing it means one ranking, one set of folding rules, and no
    second copy of the corpus. Each word links to the page that teaches it.

Nothing paid is given away: page results only link (a locked page still shows
its own lock), and word results are exactly what the free /paiboon lookup
already returns.
"""
import paiboon_lookup

# Word results carry a source label from paiboon_lookup; this is where each
# label lives on the site. A test fails if the index gains a label that is not
# here, so a new source can never produce a result that links nowhere.
SOURCE_URLS = {
    'Alphabet': '/alphabet',
    'Survival Thai': '/survival',
    'Read & Write': '/read_write',
    'Politeness registers': '/sentences',
    'Vowels': '/vowels_syllables',
    'Tones & classes': '/tones-classes',
    'Paiboon guide': '/paiboon',
    'Vocabulary': '/learn',
    'Grammar': '/grammar',
    'Sentences': '/sentences',
    'Conversations': '/sentences#conversations',
    'Lessons': '/lessons',
    'Formality': '/formality',
    'Gendered speech': '/gender-examples',
    'Tour guide': '/tour-guide',
    'Business Thai': '/business-thai',
    'Monk Mode': '/monk-mode',
    'Meditation': '/meditation',
    'Culture': '/culture',
    'Chanting book': '/chanting',
}

# Pages that are not lessons, so the curriculum outline leaves them out, but
# that people still look for by name. The keywords are the words someone would
# actually type when they can't remember what the page is called.
OTHER_PAGES = [
    {'title': 'Help & how to use the site', 'url': '/instructions',
     'keywords': 'help guide how to start learning support accessibility'},
    {'title': 'AI Tutor', 'url': '/chat',
     'keywords': 'ai tutor chat ask question translate translator practise'},
    {'title': 'Monk Mode', 'url': '/monk-mode',
     'keywords': 'monk monks english lessons sangha'},
    {'title': "Pra Kru Bob's Writings", 'url': '/bob-writings',
     'keywords': 'pra kru bob writings dhamma essays'},
    {'title': 'Journal', 'url': '/journal', 'keywords': 'journal blog news'},
    {'title': 'My Progress', 'url': '/progress',
     'keywords': 'progress xp level points receipts account'},
    {'title': 'Plans & pricing', 'url': '/premium',
     'keywords': 'premium pricing price plans subscribe basic pro upgrade'},
    {'title': 'Policies, billing & refunds', 'url': '/policies',
     'keywords': 'policies billing refund refunds cancel terms'},
    {'title': 'About ThaiBridge AI', 'url': '/about', 'keywords': 'about'},
    {'title': 'Contact', 'url': '/contact',
     'keywords': 'contact email feedback report'},
    {'title': 'Privacy', 'url': '/privacy', 'keywords': 'privacy data cookies'},
]

# Enough to scan at a glance. The /paiboon page is there for anyone who wants
# every last match for a word.
MAX_WORDS = 20

# A query this long is not a search; cap it rather than fold a whole essay.
MAX_QUERY = 100


def _all_pages(outline):
    """Every searchable page: the learning sections, then the rest."""
    pages = []
    for group in outline:
        for section in group['sections']:
            pages.append({'title': section['title'], 'url': section['url'],
                          'tier': section['tier'], 'tier_label': group['label'],
                          'level': section['level'], 'keywords': ''})
    for page in OTHER_PAGES:
        pages.append(dict(page, tier='free', tier_label='Free', level=1))
    return pages


def search_pages(query, outline):
    """Pages whose name (or keywords) contain every word of the query.

    Every word, not any word: "thai culture" should find Thai Culture, not
    every page with "Thai" in its title. Titles that match outrank keyword-only
    matches, and a shorter title wins a tie, so "Grammar" beats a longer page
    that happens to mention it.
    """
    # Split BEFORE folding: fold() drops spaces (so "khop khun" finds
    # "kɔ̀p-kun"), which would weld the words together. One-letter words are
    # dropped because "a" is inside nearly every title.
    words = [w for w in (paiboon_lookup.fold(part) for part in (query or '').split())
             if len(w) >= 2]
    if not words:
        return []
    hits = []
    for page in _all_pages(outline):
        title = paiboon_lookup.fold(page['title'])
        haystack = title + ' ' + paiboon_lookup.fold(page['keywords'])
        if all(w in haystack for w in words):
            in_title = all(w in title for w in words)
            hits.append((0 if in_title else 1, len(page['title']), page))
    hits.sort(key=lambda h: h[:2])
    return [page for *_, page in hits]


def search_words(query):
    """Thai words and phrases matching the query, each with a link."""
    return [{'thai': e.thai, 'paiboon': e.paiboon, 'english': e.english,
             'source': e.source, 'url': SOURCE_URLS.get(e.source)}
            for e in paiboon_lookup.search(query, limit=MAX_WORDS)]


def search(query, outline):
    """Both kinds of result for one query: {'pages': [...], 'words': [...]}."""
    query = (query or '').strip()[:MAX_QUERY]
    if not query:
        return {'pages': [], 'words': []}
    return {'pages': search_pages(query, outline),
            'words': search_words(query)}
