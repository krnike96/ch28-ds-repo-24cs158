# CH28 – Software Quality Insight: Project Plan (Single Source of Truth)

**Student:** Niket Kumar | **Register No:** 722824104158 | **Challenge:** CH28 – Software Quality Insight
**Course:** U23AD491 – Data Science | DS Sprint – Skill Based Assessment 2
**Last updated:** 12 Oct 2026

> **How to resume in a new chat:** upload this file and say:
> *"I'm continuing my CH28 DS Sprint project. Read PROJECT_PLAN.md, check the Status Tracker, and continue from the first unfinished phase."*
> Update the Status Tracker (Section 2) and the Decision Log (Section 12) after every phase.

---

## 1. What this is

A Data Science assessment (100 marks). I act as an analyst for the fictional company **CodeMetric Software Labs**.

**Business question:** *Which software metrics are associated with modules that have more defects?*

**Pitch focus:** Recommend code-review and testing priorities for modules showing repeated quality concerns.

| Round (PDF) | Stage | Marks |
|---|---|---|
| 1 | Quiz (MCQ: analytics, pre-processing, EDA, feature engineering, Excel, NumPy, Pandas, Matplotlib, Seaborn) | 20 |
| 2 | EDA and Feature Engineering (Python notebook) | 30 |
| 3 | Data Analysis using Excel | 30 |
| 4 | Pitching Business Insights (slides) | 20 |

**Final deliverables:** cleaned dataset, Python notebook (EDA + feature engineering), Excel workbook (analysis, charts, pivots, summary sheet), short presentation, GitHub repo link, plus the mandatory handwritten summary sheet (Section 10).

**Rules from the professor:** do not exchange challenges; upload completed work to GitHub and submit the repo link; write only important points and real obtained results on the sheet (no code).

**Important mismatch:** the PDF groups rounds as Quiz / EDA / Excel / Pitch, but the professor's sheet (Mail 2) groups them as Data Prep + EDA / Feature Engineering + **Machine Learning** / Visualization + Prototype. So the project must include an ML model even though the PDF does not mention one. Cover both.

---

## 2. Status Tracker

| Phase | Name | Status |
|---|---|---|
| 0 | Setup (Drive, Colab, GitHub) | Not started |
| 1 | Load and audit the data | **Done** (results in Section 3a) |
| 2 | Clean the data | **Done** (results in Section 3b) |
| 3 | Merge and feature engineering | **Done** (results in Section 3c) |
| 4 | EDA (answer the 6 questions) | **Done** (results in Sections 3d and 3e) |
| 5 | Feature selection and ML model | **Done** (3f, 3g, 3h); tier file generated: Tier 1 = 11, Tier 2 = 13, Tier 3 = 23 |
| 6 | Excel workbook | **Done**: 12 analysis sheets plus a Pivots sheet (6 pivot tables, 6 pivot charts); all 3,046 formulas checked, 0 errors. Open once in desktop Excel to confirm pivots refresh |
| 7 | Presentation (pitch) | **Done**: `CH28_Business_Pitch.pptx`, 8 slides with speaker notes |
| 8 | GitHub, summary sheet, final check | In progress: summary sheet text drafted; still to do: add Class, push repo, paste GitHub link, handwrite sheet |
| Q | Round 1 quiz preparation (parallel, anytime) | Not started |

Done so far: challenge understood, dataset generated, plan written, Phase 0 (setup), Phase 1 (audit), Phase 2 (clean) and Phase 3 (merge and feature engineering). Phase 4 (EDA, all 6 questions) done, Phase 5 (feature selection, regression, classifier, risk ranking) done. **Next: generate the tiered priority file, then Phase 6 (Excel workbook): upload the final CSVs to Claude, which builds the workbook; pivots are added by me in Excel.**

---

## 3. Dataset (synthetic, already generated)

The professor gave no data files, only the schema in the PDF, so a synthetic dataset was generated with Python (**seed 42**) following that schema. Say this openly in the README, notebook and sheet. Source to write on the sheet: *"Synthetic, generated using Python (seed 42) per the CH28 schema."*

Files: `ch28_dataset.zip` containing `modules.csv, metrics.csv, defects.csv, commits.csv, releases.csv, generate_ch28_data.py, README.md`.

| File | Rows | Columns |
|---|---|---|
| modules.csv | 47 | module_id, module, component, language, size (lines of code) |
| metrics.csv | 249 | module, release, complexity, coupling, churn, test_coverage |
| defects.csv | 216 | defect_id, module, release, defect_count, severity (Low/Medium/High/Critical) |
| commits.csv | 235 | module, release, commit_count, contributors, changed_lines |
| releases.csv | 247 | release_id, version, release_date, module |

- 47 modules, 6 components (Auth, Payments, UI, Database, API, Reporting), 4 languages (Python, Java, JavaScript, C++).
- 5 releases: v1.0, v1.1, v2.0, v2.1, v3.0. Clean analysis level = **module x release = 235 rows** (47 x 5).
- Join keys: `module` (needs cleaning) and `release` (called `version` in releases.csv).
- 8 hidden "problem modules" have persistently high complexity, high churn and low coverage.

**Injected data problems (what to find and fix in Phase 1 and 2):**

