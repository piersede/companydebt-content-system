# Token Optimization Strategy

## Objective

Reduce token usage materially while preserving the full editorial standard, especially the human-authorship layer that makes Company Debt content feel authored, trustworthy, and alive.

## Core diagnosis

The quality problem is not the canonical editorial system. The quality problem is runtime delivery.

This repo has a strong canonical system:

- the human-authorship engine is detailed and high quality
- the voice governance is unusually sharp about false authority
- the workflow and trust gates are serious

The weakness is that too much of that system is being treated as always-on runtime context:

- the root `CLAUDE.md` is carrying a large execution burden
- drafting guidance, governance routing, and staging logic are mixed together
- humans are implicitly expected to know which parts of the system matter for a given task
- research prompts repeat a lot of prose that should be centralized

That architecture makes the system expensive, harder to steer, and more fragile than it needs to be.

## Strategic recommendation

Split the system into four layers:

1. Canonical governance
2. Local routing
3. Runtime packs
4. Benchmarks

### 1. Canonical governance

Keep `editorial-os/` as the source of truth.
Do not weaken the long-form rule system.
This is where quality lives.

Why this works:
Because the problem is not the standard itself. The problem is sending too much of the standard on every turn.

### 2. Local routing

Shrink the root `CLAUDE.md` into a universal routing layer under roughly 1,000 tokens.
Use subdirectory `CLAUDE.md` files to load context only when work enters that subtree.

Why this works:
It removes repetitive always-on instructions without removing the rules themselves.
It also makes the system easier to operate because routing becomes structural, not memory-based.

### 3. Runtime packs

Create compact execution packs for writing, review, research, build, and deploy work, plus article-type overlays and workflow-stage packs.

Why this works:
It preserves the editorial standard while dramatically reducing default prompt weight.
The runtime pack is not a weaker system. It is a compiled execution layer derived from the canonical system.

### 4. Benchmarks

Add a benchmark set and quality checklist that compare canonical-load assumptions to runtime-pack assumptions.

Why this works:
Token savings without benchmarked quality safeguards invite silent flattening.
The benchmark creates a hard rule: savings count only if the human-authorship model and decision usefulness remain intact.

## Human-authorship safeguard

This is the most important constraint in the whole optimization.

The following markers must be treated as non-compressible in execution layers:

- concrete scenes
- earned `you` and `we`
- operational friction
- evaluative bite
- rhythm and sentence texture
- asymmetrical editorial lines
- UK texture where natural
- moral clarity when warranted

Why this works:
These are not ornamental style choices. They are the markers that prevent the system from becoming technically correct but emotionally and editorially flat.

## Implementation order

1. Shrink root and local routing files
2. Add runtime packs
3. Wire routing into scripts and docs
4. Add benchmark and non-compressible human-authorship checklist
5. Refactor research prompt construction into shared helpers

## Success criteria

- materially lower fixed-context token load
- no loss of trust, sharpness, or human-authored feel
- humans no longer need to choose packs manually
- the system defaults to the smallest relevant context automatically
- future optimizations are blocked if they weaken human-authorship markers
