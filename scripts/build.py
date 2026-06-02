#!/usr/bin/env python3
"""
build.py - one-command pipeline runner for the ASN introduction module.

Runs every step in dependency order:
  1. Download the as2org organization data (slow; skipped once data/orgs.jsonl exists)
  2. Generate tables/org-table-fields.md
  3. Generate tables/asn-customer-cone-classes.md
  4. Generate tables/country-cone-classes.md
  5. Compile answer.md + tables/* into the final report.md

A step is only re-run when its output is missing or OLDER than one of its
inputs (Make-style incremental build). This keeps iteration fast: fixing one
script regenerates only that table and then re-compiles the report.

Usage:
    uv run build.py            # build everything that is out of date
    uv run build.py --force    # rebuild everything from scratch
    uv run build.py --list     # show the pipeline steps and exit

The commands below are exactly the ones documented in the README; this script
runs them in the correct order through `uv run`.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --- Project layout (all paths are relative to this file) --------------------
ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data"
TABLES  = ROOT / "tables"
SCRIPTS = ROOT / "scripts"

ORGS   = DATA   / "orgs.jsonl"
PPDC   = DATA   / "20260501.ppdc-ases.txt.bz2"
ANSWER = ROOT   / "answer.md"
REPORT = ROOT   / "report.md"

# The customer-cone file is a MANUAL download (see README section 6.1). The
# runner checks for it and prints this URL if it is missing, but does not
# fetch it for you — downloading it is part of the assignment.
PPDC_URL = (
    "https://publicdata.caida.org/datasets/as-relationships/"
    "serial-1/20260501.ppdc-ases.txt.bz2"
)


@dataclass
class Step:
    """One pipeline stage: a command, the files it reads, the file it writes."""

    name:   str
    cmd:    list[str]           # passed to `uv run ...` (paths relative to ROOT)
    output: Path                # the file this step produces
    inputs: list[Path] = field(default_factory=list)  # files it depends on


def pipeline() -> list[Step]:
    """The full build, in dependency order."""
    return [
        # No data inputs: keyed only on its output, so a finished download is
        # never repeated (re-running the slow paginated API call wastes time).
        Step(
            name="download organizations (as2org API)",
            cmd=["scripts/orgs-download.py", "--output", "data/orgs.jsonl"],
            output=ORGS,
        ),
        Step(
            name="organization field table",
            cmd=["scripts/org-table-fields.py",
                 "--output", "tables/org-table-fields.md",
                 "data/orgs.jsonl"],
            inputs=[SCRIPTS / "org-table-fields.py", ORGS],
            output=TABLES / "org-table-fields.md",
        ),
        Step(
            name="customer-cone size classes",
            cmd=["scripts/asn-customer-cone-classes.py",
                 "--output", "tables/asn-customer-cone-classes.md",
                 "data/20260501.ppdc-ases.txt.bz2"],
            inputs=[SCRIPTS / "asn-customer-cone-classes.py", PPDC],
            output=TABLES / "asn-customer-cone-classes.md",
        ),
        Step(
            name="cone classes by country",
            cmd=["scripts/country-cone-classes.py",
                 "--output", "tables/country-cone-classes.md",
                 "-O", "data/orgs.jsonl",
                 "-C", "data/20260501.ppdc-ases.txt.bz2"],
            inputs=[SCRIPTS / "country-cone-classes.py", ORGS, PPDC],
            output=TABLES / "country-cone-classes.md",
        ),
        # Compile step: reads answer.md + all three tables, writes report.md.
        # Re-runs whenever you edit answer.md OR any table is regenerated.
        Step(
            name="compile final report",
            cmd=["scripts/compile-report.py", "--output", "report.md", "answer.md"],
            inputs=[
                SCRIPTS  / "compile-report.py",
                ANSWER,
                TABLES   / "org-table-fields.md",
                TABLES   / "asn-customer-cone-classes.md",
                TABLES   / "country-cone-classes.md",
            ],
            output=REPORT,
        ),
    ]


def missing_inputs(step: Step) -> list[Path]:
    """Inputs that do not exist yet (so the step cannot run)."""
    return [p for p in step.inputs if not p.exists()]


def is_stale(step: Step) -> bool:
    """True if the output must be (re)built."""
    if not step.output.exists():
        return True
    out_mtime = step.output.stat().st_mtime
    return any(src.stat().st_mtime > out_mtime for src in step.inputs)


def run_step(step: Step, force: bool) -> None:
    missing = missing_inputs(step)
    if missing:
        names = ", ".join(str(p.relative_to(ROOT)) for p in missing)
        print(f"  skipped:     {step.name}  (missing: {names})")
        if PPDC in missing:
            print(f"               download the customer-cone file into "
                  f"{DATA.relative_to(ROOT)}/ :")
            print(f"               {PPDC_URL}")
        return

    if not force and not is_stale(step):
        print(f"  up to date:  {step.name}")
        return

    print(f"  building:    {step.name}")
    # `uv run` executes the script inside the project's locked environment,
    # so dependencies resolved by `uv sync` are guaranteed to be present.
    result = subprocess.run(["uv", "run", *step.cmd], cwd=ROOT)
    if result.returncode != 0:
        sys.exit(f"\n  FAILED: {step.name} (exit code {result.returncode})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build all module tables and compile report.md.")
    parser.add_argument("--force", action="store_true",
                        help="rebuild every step, ignoring timestamps")
    parser.add_argument("--list", action="store_true",
                        help="print the pipeline steps and exit")
    args = parser.parse_args()

    steps = pipeline()

    if args.list:
        for s in steps:
            print(f"{s.name}\n    -> {s.output.relative_to(ROOT)}")
        return

    DATA.mkdir(exist_ok=True)
    TABLES.mkdir(exist_ok=True)

    for step in steps:
        run_step(step, args.force)

    if REPORT.exists():
        print(f"\nDone. Submit {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
