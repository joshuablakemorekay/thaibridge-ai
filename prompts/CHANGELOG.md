# Prompt Changelog

Chronological record of prompt creation and refinement. Newest entries at the top.

Each entry follows this format:
- **Date** — what changed and why

---

## critique-to-product-decision

### 2026-08-20 — v1
**Change:** First version. Asks what a hostile critique of Thai Buddhism does to the app *as a product* — for both revenue and free teaching — rather than whether the critique is correct, and ends "suggest any improvements I could make if any at all".
**Reason:** The two previous rounds had both ended in defensive front-page copy answering the same person, neither of which made the app better at teaching Thai or at earning. Asking for the product consequence separates "is this argument right?" from "should this change what I ship?".
**Impact:** Most of the critique changed nothing — the critic is not in the paying segment, and removing the Thai cultural material would cost the differentiator. One part survived: the Buddhist content presented the tradition only at its best. `d91a06a` added three Vinaya rules to `/theravada` (the money rule, eating at the wrong time, and the ไวยาวัจกร lay steward) with a note on how the tradition judges itself. `1e77b07` added a pedagogy line to `/dhamma-and-culture`. A justification page for the app's Thai focus was considered and **refused** — the position was already made three times over, and a fourth would have been the third piece of defensive copy in a week.

---

## hero-copy-rewrite

### 2026-08-20 — v3 → v4
**Change:** Tightened the hero from roughly 125 words to 95, and added two rubric criteria for what the round found: `states_the_promise_once` and `does_not_echo_the_strapline`.
**Reason:** An outside critique called the note overdone and was half right — it stated "you don't have to take on Thai culture" five separate ways, and its closing line restated the strapline three lines above it. The other half of that critique proposed a 28-word replacement that dropped the culturally-neutral branch, which is the exact commitment round 1 was spent restoring.
**Impact:** `064a055` shipped the tightened hero with both branches intact; `016cc01` brought `/dhamma-and-culture`'s closing card into line, since it still carried the wording round 1 rejected. The recorded lesson: the commitment survived because `tests/test_dhamma_open_to_all.py` asserts it, not because anyone remembered it. Also found that those assertions match exact substrings of the rendered HTML, so wrapping a guarded phrase across two template lines fails a test the copy has not actually broken.

### 2026-08-19 — v1 → v3
**Change:** First version was a one-line critique of the live hero — *"This doesn't sound very convincing."* v2 added the cultural-freedom line and had three proposed wordings rejected in turn. v3 is the author's own text, with the constraints that killed each rejected draft written back into the prompt.
**Reason:** The hero read *"Two subjects, side by side"* — a description of the site's filing system rather than a promise to a visitor, built from hedges that made two subjects sharing a page sound like an apology.
**Impact:** Four commits, all live. `95635ef` moved the strapline into the `<h1>` and replaced the subtitle with one naming the four doors; `9b234c4` normalised "Theravada" across all 26 mentions; `9cf3302` restored the culturally-neutral option to the front page in the author's own words, borrowing `/dhamma-and-culture`'s phrasing so the two pages agree; `74341c6` added the `/about` card **On "Thainess" — a personal note**, shipped verbatim at the author's explicit instruction after concerns were raised and declined. The recorded failure: an objection to the phrase "follow no culture at all" was allowed to delete the option it described, and only a direct question caught it.

---

## alphabet-gate-audit

### 2026-08-19 — v1
**Change:** First version — *"is it right for Alphabet page to be free?"*, with instructions to answer from counted data rather than instinct, then to ask the harder question underneath: is the prerequisite drawn in the right place? Measurement required for the borderline pages, and the Instant Access Pass fenced off as settled.
**Reason:** The question as asked has a one-paragraph answer. Fencing off the add-on stopped the audit spending itself re-litigating a decision already made.
**Impact:** All 21 paid sections carry `requires_alphabet`, so freeing the Alphabet is structurally forced, not generosity. Sorting the 21 found three that genuinely need the script, three that are dead or unbuilt, and 15 taught wholly in romanisation — Culture measured at 31% of strings containing any Thai across ~10,000 characters. Two changes shipped in `d99c524`: Culture freed from the gate (level and tier untouched), and a dead `requires_alphabet` removed from the pricing page, where it read as "pass a quiz to see our prices".

