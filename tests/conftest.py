"""Pytest fixtures — small files only (no full NVD load in unit tests)."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
DATA_DIR = ROOT / "data"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def minimal_kev_path(fixtures_dir: Path) -> Path:
    return fixtures_dir / "minimal_kev.json"


@pytest.fixture
def minimal_epss_path(fixtures_dir: Path) -> Path:
    return fixtures_dir / "minimal_epss.csv"


@pytest.fixture
def minimal_nvd_path(fixtures_dir: Path) -> Path:
    return fixtures_dir / "minimal_nvd.json"


@pytest.fixture
def test_assets_path(fixtures_dir: Path) -> Path:
    return fixtures_dir / "test_assets.txt"


@pytest.fixture
def sample_asset_list_path() -> Path:
    return DATA_DIR / "sample_asset_list.txt"


@pytest.fixture
def has_full_datasets() -> bool:
    return (
        (DATA_DIR / "CVE-2025.json").exists()
        and (DATA_DIR / "known_exploited_vulnerabilities.json").exists()
        and any(DATA_DIR.glob("epss_scores-*.csv"))
    )
