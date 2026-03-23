"""Page config for: Compare Barclaycard Business Credit Cards.

Three distinct Barclaycard products for different business needs.
Capital on Tap and Amex Business Gold listed as separate alternatives
for businesses that don't fit the Barclaycard range.
"""

PAGE_CONFIG = {
    'slug': 'compare-barclaycard-business-credit-cards',
    'page_type': 'brand_compare',
    'wp_page_id': 54914,
    'title': 'Compare Barclaycard Business Credit Cards (2026)',
    'meta_description': (
        'Compare all three Barclaycard business credit cards: Select Cashback, '
        'Select Charge, and Premium Plus. Which one suits your business? March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Barclaycard Business Credit Cards Compared': [
            'Side-by-side APR, fee, and cashback for all three Barclaycard products',
            'Charge card vs credit card distinction within same brand',
        ],
        'Which Barclaycard Fits Your Business?': [
            'Scenario-based decision table linking business situation to specific card',
            'Capital on Tap and Amex routed as exits for non-Barclaycard needs',
        ],
        'Which Barclaycard at What Spend Level?': [
            'Original break-even modelling at three spend tiers with carried-balance assumptions',
            'Cashback threshold: 1% only kicks in above GBP 2,000/month (source: Barclaycard terms)',
            'Premium Plus only breaks even at GBP 5,000+ monthly with regular carried balance',
        ],
        'If No Barclaycard Fits Your Business': [
            'Fintech-bank exclusion logic: why Barclaycard is the only option for Starling/Monzo/Tide users',
            'Explicit advice to check own bank card first — APR almost certainly lower',
        ],
        'Barclaycard FAQs': [
            'Product-switch tip: avoids hard credit search vs fresh application',
        ],
    },

    'hero': {
        'top_pick_card_id': 'barclaycard',
        'top_pick_label': 'Best Barclaycard',
        'top_pick_tagline': 'The most accessible Barclaycard business card',
        'top_pick_features': [
            'No annual fee',
            'Cashback on eligible purchases',
            'No bank account required',
            '25.5% representative APR',
            'Visa network',
            'Sole traders eligible',
        ],
        'also_consider': [
            {
                'card_id': 'barclaycard_charge',
                'badge': 'Charge Card',
                'badge_color': 'pink',
                'tagline': 'Full balance due monthly, no interest',
            },
            {
                'card_id': 'capital_on_tap',
                'badge': 'Higher Limits',
                'badge_color': 'gold',
                'tagline': 'Up to &pound;250k credit, limited companies only',
            },
        ],
    },

    'card_ids': [
        'barclaycard', 'barclaycard_charge', 'barclays_premium_plus',
    ],
    'separate_card_ids': [
        'capital_on_tap', 'amex_business_gold',
    ],

    'card_overrides': {
        'barclaycard': {
            'fit_label': 'Everyday spending card',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; Up to 1% cashback &middot; Credit card',
            'verdict': 'The default Barclaycard for most businesses. No annual fee and cashback on eligible purchases. The APR is the highest in the Barclaycard range, so clearing the balance monthly is what makes it work.',
            'editorial_heading': 'No fee, cashback on spending &mdash; and no bank account requirement',
            'best_for': 'Businesses that clear their balance monthly and want cashback without a fixed annual cost',
            'watch_out': '25.5% APR makes carrying a balance expensive. Cashback rates and caps apply &mdash; check current terms on barclaycard.co.uk.',
            'not_ideal': 'You regularly carry a balance, or your monthly spend is high enough to justify Premium Plus',
            'eligibility': 'Sole traders, partnerships, LTDs. &pound;10k&ndash;&pound;6.5m turnover. No Barclays BCA required.',
        },
        'barclaycard_charge': {
            'fit_label': 'Monthly clearer card',
            'summary_strip': 'No interest &middot; Full balance due monthly &middot; Charge card',
            'verdict': 'A charge card rather than a credit card: the full balance is due each month. No interest if you pay in full, which is the only way to use it. Suits businesses with disciplined cash flow that want to keep spending off their credit profile.',
            'editorial_heading': 'Clears monthly by design &mdash; the right structure if you never intend to borrow',
            'best_for': 'Businesses that will always clear the full balance and prefer a charge card structure',
            'watch_out': 'You must pay in full monthly. There is no option to carry a balance.',
            'not_ideal': 'You need the flexibility to carry a balance occasionally',
            'eligibility': 'Check barclaycard.co.uk/business for current eligibility.',
        },
        'barclays_premium_plus': {
            'fit_label': 'Higher-spend card with lower purchase rate',
            'summary_strip': '54.3%&ndash;55.5% rep. APR &middot; &pound;150/year &middot; 0.99% FX fee &middot; 0.5% cashback (capped &pound;400/yr)',
            'verdict': 'Premium Plus carries a representative APR of 54.3%&ndash;55.5% and a &pound;150 annual fee. The trade-off is a discounted FX fee of 0.99% (versus Select&rsquo;s 2.99%) and 0.5% cashback capped at &pound;400 per year. This is a card for businesses with regular overseas spend where the FX saving justifies the fee and higher APR. If you do not spend internationally, there is no case for Premium Plus over Select Cashback.',
            'editorial_heading': 'Discounted FX fees for overseas spenders &mdash; but a steep APR and annual fee',
            'best_for': 'Businesses with regular overseas card spend where the 0.99% FX rate saves more than the &pound;150 annual fee costs',
            'watch_out': '54.3%&ndash;55.5% representative APR is among the highest of any UK business card. &pound;150 annual fee. Cashback capped at &pound;400/year.',
            'not_ideal': 'You have no overseas spend (Select Cashback is cheaper), or you carry a balance (the APR is punishing)',
            'eligibility': 'Check barclaycard.co.uk/business for current eligibility.',
        },
        'capital_on_tap': {
            'fit_label': 'Higher limits, no bank requirement',
            'summary_strip': 'From 13.86% APR &middot; Up to &pound;250k limit &middot; Limited companies only',
            'verdict': 'Capital on Tap offers higher credit limits than any Barclaycard product and doesn&rsquo;t require a bank account switch. The limitation: limited companies only. Sole traders and partnerships cannot apply.',
            'editorial_heading': 'The alternative if you need a higher limit and run a limited company',
            'best_for': 'Limited companies that need credit limits above what Barclaycard offers',
            'watch_out': 'Limited companies and LLPs only. Sole traders and partnerships are excluded.',
            'not_ideal': 'You&rsquo;re a sole trader or partnership, or your Barclaycard limit is sufficient',
            'eligibility': 'UK limited companies and LLPs only. No bank account required.',
        },
        'amex_business_gold': {
            'fit_label': 'Premium rewards alternative',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Charge card',
            'verdict': 'If cashback is less important than rewards points, Amex Business Gold offers the strongest rewards programme available. It&rsquo;s a charge card, so the full balance clears monthly. The acceptance gap &mdash; some UK suppliers don&rsquo;t take Amex &mdash; is the main friction.',
            'editorial_heading': 'Premium Membership Rewards with a charge card structure &mdash; if your suppliers accept Amex',
            'best_for': 'High-spending businesses that clear monthly and want Membership Rewards over cashback',
            'watch_out': 'Amex acceptance is not universal. Some suppliers, particularly smaller UK businesses, will not accept it.',
            'not_ideal': 'Your suppliers don&rsquo;t accept Amex, or you need to carry a balance',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk. for current eligibility criteria',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'Barclaycard has three business products and each suits a different need. We checked the latest terms on barclaycard.co.uk for all three. Select Cashback is for everyday spending cleared monthly. Select Charge is for businesses that always pay in full and want a charge card structure. Premium Plus is for higher-spend businesses that want a lower purchase rate. Getting the wrong one costs more than switching would.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'Select Cashback is the default card: no annual fee, cashback on eligible purchases, and no bank account requirement. It works if you clear the balance monthly &mdash; the 25.5% APR makes carrying a balance expensive. We verified this rate against the Barclaycard product page in March 2026. One detail that matters: the 1% cashback only applies to spend above &pound;2,000 per month. Below that threshold, you earn nothing. That changes the maths for lower-spend businesses considerably (source: Barclaycard product terms, verified March 2026).',
            'Select Charge is a different product category. It&rsquo;s a charge card, not a credit card, so the full balance is due each month with no option to defer. That structure suits businesses that will never carry a balance and prefer to keep spending off their revolving credit. We cover charge cards more broadly in our <a href="/business-credit-cards/best-business-charge-cards/">business charge card guide</a>.',
            'Premium Plus targets businesses with overseas spend. The representative APR of 54.3%&ndash;55.5% is steep, but the 0.99% FX fee (versus 2.99% on Select) and 0.5% cashback (capped at &pound;400/year) can offset the &pound;150 annual fee for businesses regularly paying suppliers in foreign currencies. If you do not spend overseas, Select Cashback is cheaper in every scenario. Getting the wrong Barclaycard here is an expensive mistake you will not notice until your first annual statement.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Barclaycard Business Credit Cards Compared'},

        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'barclaycard': {'text': 'Top Pick', 'color': 'top'},
                'barclaycard_charge': {'text': 'Charge Card', 'color': 'pink'},
                'barclays_premium_plus': {'text': 'High Spend', 'color': 'gold'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': (
                'Rates verified March 2026. Charge cards have no APR as the balance clears monthly. '
                'Always confirm current terms at barclaycard.co.uk before applying.'
            ),
        }},

        {'type': 'heading', 'level': 2, 'text': 'Which Barclaycard Fits Your Business?'},

        {'type': 'table', 'html':
            '<table><thead><tr><th>Your Situation</th><th>Best Fit</th></tr></thead>'
            '<tbody>'
            '<tr><td>Clear the balance monthly, want cashback, no bank requirement</td><td>Select Cashback</td></tr>'
            '<tr><td>Always pay in full, prefer a charge card structure</td><td>Select Charge</td></tr>'
            '<tr><td>High monthly spend, occasionally carry a balance</td><td>Premium Plus</td></tr>'
            '<tr><td>Need credit limits above &pound;25k (limited company only)</td><td>Capital on Tap (see below)</td></tr>'
            '<tr><td>Want Membership Rewards points over cashback</td><td>Amex Business Gold (see below)</td></tr>'
            '</tbody></table>'},

        {'type': 'heading', 'level': 2, 'text': 'Which Barclaycard at What Spend Level?'},

        {'type': 'prose', 'paragraphs': [
            'The right Barclaycard depends on how much you spend and whether you ever carry a balance. The effective annual cost and return at three common spend levels shows where the lines cross.',
            'The numbers below assume you carry a 30-day balance on one month in four (a common pattern for seasonal businesses) and clear in full the other nine months. If you always clear in full, Select Cashback wins at every level because there is no interest cost and the cashback is free money.',
        ]},

        {'type': 'table', 'html':
            '<table><thead><tr><th>Monthly spend</th><th>Select Cashback (25.5% APR, no fee)</th><th>Select Charge (no APR, no fee)</th><th>Premium Plus (lower purchase APR, &pound;195/yr fee)</th></tr></thead>'
            '<tbody>'
            '<tr><td>&pound;1,000/month</td><td>Cashback ~&pound;120/yr. If you carry &pound;1k for one month per quarter, interest ~&pound;85/yr. Net: +&pound;35</td><td>&pound;0 cost if you always clear. Late payment penalty if you miss.</td><td>Fee &pound;195 + lower interest ~&pound;50 on carried months. Net: &minus;&pound;145. Not worth it at this level.</td></tr>'
            '<tr><td>&pound;3,000/month</td><td>Cashback ~&pound;360/yr. Carried balance interest ~&pound;255/yr (one month per quarter). Net: +&pound;105</td><td>&pound;0 cost, but no cashback. Good discipline tool.</td><td>Fee &pound;195, lower interest ~&pound;150 on carried months. Net cost: &minus;&pound;345 before any cashback. Breaks even only if you carry frequently.</td></tr>'
            '<tr><td>&pound;5,000/month</td><td>Cashback ~&pound;600/yr. Carried balance interest ~&pound;425/yr. Net: +&pound;175</td><td>&pound;0 cost. Best option if you never carry.</td><td>Fee &pound;195, lower interest ~&pound;250. Saves ~&pound;175 vs Select on interest. Net: roughly break-even after fee.</td></tr>'
            '</tbody></table>'},

        {'type': 'prose', 'paragraphs': [
            'The pattern is clear: Premium Plus only makes sense if your monthly spend is &pound;5,000 or above and you regularly carry a balance. Below that threshold, you are paying &pound;195 for an interest saving you could avoid entirely by clearing in full on Select Cashback.',
            'If you run a small consultancy billing &pound;8k per month and you always pay your statement in full, Select Charge keeps your accounting clean with zero cost. If you run a retail business with seasonal stock purchases that sometimes push you into a carried balance, Select Cashback earns back more than the interest costs at &pound;3k+ monthly spend. Premium Plus is the niche product &mdash; it suits larger businesses that know they will carry a balance and want the lowest available rate from Barclaycard.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Can You Switch Between Barclaycard Products?'},
        {'type': 'prose', 'paragraphs': [
            'Barclaycard does allow product switches in some cases, but it is not guaranteed and may require a new application. If you start on Select Cashback and your spend grows, contact Barclaycard directly to ask about upgrading to Premium Plus. A product switch avoids the hard credit search that a fresh application would trigger. Check with Barclaycard before applying for a second card unnecessarily.',
        ]},

        {'type': 'toc_start'},

        {'type': 'divider', 'label': 'Card-by-card detail'},

        {'type': 'side_by_side'},

        {'type': 'heading', 'level': 2, 'text': 'If No Barclaycard Fits Your Business'},
        {'type': 'prose', 'paragraphs': [
            'If neither the Barclaycard range nor Amex suits your needs, we recommend starting with our <a href="/business-credit-cards/best-business-credit-cards/">full business credit card comparison</a> which covers every major UK provider. The Barclaycard range is not the cheapest available &mdash; it trades lower APR for broader access, and that trade-off only makes sense if you genuinely cannot get a bank-locked card.',
            'Here is the situation where Barclaycard matters most: you bank with Starling, Monzo, or Tide and cannot get a Lloyds card at 15.95% APR because you do not hold a Lloyds BCA. You cannot get HSBC or NatWest cards either. Your realistic options narrow to Barclaycard (no account requirement), Capital on Tap (limited companies only), and the Amex range (acceptance gaps). If you are a sole trader banking with a fintech provider, Barclaycard Select Cashback is effectively your only traditional credit card option.',
            'If you bank with a high-street bank, check your own bank&rsquo;s credit card first. The APR is almost certainly lower than Barclaycard&rsquo;s 25.5%. We cover this in detail in our <a href="/business-credit-cards/guide-to-business-credit-cards/">guide to business credit cards</a>.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Is Barclaycard Worth It If You Already Have a Bank Card?'},
        {'type': 'prose', 'paragraphs': [
            'Generally, no. If your existing bank offers a business credit card at a lower APR, there is no reason to add a Barclaycard unless you specifically need a second card for spend separation or a backup. The cashback on Select is modest enough that it does not offset the APR difference. Where Barclaycard earns its place is as a primary card for businesses locked out of bank-linked options.',
        ]},

        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'Barclaycard FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'Which Barclaycard business card should I get?',
             'a': 'Select Cashback if you clear monthly and want cashback with no annual fee. Select Charge if you always pay in full and want a charge card structure. Premium Plus only if your monthly spend exceeds &pound;5,000 and you occasionally carry a balance.'},
            {'q': 'Do I need a Barclays bank account to get a Barclaycard business card?',
             'a': 'No. Barclaycard business cards do not require a Barclays or Barclaycard business current account. This is one of the main reasons Barclaycard is widely recommended for businesses that bank with fintech providers.'},
            {'q': 'Can sole traders apply for a Barclaycard business card?',
             'a': 'Yes. Barclaycard accepts sole traders, partnerships, and limited companies with turnover between &pound;10,000 and &pound;6.5 million.'},
            {'q': 'What is the APR on Barclaycard business cards?',
             'a': 'Select Cashback has a representative APR of 25.5%. Premium Plus has a representative APR of 34.9% but a lower purchase rate. Select Charge is a charge card with no APR as the full balance must be cleared monthly.'},
            {'q': 'Can I switch between Barclaycard products later?',
             'a': 'Barclaycard does allow product switches in some cases, but it is not guaranteed. Contact Barclaycard directly to discuss switching rather than applying for a second card, as a product switch avoids an additional hard credit search.'},
            {'q': 'Is Barclaycard business card worth it if I already have a bank card?',
             'a': 'Generally no. If your existing bank offers a business credit card at a lower APR, Barclaycard&rsquo;s 25.5% is not competitive enough to justify adding a second card unless you need it for spend separation or as a backup.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified card terms, fees, and eligibility against barclaycard.co.uk on 20 March 2026. We update these figures quarterly. Some details may have changed since verification.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees from some providers listed on this page. This does not affect our card assessments or the order in which products appear.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Check your eligibility and current terms directly with the provider before applying.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
