# 02 · Chinook Customer & Sales Analysis (SQL)

**Status:** ⬜ Not started  |  ✅ Finished on: __________

**Question:** Who are the most valuable customers, which markets generate the most revenue, and which products never sell?

**Tools:** SQL (SQLite) — DB Browser for SQLite, or sqliteonline.com
**Data:** Chinook sample database (a digital music store: customers, invoices, tracks)
https://www.kaggle.com/datasets?search=chinook
Alternative: https://github.com/lerocha/chinook-database

---

## Why Chinook

It is small (11 tables, a few thousand rows) but relational — perfect for showing
`JOIN`, `GROUP BY`, CTEs, window functions and subqueries, which is exactly what
UK SQL screening tests check.

**Tables you will use:** `Customer`, `Invoice`, `InvoiceLine`, `Track`, `Album`, `Artist`, `Genre`

---

## Session 1 (60 min)

- [ ] Download the SQLite file (`.sqlite` / `.db`)
- [ ] Open it in DB Browser → **Database Structure** tab → read the tables
- [ ] Skim `queries.sql` Q1–Q6 in this folder
- [ ] Run each one, then **close the file and rewrite it from memory**
- [ ] Change the filter in at least 3 queries (e.g. another country)
- [ ] Save your version in `queries.sql`

## Session 2 (60 min)

- [ ] Write Q7 (CTE)
- [ ] Write Q8 (window function)
- [ ] Write Q9 (subquery)
- [ ] Write Q10 (CASE WHEN segmentation)
- [ ] Add one query of your own
- [ ] Write the findings below

---

## Key findings

1. **[number]** — what it means
2.
3.

## Recommendation

> e.g. "The top 20% of customers generate __% of revenue, so the business should…"

---

## Files

- `queries.sql` — all queries with explanations
- `assets/02-sql-top-customers.png` — screenshot of one result

## Definition of done

- [ ] `queries.sql` runs top-to-bottom with no errors
- [ ] At least one CTE, one window function, one subquery
- [ ] 3 findings written with numbers
- [ ] Pushed to GitHub

## 60-second interview answer

"In my SQL project I analysed the Chinook music store database. I used joins to connect
customers to invoices and tracks, then CTEs and window functions to rank customers
within each country. I found that **______**, which suggests **______**. It taught me
how to break a business question into a chain of joins and aggregations."
