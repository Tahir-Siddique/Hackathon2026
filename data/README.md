# Data directory

## Required feeds (pipeline)

| File | Purpose |
|------|---------|
| `CVE-2025.json` or `CVE-2024.json` | FKIE NVD CVE records (decompressed from `.xz`) |
| `known_exploited_vulnerabilities.json` | CISA KEV catalogue |
| `epss_scores-YYYY-MM-DD.csv` | EPSS daily scores |
| `sample_asset_list.txt` | Test asset list (included) |

## Download everything

From project root:

```powershell
.\.venv\Scripts\python.exe scripts\download_datasets.py
```

Re-download with overwrite:

```powershell
.\.venv\Scripts\python.exe scripts\download_datasets.py --force
```

**Sources**

| Feed | URL |
|------|-----|
| KEV | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json |
| EPSS | https://epss.empiricalsecurity.com/epss_scores-YYYY-MM-DD.csv.gz |
| NVD | https://github.com/fkie-cad/nvd-json-data-feeds/releases/latest/download/CVE-2025.json.xz |

EPSS for “today” may return 403 until published; the script tries the last 14 days.

## Optional / not used by default

| File | Notes |
|------|-------|
| `nvdcve-2.0-modified.json.zip` | Official NVD 2.0 bulk — different JSON schema |
| `nvd-json-data-feeds/` | Full git repo — not needed if `.xz` releases are in `data/` |
| `official-cpe-dictionary_v2.3.xml` | Reference for building normalisation map only |

## Decompress NVD only

```powershell
.\.venv\Scripts\python.exe scripts\decompress_nvd.py
```

## Check status

```powershell
.\.venv\Scripts\python.exe translate.py
```

## Starter notebook

Open `starter_notebook.ipynb` in the project root (same pipeline as `translate.py`, cell-by-cell).

```powershell
pip install jupyter ipykernel
jupyter notebook starter_notebook.ipynb
```
