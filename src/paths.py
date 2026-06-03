"""Resolve offline data file paths under data/."""

from __future__ import annotations

import lzma
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
NVD_FEEDS_DIR = DATA_DIR / "nvd-json-data-feeds"


def _newest(glob_pattern: str, directory: Path = DATA_DIR) -> Path | None:
    matches = sorted(directory.glob(glob_pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def _cve_year_from_path(path: Path) -> int | None:
    """Parse CVE-YYYY from filename."""
    stem = path.name.replace(".json.xz", "").replace(".json", "")
    if stem.startswith("CVE-") and stem[4:].isdigit():
        return int(stem[4:])
    return None


def find_nvd_cve_json(year: int | None = None) -> Path | None:
    """Find decompressed FKIE-style CVE-YYYY.json (or .xz to decompress later)."""
    if year is not None:
        for directory in (DATA_DIR, NVD_FEEDS_DIR):
            for name in (f"CVE-{year}.json", f"CVE-{year}.json.xz"):
                path = directory / name
                if path.exists():
                    return path
        return None

    best: Path | None = None
    best_year = -1
    for directory in (DATA_DIR, NVD_FEEDS_DIR):
        for pattern in ("CVE-*.json", "CVE-*.json.xz"):
            for path in directory.glob(pattern):
                y = _cve_year_from_path(path)
                if y is not None and y > best_year:
                    best_year = y
                    best = path
    return best


def find_kev_json() -> Path | None:
    path = DATA_DIR / "known_exploited_vulnerabilities.json"
    return path if path.exists() else None


def find_epss_csv() -> Path | None:
    return _newest("epss_scores*.csv") or _newest("epss_scores*.csv.gz")


def find_cpe_dictionary_zip() -> Path | None:
    """CPE Dictionary 2.0 zip (replaces retired official-cpe-dictionary_v2.3.xml)."""
    for name in ("nvdcpe-2.0.zip", "official-cpe-dictionary_v2.3.xml.zip"):
        path = DATA_DIR / name
        if path.exists():
            return path
    return None


def decompress_xz(xz_path: Path) -> Path:
    """Decompress CVE-YYYY.json.xz to CVE-YYYY.json beside the source file."""
    if xz_path.suffix != ".xz":
        raise ValueError(f"Not an .xz file: {xz_path}")
    out_path = xz_path.with_suffix("")  # strips .xz → .json
    if out_path.exists() and out_path.stat().st_mtime >= xz_path.stat().st_mtime:
        return out_path
    with lzma.open(xz_path, "rb") as src, open(out_path, "wb") as dst:
        dst.write(src.read())
    return out_path


def resolve_nvd_path(preferred: Path | None = None) -> Path:
    """Return path to NVD JSON, decompressing .xz if needed."""
    if preferred and preferred.exists():
        path = preferred
    else:
        found = find_nvd_cve_json()
        if not found:
            raise FileNotFoundError(
                "No NVD CVE file found. Add CVE-2026.json or CVE-2026.json.xz under data/ "
                "(see data/README.md)."
            )
        path = found

    if path.suffix == ".xz":
        return decompress_xz(path)
    return path


def dataset_status() -> dict[str, str]:
    """Human-readable status for each expected feed."""
    nvd = find_nvd_cve_json()
    if nvd and nvd.suffix == ".xz":
        decompressed = nvd.with_suffix("")
        nvd_status = (
            f"ready ({decompressed.name}, {decompressed.stat().st_size // 1_000_000} MB)"
            if decompressed.exists()
            else f"compressed ({nvd.name}) — will decompress on first run"
        )
    elif nvd:
        nvd_status = f"ready ({nvd.name})"
    else:
        nvd_status = "missing — add CVE-YYYY.json or CVE-YYYY.json.xz"

    kev = find_kev_json()
    epss = find_epss_csv()

    modified_zip = DATA_DIR / "nvdcve-2.0-modified.json.zip"
    extra = []
    if modified_zip.exists():
        extra.append("nvdcve-2.0-modified.json.zip present (NVD 2.0 bulk — not used by default pipeline)")
    if (NVD_FEEDS_DIR / ".git").is_dir():
        extra.append("nvd-json-data-feeds/ FKIE repo clone present (optional; release JSON in data/ is used)")
    elif NVD_FEEDS_DIR.exists() and not any(NVD_FEEDS_DIR.glob("CVE-*.json*")):
        extra.append("nvd-json-data-feeds/ empty — run: python scripts/download_datasets.py --clone-repo")

    cpe = find_cpe_dictionary_zip()
    legacy_xml = DATA_DIR / "official-cpe-dictionary_v2.3.xml"
    if legacy_xml.exists():
        cpe_status = f"ready (legacy XML {legacy_xml.name})"
    elif cpe:
        size_mb = cpe.stat().st_size / (1024 * 1024)
        cpe_status = f"ready ({cpe.name}, {size_mb:.0f} MB) — CPE 2.0 JSON chunks"
    else:
        cpe_status = "optional — run: python scripts/download_datasets.py --cpe"

    return {
        "nvd": nvd_status,
        "kev": f"ready ({kev.name})" if kev else "missing — download CISA KEV JSON",
        "epss": f"ready ({epss.name})" if epss else "missing — download epss_scores-*.csv",
        "cpe": cpe_status,
        "notes": "; ".join(extra) if extra else "ok",
    }
