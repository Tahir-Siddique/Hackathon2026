"""Step 9: Plain-English risk summaries."""

from __future__ import annotations

from typing import Any


def epss_label(epss: float) -> str:
    if epss >= 0.30:
        return "high"
    if epss >= 0.10:
        return "moderate"
    return "low"


def build_risk_summary(row: dict[str, Any]) -> str:
    label = epss_label(row.get("epss", 0.0))
    kev_text = (
        "Actively exploited in the wild (CISA KEV)."
        if row.get("kev") == "yes"
        else "Not listed in CISA KEV."
    )
    return (
        f"{row['cve_id']} affects {row['affected_asset']}. "
        f"EPSS {row.get('epss', 0):.4f} indicates {label} exploitation probability. "
        f"{kev_text}"
    )


def add_summaries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["risk_summary"] = build_risk_summary(row)
    return rows
