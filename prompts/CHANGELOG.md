# Prompt Changelog

Chronological record of prompt creation and refinement. Newest entries at the top.

Each entry follows this format:
- **Date** — what changed and why

---

## market-research-report

### 2026-04-17 — v3
**Change:** Pinned a fixed 10-section structure and attached two source documents (a Product Overview and an analyst framing); kept the competitor-scraping instruction.
**Reason:** v2 was grounded but still freeform; I wanted a consistent, predictable report shape.
**Impact:** A consistently structured, source-backed report I could use to make a go/no-go decision.

### 2026-04-16 — v2
**Change:** Named the three competitors (ling-app.com, duolingo.com, thaipod101.com) and asked the model to scrape them with dedicated tools.
**Reason:** v1 was broad but not anchored to real rivals.
**Impact:** Concrete, current competitor analysis. Also surfaced a key lesson — naming a tool doesn't guarantee it runs; one scraping tool was never actually called.

### 2026-04-16 — v1
**Change:** Initial broad research request.
**Reason:** Needed a first read on the UK market for the app.
**Impact:** Good breadth, but ungrounded and unstructured.

---

## product-overview-section

### 2026-04-16 — v2
**Change:** Added answers to the model's three scoping questions (audience, emphasis, monetisation depth).
**Reason:** The bare brief left the angle ambiguous.
**Impact:** A full, structured five-part overview in one pass — later reused as a source document for the market research report.

### 2026-04-16 — v1
**Change:** Initial five-part brief (what it does / who it's for / features / problem / monetisation).
**Reason:** Needed a Product Overview section for the market research report.
**Impact:** Prompted the model to ask three scoping questions before writing.

<!-- Add more entries above as the library grows. -->
