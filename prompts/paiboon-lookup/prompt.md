# Paiboon Lookup — Search the Romanisation You Already Have

**Category:** code-generation
**Model:** Claude (Opus)
**Project area:** `paiboon_lookup.py`, `/paiboon`
**Status:** shipped 2026-08-19 — `e368522`, live

---

## Final prompt

> I want a Paiboon lookup tool: a small utility a learner reaches for daily,
> so they stay in the app between lessons.
>
> Before proposing an implementation, tell me what it *can* be. Search the
> codebase and find out whether a Thai-to-Paiboon transliterator already exists
> here, and if not, what the realistic options are. Give me the trade-off on
> each — cost, accuracy, and specifically what happens when it is WRONG.
>
> Assume the person using this is a beginner. They cannot tell a correct tone
> mark from an incorrect one; that is why they are looking it up. Weigh the
> options with that in mind rather than by which is most impressive.
>
> Then build the one I choose, and nothing else.
>
> Two things I care about more than coverage:
> - A miss must read as a miss. Never a confident guess.
> - It must be findable by someone typing what they think they heard, not what
>   Paiboon spells. Test it against the phrases beginners actually type.
>
> Put it on the page that already does this job rather than a new route.

---

## Why this prompt is shaped this way

**"Tell me what it can be" before "build it"** is the whole reason this
shipped correct. The obvious reading of "Paiboon lookup tool" is a
transliterator. There isn't one in the codebase and there shouldn't be — every
romanisation the app ships was either hand-written or generated offline and
reviewed.

**"Specifically what happens when it is WRONG"** is the question that killed the
live-AI option. Every option looks fine on its happy path.

**"Assume the person using this is a beginner"** anchors the whole trade-off. A
tool that is right 90% of the time is useless to someone who cannot tell which
90%.

**"Test it against the phrases beginners actually type"** is what turned up the
real work. The first cut could not find "sawatdee" or "khop khun" — the two most
common phrases in the language — because Paiboon spells them `sà-wàt-dii` and
`kɔ̀ɔp-kun`.

**"The page that already does this job"** kept it off a new route. `/paiboon`
already answers "how is this written?" in principle; the box answers it for one
word.
