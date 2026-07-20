"""
Thai Language & Culture Learning Web Application
================================================
A Flask-based web app for learning Thai through cultural immersion.
Features: Paiboon romanization, interactive quizzes, cultural context,
Theravada Buddhism teachings, meditation timer, grammar lessons, and more.

Version 3.0 - AI Agent Edition
"""

import os
import sys
import json
import glob

import monk_audio  # shared MP3 filename rules, also used by the build script

# On Windows the default console encoding (cp1252) can't print the emoji/Thai
# characters in our startup messages, which crashes the app on launch. Force
# UTF-8 output so those print() calls work everywhere.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv()  # Load .env file before anything else reads environment variables
# Set API key BEFORE any other imports

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import random
import re
from datetime import datetime, timedelta

app = Flask(__name__)

api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set. Check your environment variable.")

import os

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY is not set. Please set it in your environment.")

# ============================================
# STRIPE PAYMENTS (test / sandbox mode)
# ============================================
# All keys come from environment variables (.env locally — never committed).
# Use TEST keys only (sk_test_... / pk_test_...) so no real money ever moves.
# If STRIPE_SECRET_KEY isn't set, the paid-subscription buttons show a friendly
# "not configured yet" message instead of crashing the app.
import stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# ============================================
# PAYPAL PAYMENTS (sandbox mode)
# ============================================
# PayPal is offered as a second payment option. We talk to PayPal's REST API
# directly with httpx (which already ships with the Anthropic SDK), so there's
# no extra SDK to learn. Use SANDBOX credentials from
# https://developer.paypal.com/dashboard/applications/sandbox — keep PAYPAL_MODE
# as 'sandbox' until you're ready to take real money.
import httpx

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET", "")
PAYPAL_MODE = os.environ.get("PAYPAL_MODE", "sandbox")
PAYPAL_API_BASE = (
    "https://api-m.paypal.com" if PAYPAL_MODE == "live"
    else "https://api-m.sandbox.paypal.com"
)


def paypal_configured():
    """True only if both PayPal credentials are present."""
    return bool(PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET)


def _paypal_access_token():
    """Exchange the client id/secret for a short-lived access token."""
    resp = httpx.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

# ============================================
# DATABASE CONFIGURATION
# ============================================

# The database lives in an 'instance' folder next to this file. SQLite can
# create the .db file, but NOT the folder it sits in — so we make sure the
# folder exists first. Without this, running from a fresh copy of the project
# fails with "unable to open database file".
db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(db_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    db_dir, 'thai_app.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ============================================
# USER MODEL
# ============================================

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(20),  unique=True, nullable=False)
    email         = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # --- Subscription / billing (the database is the source of truth) ---
    # These are written by the Stripe webhook (Phase 3), NOT by the browser.
    subscription_tier      = db.Column(db.String(20), default='free', nullable=False)   # 'free' | 'basic' | 'pro'
    subscription_status    = db.Column(db.String(20), default='inactive', nullable=False)  # Stripe status, e.g. 'active', 'canceled', 'past_due'
    stripe_customer_id     = db.Column(db.String(64), index=True)   # 'cus_...' — links this user to Stripe
    stripe_subscription_id = db.Column(db.String(64), index=True)   # 'sub_...' — the active subscription, if any
    current_period_end     = db.Column(db.DateTime)                 # when the paid period runs out (renewal/expiry)
    full_unlock            = db.Column(db.Boolean, default=False, nullable=False)  # one-time "Instant Access Pass" add-on: skips the level/alphabet gates

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

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
        if self.subscription_status not in ('active', 'trialing'):
            return 'free'
        if self.current_period_end is not None and self.current_period_end < datetime.utcnow():
            return 'free'
        return self.subscription_tier

def _ensure_user_columns():
    """create_all() adds new TABLES but never new COLUMNS to a table that already
    exists, so add any missing ones by hand. Idempotent — each ALTER is skipped
    once its column is present — so this keeps an older database (local or live)
    in step with the current User model."""
    from sqlalchemy import inspect, text
    wanted = {
        'subscription_tier':      "VARCHAR(20) NOT NULL DEFAULT 'free'",
        'subscription_status':    "VARCHAR(20) NOT NULL DEFAULT 'inactive'",
        'stripe_customer_id':     "VARCHAR(64)",
        'stripe_subscription_id': "VARCHAR(64)",
        'current_period_end':     "DATETIME",
        'full_unlock':            "BOOLEAN NOT NULL DEFAULT 0",
    }
    existing = {c['name'] for c in inspect(db.engine).get_columns('users')}
    added = False
    for name, ddl in wanted.items():
        if name not in existing:
            db.session.execute(text(f'ALTER TABLE users ADD COLUMN {name} {ddl}'))
            app.logger.info('Migrated: added users.%s column', name)
            added = True
    if added:
        db.session.commit()

with app.app_context():
    db.create_all()
    _ensure_user_columns()

# ============================================
# LOGIN MANAGER (Flask-Login)
# ============================================
# Flask-Login keeps track of "who is logged in" across requests. It stores only
# the user's id in the (signed) session cookie, then uses the loader below to
# fetch the full User from the database on each request.
login_manager = LoginManager(app)
login_manager.login_view = 'login'          # where @login_required sends guests
login_manager.login_message = "Please log in to continue."

@login_manager.user_loader
def load_user(user_id):
    """Given the id stored in the session, return the matching User (or None)."""
    return db.session.get(User, int(user_id))

# ============================================
# AI AGENT INTEGRATION
# ============================================
try:
    from ai_agent import get_ai_agent
    ai_agent = get_ai_agent()
    print("✅ AI Agent initialized successfully!")
except Exception as e:
    ai_agent = None
    print(f"⚠️ AI Agent initialization failed: {e}")
    print("  → Place ai_agent.py in project directory")
    print("  → Set ANTHROPIC_API_KEY environment variable")
    print("  → See QUICK_START.md for setup instructions")

# ============================================
# GAMIFICATION & SUBSCRIPTION SYSTEM
# ============================================

import hashlib
from functools import wraps

# Developer password — loaded from environment
DEVELOPER_PASSWORD_HASH = hashlib.sha256(
    os.environ.get("DEVELOPER_PASSWORD", "changeme").encode()
).hexdigest()

# Points required for each level
XP_LEVELS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5500,
    9: 8000,
    10: 12000,
}

