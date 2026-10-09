"""Run the AI tutor's accuracy exam (evals/tutor_accuracy.yaml).

Every case is asked of the real tutor — the same instructions and model the
live site uses — and checked automatically. A report is written to
evals/results/ so runs can be compared over time.

    python scripts/tutor_eval.py                      # the model the site uses
    python scripts/tutor_eval.py --model claude-haiku-5-5
    python scripts/tutor_eval.py --only tone-mai,classifier-tua

This spends real money: a full run on Sonnet 5.5 is about 20 cents. That is
why it is a script you run on purpose, not part of the test suite.
Exit code 0 means every case passed.

It imports ai_agent only, never app: importing app connects to the live
database, and an exam has no business there.
"""
import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

EXAM = ROOT / 'evals' / 'tutor_accuracy.yaml'
RESULTS = ROOT / 'evals' / 'results'

# The reply caps app.py gives each mode (AI_REPLY_TOKENS, AI_REPLY_TOKENS_BY_MODE).
# Copied rather than imported because importing app touches the live database;
# tests/test_tutor_eval.py fails if these two ever drift apart.
REPLY_TOKENS = 800
REPLY_TOKENS_BY_MODE = {'generator': 1500}

THAI = re.compile(r'[฀-๿]')
# A romanisation is the bracket straight after Thai script: ครับ (kráp)
ROMANISATION = re.compile(r'[฀-๿][฀-๿\s\-/]*\**\s*\(([^)]{1,60})\)')
# ThaiBridge Spelling: no h after p, t, k or ch; ŋ not "ng"; ʉ not "ue".
SPELLING_BREAK = re.compile(r'(?<![a-z])(ph|th|kh|chh)|ng|ue', re.I)
# Words that only ever appear in an English aside, never in a romanisation.
# Without this, "(this one, near the speaker)" reads as a broken spelling of th.
ENGLISH_ASIDE = {'the', 'a', 'an', 'this', 'that', 'these', 'those', 'is', 'of',
                 'to', 'for', 'and', 'or', 'with', 'in', 'on', 'it', 'you', 'your',
                 'my', 'near', 'by', 'said', 'means', 'meaning', 'literally',
                 'male', 'female', 'polite', 'formal', 'informal', 'speaker'}


def spelling_breaks(text):
    """Romanisations in `text` that break ThaiBridge Spelling."""
    found = []
    for rom in ROMANISATION.findall(text):
        # A bracket holding Thai, a quote, a comma-separated aside or any
        # English word is a gloss, not a romanisation.
        words = {w.strip('.,;:!?"\'').lower() for w in rom.split()}
        if (THAI.search(rom) or len(words) > 6 or '"' in rom or ',' in rom
                or words & ENGLISH_ASIDE):
            continue
        if SPELLING_BREAK.search(rom):
            found.append(rom)
    return found


def check(case, answer, stop_reason):
    """Every way `answer` fails `case`, as plain-English strings. Empty = pass."""
    text = answer.lower()
    failures = []
    for entry in case.get('must_include', []):
        options = entry if isinstance(entry, list) else [entry]
        if not any(str(o).lower() in text for o in options):
            failures.append('missing: ' + ' / '.join(str(o) for o in options))
    for banned in case.get('must_not_include', []):
        if str(banned).lower() in text:
            failures.append(f'contains: {banned}')
    if case.get('no_thai_script') and THAI.search(answer):
        failures.append('contains Thai script')
    breaks = spelling_breaks(answer)
    if breaks:
        failures.append('spelling rule broken: ' + ', '.join(breaks[:3]))
    if stop_reason == 'max_tokens':
        failures.append('cut off mid-sentence')
    return failures


def load_cases(only=None):
    cases = yaml.safe_load(EXAM.read_text(encoding='utf-8'))['cases']
    if only:
        wanted = set(only)
        cases = [c for c in cases if c['id'] in wanted]
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--model', help='model to test (default: what the site uses)')
    parser.add_argument('--only', help='comma-separated case ids')
    args = parser.parse_args()

    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env')
    if args.model:
        os.environ['AI_MODEL'] = args.model
    import ai_agent

    tutor = ai_agent.ThaiLearningAI()
    cases = load_cases(args.only.split(',') if args.only else None)
    rows = []
    for i, case in enumerate(cases):
        mode = case['mode']
        reply = tutor.chat(session_id=f'eval-{i}', message=case['question'], mode=mode,
                           lens=case.get('lens'),
                           max_tokens=REPLY_TOKENS_BY_MODE.get(mode, REPLY_TOKENS))
        if not reply.get('success'):
            failures = ['request failed: ' + str(reply.get('error') or reply.get('message'))]
            answer = ''
        else:
            answer = reply['response']
            failures = check(case, answer, reply.get('stop_reason'))
        rows.append((case, answer, failures))
        print(f"{'PASS' if not failures else 'FAIL'}  {case['id']:24} {'; '.join(failures)}")

    passed = sum(1 for _, _, f in rows if not f)
    model = tutor.model_for('tutor')
    print(f'\n{passed}/{len(rows)} passed on {model}')
    report = write_report(rows, model, passed)
    print(f'report: {report.relative_to(ROOT)}')
    return 0 if passed == len(rows) else 1


def write_report(rows, model, passed):
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f'{date.today().isoformat()}_{model}.md'
    lines = [f'# Tutor accuracy exam — {model}, {date.today().isoformat()}', '',
             f'**{passed}/{len(rows)} passed.**', '',
             '| Case | Result | Why it failed |', '|---|---|---|']
    for case, _, failures in rows:
        lines.append(f"| `{case['id']}` | {'pass' if not failures else '**fail**'} | "
                     f"{'; '.join(failures).replace('|', '/')} |")
    lines += ['', '## Answers to failed cases', '']
    for case, answer, failures in rows:
        if failures:
            lines += [f"### `{case['id']}`", '', f"**Q:** {case['question']}", '',
                      answer or '_(no answer)_', '']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return path


if __name__ == '__main__':
    sys.exit(main())
