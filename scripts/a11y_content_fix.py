"""Per-page CONTENT-layer accessibility fixes (heading re-tag, generic-link
aria-labels, empty-heading removal) applied via the WP REST API on staging.

Reuses the authenticated session + post resolver from staging_edit.py. Edits the
RAW stored block content (context=edit) and PATCHes it back. Dry-run by default;
pass --apply to write. Every applied edit first saves the original raw to
tmp/a11y_content_bak/<slug>.html for reversibility (WP also keeps a revision).

Recipes are explicit per page (auditable). Each recipe is a list of steps:
  {"kind":"regex"|"literal", "find":..., "repl":..., "expect":N (optional)}
A step whose match count != expect aborts the page (nothing written) so a
changed template/markup can never silently mis-edit.

Usage:
  python scripts/a11y_content_fix.py --page am-i-solvent            # dry run
  python scripts/a11y_content_fix.py --page am-i-solvent --apply
  python scripts/a11y_content_fix.py --group qa --apply             # all quick-answer pages
  python scripts/a11y_content_fix.py --all                          # dry run everything
"""
import argparse
import importlib.util
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))   # so `scripts.accessibility_audit` imports work
_spec = importlib.util.spec_from_file_location("se", str(ROOT / "scripts" / "staging_edit.py"))
se = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(se)

BAK = ROOT / "tmp" / "a11y_content_bak"

# ── reusable step builders ──────────────────────────────────────────────────
# Quick-answer article pages: the single intro "Quick answer ..." callout is an
# <h3> sitting before the <h2> body sections (h1->h3 skip). Promote ONLY that
# block to h2. Anchored on "Quick answer" so a legitimate sub-section h3 elsewhere
# on the page is untouched. Two steps: (1) flip the <h3> tag itself (required —
# this is what the rendered audit reads); (2) flip the preceding wp:heading block
# comment level 3->2 where it exists (some pages have a malformed block with no
# opening comment, so no expect).
QA_STEPS = [
    {
        "kind": "regex",
        "find": r'<h3 class="wp-block-heading">(Quick answer[^<]*)</h3>',
        "repl": r'<h2 class="wp-block-heading">\1</h2>',
        "expect": 1,
    },
    {
        "kind": "regex",
        "find": r'<!-- wp:heading \{"level":3\} -->(\s*)<h2 class="wp-block-heading">Quick answer',
        "repl": r'<!-- wp:heading {"level":2} -->\1<h2 class="wp-block-heading">Quick answer',
    },
]

# Hub pages: section headings are <h3> and the link-card titles are
# <span class="cd-hub-card__title">. The h1->h3 skip comes from the theme
# promoting those card spans to <h4> (a the_content filter that ONLY matches
# spans). Fix:
#   - sections h3 -> h2  (h1 -> h2, sequential)
#   - card span -> <div class="cd-hub-card__title">  (NOT a heading)
# Using <div> (a) bypasses the theme's span->h4 filter, (b) keeps the cards OUT
# of the heading outline so there is no card-level skip, and (c) avoids the
# theme's .entry-content h3 typography (24px/40px-margin, !important) clobbering
# the compact .cd-hub-card__title style - a <div> takes the class's 15px and has
# no default margin, matching the original span. Net heading outline: h1 -> h2.
SECTION_STEP = {
    "kind": "regex",
    "find": r'<!-- wp:heading \{"level":3\} -->(\s*)<h3 class="wp-block-heading">([^<]*)</h3>',
    "repl": r'<!-- wp:heading {"level":2} -->\1<h2 class="wp-block-heading">\2</h2>',
}
CARD_STEP = {
    "kind": "regex",
    "find": r'<span class="cd-hub-card__title">(.*?)</span>',
    "repl": r'<div class="cd-hub-card__title">\1</div>',
}
# Repair step for the first pass, which converted cards to <h3 ... style="margin:0">
# before the theme-h3 typography clash was caught. Converts those to <div>.
CARD_REPAIR_STEP = {
    "kind": "regex",
    "find": r'<h3 class="cd-hub-card__title" style="margin:0">(.*?)</h3>',
    "repl": r'<div class="cd-hub-card__title">\1</div>',
}