---

## survival-thai

### 2026-08-19 — v1
**Change:** First version — *"One full survival module — greetings, numbers, food, directions. Finishable, genuinely useful."* Later extended with the placement question *"would you agree that survival mode is right to be placed in Tour Guide page or not?"* and, after shipping, with making it findable.
**Reason:** The free tier was Buddhism plus an alphabet chart, so someone who came to speak Thai could finish nothing without paying.
**Impact:** 50 phrases in four sets at `/survival` (`e298ab9`), free and `requires_alphabet: False` — the only language page reachable knowing nothing. The placement question is what kept it out of Tour Guide, which is basic tier, level 4 and alphabet-gated. Audio completed in `9c0c77e` (26 new clips, 51/51). The home page gap was caught last: the language card still said *"Starts with the 44 consonants"*, the exact wall the section routes around — fixed in `0492089`, where Survival Thai became step 1 of the language path.

---

## dhamma-ai-allowance

### 2026-08-19 — v1
**Change:** First version — began as *"Small free Dhamma allowance"* among five giveaway proposals, and was reframed as a check of a stated principle against the gate that actually runs. v2 added the constraint that no fix may take something away from anyone.
**Reason:** The position was already written down in a comment above `FREE_AI_DAILY_LIMIT`. Nobody had put it beside the gate underneath it.
**Impact:** Found that `/api/ai/chat` compared one shared counter without reference to `mode`, so a learner who spent the day on vocabulary was refused a question about the precepts. Fixed in `be35854` by giving the Dhamma its own 5 a day *on top of* the tutor's 15 rather than reserved out of it. Both refusal messages rewritten, and the upsell removed from the Dhamma hint entirely. The tests caught a flaw in the fix itself: the first `AI_POOLS` copied limit values in, silently becoming a second source of truth that broke an existing `monkeypatch`.

---

## paiboon-lookup

### 2026-08-19 — v1
**Change:** First version asked what a Paiboon lookup *can* be before proposing a build, and specifically what happens when each option is wrong. v2 narrowed it to one: *"Yes only do the first one leave the others out of it."*
**Reason:** The obvious reading of "lookup tool" is a transliterator. There isn't one in this codebase and there shouldn't be — every romanisation shipped was hand-written or generated offline and reviewed.
**Impact:** 1,217 entries searchable at `/paiboon` (`e368522`). Live AI was rejected because a beginner cannot catch a wrong tone mark, and a wrong tone in Thai is a different word. Three folds handle the spellings beginners actually type — tone marks, vowel length, ee/ii and oo/uu, RTGS kh/ph/th, and Paiboon's bp/dt. Two ranking bugs found by testing against real queries: an incidental substring outranking ช้าง, and fuzzy noise padding a good result set. The Yaitron dictionary's 4,894 pairs were deliberately excluded — it is the Pro feature, and its romanisation is unreviewed.

---

## free-tier-review

### 2026-08-19 — v1
**Change:** First version — five free-tier proposals judged do-or-don't, with instructions to ground every answer in `SECTION_REQUIREMENTS` and `SUBSCRIPTION_TIERS` rather than the marketing copy, and to hold each answer to any principle already stated in the code.
**Reason:** *"people pay more readily when they can see what they're buying"* — the sales argument arrived with the questions and shaped the curriculum outline that came out of them.
**Impact:** Three built, two rejected. The reading system stayed paid because those sections *are* the Basic tier; the 15-message AI cap stayed because the code's own costing makes a reduction worth pennies. The outline shipped as `curriculum.py` (`9505e4a`), assembled from the gated routes rather than hand-listed, with a startup assertion that fails the import if a section is neither advertised nor excluded for a written-down reason. Building it that way immediately found three sections priced but never built, and that Pro adds one page against Basic's sixteen.

---

## register-levels-draft

