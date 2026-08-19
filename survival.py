"""Survival Thai — the free, finishable starter set.

WHY THIS EXISTS
---------------
The free tier was Buddhism plus an alphabet chart. Someone who arrives wanting
to SPEAK Thai — the largest group of visitors — could look at 44 consonants and
then hit a paywall, having said nothing to anybody. There was no free thing they
could finish, and "finish something" is what makes a learner come back.

This is that thing: four short sets, about forty phrases, doable in one sitting.
It deliberately does NOT teach the script. Every other language page on the site
requires the alphabet quiz first, which is the right prerequisite for reading
and the wrong one for saying hello.

WHY NOT ON THE TOUR GUIDE PAGE
------------------------------
Tour Guide covers similar ground, and putting this there was the obvious move.
But Tour Guide is `basic` tier, level 4, and alphabet-gated — so this would have
either forced a paid section free or buried the free taster behind £9.99 and 44
consonants. The overlap is real and fine: a taster is meant to overlap the thing
it is a taste of. Tour Guide stays the deeper set for someone already paying.

⚠️  DRAFT THAI — every Thai string below is a first draft awaiting review by
Josh and teacher Paiboon. Nothing here is final.

A NOTE ON THE PARTICLES
-----------------------
Thai politeness particles are gendered: a man ends with ครับ (kráp), a woman
with ค่ะ (kâ). Rather than pick one and quietly teach half the learners to
sound wrong, phrases that need a particle carry `particle: True` and the page
shows both. This matches how /gender-examples already handles it.
"""

# The gendered polite particle, shown on any phrase marked `particle`.
POLITE_PARTICLE = {
    'male':   {'thai': 'ครับ', 'paiboon': 'kráp'},
    'female': {'thai': 'ค่ะ',  'paiboon': 'kâ'},
}


def _p(thai, paiboon, english, note='', particle=False):
    """One phrase. `particle` marks the ones that need ครับ/ค่ะ on the end."""
    return {
        'thai': thai,
        'paiboon': paiboon,
        'english': english,
        'note': note,
        'particle': particle,
    }


