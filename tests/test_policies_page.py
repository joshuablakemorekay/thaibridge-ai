"""The policies page quotes prices and allowances; they must be the live ones."""
import app as appmod


def test_policies_page_quotes_the_numbers_the_app_enforces():
    body = appmod.app.test_client().get('/policies').get_data(as_text=True)
    tiers = appmod.SUBSCRIPTION_TIERS
    assert f"{appmod.FREE_AI_DAILY_LIMIT} messages a day" in body
    assert f"{appmod.BASIC_AI_DAILY_LIMIT} AI tutor messages a day" in body
    assert f"{appmod.PRO_FAIR_USE_DAILY} messages a day" in body
    assert f"£{tiers['basic']['price']:.2f} a month" in body
    assert f"£{tiers['pro']['price']:.2f} a month" in body
    assert f"£{appmod.INSTANT_ACCESS_ADDON['price']:.2f} once" in body


def test_policies_page_is_linked_from_every_page():
    body = appmod.app.test_client().get('/about').get_data(as_text=True)
    assert 'href="/policies"' in body
