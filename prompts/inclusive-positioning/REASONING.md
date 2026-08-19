# Reasoning: Inclusive Positioning

## Goal

I sent the app to a European friend who visits Thai temples, so she could learn
Paiboon and use the Digital Chanting Book. She came back with something I did not
expect — not a complaint about the Thai, but about the framing:

> Why any culture needs to be combine with practises or Buddhism itself
> For me to keep it pure ot is better non cultural
> Different cultures can also divide people on different side
> Than it is ego and separation

She was not the only one:

> The main problem is anyone who is not Thai seem to be getting offended and
> upset perhaps feeling left out or excluded, possibly even discriminated or
> segregated due to the Thai culture aspect of it not being something they
> appreciate as it is not their culture.

So the question I actually needed answered was:

> How can we adapt the app to appeal to people who want Buddhism as universal.
> Buddhism taught like pure dhamma without the association of any culture or
> society? So that anyone in any part of the world feels they can learn it and
> adapt what they learn as to practice it wherever they are in the world; in
> whatever culture or society they exist? Is it possible to adapt the app like
> this while also preserving the existing Thai cultural side of it?

That last clause is the constraint that made it hard. Removing the Thai material
would have been easy and would have gutted the project.

## Iteration history

**v1 — the diagnosis.** I asked the question above and got a fix proposed
straight away. Adding "check the access rules before proposing anything" is what
turned it from a copy rewrite into a finding: the app's own `SECTION_REQUIREMENTS`
already made `theravada`, `meditation`, `chanting` and `paiboon` free, level 1,
with `requires_alphabet: False` — and the comment beside `chanting` even reads
*"you do not need to read Thai to chant along."* The permissions were right. The
shop window was lying about them.

**v2 — the two constraints.** Both were added because the first attempt got it
wrong in a way I could see and the model could not. They are in the prompt now so
the mistake is not repeatable.

## Failure modes the final version handles

- **Reading it as a translation problem.** The five-layer chanting system already
  solved accessibility. Nothing about adding more layers would have touched what
  she was objecting to.
- **Assuming the fix is to remove the Thai material.** It is the most
  distinctive thing in the project. The problem was never its presence, it was
  its apparent compulsoriness.
- **Trusting the copy over the gate logic.** The home page said "pass the quiz to
  unlock the site". No Buddhism page has ever been behind that quiz.
- **Substituting one country for another.** See below.

## Outcome

Shipped in five commits and live the same day:

| Commit | What |
|---|---|
| `80a8712` | `/dhamma-and-culture` and `/practising-anywhere` — two free, ungated pages |
| `5b113d6` | Home page "What are you here to learn?" chooser; the false unlock line removed |
| `8ab233e` | The wording pass — 27 insertions, 27 deletions, pure rewording |
| `c7fa28d` | Tests guarding the promises |
| `4167bc9` | Two nav strings the wording pass missed |

The strongest single artifact is `/practising-anywhere`, which teaches lay
practice with **no country named anywhere on the page**, and says so out loud.
That was only possible by building it from the Canon's own frameworks — the five
precepts, the three bases of merit, and the six directions of the Sigālovāda
Sutta. The six directions are universal by construction: every society has
parents, teachers, partners, friends, people who work and people who teach.

## Engineering on the output

- **Accepted as-is:** the two-lens structure (universal Dhamma beside its Thai
  expression), the four-door home chooser, and the decision to keep every piece
  of Thai cultural material.

- **Reworked — the country substitution.** The draft illustrated lay practice
  with "practising the precepts in Britain". I pushed back:

  > practising the precepts in Britain? How about Britain and other places around
  > the world? Isn't this supposed to be universal? Is it possible not to mess
  > with any of the existing content?

  That is the correction that produced the best page in the set. Naming my own
  country instead of Thailand is not universality, it is the same move with a
  different flag. The rebuild dropped worked examples entirely — because every
  worked example smuggles a culture back in — and used canonical frameworks
  instead. A test now fails if Britain, America, Europe or "the West" reappears
  on that page.

- **Reworked — the label.** "Foreigner" was renamed to "non-Thai" across the app
  on my instruction, to address bias. Looking at the result, I asked:

  > Is there a better name than non-Thai?

  It is politer and structurally identical — both define a reader by not
  belonging. The answer was to notice that almost every sentence carrying the
  label already addressed the reader as "you", which made the label redundant.
  *"As a foreigner, you're NOT expected to initiate wai"* became *"You're not
  expected to initiate the wai."* Shorter, warmer, and no category at all.

- **Reworked — Monk Mode.** The non-Thai side of the monk track was described
  throughout as "Western monks". That was never the criterion; monks learning
  Thai come from Sri Lanka, Myanmar, Cambodia, Indonesia, Brazil. Both sides are
  now described by the language they are learning.

- **Roughly:** the structure and the diagnosis went in as-is; the language went
  through two full rounds of correction from me, and the second one changed the
  approach rather than the wording.

## What I'd change next

The "you" in the etiquette pages still quietly assumes the reader is not Thai.
That is fair on a page teaching Thai etiquette in English, but it is an
assumption rather than a fact, and I have not decided whether it is worth
solving.
