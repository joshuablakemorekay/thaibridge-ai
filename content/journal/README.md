# Journal entries

One JSON file per entry. Drop a file in here and it appears on `/journal` —
no code change needed. Entries are read once when the app starts, so a new
file shows up on the next restart, which on Render is the deploy that carries
it anyway.

Entries are sorted by `date`, newest first. The filename doesn't matter, but
naming them `YYYY-MM-DD-slug.json` keeps the folder readable.

## Shape

```json
{
  "slug": "url-friendly-name",
  "date": "2026-08-21",
  "time": "16:40 UK time",
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
it becomes the URL, `/journal/<slug>` — and should be lowercase letters, digits
and hyphens, since it goes into the path unescaped. `time` is optional and is
shown beside the date. Any key starting with `_` is a note to ourselves and is
never rendered; `_source_note` is where an entry records whose words it is.

`tests/test_journal_content.py` checks all of that on every entry. It exists
because each of these rules fails quietly rather than loudly: a duplicate slug
makes one entry unreachable while still listing it, a mistyped block `type`
renders as an ordinary paragraph, and a date in the wrong format simply sorts
to the wrong place.

A file that isn't valid JSON is skipped with a warning in the log rather than
taking the site down, so a typo can't break `/journal` for everyone.
