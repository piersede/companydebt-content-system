"""
Information Gain Research Runner
Fires off batched Deep Research prompts to fill editorial gaps across the
credit card pages while reusing a shared prompt scaffold.
"""

import os
import time
from pathlib import Path

from google import genai

from research_prompt_utils import build_bundle_prompt


env_path = Path("C:/Users/piers/Downloads/companydebt-content-system/.env")
for line in env_path.read_text(encoding="utf-8").splitlines():
    if line.startswith("GEMINI_API_KEY="):
        os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()
        break

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
OUT = Path("research")
OUT.mkdir(exist_ok=True)


BUNDLES = {
    "01_rates_and_costs": {
        "title": "UK Business Credit Card Rates, Costs, and Lending Data",
        "pages_served": [
            "capital_on_tap_review",
            "low_apr",
            "best_business_credit_cards",
            "cashback_reward",
            "interest_free",
            "balance_transfer",
            "funding_circle_review",
            "poor_credit",
        ],
        "body": """
SECTION 1: CAPITAL ON TAP HISTORICAL AVERAGE RATES
Primary: Compile every publicly available Capital on Tap average interest rate disclosure by quarter, going back as far as data exists. Check capitalontap.com legal pages, Companies House filings, FCA submissions, and investor materials. For each quarter provide quarter, average rate percentage, and source URL.
Backup: If only the most recent quarter exists, check third-party sources for mentions of Capital on Tap average rates in prior periods.

SECTION 2: RATE DISTRIBUTION
Determine whether Capital on Tap publishes any distribution data on rates offered, including ranges such as below 20%, 20-35%, 35-50%, and above 50%.

SECTION 3: COMPETITIVE RATE TABLE
Find the current representative APR, published average rates if any, annual fees, foreign transaction fees, cashback rates, and maximum credit limits for Barclaycard Select Cashback, Barclaycard Premium Plus, Lloyds, NatWest, HSBC, Funding Circle, Tide, Metro Bank, Co-op, and Capital on Tap free and Pro tiers.

SECTION 4: BALANCE CARRYING DATA
Find what percentage of UK small businesses with business credit cards clear the balance in full each month versus carry a balance.

SECTION 5: TOTAL UK BUSINESS CREDIT CARD DEBT
Find the total outstanding balance on UK business credit cards from Bank of England or UK Finance data.

SECTION 6: BUSINESS VS PERSONAL CARD APR PREMIUM
Find the average personal credit card APR in the UK and compare it with business card APRs to quantify any business-card premium.

SECTION 7: 0% BUSINESS CARD HISTORY
Check whether any UK business credit card has offered a genuine promotional 0% introductory APR period or 0% balance transfer rate in the last five years.

SECTION 8: CASHBACK SPECIFICS
Find Barclaycard Select Cashback tier thresholds and rates, cashback caps on NatWest, Barclaycard, or Funding Circle, excluded spend categories for Funding Circle, and any updated HMRC guidance on business cashback tax treatment since BIM40455.

SECTION 9: FLEXIPAY FEE SCHEDULE
Find Funding Circle FlexiPay's full fee schedule by repayment term, the card issuer behind the Funding Circle business credit card, and key terms for competing BNPL-for-business products in the UK.

SECTION 10: SECURED OR POOR-CREDIT PRODUCTS
Check whether any UK providers offer secured business credit cards or business credit-builder products as of 2026, including Cashplus, Suits Me, Pockit, and fintech entrants. Find any published score thresholds used by Capital on Tap and Funding Circle if available.
""",
    },
    "02_amex_and_rewards": {
        "title": "Amex Business Cards, Rewards, and Travel Benefits",
        "pages_served": [
            "compare_amex",
            "capital_on_tap_vs_amex",
            "air_miles_avios",
            "charge_cards",
            "travel",
            "cashback_reward",
            "credit_cards_vs_charge_cards",
        ],
        "body": """
SECTION 1: AMEX UK MERCHANT ACCEPTANCE
Find the current UK merchant acceptance rate for American Express and, if available, country-by-country acceptance data for the US, France, Germany, Australia, and Japan. Backup to the most recent published estimates if direct network statistics are unavailable.

SECTION 2: MEMBERSHIP REWARDS VALUATIONS
Find current UK business-cardholder transfer ratios to Avios, Virgin Points, Hilton Honors, and Marriott Bonvoy, plus indicative redemption values across the strongest redemption routes.

SECTION 3: AMEX BUSINESS PLATINUM BENEFITS
Detail current UK Amex Business Platinum travel benefits including lounge access, insurance limits, trip duration limits, and relevant exclusions.

SECTION 4: AMEX PAY OVER TIME
Find the current interest rate and operating details for Amex Business Gold Pay Over Time and the equivalent feature on Amex Business Basic.

SECTION 5: AMEX LATE PAYMENT FEES
Find the specific late payment fees and escalation process for UK Amex Business Gold and Platinum charge cards.

SECTION 6: AMEX CREDIT LIMITS
Find real-world reports and any published information that clarify what no pre-set spending limit means in practice and what initial allowances are typically seen.

SECTION 7: AVIOS AVAILABILITY
Find any published studies or community-backed data on BA reward seat availability and real-world pence-per-Avios values across cabin classes.

SECTION 8: BA AMEX BUSINESS VS PERSONAL
Find whether the BA Amex Accelerating Business card earns a companion voucher and summarize the exact differences between the business and personal BA Amex cards.

SECTION 9: TRAVEL CARD FX FEES
Find exact FX and ATM fees for the key travel cards, the typical Visa and Mastercard exchange-rate margin above interbank, and whether NatWest's 0% FX fee applies to online overseas merchant purchases.

SECTION 10: CHARGE CARD MARKET DATA
Find any data on UK business charge-card versus credit-card application mix, treatment in credit assessments, and whether Lloyds, Barclaycard, Co-op, and NatWest currently offer standalone business charge cards.
""",
    },
    "03_eligibility_and_underwriting": {
        "title": "UK Business Credit Card Eligibility, Approval Rates, and Underwriting",
        "pages_served": [
            "sole_traders",
            "start_ups",
            "instant_approval",
            "poor_credit",
            "guide_to_business_credit_cards",
            "capital_on_tap_review",
            "compare_barclaycard",
        ],
        "body": """
SECTION 1: SOLE TRADER NUMBERS
Find the current HMRC or ONS figure for the number of sole traders in the UK and how it has changed over the last three years.

SECTION 2: APPROVAL RATES
Find published or reported approval rates for Capital on Tap, Moss, Funding Circle, Barclaycard, and Amex business card applications, including any sole-trader versus limited-company differentials.

SECTION 3: CREDIT LIMITS ACTUALLY GRANTED
Find typical credit limits actually offered to UK SMEs by provider and turnover band, including any reliable forum, broker, or regulatory data.

SECTION 4: UNDERWRITING DATA SOURCES
Find what data sources Capital on Tap, Moss, and Funding Circle use in automated underwriting, including Open Banking, Companies House, and credit-bureau inputs where documented.

SECTION 5: APPLICATION EXPERIENCE
Find detailed first-hand accounts of applying for Capital on Tap, Barclaycard, and Amex business cards, including step count, information requested, search type, timeline, and what the offer screen shows.

SECTION 6: REAPPLICATION POLICIES
Find reapplication policies after decline for Capital on Tap, Barclaycard, and Amex, including cooling-off periods where stated.

SECTION 7: VIRTUAL CARD CAPABILITIES
Find specific virtual card capabilities on Capital on Tap and Moss, including wallet support, limits, and virtual-card counts.

SECTION 8: SECTION 75 PROTECTION
Find which specific UK business credit cards are confirmed to have Section 75 protection, citing provider confirmations or FCA guidance.

SECTION 9: FCA COMPLAINT DATA
Find complaint volumes for Capital on Tap, Barclaycard, Amex, Lloyds, and Funding Circle business card products, plus complaints per 1,000 accounts if available.

SECTION 10: ACCOUNTING SOFTWARE INTEGRATION
Find which UK business credit cards have native Xero, FreeAgent, and QuickBooks integrations versus CSV-only workflows.

SECTION 11: FCA REGULATORY CONTEXT
Find any FCA guidance or thematic review material on advertised-from rates versus actual rates, pricing transparency, or enforcement actions relevant to business credit cards and SME lending.
""",
    },
}


