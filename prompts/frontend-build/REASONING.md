# Reasoning: Frontend Build

## Goal

Build the actual front end of the app — the web pages, the Thai-themed styling, and the interactive bits — on top of the Flask backend, as a complete beginner. I did it in stages on purpose: Option A (the HTML templates), then Option B (the CSS/design), then Option C (the JavaScript features), leaving deployment (Option D) for later.

## Iteration history

**v1 — Option A:** 6 HTML templates (base, homepage, learn hub, quiz, culture, premium) with a deep-red / gold / cream Thai theme.

**v2 — Option B:** moved the styling into external CSS files, added 50+ animations and a CSS-variable theming system.

**v3 — Option C:** added the interactive layer — flashcards, progress saving, confetti, sound effects, keyboard shortcuts.

**Then a long tail of styling fixes:** removing the royal-purple border on the dropdown menus, stopping a black box flashing on hover, making gold button text actually visible, adding a trilingual homepage title, and adding the alphabet to the nav dropdown.

## Failure modes the final version handles

- **Files in the wrong place** — most of my early "Internal Server Error" and "TemplateNotFound" problems weren't broken code; the files just weren't in the folder Flask looks in. I learned that pasting code into a chat is *not* the same as putting it in my project.
- **A missing `app.py`** — one "Internal Server Error" was simply the main file not being complete.
- **CSS leaking out of its block** — one page broke because CSS had escaped the `<style>` block into the template body.

## Outcome

A working, Thai-themed, multi-page app running locally — homepage, learning hub, quizzes, flashcards, animations. Good enough to keep building on.

## What I'd change next

The styling fixes took far too many back-and-forth rounds. Settling on a clear design system (colours, spacing, button styles) *up front* would have saved hours of "remove this border" tweaks.

## Tags

`code-generation` `frontend` `flask` `css` `beginner`
