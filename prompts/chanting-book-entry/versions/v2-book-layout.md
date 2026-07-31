# v2 — Make it a book you can chant from

> **Status:** verbatim from the Claude Code session, 2026-07-31.

## The instruction

```
Instruction: Make it like a book users can chant from and break it down verse by
verse just like in this example from Chat GPT
```

```
Add to Prompt 2 that it needs to make it like a book users can chant from and
break it down verse by verse. The verses need to be broken down correctly like
in the official book. Use what I pasted as an example of exactly how it should
look.
```

```
This layout follows the style of a traditional Thai chanting book: each Pali
verse stands alone, followed immediately by its Thai meaning in Paiboon
romanization, making it easy to chant the Pali and then read the meaning without
any Thai script.
```

```
Now add what's necessary to Prompt 1 for it to consistently produce outputs like
this
```

That last line is the whole point of v2. The word is **consistently**.

## The problem it fixed

v1 produced the right *content* but not reliably the right *shape*. A good run
showed its working, named its sections the way a Thai practitioner would, put
each flag beside the verse it concerned, and closed by counting what still
needed checking. A poor run did none of that — and the difference between them
was luck. **v2 made the good run the spec.**

## Four things became requirements

1. **Working notes**, in a fixed order — invitation present or absent, how many
   Pali units and how they were grouped, ordering problems, and any romanisation
   conflict in what was pasted. That last one matters because layout examples get
   pasted in from other tools: *the layout is the example, never the
   romanisation.*
2. **One Pali line per verse.** Never merged, never split, however short.
3. **Sections numbered and bilingual** — `SECTION 1 — สังขาร: The Three
   Characteristics`, not a bare English heading.
4. **Flags beside their verse, and a closing count** — *"Six things need your eye
   against the physical book."*

Also settled here: romanised Pali follows the Thai script printed beside it even
where a standard edition differs, flagging rather than silently substituting.

## Result on a real chant

Four `⚠️ CHECK` flags in one pass — a missing Pali title, a composite source, a
crossed Pali/Thai order, and a probable one-character slip in `ฉุฑโท`. None would
have been visible otherwise.

## Noted at the time, and later corrected

```
Also I did not test Prompt 1 by pasting it in Claude.ai alongside the Thai
script from book. Since Claude.ai chat is better for this than Chat GPT I should
try it.
```

This was true when written and stopped being true shortly after — Prompt 1 was
run in both Claude.ai and ChatGPT on the same page and the outputs compared. See
[REASONING.md](../REASONING.md) for the verdict.
