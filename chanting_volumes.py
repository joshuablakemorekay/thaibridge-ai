"""The plan for the THREE-VOLUME print edition, the chants for each day of
the week, and the occasion index (Josh, 2026-11-12, from Pra Kru Bob's
request).

Nothing here changes a chant or the temple book's order. A volume is a
choice of the book's own Parts, kept in the temple order inside each volume;
the one-volume edition stays exactly as it was, with the new guides added.

THIS IS A DRAFT FOR THE ABBOT TO DECIDE. Which Part goes in which volume is
one number in PART_VOLUME below, so his decision is a one-line change:
    - move a whole Part:      change its number in PART_VOLUME
    - split a Part:           add the first chant of the moved run to SPLITS
    - move a single chant:    add it to CHANT_VOLUME
then rebuild with scripts/build_chanting_print.py --volumes.

Draft rule (Pra Kru Bob's note):
    Volume 1  the daily book: morning and evening chanting, the protection
              chants and blessings used most (Maṅgala, Bojjhaṅga, Jayamaṅgala,
              sharing of merit, the Mātikā), the day-of-the-week chants and
              the Amaravati reflections
    Volume 2  more suttas: the evening discourses and the observance-day
              suttas, and the chanting with Thai translation
    Volume 3  the least used: the Sekhiya rules, formal requests,
              ceremonies and procedures, and Ajarn Owen's chants
"""

VOLUMES = [
    {'number': 1, 'roman': 'One', 'name': 'Daily Chanting',
     'description': 'Morning and evening chanting, the protection chants and blessings used '
                    'most, the chants for each day of the week, and reflections'},
    {'number': 2, 'roman': 'Two', 'name': 'More Suttas',
     'description': 'The evening discourses, the chanting for the observance days, and '
                    'morning and evening chanting with Thai translation'},
    {'number': 3, 'roman': 'Three', 'name': 'Ceremonies and Other Chants',
     'description': 'The Sekhiya rules, formal requests, ceremonies and procedures, '
                    "and the chants from Ajarn Owen's chanting book"},
]

# Part number (as printed in the one-volume contents) -> volume.
PART_VOLUME = {
    1: 1,    # Morning Chanting
    2: 3,    # The 75 Training Rules (Sekhiya)
    3: 1,    # Morning Suttas and Verses
    4: 1,    # Suat Jaeng: the Canon in Summary
    5: 1,    # The Abhidhamma in Summary (the Mātikā, Jayamaṅgala, blessings)
    6: 1,    # Evening Chanting
    7: 1,    # Evening Suttas and Protection Chants (split, see SPLITS)
    8: 2,    # The Observance Day and its Eve
    9: 2,    # The Eighth Day of the Moon
    10: 2,   # The 14th Day of the Waxing Moon
    11: 2,   # The 7th Day of the Waning Moon
    12: 2,   # The 13th or 14th Day of the Waning Moon
    13: 2,   # Morning and Evening Chanting, with Thai Translation
    14: 3,   # Miscellaneous Chants and Formal Requests
    15: 3,   # Appendix: Ceremonies and Procedures
    16: 3,   # Other Chants
}
OWEN_VOLUME = 3        # Part 17, Ajarn Owen's chants and his word lists
AMARAVATI_VOLUME = 1   # Part 18, the Amaravati reflections

# Part 7 holds the twelve protection chants (book pages 77-102) and then the
# evening discourses (103-128). The protection chants are Volume 1; from the
# first evening discourse on, the rest of the Part is Volume 2.
SPLITS = {
    'bot-khat-dasanathakarana-dhamma-suttam': 2,
}

# Single chants moved out of their Part's volume. Empty in the draft.
CHANT_VOLUME = {}


