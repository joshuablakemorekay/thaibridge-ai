# app.py at 84710a8, lines 722-772
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'FREE Explorer (FREE)',
        'price': 0,
        'features': [
            '✓ Thai alphabet — chart, flashcards & quiz',
            '✓ Theravada Buddhism teachings',
            '✓ Dhamma talks in Thai & English',
            '✓ Pra Kru Bob Dhamma articles',
            '✓ Guided meditation sessions, timer & techniques',
            f'✓ AI Thai tutor — {FREE_AI_DAILY_LIMIT} messages a day',
            f'✓ Dhamma Q&A — {FREE_DHAMMA_DAILY_LIMIT} questions a day, on its own allowance',
            '✓ Paiboon romanization guide',
            '✓ Progress tracking & levelling',
        ],
        'max_level_access': 5,
    },
    'basic': {
        'name': 'Thai Reader (Basic)',
        'price': 9.99,
        'features': [
            '✓ Everything in FREE',
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

# app.py at 84710a8, lines 7800-7865
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
                    'tax_code': TAX_CODE_COURSE,
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

# app.py at 84710a8, lines 8005-8079
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

# app.py at 84710a8, lines 8082-8303
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
    expires_dt = utcnow() + timedelta(days=30)
    _apply_subscription(current_user, tier=tier, status='active',
                        current_period_end=expires_dt)
    _mirror_tier_to_session(current_user)
    session.pop('pending_paypal_tier', None)
    session.modified = True

    return render_template('subscription_success.html',
                           tier=tier,
                           tier_info=SUBSCRIPTION_TIERS[tier],
                           expires=expires_dt.strftime('%d %B %Y'))
