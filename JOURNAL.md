# Build Journal — Thai Language & Culture Learning App

This is the honest record of building my **first web app** — a Thai language and culture learning site — mostly with AI help, as a complete beginner. It's a learning project and a portfolio piece, not a finished product. I've kept the wins and the mistakes in, because the mistakes are where I actually learned.

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
