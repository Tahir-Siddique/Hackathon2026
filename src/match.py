"""Steps 5–6: Extract CPEs from NVD and match to normalised assets."""

from __future__ import annotations

from typing import Any, Iterable


def parse_cpe_vendor_product(criteria: str) -> str | None:
    """Return vendor:product from a CPE 2.3 criteria string."""
    if not criteria or not criteria.startswith("cpe:"):
        return None
    parts = criteria.split(":")
    if len(parts) < 5:
        return None
    # cpe:2.3:part:vendor:product
    vendor, product = parts[3], parts[4]
    if vendor in ("*", "-", "") or product in ("*", "-", ""):
        return None
    return f"{vendor}:{product}"


def extract_cpe_keys(cve_item: dict[str, Any]) -> set[str]:
    """Collect vendor:product keys from all CPE match criteria on a CVE."""
    keys: set[str] = set()
    for config in cve_item.get("configurations") or []:
        for node in config.get("nodes") or []:
            _walk_nodes(node, keys)
    return keys


def _walk_nodes(node: dict[str, Any], keys: set[str]) -> None:
    for match in node.get("cpeMatch") or []:
        if not match.get("vulnerable", True):
            continue
        criteria = match.get("criteria") or ""
        key = parse_cpe_vendor_product(criteria)
        if key:
            keys.add(key)
    for child in node.get("children") or []:
        _walk_nodes(child, keys)


def get_cvss_score(cve_item: dict[str, Any]) -> float:
    """Extract base CVSS score from NVD metrics block."""
    metrics = cve_item.get("metrics") or {}
    for version in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        entries = metrics.get(version)
        if not entries:
            continue
        for entry in entries:
            data = entry.get("cvssData") or {}
            score = data.get("baseScore")
            if score is not None:
                return float(score)
    return 0.0


def get_description(cve_item: dict[str, Any]) -> str:
    for desc in cve_item.get("descriptions") or []:
        if desc.get("lang") == "en":
            return desc.get("value", "")
    descriptions = cve_item.get("descriptions") or []
    return descriptions[0].get("value", "") if descriptions else ""


def match_cves_to_assets(
    nvd_items: Iterable[dict[str, Any]],
    normalised_assets: list[dict[str, Any]],
    vendor_filter: bool = True,
) -> list[dict[str, Any]]:
    """
    Scan NVD and return raw match rows (one per CVE–asset pair).
    """
    target_keys = {a["cpe_key"] for a in normalised_assets}
    key_to_assets: dict[str, list[dict[str, Any]]] = {}
    for asset in normalised_assets:
        key_to_assets.setdefault(asset["cpe_key"], []).append(asset)

    vendors: set[str] | None = None
    if vendor_filter:
        vendors = {a["vendor"] for a in normalised_assets}

    matches: list[dict[str, Any]] = []
    for item in nvd_items:
        cpe_keys = extract_cpe_keys(item)
        if not cpe_keys:
            continue
        if vendors and not any(
            k.split(":", 1)[0] in vendors for k in cpe_keys
        ):
            continue

        hit_keys = cpe_keys & target_keys
        if not hit_keys:
            continue

        cve_id = (item.get("id") or "").upper()
        if not cve_id:
            continue

        for key in hit_keys:
            for asset in key_to_assets[key]:
                matches.append(
                    {
                        "cve_id": cve_id,
                        "affected_asset": asset["user_label"],
                        "cpe_key": key,
                        "cvss": get_cvss_score(item),
                        "description": get_description(item),
                        "_cve_item": item,
                    }
                )
    return matches
