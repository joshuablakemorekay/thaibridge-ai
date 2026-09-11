#!/usr/bin/env python3
"""check_commentary.py — did the commentary pass leave the verses alone?

    PYTHONIOENCODING=utf-8 DATABASE_URL="" python scripts/check_commentary.py
    PYTHONIOENCODING=utf-8 DATABASE_URL="" python scripts/check_commentary.py --against HEAD

Why this exists
---------------
Stage 3 writes prose INTO `chanting.py`, next to Pali that has already been
verified against the physical book. The one rule outranking everything in that
pass is that no verse, title, page number, invitation, section label or rubric
may change while the prose is added — a wrong page number is met in public,
mid-chant, by somebody who turned to it because a monk called it out.

The pass ran in thirty batches and these checks ran after every one. They were
written as throwaway scratch scripts, which is what `check_batch` and
`check_render` already record as the mistake worth not repeating: an improvised
checker is re-improvised next session, and the version that gets it wrong looks
exactly like the version that gets it right. So this is written down and tested
like the others.

Three checks, and what each is for
----------------------------------
`shape`   Every chant carries the five commentary keys, of the right types,
          with no empty strings. This is the invariant the pass established —
          305 of 305 — and nothing else stops chant 306 arriving without it.

`script`  No Lao codepoints anywhere in the prose, and every run of Thai in it
          traces back to text already in the file. Both caught real errors.
          Lao ຳ and ຺ are visually identical to Thai ํ and ฺ at reading size
          and two of them got into a Pali citation; three Thai words were typed
          with the wrong character and matched nothing in the book.

`against` Every NON-commentary field of every chant is identical to a given git
          revision. This is the proof that the verses are untouched.

⚠️ The obvious version of the `against` check is wrong
------------------------------------------------------
`git diff | grep '^-'` looks like it answers the question and does not. A large
insertion makes git re-align the hunk, so it reports untouched lines as removed
and re-added elsewhere. That produced a false alarm mid-pass: four data lines
appeared as deletions on a chant nothing had touched. Ten minutes were spent
proving the data was fine.

So this does not read the diff. It IMPORTS both versions of the module and
compares the parsed dicts field by field, with the five commentary keys
stripped. A hunk cannot be misaligned when there are no hunks.
"""
import argparse
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMENTARY_KEYS = ('summary', 'when_chanted', 'source', 'background', 'meaning')

# Lao block. Sits next to Thai in Unicode and renders near-identically at the
# size anybody reads a chant at, which is why it needs a check and not an eye.
LAO = re.compile(r'[຀-໿]')
# A run of Thai script, allowing the spaces inside a quoted phrase.
THAI_RUN = re.compile(r'[฀-๿]+(?:[ ฀-๿]*[฀-๿])?')


def prose(chant):
    """Everything in a chant that this pass WROTE, as one string."""
    parts = [chant.get('summary') or '', chant.get('when_chanted') or '',
             chant.get('source') or '']
    parts += list(chant.get('background') or [])
    parts += list(chant.get('meaning') or [])
    return ' '.join(parts)


def own_text(chant):
    """Everything in a chant the BOOK printed, as one string.

    Thai quoted in the prose should come from the chant being written about.
    Where it legitimately comes from elsewhere — a heading recorded in a CHECK
    comment, a title on a neighbouring page — the file-wide fallback catches
    it, and `script` reports it as traced-elsewhere rather than as an error.
    """
    parts = [chant.get('title_thai') or '', chant.get('source_printed') or '',
             (chant.get('invitation') or {}).get('pali') or '']
    for verse in chant.get('verses') or []:
        parts += [verse.get('pali') or '', verse.get('thai') or '',
                  verse.get('section') or '', verse.get('rubric') or '']
    return ' '.join(parts)


