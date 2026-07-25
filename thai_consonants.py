"""The 44 Thai consonants — the single source of truth for the Alphabet page.

Everything about a letter lives in one record here: the character, the name
Thai children learn it by, its meaning, its consonant class, the sound it makes,
and the filename of its recording. The page, the quiz and the audio build script
all read from this one list, so they cannot drift apart.

Order is the traditional alphabetical order (ก ข ฃ ค …), which is the order the
letters are taught and the order they appear in a Thai dictionary.

Four notes on the data:

  * ฃ (kor khuat) and ฅ (kor khon) are obsolete — no longer used in modern
    written Thai — but they are still taught as part of the 44, so they stay.
  * `sound` is the Paiboon romanisation of the letter as an INITIAL consonant.
    Several letters share a sound (ท ธ ฑ ฒ ถ ฐ are all "t"); that is a real
    feature of Thai, not a mistake in the table.
  * `speak` is a pronunciation respelling for the text-to-speech voice, and is
    set on only the handful of letters where the voice misreads the correct
    spelling. `name_thai` is always what the learner SEES; `speak` is only what
    the voice HEARS. They differ on purpose — do not "tidy" one to match the
    other. Each one carries a comment saying what the voice got wrong.

  * `emoji` is the letter's MEANING as a single glyph — ก is taught as "gɔɔ gài,
    chicken", so ก carries 🐔. Twelve meanings have no exact emoji (a cattle
    goad, a pedestal, a pot lid, the Ramakien character Montho…). Those carry
    the closest available glyph and are marked `emoji_approx=True`, which keeps
    them out of the picture round of the quiz — guessing a letter from an
    emoji that only sort-of means "lid" would be an unfair question.

`slug` is plain ASCII on purpose. Thai characters survive fine on disk but turn
into percent-encoded soup in a URL, and have caused Windows-to-Linux deployment
problems before. It doubles as the picture filename.
"""

import os

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

# Where the optional picture per letter lives, relative to the Flask static
# folder. Posix-style because it ends up in a URL, not on disk. A picture is
# named after the letter's slug (kor-kai.webp, kor-kai.png, …) and NOTHING has
# to be registered anywhere: drop the file in and the page finds it. See
# picture_static_path() below.
PICTURE_DIR = 'img/consonants'

# Tried in this order, so a small modern .webp wins over a heavy .png of the
# same letter if both happen to be present.
PICTURE_EXTENSIONS = ('.webp', '.png', '.jpg', '.jpeg', '.svg')


def _c(char, name_thai, name, meaning, sound, cls, slug, emoji,
       obsolete=False, speak=None, emoji_approx=False):
    return {
        'char': char,           # the letter itself
        'name_thai': name_thai, # e.g. 'กอ ไก่' — the correct spelling, shown on screen
        'name': name,           # e.g. 'gɔɔ gài' — Paiboon romanisation
        'meaning': meaning,     # e.g. 'chicken'
        'sound': sound,         # initial-consonant sound, Paiboon
        'cls': cls,
        'obsolete': obsolete,   # ฃ and ฅ only — still taught, no longer written
        'audio': '{}/{}.mp3'.format(AUDIO_DIR, slug),
        'speak': speak or name_thai,  # what the voice is fed — see note below
        'slug': slug,           # also the picture filename — see PICTURE_DIR
        'emoji': emoji,         # e.g. '🐔' — the letter's meaning as one glyph
        'emoji_approx': emoji_approx,  # emoji is only close, not exact
    }


