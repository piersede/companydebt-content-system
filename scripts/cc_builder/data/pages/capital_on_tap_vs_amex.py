"""Page config for: Capital on Tap vs Amex Business Gold.

Head-to-head comparison. These are fundamentally different products:
Capital on Tap is a credit card with high limits and Visa acceptance.
Amex Business Gold is a charge card with a premium rewards programme.
The decision turns on card type, supplier acceptance, and business structure
(CoT is limited companies only).
"""

PAGE_CONFIG = {
    'slug': 'capital-on-tap-vs-amex',
    'page_type': 'brand_compare',
    'wp_page_id': 45107,
    'title': 'Capital on Tap vs Amex Business Gold (2026)',
    'meta_description': (
        'Capital on Tap vs Amex Business Gold compared: credit limits, rewards, '
        'acceptance, card type, and eligibility. Which is right for your business? March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'The Key Differences': [
            'Head-to-head comparison table: card type, network, limits, eligibility',
            'Headline rate caveat: CoT 13.86% is a floor most won\'t reach; Amex GBP 0 hides GBP 195 yr-2 fee',
        ],
        'When Capital on Tap Wins': [
            'Carrying GBP 4k at 46% APR wipes four months of 1% cashback in one cycle',
            'No-redemption-step cashback vs MR points admin overhead',
            'Up to GBP 250k limit verified against capitalontap.com March 2026',
        ],
        'When Amex Business Gold Wins': [
            'MR transfer rates: Avios 1:1, Virgin 1:1, Hilton 1:2, Marriott 2:3',
            'Point value range: 0.5p (Nectar) to 1.5p (long-haul premium cabin)',
            'Sole traders cannot get CoT — comparison self-resolves for them',
        ],
        'Amex vs Capital on Tap: The Acceptance Test': [
            'Amex UK acceptance up 46% over three years (source: Amex network data)',
            '311,438 UK businesses joined Amex network 2021-2022',
            'Worked example: marketing agency vs construction firm acceptance split',
        ],
        'Other Cards to Consider': [
            'Barclaycard and Funding Circle positioned as fallbacks with trade-offs stated',
        ],
        'Capital on Tap vs Amex FAQs': [
            'Dual-card strategy only justified above GBP 3k/month Amex-eligible spend',
        ],
    },

    'hero': {
        'top_pick_card_id': 'capital_on_tap',
        'top_pick_label': 'For Most Businesses',
        'top_pick_tagline': 'Visa acceptance, high limits, no annual fee',
        'top_pick_features': [
            'Visa acceptance everywhere',
            '1% cashback on all spend',
            'No annual fee',
            'High credit limits up to &pound;250k',
            'No foreign transaction fees',
        ],
        'also_consider': [
            {
                'card_id': 'amex_business_gold',
                'badge': 'Best Rewards',
                'badge_color': 'gold',
                'tagline': 'Membership Rewards programme with flexible redemption',
            },
            {
                'card_id': 'barclaycard',
                'badge': 'Alternative',
                'badge_color': 'teal',
                'tagline': 'Open access Visa card if neither suits',
            },
        ],
    },

    'card_ids': [
        'capital_on_tap', 'amex_business_gold',
    ],
    'separate_card_ids': [
        'amex_business_basic', 'ba_amex_accelerating', 'barclaycard', 'funding_circle_cashback',
    ],

    'card_overrides': {
        'capital_on_tap': {
            'fit_label': 'High limits, Visa acceptance',
            'summary_strip': 'From 13.86% APR &middot; Up to &pound;250k credit limit &middot; Visa &middot; 1% cashback &middot; Limited companies only',
            'verdict': 'Capital on Tap offers the highest credit limits available to UK SMEs without a bank account requirement, on a Visa network that all suppliers accept. The constraint is structural: limited companies only. If you&rsquo;re a sole trader or partnership, you cannot apply.',
            'editorial_heading': 'High limits and universal acceptance &mdash; but only available to limited companies',
            'best_for': 'Limited companies that need a high credit limit and universal supplier acceptance',
            'watch_out': 'Limited companies and LLPs only &mdash; sole traders and partnerships are excluded. APR varies significantly by business profile.',
            'not_ideal': 'You&rsquo;re a sole trader or partnership, or you prioritise rewards points over cashback and credit limits',
            'eligibility': 'UK limited companies and LLPs only. No bank account required.',
        },
        'amex_business_gold': {
            'fit_label': 'Premium rewards, charge card structure',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Charge card &middot; Sole traders accepted',
            'verdict': 'Amex Business Gold earns Membership Rewards &mdash; one of the most flexible business rewards currencies available in the UK. It&rsquo;s a charge card, so the full balance clears monthly. The acceptance gap and the charge card structure are the two reasons it doesn&rsquo;t work for everyone.',
            'editorial_heading': 'The best rewards programme available &mdash; if your suppliers accept Amex and you always clear monthly',
            'best_for': 'High-spending businesses that clear monthly and want Membership Rewards over cashback',
            'watch_out': 'Charge card structure: full balance due monthly, no option to carry. Amex acceptance is not universal &mdash; verify your key suppliers first.',
            'not_ideal': 'You need to carry a balance occasionally, your suppliers don&rsquo;t accept Amex, or you&rsquo;re a limited company wanting the highest possible credit limit',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'amex_business_basic': {
            'fit_label': 'Lower-fee Amex with flexible payment',
            'summary_strip': '&pound;0 annual fee &middot; No Membership Rewards &middot; Charge card',
            'verdict': 'A lower-commitment entry point into Amex Membership Rewards. Earns at a lower rate than Gold but with a lower fee and a flexible payment option for those who can&rsquo;t commit to full monthly clearance.',
            'editorial_heading': 'Amex rewards without the charge card commitment or Gold-level fee',
            'best_for': 'Businesses new to Amex, or those that want Membership Rewards with occasional payment flexibility',
            'watch_out': 'No rewards programme &mdash; this is a no-fee charge card for businesses that just want Amex acceptance. Check current terms at americanexpress.com/uk.',
            'not_ideal': 'You want the highest Membership Rewards earn rate and will always clear monthly',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'ba_amex_accelerating': {
            'fit_label': 'Direct Avios for BA flyers',
            'summary_strip': '&pound;250/year &middot; 1.5 Avios per &pound;1 &middot; Credit card &middot; Sole traders accepted',
            'verdict': 'If you fly British Airways regularly, this earns Avios directly on card spend without a transfer step. A credit card rather than a charge card, so you can carry a balance. Only relevant if BA is your airline.',
            'editorial_heading': 'The right choice if BA travel is a genuine business cost',
            'best_for': 'Businesses that fly BA regularly and want to earn Avios on all card spend',
            'watch_out': 'No value if you don&rsquo;t fly BA. Amex acceptance gap applies.',
            'not_ideal': 'You don&rsquo;t fly BA, or Amex acceptance is a problem for your suppliers',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'barclaycard': {
            'fit_label': 'Broad access, cashback, no bank requirement',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; Up to 1% cashback &middot; Sole traders accepted &middot; Visa',
            'verdict': 'Barclaycard Select Cashback accepts sole traders, requires no bank account, and runs on Visa. It&rsquo;s the accessible fallback for businesses that can&rsquo;t get Capital on Tap (sole traders) or don&rsquo;t want the Amex acceptance overhead. The APR is the highest trade-off.',
            'editorial_heading': 'The open-access option &mdash; accepts sole traders, no bank switch, Visa',
            'best_for': 'Sole traders or businesses that need Visa acceptance and don&rsquo;t qualify for Capital on Tap',
            'watch_out': '25.5% APR. Less competitive on rewards than Amex or Capital on Tap&rsquo;s cashback at lower APR.',
            'not_ideal': 'You run a limited company and qualify for Capital on Tap, or Amex acceptance is not a problem',
            'eligibility': 'Sole traders, partnerships, LTDs. &pound;10k&ndash;&pound;6.5m turnover. No Barclays BCA required.',
        },
        'funding_circle_cashback': {
            'fit_label': 'Fintech cashback alternative',
            'summary_strip': '34.9% rep. APR &middot; 2% then 1% cashback &middot; No bank account required',
            'verdict': 'A fintech cashback card without a bank account requirement. Limited companies only, minimum 1 year trading, &pound;30k turnover.',
            'editorial_heading': 'Cashback without a bank switch &mdash; limited companies only',
            'best_for': 'Limited companies wanting cashback outside the main card issuers',
            'watch_out': '34.9% representative APR. Limited companies only &mdash; sole traders excluded. Check fundingcircle.com.',
            'not_ideal': 'You&rsquo;re a sole trader (excluded) or you carry a balance regularly (high APR)',
            'eligibility': 'UK limited companies only. Min 1 year trading, &pound;30k+ turnover.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'Capital on Tap and Amex Business Gold are often compared but they solve different problems. Capital on Tap is a Visa credit card with high limits and cashback &mdash; built for limited companies that need spending power and universal acceptance. Amex Business Gold is a charge card with premium Membership Rewards &mdash; built for businesses that always clear monthly and want the best rewards programme in the market. The right choice depends on your card type preference, your suppliers, and your legal structure.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'The card type difference is the first thing to get clear. Capital on Tap is a credit card: you have a credit limit and can carry a balance, paying interest if you don&rsquo;t clear in full. Amex Business Gold is a charge card: the full balance is due each month and there is no option to defer. We explain this distinction in detail in our <a href="/business-credit-cards/business-credit-cards-vs-charge-cards/">credit cards vs charge cards guide</a>.',
            'That structural difference affects who each card suits. If your cash flow has any variability month to month, the charge card structure is a real constraint. If you always clear in full, the rewards debate opens up &mdash; and Amex Membership Rewards is the stronger programme after comparing the redemption options across both cards.',
            'There is also an eligibility asymmetry. Capital on Tap accepts UK limited companies and LLPs only. Amex Business Gold accepts a broader range including sole traders. If you&rsquo;re not a limited company, this comparison resolves itself quickly.',
            'The headline rates are misleading in opposite directions. Capital on Tap&rsquo;s &ldquo;from 13.86%&rdquo; is a floor most applicants won&rsquo;t reach. Amex Gold&rsquo;s &ldquo;&pound;0 first year&rdquo; hides a &pound;195 annual fee that kicks in whether you&rsquo;re ready or not. Neither card is as cheap as it first looks.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'The Key Differences'},

        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'capital_on_tap': {'text': 'Visa', 'color': 'top'},
                'amex_business_gold': {'text': 'Best Rewards', 'color': 'gold'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': (
                'Rates and fees verified March 2026 where available from public sources. '
                'Confirm current terms at capitalontap.com and americanexpress.com/uk before applying.'
            ),
        }},

                {'type': 'heading', 'level': 2, 'text': 'When Capital on Tap Wins'},

        {'type': 'toc_start'},

        {'type': 'prose', 'paragraphs': [
            'Capital on Tap is the stronger choice when credit limit is the primary requirement. It offers up to &pound;250k &mdash; significantly higher than most business credit cards &mdash; and no bank account switch is needed to get it. We verified these limits against capitalontap.com in March 2026.',
            'We confirmed that Visa acceptance removes the supplier question entirely. If any of your key suppliers do not accept Amex, Capital on Tap sidesteps the problem. You will never have a payment declined because a supplier does not support your network.',
            'For limited companies that want a simple cashback return rather than a points programme to manage, Capital on Tap is also less administratively demanding. The 1% cashback applies without redemption steps &mdash; no transferring points, no booking through a portal, no worrying about devaluations. You spend, you get 1% back. At &pound;4,000/month that is &pound;480/year in your account without any effort.',
            'But that 1% disappears fast if you carry a balance at the average offered rate of 46%. One month of carrying &pound;4,000 at 46% APR costs roughly &pound;153 in interest &mdash; wiping out four months of cashback in a single billing cycle. If you plan to carry a balance, confirm your individual rate before you apply. For a deeper look at the rate and fee structure, see our <a href="/business-credit-cards/capital-on-tap-review/">full Capital on Tap review</a>.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'When Amex Business Gold Wins'},

        {'type': 'prose', 'paragraphs': [
            'Amex Membership Rewards is one of the most valuable business rewards currencies available to UK businesses. Points transfer to Avios at 1:1, Virgin Atlantic at 1:1, Hilton Honors at 1:2, and Marriott Bonvoy at 2:3. The practical value per point ranges from 0.75p to 1.5p when redeemed for airline miles, with long-haul premium cabin redemptions pushing toward the upper end. For hotel transfers, expect around 0.75p per point for Marriott and 0.66p for Hilton. The floor is roughly 0.5p per point if you redeem via Nectar or retail options &mdash; avoid that route unless you have no travel use.',
            'If you have significant monthly card spend, always clear the balance, and your key suppliers accept Amex, Business Gold earns more than Capital on Tap&rsquo;s cashback when you factor in the points value at redemption. We compared the effective earn rates across both cards and the Gold consistently wins above &pound;3k monthly spend when redeemed well. At &pound;5,000/month, Gold earns roughly 60,000 Membership Rewards points per year. Transfer those to Avios and you have enough for a return short-haul flight every quarter. Capital on Tap at the same spend gives you &pound;600 cash. Which matters more depends on whether you travel.',
            'One option that blurs the charge card line: both the Gold and Platinum now offer Pay Over Time at 29.1% variable APR on eligible purchases. It is not a standard credit facility &mdash; it applies only up to the card&rsquo;s Flexible Payment Option limit &mdash; but it gives you the option to defer payment on specific transactions if cash flow is tight in a given month. At 29.1%, it is not cheap. Capital on Tap&rsquo;s revolving credit is structurally more flexible, though its average offered rate of 46% is worse.',
            'Sole traders are also eligible for Amex Business Gold, which is not the case with Capital on Tap. If you are a freelance consultant or sole trader, this comparison resolves itself: you cannot get Capital on Tap. Your choice is between Amex Gold and a Visa card like Barclaycard. We cover the full Amex range in our <a href="/business-credit-cards/compare-american-express-business-credit-cards/">Amex business card comparison</a>.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Amex vs Capital on Tap: The Acceptance Test'},

        {'type': 'prose', 'paragraphs': [
            'Amex UK acceptance has improved materially: acceptance locations increased by 46% over the past three years, and 311,438 UK businesses joined the Amex network in 2021&ndash;2022. In the US, Amex is at near-parity with Visa and Mastercard. In the UK, the gap is smaller than it was but still real &mdash; and notably wider in France and Germany if your business has European suppliers.',
            'If you are considering Amex Business Gold, we recommend running a supplier acceptance audit before you apply. This takes fifteen minutes and can save you from committing to a card you cannot fully use.',
            'Pull your last three months of business spending. List your top ten suppliers by total spend. For each one, check whether they accept American Express. You can usually find this on their payment page, or phone and ask. If seven or more accept Amex, Gold is a viable primary card. If fewer than five accept, you will need a Visa or Mastercard for the majority of your spend, and the Gold card becomes a secondary card at best &mdash; harder to justify with a &pound;195 annual fee.',
            'Here is a common scenario: a marketing agency spending &pound;8,000/month. Google Ads, Meta Ads, Adobe Creative Cloud, and Slack all accept Amex &mdash; that accounts for &pound;5,000. The remaining &pound;3,000 goes to freelance designers and contractors who invoice via bank transfer (not card-payable at all). In this case, &pound;5,000 of &pound;8,000 is Amex-eligible card spend, and Gold earns well on that. But if you are a construction firm and &pound;6,000 of your &pound;8,000 goes to trade suppliers on Visa-only terminals, Gold earns on &pound;2,000 and the maths collapse.',
            'Capital on Tap sidesteps this entirely. Visa is accepted everywhere. You never need to check supplier acceptance, and you never need a second card. That operational simplicity has real value, even if the rewards are less exciting than Membership Rewards.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Can You Use Both Cards Together?'},
        {'type': 'prose', 'paragraphs': [
            'Yes, and some businesses do. You can use Amex Gold for Amex-accepting suppliers to earn Membership Rewards, and Capital on Tap for everything else. The cost is managing two statements, two payment dates, and a &pound;195 annual fee on the Amex. This dual-card strategy only makes sense if your Amex-eligible spend exceeds &pound;3,000/month &mdash; below that, the fee eats into the rewards advantage and you are better off consolidating everything on Capital on Tap.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'What If Your Amex Acceptance Changes?'},
        {'type': 'prose', 'paragraphs': [
            'Supplier acceptance can shift. A key supplier switching payment processors might add or drop Amex overnight. We recommend re-checking your acceptance picture annually, especially if you change suppliers or your business model shifts. If your Amex-eligible spend drops below the break-even threshold, cancel the Gold before the next fee cycle and move everything to a Visa card.',
        ]},

        {'type': 'divider', 'label': 'Card-by-card detail'},

        {'type': 'side_by_side'},

        {'type': 'bottom_line',
         'text': 'If you run a limited company, always clear your balance monthly, and most of your suppliers accept Amex: Business Gold earns more at scale. If you need a higher credit limit, want Visa acceptance across all suppliers, or can&rsquo;t always clear in full: Capital on Tap is the more practical card. Sole traders don&rsquo;t have a choice between these two &mdash; Capital on Tap is closed to them.'},

        {'type': 'heading', 'level': 2, 'text': 'Other Cards to Consider'},

        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'Capital on Tap vs Amex FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'Should I get Capital on Tap or Amex Business Gold?',
             'a': 'Capital on Tap if you need high credit limits, Visa acceptance everywhere, and run a limited company. Amex Business Gold if you always clear monthly, want Membership Rewards, and your key suppliers accept Amex. If you are a sole trader, you cannot get Capital on Tap.'},
            {'q': 'Can I use both Capital on Tap and Amex Business Gold?',
             'a': 'Yes. Some businesses use Amex Gold for Amex-accepting suppliers to earn Membership Rewards and Capital on Tap for everything else. This only makes sense if your Amex-eligible spend exceeds &pound;3,000/month to justify the &pound;195 annual fee.'},
            {'q': 'Do all UK suppliers accept Amex?',
             'a': 'No. Amex acceptance in the UK is not universal. Smaller suppliers, some trade merchants, and certain government bodies do not accept it. Check your top suppliers before committing to an Amex card as your primary business card.'},
            {'q': 'Is Capital on Tap a credit card or a charge card?',
             'a': 'Capital on Tap is a revolving credit card on the Visa network. You can carry a balance and pay interest. Amex Business Gold is a charge card that requires the full balance to be cleared every month.'},
            {'q': 'Which card has better rewards?',
             'a': 'Amex Membership Rewards is the more valuable programme at higher spend levels, especially if you redeem for travel. Capital on Tap offers a simpler 1% cashback with no redemption steps. Which matters more depends on whether you travel and how much you spend.'},
            {'q': 'Can a sole trader get either of these cards?',
             'a': 'Sole traders can apply for Amex Business Gold but cannot apply for Capital on Tap, which is restricted to UK limited companies and LLPs.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified card terms, fees, and eligibility against capitalontap.com and americanexpress.com/uk on 20 March 2026. All figures verified from public product pages. We update these figures quarterly.',
            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral fees from some providers listed on this page. This does not affect our comparisons or assessments.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Check your eligibility and current terms directly with each provider before applying.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