def shape(chants):
    """Problems with the five commentary fields. Empty list means clean."""
    problems = []
    for chant in chants:
        cid = chant.get('id', '<no id>')
        for key in ('summary', 'when_chanted'):
            value = chant.get(key)
            if not isinstance(value, str) or not value.strip():
                problems.append('%s: %s must be a non-empty string' % (cid, key))
        if not isinstance(chant.get('source'), str):
            problems.append('%s: source must be a string, empty if unknown' % cid)
        for key in ('background', 'meaning'):
            value = chant.get(key)
            if not isinstance(value, list) or not value:
                problems.append('%s: %s must be a non-empty list of paragraphs' % (cid, key))
                continue
            for n, para in enumerate(value, 1):
                if not isinstance(para, str) or not para.strip():
                    problems.append('%s: %s paragraph %d is not a non-empty string'
                                    % (cid, key, n))
    return problems


def script(chants, whole_file):
    """Lao codepoints, and Thai in the prose that is nowhere in the file.

    Returns (problems, traced_elsewhere). The second is not an error: it is
    the list of Thai runs quoted from somewhere other than their own chant,
    which is worth being able to see.
    """
    problems, elsewhere = [], []
    for chant in chants:
        cid = chant.get('id', '<no id>')
        written = prose(chant)
        for hit in LAO.finditer(written):
            problems.append('%s: LAO codepoint U+%04X in the prose'
                            % (cid, ord(hit.group(0))))
        mine = own_text(chant)
        for run in {m.group(0).strip() for m in THAI_RUN.finditer(written)}:
            if not run or run in mine:
                continue
            if run in whole_file:
                elsewhere.append((cid, run))
            else:
                problems.append('%s: Thai %r appears nowhere in the file' % (cid, run))
    return problems, elsewhere


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strip_commentary(chants):
    return [{k: v for k, v in c.items() if k not in COMMENTARY_KEYS} for c in chants]


def against(rev, chants):
    """Non-commentary differences between `rev` and the chants given."""
    try:
        blob = subprocess.check_output(['git', 'show', '%s:chanting.py' % rev],
                                       cwd=REPO, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        # A shallow clone — CI's default — has only the newest commit, so the
        # revision to compare against is simply not there. Say that, rather
        # than leaving a git exit code to be read as "the verses changed".
        raise RuntimeError(
            'git cannot show %s:chanting.py — if this is a shallow clone, fetch '
            'the history (fetch-depth: 0 in CI) so the comparison has something '
            'to compare against.\n%s' % (rev, err.output.decode('utf-8', 'replace')))
    handle, path = tempfile.mkstemp(suffix='.py', prefix='chanting_%s_' % re.sub(r'\W', '_', rev))
    os.close(handle)
    try:
        with open(path, 'wb') as out:
            out.write(blob)
        old = strip_commentary(load_module(path, 'chanting_at_rev').CHANTS)
    finally:
        os.unlink(path)

    new = strip_commentary(chants)
    problems = []
    if len(old) != len(new):
        problems.append('chant count changed: %d -> %d' % (len(old), len(new)))
    old_ids = [c.get('id') for c in old]
    new_ids = [c.get('id') for c in new]
    if old_ids != new_ids:
        problems.append('the list of ids changed')
    for before, after in zip(old, new):
        changed = sorted(k for k in set(before) | set(after)
                         if before.get(k) != after.get(k))
        if changed:
            problems.append('%s: %s changed' % (after.get('id'), ', '.join(changed)))
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--against', metavar='REV',
                        help='git revision to prove the verses identical to')
    args = parser.parse_args(argv)

    sys.path.insert(0, REPO)
    import chanting  # noqa: E402  — after sys.path, deliberately

    whole_file = open(os.path.join(REPO, 'chanting.py'), encoding='utf-8').read()
    problems = shape(chanting.CHANTS)
    script_problems, elsewhere = script(chanting.CHANTS, whole_file)
    problems += script_problems
    if args.against:
        problems += against(args.against, chanting.CHANTS)

    done = sum(1 for c in chanting.CHANTS if c.get('summary') and c.get('background'))
    print('%d chants, %d with commentary' % (len(chanting.CHANTS), done))
    print('Thai quoted from elsewhere in the file (not an error): %d' % len(elsewhere))
    if args.against:
        print('compared against %s' % args.against)

    if problems:
        print('\n%d PROBLEM(S):' % len(problems))
        for line in problems:
            print('  ' + line)
        return 1
    print('\nclean')
    return 0


if __name__ == '__main__':
    sys.exit(main())
