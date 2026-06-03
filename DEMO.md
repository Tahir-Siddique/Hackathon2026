# 5-Minute Demo Script — CVE-to-My-Stack Translator

## Before you present

```powershell
cd Hackathon2026
.\.venv\Scripts\Activate.ps1
python translate.py --brief
# Opens: output/prioritised_cves.csv + output/executive_brief.md
jupyter notebook starter_notebook.ipynb   # optional live exploration
pytest                                  # show tests pass
```

---

## 1. Problem (30 seconds)

> "Small IT teams see hundreds of new CVEs daily. They can't tell which three matter for *their* stack. We built a filter: asset list in, prioritised action list out."

---

## 2. Pipeline (60 seconds)

Show diagram or `src/pipeline.py` flow:

1. **Normalise** informal names → CPE `vendor:product` (hardest step)
2. **Match** NVD configurations
3. **Enrich** EPSS + CISA KEV
4. **Rank** KEV first, then urgency (CVSS + EPSS)
5. **Export** CSV + plain-English summaries

**Approach:** Python data pipeline (pandas, rapidfuzz) — offline files only.

---

## 3. Live run (2 minutes)

```powershell
python translate.py data/sample_asset_list.txt --brief
```

Point out:

- 12/12 assets mapped (normalisation dictionary)
- KEV rows at top (e.g. Windows Server / Chrome)
- `output/prioritised_cves.csv` columns: CVE, asset, CVSS, EPSS, KEV, risk summary

Optional fuzzy example: add alias in `config/normalisation_map.json` for "M365" → `microsoft:365_apps`.

---

## 4. Design choices (60 seconds)

| Choice | Why |
|--------|-----|
| FKIE NVD JSON | Offline, per-year, CPE configurations included |
| KEV set + EPSS dict | O(1) lookup; KEV = strongest urgency signal |
| Fuzzy aliases (`rapidfuzz`) | Handles "Office 365" vs "Microsoft 365 Apps for Business" |
| Vendor pre-filter | Keeps scan of 44k CVEs fast (~6s) |
| Top 50 cap | Actionable list, not thousands of rows |

---

## 5. Limitations (30 seconds)

1. Wrong normalisation → **silent miss** (no error)
2. Low EPSS ≠ safe
3. Not in KEV ≠ never exploited
4. **No version range matching** in MVP (may over-match)

---

## Evaluation checklist

- [x] Loads NVD + KEV + EPSS
- [x] 15+ product normalisation map
- [x] Relevant CVE filtering
- [x] KEV-first prioritisation
- [x] Plain-English output
- [x] Automated tests (`pytest`)

---

## Commands reference

| Command | Purpose |
|---------|---------|
| `python translate.py` | Full run on sample assets |
| `python translate.py --brief` | CSV + executive brief |
| `python translate.py --smoke` | Verify feeds load |
| `python scripts/download_datasets.py` | Refresh offline data |
| `pytest` | Unit + integration tests |
| `pytest -m "not integration"` | Fast tests only (fixtures) |