def run_research(bundle_key, bundle):
    """Fire off a single Deep Research call and save results."""
    print(f"\n{'=' * 60}")
    print(f"Starting: {bundle['title']}")
    print(f"Serves pages: {', '.join(bundle['pages_served'])}")
    print(f"{'=' * 60}")

    prompt = build_bundle_prompt(
        bundle["title"],
        bundle["body"],
        extra_rules=[
            "Preserve the section headings exactly.",
            "Include exact URLs for every data point where possible.",
            "State clearly when only backup-source evidence was available.",
        ],
    )

    interaction = client.interactions.create(
        agent="deep-research-pro-preview-12-2025",
        input=prompt,
        background=True,
    )
    print(f"Interaction ID: {interaction.id}")

    poll_count = 0
    while True:
        time.sleep(15)
        poll_count += 1
        interaction = client.interactions.get(interaction.id)
        elapsed = poll_count * 15
        print(f"  [{elapsed}s] {interaction.status}")
        if interaction.status == "completed":
            result = interaction.outputs[-1].text
            out_file = OUT / f"{bundle_key}.md"
            out_file.write_text(result, encoding="utf-8")
            print(f"  Saved to {out_file} ({len(result)} chars)")
            return True
        if interaction.status == "failed":
            err = getattr(interaction, "error", "Unknown error")
            print(f"  FAILED: {err}")
            out_file = OUT / f"{bundle_key}_FAILED.txt"
            out_file.write_text(str(err), encoding="utf-8")
            return False


if __name__ == "__main__":
    print("Information Gain Research Runner")
    print(f"Bundles: {len(BUNDLES)}")
    print(f"Output directory: {OUT.resolve()}")

    results = {}
    for key, bundle in BUNDLES.items():
        success = run_research(key, bundle)
        results[key] = "completed" if success else "failed"

    print(f"\n{'=' * 60}")
    print("RESULTS SUMMARY")
    for key, status in results.items():
        print(f"  {key}: {status}")
    print(f"{'=' * 60}")