# Section unlock requirements (level and/or subscription tier)
SECTION_REQUIREMENTS = {
    # ── FREE for everyone (whether Monk Mode is on or off) ────────────────
    # The free foundation: the alphabet (the gateway that unlocks levelling)
    # plus the entire Buddhism dropdown — the Dhamma is freely given. Every
    # other content section now sits behind a paid tier (see below), on TOP of
    # its level/XP requirement.
    'home': {'level': 1, 'tier': 'free', 'points_reward': 0, 'requires_alphabet': False},
    'alphabet': {'level': 1, 'tier': 'free', 'points_reward': 100, 'requires_alphabet': False},
    'theravada': {'level': 1, 'tier': 'free', 'points_reward': 40, 'requires_alphabet': False},
    'meditation': {'level': 1, 'tier': 'free', 'points_reward': 40, 'requires_alphabet': False},

    # ── BASIC — Buddhist Scholar (£9.99) ─────────────────────────────────
    # The structured language-learning content (the rest of the Learn menu,
    # Culture, and the exercises). Still gated by level/XP as well as the tier.
    'paiboon': {'level': 1, 'tier': 'basic', 'points_reward': 10, 'requires_alphabet': False},
    'learn': {'level': 1, 'tier': 'basic', 'points_reward': 0, 'requires_alphabet': True},
    'exercise_festivals': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_isan_dialect': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'vowels_syllables': {'level': 2, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'exercise_nature': {'level': 3, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_formal': {'level': 3, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'grammar': {'level': 3, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    # Consonant classes + tone rules. Its content was moved here from the Grammar
    # page, so it's gated the same way — Basic tier, level 3, alphabet required.
    'tones_classes': {'level': 3, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'culture': {'level': 3, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'lessons': {'level': 4, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},
    'register': {'level': 4, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'formality': {'level': 4, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'gender_examples': {'level': 4, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'sentences': {'level': 5, 'tier': 'basic', 'points_reward': 35, 'requires_alphabet': True},
    'greetings_wai': {'level': 5, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},
    'classifiers': {'level': 5, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},
    'tour_guide': {'level': 4, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'business_thai': {'level': 5, 'tier': 'basic', 'points_reward': 30, 'requires_alphabet': True},

    # ── PRO — Thai Master (£19.99) ───────────────────────────────────────
    # The premium power tools. Unlimited AI is enforced separately in the
    # /api/ai/chat route, and Monk Mode never lifts the AI cap.
    'dictionary': {'level': 8, 'tier': 'pro', 'points_reward': 50, 'requires_alphabet': True},
    'premium': {'level': 10, 'tier': 'pro', 'points_reward': 100, 'requires_alphabet': True},
}

# Subscription tiers
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free Explorer (Free)',
        'price': 0,
        'features': [
            '✓ Full Thai alphabet course (44 consonants, 32 vowels)',
            '✓ Theravada Buddhism teachings',
            '✓ Pra Kru Bob Dhamma articles',
            '✓ Meditation timer & techniques',
            '✓ Progress tracking & levelling',
        ],
        'max_level_access': 5,
    },
    'basic': {
        'name': 'Buddhist Scholar (Basic)',
        'price': 9.99,
        'features': [
            '✓ Everything in Free',
            '✓ Vocabulary, grammar & sentence patterns',
            '✓ Culture, formality, register & classifiers',
            '✓ Paiboon romanization guide',
            '✓ Tour Guide & Business Thai',
            '✓ 2x points multiplier',
        ],
        'max_level_access': 7,
        'points_multiplier': 2,
    },
    'pro': {
        'name': 'Thai Master (Pro)',
        'price': 19.99,
        'features': [
            '✓ Everything in Buddhist Scholar',
            '✓ Unlimited AI chat — all modes',
            '✓ Culture & Dhamma AI Q&A',
            '✓ Complete dictionary access',
            '✓ Premium learning tools & content',
            '✓ 3x points multiplier',
            '✓ Priority support',
        ],
        'max_level_access': 10,
        'points_multiplier': 3,
    }
}

# Optional one-time add-on sold on top of Thai Master (Pro): the Instant Access
# Pass flips full_unlock, skipping the level + alphabet gates so every section
# opens instantly. Built with inline Stripe pricing (no dashboard product needed).
INSTANT_ACCESS_ADDON = {
    'name': 'Instant Access Pass',
    'price': 9.99,
    'blurb': 'A one-time unlock for Thai Master members — open every section instantly, with no levelling and no alphabet prerequisite.',
}

# Points awarded for different actions
POINT_REWARDS = {
    'quiz_correct': 10,
    'quiz_perfect': 50,
    'first_visit': 5,
    'daily_login': 15,
    'complete_lesson': 30,
    'unlock_section': 25,
}

# Achievements
ACHIEVEMENTS = {
    'first_steps': {
        'name': '🪷 First Steps',
        'description': 'Complete your first quiz',
        'points': 25,
        'requirement': lambda user: user.get('quizzes_completed', 0) >= 1
    },
    'word_learner': {
        'name': '📚 Word Learner',
        'description': 'Learn 50 words',
        'points': 50,
        'requirement': lambda user: user.get('words_learned', 0) >= 50
    },
    'dedicated_student': {
        'name': '🎓 Dedicated Student',
        'description': 'Login 7 days in a row',
        'points': 100,
        'requirement': lambda user: user.get('login_streak', 0) >= 7
    },
    'grammar_master': {
        'name': '✍️ Grammar Master',
        'description': 'Complete all grammar sections',
        'points': 150,
        'requirement': lambda user: user.get('grammar_sections_complete', 0) >= 25
    },
    'thai_scholar': {
        'name': '👑 Thai Scholar',
        'description': 'Reach Level 5',
        'points': 200,
        'requirement': lambda user: user.get('level', 1) >= 5
    },
    'enlightened': {
        'name': '☸️ Enlightened',
        'description': 'Complete all Theravada teachings',
        'points': 250,
        'requirement': lambda user: user.get('theravada_complete', False)
    },
}

# Helper functions
def init_user_progress():
    """Initialize user progress in session if not exists"""
    if 'user_progress' not in session:
        session['user_progress'] = {
            'xp': 0,
            'level': 1,
            'subscription_tier': 'free',
            'subscription_expires': None,
            'is_developer': False,
            'monk_mode': False,   # free, monk-tailored track for monastics (code-gated)
            'monk_direction': MONK_DIRECTION_DEFAULT,   # 'learn_thai' or 'learn_english'
            'full_unlock': False,  # optional paid add-on (on top of Pro): skips the level/alphabet grind
            'sections_unlocked': ['home', 'alphabet', 'theravada', 'meditation'],
            'sections_visited': [],
            'achievements_earned': [],
            'quizzes_completed': 0,
            'quiz_perfect_count': 0,
            'words_learned': 0,
            'correct_answers': 0,
            'total_answers': 0,
            'login_streak': 1,
            'last_login': datetime.now().isoformat(),
            'daily_points_earned': 0,
            'alphabet_completed': False,
            'alphabet_completion_date': None,
        }
        session.modified = True

def get_user_level(xp):
    """Calculate user level based on XP"""
    for level in sorted(XP_LEVELS.keys(), reverse=True):
        if xp >= XP_LEVELS[level]:
            return level
    return 1

def get_xp_for_next_level(current_level):
    """Get XP required for next level"""
    if current_level >= max(XP_LEVELS.keys()):
        return None
    return XP_LEVELS[current_level + 1]

def active_tier():
    """The subscription tier to enforce RIGHT NOW — the single source of truth.

    For a logged-in user this comes from the DATABASE (User.effective_tier,
    which already accounts for expiry and cancellation). For an anonymous
    visitor we fall back to the session (which is 'free' by default).
    """
    if current_user.is_authenticated:
        return current_user.effective_tier
    return session.get('user_progress', {}).get('subscription_tier', 'free')


def has_full_unlock():
    """Whether the current visitor holds the one-time 'Instant Access Pass'
    add-on. For a logged-in user the DATABASE is the source of truth; anonymous
    visitors fall back to the session copy."""
    if current_user.is_authenticated:
        return bool(getattr(current_user, 'full_unlock', False))
    return session.get('user_progress', {}).get('full_unlock', False)


def monk_mode_active():
    """Monk Mode: a free, all-content-unlocked mode offered to Buddhist monks
    and the Thai diaspora.

    When it's on, every content gate (level, alphabet requirement and
    subscription tier) is bypassed at no charge. It intentionally does NOT lift
    the AI daily usage cap, because AI calls cost real money — unlimited free AI
    is a separate decision, kept out of scope on purpose.
    """
    if 'user_progress' not in session:
        return False
    return session['user_progress'].get('monk_mode', False)


def _valid_monk_codes():
    """The set of currently-valid Monk Mode access codes.

    Codes come from the MONK_MODE_CODES environment variable (comma-separated),
    so they live outside the source and git history and can be rotated or
    revoked without a code change. In local development ONLY, if none are
    configured we fall back to a single obvious test code ('monk-dev') so the
    feature is easy to try. In production an unset variable means Monk Mode
    simply can't be unlocked — it fails safe rather than open.
    """
    raw = os.environ.get('MONK_MODE_CODES', '')
    codes = {c.strip().lower() for c in raw.split(',') if c.strip()}
    if not codes and os.environ.get('FLASK_ENV') == 'development':
        codes = {'monk-dev'}
    return codes


def is_valid_monk_code(code):
    """True if `code` matches one of the currently-valid Monk Mode codes."""
    return (code or '').strip().lower() in _valid_monk_codes()


# ============================================
# MONK MODE CONTENT (the monk-specific lesson track)
# ============================================
# The monk lessons live as one JSON file per topic in content/monk/, kept apart
# from the general (paid/freemium) content on purpose. Loaded once at startup.
MONK_CONTENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content', 'monk')

def _load_monk_topics():
    """Load every content/monk/*.json topic, sorted by its 'order' field."""
    topics = []
    for path in sorted(glob.glob(os.path.join(MONK_CONTENT_DIR, '*.json'))):
        try:
            with open(path, encoding='utf-8') as f:
                topics.append(json.load(f))
        except (json.JSONDecodeError, OSError) as e:
            app.logger.warning("Skipping monk topic %s: %s", path, e)
    topics.sort(key=lambda t: t.get('order', 999))
    return topics

MONK_TOPICS = _load_monk_topics()
MONK_TOPICS_BY_ID = {t['topic']: t for t in MONK_TOPICS}

# The two learning directions Monk Mode supports.
MONK_DIRECTIONS = {'learn_thai', 'learn_english'}
MONK_DIRECTION_DEFAULT = 'learn_thai'   # a Western monk learning Thai

@app.context_processor
def inject_monk_audio():
    """Give templates monk_audio_url(english) -> URL, or None if not generated.

    Native audio is the anchor of the English pronunciation system, but it is
    generated topic by topic, so most entries have no MP3 yet. Returning None
    lets the template simply leave the play button out for those, instead of
    rendering a button that 404s.
    """
    def monk_audio_url(english):
        if not monk_audio.audio_exists(app.static_folder, english):
            return None
        return url_for('static', filename=monk_audio.audio_static_path(english))
    return {'monk_audio_url': monk_audio_url}


def monk_direction():
    """The current Monk Mode learning direction for this visitor."""
    if 'user_progress' not in session:
        return MONK_DIRECTION_DEFAULT
    return session['user_progress'].get('monk_direction', MONK_DIRECTION_DEFAULT)


@app.context_processor
def inject_static_version():
    """Give templates static_v(filename) for cache-busting CSS and JS.

    Without this, a browser that has cached base.css keeps using the old copy
    after a deploy, so style fixes appear not to work. Appending the file's
    modification time makes each edit a new URL, so the browser refetches.
    """
    def static_v(filename):
        url = url_for('static', filename=filename)
        try:
            mtime = int(os.path.getmtime(
                os.path.join(app.static_folder, filename.replace('/', os.sep))))
        except OSError:
            return url
        return '{}?v={}'.format(url, mtime)
    return {'static_v': static_v}


@app.context_processor
def inject_monk_mode():
    """Expose Monk Mode's state to every template, so the nav toggle, the
    'everything unlocked' banner and the direction switch can render on any page
    without each route having to pass them in."""
    return {'monk_mode': monk_mode_active(), 'monk_direction': monk_direction()}

# ============================================
# FREEMIUM AI LIMITS
# ============================================
# Free & Basic tiers get a "taste" of the AI: the Tutor mode only, capped at a
# few messages per day. Pro unlocks every mode with no cap. The daily counter
# lives in the SESSION (not the DB) on purpose — it needs no schema change and
# also works for logged-out visitors. It's a soft limit (a determined user could
# clear cookies to reset it), which is fine for a portfolio/demo app.
FREE_AI_DAILY_LIMIT = 15            # messages/day for free & basic tiers
FREE_AI_ALLOWED_MODES = {'tutor'}   # the only AI mode free & basic can use

def _ai_usage_today():
    """Return today's AI-usage record from the session, resetting at midnight."""
    today = datetime.now().strftime('%Y-%m-%d')
    usage = session.get('ai_usage')
    if not usage or usage.get('date') != today:
        usage = {'date': today, 'count': 0}
        session['ai_usage'] = usage
    return usage

def ai_limits_status():
    """Describe the current visitor's AI access — used by both the template and
    the API gate so the two never disagree."""
    tier = active_tier()
    if tier == 'pro':
        return {
            'tier': tier, 'unlimited': True, 'allowed_modes': None,
            'daily_limit': None, 'used_today': 0, 'remaining': None,
        }
    used = _ai_usage_today()['count']
    return {
        'tier': tier, 'unlimited': False,
        'allowed_modes': sorted(FREE_AI_ALLOWED_MODES),
        'daily_limit': FREE_AI_DAILY_LIMIT,
        'used_today': used,
        'remaining': max(0, FREE_AI_DAILY_LIMIT - used),
    }

def add_xp(points, action_description=""):
    """Add XP to user and check for level up"""
    init_user_progress()
    user = session['user_progress']

    tier = active_tier()
    multiplier = SUBSCRIPTION_TIERS[tier].get('points_multiplier', 1)
    points = int(points * multiplier)
    
    old_level = user['level']
    user['xp'] += points
    user['level'] = get_user_level(user['xp'])
    
    level_up = user['level'] > old_level
    
    session.modified = True
    
    return {
        'points_earned': points,
        'total_xp': user['xp'],
        'level': user['level'],
        'level_up': level_up,
        'action': action_description
    }

def check_section_access(section_id):
    """Check whether the current user can open a section.

    Three independent gates, checked in order: alphabet completion, level/XP,
    and subscription tier. Developer mode bypasses all of them.

    Monk Mode waives ONLY the subscription-tier gate — every content section
    becomes free — while still requiring alphabet completion and the right
    level. Monks earn their way up by levelling like everyone else; they just
    never hit the paywall. (The AI usage cap is enforced separately in the
    chat route, so Monk Mode never makes the costly AI tutor unlimited.)
    """
    init_user_progress()
    user = session['user_progress']

    # Developer mode bypasses everything
    if user.get('is_developer', False):
        return True, "Developer Access"

    if section_id not in SECTION_REQUIREMENTS:
        return True, "No restrictions"

    requirements = SECTION_REQUIREMENTS[section_id]

    # The optional "full unlock" add-on (a paid extra on top of Thai Master)
    # removes the progression grind: it skips the alphabet and level gates so
    # everything opens instantly. It never touches the tier gate (it's sold on
    # top of Pro, which already grants tier access) nor the AI usage cap.
    full_unlock = has_full_unlock()

    # Gate 1 — alphabet completion (skipped by the full-unlock add-on)
    if not full_unlock and requirements.get('requires_alphabet', False):
        if not check_alphabet_completion():
            return False, "Complete Thai Alphabet first"

    # Gate 2 — level / XP (skipped by the full-unlock add-on)
    if not full_unlock and user['level'] < requirements['level']:
        return False, f"Requires Level {requirements['level']}"

    # Gate 3 — subscription tier (payment). Monk Mode waives THIS, and only
    # this, free of charge. Everyone else is held to their real tier.
    if not user.get('monk_mode', False):
        required_tier = requirements['tier']
        user_tier = active_tier()
        tier_hierarchy = {'free': 0, 'basic': 1, 'pro': 2}
        if tier_hierarchy[user_tier] < tier_hierarchy[required_tier]:
            tier_name = SUBSCRIPTION_TIERS[required_tier]['name']
            return False, f"Requires {tier_name} subscription"

    return True, "Access granted"

def unlock_section(section_id):
    """Unlock a section and award points"""
    init_user_progress()
    user = session['user_progress']
    
    if section_id not in user['sections_unlocked']:
        user['sections_unlocked'].append(section_id)
        
        if section_id in SECTION_REQUIREMENTS:
            reward = SECTION_REQUIREMENTS[section_id].get('points_reward', 0)
            if reward > 0:
                add_xp(reward, f"Unlocked {section_id}")
        
        session.modified = True
        return True
    return False

def check_achievements(user):
    """Check and award new achievements"""
    new_achievements = []
    
    for achievement_id, achievement in ACHIEVEMENTS.items():
        if achievement_id not in user.get('achievements_earned', []):
            if achievement['requirement'](user):
                user['achievements_earned'].append(achievement_id)
                add_xp(achievement['points'], f"Achievement: {achievement['name']}")
                new_achievements.append(achievement)
    
    session.modified = True
    return new_achievements

def require_access(section_id):
    """Decorator to protect routes with access control"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            init_user_progress()
            
            has_access, message = check_section_access(section_id)
            
            if not has_access:
                return render_template('locked.html', 
                                     section=section_id,
                                     message=message,
                                     requirements=SECTION_REQUIREMENTS.get(section_id, {}),
                                     user_progress=session['user_progress'])
            
            user = session['user_progress']
            if section_id not in user['sections_visited']:
                user['sections_visited'].append(section_id)
                add_xp(POINT_REWARDS['first_visit'], f"Visited {section_id}")
            
            unlock_section(section_id)
            
            session.modified = True
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator



# ============================================
# GENDER SYSTEM - DYNAMIC LANGUAGE ADAPTATION
# ============================================

GENDER_VARIANTS = {
    'pronouns': {
        'first_person': {
            'male': {
                'formal': {'thai': 'ผม', 'paiboon': 'pǒm', 'english': 'I'},
                'polite': {'thai': 'ผม', 'paiboon': 'pǒm', 'english': 'I'},
                'neutral': {'thai': 'ผม', 'paiboon': 'pǒm', 'english': 'I'},
                'casual': {'thai': 'กู', 'paiboon': 'guu', 'english': 'I'},
            },
            'female': {
                'formal': {'thai': 'ดิฉัน', 'paiboon': 'dì-chǎn', 'english': 'I'},
                'polite': {'thai': 'ดิฉัน', 'paiboon': 'dì-chǎn', 'english': 'I'},
                'neutral': {'thai': 'ฉัน', 'paiboon': 'chǎn', 'english': 'I'},
                'casual': {'thai': 'ฉัน', 'paiboon': 'chǎn', 'english': 'I'},
            },
            'neutral': {
                'formal': {'thai': 'กระผม/ดิฉัน', 'paiboon': 'grà-pǒm/dì-chǎn', 'english': 'I'},
                'polite': {'thai': 'ผม/ดิฉัน', 'paiboon': 'pǒm/dì-chǎn', 'english': 'I'},
                'neutral': {'thai': 'ฉัน', 'paiboon': 'chǎn', 'english': 'I'},
                'casual': {'thai': 'ฉัน', 'paiboon': 'chǎn', 'english': 'I'},
            }
        },
        'second_person': {
            # Same for all genders when addressing others
            'formal': {'thai': 'ท่าน', 'paiboon': 'tân', 'english': 'you'},
            'polite': {'thai': 'คุณ', 'paiboon': 'kun', 'english': 'you'},
            'neutral': {'thai': 'เธอ', 'paiboon': 'təə', 'english': 'you'},
            'casual': {'thai': 'มึง', 'paiboon': 'mʉŋ', 'english': 'you'},
        }
    },
    'particles': {
        'male': {
            'statement': {'thai': 'ครับ', 'paiboon': 'kráp', 'english': 'polite particle'},
            'question': {'thai': 'ครับ', 'paiboon': 'kráp', 'english': 'polite particle'},
        },
        'female': {
            'statement': {'thai': 'ค่ะ', 'paiboon': 'kâ', 'english': 'polite particle'},
            'question': {'thai': 'คะ', 'paiboon': 'ká', 'english': 'polite particle'},
        },
        'neutral': {
            'statement': {'thai': 'ครับ/ค่ะ', 'paiboon': 'kráp/kâ', 'english': 'polite particle'},
            'question': {'thai': 'ครับ/คะ', 'paiboon': 'kráp/ká', 'english': 'polite particle'},
        }
    },
    'greetings': {
        'hello': {
            'male': {
                'formal': {'thai': 'สวัสดีครับ', 'paiboon': 'sà-wàt-dii kráp', 'english': 'Hello'},
                'polite': {'thai': 'สวัสดีครับ', 'paiboon': 'sà-wàt-dii kráp', 'english': 'Hello'},
                'casual': {'thai': 'หวัดดี', 'paiboon': 'wàt-dii', 'english': 'Hi'},
            },
            'female': {
                'formal': {'thai': 'สวัสดีค่ะ', 'paiboon': 'sà-wàt-dii kâ', 'english': 'Hello'},
                'polite': {'thai': 'สวัสดีค่ะ', 'paiboon': 'sà-wàt-dii kâ', 'english': 'Hello'},
                'casual': {'thai': 'หวัดดี', 'paiboon': 'wàt-dii', 'english': 'Hi'},
            }
        },
        'thank_you': {
            'male': {
                'formal': {'thai': 'ขอบพระคุณครับ', 'paiboon': 'kɔ̀ɔp prá-kun kráp', 'english': 'Thank you very much'},
                'polite': {'thai': 'ขอบคุณครับ', 'paiboon': 'kɔ̀ɔp-kun kráp', 'english': 'Thank you'},
                'casual': {'thai': 'ขอบใจ', 'paiboon': 'kɔ̀ɔp-jai', 'english': 'Thanks'},
            },
            'female': {
                'formal': {'thai': 'ขอบพระคุณค่ะ', 'paiboon': 'kɔ̀ɔp prá-kun kâ', 'english': 'Thank you very much'},
                'polite': {'thai': 'ขอบคุณค่ะ', 'paiboon': 'kɔ̀ɔp-kun kâ', 'english': 'Thank you'},
                'casual': {'thai': 'ขอบใจ', 'paiboon': 'kɔ̀ɔp-jai', 'english': 'Thanks'},
            }
        },
        'goodbye': {
            'male': {
                'formal': {'thai': 'ลาก่อนครับ', 'paiboon': 'laa gɔ̀ɔn kráp', 'english': 'Goodbye'},
                'polite': {'thai': 'ลาก่อนครับ', 'paiboon': 'laa gɔ̀ɔn kráp', 'english': 'Goodbye'},
                'casual': {'thai': 'บ้าย', 'paiboon': 'bâai', 'english': 'Bye'},
            },
            'female': {
                'formal': {'thai': 'ลาก่อนค่ะ', 'paiboon': 'laa gɔ̀ɔn kâ', 'english': 'Goodbye'},
                'polite': {'thai': 'ลาก่อนค่ะ', 'paiboon': 'laa gɔ̀ɔn kâ', 'english': 'Goodbye'},
                'casual': {'thai': 'บ้าย', 'paiboon': 'bâai', 'english': 'Bye'},
            }
        },
        'excuse_me': {
            'male': {
                'formal': {'thai': 'ขอโทษครับ', 'paiboon': 'kɔ̌ɔ-tôot kráp', 'english': 'Excuse me'},
                'polite': {'thai': 'ขอโทษครับ', 'paiboon': 'kɔ̌ɔ-tôot kráp', 'english': 'Excuse me'},
                'casual': {'thai': 'ขอโทษ', 'paiboon': 'kɔ̌ɔ-tôot', 'english': 'Sorry'},
            },
            'female': {
                'formal': {'thai': 'ขอโทษค่ะ', 'paiboon': 'kɔ̌ɔ-tôot kâ', 'english': 'Excuse me'},
                'polite': {'thai': 'ขอโทษค่ะ', 'paiboon': 'kɔ̌ɔ-tôot kâ', 'english': 'Excuse me'},
                'casual': {'thai': 'ขอโทษ', 'paiboon': 'kɔ̌ɔ-tôot', 'english': 'Sorry'},
            }
        }
    },
    'requests': {
        'please': {
            'male': {
                'formal': {'thai': 'กรุณา...ครับ', 'paiboon': 'gà-rú-naa... kráp', 'english': 'Please...'},
                'polite': {'thai': 'ช่วย...หน่อยครับ', 'paiboon': 'chûuai... nɔ̀ɔi kráp', 'english': 'Please help...'},
                'casual': {'thai': 'หน่อย', 'paiboon': 'nɔ̀ɔi', 'english': 'Please (informal)'},
            },
            'female': {
                'formal': {'thai': 'กรุณา...ค่ะ', 'paiboon': 'gà-rú-naa... kâ', 'english': 'Please...'},
                'polite': {'thai': 'ช่วย...หน่อยค่ะ', 'paiboon': 'chûuai... nɔ̀ɔi kâ', 'english': 'Please help...'},
                'casual': {'thai': 'หน่อย', 'paiboon': 'nɔ̀ɔi', 'english': 'Please (informal)'},
            }
        }
    }
}

def get_gendered_text(category, subcategory=None, formality='polite', gender=None, text_type='statement'):
    """
    Get gender-appropriate text with formality level.
    
    Args:
        category: 'pronouns', 'particles', 'greetings', 'requests'
        subcategory: e.g., 'first_person', 'hello', etc.
        formality: 'formal', 'polite', 'neutral', 'casual'
        gender: 'male', 'female', 'neutral' (from session or default)
        text_type: 'statement' or 'question' (for particles)
    
    Returns:
        dict with 'thai', 'paiboon', 'english' keys
    """
    if gender is None:
        gender = session.get('user_gender', 'neutral')
    
    try:
        if category == 'pronouns':
            if subcategory == 'first_person':
                return GENDER_VARIANTS['pronouns']['first_person'][gender][formality]
            elif subcategory == 'second_person':
                return GENDER_VARIANTS['pronouns']['second_person'][formality]
        elif category == 'particles':
            return GENDER_VARIANTS['particles'][gender][text_type]
        elif category == 'greetings':
            return GENDER_VARIANTS['greetings'][subcategory][gender][formality]
        elif category == 'requests':
            return GENDER_VARIANTS['requests'][subcategory][gender][formality]
    except KeyError:
        # Fallback to neutral/polite
        return {'thai': '—', 'paiboon': '—', 'english': '—'}
    
    return {'thai': '—', 'paiboon': '—', 'english': '—'}


def build_sentence(gender=None, formality='polite', include_particle=True):
    """
    Build example sentences with gender-appropriate pronouns and particles.
    
    Args:
        gender: 'male', 'female', 'neutral'
        formality: formality level
        include_particle: whether to add politeness particle
    
    Returns:
        dict with example sentences
    """
    if gender is None:
        gender = session.get('user_gender', 'neutral')
    
    pronoun = get_gendered_text('pronouns', 'first_person', formality, gender)
    particle = get_gendered_text('particles', None, formality, gender, 'statement') if include_particle else None
    
    examples = {
        'eating': {
            'thai': f"{pronoun['thai']}กินข้าว{particle['thai'] if particle else ''}",
            'paiboon': f"{pronoun['paiboon']} gin kâao{' ' + particle['paiboon'] if particle else ''}",
            'english': f"I eat rice{' (polite)' if particle else ''}"
        },
        'going': {
            'thai': f"{pronoun['thai']}ไป{particle['thai'] if particle else ''}",
            'paiboon': f"{pronoun['paiboon']} bpai{' ' + particle['paiboon'] if particle else ''}",
            'english': f"I go{' (polite)' if particle else ''}"
        },
        'understanding': {
            'thai': f"{pronoun['thai']}เข้าใจ{particle['thai'] if particle else ''}",
            'paiboon': f"{pronoun['paiboon']} kâo-jai{' ' + particle['paiboon'] if particle else ''}",
            'english': f"I understand{' (polite)' if particle else ''}"
        }
    }
    
    return examples


# ============================================
# FORMALITY SYSTEM - UNIQUE CLASSIFICATION
# WITH PAIBOON ROMANIZATION
# ============================================

FORMALITY_LEVELS = {
    'monastic': {
        'code': 'M',
        'symbol': '☸',
        'name': 'Monastic',
        'thai': 'ภาษาพระสงฆ์',
        'paiboon': 'paa-sǎa prá sǒŋ',
        'description': 'Used exclusively by monks, about monks, or in monastic contexts',
        'color': '#FF9933',
        'examples': [
            {'thai': 'ฉัน', 'paiboon': 'chǎn', 'english': 'to eat (monks only)'},
            {'thai': 'จีวร', 'paiboon': 'jii-won', 'english': 'monastic robes'},
            {'thai': 'บิณฑบาต', 'paiboon': 'bin-tá-bàat', 'english': 'alms round'},
            {'thai': 'พระสงฆ์', 'paiboon': 'prá sǒŋ', 'english': 'Buddhist monk'},
            {'thai': 'วิหาร', 'paiboon': 'wí-hǎan', 'english': 'temple hall'},
        ]
    },
    'royal': {
        'code': 'R',
        'symbol': '👑',
        'name': 'Royal',
        'thai': 'ราชาศัพท์',
        'paiboon': 'raa-chaa-sàp',
        'description': 'Used exclusively for/about royalty and high-ranking religious figures',
        'color': '#D4AF37',
        'examples': [
            {'thai': 'เสวย', 'paiboon': 'sà-wəəi', 'english': 'to eat (royal)'},
            {'thai': 'ตรัส', 'paiboon': 'dtrát', 'english': 'to speak (royal)'},
            {'thai': 'เสด็จ', 'paiboon': 'sà-dèt', 'english': 'to go (royal)'},
            {'thai': 'บรรทม', 'paiboon': 'ban-tom', 'english': 'to sleep (royal)'},
            {'thai': 'สวรรคต', 'paiboon': 'sà-wǎn-ká-dtà', 'english': 'to die (royal)'},
        ]
    },
    'obsolete': {
        'code': 'O',
        'symbol': '⌛',
        'name': 'Obsolete/Archaic',
        'thai': 'ภาษาโบราณ',
        'paiboon': 'paa-sǎa boo-raan',
        'description': 'No longer used in modern Thai; historical or archaic terms',
        'color': '#8B4513',
        'examples': [
            {'thai': 'ฉัน', 'paiboon': 'chǎn', 'english': 'I (obsolete, formal)'},
            {'thai': 'เขา', 'paiboon': 'kǎo', 'english': 'he/she (archaic)'},
            {'thai': 'มัน', 'paiboon': 'man', 'english': 'it (archaic formal)'},
            {'thai': 'เธอ', 'paiboon': 'təə', 'english': 'you (archaic formal)'},
        ]
    },
    'literary': {
        'code': 'L',
        'symbol': '📜',
        'name': 'Literary/Poetic',
        'thai': 'ภาษาวรรณกรรม',
        'paiboon': 'paa-sǎa wan-ná-gam',
        'description': 'Poetic, literary; used in art, literature, or when sounding eloquent',
        'color': '#8B008B',
        'examples': [
            {'thai': 'พระจันทร์', 'paiboon': 'prá jan', 'english': 'moon (poetic)'},
            {'thai': 'ดวงอาทิตย์', 'paiboon': 'duaŋ aa-tít', 'english': 'sun (literary)'},
            {'thai': 'ดวงดาว', 'paiboon': 'duaŋ daao', 'english': 'stars (poetic)'},
            {'thai': 'สายลม', 'paiboon': 'sǎai lom', 'english': 'breeze (literary)'},
            {'thai': 'ห้วงน้ำ', 'paiboon': 'hûaŋ náam', 'english': 'waters (poetic)'},
        ]
    },
    'technical': {
        'code': 'T',
        'symbol': '🔬',
        'name': 'Technical/Specialized',
        'thai': 'ภาษาวิชาการ',
        'paiboon': 'paa-sǎa wí-chaa-gaan',
        'description': 'Technical; unusually precise; used by scientists, doctors, and experts',
        'color': '#1E90FF',
        'examples': [
            {'thai': 'อนุภาค', 'paiboon': 'à-nú-pàak', 'english': 'particle (physics)'},
            {'thai': 'เซลล์', 'paiboon': 'seen', 'english': 'cell (biology)'},
            {'thai': 'ปฏิจจสมุปบาท', 'paiboon': 'bpà-dtìt-jà-sà-mùp-bpàat', 'english': 'Dependent Origination'},
            {'thai': 'โมเลกุล', 'paiboon': 'moo-lee-gun', 'english': 'molecule'},
            {'thai': 'พันธุกรรม', 'paiboon': 'pan-tú-gam', 'english': 'genetics'},
        ]
    },
    'formal': {
        'code': 'F',
        'symbol': '🎩',
        'name': 'Formal/Deferential',
        'thai': 'ภาษาทางการ',
        'paiboon': 'paa-sǎa taaŋ gaan',
        'description': 'Used when higher social ranks are present; formal, respectful, deferential',
        'color': '#4B0082',
        'examples': [
            {'thai': 'ดิฉัน', 'paiboon': 'dì-chǎn', 'english': 'I (female formal)'},
            {'thai': 'ผม', 'paiboon': 'pǒm', 'english': 'I (male polite)'},
            {'thai': 'ท่าน', 'paiboon': 'tân', 'english': 'you (honorific)'},
            {'thai': 'รับประทาน', 'paiboon': 'ráp-bprà-taan', 'english': 'to eat (formal)'},
            {'thai': 'พิจารณา', 'paiboon': 'pí-jaa-rá-naa', 'english': 'to consider (formal)'},
        ]
    },
    'neutral': {
        'code': 'N',
        'symbol': '⚪',
        'name': 'Neutral',
        'thai': 'ภาษากลาง',
        'paiboon': 'paa-sǎa glaaŋ',
        'description': 'No special connotation of formality or informality; standard speech',
        'color': '#228B22',
        'examples': [
            {'thai': 'ผม', 'paiboon': 'pǒm', 'english': 'I (male)'},
            {'thai': 'ดิฉัน', 'paiboon': 'dì-chǎn', 'english': 'I (female)'},
            {'thai': 'คุณ', 'paiboon': 'kun', 'english': 'you (polite)'},
            {'thai': 'กิน', 'paiboon': 'gin', 'english': 'to eat'},
            {'thai': 'สวัสดี', 'paiboon': 'sà-wàt-dii', 'english': 'hello/goodbye'},
            {'thai': 'ขอบคุณ', 'paiboon': 'kɔ̀ɔp kun', 'english': 'thank you'},
        ]
    },
    'casual': {
        'code': 'C',
        'symbol': '💬',
        'name': 'Casual/Colloquial',
        'thai': 'ภาษาพูด',
        'paiboon': 'paa-sǎa pûut',
        'description': 'Spoken, slang, informal, colloquial; used among friends or informal settings',
        'color': '#FFA500',
        'examples': [
            {'thai': 'เออ', 'paiboon': 'əə', 'english': 'yeah'},
            {'thai': 'อ่ะ', 'paiboon': 'à', 'english': 'ok/yeah'},
            {'thai': 'เหรอ', 'paiboon': 'rə̌ə', 'english': 'really?'},
            {'thai': 'จริง', 'paiboon': 'jiŋ', 'english': 'really/seriously (casual)'},
            {'thai': 'ชิว', 'paiboon': 'chiu', 'english': 'chill/relaxed (slang)'},
            {'thai': 'เท่', 'paiboon': 'têe', 'english': 'cool/awesome (slang)'},
        ]
    },
    'impolite': {
        'code': 'I',
        'symbol': '⚠️',
        'name': 'Impolite/Rude',
        'thai': 'ภาษาหยาบ',
        'paiboon': 'paa-sǎa yàap',
        'description': 'Impolite (use only among close friends) but not vulgar',
        'color': '#DC143C',
        'examples': [
            {'thai': 'กู', 'paiboon': 'guu', 'english': 'I (rude/close friends)'},
            {'thai': 'มึง', 'paiboon': 'mʉŋ', 'english': 'you (rude/close friends)'},
            {'thai': 'ไอ้', 'paiboon': 'âi', 'english': 'prefix for males (rude)'},
            {'thai': 'อี', 'paiboon': 'ii', 'english': 'prefix for females (rude)'},
            {'thai': 'เฮ้ย', 'paiboon': 'hə́əi', 'english': 'hey! (rude)'},
        ]
    },
    'vulgar': {
        'code': 'V',
        'symbol': '🚫',
        'name': 'Vulgar/Taboo',
        'thai': 'ภาษาหยาบคาย',
        'paiboon': 'paa-sǎa yàap-kaai',
        'description': 'Obscene; taboo and forbidden; avoid completely!',
        'color': '#8B0000',
        'examples': [
            {'thai': '[Not listed]', 'paiboon': '[Not listed]', 'english': 'Vulgar terms - avoid using'},
            {'thai': '[Forbidden]', 'paiboon': '[Forbidden]', 'english': 'Taboo vocabulary - do not learn'},
        ]
    }
}


def get_formality_badge(formality_code):
    """Generate HTML badge for formality level"""
    if not formality_code or formality_code not in FORMALITY_LEVELS:
        return ''
    
    level = FORMALITY_LEVELS[formality_code]
    return f'<span class="formality-badge" data-formality="{formality_code}" style="background: {level["color"]}; color: white; padding: 2px 6px; border-radius: 10px; font-size: 0.75rem; margin-left: 5px; white-space: nowrap;" title="{level["name"]}: {level["description"]}">{level["symbol"]} {level["code"]}</span>'

# Make formality badge function available in all templates
app.jinja_env.globals.update(get_formality_badge=get_formality_badge)







# ============================================
# THAI VOWELS & SYLLABLES - COMPLETE 32 VOWELS
# ============================================

THAI_VOWELS_32 = {
    'long_vowels': [
        # 14 Long Vowels
        {
            'number': 1,
            'thai': 'อา',
            'paiboon': 'aa',
            'type': 'long',
            'sound': 'long "aa" as in "father"',
            'example_word': {'thai': 'น้า', 'paiboon': 'náa', 'english': 'aunt/uncle'},
            'length_note': 'Held longer than short "a"'
        },
        {
            'number': 2,
            'thai': 'อี',
            'paiboon': 'ii',
            'type': 'long',
            'sound': 'long "ee" as in "see"',
            'example_word': {'thai': 'ที่', 'paiboon': 'têe', 'english': 'at/place'},
            'length_note': 'Like English "eee" held longer'
        },
        {
            'number': 3,
            'thai': 'อื',
            'paiboon': 'ʉʉ',
            'type': 'long',
            'sound': 'long "ue" - bite molars, say "errr"',
            'example_word': {'thai': 'ชื่อ', 'paiboon': 'chʉ̂ʉ', 'english': 'name'},
            'length_note': 'Unique to Thai - teeth together, lips unrounded'
        },
        {
            'number': 4,
            'thai': 'อู',
            'paiboon': 'uu',
            'type': 'long',
            'sound': 'long "oo" as in "moon"',
            'example_word': {'thai': 'ที่นู่น', 'paiboon': 'têe nûun', 'english': 'over there'},
            'length_note': 'Round lips, like "ooo" in "food"'
        },
        {
            'number': 5,
            'thai': 'เอ',
            'paiboon': 'ee',
            'type': 'long',
            'sound': 'long "ay" as in "day"',
            'example_word': {'thai': 'เล่น', 'paiboon': 'lên', 'english': 'play'},
            'length_note': 'Like "ay" held longer'
        },
        {
            'number': 6,
            'thai': 'แอ',
            'paiboon': 'ɛɛ',
            'type': 'long',
            'sound': 'long "eh" - wide mouth, like "air"',
            'example_word': {'thai': 'แม่', 'paiboon': 'mɛ̂ɛ', 'english': 'mother'},
            'length_note': 'Stretch mouth wide like smiling'
        },
        {
            'number': 7,
            'thai': 'โอ',
            'paiboon': 'oo',
            'type': 'long',
            'sound': 'long "o" as in "go"',
            'example_word': {'thai': 'โต', 'paiboon': 'dtoo', 'english': 'grow/big'},
            'length_note': 'Like "oh" held longer'
        },
        {
            'number': 8,
            'thai': 'ออ',
            'paiboon': 'ɔɔ',
            'type': 'long',
            'sound': 'long "aw" as in "saw"',
            'example_word': {'thai': 'น้อย', 'paiboon': 'nɔ́ɔi', 'english': 'little/few'},
            'length_note': 'Open mouth wide, like "aw"'
        },
        {
            'number': 9,
            'thai': 'เออ',
            'paiboon': 'əə',
            'type': 'long',
            'sound': 'long "er" as in "bird"',
            'example_word': {'thai': 'เธอ', 'paiboon': 'təə', 'english': 'you (informal)'},
            'length_note': 'Neutral vowel held longer'
        },
        {
            'number': 10,
            'thai': 'เอีย',
            'paiboon': 'ia',
            'type': 'long',
            'sound': 'long "ia" - gliding vowel',
            'example_word': {'thai': 'เที่ยว', 'paiboon': 'tîao', 'english': 'travel/trip'},
            'length_note': 'Diphthong: "ee" + "a"'
        },
        {
            'number': 11,
            'thai': 'เอือ',
            'paiboon': 'ʉa',
            'type': 'long',
            'sound': 'long "uea" - gliding vowel',
            'example_word': {'thai': 'เรือ', 'paiboon': 'rʉa', 'english': 'boat'},
            'length_note': 'Diphthong: "ʉʉ" + "a"'
        },
        {
            'number': 12,
            'thai': 'อัว',
            'paiboon': 'ua',
            'type': 'long',
            'sound': 'long "ua" - gliding vowel',
            'example_word': {'thai': 'เรือ', 'paiboon': 'rua', 'english': 'boat (alternate)'},
            'length_note': 'Diphthong: "uu" + "a"'
        },
        {
            'number': 13,
            'thai': 'ไอ/ใอ',
            'paiboon': 'ai',
            'type': 'long',
            'sound': 'long "ai" as in "Thai"',
            'example_word': {'thai': 'ใคร', 'paiboon': 'krai', 'english': 'who'},
            'length_note': 'Diphthong: "a" + "i"'
        },
        {
            'number': 14,
            'thai': 'เอา',
            'paiboon': 'ao',
            'type': 'long',
            'sound': 'long "ao" as in "Lao"',
            'example_word': {'thai': 'เก่า', 'paiboon': 'gào', 'english': 'old'},
            'length_note': 'Diphthong: "a" + "o"'
        },
    ],
    
    'short_vowels': [
        # 18 Short Vowels
        {
            'number': 15,
            'thai': 'อะ',
            'paiboon': 'a',
            'type': 'short',
            'sound': 'short "a" as in "bat"',
            'example_word': {'thai': 'ขนม', 'paiboon': 'kà-nǒm', 'english': 'snack'},
            'length_note': 'Quick, clipped - half length of "aa"'
        },
        {
            'number': 16,
            'thai': 'อิ',
            'paiboon': 'i',
            'type': 'short',
            'sound': 'short "i" as in "bit"',
            'example_word': {'thai': 'กิน', 'paiboon': 'gin', 'english': 'eat'},
            'length_note': 'Quick "i" - half length of "ii"'
        },
        {
            'number': 17,
            'thai': 'อึ',
            'paiboon': 'ʉ',
            'type': 'short',
            'sound': 'short "ue" - bite molars, quick "er"',
            'example_word': {'thai': 'พึง', 'paiboon': 'pʉŋ', 'english': 'should'},
            'length_note': 'Quick version of "ʉʉ"'
        },
        {
            'number': 18,
            'thai': 'อุ',
            'paiboon': 'u',
            'type': 'short',
            'sound': 'short "u" as in "put"',
            'example_word': {'thai': 'ตุ๊กตา', 'paiboon': 'dtúk-dtaa', 'english': 'doll'},
            'length_note': 'Quick "u" - half length of "uu"'
        },
        {
            'number': 19,
            'thai': 'เอะ',
            'paiboon': 'e',
            'type': 'short',
            'sound': 'short "e" as in "bed"',
            'example_word': {'thai': 'เด็ก', 'paiboon': 'dèk', 'english': 'child'},
            'length_note': 'Quick "e" - half length of "ee"'
        },
        {
            'number': 20,
            'thai': 'แอะ',
            'paiboon': 'ɛ',
            'type': 'short',
            'sound': 'short "eh" - wide mouth',
            'example_word': {'thai': 'แก้ว', 'paiboon': 'gɛ̂ɛo', 'english': 'glass'},
            'length_note': 'Quick "ɛ" - half length of "ɛɛ"'
        },
        {
            'number': 21,
            'thai': 'โอะ',
            'paiboon': 'o',
            'type': 'short',
            'sound': 'short "o"',
            'example_word': {'thai': 'นก', 'paiboon': 'nók', 'english': 'bird'},
            'length_note': 'Quick "o" - half length of "oo"'
        },
        {
            'number': 22,
            'thai': 'เอาะ',
            'paiboon': 'ɔ',
            'type': 'short',
            'sound': 'short "aw"',
            'example_word': {'thai': 'พอ', 'paiboon': 'pɔɔ', 'english': 'enough'},
            'length_note': 'Quick "ɔ" - half length of "ɔɔ"'
        },
        {
            'number': 23,
            'thai': 'เออะ',
            'paiboon': 'ə',
            'type': 'short',
            'sound': 'short "er" as in "the"',
            'example_word': {'thai': 'เมิน', 'paiboon': 'məən', 'english': 'ignore'},
            'length_note': 'Quick neutral vowel - half length of "əə"'
        },
        {
            'number': 24,
            'thai': 'เอียะ',
            'paiboon': 'iạ',
            'type': 'short',
            'sound': 'short "ia"',
            'example_word': {'thai': 'เปรี้ยว', 'paiboon': 'bprîao', 'english': 'sour'},
            'length_note': 'Quick gliding vowel'
        },
        {
            'number': 25,
            'thai': 'เอือะ',
            'paiboon': 'ʉạ',
            'type': 'short',
            'sound': 'short "uea"',
            'example_word': {'thai': 'เหนือ', 'paiboon': 'nʉ̌a', 'english': 'above/north'},
            'length_note': 'Quick gliding vowel'
        },
        {
            'number': 26,
            'thai': 'อัวะ',
            'paiboon': 'uạ',
            'type': 'short',
            'sound': 'short "ua"',
            'example_word': {'thai': 'กัวน', 'paiboon': 'guan', 'english': 'bother'},
            'length_note': 'Quick gliding vowel'
        },
        {
            'number': 27,
            'thai': 'ไอย',
            'paiboon': 'ai',
            'type': 'short',
            'sound': 'short "ai"',
            'example_word': {'thai': 'ไก่', 'paiboon': 'gài', 'english': 'chicken'},
            'length_note': 'Quick diphthong'
        },
        {
            'number': 28,
            'thai': 'อาว',
            'paiboon': 'aao',
            'type': 'short',
            'sound': 'short "ao"',
            'example_word': {'thai': 'กาว', 'paiboon': 'gaao', 'english': 'glue'},
            'length_note': 'Quick diphthong'
        },
        {
            'number': 29,
            'thai': 'อิว',
            'paiboon': 'io',
            'type': 'short',
            'sound': 'short "io"',
            'example_word': {'thai': 'เขียว', 'paiboon': 'kǐao', 'english': 'green'},
            'length_note': 'Quick gliding vowel'
        },
        {
            'number': 30,
            'thai': 'เอว',
            'paiboon': 'eeo',
            'type': 'short',
            'sound': 'short "eo"',
            'example_word': {'thai': 'แถว', 'paiboon': 'tɛ̌ɛo', 'english': 'row/line'},
            'length_note': 'Quick gliding vowel'
        },
        {
            'number': 31,
            'thai': 'แอว',
            'paiboon': 'ɛɛo',
            'type': 'short',
            'sound': 'short "aeo"',
            'example_word': {'thai': 'แว่น', 'paiboon': 'wɛ̂ɛn', 'english': 'glasses'},
            'length_note': 'Quick gliding vowel'
        },
        {
            'number': 32,
            'thai': 'อุย',
            'paiboon': 'ui',
            'type': 'short',
            'sound': 'short "ui"',
            'example_word': {'thai': 'ฝุ่น', 'paiboon': 'fùn', 'english': 'dust'},
            'length_note': 'Quick gliding vowel'
        },
    ],
    
    'meaning_pairs': [
        # Examples showing how vowel length changes meaning
        {
            'short': {'thai': 'นก', 'paiboon': 'nók', 'english': 'bird', 'vowel': 'o (short)'},
            'long': {'thai': 'โน้ต', 'paiboon': 'nóot', 'english': 'musical note', 'vowel': 'oo (long)'},
            'lesson': 'Vowel length completely changes the word meaning!'
        },
        {
            'short': {'thai': 'กิน', 'paiboon': 'gin', 'english': 'eat', 'vowel': 'i (short)'},
            'long': {'thai': 'กีฬา', 'paiboon': 'gii-laa', 'english': 'sport', 'vowel': 'ii (long)'},
            'lesson': 'Short "i" vs long "ii" creates different words'
        },
        {
            'short': {'thai': 'ขนม', 'paiboon': 'kà-nǒm', 'english': 'snack', 'vowel': 'a (short)'},
            'long': {'thai': 'ขนาด', 'paiboon': 'kà-nàat', 'english': 'size', 'vowel': 'aa (long)'},
            'lesson': 'Vowel length distinction is essential for correct meaning'
        },
        {
            'short': {'thai': 'สุก', 'paiboon': 'sùk', 'english': 'ripe/cooked', 'vowel': 'u (short)'},
            'long': {'thai': 'สูง', 'paiboon': 'sǔuŋ', 'english': 'tall/high', 'vowel': 'uu (long)'},
            'lesson': 'Pay attention to vowel duration for accurate pronunciation'
        },
        {
            'short': {'thai': 'คน', 'paiboon': 'kon', 'english': 'person', 'vowel': 'o (short)'},
            'long': {'thai': 'โคน', 'paiboon': 'koon', 'english': 'base/bottom', 'vowel': 'oo (long)'},
            'lesson': 'Same consonants, different vowel lengths = different meanings'
        },
    ],
    
    'syllable_structure': {
        'basic_pattern': 'C + V + T (Consonant + Vowel + Tone)',
        'note': 'Thai syllables can be: CV, CVC, CCVC, or more complex',
        'examples': [
            {
                'thai': 'ดี',
                'paiboon': 'dii',
                'structure': 'CV (consonant + vowel)',
                'breakdown': 'ด (d) + อี (ii)',
                'english': 'good'
            },
            {
                'thai': 'กิน',
                'paiboon': 'gin',
                'structure': 'CVC (consonant + vowel + consonant)',
                'breakdown': 'ก (g) + อิ (i) + น (n)',
                'english': 'eat'
            },
            {
                'thai': 'ครับ',
                'paiboon': 'kráp',
                'structure': 'CCVC (2 consonants + vowel + consonant)',
                'breakdown': 'ค (k) + ร (r) + อะ (a) + บ (p)',
                'english': 'yes (male polite)'
            },
        ]
    }
}



# ============================================
# BEGINNER MODE HELPER FUNCTIONS
# ============================================

def apply_beginner_mode(text):
    """
    Apply beginner-friendly romanization:
    - Final 'i' becomes 'y' (if only one 'i' in word)
    - Final 'o' becomes 'w' (if only one 'o' in word)
    """
    words = text.split()
    converted_words = []
    
    for word in words:
        if word.count('i') == 1 and word.endswith('i'):
            word = word[:-1] + 'y'
        if word.count('o') == 1 and word.endswith('o'):
            word = word[:-1] + 'w'
        converted_words.append(word)
    
    return ' '.join(converted_words)


def get_vocab_with_mode(vocab_list, beginner_mode=False):
    """Return vocabulary with optional beginner mode applied"""
    if not beginner_mode:
        return vocab_list
    
    converted = []
    for item in vocab_list:
        new_item = item.copy()
        new_item['paiboon'] = apply_beginner_mode(item['paiboon'])
        converted.append(new_item)
    return converted


# ============================================
# VOCABULARY DATA - EXPANDED (20 words per category except Tour/Business_Vocab = 25 words each)
# ============================================

TOUR_VOCAB = {
    'transport': [
        {'english': 'Where?', 'thai': 'ที่ไหน', 'paiboon': 'têe-nǎi', 'note': 'Common question for locations'},
        {'english': 'Go', 'thai': 'ไป', 'paiboon': 'bpai', 'note': 'Basic movement verb'},
        {'english': 'Taxi', 'thai': 'แท็กซี่', 'paiboon': 'tɛ́k-sêe', 'note': 'Borrowed from English'},
        {'english': 'Turn left', 'thai': 'เลี้ยวซ้าย', 'paiboon': 'líao sáai', 'note': 'Essential for giving directions'},
        {'english': 'Turn right', 'thai': 'เลี้ยวขวา', 'paiboon': 'líao kwǎa', 'note': 'Essential for giving directions'},
    ],
    'accommodation': [
        {'english': 'Hotel', 'thai': 'โรงแรม', 'paiboon': 'roong-rɛɛm', 'note': 'Formal term'},
        {'english': 'Room', 'thai': 'ห้อง', 'paiboon': 'hɔ̂ɔng', 'note': 'Used for hotel rooms and bathrooms'},
        {'english': 'Air conditioning', 'thai': 'แอร์', 'paiboon': 'ɛɛ', 'note': 'Shortened from "air"'},
        {'english': 'Key', 'thai': 'กุญแจ', 'paiboon': 'gun-jɛɛ', 'note': 'For room access'},
    ],
    'sightseeing': [
        {'english': 'Temple', 'thai': 'วัด', 'paiboon': 'wát', 'note': 'Buddhist temples are everywhere in Thailand'},
        {'english': 'Beautiful', 'thai': 'สวย', 'paiboon': 'sǔai', 'note': 'Common compliment'},
        {'english': 'Take a photo', 'thai': 'ถ่ายรูป', 'paiboon': 'tàai-rûup', 'note': 'Literally "take picture"'},
        {'english': 'Entrance fee', 'thai': 'ค่าเข้า', 'paiboon': 'kâa-kâo', 'note': 'Literally "entrance cost"'},
    ],
    'shopping': [
        {'english': 'How much?', 'thai': 'เท่าไหร่', 'paiboon': 'tâo-rài', 'note': 'Essential shopping phrase'},
        {'english': 'Expensive', 'thai': 'แพง', 'paiboon': 'pɛɛng', 'note': 'For negotiating prices'},
        {'english': 'Discount / Reduce', 'thai': 'ลด', 'paiboon': 'lót', 'note': 'Verb meaning "reduce"'},
        {'english': 'Cheap', 'thai': 'ถูก', 'paiboon': 'tùuk', 'note': 'Can also mean "correct"'},
    ],
    'food': [
        {'english': 'Delicious', 'thai': 'อร่อย', 'paiboon': 'à-rɔ̀i', 'note': 'Most useful food adjective'},
        {'english': 'Spicy', 'thai': 'เผ็ด', 'paiboon': 'pèt', 'note': 'Critical for food preferences'},
        {'english': 'Not spicy', 'thai': 'ไม่เผ็ด', 'paiboon': 'mâi pèt', 'note': 'Essential for many foreigners'},
        {'english': 'Water', 'thai': 'น้ำ', 'paiboon': 'náam', 'note': 'Also means liquid in general'},
        {'english': 'Bill / Check', 'thai': 'เช็คบิล', 'paiboon': 'chék-bin', 'note': 'Used to request the bill'},
    ],
    'emergencies': [
        {'english': 'Help!', 'thai': 'ช่วยด้วย', 'paiboon': 'chûai-dûai', 'note': 'Emergency cry for help'},
        {'english': 'Hospital', 'thai': 'โรงพยาบาล', 'paiboon': 'roong-pa-yaa-baan', 'note': 'Important for emergencies'},
        {'english': 'Police', 'thai': 'ตำรวจ', 'paiboon': 'dam-rùat', 'note': 'For reporting issues'},
    ],
}

BUSINESS_VOCAB = {
    'greetings': [
        {'english': 'Polite greeting', 'thai': 'สวัสดี', 'paiboon': 'sà-wàt-dii', 'note': 'Add ครับ (kráp) male or ค่ะ (kâ) female'},
        {'english': 'Nice to meet you', 'thai': 'ยินดีที่ได้รู้จัก', 'paiboon': 'yin-dii-têe-dâi-rúu-jàk', 'note': 'Formal introduction phrase'},
        {'english': 'Business card', 'thai': 'นามบัตร', 'paiboon': 'naam-bàt', 'note': 'Exchange with both hands — essential for networking'},
        {'english': 'Company', 'thai': 'บริษัท', 'paiboon': 'bɔɔ-rí-sàt', 'note': 'Formal term for company'},
    ],
    'meetings': [
        {'english': 'Meeting', 'thai': 'ประชุม', 'paiboon': 'bpra-chum', 'note': 'Can be used as noun or verb'},
        {'english': 'Appointment', 'thai': 'นัดหมาย', 'paiboon': 'nát-mǎai', 'note': 'Scheduled meeting'},
        {'english': 'Discuss (formal)', 'thai': 'หารือ', 'paiboon': 'hǎa-rʉʉ', 'note': 'Formal discussion — more respectful than พูด'},
        {'english': 'Agree', 'thai': 'เห็นด้วย', 'paiboon': 'hěn-dûai', 'note': 'To agree with something'},
        {'english': 'Consider', 'thai': 'พิจารณา', 'paiboon': 'pí-jaa-rá-naa', 'note': 'Formal deliberation — used in official contexts'},
    ],
    'office': [
        {'english': 'Document', 'thai': 'เอกสาร', 'paiboon': 'èek-gà-sǎan', 'note': 'Any official paperwork'},
        {'english': 'Email', 'thai': 'อีเมล', 'paiboon': 'ii-meen', 'note': 'Borrowed from English'},
        {'english': 'Office', 'thai': 'สำนักงาน', 'paiboon': 'sǎm-nák-ngaan', 'note': 'Formal workplace — สำนักงานใหญ่ = head office'},
        {'english': 'Schedule / Agenda', 'thai': 'กำหนดการ', 'paiboon': 'gam-nòt-gaan', 'note': 'Timeline or agenda'},
    ],
    'banking': [
        {'english': 'Bank', 'thai': 'ธนาคาร', 'paiboon': 'tá-naa-kaan', 'note': 'Financial institution'},
        {'english': 'Account', 'thai': 'บัญชี', 'paiboon': 'ban-chii', 'note': 'Bank or financial account'},
        {'english': 'Transfer', 'thai': 'โอน', 'paiboon': 'oon', 'note': 'Money transfer verb — โอนเงิน = transfer money'},
        {'english': 'Investment', 'thai': 'การลงทุน', 'paiboon': 'gaan-long-tun', 'note': 'Business investment'},
        {'english': 'Budget', 'thai': 'งบประมาณ', 'paiboon': 'ngóp-bpra-maan', 'note': 'Financial planning term'},
    ],
    'contracts': [
        {'english': 'Contract', 'thai': 'สัญญา', 'paiboon': 'sǎn-yaa', 'note': 'Legal agreement'},
        {'english': 'Sign', 'thai': 'เซ็น', 'paiboon': 'sen', 'note': 'To sign documents'},
        {'english': 'Terms and conditions', 'thai': 'เงื่อนไข', 'paiboon': 'ngʉ̂an-kǎi', 'note': 'Conditions of agreement'},
        {'english': 'Legal / Law', 'thai': 'กฎหมาย', 'paiboon': 'gòt-mǎai', 'note': 'Literally "law" — used broadly for legal matters'},
    ],
    'hierarchy': [
        {'english': 'Director', 'thai': 'ผู้อำนวยการ', 'paiboon': 'pûu-am-nuai-gaan', 'note': 'Executive director level'},
        {'english': 'Manager', 'thai': 'ผู้จัดการ', 'paiboon': 'pûu-jàt-gaan', 'note': 'Department manager'},
        {'english': 'Employee / Staff', 'thai': 'พนักงาน', 'paiboon': 'pá-nák-ngaan', 'note': 'General staff member'},
    ],
}

VOCABULARY = {
    'festivals': [
        {'thai': 'สงกรานต์', 'paiboon': 'sǒŋ-graan', 'english': 'Songkran (Thai New Year)', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'ลอยกระทง', 'paiboon': 'loi grà-toŋ', 'english': 'Loy Krathong Festival', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันวิสาขบูชา', 'paiboon': 'wan wí-sǎa-ká-boo-chaa', 'english': 'Visakha Bucha Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'บุญบั้งไฟ', 'paiboon': 'bun bâŋ fai', 'english': 'Rocket Festival (Isan)', 'category': 'festivals', 'formality': 'casual'},
        {'thai': 'วันขึ้นปีใหม่', 'paiboon': 'wan kʉ̂n bpii mài', 'english': "New Year's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันเข้าพรรษา', 'paiboon': 'wan kâo pan-sǎa', 'english': 'Buddhist Lent Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'วันออกพรรษา', 'paiboon': 'wan ɔ̀ɔk pan-sǎa', 'english': 'End of Buddhist Lent', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'วันมาฆบูชา', 'paiboon': 'wan maa-ká-boo-chaa', 'english': 'Makha Bucha Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'วันอาสาฬหบูชา', 'paiboon': 'wan aa-sǎan-há-boo-chaa', 'english': 'Asanha Bucha Day', 'category': 'festivals', 'formality': 'formal'},
        {'thai': 'ตรุษจีน', 'paiboon': 'dtrùt jiin', 'english': 'Chinese New Year', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันพ่อ', 'paiboon': 'wan pɔ̂ɔ', 'english': "Father's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันแม่', 'paiboon': 'wan mɛ̂ɛ', 'english': "Mother's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันเด็ก', 'paiboon': 'wan dèk', 'english': "Children's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันครู', 'paiboon': 'wan kruu', 'english': "Teacher's Day", 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'วันจักรี', 'paiboon': 'wan jàk-grii', 'english': 'Chakri Day', 'category': 'festivals', 'formality': 'royal'},
        {'thai': 'วันฉัตรมงคล', 'paiboon': 'wan chàt-moŋ-kon', 'english': 'Coronation Day', 'category': 'festivals', 'formality': 'royal'},
        {'thai': 'วันพืชมงคล', 'paiboon': 'wan pʉ̂ʉt-moŋ-kon', 'english': 'Royal Ploughing Ceremony', 'category': 'festivals', 'formality': 'royal'},
        {'thai': 'ผีตาโขน', 'paiboon': 'pǐi dtaa kǒon', 'english': 'Ghost Festival', 'category': 'festivals', 'formality': 'casual'},
        {'thai': 'เทศกาลกินเจ', 'paiboon': 'tâyt-sà-gaan gin jee', 'english': 'Vegetarian Festival', 'category': 'festivals', 'formality': 'neutral'},
        {'thai': 'งานบุญ', 'paiboon': 'ŋaan bun', 'english': 'Merit-making ceremony', 'category': 'festivals', 'formality': 'neutral'},
    ],
    
    'isan_dialect': [
        {'thai': 'สบายดีบ่', 'paiboon': 'sà-baai dii bɔ̀ɔ', 'english': 'How are you? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'กินข้าวแล้วบ่', 'paiboon': 'gin kâao lɛ́ɛo bɔ̀ɔ', 'english': 'Have you eaten? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'แซบหลาย', 'paiboon': 'sɛ̂ɛp lǎai', 'english': 'Very delicious (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'บักหุ่ง', 'paiboon': 'bàk hùŋ', 'english': 'Papaya (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'อีหลี', 'paiboon': 'ii-lǐi', 'english': 'Really? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'บ่เป็นหยัง', 'paiboon': 'bɔ̀ɔ bpen yǎŋ', 'english': "No problem (Isan)", 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'เว้า', 'paiboon': 'wáo', 'english': 'To speak (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'ม่วน', 'paiboon': 'mûan', 'english': 'Fun (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'โตน', 'paiboon': 'dtoon', 'english': 'Waterfall (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'คัก', 'paiboon': 'kák', 'english': 'Very/really (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'แม่นบ่', 'paiboon': 'mɛ̂ɛn bɔ̀ɔ', 'english': 'Is that right? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'เฮ็ด', 'paiboon': 'hét', 'english': 'To do (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'บ่มี', 'paiboon': 'bɔ̀ɔ mii', 'english': "Don't have (Isan)", 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'อยู่ไส', 'paiboon': 'yùu sǎi', 'english': 'Where? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'ไผ', 'paiboon': 'pǎi', 'english': 'Who? (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'สิ', 'paiboon': 'sì', 'english': 'Will (Isan future)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'แหน่', 'paiboon': 'nɛ̀ɛ', 'english': 'Emphasis particle (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'หมู่', 'paiboon': 'mùu', 'english': 'You all (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'เด้อ', 'paiboon': 'dəə', 'english': 'Polite particle (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
        {'thai': 'ข้อย', 'paiboon': 'kɔ̂ɔi', 'english': 'I/me (Isan)', 'category': 'isan_dialect', 'formality': 'casual'},
    ],
    
    'nature': [
        {'thai': 'ดอกบัว', 'paiboon': 'dɔ̀ɔk buua', 'english': 'Lotus flower', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ต้นโพธิ์', 'paiboon': 'dtôn poo', 'english': 'Bodhi tree', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ช้าง', 'paiboon': 'cháaŋ', 'english': 'Elephant', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'มะพร้าว', 'paiboon': 'má-práao', 'english': 'Coconut', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'น้ำตก', 'paiboon': 'nám dtòk', 'english': 'Waterfall', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ภูเขา', 'paiboon': 'puu-kǎo', 'english': 'Mountain', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'แม่น้ำ', 'paiboon': 'mɛ̂ɛ náam', 'english': 'River', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ทะเล', 'paiboon': 'tá-lee', 'english': 'Sea/Ocean', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ป่า', 'paiboon': 'bpàa', 'english': 'Forest', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ดอกไม้', 'paiboon': 'dɔ̀ɔk mái', 'english': 'Flower', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ต้นไม้', 'paiboon': 'dtôn mái', 'english': 'Tree', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'นก', 'paiboon': 'nók', 'english': 'Bird', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ปลา', 'paiboon': 'bplaa', 'english': 'Fish', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ผีเสื้อ', 'paiboon': 'pǐi sʉ̂a', 'english': 'Butterfly', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ดวงจันทร์', 'paiboon': 'duuaŋ jan', 'english': 'Moon', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ดวงอาทิตย์', 'paiboon': 'duuaŋ aa-tít', 'english': 'Sun', 'category': 'nature', 'formality': 'literary'},
        {'thai': 'ดาว', 'paiboon': 'daao', 'english': 'Star', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ฝน', 'paiboon': 'fǒn', 'english': 'Rain', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'ลม', 'paiboon': 'lom', 'english': 'Wind', 'category': 'nature', 'formality': 'neutral'},
        {'thai': 'เมฆ', 'paiboon': 'mâyk', 'english': 'Cloud', 'category': 'nature', 'formality': 'neutral'},
    ],
    
    'buddhist_formal': [
        {'thai': 'พระพุทธเจ้า', 'paiboon': 'prá-pút-tá-jâo', 'english': 'The Buddha', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'พระสงฆ์', 'paiboon': 'prá-sǒŋ', 'english': 'Buddhist monks', 'category': 'buddhist_formal', 'formality': 'monastic'},
        {'thai': 'ทำบุญ', 'paiboon': 'tam bun', 'english': 'Make merit', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'วัด', 'paiboon': 'wát', 'english': 'Temple', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'สวดมนต์', 'paiboon': 'sùuat mon', 'english': 'Chant prayers', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'กราบ', 'paiboon': 'gràap', 'english': 'Prostrate', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'พระธรรม', 'paiboon': 'prá-tam', 'english': 'The Dharma', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'พระไตรปิฎก', 'paiboon': 'prá-dtrai-bpì-dòk', 'english': 'Tripitaka', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'นิพพาน', 'paiboon': 'níp-paan', 'english': 'Nirvana', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'สังสารวัฏ', 'paiboon': 'sǎŋ-sǎa-rá-wát', 'english': 'Samsara', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'กรรม', 'paiboon': 'gam', 'english': 'Karma', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'ศีล', 'paiboon': 'sǐin', 'english': 'Precepts (Sila)', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'สมาธิ', 'paiboon': 'sà-maa-tí', 'english': 'Concentration (Samadhi)', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'ปัญญา', 'paiboon': 'bpan-yaa', 'english': 'Wisdom (Panna)', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'อริยสัจสี่', 'paiboon': 'à-rí-yá-sàt sìi', 'english': 'Four Noble Truths', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'มรรคมีองค์แปด', 'paiboon': 'mák mii oŋ bpàet', 'english': 'Eightfold Path', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'บิณฑบาต', 'paiboon': 'bìn-tá-bàat', 'english': 'Alms round', 'category': 'buddhist_formal', 'formality': 'monastic'},
        {'thai': 'อุโบสถ', 'paiboon': 'ù-boo-sòt', 'english': 'Ordination hall', 'category': 'buddhist_formal', 'formality': 'formal'},
        {'thai': 'เจดีย์', 'paiboon': 'jee-dii', 'english': 'Stupa/Pagoda', 'category': 'buddhist_formal', 'formality': 'neutral'},
        {'thai': 'พระพุทธรูป', 'paiboon': 'prá-pút-tá-rûup', 'english': 'Buddha statue', 'category': 'buddhist_formal', 'formality': 'formal'},
    ],
    
    'theravada_dhamma': [
        {'thai': 'ทุกข์', 'paiboon': 'túk', 'english': 'Suffering (Dukkha)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สมุทัย', 'paiboon': 'sà-mú-tai', 'english': 'Origin of suffering', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'นิโรธ', 'paiboon': 'ní-rôot', 'english': 'Cessation (Nirodha)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'มรรค', 'paiboon': 'mák', 'english': 'Path (Magga)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'อนิจจัง', 'paiboon': 'à-nít-jaŋ', 'english': 'Impermanence (Anicca)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'อนัตตา', 'paiboon': 'à-nát-dtaa', 'english': 'Non-self (Anatta)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'ไตรลักษณ์', 'paiboon': 'dtrai-lák', 'english': 'Three Marks', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'ปฏิจจสมุปบาท', 'paiboon': 'bpà-dtìt-jà-sà-mùp-bàat', 'english': 'Dependent Origination', 'category': 'theravada_dhamma', 'formality': 'technical'},
        {'thai': 'ขันธ์ห้า', 'paiboon': 'kǎn hâa', 'english': 'Five Aggregates', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สติ', 'paiboon': 'sà-dtì', 'english': 'Mindfulness (Sati)', 'category': 'theravada_dhamma', 'formality': 'neutral'},
        {'thai': 'สัมมาทิฏฐิ', 'paiboon': 'sǎm-maa-tít-tì', 'english': 'Right View', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาสังกัปปะ', 'paiboon': 'sǎm-maa-sǎŋ-gàp-bpà', 'english': 'Right Intention', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาวาจา', 'paiboon': 'sǎm-maa-waa-jaa', 'english': 'Right Speech', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมากัมมันตะ', 'paiboon': 'sǎm-maa-gam-man-dtà', 'english': 'Right Action', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาอาชีวะ', 'paiboon': 'sǎm-maa-aa-chii-wá', 'english': 'Right Livelihood', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาวายามะ', 'paiboon': 'sǎm-maa-waa-yaa-má', 'english': 'Right Effort', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาสติ', 'paiboon': 'sǎm-maa-sà-dtì', 'english': 'Right Mindfulness', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'สัมมาสมาธิ', 'paiboon': 'sǎm-maa-sà-maa-tí', 'english': 'Right Concentration', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'วิปัสสนา', 'paiboon': 'wí-bpàt-sà-naa', 'english': 'Insight (Vipassana)', 'category': 'theravada_dhamma', 'formality': 'formal'},
        {'thai': 'เมตตา', 'paiboon': 'mâyt-dtaa', 'english': 'Loving-kindness (Metta)', 'category': 'theravada_dhamma', 'formality': 'formal'},
    ],
    
    'everyday': [
        {'thai': 'สวัสดี', 'paiboon': 'sà-wàt-dii', 'english': 'Hello/Goodbye', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ขอบคุณ', 'paiboon': 'kɔ̀ɔp kun', 'english': 'Thank you', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ขอโทษ', 'paiboon': 'kɔ̌ɔ tôot', 'english': 'Sorry/Excuse me', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ใช่', 'paiboon': 'châi', 'english': 'Yes', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ไม่ใช่', 'paiboon': 'mâi châi', 'english': 'No (not so)', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ไม่เป็นไร', 'paiboon': 'mâi bpen rai', 'english': "It's okay", 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เท่าไหร่', 'paiboon': 'tâo rài', 'english': 'How much?', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'อร่อย', 'paiboon': 'à-ròi', 'english': 'Delicious', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ร้อน', 'paiboon': 'rɔ́ɔn', 'english': 'Hot', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เย็น', 'paiboon': 'yen', 'english': 'Cold/Cool', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'น้ำ', 'paiboon': 'náam', 'english': 'Water', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ข้าว', 'paiboon': 'kâao', 'english': 'Rice/Food', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'บ้าน', 'paiboon': 'bâan', 'english': 'House/Home', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'รถ', 'paiboon': 'rót', 'english': 'Car/Vehicle', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'คน', 'paiboon': 'kon', 'english': 'Person', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เงิน', 'paiboon': 'ŋəən', 'english': 'Money', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'วันนี้', 'paiboon': 'wan níi', 'english': 'Today', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'พรุ่งนี้', 'paiboon': 'prûŋ níi', 'english': 'Tomorrow', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'เมื่อวาน', 'paiboon': 'mʉ̂a waan', 'english': 'Yesterday', 'category': 'everyday', 'formality': 'neutral'},
        {'thai': 'ตอนนี้', 'paiboon': 'dtɔɔn níi', 'english': 'Now', 'category': 'everyday', 'formality': 'neutral'},
    ],
}


# ============================================
# THAI ALPHABET - COMPLETE SYSTEM
# ============================================

THAI_ALPHABET = {
    'consonants': {
        'title': 'Thai Consonants (พยัญชนะ)',
        'description': 'There are 44 consonant letters in Thai, representing 21 distinct sounds.',
        'groups': {
            'middle_class': {
                'name': 'Middle Class Consonants (อักษรกลาง)',
                'description': 'Used with mid tone, 9 consonants',
                'letters': [
                    {'thai': 'ก', 'paiboon': 'g', 'name': 'gɔɔ gài', 'meaning': 'chicken', 'example': {'thai': 'กา', 'paiboon': 'gaa', 'english': 'crow'}},
                    {'thai': 'จ', 'paiboon': 'j', 'name': 'jɔɔ jaan', 'meaning': 'plate', 'example': {'thai': 'จาน', 'paiboon': 'jaan', 'english': 'plate'}},
                    {'thai': 'ฎ', 'paiboon': 'd', 'name': 'dɔɔ chá-daa', 'meaning': 'headdress', 'example': {'thai': 'ชฎา', 'paiboon': 'chá-daa', 'english': 'headdress'}},
                    {'thai': 'ฏ', 'paiboon': 'dt', 'name': 'dtɔɔ bpà-dtàk', 'meaning': 'goad', 'example': {'thai': 'ปฏัก', 'paiboon': 'bpà-dtàk', 'english': 'goad'}},
                    {'thai': 'ด', 'paiboon': 'd', 'name': 'dɔɔ dèk', 'meaning': 'child', 'example': {'thai': 'เด็ก', 'paiboon': 'dèk', 'english': 'child'}},
                    {'thai': 'ต', 'paiboon': 'dt', 'name': 'dtɔɔ dtào', 'meaning': 'turtle', 'example': {'thai': 'เต่า', 'paiboon': 'dtào', 'english': 'turtle'}},
                    {'thai': 'บ', 'paiboon': 'b', 'name': 'bɔɔ bai-máai', 'meaning': 'leaf', 'example': {'thai': 'ใบไม้', 'paiboon': 'bai máai', 'english': 'leaf'}},
                    {'thai': 'ป', 'paiboon': 'bp', 'name': 'bpɔɔ bplaa', 'meaning': 'fish', 'example': {'thai': 'ปลา', 'paiboon': 'bplaa', 'english': 'fish'}},
                    {'thai': 'อ', 'paiboon': '', 'name': 'ɔɔ àang', 'meaning': 'basin', 'example': {'thai': 'อ่าง', 'paiboon': 'àang', 'english': 'basin'}},
                ]
            },
            'high_class': {
                'name': 'High Class Consonants (อักษรสูง)',
                'description': 'Used with rising tone, 11 consonants',
                'letters': [
                    {'thai': 'ข', 'paiboon': 'k', 'name': 'kɔ̌ɔ kài', 'meaning': 'egg', 'example': {'thai': 'ไข่', 'paiboon': 'kài', 'english': 'egg'}},
                    {'thai': 'ฃ', 'paiboon': 'k', 'name': 'kɔ̌ɔ kùat', 'meaning': 'bottle', 'example': {'thai': 'ขวด', 'paiboon': 'kùat', 'english': 'bottle'}},
                    {'thai': 'ฉ', 'paiboon': 'ch', 'name': 'chɔ̌ɔ chíng', 'meaning': 'cymbal', 'example': {'thai': 'ฉิ่ง', 'paiboon': 'chìng', 'english': 'cymbal'}},
                    {'thai': 'ฐ', 'paiboon': 't', 'name': 'tɔ̌ɔ tǎan', 'meaning': 'base', 'example': {'thai': 'ฐาน', 'paiboon': 'tǎan', 'english': 'base'}},
                    {'thai': 'ถ', 'paiboon': 't', 'name': 'tɔ̌ɔ tǔng', 'meaning': 'bag', 'example': {'thai': 'ถุง', 'paiboon': 'tǔng', 'english': 'bag'}},
                    {'thai': 'ผ', 'paiboon': 'p', 'name': 'pɔ̌ɔ pʉ̌ng', 'meaning': 'bee', 'example': {'thai': 'ผึ้ง', 'paiboon': 'pʉ̂ng', 'english': 'bee'}},
                    {'thai': 'ฝ', 'paiboon': 'f', 'name': 'fɔ̌ɔ fǎa', 'meaning': 'lid', 'example': {'thai': 'ฝา', 'paiboon': 'fǎa', 'english': 'lid'}},
                    {'thai': 'ศ', 'paiboon': 's', 'name': 'sɔ̌ɔ sǎa-laa', 'meaning': 'pavilion', 'example': {'thai': 'ศาลา', 'paiboon': 'sǎa-laa', 'english': 'pavilion'}},
                    {'thai': 'ษ', 'paiboon': 's', 'name': 'sɔ̌ɔ rʉ̌-sǐi', 'meaning': 'hermit', 'example': {'thai': 'ฤๅษี', 'paiboon': 'rʉ-sǐi', 'english': 'hermit'}},
                    {'thai': 'ส', 'paiboon': 's', 'name': 'sɔ̌ɔ sʉ̌a', 'meaning': 'tiger', 'example': {'thai': 'เสือ', 'paiboon': 'sʉ̌a', 'english': 'tiger'}},
                    {'thai': 'ห', 'paiboon': 'h', 'name': 'hɔ̌ɔ hìip', 'meaning': 'chest', 'example': {'thai': 'หีบ', 'paiboon': 'hìip', 'english': 'chest'}},
                ]
            },
            'low_class': {
                'name': 'Low Class Consonants (อักษรต่ำ)',
                'description': 'Used with low/falling tone, 24 consonants',
                'letters': [
                    {'thai': 'ค', 'paiboon': 'k', 'name': 'kɔɔ kwai', 'meaning': 'buffalo', 'example': {'thai': 'ควาย', 'paiboon': 'kwaai', 'english': 'buffalo'}},
                    {'thai': 'ฅ', 'paiboon': 'k', 'name': 'kɔɔ kon', 'meaning': 'person', 'example': {'thai': 'คน', 'paiboon': 'kon', 'english': 'person'}},
                    {'thai': 'ฆ', 'paiboon': 'k', 'name': 'kɔɔ rá-kaang', 'meaning': 'bell', 'example': {'thai': 'ระฆัง', 'paiboon': 'rá-kaang', 'english': 'bell'}},
                    {'thai': 'ง', 'paiboon': 'ng', 'name': 'ngɔɔ nguu', 'meaning': 'snake', 'example': {'thai': 'งู', 'paiboon': 'nguu', 'english': 'snake'}},
                    {'thai': 'ช', 'paiboon': 'ch', 'name': 'chɔɔ cháang', 'meaning': 'elephant', 'example': {'thai': 'ช้าง', 'paiboon': 'cháang', 'english': 'elephant'}},
                    {'thai': 'ซ', 'paiboon': 's', 'name': 'sɔɔ sôo', 'meaning': 'chain', 'example': {'thai': 'โซ่', 'paiboon': 'sôo', 'english': 'chain'}},
                    {'thai': 'ฌ', 'paiboon': 'ch', 'name': 'chɔɔ chəə', 'meaning': 'tree', 'example': {'thai': 'เฌอ', 'paiboon': 'chəə', 'english': 'tree'}},
                    {'thai': 'ญ', 'paiboon': 'y', 'name': 'yɔɔ yǐng', 'meaning': 'woman', 'example': {'thai': 'หญิง', 'paiboon': 'yǐng', 'english': 'woman'}},
                    {'thai': 'ฑ', 'paiboon': 't', 'name': 'tɔɔ mon-too', 'meaning': 'Montho', 'example': {'thai': 'มณโฑ', 'paiboon': 'mon-too', 'english': 'Montho'}},
                    {'thai': 'ฒ', 'paiboon': 't', 'name': 'tɔɔ pûu-tâo', 'meaning': 'elder', 'example': {'thai': 'ผู้เฒ่า', 'paiboon': 'pûu-tâo', 'english': 'elder'}},
                    {'thai': 'ณ', 'paiboon': 'n', 'name': 'nɔɔ neen', 'meaning': 'novice monk', 'example': {'thai': 'เณร', 'paiboon': 'neen', 'english': 'novice monk'}},
                    {'thai': 'ท', 'paiboon': 't', 'name': 'tɔɔ tá-hǎan', 'meaning': 'soldier', 'example': {'thai': 'ทหาร', 'paiboon': 'tá-hǎan', 'english': 'soldier'}},
                    {'thai': 'ธ', 'paiboon': 't', 'name': 'tɔɔ tong', 'meaning': 'flag', 'example': {'thai': 'ธง', 'paiboon': 'tong', 'english': 'flag'}},
                    {'thai': 'น', 'paiboon': 'n', 'name': 'nɔɔ nǔu', 'meaning': 'mouse', 'example': {'thai': 'หนู', 'paiboon': 'nǔu', 'english': 'mouse'}},
                    {'thai': 'พ', 'paiboon': 'p', 'name': 'pɔɔ paan', 'meaning': 'tray', 'example': {'thai': 'พาน', 'paiboon': 'paan', 'english': 'tray'}},
                    {'thai': 'ฟ', 'paiboon': 'f', 'name': 'fɔɔ fan', 'meaning': 'tooth', 'example': {'thai': 'ฟัน', 'paiboon': 'fan', 'english': 'tooth'}},
                    {'thai': 'ภ', 'paiboon': 'p', 'name': 'pɔɔ sǎm-pao', 'meaning': 'sailboat', 'example': {'thai': 'สำเภา', 'paiboon': 'sǎm-pao', 'english': 'sailboat'}},
                    {'thai': 'ม', 'paiboon': 'm', 'name': 'mɔɔ máa', 'meaning': 'horse', 'example': {'thai': 'ม้า', 'paiboon': 'máa', 'english': 'horse'}},
                    {'thai': 'ย', 'paiboon': 'y', 'name': 'yɔɔ yák', 'meaning': 'giant', 'example': {'thai': 'ยักษ์', 'paiboon': 'yák', 'english': 'giant'}},
                    {'thai': 'ร', 'paiboon': 'r', 'name': 'rɔɔ rʉa', 'meaning': 'boat', 'example': {'thai': 'เรือ', 'paiboon': 'rʉa', 'english': 'boat'}},
                    {'thai': 'ล', 'paiboon': 'l', 'name': 'lɔɔ ling', 'meaning': 'monkey', 'example': {'thai': 'ลิง', 'paiboon': 'ling', 'english': 'monkey'}},
                    {'thai': 'ว', 'paiboon': 'w', 'name': 'wɔɔ wɛ̌ɛn', 'meaning': 'ring', 'example': {'thai': 'แหวน', 'paiboon': 'wɛ̌ɛn', 'english': 'ring'}},
                    {'thai': 'ฬ', 'paiboon': 'l', 'name': 'lɔɔ jù-laa', 'meaning': 'kite', 'example': {'thai': 'จุฬา', 'paiboon': 'jù-laa', 'english': 'kite'}},
                    {'thai': 'ฮ', 'paiboon': 'h', 'name': 'hɔɔ nók-hûuk', 'meaning': 'owl', 'example': {'thai': 'นกฮูก', 'paiboon': 'nók-hûuk', 'english': 'owl'}},
                ]
            }
        }
    },
    
    'vowels': {
        'title': 'Thai Vowels (สระ)',
        'description': 'Thai has 32 vowel forms (including combinations) representing 18 distinct vowel sounds.',
        'short_vowels': [
            {'thai': 'อะ', 'paiboon': 'à', 'example': {'thai': 'กะ', 'paiboon': 'gà'}},
            {'thai': 'อิ', 'paiboon': 'ì', 'example': {'thai': 'กิ', 'paiboon': 'gì'}},
            {'thai': 'อึ', 'paiboon': 'ʉ̀', 'example': {'thai': 'กึ', 'paiboon': 'gʉ̀'}},
            {'thai': 'อุ', 'paiboon': 'ù', 'example': {'thai': 'กุ', 'paiboon': 'gù'}},
            {'thai': 'เอะ', 'paiboon': 'è', 'example': {'thai': 'เกะ', 'paiboon': 'gè'}},
            {'thai': 'แอะ', 'paiboon': 'ɛ̀', 'example': {'thai': 'แกะ', 'paiboon': 'gɛ̀'}},
            {'thai': 'โอะ', 'paiboon': 'ò', 'example': {'thai': 'โกะ', 'paiboon': 'gò'}},
            {'thai': 'เอาะ', 'paiboon': 'ɔ̀', 'example': {'thai': 'เกาะ', 'paiboon': 'gɔ̀'}},
            {'thai': 'เอิ', 'paiboon': 'ə̀', 'example': {'thai': 'เกิ', 'paiboon': 'gə̀'}},
        ],
        'long_vowels': [
            {'thai': 'อา', 'paiboon': 'aa', 'example': {'thai': 'กา', 'paiboon': 'gaa', 'english': 'crow'}},
            {'thai': 'อี', 'paiboon': 'ii', 'example': {'thai': 'กี', 'paiboon': 'gii'}},
            {'thai': 'อือ', 'paiboon': 'ʉʉ', 'example': {'thai': 'กือ', 'paiboon': 'gʉʉ'}},
            {'thai': 'อู', 'paiboon': 'uu', 'example': {'thai': 'กู', 'paiboon': 'guu'}},
            {'thai': 'เอ', 'paiboon': 'ee', 'example': {'thai': 'เก', 'paiboon': 'gee'}},
            {'thai': 'แอ', 'paiboon': 'ɛɛ', 'example': {'thai': 'แก', 'paiboon': 'gɛɛ'}},
            {'thai': 'โอ', 'paiboon': 'oo', 'example': {'thai': 'โก', 'paiboon': 'goo'}},
            {'thai': 'ออ', 'paiboon': 'ɔɔ', 'example': {'thai': 'กอ', 'paiboon': 'gɔɔ'}},
            {'thai': 'เออ', 'paiboon': 'əə', 'example': {'thai': 'เกอ', 'paiboon': 'gəə'}},
        ],
    },
    
    'tone_marks': {
        'title': 'Tone Marks (วรรณยุกต์)',
        'description': 'Thai has 4 tone marks that modify the inherent tone.',
        'marks': [
            {'symbol': '่', 'name': 'mái èek', 'paiboon': 'falling (à)', 'example': {'thai': 'ก่า', 'paiboon': 'gàa'}},
            {'symbol': '้', 'name': 'mái tôo', 'paiboon': 'high (â)', 'example': {'thai': 'ก้า', 'paiboon': 'gâa'}},
            {'symbol': '๊', 'name': 'mái dtrii', 'paiboon': 'low (ǎ)', 'example': {'thai': 'ก๊า', 'paiboon': 'gǎa'}},
            {'symbol': '๋', 'name': 'mái jàt-dtà-waa', 'paiboon': 'rising (ǎ)', 'example': {'thai': 'ก๋า', 'paiboon': 'gǎa'}},
        ]
    },
    
    'special_characters': {
        'title': 'Special Characters',
        'characters': [
            {'symbol': 'ๆ', 'name': 'mai yamok', 'use': 'Repetition mark', 'example': {'thai': 'เด็กๆ', 'paiboon': 'dèk dèk', 'english': 'children'}},
            {'symbol': '์', 'name': 'gaaran', 'use': 'Silent letter marker', 'example': {'thai': 'จันทร์', 'paiboon': 'jan', 'english': 'moon'}},
            {'symbol': 'ฯ', 'name': 'paiyannoi', 'use': 'Abbreviation mark', 'example': {'thai': 'กทม.', 'paiboon': 'Bangkok', 'english': 'Bangkok'}},
        ]
    }
}

# Spacing fix function
def fix_romanization_spacing(text):
    """Fix spacing issues in Paiboon romanization"""
    if not text:
        return text
    
    # Already has good spacing - don't mess with it
    if ' ' in text and not '  ' in text:
        return text
    
    # Common patterns that need spacing
    replacements = {
        '  ': ' ',
        '   ': ' ',
        'kráp': 'kráp ',
        'kâ': 'kâ ',
        'ká': 'ká ',
        'sà-wàt-diikráp': 'sà-wàt-dii kráp',
        'sà-wàt-diikâ': 'sà-wàt-dii kâ',
        'kɔ̀ɔp-kunkráp': 'kɔ̀ɔp-kun kráp',
        'kɔ̀ɔp-kunkâ': 'kɔ̀ɔp-kun kâ',
    }
    
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    
    # Trim extra spaces
    result = ' '.join(result.split())
    
    return result

# Alphabet completion tracking
def check_alphabet_completion():
    """Check if user has completed Thai alphabet"""
    init_user_progress()
    user = session['user_progress']
    return user.get('alphabet_completed', False)

def mark_alphabet_complete():
    """Mark alphabet as completed"""
    init_user_progress()
    user = session['user_progress']
    
    if not user.get('alphabet_completed', False):
        user['alphabet_completed'] = True
        user['alphabet_completion_date'] = datetime.now().isoformat()
        
        # Award XP for completion
        add_xp(100, 'Completed Thai Alphabet')
        
        session.modified = True
        return True
    return False


# ============================================
# THERAVADA TEACHINGS
# ============================================

THERAVADA_TEACHINGS = {
    'key_suttas': [
        {
            'pali': 'Dhammacakkappavattana Sutta',
            'thai': 'ธัมมจักกัปปวัตตนสูตร',
            'english': 'Setting the Wheel of Dhamma in Motion',
            'description': "The Buddha's first sermon containing the Four Noble Truths and Middle Way.",
            'key_teaching': 'Avoid extremes. Follow the Middle Way to wisdom and Nibbana.'
        },
        {
            'pali': 'Satipatthana Sutta',
            'thai': 'สติปัฏฐานสูตร',
            'english': 'Foundations of Mindfulness',
            'description': 'The most important discourse on meditation practice.',
            'key_teaching': 'Mindfulness of body, feelings, mind, and mental objects is the direct path.'
        },
        {
            'pali': 'Anapanasati Sutta',
            'thai': 'อานาปานสติสูตร',
            'english': 'Mindfulness of Breathing',
            'description': 'Detailed instructions on breath meditation.',
            'key_teaching': 'Through mindful breathing, develop both calm and insight.'
        },
        {
            'pali': 'Metta Sutta',
            'thai': 'เมตตสูตร',
            'english': 'Discourse on Loving-Kindness',
            'description': 'Instructions on developing universal loving-kindness.',
            'key_teaching': 'May all beings be happy, free from enmity and anxiety.'
        },
        {
            'pali': 'Mangala Sutta',
            'thai': 'มงคลสูตร',
            'english': 'Discourse on Blessings',
            'description': 'The Buddha describes 38 highest blessings.',
            'key_teaching': 'True blessings: not associating with fools, honoring the wise.'
        },
        {
            'pali': 'Karaniya Metta Sutta',
            'thai': 'กรณียเมตตสูตร',
            'english': 'Hymn of Universal Love',
            'description': 'Beautiful verses on cultivating boundless loving-kindness.',
            'key_teaching': 'As a mother protects her child, cultivate boundless love.'
        },
    ],
    
    'key_abhidhamma': [
        {
            'topic': 'Citta (Consciousness)',
            'thai': 'จิต',
            'description': '89 or 121 types of consciousness classified by ethical quality.',
            'practical': 'Understanding moment-to-moment arising develops insight into impermanence.'
        },
        {
            'topic': 'Cetasika (Mental Factors)',
            'thai': 'เจตสิก',
            'description': '52 mental factors including feeling, perception, and volition.',
            'practical': 'Recognizing mental factors helps identify wholesome and unwholesome states.'
        },
        {
            'topic': 'Rupa (Matter)',
            'thai': 'รูป',
            'description': '28 types of material phenomena including the four elements.',
            'practical': 'Contemplating elements reduces attachment to physical form.'
        },
        {
            'topic': 'Nibbana',
            'thai': 'นิพพาน',
            'description': 'The unconditioned element, cessation of suffering.',
            'practical': 'Nibbana is realized through developing the Noble Eightfold Path.'
        },
    ],
    
    'key_vinaya': [
        {
            'rule': 'Patimokkha',
            'thai': 'ปาฏิโมกข์',
            'english': 'Monastic Code',
            'description': '227 rules for bhikkhus, 311 for bhikkhunis.',
            'significance': 'Recited fortnightly. Foundation of monastic discipline.'
        },
        {
            'rule': 'Four Parajikas',
            'thai': 'ปาราชิก',
            'english': 'Defeats (Expulsion Offenses)',
            'description': 'Sexual intercourse, theft, killing, false claims.',
            'significance': 'Breaking these results in automatic expulsion.'
        },
        {
            'rule': 'Kathina',
            'thai': 'กฐิน',
            'english': 'Robe-Offering Ceremony',
            'description': 'Annual ceremony where lay supporters offer cloth.',
            'significance': 'Important merit-making opportunity.'
        },
    ],
}


# ============================================
# MEDITATION TECHNIQUES
# ============================================

MEDITATION_TECHNIQUES = {
    'samatha': {
        'name': 'Samatha (Calm/Concentration)',
        'thai': 'สมถะ',
        'paiboon': 'sà-má-tà',
        'description': 'Concentration meditation leading to deep absorption (jhana).',
        'techniques': [
            {
                'name': 'Anapanasati (Breath Meditation)',
                'thai': 'อานาปานสติ',
                'instructions': [
                    'Sit comfortably with spine straight',
                    'Close eyes gently',
                    'Bring attention to breath at nostrils',
                    'Note sensation of air entering and leaving',
                    'When mind wanders, gently return',
                    'Do not control breath, just observe',
                ],
                'benefits': 'Develops concentration, calms mind'
            },
            {
                'name': 'Buddhanussati (Recollection of Buddha)',
                'thai': 'พุทธานุสติ',
                'instructions': [
                    'Settle into comfortable posture',
                    'Bring to mind qualities of the Buddha',
                    'Recite internally: "Buddho" with each breath',
                    'Feel gratitude arising',
                    'Let mind rest in this recollection',
                ],
                'benefits': 'Develops faith, joy, concentration'
            },
            {
                'name': 'Metta Bhavana (Loving-Kindness)',
                'thai': 'เมตตาภาวนา',
                'instructions': [
                    'Generate loving-kindness towards yourself',
                    'Repeat: "May I be happy, free from suffering"',
                    'Extend to loved ones, then neutral people',
                    'Gradually extend to difficult people',
                    'Finally extend to all beings everywhere',
                ],
                'benefits': 'Overcomes ill-will, develops compassion'
            },
        ]
    },
    'vipassana': {
        'name': 'Vipassana (Insight Meditation)',
        'thai': 'วิปัสสนา',
        'paiboon': 'wí-bpàt-sà-naa',
        'description': 'Insight meditation seeing impermanence, suffering, non-self.',
        'techniques': [
            {
'name': 'Kayanupassana (Contemplation of Body)',
                'thai': 'กายานุปัสสนา',
                'instructions': [
                    'After establishing concentration',
                    'Notice physical sensations',
                    'Label: pleasant, unpleasant, or neutral',
                    'Observe how sensations arise and pass',
                    'Notice impermanent nature of the body',
                ],
                'benefits': 'Insight into the nature of the physical form'
            },
            {
                'name': 'Vedananupassana (Contemplation of Feelings)',
                'thai': 'เวทนานุปัสสนา',
                'instructions': [
                    'After establishing concentration',
                    'Notice feeling tone of each experience',
                    'Label: pleasant, unpleasant, or neutral',
                    'Observe how feelings arise and pass',
                    'Notice impermanent nature of all feelings',
                ],
                'benefits': 'Insight into arising and passing'
            },
            {
                'name': 'Cittanupassana (Contemplation of Mind)',
                'thai': 'จิตตานุปัสสนา',
                'instructions': [
                    'Observe the state of your mind',
                    'Note: Is there desire? Aversion? Delusion?',
                    'Is mind concentrated or scattered?',
                    'Simply observe without judgment',
                    'Notice how mental states change',
                ],
                'benefits': 'Understanding nature of consciousness'
            },
            {
                'name': 'Dhammanupassana (Contemplation of Dhammas)',
                'thai': 'ธัมมานุปัสสนา',
                'instructions': [
                    'Observe mental phenomena as they arise',
                    'Identify Five Hindrances when present',
                    'Notice arising and passing of thoughts',
                    'See all phenomena as "not-self"',
                    'Rest in awareness itself',
                ],
                'benefits': 'Direct insight into reality'
            },
        ]
    },
    'body_scan': {
        'name': 'Body Scan Meditation',
        'thai': 'การสแกนร่างกาย',
        'paiboon': 'gaan sà-gɛɛn râang-gaai',
        'description': (
            "A body scan is a foundational mindfulness practice that can be very helpful for developing body awareness and relaxation. "
            "Here's a step-by-step guide on how to do a basic body scan:"
        ),
        'steps': [
            {'number': 1,  'title': 'Posture',              'detail': 'Sit comfortably or lie down in a relaxed position. Close your eyes if it feels comfortable.'},
            {'number': 2,  'title': 'Set intention',        'detail': 'Take a few deep breaths and set an intention to be present with your body sensations.'},
            {'number': 3,  'title': 'Ground yourself',      'detail': 'Notice the points of contact between your body and the surface supporting you.'},
            {'number': 4,  'title': 'Start at the feet',    'detail': 'Bring your attention to your toes, then the soles of your feet, then the tops of your feet.'},
            {'number': 5,  'title': 'Move up slowly',       'detail': 'Gradually move your attention up through your body: Ankles, Calves, Knees, Thighs, Hips, Lower back, Abdomen, Chest, Upper back, Shoulders, Arms, Hands, Neck, Face, Scalp.'},
            {'number': 6,  'title': 'For each area',        'detail': 'Notice any sensations present (e.g., warmth, coolness, tingling, pressure). If there\'s no sensation, simply note the absence of sensation. Don\'t try to change anything, just observe.'},
            {'number': 7,  'title': 'Breath awareness',     'detail': 'You can use your breath as an anchor, returning to it between each body part.'},
            {'number': 8,  'title': 'Whole body awareness', 'detail': 'After scanning individual parts, try to hold an awareness of your entire body as a whole.'},
            {'number': 9,  'title': 'Ending the practice',  'detail': 'Slowly open your eyes and take a moment to notice how you feel.'},
        ],
        'tips': [
            'Start with short sessions (5-10 minutes) and gradually increase duration.',
            "If your mind wanders, gently bring it back to the body part you were focusing on.",
            'Don\'t worry about "doing it right" - the practice is about cultivating awareness, not achieving a particular state.',
        ],
        'closing': (
            "Remember, like any skill, body scanning improves with regular practice. "
            "It's normal for your mind to wander or to have difficulty feeling sensations in some areas at first. "
            "With time, your body awareness will likely become more refined."
        ),
        'body_areas': ['Ankles', 'Calves', 'Knees', 'Thighs', 'Hips', 'Lower back', 'Abdomen', 'Chest', 'Upper back', 'Shoulders', 'Arms', 'Hands', 'Neck', 'Face', 'Scalp'],
        'duration_minutes': 20,
        'phases': [
            {'name': 'Grounding',            'duration': 3,  'instruction': 'Lie down or sit comfortably. Notice the points of contact between your body and the surface supporting you.'},
            {'name': 'Scanning',             'duration': 14, 'instruction': 'Move attention slowly upward through the body, from feet to scalp. At each area, simply notice whatever is present.'},
            {'name': 'Whole Body Awareness', 'duration': 3,  'instruction': 'After scanning all parts, expand awareness to hold the entire body as a whole. Rest here.'},
        ],
    }
}


# ============================================
# GRAMMAR - COMPREHENSIVE GUIDE
# ============================================

GRAMMAR = {
    'parts_of_speech': [
        {
            'name': 'Nouns (คำนาม)',
            'thai': 'คำนาม',
            'paiboon': 'kam naam',
            'explanation': 'Thai nouns have no gender, number, or articles.',
            'examples': [
                {'thai': 'หมา', 'paiboon': 'mǎa', 'english': 'dog/dogs'},
                {'thai': 'บ้าน', 'paiboon': 'bâan', 'english': 'house/houses'},
            ]
        },
        {
            'name': 'Pronouns (คำสรรพนาม)',
            'thai': 'คำสรรพนาม',
            'paiboon': 'kam sàp-pá-naam',
            'explanation': 'Thai pronouns are MUCH more complex than English. They change based on: (1) Speaker gender, (2) Formality level, (3) Relationship to listener, (4) Social hierarchy. Understanding pronouns is ESSENTIAL for appropriate Thai communication.',
            'note': 'Visit the Gender Guide page for personalized examples based on YOUR gender!',
            
            'first_person': {
                'title': 'First Person: "I" / "We"',
                'explanation': 'The word for "I" reveals your gender, formality, and social awareness. Choose carefully!',
                'pronouns': [
                    {
                        'category': 'Male Speaker - Polite/Formal',
                        'entries': [
                            {'thai': 'ผม', 'paiboon': 'pǒm', 'formality': 'polite', 'context': 'Standard polite form for males', 'usage': 'Use in most situations'},
                            {'thai': 'กระผม', 'paiboon': 'grà-pǒm', 'formality': 'royal', 'context': 'Very formal, to royalty or monks', 'usage': 'Rare, very respectful'},
                        ]
                    },
                    {
                        'category': 'Female Speaker - Polite/Formal',
                        'entries': [
                            {'thai': 'ดิฉัน', 'paiboon': 'dì-chǎn', 'formality': 'formal', 'context': 'Formal/polite form for females', 'usage': 'Professional, formal settings'},
                            {'thai': 'ฉัน', 'paiboon': 'chǎn', 'formality': 'neutral', 'context': 'Casual form for females', 'usage': 'Friends, informal settings'},
                        ]
                    },
                    {
                        'category': 'Gender-Neutral / Casual',
                        'entries': [
                            {'thai': 'ฉัน', 'paiboon': 'chǎn', 'formality': 'neutral', 'context': 'Informal, friendly', 'usage': 'Common among women and young people'},
                            {'thai': 'กู', 'paiboon': 'guu', 'formality': 'vulgar', 'context': 'Very casual, close friends only', 'usage': 'Can be rude with strangers'},
                            {'thai': 'เรา', 'paiboon': 'rao', 'formality': 'casual', 'context': 'Casual "I" or "we"', 'usage': 'Informal, friendly'},
                        ]
                    },
                    {
                        'category': 'Royal / Monastic',
                        'entries': [
                            {'thai': 'ข้าพระพุทธเจ้า', 'paiboon': 'kâa prá-pút-tá-jâo', 'formality': 'monastic', 'context': 'To Buddha, in prayer', 'usage': 'Buddhist formal context'},
                            {'thai': 'ข้าพเจ้า', 'paiboon': 'kâa-pá-jâo', 'formality': 'royal', 'context': 'To royalty', 'usage': 'Royal protocol only'},
                        ]
                    },
                    {
                        'category': 'Plural: "We"',
                        'entries': [
                            {'thai': 'เรา', 'paiboon': 'rao', 'formality': 'neutral', 'context': 'We (informal)', 'usage': 'Common plural form'},
                            {'thai': 'พวกเรา', 'paiboon': 'pûuak rao', 'formality': 'neutral', 'context': 'We (emphasizing group)', 'usage': 'Our group/us'},
                            {'thai': 'พวกผม', 'paiboon': 'pûuak pǒm', 'formality': 'polite', 'context': 'We (male speaker, polite)', 'usage': 'Professional settings'},
                            {'thai': 'พวกดิฉัน', 'paiboon': 'pûuak dì-chǎn', 'formality': 'formal', 'context': 'We (female speaker, formal)', 'usage': 'Formal settings'},
                        ]
                    }
                ]
            },
            
            'second_person': {
                'title': 'Second Person: "You"',
                'explanation': 'Thai has MANY words for "you" - choosing the right one shows respect and awareness of social context.',
                'pronouns': [
                    {
                        'category': 'Polite / Formal',
                        'entries': [
                            {'thai': 'คุณ', 'paiboon': 'kun', 'formality': 'polite', 'context': 'Standard polite "you"', 'usage': 'Safe default for strangers'},
                            {'thai': 'ท่าน', 'paiboon': 'tân', 'formality': 'formal', 'context': 'Very respectful', 'usage': 'Elders, authority figures'},
                            {'thai': 'พี่', 'paiboon': 'pîi', 'formality': 'neutral', 'context': 'Older sibling/person', 'usage': 'Anyone slightly older'},
                            {'thai': 'น้อง', 'paiboon': 'nɔ́ɔŋ', 'formality': 'neutral', 'context': 'Younger sibling/person', 'usage': 'Anyone younger'},
                        ]
                    },
                    {
                        'category': 'Informal / Casual',
                        'entries': [
                            {'thai': 'เธอ', 'paiboon': 'təə', 'formality': 'casual', 'context': 'Casual "you"', 'usage': 'Friends, equals'},
                            {'thai': 'มึง', 'paiboon': 'mʉŋ', 'formality': 'vulgar', 'context': 'Very casual, close friends', 'usage': 'Can be rude/offensive'},
                            {'thai': 'แก', 'paiboon': 'gɛɛ', 'formality': 'vulgar', 'context': 'Casual/rude', 'usage': 'Close friends or insulting'},
                        ]
                    },
                    {
                        'category': 'By Name/Title',
                        'entries': [
                            {'thai': 'คุณ + name', 'paiboon': 'kun + name', 'formality': 'polite', 'context': 'Polite address', 'usage': 'Kun John, Kun Mary'},
                            {'thai': 'พี่ + name', 'paiboon': 'pîi + name', 'formality': 'friendly', 'context': 'Older person', 'usage': 'Pii John'},
                            {'thai': 'น้อง + name', 'paiboon': 'nɔ́ɔŋ + name', 'formality': 'friendly', 'context': 'Younger person', 'usage': 'Nong Mary'},
                        ]
                    },
                    {
                        'category': 'Plural: "You all"',
                        'entries': [
                            {'thai': 'พวกคุณ', 'paiboon': 'pûuak kun', 'formality': 'polite', 'context': 'You (plural, polite)', 'usage': 'You all (polite)'},
                            {'thai': 'พวกเธอ', 'paiboon': 'pûuak təə', 'formality': 'casual', 'context': 'You (plural, casual)', 'usage': 'You guys'},
                        ]
                    }
                ]
            },
            
            'third_person': {
                'title': 'Third Person: "He" / "She" / "They" / "It"',
                'explanation': 'Thai does NOT distinguish he/she in most pronouns. Gender-neutral is the norm!',
                'pronouns': [
                    {
                        'category': 'People - Gender Neutral',
                        'entries': [
                            {'thai': 'เขา', 'paiboon': 'kǎo', 'formality': 'neutral', 'context': 'He/She/They', 'usage': 'Most common third person'},
                            {'thai': 'ท่าน', 'paiboon': 'tân', 'formality': 'formal', 'context': 'He/She (respectful)', 'usage': 'For respected persons'},
                            {'thai': 'คนนั้น', 'paiboon': 'kon nán', 'formality': 'neutral', 'context': 'That person', 'usage': 'Neutral, descriptive'},
                        ]
                    },
                    {
                        'category': 'People - Kinship Terms',
                        'entries': [
                            {'thai': 'พี่', 'paiboon': 'pîi', 'formality': 'neutral', 'context': 'Older person', 'usage': 'Older sibling/person'},
                            {'thai': 'น้อง', 'paiboon': 'nɔ́ɔŋ', 'formality': 'neutral', 'context': 'Younger person', 'usage': 'Younger sibling/person'},
                            {'thai': 'เพื่อน', 'paiboon': 'pʉ̂an', 'formality': 'neutral', 'context': 'Friend', 'usage': 'My/our friend'},
                        ]
                    },
                    {
                        'category': 'Objects / Animals - "It"',
                        'entries': [
                            {'thai': 'มัน', 'paiboon': 'man', 'formality': 'neutral', 'context': 'It (animals, objects)', 'usage': 'Not for humans'},
                            {'thai': 'ตัว', 'paiboon': 'dtuua', 'formality': 'neutral', 'context': 'It (animals)', 'usage': 'Specific animal'},
                            {'thai': 'อัน', 'paiboon': 'an', 'formality': 'neutral', 'context': 'It (objects)', 'usage': 'Specific object'},
                        ]
                    },
                    {
                        'category': 'Plural - "They"',
                        'entries': [
                            {'thai': 'พวกเขา', 'paiboon': 'pûuak kǎo', 'formality': 'neutral', 'context': 'They (people)', 'usage': 'Group of people'},
                            {'thai': 'เขาเหล่านั้น', 'paiboon': 'kǎo làu nán', 'formality': 'formal', 'context': 'Those people', 'usage': 'Formal plural'},
                            {'thai': 'พวกมัน', 'paiboon': 'pûuak man', 'formality': 'neutral', 'context': 'They (animals/objects)', 'usage': 'Group of things'},
                        ]
                    },
                    {
                        'category': 'Gender-Specific (Rare/Informal)',
                        'entries': [
                            {'thai': 'ผู้ชาย', 'paiboon': 'pûu-chaai', 'formality': 'neutral', 'context': 'That man', 'usage': 'Descriptive, not pronoun'},
                            {'thai': 'ผู้หญิง', 'paiboon': 'pûu-yǐŋ', 'formality': 'neutral', 'context': 'That woman', 'usage': 'Descriptive, not pronoun'},
                        ]
                    }
                ]
            },
            
            'demonstrative': {
                'title': 'Demonstrative Pronouns: "This" / "That"',
                'explanation': 'Thai makes clear distinctions between near and far objects/people.',
                'pronouns': [
                    {
                        'category': 'Near (This)',
                        'entries': [
                            {'thai': 'นี่', 'paiboon': 'nîi', 'context': 'This (general)', 'usage': 'This thing'},
                            {'thai': 'คนนี้', 'paiboon': 'kon níi', 'context': 'This person', 'usage': 'This person'},
                            {'thai': 'อันนี้', 'paiboon': 'an níi', 'context': 'This one (object)', 'usage': 'This specific thing'},
                        ]
                    },
                    {
                        'category': 'Far (That)',
                        'entries': [
                            {'thai': 'นั่น', 'paiboon': 'nân', 'context': 'That (general)', 'usage': 'That thing'},
                            {'thai': 'คนนั้น', 'paiboon': 'kon nán', 'context': 'That person', 'usage': 'That person'},
                            {'thai': 'อันนั้น', 'paiboon': 'an nán', 'context': 'That one (object)', 'usage': 'That specific thing'},
                        ]
                    }
                ]
            },
            
            'key_insights': [
                {
                    'title': '🎯 KEY INSIGHT #1: No Gender in Third Person',
                    'explanation': 'Thai เขา (kǎo) means "he", "she", OR "they" - context determines meaning! This is VERY different from English.'
                },
                {
                    'title': '🎯 KEY INSIGHT #2: Kinship Terms = Pronouns',
                    'explanation': 'Thais often use พี่ (pîi - older sibling) and น้อง (nɔ́ɔŋ - younger sibling) as "you" based on relative age, even with strangers!'
                },
                {
                    'title': '🎯 KEY INSIGHT #3: Name as Pronoun',
                    'explanation': 'It\'s common to use "Khun + Name" instead of "you" - sounds more polite and personal.'
                },
                {
                    'title': '🎯 KEY INSIGHT #4: Speaker Gender Matters',
                    'explanation': 'Only first-person ("I") changes with speaker gender. Second and third person are the same for everyone!'
                },
                {
                    'title': '🎯 KEY INSIGHT #5: Context is Everything',
                    'explanation': 'The same pronoun can be polite or rude depending on context, tone, and relationship. Listen and observe!'
                }
            ]
        },
        {
            'name': 'Classifiers (ลักษณนาม)',
            'thai': 'ลักษณนาม',
            'paiboon': 'lák-sà-nà-naam',
            'explanation': 'Classifiers (also called "counters") are REQUIRED when counting or specifying quantities in Thai. Each noun has a specific classifier based on its characteristics.',
            'note': 'Pattern: Number + Classifier + Noun (e.g., สองคนนักเรียน = two students)',
            
            # Core categories with detailed classifiers
            'people': {
                'category': 'People & Professions',
                'explanation': 'Classifiers for humans based on role, status, or respect level',
                'classifiers': [
                    {
                        'thai': 'คน',
                        'paiboon': 'kon',
                        'usage': 'General classifier for people',
                        'examples': ['นักเรียน (students)', 'คนไทย (Thai people)', 'เพื่อน (friends)'],
                        'sample_sentence': {
                            'thai': 'นักเรียนสามคน',
                            'paiboon': 'nák-riian sǎam kon',
                            'english': 'three students'
                        }
                    },
                    {
                        'thai': 'ท่าน',
                        'paiboon': 'tân',
                        'usage': 'Monks, respected teachers, high-status individuals',
                        'examples': ['พระ (monks)', 'อาจารย์ (teachers)', 'ผู้นำ (leaders)'],
                        'sample_sentence': {
                            'thai': 'พระสองท่าน',
                            'paiboon': 'prá sɔ̌ɔŋ tân',
                            'english': 'two monks'
                        }
                    },
                    {
                        'thai': 'องค์',
                        'paiboon': 'oŋ',
                        'usage': 'Royalty, Buddha images, very high respect',
                        'examples': ['พระพุทธรูป (Buddha images)', 'กษัตริย์ (kings)', 'เทพ (deities)'],
                        'sample_sentence': {
                            'thai': 'พระพุทธรูปหนึ่งองค์',
                            'paiboon': 'prá-pút-tá-rûup nʉ̀ŋ oŋ',
                            'english': 'one Buddha image'
                        }
                    },
                    {
                        'thai': 'นาย',
                        'paiboon': 'naai',
                        'usage': 'Male animals, male servants (old usage)',
                        'examples': ['สุนัขตัวผู้ (male dogs)', 'ม้าตัวผู้ (male horses)'],
                        'sample_sentence': {
                            'thai': 'สุนัขสองนาย',
                            'paiboon': 'sù-nák sɔ̌ɔŋ naai',
                            'english': 'two dogs (male, formal)'
                        }
                    }
                ]
            },
            
            'animals': {
                'category': 'Animals & Living Creatures',
                'explanation': 'Classifiers for animals, insects, and other living creatures',
                'classifiers': [
                    {
                        'thai': 'ตัว',
                        'paiboon': 'dtuua',
                        'usage': 'General classifier for animals, insects, clothing, furniture',
                        'examples': ['สุนัข (dogs)', 'แมว (cats)', 'ปลา (fish)', 'เสื้อ (shirts)', 'โต๊ะ (tables)'],
                        'sample_sentence': {
                            'thai': 'แมวสามตัว',
                            'paiboon': 'mɛɛo sǎam dtuua',
                            'english': 'three cats'
                        }
                    },
                    {
                        'thai': 'ตน',
                        'paiboon': 'dton',
                        'usage': 'Trees, plants (formal)',
                        'examples': ['ต้นไม้ (trees)', 'กล้าไม้ (seedlings)'],
                        'sample_sentence': {
                            'thai': 'ต้นไม้สี่ต้น',
                            'paiboon': 'dtôn-máai sìi dtôn',
                            'english': 'four trees'
                        }
                    },
                    {
                        'thai': 'ดอก',
                        'paiboon': 'dɔ̀ɔk',
                        'usage': 'Flowers, buds',
                        'examples': ['กุหลาบ (roses)', 'ดอกไม้ (flowers)'],
                        'sample_sentence': {
                            'thai': 'ดอกกุหลาบห้าดอก',
                            'paiboon': 'dɔ̀ɔk gù-làap hâa dɔ̀ɔk',
                            'english': 'five roses'
                        }
                    }
                ]
            },
            
            'objects': {
                'category': 'Objects & Things',
                'explanation': 'Classifiers for various objects based on size, shape, and function',
                'classifiers': [
                    {
                        'thai': 'อัน',
                        'paiboon': 'an',
                        'usage': 'Small objects, general things, tools',
                        'examples': ['ช้อน (spoons)', 'ปากกา (pens)', 'กล่อง (boxes)'],
                        'sample_sentence': {
                            'thai': 'ปากกาสองอัน',
                            'paiboon': 'bpàak-gaa sɔ̌ɔŋ an',
                            'english': 'two pens'
                        }
                    },
                    {
                        'thai': 'ชิ้น',
                        'paiboon': 'chín',
                        'usage': 'Pieces, slices, portions',
                        'examples': ['เค้ก (cake)', 'เนื้อ (meat)', 'ผ้า (cloth)'],
                        'sample_sentence': {
                            'thai': 'เค้กสามชิ้น',
                            'paiboon': 'kéek sǎam chín',
                            'english': 'three pieces of cake'
                        }
                    },
                    {
                        'thai': 'เครื่อง',
                        'paiboon': 'krʉ̂aŋ',
                        'usage': 'Machines, appliances, instruments',
                        'examples': ['คอมพิวเตอร์ (computers)', 'เครื่องบิน (airplanes)', 'เครื่องดนตรี (musical instruments)'],
                        'sample_sentence': {
                            'thai': 'คอมพิวเตอร์สองเครื่อง',
                            'paiboon': 'kɔɔm-piu-dtəə sɔ̌ɔŋ krʉ̂aŋ',
                            'english': 'two computers'
                        }
                    },
                    {
                        'thai': 'ลูก',
                        'paiboon': 'lûuk',
                        'usage': 'Round objects, fruits, balls, children',
                        'examples': ['ลูกบอล (balls)', 'ส้ม (oranges)', 'ลูกชาย (sons)'],
                        'sample_sentence': {
                            'thai': 'ส้มสี่ลูก',
                            'paiboon': 'sôm sìi lûuk',
                            'english': 'four oranges'
                        }
                    }
                ]
            },
            
            'vehicles': {
                'category': 'Vehicles & Transportation',
                'explanation': 'Classifiers for various modes of transportation',
                'classifiers': [
                    {
                        'thai': 'คัน',
                        'paiboon': 'kan',
                        'usage': 'Vehicles with wheels or handles',
                        'examples': ['รถ (cars)', 'รถจักรยาน (bicycles)', 'มีด (knives)', 'ร่ม (umbrellas)'],
                        'sample_sentence': {
                            'thai': 'รถสามคัน',
                            'paiboon': 'rót sǎam kan',
                            'english': 'three cars'
                        }
                    },
                    {
                        'thai': 'ลำ',
                        'paiboon': 'lam',
                        'usage': 'Boats, ships, airplanes (long vehicles)',
                        'examples': ['เรือ (boats)', 'เครื่องบิน (airplanes)'],
                        'sample_sentence': {
                            'thai': 'เรือสองลำ',
                            'paiboon': 'rʉa sɔ̌ɔŋ lam',
                            'english': 'two boats'
                        }
                    }
                ]
            },
            
            'containers': {
                'category': 'Containers & Drinks',
                'explanation': 'Classifiers for drinks, containers, and food portions',
                'classifiers': [
                    {
                        'thai': 'แก้ว',
                        'paiboon': 'gɛ̂ɛo',
                        'usage': 'Glasses, cups (glassware)',
                        'examples': ['น้ำ (water)', 'เบียร์ (beer)', 'กาแฟ (coffee)'],
                        'sample_sentence': {
                            'thai': 'น้ำสามแก้ว',
                            'paiboon': 'náam sǎam gɛ̂ɛo',
                            'english': 'three glasses of water'
                        }
                    },
                    {
                        'thai': 'ถ้วย',
                        'paiboon': 'tûai',
                        'usage': 'Cups, bowls (porcelain/ceramic)',
                        'examples': ['ชา (tea)', 'กาแฟ (coffee)', 'ข้าว (rice in bowl)'],
                        'sample_sentence': {
                            'thai': 'ชาสองถ้วย',
                            'paiboon': 'chaa sɔ̌ɔŋ tûai',
                            'english': 'two cups of tea'
                        }
                    },
                    {
                        'thai': 'ขวด',
                        'paiboon': 'kùat',
                        'usage': 'Bottles',
                        'examples': ['น้ำ (water)', 'เบียร์ (beer)', 'โซดา (soda)'],
                        'sample_sentence': {
                            'thai': 'เบียร์สองขวด',
                            'paiboon': 'bia sɔ̌ɔŋ kùat',
                            'english': 'two bottles of beer'
                        }
                    },
                    {
                        'thai': 'จาน',
                        'paiboon': 'jaan',
                        'usage': 'Plates, dishes',
                        'examples': ['อาหาร (food)', 'ข้าว (rice on plate)'],
                        'sample_sentence': {
                            'thai': 'ข้าวผัดสองจาน',
                            'paiboon': 'kâao-pàt sɔ̌ɔŋ jaan',
                            'english': 'two plates of fried rice'
                        }
                    },
                    {
                        'thai': 'ชาม',
                        'paiboon': 'chaam',
                        'usage': 'Bowls (larger, for soup)',
                        'examples': ['ซุป (soup)', 'ก๋วยเตี๋ยว (noodles)'],
                        'sample_sentence': {
                            'thai': 'ก๋วยเตี๋ยวสามชาม',
                            'paiboon': 'gǔai-dtǐao sǎam chaam',
                            'english': 'three bowls of noodles'
                        }
                    }
                ]
            },
            
            'media': {
                'category': 'Books, Media & Documents',
                'explanation': 'Classifiers for printed materials, media, and documents',
                'classifiers': [
                    {
                        'thai': 'เล่ม',
                        'paiboon': 'lêm',
                        'usage': 'Books, notebooks, magazines',
                        'examples': ['หนังสือ (books)', 'สมุด (notebooks)', 'นิตยสาร (magazines)'],
                        'sample_sentence': {
                            'thai': 'หนังสือสามเล่ม',
                            'paiboon': 'nǎŋ-sʉ̌ʉ sǎam lêm',
                            'english': 'three books'
                        }
                    },
                    {
                        'thai': 'ฉบับ',
                        'paiboon': 'chà-bàp',
                        'usage': 'Newspapers, magazines (issues), documents',
                        'examples': ['หนังสือพิมพ์ (newspapers)', 'นิตยสาร (magazine issues)'],
                        'sample_sentence': {
                            'thai': 'หนังสือพิมพ์สองฉบับ',
                            'paiboon': 'nǎŋ-sʉ̌ʉ-pim sɔ̌ɔŋ chà-bàp',
                            'english': 'two newspapers'
                        }
                    },
                    {
                        'thai': 'แผ่น',
                        'paiboon': 'pɛ̀ɛn',
                        'usage': 'Flat things: paper, CDs, tickets',
                        'examples': ['กระดาษ (paper)', 'ซีดี (CDs)', 'ตั๋ว (tickets)'],
                        'sample_sentence': {
                            'thai': 'กระดาษสามแผ่น',
                            'paiboon': 'grà-dàat sǎam pɛ̀ɛn',
                            'english': 'three sheets of paper'
                        }
                    }
                ]
            },
            
            'buildings': {
                'category': 'Buildings & Structures',
                'explanation': 'Classifiers for buildings, rooms, and structures',
                'classifiers': [
                    {
                        'thai': 'หลัง',
                        'paiboon': 'lǎŋ',
                        'usage': 'Buildings, houses',
                        'examples': ['บ้าน (houses)', 'โรงแรม (hotels)'],
                        'sample_sentence': {
                            'thai': 'บ้านสองหลัง',
                            'paiboon': 'bâan sɔ̌ɔŋ lǎŋ',
                            'english': 'two houses'
                        }
                    },
                    {
                        'thai': 'ห้อง',
                        'paiboon': 'hɔ̂ɔŋ',
                        'usage': 'Rooms',
                        'examples': ['ห้องนอน (bedrooms)', 'ห้องประชุม (meeting rooms)'],
                        'sample_sentence': {
                            'thai': 'ห้องนอนสามห้อง',
                            'paiboon': 'hɔ̂ɔŋ-nɔɔn sǎam hɔ̂ɔŋ',
                            'english': 'three bedrooms'
                        }
                    },
                    {
                        'thai': 'ชั้น',
                        'paiboon': 'chán',
                        'usage': 'Floors, levels, layers',
                        'examples': ['ชั้นของตึก (building floors)', 'เค้ก (cake layers)'],
                        'sample_sentence': {
                            'thai': 'ตึกห้าชั้น',
                            'paiboon': 'dtʉ̀k hâa chán',
                            'english': 'five-story building'
                        }
                    }
                ]
            },
            
            'clothing': {
                'category': 'Clothing & Accessories',
                'explanation': 'Classifiers for clothes and wearable items',
                'classifiers': [
                    {
                        'thai': 'ตัว',
                        'paiboon': 'dtuua',
                        'usage': 'Shirts, upper body clothing',
                        'examples': ['เสื้อ (shirts)', 'เสื้อโค้ท (coats)'],
                        'sample_sentence': {
                            'thai': 'เสื้อสามตัว',
                            'paiboon': 'sʉ̂a sǎam dtuua',
                            'english': 'three shirts'
                        }
                    },
                    {
                        'thai': 'ข้าง',
                        'paiboon': 'kâaŋ',
                        'usage': 'Paired items (shoes, socks, gloves)',
                        'examples': ['รองเท้า (shoes)', 'ถุงเท้า (socks)'],
                        'sample_sentence': {
                            'thai': 'รองเท้าสองข้าง',
                            'paiboon': 'rɔɔŋ-táo sɔ̌ɔŋ kâaŋ',
                            'english': 'two pairs of shoes'
                        }
                    },
                    {
                        'thai': 'คู่',
                        'paiboon': 'kûu',
                        'usage': 'Pairs (alternative for shoes, people)',
                        'examples': ['รองเท้า (shoes)', 'สามีภรรยา (husband and wife)'],
                        'sample_sentence': {
                            'thai': 'รองเท้าสองคู่',
                            'paiboon': 'rɔɔŋ-táo sɔ̌ɔŋ kûu',
                            'english': 'two pairs of shoes'
                        }
                    }
                ]
            },
            
            'abstract': {
                'category': 'Abstract & Miscellaneous',
                'explanation': 'Classifiers for abstract concepts, events, and other items',
                'classifiers': [
                    {
                        'thai': 'เรื่อง',
                        'paiboon': 'rʉ̂aŋ',
                        'usage': 'Stories, matters, issues, movies',
                        'examples': ['หนัง (movies)', 'ปัญหา (problems)', 'นิทาน (tales)'],
                        'sample_sentence': {
                            'thai': 'หนังสามเรื่อง',
                            'paiboon': 'nǎŋ sǎam rʉ̂aŋ',
                            'english': 'three movies'
                        }
                    },
                    {
                        'thai': 'ครั้ง',
                        'paiboon': 'kráŋ',
                        'usage': 'Times, occasions',
                        'examples': ['สอบ (exams)', 'ไป (trips)', 'พบ (meetings)'],
                        'sample_sentence': {
                            'thai': 'ไปสองครั้ง',
                            'paiboon': 'bpai sɔ̌ɔŋ kráŋ',
                            'english': 'went two times'
                        }
                    },
                    {
                        'thai': 'คำ',
                        'paiboon': 'kam',
                        'usage': 'Words',
                        'examples': ['คำศัพท์ (vocabulary)', 'คำถาม (questions)'],
                        'sample_sentence': {
                            'thai': 'คำศัพท์สิบคำ',
                            'paiboon': 'kam-sàp sìp kam',
                            'english': 'ten vocabulary words'
                        }
                    },
                    {
                        'thai': 'บาท',
                        'paiboon': 'bàat',
                        'usage': 'Thai currency (baht)',
                        'examples': ['เงิน (money)'],
                        'sample_sentence': {
                            'thai': 'หนึ่งร้อยบาท',
                            'paiboon': 'nʉ̀ŋ rɔ́ɔi bàat',
                            'english': 'one hundred baht'
                        }
                    }
                ]
            },
            
            'usage_patterns': {
                'title': 'Common Usage Patterns',
                'patterns': [
                    {
                        'pattern': 'Number + Classifier + Noun',
                        'thai': 'สามคนนักเรียน',
                        'paiboon': 'sǎam kon nák-riian',
                        'english': 'three students',
                        'note': 'Most common pattern for counting'
                    },
                    {
                        'pattern': 'Noun + Number + Classifier',
                        'thai': 'นักเรียนสามคน',
                        'paiboon': 'nák-riian sǎam kon',
                        'english': 'three students',
                        'note': 'Alternative pattern, also common'
                    },
                    {
                        'pattern': 'Classifier alone = "one"',
                        'thai': 'แมวตัวหนึ่ง = แมวตัว',
                        'paiboon': 'mɛɛo dtuua nʉ̀ŋ = mɛɛo dtuua',
                        'english': 'one cat (หนึ่ง optional)',
                        'note': 'Can omit หนึ่ง (one) when obvious'
                    },
                    {
                        'pattern': 'Noun as own classifier',
                        'thai': 'คนสามคน, เดือนสามเดือน',
                        'paiboon': 'kon sǎam kon, dʉan sǎam dʉan',
                        'english': 'three people, three months',
                        'note': 'Some nouns double as classifiers'
                    }
                ]
            },
            
            'key_insights': [
                {
                    'title': 'Why Classifiers Matter',
                    'explanation': 'You CANNOT say "three cat" or "two book" in Thai. You MUST use classifiers: "three ANIMALS cat" (แมวสามตัว) or "two BOOKS book" (หนังสือสองเล่ม). This is not optional!'
                },
                {
                    'title': 'Shape & Size Matter',
                    'explanation': 'Classifiers often reflect physical characteristics: long things (ลำ), round things (ลูก), flat things (แผ่น), small things (อัน). Understanding the "why" helps you remember!'
                },
                {
                    'title': 'Respect Levels',
                    'explanation': 'Some classifiers show respect: คน (general people), ท่าน (monks/teachers), องค์ (royalty/Buddha). Using wrong classifier can be disrespectful!'
                },
                {
                    'title': 'Multiple Classifiers',
                    'explanation': 'Some nouns accept multiple classifiers: เสื้อ (shirts) uses ตัว, but you can also say ชิ้น (piece). Context determines which is more natural.'
                },
                {
                    'title': 'When in Doubt',
                    'explanation': 'อัน (an) is the safe general classifier for objects. Thais will understand even if not 100% correct. But learning specific ones shows fluency!'
                }
            ]
        },
        {
            'name': 'Verbs (คำกริยา)',
            'thai': 'คำกริยา',
            'paiboon': 'kam grì-yaa',
            'explanation': 'Thai verbs do not conjugate. Tense shown by context/markers.',
            'examples': [
                {'thai': 'กิน', 'paiboon': 'gin', 'english': 'eat'},
                {'thai': 'ไป', 'paiboon': 'bpai', 'english': 'go'},
                {'thai': 'มา', 'paiboon': 'maa', 'english': 'come'},
                {'thai': 'ทำ', 'paiboon': 'tam', 'english': 'do/make'},
                {'thai': 'พูด', 'paiboon': 'pûut', 'english': 'speak'},
            ]
        },
        {
            'name': 'Adjectives (คำคุณศัพท์)',
            'thai': 'คำคุณศัพท์',
            'paiboon': 'kam kun-ná-sàp',
            'explanation': 'Adjectives come AFTER nouns (opposite of English).',
            'examples': [
                {'thai': 'บ้านใหญ่', 'paiboon': 'bâan yài', 'english': 'big house'},
                {'thai': 'รถแดง', 'paiboon': 'rót dɛɛŋ', 'english': 'red car'},
                {'thai': 'คนดี', 'paiboon': 'kon dii', 'english': 'good person'},
            ]
        },
        {
            'name': 'Adverbs (คำกริยาวิเศษณ์)',
            'thai': 'คำกริยาวิเศษณ์',
            'paiboon': 'kam grì-yaa wí-sàyt',
            'explanation': 'Adverbs typically come after verbs.',
            'examples': [
                {'thai': 'เร็ว', 'paiboon': 'reo', 'english': 'quickly'},
                {'thai': 'ช้า', 'paiboon': 'cháa', 'english': 'slowly'},
                {'thai': 'มาก', 'paiboon': 'mâak', 'english': 'very/much'},
            ]
        },
        {
            'name': 'Prepositions (คำบุพบท)',
            'thai': 'คำบุพบท',
            'paiboon': 'kam bùp-pá-bòt',
            'explanation': 'Words indicating location, direction, relationships.',
            'examples': [
                {'thai': 'ใน', 'paiboon': 'nai', 'english': 'in/inside'},
                {'thai': 'บน', 'paiboon': 'bon', 'english': 'on/above'},
                {'thai': 'ใต้', 'paiboon': 'dtâi', 'english': 'under'},
                {'thai': 'ที่', 'paiboon': 'tîi', 'english': 'at/place'},
            ]
        },
        {
            'name': 'Conjunctions (คำสันธาน)',
            'thai': 'คำสันธาน',
            'paiboon': 'kam sǎn-taan',
            'explanation': 'Words connecting clauses or sentences.',
            'examples': [
                {'thai': 'และ', 'paiboon': 'láe', 'english': 'and'},
                {'thai': 'หรือ', 'paiboon': 'rʉ̌ʉ', 'english': 'or'},
                {'thai': 'แต่', 'paiboon': 'dtɛ̀ɛ', 'english': 'but'},
                {'thai': 'เพราะ', 'paiboon': 'prɔ́', 'english': 'because'},
            ]
        },
    ],
    
    'particles': [
        {
            'name': 'Politeness Particles',
            'entries': [
                {'thai': 'ครับ', 'paiboon': 'kráp', 'english': 'polite (male)'},
                {'thai': 'ค่ะ', 'paiboon': 'kâ', 'english': 'polite (female, statement)'},
                {'thai': 'คะ', 'paiboon': 'ká', 'english': 'polite (female, question)'},
            ]
        },
        {
            'name': 'Question Particles',
            'entries': [
                {'thai': 'ไหม', 'paiboon': 'mǎi', 'english': 'yes/no question'},
                {'thai': 'หรือ', 'paiboon': 'rʉ̌ʉ', 'english': 'or? / right?'},
                {'thai': 'เหรอ', 'paiboon': 'rə̌ə', 'english': 'really? (informal)'},
            ]
        },
        {
            'name': 'Softening/Emphasis Particles',
            'entries': [
                {'thai': 'นะ', 'paiboon': 'ná', 'english': 'softener / please'},
                {'thai': 'สิ', 'paiboon': 'sì', 'english': 'urging / go ahead'},
                {'thai': 'เลย', 'paiboon': 'ləəi', 'english': 'emphasis / at all'},
                {'thai': 'ก็', 'paiboon': 'gɔ̂ɔ', 'english': 'then / also'},
            ]
        },
    ],
    
    'sentence_structure': {
        'basic_order': 'Subject + Verb + Object (SVO)',
        'examples': [
            {'thai': 'ผมกินข้าว', 'paiboon': 'pǒm gin kâao', 'english': 'I eat rice'},
            {'thai': 'เขาไปตลาด', 'paiboon': 'kǎo bpai dtà-làat', 'english': 'He goes to market'},
        ],
        'adjective_position': 'Adjectives come AFTER nouns',
        'adj_examples': [
            {'thai': 'รถสีแดง', 'paiboon': 'rót sǐi dɛɛŋ', 'english': 'red car'},
            {'thai': 'อาหารอร่อย', 'paiboon': 'aa-hǎan à-ròi', 'english': 'delicious food'},
        ]
    },
    
    'tense_aspect': [
        {
            'name': 'Past',
            'markers': [
                {'thai': 'แล้ว', 'paiboon': 'lɛ́ɛo', 'english': 'already'},
                {'thai': 'เมื่อวาน', 'paiboon': 'mʉ̂a waan', 'english': 'yesterday'},
            ],
            'example': {'thai': 'ผมกินข้าวแล้ว', 'paiboon': 'pǒm gin kâao lɛ́ɛo', 'english': 'I already ate'}
        },
        {
            'name': 'Present',
            'markers': [
                {'thai': 'กำลัง', 'paiboon': 'gam-laŋ', 'english': 'currently'},
                {'thai': 'อยู่', 'paiboon': 'yùu', 'english': 'in the state of'},
            ],
            'example': {'thai': 'ผมกำลังกินข้าว', 'paiboon': 'pǒm gam-laŋ gin kâao', 'english': 'I am eating'}
        },
        {
            'name': 'Future',
            'markers': [
                {'thai': 'จะ', 'paiboon': 'jà', 'english': 'will'},
                {'thai': 'พรุ่งนี้', 'paiboon': 'prûŋ níi', 'english': 'tomorrow'},
            ],
            'example': {'thai': 'ผมจะไป', 'paiboon': 'pǒm jà bpai', 'english': 'I will go'}
        },
    ],
    
    'questions': [
        {'type': 'What', 'thai': 'อะไร', 'paiboon': 'à-rai', 'example': 'นี่คืออะไร'},
        {'type': 'Who', 'thai': 'ใคร', 'paiboon': 'krai', 'example': 'นี่คือใคร'},
        {'type': 'Where', 'thai': 'ที่ไหน', 'paiboon': 'tîi nǎi', 'example': 'คุณไปที่ไหน'},
        {'type': 'When', 'thai': 'เมื่อไหร่', 'paiboon': 'mʉ̂a rài', 'example': 'คุณมาเมื่อไหร่'},
        {'type': 'Why', 'thai': 'ทำไม', 'paiboon': 'tam-mai', 'example': 'ทำไมคุณไป'},
        {'type': 'How', 'thai': 'อย่างไร', 'paiboon': 'yàaŋ rai', 'example': 'ทำอย่างไร'},
        {'type': 'How much', 'thai': 'เท่าไหร่', 'paiboon': 'tâo rài', 'example': 'ราคาเท่าไหร่'},
        {'type': 'How many', 'thai': 'กี่', 'paiboon': 'gìi', 'example': 'กี่คน'},
    ],
    
    'negation': [
        {'pattern': 'ไม่ + verb/adj', 'thai': 'ไม่', 'paiboon': 'mâi', 'example': 'ไม่ไป - not go'},
        {'pattern': 'ไม่มี + noun', 'thai': 'ไม่มี', 'paiboon': 'mâi mii', 'example': 'ไม่มีเงิน'},
        {'pattern': 'ไม่ได้ + verb', 'thai': 'ไม่ได้', 'paiboon': 'mâi dâi', 'example': "ไม่ได้กิน - didn't eat"},
        {'pattern': 'ยังไม่ (not yet)', 'thai': 'ยังไม่', 'paiboon': 'yaŋ mâi', 'example': 'ยังไม่กิน'},
    ],
    
    'comparison': [
        {'pattern': 'more than', 'thai': 'กว่า', 'paiboon': 'gwàa', 'example': 'ใหญ่กว่า'},
        {'pattern': 'most', 'thai': 'ที่สุด', 'paiboon': 'tîi sùt', 'example': 'ใหญ่ที่สุด'},
        {'pattern': 'as...as', 'thai': 'เท่ากับ', 'paiboon': 'tâo gàp', 'example': 'ใหญ่เท่ากับ'},
        {'pattern': 'less than', 'thai': 'น้อยกว่า', 'paiboon': 'nɔ́ɔi gwàa', 'example': 'น้อยกว่า'},
    ],
    
    'classifier_counting': {
        'pattern': 'Number + Classifier (or Noun + Number + Classifier)',
        'examples': [
            {'thai': 'สามคน', 'paiboon': 'sǎam kon', 'english': 'three people'},
            {'thai': 'สองเล่ม', 'paiboon': 'sɔ̌ɔŋ lêm', 'english': 'two books'},
            {'thai': 'ห้าตัว', 'paiboon': 'hâa dtuua', 'english': 'five animals'},
        ]
    },
    
    'common_patterns': [
        {'pattern': 'I want to...', 'thai': 'อยาก...', 'paiboon': 'yàak...', 'example': 'ผมอยากกิน'},
        {'pattern': "I'm going to...", 'thai': 'จะไป...', 'paiboon': 'jà bpai...', 'example': 'ผมจะไปตลาด'},
        {'pattern': 'I like...', 'thai': 'ชอบ...', 'paiboon': 'chɔ̂ɔp...', 'example': 'ผมชอบอาหารไทย'},
        {'pattern': 'Can you...?', 'thai': '...ได้ไหม', 'paiboon': '...dâi mǎi', 'example': 'พูดไทยได้ไหม'},
        {'pattern': 'There is/are', 'thai': 'มี...', 'paiboon': 'mii...', 'example': 'มีคนสามคน'},
    ],
}


# ============================================
# TONES & CONSONANT CLASSES (unified free section)
# ============================================
# One skill that teaches consonant classes and tone rules together, because
# classes only exist to work out tones. The reference content is adapted from
# GRAMMAR['consonant_classes'] and topped up with the live/dead-syllable rules,
# the leading-ห rule, contrast pairs and the four practice drills.
# NOTE ON OBSOLETE LETTERS: ฃ (high) and ฅ (low) are shown in the reference
# chart with 'obsolete': True so the template can grey them out and the drills
# can skip them. Never include an obsolete letter as a drill question.

TONES_AND_CLASSES = {
    'core_concept': {
        'title': 'How Thai tones actually work',
        'summary': "Thai tones aren't written directly on the page. You calculate them from three things: (1) the consonant class, (2) whether the syllable is live or dead, and (3) the tone mark (if any). The consonant class is the primary factor — get that first and everything else follows.",
        'formula': 'Consonant class  +  Live / Dead syllable  +  Tone mark  =  The tone you say',
        'live_dead': "A LIVE syllable ends in a long vowel or a sonorant sound (m, n, ng, y, w). A DEAD syllable ends in a short vowel or a hard stop sound (p, t, k). Live and dead syllables follow different tone rules.",
        'shortcut': "Teaching shortcut: you only need to memorise the 20 MID + HIGH consonants. Everything else (all 24 of them) is LOW class by elimination.",
    },

    # Ordered MID → HIGH → LOW: mid is the most regular and is learned first.
    'classes': [
        {
            'label': 'MID',
            'name': 'Mid Class',
            'thai': 'อักษรกลาง',
            'paiboon': 'àk-sɔ̌ɔn glaaŋ',
            'colour': 'mid',
            'count': 9,
            'headline': 'Learn these first — the most regular, and the only class that can make all 5 tones.',
            'tone_rules': 'No tone mark on a live syllable = MID tone. Tone marks then give you LOW, FALLING, HIGH or RISING. The most predictable class.',
            'memory_tip': 'Just 9 letters — the small, well-behaved group. Memorise these and the 11 high-class letters, and every other letter is low by elimination.',
            'consonants': [
                {'thai': 'ก', 'paiboon': 'g', 'name': 'gɔɔ gài (chicken)'},
                {'thai': 'จ', 'paiboon': 'j', 'name': 'jɔɔ jaan (plate)'},
                {'thai': 'ฎ', 'paiboon': 'd', 'name': 'dɔɔ chá-daa (headdress)'},
                {'thai': 'ฏ', 'paiboon': 'dt', 'name': 'dtɔɔ bpà-dtàk (goad)'},
                {'thai': 'ด', 'paiboon': 'd', 'name': 'dɔɔ dèk (child)'},
                {'thai': 'ต', 'paiboon': 'dt', 'name': 'dtɔɔ dtào (turtle)'},
                {'thai': 'บ', 'paiboon': 'b', 'name': 'bɔɔ bai-mái (leaf)'},
                {'thai': 'ป', 'paiboon': 'bp', 'name': 'bpɔɔ bplaa (fish)'},
                {'thai': 'อ', 'paiboon': 'ʔ', 'name': 'ʔɔɔ àaŋ (basin)'},
            ],
            'examples': [
                {'thai': 'ปา', 'paiboon': 'bpaa', 'tone': 'Mid', 'english': 'throw'},
                {'thai': 'ป่า', 'paiboon': 'bpàa', 'tone': 'Low', 'english': 'forest'},
                {'thai': 'ป้า', 'paiboon': 'bpâa', 'tone': 'Falling', 'english': 'aunt'},
                {'thai': 'ป๊า', 'paiboon': 'bpáa', 'tone': 'High', 'english': 'papa'},
            ],
        },
        {
            'label': 'HIGH',
            'name': 'High Class',
            'thai': 'อักษรสูง',
            'paiboon': 'àk-sɔ̌ɔn sǔuŋ',
            'colour': 'high',
            'count': 11,
            'headline': 'No tone mark = RISING tone. Only 3 possible tones.',
            'tone_rules': 'No tone mark on a live syllable = RISING tone. Tone marks give you only LOW or FALLING. High class can never make a high tone by itself.',
            'memory_tip': 'Mostly the breathy / aspirated sounds. ฃ is obsolete — you will never meet it in real writing.',
            'consonants': [
                {'thai': 'ข', 'paiboon': 'k', 'name': 'kɔɔ kài (egg)'},
                {'thai': 'ฃ', 'paiboon': 'k', 'name': 'kɔɔ kùuat (bottle)', 'obsolete': True},
                {'thai': 'ฉ', 'paiboon': 'ch', 'name': 'chɔɔ chǐŋ (cymbal)'},
                {'thai': 'ฐ', 'paiboon': 't', 'name': 'tɔɔ tǎan (base)'},
                {'thai': 'ถ', 'paiboon': 't', 'name': 'tɔɔ tǔŋ (bag)'},
                {'thai': 'ผ', 'paiboon': 'p', 'name': 'pɔɔ pʉ̌ŋ (bee)'},
                {'thai': 'ฝ', 'paiboon': 'f', 'name': 'fɔɔ fǎa (lid)'},
                {'thai': 'ศ', 'paiboon': 's', 'name': 'sɔɔ sǎa-laa (pavilion)'},
                {'thai': 'ษ', 'paiboon': 's', 'name': 'sɔɔ rʉʉ-sǐi (hermit)'},
                {'thai': 'ส', 'paiboon': 's', 'name': 'sɔɔ sʉ̌a (tiger)'},
                {'thai': 'ห', 'paiboon': 'h', 'name': 'hɔɔ hìip (chest)'},
            ],
            'examples': [
                {'thai': 'ขา', 'paiboon': 'kǎa', 'tone': 'Rising', 'english': 'leg'},
                {'thai': 'ข่า', 'paiboon': 'kàa', 'tone': 'Low', 'english': 'galangal'},
                {'thai': 'ข้า', 'paiboon': 'kâa', 'tone': 'Falling', 'english': 'I (formal)'},
                {'thai': 'สอง', 'paiboon': 'sɔ̌ɔŋ', 'tone': 'Rising', 'english': 'two'},
            ],
        },
        {
            'label': 'LOW',
            'name': 'Low Class',
            'thai': 'อักษรต่ำ',
            'paiboon': 'àk-sɔ̌ɔn dtàm',
            'colour': 'low',
            'count': 24,
            'headline': '⚠️ The tone marks act DIFFERENTLY here — this is the most common learner error.',
            'tone_rules': "No tone mark on a live syllable = MID tone. But watch the marks: ไม้เอก ( ่ ) gives FALLING (not low!) and ไม้โท ( ้ ) gives HIGH. That is the opposite of what beginners expect.",
            'memory_tip': 'The big group (24 letters). You do not memorise it — anything that is not one of the 20 mid/high letters is low. 14 come in high/low pairs; 10 are single sounds (the sonorants ง ญ ณ น ม ย ร ล ว ฬ).',
            'consonants': [
                # Paired (14) — share a sound with a high-class partner
                {'thai': 'ค', 'paiboon': 'k', 'name': 'kɔɔ kwaai (buffalo)', 'group': 'paired'},
                {'thai': 'ฅ', 'paiboon': 'k', 'name': 'kɔɔ kon (person)', 'group': 'paired', 'obsolete': True},
                {'thai': 'ฆ', 'paiboon': 'k', 'name': 'kɔɔ rá-kaŋ (bell)', 'group': 'paired'},
                {'thai': 'ช', 'paiboon': 'ch', 'name': 'chɔɔ cháaŋ (elephant)', 'group': 'paired'},
                {'thai': 'ซ', 'paiboon': 's', 'name': 'sɔɔ sôo (chain)', 'group': 'paired'},
                {'thai': 'ฌ', 'paiboon': 'ch', 'name': 'chɔɔ chəə (tree)', 'group': 'paired'},
                {'thai': 'ฑ', 'paiboon': 't', 'name': 'tɔɔ mon-too (Montho)', 'group': 'paired'},
                {'thai': 'ฒ', 'paiboon': 't', 'name': 'tɔɔ pûu-tâo (old man)', 'group': 'paired'},
                {'thai': 'ท', 'paiboon': 't', 'name': 'tɔɔ tá-hǎan (soldier)', 'group': 'paired'},
                {'thai': 'ธ', 'paiboon': 't', 'name': 'tɔɔ toŋ (flag)', 'group': 'paired'},
                {'thai': 'พ', 'paiboon': 'p', 'name': 'pɔɔ paan (tray)', 'group': 'paired'},
                {'thai': 'ฟ', 'paiboon': 'f', 'name': 'fɔɔ fan (teeth)', 'group': 'paired'},
                {'thai': 'ภ', 'paiboon': 'p', 'name': 'pɔɔ sǎm-phao (sailboat)', 'group': 'paired'},
                {'thai': 'ฮ', 'paiboon': 'h', 'name': 'hɔɔ nók-hûuk (owl)', 'group': 'paired'},
                # Single (10) — the sonorants, no high-class partner
                {'thai': 'ง', 'paiboon': 'ŋ', 'name': 'ŋɔɔ ŋuu (snake)', 'group': 'single'},
                {'thai': 'ญ', 'paiboon': 'y', 'name': 'yɔɔ yǐŋ (woman)', 'group': 'single'},
                {'thai': 'ณ', 'paiboon': 'n', 'name': 'nɔɔ neen (novice)', 'group': 'single'},
                {'thai': 'น', 'paiboon': 'n', 'name': 'nɔɔ nǔu (mouse)', 'group': 'single'},
                {'thai': 'ม', 'paiboon': 'm', 'name': 'mɔɔ máa (horse)', 'group': 'single'},
                {'thai': 'ย', 'paiboon': 'y', 'name': 'yɔɔ yák (giant)', 'group': 'single'},
                {'thai': 'ร', 'paiboon': 'r', 'name': 'rɔɔ rʉa (boat)', 'group': 'single'},
                {'thai': 'ล', 'paiboon': 'l', 'name': 'lɔɔ liŋ (monkey)', 'group': 'single'},
                {'thai': 'ว', 'paiboon': 'w', 'name': 'wɔɔ wɛɛn (ring)', 'group': 'single'},
                {'thai': 'ฬ', 'paiboon': 'l', 'name': 'lɔɔ jù-laa (kite)', 'group': 'single'},
            ],
            'examples': [
                {'thai': 'คา', 'paiboon': 'kaa', 'tone': 'Mid', 'english': 'stuck'},
                {'thai': 'ค่า', 'paiboon': 'kâa', 'tone': 'Falling', 'english': 'value'},
                {'thai': 'ค้า', 'paiboon': 'káa', 'tone': 'High', 'english': 'trade'},
                {'thai': 'ช้าง', 'paiboon': 'cháaŋ', 'tone': 'High', 'english': 'elephant'},
            ],
        },
    ],

    # Same-sound pairs: consonants that sound identical but sit in different
    # classes, so the very same syllable comes out as a different tone. This is
    # the clearest proof that the CLASS — not the letter's sound — drives the tone.
    'sound_pairs': {
        'title': 'Same sound, different class → different tone',
        'note': "Several consonants sound identical but live in different classes. With no tone mark, the HIGH-class letter gives a RISING tone while its LOW-class twin gives a MID tone — same sound, different tone, just because of the class.",
        'demo': {
            'high': {'thai': 'ขา', 'paiboon': 'kǎa', 'tone': 'Rising', 'english': 'leg'},
            'low':  {'thai': 'คา', 'paiboon': 'kaa', 'tone': 'Mid', 'english': 'stuck'},
        },
        'pairs': [
            {'sound': 'k',  'high': 'ข', 'low': 'ค'},
            {'sound': 'ch', 'high': 'ฉ', 'low': 'ช'},
            {'sound': 't',  'high': 'ถ', 'low': 'ท'},
            {'sound': 'p',  'high': 'ผ', 'low': 'พ'},
            {'sound': 'f',  'high': 'ฝ', 'low': 'ฟ'},
            {'sound': 's',  'high': 'ส', 'low': 'ซ'},
            {'sound': 'h',  'high': 'ห', 'low': 'ฮ'},
        ],
    },

    # How to actually get good at this — the study plan and elimination tricks
    # that used to live in the Grammar page's consonant-class section.
    'mastery': {
        'title': 'How to master this',
        'steps': [
            'Memorise the 9 MID consonants first — the smallest and most regular group.',
            'Learn the 11 HIGH consonants (mostly the breathy, aspirated sounds).',
            'Everything left over is LOW class (24 letters) — you get it by elimination.',
            'Practise on real words so you recognise the patterns instead of reciting them.',
            'Run the drills below until the tone comes out automatically.',
        ],
        'mnemonic': 'MID = ก จ ฎ ฏ ด ต บ ป อ (just 9 — make a silly sentence to lock them in). HIGH = the breathy group. LOW = everything else.',
        'sonorant_tip': 'The flowing sounds — ง ญ ณ น ม ย ร ล ว ฬ — are ALL low class. No nasal or flowing sound is ever mid or high, so that is an instant way to rule classes out.',
    },

    # LIVE-syllable tone chart. Columns are the five mark states; rows are the
    # three classes. A dash means that combination is not used.
    'tone_chart_live': {
        'title': 'Live-syllable tone chart',
        'note': "Read across: pick the class row, then the tone mark column. Notice how the LOW row breaks the pattern — that mismatch is where most reading mistakes come from.",
        'columns': ['No mark', 'ไม้เอก  ่', 'ไม้โท  ้', 'ไม้ตรี  ๊', 'ไม้จัตวา  ๋'],
        'rows': [
            {'label': 'MID', 'colour': 'mid', 'tones': ['Mid', 'Low', 'Falling', 'High', 'Rising']},
            {'label': 'HIGH', 'colour': 'high', 'tones': ['Rising', 'Low', 'Falling', '–', '–']},
            {'label': 'LOW', 'colour': 'low', 'tones': ['Mid', 'Falling', 'High', '–', '–']},
        ],
    },

    'dead_syllables': {
        'title': 'Dead syllables (short vowel or a p / t / k stop ending)',
        'rules': [
            {'classes': 'MID & HIGH class', 'result': 'LOW tone', 'example': {'thai': 'จะ', 'paiboon': 'jà', 'english': 'will (short vowel = dead)'}},
            {'classes': 'LOW class, SHORT vowel', 'result': 'HIGH tone', 'example': {'thai': 'คะ', 'paiboon': 'ká', 'english': 'yes/polite (female)'}},
            {'classes': 'LOW class, LONG vowel', 'result': 'FALLING tone', 'example': {'thai': 'มาก', 'paiboon': 'mâak', 'english': 'a lot / very'}},
        ],
    },

    'leading_h': {
        'title': 'The silent leading ห',
        'rule': "Put a silent ห in front of a single low-class consonant (the sonorants ง ญ น ม ย ร ล ว) and that consonant now follows HIGH-class rules. The ห is not pronounced — it only changes the tone.",
        'pairs': [
            {'plain': {'thai': 'มา', 'paiboon': 'maa', 'tone': 'Mid', 'english': 'come'},
             'led':   {'thai': 'หมา', 'paiboon': 'mǎa', 'tone': 'Rising', 'english': 'dog'}},
            {'plain': {'thai': 'นา', 'paiboon': 'naa', 'tone': 'Mid', 'english': 'rice field'},
             'led':   {'thai': 'หนา', 'paiboon': 'nǎa', 'tone': 'Rising', 'english': 'thick'}},
        ],
    },

    'contrast_pairs': {
        'title': 'Minimal pairs — where the class changes the tone',
        'note': 'Same-ish spelling, different consonant class, completely different tone and meaning. This is why the class matters.',
        'pairs': [
            {'a': {'thai': 'คา', 'paiboon': 'kaa', 'class': 'LOW', 'mark': 'none', 'tone': 'Mid', 'english': 'stuck'},
             'b': {'thai': 'ข่า', 'paiboon': 'kàa', 'class': 'HIGH', 'mark': 'ไม้เอก ่', 'tone': 'Low', 'english': 'galangal'}},
            {'a': {'thai': 'มา', 'paiboon': 'maa', 'class': 'LOW', 'mark': 'none', 'tone': 'Mid', 'english': 'come'},
             'b': {'thai': 'หมา', 'paiboon': 'mǎa', 'class': 'HIGH (via leading ห)', 'mark': 'none', 'tone': 'Rising', 'english': 'dog'}},
            {'a': {'thai': 'กา', 'paiboon': 'gaa', 'class': 'MID', 'mark': 'none', 'tone': 'Mid', 'english': 'crow'},
             'b': {'thai': 'ไก่', 'paiboon': 'gài', 'class': 'MID', 'mark': 'ไม้เอก ่', 'tone': 'Low', 'english': 'chicken'}},
        ],
    },

    'reference_tones': [
        {'name': 'Mid', 'symbol': 'no mark', 'example': 'gaa', 'description': 'Flat, neutral pitch.'},
        {'name': 'Low', 'symbol': 'à', 'example': 'gàa', 'description': 'Start low, stay low.'},
        {'name': 'Falling', 'symbol': 'â', 'example': 'gâa', 'description': 'Start high, fall down.'},
        {'name': 'High', 'symbol': 'á', 'example': 'gáa', 'description': 'Higher pitched, pushed up.'},
        {'name': 'Rising', 'symbol': 'ǎ', 'example': 'gǎa', 'description': 'Start low, rise up (like a question).'},
    ],
    'tone_marks': [
        {'thai': ' ่', 'name': 'ไม้เอก (mai ek)', 'effect': 'Mid/High → low · Low → falling'},
        {'thai': ' ้', 'name': 'ไม้โท (mai tho)', 'effect': 'Mid/High → falling · Low → high'},
        {'thai': ' ๊', 'name': 'ไม้ตรี (mai tri)', 'effect': 'Mid class → high (rare)'},
        {'thai': ' ๋', 'name': 'ไม้จัตวา (mai jattawa)', 'effect': 'Mid class → rising (rare)'},
    ],

    # ── Practice drill pools (consumed by the template's JS) ──────────────
    # Drill 1 (class ID) is built in the template from the 'classes' lists,
    # skipping obsolete letters. Drills 2–4 use these explicit pools. Every
    # question's 'tone' is the correct answer sent to /api/check_answer.
    'drills': {
        # Drill 2 — read a syllable, pick the resulting tone. 'level' drives the
        # progression: 1 = mid class only, 2 = high, 3 = low, then mixed.
        'tone_calc': [
            {'thai': 'ปา', 'tone': 'Mid', 'class': 'MID', 'level': 1, 'english': 'throw'},
            {'thai': 'ป่า', 'tone': 'Low', 'class': 'MID', 'level': 1, 'english': 'forest'},
            {'thai': 'ป้า', 'tone': 'Falling', 'class': 'MID', 'level': 1, 'english': 'aunt'},
            {'thai': 'กา', 'tone': 'Mid', 'class': 'MID', 'level': 1, 'english': 'crow'},
            {'thai': 'ไก่', 'tone': 'Low', 'class': 'MID', 'level': 1, 'english': 'chicken'},
            {'thai': 'ขา', 'tone': 'Rising', 'class': 'HIGH', 'level': 2, 'english': 'leg'},
            {'thai': 'ข่า', 'tone': 'Low', 'class': 'HIGH', 'level': 2, 'english': 'galangal'},
            {'thai': 'ข้า', 'tone': 'Falling', 'class': 'HIGH', 'level': 2, 'english': 'I (formal)'},
            {'thai': 'สอง', 'tone': 'Rising', 'class': 'HIGH', 'level': 2, 'english': 'two'},
            {'thai': 'คา', 'tone': 'Mid', 'class': 'LOW', 'level': 3, 'english': 'stuck'},
            {'thai': 'ค่า', 'tone': 'Falling', 'class': 'LOW', 'level': 3, 'english': 'value'},
            {'thai': 'ค้า', 'tone': 'High', 'class': 'LOW', 'level': 3, 'english': 'trade'},
            {'thai': 'มา', 'tone': 'Mid', 'class': 'LOW', 'level': 3, 'english': 'come'},
        ],
        # Drill 3 — contrast pairs: show one member, pick its tone.
        'contrast': [
            {'thai': 'คา', 'tone': 'Mid', 'english': 'stuck (low class, no mark)'},
            {'thai': 'ข่า', 'tone': 'Low', 'english': 'galangal (high class + ไม้เอก)'},
            {'thai': 'กา', 'tone': 'Mid', 'english': 'crow (mid class, no mark)'},
            {'thai': 'ไก่', 'tone': 'Low', 'english': 'chicken (mid class + ไม้เอก)'},
        ],
        # Drill 4 — leading ห: pick the tone. Rising means the ห did its job.
        'leading_h': [
            {'thai': 'หมา', 'tone': 'Rising', 'english': 'dog (ห + ม)'},
            {'thai': 'มา', 'tone': 'Mid', 'english': 'come (plain ม)'},
            {'thai': 'หนา', 'tone': 'Rising', 'english': 'thick (ห + น)'},
            {'thai': 'นา', 'tone': 'Mid', 'english': 'rice field (plain น)'},
            {'thai': 'หญิง', 'tone': 'Rising', 'english': 'woman (ห + ญ)'},
        ],
    },
}


# ============================================
# PAIBOON ROMANIZATION GUIDE
# ============================================

PAIBOON_GUIDE = {
    'overview': {
        'description': 'Paiboon romanization accurately represents Thai pronunciation for English speakers.',
        'reference': 'Thai-English English-Thai Dictionary (Paiboon Publishing)',
        'audio_resource': {
            'name': 'Slice of Thai',
            'url': 'http://slice-of-thai.com/language',
            'description': 'Hear all Thai sounds with sample words and native pronunciation'
        }
    },
    
    'tones': [
        {'name': 'Mid Tone', 'symbol': 'no mark', 'example': 'gaa', 'description': 'Flat, neutral pitch.'},
        {'name': 'Low Tone', 'symbol': 'à', 'example': 'gàa', 'description': 'Start low, stay low.'},
        {'name': 'Falling Tone', 'symbol': 'â', 'example': 'gâa', 'description': 'Start high, fall down.'},
        {'name': 'High Tone', 'symbol': 'á', 'example': 'gáa', 'description': 'Higher pitched, slightly rising.'},
        {'name': 'Rising Tone', 'symbol': 'ǎ', 'example': 'gǎa', 'description': 'Start mid-low, rise up.'},
    ],
    
    'consonants': [
        {'thai': 'ก', 'paiboon': 'g', 'sound': 'g as in "go"'},
        {'thai': 'ข/ค', 'paiboon': 'k', 'sound': 'k as in "sky"'},
        {'thai': 'ง', 'paiboon': 'ŋ', 'sound': 'ŋ as in \"sing\"'},
        {'thai': 'จ', 'paiboon': 'j', 'sound': 'j as in "jam"'},
        {'thai': 'ช/ฉ', 'paiboon': 'ch', 'sound': 'ch as in "church"'},
        {'thai': 'ด/ฎ', 'paiboon': 'd', 'sound': 'd as in "day"'},
        {'thai': 'ต/ฏ', 'paiboon': 'dt', 'sound': 'unaspirated t (between d and t)'},
        {'thai': 'ท/ธ/ถ', 'paiboon': 't', 'sound': 't as in "top"'},
        {'thai': 'น/ณ', 'paiboon': 'n', 'sound': 'n as in "no"'},
        {'thai': 'บ', 'paiboon': 'b', 'sound': 'b as in "boy"'},
        {'thai': 'ป', 'paiboon': 'bp', 'sound': 'unaspirated p (between b and p)'},
        {'thai': 'พ/ภ/ผ', 'paiboon': 'p', 'sound': 'p as in "pan"'},
        {'thai': 'ฟ/ฝ', 'paiboon': 'f', 'sound': 'f as in "fun"'},
        {'thai': 'ม', 'paiboon': 'm', 'sound': 'm as in "mom"'},
        {'thai': 'ย', 'paiboon': 'y', 'sound': 'y as in "yes"'},
        {'thai': 'ร', 'paiboon': 'r', 'sound': 'r (rolled)'},
        {'thai': 'ล/ฬ', 'paiboon': 'l', 'sound': 'l as in "love"'},
        {'thai': 'ว', 'paiboon': 'w', 'sound': 'w as in "way"'},
        {'thai': 'ส/ศ/ษ', 'paiboon': 's', 'sound': 's as in "sun"'},
        {'thai': 'ห/ฮ', 'paiboon': 'h', 'sound': 'h as in "hat"'},
    ],
    
    'vowels': [
        # Note: Short vowels are pronounced as phonic sounds. There is a distinct Thai accent not to be confused with the many English accents!
        {'thai': 'อะ', 'paiboon': 'a', 'sound': 'short "a" as in "bat"'},
        {'thai': 'อา', 'paiboon': 'aa', 'sound': 'long "aa" as in "naa" (น้า)'},
        {'thai': 'อิ', 'paiboon': 'i', 'sound': 'short "i" as in "bit"'},
        {'thai': 'อี', 'paiboon': 'ii', 'sound': 'long "ee" as in "see"'},
        {'thai': 'อึ', 'paiboon': 'ʉ', 'sound': 'short "er" - Bite molar teeth & exaggerate saying "er"'},
        {'thai': 'อื', 'paiboon': 'ʉʉ', 'sound': 'Long "churrr" or Thai chʉʉ - Bite molar teeth & exaggerate saying "churrr"'},
        {'thai': 'อุ', 'paiboon': 'u', 'sound': 'short "u" as in "tuk tuk"'},
        {'thai': 'อู', 'paiboon': 'uu', 'sound': 'long "oo" as in "moon" - Pronounced "muuun"'},
        {'thai': 'เอะ', 'paiboon': 'e', 'sound': 'short "e" as in "ed"'},
        {'thai': 'เอ', 'paiboon': 'ee', 'sound': 'long "ay" as in "day"'},
        {'thai': 'แอะ', 'paiboon': 'ɛ', 'sound': 'short "e" as in "bed" - Stretch mouth wide like a smile, open slightly, tongue on bottom lip, more exaggerated than "e"'},
        {'thai': 'แอ', 'paiboon': 'ɛɛ', 'sound': 'long "ɛɛ" as in "mɛɛ" meaning Mother or like how a sheep goes "mɛɛ!"'},
        {'thai': 'โอะ', 'paiboon': 'o', 'sound': 'short "o"'},
        {'thai': 'โอ', 'paiboon': 'oo', 'sound': 'long "o" as in "go"'},
        {'thai': 'เอาะ', 'paiboon': 'ɔ', 'sound': 'short "aw"'},
        {'thai': 'ออ', 'paiboon': 'ɔɔ', 'sound': 'long "aw" as in "awwww"'},
        {'thai': 'เออะ', 'paiboon': 'ə', 'sound': 'short "er" as in "bird"'},
        {'thai': 'เออ', 'paiboon': 'əə', 'sound': 'long "errr" as in "birrrd"'},
        # Note: If a word ends with a short vowel (eg, "gɔ!" or "a!-ray" or "aa-dta!-maa"), the (!) represents a hard stop on the vowel similar to a stressed syllable.
    ],
    
    'vowel_examples': [
        # a / aa pair
        {
            'vowel': 'a / aa',
            'short': {'thai': 'อะ', 'paiboon': 'a'},
            'long': {'thai': 'อา', 'paiboon': 'aa'},
            'examples': [
                {
                    'thai': 'ขนม / ขนาด',
                    'paiboon': 'kà-nǒm / kà-nàat',
                    'english': 'snack / size',
                    'context': 'Common words',
                    'formality': 'Polite'
                },
                {
                    'thai': 'สนุก / สนาม',
                    'paiboon': 'sà-nùk / sà-nǎam',
                    'english': 'fun / field',
                    'context': 'Daily conversation',
                    'formality': 'Casual'
                },
                {
                    'thai': 'ระวัง / ราคา',
                    'paiboon': 'rá-waŋ / raa-kaa',
                    'english': 'be careful / price',
                    'context': 'Shopping, warning',
                    'formality': 'Polite'
                }
            ]
        },
        
        # i / ii pair
        {
            'vowel': 'i / ii',
            'short': {'thai': 'อิ', 'paiboon': 'i'},
            'long': {'thai': 'อี', 'paiboon': 'ii'},
            'examples': [
                {
                    'thai': 'กิน / กีฬา',
                    'paiboon': 'gin / gii-laa',
                    'english': 'eat / sport',
                    'context': 'Daily activities',
                    'formality': 'Casual'
                },
                {
                    'thai': 'ผิด / ผี',
                    'paiboon': 'pìt / pǐi',
                    'english': 'wrong / ghost',
                    'context': 'Corrections, culture',
                    'formality': 'Polite'
                },
                {
                    'thai': 'พิมพ์ / ที่',
                    'paiboon': 'pim / tîi',
                    'english': 'type/print / at, place',
                    'context': 'Work, locations',
                    'formality': 'Polite'
                }
            ]
        },
        
        # ʉ / ʉʉ pair
        {
            'vowel': 'ʉ / ʉʉ',
            'short': {'thai': 'อึ', 'paiboon': 'ʉ'},
            'long': {'thai': 'อื', 'paiboon': 'ʉʉ'},
            'examples': [
                {
                    'thai': 'ึง / ืด',
                    'paiboon': 'sʉ̀ŋ / dʉ̀ʉt',
                    'english': 'tall building / pull',
                    'context': 'Descriptions, actions',
                    'formality': 'Polite'
                },
                {
                    'thai': 'พึ่ง / พื้น',
                    'paiboon': 'pʉ̂ŋ / pʉ́ʉn',
                    'english': 'just now / floor, ground',
                    'context': 'Time, places',
                    'formality': 'Casual'
                },
                {
                    'thai': 'ึก / ื้อ',
                    'paiboon': 'sʉ̀k / sʉ́ʉ',
                    'english': 'study / buy',
                    'context': 'Daily activities',
                    'formality': 'Polite'
                }
            ]
        },
        
        # u / uu pair
        {
            'vowel': 'u / uu',
            'short': {'thai': 'อุ', 'paiboon': 'u'},
            'long': {'thai': 'อู', 'paiboon': 'uu'},
            'examples': [
                {
                    'thai': 'ุก / ูป',
                    'paiboon': 'tùk / rûup',
                    'english': 'doll / picture, photo',
                    'context': 'Objects',
                    'formality': 'Polite'
                },
                {
                    'thai': 'หนุม / หนู',
                    'paiboon': 'nùm / nǔu',
                    'english': 'young man / mouse, I (humble)',
                    'context': 'People, pronouns',
                    'formality': 'Casual/Polite'
                },
                {
                    'thai': 'ุก / ู้',
                    'paiboon': 'jùk / jûu',
                    'english': 'hurt, sore / kiss',
                    'context': 'Feelings, actions',
                    'formality': 'Casual'
                }
            ]
        },
        
        # e / ee pair
        {
            'vowel': 'e / ee',
            'short': {'thai': 'เอะ', 'paiboon': 'e'},
            'long': {'thai': 'เอ', 'paiboon': 'ee'},
            'examples': [
                {
                    'thai': 'เจ็บ / เจ',
                    'paiboon': 'jèp / jee',
                    'english': 'hurt, pain / letter J',
                    'context': 'Health, spelling',
                    'formality': 'Polite'
                },
                {
                    'thai': 'เล็ก / เล่น',
                    'paiboon': 'lék / lên',
                    'english': 'small / play',
                    'context': 'Descriptions, activities',
                    'formality': 'Casual'
                },
                {
                    'thai': 'เด็ก / เดิน',
                    'paiboon': 'dèk / dəən',
                    'english': 'child / walk',
                    'context': 'People, actions',
                    'formality': 'Polite'
                }
            ]
        },
        
        # ɛ / ɛɛ pair
        {
            'vowel': 'ɛ / ɛɛ',
            'short': {'thai': 'แอะ', 'paiboon': 'ɛ'},
            'long': {'thai': 'แอ', 'paiboon': 'ɛɛ'},
            'examples': [
                {
                    'thai': 'แจก / แจ้ง',
                    'paiboon': 'jɛ̀ɛk / jɛ̂ɛŋ',
                    'english': 'distribute / inform, notify',
                    'context': 'Work, communication',
                    'formality': 'Formal'
                },
                {
                    'thai': 'แพง / แพ้',
                    'paiboon': 'pɛɛŋ / pɛ́ɛ',
                    'english': 'expensive / lose, allergic',
                    'context': 'Shopping, health',
                    'formality': 'Polite'
                },
                {
                    'thai': 'แรก / แรง',
                    'paiboon': 'rɛ̂ɛk / rɛɛŋ',
                    'english': 'first / strong, force',
                    'context': 'Order, descriptions',
                    'formality': 'Polite'
                }
            ]
        },
        
        # o / oo pair
        {
            'vowel': 'o / oo',
            'short': {'thai': 'โอะ', 'paiboon': 'o'},
            'long': {'thai': 'โอ', 'paiboon': 'oo'},
            'examples': [
                {
                    'thai': 'โมง / โมโห',
                    'paiboon': 'mooŋ / moo-hǒo',
                    'english': "o'clock / angry",
                    'context': 'Time, emotions',
                    'formality': 'Polite'
                },
                {
                    'thai': 'โชค / โชว์',
                    'paiboon': 'chôok / choo',
                    'english': 'luck / show (performance)',
                    'context': 'Fortune, entertainment',
                    'formality': 'Casual'
                },
                {
                    'thai': 'โกรธ / โกหก',
                    'paiboon': 'gròot / goo-hòk',
                    'english': 'angry / lie (tell untruth)',
                    'context': 'Emotions, honesty',
                    'formality': 'Polite'
                }
            ]
        },
        
        # ɔ / ɔɔ pair
        {
            'vowel': 'ɔ / ɔɔ',
            'short': {'thai': 'เอาะ', 'paiboon': 'ɔ'},
            'long': {'thai': 'ออ', 'paiboon': 'ɔɔ'},
            'examples': [
                {
                    'thai': 'ก็ / ก่อน',
                    'paiboon': 'gɔ̂ɔ / gɔ̀ɔn',
                    'english': 'also, then / before',
                    'context': 'Connectors, time',
                    'formality': 'Polite'
                },
                {
                    'thai': 'น้อย / น้อง',
                    'paiboon': 'nɔ́ɔi / nɔ́ɔŋ',
                    'english': 'little, few / younger sibling',
                    'context': 'Quantity, family',
                    'formality': 'Casual'
                },
                {
                    'thai': 'ออก / ออกแบบ',
                    'paiboon': 'ɔ̀ɔk / ɔ̀ɔk bɛ̀ɛp',
                    'english': 'exit, go out / design',
                    'context': 'Directions, work',
                    'formality': 'Polite'
                }
            ]
        },
        
        # ə / əə pair (schwa)
        {
            'vowel': 'ə / əə',
            'short': {'thai': 'เออะ', 'paiboon': 'ə'},
            'long': {'thai': 'เออ', 'paiboon': 'əə'},
            'examples': [
                {
                    'thai': 'เลอะ / เบอร์',
                    'paiboon': 'lə́ / bəə',
                    'english': 'dirty, messy / number',
                    'context': 'Cleanliness, contact info',
                    'formality': 'Casual'
                },
                {
                    'thai': 'เปอะ / เดิน',
                    'paiboon': 'bpə̀ / dəən',
                    'english': 'stained / walk',
                    'context': 'Appearance, movement',
                    'formality': 'Polite'
                },
                {
                    'thai': 'เลอะเทอะ / เริ่ม',
                    'paiboon': 'lə́-tə́ / rə̂əm',
                    'english': 'messy, sloppy / start, begin',
                    'context': 'Tidiness, actions',
                    'formality': 'Casual'
                }
            ]
        },
    ],
    
    
    'tone_markers': [
        {'thai': '่', 'name': 'Mai Ek', 'effect': 'Usually low tone'},
        {'thai': '้', 'name': 'Mai Tho', 'effect': 'Usually falling tone'},
        {'thai': '๊', 'name': 'Mai Tri', 'effect': 'Usually high tone'},
        {'thai': '๋', 'name': 'Mai Jattawa', 'effect': 'Usually rising tone'},
    ],
}


# ============================================
# STRUCTURED LESSONS
# ============================================

LESSONS = [
    {
        'id': 1,
        'title': 'Greetings & Introductions',
        'thai_title': 'การทักทาย',
        'level': 'Beginner',
        'objectives': ['Say hello/goodbye', 'Introduce yourself', 'Use polite particles'],
        'sentences': {
            'short': [
                {'thai': 'สวัสดีครับ', 'paiboon': 'sà-wàt-dii kráp', 'english': 'Hello (male)'},
                {'thai': 'ขอบคุณค่ะ', 'paiboon': 'kɔ̀ɔp kun kâ', 'english': 'Thank you (female)'},
            ],
            'long': [
                {'thai': 'ผมชื่อโจชัว ยินดีที่ได้รู้จักครับ', 'paiboon': 'pǒm chʉ̂ʉ joo-chuua yin-dii tîi dâi rúu-jàk kráp', 'english': 'My name is Joshua, nice to meet you'},
            ]
        }
    },
    {
        'id': 2,
        'title': 'Numbers & Counting',
        'thai_title': 'ตัวเลข',
        'level': 'Beginner',
        'objectives': ['Count 1-100', 'Use classifiers', 'Ask prices'],
        'sentences': {
            'short': [
                {'thai': 'หนึ่ง สอง สาม', 'paiboon': 'nʉ̀ŋ sɔ̌ɔŋ sǎam', 'english': 'One, two, three'},
            ],
            'long': [
                {'thai': 'ขอน้ำสองแก้วครับ', 'paiboon': 'kɔ̌ɔ náam sɔ̌ɔŋ gɛ̂ɛo kráp', 'english': 'Two glasses of water please'},
            ]
        }
    },
    {
        'id': 3,
        'title': 'Food & Eating',
        'thai_title': 'อาหาร',
        'level': 'Beginner',
        'objectives': ['Order food', 'Express taste preferences'],
        'sentences': {
            'short': [
                {'thai': 'อร่อยมาก', 'paiboon': 'à-ròi mâak', 'english': 'Very delicious'},
            ],
            'long': [
                {'thai': 'ขอผัดไทยไม่ใส่ถั่วครับ', 'paiboon': 'kɔ̌ɔ pàt-tai mâi sài tùa kráp', 'english': 'Pad Thai without peanuts'},
            ]
        }
    },
    {
        'id': 4,
        'title': 'Directions',
        'thai_title': 'ทิศทาง',
        'level': 'Beginner',
        'objectives': ['Ask directions', 'Understand location words'],
        'sentences': {
            'short': [
                {'thai': 'ไปไหน', 'paiboon': 'bpai nǎi', 'english': 'Where going?'},
                {'thai': 'เลี้ยวขวา', 'paiboon': 'líao kwǎa', 'english': 'Turn right'},
            ],
            'long': [
                {'thai': 'ห้องน้ำอยู่ที่ไหนครับ', 'paiboon': 'hɔ̂ŋ-náam yùu tîi nǎi kráp', 'english': 'Where is the bathroom?'},
            ]
        }
    },
    {
        'id': 5,
        'title': 'Time & Days',
        'thai_title': 'เวลาและวัน',
        'level': 'Beginner',
        'objectives': ['Tell time', 'Days of the week'],
        'sentences': {
            'short': [
                {'thai': 'กี่โมง', 'paiboon': 'gìi mooŋ', 'english': 'What time?'},
            ],
            'long': [
                {'thai': 'วันนี้วันจันทร์', 'paiboon': 'wan-níi wan jan', 'english': 'Today is Monday'},
            ]
        }
    },
    {
        'id': 6,
        'title': 'Shopping',
        'thai_title': 'ซื้อของ',
        'level': 'Intermediate',
        'objectives': ['Bargain prices', 'Compare products'],
        'sentences': {
            'short': [
                {'thai': 'แพงไป', 'paiboon': 'pɛɛŋ bpai', 'english': 'Too expensive'},
            ],
            'long': [
                {'thai': 'ลดราคาได้ไหมครับ', 'paiboon': 'lót raa-kaa dâi mǎi kráp', 'english': 'Can you reduce the price?'},
            ]
        }
    },
    {
        'id': 7,
        'title': 'Family',
        'thai_title': 'ครอบครัว',
        'level': 'Intermediate',
        'objectives': ['Describe family', 'Use kinship terms'],
        'sentences': {
            'short': [
                {'thai': 'มีพี่น้องไหม', 'paiboon': 'mii pîi-nɔ́ɔŋ mǎi', 'english': 'Do you have siblings?'},
            ],
            'long': [
                {'thai': 'ครอบครัวผมมีสี่คน', 'paiboon': 'krɔ̂ɔp-kruua pǒm mii sìi kon', 'english': 'My family has four people'},
            ]
        }
    },
    {
        'id': 8,
        'title': 'Health',
        'thai_title': 'สุขภาพ',
        'level': 'Intermediate',
        'objectives': ['Describe symptoms', 'Seek medical help'],
        'sentences': {
            'short': [
                {'thai': 'ไม่สบาย', 'paiboon': 'mâi sà-baai', 'english': "I don't feel well"},
            ],
            'long': [
                {'thai': 'ผมปวดหัวมาก', 'paiboon': 'pǒm bpùuat hǔua mâak', 'english': 'I have a bad headache'},
            ]
        }
    },
    {
        'id': 9,
        'title': 'Weather',
        'thai_title': 'อากาศ',
        'level': 'Intermediate',
        'objectives': ['Discuss weather', 'Describe seasons'],
        'sentences': {
            'short': [
                {'thai': 'ร้อนมาก', 'paiboon': 'rɔ́ɔn mâak', 'english': 'Very hot'},
            ],
            'long': [
                {'thai': 'วันนี้อากาศดีมาก', 'paiboon': 'wan-níi aa-gàat dii mâak', 'english': 'The weather is very nice today'},
            ]
        }
    },
    {
        'id': 10,
        'title': 'Temple Etiquette',
        'thai_title': 'มารยาทในวัด',
        'level': 'Intermediate',
        'objectives': ['Visit temples properly', 'Make merit'],
        'sentences': {
            'short': [
                {'thai': 'กราบพระ', 'paiboon': 'gràap prá', 'english': 'Pay respect to monks'},
            ],
            'long': [
                {'thai': 'ถอดรองเท้าก่อนเข้าโบสถ์', 'paiboon': 'tɔ̀ɔt rɔɔŋ-táao gɔ̀ɔn kâo bòot', 'english': 'Remove shoes before entering chapel'},
            ]
        }
    },
    {
        'id': 11,
        'title': 'Thai Culture',
        'thai_title': 'วัฒนธรรม',
        'level': 'Intermediate',
        'objectives': ['Understand cultural norms', 'Show respect'],
        'sentences': {
            'short': [
                {'thai': 'ไหว้ผู้ใหญ่', 'paiboon': 'wâai pûu-yài', 'english': 'Wai to elders'},
            ],
            'long': [
                {'thai': 'คนไทยเคารพผู้ใหญ่มาก', 'paiboon': 'kon tai kao-róp pûu-yài mâak', 'english': 'Thai people greatly respect elders'},
            ]
        }
    },
    {
        'id': 12,
        'title': 'Buddhist Concepts',
        'thai_title': 'แนวคิดพุทธ',
        'level': 'Advanced',
        'objectives': ['Discuss Buddhist teachings', 'Use Dharma vocabulary'],
        'sentences': {
            'short': [
                {'thai': 'ทำดีได้ดี', 'paiboon': 'tam dii dâi dii', 'english': 'Do good, receive good'},
            ],
            'long': [
                {'thai': 'การปฏิบัติธรรมช่วยให้มีสติ', 'paiboon': 'gaan bpà-dtì-bàt tam chûuai hâi mii sà-dtì', 'english': 'Practicing Dharma helps develop mindfulness'},
            ]
        }
    },
    {
        'id': 13,
        'title': 'Isan Language',
        'thai_title': 'ภาษาอีสาน',
        'level': 'Advanced',
        'objectives': ['Understand Isan dialect', 'Learn regional expressions'],
        'sentences': {
            'short': [
                {'thai': 'แซบหลาย', 'paiboon': 'sɛ̂ɛp lǎai', 'english': 'Very delicious (Isan)'},
            ],
            'long': [
                {'thai': 'คนอีสานมีน้ำใจดีคัก', 'paiboon': 'kon ii-sǎan mii nám-jai dii kák', 'english': 'Isan people are very kind-hearted'},
            ]
        }
    },
    {
        'id': 14,
        'title': 'Thai Script',
        'thai_title': 'อักษรไทย',
        'level': 'Advanced',
        'objectives': ['Recognize consonant classes', 'Understand tone rules'],
        'sentences': {
            'short': [
                {'thai': 'อ่านได้ไหม', 'paiboon': 'àan dâi mǎi', 'english': 'Can you read?'},
            ],
            'long': [
                {'thai': 'ภาษาไทยมีพยัญชนะสี่สิบสี่ตัว', 'paiboon': 'paa-sǎa tai mii pá-yan-chá-ná sìi-sìp-sìi dtuua', 'english': 'Thai has 44 consonants'},
            ]
        }
    },
    {
        'id': 15,
        'title': 'Meditation',
        'thai_title': 'การทำสมาธิ',
        'level': 'Advanced',
        'objectives': ['Understand meditation terms', 'Follow instructions in Thai'],
        'sentences': {
            'short': [
                {'thai': 'หายใจเข้า', 'paiboon': 'hǎai-jai kâo', 'english': 'Breathe in'},
                {'thai': 'หายใจออก', 'paiboon': 'hǎai-jai ɔ̀ɔk', 'english': 'Breathe out'},
            ],
            'long': [
                {'thai': 'นั่งสมาธิทุกวันช่วยให้จิตใจสงบ', 'paiboon': 'nâŋ sà-maa-tí túk wan chûuai hâi jìt-jai sà-ŋòp', 'english': 'Meditating daily helps calm the mind'},
            ]
        }
    },
]


# ============================================
# CULTURAL STORIES
# ============================================

CULTURAL_STORIES = {
    'festivals': {
        'title': 'The Legend of Loy Krathong',
        'story': '''Long ago in Sukhothai, Nang Noppamas crafted a floating vessel from banana leaves, 
decorated with flowers and candles. She set it on the water as an offering to the Water Goddess.
The King declared it an annual tradition. Today, Thai people release krathongs to let go of negativity.''',
        'lesson': 'Gratitude for nature, forgiveness, and letting go.',
    },
    'nature': {
        'title': 'The Elephant and the Bodhi Tree',
        'story': '''A wise elephant found a struggling Bodhi sapling during drought. Every day he carried 
water to nourish it. Years later, when the elephant grew old, the tree provided shade and its roots 
found water for a spring. The elephant spent his final days in peace beneath the tree.''',
        'lesson': 'Kindness returns to us. All beings are interconnected.',
    },
    'buddhist_formal': {
        'title': 'The First Sermon at Deer Park',
        'story': '''After enlightenment, the Buddha walked to Deer Park to teach his five former companions.
He delivered the Dhammacakkappavattana Sutta, teaching the Middle Way and Four Noble Truths.
Kondanna immediately understood and became the first enlightened disciple.''',
        'lesson': 'The Middle Way, Four Noble Truths, and the Dharma is available to all.',
    },
    'theravada_dhamma': {
        'title': "Angulimala's Transformation",
        'story': '''Angulimala was a terrifying bandit who had killed 999 people. The Buddha intercepted him,
walking calmly though Angulimala could not catch him. "I have stopped harming beings. It is you 
who have not stopped," said the Buddha. These words pierced Angulimala's heart, and he became a monk,
eventually attaining enlightenment.''',
        'lesson': 'Transformation is possible for anyone through the power of compassion.',
    },
    'schwa_words': {
        'title': 'Modern Thailand and Global Connection',
        'story': '''Modern Thai has absorbed many English loanwords, especially in technology, business, and 
education. These words often use the schwa sound (ə/əə) - that "uh" sound from English. When foreign monks 
first arrived in Bangkok, they noticed shopkeepers saying "เบอร์" (bəə - number) and "เทอม" (təəm - term). 
Thai people have skillfully adapted foreign words while maintaining their own language's beauty. This shows 
Thailand's openness to the world while preserving cultural identity.''',
        'lesson': 'Language evolves through cultural exchange. Learning both traditional and modern vocabulary shows respect for Thai culture.',
    },
}


# ============================================
# CULTURAL INFO
# ============================================

CULTURAL_INFO = {
    'greetings_hello_goodbye': {
        'name': 'Thai Greetings - สวัสดี & ลาก่อน',
        'thai_title': 'การทักทายและการลาภาษาไทย',
        'paiboon_title': 'gaan ták-taai lɛ́ gaan laa paa-sǎa tai',
        'category': 'Daily Communication',
        'importance': 'Essential',
        'description': 'Understanding Thai greetings is fundamental to respectful communication. The same word สวัสดี (sà-wàt-dii) serves for hello, good morning, afternoon, and evening - simplifying daily interactions!',
        
        'hello': {
            'title': 'Hello - สวัสดี',
            'base_word': {
                'thai': 'สวัสดี',
                'paiboon': 'sà-wàt-dii',
                'meaning': 'hello, good morning/afternoon/evening',
                'etymology': 'From Sanskrit "svasti" meaning well-being, blessing'
            },
            'male_form': {
                'thai': 'สวัสดีครับ',
                'paiboon': 'sà-wàt-dii kráp',
                'breakdown': 'สวัสดี (greeting) + ครับ (male polite particle)',
                'usage': 'Standard polite greeting for males',
                'formality': 'Polite - use with everyone'
            },
            'female_form': {
                'thai': 'สวัสดีค่ะ',
                'paiboon': 'sà-wàt-dii kâ',
                'breakdown': 'สวัสดี (greeting) + ค่ะ (female polite particle)',
                'usage': 'Standard polite greeting for females',
                'formality': 'Polite - use with everyone'
            },
            'monk_form': {
                'thai': 'สวัสดีท่านอาจารย์',
                'paiboon': 'sà-wàt-dii tân aa-jaan',
                'breakdown': 'สวัสดี (greeting) + ท่าน (respected person) + อาจารย์ (teacher/monk)',
                'usage': 'Greeting Buddhist monks or respected teachers',
                'formality': 'Monastic - highest respect'
            },
            'key_insight': {
                'point': 'Universal Time Greeting',
                'explanation': 'Unlike English, สวัสดี works for ANY time of day! This makes life easier - one greeting covers morning, noon, and night. Just add your polite particle (ครับ/ค่ะ) and you\'re set.'
            },
            'cultural_notes': [
                'Always pair with appropriate wai gesture (see Wai section below)',
                'The polite particles ครับ/ค่ะ are NOT optional in formal situations',
                'Can be repeated: "สวัสดีครับ สวัสดีครับ" shows extra friendliness',
                'In temples, greet monks with palms together at forehead level'
            ]
        },
        
        'hi_casual': {
            'title': 'Hi (Casual) - หวัดดี',
            'base_word': {
                'thai': 'หวัดดี',
                'paiboon': 'wàt-dii',
                'meaning': 'hi (shortened, casual form)',
                'origin': 'Shortened from สวัสดี, dropping the ส sound'
            },
            'male_form': {
                'thai': 'หวัดดีครับ',
                'paiboon': 'wàt-dii kráp',
                'usage': 'Casual greeting among male friends',
                'formality': 'Casual - peers only'
            },
            'female_form': {
                'thai': 'หวัดดีค่ะ',
                'paiboon': 'wàt-dii kâ',
                'usage': 'Casual greeting among female friends',
                'formality': 'Casual - peers only'
            },
            'when_to_use': 'With close friends, younger people you know well, or peers. AVOID with: elders, monks, bosses, strangers, formal situations.',
            'comparison': 'Think of it like "hi" vs "hello" - หวัดดี is the relaxed version of สวัสดี'
        },
        
        'goodbye': {
            'title': 'Goodbye - ลาก่อน',
            'primary': {
                'thai': 'สวัสดี',
                'paiboon': 'sà-wàt-dii',
                'meaning': 'goodbye (yes, same as hello!)',
                'male': 'สวัสดีครับ (sà-wàt-dii kráp)',
                'female': 'สวัสดีค่ะ (sà-wàt-dii kâ)',
                'note': 'Context determines if it\'s hello or goodbye'
            },
            'formal_goodbye': {
                'thai': 'ลาก่อน',
                'paiboon': 'laa-gɔ̀ɔn',
                'meaning': 'goodbye, farewell',
                'male': 'ลาก่อนครับ (laa-gɔ̀ɔn kráp)',
                'female': 'ลาก่อนค่ะ (laa-gɔ̀ɔn kâ)',
                'usage': 'More formal parting, longer separations',
                'breakdown': 'ลา (part, take leave) + ก่อน (first, before)'
            },
            'see_you_again': {
                'thai': 'แล้วพบกันใหม่',
                'paiboon': 'lɛ́ɛo póp gan mài',
                'meaning': 'see you again, until we meet again',
                'male': 'แล้วพบกันใหม่ครับ (lɛ́ɛo póp gan mài kráp)',
                'female': 'แล้วพบกันใหม่ค่ะ (lɛ́ɛo póp gan mài kâ)',
                'usage': 'Friendly, anticipating future meeting',
                'breakdown': 'แล้ว (then) + พบ (meet) + กัน (each other) + ใหม่ (new/again)'
            },
            'cultural_notes': [
                'สวัสดี works for 90% of goodbye situations',
                'ลาก่อน feels more definite, like a longer separation',
                'Monks receive: สวัสดีท่านอาจารย์ (sà-wàt-dii tân aa-jaan)',
                'Combine with appropriate wai gesture when leaving'
            ]
        },
        
        'practical_scenarios': {
            'entering_shop': {
                'situation': 'Walking into a store',
                'male': 'สวัสดีครับ (sà-wàt-dii kráp)',
                'female': 'สวัสดีค่ะ (sà-wàt-dii kâ)',
                'tip': 'Shopkeeper will likely respond with same greeting'
            },
            'leaving_temple': {
                'situation': 'Leaving temple after speaking with monk',
                'male': 'สวัสดีครับ ท่านอาจารย์ (sà-wàt-dii kráp tân aa-jaan)',
                'female': 'สวัสดีค่ะ ท่านอาจารย์ (sà-wàt-dii kâ tân aa-jaan)',
                'tip': 'Wai with hands at forehead level, bow slightly'
            },
            'casual_friends': {
                'situation': 'Meeting friends at coffee shop',
                'male': 'หวัดดีครับ (wàt-dii kráp)',
                'female': 'หวัดดีค่ะ (wàt-dii kâ)',
                'tip': 'Casual form OK with peers, slight wai or nod'
            },
            'formal_business': {
                'situation': 'Business meeting',
                'male': 'สวัสดีครับ (sà-wàt-dii kráp) + proper wai',
                'female': 'สวัสดีค่ะ (sà-wàt-dii kâ) + proper wai',
                'tip': 'Always full สวัสดี, never shortened form'
            }
        },
        
        'common_mistakes': [
            {
                'mistake': 'Forgetting polite particles',
                'wrong': 'สวัสดี (alone)',
                'right': 'สวัสดีครับ/ค่ะ',
                'why': 'Without ครับ/ค่ะ sounds abrupt, even rude in formal contexts'
            },
            {
                'mistake': 'Using หวัดดี with elders/monks',
                'wrong': 'หวัดดีครับ (to monk)',
                'right': 'สวัสดีครับ ท่านอาจารย์',
                'why': 'หวัดดี is too casual for respect situations'
            },
            {
                'mistake': 'Male using female particle',
                'wrong': 'สวัสดีค่ะ (male speaker)',
                'right': 'สวัสดีครับ',
                'why': 'ค่ะ/คะ are exclusively female, ครับ exclusively male'
            }
        ],
        
        'formality_guide': {
            'monastic': {
                'form': 'สวัสดีท่านอาจารย์ (sà-wàt-dii tân aa-jaan)',
                'when': 'Monks, high-ranking teachers, Buddha images',
                'wai': 'Hands at forehead, deep bow'
            },
            'formal': {
                'form': 'สวัสดีครับ/ค่ะ (sà-wàt-dii kráp/kâ)',
                'when': 'Strangers, bosses, elders, official settings',
                'wai': 'Hands at nose level, respectful'
            },
            'polite': {
                'form': 'สวัสดีครับ/ค่ะ (sà-wàt-dii kráp/kâ)',
                'when': 'Most daily interactions, default choice',
                'wai': 'Hands at chin level, friendly'
            },
            'casual': {
                'form': 'หวัดดีครับ/ค่ะ (wàt-dii kráp/kâ)',
                'when': 'Close friends, peers, casual settings',
                'wai': 'Slight nod or small wai, relaxed'
            }
        }
    },
    
    'wai_gesture': {
        'name': 'The Wai - ไหว้',
        'thai_title': 'การไหว้',
        'paiboon_title': 'gaan wâi',
        'category': 'Body Language & Etiquette',
        'importance': 'Critical',
        'description': 'The wai (ไหว้) is Thailand\'s signature gesture - a prayer-like hand position that conveys respect, greeting, gratitude, and apology. Mastering the wai is essential for cultural fluency.',
        
        'basic_concept': {
            'thai': 'ไหว้',
            'paiboon': 'wâi',
            'meaning': 'to pay respect, to greet with palms together',
            'gesture': 'Press palms together in prayer position, bow slightly',
            'cultural_roots': 'Ancient Indian/Buddhist tradition, represents lotus bud, shows humility and respect'
        },
        
        'three_levels': {
            'explanation': 'The wai has THREE distinct levels based on the social hierarchy, age, and status of the person you\'re greeting. Height of hands and depth of bow indicate respect level.',
            
            'level_1_peers': {
                'name': 'General Greeting (เพื่อน - Friends/Peers)',
                'thai': 'การไหว้ทั่วไป',
                'paiboon': 'gaan wâi tûa-bpai',
                'hand_position': 'Palms together at chest level',
                'fingertips': 'At chin or lower face level',
                'bow': 'Slight bow, barely noticeable',
                'usage': 'Greeting peers, friends, or people of equal status',
                'examples': [
                    'Coworkers at same level',
                    'Friends of similar age',
                    'Shop staff greeting customers',
                    'Service workers to customers'
                ],
                'note': 'The most common wai you\'ll give and receive'
            },
            
            'level_2_respect': {
                'name': 'Respectful Greeting (ผู้ใหญ่ - Elders/Superiors)',
                'thai': 'การไหว้ด้วยความเคารพ',
                'paiboon': 'gaan wâi dûuai kwaam kao-róp',
                'hand_position': 'Palms together with fingertips touching nose',
                'fingertips': 'At nose tip level',
                'bow': 'Moderate bow, clearly visible',
                'usage': 'Greeting people slightly older or of higher status',
                'examples': [
                    'Parents and relatives',
                    'Teachers and professors',
                    'Bosses and supervisors',
                    'Older strangers (clearly senior)',
                    'Government officials'
                ],
                'note': 'Shows proper respect for Thai social hierarchy'
            },
            
            'level_3_highest': {
                'name': 'Highest Respect (พระ - Monks/Royalty)',
                'thai': 'การไหว้ด้วยความเคารพสูงสุด',
                'paiboon': 'gaan wâi dûuai kwaam kao-róp sǔuŋ-sùt',
                'hand_position': 'Palms together with thumbs touching between eyebrows, fingertips at hairline',
                'fingertips': 'At forehead/hairline level',
                'bow': 'Deep bow, sometimes to the point of kneeling',
                'usage': 'Reserved for monks, Buddha images, and royalty ONLY',
                'examples': [
                    'Buddhist monks (พระ - prá)',
                    'Buddha images and statues',
                    'Thai royal family members',
                    'Extremely revered teachers (rare)'
                ],
                'critical_note': 'This is called "wai pra" (ไหว้พระ) - wai to monks. NEVER used casually!'
            }
        },
        
        'who_wais_whom': {
            'rule': 'Generally, younger/lower status person wais FIRST to older/higher status person',
            'hierarchy': [
                'Children wai adults (adults may not return)',
                'Students wai teachers (teacher returns)',
                'Employee wais boss (boss may return)',
                'Younger wais older (older returns)',
                'Service staff wai customers (customer may/may not return)',
                'Everyone wais monks (monks do NOT return wai)'
            ],
            'key_insight': 'It\'s better to wai when unsure than to NOT wai when you should. Thais appreciate foreigners who try!'
        },
        
        'when_not_to_wai': {
            'dont_wai_to': [
                {
                    'who': 'Children',
                    'reason': 'Adults don\'t wai to young children (though children should wai to adults)',
                    'exception': 'Parents may return child\'s wai affectionately'
                },
                {
                    'who': 'Service workers when you are the customer',
                    'reason': 'They wai to you; you may smile/nod or light wai back',
                    'exception': 'You can wai to thank them if you want'
                },
                {
                    'who': 'Street vendors during transaction',
                    'reason': 'Not expected during business exchange',
                    'exception': 'Can wai after transaction as thanks'
                },
                {
                    'who': 'Monks as initiation',
                    'reason': 'Wait for monk\'s blessing/acknowledgment first',
                    'exception': 'Wai upon arrival/departure at temple'
                }
            ],
            'special_cases': {
                'monks': 'Monks NEVER return wais - they give blessings instead. Don\'t expect a wai back!',
                'royalty': 'In presence of royalty, follow others\' lead. Don\'t initiate.',
                'foreigners': 'Thais don\'t expect foreigners to wai, but deeply appreciate it when you do correctly'
            }
        },
        
        'wai_with_words': {
            'greeting_plus_wai': [
                {
                    'situation': 'Meeting elder',
                    'words_male': 'สวัสดีครับ (sà-wàt-dii kráp)',
                    'words_female': 'สวัสดีค่ะ (sà-wàt-dii kâ)',
                    'wai': 'Level 2 (fingertips at nose)',
                    'timing': 'Wai AS you speak the greeting'
                },
                {
                    'situation': 'Thanking someone',
                    'words_male': 'ขอบคุณครับ (kɔ̀ɔp-kun kráp)',
                    'words_female': 'ขอบคุณค่ะ (kɔ̀ɔp-kun kâ)',
                    'wai': 'Match their status level',
                    'timing': 'Wai while saying thank you'
                },
                {
                    'situation': 'Apologizing',
                    'words_male': 'ขอโทษครับ (kɔ̌ɔ-tôot kráp)',
                    'words_female': 'ขอโทษค่ะ (kɔ̌ɔ-tôot kâ)',
                    'wai': 'Slightly deeper bow shows sincerity',
                    'timing': 'Wai before and during apology'
                },
                {
                    'situation': 'At temple with monk',
                    'words_male': 'สวัสดีครับ ท่านอาจารย์ (sà-wàt-dii kráp tân aa-jaan)',
                    'words_female': 'สวัสดีค่ะ ท่านอาจารย์ (sà-wàt-dii kâ tân aa-jaan)',
                    'wai': 'Level 3 (hands at forehead)',
                    'timing': 'Wai deeply, wait for acknowledgment'
                }
            ]
        },
        
        'foreigner_guidelines': {
            'reciprocation': {
                'rule': 'If someone wais you, it\'s polite to return it',
                'how': 'Match or slightly exceed their wai level',
                'exception': 'If they\'re clearly service staff, a smile or nod is OK'
            },
            'initiation': {
                'rule': 'As a foreigner, you\'re NOT expected to initiate wai',
                'but': 'Doing so appropriately shows deep respect and cultural understanding',
                'appreciated': 'Thais will be impressed and pleased when foreigners wai correctly'
            },
            'exceptions_no_wai': [
                'Do NOT wai to children (smile/nod instead)',
                'Do NOT wai to service staff (let them wai to you)',
                'Nod and smile is always acceptable if unsure'
            ],
            'when_to_definitely_wai': [
                'When entering/leaving a temple',
                'When greeting a monk',
                'When meeting elder Thai family members',
                'When sincerely thanking someone for big help',
                'When apologizing for something serious'
            ]
        },
        
        'common_mistakes': [
            {
                'mistake': 'Wai while holding something',
                'wrong': 'Wai with phone/bag in hand',
                'right': 'Put items down first, then wai',
                'why': 'Shows carelessness, like distracted respect'
            },
            {
                'mistake': 'Wai too high for peers',
                'wrong': 'Hands at forehead for coworker',
                'right': 'Hands at chest for peer',
                'why': 'Looks awkward, they\'ll think you don\'t understand culture'
            },
            {
                'mistake': 'Expecting monk to wai back',
                'wrong': 'Waiting for return wai from monk',
                'right': 'Give wai, accept blessing, don\'t expect return',
                'why': 'Monks don\'t return wais - it\'s not their role'
            },
            {
                'mistake': 'No wai at temple',
                'wrong': 'Walking past Buddha image without wai',
                'right': 'Always wai to Buddha images',
                'why': 'Deeply disrespectful not to wai to sacred images'
            }
        ],
        
        'practical_scenarios': [
            {
                'scenario': 'Entering a temple (วัด - wát)',
                'action': 'Wai to Buddha image at main hall',
                'level': 'Level 3 - highest respect',
                'words': 'Silent wai, or นมัสการพระ (ná-má-sà-gaan prá)',
                'notes': 'Feet toward exit, head toward Buddha. Remove shoes!'
            },
            {
                'scenario': 'Meeting Thai friend\'s parents',
                'action': 'Wai when introduced',
                'level': 'Level 2 - respectful',
                'words': 'สวัสดีครับ/ค่ะ (sà-wàt-dii kráp/kâ)',
                'notes': 'Parents will appreciate foreigner showing respect'
            },
            {
                'scenario': 'Server brings your food',
                'action': 'Smile and nod (or light wai if you want)',
                'level': 'Level 1 or no wai',
                'words': 'ขอบคุณครับ/ค่ะ (kɔ̀ɔp-kun kráp/kâ)',
                'notes': 'They wai to you; returning is optional'
            },
            {
                'scenario': 'Leaving monk after Dharma talk',
                'action': 'Deep wai with forehead to ground if sitting',
                'level': 'Level 3 - prostration possible',
                'words': 'ขอบพระคุณครับ/ค่ะ (kɔ̀ɔp prá-kun kráp/kâ)',
                'notes': 'Show maximum gratitude for teaching'
            }
        ],
        
        'cultural_depth': {
            'lotus_symbolism': 'Hands together represent lotus bud - symbol of purity rising from mud (samsara to enlightenment)',
            'namaste_connection': 'Related to Indian "namaste" but uniquely Thai in execution and social rules',
            'social_glue': 'The wai maintains Thailand\'s hierarchical society while allowing fluid respect exchange',
            'tourist_respect': 'Foreigners attempting proper wai are deeply respected - shows you honor Thai culture'
        },
        
        'quick_reference': {
            'peer_greeting': {
                'hands': 'Chest level',
                'bow': 'Slight',
                'when': 'Friends, coworkers, peers'
            },
            'elder_respect': {
                'hands': 'Nose level',
                'bow': 'Moderate',
                'when': 'Parents, teachers, bosses'
            },
            'highest_honor': {
                'hands': 'Forehead level',
                'bow': 'Deep',
                'when': 'Monks, Buddha, royalty ONLY'
            }
        }
    },
    
    'songkran': {
        'name': 'Songkran - สงกรานต์',
        'description': 'Thai New Year with water splashing and family gatherings.',
        'date': 'April 13-15',
    },
    'loy_krathong': {
        'name': 'Loy Krathong - ลอยกระทง',
        'description': 'Festival of floating lanterns honoring the water goddess.',
        'date': 'Full moon of November',
    },
    'visakha_bucha': {
        'name': 'Visakha Bucha - วันวิสาขบูชา',
        'description': "Commemorates Buddha's birth, enlightenment, and death.",
        'date': 'Full moon of May',
    },
}


# ============================================
# DICTIONARY REFERENCE
# ============================================

DICTIONARY_REFERENCE = {
    'title': 'Thai-English English-Thai Dictionary',
    'subtitle': 'With Classifiers and Tones for English Speakers',
    'author': 'Benjawan Poomsan Becker',
    'publisher': 'Paiboon Publishing',
    'description': '''The definitive reference for English speakers learning Thai using 
the Paiboon romanization system. Features tone marks, classifiers, and cultural notes.''',
    'features': [
        'Over 10,000 entries with tone marks',
        'Classifiers listed for all nouns',
        'Common phrases and expressions',
        'Clear pronunciation guide',
    ],
    'online_resources': {
        'slice_of_thai': {
            'name': 'Slice of Thai - Interactive Sound Guide',
            'url': 'http://slice-of-thai.com/language',
            'description': 'Listen to audio examples of all Thai sounds, tones, and sample words. Perfect for practicing pronunciation!'
        }
    }
}


# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    # Set default gender if not set
    if 'user_gender' not in session:
        session['user_gender'] = 'neutral'
    return render_template('index.html', current_gender=session.get('user_gender', 'neutral'))


@app.route('/set-gender/<gender>')
def set_gender(gender):
    """Set user's gender preference for appropriate language use"""
    if gender in ['male', 'female', 'neutral']:
        session['user_gender'] = gender
        return jsonify({'success': True, 'gender': gender})
    return jsonify({'success': False, 'error': 'Invalid gender'})


@app.route('/monk-mode', methods=['GET', 'POST'])
def monk_mode():
    """The Monk Mode access page.

    GET  — explains who Monk Mode is for and shows a code-entry form (or, if
           it's already on, an 'active' state with a switch-off button).
    POST — checks the submitted access code. A valid code switches Monk Mode on
           for this session; an invalid one re-renders the page with a gentle
           error. Turning it ON always requires a valid code.
    """
    init_user_progress()
    error = None
    if request.method == 'POST':
        code = request.form.get('code', '')
        if is_valid_monk_code(code):
            session['user_progress']['monk_mode'] = True
            session.modified = True
            return redirect(url_for('monk_mode'))
        error = "That code wasn't recognised. Please check with the temple or teacher who shared it with you."
    return render_template(
        'monk_mode.html',
        active=session['user_progress'].get('monk_mode', False),
        error=error,
    )


@app.route('/set-monk-mode/off')
def set_monk_mode_off():
    """Switch Monk Mode off. No code is needed to turn it off — only to turn it
    on (see the /monk-mode route)."""
    init_user_progress()
    session['user_progress']['monk_mode'] = False
    session.modified = True
    return jsonify({'success': True, 'monk_mode': False})


@app.route('/set-monk-direction/<direction>')
def set_monk_direction(direction):
    """Switch the monk lessons between 'learn_thai' (a Western monk) and
    'learn_english' (a Thai monk). Flips which language is the prompt."""
    init_user_progress()
    if direction in MONK_DIRECTIONS:
        session['user_progress']['monk_direction'] = direction
        session.modified = True
    return jsonify({'success': True, 'direction': monk_direction()})


@app.route('/monk/lessons')
def monk_lessons():
    """The monk lesson track — a grid of topics. Only available in Monk Mode."""
    if not monk_mode_active():
        return redirect(url_for('monk_mode'))
    return render_template('monk_lessons.html', topics=MONK_TOPICS, direction=monk_direction())


@app.route('/monk/lesson/<topic>')
def monk_lesson_detail(topic):
    """A single monk topic, rendered in the current learning direction."""
    if not monk_mode_active():
        return redirect(url_for('monk_mode'))
    lesson = MONK_TOPICS_BY_ID.get(topic)
    if not lesson:
        return redirect(url_for('monk_lessons'))
    return render_template('monk_lesson_detail.html', lesson=lesson, direction=monk_direction())


@app.route('/monk/pronunciation')
def monk_pronunciation_guide():
    """Teaches the two pronunciation notations used on the English side.

    The respelling is what every learner sees by default, so it is taught first
    and at length. IPA is the optional layer, taught second for those who want
    it (or for teachers). Mirrors what /paiboon does for the Thai side.
    """
    if not monk_mode_active():
        return redirect(url_for('monk_mode'))
    return render_template('monk_pronunciation.html', direction=monk_direction())


@app.route('/gender-examples')
@require_access('gender_examples')
def gender_examples():
    """Show all gender variations with formality"""
    gender = session.get('user_gender', 'neutral')
    
    # Build examples for all formality levels
    examples = {
        'formal': build_sentence(gender, 'formal', True),
        'polite': build_sentence(gender, 'polite', True),
        'neutral': build_sentence(gender, 'neutral', False),
        'casual': build_sentence(gender, 'casual', False)
    }
    
    # Get greetings
    greetings = {}
    for greeting_type in ['hello', 'thank_you', 'goodbye', 'excuse_me']:
        greetings[greeting_type] = {}
        for formality in ['formal', 'polite', 'casual']:
            greetings[greeting_type][formality] = get_gendered_text('greetings', greeting_type, formality, gender)
    
    return render_template('gender_examples.html', 
                         gender=gender, 
                         examples=examples, 
                         greetings=greetings,
                         gender_variants=GENDER_VARIANTS)


@app.route('/learn')
def learn():
    categories = [{'id': k, 'name': k.replace('_', ' ').title(), 'word_count': len(v)} 
                  for k, v in VOCABULARY.items()]
    return render_template('learn.html', categories=categories)


@app.route('/culture')
@require_access('culture')
def culture():
    return render_template('culture.html', cultural_info=CULTURAL_INFO, stories=CULTURAL_STORIES)


@app.route('/exercise/<category>')
def exercise(category):
    # Check category-specific access
    has_access, message = check_section_access(f'exercise_{category}')
    if not has_access:
        return render_template('locked.html', 
                             section=f'exercise_{category}',
                             message=message,
                             requirements=SECTION_REQUIREMENTS.get(f'exercise_{category}', {}),
                             user_progress=session['user_progress'])
    
    beginner_mode = request.args.get('beginner', 'false').lower() == 'true'
    
    if category not in VOCABULARY:
        return f"Category '{category}' not found. <a href='/learn'>Back to Learn</a>", 404
    
    vocab_list = get_vocab_with_mode(VOCABULARY[category], beginner_mode)
    story = CULTURAL_STORIES.get(category)
    
    session['current_vocab'] = vocab_list
    session['current_category'] = category
    session['beginner_mode'] = beginner_mode
    
    return render_template('exercise.html', category=category, vocab=vocab_list, 
                         story=story, beginner_mode=beginner_mode)



# ============================================
# SENTENCE PATTERNS & CONVERSATIONS
# ============================================

SENTENCE_PATTERNS = {
    'aspect_markers': {
        'title': 'Aspect Markers - Showing Time & Completion',
        'explanation': 'Thai uses particles to show whether actions are ongoing, completed, or future. These are ESSENTIAL for fluency!',
        
        'progressive': {
            'name': 'Progressive: กำลัง (gam-laŋ) - "am/is/are -ing"',
            'pattern': 'Subject + กำลัง + Verb',
            'usage': 'Shows action happening RIGHT NOW',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมกำลังกินข้าว',
                        'paiboon': 'pǒm gam-laŋ gin kâao',
                        'english': 'I am eating rice',
                        'breakdown': 'ผม (I) + กำลัง (progressive) + กิน (eat) + ข้าว (rice)'
                    },
                    {
                        'thai': 'ผมกำลังทำงาน',
                        'paiboon': 'pǒm gam-laŋ tam ŋaan',
                        'english': 'I am working',
                        'breakdown': 'ผม (I) + กำลัง (progressive) + ทำงาน (work)'
                    },
                    {
                        'thai': 'เขากำลังอ่านหนังสือ',
                        'paiboon': 'kǎo gam-laŋ àan nǎŋ-sʉ̌ʉ',
                        'english': 'He/She is reading a book',
                        'breakdown': 'เขา (he/she) + กำลัง (progressive) + อ่าน (read) + หนังสือ (book)'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันกำลังกินข้าว',
                        'paiboon': 'dì-chǎn gam-laŋ gin kâao',
                        'english': 'I am eating rice',
                        'breakdown': 'ดิฉัน (I) + กำลัง (progressive) + กิน (eat) + ข้าว (rice)'
                    },
                    {
                        'thai': 'ดิฉันกำลังทำงาน',
                        'paiboon': 'dì-chǎn gam-laŋ tam ŋaan',
                        'english': 'I am working',
                        'breakdown': 'ดิฉัน (I) + กำลัง (progressive) + ทำงาน (work)'
                    },
                    {
                        'thai': 'เขากำลังอ่านหนังสือ',
                        'paiboon': 'kǎo gam-laŋ àan nǎŋ-sʉ̌ʉ',
                        'english': 'He/She is reading a book',
                        'breakdown': 'เขา (he/she) + กำลัง (progressive) + อ่าน (read) + หนังสือ (book)'
                    }
                ]
            }
        },
        
        'completed': {
            'name': 'Completed: แล้ว (lɛ́ɛo) - "already"',
            'pattern': 'Subject + Verb + แล้ว',
            'usage': 'Shows action is FINISHED/COMPLETED',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมกินข้าวแล้ว',
                        'paiboon': 'pǒm gin kâao lɛ́ɛo',
                        'english': 'I already ate / I have eaten',
                        'breakdown': 'ผม (I) + กิน (eat) + ข้าว (rice) + แล้ว (already)'
                    },
                    {
                        'thai': 'ผมทำงานเสร็จแล้ว',
                        'paiboon': 'pǒm tam ŋaan sèt lɛ́ɛo',
                        'english': 'I finished working already',
                        'breakdown': 'ผม (I) + ทำงาน (work) + เสร็จ (finish) + แล้ว (already)'
                    },
                    {
                        'thai': 'เขาไปแล้ว',
                        'paiboon': 'kǎo bpai lɛ́ɛo',
                        'english': 'He/She already went / has gone',
                        'breakdown': 'เขา (he/she) + ไป (go) + แล้ว (already)'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันกินข้าวแล้ว',
                        'paiboon': 'dì-chǎn gin kâao lɛ́ɛo',
                        'english': 'I already ate / I have eaten',
                        'breakdown': 'ดิฉัน (I) + กิน (eat) + ข้าว (rice) + แล้ว (already)'
                    },
                    {
                        'thai': 'ดิฉันทำงานเสร็จแล้ว',
                        'paiboon': 'dì-chǎn tam ŋaan sèt lɛ́ɛo',
                        'english': 'I finished working already',
                        'breakdown': 'ดิฉัน (I) + ทำงาน (work) + เสร็จ (finish) + แล้ว (already)'
                    },
                    {
                        'thai': 'เขาไปแล้ว',
                        'paiboon': 'kǎo bpai lɛ́ɛo',
                        'english': 'He/She already went / has gone',
                        'breakdown': 'เขา (he/she) + ไป (go) + แล้ว (already)'
                    }
                ]
            }
        },
        
        'future': {
            'name': 'Future: จะ (jà) - "will"',
            'pattern': 'Subject + จะ + Verb',
            'usage': 'Shows action WILL HAPPEN in the future',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมจะกินข้าว',
                        'paiboon': 'pǒm jà gin kâao',
                        'english': 'I will eat rice',
                        'breakdown': 'ผม (I) + จะ (will) + กิน (eat) + ข้าว (rice)'
                    },
                    {
                        'thai': 'ผมจะไปเมืองไทย',
                        'paiboon': 'pǒm jà bpai mʉaŋ-tai',
                        'english': 'I will go to Thailand',
                        'breakdown': 'ผม (I) + จะ (will) + ไป (go) + เมืองไทย (Thailand)'
                    },
                    {
                        'thai': 'เขาจะมาพรุ่งนี้',
                        'paiboon': 'kǎo jà maa prûŋ-níi',
                        'english': 'He/She will come tomorrow',
                        'breakdown': 'เขา (he/she) + จะ (will) + มา (come) + พรุ่งนี้ (tomorrow)'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันจะกินข้าว',
                        'paiboon': 'dì-chǎn jà gin kâao',
                        'english': 'I will eat rice',
                        'breakdown': 'ดิฉัน (I) + จะ (will) + กิน (eat) + ข้าว (rice)'
                    },
                    {
                        'thai': 'ดิฉันจะไปเมืองไทย',
                        'paiboon': 'dì-chǎn jà bpai mʉaŋ-tai',
                        'english': 'I will go to Thailand',
                        'breakdown': 'ดิฉัน (I) + จะ (will) + ไป (go) + เมืองไทย (Thailand)'
                    },
                    {
                        'thai': 'เขาจะมาพรุ่งนี้',
                        'paiboon': 'kǎo jà maa prûŋ-níi',
                        'english': 'He/She will come tomorrow',
                        'breakdown': 'เขา (he/she) + จะ (will) + มา (come) + พรุ่งนี้ (tomorrow)'
                    }
                ]
            }
        },
        
        'combined': {
            'name': 'Combined Patterns - Multiple Markers',
            'pattern': 'Mix markers for precise meaning',
            'usage': 'Combine to show complex time relationships',
            'examples': {
                'male': [
                    {
                        'thai': 'ผมกำลังจะไป',
                        'paiboon': 'pǒm gam-laŋ jà bpai',
                        'english': 'I am about to go',
                        'breakdown': 'ผม (I) + กำลัง (progressive) + จะ (will) + ไป (go)',
                        'note': 'Progressive + Future = "about to"'
                    },
                    {
                        'thai': 'ผมกินข้าวแล้วจะไป',
                        'paiboon': 'pǒm gin kâao lɛ́ɛo jà bpai',
                        'english': 'After I eat, I will go',
                        'breakdown': 'ผม (I) + กิน (eat) + ข้าว (rice) + แล้ว (after) + จะ (will) + ไป (go)',
                        'note': 'Completed + Future = sequential actions'
                    }
                ],
                'female': [
                    {
                        'thai': 'ดิฉันกำลังจะไป',
                        'paiboon': 'dì-chǎn gam-laŋ jà bpai',
                        'english': 'I am about to go',
                        'breakdown': 'ดิฉัน (I) + กำลัง (progressive) + จะ (will) + ไป (go)',
                        'note': 'Progressive + Future = "about to"'
                    },
                    {
                        'thai': 'ดิฉันกินข้าวแล้วจะไป',
                        'paiboon': 'dì-chǎn gin kâao lɛ́ɛo jà bpai',
                        'english': 'After I eat, I will go',
                        'breakdown': 'ดิฉัน (I) + กิน (eat) + ข้าว (rice) + แล้ว (after) + จะ (will) + ไป (go)',
                        'note': 'Completed + Future = sequential actions'
                    }
                ]
            }
        }
    },
    
    'question_patterns': {
        'title': 'Question Formation',
        'explanation': 'Thai questions use particles ไหม (mǎi) for yes/no and question words for information.',
        
        'yes_no': {
            'name': 'Yes/No Questions: ไหม (mǎi)',
            'pattern': 'Statement + ไหม + particle',
            'examples': {
                'male': [
                    {
                        'thai': 'คุณกินข้าวไหมครับ',
                        'paiboon': 'kun gin kâao mǎi kráp',
                        'english': 'Do you eat rice? / Have you eaten?',
                        'breakdown': 'คุณ (you) + กิน (eat) + ข้าว (rice) + ไหม (question) + ครับ (polite)'
                    },
                    {
                        'thai': 'คุณพูดไทยได้ไหมครับ',
                        'paiboon': 'kun pûut tai dâi mǎi kráp',
                        'english': 'Can you speak Thai?',
                        'breakdown': 'คุณ (you) + พูด (speak) + ไทย (Thai) + ได้ (can) + ไหม (question) + ครับ (polite)'
                    }
                ],
                'female': [
                    {
                        'thai': 'คุณกินข้าวไหมคะ',
                        'paiboon': 'kun gin kâao mǎi ká',
                        'english': 'Do you eat rice? / Have you eaten?',
                        'breakdown': 'คุณ (you) + กิน (eat) + ข้าว (rice) + ไหม (question) + คะ (polite)'
                    },
                    {
                        'thai': 'คุณพูดไทยได้ไหมคะ',
                        'paiboon': 'kun pûut tai dâi mǎi ká',
                        'english': 'Can you speak Thai?',
                        'breakdown': 'คุณ (you) + พูด (speak) + ไทย (Thai) + ได้ (can) + ไหม (question) + คะ (polite)'
                    }
                ]
            }
        },
        
        'wh_questions': {
            'name': 'Information Questions: Question Words',
            'pattern': 'Question word replaces the answer',
            'examples': {
                'male': [
                    {
                        'thai': 'คุณชื่ออะไรครับ',
                        'paiboon': 'kun chûu à-rai kráp',
                        'english': "What's your name?",
                        'breakdown': 'คุณ (you) + ชื่อ (name) + อะไร (what) + ครับ (polite)',
                        'note': 'อะไร (à-rai) = what'
                    },
                    {
                        'thai': 'คุณไปไหนครับ',
                        'paiboon': 'kun bpai nǎi kráp',
                        'english': 'Where are you going?',
                        'breakdown': 'คุณ (you) + ไป (go) + ไหน (where) + ครับ (polite)',
                        'note': 'ไหน (nǎi) = where'
                    },
                    {
                        'thai': 'ทำไมครับ',
                        'paiboon': 'tam-mai kráp',
                        'english': 'Why?',
                        'breakdown': 'ทำไม (why) + ครับ (polite)',
                        'note': 'ทำไม (tam-mai) = why'
                    }
                ],
                'female': [
                    {
                        'thai': 'คุณชื่ออะไรคะ',
                        'paiboon': 'kun chûu à-rai ká',
                        'english': "What's your name?",
                        'breakdown': 'คุณ (you) + ชื่อ (name) + อะไร (what) + คะ (polite)',
                        'note': 'อะไร (à-rai) = what'
                    },
                    {
                        'thai': 'คุณไปไหนคะ',
                        'paiboon': 'kun bpai nǎi ká',
                        'english': 'Where are you going?',
                        'breakdown': 'คุณ (you) + ไป (go) + ไหน (where) + คะ (polite)',
                        'note': 'ไหน (nǎi) = where'
                    },
                    {
                        'thai': 'ทำไมคะ',
                        'paiboon': 'tam-mai ká',
                        'english': 'Why?',
                        'breakdown': 'ทำไม (why) + คะ (polite)',
                        'note': 'ทำไม (tam-mai) = why'
                    }
                ]
            }
        }
    },
    
    'common_verbs': {
        'title': 'Essential Verbs in Context',
        'explanation': 'Practice common verbs with aspect markers',
        'verbs': [
            {
                'verb': 'ไป (bpai) - go',
                'present': {'thai': 'ไป', 'paiboon': 'bpai'},
                'progressive': {'thai': 'กำลังไป', 'paiboon': 'gam-laŋ bpai', 'english': 'am/is/are going'},
                'completed': {'thai': 'ไปแล้ว', 'paiboon': 'bpai lɛ́ɛo', 'english': 'already went / have gone'},
                'future': {'thai': 'จะไป', 'paiboon': 'jà bpai', 'english': 'will go'}
            },
            {
                'verb': 'มา (maa) - come',
                'present': {'thai': 'มา', 'paiboon': 'maa'},
                'progressive': {'thai': 'กำลังมา', 'paiboon': 'gam-laŋ maa', 'english': 'am/is/are coming'},
                'completed': {'thai': 'มาแล้ว', 'paiboon': 'maa lɛ́ɛo', 'english': 'already came / have come'},
                'future': {'thai': 'จะมา', 'paiboon': 'jà maa', 'english': 'will come'}
            },
            {
                'verb': 'กิน (gin) - eat',
                'present': {'thai': 'กิน', 'paiboon': 'gin'},
                'progressive': {'thai': 'กำลังกิน', 'paiboon': 'gam-laŋ gin', 'english': 'am/is/are eating'},
                'completed': {'thai': 'กินแล้ว', 'paiboon': 'gin lɛ́ɛo', 'english': 'already ate / have eaten'},
                'future': {'thai': 'จะกิน', 'paiboon': 'jà gin', 'english': 'will eat'}
            },
            {
                'verb': 'ทำงาน (tam ŋaan) - work',
                'present': {'thai': 'ทำงาน', 'paiboon': 'tam ŋaan'},
                'progressive': {'thai': 'กำลังทำงาน', 'paiboon': 'gam-laŋ tam ŋaan', 'english': 'am/is/are working'},
                'completed': {'thai': 'ทำงานแล้ว', 'paiboon': 'tam ŋaan lɛ́ɛo', 'english': 'already worked / have worked'},
                'future': {'thai': 'จะทำงาน', 'paiboon': 'jà tam ŋaan', 'english': 'will work'}
            },
            {
                'verb': 'เรียน (riian) - study',
                'present': {'thai': 'เรียน', 'paiboon': 'riian'},
                'progressive': {'thai': 'กำลังเรียน', 'paiboon': 'gam-laŋ riian', 'english': 'am/is/are studying'},
                'completed': {'thai': 'เรียนแล้ว', 'paiboon': 'riian lɛ́ɛo', 'english': 'already studied / have studied'},
                'future': {'thai': 'จะเรียน', 'paiboon': 'jà riian', 'english': 'will study'}
            }
        ]
    }
}

