"""Core audit: static HTML checks + optional Playwright runtime checks.

The static checks parse the served HTML (cheap, no browser). The runtime checks
load the page in headless Chromium to catch what only exists after render — most
importantly the "lazy-render hollowing" pattern, where content is in the HTML but
skipped from the rendered accessibility tree until scrolled (see check_render).

Usage:
    python -m accessibility_audit --url https://example.com
    python -m accessibility_audit --url https://staging.example.com \
        --basic-auth user:pass --json report.json
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ── severity model ──────────────────────────────────────────────────────────
# Penalty points deducted from a 100 baseline, per *distinct* finding (not per
# node). Tuned so a single critical issue (e.g. body hollowed from the tree)
# dominates the score the way it dominates real agent failure.
SEVERITY_PENALTY = {"critical": 40, "serious": 18, "moderate": 8, "minor": 3}

GENERIC_LINK_TEXT = {
    "click here", "here", "read more", "learn more", "find out more", "more",
    "view deal", "details", "view details", "see more", "this", "link",
    "continue", "go", "view", "shop now", "apply",
}

# Render-deferral markers that remove content from the accessibility tree until
# it scrolls into view. data-wpr-lazyrender = WP Rocket "Lazy Render Content".
LAZY_RENDER_MARKERS = [
    "data-wpr-lazyrender",          # WP Rocket
    "content-visibility:auto",      # raw CSS (any source)
    "content-visibility: auto",
]


@dataclass
class Finding:
    id: str
    severity: str                 # critical | serious | moderate | minor
    title: str
    detail: str
    remediation: str
    count: int = 0
    samples: list = field(default_factory=list)


@dataclass
class Report:
    url: str
    findings: list = field(default_factory=list)
    rendered: bool = False
    notes: list = field(default_factory=list)

    @property
    def score(self) -> int:
        penalty = sum(SEVERITY_PENALTY.get(f.severity, 0) for f in self.findings)
        return max(0, 100 - penalty)

    def add(self, f: Optional[Finding]):
        if f and f.count:
            self.findings.append(f)


# ── helpers ─────────────────────────────────────────────────────────────────
def _accessible_name(tag) -> str:
    """Best-effort accessible name for a link/button from static HTML."""
    if tag.get("aria-label"):
        return tag.get("aria-label").strip()
    if tag.get("title"):
        return tag.get("title").strip()
    txt = tag.get_text(" ", strip=True)
    if txt:
        return txt
    img = tag.find("img")
    if img and img.get("alt"):
        return img.get("alt").strip()
    return ""


# ── static checks (BeautifulSoup) ───────────────────────────────────────────
def check_lazy_render(html: str, report: Report):
    hits = sum(html.count(m) for m in LAZY_RENDER_MARKERS)
    if hits:
        wpr = "data-wpr-lazyrender" in html
        report.add(Finding(
            id="lazy-render-hollowing",
            severity="critical",
            title="Content deferred out of the accessibility tree (lazy render)",
            detail=(
                f"Found {hits} render-deferral marker(s)"
                + (" — WP Rocket 'Lazy Render Content'." if wpr else " (content-visibility:auto).")
                + " Off-screen content is skipped from the rendered a11y tree until"
                " scrolled, so an agent reading the page at load sees a hollow shell."
            ),
            remediation=(
                "WP Rocket: add_filter('rocket_lrc_optimization', '__return_false'); "
                "(no settings toggle in 3.20). CSS backstop: "
                "[data-wpr-lazyrender]{content-visibility:visible!important}. "
                "Generic: never apply content-visibility:auto to a wrapper holding the "
                "whole article. Purge the page cache after."
            ),
            count=hits,
        ))


def check_duplicate_main(soup: BeautifulSoup, report: Report):
    mains = soup.find_all("main") + soup.select('[role="main"]')
    if len(mains) > 1:
        report.add(Finding(
            id="duplicate-main",
            severity="serious",
            title="Multiple <main> landmarks",
            detail=f"{len(mains)} main landmarks; agents/AT can't tell which is primary.",
            remediation="Keep exactly one <main>. Demote nested ones to <div> (style by class, not tag).",
            count=len(mains),
            samples=[str(m)[:90] for m in mains[:3]],
        ))


def check_invalid_lists(soup: BeautifulSoup, report: Report):
    bad = []
    for ul in soup.find_all(["ul", "ol"]):
        for child in ul.find_all(recursive=False):
            if child.name not in ("li", "script", "template"):
                bad.append(ul)
                break
    if bad:
        report.add(Finding(
            id="invalid-list",
            severity="moderate",
            title="<ul>/<ol> with non-<li> children",
            detail=f"{len(bad)} list(s) contain direct <div>/other children; screen readers mis-announce them.",
            remediation="Make the wrapper a <div>, or wrap each item in <li>.",
            count=len(bad),
            samples=[f"<{u.name} class={u.get('class')}>" for u in bad[:3]],
        ))


def check_label_in_name(soup: BeautifulSoup, report: Report):
    """WCAG 2.5.3: accessible name must contain the visible text."""
    viol = []
    for tag in soup.find_all(["a", "button"]):
        aria = (tag.get("aria-label") or "").strip()
        if not aria:
            continue
        visible = tag.get_text(" ", strip=True)
        # strip arrows / icon glyphs from visible text
        visible_clean = re.sub(r"[←-⇿✀-➿→←↑↓»«]", "", visible).strip()
        if visible_clean and visible_clean.lower() not in aria.lower():
            viol.append((visible_clean, aria))
    if viol:
        report.add(Finding(
            id="label-in-name",
            severity="serious",
            title="aria-label does not contain the visible text (WCAG 2.5.3)",
            detail=f"{len(viol)} control(s) where the accessible name omits the visible label — breaks voice control and confuses agents.",
            remediation='Make the aria-label CONTAIN the visible string, e.g. visible "View Deal" -> aria-label="View Deal, Tide".',
            count=len(viol),
            samples=[f'visible="{v}" aria-label="{a}"' for v, a in viol[:4]],
        ))


def check_aria_role_overrides(soup: BeautifulSoup, report: Report):
    """Inappropriate role on a semantic element (e.g. <aside role=navigation>)."""
    suspicious = {"aside": {"navigation", "main", "banner"},
                  "nav": {"complementary", "main"},
                  "section": {"navigation"}}
    bad = []
    for tag in soup.find_all(list(suspicious.keys())):
        role = (tag.get("role") or "").strip().lower()
        if role and role in suspicious[tag.name]:
            bad.append((tag.name, role))
    if bad:
        report.add(Finding(
            id="inappropriate-role",
            severity="moderate",
            title="Inappropriate ARIA role override on a semantic element",
            detail=f"{len(bad)} element(s) override their implicit role (e.g. <aside role=navigation>).",
            remediation="Use the right element instead of overriding: a TOC is a <nav>, not <aside role=navigation>.",
            count=len(bad),
            samples=[f"<{n} role={r}>" for n, r in bad[:4]],
        ))


def check_th_scope(soup: BeautifulSoup, report: Report):
    bare = [th for th in soup.find_all("th") if not th.get("scope")]
    if bare:
        report.add(Finding(
            id="th-scope",
            severity="minor",
            title="Table headers without scope",
            detail=f"{len(bare)} <th> cell(s) lack a scope attribute; agents can't bind data cells to headers.",
            remediation='Add scope="col" (or "row") to every <th>.',
            count=len(bare),
        ))


def check_generic_links(soup: BeautifulSoup, report: Report):
    generic = []
    for a in soup.find_all("a"):
        name = _accessible_name(a).lower().strip(" →←»« ")
        if name in GENERIC_LINK_TEXT:
            generic.append(name)
    if generic:
        report.add(Finding(
            id="generic-link-text",
            severity="moderate",
            title='Non-descriptive link text ("click here", "view deal", ...)',
            detail=f"{len(generic)} link(s) have generic names indistinguishable out of context.",
            remediation='Make each link self-describing, or add an aria-label that contains the visible text + target.',
            count=len(generic),
            samples=sorted(set(generic))[:6],
        ))


def check_missing_alt(soup: BeautifulSoup, report: Report):
    imgs = soup.find_all("img")
    missing = [i for i in imgs if i.get("alt") is None or i.get("alt").strip() == ""]
    # images inside tables are the classic "pricing locked in an image" trap
    in_table = [i for i in missing if i.find_parent("table")]
    if missing:
        report.add(Finding(
            id="missing-alt",
            severity="serious" if in_table else "moderate",
            title="Images without alt text",
            detail=f"{len(missing)} of {len(imgs)} image(s) have no alt text"
                   + (f"; {len(in_table)} sit inside a <table> (data/pricing locked in an image)." if in_table else "."),
            remediation="Add descriptive alt text; never put pricing/specs only in an image.",
            count=len(missing),
        ))


def check_unnamed_interactive(soup: BeautifulSoup, report: Report):
    unnamed = []
    for tag in soup.find_all(["button", "a"]):
        if tag.name == "a" and not tag.get("href"):
            continue
        if not _accessible_name(tag) and not tag.get("aria-labelledby"):
            unnamed.append(tag.name)
    if unnamed:
        report.add(Finding(
            id="unnamed-interactive",
            severity="serious",
            title="Interactive elements with no accessible name",
            detail=f"{len(unnamed)} button/link(s) an agent cannot identify or invoke.",
            remediation="Give every control text content or an aria-label (icon-only buttons especially).",
            count=len(unnamed),
        ))


def check_headings(soup: BeautifulSoup, report: Report):
    levels = [int(h.name[1]) for h in soup.find_all(re.compile(r"^h[1-6]$"))]
    h1 = levels.count(1)
    skips = [f"h{levels[i-1]}->h{levels[i]}" for i in range(1, len(levels)) if levels[i] - levels[i-1] > 1]
    if h1 != 1:
        report.add(Finding(
            id="h1-count", severity="moderate",
            title=f"Page has {h1} <h1> headings (want exactly 1)",
            detail="Agents use the H1 as the page's primary topic.",
            remediation="Exactly one H1 that states what the page is.",
            count=1,
        ))
    if skips:
        report.add(Finding(
            id="heading-skips", severity="minor",
            title="Heading level skips",
            detail=f"{len(skips)} skipped level(s): {', '.join(skips[:5])}.",
            remediation="Don't jump heading levels; nest sequentially.",
            count=len(skips),
        ))


def check_structured_data(soup: BeautifulSoup, report: Report):
    blocks = soup.find_all("script", attrs={"type": "application/ld+json"})
    types = []
    for b in blocks:
        try:
            data = json.loads(b.string or "{}")
            for obj in (data if isinstance(data, list) else data.get("@graph", [data])):
                t = obj.get("@type")
                if t:
                    types.extend(t if isinstance(t, list) else [t])
        except Exception:
            pass
    report.notes.append(f"JSON-LD blocks: {len(blocks)} | types: {sorted(set(types)) or 'none'}")
    if not blocks:
        report.add(Finding(
            id="no-structured-data", severity="moderate",
            title="No JSON-LD structured data",
            detail="Structured data is the machine-readable layer answer engines consume directly.",
            remediation="Add schema.org JSON-LD (Article, BreadcrumbList, FAQPage, ItemList as relevant).",
            count=1,
        ))


def check_basics(soup: BeautifulSoup, report: Report):
    html_tag = soup.find("html")
    if not (html_tag and html_tag.get("lang")):
        report.add(Finding(id="no-lang", severity="minor", title="Missing <html lang>",
                           detail="No language declared.", remediation='Add lang, e.g. <html lang="en-GB">.', count=1))
    if not soup.find("title"):
        report.add(Finding(id="no-title", severity="moderate", title="Missing <title>",
                           detail="No document title.", remediation="Add a descriptive <title>.", count=1))


STATIC_CHECKS = [
    check_duplicate_main, check_invalid_lists, check_label_in_name,
    check_aria_role_overrides, check_th_scope, check_generic_links,
    check_missing_alt, check_unnamed_interactive, check_headings,
    check_structured_data, check_basics,
]


# ── runtime checks (Playwright) ─────────────────────────────────────────────
def check_render(url: str, report: Report, basic_auth: Optional[str], timeout: int):
    """Load in headless Chromium: detect tree-hollowing + run axe-core."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        report.notes.append("Playwright not installed — skipping runtime checks. "
                            "Install: pip install playwright && playwright install chromium")
        return

    creds = None
    if basic_auth and ":" in basic_auth:
        u, p = basic_auth.split(":", 1)
        creds = {"username": u, "password": p}

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(http_credentials=creds, viewport={"width": 1280, "height": 940})
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=timeout)
        report.rendered = True

        # 1) Tree-hollowing: innerText length + empty-in-tree headings before vs after scroll.
        before = page.evaluate("() => (document.querySelector('main')||document.body).innerText.length")
        empty_before = page.evaluate(
            "() => [...document.querySelectorAll('h1,h2,h3,summary')]"
            ".filter(h => h.textContent.trim() && !h.innerText.trim()).length")
        page.evaluate("""async () => {
            for (let y=0; y<=document.body.scrollHeight; y+=800){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,40)); }
            window.scrollTo(0, document.body.scrollHeight); await new Promise(r=>setTimeout(r,300));
        }""")
        after = page.evaluate("() => (document.querySelector('main')||document.body).innerText.length")

        if empty_before > 0 or (before and after / max(before, 1) > 1.5 and after - before > 1500):
            report.add(Finding(
                id="render-hollowing-confirmed", severity="critical",
                title="Confirmed: body content is absent from the tree until scrolled",
                detail=(f"Rendered text grew {before}->{after} chars on scroll; "
                        f"{empty_before} heading(s)/summary had text in the DOM but were empty in the "
                        "accessibility tree at load. An agent that doesn't scroll sees a hollow page."),
                remediation="Same as lazy-render-hollowing: disable the render-deferral (WP Rocket LRC / content-visibility:auto).",
                count=max(empty_before, 1),
            ))

        # 2) axe-core for WCAG violations (contrast etc.) that need a real render.
        try:
            page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js")
            res = page.evaluate("async () => await axe.run(document, {resultTypes:['violations']})")
            order = {"critical": "critical", "serious": "serious", "moderate": "moderate", "minor": "minor"}
            for v in res.get("violations", []):
                report.add(Finding(
                    id=f"axe-{v['id']}", severity=order.get(v.get("impact"), "moderate"),
                    title=f"axe: {v['help']}",
                    detail=f"{len(v['nodes'])} node(s). {v['description']}",
                    remediation=v.get("helpUrl", ""),
                    count=len(v["nodes"]),
                    samples=[n.get("target", [""])[0] for n in v["nodes"][:4]],
                ))
        except Exception as e:
            report.notes.append(f"axe-core unavailable ({e}); ran structural runtime checks only.")

        browser.close()


