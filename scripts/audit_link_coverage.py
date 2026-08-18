"""
Corpus-wide internal link audit.

Default (coverage) mode — offline, reads internal-links/_all/*.txt:
  1. Draft-status destinations — links pointing to non-published pages
  2. Inbound link coverage — which pages have zero or very few inbound links

Resolve mode (--resolve) — networked, reads drafts/*.html AND internal-links/_all/:
  Collects every root-relative href, then resolves each distinct URL against
  staging. Reports dead links and redirect-only links separately.

  This is deliberately NOT part of scripts/article_audit.py. That gate is
  per-page, must stay fast and offline, and would fail whenever staging is down.
  Run this sweep before a batch push instead.

  To keep the run cheap, the known-good set is built offline first, from the
  published pages in staging_page_inventory_fresh.json plus the "<!-- LINK: -->"
  header in each draft. Only unrecognised URLs cost a request. The trade-off is
  that the inventory is a snapshot: a page that has since been moved or
  redirected still counts as good. Pass --verify-all to fetch everything and
  catch that drift.

  Exit code is 1 if anything is dead OR unresolved. An unproven link is not a
  clean link.

Usage:
  python scripts/audit_link_coverage.py              # coverage report only
  python scripts/audit_link_coverage.py --resolve    # coverage + resolve sweep
  python scripts/audit_link_coverage.py --resolve --resolve-only
  python scripts/audit_link_coverage.py --resolve --refresh-cache
  python scripts/audit_link_coverage.py --resolve --verify-all
"""

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
ALL_DIR = ROOT / "internal-links" / "_all"
DRAFTS_DIR = ROOT / "drafts"
INVENTORY = ROOT / "staging_page_inventory_fresh.json"
CACHE_FILE = ROOT / "tmp" / "link_resolution_cache.json"

STAGING_BASE = "https://comdebstage.wpengine.com"

# WordPress serves the 404 template with HTTP 200 for some bot-ish requests and
# with HTTP 404 for perfectly good pages when the edge bot filter kicks in.
# Roughly 83% of "broken" links reported by header-only checks on this site are
# bot-blocks: 200 to a browser, 404 to a bot. So the status code proves nothing.
# The only reliable signal is the real 404 page's title.
NOT_FOUND_TITLE = "Page not found - Company Debt Ltd"

# A normal browser UA. A crawler-shaped UA gets bot-blocked and the results
# become noise.
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

HREF_RE = re.compile(r'href="(/[^"\s]*)"')
LINK_HEADER_RE = re.compile(r"<!--\s*LINK:\s*(\S+?)\s*-->")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)

# Root-relative hrefs that are not page links.
SKIP_PREFIXES = ("/wp-content/", "/wp-admin/", "/wp-json/", "/wp-includes/", "//")
SKIP_SUFFIXES = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".pdf",
                 ".css", ".js", ".ico", ".xml", ".txt", ".woff", ".woff2")


def norm(path):
    """Normalise a path to /with/leading/and/trailing/slash/."""
    path = path.split("#")[0].split("?")[0]
    return "/" + path.strip("/") + "/"


def is_page_link(path):
    if path in ("/", ""):
        return False
    if path.startswith(SKIP_PREFIXES):
        return False
    return not path.lower().endswith(SKIP_SUFFIXES)


# ══════════════════════════════════════════════════════════════════════════════
# Collection
# ══════════════════════════════════════════════════════════════════════════════

def collect_all_dir():
    """dest -> [source slug, ...] and source slug -> [dest, ...] from _all/."""
    link_map = defaultdict(list)
    source_links = defaultdict(list)
    for f in sorted(ALL_DIR.glob("*.txt")):
        slug = f.stem
        text = f.read_text(encoding="utf-8")
        for m in HREF_RE.finditer(text):
            raw = m.group(1)
            if not is_page_link(raw.split("#")[0].split("?")[0]):
                continue
            dest = norm(raw)
            link_map[dest].append(slug)
            source_links[slug].append(dest)
    return link_map, source_links


