"""The curriculum outline — everything the site teaches, on one page, for everyone.

WHY IT IS PUBLIC
----------------
Most of ThaiBridge is paid, and until now the only way to find out what "Thai
Reader (Basic)" actually contains was to buy it. A tier's feature list gave
eight bullet points for twenty-odd sections. People pay more readily when they
can see what they are buying, and the sections themselves are the strongest
argument for the price — so the outline shows all of them, locked ones
included, with the level and tier each one needs.

WHY IT IS BUILT, NOT WRITTEN
----------------------------
The obvious implementation is a hand-written list of titles and URLs beside the
tier table. This project already knows what that costs: the Culture page built
its practice links by guessing a URL from a dict key, and one story pointed at
a 404 for months with nothing in the code looking wrong. `require_access` now
records the section it guards on the view function itself, so the outline is
assembled FROM THE ROUTES — a gated page is on the outline because it is gated,
not because someone remembered to add it.

`assert_outline_is_complete()` runs at import and closes the loop the other
way: every section in SECTION_REQUIREMENTS must be on the outline, deliberately
excluded, or the app refuses to start. Adding a section and forgetting to
advertise it is then impossible.
"""

# Sections that exist in SECTION_REQUIREMENTS but are not curriculum, and the
# reason each one is here. Anything not on the outline must be named in one of
# these two maps, so an exclusion is always a decision someone wrote down.
NOT_LEARNING_CONTENT = {
    'home': 'the landing page, not something you study',
    'premium': 'the pricing page itself — it would list itself',
}

# Declared in SECTION_REQUIREMENTS with a tier and a level, but no route and no
# template anywhere in the project. They are not built. Advertising them on a
# page whose whole job is to say honestly what the money buys would be exactly
# the wrong place to be aspirational, so they are held back until they exist.
NOT_BUILT_YET = {
    'greetings_wai': 'no route or template — never built',
    'classifiers': 'no route or template — never built',
}

# Display names. `require_access` knows the section id, not what a human calls
# it, and 'gender_examples'.title() gives "Gender Examples" where the nav has
# always said "Gender Guide". These are the names already used in the sidebars,
# so the outline and the nav agree.
SECTION_TITLES = {
    'alphabet': 'Thai Alphabet',
    'tones_classes': 'Tones & Consonant Classes',
    'vowels_syllables': 'Vowels & Syllables',
    'read_write': 'Read & Write Thai Script',
    'paiboon': 'Paiboon Romanization & Lookup',
    'grammar': 'Grammar',
    'formality': 'Formality',
    'register': 'Politeness Registers',
    'gender_examples': 'Gender Guide',
    'sentences': 'Sentences',
    'learn': 'Vocabulary',
    'lessons': 'Lessons',
    'tour_guide': 'Tour Guide',
    'business_thai': 'Business Thai',
    'culture': 'Thai Culture',
    'dictionary': 'Thai–English Dictionary',
    'theravada': 'Theravada Dharma',
    'meditation': 'Meditation',
    'chanting': 'Digital Chanting Book',
    'dhamma_and_culture': 'Dhamma, Culture & Thailand',
    'practising_anywhere': 'Practising the Dhamma Anywhere',
    'exercise_festivals': 'Festival Vocabulary',
    'exercise_nature': 'Nature Vocabulary',
    'exercise_formal': 'Buddhist Formal Vocabulary',
    'exercise_isan_dialect': 'Isan Dialect',
}

# Sections whose URL cannot be discovered from a decorator.
#
#   * alphabet is deliberately UNGATED — it is the free gateway every other
#     section's prerequisite points at, so it carries no @require_access and
#     would otherwise be missing from the outline it heads.
#   * the exercise_* sections share one /exercise/<category> route that checks
#     access inside the handler, so there is no per-section view to tag.
UNDISCOVERABLE_URLS = {
    'alphabet': '/alphabet',
    'exercise_festivals': '/exercise/festivals',
    'exercise_nature': '/exercise/nature',
    'exercise_formal': '/exercise/buddhist_formal',
    'exercise_isan_dialect': '/exercise/isan_dialect',
}

# The order tiers are shown in. Their NAMES and prices are not repeated here:
# they are read from SUBSCRIPTION_TIERS, so the outline cannot drift from the
# pricing table sitting directly above it on the same page. (The first draft
# hardcoded them and immediately invented a tier called "Fluency" that does not
# exist — the real one is "Thai Master".)
TIER_ORDER = ('free', 'basic', 'pro')