# ── llms.txt (agent context file) ───────────────────────────────────────────
def check_llms_txt(url: str, report: Report, basic_auth):
    from urllib.parse import urlsplit
    parts = urlsplit(url)
    auth = tuple(basic_auth.split(":", 1)) if basic_auth and ":" in basic_auth else None
    try:
        r = requests.get(f"{parts.scheme}://{parts.netloc}/llms.txt", auth=auth, timeout=15)
        ok = r.status_code == 200 and r.text.lstrip().startswith("#") and "text" in r.headers.get("content-type", "")
        report.notes.append(f"/llms.txt: {'present & valid' if ok else f'missing/invalid (HTTP {r.status_code})'}")
        if not ok:
            report.add(Finding(
                id="no-llms-txt", severity="minor",
                title="No valid /llms.txt",
                detail="An /llms.txt gives AI agents a curated map of the site.",
                remediation="Publish /llms.txt (Markdown: # Title, > summary, sectioned links).",
                count=1,
            ))
    except Exception as e:
        report.notes.append(f"/llms.txt check failed: {e}")


# ── orchestrator ────────────────────────────────────────────────────────────
def audit_url(url: str, basic_auth: Optional[str] = None, render: bool = True,
              timeout: int = 30000) -> Report:
    report = Report(url=url)
    headers = {"User-Agent": "AccessibilityAudit/1.0 (+AI-agent-readability)"}
    auth = tuple(basic_auth.split(":", 1)) if basic_auth and ":" in basic_auth else None
    resp = requests.get(url, headers=headers, auth=auth, timeout=30)
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    check_lazy_render(html, report)
    for chk in STATIC_CHECKS:
        chk(soup, report)
    check_llms_txt(url, report, basic_auth)
    if render:
        check_render(url, report, basic_auth, timeout)
    return report


