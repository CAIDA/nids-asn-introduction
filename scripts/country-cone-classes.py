"""Country breakdown of ASN cone classes.

Usage:
    uv run scripts/country-cone-classes.py --output tables/country-cone-classes.md \
        -O data/orgs.jsonl -C data/20260501.ppdc-ases.txt.bz2
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.utils import open_safe, CLASSES, classify, FILTER_MAP


def read_asn_cone(path: Path) -> dict[str, int]:
    asn_cone: dict[str, int] = {}
    print(f"Reading {path} ...", file=sys.stderr)
    with open_safe(path) as fh:
        """
        Parse data/20260501.ppdc-ases.txt.bz2
        Each non-comment line starts with an ASN followed by its cone members.
        Map each ASN to its cone size (number of tokens minus 1).
        """
    return asn_cone


def read_asn_country(path: Path) -> dict[str, str]:
    asn_country: dict[str, str] = {}
    print(f"Reading {path} ...", file=sys.stderr)
    with open_safe(path, encoding="utf-8") as fh:
        """
        Parse data/orgs.jsonl
        Each line is a JSON record with a "country" field and a "members" list of ASNs.
        Map each member ASN to its organization's country code.
        """
    return asn_country


def render_table(rows: list[tuple[str, ...]]) -> str:
    """
    Render a list of rows as a markdown table.
    Compute column widths from the widest cell in each column.
    Emit a header row, a separator row, then all data rows.
    """
    return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Country breakdown of ASN cone classes."
    )
    parser.add_argument(
        "-O", "--org",
        type=Path,
        default=Path("data/orgs.jsonl"),
        help="Path to orgs JSONL file (default: data/orgs.jsonl)",
    )
    parser.add_argument(
        "-C", "--cone",
        type=Path,
        default=Path("data/20260501.ppdc-ases.txt.bz2"),
        help="Path to PPDC cone bz2 file (default: data/20260501.ppdc-ases.txt.bz2)",
    )
    parser.add_argument(
        "-f", "--filter",
        choices=list(FILTER_MAP),
        default="hug",
        help="Class used to rank countries (default: hug → transit huge)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("tables/country-cone-classes.md"),
        help="Output markdown file path (default: tables/country-cone-classes.md)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    for p in (args.org, args.cone):
        if not p.exists():
            raise SystemExit(f"Input file not found: {p}")

    asn_cone = read_asn_cone(args.cone)
    asn_country = read_asn_country(args.org)

    """
    Count ASNs per (class, country) pair using classify() and asn_country lookup.
    Determine the top 4 countries by count in the selected filter class (or total).
    Build a markdown table with columns: class name, top-4 countries, other.
    Each cell shows the count and percentage of that class's total.
    """
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(table, encoding="utf-8")
    print(f"Wrote table to {args.output}", file=sys.stderr)
    print(table)


if __name__ == "__main__":
    main()
