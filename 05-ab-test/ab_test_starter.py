"""
Project 05 - A/B Test Analysis
==============================

Runs out of the box with realistic synthetic data, so you can focus on the
statistics instead of hunting for a dataset.

How to use:
  COLAB  -> paste into a notebook, run top to bottom.
  LOCAL  -> pip install pandas numpy scipy matplotlib
            python ab_test_starter.py

To use a REAL dataset instead: download one from Kaggle ("A/B testing"),
then replace section 1 with something like:

    df = pd.read_csv("ab_data.csv")
    df = df.rename(columns={"group": "group", "converted": "converted"})

and make sure `df` ends up with two columns: `group` (control/treatment)
and `converted` (0/1).
"""

from __future__ import annotations

import math
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:  # Colab always has scipy; a local install might not
    from scipy import stats
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

SAVE_DIR = "assets"
os.makedirs(SAVE_DIR, exist_ok=True)
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


# ---------------------------------------------------------------------------
# 1. DATA  (synthetic: 10,000 users, 10% control rate, +1.5pp true lift)
# ---------------------------------------------------------------------------
rng = np.random.default_rng(14)

N = 10_000
CONTROL_RATE = 0.10
TRUE_LIFT = 0.015  # the effect we planted; the test should find it

df = pd.DataFrame({
    "user_id": np.arange(1, N + 1),
    "group": rng.choice(["control", "treatment"], size=N),
})
df["converted"] = np.where(
    df["group"] == "control",
    rng.random(N) < CONTROL_RATE,
    rng.random(N) < CONTROL_RATE + TRUE_LIFT,
).astype(int)

print("Rows:", len(df))
print("\nUsers per group:\n", df["group"].value_counts())
print("\nConversion by group (proportions):\n", df.groupby("group")["converted"].mean())


# ---------------------------------------------------------------------------
# 2. SUMMARY TABLE
# ---------------------------------------------------------------------------
summary = (
    df.groupby("group")["converted"]
    .agg(users="count", conversions="sum", conversion_rate="mean")
    .rename_axis("group")
)
summary["conversion_pct"] = (summary["conversion_rate"] * 100).round(2)

control = summary.loc["control"]
treatment = summary.loc["treatment"]

abs_lift = treatment["conversion_rate"] - control["conversion_rate"]
rel_lift = abs_lift / control["conversion_rate"]

print("\n--- RESULTS ---")
print(summary[["users", "conversions", "conversion_pct"]])
print(f"\nAbsolute lift : {abs_lift * 100:+.2f} percentage points")
print(f"Relative lift : {rel_lift * 100:+.2f}%")


# ---------------------------------------------------------------------------
# 3. SIGNIFICANCE TEST (two-proportion z-test)
# ---------------------------------------------------------------------------
p1, p2 = control["conversion_rate"], treatment["conversion_rate"]
n1, n2 = control["users"], treatment["users"]

p_pool = (control["conversions"] + treatment["conversions"]) / (n1 + n2)
se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
z = (p2 - p1) / se_pool

# Two-sided p-value. scipy if available, otherwise the identical maths:
# erfc(|z| / sqrt(2)) == 2 * (1 - Phi(|z|))
if HAVE_SCIPY:
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
else:
    p_value = math.erfc(abs(z) / math.sqrt(2))

# 95% confidence interval for the difference (unpooled standard error)
se_diff = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
ci_low, ci_high = (p2 - p1) - 1.96 * se_diff, (p2 - p1) + 1.96 * se_diff

print(f"\nz-statistic   : {z:.3f}")
print(f"p-value       : {p_value:.4f}")
print(f"95% CI (diff) : [{ci_low * 100:+.2f} pp, {ci_high * 100:+.2f} pp]")


# ---------------------------------------------------------------------------
# 4. CROSS-CHECK WITH CHI-SQUARE
# ---------------------------------------------------------------------------
if HAVE_SCIPY:
    table = pd.crosstab(df["group"], df["converted"])
    chi2, p_chi2, dof, expected = stats.chi2_contingency(table)
    print(f"\nChi-square    : {chi2:.3f} (p = {p_chi2:.4f}, dof = {dof})")
else:
    print("\nChi-square    : skipped (scipy not installed - run this in Colab)")


# ---------------------------------------------------------------------------
# 5. VERDICT (write your own words in the README too)
# ---------------------------------------------------------------------------
alpha = 0.05
significant = (p_value < alpha) and (ci_low > 0 or ci_high < 0)

print("\n--- VERDICT ---")
if significant and abs_lift > 0:
    print(f"Significant WIN: treatment lifted conversion by {rel_lift * 100:.1f}% (p = {p_value:.4f}).")
elif significant and abs_lift < 0:
    print(f"Significant LOSS: treatment reduced conversion by {abs(rel_lift) * 100:.1f}% (p = {p_value:.4f}).")
else:
    print(f"No significant difference (p = {p_value:.4f}). Do not ship on this evidence.")


# ---------------------------------------------------------------------------
# 6. CHART
# ---------------------------------------------------------------------------
plt.figure(figsize=(7, 4))
bars = plt.bar(
    ["Control", "Treatment"],
    [control["conversion_rate"] * 100, treatment["conversion_rate"] * 100],
    color=["#8c8c8c", "#1f77b4"],
    width=0.5,
)
for bar, value in zip(bars, [control["conversion_rate"] * 100, treatment["conversion_rate"] * 100]):
    plt.text(bar.get_x() + bar.get_width() / 2, value + 0.1, f"{value:.2f}%", ha="center")

plt.title(f"Conversion rate by group (p = {p_value:.4f})")
plt.ylabel("Conversion rate (%)")
plt.ylim(0, max(control["conversion_rate"], treatment["conversion_rate"]) * 100 * 1.3)
plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/05-ab-test-results.png", dpi=150)
plt.show()

# ---------------------------------------------------------------------------
# NOW WRITE YOUR FINDINGS in the README:
#   1. conversion rates + lift
#   2. p-value + CI -> significant or not
#   3. what you would tell the business
# ---------------------------------------------------------------------------
