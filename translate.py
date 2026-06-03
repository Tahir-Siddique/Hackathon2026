#!/usr/bin/env python3
"""CVE-to-My-Stack Translator — CLI entrypoint."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.export import print_table
from src.loaders import smoke_test
from src.paths import DATA_DIR, dataset_status, find_epss_csv, resolve_nvd_path
from src.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter and prioritise CVEs relevant to your software stack."
    )
    parser.add_argument(
        "asset_list",
        nargs="?",
        default=DATA_DIR / "sample_asset_list.txt",
        type=Path,
        help="Path to asset list (default: data/sample_asset_list.txt)",
    )
    parser.add_argument(
        "--nvd",
        type=Path,
        default=None,
        help="NVD CVE JSON or .xz (default: auto-detect)",
    )
    parser.add_argument(
        "--kev",
        type=Path,
        default=DATA_DIR / "known_exploited_vulnerabilities.json",
        help="CISA KEV catalogue JSON",
    )
    parser.add_argument(
        "--epss",
        type=Path,
        default=None,
        help="EPSS CSV path (default: newest in data/)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUTPUT_DIR / "prioritised_cves.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--brief",
        type=Path,
        default=None,
        nargs="?",
        const=OUTPUT_DIR / "executive_brief.md",
        help="Also write Markdown brief (default: output/executive_brief.md)",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=50,
        help="Maximum rows in output (default: 50)",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Only test data feed loading and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("CVE-to-My-Stack Translator\n")
    status = dataset_status()
    print("Dataset status:")
    for key in ("nvd", "kev", "epss"):
        print(f"  {key}: {status[key]}")
    if status["notes"] != "ok":
        print(f"  note: {status['notes']}")
    print()

    nvd_path = resolve_nvd_path(args.nvd) if args.nvd else resolve_nvd_path()
    epss_path = args.epss or find_epss_csv()

    if args.smoke:
        summary = smoke_test(nvd_path, args.kev, epss_path)
        for k, v in summary.items():
            print(f"  {k}: {v}")
        return 0

    if not args.asset_list.exists():
        print(f"Asset list not found: {args.asset_list}", file=sys.stderr)
        return 1

    print("Loading feeds and running pipeline...")
    result = run_pipeline(
        args.asset_list,
        nvd_path=nvd_path,
        kev_path=args.kev,
        epss_path=epss_path,
        output_csv=args.output,
        output_brief=args.brief,
        max_rows=args.max_rows,
    )

    stats = result["stats"]
    print(
        f"  KEV: {stats['kev_count']} | EPSS: {stats['epss_count']} | "
        f"NVD: {stats['nvd_count']}"
    )
    print(f"  Assets: {stats['asset_count']} | Mapped: {stats['mapped_count']}")

    for m in result["mapped"]:
        print(f"  OK  {m['user_label']} -> {m['cpe_key']} ({m['match_method']})")
    for u in result["unmapped"]:
        print(f"  ??  {u['user_label']} (no mapping)")

    if not result["mapped"]:
        print("\nNo assets mapped — check config/normalisation_map.json", file=sys.stderr)
        return 1

    print(f"\n  {stats['raw_match_count']} raw matches -> {stats['output_row_count']} in output")
    print(f"  KEV rows in output: {stats['kev_in_output']}")
    print(f"\nWrote CSV to {args.output}")
    if args.brief:
        print(f"Wrote brief to {args.brief}")

    print("\nTop prioritised CVEs:\n")
    print_table(result["rows"])

    if result["unmapped"]:
        n = len(result["unmapped"])
        print(f"\nWarning: {n} asset(s) could not be normalised (silent miss risk).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
