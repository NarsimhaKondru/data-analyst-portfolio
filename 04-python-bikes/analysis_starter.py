"""
Project 04 - London Bike-Hire Demand Analysis
=============================================

How to use:
  COLAB  -> open a new notebook, paste this file into cells, run in order.
            The `files.upload()` call will ask you for the CSV.
  LOCAL  -> put the CSV at data/raw/london_bike_sharing.csv
            pip install pandas matplotlib
            python analysis_starter.py

If column names differ from the ones below, run  print(df.columns)  first
and rename them, e.g.:   df = df.rename(columns={"Count": "cnt"})
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("display.width", 120)
plt.rcParams["figure.figsize"] = (10, 4)
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

SAVE_DIR = "assets"
os.makedirs(SAVE_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
try:  # Colab only
    from google.colab import files  # type: ignore

    uploaded = files.upload()  # pick london_bike_sharing.csv
    PATH = list(uploaded.keys())[0]
except ImportError:  # running locally
    PATH = "data/raw/london_bike_sharing.csv"

df = pd.read_csv(PATH)

print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nDtypes:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum())
print("\nFirst rows:\n", df.head())


# ---------------------------------------------------------------------------
# 2. CLEAN + FEATURE ENGINEERING
# ---------------------------------------------------------------------------
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# The dataset uses `timestamp`; rename if yours differs.
if "timestamp" not in df.columns:
    for candidate in ("date", "datetime", "time"):
        if candidate in df.columns:
            df = df.rename(columns={candidate: "timestamp"})
            break

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.dropna(subset=["timestamp", "cnt"]).sort_values("timestamp")

df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["month"] = df["timestamp"].dt.month
df["day_name"] = df["timestamp"].dt.day_name()
df["is_weekend"] = df["timestamp"].dt.day_of_week >= 5

print("\nDate range:", df["timestamp"].min(), "->", df["timestamp"].max())
print("\nDescribe:\n", df[["cnt", "t1", "hum", "wind_speed"]].describe())


# ---------------------------------------------------------------------------
# 3. CHART 1 - demand over time (daily average)
# ---------------------------------------------------------------------------
daily = df.set_index("timestamp")["cnt"].resample("D").mean()

plt.figure()
plt.plot(daily.index, daily.values)
plt.title("Average bike hires per day")
plt.ylabel("Hires")
plt.xlabel("")
plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/04-bike-demand-over-time.png", dpi=150)
plt.show()

print("\nBusiest month:", daily.groupby(daily.index.month).mean().idxmax())
print("Quietest month:", daily.groupby(daily.index.month).mean().idxmin())


# ---------------------------------------------------------------------------
# 4. CHART 2 - demand by hour of day (weekday vs weekend)
# ---------------------------------------------------------------------------
plt.figure()
for label, mask in [("Weekday", ~df["is_weekend"]), ("Weekend", df["is_weekend"])]:
    series = df.loc[mask].groupby("hour")["cnt"].mean()
    plt.plot(series.index, series.values, marker="o", label=label)

plt.title("Average hires by hour of day")
plt.xlabel("Hour")
plt.ylabel("Average hires")
plt.xticks(range(0, 24, 2))
plt.legend()
plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/04-bike-demand-by-hour.png", dpi=150)
plt.show()


# ---------------------------------------------------------------------------
# 5. CHART 3 - temperature vs demand
# ---------------------------------------------------------------------------
plt.figure()
plt.scatter(df["t1"], df["cnt"], s=6, alpha=0.25)
plt.title("Temperature vs bike hires")
plt.xlabel("Temperature (C)")
plt.ylabel("Hires")
plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/04-bike-demand-vs-temp.png", dpi=150)
plt.show()


# ---------------------------------------------------------------------------
# 6. GROUPBY + CORRELATION  (the actual analysis)
# ---------------------------------------------------------------------------
print("\nAverage hires by season:\n", df.groupby("season")["cnt"].mean().sort_values(ascending=False))
print("\nAverage hires by weather code:\n", df.groupby("weather_code")["cnt"].mean().sort_values(ascending=False))

numeric = [c for c in ("cnt", "t1", "t2", "hum", "wind_speed") if c in df.columns]
print("\nCorrelation with demand:\n", df[numeric].corr()["cnt"].sort_values())

busiest_hour = df.groupby("hour")["cnt"].mean().idxmax()
print(f"\nBusiest hour of the day: {busiest_hour}:00")


# ---------------------------------------------------------------------------
# 7. EXPORT
# ---------------------------------------------------------------------------
df.to_csv(f"{SAVE_DIR}/04-bike-clean.csv", index=False)
print(f"\nSaved 3 charts + clean data to ./{SAVE_DIR}/")

# ---------------------------------------------------------------------------
# NOW WRITE YOUR FINDINGS in the README:
#   1. numbers, 2. numbers, 3. numbers + one recommendation
# ---------------------------------------------------------------------------
