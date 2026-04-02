Use this directory for implementation and workflow tooling.

Focus:

- build and publish scripts
- runtime-pack routing
- benchmarks
- research helpers

Rules:

- script changes must preserve editorial quality, not just pass mechanically
- keep prompts structured and reusable where possible
- prefer shared prompt builders over repeated prose-heavy prompt blobs
- if a script changes what context is loaded, benchmark the savings and check human-authorship safeguards
- script changes must preserve the always-on quality kernel for article work, even when they reduce routing overhead
- default Claude-side entrypoints here are `editorial_task_entry.py`, `distill_research.py`, `prepare_revision_packet.py`, and `measure_workflow_tokens.py`
