"""Tests for the Pronunciation Analysis measuring code (static/js/pronounce_core.js).

The code is JavaScript because it runs in the learner's browser, so these tests
run it in Node. They feed it made-up voices whose pitch is known exactly — a
steady note, a rising glide, a falling glide — and check it measures them
right. A real Thai tone is a glide like these, so if the measuring is wrong
here it would be wrong for every learner.

Skipped (not failed) when Node is not installed.
"""

import json
import os
import shutil
import subprocess

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(REPO_ROOT, "static", "js", "pronounce_core.js")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")

# A voice-like test signal: a fundamental plus two quieter harmonics (a pure
# sine is too easy), gliding from one pitch to another over `seconds`.
HARNESS = r"""
const core = require(process.argv[2]);
const RATE = 48000;

function voice(fromHz, toHz, seconds, startSilence) {
    const n = Math.floor(RATE * seconds), lead = Math.floor(RATE * (startSilence || 0));
    const out = new Float32Array(lead + n);
    let phase = 0;
    for (let i = 0; i < n; i++) {
        const hz = fromHz + (toHz - fromHz) * (i / n);
        phase += 2 * Math.PI * hz / RATE;
        out[lead + i] = 0.6 * Math.sin(phase) + 0.25 * Math.sin(2 * phase) + 0.1 * Math.sin(3 * phase);
    }
    return out;
}
const line = (a, b, s, lead) => core.contour(voice(a, b, s, lead), RATE);

const steady = line(150, 150, 0.6).filter(Boolean);
const result = {
    steady120: core.framePitch(voice(120, 120, 0.1).subarray(0, 1024), RATE),
    steady220: core.framePitch(voice(220, 220, 0.1).subarray(0, 1024), RATE),
    steady400: core.framePitch(voice(400, 400, 0.1).subarray(0, 1024), RATE),
    steadyMedian: steady[Math.floor(steady.length / 2)],
    silence: core.contour(new Float32Array(RATE), RATE).filter(Boolean).length,
    rise: core.movement(core.shape(line(150, 220, 0.6))),
    fall: core.movement(core.shape(line(220, 150, 0.6))),
    level: core.movement(core.shape(line(160, 162, 0.6))),
    sameShapeDifferentVoice: core.compare(line(110, 160, 0.5), line(200, 290, 0.7)),
    wrongDirection: core.compare(line(150, 220, 0.5), line(220, 150, 0.5)),
    leadingSilenceIgnored: core.compare(line(150, 220, 0.5), line(150, 220, 0.5, 0.4)),
    nothingHeard: core.compare(line(150, 220, 0.5), new Float32Array(RATE)),
    heard: [
        core.heardWord('ไม่เผ็ด', ['ไม่ เผ็ด']),
        core.heardWord('ไม่เผ็ด', ['ไม่เผ็ดค่ะ']),
        core.heardWord('ไม่เผ็ด', ['เผ็ด', 'ไม่เผ็ดครับ']),
        core.heardWord('ไม่เผ็ด', ['เผ็ด']),
        core.heardWord('ไม่เผ็ด', []),
    ],
};
// Lines are long; tests only need their length.
for (const k of ['sameShapeDifferentVoice', 'wrongDirection', 'leadingSilenceIgnored']) {
    if (result[k]) { result[k].model = result[k].model.length; result[k].yours = result[k].yours.length; }
}
console.log(JSON.stringify(result));
"""


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    harness = tmp_path_factory.mktemp("pronounce") / "harness.js"
    harness.write_text(HARNESS, encoding="utf-8")
    out = subprocess.run(["node", str(harness), CORE], capture_output=True,
                         text=True, encoding="utf-8", check=True, timeout=60)
    return json.loads(out.stdout)


@pytest.mark.parametrize("key, hz", [("steady120", 120), ("steady220", 220), ("steady400", 400)])
def test_measures_a_steady_note_within_two_percent(measured, key, hz):
    """Including no octave slip — the classic autocorrelation mistake."""
    assert measured[key] == pytest.approx(hz, rel=0.02)


def test_a_whole_line_reads_the_note(measured):
    assert measured["steadyMedian"] == pytest.approx(150, rel=0.02)


def test_silence_has_no_pitch(measured):
    assert measured["silence"] == 0


def test_tells_rising_falling_and_level_apart(measured):
    assert (measured["rise"], measured["fall"], measured["level"]) == ("rises", "falls", "level")


def test_same_shape_in_a_different_voice_scores_high(measured):
    """A learner an octave up, speaking slower, still matches the model's shape."""
    result = measured["sameShapeDifferentVoice"]
    assert result["score"] >= 85
    assert result["modelMove"] == result["yourMove"] == "rises"
    assert result["model"] == result["yours"]


def test_wrong_direction_scores_low_and_says_why(measured):
    result = measured["wrongDirection"]
    assert result["score"] < 55
    assert "rises" in result["advice"] and "falls" in result["advice"]


def test_a_pause_before_speaking_does_not_count_against_you(measured):
    assert measured["leadingSilenceIgnored"]["score"] >= 95


def test_nothing_heard_gives_no_result(measured):
    assert measured["nothingHeard"] is None


def test_word_check_ignores_spaces_and_polite_particles(measured):
    assert measured["heard"] == [True, True, True, False, False]
