# CVE-to-My-Stack Translator

CyberHack 2026 — Project 1. Filters offline NVD, EPSS, and CISA KEV data to a prioritised CVE action list for your software stack.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/download_datasets.py   # first time only
python translate.py --brief
pytest
```

## Outputs

| File | Description |
|------|-------------|
| `output/prioritised_cves.csv` | Ranked CVE table (MVP columns) |
| `output/executive_brief.md` | One-page summary (`--brief`) |

## Docs

- [PLAN.md](PLAN.md) — implementation steps
- [DEMO.md](DEMO.md) — 5-minute presentation script
- [data/README.md](data/README.md) — dataset layout

## Tests

```powershell
pytest                  # all tests (includes ~6s integration with real data)
pytest -m "not integration"   # fast fixture-only tests
```