CONSONANTS = [
    _c('ก', 'กอ ไก่',    'gɔɔ gài',      'chicken',     'g',  CLASS_MIDDLE, 'kor-kai',     '🐔'),
    _c('ข', 'ขอ ไข่',    'kɔ̌ɔ kài',      'egg',         'k',  CLASS_HIGH,   'khor-khai',   '🥚'),
    # No plain-bottle emoji exists; ขวด is any bottle, not a champagne one.
    _c('ฃ', 'ขอ ขวด',   'kɔ̌ɔ kùat',     'bottle',      'k',  CLASS_HIGH,   'khor-khuat',  '🍾', obsolete=True, emoji_approx=True),
    _c('ค', 'คอ ควาย',  'kɔɔ kwaai',    'buffalo',     'k',  CLASS_LOW,    'khor-khwai',  '🐃'),
    _c('ฅ', 'คอ คน',    'kɔɔ kon',      'person',      'k',  CLASS_LOW,    'khor-khon',   '🧑', obsolete=True),
    _c('ฆ', 'ฆอ ระฆัง',  'kɔɔ rá-kang',  'bell',        'k',  CLASS_LOW,    'khor-rakhang','🔔'),
    _c('ง', 'งอ งู',     'ngɔɔ nguu',    'snake',       'ng', CLASS_LOW,    'ngor-ngu',    '🐍'),
    _c('จ', 'จอ จาน',   'jɔɔ jaan',     'plate',       'j',  CLASS_MIDDLE, 'chor-chan',   '🍽️'),
    # ฉิ่ง are small hand cymbals; Unicode has no cymbals, so a drum stands in.
    _c('ฉ', 'ฉอ ฉิ่ง',    'chɔ̌ɔ chìng',   'cymbals',     'ch', CLASS_HIGH,   'chor-ching',  '🥁', emoji_approx=True),
    _c('ช', 'ชอ ช้าง',   'chɔɔ cháang',  'elephant',    'ch', CLASS_LOW,    'chor-chang',  '🐘'),
    _c('ซ', 'ซอ โซ่',    'sɔɔ sôo',      'chain',       's',  CLASS_LOW,    'sor-so',      '⛓️'),
    _c('ฌ', 'ฌอ เฌอ',  'chɔɔ chəə',    'tree',        'ch', CLASS_LOW,    'chor-choe',   '🌳'),
    _c('ญ', 'ญอ หญิง',  'yɔɔ yǐng',     'woman',       'y',  CLASS_LOW,    'yor-ying',    '👩'),
    # A ชฎา is the tall ceremonial headdress — a crown reads it well enough.
    _c('ฎ', 'ฎอ ชฎา',   'dɔɔ chá-daa',  'headdress',   'd',  CLASS_MIDDLE, 'dor-chada',   '👑'),
    # A ปฏัก is a cattle goad; a trident is the nearest pointed-stick glyph.
    _c('ฏ', 'ฏอ ปฏัก',   'dtɔɔ bpà-dtàk','goad',        'dt', CLASS_MIDDLE, 'tor-patak',   '🔱', emoji_approx=True),
    # ฐาน is a pedestal or base; the classical-building glyph is the closest.
    _c('ฐ', 'ฐอ ฐาน',   'tɔ̌ɔ tǎan',     'base',        't',  CLASS_HIGH,   'thor-than',   '🏛️', emoji_approx=True),
    # Montho is a queen in the Ramakien — a proper name, so no true emoji.
    _c('ฑ', 'ฑอ มณโฑ', 'tɔɔ mon-too',  'Montho',      't',  CLASS_LOW,    'thor-montho', '👸', emoji_approx=True),
    _c('ฒ', 'ฒอ ผู้เฒ่า',  'tɔɔ pûu-tâo',  'elder',       't',  CLASS_LOW,    'thor-phuthao','👴'),
    # Voice dropped the n of เณร ("nɔɔ een"); plain spelling restores it.
    # 🧘 reads as "meditating person" rather than specifically a novice monk.
    _c('ณ', 'ณอ เณร',   'nɔɔ neen',     'novice monk', 'n',  CLASS_LOW,    'nor-nen',     '🧘',
       speak='นอ เนน', emoji_approx=True),
    _c('ด', 'ดอ เด็ก',   'dɔɔ dèk',      'child',       'd',  CLASS_MIDDLE, 'dor-dek',     '🧒'),
    _c('ต', 'ตอ เต่า',   'dtɔɔ dtào',    'turtle',      'dt', CLASS_MIDDLE, 'tor-tao',     '🐢'),
    _c('ถ', 'ถอ ถุง',    'tɔ̌ɔ tǔng',     'bag',         't',  CLASS_HIGH,   'thor-thung',  '👝'),
    _c('ท', 'ทอ ทหาร',  'tɔɔ tá-hǎan',  'soldier',     't',  CLASS_LOW,    'thor-thahan', '🪖'),
    _c('ธ', 'ธอ ธง',     'tɔɔ tong',     'flag',        't',  CLASS_LOW,    'thor-thong',  '🚩'),
    _c('น', 'นอ หนู',    'nɔɔ nǔu',      'mouse',       'n',  CLASS_LOW,    'nor-nu',      '🐭'),
    _c('บ', 'บอ ใบไม้',  'bɔɔ bai-máai', 'leaf',        'b',  CLASS_MIDDLE, 'bor-baimai',  '🍃'),
    _c('ป', 'ปอ ปลา',   'bpɔɔ bplaa',   'fish',        'bp', CLASS_MIDDLE, 'por-pla',     '🐟'),
    # ผอ is not a real word, so the voice read it as two letters, ผ + อ
    # ("pɔ̌ɔ ɔɔ pʉ̂ng"). พอ IS a word, so it comes out as one syllable. The
    # trade-off, chosen deliberately by Josh after listening: พอ is mid tone,
    # not the rising tone of ผอ. Slightly flat beats a whole spare syllable.
    _c('ผ', 'ผอ ผึ้ง',    'pɔ̌ɔ pʉ̂ng',     'bee',         'p',  CLASS_HIGH,   'phor-phueng', '🐝',
       speak='พอ ผึ้ง'),
    # ฝา is a pot lid. No lid emoji exists, so the pot itself stands in.
    _c('ฝ', 'ฝอ ฝา',     'fɔ̌ɔ fǎa',      'lid',         'f',  CLASS_HIGH,   'for-fa',      '🍲', emoji_approx=True),
    # A พาน is a footed ceremonial offering tray — trophy-shaped, roughly.
    _c('พ', 'พอ พาน',   'pɔɔ paan',     'tray',        'p',  CLASS_LOW,    'phor-phan',   '🏆', emoji_approx=True),
    _c('ฟ', 'ฟอ ฟัน',    'fɔɔ fan',      'tooth',       'f',  CLASS_LOW,    'for-fan',     '🦷'),
    _c('ภ', 'ภอ สำเภา',  'pɔɔ sǎm-pao',  'sailboat',    'p',  CLASS_LOW,    'phor-samphao','⛵'),
    _c('ม', 'มอ ม้า',    'mɔɔ máa',      'horse',       'm',  CLASS_LOW,    'mor-ma',      '🐴'),
    # Voice sounded out the silent ษ์ of ยักษ์ ("yɔɔ yák yai"); ยัก drops it.
    _c('ย', 'ยอ ยักษ์',   'yɔɔ yák',      'giant',       'y',  CLASS_LOW,    'yor-yak',     '👹',
       speak='ยอ ยัก'),
    _c('ร', 'รอ เรือ',    'rɔɔ rʉa',      'boat',        'r',  CLASS_LOW,    'ror-ruea',    '🛶'),
    _c('ล', 'ลอ ลิง',    'lɔɔ ling',     'monkey',      'l',  CLASS_LOW,    'lor-ling',    '🐒'),
    _c('ว', 'วอ แหวน',  'wɔɔ wɛ̌ɛn',     'ring',        'w',  CLASS_LOW,    'wor-waen',    '💍'),
    # A ศาลา is an open-sided pavilion; the temple glyph is the nearest thing.
    _c('ศ', 'ศอ ศาลา',  'sɔ̌ɔ sǎa-laa',  'pavilion',    's',  CLASS_HIGH,   'sor-sala',    '🛕', emoji_approx=True),
    # A ฤๅษี is a forest hermit-sage; 🧙 reads as wizard, which is close.
    _c('ษ', 'ษอ ฤๅษี',   'sɔ̌ɔ rʉ̌-sǐi',    'hermit',      's',  CLASS_HIGH,   'sor-ruesi',   '🧙', emoji_approx=True),
    _c('ส', 'สอ เสือ',   'sɔ̌ɔ sʉ̌a',      'tiger',       's',  CLASS_HIGH,   'sor-suea',    '🐅'),
    # หีบ is a lidded storage chest; the toolbox is the closest box glyph.
    _c('ห', 'หอ หีบ',    'hɔ̌ɔ hìip',     'chest',       'h',  CLASS_HIGH,   'hor-hip',     '🧰', emoji_approx=True),
    _c('ฬ', 'ฬอ จุฬา',   'lɔɔ jù-laa',   'kite',        'l',  CLASS_LOW,    'lor-chula',   '🪁'),
    # อ่าง is a washing basin; the bucket is the nearest vessel.
    _c('อ', 'ออ อ่าง',   'ɔɔ àang',      'basin',       '-',  CLASS_MIDDLE, 'or-ang',      '🪣', emoji_approx=True),
    _c('ฮ', 'ฮอ นกฮูก',  'hɔɔ nók-hûuk', 'owl',         'h',  CLASS_LOW,    'hor-nokhuk',  '🦉'),
]


