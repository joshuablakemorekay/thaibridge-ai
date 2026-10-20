"""
signups_by_source.py — How many new accounts each ad platform brought.

Reads the signup_source / signup_campaign columns written at sign-up (see
signup_source.py) and prints one line per source. Read-only: it changes
nothing.

It uses whatever database the app would use, so with the normal .env it reads
the LIVE database — which is the point, that is where the real sign-ups are.
Prefix DATABASE_URL="" to read the local instance/thai_app.db instead.

USAGE:
  python scripts/signups_by_source.py                       # all time
  python scripts/signups_by_source.py --since 2027-01-04 --until 2027-03-29
  (--until is exclusive: 2027-03-29 includes all of Sunday 28 March)
"""

import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def day(text):
    return datetime.strptime(text, '%Y-%m-%d')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--since', type=day, help='first day to count, YYYY-MM-DD')
    parser.add_argument('--until', type=day, help='day to stop before, YYYY-MM-DD')
    args = parser.parse_args()

    from app import app            # imported late: it connects to the database
    import signup_source

    with app.app_context():
        rows = signup_source.counts(since=args.since, until=args.until)

    total = sum(n for _, _, n in rows)
    print(f"{'Source':<20} {'Campaign':<24} {'Sign-ups':>8}")
    for source, campaign, n in rows:
        print(f"{source or '(no tag)':<20} {campaign or '-':<24} {n:>8}")
    print(f"{'Total':<45} {total:>8}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
