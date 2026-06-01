# AI Tutor Integration (Claude API, 6 Modes)

> **Category:** agent-workflow
> **Model used:** Claude (Claude.ai for the build; Claude API / Anthropic SDK at runtime)
> **Project area:** Thai Language & Culture Learning App — in-app AI tutor
> **Status:** production (first working version — may be revised or rebuilt)
> **Last updated:** 2025-12-09

## What this prompt does

Adds an in-app AI tutor powered by the Claude API, with several specialist modes — conversation practice, grammar tutoring, quiz generation, cultural context, Buddhist teachings, and adaptive hints — built in phases starting with the core chat system.

## The prompt

**The request (verbatim):**

```
Would it be possible to create AI agent for: 1. Conversational Practice Partner
2. Intelligent Tutoring System 3. Dynamic Content Generation 4. Pronunciation
Feedback 5. Translation & Contextual Help 6. Personalized Learning Paths
7. Cultural Context AI
A chat interface where students can practice Thai conversation
* An AI tutor button on quiz pages that explains wrong answers
* A "Buddhist AI Guide" that answers dharma questions in Thai/English
* An intelligent hint system that adapts to student needs
```

**Go-ahead for the phased build (verbatim):**

```
Yes lets do your phased approach.
```

## Inputs

- The existing Flask `app.py`
- An Anthropic API key (set as an environment variable / loaded at the top of the app)
- The app's content (vocabulary, alphabet, Buddhist material) for grounded responses
- The app's Paiboon+ romanization house style

## Expected output

An `ai_agent.py` module exposing an agent with multiple modes (each with its own system prompt), a `/chat` interface (`chat.html`), and Flask routes wiring it into the app — calling the Claude API at runtime and responding in the app's romanization style.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
