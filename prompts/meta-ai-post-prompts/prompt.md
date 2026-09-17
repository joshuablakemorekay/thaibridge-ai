# Meta AI Post Prompts — Filling the Course Templates for a Real Product

**Category:** content
**Model:** drafted with Claude (Opus, via Claude Code); run in Meta AI (Llama)
**Project area:** marketing — Meta Social Media Marketing coursework, "Create a Social Media Post Using GenAI" activity
**Status:** v1 drafted and run in Meta AI 2026-09-17, output reworked by the author (see `REASONING.md`); v2 corrects the CTA domain

---

## Context

The course activity hands out two nine- and ten-section templates and asks
the learner to fill them in for their own brand, then paste them into Meta AI.
The instruction that produced these two prompts was the activity text
followed by:

> Do this for ThaiBridge-AI

Both prompts are quoted exactly as drafted. They deliberately reuse the
settled facts from [`social-media-coursework`](../social-media-coursework/)
— the same persona, the same paid Sentences page, the same platform — so
the activity's post agrees with the four coursework documents.

---

## Final prompt — text (v2)

> Please draft a social media post based on the following information.
>
> 1. Purpose of the Post: Promote ThaiBridge AI's paid Sentences page, which teaches the three Thai politeness levels (Formal, Neutral, Casual) under every sentence, plus the special words used when speaking to monks.
>
> 2. Target Audience: British adults aged 30–55 who have married into a Thai family, volunteer at a Thai temple, or visit Thailand regularly. They already know a few Thai words but worry about sounding rude or over-familiar with in-laws, elders and monks.
>
> 3. Key Message: "Knowing the words isn't enough — knowing which version to use is what makes your Thai family smile. ThaiBridge AI shows you the formal, neutral and casual way to say every sentence, so you never guess again."
>
> 4. Tone and Style: Warm, honest and encouraging, like a friend who has made the same mistakes. Plain English, no jargon. Written in the voice of the founder, a British Buddhist monk and web developer who built the app for people in exactly this situation. British spelling.
>
> 5. Call to Action (CTA): "Try the free lessons at thaibridge-ai.smoald.com, then unlock Sentences to learn all three politeness levels."
>
> 6. Hashtags and Tags: #ThaiBridgeAI #LearnThai #ThaiFamily #ThaiTemple #ThaiCulture #SMOALD
>
> 7. Platform: Facebook
>
> 8. Length: 300–400 characters, plus hashtags.
>
> 9. Additional Notes: Open with a relatable moment — accidentally using casual Thai with a mother-in-law or a monk. Do not use emojis in the first line. Mention that the app was built by a monk who learned Thai the hard way. Do not promise fluency; promise confidence.

## Final prompt — image (v1, unchanged)

> Please generate images for a social media post based on the following information.
>
> 1. Purpose of the Image: Illustrate ThaiBridge AI's Sentences page, which teaches the formal, neutral and casual way to say each Thai sentence.
>
> 2. Target Audience: British adults aged 30–55 married into a Thai family or involved with a Thai temple, who want to speak politely and respectfully to elders and monks.
>
> 3. Key Message or Theme: "One sentence, three ways to say it — choose the right one for the person in front of you."
>
> 4. Visual Style and Tone: Warm, calm and respectful, with a gentle Thai temple feel. Modern and clean rather than touristy. Friendly and reassuring, not corporate.
>
> 5. Elements to Include: A smartphone showing a simple language-learning screen with three stacked rows labelled Formal, Neutral, Casual. In the soft background, a Thai temple scene at golden hour with a lotus flower and a hint of a monk's saffron robe. A small bridge motif to echo the name "ThaiBridge". Include the ThaiBridge AI name as a logo mark.
>
> 6. Color Scheme: Royal purple #4A1A6B, deep purple #2D1B4E, gold #D4AF37, saffron orange #FF9933, silk cream #FFF8DC, white #FFFFFF.
>
> 7. Text and Typography: Include the text "One sentence. Three ways to say it." in a clean, rounded sans-serif font in gold or cream on purple. Keep text minimal and easy to read on a phone.
>
> 8. Image Format and Size: Wide 1200x628 for a Facebook feed post.
>
> 9. Platform: Facebook
>
> 10. Additional Notes: Keep any Thai script accurate or leave it out entirely — do not invent Thai-looking characters. The mood should say "respect and belonging", not "holiday". No stock-photo smiling tourists.

---

## What changed in v2

v1 — the version actually pasted into Meta AI, kept at
[`versions/v1-render-url.md`](./versions/v1-render-url.md) — pointed the CTA at
`thaibridge-ai.onrender.com`, the Render hosting URL. The live site, the README
and all four coursework documents use the custom domain
`thaibridge-ai.smoald.com`. v2 corrects it, and the rubric now fails any output
carrying the hosting URL so the next draft cannot repeat it.

It was found by writing the rubric, not by re-reading the prompt: asking what a
*wrong* output would look like is what surfaced it.

## Inputs

- The activity's two templates, section by section
- The settled coursework facts: persona (Claire, 38, Manchester, married into
  a Thai family, temple volunteer), the paid Sentences page as the thing
  shown, Facebook as the platform
- The brand colours, read from `static/css/base.css` rather than guessed —
  royal purple, deep purple, royal gold, monk saffron, silk cream

## Why the prompts are shaped this way

**Every section filled, none padded.** The course marks on all nine and all
ten sections being answered. Each answer is a real constraint the persona
justifies, not a restatement of the section heading.

**The key message is the product's actual promise.** Not "learn Thai" but
"know which version to use" — the three politeness levels are the one thing
the paid page does that Duolingo does not, and the one thing the persona was
burned by.

**"Do not promise fluency; promise confidence."** The app is live but
pre-revenue and the founder is a monk, not a marketing agency. A claim it
cannot keep would cost more than the post earns.

**"Keep any Thai script accurate or leave it out entirely."** Image models
draw Thai-shaped nonsense. For an audience with Thai family, a fake glyph in
the picture would be the first thing they noticed.

**Colours from the stylesheet, not the brief.** The course example gives hex
codes; the app already has them, so the prompt uses the real ones.

## Expected output

- A 300–400 character Facebook caption that opens with a mistake, names the
  three levels, says a monk built it, links to the site and ends with the
  hashtags — with no fluency promise
- A 1200×628 image with a phone, three labelled rows, a temple at golden
  hour, and no invented Thai script
