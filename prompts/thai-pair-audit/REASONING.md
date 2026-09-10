# Reasoning: Thai/English Pair Audit

> Josh delegated the review of this write-up (*"yes just do what you recommend"*),
> so the reasoning below was drafted rather than dictated. The quotes are his,
> word for word; the prose around them is not, and he has not line-edited it.

## Goal

Find out whether the Thai in the app says what the English next to it says. The
suspicion came from one line on the home page, and the point of the prompt was to
turn that one line into a question that could be asked of the whole site.

## What the opening question actually was

> Also there are corrections that need to be made, some of the Thai script doesn't
> match, eg, 🪷 ThaiBridge AI
> Learn the Dhamma. Learn Thai. Find Your Own Path.
> พระธรรมและภาษาไทย - On Homepage here does the Thai script match the English?

The answer was no: `พระธรรมและภาษาไทย` means *"the Dhamma and the Thai language"* —
a noun phrase, where the English is three instructions. Not wrong Thai; wrong
Thai *for that line*.

That distinction is what made the sweep worth doing. A spellchecker would have
passed it.

## Iteration history

Three versions, and each one was narrowed by Josh rather than by me.

- **v1 — the single line.** Answer one question about one heading.
- **v2 — the sweep.** *"Do it."* Extract every dict carrying both a `thai` and an
  `english` key and check them in bulk. 707 pairs, plus every page heading.
- **v3 — the scope ruling.** *"Do the ones you can verify, hold the rest for my
  teacher"* — the constraint that decided what shipped.

## The rule that did the most work

**Only change a word if that word *and* its romanisation already appear somewhere
else in this codebase.**

That rule came out of v3 and it is the reason this audit is trustworthy. Roughly
half the broken rows could only have been fixed by writing new Thai. Writing new
Thai to fix wrong Thai swaps a known error for an unreviewed one and calls it
progress — so those rows were left visibly broken and escalated to a human
teacher instead, in `docs/vowel-review-2026-09-10.md`.

Six rows of the vowel table are still wrong in production on purpose. That is the
correct outcome, not an unfinished one.

## What it found

Roughly 40 defects, in three kinds:

- **Outright errors** — five vowel examples had lost their opening consonant
  entirely and rendered as orphan vowel marks (`ึง / ืด`); `สามคนนักเรียน` was
  taught as *"Most common pattern for counting"* and is not grammatical Thai;
  `กัวน` and `บ้าย` are not words.
- **Inconsistencies** — the same word written two ways (`เรือ` as both `rʉa` and
  `rua`), and the velar nasal written `ng` in 26 places including all ten in the
  44-consonant chart.
- **Judgement calls** — Sanskrit spellings (Dharma, Nirvana) in a Theravada app
  that uses Pali everywhere else; `ผีตาโขน` glossed as "Ghost Festival", which
  reads as the Chinese one.

## The finding behind the findings

The romanisation rules being violated were **already Josh's own documented house
style**, recorded in [`romanization-system`](../romanization-system/REASONING.md)
from an earlier session, in his own words:

> Remove h in khâ & thîi. Replace ng with ŋ...

So this was not a prompt that decided a standard. It was a prompt that discovered
a standard had been decided, written down, and then drifted in forty-odd places.
The most useful audits check work against a rule the project already agreed to —
not against the auditor's taste.

`tests/test_contents_roman.py` turned out to already assert `'ng' not in reading`
for the chanting contents. The rule was even executable. It just wasn't applied
anywhere else.

## Failure modes the final version handles

- **Inventing Thai to fix Thai.** Handled by the attestation rule above.
- **Auditing the wrong thing.** `chanting.py` holds 22,000 lines of Thai and has
  its own review pass; sweeping it here would have produced thousands of
  duplicate findings. Excluded explicitly and said so.
- **Confusing a convention with a bug.** Two findings were withdrawn on checking:
  `เซลล์` romanised `seen` is *correct* (the app maps `เอ` → `ee`), and the English
  text inside `class="thai"` on the monk pronunciation page is the site-wide
  subtitle style, not a font error.
- **Trusting the audit's own output.** Extracting by dict key missed
  `_syl()`/`_word()` positional calls in `thai_reading.py` and the whole
  `sound` field in `thai_consonants.py`. Both were only caught by checking the
  live site afterwards, one commit too late.

## Outcome

Five commits, all live: `94ba71d`, `691dcab`, `f41cf23`, `9ea83b6`, `74ff5ff`.
Full suite green at 1385 tests throughout. Verified on the deployed site, where
the alphabet page went from 0 to 12 correct `ŋ` and zero remaining `ng`, with
audio and image filenames correctly untouched because they are hashed from the
Thai, never the romanisation.

## Engineering on the output

This entry inverts the usual shape of this section, and it should be read that
way. Josh did not rework generated code here — the work was done inside Claude
Code and he directed it. His contribution was **scope control**, and it was the
part that determined whether the result was safe to ship.

- *Accepted as-is:* the extraction method and the structural checks.
- *Overruled:* the audit proposed reconstructing the five corrupt vowel entries
  from their surviving romanisation. Josh's *"hold the rest for my teacher"*
  replaced that with an escalation. Two of those five were corrupt in the gloss
  as well as the Thai, so reconstruction would have shipped confident nonsense.
- *Ruled on individually:* every one of the five romanisation conflicts was
  decided by Josh line by line, in the form *"For เรือ → rʉa (2218) vs rua (2227)
  use only เรือ → rʉa (2218)"* — not delegated to the auditor's preference.
- *Roughly:* the analysis was accepted; the **scope was cut**, and cutting it was
  the right call.

One of the fixes made a latent bug visible rather than fixing one: normalising
`rua` → `rʉa` turned vowel rows 11 and 12 into character-for-character
duplicates, which exposed that row 12's example word had been wrong all along and
that the `"boat (alternate)"` gloss had been hiding it. Worth recording — a
consistency pass earns part of its keep by making other bugs impossible to miss.

## What I'd change next

Audit `survival.py`. It has 79 lines of unchecked Thai and, since the home page
redesign, it is the free front door for anyone who wants to speak rather than
read — the highest-traffic unaudited surface in the app.

## Tags

`audit` `data-integrity` `thai` `romanization` `scope-control` `escalation`
