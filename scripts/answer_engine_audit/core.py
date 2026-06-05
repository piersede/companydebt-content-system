"""Core: environment, page-config resolution, immutable run storage.

Conventions match the rest of the repo:
- `.env` lives at the repository root and is loaded via python-dotenv.
- Page configs live in `scripts/page_builder/data/pages/<name>.py` as a
  module-level ``PAGE_CONFIG`` dict.
- Research artefacts live under ``research/<slug>/``; this system namespaces
  its output under ``research/<slug>/_answer_audit/`` so it never collides
  with existing research files.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# --------------------------------------------------------------------------
# Repo + environment
# --------------------------------------------------------------------------

def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from ``start`` until a directory containing ``.env`` or ``.git``
    is found. Falls back to two levels above this file (scripts/<pkg>/core.py
    -> repo root)."""
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".env").exists() or (parent / ".git").exists():
            return parent
    return Path(__file__).resolve().parents[2]


REPO_ROOT = find_repo_root()

# Page-config and card layout differ across repos. BusinessExpert uses
# scripts/page_builder/data/{pages,cards}; the Company Debt system uses
# scripts/cc_builder/data/{pages,cards}. We prefer the repo's own
# build_page.load_page_config (the authoritative slug->module map) and fall
# back to scanning whichever of these directories exists.
_PAGE_DIR_CANDIDATES = (
    REPO_ROOT / "scripts" / "page_builder" / "data" / "pages",
    REPO_ROOT / "scripts" / "cc_builder" / "data" / "pages",
)
_CARD_DIR_CANDIDATES = (
    REPO_ROOT / "scripts" / "page_builder" / "data" / "cards",
    REPO_ROOT / "scripts" / "cc_builder" / "data" / "cards",
)


def _first_existing(candidates: tuple[Path, ...]) -> Path:
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


PAGES_DIR = _first_existing(_PAGE_DIR_CANDIDATES)
CARDS_DIR = _first_existing(_CARD_DIR_CANDIDATES)
RESEARCH_DIR = REPO_ROOT / "research"


def load_env() -> None:
    """Load the repo-root .env into os.environ (no-op if already present)."""
    import os

    if os.getenv("OPENAI_API_KEY") and os.getenv("GEMINI_API_KEY"):
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(REPO_ROOT / ".env")
    except Exception:
        pass


def require_key(name: str) -> str:
    import os

    load_env()
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"{name} not found. Set it in the environment or in {REPO_ROOT / '.env'}."
        )
    return value


def available_engines() -> list[str]:
    """Capture engines whose API keys are present, in a stable order. Lets
    capture default to only what this repo is configured for — e.g. the Company
    Debt repo has GEMINI_API_KEY but no OPENAI_API_KEY."""
    import os

    load_env()
    out: list[str] = []
    if os.getenv("OPENAI_API_KEY"):
        out.append("openai")
    if os.getenv("GEMINI_API_KEY"):
        out.append("gemini")
    return out


# --------------------------------------------------------------------------
# Page config resolution
# --------------------------------------------------------------------------

