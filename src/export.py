"""Step 10: CSV and console export."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from tabulate import tabulate

OUTPUT_COLUMNS = [
    "cve_id",
    "affected_asset",
    "criticality",
    "cvss",
    "epss",
    "kev",
    "risk_summary",
]


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in OUTPUT_COLUMNS})


def print_table(rows: list[dict[str, Any]], limit: int = 15) -> None:
    if not rows:
        print("No matching CVEs found.")
        return
    display = [
        {
            "CVE": r["cve_id"],
            "Asset": (r["affected_asset"][:28] + "…")
            if len(r["affected_asset"]) > 29
            else r["affected_asset"],
            "Criticality": r.get("criticality", "Unknown"),
            "CVSS": f"{r.get('cvss', 0):.1f}",
            "EPSS": f"{r.get('epss', 0):.4f}",
            "KEV": r.get("kev", "no"),
        }
        for r in rows[:limit]
    ]
    print(tabulate(display, headers="keys", tablefmt="simple"))
    if len(rows) > limit:
        print(f"... and {len(rows) - limit} more rows in CSV.")


def write_brief(
    rows: list[dict[str, Any]],
    mapped: list[dict[str, Any]],
    unmapped: list[dict[str, str]],
    path: Path,
) -> None:
    """Write a one-page Markdown executive brief."""
    path.parent.mkdir(parents=True, exist_ok=True)
    kev_rows = [r for r in rows if r.get("kev") == "yes"]
    top = rows[:10]

    lines = [
        "# CVE-to-My-Stack — Executive Brief",
        "",
        "## Summary",
        f"- **Assets mapped:** {len(mapped)}",
        f"- **Assets unmapped:** {len(unmapped)}",
        f"- **Prioritised CVEs shown:** {len(rows)}",
        f"- **KEV (actively exploited) in list:** {len(kev_rows)}",
        "",
        "## Mapped stack",
        "",
    ]
    for m in mapped:
        lines.append(f"- {m['user_label']} → `{m['cpe_key']}`")
    if unmapped:
        lines.extend(["", "## Unmapped (review manually)", ""])
        for u in unmapped:
            lines.append(f"- {u['user_label']}")
    lines.extend(["", "## Top priorities", ""])
    for i, r in enumerate(top, 1):
        lines.append(
            f"{i}. **{r['cve_id']}** — {r['affected_asset']} "
            f"({r.get('criticality', 'Unknown')} · CVSS {r.get('cvss', 0):.1f}, "
            f"EPSS {r.get('epss', 0):.4f}, KEV {r.get('kev', 'no')})"
        )
        lines.append(f"   - {r.get('risk_summary', '')}")
    lines.extend(
        [
            "",
            "## Limitations",
            "- Wrong product mapping → CVE may be missing silently.",
            "- EPSS is predictive, not proof of safety.",
            "- Not in KEV ≠ unexploited.",
            "- Version ranges are not matched in this MVP.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
