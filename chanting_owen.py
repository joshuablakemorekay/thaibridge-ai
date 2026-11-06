"""Chants from Ajarn Owen's chanting book, printed as a separate Part at the
end of the ThaiBridge chanting book (Josh, 2026-11-06).

Why a separate file: `chanting.py` is the Wat Mahathat United Kingdom
chanting book, transcribed page by page, and everything there is checked
against that book's photographs. These chants come from a DIFFERENT book, so
they live here, are printed in their own Part, and never mix with it. They
are not shown on the website.

What is here: romanised Pali and English exactly as Ajarn Owen prints them,
plus a Thai-script Pali line so the pages match the book's Pali-only chants
(Josh chose three layers, 2026-11-06). His book has no Thai script: for the
Sekhiya it is the temple book's, for the Confession a careful transliteration
of his Pali. Both need a monk's check. Transcribed from
Josh's photographs of the pages (book pages 30-35 and 263-264); still to be
proofread against the printed book.

Josh's wish (2026-11-06): include every chant of Ajarn Owen's book that the
temple book lacks, plus his Sekhiyavatta. Only the pages photographed so far
are entered; the others follow as photographs arrive.

Shape of a chant:
    id, title, title_english, source_pages
    intro: list of {'pali', 'english'} printed under the title
    sections: list of
        heading, note (optional), lines, closing (optional),
        after (optional): an instruction printed under the lines
    a line: {'n', 'role' (optional), 'pali' (Thai script), 'pali_roman', 'english'}
"""

OWEN_BOOK = "Ajarn Owen's chanting book"


def _rules(pali, english):
    """Pair numbered Pali rules with their numbered English, one to one."""
    assert len(pali) == len(english), (len(pali), len(english))
    return [{'n': i, 'pali_roman': p, 'english': e}
            for i, (p, e) in enumerate(zip(pali, english), start=1)]


_KARANIYA = ' sikkhā karaṇīyā.'

SEKHIYA = {
    'id': 'owen-sekhiyavatta',
    'title_thai': 'เสขิยวัตร',
    'title': 'Sekhiyavatta',
    'title_english': 'The 75 Rules of Training in Proper Conduct',
    'source_pages': '30–35',
    'intro': [{
        'pali': 'อิเม โข ปะนายัสมันโต (ปัญจะสัตตะติ) เสขิยา ธัมมา อุทเทสัง อาคัจฉันติ.',
        'pali_roman': 'Ime kho panāyasmanto (pañcasattati) sekhiyā dhammā uddesaṃ āgacchanti.',
        'english': 'Venerable sirs, these seventy-five training rules come up for recitation.',
    }],
    'sections': [
        {
            'heading': '1. Proper Conduct (Entering & Sitting in Inhabited Areas)',
            'note': 'These rules concern behaviour when entering villages, houses, or public places.',
            'lines': _rules([
                'Parimaṇḍalaṃ nivāsessāmīti' + _KARANIYA,
                'Parimaṇḍalaṃ pārupissāmīti' + _KARANIYA,
                'Suppaṭicchanno antaraghare gamissāmīti' + _KARANIYA,
                'Suppaṭicchanno antaraghare nisīdissāmīti' + _KARANIYA,
                'Susaṃvuto antaraghare gamissāmīti' + _KARANIYA,
                'Susaṃvuto antaraghare nisīdissāmīti' + _KARANIYA,
                'Okkhittacakkhu antaraghare gamissāmīti' + _KARANIYA,
                'Okkhittacakkhu antaraghare nisīdissāmīti' + _KARANIYA,
                'Na ukkhittakāyo antaraghare gamissāmīti' + _KARANIYA,
                'Na ukkhittakāyo antaraghare nisīdissāmīti' + _KARANIYA,
                'Na ujjagghikāya antaraghare gamissāmīti' + _KARANIYA,
                'Na ujjagghikāya antaraghare nisīdissāmīti' + _KARANIYA,
                'Appasaddo antaraghare gamissāmīti' + _KARANIYA,
                'Appasaddo antaraghare nisīdissāmīti' + _KARANIYA,
                'Na kāyappacālakaṃ antaraghare gamissāmīti' + _KARANIYA,
                'Na kāyappacālakaṃ antaraghare nisīdissāmīti' + _KARANIYA,
                'Na bāhoppacālakaṃ antaraghare gamissāmīti' + _KARANIYA,
                'Na bāhoppacālakaṃ antaraghare nisīdissāmīti' + _KARANIYA,
                'Na sīsappacālakaṃ antaraghare gamissāmīti' + _KARANIYA,
                'Na sīsappacālakaṃ antaraghare nisīdissāmīti' + _KARANIYA,
                'Na khambhakato antaraghare gamissāmīti' + _KARANIYA,
                'Na khambhakato antaraghare nisīdissāmīti' + _KARANIYA,
                'Na oguṇṭhito antaraghare gamissāmīti' + _KARANIYA,
                'Na oguṇṭhito antaraghare nisīdissāmīti' + _KARANIYA,
                'Na ukkuṭikāya antaraghare gamissāmīti' + _KARANIYA,
                'Na pallatthikāya antaraghare nisīdissāmīti' + _KARANIYA,
            ], [
                'I will wear the lower robe properly wrapped all around.',
                'I will wear the upper robe properly wrapped all around.',
                'I will enter inhabited areas properly covered.',
                'I will sit in inhabited areas properly covered.',
                'I will enter inhabited areas well-restrained.',
                'I will sit in inhabited areas well-restrained.',
                'I will enter inhabited areas with downcast eyes.',
                'I will sit in inhabited areas with downcast eyes.',
                'I will not enter inhabited areas holding my body arrogantly.',
                'I will not sit holding my body arrogantly.',
                'I will not enter while laughing loudly.',
                'I will not sit while laughing loudly.',
                'I will enter quietly.',
                'I will sit quietly.',
                'I will not enter swinging or swaying my body.',
                'I will not sit swinging or swaying my body.',
                'I will not enter swinging my arms.',
                'I will not sit swinging my arms.',
                'I will not enter shaking my head.',
                'I will not sit shaking my head.',
                'I will not enter with my arms akimbo (hands on hips).',
                'I will not sit with my arms akimbo.',
                'I will not enter with my head covered.',
                'I will not sit with my head covered.',
                'I will not enter squatting.',
                'I will not sit clasping my knees.',
            ]),
            'closing': {'pali': 'ฉัพพีสะติ สารุปปา.', 'pali_roman': 'Chabbīsati sāruppā.'},
        },
        {
            'heading': '2. Proper Conduct When Receiving and Eating Almsfood',
            'lines': _rules([
                'Sakkaccaṃ piṇḍapātaṃ paṭiggahessāmīti' + _KARANIYA,
                'Pattasaññī piṇḍapātaṃ paṭiggahessāmīti' + _KARANIYA,
                'Samasūpakaṃ piṇḍapātaṃ paṭiggahessāmīti' + _KARANIYA,
                'Samatittikaṃ piṇḍapātaṃ paṭiggahessāmīti' + _KARANIYA,
                'Sakkaccaṃ piṇḍapātaṃ bhuñjissāmīti' + _KARANIYA,
                'Pattasaññī piṇḍapātaṃ bhuñjissāmīti' + _KARANIYA,
                'Sapadānaṃ piṇḍapātaṃ bhuñjissāmīti' + _KARANIYA,
                'Samasūpakaṃ piṇḍapātaṃ bhuñjissāmīti' + _KARANIYA,
                'Na thūpato omadditvā piṇḍapātaṃ bhuñjissāmīti' + _KARANIYA,
                'Na sūpaṃ vā byañjanaṃ vā odanena paṭicchādessāmi bhiyyo kāmyataṃ upādāyāti' + _KARANIYA,
                'Na sūpaṃ vā odanaṃ vā agilāno attano atthāya viññāpetvā bhuñjissāmīti' + _KARANIYA,
                'Na ujjhānasaññī paresaṃ pattaṃ olokessāmīti' + _KARANIYA,
                'Nātimahantaṃ kabaḷaṃ karissāmīti' + _KARANIYA,
                'Parimaṇḍalaṃ ālopaṃ karissāmīti' + _KARANIYA,
                'Na anāhaṭe kabaḷe mukhadvāraṃ vivarissāmīti' + _KARANIYA,
                'Na bhuñjamāno sabbaṃ hatthaṃ mukhe pakkhipissāmīti' + _KARANIYA,
                'Na sakabaḷena mukhena byāharissāmīti' + _KARANIYA,
                'Na piṇḍukkhepakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na kabaḷāvacchedakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na avagaṇḍakārakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na hatthaniddhūnakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na sitthāvakārakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na jivhānicchārakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na capucapukārakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na surusurukārakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na hatthanillehakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na pattanillehakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na oṭṭhanillehakaṃ bhuñjissāmīti' + _KARANIYA,
                'Na sāmisena hatthena pānīyathālakaṃ paṭiggahessāmīti' + _KARANIYA,
                'Na sasitthakaṃ pattadhovanaṃ antaraghare chaḍḍessāmīti' + _KARANIYA,
            ], [
                'I will receive almsfood respectfully.',
                'I will receive almsfood with attention to the bowl.',
                'I will receive almsfood with an even amount of curry.',
                'I will receive almsfood in proper proportion to the bowl.',
                'I will eat almsfood respectfully.',
                'I will eat almsfood with attention to the bowl.',
                'I will eat almsfood going from house to house without favoritism.',
                'I will eat almsfood with an even amount of curry.',
                'I will not eat almsfood pressing down the heap from the top.',
                'I will not cover curry or rice in order to get more out of greed.',
                'Being not ill, I will not request curry or rice for my own sake and then eat it.',
                "I will not look at another's bowl with a critical attitude.",
                'I will not make an excessively large mouthful.',
                'I will make a round and proper morsel.',
                'I will not open my mouth before the morsel has reached it.',
                'While eating, I will not put my whole hand into my mouth.',
                'I will not speak with my mouth full.',
                'I will not toss lumps of food into my mouth.',
                'I will not bite off pieces from a mouthful.',
                'I will not eat stuffing my cheeks.',
                'I will not eat shaking my hand.',
                'I will not eat scattering grains of rice.',
                'I will not eat sticking out my tongue.',
                'I will not eat making “chomping” sounds.',
                'I will not eat making slurping sounds.',
                'I will not lick my hand while eating.',
                'I will not lick the bowl while eating.',
                'I will not lick my lips while eating.',
                'I will not accept a drinking vessel with a hand soiled by food.',
                'I will not throw away bowl-washing water with food scraps in an inhabited area.',
            ]),
            'closing': {'pali': 'สะมะติงสะ โภชะนะปะฏิสังยุตตา.', 'pali_roman': 'Samatiṃsa bhojanapaṭisaṃyuttā.'},
        },
        {
            'heading': '3. Proper Etiquette in Teaching the Dhamma',
            'lines': _rules([
                'Na chatta-pāṇissa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na daṇḍa-pāṇissa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na sattha-pāṇissa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na āvudha-pāṇissa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na pādukārūḷhassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na upāhanārūḷhassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na yānagatassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na sayanagatassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na pallatthikāya nisinnassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na veṭṭhitasīsassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na oguṇṭhitasīsassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na chamāyaṃ nisīditvā āsane nisinnassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na nīce āsane nisīditvā ucce āsane nisinnassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na ṭhito nisinnassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na pacchato gacchanto purato gacchantassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
                'Na uppathena gacchanto pathena gacchantassa agilānassa dhammaṃ desissāmīti' + _KARANIYA,
            ], [
                'I will not teach the Dhamma to a person who is not ill while he is holding an umbrella.',
                'I will not teach the Dhamma to a person who is not ill while he is holding a stick.',
                'I will not teach the Dhamma to a person who is not ill while he is holding a knife.',
                'I will not teach the Dhamma to a person who is not ill while he is holding a weapon.',
                'I will not teach the Dhamma to a person who is not ill while he is wearing wooden sandals.',
                'I will not teach the Dhamma to a person who is not ill while he is wearing shoes.',
                'I will not teach the Dhamma to a person who is not ill while he is riding in a vehicle.',
                'I will not teach the Dhamma to a person who is not ill while he is lying down.',
                'I will not teach the Dhamma to a person who is not ill while he is sitting clasping his knees.',
                'I will not teach the Dhamma to a person who is not ill while his head is wrapped (with a turban or cloth).',
                'I will not teach the Dhamma to a person who is not ill while his head is covered.',
                'I will not teach the Dhamma while sitting on the ground to a person who is not ill who is sitting on a seat.',
                'I will not teach the Dhamma while sitting on a low seat to a person who is not ill who is sitting on a high seat.',
                'I will not teach the Dhamma while standing to a person who is not ill who is sitting.',
                'I will not teach the Dhamma while walking behind a person who is not ill who is walking ahead.',
                'I will not teach the Dhamma while walking off the path to a person who is not ill who is walking on the path.',
            ]),
            'closing': {'pali': 'โสฬะสะ ธัมมะเทสะนาปะฏิสังยุตตา.', 'pali_roman': 'Soḷasa dhammadesanāpaṭisaṃyuttā.'},
        },
        {
            'heading': '4. Rules on Cleanliness and Decorum',
            'lines': _rules([
                'Na ṭhito agilāno uccāraṃ vā passāvaṃ vā karissāmīti' + _KARANIYA,
                'Na harite agilāno uccāraṃ vā passāvaṃ vā kheḷaṃ vā karissāmīti' + _KARANIYA,
                'Na udake agilāno uccāraṃ vā passāvaṃ vā kheḷaṃ vā karissāmīti' + _KARANIYA,
            ], [
                'I will not, being in good health, urinate or defecate while standing.',
                'I will not, being in good health, urinate, defecate, or spit on green grass.',
                'I will not, being in good health, urinate, defecate, or spit into water.',
            ]),
            'closing': {'pali': 'ตะโย ปะกิณณะกา.', 'pali_roman': 'Tayo pakiṇṇakā.'},
        },
    ],
}


def _dialogue(rows):
    """Lines of a dialogue: (number, role, pali, english)."""
    return [{'n': n, 'role': role, 'pali': th, 'pali_roman': p, 'english': e}
            for n, role, th, p, e in rows]


_J, _S = 'Junior Monk', 'Senior Monk'

