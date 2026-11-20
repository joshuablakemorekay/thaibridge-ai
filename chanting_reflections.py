"""Reflections chanted after morning and evening chanting, printed as their
own Part (Josh, 2026-11-12).

Why a separate file: `chanting.py` is the Wat Mahathat United Kingdom
chanting book, page for page, and nothing from another book is mixed into it
(the same rule as chanting_owen.py). These are reflections that are commonly
chanted after morning and evening chanting but that the temple book does not
print.

The Pali lines were first typed from Josh's photographs of another
monastery's chanting book (Downloads/IMG_1250-1254 and IMG_1257-1265).
Accent marks were read from photographs and need proofreading. Spelling
follows those pages, including where it is not consistent (mayam/mayaṃ).

ENGLISH: this edition's own translation, made directly from the Pali
(Josh, 2026-11-20). It replaced the other book's English so that this Part
no longer reproduces anyone else's translation, and the book prints no
credit or licence for it. It is a DRAFT and needs checking by a teacher or
a monk, like every other English line marked as this edition's.

The Thai-script line is made by scripts/pali_to_thai.py, like Ajarn Owen's
chants, and also needs a monk's check.

Shape of a chant:
    id, title, title_english, first_line
    leader: the line the leader chants alone ("Handa mayaṃ ...")
    groups: list of {'pali': [roman lines], 'english': [lines]}, one Pali
        line and its English per group.
    continues: pages not yet entered, or None (all are entered now)
"""

PART_TITLE = 'Reflections after morning and evening chanting'


def _pairs(*rows):
    return [{'pali': [p], 'english': [e] if isinstance(e, str) else list(e)}
            for p, e in rows]


UNIVERSAL_WELL_BEING = {
    'id': 'reflection-universal-well-being',
    'title': 'Mettāpharaṇa',
    'title_english': 'Spreading Loving-Kindness',
    'leader': {
        'pali_roman': 'Handa mayam mettāpharaṇaṃ karomase',
        'english': 'Now let us spread loving-kindness.',
    },
    'groups': _pairs(
        ('Ahaṃ sukhito homi', 'May I be happy.'),
        ('Niddukkho homi', 'May I be free from suffering.'),
        ('Avero homi', 'May I be free from enmity.'),
        ('Abyāpajjho homi', 'May I be free from ill will.'),
        ('Anīgho homi', 'May I be free from trouble.'),
        ('Sukhī attānaṃ pariharāmi', 'May I look after myself with ease.'),
        ('Sabbe sattā sukhitā hontu', 'May all beings be happy.'),
        ('Sabbe sattā averā hontu', 'May all beings be free from enmity.'),
        ('Sabbe sattā abyāpajjhā hontu', 'May all beings be free from ill will.'),
        ('Sabbe sattā anīghā hontu', 'May all beings be free from trouble.'),
        ('Sabbe sattā sukhī attānaṃ pariharantu',
         'May all beings look after themselves with ease.'),
        ('Sabbe sattā sabbadukkhā pamuccantu',
         'May all beings be freed from every kind of suffering.'),
        ('Sabbe sattā laddha-sampattito mā vigacchantu',
         'May all beings not lose the good things they have gained.'),
        ('Sabbe sattā kammassakā kammadāyādā kammayonī',
         'All beings own their kamma, are heirs to their kamma, are born of their kamma,'),
        ('kammabandhū kammapaṭisaraṇā',
         'are bound to their kamma, and have their kamma as their refuge.'),
        ('Yaṃ kammaṃ karissanti', 'Whatever kamma they do,'),
        ('Kalyāṇaṃ vā pāpakaṃ vā', 'whether good or bad,'),
        ('Tassa dāyādā bhavissanti', 'of that they will be the heirs.'),
    ),
    'continues': None,
}

UNCONDITIONED = {
    'id': 'reflection-unconditioned',
    'title': 'Nibbāna Sutta',
    'title_english': 'The Discourse on Nibbāna',
    'leader': {'pali_roman': 'Handa mayaṃ nibbāna-sutta-pāṭhaṃ bhaṇāmase'},
    'groups': _pairs(
        ('Atthi bhikkhave ajātaṃ abhūtaṃ akataṃ asaṅkhataṃ',
         'Monks, there is that which is not born, not come to be, not made, not conditioned.'),
        ('No cetaṃ bhikkhave abhavissa ajātaṃ abhūtaṃ akataṃ asaṅkhataṃ',
         'Monks, if there were not that which is not born, not come to be, not made, '
         'not conditioned,'),
        ('Na yidaṃ jātassa bhūtassa katassa saṅkhatassa nissaraṇaṃ paññāyetha',
         'no way out would be known here from what is born, come to be, made and conditioned.'),
        ('Yasmā ca kho bhikkhave atthi ajātaṃ abhūtaṃ akataṃ asaṅkhataṃ',
         'But because, monks, there is that which is not born, not come to be, not made, '
         'not conditioned,'),
        ('Tasmā jātassa bhūtassa katassa saṅkhatassa nissaraṇaṃ paññāyati',
         'a way out is known from what is born, come to be, made and conditioned.'),
    ),
    'continues': None,
}

