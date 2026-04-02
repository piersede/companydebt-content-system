"""Estimate compact vs canonical token loads for a page workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_page import load_page_config
from page_runtime_metadata import resolve_page_runtime_metadata
from runtime_pack_router import resolve_runtime_context


def estimate_tokens(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return max(1, round(len(text) / 4))


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate workflow token load for one page/task.")
    parser.add_argument("--page", required=True, help="Page slug")
    parser.add_argument("--task", default="draft", help="Workflow task")
    parser.add_argument("--inputs", nargs="*", default=[], help="Optional input files to include")
    args = parser.parse_args()

    config = load_page_config(args.page)
    metadata = resolve_page_runtime_metadata(config, slug=args.page)
    runtime = resolve_runtime_context(
        args.task,
        page_type=config.get("page_type"),
        slug=args.page,
        page_class=metadata.page_class,
        freshness_tier=metadata.freshness_tier,
    )

    runtime_total = sum(estimate_tokens(Path(path)) for path in runtime["runtime_packs"])
    canonical_total = sum(estimate_tokens(Path(path)) for path in runtime["canonical_refs"])
    inputs = [Path(path).resolve() for path in args.inputs]
    input_total = sum(estimate_tokens(path) for path in inputs)

    payload = {
        "page": args.page,
        "task": args.task,
        "runtime_tokens": runtime_total,
        "canonical_tokens": canonical_total,
        "input_tokens": input_total,
        "total_compact_packet": runtime_total + input_total,
        "total_canonical_packet": canonical_total + input_total,
        "runtime_packs": runtime["runtime_packs"],
        "canonical_refs": runtime["canonical_refs"],
        "inputs": [str(path) for path in inputs],
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