CONVERSATIONS = {
    'restaurant': {
        'title': 'At a Restaurant (ที่ร้านอาหาร)',
        'setting': 'Ordering food at a Thai restaurant',
        'difficulty': 'beginner',
        'dialogue': [
            {
                'speaker': 'waiter',
                'thai': 'สวัสดีครับ รับอะไรดีครับ',
                'paiboon': 'sà-wàt-dii kráp, ráp à-rai dii kráp',
                'english': 'Hello, what would you like to order?',
                'note': 'Waiter greeting'
            },
            {
                'speaker': 'customer_male',
                'thai': 'ผมขอข้าวผัดหนึ่งจานครับ',
                'paiboon': 'pǒm kɔ̌ɔ kâao pàt nʉ̀ŋ jaan kráp',
                'english': "I'd like one fried rice please",
                'note': 'Male customer ordering'
            },
            {
                'speaker': 'customer_female',
                'thai': 'ดิฉันขอส้มตำค่ะ',
                'paiboon': 'dì-chǎn kɔ̌ɔ sôm-tam kâ',
                'english': "I'd like papaya salad please",
                'note': 'Female customer ordering'
            },
            {
                'speaker': 'waiter',
                'thai': 'เผ็ดไหมครับ',
                'paiboon': 'pèt mǎi kráp',
                'english': 'Spicy?',
                'note': 'Asking about spice level'
            },
            {
                'speaker': 'customer_female',
                'thai': 'ไม่เผ็ดค่ะ',
                'paiboon': 'mâi pèt kâ',
                'english': 'Not spicy please',
                'note': 'Declining spice'
            },
            {
                'speaker': 'waiter',
                'thai': 'รับน้ำอะไรครับ',
                'paiboon': 'ráp náam à-rai kráp',
                'english': 'What would you like to drink?',
                'note': 'Asking about beverages'
            },
            {
                'speaker': 'customer_male',
                'thai': 'เอาน้ำเปล่าครับ',
                'paiboon': 'ao náam bplào kráp',
                'english': "I'll have water",
                'note': 'Ordering water'
            }
        ]
    },
    
    'meeting': {
        'title': 'Meeting Someone (การพบปะ)',
        'setting': 'First time meeting someone',
        'difficulty': 'beginner',
        'dialogue': [
            {
                'speaker': 'person1_male',
                'thai': 'สวัสดีครับ ผมชื่อจอห์น',
                'paiboon': 'sà-wàt-dii kráp, pǒm chûu John',
                'english': "Hello, I'm John",
                'note': 'Male introduction'
            },
            {
                'speaker': 'person2_female',
                'thai': 'สวัสดีค่ะ ดิฉันชื่อนิดา ยินดีที่ได้รู้จักค่ะ',
                'paiboon': 'sà-wàt-dii kâ, dì-chǎn chûu Nida, yin-dii tîi dâi rúu-jàk kâ',
                'english': "Hello, I'm Nida, nice to meet you",
                'note': 'Female introduction'
            },
            {
                'speaker': 'person1_male',
                'thai': 'ยินดีที่ได้รู้จักเช่นกันครับ คุณมาจากไหนครับ',
                'paiboon': 'yin-dii tîi dâi rúu-jàk chên-gan kráp, kun maa jàak nǎi kráp',
                'english': 'Nice to meet you too. Where are you from?',
                'note': 'Asking origin'
            },
            {
                'speaker': 'person2_female',
                'thai': 'ดิฉันมาจากกรุงเทพค่ะ แล้วคุณล่ะคะ',
                'paiboon': 'dì-chǎn maa jàak gruŋ-têep kâ, lɛ́ɛo kun lâ ká',
                'english': "I'm from Bangkok. And you?",
                'note': 'Responding and asking back'
            },
            {
                'speaker': 'person1_male',
                'thai': 'ผมมาจากอเมริกาครับ',
                'paiboon': 'pǒm maa jàak à-mee-rí-gaa kráp',
                'english': "I'm from America",
                'note': 'Country name'
            },
            {
                'speaker': 'person2_female',
                'thai': 'คุณพูดไทยเก่งมากเลยค่ะ',
                'paiboon': 'kun pûut tai gèŋ mâak ləəi kâ',
                'english': 'You speak Thai very well!',
                'note': 'Compliment'
            },
            {
                'speaker': 'person1_male',
                'thai': 'ขอบคุณครับ ผมกำลังเรียนอยู่ครับ',
                'paiboon': 'kɔ̀ɔp-kun kráp, pǒm gam-laŋ riian yùu kráp',
                'english': "Thank you, I'm still learning",
                'note': 'Using progressive + อยู่'
            }
        ]
    },
    
    'shopping': {
        'title': 'Shopping (การซื้อของ)',
        'setting': 'Buying something at a market',
        'difficulty': 'intermediate',
        'dialogue': [
            {
                'speaker': 'customer_female',
                'thai': 'ขอดูเสื้อตัวนี้หน่อยค่ะ',
                'paiboon': 'kɔ̌ɔ duu sʉ̂a dtuua níi nɔ̀ɔi kâ',
                'english': 'Can I see this shirt please?',
                'note': 'Polite request with หน่อย'
            },
            {
                'speaker': 'seller',
                'thai': 'ได้ครับ ขนาดอะไรครับ',
                'paiboon': 'dâi kráp, kà-nàat à-rai kráp',
                'english': 'Sure, what size?',
                'note': 'Asking about size'
            },
            {
                'speaker': 'customer_female',
                'thai': 'ขนาดเอ็มค่ะ ราคาเท่าไหร่คะ',
                'paiboon': 'kà-nàat M kâ, raa-kaa tâo-rài ká',
                'english': 'Size M. How much is it?',
                'note': 'Asking price'
            },
            {
                'speaker': 'seller',
                'thai': 'สามร้อยบาทครับ',
                'paiboon': 'sǎam rɔ́ɔi bàat kráp',
                'english': '300 baht',
                'note': 'Price'
            },
            {
                'speaker': 'customer_female',
                'thai': 'แพงไปหน่อยค่ะ ลดได้ไหมคะ',
                'paiboon': 'pɛɛŋ bpai nɔ̀ɔi kâ, lót dâi mǎi ká',
                'english': "It's a bit expensive. Can you reduce the price?",
                'note': 'Negotiating'
            },
            {
                'speaker': 'seller',
                'thai': 'ลดให้สองร้อยห้าสิบบาทครับ',
                'paiboon': 'lót hâi sɔ̌ɔŋ rɔ́ɔi hâa-sìp bàat kráp',
                'english': "I'll reduce it to 250 baht",
                'note': 'Counter offer'
            },
            {
                'speaker': 'customer_female',
                'thai': 'โอเคค่ะ เอาค่ะ',
                'paiboon': 'oo-kee kâ, ao kâ',
                'english': "OK, I'll take it",
                'note': 'Accepting'
            }
        ]
    },
    
    'directions': {
        'title': 'Asking for Directions (ถามทาง)',
        'setting': 'Getting directions to a place',
        'difficulty': 'intermediate',
        'dialogue': [
            {
                'speaker': 'tourist_male',
                'thai': 'ขอโทษครับ วัดพระแก้วอยู่ที่ไหนครับ',
                'paiboon': 'kɔ̌ɔ-tôot kráp, wát prá-gɛ̂ɛo yùu tîi nǎi kráp',
                'english': 'Excuse me, where is Wat Phra Kaew?',
                'note': 'Polite question'
            },
            {
                'speaker': 'local',
                'thai': 'ตรงไปแล้วเลี้ยวซ้ายครับ',
                'paiboon': 'dtroŋ bpai lɛ́ɛo líao sáai kráp',
                'english': 'Go straight then turn left',
                'note': 'Giving directions'
            },
            {
                'speaker': 'tourist_male',
                'thai': 'ไกลไหมครับ',
                'paiboon': 'glai mǎi kráp',
                'english': 'Is it far?',
                'note': 'Asking about distance'
            },
            {
                'speaker': 'local',
                'thai': 'ไม่ไกลครับ เดินประมาณสิบนาทีครับ',
                'paiboon': 'mâi glai kráp, dəən bprà-maan sìp naa-tii kráp',
                'english': "Not far, about 10 minutes walk",
                'note': 'Time estimate'
            },
            {
                'speaker': 'tourist_male',
                'thai': 'ขอบคุณมากครับ',
                'paiboon': 'kɔ̀ɔp-kun mâak kráp',
                'english': 'Thank you very much',
                'note': 'Thanking'
            },
            {
                'speaker': 'local',
                'thai': 'ไม่เป็นไรครับ',
                'paiboon': 'mâi bpen rai kráp',
                'english': "You're welcome / No problem",
                'note': 'Standard response'
            }
        ]
    },
    
    'daily_routine': {
        'title': 'Daily Routine (กิจวัตรประจำวัน)',
        'setting': 'Talking about your day',
        'difficulty': 'intermediate',
        'dialogue': [
            {
                'speaker': 'friend1_male',
                'thai': 'เช้านี้คุณทำอะไรครับ',
                'paiboon': 'cháao níi kun tam à-rai kráp',
                'english': 'What did you do this morning?',
                'note': 'Past question'
            },
            {
                'speaker': 'friend2_female',
                'thai': 'ดิฉันไปออกกำลังกายค่ะ แล้วคุณล่ะคะ',
                'paiboon': 'dì-chǎn bpai ɔ̀ɔk gam-laŋ gaai kâ, lɛ́ɛo kun lâ ká',
                'english': 'I went to exercise. And you?',
                'note': 'Past completed + asking back'
            },
            {
                'speaker': 'friend1_male',
                'thai': 'ผมยังไม่ได้ไปครับ ผมกำลังจะไปตอนเย็นครับ',
                'paiboon': 'pǒm yaŋ mâi dâi bpai kráp, pǒm gam-laŋ jà bpai dtɔɔn yen kráp',
                'english': "I haven't gone yet. I'm going to go in the evening",
                'note': 'Negative + progressive future'
            },
            {
                'speaker': 'friend2_female',
                'thai': 'ตอนนี้คุณกำลังทำอะไรอยู่คะ',
                'paiboon': 'dtɔɔn níi kun gam-laŋ tam à-rai yùu ká',
                'english': 'What are you doing now?',
                'note': 'Progressive with อยู่'
            },
            {
                'speaker': 'friend1_male',
                'thai': 'ผมกำลังทำงานอยู่ครับ แล้วเดี๋ยวจะไปกินข้าวครับ',
                'paiboon': 'pǒm gam-laŋ tam ŋaan yùu kráp, lɛ́ɛo dǐao jà bpai gin kâao kráp',
                'english': "I'm working now, then I'll go eat soon",
                'note': 'Progressive + future'
            },
            {
                'speaker': 'friend2_female',
                'thai': 'ไปกินด้วยกันไหมคะ',
                'paiboon': 'bpai gin dûuai gan mǎi ká',
                'english': 'Want to eat together?',
                'note': 'Invitation'
            },
            {
                'speaker': 'friend1_male',
                'thai': 'ได้ครับ ไปกันเลยครับ',
                'paiboon': 'dâi kráp, bpai gan ləəi kráp',
                'english': "Sure, let's go!",
                'note': 'Accepting + suggesting action'
            }
        ]
    }
}


