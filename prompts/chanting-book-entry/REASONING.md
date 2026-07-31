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
> book."*

> *"Each Pali verse stands alone, followed immediately by its Thai meaning in
> Paiboon romanization, making it easy to chant the Pali and then read the
> meaning without any Thai script."*

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

**The decisive difference was process, not polish.** Claude.ai returned working
notes and a list of flagged issues alongside the entry; ChatGPT returned the
entry only. On a task whose whole premise is *never invent canonical Pali*, a
tool that tells you what it was unsure about is doing the job, and a tool that
hands over a clean-looking answer with nothing flagged is hiding the thing you
most need to see. Claude.ai was better on the two criteria the spec says matter
most — source fidelity and flagging — so the workflow is built around it.

**The most serious single difference was not romanisation.** It was a *meaning*
error in ChatGPT's verses 4–5. That is worth recording precisely because
romanisation is the difference that shows up first when you skim two outputs
side by side: it is visible, it is everywhere, and it is comparatively harmless
— a reader mispronounces a word. A wrong translation is invisible on a skim and
teaches the wrong Dhamma. **The obvious difference and the important difference
were not the same difference.**

ChatGPT was better in two specific places. Neither verdict was one-sided, and
recording that matters more than a clean win would.

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
