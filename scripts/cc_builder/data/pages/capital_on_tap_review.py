"""Page config for: Capital on Tap Business Credit Card Review.

Single-product review page covering Capital on Tap&rsquo;s credit card.
Key tension: floor rate of 13.86% vs the actual average rate of 46.05%
(Oct&ndash;Dec 2025). The card suits limited companies with high spend
requirements but the rate reality needs upfront disclosure.
"""

PAGE_CONFIG = {
    'slug': 'capital-on-tap-review',
    'page_type': 'review',
    'wp_page_id': 43977,
    'title': 'Capital on Tap Business Credit Card Review (2026)',
    'meta_description': (
        'Capital on Tap review: limits up to \u00a3250k, no bank account needed, '
        'but the average rate is 46.05% not the 13.86% floor. Who it suits.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'What Capital on Tap Actually Is': [
            'Clarifies fintech-not-bank status and Visa issuance',
            'Sole trader exclusion stated upfront with redirect',
            'Limit ceiling vs bank card caps quantified',
        ],
        'The Capital on Tap Rate Problem': [
            'S&P securitisation data: BBR+9.9% to BBR+49.9% range',
            'Q4 2025 average rate 46.05% sourced from CoT disclosure',
            'Pound-cost gap: 13.86% vs 46.05% on £10k over 1 month',
            'Portfolio yield ~35% from London Cards No.1/No.2 reports',
        ],
        'Rate Transparency: What You\u2019ll Actually Pay': [
            'Average rate buried in legal footer, not product page',
            'Soft-search-then-compare workflow before accepting offer',
            'FCA 51% rep APR rule explained in plain language',
        ],
        'Who Should and Shouldn\u2019t Apply for Capital on Tap': [
            'Worked scenario: digital agency on Starling, £12k/month',
            'Worked scenario: e-commerce with seasonal carried balance',
            'Sector data: 84% micro clear monthly, construction 35%',
            'Section 75 gap for business cards explained with chargeback alternative',
        ],
        'Alternatives to Capital on Tap': [
            'Alternatives contextualised against rate-uncertainty problem',
        ],
        'Capital on Tap FAQs': [
            'FAQ answers include verified Q4 2025 rate data throughout',
        ],
    },

    'hero': {
        'top_pick_card_id': 'capital_on_tap',
        'top_pick_label': 'Under Review',
        'top_pick_tagline': 'High limits, no bank switch, 1% cashback',
        'top_pick_features': [
            'Credit limits up to &pound;250k',
            '1% cashback on all spend',
            'No annual fee (free tier)',
            'No foreign transaction fees',
            'Instant virtual card on approval',
            'Limited companies only',
        ],
        'also_consider': [
            {
                'card_id': 'barclaycard',
                'badge': 'Open Access',
                'badge_color': 'teal',
                'tagline': 'No bank account required, sole traders accepted',
            },
            {
                'card_id': 'moss',
                'badge': 'Similar Fintech',
                'badge_color': 'pink',
                'tagline': 'Spend controls and team card management',
            },
            {
                'card_id': 'funding_circle_cashback',
                'badge': 'Cashback Rival',
                'badge_color': 'gold',
                'tagline': '2% cashback for 6 months, then 1% uncapped',
            },
        ],
    },

    'card_ids': ['capital_on_tap'],
    'separate_card_ids': ['barclaycard', 'moss', 'funding_circle_cashback'],

    'card_overrides': {
        'capital_on_tap': {
            'fit_label': 'Under review',
            'summary_strip': 'From 13.86% APR (average 46.05%) &middot; Up to &pound;250k limit &middot; Limited companies and LLPs only',
            'verdict': (
                'High credit limits and no bank account requirement make Capital on Tap genuinely useful '
                'for limited companies that carry a balance. The problem is the advertised floor rate is not '
                'what most borrowers pay. The average rate in Q4 2025 was 46.05%. If you&rsquo;re going to '
                'carry a balance, you need to know what rate you&rsquo;re actually likely to get before you apply.'
            ),
            'editorial_heading': 'High limits, fast decisions &mdash; but the rate you see advertised is not the rate most people pay',
            'best_for': 'Limited companies spending &pound;5k+/month that clear the balance monthly, or those who specifically need a high credit limit',
            'watch_out': 'The 13.86% is the floor rate, not the representative APR. The rep APR is 34.9% and the actual average rate (Oct&ndash;Dec 2025) was 46.05%. Sole traders and partnerships cannot apply.',
            'not_ideal': 'Sole traders (excluded entirely), limited companies that carry a balance and haven&rsquo;t confirmed their individual rate, or businesses wanting rewards on a charge card structure',
            'eligibility': 'UK limited companies and LLPs with Companies House registration. Minimum annual revenue of &pound;24,000. Sole traders and partnerships excluded.',
        },
        'barclaycard': {
            'fit_label': 'Alternative: open to sole traders and more predictable rate',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; No bank account required',
            'verdict': 'The broadest eligibility of any traditional card. Higher APR than Capital on Tap&rsquo;s floor, but the rate is predictable and it accepts sole traders and partnerships that Capital on Tap excludes.',
            'editorial_heading': 'Wider access than Capital on Tap, and you know the rate upfront',
            'best_for': 'Businesses that need confirmed upfront APR and wider entity eligibility',
            'watch_out': '25.5% APR is the representative rate &mdash; most applicants will pay this.',
            'not_ideal': 'You need credit limits above &pound;15k',
            'eligibility': 'Sole traders, partnerships, limited companies. No BCA required.',
        },
        'moss': {
            'fit_label': 'Alternative: charge card with spend controls',
            'summary_strip': 'No credit interest &middot; Prepaid/charge structure &middot; Limited companies',
            'verdict': (
                'Moss is a charge card and prepaid platform, not a revolving credit card. '
                'If you want capital controls and team spend visibility rather than a credit line, '
                'it&rsquo;s a different product solving a different problem.'
            ),
            'editorial_heading': 'Spend controls rather than a credit line &mdash; a different product category',
            'best_for': 'Finance teams wanting employee card controls without a revolving credit facility',
            'watch_out': 'This is not a substitute for Capital on Tap&rsquo;s credit line. It solves a different problem.',
            'not_ideal': 'You need a credit facility to cover cash flow gaps',
            'eligibility': 'UK limited companies.',
        },
        'funding_circle_cashback': {
            'fit_label': 'Alternative: cashback card with no annual fee',
            'summary_strip': '34.9% rep. APR &middot; 2% cashback for 6 months, then 1% &middot; No annual fee',
            'verdict': (
                'A straightforward cashback card with no annual fee. The 34.9% APR is higher than '
                'Capital on Tap&rsquo;s floor but is a fixed representative rate &mdash; no ambiguity about '
                'what you&rsquo;ll pay. Cashback partially offsets the cost if you clear monthly.'
            ),
            'editorial_heading': 'Known rate, cashback back, no annual fee &mdash; if you clear monthly',
            'best_for': 'Businesses that clear the balance monthly and want cashback rather than a large credit line',
            'watch_out': '34.9% rep. APR is higher than Capital on Tap&rsquo;s floor. Cashback benefit disappears if you carry a balance.',
            'not_ideal': 'You need a credit limit above &pound;30k',
            'eligibility': 'UK limited companies only. Min 1 year trading, &pound;30k+ turnover. fundingcircle.com.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': (
             'Capital on Tap suits limited companies that need a high credit limit quickly and '
             'don&rsquo;t have a business current account to use as leverage. It does not suit '
             'sole traders (who are excluded), or limited companies that will carry a balance '
             'without first confirming their individual rate. We verified the published rate data: '
             'the 13.86% starting rate you see advertised is the best case, the representative APR is 34.9%, and the average in Q4 2025 was 46.05%.'
         )},

        {'type': 'hero_zone'},

        {'type': 'toc_start'},

        {'type': 'prose', 'paragraphs': [
            'Capital on Tap is the most heavily marketed fintech business credit card in the UK. '
            'The pitch is hard to ignore: limits up to &pound;250,000, no bank account required, '
            'fast online decisions, and a headline APR that starts at 13.86%.',

            'The headline rate is where things get complicated. Capital on Tap advertises a '
            'starting rate from 13.86%, but the representative APR is 34.9%. The average rate '
            'their borrowers actually paid in Q4 2025 was 46.05%. That gap between the floor, '
            'the representative rate, and the average matters before you apply.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'What Capital on Tap Actually Is'},
        {'type': 'prose', 'paragraphs': [
            'Capital on Tap is a fintech credit card, not a bank. It&rsquo;s issued on the Visa '
            'network and works like a standard revolving credit card &mdash; spend up to your limit, '
            'repay monthly, carry a balance if needed. The difference from a bank card is the underwriting speed, higher limits, and no requirement '
            'to hold a business current account with them.',

            'Credit limits run up to &pound;250,000 &mdash; significantly higher than most bank cards, '
            'which typically cap at &pound;15,000&ndash;&pound;25,000 for SMEs. The application is online '
            'and decisions can come within hours. You need to be a UK limited company or LLP '
            'with Companies House registration. Sole traders and partnerships cannot apply. '
            'If you&rsquo;re a sole trader, see our <a href="/business-credit-cards/best-business-credit-cards-for-sole-traders/">best business credit cards for sole traders</a> instead.',
        ]},

        {'type': 'review_card'},

        {'type': 'heading', 'level': 2, 'text': 'The Capital on Tap Rate Problem'},
        {'type': 'prose', 'paragraphs': [
            'The starting rate of 13.86% is the floor, not the norm. The representative APR is 34.9%, '
            'which under FCA rules must be offered to at least 51% of successful applicants. '
            'But the average rate paid in practice was significantly higher still.',

            'Capital on Tap discloses its average interest rate for new customers: 46.05% for '
            'Q4 2025 (October to December). This means the majority of new customers '
            'paid significantly more than even the 34.9% representative rate. If you are planning to carry a balance, '
            'treat 46% as the more realistic planning figure until Capital on Tap confirms '
            'your individual rate.',

            'S&amp;P Global Ratings data from Capital on Tap&rsquo;s London Cards No. 1 and No. 2 '
            'securitisation reports confirms the underlying rate band: Bank of England Base Rate '
            'plus 9.9% to BBR plus 49.9%, with a total portfolio yield of approximately 35%. '
            'At the current base rate of 4.5%, that translates to a theoretical range of 14.4% '
            'to 54.4%. The published average of 46.05% sits comfortably in the upper half '
            'of that range, not in the middle.',

            'To put that in concrete terms: if your business carries a &pound;10,000 balance '
            'for one month at 46% APR, the interest charge is roughly &pound;383. At the '
            'floor rate of 13.86%, the same balance costs roughly &pound;115. That is a '
            '&pound;268 difference in a single month. Over a year of carrying the same balance, '
            'the gap widens to over &pound;3,200. The rate you actually receive is the single '
            'most important variable in whether this card works for your business.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Rate Transparency: What You\u2019ll Actually Pay'},
        {'type': 'prose', 'paragraphs': [
            'Capital on Tap is more transparent than most fintech lenders about its rate data, '
            'but the transparency is easy to miss. The average rate disclosure is buried '
            'in the legal section of their website rather than on the main product page. '
            'Here is what they publish and what it means for you.',

            'The 13.86% starting rate appears on marketing materials as the floor. '
            'The representative APR of 34.9% is the rate at least 51% of approved applicants '
            'are offered under FCA rules. But being offered a rate does not mean most customers '
            'end up paying it. The average paid was considerably higher.',

            'The 46.05% average rate for Q4 2025 is calculated across all new customers who '
            'drew down credit during that period. This is a more honest picture of what borrowers '
            'actually pay. We would like to see this figure on the main product page, not hidden '
            'in the footer.',

            'Your individual rate depends on your company&rsquo;s credit profile, trading history, '
            'and financials. Capital on Tap does not publish a rate band or range, so you cannot '
            'estimate your likely rate before applying. The application itself is a soft search '
            '(no credit file impact), but once you accept an offer, the hard search is recorded. '
            'Apply to see your offered rate, then comparing it against alternatives '
            'before accepting. If your offered rate is above 30%, check whether <a href="/business-credit-cards/compare-barclaycard-business-credit-cards/">Barclaycard at 25.5%</a> '
            'is a better option for your needs.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'How Does the Rate Compare to Other Business Credit Cards?'},
        {'type': 'prose', 'paragraphs': [
            'At the floor rate of 13.86%, Capital on Tap is the cheapest business credit card '
            'on the UK market by a meaningful margin &mdash; Lloyds is next at 15.95%. '
            'At the average rate of 46.05%, it is one of the most expensive. '
            'Barclaycard sits at 25.5%, Funding Circle at 34.9%, and most bank cards '
            'fall between 15% and 25%. You will not know where you sit in that range '
            'until you apply.',
        ]},

        {'type': 'pros_cons',
         'pros': [
             'Credit limits up to &pound;250,000 &mdash; far higher than most bank cards',
             'No business current account required',
             'Open to limited companies regardless of which bank they use',
             'Fast online decisions',
             'No foreign transaction or ATM withdrawal fees',
             'Pro card earns 0.5% cashback (after &pound;299/year fee)',
         ],
         'cons': [
             'Sole traders and partnerships excluded entirely',
             'Average rate (46.05% Q4 2025) is far above the 13.86% floor rate',
             'Pro card cashback requires &pound;299/year subscription &mdash; needs &pound;60k+ annual spend to break even',
             'No Amex-style rewards programme for the standard card',
             'Rate only confirmed post-application, not upfront',
         ]},

        {'type': 'heading', 'level': 2, 'text': 'Who Should and Shouldn&rsquo;t Apply for Capital on Tap'},
        {'type': 'prose', 'paragraphs': [
            'Capital on Tap works well for limited companies that need a large credit line, '
            'clear the balance monthly, and do not have a suitable bank card option. '
            'We reviewed the eligibility criteria in detail: the no-BCA requirement is a genuine '
            'advantage if you bank with a challenger bank '
            'or do not want to tie a credit card to your main banking relationship.',

            'Picture a digital agency banking with Starling. You spend &pound;12,000 a month '
            'on software subscriptions, contractor payments, and ad spend. Your Starling account '
            'does not come with a credit card. Lloyds would give you 15.95% APR, but you would '
            'need to open a Lloyds BCA. Capital on Tap gives you a &pound;50,000+ credit line '
            'without switching banks. If you clear monthly, the 1% cashback earns you &pound;1,440 '
            'a year. That is the ideal use case.',

            'Now picture a two-year-old e-commerce company with uneven cash flow. You carry a balance '
            'three months out of twelve &mdash; typically &pound;8,000&ndash;&pound;15,000 during stock '
            'purchasing periods. If Capital on Tap offers you 40% APR, carrying &pound;10,000 for '
            'one month costs roughly &pound;333. Your annual cashback at &pound;5,000/month is &pound;600. '
            'Three months of carried balance at 40% wipes out two-thirds of your cashback. You would '
            'be better off with Barclaycard at a known 25.5%, where the same carried balance costs '
            '&pound;213 per month.',

            'Industry data suggests approximately 84% of micro-businesses and 94% of small businesses '
            'clear their credit card balances in full each month. If your business falls into that '
            'majority, the rate is less important than the credit limit and cashback. But the picture '
            'changes sharply by sector: in construction &mdash; one of the highest adopters of business '
            'credit cards at 65% ownership &mdash; only 35% clear monthly, with 12% leaving balances '
            'outstanding for six months or more. If your business carries balances seasonally or '
            'regularly, the rate is the first thing to check, not the last.',

            'We would not recommend applying without checking your offered rate first. '
            'If the offered rate is above 25%, '
            'Barclaycard at 25.5% rep. APR is a more predictable alternative for most '
            'businesses that do not need a limit above &pound;15k. '
            'For a direct comparison, see our <a href="/business-credit-cards/capital-on-tap-vs-amex/">Capital on Tap vs Amex head-to-head</a>.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Is Capital on Tap Safe to Use?'},
        {'type': 'prose', 'paragraphs': [
            'Capital on Tap is authorised and regulated by the Financial Conduct Authority (FCA). '
            'Your credit card is issued on the Visa network with the same fraud protections '
            'as any Visa card. The company is not a bank, so deposits are not FSCS-protected, '
            'but since you are borrowing rather than depositing, that distinction does not '
            'apply here. We verified the FCA registration in March 2026.',

            'One protection gap to be aware of: business credit cards do not benefit from '
            'Section 75 consumer protection under the Consumer Credit Act 1974. If a purchase '
            'goes wrong &mdash; a supplier fails to deliver, or goods arrive faulty &mdash; your '
            'recourse is through the Visa chargeback scheme, not the statutory protection that '
            'personal credit cards provide. Chargebacks are a card network process, not a legal '
            'right, and the outcome is not guaranteed. For high-value purchases, this is worth '
            'knowing before you commit.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Alternatives to Capital on Tap'},
        {'type': 'alternatives'},

        {'type': 'heading', 'level': 2, 'text': 'Capital on Tap FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'What APR will I actually get with Capital on Tap?',
             'a': 'The starting rate is from 13.86%, the representative APR is 34.9%, and the average rate paid by new customers in Q4 2025 was 46.05%. Your individual rate depends on your company&rsquo;s credit profile and is only confirmed after you apply. The application is a soft search, so checking your rate does not affect your credit file.'},
            {'q': 'Can sole traders get a Capital on Tap card?',
             'a': 'No. Capital on Tap is restricted to UK limited companies and LLPs registered at Companies House. Sole traders and partnerships cannot apply. Barclaycard Select is the main alternative that accepts sole traders without a bank account requirement.'},
            {'q': 'Is Capital on Tap a real bank?',
             'a': 'No. Capital on Tap is a fintech lender, not a bank. It is authorised and regulated by the FCA and issues cards on the Visa network. Because it is not a bank, FSCS deposit protection does not apply &mdash; but since you are borrowing rather than depositing, that distinction is not relevant here.'},
            {'q': 'How much cashback does Capital on Tap pay?',
             'a': 'The free tier pays 1% cashback on all spend. The Pro tier (&pound;299/year) pays 0.5% cashback. You need roughly &pound;60,000 in annual spend for the Pro tier cashback to offset the annual fee.'},
            {'q': 'Does Capital on Tap charge foreign transaction fees?',
             'a': 'No. Capital on Tap does not charge foreign transaction fees or ATM withdrawal fees, making it one of the cheaper options for overseas business spending.'},
            {'q': 'How fast can I get a Capital on Tap card?',
             'a': 'Decisions can come within hours. On approval, you receive an instant virtual card you can use immediately while waiting for the physical card to arrive.'},
            {'q': 'What credit limit can I get with Capital on Tap?',
             'a': 'Limits run up to &pound;250,000, which is significantly higher than most bank-issued business cards. Your actual limit depends on your company&rsquo;s financials and credit profile.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Rate data:</strong> We verified the 46.05% average rate figure against Capital '
            'on Tap&rsquo;s published average interest rate disclosure for Q4 2025 '
            '(October&ndash;December). The 13.86% representative APR is their published '
            'representative rate as of March 2026. We reviewed the fee structure for both the free and Pro tiers.',

            '<strong>Verification date:</strong> Card details, eligibility criteria, and '
            'rates verified against capitalontap.com on 20 March 2026.',

            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral fees '
            'from some providers listed. This does not affect our rate analysis or editorial '
            'assessment.',

            '<strong>Regulatory note:</strong> This page is editorial content, not regulated '
            'financial advice. <a href="/editorial-policy/">Read our full editorial policy</a>.',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
