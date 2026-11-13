"""Every JavaScript file must at least parse (added 2026-11-13).

The Tones & Consonant Classes page script had a stray closing brace from July
to November 2026. A syntax error stops the WHOLE file, so the page's tabs and
all four drills were dead on the live site for four months. Nothing noticed:
no test ever ran the page's JavaScript, and the page itself still loaded.

Moving the inline scripts into static/js/ (for the Content-Security-Policy)
is what made this checkable. `node --check` parses a file without running it.

Skipped where Node isn't installed, like the other JavaScript tests.

Run with:  pytest tests/test_js_syntax.py -v
"""
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = sorted((ROOT / "static" / "js").rglob("*.js"))

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")


def test_there_are_scripts_to_check():
    # A wrong path would otherwise make every check below vanish silently.
    assert len(SCRIPTS) > 30


@pytest.mark.parametrize("path", SCRIPTS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_script_parses(path):
    result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