APATTI_DESANA = {
    'id': 'owen-apatti-desana',
    'title_thai': 'คำแสดงอาบัติ',
    'title': 'Āpatti-desanā',
    'title_english': 'Procedure for Confession of Offences',
    'source_pages': '263–264',
    'intro': [],
    'sections': [
        {
            'heading': 'When the Junior Monk Confesses to the Senior',
            'lines': _dialogue([
                (1, _J, 'สัพพา ตา อาปัตติโย อาโรเจมิ.', 'Sabbā tā āpattiyo ārocemi. (3x)', 'I declare all those offences. (3x)'),
                (2, _J, 'สัพพา คะรุละหุกา อาปัตติโย อาโรเจมิ.', 'Sabbā garu-lahukā āpattiyo ārocemi. (3x)', 'I declare all offences, whether grave or minor. (3x)'),
                (3, _J, 'อะหัง ภันเต สัมพะหุลา นานาวัตถุกาโย อาปัตติโย อาปัชชิง, ตา ตุมหะมูเล ปะฏิเทเสมิ.', 'Ahaṃ, bhante, sambahulā nānāvatthukāyo āpattiyo āpajjiṃ; tā tumhamūle paṭidesemi.',
                 'Venerable Sir, having committed many offences of various kinds, I confess them before you.'),
                (4, _S, 'ปัสสะสิ อาวุโส ตา อาปัตติโย?', 'Passasi āvuso tā āpattiyo?', 'Do you see those offences?'),
                (5, _J, 'อุกาสะ, อามะ ภันเต, ปัสสามิ.', 'Ukāsa, āma bhante, passāmi.', 'Yes, Venerable Sir, I see them.'),
                (6, _S, 'อายะติง อาวุโส สังวะเรยยาสิ.', 'Āyatiṃ āvuso saṃvareyyāsi.', 'In the future, you should exercise restraint.'),
                (7, _J, 'สาธุ สุฏฐุ ภันเต สังวะริสสามิ.', 'Sādhu suṭṭhu bhante saṃvarissāmi.', 'Very well, Venerable Sir, I will restrain myself properly.'),
                (8, _J, 'ทุติยัมปิ สาธุ สุฏฐุ ภันเต สังวะริสสามิ.', 'Dutiyampi sādhu suṭṭhu bhante saṃvarissāmi.', 'For the second time, I will restrain myself properly.'),
                (9, _J, 'ตะติยัมปิ สาธุ สุฏฐุ ภันเต สังวะริสสามิ.', 'Tatiyampi sādhu suṭṭhu bhante saṃvarissāmi.', 'For the third time, I will restrain myself properly.'),
                (10, _J, 'นะ ปุเนวัง กะริสสามิ.', "Na pun'evaṃ karissāmi.", 'I will not act in this way again.'),
                (11, _J, 'นะ ปุเนวัง ภาสิสสามิ.', "Na pun'evaṃ bhāsissāmi.", 'I will not speak in this way again.'),
                (12, _J, 'นะ ปุเนวัง จินเตสสามิ.', "Na pun'evaṃ cintessāmi.", 'I will not think in this way again.'),
            ]),
        },
        {
            'heading': 'When the Senior Monk Confesses to the Junior',
            'lines': _dialogue([
                (1, _S, 'สัพพา ตา อาปัตติโย อาโรเจมิ.', 'Sabbā tā āpattiyo ārocemi. (3x)', 'I declare all those offences. (3x)'),
                (2, _S, 'สัพพา คะรุละหุกา อาปัตติโย อาโรเจมิ.', 'Sabbā garu-lahukā āpattiyo ārocemi. (3x)', 'I declare all grave and minor offences. (3x)'),
                (3, _S, 'อะหัง อาวุโส สัมพะหุลา นานาวัตถุกาโย อาปัตติโย อาปัชชิง, ตา ตุมหะมูเล ปะฏิเทเสมิ.', 'Ahaṃ, āvuso, sambahulā nānāvatthukāyo āpattiyo āpajjiṃ; tā tumhamūle paṭidesemi.',
                 'Friend, having committed many offences of various kinds, I confess them before you.'),
                (4, _J, 'อุกาสะ ภันเต, ปัสสะถะ ตา อาปัตติโย?', 'Ukāsa bhante, passatha tā āpattiyo?', 'Venerable Sir, do you see those offences?'),
                (5, _S, 'อามะ อาวุโส ปัสสามิ.', 'Āma āvuso passāmi.', 'Yes, friend, I see them.'),
                (6, _J, 'อายะติง ภันเต สังวะเรยยาถะ.', 'Āyatiṃ bhante saṃvareyyātha.', 'Venerable Sir, please exercise restraint in the future.'),
                (7, _S, 'สาธุ สุฏฐุ อาวุโส สังวะริสสามิ.', 'Sādhu suṭṭhu āvuso saṃvarissāmi.', 'I will restrain myself properly.'),
                (8, _S, 'ทุติยัมปิ สาธุ สุฏฐุ อาวุโส สังวะริสสามิ.', 'Dutiyampi sādhu suṭṭhu āvuso saṃvarissāmi.', 'For the second time, I will restrain myself properly.'),
                (9, _S, 'ตะติยัมปิ สาธุ สุฏฐุ อาวุโส สังวะริสสามิ.', 'Tatiyampi sādhu suṭṭhu āvuso saṃvarissāmi.', 'For the third time, I will restrain myself properly.'),
                (10, _S, 'นะ ปุเนวัง กะริสสามิ.', "Na pun'evaṃ karissāmi.", 'I will not act in this way again.'),
                (11, _S, 'นะ ปุเนวัง ภาสิสสามิ.', "Na pun'evaṃ bhāsissāmi.", 'I will not speak in this way again.'),
                (12, _S, 'นะ ปุเนวัง จินเตสสามิ.', "Na pun'evaṃ cintessāmi.", 'I will not think in this way again.'),
            ]),
            # Handwritten in the margin of Josh's copy of page 264; added at
            # his request (2026-11-06).
            'after': 'At the end, the Junior Monk bows down three times and says “Sādhu”.',
        },
    ],
}

# The Thai-script Pali of the 75 rules is the temple book's own (chanting.py,
# the four sekhiya chants), with five words changed to Ajarn Owen's spelling
# so that the Thai-script and romanised lines always agree. His spellings
# differ from the temple book's in 24 rules (desissāmīti for desessāmīti,
# suppaṭicchanno, ukkhittakāyo, bāhoppacālakaṃ, veṭṭhita): flagged for the
# reviewer, as some may be misprints in his book.
_OWEN_SPELLING = [
    ('สุปะฏิจฉันโน', 'สุปปะฏิจฉันโน'),
    ('อุกขิตตะกายะ', 'อุกขิตตะกาโย'),
    ('พาหุปปะจาละกัง', 'พาโหปปะจาละกัง'),
    ('เทเสสสามีติ', 'เทสิสสามีติ'),
    ('เวฐิตะ', 'เวฏฐิตะ'),
]
_TEMPLE_SEKHIYA = ('sekhiyavatta', 'sekhiya-bhojanapatisamyutta',
                   'sekhiya-dhammadesanapatisamyutta', 'sekhiya-pakinnaka')


def _add_temple_thai():
    import chanting
    for section, chant_id in zip(SEKHIYA['sections'], _TEMPLE_SEKHIYA):
        verses = chanting.get_chant(chant_id)['verses']
        assert len(verses) == len(section['lines']), chant_id
        for line, verse in zip(section['lines'], verses):
            thai = verse['pali']
            for old, new in _OWEN_SPELLING:
                thai = thai.replace(old, new)
            line['pali'] = thai


_add_temple_thai()

# ── The other chants, transcribed from the photographs in
# Downloads\Chanting Book Additional Pages (54 photos, 2026-11-06). Verse is
# given as rows "left half | right half", as Ajarn Owen sets it; the print
# layout splits them again. His English is a prose "English Meaning" under
# the verses, so it is kept as paragraphs, not paired line by line. The
# Thai-script Pali is added by thai_pali() further down.

def _rows(*rows):
    """Verse rows written 'left | right' -> lines of romanised Pali."""
    return [{'n': i, 'pali_roman': ' '.join(part.strip() for part in r.split('|'))}
            for i, r in enumerate(rows, start=1)]


MORE = []

MORE.append({
    'id': 'owen-arahants-eight-directions',
    'title_thai': '',
    'title': '',              # Ajarn Owen prints an English title only
    'title_english': 'Salutation to the Arahants of the Eight Directions',
    'source_pages': '20',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': _rows(
            'Sambuddho dipadaṃ seṭṭho | Nisinno ceva majjhime',
            'Koṇḍañño puppha-bhāge ca | Āgaṇeyye ca Kassapo',
            'Sāriputto ca dakkhiṇe | Haratiye Upālī ca',
            'Pacchimepi ca Ānando | payappe ca Gavampati',
            'Moggallāno ca uttare | Īsānepi ca Rāhulo',
            'Ime kho maṅgalā buddhā | Sabbe idha patiṭṭhitā',
            'Vanditā te ca amhehi | Sakkārehi ca pūjitā',
            'Etesaṃ ānubhāvena | Sabba-sotthī bhavantu no.',
            'Iccevamaccantanamassaneyyaṃ | Namassamāno ratanattayaṃ yaṃ',
            'Puññābhisandaṃ vipulaṃ alatthaṃ | Tassānubhāvena hatantarāyo.',
        ),
    }],
    'meaning': [
        'The Buddha, the Supreme Being among all bipeds, is seated in the very center. '
        'Venerable Kondañña is in the East, and Venerable Kassapa is in the Southeast. '
        'Venerable Sariputta is in the South, while Venerable Upali resides in the Southwest. '
        'Venerable Ananda is in the West, and Venerable Gavampati is in the Northwest. '
        'Venerable Moggallana is in the North, and Venerable Rahula is in the Northeast.',
        'All these auspicious and enlightened ones are firmly established here. They are '
        'revered and honored by us with our sincere offerings. By the power of all these '
        'Great Disciples, may we always be blessed with safety and prosperity.',
        'By paying such high homage to the Triple Gem, which is most worthy of reverence, '
        'I have gained a vast abundance of merit. By the power of that merit, may all '
        'dangers and obstacles be utterly destroyed.',
    ],
})

MORE.append({
    'id': 'owen-tayana-gatha',
    'title_thai': '',
    'title': 'Tāyanagāthā',
    'title_english': 'A Verse of Protection',
    'source_pages': '22',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': _rows(
            'Chinda sotaṃ parakkamma | Kāme panūda brāhmaṇa',
            'Nappahāya muni kāme | Nekattamūpapajjati',
            'Kayirā ce kayirāthenaṃ | Daḷhamenaṃ parakkame',
            'Sithilo hi paribbājo | Bhiyyo ākirate rajaṃ',
            'Akataṃ dukkataṃ seyyo | Pacchā tappati dukkataṃ',
            'Katañca sukataṃ seyyo | Yaṃ katvā nānutappati',
            'Kuso yathā duggahito | Hatthamivānukantati',
            'Sāmaññaṃ dupparāmatthaṃ | Nirayāyupakaḍḍhati',
            'Yaṃ kiñci sithilaṃ kammaṃ | Saṅkiliṭṭhañca yaṃ vataṃ',
            'Saṅkassaraṃ brahmacariyaṃ | Na taṃ hoti mahapphalanti.',
        ),
    }],
    'meaning': [
        'Strive and cut the stream of craving; discard sense-pleasures, O Brahmin. Without '
        'abandoning sense-pleasures, a silent sage does not attain onepointedness. If there is '
        'something to be done, do it; strive for it with firmness, for a slack ascetic life only '
        'scatters more dust of defilements. Better it is to leave a bad deed undone, as a bad deed '
        'causes suffering later; better it is to do a good deed, which, having been done, brings '
        'no regret. Just as Kusa grass, if grasped wrongly, cuts the hand, so the ascetic life, if '
        'practiced wrongly, drags one down to hell. Any action performed slackly, any vow that is '
        'corrupted, or a holy life led doubtfully-none of these yield great fruit.',
    ],
})

def _lines(*texts):
    """Single lines of romanised Pali, as printed (not verse halves)."""
    return [{'n': i, 'pali_roman': t} for i, t in enumerate(texts, start=1)]


MORE.append({
    'id': 'owen-great-vanda-footprints',
    'title_thai': '',
    'title': 'Great Vandā',
    'title_english': 'Homage to the Five Sacred Footprints of the Buddha',
    'source_pages': '54–55',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': _lines(
            'Vandāmi Buddhaṃ bhavapāratinṇaṃ',
            'Tilokaketuṃ Tibhavekanāthaṃ',
            'Yo lokaseṭṭho sakalaṅkilesaṃ chetvāna',
            'Bodhesi janaṃ anantaṃ',
            'Yaṃ nammadāya nadiya puline ca tīre',
            'Yaṃ saccabandhagirike sumenā calagge',
            'Yaṃ tattha yonakapure munidun',
            'Ca pādaṃ taṃ padalañchanamahaṃ sirasā namāmi',
            'Suvaṇṇamālike Suvaṇṇapabbate',
            'Sumanakūṭe yonakapure nammadāya nadiya',
            'Pañcapādavaraṃ ṭhānaṃ ahaṃ vandāmi dūrato.',
            'Icceva maccanta Namassaneyya',
            'namassamāno ratanattayaṃ Yaṃ',
            'puññābhisandaṃ vipulaṃ alatthaṃ',
            'tassānubhāvena Hatantarāyo.',
            'Āmantayāmi vo bhikkhave paṭivedayāmi vo bhikkhave',
            'Khayavayadhammā saṅkhārā appamādena sampādethāti.',
        ),
        'meaning': [
            'I pay homage to the Buddha, who has crossed beyond the ocean of existence; the banner '
            'of the three worlds, the one supreme refuge of the three realms.',
            'He who is the highest in the world, having cut off all defilements, awakened countless '
            'beings and led them to enlightenment.',
            'I bow with my head to the sacred footprints that the Blessed One revealed upon the sandy '
            'banks of the River Nammadā; upon Mount Saccabandha; upon the summit of Mount Sumana; and '
            'within the city of Yonaka. At Suvaṇṇamālika Mountain, at Suvaṇṇapabbata Mountain, at '
            'Sumanakūṭa Mountain, in Yonaka City, and at the River Nammadā - these five sacred places '
            'of the noble footprints I revere from afar.',
            'Thus paying homage to the Triple Gem, which is worthy of the highest veneration, I obtain '
            'a vast and abundant stream of merit. By the power of that merit, may all dangers be '
            'destroyed.',
            '“Monks, I address you. Monks, I declare to you: All conditioned things are subject to '
            'decay. Strive diligently and accomplish your goal with heedfulness.”',
        ],
    }, {
        'heading': '“Verse on The Dhamma that makes one a deva”',
        'lines': _rows(
            'Hiriottappasampannā | sukkadhammā samāhitā',
            'santo sappurisā loke | devadhammāti vuccare',
        ),
        'meaning': [
            'Those who are endowed with moral shame (hiri) and moral fear (ottappa), who are '
            'established in pure (wholesome) qualities, who are peaceful and truly virtuous persons '
            'in this world - they are called “those who possess the qualities of the devas” (divine '
            'qualities).',
        ],
    }],
})

# Ajarn Owen prints the niggahīta both as ṃ and ṁ (from page to page); it is
# the same letter, so ṁ is written ṃ here throughout.
MORE.append({
    'id': 'owen-pathamabuddhavacana',
    'title_thai': '',
    'title': 'Pathamabuddhavacana',
    'title_english': 'The First Words of the Buddha',
    'source_pages': '73',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': _rows(
            'Anekajātisaṃsāraṃ | sandhāvissaṃ anibbisaṃ,',
            'gahakāraṃ gavesanto | dukkhā jāti punappunaṃ.',
            'Gahakāraka diṭṭhosi, | puna gehaṃ na kāhasi;',
            'sabbā te phāsukā bhaggā, | gahakūṭaṃ visaṅkhataṃ.',
            'Visaṅkhāragataṃ cittaṃ, | taṇhānaṃ khayamajjhagāti.',
        ),
    }],
    'meaning': [
        'Through many births in this cycle, I wandered without finding rest, seeking the builder '
        'of this house; to be born again and again is painful. Oh, House-builder! You are seen at '
        'last; you shall build this house no more. All your rafters are broken and the ridge-pole '
        'is shattered. My mind has reached the Unconditioned and attained the end of all craving.',
    ],
})

def _rows_en(*pairs):
    """Verse rows ('left | right', english) where the English is line by line."""
    return [dict(line, english=e) for line, (_, e) in zip(_rows(*[p for p, _ in pairs]), pairs)]


MORE.append({
    'id': 'owen-keniya-anumodana',
    'title_thai': '',
    'title': 'Keniya Anumodanā Gāthā',
    'title_english': "Verses of Rejoicing in Keniya's Offering",
    'source_pages': '133',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': _rows_en(
            ('Aggihuttamukhā yaññā | Sāvittī chandaso mukhaṃ',
             'Sacrificial offerings have fire as their chief; Among poetic metres, the Sāvittī is foremost.'),
            ('Rājā mukham manussānaṃ | Nadīnaṃ sāgaro mukhaṃ',
             'Among human beings, the king is foremost; Among rivers, the ocean is foremost.'),
            ('Nakkhattānaṃ mukhaṃ cando | Ādicco tappataṃ mukhaṃ',
             'Among the stars, the moon is foremost; Among shining lights, the sun is foremost.'),
            ('Puññamānaṃ mukham dānaṃ | Saṅgho ve yajataṃ mukhaṃ',
             'For those who aspire to merit, The Saṅgha is truly the foremost field of offering.'),
            ('Bhaṇissāma mayaṃ gāthā | Kāladānappadīpika',
             'We shall now recite verses, Which are a lamp illuminating timely giving.'),
            ('Etā sunantu sakkaccaṃ | Dāyakā puññakāmino',
             'May the donors who desire merit Listen to these attentively and with respect.'),
        ),
    }],
})

MORE.append({
    'id': 'owen-bhojanadana-anumodana',
    'title_thai': '',
    'title': 'Bhojanadāna Anumodanā Gāthā',
    'title_english': 'Verses of Rejoicing in the Offering of Food',
    'source_pages': '135',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': _rows(
            'Āyudo balado dhīro | vaṇṇado paṭibhāṇado',
            'Sukhassa dātā medhāvī | sukhaṃ so adhigacchati',
            'Āyuṃ datvā balaṃ vaṇṇaṃ | sukhañca paṭibhāṇado',
            'Dīghāyu yasavā hoti | yattha yatthūpapajjatīti.',
        ),
    }],
    'meaning': [
        'The wise person who gives life, gives strength; who gives beauty and gives intelligence; '
        'the wise giver of happiness gains happiness in return. Having given life, strength, '
        'beauty, happiness, and intelligence, one becomes long-lived and renowned wherever one is '
        'reborn',
    ],
})

# The Dasapāramī repeats one formula for each perfection; it is generated from
# that formula so that all ten read identically, as they do on the page.
_PARAMI = [  # (Pali name, English heading, English name in the formula)
    ('Dāna', 'Perfection of Generosity', 'Giving'),
    ('Sīla', 'Perfection of Morality', 'Moral Conduct'),
    ('Nekkhamma', 'Perfection of Renunciation', 'Renunciation'),
    ('Paññā', 'Perfection of Wisdom', 'Wisdom'),
    ('Viriya', 'Perfection of Energy / Effort', 'Energy'),
    ('Khanti', 'Perfection of Patience', 'Patience'),
    ('Sacca', 'Perfection of Truthfulness', 'Truth'),
    ('Adhiṭṭhāna', 'Perfection of Determination', 'Determination'),
    ('Mettā', 'Perfection of Loving-Kindness', 'Loving-Kindness'),
    ('Upekkhā', 'Perfection of Equanimity', 'Equanimity'),
]
_BRAHMAVIHARA_PI = 'Mettā maitrī karuṇā muditā upekkhā pāramī sampanno, Iti pi so Bhagavā.'
_BRAHMAVIHARA_EN = ('He is accomplished in loving-kindness, goodwill, compassion, sympathetic '
                    'joy, and equanimity. Thus indeed is the Blessed One.')


