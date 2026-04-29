"""Resolve runtime-routing metadata from Company Debt page configs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


DATE_FORMATS = ("%d %B %Y", "%d %b %Y", "%B %Y", "%b %Y")

SLUG_PAGE_CLASS_OVERRIDES = {
    # ── Credit card section (original entries) ─────────────────────────────
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

    # ── Liquidation section ────────────────────────────────────────────────
    # entity_owner — canonical "what is X" type / hub pages
    "liquidation": "entity_owner",
    "creditors-voluntary-liquidation": "entity_owner",
    "compulsory-liquidation": "entity_owner",
    "members-voluntary-liquidation": "entity_owner",
    "voluntary-liquidation": "entity_owner",
    "insolvency-vs-bankruptcy": "entity_owner",
    "liquidating-a-group-company-or-holding-company-in-the-uk": "entity_owner",
    "can-i-liquidate-a-dormant-company": "entity_owner",
    "can-i-liquidate-my-company-with-a-bounce-back-loan": "entity_owner",
    # asset-type pages sit under entity_owner (explaining what X is/becomes)
    "company-property-and-real-estate-in-liquidation": "entity_owner",
    "company-vehicles-and-equipment-in-liquidation": "entity_owner",
    "intellectual-property-and-trading-assets-in-liquidation": "entity_owner",
    "company-pensions-and-liquidation": "entity_owner",
    "business-bank-account-in-liquidation": "entity_owner",

    # process_guide — procedural / step-by-step / what happens next
    "how-to-prepare-for-company-liquidation": "process_guide",
    "timeline": "process_guide",
    "directors-conduct-report-2": "process_guide",
    "leases-and-contracts-in-liquidation": "process_guide",
    "creditor-meetings-in-liquidation": "process_guide",
    "how-to-choose-the-right-insolvency-procedure": "process_guide",
    "how-to-challenge-a-liquidators-decisions-or-fees": "process_guide",
    "liquidators-powers-and-duties": "process_guide",
    "how-to-prove-your-debt-in-company-liquidation": "process_guide",
    "can-i-choose-my-liquidator": "process_guide",
    "liquidating-a-company-with-no-assets-or-bank-account-uk": "process_guide",
    "which-creditors-get-paid-first": "process_guide",
    "what-happens-after-company-liquidation": "process_guide",
    "what-happens-to-employees": "process_guide",
    "insolvency-checklist": "process_guide",
    "list-of-liquidation-documents": "process_guide",

    # director_risk — director liability, conduct, personal exposure
    "what-happens-to-directors-in-liquidation": "director_risk",
    "whats-the-risk-of-being-disqualified-as-a-director": "director_risk",
    "can-directors-go-to-prison-for-company-debt": "director_risk",
    "can-directors-pay-themselves-before-liquidation": "director_risk",
    "what-happens-if-a-director-resigns-before-liquidation": "director_risk",
    "what-happens-if-a-director-transfers-assets-before-insolvency": "director_risk",
    "when-should-a-director-stop-trading": "director_risk",
    "director-conduct-review": "director_risk",
    "paying-staff-but-not-hmrc-before-liquidation": "director_risk",
    "what-happens-if-a-director-hides-company-assets": "director_risk",
    "can-a-director-be-sued-personally-by-creditors": "director_risk",
    "redundancy-payments-for-directors-in-an-mvl": "director_risk",

    # pricing_cost — fees, costs, affordability
    "how-much-does-liquidation-cost": "pricing_cost",

    # enforcement — creditor action, legal pressure, petitions
    "bailiffs-high-court-enforcement-officers": "enforcement",
    "dealing-with-an-hmrc-winding-up-petition": "enforcement",
    "can-a-supplier-force-my-company-into-liquidation": "enforcement",
    "winding-up-petition-vs-compulsory-liquidation": "enforcement",
    "ccj-when-going-insolvent": "enforcement",
    "what-happens-if-a-creditor-takes-me-to-court": "enforcement",
    "hmrc-as-a-creditor-in-liquidation": "enforcement",

    # recovery_strategy — alternatives, decisions, planning ahead
    "alternatives-to-company-liquidation": "recovery_strategy",
    "cant-afford-to-liquidate": "recovery_strategy",
    "company-restoration-after-liquidation": "recovery_strategy",
    "should-i-close-my-company-or-try-to-save-it": "recovery_strategy",
    "cva-vs-strike-off-vs-liquidation": "recovery_strategy",
    "can-you-liquidate-to-avoid-paying-suppliers": "recovery_strategy",

    # legal_compliance — dissolution, regulatory, statutory timelines
    "company-strike-off-and-dissolution": "legal_compliance",
    "liquidation-vs-dissolution-strike-off": "legal_compliance",
    "liquidation-deadlines-and-time-limits": "legal_compliance",
    "liquidating-a-limited-liability-partnership": "legal_compliance",
    "liquidating-a-charity-or-non-profit": "legal_compliance",
    "can-i-start-a-new-company-after-liquidating-my-old-one": "legal_compliance",

    # trigger — triage / "is this my situation?" decision pages
    "am-i-solvent": "trigger",
    "voluntary-vs-compulsory-liquidation": "trigger",
    "seek-insolvency-advice-before-missing-payments": "trigger",
    "what-happens-if-i-stop-paying-company-debts": "trigger",
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