MINDFULNESS_OF_BREATHING = {
    'id': 'reflection-mindfulness-of-breathing',
    'title': 'Ānāpānassati Sutta',
    'title_english': 'The Discourse on Mindfulness of Breathing',
    'leader': {'pali_roman': 'Handa mayam ānāpānassati-sutta-pāṭham bhaṇāmase'},
    'groups': _pairs(
        ('Ānāpānassati bhikkhave bhāvitā bahulīkatā',
         'Monks, mindfulness of breathing, when developed and practised often,'),
        ('Mahapphalā hoti mahānisaṃsā', 'brings great fruit and great reward.'),
        ('Ānāpānassati bhikkhave bhāvitā bahulīkatā',
         'Monks, mindfulness of breathing, when developed and practised often,'),
        ('Cattāro satipaṭṭhāne paripūreti',
         'brings the four foundations of mindfulness to completion.'),
        ('Cattāro satipaṭṭhānā bhāvitā bahulīkatā',
         'The four foundations of mindfulness, when developed and practised often,'),
        ('Satta-bojjhaṅge paripūrenti',
         'bring the seven factors of awakening to completion.'),
        ('Satta-bojjhaṅgā bhāvitā bahulīkatā',
         'The seven factors of awakening, when developed and practised often,'),
        ('Vijjā-vimuttiṃ paripūrenti', 'bring true knowledge and release to completion.'),
        ('Kathaṃ bhāvitā ca bhikkhave ānāpānassati kathaṃ bahulīkatā',
         'And how, monks, is mindfulness of breathing developed, how is it practised often,'),
        ('Mahapphalā hoti mahānisaṃsā', 'so that it brings great fruit and great reward?'),
        ('Idha bhikkhave bhikkhu', 'Here, monks, a monk'),
        ('Arañña-gato vā', 'who has gone into the forest,'),
        ('Rukkha-mūla-gato vā', 'or to the root of a tree,'),
        ('Suññāgāra-gato vā', 'or to an empty dwelling,'),
        ('Nisīdati pallaṅkaṃ ābhujitvā', 'sits down with his legs folded crosswise,'),
        ('Ujuṃ kāyaṃ paṇidhāya parimukhaṃ satiṃ upaṭṭhapetvā',
         'holds his body upright, and sets mindfulness to the fore.'),
        ('So sato’va assasati sato’va passasati',
         'Simply mindful, he breathes in; simply mindful, he breathes out.'),
        ('Dīghaṃ vā assasanto dīghaṃ assasāmī’ti pajānāti',
         'Breathing in a long breath, he understands, ‘I am breathing in a long breath’;'),
        ('Dīghaṃ vā passasanto dīghaṃ passasāmī’ti pajānāti',
         'breathing out a long breath, he understands, ‘I am breathing out a long breath’;'),
        ('Rassaṃ vā assasanto rassaṃ assasāmī’ti pajānāti',
         'breathing in a short breath, he understands, ‘I am breathing in a short breath’;'),
        ('Rassaṃ vā passasanto rassaṃ passasāmī’ti pajānāti',
         'breathing out a short breath, he understands, ‘I am breathing out a short breath’.'),
        ('Sabba-kāya-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains: ‘Feeling the whole body, I will breathe in’;'),
        ('Sabba-kāya-paṭisaṃvedī passasissāmī’ti sikkhati',
         'he trains: ‘Feeling the whole body, I will breathe out’.'),
        ('Passambhayaṃ kāya-saṅkhāraṃ assasissāmī’ti sikkhati',
         'He trains: ‘Calming the activity of the body, I will breathe in’;'),
        ('Passambhayaṃ kāya-saṅkhāraṃ passasissāmī’ti sikkhati',
         'he trains: ‘Calming the activity of the body, I will breathe out’.'),
        ('Pīti-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains: ‘Feeling joy, I will breathe in’;'),
        ('Pīti-paṭisaṃvedī passasissāmī’ti sikkhati',
         'he trains: ‘Feeling joy, I will breathe out’.'),
        ('Sukha-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains: ‘Feeling happiness, I will breathe in’;'),
        ('Sukha-paṭisaṃvedī passasissāmī’ti sikkhati',
         'he trains: ‘Feeling happiness, I will breathe out’.'),
        ('Citta-saṅkhāra-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains: ‘Feeling the activity of the mind, I will breathe in’;'),
        ('Citta-saṅkhāra-paṭisaṃvedī passasissāmī’ti sikkhati',
         'he trains: ‘Feeling the activity of the mind, I will breathe out’.'),
        ('Passambhayaṃ citta-saṅkhāraṃ assasissāmī’ti sikkhati',
         'He trains: ‘Calming the activity of the mind, I will breathe in’;'),
        ('Passambhayaṃ citta-saṅkhāraṃ passasissāmī’ti sikkhati',
         'he trains: ‘Calming the activity of the mind, I will breathe out’.'),
        ('Citta-paṭisaṃvedī assasissāmī’ti sikkhati',
         'He trains: ‘Feeling the mind, I will breathe in’;'),
        ('Citta-paṭisaṃvedī passasissāmī’ti sikkhati',
         'he trains: ‘Feeling the mind, I will breathe out’.'),
        ('Abhippamodayaṃ cittaṃ assasissāmī’ti sikkhati',
         'He trains: ‘Making the mind glad, I will breathe in’;'),
        ('Abhippamodayaṃ cittaṃ passasissāmī’ti sikkhati',
         'he trains: ‘Making the mind glad, I will breathe out’.'),
        ('Samādahaṃ cittaṃ assasissāmī’ti sikkhati',
         'He trains: ‘Steadying the mind, I will breathe in’;'),
        ('Samādahaṃ cittaṃ passasissāmī’ti sikkhati',
         'he trains: ‘Steadying the mind, I will breathe out’.'),
        ('Vimocayaṃ cittaṃ assasissāmī’ti sikkhati',
         'He trains: ‘Setting the mind free, I will breathe in’;'),
        ('Vimocayaṃ cittaṃ passasissāmī’ti sikkhati',
         'he trains: ‘Setting the mind free, I will breathe out’.'),
        ('Aniccānupassī assasissāmī’ti sikkhati',
         'He trains: ‘Seeing impermanence, I will breathe in’;'),
        ('Aniccānupassī passasissāmī’ti sikkhati',
         'he trains: ‘Seeing impermanence, I will breathe out’.'),
        ('Virāgānupassī assasissāmī’ti sikkhati',
         'He trains: ‘Seeing the fading of desire, I will breathe in’;'),
        ('Virāgānupassī passasissāmī’ti sikkhati',
         'he trains: ‘Seeing the fading of desire, I will breathe out’.'),
        ('Nirodhānupassī assasissāmī’ti sikkhati',
         'He trains: ‘Seeing ending, I will breathe in’;'),
        ('Nirodhānupassī passasissāmī’ti sikkhati',
         'he trains: ‘Seeing ending, I will breathe out’.'),
        ('Paṭinissaggānupassī assasissāmī’ti sikkhati',
         'He trains: ‘Seeing letting go, I will breathe in’;'),
        ('Paṭinissaggānupassī passasissāmī’ti sikkhati',
         'he trains: ‘Seeing letting go, I will breathe out’.'),
        ('Evaṃ bhāvitā kho bhikkhave ānāpānassati evaṃ bahulīkatā',
         'It is in this way, monks, that mindfulness of breathing is developed and practised often'),
        ('Mahapphalā hoti mahānisaṃsā’ti', 'so that it brings great fruit and great reward.'),
    ),
    'continues': None,
}

