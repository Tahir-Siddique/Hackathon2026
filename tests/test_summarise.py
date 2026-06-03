"""Tests for src/summarise.py."""

from src.summarise import add_summaries, build_risk_summary, epss_label


def test_epss_labels():
    assert epss_label(0.05) == "low"
    assert epss_label(0.15) == "moderate"
    assert epss_label(0.35) == "high"


def test_risk_summary_contains_kev_and_cve():
    row = {
        "cve_id": "CVE-2025-0001",
        "affected_asset": "Google Chrome Latest",
        "epss": 0.85,
        "kev": "yes",
    }
    text = build_risk_summary(row)
    assert "CVE-2025-0001" in text
    assert "Google Chrome" in text
    assert "KEV" in text
    assert "high" in text


def test_add_summaries():
    rows = [{"cve_id": "CVE-X", "affected_asset": "A", "epss": 0.0, "kev": "no"}]
    out = add_summaries(rows)
    assert "risk_summary" in out[0]
