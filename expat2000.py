"""Expat2000 — set yourself up for life (and work) in Thailand.

WHY THIS EXISTS
---------------
Business Thai already says it is "for expats and digital nomads", but it only
teaches words. Someone arriving to live and work here has a different first
problem: which visa, how to get a bank account, a SIM, a condo, a doctor. They
search for that, not for vocabulary. This page answers those questions FIRST and
then gives the Thai you need to sort each one out face to face — so the people
who find it through "Thailand DTV visa" discover the course on the way.

It is free and needs no alphabet, like Survival Thai: it is a front door, and a
front door with a paywall on it is a wall.

HOW IT IS SHAPED
----------------
Eight "missions", each with three parts:
    know  — the facts, in plain English
    do    — a checklist the visitor ticks off (saved in their own browser)
    say   — the Thai phrases for that situation, with audio where recorded

⚠️  FACTS GO STALE. Visa and tax rules here change often — the visa-free stay
went from 60 days to 30 on 15 September 2026, and most guides online still say
60. Every fact below was checked on LAST_CHECKED. When you re-check, update that
date, and keep pointing people at the official sources in OFFICIAL_LINKS rather
than presenting this page as the authority.

⚠️  DRAFT THAI — every Thai string below is a first draft awaiting review by
the native-speaker teacher, same as survival.py. Nothing here is final.
"""

from survival import POLITE_PARTICLE

LAST_CHECKED = '28 October 2026'

# The authorities. The page links these at the top of every mission they
# belong to, so a visitor always has the real source one tap away.
OFFICIAL_LINKS = {
    'evisa': {'label': 'Thai e-Visa (official applications)', 'url': 'https://www.thaievisa.go.th/'},
    'immigration': {'label': 'Thai Immigration Bureau', 'url': 'https://www.immigration.go.th/'},
    'tdac': {'label': 'TDAC — Digital Arrival Card (free)', 'url': 'https://tdac.immigration.go.th/'},
    'revenue': {'label': 'Thai Revenue Department', 'url': 'https://www.rd.go.th/english/'},
}


def _p(thai, paiboon, english, note='', particle=False):
    """One phrase. Same shape as survival._p so the template partial is shared."""
    return {
        'thai': thai,
        'paiboon': paiboon,
        'english': english,
        'note': note,
        'particle': particle,
    }