# ── Chanting for each day of the week (กำลังวัน, the power of the day) ──
# The number of times is the traditional Thai one. Every chant is already in
# the temple book: each is the opening verse of one of the protection chants.
# Wednesday night follows the temple book itself, which pairs Rāhu (Wednesday
# night) with the Āṭānāṭiya paritta in its Navagraha procedure (book page 268).
# A guide Josh was given names the Suriya Paritta instead; that chant is not
# in the temple book, so it is noted, not printed.
DAY_CHANTS = [
    {'day': 'Sunday', 'thai': 'วันอาทิตย์', 'times': 6, 'chant': 'mora-parittam-pancamam',
     'first_line': 'Udetayañcakkhumā ekarājā', 'name': 'The Mora Paritta'},
    {'day': 'Monday', 'thai': 'วันจันทร์', 'times': 15, 'chant': 'abhaya-parittam-ekadasamam',
     'first_line': 'Yandunnimittaṃ avamaṅgalañca', 'name': 'The Abhaya Paritta'},
    {'day': 'Tuesday', 'thai': 'วันอังคาร', 'times': 8, 'chant': 'bot-khat-dhajagga-suttam',
     'first_line': 'Yassānussaraṇenāpi', 'name': 'The opening verse of the Dhajagga Sutta'},
    {'day': 'Wednesday (day)', 'thai': 'วันพุธกลางวัน', 'times': 17,
     'chant': 'bot-khat-khandha-chaddanta-parittam',
     'first_line': 'Sabbāsīvisajātīnaṃ', 'name': 'The opening verse of the Khandha Paritta'},
    {'day': 'Wednesday (night)', 'thai': 'วันพุธกลางคืน (ราหู)', 'times': 12,
     'chant': 'bot-khat-atanatiya-parittam',
     'first_line': 'Appasannehi nāthassa', 'name': 'The opening verse of the Āṭānāṭiya Paritta'},
    {'day': 'Thursday', 'thai': 'วันพฤหัสบดี', 'times': 19, 'chant': 'bot-khat-vattaka-parittam',
     'first_line': 'Pūrentambodhisambhāre nibbattaṃ vaṭṭajātiyaṃ',
     'name': 'The opening verse of the Vaṭṭaka Paritta'},
    {'day': 'Friday', 'thai': 'วันศุกร์', 'times': 21, 'chant': 'bot-khat-karaniyametta-suttam',
     'first_line': 'Yassānubhāvato yakkhā', 'name': 'The opening verse of the Karaṇīyametta Sutta'},
    {'day': 'Saturday', 'thai': 'วันเสาร์', 'times': 10, 'chant': 'angulimala-parittam-navamam',
     'first_line': 'Yatohaṃ bhagini ariyāya jātiyā jāto', 'name': 'The Aṅgulimāla Paritta'},
]

# A simple daily practice, in order. Each step points to a page of the book.
DAILY_ORDER = [
    ('Pay homage to the Triple Gem', ['kham-namatsakan-phra-ratanattaya']),
    ('Chant the Namo three times', ['pubbabhaga-namakara']),
    ('Chant the Itipi so as many times as the power of the day', ['phra-phuttakhun']),
    ('Chant the chant for your day of birth, if you wish', []),
    ('Chant loving-kindness for yourself and for all beings', ['amaravati-universal-well-being']),
    ('End with a moment of quiet meditation', []),
]


