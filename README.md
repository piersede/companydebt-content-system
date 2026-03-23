# Company Debt Content System

Private repository for the Company Debt editorial operating system, powering content on [companydebt.co.uk](https://companydebt.co.uk/).

---

## What's in this repo

The editorial system has six major components:

1. **Core editorial workflow** — 22 governance files covering voice, evidence, structure, readability, comparisons, failure modes, and pre-publish checks. This is the main content engine. (`editorial-os/01` through `18`)
2. **Editorial image evidence system** — claim-then-verify visual strategy, proof visual types, capture standards, metadata and SEO protocol for all images. (`editorial-os/19`)
3. **Build-time quality gate** — automated checks that run on every page build. FAIL-level violations block publishing. Covers heading hierarchy, image attributes, accessibility, JSON-LD, affiliate disclosure, and link safety. (`editorial-os/20`)
4. **WordPress technical build quality** — 100-point scoring rubric across 8 categories for auditing WordPress engineering. Includes WP-CLI, HTTP, and database evidence playbooks. (`editorial-os/21`)
5. **Google search quality evaluator guidelines** — 12-agent audit system based on Google's 182-page QRG. Covers YMYL, E-E-A-T, page quality rating (Lowest through Highest), and Needs Met scoring. Standalone — not part of the core workflow, invoked manually. (`editorial-os/22`)
6. **Credit card page builder** — Python build system for generating credit card comparison and review pages, with 4 page types (roundup, review, brand_compare, guide). (`scripts/cc_builder/`)

---

## Full system map

Use this to find exactly where to go. It answers: "What does each part do, and where do I go to change it?"

```
editorial-os/
│
├── CORE EDITORIAL WORKFLOW ─── how we write and publish content
│   ├── 01  Master methodology        ← north star, principles, article structures
│   ├── 03  Workflow playbook          ← 9-stage pipeline (brief → publish)
│   ├── 17  Audience and persona       ← who we write for
│   └── 06  Prompt library             ← reusable prompts for each workflow stage
│
├── VOICE & WRITING RULES ──── how content should sound
│   ├── 09  Voice governance           ← authorship, first person, tone, vendor perspective
│   ├── 13  Readability governance     ← paragraphs, formatting, em dashes, emphasis
│   ├── 12  Structure governance       ← openings, endings, section discipline, templates
│   └── docs/human-authorship-voice-engine.md  ← Rules A-J (the humanisation engine)
│
├── TRUST & EVIDENCE ────────── how we handle facts, claims, and comparisons
│   ├── 10  Evidence governance        ← claim labels, sourcing, hedging rules
│   ├── 11  Comparison governance      ← competitor claims, frameworks, pricing, disclosure
│   ├── 04  Trust architecture         ← trust signals and infrastructure
│   └── 08  Red line library           ← hard boundaries that cannot be crossed
│
├── QUALITY GATES ──────────── what blocks publication
│   ├── 16  Pre-publish gate           ← 14 checks, all must pass before publish
│   ├── 05  Scoring rubric             ← scoring criteria (trust T1-T6, alternatives A1-A8)
│   ├── 14  Failure modes & recovery   ← 27 failure modes including 13 AI prose fingerprints
│   ├── 15  Good vs bad examples       ← concrete examples for calibration
│   ├── 20  Build-time quality gate    ← automated HTML/accessibility/SEO checks (FAIL/WARN)
│   └── 23  Prose quality gates        ← 10 YMYL enforcement gates (fact pattern, meta-copy, source constraint, etc.)
│
├── IMAGES ─────────────────── how we use visuals as evidence
│   └── 19  Editorial image evidence   ← claim-then-verify, visual rhythm, capture standards
│
├── SEO ────────────────────── search signal governance
│   └── 18  SEO signal governance      ← 18 signals, S1-S12 pre-publish checklist, F1-F69 full audit
│
├── WORDPRESS ENGINEERING ──── technical build quality for the WP site
│   └── 21  WordPress technical build  ← 100-point rubric, 8 categories, evidence playbooks
│
├── SEARCH QUALITY AUDIT ───── standalone audit against Google's QRG
│   └── 22  Google search quality evaluator  ← 12-agent system, NOT part of core workflow
│
├── ARTICLE TYPE SPECS ─────── type-specific rules layered on top of core
│   ├── docs/article-types/review.md
│   ├── docs/article-types/comparison.md
│   ├── docs/article-types/roundup.md
│   └── docs/article-types/guide.md
│
├── TEMPLATES ──────────────── starter outlines for each content type
│   ├── templates/tool-review-outline.md
│   ├── templates/comparison-page-outline.md
│   ├── templates/alternatives-page-outline.md
│   ├── templates/category-explainer-outline.md
│   ├── templates/opinion-post-outline.md
│   ├── templates/workflow-guide-outline.md
│   ├── templates/article-brief-template.md
│   └── templates/source-grounding-template.md
│
├── ENFORCEMENT SCRIPTS ────── automated rule checks
│   ├── checklists/check_comparison_integrity.js
│   ├── checklists/check_trust_architecture.js
│   ├── checklists/check_intro_quality.js
│   └── checklists/check_human_tone.js
│
├── HUMAN PROCESS ──────────── checklists for manual review
│   ├── checklists/trust-pass-checklist.md
│   ├── checklists/adversarial-review-checklist.md
│   ├── checklists/final-qa-checklist.md
│   └── checklists/pre-staging-gate.md
│
└── SUPPORT FILES
    ├── 02  Skills architecture         ← agent skill definitions
    ├── 07  Human input map             ← where human judgement is required
    ├── rules-index.md                  ← one rule, one source of truth lookup
    └── docs/agent-workflow.md          ← how the AI agent uses this system
```

---

## How the parts connect

### Writing a new article
```
Start here:
  17 (audience) → 01 (methodology) → 03 (workflow) → article type template

While writing, consult:
  09 (voice) + 13 (readability) + 12 (structure) + human-authorship-voice-engine

For evidence:
  10 (evidence) + 11 (comparison, if applicable)

For images:
  19 (editorial image evidence)

Before publishing:
  16 (pre-publish gate) + 20 (build-time quality gate) + 18 (SEO signals)
```

### Auditing an existing page
```
Technical build quality:  21 (WordPress technical build)
Content quality:          22 (Google search quality evaluator) ← run manually, separate from core
Ranking investigation:    22 (agents cover E-E-A-T, YMYL, Needs Met)
```

### Modifying the system itself
```
Adding a new rule:         Find the existing governance file → extend it → update rules-index.md
Adding a new article type: Create docs/article-types/{type}.md → add template → update 01
Adding a new quality check: Add to scripts/cc_builder/quality_checks.py → document in 20
Changing voice/tone:       09 (voice) + docs/human-authorship-voice-engine.md
Changing evidence rules:   10 (evidence)
Changing comparison rules: 11 (comparison)
```

---

## Quick reference: "I need to change..."

| What you want to change | Go to |
|---|---|
| How articles sound (tone, voice, first person) | `09-voice-governance.md` + `docs/human-authorship-voice-engine.md` |
| How we handle facts and claims | `10-evidence-governance.md` |
| How comparisons and competitor mentions work | `11-comparison-governance.md` |
| How articles are structured (openings, sections) | `12-structure-governance.md` |
| Formatting rules (paragraphs, emphasis) | `13-readability-governance.md` |
| What blocks publication | `16-pre-publish-gate.md` |
| SEO requirements | `18-seo-signal-governance.md` |
| Image standards and visual evidence | `19-editorial-image-evidence.md` |
| Automated build checks | `20-build-time-quality-gate.md` + `quality_checks.py` |
| WordPress engineering standards | `21-wordpress-technical-build-quality.md` |
| Google quality audit process | `22-google-search-quality-evaluator.md` |
| Who we write for | `17-audience-and-persona.md` |
| Article type-specific rules | `docs/article-types/{review,comparison,roundup,guide}.md` |
| Starter templates for new articles | `templates/` |
| Rule lookup (which file owns which rule) | `rules-index.md` |
| Failure patterns to avoid | `14-failure-modes-and-recovery.md` |
| What good and bad writing looks like | `15-good-vs-bad-examples.md` |

---

## Key boundaries

- **22 (Google search quality evaluator)** is a standalone audit tool. It does NOT run as part of the normal writing or publishing workflow. Invoke it manually for YMYL pages, ranking drops, or periodic reviews.
- **20 (build-time quality gate)** runs automatically on every page build. You cannot bypass it.
- **16 (pre-publish gate)** is a human-reviewed checklist. Every article must pass all 14 checks.
- **rules-index.md** is the single lookup for "which file owns this rule." If you add a rule, register it there.

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/piersede/companydebt-content-system.git
cd companydebt-content-system
```

### 2. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 3. Open the project

```bash
claude
```

Claude automatically loads `CLAUDE.md`, which contains all editorial system instructions. The governance files in `editorial-os/` are referenced from there.

---

## Other top-level files

| File | Purpose |
|---|---|
| `CLAUDE.md` | System instructions loaded automatically by Claude Code |
| `scripts/` | Build scripts including `cc_builder/` for credit card pages |
| `editorial-os/SYSTEM-MAP.md` | Full copy of this system map (also lives inside editorial-os/) |

---

Questions? Ask Piers or open an issue.
