# Testing Guide

How ThaiBridge AI is tested: how to run the suite, how it's organised, how it stays away
from the live database, and the habits that keep a green tick meaningful.

*Last checked: 13 November 2026, 73 test files, 2,828 tests passing (3 skipped).*

---

## Running the tests

```
pip install -r requirements-dev.txt
python -m pytest -q
```

That's all you need. You don't have to set any environment variables first, because
`tests/conftest.py` sets up a safe environment itself (see the next section). A full run
takes about 40 seconds.

Useful variations:

```
python -m pytest tests/test_app_reviews.py -v     # one file, test by test
python -m pytest -k "paywall or gate"             # tests whose names match
python -m pytest -x                               # stop at the first failure
```

**Tests that need Node.js** (`test_pronounce_core.py`, `test_trace_check.py`,
`test_js_syntax.py`) run JavaScript, or check that it parses. Without Node they skip
rather than fail. GitHub's test machines have Node, so CI always runs them.

**The 3 skipped tests** are deliberate. Two in `test_contents_roman.py` cover chant titles
whose spelling is romanised by hand (it doesn't follow the Pali rules the test checks), and
one in `test_thai_romanisation.py` is a check with nothing to check yet (an empty list).

---

## How the suite stays off the live database

This matters more than anything else in this guide.

`app.py` loads `.env` when it's imported. On a developer's machine `.env` can hold the
**live** Postgres connection string. A test suite pointed at the live database passes
just as happily as one pointed at a local file, while quietly writing test accounts into
real data. That really happened here once, and nothing failed.

So `tests/conftest.py`, which pytest always loads first, does two things before the app
is imported:

- **`DATABASE_URL` is set to an empty string, not deleted.** `python-dotenv` won't
  overwrite a variable that already exists, even an empty one. If it were deleted,
  dotenv would quietly load the real one back. The app treats empty as "not configured"
  and uses the local SQLite file `instance/thai_app.db`.
- **`DISABLE_RATE_LIMITS=1`** turns off rate limiting. The tests hit the same routes
  hundreds of times in seconds, which is exactly what the limits exist to block.

**For anything that isn't pytest**, like a one-off script that does `import app`, prefix it
yourself:

```
DATABASE_URL="" python my_script.py
```

---

## Automatic runs (CI)

Two GitHub Actions workflows run in `.github/workflows/`:

- **`tests.yml`** runs the whole suite on every push to `main` and every pull request, on
  Python 3.12.8 (the version Render uses). It uses placeholder keys that could never be
  mistaken for real ones, and **no** Stripe, PayPal or database credentials, so a test
  that secretly depends on a real service fails here. It fetches the full git history,
  because one chanting test compares today's verses against an older version.
- **`prompt-eval.yml`** checks the archived prompts in `prompts/` against their rubrics
  whenever a prompt changes.

The badge at the top of the README shows the latest result.

---

## How the tests are organised

One file per feature, named after it. Broadly:

| Area | Examples | What they protect |
|---|---|---|
| **Access & paywall** | `test_section_gates.py`, `test_exercise_locks.py`, `test_earned_unlock.py`, `test_dhamma_open_to_all.py` | The right people see the right pages; nobody unlocks paid content by editing a cookie |
| **Accounts & security** | `test_password_reset.py`, `test_developer_mode.py`, `test_progress_and_limits.py`, `test_domain_redirect.py` | Reset links, signing out other devices, developer mode switched off without a password, rate limits keyed on the real visitor |
| **Payments** | `test_payments.py`, `test_billing_period.py`, `test_payment_mode.py`, `test_dana.py`, `test_vat_display.py` | Every way money moves leaves exactly one record; duplicates from Stripe are ignored; cancellations end at the right time |
| **XP & progress** | `test_calculator.py`, `test_drill_cap.py`, `test_learning_path.py` | Level maths, the daily drill cap, signed answers, the learning path |
| **AI tutor** | `test_ai_usage.py`, `test_ai_streaming.py`, `test_translator_mode.py`, `test_spelling_tool.py`, `test_tutor_eval.py` | Usage logging (never the message text), allowances, streaming, the spelling tool, the accuracy exam's format |
| **Thai accuracy** | `test_thai_romanisation.py`, `test_registers.py`, `test_thai_tones.py`, `test_spelling_snapshot.py` | The ThaiBridge Spelling rules across every Thai string in the app |
| **Chanting book** | `test_chanting_*.py`, `test_check_pages.py`, `test_check_batch.py`, `test_apply_batch.py` | Verified verses never change; pages show exactly what the printed book shows |
| **Pages & content** | `test_survival.py`, `test_expat2000.py`, `test_tour_trips.py`, `test_site_search.py`, `test_curriculum.py` | Each page renders and its content is complete |
| **Security headers & scripts** | `test_security_headers.py`, `test_js_syntax.py`, `test_cookie_and_monk_limits.py`, `test_json_only.py` | Headers on every response; no inline scripts or handlers creep back in; every script file parses; every POST route refuses a plain form |
| **Accessibility** | `test_colour_blind_mode.py`, `test_css_variables.py` | Contrast at 4.5:1 or better; nothing relies on colour alone |
| **Reviews** | `test_app_reviews.py` | Who's asked, what's saved, and that the private list stays private |

### Shared helpers in `conftest.py`

- **`make_client(**overrides)`** builds a test browser for a learner described by the
  overrides. For example, `make_client(subscription_tier="basic", is_developer=False)`
  builds a paying Basic learner without developer powers.
- **`unlocked_client`** is everything open, for tests that only need to get past the gates.

Use the narrowest learner you can. A test about what a Basic subscriber sees must not run
as a developer with everything unlocked, or it proves nothing.

To test as a **signed-in account**, create a real `User` row in a fixture, put
`"<id>:<session_version>"` into the session's `_user_id`, and delete the row afterwards.
`tests/test_app_reviews.py` shows the pattern.

---

## Habits that keep the tests honest

These all come from real mistakes, written up in the README's "Results & evidence".

1. **Watch a new test fail before trusting it.** Break the code on purpose (or put the
   bug back), check the test goes red, then restore it. A test you've only seen pass
   hasn't been tested.
2. **Test the thing the code actually reads**, not something next to it. Asserting a
   setting instead of the limiter it configures, or a constant instead of the function
   that builds it, can pass for the wrong reason.
3. **Check the old thing is gone, not just that the new thing is there.** When replacing
   wording or a feature, assert the old version is absent too.
4. **Pin promises the app makes.** If the copy or a rule matters (a free section, a
   price, a tradition named on the home page), give it a test, so removing it by
   accident turns the suite red.
5. **Keep tests independent of the machine.** Never read real keys or the live
   environment. Set what a test needs inside the test.
6. **Clean up what you create.** Fixtures that add database rows delete them afterwards,
   so tests can run in any order.

---

## Beyond pytest

- **The AI tutor's accuracy exam:** `scripts/tutor_eval.py` asks the real tutor the
  questions in `evals/tutor_accuracy.yaml` and checks the answers. It makes paid API
  calls, so it isn't part of the normal suite. Run it after changing the tutor's prompts
  or model.
- **Chanting data checkers:** `scripts/check_pages.py`, `check_batch.py` and
  `check_commentary.py` check the chanting book against its page map before anything is
  written.
- **Checking it in a real browser:** run the app locally (see
  [ARCHITECTURE.md](./ARCHITECTURE.md#how-to-run-it)) and use the page as a learner would.
  The tests prove the HTML is right, but only a browser shows whether it *looks* right.
