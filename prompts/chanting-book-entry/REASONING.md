# Reasoning: Chanting Book Entry

## Goal

> *"Rather than thinking of it as a 'chanting page,' think of it as a Digital
> Chanting Book. Then, when you publish the printed edition, you're polishing
> and typesetting content that has already been tested by users."*

> *"When you later publish the printed edition, very little content will need
> changing. The web app becomes the interactive version — with collapsible
> sections and optional text layers — while the physical book presents the same
> material in a carefully typeset, permanent format. This gives your project a
> consistent identity across both digital and print, rather than treating them
> as two separate resources."*

Every chant answers the same six questions: *"What is this chant? Where does it
come from? When is it chanted? Why was it taught? What does it mean? How do I
chant it?"*

The prompt exists so that *"everytime I decide to add a new chant to the app
Digital Chanting Book, what gets added to the app ends up looking exactly as I
want it thanks to Prompt 1 and 2 plus my pasted Thai script."*

## Why two stages on two surfaces

| Stage | Surface | Why there |
|---|---|---|
| 1 | Claude.ai chat | Language work — transliteration, romanisation, translation, background. It needs reading and correcting, which suits a chat window. |
| 2 | Claude Code | File work — writing a Python dict into `chanting.py` and proving it renders. Needs an agent that can run the app. |

Splitting them also puts a human checkpoint in the middle, which is where the
verification against the physical book actually happens.

## The register the prompt has to preserve

> *"It's mostly Central Thai, but it uses a formal literary register that is
> traditional in Buddhist scriptures and chanting books. It is not Royal Thai,
> and it is not a separate 'monk language.'"*

> *"Think of it as the Thai equivalent of the language used in an English Bible
> or the Book of Common Prayer — recognizably modern English, but more formal,
> traditional, and rich in religious vocabulary."*

## What the layout has to be

> *"Make it like a book users can read/chant from and break it down verse by
> verse. The verses need to be broken down correctly like in the official
> book. Use what I pasted as an example of exactly how it should look."*

> *"This layout follows the style of a traditional Thai chanting book: each Pali
> verse stands alone, followed immediately by its Thai meaning in Paiboon
> romanization, making it easy to chant the Pali and then read the meaning
> without any Thai script."*

## The layers, as specified

> *"Each chant is presented in five optional layers to support both learning and
> practice. Pali (Thai script) — the original chant as recited in Thai Theravāda
> temples. Pali (Romanised) — the same Pali written in the Latin alphabet to aid
> pronunciation. Thai translation — the meaning in Thai. In many Thai temples,
> this is also recited after the Pali. Thai (Paiboon) — the Thai translation
> romanised for readers who cannot yet read Thai script. English translation —
> the meaning in English."*

> *"Show only the layers you need. As your confidence grows, try chanting
> directly from the Pali while using the translations to deepen your
> understanding."*

## The standard section order, as specified

> *"Standard Layout for Every Chant. Each chant follows the same format. Title.
> Pali Source — the original source of the chant, such as the Dhammapada,
> Khuddakapāṭha, Suttanipāta or another canonical text. When Chanted — when the
> chant is traditionally recited in Theravāda practice. Historical Background —
> a brief explanation of the historical setting or occasion in which the Buddha
> taught the verses, or the origin of the chant if composed later. Meaning and
> Purpose — a concise explanation of the teaching and why Buddhists continue to
> chant it today. The Chant."*

## The questions that found the bugs

Two questions that were not reporting faults each turned one up, and the pattern
is worth recording as much as the fixes:

> *"Does the JSON from Stage 1 mean the Stage 1 output? Is it the same thing?"*

> *"Is the JSON object and it's closing sentence contained in the whole Stage 1
> reply? Or do I get it from elsewhere?"*

> *"Did you update the Stage 2 prompt in GitHub? I can't see any changes."*

## Iteration — four versions in one day

| | Change | Cause |
|---|---|---|
| [v1](versions/v1-labelled-text.md) | Two stages, labelled-text output | First working version |
| [v2](versions/v2-book-layout.md) | Working notes, bilingual sections, inline flags, closing count | A good run and a poor run differed only by luck. The good run became the spec. |
| [v3](versions/v3-json-output.md) | JSON, single-line values, checks as an array | *"JSON with unwrapped single-line values and the checks as a separate array."* |
| [v4](versions/v4-migration-complete.md) | Migration finished; notes moved inside the JSON; `title_roman` added | Asking whether "the JSON" and "the output" were the same thing showed they weren't. Reading stage 2 to prove it had shipped exposed three rules pointing at labels that no longer existed. |

## Failure modes the final version handles

**Reconstruction from memory.** Four OCR errors were caught against the physical
book on chant 1. A model asked to tidy those would have rewritten the text into
something that reads perfectly and isn't the book.

**Silent tidying.** *"Just do it without changing anything from the book i.e.
don't change what I pasted."*

**Grouped verses.** One Pali line per verse, never merged, however short.

**Filling gaps to look complete.** *"Forget the Pali title here because there is
none for the pasted script."* No Pali title, no invitation, no certain source —
leave them empty and say so.

**Romanisation drift.** A self-contradicting instruction does not error; it
splits the difference. `generate_paiboon.py` said `ง → ng` on one line and
showed `waŋ not wang` on the next, producing roughly a 65/35 mix across 900
dictionary cells. Found by asking:

> *"Which one is actually correct? Which one does the official chanting book
> with Thai script use? They both have different pronunciations."*

This is the sharpest prompt-engineering lesson in the folder. The fix lived in
another script, but the cause was a prompt that disagreed with its own example.

## How fidelity is verified

Compare every Thai and Pali character against the source **in both directions** —
every character present, and no character present that was not in the source.
Chant 2 came out 869 in, 869 out.

That the file imports and the page returns 200 proves neither.

## How the surface was chosen

Stage 1 was run in **both Claude.ai and ChatGPT against the same page of the
official chanting book**, and the two outputs compared side by side. Claude.ai
was clearly better for this job, so the workflow is built around it.

The verdict, in full:

> *"Claude.ai gave the working notes and flagged issues, ChatGPT just gave
> output. The Claude output is better on the things your spec says matter most —
> source fidelity and flagging — and ChatGPT is better in two specific places I
> got wrong. The single most serious difference isn't romanisation at all; it's
> a meaning error in ChatGPT's verses 4–5."*

Two things in that are worth holding onto. **The obvious difference and the
important difference were not the same difference** — romanisation is what shows
up first when two outputs sit side by side, and it is the more harmless of the
two; a reader mispronounces a word. A wrong translation is invisible on a skim
and teaches the wrong Dhamma.

And the verdict was not one-sided. Recording where the losing tool was better
matters more than a clean win would.

> TODO — Josh to fill in: what exactly was wrong in ChatGPT's verses 4–5, and
> which two places did ChatGPT handle better? Both belong here in his own words
> rather than reconstructed.

A secondary finding, since it fed straight into the prompt: one output used RTGS
spellings (`sangkhaan`, `khɔ̌ɔng`, `thîang`) where this app uses Paiboon+
(`sǎŋ-kǎan`, `kɔ̌ɔŋ`, `tîaŋ`), and one dropped the Pali-in-Thai-script layer
entirely. Both are now explicit rules — the consonant table is pinned, and a
pasted sample is declared a *layout* example, never a romanisation one.

## What I'd change next

- The rubric checks the *shape* of the output. Only the physical book can check
  whether the Pali is right.
- Source attribution is the weakest field, which is why an inferred one is
  marked `⚠️ UNVERIFIED` in the data.

**Tags:** `content` `agent-workflow`
