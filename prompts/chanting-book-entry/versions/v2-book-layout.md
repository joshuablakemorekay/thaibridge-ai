# v2 — Make it a book you can chant from

> **Status:** verbatim from the Claude Code session, 2026-07-31.

```
Make it like a book users can read/chant from and break it down verse by verse.
The verses need to be broken down correctly like in the official book. Use what
I pasted as an example of exactly how it should look.
```

```
This layout follows the style of a traditional Thai chanting book: each Pali
verse stands alone, followed immediately by its Thai meaning in Paiboon
romanization, making it easy to chant the Pali and then read the meaning
without any Thai script.
```

**The problem v2 fixed.** v1 produced the right *content* but not reliably the
right *shape*. A good run showed its working, named its sections the way a Thai
practitioner would, put each flag beside the verse it concerned, and finished by
counting what still needed checking. A poor run did none of that — and the
difference between them was luck. v2 made the good run the spec.

**Four things became requirements:**

1. **Working notes**, in a fixed order — invitation present or absent, how many
   Pali units and how they were grouped, ordering problems, and any romanisation
   conflict in what was pasted. That last one matters because layout examples
   get pasted in from other tools: *the layout is the example, never the
   romanisation.*
2. **One Pali line per verse.** Never merged, never split, however short. A
   reader must be able to chant one line, read what it means, and move on —
   that is the whole test.
3. **Sections numbered and bilingual** — `SECTION 1 — สังขาร: The Three
   Characteristics`, not a bare English heading. A long chant is several short
   reflections, and the Thai name is what a Thai practitioner calls that
   movement.
4. **Flags beside their verse, and a closing count.** *"Six things need your eye
   against the physical book."* That count is the most useful line in the reply:
   it says how much verifying the chant needs before it goes in the app.

**Also settled here:** romanised Pali follows the Thai script printed beside it
even where a standard edition differs — flagging rather than silently
substituting, so the two chanted layers never disagree without explanation.

**Result on a real chant:** four `⚠️ CHECK` flags in one pass — a missing Pali
title, a composite source, a crossed Pali/Thai order, and a probable
one-character slip (`ฉุฑโท`). None would have been visible otherwise.
