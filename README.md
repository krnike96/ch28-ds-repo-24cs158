# CH28 Software Quality Insight (DS Sprint, U23AD491)

**Student:** Niket Kumar (722824104158)  
**Business question:** Which software metrics are associated with modules that have more defects?  
**Pitch focus:** code-review and testing priorities for modules with repeated quality concerns.

> **Data note:** the course gave only the schema, so the dataset is **synthetic**, generated with Python (seed 42) following the CH28 schema. Findings are associations in synthetic data, not proof of cause.

## Contents
| Path | What it is |
|---|---|
| `data/raw/` | the 5 original CSVs (modules, metrics, defects, commits, releases) |
| `data/clean/` | cleaned files, final module-release dataset (235 rows), module summary, priority tiers |
| `notebooks/CH28_EDA_FeatureEngineering.ipynb` | cleaning, EDA, feature engineering, feature selection, models |
| `excel/CH28_Excel_Analysis.xlsx` | formulas, charts, 6 pivot tables with pivot charts, Summary sheet |
| `slides/CH28_Business_Pitch.pptx` | 8-slide business pitch |
| `outputs/` | saved charts and the module priority list |

## Key results
- Top 10 of 47 modules hold 58.2% of 285 defects.
- Churn is the strongest metric (r = 0.65); coverage is negative (r = -0.39); complexity 0.35.
- 16 modules had defects in 4+ of 5 releases; 11 are Tier 1 (fix first).
- Random Forest Regressor (churn, complexity, coupling, test coverage): test RMSE 1.340, R-squared 0.424; module-level cross-validation R-squared 0.351. Classifier ROC-AUC 0.797.
