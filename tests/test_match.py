"""Tests for src/match.py."""

from src.loaders import load_nvd
from src.match import (
    extract_cpe_keys,
    get_cvss_score,
    match_cves_to_assets,
    parse_cpe_vendor_product,
)
from src.normalise import normalise_assets
from src.loaders import parse_asset_list


def test_parse_cpe_vendor_product():
    assert parse_cpe_vendor_product("cpe:2.3:a:google:chrome:*:*:*:*:*:*:*:*") == "google:chrome"
    assert parse_cpe_vendor_product("cpe:2.3:o:microsoft:windows_10:*:*:*:*:*:*:*:*") == (
        "microsoft:windows_10"
    )
    assert parse_cpe_vendor_product("invalid") is None


def test_extract_cpe_keys(minimal_nvd_path):
    items = load_nvd(minimal_nvd_path)
    chrome = next(i for i in items if i["id"] == "CVE-2025-0001")
    keys = extract_cpe_keys(chrome)
    assert "google:chrome" in keys


def test_get_cvss_score(minimal_nvd_path):
    items = load_nvd(minimal_nvd_path)
    chrome = next(i for i in items if i["id"] == "CVE-2025-0001")
    assert get_cvss_score(chrome) == 9.8


def test_match_filters_by_stack(minimal_nvd_path, test_assets_path):
    items = load_nvd(minimal_nvd_path)
    assets = parse_asset_list(test_assets_path)
    mapped, _ = normalise_assets(assets[:3])  # chrome, windows, openssl
    matches = match_cves_to_assets(items, mapped)
    cve_ids = {m["cve_id"] for m in matches}
    assert "CVE-2025-0001" in cve_ids
    assert "CVE-2025-0002" in cve_ids
    assert "CVE-2025-0003" in cve_ids
    assert "CVE-2025-9999" not in cve_ids
