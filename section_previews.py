"""Public previews for the course sections that need an account or a plan.

A visitor who opens a locked section used to see only a generic "Section
Locked" notice — the same thin page at a dozen addresses, which search engines
mark down and which told the visitor nothing about what they would get.
locked.html now shows the preview below FIRST, then the existing unlock
requirements, so the page is worth reading and worth listing in search.

Every fact here is taken from the section itself; keep them in step when a
section changes (tests/test_section_previews.py checks the counts). Keep to the
course-first voice: what you will be able to DO, not marketing. Audio is
tap-to-hear text-to-speech — never call it a "real" or native recording.

Keyed by the section id used in @require_access(...) / SECTION_REQUIREMENTS.
"""

SECTION_PREVIEWS = {
    'lessons': {
        'path': '/lessons',
        'name': 'Structured Lessons',
        'summary': '15 step-by-step Thai lessons, from beginner to advanced. Each one sets out what you will learn, the vocabulary, the grammar point and example sentences.',
        'points': [
            'A clear order to follow, so you always know what comes next',
            'Objectives, vocabulary and a grammar point in every lesson',
            'Example sentences in Thai script with JaiScript and English',
        ],
    },
    'learn': {
        'path': '/learn',
        'name': 'Vocabulary',
        'summary': 'Themed Thai vocabulary sets, each with 20 words in Thai script, JaiScript and English, plus practice quizzes and tap-to-hear audio.',
        'points': [
            'Six themed categories, from everyday words to festivals and the Dhamma',
            'Every word in Thai script, JaiScript and English',
            'A practice quiz for each category',
        ],
    },
    'grammar': {
        'path': '/grammar',
        'name': 'Thai Grammar Guide',
        'summary': 'A plain-English guide to Thai grammar: parts of speech, sentence structure, particles, tense and aspect, questions, negation and comparison.',
        'points': [
            'How Thai sentences are built, and why the verb never changes',
            'Particles, question words and how to say "not"',
            'How consonant classes decide the tone of a word',
        ],
    },
    'sentences': {
        'path': '/sentences',
        'name': 'Sentences & Conversations',
        'summary': 'Thai sentence patterns and real-world conversations: talk about now, the past and the future, ask and answer questions, and build sentences yourself.',
        'points': [
            'The difference between Formal, Neutral and Casual Thai',
            'A sentence builder to practise putting words in order',
            'Real-world conversations with listen-and-answer practice',
        ],
    },
    'vowels_syllables': {
        'path': '/vowels_syllables',
        'name': 'Thai Vowels & Syllables',
        'summary': 'The Thai vowels, long and short, and how vowel length changes meaning, plus how a Thai syllable is put together.',
        'points': [
            'Every long and short vowel, with examples',
            'Why a long or short vowel can change the whole word',
            'How Thai syllables are structured, including live and dead syllables',
        ],
    },
    'tones_classes': {
        'path': '/tones-classes',
        'name': 'Tones & Consonant Classes',
        'summary': 'How Thai tones work: the three consonant classes, the tone marks, and the one idea that makes the rules click, with practice drills.',
        'points': [
            'The three consonant classes and why they matter',
            'How tone marks and syllable type decide the tone',
            'Practice drills to test yourself',
        ],
    },
    'read_write': {
        'path': '/read_write',
        'name': 'Read & Write Thai Script',
        'summary': 'Put the alphabet to work: sound out real syllables, read a short Dhamma story, and practise forming the Thai letters yourself.',
        'points': [
            'Sound out real Thai syllables, step by step',
            'Read a short Dhamma story with vocabulary notes',
            'Learn how each Thai letter is formed',
        ],
    },
    'formality': {
        'path': '/formality',
        'name': 'Thai Formality',
        'summary': 'How politeness works in Thai: which words to use with monks, elders, colleagues and friends, and how to read the formality badges across the course.',
        'points': [
            'From temple language to everyday speech, explained with examples',
            'When to use each level of politeness',
            'Practical tips so you never sound rude by accident',
        ],
    },
    'register': {
        'path': '/register',
        'name': 'Thai Language Register',
        'summary': 'The levels of Thai speech, from sacred monastic language to casual slang, and how to choose the right one for who you are talking to.',
        'points': [
            'Each level of Thai speech, explained',
            'Who each level is used with, and why',
            'Key takeaways to remember',
        ],
    },
    'gender_examples': {
        'path': '/gender-examples',
        'name': 'Gender & Formality Guide',
        'summary': 'In Thai, the words for "I" and the polite endings change with the speaker. See the pronouns, particles, greetings and sentences that fit you.',
        'points': [
            'The pronouns for "I", and when to use each',
            'Polite particles such as ครับ (kráp) and ค่ะ (kâ)',
            'Greetings and full sentence examples you can switch between',
        ],
    },
    'culture': {
        'path': '/culture',
        'name': 'Thai Culture & Etiquette',
        'summary': 'Thai culture for learners: major festivals, cultural stories, everyday etiquette tips and Isan culture, so your Thai fits the situation.',
        'points': [
            'The major Thai festivals and what happens at each',
            'Cultural stories and important etiquette tips',
            'An introduction to Isan culture',
        ],
    },
    'tour_guide': {
        'path': '/tour-guide',
        'name': 'Tour Guide Thai',
        'summary': 'Seven short trips around Thailand: someone speaks to you in Thai and you choose what to say back. Finish a trip to collect its stamp. Includes a travel phrasebook.',
        'points': [
            'Seven interactive trips, each a short story in Thai',
            'A phrasebook for transport, hotels, sightseeing, shopping, food and emergencies',
            'Free travel ideas for things to do in Thailand',
        ],
    },
    'business_thai': {
        'path': '/business-thai',
        'name': 'Business Thai',
        'summary': 'Professional Thai for working in Thailand: greetings and introductions, meetings, the office, banking, contracts, and titles and hierarchy at work.',
        'points': [
            'Thai business culture: hierarchy, titles and "face"',
            'Phrases for meetings, negotiations and office life',
            'Banking, contracts and corporate titles',
        ],
    },
    'dictionary': {
        'path': '/dictionary',
        'name': 'Thai-English Dictionary',
        'summary': 'Look up Thai and English words in a full Thai-English dictionary built from the LEXiTRON corpus.',
        'points': [
            'Search in Thai or in English',
            'Thousands of entries from the LEXiTRON corpus',
            'Part of the Thai Master plan',
        ],
    },
}


def preview_for(section_id):
    return SECTION_PREVIEWS.get(section_id)