STRIVING = {
    'id': 'reflection-striving',
    'title': 'Dhammapahaṃsāna Pāṭha',
    'title_english': 'Encouragement in the Dhamma',
    'leader': {'pali_roman': 'Handa mayaṃ dhamma-pahaṃsāna-pāṭham bhaṇāmase'},
    'groups': _pairs(
        ('Evaṃ svākkhāto bhikkhave mayā dhammo',
         'Monks, in this way the Dhamma I have taught is well proclaimed:'),
        ('Uttāno', 'made plain,'),
        ('Vivaṭo', 'opened up,'),
        ('Pakāsito', 'made known,'),
        ('Chinna-pilotiko', 'with nothing patched or covered over.'),
        ('Alam-eva saddhā-pabbajitena kula-puttena viriyaṃ ārabhituṃ',
         'So it is fitting for a son of good family who has gone forth in faith '
         'to rouse up energy, thinking:'),
        ('Kāmaṃ taco ca nahāru ca aṭṭhi ca avasissatu',
         '‘Gladly, let only skin, sinew and bone be left;'),
        ('Sarīre upasussatu maṃsa-lohitaṃ',
         'let the flesh and blood dry up in my body;'),
        ('Yaṃ taṃ', 'whatever can be reached'),
        ('Purisa-thāmena', 'through human strength,'),
        ('Purisa-viriyena', 'through human energy,'),
        ('Purisa-parakkamena', 'through human striving,'),
        ('Pattabbaṃ na taṃ apāpuṇitvā', 'until I have reached it,'),
        ('Viriyassa saṇṭhānaṃ bhavissatī’ti', 'my energy will not come to rest.’'),
        ('Dukkhaṃ bhikkhave kusīto viharati', 'Monks, the lazy person lives in suffering,'),
        ('Vokiṇṇo pāpakehi akusalehi dhammehi', 'tangled up in bad, unwholesome things,'),
        ('Mahantañca sadatthaṃ parihāpeti', 'and lets his own great good slip away.'),
        ('Āraddha-viriyo ca kho bhikkhave sukhaṃ viharati',
         'But, monks, the person whose energy is roused lives in happiness,'),
        ('Pavivitto pāpakehi akusalehi dhammehi', 'set apart from bad, unwholesome things,'),
        ('Mahantañca sadatthaṃ paripūreti', 'and brings his own great good to fulfilment.'),
        ('Na bhikkhave hīnena aggassa patti hoti',
         'Monks, the highest is not reached by what is low;'),
        ('Aggena ca kho bhikkhave aggassa patti hoti',
         'monks, the highest is reached by what is highest.'),
        ('Maṇḍapeyyam-idaṃ bhikkhave brahmacariyaṃ',
         'Monks, this holy life is like the finest cream, ready to drink;'),
        ('Satthā sammukhī-bhūto', 'the Teacher is here before you.'),
        ('Tasmātiha bhikkhave viriyaṃ ārabhatha',
         'So, monks, rouse up your energy'),
        ('Appattassa pattiyā', 'to reach what is not yet reached,'),
        ('Anadhigatassa adhigamāya', 'to gain what is not yet gained,'),
        ('Asacchikatassa sacchikiriyāya', 'to realise what is not yet realised,'),
        ('Evaṃ no ayaṃ amhākaṃ pabbajjā avaṅkatā avañjhā bhavissati',
         'thinking: ‘In this way our going forth will not be wasted or barren,'),
        ('Saphalā sa-udrayā', 'but fruitful and rewarding;'),
        ('Yesaṃ mayaṃ paribhuñjāma cīvara-piṇḍapāta-senāsana-'
         'gilānappaccaya-bhesajja-parikkhāraṃ tesaṃ te kārā amhesu',
         'and for those whose robes, almsfood, dwellings and medicines we use, '
         'what they have done for us'),
        ('Mahapphalā bhavissanti mahānisaṃsā’ti',
         'will bring great fruit and great reward.’'),
        ('Evaṃ hi vo bhikkhave sikkhitabbaṃ', 'This, monks, is how you should train.'),
        ('Att’atthaṃ vā hi bhikkhave sampassamānena', 'Monks, seeing your own good,'),
        ('Alam-eva appamādena sampādetuṃ',
         'it is fitting to keep working with care;'),
        ('Par’atthaṃ vā hi bhikkhave sampassamānena', 'monks, seeing the good of others,'),
        ('Alam-eva appamādena sampādetuṃ',
         'it is fitting to keep working with care;'),
        ('Ubhay’atthaṃ vā hi bhikkhave sampassamānena', 'monks, seeing the good of both,'),
        ('Alam-eva appamādena sampādetun’ti',
         'it is fitting to keep working with care.'),
    ),
    'continues': None,
}

REFLECTION_CHANTS = [UNIVERSAL_WELL_BEING, UNCONDITIONED, MINDFULNESS_OF_BREATHING, STRIVING]


def _add_thai_script():
    """The Thai-script Pali line, made the same way as Ajarn Owen's."""
    import os
    import sys
    scripts = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from pali_to_thai import convert
    for chant in REFLECTION_CHANTS:
        # plain=True reads the word-final m (mayam, pāṭham) as ṃ, so the
        # Thai line says มะยัง as every Thai temple chants it.
        chant['leader']['pali'] = convert(chant['leader']['pali_roman'], plain=True)
        for group in chant['groups']:
            group['pali_thai'] = [convert(line) for line in group['pali']]
        chant['first_line'] = chant['groups'][0]['pali'][0]


_add_thai_script()
