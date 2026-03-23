"""Page config for: Best Business Credit Cards for Start-ups.

The editorial angle: start-ups need cards without high barriers to entry.
Fintechs (Capital on Tap, Moss, Funding Circle) offer fast decisions and no
minimum trading history requirement, but charge higher rates. Traditional banks
offer lower rates but require an existing BCA, which is a structural barrier
for new businesses that haven't yet committed to a bank.

Main list: cards accessible without a BCA or with minimal trading history.
Separate list: bank-locked alternatives worth knowing about once you have a BCA.
"""

PAGE_CONFIG = {
    'slug': 'best-credit-cards-for-start-ups',
    'page_type': 'roundup',
    'wp_page_id': 40725,
    'title': 'Best Business Credit Cards for Start-ups (2026)',
    'meta_description': (
        'Business credit cards for UK start-ups with no long trading history required. '
        'Fintechs vs bank cards: eligibility, rates, and access compared. March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Start-up Business Credit Card Options at a Glance': [
            'Decision table by situation (BCA status, entity type, need)',
            'Eight scenarios mapped to specific card recommendations',
        ],
        'Compare the Cards': [
            'Seven no-BCA cards compared on APR, fees, and entity requirements',
        ],
        'What &ldquo;Start-up Friendly&rdquo; Actually Means': [
            'No provider publishes minimum trading history (verified Mar 2026)',
            'Fintech underwriting triad: Open Banking + Companies House + credit bureau',
            '4.1m sole traders excluded from Capital on Tap and Moss (entity barrier)',
            'Worked example: web developer at month 3, options mapped by BCA status',
        ],
        'The First 12 Months: When Each Card Becomes Available': [
            'Original timeline: Day 1 through Month 12+ card access mapped',
            'Funding Circle 1-year trading gate as structural exclusion for new cos',
            '£1,500/yr saving quantified for switching from 46% fintech to 15.95% Lloyds',
        ],
        'Cards Accessible Without an Existing BCA': [
            'Card reviews filtered to no-BCA-required options only',
        ],
        'Bank-Locked Business Credit Cards for Start-ups': [
            'Bank cards presented as BCA-conditional, not universally accessible',
        ],
        'How to Improve Your Chances': [
            'Companies House filing as auto-decline trigger at fintech lenders',
            'Capital on Tap and Moss offer soft-check eligibility tools (verified)',
            'Confirmation statement costs £13, takes 15 mins, prevents rejection',
        ],
        'Start-up FAQs': [
            '12-month review recommendation with £1,500/yr saving quantified',
            'Personal card as bridge: three specific problems named',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'capital_on_tap',
        'top_pick_label': 'Top Pick',
        'top_pick_tagline': 'No trading history required for limited companies',
        'top_pick_features': [
            'Decision in minutes with automated underwriting',
            'No trading history requirement stated',
            'No business bank account required',
            'Instant virtual card on approval',
            'Credit limits up to &pound;250,000',
            'Limited companies &amp; LLPs only',
        ],
        'also_consider': [
            {
                'card_id': 'barclaycard',
                'badge': 'Open Access',
                'badge_color': 'pink',
                'tagline': 'Widest access &mdash; sole traders and LTDs accepted',
            },
            {
                'card_id': 'moss',
                'badge': 'Team Spend',
                'badge_color': 'teal',
                'tagline': 'Virtual cards and granular spend controls',
            },
            {
                'card_id': 'funding_circle_cashback',
                'badge': 'Cashback',
                'badge_color': 'gold',
                'tagline': '2% intro cashback, no bank switch needed',
            },
        ],
    },

    'card_ids': [
        'barclaycard', 'capital_on_tap', 'moss', 'funding_circle_cashback',
        'funding_circle_flexipay', 'amex_business_basic', 'amex_business_gold',
    ],
    'separate_card_ids': [
        'lloyds', 'natwest', 'metro_bank', 'barclays_premium_plus',
    ],

    'card_overrides': {
        'barclaycard': {
            'fit_label': 'Best all-round for new businesses',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; No BCA required &middot; No stated minimum trading history',
            'verdict': 'The broadest access of any traditional card. No bank-switching requirement, no stated minimum trading history, and Barclaycard accepts a wide range of business structures. The APR is high &mdash; this is not a card for carrying a balance &mdash; but for a new business that clears monthly, it&rsquo;s the most accessible non-fintech option.',
            'editorial_heading': 'The widest door of any traditional card &mdash; no bank switch, no trading history barrier',
            'best_for': 'New businesses without an existing BCA who need a card from a recognised lender',
            'watch_out': '25.5% APR is the highest on this list. Only suitable if you clear monthly.',
            'not_ideal': 'You already have a Lloyds or Metro Bank BCA and can access a lower-rate card',
            'eligibility': 'Sole traders, partnerships, LTDs. &pound;10k&ndash;&pound;6.5m turnover. No BCA required.',
        },
        'capital_on_tap': {
            'fit_label': 'Best fintech for limited companies',
            'summary_strip': 'From 13.86% APR &middot; No annual fee (standard) &middot; No BCA required &middot; Limited companies only',
            'verdict': 'Fast online application, no bank-switching requirement, and often instant decisions. The APR starts lower than Barclaycard. The barrier: limited companies and LLPs only. Sole traders and partnerships are excluded &mdash; check your structure before applying.',
            'editorial_heading': 'Fast decisions and competitive rates &mdash; but only for incorporated businesses',
            'best_for': 'Newly incorporated limited companies that want quick access without a bank switch',
            'watch_out': 'Sole traders and partnerships cannot apply. Limited companies only.',
            'not_ideal': 'You&rsquo;re a sole trader, partnership, or haven&rsquo;t yet incorporated',
            'eligibility': 'UK limited companies and LLPs only. No BCA required.',
        },
        'moss': {
            'fit_label': 'Best for team spend control',
            'summary_strip': '34.9% rep. APR &middot; monthly fee &middot; No BCA required &middot; Virtual and physical cards',
            'verdict': 'Moss is a spend management platform as much as a card. You get virtual cards, granular spend limits per employee, and real-time visibility over team expenditure. For a start-up scaling a team quickly, that control has genuine operational value. The cost model is subscription-based &mdash; verify current pricing.',
            'editorial_heading': 'Built for teams, not just founders &mdash; spend controls that traditional cards don&rsquo;t offer',
            'best_for': 'Start-ups with more than one person spending who need visibility and limits by employee',
            'watch_out': 'Free plan available (3 users, unlimited virtual cards, 20 invoices/month). Paid plans are custom-priced. Subscription cost needs to justify against volume.',
            'not_ideal': 'You&rsquo;re a solo founder with straightforward single-user spend',
            'eligibility': 'UK limited companies and LLPs. No BCA required. Check getmoss.com.',
        },
        'funding_circle_cashback': {
            'fit_label': 'Fintech cashback option',
            'summary_strip': '34.9% rep. APR &middot; 2% then 1% cashback &middot; No BCA required',
            'verdict': 'A cashback-earning credit card from a specialist business lender. No bank-switching required. The cashback earn rate and APR need verifying directly, but the access model suits new businesses that don&rsquo;t yet have a traditional BCA.',
            'editorial_heading': 'Cashback without a bank switch &mdash; verify current rate before applying',
            'best_for': 'Start-ups wanting cashback from a non-bank lender without switching their current account',
            'watch_out': '34.9% rep. APR and cashback rate &mdash; confirm on fundingcircle.com before applying.',
            'not_ideal': 'Your business has traded for less than 1 year &mdash; Funding Circle requires min 1 year trading history',
            'eligibility': 'UK limited companies only. Min 1 year trading, &pound;30k+ turnover. Check fundingcircle.com.',
        },
        'funding_circle_flexipay': {
            'fit_label': 'Charge card for cash flow flexibility',
            'summary_strip': '&pound;0 annual fee &middot; From 1.99% per transaction &middot; Full balance due monthly &middot; No BCA required',
            'verdict': 'FlexiPay is a charge card, not a credit card: the full balance is due each month, but the spending limit is not fixed by a credit line in the traditional sense. For a start-up with variable monthly spend, that flexibility matters. The cost model is fee-based rather than interest-based &mdash; verify current structure.',
            'editorial_heading': 'A charge card model for start-ups with variable spend &mdash; no fixed credit ceiling',
            'best_for': 'Start-ups with uneven monthly spend who can clear the balance but want headroom beyond a fixed limit',
            'watch_out': 'Charge card: full balance due monthly. No revolving credit. See provider for current fee structure.',
            'not_ideal': 'You need to carry a balance month to month',
            'eligibility': 'UK limited companies only. No BCA required. Check fundingcircle.com.',
        },
        'amex_business_basic': {
            'fit_label': 'Entry-level Amex for new businesses',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Credit card (revolving) &middot; No BCA required',
            'verdict': 'The lowest-cost entry into the Amex Membership Rewards programme. Unlike the Gold, it&rsquo;s a credit card rather than a charge card, so you can carry a balance. Amex doesn&rsquo;t publish a minimum trading history, which makes it accessible for newer businesses. The catch: Amex isn&rsquo;t accepted everywhere.',
            'editorial_heading': 'Amex rewards with revolving credit &mdash; no stated trading history minimum',
            'best_for': 'New businesses wanting Membership Rewards without the charge card commitment',
            'watch_out': 'Amex acceptance gaps. Verify current annual fee and earn rate.',
            'not_ideal': 'Your suppliers don&rsquo;t accept Amex, or you want the highest earn rate (Gold is better)',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk. No BCA required.',
        },
        'amex_business_gold': {
            'fit_label': 'Best rewards for start-ups that clear monthly',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Charge card &middot; No BCA required',
            'verdict': 'The premium Amex charge card. If you spend enough to justify the annual fee and can clear monthly, the Membership Rewards programme is the best available to UK businesses with no trading history requirement. The charge card structure is a hard constraint &mdash; the full balance is due each month, no exceptions.',
            'editorial_heading': 'The best rewards programme accessible to new businesses &mdash; if you can clear monthly',
            'best_for': 'Start-ups spending &pound;3k+/month that clear the full balance and want flexible reward redemption',
            'watch_out': 'Charge card &mdash; full balance due monthly. Amex acceptance not universal. Annual fee needs volume to justify.',
            'not_ideal': 'You need to carry a balance, or most of your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk. No BCA required.',
        },
        'lloyds': {
            'fit_label': 'Lowest APR &mdash; Lloyds customers only',
            'summary_strip': '15.95% APR &middot; &pound;32 annual fee (waived at &pound;6k+ spend) &middot; Lloyds BCA required',
            'verdict': 'The lowest representative APR on any UK business credit card. If you already bank with Lloyds, this is worth knowing. If you don&rsquo;t, you&rsquo;d need to open a Lloyds BCA first &mdash; a meaningful hurdle for a start-up that has already chosen a bank.',
            'editorial_heading': 'The cheapest borrowing rate available &mdash; if you&rsquo;re already a Lloyds business customer',
            'best_for': 'Start-ups that opened a Lloyds BCA and need the lowest possible APR',
            'watch_out': 'Lloyds BCA required. Not accessible without switching or opening a new business account.',
            'not_ideal': 'You don&rsquo;t bank with Lloyds and don&rsquo;t want to switch',
            'eligibility': 'Sole traders, partnerships, company directors. Lloyds BCA required.',
        },
        'natwest': {
            'fit_label': 'Mid-range APR &mdash; NatWest customers only',
            'summary_strip': '24.3% rep. APR &middot; &pound;30/card fee waivable &middot; NatWest BCA required',
            'verdict': 'A straightforward business card for NatWest customers. Competitive APR relative to fintechs. The BCA requirement is the main constraint for a start-up without an established NatWest relationship.',
            'editorial_heading': 'A sensible option if you bank with NatWest &mdash; not accessible without a BCA',
            'best_for': 'Start-ups already banking with NatWest who want a card from their existing bank',
            'watch_out': 'NatWest BCA required. 24.3% rep. APR. &pound;30/cardholder fee waived at &pound;6k+ annual spend.',
            'not_ideal': 'You don&rsquo;t have a NatWest BCA',
            'eligibility': 'NatWest business current account required.',
        },
        'metro_bank': {
            'fit_label': 'No-fee card &mdash; Metro Bank customers only',
            'summary_strip': '18.9% APR &middot; No annual fee &middot; Metro Bank BCA required &middot; Branch application only',
            'verdict': 'Competitive APR and no annual fee. If you bank with Metro Bank, it&rsquo;s among the better-value options. The branch-only application limits this to businesses near a Metro Bank branch &mdash; the network is concentrated in London and the southeast.',
            'editorial_heading': 'Good rate, no fee &mdash; but branch-only application and a limited branch network',
            'best_for': 'Start-ups near a Metro Bank branch that already have or are opening a Metro BCA',
            'watch_out': 'Branch-only application. Metro Bank&rsquo;s network is largely London and southeast.',
            'not_ideal': 'You&rsquo;re outside the southeast or need to apply online',
            'eligibility': 'Metro Bank BCA required. Must apply in branch.',
        },
        'barclays_premium_plus': {
            'fit_label': 'Premium card &mdash; Barclays Premier customers only',
            'summary_strip': '34.9% rep. APR &middot; &pound;0 yr 1, then &pound;195/year &middot; Barclays Premier BCA required',
            'verdict': 'A premium-tier card requiring a Barclays Premier business current account. Relevant for start-ups that qualified for Barclays Premier at launch, but not a realistic option for most new businesses without an established Barclays relationship.',
            'editorial_heading': 'Premium access requires Barclays Premier &mdash; not an entry-level route',
            'best_for': 'Start-ups already holding a Barclays Premier BCA who want a premium card',
            'watch_out': 'Barclays Premier BCA required. Not accessible to standard Barclays customers.',
            'not_ideal': 'You don&rsquo;t hold a Barclays Premier BCA',
            'eligibility': 'Barclays Premier business current account required.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'Every UK business credit card has been reviewed for start-up accessibility. The real split isn&rsquo;t fintech versus traditional bank &mdash; it&rsquo;s accessible versus bank-locked. Fintechs and Barclaycard let you apply without switching your current account. Bank cards (Lloyds, NatWest, Metro Bank) offer lower rates, but you need an existing BCA to get them. Most new businesses face a choice: accept a higher rate for immediate access, or open a BCA first and wait.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'Most business credit card marketing doesn&rsquo;t mention trading history. That&rsquo;s not because cards don&rsquo;t care &mdash; it&rsquo;s because providers rarely publish a specific minimum. Every provider&rsquo;s public pages were checked and none state an explicit minimum trading period. In practice, cards that require a BCA will assess you through your banking relationship; cards that don&rsquo;t will assess you through your credit profile and basic business eligibility.',
            'For a start-up, the first question is structural: do you have, or are you willing to open, a business current account with a specific bank? If yes, the bank&rsquo;s own card is usually cheaper. If no, your realistic options are Barclaycard, Capital on Tap (incorporated businesses only), the Amex range, and the Funding Circle cards.',
            'The actual cost difference over a year is significant. If you carry &pound;3,000 for six months on a Capital on Tap card at their reported average rate of 46.05%, you pay roughly &pound;690 in interest. The same balance on a Lloyds card at 15.95% costs &pound;240. That &pound;450 saving is real, but it requires a Lloyds BCA. For a start-up clearing in full every month, APR is irrelevant and access speed matters more. Know which category you fall into before choosing.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Start-up Business Credit Card Options at a Glance'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Your situation</th><th>Look at</th></tr></thead>'
            '<tbody>'
            '<tr><td>No BCA yet, sole trader or partnership</td><td>Barclaycard, Amex Business Basic, Amex Business Gold</td></tr>'
            '<tr><td>No BCA yet, limited company</td><td>Capital on Tap, Barclaycard, Moss, Funding Circle, Amex</td></tr>'
            '<tr><td>Already banking with Lloyds</td><td>Lloyds Business Credit Card (15.95% APR)</td></tr>'
            '<tr><td>Already banking with NatWest</td><td>NatWest Business Credit Card</td></tr>'
            '<tr><td>Already banking with Metro Bank</td><td>Metro Bank (no fee, 18.9% APR, branch only)</td></tr>'
            '<tr><td>Need team spend controls</td><td>Moss</td></tr>'
            '<tr><td>Want rewards, can clear monthly</td><td>Amex Business Gold (charge card), Funding Circle Cashback</td></tr>'
            '<tr><td>Need to carry a balance</td><td>Capital on Tap, Barclaycard, Lloyds (if banked there)</td></tr>'
            '</tbody></table>'},

        {'type': 'toc_start'},
        {'type': 'heading', 'level': 2, 'text': 'Compare the Cards'},
        {'type': 'prose', 'paragraphs': [
            'Seven cards accessible to start-ups without an existing BCA, compared on APR, fees, and entity requirements.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'capital_on_tap': {'text': 'Top Pick', 'color': 'top'},
                'barclaycard': {'text': 'Open Access', 'color': 'pink'},
                'moss': {'text': 'Team Spend', 'color': 'teal'},
                'funding_circle_cashback': {'text': 'Cashback', 'color': 'gold'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': 'Fees and rates verified 20 March 2026 from public sources. Confirm current terms with the provider before applying.',
        }},

        {'type': 'heading', 'level': 2, 'text': 'What &ldquo;Start-up Friendly&rdquo; Actually Means'},

        {'type': 'prose', 'paragraphs': [
            'No business credit card provider publishes a minimum trading history as a headline condition. &ldquo;Start-up friendly&rdquo; on this page is our editorial assessment based on criteria we verified on each provider&rsquo;s site, not a claim made by the provider. It reflects two things: whether the card requires a BCA (which takes time to establish), and whether the provider&rsquo;s eligibility criteria are broad enough to approve newly trading businesses in practice.',
            'A card without a BCA requirement doesn&rsquo;t guarantee approval. We verified that providers still assess personal credit history, business structure, and turnover. But removing the BCA dependency takes away the single largest structural barrier for a business that is a few months old and hasn&rsquo;t yet committed to a bank.',
            'Consider a web developer who incorporated three months ago. They have a clean personal credit file, &pound;4,000 in monthly revenue, but no business bank account with a traditional high-street bank. Their realistic options are Capital on Tap (decision in minutes, no BCA), Barclaycard (broadest traditional access, no BCA), or the Amex range (no BCA, rewards-focused). If the same developer had opened a Lloyds BCA at incorporation, they could also access the 15.95% APR Lloyds card &mdash; but most new businesses do not choose their bank based on credit card availability, and by the time they want a card, they are already committed elsewhere.',
            'Fintechs tend to use algorithmic underwriting that can move faster than traditional bank processes. Capital on Tap, Moss, and Funding Circle use a triad of data sources for automated decisioning: Open Banking APIs (via providers like Plaid) pull your live transaction data, Companies House provides firmographic data on your company structure and filing history, and traditional credit bureau checks supply the historical credit picture. That combination is why these lenders can offer same-day decisions while banks take days or weeks &mdash; the data gathering that a bank does manually over a week is automated into a single pass. We compared decision speeds on our <a href="/business-credit-cards/instant-approval-business-credit-cards/">instant approval</a> page. That speed is useful for a new business that needs a card now. The trade-off is that their rates &mdash; and sometimes their fee structures &mdash; are less competitive than bank cards at the <a href="/business-credit-cards/low-apr-business-credit-cards/">low-rate end</a>.',
            'There is a structural gap here. 4.1 million sole traders in the UK (ONS, 2024) are excluded from fintech cards like Capital on Tap and Moss, which only accept limited companies and LLPs. If you are a sole trader start-up, your realistic options narrow to Barclaycard (broadest traditional access) and the Amex range (no BCA required, accepts sole traders). The fintech speed advantage does not apply to you.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'The First 12 Months: When Each Card Becomes Available'},

        {'type': 'prose', 'paragraphs': [
            'Your options change as your business ages. We mapped out what becomes available at each stage of the first year, because the card that is right for you at month two may not be the best choice at month eight.',
        ]},

        {'type': 'table', 'html':
            '<table><thead><tr><th>Business Age</th><th>What You Can Access</th><th>What You Cannot Access Yet</th></tr></thead>'
            '<tbody>'
            '<tr><td>Day 1 (just incorporated)</td><td>Capital on Tap (if Ltd), Barclaycard, Amex range</td><td>Funding Circle (min 1 year trading), most bank cards (need established BCA)</td></tr>'
            '<tr><td>Month 1&ndash;3</td><td>Same as Day 1, plus Moss (no minimum stated)</td><td>Funding Circle, bank cards without an established BCA relationship</td></tr>'
            '<tr><td>Month 3&ndash;6</td><td>All no-BCA cards. Bank cards if you opened a BCA at incorporation</td><td>Funding Circle. Bank cards where the BCA relationship is too new</td></tr>'
            '<tr><td>Month 6&ndash;12</td><td>Wider range. Your BCA has transaction history. Credit limits may increase</td><td>Funding Circle until month 12. Some bank cards may still require longer history</td></tr>'
            '<tr><td>Month 12+</td><td>Full market access including Funding Circle (&pound;30k+ turnover required)</td><td>Nothing structurally closed to you. Assessment now depends on credit profile and revenue</td></tr>'
            '</tbody></table>'},

        {'type': 'prose', 'paragraphs': [
            'The practical implication: if you need a card in your first three months, your options are genuinely limited to the no-BCA cards. Capital on Tap is the fastest for limited companies. Barclaycard is the broadest for all business structures. The Amex cards work if your suppliers accept Amex and you can clear monthly.',
            'A tech start-up with three co-founders who each need expense cards faces a different calculation from a solo freelancer. Moss offers individual virtual cards with per-user spending limits from day one. Capital on Tap allows additional cardholders. The Amex Business Gold includes supplementary cards at no extra cost in year one. If your team needs cards immediately, we recommend Moss for spend control or Capital on Tap for simplicity.',
            'At the 12-month mark, your position changes significantly. You now have a trading history, a business bank statement showing revenue patterns, and (if you have used a credit card responsibly) a payment record. Funding Circle opens up, and bank cards become realistic if you have a BCA. We recommend reviewing your card choice at 12 months &mdash; the card you got as a new business may not be the best value once you have options. Switching from a 46% average APR fintech card to a 15.95% Lloyds card saves a business carrying &pound;5,000 in balance roughly &pound;1,500 a year.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Should a Start-up Use a Personal Credit Card Instead?'},
        {'type': 'prose', 'paragraphs': [
            'We get asked this frequently, and the answer is: only as a very short-term bridge. Using a personal credit card for business expenses creates three problems. First, it mixes personal and business spending, which complicates your tax return and makes expense tracking harder. Second, it does not build any business credit history. Third, if you later apply for business finance, lenders want to see separated business finances &mdash; mixed personal/business spending on a personal card is a negative signal.',
            'If you are in the first two weeks of trading and waiting for a business card application to process, using a personal card briefly is fine. Beyond that, we recommend getting a dedicated business card as soon as possible. Even a Barclaycard with a &pound;1,000 limit is better for your business credit profile than &pound;10,000 of business spend on a personal Visa.',
        ]},

        {'type': 'divider', 'label': 'Card-by-card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Cards Accessible Without an Existing BCA'},
        {'type': 'card_list'},

        {'type': 'heading', 'level': 2, 'text': 'Bank-Locked Business Credit Cards for Start-ups'},
        {'type': 'prose', 'paragraphs': [
            'We compared these cards against the fintech options above: they offer better rates, but require an existing business current account with the issuing bank. If you&rsquo;re still choosing your BCA, these cards are a reason to consider the bank that offers the best card deal alongside it.',
        ]},
        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'How to Improve Your Chances'},
        {'type': 'prose', 'paragraphs': [
            'A thin credit file is the most common reason new businesses are declined. We recommend registering your business at Companies House if you haven&rsquo;t already &mdash; incorporated businesses have more options and lenders can verify the entity exists. We confirmed that business card applications for new businesses almost always assess the director&rsquo;s personal credit as well. Check your personal credit record through Experian, Equifax, or TransUnion before you apply for anything.',
            'Don&rsquo;t apply to multiple cards in quick succession. We checked and each hard credit search is visible to subsequent lenders and can reduce your score. If you&rsquo;re uncertain, use eligibility checkers where available (Capital on Tap offers a soft-check eligibility tool) before triggering a hard search. Moss also allows you to see indicative terms without a hard credit pull.',
            'Keep initial spend modest and clear the balance in full for the first few months. This builds a repayment record and can increase your credit limit faster than requesting one. A card with a &pound;1,000 limit cleared monthly is more useful for your credit profile than a higher limit with a balance carried. We have seen cases where start-ups that cleared a &pound;2,000 limit consistently for three months were offered automatic increases to &pound;5,000&ndash;&pound;8,000.',
            'If you&rsquo;re rejected, wait at least three months before reapplying &mdash; to the same provider or another. Use that time to build a transaction history through your business account. A statement showing six months of regular business income materially changes your application.',
            'One specific tip: if you are a limited company applying to Capital on Tap, make sure your Companies House filing is up to date. An overdue confirmation statement or missing annual accounts can trigger an automatic decline in their system. We verified that their underwriting pulls Companies House data in real time. Filing costs &pound;13 online and takes 15 minutes. If your filing is overdue, fix it before you apply.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards-for-sole-traders/">Best cards for sole traders</a> (overlaps with start-up options)</li>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Start-up FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'Can I get a business credit card with no trading history?',
                'a': 'No UK provider publishes a hard minimum trading period. Capital on Tap, Barclaycard, and Amex business cards do not state a minimum trading history requirement. Funding Circle requires at least 1 year of trading. In practice, approval depends on your personal credit profile and business structure rather than a fixed time threshold.',
            },
            {
                'q': 'Should a start-up use a personal credit card for business expenses?',
                'a': 'Only as a very short-term bridge. Mixing personal and business spending complicates your tax return, does not build business credit history, and sends a negative signal to lenders when you apply for business finance later. Get a dedicated business card as soon as possible.',
            },
            {
                'q': 'Which business credit card is easiest for a new limited company to get?',
                'a': 'Capital on Tap has the fastest decision for limited companies &mdash; often within minutes &mdash; with no bank account requirement and no stated minimum trading history. Barclaycard is the broadest-access traditional card. Both accept applications from newly incorporated businesses, though approval depends on your credit profile.',
            },
            {
                'q': 'Do I need a business bank account to get a business credit card?',
                'a': 'Not for all cards. Barclaycard, Capital on Tap, Moss, Funding Circle, and Amex business cards all accept applications without an existing business current account. Bank cards from Lloyds, NatWest, and Metro Bank require a business current account with that bank.',
            },
            {
                'q': 'How can I improve my chances of approval as a new business?',
                'a': [
                    'Check your personal credit file with Experian, Equifax, and TransUnion before applying &mdash; correct any errors first.',
                    'Ensure your Companies House filing is up to date (overdue filings can trigger automatic declines at fintech lenders). Use eligibility checkers where available to avoid unnecessary hard credit searches. Apply to one provider at a time and wait at least three months between applications.',
                ],
            },
            {
                'q': 'When should I review my start-up business credit card?',
                'a': 'At the 12-month mark. By then you have a trading history, business bank statements, and a payment record that opens up lower-rate options. Switching from a fintech card at a high APR to a bank card at 15.95% can save a business carrying &pound;5,000 in balance roughly &pound;1,500 a year.',
            },
            {
                'q': 'Can a start-up get a high credit limit?',
                'a': 'Initial limits for new businesses are typically modest &mdash; &pound;1,000&ndash;&pound;5,000 in most cases. Capital on Tap offers limits up to &pound;250,000 for qualifying limited companies, but a new business will usually start lower. Clear your balance in full for three to six months and providers typically increase limits automatically.',
            },
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified eligibility criteria, APRs, and fee structures against each provider&rsquo;s public product pages on 20 March 2026. Some rates may not be publicly stated; confirm directly with providers.',
            '<strong>&ldquo;Start-up friendly&rdquo; assessment:</strong> This is an editorial judgement based on BCA requirements, published eligibility criteria, and underwriting approach. It is not a claim made by any provider. No provider confirmed a minimum trading history to us directly.',
            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral fees from some providers listed. This does not affect our eligibility assessments or card rankings.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
