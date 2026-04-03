"""Create a smaller revision packet so rewrites do not reload everything."""

from __future__ import annotations

import argparse
from pathlib import Path

from build_page import load_page_config
from page_runtime_metadata import resolve_page_runtime_metadata
from runtime_pack_router import resolve_runtime_context


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "debug" / "revision-packets"


def read_excerpt(path: Path, limit: int = 20) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    return [line.rstrip() for line in text[:limit] if line.strip()]


def build_packet(page: str, task: str, note_paths: list[Path]) -> str:
    config = load_page_config(page)
    metadata = resolve_page_runtime_metadata(config, slug=page)
    runtime = resolve_runtime_context(
        task,
        page_type=config.get("page_type"),
        slug=page,
        page_class=metadata.page_class,
        freshness_tier=metadata.freshness_tier,
    )

    lines = [
        f"# Revision Packet: {page}",
        "",
        "## Scope",
        f"- Task: `{task}`",
        f"- Title: {config.get('title')}",
        f"- Page type: `{config.get('page_type')}`",
        f"- Page class: `{metadata.page_class}`",
        f"- Freshness tier: `{metadata.freshness_tier}`",
        "",
        "## Runtime Packs",
        *[f"- {path}" for path in runtime["runtime_packs"]],
        "",
        "## Canonical Files To Reopen Only If Needed",
        *[f"- {path}" for path in runtime["canonical_refs"]],
        "",
        "## Revision Instructions",
        "- Work from the specific notes and changed sections first.",
        "- Do not reread the whole system unless the notes expose a real ambiguity.",
        "- Enforce the human-authorship layer while changing only the targeted problems.",
        "",
        "## Notes Snapshot",
    ]
    if note_paths:
        for note_path in note_paths:
            lines.append(f"### {note_path}")
            excerpt = read_excerpt(note_path)
            if excerpt:
                lines.extend(f"- {line}" for line in excerpt)
            else:
                lines.append("- No readable content found in the first 20 lines.")
            lines.append("")
    else:
        lines.append("- Add review notes or edit diffs here before rewriting.")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a compact revision packet for a page.")
    parser.add_argument("--page", required=True, help="Page slug")
    parser.add_argument("--task", default="rewrite", help="Task name, usually rewrite or trust-pass")
    parser.add_argument("--notes", nargs="*", default=[], help="Optional note or diff files")
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    note_paths = [Path(path).resolve() for path in args.notes]
    rendered = build_packet(args.page, args.task, note_paths)
    output = Path(args.output).resolve() if args.output else DEFAULT_OUT / f"{args.page}-{args.task}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
