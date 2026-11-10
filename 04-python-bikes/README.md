# 04 · London Bike-Hire Demand Analysis (Python)

**Status:** ⬜ Not started  |  ✅ Finished on: __________

**Question:** What actually drives bike-hire demand — time of day, weather, or season?

**Tools:** Python (pandas + matplotlib) in **Google Colab** — no installation needed
**Data:** Kaggle → search *"London Bike Sharing Dataset"*
https://www.kaggle.com/datasets?search=london%20bike%20sharing

**Expected columns:** `timestamp`, `cnt`, `t1` (temp °C), `t2` (feels like), `hum`,
`wind_speed`, `weather_code`, `is_holiday`, `is_weekend`, `season`

---

## Session 1 (60 min) — load and chart

- [ ] Open https://colab.research.google.com → **New notebook**
- [ ] Upload the CSV, or copy `analysis_starter.py` into cells
- [ ] `df.shape`, `df.head()`, `df.info()`, `df.isna().sum()`
- [ ] Convert `timestamp` to datetime, sort by it
- [ ] Create `hour`, `month`, `day_name`, `is_weekend`
- [ ] Chart 1: average hires per day (line)
- [ ] Chart 2: average hires by hour of day (bar)
- [ ] Chart 3: temperature vs hires (scatter)
- [ ] Write one markdown line under each chart

## Session 2 (60 min) — insight

- [ ] `groupby` averages by `season` and by `weather_code`
- [ ] Correlation of `cnt` with temperature, humidity, wind speed
- [ ] Compare weekend vs weekday hourly patterns
- [ ] Save 1–2 charts as PNG → `assets/`
- [ ] Write findings below
- [ ] Push notebook to GitHub **or** paste the Colab link

---

## Key findings

1. **[number]** — what it means
2.
3.

## Recommendation

> e.g. "Demand peaks at 08:00 and 17:00 on weekdays, so rebalancing bikes should happen at __."

---

## Files

- `analysis_starter.py` — starter code (paste into Colab)
- `04-bike-demand.ipynb` — your final notebook
- `assets/04-bike-demand-by-hour.png`

## Definition of done

- [ ] Notebook runs top to bottom without errors
- [ ] 3 charts, each with a caption
- [ ] 3 findings with numbers
- [ ] Committed or linked

## 60-second interview answer

"I used pandas to analyse London bike-hire data. I parsed the timestamps to get hour and
month features, then compared demand across time of day, temperature bands and seasons.
The strongest driver was **______**, and I found a correlation of **______** with
temperature. I recommended **______**. This project taught me that a good chart is just
a question made visual."