def _import_page_config(path: Path) -> dict[str, Any] | None:
    spec = importlib.util.spec_from_file_location(f"_aeo_page_{path.stem}", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    cfg = getattr(module, "PAGE_CONFIG", None)
    return cfg if isinstance(cfg, dict) else None


def _resolve_via_build_page(slug: str) -> dict[str, Any] | None:
    """Use the repo's own ``build_page.load_page_config`` if it exists. That
    function owns the canonical slug->module map (e.g. ``PAGE_REGISTRY``), so it
    works regardless of how the pages directory is laid out."""
    import importlib
    import sys

    scripts_dir = REPO_ROOT / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        build_page = importlib.import_module("build_page")
    except Exception:
        return None
    loader = getattr(build_page, "load_page_config", None)
    if loader is None:
        return None
    try:
        cfg = loader(slug)
    except Exception:
        return None
    return cfg if isinstance(cfg, dict) else None


def resolve_page(slug: str) -> dict[str, Any]:
    """Find the PAGE_CONFIG whose slug matches. Prefers the repo's own
    ``build_page.load_page_config``; otherwise scans the known pages
    directories for a module-level ``PAGE_CONFIG`` whose slug matches."""
    cfg = _resolve_via_build_page(slug)
    if cfg and cfg.get("slug") == slug:
        return cfg

    direct = PAGES_DIR / f"{slug.replace('-', '_')}.py"
    if direct.exists():
        cfg = _import_page_config(direct)
        if cfg and cfg.get("slug") == slug:
            return cfg
    for cand_dir in _PAGE_DIR_CANDIDATES:
        if not cand_dir.exists():
            continue
        for path in sorted(cand_dir.glob("*.py")):
            cfg = _import_page_config(path)
            if cfg and cfg.get("slug") == slug:
                return cfg
    raise RuntimeError(
        f"No page config with slug '{slug}' found "
        f"(tried build_page.load_page_config and {PAGES_DIR})."
    )


def derive_keyword(cfg: dict[str, Any]) -> str:
    """Target query for the audit: the head of the title before any colon."""
    title = str(cfg.get("title", "")).strip()
    return title.split(":")[0].strip() or cfg.get("slug", "").replace("-", " ").title()


# --------------------------------------------------------------------------
# Run storage (immutable snapshots)
# --------------------------------------------------------------------------

@dataclass
class RunContext:
    """A single immutable audit run. Each run is a new timestamped folder;
    prior runs are never overwritten. ``latest`` is a soft pointer file."""

    slug: str
    keyword: str
    cfg: dict[str, Any]
    run_id: str
    root: Path  # research/<slug>/_answer_audit/runs/<run_id>/
    source_index: list[dict[str, Any]] = field(default_factory=list)

    @property
    def raw_dir(self) -> Path:
        return self.root / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.root / "processed"

    @property
    def reports_dir(self) -> Path:
        return self.root / "reports"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"

    def for_dirs(self) -> list[Path]:
        return [self.raw_dir, self.processed_dir, self.reports_dir, self.logs_dir]


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def new_run(slug: str, *, dry_run: bool = False) -> RunContext:
    cfg = resolve_page(slug)
    keyword = derive_keyword(cfg)
    run_id = _utc_stamp()
    root = RESEARCH_DIR / slug / "_answer_audit" / "runs" / run_id
    ctx = RunContext(slug=slug, keyword=keyword, cfg=cfg, run_id=run_id, root=root)
    if not dry_run:
        for d in ctx.for_dirs():
            d.mkdir(parents=True, exist_ok=True)
    return ctx


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_raw(ctx: RunContext, rel_path: str, payload: Any, *,
              source_type: str, engine: str, query: str,
              source_urls: list[str] | None = None, status: str = "ok") -> Path:
    """Write a raw witness file and register it in the source index.

    ``payload`` is JSON-serialised if it is not already a string.
    """
    out = ctx.raw_dir / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    text = payload if isinstance(payload, str) else json.dumps(payload, indent=2, ensure_ascii=False)
    out.write_text(text, encoding="utf-8")
    ctx.source_index.append({
        "source_id": f"{engine}:{out.stem}:{len(ctx.source_index) + 1}",
        "source_type": source_type,
        "engine": engine,
        "date_captured": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "source_urls": source_urls or [],
        "status": status,
        "local_file": str(out.relative_to(ctx.root)),
        "sha256": _sha256(text),
    })
    return out


def write_source_index(ctx: RunContext) -> Path:
    """Write reports/01-raw-source-index.md and a JSON sibling, plus refresh
    the `latest` soft pointer."""
    md_lines = [
        f"# Raw source index — {ctx.keyword}",
        "",
        f"- **Slug:** {ctx.slug}",
        f"- **Run:** {ctx.run_id}",
        f"- **Captured witnesses:** {len(ctx.source_index)}",
        "",
        "| Source id | Engine | Type | Captured | Status | File | SHA-256 |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in ctx.source_index:
        md_lines.append(
            "| {source_id} | {engine} | {source_type} | {date_captured} | "
            "{status} | `{local_file}` | `{sha}` |".format(
                sha=s["sha256"][:12], **s)
        )
    md = "\n".join(md_lines) + "\n"
    (ctx.reports_dir / "01-raw-source-index.md").write_text(md, encoding="utf-8")
    (ctx.reports_dir / "01-raw-source-index.json").write_text(
        json.dumps(ctx.source_index, indent=2, ensure_ascii=False), encoding="utf-8")

    # Soft `latest` pointer (a file, since Windows symlinks need privileges).
    latest = RESEARCH_DIR / ctx.slug / "_answer_audit" / "latest.txt"
    latest.parent.mkdir(parents=True, exist_ok=True)
    latest.write_text(ctx.run_id + "\n", encoding="utf-8")
    return ctx.reports_dir / "01-raw-source-index.md"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
