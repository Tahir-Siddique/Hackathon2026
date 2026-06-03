# Demo Guide — CVE-to-My-Stack Translator

Aligned with **Hackathon Guide §9 Suggested Build Approach** (5-hour build → 5-minute presentation).

**Approach:** Python data pipeline (Approach A) — offline feeds only, no live APIs.

---

## Before you present

```powershell
cd c:\Users\tahir\Desktop\Hackathon2026
.\.venv\Scripts\Activate.ps1
python translate.py --brief
pytest -q
```

Have open:

- `data/sample_asset_list.txt` (input)
- `output/prioritised_cves.csv` (output)
- `output/executive_brief.md` (optional summary)
- `config/normalisation_map.json` (hardest step)

---

## What we built (§9 — hour by hour)

This is how the project follows the official suggested sequence. Use it to **explain your design** in the demo.

### Hour 1 — Data loading and exploration (0:00–1:00)

**Guide objectives**

1. Load EPSS CSV — confirm columns and score range  
2. Load CISA KEV JSON — Python `set` of CVE IDs  
3. Load one year of NVD CVE JSON — find CPEs, descriptions, CVSS  
4. Load the facilitator sample asset list  

**What we implemented**

| Item | File / command |
|------|----------------|
| Loaders | `src/loaders.py` |
| EPSS → dict | `load_epss()` |
| KEV → set | `load_kev()` |
| NVD → list | `load_nvd()` from `data/CVE-2025.json` |
| Asset parser | `parse_asset_list()` |
| Smoke test | `python translate.py --smoke` |
| Exploration | `starter_notebook.ipynb` (cells 1–2) |
| Download feeds | `python scripts/download_datasets.py` |

**Demo line (30s)**

> “First we wired three offline feeds: NVD for CVE details and CPEs, CISA KEV for confirmed exploitation, and EPSS for likelihood in the next 30 days. Everything stays local — no API calls during the run.”

**Show**

```powershell
python translate.py --smoke
```

Expect: `kev_count`, `epss_count`, `nvd_count` (~1610 / ~337k / ~44525).

---

### Hour 2 — Normalisation dictionary (1:00–2:00)

**Guide objectives**

1. Review CPE dictionary naming conventions  
2. Build a map of ≥15 common products → CPE `vendor:product`  
3. Normalisation function with fuzzy matching  
4. Test informal inputs (sample asset list)  

**What we implemented**

| Item | File / command |
|------|----------------|
| Dictionary (19 products) | `config/normalisation_map.json` |
| Fuzzy match | `src/normalise.py` (`rapidfuzz`, threshold 85) |
| CPE 2.0 reference | `data/nvdcpe-2.0.zip` (replaces retired XML) |
| Spot-check CPE | `python scripts/lookup_cpe.py "microsoft 365"` |
| Docs | `data/CPE_DICTIONARY.md` |

**Demo line (60s) — emphasise this as the hardest step**

> “CVE matching fails silently if we map ‘Office 365 Business’ to the wrong CPE. We built an alias dictionary plus fuzzy matching so informal names hit the right `vendor:product`. All twelve facilitator sample products map at 100% confidence.”

**Show**

- `config/normalisation_map.json` — one entry (e.g. Microsoft 365 → `microsoft:365_apps`)  
- Live normalisation lines when you run `translate.py` (`OK … -> microsoft:365_apps`)  
- Optional: `python scripts/lookup_cpe.py "google chrome"` to prove against the official CPE dictionary  

---

### Hour 3 — CVE matching and filtering (2:00–3:00)

**Guide objectives**

1. Filter NVD by CPE `vendor:product` from normalised assets  
2. Run for each asset in the list  
3. Merge matches with EPSS scores and KEV flags  

**What we implemented**

| Item | File |
|------|------|
| Extract CPEs from NVD | `src/match.py` — `extract_cpe_keys()`, `parse_cpe_vendor_product()` |
| Match to stack | `match_cves_to_assets()` (vendor pre-filter for speed) |
| Enrich EPSS + KEV | `src/rank.py` — `enrich_and_rank()` |
| Orchestration | `src/pipeline.py` |

**MVP rule (per guide):** match on `vendor:product` only — no version ranges yet.

**Demo line (30s)**

> “We walk each CVE’s NVD configuration blocks, pull CPE criteria strings, and keep any CVE that matches our stack. Then we attach EPSS and a yes/no KEV flag from pre-loaded dictionaries.”

**Show**

- Mention: ~1,183 raw matches on sample list → capped to top 50 for actionability  

---

### Hour 4 — Ranking and output (3:00–4:00)

**Guide objectives**

1. Sort: KEV entries first, then EPSS descending  
2. Plain-English risk sentence per CVE  
3. Write CSV  
4. Print summary table to console  

**What we implemented**

| Item | File |
|------|------|
| Sort + combined urgency | `src/rank.py` (KEV → urgency score → EPSS → CVSS) |
| Risk templates | `src/summarise.py` |
| CSV + table | `src/export.py` |
| CLI | `translate.py` |
| Stretch: executive brief | `translate.py --brief` → `output/executive_brief.md` |

