"""Gemini Deep Research integration for cc_builder.

Provides card-level and page-level research capabilities using
the Gemini Deep Research Agent (Interactions API).

Usage from CLI:
    python scripts/build_page.py --research-cards amex_business_gold,rbs
    python scripts/build_page.py --research-page best-business-credit-cards

Usage from Python:
    from cc_builder.research import research_cards, research_page, parse_card_research
    output = research_cards(['amex_business_gold', 'rbs'])
    card_drafts = parse_card_research(output)
"""

from __future__ import annotations

import json
import os
import re
import time
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

RESEARCH_DIR = Path(__file__).parent.parent.parent / "research"
CARDS_DIR = Path(__file__).parent / "data" / "cards"

AGENT = "deep-research-pro-preview-12-2025"

# Card research templates — what we need to know per card
CARD_RESEARCH_TEMPLATE = """\
{card_name} UK:
- Representative APR (the rate offered to at least 51% of successful applicants)
- Annual fee (per card or per account? Is it waived for the first year?)
- Cashback or reward rate (if any)
- Credit limit range (if published)
- Eligibility: sole traders? limited companies? LLPs? partnerships?
- Existing bank account required? If so, which bank?
- Minimum trading history or turnover requirements
- Key features or perks (e.g. travel insurance, lounge access, introductory offers)
- Is this product still available as of today?
- Verify all facts from {verify_domain}"""

# Known card metadata for research
CARD_REGISTRY = {
    # Amex cards
    'amex_business_gold': {
        'name': 'American Express Business Gold Card',
        'verify_domain': 'americanexpress.com/uk',
    },
    'amex_business_basic': {
        'name': 'American Express Business Card (Basic)',
        'verify_domain': 'americanexpress.com/uk',
    },
    'amex_business_platinum': {
        'name': 'American Express Business Platinum Card',
        'verify_domain': 'americanexpress.com/uk',
    },
    'ba_amex_accelerating': {
        'name': 'British Airways American Express Accelerating Business Card',
        'verify_domain': 'americanexpress.com/uk',
    },
    'amazon_amex': {
        'name': 'Amazon Business Prime American Express Card',
        'verify_domain': 'americanexpress.com/uk or amazon.co.uk',
    },
    # Bank cards
    'rbs': {
        'name': 'RBS Business Plus Credit Card',
        'verify_domain': 'rbs.co.uk',
    },
    'natwest_business_plus': {
        'name': 'NatWest Business Plus Credit Card',
        'verify_domain': 'natwest.com',
    },
    'barclays_premium_plus': {
        'name': 'Barclays Premium Plus Business Credit Card (Barclaycard)',
        'verify_domain': 'barclaycard.co.uk',
    },
    'lloyds_charge': {
        'name': 'Lloyds Bank Business Charge Card',
        'verify_domain': 'lloydsbank.com',
    },
    'barclaycard_charge': {
        'name': 'Barclaycard Select Charge Card',
        'verify_domain': 'barclaycard.co.uk',
    },
    'cooperative_charge': {
        'name': 'The Co-Operative Bank Business Charge Card',
        'verify_domain': 'co-operativebank.co.uk',
    },
    'natwest_onecard': {
        'name': 'NatWest Onecard',
        'verify_domain': 'natwest.com',
    },
    # Fintech cards
    'funding_circle_cashback': {
        'name': 'Funding Circle Cashback Business Credit Card',
        'verify_domain': 'fundingcircle.com',
    },
    'funding_circle_flexipay': {
        'name': 'Funding Circle FlexiPay',
        'verify_domain': 'fundingcircle.com',
    },
    'moss': {
        'name': 'Moss Business Credit Cards',
        'verify_domain': 'getmoss.com',
    },
    # Existing cards (for re-research / verification refresh)
    'lloyds': {
        'name': 'Lloyds Bank Business Credit Card',
        'verify_domain': 'lloydsbank.com',
    },
    'metro_bank': {
        'name': 'Metro Bank Business Credit Card',
        'verify_domain': 'metrobankonline.co.uk',
    },
    'hsbc': {
        'name': 'HSBC Business Credit Card',
        'verify_domain': 'business.hsbc.uk',
    },
    'santander': {
        'name': 'Santander Business Cashback Credit Card',
        'verify_domain': 'santander.co.uk',
    },
    'natwest': {
        'name': 'NatWest Business Credit Card',
        'verify_domain': 'natwest.com',
    },
    'barclaycard': {
        'name': 'Barclaycard Select Cashback Business Credit Card',
        'verify_domain': 'barclaycard.co.uk',
    },
    'capital_on_tap': {
        'name': 'Capital on Tap Business Credit Card',
        'verify_domain': 'capitalontap.com',
    },
}


