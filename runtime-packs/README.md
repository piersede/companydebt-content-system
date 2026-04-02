# Runtime Packs

This directory contains compact execution-time instruction packs derived from the canonical editorial operating system.

Design rule:

- canonical governance in `editorial-os/` is the source of truth
- runtime packs are compact, task-specific execution layers
- local `CLAUDE.md` files route work into the right subtree
- the editorial system should decide the default runtime context, not the human operator

The goal is to avoid loading large governance documents by default during routine tasks while preserving the full editorial standard.

Pack families:

- `writer-core.md`
- `review-core.md`
- `build-core.md`
- `research-core.md`
- `deploy-core.md`
- article-type overlays
- workflow-stage packs

Non-compressible rule:

- do not thin out human-authorship markers in runtime packs
- token savings must come from removing duplication, excess routing, or irrelevant context
- token savings must not come from compressing concrete scenes, earned pronoun logic, friction, evaluative bite, rhythm, cultural texture, or moral clarity

Helpful commands:

- `python scripts/runtime_pack_router.py --task draft --page-type review --slug capital-on-tap-review`
- `python scripts/build_page.py --page capital-on-tap-review --show-runtime-packs --task draft`
- `python scripts/benchmark_runtime_packs.py`
