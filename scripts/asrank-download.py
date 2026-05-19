#!/usr/bin/env python3
"""Download all ASNs from the CAIDA AS Rank API and save to CSV.

Downloads the complete global AS Rank dataset. Filter by country locally
using the country_iso column (ISO 3166-1 alpha-2 codes, e.g. US, CN, DE).

Usage:
    # Download all ASNs (full dataset, ~120k rows)
    uv run scripts/asrank-download.py --output data/asns.csv

    # Download a small sample for testing
    uv run scripts/asrank-download.py --output data/asns.csv --limit 500

Output columns:
    asn              AS number
    name             AS name
    rank             Global rank by customer cone size (1 = largest)
    country_iso      ISO 3166-1 alpha-2 country code (headquarters)
    cone_asns        Number of ASNs in the customer cone
    cone_prefixes    Number of IP prefixes in the customer cone
    cone_addresses   Number of IP addresses in the customer cone
    degree_customer  Number of direct customer ASNs
    degree_peer      Number of peer ASNs
    degree_provider  Number of provider ASNs

API documentation: https://api.asrank.caida.org/v2/restful/doc
"""

import argparse
import csv
import sys
import time

import requests

BASE_URL = "https://api.asrank.caida.org/v2/restful/asns/"
PAGE_SIZE = 1000


def fetch_asns(max_rows=None):
    rows = []
    offset = 0
    page = 1

    while True:
        params = {"limit": PAGE_SIZE, "offset": offset}
        print(f"  fetching page {page} (offset={offset}) ...", file=sys.stderr)
        response = requests.get(BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        edges = data["data"]["asns"]["edges"]
        if not edges:
            break

        for edge in edges:
            node = edge["node"]
            cone = node.get("cone") or {}
            degree = node.get("asnDegree") or {}
            country = node.get("country") or {}
            rows.append({
                "asn": node["asn"],
                "name": node.get("asnName", ""),
                "rank": node.get("rank", ""),
                "country_iso": country.get("iso", ""),
                "cone_asns": cone.get("numberAsns", ""),
                "cone_prefixes": cone.get("numberPrefixes", ""),
                "cone_addresses": cone.get("numberAddresses", ""),
                "degree_customer": degree.get("customer", ""),
                "degree_peer": degree.get("peer", ""),
                "degree_provider": degree.get("provider", ""),
            })

        has_next = data["data"]["asns"]["pageInfo"]["hasNextPage"]
        if not has_next:
            break
        if max_rows and len(rows) >= max_rows:
            rows = rows[:max_rows]
            break

        offset += PAGE_SIZE
        page += 1
        time.sleep(0.1)

    total = data["data"]["asns"]["totalCount"]
    print(f"  downloaded {len(rows)} ASNs (API reports {total} total)", file=sys.stderr)
    return rows


FIELDNAMES = [
    "asn", "name", "rank", "country_iso",
    "cone_asns", "cone_prefixes", "cone_addresses",
    "degree_customer", "degree_peer", "degree_provider",
]


def main():
    parser = argparse.ArgumentParser(description="Download CAIDA AS Rank data to CSV.")
    parser.add_argument("--output", default="data/asns.csv", help="Output CSV file path")
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum number of ASNs to download (default: all)")
    args = parser.parse_args()

    print(f"Downloading AS Rank data...", file=sys.stderr)
    rows = fetch_asns(max_rows=args.limit)

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} ASNs to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
