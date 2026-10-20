"""Things to do in Thailand — the Tour Guide page's travel section.

WHY THIS EXISTS
---------------
The trips (tour_trips.py) teach Thai with places as the setting. This section
does the other half of the job: it points people at real things to do, and at
places to book them. Josh asked for it on 2026-10-20 so the Tour Guide page
can promote Thailand as well as teach the language. Off-road expeditions
and quad biking were added the same day at his request, and later that day
he asked for the cards to be grouped as Travel, Food, Family and Outdoors
(CATEGORIES below), with new cards for food, family days out and getting
around.

Each activity still carries a few Thai words you would need there, so the
section teaches too.

AFFILIATE LINKS
---------------
Booking links can earn ThaiBridge a commission. Every partner programme lives
in AFFILIATES below, and that is the ONLY place an affiliate id goes. While an
id is empty the link is a normal link, with no label. Once an id is pasted in,
every link to that partner carries it, and the page labels the link and shows
the "we may earn a commission" note. UK advertising rules (ASA/CAP) require
that label, so don't remove it.

When a programme approves you, check its dashboard's link builder against
`param` below before pasting the id. Skyscanner works differently: it runs
through Impact, so its `id` is the whole tracking link Impact gives you (for
example https://skyscanner.pxf.io/c/1234/5678/9012), and the real page is
added on the end as ?u=<page>.

The temple route is commission-free on purpose. It links only to official
pages, so nobody earns from a visit to a temple.

WHAT IS DELIBERATELY LEFT OUT
-----------------------------
No prices, opening hours or timetables, as on the rest of the page: the
booking sites show those, and keep them current. No spearfishing. Most of
Thailand's coral reefs are inside marine national parks, where taking any
animal is banned.

PHOTOS
------
Same rule as the trips: Wikimedia Commons, CC BY / BY-SA / CC0 only, credited
on the page, shrunk to 1000px WebP in static/img/tour/.

⚠️  DRAFT THAI — the phrases below are first drafts awaiting review by Josh
and teacher Paiboon, like the trips. Their spelling was checked against the
reviewed lessons on 2026-10-20.
"""
from urllib.parse import quote, urlencode, urlsplit, urlunsplit, parse_qsl

# Paste each programme's id here once you are approved. Empty means "not yet".
AFFILIATES = {
    'getyourguide': {'name': 'GetYourGuide', 'id': '', 'param': 'partner_id'},
    'klook':        {'name': 'Klook',        'id': '', 'param': 'aid'},
    '12go':         {'name': '12Go',         'id': '17263196', 'param': 'z'},
    'skyscanner':   {'name': 'Skyscanner',   'id': '', 'param': None},  # Impact tracking link
}


def booking_link(partner, url):
    """The link to show for one partner page, with the affiliate id if there is one."""
    info = AFFILIATES[partner]
    affiliate = bool(info['id'])
    if affiliate and info['param'] is None:
        url = info['id'] + '?u=' + quote(url, safe='')
    elif affiliate:
        parts = urlsplit(url)
        query = parse_qsl(parts.query) + [(info['param'], info['id'])]
        url = urlunsplit(parts._replace(query=urlencode(query)))
    return {'url': url, 'partner': info['name'], 'affiliate': affiliate}


def _gyg(search):
    return 'https://www.getyourguide.com/s/?' + urlencode({'q': search})


def _klook(search):
    return 'https://www.klook.com/search/result/?' + urlencode({'query': search})


def _photo(file, alt, artist, license, source):
    licence_paths = {'CC BY 2.0': 'by/2.0', 'CC BY 3.0': 'by/3.0', 'CC BY 4.0': 'by/4.0', 'CC BY-SA 2.0': 'by-sa/2.0',
                     'CC BY-SA 3.0': 'by-sa/3.0', 'CC BY-SA 4.0': 'by-sa/4.0'}
    return {'file': 'img/tour/' + file, 'alt': alt, 'artist': artist, 'license': license,
            'license_url': 'https://creativecommons.org/licenses/' + licence_paths[license],
            'source': 'https://commons.wikimedia.org/wiki/File:' + source}


