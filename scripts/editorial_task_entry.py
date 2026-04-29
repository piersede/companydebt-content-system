"""Prepare a compact editorial task-entry brief for a single page."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_page import load_page_config
from page_runtime_metadata import resolve_page_runtime_metadata
from runtime_pack_router import resolve_runtime_context


def estimate_tokens_from_file(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    return max(1, round(len(text) / 4))


def build_payload(page: str, task: str) -> dict:
    config = load_page_config(page)
    metadata = resolve_page_runtime_metadata(config, slug=page)
    runtime = resolve_runtime_context(
        task,
        page_type=config.get("page_type"),
        slug=page,
        page_class=metadata.page_class,
        freshness_tier=metadata.freshness_tier,
    )
    payload = {
        "page": page,
        "task": task,
        "title": config.get("title"),
        "page_type": config.get("page_type"),
        "page_class": metadata.page_class,
        "freshness_tier": metadata.freshness_tier,
        "verification_date": metadata.verification_date,
        "runtime_packs": runtime["runtime_packs"],
        "canonical_refs": runtime["canonical_refs"],
        "component_pack": runtime.get("component_pack"),
    }
    payload["runtime_tokens_estimate"] = sum(estimate_tokens_from_file(path) for path in payload["runtime_packs"])
    payload["canonical_tokens_estimate"] = sum(estimate_tokens_from_file(path) for path in payload["canonical_refs"])
    return payload


def render_markdown(payload: dict) -> str:
    lines = [
        f"# Task Entry: {payload['page']}",
        "",
        f"- Task: `{payload['task']}`",
        f"- Title: {payload.get('title') or 'Unknown'}",
        f"- Page type: `{payload.get('page_type') or 'unknown'}`",
        f"- Page class: `{payload.get('page_class') or 'unknown'}`",
        f"- Freshness tier: `{payload.get('freshness_tier') or 'unknown'}`",
        f"- Verification date: `{payload.get('verification_date') or 'unknown'}`",
        "",
        "## Runtime Path",
        *[f"- {path}" for path in payload["runtime_packs"]],
        "",
        "## Canonical References",
        *[f"- {path}" for path in payload["canonical_refs"]],
        "",
        "## Token Estimate",
        f"- Runtime packs: `{payload['runtime_tokens_estimate']}`",
        f"- Canonical refs: `{payload['canonical_tokens_estimate']}`",
        "",
        "## Component Guidance",
        (f"- Component pack: `{payload['component_pack']}`" if payload.get("component_pack") else "- No component pack mapped for this page class. See `editorial-os/28-readability-components.md` §28.5 for manual selection."),
        "- Apply 2–3 components maximum. Never all. Rhythm rules: no two same-type blocks adjacent, no component in the first two paragraphs, ≤4 total.",
        "",
        "## Operator Rule",
        "- Use this packet for routing only. Keep the quality kernel loaded every time: writer-core, relevant stage pack, overlay, and human-authorship / trust rules. Reopen canon when those quality-bearing layers need verification or extension.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a compact task-entry brief for one page.")
    parser.add_argument("--page", required=True, help="Page slug")
    parser.add_argument("--task", default="draft", help="Workflow task such as draft, review, rewrite, trust-pass")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    payload = build_payload(args.page, args.task)
    rendered = json.dumps(payload, indent=2) if args.json else render_markdown(payload)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
