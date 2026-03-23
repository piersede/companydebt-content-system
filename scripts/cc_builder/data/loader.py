"""Load card data from JSON files and apply page-specific overrides."""

from __future__ import annotations

import json
from pathlib import Path

CARDS_DIR = Path(__file__).parent / 'cards'


def load_card(card_id: str) -> dict:
    """Load a single card's canonical data from its JSON file."""
    path = CARDS_DIR / f'{card_id}.json'
    if not path.exists():
        raise FileNotFoundError(f'Card data not found: {path}')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_cards_for_page(config: dict) -> tuple[list[dict], list[dict]]:
    """Load and prepare card data for a page.

    Loads canonical card data, applies page-specific overrides from
    config['card_overrides'], and returns (main_cards, separate_cards).
    """
    overrides = config.get('card_overrides', {})

    main_cards = []
    for card_id in config.get('card_ids', []):
        card = load_card(card_id)
        # Apply page-specific overrides
        if card_id in overrides:
            card.update(overrides[card_id])
        main_cards.append(card)

    separate_cards = []
    for card_id in config.get('separate_card_ids', []):
        card = load_card(card_id)
        if card_id in overrides:
            card.update(overrides[card_id])
        separate_cards.append(card)

    return main_cards, separate_cards


def list_available_cards() -> list[str]:
    """List all available card IDs (JSON files without extension)."""
    if not CARDS_DIR.exists():
        return []
    return sorted(p.stem for p in CARDS_DIR.glob('*.json'))