def collect_drafts():
    """dest -> [draft filename, ...] plus the set of paths named in LINK headers."""
    link_map = defaultdict(list)
    self_paths = set()
    for f in sorted(DRAFTS_DIR.glob("*.html")):
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in LINK_HEADER_RE.finditer(text[:4000]):
            parsed = urlparse(m.group(1))
            if parsed.path:
                self_paths.add(norm(parsed.path))
        for m in HREF_RE.finditer(text):
            raw = m.group(1)
            if not is_page_link(raw.split("#")[0].split("?")[0]):
                continue
            link_map[norm(raw)].append(f.name)
    return link_map, self_paths


# ══════════════════════════════════════════════════════════════════════════════
# Resolution
# ══════════════════════════════════════════════════════════════════════════════

def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            pass
    return {}


def save_cache(cache):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=1, sort_keys=True),
                          encoding="utf-8")


def find_env_file():
    """Locate .env. In a git worktree the repo root has none — .env is not
    committed, so it only exists in the main checkout. Fall back to that."""
    candidate = ROOT / ".env"
    if candidate.exists():
        return candidate
    try:
        import subprocess
        common = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=ROOT, capture_output=True, text=True, timeout=15)
        if common.returncode == 0:
            main_root = Path(common.stdout.strip()).parent
            if (main_root / ".env").exists():
                return main_root / ".env"
    except Exception:
        pass
    return None


def make_session(auth):
    import requests
    s = requests.Session()
    if auth[0]:
        s.auth = auth
    s.headers.update({
        "User-Agent": BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
    })
    return s


def page_title(body):
    m = TITLE_RE.search(body or "")
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def resolve_one(session, path):
    """Return a verdict dict for one root-relative path.

    verdict: "ok" | "redirect" | "dead" | "error"

    A 404 status alone is never enough to call a link dead — only the real
    404 page's title is. Equally, anything else that fails (401 from missing
    basic auth, 403 from the bot filter, a 5xx) is recorded as "error", never
    as "ok". A silent pass on a broken sweep is worse than no sweep.
    """
    url = STAGING_BASE + path
    try:
        r = session.get(url, timeout=30, allow_redirects=True)
    except Exception as exc:                      # network/TLS/timeout
        return {"verdict": "error", "detail": type(exc).__name__, "status": None}

    title = page_title(r.text)
    if title.lower() == NOT_FOUND_TITLE.lower():
        return {"verdict": "dead", "detail": "404 page served",
                "status": r.status_code}

    if r.status_code >= 400:
        # Bot-block, auth failure or server error. Cannot prove anything.
        return {"verdict": "error",
                "detail": f"HTTP {r.status_code}, title {title!r}",
                "status": r.status_code}

    if r.history:
        final = urlparse(r.url).path or "/"
        if norm(final) != norm(path):
            return {"verdict": "redirect", "detail": norm(final),
                    "status": r.history[0].status_code}

    return {"verdict": "ok", "detail": title, "status": r.status_code}


