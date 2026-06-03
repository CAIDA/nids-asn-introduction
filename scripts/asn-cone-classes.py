"""Classify ASNs by customer cone size and emit a markdown table.

Usage:
    uv run scripts/asn-customer-cone-classes.py --output tables/asn-customer-cone-classes.md data/20260501.ppdc-ases.txt.bz2
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.utils import open_safe, CLASSES, FILTER_MAP

def read_cone_sizes(path: Path) -> list[int]:
    sizes: list[int] = []
    print(f"Reading {path} ...", file=sys.stderr)
    with open_safe(path) as fh:
        """
        Parse  data/20260501.ppdc-ases.txt.bz2
        """
    return sizes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify ASNs by customer cone size and emit a markdown table."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=Path("data/20260501.ppdc-ases.txt.bz2"),
        help="Path to PPDC cone file (default: data/20260501.ppdc-ases.txt.bz2)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("tables/asn-customer-cone-classes.md"),
        help="Output markdown file path (default: tables/asn-customer-cone-classes.md)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input file not found: {args.input}")

    sizes = read_cone_sizes(args.input)
    total = len(sizes)
    maximum = max(sizes)

    """
    Create the markdown table with columns: class, range, number of ASNs, percentage
    The class column is based on CLASSES, which defines the size ranges for each class.
    The range column shows the size range for each class.
    The number of ASNs column shows how many ASNs fall into each class.
    The percentage column shows the percentage of ASNs that fall into each class.
    """    
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(table, encoding="utf-8")
    print(f"Wrote table to {args.output}", file=sys.stderr)
    print(table)


if __name__ == "__main__":
    main()
