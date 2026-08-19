# Inclusive Positioning — Separating a Universal Teaching from One Culture's Expression of It

**Category:** analysis / content
**Model:** Claude (Opus)
**Project area:** site-wide positioning — home page, Buddhism section, Thai culture section
**Status:** shipped 2026-08-19

---

## Final prompt (v2)

> A learner has told me the app feels culturally exclusionary. She wants the
> Buddhist teaching but not the Thai cultural identity that seems to come
> attached to it.
>
> How can we adapt the app to appeal to people who want Buddhism as universal —
> pure Dhamma without the association of any culture or society — so that anyone
> in any part of the world feels they can learn it and practise it wherever they
> are, in whatever culture or society they exist? Is it possible to adapt the app
> like this while also preserving the existing Thai cultural side of it?
>
> Before proposing anything, check what the app's access rules actually grant.
> Read the gate configuration, not the marketing copy, and tell me where the two
> disagree. Then propose the change.
>
> Constraints:
> - Do not remove or weaken the Thai cultural material. It is what makes this
>   project distinctive.
> - Universal must mean no country named at all — not my country substituted for
>   Thailand.
> - Describe people by what they are learning, never by what they are not.

---

## Why the prompt is shaped this way

**"Check what the access rules actually grant... before proposing anything."**
This is the line that produced the finding. Asked to fix the positioning, a model
will rewrite copy. Asked to compare the copy against the gate configuration first,
it found that `SECTION_REQUIREMENTS` already made every Buddhism page free, level
1, with no alphabet prerequisite — the app had granted what the learner asked for
all along, and only the home page said otherwise.

**"Universal must mean no country named at all."** Added after the first attempt
illustrated lay practice with "practising the precepts in Britain" — the same
parochialism wearing a different flag.

**"Describe people by what they are learning, never by what they are not."**
Added after "foreigner" was renamed to "non-Thai", which is politer and
structurally identical.
