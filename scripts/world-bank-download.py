#!/usr/bin/env python3
"""Download the most recent GDP (current USD) for every country from the World Bank API.

Outputs a CSV with columns: country_code, country_name, year, gdp_usd

Usage:
    uv run scripts/world-bank-download.py --output data/gdp.csv

API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581
Interactive explorer: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
"""

import argparse
import csv
import sys

import requests

BASE_URL = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD"

AGGREGATE_CODES = {
    "1A", "1W", "4E", "7E", "8S", "B8", "F1", "OE", "S1", "S2", "S3",
    "S4", "T2", "T3", "T4", "T6", "T7", "V1", "V2", "V3", "V4", "XC",
    "XD", "XE", "XF", "XG", "XH", "XI", "XJ", "XL", "XM", "XN", "XO",
    "XP", "XQ", "XT", "XU", "XY", "Z4", "Z7", "ZB", "ZF", "ZG", "ZH",
    "ZI", "ZJ", "ZQ", "ZT",
}


def fetch_gdp():
    params = {
        "format": "json",
        "per_page": 20000,
        "date": "2020:2025",
    }

    print("Fetching GDP data from World Bank API...", file=sys.stderr)
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if len(data) < 2:
        print("Unexpected API response structure.", file=sys.stderr)
        sys.exit(1)

    records = data[1]

    seen = {}
    for r in records:
        if r["value"] is None:
            continue
        code = r["country"]["id"]
        if len(code) != 2 or code in AGGREGATE_CODES:
            continue
        year = int(r["date"])
        if code not in seen or year > seen[code]["year"]:
            seen[code] = {
                "country_code": code,
                "country_name": r["country"]["value"],
                "year": year,
                "gdp_usd": r["value"],
            }

    return sorted(seen.values(), key=lambda x: x["country_code"])


def main():
    parser = argparse.ArgumentParser(description="Download World Bank GDP data to CSV.")
    parser.add_argument("--output", default="data/gdp.csv", help="Output CSV file path")
    args = parser.parse_args()

    rows = fetch_gdp()

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["country_code", "country_name", "year", "gdp_usd"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} countries to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
