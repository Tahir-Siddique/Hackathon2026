#!/usr/bin/env python3
"""Download required offline datasets into data/."""

from __future__ import annotations

import gzip
import shutil
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
FKIE_CVE_2025_URL = (
    "https://github.com/fkie-cad/nvd-json-data-feeds/releases/latest/download/CVE-2025.json.xz"
)
FKIE_CVE_2024_URL = (
    "https://github.com/fkie-cad/nvd-json-data-feeds/releases/latest/download/CVE-2024.json.xz"
)
EPSS_URL_TEMPLATE = "https://epss.empiricalsecurity.com/epss_scores-{date}.csv.gz"


def download(url: str, dest: Path, force: bool = False) -> None:
    if dest.exists() and not force:
        print(f"  skip (exists): {dest.name}")
        return
    print(f"  downloading: {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Hackathon2026-CVE-Translator/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        dest.write_bytes(resp.read())
    size_mb = dest.stat().st_size / (1024 * 1024)
    print(f"  saved: {dest.name} ({size_mb:.2f} MB)")


def decompress_gz(gz_path: Path) -> Path:
    out_path = gz_path.with_suffix("")  # .csv.gz -> .csv
    if out_path.exists() and out_path.stat().st_mtime >= gz_path.stat().st_mtime:
        print(f"  skip decompress (exists): {out_path.name}")
        return out_path
    print(f"  decompressing: {gz_path.name} -> {out_path.name}")
    with gzip.open(gz_path, "rb") as src, open(out_path, "wb") as dst:
        shutil.copyfileobj(src, dst)
    return out_path


def download_epss(days_back: int = 14) -> Path:
    existing = sorted(DATA_DIR.glob("epss_scores-*.csv"), reverse=True)
    if existing:
        print(f"  skip (exists): {existing[0].name}")
        return existing[0]
    for offset in range(days_back):
        d = date.today() - timedelta(days=offset)
        date_str = d.isoformat()
        url = EPSS_URL_TEMPLATE.format(date=date_str)
        gz_path = DATA_DIR / f"epss_scores-{date_str}.csv.gz"
        try:
            download(url, gz_path)
            return decompress_gz(gz_path)
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                print(f"  unavailable ({e.code}): {date_str}")
                continue
            raise
    raise RuntimeError(f"No EPSS file found in the last {days_back} days")


def main() -> None:
    force = "--force" in sys.argv
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("=== CISA KEV ===")
    download(KEV_URL, DATA_DIR / "known_exploited_vulnerabilities.json", force=force)

    print("\n=== EPSS ===")
    download_epss()

    print("\n=== NVD (FKIE) ===")
    nvd_2025_xz = DATA_DIR / "CVE-2025.json.xz"
    nvd_2025_json = DATA_DIR / "CVE-2025.json"
    if not nvd_2025_json.exists():
        download(FKIE_CVE_2025_URL, nvd_2025_xz, force=force)
    else:
        print("  skip (exists): CVE-2025.json")

    nvd_2024_json = DATA_DIR / "CVE-2024.json"
    nvd_2024_xz = DATA_DIR / "CVE-2024.json.xz"
    if not nvd_2024_json.exists() and not nvd_2024_xz.exists():
        download(FKIE_CVE_2024_URL, nvd_2024_xz, force=force)
    else:
        print("  skip: CVE-2024 already present")

    # Decompress NVD xz files
    sys.path.insert(0, str(ROOT))
    from src.paths import decompress_xz

    for xz in sorted(DATA_DIR.glob("CVE-*.json.xz")):
        json_path = xz.with_suffix("")
        if not json_path.exists() or force:
            print(f"\n=== Decompress {xz.name} ===")
            out = decompress_xz(xz)
            print(f"  wrote: {out.name} ({out.stat().st_size / (1024**2):.1f} MB)")

    print("\n=== Done ===")
    from src.paths import dataset_status

    for key, value in dataset_status().items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