def _parami_lines():
    lines = []
    for i, (name, heading, en) in enumerate(_PARAMI, start=1):
        lines.append({
            'n': i,
            'label': '%s Pāramī (%s)' % (name, heading),
            'pali_roman': '%s Pāramī %s-pāramī sampanno, %s-upapāramī sampanno, '
                          '%s-paramatthapāramī sampanno, %s' % (name, name, name, name, _BRAHMAVIHARA_PI),
            'english': 'The Blessed One is accomplished in the Perfection of %s, accomplished in '
                       'the Higher Perfection of %s, accomplished in the Ultimate Perfection of %s. %s'
                       % (en, en, en, _BRAHMAVIHARA_EN),
        })
    lines.append({
        'n': 11,
        'label': 'Summary Verse',
        'pali_roman': 'Dasa-pāramī sampanno, Dasa-upapāramī sampanno, Dasa-paramatthapāramī '
                      'sampanno, ' + _BRAHMAVIHARA_PI,
        'english': 'The Blessed One is accomplished in the Ten Perfections, accomplished in the '
                   'Ten Higher Perfections, accomplished in the Ten Ultimate Perfections. '
                   + _BRAHMAVIHARA_EN,
    })
    return lines


MORE.append({
    'id': 'owen-dasaparami',
    'title_thai': '',
    'title': 'Dasapāramī',
    'title_english': 'Ten Perfections – Ancient Chanting Style',
    'source_pages': '205–207',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': _parami_lines(),
        'closing': {'pali_roman': 'Buddhaṃ saraṇaṃ gacchāmi, namāmihaṃ.'},
    }],
})

# Siṅgālaka Sutta: assembled from scratchpad/singalaka_part1.txt (photos p221–230).
MORE.append({
    "id": "owen-singalaka-sutta",
    "title_thai": "",
    "title": "Siṅgālaka Sutta (Short Version)",
    "title_english": "The teaching of the Buddha given to Sigālaka, the householder's son",
    "source_pages": "221–230",
    "intro": [],
    "introduction": [
        "At one time the Blessed One was dwelling at Rājagaha, in the Bamboo Grove, the Squirrels' Feeding Ground. At that time, Sigālaka, a young householder, rose early in the morning and went out from the city of Rājagaha. With wet clothes and wet hair, and with hands joined in reverence, he worshipped the six directions: the east, the south, the west, the north, the lower direction, and the upper direction.",
        "Seeing this, the Blessed One approached and questioned him about his practice. Sigālaka explained that he was following his father's final instruction to honor the directions. The Buddha then taught that, in the Noble Discipline, the true honoring of the six directions does not consist in ritual gestures, but in fulfilling one's duties and responsibilities in human relationships.",
        "In this discourse, the Buddha reinterprets the six directions as symbolic of key relationships in life-parents, teachers, family, friends, workers, and spiritual practitioners (Buddhist monks)-and teaches a comprehensive ethical guide for laypeople. The Siṅgālaka Sutta is therefore regarded as one of the most important teachings on social harmony, moral responsibility, and daily conduct in Buddhism."
    ],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Evaṃ me sutaṃ. Ekaṃ samayaṃ Bhagavā Rājagahe viharati Veḷuvane Kalandakanivāpe. Tena kho pana samayena Siṅgālako gahapatiputto kālasseva vuṭṭhāya Rājagahā nikkhamitvā allavattho allakeso pañjaliko puthuddisā namassati puratthimaṃ disaṃ dakkhiṇaṃ disaṃ pacchimaṃ disaṃ uttaraṃ disaṃ heṭṭhimaṃ disaṃ uparimaṃ disaṃ.",
                    "english": "Thus have I heard. At one time the Blessed One was dwelling at Rājagaha, in the Bamboo Grove, at the Squirrels' Feeding Ground. At that time, Sigālaka, a householder's son, having risen early in the morning, left Rājagaha with wet clothes and wet hair, and with hands joined in reverence, was worshipping the various directions: the eastern direction, the southern direction, the western direction, the northern direction, the lower direction, and the upper direction."
                },
                {
                    "n": 2,
                    "pali_roman": "Atha kho Bhagavā pubbaṇhasamayaṃ nivāsetvā pattacīvaramādāya Rājagahaṃ piṇḍāya pāvisi. Addasā kho Bhagavā Siṅgālakaṃ gahapatiputtaṃ kālasseva vuṭṭhāya Rājagahā nikkhamitvā allavatthaṃ allakesaṃ pañjalikaṃ puthuddisā namassantaṃ puratthimaṃ disaṃ dakkhiṇaṃ disaṃ pacchimaṃ disaṃ uttaraṃ disaṃ heṭṭhimaṃ disaṃ uparimaṃ disaṃ. Disvāna Siṅgālakaṃ gahapatiputtaṃ etadavoca: “Kinnu tvaṃ gahapatiputta kālasseva vuṭṭhāya Rājagahā nikkhamitvā allavattho allakeso pañjaliko puthuddisā namassasi puratthimaṃ disaṃ dakkhiṇaṃ disaṃ pacchimaṃ disaṃ uttaraṃ disaṃ heṭṭhimaṃ disaṃ uparimaṃ disaṃ”ti",
                    "english": "Then, in the morning, the Blessed One dressed and, taking his bowl and robe, entered Rājagaha for alms. The Blessed One saw Sigālaka, the householder's son, who had risen early in the morning and left Rājagaha with wet clothes and wet hair, with hands joined in reverence, worshipping the various directions: the eastern, southern, western, northern, lower, and upper directions. Seeing him, the Blessed One said: “Why is it, householder's son, that you, having risen early in the morning, have left Rājagaha with wet clothes and wet hair, and with hands joined in reverence worship the various directions: the eastern direction, the southern direction, the western direction, the northern direction, the lower direction, and the upper direction?”"
                },
                {
                    "n": 3,
                    "pali_roman": "“Pitā maṃ, bhante, kālaṃ karonto evaṃ avoca: ‘Disā tāta namasseyyāsī’ti. So kho ahaṃ, bhante, pitu vacanaṃ sakkaronto garukaronto mānento pūjento kālasseva vuṭṭhāya Rājagahā nikkhamitvā allavattho allakeso pañjaliko puthuddisā namassāmi puratthimaṃ disaṃ dakkhiṇaṃ disaṃ pacchimaṃ disaṃ uttaraṃ disaṃ heṭṭhimaṃ disaṃ uparimaṃ disaṃ”ti.",
                    "english": "He replied: “Venerable Sir, when my father was dying, he said to me: ‘Dear son, you should worship the directions.’ Therefore, venerable sir, honoring, respecting, valuing, and revering my father's words, I rise early in the morning, leave Rājagaha with wet clothes and wet hair, and with hands joined in reverence worship the various directions: the eastern direction, the southern direction, the western direction, the northern direction, the lower direction, and the upper direction.”"
                },
                {
                    "n": 4,
                    "pali_roman": "“Na kho, gahapatiputta, ariyassa vinaye evaṃ cha disā namassitabbā”ti.",
                    "english": "The Blessed One said: “Householder's son, in the discipline of the Noble Ones, the six directions are not to be worshipped in this way.”"
                },
                {
                    "n": 5,
                    "pali_roman": "“Yathākathaṃ pana, bhante, ariyassa vinaye cha disā namassitabbā? Sādhu me, bhante, Bhagavā tathā dhammaṃ desetu yathā ariyassa vinaye cha disā namassitabbā”ti.",
                    "english": "“Then how, venerable sir, should the six directions be worshipped in the discipline of the Noble Ones? It would be good if the Blessed One would teach me the Dhamma in such a way that, in the discipline of the Noble Ones, the six directions are to be properly worshipped.”"
                },
                {
                    "n": 6,
                    "pali_roman": "“Tena hi, gahapatiputta, suṇāhi sādhukaṃ manasikarohi, bhāsissāmī”ti. “Evaṃ, bhante”ti kho Siṅgālako gahapatiputto Bhagavato paccassosi. Bhagavā etadavoca.",
                    "english": "“Then, householder's son, listen carefully and attend closely; I shall speak.” “Yes, venerable sir,” Sigālaka, the householder's son, replied to the Blessed One. Then the Blessed One said this."
                }
            ]
        },
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Upakāro ca yo mitto, sukhadukkho ca yo sakhā"
                },
                {
                    "n": 2,
                    "pali_roman": "Atthakkhāyī ca yo mitto, yo ca mittānukampako."
                },
                {
                    "n": 3,
                    "pali_roman": "Etepi mitte cattāro, iti viññāya paṇḍito"
                },
                {
                    "n": 4,
                    "pali_roman": "Sakkaccaṃ payirupāseyya, mātā puttaṃva orasaṃ."
                },
                {
                    "n": 5,
                    "pali_roman": "Paṇḍito sīlasampanno, jalaṃ aggīva bhāsati"
                },
                {
                    "n": 6,
                    "pali_roman": "Bhoge saṃharamānassa, bhamarasseva iriyato."
                },
                {
                    "n": 7,
                    "pali_roman": "Bhogā sannicayaṃ yanti, vammikovūpacīyati"
                },
                {
                    "n": 8,
                    "pali_roman": "Evaṃ bhoge samāharitvā, alamatto kule gihī."
                },
                {
                    "n": 9,
                    "pali_roman": "Catudhā vibhaje bhoge, sa ve mittāni ganthati"
                },
                {
                    "n": 10,
                    "pali_roman": "Ekena bhoge bhuñjeyya, dvīhi kammaṃ payojaye"
                },
                {
                    "n": 11,
                    "pali_roman": "Catutthaṃ ca nidhāpeyya, āpadāsu bhavissatīti."
                }
            ],
            "meaning": [
                "The friend who is helpful, the companion who is the same in happiness and suffering, the friend who points out what is beneficial, and the one who has compassion for friends.",
                "These four are friends. Having understood this, the wise person should carefully associate with them, as a mother with her own dear child.",
                "The wise one, endowed with virtue, shines like a blazing fire; for one who gathers wealth, it grows like a bee gathering honey.",
                "Wealth accumulates, like an anthill gradually rising. Having gathered wealth in this way, a householder supports his family sufficiently.",
                "He should divide his wealth into four parts: thus he binds his friends to him. One portion he should enjoy, two he should invest in work and business, and the fourth he should set aside, for it will be useful in times of trouble and dangers."
            ]
        },
        {
            "heading": "",
            "lines": [
                {
                    "n": 7,
                    "pali_roman": "Kathaṃ ca gahapatiputta ariyasāvako chadisāpaṭicchādī hoti",
                    "english": "And how, householder's son, does a noble disciple respect the six directions?"
                },
                {
                    "n": 8,
                    "pali_roman": "Cha imā gahapatiputta disā veditabbā: puratthimā disā mātāpitaro veditabbā, dakkhiṇā disā ācariyā veditabbā, pacchimā disā puttadārā veditabbā, uttarā disā mittāmaccā veditabbā, heṭṭhimā disā dāsakammakarā veditabbā, uparimā disā samaṇabrāhmaṇā veditabbā.",
                    "english": "These six directions, householder's son, should be understood thus: the eastern direction as parents, the southern direction as teachers, the western direction as wife and children, the northern direction as friends and associates, the lower direction as servants and workers, the upper direction as ascetics and brahmins."
                },
                {
                    "n": 9,
                    "pali_roman": "Pañcahi kho gahapatiputta ṭhānehi puttena puratthimā disā mātāpitaro paccupaṭṭhātabbā: bhato nesaṃ bharissāmi, kiccaṃ nesaṃ karissāmi, kulavaṃsaṃ ṭhapessāmi, dāyajjaṃ paṭipajjāmi, athavā pana petānaṃ kālakataṃ dakkhiṇaṃ anuppadassāmīti.",
                    "english": "Householder's son, parents, as the eastern direction, should be supported by their children in five ways: by reflecting, “They have cared for me; I will care for them in return”; by performing their duties; by maintaining the family lineage; by conducting oneself so as to be worthy of receiving the inheritance; and when they have passed away, by making offerings on their behalf."
                },
                {
                    "n": 10,
                    "pali_roman": "Imehi kho gahapatiputta pañcahi ṭhānehi puttena puratthimā disā mātāpitaro paccupaṭṭhitā, pañcahi ṭhānehi puttaṃ anukampanti: pāpā nivārenti, kalyāṇe nivesenti, sippaṃ sikkhāpenti, paṭirūpena dārena saṃyojenti, samaye dāyajjaṃ niyyādenti. Evaṃ assa esā puratthimā disā paṭicchannā hoti khemā appaṭibhayā.",
                    "english": "Householder's son, when parents, as the eastern direction, are supported by their children in these five ways, they in turn show compassion to their children in five ways: they restrain them from evil; they establish them in good; they provide them with education and skills; they arrange a suitable spouse for them; and they hand over their inheritance at the proper time. Householder's son, when parents, as the eastern direction, are supported by their children in these five ways, and they show compassion in these five ways, that eastern direction is thus covered, made secure, and free from danger."
                },
                {
                    "n": 11,
                    "pali_roman": "Pañcahi kho gahapatiputta ṭhānehi antevāsīhi dakkhiṇā disā ācariyā paccupaṭṭhātabbā: uṭṭhānena, upaṭṭhānena, sussūsāya, pāricariyāya, sakkaccaṃ sippaṃ paṭiggahaṇena.",
                    "english": "Householder's son, teachers, as the southern direction, should be supported by their pupils in five ways: by rising to greet them; by attending on them; by obedience; by service; and by learning the arts and sciences respectfully."
                },
                {
                    "n": 12,
                    "pali_roman": "Imehi kho gahapatiputta pañcahi ṭhānehi antevāsīhi dakkhiṇā disā ācariyā paccupaṭṭhitā, pañcahi ṭhānehi antevāsino anukampanti: suvinītaṃ vinenti, sugahitaṃ gāhāpenti, sabbasippesu samakkhāyino honti, mittāmaccāsu paṭivedenti, disāsu parittāṇaṃ karonti. Evaṃ assa esā dakkhiṇā disā paṭicchannā hoti khemā appaṭibhayā.",
                    "english": "Householder's son, when teachers, as the southern direction, are supported by their pupils in these five ways, they in turn show compassion to their pupils in five ways: they train them well; they ensure they learn well; they instruct them thoroughly in all arts and sciences; they recommend them among their friends; and they provide protection in all directions. Householder's son, when teachers, as the southern direction, are supported by their pupils in these five ways, and they show compassion in these five ways, that southern direction is thus covered, made secure, and free from danger."
                },
                {
                    "n": 13,
                    "pali_roman": "Pañcahi kho gahapatiputta ṭhānehi sāmikena pacchimā disā bhariyā paccupaṭṭhātabbā: sammānana, avimānana, anaticariyā, issariyavossaggena, alaṅkārānuppadānena.",
                    "english": "Householder's son, a wife, as the western direction, should be supported by her husband in five ways: by honoring her as his wife; by not despising her; by not being unfaithful; by giving her authority; and by providing her with adornments."
                },
                {
                    "n": 14,
                    "pali_roman": "Imehi kho gahapatiputta pañcahi ṭhānehi sāmikena pacchimā disā bhariyā paccupaṭṭhitā, pañcahi ṭhānehi sāmikaṃ anukampati: susaṃvihitakammantā ca hoti, susaṅgahitaparijanā hoti, anaticārinī hoti, sambhataṃ anurakkhati, dakkhā hoti analasā sabbakiccesu. Evaṃ assa esā pacchimā disā paṭicchannā hoti khemā appaṭibhayā.",
                    "english": "Householder's son, when a wife, as the western direction, is supported by her husband in these five ways, she in turn shows compassion to her husband in five ways: she manages the household duties well; she treats the relatives and attendants kindly; she is faithful; she safeguards the wealth he has earned; and she is diligent and not lazy in all her duties. Householder's son, when a wife, as the western direction, is supported by her husband in these five ways, and she shows compassion in these five ways, that western direction is thus covered, made secure, and free from danger."
                },
                {
                    "n": 15,
                    "pali_roman": "Pañcahi kho gahapatiputta ṭhānehi kulaputtena uttarā disā mittāmaccā paccupaṭṭhātabbā: dānena, piyavācena, atthacariyāya, samānattatāya, avisaṃvādanatāya.",
                    "english": "Householder's son, friends, as the northern direction, should be supported by a noble person in five ways: by generosity; by kind speech; by beneficial conduct; by treating them as oneself; and by sincerity."
                },
                {
                    "n": 16,
                    "pali_roman": "Imehi kho gahapatiputta pañcahi ṭhānehi kulaputtena uttarā disā mittāmaccā paccupaṭṭhitā, pañcahi ṭhānehi kulaputtaṃ anukampanti: pamattaṃ rakkhanti, pamattassa sāpateyyaṃ rakkhanti, bhītassa saraṇaṃ honti, āpadāsu na vijahanti, aparapajāpi tassa paṭipūjenti. Evaṃ assa esā uttarā disā paṭicchannā hoti khemā appaṭibhayā.",
                    "english": "Householder's son, when friends, as the northern direction, are supported in these five ways, they in turn show compassion in five ways: they protect their friend when he is heedless; they protect his property when he is heedless; they are a refuge when he is afraid; they do not abandon him in times of trouble; and they show respect to his family. Householder's son, when friends, as the northern direction, are supported in these five ways, and they show compassion in these five ways, that northern direction is thus covered, made secure, and free from danger."
                },
                {
                    "n": 17,
                    "pali_roman": "Pañcahi kho gahapatiputta ṭhānehi ayirakena heṭṭhimā disā dāsakammakarā paccupaṭṭhātabbā: yathābalaṃ kammantaṃ saṃvidhānena, bhattavettanānuppadānena, gilānupaṭṭhānena, acchariyānaṃ rasānaṃ saṃvibhāgena, samaye vossaggena.",
                    "english": "Householder's son, servants and workers, as the lower direction, should be supported by their master in five ways: by assigning work according to their ability; by providing food and wages; by caring for them when they are ill; by sharing special delicacies with them; and by granting them leave at proper times."
                },
                {
                    "n": 18,
                    "pali_roman": "Imehi kho gahapatiputta pañcahi ṭhānehi ayirakena heṭṭhimā disā dāsakammakarā paccupaṭṭhitā, pañcahi ṭhānehi ayirakaṃ anukampanti: pubbuṭṭhāyino honti, pacchānipātino honti, dinnādāyino honti, sukatakammakarā honti, kittivaṇṇaharā honti. Evaṃ assa esā heṭṭhimā disā paṭicchannā hoti khemā appaṭibhayā.",
                    "english": "Householder's son, when servants and workers, as the lower direction, are supported by their master in these five ways, they in turn show compassion to their master in five ways: they rise before him; they go to rest after him; they take only what is given; they perform their duties well; and they spread his good reputation. Householder's son, when servants and workers, as the lower direction, are supported by their master in these five ways, and they show compassion in these five ways, that lower direction is thus covered, made secure, and free from danger."
                },
                {
                    "n": 19,
                    "pali_roman": "Pañcahi kho gahapatiputta ṭhānehi kulaputtena uparimā disā samaṇabrāhmaṇā paccupaṭṭhātabbā: mettena kāyakammena, mettena vacīkammena, mettena manokammena, anāvaṭadvāratāya, āmisānuppadānena.",
                    "english": "Householder's son, ascetics and brahmins, as the upper direction, should be supported by a noble person in five ways: by bodily acts of loving-kindness; by verbal acts of loving-kindness; by mental acts of loving-kindness; by keeping an open house; and by regularly giving material offerings."
                },
                {
                    "n": 20,
                    "pali_roman": "Imehi kho gahapatiputta pañcahi ṭhānehi kulaputtena uparimā disā samaṇabrāhmaṇā paccupaṭṭhitā, chahi ṭhānehi kulaputtaṃ anukampanti: pāpā nivārenti, kalyāṇe nivesenti, kalyāṇena manasā anukampanti, assutaṃ sāventi, sutaṃ pariyodapenti, saggassa maggaṃ ācikkhanti. Evaṃ assa esā uparimā disā paṭicchannā hoti khemā appaṭibhayā.",
                    "english": "Householder's son, when ascetics and brahmins, as the upper direction, are supported in these five ways, they in turn show compassion in six ways: they restrain from evil; they encourage in good; they show compassion with a kind heart; they teach what has not been heard; they clarify what has been heard; and they show the path to heaven. Householder's son, when ascetics and brahmins, as the upper direction, are supported in these five ways, and they show compassion in these six ways, that upper direction is thus covered, made secure, and free from danger."
                },
                {
                    "n": 21,
                    "pali_roman": "Idam avoca Bhagavā, idaṃ vatvāna Sugato athāparaṃ etadavoca Satthā:",
                    "english": "Thus spoke the Blessed One; having said this, the Well-Gone One, the Teacher, further said:"
                }
            ]
        },
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Mātāpitaro disā pubbā, ācariyā dakkhiṇā disā"
                },
                {
                    "n": 2,
                    "pali_roman": "Puttadārā disā pacchā, mittāmaccā ca uttarā"
                },
                {
                    "n": 3,
                    "pali_roman": "Dāsakammakarā heṭṭhā, uddhaṃ samaṇabrāhmaṇā"
                },
                {
                    "n": 4,
                    "pali_roman": "Etā disā namasseyya, alamatto kule gihī."
                },
                {
                    "n": 5,
                    "pali_roman": "Paṇḍito sīlasampanno, saṇho ca paṭibhānavā"
                },
                {
                    "n": 6,
                    "pali_roman": "Nivātavutti atthaddho, tādiso labhate yasaṃ."
                },
                {
                    "n": 7,
                    "pali_roman": "Uṭṭhānako analaso, āpadāsu na vedhati"
                },
                {
                    "n": 8,
                    "pali_roman": "Acchinnavutti medhāvī, tādiso labhate yasaṃ."
                },
                {
                    "n": 9,
                    "pali_roman": "Saṅgahako mittakaro, vadaññū vītamaccharo"
                },
                {
                    "n": 10,
                    "pali_roman": "Netā vinayitā anunetā, tādiso labhate yasaṃ."
                },
                {
                    "n": 11,
                    "pali_roman": "Dānañca piyavācā ca, atthacariyā ca yā idha"
                },
                {
                    "n": 12,
                    "pali_roman": "Samānattatā ca dhammesu, tattha tattha yathārahaṃ."
                },
                {
                    "n": 13,
                    "pali_roman": "Ete kho saṅgahā loke, rathassāṇīva yāyato"
                },
                {
                    "n": 14,
                    "pali_roman": "Ete ca saṅgahā nāssu, na mātā puttakāraṇā"
                },
                {
                    "n": 15,
                    "pali_roman": "Labhetha mānaṃ pūjaṃ vā, pitā vā puttakāraṇā."
                },
                {
                    "n": 16,
                    "pali_roman": "Yasmā ca saṅgahā ete, sampekkhanti paṇḍitā"
                },
                {
                    "n": 17,
                    "pali_roman": "Tasmā mahattaṃ papponti, pasaṃsā ca bhavanti te."
                }
            ],
            "meaning": [
                "Parents are the eastern direction, teachers the southern direction, wife and children the western direction, friends and associates the northern direction, servants and workers the lower direction, ascetics and brahmins the upper direction. These directions a householder should honor, being competent in his family life.",
                "The wise, endowed with virtue, gentle and intelligent, humble and well-conducted-such a one gains honor. Energetic, not lazy, unshaken in adversity, blameless in conduct, wise-such a one gains honor.",
                "A supporter, a maker of friends, generous, free from stinginess, a leader, a guide, a reconciler-such a one gains honor.",
                "Generosity, kind speech, beneficial conduct, and impartiality in all things-as appropriate in each case.",
                "These are the bonds of sympathy in the world, like the linchpin of a moving chariot. If these were not present, neither mother nor father would receive honor or respect from their children.",
                "But since these qualities are regarded by the wise, they attain greatness and are praised."
            ]
        }
    ]
})

