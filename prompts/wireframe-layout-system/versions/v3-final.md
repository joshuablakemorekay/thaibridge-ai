# v3 — final (reusable distillation)

```
Design a content-first layout system for my multi-page web app.

1. First write a site outline: list every page and what each page is FOR.
2. Define a small set of layout templates matched to each page's job — Landing,
   3-column content, Simple centered, Full-width tool. Don't force one layout on
   every page.
3. Implement the shared layout with reusable partials (sidebar + right-column
   includes) so each page opts in by filling named blocks, current page
   highlighted automatically.
4. Roll it out page by page.
5. Keep it responsive: wide tables fill the column when there's room and scroll
   sideways when they don't, at any zoom — never clip.
```

**Why this is the keeper:** it captures the whole workflow — outline → per-page templates → reusable partials → responsive — in a form I can reuse on any multi-page project, not just this one.
