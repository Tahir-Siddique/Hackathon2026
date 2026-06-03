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
FKIE_RELEASE_BASE = "https://github.com/fkie-cad/nvd-json-data-feeds/releases/latest/download"
FKIE_CVE_2026_URL = f"{FKIE_RELEASE_BASE}/CVE-2026.json.xz"
FKIE_CVE_2025_URL = f"{FKIE_RELEASE_BASE}/CVE-2025.json.xz"
FKIE_CVE_2024_URL = f"{FKIE_RELEASE_BASE}/CVE-2024.json.xz"
FKIE_REPO_URL = "https://github.com/fkie-cad/nvd-json-data-feeds.git"
EPSS_URL_TEMPLATE = "https://epss.empiricalsecurity.com/epss_scores-{date}.csv.gz"
# NVD CPE Dictionary 2.0 (replaces retired official-cpe-dictionary_v2.3.xml)
CPE_DICTIONARY_20_ZIP_URL = "https://nvd.nist.gov/feeds/json/cpe/2.0/nvdcpe-2.0.zip"


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


def download_fkie_year(year: int, force: bool = False) -> Path | None:
    """Download and decompress FKIE CVE-YYYY.json.xz release asset."""
    urls = {2026: FKIE_CVE_2026_URL, 2025: FKIE_CVE_2025_URL, 2024: FKIE_CVE_2024_URL}
    if year not in urls:
        print(f"  skip: no URL configured for CVE-{year}")
        return None
    xz_path = DATA_DIR / f"CVE-{year}.json.xz"
    json_path = DATA_DIR / f"CVE-{year}.json"
    if json_path.exists() and not force:
        print(f"  skip (exists): {json_path.name}")
        return json_path
    download(urls[year], xz_path, force=force)
    sys.path.insert(0, str(ROOT))
    from src.paths import decompress_xz

    return decompress_xz(xz_path)


def clone_fkie_repo(force: bool = False) -> Path:
    """
    Optional shallow clone of fkie-nvd-json-data-feeds (reference / CVE-2026 chunks on main).
    Pipeline uses CVE-YYYY.json.xz releases, not the chunked repo layout.
    """
    import subprocess

    dest = DATA_DIR / "nvd-json-data-feeds"
    if dest.exists() and (dest / ".git").exists() and not force:
        print(f"  skip (exists): {dest.name}/")
        return dest
    if dest.exists() and force:
        import shutil

        shutil.rmtree(dest, ignore_errors=True)
    print(f"  cloning: {FKIE_REPO_URL} -> {dest}")
    subprocess.run(
        ["git", "clone", "--depth", "1", FKIE_REPO_URL, str(dest)],
        check=True,
        cwd=DATA_DIR,
    )
    print(f"  cloned: {dest} (see main/CVE-2026/ for chunked layout; pipeline uses release JSON)")
    return dest


def download_cpe_dictionary(force: bool = False) -> Path:
    dest = DATA_DIR / "nvdcpe-2.0.zip"
    download(CPE_DICTIONARY_20_ZIP_URL, dest, force=force)
    return dest


def main() -> None:
    force = "--force" in sys.argv
    cpe_only = "--cpe" in sys.argv
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if cpe_only:
        print("=== CPE Dictionary 2.0 (replaces legacy XML) ===")
        download_cpe_dictionary(force=force)
        print("\nSpot-check: python scripts/lookup_cpe.py \"microsoft 365\"")
        return

    print("=== CISA KEV ===")
    download(KEV_URL, DATA_DIR / "known_exploited_vulnerabilities.json", force=force)

    print("\n=== EPSS ===")
    download_epss()

    print("\n=== NVD (FKIE) — primary year 2026 ===")
    download_fkie_year(2026, force=force)
    if "--with-2025" in sys.argv:
        download_fkie_year(2025, force=force)
    if "--with-2024" in sys.argv:
        download_fkie_year(2024, force=force)

    if "--clone-repo" in sys.argv or force:
        print("\n=== FKIE repo (optional reference clone) ===")
        try:
            clone_fkie_repo(force=force)
        except Exception as e:
            print(f"  warning: git clone failed ({e})")
            print("  release JSON above is sufficient for the pipeline")

    print("\n=== CPE Dictionary 2.0 (optional, ~79 MB) ===")
    cpe_zip = DATA_DIR / "nvdcpe-2.0.zip"
    if cpe_zip.exists() and not force:
        print(f"  skip (exists): {cpe_zip.name}")
    else:
        try:
            download_cpe_dictionary(force=force)
        except Exception as e:
            print(f"  warning: CPE download failed ({e})")
            print("  retry later: python scripts/download_datasets.py --cpe")

    print("\n=== Done ===")
    from src.paths import dataset_status

    for key, value in dataset_status().items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
