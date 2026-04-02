You are operating inside Company Debt's Editorial Operating System v2.4.

All editorial rules live in `/editorial-os/`. Load `/editorial-os/CLAUDE.md` as the primary instruction set — it contains the full writing rules, workflow, and staging-push gate.

This file adds only the rules that are NOT in the editorial-os directory.

---

## Credit card page build rules

When building or modifying credit card pages via `cc_builder`:

1. **H2s: keywords but natural.** H2s should read as chapter titles — clear, sharp, reader-first. Include a topic keyword where it reads naturally, but don't force the full keyword phrase into every H2. The page context already establishes the topic. See Signal 5a in `18-seo-signal-governance.md`.

2. **Build quality gate runs automatically.** `build_page.py` runs `cc_builder/quality_checks.py` on every build. FAIL-level violations block `--publish`. There is no bypass flag.

3. **When creating or editing page configs:**
   - H2s should be contextually relevant chapter titles (advisory, not a hard gate)
   - Images must have `loading="lazy"` (except above-fold hero), `width`, `height`, and `alt`
   - No heading level skips (h2→h4). Use styled divs for component labels.
   - Interactive elements must have ARIA attributes and keyboard support
   - No inline `onclick` handlers. Use event listeners in JS blocks.
   - JSON-LD structured data required on every page
   - Three-tier affiliate disclosure required on every page

4. **When the build quality gate fails:** Fix the violations, do not bypass or suppress the check. The gate exists to prevent regressions.
