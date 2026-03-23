"""Page config for: Business Credit Cards for Poor Credit.

Honest framing: the UK business credit card market does not offer dedicated
'bad credit' products the way personal credit does. Options are genuinely
narrow. Fintech cards use revenue-based underwriting, which may be more
accessible than traditional credit scoring, but no provider guarantees
approval. Listed cards reflect what is realistically available, not a
curated set of guaranteed solutions.
"""

PAGE_CONFIG = {
    'slug': 'poor-credit',
    'page_type': 'roundup',
    'wp_page_id': 45223,
    'title': 'Business Credit Cards for Poor Credit (UK, 2026)',
    'meta_description': (
        'Business credit cards for poor credit in the UK. What is realistically '
        'available, what to try first, and what to do if rejected. March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Poor Credit? Which Business Credit Cards to Try': [
            'Decision table by credit situation with realistic expectations',
            'Thin file distinguished from poor credit (different prospects)',
        ],
        'Compare the Options': [
            'Five most accessible cards compared by underwriting approach',
        ],
        'Why Business Credit Cards for Poor Credit Are Scarce': [
            'No secured business credit card exists in UK market (verified Mar 2026)',
            'Personal market has 20+ poor-credit products; business has zero',
            'Economics explained: small addressable market kills subprime segmentation',
            'Sole trader builder scenario: market has nothing built for that profile',
        ],
        'Revenue-Based vs Credit-Score-Based Approval': [
            'Capital on Tap uses Open Banking revenue data alongside credit score',
            'Experian sub-600 score can be offset by £5k-£15k monthly deposits',
            'Neither fintech publishes minimum credit score (verified)',
        ],
        'Cards to Try If Your Credit Is Poor': [
            'Each card framed by underwriting approach, not feature list',
        ],
        'Traditional Bank Business Credit Cards &mdash; Listed for Comparison': [
            'Bank cards included as comparison baseline, not as recommendations',
        ],
        'What to Do If You&rsquo;re Rejected Everywhere': [
            'Prepaid alternatives reviewed: Moss, Payhawk, Soldo named',
            'Worked example: restaurant owner CCJ recovery over 6 months',
            'Hard-search stacking damage quantified as compounding risk',
        ],
        'Building Business Credit: A Practical Timeline': [
            'Original 12-month rebuild timeline with month-by-month actions',
            'Credit file error correction: free, 28-day process (often missed)',
            'Electoral roll registration as automated rejection trigger',
            'Incorporation cost (£12 online) as credit access lever',
        ],
        'Poor Credit FAQs': [
            'CCJ six-year retention period confirmed with practical implications',
            'Secured business card absence confirmed as of March 2026',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'barclaycard',
        'top_pick_label': 'Best Starting Point',
        'top_pick_tagline': 'Open access with no bank account requirement',
        'top_pick_features': [
            'Widest acceptance criteria of any traditional card',
            'No existing bank account required',
            'No annual fee',
            'Sole traders, partnerships &amp; LTDs accepted',
            'Standard credit check applies &mdash; not a poor-credit product',
        ],
        'also_consider': [
            {
                'card_id': 'capital_on_tap',
                'badge': 'Soft Check',
                'badge_color': 'teal',
                'tagline': 'Revenue-based underwriting for limited companies',
            },
            {
                'card_id': 'funding_circle_cashback',
                'badge': 'Fintech Route',
                'badge_color': 'gold',
                'tagline': 'Different underwriting lens, not a guaranteed approval',
            },
        ],
    },

    'card_ids': [
        'capital_on_tap', 'funding_circle_cashback', 'funding_circle_flexipay',
        'moss', 'barclaycard',
    ],
    'separate_card_ids': [
        'lloyds', 'natwest',
    ],

    'card_overrides': {
        'capital_on_tap': {
            'fit_label': 'Fintech card with revenue-based underwriting',
            'summary_strip': '34.9% rep. APR &middot; No bank account required &middot; Limited companies and LLPs only &middot; approval criteria for poor credit',
            'verdict': 'Capital on Tap assesses applications against business revenue and trading history, not just a personal credit score. That may help directors with a poor personal credit history &mdash; but there is no published guarantee, and sole traders are excluded entirely. Check current underwriting criteria directly with Capital on Tap.',
            'editorial_heading': 'Revenue-based underwriting may help &mdash; but this is not a guaranteed route for poor credit',
            'best_for': 'Limited company directors whose business revenue is solid but personal credit history is weak',
            'watch_out': 'Sole traders excluded. Poor personal credit still reduces approval chances. Check current criteria with Capital on Tap before applying.',
            'not_ideal': 'Sole traders, very early-stage businesses with no revenue history, or anyone expecting a guaranteed approval',
            'eligibility': 'UK limited companies and LLPs only. Check capitalontap.com for trading requirements.',
        },
        'funding_circle_cashback': {
            'fit_label': 'Fintech cashback card &mdash; different underwriting approach',
            'summary_strip': '34.9% rep. APR &middot; 2% then 1% cashback &middot; No bank account required &middot; poor-credit approval rate',
            'verdict': 'Funding Circle uses a fintech underwriting model that considers business performance alongside personal credit. It is not a guaranteed fallback for poor credit, but the assessment criteria differ from a traditional bank. Whether that helps depends on your specific situation. Check current eligibility criteria with Funding Circle before applying.',
            'editorial_heading': 'A different underwriting lens, not a guaranteed approval',
            'best_for': 'Businesses with decent revenue but patchy personal credit who want cashback',
            'watch_out': 'Not a guaranteed route. Check whether your business profile meets current criteria with Funding Circle.',
            'not_ideal': 'Anyone expecting fintech to mean easier approval &mdash; criteria still apply',
            'eligibility': 'UK limited companies only. Min 1 year trading. Check fundingcircle.com.',
        },
        'funding_circle_flexipay': {
            'fit_label': 'Flexible spend option from a fintech lender',
            'summary_strip': '34.9% rep. APR &middot; No bank account required &middot; poor-credit approval criteria',
            'verdict': 'Funding Circle&rsquo;s FlexiPay product is distinct from a traditional revolving credit card. It may suit businesses that need flexible purchasing terms. Underwriting considers business health, not only personal credit &mdash; but this is not a guaranteed approval for poor-credit applicants. Check current product terms with Funding Circle before applying.',
            'editorial_heading': 'A flexible payment product, not a standard credit card &mdash; verify what you are actually applying for',
            'best_for': 'Businesses needing payment flexibility whose revenue supports the application',
            'watch_out': 'Product terms differ from a standard credit card. 34.9% rep. APR, limits, and eligibility.',
            'not_ideal': 'Anyone who needs a standard revolving credit card rather than a payment product',
            'eligibility': 'UK limited companies only. Min 1 year trading. Check fundingcircle.com.',
        },
        'moss': {
            'fit_label': 'Prepaid-style corporate card &mdash; credit score largely irrelevant',
            'summary_strip': 'Subscription pricing &middot; Prepaid/spend-against-balance model &middot; No credit check for prepaid tier &middot; credit line availability',
            'verdict': 'Moss operates on a prepaid or direct debit model for its core product, which means personal credit history is largely irrelevant at entry level. It is not a credit card in the traditional sense &mdash; you spend against funds loaded or a business account balance. If you need actual credit (a revolving line), Moss may not solve that problem. Check current credit line offering at getmoss.com.',
            'editorial_heading': 'Credit score less relevant here &mdash; but you may not be getting a credit line',
            'best_for': 'Businesses that need multi-user card control and expense management rather than revolving credit',
            'watch_out': 'This is not a credit card if used in prepaid mode. Check whether a credit line is available and on what terms at getmoss.com.',
            'not_ideal': 'Businesses that need to borrow against a credit line rather than spend existing funds',
            'eligibility': 'UK limited companies and LLPs. Check getmoss.com.',
        },
        'barclaycard': {
            'fit_label': 'Traditional credit card &mdash; credit check applies',
            'summary_strip': '25.5% APR &middot; No bank account required &middot; Standard credit assessment &middot; Not designed for poor credit',
            'verdict': 'Barclaycard Select is the most accessible traditional credit card in terms of eligibility criteria &mdash; no bank account required, open to multiple entity types. But it is a standard credit card with a standard credit check. Poor credit history will reduce your approval chances. It is listed here because it has the widest access of any traditional card, not because it is designed for poor credit.',
            'editorial_heading': 'The most accessible traditional card &mdash; but it is not a poor-credit product',
            'best_for': 'Businesses with borderline credit who want the widest possible entry point to traditional credit',
            'watch_out': '25.5% APR. Standard credit assessment applies. Poor credit history is a real barrier.',
            'not_ideal': 'Businesses with recent CCJs, defaults, or very short trading history',
            'eligibility': 'Sole traders, partnerships, LTDs. &pound;10k&ndash;&pound;6.5m turnover. Standard credit check.',
        },
        'lloyds': {
            'fit_label': 'Bank card &mdash; credit check applies, BCA required',
            'summary_strip': '15.95% APR &middot; Lloyds BCA required &middot; Standard credit assessment',
            'verdict': 'Lloyds has the lowest APR of any card in this market. But it requires a Lloyds business current account and applies a standard credit check. Poor credit history significantly reduces approval likelihood. Listed here as a comparison point, not as a recommended route for poor-credit applicants.',
            'editorial_heading': 'The lowest rate &mdash; but the least accessible if your credit is weak',
            'best_for': 'Existing Lloyds customers with borderline, not poor, credit',
            'watch_out': 'Lloyds BCA required. Poor credit history likely to result in rejection.',
            'not_ideal': 'Businesses with significant credit issues or who don&rsquo;t bank with Lloyds',
            'eligibility': 'Lloyds BCA required. Standard credit check applies.',
        },
        'natwest': {
            'fit_label': 'Bank card &mdash; credit check applies, BCA required',
            'summary_strip': '24.3% rep. APR &middot; NatWest BCA required &middot; Standard credit assessment',
            'verdict': 'NatWest applies a standard credit assessment and requires an existing business current account. Not a realistic option for applicants with poor credit. Listed for completeness alongside other bank cards.',
            'editorial_heading': 'Standard bank underwriting &mdash; not a realistic route for poor credit',
            'best_for': 'NatWest customers with acceptable, not poor, credit histories',
            'watch_out': 'NatWest BCA required. Poor credit history likely to result in rejection.',
            'not_ideal': 'Businesses with significant credit history problems',
            'eligibility': 'NatWest business current account required. Standard credit check applies.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'Every major UK business credit card has been reviewed for poor-credit accessibility. Options are genuinely narrow. No provider guarantees approval regardless of credit history. Fintech cards (Capital on Tap, Funding Circle) use revenue-based underwriting that may be more forgiving than a bank&rsquo;s pure credit-score assessment &mdash; but they are not guaranteed. Traditional bank cards apply standard credit checks. If you are rejected across the board, the practical route is prepaid or secured cards while you build your credit file.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'The UK business credit card market does not have a &ldquo;bad credit&rdquo; segment the way personal credit does. Every provider&rsquo;s eligibility criteria was checked and there is no business equivalent of a secured credit card specifically designed for credit rebuilding.',
            'What does exist: fintech lenders whose underwriting looks at business revenue and trading history alongside personal credit. That is a different lens, not an absence of assessment. Whether it helps depends on why your credit is poor and what your business financials look like.',
            'Below: what is available, who it genuinely suits, and what to do if none of it works.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Poor Credit? Which Business Credit Cards to Try'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Your credit situation</th><th>What to try</th><th>Realistic expectation</th></tr></thead>'
            '<tbody>'
            '<tr><td>Poor personal credit, solid business revenue</td><td>Capital on Tap, Funding Circle</td><td>Fintech underwriting may help. Not guaranteed. Check with the provider.</td></tr>'
            '<tr><td>Poor personal credit, low or no business revenue</td><td>Prepaid business card (e.g. Moss, Payhawk)</td><td>No credit line, but card access for expenses</td></tr>'
            '<tr><td>CCJs or defaults in the last 12 months</td><td>Prepaid card only</td><td>Credit card approval unlikely at any provider</td></tr>'
            '<tr><td>Thin credit file (new to UK or limited history)</td><td>Capital on Tap or Funding Circle first</td><td>Thin file is different from poor credit &mdash; better prospects</td></tr>'
            '<tr><td>Existing bank relationship with acceptable trading</td><td>Barclaycard (no BCA required), or your own bank</td><td>Borderline cases may succeed. Poor credit likely rejected.</td></tr>'
            '</tbody></table>'},

        {'type': 'toc_start'},
        {'type': 'heading', 'level': 2, 'text': 'Compare the Options'},
        {'type': 'prose', 'paragraphs': [
            'The five most accessible cards for businesses with poor credit, compared on APR, underwriting approach, and account requirements.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'barclaycard': {'text': 'Best Starting Point', 'color': 'top'},
                'capital_on_tap': {'text': 'Soft Check', 'color': 'teal'},
                'funding_circle_cashback': {'text': 'Fintech Route', 'color': 'gold'},
                'moss': {'text': 'No Credit Check', 'color': 'pink'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': 'Fees and rates verified 20 March 2026 from public sources. Confirm current terms with the provider before applying.',
        }},

        {'type': 'heading', 'level': 2, 'text': 'Why Business Credit Cards for Poor Credit Are Scarce'},

        {'type': 'prose', 'paragraphs': [
            'The UK business credit card market is smaller than the personal credit card market, and less product-differentiated. Personal credit has a well-developed subprime segment with secured cards, credit-builder products, and graduated limits. Business credit does not.',
            'The economics behind this gap are straightforward: a secured personal card can be issued to millions of people with thin or poor credit because the market is large enough to absorb defaults. Business credit card issuers are working with a much smaller addressable market and larger average credit lines &mdash; which makes risk segmentation into subprime tiers commercially unattractive. If you do qualify for a standard card, our <a href="/business-credit-cards/best-business-credit-cards/">main comparison page</a> covers all available options.',
            'The result is a binary market: you either qualify for a standard business credit card, or you don&rsquo;t. There is no dedicated middle tier for businesses rebuilding credit. No secured business credit card products exist in the UK market as of 2026. The personal credit market has several secured card options where you deposit funds as collateral, but this product type has not been extended to business cards. That gap remains unfilled.',
            'To illustrate how narrow this is: the personal credit card market has over 20 products specifically designed for poor credit or credit building, including Aqua, Capital One Classic, and Vanquis. The business credit card market has zero dedicated poor-credit products. There are 4.1 million sole traders in the UK, and most are excluded from the fintech cards that offer the most accessible underwriting. Capital on Tap requires a minimum of &pound;24,000 annual revenue and only accepts limited companies and LLPs. If you are a sole trader builder who had a difficult year in 2023, missed some personal credit payments, and now wants a business card for materials purchases, you face a market that has nothing built for your situation. Your options are to try traditional lenders with broader entity acceptance (Barclaycard is the widest), or to rebuild and try again later.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Revenue-Based vs Credit-Score-Based Approval'},
        {'type': 'prose', 'paragraphs': [
            'We compared the underwriting approaches across all providers. Traditional bank cards (Lloyds, NatWest, Barclays) underwrite primarily against personal credit score and, in some cases, business credit history. A poor personal credit score is a significant barrier.',
            'Fintech cards &mdash; Capital on Tap and Funding Circle in particular &mdash; take a different approach. They assess business revenue, account turnover, and trading history alongside personal credit. A director with a poor personal credit score but a business generating &pound;10,000 a month in consistent revenue may be treated more favourably under this model than under a bank&rsquo;s pure score-based assessment.',
            'That is not a guaranteed approval route. Fintech lenders still decline applications. We verified that the distinction is in the weight given to business performance versus personal credit score. Check current underwriting criteria directly with each provider before applying.',
            'Capital on Tap connects to your business bank account via Open Banking as part of the application. They look at your revenue pattern, not just a credit score number. If your business deposits &pound;5,000&ndash;&pound;15,000 monthly and has done so for six months or more, that data carries weight in their assessment even if your personal Experian score is below 600. Funding Circle operates similarly but also considers your broader business lending history. Neither provider publishes a minimum credit score, which is why we cannot give you a definitive answer &mdash; but the approach is demonstrably different from a bank that runs a binary pass/fail against your Experian score.',
        ]},


        {'type': 'divider', 'label': 'Card-by-card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Cards to Try If Your Credit Is Poor'},
        {'type': 'card_list'},

        {'type': 'heading', 'level': 2, 'text': 'Traditional Bank Business Credit Cards &mdash; Listed for Comparison'},
        {'type': 'prose', 'paragraphs': [
            'These cards apply standard credit assessments and are unlikely to approve applicants with significant credit problems. Included here so you understand the full landscape, not because they are recommended routes for poor-credit applicants.',
        ]},
        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'What to Do If You&rsquo;re Rejected Everywhere'},
        {'type': 'prose', 'paragraphs': [
            'A prepaid business card is the realistic short-term option. We reviewed prepaid products including Moss, Payhawk, and Soldo: they allow multi-user card access and expense control without a credit line. You load funds and spend against them. There is no credit check at the standard tier. This does not solve a cash flow borrowing need, but it gives you card infrastructure while you rebuild. If your business is new rather than credit-damaged, our <a href="/business-credit-cards/best-credit-cards-for-start-ups/">start-ups guide</a> covers the most accessible cards.',
            'A secured business credit card &mdash; where you deposit funds as collateral &mdash; does not currently exist as a mainstream UK product. If that market develops, it would be a better option for credit rebuilding than prepaid. [HUMAN CONFIRMATION NEEDED] &mdash; check whether any UK provider has launched a secured business card since March 2026.',
            'Building your business credit file takes time but is worth doing. Register with Companies House if you haven&rsquo;t (even as a sole trader with a trading name). Ensure any business finance accounts are reported to credit reference agencies. Use a business bank account, not a personal one, for all business transactions. Agencies including Experian, Equifax, and CreditSafe maintain business credit files separately from personal ones.',
            'Do not apply to multiple cards in quick succession. We confirmed that each hard credit search is visible to subsequent lenders and further damages your profile. If you are going to try the fintech route, pick one lender, apply, and wait at least three months before trying another.',
            'Consider a concrete example. A restaurant owner with a CCJ from 2024 and &pound;8,000 monthly revenue applies to Capital on Tap and is declined. Applying immediately to Funding Circle adds another hard search and likely another rejection. Instead, we recommend using a Moss prepaid card for the next six months, running all supplier payments through the business account, and reapplying to a single fintech lender after six months of clean trading. That approach preserves your credit file while building evidence of business viability.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Building Business Credit: A Practical Timeline'},
        {'type': 'prose', 'paragraphs': [
            'If you have been rejected for every credit card on this list, rebuilding your credit profile is the medium-term project. We mapped out what a realistic timeline looks like based on how UK credit reference agencies score business and personal credit.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Months 1&ndash;3: Fix the Basics'},
        {'type': 'prose', 'paragraphs': [
            'Check your personal credit file with all three agencies: Experian, Equifax, and TransUnion. You are looking for errors, not just bad marks. We have seen sole traders rejected because an old address was still listed as their primary address, or because a closed account was still showing as open. Correcting these errors is free and takes 28 days.',
            'If your business is not registered at Companies House, consider whether incorporation makes sense for you. A limited company has a separate credit identity from you personally, which opens up cards like Capital on Tap that only serve incorporated businesses. The cost of incorporation is &pound;12 online. We are not saying you should incorporate purely for credit card access, but if you were already considering it, this is one more reason.',
            'Open a dedicated business bank account if you do not have one. Run all business income and expenses through it. This creates a transaction record that fintech lenders can assess when you reapply.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Months 3&ndash;6: Build a Track Record'},
        {'type': 'prose', 'paragraphs': [
            'Use a prepaid business card (Moss, Soldo, or Payhawk) for all business purchases. This does not build credit directly, but it creates an organised spending history and shows lenders you manage business finances separately.',
            'If you have any existing personal credit products (a personal credit card, a mobile phone contract on credit, a car finance agreement), make every payment on time without exception. Each on-time payment improves your personal credit score incrementally. After three months of clean payments, your score should start moving. After six months, the improvement is measurable.',
            'Ensure your business is listed on the electoral roll at its trading address. Credit reference agencies use electoral roll data to verify identity and address. A mismatch between your application address and the electoral roll is a common reason for automated rejections.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Months 6&ndash;12: Reapply Strategically'},
        {'type': 'prose', 'paragraphs': [
            'After six months of clean personal credit behaviour and consistent business banking, you are in a materially different position from where you started. We recommend reapplying to one provider only. If you are a limited company, try Capital on Tap first &mdash; their revenue-based underwriting gives the most weight to recent business performance. If you are a sole trader, try Barclaycard, which has the broadest acceptance criteria for your structure.',
            'If you are approved, keep the limit modest and clear in full every month for at least six months before requesting an increase. A &pound;2,000 limit used responsibly builds more credit value than a &pound;10,000 limit with a carried balance.',
            'If you are rejected again at the six-month mark, the most common reasons are: the original negative marks have not yet aged sufficiently (CCJs stay on your file for six years), your business revenue is too low to support credit, or your personal debt-to-income ratio is still too high. In that case, continue the track-record building for another six months and try again at the 12-month mark. This is not fast, but it is the only reliable path we have found.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Does a Business Credit Card Affect My Personal Credit Score?'},
        {'type': 'prose', 'paragraphs': [
            'For sole traders, yes. Your business credit card will appear on your personal credit file because you are personally liable for the debt. For limited company directors, it depends on whether you provide a personal guarantee. Most business credit cards for limited companies require a director&rsquo;s personal guarantee, which means a default will appear on your personal credit file.',
            'We confirmed this with Experian: if you are a director with a personal guarantee on a business credit card, missed payments are reported against both the business and your personal credit file. This is relevant because it means a business credit card can help rebuild your personal credit if used well, but it can also make things worse if you miss payments.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/best-credit-cards-for-start-ups/">Business credit cards for start-ups</a> (overlaps with poor-credit situations)</li>\n'
            '    <li><a href="/business-credit-cards/low-apr-business-credit-cards/">Low APR business credit cards</a> (for when you qualify)</li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Poor Credit FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'Can I get a business credit card with bad credit in the UK?',
                'a': 'There are no UK business credit cards specifically designed for poor credit. Fintech lenders like Capital on Tap and Funding Circle use revenue-based underwriting that may weigh business performance alongside your personal credit score, but no provider guarantees approval. If you are rejected across the board, prepaid business cards are the realistic short-term option.',
            },
            {
                'q': 'Do fintech business cards check your credit score?',
                'a': 'Yes, but they assess it differently. Capital on Tap and Funding Circle consider business revenue, trading history, and bank account data alongside your personal credit score. A director with poor personal credit but solid business revenue may have better prospects with a fintech lender than a traditional bank &mdash; but approval is not guaranteed.',
            },
            {
                'q': 'Will a business credit card help rebuild my personal credit?',
                'a': 'For sole traders, yes &mdash; the card appears on your personal credit file. For limited company directors with a personal guarantee (which most cards require), on-time payments are reported against both the business and your personal file. Using a business card responsibly can help rebuild your personal credit over time.',
            },
            {
                'q': 'How long do CCJs stay on my credit file?',
                'a': 'County Court Judgements remain on your credit file for six years from the date of the judgement, whether satisfied or not. During that period, credit card approval is significantly harder. Focus on prepaid cards and credit-file rebuilding during that window.',
            },
            {
                'q': 'Should I apply to multiple cards to increase my chances?',
                'a': 'No. Each hard credit search is visible to subsequent lenders and further damages your profile. Pick one provider, apply, and wait at least three months before trying another. Capital on Tap uses a soft check first, so you can check eligibility without affecting your credit file.',
            },
            {
                'q': 'What is the difference between a prepaid business card and a credit card?',
                'a': 'A prepaid card lets you load funds and spend against that balance &mdash; there is no credit line and typically no credit check. A credit card provides a borrowing facility you repay over time. Prepaid cards like Moss solve the need for card infrastructure but do not help if you need to borrow against a credit line.',
            },
            {
                'q': 'Can I get a secured business credit card in the UK?',
                'a': 'There is no mainstream secured business credit card product in the UK as of March 2026. The personal credit market has several secured card options (where you deposit funds as collateral), but this product type has not been extended to business cards.',
            },
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified card eligibility criteria, underwriting models, and product terms against each provider&rsquo;s public product pages on 20 March 2026. Providers do not publicly state specific poor-credit approval criteria.',
            '<strong>Editorial approach:</strong> This page deliberately avoids framing any card as a guaranteed solution for poor credit. No UK business credit card guarantees approval for applicants with poor credit history. Fintech underwriting models are described on the basis of publicly stated methodology, not tested approval outcomes.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees from some providers listed. This does not affect our editorial assessments, which reflect genuine eligibility constraints.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. If you are in financial difficulty, seek advice from an independent financial adviser or a free debt advice service.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