# Lakkhaṇa Sutta: from scratchpad/lakkhana.txt (photos p232–235).
MORE.append({
    "id": "owen-lakkhana-sutta",
    "title_thai": "",
    "title": "Lakkhaṇa Sutta (Short Version)",
    "title_english": "The Discourse on the 32 Marks of a Great Man (Buddha and emperor)",
    "source_pages": "232–235",
    "intro": [],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Evaṃ me sutaṃ. Ekaṃ samayaṃ Bhagavā Sāvatthiyaṃ viharati Jetavane Anāthapiṇḍikassa ārāme. Tatra kho Bhagavā bhikkhū āmantesi “bhikkhavo”ti. “Bhadante”ti te bhikkhū Bhagavato paccassosuṃ.",
                    "english": "Thus have I heard. At one time the Blessed One was staying at Sāvatthī, in Jetavana, Anāthapiṇḍika's Park. There the Blessed One addressed the monks: “Monks.” “Venerable Sir,” they replied."
                },
                {
                    "n": 2,
                    "pali_roman": "Bhagavā etadavoca: “Dvattiṃsimāni bhikkhave mahāpurisassa mahāpurisalakkhaṇāni, yehi samannāgatassa mahāpurisassa dveva gatiyo bhavanti anaññā. Sace agāraṃ ajjhāvasati rājā hoti cakkavattī dhammiko dhammarājā cāturanto vijitāvī janapadatthāvariyappatto sattaratanasamanvāgato. Tassimāni satta ratanāni bhavanti, seyyathīdaṃ: cakkaratanaṃ, hatthiratanaṃ, assaratanaṃ, maṇiratanaṃ, itthiratanaṃ, gahapatiratanaṃ, pariṇāyakaratanaṃ eva sattamaṃ. Parosahassaṃ kho panassa puttā bhavanti sūrā vīraṅgarūpā parasenappamaddanā. So imaṃ pathaviṃ sāgarapariyantaṃ akhilaṃ animittaṃ akaṇṭakaṃ iddhaṃ phītaṃ khemaṃ sivaṃ nirabbudaṃ adaṇḍena asatthena dhammena samena abhivijiya ajjhāvasati. Sace kho pana agārā anagāriyaṃ pabbajati arahā hoti sammāsambuddho loke vivaṭacchado.”",
                    "english": "The Blessed One said: “Monks, there are thirty-two marks of a Great Man. When a Great Man possesses these marks, only two paths are possible for him, no other. If he lives the household life, he becomes a emperor, a Wheel-Turning Monarch, a righteous ruler who rules by Dhamma, a conqueror of the four quarters, established in his realm, endowed with the seven treasures: the Wheel Treasure, the Elephant Treasure, the Horse Treasure, the Jewel Treasure, the Woman Treasure, the Householder Treasure, and the Advisor Treasure. He has more than a thousand sons, brave and heroic, who defeat enemy armies. He rules the earth, surrounded by the ocean, without violence, without weapons, justly and righteously, in prosperity, safety, and peace. But if he goes forth into homelessness, he becomes an arahant, a perfectly awakened Buddha, who removes the veil from the world.”"
                },
                {
                    "n": 3,
                    "pali_roman": "Katamāni tāni bhikkhave dvattiṃsa mahāpurisassa mahāpurisalakkhaṇāni, yehi samannāgatassa mahāpurisassa dveva gatiyo bhavanti anaññā? Sace agāraṃ ajjhāvasati rājā hoti cakkavattī. Saṅkhittaṃ. Sace kho pana agārā anagāriyaṃ pabbajati arahā hoti sammāsambuddho loke vivaṭacchado.",
                    "english": "“And what, monks, are these thirty-two marks of a Great Man?”"
                },
                {
                    "n": 4,
                    "pali_roman": "Idha bhikkhave mahāpuriso supatiṭṭhitapādo hoti. Yampi bhikkhave mahāpuriso supatiṭṭhitapādo hoti, idampi bhikkhave mahāpurisassa mahāpurisalakkhaṇaṃ bhavati.",
                    "english": "1. He has well-planted feet."
                },
                {
                    "n": 5,
                    "pali_roman": "Puna caparaṃ bhikkhave mahāpurisassa heṭṭhāpādatalesu cakkāni jātāni honti sahassārāni sanemikāni sanābhikāni sabbākāraparipūrāni. Yampi bhikkhave mahāpurisassa heṭṭhāpādatalesu cakkāni jātāni honti sahassārāni sanemikāni sanābhikāni sabbākāraparipūrāni, idampi bhikkhave mahāpurisassa mahāpurisalakkhaṇaṃ bhavati.",
                    "english": "2. On the soles of his feet are wheels with a thousand spokes, complete with rim and hub."
                },
                {
                    "n": 6,
                    "pali_roman": "Puna caparaṃ bhikkhave mahāpuriso āyatapaṇhi hoti, dīghaṅgulī hoti, mudutalunahatthapādo hoti, jālahatthapādo hoti, ussaṅkhapādo hoti, eṇijaṅgho hoti, ṭhitako va anonamanto ubhohi pāṇitalehi jaṇṇukāni parimasati parimajjati, kosohitavatthaguyho hoti, suvaṇṇavaṇṇo kañcanasannibhattaco hoti, sukhumacchavī hoti sukhumattā chaviya rajojallaṃ kāye na upalippati, ekekalomo hoti ekekāni lomāni lomakūpesu jātāni, uddhaggolomo hoti uddhaggāni lomāni jātāni nīlāni añjanavaṇṇāni kuṇḍalāvattāni dakkhiṇāvattakajātāni, brahmujugatto hoti, sattussado hoti, sīhapubbaddhakāyo hoti, pītantaraṃso hoti, nigrodhaparimaṇḍalo hoti yāvatakvassa kāyo tāvatakvassa byāmo yāvatakvassa byāmo tāvatakvassa kāyo, samavaṭṭakkhandho hoti, rasaggasaggī hoti, sīhahanu hoti, cattālīsadanto hoti, samadanto hoti, aviraḷadanto hoti, susukkadāṭho hoti, pahūtajivho hoti, brahmasaro hoti karavikabhāṇī hoti, abhinīlanetto hoti, gopakhumo hoti, uṇṇā bhumukantare jātā hoti odātā mudu tūlasannibhā. Yampi bhikkhave mahāpurisassa uṇṇā bhumukantare jātā hoti odātā mudu tūlasannibhā, idampi bhikkhave mahāpurisassa mahāpurisalakkhaṇaṃ bhavati.",
                    "english": "3. He has projecting heels. 4. He has long fingers and toes. 5. His hands and feet are soft and tender. 6. His hands and feet are webbed. 7. His ankles are high. 8. His legs are like those of an antelope. 9. Standing upright without bending, he can touch his knees with both hands. 10. His private parts are enclosed in a sheath. 11. His complexion is golden, like refined gold. 12. His skin is so delicate that dust and dirt do not cling to his body. 13. Each hair grows singly from each pore. 14. The hairs grow upward, dark blue-black like collyrium, curling to the right. 15. His body is straight like that of Brahmā. 16. He has seven convex surfaces 17. His chest is like that of a lion. 18. There is no hollow between his shoulders. 19. His body is proportioned like a banyan tree, the span of his arms equal to his height. 20. His shoulders are evenly rounded. 21. He has a refined sense of taste. 22. He has a lion-like jaw. 23. He has forty teeth. 24. His teeth are even. 25. His teeth have no gaps. 26. His teeth are very white. 27. He has a large tongue. 28. He has a Brahmā-like voice, like the cal of a karavīka bird. 29. His eyes are deep blue. 30. He has eyelashes like those of a cow. 31. Between his eyebrows there grows a tuft of hair, white, soft, like cotton."
                }
            ],
            "meaning": [
                "32. His head is shaped like a royal turban (uṇhīsa).",
                "“These, monks, are the thirty-two marks of a Great Man. Possessing these, only two destinies are possible: if he remains in the household life, he becomes a Wheel-Turning Monarch; if he goes forth, he becomes a perfectly awakened Buddha.”"
            ]
        }
    ],
    "review_notes": [
        "Pali ends at mark 31 (uṇṇā); English adds 32 (uṇhīsa).",
        "Mark 28 prints 'cal'; probably 'call'."
    ]
})

