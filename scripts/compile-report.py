#!/usr/bin/env python3
"""
compile-report.py  (provided — do not modify)

Reads answer.md, replaces every {{INSERT:path}} placeholder with the contents
of the referenced table file, and writes the finished report.md.

This script is called automatically by build.py as the final pipeline step.
You do not need to run it by hand, but you can:

    uv run scripts/compile-report.py --output report.md answer.md

If a placeholder references a table that does not exist yet, the script will
tell you which step to run first.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# All INSERT paths are resolved from the project root (the parent of scripts/).
ROOT = Path(__file__).resolve().parent.parent

# Pattern: {{INSERT:tables/some-table.md}}
_PLACEHOLDER = re.compile(r"\{\{INSERT:(.*?)\}\}")


def replace_placeholders(source: str) -> str:
    """Return source with every {{INSERT:path}} replaced by file contents."""

    def _sub(match: re.Match) -> str:
        rel = match.group(1)
        table_path = ROOT / rel
        if not table_path.exists():
            sys.exit(
                f"compile-report: missing table file '{rel}'\n"
                f"  Run `uv run build.py` to generate it before compiling the report."
            )
        return table_path.read_text(encoding="utf-8").strip()

    return _PLACEHOLDER.sub(_sub, source)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fill table placeholders in answer.md and write report.md."
    )
    parser.add_argument("source", help="path to answer.md")
    parser.add_argument("--output", required=True, help="path to write report.md")
    args = parser.parse_args()

    source_path = Path(args.source)
    if not source_path.exists():
        sys.exit(f"compile-report: source file not found: {args.source}")

    text = source_path.read_text(encoding="utf-8")
    result = replace_placeholders(text)

    output_path = Path(args.output).resolve()
    output_path.write_text(result, encoding="utf-8")
    print(f"  compiled:    {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
