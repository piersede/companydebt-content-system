"""Resolve runtime-routing metadata from Company Debt page configs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


DATE_FORMATS = ("%d %B %Y", "%d %b %Y", "%B %Y", "%b %Y")

SLUG_PAGE_CLASS_OVERRIDES = {

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
    "are-directors-personally-liable-for-company-debts": "director_risk",

    # pricing_cost — fees, costs, affordability
    "how-much-does-liquidation-cost": "pricing_cost",

    # enforcement — creditor action, legal pressure, petitions
    "bailiffs-high-court-enforcement-officers": "enforcement",
    "dealing-with-an-hmrc-winding-up-petition": "enforcement",
    "winding-up-petitions": "enforcement",
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
    "cant-pay-vat": "trigger",
    "problems-paying-corporation-tax-hmrc": "trigger",

    # data_reference — official statistics and data series pages
    "uk-insolvency-statistics": "data_reference",
    "data": "data_reference",
    "winding-up-petition-tracker": "data_reference",
    "dissolutions-vs-insolvencies": "data_reference",
    "payment-practices-late-payment": "data_reference",
    "pub-closures-in-the-uk": "data_reference",
    "cvl-statistics": "data_reference",
    "compulsory-liquidation-statistics": "data_reference",
    "administration-statistics": "data_reference",
    "company-insolvencies-by-sector": "data_reference",
    "construction-insolvency-statistics": "data_reference",

    # sector_statistics — single-SIC-sector insolvency data pages (the
    # per-sector rollout family: scripts/datahub/pages/sic_group_stats.py).
    # A distinct sub-class of data_reference: same statistics-page discipline,
    # plus its own real automated gate (scripts/sector_data_audit.py, wired
    # into build_page.py --publish) requiring a sourced sector-context fact
    # and a practitioner-voice insight paragraph on every page.
    "furniture-insolvency-statistics": "sector_statistics",
    "restaurant-insolvency-statistics": "sector_statistics",
    "road-haulage-insolvency-statistics": "sector_statistics",
    "recruitment-agency-insolvency-statistics": "sector_statistics",
    "temporary-staffing-agency-insolvency-statistics": "sector_statistics",
    "motor-vehicle-repair-insolvency-statistics": "sector_statistics",
    "cleaning-company-insolvency-statistics": "sector_statistics",
    "hotel-insolvency-statistics": "sector_statistics",
    "estate-agency-insolvency-statistics": "sector_statistics",
    "it-consultancy-insolvency-statistics": "sector_statistics",
    "management-consultancy-insolvency-statistics": "sector_statistics",
    "architectural-engineering-insolvency-statistics": "sector_statistics",
    "personal-care-services-insolvency-statistics": "sector_statistics",
    "sports-facility-insolvency-statistics": "sector_statistics",
    "medical-dental-practice-insolvency-statistics": "sector_statistics",
    "creative-arts-entertainment-insolvency-statistics": "sector_statistics",
    "amusement-recreation-insolvency-statistics": "sector_statistics",
    "real-estate-letting-investment-insolvency-statistics": "sector_statistics",
    "freight-forwarding-logistics-insolvency-statistics": "sector_statistics",
    "retail-insolvency-statistics": "sector_statistics",

    # -- Adopted existing pages: HMRC pressure and enforcement (/hmrc/*) --
    "accelerated-payment-notices-apn": "enforcement",
    "can-hmrc-shut-down-my-business": "enforcement",
    "controlled-goods-agreement": "enforcement",
    "corporation-tax-penalties": "enforcement",
    "distraint-order-notice": "enforcement",
    "hmrc-compliance-checks": "enforcement",
    "hmrc-criminal-investigations": "enforcement",
    "hmrc-enforcement-action": "enforcement",
    "hmrc-follower-notice": "enforcement",
    "hmrc-fraud-investigations": "enforcement",
    "hmrc-penalties-investigations": "enforcement",
    "hmrc-tax-investigations": "enforcement",
    "hmrc-threatening-letters": "enforcement",
    "joint-and-several-liability-for-unpaid-vat": "enforcement",
    "notice-of-enforcement": "enforcement",
    "pay-hmrc-or-suppliers-first": "enforcement",
    "personal-liability-notices": "enforcement",
    "security-bond-notices": "enforcement",
    "security-bonds": "enforcement",
    "tax-penalties": "enforcement",
    "understanding-hmrc-debt-collection": "enforcement",
    "vat-penalties": "enforcement",
    "what-can-hmrc-bailiffs-take": "enforcement",
    "what-happens-if-hmrc-freezes-your-business-bank-account": "enforcement",
    "what-happens-if-hmrc-sends-bailiffs-to-a-business": "enforcement",
    "what-happens-if-you-ignore-hmrc-letters": "enforcement",
    "hmrc": "entity_owner",
    "hmrc-debt-enforcement-hub": "entity_owner",
    "hmrc-offices-contact-guide": "process_guide",
    "time-to-pay-hmrc": "recovery_strategy",
    "what-happens-if-hmrc-rejects-your-time-to-pay-arrangement": "recovery_strategy",
    "cant-pay-paye": "trigger",

    # -- Adopted existing pages: Liquidation section (/liquidation/*) --
    "directors-responsibilities-after-a-company-is-struck-off": "director_risk",
    "insolvency-myths-debunked": "entity_owner",
    "uk-insolvency-glossary": "entity_owner",
    "can-i-be-sued-after-my-company-is-dissolved": "legal_compliance",
    "uk-insolvency-flowchart": "process_guide",

    # -- Adopted existing pages: Director advice (/advice/*) --
    "can-a-director-be-made-bankrupt-if-a-business-fails": "director_risk",
    "can-director-criminal-record": "director_risk",
    "can-personal-assets-of-directors-be-seized-from-a-ltd-company": "director_risk",
    "directors-disqualification": "director_risk",
    "directors-duties-to-creditors": "director_risk",
    "directors-personal-guarantees": "director_risk",
    "losing-house-if-company-goes-bust": "director_risk",
    "misfeasance": "director_risk",
    "overdrawn-directors-loan-accounts": "director_risk",
    "personal-guarantee-insurance": "director_risk",
    "personal-liability-for-cbils-loans": "director_risk",
    "the-risks-of-signing-a-personal-guarantee": "director_risk",
    "unenforceable-personal-guarantee": "director_risk",
    "what-are-a-company-directors-duties-to-avoid-and-disclose-conflicts-of-interest": "director_risk",
    "what-are-the-duties-and-responsibilities-of-a-company-director": "director_risk",
    "what-is-a-directors-responsibility-for-accountancy-errors": "director_risk",
    "writing-off-a-directors-loan-account": "director_risk",
    "advice-hub": "entity_owner",
    "what-are-fixed-and-floating-charges": "entity_owner",
    "what-are-phoenix-companies": "entity_owner",
    "what-is-limited-liability": "entity_owner",
    "what-is-the-companies-act-2006": "legal_compliance",
    "frozen-bank-account": "process_guide",
    "hmrcs-ir35-investigations-different": "process_guide",
    "how-to-legally-take-money-out-of-a-limited-company": "process_guide",
    "insolvency-advice-for-directors": "process_guide",
    "preventing-company-director-disputes": "process_guide",
    "business-restructuring": "recovery_strategy",
    "debt-management-guide": "recovery_strategy",
    "funding-options-for-smes-in-the-uk": "recovery_strategy",
    "get-free-business-debt-advice": "recovery_strategy",

    # -- Adopted existing pages: Insolvency reference (/insolvency/*) --
    "secured-vs-unsecured-creditors": "debt_solution_comparison",
    "personal-liability-spouses-business-debts": "director_risk",
    "personally-liabilty-of-company-secretary": "director_risk",
    "shareholders-liable-company-debts": "director_risk",
    "what-is-wrongful-trading": "director_risk",
    "retail-industry-insolvency-trends": "distress_use_case",
    "dealing-with-creditor-pressure": "enforcement",
    "insolvent-company-owes-me-money": "enforcement",
    "what-is-a-freezing-order-or-injunction": "enforcement",
    "what-is-a-high-court-writ": "enforcement",
    "what-to-do-about-customer-insolvency": "enforcement",
    "cease-trading": "entity_owner",
    "insolvent-company-investigations": "entity_owner",
    "limited-company-bankruptcy": "entity_owner",
    "lpa-receivership": "entity_owner",
    "preferential-non-preferential-creditors": "entity_owner",
    "what-is-a-creditor": "entity_owner",
    "what-is-an-individual-voluntary-arrangement": "entity_owner",
    "what-is-an-insolvency-practitioner": "entity_owner",
    "antecedent-transactions": "legal_compliance",
    "insolvency-act-1986": "legal_compliance",
    "preferential-payments-during-insolvency": "legal_compliance",
    "transactions-at-undervalue": "legal_compliance",
    "validation-order": "legal_compliance",
    "what-is-the-insolvency-service": "legal_compliance",
    "creditors-guides-to-insolvency-practitioners-fees": "pricing_cost",
    "check-if-a-company-is-insolvent": "process_guide",
    "creditors-meeting": "process_guide",
    "find-a-liquidator-near-me": "process_guide",
    "statement-of-affairs": "process_guide",
    "business-recovery-services": "recovery_strategy",
    "can-we-trade-out-of-insolvency": "recovery_strategy",
    "can-you-sell-your-insolvent-company": "recovery_strategy",
    "creditor-negotiations": "recovery_strategy",
    "how-to-reduce-insolvency-risk": "recovery_strategy",
    "how-to-save-a-struggling-business": "recovery_strategy",
    "rescue-your-business-from-insolvency": "recovery_strategy",
    "stop-or-avoid-insolvency": "recovery_strategy",
    "what-are-the-warning-signs-of-an-insolvent-company": "trigger",
    "what-happens-if-a-company-cannot-pay-its-debts": "trigger",

    # -- Adopted existing pages: Cash-flow pressure and Bounce Back Loans --
    "can-i-lose-my-house-with-a-bounce-back-loan": "director_risk",
    "directors-liability-for-bounce-back-loans": "director_risk",
    "challenge-a-statutory-demand": "enforcement",
    "what-is-a-statutory-demand-against-a-company": "enforcement",
    "bounce-back-loan-hub": "entity_owner",
    "why-debt-is-not-always-a-bad-thing-for-your-business": "entity_owner",
    "dissolving-a-company-with-bounce-back-loan": "legal_compliance",
    "bounce-back-loan-fraud": "process_guide",
    "biggest-struggles-for-small-business-owners": "trigger",
    "cant-afford-to-pay-suppliers-what-are-the-options": "trigger",
    "cant-afford-to-repay-business-loan": "trigger",
    "cant-pay-a-commercial-lease-or-rent": "trigger",
    "cant-pay-a-company-mortgage": "trigger",
    "cant-pay-business-energy": "trigger",
    "cant-pay-business-rates": "trigger",
    "cant-pay-coronavirus-business-interruption-loan-cbils": "trigger",
    "cant-pay-staff-wages": "trigger",
    "company-cash-flow-problems": "trigger",
    "company-is-having-financial-difficulties": "trigger",
    "what-happens-if-i-default": "trigger",
    "when-employers-cant-afford-redundancy-payments": "trigger",

    # -- Adopted existing pages: Rescue, administration, CVA and pre-pack --
    "company-voluntary-arrangement-vs-administration-which-to-choose": "debt_solution_comparison",
    "vs-administrative-receivership": "debt_solution_comparison",
    "vs-cva": "debt_solution_comparison",
    "vs-liquidation": "debt_solution_comparison",
    "director-guarantees-in-a-cva": "director_risk",
    "company-administration": "entity_owner",
    "company-rescue-solutions": "entity_owner",
    "company-voluntary-arrangement": "entity_owner",
    "partnership-voluntary-arrangements": "entity_owner",
    "pre-packs": "entity_owner",
    "receivership-mean-business": "entity_owner",
    "what-is-a-pre-pack-administration": "entity_owner",
    "advantages-and-disadvantages": "recovery_strategy",
    "light-touch-administration": "recovery_strategy",
    "making-employees-redundant-cva": "recovery_strategy",
    "notice-of-intention-to-appoint-administrators": "recovery_strategy",
    "pros-and-cons": "recovery_strategy",
    "use-a-cva-to-close-a-company": "recovery_strategy",
    "what-happens-if-a-cva-fails-mid-term": "recovery_strategy",
    "when-a-cva-fails": "recovery_strategy",

    # -- Adopted existing pages: Sample letters (/sample-letters/*) --
    "sample-letters-hub": "entity_owner",
    "cease-trading-template": "process_guide",
    "hold-action-on-my-account": "process_guide",
    "i-cannot-afford-to-repay-my-debt": "process_guide",
    "i-have-no-knowledge-of-this-debt": "process_guide",
    "i-need-more-information-about-this-debt": "process_guide",
    "request-a-reduced-monthly-payment": "process_guide",
    "tell-debt-collector-to-stop-contacting-you": "process_guide",
    "write-off-my-debt": "process_guide",

    # -- Adopted existing pages: Hubs, sector distress pages and standalone guides --
    "chinese-takeaway": "case_insight",
    "director-redundancy": "director_risk",
    "care-home-insolvency": "distress_use_case",
    "charity-non-profit-insolvency": "distress_use_case",
    "construction-insolvency": "distress_use_case",
    "energy-provider-insolvency": "distress_use_case",
    "hospitality-restaurant-insolvency": "distress_use_case",
    "manufacturing-insolvency": "distress_use_case",
    "professional-services-insolvency": "distress_use_case",
    "transport-haulage-insolvency": "distress_use_case",
    "county-court-judgements": "enforcement",
    "company-rescue-recovery-hub": "entity_owner",
    "debt-creditor-pressure-hub": "entity_owner",
    "director-protection-hub": "entity_owner",
    "insolvency-news-commentary": "entity_owner",
    "sector-specific-insolvency": "entity_owner",
    "closing-a-limited-company": "process_guide",
    "business-debt-advice": "recovery_strategy",
    "debt-charities-uk": "recovery_strategy",
    "mental-health-debt-stress-support": "recovery_strategy",
    "insolvency-test": "trigger",
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
