# Reasoning: Wireframe Layout System

## Goal

I wanted my Flask app to have a consistent, professional layout instead of pages that looked "all over the place." Following the method from my web-design book, I wanted to plan the *content* first (a site outline), then design a small set of reusable layout "shapes" and apply the right one to each page — rather than forcing one layout everywhere.

## Iteration history

**v1 — "all pages?":** my first instinct was narrow — should the wireframe go on *all* pages (or maybe just the homepage)?

**v2 — content-first:** I learned a wireframe is a *planning tool, not a feature*, and that each page wants the shape that fits its job — so I switched to writing a content-first site outline first ("get the plan on paper").

**v3 — distilled:** outline → define a layout template per page type → build with reusable partials → roll out page by page → keep it responsive.

## Failure modes the final version handles

- **Forcing one layout on every page** — a 3-column layout makes simple info pages and full-width tools look wrong.
- **"Tests pass / 200 OK" hiding visual problems** — I learned to check with my own eyes (eight "broken" pages turned out to be working paywalls serving a locked page).
- **Copy-pasting the sidebar into every page** — reusable partials mean editing one file, not fourteen.
- **Wide tables getting clipped in a narrow column** — fixed with a fill-or-scroll wrapper that works at any zoom (25–500%).

## Outcome

A documented site outline, three reusable Jinja partials, the 3-column layout rolled out across the Learn / Culture / Buddhism pages, and responsive tables. Shipped (commits `ac6472a`, `eb1990c`, `8dee521` on `rebuild-experiment`).

## What I'd change next

Build the homepage's own "Landing" layout (it's still on the old design), and decide the layout shapes up front on future projects instead of retrofitting.

## Tags

`code-generation` `frontend` `flask` `css` `layout` `agent-workflow`
