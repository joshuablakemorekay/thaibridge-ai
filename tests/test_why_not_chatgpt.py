"""The "Why not just use ChatGPT?" section on the pricing page.

It answers the question people ask before paying, and it answers with the
course rather than the AI. These pin the claims that must stay true.
"""
from app import app


def page():
    app.config["TESTING"] = True
    return app.test_client().get("/premium").get_data(as_text=True)


def section():
    html = page()
    start = html.index('id="why-not-chatgpt"')
    return html[start:html.index("</section>", start)]


def test_the_pricing_page_answers_the_question():
    assert "Why not just use ChatGPT?" in section()


def test_it_leads_with_the_course_not_the_ai():
    text = section()
    assert "checked by a native Thai teacher" in text
    assert "the helper inside all this" in text


def test_it_never_calls_the_audio_real_or_recorded():
    text = section().lower()
    assert "tap-to-hear" in text
    assert "real audio" not in text and "recorded" not in text


def test_it_only_claims_the_course_is_teacher_checked():
    """The trips and the chanting book have not been reviewed."""
    assert "The course's Thai is checked" in section()
