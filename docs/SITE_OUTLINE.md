# Site Outline — Thai Language & Culture Learning App

> **What this is:** the written content plan for the site — the book's *"Step 3: Create an outline"* (Figure 1-1).
> It lists every page, what each page is *for*, the key content it holds, and which layout template it should use.
> Made **content-first**: we decide *what each page says and does* before worrying about colours, fonts or fancy styling.

---

## The site in one sentence

A friendly, culture-rich site for learning Thai language and Theravada Buddhism — with an AI tutor, a dictionary, structured lessons, and a meditation timer.

---

## Layout templates (the four "shapes" a page can take)

Instead of forcing one layout onto every page, each page uses the template that fits its **job**. There are four:

| # | Template | Looks like | Used when a page needs to… |
|---|----------|-----------|-----------------------------|
| **L** | **Landing** | Big welcome banner + a few feature cards, full width | …welcome visitors and point them somewhere (the front door) |
| **C** | **3-column content** | Sidebar (section menu) · main reading area · right column (search / progress) | …teach reference material that has related sub-pages + handy extras |
| **S** | **Simple centered** | One clean column down the middle | …show a small amount of info or a short form |
| **T** | **Full-width tool** | Edge-to-edge interactive area, no sidebars | …give an app-like tool room to breathe |

---

## The content outline

### 🏠 Home  — template **L**
- **Purpose:** welcome visitors and send them to the right starting point.
- **Key content:** hero banner (what the site is + a "Start learning" button), 3–6 feature cards (Learn, Dictionary, AI Tutor, Buddhism, Meditation), a short "why this site" line.
- *Note:* this is the one page that should **not** use the 3-column layout — a front door directs, it doesn't navigate.

### 📚 Learn  *(the heart of the site — these all share template **C**)*
A shared **sidebar** lists these sub-pages; a shared **right column** offers dictionary search + a "your progress" card.

| Page | Route | Purpose / key content |
|------|-------|------------------------|
| Alphabet | `/alphabet` | The 44 consonants + 32 vowels, with a completion requirement |
| Vowels & Syllables | `/vowels_syllables` | How Thai vowels and syllables work |
| Paiboon Romanization | `/paiboon` | Your custom Paiboon+ romanization system explained |
| Grammar Guide | `/grammar` | Core grammar rules and patterns |
| Formality Levels | `/formality` | How politeness/formality changes word choice |
| Gender Guide | `/gender-examples` | How the speaker's gender changes speech (with a male/female toggle) |
| Sentences & Conversations | `/sentences` | Example sentences and dialogues |
| Vocabulary | `/learn` | 6 themed categories, 20 words each *(✅ wireframe already piloted here)* |
| Lessons | `/lessons` → `/lesson/<id>` | Structured, ordered lessons |
| Tour Guide Thai | `/tour-guide` | Practical travel/everyday Thai |
| Business Thai | `/business-thai` | Workplace and formal-setting Thai |

### 🎭 Culture  — template **C**
- **Purpose:** Thai customs, etiquette and cultural context.
- **Key content:** culture articles; sidebar can reuse the Learn menu or a Culture menu.

### ☸️ Buddhism  *(template **C** — sidebar = this Buddhism menu)*
| Page | Route | Purpose / key content |
|------|-------|------------------------|
| Theravada Dharma | `/theravada` | Suttas, Abhidhamma, Vinaya — core teachings |
| Pra Kru Bob: Overview | `/bob-buddhism-overview` | Introduction to the teacher's perspective |
| Pra Kru Bob: On Fear | `/bob-fear-article` | A longer-form article |
| Meditation | `/meditation` | **template T** — Samatha & Vipassana timer (needs full width) |

### 📕 Dictionary  — template **T**
- **Purpose:** look up Thai ↔ English words (Yaitron dictionary).
- **Key content:** big search box + results table; full width so results have room.

### 🤖 AI Tutor  — template **T**
- **Route:** `/chat` — **Purpose:** chat with the Claude-powered tutor (6 modes).
- **Key content:** full-width chat window; no sidebar so the conversation has space.

### 🏆 Progress  — template **S**
- **Route:** `/progress` — **Purpose:** show the learner their level, XP and achievements.

### 👤 Account  *(template **S** — short, centered)*
| Page | Route | Purpose |
|------|-------|---------|
| Sign up | `/signup` | Create an account (demo-only for now) |
| Log in | `/login` | "Coming soon" placeholder — real auth is a later goal |
| Developer Login | `/developer-login` | Password-gated developer/admin view |

### ⭐ Premium  — template **S**
- **Route:** `/premium` — **Purpose:** explain the 3 subscription tiers (demo pricing).

### 🧩 Practice / Exercises  — template **T**
- **Route:** `/exercise/<category>` — **Purpose:** interactive quiz for a vocabulary category; full width for the activity.

### 📄 Footer pages  *(template **S** — simple and honest)*
| Page | Route | Purpose |
|------|-------|---------|
| About | `/about` | What this project is and who made it |
| Contact | `/contact` | How to get in touch |
| Privacy | `/privacy` | What data is (and isn't) collected |

---

## Status: what's done vs. what's next

- ✅ **Vocabulary (`/learn`)** — 3-column layout piloted and (after the CSS fixes) now rendering correctly.
- ⏳ **Other Learn pages** — built, but not yet switched to the shared 3-column layout.
- ⏳ **Home** — still on the old layout; needs its own proper **Landing** design.
- ✅ **About / Contact / Privacy / Login** — exist as simple pages.

**Suggested next step:** roll the 3-column layout out to the other Learn pages (where it clearly fits), then give Home its own Landing layout as a separate small project.

---

*This outline is a living document — update it whenever a page's job or content changes.*