| Problem | Where | Detail |
|---|---|---|
| Missing metric values | metrics.csv (about 6% per metric column), commits.csv contributors (7 blanks) | 58 nulls in metrics |
| Duplicate rows | metrics.csv (14), releases.csv (12) | exact duplicates |
| Inconsistent module names | metrics, defects, commits, releases | UPPER CASE, Title Case, leading/trailing spaces, hyphens instead of underscores |
| Extreme complexity | metrics.csv | 7 values between about 200 and 300 (normal is about 10 to 30) |
| Unmatched defect records | defects.csv | 18 rows (53 defects) across 5 names not in modules.csv: payments_crypto, ui_widgets_old, auth_sso_beta, tmp_migration, reporting_v0 |

Rough correlations with defect count seen in a quick check (a guide only, do not quote in the sheet): churn about +0.67, test_coverage about -0.40, complexity about +0.35, coupling about +0.34. **Always report what my own notebook produces.**

---

## 3a. Phase 1 audit results (real numbers from my notebook, 12 Oct 2026)

| Check | File | Result |
|---|---|---|
| Rows | modules / metrics / defects / commits / releases | 47 / 249 / 216 / 235 / 247 |
| Missing values | metrics | 58 cells: complexity 14, coupling 15, churn 15, test_coverage 14 |
| Missing values | commits | 7 (all in `contributors`) |
| Missing values | modules, defects, releases | 0 |
| Exact duplicate rows | metrics / releases | 14 / 12 (so metrics should be 235 after dedupe) |
| Raw module-name variants | metrics / defects / commits / releases | 102 / 94 / 96 / 106 distinct names, collapsing to 47 / 46 / 47 / 47 after strip + lowercase + `-` to `_` |
| Names not in modules.csv after normalizing | defects only | 5 names |
| Unmatched defect rows | defects | 18 rows, 53 defects (payments_crypto 6, ui_widgets_old 4, auth_sso_beta 3, tmp_migration 3, reporting_v0 2) |
| Complexity | metrics | mean 23.5, median 15.1, max 299.9; IQR upper fence 33.1; 9 rows above it |

Notes from the audit:
- Of the 9 rows above the fence, 7 are the genuine extremes (about 200 to 300), 1 is an exact duplicate copy of one of them (payments_gateway v1.0), and 1 is borderline (reporting_scheduler v3.0 at 33.4, which is a real value and should be kept).
- Only 41 of the 47 modules appear in defects.csv after cleaning (46 names minus 5 unmatched). The other 6 modules seem to have no defect rows in any release, so they should get 0 defects at merge time. To verify in Phase 3.
- Not yet checked: duplicate module-release keys after name cleanup (Cell 6). Expected 0 after exact duplicates are dropped; confirm in Phase 2.

---

## 3b. Phase 2 cleaning results (real numbers from my notebook, 12 Oct 2026)

| Step | Before | After |
|---|---|---|
| Module names standardized (strip, lowercase, `-` to `_`) | 102 / 96 / 106 raw names in metrics / commits / releases | 47 / 47 / 47 |
| Exact duplicates removed | metrics 249, releases 247 | 235, 235 |
| Duplicate module-release keys | checked | 0 in metrics, commits, releases |
| Unmatched defects | 216 defect rows | 18 rows (53 defects) set aside in `defects_orphans.csv`; 198 rows kept |
| Extreme complexity | 7 values above 100 | flagged in `complexity_outlier`, raw kept in `complexity_raw`, set to missing and imputed |
| Missing metric values | 58 cells in metrics, 7 in commits | filled with the module's median (global median as safety net); 0 missing remaining |

Cleaned files saved in `data/clean/`: metrics_clean.csv, defects_clean.csv, defects_orphans.csv, commits_clean.csv, releases_clean.csv.

---

## 3c. Phase 3 merge and feature engineering results (real numbers from my notebook, 12 Oct 2026)

| Check | Result |
|---|---|
| Defects aggregated to module-release level | 120 module-release combinations have defects; total 285 defects, equal to the cleaned defects file |
| Merged table | 235 rows (47 modules x 5 releases), 20 columns before feature engineering |
| Modules with zero defects in every release | 6 (they get 0 defects at merge) |
| `high_defect` target | threshold = 75th percentile = 2 defects; high_defect = more than 2 in a release: 36 rows (15.3%) vs 199 rows; classes are imbalanced |
| Encoding | one-hot: comp_API, comp_Auth, comp_Database, comp_Payments, comp_Reporting, comp_UI, lang_C++, lang_Java, lang_JavaScript, lang_Python (text columns `component` and `language` kept for EDA and Excel) |
| Final dataset | `ch28_clean_module_release.csv`: 235 rows x 42 columns; `ch28_module_summary.csv`: 47 rows (both in `data/clean/`) |
| Missing cells in final dataset | 14, confirmed: all in `complexity_raw`, which keeps the originally missing complexity values on purpose. To be dropped at the start of Phase 5 (the `complexity_outlier` flag stays as evidence of the outlier treatment). |

First look at the module summary (top 10 by total defects): api_gateway 29 (15 of them in a single release, defects in all 5 releases), ui_notifications 25, ui_themes 19, auth_session 17, payments_fraud 15, reporting_audit_logs 14, reporting_scheduler 13, database_migration 12, payments_invoice 12, database_replication 10. Six of these ten had defects in all 5 releases. These are first impressions only; the formal analysis is Phase 4.

