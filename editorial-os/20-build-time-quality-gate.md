# 20. Build-Time Quality Gate

See `scripts/cc_builder/quality_checks.py` for the automated implementation.

## 20.1 Purpose

The build-time quality gate runs automatically during every page build (`build_page.py`). It catches structural, accessibility, and SEO issues before content reaches staging or production. FAIL-level violations block the `--publish` flag. There is no bypass.

## 20.2 Automated checks

| Check | What it catches | Severity |
|---|---|---|
| H2 semantic relevance | H2s lacking topic keywords (advisory) | WARN |
| HTML parse | Malformed HTML that cannot be parsed | FAIL |
| Heading hierarchy | Heading level skips (e.g. h2 → h4) | FAIL |
| Image alt | Images missing `alt` attribute | FAIL |
| Image lazy loading | Non-hero images missing `loading="lazy"` | WARN |
| Image dimensions | Images missing `width`/`height` (CLS risk) | WARN |
| Inline onclick | CSP-unsafe inline event handlers | WARN |
| Link rel | `target="_blank"` without `rel="noopener"` | FAIL |
| ARIA minimum | Fewer than 2 ARIA attributes on interactive pages | WARN |
| CSS !important | More than 35 `!important` declarations | WARN |
| JSON-LD schema | No structured data found | FAIL |
| Disclosure | No affiliate disclosure found | FAIL |
| Info gain missing | No `info_gain` declarations in page config | FAIL |
| Info gain per H2 | Content H2 with no declared info gain element | FAIL |
| Info gain article minimum | Fewer than 3 total info gain elements declared | FAIL |
| Info gain format | Empty or too-short info gain element (<10 chars) | FAIL |
| Primary source | Competitor/aggregator site cited as product data source | FAIL |

## 20.3 Enforcement rules

1. Any FAIL-level violation blocks `--publish`. Fix the violation; do not suppress the check.
2. WARN-level violations are logged but do not block. Review and fix where practical.
3. H2 relevance is advisory only. H2s should read as natural chapter titles with gentle keyword inclusion, not keyword targets. See `18-seo-signal-governance.md` Signal 5a.
4. The quality gate runs after page assembly, before any staging push.

## 20.4 Information gain declarations

Every page config must include an `info_gain` dict that maps H2 section text to a list of strings describing what that section adds that competitors omit. This is the enforcement mechanism for §12 of `10-evidence-governance.md`.

### Format

```python
'info_gain': {
    'H2 Text Exactly As Written': [
        'Description of novel element (source: provider/regulator)',
        'Second novel element if present',
    ],
},
```

### Rules

- **Article minimum**: At least 3 total elements across all H2s
- **H2 minimum**: Every content H2 must have at least 1 element
- **Element quality**: Each element must be 10+ characters and describe what is novel and where it came from
- **Exempt H2s**: Methodology, disclosure, and navigation-only sections are exempt
- **Source requirement**: Elements based on data should cite the primary source (provider, regulator, or official body — never competitor sites)

### What qualifies as information gain

Per §12 of `10-evidence-governance.md`:
- A fact competitors usually omit
- A better explanation of why a fact matters
- A clearer recommendation tied to a specific user type
- A more exact trade-off than the current SERP norm
- First-hand testing detail or observed behaviour
- Original comparison logic or framework
- Sourced data from primary sources (providers, FCA, UK Finance, ONS)

### What does NOT qualify

- Restated SERP consensus
- Generic descriptions available on any comparison site
- Unsourced claims or editorial filler
- "Comprehensive" coverage that adds no evaluative insight

## 20.5 Primary source enforcement

The build gate scans all prose paragraphs and FAQ answers for competitor/aggregator sites being cited as product data sources. Banned sources include: MoneySupermarket, MoneySavingExpert, NerdWallet, Finder, Forbes Advisor, Uswitch, GoCompare, CompareTheMarket, and equivalents. See `10-evidence-governance.md` §7a for the full rule.

Mentions of competitor sites for rhetorical contrast (e.g. "most comparison sites bury this") are not flagged. Only citation patterns (e.g. "source: Finder UK", "according to NerdWallet") trigger the check.

## 20.6 Adding new checks

New checks are added to `scripts/cc_builder/quality_checks.py`. Each check must return a dict with `check` (identifier), `detail` (human-readable message), and `severity` (`FAIL` or `WARN`). Add the check to either `validate_h2_relevance()` (config-level) or `validate_build_quality()` (HTML-level), and document it in this section.
