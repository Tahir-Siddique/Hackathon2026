"""Tests for src/loaders.py."""

from src.loaders import load_epss, load_kev, load_nvd, parse_asset_list, smoke_test


def test_load_kev(minimal_kev_path):
    ids = load_kev(minimal_kev_path)
    assert ids == {"CVE-2025-0001", "CVE-2025-0002"}


def test_load_epss(minimal_epss_path):
    epss = load_epss(minimal_epss_path)
    assert epss["CVE-2025-0001"]["epss"] == 0.85
    assert epss["CVE-2025-0001"]["percentile"] == 0.99


def test_load_nvd(minimal_nvd_path):
    items = load_nvd(minimal_nvd_path)
    assert len(items) == 4
    assert items[0]["id"] == "CVE-2025-0001"


def test_parse_asset_list(test_assets_path):
    assets = parse_asset_list(test_assets_path)
    assert len(assets) == 4
    assert assets[0]["name"] == "Google Chrome"
    assert assets[0]["version"] == "Latest"


def test_smoke_test(minimal_kev_path, minimal_epss_path, minimal_nvd_path):
    summary = smoke_test(minimal_nvd_path, minimal_kev_path, minimal_epss_path)
    assert summary["kev_count"] == 2
    assert summary["epss_count"] == 4
    assert summary["nvd_count"] == 4
