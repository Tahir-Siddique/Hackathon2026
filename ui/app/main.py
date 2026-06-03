"""FastAPI + Jinja2 + Tailwind UI for CVE-to-My-Stack Translator."""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .deps import DATA_DIR, OUTPUT_DIR, PROJECT_ROOT, STATIC_DIR, TEMPLATES_DIR

from src.paths import dataset_status
from src.pipeline import run_pipeline

app = FastAPI(
    title="CVE-to-My-Stack Translator",
    description="Filter and prioritise CVEs for your software stack.",
)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

LATEST_CSV = OUTPUT_DIR / "latest_prioritised_cves.csv"


def _default_asset_text() -> str:
    sample = DATA_DIR / "sample_asset_list.txt"
    if sample.exists():
        return sample.read_text(encoding="utf-8")
    return "Google Chrome\tLatest\nOpenSSL\t3.0.7\n"


def _write_assets_temp(content: str) -> Path:
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8",
        dir=OUTPUT_DIR,
    )
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


async def _run_pipeline_async(
    asset_path: Path,
    max_rows: int,
) -> dict[str, Any]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: run_pipeline(
            asset_path,
            output_csv=LATEST_CSV,
            output_brief=OUTPUT_DIR / "latest_executive_brief.md",
            max_rows=max_rows,
        ),
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    status = dataset_status()
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "status": status,
            "default_assets": _default_asset_text(),
            "project_root": str(PROJECT_ROOT),
        },
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    assets_text: str = Form(""),
    max_rows: int = Form(50),
    asset_file: UploadFile | None = File(None),
):
    errors: list[str] = []

    if asset_file and asset_file.filename:
        raw = await asset_file.read()
        content = raw.decode("utf-8", errors="replace")
    elif assets_text.strip():
        content = assets_text
    else:
        errors.append("Provide an asset list in the text box or upload a file.")
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "status": dataset_status(),
                "default_assets": assets_text or _default_asset_text(),
                "errors": errors,
                "project_root": str(PROJECT_ROOT),
            },
            status_code=400,
        )

    max_rows = max(1, min(max_rows, 500))
    asset_path = _write_assets_temp(content)

    try:
        for key in ("nvd", "kev", "epss"):
            if "missing" in dataset_status().get(key, "").lower():
                errors.append(f"Dataset not ready: {key}. Run scripts/download_datasets.py from project root.")
        if errors:
            raise RuntimeError(" ".join(errors))

        result = await _run_pipeline_async(asset_path, max_rows)
    except Exception as exc:
        errors.append(str(exc))
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "status": dataset_status(),
                "default_assets": content,
                "errors": errors,
                "project_root": str(PROJECT_ROOT),
            },
            status_code=500,
        )
    finally:
        if asset_path.exists():
            asset_path.unlink(missing_ok=True)

    if not result["mapped"]:
        errors.append("No assets could be normalised. Check config/normalisation_map.json.")
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "status": dataset_status(),
                "default_assets": content,
                "errors": errors,
                "project_root": str(PROJECT_ROOT),
            },
            status_code=400,
        )

    criticality_order = ("Critical", "High", "Medium", "Low", "Unknown")
    criticality_counts: dict[str, int] = {}
    asset_counts: dict[str, int] = {}
    for row in result["rows"]:
        level = row.get("criticality", "Unknown")
        criticality_counts[level] = criticality_counts.get(level, 0) + 1
        asset = row.get("affected_asset", "")
        if asset:
            asset_counts[asset] = asset_counts.get(asset, 0) + 1
    criticality_counts = {
        k: criticality_counts[k]
        for k in criticality_order
        if k in criticality_counts
    }
    asset_counts_list = sorted(
        asset_counts.items(),
        key=lambda item: (-item[1], item[0].lower()),
    )

    return templates.TemplateResponse(
        request,
        "results.html",
        {
            "rows": result["rows"],
            "mapped": result["mapped"],
            "unmapped": result["unmapped"],
            "stats": result["stats"],
            "max_rows": max_rows,
            "csv_ready": LATEST_CSV.exists(),
            "criticality_counts": criticality_counts,
            "asset_counts": asset_counts_list,
        },
    )


@app.get("/download/csv")
async def download_csv():
    if not LATEST_CSV.exists():
        return RedirectResponse("/", status_code=302)
    return FileResponse(
        LATEST_CSV,
        media_type="text/csv",
        filename="prioritised_cves.csv",
    )


@app.get("/health")
async def health():
    return {"status": "ok", "datasets": dataset_status()}