# ── Chants for occasions ──────────────────────────────────────────────────
# Where to find the chants for a birthday, a funeral, a meal and so on.
# `source` says where the advice comes from: the temple book's own pages of
# ceremony procedures (pages 249-276) wherever possible, otherwise the
# book's own notes on when a chant is chanted. Nothing is guessed: an
# occasion the book does not cover is not listed.
OCCASIONS = [
    {'group': 'Happy occasions', 'items': [
        {'occasion': 'A birthday',
         'note': 'The Dhammacakkappavattana Sutta, then the short Seven Tamnan, which opens '
                 'with the Maṅgala Sutta, the Highest Blessings.',
         # The Maṅgala Sutta is printed twice; Volume 1's copy (book page 81)
         # comes first, so a birthday needs only Volume 1 for it (Pra Kru Bob).
         'chants': ['mangala-suttam-pathamam', 'dhammacakkappavattana-suttam',
                    'rabiap-suat-chet-tamnan-yang-yo', 'mangala-suttam-chet-tamnan'],
         'source': 'temple book, page 256'},
        {'occasion': 'A new home, and other happy occasions',
         'note': 'The Seven Tamnan, in its full, middling or short form. The Passage for '
                 'Making a Protection is chanted over a new house.',
         'chants': ['rabiap-suat-mon-nai-ngan-phithi-mongkhon-uen',
                    'rabiap-suat-chet-tamnan-yang-tem-thi', 'parittakarana-patha'],
         'source': 'temple book, pages 20 and 258'},
        {'occasion': 'Long life and protection',
         'note': 'The Uṇhissavijaya verses, and the Lesser Universal Blessing.',
         'chants': ['unhissavijaya-gatha', 'mongkhon-chakkrawan-noi'],
         'source': 'temple book, pages 46, 237 and 271'},
        {'occasion': 'Lighting and putting out the victory candle',
         'note': 'At a happy ceremony with a victory candle.',
         'chants': ['gatha-jut-thian-chai', 'gatha-dap-thian-chai'],
         'source': 'temple book, page 254'},
        {'occasion': 'Chanting for the nine planets (Navagraha)',
         'note': 'Nine monks, one protection chant for each planet.',
         'chants': ['rabiap-suat-mon-noppakhro'],
         'source': 'temple book, page 268'},
    ]},
    {'group': 'Health', 'items': [
        {'occasion': 'Someone who is ill',
         'note': 'The Bojjhaṅga Paritta (the Factors of Awakening), the three Bojjhaṅga '
                 'discourses, and the Girimānanda Sutta.',
         'chants': ['bojjhanga-parittam-dasamam', 'mahakassapa-bojjhanga-suttam',
                    'girimananda-suttam'],
         'source': "the book's notes on these chants"},
    ]},
    {'group': 'Meals and offerings', 'items': [
        {'occasion': 'Before a meal: the blessing (thawai phon phra)',
         'note': 'Namo, Itipi so, the Jayamaṅgala verses (Bāhuṃ), the Jayaparitta '
                 '(Mahākāruṇiko), then Bhavatu sabbamaṅgalaṃ.',
         'chants': ['thawai-phon-phra', 'jayamangala-atthaka-gatha', 'jayaparitta-gatha'],
         'source': 'temple book, pages 264 and 270'},
        {'occasion': 'After a meal or an offering: the anumodanā',
         'note': 'Yathā vārivahā and Sabbītiyo, then Bhavatu sabbamaṅgalaṃ. At a happy '
                 'occasion verses such as the Kāladāna Sutta verses are added.',
         'chants': ['anumothana-withi', 'devatadissa-dakkhinanumodana', 'kaladana-sutta-gatha',
                    'viharadana-gatha'],
         'source': 'temple book, pages 271–272'},
        {'occasion': 'Sharing merit',
         'note': 'The verses for sharing merit, and the verses of dedication (Iminā '
                 'puññakammena).',
         'chants': ['pattidana-gatha', 'uddissanadhitthana-gatha'],
         'source': 'temple book, pages 7 and 62'},
    ]},
    {'group': 'Death and remembrance', 'items': [
        {'occasion': 'A funeral: the paṃsukūla',
         'note': 'The Mātikā, the Vipassanābhūmi passage and the Paṭṭhāna Mātikā, then the '
                 'paṃsukūla verse (Aniccā vata saṅkhārā).',
         'chants': ['thammasangkhani-matika-patho', 'wipassanaphumi-patho', 'phra-mahapatthan',
                    'kham-bangsukun-sop-rue-atthi'],
         'source': 'temple book, pages 252 and 274'},
        {'occasion': 'A funeral: Suat Jaeng',
         'note': 'The Vinaya, the Suttas and the seven books of the Abhidhamma in summary.',
         'chants': ['phra-winai-sangkhep', 'phra-sangkhani'],
         'source': "the book's notes on these chants"},
        {'occasion': 'Seven days after a death',
         'note': 'The Anattalakkhaṇa Sutta, opened with the Pabbatopama and Ariyadhana '
                 'verses and closed with Dependent Origination, the Buddha\'s Udāna and '
                 'the Bhaddekaratta verses.',
         'chants': ['anattalakkhana-suttam', 'pabbatopama-gatha', 'bhaddekaratta-gatha'],
         'source': 'temple book, page 264'},
        {'occasion': 'Fifty days after a death',
         'note': 'The Ādittapariyāya Sutta.',
         'chants': ['adittapariyaya-suttam'], 'source': 'temple book, page 264'},
        {'occasion': 'A hundred days after a death',
         'note': 'The Satipaṭṭhāna passage.',
         'chants': ['satipatthana-patho'], 'source': 'temple book, page 264'},
        {'occasion': 'Other seven-day observances, and anniversaries of a death',
         'note': 'Usually the Dhammaniyāma Sutta.',
         'chants': ['dhammaniyama-suttam'], 'source': 'temple book, page 264'},
        {'occasion': 'Dedicating merit to someone who has died',
         'note': 'The Tirokuḍḍa verses, chanted in the anumodanā while the water of '
                 'dedication is poured.',
         'chants': ['tirokuddakanda-pacchimaphak'], 'source': 'temple book, pages 271 and 273'},
    ]},
    {'group': 'Observance days and festivals', 'items': [
        {'occasion': 'An Uposatha day: taking the eight precepts',
         'note': 'The announcement, the request, the refuges and the precepts.',
         'chants': ['kham-prakat-ubosot', 'kham-aradhana-ubosot-sila', 'ubosot-sila'],
         'source': 'temple book, pages 10–13'},
        {'occasion': 'Visākha Pūjā', 'note': 'Offering flowers, incense and candles, and its verses.',
         'chants': ['kham-tawai-dokmai-thup-thian-visakha', 'sarabhanna-gatha-visakha'],
         'source': 'temple book, pages 66–67'},
        {'occasion': 'Aṭṭhamī Pūjā', 'note': 'Offering flowers, incense and candles, and its verses.',
         'chants': ['kham-tawai-dokmai-thup-thian-atthami', 'sarabhanna-gatha-atthami'],
         'source': 'temple book, pages 68–69'},
        {'occasion': 'Māgha Pūjā', 'note': 'Offering flowers, incense and candles, its verses, '
                                           'and the Ovāda Pāṭimokkha.',
         'chants': ['kham-tawai-dokmai-thup-thian-magha', 'sarabhanna-gatha-magha',
                    'ovada-patimokkhadi-patha'],
         'source': 'temple book, pages 71–72'},
        {'occasion': 'Āsāḷha Pūjā', 'note': 'Offering flowers, incense and candles.',
         'chants': ['kham-tawai-dokmai-thup-thian-asalha'], 'source': 'temple book, page 75'},
    ]},
    {'group': 'Requests and asking forgiveness', 'items': [
        {'occasion': 'Requesting the five or eight precepts',
         'note': 'The ordinary and the special forms.',
         'chants': ['kham-aradhana-sin-5-prokati', 'kham-aradhana-sin-8-prokati'],
         'source': 'temple book, page 249'},
        {'occasion': 'Requesting a Dhamma talk, or the protection chants',
         'note': '',
         'chants': ['kham-aradhana-sadaeng-tham', 'kham-aradhana-suat-phra-paritta'],
         'source': 'temple book, page 250'},
        {'occasion': 'Asking forgiveness of the Triple Gem or of an elder',
         'note': '',
         'chants': ['kham-kho-khama-thot-phra-ratanatrai', 'kham-kho-khama-thot-dae-phra-maha-thera'],
         'source': 'temple book, pages 252–253'},
    ]},
    {'group': 'For the monastery', 'items': [
        {'occasion': 'Going forth and ordination', 'note': 'Both forms of the procedure.',
         'chants': ['withi-banphacha-upasombot-baep-ukasa', 'withi-banphacha-upasombot-baep-esaham'],
         'source': 'temple book, pages 279–297'},
        {'occasion': 'Entering and leaving the Rains', 'note': '',
         'chants': ['kham-athitthan-khao-phansa', 'kham-pawarana-ok-phansa'],
         'source': 'temple book, page 303'},
        {'occasion': 'The Kathina', 'note': '',
         'chants': ['kham-apalok-kathin-baep-2-rup', 'baep-kammavaca-suat-hai-pha-kathin'],
         'source': 'temple book, pages 305–308'},
    ]},
]


def occasion_chant_ids():
    return [cid for g in OCCASIONS for item in g['items'] for cid in item['chants']]
