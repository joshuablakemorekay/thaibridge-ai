# Build Journal — Thai Language & Culture Learning App

This is the honest record of building my **first web app** — a Thai language and culture learning site — mostly with AI help, as a complete beginner. It's a learning project and a portfolio piece, not a finished product. I've kept the wins and the mistakes in, because the mistakes are where I actually learned.

---

## 6 June 2026 — Taking a real test payment with Stripe (and fixing a renewal-date bug)

**Type:** Milestone

**TL;DR:**
- Took my **first real test-card payment** through Stripe Checkout, end to end.
- Confirmed the webhook (Stripe's server messaging mine) flips the user to a paid plan in the database.
- Fixed a real bug: the subscription's renewal date wasn't being saved.

**What I built or did**
I set up local Stripe testing — the Stripe command-line tool and its webhook forwarder (which relays Stripe's "payment happened" messages to my app) — then paid with the test card `4242 4242 4242 4242`. It activated a real subscription in my database, with a genuine Stripe customer and subscription id attached.

**Why I did it this way**
The webhook is the trustworthy source of truth: a browser redirect can be faked, but a signed server-to-server message can't. Testing it locally proves the whole flow before going live.

**How We Did It**
Confirmed the right folder/branch → fixed an env-var name (`FLASK_SECRET_KEY`) that blocked startup → installed the `stripe` library and command-line tool → forwarded webhook events to `/stripe/webhook` → made a real test payment → verified the database flipped to paid → fixed the renewal-date bug → re-tested.

**What this means for the app**
Paid subscriptions now genuinely work and are safely recorded — the last blocker before going live.

**What I learned**
APIs change: Stripe moved the renewal date onto each subscription *item*, so my code was reading an empty field. The bigger lesson — **a "200 OK" doesn't prove it worked**; only checking the actual database caught both the missing date and the fact my browser first hit a stale tab.

**References / Conversations**
This Claude Code session; the `_subscription_period_end` helper in `app.py`.

---

## 6 June 2026 — Building the real subscription billing service (login, database-backed plans, premium page, freemium AI)

**Type:** Milestone

**TL;DR:**
- Replaced the fake "coming soon" login with **real accounts** (sign up, log in, log out).
- Built a **subscription billing service** where the **database is the source of truth**, not a cookie.
- Added a **premium/pricing page** and **gated the AI tutor** (free taste vs unlimited on Pro).

**What I built or did**
I turned the placeholder paywall into a real system. Real login/logout via Flask-Login (a toolkit that tracks "who is logged in"). Each user now stores their plan, status and Stripe ids in the database, with one rule (`effective_tier`) deciding what they can access. Checkout is tied to the logged-in user, and the Stripe webhook — not the browser — is the trusted thing that marks someone paid, renewed or cancelled. I wired checkout for **both Stripe and PayPal**, though only **Stripe is configured and verified so far** (PayPal is scaffolded for a later session). I merged the old feature showcase and pricing into one **Premium page**, and gated the **AI tutor**: free/basic get a daily taste (5 messages), Pro unlocks all modes unlimited.

**Why I did it this way**
A cookie can be faked; the database can't. Keeping the truth in the database (written only by the signed webhook) means a user can't just edit their browser to unlock Pro. Gating the AI fixed a mismatch — Pro advertised "premium AI" while everyone already got it free.

**How We Did It**
Added real login → added subscription fields to the User → tied checkout to the user → made the webhook the source of truth → enforced access from the database → merged the premium/pricing page → gated the AI tutor.

**What this means for the app**
The app now has a genuine, tamper-resistant freemium model: real accounts, plans stored safely, and paid features that are actually locked.

**What I learned**
"Source of truth" matters — deciding *one* place owns each fact (the database) removes a whole class of bugs and cheats. Keeping the access rule in one method (`effective_tier`) means every part of the app agrees on who gets what.

**References / Conversations**
Earlier Claude Code sessions today; architecture notes in `docs/` (commit `8bf705f`); commits `b119038`–`e088f0b`.

---

## 5 June 2026 — Finishing the wireframe layout, a clean rename, and shipping payments

**Type:** Milestone

**TL;DR:**
- Finished the Goal #1 frontend work: a proper **wireframe layout system** and a Help page.
- Settled the app's display name as **ThaiBridge AI** across the whole UI (the GitHub repo/handle stays `thaibridge-ai`).
- Bundled the now-complete **Stripe + PayPal** subscription payments.

**What I built or did**
I traced a startup crash ("unable to open database file") to a missing `instance/` folder and fixed it in one line, then cleaned up four broken CSS rules left from an earlier file move — the real cause of the "all over the place" look. I wrote a **content-first site outline** (the method from my web-design book: plan what each page says before styling it), which set out four page **wireframes** — *Landing*, *3-column content*, *Simple centered*, and *Full-width tool*. I then built the **3-column wireframe** (menu · content · extras) and rolled it out to the Learn, Culture and Buddhism pages using reusable partials (shared page-pieces), made tables fill-or-scroll at any zoom, added an `/instructions` Help page that explains the wireframe system to users, named the app **ThaiBridge AI** consistently across the UI, and shipped the finished Stripe + PayPal checkout.

**Why I did it this way**
I followed the **content-first outline → wireframe** method from my web-design book: decide what each page *does*, then give it the layout shape that fits — rather than forcing one layout on every page. Reusable partials mean editing one file, not fourteen. Using **ThaiBridge AI** as the display name while the GitHub repo/handle stays `thaibridge-ai` mirrors my own display-name-vs-handle approach (Joshua Kay / joshuablakemorekay).

**How We Did It**
Reproduced and fixed the database crash → balanced the broken CSS → wrote the content-first outline and its four wireframes → built shared sidebar/right-column partials and applied the 3-column wireframe page by page → fixed table overflow with a scroll wrapper → wrote the Help page → renamed across ~20 files → installed the missing payment library → committed and pushed.

**What this means for the app**
The learning pages now share one consistent, responsive wireframe, the name is consistent, and paid subscriptions work.

**What I learned**
A wireframe is a *planning* tool, not a feature — and each page wants the shape that fits its job. I also re-learned that a green tick and "200 OK" prove a page *loads*, not that it *looks right* (eight "broken" pages turned out to be working paywalls). And on this machine I must run the app with the project's **virtual-environment Python**, not the global one, or it crashes on a missing library.

**References / Conversations**
This Claude Code session; commit `ac6472a`.

---

## 5 June 2026 — Restructuring the frontend: site outline + shared wireframe (Goal #1)

**Type:** Milestone (in progress)

**TL;DR:** I reorganised the frontend in six small phases on the `rebuild-experiment` branch — but a visual check at the end showed the pages looking "all over the place," so this is a mid-fix checkpoint, not a finished job.

**What I built or did**
Moved the shared CSS and JS out of `base.html` into a new `static/` folder; added an optional wireframe layout (sidebar / main / right column), piloted on the Learn page; realigned the nav to a clean site outline; and added honest About, Contact and Privacy pages plus a "coming soon" login placeholder.

**Why I did it this way**
I followed the method from my web-design book — content-driven outline first, then a shared wireframe — and worked in tiny phases so each change was easy to check and to undo.

**How We Did It**
Tagged a restore point → extracted CSS → extracted JS → added empty wireframe blocks → filled them on one pilot page → realigned the nav → added the footer pages. After every phase I ran the app and the 32 tests, and committed each phase on its own.

**What this means for the app**
The code is much tidier and the structure now matches a real site map — but the layout still needs fixing before it's an improvement a user would actually feel.

**What I learned**
Passing tests and "200 OK" prove a page *loads*, not that it *looks right*. I only caught the mess by opening it in a browser — a reminder to trust my own eyes, not just green ticks.

**References / Conversations**
This Claude Code session; the full plan is saved as "Goal #1." Next step: diagnose the visual issue (likely the cramped Learn wireframe) or revert to the `pre-goal1` tag.

---

## 1 June 2026 — Archiving the verbatim build prompts as a tested library

**Type:** Milestone / Decision

**TL;DR:** I archived the *actual prompts* I used to build the app — word-for-word — into seven themed, automatically-tested folders in the prompt library, and merged them through my first proper pull request.

**What I built or did**
I turned the real build conversation into seven new prompt folders: `frontend-build`, `gamification-system`, `thai-alphabet-exercises`, `romanization-system`, `buddhist-pdf-integration`, `ai-tutor-integration`, and `claude-code-workflow`. Each one holds the verbatim prompt, my reasoning, an executable rubric, and a version history. The `romanization-system` folder documents my custom Paiboon+ vowel set (built on the system used by Benjawan Poomsan Becker, co-developed with my friend Douglas J. Alford, and still in active development).

**Why I did it this way**
My prompt library only held the two market-research prompts. Everything else — how I actually built the app — lived only in chat history, and the journal only *paraphrased* it. I wanted the library to hold my real, word-for-word prompts so it honestly reflects how the app was made.

**How We Did It**
Drafted the reasoning for each folder from my own words → reviewed each one → wrote the files → added a test fixture per prompt so the checks run for free → confirmed all nine prompts pass at 100% → put it through a feature branch and pull request (#1) and squash-merged it.

**What I learned**
A *paraphrased story* (the journal) and the *verbatim prompts* (the archive) are two different things, and both are worth keeping. This was my first real go at the branch-and-pull-request workflow I'd promised myself to adopt — and the green check before merging is exactly the payoff. I also hit two honest gotchas: a GitHub Action can't comment on a PR unless you explicitly grant it permission (it failed with a 403 until I fixed it), and a merge I *thought* had gone through actually hadn't — so I learned to verify a merge really landed before deleting the branch.

**References / Conversations**
This Claude Code session; pull request #1 on the `Thai-App-NEW` repo. Built using the prompt-archivist, commit-message and pr-description skills.

---

## 1 June 2026 — A prompt library, a tidier history, and documenting the codebase

**Type:** Milestone / Decision

**TL;DR:** I added a version-controlled prompt library and build journal to the repo, removed an outdated commit from history, and documented the whole codebase — deliberately using the right Claude tool for each job.

**What I built or did**
I brought a prompt library, an evaluation harness, a CI check and a new README into the repo (20 files), wrote a developer architecture guide from the real code, and cleaned up git history by removing one old, redundant commit.

**Why I did it this way**
I split the work by platform on purpose: **Claude.ai chat** for the human narrative (it can see my conversation transcripts), and **Claude Code** for the codebase docs and the git work (it can read my actual files). Right tool, right job.

**How We Did It**
Backed up the history with a tag → shelved unrelated changes → removed the old commit cleanly → extracted the archive → proved the prompt checks pass → wrote `docs/ARCHITECTURE.md` from the real files → restored a dictionary file I'd deleted by accident.

**What I learned**
Rewriting *published* history needs a backup and a force-push — handle with care. And **don't trust a stray "exit 0"**: my prompt checks looked like they'd passed when they'd actually crashed, until I checked the real exit code.

**References / Conversations**
This Claude Code session; the longer narrative journal was authored via Claude.ai.

---

## March–April 2026 — Researching whether it's worth building

Before building more, I stopped to research the market: who the competitors are, how big the UK audience is, what people would pay, and whether there's a real gap.

**What I learned:** the gap is real — the big apps don't teach Thai at all, and none combine Thai with Buddhist culture. I also learned to *ground* research in real sources and to **check which tools actually ran** — I'd named a web-scraping tool and later found it never fired. (The prompts behind this research are saved in the `/prompts` folder.)

## February 2026 — Version control and a proper workflow

I set up Git (version control — a way to save snapshots of the project) and connected it to GitHub (online backup) one step at a time. Then I started using Claude Code (an AI that edits files in the project directly) for real tasks:

- Built a **user registration system** with a database and a signup form.
- Fixed a bug where empty forms could be submitted (used two safety layers — a browser check and a JavaScript check).
- Cleaned up the signup code and added **32 automatic tests** for the points/levels logic.
- Did a code review and fixed the important issues — including returning the correct error codes and stopping a database error from crashing the app.

**What I learned:** once Git was set up, I could make big changes — and let an AI make them — **without fear, because I could always roll back**. I also learned to give the AI small, specific jobs and review every change before accepting it. When Claude Code ran out of credits, I made two of the fixes by hand and understood what they did — which felt like a turning point.

## February 2026 — Adding Pra Kru Bob's Buddhist writings

I added two of Pra Kru Bob's Buddhist essays as new pages, keeping the wording faithful to the originals.

**What I learned:** my first attempt quietly dropped paragraphs. **Faithful means faithful** — I had to insist on the complete text and check it against the source rather than trust a summary.

## December 2025 — Adding the AI tutor

I connected the app to the Claude API (a way for the app to talk to the AI) to build an in-app tutor with several modes — conversation, grammar help, quizzes, culture, and Buddhism.

**What I learned:** this was the hardest setup. Python wasn't installed; then packages weren't installed; then my secret key vanished because I'd only set it for one terminal session; then it broke because I'd **forgotten the quote marks** around the key in Python. It finally worked once I loaded the key right at the top of the file. Biggest lesson: **don't trust "it works" — including from an AI.** I had to correct the claim that the chat worked when it didn't, and test it myself.

## December 2025 — The romanization display problem

Thai romanization uses accent marks, and one vowel combination (`ɔ̌ɔ`) kept rendering with mismatched letters. I tried several fixes — spacing, fonts, rendering tricks — and most didn't fully work.

**What I learned:** some problems are genuinely deeper than they look (this one is about how computers combine accent characters). I learned **when to stop polishing and pick a pragmatic workaround** rather than chase perfection.

## November 2025 — Building the first version (and debugging it)

I built the first working version: the Flask backend, the Thai alphabet and vocabulary content, lessons, a points-and-levels system, and the page styling.

**What I learned:** most of my early errors weren't broken code — they were **files in the wrong place**. "Template not found" meant a page wasn't in the folder Flask looks in. "name 'app' is not defined" meant I'd tried to *run* a file that was only meant to be *imported* into the main app. And two pages sharing the same web address crashed it. **Reading the error message** usually told me exactly what was wrong.

## November 2025 — Planning the app

I planned the app using a describe-then-check method: I told the AI exactly what I wanted (the format, the approach, how to work with me), then judged what came back and refined it.

**What I learned:** my plan ballooned into a huge, expensive vision. The real progress came from **cutting it down to a small, working version first** (an MVP — the minimum useful version) instead of trying to build everything at once.

---

## Lessons learned (the short version)

- **Where files live matters** — pasting code into a chat isn't the same as putting it in your project.
- **Read the error message** — it usually names the exact problem.
- **Small syntax things break everything** — one missing pair of quotes cost me an hour.
- **Don't trust "it works"** — test it yourself, even when an AI says it's done.
- **Some problems are genuinely hard** — know when to use a workaround.
- **Cut the scope** — a small thing that works beats a big thing that doesn't.
- **Version control is a safety net** — it let me take risks and roll back.
- **Give AI small, specific jobs** — and review every change before accepting it.
- **Two AI products, two bills** — Claude Code is billed separately from the Claude.ai subscription.
