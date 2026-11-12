"""Chants from the Amaravati chanting book, printed as their own Part
(Josh, 2026-11-12).

Why a separate file: `chanting.py` is the Wat Mahathat United Kingdom
chanting book, page for page, and nothing from another book is mixed into it
(the same rule as chanting_owen.py). These are the reflections that are
commonly chanted after morning and evening chanting but that the temple book
does not print.

Source: "Chanting, Volume One: Morning and Evening Chanting (Pūjā) and
Reflections", Pāli | English, Amaravati Buddhist Monastery, 2015. Typed from
Josh's photographs of pages 40-41, 49, 85-90 and 115-119
(Downloads/IMG_1250-1254 and IMG_1257-1265). Accent marks were read from
photographs and need proofreading against the printed book. Spelling is the
book's own, including where it is not consistent (mayam/mayaṃ,
tranquillizing/tranquilizing).

LICENCE: the book is CC BY-NC-ND 3.0 (its page 146, IMG_1266-1267). Free
copying and distribution are allowed with credit, not for commercial use, and
with NO alterations. So the text is printed exactly as the book has it, the
credit and licence are printed with it, and it is NOT put in the paid app.
The Thai-script line is our addition, not theirs: whether that counts as an
alteration is a question for Amaravati Publications (publications@amaravati.org).

The Amaravati book prints romanised Pali and English only. The Thai-script
line is made by scripts/pali_to_thai.py, like Ajarn Owen's chants, and needs
a monk's check.

Shape of a chant:
    id, title, title_english, source_pages, first_line
    leader: the bracketed line the leader chants alone ("Handa mayaṃ ...")
    groups: list of {'pali': [roman lines], 'english': [lines]}
        Where the book sets Pali and English line by line, each group is one
        Pali line and its English. Where it sets the Pali on one page and a
        chanted English version on the facing page (Universal Well-Being),
        a group is one stanza of each.
    continues: pages not yet entered, or None (all are entered now)
"""

AMARAVATI_BOOK = 'the Amaravati chanting book'
AMARAVATI_LICENCE = ('Chanting, Volume One, © 2015 Amaravati Buddhist Monastery, '
                     'Amaravati Publications. Licensed under Creative Commons '
                     'Attribution-NonCommercial-NoDerivs 3.0 Unported, '
                     'creativecommons.org/licenses/by-nc-nd/3.0/. Offered for free '
                     'distribution; please do not sell. Also available free from '
                     'forestsanghapublications.org.')
AMARAVATI_BOOK_FULL = ('Chanting, Volume One: Morning and Evening Chanting (Pūjā) '
                       'and Reflections, Amaravati Buddhist Monastery')


def _pairs(*rows):
    return [{'pali': [p], 'english': [e] if isinstance(e, str) else list(e)}
            for p, e in rows]


UNIVERSAL_WELL_BEING = {
    'id': 'amaravati-universal-well-being',
    'title': 'Mettāpharaṇa',
    'title_english': 'Reflection on Universal Well-Being',
    'source_pages': '40–41',
    'leader': {
        'pali_roman': 'Handa mayam mettāpharaṇaṃ karomase',
        'english': 'Now let us chant the reflections on universal well-being.',
    },
    # The Pali (page 40) and a chanted English version (page 41) face each
    # other; they are paired here stanza by stanza, as the pages are set.
    'groups': [
        {'pali': ['Ahaṃ sukhito homi', 'Niddukkho homi', 'Avero homi',
                  'Abyāpajjho homi', 'Anīgho homi', 'Sukhī attānaṃ pariharāmi'],
         'english': ['May I abide in well-being,', 'In freedom from affliction,',
                     'In freedom from hostility,', 'In freedom from ill-will,',
                     'In freedom from anxiety,', 'And may I maintain well-being in myself.']},
        {'pali': ['Sabbe sattā sukhitā hontu', 'Sabbe sattā averā hontu',
                  'Sabbe sattā abyāpajjhā hontu', 'Sabbe sattā anīghā hontu',
                  'Sabbe sattā sukhī attānaṃ pariharantu'],
         'english': ['May everyone abide in well-being,', 'In freedom from hostility,',
                     'In freedom from ill-will,', 'In freedom from anxiety, and may they',
                     'Maintain well-being in themselves.']},
        {'pali': ['Sabbe sattā sabbadukkhā pamuccantu'],
         'english': ['May all beings be released from all suffering.']},
        {'pali': ['Sabbe sattā laddha-sampattito mā vigacchantu'],
         'english': ['And may they not be parted from the good fortune they have attained.']},
        {'pali': ['Sabbe sattā kammassakā kammadāyādā kammayonī',
                  'kammabandhū kammapaṭisaraṇā',
                  'Yaṃ kammaṃ karissanti', 'Kalyāṇaṃ vā pāpakaṃ vā',
                  'Tassa dāyādā bhavissanti'],
         'english': ['When they act upon intention,',
                     'All beings are the owners of their action and inherit its results.',
                     'Their future is born from such action, companion to such action,',
                     'And its results will be their home.',
                     'All actions with intention,', 'Be they skilful or harmful —',
                     'Of such acts they will be the heirs.']},
    ],
    'continues': None,
}

