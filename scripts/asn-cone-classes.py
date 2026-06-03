"""Classify ASNs by customer cone size and emit a markdown table.

Usage:
    uv run scripts/asn-customer-cone-classes.py --output tables/asn-customer-cone-classes.md data/20260501.ppdc-ases.txt.bz2
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ------------------------------------------------
#
# We recommend using open_safe — it uses the file extension to determine
# how to open the file (plain text, bz2, gz, etc.):
#
#   with open_safe(path) as fh:
#       for line in fh:
#           line = line.strip()
#           if not line or line.startswith("#"):
#               continue
#
# ------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent))
from lib.utils import open_safe, CLASSES, FILTER_MAP

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

    table = None
    """
    TODO:
    1. Read data/20260501.ppdc-ases.txt.bz2 to build a dict {asn: cone_size}.
       Each non-comment line starts with an ASN followed by its cone members;
       the cone size is the number of tokens on the line minus 1.

    2. Use CLASSES from lib.utils to count how many ASNs fall into each class.

    3. Build Table 1 as a Markdown table:
       - Columns: class, range, number of ASNs, percentage
       - Rows: one per class in CLASSES order
       - percentage is the share of all ASNs (one decimal place)

    The output should look like:

    |          class | range        | number of ASNs |   percentage |
    | -------------: | ------------ | -------------: | -----------: |
    |           edge | 1            |          67090 |       84.24% |
    | ...
    """

    if table is None:
        raise SystemExit(replace_code_error_messsage)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(table, encoding="utf-8")
    print(f"Wrote table to {args.output}", file=sys.stderr)
    print(table)

replace_code_error_messsage = """
    -----------------------------------------------
    Please replace the TODO comments with your code
    -----------------------------------------------
    """

if __name__ == "__main__":
    main()
