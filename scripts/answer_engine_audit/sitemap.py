"""Sitemap-driven page resolution for the answer-engine audit.

The audit's unit of work is a LIVE page on companydebt.com, not a local
``PAGE_CONFIG``. This module is the new "guest list": it reads the site's Yoast
sitemap index, enumerates the content URLs worth auditing, and fetches a live
page's HTML so the rest of the pipeline can compare engine answers against what
the answer engines actually crawl.

Why live, not staging: an AEO/citation audit must compare against exactly what
ChatGPT and Gemini index. Staging can differ from production, so for THIS tool
the usual "staging only" rule is deliberately inverted. Everything here is
read-only HTTP (GET); the audit still never writes anything to the live site.

Scope (substantive guidance only):
- INCLUDE the page + post sitemaps.
- EXCLUDE landing pages (``/sectors/``, ``/services-to/``), news posts
  (``/articles/``), tools, and utility/legal pages (home, terms, cookies,
  sitemap, calculator). The exclusion lists are constants below so they are easy
  to audit and adjust.
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from .core import RESEARCH_DIR

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

BASE = "https://www.companydebt.com"
SITEMAP_INDEX = f"{BASE}/sitemap_index.xml"

# Only these child sitemaps carry auditable content. testimonial / category
# sitemaps are never content for this purpose.
CONTENT_SITEMAPS = ("page-sitemap.xml", "post-sitemap.xml")

# Landing pages and news posts: present on the site, but not the substantive
# guidance the audit targets. Matched as path prefixes.
EXCLUDE_PATH_PREFIXES = (
    "/sectors/",        # sector landing pages
    "/services-to/",    # B2B referral landing pages
    "/articles/",       # news / press posts
)

# Utility, legal and tool pages: not guidance content.
EXCLUDE_EXACT_PATHS = {
    "/",                       # homepage
    "/site-map/",
    "/sitemap/",
    "/terms-conditions/",
    "/terms-and-conditions/",
    "/cookie-policy/",
    "/privacy-policy/",
    "/privacy/",
    "/contact/",
    "/contact-us/",
    "/about/",
    "/about-us/",
    "/insolvency-calculator/",  # interactive tool, no prose to audit
}

# Polite live-fetch defaults.
USER_AGENT = ("Mozilla/5.0 (compatible; CompanyDebtAEOAudit/1.0; "
              "+https://www.companydebt.com)")
FETCH_DELAY_S = 0.5          # between successive live page fetches
HTTP_TIMEOUT_S = 30
SITEMAP_TTL_DAYS = 7         # reuse the cached URL list within this window

_CACHE_DIR = RESEARCH_DIR / "_answer_audit_sitemap"
_CACHE_FILE = _CACHE_DIR / "urls.json"

# Namespace-agnostic <loc> matcher. The wildcard namespace works in
# findall/iterfind (ElementPath) but NOT in Element.iter (exact tag match only).
_LOC = ".//{*}loc"


# --------------------------------------------------------------------------
# Page reference
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class PageRef:
    """A single auditable page, identified by its live URL."""

    url: str          # canonical absolute URL
    path: str         # url path, e.g. "/advice/misfeasance/"
    key: str          # filesystem-safe storage key, e.g. "advice__misfeasance"
    section: str      # first path segment, e.g. "advice" ("" for root-level)


def _path_of(url: str) -> str:
    m = re.match(r"https?://[^/]+(/.*)?$", url.strip())
    path = (m.group(1) if m and m.group(1) else "/")
    if not path.endswith("/"):
        path += "/"
    return path


def page_key(path: str) -> str:
    """Filesystem-safe storage key from a url path.

    "/advice/misfeasance/" -> "advice__misfeasance"
    "/county-court-judgements/" -> "county-court-judgements"
    """
    parts = [p for p in path.strip("/").split("/") if p]
    if not parts:
        return "_root"
    safe = ["-".join(re.findall(r"[a-z0-9]+", p.lower())) for p in parts]
    return "__".join(s for s in safe if s) or "_root"


def _ref(url: str) -> PageRef:
    path = _path_of(url)
    parts = [p for p in path.strip("/").split("/") if p]
    section = parts[0] if parts else ""
    # Canonicalise to the trailing-slash form on the configured base host.
    canonical = url if url.startswith("http") else f"{BASE}{path}"
    return PageRef(url=canonical, path=path, key=page_key(path), section=section)


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

def _http_get(url: str, *, timeout: int = HTTP_TIMEOUT_S) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (trusted host)
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


# --------------------------------------------------------------------------
# Sitemap enumeration
# --------------------------------------------------------------------------

def _locs(xml_text: str) -> list[str]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    return [el.text.strip() for el in root.findall(_LOC) if el.text and el.text.strip()]


def _exclusion_reason(path: str) -> str | None:
    """Why a path is NOT auditable, or None if it is. Used for transparency."""
    if path in EXCLUDE_EXACT_PATHS:
        return "utility/legal/tool"
    for prefix in EXCLUDE_PATH_PREFIXES:
        if path.startswith(prefix):
            return f"landing/news ({prefix})"
    return None


def _fetch_all_urls() -> list[str]:
    """Fetch the sitemap index and every CONTENT child sitemap; return all
    content URLs (unfiltered)."""
    index = _http_get(SITEMAP_INDEX)
    child_sitemaps = [u for u in _locs(index)
                      if any(u.endswith(name) for name in CONTENT_SITEMAPS)]
    urls: list[str] = []
    for sm in child_sitemaps:
        urls.extend(_locs(_http_get(sm)))
    # de-dupe, preserve order
    seen: set[str] = set()
    return [u for u in urls if not (u in seen or seen.add(u))]


def _load_cache(ttl_days: int) -> dict | None:
    if not _CACHE_FILE.exists():
        return None
    try:
        data = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
        stamp = datetime.fromisoformat(data["fetched_at"])
    except Exception:
        return None
    age_days = (datetime.now(timezone.utc) - stamp).total_seconds() / 86400
    return data if age_days <= ttl_days else None


def refresh_urls() -> dict:
    """Force a live sitemap fetch and rewrite the cache. Returns the cache dict."""
    all_urls = _fetch_all_urls()
    kept: list[str] = []
    skipped: list[dict] = []
    for u in all_urls:
        reason = _exclusion_reason(_path_of(u))
        if reason:
            skipped.append({"url": u, "reason": reason})
        else:
            kept.append(u)
    data = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "auditable": kept,
        "skipped": skipped,
        "counts": {"auditable": len(kept), "skipped": len(skipped),
                   "total": len(all_urls)},
    }
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _CACHE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                           encoding="utf-8")
    return data


def load_urls(*, ttl_days: int = SITEMAP_TTL_DAYS, force: bool = False) -> dict:
    """Return the cached sitemap data, refreshing if stale or missing."""
    if not force:
        cached = _load_cache(ttl_days)
        if cached is not None:
            return cached
    return refresh_urls()


def auditable_refs(*, ttl_days: int = SITEMAP_TTL_DAYS,
                   force: bool = False) -> list[PageRef]:
    return [_ref(u) for u in load_urls(ttl_days=ttl_days, force=force)["auditable"]]


# --------------------------------------------------------------------------
# Target resolution (url | path | bare slug)
# --------------------------------------------------------------------------

def resolve_target(target: str, *, ttl_days: int = SITEMAP_TTL_DAYS) -> PageRef:
    """Resolve a user-supplied target to a single auditable PageRef.

    Accepts a full URL, a path ("/advice/misfeasance/"), or a bare last-segment
    slug ("misfeasance"). A bare slug that matches more than one page raises with
    the candidates listed, so resolution is never silently wrong.
    """
    refs = auditable_refs(ttl_days=ttl_days)
    t = target.strip()

    if t.startswith("http") or t.startswith("/"):
        want = _path_of(t if t.startswith("http") else f"{BASE}{t}")
        for r in refs:
            if r.path == want:
                return r
        raise RuntimeError(
            f"'{target}' is not in the auditable sitemap (path {want}). "
            f"It may be excluded (landing/news/utility) or not published. "
            f"Run `sitemap --refresh` to update the list.")

    # bare slug -> match the final path segment
    matches = [r for r in refs if r.path.strip("/").split("/")[-1] == t.lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise RuntimeError(
            f"No auditable page with slug '{t}'. Pass a full path or URL, or "
            f"run `sitemap` to list available targets.")
    cands = "\n  ".join(r.path for r in matches)
    raise RuntimeError(
        f"Slug '{t}' is ambiguous across {len(matches)} pages. Pass the full "
        f"path instead:\n  {cands}")


# --------------------------------------------------------------------------
# Live page fetch + parsing
# --------------------------------------------------------------------------

_last_fetch_at = [0.0]


def fetch_page_html(url: str) -> str:
    """Polite live GET of a page. Spaces successive calls by FETCH_DELAY_S."""
    wait = FETCH_DELAY_S - (time.monotonic() - _last_fetch_at[0])
    if wait > 0:
        time.sleep(wait)
    html = _http_get(url)
    _last_fetch_at[0] = time.monotonic()
    return html


def extract_title(html: str) -> str:
    """The page's topic, for use as the audit keyword. Prefers the first <h1>,
    falls back to <title> minus a trailing brand suffix."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            return text
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    if m:
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
        # strip "... | Company Debt" / "... - Company Debt" brand suffixes
        text = re.split(r"\s[|\-]\s", text)[0].strip()
        return text
    return ""


def extract_jsonld(html: str) -> str:
    """All JSON-LD schema blocks from the live page, pretty-printed. Empty
    string if none. Mirrors the previous build-time guard but uses the REAL
    rendered page."""
    blocks = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.S | re.I)
    pretty: list[str] = []
    for b in blocks:
        try:
            pretty.append(json.dumps(json.loads(b), ensure_ascii=False, indent=1))
        except Exception:
            pretty.append(b.strip())
    return "\n\n".join(pretty)
