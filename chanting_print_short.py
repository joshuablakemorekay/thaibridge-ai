"""Short commentary for the PRINTED chanting book.

The app shows each chant's full Historical background and Meaning and
purpose (chanting.py). Printed in full they made the book far too long, so
the print edition (scripts/build_chanting_print.py) uses these instead:
two or three sentences per section, keeping where the chant comes from and
what it means.

Kept in its own file rather than as extra fields in chanting.py, because
chanting.py holds 305 chants of verified Pali and editing every one of
them is exactly the kind of change that file's workflow avoids. The app
never reads this file.

Written from the full text in chanting.py, never from outside sources, so
the short version says nothing the long one does not.

    SHORT[chant_id] = {'background': '...', 'meaning': '...'}

A chant with no entry here prints its full text.
"""

SHORT = {
    'kham-bucha-phra-ratanattaya': {
        'background': (
            'This is the first chant in the book and opens the morning service. Its '
            'name comes from pūjā, honouring done by an act: candles, incense and '
            'flowers are set before the shrine, and the chant is spoken over them. '
            'The epithets are canonical, but the arrangement into an offering '
            'formula is the work of the liturgy.'
        ),
        'meaning': (
            'The chant names each of the Three Jewels by its own epithet, then '
            'offers the gifts set out before them. It openly admits that the Buddha '
            'passed away long ago and that the gifts are poor, and asks anyway, out '
            'of his compassion for later generations. Its real work is to settle '
            'the assembly, so the service can begin, for the lasting welfare of '
            'those present.'
        ),
    },
    'kham-namatsakan-phra-ratanattaya': {
        'background': (
            'These three lines reuse the epithets of the offering before them, '
            'which come from the standard canonical recollections of the Buddha, '
            'Dhamma and Sangha. The book prints an instruction to bow together '
            'after each line, so the chant has a simple shape: three statements, '
            'three prostrations.'
        ),
        'meaning': (
            'Each line first states a quality, then says what the speaker does '
            'about it. The three verbs differ: a salutation to a teacher, homage to '
            'a teaching, a bow to a community. The words exist to give each bow a '
            'stated reason just before the body makes it.'
        ),
    },
    'kham-choen-bucha-lae-suat-namo': {
        'background': (
            "This is a leader's line: one voice says what is about to happen and "
            'the assembly takes up the chant named. Its speakers are those who have '
            'gone for refuge, gone forth and live the holy life, so it is phrased '
            'for a monastic assembly.'
        ),
        'meaning': (
            "It first describes the speakers' relation to the Buddha, then narrates "
            "the offering just made, then turns with 'now then' to the praise that "
            'follows. It marks the moment the service moves from gifts and gestures '
            'into speech, keeping a large assembly moving together.'
        ),
    },
    'pubbabhaga-namakara': {
        'background': (
            'This is very likely the most often recited sentence in Theravāda '
            'Buddhism, spoken across the canon by those declaring confidence in the '
            'Buddha. It is chanted three times, with the deputy leader beginning, '
            'the others joining, and one shared breath after each.'
        ),
        'meaning': (
            'It is one word of homage followed by three epithets of the Buddha: '
            'blessed, worthy, and perfectly enlightened by himself. Nothing is '
            'asked and the Buddha is spoken about rather than to, so it suits any '
            'occasion. Said three times, it marks the threshold between ordinary '
            'speech and chanting.'
        ),
    },
    'buddhabhithuti': {
        'background': (
            "Its name comes from the leader's invitation, 'now let us give praise "
            "to the Buddha'. The epithets and the passages on teaching are stock "
            'canonical formulas; the liturgy composed the frame, a single sentence '
            'held open from the first clause to the last.'
        ),
        'meaning': (
            'The chant praises the Buddha twice over: first by his epithets, then '
            'by his deeds, making the world known through his own direct knowledge '
            'and teaching a Dhamma complete in meaning and letter. It ends in '
            'offering and a bow, so the bow is made by someone who has just said '
            'aloud what it is for.'
        ),
    },
    'dhammabhithuti': {
        'background': (
            "This is the middle of a set of three praises built to one plan: 'that "
            "which', then its qualities, then offering and a bow. Its six qualities "
            'are the standard canonical recollection of the Dhamma.'
        ),
        'meaning': (
            'The qualities describe the teaching by what can be done with it: '
            'visible here and now, timeless, inviting all to come and see, leading '
            'onwards, and to be known by each wise person for themselves. Chanted '
            "daily, it is a description to hold one's own practice up against."
        ),
    },
    'sanghabhithuti': {
        'background': (
            'Here the Sangha means the four pairs and eight kinds of noble ones, '
            'those who have reached the stages of awakening, so membership is by '
            'attainment rather than by ordination. The rubric after it closes the '
            'whole opening movement of the service.'
        ),
        'meaning': (
            'It names four aspects of one practice, practised well, '
            'straightforwardly, methodically and fittingly, and then says what is '
            'therefore owed: gifts, hospitality, offerings and respect. It closes '
            'on the image of the unexcelled field of merit for the world, a field '
            'honoured for what grows in it.'
        ),
    },
    'ratanattayappanamagatha': {
        'background': (
            'This is the first chant in metre rather than prose, in stanzas of four '
            "lines. It is a poet's composition rather than a canonical passage, "
            'richer in imagery than the formulas before it.'
        ),
        'meaning': (
            "Each stanza describes one of the Three Jewels and ends 'I revere it "
            "with devotion': the Buddha as an ocean of compassion, the Dhamma as a "
            'lamp lighting the way, the Sangha as the finest field. The last stanza '
            'dedicates the merit of this reverence to clearing away obstacles.'
        ),
    },
    'samvega-parikittana-patha': {
        'background': (
            'Saṃvega names the jolt of seeing that life is serious and time is '
            'short, the kind that starts a person rather than stopping them. The '
            'passage shares its invitation with the verses before it, so the two '
            'are chanted as one stretch. Much of its wording is canonical, recast '
            'in the first person plural.'
        ),
        'meaning': (
            'It sets out the first noble truth, then names the five aggregates '
            'slowly, as suffering, as impermanent and as not-self. It then turns to '
            'the chanters themselves, overcome by suffering, and to the hope that '
            'an end to it can be found. Recited daily, it keeps the reason for the '
            "day's practice from going missing."
        ),
    },
    'tangkhanika-paccavekkhana-patho': {
        'background': (
            "The book itself prints its canonical source. The title means 'at that "
            "moment': it is a reflection made at the instant of using the robe, "
            'food, lodging or medicine, rehearsed in the morning so it is ready '
            'during the day.'
        ),
        'meaning': (
            "Each reflection opens 'reflecting wisely' and names its requisite only "
            'for its basic use, such as warding off cold and heat. A limit is set '
            'before the use is granted, so the thing stays in use while the reasons '
            'for wanting a better one fall away.'
        ),
    },
    'pattidana-gatha': {
        'background': (
            'Pattidāna is the giving over of merit, which the tradition holds is '
            'not used up by sharing. This is the last chant of the morning service, '
            'and almost every formal chanting in the book closes with some form of '
            'it.'
        ),
        'meaning': (
            'It first gives the merit of the service to the devas of the place, '
            'then widens step by step to monks, lay supporters, towns and rulers, '
            'and every kind of living being. It closes by asking for ordinary '
            'blessings: the Dhamma lasting, the Sangha united, rain in season, and '
            'rulers who care for their people.'
        ),
    },
    'samvega-parikittana-patha-lay-variant': {
        'background': (
            "This is the lay chanters' version of the Passage on Spiritual Urgency, "
            "printed in the book's notes on the morning service. It exists because "
            'the original ends with words only a monastic can say truthfully.'
        ),
        'meaning': (
            'Where monastics say they have gone forth, lay chanters say they have '
            "gone for refuge, and they practise 'as far as ability and strength "
            "allow'. The last line is unchanged: the aim, the ending of all "
            'suffering, is the same for both.'
        ),
    },
    'kham-choen-bucha-phitsadan': {
        'background': (
            'This is the elaborate form of the invitation to make offering. It is '
            'longer because it stops to explain the shrine itself, and it names its '
            'own Buddha image, made by a named prince, tying it to a particular '
            'hall.'
        ),
        'meaning': (
            'It traces a line from the Buddha to the chanters and admits that the '
            'teaching has been carried on unevenly. It then explains that the image '
            'exists only to call the Buddha to mind, inspiring confidence and '
            'urgency. On observance days, it answers what the image is for before '
            'anyone is asked to bow to it.'
        ),
    },
    'kham-prakat-ubosot': {
        'background': (
            'The Uposatha is the observance day at the quarters of the lunar month, '
            'when lay people may keep eight precepts for a day and a night at the '
            'monastery. This is the announcement made before it begins. Its Thai is '
            'a free, much expanded rendering rather than a translation.'
        ),
        'meaning': (
            'It states the date, gives the reason (a time the Buddha set for '
            'hearing the Dhamma) and invites everyone to keep it for this night and '
            'day. It ends with the line people remember: may our life not be barren '
            'of fruit.'
        ),
    },
    'kham-aradhana-ubosot-sila': {
        'background': (
            'In this tradition precepts are not handed out unasked: the one who '
            'wants them asks a monk, and only then are they given. Here the eight '
            'Uposatha precepts and the Three Refuges are requested together, three '
            'times.'
        ),
        'meaning': (
            "Apart from 'a second time' and 'a third time', the lines are "
            'identical; saying a thing three times marks it as formally done. The '
            'point is the order: a precept that has been asked for belongs to the '
            'person who asked.'
        ),
    },
    'tisarana-gamana-ubosot': {
        'background': (
            'Going for refuge is how a person becomes a follower of the tradition. '
            'Refuge here means a direction rather than rescue: the Buddha who found '
            'the way, the Dhamma that is the way, the Sangha who have walked it. '
            'The same words are used whenever refuge is taken.'
        ),
        'meaning': (
            "The key word is 'I go', an act rather than a belief, said by each "
            'person in the first person. Repeated three times, it means the '
            'precepts that follow are kept by someone who has just said where they '
            'stand.'
        ),
    },
    'ubosot-sila': {
        'background': (
            'Lay people usually keep five precepts; on the observance day they keep '
            'eight. The third becomes full celibacy, and three new ones are added. '
            'Each is a training rule taken up by the person, not a commandment '
            'imposed on them.'
        ),
        'meaning': (
            'The added precepts give up afternoon food, entertainment and '
            'adornment, and high or luxurious beds. They are there to make the day '
            'unlike other days, leaving time and quiet for practice. The last line '
            'limits the undertaking to this night and day, so a householder can '
            'truly promise it.'
        ),
    },
    'imani-attha-sikkhapadani': {
        'background': (
            'This one sentence belongs to the monk giving the precepts, and it '
            'closes the exchange of request, refuges and precepts.'
        ),
        'meaning': (
            'It asks that the eight precepts just taken be guarded with '
            'heedfulness. The opposite of heedfulness is not wickedness but '
            'inattention, which is how most undertakings are lost: taking a precept '
            'takes a moment, keeping it is the work.'
        ),
    },
    'silena-sugatim-yanti': {
        'background': (
            'These four lines are among the most often heard in Thai temples, short '
            'enough to be remembered by people who chant nothing else. They come at '
            'the end of the taking of the precepts.'
        ),
        'meaning': (
            'Virtue leads to a good rebirth, to wealth in this life, and to peace '
            'beyond both. The verse gives the reasons first, then the instruction: '
            'therefore, let virtue be purified.'
        ),
    },
    'sarana-gamananussarana-gatha': {
        'background': (
            'This is a recollection of the going for refuge, calling it to mind '
            "afterwards as a practice in its own right. It is a lay follower's "
            'chant, and it says so: refuge was declared in the presence of the '
            'Sangha. Its middle verses echo a well known canonical verse, recast in '
            'the first person.'
        ),
        'meaning': (
            'It claims the refuge is safe and supreme, freeing one from all '
            'suffering, while the speaker promises only to practise as far as their '
            'strength allows. The refuge is complete; the practitioner is not yet, '
            'and the verses close looking to the time to come.'
        ),
    },
    'kham-kho-khama-phra-rattanatrai': {
        'background': (
            'Khamā is asking pardon. One stanza is said three times, to the Buddha, '
            'the Dhamma and the Sangha in turn. The tradition has no way for a '
            'confessed fault to be cancelled, and the chant does not ask for one: '
            'it brings the fault into the open and looks to the future.'
        ),
        'meaning': (
            'Each stanza names the three doors of action, body, speech and mind, '
            'then the fault, then asks that it be accepted. The reason given is '
            "'that in time to come I may be restrained': pardon is sought for the "
            'sake of future restraint, not to undo the past. It suits the start of '
            'a retreat or a day of precepts.'
        ),
    },
    'sekhiyavatta': {
        'background': (
            'The Sekhiya are the training observances, the last, largest and '
            'mildest section of the monastic rule, governing how a monk appears to '
            'the households he walks among. This is the first of four groups, '
            'twenty-six rules on what is fitting.'
        ),
        'meaning': (
            "Each rule is a first-person resolution ending 'this is a training to "
            "be observed', not an order. They cover ordinary things: wearing the "
            'robes evenly, going among houses well covered, not lolling. A '
            'community living on alms depends on village goodwill, and reciting the '
            'list keeps these small things in mind before the moment arrives.'
        ),
    },
    'sekhiya-bhojanapatisamyutta': {
        'background': (
            'This is the second and largest group of the training rules, thirty in '
            'all. The almsround and the meal are where monastic and lay life meet '
            'every morning, so more rules attach to that hour than to any other.'
        ),
        'meaning': (
            'The rules govern the manner of receiving and eating food, not its '
            'amount or quality: receiving it attentively, eating with care in '
            "another person's home. They are good manners written down and "
            "memorised, so that the most visible and dependent moment of a monk's "
            'day is practised in advance.'
        ),
    },
    'sekhiya-dhammadesanapatisamyutta': {
        'background': (
            'This is the third group of training rules, sixteen in all, on teaching '
            'the Dhamma. Every rule repeats an exception for someone who is ill, so '
            'that no rule can be quoted without it.'
        ),
        'meaning': (
            'Each rule declines to teach a listener in a certain position, such as '
            'holding a weapon or walking ahead of the teacher. The concern is the '
            "arrangement, not the person's worth: the rules protect the teaching by "
            'naming when speech can be received. Where there is real need, as in '
            'illness, the whole group falls away.'
        ),
    },
    'sekhiya-pakinnaka': {
        'background': (
            'Pakiṇṇaka means miscellaneous. These three rules close the training '
            'observances, which number twenty-six, thirty, sixteen and three across '
            'the four groups, and they carry the same exception for illness.'
        ),
        'meaning': (
            'All three concern disposing of what the body produces, with care for '
            'the plants and water other people use. Having covered robes, walking, '
            'eating and teaching, the section ends by treating the least dignified '
            'part of life with the same attention as everything else.'
        ),
    },
    'dasadhamma-sutta': {
        'background': (
            'This is the first chant the book numbers, a full discourse set in '
            "Jeta's Grove at Sāvatthī. Its ten reflections are the monastic "
            'counterpart of the five recollections for everyone: they concern what '
            'a monk has taken on by choice.'
        ),
        'meaning': (
            'The reflections ask whether the change of life has really been '
            "noticed, whether one's own conscience and wise companions find fault, "
            'and how the days and nights are being spent. The last asks whether one '
            'would be embarrassed if questioned at the end of life. The discourse '
            'says to return to them again and again, which is why it is chanted.'
        ),
    },
    'parittakarana-patha': {
        'background': (
            'Paritta means protection: a text chanted for safety. In the '
            "tradition's own account it works through truth, not magic: a true "
            'statement is made and its truth invoked. This chant joins three prose '
            'passages with verses that share a common refrain.'
        ),
        'meaning': (
            'The prose declares the Buddha foremost of beings, dispassion foremost '
            'of things, and the Sangha foremost of communities. Each verse then '
            "ends 'by this truth may there be well-being'. Nothing is begged; "
            'well-being is claimed as following from what is true, said aloud for '
            'someone frightened or ill.'
        ),
    },
    'mettanisamsa-sutta': {
        'background': (
            "This short discourse, spoken at Jeta's Grove in Sāvatthī, is built "
            'around a numbered list of eleven benefits. The Pali states the count '
            'twice, so the list is easy to check.'
        ),
        'meaning': (
            'The benefits come only from loving-kindness developed as a liberation '
            'of mind, practised fully and made a foundation. They run from sleeping '
            'and waking happily without bad dreams, through being dear to humans '
            'and non-humans, safety and a clear face, to dying unconfused and '
            'rebirth in the Brahmā world.'
        ),
    },
    'mettanisamsa-gatha': {
        'background': (
            'These verses follow the discourse on loving-kindness, but give their '
            "benefits to something more concrete: not betraying one's friends. Each "
            'of the ten stanzas names three rewards and ends on the same refrain.'
        ),
        'meaning': (
            'The rewards are worldly and practical: food far from home, honour in '
            'towns, safety from thieves, a welcome in the assembly, healthy cattle '
            'and good harvests. What is given out returns. The chant ends with a '
            'banyan tree whose wide roots the wind cannot overturn; so enemies '
            'cannot overcome a faithful friend.'
        ),
    },
    'nidhikanda-gatha': {
        'background': (
            'The book prints the source of these verses. The chant is one long '
            "simile: a man buries treasure at the water's edge against a future "
            'need, and eleven verses stay with that picture before the argument '
            'turns.'
        ),
        'meaning': (
            'Buried treasure can shift, be forgotten, be stolen by spirits or '
            'unloved heirs, or be lost when merit runs out. The lasting store is '
            'laid up through giving, virtue and restraint, and in shrines, the '
            'Sangha, guests and parents. Its rewards reach from good looks and '
            'kingship to Nibbāna itself. Chanted after a donation, it tells the '
            'giver what they have done.'
        ),
    },
    'dhammagaravadi-gatha': {
        'background': (
            'The chant opens by saying that all Buddhas, past, future and present, '
            'dwell revering the true Dhamma, and that this is the nature of '
            'Buddhas. What follows is a compilation of verses on several subjects, '
            'with no citation in the book.'
        ),
        'meaning': (
            'It argues from precedent: since every Buddha revered the Dhamma, so '
            "should anyone who wishes for greatness. Its hinge is 'Dhamma protects "
            "the one who lives by Dhamma'. It closes on fragrance: no flower's "
            'scent travels against the wind, but the goodness of the virtuous '
            'spreads everywhere, like a lotus growing from a roadside rubbish heap.'
        ),
    },
    'devatadissa-dakkhinanumodana': {
        'background': (
            'Anumodanā verses are spoken by those who receive an offering, each '
            'fitted to an occasion. These belong to a donor settling in a new place '
            'who dedicates the merit of feeding the virtuous to the devas living '
            'there. The book cites the Vinaya and the Dīgha Nikāya.'
        ),
        'meaning': (
            'The offering is made to the Sangha and its merit given to the devas, '
            'who return the regard shown them, caring for the donor as a mother '
            'cares for her own child. The one the devas favour sees good fortune '
            'always.'
        ),
    },
    'tilakkhanadi-gatha': {
        'background': (
            "The title says 'the three characteristics and others', marking a "
            'compilation. The opening three stanzas give the canonical verses on '
            'impermanence, suffering and not-self; the book cites the Khuddaka '
            'Nikāya.'
        ),
        'meaning': (
            'Seeing each characteristic with wisdom, one turns away from suffering: '
            'this is the path to purity. Few people reach the far shore; the rest '
            'run up and down the near bank. The wise leave the dark for the bright, '
            'seek seclusion and cleanse the mind, and the chant ends with those '
            'whose taints are gone, wholly at peace in the world.'
        ),
    },
    'devatabhisammantana': {
        'background': (
            'This follows the previous chant, but where that one dedicated merit to '
            'the devas, this one speaks to them directly. The book gives no source '
            'for it.'
        ),
        'meaning': (
            'It greets the beings of earth and air and asks them to listen gladly, '
            'offering them a teaching as its gift. Only then does it ask them to '
            'show loving-kindness to the people who bring them offerings day and '
            'night. It is candid about why: humans are weak, these beings unseen '
            'and strong, so may they guard them.'
        ),
    },
    'viharadana-gatha': {
        'background': (
            'A short chant for one occasion: the gift of a dwelling, from a single '
            'hut to a whole monastery. The book prints its source.'
        ),
        'meaning': (
            'It first lists the practical facts: a dwelling keeps off cold, heat, '
            'wild animals, insects, rain and wind, giving shelter and a place to '
            'meditate. A wise person therefore builds dwellings and supports the '
            'learned in them. In return, they teach the Dhamma that ends suffering, '
            'the one thing they have to give.'
        ),
    },
    'saccapanavidhyanurupa-gatha': {
        'background': (
            'The title names an occasion, a rite at which an undertaking is sworn, '
            'and the verses were chosen to suit it. Every verse turns on truth, '
            'faith, or what a householder should stand on. The book prints its '
            'source.'
        ),
        'meaning': (
            'It opens with its largest claim: truth is deathless speech. Faith is '
            'the best wealth, truth the sweetest taste, and a life lived by wisdom '
            'the best life. The faithful householder with truth, steadfastness and '
            'generosity does not grieve at death, and the verses end by inviting '
            'anyone to find something greater than truth, restraint, generosity and '
            'patience.'
        ),
    },
    'pabbatopama-gatha': {
        'background': (
            'These verses come from a discourse addressed to a king, and take their '
            'name from the opening simile: vast mountains closing in from all four '
            'directions, grinding down everything between. The book cites both the '
            'Sutta-nipāta and the Saṃyutta Nikāya.'
        ),
        'meaning': (
            'Just so, ageing and death crush everyone, whatever their rank, and no '
            'army, spell or wealth can stop them. The wise therefore place their '
            'faith in the Buddha, Dhamma and Sangha. The one who lives by Dhamma in '
            'body, speech and mind is praised in this life and rejoices hereafter.'
        ),
    },
    'adiyasutta-gatha': {
        'background': (
            'The book prints the source of these verses. They speak in the voice of '
            'a householder with property taking stock of what he has done with it, '
            'without any suggestion that he should not have had it.'
        ),
        'meaning': (
            'He lists what his wealth was used for: enjoyment, supporting '
            'dependants, overcoming hardship, offerings, and serving the virtuous. '
            'He has used it for the purpose a wise householder would want wealth '
            "for. The key line is 'what has been done brings no remorse': reaching "
            'the end of life able to look at the account calmly.'
        ),
    },
    'ariyadhana-gatha': {
        'background': (
            'The noble wealth is a standard list of goods that cannot be lost to '
            'theft, fire or the state. These verses take four of them: faith, '
            'virtue, confidence in the Sangha, and upright vision.'
        ),
        'meaning': (
            'Whoever has unshaken faith in the Buddha, good virtue, confidence in '
            'the Sangha and upright vision is not poor, and their life is not in '
            "vain. So the wise should pursue these four, remembering the Buddhas' "
            'teaching.'
        ),
    },
    'paticcasamuppada-patho': {
        'background': (
            'This is the doctrinal formula of dependent origination, in the two '
            'movements the tradition always pairs: arising and cessation. The book '
            'supplies its own headings and cites the Saṃyutta, the Aṅguttara and '
            'the Udāna.'
        ),
        'meaning': (
            'Twelve links arise each in dependence on the one before, from '
            "ignorance to ageing and death, and 'thus is the arising of this whole "
            "mass of suffering'. The reverse shows that when ignorance fully "
            'ceases, every link after it ceases too: the sequence is a chain that '
            'can be broken, not a fate.'
        ),
    },
    'buddhaudana-gatha': {
        'background': (
            'These are the first three utterances of the Udāna, spoken in the three '
            "watches of a single night soon after the Buddha's awakening. The book "
            'cites the Udāna and its Vinaya parallel. Each stanza repeats the same '
            'opening and changes only its ending.'
        ),
        'meaning': (
            'When things become clear to the ardent, meditating practitioner, the '
            'first stanza ends with knowing things and their causes, the second '
            'with knowing the ending of those conditions: the two halves of '
            'dependent origination. The third gives an image instead: he stands '
            "scattering Māra's army, like the sun lighting up the sky."
        ),
    },
    'bhaddekaratta-gatha': {
        'background': (
            "Bhaddekaratta means 'the auspicious single night', a day and night "
            'well spent. These four stanzas come from a canonical discourse of the '
            'same name, which goes on to explain them; the chanting books print the '
            'verses alone.'
        ),
        'meaning': (
            'Do not run after the past or hope for the future: the past is gone and '
            'the future has not come. See whatever is present clearly, steadily, '
            'where it is. Make the effort today, since death may come tomorrow and '
            'cannot be bargained with. Whoever lives like this, ardent day and '
            'night, the sage calls one who has had an auspicious night.'
        ),
    },
    'mahakassapa-bojjhanga-suttam': {
        'background': (
            'The seven factors of awakening are mindfulness, investigation, energy, '
            'rapture, tranquillity, concentration and equanimity. This is the first '
            'of three parallel discourses, set at Rājagaha and chanted as a set, in '
            'which the factors are recited to someone who is ill.'
        ),
        'meaning': (
            'The Buddha asks the sick Mahākassapa whether his pain is easing; '
            'Kassapa says plainly that it is getting worse. No comfort is offered, '
            'only the seven factors, which lead to awakening and Nibbāna. Kassapa '
            'recovers. The recovery is recorded, not promised, which is how the '
            'chant is used at sickbeds.'
        ),
    },
    'mahamoggallana-bojjhanga-suttam': {
        'background': (
            'The second discourse of the set is almost word for word the first, '
            "with a different patient and place: Mahāmoggallāna, on the Vulture's "
            'Peak. The book prints all three in full, so the seven factors are '
            'recited three times in one sitting.'
        ),
        'meaning': (
            'Again the pain is not easing, and again the Buddha answers not the '
            'pain but the seven factors of awakening. Two senior disciples, in '
            'different places, are given exactly the same words, and both recover. '
            'The sameness is the point: nothing is tailored to the person.'
        ),
    },
    'mahacunda-bojjhanga-suttam': {
        'background': (
            'In the third discourse, set in the same Bamboo Grove at Rājagaha, the '
            'sick person is the Buddha himself. Alone of the three, it carries a '
            'reference printed in the book.'
        ),
        'meaning': (
            'Here the Buddha asks Mahācunda to recite the factors to him, and Cunda '
            'gives the list back. The Buddha confirms it, as his disciples did to '
            'him, and recovers. The set shows that recitation is not only for the '
            'junior or the sick: even the one who taught the list is recited to.'
        ),
    },
    'phra-winai-sangkhep': {
        'background': (
            'Suat Jaeng is funeral chanting in which each of the three divisions of '
            'the canon is represented by a short opening extract. This first one '
            'stands for the whole of the monastic discipline, far too long to '
            'recite.'
        ),
        'meaning': (
            'It opens as question and answer about the first and gravest rule, laid '
            'down at Vesālī over the monk Sudinna, then turns to the opening scene '
            'of the Buddha at Verañjā. Both are beginnings, which is why they can '
            "stand for the whole: a gesture towards completeness, ending 'here ends "
            "the Vinaya'."
        ),
    },
    'phra-sut-sangkhep': {
        'background': (
            'The second extract of the funeral set stands for the Suttas, as the '
            'one before stood for the Vinaya. The book prints its source. It is '
            'only four sentences, chosen because it is an opening.'
        ),
        'meaning': (
            'The Buddha travels between Rājagaha and Nāḷandā with five hundred '
            'monks, followed by the wanderer Suppiya, who criticises the Three '
            'Jewels, and his pupil, who praises them. The extract stops there, '
            'unresolved, showing how the Suttas typically begin: a road, a company, '
            'and something that must be answered.'
        ),
    },
    'phra-sangkhani': {
        'background': (
            'The Abhidhamma, the third division of the canon, restates the teaching '
            'analytically, in lists. Each of its seven books is represented at '
            'funerals by its opening lines; this is the first.'
        ),
        'meaning': (
            'It opens on the triad the whole Abhidhamma rests on: wholesome, '
            'unwholesome and indeterminate states. It then describes the conditions '
            'in which wholesome consciousness arises, without defining it. Chanted '
            'at a death, it sets out exactly what a person consists of, in '
            'categories that do not include a self.'
        ),
    },
    'phra-wiphang': {
        'background': (
            'Vibhaṅga means analysis, a taking apart. Where the first book lists, '
            'this one divides: it names a set, then analyses one member of it.'
        ),
        'meaning': (
            'It names the five aggregates, form, feeling, perception, formations '
            'and consciousness, which together make up a person. It then defines '
            'form as all form, past, future or present, near or far, gathered into '
            'one heap under one word. Beside a body, it includes form that is past.'
        ),
    },
    'phra-thatukatha': {
        'background': (
            'Dhātukathā is the discussion of elements. Its extract is the shortest '
            'and most forbidding of the set, because the book opens not with a '
            'teaching but with the vocabulary it uses to ask questions.'
        ),
        'meaning': (
            'It recites terms such as included and not included, associated and '
            'dissociated, with all their combinations. It is a grammar rather than '
            'a doctrine, the frame for asking how every element relates to every '
            'other: an instrument for thinking, which is a fair picture of the '
            'Abhidhamma itself.'
        ),
    },
    'phra-pukkhalabanyat': {
        'background': (
            'Puggalapaññatti, the designation of persons, is the only one of the '
            'seven books to speak of persons at all. The book prints its source.'
        ),
        'meaning': (
            'It asks on what basis a person may be spoken of, and answers with '
            'pairs: one who may fall away and one who cannot, the ordinary person '
            'and the noble one, the one practising and the one who has arrived. '
            'Every distinction is a position on the path, never a personality or a '
            'name.'
        ),
    },
    'phra-kathawatthu': {
        'background': (
            'Kathāvatthu means points of controversy; this book is a record of '
            'disputes. The extract is part of an actual exchange, printed with both '
            'voices.'
        ),
        'meaning': (
            'Is a person found as a real, ultimate fact? The opponent says yes, but '
            'will not say a person is found in the same way as real facts are, and '
            'is refuted. The argument turns on the difference between speaking of a '
            'person and finding one. At a funeral, it declines to give the '
            'consoling answer.'
        ),
    },
    'phra-yamaka': {
        'background': (
            'Yamaka means a pair. Every question in this book is asked in both '
            'directions, so that a statement and its reverse are both tested. The '
            'book prints a reference for it.'
        ),
        'meaning': (
            'Whatever states are wholesome have wholesome roots; and whatever have '
            'wholesome roots are wholesome. Here both directions hold, but the book '
            'exists to catch the many cases where they do not. It recites a habit '
            'of checking a statement both ways before believing it.'
        ),
    },
    'phra-mahapatthan': {
        'background': (
            'The Paṭṭhāna, the book of conditional relations, is the largest and '
            'most demanding of the seven. It is represented only by its list of '
            'conditions, and the funeral set ends here.'
        ),
        'meaning': (
            'Twenty-four conditions are named one after another, from root and '
            'object to presence and absence, each a way one thing can bring about '
            'another. Having named states, aggregates, persons and disputes, the '
            'service ends by naming every way things condition each other, and '
            'simply stops.'
        ),
    },
    'thammasangkhani-matika-patho': {
        'background': (
            'The mātikā is the table of headings that organises the first book of '
            'the Abhidhamma. Here it is recited in full, with its own number and '
            'printed source, and is among the most familiar funeral chants in '
            'Thailand.'
        ),
        'meaning': (
            'Almost every line is a triad: two opposites and a third that is '
            'neither, beginning with wholesome, unwholesome and indeterminate. That '
            'third term makes the scheme cover the whole of experience. Said over a '
            'death, it states that the person who has died was, at every moment, '
            'describable in these terms.'
        ),
    },
    'wipassanaphumi-patho': {
        'background': (
            'Vipassanābhūmi means the grounds of insight: not how to practise '
            'insight, but what insight examines. Every set in it appears elsewhere '
            'in the book; this chant gathers them into one place and fixes their '
            'order.'
        ),
        'meaning': (
            'It runs from the five aggregates to the twelve sense bases, the '
            'eighteen elements, the twenty-two faculties and finally the four noble '
            'truths. Each set divides the same experience more finely, and the '
            'truths come last because they are what the dividing is for. Insight '
            'here is attention paid to set things in a set order.'
        ),
    },
    'thawai-phon-phra': {
        'background': (
            'Thawai phon phra names the occasion, the blessing offered by the '
            'monks, which these three verses open. They are the standard '
            'recollections of the Buddha, the Dhamma and the Sangha, each '
            'compressed into one sentence.'
        ),
        'meaning': (
            'The verses list nine qualities of the Buddha, six of the Dhamma and '
            "the Sangha's four ways of practising and the honour due to it. Nothing "
            'is asked for; the blessing is held to follow from recollecting these '
            'qualities aloud. Before a meal, it puts the reason for the meal into '
            'words.'
        ),
    },
    'jayamangala-atthaka-gatha': {
        'background': (
            'These eight verses each tell of one adversary the Buddha overcame, '
            'among them Māra, the yakkha Āḷavaka, the drunken elephant Nāḷāgiri and '
            'the murderer Aṅgulimāla. Each ends with the wish that by that power '
            "victory and blessing be the hearer's."
        ),
        'meaning': (
            'None of the eight is overcome by force: generosity, patience, '
            'loving-kindness, gentleness, wisdom and knowledge answer temptation, '
            'rage, an animal, a murderer, slander and a mistaken god. A ninth verse '
            'says that whoever recalls these daily will leave misfortune behind, '
            'which is how the chant is used.'
        ),
    },
    'jayaparitta-gatha': {
        'background': (
            'These verses follow straight on from the eight verses of victory, but '
            'turn from what the Buddha did to the person present. They end with a '
            'refrain that also closes the next chant, binding the sequence '
            'together.'
        ),
        'meaning': (
            'As the Buddha was victorious under the Bodhi tree, so may you be '
            'victorious. Its best-known lines say that a good day is made by good '
            'actions of body, speech and mind, not found on a calendar. It closes '
            'by asking protection through the power of the Buddhas, the Dhamma and '
            'the Sangha.'
        ),
    },
    'mongkhon-chakkrawan-noi': {
        'background': (
            'This is the shorter of two universal blessings. It works by '
            'accumulation, naming powers and then troubles until there are no more '
            'to name, and closes on the same refrain as the chant before it.'
        ),
        'meaning': (
            'It invokes all the Buddhas, the whole Dhamma and Sangha, the '
            'eighty-four thousand teachings, the three baskets and the disciples. '
            'Then it asks that illness, fear and misfortune be destroyed, and long '
            'life, wealth, strength, beauty and happiness grow. It is openly '
            'worldly, the blessing people most often come for.'
        ),
    },
    'kaladana-sutta-gatha': {
        'background': (
            'Kāladāna is giving at the right time, and these verses come from the '
            'discourse of that name, printed without its prose frame. Unusually for '
            'a text on giving, they are mostly about other people.'
        ),
        'meaning': (
            'A gift given at the right time to the upright becomes abundant: its '
            'moment and recipient matter more than its size. Those who rejoice in a '
            'gift or help with it share in the merit, and the giver loses nothing. '
            'At a ceremony where many have carried and cooked, nobody is a '
            'spectator; so give with an unhesitating mind.'
        ),
    },
    'sangahavatthu-gatha': {
        'background': (
            'The four grounds of kindness, the bases that draw people together, are '
            'among the most quoted teachings for lay life in Thai Buddhism. The '
            'book notes the occasion the verses belong to.'
        ),
        'meaning': (
            "The four are giving, kindly speech, conduct for others' good, and "
            'treating everyone alike, making no exception of oneself. They hold the '
            'world together like the linchpin of a moving chariot. Without them, '
            'the verses say, not even parents would be honoured by their children, '
            'so the wise attain greatness by them.'
        ),
    },
    'mokkhupaya-gatha': {
        'background': (
            'Mokkhupāya is the way to liberation, and this chant is a verse manual '
            'that sets it out in order, each step following from the last. Unlike '
            'most chants around it, it is an argument rather than a list, story or '
            'blessing.'
        ),
        'meaning': (
            'It begins with the fourfold purity of virtue, then four protective '
            'meditations: on the Buddha, loving-kindness, the body and death. It '
            'reasons that the five aggregates are impermanent, suffering and '
            'not-self, like a house on fire. It ends with the four truths and '
            'invites the wise to practise on even these few lines.'
        ),
    },
    'ratanattayappabhavasiddhi-gatha': {
        'background': (
            'This chant opens like many others, praising the Three Jewels, but then '
            'names a country: the Thai land, its nation and its righteous king. It '
            'is a modern composition in Pali, written for a kingdom that took the '
            'Triple Gem as the banner of its realm.'
        ),
        'meaning': (
            'After praising the Buddha, Dhamma and Sangha as a refuge that will '
            'bear inspection, it says the Thai land has honoured and guarded them '
            "and stands in peace. It prays for the nation's growth, the long life "
            'of the teaching and the king, and success for those who guard the '
            "realm, showing the tradition's relation to the Thai state in its own "
            'words.'
        ),
    },
    'khatha-bucha-phra-ratanattaya': {
        'background': (
            'This is the same text as the offering at the very start of the book, '
            "nearly word for word, but titled here the 'verse' of offering rather "
            "than the 'words'. It is printed with no service around it, so it can "
            'be used on its own.'
        ),
        'meaning': (
            'It names the Three Jewels, makes the offering, and asks the Buddha, '
            'though long gone, to accept these poor gifts out of compassion, for '
            'our lasting welfare. Here it is a complete act rather than an opening. '
            'A chanting book is arranged by occasion, so a chant needed twice is '
            'printed twice.'
        ),
    },
    'kham-namatsakan-phra-ratanattaya-evening': {
        'background': (
            'These are the same three salutations as at the front of the book, with '
            'the same instruction to bow together after each line. What makes this '
            'the evening version is where it stands, not what it says.'
        ),
        'meaning': (
            'Each line states a quality of one of the Three Jewels and is answered '
            'by a shared prostration. In the evening, the salutation leads into '
            'praise and then, at the quietest point, into asking pardon. Both daily '
            'services begin the same way, with three bows.'
        ),
    },
    'kham-choen-bucha-lae-suat-namo-lae-phra-phuttakhun': {
        'background': (
            "This is the evening version of the leader's invitation near the front "
            'of the book, with the same words. Its longer title also names the two '
            'pieces it leads into, because the book prints no more titles for the '
            'evening service from here.'
        ),
        'meaning': (
            'It names the Buddha as refuge and teacher, recounts the offering, and '
            "hands over with 'now then' to what follows. It works as a signpost, so "
            'that everyone in the hall knows which pieces come next without turning '
            'a page.'
        ),
    },
    'pubbabhaga-namakara-evening': {
        'background': (
            'The same single line as earlier in the book, printed again three times '
            'in full rather than with a note to repeat it.'
        ),
        'meaning': (
            'It pays homage to the Buddha as fortunate, worthy and perfectly '
            'enlightened by himself. The book prints it again in full because a '
            'chanting book must be usable in a dim hall, at speed, with no free '
            'hand to turn back the pages.'
        ),
    },
    'phra-phuttakhun': {
        'background': (
            'The evening service is built on three recollections, of the Buddha, '
            'the Dhamma and the Sangha, each followed by a longer hymn. This one '
            "introduces the Buddha's qualities as 'a good report that has gone "
            "abroad' about him."
        ),
        'meaning': (
            "It lists the Buddha's nine qualities in one breath, from worthy and "
            'perfectly enlightened to teacher of gods and humans. Because they come '
            'as a report, the reciter recollects rather than claims. It is kept '
            "short so the plain list is heard before the hymn's praise."
        ),
    },
    'buddhabhigiti': {
        'background': (
            "This is the first of the evening service's three hymns, which set the "
            'pattern for the others: each is eighteen verses, and from the fifth '
            'verse on they are word for word alike. It opens in ornate metre and '
            'ends with a change of posture and voice.'
        ),
        'meaning': (
            'It praises the Buddha, who woke the good as the sun wakes the lotus, '
            "then turns personal: 'I am the Buddha's servant… for me there is no "
            "other refuge.' At a printed instruction, everyone prostrates and "
            "lowers their voice to ask pardon for any wrong done. The day's service "
            'ends by asking to be excused the day.'
        ),
    },
    'phra-thammakhun': {
        'background': (
            'This is the shortest passage in the evening service: three lines, six '
            'qualities of the Dhamma, with nothing around them. The same six appear '
            'twice more in the book.'
        ),
        'meaning': (
            'The qualities describe what can be done with the teaching: well '
            'proclaimed, visible here and now, timeless, inviting all to come and '
            'see, leading onwards, and to be known by each person for themselves. '
            'Kept this bare between two long hymns, the statement is not lost in '
            'the praise.'
        ),
    },
    'dhammabhigiti': {
        'background': (
            'This is the second of the three evening hymns; from the fifth verse it '
            'follows the first word for word. Its opening divides the Dhamma four '
            'ways: path, fruit, scripture and release.'
        ),
        'meaning': (
            'The Dhamma holds up those who hold to it, keeping them from falling '
            'into lower worlds, and dispels darkness. The reciter calls themselves '
            "the Dhamma's servant and surrenders body and life to it. Then comes "
            'the same prostration and quiet request for pardon for any wrong '
            'towards the Dhamma, which in practice means neglecting it.'
        ),
    },
    'phra-sangkhakhun': {
        'background': (
            'This is the longest of the three evening recollections. The same words '
            'appear in the morning service inside a frame of praise; here they are '
            'given plain.'
        ),
        'meaning': (
            'It names four ways of practising well, then defines the Sangha as the '
            'four pairs and eight kinds of noble ones, those who have reached the '
            'stages of awakening, not simply whatever monks are present. Only then '
            'is the Sangha praised as worthy of gifts and respect, the unexcelled '
            'field of merit for the world.'
        ),
    },
    'sanghabhigiti': {
        'background': (
            'This third hymn completes the set, saluting the Sangha as born of the '
            'true Dhamma, eightfold and wholly pure. By now the same fourteen lines '
            'have been said three times, with one word changed each time.'
        ),
        'meaning': (
            'The same complete devotion is offered to the Sangha as to the Buddha '
            'and the Dhamma, with nothing ranked above the rest. Then come the last '
            'prostration and the quietest moment of the evening service: not praise '
            'but an apology, which is how a day is properly put down.'
        ),
    },
    'buddhamangala-gatha': {
        'background': (
            'These verses set out an arrangement: the Buddha seated in the centre, '
            'and eight named disciples at the eight points of the compass, from '
            'Koṇḍañña in the east to Rāhula in the north-east.'
        ),
        'meaning': (
            'Each disciple is given only a direction, so the chant builds a place '
            'rather than a story: a centre and a complete circle with no gap. It '
            'says they are all present here, honoured by us, and asks blessing by '
            'their power. With the Buddha at the centre and his disciples around, '
            'there is no room left for harm.'
        ),
    },
    'siluddesa-patho': {
        'background': (
            "Sīluddesa is a summary of virtue. Four lines of the Buddha's "
            'instruction are followed by the same four lines spoken by the assembly '
            'about itself.'
        ),
        'meaning': (
            'The instruction is to dwell in virtue and restraint, good in conduct, '
            'seeing danger in the smallest fault. Then the assembly repeats it as '
            "'we shall dwell, we shall train'. Without changing a word, an "
            'instruction becomes an undertaking, closing the gap where most '
            'training is lost.'
        ),
    },
    'bot-khat-sikkhabot-10': {
        'background': (
            'A bot khat is an introductory verse that says what a chant is and why '
            "it exists, ending 'let us now recite'. This one introduces the ten "
            'training rules for novices.'
        ),
        'meaning': (
            'It gives a short history: the Buddha arose, set the Wheel of Dhamma '
            "rolling and, at Jeta's Grove in Sāvatthī, allowed ten rules out of "
            'care for how novices should train. The rules become an answer to a '
            'real need, not a code from nowhere.'
        ),
    },
    'sikkhabot-10': {
        'background': (
            'These are the ten training rules a novice undertakes. The list is '
            "framed at both ends by the statement that the Buddha 'allowed' them."
        ),
        'meaning': (
            'Compared with the eight precepts lay people keep on observance days, '
            'one rule is split in two, and one is new: not accepting gold and '
            'silver. A novice does not handle money at all, which changes a life '
            'more than the other nine together. The rules are framed as permissions '
            'granted, not commands.'
        ),
    },
    'bot-khat-nasananga': {
        'background': (
            'The second introductory verse gives a single named case: a novice '
            'called Kaṇṭaka and the nun Kaṇṭakī. The offence is stated plainly.'
        ),
        'meaning': (
            'An offence occurred, the Buddha learnt of it from the monks, and he '
            'allowed a novice to be expelled on ten grounds. Each rule in this '
            'tradition has an occasion that is remembered with it, so the rule '
            'stays a response rather than a legal code.'
        ),
    },
    'nasananga-10-sikkhabot': {
        'background': (
            'This list of ten grounds for expelling a novice is framed at both ends '
            "by the same sentence. Expulsion ends a novice's standing rather than "
            'punishing them, and the book prints a milder alternative next.'
        ),
        'meaning': (
            "The first five are the gravest training rules, now phrased as 'he is "
            "one who kills' and so on: what a person is, not what they abstain "
            'from. Next come speaking against the Buddha, Dhamma or Sangha, placed '
            'at the same level. The last two are wrong view and seducing a nun, the '
            'very case the introduction described.'
        ),
    },
    'bot-khat-thanthakam': {
        'background': (
            'The third introductory verse follows the same shape: an occasion, the '
            'Buddha learning of it, and an allowance in response. It is printed '
            'beside the verse on expulsion so the difference in scale can be seen.'
        ),
        'meaning': (
            'The occasion is ordinary: novices being disrespectful and behaving '
            'badly towards the monks. What was allowed is a penalty, a correction '
            'for someone who stays, not removal. Read together, the two verses set '
            'out a graded response, so the smaller failing is not mistaken for the '
            'larger.'
        ),
    },
    'thanthakam-5-sikkhabot': {
        'background': (
            'The book prints its own source for this list, framed like the grounds '
            'for expulsion so the two can be compared line by line. These five are '
            'not lesser versions of the ten; they concern something else.'
        ),
        'meaning': (
            "All five are about harm to the community: working against the monks' "
            'gain or welfare, depriving them of a dwelling, abusing them, and '
            'setting monks against each other. A novice could keep every training '
            'rule and still do these. The last is gravest, because a division in a '
            'community cannot simply be undone.'
        ),
    },
    'atita-paccavekkhana-patha': {
        'background': (
            'Atīta means past. This reflection covers the same four requisites as '
            'the one made at the moment of use, but afterwards, in the evening. The '
            'book prints its source. It exists because the reflection at the moment '
            'of use is often not made.'
        ),
        'meaning': (
            "Each section begins 'whatever I have used today without reflecting', "
            'assuming the reflection was missed. It then applies the same purposes '
            'in the past tense: the robe was only to ward off cold and heat, the '
            'food only to sustain the body. It is a rule that expects to be '
            'forgotten and provides for it.'
        ),
    },
    'dhatupatikula-paccavekkhana-p61': {
        'background': (
            'This reflection reduces each requisite to elements and then observes '
            'its repulsiveness. It completes a set of three: what a requisite is '
            'for, a look back over the day, and what the requisite and its user '
            'really are. The book prints it again later with a Thai translation.'
        ),
        'meaning': (
            'The robe is merely elements, and so is the person using it: not a '
            'being, not a soul, empty. The requisites are not repulsive in '
            'themselves, but become so on touching this body. The aim is not '
            'disgust but to undercut the sense of someone to whom pleasant things '
            'are happening, even in choosing robes or food.'
        ),
    },
    'uddissanadhitthana-gatha': {
        'background': (
            'The title names two acts: dedication, giving away merit, and resolve, '
            'a determination made for oneself. The verses do the first and then the '
            'second.'
        ),
        'meaning': (
            'The dedication reaches teachers, parents and kin, the sun, moon and '
            "king, gods and Māra, friends, strangers and enemies, and ends 'may all "
            "beings be happy'. The resolve asks to cut off craving and clinging in "
            'every birth, and that Māra find no opening against these efforts: not '
            'victory, only room to keep working.'
        ),
    },
    'kham-choen-bucha-phra-ratanattaya-phiset': {
        'background': (
            'This is the fullest of the three forms of the invitation to worship: '
            'the short one opens the daily services, the elaborate one is for '
            'observance days, and this one opens the festivals. It contains the '
            "only connected account of the Buddha's life in this part of the book."
        ),
        'meaning': (
            'It places the Buddha in the world: born in the Middle Country, a '
            'khattiya of the Gotama clan, a son of the Sakyans who went forth. It '
            'then stresses effort, right application and endeavour, before what he '
            'attained and taught. It hands over to both the salutation and the '
            'recollection of the Buddha, because a festival service is longer.'
        ),
    },
    'khatha-aradhana-dhamma': {
        'background': (
            'In this tradition a sermon is asked for, not simply delivered, and '
            'these are the words that ask. Short enough to be known by heart, they '
            'are heard almost whenever a monk is about to speak.'
        ),
        'meaning': (
            'It begins with the calendar: the eighth, fourteenth and fifteenth of '
            'the fortnight are days the Buddha set for hearing the Dhamma, and so '
            'the assembly has gathered. It asks the Sangha to teach and commits the '
            'whole assembly to listening, so nobody can ask for a sermon and then '
            'not attend to it.'
        ),
    },
    'kham-tawai-dokmai-thup-thian-visakha': {
        'background': (
            'The four festival offerings share one plan: the same opening, what the '
            'day commemorates, and a request that the offerings be accepted. '
            "Visākha, the first and largest, marks the Buddha's birth, awakening "
            'and final passing, all held to fall on the same full moon.'
        ),
        'meaning': (
            'It recites his life slowly, a few words to a line, as the assembly '
            'holds flowers. It says openly that the Buddha is long gone and known '
            'now only by his qualities, and then offers anyway, for our lasting '
            'welfare and happiness. The flowers are offered knowingly, by people '
            'who have just said he is not there.'
        ),
    },
    'sarabhanna-gatha-visakha': {
        'background': (
            'Sarabhañña is a sung style of chanting with a real melody, used for '
            'verse. Each of the three festivals has its own set, all of the same '
            'length and metre and ending with the same petition.'
        ),
        'meaning': (
            'The first verse states the coincidence the day rests on: on the '
            'Visākha full moon he was born, awakened and passed away. The verses '
            "then praise him as the unsurpassed teacher and the reciters' refuge, "
            'and close by asking that the offerings be accepted for lasting welfare '
            'and happiness.'
        ),
    },
    'kham-tawai-dokmai-thup-thian-atthami': {
        'background': (
            'Aṭṭhamī is the second and least observed of the four festivals. It '
            "marks the eighth day after Visākha, when the Buddha's body was "
            'cremated: the only one of the four days to remember something after '
            'his death.'
        ),
        'meaning': (
            'The offering runs almost line for line with the Visākha one; only the '
            'event in the middle changes. The same refuge, qualities and request '
            'are said over a funeral pyre, and the closing request reads less like '
            'a petition than a statement of what is left.'
        ),
    },
    'sarabhanna-gatha-atthami': {
        'background': (
            'The second sung set is the most narrative of the three, telling what '
            'happened on one afternoon. Its opening line counts the days: today is '
            'the eighth from the Visākha full moon.'
        ),
        'meaning': (
            'The faithful Mallas built a pyre of fragrant woods, which caught fire '
            "of itself, and the Buddha's final body was burnt. Both the body and "
            'the fire are named as elements. The tradition sings about the one '
            'thing it might have exempted from that analysis, and does not exempt '
            'it.'
        ),
    },
    'kham-tawai-dokmai-thup-thian-magha': {
        'background': (
            'Māgha is the third of the four festivals, and the only one to '
            "commemorate an assembly rather than an event in the Buddha's life. It "
            'marks four things that came together at once.'
        ),
        'meaning': (
            'There were twelve hundred and fifty monks, all arahants, all ordained '
            'by the Buddha himself, and all came without being called, in the '
            'Bamboo Grove on the Māgha full moon. The last condition is what is '
            'honoured: a gathering can be arranged, but not one that assembles '
            'unsummoned.'
        ),
    },
    'sarabhanna-gatha-magha': {
        'background': (
            'The third and shortest sung set names the day by its full moon and '
            'places the Buddha in the Bamboo Grove at Rājagaha. It alone asks for '
            "something beyond the reciters' own welfare."
        ),
        'meaning': (
            'Verse by verse it builds the scene: the day, who the Buddha was, and '
            'where he stayed. What it celebrates is a community meeting held '
            'properly, the recitation of the Pāṭimokkha. It closes by asking for '
            "our well-being and that the Teacher's dispensation long endure."
        ),
    },
    'ovada-patimokkhadi-patha': {
        'background': (
            'This is the text the whole Māgha observance points to, printed with a '
            'prefatory verse and further material. The preface presents the '
            'exhortation as taught by all seven Buddhas, older than the Buddha of '
            'this era.'
        ),
        'meaning': (
            'Its heart is three lines: do no evil, take up what is skilful, purify '
            'your own mind; this is the teaching of the Buddhas. It adds that one '
            'gone forth harms no one, followed by restraint and moderation. The '
            'longer material explains virtue, concentration and wisdom at two '
            'levels, and closes on diligence, the root of every wholesome state.'
        ),
    },
    'kham-tawai-dokmai-thup-thian-asalha': {
        'background': (
            'Āsāḷha is the last of the four festivals, and its offering is much the '
            'shortest. It recounts not a life but a decision: that out of '
            'compassion the Buddha chose to teach.'
        ),
        'meaning': (
            'Four words are used where one would do: compassion, mercy, seeking '
            "beings' welfare, sympathy. The day marks the choice to speak more than "
            'what was spoken, which takes one sentence. It closes like the others, '
            'asking that the offerings be accepted for lasting welfare and '
            'happiness.'
        ),
    },
    'bot-khat-chumnum-thewada': {
        'background': (
            'Assembling the devas opens every protective chanting, beginning the '
            'collection this book calls the Twelve Tamnan. The verse speaks to two '
            'audiences at once: it tells the monks how to chant, and asks the devas '
            'to come and listen.'
        ),
        'meaning': (
            'It opens by asking protection for the ruler, his realm and his people. '
            'It asks the monks to chant with loving-kindness and undistracted '
            "minds, since the protection depends on the chanters' state. It invites "
            'devas from every world, and asks of them only one thing, three times: '
            'this is the time to hear the Dhamma.'
        ),
    },
    'pubbabhaga-namakara-sipsong-tamnan': {
        'background': (
            'This is the third full printing of this line in the book, set out '
            'again because this section is used on its own.'
        ),
        'meaning': (
            'The words are unchanged: homage to the Blessed One, worthy and '
            'perfectly enlightened. What changes is the company: here the devas of '
            'every world have already been invited, and the homage is made before '
            'them, three times, marking a formal beginning.'
        ),
    },
    'sarana-gamana-patha-sipsong-tamnan': {
        'background': (
            'The book prints its own source for this passage. The words are the '
            'usual going for refuge, but each of the nine statements has its own '
            'line.'
        ),
        'meaning': (
            'I go to the Buddha, the Dhamma and the Sangha for refuge, three times '
            'over. Setting each on its own line slows the pace of a long service. A '
            'protective chanting states where safety is sought before it makes any '
            'requests.'
        ),
    },
    'sambuddhe': {
        'background': (
            'This chant works by number rather than name: twenty-eight Buddhas, '
            'then twelve thousand, then five hundred thousand. A refrain follows '
            'each group.'
        ),
        'meaning': (
            'The twenty-eight are the Buddhas the tradition can list; the larger '
            "figures say the number is past listing. Each group's Dhamma and Sangha "
            'are honoured too, and then misfortunes and dangers are asked to be '
            'destroyed. Before asking for protection, it establishes the sheer size '
            'of what is honoured.'
        ),
    },
    'namakarasiddhi-gatha': {
        'background': (
            "The title states the chant's premise: that the act of paying homage "
            'itself accomplishes something. It has three parts, one for each of the '
            'Three Jewels.'
        ),
        'meaning': (
            'The Buddha, free of delusion and awakened by himself, freed from '
            "Māra's snares the people fit to be trained, a claim bounded in the "
            "same line. Each part ends 'by this power may victory and success be "
            "yours', so the blessing is for the hearer, not the reciter."
        ),
    },
    'namokara-atthaka-gatha': {
        'background': (
            'Every one of the eight lines begins with namo, homage. It is the most '
            'compressed of the opening homages, and two of its lines salute not a '
            'person or community but a form of words.'
        ),
        'meaning': (
            'It pays homage to the Buddha, the Dhamma and the Sangha, then to the '
            'Triple Gem as named in a sacred syllable: the formula itself is '
            'honoured, the premise of all protective chanting. It closes by asking '
            'for well-being always, and for strength in the task at hand.'
        ),
    },
    'bot-khat-ton-tamnan': {
        'background': (
            'This second invitation to the devas begins the Tamnan collection '
            'itself, so the devas are called twice. Unlike the first brisk summons, '
            'it spends most of its length describing who is being called.'
        ),
        'meaning': (
            'It invites devas who are at peace and have taken the Three Refuges, '
            'wherever they dwell, from the earth to Mount Meru and every '
            'world-system. Before any protective text is chanted, it wishes all of '
            'them happiness, freedom from trouble and gladness, with all their kin.'
        ),
    },
    'bot-khat-mangkhala-sutta': {
        'background': (
            'Each sutta in the Tamnan is introduced by a verse like this, saying '
            'why the text was needed. This is the first, introducing the discourse '
            'on blessings.'
        ),
        'meaning': (
            'For twelve years beings and devas pondered what a blessing is and '
            'never found out, and the debate spread through ten thousand '
            'world-systems. This build-up makes the plain list that follows land as '
            'an answer, taught by the Refuge of the World.'
        ),
    },
    'mangala-suttam-pathamam': {
        'background': (
            'The book prints its source and calls this the first Maṅgala Sutta, '
            'since the text appears again later. A radiant deity comes to the '
            "Buddha at Jeta's Grove in the night to ask its question."
        ),
        'meaning': (
            'Asked what the highest blessing is, the Buddha gives a list that '
            'starts where anyone can: avoiding fools and keeping wise company. It '
            'moves through learning, caring for parents and family, honest work, '
            'generosity, humility and gratitude. Those who live like this go safely '
            'everywhere: safety follows from conduct, even as the text is chanted '
            'for protection.'
        ),
    },
    'bot-khat-ratana-suttam': {
        'background': (
            'This is the longest of the introductory verses. Before introducing the '
            "sutta, it sums up the Buddha's whole career: the perfections fulfilled "
            'over many lives, his birth, going forth, striving and victory over '
            'Māra.'
        ),
        'meaning': (
            'It sets out the power standing behind the text, then names what the '
            'sutta once did: swiftly end a threefold fear of disease, spirits and '
            'famine. Its argument for chanting the sutta is historical, resting on '
            'what it is said to have done before.'
        ),
    },
    'ratana-suttam-dutiyam': {
        'background': (
            'The book prints its source, and calls this the second Ratana Sutta '
            'because the text appears again later. It is the plainest example of '
            'how a paritta works: each verse states a truth and asks for well-being '
            'because of it.'
        ),
        'meaning': (
            'It opens by asking all beings present, of earth or sky, to listen with '
            'glad minds. Each verse then praises a quality of the Buddha, Dhamma or '
            "Sangha as a jewel and ends 'by this truth may there be well-being'. It "
            'closes by saluting the Tathāgata with the same beings it first '
            'summoned.'
        ),
    },
    'bot-khat-karaniyametta-suttam': {
        'background': (
            'This introduction says why the Karaṇīya-metta Sutta matters by listing '
            'its results, and what it promises is unusually homely: an untroubled '
            'night.'
        ),
        'meaning': (
            'By its power, frightening spirits show nothing fearful. Whoever '
            'practises it day and night without tiring sleeps happily and sees no '
            'bad dreams. The condition is continuous practice, not recitation: the '
            'protection and the practice are the same thing.'
        ),
    },
    'karaniyametta-suttam-tatiyam': {
        'background': (
            "The book prints its source; 'the third' refers to its place in the "
            'Tamnan. It is one of the few texts in the book used as much outside '
            'chanting as within it, because it sets out a practice in order.'
        ),
        'meaning': (
            'It begins with character: capable, upright, gentle, humble, content, '
            'with few duties and calm senses. Only then does loving-kindness extend '
            'to every living being, seen or unseen, near or far, as a mother would '
            'protect her only child. Kept in mind in every posture, this is the '
            'divine abiding, and it leads beyond rebirth.'
        ),
    },
    'bot-khat-khandha-chaddanta-parittam': {
        'background': (
            'This introductory verse alone introduces two chants: a declaration of '
            'loving-kindness towards snakes, and a story about an elephant. Both '
            'concern an animal and a danger.'
        ),
        'meaning': (
            'It calls the chants a divine spell and antidote against venomous '
            'creatures, destroying poison and every other danger for all beings. '
            "The words 'within its domain' keep the claim honest: the protection "
            'holds within a range, not everywhere.'
        ),
    },
    'khandha-parittam-catuttham': {
        'background': (
            'The book prints its source. The chant addresses four snake families by '
            'name, which is why it is used where snakes are a real danger. Nothing '
            'is commanded or driven off: loving-kindness is declared, and safety is '
            'said to follow.'
        ),
        'meaning': (
            'It offers loving-kindness to the four snake families and to all '
            'creatures, footless, two-footed, four-footed and many-footed, then '
            'asks that none of them harm the speaker, in the same words and order. '
            'It closes with homage to the Buddha and the seven Buddhas of the past.'
        ),
    },
    'chaddanta-parittam': {
        'background': (
            'This is the shortest paritta in this stretch and the only purely '
            "narrative one, a scene from a story of the Buddha's past life as an "
            'elephant. A hunter has come to kill him for his tusks, disguised in a '
            "monk's robe."
        ),
        'meaning': (
            'As he is struck, the elephant sees the ochre robe and thinks: the '
            'banner of the arahants is not to be harmed by the good. He holds to '
            'what the robe means even as it is used against him. The chant offers '
            'that restraint, shown while pierced and in pain, as the thing worth '
            'having power in the world.'
        ),
    },
    'bot-khat-mora-parittam': {
        'background': (
            'This verse introduces a paritta from a past life in which the Buddha '
            'was a peacock. It is the second of three animal parittas in a row.'
        ),
        'meaning': (
            'Hunters tried for a long time to catch the peacock and never could. '
            'The verse is careful that the protection came from the paritta, not '
            "the bird, and calls it a 'Brahma-spell', an old and frank word for "
            'what a paritta is.'
        ),
    },
    'mora-parittam-pancamam': {
        'background': (
            'This chant has two matched halves: one salutes the rising sun and asks '
            'for safety through the day, the other salutes the setting sun and asks '
            'for safety through the night. The peacock is said to have chanted them '
            'on waking and before sleeping.'
        ),
        'meaning': (
            'The sun is greeted warmly as a benefactor, not worshipped as a god, '
            'and protection is also asked of the wise. Each half pays homage to the '
            'Buddhas, to awakening, to the liberated and to liberation. It ends '
            'simply, with the peacock settling down to rest.'
        ),
    },
    'bot-khat-vattaka-parittam': {
        'background': (
            'The third animal paritta comes from a past life in which the Buddha '
            'was a quail. The verse adds that the Buddha told this story to '
            'Sāriputta.'
        ),
        'meaning': (
            'By the power of this paritta a forest fire turned aside from the Great '
            'Being. The verse says it is of great power and lasts an aeon, a claim '
            'deliberately out of proportion to a small bird that could neither fly '
            'nor walk.'
        ),
    },
    'vattaka-parittam-chattham': {
        'background': (
            "This is the book's clearest example of an act of truth: a formal "
            'statement of something true, made so that its truth will have an '
            'effect.'
        ),
        'meaning': (
            'It first affirms that virtue, truth, purity and compassion have force '
            'in the world. The quail chick then states its helplessness exactly: it '
            'has wings but cannot fly, feet but cannot walk. The fire spares the '
            'area as a flame dies at water. What the chick practised was the '
            'perfection of truth: accuracy.'
        ),
    },
    'bot-khat-dhajagga-suttam': {
        'background': (
            'This verse opens with the image the sutta is known for: by merely '
            'recalling it, even creatures in mid-air find a footing, as if on solid '
            'ground. It is chanted for someone with nothing solid beneath them.'
        ),
        'meaning': (
            'It claims that countless beings have been freed from misfortunes '
            'caused by spirits, thieves and the like, a claim about the past rather '
            'than a promise. The key word is recollection: the protection comes '
            'from calling something to mind, which the sutta goes on to explain.'
        ),
    },
    'dhajagga-parittam-sattamam': {
        'background': (
            'The book prints its source. Dhajagga means the top of a banner. The '
            'Buddha recounts the advice the god Sakka gave his devas when afraid, '
            'then explains why it was not good enough.'
        ),
        'meaning': (
            'Sakka told the frightened devas to look at his banner, but he is not '
            'free of greed, hatred and delusion and is fearful himself, so the '
            'advice may not work. The Buddha offers instead the recollection of the '
            'Buddha, Dhamma or Sangha: then there will be no fear, no trembling and '
            'no hair standing on end.'
        ),
    },
    'bot-khat-atanatiya-parittam': {
        'background': (
            'This introduction is unusual in admitting a problem: some beings are '
            'not convinced by the teaching and keep doing harm.'
        ),
        'meaning': (
            "The Buddha's response was given simply for the safety and protection "
            'of his followers, not to convert anyone. It is the most defensive text '
            'in the collection, which is why the chant that follows is largely a '
            'list of names: if a being cannot be reasoned with, what remains is '
            'knowing who outranks them.'
        ),
    },
    'atanatiya-parittam-atthamam': {
        'background': (
            'The book prints its source. The chant opens by naming the seven '
            'Buddhas of the past, each with his own epithet. Naming is its method: '
            'it establishes protection by reciting who holds authority.'
        ),
        'meaning': (
            'It asserts that these names are known and that harmful beings are '
            'subject to them, so harm should not come; it is the least meditative '
            'text in the collection. It ends gently: may no obstacle be yours, and '
            'for one who honours elders, four things grow: long life, beauty, '
            'happiness and strength.'
        ),
    },
    'bot-khat-angulimala-parittam': {
        'background': (
            'This is the most specific introduction: it names one use, the safe '
            'birth of a child. It also describes a physical practice, in which '
            'water used to wash the seat of the reciter is itself held to remove '
            'danger.'
        ),
        'meaning': (
            'Power here is treated as something that settles on a place and can be '
            'carried in a bowl, a very concrete idea of blessing. Because '
            'childbirth is a recurring need that cannot wait, this paritta has '
            "stayed in constant use. Like the quail's chant, it is said to be of "
            'great power and to last an aeon.'
        ),
    },
    'angulimala-parittam-navamam': {
        'background': (
            'This is the shortest text in the Tamnan and among the most used: three '
            'sentences, said three times. Who speaks it matters: Aṅgulimāla had '
            "been a murderer who wore a garland of his victims' fingers before he "
            'was ordained.'
        ),
        'meaning': (
            "He says that since his 'noble birth', his ordination, he is not aware "
            'of having intentionally killed any living being. He does not claim '
            'never to have killed; he dates his claim and vouches only for what he '
            'knows. By that carefully limited truth, he wishes well-being to the '
            'mother and her child.'
        ),
    },
    'bot-khat-bojjhanga-parittam': {
        'background': (
            'The seven factors of awakening appeared earlier as three discourses '
            'chanted at sickbeds. Here they return as a paritta, and the '
            'introduction explains why.'
        ),
        'meaning': (
            "The seven factors crush Māra's army and lead those who develop them to "
            'the unborn, ageless, deathless and fearless. Only then does it turn to '
            "use, calling the text 'a medicine and a spell'. The two words sit side "
            'by side without apology, and the chant is used as both.'
        ),
    },
    'bojjhanga-parittam-dasamam': {
        'background': (
            'The last of the ten parittas compresses the three earlier Bojjhaṅga '
            'discourses, to Mahākassapa, Mahāmoggallāna and Mahācunda, into a few '
            'verses to be chanted over someone who is ill.'
        ),
        'meaning': (
            'It names the seven factors of awakening, leading to Nibbāna, with the '
            "refrain 'by this utterance of truth may you be well always'. It "
            'recalls all three recoveries together: the illnesses went the way '
            'defilements go when struck down by the path, never to return.'
        ),
    },
    'bot-khat-abhaya-parittam': {
        'background': (
            'This is the shortest introduction in the collection, three lines long; '
            'by this point in a service the introductions have grown brief. It '
            'openly promises worldly benefits.'
        ),
        'meaning': (
            'It names merit, majesty, beauty and fame together, without '
            'embarrassment, and asks that all beings listen. It calls the chant '
            "arisen 'for the good of self and others', the tradition's usual answer "
            'to the charge that such requests are selfish.'
        ),
    },
    'abhaya-parittam-ekadasamam': {
        'background': (
            'Abhaya means without fear, and the chant is named for what it is meant '
            'to produce. It is four lines said three times, by the power of the '
            'Buddha, the Dhamma and the Sangha.'
        ),
        'meaning': (
            'It names ill omens, unlucky signs, an unwelcome bird call, a bad '
            'planet and a disturbing dream: signs that frighten rather than real '
            'dangers. It asks that they come to nothing, aiming at the fear itself, '
            'which is what actually helps someone who cannot stop thinking about a '
            'dream.'
        ),
    },
    'devata-uyyojana-gatha': {
        'background': (
            'The service opened by inviting the devas of every world; these verses '
            'formally send them away again. A gathering that was formally opened '
            'has to be formally closed.'
        ),
        'meaning': (
            'It first wishes that all who suffer, fear or grieve be free of it. It '
            "then shares the merit gathered, 'by this much', with the devas, "
            'without claiming how much there was. Finally it wishes the departing '
            'devas a practice of their own: to give with faith and always keep the '
            'precepts.'
        ),
    },
    'bot-khat-jaya-parittam': {
        'background': (
            'This last introduction in the Twelve Tamnan returns to the scene under '
            'the Bodhi tree, stressing not the awakening but its defence against '
            'Māra.'
        ),
        'meaning': (
            "Māra's army came on twelve leagues deep on every side, and the Buddha "
            'scattered it through patience and loving-kindness, qualities anyone '
            'could practise. The verse closes by asking safety, welfare and '
            'happiness for all beings, not only for those chanting.'
        ),
    },
    'jaya-parittam-dvadasamam': {
        'background': (
            'The last of the twelve parittas begins with the same verses as the '
            'Victory Protection verses printed earlier, so the text appears twice '
            'in the book. This version adds closing verses not found there.'
        ),
        'meaning': (
            'As the Buddha fulfilled the perfections and won victory under the '
            'Bodhi tree, so may you be victorious; the blessing works by likeness, '
            'not transfer. Its closing verses turn to the people in the room, '
            'wishing them health and happiness with their kin and success in the '
            "Buddha's teaching."
        ),
    },
    'ratanattayappabhavabhiyacana-gatha': {
        'background': (
            'This is one of the few chants in the book that argues rather than '
            'declares. Like the earlier verses on the power of the Triple Gem, it '
            'later turns to Siam and its rulers, so it belongs to the same modern '
            'layer.'
        ),
        'meaning': (
            'The Buddha, Dhamma and Sangha are separate yet one: the Buddha awakens '
            "to the Dhamma, the Sangha upholds it, and the Sangha are the Buddha's "
            'disciples, so none can stand without the others. It ends by asking, '
            'three times, that success come to those whose hearts rest in faith in '
            'the Triple Gem.'
        ),
    },
    'sukhabhiyacana-gatha': {
        'background': (
            'This companion to the previous verses simply asks, and asks for '
            'worldly happiness. It is addressed first to the royal house, one of '
            'the few chants in the book written for a kingdom.'
        ),
        'meaning': (
            'By the power of everything already chanted, it asks happiness for the '
            'royal house, and offers the gift of Dhamma to the local guardian devas '
            'in return for their protection. It ends asking that rulers guard their '
            'people as parents guard a child, and do so by Dhamma, lawfully.'
        ),
    },
    'mongkhon-chakkrawan-yai': {
        'background': (
            'This is the longer companion to the Lesser Universal Blessing, built '
            'the same way by accumulation. The line printed after it closes the '
            'whole Twelve Tamnan collection.'
        ),
        'meaning': (
            'It invokes the thirty-two marks of a Great Man in one very long '
            'compound, then the guardians of sky, mountains, forests, earth, rivers '
            'and oceans, so nowhere is left unprotected. It closes by warding off '
            'bad planets and harmful spirits, ending the collection with the '
            'unseen, where it began.'
        ),
    },
    'bot-khat-dasanathakarana-dhamma-suttam': {
        'background': (
            'Nātha is a refuge or protector, and the ten things this discourse '
            'names are what make one. The introduction plays on the two senses: the '
            'Buddha is a refuge, and he taught how to have one.'
        ),
        'meaning': (
            'It calls the Buddha a refuge for the world, who taught so that his '
            'disciples could become people with a refuge of their own, less '
            'dependent on him. The reciters chant it so that they themselves may '
            'become established as ones with a refuge.'
        ),
    },
    'dasanathakarana-dhamma-suttam': {
        'background': (
            'This discourse, spoken at Sāvatthī, gives ten qualities that make a '
            "person a refuge for themselves, each introduced with 'and further, "
            "monks'."
        ),
        'meaning': (
            'It begins with virtue and learning, then turns to living with others: '
            'good friends, being easy to speak to and accepting correction, and '
            "helping one's fellows with their duties. It closes: dwell as those who "
            'have a refuge, not without one, for one without a refuge lives in '
            'suffering.'
        ),
    },
    'bot-khat-abhinha-paccavekkhana-patha': {
        'background': (
            'This verse introduces the full discourse on the five reflections: '
            "ageing, sickness, death, separation, and ownership of one's actions. "
            'Its claim is practical: the reflections do something.'
        ),
        'meaning': (
            "It calls the Buddha 'he of the five stainless eyes' and says each of "
            'the five themes accomplishes its own purpose when properly practised '
            'by those who follow the teaching. It is practising them, not merely '
            'reciting them, that brings results.'
        ),
    },
    'abhinha-paccavekkhana-patha': {
        'background': (
            'The book prints the five reflections twice: elsewhere as bare '
            'formulas, here as the whole discourse with its reasoning. It cites its '
            'source, and says the reflections are for anyone, woman or man, lay or '
            'ordained.'
        ),
        'meaning': (
            'I am subject to ageing, sickness and death; I will be separated from '
            'all that is dear; I own my actions. Each reflection is given a '
            'purpose, undercutting a particular pride or correcting conduct. It '
            'ends by saying the same of all beings, which is where it stops being '
            'only about oneself.'
        ),
    },
    'bot-khat-maggavibhanga-suttam': {
        'background': (
            "This introduction uses the word 'path' four times in four senses, and "
            'the repetition is its argument.'
        ),
        'meaning': (
            'The world does not know which path leads out of suffering. The Buddha '
            'points out the path because he realised it and travelled it himself: a '
            'guide who has made the journey, not one with a map. The discourse is '
            'recited to deepen faith, straighten view and bring well-being.'
        ),
    },
    'maggavibhanga-suttam': {
        'background': (
            'The book prints its source. This discourse defines each of the eight '
            'factors of the path in turn, in the same form each time, with no story '
            'or simile.'
        ),
        'meaning': (
            'The definitions are plain: right view is knowing the four noble '
            'truths; right speech is abstaining from lies, malice, harshness and '
            'idle talk. The last factors describe effort, mindfulness and '
            'concentration in action. Chanted straight through, it gives the whole '
            'path in eight sentences.'
        ),
    },
    'atthangikamagga-gatha': {
        'background': (
            'The book prints the source of these verses, which follow the discourse '
            'defining the eightfold path. Where that analysed, these urge, and they '
            'are among the most quoted verses in the tradition.'
        ),
        'meaning': (
            'The eightfold path is the best of paths and the only one for purifying '
            "vision: follow it, and Māra's army is bewildered. Then the line that "
            'qualifies everything: you must make the effort yourselves; the Buddhas '
            'only show the way.'
        ),
    },
    'bot-khat-karaniyakaraniya-suttam': {
        'background': (
            "This introduction gives the discourse's purpose in one pairing: that "
            'what should not be done be abandoned and what should be done be done. '
            "The listener is Ānanda, the Buddha's attendant."
        ),
        'meaning': (
            "The Buddha trains those who can be trained 'in the path of happiness'. "
            "'Should be done' and 'should not be done' together cover the whole of "
            'conduct, and the discourse is recited so as to act on it, not as '
            'merit.'
        ),
    },
    'karaniyakaraniya-suttam': {
        'background': (
            'The book prints its source. This is one of the shortest discourses in '
            'the collection: the Buddha makes a statement and Ānanda asks him to '
            'expand it.'
        ),
        'meaning': (
            'The Buddha, who usually says questions need careful distinguishing, '
            'states this categorically: good conduct of body, speech and mind '
            'should be done. Ānanda asks what follows from such conduct, turning '
            'one plain claim into a discourse.'
        ),
    },
    'bot-khat-aggappasada-suttam': {
        'background': (
            'This introduction turns on one word, agga, the foremost, used in '
            'almost every line. It sets up a proportion: faith in the best brings '
            'the best.'
        ),
        'meaning': (
            'Of all things reckoned foremost, the Buddha, the Dhamma and the Sangha '
            'are the highest, and faith placed in them brings a foremost result. It '
            'recommends not faith in general but faith placed carefully, so that it '
            'rests on the foremost alone.'
        ),
    },
    'aggappasada-suttam': {
        'background': (
            'The book prints its source. Parts of this discourse also appear in the '
            'protection passage near the front of the book. Its method is to take '
            'the widest possible category and name one member of it as foremost.'
        ),
        'meaning': (
            'Of all beings, the Buddha is foremost; of all things, dispassion; of '
            'all conditioned things, the noble eightfold path; of all communities, '
            'the Sangha. The closing verses say that whoever gives to the foremost, '
            'as god or human, reaches the foremost: faith placed in the best is '
            'treated, openly, as an investment.'
        ),
    },
    'bot-khat-chasaraniyadhamma-suttam': {
        'background': (
            "This introduction calls the Buddha a 'maker of concord', an epithet "
            'found nowhere else in the book. What follows is a text about living '
            'together.'
        ),
        'meaning': (
            'The discourse is for affection, respect, cohesion, freedom from '
            'dispute and unity, all social rather than individual goods. These lead '
            'onward for monks who practise by the Dhamma, and the assembly recites '
            'it in order to act on it.'
        ),
    },
    'chasaraniyadhamma-suttam': {
        'background': (
            'Six qualities a community should keep in mind about itself, each '
            "ending 'this too is a state to be remembered'."
        ),
        'meaning': (
            "The first three are acts of loving-kindness towards one's fellows in "
            'body, speech and mind, both openly and in private, the same when '
            'nobody is watching. The fourth is sharing whatever one receives, down '
            "to the contents of one's bowl. The last two are holding the same "
            'virtues and the same view: a community also rests on agreeing about '
            'what is true.'
        ),
    },
    'bot-khat-bhikkhu-aparihaniyadhamma-suttam': {
        'background': (
            'A four-line introduction whose subject is named by a negative: the '
            'things that do not lead to decline.'
        ),
        'meaning': (
            'The Buddha is described by his motive: great compassion and the wish '
            "for his disciples' growth in the Dhamma. He declared the conditions "
            'for avoiding decline, and the assembly recites them so as to practise '
            'them.'
        ),
    },
    'bhikkhu-aparihaniyadhamma-suttam': {
        'background': (
            "Spoken at Rājagaha on the Vulture's Peak, this discourse gives seven "
            "conditions, each beginning 'so long as'. None concern meditation; all "
            'concern how a community conducts its affairs.'
        ),
        'meaning': (
            'So long as monks meet often, act in harmony, neither invent new rules '
            'nor abolish old ones, respect their elders, resist craving, value '
            'forest dwellings and care for fellow monks yet to come, growth can be '
            'expected, not decline. Inventing requirements harms a community as '
            'much as abandoning them.'
        ),
    },
    'bot-khat-pahana-bhavana-suttam': {
        'background': (
            'A short introduction built on the pair its title names: abandoning and '
            'developing, treated as two halves of one task.'
        ),
        'meaning': (
            'The Buddha, out of great compassion, showed what can actually be done '
            'in abandoning the unwholesome and developing the wholesome. The '
            'discourse is recited for the sake of right practice, so that hearing '
            'it, we may act on it.'
        ),
    },
    'pahana-bhavana-suttam': {
        'background': (
            'This is one of the shortest discourses in the book, built on a single '
            'condition the Buddha states twice.'
        ),
        'meaning': (
            'Abandon the unwholesome; develop the wholesome. It can be done: if it '
            'could not, the Buddha would not ask it. By ruling out asking for the '
            'impossible, the discourse closes off the excuse that the task was '
            'never possible.'
        ),
    },
    'bot-khat-caturappamanna-patha': {
        'background': (
            'Appamaññā means immeasurable: these four practices are named so '
            'because their range, all beings, has no measure.'
        ),
        'meaning': (
            'The introduction pairs each practice with what it cures: '
            'loving-kindness answers ill will, compassion answers cruelty, gladness '
            'answers discontent, and equanimity answers aversion. Knowing which '
            'state one is in shows which of the four to develop.'
        ),
    },
    'caturappamanna-patho': {
        'background': (
            'Each of the four immeasurables is given the same long paragraph with '
            'one word changed. The repetition is the practice itself.'
        ),
        'meaning': (
            'One dwells pervading each direction in turn, then above, below and all '
            'around, with a heart full of loving-kindness, then compassion, then '
            'gladness, then equanimity. Chanted, it is not a description of the '
            'practice but the practice being done while it is spoken.'
        ),
    },
    'bot-khat-dhammaniyama-suttam': {
        'background': (
            'Dhammaniyāma is the fixed order of things: what holds true whether or '
            'not anyone notices it.'
        ),
        'meaning': (
            'The verse calls this the knowledge that comes before the knowledge of '
            'Nibbāna, and names its content: impermanence, suffering and not-self. '
            'The three characteristics are not a conclusion reached at the end of '
            'the path but what must be seen first.'
        ),
    },
    'dhammaniyama-suttam': {
        'background': (
            'This short discourse is among the most compressed and most important '
            "in the collection. The book's order for funeral observances names it "
            'for the second and third weeks after a death.'
        ),
        'meaning': (
            'Whether or not Buddhas arise, it stands as the fixed order of things: '
            'all formations are impermanent, all formations are suffering, all '
            'things are not-self. The Buddha discovers this rather than decrees it. '
            "The last line widens from 'formations' to 'all things', a difference "
            'that matters at a death.'
        ),
    },
    'bot-khat-anattalakkhana-suttam': {
        'background': (
            'This introduction admits difficulty in its first line: the mark of '
            'not-self is hard for beings to know.'
        ),
        'meaning': (
            'The discourse frees one from both the doctrine of a self and the '
            'perception of self, two different targets. It was first taught to '
            'those who had already seen the truth, for deeper understanding; it is '
            'recited for all who wish to practise, that their aim be accomplished.'
        ),
    },
    'anattalakkhana-suttam': {
        'background': (
            'Spoken at Benares in the Deer Park to the same five monks who heard '
            'the first sermon, this is by tradition the second teaching. The book '
            'names it for the seventh day after a death.'
        ),
        'meaning': (
            'The argument is made for each of the five aggregates: if form were '
            'self, it would not bring affliction and we could command it to be as '
            'we wish. None of the five obeys, so none is self. Seeing this brings '
            'disenchantment and release, and the minds of the five monks were freed '
            'as it was spoken.'
        ),
    },
    'bot-khat-adittapariyaya-suttam': {
        'background': (
            'This introduction names its audience: a thousand monks at Gayā who had '
            'been fire-worshipping ascetics, and so were taught in the language of '
            'fire.'
        ),
        'meaning': (
            'The Buddha, skilled in taming those who can be led, taught each '
            'according to what they had practised. The discourse on burning is '
            'offered to the reciters as a way into the truth of suffering.'
        ),
    },
    'adittapariyaya-suttam': {
        'background': (
            'Spoken at Gayā to a thousand monks, this is by tradition the third '
            'teaching. The book names it for the fiftieth day after a death.'
        ),
        'meaning': (
            'All is burning: the eye, forms, eye-consciousness, eye-contact and '
            'every feeling arising from them, and the same for ear, nose, tongue, '
            'body and mind. Burning with greed, hatred and delusion. Seeing this, '
            "the disciple turns away in disenchantment, and the thousand monks' "
            'minds were freed as it was spoken.'
        ),
    },
    'bot-khat-satipatthana-patha': {
        'background': (
            "This introduction turns on the phrase 'the one way', repeated in the "
            'passage that follows.'
        ),
        'meaning': (
            'It lists what the practice is for before naming it: purifying defiled '
            'minds, going beyond sorrow and lamentation, and ending pain and grief. '
            'Only then does it name the foundations of mindfulness, a remedy '
            'identified by what it cures.'
        ),
    },
    'satipatthana-patho': {
        'background': (
            'This is the short form of the foundations of mindfulness. The full '
            'discourse follows soon after, with the same structure at far greater '
            'length.'
        ),
        'meaning': (
            'One dwells contemplating body, feelings, mind and mental objects, '
            'ardent, clearly comprehending and mindful, putting aside craving and '
            'grief, inwardly, outwardly or both. It is the one way by which people '
            'crossed over before, cross now and will cross in future.'
        ),
    },
    'mahasatipatthana-sutta-patho': {
        'background': (
            'The book prints its source. This is the full discourse on the '
            'foundations of mindfulness, over thirty printed pages long, and the '
            'practice tradition of this book rests on it.'
        ),
        'meaning': (
            'It is the one way to purify beings, overcome sorrow and realise '
            'Nibbāna. The four foundations are worked through: breath, posture, the '
            "body's parts, feelings, states of mind and mental objects, each "
            'observed arising and passing away. It ends with a graded promise: '
            'practised this way for seven years, or months, or even seven days, it '
            'bears fruit.'
        ),
    },
    'bot-khat-dhammacakkappavattana-suttam': {
        'background': (
            'This introduces the discourse the tradition counts as the first '
            'teaching. Unusually, it summarises the content rather than the '
            'occasion, and ends with a note on how to chant it: as prose.'
        ),
        'meaning': (
            'In five lines it gives the whole: the Wheel of Dhamma set rolling and '
            'unstoppable, the two extremes, the middle way, and the knowledge and '
            'vision of the four noble truths.'
        ),
    },
}