# Ordered the way a move actually happens: you cannot open a bank account
# without the right visa, cannot use most apps without a Thai number, and so on.
MISSIONS = [
    {
        'key': 'visas',
        'title': 'Visas & staying legal',
        'emoji': '🛂',
        'tagline': 'Get in, stay in, and never overstay.',
        'links': ['evisa', 'immigration', 'tdac'],
        'know': [
            'Visa-free entry is now 30 days, for tourism only. From 15 September '
            '2026 Thailand cut the visa-exempt stay from 60 days to 30 for around '
            '60 countries, including the UK, EU, US and Australia. You can ask to '
            'extend once by 30 days at an immigration office (1,900 baht), but it is '
            'up to the officer.',
            'The Destination Thailand Visa (DTV) is the digital-nomad visa: valid '
            'for 5 years with multiple entries, 180 days per entry, and one 180-day '
            'extension per entry. You need about 500,000 baht in savings (most '
            'embassies want it held for 3 months). The fee is around 10,000 baht, '
            'charged in local currency (London charges £300).',
            'New since 31 August 2026: you apply for the DTV in a country where you '
            'are a citizen or permanent resident, and you need a police clearance '
            'certificate.',
            'The DTV lets you work remotely for employers and clients OUTSIDE '
            'Thailand. Working for a Thai company or Thai clients needs a proper '
            'work visa and work permit.',
            'Every foreign visitor fills in the TDAC (digital arrival card) online, '
            'free, in the 72 hours before landing. Use only the official site — '
            'look-alike sites charge for it.',
            'Staying more than 90 days in a row? Report your address to immigration '
            'every 90 days (online or in person). Your landlord or hotel must also '
            'file a "TM30" telling immigration where you live — check they have.',
        ],
        'do': [
            {'id': 'passport', 'text': 'Passport valid for at least 6 more months'},
            {'id': 'visa-route', 'text': 'Pick your route: 30-day visa-free, DTV or a work visa'},
            {'id': 'tdac', 'text': 'TDAC filled in on the official site (72 hours before landing)'},
            {'id': 'tm30', 'text': 'Landlord has filed my TM30'},
            {'id': '90day', 'text': 'Reminder set for my first 90-day report'},
        ],
        'say': [
            _p('วีซ่า', 'wii-sâa', 'Visa'),
            _p('ต่อวีซ่า', 'dtɔ̀ɔ wii-sâa', 'To extend a visa'),
            _p('หนังสือเดินทาง', 'nǎŋ-sʉ̌ʉ dəən-taaŋ', 'Passport'),
            _p('สำนักงานตรวจคนเข้าเมือง', 'sǎm-nák-ŋaan dtrùat kon kâo mʉaŋ',
               'Immigration office',
               'Most people just say ตม. (dtɔɔ-mɔɔ) for short.'),
            _p('รายงานตัวเก้าสิบวัน', 'raai-ŋaan dtua gâo-sìp wan', '90-day report'),
            _p('ต้องใช้เอกสารอะไรบ้าง', 'dtɔ̂ŋ chái èek-gà-sǎan à-rai bâaŋ',
               'Which documents do I need?', particle=True),
        ],
    },
    {
        'key': 'money',
        'title': 'Money, banking & tax',
        'emoji': '💸',
        'tagline': 'Pay like a local and keep the taxman happy.',
        'links': ['revenue'],
        'know': [
            'Thailand pays by QR code. PromptPay QR codes are on street stalls, '
            'taxis and rent invoices, and you need a Thai bank account to use them.',
            'Whether you can open a bank account depends on the bank AND the '
            'branch. Most want your passport, a long-stay visa (DTV, work, study or '
            'retirement) and proof of address. Some also ask for a letter from '
            'immigration or your embassy. If one branch says no, try another.',
            'Thai ATMs charge foreign cards around 220–250 baht per withdrawal, on '
            'top of whatever your bank charges. Wise and similar cards usually '
            'cost less than airport exchange counters and bank transfers.',
            'Tax: if you spend 180 days or more in Thailand in a calendar year, you '
            'are a Thai tax resident. Since 1 January 2024, foreign income you bring '
            'into Thailand while resident can be taxed at 5–35%. A proposed '
            'exemption is still only a draft as of October 2026. This is not tax '
            'advice: check with the Revenue Department or a tax adviser, and with '
            'your home country, which may have a tax treaty with Thailand.',
        ],
        'do': [
            {'id': 'travel-card', 'text': 'Low-fee travel card (e.g. Wise) ready'},
            {'id': 'cash', 'text': 'Some baht in cash for the first few days'},
            {'id': 'bank', 'text': 'Thai bank account opened'},
            {'id': 'promptpay', 'text': 'Banking app installed and PromptPay working'},
            {'id': 'day-count', 'text': 'Counting my days in Thailand this year (the 180-day tax line)'},
        ],
        'say': [
            _p('ธนาคาร', 'tá-naa-kaan', 'Bank'),
            _p('อยากเปิดบัญชี', 'yàak bpə̀ət ban-chii', 'I\'d like to open an account',
               particle=True),
            _p('โอนเงิน', 'oon ŋən', 'To transfer money'),
            _p('เงินสด', 'ŋən sòt', 'Cash'),
            _p('สแกนจ่ายได้มั๊ย', 'sà-gɛɛn jàai dâi mái', 'Can I scan to pay?',
               'Ask this anywhere you see a QR code.', particle=True),
            _p('ค่าธรรมเนียมเท่าไหร่', 'kâa tam-niam tâo-rài', 'How much is the fee?',
               particle=True),
        ],
    },
    {
        'key': 'phone',
        'title': 'Phone & internet',
        'emoji': '📶',
        'tagline': 'A Thai number unlocks almost everything else.',
        'links': [],
        'know': [
            'You need a Thai number for banking apps, Grab and food delivery, so '
            'get it sorted early.',
            'SIM cards must be registered to your passport. Airport kiosks and the '
            'networks\' own shops do this on the spot. The big networks are AIS and '
            'True (which merged with dtac).',
            'If your phone takes an eSIM, you can buy one before you fly and land '
            'already connected.',
            'LINE is Thailand\'s main messaging app. Landlords, shops and even some '
            'government offices use it.',
            'Home fibre internet is cheap and fast in the cities. Ask whether your '
            'condo already includes it.',
        ],
        'do': [
            {'id': 'sim', 'text': 'Thai SIM or eSIM, registered to my passport'},
            {'id': 'line', 'text': 'LINE installed'},
            {'id': 'wifi', 'text': 'Home internet sorted'},
        ],
        'say': [
            _p('ซิมการ์ด', 'sim-gáat', 'SIM card'),
            _p('เติมเงิน', 'dtəəm ŋən', 'To top up (credit)'),
            _p('แพ็กเกจเน็ต', 'pɛ́k-gèt nét', 'Internet package'),
            _p('รหัสไวไฟคืออะไร', 'rá-hàt wai-fai kʉʉ à-rai',
               'What\'s the wifi password?', particle=True),
            _p('เน็ตช้ามาก', 'nét cháa mâak', 'The internet is really slow'),
        ],
    },
    {
        'key': 'home',
        'title': 'Finding a home',
        'emoji': '🏠',
        'tagline': 'From a first-month crash pad to your own condo.',
        'links': [],
        'know': [
            'Most newcomers book a serviced apartment or short let for the first '
            'month, then look at condos in person. Never pay a deposit on a place '
            'you have only seen in photos.',
            'Monthly leases are common. 6–12 month leases cost less per month.',
            'Expect a deposit of 1–2 months\' rent, plus the first month in advance. '
            'Photograph every room when you move in so you can get the deposit back.',
            'Ask whether you pay the government rate for electricity and water or a '
            'higher "building rate". It can make a big difference to the bill.',
            'Ask your landlord to file your TM30 (see Visas). It is their job, but '
            'you are the one who has trouble at immigration if it is missing.',
        ],
        'do': [
            {'id': 'first-month', 'text': 'First month booked somewhere short-term'},
            {'id': 'viewings', 'text': 'Viewed condos in person'},
            {'id': 'contract', 'text': 'Contract read, deposit agreed, rooms photographed'},
        ],
        'say': [
            _p('คอนโด', 'kɔn-doo', 'Condo'),
            _p('มีห้องว่างมั๊ย', 'mii hɔ̂ŋ wâaŋ mái', 'Do you have a room free?',
               particle=True),
            _p('ค่าเช่าเดือนละเท่าไหร่', 'kâa châo dʉan lá tâo-rài',
               'How much is the rent per month?', particle=True),
            _p('ค่ามัดจำ', 'kâa mát-jam', 'Deposit'),
            _p('สัญญาเช่า', 'sǎn-yaa châo', 'Rental contract'),
            _p('ค่าน้ำค่าไฟ', 'kâa náam kâa fai', 'Water and electricity bills'),
        ],
    },
    {
        'key': 'transport',
        'title': 'Getting around',
        'emoji': '🛵',
        'tagline': 'Apps, Skytrain and the two-wheeled truth.',
        'links': [],
        'know': [
            'Grab and Bolt work like Uber, for cars, motorbike taxis and food '
            'delivery. They show the price before you book, so there is no haggling.',
            'Bangkok has the BTS Skytrain and the MRT underground. They are fast, '
            'cheap and air-conditioned.',
            'To drive or ride legally, carry an International Driving Permit with '
            'your home licence. If you are staying long term, get a Thai licence. '
            'Riding without the right licence can void your insurance, and helmets '
            'are the law.',
            'Rental shops sometimes ask to keep your passport. Do not hand it over. '
            'Offer a copy and a cash deposit instead.',
        ],
        'do': [
            {'id': 'apps', 'text': 'Grab and Bolt installed'},
            {'id': 'idp', 'text': 'International Driving Permit (if I\'ll drive or ride)'},
        ],
        'say': [
            _p('ไปที่นี่ได้มั๊ย', 'bpai tîi-nîi dâi mái', 'Can you take me here?',
               'Point at the map on your phone as you say it.', particle=True),
            _p('ตรงไป', 'dtroŋ bpai', 'Go straight on'),
            _p('จอดตรงนี้', 'jɔ̀ɔt dtroŋ-níi', 'Stop here', particle=True),
            _p('ใบขับขี่', 'bai kàp-kìi', 'Driving licence'),
            _p('หมวกกันน็อก', 'mùak gan-nɔ́k', 'Helmet'),
        ],
    },
    {
        'key': 'health',
        'title': 'Health & safety',
        'emoji': '🏥',
        'tagline': 'Sorted before you need it.',
        'links': [],
        'know': [
            'Private hospitals in the big cities are excellent and used to foreign '
            'patients, but bills add up fast without insurance.',
            'Get health insurance that covers you in Thailand for as long as you '
            'stay. Ordinary travel insurance often stops covering you after a set '
            'number of days.',
            'There are pharmacies on almost every street, and the pharmacists are '
            'happy to help with minor problems.',
            'Emergency numbers: 1669 ambulance · 191 police · 1155 tourist police '
            '(English spoken) · 199 fire.',
        ],
        'do': [
            {'id': 'insurance', 'text': 'Health insurance that covers long stays in Thailand'},
            {'id': 'numbers', 'text': 'Emergency numbers saved in my phone'},
            {'id': 'hospital', 'text': 'Found my nearest private hospital'},
            {'id': 'meds', 'text': 'Prescriptions packed, with a doctor\'s letter'},
        ],
        'say': [
            _p('โรงพยาบาล', 'rooŋ-pá-yaa-baan', 'Hospital'),
            _p('ร้านขายยา', 'ráan kǎai yaa', 'Pharmacy'),
            _p('ไม่สบาย', 'mâi sà-baai', 'I feel unwell', particle=True),
            _p('ปวดหัว', 'bpùat hǔa', 'I have a headache'),
            _p('แพ้ยา', 'pɛ́ɛ yaa', 'Allergic to medicine',
               'Show a note naming the medicine too.'),
            _p('ประกันสุขภาพ', 'bprà-gan sùk-kà-pâap', 'Health insurance'),
        ],
    },
    {
        'key': 'work',
        'title': 'Work & community',
        'emoji': '💻',
        'tagline': 'Find your desk and your people.',
        'links': [],
        'know': [
            'Bangkok, Chiang Mai and the islands are the big nomad hubs. Coworking '
            'spaces almost always sell day passes, so try a few before committing.',
            'Working from cafés is normal. Buy something every couple of hours and '
            'leave the big tables free at busy times.',
            'Meetups, coworking events and local Facebook groups are the quickest '
            'way to meet people. Learning a little Thai is the quickest way to meet '
            'Thai people.',
            'Remember the visa rule: remote work for clients abroad is fine on a '
            'DTV, but Thai clients need a work permit.',
        ],
        'do': [
            {'id': 'cowork', 'text': 'Tried a coworking day pass'},
            {'id': 'community', 'text': 'Joined a local meetup or group'},
            {'id': 'thai-10', 'text': 'Learned my first 10 Thai phrases'},
        ],
        'say': [
            _p('ทำงานออนไลน์', 'tam-ŋaan ɔɔn-lai', 'I work online'),
            _p('ขอนั่งทำงานที่นี่ได้มั๊ย', 'kɔ̌ɔ nâŋ tam-ŋaan tîi-nîi dâi mái',
               'May I sit and work here?', particle=True),
            _p('มีปลั๊กมั๊ย', 'mii bplák mái', 'Is there a plug socket?',
               particle=True),
            _p('ยินดีที่ได้รู้จัก', 'yin-dii tîi dâi rúu-jàk', 'Nice to meet you',
               particle=True),
            _p('คุณมาจากไหน', 'kun maa jàak nǎi', 'Where are you from?'),
        ],
    },
    {
        'key': 'fit-in',
        'title': 'Fitting in',
        'emoji': '🙏',
        'tagline': 'The unwritten rules that make Thailand feel like home.',
        'links': [],
        'know': [
            'Respect for the monarchy is taken very seriously, and it is also the '
            'law. Stand for the royal anthem in cinemas.',
            'The head is the highest part of the body and the feet the lowest. '
            'Don\'t touch anyone\'s head, and don\'t point your feet at people or at '
            'Buddha images.',
            'Take your shoes off when you go into a home, and into many shops and '
            'offices too. If you see shoes by the door, follow suit.',
            'Keeping calm wins. Raising your voice makes everyone lose face, '
            'including you.',
            'Dress modestly at temples: cover your shoulders and knees.',
        ],
        'do': [
            {'id': 'wai', 'text': 'Learned when (and when not) to wai'},
            {'id': 'temple', 'text': 'Read the temple etiquette guide'},
        ],
        'say': [
            _p('ไม่เป็นไร', 'mâi bpen rai', 'It\'s nothing / No problem',
               'The phrase you\'ll hear most, and a whole attitude.'),
            _p('ใจเย็นๆ', 'jai yen yen', 'Keep calm / Take it easy',
               'Literally "cool heart".'),
            _p('เกรงใจ', 'greeŋ-jai', 'Not wanting to impose on someone',
               'There\'s no English word for it, and you\'ll see it everywhere.'),
        ],
    },
]

MISSIONS_BY_KEY = {m['key']: m for m in MISSIONS}


def all_phrases():
    """Every phrase across every mission, in page order."""
    return [phrase for mission in MISSIONS for phrase in mission['say']]


def all_tasks():
    """Every checklist item, keyed '<mission>:<task>' so ids stay unique."""
    return ['{}:{}'.format(m['key'], t['id']) for m in MISSIONS for t in m['do']]


def thai_strings():
    """Every pronounceable Thai string, for the audio build script.

    Same filtering as survival.thai_strings(): templates and either-or forms
    would be read aloud as nonsense, so they are dropped.
    """
    found = [phrase['thai'] for phrase in all_phrases()]
    found.extend(form['thai'] for form in POLITE_PARTICLE.values())
    return [thai for thai in found if '...' not in thai and '/' not in thai]
