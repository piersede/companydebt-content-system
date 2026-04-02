# Editorial Operator Playbook

## Non-Negotiable Workflow Rules
- Start a new Claude thread for each article or page.
- Start a new thread for each major rewrite.
- Keep research, drafting, revision, and system work in separate threads.
- Point Claude at the exact page or file, not the whole repo.
- Use the compact runtime path by default. Canonical governance is for ambiguity, auditing, or maintenance only.

## Recommended Entry Commands
- `python scripts/editorial_task_entry.py --page <slug> --task draft`
- `python scripts/editorial_task_entry.py --page <slug> --task review`
- `python scripts/prepare_revision_packet.py --page <slug> --task rewrite --notes <note-file>`
- `python scripts/measure_workflow_tokens.py --page <slug> --task draft --inputs <file>`

## Research Discipline
- Distill raw research before drafting.
- Preferred outputs:
- `research/distilled/<slug>-research-summary.md`
- `research/distilled/<slug>-claims-to-verify.json`
- `research/distilled/<slug>-decision-brief.md`
- Use `python scripts/distill_research.py --slug <slug> <source-files...>` to create them.

## Revision Discipline
- Rewrite from the revision packet, not from the whole repo context.
- Reopen canon only if the notes expose a genuine conflict or quality-risk question.
- Preserve the human-authorship layer while changing only the sections that need work.

## Token-Survival Rule
- If the thread is becoming long, end it and start a fresh one rather than carrying accumulated history.
