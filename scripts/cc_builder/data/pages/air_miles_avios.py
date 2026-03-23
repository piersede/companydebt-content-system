"""Page config for: Best Business Credit Cards for Air Miles and Avios.

This page is specifically about earning Avios and air miles on business card spend.
BA Amex earns Avios directly. Amex Membership Rewards transfer to Avios 1:1.
Capital on Tap Pro points may transfer to Avios (unconfirmed from public sources).
All other UK business cards do NOT earn air miles.
Cards that don't earn Avios are in separate_card_ids with explanation of why they
appear on this page (common search result confusion or indirect rewards relevance).
"""

PAGE_CONFIG = {
    'slug': 'best-cards-with-air-miles-avios',
    'page_type': 'roundup',
    'wp_page_id': 44276,
    'title': 'Best Business Credit Cards for Air Miles and Avios (2026)',
    'meta_description': (
        'The only UK business credit cards that earn Avios and air miles. '
        'BA Amex, Membership Rewards, and what else is available. Verified March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Which Cards Actually Earn Avios?': [
            'Definitive table: only 3 confirmed Avios-earning cards',
            'Capital on Tap Avios transfer flagged as unconfirmed',
        ],
        'Compare the Avios Cards': [
            'Five cards compared on earn mechanism and card type',
        ],
        'Direct Avios vs Transfer: What&rsquo;s the Difference?': [
            'MR point valuation range by redemption route (0.5p-1.5p)',
            'Recruitment agency scenario: BA-only vs mixed travel',
            'Transfer is manual step; BA Amex credits automatically',
        ],
        'How Many Avios Does Your Spend Actually Earn?': [
            'Break-even calc: £17k-£21k spend to cover £250 fee',
            'Net Avios after fee deduction at £48k spend',
            'BA Amex vs Gold earn rate at same spend level',
        ],
        'How Many Flights Can You Actually Earn?': [
            'Spend-to-flight table for 7 routes (BA reward pricing)',
            'Business-class Avios costs show 18-month accumulation',
        ],
        'Cards That Earn Avios or Air Miles': [
            'Ordered by earn clarity: direct first, then transfer',
        ],
        'Cards That Do NOT Earn Avios': [
            'Prevents wasted applications on non-Avios cards',
        ],
        'The Amex Acceptance Problem for Avios Earners': [
            '30% non-Amex supplier threshold calculation',
            'Three-month statement audit method for Amex fit',
            'Workaround: Amex primary + no-FX Visa backup',
        ],
        'Avios and Air Miles FAQs': [
            '36-month inactivity expiry rule verified on BA site',
            'Personal + business Avios pooling confirmed',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'ba_amex_accelerating',
        'top_pick_label': 'Top Pick',
        'top_pick_tagline': 'Up to 3 Avios per pound on BA purchases',
        'top_pick_features': [
            '1.5 Avios per &pound;1 on general spend',
            '3 Avios per &pound;1 on BA purchases',
            '&pound;250/year annual fee',
            'Direct Avios earn &mdash; no transfer step required',
            'Travel benefits included',
            'Sole traders, partnerships &amp; LTDs accepted',
        ],
        'also_consider': [
            {
                'card_id': 'amex_business_gold',
                'badge': 'Flexible Points',
                'badge_color': 'gold',
                'tagline': 'MR points transfer to Avios 1:1, or use for hotels',
            },
            {
                'card_id': 'amex_business_platinum',
                'badge': 'Premium Perks',
                'badge_color': 'pink',
                'tagline': 'Highest earn rate plus lounge access',
            },
        ],
    },

    'card_ids': [
        'ba_amex_accelerating', 'amex_business_gold', 'amex_business_platinum',
        'amex_business_basic', 'capital_on_tap',
    ],
    'separate_card_ids': [
        'amazon_amex', 'natwest_business_plus', 'barclays_premium_plus',
    ],

    'card_overrides': {
        'ba_amex_accelerating': {
            'fit_label': 'Best card for earning Avios',
            'summary_strip': '&pound;250/year &middot; 1.5 Avios per &pound;1 on general spend &middot; 3 Avios per &pound;1 on BA spend',
            'verdict': 'The only UK business card that earns Avios directly on every pound of spend. No transfer step, no intermediary points currency, no partner conversion. If BA is your airline and Amex is accepted by your suppliers, there is no better card for Avios accumulation.',
            'editorial_heading': 'Direct Avios on every pound &mdash; the cleanest Avios-earning mechanism in the UK business card market',
            'best_for': 'Businesses with regular BA flights that want Avios on all card spend, not just on flight purchases',
            'watch_out': 'Amex acceptance gaps mean some suppliers won&rsquo;t take it. Annual fee requires enough spend to justify. Only valuable for BA or oneworld flyers.',
            'not_ideal': 'You don&rsquo;t fly BA or oneworld partners, or your primary suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs &mdash; check americanexpress.com/uk for full criteria',
        },
        'amex_business_gold': {
            'fit_label': 'Best flexible route to Avios',
            'summary_strip': '&pound;0 first year, then &pound;195/year &middot; 1 MR point per &pound;1 &middot; Transfers to Avios 1:1 &middot; Charge card',
            'verdict': 'Membership Rewards points transfer to BA Avios at 1:1, making this an effective Avios-earning card with the option to redirect points to hotel programmes or statement credit if your travel plans change. The flexibility over the BA card is the reason some businesses prefer it.',
            'editorial_heading': 'Avios when you want them, hotel points when you don&rsquo;t &mdash; the case for Gold over the BA card',
            'best_for': 'Businesses spending &pound;3k+/month that clear monthly, fly BA sometimes but not exclusively, and want to keep reward options open',
            'watch_out': 'Charge card &mdash; full balance due monthly. Transfer to Avios is 1:1 but points value depends on redemption choice. Amex acceptance gaps.',
            'not_ideal': 'You exclusively fly BA and want the highest direct Avios earn rate (BA Amex earns Avios directly, which avoids any transfer friction)',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs &mdash; check americanexpress.com/uk for full criteria',
        },
        'amex_business_platinum': {
            'fit_label': 'Highest earn rate, biggest fee',
            'summary_strip': '&pound;650/year &middot; 1 MR point per &pound;1 (bonus at &pound;10k/month) &middot; Transfers to Avios 1:1 &middot; Lounge access &middot; Charge card',
            'verdict': 'The highest Membership Rewards earn rate of any Amex business card, plus lounge access and travel insurance. Points transfer to Avios at 1:1. The annual fee is the highest on this list and only makes sense at significant spend volume.',
            'editorial_heading': 'More Avios per pound than Gold, but the fee only pays off above a high spend threshold',
            'best_for': 'High-spend businesses (&pound;10k+/month) that fly frequently and value the Centurion lounge access alongside Avios',
            'watch_out': 'Highest annual fee on this list. Charge card structure &mdash; full balance due monthly. Amex acceptance gaps overseas.',
            'not_ideal': 'Monthly spend under &pound;5k, or you want Avios without the premium travel perks you won&rsquo;t use',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs &mdash; check americanexpress.com/uk for full criteria',
        },
        'amex_business_basic': {
            'fit_label': 'No Avios &mdash; listed for clarity',
            'summary_strip': '&pound;0 annual fee &middot; No Membership Rewards &middot; Charge card (no rewards programme)',
            'verdict': 'The Business Basic Card does not earn Membership Rewards points and has no rewards programme. It is a charge card with a Pay Over Time option for eligible purchases. Listed here because it is an Amex business card, but it is not an Avios-earning card.',
            'editorial_heading': 'No Membership Rewards, no Avios &mdash; not an air miles card despite being in the Amex range',
            'best_for': 'Businesses wanting Amex infrastructure with no annual fee &mdash; but not for Avios or rewards',
            'watch_out': 'No Membership Rewards. No Avios earn. This card does not contribute to air miles accumulation.',
            'not_ideal': 'You want to earn Avios or any rewards on card spend (Gold, Platinum, or BA Amex are the options)',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs &mdash; check americanexpress.com/uk for full criteria',
        },
        'capital_on_tap': {
            'fit_label': 'Points may transfer to Avios (unconfirmed)',
            'summary_strip': 'From 13.86% floor APR &middot; Pro card: up to 1% rewards &middot; Avios transfer unconfirmed &middot; No bank account required',
            'verdict': 'Capital on Tap Pro earns rewards points on spend. Whether those points can transfer to BA Avios is not confirmed from public sources. Check directly with Capital on Tap before choosing this card as an Avios route.',
            'editorial_heading': 'The Avios transfer link is not confirmed &mdash; verify before relying on this as an air miles card',
            'best_for': 'Limited companies that want high credit limits and have confirmed the Avios transfer option works for them',
            'watch_out': 'Avios transfer partner status is unconfirmed from public sources &mdash; check directly with Capital on Tap. Average actual APR Oct&ndash;Dec 2025 was 46.05%. Sole traders excluded.',
            'not_ideal': 'You want a confirmed, direct Avios-earning mechanism without verification steps',
            'eligibility': 'UK limited companies and LLPs only. Min turnover &pound;24,000/year. Companies House registration required.',
        },
        'amazon_amex': {
            'fit_label': 'Amazon cashback card, not an Avios card',
            'summary_strip': '1.5&ndash;2% cashback on Amazon &middot; &pound;50/year (free yr 1) &middot; Requires Amazon Business account',
            'verdict': 'The Amazon Business Amex earns cashback on Amazon purchases, not Avios. It earns Membership Rewards points on other spend, which can transfer to Avios, but Amazon-specific cashback does not convert to air miles.',
            'editorial_heading': 'The Amazon cashback is cashback, not Avios &mdash; only the general MR earn transfers to air miles',
            'best_for': 'Heavy Amazon Business spenders who also want a secondary Avios route on non-Amazon spend',
            'watch_out': 'The elevated earn rate on Amazon spend is cashback, not transferable points. Non-Amazon spend earns 0.5% cashback only &mdash; no Membership Rewards points to transfer to Avios.',
            'not_ideal': 'You want to maximise Avios on all spend &mdash; the BA Amex earns more Avios per pound on general spend',
            'eligibility': 'Requires Amazon Business account. Sole traders, partnerships, limited companies accepted.',
        },
        'natwest_business_plus': {
            'fit_label': 'Does NOT earn Avios or air miles',
            'summary_strip': '29% rep. APR &middot; 0.5&ndash;3% tiered cashback &middot; No Avios earn &middot; NatWest BCA required',
            'verdict': 'NatWest Business Plus earns rewards in the NatWest scheme, not Avios or air miles. Listed here because it appears in searches for UK travel business cards, but it is not an air miles card.',
            'editorial_heading': 'NatWest rewards are not Avios &mdash; listed here to prevent wasted application time',
            'best_for': 'Existing NatWest customers who want rewards and no FX fee, and don&rsquo;t specifically need air miles',
            'watch_out': 'This card does not earn Avios or air miles. It earns tiered cashback (0.5&ndash;3%) in the NatWest rewards programme only.',
            'not_ideal': 'You specifically want to earn Avios or air miles on business card spend',
            'eligibility': 'NatWest business current account required. &pound;2m&ndash;&pound;6.5m turnover.',
        },
        'barclays_premium_plus': {
            'fit_label': 'Does NOT earn Avios or air miles',
            'summary_strip': '19.0% purchase rate &middot; &pound;100/year &middot; No Avios earn &middot; Barclays account not required',
            'verdict': 'Barclays Business Premium Plus is a premium card with a rewards programme, but it does not earn Avios or air miles. Listed here because it appears in premium business card comparisons alongside Avios cards.',
            'editorial_heading': 'Premium card, but not an air miles card &mdash; the rewards do not convert to Avios',
            'best_for': 'Businesses wanting a premium bank card without the Amex acceptance constraint &mdash; but not for air miles',
            'watch_out': 'This card does not earn Avios or air miles. Rewards programme details should be confirmed directly with Barclays.',
            'not_ideal': 'You want Avios or air miles on business card spend',
            'eligibility': 'No Barclays business account required. Check barclays.co.uk/business for full eligibility criteria.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'Most UK business credit cards do not earn Avios or air miles. The list of cards that actually earn Avios is short: the BA Amex earns Avios directly. The Amex Membership Rewards cards (Gold and Platinum) earn points that transfer to Avios at 1:1. Capital on Tap Pro may transfer to Avios but this is unconfirmed. Every other UK business card earns cashback, proprietary points, or nothing &mdash; not air miles.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'If you want to earn Avios on business card spend in the UK, you have two options: the BA Amex (direct Avios) or an Amex Membership Rewards card (points that transfer to Avios at 1:1). That&rsquo;s the complete list of confirmed options. We verified this against each provider&rsquo;s public product pages in March 2026. Any comparison page that lists NatWest, Lloyds, Barclaycard, or Capital on Tap alongside the Amex cards without this clarification is misleading you.',
            'The decision between the two routes is not complicated: if you fly BA exclusively and clear monthly, the BA Amex earns Avios at a higher rate than transferring from Membership Rewards. If you want flexibility &mdash; sometimes Avios, sometimes hotel points, sometimes statement credit &mdash; the Amex Gold is the better platform. If you don&rsquo;t fly at all, see our <a href="/business-credit-cards/best-cashback-and-reward/">cashback card roundup</a> instead &mdash; Avios have no value without flights.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Which Cards Actually Earn Avios?'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Card</th><th>Earns Avios?</th><th>How</th><th>Annual Fee</th></tr></thead>'
            '<tbody>'
            '<tr><td>BA Amex Accelerating</td><td>Yes &mdash; directly</td><td>1.5 Avios per &pound;1 (3 on BA)</td><td>&pound;250/year</td></tr>'
            '<tr><td>Amex Business Gold</td><td>Yes &mdash; via transfer</td><td>MR points transfer to Avios 1:1</td><td>&pound;0 yr 1, then &pound;195</td></tr>'
            '<tr><td>Amex Business Platinum</td><td>Yes &mdash; via transfer</td><td>MR points transfer to Avios 1:1</td><td>&pound;650/year</td></tr>'
            '<tr><td>Amex Business Basic</td><td>No</td><td>No Membership Rewards programme</td><td>&pound;0</td></tr>'
            '<tr><td>Capital on Tap Pro</td><td>Unconfirmed</td><td>Check directly with provider</td><td>&pound;299/year (Pro)</td></tr>'
            '<tr><td>NatWest Business Plus</td><td>No</td><td>NatWest cashback scheme only</td><td>&pound;70/card</td></tr>'
            '<tr><td>All other UK bank cards</td><td>No</td><td>No air miles programme</td><td>Various</td></tr>'
            '</tbody></table>'},

        {'type': 'toc_start'},
        {'type': 'heading', 'level': 2, 'text': 'Compare the Avios Cards'},
        {'type': 'prose', 'paragraphs': [
            'The five cards below are the confirmed or possible Avios-earning options. Annual fee, earn mechanism, and card type are the key variables.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'ba_amex_accelerating': {'text': 'Top Pick', 'color': 'top'},
                'amex_business_gold': {'text': 'Flexible Points', 'color': 'gold'},
                'amex_business_platinum': {'text': 'Premium Perks', 'color': 'pink'},
                'capital_on_tap': {'text': 'Unconfirmed Avios', 'color': 'teal'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': 'Fees and rates verified 20 March 2026 from public sources. Confirm current terms with the provider before applying.',
        }},

        {'type': 'prose', 'paragraphs': [
            '<em>Avios earn confirmed against provider pages, 20 March 2026. Capital on Tap Avios transfer status unconfirmed from public sources.</em>',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Direct Avios vs Transfer: What&rsquo;s the Difference?'},
        {'type': 'prose', 'paragraphs': [
            'The BA Amex credits Avios directly to your British Airways Executive Club account with each statement. There is no transfer step and no minimum point balance to convert. We confirmed this against the BA Amex product page in March 2026.',
            'Membership Rewards cards (Gold and Platinum) earn proprietary Amex points. When you want Avios, you initiate a transfer from your Membership Rewards balance to your Executive Club account. We confirmed the transfer rate is 1:1 and near-instant, but it is a manual step. For a full breakdown of all five Amex cards, see our <a href="/business-credit-cards/compare-american-express-business-credit-cards/">Amex business card comparison</a>.',
            'MR point valuations vary significantly by redemption route. For airline mile transfers, expect 0.75p&ndash;1.5p per point, with long-haul premium cabin bookings pushing toward the upper end. Hotel transfers are lower: roughly 0.75p per point for Marriott Bonvoy (2:3 transfer ratio) and 0.66p for Hilton Honors (1:2). The floor is around 0.5p per point if you redeem through Nectar or the Amex retail portal. If you are accumulating MR specifically for Avios, the 1:1 transfer rate means each point is worth whatever you get per Avios at redemption &mdash; typically 0.8p&ndash;1.2p on short-haul economy, and 1.5p or more on long-haul in a premium cabin.',
            'The practical implication: if you know with certainty you want Avios, we recommend the BA Amex as the cleaner route. If you&rsquo;re not sure you&rsquo;ll always want Avios &mdash; or if you sometimes travel on non-BA airlines and want hotel points instead &mdash; keeping Membership Rewards unredeemed gives you more time to decide.',
            'Here is a common scenario: a recruitment agency director flies BA to Edinburgh most months but takes two or three European trips a year on non-BA carriers. The BA Amex earns Avios faster, but those Avios are useless on Lufthansa or KLM. The Amex Gold lets you keep points uncommitted until you know which airline or hotel you need. We think the flexibility premium is worth the lower earn rate for businesses that do not fly exclusively on BA or oneworld partners.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Do Avios Expire If You Don&rsquo;t Use Them?'},
        {'type': 'prose', 'paragraphs': [
            'BA Avios expire after 36 months of inactivity in your Executive Club account. Any earning or spending activity resets the clock. If you are earning Avios monthly on a business card, expiry is not a practical concern &mdash; your balance resets every time a statement credits. We confirmed the 36-month inactivity rule on the BA Executive Club terms page in March 2026.',
            'Membership Rewards points on the Amex Gold and Platinum do not have a fixed expiry date while your account is open. We confirmed this on the Amex UK terms page. However, if you close the card, your unredeemed MR points are lost. Transfer them to Avios (or another partner) before cancelling.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'How Many Avios Does Your Spend Actually Earn?'},
        {'type': 'prose', 'paragraphs': [
            'At 1.5 Avios per &pound;1 on general spend via the BA Amex, &pound;30,000 of annual card spend earns 45,000 Avios. A short-haul return flight on BA in economy typically costs 9,000&ndash;18,000 Avios depending on route and timing. We compared the headline earn rates across all five Amex cards and the BA Amex delivers the highest direct Avios return for most spending patterns.',
            'The maths changes when you factor in the &pound;250 annual fee. We calculated the break-even point at a conservative redemption value of around 0.8p&ndash;1p per Avios: you need to earn at least 25,000&ndash;31,250 Avios per year to cover the fee. That&rsquo;s roughly &pound;17,000&ndash;&pound;21,000 in annual card spend. Below that level, the fee eats into the value of your Avios.',
            'Consider a small consultancy spending &pound;4,000 per month on the BA Amex &mdash; office supplies, software subscriptions, client entertainment. That is &pound;48,000 per year, which earns you 72,000 Avios. After deducting the &pound;250 fee (worth roughly 25,000 Avios at a conservative 1p valuation), your net gain is around 47,000 Avios. That is enough for a short-haul return and a domestic UK flight, earned from spend you were making anyway.',
            'For the Amex Gold route, the earn rate on general spend is 1 MR point per &pound;1, transferring to 1 Avios. The same &pound;48,000 spend earns 48,000 Avios &mdash; 24,000 fewer than the BA Amex. But the Gold fee is &pound;195 (free in year one), and you keep the option to redirect those points to hotels or statement credit if your travel plans shift. We think the BA Amex is better if you are committed to BA, and the Gold is better if you are not sure.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'How Many Flights Can You Actually Earn?'},
        {'type': 'prose', 'paragraphs': [
            'Avios accumulation means nothing unless you know what you can actually book with them. We pulled together the typical Avios costs for common UK business flight routes using BA&rsquo;s published reward flight tables (off-peak economy, one-way). These figures are indicative &mdash; BA adjusts pricing by demand, so peak dates cost more.',
        ]},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Route (one-way, economy)</th><th>Avios needed (off-peak)</th><th>Annual card spend needed (BA Amex at 1.5/&pound;1)</th><th>Annual card spend needed (Amex Gold at 1/&pound;1)</th></tr></thead>'
            '<tbody>'
            '<tr><td>London &ndash; Edinburgh</td><td>9,000</td><td>&pound;6,000</td><td>&pound;9,000</td></tr>'
            '<tr><td>London &ndash; Dublin</td><td>13,000</td><td>&pound;8,667</td><td>&pound;13,000</td></tr>'
            '<tr><td>London &ndash; Amsterdam</td><td>13,000</td><td>&pound;8,667</td><td>&pound;13,000</td></tr>'
            '<tr><td>London &ndash; Paris</td><td>13,000</td><td>&pound;8,667</td><td>&pound;13,000</td></tr>'
            '<tr><td>London &ndash; New York</td><td>40,000</td><td>&pound;26,667</td><td>&pound;40,000</td></tr>'
            '<tr><td>London &ndash; Dubai</td><td>25,000</td><td>&pound;16,667</td><td>&pound;25,000</td></tr>'
            '<tr><td>London &ndash; Singapore</td><td>51,000</td><td>&pound;34,000</td><td>&pound;51,000</td></tr>'
            '</tbody></table>'},
        {'type': 'prose', 'paragraphs': [
            '<em>Avios costs from BA reward flight pricing, indicative off-peak one-way economy. Actual costs vary by date, availability, and cabin. Taxes and fees are payable in cash on top of Avios. Verified March 2026.</em>',
            'The practical takeaway: if your business spends &pound;50,000 per year on the BA Amex, you earn 75,000 Avios. That covers a return flight to New York in economy (80,000 Avios peak, ~65,000 off-peak return) or multiple short-haul returns to European cities. For a two-person consultancy flying to Edinburgh quarterly, the 36,000 Avios needed for four return trips requires about &pound;24,000 in annual card spend. That is realistic for many small businesses.',
            'Where this breaks down: if you fly business class, the Avios costs are roughly double. A London&ndash;New York return in Club World costs around 100,000&ndash;120,000 Avios. At &pound;50,000 annual spend on the BA Amex, you are looking at 18 months to two years of accumulation for a single business-class transatlantic return. The maths only works for business class at very high spend levels or over multiple years of accumulation.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Can You Combine Personal and Business Avios?'},
        {'type': 'prose', 'paragraphs': [
            'Yes. BA Executive Club allows you to pool Avios from multiple sources into one account. If you hold both a personal BA Amex and a business BA Amex, both feed the same Executive Club balance. We confirmed this on the BA Avios FAQ page. This means a business spending &pound;30,000 on the business card and &pound;15,000 on a personal card earns a combined 67,500 Avios per year. For smaller businesses where the director is also the primary cardholder, combining personal and business earn accelerates your accumulation significantly.',
            'One thing to watch: the Amex Membership Rewards points on the Gold and Platinum cards sit in a separate Amex account until you transfer them. You can transfer from both a personal Gold and a business Gold into the same Executive Club account, but you initiate each transfer separately. The BA Amex is simpler because Avios credit automatically.',
        ]},

        {'type': 'divider', 'label': 'Card-by-card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Cards That Earn Avios or Air Miles'},
        {'type': 'prose', 'paragraphs': [
            'Ordered by Avios earn clarity: direct-earn cards first, then transfer-route cards, then the unconfirmed option.',
        ]},
        {'type': 'card_list'},

        {'type': 'heading', 'level': 2, 'text': 'Cards That Do NOT Earn Avios'},
        {'type': 'prose', 'paragraphs': [
            'These cards appear on this page because they come up in searches alongside Avios cards, or because they have rewards programmes that are sometimes confused with air miles. None of them earn Avios or air miles. Listed to prevent wasted applications.',
        ]},
        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'The Amex Acceptance Problem for Avios Earners'},
        {'type': 'prose', 'paragraphs': [
            'Every card on the main list is an Amex card. That matters because Amex acceptance in the UK is lower than Visa or Mastercard, though the gap has narrowed &mdash; Amex acceptance locations grew by 46% over the past three years. We reviewed acceptance across common business spend categories: most major hotels, airlines, and online business suppliers accept Amex. Many smaller UK suppliers, contractors, and local services still do not.',
            'If a significant part of your business spend goes through suppliers that don&rsquo;t take Amex, the Avios earn rate on that spend is zero regardless of which card you have. We recommend checking your three or four largest regular suppliers before committing. If Amex acceptance is a problem, see our <a href="/business-credit-cards/what-are-the-best-business-credit-cards-for-travel/">guide to the best travel business credit cards</a> for Visa/Mastercard options with overseas fee benefits.',
            'A practical test we recommend: look at your last three months of business card statements. Add up every transaction where Amex would have been accepted (airlines, hotels, major online platforms like AWS, Google Ads, Microsoft, most SaaS tools) and every transaction where it would not have been (many trade suppliers, local services, some government payments). If more than 30% of your spend goes to non-Amex suppliers, the effective Avios earn rate on your total spend drops significantly. A business spending &pound;5,000/month where &pound;2,000 goes to non-Amex suppliers earns Avios on only &pound;3,000 &mdash; that is 4,500 Avios per month on the BA Amex, not the 7,500 you might expect.',
            'The workaround most Avios-focused businesses use: carry the BA Amex or Gold as your primary card for Amex-accepting suppliers, and a no-FX-fee Visa card (like <a href="/business-credit-cards/what-are-the-best-business-credit-cards-for-travel/">NatWest or Capital on Tap</a>) for everything else. You lose the Avios on non-Amex spend, but you avoid the FX fee that a bank card would charge you overseas.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/what-are-the-best-business-credit-cards-for-travel/">Best business credit cards for travel</a></li>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a> (pillar page)</li>\n'
            '    <li><a href="/business-credit-cards/compare-american-express-business-credit-cards/">Compare Amex business cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-cashback-and-reward/">Best cashback and reward cards</a></li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Avios and Air Miles FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'Which UK business credit cards earn Avios?',
                'a': 'The BA Amex Accelerating earns Avios directly on every purchase. The Amex Business Gold and Platinum earn Membership Rewards points that transfer to Avios at 1:1. Capital on Tap Pro may transfer to Avios, but this is unconfirmed from public sources. No other UK business card earns Avios.',
            },
            {
                'q': 'Do Avios expire if I don&rsquo;t use them?',
                'a': 'BA Avios expire after 36 months of inactivity in your Executive Club account. Any earning or spending activity resets the clock. If you earn Avios monthly through a business card, expiry is not a practical concern. Membership Rewards points on Amex cards do not expire while the account is open.',
            },
            {
                'q': 'Can I combine personal and business Avios in one account?',
                'a': 'Yes. BA Executive Club lets you pool Avios from multiple sources into one account. Both a personal and a business BA Amex can feed the same Executive Club balance, accelerating your accumulation.',
            },
            {
                'q': 'How many Avios do I need for a flight?',
                'a': 'A short-haul one-way flight in economy (e.g. London to Edinburgh) costs around 9,000 Avios off-peak. A long-haul return to New York costs roughly 65,000&ndash;80,000 Avios in economy. Taxes and fees are payable in cash on top of Avios. Check ba.com for current reward flight pricing.',
            },
            {
                'q': 'Is the BA Amex or Amex Gold better for earning Avios?',
                'a': 'The BA Amex earns Avios at a higher rate (1.5 per &pound;1 vs 1 per &pound;1 on Gold) and credits them directly to your Executive Club. The Gold offers flexibility &mdash; points can go to Avios, hotel programmes, or statement credit. If you fly BA exclusively, the BA Amex is better. If your travel plans vary, the Gold keeps your options open.',
            },
            {
                'q': 'What happens to my Membership Rewards points if I cancel my Amex card?',
                'a': 'Unredeemed Membership Rewards points are lost when you close your Amex account. Transfer them to BA Avios or another partner programme before cancelling.',
            },
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified Avios earn rates, Membership Rewards transfer ratios, and annual fees against each provider&rsquo;s public product pages on 20 March 2026. Capital on Tap&rsquo;s Avios transfer status could not be confirmed from public sources. We update these figures quarterly.',
            '<strong>What this page covers:</strong> Only cards with a confirmed or stated Avios/air miles earning mechanism are listed in the main ranked section. Cards that appear in searches for air miles cards but do not earn Avios are included in the separate section below the main list with a clear explanation.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees from some providers listed. This does not affect our assessment of which cards earn Avios, which is based on publicly available product information.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Avios redemption values and transfer rates may change &mdash; verify directly with BA and Amex before making decisions based on points valuations.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
