"""The shared database object and the account model.

db is created here, unbound, and app.py attaches it to the Flask app with
db.init_app(app). Keeping it out of app.py is what lets auth.py use User and
db without importing app.py — the same one-way rule as every other module:
app.py imports them, they never import app.py.

Only User moved. AiUsage and Payment stay in app.py for now, because Payment
reads the price lists that live there.
"""

import logging
from datetime import datetime, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

log = logging.getLogger(__name__)

db = SQLAlchemy()


# ============================================
# TIME
# ============================================

def utcnow():
    """UTC, naive — the shape every db.DateTime column in this file stores.

    datetime.utcnow() is deprecated, but its recommended replacement
    datetime.now(timezone.utc) returns an *aware* datetime, and none of the
    columns here are timezone-aware. Comparing an aware value against a naive
    one raises TypeError, so a straight swap would turn a warning into a crash
    on the subscription-expiry check below.

    The tzinfo is therefore dropped on purpose, in one place, rather than
    accidentally in several. Use this everywhere instead of datetime.utcnow();
    if the columns are ever migrated to timezone=True, this is the only line
    that has to change. Pinned by tests/test_utcnow_contract.py.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ============================================
# USER MODEL
# ============================================

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(20),  unique=True, nullable=False)
    email         = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=utcnow, nullable=False)

    # --- Subscription / billing (the database is the source of truth) ---
    # These are written by the Stripe webhook (Phase 3), NOT by the browser.
    subscription_tier      = db.Column(db.String(20), default='free', nullable=False)   # 'free' | 'basic' | 'pro'
    subscription_status    = db.Column(db.String(20), default='inactive', nullable=False)  # Stripe status, e.g. 'active', 'canceled', 'past_due'
    stripe_customer_id     = db.Column(db.String(64), index=True)   # 'cus_...' — links this user to Stripe
    stripe_subscription_id = db.Column(db.String(64), index=True)   # 'sub_...' — the active subscription, if any
    current_period_end     = db.Column(db.DateTime)                 # when the paid period runs out (renewal/expiry)
    full_unlock            = db.Column(db.Boolean, default=False, nullable=False)  # one-time "Instant Access Pass" add-on: skips the level gates
    # The one Thai Reader section this learner opened by levelling rather than
    # paying (see EARNED_UNLOCK_LEVEL). A column, not a progress key, for the
    # same reason as the flags above: it is an entitlement, so the browser must
    # not be able to hand itself one by editing a cookie.
    earned_unlock_section  = db.Column(db.String(50))

    # --- Alphabet gate ---
    # The alphabet is the prerequisite for every other content section, so
    # "have they passed it?" cannot live in the session cookie alone: clearing
    # cookies or opening the site on a second device would re-lock the whole
    # site for someone who has already earned their way in. The database is the
    # source of truth for logged-in users; the session is only a cache of it.
    alphabet_completed     = db.Column(db.Boolean, default=False, nullable=False)
    alphabet_completed_at  = db.Column(db.DateTime)

    # --- Learning progress ---
    # XP, level, streak, achievements and the rest of session['user_progress'],
    # kept here so a learner does not lose their level by clearing cookies or
    # picking up their phone. Same reasoning as the alphabet gate above: the
    # session stays the working copy, this is the durable one.
    #
    # One JSON column rather than twenty-odd real ones because none of it is
    # queried or reported on — it is only ever read back whole for one user. A
    # column per field would mean a schema change every time a new counter is
    # added. JSONB on Postgres, JSON-in-TEXT on SQLite; SQLAlchemy handles both.
    progress               = db.Column(db.JSON)

    # --- Signing out everywhere ---
    # Part of the id Flask-Login puts in the session and remember-me cookies
    # (see get_id). A new password bumps it, so every cookie issued before the
    # change stops matching and that device is signed out — including whoever
    # had the account if it was taken over, which is the point of changing it.
    session_version        = db.Column(db.Integer, default=0, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        # Here rather than in each route, so no route that sets a password can
        # forget to sign the old sessions out.
        self.session_version = (self.session_version or 0) + 1

    def get_id(self):
        return f"{self.id}:{self.session_version or 0}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def effective_tier(self):
        """The tier this user should actually get RIGHT NOW.

        A paid tier only counts while the subscription is active and the paid
        period hasn't run out — otherwise they fall back to 'free'. This is the
        single rule Phase 4 will use to gate access, so it lives on the model.
        """
        if self.subscription_tier == 'free':
            return 'free'
        # 'canceling' = cancelled, but the period already paid for has not run
        # out yet. They keep what they paid for; current_period_end ends it.
        if self.subscription_status not in ('active', 'trialing', 'canceling'):
            return 'free'
        if self.current_period_end is not None and self.current_period_end < utcnow():
            return 'free'
        return self.subscription_tier


def ensure_user_columns():
    """create_all() adds new TABLES but never new COLUMNS to a table that already
    exists, so add any missing ones by hand. Idempotent — each ALTER is skipped
    once its column is present — so this keeps an older database (local or live)
    in step with the current User model.

    The column types are picked per dialect because this is raw DDL, and raw DDL
    is not portable: Postgres has no DATETIME type (it is TIMESTAMP), and a
    Postgres boolean rejects a DEFAULT of 0 (it must be FALSE). SQLite is happy
    with either spelling, so the Postgres-correct choice is the safe one to make
    conditional rather than the other way round."""
    from sqlalchemy import inspect, text
    is_pg = db.engine.dialect.name == 'postgresql'
    dt    = 'TIMESTAMP' if is_pg else 'DATETIME'
    false = 'FALSE'     if is_pg else '0'
    json_ = 'JSONB'     if is_pg else 'TEXT'
    wanted = {
        'subscription_tier':      "VARCHAR(20) NOT NULL DEFAULT 'free'",
        'subscription_status':    "VARCHAR(20) NOT NULL DEFAULT 'inactive'",
        'stripe_customer_id':     "VARCHAR(64)",
        'stripe_subscription_id': "VARCHAR(64)",
        'current_period_end':     dt,
        'full_unlock':            f"BOOLEAN NOT NULL DEFAULT {false}",
        'earned_unlock_section':  "VARCHAR(50)",
        'alphabet_completed':     f"BOOLEAN NOT NULL DEFAULT {false}",
        'alphabet_completed_at':  dt,
        'progress':               json_,
        'session_version':        "INTEGER NOT NULL DEFAULT 0",
    }
    _ensure_columns('users', wanted)
    _ensure_columns('ai_usage', {'cache_write_tokens': 'INTEGER',
                                 'cache_read_tokens': 'INTEGER'})


def _ensure_columns(table_name, wanted):
    """Add any missing columns to an existing table. Idempotent.

    Split out from the users-specific version so a second table costs one small
    function rather than a copy of this loop. Adding a nullable column is instant
    on Postgres, and rows written before it existed simply read NULL — which is
    the honest answer: we were not recording that yet.
    """
    from sqlalchemy import inspect, text
    existing = {c['name'] for c in inspect(db.engine).get_columns(table_name)}
    added = False
    for name, ddl in wanted.items():
        if name not in existing:
            db.session.execute(
                text(f'ALTER TABLE {table_name} ADD COLUMN {name} {ddl}'))
            log.info('Migrated: added %s.%s column', table_name, name)
            added = True
    if added:
        db.session.commit()
