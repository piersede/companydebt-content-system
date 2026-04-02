# Token Optimization Implementation Plan

## Goal

Move Company Debt from a governance-heavy prompt architecture to a lean runtime architecture without losing any editorial quality.

## Phase 1: Instruction topology

- reduce root `CLAUDE.md` to universal rules and routing only
- reduce `editorial-os/CLAUDE.md` to canonical ownership and escalation guidance
- add local `CLAUDE.md` files in `scripts/`, `scripts/cc_builder/`, `research/`, `preview/`, and `docs/`

Exit criteria:

- root instructions are lean
- canonical governance remains intact
- local routing is explicit

## Phase 2: Runtime packs

Add:

- `runtime-packs/writer-core.md`
- `runtime-packs/review-core.md`
- `runtime-packs/build-core.md`
- `runtime-packs/research-core.md`
- `runtime-packs/deploy-core.md`
- article overlays for review, comparison, roundup, guide, and alternatives
- stage packs for brief, source-grounding, outline, draft, trust-pass, adversarial-review, and final-polish

Exit criteria:

- routine editorial tasks can run from compact packs
- human-authorship markers remain explicit in execution context

## Phase 3: Routing and workflow wiring

- add `scripts/runtime_pack_router.py`
- expose runtime context from `scripts/build_page.py`
- update docs so the system decides default context automatically

Exit criteria:

- humans are not asked to choose packs for normal work
- runtime context is inspectable and deterministic

## Phase 4: Research prompt efficiency

- add shared prompt helpers
- refactor research scripts to build prompts from structured sections rather than long repeated prose

Exit criteria:

- research prompts are easier to maintain
- prompt duplication is reduced

## Phase 5: Benchmark and quality enforcement

- add `benchmarks/runtime-pack-benchmark-set.json`
- add `scripts/benchmark_runtime_packs.py`
- encode the non-compressible human-authorship checklist in benchmark docs

Exit criteria:

- token savings are measurable
- human-authorship safeguards are explicit
- future reductions can be rejected if they flatten the work