# Vasala Sutta: from scratchpad/vasala.txt (photos p236–241).
MORE.append({
    "id": "owen-vasala-sutta",
    "title_thai": "",
    "title": "Vasala Sutta",
    "title_english": "Outcast Sutta",
    "source_pages": "236–241",
    "intro": [],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Evaṃ me sutaṃ. Ekaṃ samayaṃ Bhagavā Sāvatthiyaṃ viharati Jetavane Anāthapiṇḍikassa ārāme. Atha kho Bhagavā pubbaṇhasamayaṃ nivāsetvā pattacīvaramādāya Sāvatthiṃ piṇḍāya pāvisi. Tena kho pana samayena Aggikabhāradvājassa brāhmaṇassa nivesane aggi pajjalito hoti āhutī paggahitā. Atha kho Bhagavā Sāvatthiyaṃ sapadānaṃ piṇḍāya caramāno yena Aggikabhāradvājassa brāhmaṇassa nivesanaṃ tenupasaṅkami. Addasā kho Aggikabhāradvājo brāhmaṇo Bhagavantaṃ dūrato va āgacchantaṃ, disvāna Bhagavantaṃ etadavoca: “Atreva muṇḍaka, atreva samaṇaka, atreva vasalaka, tiṭṭhāhī”ti.",
                    "english": "Thus have I heard. At one time the Blessed One was staying at Sāvatthī, in Jeta's Grove, in the monastery of Anāthapiṇḍika. Then, in the morning, the Blessed One put on his robe, took his bowl and outer robe, and entered Sāvatthī for alms. At that time, in the house of the brahmin Aggikabhāradvāja, a fire was burning and an offering was being prepared. Then the Blessed One, going on alms round in Sāvatthī from house to house, approached the residence of the brahmin Aggikabhāradvāja. The brahmin Aggikabhāradvāja saw the Blessed One coming from a distance. Seeing him, he said: “Stop there, shaven one! Stop there, ascetic! Stop there, outcast! Stand there!”"
                },
                {
                    "n": 2,
                    "pali_roman": "Evaṃ vutte Bhagavā Aggikabhāradvājaṃ brāhmaṇaṃ etadavoca: “Jānāsi pana tvaṃ brāhmaṇa vasalaṃ vā vasalakaraṇe vā dhamme”ti? “Na khvāhaṃ bho Gotama jānāmi vasalaṃ vā vasalakaraṇe vā dhamme. Sādhu me bhavaṃ Gotamo tathā dhammaṃ desetu yathāhaṃ jāneyyaṃ vasalaṃ vā vasalakaraṇe vā dhamme”ti. “Tena hi brāhmaṇa suṇāhi, sādhukaṃ manasikarohi, bhāsissāmī”ti. “Evaṃ bho”ti kho Aggikabhāradvājo brāhmaṇo Bhagavato paccassosi. Bhagavā etadavoca.",
                    "english": "When this was said, the Blessed One said to the brahmin Aggikabhāradvāja: “But do you know, brahmin, what an outcast is, or the things that make one an outcast?” “No indeed, Master Gotama, I do not know what an outcast is or the things that make one an outcast. It would be good if Master Gotama would teach me the Dhamma so that I may know what an outcast is and the things that make one an outcast.” “Then listen, brahmin, pay careful attention, I will speak.” “Yes, sir,” the brahmin Aggikabhāradvāja replied to the Blessed One. The Blessed One said:"
                }
            ]
        },
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Kodhano upanāhī ca pāpamakkhī ca yo naro"
                },
                {
                    "n": 2,
                    "pali_roman": "vipannadiṭṭhi māyāvī taṃ jaññā vasalo iti"
                },
                {
                    "n": 3,
                    "pali_roman": "Ekajaṃ vā dvijaṃ vāpi yo dha pāṇaṃ vihiṃsati"
                },
                {
                    "n": 4,
                    "pali_roman": "yassa pāṇe dayā natthi taṃ jaññā vasalo iti"
                },
                {
                    "n": 5,
                    "pali_roman": "Yo hanti uparundheti gāmāni nigamāni ca"
                },
                {
                    "n": 6,
                    "pali_roman": "niggāhako samaññāto taṃ jaññā vasalo iti"
                },
                {
                    "n": 7,
                    "pali_roman": "Gāme vā yadi vā araññe yaṃ paresaṃ mamāyitaṃ"
                },
                {
                    "n": 8,
                    "pali_roman": "theyyā adinnaṃ āneti taṃ jaññā vasalo iti"
                },
                {
                    "n": 9,
                    "pali_roman": "Yo have iṇamādāya bhuñjamāno palāyati"
                },
                {
                    "n": 10,
                    "pali_roman": "na hi te iṇamatthīti taṃ jaññā vasalo iti"
                },
                {
                    "n": 11,
                    "pali_roman": "Yo ve kiñcikkhakamyatā panthasmiṃ vajataṃ janaṃ"
                },
                {
                    "n": 12,
                    "pali_roman": "hanta kiñcikkhamāteti taṃ jaññā vasalo iti"
                },
                {
                    "n": 13,
                    "pali_roman": "Yo attahetu parahetu dhanahetu ca yo naro"
                },
                {
                    "n": 14,
                    "pali_roman": "sakkhipuṭṭho musā brūti taṃ jaññā vasalo iti"
                },
                {
                    "n": 15,
                    "pali_roman": "Yo ñātīnaṃ sakhīnaṃ vā dāresu paṭidissati"
                },
                {
                    "n": 16,
                    "pali_roman": "sahasā sampiyena vā taṃ jaññā vasalo iti"
                },
                {
                    "n": 17,
                    "pali_roman": "Yo mātaraṃ vā pitaraṃ vā jiṇṇakaṃ gatayobbanaṃ"
                },
                {
                    "n": 18,
                    "pali_roman": "pahusanto na bharati taṃ jaññā vasalo iti"
                },
                {
                    "n": 19,
                    "pali_roman": "Yo mātaraṃ vā pitaraṃ vā bhātaraṃ bhaginiṃ sasuṃ"
                },
                {
                    "n": 20,
                    "pali_roman": "hanti roseti vācāya taṃ jaññā vasalo iti"
                },
                {
                    "n": 21,
                    "pali_roman": "Yo atthaṃ pucchito santo anatthamanusāsati"
                },
                {
                    "n": 22,
                    "pali_roman": "paṭicchannena manteti taṃ jaññā vasalo iti"
                },
                {
                    "n": 23,
                    "pali_roman": "Yo katvā pāpakaṃ kammaṃ mā maṃ jaññāti icchati"
                },
                {
                    "n": 24,
                    "pali_roman": "yo paṭicchannakammano taṃ jaññā vasalo iti"
                },
                {
                    "n": 25,
                    "pali_roman": "Yo ve parakulaṃ gantvā bhutvā ca sucibhojanaṃ"
                },
                {
                    "n": 26,
                    "pali_roman": "āgataṃ nappaṭipūjeti taṃ jaññā vasalo iti"
                },
                {
                    "n": 27,
                    "pali_roman": "Yo brāhmaṇaṃ vā samaṇaṃ vā aññaṃ vāpi vanibbakaṃ"
                },
                {
                    "n": 28,
                    "pali_roman": "musāvādena vañceti taṃ jaññā vasalo iti"
                },
                {
                    "n": 29,
                    "pali_roman": "Yo brāhmaṇaṃ vā samaṇaṃ vā bhattakāle upaṭṭhite"
                },
                {
                    "n": 30,
                    "pali_roman": "roseti vācā na ca deti taṃ jaññā vasalo iti"
                },
                {
                    "n": 31,
                    "pali_roman": "Asataṃ yodha pabrūti mohena paliguṇṭhito"
                },
                {
                    "n": 32,
                    "pali_roman": "kiñcikkhaṃ nijigīṃsāno taṃ jaññā vasalo iti"
                },
                {
                    "n": 33,
                    "pali_roman": "Yo cattanam samukkaṃse pare ca avajānati"
                },
                {
                    "n": 34,
                    "pali_roman": "nihīno sena mānena taṃ jaññā vasalo iti"
                },
                {
                    "n": 35,
                    "pali_roman": "Rosako kadariyo ca pāpiccho maccharī saṭho"
                },
                {
                    "n": 36,
                    "pali_roman": "ahiriko anottappī taṃ jaññā vasalo iti"
                },
                {
                    "n": 37,
                    "pali_roman": "Yo Buddhaṃ paribhāsati atha vā tassa sāvakaṃ"
                },
                {
                    "n": 38,
                    "pali_roman": "paribbājakaṃ gahattaṃ vā taṃ jaññā vasalo iti"
                },
                {
                    "n": 39,
                    "pali_roman": "Yo ve anarahaṃ santo arahaṃ paṭijānati"
                },
                {
                    "n": 40,
                    "pali_roman": "coro sabrahmake loke eso kho vasalādhamma"
                },
                {
                    "n": 41,
                    "pali_roman": "Ete kho vasalā vuttā mayā ye te pakāsitā"
                },
                {
                    "n": 42,
                    "pali_roman": "Na jaccā vasalo hoti na jaccā hoti brāhmaṇo"
                },
                {
                    "n": 43,
                    "pali_roman": "kammunā vasalo hoti hoti kammunā hoti brāhmaṇo"
                },
                {
                    "n": 44,
                    "pali_roman": "Tadamināpi jānātha yathā metaṃ nidassanaṃ"
                },
                {
                    "n": 45,
                    "pali_roman": "caṇḍālaputto sopāko Mātaṅgo iti vissuto"
                },
                {
                    "n": 46,
                    "pali_roman": "So yasapparamappatto Mātaṅgo yaṃ sudullabhaṃ"
                },
                {
                    "n": 47,
                    "pali_roman": "āgacchuṃ tassupatthānaṃ khattiyā brāhmaṇā Bahoo"
                },
                {
                    "n": 48,
                    "pali_roman": "So devayānaṃ abhiruyha virajaṃ so mahāpathaṃ"
                },
                {
                    "n": 49,
                    "pali_roman": "kāmarāgaṃ virājetvā brahmalokūpago ahu"
                },
                {
                    "n": 50,
                    "pali_roman": "na naṃ jāti nivāresi brahmalokūpapattiyā"
                },
                {
                    "n": 51,
                    "pali_roman": "Ajjhāyikakule jātā brāhmaṇā mantabandhavā"
                },
                {
                    "n": 52,
                    "pali_roman": "te ca pāpesu kammesu abhiṇhamupadissare"
                },
                {
                    "n": 53,
                    "pali_roman": "Diṭṭheva dhamme gārayhā samparāye ca duggati"
                },
                {
                    "n": 54,
                    "pali_roman": "na ne jāti nivāreti duggaccā garahāya vā"
                },
                {
                    "n": 55,
                    "pali_roman": "Na jaccā vasalo hoti na jaccā hoti brāhmaṇo"
                },
                {
                    "n": 56,
                    "pali_roman": "kammunā vasalo hoti kammunā hoti brāhmaṇoti."
                }
            ],
            "meaning": [
                "“One who is angry and bears grudges, who is evil-minded and ungrateful, who holds wrong views and is deceitful-know that person as an outcast.",
                "Whoever in this world harms living beings, whether once-born or twice-born, and has no compassion for living creatures-know that person as an outcast.",
                "Whoever destroys or oppresses villages and towns and is known as a tyrant-know that person as an outcast.",
                "Whether in village or forest, whoever steals what belongs to others, taking what is not given-know that person as an outcast.",
                "Whoever, having taken a loan, enjoys it and then runs away saying, ‘I owe nothing’-know that person as an outcast.",
                "Whoever, desiring something small, attacks people on the road and kills to take it-know that person as an outcast.",
                "Whoever, for his own sake, for the sake of others, or for wealth, when questioned as a witness, speaks falsely-know that person as an outcast.",
                "Whoever is found with the wives of relatives or friends, either by force or by consent-know that person as an outcast.",
                "Whoever, being wealthy, does not support his mother and father who are old and past their youth-know that person as an outcast.",
                "Whoever strikes or abuses with words his mother, father, brother, sister, or mother-in-law-know that person as an outcast.",
                "Whoever, when asked what is good, gives harmful advice and speaks with hidden intent-know that person as an outcast.",
                "Whoever, having done evil, wishes ‘May no one know me,’ and conceals his actions-know that person as an outcast.",
                "Whoever, having gone to another's house and eaten fine food, does not honor the host when he returns-know that person as an outcast.",
                "Whoever deceives a brahmin, an ascetic, or any mendicant by lying-know that person as an outcast.",
                "Whoever, when a brahmin or ascetic comes at mealtime, abuses him with words and does not give anything-know that person as an outcast.",
                "Whoever, blinded by delusion, speaks falsehood, desiring some small gain-know that person as an outcast.",
                "Whoever exalts himself and despises others, being low through his own pride-know that person as an outcast.",
                "Whoever is angry, stingy, of evil desires, greedy, deceitful, shameless, and without moral fear-know that person as an outcast.",
                "Whoever insults the Buddha, or one of his disciples, or a recluse, or a householder-know that person as an outcast.",
                "Whoever, not being an arahant, claims to be an arahant-he is a thief in the world together with its gods; this is the lowest outcast.",
                "These are called outcasts, as I have declared. Not by birth is one an outcast; not by birth is one a brahmin. By action one becomes an outcast; by action one becomes a brahmin.",
                "And you should know this by an example:",
                "There was a man named Mātaṅga, born in a very low family, known as a caṇḍāla. Mātaṅga attained the highest fame, which is hard to gain. Many nobles and brahmins came to attend on him.",
                "He mounted the divine vehicle, traveled the great path, and, having removed sensual desire, he was reborn in the Brahma world. His birth did not prevent him from reaching the Brahma world.",
                "But there are brahmins born in learned families, relatives of sacred texts, who repeatedly engage in evil actions.",
                "They are blamed in this very life and go to a bad destination after death. Their birth does not prevent them from blame or from a bad destination.",
                "Not by birth is one an outcast; not by birth is one a brahmin. By action one becomes an outcast; by action one becomes a brahmin.”"
            ]
        },
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "“Abhikkantaṃ bho Gotama, abhikkantaṃ bho Gotama Seyyathāpi nikkujjitaṃ vā ukkujjeyya, paṭicchannaṃ vā vivareyya, mūḷhassa vā maggaṃ ācikkheyya, andhakāre vā telapajjotaṃ dhāreyya, cakkhumanto rūpāni dakkhantīti; evamevaṃ anekapariyāyena bhotā Gotamena dhammo pakāsito.",
                    "english": "When this was said, the brahmin Aggikabhāradvāja said to the Blessed One: “Excellent, Master Gotama! Excellent, Master Gotama! Just as if one were to set upright what had been overturned, reveal what was hidden, show the way to one who was lost, or hold up a lamp in the darkness so that those with eyes could see-just so has the Dhamma been explained in many ways by Master Gotama."
                },
                {
                    "n": 2,
                    "pali_roman": "Esāhaṃ bhavantaṃ Gotamaṃ saraṇaṃ gacchāmi, dhammañca bhikkhusaṅghañca. Upāsakaṃ maṃ bhavaṃ Gotamo dhāretu ajjatagge pāṇupetaṃ saraṇaṃ gataṃ.”",
                    "english": "I go to Master Gotama for refuge, to the Dhamma, and to the Sangha. Let Master Gotama remember me as a lay follower who has gone for refuge from this day forward for life.”"
                }
            ]
        }
    ],
    "review_notes": [
        "Printed as in Ajarn Owen's book: 'gahattaṃ' (standard gahaṭṭhaṃ), 'hoti kammunā hoti brāhmaṇo' (extra hoti), 'Bahoo' (standard bahū), 'tassupatthānaṃ' (standard tassupaṭṭhānaṃ)."
    ]
})

