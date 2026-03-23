"""Page config for: Best Cashback and Reward Business Credit Cards."""

PAGE_CONFIG = {
    'slug': 'best-cashback-and-reward',
    'page_type': 'roundup',
    'wp_page_id': 44068,
    'title': 'Best Cashback and Reward Business Credit Cards in the UK (2026)',
    'meta_description': (
        'Compare UK business credit cards with the best cashback rates and rewards '
        'programmes. Rates verified March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Do You Actually Benefit From a Rewards Card?': [
            'UK Finance data: 84% micro / 94% small businesses clear monthly',
            'Sector variation: only 35% of construction firms clear monthly',
            'Decision table by payment pattern, not card type',
        ],
        'Compare the Cashback and Reward Cards': [
            'All 11 UK business rewards cards in one verified comparison',
        ],
        'Cashback vs Points vs Avios': [
            'MR point value range: 0.45p (statement credit) to 2p (premium cabin)',
            'Avios worked example: 6,000/month on £4k spend = EU return every 2 months',
            'Common mistake named: choosing rewards complexity over flat cashback',
        ],
        'The Real Return: Cashback at Different Spend Levels': [
            'Original table: net cashback at £1k/£3k/£5k/£10k monthly spend',
            'CoT Pro break-even: £29,900 annual spend to cover £299 fee',
            'Single-month balance carry wipes two months of cashback (quantified)',
        ],
        'Every Cashback and Rewards Card': [
            'Card-level reviews with earn rate and fee verified per provider',
        ],
        'Other Reward Cards Worth Knowing About': [
            'Moss and Barclays Premium Plus listed as non-mainstream alternatives',
        ],
        'The Maths: When Rewards Pay Off': [
            'Amex Gold break-even: ~£25k annual spend at good redemption rates',
            'Worked example: same 60k MR points worth £1,200 or £270 by redemption',
            'HMRC BIM40455: cashback is expense reduction, not taxable income',
        ],
        'Cashback and Rewards FAQs': [
            'Tax treatment of business cashback cited to HMRC BIM40455',
            'Clarification: no card earns both cashback and Avios simultaneously',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'capital_on_tap',
        'top_pick_label': 'Top Pick',
        'top_pick_tagline': '1% uncapped cashback on every purchase',
        'top_pick_features': [
            '1% cashback on all spend (Pro card)',
            'No annual fee on free tier',
            'Credit limits up to &pound;250,000',
            'No FX fees or ATM fees',
            'No business bank account required',
        ],
        'also_consider': [
            {
                'card_id': 'funding_circle_cashback',
                'badge': 'Best Intro Rate',
                'badge_color': 'gold',
                'tagline': '2% cashback first 6 months, then 1% uncapped',
            },
            {
                'card_id': 'barclaycard',
                'badge': 'Open Access',
                'badge_color': 'pink',
                'tagline': 'Cashback without a bank account requirement',
            },
            {
                'card_id': 'santander',
                'badge': 'Simple Cashback',
                'badge_color': 'teal',
                'tagline': '1% flat cashback plus no FX fee',
            },
        ],
    },

    'card_ids': [
        'amex_business_gold', 'ba_amex_accelerating', 'amex_business_platinum',
        'amex_business_basic', 'amazon_amex', 'santander', 'barclaycard',
        'capital_on_tap', 'funding_circle_cashback', 'natwest_business_plus', 'rbs',
    ],
    'separate_card_ids': ['moss', 'barclays_premium_plus'],

    'card_overrides': {
        'amex_business_gold': {
            'fit_label': 'Best flexible rewards programme',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Charge card',
            'verdict': 'Membership Rewards points transfer to airlines, hotels, or statement credit. The most flexible rewards programme in the UK business card market.',
            'editorial_heading': 'The most flexible reward points &mdash; transfer to Avios, hotels, or statement credit',
            'best_for': 'High-spend businesses (&pound;3k+/month) that clear monthly and want flexible reward redemption',
            'watch_out': 'Charge card &mdash; full balance due monthly. Amex acceptance is not universal.',
            'not_ideal': 'You need to carry a balance, or most of your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Limited companies and LLPs. No existing account required.',
        },
        'ba_amex_accelerating': {
            'fit_label': 'Best for earning air miles (Avios)',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; 1.5 Avios per &pound;1 &middot; Travel perks',
            'verdict': 'Purpose-built for Avios. The fastest Avios earn rate on any UK business card. If BA is your airline, this is the only card to consider for travel rewards.',
            'editorial_heading': 'The direct route to Avios &mdash; no intermediary points, no transfer friction',
            'best_for': 'Businesses with frequent BA travel who want Avios on every pound of card spend',
            'watch_out': 'Only valuable for BA flyers. Amex acceptance gaps in UK supply chains.',
            'not_ideal': 'You don&rsquo;t fly BA specifically, or you want cashback instead of air miles',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. &pound;250/year. No existing account required.',
        },
        'amex_business_platinum': {
            'fit_label': 'Premium rewards + travel perks',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Centurion lounge access &middot; Highest MR earn rate',
            'verdict': 'The premium tier. Higher earn rate than Gold, plus lounge access and travel insurance. Only makes financial sense at very high spend.',
            'editorial_heading': 'The perks are real, but the annual fee only pays off at scale',
            'best_for': 'Businesses spending &pound;10k+/month that travel frequently',
            'watch_out': 'Highest annual fee. Charge card structure. Amex acceptance.',
            'not_ideal': 'Monthly spend under &pound;5k, or you don&rsquo;t value travel perks',
            'eligibility': 'Limited companies and LLPs. &pound;650/year (supplementary: &pound;295). No existing account required.',
        },
        'amex_business_basic': {
            'fit_label': 'Entry-level Amex rewards',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards &middot; Credit card (revolving)',
            'verdict': 'Lowest-cost entry to Membership Rewards. Unlike the Gold and Platinum, this is a credit card &mdash; you can carry a balance.',
            'editorial_heading': 'Amex rewards without the charge card requirement',
            'best_for': 'Businesses wanting Membership Rewards at a lower annual fee',
            'watch_out': 'Lower earn rate than Gold. Still subject to Amex acceptance gaps.',
            'not_ideal': 'You want the highest earn rate (Gold or Platinum are better)',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. &pound;0 annual fee. No existing account required.',
        },
        'amazon_amex': {
            'fit_label': 'Best for heavy Amazon Business spenders',
            'summary_strip': '2% then 1% cashback &middot; &pound;0 yr 1, then &pound;195/year &middot; Amazon purchases',
            'verdict': 'If you spend heavily on Amazon Business, the cashback rate on Amazon purchases is higher than any other card. Outside Amazon, the earn rate is ordinary.',
            'editorial_heading': 'Niche but potent &mdash; only worth it if Amazon is a major spend category for your business',
            'best_for': 'Businesses spending &pound;1k+/month on Amazon Business',
            'watch_out': 'The premium earn rate only applies to Amazon purchases. General spend earn rate is lower.',
            'not_ideal': 'Your Amazon spend is occasional, not a core business expense',
            'eligibility': 'Amazon Business account required. Sole traders, partnerships, LTDs accepted.',
        },
        'santander': {
            'fit_label': 'Straightforward 1% cashback',
            'summary_strip': '23.7% APR &middot; 1% cashback on all spend &middot; &pound;30/account',
            'verdict': 'Flat 1% cashback on all purchases. No tiers, no categories, no caps. Simple. The flat per-account fee also benefits multi-card teams.',
            'editorial_heading': '1% cashback with no complexity &mdash; but only for Santander customers',
            'best_for': 'Santander customers who want simple, uncapped cashback without tracking categories',
            'watch_out': 'Santander BCA required. 1% is competitive but not market-leading.',
            'not_ideal': 'You don&rsquo;t bank with Santander, or you want higher rates for specific categories',
            'eligibility': 'Santander BCA required.',
        },
        'barclaycard': {
            'fit_label': 'Cashback without a bank account requirement',
            'summary_strip': '25.5% APR &middot; Up to 1% cashback &middot; No bank account required',
            'verdict': 'The only cashback card you can get without switching your bank. Cashback is tiered based on monthly spend volume.',
            'editorial_heading': 'Open-access cashback &mdash; but the tiered structure means you need volume to earn well',
            'best_for': 'Businesses on Tide, Starling, or Monzo who want cashback without a BCA switch',
            'watch_out': '25.5% APR. Cashback rate depends on spend volume &mdash; low spenders earn less.',
            'not_ideal': 'You can access Santander&rsquo;s flat 1% through an existing BCA',
            'eligibility': 'No existing account required. &pound;10k&ndash;&pound;6.5m turnover.',
        },
        'capital_on_tap': {
            'fit_label': 'Cashback on the Pro card tier',
            'summary_strip': 'Up to 1% cashback (Pro) &middot; &pound;299/year Pro card &middot; No bank account required',
            'verdict': 'The free card earns minimal rewards. The Pro card (&pound;299/year) earns up to 1% cashback. Whether it&rsquo;s worth the fee depends entirely on your spend volume.',
            'editorial_heading': 'You pay &pound;299/year for the cashback. At 1%, you need &pound;29,900 spend to break even.',
            'best_for': 'Limited companies spending &pound;30k+ annually who want cashback and high limits',
            'watch_out': '&pound;299 annual fee on Pro card. Free card earns very little. Sole traders excluded.',
            'not_ideal': 'Your annual spend is under &pound;30k, or you&rsquo;re a sole trader',
            'eligibility': 'Limited companies and LLPs only.',
        },
        'funding_circle_cashback': {
            'fit_label': 'Fintech cashback card',
            'summary_strip': '2% then 1% cashback &middot; &pound;0 yr 1, then &pound;195/year &middot; No bank account required',
            'verdict': 'A cashback-focused fintech card. No bank-switching required. Verify current cashback rate and terms before applying.',
            'editorial_heading': 'Cashback from a fintech lender &mdash; check current rate before applying',
            'best_for': 'Businesses wanting cashback outside the traditional bank system',
            'watch_out': '34.9% rep. APR. 2% cashback first 6 months, then 1% uncapped. Check fundingcircle.com.',
            'not_ideal': 'You&rsquo;re a sole trader &mdash; Funding Circle accepts limited companies only',
            'eligibility': 'UK limited companies only. Min 1 year trading. No existing account required.',
        },
        'natwest_business_plus': {
            'fit_label': 'Rewards for NatWest customers',
            'summary_strip': 'Tiered cashback &middot; NatWest BCA required',
            'verdict': 'The rewards-focused variant of the NatWest card. If you already bank with NatWest and want rewards rather than low APR, this is the one to consider.',
            'editorial_heading': 'NatWest&rsquo;s rewards card &mdash; if you already bank there',
            'best_for': 'Existing NatWest customers who prefer rewards over a low APR',
            'watch_out': 'Tiered cashback details',
            'not_ideal': 'You don&rsquo;t bank with NatWest',
            'eligibility': 'NatWest business current account required.',
        },
        'rbs': {
            'fit_label': 'Rewards for RBS customers (Scotland)',
            'summary_strip': 'Cashback/rewards &middot; RBS BCA required',
            'verdict': 'Essentially the NatWest Plus card but through the RBS brand. Primarily relevant for Scottish businesses banking with RBS.',
            'editorial_heading': 'The RBS equivalent of NatWest Plus &mdash; for Scottish businesses',
            'best_for': 'RBS business customers who want a rewards card',
            'watch_out': '29% rep. APR. &pound;70/cardholder fee. 0.5%&ndash;3% tiered cashback capped at &pound;600/year. RBS BCA required.',
            'not_ideal': 'You don&rsquo;t bank with RBS',
            'eligibility': 'RBS business current account required.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'Cashback and rewards cards only deliver value if you clear the balance monthly or if the reward outweighs the interest you pay. We reviewed the earn rates and APRs across every UK business rewards card: if you carry a balance, the interest cost will almost certainly exceed any cashback or points earned. Check the APR before you check the earn rate.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'UK business credit card rewards split into three types: flat cashback (Santander, Barclaycard, Funding Circle), Membership Rewards points (Amex Gold and Platinum), and Avios air miles (BA Amex). Each works differently and suits different spending patterns.',
            'This page ranks every cashback and reward card available to UK businesses in March 2026, with earn rates and fees verified against each provider. The page leads with the question that determines whether a rewards card makes sense for you at all. Most businesses carrying a balance will lose more in interest than they earn in rewards &mdash; the maths is not close.',
            'If you spend &pound;3,000 a month on business expenses and clear in full, you could earn &pound;360&ndash;&pound;720 a year depending on the card. If you carry even part of that balance at 25% APR, the interest can exceed the rewards within a single billing cycle. We walk through the exact calculations below so you can see where you fall.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Do You Actually Benefit From a Rewards Card?'},
        {'type': 'prose', 'paragraphs': [
            'The answer depends almost entirely on whether you clear your balance each month. Data from UK Finance shows that 84% of micro-businesses and 94% of small businesses do clear monthly &mdash; which means cashback works for the majority. But averages hide sector variation: in construction, only 35% of businesses clear monthly. If you are in a lumpy-cash-flow sector, the interest cost on a carried balance will almost certainly exceed your cashback earnings. Check your own payment history before choosing a rewards card over a <a href="/business-credit-cards/low-apr-business-credit-cards/">low APR card</a>.',
        ]},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Your pattern</th><th>Rewards card?</th><th>Why</th></tr></thead>'
            '<tbody>'
            '<tr><td>Clear balance in full every month</td><td>Yes</td><td>You earn rewards with zero interest cost</td></tr>'
            '<tr><td>Carry a balance most months</td><td>Probably not</td><td>Interest will exceed rewards. Look at <a href="/business-credit-cards/low-apr-business-credit-cards/">low APR cards</a> instead</td></tr>'
            '<tr><td>Clear most months, carry occasionally</td><td>Maybe</td><td>Run the numbers: monthly reward vs occasional interest charge</td></tr>'
            '<tr><td>Spend heavily in one category (Amazon, travel)</td><td>Yes, if matched</td><td>Category-specific cards earn 2&ndash;3x the general rate</td></tr>'
            '</tbody></table>'},

        {'type': 'toc_start'},
        {'type': 'heading', 'level': 2, 'text': 'Compare the Cashback and Reward Cards'},
        {'type': 'prose', 'paragraphs': [
            'Earn rates, annual fees, and card types for all 11 cashback and rewards cards verified March 2026.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'capital_on_tap': {'text': 'Top Pick', 'color': 'top'},
                'funding_circle_cashback': {'text': 'Best Intro Rate', 'color': 'gold'},
                'barclaycard': {'text': 'Open Access', 'color': 'pink'},
                'santander': {'text': 'Simple Cashback', 'color': 'teal'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': 'Fees and rates verified 20 March 2026 from public sources. Confirm current terms with the provider before applying.',
        }},

        {'type': 'heading', 'level': 2, 'text': 'Cashback vs Points vs Avios'},

        {'type': 'prose', 'paragraphs': [
            'Cashback is the simplest: you earn a percentage back on spend, credited to your statement. No transfer decisions, no partner programmes, no redemption complexity. We verified that Santander offers 1% flat and Barclaycard tiers by volume. If you want your rewards in cash with zero effort, this is the category for you.',
            'Membership Rewards (Amex) are more flexible but more complex. You earn points per pound that can transfer to airline partners (including BA Avios), hotel programmes, or be used as statement credit. The value per point depends entirely on how you redeem. At best, transferring to BA Avios and booking premium cabin flights, you can extract 1.5&ndash;2p per point. At worst, using points as statement credit, you get around 0.45p per point. That range means two businesses earning the same points can get wildly different value. We cover the full Amex range in our <a href="/business-credit-cards/compare-american-express-business-credit-cards/">Amex business card comparison</a>.',
            'Avios (BA Amex) are straightforward if you fly BA. You earn Avios directly on spend. No transfer step, no intermediary currency. If you don&rsquo;t fly BA, these points have limited value. A recruitment consultant spending &pound;4,000 a month on the BA Amex Accelerating would earn 6,000 Avios monthly &mdash; enough for a short-haul return to Europe every two months. See our <a href="/business-credit-cards/best-cards-with-air-miles-avios/">guide to air miles and Avios cards</a> for the full breakdown.',
            'The most common mistake: businesses choosing rewards complexity when cashback would serve them better. If you do not fly BA regularly and you do not have the time or interest to optimise Membership Rewards redemptions, flat cashback gives you the best return for the least effort. That is not a criticism of Amex &mdash; it is a realistic assessment of how most small businesses actually use their cards.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'The Real Return: Cashback at Different Spend Levels'},

        {'type': 'prose', 'paragraphs': [
            'We calculated what you actually earn from the main cashback cards at four monthly spend levels. These figures assume you clear the balance in full every month &mdash; if you carry a balance, subtract the interest cost from the return. At most APRs on this list, carrying even a small balance wipes out the cashback entirely.',
        ]},

        {'type': 'table', 'html':
            '<table><thead><tr><th>Monthly Spend</th><th>Santander (1% flat)</th><th>Barclaycard (up to 1%)</th><th>Capital on Tap Pro (1%)</th><th>Funding Circle (1% ongoing)</th></tr></thead>'
            '<tbody>'
            '<tr><td>&pound;1,000/month</td><td>&pound;120/year</td><td>&pound;60&ndash;&pound;120/year</td><td>&pound;120/year minus &pound;299 fee = <strong>-&pound;179</strong></td><td>&pound;120/year</td></tr>'
            '<tr><td>&pound;3,000/month</td><td>&pound;360/year</td><td>&pound;240&ndash;&pound;360/year</td><td>&pound;360/year minus &pound;299 fee = <strong>&pound;61</strong></td><td>&pound;360/year</td></tr>'
            '<tr><td>&pound;5,000/month</td><td>&pound;600/year</td><td>&pound;480&ndash;&pound;600/year</td><td>&pound;600/year minus &pound;299 fee = <strong>&pound;301</strong></td><td>&pound;600/year</td></tr>'
            '<tr><td>&pound;10,000/month</td><td>&pound;1,200/year</td><td>&pound;960&ndash;&pound;1,200/year</td><td>&pound;1,200/year minus &pound;299 fee = <strong>&pound;901</strong></td><td>&pound;1,200/year</td></tr>'
            '</tbody></table>'},

        {'type': 'prose', 'paragraphs': [
            'The numbers expose the break-even clearly. Capital on Tap&rsquo;s Pro card costs &pound;299 per year. At 1% cashback, you need &pound;29,900 of annual spend just to cover the fee. Below that, you are paying for the privilege of earning cashback. A marketing agency spending &pound;8,000 a month clears the fee comfortably and nets &pound;661 in genuine cashback. A sole trader spending &pound;1,500 a month loses money on the Pro card and would be better off with Santander or Barclaycard.',
            'At the &pound;10,000 monthly level, the differences between providers narrow. You earn roughly &pound;1,200 per year on any 1% card. The real differentiator at that spend level becomes secondary features: FX fees (Capital on Tap charges none), acceptance gaps (Amex is not universal), and whether you need a BCA (Santander does, Barclaycard does not).',
            'One scenario we want to flag: if you carry a balance even one month in three, the maths changes dramatically. Carrying &pound;3,000 for a single month at 25.5% APR costs you roughly &pound;64 in interest. That wipes out two months of cashback at &pound;3,000 monthly spend. Your rewards card just became a cost centre. If you think you might carry a balance, compare the <a href="/business-credit-cards/low-apr-business-credit-cards/">low APR cards</a> first.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Is Cashback Taxable for Businesses?'},
        {'type': 'prose', 'paragraphs': [
            'HMRC treats cashback earned on business credit card purchases as a reduction in allowable expenses rather than taxable income (see HMRC Business Income Manual BIM40455). You reduce the cost of the expense rather than declaring cashback as revenue. If you spend &pound;1,000 and receive &pound;10 cashback, you record the expense as &pound;990. This means cashback does not increase your tax bill &mdash; it decreases the deduction you can claim, which has a smaller impact. We recommend checking with your accountant if your cashback amounts are significant, but for most small businesses this is straightforward bookkeeping.',
        ]},

        {'type': 'divider', 'label': 'Card-by-card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Every Cashback and Rewards Card'},
        {'type': 'card_list'},

        {'type': 'heading', 'level': 2, 'text': 'Other Reward Cards Worth Knowing About'},
        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'The Maths: When Rewards Pay Off'},
        {'type': 'prose', 'paragraphs': [
            'We calculated the returns at different spend levels. At 1% cashback and &pound;3,000 monthly spend, you earn &pound;360 per year. That&rsquo;s meaningful. At &pound;500 monthly spend, you earn &pound;60 &mdash; less than one month of a &pound;32 annual fee.',
            'For Amex Membership Rewards, the value depends on redemption. Transfer to BA Avios at 1:1 and book a short-haul return at 9,000 Avios: that&rsquo;s roughly 0.8p per point. Use as statement credit: typically 0.45p per point. We compared the effective return across all redemption routes and the gap between best and worst can double the value of the same spend.',
            'These numbers matter because they determine whether the annual fee is worth paying. We calculated the break-even: a &pound;195 annual fee on an Amex Gold needs roughly &pound;25,000 of annual spend at good redemption rates to cover the cost. Below that threshold, the fee eats your rewards and you would have been better off with a no-fee card.',
            'Here is a worked example. A consultancy spending &pound;5,000 per month on an Amex Business Gold earns roughly 5,000 Membership Rewards points monthly (60,000 per year). If you transfer those to BA Avios and book two long-haul return flights at 40,000 Avios each (off-peak economy), you could get &pound;1,200+ of flights for the &pound;195 annual fee. That is a genuine return. But if you let the same points sit unused or redeem them as statement credit at 0.45p each, you get &pound;270 &mdash; a net return of just &pound;75 after the annual fee. Same card, same spend, vastly different outcomes depending on whether you actually use the rewards.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Which Reward Type Suits Your Business?'},
        {'type': 'prose', 'paragraphs': [
            'If you travel for business more than four times a year on BA routes, Avios cards will almost certainly outperform cashback for you. If you never fly or fly on budget airlines, Avios have minimal practical value and you should stick with cashback.',
            'If your business buys heavily on Amazon, the Amazon Amex card concentrates value where your spend already sits. A small ecommerce business ordering &pound;3,000 of stock monthly from Amazon Business earns more from this niche card than from a general 1% cashback card. But if your Amazon spend is &pound;200 a month, the niche earn rate barely registers and you are better off with a broad cashback card.',
            'Cashback is the right default for most UK small businesses. It requires no redemption strategy, no partner knowledge, and no ongoing optimisation. You earn money back, it appears on your statement, and you move on. Points-based rewards only outperform cashback if you actively manage them.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/best-cards-with-air-miles-avios/">Cards for Avios and air miles</a></li>\n'
            '    <li><a href="/business-credit-cards/compare-american-express-business-credit-cards/">Compare Amex business cards</a></li>\n'
            '    <li><a href="/business-credit-cards/low-apr-business-credit-cards/">Low APR cards</a> (if you carry a balance)</li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Cashback and Rewards FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'Is cashback on business credit cards taxable in the UK?',
                'a': 'HMRC treats cashback earned on business purchases as a reduction in allowable expenses rather than taxable income (HMRC Business Income Manual BIM40455). You record the net expense (purchase minus cashback) rather than declaring cashback as revenue. This means cashback reduces your deduction rather than increasing your tax bill. Check with your accountant if amounts are significant.',
            },
            {
                'q': 'What is the best cashback rate on a UK business credit card?',
                'a': 'Funding Circle offers 2% cashback for the first six months, then 1% uncapped. Capital on Tap Pro and Santander both offer 1% flat cashback on all spend. The best effective rate depends on your spend volume and whether annual fees apply &mdash; check current terms with each provider.',
            },
            {
                'q': 'Are cashback cards worth it if I carry a balance?',
                'a': 'Usually not. At 25.5% APR, carrying &pound;3,000 for a single month costs roughly &pound;64 in interest &mdash; wiping out two months of cashback at that spend level. If you carry a balance regularly, a low-APR card will save you more than any cashback programme earns.',
            },
            {
                'q': 'What is the difference between cashback and Membership Rewards points?',
                'a': 'Cashback credits a percentage of your spend back to your statement as cash. Membership Rewards (Amex) earn points that can be transferred to airline partners, hotel programmes, or redeemed as statement credit. Cashback is simpler and requires no redemption strategy. Points can deliver higher value if you actively manage transfers, but lower value if redeemed as statement credit.',
            },
            {
                'q': 'Do I need to spend a minimum amount to earn cashback?',
                'a': 'Most UK business cashback cards have no minimum spend to start earning. However, cards with annual fees (like Capital on Tap Pro at &pound;299/year) require enough spend to cover the fee before cashback becomes a net gain. At 1% cashback, you need &pound;29,900 in annual spend to break even on the Pro card fee.',
            },
            {
                'q': 'Can I earn cashback and Avios on the same card?',
                'a': 'No. Each card earns one type of reward. Amex Membership Rewards cards earn points that can be converted to Avios or used as statement credit, but you choose at the point of redemption &mdash; you do not earn both simultaneously.',
            },
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified cashback rates, earn rates, and fees against each provider&rsquo;s public pricing page on 20 March 2026. We update these figures quarterly.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees from some providers listed. This does not affect our editorial rankings.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