---

## 3d. Phase 4a EDA results, Q1 to Q3 (real numbers from my notebook, 12 Oct 2026)

Charts saved in `outputs/`: q1_top10_modules, q1_defect_distribution, corr_metrics_vs_defects, q2_complexity, q3_churn.

**Q1 Which modules have more defects?**
- Defects by component (total, mean per module-release): UI 70 / 1.75, Payments 55 / 1.38, API 50 / 1.25, Reporting 43 / 1.08, Database 36 / 1.03, Auth 31 / 0.78 (total 285).
- The top 10 modules (about 21% of the 47) account for 58.2% of all defects.

**Correlation of each metric with total defects (module-release level, 235 rows)**

| Metric | Pearson | Spearman |
|---|---|---|
| churn | 0.65 | 0.41 |
| changed_lines | 0.65 | 0.41 |
| commit_count | 0.61 | 0.36 |
| contributors | 0.51 | 0.38 |
| complexity | 0.35 | 0.40 |
| coupling | 0.34 | 0.40 |
| test_coverage | -0.39 | -0.39 |
| size | 0.24 | 0.11 |

Reading: Pearson is clearly higher than Spearman for churn, commit_count and contributors, meaning those relationships are driven by the high-defect upper tail (a few rows with many defects). Test coverage has the same value in both, a steady negative relationship. Size alone is weak. churn and changed_lines have identical correlations (near-duplicates); complexity and coupling likely move together. Handle both in feature selection (Phase 5). Most rows have 0 to 2 defects (median 0 in most quartiles), so the target is zero-heavy; expect modest R2 in Phase 5.

**Q2 Complexity (mean defects by quartile, rows per quartile 59/59/58/59):** Q1 0.76, Q2 0.53, Q3 1.29, Q4 2.27. Defects stay low in the bottom half and rise only in the top half; the highest quartile averages about 3 times the lowest.

**Q3 Churn (mean defects by quartile):** Q1 0.47, Q2 0.78, Q3 0.86, Q4 2.73 (median 0 for the first three quartiles, 2 for the top). The highest-churn quartile averages about 5.8 times the lowest, so defects concentrate where churn is highest.

Draft EDA findings for the sheet (confirm after 4b): (1) defects are concentrated, top 10 of 47 modules hold 58.2% of defects, and UI has the highest average per module-release (1.75) while Auth has the lowest (0.78); (2) churn shows the strongest link (Pearson 0.65, top-churn quartile averages 2.73 defects vs 0.47 in the lowest) and test coverage is negatively related (-0.39). These are patterns in synthetic data and are associations, not proof of cause.

---

## 3e. Phase 4b EDA results, Q4 to Q6 (real numbers from my notebook, 12 Oct 2026)

Charts saved in `outputs/`: q4_coverage, q5_component_release_heatmap, q5_component_trend, q6_contributors, correlation_heatmap.

**Q4 Test coverage**
- Mean defects by coverage band (rows): up to 40% 3.68 (22), 40-60% 1.47 (68), 60-80% 0.73 (124), above 80% 0.62 (21). Defects fall steeply as coverage rises and flatten above about 60%.
- Average coverage by component: UI 55.6 (lowest), Payments 61.1, API 63.8, Reporting 66.5, Auth 66.7, Database 66.9. UI has both the lowest coverage and the most defects.
- Top-10 defect modules average 49.2% coverage vs 67.2% for the other modules.

**Q5 Repeated defects by component** (total defects per release v1.0, v1.1, v2.0, v2.1, v3.0)
- API 17, 3, 12, 3, 15 (swings, high again in v3.0)
- Auth 10, 4, 6, 9, 2 (lowest overall, low in v3.0)
- Database 8, 8, 6, 7, 7 (flat: a steady stream of defects every release)
- Payments 19, 11, 11, 3, 11
- Reporting 7, 11, 5, 8, 12 (rising, highest in v3.0)
- UI 27, 16, 10, 7, 10 (falling from a high start, still highest total)
- All components per release: v1.0 88, v1.1 53, v2.0 50, v2.1 37, v3.0 57 (down to v2.1, then back up 54% in v3.0).
- Modules by number of releases with defects (0 to 5): 6, 6, 13, 6, 10, 6. The flag "defects in 2+ releases" covers 35 of 47 modules, too broad to be useful, so repeat-defect modules are now defined as **defects in 4 or more of the 5 releases: 16 modules**.
- Repeat-defect modules by component (of 8 modules each, Database has 7): UI 4, Database 3, Payments 3, Reporting 3, API 2, Auth 1.

**Q6 Contributors:** mean defects by contributor group (rows): 1-2 0.49 (79), 3-4 1.05 (108), 5-6 2.22 (41), 7+ 6.00 (7, too few rows to trust). Defects rise with contributors (correlation 0.51), but contributors move closely with commit_count (0.88) and churn (0.79), so this is mostly activity volume; Phase 5 tests whether contributors adds anything beyond churn.

**Correlation matrix notes:** activity cluster churn / changed_lines 0.93, churn / commit_count 0.89, contributors / commit_count 0.88, contributors / churn 0.79; complexity / coupling 0.82; test_coverage is mildly negative with everything (-0.12 to -0.32) and -0.39 with defects.