@app.route('/grammar')
@require_access('grammar')
def grammar():
    gender = session.get('user_gender', 'neutral')
    gendered_examples = build_sentence(gender, 'polite', True)
    return render_template('grammar.html', 
                         grammar=GRAMMAR, 
                         gender=gender,
                         gendered_examples=gendered_examples)



@app.route('/lessons')
@require_access('lessons')
def lessons():
    return render_template('lessons.html', lessons=LESSONS)


@app.route('/lesson/<int:lesson_id>')
def lesson_detail(lesson_id):
    lesson = next((l for l in LESSONS if l['id'] == lesson_id), None)
    if not lesson:
        return "Lesson not found. <a href='/lessons'>Back</a>", 404
    return render_template('lesson_detail.html', lesson=lesson)


@app.route('/tour-guide')
@require_access('tour_guide')
def tour_guide():
    """Thai for tourists and holiday makers"""
    return render_template('tour_guide.html', vocab=TOUR_VOCAB)


@app.route('/business-thai')
@require_access('business_thai')
def business_thai():
    """Business Thai for professionals and expats"""
    return render_template('business_thai.html', vocab=BUSINESS_VOCAB)


@app.route('/paiboon')
@require_access('paiboon')
def paiboon_guide():
    return render_template('paiboon.html', guide=PAIBOON_GUIDE)



