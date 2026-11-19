"""Work out when each sitemap page last changed, and save it to sitemap_dates.json.

The sitemap's <lastmod> tells Google which pages are worth re-visiting. It only
helps if it is honest: a sitemap that stamps every page with today's date
claims the whole site changes daily, and Google learns to ignore it. So each
date here is the last git commit that touched the files that page is made from:

  * the page's own templates (found by opening the page as a visitor and
    noting which templates render), leaving out the shared layout — a menu
    tweak changes every page's HTML but not what any page is about;
  * the content file behind a journal entry or a Dhamma talk;
  * section_previews.py for the public previews of locked sections.

A file with uncommitted changes counts as changed today, so running this
before committing gives the date the commit is about to make true.

Run it after changing a public page, and commit sitemap_dates.json with the
change:

    python scripts/update_sitemap_dates.py

tests/test_seo.py fails when a date is out of step with git, so a forgotten
run is caught before it reaches Google.
"""
import datetime
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATES_FILE = os.path.join(ROOT, 'sitemap_dates.json')

# Layout every page shares. Changes here are not changes to a page's content.
SHARED_TEMPLATES = ('base.html',)
SHARED_PREFIXES = ('partials/', '_', 'print/')


def _git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def _content_file(folder, slug):
    """The content/<folder>/*.json file whose 'slug' is this slug."""
    for path in sorted(glob.glob(os.path.join(ROOT, 'content', folder, '*.json'))):
        with open(path, encoding='utf-8') as f:
            if json.load(f).get('slug') == slug:
                return path
    return None


def source_files(app, path, preview_paths):
    """Repo-relative files a visitor's view of this page is built from."""
    from flask import template_rendered

    rendered = []

    def note(sender, template, context, **extra):
        rendered.append(template.name)

    with template_rendered.connected_to(note, app):
        app.test_client().get(path)

    files = {'templates/' + name for name in rendered
             if name not in SHARED_TEMPLATES and not name.startswith(SHARED_PREFIXES)}
    for folder, prefix in (('journal', '/journal/'), ('talks', '/dhamma-talk/')):
        if path.startswith(prefix):
            found = _content_file(folder, path[len(prefix):])
            if found:
                files.add(os.path.relpath(found, ROOT).replace(os.sep, '/'))
    if path in preview_paths:
        files.add('section_previews.py')
    return sorted(files)


def last_changed(files):
    """The date (YYYY-MM-DD) these files last changed, or None if unknown."""
    if not files:
        return None
    if _git('status', '--porcelain', '--', *files):
        return datetime.date.today().isoformat()
    return _git('log', '-1', '--format=%cs', '--', *files) or None


def compute_dates(app):
    import section_previews
    import seo

    preview_paths = {p['path'] for p in section_previews.SECTION_PREVIEWS.values()}
    dates = {}
    for path in seo.sitemap_paths():
        date = last_changed(source_files(app, path, preview_paths))
        if date:
            dates[path] = date
    return dates


def main():
    # Same safety as tests/conftest.py: never let `import app` reach the live
    # database, and don't trip the rate limits by opening every page at once.
    os.environ['DATABASE_URL'] = ''
    os.environ['DISABLE_RATE_LIMITS'] = '1'
    sys.path.insert(0, ROOT)
    import app as app_module

    dates = compute_dates(app_module.app)
    with open(DATES_FILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(dates, f, indent=2, sort_keys=True)
        f.write('\n')
    print('Saved {} page dates to sitemap_dates.json'.format(len(dates)))


if __name__ == '__main__':
    main()
