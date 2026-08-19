# Reasoning: Survival Thai

## Goal

The free tier was Buddhism plus an alphabet chart. Someone who came to *speak*
Thai could finish nothing without paying. I asked for the smallest thing that
fixed that:

> One full survival module — greetings, numbers, food, directions. Finishable,
> genuinely useful.

## Iteration history

**v1 — the module.** Approved as one of five free-tier proposals, and rated the
strongest of them.

**v2 — where does it go?** I asked the placement question rather than assuming:

> would you agree that survival mode is right to be placed in Tour Guide page or
> not?

The answer was no, with the facts: Tour Guide is `{'level': 4, 'tier': 'basic',
'requires_alphabet': True}`. Putting free content there would have meant either
freeing a paid section or burying the taster behind £9.99, level 4 and 44
consonants. That question is the reason this is its own section.

**v3 — making it findable.** After it shipped I asked what was left, and the
answer was that the home page did not mention it once. A free front door nobody
can find does nothing.

## Failure modes the final version handles

- **Free but unreachable.** Free tier alone was not enough. The alphabet gate is
  checked *first* in `check_section_access`, before level and tier, so this
  needed `requires_alphabet: False` as well — the only language page on the site
  you can reach knowing nothing.
- **Freeing a paid section by accident.** A test asserts Tour Guide *stays*
  `basic`, so if that ever changes the justification for the split is gone and
  someone gets told to think again.
- **Growing out of its purpose.** "Finishable" is enforced, not intended — a
  test fails if the phrase count leaves the 30–70 range.
- **Teaching half the learners to sound wrong.** ครับ and ค่ะ are both shown on
  every phrase that needs a particle, matching how `/gender-examples` already
  handles it.
- **Reciting a template out loud.** `ไป...ครับ/ค่ะ` is a shape with a blank for
  a place name. It is excluded from the audio strings, or the recording would be
  nonsense.
- **A draft passing as checked.** An amber banner on the page says the Thai is
  unreviewed and links to `/contact`. In the page, where a learner sees it.

## Outcome

Shipped in `e298ab9`, live at `/survival`. 50 phrases in four sets, 20 tests.
Audio followed in `9c0c77e` — 26 new recordings, and the page is now 51/51.
The home page change is `0492089`.

**It wired itself into three places for free**, which is the part worth
noticing. It appears on the public curriculum outline because it carries
`@require_access`; its phrases joined the Paiboon lookup because that walks
modules rather than a hand-kept list; and it registered with the audio build
script through one collector. Half its clips already existed, because phrase
audio is stored under a hash of the Thai — anything another page had already
taught arrived with its recording.

**The home page was the gap I nearly left.** The language card pointed at
`/alphabet` and said *"Starts with the 44 consonants"* — the exact wall this
section exists to route around. It now opens on `/survival`, badged "no alphabet
needed", and Survival Thai is step 1 of the Thai Language Path. Two tests pin
both, because an unlinked page fails silently.

## Engineering on the output

- *Accepted as-is:* the module, the page, the tests and the home page rework.
- *Reworked, and why:* nothing at the code level this session.
- *Decisions made:* build it as its own section rather than folding it into
  Tour Guide; make it ungated as well as free; keep Tour Guide paid; put it
  first on the home page and in the learning path rather than merely linking it.
- *Roughly:* shipped as-is on code, with the direction and the product
  decisions mine.

> Review of this file was delegated — I asked for a recommendation rather than
> approving each section line by line.

The placement question is the one I would point a reader at. Building it into
Tour Guide would have looked reasonable in a diff and quietly defeated the whole
feature.

## What I'd change next

The Thai is a first draft and the audio is synthesised, so the page currently
teaches pronunciation nobody has checked. The banner is honest about it, but
honesty is not the same as correctness, and this is the page beginners meet
first — the worst place on the site for an unreviewed tone.

It is also four lists with no way to practise. Every other section has a drill
or a quiz; this one has cards. "Finishable" would mean more if there were
something to finish rather than something to read.

## Tags

`content` `free-tier` `onboarding` `flask` `accessibility` `thai`
