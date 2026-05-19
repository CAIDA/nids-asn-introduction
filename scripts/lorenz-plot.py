#!/usr/bin/env python3
"""Plot a Lorenz curve for one or more CSV files and print Gini coefficients.

Each CSV file must have a column of numeric values representing the "wealth"
to be distributed (e.g. GDP, cone size, number of addresses).

Usage:
    # Single file
    uv run scripts/lorenz-plot.py data/gdp.csv --value gdp_usd --label "World GDP"

    # Multiple files on one chart
    uv run scripts/lorenz-plot.py data/asns_us.csv data/asns_cn.csv \\
        --value cone_addresses \\
        --labels "US ASNs" "CN ASNs" \\
        --output lorenz_comparison.png

Options:
    --value     Column name to use as the value (default: value)
    --labels    Legend label for each input file (default: file basename)
    --output    Save the plot to this path instead of displaying it
    --title     Chart title
"""

import argparse
import csv
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


def load_values(path, column):
    values = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if column not in reader.fieldnames:
            print(
                f"Error: column '{column}' not found in {path}. "
                f"Available columns: {reader.fieldnames}",
                file=sys.stderr,
            )
            sys.exit(1)
        for row in reader:
            raw = row[column].strip()
            if raw == "" or raw.lower() == "none":
                continue
            try:
                values.append(float(raw))
            except ValueError:
                continue
    return values


def lorenz_curve(values):
    arr = np.array(values, dtype=float)
    arr = arr[arr > 0]
    arr = np.sort(arr)
    n = len(arr)
    cumulative = np.cumsum(arr)
    x = np.linspace(0, 1, n + 1)
    y = np.concatenate([[0], cumulative / cumulative[-1]])
    return x, y


def gini(values):
    arr = np.array(values, dtype=float)
    arr = arr[arr > 0]
    arr = np.sort(arr)
    n = len(arr)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * arr) / (n * arr.sum())) - (n + 1) / n


def main():
    parser = argparse.ArgumentParser(description="Plot Lorenz curves from CSV files.")
    parser.add_argument("files", nargs="+", help="CSV files to plot")
    parser.add_argument("--value", default="value", help="Column name for the values")
    parser.add_argument("--labels", nargs="*", help="Legend labels (one per file)")
    parser.add_argument("--output", help="Save plot to this path (default: display)")
    parser.add_argument("--title", default="Lorenz Curve", help="Chart title")
    args = parser.parse_args()

    labels = args.labels or []
    while len(labels) < len(args.files):
        labels.append(os.path.basename(args.files[len(labels)]))

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Perfect equality")

    for path, label in zip(args.files, labels):
        values = load_values(path, args.value)
        if not values:
            print(f"Warning: no valid values found in {path}", file=sys.stderr)
            continue
        x, y = lorenz_curve(values)
        g = gini(values)
        print(f"{label}: n={len(values):,}  Gini={g:.4f}")
        ax.plot(x, y, linewidth=2, label=f"{label}  (Gini = {g:.3f})")

    ax.set_xlabel("Cumulative fraction of units (sorted ascending)")
    ax.set_ylabel("Cumulative fraction of total value")
    ax.set_title(args.title)
    ax.legend(loc="upper left")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout()

    if args.output:
        plt.savefig(args.output, dpi=150)
        print(f"Saved plot to {args.output}", file=sys.stderr)
    else:
        plt.show()


if __name__ == "__main__":
    main()
