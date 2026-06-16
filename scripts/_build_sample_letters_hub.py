"""Build and push the /sample-letters/ hub page."""
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
    section("Debt Negotiation and Repayment", [
        ("I cannot afford to repay my debt", "Template for writing to creditors when repayment is not possible", "/sample-letters/i-cannot-afford-to-repay-my-debt/"),
        ("Request a reduced monthly payment", "Ask a creditor to accept a lower payment amount", "/sample-letters/request-a-reduced-monthly-payment/"),
        ("Write off my debt", "Request that a creditor considers writing off the outstanding balance", "/sample-letters/write-off-my-debt/"),
        ("Hold action on my account", "Ask a creditor to pause collection activity while you seek advice", "/sample-letters/hold-action-on-my-account/"),
        ("Cease trading letter template", "Formal notice to creditors that the company has ceased trading", "/sample-letters/cease-trading-template/"),
    ]),
    section("Disputing and Challenging Debts", [
        ("I have no knowledge of this debt", "Template for challenging a debt you do not recognise", "/sample-letters/i-have-no-knowledge-of-this-debt/"),
        ("I need more information about this debt", "Request a creditor provide documentation before you respond", "/sample-letters/i-need-more-information-about-this-debt/"),
        ("Tell a debt collector to stop contacting you", "Exercise your right to limit contact from a debt collector", "/sample-letters/tell-debt-collector-to-stop-contacting-you/"),
    ]),
])

draft = f"""<!-- TITLE: Sample Letters Hub -->
<!-- POST ID: 53253 / TYPE: pages / AUTHOR: 34 / TEMPLATE: templates/content-page-hub_with_buttons.php -->
<!-- LINK: https://comdebstage.wpengine.com/sample-letters/ -->

<article>
<!-- wp:paragraph -->
<p>Free letter templates for directors and individuals dealing with creditor pressure. Each template covers a specific situation — choose the one that matches where you are, adapt it to your circumstances, and send it directly to your creditor or debt collector.</p>
<!-- /wp:paragraph -->

{blocks}

</article>
"""

out = ROOT / "drafts" / "53253_sample-letters-hub.html"
out.write_text(draft, encoding="utf-8")
print(f"Written: {out}")
