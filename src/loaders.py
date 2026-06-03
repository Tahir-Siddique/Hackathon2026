"""Step 1–2: Load offline feeds and parse asset lists."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterator

from src.paths import find_epss_csv, find_kev_json, resolve_nvd_path


def load_kev(path: Path | None = None) -> set[str]:
    """Load CISA KEV catalogue as a set of CVE IDs."""
    kev_path = path or find_kev_json()
    if not kev_path or not kev_path.exists():
        raise FileNotFoundError("KEV file not found: known_exploited_vulnerabilities.json")
    with open(kev_path, encoding="utf-8") as f:
        data = json.load(f)
    return {entry["cveID"].upper() for entry in data["vulnerabilities"]}


def load_epss(path: Path | None = None) -> dict[str, dict[str, float]]:
    """Load EPSS scores keyed by CVE ID."""
    epss_path = path or find_epss_csv()
    if not epss_path or not epss_path.exists():
        raise FileNotFoundError("EPSS CSV not found in data/")
    scores: dict[str, dict[str, float]] = {}
    with open(epss_path, encoding="utf-8") as f:
        lines = [line for line in f if not line.startswith("#")]
    reader = csv.DictReader(lines)
    for row in reader:
        cve_id = row["cve"].strip().upper()
        scores[cve_id] = {
            "epss": float(row["epss"]),
            "percentile": float(row["percentile"]),
        }
    return scores


def load_nvd(path: Path | None = None) -> list[dict[str, Any]]:
    """Load NVD CVE items from FKIE JSON feed."""
    nvd_path = resolve_nvd_path(path) if path else resolve_nvd_path()
    with open(nvd_path, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("cve_items") or data.get("CVE_Items") or data.get("vulnerabilities")
    if items is None:
        raise ValueError(f"Unrecognised NVD JSON structure in {nvd_path}")
    return items


def iter_nvd(path: Path | None = None) -> Iterator[dict[str, Any]]:
    """Yield CVE records from NVD JSON."""
    yield from load_nvd(path)


def parse_asset_list(path: Path) -> list[dict[str, str]]:
    """Parse asset list file into name, version, raw_line records."""
    assets: list[dict[str, str]] = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "\t" in line:
                parts = line.split("\t", 1)
            elif "," in line and not line.upper().startswith("CVE-"):
                parts = line.split(",", 1)
            else:
                parts = line.rsplit(None, 1) if " " in line else [line]
            name = parts[0].strip()
            version = parts[1].strip() if len(parts) > 1 else ""
            assets.append(
                {
                    "name": name,
                    "version": version,
                    "raw_line": line,
                    "user_label": f"{name} {version}".strip(),
                }
            )
    return assets


def smoke_test(
    nvd_path: Path | None = None,
    kev_path: Path | None = None,
    epss_path: Path | None = None,
) -> dict[str, int | str]:
    """Load all feeds and return summary counts."""
    kev_ids = load_kev(kev_path)
    epss = load_epss(epss_path)
    nvd_items = load_nvd(nvd_path)
    sample = nvd_items[0] if nvd_items else {}
    return {
        "kev_count": len(kev_ids),
        "epss_count": len(epss),
        "nvd_count": len(nvd_items),
        "sample_cve_id": sample.get("id", "n/a"),
        "sample_has_configurations": bool(sample.get("configurations")),
        "sample_has_metrics": bool(sample.get("metrics")),
    }
