"""
Company Debt Deep Research Script
Uses the Gemini Deep Research agent to run a single batched research prompt
covering all articles in the current batch.
"""

import argparse
import json
import os
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

from research_prompt_utils import build_article_batch_prompt

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


def build_master_prompt(articles: list[dict]) -> str:
    today = datetime.now().strftime("%d %B %Y")
    intro = f"""You are a professional UK business finance researcher.

Research the following topics for a series of UK business finance articles for companydebt.co.uk.

Structure your response by article slug, using this exact format:

===
ARTICLE: /slug/
TITLE: Article Title
RESEARCHED: {today}

[Structured findings with source URLs]
===
"""
    return build_article_batch_prompt(
        articles,
        intro=intro,
        extra_rules=[
            "For financial products, include representative APR, fees, eligibility, minimum trading history, and whether an existing current account is required where relevant.",
            "For pricing, include the exact figure, the source page URL, and the date verified.",
            "Flag anything that could not be verified with [UNVERIFIED - source not found].",
        ],
    )


def run_research(articles: list[dict]) -> str:
    prompt = build_master_prompt(articles)

    print("\nStarting Deep Research Agent...")
    print(f"Articles in batch: {len(articles)}")
    print("Estimated time: 5-20 minutes\n")

    interaction_id = None
    last_event_id = None
    is_complete = False
    full_output: list[str] = []

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

    try:
        initial_stream = client.interactions.create(
            input=prompt,
            agent=AGENT,
            background=True,
            store=True,
            stream=True,
            agent_config={"type": "deep-research", "thinking_summaries": "auto"},
        )
        process_stream(initial_stream)
    except Exception as exc:
        print(f"\nStream interrupted: {exc}")

    while not is_complete and interaction_id:
        print(f"\nReconnecting... (last event: {last_event_id})")
        time.sleep(5)
        try:
            resume_stream = client.interactions.get(
                id=interaction_id,
                stream=True,
                last_event_id=last_event_id,
            )
            process_stream(resume_stream)
        except Exception as exc:
            print(f"Reconnect attempt failed: {exc}. Retrying in 10s...")
            time.sleep(10)

    return "".join(full_output)


def save_research(content: str, batch_name: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{timestamp}_{batch_name}_research.md"
    output_path = RESEARCH_DIR / filename

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(f"# Deep Research Output: {batch_name}\n")
        handle.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        handle.write(f"Agent: {AGENT}\n\n")
        handle.write("---\n\n")
        handle.write(content)

    print(f"\nSaved to: {output_path}")
    return output_path


DEFAULT_ARTICLES = [
    {
        "slug": "/business-credit-cards/low-apr/",
        "title": "Best Low APR Business Credit Cards in the UK",
        "research_questions": [
            "Current representative APR for Lloyds Bank Business Credit Card UK. Verify from lloydsbank.com.",
            "Current representative APR for HSBC Business Credit Card UK. Verify from business.hsbc.uk.",
            "Current representative APR for NatWest Business Credit Card UK. Verify from natwest.com.",
            "Current representative APR for Santander Business Cashback Credit Card UK. Verify from santander.co.uk.",
            "Current representative APR for Barclaycard Select Cashback Business Credit Card. Verify from barclaycard.co.uk.",
            "Current representative APR for Metro Bank Business Credit Card. Verify from metrobankonline.co.uk.",
            "Capital on Tap Business Credit Card statutory representative APR offered to 51% of applicants. Verify from capitalontap.com SECCI or key information document.",
            "Annual fees for each card above. Clarify whether the fee is per card or per account.",
            "Which of the cards above require an existing business current account with the same bank?",
            "Minimum trading history requirements for each card above.",
            "Do any of the cards above accept sole traders?",
        ],
    }
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Company Debt Deep Research Script - runs one batched Gemini Deep Research prompt"
    )
    parser.add_argument("--batch", help="Path to JSON file with article definitions")
    parser.add_argument("--name", default="research", help="Name for this batch")
    args = parser.parse_args()

    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as handle:
            articles = json.load(handle)
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
    except Exception as exc:
        print(f"\nFATAL ERROR: {exc}")
        sys.exit(1)
