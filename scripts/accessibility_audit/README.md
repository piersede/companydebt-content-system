# AI Agent Readability & Accessibility Audit

Audits a URL for how well **AI agents** (and assistive technology) can read and
operate it. The key insight: agents read the **rendered accessibility tree**, not
your source HTML or your design. A page can look perfect to humans and be a maze
to an agent — content hidden from the tree, controls with no names, pricing
locked in images, links that all say "view deal".

This tool was built from a real remediation where the **entire article body was
invisible to agents** because a caching plugin deferred off-screen rendering.
That root cause and its fix are baked into the checks and the playbook below.

## Install

```bash
pip install requests beautifulsoup4
# optional but recommended — enables the runtime (browser) checks:
pip install playwright && playwright install chromium
```

## Usage

```bash
# from the scripts/ directory
python -m accessibility_audit --url https://example.com/some-page/

# staging behind WP Engine HTTP basic auth
python -m accessibility_audit --url https://stg.example.com/page/ --basic-auth user:pass

# static checks only (no browser), machine-readable output
python -m accessibility_audit --url https://example.com/ --no-render --json report.json
```

Exit code is **1** if any critical/serious finding is present (CI-friendly).

## What it checks

**Static (served HTML — always run):**

| Check | Severity | Why it matters to an agent |
|---|---|---|
| `lazy-render-hollowing` | critical | `data-wpr-lazyrender` / `content-visibility:auto` defers content out of the tree until scrolled |
| `duplicate-main` | serious | Multiple `<main>` landmarks — can't tell which is the primary region |
| `label-in-name` | serious | `aria-label` doesn't contain the visible text (WCAG 2.5.3) — breaks voice control + diverges the agent's view |
| `unnamed-interactive` | serious | Buttons/links with no accessible name — can't be identified or invoked |
| `missing-alt` | serious/moderate | Images (esp. in tables) with no alt = data/pricing locked in an image |
| `invalid-list` | moderate | `<ul>`/`<ol>` with non-`<li>` children — mis-announced |
| `inappropriate-role` | moderate | e.g. `<aside role="navigation">` instead of `<nav>` |
| `generic-link-text` | moderate | "click here", "view deal", "details" — meaningless out of context |
| `no-structured-data` | moderate | No JSON-LD — the machine-readable layer answer engines consume |
| `h1-count` / `heading-skips` | moderate/minor | Topic clarity + document outline |
| `th-scope` | minor | `<th>` without `scope` — can't bind cells to headers |
| `no-lang` / `no-title` / `no-llms-txt` | minor | Basic agent context |

**Runtime (headless Chromium, if Playwright is installed):**

- **`render-hollowing-confirmed`** — *the headline check.* Measures rendered text
  length and counts headings/`<summary>` that have text in the DOM but are **empty
  in the accessibility tree at load**, then scrolls and re-measures. A large jump
  (e.g. 2.9k → 17k chars) is the signature of content being hidden from agents.
- **axe-core** — full WCAG violation scan (colour contrast, ARIA, names, etc.)
  that needs a real render. Injected from CDN.

## Remediation playbook (from the original fix)

### 1. Content hollowed from the tree (the big one)
Most often **WP Rocket "Lazy Render Content"**: it tags blocks with
`data-wpr-lazyrender` and applies `content-visibility:auto`, skipping off-screen
rendering. There is **no settings toggle** in WP Rocket 3.20 — disable via filter:

```php
add_filter( 'rocket_lrc_optimization', '__return_false' );
```

CSS backstop (git-tracked, survives plugin updates, reaches every environment):

```css
[data-wpr-lazyrender] { content-visibility: visible !important; }
```

Then **purge the page cache**. Generic rule: never put `content-visibility:auto`
on a wrapper that holds the whole article — it's meant for many small repeated
off-screen items, not one giant container.

### 2. Duplicate `<main>`
Keep exactly one `<main>` landmark. If a template opens `<main id="primary">` and
the content wrapper is also `<main>`, demote the inner one to `<div>` (style by
class, not tag).

### 3. Sidebar / TOC as `<aside role="navigation">`
A table of contents *is* navigation — use a `<nav aria-label="...">`, not an
`<aside>` with an overridden role. (Lighthouse's agentic audit flags the override.)

### 4. Label-in-Name (WCAG 2.5.3)
If a button shows "View Deal" but needs a per-item name, the accessible name must
**contain** the visible text: `aria-label="View Deal, Tide"` — not
`"View Tide deal"` (which omits "View Deal").

### 5. Tables
Real `<table>` + `<th scope="col">`. A site-wide fix is to normalise bare `<th>`
at build time:
`re.sub(r'<th(?=[\s>])(?![^>]*\bscope=)', '<th scope="col"', html)`.

### 6. Contrast
Small UI labels (badges, pills, stat labels) are the usual culprits — verify text
clears **4.5:1** (normal) against its actual background.

## Auditing live pages — gotchas

- **Cache variance.** Cached pages (WP Rocket / Cloudflare) can serve different
  HTML between requests — sometimes with the lazy-render markers, sometimes a
  regenerated variant without. Audit against origin, or purge + re-fetch, when a
  result looks inconsistent.
- **Staging auth.** Pass `--basic-auth user:pass` for WP Engine nginx auth.
- **Lighthouse "Agentic Browsing".** This tool complements Lighthouse's new
  Agentic Browsing category (and Accessibility). Its `agent-accessibility-tree`
  audit fails on exactly the issues above; cross-check with Chrome DevTools.
- **`/llms.txt`.** Lighthouse's `llms-txt` sub-fetch fails on basic-auth staging
  even when the file is valid — verify on the public origin.