def by_class(cls):
    """Every consonant of one class, in alphabetical order."""
    return [c for c in CONSONANTS if c['cls'] == cls]


def picture_static_path(static_root, slug):
    """Static-relative path of this letter's picture, or None if there isn't one.

    Deliberately a look-on-disk rather than a list kept in this file: the whole
    point is that adding a picture is copying a file in, not editing code. Name
    it after the slug (`img/consonants/kor-kai.webp`) and it appears on the
    flashcard; until then that letter falls back to its emoji.

    Mirrors thai_audio.audio_exists(), which does the same trick for the phrase
    recordings, so both halves of the site behave the same way.
    """
    for ext in PICTURE_EXTENSIONS:
        relative = '{}/{}{}'.format(PICTURE_DIR, slug, ext)
        if os.path.isfile(os.path.join(static_root, PICTURE_DIR, slug + ext)):
            return relative
    return None


def with_pictures(static_root):
    """The 44 consonants, each with a `picture` key: a path, or None.

    Returns shallow copies so the module-level CONSONANTS list stays the plain
    data every other page reads — only the Alphabet page needs pictures, and it
    should not be able to mutate the source of truth to get them.
    """
    letters = []
    for c in CONSONANTS:
        letter = dict(c)
        letter['picture'] = picture_static_path(static_root, c['slug'])
        letters.append(letter)
    return letters


# A guard against a typo silently changing the alphabet. The three class counts
# are fixed facts of the language: 9 middle, 11 high, 24 low.
assert len(CONSONANTS) == 44, 'expected 44 consonants, got %d' % len(CONSONANTS)
assert len(by_class(CLASS_MIDDLE)) == 9
assert len(by_class(CLASS_HIGH)) == 11
assert len(by_class(CLASS_LOW)) == 24
assert len({c['char'] for c in CONSONANTS}) == 44, 'duplicate letter in the table'
assert len({c['audio'] for c in CONSONANTS}) == 44, 'duplicate audio filename'
assert len({c['slug'] for c in CONSONANTS}) == 44, 'duplicate slug (= picture filename)'

# Every letter must carry a picture-glyph, or a tile in the chart would render
# blank. A missing emoji is a typo, not a design choice.
assert all(c['emoji'] for c in CONSONANTS), 'a consonant is missing its emoji'

# The picture round of the quiz draws only on letters whose emoji is exact, so
# there have to be enough of them to fill a third of a 44-question quiz.
assert len([c for c in CONSONANTS if not c['emoji_approx']]) >= 15, \
    'too few exact emoji left to build the picture round'
