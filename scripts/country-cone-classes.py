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
from lib.utils import open_safe, CLASSES, classify, FILTER_MAP


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

    table = None
    """
    TODO:
    Use the classification from Task 2 (CLASSES and classify() from lib.utils).

    1. Read data/20260501.ppdc-ases.txt.bz2 to build a dict {asn: cone_size}.
       Each non-comment line starts with an ASN followed by its cone members;
       the cone size is the number of tokens on the line minus 1.

    2. Read data/orgs.jsonl to build a dict {asn: country_code}.
       Each line is a JSON record with a "country" field and a "members" list of ASNs.

    3. Use classify() on each ASN's cone size to assign it a class name.
       Count ASNs per (class, country) pair.

    4. Find the top 4 countries by total number of ASNs across all classes.
       Map all remaining countries to "other".

    5. Build Table 2 as a Markdown table:
       - Columns: class name, top-4 country codes (e.g. US, CN), "other"
       - Rows: one per class in CLASSES order
       - Each cell shows: [total] ([%]) where [%] is the percentage of that
         class's total (one decimal place)

    The output should look like:

    | name           | US            | CN            | ...  | other         |
    | -------------- | ------------- | ------------- | ---- | ------------- |
    | edge           | 1234 (12.3%)  | 567 (5.7%)    | ...  | 4321 (43.2%)  |
    | transit small  | ...           | ...           | ...  | ...           |
    ...
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
