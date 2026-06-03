"""Tests for CPE dictionary lookup (requires nvdcpe-2.0.zip)."""

from pathlib import Path

import pytest

from src.cpe_lookup import find_cpe_zip, parse_vendor_product, search_cpe_dictionary

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@pytest.mark.skipif(
    not (DATA_DIR / "nvdcpe-2.0.zip").exists(),
    reason="CPE dictionary zip not downloaded",
)
def test_search_microsoft_365():
    hits = search_cpe_dictionary("microsoft 365", max_results=5)
    assert hits
    assert any("microsoft" in h["cpe_name"].lower() for h in hits)


def test_parse_vendor_product():
    assert (
        parse_vendor_product("cpe:2.3:a:google:chrome:*:*:*:*:*:*:*:*")
        == "google:chrome"
    )


def test_find_cpe_zip_when_present():
    if (DATA_DIR / "nvdcpe-2.0.zip").exists():
        assert find_cpe_zip() is not None
