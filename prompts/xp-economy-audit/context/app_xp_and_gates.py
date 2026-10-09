# app.py at bc471ce, lines 495-651
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
    # The free foundation: the Theravada Dhamma teachings — the Dhamma itself
    # is freely given.
    # Every other content section sits behind a paid tier (see below), on TOP
    # of its level/XP requirement.
    #
    # Meditation moved to 'basic' for a while, on the reasoning that the page had
    # grown from a bare timer into practice *tooling*. It is back here now: sitting
    # in meditation is not tooling, it is the practice the teachings are for, and
    # splitting "the Dhamma is free but learning to practise it costs £9.99" was a
    # line that could not be defended. Dhamma Talks sit here for the same reason.
    'home': {'level': 1, 'tier': 'free', 'points_reward': 0},
    # The alphabet is free on purpose. It is the prerequisite for every
    # section below, so charging for it would put the whole site behind the
    # paywall with no way in.
    'alphabet': {'level': 1, 'tier': 'free', 'points_reward': 100, 'requires_alphabet': False},
    'theravada': {'level': 1, 'tier': 'free', 'points_reward': 40},
    'meditation': {'level': 1, 'tier': 'free', 'points_reward': 40},
    # Chanting sits with the other Dhamma pages: the chants and their
    # translations are not ours to sell, and there is no alphabet
    # prerequisite — you do not need to read Thai to chant along.
    'chanting': {'level': 1, 'tier': 'free', 'points_reward': 40},
    # Paiboon was Basic for a while, filed with the Learn menu it sits in. It is
    # free now because the free pages already USE it: the chanting layers and the
    # meditation techniques print Paiboon on screen. Charging for the guide meant
    # showing a free reader "kam buu-chaa" and then selling them the key to it —
    # a notation key is not a lesson, it is the legend on the map.
    'paiboon': {'level': 1, 'tier': 'free', 'points_reward': 10, 'requires_alphabet': True},

    # ── BASIC — Thai Reader (£9.99) ─────────────────────────────────
    # The structured language-learning content (the rest of the Learn menu,
    # Culture, and the exercises). Still gated by level/XP as well as the tier.
    # Vocabulary sits in the Learn menu alongside the sections below, so it carries
    # the same alphabet prerequisite. It also earns XP on unlock like every one of
    # its siblings — a 0 reward made its locked page read "+0 XP upon unlock" while
    # the rest promised something.
    'learn': {'level': 1, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'exercise_festivals': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_isan_dialect': {'level': 2, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'vowels_syllables': {'level': 2, 'tier': 'basic', 'points_reward': 20, 'requires_alphabet': True},
    'read_write': {'level': 2, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    'exercise_nature': {'level': 3, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'exercise_formal': {'level': 3, 'tier': 'basic', 'points_reward': 15, 'requires_alphabet': True},
    'grammar': {'level': 3, 'tier': 'basic', 'points_reward': 25, 'requires_alphabet': True},
    # Consonant classes + tone rules. Its content was moved here from the Grammar
    # page, so it's gated the same way — Basic tier, level 3.
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

# Freemium AI limits. Free & Basic get the Tutor mode plus Dhamma, capped at a
# few messages a day between them. Pro unlocks every mode with no cap. Dhamma is
# free because the teachings on this site are free — charging for the follow-up
# question would be selling the Dhamma, the same line we refused to cross when
# Meditation went back to the free tier. The daily cap isn't a toll on the
# teaching, it's the honest cost of running the model. The daily counter lives in
# the SESSION (not the DB) on purpose — it needs no schema change and also works
# for logged-out visitors. It's a soft limit (a determined user could clear
# cookies to reset it), which is fine for a portfolio/demo app. Defined here,
# above SUBSCRIPTION_TIERS, so the Free tier's feature list can quote the real
# number instead of a hardcoded one that goes stale.
FREE_AI_DAILY_LIMIT = 15                       # messages/day for free & basic tiers
FREE_AI_ALLOWED_MODES = {'tutor', 'buddhist'}  # AI modes free & basic can use

# Pro is "unlimited" in the sense that matters to a learner, but not literally:
# without a ceiling, one subscriber could run up more in API costs than they pay.
# At 0.285p worst case per message (a full 500-token reply on top of the ~1,100
# token system prompt), 150 a day is £12.84 a month against £19.99 of revenue —
# still profitable even if someone maxes it out every single day of the month.
#
# The number is chosen to be invisible: ten times the free allowance, and roughly
# three times what a genuinely heavy day of study looks like. Anyone who reaches
# it is not studying, and the reply says so kindly and invites them to get in
# touch rather than treating them as an abuser.
PRO_FAIR_USE_DAILY = 150

# Subscription tiers
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free Explorer (Free)',
        'price': 0,
        'features': [
            '✓ Thai alphabet — chart, flashcards & quiz',
            '✓ Theravada Buddhism teachings',
            '✓ Dhamma talks in Thai & English',
            '✓ Pra Kru Bob Dhamma articles',
            '✓ Guided meditation sessions, timer & techniques',
            f'✓ AI Tutor & Dhamma Q&A — {FREE_AI_DAILY_LIMIT} messages a day',
            '✓ Paiboon romanization guide',
            '✓ Progress tracking & levelling',
        ],
        'max_level_access': 5,
    },
    'basic': {
        'name': 'Thai Reader (Basic)',
        'price': 9.99,
        'features': [
            '✓ Everything in Free',
            '✓ Vowels, syllables & Read & Write Script',
            '✓ Tones & consonant classes',
            '✓ Vocabulary, grammar & lessons',
            '✓ Sentences & conversations, with audio',
            '✓ Culture, formality, register & gender guides',
            '✓ Themed exercise sets',
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
            '✓ Everything in Thai Reader',
            f'✓ Unlimited AI chat — every mode, fair use up to {PRO_FAIR_USE_DAILY}/day',
            '✓ AI conversation partner with roleplay scenarios',
            '✓ Culture AI Q&A',
            '✓ AI exercise generator',
            '✓ Thai–English dictionary',
            '✓ 3x points multiplier',
            '✓ Priority support',
        ],
        'max_level_access': 10,
        'points_multiplier': 3,
    }
}

# app.py at bc471ce, lines 680-728
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

# app.py at bc471ce, lines 1251-1343
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

# app.py at bc471ce, lines 6856-6886
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

# app.py at bc471ce, lines 7804-7818
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
