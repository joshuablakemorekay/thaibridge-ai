#!/usr/bin/env python3
"""
eval_runner.py — Run prompt evaluations defined in rubric.yaml files.

For each prompt directory under /prompts:
  1. Load prompt.md and rubric.yaml
  2. For each test_case, run the prompt against an LLM with the input
  3. Evaluate each output against the rubric's pass_condition checks
  4. Write results to /prompts/<name>/results/run_<timestamp>.json
  5. Write a summary report to /prompts/results-summary.md

Pass conditions are Python expressions evaluated against a context containing:
  - output: the raw string returned by the model
  - lines: output.strip().split('\\n')
  - json: the json module
  - re: the re module

Usage:
  python eval_runner.py                       # run all prompts
  python eval_runner.py --prompt extract-foo  # run one prompt
  python eval_runner.py --dry-run             # check rubrics without LLM calls
  python eval_runner.py --provider mock       # use deterministic mock outputs

The runner is provider-agnostic. Set ANTHROPIC_API_KEY for Claude, or use
--provider mock for deterministic local testing (used in CI by default).
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# ----------------------------------------------------------------------------
# Provider abstraction — keeps the runner LLM-agnostic
# ----------------------------------------------------------------------------

class Provider:
    """Base class for LLM providers."""
    def complete(self, prompt: str, inputs: dict) -> str:
        raise NotImplementedError


class MockProvider(Provider):
    """
    Deterministic provider for CI and offline testing.
    Returns canned outputs based on input fingerprint so test runs are
    reproducible without spending API credits.
    """
    def __init__(self, fixtures_dir: Path | None = None):
        self.fixtures_dir = fixtures_dir

    def complete(self, prompt: str, inputs: dict) -> str:
        # Look for a fixture file matching the inputs
        if self.fixtures_dir and self.fixtures_dir.exists():
            fingerprint = self._fingerprint(inputs)
            fixture_path = self.fixtures_dir / f"{fingerprint}.txt"
            if fixture_path.exists():
                return fixture_path.read_text()
        # Fallback: produce something plausibly shaped
        return "MOCK_OUTPUT\nthis is a mock response\nGet started"

    @staticmethod
    def _fingerprint(inputs: dict) -> str:
        s = json.dumps(inputs, sort_keys=True)
        return re.sub(r'\W+', '_', s)[:60]


class AnthropicProvider(Provider):
    """Calls the Anthropic API. Lazy-imported so the runner works without the SDK."""
    def __init__(self, model: str = "claude-sonnet-4-5"):
        try:
            import anthropic  # noqa
        except ImportError:
            raise RuntimeError(
                "anthropic SDK not installed. Run: pip install anthropic"
            )
        self.model = model
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic()  # picks up ANTHROPIC_API_KEY
        return self._client

    def complete(self, prompt: str, inputs: dict) -> str:
        # Render {{variables}} in the prompt
        rendered = render_prompt(prompt, inputs)
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": rendered}],
        )
        return msg.content[0].text


def render_prompt(template: str, inputs: dict) -> str:
    """Replace {{key}} placeholders with values from inputs."""
    def replace(match):
        key = match.group(1).strip()
        if key in inputs:
            return str(inputs[key])
        return match.group(0)  # leave unfilled
    return re.sub(r'\{\{(\w+)\}\}', replace, template)


# ----------------------------------------------------------------------------
# Rubric evaluation
# ----------------------------------------------------------------------------

def evaluate_criterion(criterion: dict, output: str) -> dict:
    """
    Evaluate a single rubric criterion against an output.
    Returns {'name', 'passed', 'weight', 'error'}.
    """
    name = criterion.get('name', 'unnamed')
    weight = criterion.get('weight', 1)
    pass_condition = criterion.get('pass_condition', '')

    if not pass_condition:
        return {'name': name, 'passed': None, 'weight': weight,
                'error': 'no pass_condition defined'}

    # Build a restricted evaluation context
    lines = output.strip().split('\n') if output else []
    context = {
        'output': output,
        'lines': lines,
        'json': json,
        're': re,
        'len': len,
        'any': any,
        'all': all,
        'str': str,
        'int': int,
        'float': float,
        'type': type,
    }

    # Pass context as globals (not locals) so generator expressions and
    # comprehensions can resolve names through the enclosing scope.
    safe_globals = {"__builtins__": {}, **context}
    try:
        result = eval(pass_condition, safe_globals)
        return {'name': name, 'passed': bool(result), 'weight': weight,
                'error': None}
    except Exception as e:
        return {'name': name, 'passed': False, 'weight': weight,
                'error': f'{type(e).__name__}: {e}'}


def evaluate_output(rubric: dict, output: str) -> dict:
    """Run all criteria in a rubric against an output. Returns aggregate result."""
    criteria = rubric.get('criteria', [])
    criterion_results = [evaluate_criterion(c, output) for c in criteria]

    total_weight = sum(c['weight'] for c in criterion_results
                       if c['passed'] is not None)
    earned_weight = sum(c['weight'] for c in criterion_results
                        if c['passed'] is True)

    score = (earned_weight / total_weight) if total_weight > 0 else 0.0
    passed = all(c['passed'] for c in criterion_results
                 if c['passed'] is not None)

    return {
        'score': round(score, 3),
        'passed': passed,
        'criteria': criterion_results,
    }


# ----------------------------------------------------------------------------
# Prompt directory loading
# ----------------------------------------------------------------------------

def extract_prompt_text(prompt_md: str) -> str:
    """
    Pull the prompt body out of the ``` fenced block in prompt.md.
    Falls back to the whole file if no fenced block is found.
    """
    match = re.search(r'```\n(.*?)\n```', prompt_md, re.DOTALL)
    if match:
        return match.group(1).strip()
    return prompt_md.strip()


def load_prompt_dir(prompt_dir: Path) -> dict | None:
    """Load prompt.md and rubric.yaml from a directory. Returns None if invalid."""
    prompt_file = prompt_dir / 'prompt.md'
    rubric_file = prompt_dir / 'rubric.yaml'

    if not prompt_file.exists() or not rubric_file.exists():
        return None

    prompt_text = extract_prompt_text(prompt_file.read_text())
    rubric = yaml.safe_load(rubric_file.read_text())

    return {
        'name': prompt_dir.name,
        'dir': prompt_dir,
        'prompt': prompt_text,
        'rubric': rubric,
    }


# ----------------------------------------------------------------------------
# Main runner
# ----------------------------------------------------------------------------

def run_prompt(prompt_data: dict, provider: Provider, dry_run: bool = False) -> dict:
    """Run all test cases for one prompt and evaluate outputs."""
    rubric = prompt_data['rubric']
    test_cases = rubric.get('test_cases', [])

    case_results = []
    for i, case in enumerate(test_cases):
        inputs = case.get('input', {})
        if isinstance(inputs, str):
            inputs = {'input': inputs}

        if dry_run:
            output = ''
            eval_result = {'score': None, 'passed': None, 'criteria': []}
        else:
            try:
                output = provider.complete(prompt_data['prompt'], inputs)
                eval_result = evaluate_output(rubric, output)
            except Exception as e:
                output = ''
                eval_result = {
                    'score': 0.0,
                    'passed': False,
                    'criteria': [],
                    'error': f'provider error: {e}',
                }

        case_results.append({
            'case_index': i,
            'inputs': inputs,
            'output': output,
            **eval_result,
        })

    scores = [c['score'] for c in case_results if c['score'] is not None]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    all_passed = all(c['passed'] for c in case_results
                     if c['passed'] is not None) if case_results else False

    return {
        'prompt': prompt_data['name'],
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'cases_run': len(case_results),
        'avg_score': round(avg_score, 3),
        'all_passed': all_passed,
        'cases': case_results,
    }


def write_summary(results: list[dict], output_path: Path) -> None:
    """Write a markdown summary across all prompts."""
    lines = [
        '# Eval Results Summary',
        '',
        f'_Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}_',
        '',
        '| Prompt | Cases | Avg Score | Status |',
        '|---|---|---|---|',
    ]
    for r in results:
        status = '✅ pass' if r['all_passed'] else '❌ fail'
        lines.append(
            f'| `{r["prompt"]}` | {r["cases_run"]} | '
            f'{r["avg_score"]:.1%} | {status} |'
        )

    overall_pass = all(r['all_passed'] for r in results)
    lines += ['', f'**Overall:** {"✅ all prompts passing" if overall_pass else "❌ failures present"}']
    output_path.write_text('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description='Run prompt evaluations')
    parser.add_argument('--prompts-dir', default='prompts',
                        help='Path to /prompts folder (default: ./prompts)')
    parser.add_argument('--prompt', help='Run only one named prompt')
    parser.add_argument('--provider', default='mock',
                        choices=['mock', 'anthropic'],
                        help='LLM provider to use')
    parser.add_argument('--model', default='claude-sonnet-4-5')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate rubrics without calling the LLM')
    parser.add_argument('--fail-under', type=float, default=None,
                        help='Exit nonzero if avg score below this (e.g. 0.8)')
    args = parser.parse_args()

    prompts_dir = Path(args.prompts_dir)
    if not prompts_dir.exists():
        print(f'ERROR: {prompts_dir} does not exist', file=sys.stderr)
        sys.exit(2)

    # Pick provider
    if args.provider == 'anthropic':
        provider = AnthropicProvider(model=args.model)
    else:
        # Look for fixtures next to the prompts (used in CI)
        provider = MockProvider(fixtures_dir=prompts_dir / '.fixtures')

    # Collect prompt directories
    prompt_dirs = sorted([d for d in prompts_dir.iterdir() if d.is_dir()
                          and not d.name.startswith('.')])

    if args.prompt:
        prompt_dirs = [d for d in prompt_dirs if d.name == args.prompt]
        if not prompt_dirs:
            print(f'ERROR: no prompt directory named "{args.prompt}"',
                  file=sys.stderr)
            sys.exit(2)

    # Run each prompt
    all_results = []
    for pdir in prompt_dirs:
        prompt_data = load_prompt_dir(pdir)
        if not prompt_data:
            print(f'WARN: {pdir.name} missing prompt.md or rubric.yaml, skipping')
            continue

        print(f'Running {prompt_data["name"]}... ', end='', flush=True)
        result = run_prompt(prompt_data, provider, dry_run=args.dry_run)
        all_results.append(result)

        # Persist per-prompt result
        results_dir = pdir / 'results'
        results_dir.mkdir(exist_ok=True)
        ts = result['timestamp'].replace(':', '-').split('.')[0]
        out_file = results_dir / f'run_{ts}.json'
        out_file.write_text(json.dumps(result, indent=2))

        status = '✓' if result['all_passed'] else '✗'
        print(f'{status} {result["avg_score"]:.1%}  ({result["cases_run"]} cases)')

    if not all_results:
        print('No prompts found.', file=sys.stderr)
        sys.exit(2)

    # Write top-level summary
    summary_path = prompts_dir / 'results-summary.md'
    write_summary(all_results, summary_path)
    print(f'\nSummary written to {summary_path}')

    # Optional fail-under threshold
    if args.fail_under is not None:
        overall_avg = sum(r['avg_score'] for r in all_results) / len(all_results)
        if overall_avg < args.fail_under:
            print(f'\n✗ Overall avg {overall_avg:.1%} below threshold '
                  f'{args.fail_under:.1%}', file=sys.stderr)
            sys.exit(1)

    # Default: nonzero exit if any prompt failed
    if not all(r['all_passed'] for r in all_results):
        sys.exit(1)


if __name__ == '__main__':
    main()
