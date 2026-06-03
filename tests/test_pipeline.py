"""Integration tests for full pipeline (fixture data only)."""

import csv
from pathlib import Path

import pytest

from src.export import OUTPUT_COLUMNS
from src.pipeline import run_pipeline


def test_pipeline_fixture_run(
    minimal_nvd_path,
    minimal_kev_path,
    minimal_epss_path,
    test_assets_path,
    tmp_path,
):
    csv_out = tmp_path / "prioritised.csv"
    brief_out = tmp_path / "brief.md"

    result = run_pipeline(
        test_assets_path,
        nvd_path=minimal_nvd_path,
        kev_path=minimal_kev_path,
        epss_path=minimal_epss_path,
        output_csv=csv_out,
        output_brief=brief_out,
        max_rows=50,
    )

    assert result["stats"]["mapped_count"] == 3
    assert result["stats"]["unmapped_count"] == 1
    assert result["stats"]["raw_match_count"] >= 3
    assert len(result["rows"]) >= 3

    # KEV CVE-2025-0001 must rank above non-KEV with higher EPSS on another CVE
    rows = result["rows"]
    kev_rows = [r for r in rows if r["kev"] == "yes"]
    non_kev = [r for r in rows if r["kev"] == "no"]
    assert kev_rows
    if non_kev:
        first_kev_idx = rows.index(kev_rows[0])
        first_non_kev_idx = rows.index(non_kev[0])
        assert first_kev_idx < first_non_kev_idx

    assert csv_out.exists()
    with open(csv_out, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == OUTPUT_COLUMNS
        data = list(reader)
        assert len(data) >= 3
        assert all(col in data[0] for col in OUTPUT_COLUMNS)

    assert brief_out.exists()
    assert "Executive Brief" in brief_out.read_text(encoding="utf-8")


@pytest.mark.integration
def test_pipeline_sample_asset_list(has_full_datasets, sample_asset_list_path, tmp_path):
    if not has_full_datasets:
        pytest.skip("Full datasets not in data/")
    if not sample_asset_list_path.exists():
        pytest.skip("sample_asset_list.txt missing")

    csv_out = tmp_path / "full_sample.csv"
    result = run_pipeline(
        sample_asset_list_path,
        output_csv=csv_out,
        max_rows=50,
    )

    assert result["stats"]["unmapped_count"] == 0
    assert result["stats"]["mapped_count"] >= 10
    assert result["stats"]["output_row_count"] == 50
    assert result["stats"]["kev_in_output"] >= 1

    with open(csv_out, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["kev"] == "yes" or float(rows[0]["epss"]) >= float(rows[-1]["epss"])