@app.route('/vowels_syllables')
@require_access('vowels_syllables')
def vowels_syllables():
    """Display comprehensive 32-vowel system with syllable structure"""
    return render_template('vowels_syllables.html', vowels=THAI_VOWELS_32)


@app.route('/tones-classes')
@require_access('tones_classes')
def tones_classes():
    """Unified free section: consonant classes + tone rules taught together."""
    return render_template('tones_classes.html', data=TONES_AND_CLASSES)

@app.route('/register')
@require_access('register')
def register_guide():
    return render_template('register.html', registers=REGISTER_LEVELS)


@app.route('/theravada')
@require_access('theravada')
def theravada():
    return render_template('theravada.html', teachings=THERAVADA_TEACHINGS)

@app.route('/bob-buddhism-overview')
def bob_buddhism_overview():
    """Pra Kru Bob's Buddhism: An Overview for Children article"""
    return render_template('bob_buddhism_overview.html')


@app.route('/bob-fear-article')
def bob_fear_article():
    """Pra Kru Bob's Fear as Guardian and Tyrant article"""
    return render_template('bob_fear_article.html')


@app.route('/sentences')
@require_access('sentences')
def sentences():
    """Sentence patterns and conversations for fluency practice"""
    gender = session.get('user_gender', 'neutral')
    
    # Select appropriate gender examples
    if gender == 'male':
        aspect_examples = {
            'progressive': SENTENCE_PATTERNS['aspect_markers']['progressive']['examples']['male'],
            'completed': SENTENCE_PATTERNS['aspect_markers']['completed']['examples']['male'],
            'future': SENTENCE_PATTERNS['aspect_markers']['future']['examples']['male'],
            'combined': SENTENCE_PATTERNS['aspect_markers']['combined']['examples']['male']
        }
        question_examples = {
            'yes_no': SENTENCE_PATTERNS['question_patterns']['yes_no']['examples']['male'],
            'wh_questions': SENTENCE_PATTERNS['question_patterns']['wh_questions']['examples']['male']
        }
    elif gender == 'female':
        aspect_examples = {
            'progressive': SENTENCE_PATTERNS['aspect_markers']['progressive']['examples']['female'],
            'completed': SENTENCE_PATTERNS['aspect_markers']['completed']['examples']['female'],
            'future': SENTENCE_PATTERNS['aspect_markers']['future']['examples']['female'],
            'combined': SENTENCE_PATTERNS['aspect_markers']['combined']['examples']['female']
        }
        question_examples = {
            'yes_no': SENTENCE_PATTERNS['question_patterns']['yes_no']['examples']['female'],
            'wh_questions': SENTENCE_PATTERNS['question_patterns']['wh_questions']['examples']['female']
        }
    else:  # neutral - show both
        aspect_examples = {
            'progressive': SENTENCE_PATTERNS['aspect_markers']['progressive']['examples'],
            'completed': SENTENCE_PATTERNS['aspect_markers']['completed']['examples'],
            'future': SENTENCE_PATTERNS['aspect_markers']['future']['examples'],
            'combined': SENTENCE_PATTERNS['aspect_markers']['combined']['examples']
        }
        question_examples = {
            'yes_no': SENTENCE_PATTERNS['question_patterns']['yes_no']['examples'],
            'wh_questions': SENTENCE_PATTERNS['question_patterns']['wh_questions']['examples']
        }
    
    return render_template('sentences.html',
                         gender=gender,
                         patterns=SENTENCE_PATTERNS,
                         aspect_examples=aspect_examples,
                         question_examples=question_examples,
                         conversations=CONVERSATIONS)


