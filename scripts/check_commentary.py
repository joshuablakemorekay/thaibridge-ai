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
import unicodedata

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


# Paiboon+ writes a long diphthong doubled (riian, tuua, rʉ̂ʉa); ThaiBridge
# Spelling writes Paiboon's ia/ua/ʉa for both lengths. The book was converted
# to the app's standard on 2026-10-14, after its baseline was taken.
_LONG_DIPHTHONG = re.compile('([uiʉ])([̀́̂̌]?)\\1([̀́̂̌]?)a')


def shorten_diphthongs(value):
    """The 2026-10-14 spelling change, applied to any string inside `value`."""
    if isinstance(value, str):
        nfd = unicodedata.normalize('NFD', value)
        out = _LONG_DIPHTHONG.sub(lambda m: m.group(1) + (m.group(2) or m.group(3)) + 'a', nfd)
        return value if out == nfd else unicodedata.normalize('NFC', out)
    if isinstance(value, dict):
        return {k: shorten_diphthongs(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(shorten_diphthongs(v) for v in value)
    return value


# 2026-11-06: a final ย after any vowel but a/aa is written y, not i
# (dûai -> dûay, ləəi -> ləəy, nɔ́ɔi -> nɔ́ɔy). ai/aai are untouched. Only a
# word carrying a tone mark or ɛ ɔ ə ʉ ŋ, or a known toneless one, counts as
# romanisation, so English and IAST are never matched.
_TONES = '̀́̂̌'
_WORD = re.compile('[a-zA-ZɛɔəʉŋÀ-ɏḀ-ỿ̀-ͯ]+')
_FINAL_I = re.compile('(u[%s]?a|ʉ[%s]?a|o[%s]?o?|ɔ[%s]?ɔ?|ə[%s]?ə?|u[%s]?)i$' % ((_TONES,) * 6))
_THAIISH = re.compile('[%sɛɔəʉŋ]' % _TONES)
_PLAIN_FINAL_I = {'dooi', 'kui', 'rooi', 'ooi'}


def final_y(value):
    """The 2026-11-06 spelling change, applied to any string inside `value`."""
    if isinstance(value, str):
        def swap(m):
            word = unicodedata.normalize('NFD', m.group(0))
            if _FINAL_I.search(word) and (_THAIISH.search(word) or word.lower() in _PLAIN_FINAL_I):
                return m.group(0)[:-1] + 'y'
            return m.group(0)
        return _WORD.sub(swap, value)
    if isinstance(value, dict):
        return {k: final_y(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(final_y(v) for v in value)
    return value


# Single-word corrections to the book's romanisation, made after the baseline.
# ครีเมขละ: hyphens missing, and ขะ is high class + dead syllable = low tone.
BOOK_CORRECTIONS = [
    ('kriimeekálá', 'krii-mee-kà-lá'),       # 2026-10-14, page 203
]


# Translation lines given ThaiBridge Spelling on 2026-11-06. Their `paiboon`
# was empty in the baseline, left so on purpose until a dedicated pass (see
# the page-306 note in chanting.py). Only `paiboon` on these verses is
# excused; their Thai, Pali and English are still compared. The two
# kham-anumothana-kathin lines stay empty: they are instructions, not
# translations.
SPELLING_ADDED = {
    'atita-paccavekkhana-patha-plae': {*range(2, 7), *range(8, 20), *range(21, 26), *range(27, 30)},
    'buddhabhigiti-plae': {*range(1, 15), *range(16, 20)},
    'buddhanussati-plae': {*range(1, 12)},
    'dhammabhigiti-plae': {*range(1, 15), *range(16, 20)},
    'dhammanussati-plae': {*range(1, 7)},
    'kham-bucha-phra-ratanattaya-yen-plae': {*range(1, 9)},
    'kham-la-sikkha': {1},
    'kham-namatsakan-phra-ratanattaya-yen-plae': {1, 2, 4, 5, 7, 8},
    'kham-samathan-sin': {*range(1, 9)},
    'pubbabhaga-namakara-yen-plae': {*range(1, 4)},
    'sanghabhigiti-plae': {*range(1, 15), *range(16, 20)},
    'sanghanussati-plae': {*range(1, 13)},
    'uddissanadhitthana-gatha-plae': {*range(1, 35)},
}


# Chant headings given a romanised title on 2026-11-06. Their `title_roman`
# was empty in the baseline; 69 copy the book's own contents line (the
# heading must match it) and 10 are new drafts. Only that field is excused.
TITLE_ROMAN_ADDED = {
    'akkappasada-suttagatha',
    'anumothana-withi',
    'atanatiya-parittam-yo',
    'athibai-rabiap-suat-mon-phiset',
    'baep-kammavaca-suat-hai-pha-kathin',
    'baep-suat-kammawaca-nai-upasombotkam-samrap-nak-diao',
    'bhojanadanumothana-gatha',
    'gatha-dap-thian-chai',
    'gatha-jut-thian-chai',
    'kammawaca-upasombot',
    'katha-sarathaphrot',
    'kham-anumothana-kathin',
    'kham-anumothana-kathin-303',
    'kham-anumothana-khong-phra-maha-thera',
    'kham-apalok-kathin-baep-2-rup',
    'kham-apalok-kathin-baep-4-rup',
    'kham-aradhana-sadaeng-tham',
    'kham-aradhana-sadaeng-tham-phisadan',
    'kham-aradhana-sin-5-phiset',
    'kham-aradhana-sin-5-prokati',
    'kham-aradhana-sin-8',
    'kham-aradhana-sin-8-phiset',
    'kham-aradhana-sin-8-prokati',
    'kham-aradhana-suat-phra-paritta',
    'kham-athibai-prakop',
    'kham-athitthan',
    'kham-athitthan-khao-phansa',
    'kham-athitthan-pha-kathin',
    'kham-bangsukun-khon-pen',
    'kham-bangsukun-sop-rue-atthi',
    'kham-bok-anusat',
    'kham-kho-banphacha-nak-khu',
    'kham-kho-buat-chi',
    'kham-kho-khama-thot-dae-phra-maha-thera',
    'kham-kho-khama-thot-phra-ratanatrai',
    'kham-kho-khama-thot-phra-therauthera',
    'kham-kho-nissai-nak-khu',
    'kham-kho-riak-upasampathapekkha-khao-ma',
    'kham-kho-upasombot-phrom-kan',
    'kham-khuen',
    'kham-la-sikkha',
    'kham-namatsakan-phra-phutthachao',
    'kham-pawarana-ok-phansa',
    'kham-phinthu-pha',
    'kham-phra-upatchai-klao-phadiang-song',
    'kham-phra-upatchaiya-klao-phadiang-song',
    'kham-rap-khama-thot-khong-phra-maha-thera',
    'kham-riak-upasampathapekkha-khao-ma',
    'kham-sadaeng-ton-pen-ubasok',
    'kham-samathan-sin',
    'kham-sattaha',
    'kham-sia-sala',
    'kham-sommot-ton-lae-kham-tham-antarayikatham',
    'kham-sommot-ton-phuea-son-som',
    'kham-sommot-ton-phuea-tham-antarayikatham',
    'kham-son-som',
    'kham-suat-kammawaca-upasombot',
    'kham-suat-sommot-lae-kham-son-som',
    'kham-tham-antarayikatham',
    'kham-thon',
    'kham-wikap',
    'kitchawat-10-yang',
    'mongkhon-chakkrawan-noi-yo',
    'rabiap-anumothana',
    'rabiap-bangsukun',
    'rabiap-suat-chet-tamnan-yang-pan-klang',
    'rabiap-suat-chet-tamnan-yang-tem-thi',
    'rabiap-suat-chet-tamnan-yang-yo',
    'rabiap-suat-mon-nai-ngan-phithi-awamongkhon',
    'rabiap-suat-mon-nai-ngan-phithi-mongkhon-uen',
    'rabiap-suat-mon-ngan-phithi-mongkhon',
    'rabiap-suat-mon-noppakhro',
    'rabiap-suat-thawai-phon-phra-kon-chan',
    'rabiap-thawai-phon-phra',
    'tirokuddakanda-pacchimaphak',
    'vipassit-thai',
    'withi-banphacha-upasombot-baep-esaham',
    'withi-banphacha-upasombot-baep-ukasa',
    'withi-sadaeng-abat',
}


def drop_added_spelling(chant):
    """Blank the spelling added after the baseline on one chant dict:
    `paiboon` on the SPELLING_ADDED verses, `title_roman` on TITLE_ROMAN_ADDED."""
    if chant.get('id') in TITLE_ROMAN_ADDED and 'title_roman' in chant:
        chant = dict(chant, title_roman='')
    added = SPELLING_ADDED.get(chant.get('id'))
    if not added or not isinstance(chant.get('verses'), list):
        return chant
    verses = [dict(v, paiboon='') if v.get('number') in added else v
              for v in chant['verses']]
    return dict(chant, verses=verses)


def book_spelling_changes(value):
    """Every deliberate romanisation change since the baseline, applied."""
    value = final_y(shorten_diphthongs(value))
    if isinstance(value, str):
        for old, new in BOOK_CORRECTIONS:
            value = value.replace(unicodedata.normalize('NFC', old),
                                  unicodedata.normalize('NFC', new))
        return value
    if isinstance(value, dict):
        value = drop_added_spelling(value)
        return {k: book_spelling_changes(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(book_spelling_changes(v) for v in value)
    return value


def against(rev, chants, normalise=None):
    """Non-commentary differences between `rev` and the chants given.

    `normalise`, if given, is applied to both sides first, so a deliberate
    book-wide change (a spelling rule) can be carried forward while the
    comparison still catches anything else that moved."""
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
    if normalise:
        old, new = normalise(old), normalise(new)
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
