#!/usr/bin/env python3
"""Download organization records from the CAIDA AS2org API and save as JSONL.

Usage:
    uv run scripts/orgs-download.py \
        --url https://api.data.caida.org/as2org/v1/orgs/ \
        --output data/orgs.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import requests

DEFAULT_URL = "https://api.data.caida.org/as2org/v1/orgs/"
DEFAULT_PAGE_SIZE = 5000
MAX_PAGE_SIZE = 5000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download CAIDA AS2org organization records to a JSONL file."
    )
    parser.add_argument(
        "-u",
        "--url",
        default=DEFAULT_URL,
        help="AS2org orgs API endpoint to download from",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="data/orgs.jsonl",
        help="Output JSONL file path",
    )
    parser.add_argument(
        "--page-size",
        "--first",
        dest="page_size",
        type=int,
        default=DEFAULT_PAGE_SIZE,
        help=(
            "Number of orgs to request per page "
            f"(default: {DEFAULT_PAGE_SIZE}, max: {MAX_PAGE_SIZE})"
        ),
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Starting offset for paginated downloads (default: 0)",
    )
    parser.add_argument(
        "--sort",
        help="Optional API sort value, such as score or id",
    )
    parser.add_argument(
        "--date-start",
        help="Optional dateStart filter passed through to the API",
    )
    parser.add_argument(
        "--date-end",
        help="Optional dateEnd filter passed through to the API",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Pass verbose=true to the API",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Seconds to sleep between page requests (default: 0.1)",
    )
    return parser.parse_args()


def download_orgs(
    url: str,
    output_path: Path,
    page_size: int,
    start_offset: int,
    delay: float,
    sort: str | None,
    date_start: str | None,
    date_end: str | None,
    verbose: bool,
) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_written = 0
    page = 1
    offset = start_offset

    with requests.Session() as session, output_path.open("w", encoding="utf-8") as handle:
        while True:
            params: dict[str, str | int | bool] = {"first": page_size, "offset": offset}
            if sort:
                params["sort"] = sort
            if date_start:
                params["dateStart"] = date_start
            if date_end:
                params["dateEnd"] = date_end
            if verbose:
                params["verbose"] = True

            print(
                f"Downloading page {page} (offset={offset}, first={page_size})...",
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

            errors = payload.get("errors")
            if errors:
                raise SystemExit(f"API returned errors on page {page}: {errors}")

            records = payload.get("data", [])
            page_info = payload.get("pageInfo") or {}
            total_count = payload.get("totalCount")

            if not isinstance(records, list):
                raise SystemExit("Unexpected API response: data is not a list")

            if not records:
                print(f"Page {page} returned 0 orgs; stopping.", file=sys.stderr)
                break

            for record in records:
                json.dump(record, handle, separators=(",", ":"))
                handle.write("\n")

            handle.flush()
            total_written += len(records)

            total_suffix = f"/{total_count}" if total_count is not None else ""
            print(
                f"Downloaded page {page}: {len(records)} orgs "
                f"({total_written}{total_suffix} written)",
                file=sys.stderr,
            )

            if not page_info.get("hasNextPage"):
                break

            page += 1
            offset += len(records)
            if delay > 0:
                time.sleep(delay)

    return total_written


def main() -> None:
    args = parse_args()

    if args.page_size <= 0:
        raise SystemExit("--page-size must be greater than 0")
    if args.page_size > MAX_PAGE_SIZE:
        raise SystemExit(f"--page-size must be less than or equal to {MAX_PAGE_SIZE}")
    if args.offset < 0:
        raise SystemExit("--offset must be 0 or greater")
    if args.delay < 0:
        raise SystemExit("--delay must be 0 or greater")

    output_path = Path(args.output)
    print(f"Saving org JSONL to {output_path}", file=sys.stderr)
    total = download_orgs(
        args.url,
        output_path,
        args.page_size,
        args.offset,
        args.delay,
        args.sort,
        args.date_start,
        args.date_end,
        args.verbose,
    )
    print(f"Saved {total} orgs to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