# Ordered deliberately: greetings first because it is the one exchange a
# learner can complete with a real person the same day, numbers second because
# every other set leans on them (prices, quantities, directions).
SETS = [
    {
        'key': 'greetings',
        'title': 'Greetings & politeness',
        'emoji': '🙏',
        'blurb': 'Enough to open and close a conversation politely. If you learn '
                 'nothing else here, learn สวัสดี and ขอบคุณ.',
        'phrases': [
            _p('สวัสดี', 'sà-wàt-dii', 'Hello / Goodbye',
               'The all-purpose greeting, any time of day.', particle=True),
            _p('ขอบคุณ', 'kɔ̀ɔp-kun', 'Thank you',
               'Add มาก (mâak) for "thank you very much".', particle=True),
            _p('ขอโทษ', 'kɔ̌ɔ-tôot', 'Sorry / Excuse me',
               'Also how you get someone\'s attention politely.', particle=True),
            _p('ไม่เป็นไร', 'mâi bpen rai', 'It\'s nothing / No problem',
               'The reply to ขอโทษ, and a whole Thai attitude in three words.'),
            _p('สบายดีไหม', 'sà-baai dii mǎi', 'How are you?'),
            _p('สบายดี', 'sà-baai dii', 'I\'m well'),
            _p('ใช่', 'châi', 'Yes'),
            _p('ไม่ใช่', 'mâi châi', 'No'),
            _p('ไม่เข้าใจ', 'mâi kâo-jai', 'I don\'t understand',
               'The most useful sentence on this page.'),
            _p('พูดช้าๆ ได้ไหม', 'pûut cháa cháa dâi mǎi',
               'Could you speak slowly?'),
            _p('คุณพูดภาษาอังกฤษได้ไหม', 'kun pûut paa-sǎa aŋ-grìt dâi mǎi',
               'Do you speak English?'),
        ],
    },
    {
        'key': 'numbers',
        'title': 'Numbers',
        'emoji': '🔢',
        'blurb': 'Thai numbers are regular once you have one to ten: eleven is '
                 '"ten-one", twenty-one is "two-ten-one". Learn these and you can '
                 'count to a hundred.',
        'phrases': [
            _p('ศูนย์', 'sǔun', 'Zero'),
            _p('หนึ่ง', 'nʉ̀ŋ', 'One'),
            _p('สอง', 'sɔ̌ɔŋ', 'Two'),
            _p('สาม', 'sǎam', 'Three'),
            _p('สี่', 'sìi', 'Four'),
            _p('ห้า', 'hâa', 'Five',
               'Thai texting: "555" is laughter, because ห้า sounds like "ha".'),
            _p('หก', 'hòk', 'Six'),
            _p('เจ็ด', 'jèt', 'Seven'),
            _p('แปด', 'bpɛ̀ɛt', 'Eight'),
            _p('เก้า', 'gâo', 'Nine'),
            _p('สิบ', 'sìp', 'Ten'),
            _p('สิบเอ็ด', 'sìp-èt', 'Eleven',
               'Note: "one" becomes เอ็ด (èt), not หนึ่ง, in the teens and after.'),
            _p('ยี่สิบ', 'yîi-sìp', 'Twenty',
               'Twenty is the one irregular: ยี่ (yîi), not สอง.'),
            _p('ร้อย', 'rɔ́ɔi', 'Hundred'),
            _p('พัน', 'pan', 'Thousand'),
        ],
    },
    {
        'key': 'food',
        'title': 'Ordering food',
        'emoji': '🍜',
        'blurb': 'Enough to order, ask what something costs, and control how spicy '
                 'it comes. เผ็ด is the word to get right.',
        'phrases': [
            _p('เอา', 'ao', 'I\'ll have / I want',
               'Point and say เอาอันนี้ (ao an níi) — "I\'ll have this one".'),
            _p('อันนี้', 'an níi', 'This one'),
            _p('อร่อย', 'à-rɔ̀i', 'Delicious',
               'Say it to the cook. It goes a long way.'),
            _p('เผ็ด', 'pèt', 'Spicy'),
            _p('ไม่เผ็ด', 'mâi pèt', 'Not spicy',
               'Thai "not spicy" and your "not spicy" may still differ.'),
            _p('เผ็ดนิดหน่อย', 'pèt nít nɔ̀i', 'A little bit spicy'),
            _p('น้ำ', 'náam', 'Water'),
            _p('ข้าว', 'kâao', 'Rice',
               'Also means "food" or "a meal" in general.'),
            _p('กินเจ', 'gin jee', 'I eat vegetarian',
               'เจ is strict vegan-Buddhist; มังสวิรัติ (maŋ-sà-wí-rát) is ordinary '
               'vegetarian.'),
            _p('เท่าไหร่', 'tâo-rài', 'How much?'),
            _p('แพง', 'pɛɛŋ', 'Expensive'),
            _p('เช็คบิล', 'chék-bin', 'The bill, please',
               'Borrowed straight from English "check bill".'),
        ],
    },
    {
        'key': 'directions',
        'title': 'Getting around',
        'emoji': '🧭',
        'blurb': 'Enough to get into a taxi, say where you are going, and understand '
                 'the answer when you ask where something is.',
        'phrases': [
            _p('ไป', 'bpai', 'Go / To'),
            _p('ไป...ครับ/ค่ะ', 'bpai … kráp/kâ', 'To ___, please',
               'The whole taxi transaction: ไป plus the place name.'),
            _p('ที่ไหน', 'tîi nǎi', 'Where?'),
            _p('ห้องน้ำอยู่ที่ไหน', 'hɔ̂ŋ-náam yùu tîi nǎi',
               'Where is the toilet?'),
            _p('ตรงไป', 'droŋ bpai', 'Straight ahead'),
            _p('เลี้ยวซ้าย', 'líiao sáai', 'Turn left'),
            _p('เลี้ยวขวา', 'líiao kwǎa', 'Turn right'),
            _p('หยุดที่นี่', 'yùt tîi nîi', 'Stop here'),
            _p('ใกล้', 'glâi', 'Near'),
            _p('ไกล', 'glai', 'Far',
               'Near and far differ only by tone — glâi is near, glai is far.'),
            _p('ช่วยด้วย', 'chûai dûai', 'Help!'),
            _p('โรงพยาบาล', 'rooŋ-pá-yaa-baan', 'Hospital'),
        ],
    },
]

SETS_BY_KEY = {s['key']: s for s in SETS}


def all_phrases():
    """Every phrase across every set, in page order."""
    return [phrase for group in SETS for phrase in group['phrases']]


def thai_strings():
    """Every pronounceable Thai string, for the audio build script.

    The particle forms are included as bare words: the page renders them beside
    a phrase, but a learner taps them on their own to hear the difference
    between kráp and kâ.
    """
    found = [phrase['thai'] for phrase in all_phrases()]
    found.extend(form['thai'] for form in POLITE_PARTICLE.values())
    # Two things are dropped, the way gender_thai_strings() drops its combined
    # forms. Both would produce nonsense if read aloud:
    #   '...'  a TEMPLATE — the blank is where a place name goes, so
    #          'ไป...ครับ/ค่ะ' is a shape rather than a sentence.
    #   '/'    an EITHER-OR — 'ครับ/ค่ะ' means "one of these depending on who is
    #          speaking", not a phrase. The particles are recorded separately
    #          above, which is how a learner hears the difference.
    return [thai for thai in found if '...' not in thai and '/' not in thai]