### 2026-08-19 — v1
**Change:** First version — asks for the nine formality registers as a reviewable draft: *"draft the nine register levels for me to review"*, with instructions to derive the field contract from the consuming template first, ground the romanisation in the app's existing Paiboon index, and flag uncertainty per register.
**Reason:** `templates/register.html` had been in the repo since the first commit with no data behind it. The last three words of the request set the shape: the deliverable was something a Thai teacher could check, not finished content.
**Impact:** Nine registers and 29 examples in `register_levels.py` (`e921ad4`). Found that `REGISTER_LEVELS` never existed in any commit, so `/register` had raised `NameError` for anyone past the access gate since the first commit — fixed first with a temporary 302 to `/formality` (`3d2fb99`). Also found the Paiboon index disagrees with itself (`phrá`/`prá`, `thaan`/`taan`, an IPA `ŋ` against the app's `ng`), which feeds the dictionary and chanting book too. The Thai remains unreviewed; the page carries a permanent invitation for corrections (`3eb7019`) rather than a temporary draft banner.

---

## inclusive-positioning

### 2026-08-19 — v2 (the two constraints)
**Change:** Adds *"Universal must mean no country named at all — not my country substituted for Thailand"* and *"Describe people by what they are learning, never by what they are not."*
**Reason:** Both were caused by specific failures in v1's output that Josh caught. The draft proposed "practising the precepts in Britain" — *"Isn't this supposed to be universal?"* — and a first pass renamed "foreigner" to "non-Thai", which prompted *"Is there a better name than non-Thai?"*
**Impact:** `/practising-anywhere` names no country anywhere on the page and says so, built from the five precepts, the three bases of merit and the Sigālovāda Sutta's six directions. The label was dropped rather than renamed, in favour of second-person address. Monk Mode stopped calling non-Thai monks "Western" and now describes both sides by the language they are learning. Tests fail if any of it comes back (`c7fa28d`, `4167bc9`).

### 2026-08-19 — v1 (the diagnosis)
**Change:** First version — the positioning question with an audit step in front of it: read the gate configuration before proposing any change.
**Reason:** A learner who visits Thai temples said the app felt like Thai culture was the price of admission for the Dhamma. Without the audit step the prompt rewrites copy; with it, it checks whether the copy is even true.
**Impact:** Found that the app already granted exactly what she asked for — `theravada`, `meditation`, `chanting` and `paiboon` all free, level 1, `requires_alphabet: False` — and that the home page said the opposite. Shipped as two new pages plus a home-page chooser (`80a8712`, `5b113d6`).

---

## xp-economy-audit

### 2026-08-18 — v2 (remediation)
**Change:** Follow-up prompt asking for fixes, with the priority named: *"How can we fix this? Especially so that a free user watches a progress bar fill up toward a reward that doesn't exist issue can be fixed."*
**Reason:** v1 diagnosed; this asked what to do about it, and the second sentence ruled out an answer that fixed the security holes and left the free tier as it was.
**Impact:** Three options for the free-user problem, of which "let XP buy one real paid section" shipped as the earned unlock (`a4385f3`) — Level 3 now opens one Thai Reader section, permanently and free. The other three findings shipped alongside it as separate commits.

### 2026-08-18 — v1 (audit)
**Change:** First version — asks whether the XP system is *effective*, naming the free sections so the answer has to be arithmetic: *"how do users get XP when only Alphabet, Paiboon and Buddhism is free? Can other sections be unlocked with XP or do they require payment?"*
**Reason:** The XP system had been live since 2025-12 and nobody had checked whether it did anything for the audience that never pays.
**Impact:** Found that free-tier levelling unlocks nothing (every free section is level 1, so ~360 earnable XP buys nothing), that `max_level_access` is set on all three tiers and read nowhere, that four of six `POINT_REWARDS` are dead, and that `/api/award_points` took its XP amount from the caller with no callers anywhere in the app.

---

## chanting-book-batch

### 2026-08-06 — v7 (a publication, not a translation)
**Change:** Adds the seven-step lifecycle the three stages sit inside — read the page, write the layers, quality check, human review, enrich, final QA, approve — with steps 4 and 7 marked as Josh's and not delegable. Stage 1 gains a self-check run while the photograph is still open (layers agreeing with each other unit for unit, romanised Pali spelled consistently across the batch, Paiboon+ drift, and every printed thing on the page accounted for) and collects six to ten glossed Pali terms per chant. Stage 2 gains two things: it may no longer drop anything stage 1 recorded — every key of the batch file must be shown to have landed somewhere, and "there is no field for it" now stops the batch — and it ends with a QA pass on the rendered page rather than the data. Stage 3 gains a table mapping what a learner arrives asking onto the fields that answer it.
**Reason:** Josh's framing: *"treat the project like a digital publication, not just a translation... it produces a richer educational resource with explanations, context, and learning material that add value beyond the original text."* The workflow reproduced the book well and had no account of the value beyond it — nor, more urgently, any step where something checked that what stage 1 read actually reached the app. That gap was not hypothetical: pages 7 and 8 went live showing roughly half of what the printed page shows, because stage 1 recorded the service closing, the explanatory section and its footnote faithfully and stage 2 had no field for any of it. Nothing raised, nothing failed, found weeks later by Josh reading the app beside the book. The other half is division of labour — his time is the scarce input across 325 pages, and it was partly going on things a machine can prove, like whether two layers have the same number of units.
**Impact:** `vocabulary` and `references` are deliberately NOT written into `chanting.py`, and the prompt says so twice: the app has no field for either and the templates render neither, and writing data the app cannot display is the same mistake as dropping data it has no field for — a second copy of the truth that nothing renders, nothing tests and nobody reads. They stay in the batch files until the app grows somewhere to show them. One bug found while rebuilding the sheet: the PDF builder asserts fenced-block count against stage count, and a fenced `json` example added inside stage 1's prompt block broke the fence and made the file look like four stages. The assertion was added in v2 for exactly this and had not fired since — examples inside a stage prompt are indented, never fenced. Sheet rebuilt to 29 pages; prompt-sheet tests still pass.

### 2026-08-05 — v4 (reading from photographs, and making the page the unit)
**Change:** Stage 1 now reads PHOTOGRAPHS of the book — nine pages a batch — instead of text Josh typed with `[p.47]` markers in it. It declares a **page map** alongside the chant manifest (one row per page per chant, with the verse range) before writing any entry, and Stage 2 rebuilds each verse's page by carrying forward and reconciles it against that map before writing anything. Added: continuations for a chant whose pages cross a batch boundary, `book_number` for the book's own chant numbers, resume-by-page, and an image-reading section on what a camera cannot give you. Nine rubric criteria added; rubric to v2.
**Reason:** Josh's framing set the standard — *"I want the chants added to the app to look exactly like the images from the book... so page numbers contain exactly the script from each image... when a monk calls out a page number, users go to that called-out page number and find the exact chant."* Asked how the book prints its page numbers, his answer named the trap: *"There is alwyas a page number at the top centre in English. All other numbers contained within some pages are numbers for chants or something else; either in Thai or English?"* So only the top-centre number is ever a page number, in any script. A chant number read as a page number produces output that looks entirely reasonable and is wrong for every page after it.
**Impact:** Per-verse pages are stored sparsely — a verse carries `page` only where the page turns — which means one missing marker moves every following verse onto the wrong page and leaves data that looks well-formed. Nothing downstream could catch it, so the page map exists to be disagreed with, and neither side may be edited to agree with the other. Continuations fix a rule that was quietly wrong: "finish or don't start" was written for truncated replies, where stopping early means something broke; when the BOOK carries a chant onto an unphotographed page it means the opposite, and the two are indistinguishable in the output unless the model says which. Verified while writing it: the seventeen pre-existing chants have `page_start` on **zero** of them, so until the merge pass reaches their pages the book would have holes exactly where its first chants are. The eval fixture was rebuilt with a real page map so the new criteria are exercised rather than passing on absence; full suite re-run at 12 prompts, 100%. One harness fix fell out — `page_map_runs_forwards` errored with `NameError` rather than failing, because the eval sandbox exposed no `sorted`; `scripts/eval_runner.py` now exposes the pure ordering builtins, which cannot change how any existing condition evaluates. The page-by-page reading view itself is deliberately NOT built by these prompts: Stage 2 still may not touch the route or the template, because a batch that could alter how the whole book renders is a batch whose diff nobody reads.

### 2026-08-04 — v3 (page numbers, and merging the chants already in)
**Change:** Stage 1 now captures the page number each chant appears on in the physical book, marked `[p.47]` in the paste — `page_start` on the chant, `page` on a verse only where the printed page turns. Stage 2 merges a chant that already exists rather than appending a second copy. The app shows a page badge on each index card and a quiet marker at every page turn. Version history added under `versions/`.
**Reason:** Josh's own framing decided the priority — *"Important so users can keep up with the Monk who calls out page numbers or chant titles as we chant along."* A digital chanting book that cannot answer "page 47" has failed at the job, whatever its five layers do. Which also makes a wrong page number unlike any other error here: it is met in public, mid-chant, with no recovery. So its rules match the fidelity rules — never infer, never estimate, never carry a number forward.
**Impact:** The seventeen chants set before this workflow existed now get re-pasted rather than skipped, which is how they gain page numbers and the only chance to check them against the book a second time. The merge rule keeps that safe: the file wins unconditionally, differences are reported and acted on by nobody but Josh, and `len(CHANTS)` is checked to grow by the number of NEW chants only — a merge quietly becoming an append is how a book ends up with the same chant twice. Three rubric criteria added and negative-tested: page values must be bare integers, since `"47"` would break any later sort or page search.

### 2026-08-04 — v2 (all five layers at every depth, plus a Stage 3)
**Change:** `DATA-ONLY` now keeps the per-verse `english` it used to drop, so all five layers are written at every depth and only the chant-level prose varies. Added Stage 3, a commentary pass that runs in Claude Code after a DATA-ONLY batch is in and verified.
**Reason:** Josh asked whether DATA-ONLY gave all five layers, which it did not — it gave four. Answering it exposed a bad trade: dropping `english` bought 8–12 chants a reply instead of 6–9, but a verse without its meaning is not usable, the layers are read together down the page, and a second pass over 286 chants purely to add one layer per verse costs more than the extra chants save. The depth setting should only ever vary prose written *about* a chant, never the chant itself.
**Impact:** Stage 3 needs nothing pasted — by the time it runs the chants are in `chanting.py`, so it reads them from the file, which is the real payoff of splitting the depths: the deferred half stops being a copy-paste job. Its governing rule is that it may not alter one character of any verse, and it proves that with a before-and-after dump of every verse, title and invitation, diffed to show the diff is empty — evidence rather than assurance, since verified Pali that quietly changed would not look wrong afterwards. Rubric criterion widened from four layers to five and confirmed to fail when `english` is removed; the PDF builder now takes a variable number of stages and asserts the count, so a sheet cannot silently print two stages when the prompt has three.

### 2026-08-04 — v1 (batch variant, forked from chanting-book-entry v4)
**Change:** A second copy of the two-stage workflow, rebuilt to take several chants per message instead of one. `chanting-book-entry` is unchanged and stays the prompt for setting a single chant carefully. New in the batch version: a depth setting (`FULL` / `COMPACT` / `DATA-ONLY`), a manifest declared ahead of the entries, per-chant `checks` instead of one pooled array, repeat detection, and a Paiboon+ self-scan before the batch closes.
**Reason:** The book is 286 chants. Measured against the 17 already set, a finished entry is ×9.1 the size of what gets pasted in, and Thai, IAST and Paiboon+ tokenise at 1.91 chars/token — about half as efficiently as English. That puts the whole book at ~1.09M output tokens and the honest ceiling at 2–3 chants a reply, which is arithmetic rather than anything wording can fix. Breaking an entry down by field showed the way through: ~58% of it is commentary written *about* the chant, and none of that needs checking against the physical book. `DATA-ONLY` defers it and gets 8–12 chants a reply.
**Impact:** The failure batching introduces is a reply cut off mid-array — at one chant a message you would see it, at eight you would not, because truncated JSON still parses. Nothing written at the end of a reply can report this, since in a truncated reply the end is what is missing. So the manifest goes first and stage 2 refuses to write anything until it reconciles. Two bugs found while building it: the v1 `invitation` template showed three layers where the dicts in `chanting.py` hold five, and `english_unverified` — live on 10 of 17 chants — was never mentioned, so it had been added by hand every time.

### 2026-08-04 — rubric fix (inherited RTGS check was nearly dead)
**Change:** The `paiboon_not_rtgs` condition now matches `kh`/`th`/`ph` bare, instead of requiring a plain vowel after them.
**Reason:** Found by negative-testing the new rubric rather than by it failing. The inherited regex was `(kh|th|ph)[aeiouɛɔəʉ]`, but every Paiboon+ syllable carries a tone mark — so `thâng`, `khǎn` and `phrá` all slipped through, which is to say every RTGS slip that would realistically occur. It only ever caught unaccented spellings, which are the ones that do not happen.
**Impact:** Checked against the 133 paiboon lines already in `chanting.py`: bare `kh`/`th`/`ph` appears zero times, so matching bare is safe as well as effective. The same weakness is still present in `chanting-book-entry`'s rubric and has been left alone, since that prompt is deliberately frozen. Worth noting separately: each criterion catches exactly its own failure, but one failing criterion only moves the weighted score from 100% to ~94%, so `--fail-under 0.8` will not trip on a single fault. The rubric names the failure; it does not gate on it.

---

## chanting-book-entry

### 2026-07-31 — v4 (migration complete)
**Change:** Moved the working notes inside the JSON object, renamed the note headings to match the keys they feed, rewrote the three stage-2 rules that still looked for the old `TITLE_PALI` / `INVITATION` / `SOURCE` labels, and added `title_roman` so a chant with a Thai title is findable by a reader who cannot read Thai script.
**Reason:** Two questions found two bugs. Asking whether "the JSON" and "the stage 1 output" were the same thing showed they were not — the prompt asked for the notes twice, in two places. Reading stage 2 to prove it had reached GitHub showed three rules pointing at labels stage 1 stopped emitting at v3; they guarded exactly the "never invent a title, source or invitation" behaviour, and were silently dead.
**Impact:** Removed a live hazard — the JSON is found by taking the first `{` to the last `}`, so any prose above it was one stray curly bracket away from breaking the parse. Both bugs were migration debris: rules written for a replaced format, still sitting there looking authoritative, neither producing an error.

### 2026-07-31 — v3 (JSON output)
**Change:** Stage 1 now emits one JSON object whose keys match the dict keys in `chanting.py`, every value on a single line, with the `⚠️ CHECK` flags moved into their own top-level array that names the verse each belongs to.
**Reason:** Long values wrapped on the way through the clipboard, and Thai script, Paiboon+ diacritics and IAST all survive a wrapped line badly. Inline flags read well but were easy to lose moving text between two tools.
**Impact:** Stage 2 maps keys straight across instead of parsing by eye, and reports how many checks it carried. Rubric rewritten to cover both newline failure modes. Found two evaluator sandbox traps on the way: no `bool` and no `list` in the pass-condition namespace.

### 2026-07-31 — v2 (book layout)
**Change:** Working notes in a fixed order, one Pali line per verse, sections numbered and bilingual (`SECTION 1 — สังขาร: The Three Characteristics`), flags beside the verse they concern, and a closing sentence counting them.
**Reason:** v1 produced the right content but not reliably the right shape — a good run and a poor run differed by luck. Making the good run the spec removed the luck.
**Impact:** Four `⚠️ CHECK` flags on the first real chant — a missing Pali title, a composite source, a crossed Pali/Thai order, and a probable one-character slip in `ฉุฑโท`. None would have been visible otherwise.

### 2026-07-31 — v1 (two-stage workflow)
**Change:** A two-surface prompt pair — stage 1 in Claude.ai does transliteration, romanisation, translation and background; stage 2 in Claude Code writes it into `chanting.py` and verifies it renders.
**Reason:** Turning a page of a physical Thai chanting book into an app entry needs both language work and file work, and they suit different tools. Splitting them also puts a human checkpoint in the middle, which is where the Pali gets verified against the book.
**Impact:** Established the rules every later version kept — the five layers are not interchangeable, never reconstruct Pali from memory, flag rather than guess, and hold the formal literary register. Chant 2 shipped from it: 13 verses, 869 Thai characters in, 869 out.

---

## tones-consonant-classes

### 2026-07-19 — v1 (explore-first build)
**Change:** Added one free, unified "Tones & Consonant Classes" section — a `TONES_AND_CLASSES` data dict, a `/tones-classes` route, a template with reference tabs and four progressive drills, built on the `feature-experiment` branch.
**Reason:** Consonant classes only exist to determine tones, so teaching them as separate sections was confusing; the content also lived scattered across three places (one paywalled).
**Impact:** A single free reading skill that reuses the existing `/api/check_answer` XP scoring. Taught me the value of an explore-first gate — surveying the codebase and recommending merge-vs-rebuild *before* editing avoided duplicating content and kept the change from touching unrelated code.

---

## frontend-build

### 2025-11-19 — v3 (Option C)
**Change:** Added the interactive JavaScript layer — flashcards, progress saving, confetti, sounds, keyboard nav.
**Reason:** A static app isn't engaging; learners need feedback and persistence.
**Impact:** A genuinely interactive front end (and where the front-end bugs lived).

### 2025-11-19 — v2 (Option B)
**Change:** Moved styling into external CSS with a variable-based Thai theme and animations.
**Reason:** Inline styles were unmaintainable.
**Impact:** One place to change the whole colour scheme.

### 2025-11-19 — v1 (Option A)
**Change:** Generated the 6 core HTML templates with a deep-red / gold / cream theme.
**Reason:** Needed the actual pages on top of the Flask backend.
**Impact:** A working multi-page UI; taught me that pasting code into chat ≠ putting it in the project folder.

---

## gamification-system

### 2025-12-03 — v3 (templates added)
**Change:** Added the new templates (`progress`, `locked`, `developer_login`, `subscription_success`).
**Reason:** Routes throw `TemplateNotFound` until their templates exist.
**Impact:** Developer mode, progress dashboard and subscription tiers all working end to end.

### 2025-12-03 — v2 (integrated app)
**Change:** Merged the gamification into a single `app.py`.
**Reason:** The paste-in snippet couldn't run on its own.
**Impact:** Surfaced a duplicate `/formality` route that crashed startup until removed.

### 2025-12-03 — v1 (paste-in snippet)
**Change:** First version delivered as a `gamification_system.py` snippet.
**Reason:** Add XP/levels, locked sections, developer mode and subscriptions.
**Impact:** Hit `name 'app' is not defined` — a snippet has no Flask app to run on its own.

---

## romanization-system

### 2025-12-09 — v3 (AI tutor match)
**Change:** Pinned the AI tutor's romanization to the app's house style (`khâ`→`kâ`, `ng`→`ŋ`, `thai`→`tai`).
**Reason:** The tutor used a different romanization than the app.
**Impact:** One consistent romanization everywhere.

### 2025-12-04 — v2 (display consistency)
**Change:** After several failed CSS attempts on the `ɔ̌ɔ` vowel, switched all romanization to a monospace font.
**Reason:** Combining diacritics render unevenly in proportional fonts.
**Impact:** Characters line up consistently — a pragmatic workaround, not a true typographic fix.

### 2025-11-19 — v1 (beginner mode)
**Change:** Added a beginner mode that swaps word-final single `i`→`y` and `o`→`w`, leaving vowel combos and double vowels alone.
**Reason:** Beginners misread final `i`/`o` as "ee"/"oh".
**Impact:** Clearer pronunciation cues, toggleable on/off.

---

## buddhist-pdf-integration

### 2026-02-19 — v2 (complete, faithful)
**Change:** Reproduced each essay in full on its own HTML page, every paragraph preserved, linked via new routes.
**Reason:** v1 quietly dropped paragraphs and reworded the text.
**Impact:** Faithful pages — *faithful means faithful*; check against the source, don't trust a summary.

### 2026-02-19 — v1 (dropped paragraphs)
**Change:** First attempt adding the "Pra Kru Bob's Writings" section.
**Reason:** Add two PDF essays to the Dharma page, styled.
**Impact:** Looked nice but abridged the content — not acceptable.

---

## ai-tutor-integration

### 2025-12-09 — v2 (running)
**Change:** Got the Claude-powered tutor actually working through a chain of setup fixes (Python, Flask, API key quoting, loading the key at the top of the file).
**Reason:** Phase 1 code was correct but wouldn't run as a beginner setup.
**Impact:** A live 6-mode tutor at `/chat`; biggest lesson — don't trust "it works" until you test it.

### 2025-12-08 — v1 (Phase 1 core)
**Change:** Built `ai_agent.py` (6 modes), `chat.html`, and integration routes.
**Reason:** Add an in-app AI tutor, built in phases.
**Impact:** The core chat system, ready to wire in.

---

## claude-code-workflow

### 2026-02-23 — tests & review
**Change:** Added 32 unit tests for the XP/level logic; ran a code review and fixed high-priority issues (HTTP 400s, try/except around the DB commit).
**Reason:** Make the gamification logic verifiable and the signup route robust.
**Impact:** A test suite and safer error handling; made two fixes by hand when Claude Code ran out of credits.

### 2026-02-22 — bug fix & refactor
**Change:** Fixed the empty-form submission bug (removed `novalidate`, added `required`) and refactored the signup `fetch` to async/await.
**Reason:** Build real features safely via Claude Code with a Git safety net.
**Impact:** Cleaner code and a clean commit history; decided to adopt feature branches + PRs going forward.

---

## market-research-report

### 2026-04-17 — v3
**Change:** Pinned a fixed 10-section structure and attached two source documents (a Product Overview and an analyst framing); kept the competitor-scraping instruction.
**Reason:** v2 was grounded but still freeform; I wanted a consistent, predictable report shape.
**Impact:** A consistently structured, source-backed report I could use to make a go/no-go decision.

### 2026-04-16 — v2
**Change:** Named the three competitors (ling-app.com, duolingo.com, thaipod101.com) and asked the model to scrape them with dedicated tools.
**Reason:** v1 was broad but not anchored to real rivals.
**Impact:** Concrete, current competitor analysis. Also surfaced a key lesson — naming a tool doesn't guarantee it runs; one scraping tool was never actually called.

### 2026-04-16 — v1
**Change:** Initial broad research request.
**Reason:** Needed a first read on the UK market for the app.
**Impact:** Good breadth, but ungrounded and unstructured.

---

## product-overview-section

### 2026-04-16 — v2
**Change:** Added answers to the model's three scoping questions (audience, emphasis, monetisation depth).
**Reason:** The bare brief left the angle ambiguous.
**Impact:** A full, structured five-part overview in one pass — later reused as a source document for the market research report.

### 2026-04-16 — v1
**Change:** Initial five-part brief (what it does / who it's for / features / problem / monetisation).
**Reason:** Needed a Product Overview section for the market research report.
**Impact:** Prompted the model to ask three scoping questions before writing.

---

## wireframe-layout-system

### 2026-06-06 — v3 (reusable distillation)
**Change:** Distilled the layout work into a reusable prompt — outline → per-page layout templates → reusable partials → responsive roll-out.
**Reason:** Capture the whole workflow in a form reusable on any multi-page project.
**Impact:** A documented site outline, three Jinja partials, the 3-column layout across Learn/Culture/Buddhism, and fill-or-scroll tables.

### 2026-06-06 — v2 (content-first)
**Change:** Switched from "stamp a wireframe on every page" to writing a content-first site outline first.
**Reason:** A wireframe is a planning tool, not a feature — plan content before styling.
**Impact:** A deliberate per-page plan instead of one forced layout.

### 2026-06-06 — v1 (all pages)
**Change:** First instinct — apply the wireframe layout to all pages.
**Reason:** Wanted a consistent look.
**Impact:** Would have made simple info and full-width pages look wrong; corrected by matching the layout to each page's job.

<!-- Add more entries above as the library grows. -->
