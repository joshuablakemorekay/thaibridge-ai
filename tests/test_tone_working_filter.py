"""Tone working is cut from the start of a reply.

The model is told to work tones out silently, and still sometimes opens with
the working ("ถาม: ถ high class, live syllable ..., so rising tone"). Two
real Translator replies did so on 2026-10-28; both are pinned here. The cut
only ever takes a block at the very start, keeps the working when the student
asked how a tone works, and never empties a reply. No test reaches the API.
"""
import os
import sys
from types import SimpleNamespace as NS

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

import ai_agent  # noqa: E402

TEMPLE = """Working out the tones:
- ติด: ต middle class, dead syllable (ending ด) with a short vowel, so low tone: dtìt
- ต่อ: ต middle class with mai ek, so low tone: dtɔ̀ɔ
- สอบ: ส high class, dead syllable (ending บ) with a long vowel, so low tone: sɔ̀ɔp
- ถาม: ถ high class, live syllable with no tone mark, so rising tone: tǎam

A sign for an information desk

**ติดต่อสอบถาม (dtìt-dtɔ̀ɔ sɔ̀ɔp-tǎam) = Information / Inquiries**"""

SOMTAM = """Working out the tones:

-   ส้ม: high-class ส with mai tho gives the falling tone, so sôm.
-   ตำ: middle-class ต, live syllable, no tone mark, gives mid tone, so dtam.

A street food stall with a red banner.

1.  ส้มตำ (sôm-dtam) = papaya salad"""

NO_HEADING = """ยัง: low class ย, short vowel, live ending, so mid tone

ยัง (yaŋ) = yet, still"""


@pytest.mark.parametrize('reply,starts', [
    (TEMPLE, 'A sign for an information desk'),
    (SOMTAM, 'A street food stall'),
    (NO_HEADING, 'ยัง (yaŋ) = yet'),
])
def test_working_at_the_start_is_cut(reply, starts):
    out = ai_agent._without_working(reply, 'Please read the Thai in this photo.')
    assert out.startswith(starts)
    assert 'class' not in out


def test_the_working_stays_when_the_student_asked_for_it():
    assert ai_agent._without_working(TEMPLE, 'Why is ถาม a rising tone?') == TEMPLE


def test_working_later_in_a_reply_is_left_alone():
    reply = "**ถาม** (tǎam) = to ask\n\n- ถาม: ถ high class, live syllable, so rising tone"
    assert ai_agent._without_working(reply, 'ถาม') == reply


def test_a_reply_that_is_only_working_is_not_emptied():
    only = TEMPLE.split('\n\n')[0]
    assert ai_agent._without_working(only, 'hi') == only


def test_an_ordinary_reply_is_unchanged():
    reply = "**ขอบคุณ** (kɔ̀ɔp-kun)\nThank you"
    assert ai_agent._without_working(reply, 'thank you') == reply


# ── Both ways of getting a reply cut it ───────────────────────────────────

def _usage():
    return NS(input_tokens=1, output_tokens=1,
              cache_creation_input_tokens=0, cache_read_input_tokens=0)


class FakeMessages:
    """Replies with `text`, streamed a few characters at a time."""

    def __init__(self, text):
        self.reply = NS(stop_reason='end_turn', usage=_usage(),
                        content=[NS(type='text', text=text)])
        self.chunks = [text[i:i + 15] for i in range(0, len(text), 15)]

    def create(self, **request):
        return self.reply

    def stream(self, **request):
        outer = self

        class Manager:
            def __enter__(self):
                return NS(text_stream=iter(outer.chunks),
                          get_final_message=lambda: outer.reply)

            def __exit__(self, *a):
                return False
        return Manager()


@pytest.fixture
def agent(monkeypatch):
    # The spelling check is tested elsewhere; here it would only add noise.
    monkeypatch.setattr(ai_agent, '_checked', lambda t: t)
    a = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    a.client = NS(messages=FakeMessages(TEMPLE))
    return a


def test_a_one_piece_reply_is_cut(agent):
    r = agent.chat('s', 'Please read this photo.', mode='translator', history=[])
    assert r['response'].startswith('A sign for an information desk')


def test_a_streamed_reply_never_shows_the_working(agent):
    events, failure = agent.start_chat_stream('s', 'Please read this photo.',
                                              mode='translator', history=[])
    assert failure is None
    events = list(events)
    shown = ''.join(e['text'] for e in events if e['type'] == 'text')
    assert shown.startswith('A sign for an information desk')
    assert 'class' not in shown
    # What was shown is the answer, so nothing needs replacing.
    assert 'replace' not in [e['type'] for e in events]
    assert events[-1]['response'] == shown
