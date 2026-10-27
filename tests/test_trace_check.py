"""Tests for Writing Practice's letter checking (static/js/trace_check.js).

The checker runs in the learner's browser, so these tests run it in Node with
made-up "letters" drawn as grids — a ring, its halves, a bar — whose right
answers are obvious: tracing all of the ring is done, half of it is not (and
the missing half is named), scribbling off it is flagged, and a smaller ring
written from memory in a corner still has the right shape.

Skipped (not failed) when Node is not installed.
"""

import json
import os
import shutil
import subprocess

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO_ROOT, "static", "js", "trace_check.js")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")

HARNESS = r"""
const tc = require(process.argv[2]);
const N = 48;

// A ring of radius r and thickness t around (cx, cy), optionally only where keep(x, y).
function ring(cx, cy, r, t, keep) {
    const g = new Array(N * N).fill(false);
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
        const d = Math.hypot(x - cx, y - cy);
        if (Math.abs(d - r) <= t / 2 && (!keep || keep(x, y))) g[y * N + x] = true;
    }
    return g;
}
function bar(x0, x1, y0, y1) {
    const g = new Array(N * N).fill(false);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) g[y * N + x] = true;
    return g;
}
const or = (a, b) => a.map((v, i) => v || b[i]);
const pick = r => ({ covered: +r.covered.toFixed(2), off: +r.off.toFixed(2), done: r.done,
                     missing: r.missing, message: r.message });

const letter = ring(24, 24, 15, 4);
console.log(JSON.stringify({
    empty: pick(tc.assess(letter, new Array(N * N).fill(false), N)),
    whole: pick(tc.assess(letter, ring(24, 24, 15, 2), N)),
    leftHalf: pick(tc.assess(letter, ring(24, 24, 15, 2, (x) => x < 24), N)),
    topHalf: pick(tc.assess(letter, ring(24, 24, 15, 2, (x, y) => y < 24), N)),
    scribble: pick(tc.assess(letter, or(ring(24, 24, 15, 2), bar(0, 10, 0, 47)), N)),
    memorySmallInCorner: pick(tc.assessFromMemory(letter, ring(12, 12, 8, 2), N)),
    memoryWrongShape: pick(tc.assessFromMemory(letter, bar(20, 22, 5, 40), N)),
    memoryEmpty: pick(tc.assessFromMemory(letter, new Array(N * N).fill(false), N)),
    zoneWider: tc.zone(letter, N).filter(Boolean).length > letter.filter(Boolean).length,
}));
"""


@pytest.fixture(scope="module")
def checked(tmp_path_factory):
    harness = tmp_path_factory.mktemp("trace") / "harness.js"
    harness.write_text(HARNESS, encoding="utf-8")
    out = subprocess.run(["node", str(harness), CHECK], capture_output=True,
                         text=True, encoding="utf-8", check=True, timeout=60)
    return json.loads(out.stdout)


def test_nothing_drawn_asks_you_to_start(checked):
    assert not checked["empty"]["done"]
    assert "Trace over" in checked["empty"]["message"]


def test_tracing_the_whole_letter_is_done(checked):
    whole = checked["whole"]
    assert whole["done"] and whole["covered"] >= 0.95 and whole["off"] == 0
    assert "Well done" in whole["message"]


@pytest.mark.parametrize("case, missing", [("leftHalf", "right"), ("topHalf", "bottom")])
def test_half_a_letter_names_the_missing_part(checked, case, missing):
    result = checked[case]
    assert not result["done"]
    assert 0.4 <= result["covered"] <= 0.65
    assert result["missing"] == missing
    assert f"the {missing} part" in result["message"]


def test_scribbling_off_the_letter_is_flagged(checked):
    result = checked["scribble"]
    assert not result["done"]
    assert result["off"] > 0.2
    assert "wander off" in result["message"]


def test_from_memory_a_smaller_letter_elsewhere_has_the_right_shape(checked):
    assert checked["memorySmallInCorner"]["done"]


def test_from_memory_a_different_shape_is_not_accepted(checked):
    result = checked["memoryWrongShape"]
    assert not result["done"]
    assert "Show the guide" in result["message"]


def test_from_memory_empty_asks_you_to_write(checked):
    assert "tap Check" in checked["memoryEmpty"]["message"]


def test_the_red_line_zone_reaches_past_the_letter(checked):
    """Ink just beside the letter still counts as on it — a pen is wider than a pixel."""
    assert checked["zoneWider"]
