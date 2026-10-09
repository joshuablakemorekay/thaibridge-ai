"""The phrase-audio build script must never leave an empty MP3 behind.

edge-tts opens the output file before any audio arrives. When the voice
service refuses a request (it throttles after a burst), the file is left on
disk at 0 bytes. The next run then counts it as "already present", never
retries, and the page shows a listen button that plays nothing. This happened
for real while recording the Tour Guide trips: 110 empty files in one run.

These tests fake the voice service, so they need no network and no edge-tts.
"""
import asyncio
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import generate_thai_phrase_audio as gen  # noqa: E402
import thai_audio  # noqa: E402

PHRASE = 'ทดสอบ'


@pytest.fixture
def fake_run(monkeypatch, tmp_path):
    """Point the script at a temp static folder with one one-phrase page."""
    monkeypatch.setattr(gen, 'STATIC_DIR', str(tmp_path))
    monkeypatch.setattr(gen, 'PAGES', {'test': lambda: [PHRASE]})
    monkeypatch.setitem(sys.modules, 'edge_tts', types.ModuleType('edge_tts'))
    return thai_audio.audio_disk_path(str(tmp_path), PHRASE)


def test_a_refused_recording_leaves_no_file(fake_run, monkeypatch):
    async def refused(text, out_path):
        open(out_path, 'wb').close()        # what edge-tts does before failing
        raise RuntimeError('No audio was received')

    monkeypatch.setattr(gen, 'synthesize', refused)
    asyncio.run(gen.main(['test'], force=False))
    assert not os.path.exists(fake_run), 'an empty mp3 was left behind'


def test_the_next_run_retries_the_phrase(fake_run, monkeypatch):
    """The point of deleting it: a later run must try again, not skip it.

    Guarded twice: the failed attempt deletes its empty file, and the runner
    also treats any 0-byte file as missing. Either alone keeps this passing,
    which is deliberate, since an empty mp3 can also come from an aborted run."""
    calls = []

    async def refused(text, out_path):
        open(out_path, 'wb').close()
        raise RuntimeError('No audio was received')

    async def works(text, out_path):
        calls.append(text)
        with open(out_path, 'wb') as f:
            f.write(b'ID3 fake mp3')

    monkeypatch.setattr(gen, 'synthesize', refused)
    asyncio.run(gen.main(['test'], force=False))
    monkeypatch.setattr(gen, 'synthesize', works)
    asyncio.run(gen.main(['test'], force=False))

    assert calls == [PHRASE]
    assert os.path.getsize(fake_run) > 0
