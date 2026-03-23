# Gemini Deep Research Workflow

## Overview

The BusinessExpert editorial system uses Google's Gemini Deep Research Agent for automated fact verification and data gathering. This document covers the complete workflow from prompt to resolved content.

## Architecture

```
research question → batched prompt → Deep Research Agent → structured output → parse → update page configs
```

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/gemini_research.py` | Standalone batched research | `python scripts/gemini_research.py --name "batch-name"` |
| `scripts/cc_builder/research.py` | Integrated card/page research | `python scripts/build_page.py --research-cards amex_business_gold,rbs` |
| `scripts/quality_check.py` | Pre-publish editorial checks | `python scripts/quality_check.py --verbose` |

### API Configuration

- **SDK:** `google-genai` (Python), installed via `pip install -U google-genai`
- **Credentials:** `.env` file with `GEMINI_API_KEY`
- **Agent:** `deep-research-pro-preview-12-2025`
- **Cost:** ~$2-5 per batched research run
- **Runtime:** 5-20 minutes depending on complexity

## Batching Rules

**Always batch research questions into one prompt.** This saves tokens and money.

- One Deep Research call per editorial batch (not one per question)
- Group questions by topic (charge card terms, FX fees, eligibility, etc.)
- Use numbered questions (Q1, Q2...) with clear grouping headers
- The agent handles multi-topic research well

## Prompt Template

```
You are a professional UK business finance researcher. Today's date is {today}.

Research the following specific questions about UK business credit cards.
Every answer must cite a specific source URL and access date.
If a fact cannot be verified, flag it as [UNVERIFIED - source not found].

=== GROUP 1: {topic} ===
Q1: {specific question}. Verify from {primary_source}.
Q2: ...

RESEARCH STANDARDS:
- UK-specific data only
- Primary source (issuer website) first
- For each data point: exact figure, source URL, access date
- Flag anything unverifiable with [UNVERIFIED - source not found]
```

## Execution Patterns

### Streaming with reconnect (preferred for long runs)

```python
from google import genai
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

stream = client.interactions.create(
    input=prompt,
    agent="deep-research-pro-preview-12-2025",
    background=True,
    store=True,
    stream=True,
    agent_config={"type": "deep-research", "thinking_summaries": "auto"}
)

interaction_id = None
last_event_id = None
is_complete = False
output = []

for event in stream:
    if event.event_type == "interaction.start":
        interaction_id = event.interaction.id
    if event.event_id:
        last_event_id = event.event_id
    if event.event_type == "content.delta":
        if event.delta.type == "text":
            output.append(event.delta.text)
        elif event.delta.type == "thought_summary":
            print(f"[Thinking: {event.delta.content.text}]")
    if event.event_type == "interaction.complete":
        is_complete = True
        break

# Reconnect if stream dropped
while not is_complete and interaction_id:
    time.sleep(5)
    resume = client.interactions.get(
        id=interaction_id, stream=True, last_event_id=last_event_id
    )
    for event in resume:
        # same processing...
```

### Simple polling (for shorter tasks)

```python
interaction = client.interactions.create(
    agent="deep-research-pro-preview-12-2025",
    input=prompt,
    background=True
)
while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        result = interaction.outputs[-1].text
        break
    elif interaction.status == "failed":
        raise RuntimeError(interaction.error)
    time.sleep(10)
```

## Processing Research Output

1. Save raw markdown to `research/` directory with timestamp
2. Parse structured data (card terms, fees, eligibility)
3. Update page config files: replace `[VERIFY]` placeholders with verified values
4. Re-run `scripts/quality_check.py` to confirm all placeholders resolved
5. Rebuild and push pages to staging

## Card Data Pipeline

```
research_cards(['amex_business_gold', 'rbs'])
    -> parse_card_research(output)
    -> draft_card_json(card_id, parsed_data)
    -> save_card_draft(card_id, card_json)
```

Card registry in `scripts/cc_builder/research.py` covers 25+ UK business cards with:
- Card name
- Primary verification domain
- Research template questions

## Integration with Editorial OS

Research output feeds into the editorial workflow at Stage 2 (source-grounding map):

1. Identify `[VERIFY]` placeholders across page configs
2. Batch all verification questions into one Deep Research prompt
3. Run research
4. Parse and apply results
5. Run `quality_check.py` (mechanical checks)
6. Run editorial trust pass (Tier 3 judgement checks)
7. Push to staging via `build_page.py`

## Models Reference (March 2026)

| Model | Use case |
|-------|----------|
| `gemini-3.1-pro-preview` | Complex reasoning, long context |
| `gemini-3-flash-preview` | Fast general tasks |
| `deep-research-pro-preview-12-2025` | Deep Research agent |

**Deprecated (do not use):** `gemini-2.0-*`, `gemini-1.5-*`