def hub_steps(sections, cards):
    return [dict(SECTION_STEP, expect=sections), dict(CARD_STEP, expect=cards)]


def hub_repair_steps(cards):
    return [dict(CARD_REPAIR_STEP, expect=cards)]


RECIPES = {
    # ---- group: qa (quick-answer article pages) ----
    "am-i-solvent":                           {"group": "qa", "url": "/liquidation/am-i-solvent/", "steps": QA_STEPS},
    "business-bank-account-in-liquidation":   {"group": "qa", "url": "/liquidation/business-bank-account-in-liquidation/", "steps": QA_STEPS},
    "bailiffs-high-court-enforcement-officers":{"group": "qa", "url": "/liquidation/bailiffs-high-court-enforcement-officers/", "steps": QA_STEPS},
    "can-a-supplier-force-my-company-into-liquidation": {"group": "qa", "url": "/liquidation/can-a-supplier-force-my-company-into-liquidation/", "steps": QA_STEPS},
    "can-a-director-be-sued-personally-by-creditors":   {"group": "qa", "url": "/liquidation/can-a-director-be-sued-personally-by-creditors/", "steps": QA_STEPS},

    # ---- group: hub (first pass: sections h3->h2, cards span->div) ----
    "advice":                  {"group": "hub", "url": "/advice/", "steps": hub_steps(6, 31)},
    "bounce-back-loan-support-hub": {"group": "hub", "url": "/bounce-back-loan-support-hub/", "steps": hub_steps(2, 6)},
    "sample-letters":          {"group": "hub", "url": "/sample-letters/", "steps": hub_steps(2, 8)},

    # ---- group: hubrepair (convert already-applied <h3> cards to <div>) ----
    "advice-repair":           {"group": "hubrepair", "url": "/advice/", "steps": hub_repair_steps(31)},
    "bounce-back-repair":      {"group": "hubrepair", "url": "/bounce-back-loan-support-hub/", "steps": hub_repair_steps(6)},
    "sample-letters-repair":   {"group": "hubrepair", "url": "/sample-letters/", "steps": hub_repair_steps(8)},

    # ---- group: misc content ----
    # Empty heading -> remove (fixes h1->h3 skip; an empty <h3> names nothing).
    "articles-insights-hub":   {"group": "misc", "url": "/business-insolvency/articles-insights-hub/",
                                 "steps": [{"kind": "literal", "find": '<h3 class="box-heading"></h3>', "repl": "", "expect": 1}]},

    # ---- group: stats (uk-insolvency-statistics data hub, rendered axe) ----
    # (a) axe-definition-list: <dl class="cd-meta-grid"> has <div><span><strong>
    #     children, not dt/dd. It's a styled key/value grid, not a real
    #     definition list -> demote to <div> (all styling is on .cd-meta-grid /
    #     .cd-meta-item classes, so rendering is unchanged).
    # (b) axe-aria-required-children: <div role="tablist"> owns aria-pressed
    #     toggle <button>s, not role="tab" children. They are a labelled set of
    #     view-toggle buttons -> role="group" (no required children, keeps the
    #     aria-label="Time range" grouping and the aria-pressed toggle pattern).
    "uk-insolvency-statistics": {"group": "stats", "url": "/uk-insolvency-statistics/", "steps": [
        {"kind": "regex", "find": r'<dl class="cd-meta-grid">(.*?)</dl>',
         "repl": r'<div class="cd-meta-grid">\1</div>', "expect": 1},
        {"kind": "literal", "find": '<div class="cd-chart-controls" role="tablist"',
         "repl": '<div class="cd-chart-controls" role="group"', "expect": 1},
    ]},
}