UNCONDITIONED = {
    'id': 'amaravati-unconditioned',
    'title': 'Nibbāna Sutta',
    'title_english': 'Reflection on the Unconditioned',
    'source_pages': '49',
    'leader': {'pali_roman': 'Handa mayaṃ nibbāna-sutta-pāṭhaṃ bhaṇāmase'},
    'groups': _pairs(
        ('Atthi bhikkhave ajātaṃ abhūtaṃ akataṃ asaṅkhataṃ',
         'There is an Unborn, Unoriginated, Uncreated and Unformed.'),
        ('No cetaṃ bhikkhave abhavissa ajātaṃ abhūtaṃ akataṃ asaṅkhataṃ',
         'If there was not this Unborn, this Unoriginated, this Uncreated, this Unformed,'),
        ('Na yidaṃ jātassa bhūtassa katassa saṅkhatassa nissaraṇaṃ paññāyetha',
         'Freedom from the world of the born, the originated, the created, the formed '
         'would not be possible.'),
        ('Yasmā ca kho bhikkhave atthi ajātaṃ abhūtaṃ akataṃ asaṅkhataṃ',
         'But since there is an Unborn, Unoriginated, Uncreated and Unformed,'),
        ('Tasmā jātassa bhūtassa katassa saṅkhatassa nissaraṇaṃ paññāyati',
         'Therefore is freedom possible from the world of the born, the originated, '
         'the created and the formed.'),
    ),
    'continues': None,
}

