# Journal entries

One JSON file per entry. Drop a file in here and it appears on `/journal` —
no code change needed.

Entries are sorted by `date`, newest first. The filename doesn't matter, but
naming them `YYYY-MM-DD-slug.json` keeps the folder readable.

## Shape

```json
{
  "slug": "url-friendly-name",
  "date": "2026-08-21",
  "title": "The title of the entry",
  "subtitle": "Optional one-line subtitle",
  "summary": "A short paragraph shown on the /journal index card.",
  "blocks": [
    "A plain string is the shorthand for an ordinary paragraph.",
    { "type": "heading", "text": "A section heading" },
    { "type": "quote", "text": "A quoted passage.", "attribution": "Who said it" },
    { "type": "pali", "text": "Sabbadānaṃ dhammadānaṃ jināti",
      "translation": "The gift of Dhamma surpasses all gifts." },
    { "type": "th", "text": "ภาษาไทย", "translation": "The English of that line." }
  ]
}
```

Only `slug`, `date`, `title` and `blocks` are required. `slug` must be unique —
it becomes the URL, `/journal/<slug>`.

A file that isn't valid JSON is skipped with a warning in the log rather than
taking the site down, so a typo can't break `/journal` for everyone.
