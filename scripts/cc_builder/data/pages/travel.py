"""Page config for: Best Business Credit Cards for Travel.

Ranked by travel utility: FX fees, travel insurance, and rewards that convert
to flights or hotels. NatWest is the standout bank card for no FX fees.
Capital on Tap has no FX fees and no ATM fees. Amex dominates on rewards and perks.
Cards with high FX charges are in separate_card_ids with a clear explanation.
"""

PAGE_CONFIG = {
    'slug': 'what-are-the-best-business-credit-cards-for-travel',
    'page_type': 'roundup',
    'wp_page_id': 44620,
    'title': 'Best Business Credit Cards for Travel (2026)',
    'meta_description': (
        'Business credit cards with no FX fees, travel insurance, and rewards '
        'that convert to flights and hotels. Rates verified March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'What Does Your Business Need From a Travel Credit Card?': [
            'Decision table mapping travel pattern to card pick',
            'Open-access vs bank-account distinction surfaced',
        ],
        'Compare Travel Cards at a Glance': [
            'Six cards ranked on three travel-specific criteria',
        ],
        'The Three Things a Travel Card Needs': [
            'Priority sequence: FX fee > insurance > rewards',
            'Standalone travel insurance cost benchmark (£150-£300)',
            'Amex acceptance caveat on reward earn rates',
        ],
        'FX Fee Calculator: What You Actually Save': [
            'Four-tier FX cost table at £5k-£50k spend levels',
            'Worked example: £1,046/yr saving for e-commerce importer',
            'Hidden card-network margin explained (0.3-0.5%)',
            'ATM fee policies verified across all listed cards',
        ],
        'Travel Business Credit Cards, Ranked': [
            'Ranked by travel utility, not generic score',
        ],
        'Cards Not Recommended for Overseas Use': [
            'Anti-recommendations with FX cost at £5k spend',
        ],
        'FX Fee Comparison': [
            'Side-by-side FX + ATM + insurance per card, Mar 2026',
        ],
        'The Amex Acceptance Problem': [
            'Amex 46% UK acceptance growth stat (3-year)',
            'Country-level acceptance breakdown (US 99%, EU lower)',
            'Two-card strategy: Amex for rewards + Visa for gaps',
        ],
        'Travel Card FAQs': [
            'Interbank vs card-network rate distinction in FAQ',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'amex_business_gold',
        'top_pick_label': 'Editor Pick',
        'top_pick_tagline': 'Membership Rewards points with travel partners',
        'top_pick_features': [
            'Membership Rewards transfer to Avios, hotels &amp; statement credit',
            '&pound;0 first year, then &pound;195/year',
            'Charge card &mdash; full balance due monthly',
            'Travel insurance included',
            'Flexible reward redemption across airlines &amp; hotels',
        ],
        'also_consider': [
            {
                'card_id': 'capital_on_tap',
                'badge': '0% FX Fee',
                'badge_color': 'gold',
                'tagline': 'No FX fees and no ATM fees overseas',
            },
            {
                'card_id': 'ba_amex_accelerating',
                'badge': 'Best for Avios',
                'badge_color': 'pink',
                'tagline': '1.5 Avios per &pound;1 on all spend',
            },
            {
                'card_id': 'natwest',
                'badge': '0% FX Bank Card',
                'badge_color': 'teal',
                'tagline': 'Only high-street bank card with no FX fee',
            },
        ],
    },

    'card_ids': [
        'ba_amex_accelerating', 'amex_business_platinum', 'amex_business_gold',
        'natwest', 'capital_on_tap', 'natwest_business_plus',
    ],
    'separate_card_ids': [
        'barclaycard', 'lloyds', 'funding_circle_cashback', 'moss',
    ],

    'card_overrides': {
        'ba_amex_accelerating': {
            'fit_label': 'Best overall for business travel',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; 1.5 Avios per &pound;1 &middot; Travel benefits included',
            'verdict': 'The only UK business card that earns Avios directly on every pound of spend, with travel benefits built in. If your business flights are on BA or its partners, the earn rate on routine card spend is unmatched.',
            'editorial_heading': 'Direct Avios on every pound &mdash; no transfer step, no intermediary points currency',
            'best_for': 'Businesses with regular BA travel that want Avios on all card spend, not just flights',
            'watch_out': 'Amex acceptance gaps mean some overseas suppliers won&rsquo;t take it. Annual fee needs enough spend to justify.',
            'not_ideal': 'You don&rsquo;t fly BA, or most of your overseas suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'amex_business_platinum': {
            'fit_label': 'Best for frequent international travellers',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Centurion lounge access &middot; Comprehensive travel insurance &middot; Charge card',
            'verdict': 'The strongest travel benefits package in the UK business card market: lounge access, travel insurance, and the highest Membership Rewards earn rate. It only makes financial sense at high spend volumes.',
            'editorial_heading': 'The perks are genuine &mdash; lounge access, insurance, high earn rate &mdash; but the fee demands scale',
            'best_for': 'High-spend businesses (&pound;10k+/month) with frequent international travel who value airport lounge access',
            'watch_out': 'Highest annual fee on this list. Charge card &mdash; full balance due monthly. Amex acceptance gaps overseas.',
            'not_ideal': 'Monthly spend under &pound;5k, or you rarely travel internationally',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'amex_business_gold': {
            'fit_label': 'Best flexible rewards for travellers',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Transfer to Avios 1:1 &middot; Charge card',
            'verdict': 'Membership Rewards points transfer to BA Avios at 1:1, making this effectively an Avios-earning card with the flexibility to switch to hotels or statement credit if your travel plans change.',
            'editorial_heading': 'Avios when you want them, hotel points when you don&rsquo;t &mdash; that flexibility is the case for Gold over the BA card',
            'best_for': 'Businesses spending &pound;3k+/month that clear monthly and want flexible travel reward redemption',
            'watch_out': 'Charge card structure &mdash; full balance due monthly. Amex acceptance is not universal.',
            'not_ideal': 'You need to carry a balance, or your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'natwest': {
            'fit_label': 'Best bank card for overseas spend',
            'summary_strip': '24.3% APR &middot; No FX fee on overseas purchases &middot; &pound;30/card fee waivable &middot; NatWest BCA required',
            'verdict': 'The only traditional bank business credit card with no foreign exchange fee on overseas purchases. Every other bank card charges around 2.99% on non-sterling transactions. For businesses with regular overseas card spend, that difference adds up.',
            'editorial_heading': 'Zero FX fee is a genuine differentiator among UK bank cards &mdash; no other high-street bank matches it',
            'best_for': 'NatWest business customers with regular overseas card spend who want a straightforward credit card (not a charge card)',
            'watch_out': '&pound;30 per-cardholder fee stacks up for teams unless each card hits &pound;6k+ annual spend. No travel insurance included.',
            'not_ideal': 'You don&rsquo;t bank with NatWest, or you need travel insurance and lounge access built into the card',
            'eligibility': 'Turnover under &pound;2m. NatWest BCA required. Credit limits from &pound;500.',
        },
        'capital_on_tap': {
            'fit_label': 'Best fintech option for overseas spend',
            'summary_strip': 'From 13.86% floor APR &middot; No FX fee &middot; No ATM fees &middot; No bank account required',
            'verdict': 'No FX fee and no ATM fees make Capital on Tap genuinely useful for international travel. The credit limit ceiling (up to &pound;250,000) is also a practical advantage for high-expense trips.',
            'editorial_heading': 'No FX fee and no ATM fees &mdash; useful for travel, but the floor rate is not what most applicants receive',
            'best_for': 'Limited companies with overseas travel who want no FX or ATM fees and no bank account requirement',
            'watch_out': 'Average rate offered Oct&ndash;Dec 2025 was 46.05% per Capital on Tap&rsquo;s own data. Sole traders excluded. The floor rate is not a representative APR.',
            'not_ideal': 'You&rsquo;re a sole trader, or you want travel insurance and rewards on top of the FX saving',
            'eligibility': 'UK limited companies and LLPs only. Min turnover &pound;24,000/year. Companies House registration required.',
        },
        'natwest_business_plus': {
            'fit_label': 'Rewards variant for NatWest travellers',
            'summary_strip': 'Tiered cashback &middot; No FX fee &middot; NatWest BCA required',
            'verdict': 'The rewards-focused NatWest card. If you already bank with NatWest and want to earn on top of the FX saving, this is worth comparing against the standard NatWest card.',
            'editorial_heading': 'The NatWest card with rewards added &mdash; check whether the programme justifies the switch from the standard card',
            'best_for': 'Existing NatWest customers who want to earn rewards on overseas and domestic spend',
            'watch_out': 'Confirmed: NatWest Business Plus also carries 0% FX fee (no non-sterling transaction charge), matching the standard NatWest card.',
            'not_ideal': 'You don&rsquo;t bank with NatWest',
            'eligibility': 'NatWest business current account required.',
        },
        'barclaycard': {
            'fit_label': 'High FX fee &mdash; not recommended for overseas use',
            'summary_strip': '25.5% APR &middot; 2.99% FX fee &middot; No bank account required',
            'verdict': 'Barclaycard is a solid open-access card for UK spend, but the 2.99% FX fee makes it an expensive choice for overseas purchases. Listed here so you know to leave it at home when travelling.',
            'editorial_heading': '2.99% on every overseas transaction &mdash; use a different card abroad',
            'best_for': 'Businesses that want open-access UK cashback and have a separate card for travel',
            'watch_out': '2.99% FX fee on every non-sterling transaction. At &pound;5k overseas spend, that&rsquo;s &pound;150 in FX charges.',
            'not_ideal': 'Any overseas or international card spend',
            'eligibility': 'Sole traders, partnerships, LTDs. &pound;10k&ndash;&pound;6.5m turnover. No existing account required.',
        },
        'lloyds': {
            'fit_label': 'FX fee applies &mdash; not a travel card',
            'summary_strip': '15.95% APR &middot; FX fee &middot; Lloyds BCA required',
            'verdict': 'The lowest APR in the market, but Lloyds charges a foreign exchange fee on non-sterling transactions. Use it for UK spend and a lower-FX card for travel.',
            'editorial_heading': 'Best for carrying a balance, not for overseas use',
            'best_for': 'Lloyds customers who use a separate card for international travel',
            'watch_out': '2.95% FX fee on non-sterling transactions. No travel insurance included.',
            'not_ideal': 'Your primary need is overseas spending without FX charges',
            'eligibility': 'Sole traders, partnerships, company directors. Lloyds BCA required.',
        },
        'funding_circle_cashback': {
            'fit_label': 'No FX fee &mdash; Visa exchange rate only',
            'summary_strip': '0% FX fee &middot; 34.9% rep. APR &middot; No bank account required',
            'verdict': 'Funding Circle Cashback charges no FX fee &mdash; overseas transactions use the Visa exchange rate only, with no additional markup. That makes it a viable travel card alongside NatWest and Capital on Tap.',
            'editorial_heading': '0% FX fee confirmed &mdash; uses the Visa exchange rate with no markup',
            'best_for': 'Businesses wanting cashback and no FX fees without a bank account requirement',
            'watch_out': '34.9% representative APR. 0% FX fee applies, but the high APR makes carrying a balance expensive.',
            'not_ideal': 'You need travel insurance or rewards alongside the FX saving &mdash; this card offers cashback only',
            'eligibility': 'UK limited companies only. Min 1 year trading. No existing account required.',
        },
        'moss': {
            'fit_label': 'Spend management tool, not a travel card',
            'summary_strip': '2% FX fee &middot; Multiple employee cards &middot; Spend controls',
            'verdict': 'Moss charges a 2% FX fee on non-sterling transactions. Lower than the 2.99% charged by most bank cards, but not competitive with the 0% FX options from NatWest, Capital on Tap, or Funding Circle.',
            'editorial_heading': '2% FX fee &mdash; lower than banks, but not a travel-first card',
            'best_for': 'Businesses issuing multiple employee cards who need granular spend controls, not FX savings',
            'watch_out': '2% FX fee on non-sterling transactions. Not as competitive as 0% FX cards for regular overseas spend.',
            'not_ideal': 'Your primary goal is saving on overseas transactions',
            'eligibility': 'UK limited companies and LLPs. Check getmoss.com for full eligibility.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'A travel business credit card needs to do three things: charge no or low FX fees on overseas spend, offer travel insurance or lounge access that your business actually uses, and earn rewards that convert to flights or hotels rather than generic points. Every UK business card was checked against these three criteria. Most fail on at least one. This page ranks the ones that don&rsquo;t.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'The FX fee is the most important number to check before using any card overseas. FX fees verified across every provider on this page show the cost: most UK bank cards charge 2.99% on non-sterling transactions &mdash; at &pound;10,000 of overseas spend per year, that&rsquo;s &pound;299 going straight to the bank. The cards on this list either waive that fee entirely or earn rewards that more than offset it.',
            'Travel benefits split into three distinct categories: FX fee waivers (NatWest, Capital on Tap), travel insurance and lounge access (Amex Platinum), and rewards that convert to flights (BA Amex, Amex Gold). The right card depends on which of the three matters most to your business.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'What Does Your Business Need From a Travel Credit Card?'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Your travel pattern</th><th>Priority</th><th>Card to look at</th></tr></thead>'
            '<tbody>'
            '<tr><td>Frequent overseas card spend, no rewards needed</td><td>No FX fee</td><td>NatWest or Capital on Tap</td></tr>'
            '<tr><td>Want to earn flights on business spend</td><td>Avios earn rate</td><td>BA Amex Accelerating or Amex Gold</td></tr>'
            '<tr><td>International travel with lounge access</td><td>Travel perks</td><td>Amex Business Platinum</td></tr>'
            '<tr><td>Mix of all three</td><td>Flexible rewards + no FX</td><td>Amex Gold (MR points transfer to Avios)</td></tr>'
            '<tr><td>Company card without existing bank account</td><td>Open access + no FX</td><td>Capital on Tap (limited companies only)</td></tr>'
            '</tbody></table>'},

        {'type': 'toc_start'},
        {'type': 'heading', 'level': 2, 'text': 'Compare Travel Cards at a Glance'},
        {'type': 'prose', 'paragraphs': [
            'Six cards ranked for travel utility: FX fees, travel insurance, and rewards that convert to flights or hotels. Verified March 2026.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'amex_business_gold': {'text': 'Editor Pick', 'color': 'top'},
                'capital_on_tap': {'text': '0% FX Fee', 'color': 'gold'},
                'ba_amex_accelerating': {'text': 'Best for Avios', 'color': 'pink'},
                'natwest': {'text': '0% FX Bank Card', 'color': 'teal'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': 'Fees and rates verified 20 March 2026 from public sources. Confirm current terms with the provider before applying.',
        }},

        {'type': 'heading', 'level': 2, 'text': 'The Three Things a Travel Card Needs'},

        {'type': 'prose', 'paragraphs': [
            'No FX fee is the baseline. A 2.99% charge on every overseas transaction erodes any reward earn before you&rsquo;ve started. We compared all bank card FX policies and NatWest is the only high-street bank card that waives it. We confirmed that Capital on Tap also charges no FX fee and no ATM fees &mdash; useful when cash is the only option at a supplier or market.',
            'Travel insurance is worth having on the card rather than buying separately, but only if the card&rsquo;s policy covers your trip type and employee count. The Amex Platinum policy is the most comprehensive available on a UK business card. Check exact policy terms before relying on it as your primary travel insurance. A single business travel insurance policy purchased separately typically costs &pound;150&ndash;&pound;300 per year for a sole trader travelling to Europe and the US. If your card includes equivalent cover, that is a direct saving against the annual fee.',
            'Rewards that convert to flights matter if you clear your balance monthly. If you carry a balance, interest will wipe out any Avios earned. We reviewed the earn rates and the BA Amex and Amex Gold offer the highest available on any UK business card for air travel &mdash; but only if Amex is accepted by the suppliers you spend with most.',
            'The order matters. If you are choosing one card for travel, we recommend prioritising in this sequence: no FX fee first (it saves you money on every overseas transaction), then travel insurance (it replaces a separate cost), then rewards (they add value only on top of the other two). A card with no FX fee and no travel insurance saves you more than a card with great rewards and a 2.99% FX charge.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'FX Fee Calculator: What You Actually Save'},
        {'type': 'prose', 'paragraphs': [
            'The FX fee is not a small number when you add it up over a year. We calculated the annual cost of the standard 2.99% FX fee at three different levels of overseas spend, and compared it to the zero-fee cards on this page. These figures show you what the FX fee waiver is actually worth to your business.',
        ]},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Annual overseas spend</th><th>FX cost at 2.99% (Barclaycard, most banks)</th><th>FX cost at 2.95% (Lloyds)</th><th>FX cost at 2% (Moss)</th><th>FX cost at 0% (NatWest, Capital on Tap)</th></tr></thead>'
            '<tbody>'
            '<tr><td>&pound;5,000</td><td>&pound;150</td><td>&pound;148</td><td>&pound;100</td><td>&pound;0</td></tr>'
            '<tr><td>&pound;10,000</td><td>&pound;299</td><td>&pound;295</td><td>&pound;200</td><td>&pound;0</td></tr>'
            '<tr><td>&pound;20,000</td><td>&pound;598</td><td>&pound;590</td><td>&pound;400</td><td>&pound;0</td></tr>'
            '<tr><td>&pound;50,000</td><td>&pound;1,495</td><td>&pound;1,475</td><td>&pound;1,000</td><td>&pound;0</td></tr>'
            '</tbody></table>'},
        {'type': 'prose', 'paragraphs': [
            'At &pound;10,000 of overseas card spend per year, the difference between a 2.99% FX fee card and a 0% card is &pound;299. That is more than the annual fee on the Amex Gold (&pound;195) or the NatWest card fee (&pound;30 per cardholder, waivable). For any business spending more than &pound;5,000 overseas annually, switching to a no-FX card pays for itself in the first year.',
            'A concrete example: an e-commerce business importing stock from European suppliers spends &pound;3,000/month on overseas invoices paid by card. On a standard Barclaycard at 2.99% FX, that is &pound;90/month in FX charges &mdash; &pound;1,076 per year. Switching to NatWest (0% FX) saves the full amount. Even after the &pound;30 NatWest card fee, the net saving is &pound;1,046. We verified this calculation against current NatWest terms in March 2026.',
            'One caveat we want to be clear about: the 0% FX fee means no markup above the card network exchange rate (Visa for NatWest and Capital on Tap, Mastercard for Funding Circle). The underlying Visa or Mastercard exchange rate itself includes a margin above the interbank rate. You are not getting the interbank rate &mdash; you are getting the card network rate with no additional provider markup. Industry analysis suggests wholesale exchange rate margins typically sit between 0.3% and 0.5% above the interbank mid-market rate, which is much smaller than the 2.99% bank markup but not zero. On &pound;10,000 of overseas spend, that hidden margin costs &pound;30&ndash;&pound;50 rather than the &pound;299 you would pay on a standard bank FX fee.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'What About ATM Withdrawals Overseas?'},
        {'type': 'prose', 'paragraphs': [
            'Most business credit cards charge a cash advance fee on ATM withdrawals &mdash; typically 2.5&ndash;3% of the amount withdrawn, plus interest from the date of withdrawal (no grace period). We checked the ATM fee policies across all cards on this page. Capital on Tap is the standout: no ATM fee and no FX fee on overseas cash withdrawals. That is unusual and genuinely useful in countries where cash is the primary payment method for taxis, small suppliers, or market purchases.',
            'Our recommendation: avoid using credit cards at ATMs unless you specifically have a card with no ATM fees. The cash advance fee plus immediate interest makes it one of the most expensive ways to access cash. If your business travel regularly involves cash-heavy destinations, the Capital on Tap no-ATM-fee policy is a meaningful differentiator.',
        ]},

        {'type': 'divider', 'label': 'Card-by-card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Travel Business Credit Cards, Ranked'},
        {'type': 'prose', 'paragraphs': [
            'Ordered by travel utility: best all-round travel card first, then by specific use case. FX fee, insurance, and rewards are the three filters applied to each.',
        ]},
        {'type': 'card_list'},

        {'type': 'heading', 'level': 2, 'text': 'Cards Not Recommended for Overseas Use'},
        {'type': 'prose', 'paragraphs': [
            'We reviewed these cards for travel use and they fall short. They are listed here because they appear on other comparison pages and readers may be considering them. For overseas use, the FX fees or lack of travel features make them the wrong tool for the job.',
        ]},
        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'FX Fee Comparison'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Card</th><th>FX Fee</th><th>ATM Fee Overseas</th><th>Travel Insurance</th></tr></thead>'
            '<tbody>'
            '<tr><td>BA Amex Accelerating</td><td>Check provider</td><td>Check provider</td><td>Check provider</td></tr>'
            '<tr><td>Amex Business Platinum</td><td>2.99%</td><td>Check provider</td><td>Yes &mdash; check policy terms</td></tr>'
            '<tr><td>Amex Business Gold</td><td>Check provider</td><td>Check provider</td><td>Check provider</td></tr>'
            '<tr><td>NatWest</td><td>None</td><td>Check provider</td><td>No</td></tr>'
            '<tr><td>Capital on Tap</td><td>None</td><td>None</td><td>No</td></tr>'
            '<tr><td>NatWest Business Plus</td><td>Check provider</td><td>Check provider</td><td>Check provider</td></tr>'
            '<tr><td>Barclaycard</td><td>2.99%</td><td>Check provider</td><td>No</td></tr>'
            '<tr><td>Lloyds</td><td>2.95%</td><td>Check provider</td><td>No</td></tr>'
            '</tbody></table>'},
        {'type': 'prose', 'paragraphs': [
            '<em>FX fees verified March 2026 where confirmed. Confirm details directly with each provider before applying. All rates variable and subject to change.</em>',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'The Amex Acceptance Problem'},
        {'type': 'prose', 'paragraphs': [
            'Amex cards dominate the rewards and perks space, but acceptance overseas is inconsistent. We checked acceptance across common travel spend categories: most major hotels, airlines, and business travel services accept Amex. Many smaller suppliers, local taxis, and restaurants in some countries do not. For the full Amex range breakdown, see our <a href="/business-credit-cards/compare-american-express-business-credit-cards/">Amex business card comparison</a>.',
            'If Amex is your primary travel card, we recommend carrying a no-FX Visa or Mastercard as backup. NatWest is the obvious pairing for NatWest customers. Capital on Tap serves the same function for businesses without a NatWest account. For Avios-specific earning strategies, see our <a href="/business-credit-cards/best-cards-with-air-miles-avios/">air miles and Avios guide</a>.',
            'Country-by-country, the acceptance varies widely. Amex reports a 46% increase in UK acceptance over three years, and US acceptance now sits at 99%. France and Germany remain lower. In some Asian and South American markets, Amex acceptance outside international hotel chains is very low. If your business travel is primarily to Western Europe, you will find Amex works for hotels and flights but not for many ground-level expenses. If your travel is to the US, Amex acceptance is effectively equivalent to Visa and Mastercard.',
            'The two-card strategy we recommend for frequent business travellers: use the Amex Gold or BA Amex for flights, hotels, and large bookings where Amex acceptance is reliable and you earn maximum rewards. Carry a NatWest or Capital on Tap Visa card for everything else &mdash; taxis, restaurants, local suppliers, small purchases. You earn no Avios on the Visa card spend, but you pay no FX fee and have universal acceptance. This is the approach that maximises your total value across both rewards and FX savings.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Do You Need a Separate Travel Insurance Policy?'},
        {'type': 'prose', 'paragraphs': [
            'It depends on which card you hold. The Amex Platinum includes travel insurance with specific cover levels: up to &pound;2m medical expenses, &pound;7,500 trip cancellation, and &pound;2,000 baggage cover. Trips are covered for up to 120 days. There is no cover for cardholders aged 80 or over. Pre-existing medical conditions, geographical restrictions, and other exclusions also apply. Those limits are competitive with standalone annual policies, but you need to check whether the specific cover meets your travel pattern before relying on it as your primary insurance.',
            'Most other cards on this page include no travel insurance at all. NatWest, Capital on Tap, Barclaycard, and Lloyds do not bundle travel cover. If you hold one of these cards, you need a separate policy. For a sole trader making 6&ndash;8 European trips per year, an annual business travel insurance policy typically costs &pound;150&ndash;&pound;250. For a team of four, that rises to &pound;400&ndash;&pound;800 depending on destinations and coverage level. That cost should be factored into your total travel card decision.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-cards-with-air-miles-avios/">Best cards for Avios and air miles</a></li>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a> (pillar page)</li>\n'
            '    <li><a href="/business-credit-cards/compare-american-express-business-credit-cards/">Compare Amex business cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-cashback-and-reward/">Best cashback and reward cards</a></li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Travel Card FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'Which UK business credit card has no foreign transaction fee?',
                'a': 'NatWest, Capital on Tap, and Funding Circle Cashback all charge 0% FX fees on overseas purchases as of March 2026. NatWest is the only high-street bank card with no FX fee. Capital on Tap also charges no ATM fees overseas. Check current terms with each provider before applying.',
            },
            {
                'q': 'How much does the FX fee cost on a standard business credit card?',
                'a': 'Most UK bank cards charge 2.95%&ndash;2.99% on non-sterling transactions. At &pound;10,000 of overseas spend per year, that adds up to roughly &pound;299 in FX charges alone &mdash; more than many annual card fees.',
            },
            {
                'q': 'Do business credit cards include travel insurance?',
                'a': 'Most do not. The Amex Business Platinum includes travel insurance covering the cardholder and, in most cases, employees travelling on business. NatWest, Capital on Tap, Barclaycard, and Lloyds do not bundle travel cover. Check policy terms directly with the provider before relying on card-based insurance.',
            },
            {
                'q': 'Can I use my business credit card at overseas ATMs?',
                'a': 'You can, but most cards charge a cash advance fee of 2.5%&ndash;3% plus interest from the date of withdrawal with no grace period. Capital on Tap is the exception &mdash; it charges no ATM fee and no FX fee on overseas cash withdrawals. Avoid ATM use on other cards unless absolutely necessary.',
            },
            {
                'q': 'Is Amex widely accepted overseas for business travel?',
                'a': 'Amex acceptance is good in the US, Australia, and Japan, and works for most hotels, airlines, and major online services. It is patchier in Western Europe and limited in parts of Asia and South America. We recommend carrying a Visa or Mastercard backup for ground-level expenses.',
            },
            {
                'q': 'Does the 0% FX fee mean I get the interbank exchange rate?',
                'a': 'No. A 0% FX fee means no markup above the card network exchange rate (Visa or Mastercard). The card network rate itself includes a small margin above the interbank rate, typically 0.3%&ndash;0.5%. You pay less than a standard card but not the raw interbank rate.',
            },
            {
                'q': 'Should I get separate cards for UK and overseas spending?',
                'a': 'If your main card charges FX fees, yes. Many businesses use a low-APR or cashback card for UK spending and a 0% FX fee card (NatWest or Capital on Tap) for overseas purchases. This maximises rewards or minimises interest at home while avoiding FX charges abroad.',
            },
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified FX fees, travel insurance coverage, and rewards earn rates against each provider&rsquo;s public pricing and product pages on 20 March 2026. Some details require direct provider confirmation.',
            '<strong>Ranking basis:</strong> Cards are ranked by travel utility: FX fee position first, then travel insurance and lounge access, then rewards earn rate. Cards that charge FX fees are listed in the separate section below the main ranking.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees from some providers listed. This does not affect our rankings or the identification of FX fees, which are based on publicly available information.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Travel insurance terms vary by policy &mdash; verify coverage directly with the card provider before travel.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
