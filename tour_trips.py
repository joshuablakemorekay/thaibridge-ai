"""Tour Guide trips — short journeys you play through in Thai.

WHY THIS EXISTS
---------------
The Tour Guide page used to be a word list: 25 useful words in six boxes. Good
reference, but nothing to DO. A list of places to visit would have been the
obvious addition, and the wrong one: prices, opening hours and ferry times go
stale, and the app would quietly turn into a travel website that needs
re-checking every month.

So each trip is a place used as a SETTING for language, not a listing. You ride
a red truck up Doi Suthep, haggle for a longtail boat in Krabi, order som tam in
Phimai. At every stop someone says something in Thai and you pick the right
reply. The words are the ones on the phrasebook below, plus a few new ones each
trip, met in the situation where you would actually need them.

At least one trip in each of the six regions the Tourism Authority of Thailand
uses (North, Central, Northeast, East, South, West), so the whole country is
covered. The North has two, Chiang Mai and Chiang Rai, because Josh asked for
Chiang Rai by name and it is a different day out from Doi Suthep.

PHOTOS
------
One photo per trip, from Wikimedia Commons under a Creative Commons licence
that allows reuse with credit. Each trip's `photo` keeps the photographer,
licence and source page, and the page prints that credit under the image:
BY and BY-SA licences require it. The files are shrunk to 1000px WebP in
static/img/tour/. To swap a photo, keep to the same licences (no NC or ND).

WHAT IS DELIBERATELY LEFT OUT
-----------------------------
No real prices, fees, opening hours or timetables. Where a character names a
price, it is story money, and the scene says so. Nothing on this page can go
out of date.

⚠️  DRAFT THAI — every Thai line below is a first draft awaiting review by Josh
and teacher Paiboon, like survival.py. Nothing here is final.

HOW THE POLITE ENDINGS WORK
---------------------------
A learner's own lines end with a polite particle, and it depends on who is
speaking AND on the kind of sentence:

    man, any sentence        ครับ  kráp
    woman, statement         ค่ะ   kâ
    woman, question          คะ    ká

The ค่ะ/คะ split is a classic learner mistake, so it is built in rather than
glossed over. A line marks where the particle goes with {s} (statement) or {q}
(question), in both the Thai and the Paiboon. The page asks "how do you speak?"
once and fills them in. Lines spoken by the people you meet are fixed, because
their gender is part of the story.
"""

# Particle forms for the {s} / {q} markers in a learner's line.
PARTICLES = {
    'male':   {'s': ('ครับ', 'kráp'), 'q': ('ครับ', 'kráp')},
    'female': {'s': ('ค่ะ', 'kâ'),   'q': ('คะ', 'ká')},
}


def _c(thai, paiboon, english, verdict, reply):
    """One answer the learner can pick.

    verdict is 'good' (right), 'ok' (understood, with a catch) or 'miss'
    (wrong — the page offers another go)."""
    return {'thai': thai, 'paiboon': paiboon, 'english': english,
            'verdict': verdict, 'reply': reply}


def _scene(stop, place, title, narration, prompt, choices, tip,
           who='', thai='', paiboon='', english=''):
    """One stop on a trip. `who/thai/paiboon/english` is what someone says to
    you; leave it empty when the scene opens with you speaking first."""
    return {'stop': stop, 'place': place, 'title': title,
            'narration': narration, 'prompt': prompt, 'choices': choices,
            'tip': {'title': tip[0], 'text': tip[1]},
            'who': who, 'thai': thai, 'paiboon': paiboon, 'english': english}