def _title(section_id):
    """A human name for a section, falling back to a tidied-up id.

    The fallback exists so a newly added section shows up on the outline
    looking slightly scruffy rather than not showing up at all. A missing
    entry here is a cosmetic bug; a missing section is a broken promise.
    """
    return SECTION_TITLES.get(section_id, section_id.replace('_', ' ').title())


def _discover_urls(flask_app):
    """Map section id → URL for every view that `require_access` guards.

    Reads the `_section_id` attribute the decorator stamps on each wrapped
    view, then asks Flask's own url_map for that endpoint's rule. Routes that
    take parameters are skipped: there is no single URL to link to.
    """
    urls = {}
    for rule in flask_app.url_map.iter_rules():
        view = flask_app.view_functions.get(rule.endpoint)
        section_id = getattr(view, '_section_id', None)
        if not section_id or rule.arguments:
            continue
        # Several views can guard the same section — the chanting book has both
        # /chanting and /chanting/pages. The shortest rule is the landing page
        # and the one to link to; without this the winner is whichever route
        # Flask happened to register last, which put the outline's chanting
        # link on the page index rather than the book's front door.
        existing = urls.get(section_id)
        if existing is None or len(rule.rule) < len(existing):
            urls[section_id] = rule.rule
    return urls


def build_outline(app_module):
    """Group every taught section by the tier that opens it.

    Returns a list of {tier, label, sections} in TIER_ORDER, each section
    carrying its title, URL, level and tier. Sections are ordered by the level
    they unlock at, then by name — which is the order someone works through
    them, and the order that makes a tier's contents read as a path.
    """
    urls = dict(UNDISCOVERABLE_URLS)
    urls.update(_discover_urls(app_module.app))

    by_tier = {tier: [] for tier in TIER_ORDER}
    for section_id, requirement in app_module.SECTION_REQUIREMENTS.items():
        if section_id in NOT_LEARNING_CONTENT or section_id in NOT_BUILT_YET:
            continue
        url = urls.get(section_id)
        if url is None:
            continue          # nothing to link to; assert_* below catches it
        tier = requirement.get('tier', 'free')
        by_tier.setdefault(tier, []).append({
            'id': section_id,
            'title': _title(section_id),
            'url': url,
            'level': requirement.get('level', 1),
            'tier': tier,
        })

    outline = []
    for tier in TIER_ORDER:
        sections = sorted(by_tier.get(tier, []),
                          key=lambda s: (s['level'], s['title']))
        if not sections:
            continue
        details = app_module.SUBSCRIPTION_TIERS.get(tier, {})
        outline.append({
            'tier': tier,
            'label': details.get('name', tier.title()),
            'price': details.get('price', 0),
            # Pro adds exactly ONE page (the dictionary) and would look thin
            # next to Basic's seventeen. What it actually sells is unlimited
            # AI, the roleplay partner and the exercise generator — none of
            # which are sections and none of which the page count can show. So
            # the tier's own feature list is carried alongside its pages, or
            # the outline would undersell the most expensive tier.
            'features': details.get('features', []),
            'sections': sections,
        })
    return outline


def assert_outline_is_complete(app_module):
    """Every section is on the outline or deliberately left off. No third case.

    Runs at import, the way _assert_story_links_resolve() does for the Culture
    page. Two failures are possible and both are silent without this:

      * a new section is added to SECTION_REQUIREMENTS and never advertised,
        so people pay for a tier whose contents are understated;
      * a section is excluded for a reason nobody recorded, and the exclusion
        outlives the reason.

    Raising at import turns both into a failure on the next test run rather
    than a quiet gap on the pricing page.
    """
    outlined = {s['id'] for group in build_outline(app_module)
                for s in group['sections']}
    accounted = outlined | set(NOT_LEARNING_CONTENT) | set(NOT_BUILT_YET)

    missing = sorted(set(app_module.SECTION_REQUIREMENTS) - accounted)
    if missing:
        raise RuntimeError(
            'These sections are in SECTION_REQUIREMENTS but would not appear '
            'on the public curriculum outline: ' + ', '.join(missing) + '. '
            'Either they need a route (so the outline can find them), an entry '
            'in curriculum.UNDISCOVERABLE_URLS, or a recorded reason in '
            'NOT_LEARNING_CONTENT / NOT_BUILT_YET.')

    stale = sorted((set(NOT_LEARNING_CONTENT) | set(NOT_BUILT_YET))
                   - set(app_module.SECTION_REQUIREMENTS))
    if stale:
        raise RuntimeError(
            'These sections are excluded from the curriculum outline but no '
            'longer exist in SECTION_REQUIREMENTS: ' + ', '.join(stale) + '. '
            'Remove them from curriculum.py — the exclusion has outlived what '
            'it was excluding.')
