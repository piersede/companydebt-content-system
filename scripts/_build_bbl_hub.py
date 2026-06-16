"""Build and push the /bounce-back-loan-support-hub/ hub page."""
import pathlib, sys
sys.path.insert(0, '.')

ROOT = pathlib.Path(__file__).resolve().parents[1]


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


def section(heading, items):
    return (
        f'<!-- wp:heading {{"level":3}} -->\n'
        f'<h3 class="wp-block-heading">{heading}</h3>\n'
        f'<!-- /wp:heading -->\n\n'
        f'{card_grid(items)}'
    )


blocks = "\n\n".join([
    section("Repayment, Default and Director Liability", [
        ("What happens if I default on a Bounce Back Loan?", "The government guarantee, lender options, and your exposure", "/bounce-back-loan-support-hub/what-happens-if-i-default/"),
        ("Directors' liability for Bounce Back Loans", "When personal liability arises from a government-backed loan", "/bounce-back-loan-support-hub/directors-liability-for-bounce-back-loans/"),
        ("Can I lose my house with a Bounce Back Loan?", "Personal assets and the BBL — what is actually at risk", "/bounce-back-loan-support-hub/can-i-lose-my-house-with-a-bounce-back-loan/"),
        ("Bounce Back Loan fraud", "What counts as misuse and how it is investigated", "/bounce-back-loan-support-hub/bounce-back-loan-fraud/"),
    ]),
    section("Closing a Company with a Bounce Back Loan", [
        ("Dissolving a company with a Bounce Back Loan", "Why strike-off is blocked and what to do instead", "/bounce-back-loan-support-hub/dissolving-a-company-with-bounce-back-loan/"),
        ("Can't pay a CBILS loan", "Options when a Coronavirus Business Interruption Loan can't be repaid", "/bounce-back-loan-support-hub/cant-pay-coronavirus-business-interruption-loan-cbils/"),
    ]),
])

draft = f"""<!-- TITLE: Bounce Back Loan Support Hub -->
<!-- POST ID: 43758 / TYPE: pages / AUTHOR: 34 / TEMPLATE: templates/content-page-hub_with_buttons.php -->
<!-- LINK: https://comdebstage.wpengine.com/bounce-back-loan-support-hub/ -->

<article>
<!-- wp:paragraph -->
<p>Most Bounce Back Loans were taken out quickly and with limited advice. The questions that follow tend to arrive later: what happens if the company can't repay, whether the director carries personal liability, and whether the company can be closed with the loan still outstanding. This hub covers those questions.</p>
<!-- /wp:paragraph -->

{blocks}

</article>
"""

out = ROOT / "drafts" / "43758_bounce-back-loan-hub.html"
out.write_text(draft, encoding="utf-8")
print(f"Written: {out}")