# Pahārāda Sutta: from scratchpad/paharada.txt (photos p242–250).
MORE.append({
    "id": "owen-paharada-sutta",
    "title_thai": "",
    "title": "Pahārāda Sutta",
    "title_english": "Great Ocean Sutta",
    "source_pages": "242–250",
    "intro": [],
    "introduction": [
        "It records a dialogue between the Buddha and Pahārāda, the lord of the Asuras. In this teaching, both sides compare the eight wonderful qualities of the great ocean with the eight wonderful qualities of the Dhamma-Vinaya"
    ],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Ekaṃ samayaṃ Bhagavā Verañjāyaṃ viharati Naḷerupucimaṇḍe. Atha kho Pahārādo asurindo yena Bhagavā tenupasaṅkami, upasaṅkamitvā Bhagavantaṃ abhivādetvā ekamantaṃ aṭṭhāsi. Ekamantaṃ ṭhitaṃ kho Pahārādaṃ asurindaṃ Bhagavā etadavoca: “Api pana Pahārāda, asurā mahāsamudde abhiramantī”ti? “Abhiramanti, bhante, asurā mahāsamudde”ti. “Kati pana, Pahārāda, mahāsamudde acchariyā abbhutadhammā ye disvā disvā asurā mahāsamudde abhiramantī”ti “Aṭṭha, bhante, mahāsamudde acchariyā abbhutadhammā ye disvā disvā asurā mahāsamudde abhiramanti. Katame aṭṭha",
                    "english": "At one time the Blessed One was staying at Verañjā, at the root of the Naḷeru tree. Then Pahārāda, the lord of the Asuras, approached the Blessed One. Having approached, he paid homage to the Blessed One and stood to one side. Standing to one side, the Blessed One said to Pahārāda, the lord of the Asuras: “Pahārāda, do the Asuras delight in the great ocean?” “They do, Bhante, the Asuras delight in the great ocean.” “How many, Pahārāda, are the wonderful and marvelous qualities of the great ocean, seeing which the Asuras delight in the great ocean?” “There are eight, Bhante, wonderful and marvelous qualities of the great ocean, seeing which the Asuras delight in the great ocean. What eight?"
                },
                {
                    "n": 2,
                    "pali_roman": "Mahāsamuddo, bhante, anupubbaninno anupubbapoṇo anupubbapabbhāro, nāyatakeneva papāto. Yampi, bhante, mahāsamuddo anupubbaninno anupubbapoṇo anupubbapabbhāro, nāyatakeneva papāto, ayaṃ, bhante, mahāsamudde paṭhamo acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Bhante, the great ocean has a gradual slope, a gradual incline, a gradual depth; it does not suddenly drop off. In that the great ocean has a gradual slope, a gradual incline, a gradual depth, and does not suddenly drop off, this is the first wonderful and marvelous quality of the great ocean, seeing which the Asuras delight in it."
                },
                {
                    "n": 3,
                    "pali_roman": "Puna caparaṃ, bhante, mahāsamuddo ṭhitadhammo velaṃ nātivattati. Yampi, bhante, mahāsamuddo ṭhitadhammo velaṃ nātivattati, ayaṃ, bhante, mahāsamudde dutiyo acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Again, Bhante, the great ocean remains stable and does not overstep its boundary. In that the great ocean remains stable and does not overstep its boundary, this is the second wonderful and marvelous quality of the great ocean, seeing which the Asuras delight in it."
                },
                {
                    "n": 4,
                    "pali_roman": "Puna caparaṃ, bhante, mahāsamuddo na matena kuṇapena saṃvasati. Yaṃ hoti mahāsamudde mataṃ kuṇapaṃ taṃ khippameva tīraṃ vāheti, thalaṃ ussāreti. Yampi, bhante, mahāsamuddo na matena kuṇapena saṃvasati, yaṃ hoti mahāsamudde mataṃ kuṇapaṃ taṃ khippameva tīraṃ vāheti, thalaṃ ussāreti, ayaṃ, bhante, mahāsamudde tatiyo acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Again, Bhante, the great ocean does not associate with a corpse. Whatever corpse there is in the great ocean, it quickly carries it to the shore and throws it up on land. In that the great ocean does not associate with a corpse, but quickly carries it to the shore and throws it up on land, this is the third wonderful and marvelous quality of the great ocean, seeing which the Asuras delight in it."
                },
                {
                    "n": 5,
                    "pali_roman": "Puna caparaṃ, bhante, yā kāci mahānadiyo seyyathidaṃ Gaṅgā Yamunā Aciravatī Sarabhū Mahī, tā mahāsamuddaṃ patvā jahanti purimāni nāmagottāni, mahāsamuddotveva saṅkhaṃ gacchanti. Yampi, bhante, yā kāci mahānadiyo seyyathidaṃ Gaṅgā Yamunā Aciravatī Sarabhū Mahī, tā mahāsamuddaṃ patvā jahanti purimāni nāmagottāni, mahāsamuddotveva saṅkhaṃ gacchanti, ayaṃ, bhante, mahāsamudde catuttho acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Again, Bhante, whatever great rivers there are, such as the Ganges, Yamunā, Aciravatī, Sarabhū, and Mahī, when they reach the great ocean, they abandon their former names and identities and are simply called ‘the great ocean.’ In that the great rivers, upon reaching the great ocean, abandon their former names and identities and are known simply as the great ocean, this is the fourth wonderful and marvelous quality of the great ocean, seeing which the Asuras delight in it."
                },
                {
                    "n": 6,
                    "pali_roman": "Puna caparaṃ, bhante, yā kāci loke savantiyo mahāsamuddaṃ appenti, yā ca antalikkhā dhārā papatanti, na tena mahāsamuddassa ūnattaṃ vā pūrattaṃ vā paññāyati. Yampi, bhante, yā kāci loke savantiyo mahāsamuddaṃ appenti, yā ca antalikkhā dhārā papatanti, na tena mahāsamuddassa ūnattaṃ vā pūrattaṃ vā paññāyati, ayaṃ, bhante, mahāsamudde pañcamo acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Again, Bhante, whatever streams in the world flow into the great ocean, and whatever rain falls from the sky, by that the great ocean is not seen to increase or decrease. In that the great ocean is not seen to increase or decrease despite the inflow of waters, this is the fifth wonderful and marvelous quality of the great ocean, seeing which the Asuras delight in it."
                },
                {
                    "n": 7,
                    "pali_roman": "Puna caparaṃ, bhante, mahāsamuddo ekaraso loṇaraso. Yampi, bhante, mahāsamuddo ekaraso loṇaraso, ayaṃ, bhante, mahāsamudde chaṭṭho acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Again, Bhante, the great ocean has one taste, the taste of salt. In that the great ocean has one taste, the taste of salt, this is the sixth wonderful and marvelous quality of the great ocean, seeing which the Asuras delight in it."
                },
                {
                    "n": 8,
                    "pali_roman": "Puna caparaṃ, bhante, mahāsamuddo bahuratano anekaratano. Tatrimāni ratanāni seyyathidaṃ muttā maṇi veḷuriyo saṅkho silā pavāḷaṃ rajataṃ jātarūpaṃ lohitako masāragallaṃ. Yampi, bhante, mahāsamuddo bahuratano anekaratano, tatrimāni ratanāni seyyathidaṃ muttā maṇi veḷuriyo saṅkho silā pavāḷaṃ rajataṃ jātarūpaṃ lohitako masāragallaṃ, ayaṃ bhante mahāsamudde sattamo acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Again, Bhante, the great ocean is rich in treasures, possessing many kinds of treasures. These treasures are such as pearls, gems, beryl, conch, stone, coral, silver, gold, and ruby. In that the great ocean is rich in treasures, possessing many kinds of treasures such as pearls, gems, beryl, conch, stone, coral, silver, gold, and ruby, this is the seventh wonderful and marvelous quality of the great ocean, seeing which the Asuras delight in it."
                },
                {
                    "n": 9,
                    "pali_roman": "Puna caparaṃ, bhante, mahāsamuddo mahatānaṃ bhūtānaṃ āvāso. Tatrime bhūtā timitimingalā timirapiṅgalā asurā nāgā gandhabbā santi mahāsamudde, yojanasatikāpi attabhāvā, dviyojanasatikāpi attabhāvā, tiyojanasatikāpi attabhāvā, catuyojanasatikāpi attabhāvā, pañcayojanasatikāpi attabhāvā. Yampi, bhante, mahāsamuddo mahatānaṃ bhūtānaṃ āvāso, tatrime bhūtā timitimingalā timirapiṅgalā asurā nāgā gandhabbā santi mahāsamudde, Yo janasatikāpi attabhāvā, dve janasatikāpi attabhāvā, tī janasatikāpi attabhāvā, catu janasatikāpi attabhāvā, pañca janasatikāpi attabhāvā, ayaṃ bhante mahāsamudde aṭṭhamo acchariyo abbhutadhammo yaṃ disvā disvā asurā mahāsamudde abhiramanti. Ime kho, bhante, mahāsamudde aṭṭha acchariyā abbhutadhammā ye disvā disvā asurā mahāsamudde abhiramanti.",
                    "english": "Again, Bhante, the great ocean is the dwelling place of great beings. Therein exist beings such as timi, timingala, timirapiṅgala, asuras, nāgas, and gandhabbas in the great ocean, beings whose bodies are a hundred yojanas in size, two hundred yojanas in size, three hundred yojanas in size, four hundred yojanas in size, and five hundred yojanas in size. And also, Bhante, since the great ocean is the abode of such great beings, where these creatures-timi, timingala, timirapiṅgala, asuras, nāgas, and gandhabbas-exist, with bodies measuring one hundred yojanas, two hundred yojanas, three hundred yojanas, four hundred yojanas, and five hundred yojanas, These, Bhante, are the eight wonderful and marvelous qualities of the great ocean; seeing them again and again, the asuras take delight in the great ocean.”"
                },
                {
                    "n": 10,
                    "pali_roman": "“Api pana, bhante, bhikkhū imasmiṃ dhammavinaye abhiramantī”ti “Abhiramanti, Pahārāda, bhikkhū imasmiṃ dhammavinaye”ti. “Kati pana, bhante, imasmiṃ dhammavinaye acchariyā abbhutadhammā ye disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramantī”ti? “Aṭṭha, Pahārāda, imasmiṃ dhammavinaye acchariyā abbhutadhammā ye disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti. Katame aṭṭha?",
                    "english": "“Bhante, do the monks delight in this Dhamma and discipline?” “They do, Pahārāda, the monks delight in this Dhamma and discipline.” “How many, Bhante, are the wonderful and marvelous qualities in this Dhamma and discipline, seeing which the monks delight in it?” “There are eight, Pahārāda, wonderful and marvelous qualities in this Dhamma and discipline, seeing which the monks delight in it. What eight?"
                },
                {
                    "n": 11,
                    "pali_roman": "Seyyathāpi, Pahārāda, mahāsamuddo anupubbaninno anupubbapoṇo anupubbapabbhāro, nāyatakeneva papāto, evameva kho, Pahārāda, imasmiṃ dhammavinaye anupubbasikkhā anupubbakiriyā anupubbapaṭipadā, nāyatakeneva aññāpaṭivedho. Yampi, Pahārāda, imasmiṃ dhammavinaye anupubbasikkhā anupubbakiriyā anupubbapaṭipadā, nāyatakeneva aññāpaṭivedho, ayaṃ, Pahārāda, imasmiṃ dhammavinaye paṭhamo acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti.",
                    "english": "Just as, Pahārāda, the great ocean has a gradual slope, a gradual incline, a gradual depth, and does not suddenly drop off, even so, Pahārāda, in this Dhamma and discipline there is gradual training, gradual practice, gradual progress; there is no sudden realization. In that there is gradual training, gradual practice, and gradual progress without sudden realization, this is the first wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it."
                },
                {
                    "n": 12,
                    "pali_roman": "Seyyathāpi, Pahārāda, mahāsamuddo ṭhitadhammo velaṃ nātivattati, evameva kho, Pahārāda, yaṃ mayā sāvakānaṃ sikkhāpadaṃ paññattaṃ, taṃ mama sāvakā jīvitahetupi nātikkamanti. Yampi, Pahārāda, mayā sāvakānaṃ sikkhāpadaṃ paññattaṃ, taṃ mama sāvakā jīvitahetupi nātikkamanti, ayaṃ Pahārāda imasmiṃ dhammavinaye dutiyo acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti.",
                    "english": "Just as, Pahārāda, the great ocean remains stable and does not overstep its boundary, even so, Pahārāda, whatever training rules I have laid down for my disciples, they do not transgress them even for the sake of life. In that the disciples do not transgress the training rules even for the sake of life, this is the second wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it."
                },
                {
                    "n": 13,
                    "pali_roman": "Seyyathāpi, Pahārāda, mahāsamuddo na matena kuṇapena saṃvasati, yaṃ hoti mahāsamudde mataṃ kuṇapaṃ taṃ khippameva tīraṃ vāheti, thalaṃ ussādeti. Evameva kho, Pahārāda, yo so puggalo dussīlo pāpadhammo asucisaṅkassarasamācāro paṭicchannakammanto assamaṇo samaṇapaṭiñño abrahmacārī brahmacāripaṭiñño antopūti avassuto kasambujāto, na tena saṅgho saṃvasati, khippameva naṃ sannipatitvā ukkhipati. Kiñcāpi so hoti majjhe bhikkhusaṅghassa nisinno, atha kho so ārakāva saṅghamhā, saṅgho ca tena. Yampi, Pahārāda, yo puggalo dussīlo pāpadhammo asucisaṅkassarasamācāro paṭicchannakammanto assamaṇo samaṇapaṭiñño abrahmacārī brahmacāripaṭiñño antopūti avassuto kasambujāto, na tena saṅgho saṃvasati, khippaññeva naṃ sannipatitvā ukkhipati. Kiñcāpi so hoti majjhe bhikkhusaṅghassa nisinno, atha kho so ārakāva saṅghamhā, saṅgho ca tena. Ayaṃ, Pahārāda, imasmiṃ dhammavinaye tatiyo acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti.",
                    "english": "Just as, Pahārāda, the great ocean does not associate with a corpse, but quickly carries it to the shore and throws it up on land, even so, Pahārāda, a person who is immoral, of bad conduct, impure, of doubtful behavior, secretive in deeds, not a true ascetic though claiming to be one, not living the holy life though claiming to do so, inwardly rotten, corrupt-such a person is not lived with by the Saṅgha. The Saṅgha quickly assembles and expels him. Even if he is sitting in the midst of the Saṅgha, he is far from the Saṅgha, and the Saṅgha is far from him. In that such a person is not lived with by the Saṅgha and is quickly expelled, this is the third wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it."
                },
                {
                    "n": 14,
                    "pali_roman": "Seyyathāpi, Pahārāda, yā kāci mahānadiyo seyyathidaṃ Gaṅgā Yamunā Aciravatī Sarabhū Mahī, tā mahāsamuddaṃ patvā jahanti purimāni nāmagottāni, mahāsamuddotveva saṅkhaṃ gacchanti. Evameva kho, Pahārāda, cattārome vaṇṇā khattiyā brāhmaṇā vessā suddā, te Tathāgatappavedite dhammavinaye agārasmā anagāriyaṃ pabbajitvā jahanti purimāni nāmagottāni, samaṇā Sakyaputtiyotveva saṅkhaṃ gacchanti. Yampi, Pahārāda, cattārome vaṇṇā khattiyā brāhmaṇā vessā suddā, te Tathāgatappavedite dhammavinaye agārasmā anagāriyaṃ pabbajitvā jahanti purimāni nāmagottāni, samaṇā Sakyaputtiyotveva saṅkhaṃ gacchanti, ayampi, Pahārāda, imasmiṃ dhammavinaye catuttho acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti.",
                    "english": "Just as, Pahārāda, whatever great rivers there are-such as the Ganges, Yamunā, Aciravatī, Sarabhū, and Mahī-upon reaching the great ocean abandon their former names and identities and are known simply as the great ocean, even so, Pahārāda, the four castes-nobles, brahmins, merchants, and workers-upon going forth from the household life into homelessness in this Dhamma and discipline proclaimed by the Tathāgata, abandon their former names and identities and are known simply as ascetics, sons of the Sakyan. In that they abandon their former identities and are known as ascetics, sons of the Sakyan, this is the fourth wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it."
                },
                {
                    "n": 15,
                    "pali_roman": "Seyyathāpi, Pahārāda, yā kāci loke savantiyo mahāsamuddaṃ appenti, yā ca antalikkhā dhārā papatanti, na tena mahāsamuddassa ūnattaṃ vā pūrattaṃ vā paññāyati. Evameva kho, Pahārāda, bahū cepi bhikkhū anupādisesāya nibbānadhātuyā parinibbāyanti, na tena nibbānadhātuyā ūnattaṃ vā pūrattaṃ vā paññāyati. Yampi, Pahārāda, bahū cepi bhikkhū anupādisesāya nibbānadhātuyā parinibbāyanti, na tena nibbānadhātuyā ūnattaṃ vā pūrattaṃ vā paññāyati, ayaṃ Pahārāda imasmiṃ dhammavinaye pañcamo acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti.",
                    "english": "Just as, Pahārāda, whatever streams in the world flow into the great ocean and whatever rain falls from the sky, the great ocean is not seen to increase or decrease, even so, Pahārāda, though many monks attain final Nibbāna without remainder, by that the element of Nibbāna is not seen to increase or decrease. In that Nibbāna is not increased or diminished though many attain it, this is the fifth wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it."
                },
                {
                    "n": 16,
                    "pali_roman": "Seyyathāpi, Pahārāda, mahāsamuddo ekaraso loṇaraso, evameva kho, Pahārāda, ayaṃ dhammavinayo ekaraso vimuttiraso. Yampi, Pahārāda, ayaṃ dhammavinayo ekaraso vimuttiraso, ayaṃ Pahārāda imasmiṃ dhammavinaye chaṭṭho acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti.",
                    "english": "Just as, Pahārāda, the great ocean has one taste, the taste of salt, even so, Pahārāda, this Dhamma and discipline has one taste, the taste of liberation. In that this Dhamma and discipline has one taste, the taste of liberation, this is the sixth wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it."
                },
                {
                    "n": 17,
                    "pali_roman": "Seyyathāpi, Pahārāda, mahāsamuddo bahuratano anekaratano, tatrimāni ratanāni seyyathidaṃ muttā maṇi veḷuriyo saṅkho silā pavāḷaṃ rajataṃ jātarūpaṃ lohitako masāragallaṃ. Evameva kho, Pahārāda, ayaṃ dhammavinayo bahuratano anekaratano. Tatrimāni ratanāni seyyathidaṃ cattāro satipaṭṭhānā cattāro sammappadhānā cattāro iddhipādā pañcindriyāni pañca balāni satta bojjhaṅgā ariyo aṭṭhaṅgiko maggo. Yampi, Pahārāda, ayaṃ dhammavinayo bahuratano anekaratano, tatrimāni ratanāni seyyathidaṃ cattāro satipaṭṭhānā cattāro sammappadhānā cattāro iddhipādā pañcindriyāni pañca balāni satta bojjhaṅgā ariyo aṭṭhaṅgiko maggo, ayaṃ Pahārāda imasmiṃ dhammavinaye sattamo acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti.",
                    "english": "Just as, Pahārāda, the great ocean is rich in treasures, possessing many kinds of treasures such as pearls, gems, beryl, conch, stone, coral, silver, gold, and ruby, even so, Pahārāda, this Dhamma and discipline is rich in treasures, possessing many kinds of treasures. These treasures are: the four establishments of mindfulness, the four right efforts, the four bases of spiritual power, the five faculties, the five powers, the seven factors of awakening, and the noble eightfold path. In that this Dhamma and discipline is rich in treasures with these qualities, this is the seventh wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it."
                },
                {
                    "n": 18,
                    "pali_roman": "Seyyathāpi, Pahārāda, mahāsamuddo mahatānaṃ bhūtānaṃ āvāso. Tatrime bhūtā timitimingalā timirapiṅgalā asurā nāgā gandhabbā santi mahāsamudde, yojanasatikāpi attabhāvā, dviyojanasatikāpi attabhāvā, tiyojanasatikāpi attabhāvā, catuyojanasatikāpi attabhāvā, pañcayojanasatikāpi attabhāvā. Evameva kho, Pahārāda, ayaṃ dhammavinayo mahatānaṃ bhūtānaṃ āvāso. Tatrime bhūtā sotāpanno sotāpattiphalasacchikiriyāya paṭipanno, sakadāgāmī sakadāgāmiphalasacchikiriyāya paṭipanno, anāgāmī anāgāmiphalasacchikiriyāya paṭipanno, arahā arahattāya paṭipanno. Yampi, Pahārāda, ayaṃ dhammavinayo mahatānaṃ bhūtānaṃ āvāso, tatrime bhūtā sotāpanno sotāpattiphalasacchikiriyāya paṭipanno, sakadāgāmī sakadāgāmiphalasacchikiriyāya paṭipanno, anāgāmī anāgāmiphalasacchikiriyāya paṭipanno, arahā arahattāya paṭipanno, ayaṃ Pahārāda imasmiṃ dhammavinaye aṭṭhamo acchariyo abbhutadhammo yaṃ disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramanti. Ime kho, Pahārāda, imasmiṃ dhammavinaye aṭṭha acchariyā abbhutadhammā ye disvā disvā bhikkhū imasmiṃ dhammavinaye abhiramantī”ti.",
                    "english": "Just as, Pahārāda, the great ocean is the dwelling place of great beings-such as timitimingalas, timirapiṅgalas, asuras, nāgas, and gandhabbas, of immense size-so too, Pahārāda, this Dhamma and discipline is the dwelling place of great beings. In it are beings such as a stream-enterer practicing for the realization of the fruit of stream-entry, a once-returner practicing for the realization of the fruit of once-returning, a non-returner practicing for the realization of the fruit of non-returning, and an arahant practicing for arahantship. In that this Dhamma and discipline is the dwelling place of such great beings, this is the eighth wonderful and marvelous quality in this Dhamma and discipline, seeing which the monks delight in it. These, Pahārāda, are the eight wonderful and marvelous qualities in this Dhamma and discipline, seeing which the monks delight in it.”"
                }
            ]
        }
    ],
    "review_notes": [
        "p244: lines of the third quality (dussīlo…) are printed out of order; set here in reading order, all words kept.",
        "p243: 'Yo janasatikāpi … dve janasatikāpi …' kept as printed (standard yojanasatikāpi, dviyojanasatikāpi)."
    ]
})

