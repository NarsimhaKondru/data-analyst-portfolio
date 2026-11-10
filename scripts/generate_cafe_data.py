"""
Generate a realistic *messy* cafe sales dataset for the Excel cleaning project.

This is SIMULATED data (not real transactions). It deliberately contains the
problems a real analyst deals with, so that cleaning it is a genuine exercise:

  - exact duplicate rows
  - missing values written as "", ERROR, UNKNOWN, N/A, NaN
  - three different date formats, plus a few impossible dates
  - item / payment / location names with inconsistent case and spacing
  - prices stored as text with a pound sign for some rows
  - negative, zero and absurd quantities
  - Total Spent that does not always equal Quantity x Price
  - five completely blank rows

Run:
    python scripts/generate_cafe_data.py

Output:
    data/raw/cafe_sales_raw.csv      (~10,000 rows + duplicates)

The seed is fixed, so everyone who runs it gets the same file.
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

SEED = 2024
N = 10_000
OUT_PATH = os.path.join("data", "raw", "cafe_sales_raw.csv")

MENU = {
    "Coffee": 2.60,
    "Latte": 3.20,
    "Cappuccino": 3.10,
    "Tea": 2.20,
    "Sandwich": 4.80,
    "Salad": 5.50,
    "Cake": 3.40,
    "Cookie": 1.80,
    "Smoothie": 4.20,
    "Juice": 3.00,
}

UNKNOWN = ["", "ERROR", "UNKNOWN", "N/A", "NaN"]

rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# 1. Build the "clean" truth
# ---------------------------------------------------------------------------
days = pd.date_range("2024-01-01", "2024-12-31", freq="D")
doy = np.arange(len(days))
# busier in winter, quieter in August
day_weight = 1 + 0.25 * np.cos(2 * np.pi * (doy - 14) / 365)
day_idx = rng.choice(len(days), size=N, p=day_weight / day_weight.sum())
dates = days[day_idx]

hours = np.arange(7, 19)                      # 07:00 - 18:00
hour_weight = np.array([6, 14, 18, 12, 8, 15, 18, 14, 9, 6, 4, 2], dtype=float)
hours_picked = rng.choice(hours, size=N, p=hour_weight / hour_weight.sum())
minutes = rng.integers(0, 60, N)

is_weekend = np.isin(dates.day_of_week, [5, 6])
morning = (hours_picked >= 7) & (hours_picked <= 11)
lunch = (hours_picked >= 12) & (hours_picked <= 14)
afternoon = hours_picked >= 15

items = np.empty(N, dtype=object)
for block, weights in [
    (morning, {"Coffee": 24, "Latte": 16, "Cappuccino": 11, "Tea": 13, "Sandwich": 7,
               "Salad": 2, "Cake": 6, "Cookie": 6, "Smoothie": 2, "Juice": 2}),
    (lunch, {"Coffee": 8, "Latte": 9, "Cappuccino": 6, "Tea": 6, "Sandwich": 22,
             "Salad": 14, "Cake": 8, "Cookie": 6, "Smoothie": 4, "Juice": 5}),
    (afternoon, {"Coffee": 12, "Latte": 11, "Cappuccino": 8, "Tea": 10, "Sandwich": 7,
                 "Salad": 4, "Cake": 16, "Cookie": 13, "Smoothie": 4, "Juice": 4}),
]:
    names = list(weights)
    p = np.array([weights[n] for n in names], dtype=float)
    p = p / p.sum()
    items[block] = rng.choice(names, size=block.sum(), p=p)

# weekends sell more cake/cookies
weekend_snack = is_weekend & (rng.random(N) < 0.08)
items[weekend_snack] = rng.choice(["Cake", "Cookie"], size=weekend_snack.sum())

quantity = rng.choice([1, 2, 3], size=N, p=[0.70, 0.25, 0.05])
unit_price = np.array([MENU[i] for i in items], dtype=float)
total = np.round(quantity * unit_price, 2)

hour_ts = pd.to_datetime(dates) + pd.to_timedelta(hours_picked, unit="h") + pd.to_timedelta(minutes, unit="m")

payment = rng.choice(["Card", "Cash", "Digital Wallet"], size=N, p=[0.55, 0.20, 0.25])
location = rng.choice(["In-store", "Takeaway"], size=N, p=[0.62, 0.38])

df = pd.DataFrame({
    "Transaction ID": [f"TXN-{i:06d}" for i in range(1, N + 1)],
    "Item": items,
    "Quantity": quantity,
    "Price Per Unit": unit_price,
    "Total Spent": total,
    "Payment Method": payment,
    "Location": location,
    "Transaction Date": hour_ts,
})

# make numeric columns object so we can inject text "missing" markers
for col in ("Quantity", "Price Per Unit", "Total Spent"):
    df[col] = df[col].astype(object)

# ---------------------------------------------------------------------------
# 2. Now make it messy
# ---------------------------------------------------------------------------
def inject_unknown(column: str, fraction: float) -> None:
    idx = rng.choice(len(df), size=int(len(df) * fraction), replace=False)
    df.loc[idx, column] = rng.choice(UNKNOWN, size=len(idx))


def inject_variants(column: str, fraction: float) -> None:
    idx = rng.choice(len(df), size=int(len(df) * fraction), replace=False)
    for i in idx:
        value = str(df.at[i, column])
        style = rng.integers(0, 4)
        if style == 0:
            value = value.lower()
        elif style == 1:
            value = value.upper()
        elif style == 2:
            value = "  " + value + " "
        else:
            value = value.replace(" ", "  ") if " " in value else value + " "
        df.at[i, column] = value


# quantities that make no sense
neg_idx = rng.choice(len(df), size=12, replace=False)
df.loc[neg_idx, "Quantity"] = -rng.integers(1, 4, len(neg_idx))
zero_idx = rng.choice(len(df), size=6, replace=False)
df.loc[zero_idx, "Quantity"] = 0
out_idx = rng.choice(len(df), size=3, replace=False)
df.loc[out_idx, "Quantity"] = 999

# Total Spent that does not match Quantity x Price
mismatch_idx = rng.choice(len(df), size=150, replace=False)
for i in mismatch_idx:
    try:
        df.at[i, "Total Spent"] = round(float(df.at[i, "Total Spent"]) * rng.choice([0.8, 1.2, 1.5]), 2)
    except (TypeError, ValueError):
        pass

# prices stored as text
price_idx = rng.choice(len(df), size=int(N * 0.03), replace=False)
for i in price_idx:
    try:
        df.at[i, "Price Per Unit"] = f"£{float(df.at[i, 'Price Per Unit']):.2f}"
    except (TypeError, ValueError):
        pass

# missing values
inject_unknown("Quantity", 0.03)
inject_unknown("Price Per Unit", 0.025)
inject_unknown("Total Spent", 0.02)
inject_unknown("Payment Method", 0.02)
inject_unknown("Location", 0.02)

# inconsistent text
inject_variants("Item", 0.08)
inject_variants("Payment Method", 0.10)
inject_variants("Location", 0.10)

# a few missing transaction IDs
df.loc[rng.choice(len(df), size=5, replace=False), "Transaction ID"] = ""

# ---------------------------------------------------------------------------
# 3. Dates in three formats, plus impossible dates
# ---------------------------------------------------------------------------
fmt = rng.choice(["iso", "uk", "long"], size=len(df), p=[0.60, 0.25, 0.15])
date_strings = []
for ts, f in zip(df["Transaction Date"], fmt):
    if f == "iso":
        date_strings.append(ts.strftime("%Y-%m-%d"))
    elif f == "uk":
        date_strings.append(ts.strftime("%d/%m/%Y"))
    else:
        date_strings.append(ts.strftime("%d %b %Y"))
df["Transaction Date"] = date_strings

bad_date_idx = rng.choice(len(df), size=10, replace=False)
for i in bad_date_idx:
    df.at[i, "Transaction Date"] = rng.choice(["2024-13-45", "31/02/2024", "not a date", "00/00/2024"])

# ---------------------------------------------------------------------------
# 4. Duplicates and blank rows
# ---------------------------------------------------------------------------
dupes = df.sample(n=140, random_state=SEED)
blanks = pd.DataFrame([{c: np.nan for c in df.columns}] * 5)
df = pd.concat([df, dupes, blanks], ignore_index=True)
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 5. Write
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
# utf-8-sig adds a BOM so Excel displays the pound sign correctly
df.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")

print(f"Wrote {len(df):,} rows x {len(df.columns)} columns to {OUT_PATH}")
print("\nColumns:", list(df.columns))
print("\nDeliberate problems injected:")
print("  - 140 exact duplicate rows + 5 blank rows")
print("  - missing values as '', ERROR, UNKNOWN, N/A, NaN")
print("  - 3 date formats + 10 impossible dates")
print("  - inconsistent Item / Payment Method / Location spellings and spacing")
print("  - 12 negative and 6 zero quantities, 3 x quantity 999")
print("  - 150 rows where Total Spent != Quantity x Price")
print("  - prices stored as text with a pound sign")
