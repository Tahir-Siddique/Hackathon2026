"""Tests for src/rank.py."""

from src.rank import combined_urgency_score, enrich_and_rank, vulnerability_criticality


def test_criticality_kev_elevates_moderate_cvss():
    assert vulnerability_criticality(4.3, 0.57, kev=True) == "Critical"


def test_criticality_cvss_only_high():
    assert vulnerability_criticality(8.0, 0.01, kev=False) == "High"


def test_criticality_low_scores():
    assert vulnerability_criticality(2.0, 0.01, kev=False) == "Low"


def test_enrich_includes_criticality():
    matches = [
        {"cve_id": "CVE-A", "affected_asset": "Chrome", "cvss": 4.3, "description": ""},
    ]
    epss = {"CVE-A": {"epss": 0.57, "percentile": 0.9}}
    rows = enrich_and_rank(matches, epss, {"CVE-A"}, max_rows=None)
    assert rows[0]["criticality"] == "Critical"


def test_combined_urgency_kev_boost():
    assert combined_urgency_score(10.0, 0.5, kev=True) > combined_urgency_score(
        10.0, 0.5, kev=False
    )


def test_kev_sorted_above_higher_epss_non_kev():
    matches = [
        {"cve_id": "CVE-A", "affected_asset": "Chrome", "cvss": 9.0, "description": ""},
        {"cve_id": "CVE-B", "affected_asset": "Chrome", "cvss": 5.0, "description": ""},
    ]
    epss = {"CVE-A": {"epss": 0.01, "percentile": 0.1}, "CVE-B": {"epss": 0.99, "percentile": 0.99}}
    kev_ids = {"CVE-A"}
    rows = enrich_and_rank(matches, epss, kev_ids, max_rows=None)
    assert rows[0]["cve_id"] == "CVE-A"
    assert rows[0]["kev"] == "yes"
    assert rows[1]["kev"] == "no"


def test_dedupe_by_cve_and_asset():
    matches = [
        {"cve_id": "CVE-A", "affected_asset": "A", "cvss": 1.0, "description": ""},
        {"cve_id": "CVE-A", "affected_asset": "A", "cvss": 1.0, "description": ""},
    ]
    rows = enrich_and_rank(matches, {}, set(), max_rows=None)
    assert len(rows) == 1


def test_max_rows_cap():
    matches = [
        {"cve_id": f"CVE-{i}", "affected_asset": "X", "cvss": float(i), "description": ""}
        for i in range(10)
    ]
    rows = enrich_and_rank(matches, {}, set(), max_rows=3)
    assert len(rows) == 3
