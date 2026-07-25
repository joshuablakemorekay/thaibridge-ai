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

**TL;DR:** All 44 consonants now show the thing they're named after — ก is "gɔɔ gài, chicken", so ก gets a chicken.

**What I built or did**
Added a picture to every letter in four places: the chart tiles, the detail strip, the flashcard's reveal side, and a new quiz round that asks *"which letter is this the picture for?"*

**Why I did it this way**
Two kinds of picture, chosen by context. The chart shows 44 tiles at once, so that uses emoji — no downloads, and page weight is exactly what crashed this page's renderer before. The strip, flashcard and quiz show one letter at a time, so those can afford a real image.

**How it works**
Pictures are drop-in: name a file after the letter's slug (`kor-kai.webp`), drop it in `static/img/consonants/`, and it appears. No code to edit — the same trick the phrase audio already uses. Until a file exists, the emoji stands in.

**What this means for the app**
A picture is a memory hook. Recognising a chicken is far easier than recalling "gɔɔ gài" cold.

**What I learned**
Twelve meanings have no honest emoji — a cattle goad, a pot lid, Montho from the Ramakien. Rather than fudge it, I flagged those and kept them out of the picture round: guessing a letter from a vaguely-right picture is an unfair question. Add a real photo later and the letter rejoins automatically.

I also broke something and caught it by testing. I'd set the images to "lazy load" — a trick for pictures far down a long page. But here exactly one image is built at the moment it's shown, so lazy could only ever delay the thing being looked at. In a background tab it never loaded at all. **The fix for a slow page isn't always right for a fast one.**

**How We Did It**
1. Read how the page was built first — one table, `thai_consonants.py`, feeding chart, flashcards and quiz alike.
2. Chose emoji vs real images per place, based on how many appear on screen at once.
3. Added an emoji to all 44 letters, marking the twelve that are only approximate.
4. Built the drop-in folder so pictures can be added later without touching code.
5. Added the quiz's picture round, excluding the approximate twelve.
6. Tested in a real browser — including with a deliberately wrong-shaped image, which is how I caught the lazy-loading mistake.
7. Pushed, then confirmed the live site was actually serving the new version.

**References / Conversations**
Claude Code session, 25 July 2026. Commits `c9a2bc9`, `c9cd015`.

---

## 25 July 2026 — Drawing 44 letters instead of downloading them

**Type:** Feature

**TL;DR:** The alphabet pictures are real drawings now, not emoji — 44 SVG icons in the site's own colours, 30 KB for the whole set.

**What I built or did**
Replaced the emoji fallback with a hand-drawn icon set on the flashcards, the chart's detail strip and the quiz's picture round. The chart's 44 tiles still use emoji, on purpose.

**Why I did it this way**
I wanted photographs and couldn't have them. Every stock photo needs a licence that holds up in a public repo, and 44 downloads is page weight this page can't afford. Drawing them solved both at once: nothing to license, and the whole set is smaller than a single photograph. SVGs are shapes described in code, so they stay sharp at any size.

**How it works**
No code changed at all. The drop-in lookup I built earlier finds a picture by filename, so adding 44 files *was* the whole job.

**What this means for the app**
A side effect I didn't have to build: the twelve letters whose emoji was only approximate — a pot lid, a cattle goad, Montho — now have unambiguous pictures, so they rejoined the quiz's picture round by themselves. Picture questions went from about 9 a quiz to 14.

**What I learned**
When you can't source something, make it — and the constraint often picks the better answer anyway. Vectors beat photos here on every measure that mattered.

Also: judging your own work is part of the work. I laid all 44 out side by side and four were bad — the plate read as a target, the cymbals as leaves, the horse as a blob. I only saw it because I viewed them together at the size they'd really be used.

**How We Did It**
1. Ruled out stock photos on licensing and page weight.
2. Drew six easy objects first and looked at them before committing to the idea.
3. Tested the hard case next — animals — because that's what would decide it.
4. Drew the remaining 35, flagging eight culturally specific ones for review.
5. Laid all 44 on one page at real size and redrew the five that failed.
6. Checked the live site returned 404 before pushing and 200 after, so "live" meant something.

**References / Conversations**
Claude Code session, 25 July 2026. Commit `0c398ac`.

---

## 25 July 2026 — When the reason for a rule expires

**Type:** Decision

**TL;DR:** The chart tiles now show the drawn icons too — because the reason they didn't had quietly stopped being true.

**What I built or did**
Switched the 44 chart tiles from emoji to the same drawn icons the rest of the page uses. The trigger: I spotted that ฉ (cymbals) was showing a drum and พ (a footed offering tray) a trophy.

**Why I did it this way**
No emoji swap could have fixed those two — Unicode has no cymbals character and no offering-tray character. They can't be said in emoji at all. The drawings say them exactly.

And the chart's emoji rule had expired without anyone noticing. It existed because 44 pictures at once was the page weight that crashed this page's iOS renderer — but that was a rule about *photographs*. The drawn set is vector art: 30 KB for all 44, less than one photo.

**How it works**
One line in `buildChart`. Every tile's picture sits in a fixed 32px slot shared by the icon and the emoji fallback, so a missing or slow icon can't reflow a 44-cell grid.

**What I learned**
A design rule is only as good as the fact underneath it, and facts change. The dangerous part is that a rule outlives its reason **silently** — nobody re-checks. So I wrote the condition into the code and the folder README: if these ever become photographs, the chart goes back to emoji. A rule worth keeping is worth writing down with its expiry condition.

**How We Did It**
1. Checked where emoji still appeared — only the chart tiles.
2. Established that no exact emoji exists, so the drawings had to be the fix.
3. Measured the real cost: 30 KB for 44 vectors, against a rule written for photos.
4. Gave every tile a fixed 32px slot so nothing can reflow the grid.
5. Deleted an icon and reloaded, proving the emoji fallback still catches it.
6. Verified live before calling it done.

**Amended later the same day**
I looked at the result and narrowed it. Emoji are the right default for that
chart: 44 are on screen at once, they cost nothing to load, and they are
*designed* to be legible at small sizes — which a drawing shrunk to 32px is
not. So the chart went back to emoji, keeping the drawing only for the two
letters emoji genuinely cannot express: ฉ ฉิ่ง and พ พาน.

I had swung from one blanket rule to the opposite one. The real answer was
narrower than either: **emoji unless no emoji exists.** That now lives in the
data as a `no_emoji` flag rather than a list of letters buried in the code, so
marking another letter later is a one-line change.

So there are two lessons here, not one. The first still stands — a rule outlives
its reason silently. The second is the corrective: **noticing that a rule has
expired is not a licence to throw it out.** The reason the chart used emoji (44
things on screen at once) had not gone away; only the part about file size had.
Replace an expired rule with a narrower one, not with nothing.

**References / Conversations**
Claude Code session, 25 July 2026. Commit `8ab1cbe`, then `c229e0b` for the
correction.

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
