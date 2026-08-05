"""Guards against the printed prompt sheets going stale.

Written because they did. The chanting batch workflow moved from Claude.ai chat
into Claude Code, prompt.md was rewritten, the PDF was regenerated — and the
sheet still told the reader to open Claude.ai and paste a batch of chants,
because that wrapper text is hardcoded in scripts/make_prompt_pdf.py rather than
read from the prompt.

What made it slip through was the shape of the check, not the lack of one. The
rebuilt PDF was verified to CONTAIN the new rules; nobody verified it no longer
contained the old ones. A stale instruction sits quite happily beside a correct
one, and the reader follows whichever they meet first.

So these assert absence, not presence.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

from make_prompt_pdf import VARIANTS  # noqa: E402


def wrapper_text(variant):
    """Every string the sheet prints around the prompts themselves."""
    spec = VARIANTS[variant]
    parts = [spec['title'], spec['subtitle']]
    for heading, body in spec['howto']:
        parts += [heading, body]
    for heading, body in spec['stages']:
        parts += [heading, body]
    for heading, body in (spec['depth'] or []):
        parts += [heading, body]
    return '\n'.join(parts)


class TestTheBatchSheetMatchesTheBatchWorkflow:
    """chanting-book-batch runs entirely in Claude Code and reads files."""

    def test_it_never_tells_you_to_open_a_chat(self):
        text = wrapper_text('chanting-book-batch')

        assert 'Claude.ai' not in text, \
            'the batch sheet still points at the chat workflow it moved off'

    def test_it_never_instructs_you_to_paste(self):
        """Nothing is pasted any more — the stages read and write files.

        'Paste this, then the JSON underneath it' is the most misleading line
        the old sheet carried: it describes a workflow that looks like it works
        while damaging the Thai in transit.

        Matched as a whole word so the sheet can still SAY that nothing is
        pasted, which is a true and useful thing for it to say. The instruction
        is what must not survive, not the topic.
        """
        text = wrapper_text('chanting-book-batch')

        assert not re.search(r'\bpaste\b', text, re.IGNORECASE), \
            'the batch sheet still instructs the reader to paste something'

    def test_it_says_where_the_work_actually_happens(self):
        text = wrapper_text('chanting-book-batch')

        assert 'Claude Code' in text
        assert 'batches/' in text


class TestTheSingleChantSheetIsLeftAlone:
    """chanting-book-entry is deliberately frozen and IS still a chat workflow.

    Asserted so that a future tidy-up of the batch sheet does not sweep this one
    along with it. Its Claude.ai references are correct.
    """

    def test_it_still_describes_the_chat_workflow(self):
        text = wrapper_text('chanting-book-entry')

        assert 'Claude.ai' in text
        assert 'Paste' in text


@pytest.mark.parametrize('variant', sorted(VARIANTS))
def test_every_stage_has_a_heading_and_a_description(variant):
    for heading, body in VARIANTS[variant]['stages']:
        assert heading.strip()
        assert body.strip()


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
