"""The tutor looks up Thai spellings, and its answers are checked against the lessons.

On 2026-10-14 the tutor wrote บริบท as "boo-rì-bàt" (it is bɔɔ-rí-bòt): a word
it brought in itself, so the per-question reference never covered it. These
tests pin the three layers that fix that: the lookup tool's answers, the loop
that lets the model call it, and the check that corrects a finished answer
even when the model skipped the lookup. No test here reaches the real API.
"""
import os
import sys
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

import ai_agent  # noqa: E402
import paiboon_lookup  # noqa: E402
import tutor_reference  # noqa: E402

E = paiboon_lookup.Entry
INDEX = [
    E('ขอบคุณ', 'kɔ̀ɔp-kun', 'Thank you', 'Survival Thai'),
    E('ครับ', 'kráp', 'polite particle (male)', 'Survival Thai'),
    E('ค่ะ', 'kâ', 'polite particle (female)', 'Survival Thai'),
    E('ไป', 'bpai', 'go', 'Vocabulary'),
    E('ทำบุญ', 'tam-bun', 'make merit', 'Read & Write'),
    E('สวัสดี', 'sà-wàt-dii', 'hello', 'Survival Thai'),
    # A word the lessons spell two ways: never "corrected" either way.
    E('ช้าง', 'cháaŋ', 'elephant', 'Vocabulary'),
    E('ช้าง', 'cháŋ', 'elephant', 'Culture'),
]


# ── The lookup tool ──────────────────────────────────────────────────────

def test_a_word_in_the_lessons_comes_back_checked():
    out = tutor_reference.look_up(['ขอบคุณ'], INDEX)
    assert 'kɔ̀ɔp-kun' in out and 'CHECKED' in out


def test_a_phrase_made_of_checked_words_is_put_together():
    out = tutor_reference.look_up(['ไปทำบุญ'], INDEX)
    assert 'bpai tam-bun' in out and 'ไป + ทำบุญ' in out


def test_an_unknown_word_gets_its_consonant_classes_not_a_guess():
    out = tutor_reference.look_up(['บริบท'], INDEX)
    assert 'NOT IN THE LESSONS' in out
    assert 'บ middle' in out and 'ร low' in out and 'ท low' in out
    # It never invents a romanisation for a word it does not have.
    assert 'boo' not in out and 'bɔɔ' not in out


def test_tone_marks_are_named_for_an_unknown_word():
    assert 'mai tho' in tutor_reference.look_up(['บ้านใหม่'], INDEX)


def test_junk_input_is_handled():
    assert tutor_reference.look_up([], INDEX) == 'No Thai words were given.'
    assert tutor_reference.look_up('ไป', INDEX).startswith('- ไป')
    many = [f'ไป{i}' for i in range(100)]
    # One line per word, capped, plus the closing reminder.
    assert tutor_reference.look_up(many, INDEX).count('\n') == tutor_reference.MAX_TOOL_WORDS


def test_the_answer_must_not_show_the_tone_working():
    assert 'never shows the working' in tutor_reference.look_up(['บริบท'], INDEX)


# ── The check on a finished answer ───────────────────────────────────────

def check(text):
    return tutor_reference.check_spellings(text, INDEX)


def test_a_misspelling_of_a_known_word_is_corrected():
    text, fixes = check('Say ขอบคุณ (khop-khun) to thank someone.')
    assert text == 'Say ขอบคุณ (kɔ̀ɔp-kun) to thank someone.'
    assert fixes == [('ขอบคุณ', 'khop-khun', 'kɔ̀ɔp-kun')]


def test_bold_thai_is_corrected_and_stays_bold():
    text, _ = check('**สวัสดี** (sa-wat-dee)')
    assert text == '**สวัสดี** (sà-wàt-dii)'


def test_a_right_spelling_is_left_alone():
    assert check('ครับ (kráp)') == ('ครับ (kráp)', [])


def test_a_gloss_in_brackets_is_not_overwritten():
    assert check('Men end with ครับ (male) and women with ค่ะ (female).')[1] == []


def test_alternatives_are_not_touched():
    assert check('Add ครับ/ค่ะ (kráp/kâ) at the end.')[1] == []


def test_a_word_the_lessons_spell_two_ways_is_left_alone():
    assert check('ช้าง (chang)')[1] == []


def test_a_word_the_lessons_do_not_have_is_left_alone():
    assert check('บริบท (boo-rì-bàt)')[1] == []


def test_thai_in_quote_marks_is_corrected():
    assert check('Say "ครับ" (krap).')[0] == 'Say "ครับ" (kráp).'


def test_a_phrase_made_of_known_words_is_corrected():
    text, _ = check('ขอบคุณค่ะ (kɔ̀ɔp kun kâ)')
    assert text == 'ขอบคุณค่ะ (kɔ̀ɔp-kun kâ)'


def test_josh_confirmed_spellings_reach_the_tutor(monkeypatch):
    # บริบท is the word that started this; it is in no lesson yet.
    monkeypatch.setattr(paiboon_lookup, 'get_index', lambda: INDEX)
    index = tutor_reference._index()
    assert 'bɔɔ-rí-bòt' in tutor_reference.look_up(['บริบท'], index)
    assert tutor_reference.check_spellings('บริบท (boo-rì-bàt)', index)[0] == 'บริบท (bɔɔ-rí-bòt)'


def test_a_confirmed_spelling_gives_way_once_a_lesson_teaches_the_word(monkeypatch):
    taught = INDEX + [E('บริบท', 'bɔɔ-rí-bòt', 'context', 'Vocabulary')]
    monkeypatch.setattr(paiboon_lookup, 'get_index', lambda: taught)
    assert [e.source for e in tutor_reference._index() if e.thai == 'บริบท'] == ['Vocabulary']


