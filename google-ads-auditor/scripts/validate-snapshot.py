#!/usr/bin/env python3
"""Validate a saved audit run snapshot folder.

Usage: python scripts/validate-snapshot.py runs/2026-07-17-company-debt
"""

import json
import sys
from pathlib import Path

REQUIRED_RAW_FILES = [
    "account-baseline.json",
    "campaigns.json",
    "daily-performance.json",
    "conversions.json",
    "search-terms.json",
    "keywords.json",
    "ads.json",
    "devices.json",
    "networks.json",
    "landing-pages.json",
    "impression-share.json",
    "pmax.json",
]

RECONCILE_TOLERANCE_PCT = 1.0


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate-snapshot.py <run-folder>", file=sys.stderr)
        sys.exit(2)

    run_dir = Path(sys.argv[1])
    if not run_dir.exists():
        print(f"ERROR: run folder not found: {run_dir}", file=sys.stderr)
        sys.exit(2)

    errors = []
    warnings = []

    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        errors.append("missing manifest.json")
        manifest = {}
    else:
        try:
            manifest = load_json(manifest_path)
        except json.JSONDecodeError as e:
            errors.append(f"manifest.json is not valid JSON: {e}")
            manifest = {}

    if not (run_dir / "account-config.yml").exists():
        errors.append("missing account-config.yml (the config used for this run must be copied in for reproducibility)")

    raw_dir = run_dir / "raw"
    if not raw_dir.exists():
        errors.append("missing raw/ directory")
    else:
        failed_queries = {fq.get("query_file") for fq in manifest.get("failed_queries", [])}
        for filename in REQUIRED_RAW_FILES:
            file_path = raw_dir / filename
            if not file_path.exists():
                if filename in failed_queries:
                    warnings.append(f"raw/{filename} missing but recorded as a failed query in the manifest — OK")
                else:
                    errors.append(f"raw/{filename} missing and not recorded as a failed query")
                continue
            try:
                data = load_json(file_path)
            except json.JSONDecodeError as e:
                errors.append(f"raw/{filename} is not valid JSON: {e}")
                continue

            rows = data if isinstance(data, list) else data.get("results", data)
            if isinstance(rows, list):
                seen_ids = set()
                for row in rows:
                    row_id = json.dumps(row, sort_keys=True) if not isinstance(row, dict) else row.get("id") or row.get("resourceName")
                    if row_id and row_id in seen_ids:
                        warnings.append(f"raw/{filename} has a duplicate row identifier: {row_id}")
                    if row_id:
                        seen_ids.add(row_id)

    if manifest.get("warnings"):
        for w in manifest["warnings"]:
            warnings.append(f"manifest warning: {w}")

    if manifest.get("failed_queries"):
        warnings.append(f"{len(manifest['failed_queries'])} query failure(s) recorded in manifest — see failed_queries")

    if manifest.get("data_complete") is False:
        warnings.append("manifest declares data_complete: false")

    reconciliation = manifest.get("reconciliation", {})
    if reconciliation and not reconciliation.get("reconciled", False):
        errors.append(
            f"account totals did not reconcile within tolerance "
            f"(tolerance_pct={reconciliation.get('tolerance_pct', RECONCILE_TOLERANCE_PCT)}) — "
            f"analysis should not proceed until this is resolved"
        )
    elif not reconciliation:
        warnings.append("manifest has no reconciliation block — totals were not checked against each other")

    currencies = set()
    if "currency" in manifest:
        currencies.add(manifest["currency"])
    if len(currencies) > 1:
        errors.append(f"inconsistent currency across manifest/snapshot: {currencies}")

    print(f"Validating snapshot: {run_dir}")
    print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print()
        print("FAIL")
        sys.exit(1)

    print("PASS")


if __name__ == "__main__":
    main()
