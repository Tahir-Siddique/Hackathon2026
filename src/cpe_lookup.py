"""Search NVD CPE Dictionary 2.0 (offline zip) for vendor/product verification."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any, Iterator

from src.paths import DATA_DIR

CPE_ZIP_DEFAULT = DATA_DIR / "nvdcpe-2.0.zip"
# Legacy hackathon filename (retired by NIST Aug 2025) — see data/CPE_DICTIONARY.md
CPE_LEGACY_XML_NAME = "official-cpe-dictionary_v2.3.xml"


def find_cpe_zip(path: Path | None = None) -> Path | None:
    if path and path.exists():
        return path
    candidates = [
        DATA_DIR / "nvdcpe-2.0.zip",
        DATA_DIR / "official-cpe-dictionary_v2.3.xml.zip",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query.lower().strip())


def _product_matches(product: dict[str, Any], query: str) -> bool:
    cpe = product.get("cpe") or {}
    cpe_name = (cpe.get("cpeName") or "").lower()
    if query in cpe_name:
        return True
    for title in cpe.get("titles") or []:
        if query in (title.get("title") or "").lower():
            return True
    return False


def iter_cpe_products(zip_path: Path) -> Iterator[dict[str, Any]]:
    with zipfile.ZipFile(zip_path) as zf:
        for name in sorted(zf.namelist()):
            if not name.endswith(".json"):
                continue
            with zf.open(name) as handle:
                payload = json.load(handle)
            for product in payload.get("products") or []:
                yield product


def search_cpe_dictionary(
    query: str,
    zip_path: Path | None = None,
    max_results: int = 15,
) -> list[dict[str, str]]:
    """
    Search CPE Dictionary 2.0 chunks for a product name or vendor:product string.
    Returns list of {cpe_name, title, chunk}.
    """
    zpath = find_cpe_zip(zip_path)
    if not zpath:
        raise FileNotFoundError(
            "CPE dictionary not found. Run: python scripts/download_datasets.py --cpe"
        )

    q = _normalize_query(query)
    results: list[dict[str, str]] = []

    with zipfile.ZipFile(zpath) as zf:
        for chunk in sorted(zf.namelist()):
            if not chunk.endswith(".json"):
                continue
            with zf.open(chunk) as handle:
                payload = json.load(handle)
            for product in payload.get("products") or []:
                if not _product_matches(product, q):
                    continue
                cpe = product.get("cpe") or {}
                titles = cpe.get("titles") or []
                en_title = next(
                    (t.get("title") for t in titles if t.get("lang") == "en"),
                    titles[0].get("title") if titles else "",
                )
                results.append(
                    {
                        "cpe_name": cpe.get("cpeName", ""),
                        "title": en_title or "",
                        "chunk": Path(chunk).name,
                    }
                )
                if len(results) >= max_results:
                    return results
    return results


def parse_vendor_product(cpe_name: str) -> str | None:
    """Return vendor:product from cpe:2.3:a:vendor:product:..."""
    if not cpe_name.startswith("cpe:"):
        return None
    parts = cpe_name.split(":")
    if len(parts) >= 5:
        return f"{parts[3]}:{parts[4]}"
    return None
