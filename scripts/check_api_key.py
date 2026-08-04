"""
check_api_key.py — Manual smoke test for the Anthropic API key.

Confirms that ANTHROPIC_API_KEY is present and actually works, by asking the
model for one short Paiboon romanization.

This makes a real (tiny) paid API call, so it is NOT part of the test suite —
it lives in scripts/ and runs only when you ask for it. It used to be named
test_api.py at the repo root, where pytest collected it and fired the call on
every test run.

USAGE:
  python scripts/check_api_key.py

EXIT CODES:
  0 — key is present and working
  1 — key is missing, or the API rejected it
"""

import os
import sys

from dotenv import load_dotenv
import anthropic

MODEL = "claude-haiku-4-5-20251001"
TEST_WORD = "ภิกษุ"


def main() -> int:
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY")

    if not key:
        print("FAIL ANTHROPIC_API_KEY is not set (checked the environment and .env)")
        return 1

    print(f"OK   Key found: {key[:15]}...")

    client = anthropic.Anthropic(api_key=key)
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=50,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Give me ONLY the Paiboon romanization for this Thai "
                        f"word: {TEST_WORD}. Just the romanization, nothing else."
                    ),
                }
            ],
        )
    except anthropic.AuthenticationError:
        print("FAIL The API rejected this key. Check it hasn't been revoked or mistyped.")
        return 1
    except anthropic.APIError as exc:
        # Network blips and rate limits are not key problems — say so, so the
        # reader doesn't go hunting for a bad key that isn't the issue.
        print(f"FAIL API call failed ({type(exc).__name__}): {exc}")
        return 1

    print(f"OK   API responded: {msg.content[0].text.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