TRIPS = [
    # ── North ────────────────────────────────────────────────────────────
    {
        'key': 'doi-suthep',
        'region': 'North',
        'title': 'A morning at Doi Suthep',
        'place': 'Chiang Mai',
        'place_thai': 'วัดพระธาตุดอยสุเทพ',
        'place_paiboon': 'wát prá-tâat dɔɔi sù-têep',
        'place_english': 'The temple of the relic on Suthep mountain',
        'blurb': 'Ride a red truck up the mountain, visit Chiang Mai’s best-known '
                 'temple, and come back down for khao soi.',
        'stamp': 'ดอยสุเทพ',
        'photo': {
            'file': 'img/tour/doi-suthep.webp',
            'alt': 'The golden chedi of Wat Phra That Doi Suthep under a blue sky',
            'artist': 'เทวประภาส มากคล้าย',
            'license': 'CC BY 3.0',
            'license_url': 'https://creativecommons.org/licenses/by/3.0',
            'source': 'https://commons.wikimedia.org/wiki/File:Phra_That_Doi_Suthep_01.jpg',
        },
        'stops': ['University gate', 'Red truck', 'Naga stairs', 'The temple', 'Khao soi'],
        'tutor': 'restaurant',
        'tutor_line': 'The AI tutor plays a cook in a Thai restaurant. Order in your own words.',
        'scenes': [
            _scene(0, 'Outside Chiang Mai University', 'Find a red truck',
                   'A row of red pickup trucks waits by the university gate. These are '
                   'rót-dɛɛŋ, shared taxis that go up the mountain once enough people '
                   'climb in. A driver leans out.',
                   'Tell him where you want to go.',
                   [_c('ไปดอยสุเทพ{s}', 'bpai dɔɔi sù-têep {s}', 'To Doi Suthep.', 'good',
                       'He nods at the back bench. You are going up the mountain.'),
                    _c('ไปโรงแรม{s}', 'bpai rooŋ-rɛɛm {s}', 'To the hotel.', 'miss',
                       'He looks puzzled. Which hotel? There are hundreds. Name the place.'),
                    _c('เลี้ยวซ้าย{s}', 'líao sáai {s}', 'Turn left.', 'miss',
                       'You have not even set off yet. Directions come later.')],
                   ('Say the place, then the polite ending',
                    'ไป + place is all you need. ไปดอยสุเทพ is literally "go Doi Suthep". '
                    'Thai drops the little words English needs.'),
                   who='Driver', thai='ไปไหนครับ', paiboon='bpai nǎi kráp',
                   english='Where are you going?'),
            _scene(1, 'At the back of the truck', 'Agree the price first',
                   'Before you climb in, settle the fare. Locals always do this, and '
                   'drivers expect it.',
                   'Ask how much it costs.',
                   [_c('เท่าไหร่{q}', 'tâo-rài {q}', 'How much?', 'good',
                       'หกสิบบาทครับ (hòk-sìp bàat kráp), "Sixty baht." That is story '
                       'money. Real fares change, so always ask.'),
                    _c('แพง{s}', 'pɛɛŋ {s}', 'Expensive.', 'miss',
                       'He has not told you a price yet. Ask first, then react.'),
                    _c('อร่อย{s}', 'à-rɔ̀i {s}', 'Delicious.', 'miss',
                       'He laughs. That is a food word. Save it for lunch.')],
                   ('Why ask before you get in',
                    'Once you are sitting down it is too late to agree a price. The same '
                    'habit works for tuk-tuks and motorbike taxis.')),
            _scene(1, 'Still at the truck', 'Haggle, or not',
                   'Sixty baht. You can accept, or try for a little less. Neither is wrong.',
                   'What do you say?',
                   [_c('ลดได้ไหม{q}', 'lót dâi mǎi {q}', 'Can you lower it?', 'good',
                       'He grins. ห้าสิบบาท (hâa-sìp bàat), "Fifty." Smiling while you '
                       'asked is what made that work.'),
                    _c('โอเค{s}', 'oo-kee {s}', 'OK.', 'good',
                       'Easy. You climb in and the truck starts winding up the mountain.'),
                    _c('ถูก{s}', 'tùuk {s}', 'Cheap.', 'ok',
                       'He smiles. Calling his price cheap means yes, but it also tells '
                       'him you would have paid more.')],
                   ('ถูก has two meanings',
                    'ถูก means "cheap", and it also means "correct". You will hear '
                    'ถูกต้อง (tùuk-dtɔ̂ŋ), "that is right", all the time.'),
                   who='Driver', thai='หกสิบบาทครับ', paiboon='hòk-sìp bàat kráp',
                   english='Sixty baht.'),
            _scene(2, 'Foot of the naga staircase', 'Three hundred steps',
                   'The truck stops at a long staircase lined with serpents, the nâak. '
                   'You climb about 300 steps. At the top is a ticket window for '
                   'foreign visitors.',
                   'Ask the woman at the window how much the entrance fee is.',
                   [_c('ค่าเข้าเท่าไหร่{q}', 'kâa-kâo tâo-rài {q}', 'How much is the entrance fee?', 'good',
                       'อยู่ที่ป้ายค่ะ (yùu tîi bpâai kâ), "It is on the sign." She points. '
                       'She understood you perfectly.'),
                    _c('กุญแจ{s}', 'gun-jɛɛ {s}', 'Key.', 'miss',
                       'A key? That word belongs at the hotel.'),
                    _c('เช็คบิล{s}', 'chék-bin {s}', 'The bill, please.', 'miss',
                       'You have not eaten anything yet. This is a ticket, not a meal.')],
                   ('Before you go in',
                    'Cover your shoulders and knees. Shoes come off before you step into '
                    'a hall with Buddha images.'),
                   who='Sign by the window', thai='ค่าเข้า', paiboon='kâa-kâo',
                   english='Entrance fee'),
            _scene(3, 'The golden chedi', 'On the terrace',
                   'The golden chedi shines in the sun, and all of Chiang Mai is spread '
                   'out below. A Thai visitor sees you holding your phone at arm’s length.',
                   'Accept her offer.',
                   [_c('ได้{s} ขอบคุณ{s}', 'dâi {s}, kɔ̀ɔp-kun {s}', 'Yes please, thank you.', 'good',
                       'She takes three photos, then points at the view. You say สวยมาก '
                       '(sǔai mâak), "Very beautiful."'),
                    _c('ไม่เผ็ด{s}', 'mâi pèt {s}', 'Not spicy.', 'miss',
                       'She blinks. Wrong word list. You are thinking about lunch already.'),
                    _c('ช่วยด้วย', 'chûai dûai', 'Help!', 'miss',
                       'Everyone on the terrace turns round. ช่วยด้วย is for real emergencies.')],
                   ('Walking round the chedi',
                    'Walk round it clockwise, keeping it on your right. When you sit, tuck '
                    'your feet away so they never point at a Buddha image.'),
                   who='Thai visitor', thai='ถ่ายรูปให้ไหมคะ', paiboon='tàai-rûup hâi mǎi ká',
                   english='Shall I take a photo for you?'),
            _scene(4, 'A khao soi stall in town', 'Lunch',
                   'Back down the mountain, you stop for ข้าวซอย (kâao-sɔɔi), Chiang Mai’s '
                   'curry noodle soup. The cook looks up.',
                   'How spicy do you want it?',
                   [_c('ไม่เผ็ด{s}', 'mâi pèt {s}', 'Not spicy.', 'good',
                       'ได้ค่ะ (dâi kâ). There is chilli on the table if you change your mind.'),
                    _c('เผ็ดนิดหน่อย{s}', 'pèt nít-nɔ̀i {s}', 'A little spicy.', 'good',
                       'ได้ค่ะ. The safest answer anywhere in Thailand.'),
                    _c('เผ็ดมาก{s}', 'pèt mâak {s}', 'Very spicy.', 'ok',
                       'She raises an eyebrow and reaches for the chillies. Brave. Keep '
                       'your water close.')],
                   ('A new word: นิดหน่อย',
                    'นิดหน่อย (nít-nɔ̀i) means "a little". It is modest and polite, and it '
                    'goes with almost anything.'),
                   who='Cook', thai='เผ็ดไหมคะ', paiboon='pèt mǎi ká', english='Spicy?'),
            _scene(4, 'Same stall, empty bowl', 'Time to pay',
                   'The bowl is empty. Tell the cook it was good, and ask to pay.',
                   'Pick what to say.',
                   [_c('อร่อยมาก{s} เก็บเงินด้วย{s}', 'à-rɔ̀i mâak {s}, gèp ŋən dûai {s}',
                       'Delicious! Can I pay, please?', 'good',
                       'She beams. เก็บเงิน is what people say at street stalls.'),
                    _c('อร่อยมาก{s} เช็คบิล{s}', 'à-rɔ̀i mâak {s}, chék-bin {s}',
                       'Delicious! The bill, please.', 'good',
                       'That works too. เช็คบิล sounds more like a restaurant, but '
                       'everyone understands it.'),
                    _c('แพง{s}', 'pɛɛŋ {s}', 'Expensive.', 'miss',
                       'Ouch. That was a cheap bowl of noodles, and she made it for you.')],
                   ('Two ways to ask for the bill',
                    'เก็บเงินด้วย (gèp ŋən dûai), "please collect the money", at stalls. '
                    'เช็คบิล (chék-bin) in restaurants.')),
        ],
    },

    {
        'key': 'chiang-rai',
        'region': 'North',
        'title': 'White, blue and black in Chiang Rai',
        'place': 'Chiang Rai',
        'place_thai': 'วัดร่องขุ่น',
        'place_paiboon': 'wát rɔ̂ŋ-kùn',
        'place_english': 'Wat Rong Khun, the White Temple',
        'blurb': 'Three artists’ temples in a day: the White Temple, the Blue Temple '
                 'and the Black House, then the river where three countries meet.',
        'stamp': 'เชียงราย',
        'photo': {
            'file': 'img/tour/chiang-rai.webp',
            'alt': 'The White Temple, Wat Rong Khun, reflected in its pond',
            'artist': 'Chainwit',
            'license': 'CC BY 4.0',
            'license_url': 'https://creativecommons.org/licenses/by/4.0',
            'source': 'https://commons.wikimedia.org/wiki/File:Chiang_Rai_-_Wat_Rong_Khun_%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%A3%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B8%82%E0%B8%B8%E0%B9%88%E0%B8%99_(2026)_-_img_11.jpg',
        },
        'stops': ['Town', 'White Temple', 'Blue Temple', 'Black House', 'Golden Triangle'],
        'tutor': 'meeting',
        'tutor_line': 'The AI tutor plays a Thai traveller you have just met. Chat about your trip.',
        'scenes': [
            _scene(0, 'Chiang Rai clock tower', 'A ride out of town',
                   'The White Temple is about 13 kilometres south of town. A driver '
                   'waiting by the clock tower calls out to you.',
                   'Say yes, and ask how much.',
                   [_c('ไป{s} เท่าไหร่{q}', 'bpai {s}, tâo-rài {q}', 'Yes. How much?', 'good',
                       'He names a price for there and back, and waits while you look round. '
                       'Story money, as always.'),
                    _c('วัด{s}', 'wát {s}', 'Temple.', 'ok',
                       'He laughs. Chiang Rai has dozens of temples. He meant the white one, '
                       'and you still have not asked the price.'),
                    _c('ไม่ไป{s}', 'mâi bpai {s}', 'I’m not going.', 'miss',
                       'He shrugs and turns to the next tourist. That was a no.')],
                   ('Saying yes by repeating the verb',
                    'He asked ไปไหม, "going?". You answer ไป, "going", or ไม่ไป, "not going". '
                    'Two short sentences in a row is perfectly natural Thai.'),
                   who='Driver', thai='ไปวัดร่องขุ่นไหมครับ', paiboon='bpai wát rɔ̂ŋ-kùn mǎi kráp',
                   english='Going to the White Temple?'),
            _scene(1, 'Wat Rong Khun', 'The White Temple',
                   'The artist Chalermchai Kositpipat began rebuilding this temple in 1997, '
                   'in white plaster and mirror glass. You cross a bridge over hundreds of '
                   'sculpted hands reaching up from below. At the door of the main hall, '
                   'you lift your phone.',
                   'A guard stops you. Answer him.',
                   [_c('ขอโทษ{s}', 'kɔ̌ɔ-tôot {s}', 'Sorry.', 'good',
                       'He smiles and waves you in. The phone stays in your pocket.'),
                    _c('เข้าใจแล้ว{s}', 'kâo-jai lɛ́ɛo {s}', 'Understood.', 'good',
                       'He nods. Plenty to photograph outside.'),
                    _c('ถ่ายรูป{s}', 'tàai-rûup {s}', 'Take a photo.', 'miss',
                       'He shakes his head and points at the sign. That is exactly what he '
                       'just asked you not to do.')],
                   ('ห้าม: not allowed',
                    'ห้าม (hâam) means "forbidden", and you will see it on signs everywhere: '
                    'ห้ามถ่ายรูป no photos, ห้ามสูบบุหรี่ no smoking. ขอโทษ (kɔ̌ɔ-tôot) is '
                    '"sorry" and also "excuse me".'),
                   who='Guard', thai='ห้ามถ่ายรูปข้างในครับ', paiboon='hâam tàai-rûup kâaŋ-nai kráp',
                   english='No photos inside.'),
            _scene(2, 'Wat Rong Suea Ten', 'The Blue Temple',
                   'วัดร่องเสือเต้น (wát rɔ̂ŋ sʉ̌a dtên), "the temple of the dancing tiger", '
                   'is deep blue inside and out, with a white Buddha glowing at the end of '
                   'the hall. Outside, a stall sells little cloth bags in every colour.',
                   'Choose a colour.',
                   [_c('เอาสีฟ้า{s}', 'ao sǐi fáa {s}', 'The blue one, please.', 'good',
                       'Of course. She hands it over with a grin: blue, like the temple.'),
                    _c('เอาสีขาว{s}', 'ao sǐi kǎao {s}', 'The white one, please.', 'good',
                       'A souvenir of this morning’s temple. She wraps it for you.'),
                    _c('เอาสีเผ็ด{s}', 'ao sǐi pèt {s}', 'The spicy one, please.', 'miss',
                       'She bursts out laughing. Colours are not spicy.')],
                   ('Colours',
                    'สี (sǐi) is "colour", and it comes before the colour word: สีขาว white, '
                    'สีฟ้า sky blue, สีดำ (dam) black, สีแดง (dɛɛŋ) red, as in the red trucks, '
                    'and สีทอง (tɔɔŋ) gold.'),
                   who='Stall-holder', thai='เอาสีไหนคะ', paiboon='ao sǐi nǎi ká',
                   english='Which colour would you like?'),
            _scene(3, 'Baan Dam', 'The Black House',
                   'บ้านดำ (bâan dam), the Black House, is the opposite of the White Temple: '
                   'dark teak buildings filled with horns, bones and skins, made by the '
                   'artist Thawan Duchanee. It has been a long morning. You need the toilet.',
                   'Ask a member of staff where it is.',
                   [_c('ห้องน้ำอยู่ที่ไหน{q}', 'hɔ̂ɔŋ-náam yùu tîi-nǎi {q}', 'Where is the toilet?', 'good',
                       'ตรงไป เลี้ยวขวาค่ะ (dtroŋ bpai, líao kwǎa kâ), "Straight on, then right."'),
                    _c('ห้องน้ำ{s}', 'hɔ̂ɔŋ-náam {s}', 'Toilet.', 'ok',
                       'She points the way. It works, though the full question is kinder.'),
                    _c('มีห้องว่างไหม{q}', 'mii hɔ̂ɔŋ wâaŋ mǎi {q}', 'Do you have a free room?', 'miss',
                       'She looks puzzled. That is what you ask at a hotel, not a museum.')],
                   ('ห้องน้ำ: the water room',
                    'ห้องน้ำ (hɔ̂ɔŋ-náam) is literally "water room", and it means both bathroom '
                    'and toilet. ห้อง on its own is any room.'),
                   who='Staff member', thai='สวัสดีค่ะ', paiboon='sà-wàt-dii kâ', english='Hello.'),
            _scene(4, 'Sop Ruak, on the Mekong', 'The Golden Triangle',
                   'An hour north, the Mekong and Ruak rivers meet. This is the Golden '
                   'Triangle, where Thailand, Laos and Myanmar touch. A man by the river '
                   'is selling boat rides.',
                   'Point across the water and ask what country that is.',
                   [_c('นั่นประเทศอะไร{q}', 'nân bprà-têet à-rai {q}', 'What country is that?', 'good',
                       'ลาวครับ (laao kráp), "Laos." Then he points along the bank: พม่า (pá-mâa), Myanmar.'),
                    _c('ที่ไหน{q}', 'tîi-nǎi {q}', 'Where?', 'ok',
                       'He points at where you are pointing. Fair enough. Ask what country.'),
                    _c('เช็คบิล{s}', 'chék-bin {s}', 'The bill, please.', 'miss',
                       'You have not even got in the boat yet.')],
                   ('Three countries',
                    'ประเทศ (bprà-têet) is "country". ไทย (tai) Thailand, ลาว (laao) Laos, '
                    'พม่า (pá-mâa) Myanmar. นั่น (nân) is "that", for something you can see '
                    'over there.'),
                   who='Boatman', thai='นั่งเรือไหมครับ', paiboon='nâŋ rʉa mǎi kráp',
                   english='Want a boat ride?'),
        ],
    },

    # ── Central / Bangkok ────────────────────────────────────────────────
    {
        'key': 'bangkok-river',
        'region': 'Central',
        'title': 'Bangkok by river',
        'place': 'Bangkok',
        'place_thai': 'วัดโพธิ์',
        'place_paiboon': 'wát poo',
        'place_english': 'Wat Pho, home of the Reclining Buddha',
        'blurb': 'Take the river boat to Wat Pho, get a massage at the temple, cross '
                 'to Wat Arun, haggle in Sampheng market and end with dinner in '
                 'Chinatown.',
        'stamp': 'กรุงเทพฯ',
        'photo': {
            'file': 'img/tour/bangkok-river.webp',
            'alt': 'The gold-covered Reclining Buddha at Wat Pho',
            'artist': 'Diego Delso',
            'license': 'CC BY-SA 3.0',
            'license_url': 'https://creativecommons.org/licenses/by-sa/3.0',
            'source': 'https://commons.wikimedia.org/wiki/File:Wat_Pho,_Bangkok,_Tailandia,_2013-08-22,_DD_06.jpg',
        },
        'stops': ['The pier', 'Wat Pho', 'Massage', 'Wat Arun', 'Chinatown'],
        'tutor': 'taxi',
        'tutor_line': 'The AI tutor plays a Bangkok taxi driver. Get yourself back to your hotel.',
        'scenes': [
            _scene(0, 'A pier on the Chao Phraya', 'Which boat?',
                   'The river is the easiest way round old Bangkok. Boats stop at piers '
                   'called tâa. Wat Pho is near Tha Tien pier. A man selling tickets '
                   'looks your way.',
                   'Ask if this boat goes to Tha Tien.',
                   [_c('ไปท่าเตียนไหม{q}', 'bpai tâa-tian mǎi {q}', 'Does it go to Tha Tien?', 'good',
                       'ไปครับ (bpai kráp), "It goes." To say yes, Thai repeats the verb.'),
                    _c('ท่าเตียนอร่อย{s}', 'tâa-tian à-rɔ̀i {s}', 'Tha Tien is delicious.', 'miss',
                       'He tries not to laugh. A pier is not a dish.'),
                    _c('แท็กซี่{s}', 'tɛ́k-sîi {s}', 'Taxi.', 'miss',
                       'He waves at the road behind you. Wrong kind of transport.')],
                   ('Yes and no without "yes"',
                    'Thai often answers by repeating the verb: ไป "goes", ไม่ไป "doesn’t go". '
                    'Turning a sentence into a question is just adding ไหม (mǎi) to the end.'),
                   who='Ticket seller', thai='ไปไหนครับ', paiboon='bpai nǎi kráp',
                   english='Where are you going?'),
            _scene(1, 'Inside Wat Pho', 'The Reclining Buddha',
                   'The Reclining Buddha is 46 metres long and covered in gold leaf. Along '
                   'the wall is a row of small bronze bowls. People drop coins in, one by '
                   'one, for luck. A guard notices your shorts.',
                   'He hands you a cloth to wrap round your legs. Answer him.',
                   [_c('ขอบคุณ{s}', 'kɔ̀ɔp-kun {s}', 'Thank you.', 'good',
                       'He smiles. Many temples lend a wrap or sarong at the door.'),
                    _c('แพง{s}', 'pɛɛŋ {s}', 'Expensive.', 'miss',
                       'He has not asked for any money. It is a loan, not a sale.'),
                    _c('ไม่เอา{s}', 'mâi ao {s}', 'I don’t want it.', 'miss',
                       'Then you cannot go in. Covering your legs is the rule here, not a suggestion.')],
                   ('Dress for temples',
                    'Shoulders and knees covered, shoes off before you go into a hall. '
                    'Carry a light scarf in Bangkok and you are always ready.'),
                   who='Guard', thai='ใส่อันนี้ครับ', paiboon='sài an-níi kráp',
                   english='Put this on.'),
            _scene(2, 'The massage school at Wat Pho', 'A massage at the temple',
                   'Wat Pho is famous for teaching traditional Thai massage. Halfway '
                   'through, the therapist presses a knot in your shoulder.',
                   'It hurts. Ask her to go gently.',
                   [_c('เบาๆ หน่อย{s}', 'bao-bao nɔ̀i {s}', 'A bit more gently, please.', 'good',
                       'ได้ค่ะ (dâi kâ). The pressure eases straight away.'),
                    _c('แรงๆ{s}', 'rɛɛŋ-rɛɛŋ {s}', 'Harder.', 'ok',
                       'She presses harder. It is your shoulder, but you did say it hurt.'),
                    _c('ช่วยด้วย', 'chûai dûai', 'Help!', 'miss',
                       'The whole room goes quiet. A bit much for a sore shoulder.')],
                   ('Doubled words',
                    'Saying a word twice softens it or spreads it out: เบาๆ (bao-bao) is '
                    '"gently", ช้าๆ (cháa-cháa) is "slowly". The ๆ mark means "say it again".'),
                   who='Therapist', thai='เจ็บไหมคะ', paiboon='jèp mǎi ká', english='Does it hurt?'),
            _scene(3, 'Tha Tien cross-river ferry', 'Over to Wat Arun',
                   'A small ferry crosses the river to Wat Arun, the Temple of Dawn, its '
                   'towers covered in pieces of coloured china. On the far bank you want a '
                   'photo with the tower behind you.',
                   'Ask someone to take your photo.',
                   [_c('ช่วยถ่ายรูปให้หน่อยได้ไหม{q}', 'chûai tàai-rûup hâi nɔ̀i dâi mǎi {q}',
                       'Could you take a photo for me?', 'good',
                       'ได้ครับ (dâi kráp). He crouches low to fit the whole tower in.'),
                    _c('ถ่ายรูป{s}', 'tàai-rûup {s}', 'Take photo.', 'ok',
                       'He gets it, but it sounds like an order. ช่วย...หน่อย makes it a favour.'),
                    _c('ห้อง{s}', 'hɔ̂ɔŋ {s}', 'Room.', 'miss',
                       'A room? He looks around for a hotel.')],
                   ('ช่วย…หน่อย: the polite favour',
                    'Put ช่วย (chûai, "help") before a verb and หน่อย (nɔ̀i, "a little") after '
                    'it, and any request becomes a polite favour.')),
            _scene(4, 'Sampheng Lane, Chinatown', 'Sampheng market',
                   'Before dinner you squeeze into สำเพ็ง (sǎm-peŋ), Chinatown’s oldest '
                   'market: a lane barely wide enough for two people, packed with stalls '
                   'selling everything in bulk. Hair clips, toys, fabric, phone cases. '
                   'You like a bag of keyrings.',
                   'Sampheng sells wholesale. Ask for a discount if you buy three.',
                   [_c('ซื้อสามอัน ลดได้ไหม{q}', 'sʉ́ʉ sǎam an, lót dâi mǎi {q}',
                       'If I buy three, can you lower the price?', 'good',
                       'She taps her calculator and shows you a better price. Buying more is '
                       'exactly how Sampheng works.'),
                    _c('ลดได้ไหม{q}', 'lót dâi mǎi {q}', 'Can you lower the price?', 'ok',
                       'She shakes her head for one, then holds up three fingers. Here the '
                       'discount comes from buying more.'),
                    _c('อร่อย{s}', 'à-rɔ̀i {s}', 'Delicious.', 'miss',
                       'She looks at the keyrings, then at you. Please don’t eat them.')],
                   ('Wholesale Thai',
                    'อัน (an) is the counting word for small objects. In wholesale markets '
                    'you will hear โหล (lǒo), "a dozen", and ส่ง (sòŋ), "wholesale price". '
                    'Go in the morning, before the lane gets too crowded to move.'),
                   who='Stall-holder', thai='อันละยี่สิบค่ะ', paiboon='an lá yîi-sìp kâ',
                   english='Twenty baht each.'),
            _scene(4, 'Yaowarat Road, Chinatown', 'Dinner in Chinatown',
                   'At night Yaowarat fills with neon signs and food stalls. You point at '
                   'a pot of noodles and the vendor holds up some fingers.',
                   'You want one bowl. What do you say?',
                   [_c('เอาหนึ่งชาม{s}', 'ao nʉ̀ŋ chaam {s}', 'One bowl, please.', 'good',
                       'She ladles it out. ชาม (chaam) is the counting word for bowls.'),
                    _c('เอาหนึ่ง{s}', 'ao nʉ̀ŋ {s}', 'One, please.', 'ok',
                       'She understands, with you pointing. Next time add ชาม, the word for bowls.'),
                    _c('น้ำ{s}', 'náam {s}', 'Water.', 'miss',
                       'She hands you a bottle of water. Still no noodles.')],
                   ('Counting words',
                    'Thai counts things with a word for the kind of thing: ชาม for bowls, '
                    'จาน (jaan) for plates, แก้ว (gɛ̂ɛo) for glasses. Number first, then the word.'),
                   who='Vendor', thai='กี่ชามคะ', paiboon='gìi chaam ká', english='How many bowls?'),
        ],
    },

    # ── Northeast / Isan ─────────────────────────────────────────────────
    {
        'key': 'phimai',
        'region': 'Northeast',
        'title': 'Stone temples of Phimai',
        'place': 'Nakhon Ratchasima (Korat)',
        'place_thai': 'ปราสาทหินพิมาย',
        'place_paiboon': 'bprà-sàat hǐn pí-maai',
        'place_english': 'Phimai, the stone sanctuary',
        'blurb': 'Cycle round a Khmer temple nearly a thousand years old, then eat '
                 'Isan food the way Isan eats it.',
        'stamp': 'พิมาย',
        'photo': {
            'file': 'img/tour/phimai.webp',
            'alt': 'The sandstone towers of Phimai Historical Park',
            'artist': 'Napast3379',
            'license': 'CC BY-SA 3.0',
            'license_url': 'https://creativecommons.org/licenses/by-sa/3.0',
            'source': 'https://commons.wikimedia.org/wiki/File:Phimai_Historical_Park_03.JPG',
        },
        'stops': ['Bus station', 'Bike hire', 'The sanctuary', 'Som tam', 'Sticky rice'],
        'tutor': 'restaurant',
        'tutor_line': 'The AI tutor plays a waiter. Order a full Isan meal.',
        'scenes': [
            _scene(0, 'Korat bus station', 'Find the bus',
                   'Phimai is a small town about an hour from Korat. The bus station is '
                   'busy and every sign is in Thai.',
                   'Ask where the bus to Phimai leaves from.',
                   [_c('รถไปพิมายอยู่ที่ไหน{q}', 'rót bpai pí-maai yùu tîi-nǎi {q}',
                       'Where is the bus to Phimai?', 'good',
                       'She points. ตรงนั้นค่ะ (dtroŋ nán kâ), "Over there."'),
                    _c('พิมายแพง{s}', 'pí-maai pɛɛŋ {s}', 'Phimai is expensive.', 'miss',
                       'She frowns. You have not even got there yet.'),
                    _c('ที่ไหน', 'tîi-nǎi', 'Where?', 'ok',
                       'Where what? She waits. Add the bus and the place and she can help.')],
                   ('รถ means any vehicle',
                    'รถ (rót) is a car, a bus or a truck. รถไป + place is "the vehicle going '
                    'to…", which is how you ask for any bus.'),
                   who='Woman at the counter', thai='ไปไหนคะ', paiboon='bpai nǎi ká',
                   english='Where are you going?'),
            _scene(1, 'A shop opposite the park', 'Hire a bicycle',
                   'The historical park is flat and the ruins are spread out. A shop '
                   'across the road has a row of old bicycles outside.',
                   'Ask if you can hire one.',
                   [_c('เช่าจักรยานได้ไหม{q}', 'châo jàk-grà-yaan dâi mǎi {q}',
                       'Can I hire a bicycle?', 'good',
                       'ได้ครับ (dâi kráp). He pumps up the tyres for you.'),
                    _c('ขายจักรยานไหม{q}', 'kǎai jàk-grà-yaan mǎi {q}',
                       'Do you sell bicycles?', 'ok',
                       'He blinks. ขาย is "sell". You only want it for the afternoon. '
                       'เช่า (châo) is "hire".'),
                    _c('จักรยานสวย{s}', 'jàk-grà-yaan sǔai {s}', 'Bicycle beautiful.', 'miss',
                       'He agrees it is a nice bike, and waits for the actual question.')],
                   ('ได้ไหม: can I?',
                    'Put ได้ไหม (dâi mǎi) after almost anything to ask if it is allowed or '
                    'possible. The answer is ได้ (dâi, "can") or ไม่ได้ (mâi dâi, "can’t").'),
                   who='Shop owner', thai='สวัสดีครับ', paiboon='sà-wàt-dii kráp',
                   english='Hello.'),
            _scene(2, 'The main sanctuary', 'Older than Angkor Wat',
                   'Phimai was built by the Khmer empire nearly a thousand years ago, and '
                   'its central tower is a little older than Angkor Wat. It is midday and '
                   'very hot. A guard sitting in the shade calls you over.',
                   'He asks if you are hot. Answer him.',
                   [_c('ร้อนมาก{s}', 'rɔ́ɔn mâak {s}', 'Very hot.', 'good',
                       'He laughs and points at the shade. พักก่อน (pák gɔ̀ɔn), "Rest first."'),
                    _c('หนาว{s}', 'nǎao {s}', 'Cold.', 'miss',
                       'He looks at the sweat on your shirt and shakes his head. หนาว is cold.'),
                    _c('เผ็ด{s}', 'pèt {s}', 'Spicy.', 'miss',
                       'Close. In Thai, heat from chilli and heat from the sun are different words.')],
                   ('Hot, spicy, cold',
                    'ร้อน (rɔ́ɔn) is hot weather or hot water. เผ็ด (pèt) is hot food. '
                    'หนาว (nǎao) is cold weather, and เย็น (yen) is cool or cold to touch.'),
                   who='Guard', thai='ร้อนไหมครับ', paiboon='rɔ́ɔn mǎi kráp',
                   english='Are you hot?'),
            _scene(3, 'A som tam stall', 'Som tam',
                   'Isan is home to som tam, green papaya salad pounded in a clay mortar. '
                   'The cook holds up a handful of chillies and waits.',
                   'Ask for it not too spicy.',
                   [_c('ไม่เผ็ดมาก{s}', 'mâi pèt mâak {s}', 'Not too spicy.', 'good',
                       'She drops most of the chillies back. Isan "not too spicy" is still '
                       'fairly spicy.'),
                    _c('เผ็ดมาก{s}', 'pèt mâak {s}', 'Very spicy.', 'ok',
                       'She adds every chilli in her hand and smiles. Brave.'),
                    _c('ไม่เอา{s}', 'mâi ao {s}', 'I don’t want it.', 'miss',
                       'She puts the pestle down. You just cancelled your lunch.')],
                   ('ไม่…มาก: not very',
                    'ไม่เผ็ด is "not spicy". ไม่เผ็ดมาก is "not very spicy". That small '
                    'มาก makes a big difference at an Isan stall.'),
                   who='Cook', thai='เผ็ดไหมคะ', paiboon='pèt mǎi ká', english='Spicy?'),
            _scene(4, 'The same stall', 'Sticky rice',
                   'In Isan, som tam comes with sticky rice in a little woven basket. You '
                   'eat it with your right hand. After the first mouthful the cook asks '
                   'what you think.',
                   'Tell her it is delicious.',
                   [_c('อร่อยมาก{s}', 'à-rɔ̀i mâak {s}', 'Very delicious.', 'good',
                       'She is pleased. Then she teaches you the Isan word: แซ่บ (sɛ̂ɛp).'),
                    _c('แซ่บ{s}', 'sɛ̂ɛp {s}', 'Delicious! (Isan word)', 'good',
                       'Her face lights up. You just used the local word, and everyone at '
                       'the stall heard.'),
                    _c('ถูก{s}', 'tùuk {s}', 'Cheap.', 'ok',
                       'True, but she asked about the taste, not the price.')],
                   ('A word from Isan',
                    'Isan has its own language, close to Lao. แซ่บ (sɛ̂ɛp) is "delicious" '
                    'there, and Thais from every region know it. Use it in the northeast '
                    'and people will smile.'),
                   who='Cook', thai='อร่อยไหมคะ', paiboon='à-rɔ̀i mǎi ká',
                   english='Is it good?'),
        ],
    },

    # ── East ─────────────────────────────────────────────────────────────
    {
        'key': 'koh-chang',
        'region': 'East',
        'title': 'An island weekend on Koh Chang',
        'place': 'Trat',
        'place_thai': 'เกาะช้าง',
        'place_paiboon': 'gɔ̀ cháaŋ',
        'place_english': 'Koh Chang, "Elephant Island"',
        'blurb': 'Catch the car ferry, find a room by the beach, and order seafood '
                 'as the sun goes down.',
        'stamp': 'เกาะช้าง',
        'photo': {
            'file': 'img/tour/koh-chang.webp',
            'alt': 'Klong Prao Beach on Koh Chang, with forested mountains behind',
            'artist': 'Vyacheslav Argenberg',
            'license': 'CC BY 4.0',
            'license_url': 'https://creativecommons.org/licenses/by/4.0',
            'source': 'https://commons.wikimedia.org/wiki/File:Klong_Prao_Beach,_west_coast_of_Ko_Chang_Island,_Thailand.jpg',
        },
        'stops': ['The ferry', 'Island taxi', 'A room', 'The beach', 'Seafood'],
        'tutor': 'directions',
        'tutor_line': 'The AI tutor plays a local on the street. Find your way back to the beach.',
        'scenes': [
            _scene(0, 'The ferry pier near Trat', 'Buy a ticket',
                   'Koh Chang is one of Thailand’s biggest islands. Car ferries leave from '
                   'piers on the mainland near Trat. You walk up to the ticket window.',
                   'Ask for one ticket to Koh Chang.',
                   [_c('ตั๋วไปเกาะช้างหนึ่งใบ{s}', 'dtǔa bpai gɔ̀ cháaŋ nʉ̀ŋ bai {s}',
                       'One ticket to Koh Chang, please.', 'good',
                       'She tears off a ticket. ใบ (bai) is the counting word for tickets.'),
                    _c('ไปเกาะช้าง{s}', 'bpai gɔ̀ cháaŋ {s}', 'To Koh Chang.', 'ok',
                       'She understands. She holds up one finger to check how many.'),
                    _c('ห้องน้ำ{s}', 'hɔ̂ɔŋ-náam {s}', 'Toilet.', 'miss',
                       'She points to the toilets. You might need them, but you still need a ticket.')],
                   ('เกาะ means island',
                    'เกาะ (gɔ̀) is "island", so every Koh you see on a map is an island. '
                    'ช้าง (cháaŋ) is "elephant".'),
                   who='Ticket seller', thai='กี่ใบคะ', paiboon='gìi bai ká',
                   english='How many tickets?'),
            _scene(1, 'The island pier', 'A ride to the beach',
                   'Shared pickup trucks meet the ferry and run along the coast road. '
                   'Your guesthouse is at White Sand Beach, Hat Sai Khao.',
                   'Tell the driver where you are going.',
                   [_c('ไปหาดทรายขาว{s}', 'bpai hàat saai kǎao {s}', 'To White Sand Beach.', 'good',
                       'He nods you onto the back. Hat Sai Khao is the first big beach.'),
                    _c('ไปทะเล{s}', 'bpai tá-lee {s}', 'To the sea.', 'ok',
                       'He spreads his arms. It is an island. The sea is everywhere. Which beach?'),
                    _c('เลี้ยวขวา{s}', 'líao kwǎa {s}', 'Turn right.', 'miss',
                       'There is only one road. Turning right means driving into the sea.')],
                   ('Reading a beach name',
                    'หาด (hàat) is "beach", ทราย (saai) is "sand", ขาว (kǎao) is "white". '
                    'Many place names are plain descriptions like this one.'),
                   who='Driver', thai='ไปไหนครับ', paiboon='bpai nǎi kráp',
                   english='Where are you going?'),
            _scene(2, 'A guesthouse by the beach', 'Find a room',
                   'You have not booked. A guesthouse has a hand-painted sign by the road.',
                   'Ask if they have a room free.',
                   [_c('มีห้องว่างไหม{q}', 'mii hɔ̂ɔŋ wâaŋ mǎi {q}', 'Do you have a free room?', 'good',
                       'มีค่ะ (mii kâ), "We have." She asks: ห้องแอร์หรือห้องพัดลม, "Air-con or fan?"'),
                    _c('ห้องสวย{s}', 'hɔ̂ɔŋ sǔai {s}', 'Room beautiful.', 'miss',
                       'She thanks you, but you still have not asked for one.'),
                    _c('กุญแจ{s}', 'gun-jɛɛ {s}', 'Key.', 'ok',
                       'She laughs. You skipped a step. Ask if there is a room first.')],
                   ('Air-con or fan?',
                    'Small places often have both. ห้องแอร์ (hɔ̂ɔŋ ɛɛ) is an air-conditioned '
                    'room, ห้องพัดลม (hɔ̂ɔŋ pát-lom) a fan room. Fan rooms cost less.'),
                   who='Owner', thai='สวัสดีค่ะ', paiboon='sà-wàt-dii kâ', english='Hello.'),
            _scene(3, 'White Sand Beach', 'On the sand',
                   'The water is warm and clear. A woman is renting out snorkels from a '
                   'table in the shade.',
                   'Ask how much it is to rent one.',
                   [_c('เช่าเท่าไหร่{q}', 'châo tâo-rài {q}', 'How much to rent?', 'good',
                       'She tells you the price for the day. Story money again. Always ask.'),
                    _c('ซื้อเท่าไหร่{q}', 'sʉ́ʉ tâo-rài {q}', 'How much to buy?', 'ok',
                       'She gives you a much bigger number. ซื้อ (sʉ́ʉ) is buy. เช่า (châo) is rent.'),
                    _c('ร้อน{s}', 'rɔ́ɔn {s}', 'Hot.', 'miss',
                       'She agrees, and waits for a question.')],
                   ('Buy, sell, rent',
                    'ซื้อ (sʉ́ʉ) is buy, ขาย (kǎai) is sell, เช่า (châo) is rent or hire. '
                    'You will use all three on any island.')),
            _scene(4, 'A beach restaurant at sunset', 'Seafood',
                   'Tables on the sand, lanterns in the trees, and the day’s catch laid '
                   'out on ice. You would like grilled prawns.',
                   'Order the prawns.',
                   [_c('ขอกุ้งเผา{s}', 'kɔ̌ɔ gûŋ pǎo {s}', 'Grilled prawns, please.', 'good',
                       'He nods and takes them off the ice. ขอ (kɔ̌ɔ) is the polite way to ask for something.'),
                    _c('กุ้ง{s}', 'gûŋ {s}', 'Prawns.', 'ok',
                       'He understands, and asks how you want them cooked. เผา (pǎo) is grilled.'),
                    _c('เช็คบิล{s}', 'chék-bin {s}', 'The bill, please.', 'miss',
                       'You have not ordered yet. A bold way to save money.')],
                   ('ขอ: may I have',
                    'ขอ (kɔ̌ɔ) + the thing is the polite way to ask for anything: '
                    'ขอน้ำ "water, please", ขอเมนู "the menu, please".'),
                   who='Waiter', thai='รับอะไรครับ', paiboon='ráp à-rai kráp',
                   english='What would you like?'),
        ],
    },

    # ── South ────────────────────────────────────────────────────────────
    {
        'key': 'railay',
        'region': 'South',
        'title': 'Krabi: cliffs and jungle pools',
        'place': 'Krabi',
        'place_thai': 'ไร่เลย์',
        'place_paiboon': 'râi-lee',
        'place_english': 'Railay, the beach you can only reach by boat',
        'blurb': 'Ride a longtail boat to Railay, find a pharmacy when the reef bites, '
                 'then head inland to Khlong Thom’s Emerald Pool and hot springs.',
        'stamp': 'กระบี่',
        'photo': {
            'file': 'img/tour/railay.webp',
            'alt': 'A longtail boat pulled up on the sand below Railay’s limestone cliffs',
            'artist': 'Vyacheslav Argenberg',
            'license': 'CC BY 4.0',
            'license_url': 'https://creativecommons.org/licenses/by/4.0',
            'source': 'https://commons.wikimedia.org/wiki/File:Railay,_Krabi,_Boat,_Thailand.jpg',
        },
        'stops': ['Ao Nang', 'Longtail', 'The cliffs', 'Pharmacy', 'Emerald Pool', 'Hot springs'],
        'tutor': 'market',
        'tutor_line': 'The AI tutor plays a stall-holder on Ao Nang’s beach road. Buy a souvenir.',
        'scenes': [
            _scene(0, 'Ao Nang beach', 'Find a boat',
                   'Railay is cut off by limestone cliffs, so the only way in is by boat. '
                   'Longtail boats wait on the sand at Ao Nang.',
                   'Ask the boatman if he goes to Railay.',
                   [_c('ไปไร่เลย์ไหม{q}', 'bpai râi-lee mǎi {q}', 'Do you go to Railay?', 'good',
                       'ไปครับ. He points to the board with the fare. Pay before you board.'),
                    _c('ไร่เลย์ที่ไหน{q}', 'râi-lee tîi-nǎi {q}', 'Where is Railay?', 'ok',
                       'He points round the headland. Right answer, but you wanted a ride.'),
                    _c('ว่ายน้ำ{s}', 'wâai-náam {s}', 'Swim.', 'miss',
                       'He grins. You could swim round, but the boat is quicker.')],
                   ('Longtail boats',
                    'เรือหางยาว (rʉa hǎaŋ-yaao), "long-tail boat", is named after the long '
                    'propeller shaft at the back. Climb in at the front, not over the engine.'),
                   who='Boatman', thai='ไปไหนครับ', paiboon='bpai nǎi kráp',
                   english='Where are you going?'),
            _scene(1, 'On the boat', 'Wet landing',
                   'The boat pulls up in shallow water and the boatman cuts the engine. '
                   'There is no pier. He says something and points at your feet.',
                   'You did not catch it. Ask him to say it again.',
                   [_c('พูดอีกทีได้ไหม{q}', 'pûut ìik tii dâi mǎi {q}', 'Could you say that again?', 'good',
                       'He says it slower: ถอดรองเท้า (tɔ̀ɔt rɔɔŋ-táao), "take off your shoes." Good thing you asked.'),
                    _c('ไม่เข้าใจ{s}', 'mâi kâo-jai {s}', 'I don’t understand.', 'good',
                       'He mimes taking off his shoes. Honest, and it worked.'),
                    _c('โอเค{s}', 'oo-kee {s}', 'OK.', 'ok',
                       'You nod and jump straight in. Your trainers are now full of seawater.')],
                   ('The two phrases that save you',
                    'ไม่เข้าใจ (mâi kâo-jai), "I don’t understand", and พูดอีกทีได้ไหม, '
                    '"say it again?". Thais are patient with learners who ask.'),
                   who='Boatman', thai='ถอดรองเท้าครับ', paiboon='tɔ̀ɔt rɔɔŋ-táao kráp',
                   english='Take off your shoes.'),
            _scene(2, 'Under the cliffs', 'Ouch',
                   'You wade out to look at the cliffs and step on sharp coral. Your foot '
                   'is bleeding. Not badly, but it needs cleaning. A climber sees you limp.',
                   'Tell her your foot hurts.',
                   [_c('เจ็บเท้า{s}', 'jèp táao {s}', 'My foot hurts.', 'good',
                       'She looks and nods. Not a hospital job. She tells you there is a '
                       'pharmacy, ร้านขายยา, on the walking street.'),
                    _c('ช่วยด้วย', 'chûai dûai', 'Help!', 'ok',
                       'She runs over, then sees the cut. Use ช่วยด้วย when it is serious. '
                       'For a cut foot, say what hurts.'),
                    _c('สวยมาก{s}', 'sǔai mâak {s}', 'Very beautiful.', 'miss',
                       'She agrees the cliffs are lovely. Your foot is still bleeding.')],
                   ('เจ็บ + body part',
                    'เจ็บ (jèp) is "hurt". Add the body part: เจ็บเท้า foot, เจ็บหัว head, '
                    'เจ็บท้อง stomach. For anything serious, โรงพยาบาล is a hospital.'),
                   who='A climber', thai='เป็นอะไรไหมคะ', paiboon='bpen à-rai mǎi ká',
                   english='Are you all right?'),
            _scene(3, 'A pharmacy on the walking street', 'The pharmacy',
                   'Thai pharmacists give a lot of everyday advice. You show her your foot.',
                   'Ask for something to clean the cut.',
                   [_c('มียาล้างแผลไหม{q}', 'mii yaa láaŋ plɛ̌ɛ mǎi {q}',
                       'Do you have something to clean a wound?', 'good',
                       'มีค่ะ. She hands you antiseptic and plasters, and shows you how much to use.'),
                    _c('ยา{s}', 'yaa {s}', 'Medicine.', 'ok',
                       'Which one? She points at the foot to check. Name what it is for and she can help faster.'),
                    _c('เผ็ดไหม{q}', 'pèt mǎi {q}', 'Is it spicy?', 'miss',
                       'She laughs. Antiseptic is many things, but not spicy.')],
                   ('Pharmacy words',
                    'ร้านขายยา (ráan kǎai yaa) is a pharmacy, literally "shop that sells '
                    'medicine". ยา (yaa) is medicine, แผล (plɛ̌ɛ) is a cut or wound.'),
                   who='Pharmacist', thai='เป็นอะไรคะ', paiboon='bpen à-rai ká',
                   english='What’s the matter?'),
            _scene(4, 'Khlong Thom, an hour inland', 'The Emerald Pool',
                   'Next morning, foot patched, you take a minivan inland to Khlong Thom '
                   '(คลองท่อม). In the forest there is สระมรกต (sà mɔɔ-rá-gòt), the '
                   'Emerald Pool: spring water so clear and green it looks lit from '
                   'below. A boardwalk leads through the trees. After a while you wonder '
                   'how much further it is.',
                   'Ask a ranger if it is still far.',
                   [_c('อีกไกลไหม{q}', 'ìik glai mǎi {q}', 'Is it much further?', 'good',
                       'ไม่ไกลครับ (mâi glai kráp), "Not far." He points ahead. You can hear '
                       'people splashing.'),
                    _c('อีกใกล้ไหม{q}', 'ìik glâi mǎi {q}', 'Is it much nearer?', 'ok',
                       'He works out what you meant. Near and far differ only by tone, so '
                       'it is an easy slip.'),
                    _c('เลี้ยวขวา{s}', 'líao kwǎa {s}', 'Turn right.', 'miss',
                       'There is only one boardwalk. Turning right means walking into the trees.')],
                   ('Near and far',
                    'ใกล้ (glâi), falling tone, is "near". ไกล (glai), mid tone, is "far". '
                    'อีก (ìik) means "more", so อีกไกลไหม is "is there much further to go?".'),
                   who='Ranger', thai='สวัสดีครับ', paiboon='sà-wàt-dii kráp',
                   english='Hello.'),
            _scene(5, 'Khlong Thom hot springs', 'Hot springs',
                   'Not far away, hot spring water runs down over the rocks into warm '
                   'pools in the forest. You lower yourself in slowly. The woman in the '
                   'next pool smiles at your face.',
                   'Agree with her, and say it feels good.',
                   [_c('ใช่ ร้อนแต่สบาย{s}', 'châi, rɔ́ɔn dtɛ̀ɛ sà-baai {s}',
                       'Yes, hot but lovely.', 'good',
                       'She laughs and nods. สบาย is exactly the word for this.'),
                    _c('ใช่ ร้อนมาก{s}', 'châi, rɔ́ɔn mâak {s}', 'Yes, very hot.', 'good',
                       'She nods. Give it a minute. It gets better.'),
                    _c('หนาว{s}', 'nǎao {s}', 'Cold.', 'miss',
                       'She raises an eyebrow. You are sitting in a hot spring.')],
                   ('สบาย: comfortable, relaxed',
                    'สบาย (sà-baai) is comfortable, easy, relaxed. It is the สบาย in '
                    'สบายดีไหม, "how are you?". ใช่ (châi) means "that’s right", and '
                    'แต่ (dtɛ̀ɛ) means "but".'),
                   who='Woman in the next pool', thai='ร้อนไหมคะ', paiboon='rɔ́ɔn mǎi ká',
                   english='Is it hot?'),
        ],
    },

    # ── West ─────────────────────────────────────────────────────────────
    {
        'key': 'kanchanaburi',
        'region': 'West',
        'title': 'River Kwai and Erawan Falls',
        'place': 'Kanchanaburi',
        'place_thai': 'น้ำตกเอราวัณ',
        'place_paiboon': 'náam-dtòk ee-raa-wan',
        'place_english': 'Erawan Falls, seven tiers of turquoise pools',
        'blurb': 'Walk the bridge over the River Kwai, then climb the seven tiers of '
                 'Erawan Falls and swim with the fish.',
        'stamp': 'กาญจนบุรี',
        'photo': {
            'file': 'img/tour/kanchanaburi.webp',
            'alt': 'A turquoise pool at Erawan Falls, with fish in the clear water',
            'artist': 'Rungsilp Sasitorn',
            'license': 'CC BY-SA 4.0',
            'license_url': 'https://creativecommons.org/licenses/by-sa/4.0',
            'source': 'https://commons.wikimedia.org/wiki/File:Erawan_Waterfall,_tier_1,_Erawan_National_Park,_Kanchanaburi,_Thailand.jpg',
        },
        'stops': ['The bridge', 'The bus', 'Erawan', 'The pools', 'The way back'],
        'tutor': 'directions',
        'tutor_line': 'The AI tutor plays a friendly local. Ask your way to the night market.',
        'scenes': [
            _scene(0, 'The bridge over the River Kwai', 'The bridge',
                   'Prisoners of war and conscripted Asian labourers built this railway in '
                   'the Second World War, and tens of thousands died. It is a quiet place. '
                   'An older Thai man standing by the rail asks where you are from.',
                   'Answer him.',
                   [_c('มาจากอังกฤษ{s}', 'maa jàak aŋ-grìt {s}', 'I’m from England.', 'good',
                       'He nods, and tells you the war cemetery in town is worth a quiet visit.'),
                    _c('มาจาก...{s}', 'maa jàak … {s}', 'I’m from… (your country)', 'good',
                       'มาจาก + your country. He nods and asks if this is your first time here.'),
                    _c('อร่อยมาก{s}', 'à-rɔ̀i mâak {s}', 'Very delicious.', 'miss',
                       'He waits politely. That did not answer his question.')],
                   ('Where are you from?',
                    'มาจากไหน (maa jàak nǎi) and the answer มาจาก + country is one of the '
                    'first conversations you will have anywhere in Thailand. Learn your '
                    'country’s Thai name.'),
                   who='Older man', thai='มาจากไหนครับ', paiboon='maa jàak nǎi kráp',
                   english='Where are you from?'),
            _scene(1, 'Kanchanaburi bus station', 'The bus to Erawan',
                   'Erawan National Park is about an hour and a half away by local bus. '
                   'You want to know when the next one leaves.',
                   'Ask what time the bus leaves.',
                   [_c('รถออกกี่โมง{q}', 'rót ɔ̀ɔk gìi mooŋ {q}', 'What time does the bus leave?', 'good',
                       'สิบโมง (sìp mooŋ), "Ten o’clock." Story time, like story money. Check on the day.'),
                    _c('รถเท่าไหร่{q}', 'rót tâo-rài {q}', 'How much is the bus?', 'ok',
                       'Useful, and he tells you. But you still do not know when it goes.'),
                    _c('รถสวย{s}', 'rót sǔai {s}', 'The bus is beautiful.', 'miss',
                       'He looks at the old orange bus and laughs.')],
                   ('กี่โมง: what time?',
                    'กี่ (gìi) asks "how many", โมง (mooŋ) is the daytime hour. So กี่โมง is '
                    '"what time?". You saw กี่ already in กี่ชาม, "how many bowls?".'),
                   who='Man at the desk', thai='ไปเอราวัณใช่ไหมครับ',
                   paiboon='bpai ee-raa-wan châi mǎi kráp',
                   english='Going to Erawan, right?'),
            _scene(2, 'Park entrance', 'Seven tiers',
                   'The falls climb up the hill in seven tiers, each with its own pool. '
                   'A ranger checks bags at the start of the trail.',
                   'Ask the ranger if you can swim.',
                   [_c('ว่ายน้ำได้ไหม{q}', 'wâai-náam dâi mǎi {q}', 'Can I swim?', 'good',
                       'ได้ครับ. He adds: in most of the pools, but watch the signs.'),
                    _c('ว่ายน้ำ{s}', 'wâai-náam {s}', 'Swim.', 'ok',
                       'He understands. ได้ไหม on the end would have made it a question.'),
                    _c('ขายน้ำไหม{q}', 'kǎai náam mǎi {q}', 'Do you sell water?', 'miss',
                       'He points to the shop. Useful later, but not what you meant.')],
                   ('ว่ายน้ำ: swim',
                    'ว่าย (wâai) is the swimming movement and น้ำ (náam) is water. Thai builds '
                    'lots of words this way, from simple pieces.'),
                   who='Ranger', thai='สวัสดีครับ', paiboon='sà-wàt-dii kráp',
                   english='Hello.'),
            _scene(3, 'The fourth pool', 'Fish at your feet',
                   'The water is a bright turquoise. You step in, and small fish start '
                   'nibbling your toes. A boy on the rock next to you is laughing.',
                   'Tell him it tickles.',
                   [_c('จั๊กจี้{s}', 'ják-gà-jîi {s}', 'It tickles!', 'good',
                       'He laughs even more, and shouts it to his sister.'),
                    _c('เจ็บ{s}', 'jèp {s}', 'It hurts.', 'ok',
                       'He looks worried. They are tiny fish. They don’t really hurt.'),
                    _c('ช่วยด้วย', 'chûai dûai', 'Help!', 'miss',
                       'The ranger looks up. Not for fish.')],
                   ('A fun word',
                    'จั๊กจี้ (ják-gà-jîi) means "ticklish". It is one of those words Thai '
                    'people love hearing a foreigner say.'),
                   who='Boy', thai='ปลาตอดเท้าใช่ไหม', paiboon='bplaa dtɔ̀ɔt táao châi mǎi',
                   english='The fish are nibbling your feet, aren’t they?'),
            _scene(4, 'Back in town', 'The way back',
                   'It is dark when the bus drops you in town. You want the night market, '
                   'but the streets all look the same.',
                   'Ask a passer-by where the night market is.',
                   [_c('ตลาดกลางคืนอยู่ที่ไหน{q}', 'dtà-làat glaaŋ-kʉʉn yùu tîi-nǎi {q}',
                       'Where is the night market?', 'good',
                       'ตรงไป แล้วเลี้ยวซ้าย (dtroŋ bpai, lɛ́ɛo líao sáai), "Straight on, then left."'),
                    _c('ตลาด{s}', 'dtà-làat {s}', 'Market.', 'ok',
                       'She points, but there are two. Add กลางคืน, "night", to get the right one.'),
                    _c('โรงแรม{s}', 'rooŋ-rɛɛm {s}', 'Hotel.', 'miss',
                       'She points you to a hotel. Bed can wait. Dinner first.')],
                   ('Following directions',
                    'ตรงไป (dtroŋ bpai) straight on, เลี้ยวซ้าย left, เลี้ยวขวา right, '
                    'แล้ว (lɛ́ɛo) "then". That is enough to understand most directions.'),
                   who='Passer-by', thai='หาอะไรคะ', paiboon='hǎa à-rai ká',
                   english='Looking for something?'),
        ],
    },
]

TRIPS_BY_KEY = {t['key']: t for t in TRIPS}


def fill_particles(text, gender, paiboon=False):
    """Replace the {s}/{q} markers with the speaker's polite ending."""
    forms = PARTICLES[gender]
    index = 1 if paiboon else 0
    return text.replace('{s}', forms['s'][index]).replace('{q}', forms['q'][index])


def thai_strings():
    """Every Thai line a learner can hear, for the audio build script.

    A learner's own lines are recorded once for each speaker, with the ending
    filled in, so the page can play exactly what the learner chose. Lines with
    a '...' blank are a shape rather than a sentence, so they are skipped.
    """
    found = []
    for trip in TRIPS:
        found.append(trip['place_thai'])
        for scene in trip['scenes']:
            if scene['thai']:
                found.append(scene['thai'])
            for choice in scene['choices']:
                for gender in PARTICLES:
                    found.append(fill_particles(choice['thai'], gender))
    seen, out = set(), []
    for thai in found:
        if '...' not in thai and thai not in seen:
            seen.add(thai)
            out.append(thai)
    return out
