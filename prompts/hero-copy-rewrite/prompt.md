# Hero Copy Rewrite — Writing Cultural Freedom Without Making the Host Culture Optional

**Category:** content
**Model:** Claude (Opus)
**Project area:** home page hero, `/about`
**Status:** shipped 2026-08-19 (commits `95635ef`, `9b234c4`, `9cf3302`, `74341c6`)

---

## Final prompt (v3)

> Here is the hero on my home page:
>
> [paste the current hero]
>
> This doesn't sound very convincing. Rewrite it.
>
> Constraints:
> - The hero must say what a visitor **gets**, not how the site is organised.
>   "Two subjects, side by side" describes my filing system, not their reason
>   to stay.
> - The app teaches a universal teaching (the Dhamma) alongside one culture
>   that has carried it (Thailand). The copy must offer three real options:
>   study it through that culture, take part of it, or take none at all — and
>   the third must be **named explicitly**, not implied by a general promise
>   of freedom.
> - Never frame the host culture as the thing being declined. It is what the
>   app exists to honour and preserve, so it must read as something *given*.
> - Do not write the reader's life as a set of constraints they must fit
>   around.
> - Do not position the reader as a spectator of someone else's practice.
> - Before you propose wording, check it against what the site already argues
>   on its other pages, and tell me if my draft contradicts any of it.

---

## Why the prompt is shaped this way

**"Say what a visitor gets, not how the site is organised."** The hero being
replaced read *"Two subjects, side by side. Study the Dhamma on its own, learn
Thai on its own, or follow how the two meet in Thailand's temples."* That is an
org chart. It is also built out of hedges, which makes it read as an apology for
two subjects sharing a page rather than a promise about either.

**"The third must be named explicitly."** This is the constraint that came out
of a mistake. An earlier draft promised freedom in general terms — *"find your
own way to bring the teachings into your life"* — and quietly dropped the
option of practising without adopting any cultural identity at all. A general
promise of freedom is not the same as naming the option, and a reader looking
for that specific permission will not find it in a vague one.

**"The host culture must read as something given."** A rejected draft ran
*"Keep your own culture, take on part of another, or follow none at all."* Thai
culture never appears in that sentence as itself — only as "another", unnamed,
and grammatically the one option being declined. On an app whose stated purpose
is to celebrate and preserve Thai heritage, that inversion is fatal.

**"Check it against what the site already argues."** The same rejected draft
said "follow no culture at all", which contradicts this app's own explainer page
arguing that no Buddhism sits anywhere culture-free. The fix was to borrow the
explainer's own words — *"without adopting any particular cultural identity or
tradition"* — so the front page and the explanation agree instead of
paraphrasing each other into conflict.

---

## What shipped

The live hero note now runs from *"Thai heritage is honoured, respected and
preserved; not required"* through **both** branches — explore the Dhamma as
expressed through Thai language, society, temples and traditions, **or** study
and practise it without adopting any particular cultural identity or tradition
at all — and closes *"The Dhamma is Universal!"*

See `REASONING.md` for what the AI produced versus what was actually shipped.
