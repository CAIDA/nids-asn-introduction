"""Shared utilities for scripts."""

from __future__ import annotations

import bz2
import gzip
import io
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO


@contextmanager
def open_safe(filename: str | Path, encoding: str = "utf-8") -> Iterator[TextIO]:
    """Open a file for reading, transparently handling .gz, .bz2, and .zip compression."""
    path = Path(filename)
    suffix = path.suffix.lower()
    if suffix == ".gz":
        with gzip.open(path, "rt", encoding=encoding) as f:
            yield f
    elif suffix == ".bz2":
        with bz2.open(path, "rt", encoding=encoding) as f:
            yield f
    elif suffix == ".zip":
        with zipfile.ZipFile(path) as zf:
            with zf.open(zf.namelist()[0]) as raw:
                yield io.TextIOWrapper(raw, encoding=encoding)
    else:
        with path.open(encoding=encoding) as f:
            yield f


CLASSES: list[tuple[str, int, int]] = [
    ("stub",           1,     1),
    ("transit small",  2,     10),
    ("transit middle", 11,    1000),
    ("transit large",  1001,  10000),
    ("transit huge",   10001, -1),
]


FILTER_MAP: dict[str, str | None] = {
    "hug":    "transit huge",
    "large":  "transit large",
    "middle": "transit middle",
    "small":  "transit small",
    "sub":    "stub",
    "total":  None,
}


def classify(size: int) -> str:
    for label, lo, hi in CLASSES:
        if lo <= size and (hi == -1 or size <= hi):
            return label
    return "unknown"
