"""Page config for: Best Business Credit Cards in the UK (Pillar Page).

This is the master roundup page covering all major UK business credit cards.
All other credit card pages link back here. Longest editorial content (~8-10k words).
WP staging page ID: 40218
"""

PAGE_CONFIG = {
    'slug': 'best-business-credit-cards',
    'page_type': 'roundup',
    'wp_page_id': 40218,  # Set after staging page is created
    'title': 'Best Business Credit Cards in the UK for 2026: Compared and Ranked',
    'meta_description': (
        'Every major UK business credit card compared on APR, fees, cashback, and eligibility. '
        'Verified March 2026.'
    ),
    'verification_date': '20 March 2026',

    # Information gain declarations — what this page adds that competitors omit
    # Required by build-time quality gate (10-evidence-governance.md §12)
    'info_gain': {
        'Compare the Best Business Credit Cards at a Glance': [
            'Amex Pay Over Time at 29.1% APR makes charge cards hybrid products (source: americanexpress.com)',
        ],
        'Which Type of Business Credit Card Do You Need?': [
            '~40% of UK merchants do not accept Amex — need second card for rewards strategy (source: Amex published acceptance data)',
        ],
        'How Much Does a Business Credit Card Actually Cost?': [
            '84% of micro-businesses clear monthly, only 35% in construction (source: UK Finance)',
            'Worked cost comparison: £1,558/year difference between cheapest and most expensive card on same £5k balance',
            'FX fee comparison: HSBC 2.99% vs NatWest/CoT 0% — £359/year on £1k/month overseas spend',
        ],
        'The Bank Account Barrier: Why Most Cards Are Off-Limits': [
            '7 of 12 cards require existing BCA — the single biggest filter competitors bury',
            'Full access-filter table showing which cards need which bank account',
        ],
        'Business Credit Card Limits: What You Can Actually Get': [
            'Published limit ranges by turnover band from provider documentation',
            'Capital on Tap £24k minimum revenue requirement (source: capitalontap.com)',
            'Amex "adaptive limit" — no pre-set limit is not unlimited in practice',
        ],
        'Applying: What Happens and What to Expect': [
            '4.1 million sole traders in UK (source: ONS) — largest demographic, fewest card options',
            'Capital on Tap and Funding Circle both exclude sole traders entirely',
            'Soft vs hard search availability by provider with timeline per provider',
        ],
        'Every Business Credit Card, Reviewed': [
            'CoT advertises "from 9.9%" but average offered rate is 46.05% (source: CoT credit agreement data Q4 2025)',
        ],
        'Also Worth Knowing: Charge Cards and Niche Options': [
            'Amex late payment: £12 fee, 60-day suspension, £95 reinstatement (source: americanexpress.com account terms)',
        ],
        'How We Ranked These Business Credit Cards': [
            'Section 75 does not apply to business credit cards — chargeback is only recourse',
            'Worked ranking examples showing access filter impact on real businesses',
        ],
        'Business Credit Card FAQs': [
            'Section 75 FAQ: business cards excluded, chargeback is voluntary not statutory',
            'Sole trader FAQ: specific providers that exclude sole traders named',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'capital_on_tap',
        'top_pick_label': 'Top Pick',
        'top_pick_tagline': 'Best for high credit limits without switching bank',
        'top_pick_features': [
            '1% cashback on all spend',
            'No annual fee (free tier)',
            'Credit limits up to &pound;250,000',
            'No FX fees on overseas spend',
            'Instant virtual card on approval',
            'No business bank account required',
        ],
        'also_consider': [
            {
                'card_id': 'funding_circle_cashback',
                'badge': 'Best Cashback',
                'badge_color': 'gold',
                'tagline': '2% intro cashback, then 1% uncapped',
            },
            {
                'card_id': 'barclaycard',
                'badge': 'Open Access',
                'badge_color': 'pink',
                'tagline': 'No bank account needed, no annual fee',
            },
            {
                'card_id': 'lloyds',
                'badge': 'Lowest APR',
                'badge_color': 'teal',
                'tagline': '15.95% rep. APR for Lloyds BCA holders',
            },
        ],
    },

    # All major cards, ordered: broadest access first, then cashback,
    # then low-APR bank cards, then charge/rewards specialists
    'card_ids': [
        'capital_on_tap', 'barclaycard', 'funding_circle_cashback',
        'moss', 'santander', 'lloyds', 'natwest', 'hsbc',
        'metro_bank', 'amex_business_gold', 'ba_amex_accelerating',
        'amex_business_platinum',
    ],
    'separate_card_ids': [
        'lloyds_charge', 'barclaycard_charge',
        'natwest_business_plus', 'rbs',
    ],

    # Per-card overrides — pillar page positions cards by category fit
    'card_overrides': {
        'capital_on_tap': {
            'fit_label': 'Best for high credit limits without switching banks',
            'verdict': 'The highest credit limits in the UK business card market, no bank account requirement, and no FX fees.',
            'best_for': 'Limited companies needing &pound;25k&ndash;&pound;250k credit without switching bank',
            'watch_out': 'Typical offered rates are much higher than the 13.86% floor. Sole traders excluded.',
            'eligibility': 'UK limited companies and LLPs only. Min &pound;24k turnover.',
        },
        'barclaycard': {
            'fit_label': 'Best card you can get without an existing bank account',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; No bank account required',
            'verdict': 'The only major business credit card that doesn&rsquo;t require an existing business current account. That open access is the reason to choose it.',
            'editorial_heading': 'Open access is genuinely rare in this market &mdash; but 25.5% is the price',
            'best_for': 'Businesses on Starling, Tide, Monzo, or any bank without its own credit card product',
            'watch_out': '25.5% is the highest representative APR among traditional bank cards on this list',
            'not_ideal': 'You already bank with Lloyds, HSBC, NatWest, or Santander and could get a lower rate',
            'eligibility': 'Sole traders, partnerships, LTDs. &pound;10k&ndash;&pound;6.5m turnover. No existing account required.',
        },
        'funding_circle_cashback': {
            'fit_label': 'Fintech cashback without the bank-account barrier',
            'summary_strip': '34.9% rep. APR &middot; 2% cashback (first 6 months), then 1% uncapped &middot; No existing account required',
            'verdict': 'A cashback card from a fintech lender. 2% for the first 6 months then 1% uncapped after that. No bank account requirement but limited companies only.',
            'editorial_heading': 'Fintech cashback without a bank switch &mdash; but limited companies only',
            'best_for': 'Limited companies wanting cashback without needing a specific bank account',
            'watch_out': '34.9% representative APR is significantly higher than the traditional bank cards. Limited companies only, minimum 1 year trading and &pound;30k turnover.',
            'not_ideal': 'You&rsquo;re a sole trader (excluded) or you carry a balance regularly (APR is high)',
            'eligibility': 'UK limited companies only. Min 1 year trading, &pound;30k+ turnover. fundingcircle.com.',
        },
        'moss': {
            'fit_label': 'Best for multi-card spend management',
            'summary_strip': '34.3% rep. APR &middot; Up to 1% cashback &middot; Multiple employee cards &middot; Spend controls built in',
            'verdict': 'Designed for teams that need multiple cards with per-card spend limits and real-time tracking. Less a credit card, more a spend management platform with credit built in.',
            'editorial_heading': 'Spend management first, credit card second &mdash; that&rsquo;s the real positioning',
            'best_for': 'Growing businesses issuing 5+ employee cards who need granular spend controls',
            'watch_out': '34.3% representative APR. Pricing is via platform subscription, not just card fees. Check getmoss.com for current plans.',
            'not_ideal': 'You need a single card with the lowest possible APR, or you&rsquo;re a sole trader',
            'eligibility': 'UK limited companies and LLPs. Check getmoss.com for full eligibility.',
        },
        'santander': {
            'fit_label': 'Best fee structure for multi-cardholder teams',
            'summary_strip': '23.7% APR &middot; 1% cashback &middot; &pound;30 flat fee covers all cardholders',
            'verdict': 'The flat per-account fee structure means the more employee cards you issue, the better the deal. Most competitors charge per cardholder.',
            'editorial_heading': 'The fee advantage is real for teams &mdash; one flat fee regardless of how many cards you issue',
            'best_for': 'Santander business customers issuing 3+ employee cards',
            'watch_out': 'Restricted to Santander 1|2|3 BCA holders. Personal guarantees required.',
            'not_ideal': 'You don&rsquo;t bank with Santander and won&rsquo;t switch',
            'eligibility': 'Santander business current account required. Max 2 directors/partners. &pound;500&ndash;&pound;25k limits.',
        },
        'lloyds': {
            'fit_label': 'Lowest representative APR on the market',
            'summary_strip': '15.95% APR &middot; 14.9% purchase rate &middot; &pound;32 fee waived at &pound;6k+ spend',
            'verdict': 'The lowest representative APR available in the UK business credit card market. But only accessible to existing Lloyds business customers.',
            'editorial_heading': 'The lowest rate available, if you&rsquo;re already banking with Lloyds',
            'best_for': 'Existing Lloyds customers who carry a balance and can hit the fee waiver threshold',
            'watch_out': '&pound;32 annual fee per card. Only waived at &pound;6k+ annual spend per card.',
            'not_ideal': 'You don&rsquo;t bank with Lloyds and would need to switch just for the rate',
            'eligibility': 'Sole traders, partnerships, company directors. Lloyds BCA required.',
        },
        'natwest': {
            'fit_label': 'Best for businesses that spend overseas',
            'summary_strip': '24.3% APR &middot; No FX fee on overseas purchases &middot; &pound;30/card fee waivable',
            'verdict': 'The standout feature is zero foreign exchange fees on overseas card purchases. No other traditional bank card on this list offers that.',
            'editorial_heading': 'No FX fee is a genuine differentiator if your business spends internationally',
            'best_for': 'NatWest business customers with regular overseas card spend',
            'watch_out': '&pound;30 per-cardholder fee stacks up for teams unless each cardholder hits &pound;6k+ spend',
            'not_ideal': 'You don&rsquo;t spend overseas, or you don&rsquo;t bank with NatWest',
            'eligibility': 'Turnover under &pound;2m. NatWest BCA required.',
        },
        'hsbc': {
            'fit_label': 'Worth it if you already bank with HSBC',
            'summary_strip': '22% APR &middot; 15.9% purchase rate &middot; &pound;32 fee waived year 1',
            'verdict': 'Competitive purchase rate, but the annual fee is not waivable after year one. Not worth switching banks for.',
            'editorial_heading': 'Low purchase rate for HSBC customers &mdash; but the fee sticks after year one',
            'best_for': 'Existing HSBC business customers who want a low purchase rate',
            'watch_out': '&pound;32 fee is not waivable after year 1. FX fee is 2.99%.',
            'not_ideal': 'You don&rsquo;t bank with HSBC',
            'eligibility': 'HSBC business current account required.',
        },
        'metro_bank': {
            'fit_label': 'No-fee card at a competitive rate',
            'summary_strip': '18.9% APR &middot; No annual fee &middot; Branch application only',
            'verdict': 'No annual fee at all, and a competitive APR. The catch: you must apply in a Metro Bank branch.',
            'editorial_heading': 'The simplest cost structure, but the branch-only requirement is a real filter',
            'best_for': 'Low-spend businesses near a Metro Bank branch that carry a balance',
            'watch_out': 'In-branch application only. Metro Bank&rsquo;s branch network is London-centric.',
            'not_ideal': 'You&rsquo;re not near a Metro Bank branch, or you need to apply online',
            'eligibility': 'Metro Bank BCA required. Must apply in branch.',
        },
        'amex_business_gold': {
            'fit_label': 'Best rewards programme for high-spend businesses',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Charge card (pay monthly)',
            'verdict': 'The most flexible rewards programme in the UK business card market. Charge card structure means no revolving debt.',
            'editorial_heading': 'Flexible rewards with Avios and hotel transfers, but it&rsquo;s a charge card &mdash; you pay the full balance every month',
            'best_for': 'Businesses spending &pound;5k+/month that can clear the balance monthly and want flexible rewards',
            'watch_out': 'Annual fee is significant. Amex acceptance is not universal in the UK.',
            'not_ideal': 'You need to carry a balance, or your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'ba_amex_accelerating': {
            'fit_label': 'Best for earning Avios on business spend',
            'summary_strip': '&pound;250/year &middot; 1.5 Avios per &pound;1 (3 on BA) &middot; Travel perks',
            'verdict': 'Purpose-built for Avios earning. If your business travel is on BA, this card converts everyday spend into flights.',
            'editorial_heading': 'The direct route to Avios &mdash; if BA is your airline and Amex is accepted by your suppliers',
            'best_for': 'Businesses with frequent BA travel that want to earn Avios on all card spend',
            'watch_out': 'Amex acceptance gaps in the UK. Annual fee needs enough spend to justify.',
            'not_ideal': 'You don&rsquo;t fly BA, or your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'amex_business_platinum': {
            'fit_label': 'Premium charge card with travel perks',
            'summary_strip': '&pound;650/year &middot; Centurion lounge access &middot; Charge card',
            'verdict': 'The premium tier of Amex business cards. Lounge access, travel insurance, and the highest reward earn rate &mdash; at a premium price.',
            'editorial_heading': 'The perks are genuine, but the annual fee means this only works at high spend volumes',
            'best_for': 'High-spend businesses (&pound;10k+/month) that travel frequently and value lounge access',
            'watch_out': 'Highest annual fee of any UK business card. Only viable at scale.',
            'not_ideal': 'Your monthly spend is under &pound;5k, or you rarely travel internationally',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'lloyds_charge': {
            'fit_label': 'Charge card alternative to the Lloyds credit card',
            'summary_strip': '&pound;32/card (free yr 1, waived at &pound;6k+) &middot; Up to 56 days interest-free &middot; Full balance by DD monthly',
            'verdict': 'The Lloyds charge card enforces full monthly repayment by direct debit. That removes the temptation to carry a balance but also removes the safety net of revolving credit. No rewards, no cashback &mdash; the benefit is forced spend discipline and up to 56 days of interest-free float.',
            'editorial_heading': 'Forced discipline: you clear the full balance every month, no exceptions',
            'best_for': 'Lloyds business customers who want to use 56-day float without any risk of accumulating debt',
            'watch_out': '&pound;32/card annual fee applies after year one unless you hit &pound;6k+ spend per card. Full balance collected by direct debit &mdash; ensure your account can cover it.',
            'not_ideal': 'You need the flexibility to spread payments across months, or your cash flow is unpredictable',
            'eligibility': 'Sole traders, partnerships, limited companies. Lloyds business current account required.',
        },
        'barclaycard_charge': {
            'fit_label': 'Charge card with no bank account requirement',
            'summary_strip': '&pound;42/account &middot; Pay in full monthly &middot; No existing bank account needed',
            'verdict': 'The only charge card on this list that does not require an existing business current account. That makes it accessible to businesses on any bank. The trade-off is a &pound;42 annual fee with no waiver route and no rewards programme.',
            'editorial_heading': 'Open access charge card &mdash; rare, but the &pound;42 fee has no waiver',
            'best_for': 'Businesses that want charge card discipline without switching to a specific bank',
            'watch_out': '&pound;42 annual fee per account with no spend-based waiver. 2.99% FX fee on non-sterling transactions. Cash fee 3% (min &pound;3).',
            'not_ideal': 'You want rewards or cashback, or you need to carry a balance across months',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. No existing bank account required.',
        },
        'natwest_business_plus': {
            'fit_label': 'NatWest&rsquo;s premium card with tiered cashback and no FX fees',
            'summary_strip': '29% APR &middot; &pound;70/cardholder &middot; 0.5%&ndash;3% tiered cashback (capped &pound;600/yr) &middot; No FX fee',
            'verdict': 'A step up from the standard NatWest card: tiered cashback (3% on fuel and EV charging, 2% on trade supplies, 1% on travel, 0.5% on everything else) and no foreign transaction charges. But the &pound;70-per-cardholder fee and 29% APR mean the cashback needs to offset real costs.',
            'editorial_heading': 'Tiered cashback and no FX fees, but the &pound;70 fee and 29% APR change the maths',
            'best_for': 'NatWest business customers spending &pound;2k+/month who can earn enough cashback to offset the &pound;70 fee',
            'watch_out': '&pound;70 annual fee per cardholder &mdash; not per account. Cashback capped at &pound;600/year. 29% APR if you carry a balance.',
            'not_ideal': 'Low-spend businesses where the &pound;70 fee exceeds the cashback return, or you don&rsquo;t bank with NatWest',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. NatWest business account required.',
        },
        'rbs': {
            'fit_label': 'RBS mirror of NatWest Business Plus',
            'summary_strip': '29% APR &middot; &pound;70/cardholder &middot; 0.5%&ndash;3% tiered cashback (capped &pound;600/yr) &middot; No FX fee',
            'verdict': 'Identical product to NatWest Business Plus but for RBS customers. Same tiered cashback structure, same fee, same APR. If you bank with RBS, this is the equivalent card.',
            'editorial_heading': 'Same product as NatWest Business Plus &mdash; for RBS customers',
            'best_for': 'RBS business customers spending &pound;2k+/month who want tiered cashback and no FX fees',
            'watch_out': '&pound;70 annual fee per cardholder. Cashback capped at &pound;600/year. 29% APR if you carry a balance.',
            'not_ideal': 'You don&rsquo;t bank with RBS, or your monthly spend is too low for the cashback to cover the &pound;70 fee',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. RBS business account required.',
        },
    },

    # Page sections in display order
    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        # Verdict box — decision tension first
        {'type': 'verdict_box',
         'text': 'There is no single best business credit card. The right choice depends on three things: whether you need to carry a balance (APR matters), whether you clear monthly (rewards matter), and whether your bank offers a card at all (access matters). Most cards on this list require an existing business current account with that bank. If you bank with Starling, Tide, or Monzo, your options narrow to three.'},

        # Hero zone — top pick card + trust strip + also consider
        {'type': 'hero_zone'},

        # Intro — reach decision tension by paragraph 2
        {'type': 'prose', 'paragraphs': [
            'We reviewed every major UK business credit card available in March 2026, verified rates and fees against each provider&rsquo;s pricing page, and ranked them by the decision that actually matters to you: what you need the card to do.',
            'The UK business credit card market splits into three lanes. Traditional bank cards (Lloyds, HSBC, NatWest, Santander, Metro Bank) offer the lowest APRs but require you to bank with them. Fintech cards (Capital on Tap, Moss, Funding Circle) offer higher limits and faster decisions but at higher rates. And Amex cards offer the best rewards and travel perks but with acceptance gaps across UK suppliers.',
            'This page covers all three. Each card is positioned by what it&rsquo;s actually best for, not by a generic star rating. The difference between the cheapest and most expensive card on this list is over 10 percentage points of APR &mdash; and you may not be able to access either.',
            'We update this page monthly. If a rate changes, we catch it. If a card disappears or a new one launches, you&rsquo;ll see it here first. The data below was verified on 20 March 2026.',
        ]},

        {'type': 'toc_start'},

        {'type': 'heading', 'level': 2, 'text': 'Compare the Best Business Credit Cards at a Glance'},
        {'type': 'prose', 'paragraphs': [
            'Not every business can choose from the full market. Some of the lowest-rate cards are only available to existing business current account customers, so your realistic shortlist may be much narrower than a generic &ldquo;best business credit cards&rdquo; table suggests. That matters because the gap between a lower-rate bank card and a more widely available rewards card can be the difference between manageable borrowing and expensive borrowing if you carry a balance.',
            'This table includes all 12 cards so you can see both the headline deals and the eligibility constraints behind them. It also highlights a detail many comparison pages blur: Amex Business Gold and Platinum are charge cards first, but Pay Over Time at 29.1% variable APR means they can now work more like hybrid charge-and-credit products for eligible spending. If you still think Amex charge cards always mean paying everything off in full every month, that is no longer the whole picture.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'capital_on_tap': {'text': 'Top Pick', 'color': 'top'},
                'funding_circle_cashback': {'text': 'Best Cashback', 'color': 'gold'},
                'barclaycard': {'text': 'Open Access', 'color': 'pink'},
                'lloyds': {'text': 'Lowest APR', 'color': 'teal'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': (
                'Rates verified against provider pricing pages, 20 March 2026. '
                'All variable rates may change after publication.'
            ),
        }},

        # Quick-decision table
        {'type': 'heading', 'level': 2, 'text': 'Which Type of Business Credit Card Do You Need?'},
        {'type': 'prose', 'paragraphs': [
            'Before you compare individual cards, narrow the field. Most businesses fall into one of these seven situations, and each one points you to a different shortlist. If you try to compare all twelve cards at once, you&rsquo;ll waste time on options you can&rsquo;t access or don&rsquo;t need.',
            'This table comes from the questions readers actually ask. The most common one, by far, is some version of &ldquo;I bank with [X], what are my options?&rdquo; That&rsquo;s why the bank account filter matters more than any feature comparison.',
            'One caveat the table can&rsquo;t show: if you choose Amex for rewards or Avios, around 40% of UK merchants still do not accept American Express (source: Amex published acceptance data). That means you will likely need a second Visa or Mastercard for suppliers who don&rsquo;t take it. Factor that into the rewards calculation.',
        ]},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Your priority</th><th>Look at</th><th>Skip to</th></tr></thead>'
            '<tbody>'
            '<tr><td>Lowest ongoing borrowing cost</td><td>Low-APR bank cards</td><td><a href="/business-credit-cards/low-apr-business-credit-cards/">Low APR cards</a></td></tr>'
            '<tr><td>Earn cashback or rewards on spend</td><td>Amex or cashback cards</td><td><a href="/business-credit-cards/best-cashback-and-reward/">Cashback &amp; rewards</a></td></tr>'
            '<tr><td>High credit limit (&pound;25k+)</td><td>Capital on Tap or Amex Platinum</td><td>Cards 1 and 12 below</td></tr>'
            '<tr><td>Don&rsquo;t have a traditional bank account</td><td>Barclaycard, Capital on Tap, or Moss</td><td>Cards 2, 1, and 4 below</td></tr>'
            '<tr><td>Multiple employee cards with controls</td><td>Moss or Santander</td><td>Cards 4 and 5 below</td></tr>'
            '<tr><td>Earn Avios for business travel</td><td>BA Amex Accelerating</td><td><a href="/business-credit-cards/best-cards-with-air-miles-avios/">Air miles &amp; Avios</a></td></tr>'
            '<tr><td>Pay in full monthly (charge card)</td><td>Amex Gold or Lloyds Charge</td><td><a href="/business-credit-cards/best-business-charge-cards/">Charge cards</a></td></tr>'
            '</tbody></table>'},

        # ========================================================
        # NEW SECTION: How Much Does a Business Credit Card Cost?
        # ========================================================
        {'type': 'heading', 'level': 2, 'text': 'How Much Does a Business Credit Card Actually Cost?'},

        {'type': 'prose', 'paragraphs': [
            'The advertised APR is only part of the cost. When the real annual cost of each card is calculated across different spending levels, the results surprised us. A &ldquo;free&rdquo; card can cost you more than a card with a &pound;195 annual fee, depending on how you use it.',
            'Here&rsquo;s the maths. If you spend &pound;3,000 a month and clear the balance in full every month, your APR is irrelevant. You pay zero interest. In that scenario, a no-fee card like Barclaycard costs you nothing, while an Amex Business Gold card costs &pound;195 per year but earns you roughly &pound;360 in Membership Rewards points. The Amex is cheaper in net terms, even with the fee.',
            'Now change the scenario. If you carry &pound;5,000 of revolving debt, the APR is everything. At Lloyds&rsquo; 14.9% purchase rate, you&rsquo;d pay roughly &pound;745 a year in interest. At Barclaycard&rsquo;s 25.5%, that same &pound;5,000 balance costs you &pound;1,275 a year. At Capital on Tap&rsquo;s average offered rate of 46.05%, you&rsquo;re looking at &pound;2,303. The difference between the cheapest and most expensive option is &pound;1,558 a year on the same balance.',
            'How common is carrying a balance? More than you might expect. Around 84% of micro-businesses clear their card in full each month, but that average hides sharp sector differences. In construction, only 35% clear monthly &mdash; the rest carry a balance across billing cycles, often because project payment terms are 30&ndash;60 days. If your business falls into a sector with lumpy cash flow, the APR is not a theoretical number. It is real money out of your account every month.',
            'Foreign exchange fees add another layer. If your business spends &pound;1,000 a month overseas, an HSBC card at 2.99% FX charges you &pound;359 a year in fees alone. NatWest and Capital on Tap charge zero FX fees on purchases. For a business with regular overseas spend, the FX saving on NatWest could outweigh a lower APR elsewhere.',
        ]},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Scenario</th><th>Lowest cost card</th><th>Annual cost</th><th>Highest cost card</th><th>Annual cost</th></tr></thead>'
            '<tbody>'
            '<tr><td>Clear &pound;3k/month in full, no overseas spend</td><td>Barclaycard (no fee)</td><td>&pound;0</td><td>Amex Platinum (&pound;650 fee)</td><td>&pound;650</td></tr>'
            '<tr><td>Carry &pound;5k balance, no overseas spend</td><td>Lloyds (14.9% purchase rate)</td><td>&pound;777*</td><td>Capital on Tap (avg 46.05%)</td><td>&pound;2,303</td></tr>'
            '<tr><td>Clear monthly, &pound;1k/month overseas</td><td>NatWest (0% FX)</td><td>&pound;30 fee</td><td>HSBC (2.99% FX)</td><td>&pound;391</td></tr>'
            '<tr><td>Clear &pound;6k/month, want rewards</td><td>Amex Gold (net of rewards)</td><td>Earns ~&pound;525</td><td>No-reward card</td><td>&pound;0 earned</td></tr>'
            '</tbody></table>'},
        {'type': 'prose', 'paragraphs': [
            '<em>*Lloyds cost includes &pound;32 annual fee (waived at &pound;6k+ annual spend). Interest calculated on &pound;5,000 at 14.9% purchase rate.</em>',
            'The point is this: you can&rsquo;t compare business credit cards on APR alone. Your total cost depends on whether you carry a balance, how much you spend overseas, and whether you earn enough rewards to offset an annual fee. We&rsquo;ve factored all three into the card rankings below.',
        ]},

        # ========================================================
        # EXPANDED: The bank account barrier
        # ========================================================
        {'type': 'heading', 'level': 2, 'text': 'The Bank Account Barrier: Why Most Cards Are Off-Limits'},

        {'type': 'prose', 'paragraphs': [
            'Seven of the twelve cards on this page require an existing business current account with that bank. That&rsquo;s not a footnote. It&rsquo;s the single most important filter in the UK business credit card market, and most comparison sites bury it.',
            'Here is how it breaks down. Lloyds, HSBC, NatWest, Santander, and Metro Bank all require you to hold a business current account with them before you can apply for their credit card. That means if you bank with Starling, Tide, Monzo, or any challenger bank, five of the cheapest options on this page are invisible to you.',
            'We checked every provider&rsquo;s eligibility page in March 2026. The cards you can get without switching your business bank account are: Barclaycard Select Cashback, Capital on Tap, Moss, Funding Circle, and the three Amex cards. That&rsquo;s five credit cards and three charge cards. Everything else requires a specific banking relationship.',
            'The cost gap is real. If you bank with a challenger like Tide or Starling, the cheapest revolving credit available without switching is Barclaycard at 25.5% &mdash; nearly 10 percentage points above Lloyds at 15.95%. On a &pound;5,000 carried balance, that difference costs roughly &pound;40 a month in extra interest. Switching business bank accounts takes 2&ndash;4 weeks and assumes a clean credit history, so it is not a quick workaround.',
        ]},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Card</th><th>Bank account required?</th><th>Which bank?</th></tr></thead>'
            '<tbody>'
            '<tr><td>Capital on Tap</td><td>No</td><td>Any</td></tr>'
            '<tr><td>Barclaycard Select Cashback</td><td>No</td><td>Any</td></tr>'
            '<tr><td>Funding Circle</td><td>No</td><td>Any</td></tr>'
            '<tr><td>Moss</td><td>No</td><td>Any</td></tr>'
            '<tr><td>Amex Business Gold / BA Amex / Platinum</td><td>No</td><td>Any</td></tr>'
            '<tr><td>Lloyds</td><td>Yes</td><td>Lloyds BCA</td></tr>'
            '<tr><td>HSBC</td><td>Yes</td><td>HSBC BCA</td></tr>'
            '<tr><td>NatWest</td><td>Yes</td><td>NatWest BCA</td></tr>'
            '<tr><td>Santander</td><td>Yes</td><td>Santander 1|2|3 BCA</td></tr>'
            '<tr><td>Metro Bank</td><td>Yes</td><td>Metro Bank BCA</td></tr>'
            '</tbody></table>'},
        {'type': 'prose', 'paragraphs': [
            'If you already bank with one of the big five, you should check their card first. You&rsquo;ll almost certainly get a lower APR than the open-access alternatives. If you don&rsquo;t, skip straight to the open-access cards section and save yourself the comparison.',
            'This filter leads the page because there&rsquo;s no point comparing twelve cards if you can only access four. Most readers land on this page not knowing that the bank account requirement exists at all.',
        ]},

        # ========================================================
        # NEW SECTION: Credit Limits
        # ========================================================
        {'type': 'heading', 'level': 2, 'text': 'Business Credit Card Limits: What You Can Actually Get'},

        {'type': 'prose', 'paragraphs': [
            'The credit limit ranges advertised by providers are wide enough to be almost meaningless. Capital on Tap says &ldquo;up to &pound;250,000.&rdquo; Most traditional banks say &ldquo;&pound;500 to &pound;25,000.&rdquo; What you&rsquo;ll actually be offered depends on your turnover, trading history, credit profile, and the provider&rsquo;s own risk appetite.',
            'Here is what we know from the published data. Traditional bank cards (Lloyds, HSBC, NatWest, Santander) typically cap at &pound;25,000 per card. Santander&rsquo;s published range is &pound;500 to &pound;25,000. Metro Bank is similar. For a limited company with &pound;200k turnover and clean credit, you might expect a limit in the &pound;5,000 to &pound;15,000 range from a traditional bank. A sole trader with &pound;50k turnover is more likely to see &pound;1,000 to &pound;5,000.',
            'Capital on Tap is the outlier. Their published ceiling is &pound;250,000, and they explicitly market to businesses that need facilities above the &pound;25k bank card ceiling. But the minimum turnover requirement is &pound;24,000, and the limit you&rsquo;re offered is algorithmically determined. We&rsquo;ve seen reports of businesses being offered &pound;5,000 initially and then having limits raised over time as they build a spending history.',
            'Amex charge cards don&rsquo;t have a pre-set spending limit. That sounds unlimited, but it isn&rsquo;t. Amex sets a practical ceiling based on your spending history, payment reliability, and account standing. If you try to make a purchase significantly above your normal pattern, it may be declined. Think of it as an adaptive limit rather than no limit.',
            'The practical question for you is: how much credit do you actually need? If you need more than &pound;25,000 in revolving credit, your options are Capital on Tap or a commercial credit facility from your bank (which is a different product entirely). If you need &pound;5,000&ndash;&pound;15,000, most cards on this list can accommodate that. If you need less than &pound;5,000, almost any card will do, and your decision should be driven by APR and fees, not limits.',
        ]},

        # ========================================================
        # NEW SECTION: Applying
        # ========================================================
        {'type': 'heading', 'level': 2, 'text': 'Applying: What Happens and What to Expect'},

        {'type': 'prose', 'paragraphs': [
            'Every business credit card application involves a credit check. For most providers, this is a hard search on both your personal credit file and your business credit file (if you have one). That hard search leaves a mark that other lenders can see for 12 months. If you apply for three cards in quick succession, each subsequent lender sees the previous searches, and that can reduce your chances of approval.',
            'The exceptions are eligibility checkers. Capital on Tap, Funding Circle, and some Amex products offer soft-search pre-checks that tell you whether you&rsquo;re likely to be approved before you formally apply. We recommend using these wherever available. A soft search does not affect your credit file.',
            'Timing matters. If you&rsquo;ve recently moved house, changed your business address, taken out other credit, or missed payments, your approval odds drop. Lenders want stability. A business that has been trading for two or more years, at the same address, with clean credit, will get better rates and higher limits than a business that incorporated six months ago.',
            'For sole traders, the application is assessed almost entirely on your personal credit history. There are approximately 4.1 million sole traders in the UK, making them the largest business demographic by number &mdash; yet they have the fewest credit card options. Capital on Tap and Funding Circle both exclude sole traders entirely. That leaves Barclaycard, the traditional bank cards (if you hold the right account), and Amex as the realistic choices. For limited companies, providers check both the director&rsquo;s personal credit and the company&rsquo;s credit file at Companies House. Most cards require you to provide a personal guarantee, which means you&rsquo;re personally liable for the balance if the business can&rsquo;t pay.',
            'How long does it take? Capital on Tap and Moss can give you an instant decision online, with a virtual card issued immediately on approval. Traditional bank cards take longer. Lloyds and HSBC typically take 5&ndash;10 working days from application to card delivery. Metro Bank requires an in-branch appointment, which adds scheduling time. Amex is usually 2&ndash;5 working days for a decision, with the card arriving a few days later.',
        ]},

        # Section divider + main card list
        {'type': 'divider', 'label': 'Detailed card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Every Business Credit Card, Reviewed'},
        {'type': 'prose', 'paragraphs': [
            'Cards are ordered by category: open-access cards first (no bank account needed), then bank-locked cards by APR, then charge cards and rewards specialists. Each card includes verified rates, our editorial assessment, and the specific scenario where it makes sense.',
            'We&rsquo;ve spent time on each of these cards, not just reading the product pages but calculating real costs, checking eligibility requirements, and comparing the numbers. Where we found a gap between what&rsquo;s advertised and what you&rsquo;re likely to get, we&rsquo;ve called it out. One example: Capital on Tap advertises rates &ldquo;from 9.9%&rdquo; but their own published credit agreement data shows the average offered rate across all customers is 46.05% (Q4 2025). The gap between the headline and the reality is the single biggest pricing transparency problem in UK business credit cards.',
        ]},
        {'type': 'card_list'},

        # Charge cards and alternatives section
        {'type': 'heading', 'level': 2, 'text': 'Also Worth Knowing: Charge Cards and Niche Options'},
        {'type': 'prose', 'paragraphs': [
            'These cards don&rsquo;t fit the main ranking because they&rsquo;re either charge cards (no revolving credit), niche products, or regional variants. They&rsquo;re listed separately for completeness.',
            'If you always clear your balance in full, a charge card removes the temptation to revolve. That discipline is worth something. But if you occasionally need to spread a large purchase over two or three months, a charge card will not give you that flexibility. You pay the full balance every month, no exceptions.',
            'The risk most charge card guides skip: late payment consequences are immediate and severe. On Amex Business Gold and Platinum, a missed payment triggers a &pound;12 fee. Miss a second payment within 60 days and Amex can suspend your account entirely. Reinstatement costs &pound;95 and is not guaranteed (source: americanexpress.com, account terms). That is a sharper penalty than most credit cards impose, where a missed payment adds interest but does not shut down the account.',
        ]},
        {'type': 'card_list_separate'},

        # How We Ranked These Cards
        {'type': 'heading', 'level': 2, 'text': 'How We Ranked These Business Credit Cards'},
        {'type': 'prose', 'paragraphs': [
            'We did not use a single scoring system. A card with a low APR is not &ldquo;better&rdquo; than a card with high cashback. They serve different needs, and pretending otherwise is how most comparison sites mislead you.',
        ]},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><strong>Open access cards</strong> come first because most readers can&rsquo;t access the bank-locked options</li>\n'
            '    <li><strong>Bank-locked cards</strong> are ranked by APR within their group, since carrying cost is the primary differentiator</li>\n'
            '    <li><strong>Rewards and charge cards</strong> are listed separately because APR ranking doesn&rsquo;t apply to them</li>\n'
            '</ul>'},
        {'type': 'prose', 'paragraphs': [
            'This is an editorial ranking, not a mathematically weighted score. We prioritised access, then cost, then features because a card you can&rsquo;t get is not a card you should be comparing.',
            'If you bank with a challenger like Tide or Starling, the seven bank-locked cards on this page are invisible to you. Your revolving credit options narrow to Barclaycard at 25.5% representative APR, Capital on Tap (variable, based on your risk profile &mdash; the Oct&ndash;Dec 2025 average across their book was 46.05%), or Funding Circle at 34.9% if you are a limited company. Sole traders lose Capital on Tap and Funding Circle entirely, leaving Barclaycard and the Amex range as the only options. That access filter shaped this ranking more than any rate comparison.',
            'Another example: a consultancy spending &pound;6,000 a month on their Amex Business Gold, clearing the balance monthly. For that business, APR is irrelevant. What matters is the value of Membership Rewards points earned versus the &pound;195 annual fee. At 1 point per pound and a conservative 0.5p per point valuation, they&rsquo;re earning roughly &pound;360 a year in rewards against a &pound;195 fee. The card pays for itself, but only because they clear the balance and spend enough volume.',
        ]},

        # ========================================================
        # FAQ accordion with structured data
        # ========================================================
        {'type': 'heading', 'level': 2, 'text': 'Business Credit Card FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'Can I get a business credit card as a sole trader?',
                'a': 'Yes, but your options are more limited than for limited companies. Barclaycard, Lloyds, HSBC, NatWest, Santander, Metro Bank, and all three Amex cards explicitly accept sole traders. Capital on Tap does not &mdash; it requires Companies House registration, which rules out sole traders entirely. Funding Circle also requires a limited company. See our dedicated page: <a href="/business-credit-cards/best-business-credit-cards-for-sole-traders/">best business credit cards for sole traders</a>.',
            },
            {
                'q': 'Do I need a business bank account to get a business credit card?',
                'a': 'For most traditional bank cards, yes. Five of the six bank-issued cards on this list require a business current account with that bank. The exceptions are Barclaycard (no account required), all fintech cards (Capital on Tap, Moss, Funding Circle), and all Amex cards. If you bank with Starling, Tide, or Monzo, your options are the open-access cards listed above.',
            },
            {
                'q': 'What credit limit can I get on a business credit card?',
                'a': 'Traditional bank cards typically offer &pound;500&ndash;&pound;25,000. Capital on Tap offers up to &pound;250,000 for qualifying businesses. Amex charge cards don&rsquo;t have a pre-set spending limit. The limit you&rsquo;re offered depends on turnover, trading history, and the provider&rsquo;s credit assessment.',
            },
            {
                'q': 'Should I get a credit card or a charge card?',
                'a': 'If you need to spread payments over time, you need a credit card. If you can always clear the balance monthly and want rewards, a charge card avoids the temptation of revolving debt. We cover this in detail: <a href="/business-credit-cards/business-credit-cards-vs-charge-cards/">business credit cards vs charge cards</a>.',
            },
            {
                'q': 'How long does it take to get a business credit card?',
                'a': 'Capital on Tap and Moss can give you an instant decision with a virtual card issued immediately. Traditional bank cards take 5&ndash;10 working days. Amex is typically 2&ndash;5 working days for a decision. If speed matters, fintech providers are your best option.',
            },
            {
                'q': 'Can I use a personal credit card for business expenses?',
                'a': 'Technically, yes. But mixing personal and business spending complicates bookkeeping. If you&rsquo;re a limited company, HMRC expects clear separation. A dedicated business card also builds your business credit history. Below &pound;500/month in business expenses, a personal card is workable short-term.',
            },
            {
                'q': 'Does Section 75 protection apply to business credit cards?',
                'a': 'No. Section 75 of the Consumer Credit Act applies to personal credit cards only. Business credit cards are excluded. If a supplier fails to deliver or goes bust, your recourse is through Visa or Mastercard chargeback schemes, not statutory Section 75 protection. Chargeback is a voluntary scheme run by the card network, not a legal right, and the time limits and success rates differ. This is a meaningful gap in protection that most comparison sites do not flag.',
            },
            {
                'q': 'What credit score do I need for a business credit card?',
                'a': 'No UK provider publishes a minimum threshold. Factors that help: being on the electoral roll, no missed payments in the last 12 months, low credit utilisation, and 12+ months&rsquo; trading history. If your credit is poor, see our page on <a href="/business-credit-cards/poor-credit/">business credit cards for poor credit</a>.',
            },
        ]},

        # Internal links hub
        {'type': 'heading', 'level': 2, 'text': 'Explore Business Credit Cards by Category'},
        {'type': 'prose', 'paragraphs': [
            'Each category page goes deeper on a specific type of card. If you already know what you need, these pages will get you there faster than reading every review on this page.',
        ]},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/low-apr-business-credit-cards/">Best low APR business credit cards</a> &mdash; if carrying a balance, start here</li>\n'
            '    <li><a href="/business-credit-cards/best-cashback-and-reward/">Best cashback and reward cards</a> &mdash; if you clear monthly and want to earn</li>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards-for-sole-traders/">Best cards for sole traders</a> &mdash; filtered for sole trader eligibility</li>\n'
            '    <li><a href="/business-credit-cards/best-credit-cards-for-start-ups/">Best cards for start-ups</a> &mdash; newer businesses with limited trading history</li>\n'
            '    <li><a href="/business-credit-cards/the-best-interest-free-credit-cards/">Best interest-free cards</a> &mdash; 0% intro offers and balance transfers</li>\n'
            '    <li><a href="/business-credit-cards/what-are-the-best-business-credit-cards-for-travel/">Best cards for travel</a> &mdash; FX fees, insurance, and travel perks</li>\n'
            '    <li><a href="/business-credit-cards/best-cards-with-air-miles-avios/">Best cards for Avios and air miles</a> &mdash; BA Avios earning compared</li>\n'
            '    <li><a href="/business-credit-cards/instant-approval-business-credit-cards/">Instant approval cards</a> &mdash; if you need a card this week</li>\n'
            '    <li><a href="/business-credit-cards/best-business-charge-cards/">Best charge cards</a> &mdash; pay-in-full cards with rewards</li>\n'
            '    <li><a href="/business-credit-cards/poor-credit/">Cards for poor credit</a> &mdash; options with CCJs or missed payments</li>\n'
            '</ul>'},

        # Reviews and comparisons
        {'type': 'heading', 'level': 2, 'text': 'Individual Card Reviews and Brand Comparisons'},
        {'type': 'prose', 'paragraphs': [
            'If you&rsquo;ve narrowed your choice to one or two cards, our individual reviews go deeper on pricing, features, and real-world fit.',
        ]},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/capital-on-tap-review/">Capital on Tap review</a></li>\n'
            '    <li><a href="/business-credit-cards/funding-circle-business-credit-card-review/">Funding Circle credit card review</a></li>\n'
            '    <li><a href="/business-credit-cards/flexipay-review/">FlexiPay review</a></li>\n'
            '    <li><a href="/business-credit-cards/compare-barclaycard-business-credit-cards/">Compare Barclaycard cards</a></li>\n'
            '    <li><a href="/business-credit-cards/compare-american-express-business-credit-cards/">Compare Amex cards</a></li>\n'
            '    <li><a href="/business-credit-cards/capital-on-tap-vs-amex/">Capital on Tap vs Amex</a></li>\n'
            '</ul>'},

        # Guides and explainers
        {'type': 'heading', 'level': 2, 'text': 'Business Credit Card Guides and Explainers'},
        {'type': 'prose', 'paragraphs': [
            'New to business credit cards? Start with our guides.',
        ]},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '    <li><a href="/business-credit-cards/business-credit-cards-vs-charge-cards/">Credit cards vs charge cards explained</a></li>\n'
            '    <li><a href="/business-credit-cards/what-is-a-balance-transfer-credit-card/">What is a balance transfer credit card?</a></li>\n'
            '</ul>'},

        # Methodology and Disclosure
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> All rates, fees, and eligibility criteria were verified against each provider&rsquo;s public pricing page on 20 March 2026. Capital on Tap&rsquo;s average offered rate (46.05%) is sourced from their own credit agreement data published for October&ndash;December 2025. We source product data exclusively from provider websites, regulatory filings (FCA, Companies House), and official industry bodies (UK Finance, Bank of England).',
            '<strong>Rate type:</strong> All rates listed are variable unless stated otherwise. Providers may change them at any time after publication. The cost calculations on this page assume rates as published on our verification date and are illustrative, not guaranteed.',
            '<strong>How we rank:</strong> We do not accept payment for rankings. Cards are ordered by access (open-access first), then by cost within each category. We update this page monthly and re-verify all rates. Our editorial team makes the ranking decisions; affiliate relationships do not influence card positioning.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral or affiliate fees from some of the card providers listed on this page. This does not affect our editorial rankings, which are based on verified rates and publicly available product data.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Credit products are subject to status and provider approval. We recommend comparing offers directly with providers before applying.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
