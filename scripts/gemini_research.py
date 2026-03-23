"""
BusinessExpert Deep Research Script
====================================
Uses the Gemini Deep Research Agent (Interactions API) to run a single
batched research prompt covering all articles in the current batch.

The agent autonomously plans, searches, reads, and synthesises findings
into a structured report. One prompt per batch — not one per article.

Estimated cost: $2–$5 per run depending on research depth.
Typical run time: 5–20 minutes.

Usage:
    python scripts/gemini_research.py
    python scripts/gemini_research.py --batch path/to/articles.json
    python scripts/gemini_research.py --name "credit-cards-batch-1"

Requirements:
    pip install google-genai python-dotenv
"""

import os
import sys
import json
import time
import argparse
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    except Exception:
        pass
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found. Set in environment or .env file.")
    sys.exit(1)

try:
    from google import genai
except ImportError:
    print("ERROR: google-genai not installed. Run: pip install google-genai python-dotenv")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

RESEARCH_DIR = Path(__file__).parent.parent / "research"
RESEARCH_DIR.mkdir(exist_ok=True)

AGENT = "deep-research-pro-preview-12-2025"


# ----------------------------------------------------------------
# PROMPT BUILDER
# ----------------------------------------------------------------

def build_master_prompt(articles: list[dict]) -> str:
    today = datetime.now().strftime("%d %B %Y")

    prompt = f"""You are a professional UK business finance researcher. Today's date is {today}.

Research the following topics for a series of UK business finance articles for businessexpert.co.uk.

For each article, provide current, verified data from authoritative UK sources.
Cite the specific source URL and access date for every fact.
If a figure cannot be verified from a primary source, flag it explicitly as [UNVERIFIED — source not found].
Do not estimate or infer figures. Only report what can be confirmed.

Structure your response by article slug, using this exact format:

===
ARTICLE: /slug/
TITLE: Article Title
RESEARCHED: {today}

[Structured findings with source URLs]
===

HERE ARE THE ARTICLES TO RESEARCH:

"""
    for article in articles:
        prompt += f"ARTICLE: {article['slug']}\n"
        prompt += f"TITLE: {article['title']}\n"
        prompt += "FACTS NEEDED:\n"
        for q in article['research_questions']:
            prompt += f"  - {q}\n"
        prompt += "\n"

    prompt += """
RESEARCH STANDARDS:
- UK-specific data only unless stated otherwise
- For financial products: include representative APR, annual/monthly fees, eligibility, minimum trading history, and whether an existing account with the same bank is required
- For pricing: include the exact figure, the source page URL, and the date you verified it
- Flag anything that could not be verified with [UNVERIFIED — source not found]
- Do not pad with generic category descriptions — focus only on the specific facts requested
"""
    return prompt


# ----------------------------------------------------------------
# RUN RESEARCH (background + streaming)
# ----------------------------------------------------------------

def run_research(articles: list[dict]) -> str:
    prompt = build_master_prompt(articles)

    print(f"\nStarting Deep Research Agent...")
    print(f"Articles in batch: {len(articles)}")
    print(f"Estimated time: 5–20 minutes\n")

    interaction_id = None
    last_event_id = None
    is_complete = False
    full_output = []

    def process_stream(event_stream):
        nonlocal interaction_id, last_event_id, is_complete

        for event in event_stream:
            if event.event_type == "interaction.start":
                interaction_id = event.interaction.id
                print(f"Research started (ID: {interaction_id})")

            if event.event_id:
                last_event_id = event.event_id

            if event.event_type == "content.delta":
                if event.delta.type == "text":
                    print(event.delta.text, end="", flush=True)
                    full_output.append(event.delta.text)
                elif event.delta.type == "thought_summary":
                    print(f"\n[Thinking: {event.delta.content.text}]", flush=True)

            if event.event_type == "interaction.complete":
                print("\n\nResearch complete.")
                is_complete = True

    # Start streaming
    try:
        initial_stream = client.interactions.create(
            input=prompt,
            agent=AGENT,
            background=True,
            store=True,
            stream=True,
            agent_config={
                "type": "deep-research",
                "thinking_summaries": "auto"
            }
        )
        process_stream(initial_stream)

    except Exception as e:
        print(f"\nStream interrupted: {e}")

    # Reconnect if stream dropped before completion
    while not is_complete and interaction_id:
        print(f"\nReconnecting... (last event: {last_event_id})")
        time.sleep(5)
        try:
            resume_stream = client.interactions.get(
                id=interaction_id,
                stream=True,
                last_event_id=last_event_id
            )
            process_stream(resume_stream)
        except Exception as e:
            print(f"Reconnect attempt failed: {e}. Retrying in 10s...")
            time.sleep(10)

    return "".join(full_output)


# ----------------------------------------------------------------
# SAVE OUTPUT
# ----------------------------------------------------------------

def save_research(content: str, batch_name: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{timestamp}_{batch_name}_research.md"
    output_path = RESEARCH_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Deep Research Output: {batch_name}\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Agent: {AGENT}\n\n")
        f.write("---\n\n")
        f.write(content)

    print(f"\nSaved to: {output_path}")
    return output_path


# ----------------------------------------------------------------
# DEFAULT ARTICLE BATCH
# Edit this section to define the articles for your current run.
# Or pass a JSON file with --batch.
# ----------------------------------------------------------------

DEFAULT_ARTICLES = [
    {
        "slug": "/business-credit-cards/low-apr/",
        "title": "Best Low APR Business Credit Cards in the UK",
        "research_questions": [
            "Current representative APR for Lloyds Bank Business Credit Card UK — verify from lloydsbank.com",
            "Current representative APR for HSBC Business Credit Card UK — verify from business.hsbc.uk",
            "Current representative APR for NatWest Business Credit Card UK — verify from natwest.com",
            "Current representative APR for Santander Business Cashback Credit Card UK — verify from santander.co.uk",
            "Current representative APR for Barclaycard Select Cashback Business Credit Card — verify from barclaycard.co.uk",
            "Current representative APR for Metro Bank Business Credit Card — verify from metrobankonline.co.uk",
            "Capital on Tap Business Credit Card: what is the statutory representative APR (offered to 51% of applicants)? Verify from capitalontap.com SECCI or key information document",
            "Annual fees for each card above — per card or per account?",
            "Which of the above cards require an existing business current account with the same bank?",
            "Minimum trading history requirements for each card above",
            "Do any of the above cards accept sole traders?",
        ]
    },
    # Add more articles here:
    # {
    #     "slug": "/business-credit-cards/cashback/",
    #     "title": "Best Cashback Business Credit Cards UK",
    #     "research_questions": [...]
    # },
]


# ----------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="BusinessExpert Deep Research Script — runs one batched Gemini Deep Research prompt"
    )
    parser.add_argument("--batch", help="Path to JSON file with article definitions")
    parser.add_argument("--name", default="research", help="Name for this batch (used in output filename)")
    args = parser.parse_args()

    if args.batch:
        with open(args.batch, "r") as f:
            articles = json.load(f)
        print(f"Loaded {len(articles)} articles from {args.batch}")
    else:
        articles = DEFAULT_ARTICLES
        print(f"Using default batch ({len(articles)} articles)")

    try:
        result = run_research(articles)
        if result.strip():
            output_path = save_research(result, args.name)
            print(f"\nDone. Review research at:\n{output_path}")
        else:
            print("\nNo output returned. Check your API key and quota.")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)
