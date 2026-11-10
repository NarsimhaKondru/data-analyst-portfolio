# 03 · Sales Dashboard (Power BI)

**Status:** ⬜ Not started  |  ✅ Finished on: __________

**Question:** How is the business performing — revenue, profit and growth — at a glance?

**Tools:** Power BI Desktop (free). Fallback if install is blocked: Looker Studio in the browser.
**Data:** Kaggle → search *"Superstore Sales"*
https://www.kaggle.com/datasets?search=superstore%20sales

---

## Session 1 (60 min) — model the data

- [ ] Download CSV → `data/raw/superstore_raw.csv`
- [ ] Power BI → **Get Data → Text/CSV → Transform Data**
- [ ] In Power Query: set data types, trim text, remove nulls in key columns
- [ ] Rename columns to clean names (`Sales`, `Profit`, `Order Date`, `Category`, `Region`)
- [ ] **Create a Date table** (New Table):

```dax
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2024, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "mmm" ),
    "Month Number", MONTH ( [Date] )
)
```

- [ ] Mark as date table
- [ ] Relationships: `Sales[Order Date]` → `Date[Date]` (many-to-one)
- [ ] Save as `superstore_dashboard.pbix`

---

## Session 2 (60 min) — measures + dashboard

- [ ] Create these measures (**New Measure**):

```dax
Total Sales  = SUM ( 'Sales'[Sales] )
Total Profit = SUM ( 'Sales'[Profit] )
Profit %     = DIVIDE ( [Total Profit], [Total Sales] )
Orders       = DISTINCTCOUNT ( 'Sales'[Order ID] )

YoY Growth =
VAR CurrentYear = [Total Sales]
VAR PriorYear   = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
RETURN DIVIDE ( CurrentYear - PriorYear, PriorYear )
```

- [ ] Layout, one page only:
  - KPI cards across the top: Sales · Profit · Profit % · Orders
  - Line chart: Sales by month (use `Date[Date]`)
  - Bar chart: Sales by Category
  - Bar chart: Sales by Region
  - Slicer: Year, Region
- [ ] Format: consistent colours, data labels on, no clutter, readable font size
- [ ] **Publish to web** (File → Embed report → Publish to web) → copy the link
- [ ] Screenshot → `assets/03-powerbi-dashboard.png`

---

## Key findings

1. **[number]** — what it means
2.
3.

## Recommendation

> e.g. "Technology is the most profitable category at __%, but the __ region is loss-making — investigate discounting there."

---

## Files

- `superstore_dashboard.pbix` (not committed — see `.gitignore`)
- `assets/03-powerbi-dashboard.png`
- Live link: __________

## Definition of done

- [ ] Dashboard loads with no errors
- [ ] At least 4 DAX measures used
- [ ] Screenshot + live link in this README
- [ ] Pushed to GitHub

## 60-second interview answer

"I built a one-page Power BI dashboard on Superstore sales data. I cleaned it in Power Query,
added a proper Date table so time intelligence works, and wrote DAX measures for sales,
profit margin and year-on-year growth. The dashboard shows **______**. My main design
decision was **______**, because a manager needs the headline first and detail second."
