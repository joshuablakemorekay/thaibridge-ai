# Build Journal — ThaiBridge AI

This is the honest record of building **ThaiBridge AI**, my **first web app** — a Thai language and culture learning site — mostly with AI help, as a complete beginner. It's a learning project and a portfolio piece, not a finished product. I've kept the wins and the mistakes in, because the mistakes are where I actually learned.

---

## November 2025 — Planning the app

I planned the app using a describe-then-check method: I told the AI exactly what I wanted (the format, the approach, how to work with me), then judged what came back and refined it.

**What I learned:** my plan ballooned into a huge, expensive vision. The real progress came from **cutting it down to a small, working version first** (an MVP — the minimum useful version) instead of trying to build everything at once.

---

## November 2025 — Building the first version (and debugging it)

I built the first working version: the Flask backend, the Thai alphabet and vocabulary content, lessons, a points-and-levels system, and the page styling.

**What I learned:** most of my early errors weren't broken code — they were **files in the wrong place**. "Template not found" meant a page wasn't in the folder Flask looks in. "name 'app' is not defined" meant I'd tried to *run* a file that was only meant to be *imported* into the main app. And two pages sharing the same web address crashed it. **Reading the error message** usually told me exactly what was wrong.

---

## December 2025 — The romanization display problem

Thai romanization uses accent marks, and one vowel combination (`ɔ̌ɔ`) kept rendering with mismatched letters. I tried several fixes — spacing, fonts, rendering tricks — and most didn't fully work.

**What I learned:** some problems are genuinely deeper than they look (this one is about how computers combine accent characters). I learned **when to stop polishing and pick a pragmatic workaround** rather than chase perfection.

---

## December 2025 — Adding the AI tutor

I connected the app to the Claude API (a way for the app to talk to the AI) to build an in-app tutor with several modes — conversation, grammar help, quizzes, culture, and Buddhism.

**What I learned:** this was the hardest setup. Python wasn't installed; then packages weren't installed; then my secret key vanished because I'd only set it for one terminal session; then it broke because I'd **forgotten the quote marks** around the key in Python. It finally worked once I loaded the key right at the top of the file. Biggest lesson: **don't trust "it works" — including from an AI.** I had to correct the claim that the chat worked when it didn't, and test it myself.

---

## February 2026 — Adding Pra Kru Bob's Buddhist writings

I added two of Pra Kru Bob's Buddhist essays as new pages, keeping the wording faithful to the originals.

**What I learned:** my first attempt quietly dropped paragraphs. **Faithful means faithful** — I had to insist on the complete text and check it against the source rather than trust a summary.

---

## February 2026 — Version control and a proper workflow

I set up Git (version control — a way to save snapshots of the project) and connected it to GitHub (online backup) one step at a time. Then I started using Claude Code (an AI that edits files in the project directly) for real tasks:

- Built a **user registration system** with a database and a signup form.
- Fixed a bug where empty forms could be submitted (used two safety layers — a browser check and a JavaScript check).
- Cleaned up the signup code and added **32 automatic tests** for the points/levels logic.
- Did a code review and fixed the important issues — including returning the correct error codes and stopping a database error from crashing the app.

**What I learned:** once Git was set up, I could make big changes — and let an AI make them — **without fear, because I could always roll back**. I also learned to give the AI small, specific jobs and review every change before accepting it. When Claude Code ran out of credits, I made two of the fixes by hand and understood what they did — which felt like a turning point.

---

## March–April 2026 — Researching whether it's worth building

Before building more, I stopped to research the market: who the competitors are, how big the UK audience is, what people would pay, and whether there's a real gap.

**What I learned:** the gap is real — the big apps don't teach Thai at all, and none combine Thai with Buddhist culture. I also learned to *ground* research in real sources and to **check which tools actually ran** — I'd named a web-scraping tool and later found it never fired. (The prompts behind this research are saved in the `/prompts` folder.)

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

## 7 June 2026 — Making the Dhamma free, keeping the AI Pro

**Type:** Decision / Feature

**What I built or did**
I changed how the subscription tiers work so that the **Theravada Dhamma teachings** and the **meditation timer & techniques** are now completely free for everyone — no account, no subscription, no XP/level, and no "finish the alphabet first" gate. At the same time I kept the **AI Culture & Dhamma Q&A** as a Pro-only feature. I added the four "Coming soon" cards to the pricing page (Personalised Learning Path, Pronunciation Analysis, Listening Exercises, Writing Practice) as greyed-out, non-clickable placeholders, and wrote a short "freely given (dāna)" message on the Dhamma page, the meditation page, and the pricing page to explain the reasoning. While I was in there I also switched the whole app's pricing from dollars to **pounds (£9.99 / £19.99)** — both the displayed prices and the actual Stripe/PayPal charge currency (GBP), so they stay consistent.

**Why I did it this way**
It didn't sit right with me to lock the Buddha's teachings behind a paywall. I value generosity (*dāna*) — the teachings were freely given, so they should be free to read. But the AI features genuinely cost real money every time someone sends a message, so those make sense as a paid product. This gives the app a cleaner, more honest story: **Free** = read and learn everything; **Buddhist Scholar (£9.99)** = practise actively (2× XP, extended content); **Thai Master (£19.99)** = the AI works with you. I changed the charge currency to GBP at the same time so the £ I show isn't a lie about what actually gets billed.

**How it works**
There are two separate systems, and I was careful not to confuse them:
1. **Page access** is controlled by a `SECTION_REQUIREMENTS` dictionary in `app.py`. I changed `theravada` and `meditation` to `tier: 'free'`, `level: 1`, and `requires_alphabet: False`, so the access check always passes.
2. **AI chat modes** are gated separately in the `/api/ai/chat` route by a `FREE_AI_ALLOWED_MODES` set (just `tutor`). The Culture and Dhamma modes (their real internal ids are `cultural` and `buddhist`) were already excluded, so they stay Pro automatically. I left that logic untouched.
I also updated the tier feature lists so Free lists the teachings, Buddhist Scholar no longer does, and Thai Master names the AI Q&A perk — and changed `currency: 'usd'` → `'gbp'` (Stripe) and `"USD"` → `"GBP"` (PayPal).

**What this means for the app**
Anyone can now read the Dhamma and use the meditation timer for free, while the genuinely costly AI tools remain the thing people pay for. The pricing page explains *why*, which makes the offer feel honest rather than stingy, and prices are now shown in pounds to match me being UK-based.

**What I learned**
The big lesson was spotting that "the teachings" and "the AI about the teachings" are two completely different systems — page access vs. AI mode gating. I also learned to verify against the real code instead of trusting my own description: the AI modes were actually called `cultural` and `buddhist`, not `culture` and `dhamma`, and some pieces (the coming-soon cards) already existed. And changing a *displayed* price isn't enough — the billing currency lives separately in the Stripe and PayPal calls, so I had to change both or they'd disagree. I tested everything with Flask's test client before committing.

**References / Conversations**
Built in a Claude Code session on 7 June 2026. Tier/teaching changes committed as `ee1f507` on the `rebuild-experiment` branch; the £ currency switch followed.

---

## 9 June 2026 — Putting ThaiBridge live, with a cost-safe AI link

**Type:** Milestone

**TL;DR:**
- Put ThaiBridge **live on the public internet** for the first time (Render free tier) — a clickable AI demo for my freelance portfolio.
- Made the public AI **cost-safe**: cheap Haiku model on the demo, a hard spend ceiling, and the `changeme` backdoor closed.
- Verified the live AI tutor end-to-end and kept the app warm with a free uptime pinger.

**What I built or did**
I deployed the `rebuild-experiment` branch to Render with a Blueprint (`render.yaml`), a Linux-safe build script and a pinned Python version, then made the repo public. The public demo runs the cheap Haiku model via an `AI_MODEL` environment variable, while local dev still uses Sonnet. I sent a real message to the live tutor, got a proper Thai answer back, and set UptimeRobot to ping the homepage every 5 minutes so it never sleeps.

**Why I did it this way**
A live, clickable AI app is far stronger portfolio proof than a private repo. Haiku plus a small prepaid balance with auto-reload off means the public demo can't run up my card.

**How We Did It**
Checked the app for tracked secrets → wrote the deploy files → smoke-tested the import → pushed and deployed → set a spend limit → switched the public model to Haiku via an env var → tested the live tutor → added the uptime pinger.

**What this means for the app**
ThaiBridge is now a fast, public, cost-protected demo I can put in front of clients.

**What I learned**
When the live app flickered with "no-server" errors, the Render logs showed it was just the free tier waking from sleep — not the memory crash I'd feared. Checking the logs beat guessing from outside. And for a public AI demo, "auto-reload off" is the *protective* setting, even though the dashboard nudges you to turn it on.

**References / Conversations**
This Claude Code session; commits `3ca8fe5` and `72072c4` on `rebuild-experiment`. Live at https://thaibridge-ai.onrender.com.

---

## 9 June 2026 — Protecting the public AI demo's costs

**Type:** Decision / Learning

**TL;DR:**
- Raised the free AI limit from **5 to 15** messages per visitor so clients can properly try the tutor.
- Walled the public demo off with its **own Anthropic workspace key** (kill switch + separate tracking) and a **$7 hard spend cap**.
- Learned my account tier only offers an *org-wide* spend limit, not per-workspace — so I isolated by **key**, not by budget.

**What I built or did**
I gave the public demo its own Anthropic "ThaiBridge Demo" workspace and a dedicated API key, used only on Render, while my laptop keeps its old key. I set a $7 monthly spend cap with an email alert at ~$2, and raised `FREE_AI_DAILY_LIMIT` to 15.

**Why I did it this way**
A public AI link spends my real credits on every message. I wanted a hard ceiling so a bad day can't surprise me with a bill, and the demo isolated so abuse can't touch my own development work.

**How it works**
Three layers: cheap Haiku makes each message a fraction of a penny; the 15/day limit stops one person hogging it; the $7 cap is the wall nothing crosses. The separate key lets me revoke just the demo if it's abused, without breaking local dev.

**What I learned**
I assumed I could cap one workspace's spending — but on my tier, Anthropic only offers an *org-wide* spend limit; per-workspace limits are higher-tier. So I isolated by **key** (a kill switch and clean tracking) rather than by budget. And "free" messages aren't free to *me*: every message spends my credits — the limit caps the *count*, not the charge.

**References / Conversations**
This Claude Code session; message-limit change in commit `908cee8`. Workspace `ThaiBridge Demo`; live demo at https://thaibridge-ai.onrender.com.

---

## 10 June 2026 — Making ThaiBridge fit every phone and laptop

**Type:** Bug Fix / Learning

**TL;DR:**
- Made the whole app **responsive** — one link now adapts from a 320px phone to a desktop, so I don't need a separate mobile version.
- Fixed a sneaky **CSS specificity bug** that stopped sidebar pages collapsing to a single column on phones.
- Switched headings and the logo to **fluid sizing** and tidied the AI Tutor page on mobile.

**What I built or did**
On my iPhone, the sidebar pages were crushing content into a one-word-per-line strip, and the AI Tutor (chat) page had an oversized header plus tooltips poking off the screen. I made the layouts collapse to one column on phones, set the headings, logo and chat header to scale with screen width, and capped or hid the stray tooltips.

**Why I did it this way**
One responsive codebase beats a separate mobile app — half the upkeep and the two can't drift apart. Fluid `clamp()` sizing (a CSS rule that scales a value smoothly between a minimum and maximum) covers every screen width continuously instead of patching one phone size at a time.

**How We Did It**
Reproduced the breakage in a real browser at iPhone width → traced it to a CSS specificity clash → matched the mobile rules' specificity so they win → added fluid headings → shrank the chat header → ran an overflow audit across seven widths → fixed the last off-screen tooltips → confirmed zero sideways scroll on every page, with desktop unchanged.

**What this means for the app**
The whole site is now tidy and usable on any phone, tablet or laptop from the same link — much stronger when I show it to clients on a phone.

**What I learned**
CSS media queries add no specificity, so a more specific desktop rule beats a mobile one no matter the screen size — exactly why the layout refused to collapse. And measuring overflow across several real widths catches bugs that checking a single phone size hides completely.

**References / Conversations**
This Claude Code session; sidebar fix committed as `7d90ea0` on `rebuild-experiment`. Live at https://thaibridge-ai.smoald.com.

---

## 10 June 2026 — The rebuild experiment worked: merging it into `main`

**Type:** Milestone