MINDFULNESS_OF_BREATHING = {
    'id': 'amaravati-mindfulness-of-breathing',
    'title': 'Ānāpānassati Sutta',
    'title_english': 'The Teaching on Mindfulness of Breathing',
    'source_pages': '85–90',
    'leader': {'pali_roman': 'Handa mayam ānāpānassati-sutta-pāṭham bhaṇāmase'},
    # The book prints "tranquillizing" for the bodily formations and
    # "tranquilizing" for the mental ones; both kept as printed.
    'groups': _pairs(
        ('Ānāpānassati bhikkhave bhāvitā bahulīkatā',
         'Bhikkhus, when mindfulness of breathing is developed and cultivated'),
        ('Mahapphalā hoti mahānisaṃsā', 'It is of great fruit and great benefit;'),
        ('Ānāpānassati bhikkhave bhāvitā bahulīkatā',
         'When mindfulness of breathing is developed and cultivated'),
        ('Cattāro satipaṭṭhāne paripūreti', 'It fulfills the Four Foundations of Mindfulness;'),
        ('Cattāro satipaṭṭhānā bhāvitā bahulīkatā',
         'When the Four Foundations of Mindfulness are developed and cultivated'),
        ('Satta-bojjhaṅge paripūrenti', 'They fulfill the Seven Factors of Awakening;'),
        ('Satta-bojjhaṅgā bhāvitā bahulīkatā',
         'When the Seven Factors of Awakening are developed and cultivated'),
        ('Vijjā-vimuttiṃ paripūrenti', 'They fulfill true knowledge and deliverance.'),
        ('Kathaṃ bhāvitā ca bhikkhave ānāpānassati kathaṃ bahulīkatā',
         'And how, bhikkhus, is mindfulness of breathing developed and cultivated'),
        ('Mahapphalā hoti mahānisaṃsā', 'So that it is of great fruit and great benefit?'),
        ('Idha bhikkhave bhikkhu', 'Here, bhikkhus, a bhikkhu,'),
        ('Arañña-gato vā', 'Gone to the forest,'),
        ('Rukkha-mūla-gato vā', 'To the foot of a tree'),
        ('Suññāgāra-gato vā', 'Or to an empty hut.'),
        ('Nisīdati pallaṅkaṃ ābhujitvā', 'Sits down having crossed his legs,'),
        ('Ujuṃ kāyaṃ paṇidhāya parimukhaṃ satiṃ upaṭṭhapetvā',
         'Sets his body erect, having established mindfulness in front of him.'),
        ('So sato’va assasati sato’va passasati',
         'Ever mindful he breathes in; mindful he breathes out.'),
        ('Dīghaṃ vā assasanto dīghaṃ assasāmī’ti pajānāti',
         'Breathing in long, he knows ‘I breathe in long’;'),
        ('Dīghaṃ vā passasanto dīghaṃ passasāmī’ti pajānāti',
         'Breathing out long, he knows ‘I breathe out long’;'),
        ('Rassaṃ vā assasanto rassaṃ assasāmī’ti pajānāti',
         'Breathing in short, he knows ‘I breathe in short’;'),
        ('Rassaṃ vā passasanto rassaṃ passasāmī’ti pajānāti',
         'Breathing out short, he knows ‘I breathe out short’.'),
        ('Sabba-kāya-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in experiencing the whole body’.'),
        ('Sabba-kāya-paṭisaṃvedī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out experiencing the whole body’.'),
        ('Passambhayaṃ kāya-saṅkhāraṃ assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in tranquillizing the bodily formations’.'),
        ('Passambhayaṃ kāya-saṅkhāraṃ passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out tranquillizing the bodily formations’.'),
        ('Pīti-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in experiencing rapture’.'),
        ('Pīti-paṭisaṃvedī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out experiencing rapture’.'),
        ('Sukha-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in experiencing pleasure’'),
        ('Sukha-paṭisaṃvedī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out experiencing pleasure’.'),
        ('Citta-saṅkhāra-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in experiencing the mental formations’.'),
        ('Citta-saṅkhāra-paṭisaṃvedī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out experiencing the mental formations’.'),
        ('Passambhayaṃ citta-saṅkhāraṃ assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in tranquilizing the mental formations’.'),
        ('Passambhayaṃ citta-saṅkhāraṃ passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out tranquilizing the mental formations’.'),
        ('Citta-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in experiencing the mind’.'),
        ('Citta-paṭisaṃvedī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out experiencing the mind’.'),
        ('Abhippamodayaṃ cittaṃ assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in gladdening the mind’.'),
        ('Abhippamodayaṃ cittaṃ passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out gladdening the mind’.'),
        ('Samādahaṃ cittaṃ assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in concentrating the mind’'),
        ('Samādahaṃ cittaṃ passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out concentrating the mind’.'),
        ('Vimocayaṃ cittaṃ assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in liberating the mind’.'),
        ('Vimocayaṃ cittaṃ passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out liberating the mind’.'),
        ('Aniccānupassī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in contemplating impermanence’.'),
        ('Aniccānupassī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out contemplating impermanence’.'),
        ('Virāgānupassī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in contemplating the fading away of passions’.'),
        ('Virāgānupassī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out contemplating the fading away of passions’.'),
        ('Nirodhānupassī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in contemplating cessation’.'),
        ('Nirodhānupassī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out contemplating cessation’.'),
        ('Paṭinissaggānupassī assasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe in contemplating relinquishment’.'),
        ('Paṭinissaggānupassī passasissāmī’ti sikkhati',
         'He trains thus: ‘I shall breathe out contemplating relinquishment’.'),
        ('Evaṃ bhāvitā kho bhikkhave ānāpānassati evaṃ bahulīkatā',
         'Bhikkhus, that is how mindfulness of breathing is developed and cultivated'),
        ('Mahapphalā hoti mahānisaṃsā’ti', 'So that it is of great fruit and great benefit.'),
    ),
    'continues': None,
}