@app.route('/meditation')
@require_access('meditation')
def meditation():
    return render_template('meditation.html', techniques=MEDITATION_TECHNIQUES)


def _load_yaitron():
    """Load Yaitron Paiboon TSV once at startup. Falls back to the base TSV if
    the Paiboon-enriched file does not exist yet (i.e. generate_paiboon.py
    has not been run)."""
    paiboon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'yaitron_dictionary_paiboon_fixed.tsv')
    base_path    = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'yaitron_dictionary.tsv')
    path         = paiboon_path if os.path.exists(paiboon_path) else base_path
    has_paiboon  = path == paiboon_path

    entries = []
    seen = set()
    with open(path, encoding='utf-8') as f:
        # Skip header row if present
        first = f.readline().rstrip('\n')
        if not first.startswith('english\t'):
            f.seek(0)   # no header — rewind

        for line in f:
            parts = line.rstrip('\n').split('\t')
            if has_paiboon and len(parts) >= 3:
                en, th, pb = parts[0].strip(), parts[1].strip(), parts[2].strip()
            elif not has_paiboon and len(parts) == 2:
                en, th, pb = parts[0].strip(), parts[1].strip(), ''
            else:
                continue
            if not en or not th:
                continue
            key = (en.lower(), th)
            if key not in seen:
                seen.add(key)
                entries.append({'english': en, 'thai': th, 'paiboon': pb})
    return entries

