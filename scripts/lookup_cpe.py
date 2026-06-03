#!/usr/bin/env python3
"""Spot-check a product name against the NVD CPE Dictionary 2.0 zip."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cpe_lookup import parse_vendor_product, search_cpe_dictionary


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/lookup_cpe.py <search term>")
        print("Example: python scripts/lookup_cpe.py \"microsoft 365\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Searching CPE dictionary for: {query!r}\n")
    try:
        hits = search_cpe_dictionary(query)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    if not hits:
        print("No matches.")
        sys.exit(0)

    for i, hit in enumerate(hits, 1):
        vp = parse_vendor_product(hit["cpe_name"])
        print(f"{i}. {hit['title']}")
        print(f"   cpe: {hit['cpe_name']}")
        if vp:
            print(f"   vendor:product -> {vp}")
        print()


if __name__ == "__main__":
    main()