STRIVING = {
    'id': 'amaravati-striving',
    'title': 'Dhammapahaṃsāna Pāṭha',
    'title_english': 'The Teaching on Striving According to Dhamma',
    'source_pages': '115–119',
    'leader': {'pali_roman': 'Handa mayaṃ dhamma-pahaṃsāna-pāṭham bhaṇāmase'},
    'groups': _pairs(
        ('Evaṃ svākkhāto bhikkhave mayā dhammo',
         'Bhikkhus, the Dhamma has thus been well expounded by me,'),
        ('Uttāno', 'Elucidated,'),
        ('Vivaṭo', 'Disclosed,'),
        ('Pakāsito', 'Revealed,'),
        ('Chinna-pilotiko', 'And stripped of patchwork —'),
        ('Alam-eva saddhā-pabbajitena kula-puttena viriyaṃ ārabhituṃ',
         'This is enough for a clansman, who has gone forth out of faith, to arouse '
         'his energy thus:'),
        ('Kāmaṃ taco ca nahāru ca aṭṭhi ca avasissatu',
         '‘Willingly let only my skin, sinews and bones remain,'),
        ('Sarīre upasussatu maṃsa-lohitaṃ',
         'And let the flesh and blood in this body wither away.'),
        ('Yaṃ taṃ', 'As long as whatever is to be attained'),
        ('Purisa-thāmena', 'By human strength,'),
        ('Purisa-viriyena', 'By human energy,'),
        ('Purisa-parakkamena', 'By human effort,'),
        ('Pattabbaṃ na taṃ apāpuṇitvā', 'Has not been attained,'),
        ('Viriyassa saṇṭhānaṃ bhavissatī’ti', 'Let not my efforts stand still.’'),
        ('Dukkhaṃ bhikkhave kusīto viharati', 'Bhikkhus, the lazy person dwells in suffering,'),
        ('Vokiṇṇo pāpakehi akusalehi dhammehi', 'Soiled by evil, unwholesome states'),
        ('Mahantañca sadatthaṃ parihāpeti', 'And great is the personal good that he neglects.'),
        ('Āraddha-viriyo ca kho bhikkhave sukhaṃ viharati',
         'The energetic person though dwells happily,'),
        ('Pavivitto pāpakehi akusalehi dhammehi', 'Well withdrawn from unwholesome states'),
        ('Mahantañca sadatthaṃ paripūreti', 'And great is the personal good that he achieves.'),
        ('Na bhikkhave hīnena aggassa patti hoti',
         'Bhikkhus, it is not by lower means that the supreme is attained'),
        ('Aggena ca kho bhikkhave aggassa patti hoti',
         'But, bhikkhus, it is by the supreme that the supreme is attained.'),
        ('Maṇḍapeyyam-idaṃ bhikkhave brahmacariyaṃ',
         'Bhikkhus, this holy life is like the cream of the milk:'),
        ('Satthā sammukhī-bhūto', 'The Teacher is present,'),
        ('Tasmātiha bhikkhave viriyaṃ ārabhatha',
         'Therefore, bhikkhus, start to arouse your energy'),
        ('Appattassa pattiyā', 'For the attainment of the as yet unattained,'),
        ('Anadhigatassa adhigamāya', 'For the achievement of the as yet unachieved,'),
        ('Asacchikatassa sacchikiriyāya', 'For the realization of the as yet unrealized.'),
        ('Evaṃ no ayaṃ amhākaṃ pabbajjā avaṅkatā avañjhā bhavissati',
         'Thinking, in such a way: ‘Our Going Forth will not be barren'),
        ('Saphalā sa-udrayā', 'But will become fruitful and fertile,'),
        ('Yesaṃ mayaṃ paribhuñjāma cīvara-piṇḍapāta-senāsana-'
         'gilānappaccaya-bhesajja-parikkhāraṃ tesaṃ te kārā amhesu',
         'And all our use of robes, almsfood, lodgings, and medicinal requisites, '
         'given by others for our support,'),
        ('Mahapphalā bhavissanti mahānisaṃsā’ti',
         'Will reward them with great fruit and great benefit.’'),
        ('Evaṃ hi vo bhikkhave sikkhitabbaṃ', 'Bhikkhus, you should train yourselves thus:'),
        ('Att’atthaṃ vā hi bhikkhave sampassamānena', 'Considering your own good,'),
        ('Alam-eva appamādena sampādetuṃ',
         'It is enough to strive for the goal without negligence;'),
        ('Par’atthaṃ vā hi bhikkhave sampassamānena', 'Bhikkhus, considering the good of others,'),
        ('Alam-eva appamādena sampādetuṃ',
         'It is enough to strive for the goal without negligence;'),
        ('Ubhay’atthaṃ vā hi bhikkhave sampassamānena', 'Bhikkhus, considering the good of both,'),
        ('Alam-eva appamādena sampādetun’ti',
         'It is enough to strive for the goal without negligence.'),
    ),
    'continues': None,
}

AMARAVATI_CHANTS = [UNIVERSAL_WELL_BEING, UNCONDITIONED, MINDFULNESS_OF_BREATHING, STRIVING]


def _add_thai_script():
    """The Thai-script Pali line, made the same way as Ajarn Owen's."""
    import os
    import sys
    scripts = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from pali_to_thai import convert
    for chant in AMARAVATI_CHANTS:
        # plain=True reads the book's word-final m (mayam, pāṭham) as ṃ, so
        # the Thai line says มะยัง as every Thai temple chants it.
        chant['leader']['pali'] = convert(chant['leader']['pali_roman'], plain=True)
        for group in chant['groups']:
            group['pali_thai'] = [convert(line) for line in group['pali']]
        chant['first_line'] = chant['groups'][0]['pali'][0]


_add_thai_script()
