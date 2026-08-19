"""Tests for the politeness rungs shown under each line on the Sentences page.

`thai_registers.VARIANTS` is keyed by the **exact Thai string** of the formal
line it hangs off. That keeping is deliberate — it means the existing content in
app.py did not have to change shape to gain a Neutral and Casual version — but it
buys that convenience with one specific fragility, and these tests exist for it:

    if anyone edits a line in CONVERSATIONS, SENTENCE_PATTERNS or
    CONVERSATIONAL_PHRASES — even to fix a typo — its key stops matching, and
    the rungs underneath it silently disappear.

Nothing raises. The page still renders. It just quietly teaches less than it did
yesterday, and the only way to notice is to remember what used to be there. So
the first test below is the one that matters: every key must still correspond to
a line that is actually on the page.

The rest guard the two promises the page makes to a learner who cannot yet read
Thai — that every rung shown has a romanisation to read and a recording to copy
— and the one cultural rule the feature must not break: there is no casual way
to speak to a monk.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

from flask import session as flask_session  # noqa: E402

import app  # noqa: E402
import thai_audio  # noqa: E402
import thai_registers  # noqa: E402
from generate_thai_phrase_audio import _walk_thai  # noqa: E402


def page_thai_strings():
    """Every Thai string the Sentences page renders as a line of its own.

    Deliberately reuses the audio build script's walker rather than a second
    copy of the same recursion: if the two ever disagreed about what counts as
    a line on this page, the recordings and these tests would drift apart, and
    the drift would show up as missing audio rather than as a failing test.
    """
    found = []
    _walk_thai(app.CONVERSATIONS, found)
    _walk_thai(app.SENTENCE_PATTERNS, found)
    _walk_thai(app.CONVERSATIONAL_PHRASES, found)
    return list(dict.fromkeys(found))


def rungs():
    """(formal line, level key, variant) for every rung that carries Thai."""
    out = []
    for formal, entry in thai_registers.VARIANTS.items():
        for key in thai_registers.ORDER:
            variant = entry.get(key)
            if isinstance(variant, dict) and variant.get('thai'):
                out.append((formal, key, variant))
    return out


def _short(thai, limit=24):
    return thai if len(thai) <= limit else thai[:limit] + '…'


# ── The one that catches silent drift ──────────────────────────────────────

@pytest.mark.parametrize('formal', sorted(thai_registers.VARIANTS),
                         ids=_short)
def test_every_keyed_line_is_still_on_the_page(formal):
    """A key with no matching line means its rungs stopped being displayed.

    This fails the moment someone edits the formal line in app.py without
    editing the key here — which is exactly the change that would otherwise
    remove content from the page without anybody noticing.
    """
    assert formal in page_thai_strings(), (
        f'{formal!r} is keyed in thai_registers.VARIANTS but no longer appears '
        f'on the Sentences page. If the line was edited, update the key to '
        f'match; if it was deleted, delete its entry here too.'
    )


# ── What every rung owes the learner ───────────────────────────────────────

@pytest.mark.parametrize('formal,level,variant', rungs(),
                         ids=lambda v: _short(v) if isinstance(v, str) else '')
def test_every_rung_has_a_romanisation(formal, level, variant):
    """Thai script without Paiboon is unreadable to most of this page's users.

    The page's whole premise is that a beginner can read the romanisation while
    they learn the script, so a rung with Thai and no Paiboon is worse than no
    rung at all.
    """
    assert variant.get('paiboon', '').strip(), (
        f'the {level} rung of {formal!r} has Thai but no paiboon'
    )


@pytest.mark.parametrize('formal,level,variant', rungs(),
                         ids=lambda v: _short(v) if isinstance(v, str) else '')
def test_every_rung_has_a_recording(formal, level, variant):
    """Tones are the point, and they do not survive romanisation.

    A written rung tells a learner the words; only the clip tells them how it
    should sound. If this fails, the fix is to run:

        python scripts/generate_thai_phrase_audio.py --page sentences
    """
    assert thai_audio.audio_exists(app.app.static_folder, variant['thai']), (
        f'no MP3 for the {level} rung of {formal!r} ({variant["thai"]!r})'
    )


# ── The cultural rule the feature must not break ───────────────────────────

def monk_dialogue_lines():
    """Every line spoken in a conversation that has a monk in it."""
    out = []
    for conv_id in ('offering_alms', 'learning_meditation'):
        for line in app.CONVERSATIONS[conv_id]['dialogue']:
            out.append((conv_id, line['thai']))
    return out


@pytest.mark.parametrize('conv_id,thai', monk_dialogue_lines(),
                         ids=lambda v: _short(v))
def test_no_casual_rung_where_a_monk_is_speaking_or_listening(conv_id, thai):
    """Monastic is a different vocabulary, not a lower rung on the ladder.

    Dropping ครับ/ค่ะ or swapping ถวาย for ให้ with a monk is the one thing this
    page must never model, so these two dialogues get a monastic note in the
    third slot instead of a casual form. A casual rung appearing here would mean
    somebody had treated the register as if it slid down like the others.
    """
    entry = thai_registers.VARIANTS.get(thai, {})
    assert 'casual' not in entry, (
        f'{thai!r} in the {conv_id} dialogue has a casual rung. Speaking with '
        f'monastics has no casual register — use a monastic note instead.'
    )


# ── The helper the template leans on ───────────────────────────────────────

def test_an_unknown_line_renders_nothing_rather_than_failing():
    """The template calls variants_for() on every line, keyed or not.

    Returning an empty list for a line with no entry is what lets the 22
    register-less lines (the bare-verb table, the hesitation fillers) share one
    macro with the rest instead of needing a guard at each call site.
    """
    assert thai_registers.variants_for('ไม่มีอยู่จริง') == []
    assert thai_registers.warning_for('ไม่มีอยู่จริง') is None


def test_a_same_rung_carries_no_thai_of_its_own():
    """SAME means 'identical to the formal line', so it must not repeat it.

    If a SAME rung ever gained its own `thai`, the page would print the same
    sentence twice under two different labels and the learner would be left
    looking for a difference that is not there.
    """
    for formal, entry in thai_registers.VARIANTS.items():
        for key in thai_registers.ORDER:
            variant = entry.get(key)
            if isinstance(variant, dict) and variant.get('same'):
                assert 'thai' not in variant, (
                    f'the {key} rung of {formal!r} is marked SAME but also '
                    f'carries its own Thai'
                )


# ── The Formal label on the page ───────────────────────────────────────────

@pytest.fixture(scope='module')
def sentences_html():
    """The rendered Sentences page, seen by a learner who can open it.

    The page is gated behind Level 5 and a Basic subscription, so an anonymous
    client gets the locked page instead — which renders no rungs at all and
    would let every assertion below pass for the wrong reason. Hence the
    explicit check that we are looking at the real thing.
    """
    app.app.config['TESTING'] = True

    # Build the app's own default progress dict rather than hand-writing one, so
    # a new key added to it later cannot make this fixture the thing that breaks.
    with app.app.test_request_context():
        app.init_user_progress()
        progress = dict(flask_session['user_progress'])
    progress.update({
        'level': 99, 'subscription_tier': 'pro', 'full_unlock': True,
        'alphabet_completed': True,
    })

    client = app.app.test_client()
    with client.session_transaction() as sess:
        sess['user_progress'] = progress
    html = client.get('/sentences').get_data(as_text=True)
    assert 'Section Locked' not in html, 'the gate is still shut — see docstring'
    return html


def test_every_rung_stack_is_labelled_formal_at_the_top(sentences_html):
    """The main line IS the formal rung, and used to be the only unlabelled one.

    Without its own chip the ladder read as two levels (Neutral, Casual) hanging
    off an unnamed sentence, and the learner had to carry 'the big line is the
    formal one' in their head from the intro card.

    Counted as a total rather than per block, because the chip sits on the main
    line *above* its rungs — the two are siblings, not parent and child. The
    macro's chip carries reg-tag-main so the intro card's hand-written example
    ladder, which is an explainer rather than a line, stays out of the count.
    """
    stacks = sentences_html.split('<div class="reg-block">')[1:]
    with_rungs = sum(1 for block in stacks if 'class="reg-row"' in block)
    assert with_rungs > 100, f'only {with_rungs} rung stacks rendered'
    assert sentences_html.count('reg-tag-main') == with_rungs


def test_a_warning_only_line_gets_no_formal_chip(sentences_html):
    """A line can carry a note without carrying rungs — แบบว่า... is already
    casual, so it has something to say and nothing to compare against. Those
    blocks must render the warning and no chip."""
    stacks = sentences_html.split('<div class="reg-block">')[1:]
    warning_only = [b for b in stacks if 'class="reg-row"' not in b]
    assert warning_only, 'no warning-only block on the page to check'
    for block in warning_only:
        assert 'reg-warn' in block
        assert 'reg-tag-main' not in block.split('</div>')[0]


def test_a_line_with_no_rungs_gets_no_formal_chip(sentences_html):
    """A lone Formal tag with nothing beneath it labels a comparison that isn't
    being made, so the register-less lines stay bare."""
    lines = sentences_html.count('class="thai-text"')
    assert sentences_html.count('>Formal</span>') < lines
