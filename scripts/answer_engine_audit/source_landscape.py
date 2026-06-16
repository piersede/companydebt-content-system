"""Source-landscape stage — WHO the answer engines cite for this query.

AEO/GEO is a comprehensiveness-and-citability exercise, not a fact-check: the
goal is to become the source the engines cite. So before we look at our page at
all, we look at the *citation landscape* for the target query: which domains
ChatGPT and Gemini ground their answers on, whether we are even in the set, and
which competitor URLs are currently winning the citation we want.

This stage is DETERMINISTIC — pure parsing of the captured raw witnesses, no
model call, no live lookup. It cannot hallucinate a citation. It therefore also
runs cleanly on a ``--skip-capture`` resume (it reads the run's ``raw/`` dir,
not the in-memory RunContext).

Two engine quirks it normalises:

- **OpenAI** writes ``<label>.sources.json`` with a real ``source_urls`` list, so
  the domain is just the netloc.
- **Gemini** writes ``<label>.grounding-metadata.json`` whose ``cited_uris`` are
  opaque ``vertexaisearch.cloud.google.com/grounding-api-redirect/...`` blobs —
  the READABLE domain lives in ``grounding_chunks[].title`` (e.g.
  "companydebt.com"). Reading ``cited_uris`` alone (as the witness consolidation
  used to) silently dropped every Gemini source. We resolve the chunk titles
  instead, falling back to the redirect netloc only as a label. This matters
  doubly here: the Company Debt repo runs Gemini-only, so without title
  resolution the landscape would be empty.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# Our own domain — used to answer "are we already cited for this query?".
OUR_DOMAIN = "companydebt.com"

# Google's grounding redirect host. A title equal to this (or a bare netloc of a
# redirect URI) is NOT a real source domain, only an unresolved label.
_REDIRECT_HOST = "vertexaisearch.cloud.google.com"


def _norm_domain(value: str) -> str:
    """Normalise a domain-ish string to a bare registrable-ish host.

    Accepts either a full URL or an already-bare domain (Gemini chunk titles are
    bare, e.g. "support.gov.uk"). Strips scheme, ``www.`` and any path.
    Returns "" for empties or the opaque redirect host.
    """
    v = (value or "").strip()
    if not v:
        return ""
    if "://" in v or v.startswith("//") or "/" in v:
        host = urlparse(v if "://" in v else "https://" + v.lstrip("/")).netloc
    else:
        host = v
    host = host.lower().lstrip(".")
    if host.startswith("www."):
        host = host[4:]
    if not host or host == _REDIRECT_HOST:
        return ""
    return host


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def cited_domains_for_label(engine_dir: Path, label: str) -> list[str]:
    """Resolve the readable source domains a single witness cited.

    ``label`` is the query stem (``broad``, ``risk``, ``usecase-1`` ...). Returns
    a de-duplicated, order-preserving list of bare domains. Empty if the witness
    cited nothing resolvable.
    """
    domains: list[str] = []

    # OpenAI: <label>.sources.json -> source_urls (real URLs).
    src = engine_dir / f"{label}.sources.json"
    if src.exists():
        data = _read_json(src)
        urls: list[str] = []
        if isinstance(data, dict):
            urls = data.get("source_urls") or data.get("citations") or []
        elif isinstance(data, list):
            urls = data
        for u in urls:
            url = u.get("url") if isinstance(u, dict) else u
            d = _norm_domain(str(url or ""))
            if d:
                domains.append(d)

    # Gemini: <label>.grounding-metadata.json -> grounding_chunks[].title (domain),
    # NOT cited_uris (opaque redirects).
    gm = engine_dir / f"{label}.grounding-metadata.json"
    if gm.exists():
        data = _read_json(gm)
        if isinstance(data, dict):
            for chunk in data.get("grounding_chunks") or []:
                if not isinstance(chunk, dict):
                    continue
                title = chunk.get("title") or ""
                d = _norm_domain(str(title))
                if not d:
                    # Last resort: the redirect netloc is opaque, so skip it; a
                    # bare uri that is NOT a redirect (rare) is still usable.
                    d = _norm_domain(str(chunk.get("uri") or ""))
                if d:
                    domains.append(d)

    # De-dupe, preserve order.
    seen: set[str] = set()
    out: list[str] = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def build_landscape(run_dir: Path) -> dict[str, Any]:
    """Parse a run's raw witnesses into a citation-landscape structure.

    Shape::

        {
          "queries": {label: {engine: [domains...]}},
          "domain_counts": {domain: total_citation_count},
          "domain_queries": {domain: [labels...]},
          "we_cited": bool,
          "we_cited_on": [labels...],
          "competitors": [(domain, count), ...]  # excludes our domain
        }
    """
    raw = run_dir / "raw"
    queries: dict[str, dict[str, list[str]]] = defaultdict(dict)
    domain_counts: Counter[str] = Counter()
    domain_queries: dict[str, set[str]] = defaultdict(set)
    we_cited_on: set[str] = set()

    if raw.exists():
        for engine_dir in sorted(p for p in raw.iterdir() if p.is_dir()):
            engine = engine_dir.name
            labels = sorted({p.name.split(".")[0] for p in engine_dir.glob("*.*")})
            for label in labels:
                doms = cited_domains_for_label(engine_dir, label)
                if not doms:
                    continue
                queries[label][engine] = doms
                for d in doms:
                    domain_counts[d] += 1
                    domain_queries[d].add(label)
                    if d == OUR_DOMAIN:
                        we_cited_on.add(label)

    competitors = [(d, c) for d, c in domain_counts.most_common() if d != OUR_DOMAIN]
    return {
        "queries": {k: dict(v) for k, v in queries.items()},
        "domain_counts": dict(domain_counts),
        "domain_queries": {d: sorted(q) for d, q in domain_queries.items()},
        "we_cited": OUR_DOMAIN in domain_counts,
        "we_cited_on": sorted(we_cited_on),
        "competitors": competitors,
    }


def cited_domains_for_label_compat(run_dir: Path, label: str) -> list[str]:
    """Readable domains for a label across BOTH engines (used by corpus.md).

    corpus.consolidate_witnesses shows a "Cited sources" line per witness; this
    helper lets it print resolved domains (incl. Gemini titles) instead of the
    opaque redirect URIs that the raw grounding metadata holds.
    """
    raw = run_dir / "raw"
    out: list[str] = []
    seen: set[str] = set()
    if raw.exists():
        for engine_dir in sorted(p for p in raw.iterdir() if p.is_dir()):
            for d in cited_domains_for_label(engine_dir, label):
                if d not in seen:
                    seen.add(d)
                    out.append(d)
    return out


def render_markdown(keyword: str, run_id: str, land: dict[str, Any]) -> str:
    we = land["we_cited"]
    on = land["we_cited_on"]
    total_queries = len(land["queries"])
    lines: list[str] = [
        f"# Source landscape: {keyword}",
        "",
        f"**Run:** {run_id}  ",
        "**What this is:** the domains ChatGPT and Gemini actually grounded their "
        "answers on for this query, parsed from the captured citations (no model, "
        "no live lookup). It tells us who currently wins the citation we want and "
        "whether we are even in the set.",
        "",
        "---",
        "",
        "## Are we cited?",
        "",
    ]
    if we:
        lines.append(
            f"**Yes** — `{OUR_DOMAIN}` is cited on {len(on)}/{total_queries} "
            f"queries: {', '.join(on)}.")
        lines.append("")
        lines.append(
            "Being cited already is the goal; the job now is to DEFEND and widen "
            "the lead — close any coverage gap a competitor source answers that we "
            "do not, so we stay the most complete answer.")
    else:
        lines.append(
            f"**No** — `{OUR_DOMAIN}` is not cited for this query. The domains "
            "below are taking the citation. Closing their coverage gaps (in our "
            "voice, better evidenced) is how we get into the set.")
    lines += ["", "---", "", "## Who is cited (most-cited first)", ""]
    if not land["domain_counts"]:
        lines.append("_No resolvable citations in this run._")
    else:
        lines.append("| Domain | Citations | Queries | |")
        lines.append("|---|---|---|---|")
        ordered = sorted(land["domain_counts"].items(),
                         key=lambda kv: (-kv[1], kv[0]))
        for dom, cnt in ordered:
            q = ", ".join(land["domain_queries"].get(dom, []))
            us = " **(us)**" if dom == OUR_DOMAIN else ""
            lines.append(f"| `{dom}`{us} | {cnt} | {q} | |")
    lines += [
        "",
        "---",
        "",
        "_Use this to read the witnesses query-first: where a competitor domain "
        "wins a query we are weak on, that is the coverage gap to close. The "
        "additive nuggets in `06-recommended-edits.md` are how we close it, "
        "reframed in our voice, never parroted._",
        "",
    ]
    return "\n".join(lines)


def write_source_landscape(slug: str, keyword: str, run_dir: Path) -> tuple[Path, dict[str, Any]]:
    """Build + write ``reports/02-source-landscape.md`` and a JSON sibling.

    Returns (md_path, landscape). Deterministic; safe on --skip-capture resumes.
    """
    land = build_landscape(run_dir)
    reports = run_dir / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    md = render_markdown(keyword, run_dir.name, land)
    md_path = reports / "02-source-landscape.md"
    md_path.write_text(md, encoding="utf-8")
    (reports / "02-source-landscape.json").write_text(
        json.dumps(land, indent=2, ensure_ascii=False), encoding="utf-8")
    return md_path, land