**What I did**
**I merged my `rebuild-experiment` branch (a separate copy of the project I'd been working on safely) into `main`.** It had grown to 44 commits ahead — all the big recent work: real login, Stripe billing in £, the free/Pro AI tiers, the live deployment setup, and mobile fixes.

**Why**
The branch started as a sandbox to try a bigger redesign without risking the original. It's proven itself now, so it's earned its place as the main version.

**How it worked**
Because `main` had nothing new of its own, git did a clean **fast-forward** (it just slid `main` up to match the rebuild) — no conflicts. I checked afterwards: `main` now matches the rebuild exactly, at commit `31696b0`.

**What it means for the app**
`main` is the real, current version again. **The live site didn't change** — it still deploys from `rebuild-experiment`, so this was purely tidying up behind the scenes.

**What I learned**
Merging a long-running branch isn't scary when the target hasn't moved — it's a clean fast-forward. And "merge to main" and "what the server deploys" are two separate switches; I only flipped one.

---

## 10 June 2026 — Polishing the README into a case study and tidying the journal

**Type:** Documentation / Learning

**TL;DR:**
- Rebuilt the README as a portfolio case study, keeping the screenshots, badges and run steps.
- Reordered the whole journal into newest-first order without changing a word.
- Caught myself verifying against a stale local copy — a real lesson in checking the right source.

**What I built or did**
I reworked the README around a case-study narrative (problem, approach, proof) while keeping the screenshots, badges and run-it-locally steps a repo needs. I reordered JOURNAL.md into newest-first order and rebranded both files to ThaiBridge AI.

**Why I did it this way**
A case study tells recruiters a stronger story than a plain description, but a README must still show the app and how to run it — so I kept both. I reordered the journal rather than rewriting it, so no honest history was lost.

**How We Did It**
Compared the two READMEs → verified every number against the code → found my local `main` was 47 commits behind and re-verified against the real code → assembled the case study → reordered the journal with a script → proved the content was identical → renamed throughout.

**What this means for the app**
The repo now reads as a polished, honest portfolio piece: strong narrative, real screenshots, verified numbers, and a clean chronological build story.

**What I learned**
Check you're reading the live code, not a stale copy — I "corrected" right numbers into wrong ones until I synced. And reordering beats rewriting: you can tidy a journal without losing the honest record.

**References / Conversations**
This Claude Code session; PRs #3–#7.

---

## 8 July 2026 — Bringing the custom domain back online

**Type:** Bug Fix / Milestone

**TL;DR:**
- The branded link `thaibridge-ai.smoald.com` had stopped loading ("can't reach this page").
- The real cause wasn't the app — the subdomain had gone missing when `smoald.com` moved from Namecheap to Cloudflare.
- Rebuilt the DNS record on Cloudflare, re-added the custom domain in Render, and verified it live with a valid HTTPS padlock.

**What I built or did**
The pretty address for the app — `https://thaibridge-ai.smoald.com` — had stopped working. I traced it and found the subdomain simply didn't exist in DNS any more: when I moved `smoald.com` onto Cloudflare, the old subdomain record hadn't come across. I added a fresh record on Cloudflare (a CNAME pointing `thaibridge-ai` → `thaibridge-ai.onrender.com`), set to "DNS-only" so Render could still handle its own certificate, then re-added the custom domain inside Render. I also set the repo's Website link to the branded domain.

**Why I did it this way**
The app itself was never broken — only the address in front of it. So the fix belonged in DNS and hosting settings, not the code. Keeping the app on Render (which runs Flask apps as-is) and using Cloudflare only for the address gives the best of both: no rewrite, plus a professional `smoald.com` link.

**How it works**
A CNAME record is a signpost: it tells the internet "`thaibridge-ai.smoald.com` actually lives at `thaibridge-ai.onrender.com`." Render sees the matching custom domain on its side, issues a free HTTPS certificate, and serves the app. The old `onrender.com` address still works underneath as a fallback.

**What this means for the app**
The app is reachable again at a clean, branded address I can put on my CV and portfolio — with a valid HTTPS padlock. The link is permanent; it doesn't expire or need replacing.

**What I learned**
When a "site is down," it isn't always the app — this was pure DNS. I also learned that moving a domain between providers can silently drop subdomain records, so they need re-creating. And a small but important detail: with Cloudflare in front of Render, the DNS record must be "DNS-only" (grey cloud), or Render can't finish its certificate check.

**References / Conversations**
This Claude Code session.

---

## 16 July 2026 — Monk Mode: a free lesson track for monastics, plus a redesign start

**Type:** Feature

**TL;DR**
- Built **Monk Mode** — a free, code-gated lesson track for Buddhist monks, learnable both ways (Thai monks learning English, Western monks learning Thai).
- Drafted 10 monk-specific topics (140 items) — still to be reviewed.
- Started fixing the "boring long scroll" by rolling out the app's existing click-to-open sections.

**What I built or did**
Monk Mode: enter an access code to unlock a dedicated track of monastic lessons (alms round, precepts, daily routine…), each switchable between learning Thai and learning English with the right pronunciation help. I also turned several long pages (Theravada, Meditation, Gender) into collapsible sections. All on a safe `rebuild-experiment` branch (a separate copy to work on) — the live site was never touched.

**Why I did it this way**
One app, not two — the lessons already hold both languages, so a second app would just double the upkeep. I gated only the free *unlock* with a code, keeping the direction switch open to everyone. Paid value stays in the AI tutor, so giving content away doesn't dent revenue.

**How it works**
Monk lessons live as plain JSON files, one per topic, loaded when the app starts. A session setting holds the direction, and a small check lets Monk Mode skip the paywall. The redesign reuses an accordion the app *already had* — just applied to more pages.

**What this means for the app**
Monks and the wider community get genuinely useful, free lessons, and the long pages are far easier to navigate.

**What I learned**
Check what already exists before building — the accordion was already there, and I nearly wrote a second one. I also left the English side leaning on IPA, which I already suspected was wrong for the reader but couldn't yet say what should replace it. **Naming a weak spot is worth doing even when you can't fix it yet** — it's what I came back to on the 20th.

**How We Did It**
1. Untangled two duplicate local copies and picked one clean folder.
2. Made a safe branch so the live site was never at risk.
3. Built Monk Mode in phases: free unlock → access-code gate → content track + direction switch.
4. Wrote and checked 10 lesson topics against the app's own romanization.
5. Found the app already had collapsible sections, and rolled them out to the long pages.
6. Committed and pushed each verified step.

**References / Conversations**
Claude Code session, 15–16 July 2026.

---

## 18 July 2026 — Access model rework + Instant Access Pass, and Monk Mode goes live

**Type:** Milestone

**TL;DR**
- Reworked who pays for what: only the **Alphabet + Buddhism** section is free now; everything else needs a subscription *and* levelling up.
- Built the **Instant Access Pass** — an optional one-time £9.99 add-on that unlocks everything instantly.
- Tested it all and **went live** — Monk Mode and the new model are on the real site.

**What I built or did**
I shrank the free tier to just the alphabet and the Buddhism section, put the rest behind Basic (Buddhist Scholar) and Pro (Thai Master), and made Monk Mode waive only the payment — monks still level up. I added tier-name brackets (Free/Basic/Pro), gated two pages that were slipping through for free (Tour Guide, Business Thai), and built the Instant Access Pass: a one-time purchase that skips the level-and-alphabet grind.

**Why I did it this way**
I want the app to stay a fun learning challenge, so paying removes the paywall but never the levelling. The Pass is for people who'd rather skip the grind — an optional extra, not the default.

**How it works**
One access check runs three gates in order: alphabet, level, then payment. Monk Mode skips the payment gate; the Pass skips the alphabet and level gates. The Pass is a database flag set by a one-time Stripe payment, with a self-healing migration (adds any missing columns on startup).

**What this means for the app**
A clear, honest paid model with a generous free core — and Monk Mode, built two days earlier, is now reachable by real monks rather than sitting on a branch. Today was about *access*: the lessons themselves didn't change.

**What I learned**
Testing caught what I couldn't see: two pages were free by accident, the pricing page still advertised now-paid content, and my local database was quietly missing columns. **The gate can be right while the label lies.** And going live taught me a hosting gotcha: a Blueprint-managed host treats its config file as the source of truth, so a variable added only in the dashboard gets wiped on the next deploy — the fix is to declare it in the config.

**How We Did It**
1. Tested the existing Monk Mode in the browser; fixed a see-through-navbar bug.
2. Set real Monk Mode access codes and stored them safely on the host.
3. Reworked the access rules: free = Alphabet + Buddhism, rest paid, Monk Mode free-but-still-levels.
4. Closed loose ends testing surfaced: ungated pages, stale pricing copy, a misleading progress page.
5. Added tier brackets and built the Instant Access Pass add-on end to end.
6. Verified with test scripts and a real Stripe test call, then merged to `main` and went live.
7. Hit a deploy gotcha — the host kept wiping the Monk Mode codes — and fixed it by declaring them in the Blueprint config so they persist.

**References / Conversations**
Built across a single Claude Code session (18 July 2026).

---

## 19 July 2026 — Tones & Consonant Classes: built, consolidated, and gated

**Type:** Feature

**TL;DR**
- Built one section teaching consonant classes and tone rules together — because classes only exist to work out tones.
- Reused my existing quiz/XP scoring for four practice drills — no new system invented.
- Explored first and merged scattered content, folded in the old Grammar version, then gated the page behind the Basic tier (same as Grammar) and shipped it live.

**What I built or did**
A new "Tones & Consonant Classes" section: one data set, a `/tones-classes` page with reference tabs, and four progressive drills — class ID, tone calculation, contrast pairs, and the leading-ห rule. I started it on a feature branch (a separate copy of the project to work on safely), then consolidated: I moved the old "3-Tier Consonant Class System" out of the paid Grammar Guide into this one section (leaving a pointer link behind), added a same-sound consonant-pairs table and a "How to master this" study block, and added a Help-page note about learning tones early. Finally I put the whole page behind the Basic tier — the same paywall Grammar had.

**Why I did it this way**
Classes and tones belong together — you learn classes only to predict tones, so teaching them in two places was confusing. My tone content was scattered across three places, so I merged the best of it into one page. I first built it free, but since it now holds content that used to be paid (the Grammar consonant-class system), I gated it the same way as Grammar so I'm not giving away paid material.

**How it works**
The page reads from a single data dictionary. The drills send answers to my existing `/api/check_answer` endpoint, so points and levelling stay consistent. Access is gated like Grammar: **Basic tier, level 3, alphabet completed first**.

**How We Did It**
1. Searched `app.py`, data and templates for existing tone/class content.
2. Recommended merge vs rebuild, then waited for my approval.
3. Built the data, route, template and menu links, with four drills.
4. Merged the old Grammar consonant-class content in and removed the duplicate (left a pointer link).
5. Gated the page behind the Basic tier, then merged to `main` — it's now live.

**What this means for the app**
One clear place to learn tones and consonant classes, sitting properly inside the paid learning track instead of being duplicated across two pages.

**What I learned**
Exploring before editing paid off — I found content I'd otherwise have duplicated. And access level is a real decision: moving paid content into a "free" section quietly gives it away, so consolidation and pricing have to be thought through together.

**References / Conversations**
This Claude Code session; prompt archived under `prompts/tones-consonant-classes/`. Merged to `main` and live at https://thaibridge-ai.smoald.com/tones-classes.

---

## 19 July 2026 — Making developer login work on the live site

**Type:** Fix / Learning

**TL;DR**
- Fixed developer-mode login on the live site — it kept rejecting my password.
- Cause: Render had generated a *random* production password; my own one only worked locally.
- Switched the setup so a known, dashboard-set password works everywhere.

**What I built or did**
Got developer mode working on the live site. In `render.yaml` I switched `DEVELOPER_PASSWORD` from `generateValue: true` to `sync: false`, set my chosen password in the Render dashboard, and redeployed. Now the same password logs me in on the live site.

**Why I did it this way**
`generateValue: true` told Render to invent a random password, so login always failed there — while it worked locally because the app reads my `.env` file. `sync: false` (the same pattern I already use for Monk Mode codes) lets me set a known value in the dashboard that survives redeploys, without ever putting the secret in the public repo.

**How it works**
The app reads `DEVELOPER_PASSWORD` from the environment — locally from `.env`, and on the live site now from the Render dashboard value. Developer mode bypasses the paywall, so I can test gated sections like Tones & Consonant Classes.

**What this means for the app**
I can finally log into developer mode on the live site to check gated content — something I couldn't do before.

**What I learned**
Two things. First, "not updated in PyCharm" was a red herring — the code was fine; I was just hitting the new paywall (the gate doing its job). Second, order matters: set the dashboard value *before* switching to `sync: false`, or the live password briefly falls back to a guessable `"changeme"`.

**References / Conversations**
This Claude Code session. Live at https://thaibridge-ai.smoald.com.

---

## 20 July 2026 — A pronunciation system for Thai monks learning English

**Type:** Feature

**TL;DR**
- Gave the English side of Monk Mode a proper pronunciation system: **native audio**, a plain respelling, a tip written in Thai, and optional IPA.
- Left the Western-monk side (learning Thai) exactly as it was, and checked all ten topics to be sure the two directions don't bleed into each other.
- **Merged and live.** The 140 Thai tips and the Pāli audio are mine to review next — shipped honestly, not perfectly.

**What I built or did**
Monk Mode serves two readers from one set of lesson files: **Western monks learning Thai**, and **Thai monks learning English**. The Thai-learning side was already in good shape. The English-learning side was the weak half: the only pronunciation help was IPA — symbols most learners can't read — sitting beside Paiboon and English notes that were written for the *other* reader.

I replaced that with four things working together, across all 140 items in 10 topics: **native audio** on every word, a respelling (CAPITALS mark the stressed syllable), a tip in Thai, and IPA behind a toggle. Audio is the anchor — hearing a word beats any way of writing it down — and the rest are memory aids for when the sound has faded.

**Why I did it this way**
Paiboon exists to write *Thai* sounds and has no symbols for th, v, z or sh — the exact distinctions an English learner needs. It's the right tool for the Western monk and the wrong one for the Thai monk, so the app got its own system for English rather than stretching one never built for it.

The audio is generated once on my machine and the MP3 files are committed — 138 of them, 1.5 MB. The live site just serves them as ordinary files. That means no speech service to pay for per play, no API key to keep safe on the host, and if the tool I used to make them ever disappears, the website doesn't notice.

**How it works**
Sounds Thai already has are anchored to Thai script (`ai` = ไ). Sounds Thai lacks get mouth instructions instead, because no script can carry them. Each direction shows only what its reader needs. A play button appears next to a word only when its audio file actually exists, so a half-finished topic looks tidy rather than broken.

**What this means for the app**
Thai monks can now *hear* the English they're learning, not just read a description of it — and Western monks learning Thai get the same experience as before, untouched.

**What I learned**
My first attempt at the respelling was circular — explaining English with roman letters to someone whose main reference for roman letters *is* English. And I'd written the tips in English, for people learning English. Both only surfaced by testing properly and pushing back.

Three more, all the same shape — **the code was right and the thing in front of me was lying**:
- I saw the IPA had a "hidden" tag and called it fixed, but a CSS rule was quietly overriding it. **Test what the user sees, not what the code says.**
- Two audio files "failed" to generate. They hadn't — the *success message* had crashed, because a Windows console can't print the ā in "nibbāna", and the error handler then deleted the perfectly good file it had just made. **Only let the risky step count as a failure.**
- A `NameError` sent me hunting through correct code. An old copy of the app was still running from earlier and serving the previous version. **Check what's actually running before you debug what's written.**

**How We Did It**
1. Read the existing Monk Mode code to see what was already there.
2. Designed a respelling system, then scrapped the first version when it didn't hold up.
3. Rewrote the tips in Thai and gave them one clear job.
4. Piloted on one topic, checked it in a real browser, then rolled out to all ten.
5. Built a guide page teaching both notations.
6. Generated native audio for all 140 entries and added a play button to each.
7. Put the filename rule in one shared file, so the script that *writes* the audio and the page that *links* to it can never drift apart and quietly 404.
8. Checked all 140 entries in both directions, then merged to `main` and went live.

**References / Conversations**
Claude Code sessions, 20 July 2026. Built on branch `feature/monk-english-pronunciation`, merged to `main` and deployed.

---

## 20 July 2026 (later) — Two accents for the monk English track

**Type:** Feature + Bug Fix

**TL;DR**
- A friend who teaches Thai questioned the Ls and Rs in the respellings — that one question became a full **British/American accent toggle**.
- Fixed 15 tips that were teaching the *Thai* rolled ร for the English R, plus a British word (`aeroplane`) that had been carrying the American pronunciation all along.
- All merged and live. The new Thai wording still needs a native speaker's review.

**What I built or did**
Thai monks learning English can now choose 🇬🇧 or 🇺🇸, and the whole lesson follows: the word (aeroplane/airplane, practise/practice), the respelling (MAW-ning/MOR-ning), and the voice — 138 audio files per accent. I also rewrote 21 tips so they teach the L sounds Thai speakers actually struggle with (final L becoming น, so "bowl" turns into "bone") and say honestly which accent pronounces an R.

**Why I did it this way**
Only 14 entries store a US spelling override — everything else is identical in both accents, so most of the system stays single-valued and easy to review. British stayed the default because all the existing audio and IPA were built to it.

**How it works**
The toggle is a session setting (remembered per visitor), mirroring the existing direction switch. Audio lives in per-accent folders sharing one filename rule, so one voice can never overwrite the other.

**How We Did It**
1. Audited all 140 entries with a script before forming an opinion — the "44 broken entries" I first estimated turned out to be 14.
2. Fixed the rolled-ร bug first, on its own branch, because it was live and needed no decisions.
3. Scaffolded the toggle (state, routes, audio folders), then content (respellings, tips), then the words themselves — each phase committed and verified separately.
4. Merged each branch into `main` (a saved snapshot going live) and deleted it, keeping one clean trunk.

**What I learned**
I initially rewrote the wrong layer — the Thai tip boxes instead of the respelling system — because I treated a question as an instruction. And my friend's "wrong" suggestion (AALMZ) pointed at a real design gap even though the specific fix wasn't right. **Listen to the question behind the question.**

**References / Conversations**
Claude Code session, 20 July 2026. Known gap logged: the pronunciation guide page has no accent section yet and its British-only footnote is now stale.

---

## 20 July 2026 (evening) — My Thai teacher's homework becomes lessons 11 and 12

**Type:** Feature

**TL;DR**
- My Thai teacher gave me real classroom material: a tongue twister for the **L sound**, fifteen drill sentences for the **R sound**, and three Ajahn Sumedho passages for learning Dhamma-teaching vocabulary in context.
- It became two new Monk Mode lessons: **11 — Pronunciation Practice: L and R** and **12 — Dhamma Reading: Ajahn Sumedho**, with audio in both accents.
- The teacher's own idea — "you can get AI to read the text in American or British English" — was something the app could already do, because of the accent toggle built earlier today.

**What I built or did**
Lesson 11 tackles the classic problem: Thai speakers often turn R into L, so *rice* becomes *lice*. It starts with nine minimal-pair words (rice/lice, right/light, and the flea/fly/flee/flaw/flue family — each with Thai meaning, respelling and audio), then two drill sections: the "flea and a fly in a flue" twister line by line for L, and the fifteen R sentences, every line with a respelling, hidden IPA, a Thai gloss of what it means, and a play button.

Lesson 12 holds the three Ajahn Sumedho readings — *Observing Our Reactions*, *Grasping and Suffering*, *The Body Breathes* — each with a **listen-to-the-whole-passage** button in either accent, plus twelve key teaching words (refuge, grasping, aversion, conditioning…) and four sentences worth memorising, all in the existing lesson format with Pāli where it applies.

**Why I did it this way**
The lesson files only knew about single words and short phrases, and neither a tongue twister nor a 250-word reading fits that shape. Rather than force them in, I added two new optional sections to the lesson format: `drill_sections` (English-only lines — there is no Thai prompt side because the whole point is saying the English sound) and `passages` (whole readings). Every drill line still carries a Thai meaning, because a tongue twister you understand is far easier to remember than nonsense.

The passages are from a free-distribution Dhamma book, so they sit in the free Monk Mode section with the source credited on every passage — teaching material passed on the way it was meant to be.

**How it works**
The audio script now collects drill lines like any other entry, and passages get a special key: the file is named after the passage's id (`passage-the-body-breathes.mp3`), never a slug of its 200-word text. The template asks for exactly the same key, so the two sides can't drift apart — the same one-rule-shared-in-one-place idea the audio system was built on. About 47 new MP3 files per accent, generated once on my machine, served as plain static files.

**How We Did It**
1. Read the teacher's material carefully first — including the correction that the flea/fly twister trains **L**, and the R sentences train **R**.
2. Explored how the ten existing lessons, the templates and the audio pipeline worked before writing anything.
3. Drafted both JSON lesson files, then extended the lesson template, the topic-grid counts, the CSS and the audio script.
4. Smoke-tested both pages in both learning directions, ran the full test suite (32 passing), then generated the audio in both accents.

**What I learned**
Content from a real teacher beats content I'd invent — the material arrived with its own pedagogy (minimal pairs → twisters → drills → reading in context) and my job was to give it a home, not improve it. And building infrastructure honestly pays off later: the accent toggle from this morning meant the teacher's "read it in British or American" wish cost nothing extra.

**References / Conversations**
Claude Code session, 20 July 2026 (evening). Material from my Thai teacher; passages from Ajahn Sumedho, *Direct Realization* (Anthology Vol. 3), Amaravati — free distribution. All Thai glosses and Paiboon in the two new files are mine to verify next.

---

## 20 July 2026 (night) — My teacher reviews the lessons, and her feedback becomes features

**Type:** Feature + Fix

**TL;DR**
- My Thai teacher reviewed the pronunciation lessons and gave four specific pieces of feedback — each one became something in the app.
- Her sharpest point: a word pronounced perfectly on its own gets mispronounced again once it sits inside a sentence. That changed the **structure** of every pronunciation lesson, not just the content.
- I'd only applied her V/F/TH feedback to the new lesson. Being asked whether it had reached the older ones turned up 15 entries with the same gap.

**What I built or did**
A new **lesson 13 — Pronunciation Practice: V, F and TH**, covering the sounds she named: V collapsing into W, a final F becoming P, and TH (which doesn't exist in Thai at all) landing as T, D or S. Both pronunciation lessons now end with a **"From word to sentence"** section — the same sounds embedded in real sentences, as the test of whether a sound is truly learned. Lesson 12 gained a **reading guide** (pause at the comma, stop at the full stop, then read again with vocal variety) and a **"one idea, several words"** block — *stress* as well as *suffering*, *uncertainty* as well as *impermanence*. 134 new audio files, both accents.

**Why I did it this way**
She made the case that reading a short Dhamma text out loud does more than drilling word lists: it exposes the same stumbles every time, and it teaches punctuation as meaning rather than decoration. So I built what she described rather than inventing my own version of it.

**How it works**
Two new optional blocks in the lesson format (`reading_guide` and `word_choices`), rendered by the template and picked up by the audio generator, so an alternative wording is never a silent one. I also wrote `scripts/make_review_sheet.py`, which diffs the lesson files against an older commit (compares them to see what changed) and produces a printable Thai review sheet — so she only ever gets asked about material she hasn't already corrected.

**How We Did It**
1. Read her feedback carefully and mapped each of the four points to a concrete change before writing anything.
2. Built lesson 13, the sentence-transfer drills, the reading guide and the word-choice block; generated audio in both accents.
3. Asked whether the fix had reached the *existing* lessons — it hadn't. Audited all 140 entries in lessons 01–10.
4. Found TH already covered (14 of 14) but **V and F missing in 15 entries** — plus a real bug where one phrase's respelling stopped halfway through the sentence.
5. Regenerated the review sheet so the corrected tips reach her too.

**What I learned**
**A fix isn't finished until it's applied everywhere the problem exists.** I built the lesson named after the problem and called it done — but the same sounds appear in `food`, `faith`, `mindfulness` and every `venerable` across the older lessons. "Did you apply it to the others?" was the most useful question of the session. Also a practical one: rewriting JSON with `json.dump` reformatted every file and turned a 15-line change into 1,119 lines. I reverted and edited the raw text instead — **matching a file's existing layout matters as much as getting its content right.**

**References / Conversations**
Claude Code session, 20 July 2026 (night). Feedback from my Thai teacher. All new Thai is AI-drafted and awaiting her review — that's what the generated sheet is for.

---

## 20 July 2026 (late) — Where the "freely given" line actually falls

**Type:** Decision

**TL;DR**
- Moved the **Meditation page** from free to **Buddhist Scholar (£9.99)**.
- The principle didn't change — the Dhamma is still freely given — but the *line* moved: **the teaching is free, the tooling built on top of it is the product.**
- Updated all seven places that said otherwise, including the pricing page, both *dāna* notices, and my portfolio case study.

**What I built or did**
Changed `meditation` from `tier: 'free'` to `tier: 'basic'` and took it out of the sections a brand-new account starts with. Then swept everywhere that advertised it as free: the Free plan's feature list, the pricing page's "why some things are free" panel, the banner on the meditation page itself, the banner on the Theravada page, the architecture doc's tier table (which was badly out of date anyway — still in dollars, still claiming vocab and grammar were free), and the values paragraph in both my README and my portfolio case study.

**Why I did it this way**
I asked for a second opinion before touching anything, and the pushback was useful: don't gate it, it's weak paywall material, it's a values reversal, and it's advertised as free. Two of those dissolved once I said out loud that **I have no users yet** — nothing is being taken from anyone, and this is still design, not a broken promise. What survived was the values question, and thinking it through is what produced the better line. "Meditation is free but Thai grammar isn't" was never a principle, just where I happened to stop. **"The teaching is free, the tools are paid"** is a rule I can state in one sentence and defend to anyone.

**How it works**
`SECTION_REQUIREMENTS` in `app.py` drives every gate, so the actual change is one word. Monk Mode waives the tier gate, so **monastics still get everything free** — I made both *dāna* notices say so explicitly, with a link.

**What this means for the app**
The free tier is now a cleaner offer: the full Thai alphabet plus all the Dhamma teachings and articles, forever, no account needed. Everything built *on top* of that — guided practice, language study, AI — is the paid product.

**What I learned**
**Working out where a values line falls is harder than declaring one.** I'd made the call once and assumed it was settled, but "free" wasn't a principle until I could say *why* those things and not others. Also: when a decision reverses, the honest move is to make the change the story rather than quietly delete the old one — the case study now reads as judgment developing, which is truer and more interesting than pretending I got it right first time. And a small practical thing: **a one-word gate change had seven downstream places to fix.** Grepping for every mention before editing anything is what stopped the pricing page contradicting the app.

**References / Conversations**
Claude Code session, 20 July 2026 (late). Verified with a test across all four user types — free (locked), Basic, Pro, and Monk Mode (all open) — plus the full 32-test suite.

---

## 22 July 2026 — The Alphabet page that was never broken

**Type:** Feature + Bug Fix + Learning

**TL;DR**
- Rebuilt the **Thai Alphabet page from scratch** — a 44-letter chart, flashcards and a 44-question quiz, all with Thai audio. It's free, and passing it (35/44) unlocks the rest of the site.
- The "won't open on my iPhone" bug **was never the Alphabet page**. It was three lines of CSS in the shared layout that stacked a 644px sidebar on top of the page content on phones.
- I rebuilt the same page twice before I thought to ask the phone what was actually happening.

**What I built or did**
A new Alphabet page with three study modes — a chart of all 44 consonants grouped by class, flashcards, and a quiz — plus 44 Thai audio recordings generated with edge-tts. Passing the quiz stores completion on the user's database row and unlocks 20 other sections. Then I found and fixed the real bug: on a phone the layout collapsed to one column but stacked in source order, putting the sidebar first.

**Why I did it this way**
The alphabet is the prerequisite for everything else, so it had to be **free** — charging for it would put the whole site behind the paywall with no way in. Completion had to live in the database, not a cookie, or clearing cookies would re-lock the entire site for someone who'd already earned their way in.

**How it works**
`order` on the mobile breakpoint moves `<main>` above the sidebar visually while leaving the HTML order alone, so screen readers still get nav-then-content:

```css
.layout > main { order: -1; }
.layout-sidebar { order: 1; }
```

**How We Did It**
1. Deleted 20 commits from GitHub and force-pushed — which silently took an old iOS fix with them.
2. Built a new Alphabet page. Still "wouldn't open" on the iPhone.
3. Deleted it entirely and purged it from git history, to rebuild from nothing.
4. Rebuilt it again from scratch. **Same symptom.**
5. Checked the backend and frontend properly — both clean, no errors.
6. Added a temporary beacon so the phone could report back.
7. The phone said the page loaded **perfectly, six times, all 44 letters**. That killed the whole theory.
8. Measured the layout at 390px: the heading was 1.4 screens down, the first letter 2.6 screens down.
9. Three lines of CSS. Fixed.

**What this means for the app**
Every page with a sidebar is now usable on a phone, not just this one.

**What I learned**
**When a rebuilt-from-scratch component fails identically, stop rebuilding it.** Two identical failures were telling me the cause was somewhere else, and I didn't listen. The fix that mattered took twenty minutes once I stopped guessing and made the broken device report what it was actually doing — measuring beats theorising, and I should have reached for it far sooner.

**References / Conversations**
Claude Code session, 22 July 2026. Confirmed working on iPhone (iOS 18.7 / Safari 26.5.2). Full 32-test suite passing.

---

## 23 July 2026 — Giving the app a voice, and a conversation partner

**Type:** Feature + Bug Fix + Learning

**TL;DR**
- Built a **reusable Thai audio system** — tap any Thai word to hear a native voice — and shipped it on the Vowels and Sentences pages.
- Turned the Sentences page into a **fluency tool**: practice mode, expanded conversations (including Dharma dialogues), everyday phrases, and an **AI roleplay partner**.
- Announced two deploys as "live" before the server actually had them. Learned to check the live server first, every time.

**What I built or did**
A shared audio helper (`thai_audio.py`) plus one page-wide player, so any page can get 🔊 buttons cheaply. Then a three-phase upgrade to the Sentences page: line-by-line audio + a hide-and-reveal practice mode; five new conversations (taxi, market, and three temple/monastic ones) and an "everyday phrases" section; and a roleplay mode where the AI plays a waiter, vendor or taxi driver and stays in character. Also fixed a real bug — the AI's default model had been retired and was returning a 404 for local dev.

**Why I did it this way**
Fluency comes from hearing and speaking, not reading, so the audio and practice mode matter more than more content. Audio is pre-generated once and served as files — free, and it sounds identical on every device.

**How We Did It**
1. Built the reusable audio core and proved it on the Vowels page.
2. Rolled audio onto Sentences, then added practice mode.
3. Wrote new conversations + phrases; had the Dharma ones checked before shipping.
4. Added AI roleplay scenarios to the existing chat tutor.
5. Dropped the "talk to a monk" roleplay — the cheap live model wouldn't hold monastic register.
6. Found and fixed the retired-model 404.

**What I learned**
**A push is not a deploy.** I told myself it was live twice before the server caught up — now I confirm on the real URL before saying the word. And an AI is only as good as the model behind it: the cheap live model couldn't be trusted with a monk's speech, so that scenario waited.

---

## 24 July 2026 — Everything can be heard, and read & written

**Type:** Feature + Bug Fix + Learning

**TL;DR**
- Built a new **Read & Write Thai Script** section — sound-out-the-syllable reading, a trace-the-letter writing canvas, and a tappable Jataka-tale reader.
- Rolled tap-to-hear audio across **every remaining page** — all 13 Learn pages plus Culture, Theravada and Meditation. The whole app can now be heard.
- Extracted the audio wiring into a reusable partial partway through, which made the last pages near-instant.

**What I built or did**
First, a two-part "Read & Write" page: a reading trainer that teaches how Thai vowels sit before/above/below/around a consonant, and a canvas to trace all 42 written letters by hand, capped with a short Jataka story you read one tapped word at a time. Then the big push — tap-to-hear 🔊 buttons on every page that holds learnable Thai, ~500 native-voice clips in one consistent system. Also fixed a live bug on the Formality page: examples were showing as raw code (`{'thai': ...}`) to real users.

**Why I did it this way**
Reading and writing are the two skills the app never taught directly, and hearing a word matters more than reading its romanisation. One shared audio helper meant each new page cost almost nothing.

**How We Did It**
1. Built the Read & Write section (data file, reading trainer, trace canvas, Jataka reader) and shipped it.
2. Added audio page by page: check if the Thai is structured data or hidden in prose, wire it, generate clips, verify on the *live* server.
3. Hit a wall on the big Grammar page (~190 phrases) — switched from hand-editing to a map-plus-script that auto-tags every Thai cell.
4. Pulled that pattern into a reusable partial, so the final pages were a one-line include.
5. Marked all draft Thai and unverified audio for the teacher's review.

**What I learned**
When a job repeats, stop and build the tool — the reusable partial turned a slog into a stamp. And check the rendered page, not just the data: the Formality bug was invisible until I actually looked at what users saw.

---

## 24 July 2026 — Learning Support: an accessibility panel for every page

**Type:** Feature

**TL;DR:** I added a site-wide "Learning Support" menu so learners can switch on an easy-to-read font, bigger text, extra spacing, reduced motion, or read-aloud — all saved in their own browser, no login needed.

**What I built or did**
A dropdown in the top menu with toggles for a dyslexia-friendly font (Atkinson Hyperlegible), bigger text, extra letter/line spacing, reduce motion & distractions, and a 🔊 Read aloud button. It carries a note saying who it helps — dyslexia, ADHD, autism, low vision, or reading fatigue.

**Why I did it this way**
I kept it purely front-end so it never touches login or payments. Because different people need different help, I used separate toggles instead of one on/off switch.

**How it works**
Each toggle adds a class to the page and saves the choice in the browser (localStorage — the browser's own small storage). Read-aloud uses the browser's built-in voice and deliberately skips Thai, which those voices read poorly.

**What this means for the app**
More learners — including those who find reading hard — can now study comfortably.

**What I learned**
The spacing option has the strongest research behind it, and "dyslexia fonts" don't actually beat a plain, clean one. Also a sharp reminder: always check text colour against its *real* background — my panel text was invisible on the dark menu until I fixed it.

**How We Did It**
1. Explored the app's shared layout and styles.
2. Agreed the design: separate toggles + Atkinson Hyperlegible font.
3. Built it on a branch and tested every toggle live in the browser.
4. Refined after review — dropped a cream-background idea, added read-aloud and reduce-motion, renamed it to "Learning Support", added the who-it-helps note.
5. Merged to `main` and confirmed it live.
6. Hotfixed the panel text colour so it reads on the dark menu.

**References / Conversations**
Claude Code session, 24 July 2026 (Pull Request #19).

---

## 24 July 2026 — Learning Support, part two: you choose what gets read aloud

**Type:** Feature

**TL;DR:** I cut a toggle that wasn't earning its place, and rebuilt Read aloud so the learner picks what gets spoken — the whole page, one part they click, or text they've highlighted.

**What I built or did**
Removed "Reduce motion & distractions", added a "what should I read?" chooser above the Read aloud button, rewrote the panel note to name exactly who the feature is for, and wrote a step-by-step guide on the Help page.

**Why I did it this way**
Reading a whole page aloud is no use to someone who wanted one paragraph. And the reduce-motion toggle barely changed anything — clutter in a menu whose whole job is removing clutter.

**How it works**
"A part I click on" puts the page into a pick mode: hovering outlines each paragraph, clicking reads just that one, Esc cancels. The hint line under the button changes with your choice, so it always says what to do next.

**What this means for the app**
Learners get control instead of an all-or-nothing button, and a plain-English guide telling them how to use it.

**What I learned**
Browsers wipe your highlight the moment you click a button — so the code has to remember the last highlight *as it happens*, not read it afterwards.

**How We Did It**
1. Traced the feature through the shared layout, script and stylesheet.
2. Removed the reduce-motion toggle from all four places it touched.
3. Rebuilt Read aloud around the chooser, including click-to-pick mode.
4. Tested every path in a real browser — pick mode, empty highlight, Esc, links.
5. Raised the panel height when the new note landed below a scrollbar, then wrote the Help page section.

**References / Conversations**
Claude Code session, 24 July 2026.

---

## 25 July 2026 — Three letters the robot voice couldn't read

**Type:** Bug Fix

**TL;DR:** Three of the 44 consonants were being mispronounced by the text-to-speech voice. The spellings were right all along — the voice just couldn't read them — so I taught the recording script to say something different from what the page shows.

**What I built or did**
Fixed the spoken names of ณ, ผ and ย. ณ was saying "nɔɔ **een**" and swallowing the n. ผ was slipping an extra **ɔɔ** into the middle. ย was adding a **yai** on the end that shouldn't be there. Only those three recordings were remade; the other 41 weren't touched.

**Why I did it this way**
My first instinct was to change the spelling in the table until the voice got it right. But that spelling is what learners *see* on the Alphabet page — "fixing" it would have put wrong Thai in front of people trying to learn Thai. So I split the two jobs apart: `name_thai` is what you see, a new optional `speak` field is what the voice hears. They only differ where the voice genuinely can't cope, which right now is three letters out of forty-four.

**How it works**
The recording script now reads `speak` instead of `name_thai`, falling back to the spelling when no respelling is set — so 41 letters carry no extra baggage at all.

```python
'speak': speak or name_thai,  # what the voice is fed
```

Working out *why* the voice tripped up mattered more than the fix itself. ขอ ไข่ comes out perfectly because ขอ is a real Thai word. ผอ isn't a word, so the voice gave up and read it as two separate letters — ผ then อ — which is exactly where the spare ɔɔ was coming from. Once I understood that, the fix was obvious: give it a real word.

**What this means for the app**
Learners hear the right thing on a page whose entire job is teaching pronunciation. A wrong recording on an alphabet page isn't a cosmetic bug — it teaches the mistake.

**What I learned**
Two things. First, when a computer gets something wrong, find out *why* before patching it — the "extra ɔɔ" looked random until I spotted that the broken ones weren't real words. Second, I can't hear audio through Claude, so Claude generated a dozen candidate pronunciations and built me a little web page to click through and compare. That turned a guessing game into a five-minute listening test. Worth remembering: when an AI can't judge something, get it to lay the options out so *you* can.

I also made a judgement call I want on record. The best-sounding fix for ผ uses พอ, which is a real word and comes out as one clean syllable — but it's mid tone where the letter should be rising. I chose slightly-flat over a whole spare syllable. It's a compromise, not a perfect fix, and it's flagged for Paiboon to check.

**How We Did It**
1. Traced the recordings back to their source — one table, `thai_consonants.py`, feeding both the page and the audio script.
2. Generated candidate respellings and compared them in the browser, rather than guessing.
3. Worked out the pattern behind the failures (real words read fine, non-words get split up).
4. Added the `speak` field so the spelling on screen stayed correct, with a comment on each fix saying what went wrong — so nobody "tidies" it back into the bug later.
5. Re-recorded just the three affected clips and checked the other 41 were untouched.
6. Pushed, then confirmed the live site was actually serving the new files by comparing checksums — not just trusting that the push worked.

**References / Conversations**
Claude Code session, 25 July 2026. Commit `962ec7b`.

---

## 25 July 2026 — A picture for every letter

**Type:** Feature

**TL;DR:** Every one of the 44 consonants now shows the thing it's named after — ก is "gɔɔ gài, chicken", so ก gets a chicken — with a new quiz round built on it, and 44 icons I drew myself.

**What I built or did**
Gave every letter a picture in four places: the chart tiles, the detail strip, the flashcard's reveal side, and a new quiz round that asks *"which letter is this the picture for?"* Then replaced the stand-in emoji with a hand-drawn icon set — 44 SVGs in the site's own colours, 30 KB for the whole lot.

**Why I did it this way**
Two kinds of picture, chosen by how many are on screen at once. The chart shows 44 tiles together, so it uses emoji: they cost nothing to load, and page weight is exactly what crashed this page's renderer before. The strip, flashcard and quiz show one letter at a time, so they can afford a real image.

I wanted photographs and couldn't have them. Every stock photo needs a licence that holds up in a public repo, and 44 downloads is weight this page can't carry. Drawing them solved both: nothing to license, and all 44 together are smaller than a single photograph. SVGs are shapes described in code, so they stay sharp at any size.

**How it works**
Pictures are drop-in: name a file after the letter's slug (`kor-kai.svg`), put it in `static/img/consonants/`, and it appears — no code to edit, the same trick the phrase audio already uses. Where no file exists the letter falls back to its emoji, so the page is complete whether the folder is empty or full.

**What this means for the app**
A picture is a memory hook: recognising a chicken is far easier than recalling "gɔɔ gài" cold. And one payoff I didn't have to build — twelve letters whose emoji was only approximate (a pot lid, a cattle goad, Montho) got unambiguous drawings, so they rejoined the quiz's picture round on their own. Picture questions went from about 9 a quiz to 14.

**What I learned**
Four things, three of them from getting something wrong first.

*The right technique in one place is the wrong one in another.* I set the pictures to "lazy load" — the standard trick for images far down a long page. But here exactly one image is built at the moment it's shown, so lazy could only ever delay the very thing being looked at; in a background tab it never appeared at all. I only found it because a test of mine hung waiting for a load event that never fired.

*When you can't source it, make it* — and the constraint often picks the better answer anyway. Vectors beat photographs here on every measure that mattered.

*Judging your own work is part of the work.* I laid all 44 icons out side by side and four were plainly bad: the plate read as a target, the cymbals as leaves, the horse as a blob. I only saw it because I viewed them together, at the size they would really be used.

*When a rule expires, replace it with a narrower one — not with nothing.* Two letters were stuck showing a drum and a trophy, because Unicode has no cymbals character and no offering-tray character, so no emoji swap could ever fix them. My move was to put the drawings on all 44 chart tiles, reasoning that vectors weigh nothing so the old page-weight rule no longer applied. Too broad, and I was pulled up on it: emoji are *designed* to be legible at 32px and a shrunk drawing is not. Only those two letters actually needed one. The rule's reason had half-expired and I had thrown out the half that still held. The exception now lives in the data as a `no_emoji` flag rather than two letter names buried in the code.

**The eight I can't check myself**
Eight of the drawings are culturally specific — the ชฎา headdress, Montho, a เณร novice, a ยักษ์ giant, a ฤๅษี hermit, a ศาลา pavilion, the จุฬา kite and a พาน offering tray. I drew them from description rather than from knowing them, and they want a Thai eye. Any that miss get redrawn or simply deleted: with no file present, that letter falls back to its emoji with no code change.

**How We Did It**
1. Read how the page was built first — one table, `thai_consonants.py`, feeding chart, flashcards and quiz alike.
2. Chose emoji vs real images per place, based on how many appear on screen at once.
3. Built the drop-in folder so pictures could be added later without touching code.
4. Added the quiz's picture round, leaving out letters whose emoji was too vague to make a fair question.
5. Ruled out stock photos on licensing and page weight, then drew six easy objects and looked at them before committing to the idea.
6. Tested the hard case next — animals — because that is what would decide it, then drew the remaining 35.
7. Laid all 44 on one page at real size and redrew the five that failed.
8. Over-applied the icons to the whole chart, then narrowed it back to the two letters emoji genuinely cannot express.
9. Checked the live site returned 404 before pushing and 200 after, so "live" meant something.

**References / Conversations**
Claude Code session, 25 July 2026. Commits `c9a2bc9`, `c9cd015`, `0c398ac`, `8ab1cbe`, `c229e0b`.

---

## 27 July 2026 — One Jataka, two ways to read it

**Type:** Feature

**TL;DR:** The Matuposaka Jataka — the elephant who wouldn't eat while his blind mother went hungry — is now in the app twice: the full English telling on the Culture page, and the real Thai, unsimplified, on Read & Write. Getting there took three rewrites, and each one was me being told no.

**What I built or did**
Added *มาตุโปสกชาดก* in two forms that link to each other. On Culture it's the English story with the scripture framing — a Jataka isn't folklore, so the page names who each character really is (the Bodhisatta, Ānanda, the Buddha's own mother). On Read & Write it's thirteen numbered paragraphs of genuine Thai, each with the English hidden behind a button until you've read the Thai aloud.

**Why I did it this way**
Three attempts. First I built a whole new "Thai Stories" section — undone, because stories already lived in two places and a third home split them further. Then I wrote a *graded* Thai retelling, three-to-six words a sentence — replaced, because plain Thai wasn't what was wanted. Then a folk-tale version — replaced by the canonical Jataka. Each round moved the same way: toward the real thing, in the place that already did that job.

**How it works**
The Story tab now supports two shapes, set by a `format` key. `tokens` is the old word-by-word reader for a beginner still decoding. `passages` is real Thai read whole, with the English hidden by default — because the instruction is to read it aloud *first*. The Monkey King stays as the beginner option, so the tab now spans both stages. On Culture the tale sits in its own list, not the short-stories dict, whose keys double as `/exercise/` links.

**What this means for the app**
A learner can meet the same story at whatever level they're at: in English to understand it, or in unsimplified Thai — royal register and all — to actually read it.

**What I learned**
*When the text is too hard, don't simplify the text — change the interaction.* My instinct was to grade the Thai down until a beginner could tap through it word by word. But the answer was to keep the Thai exactly as hard as real Thai is, and change what the page asks you to do with it: read a whole paragraph aloud, then check yourself. Same words, different job for the reader.

*A new section is rarely the answer.* Content that already has a home usually needs pointing at, not moving.

**How We Did It**
1. Read how the page already worked before adding anything.
2. Built a standalone Stories section — and undid every file when it was the wrong call.
3. Put a graded Thai retelling in the existing Story tab instead.
4. Found the tab only ever rendered one story, so built a picker.
5. Swapped the graded retelling for real Thai passages, and the folk tale for the canonical Jataka.
6. Gave the reader a second format rather than forcing the new text into the old one.
7. Drove the page in the browser and read the DOM directly when the screenshots flaked.

**References / Conversations**
Claude Code session, 27 July 2026. Jataka No. 455, Khuddaka Nikaya.

---

## 27 July 2026 — Giving the Jataka a voice

**Type:** Feature

**TL;DR:** All 13 Thai paragraphs are now read aloud, plus the 11 vocabulary clips the pages were missing. Adding a 19-second clip exposed something I hadn't noticed: the site's audio player had no way to stop.

**What I built or did**
Recorded every Thai string on the Read & Write and Culture pages — 24 new clips, 1.75 MB. Eleven are single words (มาตุโปสกชาดก, พระโพธิสัตว์, มารดา…); thirteen are whole paragraphs of the Jataka read straight through, 165 seconds in all. Each paragraph now has a "Listen to this paragraph" button beside "Check the English".

**Why I did it this way**
The readings got their own build page rather than joining the word clips. Recording a paragraph and recording a word are different jobs with different costs — now the readings can be redone without re-running 700 word clips, and the reverse.

**How it works**
Clips are generated once on my machine and committed as ordinary files, so the live site needs no speech service and pays nothing per play. Filenames are a hash of the Thai itself, which is why 61 of the 72 strings needed no work at all: a word recorded for one page is reused everywhere it appears.

**What this means for the app**
A learner facing real, unsimplified Thai can hear it read properly first, or read it themselves and check against the recording. That's a lot of what makes a hard text usable at all.

**What I learned**
*A new requirement doesn't entitle you to change behaviour for everyone.* The player restarts a clip when you tap it twice — right for a one-second word you're drilling, useless for a 19-second paragraph you want to stop. The lazy fix was to make every button stop on a second tap, which would have quietly broken every existing word button on the site. So stopping is opt-in: a button asks for it, and the several hundred others are untouched.

*Check long recordings by proportion, not by presence.* A speech request that dies halfway still writes a perfectly valid, playable MP3 — it's just short, and nothing looks broken. So I measured seconds-per-character across all 13 paragraphs, where a truncated one would stand out as an outlier. All consistent at ~0.045.

**How We Did It**
1. Ran the generator for both pages — 11 made, 61 already existed and were skipped.
2. Checked the files were really audio, and found my own check was wrong before the files were.
3. Gave the paragraph readings their own build page, separate from the word clips.
4. Found the player had no stop, and made stopping opt-in rather than universal.
5. Tested both directions — word buttons must still restart, passage buttons must stop.
6. Verified against truncation by timing, then confirmed every clip live on the real site.

**References / Conversations**
Claude Code session, 27 July 2026. Commits `ff6be28`, `8e51589`.

---

## 27 July 2026 — The broken link that raised no error

**Type:** Bug Fix

**TL;DR:** One of the five cultural stories linked to a page that doesn't exist. Nothing in the code looked wrong — the page loaded, the link rendered, no exception anywhere. It was only findable by clicking.

**What I built or did**
Fixed the "Modern Thailand" story on the Culture page, whose practice link went to a 404. Each story now says where its link goes, instead of the page working it out. Added a check that runs when the app starts and refuses to boot if any story link is dead.

**Why I did it this way**
The page had been building the link by guessing: it took each story's ID and turned it into `/exercise/<id>`. That works for four of the five, because their IDs happen to double as vocabulary categories. The fifth is about loanword pronunciation and has no vocabulary — so its link pointed at nothing.

I could have written a vocabulary category to make the guess true. But that means inventing Thai, and the story isn't really about vocabulary — it's about the ə/əə sound. So it now points at the Paiboon guide, which actually teaches that.

**How it works**
`_assert_story_links_resolve()` runs at import, the same way the alphabet locks its counts. An `/exercise/` link is only valid if that category really exists; a story with no link at all fails too. The app won't start if either is wrong.

**What this means for the app**
Five out of five links land somewhere real, and the sixth story someone adds can't quietly repeat the mistake.

**What I learned**
*The worst bugs raise no error.* This one had every sign of health: a 200 page, a rendered link, nothing in any log. The only way to find it was to click. Anything derived by convention rather than declared — an ID quietly doubling as something else — can drift apart without a single thing looking broken.

*Verify the thing you're claiming to verify.* My first check that the fix had gone live returned "healthy" on the very first attempt, which meant it was measuring "the site is up", not "the new code is running". A check that would pass before you did the work is not a check. I said so rather than let it stand.

**How We Did It**
1. Looked up why the link 404'd instead of assuming, and found the page was guessing the URL.
2. Ruled out inventing Thai vocabulary to make the guess correct.
3. Made every story declare its own destination.
4. Sent the odd one out to the page that actually teaches its subject.
5. Added a startup check and deliberately fed it broken data to prove it bites.
6. Followed all five links for real, rather than reading the code and calling it done.

**References / Conversations**
Claude Code session, 27 July 2026. Commit `63135bd`.

---

## 28 July 2026 — Dhamma talks, published free

**Type:** Feature

**TL;DR:** A free Dhamma Talks section, first talk in Thai and English. I copied the content pattern from a different part of the codebase rather than the one sitting on the same page, so the next talk costs a file instead of a page.

**What I built or did**
A Dhamma Talks section on the Theravada page, and a reading page for each talk showing the Thai passage with its English underneath. First talk: "Happiness, Like Wealth", translation by Super Pra Ajahn Sujan.

**Why I did it this way**
Two patterns for long-form writing already existed. Pra Kru Bob's articles are hand-built — a route and a 500-line template each. Monk Mode loads a folder of JSON files at startup. Two articles suit the first; a series of talks doesn't.

Free wasn't really a decision. Theravada is already the one free section, on the stated principle that the Dhamma is freely given, so the route carries no access check at all.

**How it works**
`_load_dhamma_talks()` reads `content/talks/*.json`, sorts by an `order` field, and `/dhamma-talk/<slug>` looks one up. The section hides itself while the folder is empty.

**What this means for the app**
The free tier gains content that can keep growing, instead of a fixed set of pages.

**What I learned**
*Ask where content belongs before asking how to build it.* The useful question wasn't which template to write — it was which page already does this job. The answer settled the paywall question too, because that page's free status already came with a reason attached.

*Copy the pattern that fits the future, not the one nearest to hand.* The closest example was Bob's hardcoded articles, sitting on the very page I was adding to. The right model was in a different folder entirely.

**How We Did It**
1. Asked which page owned this content before writing anything, instead of reaching for a new `/talks` route.
2. Read the free/paid table and found the reasoning already in a comment.
3. Compared the two existing content patterns and picked folder-of-JSON.
4. Kept the Thai and English exactly as written, translator credited in the header.
5. Ran the app and loaded both pages logged out, to prove "free" meant free.
6. Checked the live site served the new page before calling it done.

**References / Conversations**
Claude Code session, 28 July 2026. Commit `44f115f`.

---

## 28 July 2026 — One Writings page, and a values line moved back

**Type:** Feature / Decision

**TL;DR:** Merged Pra Kru Bob's two essays into one page, put meditation back on the free side, and found four buttons that had been invisible because of a CSS variable that doesn't exist.

**What I built or did**
Pra Kru Bob's two essays now share one page at `/bob-writings`, with the old URLs redirecting to anchors. Meditation moved from the Basic tier back to Free. Also fixed four buttons whose labels were invisible, and squashed the 27 July commits so the log only shows what's in the app.

**Why I did it this way**
Meditation went to Basic on the reasoning that the page had become practice *tooling* rather than teaching. That didn't hold up. Sitting in meditation isn't tooling — it's the practice the teachings exist for, and "the Dhamma is free but learning to practise it costs £9.99" isn't a line I could defend. So the Buddhism side is free, and the Thai language course is the product.

**How it works**
The essays became one template with in-page anchors; the two old routes now 301 to them, so anything already shared still lands right. The tier change is one word in `SECTION_REQUIREMENTS` — but three other places had the old decision written into them.

**What this means for the app**
One menu entry for Pra Kru Bob instead of two, and everything Buddhist — teachings, talks, articles, meditation — is free to anyone, no account.

**What I learned**
*An undefined CSS variable deletes the whole line it sits in.* Four buttons used `var(--gold)`, which isn't defined anywhere — the real name is `--royal-gold`. So the background was discarded and white text sat on a pale page. They appeared on hover, because the hover rule used a variable that does exist. **Those two dead names are used about 90 times across 16 templates** — colours that have never once rendered as written.

*A decision lives in more places than the code that enforces it.* Changing meditation's tier was one word. But the dāna banner named meditation as the paid part, the pricing page sold it under Basic, and the README argued the old position at length. **Change the rule and you have to change every place you argued for it, or the app contradicts itself in public.**

*Mixed answers across two URLs during a deploy mean it's still deploying.* One page served the new build while another still 404'd, and I called it a broken route. It was a half-finished swap. I was wrong for about two minutes.

**How We Did It**
1. Merged the two essays by extracting their bodies programmatically, then checked the text was byte-identical rather than eyeballing 800 lines.
2. Redirected the old URLs instead of deleting them.
3. Traced the meditation decision to all four places it was written down.
4. Tested the gate logged out — and found gated pages return 200 with a locked screen, so checking status codes proves nothing. Checked content.
5. Squashed the 27 July commits, verifying the file tree came out identical.

**References / Conversations**
Claude Code session, 28 July 2026. Commits `b373c9d`, `58ffba7`.

---

## 30 July 2026 — Fixed the Monk Mode ON and Monk Mode OFF pages

**Type:** Bug Fix

**TL;DR:** Monk Mode already waived payment in the access code, but every page still quoted monks a price. Fixed that across the whole site, and found the Vocabulary page had never been gated at all.

**What I achieved**

*Monk Mode ON — no way to pay, anywhere:*
- No pay or upgrade button on any page. Locked pages now read **"Free 🧡 — no payment needed, just reach the level"**
- No prices and no "Basic"/"Pro" tier names anywhere on the site
- **Progress** — tier card shows "Free 🧡"; the £9.99/£19.99 plans table is replaced by "no subscription needed"
- **Premium** — "🧡 Monk Mode — nothing to buy"; plans grid and the £9.99 Instant Access Pass both gone
- **Footer** (on all 26 pages) — "Requires Level 8 — free with Monk Mode" instead of "£19.99/mo"
- **Meditation** — the generosity note no longer names a paid tier
- **Vocabulary and the Paiboon Guide** — now gated by progress only, free of charge, and their Requirements to Unlock box looks identical to every other Learn page

*Monk Mode OFF — the paid product, corrected:*
- **The pay button and all prices stay exactly as they were** — checked page by page so nothing about the paid experience drifted
- **Vocabulary is now gated at Basic.** It had been open to everyone — its rules were written down but never enforced
- **Paiboon now requires the alphabet first**, like every other Learn page
- **Subscription tiers rewritten to say what you actually get:** Free gains the Thai alphabet and the AI Tutor allowance; Basic gains vowels & syllables, reading the script, tones & consonant classes, sentences with audio, the gender guide and the exercise sets; Pro gains the roleplay conversation partner and the exercise generator
- **Premium advertised 5 free AI messages a day while the code allowed 15** — both now read the same value, so they can't disagree again

*The known exception — AI Chat:*
- **AI Chat is the one thing Monk Mode still doesn't make free.** Monks get 15 messages a day and Tutor mode only, and the other modes still say "upgrade to Pro". That's deliberate: every AI reply costs real money to run, so unlimited free AI is a separate decision I've kept out of scope. Everything else on the site is free to a monk; this one isn't, and the entry says so rather than claiming otherwise.

**How it works**
`monk_mode` was already passed to every template, so the display fixes needed no route changes — each sits behind `{% if monk_mode %}` with the original markup kept in the else branch. Vocabulary needed a real fix: `@require_access('learn')` was missing from the route.

**What this means for the app**
A monk sees one consistent story — free of charge, still gated by progress. Paying visitors can no longer read the entire Vocabulary section for nothing.

**What I learned**

*A keyword search is not proof.* My audit called the AI chat page "clean" for monks. It wasn't — its upgrade prompts live in JavaScript strings my patterns never looked at. **The scan answered what I asked, not what was true.**

*Defining a rule isn't enforcing it.* `SECTION_REQUIREMENTS` held a complete entry for Vocabulary — level, tier, alphabet — and none of it did anything, because the route was never decorated.

*A flag is only as good as every place that reads it.* `monk_mode` was right in the access function and ignored by five templates.

**How We Did It**
1. Read the access code first and separated what actually charges monks from what only *says* it does.
2. Fixed the locked page, then swept every other template instead of stopping at the reported symptom.
3. Verified by rendering 28 routes twice — Monk Mode on and off — rather than clicking around.
4. Checked the paid experience in the same pass, so the fix couldn't quietly break the product.
5. Broke the local server with a `NameError` moving a constant, and caught it because it crashed loudly.

**References / Conversations**
Claude Code session, 30 July 2026. Commits `f999bf3`, `6141ca5`.

---

## 30 July 2026 — A chanting book, and the tone-mark bug it uncovered

**Type:** Feature + Bug Fix

**TL;DR:** Built the first page of a chanting book — Pali, Thai, Paiboon and English, line by line. Building it uncovered a bug that had been quietly wrong in every AI reply the app has ever sent: three of my five Paiboon tone marks were mapped to the wrong tones.

**What I achieved**
- A new **Chanting Book** page, on the free tier alongside the other Dhamma pages — the chants aren't mine to sell
- Every verse carries four layers: **Pali in Thai script** (what's actually chanted), the same **Pali romanised**, the **Thai translation**, **Paiboon** for reading that Thai aloud, and the **English** meaning
- Layers are colour-coded and can be **switched on and off** — a Thai chanter hides the Paiboon and English, an English reader hides the Thai script. One page, two books.
- Chants sit in a **grid of cards** that expand on click, ready for the dozens still to come
- First chant in: **Khemākhema-saraṇadīpikā-gāthā** (Dhammapada 188–192)
- Fixed the Paiboon tone marks across the whole app

**How it works**
The chants live as data in `chanting.py` rather than as page markup, because the end goal is a printed book — same source, different renderer. Adding a chant means appending one dictionary. The cards are plain `<details>` elements, so they open without JavaScript and print properly.

**What this means for the app**
Anyone can chant along in whichever script they read, and hide the rest. And every AI reply now romanises tones correctly.

**What I learned**

*When a spec contradicts its own examples, trust the examples.* My AI prompt defined `à` as falling and `ǎ` as low. Its own examples used them the standard way — `sà-wàt-dii`, `rʉ̌ʉ`. **The examples were right and the rules had been wrong for months.**

*Pali is not Thai.* Both sit in Thai script on the same page, and I nearly ran my Thai romanisation system over the Pali. **Same letters, different language, different rules.**

*A scan is not a source.* The OCR read ทั้ง for ทัง and merged two words into one. I only caught it against the physical book — which is the division of labour worth keeping: I verify the Pali, the AI does the structure.

**How We Did It**
1. Worked out the layer structure first — spotted that "Thai script" meant two different things (the Pali *and* the translation) before writing any code.
2. Pasted the chant from a scanned book, then checked it against the physical copy and corrected four OCR errors.
3. Found the tone-mark bug while generating the Paiboon, and fixed the prompt rather than working around it.
4. Went through all five verses of Paiboon line by line before committing anything.
5. Rebuilt the single-scroll page into a grid of cards once it was clear the book would hold dozens of chants.

**References / Conversations**
Claude Code session, 30 July 2026. Commits `5944994`, `3b077bb`, `198d045`, `73db735`, `88e20de`.

---

## 31 July 2026 — From a chanting page to a Digital Chanting Book

**Type:** Feature / Strategy

**TL;DR:** Reframed the whole thing before writing a line of code — the web app is where the content gets tested, the printed book is what it becomes.

**The brief I set, in my own words**

> "Rather than thinking of it as a 'chanting page,' think of it as a Digital Chanting Book. Then, when you publish the printed edition, you're polishing and typesetting content that has already been tested by users."

> "When you later publish the printed edition, very little content will need changing. The web app becomes the interactive version — with collapsible sections and optional text layers — while the physical book presents the same material in a carefully typeset, permanent format. This gives your project a consistent identity across both digital and print, rather than treating them as two separate resources."

> "Every chant answers six questions: What is this chant? Where does it come from? When is it chanted? Why was it taught? What does it mean? How do I chant it? That makes the Digital Chanting Book suitable for complete beginners while remaining useful to experienced practitioners who want to deepen their understanding."

**Why that way round.** Print a thousand copies and *then* discover a translation reads badly, and it's an expensive lesson. Build it digitally, let people use it, and print what has survived contact with readers — but only if the digital version already holds everything the printed one needs, in the same order, from day one.

I specified the layers and the layout too:

> "Welcome to the Digital Chanting Book. Each chant is presented in five optional layers to support both learning and practice. Pali (Thai script) — the original chant as recited in Thai Theravāda temples. Pali (Romanised) — the same Pali written in the Latin alphabet to aid pronunciation. Thai translation — the meaning in Thai. In many Thai temples, this is also recited after the Pali. Thai (Paiboon) — the Thai translation romanised for readers who cannot yet read Thai script. English translation — the meaning in English."

> "Show only the layers you need. As your confidence grows, try chanting directly from the Pali while using the translations to deepen your understanding."

> "Standard Layout for Every Chant. Each chant follows the same format. Title. Pali Source — the original source of the chant, such as the Dhammapada, Khuddakapāṭha, Suttanipāta or another canonical text. When Chanted — when the chant is traditionally recited in Theravāda practice. Historical Background — a brief explanation of the historical setting or occasion in which the Buddha taught the verses, or the origin of the chant if composed later. Meaning and Purpose — a concise explanation of the teaching and why Buddhists continue to chant it today. The Chant."

And the constraint on the rebuild:

> "Can we restructure the existing chanting page to the digital chanting book while ensuring all content such as verse by verse chanting content (scripts and translations) remain as is."

**What I achieved**
- The six questions became six fields, in that order, on every chant
- Split the old catch-all note into `when_chanted`, `background`, `meaning` and a `summary`
- Background and meaning collapse, so someone who came only to chant isn't scrolling past history

**How it works**
Chants live as **data** in `chanting.py`, never page markup — one source, two renderers.

**What this means for the app**
A reader can chant from it now. A publisher could set from it later. Neither needs the content rewritten.

**What I learned**

*A closed section prints as just its heading.* Background and meaning would have come out blank on paper — for a project aimed at print, exactly the bug you don't want to find at the printers. They now open before printing and close again after.

**How We Did It**
1. Wrote the six questions down before touching code.
2. Split one overloaded field into four honest ones.
3. Verified every line of chant content was byte-for-byte unchanged.
4. Tested printing, found the blank-section bug, fixed it.

**References / Conversations**
Claude Code session, 31 July 2026. Commits `ab1d0e3`, `55727c6`.

---

## 31 July 2026 — One romanisation system, not two

**Type:** Bug Fix / Consistency

**TL;DR:** Questioning one spelling uncovered 904 inconsistent dictionary entries — and the prompt that had been causing them.

**How it started — one question**

> "I am concerned about this: ของ → kɔ̌ɔŋ (never 'khǎaw'). Which one is actually correct? Which one does the official chanting book with Thai script use? They both have different pronunciations."

That was the whole thing. Two spellings can't both be right, and the answer decided 904 entries. Once it was clear:

> "normalise the Paiboon to ŋ everywhere now"

**Why it mattered more than it looks**
On a website an inconsistency is patched next week. **In a printed book it's permanent.** If `พระ` is `prá` on page 12 and `phrá` on page 40, a learner can't tell whether `k` means a puff of air — and the pronunciation guide stops teaching. Better settled at two chants than at thirty.

**What I achieved**
- Normalised ง to `ŋ` everywhere the app romanises Thai
- Fixed both Paiboon generator prompts, which were the actual cause

**What I learned**

*A prompt that contradicts itself doesn't fail — it splits the difference.* My generator said `ง → ng` on one line and showed `waŋ not wang` on the next. Given a rule that disagrees with its own example, the AI picked one at random each time. That's why the data was a *mix* rather than consistently wrong — and why it looked like flakiness instead of a bug with a cause.

*Fix the source, not the symptom.* Cleaning 904 cells without fixing the generator would have meant the next batch quietly put them back.

**How We Did It**
1. Checked all 186 tokens containing "ng" for ambiguity first — `g` is a real Paiboon letter, so a blind find-and-replace could have broken real words.
2. Changed only the romanisation column, then proved row by row the English and Thai were untouched.
3. Traced it back to the generator prompt and fixed that too.

**References / Conversations**
Claude Code session, 31 July 2026. Commit `7bdc618`.

---

## 31 July 2026 — The second chant, and what "done" looks like

**Type:** Feature

**TL;DR:** Added บทพิจารณาสังขาร (13 verses) and used it to pin down exactly what a finished chant looks like.

**Why this chant mattered**
It was the first chant added *after* deciding the book had to be print-ready, so it doubled as the specification — everything I wanted future chants to look like had to be true of this one first. That's what made it the right test case for the prompts.

**The instructions that shaped it**

On fidelity, when I'd already flagged things that looked wrong in my own source:

> "Just do it without changing anything from the book i.e. don't change what I pasted."

On not filling gaps to look complete:

> "Forget the Pali title here because there is none for the pasted script."

On how it should read:

> "Make it like a book users can read/chant from and break it down verse by verse. The verses need to be broken down correctly like in the official book. Use what I pasted as an example of exactly how it should look."

> "This layout follows the style of a traditional Thai chanting book: each Pali verse stands alone, followed immediately by its Thai meaning in Paiboon romanization, making it easy to chant the Pali and then read the meaning without any Thai script."

And on the index:

> "Add this to chant 2 card in app Digital Chanting Book so users can quickly and easily identify which chant to look for in the book."

**What I achieved**
- The chant broken **one Pali line per verse**, the way the official book breaks it
- Three section headings inside the chant: impermanence, life and death, the body
- Cards that identify a chant at a glance: Thai title, romanised title, English name with its opening line, and when it's chanted

**What I learned**

*Faithful means faithful, even when the source looks wrong.* My book prints `ฉุฑโท` where standard editions have `chuddho`. I kept what my book says and flagged it, rather than correcting my own source into someone else's.

*Name things the way people look for them.* I first called it "(Saṅkhāra)" — a *topic* several chants touch. Renaming it by its opening line, "(Sabbe saṅkhārā aniccā)", names *this* chant.

**How We Did It**
1. Pasted the Thai straight from the official book.
2. Had every Thai character counted both ways — 869 in, 869 out.
3. Rebuilt the verse split once I saw it didn't read like a chanting book.
4. Added the card identifiers so the index is scannable.

**References / Conversations**
Claude Code session, 31 July 2026. Commits `efd8f6b`, `b8eb4b1`, `4fc20b1`, `859bc8c`.

---

## 31 July 2026 — A repeatable process for adding a chant

**Type:** Tooling / Strategy

**TL;DR:** Built the thing that adds chants, rather than adding chants one at a time.

**Why, in my own words**

> "So that everytime I decide to add a new chant to the app Digital Chanting Book, what gets added to the app ends up looking exactly as I want it thanks to Prompt 1 and 2 plus my pasted Thai script."

> "The process of how we created Prompt 1 and Prompt 2 [was] a strategic move to improve speed and efficiency and also accuracy and consistency in line with my exact aims of designing and building the Digital Chanting Book as well as it being preparation for a future physical published book."

The register the prompt has to hold, which I'd worked out first:

> "It's mostly Central Thai, but it uses a formal literary register that is traditional in Buddhist scriptures and chanting books. It is not Royal Thai, and it is not a separate 'monk language.' Think of it as the Thai equivalent of the language used in an English Bible or the Book of Common Prayer — recognizably modern English, but more formal, traditional, and rich in religious vocabulary."

And the format decision that made the handover reliable:

> "For Prompt 1 can we add this instruction: JSON with unwrapped single-line values and the checks as a separate array."

**Why build the tool instead of adding chants**
There are dozens of chants still to add. Doing each by hand is **slow**, it **drifts** (chant 9 ends up shaped slightly differently from chant 2), and it's **error-prone** in the one place errors matter most — the Pali. A book with inconsistent structure is a book you re-edit before printing. So I spent the day building the *thing that adds chants*. Four aims, all pulling the same way:

- **Speed** — a pasted page becomes a structured entry in minutes
- **Efficiency** — two tools, each doing what it's actually good at
- **Accuracy** — the AI never invents Pali; it flags what I must check
- **Consistency** — the same six sections, five layers and romanisation, every time

That last one is the print preparation. Consistency is cheap to enforce with a prompt and expensive to fix in a typeset book.

**The process, start to finish**
1. **Copy from the official chanting book** — the Pali in Thai script and its Thai translation
2. **Paste into Claude.ai under Prompt 1** — returns one JSON object: five layers, background, meaning, section headings, plus everything it wasn't sure about
3. **Check the flagged items against the physical book** — the step nothing can do for me
4. **Paste Prompt 2 plus that JSON into Claude Code** — writes it into `chanting.py`, counts every Thai character both ways, renders the page
5. **Review, commit, push** — live in the app

**What I achieved**
- Both prompts written, tested on a real chant, and refined through **four versions in one day** — each caused by a real failure, not a hunch
- Archived with reasoning, version history, an automatic scoring rubric and a check that runs on every push
- A 7-page PDF built from the prompt file itself, so the sheet can't drift

**Choosing the tool by testing it**
I ran Prompt 1 in **both Claude.ai and ChatGPT with the same page of Thai** from the official book, and compared:

> "Claude.ai gave the working notes and flagged issues, ChatGPT just gave output. The Claude output is better on the things your spec says matter most — source fidelity and flagging — and ChatGPT is better in two specific places I got wrong. The single most serious difference isn't romanisation at all; it's a meaning error in ChatGPT's verses 4–5."

**What I learned**

*The obvious difference and the important difference were not the same difference.* Romanisation is what you notice first — visible, on every line, and comparatively harmless; a reader mispronounces a word. A wrong translation is invisible on a skim and teaches the wrong Dhamma.

*Questions that aren't reporting bugs still find them.* Two of mine each turned up a real fault:

> "Does the JSON from Stage 1 mean the Stage 1 output? Is it the same thing?"

The prompt was asking for the same thing twice, in two places — left over from a format change.

> "Is the JSON object and it's closing sentence contained in the whole Stage 1 reply? Or do I get it from elsewhere?"

That one showed the handover wasn't actually written down anywhere.

> "Did you update the Stage 2 prompt in GitHub? I can't see any changes."

It had. Reading it to prove so exposed three rules pointing at labels that no longer existed — guarding the "never invent a title, source or invitation" behaviour. Silently dead.

*Fonts are a real constraint when you're aiming at print.* Only one font on my machine covers Thai, Pali diacritics and Paiboon at once, and the warning symbol printed as empty boxes until every character was checked against it.

**The prompts themselves**
Both live in [`prompts/chanting-book-entry/`](prompts/chanting-book-entry/) with their reasoning and version history, and as a printable sheet at [`chanting-book-prompts.pdf`](prompts/chanting-book-entry/chanting-book-prompts.pdf). Not copied here on purpose — they changed four times in a day, and a journal entry can't be kept current the way a source file can.

**How We Did It**
1. Wrote both prompts, then tested them on a real chant.
2. Rewrote them when the output didn't read like a chanting book.
3. Switched the handover to JSON so Thai and Paiboon can't get mangled between tools.
4. Built the PDF from the prompt file itself so it regenerates whenever the prompts change.

**References / Conversations**
Claude Code session, 31 July 2026. Commits `2e3dc45`, `1fbe2ad`, `ca1fff3`, `a2f1964`, `40148d7`, `09de131`, `1b59559`, `9561e97`, `0550f6c`, `a755426`.

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

---

## 3 August 2026 — Seven chants in, and a pipeline that proves nothing was lost

**Type:** Milestone

**TL;DR:**
- The Digital Chanting Book went from 2 chants to 9 — 18 verses to 186.
- I stopped hand-typing chants and had them generated mechanically from the source, so no Pali could be quietly altered on the way in.
- Every correction now keeps the original reading next to it, so I can still check it against my physical book.

**What I built**
Seven new chants, each one added, verified and committed on its own before the next was started. Two of them are printed Pali-only, so the app now says on the page that their English is a working translation, not the book's own words.

**Why I did it this way**
Hand-typing Thai and Pali is exactly where a chanting book goes wrong — a lost space or a swapped tone mark is invisible on screen and wrong forever in print. So each chant was transcribed once, then the Python was *generated* from that file. Every Pali, Thai and Paiboon line is written as one unwrapped line, so the code that wraps text physically can't reach them.

**What I learned**

*A correction that hides the evidence is worse than the error.* When I authorised fixing the Thai, the fix had to keep the original reading in a note beside it. Correcting silently would have removed the very thing I need to check against the book.

*Only correct what the text itself proves.* `เล่า` → `เหล่า` is fair when the same chant spells it correctly five times. `เกิด` → `เถิด` only *reads* better — that one stays flagged.

*A denylist only catches what you've already seen.* A stray key kept arriving under new names — `note`, `stanza_note`, `line_break_note`. Listing the bad names failed; listing the *good* ones caught it every time.

**How We Did It**
1. Transcribed each chant once into a plain data file.
2. Generated the Python from it, rather than typing it out.
3. Counted every Thai and Pali character both ways — delta 0, every chant.
4. Rendered the real page to confirm verse counts, headings and layers.
5. Committed one chant at a time, so any problem stays isolated.

**References / Conversations**
Stage-1 chant sessions; 127 `‼` verification notes left in `chanting.py`.

---

## 3 August 2026 — Crediting two senior monks properly

**Type:** Decision

**TL;DR:**
- Both essays and the Dhamma talk now name the monks behind them in full, rather than by a short name alone.
- Ajahn Sujan's Thai isn't word-for-word, and the page now says so — which matters on a site people use to learn Thai.
- The whole thing started from wondering how I'd credit the Pali Canon if I add it.

**What I did**

Added a source note to Pra Kru Bob's Writings giving his full monastic name, **Pra Kru Samu Panya Vajiro**, the Level 3 Advanced Buddhist Studies examination, his Doctorate of Science and psychology background, and the fact that he is the monk who first guided me toward AI. Upgraded the Dhamma talk credit to name **Super Pra Ajahn Sujan (Dr. Sujan), PhD in Buddhist Psychology**, and added a line explaining how he worked on the talk.

**Why I did it this way**

This began while I was considering adding the full 44-volume Tipitaka (the Pali Canon) from SuttaCentral to the app — the original Pali with accurate English translations. Thinking about how I would credit a body of work that size made me look at how I was crediting the two monks already on my site. I already had "By Pra Kru Bob" on both essays and a short translation credit on the talk. Both were true, but both were thin. These are senior monks who gave real work to this site, and a short name undervalues them.

**What this means for the app**

Ajahn Sujan didn't translate my talk literally — he reworked the wording to sharpen the points, bringing his scholarship to it. The page shows Thai and English stacked as pairs, so a learner who found they didn't match would assume they'd misread the Thai. Now the page tells them the two genuinely differ.

**What I learned**

*Credit is worth more when it's specific.* "By Pra Kru Bob" is a name. "Pra Kru Samu Panya Vajiro, who passed the Level 3 Advanced examination and first guided me toward AI" is a person, and tells the reader why his writing is worth their time.

*Relevance isn't only about the subject.* A Computer Science degree says nothing about essays on Buddhism — but it explains why he is connected to this site at all. That earned its place.

**What's next**

Possibly the Tipitaka itself. I want the direct teachings of the Buddha from sources that are accurate and factual, without opinion or bias layered on top — which is exactly why SuttaCentral appeals to me, and why getting the crediting right matters before I start.

**References / Conversations**

Commit `29d9abc`. Verified live on `/bob-writings` and `/dhamma-talk/happiness-like-wealth`. SuttaCentral considered as a future source.

---

## 3 August 2026 — Four more chants, and a fragment that had to say so

**Type:** Milestone

**TL;DR:**
- The Digital Chanting Book went from 9 chants to 12 — 186 verses to 263.
- One chant arrived in two halves, sat on the live page as a fragment pretending to be whole, and now there's a way for a part-set chant to say so.
- Removed the second ติลักขะณาทิคาถา. It wasn't a mistake — it was a question I'd deliberately left open, and this is me answering it.
- One chant came from photographs rather than typed text, which is a different and larger kind of risk.

**What I built**

Four chants, added one at a time: เมตตานิสังสะสุตตัง (24 verses, the eleven benefits of loving-kindness in prose), เมตตานิสังสะคาถา (41 verses, the ten-stanza refrain form), ท์วัตติงสาการะปาโฐ (39 verses, all thirty-two parts of the body) and ภาระสุตตะคาถา (8 verses, on the burden of the aggregates).

Also a `partial` field, which prints a notice above any chant whose text is only part-set — "An incomplete chant. Only the preamble and the first ten of the thirty-two parts are set here."

**Why I did it this way**

The `partial` notice holds its own sentence in `chanting.py` rather than in the template. The first sketch put the wording in the markup, which would have meant one chant's specifics baked into a block shared by every chant. Keeping the sentence beside the chant it describes means the next fragment needs no template edit at all — and it's the same rule this file has followed from the start: the data lives here, not in the page.

For ท์วัตติงสาการะปาโฐ I merged the second half into the existing entry rather than appending a new one. Two entries with the same title is exactly the thing I'd just spent the morning cleaning up, and the chant's own section heading, opened at verse 6, has to span the whole enumeration to make sense.

**How it works**

Same pipeline as the last seven chants — transcribe once, generate the Python from that file rather than typing it, then count every Thai and Pali character both ways. Delta was 0 on all four chants. The merge worked the same way: it rebuilt the whole entry from source rather than patching it by hand.

**What this means for the app**

263 verses live at `/chanting`, one card per chant instead of a duplicate showing twice, and a fragment can no longer pass itself off as a finished chant.

**What I learned**

*A fragment that looks complete is worse than one that's obviously missing.* Ten of thirty-two parts rendered as a perfectly ordinary chant, with nothing on the page saying otherwise. Nobody reading it would have known to doubt it.

*Count the thing, not the container.* Several verses name two body parts at once, so verse count isn't part count. Counting verses said 28 and looked wrong; counting parts said 32 and matched the title. The check only works if you count what you're actually claiming.

*The text can settle its own arguments.* The first half printed อะโฮ where the second printed อะโธ — the same line, two ways, in one chant. I'd flagged the first as suspect; the second half proved it. The book disagreeing with itself was the evidence.

*A flag is only as good as what it actually tracks.* `english_unverified` marks chants where the book prints no Thai and the English is ours. Two of these chants do print Thai, so setting it out of habit would have put a false notice on the page. Worth checking what a flag means before reaching for it.

*I got a word wrong in the git history.* My commit and merge messages call the removed ติลักขะณาทิคาถา an "accidental duplicate". It wasn't. Commit `c349807` added it deliberately, on my instruction that it was a distinct chant, and flagged itself `FOR REVIEW` with the right question attached: if the book prints this chant twice, this is correct; if not, deleting it is a clean revert. Today's deletion was me answering that, not fixing a slip. The commits are pushed and I'm not rewriting them, so this is where the record gets put straight.

**Still open**

157 `‼ CHECK` notes now sit in `chanting.py`. ภาระสุตตะคาถา is the one to read first — its Pali and Thai were transcribed from photographs rather than typed out, so the whole entry needs reading against the book rather than spot-checking. It's live, and it's the least verified thing in the file.

**References / Conversations**
Stage-1 chant sessions; commit `c349807` for the duplicate's original open question; 157 `‼ CHECK` notes in `chanting.py`.

---

## 4 August 2026 — A pipeline for 286 chants, and a page number that has to be right

**Type:** Milestone

**TL;DR:**
- Built a three-stage batch workflow so 286 chants can go in without pasting one at a time.
- Added the physical book's page numbers to the app — the monk calls out a page, so the app has to answer.
- Measuring before rewriting changed the design; negative-testing found a check that had never worked.

**What I built**

A batch variant of the chanting prompt. Stage 1 takes 6–9 chants at once, Stage 2 writes them into `chanting.py` and merges repeats instead of duplicating them, Stage 3 adds the commentary later. Page numbers now show on each index card and at every page turn.

**Why I did it this way**

I measured before rewriting. A finished entry is **9.1× the size of what I paste in**, and Thai script tokenises about twice as expensively as English — so chants-per-reply is arithmetic, not wording. That killed my "10–20 pages a message" idea before I built anything on top of it.

**How We Did It**

Measured the real data → found the true ceiling → split the work by depth → built a manifest that makes truncation detectable → negative-tested every check → added page numbers → two commits, pushed, verified live on Render.

**What I learned**

*A green tick is a claim, not evidence.* All 17 checks passed at 100% — until I fed them deliberately broken input. That exposed a check that had never caught a real error: it only matched unaccented spellings, and every Paiboon+ syllable carries a tone mark.

*Cheaper isn't better.* Dropping the English layer bought more chants per reply, but would have forced Stage 3 to edit ~5,800 verses instead of adding keys — destroying the one guarantee protecting verified Pali.

**Still open**

269 chants to go. Search and A–Z browse deferred until there's enough to browse.

**References / Conversations**

Commits `38fb244`, `a3e609d`, `6fd2369`, `ca295bd`.

---

## 2026-08-05 — The chanting book starts reading like a book

**TL;DR:**
- The batch workflow left Claude.ai chat for Claude Code — it reads the photographs off disk now, and nothing crosses a clipboard.
- The Digital Chanting Book has real pages for the first time: 29 chants, 491 verses, pages 2–8 live.
- Three of my prompt's rules turned out to be wrong, and only running it on real pages showed which three.

**What I built**

A page-by-page reading view with two modes — as the book prints it, or verse by verse with all five layers — and the workflow that fills it.

**Why I did it this way**

> "As we work through the chants, adding them to the app in batches, I want all chants added to the app Digital Chanting Book to be laid out like the actual book... This is important for accuracy when a monk calls out a page number, users go to that called-out page number and find the exact chant as to follow along chanting with the monk."

A wrong page number isn't untidy — it's someone lost mid-chant in a silent room.

Then a constraint changed the architecture:

> "Claude.ai chat is unable to handle 9 pasted images from the chanting book. Would it be better to adapt Stage 1 to Claude Code as I'm sure Claude Code can do this entire job on it's own?"

It could. I kept two stages anyway — one pass that reads a photograph and writes the chant is marking its own homework.

**How We Did It**

Photograph the pages → Stage 1 reads them into a JSON batch file → Stage 2 reconciles the page map before writing a line → verify → commit.

**What I learned**

*My own answer was worth more than my question.* I asked how the book numbers its pages and got:

> "There is alwyas a page number at the top centre in English. All other numbers contained within some pages are numbers for chants or something else; either in Thai or English?"

That became a hard rule: a chant number read as a page number looks reasonable and is wrong for every page after it.

*Two options were both worse than a third:*

> "Should we add a button which opens 1. One verse per item (Recommended) so we get the option of seeing original image (Book) lay out and also a button which opens the 5 layers of translations in verse by verse mode?"

*Don't design for the page in front of you:*

> "It's just an example of a page. Can you adapt to a page whether it contains Thai translations, Pali only or a mixture?"

*Checking that something is present is not checking that the old thing is gone.* The rebuilt PDF still told readers to open a chat:

> "This has not yet been updated it still appears as the old one saying Claude.ai"

The prompts were right; the sheet's own instructions were hardcoded in the PDF builder. I verified the new rules were in it and never verified the old ones weren't.

**Still open**

8 pages of roughly 330 are in — the whole morning service. 37 checks to verify against the physical book — starting with `สวากขาโต`, which I read two different ways on two pages, so one of them is wrong.

**Engineering Contribution**

*Decisions made:*
- Kept Stage 1 and Stage 2 apart when one pass would have been simpler. Stage 1 may not touch the app; Stage 2 may not open the photographs. The failure being guarded — a verse on a plausible but wrong page — leaves no trace afterwards, so the pass that makes the claim must not be the pass that checks it.
- Dropped a sticky page bar after building it. The site nav is already sticky at 202px; a second one left almost no room for the verses, which are the point of the page.
- Measured `build_page_index` instead of caching it — 0.02 ms now, 0.34 ms projected at 286 chants. Rejected the optimisation and recorded the number.
- Committed the batch JSON files. They are the only record of what each photograph said; `chanting.py` holds what reached the app, and the book is on a shelf.

*Improvements made to generated code:*
- Extracted `scripts/apply_batch.py` with 24 tests, after hand-writing the same Stage 2 step three times — one copy reported "CONTINUES marker removed" without removing it. Dry-running the new script against the real batches then found a gap in it: no duplicate-id guard, so re-applying batch 1–3 would have appended eight duplicate chants.
- Moved the "this English is ours, not the book's" notice out of the `starts_here` branch. Page 5 was showing our translation with no notice at all.
- Aligned the comment marker: the prompt said `⚠️`, the file uses `‼` 336 times.
- Added a markup guard asserting *absence* after an unclosed `</style>` rendered a blank page while the server returned 200 with correct HTML.

*Roughly how much was accepted as-is:*
About half. The page view's structure and the batch prompt's fidelity rules went in close to first draft. The two-stage split, the sticky-bar removal, the page-map reconciliation and everything in `apply_batch.py` came out of rework — most of it prompted by things going wrong in front of me rather than by review.

**References / Conversations**

Commits `5b33172` through `dcb6eb6`. Prompt archive: `prompts/chanting-book-batch/` (v4, v5, v6 under `versions/`). Batch records: `prompts/chanting-book-batch/batches/`.

---

## 2026-08-06 — The page that looked finished and wasn't

**TL;DR:**
- Pages 7 and 8 were live showing about 40% of what the printed page shows. No test failed.
- The data model was chant-shaped; the book isn't. Built `PAGE_BLOCKS` so a page can hold what belongs to the page.
- Prompt v7: the project is a digital publication, not a translation — and a batch now can't close while anything it read is unaccounted for.

**What I built**

A page-level content model — headings, instruction paragraphs, service closings, numbered items, rubrics, footnotes and invitations — woven into the chants in printed order. Pages 2–9 now match the book. Tests 101 → 123.

**Why I did it this way**

I found it by reading the app beside the book, not by running anything:

> "What about Page 7 & 8 which are both empty?"

Claude checked the data, the local render and the live site, found the chant text in all three, and told me there was no problem. It had answered the wrong question:

> "I checked them in the app against the book and they don't appear to contain everything so make it exactly the same as the book."

"Empty" meant incomplete, not blank. Stage 1 had read the missing material correctly and written it into the batch file; stage 2 had nowhere to put it and dropped it silently. **The bug wasn't carelessness — it was that nothing compared the batch file to what got written.**

**How We Did It**

1. Diffed the printed page against the app, block by block, and listed exactly what was missing.
2. Built `PAGE_BLOCKS` + `check_page_blocks()`, reworked `build_page_index` and the template. No content yet — model first, so the diff stayed readable.
3. Retro-filled pages 2–8 from the photographs. Found the app was *inventing* headings on four chants the book gives no title.
4. Rewrote the prompt to v7 and proved it additive: 229 lines added, **0 removed**.
5. Entered page 9 under v7 — the first page where the new gates ran.

**Engineering Contribution**

- *Decisions made:* Page material kept separate from chants rather than bolted on as more chant fields — `จบพิธีทำวัตรเช้า` closes the morning *service*, so attaching it to the chant above would state something false about the book. The anchor check was moved out of `build_page_index` into a validator after the first version 500'd the whole chanting book over a single typo.
- *Improvements made to generated code:* A self-review of this session's own code found four real defects: dead code, two `O(n×m)` dict rebuilds (~93,000 needless constructions across the full book), and a test docstring that had quietly become untrue. Five new rubric criteria, each negative-tested before being trusted.
- *Roughly how much was accepted as-is vs engineered on:* Direction and review, not code. I wrote none of it — but I found the defect, set the standard, and made it prove v7 hadn't quietly removed anything. Evidence: `prompts/chanting-book-batch/REASONING.md`.

---

## 2026-08-06 (later) — The index that knows what's missing

**TL;DR:**
- The book's front matter is in: cover, title pages, and all ten pages of `สารบัญ` — 301 lines naming every chant across 325 pages.
- Built from data rather than reproduced as a picture, so it doubles as an honest progress map — entering a page turns its index lines into links on its own.
- Page 1 completed, so the book now runs 1–9 unbroken.

**What I built**

A contents page at `/chanting/contents` that reproduces the book's index *and* navigates it: each line carries English, the page in both `๑ / 1`, and buttons to the chant or the page.

**Why I did it this way**

Front matter is numbered `(๓๖)` in its own bracketed sequence — and the body has its own page 36. They're different pages of the same book, so they never share a route: a monk calling out a number always means the body.

The part worth keeping is what the data bought. I asked for it plainly:

> "Can we add button links for each chant in index so whe user clicks it directs them to the chant selected?"

Then when I completed page 1, **three more index lines became links with no work at all**. A picture of a list can't do that. Lines whose page isn't entered stay grey — because a link that goes nowhere is a worse lie than a visible gap.

**How We Did It**

1. Modelled front matter with its own numbering so `(๓๖)` and page 36 can't collide.
2. Transcribed all ten `สารบัญ` pages — 301 lines, 15 sections.
3. Stored **only** the printed Thai numeral and derived the integer from it, so the two can't drift across 300 rows.
4. Added English to every line, taking it from the chant itself wherever one exists.
5. Completed page 1 — which needed rubrics to sit *between* verses for the first time.

**Engineering Contribution**

- *Decisions made:* Front matter got its own sequence rather than negative page numbers — a number meaning something different from what's printed is the exact class of bug we'd spent the morning removing. The page and the chant are offered as **separate** buttons rather than one link, because sending someone to the page when they wanted the chant matters when a chant starts half way down.
- *Improvements made to generated code:* Two checks a machine *can* run on a hand-transcribed index: a contents never runs backwards (zero violations across 301 rows), and the middle pages each hold exactly 31 lines. Then an engineering pass found `_english_for` scanning every chant for every row — ~86,000 comparisons once the book's full — and the contents route rebuilding the whole page index twice per request. Both fixed; per-page build 0.8 ms → 0.1 ms.
- *Roughly how much was accepted as-is vs engineered on:* Direction and review. I specified the buttons, the English, and the back navigation, and asked for a live link to check it actually worked rather than taking "it's pushed" for done.

## 2026-08-07 — Exactly the same as the book

**TL;DR:**
- Pages 10–20 in: 30 → 44 chants, 509 → 644 verses, all 75 Sekhiya rules.
- One sentence of mine, said three times, settled three different arguments.
- Stage 1 finally has a tested validator. It found a defect in work already shipped.

**What I built**

Eleven pages. `check_batch.py` — Stage 1's counterpart to `apply_batch.py`, 14 checks, 57 tests. A `printed_number` layer so a list the book numbers renders numbered. Tests 141 → 217.

**Why I did it this way**

> "Should we carry on adding batches to the Digital Chanting Book? How many can we do at a time in this session?"

One standard, repeated, decided three different things:

> "Keep it all exactly as it is in the book"

> "Do 1. as recommended as long as in the app it remains exactly the same as in the book."

> "as long as it's exactly the same as in the physical book image then it is good"

Enter the นะโม twice rather than stub it. Move footnotes out of `source_printed`. Show the numbers the book prints — book layout was hiding every one. Then:

> "build the stage 1 validator"

> "Is there a way to make Claude code sessions short, simple and less technical so I don't get bogged down with all the text whilst developing projects?"

**How We Did It**

1. One page per batch: photograph, batch file, dry-run, apply, verify, commit, confirm live.
2. Built `check_batch.py` after three throwaway checkers gave false results in one afternoon.
3. Added `printed_number`; backfilled 83 verses across pages 12 and 15–18.
4. Brevity rule into `CLAUDE.md`, not a skill — a skill must be invoked; a standing instruction needn't be.

**Engineering Contribution**

- *Decisions made:* Split the four Sekhiya groups into separate chants rather than one — the book restarts its numbering at each group, and a chant numbers its verses uniquely. I later found the reasoning I'd been given was overstated (book view hides verse numbers, so only the study view was ever affected) and had it corrected rather than left standing. Kept `printed_number` separate from `number` instead of renumbering verses to match the book: the Dasadhamma Sutta opens with two unnumbered chanted lines, so the book's item 1 *is* the app's verse 3, and forcing them to agree would mean lying about one or the other.
- *Improvements made to generated code:* Three silent-data-loss gaps found in `apply_batch` by checking every key of the batch file had landed rather than trusting "it applied cleanly" — `printed_number`, `closing`, and `source_printed` on a continuation. One of my own checks was deleted as unfalsifiable: it hunted raw newlines inside JSON strings, which `json.load` makes impossible, so it could only ever fire on legitimate couplet breaks. Replaced with one that earns its place — `pali` and `pali_roman` must break in the same places. The new `printed_number` check was negative-tested against four realistic mis-transcriptions before being trusted.
- *Roughly how much was accepted as-is vs engineered on:* Direction, standard and review; I wrote none of the code. The standard was mine and it reshaped three separate mechanisms. Clearest evidence for why review matters: a backfill that stripped the indentation off 83 lines still imported cleanly and passed all 194 tests, because Python doesn't care about indentation inside a dict literal. Only the diff caught it.

---

## 2026-08-10 — How I'm working: AI agents and agentic workflows

*Not a build entry — a note to myself about the way of working that sits behind every session above.*

During this project, I have been using Claude Code with an **agentic development workflow** instead of simply asking AI questions and copying the answers.

Claude Code can explore the project files, plan tasks, edit code, use development tools, run tests, check the results, and find problems. I then review the work and make important decisions where human judgement is needed.

I have also been learning how **multiple AI agents or sub-agents** can be used to work on different parts of a project. For example, one agent can investigate a problem, another can make changes, and another can test and review the work.

Through this project, I have gained practical experience with:

- AI coding agents
- Multi-agent and sub-agent workflows
- AI working with existing code repositories
- Tool use and automation
- Planning tasks with AI
- Testing and reviewing AI-generated work
- Human approval and oversight

My role is to give the project direction, make important decisions, review the AI's work, and approve major changes. The AI handles much of the repetitive coding and testing work.

This has helped me understand how AI agents can be used to make software development faster and more organised, while still keeping a human involved to make important decisions.

---

## 2026-08-10 (later) — Seventeen pages, and three bugs that passed every test

**TL;DR:**
- Pages 34–50 in; the book runs 1–50 unbroken — 71 chants, 1,007 verses.
- Three silent-data bugs in the batch tooling, each of which imported cleanly and passed the whole suite.
- One sentence of mine set the standard for the session.

**What I built**

Seventeen pages — **21 new chants, 312 new verses**. Pages 34–37 finish the three Bojjhaṅga discourses to Mahākassapa, Mahāmoggallāna and Mahācunda. Pages 38–41 are the whole **Suat Jaeng** service: the Vinaya and Sutta in brief, then all seven Abhidhamma books — Saṅgaṇī, Vibhaṅga, Dhātukathā, Puggalapaññatti, Kathāvatthu, Yamaka, Mahāpaṭṭhāna — closing with จบสวดแจงเท่านี้. Then the Dhammasaṅgaṇī Mātikā's twenty-two triads (22) and the Vipassanābhūmi (23). Pages 44–50 turn to the blessing chants: Thawai Phon Phra, the eight **Jayamaṅgala** victory stanzas (24), Jayaparitta (25), Mongkhon Chakkrawan Noi (26), Kāladāna (27), Saṅgahavatthu (28), Mokkhupāya (29) and Ratanattayappabhāvasiddhi (30).

Also three fixes to `apply_batch.py`, a backfill of seventeen missing page blocks, and two new guards.

**Why I did it this way**

I gave the standard once and it kept deciding things:

> "as long as the app chanting pages are all exactly the same as the book then keep going, do pages 35 to 40"

It settled whether (ลากเสียง) stays inline, and how the Abhidhamma books split. When the app turned out to be showing less than the book prints, it decided that too:

> "yes do the PAGE_BLOCKS fix and backfill"

**How We Did It**

1. One page per batch: photograph, batch file, validate, dry-run, apply, test, render, commit, confirm live.
2. Found the page-break completion was appending duplicates instead of completing lines.
3. Found page blocks were never written at all — seventeen of them, on pages already shipped.
4. Fixed both, backfilled, added a regression test holding the app to the batch files.
5. Added a non-Latin scan last, on one condition:

> "only if it makes it better"

**Engineering Contribution**

- *Decisions made:* A footnote anchors at the page foot but a service closing anchors inline — my first version treated them alike and put page 41's จบสวดแจงเท่านี้ a whole chant too low. Structure for the Suat Jaeng came from the book's own contents rather than my reading of the page: it lists สวดแจง and พระอภิธรรมสังเขป as sections and each Abhidhamma book as an entry. Chant 27's footnote marker was left unpaired rather than matched to a plausible citation — a false reference in a book about the Dhamma costs more than a gap.
- *Improvements made to generated code:* Three bugs whose output passed everything — a completion regex that could never match the last verse (and a page-break stub is always the last verse), page blocks silently dropped, and a service closing skipped for the same reason. Each fix carries a guard: a duplicate-verse check that refuses to write, and a test that holds the app to what the photographs recorded. Both negative-tested. Two more caught mid-build: matching against raw source text called five pages "missing" because long blocks are stored as adjacent string literals, and keying on text alone would have dropped one of page 32's two footnotes. Also corrected a test that only passed because page 36 didn't exist.
- *Roughly how much was accepted as-is vs engineered on:* Direction, standard and review — I wrote none of the transcription. The clearest evidence for why review matters is that all three bugs shipped green: 473 tests passed with a verse present twice, and seventeen printed lines were missing from live pages with nothing anywhere reporting it.

---

## 2026-08-11 — Seven pages, and the difference between a verse and a colophon

**TL;DR:**
- Pages 52–58 in; the book runs 1–58 unbroken — 88 chants, 1,155 verses.
- Eight chants were inviting readers to chant "here end the verses on…" as a numbered line.
- My own migration script deleted five real verses before I caught it. The fix is now a test.

**What I built**

Seven pages. Pages 52–55 are one shape repeated three times, once per member of
the Triple Gem: a recollection as run-on prose, then an *abhigīti* hymn.
Page 55 gives the first printed title since 51 — พุทธะมังคะละคาถา, homage to the
arahants of the eight directions. Page 56 turns to สีลุทเทสะปาโฐ, and 57–58 hand
the service from the bhikkhus to the sāmaṇeras: the ten training rules, then the
ten grounds for expulsion.

Then the fidelity pass.

**Why I did it this way**

One sentence set the standard and then decided everything:

> "fix any issues so app chanting pages are exactly same as book pages then continue adding batches."

That is what sent me back to seven photographs rather than trusting the data. And
earlier, on punctuation the book does not print:

> "Keep app chanting pages exactly same as book pages."

**How We Did It**

1. One page per batch: photograph, batch file, validate, dry-run, apply, test, render against the photo, commit, push.
2. Audited every chant for a colophon held as a chanted verse — found eight.
3. Re-read all seven pages to place each colophon on the page the book prints it on.
4. Wrote the migration, checked the verse numbers, found it had deleted the wrong lines, reverted.
5. Rewrote it anchored on text instead of position, then pinned the cause with a test.

**Engineering Contribution**

- *Decisions made:* Pabbatopama's colophon goes on page 31, not 30 — its verses run to the foot of 30, and only the photograph could say. A footnote marker on page 57 with no footnote, and a footnote on page 58 with no marker, were left **unpaired** despite obviously belonging together: footnote numbers restart every page, and a false citation in a book about the Dhamma costs more than a gap. On page 56 I had used quotation marks to mark the Buddha's speech; the book prints none, so they came out — the shift from "train yourselves" to "we shall train" is the Pali's own signal and needed no help.
- *Improvements made to generated code:* Two `apply_batch` bugs that misreported rather than miswrote — `COMPLETED FROM p?` read a key that deliberately does not exist, and the `CONTINUES` count was taken around the removal only, so a batch that closed one chant and opened another reported `1 -> 0` of a file still holding one. Both now correct, and the second was verified in anger on page 55. Made the page-9 batch readable by the tool for the first time; the pin that recorded the defect became the general claim that no batch on disk is unreadable. Normalised 27 verse dicts that led with `'section'` where 1,128 lead with `'number'` — two shapes in one file, provably identical output, now one shape and a test.
- *Roughly how much was accepted as-is vs engineered on:* I wrote none of the transcription. The evidence for why review matters is my own migration: it imported cleanly, and left the numbering reading 21, 22, 24 with a chanted line gone. Nothing failed — I caught it by reading the numbers before rendering anything.

---
## August 2026 — Eight pages, and the checker that kept crying wolf

**TL;DR**

- Pages 61–68 of the chanting book went in: 8 pages, 7 new chants, 174 verses.
- I said the same thing five times without noticing, and it turned out to be the spec.
- Built the check nobody had written down — then it reported five faults, and the app was right all five times.

**What I built**

Eight pages, one at a time. Page 61's reflection on the requisites, page 62's
verses of dedication, page 63 — the first sheet in the whole book with **no
chant on it at all**, just the notes to the evening service. Then the long
special invitation running across 64 and 65, and the four festival offerings
starting at 66.

Then the tooling caught up. `check_batch` learned about `[…]`, the mark for a
line the page break cut in half. And I finally wrote down the check I'd been
re-improvising every single page.

**Why I did it this way**

I only spotted it reading back. Five times, in five different messages, I said
some version of the same sentence:

> "as long as what is added to app cahnting page remians exactly as is in the book"

> "continue as long as app chanting pages remain exactly as is in book."

> "so long as it is all consistent with the book as in the app"

> "keeping app chanting pages exactly same as book."

That wasn't nagging. That was the spec, and it decided every hard call this
session — including the one where the book prints the same chant twice, in two
different shapes, and I chose to carry both rather than let one page show text
it doesn't print.

**How We Did It**

1. One page per batch: read the photograph, write the batch file, validate,
   dry-run, apply, test, render against the photo, commit.
2. Hit the two-printings problem on page 61 and decided it: two entries, one
   per printing.
3. Found page 63 has no chant at all — an empty manifest, everything a block.
   That broke a count in `check_pages`, so I fixed it and pinned it with a test.
4. Wrote a `[…]` by hand on page 68 and realised nothing checked it.
5. Promoted the throwaway render check into the repo, and watched it be wrong
   three times before it was right.

**Engineering Contribution**

- *Decisions made:* **Two entries for one chant.** Dhātupaṭikūla is printed at
  both page 61 and page 207, and the entry already in the app has a Thai
  translation and thirty short verses where page 61 has neither. Merging would
  have put text on page 61 that page 61 does not print. **Kept `โอพารกา` on page
  64 and wrote `อาสาฬหะ` on page 66** — both are the ฬ/พ hazard my own photo map
  says a photograph cannot settle, but the second word this book spells with ฬ
  in two other places, so one is a reading and the other is a guess. **Scoped
  the new render check deliberately narrow:** it does not police which chant
  renders first or where a block sits, because `build_page_index` and
  `block_groups` already decide those and have their own tests. A second copy of
  a rule inside a checker is how a checker starts disagreeing with the thing it
  checks.
- *Improvements made to generated code:* `check_batch` now validates a cut line
  three ways — both chanted layers agree it was cut, the chant is listed as
  continuing, and the cut falls on the last verse. I proved all three passed
  silently first rather than assuming. New `scripts/check_render.py` walks the
  rendered page instead of counting hits on it, which is the fix for the two
  false alarms the throwaway versions kept producing: the book legitimately
  prints some lines twice, and short verses sit inside longer ones. 23 new tests,
  531 total.
- *Roughly how much was accepted as-is vs engineered on:* I wrote none of the
  transcription. The evidence is the render check: it reported 18 pages, then 9
  verses, then 5 verses as broken, and **every single one was the checker being
  wrong, not the app.** The last five were continuations — a line cut by a page
  break renders where it starts, not where it finishes. If I'd trusted the first
  red result I'd have "fixed" five pages that were already correct.

---
## 2026-08-17 — The database that was deleting itself

**TL;DR**

- The live site had been silently deleting every account it created. Now on Neon
  Postgres, proved by registering, redeploying, and logging back in.
- Freed the Dhamma AI mode — the line I'd already drawn for Meditation applied to
  the follow-up question too.
- Nine things looked fine while being wrong today — including my own test suite,
  which had been running against the live database, and an AI that had never
  remembered a single previous message.

**What I built**

Neon Postgres replaces a SQLite file that sat on Render's disk and was wiped on
every deploy. Progress moved out of the browser cookie into a JSON column, so a
level survives a new phone. Rate limits on the AI endpoints and on the sign-in
forms. Developer mode now switches off when no password is configured instead of
falling back to `changeme`. An `ai_usage` table that records every AI request, so
what the thing costs and how many people use it are answerable at all. A fair-use
ceiling of 150 messages a day on Pro, which was literally uncapped. A runbook
for operating the database, because the README is for reviewers and the journal
is history and neither says how to check what the app is doing right now. Fifty
tests, because none of this had any.

**Why I did it this way**

> "I offer dhamma education freely whilst monetising parts of the app as to make
> a small profit. I need to act ethically and morally, especially in a Buddhist
> sense - call me the Buddhist businessman."

Dhamma mode was Pro-only, so a reader could reach the free Theravada teachings
and then hit a paywall asking about them — the same line I refused to cross when
Meditation went back to free. The daily cap stays: that is the cost of running
the model, not a toll on the teaching.

One question saved a wrong turn:

> "Is the postgres migration necessary if I want to use Neon for the database"

Neon **is** Postgres. One job, not two.

**How We Did It**

Cost first (~0.2–0.3p a message), then the spend cap, then Neon, then progress,
then limits — each verified live before starting the next.

Eight things looked fine while being wrong. `.env` reported saved but was
untouched; the timestamp proved it. `DATABASE_URL` was saved in Render and
wasn't in the Environment tab. Render served two-hour-old code while reporting
itself healthy and Live. A probe returned HTTP 400 thirteen times because it
sent `username` where the route wanted `identifier` — a false negative, not a
verdict. A working feature looked broken because the test harness kept only the
first of two cookies. And I diagnosed auto-deploy as broken and committed a fix
for it, until:

> "It says auto deploy on commit"

It had been on the whole time. The push had simply missed a webhook.

The last two only turned up at the end, while adding rate limits to the login
form, and they are the worst of the set because they were **my own checks
lying to me**.

The test suite had been reading and writing the **live database**. The guard
that was supposed to stop it deleted `DATABASE_URL` — and `app.py` calls
`load_dotenv()` at import, which loaded the real one straight back. Ids 1 to 25
of the production `users` table were spent on test runs. Nothing failed: a suite
pointed at production passes exactly as happily as one pointed at SQLite, just
five seconds slower. I had even "proved" the guard worked by running the suite
with a deliberately broken connection string — it passed, and I read that as
success. It passed because dotenv had quietly swapped my broken string for the
real one.

And the rate limits were never off during tests either. `Limiter` reads its
enabled setting when it is *constructed* and keeps its own copy, so switching it
off afterwards is accepted and ignored. The config said `False`; the limiter
carried on limiting. It surfaced only when one limit got tight enough for a
single test file to exhaust on its own.

The ninth turned up last, and it had been true the whole time the chat has been
live. `session['session_id']` was **never set anywhere**. It was read with a
default, so every request minted a new one — and `ai_agent` keys its conversation
history on that value. The AI began from nothing on every single message.
"Conversation mode" was never a conversation. Its history dictionary also grew a
dead entry per message, and `/api/ai/clear` used a *different* default again, so
it cleared something nobody had.

Nothing would ever have reported that. Every reply reads perfectly sensibly on
its own; the fault is only visible across two messages, and no test asked. It
surfaced because a completely different feature — counting how many people use
the tutor — needed that id to hold still. **The bug was not hiding. It just had
nothing pointed at it.**

One more went the other way, and it is the reason the day ended well. After the
database was wiped I created my account again and the old 145 XP came straight
back. That looks precisely like a wipe that failed, so I said so:

> "it's dodgy"

It wasn't. The progress blob on a row created at 21:16 contained
`last_login: 2026-08-15`, two days before the account existed — so it could only
have come from my browser, not the database. A new account deliberately adopts
whatever XP the browser is carrying, so that trying the alphabet quiz before
registering doesn't cost you anything.

Right behaviour, no limit on it. A cookie of any age could resurrect itself onto
a fresh account — and on a shared monastery or library machine that means one
person's progress landing on the next person's account. Bounded to 12 hours now.

**Everything else today looked fine while being wrong. This one looked wrong
while being fine**, and it still needed the data to tell the two apart. Being
suspicious of a correct thing found a real bug that being satisfied would not
have.

Both of the earlier two hid behind a check that asserted on something *next to* the truth — a
config value beside the limiter, an environment variable that something else
would overwrite. That is the sharper version of the day's lesson, and worth
writing down properly: **a check placed next to the thing it means to test will
pass for the wrong reason, and I will believe it.** The guards added afterwards
assert on `limiter.enabled` and on the database URI the app is actually using,
because those are the values that decide behaviour.

**Engineering Contribution**

- *Decisions made:* One JSON column for progress rather than twenty-two real
  ones — none of it is queried, only ever read back whole for one user, and a
  column per field means a schema change per new counter. Rate limits keyed on
  `CF-Connecting-IP`, not `remote_addr`: Render serves through Cloudflare, so
  `remote_addr` is a proxy, and limiting on it would give every visitor on earth
  one shared quota — taking the site down rather than protecting it. Fixed the
  existing `_ensure_user_columns` instead of adopting Flask-Migrate; Alembic is
  the better long-term answer, but learning a new tool while changing databases
  is two risks, not one. Kept SQLite as the local fallback so development works
  offline and the suite stays fast.

- *Improvements made to generated code:* Login now lets the database win —
  `init_user_progress()` only fills gaps, so a leftover anonymous cookie would
  have beaten a real saved level. Excluded `is_developer` from the saved blob: a
  privileged flag should be re-earned with the password, not restored from
  storage. Filtered the authoritative keys on load as well as save, so the
  invariant doesn't rest on "nothing ever writes them". Replaced `hash()`-derived
  test usernames with `uuid4` after a run died mid-test and the leftover row made
  working code look broken. Mutation-tested the new tests — broke each feature
  deliberately and confirmed the right test failed. That is what caught the worst
  test of the day: my check that the `changeme` fallback was gone read a module
  constant, which is correct on any machine that has the password configured —
  every machine except the one the check exists for. Putting the bug straight
  back left it green. The credential logic became a small pure function so the
  unset case could be tested at all.

- *Sign-in limits, and who pays for them:* Login counts failed attempts only,
  not successful ones. These users are monks and expats who may share a single
  monastery or guesthouse connection, so charging them for signing in correctly
  would let ordinary use lock out everyone behind that connection. Brute force
  produces failures by definition. Signup is the deliberate exception and counts
  every attempt, because mass account creation succeeds each time and counting
  failures would never see it.

- *What the usage table stores, and what it refuses to:* Tokens and the model
  name, never a cash figure — prices move, and a number in pounds written into a
  row would freeze last year's price there forever. The money is worked out when
  the numbers are read. It also never stores the message or the reply: nothing in
  that table says what anyone asked, which matters most for the Dhamma mode,
  where someone asking about their own practice should not have it filed away.
  Blocked requests are logged too, with zero tokens. They cost nothing, but they
  are the entire answer to "do people who hit a wall subscribe?", and recording
  only successes would have quietly thrown that away.

- *Setting the Pro ceiling from a measurement instead of a guess:* Pro was
  literally uncapped. The number came from the row the new table had just logged
  — about 1,100 input tokens of system prompt against a 500-token reply cap, so
  0.285p at worst. That makes 150 a day £12.84 against £19.99 of revenue: still
  profitable if someone maxes it every day, and ten times the free allowance, so
  no one studying will ever meet it. Counted from the table rather than the
  session, because a cookie counter is exactly what a ceiling must not rest on.
  And the Pro plan had been advertising "no daily cap", so the copy changed too —
  a limit nobody will reach is still a limit.

- *Bounding a behaviour rather than removing it:* The tempting fix for the XP
  that came back was to stop new accounts inheriting anonymous progress at all.
  That would have thrown away the reason it exists — someone who tries the quiz
  and then registers should not be punished for registering. The fix is a limit,
  not a deletion: 12 hours, measured from a timestamp the session already
  carried and never updates, so it costs nothing to read. Anything undateable
  counts as stale, because inheriting progress of unknown age is the outcome
  worth avoiding.

- *A mutation that did not fail, reported anyway:* the check is written
  `if not user.progress and _anonymous_progress_is_stale()`. Removing the first
  half broke no test — for a returning user the saved progress is loaded over
  the top regardless, so the condition is currently doing nothing. It stays as a
  statement of intent, and would start mattering if that load ever became a
  merge. Worth writing down that it is not load-bearing rather than leaving a
  future reader to assume it is.

- *Roughly how much was accepted as-is vs engineered on:* About half. The Neon
  connection change went in close to first draft. The progress work took three
  corrections that only came from reading the existing code, and the test module
  was reshaped twice — the first version shipped dead placeholder code, the
  second proved flaky. The last stretch was almost entirely rework: the rate
  limits themselves were straightforward, and everything after them was fixing
  checks that had been passing for the wrong reason.

---

## August 2026 — Asking whether the XP system actually does anything

I built the XP and levels system back in December and never checked whether it
worked for the people who don't pay:

> Is the user XP system effective in the app? For example, how do users get XP
> when only Alphabet, Paiboon and Buddhism is free? Can other sections be
> unlocked with XP or do they require payment?

No, it turns out. Every free section is level 1, so the ~360 XP a free learner
can earn unlocks nothing. The levelling is real progression for Monk Mode users
and real pacing for subscribers — and decorative for everyone else. The audit
also found `/api/award_points`, which took the XP amount from whoever called it
and had no callers at all. One request could reach Level 10.

> How can we fix this? Especially so that a free user watches a progress bar
> fill up toward a reward that doesn't exist issue can be fixed.

**How we did it:** four commits in order — deleted the minting endpoint, made
locked sections name the paywall instead of only the level, added the earned
unlock (Level 3 opens one Thai Reader section, free and permanent, learner's
choice), then capped drill XP at 200/day. Earlier the same session,
`make paiboon free` moved the romanisation guide to the free tier, since the
free chanting and meditation pages already print Paiboon on screen.

**What I learned:** "is it working?" and "is it effective?" are different
questions. The code was fine. The system wasn't.

**Engineering Contribution**

- *Decisions made:* Chose the earned unlock over badges-and-streaks — the bar
  needed a real destination, not a consolation prize. Rejected wiring up
  `daily_login` (15 XP/day), which was sitting there dead and looked like an
  easy win: it would let someone reach the unlock in ~17 days of just opening
  the tab, buying content by showing up rather than by learning. A streak should
  pay a badge, not the currency that buys sections.

- *Improvements made to generated code:* The unlock shipped discoverable only by
  accident — you would learn you had one by chance-opening a locked section, and
  a spent one was invisible afterwards. Added it to the progress dashboard,
  which is where the bar it rewards actually lives. Monks are shown nothing,
  since they already have every section without paying.

- *Roughly how much was accepted as-is vs engineered on:* Code shipped as-is;
  the direction and the product decisions were mine. Backed by
  `prompts/xp-economy-audit/REASONING.md`.

- *Known-dead, deliberately left:* `max_level_access` is set on all three tiers
  and read nowhere — the docs advertise "Levels 6–7" for Basic and nothing
  enforces it. Noted, not fixed.

- *A change with no commit of its own:* `make paiboon free` landed inside commit
  `601624d`, whose message is entirely about dāna and Stripe. The reasoning
  lives in the prompt archive because the git history does not carry it.

---

## August 2026 — Three ways to order fried rice, and the label that meant two things

Every line on the Sentences page was written formally. Josh sent a photo of one
and asked:

> In sentence & conversation dropdown under Learn tab existing content is
> formal. Can we add informal to it, eg, (formal example) plus informal -
> kaao/w pat jaan krap or kaao/w pat nʉŋ jaan krap. Do this for all the existing
> content as to appeal to a wider audience. If there are any other formalities
> add those too.

I proposed "formal / everyday / casual" and got pulled up twice:

> What about monk formality? Is casual informal? Because there is neutral as
> well.

> Is neutral same as central Thai? Is casual same as how friends should speak to
> eachother? What's the difference between everyday and casual?

Both corrections landed. "Informal" is an umbrella, not a rung — and I had given
the middle rung two names in a single message. The second question found a real
bug: `FORMALITY_LEVELS['neutral']` was labelled ภาษากลาง, which means Central
Thai, a *dialect*. A politeness level and a dialect were sharing a name in
shipped code.

> What do we do then? I feel like we need to include Central Thai (standard
> Bangkok-region Thai) here as well as, in the entire app as the default Thai.

**How we did it:** renamed the level to ภาษาทั่วไป and added a card to the
Formality page separating the two axes — dialect is where the speaker is *from*,
formality is who they are *talking to*. Then built `thai_registers.py`: 108 of
the page's 130 lines gained a Neutral and/or Casual version, keyed by the formal
Thai string so app.py never changed shape. 123 new audio clips, two commits.

**What I learned:** the app already had a ten-level register system, Monastic
included. I nearly invented a parallel one before checking.

**Engineering Contribution**

- *Decisions made:* Monastic gets a note, not a casual rung — speaking to a monk
  swaps the vocabulary (ถวาย not ให้, นิมนต์ not ชวน) rather than sliding down
  the ladder, so a casual form there would model the one thing you must never
  do. Rejected adding a monastic row site-wide; it only applies where a monk is
  actually present. Keyed the variants by the formal Thai string rather than
  restructuring the content dicts — it leaves app.py untouched and lets a
  reviewer diff all the new Thai as one file. That trade has a cost, which is
  what the tests are for.

- *Improvements made to generated code:* Wrote `tests/test_registers.py` after
  the feature shipped, aimed squarely at the fragility the keying buys — edit a
  line in app.py to fix a typo and its rungs vanish silently, nothing raises,
  the page just teaches less than it did yesterday. Proved the test works by
  adding a single space to one line and watching it fail with the fix in the
  message. Also made the rung block a *sibling* of `.answer` rather than a
  child, so practice mode still hides it (via `~`) while tapping a rung's 🔊 no
  longer trips `revealAnswer`.

- *Roughly how much was accepted as-is vs engineered on:* The module structure
  and all the Thai are mine to answer for. The two-commit split, the
  sibling-combinator fix and the whole test file came after the first working
  version. Direction was Josh's throughout — without his two questions I would
  have shipped the wrong model twice.

- *Offered and declined:* Suggested also removing a dead `register_levels`
  parameter and fixing three identical `aria-label`s on the rung audio buttons.
  Josh took the tests only; both remain.

- *Raised and settled:* Whether to rename the Casual rung "Central". No — that
  would put a dialect name on a politeness rung, which is the same mistake as
  ภาษากลาง, in English. Colloquial stays available if Casual ever grates.

- ⚠️ *Unreviewed:* all 127 new Thai strings are drafts awaiting Josh's check and
  his teacher's Paiboon pass.

---

## August 2026 — The webhook that never reads the receipt number

I asked a narrow question about the Stripe webhook and told Claude not to touch
anything:

> Inspect the /stripe/webhook handler in app.py. Tell me exactly what fields it
> reads from checkout.session.completed, and whether it requires a real Checkout
> Session ID or can process a Stripe test fixture. Do not modify any files.

**What it reads.** Six fields, and one of them isn't really used. The route
branches on `metadata.kind` (dāna gifts get logged and nothing else) and
`metadata.addon` (the Instant Access Pass). `_sync_checkout_session` then reads
`metadata.user_id` (falling back to `client_reference_id`), `metadata.tier`,
`customer`, and `subscription` — which it re-fetches from Stripe to get the
status and period end. The session `id` appears only in log messages.

**The answer to the actual question:** no, it does not need a real Checkout
Session ID. The id is never a lookup key, never re-fetched, never stored. What
the handler actually gates on is the signature (`construct_event`, which checks
the HMAC *and* the timestamp window) and metadata that resolves to a real user
row. A stock `stripe trigger` fixture has empty metadata, so it logs
"missing user_id/tier" and returns 200 having done nothing.

**Three things worth writing down:**

- A fixture with a fake `subscription` id grants a **non-expiring** paid tier.
  `Subscription.retrieve()` fails, the exception is caught, `period_end` stays
  `None`, `_apply_subscription` skips `None` period ends, and `effective_tier`
  only expires a tier when `current_period_end is not None`. Every step is
  individually sensible; the chain isn't.

- No event-id dedupe. Replaying the same event re-applies it. Both sync helpers
  are idempotent so it's harmless today, but replay protection rests entirely on
  the signature's timestamp tolerance.

- `_find_user_for_stripe` does `int(user_id)` unguarded. A non-numeric
  `metadata.user_id` raises, 500s, and Stripe retries it. Only reachable by
  someone who can already sign payloads, so it's a robustness wart rather than a
  hole.

**What I learned:** "does it work?" and "what would it accept?" are different
questions, same as the XP audit. The webhook works fine for real Stripe traffic.
Asking what it would swallow from a fixture is what surfaced the three findings,
and none of them are visible from reading the happy path.

**Engineering Contribution**

- *Decisions made:* Kept this read-only on purpose. I could have had the `int()`
  guard fixed in the same breath, but a review that quietly turns into a commit
  stops being a review — I wanted the findings recorded as findings first, so the
  fix gets its own decision later.

- *Improvements made to generated code:* None — no code was touched this session.

- *Roughly how much was accepted as-is vs engineered on:* N/A. This is an audit;
  the output is the three findings above.

- *Left open, deliberately:* All three. The `int()` guard is the small one and
  the obvious next commit. Whether the non-expiring-tier chain needs changing
  depends on whether test fixtures ever hit a real database — worth deciding
  before it matters.

---

## 2026-08-19 — The rung with no label

Yesterday's work hung a Neutral and a Casual version under every line on the
Sentences page. Today Josh looked at it and asked:

> in sentences & conversation page shouldn't formal be next to neutral and
> casual everywhere?

He was right, and the reason it wasn't is a nice example of building something
while standing too close to it. The main line on that page *is* the formal rung
— that is the whole premise of the feature — but it was the only rung on the
ladder without a chip on it. Neutral and Casual were labelled, the thing they
were rungs *below* was not. So a three-level ladder read as two levels dangling
off an unnamed sentence, and the only place that said otherwise was a paragraph
in the intro card that a learner reads once and scrolls past.

**How we did it:** I offered two shapes. Either add a Formal row inside the
existing `registers_block` macro — one edit, covers all fourteen call sites
automatically, but prints the same Thai sentence twice on screen — or tag the
main line where it already sits. Josh took the second. A new `formal_tag()`
macro, fourteen one-line insertions, and a `formal` entry added to `LEVELS` in
`thai_registers.py` so the chip's wording and colour come from the same place as
the rungs beneath it rather than being hardcoded a second time in the template.
Two commits, `141f3af` and `f4bb534`, both live on Render within the hour.

**What I learned:** the label and the thing being labelled don't have to be
generated by the same code to belong in the same place. `formal` sits in
`LEVELS` but not in `ORDER`, so the module still produces exactly two rungs and
the template gets a third name to print. It also quietly gave a job to the
`register_levels` parameter I offered to delete last session and Josh kept.

**Engineering Contribution**

- *Decisions made:* The chip renders only when a line actually has rungs
  underneath it. About twenty lines on that page — the bare-verb table, the
  hesitation fillers — have no variants at all, and tagging those Formal would
  label a comparison that isn't being made. Also chose to tag the main line in
  place rather than repeat it inside the rung block: the duplicate would have
  been cheaper to build and worse to read.

- *Improvements made to generated code:* The first working version had the
  test fixture hand-writing a progress dict. Replaced it with one built from
  `init_user_progress()` and updated on top, so a new key added to that default
  later can't make the fixture the thing that breaks. Added an explicit
  assertion that the page actually opened — `/sentences` is gated behind Level 5
  and a subscription, and against the locked page every chip count is zero and
  every assertion passes for the wrong reason.

- *Roughly how much was accepted as-is vs engineered on:* Small change, and the
  shape of it was Josh's call from two options. The tests and the LEVELS
  placement came after the first version worked.

- *Left open:* Josh reports the pill isn't showing for him on the live site. I
  rendered `/sentences` from the deployed commit and the chip is present on all
  thirty-two example lines and all 115 register blocks, so the server is sending
  it — most likely a cached page in his browser, but unconfirmed at the time of
  writing. Worth settling before trusting it.

- *Noticed, not touched:* in male or female gender mode the aspect and question
  example loops ask for `aspect_examples.progressive.male` while the route has
  already resolved that to a list, so those sections render nothing at all.
  Pre-existing, unrelated to this change, and not mine to fix mid-session.

---

## 2026-08-19 (later) — The label that made an old inconsistency visible

Right after the Formal chip shipped, Josh asked:

> We need to add polite particle to sentences & conversations to either
> neutral, casual or formal whichever one suit polite particle the most.

The direct answer is Neutral. Formal carries ครับ/ค่ะ too, but what *defines*
Formal is the full pronoun, and Casual is defined by dropping the particle.
Neutral is the only rung whose whole identity is "pronoun gone, particle kept".
There is no Polite level in the app's ten-level system either — it runs monastic,
royal, obsolete, literary, technical, formal, neutral, casual, impolite, vulgar —
so this was never a missing level. It was a missing particle.

Then I counted, and the counting is the interesting part. Of the 108 lines with
rungs, **25 had no polite particle at all** — including nineteen that the page
had just started tagging **FORMAL**. ผมกำลังกินข้าว has a pronoun and no ครับ.
By the module's own definition that is not formal. Their Neutral rungs had no
particle either, which by the same one-question test made them casual. The chip
did not create that problem; it made a year-old inconsistency impossible to
ignore, which is the argument for labels over prose.

> Should we add it to every formal and neutral?

**How we did it:** yes, to those nineteen lines and their eighteen neutral rungs,
in `app.py` and `thai_registers.py` in the same commit — the variants are keyed by
the exact formal Thai string, so editing one file without the other silently
detaches every rung on the page. Paiboon and the `breakdown` strings updated with
each. Forty new edge-tts clips. Two commits, `0c13ca9` and `e082d40`, live on
Render within twenty minutes.

**What I learned:** four of the forty clips came back zero-byte from a failed
edge-tts call, and the next run counted them as "already present" and skipped
them. A file existing is not the same as a file being right, and the generator
only checks the first thing.

**Engineering Contribution**

- *Decisions made:* The three เขา lines split into male and female entries. A
  third-person sentence carries the particle of whoever is *speaking*, not of the
  person spoken about, so one shared entry could not serve both example lists.
  Monastic lines keep no particle — a monk says เจริญพร — and all 95 casual rungs
  stay bare, because dropping the particle is the entire definition of casual.
  Adding one there would have collapsed Casual into Neutral.

- *Improvements made to generated code:* Found `แบบว่า...` carrying a "casual"
  rung identical to the line itself, with a note reading *already casual* — so
  the new chip was tagging a filler as formal. Converted it to a warning-only
  entry, which renders the note and no chip. That in turn broke my own
  one-chip-per-block test, correctly: rewrote it to count chips against stacks
  that actually have rungs, and added a second test pinning the warning-only
  case. Gave the macro's chip a `reg-tag-main` class so the intro card's
  hand-written ladder stays out of the count.

- *Roughly how much was accepted as-is vs engineered on:* The direction was
  Josh's question. The audit that turned "add the particle" into "nineteen lines
  are mislabelled" is the work, and so is deciding where *not* to add it.

- *Left open:* the audio generator still treats a zero-byte MP3 as done. I
  deleted and regenerated the four bad clips by hand; the failure handling is
  unchanged and will do it again.

- ⚠️ *Unreviewed:* all the new Thai is a draft awaiting Josh's check and his
  teacher's Paiboon pass.

---

## 2026-08-19 (evening) — The permissions were right; the shop window was lying

**What I built.** I sent the app to a European friend who visits Thai temples and
got back an objection I did not expect:

> The main problem is anyone who is not Thai seem to be getting offended and
> upset perhaps feeling left out or excluded

Before proposing anything, I had the access rules read. `theravada`,
`meditation`, `chanting` and `paiboon` were already free, level 1,
`requires_alphabet: False` — the comment beside `chanting` literally says *"you
do not need to read Thai to chant along."* The app had granted what she wanted
all along. The home page just said the opposite: *"pass the quiz to unlock the
site."*

**How we did it.** Audited the gates, then fixed the copy to match: two new free
pages (`/dhamma-and-culture`, `/practising-anywhere`), a "What are you here to
learn?" chooser with four equal doors, and a wording pass. Then `/register`
turned up crashing — `REGISTER_LEVELS` had never existed in *any* commit, and the
access gate meant only paying learners ever saw the 500. Redirected it, then
wrote the nine registers.

**Engineering Contribution**

- *Decisions made:* Kept every piece of Thai cultural material — the objection
  was never to its presence but to its apparent compulsoriness.
  `/practising-anywhere` names **no country at all**, built from the five
  precepts, the three bases of merit and the Sigālovāda's six directions, which
  are universal by construction. Skipped renaming `register_levels.py` despite
  its collision with `thai_registers.py`: another session had `app.py` open and a
  rename touching imports was the wrong risk today.

- *Improvements made to generated code:* Twice I sent the wording back and both
  times it changed the approach, not the phrasing. First:

  > practising the precepts in Britain? How about Britain and other places around
  > the world? Isn't this supposed to be universal?

  Naming my own country instead of Thailand is the same move with a different
  flag. Then, after "foreigner" became "non-Thai":

  > Is there a better name than non-Thai?

  Politer, structurally identical — both define a reader by not belonging. The
  fix was noticing the sentences already said "you", making the label redundant.
  Then a self-inflicted one: the nine register colours I picked render as
  white-on-colour badges, and **six of nine failed AA** (saffron 2.13:1, gold
  2.10:1) — on a site with a Learning Support panel for visual stress. Darkened
  in HLS, hue and saturation untouched, with a test pinning it.

- *Roughly how much was accepted as-is vs engineered on:* The structure and the
  diagnosis went in unchanged. Every piece of language went through my
  corrections, and the accessibility bug was mine to find and mine to have
  caused. Backed by `prompts/inclusive-positioning/REASONING.md` and
  `prompts/register-levels-draft/REASONING.md`.

- *Lesson:* **Renaming a category is not removing it**, and a gate that hides a
  crash from everyone except the people who paid is worse than one that crashes
  for everybody.

- ⚠️ *Unreviewed:* the nine registers are a draft awaiting my teacher.

---

## 2026-08-19 (night) — Two of the five were noes

**What I built.** I had five ideas for loosening the free tier and no way to
tell which were generous and which were just expensive. I asked for a verdict on
each, and put the sales argument in with the question:

> The whole curriculum outline, visible to everyone people pay more readily when
> they can see what they're buying.

Three shipped, two were refused. The refusals matter more: freeing the reading
sections would have gutted the tier they *are*, and cutting the AI allowance
would have saved pennies at the cost of the best free thing on the site.

**How we did it.** Five features, all live. A Paiboon lookup that searches 1,217
reviewed entries rather than transliterating; a public curriculum outline built
from the gated routes; the Dhamma given its own AI allowance; a free Survival
Thai section; and the alphabet prerequisite narrowed. Then two questions of mine
turned out to find more than the answers did:

> would you agree that survival mode is right to be placed in Tour Guide page or
> not?

> is it right for Alphabet page to be free?

**Engineering Contribution**

- *Decisions made:* Refused two of the five. Shown three possible builds for
  the lookup, I closed it to one:

  > Yes only do the first one leave the others out of it

  Corpus search, not live AI and not a rule-based engine — a beginner cannot
  tell a hallucinated tone mark from a real one, and in Thai a wrong tone is a
  different word. Excluded the Yaitron dictionary's 4,894 pairs: it *is* the Pro
  feature, and its romanisation was machine-generated, never checked. The Dhamma
  allowance began as three words on a list — *"Small free Dhamma allowance"* —
  and came back as a bug rather than a feature, so I asked what it actually
  meant:

  > What is the Dhamma quota split?

  Funded it **on top of** the tutor's 15 rather than reserved out of it: nobody
  should lose something so the site can keep a promise it had already made.
  Built Survival Thai as its own section rather than folding it into Tour Guide,
  which is paid, level 4 and alphabet-gated — I asked for that spec as
  *"greetings, numbers, food, directions. Finishable, genuinely useful."* and it
  is now enforced by a test that fails outside 30–70 phrases. Changed only
  Culture of 15 candidate sections, and left the Instant Access Pass alone.

- *Improvements made to generated code:* Nothing reworked at code level while
  building. The quality pass afterwards found three things, all self-inflicted:
  a compatibility shim in `ai_limits_status()` justified by a comment that was
  already untrue when it shipped — its only reader moved to the new shape in the
  same commit; a module docstring in `paiboon_lookup.py` describing one fold when
  two shipped, and the undocumented one is what makes "sawatdee" findable at all;
  and a filter dropping strings containing `/` with a comment explaining only the
  other half of what it did. On verification, with another session editing the
  same clone, I asked for:

  > do what is safest and most effective.

  which is how the commits came to be checked out into a throwaway `git
  worktree` and tested alone — proving a failing test was theirs without
  touching their files.

- *Roughly:* shipped as-is on code, with the direction and the product decisions
  mine. Full reasoning per feature in `prompts/free-tier-review/`,
  `prompts/paiboon-lookup/`, `prompts/dhamma-ai-allowance/`,
  `prompts/survival-thai/` and `prompts/alphabet-gate-audit/`.

**What I learned.** My two best contributions today were questions, not
instructions. Asking whether Survival Thai belonged on Tour Guide stopped free
content landing behind a £9.99 paywall. Asking whether the Alphabet should be
free led to the finding underneath it — that 15 sections taught entirely in
romanisation still demanded 35 of 44 consonants first, and the pricing page
carried a flag reading "pass a quiz to see our prices".

- 📉 *On the verbatim ratio:* about 9% of this entry is quoted from me, well
  under the 40% I aim for. That is honest rather than lazy. My inputs today were
  short questions and short instructions — the leverage was in *which* question,
  not in the volume of words. Raising the ratio would have meant deleting the
  reasoning that explains the decisions, or padding with my approvals, and both
  are worse entries. Recorded here rather than quietly massaged.

- ⚠️ *Unreviewed:* Survival Thai's 50 phrases are a draft awaiting my teacher.

---
