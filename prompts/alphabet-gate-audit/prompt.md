# Alphabet Gate Audit — Is the Prerequisite Drawn in the Right Place?

**Category:** analysis
**Model:** Claude (Opus)
**Project area:** `SECTION_REQUIREMENTS`, `check_section_access`
**Status:** shipped 2026-08-19 — `d99c524`, live

---

## Final prompt

> Is it right for the Alphabet page to be free?
>
> Answer from the data, not from instinct. Count how many sections carry
> `requires_alphabet`, and say what would follow for each of them if the
> Alphabet itself were paid.
>
> Then ask the harder question I have not asked: is the prerequisite drawn in
> the right place? For every section that requires it, decide whether that page
> actually needs someone to READ THAI SCRIPT, or whether it is taught in
> romanisation and English and the requirement is doing no teaching work.
>
> Measure it rather than asserting it — for the borderline pages, work out how
> much of the content is even in Thai.
>
> Check what "passing" costs, and check the order the gates run in. If a paying
> subscriber can be blocked by this, say so.
>
> Flag anything that is plainly wrong rather than merely arguable. Do not
> propose changing the paid add-on that exists to skip these gates — that is
> settled.

---

## Why this prompt is shaped this way

**"Answer from the data"** turned a matter of opinion into arithmetic. All 21
paid sections carry the flag, so charging for the Alphabet would put a paid
prerequisite in front of everything paid.

**"Then ask the harder question I have not asked"** is where the value was. The
question as posed had a short answer. The interesting finding was one level
down: the prerequisite is applied to *everything* paid, including pages taught
entirely in romanisation.

**"Measure it rather than asserting it"** produced the numbers that made the
Culture case: 31% of its strings contain any Thai at all.

**"Check the order the gates run in"** found the sharpest version of the
problem — the alphabet gate is checked *first*, so someone who has paid can
still be refused.

**"Do not propose changing the paid add-on"** fenced off a settled decision so
the audit did not spend itself re-litigating it.
