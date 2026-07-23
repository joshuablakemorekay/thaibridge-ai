"""The 44 Thai consonants — the single source of truth for the Alphabet page.

Everything about a letter lives in one record here: the character, the name
Thai children learn it by, its meaning, its consonant class, the sound it makes,
and the filename of its recording. The page, the quiz and the audio build script
all read from this one list, so they cannot drift apart.

Order is the traditional alphabetical order (ก ข ฃ ค …), which is the order the
letters are taught and the order they appear in a Thai dictionary.

Two notes on the data:

  * ฃ (kor khuat) and ฅ (kor khon) are obsolete — no longer used in modern
    written Thai — but they are still taught as part of the 44, so they stay.
  * `sound` is the Paiboon romanisation of the letter as an INITIAL consonant.
    Several letters share a sound (ท ธ ฑ ฒ ถ ฐ are all "t"); that is a real
    feature of Thai, not a mistake in the table.

`slug` is plain ASCII on purpose. Thai characters survive fine on disk but turn
into percent-encoded soup in a URL, and have caused Windows-to-Linux deployment
problems before.
"""

# Consonant classes decide a syllable's tone, which is why every letter carries
# one. The labels are used verbatim in the page headings.
CLASS_MIDDLE = 'middle'
CLASS_HIGH = 'high'
CLASS_LOW = 'low'

CLASS_LABELS = {
    CLASS_MIDDLE: 'Middle class (อักษรกลาง)',
    CLASS_HIGH: 'High class (อักษรสูง)',
    CLASS_LOW: 'Low class (อักษรต่ำ)',
}

# Where the recordings live, relative to the Flask static folder. Posix-style
# because it ends up in a URL, not on disk.
AUDIO_DIR = 'audio/th'

# The voice the recordings were made with. Kept beside the data so the build
# script and any future re-recording agree.
AUDIO_VOICE = 'th-TH-PremwadeeNeural'


def _c(char, name_thai, name, meaning, sound, cls, slug, obsolete=False):
    return {
        'char': char,           # the letter itself
        'name_thai': name_thai, # e.g. 'กอ ไก่' — what the recording says
        'name': name,           # e.g. 'gɔɔ gài' — Paiboon romanisation
        'meaning': meaning,     # e.g. 'chicken'
        'sound': sound,         # initial-consonant sound, Paiboon
        'cls': cls,
        'obsolete': obsolete,   # ฃ and ฅ only — still taught, no longer written
        'audio': '{}/{}.mp3'.format(AUDIO_DIR, slug),
    }


