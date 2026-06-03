"""CLI smoke tests."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_translate_smoke_with_fixtures(tmp_path):
    """Run CLI against minimal fixtures (fast, no 200MB NVD)."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "translate.py"),
            str(ROOT / "tests" / "fixtures" / "test_assets.txt"),
            "--nvd",
            str(ROOT / "tests" / "fixtures" / "minimal_nvd.json"),
            "--kev",
            str(ROOT / "tests" / "fixtures" / "minimal_kev.json"),
            "--epss",
            str(ROOT / "tests" / "fixtures" / "minimal_epss.csv"),
            "-o",
            str(tmp_path / "out.csv"),
            "--max-rows",
            "10",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "out.csv").exists()
    assert "CVE-2025-0001" in (tmp_path / "out.csv").read_text(encoding="utf-8")


def test_translate_smoke_flag():
    if not any((ROOT / "data").glob("CVE-*.json")):
        pytest.skip("Full NVD not present")
    result = subprocess.run(
        [sys.executable, str(ROOT / "translate.py"), "--smoke"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0
    assert "nvd_count" in result.stdout or "KEV:" in result.stdout
