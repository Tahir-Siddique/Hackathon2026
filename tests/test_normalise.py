"""Tests for src/normalise.py."""

from pathlib import Path

import pytest

from src.loaders import parse_asset_list
from src.normalise import load_normalisation_map, normalise_assets

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_EXPECTED = {
    "Microsoft 365 Apps for Business Current": "microsoft:365_apps",
    "Windows Server 2022 21H2": "microsoft:windows_server_2022",
    "Windows 10 Pro 22H2": "microsoft:windows_10",
    "Adobe Acrobat Reader DC 2024.001": "adobe:acrobat_reader",
    "Cisco IOS XE 17.9": "cisco:ios_xe",
    "VMware vSphere 8.0": "vmware:vsphere",
    "Google Chrome Latest": "google:chrome",
    "OpenSSL 3.0.7": "openssl:openssl",
    "Apache HTTP Server 2.4.57": "apache:http_server",
    "Zoom 5.17": "zoom:zoom",
    "WordPress 6.4": "wordpress:wordpress",
    "Moodle 4.3": "moodle:moodle",
}


def test_normalisation_map_has_at_least_15_products():
    products = load_normalisation_map()
    assert len(products) >= 15


@pytest.mark.parametrize("user_label,cpe_key", list(SAMPLE_EXPECTED.items()))
def test_sample_asset_normalisation(user_label, cpe_key, sample_asset_list_path):
    if not sample_asset_list_path.exists():
        pytest.skip("sample_asset_list.txt not in data/")
    assets = parse_asset_list(sample_asset_list_path)
    asset = next(a for a in assets if a["user_label"] == user_label)
    mapped, unmapped = normalise_assets([asset])
    assert len(unmapped) == 0
    assert mapped[0]["cpe_key"] == cpe_key


def test_all_sample_assets_map(sample_asset_list_path):
    if not sample_asset_list_path.exists():
        pytest.skip("sample_asset_list.txt not in data/")
    assets = parse_asset_list(sample_asset_list_path)
    mapped, unmapped = normalise_assets(assets)
    assert len(unmapped) == 0
    assert len(mapped) >= 10


def test_unknown_product_unmapped(test_assets_path):
    assets = parse_asset_list(test_assets_path)
    unknown = [a for a in assets if "Unknown" in a["name"]][0]
    mapped, unmapped = normalise_assets([unknown])
    assert len(mapped) == 0
    assert len(unmapped) == 1