**Summary statistics (after cleaning):** complexity mean 15.1 (max 33.4), coupling mean 10.7, churn mean 322.5 (max 1249.4, a long tail left as is), coverage mean 63.4 (range 24.9 to 98), contributors mean 3.3 (1 to 9), total_defects mean 1.21 (max 15).

**Final EDA findings for the sheet (choose two):**
1. Defects are concentrated: the top 10 of 47 modules hold 58.2% of all 285 defects, and they average 49.2% test coverage vs 67.2% for the rest.
2. Churn and coverage separate quality best: the highest-churn quartile averages 2.73 defects per release vs 0.47 in the lowest, and modules with coverage up to 40% average 3.68 vs 0.62 above 80%.
3. UI has the most defects (70) and the lowest coverage; Auth the fewest (31).

**Draft business insights for the pitch:** (a) concentrate review effort on the 16 repeat-defect modules and the top-10 list; (b) raise coverage on modules below about 60%, where defects rise sharply; (c) put extra review on high-churn modules; (d) watch Reporting (rising to its highest in v3.0) and API (spiky, high again in v3.0); (e) Database is a chronic steady source, a candidate for a systematic quality fix. Associations in synthetic data, not proof of cause.

---

## 3f. Phase 5a feature selection results (real numbers from my notebook, 12 Oct 2026)

Housekeeping done: `repeat_defect_flag` now means defects in 4+ of 5 releases (16 modules); `complexity_raw` dropped; final dataset is 235 rows x 41 columns with 0 missing cells (saved to `data/clean/`); `module_summary` gained `repeat_defect_module`.

