# 10-Day Checklist — 1 hour per day

**Rule:** finish the session, not the project. Small and done beats big and abandoned.

Legend: `[ ]` todo · `[x]` done

---

## Day 0 — Setup (20 min)

- [ ] GitHub account created
- [ ] Kaggle account created
- [ ] Power BI Desktop installed (fallback: Looker Studio)
- [ ] DB Browser for SQLite installed (fallback: sqliteonline.com)
- [ ] Google Colab reachable (no install needed)
- [ ] This folder opened in VS Code / Explorer
- [ ] GitHub repo created and this folder pushed

---

## Week 1

### Day 1 — Project 01: clean (60 min)
- [ ] Raw CSV downloaded to `data/raw/cafe_sales_raw.csv`
- [ ] Duplicates removed
- [ ] Dates fixed
- [ ] Blanks handled (and decision noted)
- [ ] Categories standardised
- [ ] `Total` column added
- [ ] 3 pivot tables built
- [ ] 3 findings written in `01-excel-sales/README.md`

### Day 2 — Project 01: dashboard (60 min)
- [ ] Dashboard sheet built (3–4 charts + 2 slicers)
- [ ] KPI tiles at the top
- [ ] Screenshot saved to `assets/`
- [ ] Recommendation line written
- [ ] Pushed to GitHub
- [ ] **Project 01 finished**

### Day 3 — Project 02: SQL basics (60 min)
- [ ] Chinook database downloaded
- [ ] Tables browsed in DB Browser
- [ ] Q1–Q4 written and running
- [ ] `queries.sql` saved with comments

### Day 4 — Project 02: SQL advanced (60 min)
- [ ] CTE query written
- [ ] Window function query written
- [ ] Subquery written
- [ ] Customer segmentation (CASE WHEN) written
- [ ] Insights written in README
- [ ] **Project 02 finished**

### Day 5 — Project 03: Power BI model (60 min)
- [ ] Superstore CSV loaded
- [ ] Power Query cleaning done
- [ ] Date table created
- [ ] Relationships set (Sales → Date / Product / Customer)
- [ ] `.pbix` saved

### Day 6 — Project 03: Power BI dashboard (60 min)
- [ ] 4 DAX measures created
- [ ] One-page dashboard built
- [ ] Published to web
- [ ] Link + screenshot added to README
- [ ] Pushed to GitHub
- [ ] **Project 03 finished**

### Day 7 — Project 04: Python EDA (60 min)
- [ ] Dataset loaded in Colab
- [ ] Missing values / dtypes checked
- [ ] 3 charts built
- [ ] Markdown notes under each chart

---

## Week 2

### Day 8 — Project 04: Python insights (60 min)
- [ ] `groupby` analysis by season / weather
- [ ] Correlation matrix
- [ ] 3 findings + 1 recommendation written
- [ ] Notebook pushed (or Colab link added)
- [ ] **Project 04 finished**

### Day 9 — Project 05: A/B test (60 min)
- [ ] Data loaded (synthetic or Kaggle)
- [ ] Conversion rates per group
- [ ] Significance test run
- [ ] Confidence interval calculated
- [ ] Bar chart built

### Day 10 — Project 05 + packaging (60 min)
- [ ] Verdict written in plain English
- [ ] **Project 05 finished**
- [ ] Root `README.md` progress table updated
- [ ] 5 CV bullets written
- [ ] LinkedIn post published with a screenshot
- [ ] Repo link added to CV header

---

## If you fall behind

Cut in this order — never skip Project 01, 02 or 03:

1. Project 05 → notebook only, no chart
2. Project 04 → 2 charts instead of 3
3. Project 03 → drop `YoY Growth`, 3 measures is enough
4. Project 01 → skip slicers

**Never cut:** the README write-up. The findings are what gets you the interview.
