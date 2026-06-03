# CVE-to-My-Stack — Web UI

FastAPI + Jinja2 + Tailwind CSS (CDN) front end for the parent pipeline in `../`.

## Setup

From the **repository root** (`Hackathon2026/`):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r ui\requirements.txt
```

Ensure parent data feeds exist (`data/CVE-2025.json`, KEV, EPSS) — see `../data/README.md`.

## Run

```powershell
# From repository root
.\.venv\Scripts\uvicorn.exe ui.app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000

## Features

- Paste or upload asset list (`.txt`)
- Dataset status cards (NVD, KEV, EPSS, CPE)
- Prioritised results table (KEV highlighted)
- Download latest CSV

## Layout

```
ui/
├── app/
│   ├── main.py      # FastAPI routes
│   └── deps.py      # Paths into parent project
├── templates/       # Jinja + Tailwind
├── output/          # latest_prioritised_cves.csv (gitignored)
└── requirements.txt
```

The UI calls `src.pipeline.run_pipeline` from the parent project — no duplicate logic.
