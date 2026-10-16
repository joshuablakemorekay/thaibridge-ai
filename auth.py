"""Account routes: sign up, log in, log out, and reset or change a password.

A Flask Blueprint — a bundle of routes registered on the app in app.py. Like
every other module it never imports app.py: it gets the database and User from
models.py, the limiter and login manager from extensions.py, and the password
rules and emails from accounts.py.

The one thing it deliberately does NOT do is restore a learner's saved XP and
level when they log in. That is gamification, and it lives in app.py. app.py
listens for Flask-Login's user_logged_in signal instead, so these routes only
have to call login_user() and the progress follows.
"""

import re

from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

import accounts
from extensions import _failed_attempt_only, _rate_limit_key, limiter, login_manager
from models import User, db

bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    """Given the id stored in the session, return the matching User (or None).

    The id is "<user id>:<session version>" (User.get_id). A version that no
    longer matches means the password has changed since this cookie was issued,
    so the visitor is treated as signed out. A bare "<user id>" is a cookie from
    before versions existed: it counts as version 0, so shipping this signed
    nobody out — only a later password change does."""
    uid, _, version = str(user_id).partition(':')
    try:
        user = db.session.get(User, int(uid))
        version = int(version or 0)
    except ValueError:
        return None
    if user is None or (user.session_version or 0) != version:
        # Sign this device out properly, once. Flask-Login leaves a rejected id
        # in the session and keeps the remember-me cookie, so without this the
        # dead id came back on every page — and each time, the line below wiped
        # whatever the visitor had earned since as a guest. '_remember': 'clear'
        # tells Flask-Login to delete that cookie on this response.
        session.pop('_user_id', None)
        session.pop('_fresh', None)
        session['_remember'] = 'clear'
        # Same as /logout: don't leave this account's cached progress behind.
        session.pop('user_progress', None)
        return None
    return user


@bp.route('/login', methods=['GET', 'POST'])
# Brute-force protection. POST only, so viewing the form is never limited, and
# failures only, so a real learner signing in is never charged for it.
@limiter.limit("10 per 15 minutes; 40 per hour", key_func=_rate_limit_key,
               methods=["POST"], deduct_when=_failed_attempt_only)
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

    return jsonify({
        'success': True,
        'message': f'Welcome back, {user.username}!',
        'redirect': '/'
    })


@bp.route('/logout')
def logout():
    """Log the current user out and reset their session progress."""
    logout_user()
    session.pop('user_progress', None)   # clear cached progress so it doesn't bleed across logins
    return redirect('/')


# ============================================
# PASSWORD RESET AND CHANGE
# ============================================
#
# Forgotten passwords are reset by emailed link; logged-in users can change
# theirs on /progress. Before this, a forgotten password meant Josh editing the
# live database by hand. The rules, reset links and emails live in accounts.py;
# these routes only handle the web side.


def _tell_owner_password_changed(user):
    accounts.send_changed_email(
        user, accounts.public_base_url() + url_for('auth.forgot_password'))


@bp.route('/forgot-password', methods=['GET', 'POST'])
# Counts every request: each one can send an email, so this guards against
# someone flooding a stranger's inbox as much as against probing for accounts.
@limiter.limit("5 per 15 minutes; 20 per hour", key_func=_rate_limit_key,
               methods=["POST"])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')

    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    if not email:
        return jsonify({'success': False, 'message': 'Please enter your email address.'}), 400

    user = User.query.filter_by(email=email).first()
    if user is not None:
        token = accounts.make_reset_token(user)
        accounts.send_reset_email(
            user, accounts.public_base_url() + url_for('auth.reset_password', token=token))

    # Identical reply either way, so this page can't be used to find out
    # whether an email address has an account here.
    return jsonify({
        'success': True,
        'message': "If an account uses that email, we've sent it a link to reset "
                   "the password. Check your inbox (and spam folder). The link "
                   "expires in 30 minutes.",
    })


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
@limiter.limit("10 per 15 minutes; 40 per hour", key_func=_rate_limit_key,
               methods=["POST"], deduct_when=_failed_attempt_only)
def reset_password(token):
    user = accounts.user_from_reset_token(token, lambda uid: db.session.get(User, uid))

    if request.method == 'GET':
        return render_template('reset_password.html', token_valid=user is not None)

    if user is None:
        return jsonify({'success': False,
                        'message': 'This reset link has expired or has already been used. '
                                   'Please ask for a new one.'}), 400

    data = request.get_json(silent=True) or {}
    problem = accounts.password_problem(data.get('password', ''), data.get('confirm_password', ''))
    if problem:
        return jsonify({'success': False, 'message': problem}), 400

    user.set_password(data['password'])
    db.session.commit()
    _tell_owner_password_changed(user)

    # Proving you own the inbox is as good as knowing the old password.
    login_user(user, remember=True)
    return jsonify({'success': True,
                    'message': 'Your password has been changed. Welcome back!',
                    'redirect': '/'})


@bp.route('/change-password', methods=['POST'])
@login_required
# Asks for the current password, so it is a password-guessing door like /login.
@limiter.limit("10 per 15 minutes; 40 per hour", key_func=_rate_limit_key,
               deduct_when=_failed_attempt_only)
def change_password():
    data = request.get_json(silent=True) or {}
    if not current_user.check_password(data.get('current_password', '')):
        return jsonify({'success': False, 'message': 'Your current password is not right.'}), 400

    problem = accounts.password_problem(data.get('new_password', ''), data.get('confirm_password', ''))
    if problem:
        return jsonify({'success': False, 'message': problem}), 400

    user = current_user._get_current_object()
    user.set_password(data['new_password'])
    db.session.commit()
    # The new password signed out every device, this one included. Re-issue
    # this device's cookies so the person who just changed it stays signed in.
    login_user(user, remember=True)
    _tell_owner_password_changed(user)
    return jsonify({'success': True, 'message': 'Your password has been changed.'})


# ============================================
# USER REGISTRATION ROUTE
# ============================================

@bp.route('/signup', methods=['GET', 'POST'])
# Counts EVERY attempt, unlike the sign-in routes: the abuse here is mass
# account creation, which succeeds each time, so counting only failures would
# never see it. Generous enough for a group signing up on one shared
# connection, which is a realistic evening at a monastery.
@limiter.limit("10 per hour; 30 per day", key_func=_rate_limit_key,
               methods=["POST"])
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
    problem = accounts.password_problem(password, confirm_password)
    if problem:
        return jsonify({'success': False, 'message': problem}), 400
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

    return jsonify({
        'success': True,
        'message': f'Welcome, {new_user.username}! Your account has been created.',
        'redirect': '/'
    })
