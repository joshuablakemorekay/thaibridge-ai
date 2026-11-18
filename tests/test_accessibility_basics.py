"""Phase 3a of the website work: accessibility basics every page shares.

* a "Skip to content" link, first in the page, pointing at <main>
* the phone menu button has a name ("Menu") and says whether it is open
* Thai text is marked lang="th", so screen readers switch to a Thai voice
  and browsers and search engines know which language it is
"""
import pathlib
import re

import app as app_module

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _html(path='/'):
    return app_module.app.test_client().get(path).get_data(as_text=True)


def test_skip_link_is_the_first_thing_in_the_page_and_reaches_main():
    html = _html('/survival')
    body = html.split('<body', 1)[1]
    first_link = re.search(r'<a\b[^>]*>', body).group(0)
    assert 'class="skip-link"' in first_link and 'href="#main-content"' in first_link
    assert '<main id="main-content"' in html


def test_phone_menu_button_is_labelled():
    html = _html()
    button = re.search(r'<button class="mobile-menu-toggle"[^>]*>', html).group(0)
    assert 'aria-label="Menu"' in button
    assert 'aria-expanded="false"' in button
    assert "setAttribute('aria-expanded'" in (ROOT / 'static' / 'js' / 'base.js').read_text(encoding='utf-8')


def test_thai_text_is_marked_as_thai():
    html = _html('/survival')
    assert re.search(r'class="thai-text" lang="th">', html)


def test_no_thai_class_is_left_without_a_language():
    # Any element styled as Thai must also say it is Thai.
    missing = []
    for path in (ROOT / 'templates').rglob('*.html'):
        if 'print' in path.parts:
            continue
        for tag in re.findall(r'<[a-zA-Z][a-zA-Z0-9]*\b[^<>]*\bclass="[^"]*"[^<>]*>', path.read_text(encoding='utf-8')):
            classes = re.search(r'class="([^"]*)"', tag).group(1).split()
            if {'thai', 'thai-text'} & set(classes) and 'lang=' not in tag:
                missing.append(f'{path.name}: {tag[:80]}')
    assert not missing, missing[:5]