YAITRON_ENTRIES = _load_yaitron()


@app.route('/dictionary')
@require_access('dictionary')
def dictionary():
    query = request.args.get('q', '').strip()
    results = []
    if query:
        q = query.lower()
        results = [e for e in YAITRON_ENTRIES if q in e['english'].lower()][:50]
    return render_template(
        'dictionary.html',
        reference=DICTIONARY_REFERENCE,
        query=query,
        results=results,
        total_entries=len(YAITRON_ENTRIES),
    )


@app.route('/premium')
def premium():
    init_user_progress()
    return render_template('premium.html',
                           tiers=SUBSCRIPTION_TIERS,
                           current_tier=active_tier(),
                           addon=INSTANT_ACCESS_ADDON,
                           has_addon=has_full_unlock())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Real sign-in. GET shows the form; POST verifies the password.

    A returning user can log in with EITHER their username or their email, plus
    their password. On success we hand the user to Flask-Login (which remembers
    them across requests) and re-link the gamification progress in the session.
    """
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('login.html')

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request format.'}), 400

    identifier = data.get('identifier', '').strip()
    password   = data.get('password', '')

    if not identifier or not password:
        return jsonify({'success': False, 'message': 'Please enter your username or email and your password.'}), 400

    # Look the user up by username OR email (email is stored lower-case).
    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier.lower())
    ).first()

    # Same generic message whether the user or the password was wrong — we don't
    # want to reveal which usernames/emails exist.
    if user is None or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Incorrect username/email or password.'}), 401

    login_user(user, remember=True)
    init_user_progress()
    session['user_progress']['user_id']  = user.id
    session['user_progress']['username'] = user.username
    session.modified = True

    return jsonify({
        'success': True,
        'message': f'Welcome back, {user.username}!',
        'redirect': '/'
    })


@app.route('/logout')
def logout():
    """Log the current user out and reset their session progress."""
    logout_user()
    session.pop('user_progress', None)   # clear cached progress so it doesn't bleed across logins
    return redirect('/')


# ============================================
# API ROUTES
# ============================================

@app.route('/api/quiz/<category>')
def get_quiz(category):
    beginner_mode = request.args.get('beginner', 'false').lower() == 'true'
    
    if category not in VOCABULARY:
        return jsonify({'error': f'Invalid category: {category}'}), 400
    
    vocab_list = get_vocab_with_mode(VOCABULARY[category], beginner_mode)
    word = random.choice(vocab_list)
    
    wrong = [v['paiboon'] for v in vocab_list if v['paiboon'] != word['paiboon']]
    wrong = random.sample(wrong, min(3, len(wrong)))
    options = wrong + [word['paiboon']]
    random.shuffle(options)
    
    return jsonify({
        'thai': word['thai'],
        'english': word['english'],
        'correct_answer': word['paiboon'],
        'options': options,
        'beginner_mode': beginner_mode
    })


@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    
    is_correct = data.get('answer') == data.get('correct')
    
    # Gamification: Award points for correct answers
    init_user_progress()
    user = session['user_progress']
    xp_earned = 0
    new_level = user['level']
    
    if is_correct:
        result = add_xp(POINT_REWARDS['quiz_correct'], 'Correct answer')
        xp_earned = result.get('points_earned', 0)
        new_level = result.get('level')
        user['correct_answers'] = user.get('correct_answers', 0) + 1
        user['words_learned'] = user.get('words_learned', 0) + 1
    
    user['total_answers'] = user.get('total_answers', 0) + 1
    user['quizzes_completed'] = user.get('quizzes_completed', 0) + 1
    session.modified = True
    
    return jsonify({
        'correct': is_correct,
        'message': 'ถูกต้อง! (Correct!)' if is_correct else f"ไม่ถูกต้อง. Answer: {data.get('correct')}",
        'xp_earned': xp_earned,
        'new_level': new_level,
        'total_xp': user['xp']
    })


@app.route('/api/vocabulary/<category>')
def get_vocabulary(category):
    beginner_mode = request.args.get('beginner', 'false').lower() == 'true'
    if category not in VOCABULARY:
        return jsonify({'error': 'Invalid category'}), 400
    
    vocab = get_vocab_with_mode(VOCABULARY[category], beginner_mode)
    return jsonify({'category': category, 'vocabulary': vocab, 'count': len(vocab)})


@app.route('/api/categories')
def get_categories():
    return jsonify({'categories': [
        {'id': k, 'name': k.replace('_', ' ').title(), 'word_count': len(v)} 
        for k, v in VOCABULARY.items()
    ]})


@app.route('/api/beginner_convert', methods=['POST'])
def beginner_convert():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text'}), 400
    
    original = data['text']
    converted = apply_beginner_mode(original)
    return jsonify({'original': original, 'converted': converted, 'changed': original != converted})


@app.route('/api/grammar')
def get_grammar():
    return jsonify(GRAMMAR)


@app.route('/api/lessons')
def get_lessons():
    return jsonify({'lessons': LESSONS})


@app.route('/api/theravada')
def get_theravada():
    return jsonify(THERAVADA_TEACHINGS)


@app.route('/api/meditation')
def get_meditation():
    return jsonify(MEDITATION_TECHNIQUES)


# ============================================
# RUN APPLICATION
# ============================================


# ============================================
# GAMIFICATION ROUTES
# ============================================

@app.route('/progress')
def progress_dashboard():
    """User progress dashboard"""
    init_user_progress()
    user = session['user_progress']
    
    next_level_xp = get_xp_for_next_level(user['level'])
    current_level_xp = XP_LEVELS[user['level']]
    
    if next_level_xp:
        progress_to_next = ((user['xp'] - current_level_xp) / (next_level_xp - current_level_xp)) * 100
    else:
        progress_to_next = 100
    
    new_achievements = check_achievements(user)
    
    available_sections = []
    locked_sections = []
    
    for section_id, requirements in SECTION_REQUIREMENTS.items():
        has_access, message = check_section_access(section_id)

        tier = requirements['tier']
        level = requirements['level']
        if tier != 'free':
            tier_info = SUBSCRIPTION_TIERS[tier]
            requirement_message = f"Requires Level {level} + {tier_info['name']} subscription (£{tier_info['price']:.2f}/mo)"
        elif level > 1:
            requirement_message = f"Requires Level {level} to unlock"
        else:
            requirement_message = "Complete Thai Alphabet first"

        section_info = {
            'id': section_id,
            'name': section_id.replace('_', ' ').title(),
            'level_required': requirements['level'],
            'tier_required': requirements['tier'],
            'points_reward': requirements['points_reward'],
            'unlocked': section_id in user['sections_unlocked'],
            'has_access': has_access,
            'message': requirement_message
        }
        
        if has_access or section_id in user['sections_unlocked']:
            available_sections.append(section_info)
        else:
            locked_sections.append(section_info)
    
    return render_template('progress.html',
                         user=user,
                         next_level_xp=next_level_xp,
                         progress_to_next=progress_to_next,
                         available_sections=available_sections,
                         locked_sections=locked_sections,
                         subscription_tiers=SUBSCRIPTION_TIERS,
                         achievements=ACHIEVEMENTS,
                         new_achievements=new_achievements)

@app.route('/developer-login', methods=['GET', 'POST'])
def developer_login():
    """Developer mode login"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash == DEVELOPER_PASSWORD_HASH:
            init_user_progress()
            session['user_progress']['is_developer'] = True
            session.modified = True
            return jsonify({'success': True, 'message': 'Developer mode activated!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid password'})
    
    return render_template('developer_login.html')

