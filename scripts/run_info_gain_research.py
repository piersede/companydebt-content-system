"""
Information Gain Research Runner
Fires off batched Deep Research prompts to fill editorial gaps across all 20 credit card pages.
Consolidates into thematic research bundles to minimise API calls.
"""
import os, time, json
from pathlib import Path
from google import genai

# Load API key from main repo .env
env_path = Path("C:/Users/piers/Downloads/companydebt-content-system/.env")
for line in env_path.read_text().splitlines():
    if line.startswith("GEMINI_API_KEY="):
        os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()
        break

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
OUT = Path("research")
OUT.mkdir(exist_ok=True)

# --- Research bundles (themed to minimise calls) ---

BUNDLES = {
    "01_rates_and_costs": {
        "title": "UK Business Credit Card Rates, Costs, and Lending Data",
        "pages_served": [
            "capital_on_tap_review", "low_apr", "best_business_credit_cards",
            "cashback_reward", "interest_free", "balance_transfer",
            "funding_circle_review", "poor_credit"
        ],
        "prompt": """Research UK business credit card rates, lending data, and cost transparency. Answer every section. If primary data is unavailable, follow the backup instruction.

SECTION 1: CAPITAL ON TAP HISTORICAL AVERAGE RATES
Primary: Compile every publicly available Capital on Tap average interest rate disclosure by quarter, going back as far as data exists. Check capitalontap.com legal pages, Companies House filings, FCA submissions, and investor materials. For each quarter provide: quarter, average rate percentage, source URL.
Backup: If only the most recent quarter exists, check third-party sources (FCA, journalists, comparison sites, Trustpilot reviews mentioning rates, Reddit) for any mentions of Capital on Tap average rates in prior periods.

SECTION 2: RATE DISTRIBUTION
Does Capital on Tap publish any data on the distribution of rates offered (e.g. what percentage of applicants receive rates below 20%, 20-35%, 35-50%, above 50%)? Check their website, FCA filings, Companies House annual accounts, and investor materials.

SECTION 3: COMPETITIVE RATE TABLE
Find the current representative APR, any published average rates, annual fees, foreign transaction fees, cashback rates, and maximum credit limits for: Barclaycard Select Cashback, Barclaycard Premium Plus, Lloyds Bank Business Card, NatWest Business Credit Card, HSBC Business Credit Card, Funding Circle Business Credit Card, Tide Business Credit Card, Metro Bank Business Credit Card, Co-op Business Credit Card, and Capital on Tap (both free and Pro tiers). Present as a comparison table with source URLs.

SECTION 4: BALANCE CARRYING DATA
What percentage of UK small businesses carrying business credit cards clear the balance in full each month vs carry a balance? Check Bank of England, UK Finance, and FCA publications from 2023-2026.

SECTION 5: TOTAL UK BUSINESS CREDIT CARD DEBT
What is the total outstanding balance on UK business credit cards? Bank of England or UK Finance data.

SECTION 6: BUSINESS VS PERSONAL CARD APR PREMIUM
What is the average personal credit card APR in the UK (from FCA or Bank of England) compared to business cards, to quantify the business card premium?

SECTION 7: 0% BUSINESS CARD HISTORY
Has any UK business credit card ever offered a genuine promotional 0% introductory APR period or 0% balance transfer rate? Check Moneyfacts, Defaqto, or archived product data from the last 5 years.

SECTION 8: CASHBACK SPECIFICS
What are Barclaycard Select Cashback's exact tier thresholds and rates? Are there caps on NatWest, Barclaycard, or Funding Circle cashback? What spend categories are excluded from Funding Circle's cashback? Has HMRC published updated guidance on business cashback tax treatment since BIM40455?

SECTION 9: FLEXIPAY FEE SCHEDULE
What is Funding Circle FlexiPay's full fee schedule by repayment term (1, 3, 6, 12 months)? Who is the card issuer behind the Funding Circle business credit card? What competing BNPL-for-business products exist in the UK (iwoca PayLater, Kriya PayLater, Liberis) and what are their terms?

SECTION 10: SECURED/POOR CREDIT PRODUCTS
Are there any UK providers offering secured business credit cards or business credit-builder products as of 2026? Check Cashplus, Suits Me, Pockit, and fintech entrants. What are the Experian/Equifax score thresholds that Capital on Tap and Funding Circle use? How long does an Experian score typically take to move from Poor (0-560) to Fair (561-720)?

FORMAT: Clear section headers matching SECTION 1-10. State primary or backup for each. Include exact URLs for every data point. Flag anything unverified."""
    },

    "02_amex_and_rewards": {
        "title": "Amex Business Cards, Rewards, and Travel Benefits",
        "pages_served": [
            "compare_amex", "capital_on_tap_vs_amex", "air_miles_avios",
            "charge_cards", "travel", "cashback_reward",
            "credit_cards_vs_charge_cards"
        ],
        "prompt": """Research American Express UK business card products, rewards programmes, and travel card benefits. Answer every section. If primary data is unavailable, follow the backup instruction.

SECTION 1: AMEX UK MERCHANT ACCEPTANCE
What is the current UK merchant acceptance rate for American Express? Check Amex investor reports, FCA data, and published network statistics. Also find country-by-country acceptance data for the US, France, Germany, Australia, and Japan.
Backup: Find the most recent published estimate from Amex, financial journalists, or industry reports.

SECTION 2: MEMBERSHIP REWARDS VALUATIONS
What are the current Membership Rewards transfer ratios to Avios, Virgin Points, Hilton Honors, and Marriott Bonvoy for UK business cardholders? What is the average pence-per-point redemption value across the top 5 redemption routes? Check HeadForPoints, FlyerTalk UK, and points valuation trackers.

SECTION 3: AMEX BUSINESS PLATINUM BENEFITS
What are the current Amex Business Platinum UK travel benefits in detail? Centurion lounge access, Priority Pass, travel insurance coverage limits (medical, cancellation, baggage, per-trip duration, geographical exclusions), and any other specific perks.

SECTION 4: AMEX PAY OVER TIME
What is the current interest rate on Amex Business Gold's "Pay Over Time" feature in the UK? What purchases qualify? What is the minimum payment? What is the interest rate on Amex Business Basic's equivalent feature?

SECTION 5: AMEX LATE PAYMENT FEES
What are the specific late payment fees for UK Amex Business Gold and Platinum charge cards? What is the escalation process (first missed payment, second, suspension)?

SECTION 6: AMEX CREDIT LIMITS
What do "no pre-set spending limit" charge cards actually offer in practice? What initial credit allowances do Amex Business Gold and Platinum typically provide to new businesses at different revenue tiers? Check forums, HeadForPoints, FlyerTalk for real-world reports.

SECTION 7: AVIOS AVAILABILITY
What is the actual reward seat availability rate on BA's most popular UK short-haul routes? Are there published studies or travel community data on how often off-peak Avios seats are bookable? What is the real-world pence-per-Avios redemption value across economy, premium economy, and business class?

SECTION 8: BA AMEX BUSINESS VS PERSONAL
Does the BA Amex Accelerating Business card earn a companion voucher at any spend threshold? What are the exact differences between the business and personal BA Amex cards?

SECTION 9: TRAVEL CARD FX FEES
What are the exact FX fees and ATM fees for Amex Business Gold and BA Amex Accelerating cards? What is the Visa and Mastercard wholesale exchange rate margin above interbank? Does NatWest's 0% FX fee apply to online overseas merchant purchases?

SECTION 10: CHARGE CARD MARKET DATA
What percentage of UK business card applications are for charge cards vs credit cards? Do UK business lenders treat charge card accounts differently from credit card accounts in credit assessments? Do Lloyds, Barclaycard, Co-op, and NatWest currently offer standalone business charge card products?

FORMAT: Clear section headers. State primary or backup for each. Include exact URLs. Flag anything unverified."""
    },

    "03_eligibility_and_underwriting": {
        "title": "UK Business Credit Card Eligibility, Approval Rates, and Underwriting",
        "pages_served": [
            "sole_traders", "start_ups", "instant_approval",
            "poor_credit", "guide_to_business_credit_cards",
            "capital_on_tap_review", "compare_barclaycard"
        ],
        "prompt": """Research UK business credit card eligibility criteria, approval processes, and underwriting practices. Answer every section. If primary data is unavailable, follow the backup instruction.

SECTION 1: SOLE TRADER NUMBERS
What is the current HMRC or ONS figure for the number of sole traders in the UK? How has it changed over 3 years? Source and URL required.

SECTION 2: APPROVAL RATES
What are the published or reported approval rates for Capital on Tap, Moss, Funding Circle, Barclaycard, and Amex business card applications? Check FCA submissions, investor reports, Companies House filings, and intermediary data. What about approval rate differentials between sole traders and limited companies?

SECTION 3: CREDIT LIMITS ACTUALLY GRANTED
What are typical credit limits actually offered to UK SMEs by provider and turnover band? Any data from FCA, providers, forums, or brokers on what businesses with £100k-£500k and £500k-£2m turnover actually receive?

SECTION 4: UNDERWRITING DATA SOURCES
What data sources do Capital on Tap, Moss, and Funding Circle use in automated underwriting? (Open Banking, Companies House, credit bureaux.) Any published details from provider documentation or FCA filings?

SECTION 5: APPLICATION EXPERIENCE
Find detailed first-hand accounts of applying for Capital on Tap, Barclaycard, and Amex business cards. How many screens/steps, what information requested, soft vs hard search, decision timeline, what the offer screen shows. Check Trustpilot, Reddit (r/UKPersonalFinance, r/UKBusiness), YouTube walkthroughs, and comparison site reviews.

SECTION 6: REAPPLICATION POLICIES
What is Capital on Tap's policy on reapplication after decline? Stated cooling-off period? Do Barclaycard or Amex publish reapplication guidance?

SECTION 7: VIRTUAL CARD CAPABILITIES
What are the specific virtual card capabilities on Capital on Tap and Moss? Contactless limits, online transaction limits, Apple Pay/Google Pay compatibility, number of virtual cards per account?

SECTION 8: SECTION 75 PROTECTION
Which specific UK business credit cards are confirmed to have Section 75 consumer protection? Provider confirmations or FCA guidance?

SECTION 9: FCA COMPLAINT DATA
What are the FCA-registered complaint volumes for Capital on Tap, Barclaycard, Amex, Lloyds, and Funding Circle business card products? Complaints per 1,000 accounts if available?

SECTION 10: ACCOUNTING SOFTWARE INTEGRATION
Which UK business credit cards have native Xero, FreeAgent, and QuickBooks bank feed integrations vs requiring manual CSV import?

SECTION 11: FCA REGULATORY CONTEXT
Has the FCA published any guidance or thematic reviews about the gap between advertised "from" rates and actual rates on business credit cards or SME lending? Any enforcement actions involving Capital on Tap? Any guidance on business card pricing transparency vs personal cards?

FORMAT: Clear section headers. State primary or backup for each. Include exact URLs. Flag anything unverified."""
    }
}


def run_research(bundle_key, bundle):
    """Fire off a single Deep Research call and save results."""
    print(f"\n{'='*60}")
    print(f"Starting: {bundle['title']}")
    print(f"Serves pages: {', '.join(bundle['pages_served'])}")
    print(f"{'='*60}")

    interaction = client.interactions.create(
        agent="deep-research-pro-preview-12-2025",
        input=bundle["prompt"],
        background=True
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
        elif interaction.status == "failed":
            err = getattr(interaction, 'error', 'Unknown error')
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

    print(f"\n{'='*60}")
    print("RESULTS SUMMARY")
    for key, status in results.items():
        print(f"  {key}: {status}")
    print(f"{'='*60}")