**Correlation filter (drop one of any pair above 0.85):** churn vs changed_lines 0.93 (dropped churn, the filter's tie-break) and changed_lines vs commit_count 0.89 (dropped commit_count). Kept numeric: complexity, coupling, changed_lines, contributors, test_coverage, size, churn_per_commit, lines_per_contributor, commits_per_contributor, release_index; plus 10 one-hot columns = 20 candidate features. Complexity and coupling (0.82) were both kept.

**Random Forest importance (80/20 split, random_state=42; permutation importance on only 47 test rows, so small values are noise):**

| Feature | RF importance | Permutation importance |
|---|---|---|
| changed_lines | 0.479 | 0.507 |
| coupling | 0.096 | 0.037 |
| test_coverage | 0.090 | 0.036 |
| commits_per_contributor | 0.070 | 0.000 |
| release_index | 0.056 | 0.009 |
| complexity | 0.052 | 0.050 |
| contributors | 0.051 | -0.017 |
| size | 0.037 | -0.010 |
| lines_per_contributor, churn_per_commit | 0.029, 0.024 | 0.003, -0.006 |
| all component and language dummies | 0.000 to 0.005 | about 0 |

Reading: code change volume dominates by a wide margin; coupling, test coverage and complexity come next. Contributors adds nothing once change volume is in the model (permutation importance slightly negative), which answers Q6: the contributor-count link is explained by activity volume. Component and language add almost nothing.

**Decisions:** (1) use `churn` as the change-volume measure in the final model, not `changed_lines`: they correlate at 0.93, carry the same information, and churn is the metric named in the business question and used in the EDA and Excel work; (2) compare two feature sets in 5b: **core 4** = churn, complexity, coupling, test_coverage, and **extended** = core 4 + contributors, size, release_index + the 10 component and language dummies; (3) Linear Regression baseline vs Random Forest, plus a mean-predictor baseline for context.

---

## 3g. Phase 5b regression results (real numbers from my notebook, 12 Oct 2026)

Target: `total_defects` per module-release. Feature sets: **core 4** = churn, complexity, coupling, test_coverage; **extended** (17) = core 4 + contributors, size, release_index + component and language dummies. Random Forest: 300 trees, min_samples_leaf 3, random_state 42.

**Single 80/20 split (47 test rows):**

| Model | RMSE | MAE | R2 |
|---|---|---|---|
| Linear Regression, core 4 | 1.258 | 0.922 | 0.492 |
| Random Forest, core 4 | 1.340 | 0.874 | 0.424 |
| Random Forest, extended | 1.371 | 0.905 | 0.396 |
| Linear Regression, extended | 1.372 | 1.024 | 0.396 |
| Baseline: predict the mean | 1.810 | 1.308 | -0.051 |

**Group cross-validation by module, 5 folds (predicting modules the model never saw):**

| Model | CV RMSE | CV R2 |
|---|---|---|
| Random Forest, extended | 1.291 | 0.362 |
| Random Forest, core 4 | 1.305 | 0.351 |
| Linear Regression, core 4 | 1.382 | 0.320 |
| Linear Regression, extended | 1.458 | 0.248 |

Chart `actual_vs_predicted` (saved in `outputs/`): most rows have 0 to 2 actual defects and are predicted between about 0.3 and 1.5; the two largest cases are misjudged (actual 4 predicted about 7.7, actual 10 predicted about 4.3, actual 5 predicted about 1.7). The model gets direction and rough size right but squeezes the extremes, so it is better for ranking modules by risk than for predicting exact counts.

Reading: every model clearly beats the mean baseline (RMSE about 1.26 to 1.37 vs 1.81). Linear Regression on core 4 won the single 47-row split, but that split is small and noisy; the module-level cross-validation, which uses all 235 rows and unseen modules, favours Random Forest. The extended set gives no real gain over core 4 (CV RMSE 1.291 vs 1.305; worse on the single split), so the extras (contributors, size, release, component, language) add nothing.

**Final model decision:** Random Forest Regressor on the core 4 features (simpler than extended with the same accuracy; captures the non-linear threshold effects seen in the EDA, such as defects rising only in the top churn and complexity quartiles).

**Draft answers for the sheet, Round 2** (use these real values):
1. Selected features: churn, complexity, coupling, test_coverage. Target: total_defects (defects per module per release).
2. Algorithm: Random Forest Regressor (300 trees, min_samples_leaf 3, random_state 42).
3. Justification: handles non-linear relationships and threshold effects, robust to skewed data, needs no scaling, gives feature importance that answers which metrics matter; beat the mean baseline and was the better choice on module-level cross-validation.
4. Performance: test split RMSE 1.340, MAE 0.874, R2 0.424; module-level cross-validation RMSE 1.305, R2 0.351; baseline (predict the mean) RMSE 1.810. Linear Regression on the same features: test RMSE 1.258, R2 0.492; cross-validation RMSE 1.382, R2 0.320.

---

## 3h. Phase 5c classifier and risk ranking results (real numbers from my notebook, 12 Oct 2026)

**Classifier for `high_defect` (more than 2 defects in a release; 36 of 235 rows)**: Random Forest Classifier, core 4 features, class_weight balanced, predictions from group cross-validation by module (5 folds), so every module was scored by a model that never saw it.

| Threshold | Precision | Recall | F1 |
|---|---|---|---|
| 0.3 | 0.403 | 0.750 | 0.524 |
| 0.4 | 0.413 | 0.528 | 0.463 |
| 0.5 | 0.515 | 0.472 | 0.493 |

ROC-AUC 0.797. Confusion matrix at 0.4: 172 true negatives, 27 false positives, 17 false negatives, 19 true positives. Reading: at threshold 0.3 the model catches 75% of high-defect rows (27 of 36) but flags about 67 rows, so about 40 are false alarms; for review and testing prioritization, where missing a bad module costs more than an extra review, recall matters more, so 0.3 is the working threshold (only three thresholds were compared). F1 is not smooth across thresholds because there are only 36 positive rows. Accuracy is not reported because predicting "never high" is already about 85% accurate.

**Risk ranking (prototype / intelligence layer):** Random Forest Regressor predictions for every module-release from unseen-module cross-validation; Spearman rank agreement between predicted and actual defects over all 235 rows = **0.556**. Modules ranked for the latest release (v3.0), with a rule-based action: churn above the 75th percentile (397.35) counts as high churn, coverage below 60% as low coverage; action = Code review + more tests (both), Priority code review (high churn only), Add tests (low coverage only), else Monitor. Action counts over 47 modules: Monitor 24, Add tests 9, Code review + more tests 8, Priority code review 6.

Top 10 by predicted defects in v3.0 (predicted / actual in v3.0 / releases with defects / churn / complexity / coverage % / action):
1. api_docs: 8.55 / 4 / 1 / 1161.8 / 10.3 / 87.4 / Priority code review
2. payments_wallet: 4.54 / 1 / 3 / 563.7 / 25.5 / 36.9 / Code review + more tests
3. payments_fraud: 3.19 / 1 / 4 / 454.2 / 20.1 / 30.7 / Code review + more tests
4. ui_themes: 3.00 / 5 / 4 / 529.0 / 33.0 / 57.6 / Code review + more tests
5. payments_gateway: 2.11 / 1 / 4 / 326.7 / 22.8 / 65.4 / Monitor
6. reporting_audit_logs: 2.00 / 5 / 5 / 773.4 / 24.9 / 62.4 / Priority code review
7. reporting_scheduler: 1.76 / 4 / 5 / 262.5 / 33.4 / 41.1 / Add tests
8. api_gateway: 1.75 / 5 / 5 / 455.5 / 17.0 / 41.1 / Code review + more tests
9. api_versioning: 1.75 / 1 / 3 / 594.2 / 15.1 / 59.5 / Code review + more tests
10. api_webhooks: 1.62 / 0 / 4 / 100.2 / 13.7 / 29.5 / Add tests

Observations: (a) api_docs is a churn-spike case: churn 1161.8 (near the maximum) in a module with good coverage (87.4%) and low complexity, defects in only one release (this one); the model overpredicts (8.55 vs 4) but the direction is right, and the right action is code review, not more tests. (b) The model underpredicts some chronic modules (reporting_audit_logs 2.0 vs 5, api_gateway 1.75 vs 5, ui_themes 3.0 vs 5, reporting_scheduler 1.76 vs 4) and overpredicts others (payments_wallet 4.54 vs 1, payments_fraud 3.19 vs 1): four metrics do not capture everything, and defect history is an extra signal. Hence the final list combines the model score with repeat-defect history.

**Tier rule for the final priority list** (simple and explainable, matches the pitch focus on repeated quality concerns): Tier 1 = repeat-defect module (defects in 4+ of 5 releases) AND action is not Monitor; Tier 2 = action is not Monitor, or predicted defects of 2 or more; Tier 3 = everything else (monitor). Saved by the tier cell as `data/clean/ch28_module_priority_tiers.csv` (all 47 modules). Tier counts and the Tier 1 list: to be filled in from the notebook output.

**Draft answers for the sheet, Round 3** (finalize after Excel and the tier output):
1. Visualizations: top-10 modules by defects, defect distribution, correlation heatmap, complexity and churn scatter plots with quartile bars, coverage-band chart, component-by-release heatmap and trend lines, contributors chart, feature importance, actual vs predicted, risk-ranking chart; plus the Excel charts and pivot charts.
2. Key insights: (a) churn is the strongest driver: the highest-churn quartile averages 2.73 defects per release vs 0.47 in the lowest (5.8 times), and rows with coverage up to 40% average 3.68 defects vs 0.62 above 80%; (b) 16 of 47 modules had defects in 4 or more of 5 releases (UI 4, Database 3, Payments 3, Reporting 3, API 2, Auth 1), and the classifier flags high-defect rows with ROC-AUC 0.797 and recall 0.75 at threshold 0.3.
3. Prototype: a module risk-ranking tool. A Random Forest predicts expected defects from churn, complexity, coupling and test coverage (scored on unseen modules); simple rules turn churn and coverage into actions, and combined with repeat-defect history they produce a three-tier code-review and testing priority list (CSV and Excel).
4. Recommendations: (a) put Tier 1 modules under mandatory code review and raise their test coverage to at least 60% first; (b) add a review trigger for churn spikes (top-quartile churn, above about 400 changed lines per release), as the api_docs case shows a clean module can jump in risk quickly.
Caveats to keep: data is synthetic; associations not causes; regression R2 is moderate (0.35 to 0.42).

---

## 4. Environment and folder structure

Working in **Google Colab + Google Drive**, with the final work pushed to **GitHub**.

```
MyDrive/DS_Sprint_CH28/
├── data/
│   ├── raw/        <- the 5 original CSVs (never edit these)
│   └── clean/      <- cleaned outputs
├── notebooks/      <- CH28_EDA_FeatureEngineering.ipynb
├── excel/          <- CH28_Excel_Analysis.xlsx
├── slides/         <- CH28_Business_Pitch.pptx
├── outputs/        <- saved charts (png), model results
├── README.md
└── PROJECT_PLAN.md
```

Colab start-of-notebook cell:

```python
from google.colab import drive
drive.mount('/content/drive')
BASE = '/content/drive/MyDrive/DS_Sprint_CH28'
RAW, CLEAN, OUT = f'{BASE}/data/raw', f'{BASE}/data/clean', f'{BASE}/outputs'
```

Pushing to GitHub: easiest is to download the folder from Drive and upload via the GitHub web UI, or use `git` from Colab with a personal access token (never paste the token into the notebook or commit it).

---

## 5. Phase plan (do one phase at a time, finish and record before moving on)

### Phase 0 – Setup
- [ ] Unzip the dataset, create the Drive folder structure above, upload the 5 CSVs to `data/raw/`
- [ ] Create a new Colab notebook in `notebooks/`, mount Drive, confirm files load
- [ ] Create an empty GitHub repo (suggested name: `ds-sprint-ch28-software-quality`)
- [ ] Optional: message the professor to confirm a synthetic dataset is acceptable (record the answer in the Decision Log)

### Phase 1 – Load and audit
- [x] Load all 5 files, check shape, dtypes, `head()`, `describe()`
- [x] Count missing values, exact duplicates, duplicate module-release keys
- [x] List unique module names per file and compare against `modules.csv`
- [x] Inspect complexity distribution (boxplot, max values)
- [x] Find defect rows that do not match any module
- [ ] **Output:** an audit table (problem, file, count). This is the "before" evidence for the sheet.

### Phase 2 – Clean
- [x] Standardize module names (proposed rule: strip spaces, lowercase, replace `-` with `_`), then verify all names match `modules.csv` (except true orphans)
- [x] Drop exact duplicates, then enforce one row per module-release
- [x] Handle missing values (proposed: median per module, fall back to median per component)
- [x] Handle extreme complexity (proposed, updated after the audit: keep the raw value in `complexity_raw`, flag values above 100 with `complexity_outlier`, set them to missing, then impute with the module's median complexity computed without the extremes. Reason: capping at the IQR fence of 33.1 would still give those modules an unrealistically high value.)
- [x] Unmatched defects: set aside in a separate "orphan defects" table and exclude from the model, record the count
- [x] **Output:** cleaned versions of each file and an "after" audit table

### Phase 3 – Merge and feature engineering
- [x] Aggregate defects to module-release level (total defects, plus counts by severity)
- [x] Merge modules + metrics + defects + commits + releases into one table, 235 rows. Modules with no defect record get 0 defects.
- [x] Create new features (proposed list):
  - `defect_density` = defects per 1,000 lines of code
  - `churn_per_commit`, `lines_per_contributor`, `commits_per_contributor`
  - `high_severity_defects` (High + Critical) and `high_severity_ratio`
  - `defect_count_prev_release` and `repeat_defect_flag` (defects in 2 or more releases)
  - `module_age` or release index (1 to 5)
  - `risk_score` (a simple combination of complexity, churn and low coverage)
  - `high_defect` binary target (for example above the 75th percentile)
- [x] Encode categorical variables: one-hot for `component` and `language`. Severity is already aggregated into counts per level, so instead of ordinal encoding we add a `weighted_severity` score (Low x1, Medium x2, High x3, Critical x4).
- [x] Leakage rule: every defect-derived column (total_defects, severity counts, defect_density, high_severity_*, weighted_severity, repeat_defect_flag, high_defect) is for EDA and the pitch only, never an ML input. `risk_score` is built only from complexity, churn and coverage, so it is safe. `defects_prev_release` is a past value; decide in Phase 5 whether to use it.
- [x] **Output:** `ch28_clean_module_release.csv` (save to `data/clean/`) and a module-level summary table (one row per module)

### Phase 4 – EDA (answers the 6 required questions, each with a chart)
- [x] Q1 Which modules have more defects? (top-10 bar chart, defect distribution)
- [x] Q2 How does complexity relate to defects? (scatter with trend line, correlation)
- [x] Q3 Does code churn relate to quality? (scatter, churn bins vs average defects)
- [x] Q4 How does test coverage differ? (coverage bands vs defects, boxplot by component)
- [x] Q5 Which components show repeated defects? (component x release heatmap)
- [x] Q6 Does contributor count relate to defect frequency? (box or bar by contributor bins)
- [x] Correlation heatmap and summary statistics
- [x] Write 2 key observations for the sheet from real results
- [x] **Output:** saved charts in `outputs/`

### Phase 5 – Feature selection and ML model
- [x] Choose target: `defect_count` (regression). Optional second model: `high_defect` (classification)
- [x] Feature selection: correlation filter plus Random Forest feature importance; consider PCA only if it adds value
- [x] Split train/test (80/20, `random_state=42`); avoid leakage (do not use defect-derived columns as inputs)
- [x] Because the same module appears in several rows, also check performance with group cross-validation by module (GroupKFold, 5 folds), so the score reflects predicting unseen modules
- [x] Baseline (Linear Regression) vs **Random Forest Regressor** (proposed main algorithm)
- [x] Record the **actual** metrics: RMSE, MAE, R² (and accuracy/F1 if classification is added)
- [x] **Output:** selected features, algorithm, justification, actual metric values, importance chart

### Phase 6 – Excel workbook (Round 3, 30 marks)
- [ ] Import cleaned data, format it as a Table, freeze header, number formats
- [ ] Formulas and statistics: AVERAGE, MEDIAN, STDEV, CORREL, COUNTIF(S), SUMIF(S), RSQ, SLOPE
- [ ] Required analyses, each with a chart: defects by module, complexity relationship, code-churn analysis, coverage comparison, component trend, contributor analysis
- [ ] Pivot Tables and Pivot Charts for the above
- [ ] **One Summary sheet** with the important results
- [ ] **Note:** pivot tables and pivot charts must be built in desktop Excel (or Google Sheets equivalents) by me; Claude can prepare the data sheet, formulas and chart structure, and give click-by-click pivot steps.

### Phase 7 – Presentation (Round 4, 20 marks)
- [ ] 6 to 8 slides: Problem, Data and cleaning, Key findings (with evidence), Patterns and business meaning, Areas needing attention (repeat-defect modules), Recommendations (review and testing priorities), Conclusion
- [ ] Every finding supported by a chart or number from my own analysis
- [ ] Pitch focus: which modules get code review first, which need more tests, with the data to justify it

### Phase 8 – GitHub, sheet and final check
- [ ] Repo contents: notebook, raw and cleaned data, Excel file, slides, generator script, README (state clearly that the data is synthetic), this plan
- [ ] Re-run the notebook top to bottom to confirm it works
- [ ] Fill in the mandatory summary sheet (Section 10) using real results
- [ ] Submit the GitHub link as instructed

### Phase Q – Round 1 quiz (20 marks)
- [ ] Revise: Pandas (merge, groupby, missing values), NumPy basics, Matplotlib/Seaborn chart types, EDA and feature engineering concepts, Excel functions and pivots
- [ ] Optional: ask Claude for a practice MCQ set

---

## 6. Analytical questions to answer (from the PDF)

1. Which modules have more defects?
2. How does complexity relate to defects?
3. Does code churn relate to quality?
4. How does test coverage differ?
5. Which components show repeated defects?
6. Does contributor count relate to defect frequency?

## 7. Minimum Excel analysis (from the PDF)

Defects by module, complexity relationship, code-churn analysis, coverage comparison, component trend, contributor analysis, and one summary sheet.

## 8. ML plan (to satisfy the professor's Round 2 sheet)

- **Target:** `defect_count` per module-release (optionally `high_defect`).
- **Candidate inputs:** complexity, coupling, churn, test_coverage, size, commit_count, contributors, changed_lines, engineered ratios, encoded component and language.
- **Algorithm (proposed):** Random Forest Regressor, with Linear Regression as a baseline.
- **Why suitable:** handles non-linear relationships and interactions, robust to outliers and mixed feature scales, gives feature importance that directly answers "which metrics matter".
- **Metrics:** RMSE, MAE, R². Record the real numbers only.

## 9. Pitch outline (draft, finalize with real results)

Open with the business question, show 2 or 3 strongest metric-defect relationships, name the repeat-defect modules and components, then recommend: (1) code-review priority list, (2) testing priority list with target coverage, (3) a simple monitoring rule using the risk score.

---

## 10. Summary sheet template (Mail 2) – fill ONLY with real results

**Student details:** Niket Kumar | 722824104158 | Class: ____ | CH28 – Software Quality Insight

**Round 1 – Data Understanding, Preparation and EDA**
1. Problem statement (2 to 3 lines): ____
2. Dataset: synthetic, generated using Python (seed 42); 5 files; records: 47 modules, 235 module-release rows after cleaning (raw file sizes in Section 3); attributes: ____
3. Preprocessing: missing values ____, duplicates removed ____, outliers ____
4. Two EDA findings: ____

**Round 2 – Feature Engineering and Machine Learning**
1. Selected features / target: ____
2. Algorithm: ____
3. Justification: ____
4. Performance (actual values): ____

**Round 3 – Intelligence Layer, Visualization and Prototype**
1. Visualizations: ____
2. Two key insights: ____
3. Prototype / intelligence layer (for example the risk-score ranking of modules): ____
4. Two recommendations: ____

**Final:** GitHub link: ____ | Conclusion (2 to 3 lines): ____

---

## 11. Rules for working together

- One phase at a time. Each phase ends with working code, a short result summary, and a Status Tracker update.
- Real results only. Never invent numbers; run the code and copy actual outputs.
- Keep code beginner-readable with comments, in small Colab cells.
- Prefer Excel-compatible functions so formulas work in both Excel and Google Sheets.
- Be open that the dataset is synthetic.

## 12. Decision Log (append new decisions with dates)

| Date | Decision |
|---|---|
| 12 Oct 2026 | Challenge CH28 allocated; do not exchange |
| 12 Oct 2026 | No dataset provided, so using a synthetic dataset following the PDF schema |
| 12 Oct 2026 | Synthetic data generated with seed 42 (5 CSVs plus generator script) |
| 12 Oct 2026 | Workflow: Google Drive + Google Colab, phased and incremental, then GitHub |
| 12 Oct 2026 | This plan is the single source of truth |
| 12 Oct 2026 | Phase 0 (setup, files load with expected shapes) and Phase 1 (audit) completed |
| 12 Oct 2026 | Outlier method changed from IQR capping to: flag values above 100, set to missing, impute with module median (see Phase 2) |
| 12 Oct 2026 | Phase 2 (clean) completed; all outputs matched expectations. Rules used: name normalization, drop exact duplicates, orphan defects set aside, extremes (above 100) set to missing, missing values filled with module median |
| 12 Oct 2026 | Severity handled as per-level counts plus a weighted severity score; defect-derived columns are never ML inputs (leakage rule) |
| 12 Oct 2026 | Phase 3 completed (merge, features, encoding, files saved); 14 missing cells in the final dataset pending a check |
| 12 Oct 2026 | Phase 4a (Q1 to Q3) completed; findings recorded in Section 3d |
| 12 Oct 2026 | Phase 4b (Q4 to Q6) completed; Phase 4 done. Findings in Sections 3d and 3e |
| 12 Oct 2026 | Phase 5a completed. Activity cluster resolved by keeping churn only (0.93 with changed_lines); complexity and coupling both kept (0.82); PCA not used (few features, interpretability matters) |
| 12 Oct 2026 | Two feature sets to compare in 5b: core 4 (churn, complexity, coupling, test_coverage) and extended (core 4 + contributors, size, release_index + dummies) |
| 12 Oct 2026 | Repeat-defect modules redefined as defects in 4 or more of 5 releases (16 modules), because the 2+ releases flag covered 35 of 47 modules. `complexity_raw` dropped from the final dataset |
| 12 Oct 2026 | Phase 5b completed. Final model: Random Forest Regressor on core 4 features (churn, complexity, coupling, test_coverage); chosen on group cross-validation, extended set gave no gain |
| 12 Oct 2026 | Phase 5c completed: classifier ROC-AUC 0.797 (F1 0.524, recall 0.75 at threshold 0.3), risk-ranking Spearman 0.556; action rules (churn above 397.35, coverage below 60) and tier rule defined (Section 3h) |
| 12 Oct 2026 | Phase 6 approach: I upload the final CSVs (ch28_clean_module_release, ch28_module_summary, ch28_module_priority_tiers); Claude builds the Excel workbook with formulas, charts and summary sheet; I add the Pivot Tables and Pivot Charts myself in desktop Excel using step-by-step instructions |
| 12 Oct 2026 | Tier counts: Tier 1 = 11 (payments_fraud, ui_themes, reporting_audit_logs, reporting_scheduler, api_gateway, api_webhooks, reporting_export, ui_notifications, auth_session, ui_charts, database_migration), Tier 2 = 13, Tier 3 = 23 |
| 12 Oct 2026 | Phase 6 done. Pivot 2 uses rows = release, columns = component (so the pivot chart shows trend lines). Pivots live on one sheet, `Pivots` |
| 12 Oct 2026 | Phase 7 done: 8-slide deck |
| (open) | Professor's reply on whether synthetic data is acceptable |