def _get_client():
    """Lazy-load Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            from dotenv import load_dotenv
            env_path = Path(__file__).parent.parent.parent / ".env"
            load_dotenv(env_path)
            api_key = os.getenv("GEMINI_API_KEY")
        except Exception:
            pass
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found. Set it in environment or .env file")

    from google import genai
    return genai.Client(api_key=api_key)


def _build_card_research_prompt(card_ids: list[str]) -> str:
    """Build a research prompt for specific cards."""
    today = datetime.now().strftime("%d %B %Y")

    questions = []
    for card_id in card_ids:
        if card_id not in CARD_REGISTRY:
            raise ValueError(f"Unknown card ID: {card_id}. Available: {sorted(CARD_REGISTRY.keys())}")
        meta = CARD_REGISTRY[card_id]
        questions.append(CARD_RESEARCH_TEMPLATE.format(
            card_name=meta['name'],
            verify_domain=meta['verify_domain'],
        ))

    prompt = f"""You are a professional UK business finance researcher. Today's date is {today}.

Research the following UK business credit card products. For each card, provide current, verified data from authoritative UK sources.

CRITICAL RULES:
- Cite the specific source URL and access date for every fact
- If a figure cannot be verified from a primary source, flag it as [UNVERIFIED — source not found]
- Do not estimate or infer figures — only report what can be confirmed
- Check whether each product is still available (some may have been discontinued)
- For charge cards: note that they require full balance payment monthly (no revolving credit)
- Representative APR means the rate offered to at least 51% of successful applicants

Structure your response using this exact format for each card:

===
CARD: {{card_id}}
NAME: {{full card name}}
RESEARCHED: {today}
STATUS: available / discontinued / unclear

Representative APR: {{value}} [source: {{url}}, accessed {{date}}]
Annual Fee: {{value}} [source: {{url}}, accessed {{date}}]
Cashback/Rewards: {{value}} [source: {{url}}, accessed {{date}}]
Credit Limit: {{value}} [source: {{url}}, accessed {{date}}]
Card Type: credit card / charge card [source: {{url}}, accessed {{date}}]
Eligibility — Sole Traders: yes / no / unclear [source: {{url}}, accessed {{date}}]
Eligibility — Limited Companies: yes / no / unclear [source: {{url}}, accessed {{date}}]
Existing Account Required: yes ({{bank}}) / no [source: {{url}}, accessed {{date}}]
Minimum Trading History: {{value}} [source: {{url}}, accessed {{date}}]
Key Features: {{bullet list}}
Additional Notes: {{anything notable}}
===

HERE ARE THE CARDS TO RESEARCH:

"""
    for i, card_id in enumerate(card_ids, 1):
        meta = CARD_REGISTRY[card_id]
        prompt += f"\n{i}. CARD ID: {card_id}\n"
        prompt += questions[i - 1] + "\n"

    prompt += """
RESEARCH STANDARDS:
- UK-specific data only
- Primary source (issuer website) first, secondary sources only if primary is unavailable
- For each data point: exact figure, source URL, access date
- Flag anything unverifiable with [UNVERIFIED — source not found]
- If the product appears to be discontinued, state this clearly and note when it was last available if known
"""
    return prompt


def _build_page_research_prompt(page_slug: str, page_title: str, topics: list[str]) -> str:
    """Build a research prompt for page-level editorial content."""
    today = datetime.now().strftime("%d %B %Y")

    topic_list = "\n".join(f"  - {t}" for t in topics)

    return f"""You are a professional UK business finance researcher. Today's date is {today}.

