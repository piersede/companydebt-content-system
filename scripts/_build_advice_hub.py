"""Rebuild the /advice/ hub page with individual per-page cards."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Each section: (heading, [(title, descriptor, url), ...])
SECTIONS = [
    ("Personal Liability", [
        ("Are directors personally liable for company debts?", "When limited liability does not protect you", "/advice/are-directors-personally-liable-for-company-debts/"),
        ("Can a director be made bankrupt?", "Personal insolvency risk after company failure", "/advice/can-a-director-be-made-bankrupt-if-a-business-fails/"),
        ("Can personal assets be seized from a limited company?", "When creditors can come after your property", "/advice/can-personal-assets-of-directors-be-seized-from-a-ltd-company/"),
        ("Losing your house if the company goes bust", "When your home is at risk", "/advice/losing-house-if-company-goes-bust/"),
        ("What is limited liability?", "What the protection actually covers", "/advice/what-is-limited-liability/"),
        ("Misfeasance", "The civil claim liquidators use most", "/advice/misfeasance/"),
    ]),
    ("Personal Guarantees", [
        ("The risks of signing a personal guarantee", "What you are agreeing to before you sign", "/advice/the-risks-of-signing-a-personal-guarantee/"),
        ("Directors' personal guarantees", "How guarantees work and when they crystallise", "/advice/directors-personal-guarantees/"),
        ("Unenforceable personal guarantee", "When a PG can be challenged", "/advice/unenforceable-personal-guarantee/"),
        ("Personal guarantee insurance", "Covering the liability before it is called", "/advice/personal-guarantee-insurance/"),
        ("Personal liability for CBILS loans", "Government-backed loans and personal exposure", "/advice/personal-liability-for-cbils-loans/"),
    ]),
    ("Director Duties and Conduct", [
        ("Duties and responsibilities of a company director", "The legal framework directors operate under", "/advice/what-are-the-duties-and-responsibilities-of-a-company-director/"),
        ("Directors' duties to creditors", "When your duty shifts from shareholders to creditors", "/advice/directors-duties-to-creditors/"),
        ("Avoiding and disclosing conflicts of interest", "Section 175 and 177 CA 2006 obligations", "/advice/what-are-a-company-directors-duties-to-avoid-and-disclose-conflicts-of-interest/"),
        ("Companies Act 2006", "The legislation that governs directors' conduct", "/advice/what-is-the-companies-act-2006/"),
        ("Director's responsibility for accountancy errors", "When the accounts go wrong", "/advice/what-is-a-directors-responsibility-for-accountancy-errors/"),
        ("Preventing company director disputes", "Board conflict before it reaches a lawyer", "/advice/preventing-company-director-disputes/"),
    ]),
    ("Director Consequences", [
        ("Directors' disqualification", "How the Insolvency Service investigates conduct", "/advice/directors-disqualification/"),
        ("Can a director get a criminal record?", "When misconduct becomes criminal", "/advice/can-director-criminal-record/"),
        ("Phoenix companies explained", "Legal phoenixing vs. restricted conduct", "/advice/what-are-phoenix-companies/"),
        ("Frozen company bank account", "Why banks freeze accounts and what to do", "/advice/frozen-bank-account/"),
        ("HMRC IR35 investigations", "Off-payroll working rules and enforcement", "/advice/hmrcs-ir35-investigations-different/"),
    ]),
    ("Directors' Loans and Company Finance", [
        ("How to legally take money out of a limited company", "Salary, dividends, and loans in the right order", "/advice/how-to-legally-take-money-out-of-a-limited-company/"),
        ("Overdrawn directors' loan accounts", "When the loan account creates a debt to the company", "/advice/overdrawn-directors-loan-accounts/"),
        ("Writing off a director's loan account", "Tax implications and when it is possible", "/advice/writing-off-a-directors-loan-account/"),
        ("Fixed and floating charges", "What lenders hold over company assets", "/advice/what-are-fixed-and-floating-charges/"),
        ("Funding options for SMEs", "Finance routes when growth stalls", "/advice/funding-options-for-smes-in-the-uk/"),
    ]),
    ("Getting Advice", [
        ("Insolvency advice for directors", "What to ask an IP before the procedure starts", "/advice/insolvency-advice-for-directors/"),
        ("Get free business debt advice", "Where to get independent guidance", "/advice/get-free-business-debt-advice/"),
        ("Business restructuring", "Options before a formal procedure", "/advice/business-restructuring/"),
        ("Debt management guide", "Prioritising and negotiating company debts", "/advice/debt-management-guide/"),
    ]),
]


def card_grid(items):
    cards = "\n".join(
        f'  <a class="cd-hub-card" href="{url}">\n'
        f'    <span class="cd-hub-card__title">{title}</span>\n'
        f'    <span class="cd-hub-card__desc">{desc}</span>\n'
        f'  </a>'
        for title, desc, url in items
    )
    return (
        "<!-- wp:html -->\n"
        '<div class="cd-hub-grid">\n'
        f"{cards}\n"
        "</div>\n"
        "<!-- /wp:html -->"
    )


blocks = []
for heading, items in SECTIONS:
    blocks.append(
        f'<!-- wp:heading {{"level":3}} -->\n'
        f'<h3 class="wp-block-heading">{heading}</h3>\n'
        f'<!-- /wp:heading -->\n\n'
        f'{card_grid(items)}'
    )

content = "\n\n".join(blocks)

draft = f"""<!-- TITLE: Director Advice Hub -->
<!-- POST ID: 68153 / TYPE: pages / AUTHOR: 34 / TEMPLATE: templates/content-page-hub_with_buttons.php -->
<!-- LINK: https://comdebstage.wpengine.com/advice/ -->

<article>
<!-- wp:paragraph -->
<p>Most of the questions directors bring us are not about insolvency procedure. They are about what happens to them personally: whether the guarantee they signed three years ago will follow them home, whether the loan account creates a liability, whether stopping trading now makes things better or worse. This hub covers the personal side of company distress.</p>
<!-- /wp:paragraph -->

{content}

</article>
"""

out = ROOT / "drafts" / "68153_advice-hub.html"
out.write_text(draft, encoding="utf-8")
print(f"Written: {out}")
