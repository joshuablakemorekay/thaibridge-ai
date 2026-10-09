# app.py at b26522a, lines 597-631
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

# Ceiling on XP earned from practice drills in one day.
#
# The drills are generated in the browser, so the answer is already on the page
# and /api/check_answer cannot tell a learner from a script — nothing it is
# sent can prove the question was really faced. Verifying harder is not the
# answer; bounding the reward is. 200 is twenty correct answers, comfortably
# more than a real sitting, and it caps a scripted run at a couple of days'
# honest work rather than an instant level 10.
#
# This matters more since levelling started earning a free paid section: XP is
# no longer only a score, it opens a door. The counter lives in user_progress
# rather than a bare session key so it is saved with the rest of a learner's
# progress and a cookie wipe does not hand back a fresh allowance.
DRILL_XP_DAILY_CAP = 200
FREE_AI_ALLOWED_MODES = {'tutor', 'buddhist'}  # AI modes free & basic can use

# Pro is "unlimited" in the sense that matters to a learner, but not literally:
# without a ceiling, one subscriber could run up more in API costs than they pay.
# At 0.285p worst case per message (a full 500-token reply on top of the ~1,100
# token system prompt), 150 a day is £12.84 a month against £19.99 of revenue —

# app.py at b26522a, lines 1297-1314
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

# app.py at b26522a, lines 8390-8500
@app.route('/api/ai/chat', methods=['POST'])
# ~30 messages an hour is far more than a learner types and far less than a
# script manages in a second. The per-session daily cap still does the real
# product work; this only stops something that ignores cookies entirely.
@limiter.limit("30 per hour; 200 per day", key_func=_rate_limit_key)
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
        scenario = data.get('scenario') or None
        # Give this visitor a conversation id and KEEP it. Reading with a
        # default and never storing it handed out a fresh id on every request,
        # which quietly broke three things: ai_agent keys its conversation
        # history on this, so the AI started from nothing every message and
        # "conversation mode" was never a conversation; its history dict grew a
        # dead entry per message; and /api/ai/clear had nothing to clear.
        session_id = _visitor_session_id()

        # --- Freemium gate: free & basic get a taste, Pro a fair-use ceiling ---
        tier = active_tier()
        if tier != 'pro':
            if mode not in FREE_AI_ALLOWED_MODES:
                # Logged even though it cost nothing: a blocked request is the
                # conversion signal, not spend. Recording only successes would
                # lose the answer to "do people who hit a wall subscribe?"
                log_ai_usage('chat', 'blocked_mode', mode=mode)
                return jsonify({
                    'success': False,
                    'gate': 'mode_locked',
                    'message': "This AI mode is a Pro feature. Free and Basic plans "
                               "include the Tutor and Dhamma modes — upgrade to Pro to "
                               "unlock Conversation, Culture and the Exercise Generator.",
                })
            usage = _ai_usage_today()
            if usage['count'] >= FREE_AI_DAILY_LIMIT:
                log_ai_usage('chat', 'blocked_cap', mode=mode)
                return jsonify({
                    'success': False,
                    'gate': 'daily_limit',
                    'message': f"You’ve used your {FREE_AI_DAILY_LIMIT} free AI messages "
                               "for today. Upgrade to Pro for a much higher "
                               "daily allowance, or come back tomorrow.",
                })

        # Pro has no daily allowance to spend, but it does have a ceiling — see
        # PRO_FAIR_USE_DAILY. Anonymous visitors are skipped: a Pro tier requires
        # an account, so there is no reliable identity to count against, and the
        # per-IP rate limit still applies to them.
        elif current_user.is_authenticated:
            if _pro_messages_today() >= PRO_FAIR_USE_DAILY:
                log_ai_usage('chat', 'blocked_fairuse', mode=mode)
                return jsonify({
                    'success': False,
                    'gate': 'fair_use',
                    'message': f"You've reached today's fair-use limit of "
                               f"{PRO_FAIR_USE_DAILY} AI messages. It resets at "
                               "midnight. This is here to keep the AI affordable "
                               "to run, not to interrupt your study — if you "
                               "regularly need more, please get in touch.",
                })

        # Get user context from session
        user_context = {
            'level': session.get('level', 1),
            'xp': session.get('xp', 0),
            'name': session.get('username', 'Student')
        }

        # Get AI response (max_tokens controls API cost)
        response = ai_agent.chat(
            message=message,
            mode=mode,
            session_id=session_id,
            user_context=user_context,
            max_tokens=500,
            scenario=scenario
        )

        # Record what it cost. ai_agent has returned these token counts all
        # along and nothing read them, so the spend was invisible.
        if isinstance(response, dict) and response.get('success'):
            tokens = response.get('tokens_used') or {}
            log_ai_usage('chat', 'ok', mode=mode, model=getattr(ai_agent, 'model', None),
                         input_tokens=tokens.get('input', 0),
                         output_tokens=tokens.get('output', 0))
        else:
            # The agent caught the failure itself and returned it, so no
            # exception reaches the handler below — without this branch those
            # failures would be missing from the record entirely.
            log_ai_usage('chat', 'error', mode=mode,
                         model=getattr(ai_agent, 'model', None),
                         error_type=(response or {}).get('error_type')
                                    if isinstance(response, dict) else 'bad_response')

        # Count this message against the daily taste for free & basic users,
        # and tell the UI how many they have left.
        if tier != 'pro' and isinstance(response, dict) and response.get('success'):
            usage = _ai_usage_today()
            usage['count'] += 1
            session['ai_usage'] = usage
            session.modified = True
            response['remaining'] = max(0, FREE_AI_DAILY_LIMIT - usage['count'])

        return jsonify(response)

# app.py at b26522a, lines 1276-1284
def _ai_usage_today():
    """Return today's AI-usage record from the session, resetting at midnight."""
    today = datetime.now().strftime('%Y-%m-%d')
    usage = session.get('ai_usage')
    if not usage or usage.get('date') != today:
        usage = {'date': today, 'count': 0}
        session['ai_usage'] = usage
    return usage