def resolve_mode(args):
    try:
        import requests  # noqa: F401
        from dotenv import load_dotenv
    except ImportError as exc:
        print(f"  Resolve mode needs requests and python-dotenv ({exc}).")
        return 1

    env_file = find_env_file()
    if env_file:
        load_dotenv(dotenv_path=env_file)
    auth = (os.getenv("WP_BASIC_AUTH_USER", ""), os.getenv("WP_BASIC_AUTH_PASS", ""))
    if not auth[0] or not auth[1]:
        print("  Staging basic-auth credentials missing. Set WP_BASIC_AUTH_USER "
              "and WP_BASIC_AUTH_PASS in the repo root .env.")
        return 1

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))

    all_map, _ = collect_all_dir()
    draft_map, self_paths = collect_drafts()

    # dest -> sorted list of sources, across both corpora
    combined = defaultdict(set)
    for dest, sources in all_map.items():
        combined[dest].update(f"_all/{s}" for s in sources)
    for dest, sources in draft_map.items():
        combined[dest].update(f"drafts/{s}" for s in sources)

    targets = sorted(combined)

    # Known-good set built offline first, so only unrecognised URLs cost a fetch.
    known_good = {norm(k) for k, v in inventory.items() if v.get("status") == "publish"}
    known_good |= self_paths

    if args.verify_all:
        known_good = set()

    cache = {} if args.refresh_cache else load_cache()

    unknown = [p for p in targets if p not in known_good]
    # Only a clean verdict is worth trusting from cache. Dead, redirecting and
    # unresolved links get re-checked every run, so a fix shows up immediately
    # and a one-off network wobble does not become a permanent verdict.
    to_fetch = [p for p in unknown if cache.get(p, {}).get("verdict") != "ok"]

    print("=" * 70)
    print("RESOLVE: internal links checked against staging")
    print("=" * 70)
    print(f"\n  Distinct internal links found:      {len(targets)}")
    print(f"    from drafts/*.html:               {len(draft_map)}")
    print(f"    from internal-links/_all/:        {len(all_map)}")
    print(f"  Recognised offline (no fetch):      {len(targets) - len(unknown)}")
    print(f"  Already cached:                     {len(unknown) - len(to_fetch)}")
    print(f"  Fetching now:                       {len(to_fetch)}")

    if to_fetch:
        session = make_session(auth)

        # Pre-flight. If staging refuses us, every fetch returns an auth or
        # block page and the sweep would report a reassuring nothing.
        probe = resolve_one(session, "/liquidation/")
        if probe["verdict"] != "ok":
            print(f"\n  Staging is not answering normally "
                  f"({probe['verdict']}: {probe['detail']}).")
            print(f"  Credentials read from: {env_file or 'environment'}")
            print("  Aborting rather than reporting a clean sweep.")
            return 1

        def work(path):
            verdict = resolve_one(session, path)
            time.sleep(args.delay)
            return path, verdict

        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for i, (path, verdict) in enumerate(pool.map(work, to_fetch), 1):
                cache[path] = verdict
                print(f"    [{i}/{len(to_fetch)}] {verdict['verdict']:8} {path}")
        save_cache(cache)

    dead, redirects, errors = [], [], []
    for path in unknown:
        v = cache.get(path)
        if not v:
            continue
        if v["verdict"] == "dead":
            dead.append((path, v))
        elif v["verdict"] == "redirect":
            redirects.append((path, v))
        elif v["verdict"] == "error":
            errors.append((path, v))

    print()
    print("-" * 70)
    print(f"DEAD LINKS ({len(dead)})")
    print("-" * 70)
    if dead:
        for path, v in sorted(dead):
            sources = sorted(combined[path])
            print(f"\n  {path}")
            print(f"    staging serves the real 404 page (HTTP {v['status']})")
            times = "once" if len(sources) == 1 else f"{len(sources)} times"
            print(f"    used {times}, in:")
            for s in sources[:5]:
                print(f"      - {s}")
            if len(sources) > 5:
                print(f"      ... and {len(sources) - 5} more")
    else:
        print("\n  None. Every link resolves to a real page.")

    print()
    print("-" * 70)
    print(f"REDIRECT-ONLY LINKS ({len(redirects)})")
    print("-" * 70)
    print("  These work, but cost the reader a hop. Point them at the final URL.")
    if redirects:
        for path, v in sorted(redirects):
            sources = sorted(combined[path])
            print(f"\n  {path}")
            print(f"    -> {v['detail']}  (HTTP {v['status']})")
            times = "once" if len(sources) == 1 else f"{len(sources)} times"
            print(f"    used {times}, in:")
            for s in sources[:5]:
                print(f"      - {s}")
            if len(sources) > 5:
                print(f"      ... and {len(sources) - 5} more")
    else:
        print("\n  None.")

    if errors:
        print()
        print("-" * 70)
        print(f"UNRESOLVED ({len(errors)}) — network problem, verdict unknown")
        print("-" * 70)
        for path, v in sorted(errors):
            print(f"  {path}  ({v['detail']})")

    print()
    print(f"  Summary: dead={len(dead)}  redirect-only={len(redirects)}  "
          f"unresolved={len(errors)}")
    print(f"  Cache: {CACHE_FILE}")

    # Unresolved links count as a failure too: an unproven link is not a
    # clean one, and treating it as clean is how the two dead URLs survived
    # 49 copies each.
    return 1 if (dead or errors) else 0