# ── reporting ───────────────────────────────────────────────────────────────
_SEV_ORDER = ["critical", "serious", "moderate", "minor"]


def print_report(report: Report):
    # ASCII-only output so it never crashes a Windows cp1252 console.
    print("\n" + "=" * 70)
    print(f"AI AGENT READABILITY AUDIT  --  {report.url}")
    print("=" * 70)
    print(f"SCORE: {report.score}/100   ({'rendered' if report.rendered else 'static only'}, "
          f"{len(report.findings)} finding type(s))")
    for note in report.notes:
        print(f"  note: {note}")
    for sev in _SEV_ORDER:
        group = [f for f in report.findings if f.severity == sev]
        if not group:
            continue
        print(f"\n-- {sev.upper()} ({len(group)}) " + "-" * (60 - len(sev)))
        for f in group:
            print(f"  [{f.id}] {f.title}  (x{f.count})")
            print(f"      {f.detail}")
            if f.samples:
                print(f"      e.g. {f.samples[:4]}")
            print(f"      FIX: {f.remediation}")
    if not report.findings:
        print("\n  No agent-readability issues detected.")
    print()


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="AI Agent Readability & Accessibility audit for a URL.")
    ap.add_argument("--url", required=True, help="Page URL to audit")
    ap.add_argument("--basic-auth", help="user:pass for HTTP basic auth (e.g. WP Engine staging)")
    ap.add_argument("--no-render", action="store_true", help="Skip the headless-browser runtime checks")
    ap.add_argument("--json", metavar="PATH", help="Write the full report as JSON")
    ap.add_argument("--timeout", type=int, default=30000, help="Render timeout (ms)")
    args = ap.parse_args(argv)

    report = audit_url(args.url, basic_auth=args.basic_auth,
                       render=not args.no_render, timeout=args.timeout)
    print_report(report)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"url": report.url, "score": report.score, "rendered": report.rendered,
                       "notes": report.notes, "findings": [asdict(f) for f in report.findings]},
                      fh, indent=2)
        print(f"JSON written to {args.json}")
    # non-zero exit if any critical/serious finding — useful in CI
    sys.exit(1 if any(f.severity in ("critical", "serious") for f in report.findings) else 0)


if __name__ == "__main__":
    main()
