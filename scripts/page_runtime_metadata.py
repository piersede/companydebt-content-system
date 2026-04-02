"""Resolve runtime-routing metadata from Company Debt page configs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


DATE_FORMATS = ("%d %B %Y", "%d %b %Y", "%B %Y", "%b %Y")

SLUG_PAGE_CLASS_OVERRIDES = {
    "capital-on-tap-review": "entity_owner",
    "funding-circle-review": "entity_owner",
    "flexipay-review": "entity_owner",
    "compare-barclaycard": "entity_modifier",
    "compare-amex": "entity_modifier",
    "capital-on-tap-vs-amex": "debt_solution_comparison",
    "low-apr": "pricing_cost",
    "interest-free": "pricing_cost",
    "balance-transfer": "process_guide",
    "guide-to-business-credit-cards": "process_guide",
    "credit-cards-vs-charge-cards": "debt_solution_comparison",
}


@dataclass(frozen=True)
class RuntimeMetadata:
    page_class: str | None
    freshness_tier: str | None
    verification_date: str | None


def parse_verification_date(value: str | None) -> date | None:
    if not value:
        return None

    cleaned = value.strip()
    for fmt in DATE_FORMATS:
        try:
            parsed = datetime.strptime(cleaned, fmt)
            if fmt in {"%B %Y", "%b %Y"}:
                return date(parsed.year, parsed.month, 1)
            return parsed.date()
        except ValueError:
            continue
    return None


def infer_freshness_tier(verification_date: str | None, *, today: date | None = None) -> str | None:
    parsed = parse_verification_date(verification_date)
    if not parsed:
        return None

    current_day = today or date.today()
    age_days = (current_day - parsed).days

    if age_days <= 45:
        return "current"
    if age_days <= 120:
        return "aging"
    return "stale"


def infer_page_class(config: dict, slug: str | None = None) -> str | None:
    explicit = config.get("page_class")
    if explicit:
        return str(explicit)

    resolved_slug = slug or config.get("slug")
    if resolved_slug in SLUG_PAGE_CLASS_OVERRIDES:
        return SLUG_PAGE_CLASS_OVERRIDES[resolved_slug]

    page_type = str(config.get("page_type", "")).strip().lower()
    lowered_slug = (resolved_slug or "").strip().lower()

    if page_type == "review":
        return "entity_owner"
    if page_type in {"brand_compare", "brand-comparison", "brand_comparison", "comparison"}:
        if "-vs-" in lowered_slug or lowered_slug.endswith("-vs") or lowered_slug.startswith("vs-"):
            return "debt_solution_comparison"
        return "entity_modifier"
    if page_type == "guide":
        if "-vs-" in lowered_slug or "compare" in lowered_slug:
            return "debt_solution_comparison"
        return "process_guide"
    if page_type == "roundup":
        if any(token in lowered_slug for token in ("apr", "interest", "fee", "cost", "balance-transfer")):
            return "pricing_cost"
        return "debt_solution_comparison"

    return None


def resolve_page_runtime_metadata(config: dict, *, slug: str | None = None, today: date | None = None) -> RuntimeMetadata:
    verification_date = config.get("verification_date")
    return RuntimeMetadata(
        page_class=infer_page_class(config, slug=slug),
        freshness_tier=infer_freshness_tier(verification_date, today=today),
        verification_date=verification_date,
    )
