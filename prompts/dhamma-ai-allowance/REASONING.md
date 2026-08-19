# Reasoning: Dhamma AI Allowance

## Goal

This started as the fifth item on a list of giveaways, in three words:

> Small free Dhamma allowance

It came back not as a giveaway but as a bug report, which is the right answer
and not the one I was expecting.

## Iteration history

**v1 — as a giveaway.** Asked alongside four other free-tier proposals. The
answer reframed it: the Dhamma was already free, and the thing that needed
fixing was that the *code* did not honour the position the *comment* stated.

**v2 — the fix, with a constraint.** Two ways to do it came back:

- Reserve 5 of the existing 15 — costs nothing, cuts everyone's tutor allowance
  from 15 to 10.
- Add a separate 5 on top — nobody loses anything, about 1.4p a day for someone
  who exhausts it daily.

The second shipped. Nobody should lose something so the site can keep a promise
it had already made.

## Failure modes the final version handles

- **The principle and the gate disagreeing.** The comment above
  `FREE_AI_DAILY_LIMIT` says charging for the follow-up question would be
  selling the Dhamma. The gate checked one shared counter with no reference to
  `mode`, so tutor and Dhamma drained the same 15. A learner who drilled
  vocabulary all morning and then asked about the precepts was told to come back
  tomorrow or upgrade.
- **Fixing the gate and leaving the sales pitch.** Both refusal messages were
  rewritten. Running out of *Dhamma* questions offers no upgrade at all; running
  out of *tutor* messages now names the Dhamma questions still in hand **before**
  it mentions Pro.
- **The hint under the chat box.** It showed one number for both modes, so
  switching to Dhamma looked like it spent the tutor's messages. It follows the
  mode now — and carries no upsell on the Dhamma side in either state.
- **A session opened before the split.** Old sessions have no `dhamma` key.
  `setdefault` fills it rather than every call site defaulting, and the tutor
  key keeps its original name so nobody's tally resets at rollout.

## Outcome

Shipped in `be35854`, live. Dhamma has its own 5 a day; the tutor keeps its full
15. 12 new tests, the sharpest being
`test_the_tutor_cannot_eat_the_dhamma_allowance`.

**The bug the tests caught in my own fix.** The first cut of `AI_POOLS` copied
the limit *values* into the dict. That quietly made it a second source of truth
that won: the constants above still looked authoritative but no longer
controlled the gate, and an existing test's `monkeypatch` of
`FREE_AI_DAILY_LIMIT` stopped biting. It now stores the constant's *name* and
reads it at call time. The only reason this was noticed is that the existing
test failed — which is the argument for the suite in one line.

**Wording, verified without a browser.** Chrome could not reach the test server
after a restart, so the hint function was pulled out of the *served* HTML and
run under Node against all five states. All correct, singular and plural right,
and an assertion confirmed no Dhamma line contains an upsell.

## Engineering on the output

- *Accepted as-is:* the pool split, the counter, the rewritten refusals and the
  tests.
- *Reworked, and why:* nothing at the code level this session.
- *Decisions made:* add the allowance on top rather than reserving it out of
  the existing 15; treat this as a bug rather than a feature; accept removing
  the upsell from the Dhamma hint entirely, not just from the refusal.
- *Roughly:* shipped as-is on code, with the direction and the product
  decisions mine.

> Review of this file was delegated — I asked for a recommendation rather than
> approving each section line by line.

The no-upsell-on-the-hint change went further than I asked for and was flagged
as such before it shipped. I let it stand: a "go Pro" beside your remaining
Dhamma questions is the same objection as charging for them, just quieter.

## What I'd change next

The counter still lives in the session, which was a deliberate choice when it
was one shared number — no schema change, and it works for logged-out visitors.
It is a soft limit; clearing cookies resets it. That was fine for a demo
allowance and is slightly less fine now that one of the two pools exists to
protect a stated principle rather than to meter cost.

Five a day is also a guess, not a measured figure. It wants watching against
what a real Dhamma conversation needs — five questions is not many if someone
is actually working something through.

## Tags

`analysis` `bug-fix` `ethics` `monetization` `flask` `testing`