# Kālāma Sutta: from scratchpad/kalama.txt (photos p251–253).
MORE.append({
    "id": "owen-kalama-sutta",
    "title_thai": "",
    "title": "Kālāma Sutta (Short Version)",
    "title_english": "The Discourse to the Kālāmas",
    "source_pages": "251–253",
    "intro": [],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Ekam samayam bhagava Kosalesu carikam caramano mahata bhikkhusanghena saddhim yena Kesaputtam nama Kalamanan nigamo tad avasari.",
                    "english": "At one time, the Blessed One was wandering in the country of the Kosalans with a large community of monks and arrived at a town of the Kālāmas called Kesaputta."
                },
                {
                    "n": 2,
                    "pali_roman": "Assosum kho Kesaputtiya Kalama samano khalu bho Gotamo Sakyaputto Sakyakula pabbajito Kesaputtam anuppatto. Tam kho pana bhavantam Gotamam evam kalyano kittisaddo abbhuggato: itipi so bhagava arahammā sammasambuddho vijjacaranasampanno sugato lokavidu anuttaro purisadammasarathi sattha devamanussanam buddho bhagava. So imam lokam sadevakam samarakam sabrahmakam sassamanabrahmanim pajam sadevamanussam sayam abhinna sacchikatva pavedeti. So dhammam deseti adikalyanam majjhekalyanam pariyosanakalyanam sattham sabyanjanam kevalaparipunnam parisuddham brahmacariyam pakaseti. Sadhu kho pana tatharupanam arahantam dassanam hoti.",
                    "english": "The Kālāmas of Kesaputta heard: “It is said that the ascetic Gotama, the son of the Sakyans who went forth from the Sakyan clan, has arrived at Kesaputta. A good report of Master Gotama has been spread: ‘Indeed, the Blessed One is an Arahant, perfectly enlightened, accomplished in knowledge and conduct, well-gone, knower of the world, unsurpassed trainer of persons to be trained, teacher of gods and humans, the Buddha, the Blessed One. Having realized for himself with direct knowledge this world—with its devas, Māra, and Brahmā, this generation with its ascetics and brahmins, its gods and humans—he makes it known to others. He teaches the Dhamma that is good in the beginning, good in the middle, and good in the end, complete in meaning and expression. He reveals the perfectly fulfilled and purified holy life.’ It is good to see such Arahants.”"
                },
                {
                    "n": 3,
                    "pali_roman": "Atha kho Kesaputtiya Kalama yena bhagava tenupasankamimsu. Upasankamitva appekacce bhagavantam abhivadetva ekamantam nisidimsu. Appekacce bhagavata saddhim sammodimsu sammodaniyam katham saraniyam vitisaretva ekamantam nisidimsu. Appekacce yena bhagava tenanjalim panametva ekamantam nisidimsu. Appekacce namagottam savatva ekamantam nisidimsu. Appekacce tunhibhuta ekamantam nisidimsu. Ekamantam nisinna kho Kesaputtiya Kalama bhagavantam etad avocum: “Santi bhante eke samanabrahmana Kesaputtam agacchanti. Te sakam yeva vadam dipenti jotenti paravadam pana khumsenti vambhenti paribhavanti opakkhim karonti. Apares pi bhante eke samanabrahmana Kesaputtam agacchanti. Tepi sakam yeva vadam dipenti jotenti paravadam pana khumsenti vambhenti paribhavanti opakkhim karonti. Tesam no bhante amhakam hoteva kankha hoti vicikiccha: ko nu nama imesam bhavantanam samanabrahmananam saccam aha ko musa ti.”",
                    "english": "Then the Kālāmas of Kesaputta went to the Blessed One. Some paid homage and sat down to one side. Some exchanged greetings and polite conversation and then sat down. Some saluted him with joined palms and sat down. Some announced their names and clans and sat down. Some remained silent and sat down. Seated to one side, the Kālāmas said to the Blessed One: “Venerable Sir, there are some ascetics and brahmins who come to Kesaputta. They explain and glorify only their own teachings, but they attack, criticize, and reject the teachings of others. Then others come and do the same. For us, Venerable Sir, there is doubt and uncertainty: ‘Which of these teachers speaks the truth, and which speaks falsely?’”"
                },
                {
                    "n": 4,
                    "pali_roman": "Alam hi vo Kalama kankhitum alam vicikicchitum kankhaniyeva vo thane vicikiccha uppanna etha tumhe Kalama ma anussavena ma paramparaya ma itikiraya ma pitakasampadanena ma takkahetu ma nayahetu ma akaraparivitakkena ma ditthinijjhanakkhantiya ma bhabbarupataya ma samano no garu ti yada tumhe Kalama attanava janeyyatha ime dhamma akusala ime dhamma savajja ime dhamma vinnugarahita ime dhamma samatta samadinna ahitaya dukkhaya samvattanti ti atha tumhe Kalama pajahyyatha tam kim mannatha Kalama lobho purisassa ajjhattam uppajjamano uppajjati hitaya va ahitaya va ti. ahitaya bhante.",
                    "english": "The Blessed One said: “It is proper for you, Kālāmas, to doubt; it is proper for you to be uncertain. Doubt has arisen in a situation that is doubtful. Come, Kālāmas: Do not believe by hearsay, Do not believe by tradition, Do not believe by rumors, Do not believe just because something is written in scriptures, Do not believe by logic alone, Do not believe by reasoning alone, Do not believe by thinking about appearances, Do not believe just because it fits your views, Do not believe because it seems convincing, Do not believe because a teacher is respected. But when you know for yourselves: ‘These things are unwholesome, harmful, criticized by the wise, and when followed lead to suffering,’ then you should abandon them. What do you think, Kālāmas? When greed arises within a person, does it lead to benefit or to harm?” “It leads to harm, Venerable Sir.”"
                },
                {
                    "n": 5,
                    "pali_roman": "Iti kho Kalama yam tam avocumha etha tumhe Kalama ma anussavena ma paramparaya ma itikiraya ma pitakasampadanena ma takkahetu ma nayahetu ma akaraparivitakkena ma ditthinijjhanakkhantiya ma bhabbarupataya ma samano no garu ti yada tumhe Kalama attanava janeyyatha ime dhamma kusala ime dhamma anavajja ime dhamma vinnuppasattha ime dhamma samatta samadinna hitaya sukhaya samvattanti ti atha tumhe Kalama upasampajja vihareyyatha iti yam tam vuttam idam etam paticca vuttam.",
                    "english": "So, Kālāmas, this is what I said: Come, Kālāmas, Do not believe by hearsay, Do not believe by tradition, Do not believe by rumors, Do not believe just because something is written in scriptures, Do not believe by logic alone, Do not believe by reasoning alone, Do not believe by thinking about appearances, Do not believe just because it fits your views, Do not believe because it seems convincing, Do not believe because a teacher is respected. But when you know for yourselves: “These things are good, These things are blameless, These things are praised by the wise, These things, when practiced, lead to benefit and happiness,” then you should accept them, live by them, and put them into practice. This is the reason why it was said."
                }
            ]
        }
    ],
    "review_notes": [
        "Ajarn Owen prints this Pali without diacritics (bhagava, Kalama…); kept as printed. The Thai-script line made from it will need extra care.",
        "'arahammā', 'pajahyyatha' kept as printed."
    ]
})

MORE.append({
    'id': 'owen-silanisamsa-sutta',
    'title_thai': '',
    'title': 'Sīlānisaṃsa Sutta',
    'title_english': 'Five Benefits of Virtue',
    'source_pages': '254',
    'intro': [],
    'sections': [{
        'heading': '',
        'lines': [
            {'n': 1, 'pali_roman': 'Pañcime gahapatayo ānisaṃsā sīlavato sīlasampadāya. Katame pañca.',
             'english': '“Householders, there are these five benefits of one who is virtuous, accomplished in virtue. What five?'},
            {'n': 2, 'pali_roman': 'Idha gahapatayo sīlavā sīlasampanno appamādādhikaraṇaṃ mahantaṃ bhogakkhandhaṃ adhigacchati. Ayaṃ paṭhamo ānisaṃso sīlavato sīlasampadāya.',
             'english': 'Here, householders, a virtuous person, accomplished in virtue, acquires great wealth through diligence. This is the first benefit of one who is virtuous, accomplished in virtue.'},
            {'n': 3, 'pali_roman': 'Puna caparaṃ gahapatayo sīlavato sīlasampannassa kalyāṇo kittisaddo abbhuggacchati. Ayaṃ dutiyo ānisaṃso sīlavato sīlasampadāya.',
             'english': 'Again, householders, for a virtuous person, accomplished in virtue, a good reputation spreads far and wide. This is the second benefit of one who is virtuous, accomplished in virtue.'},
            {'n': 4, 'pali_roman': 'Puna caparaṃ gahapatayo sīlavā sīlasampanno yaññadeva parisaṃ upasaṅkamati, yadi khattiyaparisaṃ yadi brāhmaṇaparisaṃ yadi gahapatiparisaṃ yadi samaṇaparisaṃ, visārado upasaṅkamati amaṅkubhūto. Ayaṃ tatiyo ānisaṃso sīlavato sīlasampadāya.',
             'english': 'Again, householders, a virtuous person, accomplished in virtue, approaches any assembly-whether of nobles, brahmins, householders, or ascetics-confidently and without embarrassment. This is the third benefit of one who is virtuous, accomplished in virtue.'},
            {'n': 5, 'pali_roman': 'Puna caparaṃ gahapatayo sīlavā sīlasampanno asammūḷho kālaṃ karoti. Ayaṃ catuttho ānisaṃso sīlavato sīlasampadāya.',
             'english': 'Again, householders, a virtuous person, accomplished in virtue, dies unconfused. This is the fourth benefit of one who is virtuous, accomplished in virtue.'},
            {'n': 6, 'pali_roman': 'Puna caparaṃ gahapatayo sīlavā sīlasampanno kāyassa bhedā paraṃ maraṇā sugatiṃ saggaṃ lokaṃ upapajjati. Ayaṃ pañcamo ānisaṃso sīlavato sīlasampadāya.',
             'english': 'Again, householders, a virtuous person, accomplished in virtue, after the breakup of the body, after death, is reborn in a good destination, in a heavenly world. This is the fifth benefit of one who is virtuous, accomplished in virtue.'},
            {'n': 7, 'pali_roman': 'Ime kho gahapatayo pañca ānisaṃsā sīlavato sīlasampadāyāti.',
             'english': 'These, householders, are the five benefits of one who is virtuous, accomplished in virtue.”'},
        ],
    }],
    # Line 4: the page sets "yaññadeva parisā upasaṅkamati" and the assembly
    # list out of order across lines and prints "pariṣaṃ" (with ṣ); the order
    # and spelling here follow the canonical text (parisaṃ). Flag for review.
    'review_notes': ["Line 4 is set out of order on the page and prints 'pariṣaṃ'; set here in reading order as 'parisaṃ'."],
})

