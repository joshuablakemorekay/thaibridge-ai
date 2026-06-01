# Reasoning: Claude Code Workflow (Bug Fix, Refactor, Tests, Review)

## Goal

Use **Claude Code** (the CLI tool that edits project files directly) for real development tasks on the app, paired with a safe **Git workflow** — make a change, review each edit, commit, push. The aim was as much about building good habits as shipping features: version control as a safety net, small specific tasks, and reviewing every change before accepting it.

## What I did with it (the verbatim tasks)

- *"there's a bug where users can submit empty forms - fix it"* → removed `novalidate`, added `required` to every field (two validation layers).
- *"refactor the authentication module to use async/await instead of callbacks"* → converted the signup `fetch` from `.then()` chains to `async/await` + `try/catch`.
- *"add input validation to the user registration form"* → which grew into a full SQLite user-registration system with a signup page.
- Added **32 unit tests** for the XP/level logic, did a **code review**, and fixed the high-priority issues (correct HTTP error codes, wrapping `db.session.commit()` in try/except).
- Conversational Git: *"what files have I changed?"*, *"commit this"*, *"push it"*.

## Failure modes / lessons

- **Which terminal does what** — Claude Code once reported the project "isn't a git repo" because it was running from a different directory; I learned to keep Claude Code edits and Git commands straight.
- **Edits are real and immediate** — Claude Code writes to disk the moment you confirm, so setting up Git *first* means you can roll back fearlessly.
- **Small, specific tasks + review each edit** — far safer than a big vague request.
- **Two products, two bills** — Claude Code is billed separately from the Claude.ai subscription; when it ran out of credits I made two fixes **by hand** and understood what they did.

## Outcome

A registration system, an empty-form bug fix, an async refactor, 32 passing tests, and code-review fixes — all committed and pushed with a clean, readable history.

## What I'd change next

I decided to adopt **feature branches + pull requests** going forward (instead of committing straight to `main`), and to move the developer password and API key into environment variables.

## Tags

`claude-code` `git` `workflow` `testing` `code-review` `refactoring`
