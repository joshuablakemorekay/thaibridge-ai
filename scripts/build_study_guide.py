"""Build "Thinking Ahead", the independent-thinking study guide, as an A4 PDF.

    python scripts/build_study_guide.py                  # writes docs/thinking-ahead-study-guide.pdf
    python scripts/build_study_guide.py some/other.pdf   # writes somewhere else

The guide retells this project's history (JOURNAL.md and the commit log) as
lessons in anticipating problems: the six planning questions answered with
hindsight, each build stage with the thinking skill it taught, and real
incidents set out as predict-then-read exercises.

The words live in this file, not in a data file, because they are prose
written once and edited by hand, not records the app reads.

The figures in it (commit count, test count, dates) are a SNAPSHOT from
3 November 2026, stated as such on the cover. Rebuilding does not refresh
them; edit the text first if you want them current.

ReportLab with Segoe UI (a Windows font), so this builds on Windows only.
That is fine for a guide that is built by hand and committed as a PDF, and
it is why the guide carries no Thai script: ReportLab places Thai vowels and
tone marks wrongly (see build_chanting_print.py, which uses Chrome instead).
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "docs" / "thinking-ahead-study-guide.pdf")

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Body", F + "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", F + "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", F + "segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("Body-BoldItalic", F + "segoeuiz.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Body", normal="Body", bold="Body-Bold",
                   italic="Body-Italic", boldItalic="Body-BoldItalic")

SAFFRON = colors.HexColor("#B4610E")
GOLD = colors.HexColor("#C99A2E")
INK = colors.HexColor("#2B2622")
MUTED = colors.HexColor("#6B625A")
CREAM = colors.HexColor("#FBF5EA")
PALE = colors.HexColor("#F3E6CF")
TEAL = colors.HexColor("#2F6B66")
TEAL_PALE = colors.HexColor("#E3F0EE")

S = {}
S["body"] = ParagraphStyle("body", fontName="Body", fontSize=10.5, leading=15.5,
                           textColor=INK, spaceAfter=6)
S["small"] = ParagraphStyle("small", parent=S["body"], fontSize=9.5, leading=13.5,
                            textColor=MUTED)
S["h1"] = ParagraphStyle("h1", fontName="Body-Bold", fontSize=20, leading=25,
                         textColor=SAFFRON, spaceBefore=4, spaceAfter=10)
S["h2"] = ParagraphStyle("h2", fontName="Body-Bold", fontSize=13.5, leading=18,
                         textColor=INK, spaceBefore=12, spaceAfter=5)
S["h3"] = ParagraphStyle("h3", fontName="Body-Bold", fontSize=11, leading=15,
                         textColor=SAFFRON, spaceBefore=8, spaceAfter=3)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=14,
                             bulletIndent=3, spaceAfter=3)
S["box"] = ParagraphStyle("box", parent=S["body"], fontSize=10, leading=14.5,
                          spaceAfter=4)
S["boxhead"] = ParagraphStyle("boxhead", parent=S["box"], fontName="Body-Bold",
                              textColor=TEAL, spaceAfter=3)
S["cell"] = ParagraphStyle("cell", parent=S["body"], fontSize=9.5, leading=13,
                           spaceAfter=0)
S["cellb"] = ParagraphStyle("cellb", parent=S["cell"], fontName="Body-Bold")
S["cover_t"] = ParagraphStyle("ct", fontName="Body-Bold", fontSize=30, leading=36,
                              textColor=SAFFRON, alignment=TA_LEFT)
S["cover_s"] = ParagraphStyle("cs", fontName="Body", fontSize=14, leading=20,
                              textColor=INK)

story = []
P = lambda t, s="body": story.append(Paragraph(t, S[s]))


def bullets(items, style="bullet"):
    for it in items:
        story.append(Paragraph(it, S[style], bulletText="\u2022"))


def box(title, lines, bg=TEAL_PALE, edge=TEAL):
    inner = [Paragraph(title, S["boxhead"])] + [Paragraph(l, S["box"]) for l in lines]
    t = Table([[inner]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 4))
    story.append(KeepTogether(t))
    story.append(Spacer(1, 8))


def grid(rows, widths, head=True):
    data = [[Paragraph(c, S["cellb"] if (head and i == 0) else S["cell"]) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if head else 0)
    st = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2D5BF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), PALE))
    t.setStyle(TableStyle(st))
    story.append(t)
    story.append(Spacer(1, 8))


def writing_lines(n):
    t = Table([[""] for _ in range(n)], colWidths=[170 * mm], rowHeights=[9 * mm] * n)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#CDBFA8"))]))
    story.append(t)


# ---------------------------------------------------------------- cover
story.append(Spacer(1, 45 * mm))
P("Thinking Ahead", "cover_t")
story.append(Spacer(1, 4))
P("Independent-thinking lessons from building ThaiBridge AI, start to finish", "cover_s")
story.append(Spacer(1, 10 * mm))
P("A personal study guide for Joshua Kay", "body")
P("Built from 1,075 commits (22 Feb 2026 to 28 Oct 2026) and the project journal", "small")
P("Prepared 3 November 2026", "small")
story.append(Spacer(1, 30 * mm))
box("The skill this guide trains",
    ["My Senior Advisor's advice: <b>be flexible in your thinking, and be able to anticipate "
     "the next few steps.</b>",
     "This guide doesn't teach you to write code. It teaches the habit of thinking that "
     "sits behind good code, and that habit carries over to farming, logistics, running a "
     "business and running a project. All the examples come from things you have "
     "already built, broken and fixed."],
    bg=CREAM, edge=SAFFRON)
story.append(PageBreak())

# ---------------------------------------------------------------- how to use
P("How to use this guide", "h1")
P("ThaiBridge wasn't built from a perfect plan. It was built the way real projects "
  "usually are: a rough idea, a first version, then a long run of surprises. The good "
  "news is that every surprise can be turned into a lesson. Looking back over finished work "
  "and asking <i>\u201cwhat could I have seen coming?\u201d</i> is one of the fastest ways "
  "to get better at seeing what's coming next time.")
P("Read it in three passes:")
bullets([
    "<b>Pass 1 - the big picture (pages 3-5).</b> The six questions every project should "
    "answer, answered for ThaiBridge now that we know how things turned out.",
    "<b>Pass 2 - the journey (pages 6-7).</b> Each stage from November 2025 to now: what was "
    "built, what went wrong, and the thinking skill it taught.",
    "<b>Pass 3 - practise (pages 8-11).</b> Real incidents set out as puzzles. "
    "<b>Cover the answer, make your prediction, then read on.</b> Being wrong here is the "
    "point of the exercise.",
])
box("The one question to carry everywhere",
    ["<b>\u201cWhat happens next, and what else does this touch?\u201d</b>",
     "Almost every surprise in this project came from something that looked finished "
     "but was quietly connected to something else: a database wiped on every deploy, "
     "a price that included tax in one place and not another, a phone layout that broke "
     "a page nobody had touched."])

P("The four thinking moves", "h2")
grid([
    ["Move", "What it means", "The ThaiBridge habit"],
    ["1. Zoom out", "Before acting, ask what the thing is <i>for</i> and who relies on it.",
     "\u201cThe alphabet is the way in, so it has to be free.\u201d"],
    ["2. Look ahead", "Run the clock forward: after this, then what? Then what?",
     "\u201cIf progress lives in a cookie, a new phone loses it.\u201d"],
    ["3. Look for the hidden link", "Ask what else depends on this, or what it depends on.",
     "\u201cThe webhook trusts metadata, not the session ID.\u201d"],
    ["4. Check the source", "Separate what you <i>know</i> from what you <i>assume</i>. "
     "Prove it from the real thing.",
     "\u201cA confident answer from the wrong source is worse than no answer.\u201d"],
], [32, 70, 68])
story.append(PageBreak())

# ---------------------------------------------------------------- six questions
P("Part 1 - The six big questions, answered", "h1")
P("These are the six questions from the reusable prompt's \u201cFirst action\u201d. At the "
  "start of a project you answer them with guesses. Answering them <i>now</i>, with "
  "hindsight, shows you what good answers look like.", "small")

P("1. What problem are we solving?", "h2")
P("English speakers who are drawn to Thailand (expats, travellers, students and people "
  "interested in Theravada Buddhism) have nowhere to learn Thai <i>together with</i> the "
  "culture and the Dhamma. The March-April 2026 research confirmed it: the big language "
  "apps don't teach Thai at all, and none of them combine it with Buddhist culture.")
box("Thinking skill: name the gap, then check it's real",
    ["You researched competitors and audience <i>before</i> building more. Lots of people "
     "skip this and build something nobody needs. Next time, write the problem in one "
     "sentence and find three pieces of evidence that it's real."])

P("2. What does the finished product need to do?", "h2")
bullets([
    "Teach the foundations: alphabet, tones, consonant classes, vocabulary and sentences, "
    "with audio for everything.",
    "Give learners an AI tutor that is <b>accurate</b>. A wrong answer from a tutor is worse "
    "than no answer at all.",
    "Respect the source material: the chanting book, Pra Kru Bob's writings, real Thai "
    "checked by native speakers.",
    "Earn money fairly through Free, Reader, Pro and an Instant Access Pass, while keeping "
    "the Dhamma freely given.",
    "Keep accounts, progress and payments safe and lasting.",
])

P("3. What is the simplest appropriate technical solution?", "h2")
grid([
    ["Part", "What ThaiBridge uses", "Why this is the simple choice"],
    ["Web app", "Flask (Python)", "One language for everything; small and easy to understand."],
    ["Pages", "HTML templates + CSS", "No heavy front-end framework needed for a content site."],
    ["Database", "SQLite locally, Neon Postgres live",
     "SQLite needs no setup; Postgres survives redeploys (see Case 3)."],
    ["AI", "Claude API (Sonnet 5.5) via ai_agent.py", "One provider, one file, an accuracy exam guarding it."],
    ["Payments", "Stripe Checkout + webhooks", "Stripe handles cards, tax and receipts so you don't have to."],
    ["Hosting", "Render (auto-deploy from main)", "Free tier, a push to GitHub puts it live."],
    ["Safety net", "Git + 970-odd automated tests", "You can take risks because you can check and roll back."],
], [28, 62, 80])
story.append(PageBreak())

P("4. What were the major development stages?", "h2")
P("Looking back, the order made sense, and each stage <i>needed</i> the one before it:")
grid([
    ["#", "Stage", "Why it had to come here"],
    ["0", "Plan and cut to an MVP", "Without a small target, nothing gets finished."],
    ["1", "First working version + AI tutor", "You need something real to test and learn from."],
    ["2", "Git, tests, sign-up", "A safety net before making bigger changes."],
    ["3", "Market research", "Check the idea is worth more time before investing it."],
    ["4", "Layout, payments, going live", "Real users and real money show the real problems."],
    ["5", "Content tracks, access model, audio", "Once it's live, make it worth paying for."],
    ["6", "Chanting book + a database that lasts", "Scale exposed the weak foundation."],
    ["7", "Payments ledger, honest prices", "Money is where mistakes hurt trust most."],
    ["8", "Tutor accuracy, accounts, learning tools", "Quality and safety for a growing app."],
], [8, 62, 100])

P("5. What problems should we anticipate?", "h2")
P("These are the <b>categories</b> that kept coming up. When you start something new, "
  "go through this list and ask \u201cwhere could this bite me?\u201d")
bullets([
    "<b>Things that look finished but aren't</b>: a page that loads but links nowhere, "
    "tests that pass while running against the wrong database.",
    "<b>Things that vanish</b>: data stored on a disk that resets, a secret key set for "
    "one terminal only, progress kept in a browser cookie.",
    "<b>Money leaks</b>: a public AI link spending your credits, a paid quiz left open, a "
    "price that differs from the charge.",
    "<b>Trust and accuracy</b>: an AI teaching wrong Thai, a summary that drops "
    "paragraphs of a sacred text.",
    "<b>Different devices</b>: an iPhone layout that buries the page under a sidebar.",
    "<b>Wrong source of truth</b>: checking an old Stripe account, trusting a code "
    "comment over the real settings.",
])

P("6. What should I understand before beginning?", "h2")
bullets([
    "<b>Where things live.</b> Most early errors were files in the wrong folder.",
    "<b>Where data lives, and how long it lasts.</b> Browser, server disk or database?",
    "<b>Who can see what.</b> What's free, what's paid, what's secret (keys in .env, "
    "never in code).",
    "<b>How you'll know it works.</b> Decide the test <i>before</i> you build.",
    "<b>\u201cDone\u201d means checked by you</b>, not claimed by an AI.",
])
story.append(PageBreak())

# ---------------------------------------------------------------- journey
P("Part 2 - The journey, stage by stage", "h1")
P("For each stage: <b>what was built</b>, <b>what went wrong or was learned</b>, and "
  "<b>the thinking skill</b> it trains. Try to spot the skill before you read it.", "small")

stages = [
    ("Stage 0 - Nov 2025: Planning the app",
     "A describe-then-check plan: tell the AI exactly what you want, judge what comes back, refine.",
     "The plan ballooned into a huge, expensive vision. Progress only started after cutting it to a small working version.",
     "<b>Scope control.</b> Ask \u201cwhat is the smallest version that is actually useful?\u201d"),
    ("Stage 1 - Nov-Dec 2025: First version and the AI tutor",
     "Flask backend, alphabet and vocabulary, lessons, points and levels, then a Claude-powered tutor with several modes.",
     "\u201cTemplate not found\u201d was a file in the wrong place. The API key vanished because it was set for one terminal only. "
     "An AI said the chat worked when it didn't. A romanisation accent bug was so deep that a workaround was the right call.",
     "<b>Read the error message</b>, and <b>know when to stop polishing</b> and choose a workaround."),
    ("Stage 2 - Feb 2026: Version control and a real workflow",
     "Git and GitHub, user registration with a database, 32 tests for the points logic, a first code review.",
     "Empty forms could be submitted, and a database error could crash the app. When Claude Code ran out of credits, you made two fixes by hand.",
     "<b>Build the safety net first.</b> With rollback available, you can take bigger risks calmly."),
    ("Stage 3 - Mar-Apr 2026: Is it worth building?",
     "Competitor, audience and pricing research, with the prompts saved in /prompts.",
     "A web-scraping tool you'd named in a prompt had never actually run.",
     "<b>Check which tools actually ran.</b> \u201cI asked for X\u201d is not \u201cX happened\u201d."),
    ("Stage 4 - Jun 2026: Layout, payments, going live",
     "A site outline and shared layout, Stripe and PayPal, real subscriptions, the first public deploy on Render, and a cost-safe AI demo.",
     "A renewal-date bug turned up in the first test payment. A public AI link spends <i>your</i> credits, so you added a cheap model, a daily limit, "
     "a separate API key as a kill switch, and a hard spend cap.",
     "<b>Ask \u201cwho pays if this goes wrong?\u201d</b> Layer your protections so no single one has to be perfect."),
    ("Stage 5 - Jul 2026: Making it worth paying for",
     "Monk Mode, a reworked access model, tones and consonant classes, a rebuilt alphabet, audio everywhere, an accessibility panel, Jataka tales.",
     "The \u201cbroken\u201d iPhone alphabet page was really three lines of shared CSS. A story link went to a missing page while raising no error.",
     "<b>Find the real cause before rebuilding.</b> The worst bugs raise no error, so make the app check itself."),
    ("Stage 6 - Aug 2026: The chanting book and a database that lasts",
     "A pipeline for 286+ chants that proves nothing was lost, and a move from SQLite to Neon Postgres.",
     "The live site had been deleting every account on every deploy. Your own tests had been running against the live database.",
     "<b>Ask \u201chow long does this last, and where does it live?\u201d</b> about every piece of data."),
    ("Stage 7 - Sep 2026: Money you can trust",
     "A payments ledger, receipts on /progress, a real live-money test.",
     "A \u00a39.99 plan charged \u00a311.99 (VAT). The first fix raised every price; the right fix was one line telling Stripe the price already includes tax. "
     "A key file was one command away from being made public.",
     "<b>Fix the right thing.</b> When two parts disagree, ask which one should change."),
    ("Stage 8 - Oct 2026: Quality, safety and new tools",
     "Tutor on Sonnet 5.5 with a 17-question accuracy exam, playable Tour Guide trips, password reset, sign-out-everywhere, IEP learning path, "
     "Listening and Writing tools, Translator mode with photo input.",
     "The old tutor model taught wrong Thai and wrong Dhamma. The sign-out feature quietly wiped logged-out visitors' progress, caught by a review after the tests passed. "
     "Three paid quizzes were open to everyone.",
     "<b>Measure quality, don't assume it.</b> A review after \u201cdone\u201d still finds things."),
]
for title, built, wrong, skill in stages:
    rows = [[Paragraph(title, S["h3"])],
            [Paragraph("<b>Built:</b> " + built, S["cell"])],
            [Paragraph("<b>What went wrong or was learned:</b> " + wrong, S["cell"])],
            [Paragraph("<b>Thinking skill:</b> " + skill, S["cell"])]]
    t = Table(rows, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 3), (0, 3), TEAL_PALE),
        ("LINEBELOW", (0, 0), (0, 0), 0.6, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(KeepTogether([t, Spacer(1, 8)]))
story.append(PageBreak())

# ---------------------------------------------------------------- cases
P("Part 3 - Predict before you read", "h1")
P("Each case is a real moment from ThaiBridge. <b>Cover everything below \u201cPause and "
  "predict\u201d</b>, write your answer in the margin, then uncover. The aim isn't to get it "
  "right. It's to build the reflex of <i>predicting</i> before reacting.", "small")

cases = [
    ("Case 1 - The page that wouldn't open on iPhone",
     "The Alphabet page wouldn't work on an iPhone, so the page was rebuilt. Still broken. Rebuilt again. Still broken.",
     "If rebuilding the page twice didn't help, where else could the problem be?",
     "The page was never the problem. Three lines of CSS in the <i>shared</i> layout stacked a 644px sidebar on top of the content on phones. "
     "One small change (moving the main content first on small screens) fixed every page at once.",
     "<b>If fixing the obvious thing doesn't work, the cause is somewhere else.</b> Look at what the thing <i>shares</i> with others. "
     "And ask the failing device what it's actually doing before rebuilding anything."),
    ("Case 2 - The link that raised no error",
     "Five culture stories each linked to a practice page. The page built each link by turning the story's ID into /exercise/&lt;id&gt;.",
     "Can you spot what might go wrong with building links from IDs?",
     "It worked for four stories because their IDs happened to match vocabulary categories. The fifth had no category, so its link pointed at nothing. "
     "No error, no log, a page that loaded fine. The fix: each story says where its link goes, and the app refuses to start if any link is dead.",
     "<b>Anything that works \u201cby coincidence\u201d will break one day.</b> Prefer stating things outright over guessing, "
     "and build checks that fail loudly."),
    ("Case 3 - The database that was deleting itself",
     "The live site stored accounts in a SQLite file on Render's server disk. Render rebuilds the server on every deploy.",
     "What happens to every account each time you push an update?",
     "Every deploy wiped the file, so every account created since the last deploy was silently deleted. The fix was Neon Postgres, a database that lives "
     "separately from the server, proved by registering, redeploying and logging back in. The same session found the test suite had been running "
     "against the live database.",
     "<b>For every piece of data, ask: where does it live, and what wipes it?</b> Then prove survival by actually doing the thing that would wipe it."),
    ("Case 4 - \u00a39.99 that charged \u00a311.99",
     "A live payment test showed Stripe adding 20% VAT on top of a \u00a39.99 plan. You are not VAT registered.",
     "There are two ways to make the advertised price and the charge agree. What are they, and which is fairer to customers?",
     "Option one: raise the advertised price to include VAT. That was tried first and quietly raised every price by 20%. Option two: tell Stripe the price "
     "already includes tax (one line: tax_behavior: inclusive). Stripe is the merchant of record, so it pays the VAT out of the \u00a39.99. "
     "Along the way, two wrong turns: trusting a code comment about account settings, and checking an old Stripe account from a stale .env file.",
     "<b>When two things disagree, decide which one is right before changing either.</b> And check you are looking at the <i>real</i> source."),
    ("Case 5 - The tutor that taught mistakes",
     "The live tutor ran on a cheap, fast model to keep costs down. It sounded confident and fluent.",
     "How would you find out whether a confident AI is actually correct, and what would you do about cost if you switched?",
     "A side-by-side test with the same questions across three models showed the cheap one confusing mett\u0101 with mudit\u0101, inventing teaching, and getting "
     "consonant classes wrong. The tutor moved to Sonnet 5.5. A rule was set first (\u201cit must not lose money\u201d), so the daily limit was lowered and a "
     "monthly cap added. Now a 17-question exam runs before any change to the tutor.",
     "<b>Fluent is not the same as correct.</b> Make a test you can repeat, and set your limits (like cost) <i>before</i> you change things."),
    ("Case 6 - The safety feature that wiped progress",
     "Changing your password now signs you out on every other device. Five tests passed.",
     "A device that's been signed out still has its old login cookie. What happens on that device's next page load, and the one after?",
     "The app rejected the dead cookie on every page, and each time it wiped whatever the visitor had earned since. The tests missed it; a review "
     "afterwards caught it. The fix clears the dead cookie once.",
     "<b>Run the clock forward past the happy path.</b> Ask what happens on the <i>second</i> and <i>third</i> visit, not just the first."),
    ("Case 7 - A public AI link",
     "You want clients to try the AI tutor from your portfolio, with no login needed.",
     "List three ways this could cost you money or cause trouble, and one protection for each.",
     "One person could spam it (fixed with a daily message limit). A bad day could run up a big bill (a hard spend cap, auto-reload off). Abuse could break "
     "your own development work (a separate API key you can switch off on its own). Plus a cheaper model for the public demo.",
     "<b>Ask \u201cwhat's the worst a stranger could do with this?\u201d</b> Then add layers, so no single protection has to be perfect."),
]
for title, situation, q, answer, lesson in cases:
    story.append(KeepTogether([
        Paragraph(title, S["h2"]),
        Paragraph("<b>The situation:</b> " + situation, S["body"]),
        Table([[Paragraph("<b>Pause and predict:</b> " + q, S["box"])]],
              colWidths=[170 * mm],
              style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CREAM),
                                ("LINEBEFORE", (0, 0), (0, -1), 3, SAFFRON),
                                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                                ("TOPPADDING", (0, 0), (-1, -1), 7),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 5)])),
        Spacer(1, 18 * mm),
        Paragraph("<b>What actually happened:</b> " + answer, S["body"]),
        Paragraph("<b>The lesson:</b> " + lesson, S["body"]),
        Spacer(1, 6),
    ]))
story.append(PageBreak())

# ---------------------------------------------------------------- toolkit
P("Part 4 - Your thinking toolkit", "h1")
P("The anticipation checklist", "h2")
P("Run through this <b>before</b> building or changing anything, whether it's a feature, "
  "a business offer or a job on the farm. It comes from the reusable prompt, put into "
  "plain words.")
grid([
    ["Ask yourself", "ThaiBridge example"],
    ["What happens straight after this is used?", "After payment, the webhook must unlock the right plan."],
    ["What depends on this?", "Twenty sections depend on the alphabet quiz being passed."],
    ["What could go wrong?", "The quiz result is stored in a cookie and gets cleared."],
    ["What if someone does something unexpected?", "An empty form, a fake Stripe event, 500 AI messages."],
    ["What if an outside service fails?", "If the AI spend cap is reached, visitors see \u201cthe tutor is resting\u201d, not an error."],
    ["Security, privacy or speed problems?", "Chats kept in the learner's browser, so the server stores no message text."],
    ["What will we need next?", "Accounts led to password reset, which led to sign-out-everywhere."],
    ["Could this choice cause trouble later?", "SQLite on a server disk was fine until the first redeploy."],
], [72, 98])

P("Ten habits that came out of this project", "h2")
habits = [
    "<b>Cut to the smallest useful version</b> before adding anything.",
    "<b>Read the error message.</b> It usually names the problem.",
    "<b>Don't trust \u201cit works\u201d</b>, from an AI or from yourself, until you've checked it.",
    "<b>Know where every piece of data lives</b> and what could wipe it.",
    "<b>Check the real source</b>, not a comment, a memory or an old account.",
    "<b>Fix the cause, not the symptom.</b> Rebuilding the page twice didn't fix the layout.",
    "<b>Make things fail loudly.</b> An app that refuses to start beats a silent dead link.",
    "<b>Decide the test before you build.</b> The tutor exam came before the model switch.",
    "<b>Protect the commitment, not just the wording.</b> When someone criticises how "
    "something is said, keep what it <i>means</i>.",
    "<b>Review after \u201cdone\u201d.</b> The worst bug of October was found after the tests passed.",
]
for i, h in enumerate(habits, 1):
    story.append(Paragraph(h, S["bullet"], bulletText=f"{i}."))
story.append(PageBreak())

# ---------------------------------------------------------------- real world
P("Part 5 - Using this outside code", "h1")
P("My Senior Advisor's point was about <i>real-world</i> activities. The same four moves work anywhere. "
  "Try them on these:")
grid([
    ["Situation", "Zoom out / look ahead / hidden link / check source"],
    ["Your two bee nucs arrive on 13 April 2027.",
     "What has to be ready the day <i>before</i>? What if it rains that week? What depends on the hive stand being level? Who has actually done this locally?"],
    ["A client on PeoplePerHour asks for a \u201cquick change\u201d.",
     "What is it really for? What else does that page touch? What will they ask for next? Is it in the agreed scope?"],
    ["Loading a delivery lorry.",
     "What gets unloaded first? What's fragile or heavy? What happens if one drop-off is cancelled?"],
    ["Launching a new SMOALD offer.",
     "Who pays if it goes wrong? What does the customer do the minute after buying? What does the price page say compared with the checkout?"],
], [55, 115])

P("A five-minute daily practice", "h2")
bullets([
    "Pick one thing you'll do today.",
    "Write down <b>three things that happen after it</b>, then three after each of those.",
    "Circle the one that would hurt most if it went wrong. Add one protection.",
    "That evening, check: did anything happen that you <i>could</i> have predicted?",
])

P("Working with Claude Code this way", "h2")
P("You don't need to start a project from scratch to use the reusable prompt. For "
  "ThaiBridge, try opening a session with one of these:")
bullets([
    "\u201cBefore you build this, ask me to predict what could go wrong, then tell me what I missed.\u201d",
    "\u201cGive me two ways to do this, the trade-off between them, and your recommendation.\u201d",
    "\u201cAfter this stage, give me the short review: built / how it works / risks / what I learned / next.\u201d",
])
story.append(PageBreak())

# ---------------------------------------------------------------- reflection
P("Reflection", "h1")
P("Answer in your own words. Coming back to these in a month is the best way to see how "
  "far your thinking has moved.", "small")
for q in [
    "Which case (1-7) did I predict correctly? What helped me see it?",
    "Which case surprised me most? What question would have caught it?",
    "What is one thing in my current work that \u201clooks finished\u201d but that I haven't proved?",
    "Where does the most important data in my life or business live, and what could wipe it?",
]:
    P(q, "h3")
    writing_lines(4)

# ---------------------------------------------------------------- page decoration
def on_page(c, doc):
    c.saveState()
    if doc.page == 1:
        c.setFillColor(CREAM)
        c.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
        c.setFillColor(SAFFRON)
        c.rect(0, A4[1] - 14 * mm, A4[0], 14 * mm, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, A4[1] - 16 * mm, A4[0], 2 * mm, stroke=0, fill=1)
    else:
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.6)
        c.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
        c.setFont("Body", 8.5)
        c.setFillColor(MUTED)
        c.drawString(20 * mm, 9 * mm, "Thinking Ahead - ThaiBridge AI study guide")
        c.drawRightString(A4[0] - 20 * mm, 9 * mm, str(doc.page))
    c.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=18 * mm, bottomMargin=20 * mm,
                      title="Thinking Ahead - ThaiBridge AI study guide",
                      author="Joshua Kay")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
doc.build(story)
print("ok", OUT)
