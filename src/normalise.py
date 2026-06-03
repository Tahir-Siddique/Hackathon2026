"""Steps 3–4: Map informal asset names to CPE vendor:product."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from rapidfuzz import fuzz, process

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "normalisation_map.json"
FUZZ_THRESHOLD = 85


def _clean(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s.-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_normalisation_map(path: Path | None = None) -> list[dict[str, Any]]:
    map_path = path or CONFIG_PATH
    with open(map_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["products"]


def build_alias_index(products: list[dict[str, Any]]) -> list[tuple[str, str, str, str]]:
    """Return (alias, vendor, product, display_name) tuples."""
    index: list[tuple[str, str, str, str]] = []
    for entry in products:
        vendor = entry["vendor"]
        product = entry["product"]
        display = entry.get("display_name", f"{vendor}:{product}")
        for alias in entry.get("aliases", []):
            index.append((_clean(alias), vendor, product, display))
        index.append((_clean(display), vendor, product, display))
    return index


def normalise_asset(
    asset: dict[str, str],
    alias_index: list[tuple[str, str, str, str]],
    alias_choices: list[str],
) -> dict[str, Any] | None:
    """Map one asset to vendor/product; None if no match above threshold."""
    query = _clean(asset.get("name") or asset.get("user_label", ""))
    if not query:
        return None

    for alias, vendor, product, display in alias_index:
        if query == alias or query in alias or alias in query:
            return {
                "user_label": asset.get("user_label", asset.get("name", "")),
                "vendor": vendor,
                "product": product,
                "display_name": display,
                "cpe_key": f"{vendor}:{product}",
                "confidence": 100.0,
                "match_method": "exact",
            }

    result = process.extractOne(
        query,
        alias_choices,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=FUZZ_THRESHOLD,
    )
    if not result:
        return None

    matched_alias, score, _idx = result
    for alias, vendor, product, display in alias_index:
        if alias == matched_alias:
            return {
                "user_label": asset.get("user_label", asset.get("name", "")),
                "vendor": vendor,
                "product": product,
                "display_name": display,
                "cpe_key": f"{vendor}:{product}",
                "confidence": float(score),
                "match_method": "fuzzy",
            }
    return None


def normalise_assets(
    assets: list[dict[str, str]],
    map_path: Path | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Normalise all assets; return (mapped, unmapped)."""
    products = load_normalisation_map(map_path)
    alias_index = build_alias_index(products)
    alias_choices = [alias for alias, *_ in alias_index]

    mapped: list[dict[str, Any]] = []
    unmapped: list[dict[str, str]] = []
    seen_keys: set[str] = set()

    for asset in assets:
        hit = normalise_asset(asset, alias_index, alias_choices)
        if hit is None:
            unmapped.append(asset)
            continue
        key = hit["cpe_key"]
        if key not in seen_keys:
            seen_keys.add(key)
            mapped.append(hit)
    return mapped, unmapped
