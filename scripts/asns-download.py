#!/usr/bin/env python3
"""Download all ASNs from the CAIDA AS Rank API and save them as JSONL.

Usage:
    uv run scripts/asns-download.py \
        -u https://api.asrank.caida.org/v2/restful/asns/ \
        -o data/asns.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import requests

DEFAULT_URL = "https://api.asrank.caida.org/v2/restful/asns/"
DEFAULT_PAGE_SIZE = 10000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download CAIDA AS Rank ASN records to a JSONL file."
    )
    parser.add_argument(
        "-u",
        "--url",
        default=DEFAULT_URL,
        help="AS Rank API endpoint to download from",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="data/asns.jsonl",
        help="Output JSONL file path",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=DEFAULT_PAGE_SIZE,
        help=f"Number of ASNs to request per page (default: {DEFAULT_PAGE_SIZE})",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Seconds to sleep between page requests (default: 0.1)",
    )
    return parser.parse_args()


def download_asns(url: str, output_path: Path, page_size: int, delay: float) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_written = 0
    page = 1
    offset = 0

    with requests.Session() as session, output_path.open("w", encoding="utf-8") as handle:
        while True:
            params = {"limit": page_size, "offset": offset}
            print(
                f"Downloading page {page} (offset={offset}, limit={page_size})...",
                file=sys.stderr,
            )
            try:
                response = session.get(url, params=params, timeout=60)
                response.raise_for_status()
                payload = response.json()
            except requests.RequestException as exc:
                raise SystemExit(f"Request failed on page {page}: {exc}") from exc
            except ValueError as exc:
                raise SystemExit(f"Invalid JSON response on page {page}: {exc}") from exc

            asns_data = payload.get("data", {}).get("asns", {})
            edges = asns_data.get("edges", [])
            page_info = asns_data.get("pageInfo") or {}
            total_count = asns_data.get("totalCount")

            if not isinstance(edges, list):
                raise SystemExit("Unexpected API response: data.asns.edges is not a list")

            if not edges:
                print(f"Page {page} returned 0 ASNs; stopping.", file=sys.stderr)
                break

            for edge in edges:
                node = edge.get("node")
                if node is None:
                    continue
                json.dump(node, handle, separators=(",", ":"))
                handle.write("\n")

            handle.flush()
            total_written += len(edges)

            total_suffix = f"/{total_count}" if total_count is not None else ""
            print(
                f"Downloaded page {page}: {len(edges)} ASNs "
                f"({total_written}{total_suffix} written)",
                file=sys.stderr,
            )

            if not page_info.get("hasNextPage"):
                break

            page += 1
            offset += len(edges)
            if delay > 0:
                time.sleep(delay)

    return total_written


def main() -> None:
    args = parse_args()

    if args.page_size <= 0:
        raise SystemExit("--page-size must be greater than 0")
    if args.delay < 0:
        raise SystemExit("--delay must be 0 or greater")

    output_path = Path(args.output)
    print(f"Saving ASN JSONL to {output_path}", file=sys.stderr)
    total = download_asns(args.url, output_path, args.page_size, args.delay)
    print(f"Saved {total} ASNs to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
