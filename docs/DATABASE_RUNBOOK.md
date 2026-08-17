# Database runbook

How to look at the live database, answer the everyday questions, and change
things without breaking them.

This is deliberately **in the repo rather than a PDF**. A PDF describing a
database goes out of date the moment a column changes and has no way of telling
you — which is the exact failure this project keeps running into. Here, a schema
change and the note describing it land in the same commit. The last section
gives you a way to check this file is still true rather than trusting it.

---

## Getting in

1. **https://console.neon.tech** — sign in the way you created the account
2. Open the **thaibridge-ai** project
3. The tools are in the project's left sidebar

Two ways to work, and they suit different jobs:

| | Use it for |
|---|---|
| **Tables** | Looking, and point-and-click edits. A spreadsheet view: filter columns, click a cell to change it, tick rows and delete them, export CSV/JSON. |
| **SQL Editor** | Anything that counts, sums or groups. Saves queries for reuse and keeps a history. Pick branch `main` and database `neondb`. |

Rule of thumb: **Tables to look at one row, SQL Editor to ask a question.**

Quickest check you are in the right place — run this in the SQL Editor:

```sql
SELECT count(*) FROM users;
```

That is the same database the live site writes to. If a number comes back, you
are connected.

---

## The everyday questions

**Who has signed up**

```sql
SELECT id, username, email, subscription_tier, created_at
FROM users
ORDER BY created_at DESC;
```

**What the AI is costing, per day**

```sql
SELECT date(created_at)                                   AS day,
       count(*)                                           AS messages,
       count(DISTINCT coalesce(user_id::text, session_key)) AS people,
       sum(input_tokens)                                  AS tokens_in,
       sum(output_tokens)                                 AS tokens_out,
       round((sum(input_tokens) * 1.00
            + sum(output_tokens) * 5.00) / 1000000.0, 4)  AS usd
FROM ai_usage
WHERE outcome = 'ok'
GROUP BY 1
ORDER BY 1 DESC;
```

The prices in that sum are **Claude Haiku 4.5 list rates** ($1 per million input
tokens, $5 per million output). They are written into the query, not the table,
on purpose: the row stores tokens and the model name, so when the model or the
price changes, this query gains a `CASE` and every old row stays correct.

**Is anyone hitting the limits** — the conversion question

```sql
SELECT outcome, tier, count(*)
FROM ai_usage
WHERE outcome LIKE 'blocked%'
GROUP BY 1, 2
ORDER BY 3 DESC;
```

`blocked_cap` is a free user out of their 15 a day. `blocked_mode` is someone
reaching for a Pro-only mode. `blocked_fairuse` is a Pro subscriber past 150 —
if that ever appears, look at who and why before changing the number.

**Is the AI failing**

```sql
SELECT date(created_at), error_type, count(*)
FROM ai_usage
WHERE outcome = 'error'
GROUP BY 1, 2
ORDER BY 1 DESC;
```

**What one person has been doing**

```sql
SELECT u.username, a.created_at, a.mode, a.outcome,
       a.input_tokens, a.output_tokens
FROM ai_usage a
JOIN users u ON u.id = a.user_id
WHERE u.username = 'someone'
ORDER BY a.created_at DESC
LIMIT 50;
```

---

## Changing things without breaking them

**The one rule: never run `DELETE` or `UPDATE` without a `WHERE`.**

`DELETE FROM users;` removes every account. There is no undo and no
confirmation — it reports "500 rows affected" in exactly the same tone it would
report one.

**The habit that prevents it: write it as a `SELECT` first, then swap the verb.**

```sql
SELECT * FROM users WHERE username = 'testaccount';   -- look at it
DELETE  FROM users WHERE username = 'testaccount';    -- then delete it
```

If the `SELECT` returns forty rows when you expected one, you have just saved
yourself. This costs three seconds and is the single most useful habit here.

**Deleting a user who has AI usage rows** — remove the usage first, or the
foreign key will refuse:

```sql
DELETE FROM ai_usage WHERE user_id = (SELECT id FROM users WHERE username = 'x');
DELETE FROM users    WHERE username = 'x';
```

**Starting genuinely fresh** (empties both tables and restarts ids at 1):

```sql
DELETE FROM ai_usage;
DELETE FROM users;
ALTER SEQUENCE users_id_seq    RESTART WITH 1;
ALTER SEQUENCE ai_usage_id_seq RESTART WITH 1;
```

---

## Before you try something risky: branch

Neon can copy the whole database instantly as a **branch**. Nothing you do to a
branch touches the real data.

Create one, point a local run at its connection string, break whatever you like,
then delete it. This is the right way to test a migration, a bulk update, or any
query you are not sure about — and it is the main reason Neon is a good choice
while you are learning.

The SQL Editor also has **Time Travel**, which queries how the data looked at an
earlier moment. Worth knowing about before the day you need it.

---

## When something looks wrong

Work outwards, cheapest check first:

1. **Is the site up?** Load the home page.
2. **Is the database up?** `SELECT 1;` in the SQL Editor.
3. **Is the app talking to *this* database?** Sign up on the live site, then
   look for the row here. If it does not appear, the app is not connected to
   what you are looking at — check `DATABASE_URL` in the Render dashboard.
4. **Is it deployed?** Render can serve old code while reporting itself healthy.
   Check the Events tab shows the commit you expect, not just "Live".

That order matters. Step 3 is the one that catches the confusing failures,
because a site that is up and a database that is up can still be strangers.

---

## Checking this file is still true

Rather than listing the columns here, where they would rot quietly, ask the
database:

```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

If that returns tables or columns this document does not mention, **this document
is out of date and the database is right.** Update it in the same commit as
whatever changed.

At the time of writing there are two tables: `users` (accounts, subscription
state, and a `progress` JSON column) and `ai_usage` (one row per AI request).
