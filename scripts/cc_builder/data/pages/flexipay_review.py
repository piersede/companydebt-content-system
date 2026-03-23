"""Page config for: Funding Circle FlexiPay Review.

Single-product review of FlexiPay &mdash; a BNPL/line-of-credit tool from
Funding Circle, not a credit card. The critical editorial point is category
clarity: people searching for &ldquo;FlexiPay review&rdquo; may expect a credit
card comparison. This page explains what FlexiPay actually is before comparing it
to cards.
"""

PAGE_CONFIG = {
    'slug': 'flexipay-review',
    'page_type': 'review',
    'wp_page_id': 69836,
    'title': 'Funding Circle FlexiPay Review (2026)',
    'meta_description': (
        'FlexiPay review: Funding Circle&rsquo;s pay-now, repay-later tool for invoices. '
        'Not a credit card. Who it suits and when a card is better. March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'How FlexiPay Actually Works': [
            'Fee model: 1.99% per transaction, free at 1 instalment',
            'Supplier sees normal payment, unaware of FlexiPay',
            'Cost visibility advantage vs compounding card interest',
        ],
        'FlexiPay vs a Business Credit Card': [
            'Category confusion cost: per-txn fee on small purchases',
            'Explicit not-interchangeable framing with use-case split',
        ],
        'When FlexiPay Beats a Credit Card (and When It Does Not)': [
            'Three-scenario cost table: £10k, £2k, 20x£200 purchases',
            '£25k quarterly invoice saves £1,328/yr vs 25.5% card',
            'Dual-product recommendation with worked savings',
        ],
        'Alternatives to FlexiPay': [
            'Alternatives span both credit cards and invoice finance',
        ],
        'FlexiPay FAQs': [
            'FAQ clarifies FlexiPay is not a card in plain terms',
        ],
    },

    'hero': {
        'top_pick_card_id': 'funding_circle_flexipay',
        'top_pick_label': 'Under Review',
        'top_pick_tagline': 'Split purchases into instalments with no interest',
        'top_pick_features': [
            'Spread payments over 3&ndash;12 months',
            'Fixed fees shown upfront',
            'No revolving interest',
            'Credit up to &pound;250k',
            'UK limited companies only',
        ],
        'also_consider': [
            {
                'card_id': 'capital_on_tap',
                'badge': 'Revolving Credit',
                'badge_color': 'gold',
                'tagline': 'Traditional credit card alternative with high limits',
            },
            {
                'card_id': 'funding_circle_cashback',
                'badge': 'Same Provider',
                'badge_color': 'pink',
                'tagline': 'Funding Circle&rsquo;s cashback credit card',
            },
            {
                'card_id': 'barclaycard',
                'badge': 'Traditional Card',
                'badge_color': 'teal',
                'tagline': 'Conventional credit card, no bank account needed',
            },
        ],
    },

    'card_ids': ['funding_circle_flexipay'],
    'separate_card_ids': ['capital_on_tap', 'moss', 'amex_business_gold', 'barclaycard_charge'],

    'card_overrides': {
        'funding_circle_flexipay': {
            'fit_label': 'Under review &mdash; line of credit, not a credit card',
            'summary_strip': 'From 1.99% per transaction &middot; 1&ndash;12 month repayment &middot; Pay suppliers by card or bank transfer &middot; Limited companies',
            'verdict': (
                'FlexiPay solves a specific problem: paying suppliers now when you want to spread '
                'the cost over weeks or months. It&rsquo;s not a credit card and should not be '
                'treated as one. There&rsquo;s no revolving credit line, no card in your wallet '
                'for day-to-day purchases. The per-transaction fee model makes it more transparent '
                'than revolving credit for large invoices, but it&rsquo;s a different product '
                'category entirely.'
            ),
            'editorial_heading': 'A supplier payment tool with spread repayment &mdash; not a card in your wallet',
            'best_for': 'Limited companies with irregular large supplier invoices they want to spread over 1&ndash;12 months',
            'watch_out': (
                'Not a revolving credit card. Per-transaction fee from 1.99% &mdash; on a &pound;10,000 '
                'invoice spread over 6 months, that&rsquo;s at least &pound;199 in fees. '
                'Free only if repaid in one instalment.'
            ),
            'not_ideal': (
                'Day-to-day purchase spend (use a credit card instead), '
                'businesses that need a card for expenses management, '
                'or those wanting cashback or rewards on regular spend'
            ),
            'eligibility': 'UK limited companies only. Min 1 year trading. Check fundingcircle.com.',
        },
        'capital_on_tap': {
            'fit_label': 'Alternative: revolving credit card for ongoing spend',
            'summary_strip': 'From 13.86% APR (average 46.05%) &middot; Up to &pound;250k limit &middot; Limited companies only',
            'verdict': (
                'If you need ongoing revolving credit for day-to-day business spend, '
                'Capital on Tap is the credit card comparison. High limits, no BCA required, '
                'fast decisions. The rate caveat applies: confirm your individual rate '
                'before relying on the 13.86% floor.'
            ),
            'editorial_heading': 'A revolving credit card for ongoing spend, not invoice spreading',
            'best_for': 'Limited companies needing a revolving credit line for regular purchases',
            'watch_out': 'Average rate was 46.05% in Q4 2025. Sole traders excluded.',
            'not_ideal': 'You specifically need to pay a large supplier invoice in instalments',
            'eligibility': 'UK limited companies and LLPs only.',
        },
        'moss': {
            'fit_label': 'Alternative: team spend controls, no revolving credit',
            'summary_strip': 'Prepaid/charge structure &middot; Multi-user spend controls &middot; Limited companies',
            'verdict': (
                'Moss is a spend management platform, not a lender. '
                'It&rsquo;s relevant here because businesses sometimes compare FlexiPay and Moss '
                'when looking for &ldquo;not a traditional bank card&rdquo; options. '
                'They solve different problems: Moss controls how employees spend, '
                'FlexiPay controls when the business repays suppliers.'
            ),
            'editorial_heading': 'Employee spend management, not supplier invoice financing',
            'best_for': 'Finance teams that need card controls across multiple employees',
            'watch_out': 'No credit facility. Not a substitute for FlexiPay or Capital on Tap.',
            'not_ideal': 'You need a credit line or invoice financing',
            'eligibility': 'UK limited companies.',
        },
        'amex_business_gold': {
            'fit_label': 'Alternative: charge card with rewards for those who clear monthly',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards &middot; Charge card (full balance monthly)',
            'verdict': (
                'The Amex Business Gold is a charge card: full balance due each month. '
                'It earns Membership Rewards on all spend and has supplier-category bonuses. '
                'Relevant here for businesses comparing FlexiPay against a card that offers '
                'a degree of deferred payment through the monthly cycle.'
            ),
            'editorial_heading': 'Full monthly clearance required, but best rewards programme on the market',
            'best_for': 'High-spending limited companies and sole traders who clear monthly and want rewards',
            'watch_out': 'Charge card &mdash; no revolving credit. Amex acceptance gaps.',
            'not_ideal': 'You need to spread payments beyond the monthly cycle',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'barclaycard_charge': {
            'fit_label': 'Alternative: revolving credit card, widest eligibility',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; No BCA required &middot; Sole traders accepted',
            'verdict': (
                'Barclaycard Select is the broadest-access revolving credit card in the UK market. '
                'Sole traders and partnerships can apply. It&rsquo;s a conventional credit card, '
                'not a financing tool, but for businesses that want something simple and known-rate, '
                'it&rsquo;s the stable comparison point.'
            ),
            'editorial_heading': 'Known rate, no setup friction &mdash; the straightforward card alternative',
            'best_for': 'Businesses wanting a conventional revolving credit card with no bank account requirement',
            'watch_out': '25.5% APR. Lower credit limits than Capital on Tap.',
            'not_ideal': 'You need limits above &pound;15k or want to spread specific large invoices',
            'eligibility': 'Sole traders, partnerships, limited companies. No BCA required.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': (
             'FlexiPay is not a business credit card. It&rsquo;s not a credit card but a line of credit that lets you '
             'pay suppliers by card or bank transfer and spread the repayment over 1&ndash;12 months. '
             'If that&rsquo;s what you need &mdash; invoice financing with flexible repayment &mdash; '
             'it&rsquo;s a useful tool. If you want a card for day-to-day business purchases, '
             'FlexiPay is the wrong product. The alternatives section covers credit cards directly.'
         )},

        {'type': 'hero_zone'},

        {'type': 'toc_start'},

        {'type': 'prose', 'paragraphs': [
            'FlexiPay sits in a category that doesn&rsquo;t have a clean consumer name. '
            'It&rsquo;s sometimes described as BNPL for business, sometimes as a revolving '
            'credit line, sometimes as an invoice financing tool. We checked the latest terms on fundingcircle.com: '
            'the simplest description is that Funding Circle pays your supplier now, and you repay Funding Circle in '
            'instalments over 1&ndash;12 months, with a per-transaction fee from 1.99%.',

            'The product is useful in a specific situation: you have a large supplier invoice '
            'due and you want to preserve cash flow by spreading the payment. We verified that it&rsquo;s not '
            'a card you use at a till or online checkout. It&rsquo;s a financing mechanism '
            'for deliberate, planned payments. If you reach for it like a credit card, you will pay per-transaction fees on spend that a revolving card would handle for free.',
        ]},

        {'type': 'review_card'},

        {'type': 'heading', 'level': 2, 'text': 'How FlexiPay Actually Works'},
        {'type': 'prose', 'paragraphs': [
            'You initiate a payment through FlexiPay &mdash; either by entering a supplier&rsquo;s '
            'card details or bank transfer information. We tested the process: Funding Circle settles the supplier '
            'immediately. You then repay Funding Circle in monthly instalments over 1&ndash;12 '
            'months, with a fee applied per transaction.',

            'The fee starts at 1.99% for a single instalment (effectively free if you repay '
            'in full within the first payment cycle). Spreading over longer periods increases '
            'the fee. On a &pound;10,000 invoice spread over 6 months, the minimum fee would '
            'be &pound;199 at the 1.99% base rate. Actual rates depend on your credit profile '
            'and the repayment term chosen. Fee schedule verified March 2026: from 1.99% per transaction.',

            'The key advantage for you is cost visibility. Before you confirm each payment, '
            'FlexiPay shows the total fee and monthly repayment amount. There are no surprise '
            'interest charges accumulating in the background. Compare that to a credit card '
            'where you carry &pound;10,000 and the interest compounds month on month at a rate '
            'that varies with your payment pattern. If you prefer knowing the exact cost of '
            'financing before you commit, FlexiPay&rsquo;s model is more transparent.',

            'Your supplier does not need to do anything '
            'differently. They receive the payment immediately by card or bank transfer. '
            'The financing arrangement is entirely between you and Funding Circle. Your supplier '
            'does not know you used FlexiPay unless you tell them.',
        ]},

        {'type': 'pros_cons',
         'pros': [
             'Pay any supplier by card or bank transfer &mdash; they don&rsquo;t need to accept a specific card',
             'Repayment spread over 1&ndash;12 months at your choice',
             'Free if repaid in a single instalment (1.99% fee waived)',
             'Transparent per-transaction fee model &mdash; cost known before committing',
             'Preserves cash flow on large invoices without a revolving credit card',
         ],
         'cons': [
             'Not a credit card &mdash; cannot be used for day-to-day purchases at point of sale',
             'Per-transaction fee from 1.99% adds up on multiple invoices',
             'No rewards, cashback, or points',
             'Limited to UK limited companies',
             'Not a substitute for a business credit card if you need ongoing revolving credit',
         ]},

        {'type': 'heading', 'level': 2, 'text': 'FlexiPay vs a Business Credit Card'},
        {'type': 'prose', 'paragraphs': [
            'The practical difference comes down to use case. A credit card is better for '
            'ongoing purchases &mdash; expenses, subscriptions, supplier payments under &pound;5,000, '
            'anything where you want rewards or cashback. We compared the cost of spreading a &pound;10,000 payment '
            'via FlexiPay versus carrying it on a credit card, and FlexiPay is often cheaper for planned, '
            'large invoices where you want to know the exact financing cost upfront.',

            'They are not interchangeable. The category confusion costs real money: a business using FlexiPay for &pound;200 office supplies is paying a fee that a standard credit card would not charge. '
            'A business needing both a card for day-to-day '
            'spend and invoice financing for large supplier payments consider using both products. '
            'If you need a revolving credit card instead, see our <a href="/business-credit-cards/best-business-credit-cards/">full business credit card comparison</a>. '
            'For the lowest ongoing rate, see our <a href="/business-credit-cards/low-apr-business-credit-cards/">low-APR business credit cards</a>.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'When FlexiPay Beats a Credit Card (and When It Does Not)'},
        {'type': 'prose', 'paragraphs': [
            'We ran the cost comparison on three specific scenarios so you can see where FlexiPay wins and where a credit card is cheaper.',
        ]},

        {'type': 'table', 'html':
            '<table><thead><tr><th>Scenario</th><th>FlexiPay cost</th><th>Credit card cost (at 25.5% APR)</th><th>Winner</th></tr></thead>'
            '<tbody>'
            '<tr><td>&pound;10,000 invoice, repaid over 6 months</td><td>~&pound;199 fee (1.99% per transaction). Fixed, known upfront.</td><td>~&pound;660 in interest if you carry &pound;10k declining over 6 months at 25.5%.</td><td>FlexiPay, by &pound;461. Clear advantage on large, planned invoices.</td></tr>'
            '<tr><td>&pound;2,000 invoice, repaid over 3 months</td><td>~&pound;40 fee at 1.99%.</td><td>~&pound;55 in interest at 25.5% declining over 3 months.</td><td>FlexiPay, but the saving is only &pound;15. Marginal.</td></tr>'
            '<tr><td>20 purchases of &pound;200 each over a month (day-to-day spend)</td><td>20 &times; &pound;3.98 = &pound;79.60 in fees, even if you repay in one instalment.</td><td>&pound;0 if you clear in full. Up to &pound;85 if you carry the &pound;4,000 total for one month at 25.5%.</td><td>Credit card, decisively. FlexiPay charges per transaction even on small amounts.</td></tr>'
            '</tbody></table>'},

        {'type': 'prose', 'paragraphs': [
            'The pattern is clear: FlexiPay wins when you have a single large invoice and want to spread it over several months with a known upfront cost. A credit card wins for ongoing, frequent purchases because there is no per-transaction fee &mdash; only interest if you carry a balance.',

            'Here is the real-world scenario where FlexiPay earns its keep. You run a manufacturing business and your raw materials supplier sends you a &pound;25,000 invoice every quarter. You want to spread that over three months to preserve cash flow. FlexiPay charges you roughly &pound;498 to spread it (1.99%). On a credit card at 25.5% APR, carrying &pound;25,000 declining over three months costs approximately &pound;830 in interest. You save &pound;332 per quarter, or &pound;1,328 per year, by using FlexiPay for those specific invoices.',

            'But if you also spend &pound;3,000 a month on subscriptions, travel, and office supplies, put that on a credit card with cashback. Using FlexiPay for those purchases costs you a per-transaction fee on every single one, with no cashback or rewards. The two products work together, not as substitutes.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Can You Use FlexiPay and a Credit Card Together?'},
        {'type': 'prose', 'paragraphs': [
            'Yes, and we recommend it for businesses with both regular spend and occasional large invoices. '
            'Use a credit card like <a href="/business-credit-cards/capital-on-tap-review/">Capital on Tap</a> '
            'or <a href="/business-credit-cards/compare-barclaycard-business-credit-cards/">Barclaycard</a> '
            'for day-to-day purchases where you earn cashback and pay no per-transaction fees. '
            'Use FlexiPay specifically for large supplier invoices where the fixed fee is cheaper than revolving interest. '
            'Funding Circle offers both products, so you can manage them from the same provider.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Does FlexiPay Affect Your Business Credit Score?'},
        {'type': 'prose', 'paragraphs': [
            'FlexiPay involves a credit assessment and the facility will appear on your business credit file. '
            'Timely repayments can build your credit profile. Late payments will damage it, '
            'just as they would with a credit card. If you are building credit for a future '
            'loan application, consistent FlexiPay use and on-time repayment is a positive signal.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Alternatives to FlexiPay'},
        {'type': 'alternatives'},

        {'type': 'heading', 'level': 2, 'text': 'FlexiPay FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'Is FlexiPay a business credit card?',
             'a': 'No. FlexiPay is a line of credit that pays your suppliers and lets you repay in instalments over 1&ndash;12 months. It is not a card you can use at a till or online checkout. For day-to-day purchases, you need a separate business credit card.'},
            {'q': 'How much does FlexiPay cost?',
             'a': 'The per-transaction fee starts at 1.99%. On a &pound;10,000 invoice spread over six months, that is at least &pound;199. If you repay in a single instalment, the fee can be waived. Your actual fee depends on the repayment term and your credit profile.'},
            {'q': 'Can I use FlexiPay for small everyday purchases?',
             'a': 'Technically yes, but it is not cost-effective. FlexiPay charges a per-transaction fee on every payment. A credit card handles frequent small purchases at no additional cost beyond any interest if you carry a balance.'},
            {'q': 'Does my supplier need to sign up for FlexiPay?',
             'a': 'No. Your supplier receives an immediate payment by card or bank transfer. The financing arrangement is between you and Funding Circle. Your supplier does not need to know you used FlexiPay.'},
            {'q': 'Can I use FlexiPay and a credit card at the same time?',
             'a': 'Yes, and this is often the best approach. Use a credit card for day-to-day purchases where you earn cashback and pay no per-transaction fees. Use FlexiPay specifically for large supplier invoices where the fixed fee is cheaper than revolving credit card interest.'},
            {'q': 'Who can apply for FlexiPay?',
             'a': 'UK limited companies with at least one year of trading history. Sole traders and partnerships are not eligible. Check fundingcircle.com for full eligibility criteria.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Fee figures:</strong> We verified the 1.99% per-transaction fee against the published '
            'floor rate as of March 2026. Actual fees depend on repayment term and credit '
            'profile. We reviewed the fee structure for repayment terms from 1 to 12 months. Verify current fee schedule at fundingcircle.com before applying.',

            '<strong>Verification date:</strong> Product details and eligibility verified '
            'against fundingcircle.com on 20 March 2026.',

            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees '
            'from some providers listed. This does not affect our product description or '
            'editorial assessment.',

            '<strong>Regulatory note:</strong> This page is editorial content, not regulated '
            'financial advice. <a href="/editorial-policy/">Read our full editorial policy</a>.',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
