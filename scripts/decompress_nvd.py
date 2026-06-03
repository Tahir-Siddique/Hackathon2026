#!/usr/bin/env python3
"""Decompress CVE-YYYY.json.xz in data/ (FKIE NVD feed)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.paths import DATA_DIR, decompress_xz, find_nvd_cve_json


def main() -> None:
    xz = find_nvd_cve_json()
    if xz is None or xz.suffix != ".xz":
        candidates = list(DATA_DIR.glob("CVE-*.json.xz"))
        if not candidates:
            print("No CVE-*.json.xz found in data/")
            sys.exit(1)
        xz = candidates[0]

    print(f"Decompressing {xz.name} ...")
    out = decompress_xz(xz)
    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"Wrote {out} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
