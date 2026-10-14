# Translator Mode: a Pro Chat Mode Built on the Rules the App Already Teaches

**Category:** agent-workflow
**Model:** Claude (Opus) to build it, Sonnet 5.5 to run it
**Project area:** `/chat`, the AI tutor's seventh mode
**Status:** shipped 2026-10-14 (Thai output is unreviewed AI output, and says so)

---

## Final prompt

> Can we build a proficient translator feature for the app?

Claude read the tutor's code before answering, found six modes and no
translator, and proposed a seventh mode rather than a new page. I chose:

> yes, plan it as a Pro chat mode

and, after reading the four-step plan:

> yes, build it

The translator's own instructions, the part that runs on every request, are in
[`context/translator_mode_prompt.txt`](./context/translator_mode_prompt.txt).

---

## Why the prompt is shaped this way

**"Proficient", not "simple".** A word-swap translator is what every free app
already does, and it is wrong for Thai in a specific way: the same English
sentence has different Thai depending on who is speaking and who is listening.
Asking for *proficient* is what led to politeness levels, the dropped "I" and
the monk vocabulary being part of every answer rather than extras.

**"As a Pro chat mode."** The chat already had the model, the politeness rules,
the checked word list, the fair-use limit and the Pro lock. A separate page would
have had to rebuild all five. A chat also makes follow-ups free: "to a friend?"
re-translates on the casual level without a settings screen.

**Plan before build.** The plan named every file it would touch and the tests
that would prove each step, so "yes, build it" approved something specific.
