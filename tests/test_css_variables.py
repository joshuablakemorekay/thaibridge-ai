"""Every var(--name) the site uses is actually defined (added 2026-08-19).

Found by accident while restyling /dhamma-and-culture: `--saffron` is typed
about seventy times across sixteen templates and once in base.css, and it had
never been defined anywhere. CSS does not warn about this — an undefined custom
property makes the *entire declaration* invalid, so the property silently falls
back to its inherited or initial value and the page still renders. That is why
it survived so long. `--gold` and `--cream` were missing too, which is why the
gender selector's active button had no background, no text colour and no border
all at the same time.

A misspelt colour is invisible in review and invisible in the browser's console.
It is only visible to a test that reads both sides.

Run with:  pytest tests/test_css_variables.py -v
"""

import glob
import io
import os
import re

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFINITION = re.compile(r"(--[A-Za-z0-9-]+)\s*:")
USAGE = re.compile(r"var\(\s*(--[A-Za-z0-9-]+)\s*([,)])")


def read(path):
    return io.open(path, encoding="utf-8").read()


def sources(*patterns):
    for pattern in patterns:
        for path in glob.glob(os.path.join(ROOT, pattern), recursive=True):
            yield path, read(path)


def defined_names():
    """Anything declared in a stylesheet OR in a template's own <style> block.

    Templates are included because a page may legitimately declare a variable
    it alone uses — /tones-classes sets --cls per consonant class that way.
    """
    names = set()
    for _, text in sources("static/css/*.css", "templates/**/*.html"):
        names.update(DEFINITION.findall(text))
    return names


def used_names():
    """name -> the files that reference it, so a failure says where to look.

    A `var(--x, fallback)` is deliberately excluded: the fallback is what makes
    it safe, and that form is the correct way to read a variable that may not
    be set on a given element.
    """
    uses = {}
    for path, text in sources("static/css/*.css", "templates/**/*.html",
                              "static/js/*.js"):
        for name, terminator in USAGE.findall(text):
            if terminator == ",":
                continue  # has a fallback
            uses.setdefault(name, set()).add(os.path.relpath(path, ROOT))
    return uses


@pytest.mark.parametrize("name", sorted(used_names()))
def test_the_variable_is_defined_somewhere(name):
    defined = defined_names()
    assert name in defined, (
        "%s is used in %s but never defined. An undefined custom property "
        "invalidates the whole declaration, so this colour is not being applied "
        "anywhere and nothing reports it." % (name, ", ".join(sorted(used_names()[name])))
    )


def test_the_aliases_still_match_the_colours_they_alias():
    """--saffron, --gold and --cream are shorthands, not second opinions.

    If someone later edits --monk-saffron and leaves --saffron behind, half the
    site changes colour and half does not, which is worse than the original bug.
    """
    css = read(os.path.join(ROOT, "static/css/base.css"))

    def value(name):
        match = re.search(re.escape(name) + r"\s*:\s*([^;]+);", css)
        assert match, "%s is no longer defined in base.css" % name
        return match.group(1).strip().lower()

    assert value("--saffron") == value("--monk-saffron")
    assert value("--gold") == value("--royal-gold")
    assert value("--cream") == value("--silk-cream")
