"""End-to-end pipeline orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.export import write_brief, write_csv
from src.loaders import load_epss, load_kev, load_nvd, parse_asset_list
from src.match import match_cves_to_assets
from src.normalise import normalise_assets
from src.rank import enrich_and_rank
from src.summarise import add_summaries


def run_pipeline(
    asset_list_path: Path,
    *,
    nvd_path: Path | None = None,
    kev_path: Path | None = None,
    epss_path: Path | None = None,
    norm_map_path: Path | None = None,
    output_csv: Path | None = None,
    output_brief: Path | None = None,
    max_rows: int | None = 50,
) -> dict[str, Any]:
    """
    Run full CVE-to-stack translation.

    Returns dict with rows, mapped, unmapped, and stats.
    """
    kev_ids = load_kev(kev_path)
    epss_by_cve = load_epss(epss_path)
    nvd_items = load_nvd(nvd_path)

    assets = parse_asset_list(asset_list_path)
    mapped, unmapped = normalise_assets(assets, map_path=norm_map_path)

    if not mapped:
        return {
            "rows": [],
            "mapped": [],
            "unmapped": unmapped,
            "stats": {
                "kev_count": len(kev_ids),
                "epss_count": len(epss_by_cve),
                "nvd_count": len(nvd_items),
                "asset_count": len(assets),
                "raw_match_count": 0,
            },
        }

    raw_matches = match_cves_to_assets(nvd_items, mapped)
    rows = enrich_and_rank(raw_matches, epss_by_cve, kev_ids, max_rows=max_rows)
    rows = add_summaries(rows)

    if output_csv:
        write_csv(rows, output_csv)
    if output_brief:
        write_brief(rows, mapped, unmapped, output_brief)

    kev_in_output = sum(1 for r in rows if r.get("kev") == "yes")

    return {
        "rows": rows,
        "mapped": mapped,
        "unmapped": unmapped,
        "stats": {
            "kev_count": len(kev_ids),
            "epss_count": len(epss_by_cve),
            "nvd_count": len(nvd_items),
            "asset_count": len(assets),
            "mapped_count": len(mapped),
            "unmapped_count": len(unmapped),
            "raw_match_count": len(raw_matches),
            "output_row_count": len(rows),
            "kev_in_output": kev_in_output,
        },
    }
