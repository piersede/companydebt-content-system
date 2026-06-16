"""Site-wide sweep: run the accessibility audit across the sitemap.

Reuses the answer-engine audit's sitemap enumeration for the page list, maps
each live path onto the target host (staging by default, so findings can be
fixed and re-verified in place), and aggregates findings across pages.

The unit of remediation is usually a *template*, not a page, so the summary
groups findings by id and shows how many pages each hits — that tells you which
fixes are site-wide (one template/CSS/plugin change clears N pages) versus a
per-page content tail (alt text, link wording).

Usage (from repo root):
    python -m scripts.accessibility_audit.sweep --sample          # 1 page per section, rendered
    python -m scripts.accessibility_audit.sweep --no-render       # fast static sweep, every page
    python -m scripts.accessibility_audit.sweep --section liquidation
    python -m scripts.accessibility_audit.sweep --json sweep.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from .audit import audit_url, SEVERITY_PENALTY
from ..answer_engine_audit import sitemap


def _load_env() -> dict:
    env: dict = {}
    p = Path(__file__).resolve().parents[2] / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"([A-Z_][A-Z0-9_]*)=(.*)", line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def _real_pages():
    """Auditable refs minus media-attachment (/wp-content/) and trashed URLs."""
    refs = sitemap.auditable_refs()
    out = []
    for r in refs:
        if r.section == "wp-content":          # image/media attachment pages
            continue
        if "__trashed" in r.path:
            continue
        out.append(r)
    return out


def _retarget(path: str, host_base: str) -> str:
    """Put a sitemap path onto the target host (e.g. staging)."""
    parts = urlsplit(host_base)
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Sweep the accessibility audit across the site.")
    ap.add_argument("--target", help="Host base to audit (default: staging from .env)")
    ap.add_argument("--no-render", action="store_true", help="Static checks only (fast)")
    ap.add_argument("--sample", action="store_true", help="One page per section only")
    ap.add_argument("--section", help="Limit to a single sitemap section")
    ap.add_argument("--limit", type=int, help="Cap number of pages")
    ap.add_argument("--json", metavar="PATH", help="Write full per-page results as JSON")
    ap.add_argument("--timeout", type=int, default=45000)
    args = ap.parse_args(argv)

    env = _load_env()
    target = args.target or env.get("WP_STAGING_URL", sitemap.BASE)
    user = env.get("WP_BASIC_AUTH_USER")
    pw = env.get("WP_BASIC_AUTH_PASS")
    basic_auth = f"{user}:{pw}" if (user and pw and "wpengine" in target) else None

    refs = _real_pages()
    if args.section:
        refs = [r for r in refs if r.section == args.section]
    if args.sample:
        seen, picked = set(), []
        for r in refs:
            if r.section not in seen:
                seen.add(r.section)
                picked.append(r)
        refs = picked
    if args.limit:
        refs = refs[: args.limit]

    print(f"Target: {target}  |  basic-auth: {'yes' if basic_auth else 'no'}  |  "
          f"render: {not args.no_render}  |  pages: {len(refs)}\n")

    results = []
    by_finding = defaultdict(list)        # id -> [paths]
    finding_meta = {}                     # id -> (severity, title)
    perfect = 0
    for i, r in enumerate(refs, 1):
        url = _retarget(r.path, target)
        try:
            rep = audit_url(url, basic_auth=basic_auth,
                            render=not args.no_render, timeout=args.timeout)
        except Exception as e:
            print(f"[{i:3}/{len(refs)}]  ERR  {r.path}  -- {e}")
            results.append({"path": r.path, "error": str(e)})
            continue
        score = rep.score
        if score == 100:
            perfect += 1
        flag = "OK " if score == 100 else "    "
        ids = ",".join(sorted(f.id for f in rep.findings)) or "-"
        print(f"[{i:3}/{len(refs)}] {flag}{score:3}/100  {r.path}  [{ids}]")
        for f in rep.findings:
            by_finding[f.id].append(r.path)
            finding_meta[f.id] = (f.severity, f.title)
        results.append({
            "path": r.path, "url": url, "score": score, "rendered": rep.rendered,
            "findings": [{"id": f.id, "severity": f.severity, "count": f.count,
                          "title": f.title} for f in rep.findings],
            "notes": rep.notes,
        })

    # ---- aggregate summary -------------------------------------------------
    print("\n" + "=" * 72)
    print(f"SWEEP SUMMARY  --  {perfect}/{len(refs)} pages at 100/100")
    print("=" * 72)
    sev_rank = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}
    for fid in sorted(by_finding, key=lambda k: (sev_rank.get(finding_meta[k][0], 9),
                                                 -len(by_finding[k]))):
        sev, title = finding_meta[fid]
        pages = by_finding[fid]
        scope = "SITE-WIDE" if len(pages) >= max(3, 0.5 * len(refs)) else "per-page"
        print(f"  [{sev:8}] {fid:28} {len(pages):4} page(s)  {scope}")
        print(f"             {title}")
    if not by_finding:
        print("  No findings. Every audited page is at full marks.")

    if args.json:
        Path(args.json).write_text(json.dumps({
            "target": target, "pages": len(refs), "perfect": perfect,
            "by_finding": {k: v for k, v in by_finding.items()},
            "results": results,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON written to {args.json}")


if __name__ == "__main__":
    main()