@app.route('/developer-logout')
def developer_logout():
    """Exit developer mode"""
    init_user_progress()
    session['user_progress']['is_developer'] = False
    session.modified = True
    return redirect('/')

# ============================================
# USER REGISTRATION ROUTE
# ============================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request format.'}), 400

    username         = data.get('username', '').strip()
    email            = data.get('email', '').strip().lower()
    password         = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not all([username, email, password, confirm_password]):
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return jsonify({'success': False, 'message': 'Username must be 3\u201320 characters: letters, numbers, and underscores only.'}), 400
    if not re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400
    if len(password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters.'}), 400
    if not re.search(r'[a-zA-Z]', password) or not re.search(r'[0-9]', password):
        return jsonify({'success': False, 'message': 'Password must contain at least one letter and one number.'}), 400
    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match.'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'That username is already taken.'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'An account with that email already exists.'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed. Please try again.'}), 500

    login_user(new_user, remember=True)   # creating an account also logs you in
    init_user_progress()
    session['user_progress']['user_id'] = new_user.id
    session['user_progress']['username'] = new_user.username
    session.modified = True

    return jsonify({
        'success': True,
        'message': f'Welcome, {new_user.username}! Your account has been created.',
        'redirect': '/'
    })

@app.route('/subscribe/<tier>')
@login_required
def subscribe(tier):
    """Start a subscription.

    The free tier is applied instantly (no payment needed). For paid tiers we
    show a small page that lets the user choose Stripe or PayPal — the actual
    checkout happens at /subscribe/<tier>/stripe or /subscribe/<tier>/paypal.
    """
    if tier not in SUBSCRIPTION_TIERS:
        return "Invalid tier", 400

    init_user_progress()

    # Free tier (or "downgrade") needs no payment — apply it straight away.
    if tier == 'free' or SUBSCRIPTION_TIERS[tier]['price'] == 0:
        _apply_subscription(current_user, tier='free', status='inactive',
                            current_period_end=None)
        _mirror_tier_to_session(current_user)
        return render_template('subscription_success.html',
                               tier='free',
                               tier_info=SUBSCRIPTION_TIERS['free'],
                               expires=None)

    # Paid tier — let the user pick how they want to pay.
    return render_template('subscribe_choose.html',
                           tier=tier,
                           tier_info=SUBSCRIPTION_TIERS[tier],
                           stripe_enabled=bool(stripe.api_key),
                           paypal_enabled=paypal_configured())


@app.route('/subscribe/<tier>/stripe')
@login_required
def subscribe_stripe(tier):
    """Send the user to Stripe Checkout (TEST mode) for a paid tier."""
    if tier not in SUBSCRIPTION_TIERS or tier == 'free':
        return redirect('/progress')

    # We need Stripe configured to take a (test) payment.
    if not stripe.api_key:
        return render_template('subscription_success.html',
                               stripe_unconfigured=True,
                               tier=tier,
                               tier_info=SUBSCRIPTION_TIERS[tier],
                               expires=None), 503

    tier_info = SUBSCRIPTION_TIERS[tier]
    base_url = request.url_root.rstrip('/')

    # Identity tags so the webhook (Phase 3) knows WHOSE payment this is.
    # We attach the user id in three places: on the Checkout Session (metadata +
    # client_reference_id) and on the Subscription itself (subscription_data),
    # so later renewal/cancellation events also carry it.
    user_meta = {'tier': tier, 'user_id': str(current_user.id)}

    checkout_kwargs = dict(
        mode='subscription',
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'unit_amount': int(round(tier_info['price'] * 100)),  # pence
                'recurring': {'interval': 'month'},
                'product_data': {
                    'name': f"ThaiBridge AI — {tier_info['name']}",
                },
            },
            'quantity': 1,
        }],
        # Stripe swaps {CHECKOUT_SESSION_ID} for the real id on redirect.
        success_url=f"{base_url}/subscribe/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}/subscribe/cancel",
        client_reference_id=str(current_user.id),
        metadata=user_meta,
        subscription_data={'metadata': user_meta},
    )

    # Reuse this user's Stripe customer if we already know it (keeps all their
    # invoices under one customer); otherwise pre-fill their email and let Stripe
    # create the customer — we'll capture and store its id in the webhook.
    if current_user.stripe_customer_id:
        checkout_kwargs['customer'] = current_user.stripe_customer_id
    else:
        checkout_kwargs['customer_email'] = current_user.email

    try:
        # We build the price inline ("price_data") rather than pre-creating
        # Products/Prices in the Stripe dashboard — fewer setup steps for a demo.
        checkout_session = stripe.checkout.Session.create(**checkout_kwargs)
    except Exception as e:
        app.logger.exception("Stripe checkout session creation failed")
        return f"Sorry, we couldn't start checkout: {e}", 502

    # 303 = "go look over there with a GET" — the correct redirect for this.
    return redirect(checkout_session.url, code=303)


@app.route('/addon/instant-access/stripe')
@login_required
def addon_instant_access_stripe():
    """One-time Stripe Checkout (TEST mode) for the Instant Access Pass.

    Sold on top of Thai Master (Pro): a single payment that sets full_unlock,
    skipping the level + alphabet gates so every section opens instantly. It
    requires an active Pro subscription (the add-on removes the grind, not the
    paywall) and is a no-op if they already own it."""
    if current_user.effective_tier != 'pro':
        return redirect('/premium')
    if current_user.full_unlock:
        return redirect('/progress')
    if not stripe.api_key:
        return render_template('subscription_success.html',
                               stripe_unconfigured=True, tier='pro',
                               tier_info=SUBSCRIPTION_TIERS['pro'], expires=None), 503

    base_url = request.url_root.rstrip('/')
    user_meta = {'addon': 'full_unlock', 'user_id': str(current_user.id)}
    checkout_kwargs = dict(
        mode='payment',   # one-time charge, not a subscription
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'unit_amount': int(round(INSTANT_ACCESS_ADDON['price'] * 100)),  # pence
                'product_data': {'name': f"ThaiBridge AI — {INSTANT_ACCESS_ADDON['name']}"},
            },
            'quantity': 1,
        }],
        success_url=f"{base_url}/addon/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}/subscribe/cancel",
        client_reference_id=str(current_user.id),
        metadata=user_meta,
    )
    if current_user.stripe_customer_id:
        checkout_kwargs['customer'] = current_user.stripe_customer_id
    else:
        checkout_kwargs['customer_email'] = current_user.email

    try:
        checkout_session = stripe.checkout.Session.create(**checkout_kwargs)
    except Exception as e:
        app.logger.exception("Stripe add-on checkout session creation failed")
        return f"Sorry, we couldn't start checkout: {e}", 502
    return redirect(checkout_session.url, code=303)


@app.route('/subscribe/<tier>/paypal')
@login_required
def subscribe_paypal(tier):
    """Create a PayPal order (sandbox) and send the user to PayPal to approve it."""
    if tier not in SUBSCRIPTION_TIERS or tier == 'free':
        return redirect('/progress')

    if not paypal_configured():
        return render_template('subscription_success.html',
                               paypal_unconfigured=True,
                               tier=tier,
                               tier_info=SUBSCRIPTION_TIERS[tier],
                               expires=None), 503

    tier_info = SUBSCRIPTION_TIERS[tier]
    base_url = request.url_root.rstrip('/')

    try:
        token = _paypal_access_token()
        resp = httpx.post(
            f"{PAYPAL_API_BASE}/v2/checkout/orders",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json={
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "GBP",
                        "value": f"{tier_info['price']:.2f}",
                    },
                    "description": f"ThaiBridge AI — {tier_info['name']} (monthly)",
                    # Tie the order to the logged-in user (and tier) so the
                    # return handler can update the right account.
                    "custom_id": f"{current_user.id}:{tier}",
                }],
                "application_context": {
                    "brand_name": "ThaiBridge AI",
                    "user_action": "PAY_NOW",
                    "shipping_preference": "NO_SHIPPING",
                    "return_url": f"{base_url}/paypal/success",
                    "cancel_url": f"{base_url}/subscribe/cancel",
                },
            },
            timeout=20,
        )
        resp.raise_for_status()
        order = resp.json()
    except Exception as e:
        app.logger.exception("PayPal order creation failed")
        return f"Sorry, we couldn't start PayPal checkout: {e}", 502

    # Remember which tier this order is for; we re-check the payment with PayPal
    # before trusting it on the way back.
    session['pending_paypal_tier'] = tier
    session.modified = True

    approve_url = next(
        (link["href"] for link in order.get("links", [])
         if link.get("rel") == "approve"),
        None,
    )
    if not approve_url:
        return "PayPal did not return an approval link", 502

    return redirect(approve_url, code=303)


# ============================================
# SUBSCRIPTION SYNC HELPERS  (the database is the source of truth)
# ============================================
# These translate what Stripe/PayPal tell us into updates on the User row.
# The Stripe webhook is the authoritative caller (it can't be spoofed); the
# success-redirect handlers call the same helpers as an idempotent fallback, so
# things still work in local dev where a webhook may not be wired up.

def _ts_to_dt(unix_ts):
    """Stripe sends times as unix timestamps; store them as naive UTC datetimes."""
    if not unix_ts:
        return None
    return datetime.utcfromtimestamp(int(unix_ts))


def _subscription_period_end(sub):
    """Read a subscription's current-period-end as a datetime.

    Newer Stripe API versions moved `current_period_end` OFF the Subscription
    object and onto each subscription item, so we look on the first item first
    and fall back to the old top-level field for older API versions.
    """
    items = (sub.get('items') or {}).get('data') or []
    ts = items[0].get('current_period_end') if items else None
    if not ts:
        ts = sub.get('current_period_end')
    return _ts_to_dt(ts)


def _find_user_for_stripe(user_id=None, subscription_id=None, customer_id=None):
    """Find the User a Stripe event refers to, trying the most reliable id first."""
    if user_id:
        u = db.session.get(User, int(user_id))
        if u:
            return u
    if subscription_id:
        u = User.query.filter_by(stripe_subscription_id=subscription_id).first()
        if u:
            return u
    if customer_id:
        u = User.query.filter_by(stripe_customer_id=customer_id).first()
        if u:
            return u
    return None


def _mirror_tier_to_session(user):
    """Keep the session's gamification copy in step with the DB.

    (Phase 4 will make the whole app read the tier straight from the DB; until
    then we mirror it so points multipliers and unlocks reflect the purchase.)
    """
    if 'user_progress' in session:
        session['user_progress']['subscription_tier'] = user.effective_tier
        session['user_progress']['subscription_expires'] = (
            user.current_period_end.isoformat() if user.current_period_end else None
        )
        session['user_progress']['full_unlock'] = bool(user.full_unlock)
        session.modified = True


def _apply_subscription(user, *, tier, status, customer_id=None,
                        subscription_id=None, current_period_end=None):
    """Write a subscription state onto a user and commit. Safe to call repeatedly."""
    user.subscription_tier = tier
    user.subscription_status = status
    if customer_id:
        user.stripe_customer_id = customer_id
    if subscription_id:
        user.stripe_subscription_id = subscription_id
    if current_period_end is not None:
        user.current_period_end = current_period_end
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Failed to save subscription for user %s", user.id)
        return False
    return True


def _sync_checkout_session(cs):
    """A Stripe Checkout finished -> activate the user's tier. Returns the User."""
    meta = cs.get('metadata') or {}
    user_id = meta.get('user_id') or cs.get('client_reference_id')
    tier = meta.get('tier')
    if not user_id or tier not in SUBSCRIPTION_TIERS:
        app.logger.warning("Checkout session %s missing user_id/tier", cs.get('id'))
        return None

    user = _find_user_for_stripe(user_id=user_id,
                                 customer_id=cs.get('customer'),
                                 subscription_id=cs.get('subscription'))
    if not user:
        app.logger.warning("No user matched checkout session %s", cs.get('id'))
        return None

    # The Checkout Session doesn't include the period end — read it off the
    # Subscription it created (this is also where renewals get their dates).
    status, period_end = 'active', None
    sub_id = cs.get('subscription')
    if sub_id and stripe.api_key:
        try:
            sub = stripe.Subscription.retrieve(sub_id)
            status = sub.get('status', 'active')
            period_end = _subscription_period_end(sub)
        except Exception:
            app.logger.exception("Could not retrieve subscription %s", sub_id)

    _apply_subscription(user, tier=tier, status=status,
                        customer_id=cs.get('customer'),
                        subscription_id=sub_id, current_period_end=period_end)
    app.logger.info("Activated tier '%s' for user %s", tier, user.id)
    return user


def _sync_addon_session(cs):
    """A one-time add-on Checkout finished -> grant the Instant Access Pass
    (full_unlock). Idempotent. Returns the User."""
    meta = cs.get('metadata') or {}
    user_id = meta.get('user_id') or cs.get('client_reference_id')
    if not user_id:
        app.logger.warning("Add-on session %s missing user_id", cs.get('id'))
        return None
    user = _find_user_for_stripe(user_id=user_id, customer_id=cs.get('customer'))
    if not user:
        app.logger.warning("No user matched add-on session %s", cs.get('id'))
        return None
    if not user.full_unlock:
        user.full_unlock = True
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            app.logger.exception("Failed to grant full_unlock for user %s", user.id)
            return None
    app.logger.info("Granted Instant Access Pass (full_unlock) to user %s", user.id)
    return user


def _sync_subscription_object(sub):
    """A customer.subscription.* event -> update status/tier/period (handles
    cancellations: a deleted/canceled subscription drops the user back to free
    via User.effective_tier)."""
    meta = sub.get('metadata') or {}
    user = _find_user_for_stripe(user_id=meta.get('user_id'),
                                 subscription_id=sub.get('id'),
                                 customer_id=sub.get('customer'))
    if not user:
        app.logger.warning("No user matched subscription %s", sub.get('id'))
        return None

    _apply_subscription(user,
                        tier=meta.get('tier', user.subscription_tier),
                        status=sub.get('status', 'canceled'),
                        customer_id=sub.get('customer'),
                        subscription_id=sub.get('id'),
                        current_period_end=_subscription_period_end(sub))
    app.logger.info("Subscription %s for user %s -> %s",
                    sub.get('id'), user.id, sub.get('status'))
    return user


def _sync_invoice_paid(invoice):
    """invoice.paid -> a successful monthly renewal. Extend the paid period."""
    sub_id = invoice.get('subscription')
    user = _find_user_for_stripe(subscription_id=sub_id,
                                 customer_id=invoice.get('customer'))
    if not user:
        return None

    status, period_end = 'active', None
    if sub_id and stripe.api_key:
        try:
            sub = stripe.Subscription.retrieve(sub_id)
            status = sub.get('status', 'active')
            period_end = _subscription_period_end(sub)
        except Exception:
            app.logger.exception("Could not retrieve subscription %s", sub_id)

    _apply_subscription(user, tier=user.subscription_tier, status=status,
                        current_period_end=period_end)
    app.logger.info("Renewal recorded for user %s (sub %s)", user.id, sub_id)
    return user


@app.route('/paypal/success')
@login_required
def paypal_success():
    """PayPal redirects here after the user approves the payment.

    Like the Stripe flow, we never trust the browser: we ask PayPal to capture
    the order and only unlock the tier if PayPal says the status is COMPLETED.
    """
    order_id = request.args.get('token')  # PayPal names the order id "token"
    tier = session.get('pending_paypal_tier')
    if not order_id or tier not in SUBSCRIPTION_TIERS:
        return redirect('/progress')

    try:
        token = _paypal_access_token()
        resp = httpx.post(
            f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            timeout=20,
        )
        resp.raise_for_status()
        result = resp.json()
    except Exception:
        app.logger.exception("PayPal capture failed")
        return redirect('/subscribe/cancel')

    if result.get('status') != 'COMPLETED':
        return redirect('/subscribe/cancel')

    # PayPal here is a one-off 30-day access grant (this demo doesn't use PayPal's
    # recurring billing, so there's no webhook to renew it). We record it on the
    # user's account — the database, not the cookie, is the source of truth.
    expires_dt = datetime.utcnow() + timedelta(days=30)
    _apply_subscription(current_user, tier=tier, status='active',
                        current_period_end=expires_dt)
    _mirror_tier_to_session(current_user)
    session.pop('pending_paypal_tier', None)
    session.modified = True

    return render_template('subscription_success.html',
                           tier=tier,
                           tier_info=SUBSCRIPTION_TIERS[tier],
                           expires=expires_dt.strftime('%d %B %Y'))


@app.route('/subscribe/success')
@login_required
def subscribe_success():
    """Stripe redirects here after a successful test payment.

    The webhook is the real source of truth, but it may not have arrived yet
    (or may not be configured in local dev), so we also sync here — the sync is
    idempotent, so running it twice is harmless. We never trust the browser: we
    re-fetch the Checkout Session from Stripe and only act if Stripe says paid.
    """
    session_id = request.args.get('session_id')
    if not session_id:
        return redirect('/progress')

    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        app.logger.exception("Could not retrieve Stripe checkout session")
        return redirect('/progress')

    # 'paid' for cards; 'no_payment_required' can happen for 100%-off sessions.
    if checkout_session.payment_status not in ('paid', 'no_payment_required'):
        return redirect('/subscribe/cancel')

    user = _sync_checkout_session(checkout_session) or current_user
    _mirror_tier_to_session(user)

    expires = (user.current_period_end.strftime('%d %B %Y')
               if user.current_period_end else None)
    return render_template('subscription_success.html',
                           tier=user.subscription_tier,
                           tier_info=SUBSCRIPTION_TIERS.get(
                               user.subscription_tier, SUBSCRIPTION_TIERS['free']),
                           expires=expires)


@app.route('/addon/success')
@login_required
def addon_success():
    """Stripe redirects here after the Instant Access Pass is paid. The webhook
    is the real source of truth; we also sync here idempotently so it works in
    local dev where a webhook may not be wired up. We re-fetch from Stripe and
    only grant if Stripe says paid."""
    session_id = request.args.get('session_id')
    if not session_id:
        return redirect('/progress')
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        app.logger.exception("Could not retrieve add-on checkout session")
        return redirect('/progress')
    if checkout_session.payment_status not in ('paid', 'no_payment_required'):
        return redirect('/subscribe/cancel')
    user = _sync_addon_session(checkout_session) or current_user
    _mirror_tier_to_session(user)
    return render_template('addon_success.html', addon=INSTANT_ACCESS_ADDON)


@app.route('/subscribe/cancel')
def subscribe_cancel():
    """User backed out of Stripe Checkout — no charge, send them back to plans."""
    return render_template('subscription_cancel.html')


@app.route('/subscribe/cancel-subscription', methods=['POST'])
@login_required
def cancel_subscription():
    """Let a logged-in user cancel their own paid Stripe subscription.

    We cancel it immediately in Stripe. Stripe then fires
    customer.subscription.deleted, which the webhook turns into a downgrade — but
    we also write that downgrade to the database here (safe to do twice) so the
    change shows up straight away, without waiting for the webhook to arrive.

    To instead let the user keep access until the period they've already paid for
    runs out, swap the cancel call for:
        stripe.Subscription.modify(sub_id, cancel_at_period_end=True)
    """
    sub_id = current_user.stripe_subscription_id
    if not sub_id or not stripe.api_key:
        # Nothing to cancel via Stripe (free tier, or a one-off PayPal grant).
        return redirect('/progress')

    try:
        stripe.Subscription.cancel(sub_id)
    except Exception:
        app.logger.exception("Failed to cancel subscription %s", sub_id)
        return redirect('/progress')

    # Mark them canceled now (the webhook will also do this — both are idempotent).
    _apply_subscription(current_user, tier=current_user.subscription_tier,
                        status='canceled')
    _mirror_tier_to_session(current_user)
    app.logger.info("User %s cancelled subscription %s", current_user.id, sub_id)
    # Send them to a warm goodbye page (PRG pattern: redirect after the POST).
    return redirect('/subscription-goodbye')


@app.route('/subscription-goodbye')
@login_required
def subscription_goodbye():
    """A friendly 'sorry to see you go' page shown right after cancellation."""
    return render_template('subscription_goodbye.html')


@app.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    """Receive events from Stripe (server-to-server) — the SOURCE OF TRUTH.

    We verify the signature so we know the event really came from Stripe, then
    write the result to the database. Unlike the success redirect (which the
    browser could fake), Stripe calls this directly, so it's the trustworthy
    place to mark a user paid, renew them, or cancel them.

    Events handled:
      • checkout.session.completed     — first payment: activate the tier
      • invoice.paid                   — monthly renewal: extend the paid period
      • customer.subscription.updated  — status/plan change
      • customer.subscription.deleted  — cancellation: drop back to free
    """
    if not STRIPE_WEBHOOK_SECRET:
        app.logger.warning("Stripe webhook hit but STRIPE_WEBHOOK_SECRET is not set")
        return '', 400

    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        app.logger.warning("Invalid Stripe webhook signature — ignoring")
        return '', 400

    etype = event['type']
    obj = event['data']['object']

    if etype == 'checkout.session.completed':
        if (obj.get('metadata') or {}).get('addon') == 'full_unlock':
            _sync_addon_session(obj)
        else:
            _sync_checkout_session(obj)
    elif etype == 'invoice.paid':
        _sync_invoice_paid(obj)
    elif etype in ('customer.subscription.updated',
                   'customer.subscription.deleted',
                   'customer.subscription.created'):
        _sync_subscription_object(obj)
    else:
        app.logger.debug("Unhandled Stripe event type: %s", etype)

    # Always 200 so Stripe doesn't keep retrying a handled event.
    return '', 200

@app.route('/api/award_points', methods=['POST'])
def award_points():
    """API endpoint to award points"""
    data = request.get_json()
    action = data.get('action', 'unknown')
    points = data.get('points', 0)
    
    result = add_xp(points, action)
    
    user = session['user_progress']
    new_achievements = check_achievements(user)
    
    result['new_achievements'] = [{'name': a['name'], 'description': a['description']} 
                                 for a in new_achievements]
    
    return jsonify(result)

@app.route('/api/user_stats')
def user_stats():
    """Get user statistics"""
    init_user_progress()
    user = session['user_progress']
    
    accuracy = 0
    if user['total_answers'] > 0:
        accuracy = (user['correct_answers'] / user['total_answers']) * 100
    
    return jsonify({
        'xp': user['xp'],
        'level': user['level'],
        'tier': active_tier(),
        'is_developer': user.get('is_developer', False),
        'quizzes_completed': user['quizzes_completed'],
        'accuracy': round(accuracy, 1),
        'achievements': len(user['achievements_earned']),
        'login_streak': user['login_streak']
    })


# ============================================
# RUN APPLICATION
# ============================================


@app.route('/formality')
@require_access('formality')
def formality_guide():
    """Display formality system guide"""
    return render_template('formality.html', levels=FORMALITY_LEVELS)


# ============================================
# THAI ALPHABET ROUTES
# ============================================

@app.route('/alphabet')
def thai_alphabet():
    """Thai Alphabet learning page"""
    init_user_progress()
    user = session['user_progress']
    alphabet_complete = check_alphabet_completion()
    
    return render_template('alphabet.html',
                         alphabet=THAI_ALPHABET,
                         alphabet_complete=alphabet_complete,
                         user_progress=user)

@app.route('/api/complete_alphabet', methods=['POST'])
def complete_alphabet():
    """Mark alphabet as completed"""
    result = mark_alphabet_complete()
    
    if result:
        return jsonify({
            'success': True,
            'message': 'Alphabet completed! +100 XP earned!',
            'xp_earned': 100
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Alphabet already completed'
        })


# ============================================
# AI CHAT ROUTES
# ============================================

@app.route('/chat')
def chat():
    """AI Chat interface"""
    if not ai_agent:
        return render_template('error.html',
                             message='AI Agent not available',
                             details='Please check setup instructions')
    return render_template('chat.html', ai_limits=ai_limits_status())

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """Send message to AI and get response"""
    if not ai_agent:
        return jsonify({
            'error': 'AI Agent not initialized. Please ensure ai_agent.py is in the project directory and ANTHROPIC_API_KEY is set.'
        }), 503
    
    try:
        data = request.json
        message = data.get('message', '')
        mode = data.get('mode', 'conversation')
        session_id = session.get('session_id', 'session_' + str(datetime.now().timestamp()))

        # --- Freemium gate: Pro is unlimited; free & basic get a taste ---
        tier = active_tier()
        if tier != 'pro':
            if mode not in FREE_AI_ALLOWED_MODES:
                return jsonify({
                    'success': False,
                    'gate': 'mode_locked',
                    'message': "This AI mode is a Pro feature. Free and Basic plans "
                               "include the Tutor mode — upgrade to Pro to unlock "
                               "Conversation, Culture, Dhamma and the Exercise Generator.",
                })
            usage = _ai_usage_today()
            if usage['count'] >= FREE_AI_DAILY_LIMIT:
                return jsonify({
                    'success': False,
                    'gate': 'daily_limit',
                    'message': f"You’ve used your {FREE_AI_DAILY_LIMIT} free AI messages "
                               "for today. Upgrade to Pro for unlimited AI, or come back tomorrow.",
                })

        # Get user context from session
        user_context = {
            'level': session.get('level', 1),
            'xp': session.get('xp', 0),
            'alphabet_completed': session.get('alphabet_completed', False),
            'name': session.get('username', 'Student')
        }

        # Get AI response (max_tokens controls API cost)
        response = ai_agent.chat(
            message=message,
            mode=mode,
            session_id=session_id,
            user_context=user_context,
            max_tokens=500
        )

        # Count this message against the daily taste for free & basic users,
        # and tell the UI how many they have left.
        if tier != 'pro' and isinstance(response, dict) and response.get('success'):
            usage = _ai_usage_today()
            usage['count'] += 1
            session['ai_usage'] = usage
            session.modified = True
            response['remaining'] = max(0, FREE_AI_DAILY_LIMIT - usage['count'])

        return jsonify(response)
        
    except Exception as e:
        print(f"AI Chat Error: {e}")
        return jsonify({
            'error': 'API error occurred. Please check your API key and try again.'
        }), 500

@app.route('/api/ai/hint', methods=['POST'])
def ai_hint():
    """Get a progressive hint for a quiz question"""
    if not ai_agent:
        return jsonify({'error': 'AI not available'}), 503
    
    try:
        data = request.json
        question = data.get('question', '')
        context = data.get('context', '')
        hint_level = data.get('hint_level', 1)
        
        response = ai_agent.get_quick_hint(
            question=question,
            context=context,
            hint_level=hint_level
        )
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/explain', methods=['POST'])
def ai_explain():
    """Explain why an answer is correct/incorrect"""
    if not ai_agent:
        return jsonify({'error': 'AI not available'}), 503
    
    try:
        data = request.json
        question = data.get('question', '')
        user_answer = data.get('user_answer', '')
        correct_answer = data.get('correct_answer', '')
        
        response = ai_agent.explain_answer(
            question=question,
            user_answer=user_answer,
            correct_answer=correct_answer
        )
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/generate', methods=['POST'])
def ai_generate():
    """Generate custom content (quizzes, flashcards, etc.)"""
    if not ai_agent:
        return jsonify({'error': 'AI not available'}), 503
    
    try:
        data = request.json
        content_type = data.get('type', 'quiz')
        topic = data.get('topic', '')
        difficulty = data.get('difficulty', 'medium')
        
        user_context = {
            'level': session.get('level', 1)
        }
        
        response = ai_agent.generate_content(
            content_type=content_type,
            topic=topic,
            difficulty=difficulty,
            user_context=user_context
        )
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/clear', methods=['POST'])
def ai_clear():
    """Clear conversation history"""
    if not ai_agent:
        return jsonify({'error': 'AI not available'}), 503
    
    try:
        session_id = session.get('session_id', 'session_default')
        ai_agent.clear_conversation(session_id)
        return jsonify({'success': True, 'message': 'Conversation cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/status', methods=['GET'])
def ai_status():
    """Check if AI is available"""
    return jsonify({
        'available': ai_agent is not None,
        'status': 'active' if ai_agent else 'unavailable'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🪷 ThaiBridge AI v3.0 GAMIFIED")
    print("=" * 60)
    print("🪷 ThaiBridge AI v3.0 + AI")
    print("=" * 60)
    print("Features:")
    print("  • Thai Alphabet (44 consonants, 32 vowels)")
    print("  • 6 Vocabulary Categories (20 words each)")
    print("  • Theravada Buddhism: Suttas, Abhidhamma, Vinaya")
    print("  • Meditation Timer: Samatha & Vipassana")
    print("  • 10-Level Progression System")
    print("  • XP & Achievements")
    print("  • 3 Subscription Tiers")
    print("  • Alphabet Completion Requirement")
    print("  • 🤖 AI Learning Assistant (6 modes)")
    print("  • Developer Mode (Password: set via DEVELOPER_PASSWORD env var)")
    print("=" * 60)
    if ai_agent:
        print("AI Status: ✅ Active")
    else:
        print("AI Status: ⚠️ Not configured")
        print("  → Place ai_agent.py in project directory")
        print("  → Set ANTHROPIC_API_KEY environment variable")
        print("  → See QUICK_START.md for setup instructions")
    print("=" * 60)
    print("🔐 Developer Login: http://localhost:5000/developer-login")
    print("📊 Progress Dashboard: http://localhost:5000/progress")
    print("🤖 AI Chat: http://localhost:5000/chat")
    print("=" * 60)
    print("Open browser: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
