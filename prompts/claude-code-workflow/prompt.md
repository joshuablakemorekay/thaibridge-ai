# Claude Code Workflow (Bug Fix, Refactor, Tests, Review)

> **Category:** agent-workflow
> **Model used:** Claude Code (CLI agent that edits project files directly)
> **Project area:** Thai Language & Culture Learning App — development workflow
> **Status:** production
> **Last updated:** 2026-02-23

## What this prompt does

A set of short, specific instructions given to Claude Code to do real development work on the app — fixing a bug, refactoring, building a feature, and reviewing code — each paired with a Git commit/push so the history stays clean.

## The prompts

These were typed directly into Claude Code (not Claude.ai). Each is verbatim.

```
there's a bug where users can submit empty forms - fix it
```

```
refactor the authentication module to use async/await instead of callbacks
```

```
add input validation to the user registration form
```

Conversational Git, also verbatim:

```
what files have I changed?
```
```
commit this
```
```
push it
```

## Inputs

- The project files on disk (Claude Code reads and edits them directly)
- A Git repository connected to GitHub (for commit/push/rollback)
- A specific, small task per instruction

## Expected output

A confirmed file edit (shown as a diff to approve), applied to disk — e.g. the empty-form fix removes `novalidate` and adds `required` to each field while keeping the JavaScript validation — followed by a Git commit and push.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
