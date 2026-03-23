"""Page config for: Funding Circle Business Credit Card Review.

Single-product review of the Funding Circle Cashback Business Credit Card.
Key points: 2% cashback for 6 months (capped at &pound;2k), then 1% uncapped,
no annual fee, but 34.9% representative APR. Only worth it if you clear monthly.
"""

PAGE_CONFIG = {
    'slug': 'funding-circle-business-credit-card-review',
    'page_type': 'review',
    'wp_page_id': 69831,
    'title': 'Funding Circle Business Credit Card Review (2026)',
    'meta_description': (
        'Funding Circle business credit card review: 2% cashback for 6 months then 1% uncapped, '
        'no annual fee, 34.9% APR. Who it suits. Verified March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Funding Circle Cashback Structure': [
            '£100k spend needed to hit £2k intro cap, most won\'t',
            'Net cashback at three spend levels with no annual fee offset',
        ],
        'Funding Circle Rates and Fees': [
            'Carried-balance cost calculated: £87/month on £3k at 34.9%',
            '0% FX fee verified March 2026 vs 2.75-2.99% market norm',
            'Tide card is actually Capital on Tap via Funding Options',
        ],
        'Cashback vs Interest: The Break-Even Math': [
            'Break-even table at £1.5k, £3k, £5k monthly spend levels',
            'One carried month per quarter nearly zeroes net benefit',
            'Year-one intro buffer calculated: £540 at £3k/month',
            'Crossover point: 5 carried months tips net negative',
        ],
        'Alternatives to Funding Circle': [
            'Alternatives framed around payment-discipline threshold',
        ],
        'Funding Circle FAQs': [
            'Sole trader eligibility gap flagged as unconfirmed',
        ],
    },

    'hero': {
        'top_pick_card_id': 'funding_circle_cashback',
        'top_pick_label': 'Under Review',
        'top_pick_tagline': '2% intro cashback, then 1% uncapped',
        'top_pick_features': [
            '2% cashback for first 6 months',
            '1% cashback uncapped after that',
            'No annual fee',
            'No foreign transaction fees',
            'Credit up to &pound;250k',
            'Unlimited employee cards',
        ],
        'also_consider': [
            {
                'card_id': 'capital_on_tap',
                'badge': 'Higher Limits',
                'badge_color': 'gold',
                'tagline': 'Up to &pound;250k credit, no bank account needed',
            },
            {
                'card_id': 'moss',
                'badge': 'Expense Management',
                'badge_color': 'pink',
                'tagline': 'Team spend controls and card management',
            },
            {
                'card_id': 'barclaycard',
                'badge': 'Open Access',
                'badge_color': 'teal',
                'tagline': 'Sole traders accepted, no bank account required',
            },
        ],
    },

    'card_ids': ['funding_circle_cashback'],
    'separate_card_ids': ['capital_on_tap', 'barclaycard', 'santander'],

    'card_overrides': {
        'funding_circle_cashback': {
            'fit_label': 'Under review',
            'summary_strip': '34.9% rep. APR &middot; 2% cashback for 6 months, then 1% &middot; No annual fee &middot; No BCA required',
            'verdict': (
                'The cashback structure is one of the more competitive on the UK market, '
                'and there&rsquo;s no annual fee to offset. The catch is a 34.9% representative APR. '
                'If you clear the balance monthly, the cashback is real. If you carry a balance, '
                'the interest wipes it out quickly. This is a card for businesses with disciplined '
                'payment habits, not for managing cash flow gaps.'
            ),
            'editorial_heading': 'Good cashback structure, no annual fee &mdash; but only works if you clear monthly',
            'best_for': 'Businesses with &pound;2k&ndash;&pound;5k/month card spend that clear the balance each month and want simple cashback',
            'watch_out': '34.9% rep. APR. The 2% introductory rate is capped at &pound;2,000 in cashback. After 6 months, the rate drops to 1% (uncapped).',
            'not_ideal': 'You carry a balance, need a credit limit above &pound;30k, or want a rewards programme rather than cashback',
            'eligibility': 'Limited companies only (sole traders excluded) directly on fundingcircle.com',
        },
        'capital_on_tap': {
            'fit_label': 'Alternative: higher limits, but rate uncertainty',
            'summary_strip': 'From 13.86% APR (average 46.05%) &middot; Up to &pound;250k limit &middot; Limited companies only',
            'verdict': (
                'Capital on Tap offers far higher credit limits and no BCA requirement. '
                'The floor rate of 13.86% is lower than Funding Circle&rsquo;s 34.9%, '
                'but the average rate in Q4 2025 was 46.05%. If you need a large credit line '
                'and are a limited company, Capital on Tap is worth applying for &mdash; '
                'but confirm your individual rate before committing.'
            ),
            'editorial_heading': 'Higher limits, but confirm your rate &mdash; the average is 46.05%',
            'best_for': 'Limited companies needing credit limits above &pound;30k',
            'watch_out': 'Sole traders excluded. Average rate (46.05% Q4 2025) is far above the floor.',
            'not_ideal': 'Sole traders, or businesses that want a known rate upfront',
            'eligibility': 'UK limited companies and LLPs only.',
        },
        'barclaycard': {
            'fit_label': 'Alternative: known rate, sole traders accepted',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; No bank account required',
            'verdict': (
                'Barclaycard&rsquo;s 25.5% rep. APR is higher than Funding Circle&rsquo;s floor '
                'and lower than Funding Circle&rsquo;s actual rate in practice. '
                'No cashback, but you get a known rate from the outset and sole traders can apply.'
            ),
            'editorial_heading': 'Known rate, no cashback &mdash; the stable alternative if APR certainty matters',
            'best_for': 'Businesses that carry a balance occasionally and want a predictable rate',
            'watch_out': 'No cashback. 25.5% APR is still a significant borrowing cost.',
            'not_ideal': 'You clear monthly and want to earn cashback on spend',
            'eligibility': 'Sole traders, partnerships, limited companies. No BCA required.',
        },
        'santander': {
            'fit_label': 'Alternative: cashback at a lower APR',
            'summary_strip': '23.7% APR &middot; 1% cashback &middot; Santander BCA required',
            'verdict': (
                'Santander offers 1% cashback at a lower representative APR than Funding Circle. '
                'The trade-off: you need a Santander business current account. '
                'If you already bank with Santander, this is the cheaper cashback option.'
            ),
            'editorial_heading': 'Cheaper APR with 1% cashback &mdash; if you bank with Santander',
            'best_for': 'Businesses already banking with Santander who want cashback at a lower rate',
            'watch_out': 'Santander BCA required. Sole trader eligibility not confirmed on public pages.',
            'not_ideal': 'You don&rsquo;t bank with Santander or don&rsquo;t want to switch',
            'eligibility': 'Santander BCA required. Sole trader eligibility: not confirmed on public pages.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': (
             'The Funding Circle cashback card, measured against its direct competitors, comes down to simple maths. At &pound;3,000/month, you earn '
             '&pound;360 in year one and &pound;360 annually after that &mdash; against zero annual fee. '
             'If you carry a balance, the 34.9% APR cancels that out fast. The decision hinges '
             'entirely on your payment discipline.'
         )},

        {'type': 'hero_zone'},

        {'type': 'toc_start'},

        {'type': 'prose', 'paragraphs': [
            'Funding Circle is better known as a business loan platform, but it has been running '
            'a business credit card for several years. We verified the current terms on fundingcircle.com '
            'and the card earns cashback, charges no annual '
            'fee, and requires no business current account. That is a competitive combination '
            'on paper.',

            'The 34.9% representative APR is the number that changes the calculation. Compared against every card on our <a href="/business-credit-cards/best-business-credit-cards/">main roundup</a> '
            'and it is one of the higher rates among UK business credit cards. The cashback makes sense '
            'only for businesses that genuinely clear the balance each month and treat the card '
            'as a spend tool, not a credit line.',

            'If you run an accounting practice spending &pound;2,500 a month on software subscriptions '
            'and office costs, and you clear the balance on the due date every month without exception, '
            'this card pays you &pound;300 a year for doing what you already do. No fee, no complexity. '
            'If you run a retail business that sometimes carries &pound;5,000 of stock purchases into '
            'the next billing cycle, the 34.9% interest on that carried balance costs more than the '
            'cashback earns. Your payment pattern determines whether this card is free money or expensive debt.',

            'One thing worth clarifying: Tide advertises a business credit card, but it is not issued '
            'by Tide. The Tide credit card is powered by Capital on Tap (via Funding Options). If you '
            'apply through Tide, you are getting a Capital on Tap product with Tide branding. The terms, '
            'rates, and underwriting are Capital on Tap&rsquo;s, not Tide&rsquo;s. That matters if you are '
            'comparing Funding Circle against what you think is a Tide card &mdash; you are actually '
            'comparing against Capital on Tap.',
        ]},

        {'type': 'review_card'},

        {'type': 'heading', 'level': 2, 'text': 'Funding Circle Cashback Structure'},
        {'type': 'prose', 'paragraphs': [
            'We checked the introductory terms: 2% cashback on all spend for the first six months, '
            'capped at &pound;2,000 total cashback earned. To hit that cap you&rsquo;d need to '
            'spend &pound;100,000 in the first six months. Most businesses won&rsquo;t reach '
            'the cap, so treat 2% as your actual introductory rate.',

            'After six months the rate drops to 1% with no cap. At &pound;3,000/month that&rsquo;s '
            '&pound;360/year in cashback. At &pound;5,000/month it&rsquo;s &pound;600/year. '
            'There is no annual fee to offset, so the cashback is net positive as long as '
            'you clear the balance.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Funding Circle Rates and Fees'},
        {'type': 'prose', 'paragraphs': [
            'We calculated the cost of carrying a balance at this rate: at &pound;3,000 outstanding, '
            'one month of interest costs around &pound;87 &mdash; erasing nearly three months '
            'of cashback at 1%. Cashback and interest do not coexist productively. '
            'This is a card for zero-balance users.',

            'There is no annual fee, which removes the usual fixed-cost threshold you need '
            'to hit before the card breaks even. The card also charges 0% on foreign transactions '
            '(source: Funding Circle product page, verified March 2026), which is a genuine differentiator &mdash; most business credit cards '
            'charge 2.75%&ndash;2.99% on non-sterling spend. If your business pays overseas suppliers or '
            'travels internationally, the FX saving alone could be worth more than the cashback. '
            'We recommend comparing this rate against '
            'lower-APR alternatives on our <a href="/business-credit-cards/low-apr-business-credit-cards/">low APR '
            'business credit cards</a> page. The cashback is genuinely incremental for '
            'low-to-mid spend businesses as long as the payment discipline is there.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Cashback vs Interest: The Break-Even Math'},
        {'type': 'prose', 'paragraphs': [
            'The numbers at three typical monthly spend levels show exactly where '
            'the cashback-vs-interest line sits. The pattern is unambiguous: even one month of '
            'carried balance per quarter destroys most of the cashback return.',
        ]},

        {'type': 'table', 'html':
            '<table><thead><tr><th>Monthly spend</th><th>Annual cashback (1% after intro)</th><th>Cost of carrying balance for 1 month</th><th>Net if you carry 1 month per quarter</th></tr></thead>'
            '<tbody>'
            '<tr><td>&pound;1,500/month</td><td>&pound;180/year</td><td>&pound;44 per carried month</td><td>+&pound;4/year. Barely positive. One extra carried month tips you negative.</td></tr>'
            '<tr><td>&pound;3,000/month</td><td>&pound;360/year</td><td>&pound;87 per carried month</td><td>+&pound;12/year. Negligible net benefit.</td></tr>'
            '<tr><td>&pound;5,000/month</td><td>&pound;600/year</td><td>&pound;145 per carried month</td><td>+&pound;20/year. Still barely worth it if you carry at all.</td></tr>'
            '</tbody></table>'},

        {'type': 'prose', 'paragraphs': [
            'At &pound;3,000/month, four carried months in a year cost you &pound;348 in interest. '
            'Your annual cashback is &pound;360. Net gain: &pound;12. You have spent a full year '
            'managing a credit card for twelve pounds. If you carry five months instead of four, '
            'you are in the red.',

            'The introductory 2% rate in months one to six improves the first-year picture. '
            'At &pound;3,000/month, you earn &pound;360 in the first six months (2% rate) '
            'plus &pound;180 in the second half (1% rate), totalling &pound;540 in year one. '
            'That gives you a meaningful buffer even if you carry a balance once or twice. '
            'But from year two onwards, you are back to 1% and the margins tighten.',

            'The conclusion is straightforward: if you clear every month, this card earns you '
            'free money with no annual fee to offset. If you carry a balance more than once '
            'a quarter, the 34.9% APR makes the cashback irrelevant. You should look at '
            'Lloyds (15.95% APR) or even Barclaycard (25.5% APR) instead, even without cashback, '
            'because the interest savings exceed the cashback you would have earned. '
            'We compared these scenarios across all major cards on our '
            '<a href="/business-credit-cards/best-business-credit-cards/">main comparison page</a>.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Does the 2% Introductory Rate Make Up for a Bad First Half-Year?'},
        {'type': 'prose', 'paragraphs': [
            'If you carry a balance in every month of the introductory period, no. At &pound;3,000 '
            'outstanding for all six months, you pay roughly &pound;522 in interest while earning '
            '&pound;360 in cashback at 2%. You are &pound;162 in the red before you even reach '
            'the standard rate. The introductory rate is a bonus for disciplined payers, not '
            'a subsidy for borrowing.',
        ]},

        {'type': 'pros_cons',
         'pros': [
             'No annual fee &mdash; cashback starts from zero fixed cost',
             '2% cashback for first 6 months (capped at &pound;2k earned)',
             '1% cashback thereafter, uncapped',
             'No foreign transaction fees &mdash; 0% on non-sterling spend',
             'No business current account required',
             'Straightforward cashback &mdash; no points conversion or redemption friction',
         ],
         'cons': [
             '34.9% representative APR &mdash; one of the higher rates in this market',
             'Cashback only works financially if you clear the balance monthly',
             '2% introductory rate capped at &pound;2,000 cashback earned',
             'Lower credit limits than Capital on Tap',
             'Sole trader eligibility not confirmed on public pages',
         ]},

        {'type': 'heading', 'level': 2, 'text': 'Alternatives to Funding Circle'},
        {'type': 'alternatives'},

        {'type': 'heading', 'level': 2, 'text': 'Funding Circle FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'Is the Funding Circle cashback card worth it?',
             'a': 'Only if you clear the balance every month. At &pound;3,000/month spend, you earn &pound;360/year in cashback with no annual fee. If you carry a balance at 34.9% APR, the interest erases the cashback within one or two months of carried debt.'},
            {'q': 'What happens after the 2% introductory cashback period?',
             'a': 'After six months, the cashback rate drops to 1% with no cap. The 2% introductory rate is capped at &pound;2,000 total cashback earned. Most businesses will not hit that cap during the introductory period.'},
            {'q': 'Can sole traders get the Funding Circle credit card?',
             'a': 'Funding Circle does not confirm sole trader eligibility on its public product pages. The card is available to limited companies with at least one year of trading history and &pound;30,000+ turnover. Check fundingcircle.com for current eligibility.'},
            {'q': 'How does Funding Circle&rsquo;s cashback compare to Capital on Tap?',
             'a': 'Funding Circle offers 2% for six months then 1% ongoing. Capital on Tap offers 1% from day one. Funding Circle has the stronger first-year return, but Capital on Tap offers higher credit limits and a lower floor APR (though the average rate is higher).'},
            {'q': 'Do I need a business bank account to get the Funding Circle card?',
             'a': 'No. The Funding Circle cashback card does not require a business current account with any specific provider.'},
            {'q': 'What is the credit limit on the Funding Circle card?',
             'a': 'Credit limits go up to &pound;250,000 depending on your business profile. Check current terms at fundingcircle.com, as your offered limit will depend on your company&rsquo;s trading history and financials.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Cashback figures:</strong> We calculated cashback at stated rates against '
            'illustrative monthly spend figures (&pound;1,500, &pound;3,000, and &pound;5,000 per month). '
            'The 2% introductory rate applies to the first six months and is capped at &pound;2,000 '
            'in total cashback earned. The ongoing 1% rate is uncapped. Actual cashback depends on '
            'eligible spend categories &mdash; verify current scope at fundingcircle.com.',

            '<strong>Interest cost calculations:</strong> We calculated monthly interest using '
            'the 34.9% representative APR divided by 12 to derive a monthly rate, applied to '
            'illustrative carried balances. The break-even table assumes the full monthly spend '
            'is carried for one month per quarter. These are simplified calculations for comparison '
            'purposes &mdash; actual interest depends on your statement cycle, payment timing, and '
            'any promotional terms.',

            '<strong>Competitor comparisons:</strong> Alternative card rates (Barclaycard 25.5%, '
            'Santander 23.7%, Capital on Tap from 13.86%) are representative APRs taken from each '
            'provider&rsquo;s public product pages as of March 2026. Capital on Tap&rsquo;s average '
            'rate of 46.05% is from their published Q4 2025 disclosure. We compared these rates '
            'on a like-for-like basis using the same carried-balance scenarios.',

            '<strong>Verification date:</strong> We verified card details, rates, cashback terms, '
            'and eligibility criteria against fundingcircle.com on 20 March 2026. Competitor terms '
            'verified against each provider&rsquo;s website on the same date.',

            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral fees '
            'from some providers listed. This does not affect our rate analysis or editorial '
            'assessment. Our cashback and interest calculations use the same methodology regardless '
            'of commercial relationships.',

            '<strong>Regulatory note:</strong> This page is editorial content, not regulated '
            'financial advice. Credit card terms, rates, and cashback structures can change. '
            'Always verify current terms directly with the provider before applying. '
            '<a href="/editorial-policy/">Read our full editorial policy</a>.',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
