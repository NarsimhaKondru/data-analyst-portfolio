# 05 · A/B Test Analysis (Python)

**Status:** ⬜ Not started  |  ✅ Finished on: __________

**Question:** Did the new design actually increase conversion — or is the difference just noise?

**Tools:** Python (pandas + scipy) in Google Colab
**Data:** run `ab_test_starter.py` as-is (it generates realistic test data), **or** use a
real one: Kaggle → search *"A/B testing"*
https://www.kaggle.com/datasets?search=a%2Fb%20testing

---

## Why this project matters

Most junior analysts can build a chart. Far fewer can say **"the difference is / isn't
statistically significant"** and explain it. This is the project that makes you sound
like an analyst rather than a spreadsheet user.

**Concepts to be able to explain:**

| Term | Plain English |
|---|---|
| Conversion rate | % of users who did the action |
| Absolute lift | treatment % − control % |
| Relative lift | absolute lift ÷ control % |
| p-value | chance of seeing this result if there were no real difference |
| 95% CI | range the true difference probably sits in |
| Significant | p < 0.05 **and** the CI excludes zero |

---

## Session 1 (60 min)

- [ ] New Colab notebook, paste `ab_test_starter.py` (or upload a real dataset)
- [ ] Inspect the data: rows, groups, conversions
- [ ] Table: users, conversions, conversion rate per group
- [ ] Calculate absolute lift and relative lift
- [ ] Run the two-proportion z-test → get z and p-value
- [ ] Run `chi2_contingency` as a cross-check
- [ ] Calculate the 95% confidence interval for the difference

## Session 2 (60 min)

- [ ] Bar chart: conversion rate by group with % labels
- [ ] Write a verdict in **plain English** (no stats jargon in the first sentence)
- [ ] Add a "what I would tell the business" paragraph
- [ ] Push notebook to GitHub or paste the Colab link

---

## Key findings

1. Control: **__%** · Treatment: **__%** → absolute lift **__ pp** (relative **__%**)
2. p-value = **__** → significant / not significant
3. 95% CI = **[__, __]** → what it means for the decision

## Recommendation

> e.g. "Ship the new version / do not ship / run the test longer because __."

---

## Files

- `ab_test_starter.py`
- `05-ab-test.ipynb`
- `assets/05-ab-test-results.png`

## Definition of done

- [ ] Conversion table, lift, p-value, CI all present
- [ ] A single-sentence verdict a non-technical manager would understand
- [ ] Chart saved and committed

## 60-second interview answer

"I ran an A/B test analysis. I compared conversion rates between control and treatment,
calculated the absolute and relative lift, then tested significance with a two-proportion
z-test and checked it with a chi-square test. The result was **______** with a p-value of
**______**, so my recommendation was **______**. The key lesson was that a higher number
is not automatically a win — you have to check whether the difference is real."
