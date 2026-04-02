"""Measure canonical-vs-runtime context load for representative workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime_pack_router import resolve_runtime_context


ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_FILE = ROOT / "benchmarks" / "runtime-pack-benchmark-set.json"


def estimate_tokens(text: str) -> int:
    return max(1, round(len(text) / 4))


def file_tokens(path: Path) -> int:
    return estimate_tokens(path.read_text(encoding="utf-8"))


def benchmark_case(case: dict) -> dict:
    recommendation = resolve_runtime_context(
        case["task"],
        page_type=case.get("page_type"),
        page_class=case.get("page_class"),
        freshness_tier=case.get("freshness_tier"),
        slug=case.get("slug"),
    )
    runtime_paths = [Path(p) for p in recommendation["runtime_packs"]]
    canonical_paths = [Path(p) for p in recommendation["canonical_refs"]]

    runtime_tokens = sum(file_tokens(path) for path in runtime_paths)
    canonical_tokens = sum(file_tokens(path) for path in canonical_paths)
    saved = canonical_tokens - runtime_tokens
    saved_pct = (saved / canonical_tokens * 100) if canonical_tokens else 0.0

    return {
        "name": case["name"],
        "task": case["task"],
        "slug": case.get("slug"),
        "page_type": case.get("page_type"),
        "page_class": case.get("page_class"),
        "freshness_tier": case.get("freshness_tier"),
        "runtime_tokens": runtime_tokens,
        "canonical_tokens": canonical_tokens,
        "tokens_saved": saved,
        "savings_pct": round(saved_pct, 1),
        "runtime_packs": recommendation["runtime_packs"],
        "canonical_refs": recommendation["canonical_refs"],
        "acceptance_checks": case.get("acceptance_checks", []),
    }


def load_cases() -> list[dict]:
    data = json.loads(BENCHMARK_FILE.read_text(encoding="utf-8"))
    return data["cases"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark runtime-pack savings")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    cases = [benchmark_case(case) for case in load_cases()]
    total_runtime = sum(case["runtime_tokens"] for case in cases)
    total_canonical = sum(case["canonical_tokens"] for case in cases)
    total_saved = total_canonical - total_runtime
    total_saved_pct = (total_saved / total_canonical * 100) if total_canonical else 0.0

    payload = {
        "cases": cases,
        "summary": {
            "runtime_tokens": total_runtime,
            "canonical_tokens": total_canonical,
            "tokens_saved": total_saved,
            "savings_pct": round(total_saved_pct, 1),
        },
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return

    print("Runtime Pack Benchmark")
    print("=" * 72)
    for case in cases:
        print(
            f"{case['name']}: runtime {case['runtime_tokens']}  "
            f"canonical {case['canonical_tokens']}  "
            f"saved {case['tokens_saved']} ({case['savings_pct']}%)"
        )
    print("=" * 72)
    print(
        f"TOTAL: runtime {total_runtime}  canonical {total_canonical}  "
        f"saved {total_saved} ({round(total_saved_pct, 1)}%)"
    )


if __name__ == "__main__":
    main()