Research the following topics for a Company Debt.co.uk article:

ARTICLE: {page_slug}
TITLE: {page_title}

TOPICS TO RESEARCH:
{topic_list}

CRITICAL RULES:
- UK-specific data only unless stated otherwise
- Cite source URL and access date for every fact
- Flag anything unverifiable with [UNVERIFIED — source not found]
- Do not pad with generic descriptions — focus on specific facts
- Include regulatory context where relevant (FCA, consumer credit regulations)

Structure your response with clear headings per topic.
"""


def _run_deep_research(prompt: str, batch_name: str) -> str:
    """Execute a Deep Research request and return the output text."""
    client = _get_client()

    print(f"Starting Deep Research Agent ({batch_name})...")
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

    # Reconnect if stream dropped
    retries = 0
    while not is_complete and interaction_id and retries < 10:
        retries += 1
        print(f"\nReconnecting... (attempt {retries}, last event: {last_event_id})")
        time.sleep(5)
        try:
            resume_stream = client.interactions.get(
                id=interaction_id,
                stream=True,
                last_event_id=last_event_id
            )
            process_stream(resume_stream)
        except Exception as e:
            print(f"Reconnect failed: {e}. Retrying in 10s...")
            time.sleep(10)

    output = "".join(full_output)

    # Save raw output
    RESEARCH_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = RESEARCH_DIR / f"{timestamp}_{batch_name}_research.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Deep Research Output: {batch_name}\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Agent: {AGENT}\n\n---\n\n")
        f.write(output)
    print(f"\nSaved raw output: {output_path}")

    return output


# ── Public API ──────────────────────────────────────────────────────

def research_cards(card_ids: list[str]) -> str:
    """Research specific cards via Gemini Deep Research.

    Args:
        card_ids: List of card IDs from CARD_REGISTRY.

    Returns:
        Raw research output text.
    """
    prompt = _build_card_research_prompt(card_ids)
    batch_name = f"cards-{'_'.join(card_ids[:3])}"
    if len(card_ids) > 3:
        batch_name += f"-and-{len(card_ids) - 3}-more"
    return _run_deep_research(prompt, batch_name)


def research_page(page_slug: str, page_title: str, topics: list[str]) -> str:
    """Research editorial topics for a specific page.

    Args:
        page_slug: URL slug of the page.
        page_title: Title of the page.
        topics: List of research questions/topics.

    Returns:
        Raw research output text.
    """
    prompt = _build_page_research_prompt(page_slug, page_title, topics)
    slug_short = page_slug.strip("/").split("/")[-1]
    return _run_deep_research(prompt, f"page-{slug_short}")


def parse_card_research(research_output: str) -> dict[str, dict]:
    """Parse structured card research output into draft card data.

    Args:
        research_output: Raw text from research_cards().

    Returns:
        Dict mapping card_id to parsed data dict with keys like
        'representative_apr', 'annual_fee', 'status', etc.
    """
    cards = {}
    # Split on === blocks
    blocks = re.split(r'={3,}', research_output)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Extract card ID
        card_match = re.search(r'CARD:\s*(\S+)', block)
        if not card_match:
            continue

        card_id = card_match.group(1)
        data = {'raw': block}

        # Extract structured fields
        patterns = {
            'name': r'NAME:\s*(.+)',
            'status': r'STATUS:\s*(.+)',
            'representative_apr': r'Representative APR:\s*(.+?)(?:\[|$)',
            'annual_fee': r'Annual Fee:\s*(.+?)(?:\[|$)',
            'cashback_rewards': r'Cashback/Rewards:\s*(.+?)(?:\[|$)',
            'credit_limit': r'Credit Limit:\s*(.+?)(?:\[|$)',
            'card_type': r'Card Type:\s*(.+?)(?:\[|$)',
            'sole_traders': r'Eligibility.*Sole Traders:\s*(.+?)(?:\[|$)',
            'limited_companies': r'Eligibility.*Limited Companies:\s*(.+?)(?:\[|$)',
            'existing_account': r'Existing Account Required:\s*(.+?)(?:\[|$)',
            'min_trading_history': r'Minimum Trading History:\s*(.+?)(?:\[|$)',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, block, re.IGNORECASE)
            if match:
                data[key] = match.group(1).strip()

        # Extract source URLs
        sources = re.findall(r'\[source:\s*(https?://\S+)', block)
        data['sources'] = list(set(sources))

        # Check for UNVERIFIED flags
        data['unverified_fields'] = []
        for line in block.split('\n'):
            if '[UNVERIFIED' in line:
                field = line.split(':')[0].strip()
                data['unverified_fields'].append(field)

        cards[card_id] = data

    return cards


def draft_card_json(card_id: str, parsed_data: dict) -> dict:
    """Convert parsed research data into a draft card JSON structure.

    This creates a starter JSON that matches our card schema.
    Fields marked [UNVERIFIED] get a qualifier noting this.
    Human review is still required before finalising.

    Args:
        card_id: The card identifier.
        parsed_data: Output from parse_card_research() for this card.

    Returns:
        Dict matching our card JSON schema (ready for json.dump).
    """
    meta = CARD_REGISTRY.get(card_id, {})
    today = datetime.now().strftime("%d %B %Y")

    # Determine entity eligibility
    entities = []
    sole = parsed_data.get('sole_traders', '').lower()
    ltd = parsed_data.get('limited_companies', '').lower()
    if 'yes' in sole:
        entities.append('sole-trader')
    if 'yes' in ltd:
        entities.append('limited-company')
    if not entities:
        entities = ['[VERIFY]']

    # Determine existing account requirement
    existing_acct = parsed_data.get('existing_account', '')
    acct_required = 'yes' in existing_acct.lower()
    acct_bank = None
    if acct_required:
        # Try to extract bank name from parentheses
        bank_match = re.search(r'\(([^)]+)\)', existing_acct)
        if bank_match:
            acct_bank = bank_match.group(1)

    # Build facts array
    facts = []
    apr = parsed_data.get('representative_apr', '[VERIFY]')
    if apr and '[UNVERIFIED' not in apr:
        facts.append({
            "label": "Representative APR",
            "value": apr.strip().rstrip('.'),
            "modifier": "apr",
            "qualifier": None
        })
    else:
        facts.append({
            "label": "Representative APR",
            "value": "[VERIFY]",
            "modifier": "apr",
            "qualifier": "Could not verify from primary source"
        })

    fee = parsed_data.get('annual_fee', '[VERIFY]')
    facts.append({
        "label": "Annual Fee",
        "value": fee.strip().rstrip('.') if fee else "[VERIFY]",
        "modifier": None,
        "qualifier": None
    })

    reward = parsed_data.get('cashback_rewards', '')
    if reward and '[UNVERIFIED' not in reward:
        facts.append({
            "label": "Rewards",
            "value": reward.strip().rstrip('.'),
            "modifier": None,
            "qualifier": None
        })

    acct_text = "No existing account required" if not acct_required else f"Requires {acct_bank or 'bank'} account"
    facts.append({
        "label": "Existing Account",
        "value": acct_text,
        "modifier": "none-required" if not acct_required else None,
        "qualifier": None
    })

    card_json = {
        "id": f"{card_id}_business_{'charge' if 'charge' in parsed_data.get('card_type', '').lower() else 'credit'}_card",
        "bank": meta.get('name', '').split(' ')[0] if meta else card_id,
        "name": parsed_data.get('name', meta.get('name', card_id)),
        "img_url": f"[NEEDS_IMAGE]",
        "img_alt": f"{parsed_data.get('name', card_id)} card",
        "facts": facts,
        "cta_url": parsed_data.get('sources', ['[VERIFY]'])[0] if parsed_data.get('sources') else "[VERIFY]",
        "cta_label": f"View {meta.get('name', card_id).split(' ')[0]} Details",
        "verify_source": meta.get('verify_domain', '[VERIFY]'),
        "verify_date": today,
        "categories": [],
        "accepted_entities": entities,
        "existing_account_required": acct_required,
        "existing_account_bank": acct_bank,
        "_research_status": parsed_data.get('status', 'unknown'),
        "_unverified_fields": parsed_data.get('unverified_fields', []),
    }

    return card_json


def save_card_draft(card_id: str, card_json: dict) -> Path:
    """Save a draft card JSON file.

    Saves to data/cards/{card_id}.json. Will NOT overwrite existing files
    unless the existing file has an older verify_date.

    Args:
        card_id: Card identifier.
        card_json: Card data dict.

    Returns:
        Path to saved file.
    """
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CARDS_DIR / f"{card_id}.json"

    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        # Don't overwrite unless research is newer
        existing_date = existing.get('verify_date', '')
        new_date = card_json.get('verify_date', '')
        if existing_date >= new_date:
            print(f"  Skipping {card_id}: existing data ({existing_date}) is current")
            return output_path

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(card_json, f, indent=2, ensure_ascii=False)

    print(f"  Saved draft: {output_path}")
    return output_path


def research_and_create_cards(card_ids: list[str], dry_run: bool = False) -> dict[str, Path]:
    """Full pipeline: research cards → parse → create draft JSONs.

    Args:
        card_ids: List of card IDs to research.
        dry_run: If True, build prompt but don't call API.

    Returns:
        Dict mapping card_id to saved file path.
    """
    # Filter to only cards that need research
    new_cards = []
    for cid in card_ids:
        json_path = CARDS_DIR / f"{cid}.json"
        if json_path.exists():
            print(f"  {cid}: JSON exists, skipping (use --force to re-research)")
        else:
            new_cards.append(cid)

    if not new_cards:
        print("All cards already have JSON files.")
        return {}

    if dry_run:
        prompt = _build_card_research_prompt(new_cards)
        print(f"\n--- DRY RUN: Would send this prompt ({len(prompt)} chars) ---\n")
        print(prompt[:500] + "...\n")
        return {}

    # Run research
    output = research_cards(new_cards)

    # Parse results
    parsed = parse_card_research(output)
    print(f"\nParsed {len(parsed)} cards from research output")

    # Create draft JSONs
    saved = {}
    for card_id, data in parsed.items():
        if data.get('status', '').lower() == 'discontinued':
            print(f"  {card_id}: DISCONTINUED — skipping JSON creation")
            continue
        card_json = draft_card_json(card_id, data)
        path = save_card_draft(card_id, card_json)
        saved[card_id] = path

    return saved


def list_missing_cards(required_card_ids: list[str] | None = None) -> list[str]:
    """List card IDs that don't have JSON files yet.

    Args:
        required_card_ids: Specific cards to check. If None, checks all in CARD_REGISTRY.

    Returns:
        List of card IDs without JSON files.
    """
    check_ids = required_card_ids or list(CARD_REGISTRY.keys())
    missing = []
    for cid in check_ids:
        if not (CARDS_DIR / f"{cid}.json").exists():
            missing.append(cid)
    return missing


def verify_card_freshness(max_age_days: int = 30) -> list[dict]:
    """Check all card JSON files for stale verify_dates.

    Returns:
        List of dicts with 'card_id', 'verify_date', 'age_days' for stale cards.
    """
    stale = []
    today = datetime.now()

    for json_file in CARDS_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            card = json.load(f)

        vdate_str = card.get('verify_date', '')
        try:
            vdate = datetime.strptime(vdate_str, "%d %B %Y")
            age = (today - vdate).days
            if age > max_age_days:
                stale.append({
                    'card_id': json_file.stem,
                    'verify_date': vdate_str,
                    'age_days': age,
                })
        except ValueError:
            stale.append({
                'card_id': json_file.stem,
                'verify_date': vdate_str,
                'age_days': -1,  # unparseable
            })

    return sorted(stale, key=lambda x: x['age_days'], reverse=True)
