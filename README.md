# CVE-to-My-Stack Translator

CyberHack 2026 — Project 1. Filters offline NVD, EPSS, and CISA KEV data to a prioritised CVE action list for your software stack.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/download_datasets.py   # first time only
python scripts/download_datasets.py --cpe   # optional CPE dictionary (~79 MB)
python translate.py --brief
pytest
```

## Outputs

| File | Description |
|------|-------------|
| `output/prioritised_cves.csv` | Ranked CVE table (MVP columns) |
| `output/executive_brief.md` | One-page summary (`--brief`) |

## Web UI (FastAPI + Jinja + Tailwind)

```powershell
pip install -r ui/requirements.txt
uvicorn ui.app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 — see [ui/README.md](ui/README.md).

## Presentation (5 min)

- [presentation/SLIDES.md](presentation/SLIDES.md) — Marp slides (export to PDF/PPTX)
- [presentation/slides.html](presentation/slides.html) — browser slideshow (double-click or local server)
- [presentation/SPEAKER_NOTES.md](presentation/SPEAKER_NOTES.md) — timing per slide

## Docs

- [PLAN.md](PLAN.md) — implementation steps
- [DEMO.md](DEMO.md) — 5-minute presentation script
- [REQUIREMENTS_VERIFICATION.md](REQUIREMENTS_VERIFICATION.md) — guide compliance & use cases
- [data/README.md](data/README.md) — dataset layout

## Tests

```powershell
pytest                  # all tests (includes ~6s integration with real data)
pytest -m "not integration"   # fast fixture-only tests
```
