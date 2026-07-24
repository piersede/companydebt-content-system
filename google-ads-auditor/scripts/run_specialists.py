#!/usr/bin/env python3
"""Run all four specialist skills against a snapshot and save their output
where scripts/merge-findings.py expects it.

Usage:
    python scripts/run_specialists.py <run-folder>
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (script, output filename per merge-findings.py's SPECIALIST_FILES)
SPECIALISTS = [
    ("mine_negative_keywords.py", "negative-keywords.json"),
    ("analyze_search_terms.py", "search-opportunities.json"),
    ("diagnose_ad_performance.py", "campaign-diagnostics.json"),
    ("audit_performance_max.py", "pmax-findings.json"),
]


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_specialists.py <run-folder>", file=sys.stderr)
        sys.exit(2)

    run_dir = Path(sys.argv[1])
    if not run_dir.exists():
        print(f"ERROR: run folder not found: {run_dir}", file=sys.stderr)
        sys.exit(2)

    out_dir = run_dir / "specialist-findings"
    out_dir.mkdir(exist_ok=True)

    failures = []
    for script, out_name in SPECIALISTS:
        print(f"Running {script} -> specialist-findings/{out_name}")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), str(run_dir)],
            capture_output=True, text=True, encoding="utf-8",
        )
        if result.returncode != 0:
            print(f"  FAILED: {result.stderr[-2000:]}")
            failures.append(script)
            continue
        try:
            findings = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print(f"  FAILED to parse output as JSON: {e}")
            failures.append(script)
            continue
        (out_dir / out_name).write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")
        summary_line = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else ""
        print(f"  {len(findings)} finding(s). {summary_line}")

    if failures:
        print(f"\n{len(failures)} specialist(s) failed: {failures}", file=sys.stderr)
        sys.exit(1)

    print(f"\nAll specialist findings saved to {out_dir}")


if __name__ == "__main__":
    main()
