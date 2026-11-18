"""
ltv_report.py — Lifetime value (LTV): how much each ad source's learners have paid,
and whether they're still here.

The ZenBrew lesson: an ad can bring in lots of sign-ups (high ROAS) whose
learners pay once and leave (low LTV). This report judges each source by the
money its learners have paid over time, not by sign-ups alone.

For each signup_source / signup_campaign it prints:
  Sign-ups     accounts created
  Payers       accounts with at least one payment (plan, renewal or pass)
  Paying now   accounts whose paid plan is still running today
  Revenue      everything those accounts have paid, in £ (dāna gifts left out:
               a gift isn't a purchase)
  LTV/sign-up  revenue / sign-ups — what one sign-up from this source is worth
  LTV/payer    revenue / payers — what one paying learner is worth
  Level 3      how many reached Level 3 (only counted since 2026-11-18)
  Active 30d   how many used the site in the last 30 days (since 2026-11-18)

Then the cancellation reasons people gave, and monthly vs annual payments.

Read-only: it changes nothing. It uses whatever database the app would use,
so with the normal .env it reads the LIVE database — which is the point, that
is where the real learners are. Prefix DATABASE_URL="" to read the local
instance/thai_app.db instead.

USAGE:
  python scripts/ltv_report.py                       # everyone
  python scripts/ltv_report.py --since 2027-01-04    # only accounts created from then
"""

import argparse
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ACTIVE_DAYS = 30
PAID_KINDS = ('subscription', 'renewal', 'addon')   # 'dana' is a gift, not a sale


def day(text):
    return datetime.strptime(text, '%Y-%m-%d')


def build_report(User, Payment, since=None, until=None, today=None):
    """Work the numbers out. Returns a dict, so tests can check it without printing.

    Only pounds are added up. PayPal can settle in other currencies, and adding
    dollars to pounds would give a wrong total, so those payments are counted
    in 'other_currency' instead.
    """
    today = today or date.today()
    active_since = today - timedelta(days=ACTIVE_DAYS)

    users = User.query
    if since is not None:
        users = users.filter(User.created_at >= since)
    if until is not None:
        users = users.filter(User.created_at < until)
    users = users.all()
    ids = [u.id for u in users]

    paid_pence = defaultdict(int)
    payers = set()
    periods = Counter()
    other_currency = 0
    if ids:
        for p in Payment.query.filter(Payment.user_id.in_(ids),
                                      Payment.kind.in_(PAID_KINDS)).all():
            payers.add(p.user_id)
            if p.kind in ('subscription', 'renewal'):
                periods[p.billing_period or 'unknown'] += 1
            if p.amount_pence is None:
                continue
            if (p.currency or 'gbp') == 'gbp':
                paid_pence[p.user_id] += p.amount_pence
            else:
                other_currency += 1

    groups = defaultdict(lambda: {'signups': 0, 'payers': 0, 'paying_now': 0,
                                  'revenue_pence': 0, 'level3': 0, 'active': 0})
    reasons = Counter()
    for u in users:
        g = groups[(u.signup_source, u.signup_campaign)]
        g['signups'] += 1
        g['payers'] += u.id in payers
        g['paying_now'] += u.effective_tier != 'free'
        g['revenue_pence'] += paid_pence[u.id]
        g['level3'] += u.level3_reached_at is not None
        g['active'] += bool(u.last_active_on and u.last_active_on >= active_since)
        if u.cancel_reason:
            reasons[u.cancel_reason] += 1

    rows = []
    for (source, campaign), g in groups.items():
        g = dict(g, source=source, campaign=campaign)
        g['ltv_signup_pence'] = g['revenue_pence'] // g['signups']
        g['ltv_payer_pence'] = g['revenue_pence'] // g['payers'] if g['payers'] else 0
        rows.append(g)
    rows.sort(key=lambda r: (-r['revenue_pence'], -r['signups'],
                             r['source'] or '', r['campaign'] or ''))
    return {'rows': rows, 'reasons': reasons, 'periods': periods,
            'other_currency': other_currency}


def pounds(pence):
    return f"£{pence / 100:,.2f}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--since', type=day, help='first sign-up day to include, YYYY-MM-DD')
    parser.add_argument('--until', type=day, help='sign-up day to stop before, YYYY-MM-DD')
    args = parser.parse_args()

    from app import app, Payment   # imported late: it connects to the database
    from models import User
    from activity import CANCEL_REASONS

    with app.app_context():
        report = build_report(User, Payment, since=args.since, until=args.until)

    head = (f"{'Source':<14} {'Campaign':<16} {'Sign-ups':>8} {'Payers':>7} "
            f"{'Paying now':>10} {'Revenue':>10} {'LTV/sign-up':>11} {'LTV/payer':>10} "
            f"{'Level 3':>7} {'Active 30d':>10}")
    print(head)
    print('-' * len(head))
    total = Counter()
    for r in report['rows']:
        print(f"{(r['source'] or '(no tag)')[:14]:<14} {(r['campaign'] or '-')[:16]:<16} "
              f"{r['signups']:>8} {r['payers']:>7} {r['paying_now']:>10} "
              f"{pounds(r['revenue_pence']):>10} {pounds(r['ltv_signup_pence']):>11} "
              f"{pounds(r['ltv_payer_pence']):>10} {r['level3']:>7} {r['active']:>10}")
        for k in ('signups', 'payers', 'paying_now', 'revenue_pence', 'level3', 'active'):
            total[k] += r[k]
    print('-' * len(head))
    ltv_signup = total['revenue_pence'] // total['signups'] if total['signups'] else 0
    ltv_payer = total['revenue_pence'] // total['payers'] if total['payers'] else 0
    print(f"{'Total':<31} {total['signups']:>8} {total['payers']:>7} {total['paying_now']:>10} "
          f"{pounds(total['revenue_pence']):>10} {pounds(ltv_signup):>11} "
          f"{pounds(ltv_payer):>10} {total['level3']:>7} {total['active']:>10}")

    print('\nWhy people cancelled (from the goodbye page):')
    if report['reasons']:
        for key, n in report['reasons'].most_common():
            print(f"  {n:>4}  {CANCEL_REASONS.get(key, key)}")
    else:
        print('  No answers yet.')

    print('\nPlan payments by billing period:')
    for period in ('month', 'year', 'unknown'):
        if report['periods'][period]:
            label = {'month': 'Monthly', 'year': 'Annual',
                     'unknown': 'Not recorded (before 2026-11-18, or PayPal)'}[period]
            print(f"  {report['periods'][period]:>4}  {label}")
    if not report['periods']:
        print('  None yet.')

    if report['other_currency']:
        print(f"\nNote: {report['other_currency']} payment(s) in another currency "
              f"are left out of the £ totals.")
    print("\nLevel 3 and Active 30d only count from 2026-11-18, when they started being recorded.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
