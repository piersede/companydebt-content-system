"""Decode UTF-16 Ahrefs site-audit CSVs and extract URL/field maps.

Usage:
    python decode_csv.py path/to/file.csv               # print as TSV (UTF-8)
    python decode_csv.py path/to/file.csv --json col1,col2  # emit JSON list of dicts

Ahrefs exports as UTF-16 LE with BOM, tab-separated, double-quoted fields.
Fields can contain literal newlines inside quotes (multi-value cells).
"""
from __future__ import annotations
import csv, json, sys, io, pathlib


def read_csv(path: str | pathlib.Path) -> list[dict[str, str]]:
    """Read a UTF-16 Ahrefs CSV and return list of dicts (one per data row)."""
    p = pathlib.Path(path)
    raw = p.read_bytes()
    # decode UTF-16 (handles BOM)
    text = raw.decode('utf-16')
    # csv.DictReader handles tab-separated, quoted fields, and embedded newlines
    reader = csv.DictReader(io.StringIO(text), delimiter='\t', quotechar='"')
    return list(reader)


def main():
    if len(sys.argv) < 2:
        print("usage: decode_csv.py <file.csv> [--json col1,col2,...]", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    rows = read_csv(path)
    if '--json' in sys.argv:
        cols = sys.argv[sys.argv.index('--json') + 1].split(',')
        out = [{c: r.get(c, '') for c in cols} for r in rows]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    if not rows:
        print("(no rows)", file=sys.stderr)
        return
    cols = list(rows[0].keys())
    print('\t'.join(cols))
    for r in rows:
        print('\t'.join((r.get(c, '') or '').replace('\n', ' | ') for c in cols))


if __name__ == '__main__':
    main()