# Landmark-unique batch (site-wide content asides). Article pages carry two
# stored <aside> blocks - .cd-methodology and .cd-sources - both unnamed
# complementary landmarks. With the theme sidebar (.widget-area, also
# complementary) that is three unnamed complementary landmarks colliding
# (axe-landmark-unique). Naming BOTH content asides leaves only the single
# template .widget-area, which is then unique. (The two TOC navs share a name but
# only one is in the a11y tree per breakpoint, so they don't collide.) Additive +
# idempotent. .widget-area itself is template, out of the content layer.
ASIDE_LABELS = [
    ('<aside class="cd-methodology">', '<aside class="cd-methodology" aria-label="Methodology">'),
    ('<aside class="cd-sources">', '<aside class="cd-sources" aria-label="Sources">'),
]

STAGING = se.STAGING_URL


def apply_steps(raw, steps):
    out, counts = raw, []
    for st in steps:
        if st["kind"] == "regex":
            new, n = re.subn(st["find"], st["repl"], out, flags=re.DOTALL)
        else:
            n = out.count(st["find"])
            new = out.replace(st["find"], st["repl"])
        counts.append(n)
        if "expect" in st and n != st["expect"]:
            return None, counts, f'step matched {n}, expected {st["expect"]}'
        out = new
    return out, counts, None


def run_page(s, slug, rec, apply):
    url = STAGING + rec["url"]
    res = se.resolve_post(s, url)
    if not res:
        print(f"[{slug}] NOT_FOUND {url}")
        return False
    ep, pid, _slug, link, raw = res
    new, counts, err = apply_steps(raw, rec["steps"])
    tag = f"[{slug}] ({ep}/{pid}) steps={counts}"
    if err:
        print(f"{tag}  ABORT: {err}")
        return False
    if new == raw:
        print(f"{tag}  no change (already fixed?)")
        return True
    if not apply:
        print(f"{tag}  OK dry-run (+{len(new)-len(raw)} chars) — pass --apply")
        return True
    BAK.mkdir(parents=True, exist_ok=True)
    (BAK / f"{slug}.html").write_text(raw, encoding="utf-8")
    code = se.patch(s, ep, pid, new)
    print(f"{tag}  PATCH {code}  (backup tmp/a11y_content_bak/{slug}.html)")
    return True


def run_methodology(s, apply, limit=None):
    """Give every stored .cd-methodology / .cd-sources <aside> a unique aria-label
    across the whole sitemap (axe-landmark-unique). Idempotent."""
    from scripts.accessibility_audit.sweep import _real_pages
    refs = _real_pages()
    if limit:
        refs = refs[:limit]
    done = skipped = 0
    for r in refs:
        try:
            res = se.resolve_post(s, "https://comdebstage.wpengine.com" + r.path)
        except Exception:
            continue
        if not res:
            continue
        ep, pid, _slug, link, raw = res
        new = raw
        for find, repl in ASIDE_LABELS:
            new = new.replace(find, repl)
        if new == raw:
            if 'cd-methodology" aria-label' in raw or 'cd-sources" aria-label' in raw:
                skipped += 1   # asides present but already labelled
            continue
        if not apply:
            print(f"  would fix {ep}/{pid}  {r.path}")
            done += 1
            continue
        BAK.mkdir(parents=True, exist_ok=True)
        (BAK / f"landmark_{pid}.html").write_text(raw, encoding="utf-8")
        code = se.patch(s, ep, pid, new)
        print(f"  PATCH {code}  {ep}/{pid}  {r.path}")
        done += 1
    print(f"\nlandmark asides: {done} {'fixed' if apply else 'to fix'}, {skipped} already labelled")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    ap.add_argument("--group")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--methodology", action="store_true", help="batch: aria-label all cd-methodology asides")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    s = se.session()

    if a.methodology:
        run_methodology(s, a.apply, a.limit)
        return

    if a.page:
        pages = [a.page]
    elif a.group:
        pages = [k for k, v in RECIPES.items() if v["group"] == a.group]
    elif a.all:
        pages = list(RECIPES)
    else:
        ap.error("specify --page, --group, --methodology, or --all")

    for slug in pages:
        rec = RECIPES.get(slug)
        if not rec:
            print(f"[{slug}] no recipe"); continue
        run_page(s, slug, rec, a.apply)


if __name__ == "__main__":
    main()
