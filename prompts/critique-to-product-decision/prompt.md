# Critique to Product Decision — Sorting Hostile Feedback Into Changes and Noise

**Category:** analysis
**Model:** Claude (Opus)
**Project area:** `/theravada`, `/dhamma-and-culture`, product strategy
**Status:** shipped 2026-08-20 (commits `d91a06a`, `1e77b07`)

---

## The situation

A friend of the developer sent a long, hostile critique of Thai Buddhism and of
the app's Thai focus: that Thai monks do no charity and live off free food and
envelopes of cash, that Thais have forgotten Theravada came from India, that
they live in a "Thai Culture bubble". Some of it was factually wrong, some of it
was true, and the emotional temperature made it hard to tell which was which.

The temptation in that situation is to answer it — and the app had already spent
two rounds of front-page copy answering this same person.

## Final prompt

> Now take what Chris said and Claude's response then tell me how any of this
> would affect the app as a product for making money and providing free
> teaching. Suggest any improvements I could make if any at all?

Followed by:

> Should we justify the app being focused on Thai culture? Because Chris was
> critisicing and dissaproving of it.

## What makes this prompt work

It does not ask "is he right?" — a question that produces a rebuttal nobody
ships. It asks what the criticism means **for the product**, names both things
the product is for (revenue and free teaching), and explicitly permits the
answer "no changes": *"if any at all"*.

That last clause is the load-bearing one. Without it, an assistant asked for
improvements will find some.