**Required CSV columns**

`cve_id`, `affected_asset`, `cvss`, `epss`, `kev`, `risk_summary`

**Demo line (60s)**

> “Ranking is KEV first — if CISA says it’s actively exploited, it goes to the top. Then we use EPSS and CVSS. Each row gets one sentence a non-expert can act on.”

**Show**

- Open `output/prioritised_cves.csv`  
- Read **one** `risk_summary` aloud, e.g. top Windows Server row with KEV yes and high EPSS  

---

### Hour 5 — Testing, refinement, and demo prep (4:00–5:00)

**Guide objectives**

1. Full pipeline on `sample_asset_list.txt`  
2. Fix errors and edge cases  
3. Prepare 5-minute demo (what / hardest step / output)  
4. Stretch goals if time allows  

**What we implemented**

| Item | File / command |
|------|----------------|
| End-to-end CLI | `python translate.py data/sample_asset_list.txt --brief` |
| Tests (40) | `pytest` — `tests/` + fixtures |
| Demo script | This file (`DEMO.md`) |
| Stretch | Combined urgency score, `--brief`, full CLI flags |

**Demo line (30s)**

> “We test against the facilitator list and automated fixtures. Forty tests cover loaders, all twelve sample normalisations, KEV-first ranking, and the full pipeline.”

**Show (optional, 15s)**

```powershell
pytest -q
```

---

## 5-minute presentation script (walk the hours in ~5 min)

| Time | §9 phase | What to do |
|------|----------|------------|
| **0:00–0:30** | — | **Problem:** CVE firehose vs one sysadmin; asset list in → prioritised list out. |
| **0:30–1:30** | Hours 1–2 | **Pipeline + normalisation:** Show `sample_asset_list.txt` → dictionary → “silent miss” risk. |
| **1:30–3:00** | Hours 3–4 | **Live run:** `python translate.py --brief` → show CSV top rows, read one risk summary. |
| **3:00–4:00** | Hour 4–5 | **Design + quality:** Offline feeds, KEV-first, fuzzy aliases, `pytest`. |
| **4:00–5:00** | Limits | **Honest gaps:** wrong map = miss; low EPSS ≠ safe; no version matching in MVP. |

**Opening sentence**

> “We followed the suggested five-hour build: load offline data, normalise the stack, match NVD, rank with KEV and EPSS, and export a short action list — here’s that pipeline running on the facilitator sample.”

**Closing sentence**

> “The core challenge is normalisation; the core value is turning hundreds of CVEs into fifty prioritised, plain-English actions for this specific stack.”

---

## Limitations (state clearly — guide §7.3)

1. **Silent misses** — wrong product alias → CVE never appears  
2. **EPSS** — predictive, not “safe”  
3. **KEV** — absence does not mean unexploited  
4. **Versions** — MVP matches product family only, not version ranges  
5. **CPE dictionary** — legacy XML retired; we use NVD CPE Dictionary 2.0 (`nvdcpe-2.0.zip`) for reference only  

---

## Evaluation checklist (guide §11)

| Criterion | How we demonstrate |
|-----------|-------------------|
| Data pipeline | `--smoke` or live run loads NVD + KEV + EPSS |
| Normalisation | 12/12 sample assets; show `normalisation_map.json` |
| Matching | Relevant CVEs for Chrome, Windows, OpenSSL, etc. |
| Prioritisation | KEV rows at top of CSV |
| Output clarity | Read one `risk_summary` aloud |
| Limitations | 30-second honest list above |
| Tests | `pytest` — 40 passed |

---

## Commands reference

| Command | §9 phase | Purpose |
|---------|----------|---------|
| `python scripts/download_datasets.py` | Hour 1 | Download KEV, EPSS, NVD, CPE zip |
| `python translate.py --smoke` | Hour 1 | Verify feeds load |
| `python scripts/lookup_cpe.py "…"` | Hour 2 | Verify CPE vendor:product |
| `python translate.py --brief` | Hours 3–4 | Full pipeline + CSV + brief |
| `jupyter notebook starter_notebook.ipynb` | Hours 1–4 | Step-by-step exploration |
| `pytest` | Hour 5 | Automated validation |

---

## Architecture (one diagram for slides)

```text
sample_asset_list.txt
        │
        ▼
  [Hour 2] Normalise (dictionary + rapidfuzz)
        │
        ▼
  [Hour 3] Match NVD CPE configurations
        │
        ▼
  [Hour 3] Enrich EPSS + KEV
        │
        ▼
  [Hour 4] Rank (KEV first) → Summarise → CSV + brief
```

**Data inputs (Hour 1):** `CVE-2025.json`, `known_exploited_vulnerabilities.json`, `epss_scores-*.csv`

---

*Demo guide v2 — structured on Hackathon Project Guide §9 Suggested Build Approach*
