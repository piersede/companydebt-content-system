"""Consolidate a capture run + our existing page into two compact inputs for
the nugget-delta analysis:

- ``witnesses.md`` : every engine answer with its engine, intent label and the
  source URLs it cited (so competitor citations are visible).
- ``our-page.txt`` : the plain text of our existing page.

Keeping these as files (not dumping raw JSON into a reasoning context) is the
point: the analysis reads prose + citations, not API envelopes.
"""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

from .core import RESEARCH_DIR


# --------------------------------------------------------------------------
# Our page -> plain text
# --------------------------------------------------------------------------

class _TextExtractor(HTMLParser):
    _SKIP = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in self._SKIP:
            self._skip_depth += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "br", "div"):
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n\s*\n+", "\n\n", raw)
        return raw.strip()


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    return parser.text()


# --------------------------------------------------------------------------
# Run discovery + witness consolidation
# --------------------------------------------------------------------------

def latest_run(slug: str) -> Path:
    base = RESEARCH_DIR / slug / "_answer_audit"
    pointer = base / "latest.txt"
    if pointer.exists():
        run_id = pointer.read_text(encoding="utf-8").strip()
        cand = base / "runs" / run_id
        if cand.exists():
            return cand
    runs = sorted((base / "runs").glob("*/"))
    if not runs:
        raise RuntimeError(f"No capture runs found under {base / 'runs'}")
    return runs[-1]


def consolidate_witnesses(run_dir: Path) -> str:
    """Build witnesses.md from every <label>.answer.md + its sources file."""
    raw = run_dir / "raw"
    blocks: list[str] = ["# Answer-engine witnesses\n"]
    for engine_dir in sorted(p for p in raw.iterdir() if p.is_dir()):
        engine = engine_dir.name
        for answer in sorted(engine_dir.glob("*.answer.md")):
            label = answer.stem.replace(".answer", "")
            text = answer.read_text(encoding="utf-8").strip()
            # Cited URLs live in the sibling sources/grounding file.
            urls: list[str] = []
            for sib in (engine_dir / f"{label}.sources.json",
                        engine_dir / f"{label}.grounding-metadata.json"):
                if sib.exists():
                    data = json.loads(sib.read_text(encoding="utf-8"))
                    urls = data.get("source_urls") or data.get("cited_uris") or []
                    break
            blocks.append(f"\n## [{engine} · {label}]\n")
            if urls:
                blocks.append("**Cited sources:** " + ", ".join(urls) + "\n")
            blocks.append(text + "\n")
    out = run_dir / "processed" / "witnesses.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    md = "\n".join(blocks)
    out.write_text(md, encoding="utf-8")
    return md


def consolidate_our_page(run_dir: Path, article_html_path: Path) -> str:
    text = html_to_text(article_html_path.read_text(encoding="utf-8"))
    out = run_dir / "processed" / "our-page.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return text
