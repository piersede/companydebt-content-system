#!/usr/bin/env python3
"""Merge and reconcile findings from the four specialist skills into
reconciled-findings.json.

This script validates and organises data only — it does not perform
commercial judgement (severity/confidence downgrades beyond straightforward
duplicate/conflict handling are the orchestrator skill's job, not this
script's).

Usage:
  python scripts/merge-findings.py runs/2026-07-17-company-debt
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    jsonschema = None

SPECIALIST_FILES = [
    "negative-keywords.json",
    "search-opportunities.json",
    "pmax-findings.json",
    "campaign-diagnostics.json",
]

SEVERITY_RANK = {"high": 3, "medium": 2, "low": 1}
CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dedup_key(finding):
    return (
        finding.get("source_skill"),
        finding.get("campaign_id"),
        finding.get("ad_group_id"),
        finding.get("category"),
        finding.get("observation"),
    )


def conflict_key(finding):
    """Findings about the same entity that might disagree on a recommendation."""
    return (finding.get("campaign_id"), finding.get("ad_group_id"), finding.get("category"))


def rank_finding(finding):
    return (
        SEVERITY_RANK.get(finding.get("severity"), 0),
        CONFIDENCE_RANK.get(finding.get("confidence"), 0),
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python merge-findings.py <run-folder>", file=sys.stderr)
        sys.exit(2)

    run_dir = Path(sys.argv[1])
    specialist_dir = run_dir / "specialist-findings"
    if not specialist_dir.exists():
        print(f"ERROR: {specialist_dir} not found", file=sys.stderr)
        sys.exit(2)

    schema = None
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "finding.schema.json"
    if jsonschema is not None and schema_path.exists():
        schema = load_json(schema_path)
    else:
        print("WARNING: jsonschema not installed or schema missing — skipping schema validation", file=sys.stderr)

    all_findings = []
    errors = []

    for filename in SPECIALIST_FILES:
        file_path = specialist_dir / filename
        if not file_path.exists():
            errors.append(f"missing specialist findings file: {filename}")
            continue
        data = load_json(file_path)
        findings = data if isinstance(data, list) else data.get("findings", [])
        for finding in findings:
            if schema is not None:
                try:
                    jsonschema.validate(finding, schema)
                except jsonschema.ValidationError as e:
                    errors.append(f"{filename}: schema validation failed for {finding.get('finding_id', '?')}: {e.message}")
                    continue
            all_findings.append(finding)

    if errors:
        print(f"ERRORS ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(file=sys.stderr)

    seen = {}
    deduped = []
    for finding in all_findings:
        key = dedup_key(finding)
        if key in seen:
            continue
        seen[key] = finding
        deduped.append(finding)

    groups = {}
    for finding in deduped:
        groups.setdefault(conflict_key(finding), []).append(finding)

    conflicts = [group for group in groups.values() if len(group) > 1 and len({f.get("recommendation") for f in group}) > 1]

    ranked = sorted(deduped, key=rank_finding, reverse=True)

    output = {
        "generated_from": str(specialist_dir),
        "total_findings": len(ranked),
        "duplicates_removed": len(all_findings) - len(deduped),
        "conflicting_groups": len(conflicts),
        "findings": ranked,
    }

    out_path = run_dir / "reconciled-findings.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote {out_path}")
    print(f"  {len(all_findings)} findings in -> {len(deduped)} after dedup -> {len(conflicts)} conflicting group(s) flagged")

    if conflicts:
        print("\nConflicting groups (same campaign/ad_group/category, different recommendations) need orchestrator judgement:")
        for group in conflicts:
            print(f"  - {conflict_key(group[0])}: {[f.get('finding_id') for f in group]}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
