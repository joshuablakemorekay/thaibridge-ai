# Reasoning: Register Levels Draft

## Goal

`templates/register.html` had been in the repo since the first commit — a
finished page for the nine levels of Thai formality, from monastic language down
to vulgar, with examples, usage notes and warnings. It had never once rendered.
It called for a `registers` dict named `REGISTER_LEVELS` that did not exist.

I asked for the missing half:

> draft the nine register levels for me to review

The last three words are the whole brief. I am a monk and I have a Thai teacher;
what I needed was not finished content but something reviewable.

## Iteration history

Single version, but it followed a bug fix on the same page. The route had been
raising `NameError` since the first commit. Because the access gate ran *before*
the view, a logged-out visitor got the ordinary "locked" page and only someone
who had paid, reached Level 4 or used Monk Mode ever saw the 500. Nothing linked
to it, so nobody ever reported it.

Asked how to handle it, I said:

> do the safest and most effective way

which produced a temporary 302 to `/formality` — deliberately a 302 and not a
301, so browsers would not cache it and keep sending people away once the page
was finished. That redirect is what made it safe to write the content without
time pressure.

## Failure modes the final version handles

- **Holes that render as blank paragraphs.** Jinja resolves a missing key to
  empty rather than raising. Deriving the contract from the template first, and
  testing every field, is what catches this.
- **Invented romanisation.** The app already had 1,217 Paiboon entries. Writing
  fresh romanisation beside them would have made the page disagree with the
  dictionary.
- **A draft presented at uniform confidence.** Per-register "please check" lists
  say where I am least sure, so the review starts somewhere useful.
- **A review copy that drifts from the data.** The sheet is generated from
  `register_levels.py`, so correcting one without the other is not possible.

## Outcome

Nine registers, 29 worked examples, in `register_levels.py` — deliberately its
own module rather than more weight in `app.py`, and deliberately named apart from
`thai_registers.py`, which holds the three politeness *variants* applied to
sentences. Two files with similar names doing different jobs needed the
difference written down, so it is in both docstrings.

Two findings came out of the work that were not part of the brief:

1. **`REGISTER_LEVELS` never existed in any commit.** I traced it through the
   whole history, including the deleted 236KB `app_backup.py`. Both files only
   ever *used* the name. There was nothing to restore.
2. **The Paiboon index disagrees with itself** — `phrá` vs `prá`, `thaan` vs
   `taan`, an IPA `ŋ` where the rest of the app uses `ng`. It feeds the
   dictionary, the chanting book and this page, so it is worth settling once.

| Commit | What |
|---|---|
| `3d2fb99` | The redirect, replacing a crash that predated every other commit |
| `248ab5f` | Test that the redirect stayed off the public curriculum outline |
| `e921ad4` | The nine registers |
| `3eb7019` | A permanent invitation for corrections |

## Engineering on the output

- **Accepted as-is:** the nine-register content itself, the module split, and
  the decision to generate the review sheet from the data.

- **Reworked — the draft banner.** I told the page to ship. It added a red
  banner across the top saying the Thai was unchecked. I removed it:

  > remove the draft banner

  Then, asked what to do about the underlying honesty problem, I said:

  > Do what is safe and most effective

  The second attempt is better than either the banner or nothing: a quiet line
  at the *foot* of the page inviting corrections. The banner framed the page as
  broken and was temporary by design — something to delete after sign-off. But
  register is the part of Thai that shifts most with region, age and setting, so
  there is no date after which corrections stop mattering. The line earns its
  place permanently.

- **My editorial call, recorded because it is arguable:** level 9 lists the
  coarse pronouns and the derogatory prefixes and stops short of the real
  obscenities. Enough to recognise the register without the page becoming a
  glossary of swearing. That is a judgement about what belongs on a Buddhist
  learning app, not a linguistic one.

- **Not tracked:** the Thai itself has not been through my teacher yet, so there
  is no delta to claim on it. That is honest rather than modest — the review is
  genuinely outstanding.

## What I'd change next

Settle the Paiboon index inconsistencies once, across the dictionary, the
chanting book and this page. And get the teacher's pass on the monastic register
first, since that is the one where my own knowledge is strongest and the cost of
being wrong on the app is highest.
