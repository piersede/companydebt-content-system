# Checkpoint Workflow for Large Refactors

## When to use this workflow

Apply explicit checkpointing whenever:
- architecture refactors
- multi-file system changes
- content system rewrites
- design-system overhauls
- any task where failure would otherwise only become visible near the end

## Required behaviour

- Break major refactors into isolated files, modules, or tightly scoped units of work
- Define a clear exit criterion for each unit before work begins
- Complete one unit at a time
- Verify each unit before moving to the next
- Do not allow the agent to summarise a long multi-part change as if it were one task
- Require visible intermediate proof of progress at each checkpoint

## Why

Agents are usually competent at individual tasks but degrade badly on large-scale work when the feedback loop is too slow. Explicit checkpointing keeps the work inspectable, reduces silent drift, and forces the agent to show what it has actually completed rather than compressing a long operation into a vague end-summary.

## Preferred shape

1. Identify the set of files or modules being changed
2. Define the success condition for the first unit
3. Complete and verify that unit
4. Move to the next unit only after verification passes
5. Continue until the full refactor is complete

## Verification at each checkpoint

Verification means one of:
- running a relevant script and showing the output
- reading the changed file and confirming the edit is correct
- running a diff to show what changed
- showing a before/after comparison

"I updated the file" is not verification. The proof must be visible.
