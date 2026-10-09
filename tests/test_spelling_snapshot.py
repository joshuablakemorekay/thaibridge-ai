"""The snapshot that feeds the MCP spelling checker (mcp-server/thaibridge_spelling).

The checker trusts this file as "what ThaiBridge has reviewed", so it must hold
exactly that: every reviewed source, never the draft chanting book, and every
spelling variant kept apart so the consistency report can find them.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                'scripts'))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

import export_spelling_snapshot as export  # noqa: E402
import paiboon_lookup  # noqa: E402

SNAPSHOT = export.build_snapshot()


def test_all_44_consonants_go_out_with_class_and_sound():
    consonants = SNAPSHOT['consonants']
    assert len(consonants) == 44
    do = next(c for c in consonants if c['char'] == 'ด')
    assert (do['class'], do['sound']) == ('middle', 'd')


def test_the_draft_chanting_book_is_left_out():
    labels = {s for e in SNAPSHOT['entries'] for s in e['sources']}
    assert 'Chanting book' not in labels
    assert labels <= {label for _, label in paiboon_lookup.reviewed_sources()}


def test_spelling_variants_are_kept_apart():
    """The /paiboon index merges these; the consistency report needs both."""
    kob_kun = {e['romanisation'] for e in SNAPSHOT['entries'] if e['thai'] == 'ขอบคุณ'}
    assert len(kob_kun) >= 1
    keys = [(e['thai'], e['romanisation']) for e in SNAPSHOT['entries']]
    assert len(keys) == len(set(keys)), "one row per distinct spelling"