# Bodhisattamātā Sutta: from scratchpad/bodhi.txt (photos p255–258).
MORE.append({
    "id": "owen-bodhisattamata-sutta",
    "title_thai": "",
    "title": "Bodhisattamātā Sutta",
    "title_english": "The 14 Qualities of the Buddha's Mother",
    "source_pages": "255–258",
    "intro": [],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchiṃ okkanto hoti cattāro devaputtā catuddisaṃ rakkhāya upagacchanti mā naṃ bodhisattaṃ vā bodhisattamātaraṃ vā manusso vā amanusso vā koci viheṭhesīti. Ayamettha dhammatā.",
                    "english": "“Bhikkhus, it is a natural law that when the Bodhisatta descends into his mother's womb, four deva sons from the four directions come to guard him, so that no human or non-human being may harm the Bodhisatta or his mother. This is the natural law in this case."
                },
                {
                    "n": 2,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchiṃ okkanto hoti pakatiyā sīlavatī bodhisattamātā hoti viratā pāṇātipātā viratā adinnādānā viratā kāmesumicchācārā viratā musāvādā viratā surāmerayamajjapamādaṭṭhānā. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta descends into his mother's womb, the mother of the Bodhisatta is by nature virtuous: she abstains from killing living beings, from taking what is not given, from sexual misconduct, from false speech, and from intoxicants that cause heedlessness. This is the natural law in this case."
                },
                {
                    "n": 3,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchiṃ okkanto hoti na bodhisattamātu purisesu mānasaṃ uppajjati kāmaguṇūpasaṃhitaṃ anatikammaniyā va bodhisattamātā hoti kenaci purisena rattacittena. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta descends into his mother's womb, no lustful thought connected with sensual pleasure arises in the Bodhisatta's mother toward men, and no man with lustful mind can approach her. This is the natural law in this case."
                },
                {
                    "n": 4,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchiṃ okkanto hoti lābhinī bodhisattamātā hoti pañcannaṃ kāmaguṇānaṃ sā pañcahi kāmaguṇehi samappitā samaṅgibhūtā paricāreti. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta descends into his mother's womb, the mother of the Bodhisatta becomes endowed with the five kinds of sensual pleasures, enjoying and being provided with them. This is the natural law in this case."
                },
                {
                    "n": 5,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchiṃ okkanto hoti na bodhisattamātu kocideva ābādho uppajjati sukhinī bodhisattamātā hoti akilantakāyā bodhisattañca bodhisattamātā tirokucchigataṃ passati sabbaṅgapaccaṅgaṃ ahīnindriyaṃ. Seyyathāpi bhikkhave maṇiveḷuriyo subho jātimā aṭṭhaṃso suparikammakato accho vippasanno sabbākārasampanno tatrassa suttaṃ āvutaṃ nīlaṃ vā pītaṃ vā lohitakaṃ vā odātaṃ vā paṇḍusuttaṃ vā tamenaṃ cakkhumā puriso hatthe karitvā paccavekkheyya ayaṃ kho maṇiveḷuriyo subho jātimā aṭṭhaṃso suparikammakato accho vippasanno sabbākārasampanno tatrassa suttaṃ āvutaṃ nīlaṃ vā pītaṃ vā lohitakaṃ vā odātaṃ vā paṇḍusuttaṃ vā evameva kho bhikkhave yadā bodhisatto mātu kucchiṃ okkanto hoti na bodhisattamātu kocideva ābādho uppajjati sukhinī bodhisattamātā hoti akilantakāyā bodhisattañca bodhisattamātā tirokucchigataṃ passati sabbaṅgapaccaṅgaṃ ahīnindriyaṃ. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta descends into his mother's womb, no illness arises in the Bodhisatta's mother. She is happy, free from bodily fatigue, and she can see the Bodhisatta within her womb, complete in all limbs and faculties. Just as a pure, well-polished beryl gem, clear and flawless, when a thread of blue, yellow, red, white, or brown is placed through it, a person with good eyesight can clearly see it, so too the Bodhisatta's mother sees the Bodhisatta in her womb, complete in all parts and faculties. This is the natural law in this case."
                },
                {
                    "n": 6,
                    "pali_roman": "Dhammatā esā bhikkhave sattāhajāte bodhisatte bodhisattamātā kālaṃ karoti tusitaṃ kāyaṃ upapajjati. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that seven days after the Bodhisatta is born, the mother of the Bodhisatta passes away and is reborn in the Tusita heaven. This is the natural law in this case."
                },
                {
                    "n": 7,
                    "pali_roman": "Dhammatā esā bhikkhave yathā aññā itthikā nava vā dasa vā māse gabbhaṃ kucchinā pariharitvā vijāyanti na hevaṃ bodhisattamātā vijāyati dasa eva māsāni bodhisattaṃ bodhisattamātā kucchinā pariharitvā vijāyati. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that while other women carry the fetus for nine or ten months and then give birth, the Bodhisatta's mother carries him for exactly ten months before giving birth. This is the natural law in this case."
                },
                {
                    "n": 8,
                    "pali_roman": "Dhammatā esā bhikkhave yathā aññā itthikā nisinnā vā nipannā vā vijāyanti na hevaṃ bodhisattaṃ bodhisattamātā vijāyati ṭhitā ca bodhisattaṃ bodhisattamātā vijāyati. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that while other women give birth sitting or lying down, the Bodhisatta's mother gives birth standing. This is the natural law in this case."
                },
                {
                    "n": 9,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchismā nikkhamati devā paṭhamaṃ paṭiggaṇhanti pacchā manussā. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta emerges from his mother's womb, devas first receive him, and only afterwards do humans. This is the natural law in this case."
                },
                {
                    "n": 10,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchismā nikkhamati appatto ca bodhisatto paṭhaviṃ hoti cattāro naṃ devaputtā paṭiggahetvā mātu purato ṭhapenti attamanā devi hohi mahesakkho te putto uppannoti. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta emerges from his mother's womb, before touching the ground, four deva sons receive him and place him before his mother, saying: ‘Rejoice, O queen! A great and mighty son has been born to you.’ This is the natural law in this case."
                },
                {
                    "n": 11,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchismā nikkhamati visado va nikkhamati amakkhito udakena amakkhito semhena amakkhito ruhirena amakkhito kenaci asucinā suddho visuddho. Seyyathāpi bhikkhave maṇiratanaṃ kāsike vathe nikkhittaṃ neva maṇiratanaṃ kāsikaṃ vatthaṃ makkheti napi kāsikaṃ vatthaṃ maṇiratanaṃ makkheti taṃ kissa hetu ubhinnaṃ suddhatta evameva kho bhikkhave yadā bodhisatto mātu kucchismā nikkhamati visado va nikkhamati amakkhito udakena amakkhito semhena amakkhito ruhirena amakkhito kenaci asucinā suddho visuddho. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta emerges from his mother's womb, he comes out pure, unstained by water, mucus, blood, or any impurity-clean and purified. Just as a jewel placed on a fine cloth does not stain the cloth, nor does the cloth stain the jewel, because both are pure, so too the Bodhisatta emerges pure and undefiled. This is the natural law in this case."
                },
                {
                    "n": 12,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchismā nikkhamati dve udakassa dhārā antalikkhā pātubhavanti ekā sītassa ekā uṇhassa yena bodhisattassa udakakiccaṃ karonti mātu ca. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta emerges from his mother's womb, two streams of water appear from the sky—one cool and one warm-by which the Bodhisatta and his mother are bathed. This is the natural law in this case."
                },
                {
                    "n": 13,
                    "pali_roman": "Dhammatā esā bhikkhave sampatijāto bodhisatto samehi pādehi patiṭṭhahitvā uttarena abhimukho sattapadavītihārena gacchati setamhi chatte anudhāriyamāne sabbā ca disā anuviloketi āsabhiñca vācaṃ bhāsati aggohamasmi lokassa jeṭṭhohamasmi lokassa seṭṭhohamasmi lokassa ayamantimā me jāti natthidāni punabbhavoti. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta is born, he stands firmly on his feet, faces north, takes seven steps, and with a white parasol held over him, surveys all directions and utters the noble declaration: ‘I am the foremost in the world, I am the highest in the world, I am the supreme in the world. This is my last birth; now there is no more becoming.’ This is the natural law in this case."
                },
                {
                    "n": 14,
                    "pali_roman": "Dhammatā esā bhikkhave yadā bodhisatto mātu kucchismā nikkhamati atha sadevakā loke samārake sabrahmake sassamaṇabrāhmaṇiyā pajāya sadevamanuṣṣāya appamāṇo oḷāro obhāso pātubhavati atikkammeva devānaṃ devānubhāvaṃ yāpi tā lokantarikā aghā asaṃvutā andhakāratimisā yatthapime candimasūriyā evaṃmahiddhikā evaṃmahānubhāvā ābhāya nānubhonti tatthapi appamāṇo oḷāro obhāso pātubhavati atikkammeva devānaṃ devānubhāvaṃ yepi tattha sattā upapannā tepi tenobhāsena aññamaññaṃ sañjānanti aññepi kira bho santi sattā idhūpapannāti ayañca dasasahassī lokadhātu saṅkampati sampakampati sampavedheti appamāṇo ca oḷāro obhāso loke pātubhavati atikkammeva devānaṃ devānubhāvaṃ. Ayamettha dhammatā.",
                    "english": "Bhikkhus, it is a natural law that when the Bodhisatta emerges from his mother's womb, a vast and immeasurable light appears in the world-surpassing even the splendor of the devas-throughout the world with its devas, Māras, Brahmās, ascetics, and brahmins, among gods and humans. Even in the dark, inter-world spaces where the sun and moon do not shine, that great light appears. Beings there perceive one another by that light, thinking: ‘Indeed, there are other beings here.’ And this ten-thousandfold world system trembles, shakes, and quakes, and a great, immeasurable radiance appears in the world, surpassing the divine splendor of the devas. This is the natural law in this case.”"
                }
            ]
        }
    ],
    "review_notes": [
        "Kept as printed: 'vathe' (standard vatthe), 'suddhatta', 'sadevamanuṣṣāya' (with ṣ), 'devi'."
    ]
})

# Four Holy Places: from scratchpad/holy.txt (photos p259–260).
MORE.append({
    "id": "owen-catu-samvejaniya-sutta",
    "title_thai": "",
    "title": "Jatu-Saṅvejanīya Sthāna Sutta",
    "title_english": "Four Holy Places of Pilgrimage",
    "source_pages": "259–260",
    "intro": [],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Pubbe bhante disāsu vassaṃ vutthā bhikkhū āgacchanti tathāgatadassanaṃ te mayaṃ labhāma manobhāvanīye bhikkhū dassanāya labhāma payirupāsanāya bhagavato pana mayaṃ bhante accayena na labhissāma manobhāvanīye bhikkhū dassanāya na labhissāma payirupāsanāyāti.",
                    "english": "“Bhante, formerly, monks who had spent the rains retreat in the various directions would come to see the Tathāgata. We would gain the opportunity to see those monks who inspire the mind and to attend upon them. But, Bhante, after the Blessed One has passed away, we will no longer have the opportunity to see such inspiring monks or to attend upon them."
                },
                {
                    "n": 2,
                    "pali_roman": "Cattārimāni ānanda saddhassa kulaputtassa dassanīyāni saṃvejanīyāni ṭhānāni. Katamāni cattāri.",
                    "english": "Ānanda, there are these four places that a faithful person should visit and look upon with a sense of reverence and spiritual urgency. What four?"
                },
                {
                    "n": 3,
                    "pali_roman": "Idha tathāgato jāto ti ānanda saddhassa kulaputtassa dassanīyaṃ saṃvejanīyaṃ ṭhānaṃ.",
                    "english": "Here the Tathāgata was born-this is a place that a faithful person should visit and contemplate with devotion."
                },
                {
                    "n": 4,
                    "pali_roman": "Idha tathāgato anuttaraṃ sammāsambodhiṃ abhisambuddho ti ānanda saddhassa kulaputtassa dassanīyaṃ saṃvejanīyaṃ ṭhānaṃ.",
                    "english": "Here the Tathāgata attained unsurpassed perfect enlightenment-this is a place that a faithful person should visit and contemplate with devotion."
                },
                {
                    "n": 5,
                    "pali_roman": "Idha tathāgatena anuttaraṃ dhammacakkaṃ pavattitaṃ ti ānanda saddhassa kulaputtassa dassanīyaṃ saṃvejanīyaṃ ṭhānaṃ.",
                    "english": "Here the Tathāgata set in motion the unsurpassed Wheel of Dhamma-this is a place that a faithful person should visit and contemplate with devotion."
                },
                {
                    "n": 6,
                    "pali_roman": "Idha tathāgato anupādisesāya nibbānadhātuyā parinibbuto ti ānanda saddhassa kulaputtassa dassanīyaṃ saṃvejanīyaṃ ṭhānaṃ.",
                    "english": "Here the Tathāgata passed away into the element of Nibbāna without remainder-this is a place that a faithful person should visit and contemplate with devotion."
                },
                {
                    "n": 7,
                    "pali_roman": "Imāni kho ānanda cattāri saddhassa kulaputtassa dassanīyāni saṃvejanīyāni ṭhānāni.",
                    "english": "These, Ānanda, are the four places that a faithful person should visit and look upon with reverence and spiritual urgency."
                },
                {
                    "n": 8,
                    "pali_roman": "Āgamissanti kho ānanda saddhā bhikkhū bhikkhuniyo upāsakā upāsikāyo idha tathāgato jāto ti pi idha tathāgato anuttaraṃ sammāsambodhiṃ abhisambuddho ti pi idha tathāgatena anuttaraṃ dhammacakkaṃ pavattitaṃ ti pi idha tathāgato anupādisesāya nibbānadhātuyā parinibbuto ti pi.",
                    "english": "There will come, Ānanda, faithful monks, nuns, laymen, and laywomen who will visit these places, saying: ‘Here the Tathāgata was born,’ ‘Here the Tathāgata attained enlightenment,’ ‘Here the Tathāgata set in motion the Wheel of Dhamma,’ and ‘Here the Tathāgata attained Parinibbāna.’"
                },
                {
                    "n": 9,
                    "pali_roman": "Ye hi keci ānanda cetiyacārikaṃ āhiṇḍantā pasannacittā kālaṃ karissanti sabbe te kāyassa bhedā paraṃ maraṇā sugatiṃ saggaṃ lokaṃ upapajjissantīti.",
                    "english": "And those who undertake such pilgrimages with a faithful and serene mind, and who pass away while doing so, all of them, at the breaking up of the body after death, will be reborn in a good destination, in a heavenly world.”"
                }
            ]
        }
    ],
    "review_notes": [
        "Title kept as printed ('Jatu-Saṅvejanīya Sthāna'); the Pali text itself reads 'cattāri … saṃvejanīyāni ṭhānāni'."
    ]
})

# Bhūmicāla Sutta: from scratchpad/bhumi.txt (photos p261–262).
MORE.append({
    "id": "owen-bhumicala-sutta",
    "title_thai": "",
    "title": "Bhūmicāla Sutta",
    "title_english": "The Eight Causes of an Earthquake",
    "source_pages": "261–262",
    "intro": [],
    "sections": [
        {
            "heading": "",
            "lines": [
                {
                    "n": 1,
                    "pali_roman": "Aṭṭha kho ime ānanda hetū aṭṭha paccayā mahato bhūmicālassa pātubhāvāya. Katame aṭṭha.",
                    "english": "“Ānanda, there are these eight causes and conditions for the occurrence of a great earthquake. What eight?"
                },
                {
                    "n": 2,
                    "pali_roman": "Idha ānanda mahāpathavī udake patiṭṭhitā udakaṃ vāte patiṭṭhitaṃ vāto ākāsaṭṭho hoti. So kho ānanda samayo yaṃ mahāvātā vāyanti. Mahāvātā vāyantā udakaṃ kampenti. Udakaṃ kampamānaṃ pathaviṃ kampeti. Ayaṃ paṭhamo hetu paṭhamo paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Here, Ānanda, the great earth rests upon water, the water rests upon air, and the air rests upon space. At a time when powerful winds blow, the winds stir the water; when the water is stirred, it shakes the earth. This is the first cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 3,
                    "pali_roman": "Puna caparaṃ ānanda samaṇo vā brāhmaṇo vā iddhimā cetovasippatto devo vā mahiddhiko mahānubhāvo tassa pathavīsaññā parittā bhāvitā hoti appamāṇā āposaññā. So imaṃ pathaviṃ kampeti saṅkampeti sampakampeti sampavedheti. Ayaṃ dutiyo hetu dutiyo paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Again, Ānanda, there may be an ascetic or brahmin with spiritual power, mastery of mind, or a powerful deity of great might and influence. If such a being has developed limited perception of earth and vast perception of water, he can shake, quake, and agitate the earth. This is the second cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 4,
                    "pali_roman": "Puna caparaṃ ānanda yadā bodhisatto tusitā kāyā cavitvā sato sampajāno mātu kucchiṃ okkamati tadā pathavī kampati saṅkampati sampakampati sampavedheti. Ayaṃ tatiyo hetu tatiyo paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Again, Ānanda, when the Bodhisatta passes away from the Tusita heaven and mindfully and clearly comprehending enters his mother's womb, at that time the earth shakes, quakes, trembles, and is agitated. This is the third cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 5,
                    "pali_roman": "Puna caparaṃ ānanda yadā bodhisatto sato sampajāno mātu kucchimha nikkhamati tadā pathavī kampati saṅkampati sampakampati sampavedheti. Ayaṃ catuttho hetu catuttho paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Again, Ānanda, when the Bodhisatta mindfully and clearly comprehending emerges from his mother's womb, at that time the earth shakes, quakes, trembles, and is agitated. This is the fourth cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 6,
                    "pali_roman": "Puna caparaṃ ānanda yadā tathāgato anuttaraṃ sammāsambodhiṃ abhisambujjhati tadā pathavī kampati saṅkampati sampakampati sampavedheti. Ayaṃ pañcamo hetu pañcamo paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Again, Ānanda, when the Tathāgata attains unsurpassed perfect enlightenment, at that time the earth shakes, quakes, trembles, and is agitated. This is the fifth cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 7,
                    "pali_roman": "Puna caparaṃ ānanda yadā tathāgato anuttaraṃ dhammacakkaṃ pavatteti tadā pathavī kampati saṅkampati sampakampati sampavedheti. Ayaṃ chaṭṭho hetu chaṭṭho paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Again, Ānanda, when the Tathāgata sets in motion the unsurpassed Wheel of Dhamma, at that time the earth shakes, quakes, trembles, and is agitated. This is the sixth cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 8,
                    "pali_roman": "Puna caparaṃ ānanda yadā tathāgato sato sampajāno āyusaṅkhāraṃ ossajjati tadā pathavī kampati saṅkampati sampakampati sampavedheti. Ayaṃ sattamo hetu sattamo paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Again, Ānanda, when the Tathāgata mindfully and clearly comprehending relinquishes the life-force, at that time the earth shakes, quakes, trembles, and is agitated. This is the seventh cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 9,
                    "pali_roman": "Puna caparaṃ ānanda yadā tathāgato anupādisesāya nibbānadhātuyā parinibbāyati tadā pathavī kampati saṅkampati sampakampati sampavedheti. Ayaṃ aṭṭhamo hetu aṭṭhamo paccayo mahato bhūmicālassa pātubhāvāya.",
                    "english": "Again, Ānanda, when the Tathāgata passes away into the element of Nibbāna without remainder, at that time the earth shakes, quakes, trembles, and is agitated. This is the eighth cause and condition for the occurrence of a great earthquake."
                },
                {
                    "n": 10,
                    "pali_roman": "Ime kho ānanda aṭṭha hetū aṭṭha paccayā mahato bhūmicālassa pātubhāvāyāti.",
                    "english": "These, Ānanda, are the eight causes and conditions for the occurrence of a great earthquake.”"
                }
            ]
        }
    ]
})

# ── (more chants are appended here, in Ajarn Owen's page order) ──


# ── The Thai-script Pali line for the chants entered from romanised text ──
# Made by scripts/pali_to_thai.py, which reproduces the temple book's own
# spelling for 98.8% of the words already in chanting.py. Lines that already
# have a Thai-script line (the Sekhiya, taken from the temple book, and the
# Confession) keep it. Every line made here is a draft for a monk to check.
def _add_thai_script():
    import os
    sys_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    import sys
    if sys_path not in sys.path:
        sys.path.insert(0, sys_path)
    from pali_to_thai import convert
    for chant in MORE:
        plain = chant['id'] == 'owen-kalama-sutta'
        lines = list(chant.get('intro', []))
        for section in chant['sections']:
            lines += section['lines']
            if section.get('closing'):
                lines.append(section['closing'])
        for line in lines:
            if line.get('pali_roman') and not line.get('pali'):
                line['pali'] = convert(line['pali_roman'], plain=plain)


_add_thai_script()


def _first_page(chant):
    return int(chant['source_pages'].split('–')[0].split('-')[0])


OWEN_CHANTS = sorted([SEKHIYA, APATTI_DESANA] + MORE, key=_first_page)
