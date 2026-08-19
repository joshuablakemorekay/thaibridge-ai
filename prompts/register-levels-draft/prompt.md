# Register Levels Draft — Nine Levels of Thai Formality, Grounded and Reviewable

**Category:** content
**Model:** Claude (Opus)
**Project area:** `/register` — the nine-level formality reference
**Status:** shipped 2026-08-19 (Thai awaiting native-speaker review)

---

## Final prompt

> Draft the nine register levels for me to review.
>
> The template `templates/register.html` already exists and expects a `registers`
> dict. Read it first and derive the exact contract — which nine keys, which
> fields on each, which fields only some of them use — before writing any
> content. A missing key renders as empty in Jinja rather than raising, so a hole
> would ship as a blank paragraph nobody notices.
>
> Ground the Thai in the app's own data where it exists: check each word against
> the Paiboon index rather than inventing romanisation, and report where the
> index disagrees with itself.
>
> This is a draft for me and my teacher to check, so:
> - Flag what you are least sure about, per register, rather than presenting it
>   all at one confidence level.
> - Generate the review copy from the data, not by hand, so the two cannot drift.
> - Do not put unreviewed Thai in front of a learner without saying so.

---

## Why the prompt is shaped this way

**"Read it first and derive the exact contract."** The template was written years
before the data. Deriving the contract from the template — nine keys in a fixed
order, thirteen fields, `sub_level_a`/`sub_level_b` only on `casual`,
`cultural_notes` only on `vulgar` — is what stopped the draft from having holes.

**"Check each word against the Paiboon index."** The app already holds 1,217
Paiboon entries. Using them keeps the page consistent with the dictionary and the
chanting book, and it surfaced that the index disagrees with itself (`phrá` vs
`prá`, `thaan` vs `taan`, an IPA `ŋ` where the rest of the app uses `ng`).

**"Flag what you are least sure about, per register."** A draft presented at one
confidence level makes a teacher re-derive which parts are shaky. Per-register
"please check" lists give the review somewhere to start.

**"Generate the review copy from the data."** A corrected review sheet sitting
beside an uncorrected dict would be worse than no review sheet at all.