CONSONANTS = [
    _c('ก', 'กอ ไก่',    'gɔɔ gài',      'chicken',     'g',  CLASS_MIDDLE, 'kor-kai'),
    _c('ข', 'ขอ ไข่',    'kɔ̌ɔ kài',      'egg',         'k',  CLASS_HIGH,   'khor-khai'),
    _c('ฃ', 'ขอ ขวด',   'kɔ̌ɔ kùat',     'bottle',      'k',  CLASS_HIGH,   'khor-khuat', obsolete=True),
    _c('ค', 'คอ ควาย',  'kɔɔ kwaai',    'buffalo',     'k',  CLASS_LOW,    'khor-khwai'),
    _c('ฅ', 'คอ คน',    'kɔɔ kon',      'person',      'k',  CLASS_LOW,    'khor-khon', obsolete=True),
    _c('ฆ', 'ฆอ ระฆัง',  'kɔɔ rá-kang',  'bell',        'k',  CLASS_LOW,    'khor-rakhang'),
    _c('ง', 'งอ งู',     'ngɔɔ nguu',    'snake',       'ng', CLASS_LOW,    'ngor-ngu'),
    _c('จ', 'จอ จาน',   'jɔɔ jaan',     'plate',       'j',  CLASS_MIDDLE, 'chor-chan'),
    _c('ฉ', 'ฉอ ฉิ่ง',    'chɔ̌ɔ chìng',   'cymbals',     'ch', CLASS_HIGH,   'chor-ching'),
    _c('ช', 'ชอ ช้าง',   'chɔɔ cháang',  'elephant',    'ch', CLASS_LOW,    'chor-chang'),
    _c('ซ', 'ซอ โซ่',    'sɔɔ sôo',      'chain',       's',  CLASS_LOW,    'sor-so'),
    _c('ฌ', 'ฌอ เฌอ',  'chɔɔ chəə',    'tree',        'ch', CLASS_LOW,    'chor-choe'),
    _c('ญ', 'ญอ หญิง',  'yɔɔ yǐng',     'woman',       'y',  CLASS_LOW,    'yor-ying'),
    _c('ฎ', 'ฎอ ชฎา',   'dɔɔ chá-daa',  'headdress',   'd',  CLASS_MIDDLE, 'dor-chada'),
    _c('ฏ', 'ฏอ ปฏัก',   'dtɔɔ bpà-dtàk','goad',        'dt', CLASS_MIDDLE, 'tor-patak'),
    _c('ฐ', 'ฐอ ฐาน',   'tɔ̌ɔ tǎan',     'base',        't',  CLASS_HIGH,   'thor-than'),
    _c('ฑ', 'ฑอ มณโฑ', 'tɔɔ mon-too',  'Montho',      't',  CLASS_LOW,    'thor-montho'),
    _c('ฒ', 'ฒอ ผู้เฒ่า',  'tɔɔ pûu-tâo',  'elder',       't',  CLASS_LOW,    'thor-phuthao'),
    _c('ณ', 'ณอ เณร',   'nɔɔ neen',     'novice monk', 'n',  CLASS_LOW,    'nor-nen'),
    _c('ด', 'ดอ เด็ก',   'dɔɔ dèk',      'child',       'd',  CLASS_MIDDLE, 'dor-dek'),
    _c('ต', 'ตอ เต่า',   'dtɔɔ dtào',    'turtle',      'dt', CLASS_MIDDLE, 'tor-tao'),
    _c('ถ', 'ถอ ถุง',    'tɔ̌ɔ tǔng',     'bag',         't',  CLASS_HIGH,   'thor-thung'),
    _c('ท', 'ทอ ทหาร',  'tɔɔ tá-hǎan',  'soldier',     't',  CLASS_LOW,    'thor-thahan'),
    _c('ธ', 'ธอ ธง',     'tɔɔ tong',     'flag',        't',  CLASS_LOW,    'thor-thong'),
    _c('น', 'นอ หนู',    'nɔɔ nǔu',      'mouse',       'n',  CLASS_LOW,    'nor-nu'),
    _c('บ', 'บอ ใบไม้',  'bɔɔ bai-máai', 'leaf',        'b',  CLASS_MIDDLE, 'bor-baimai'),
    _c('ป', 'ปอ ปลา',   'bpɔɔ bplaa',   'fish',        'bp', CLASS_MIDDLE, 'por-pla'),
    _c('ผ', 'ผอ ผึ้ง',    'pɔ̌ɔ pʉ̂ng',     'bee',         'p',  CLASS_HIGH,   'phor-phueng'),
    _c('ฝ', 'ฝอ ฝา',     'fɔ̌ɔ fǎa',      'lid',         'f',  CLASS_HIGH,   'for-fa'),
    _c('พ', 'พอ พาน',   'pɔɔ paan',     'tray',        'p',  CLASS_LOW,    'phor-phan'),
    _c('ฟ', 'ฟอ ฟัน',    'fɔɔ fan',      'tooth',       'f',  CLASS_LOW,    'for-fan'),
    _c('ภ', 'ภอ สำเภา',  'pɔɔ sǎm-pao',  'sailboat',    'p',  CLASS_LOW,    'phor-samphao'),
    _c('ม', 'มอ ม้า',    'mɔɔ máa',      'horse',       'm',  CLASS_LOW,    'mor-ma'),
    _c('ย', 'ยอ ยักษ์',   'yɔɔ yák',      'giant',       'y',  CLASS_LOW,    'yor-yak'),
    _c('ร', 'รอ เรือ',    'rɔɔ rʉa',      'boat',        'r',  CLASS_LOW,    'ror-ruea'),
    _c('ล', 'ลอ ลิง',    'lɔɔ ling',     'monkey',      'l',  CLASS_LOW,    'lor-ling'),
    _c('ว', 'วอ แหวน',  'wɔɔ wɛ̌ɛn',     'ring',        'w',  CLASS_LOW,    'wor-waen'),
    _c('ศ', 'ศอ ศาลา',  'sɔ̌ɔ sǎa-laa',  'pavilion',    's',  CLASS_HIGH,   'sor-sala'),
    _c('ษ', 'ษอ ฤๅษี',   'sɔ̌ɔ rʉ̌-sǐi',    'hermit',      's',  CLASS_HIGH,   'sor-ruesi'),
    _c('ส', 'สอ เสือ',   'sɔ̌ɔ sʉ̌a',      'tiger',       's',  CLASS_HIGH,   'sor-suea'),
    _c('ห', 'หอ หีบ',    'hɔ̌ɔ hìip',     'chest',       'h',  CLASS_HIGH,   'hor-hip'),
    _c('ฬ', 'ฬอ จุฬา',   'lɔɔ jù-laa',   'kite',        'l',  CLASS_LOW,    'lor-chula'),
    _c('อ', 'ออ อ่าง',   'ɔɔ àang',      'basin',       '-',  CLASS_MIDDLE, 'or-ang'),
    _c('ฮ', 'ฮอ นกฮูก',  'hɔɔ nók-hûuk', 'owl',         'h',  CLASS_LOW,    'hor-nokhuk'),
]


def by_class(cls):
    """Every consonant of one class, in alphabetical order."""
    return [c for c in CONSONANTS if c['cls'] == cls]


# A guard against a typo silently changing the alphabet. The three class counts
# are fixed facts of the language: 9 middle, 11 high, 24 low.
assert len(CONSONANTS) == 44, 'expected 44 consonants, got %d' % len(CONSONANTS)
assert len(by_class(CLASS_MIDDLE)) == 9
assert len(by_class(CLASS_HIGH)) == 11
assert len(by_class(CLASS_LOW)) == 24
assert len({c['char'] for c in CONSONANTS}) == 44, 'duplicate letter in the table'
assert len({c['audio'] for c in CONSONANTS}) == 44, 'duplicate audio filename'
