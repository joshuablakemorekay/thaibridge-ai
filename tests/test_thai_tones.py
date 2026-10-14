"""The tone written in each romanisation must be the tone the Thai spelling gives."""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
sys.path.insert(0, ROOT)

from check_thai_tones import check, spelled_tone  # noqa: E402


@pytest.mark.parametrize('thai, tone', [
    # the five-tone set the app teaches with
    ('คา', 'mid'), ('ข่า', 'low'), ('ค่า', 'falling'), ('ค้า', 'high'), ('ขา', 'rising'),
    # each class on live and dead syllables
    ('นก', 'high'), ('มาก', 'falling'), ('จาก', 'low'), ('สุข', 'low'),
    ('สาม', 'rising'), ('กิน', 'mid'), ('ครับ', 'high'),
    # leading ห and อ, clusters, special vowels
    ('หมา', 'rising'), ('อยู่', 'low'), ('ขวา', 'rising'), ('กลาง', 'mid'),
    ('ไป', 'mid'), ('ทำ', 'mid'), ('เกาะ', 'low'), ('ตรัส', 'low'),
])
def test_the_calculator_reads_the_spelling(thai, tone):
    assert spelled_tone(thai) == tone


def test_every_one_syllable_word_in_the_app_has_the_right_tone():
    """ตรัส was romanised dtrát (high) where the spelling gives dtràt (low)."""
    os.environ.setdefault('DATABASE_URL', '')
    import paiboon_lookup
    entries = [(e.thai, e.paiboon, e.source) for e in paiboon_lookup.get_index()]
    faults = check(entries)
    assert not faults, '\n'.join(f'{t} {r}: written {w}, spelling gives {s} ({src})'
                                 for t, r, w, s, src in faults)
