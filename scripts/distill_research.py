"""Create smaller research artifacts from larger research inputs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "research" / "distilled"
URL_RE = re.compile(r"https?://[^\s)>\"]+")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6}\s+.+)$", re.MULTILINE)
NUMBER_LINE_RE = re.compile(r"^.*\b(\d{1,4}(?:\.\d+)?%?|\d{4})\b.*$", re.MULTILINE)


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(data, indent=2, ensure_ascii=True)
    return path.read_text(encoding="utf-8", errors="ignore")


def collect_highlights(text: str) -> dict:
    headings = HEADING_RE.findall(text)[:12]
    urls = list(dict.fromkeys(URL_RE.findall(text)))[:20]
    lines_with_numbers = []
    for line in text.splitlines():
        if NUMBER_LINE_RE.match(line):
            lines_with_numbers.append(line.strip())
        if len(lines_with_numbers) >= 20:
            break
    return {
        "headings": headings,
        "urls": urls,
        "claims": lines_with_numbers,
    }


def write_outputs(slug: str, sources: list[Path], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    combined = "\n\n".join(read_text(path) for path in sources)
    highlights = collect_highlights(combined)

    summary_path = out_dir / f"{slug}-research-summary.md"
    claims_path = out_dir / f"{slug}-claims-to-verify.json"
    brief_path = out_dir / f"{slug}-decision-brief.md"

    heading_lines = [f"- {item}" for item in highlights["headings"]] or ["- None found"]
    url_lines = [f"- {item}" for item in highlights["urls"]] or ["- None found"]
    claim_lines = [f"- {item}" for item in highlights["claims"]] or ["- None found"]
    brief_url_lines = [f"- {item}" for item in highlights["urls"]] or ["- None surfaced automatically"]

    summary_lines = [
        f"# Research Summary: {slug}",
        "",
        "## Source Files",
        *[f"- {path}" for path in sources],
        "",
        "## Key Headings Surfaced",
        *heading_lines,
        "",
        "## URLs Worth Keeping",
        *url_lines,
        "",
        "## Quantitative / Date Signals",
        *claim_lines,
        "",
        "## Writer Notes",
        "- Distill the evidence into a short decision-shaped brief before drafting.",
        "- Keep only the facts, trade-offs, and differentiators the draft truly needs.",
    ]
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    claims_payload = {
        "slug": slug,
        "source_files": [str(path) for path in sources],
        "claims_to_verify": [
            {"claim": item, "status": "unchecked", "notes": ""}
            for item in highlights["claims"]
        ],
    }
    claims_path.write_text(json.dumps(claims_payload, indent=2), encoding="utf-8")

    brief_lines = [
        f"# Decision Brief: {slug}",
        "",
        "## Reader Decision",
        "- What does the reader actually need to decide after reading this page?",
        "",
        "## Must-Keep Facts",
        "- Fill in the 3-7 facts that materially change the decision.",
        "",
        "## Non-Negotiable Trade-Offs",
        "- Fill in the frictions, costs, exclusions, or caveats that must survive drafting.",
        "",
        "## Sources To Reopen If Challenged",
        *brief_url_lines,
        "",
        "## Writing Rule",
        "- Draft from this brief, not from the full research dump.",
    ]
    brief_path.write_text("\n".join(brief_lines) + "\n", encoding="utf-8")
    return [summary_path, claims_path, brief_path]


def main() -> int:
    parser = argparse.ArgumentParser(description="Distill large research inputs into smaller working artifacts.")
    parser.add_argument("sources", nargs="+", help="Research source files")
    parser.add_argument("--slug", required=True, help="Slug used for output artifact names")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT), help="Output directory for distilled artifacts")
    args = parser.parse_args()

    paths = [Path(source).resolve() for source in args.sources]
    outputs = write_outputs(args.slug, paths, Path(args.out_dir).resolve())
    for path in outputs:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