# ── The loop that lets the model look words up ───────────────────────────

def block(type_, **kw):
    return NS(type=type_, **kw)


def usage(i=10, o=5):
    return NS(input_tokens=i, output_tokens=o,
              cache_creation_input_tokens=0, cache_read_input_tokens=0)


LOOKUP = NS(stop_reason='tool_use', usage=usage(),
            content=[block('tool_use', id='t1', name=tutor_reference.SPELLING_TOOL_NAME,
                           input={'words': ['ขอบคุณ']})])
ANSWER = NS(stop_reason='end_turn', usage=usage(),
            content=[block('text', text='Say ขอบคุณ (khop-khun).')])


class FakeMessages:
    def __init__(self, replies):
        self.replies, self.requests = list(replies), []

    def create(self, **request):
        self.requests.append(request)
        return self.replies.pop(0)

    def stream(self, **request):
        self.requests.append(request)
        reply = self.replies.pop(0)
        texts = [b.text for b in reply.content if b.type == 'text']

        class Manager:
            def __enter__(self):
                return NS(text_stream=iter(texts), get_final_message=lambda: reply)

            def __exit__(self, *a):
                return False
        return Manager()


def agent_with(replies):
    agent = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    agent.client = NS(messages=FakeMessages(replies))
    return agent


def test_every_request_offers_the_spelling_tool():
    agent = agent_with([ANSWER])
    agent.chat('s', 'hi', mode='tutor', history=[])
    assert agent.client.messages.requests[0]['tools'] == [tutor_reference.SPELLING_TOOL]


def test_a_lookup_is_answered_and_the_answer_is_checked(monkeypatch):
    monkeypatch.setattr(tutor_reference, '_index', lambda: INDEX)
    agent = agent_with([LOOKUP, ANSWER])
    result = agent.chat('s', 'how do I say thank you?', mode='tutor', history=[])
    second = agent.client.messages.requests[1]['messages']
    assert second[-1]['content'][0]['type'] == 'tool_result'
    assert 'kɔ̀ɔp-kun' in second[-1]['content'][0]['content']
    # Corrected even though the fake model ignored its own lookup.
    assert result['response'] == 'Say ขอบคุณ (kɔ̀ɔp-kun).'
    # Both requests are counted for the cost log.
    assert result['tokens_used']['input'] == 20


def test_the_last_round_must_answer(monkeypatch):
    monkeypatch.setattr(tutor_reference, '_index', lambda: INDEX)
    rounds = ai_agent.MAX_TOOL_ROUNDS
    agent = agent_with([LOOKUP] * rounds + [ANSWER])
    agent.chat('s', 'hi', mode='tutor', history=[])
    requests = agent.client.messages.requests
    assert len(requests) == rounds + 1
    assert requests[-1]['tool_choice'] == {'type': 'none'}
    assert all('tool_choice' not in r for r in requests[:-1])


def test_a_streamed_answer_is_corrected_with_a_replace_line(monkeypatch):
    monkeypatch.setattr(tutor_reference, '_index', lambda: INDEX)
    agent = agent_with([LOOKUP, ANSWER])
    events, failure = agent.start_chat_stream('s', 'thanks?', mode='tutor', history=[])
    assert failure is None
    events = list(events)
    assert [e['type'] for e in events] == ['text', 'replace', 'done']
    assert events[1]['text'] == 'Say ขอบคุณ (kɔ̀ɔp-kun).'
    assert events[-1]['response'] == 'Say ขอบคุณ (kɔ̀ɔp-kun).'


def test_a_streamed_answer_that_is_already_right_needs_no_replace(monkeypatch):
    monkeypatch.setattr(tutor_reference, '_index', lambda: INDEX)
    right = NS(stop_reason='end_turn', usage=usage(),
               content=[block('text', text='Say ขอบคุณ (kɔ̀ɔp-kun).')])
    events, _ = agent_with([right]).start_chat_stream('s', 'thanks?', mode='tutor', history=[])
    assert [e['type'] for e in events] == ['text', 'done']


def test_words_written_before_a_lookup_are_never_shown(monkeypatch):
    monkeypatch.setattr(tutor_reference, '_index', lambda: INDEX)
    chatty = NS(stop_reason='tool_use', usage=usage(),
                content=[block('text', text='Let me check those spellings.'),
                         *LOOKUP.content])
    events, _ = agent_with([chatty, ANSWER]).start_chat_stream('s', 'hi', mode='tutor',
                                                                history=[])
    shown = ''.join(e['text'] for e in events if e['type'] == 'text')
    assert 'Let me check' not in shown


def test_a_long_answer_still_streams_in_pieces(monkeypatch):
    monkeypatch.setattr(tutor_reference, '_index', lambda: INDEX)
    long = NS(stop_reason='end_turn', usage=usage(),
              content=[block('text', text='word ' * 30), block('text', text='more ' * 30),
                       block('text', text='and ' * 30)])
    events, _ = agent_with([long]).start_chat_stream('s', 'hi', mode='tutor', history=[])
    # The first two pieces are held back together; after that it streams.
    assert [e['type'] for e in events].count('text') == 2


def test_every_mode_is_told_to_use_the_tool():
    agent = ai_agent.ThaiLearningAI(api_key='test-key-not-used')
    for mode in ('conversation', 'tutor', 'generator', 'cultural', 'buddhist', 'helper',
                 'translator'):
        assert tutor_reference.SPELLING_TOOL_NAME in agent.get_system_prompt(mode, {})
