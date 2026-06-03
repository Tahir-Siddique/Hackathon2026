"""Steps 7–8: Enrich matches with EPSS/KEV and rank."""

from __future__ import annotations

from typing import Any


def vulnerability_criticality(cvss: float, epss: float, kev: bool) -> str:
    """
    Plain-language severity for the output table.

    Uses CVSS bands, elevated when CISA KEV or high EPSS indicate active/high-likelihood
    exploitation (so a moderate CVSS + KEV row is not labelled only "Medium").
    """
    if (
        cvss >= 9.0
        or (kev and epss >= 0.5)
        or (kev and cvss >= 7.0)
        or (kev and epss >= 0.3)
    ):
        return "Critical"
    if kev or cvss >= 7.0 or epss >= 0.5:
        return "High"
    if cvss >= 4.0 or epss >= 0.15:
        return "Medium"
    if cvss > 0 or epss > 0:
        return "Low"
    return "Unknown"


def combined_urgency_score(cvss: float, epss: float, kev: bool) -> float:
    """
    Single urgency rank: weighted CVSS + EPSS, boosted when in KEV.
    KEV sort still takes precedence in enrich_and_rank; this aids comparison.
    """
    base = 0.4 * (cvss / 10.0) + 0.6 * epss
    return min(1.0, base + (0.25 if kev else 0.0))


def enrich_and_rank(
    matches: list[dict[str, Any]],
    epss_by_cve: dict[str, dict[str, float]],
    kev_ids: set[str],
    max_rows: int | None = 50,
) -> list[dict[str, Any]]:
    """Add EPSS/KEV fields, dedupe by CVE+asset, sort, and cap rows."""
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for m in matches:
        cve_id = m["cve_id"].upper()
        asset = m["affected_asset"]
        dedupe_key = (cve_id, asset)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        epss_data = epss_by_cve.get(cve_id, {})
        epss = epss_data.get("epss", 0.0)
        kev = cve_id in kev_ids

        cvss = m.get("cvss", 0.0)
        rows.append(
            {
                "cve_id": cve_id,
                "affected_asset": asset,
                "criticality": vulnerability_criticality(cvss, epss, kev),
                "cvss": cvss,
                "epss": epss,
                "epss_percentile": epss_data.get("percentile", 0.0),
                "kev": "yes" if kev else "no",
                "kev_bool": kev,
                "urgency_score": combined_urgency_score(cvss, epss, kev),
                "description": m.get("description", ""),
            }
        )

    rows.sort(
        key=lambda r: (r["kev_bool"], r["urgency_score"], r["epss"], r["cvss"]),
        reverse=True,
    )

    if max_rows is not None and len(rows) > max_rows:
        rows = rows[:max_rows]
    return rows
