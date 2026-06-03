"""Tests for src/export.py."""

import csv
from pathlib import Path

from src.export import OUTPUT_COLUMNS, write_brief, write_csv


def test_write_csv_columns(tmp_path):
    rows = [
        {
            "cve_id": "CVE-2025-0001",
            "affected_asset": "Chrome",
            "criticality": "Critical",
            "cvss": 9.8,
            "epss": 0.85,
            "kev": "yes",
            "risk_summary": "Test summary.",
        }
    ]
    out = tmp_path / "out.csv"
    write_csv(rows, out)
    with open(out, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == OUTPUT_COLUMNS
        row = next(reader)
        assert row["cve_id"] == "CVE-2025-0001"
        assert row["kev"] == "yes"
        assert row["criticality"] == "Critical"


def test_write_brief(tmp_path):
    rows = [
        {
            "cve_id": "CVE-2025-0001",
            "affected_asset": "Chrome",
            "cvss": 9.8,
            "epss": 0.85,
            "kev": "yes",
            "risk_summary": "Summary line.",
        }
    ]
    mapped = [{"user_label": "Chrome", "cpe_key": "google:chrome"}]
    brief = tmp_path / "brief.md"
    write_brief(rows, mapped, [], brief)
    text = brief.read_text(encoding="utf-8")
    assert "Executive Brief" in text
    assert "CVE-2025-0001" in text
    assert "google:chrome" in text
