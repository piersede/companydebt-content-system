"""Normalise an Ahrefs 'all issues' CSV export into queryable records.

Ahrefs exports UTF-16-LE, tab-separated, every field double-quoted, with
embedded newlines inside quoted fields (redirect chains especially). Feeding
these to a naive line-based reader silently truncates rows, so everything goes
through csv.reader with the right dialect.
"""
from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

# Redirect-chain fields pack several URLs into one cell separated by newlines.
csv.field_size_limit(10_000_000)


def read_export(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        text = raw.decode("utf-16")
    else:
        text = raw.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text), delimiter="\t", quotechar='"')
    rows = list(reader)
    if not rows:
        return []
    header = [h.strip() for h in rows[0]]
    out = []
    for row in rows[1:]:
        if not any(cell.strip() for cell in row):
            continue
        row = row + [""] * (len(header) - len(row))
        out.append(dict(zip(header, row)))
    return out


def issue_name(path: Path) -> str:
    """'Warning-indexable-Page_has_links_to_redirect.csv' -> readable name."""
    stem = path.stem
    for sev in ("Error-", "Warning-", "Notice-"):
        if stem.startswith(sev):
            stem = stem[len(sev):]
            break
    if stem.startswith("indexable-"):
        stem = stem[len("indexable-"):]
    return stem.replace("_", " ")


def severity(path: Path) -> str:
    return path.stem.split("-", 1)[0]


def load_all(export_dir: Path) -> dict[str, list[dict[str, str]]]:
    """Map filename stem -> rows, for every CSV in the export."""
    return {p.name: read_export(p) for p in sorted(export_dir.glob("*.csv"))}


if __name__ == "__main__":
    d = Path(sys.argv[1])
    for name, rows in load_all(d).items():
        print(f"{len(rows):>6}  {severity(Path(name)):<8} {issue_name(Path(name))}")