# ══════════════════════════════════════════════════════════════════════════════
# Coverage report (offline, unchanged behaviour)
# ══════════════════════════════════════════════════════════════════════════════

def coverage_mode():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    inventory_norm = {norm(k): v for k, v in inventory.items()}
    link_map, _ = collect_all_dir()

    print("=" * 70)
    print("PART 1: Links pointing to non-published pages")
    print("=" * 70)

    draft_issues = []
    for dest, sources in sorted(link_map.items()):
        entry = inventory_norm.get(dest)
        if entry and entry["status"] != "publish":
            draft_issues.append((dest, entry["status"], sources))

    if draft_issues:
        for dest, status, sources in draft_issues:
            print(f"\n  {dest}  [{status}]")
            for s in sources:
                print(f"    <- {s}")
    else:
        print("\n  None — all linked destinations are published.\n")

    print()
    print("=" * 70)
    print("PART 2: Published pages with zero or very few inbound links")
    print("=" * 70)

    managed_slugs = {f.stem for f in ALL_DIR.glob("*.txt")}
    published = {norm(k): v for k, v in inventory.items() if v["status"] == "publish"}

    print(f"\n  Total published pages in inventory: {len(published)}")
    print(f"  Pages with _all/ content files: {len(managed_slugs)}")

    inbound_counts = []
    for path, entry in sorted(published.items()):
        slug = entry["slug"]
        count = len(link_map.get(path, []))
        inbound_counts.append((count, path, slug, entry.get("type", "?")))

    inbound_counts.sort()

    print("\n  Pages with 0 inbound links (from managed _all/ files):")
    zero = [(p, s, t) for c, p, s, t in inbound_counts if c == 0]
    zero_managed = [(p, s, t) for p, s, t in zero if s in managed_slugs]
    for p, s, t in zero_managed:
        print(f"    {p}  ({t})")

    print("\n  Pages with exactly 1 inbound link:")
    one_managed = [(p, s, t) for c, p, s, t in inbound_counts
                   if c == 1 and s in managed_slugs]
    for p, s, t in one_managed:
        sources = link_map.get(p, [])
        print(f"    {p}  <- {sources[0]}")

    print("\n  Pages with exactly 2 inbound links:")
    two_managed = [(p, s, t) for c, p, s, t in inbound_counts
                   if c == 2 and s in managed_slugs]
    for p, s, t in two_managed:
        sources = link_map.get(p, [])
        print(f"    {p}  <- {', '.join(sources)}")

    print(f"\n  Summary: 0 inbound={len(zero_managed)}  1 inbound={len(one_managed)}"
          f"  2 inbound={len(two_managed)}")

    print("\n  Top 10 most-linked pages (for context):")
    for c, p, s, t in reversed(inbound_counts[-10:]):
        print(f"    {c:3d}  {p}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resolve", action="store_true",
                    help="also resolve every internal link against staging")
    ap.add_argument("--resolve-only", action="store_true",
                    help="skip the offline coverage report")
    ap.add_argument("--refresh-cache", action="store_true",
                    help="ignore cached verdicts and re-fetch everything")
    ap.add_argument("--verify-all", action="store_true",
                    help="fetch every link, including ones the inventory "
                         "already vouches for (slow; catches inventory drift)")
    ap.add_argument("--jobs", type=int, default=4,
                    help="parallel requests (default 4)")
    ap.add_argument("--delay", type=float, default=0.2,
                    help="seconds to pause after each request (default 0.2)")
    args = ap.parse_args()

    if not (args.resolve_only and args.resolve):
        coverage_mode()

    if args.resolve:
        print()
        return resolve_mode(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