# The page shows the activities under these headings, in this order. Each
# activity's 'category' must be one of these keys.
CATEGORIES = [
    ('travel', '✈️', 'Travel'),
    ('food', '🍜', 'Food'),
    ('family', '👨‍👩‍👧', 'Family'),
    ('outdoors', '🌿', 'Outdoors'),
    ('temples', '🛕', 'Temples'),
]

ACTIVITIES = [
    {
        'key': 'flights',
        'category': 'travel',
        'title': 'Getting to Thailand',
        'emoji': '✈️',
        'where': 'Bangkok Suvarnabhumi (BKK) for most long-haul flights, or Phuket and Chiang Mai to land closer to the beach or the mountains.',
        'blurb': 'Compare flights from wherever you are. Once you land, trains, buses and '
                 'ferries go almost everywhere, and you can book those ahead too.',
        'tip': 'Check the entry rules for your passport before you book. They change from time to time.',
        'photo': _photo('do-flights.webp', 'A plane wing over the runway at Suvarnabhumi Airport, Bangkok',
                        'Vyacheslav Argenberg', 'CC BY 4.0',
                        'Suvarnabhumi_Airport,_Airfield,_Aircraft,_Thailand.jpg'),
        'phrases': [('สนามบิน', 'sà-nǎam-bin', 'Airport'),
                    ('ตั๋วเครื่องบิน', 'dtǔa krʉ̂aŋ-bin', 'Plane ticket'),
                    ('หนังสือเดินทาง', 'nǎŋ-sʉ̌ʉ dəən-taaŋ', 'Passport')],
        'links': [('skyscanner', 'Flights to Thailand',
                   'https://www.skyscanner.net/flights-to/th/cheap-flights-to-thailand.html'),
                  ('skyscanner', 'Flights to Bangkok',
                   'https://www.skyscanner.net/flights-to/bkk/cheap-flights-to-bangkok-suvarnabhumi-airport.html'),
                  ('12go', 'Trains, buses and ferries', 'https://12go.asia/en/travel/thailand')],
    },
    {
        'key': 'temples',
        'category': 'temples',
        'title': 'A temple route across Thailand',
        'emoji': '🛕',
        'where': 'Bangkok (Wat Pho, Wat Arun, the Emerald Buddha at Wat Phra Kaew) → Nakhon Pathom '
                 '(Phra Pathom Chedi) → Ayutthaya → Sukhothai → Chiang Mai (Doi Suthep) → Chiang Rai '
                 '(the White Temple) → Phimai → Ubon Ratchathani (Wat Nong Pah Pong, Ajahn Chah’s '
                 'forest monastery) → Nakhon Si Thammarat (Wat Phra Mahathat).',
        'blurb': 'From royal temples in Bangkok to the ruined capitals of Ayutthaya and Sukhothai, '
                 'mountain temples in the north and the quiet forest monasteries of the northeast. '
                 'Take it in pieces or as one long journey.',
        'tip': 'Cover your shoulders and knees, take your shoes off before a hall with Buddha '
               'images, and never point your feet at a Buddha image or a monk.',
        'photo': _photo('do-temples.webp', 'A temple hall with an ornate orange and gold roof at Wat Arun, Bangkok',
                        'Diego Delso', 'CC BY-SA 3.0',
                        'Templo_Wat_Arun,_Bangkok,_Tailandia,_2013-08-22,_DD_30.jpg'),
        'phrases': [('วัด', 'wát', 'Temple'),
                    ('ทำบุญ', 'tam-bun', 'To make merit'),
                    ('ถอดรองเท้า', 'tɔ̀ɔt rɔɔŋ-táao', 'Take off your shoes')],
        # Commission-free on purpose: official pages only. See the note at the top.
        'links': [('info', 'Ayutthaya (UNESCO)', 'https://whc.unesco.org/en/list/576'),
                  ('info', 'Sukhothai (UNESCO)', 'https://whc.unesco.org/en/list/574'),
                  ('info', 'Tourism Authority of Thailand', 'https://www.tourismthailand.org/')],
        'trips': ['doi-suthep', 'chiang-rai', 'phimai'],
        'see_also': ('/theravada', 'Learn about the Buddhism behind the temples'),
    },
    {
        'key': 'climbing',
        'category': 'outdoors',
        'title': 'Rock climbing',
        'emoji': '🧗',
        'where': 'Railay and Tonsai in Krabi, where limestone cliffs rise straight out of the sea. '
                 'Crazy Horse Buttress near Chiang Mai is the north’s climbing spot.',
        'blurb': 'Half-day and full-day courses take complete beginners up their first routes, '
                 'and experienced climbers can hire gear and a guide.',
        'tip': 'Go in the morning, before the rock gets hot, and check how old the bolts are on '
               'sea cliffs. Salt air wears them out.',
        'photo': _photo('do-climbing.webp', 'Climbers on the overhanging limestone roof above Tonsai beach',
                        'Maria Ly', 'CC BY 2.0', 'Climbing_at_Ton_Sai_Roof,_Thailand.jpg'),
        'phrases': [('ปีนผา', 'bpiin pǎa', 'Rock climbing'),
                    ('เชือก', 'chʉ̂ak', 'Rope'),
                    ('กลัวความสูง', 'glua kwaam-sǔuŋ', 'Scared of heights')],
        'links': [('getyourguide', 'Climbing in Railay', _gyg('Railay rock climbing')),
                  ('klook', 'Climbing in Krabi', _klook('Krabi rock climbing'))],
    },
    {
        'key': 'diving',
        'category': 'outdoors',
        'title': 'Scuba diving and snorkelling',
        'emoji': '🤿',
        'where': 'Koh Tao is one of the world’s busiest places to learn to dive. The Similan and '
                 'Surin Islands are the famous liveaboard trips, open from mid-October to mid-May.',
        'blurb': 'Learn to dive from scratch, or swim over coral reefs with turtles and reef '
                 'sharks. Snorkelling trips need no training at all.',
        'tip': 'Spearfishing is banned in Thailand’s marine national parks, where most of the '
               'coral is, so we don’t list it. Look, photograph, and leave the reef as you found it.',
        'photo': _photo('do-diving.webp', 'A wooden dive boat on calm water off Koh Tao',
                        'Eli Duke', 'CC BY-SA 2.0', 'Dive_boat_in_Koh_Tao,_Thailand.jpg'),
        'phrases': [('ดำน้ำ', 'dam-náam', 'Dive, snorkel'),
                    ('ปะการัง', 'bpà-gaa-raŋ', 'Coral'),
                    ('หูเจ็บ', 'hǔu jèp', 'My ears hurt')],
        'links': [('getyourguide', 'Diving on Koh Tao', _gyg('Koh Tao scuba diving')),
                  ('getyourguide', 'Similan Islands trips', _gyg('Similan Islands')),
                  ('klook', 'Snorkelling trips', _klook('Thailand snorkeling'))],
    },
    {
        'key': 'sea-fishing',
        'category': 'outdoors',
        'title': 'Sea fishing',
        'emoji': '🎣',
        'where': 'Day and night trips leave from Phuket, Krabi, Koh Samui and Pattaya. Night squid '
                 'fishing, under bright lamps, is a Thai favourite.',
        'blurb': 'Charter a boat for deep-sea game fish, or join a relaxed longtail trip, '
                 'and often eat what you catch.',
        'tip': 'Ask what is included before you go: rods, bait, food, and whether you can keep the catch.',
        'photo': _photo('do-sea-fishing.webp', 'Longtail fishing boats moored off a Phuket beach',
                        'Radek Kucharski', 'CC BY 2.0', 'Thai_fishing_boats_on_Phuket_Island.jpg'),
        'phrases': [('ตกปลา', 'dtòk-bplaa', 'To fish'),
                    ('เรือ', 'rʉa', 'Boat'),
                    ('เมาเรือ', 'mao-rʉa', 'Seasick')],
        'links': [('getyourguide', 'Fishing trips in Phuket', _gyg('Phuket fishing trip')),
                  ('klook', 'Squid fishing', _klook('squid fishing Thailand'))],
    },
    {
        'key': 'freshwater-fishing',
        'category': 'outdoors',
        'title': 'Freshwater fishing',
        'emoji': '🐟',
        'where': 'Fishing parks near Bangkok, Pattaya, Phuket and Chiang Mai are stocked with '
                 'big fish like the Mekong giant catfish. Rivers and reservoirs up north are wilder.',
        'blurb': 'Fishing parks rent you everything, so you can turn up and fish. Most are '
                 'catch and release.',
        'tip': 'Fishing parks set their own rules on hooks and keeping fish. Ask before you cast.',
        'photo': _photo('do-freshwater-fishing.webp', 'People fishing with nets and lines in the Nan river',
                        'Takeaway', 'CC BY-SA 3.0', 'Thailand_nan_river_fishing.jpg'),
        'phrases': [('บ่อตกปลา', 'bɔ̀ɔ dtòk-bplaa', 'Fishing pond'),
                    ('เหยื่อ', 'yʉ̀a', 'Bait'),
                    ('ปลาบึก', 'bplaa-bʉ̀k', 'Mekong giant catfish')],
        'links': [('getyourguide', 'Fishing parks', _gyg('fishing park Thailand')),
                  ('klook', 'Fishing near Bangkok', _klook('Bangkok fishing'))],
    },
    {
        'key': 'hiking',
        'category': 'outdoors',
        'title': 'Hiking and trekking',
        'emoji': '🥾',
        'where': 'Doi Inthanon, Thailand’s highest mountain, has short nature trails. Chiang Mai '
                 'and Chiang Rai run treks through hill-tribe villages, and Khao Sok has rainforest '
                 'and a huge lake in the south.',
        'blurb': 'From an hour’s walk to a waterfall to several days in the hills, sleeping in '
                 'village homestays.',
        'tip': 'Some national park trails can only be walked with a local guide. Start early and '
               'carry more water than you think.',
        'photo': _photo('do-hiking.webp', 'Wooden steps on the Kew Mae Pan trail, Doi Inthanon, with mountains behind',
                        'Douglas Perkins', 'CC BY 4.0', 'Kew_Mae_Pan_Nature_Trail_Steps.jpg'),
        'phrases': [('เดินป่า', 'dəən-bpàa', 'Trekking'),
                    ('น้ำตก', 'nám dtòk', 'Waterfall'),
                    ('ทางนี้ใช่มั๊ย', 'taaŋ níi châi mái', 'Is it this way?')],
        'links': [('getyourguide', 'Treks from Chiang Mai', _gyg('Chiang Mai trekking')),
                  ('getyourguide', 'Doi Inthanon trips', _gyg('Doi Inthanon')),
                  ('klook', 'Khao Sok', _klook('Khao Sok'))],
    },
    {
        'key': 'wildlife',
        'category': 'family',
        'title': 'Wildlife, zoos and national parks',
        'emoji': '🐒',
        'where': 'Khao Yai, a few hours from Bangkok, has wild elephants, gibbons and hornbills. '
                 'Kaeng Krachan is for birdwatchers. Khao Kheow Open Zoo and Chiang Mai Zoo suit families.',
        'blurb': 'See elephants in the wild, take a night safari with a ranger, or spend a day '
                 'at an open zoo.',
        'tip': 'If you meet wild elephants on a park road, stay in the car, keep your distance '
               'and let them pass. Never feed wild animals.',
        'photo': _photo('do-wildlife.webp', 'A herd of wild Asian elephants grazing in Khao Yai National Park',
                        'Pailoolom', 'CC BY-SA 4.0', 'Asian_elephant_herd_in_Khao_Yai_National_Park.jpg'),
        'phrases': [('ช้าง', 'cháaŋ', 'Elephant'),
                    ('ลิง', 'liŋ', 'Monkey'),
                    ('อุทยานแห่งชาติ', 'ùt-tá-yaan hɛ̀ŋ châat', 'National park')],
        'links': [('getyourguide', 'Khao Yai tours', _gyg('Khao Yai National Park')),
                  ('klook', 'Zoos and safaris', _klook('Thailand zoo')),
                  ('info', 'Thai national parks (official)', 'https://portal.dnp.go.th/')],
    },
    {
        'key': 'road-trip',
        'category': 'travel',
        'title': 'Road trips',
        'emoji': '🛣️',
        'where': 'The Mae Hong Son Loop from Chiang Mai, through Pai, is famous for its curves. '
                 'The coast road south of Bangkok and the quiet roads of Isan are easier going.',
        'blurb': 'Hire a car or a motorbike and stop wherever you like: viewpoints, hot springs, '
                 'night markets. Or let a bus do the driving.',
        'tip': 'You need an International Driving Permit as well as your licence, and a motorbike '
               'licence to ride one. Check your travel insurance covers it, and always wear a helmet.',
        'photo': _photo('do-road-trip.webp', 'A minibus parked beside a winding mountain road on Route 1095',
                        'Christophe95', 'CC BY-SA 4.0', 'Thailand_Route_1095.jpg'),
        'phrases': [('ปั๊มน้ำมัน', 'bpám náam-man', 'Petrol station'),
                    ('เติมเต็มถัง', 'dtəəm dtem tǎŋ', 'Fill it up'),
                    ('ไกลมั๊ย', 'glai mái', 'Is it far?')],
        'links': [('12go', 'Bus: Chiang Mai to Pai', 'https://12go.asia/en/travel/chiang-mai/pai'),
                  ('12go', 'Bangkok to Chiang Mai', 'https://12go.asia/en/travel/bangkok/chiang-mai'),
                  ('klook', 'Car hire', _klook('Thailand car rental'))],
    },
    {
        'key': 'off-road',
        'category': 'outdoors',
        'title': 'Off-road expeditions',
        'emoji': '🚙',
        'where': 'The mountains around Chiang Mai, Mae Hong Son and Chiang Rai have the best dirt '
                 'tracks, up to hill-tribe villages and viewpoints. Khao Kho and the Isan hills are '
                 'quieter.',
        'blurb': 'Ride in a 4x4 convoy on jungle tracks and river crossings, or join a guided '
                 'dirt-bike tour if you already ride.',
        'tip': 'Go with a guide who knows the tracks: they turn to deep mud in the rainy season, '
               'roughly May to October.',
        'photo': _photo('do-off-road.webp', 'A convoy of 4x4 vehicles lined up on a dirt track near Chiang Mai',
                        'Maxim Cruiser', 'CC BY 3.0', 'Chiang_mai_trip_2011_-_panoramio.jpg'),
        'phrases': [('ทางลูกรัง', 'taaŋ lûuk-raŋ', 'Dirt road'),
                    ('รถโฟร์วีล', 'rót foo-wiil', '4x4'),
                    ('โคลน', 'kloon', 'Mud')],
        'links': [('getyourguide', '4x4 tours from Chiang Mai', _gyg('Chiang Mai jeep tour')),
                  ('getyourguide', 'Dirt-bike tours', _gyg('Chiang Mai dirt bike tour')),
                  ('klook', 'Off-road tours', _klook('Thailand off road tour'))],
    },
    {
        'key': 'quad-biking',
        'category': 'outdoors',
        'title': 'Quad biking',
        'emoji': '🏍️',
        'where': 'ATV parks and jungle trails around Chiang Mai, Phuket, Krabi, Koh Samui and Pattaya. '
                 'Most trips include a short practice lap first.',
        'blurb': 'Drive your own quad bike along jungle and farm tracks, often with a waterfall '
                 'or viewpoint stop. No experience needed.',
        'tip': 'Wear the helmet, check that the brakes work before you set off, and make sure your '
               'travel insurance covers quad bikes. Many policies don’t.',
        'photo': _photo('do-quad-biking.webp', 'A line of quad bikes on a jungle dirt road in Mae Taeng, Chiang Mai',
                        'Maxim Cruiser', 'CC BY 3.0', 'Follow_THE_PEACK_ATV_adventure_-_panoramio.jpg'),
        'phrases': [('หมวกกันน็อค', 'mùak gan-nɔ́k', 'Helmet'),
                    ('เบรก', 'brèek', 'Brake'),
                    ('ช้าลงหน่อย', 'cháa loŋ nɔ̀i', 'Slow down a bit')],
        'links': [('getyourguide', 'Quad biking in Phuket', _gyg('Phuket ATV')),
                  ('getyourguide', 'Quad biking in Chiang Mai', _gyg('Chiang Mai ATV')),
                  ('klook', 'ATV tours', _klook('Thailand ATV'))],
    },
    {
        'key': 'trains-ferries',
        'category': 'travel',
        'title': 'Trains, buses and island ferries',
        'emoji': '⛴️',
        'where': 'Overnight sleeper trains run from Bangkok to Chiang Mai and down to the south. '
                 'Ferries link the mainland with Koh Samui, Koh Phangan, Koh Tao, Koh Chang and the '
                 'Andaman islands.',
        'blurb': 'Thailand is easy to cross without flying. A sleeper train is an adventure in '
                 'itself, and a bus-and-boat ticket gets you to most islands in one booking.',
        'tip': 'Book sleeper berths a few days ahead, especially at weekends and Thai holidays. '
               'Lower berths are a little wider.',
        'photo': _photo('do-trains-ferries.webp', 'A white passenger ferry moored at Haad Rin pier on Koh Phangan',
                        'Fabio Achilli', 'CC BY 2.0', 'Koh_Phangan,_Haadrin_Queen_Ferry_(6218499944).jpg'),
        'phrases': [('รถไฟ', 'rót-fai', 'Train'),
                    ('ท่าเรือ', 'tâa-rʉa', 'Pier'),
                    ('รถไฟออกกี่โมง', 'rót-fai ɔ̀ɔk gìi mooŋ', 'What time does the train leave?')],
        'links': [('12go', 'Sleeper train to Chiang Mai', 'https://12go.asia/en/travel/bangkok/chiang-mai'),
                  ('12go', 'Bangkok to Koh Samui', 'https://12go.asia/en/travel/bangkok/koh-samui'),
                  ('12go', 'Bangkok to Koh Tao', 'https://12go.asia/en/travel/bangkok/koh-tao')],
    },
    {
        'key': 'street-food',
        'category': 'food',
        'title': 'Street food and night markets',
        'emoji': '🍢',
        'where': 'Yaowarat (Chinatown) in Bangkok, the Sunday Walking Street in Chiang Mai, and '
                 'the night market in almost every Thai town.',
        'blurb': 'Some of the best food in Thailand costs a few coins from a cart. Wander on your '
                 'own, or join a guided food tour to try dishes you wouldn’t know to order.',
        'tip': 'Pick the busy stalls: a queue of locals means fresh food. Say “mâi pèt” if you '
               'can’t take chilli.',
        'photo': _photo('do-street-food.webp', 'Sausages and skewers grilling at a street food stall in Chiang Mai',
                        'David McKelvey', 'CC BY 2.0', 'Street_Food_Stall,_Chiang_Mai,_Thailand_(7113967189).jpg'),
        'phrases': [('อาหารข้างทาง', 'aa-hǎan kâaŋ taaŋ', 'Street food'),
                    ('ไม่เผ็ด', 'mâi pèt', 'Not spicy'),
                    ('อร่อยมาก', 'à-rɔ̀i mâak', 'Delicious')],
        'links': [('getyourguide', 'Bangkok food tours', _gyg('Bangkok street food tour')),
                  ('getyourguide', 'Chiang Mai food tours', _gyg('Chiang Mai food tour')),
                  ('klook', 'Food tours', _klook('Thailand food tour'))],
    },
    {
        'key': 'cooking-class',
        'category': 'food',
        'title': 'Thai cooking classes',
        'emoji': '🧑‍🍳',
        'where': 'Chiang Mai is the cooking-class capital, often with a market visit and a farm '
                 'kitchen. Bangkok, Sukhothai, Krabi and the islands have good ones too.',
        'blurb': 'Shop for ingredients at a local market, then cook four or five dishes, such as '
                 'pad thai, green curry and tom yum, and eat everything you make.',
        'tip': 'Tell the school about allergies or a vegetarian diet when you book. Most will '
               'change the recipes for you.',
        'photo': _photo('do-cooking-class.webp', 'Two plates of freshly cooked pad thai at a cooking school in Sukhothai',
                        'Elmschrat', 'CC BY-SA 4.0', 'Pad_Thai_in_Thai_Cooking_School_in_Sukhothai.jpg'),
        'phrases': [('ทำอาหาร', 'tam aa-hǎan', 'To cook'),
                    ('ผัดไทย', 'pàt-tai', 'Pad thai'),
                    ('ใส่พริกนิดเดียว', 'sài prík nít diao', 'Just a little chilli')],
        'links': [('getyourguide', 'Cooking classes in Chiang Mai', _gyg('Chiang Mai cooking class')),
                  ('getyourguide', 'Cooking classes in Bangkok', _gyg('Bangkok cooking class')),
                  ('klook', 'Cooking classes', _klook('Thai cooking class'))],
    },
    {
        'key': 'elephant-sanctuary',
        'category': 'family',
        'title': 'Ethical elephant sanctuaries',
        'emoji': '🐘',
        'where': 'Most are in the hills around Chiang Mai, with others near Phuket, Kanchanaburi '
                 'and Koh Samui. Many look after elephants rescued from logging and tourist camps.',
        'blurb': 'Walk with elephants through the forest, help prepare their food and watch them '
                 'being elephants. A day most children never forget.',
        'tip': 'Choose a sanctuary with no riding, no shows and no bathing with the elephants. If a '
               'place lets you ride or hold animals for photos, give it a miss.',
        'photo': _photo('do-elephant-sanctuary.webp', 'Visitors walking with elephants along a forest track near Chiang Mai',
                        'Nina R', 'CC BY 2.0', 'Elephant_Nature_Park_(49418413298).jpg'),
        'phrases': [('ปางช้าง', 'bpaaŋ cháaŋ', 'Elephant camp'),
                    ('ให้อาหาร', 'hâi aa-hǎan', 'To feed'),
                    ('ห้ามขี่', 'hâam kìi', 'No riding')],
        'links': [('getyourguide', 'Sanctuaries near Chiang Mai', _gyg('Chiang Mai ethical elephant sanctuary')),
                  ('getyourguide', 'Sanctuaries near Phuket', _gyg('Phuket ethical elephant sanctuary')),
                  ('klook', 'Elephant sanctuaries', _klook('elephant sanctuary Thailand'))],
    },
    {
        'key': 'aquarium',
        'category': 'family',
        'title': 'Aquariums and water parks',
        'emoji': '🐠',
        'where': 'SEA LIFE Bangkok Ocean World sits under a shopping centre in the middle of '
                 'Bangkok. Phuket and Pattaya have big aquariums and water parks.',
        'blurb': 'A cool, easy day out with children on a hot afternoon: sharks, rays and turtles '
                 'behind the glass, or slides and wave pools.',
        'tip': 'Water parks get busy at weekends and in school holidays. Go on a weekday and '
               'bring a rash vest: the sun is strong even on cloudy days.',
        'photo': _photo('do-aquarium.webp', 'A queen angelfish swimming over rocks in a tank at SEA LIFE Bangkok Ocean World',
                        'กสิณธร ราชโอรส', 'CC BY-SA 4.0', 'SEA_LIFE_Bangkok_Ocean_World_in_2018_(11).jpg'),
        'phrases': [('พิพิธภัณฑ์สัตว์น้ำ', 'pí-pít-tá-pan sàt-náam', 'Aquarium'),
                    ('ปลาฉลาม', 'bplaa chà-lǎam', 'Shark'),
                    ('เต่าทะเล', 'dtào tá-lee', 'Sea turtle')],
        'links': [('getyourguide', 'SEA LIFE Bangkok', _gyg('SEA LIFE Bangkok Ocean World')),
                  ('klook', 'Aquariums', _klook('Thailand aquarium')),
                  ('klook', 'Water parks', _klook('Thailand water park'))],
    },
]

ACTIVITIES_BY_CATEGORY = [
    {'key': key, 'emoji': emoji, 'title': title,
     'activities': [a for a in ACTIVITIES if a['category'] == key]}
    for key, emoji, title in CATEGORIES
]

ACTIVITIES_BY_KEY = {a['key']: a for a in ACTIVITIES}


def links_for(activity):
    """An activity's links, ready for the page. 'info' links are plain, never affiliate."""
    out = []
    for partner, label, url in activity['links']:
        if partner == 'info':
            out.append({'label': label, 'url': url, 'partner': '', 'affiliate': False})
        else:
            out.append({'label': label, **booking_link(partner, url)})
    return out


def any_affiliate():
    """True once any programme has an id, which switches on the page's commission note."""
    return any(info['id'] for info in AFFILIATES.values())


def thai_strings():
    """Every Thai phrase in this section, for the page's audio map."""
    return [thai for a in ACTIVITIES for thai, _, _ in a['phrases']]
