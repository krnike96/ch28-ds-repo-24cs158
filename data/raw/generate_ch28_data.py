"""
CH28 - Software Quality Insight | Synthetic dataset generator
Creates 5 CSV files (modules, metrics, defects, commits, releases) with
deliberately injected data-quality issues. Seeded for reproducibility.
"""
import numpy as np, pandas as pd, os

SEED = 42
rng = np.random.default_rng(SEED)
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- 1. modules ----------
components = {
    "Auth":      ["login", "session", "oauth", "password", "token", "mfa", "rbac", "audit"],
    "Payments":  ["checkout", "invoice", "refund", "gateway", "wallet", "tax", "subscription", "fraud"],
    "UI":        ["dashboard", "forms", "navbar", "charts", "themes", "search", "notifications", "profile"],
    "Database":  ["orm", "migration", "cache", "backup", "indexing", "pool", "replication"],
    "API":       ["router", "gateway", "ratelimit", "validator", "webhooks", "graphql", "docs", "versioning"],
    "Reporting": ["export", "scheduler", "analytics", "pdfgen", "emailer", "aggregator", "templates", "audit_logs"],
}
comp_lang = {"Auth": ["Java", "Python"], "Payments": ["Java", "C++"], "UI": ["JavaScript"],
             "Database": ["C++", "Python"], "API": ["Python", "JavaScript", "Java"],
             "Reporting": ["Python", "Java"]}
rows = []
for comp, mods in components.items():
    for m in mods:
        lang = rng.choice(comp_lang[comp])
        size = int(np.clip(rng.lognormal(7.6, 0.6), 600, 20000))   # lines of code
        rows.append((f"{comp.lower()}_{m}", comp, lang, size))
modules = pd.DataFrame(rows, columns=["module", "component", "language", "size"])
modules.insert(0, "module_id", [f"M{str(i+1).zfill(3)}" for i in range(len(modules))])
N = len(modules)

# a handful of "problem modules" with persistently worse quality
problem = rng.choice(modules.module, size=8, replace=False)

# ---------- 2. releases ----------
versions = ["v1.0", "v1.1", "v2.0", "v2.1", "v3.0"]
dates = pd.to_datetime(["2024-01-15", "2024-05-20", "2024-09-10", "2025-02-18", "2025-07-01"])

# ---------- 3. latent module-release truth ----------
recs = []
for _, r in modules.iterrows():
    base_cx = rng.normal(14, 5) + (8 if r.module in problem else 0)
    base_cov = rng.normal(68, 12) - (18 if r.module in problem else 0)
    for v, d in zip(versions, dates):
        complexity = max(2, base_cx + rng.normal(0, 3))
        coupling = max(1, 0.45 * complexity + rng.normal(4, 2))
        churn = max(5, rng.gamma(2.5, 120) * (1 + (0.8 if r.module in problem else 0)))
        coverage = float(np.clip(base_cov + rng.normal(0, 6), 10, 98))
        commits = max(1, int(churn / rng.uniform(18, 40)))
        contributors = int(np.clip(round(commits ** 0.5 * rng.uniform(0.7, 1.4)), 1, 15))
        changed_lines = int(churn * rng.uniform(1.1, 1.8))
        lam = np.exp(-1.2 + 0.045 * complexity + 0.0016 * churn - 0.017 * coverage
                     + 0.05 * contributors + 0.00005 * r["size"] + 0.4 * (r.module in problem)) * 1.6
        defects = int(rng.poisson(min(lam, 25)))
        recs.append(dict(module=r.module, version=v, release_date=d, complexity=round(complexity, 2),
                         coupling=round(coupling, 2), churn=round(churn, 1), test_coverage=round(coverage, 1),
                         commit_count=commits, contributors=contributors, changed_lines=changed_lines,
                         total_defects=defects))
truth = pd.DataFrame(recs)

# ---------- helpers for messy module names ----------
def mess(name):
    p = rng.random()
    if p < 0.10: return name.upper()
    if p < 0.17: return name.title()
    if p < 0.24: return " " + name + " "
    if p < 0.28: return name.replace("_", "-")
    return name

# ---------- metrics.csv ----------
metrics = truth[["module", "version", "complexity", "coupling", "churn", "test_coverage"]].copy()
for col in ["complexity", "coupling", "churn", "test_coverage"]:           # missing values ~6%
    idx = rng.choice(metrics.index, size=int(0.06 * len(metrics)), replace=False)
    metrics.loc[idx, col] = np.nan
ext = rng.choice(metrics.index, size=7, replace=False)                      # extreme complexity
metrics.loc[ext, "complexity"] = rng.uniform(150, 320, size=7).round(2)
metrics["module"] = metrics["module"].map(mess)                             # inconsistent names
metrics = pd.concat([metrics, metrics.sample(14, random_state=SEED)], ignore_index=True)  # duplicates
metrics = metrics.sample(frac=1, random_state=SEED).reset_index(drop=True)
metrics = metrics.rename(columns={"version": "release"})

# ---------- defects.csv (one row per module-release-severity) ----------
sev_levels = ["Low", "Medium", "High", "Critical"]
drows = []
for _, r in truth.iterrows():
    if r.total_defects == 0: continue
    split = rng.multinomial(r.total_defects, [0.40, 0.33, 0.20, 0.07])
    for s, c in zip(sev_levels, split):
        if c > 0: drows.append((r.module, r.version, int(c), s))
defects = pd.DataFrame(drows, columns=["module", "release", "defect_count", "severity"])
defects["module"] = defects["module"].map(mess)
orphan = pd.DataFrame({"module": rng.choice(["legacy_billing", "payments_crypto", "ui_widgets_old", "tmp_migration",
                                             "auth_sso_beta", "reporting_v0"], 18),
                       "release": rng.choice(versions, 18), "defect_count": rng.integers(1, 6, 18),
                       "severity": rng.choice(sev_levels, 18)})           # unmatched defect records
defects = pd.concat([defects, orphan], ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)
defects.insert(0, "defect_id", [f"D{str(i+1).zfill(4)}" for i in range(len(defects))])

# ---------- commits.csv ----------
commits = truth[["module", "version", "commit_count", "contributors", "changed_lines"]].copy()
idx = rng.choice(commits.index, size=int(0.03 * len(commits)), replace=False)
commits.loc[idx, "contributors"] = np.nan
commits["module"] = commits["module"].map(mess)
commits = commits.rename(columns={"version": "release"})

# ---------- releases.csv (one row per module-release, with duplicates) ----------
releases = truth[["version", "release_date", "module"]].copy()
releases.insert(0, "release_id", [f"R{str(i+1).zfill(4)}" for i in range(len(releases))])
releases["release_date"] = releases["release_date"].dt.strftime("%Y-%m-%d")
releases["module"] = releases["module"].map(mess)
releases = pd.concat([releases, releases.sample(12, random_state=SEED + 1)], ignore_index=True)
releases = releases.sample(frac=1, random_state=SEED).reset_index(drop=True)

# ---------- write ----------
modules.to_csv(f"{OUT}/modules.csv", index=False)
metrics.to_csv(f"{OUT}/metrics.csv", index=False)
defects.to_csv(f"{OUT}/defects.csv", index=False)
commits.to_csv(f"{OUT}/commits.csv", index=False)
releases.to_csv(f"{OUT}/releases.csv", index=False)
for n, d in [("modules", modules), ("metrics", metrics), ("defects", defects), ("commits", commits), ("releases", releases)]:
    print(f"{n}.csv: {d.shape[0]} rows x {d.shape[1]} cols | nulls={int(d.isna().sum().sum())} | dup rows={int(d.duplicated().sum())}")
