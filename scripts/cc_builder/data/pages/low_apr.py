"""Page config for: Best Low APR Business Credit Cards in the UK.

Reference implementation — this is the first page built with v4 template.
WP staging page ID: 70072
"""

PAGE_CONFIG = {
    'slug': 'low-apr-business-credit-cards',
    'page_type': 'roundup',
    'wp_page_id': 70072,
    'title': 'Best Low APR Business Credit Cards in the UK (2026)',
    'meta_description': (
        'Compare the lowest APR business credit cards in the UK. '
        'Rates verified against provider pricing pages, March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'APR Comparison at a Glance': [
            'Worked pound-cost example: £798 vs £1,275 on same £5k balance',
            'Bank-relationship lock-in as rate gatekeeper made explicit',
        ],
        'Keep Your Current Card, Switch to Low APR, or Look Elsewhere': [
            'Decision table splits by payment behaviour, not card features',
        ],
        'What &ldquo;Representative APR&rdquo; Means for Your Application': [
            '51% rule explained with 49% higher-rate consequence',
            'No provider publishes upper rate bound (verified Mar 2026)',
            'Sole traders and thin-file applicants flagged as likely above headline',
        ],
        'The Low-APR Business Credit Cards': [
            'Cards ranked by verified rep APR with per-card fee-waiver thresholds',
        ],
        'Not Directly Comparable: Capital on Tap': [
            'Floor-rate vs rep APR distinction: avg rate 46.05% (Oct-Dec 2025 CoT data)',
            'Separated from ranked table to prevent misleading like-for-like comparison',
        ],
        'Total Annual Cost: APR + Fees at Different Balances': [
            'Original cost model at £2k/£5k/£10k balances incl. annual fees',
            'Crossover analysis: Metro Bank cheaper than Lloyds below fee-waiver threshold',
            'Barclaycard open-access premium quantified at £160/yr on £2k balance',
        ],
        'What the APR Comparison Alone Misses': [
            'FX fee impact quantified: £299/yr on £10k overseas spend',
            'Per-cardholder vs per-account fee modelled for 4-person teams',
            'Santander saves £90/yr in fees alone vs NatWest for team of four',
        ],
        'Who Low-APR Cards Don&rsquo;t Suit': [
            'Explicit misfit: monthly clearers directed to cashback instead',
            'Capital on Tap credit ceiling (£250k) vs £25k cap on ranked cards',
            'Newer businesses warned representative APR is not guaranteed rate',
        ],
        'How to Compare Before You Apply': [
            'Worked bank-switching decision: Tide plumber saving £287/yr vs hassle cost',
            'No soft-search pre-qualification for most UK business cards (verified)',
            'Hard-search stacking risk quantified for multiple applications',
        ],
        'Low-APR FAQs': [
            'FAQ confirms fee included in rep APR calculation (common misconception)',
            'Negotiation FAQ: providers do not negotiate business card rates',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'lloyds',
        'top_pick_label': 'Top Pick',
        'top_pick_tagline': '15.95% representative APR for BCA holders',
        'top_pick_features': [
            'Lowest representative APR at 15.95%',
            '14.9% purchase rate',
            '&pound;32 annual fee waived year 1 &amp; at &pound;6k+ spend',
            'Credit limits up to &pound;25,000',
            'Sole traders, partnerships &amp; company directors accepted',
        ],
        'also_consider': [
            {
                'card_id': 'barclaycard',
                'badge': 'Open Access',
                'badge_color': 'pink',
                'tagline': 'No existing bank account required',
            },
            {
                'card_id': 'natwest',
                'badge': 'Next Lowest',
                'badge_color': 'teal',
                'tagline': '24.3% APR with 0% FX fee on overseas spend',
            },
            {
                'card_id': 'hsbc',
                'badge': 'Low Purchase Rate',
                'badge_color': 'gold',
                'tagline': '15.9% purchase rate for HSBC customers',
            },
        ],
    },

    # Card IDs in display order (ranked by APR, lowest first)
    'card_ids': [
        'lloyds', 'metro_bank', 'hsbc', 'santander', 'natwest', 'barclaycard',
    ],
    'separate_card_ids': ['capital_on_tap'],

    # Per-card overrides for this page's context
    'card_overrides': {
        'lloyds': {
            'fit_label': 'Lowest APR on this list',
            'summary_strip': '15.95% APR &middot; 14.9% purchase rate &middot; &pound;32 fee waived yr 1 and at &pound;6k+ spend',
            'verdict': 'The lowest representative APR available, but the annual fee means it only pays off with consistent spend above the waiver threshold.',
            'editorial_heading': 'Lowest headline rate, but the fee waiver threshold decides whether it actually saves you money',
            'best_for': 'Existing Lloyds customers who carry a balance and can hit &pound;6k annual spend to waive the fee',
            'watch_out': '&pound;32 annual fee per card is not waived unless you spend enough &mdash; at low volumes, Metro Bank&rsquo;s 18.9% with no fee costs less overall',
            'not_ideal': 'You bank elsewhere and would need to switch to Lloyds just for the card rate',
            'eligibility': 'Sole traders, partnerships, and company directors. Lloyds BCA required. Credit limits up to &pound;25,000.',
        },
        'metro_bank': {
            'fit_label': 'Cheapest if you won&rsquo;t hit the Lloyds fee waiver',
            'summary_strip': '18.9% APR &middot; No annual fee &middot; In-branch application only',
            'verdict': 'No annual fee at all. If your spend is too low to waive the Lloyds or NatWest fee, this is the cheaper card.',
            'editorial_heading': 'The simplest cost structure, but the branch-only application is a real barrier',
            'best_for': 'Low-spend businesses that carry a balance &mdash; no fee means APR is your only cost',
            'watch_out': 'In-branch application only. You cannot apply online, and Metro Bank&rsquo;s branch network is London-centric.',
            'not_ideal': 'Your business isn&rsquo;t near a Metro Bank branch, or you need to apply quickly',
            'eligibility': 'Sole traders and limited companies. Metro Bank BCA required. Must apply in branch.',
        },
        'hsbc': {
            'fit_label': 'Worth considering if you already bank with HSBC',
            'summary_strip': '22% APR &middot; 15.9% purchase rate &middot; &pound;32 fee waived year 1',
            'verdict': 'Competitive purchase rate at 15.9%, but the annual fee pushes the representative APR to 22%. Not worth switching banks for.',
            'editorial_heading': 'Low purchase rate for existing HSBC customers, but the fee sticks after year one',
            'best_for': 'Existing HSBC business customers who want a low purchase rate without switching banks',
            'watch_out': 'The &pound;32 fee is not waivable after year 1 regardless of spend. FX fee is 2.99%.',
            'not_ideal': 'You don&rsquo;t already have an HSBC business account &mdash; the rate doesn&rsquo;t justify switching',
            'eligibility': 'HSBC business current account required. Credit limits from &pound;500.',
        },
        'santander': {
            'fit_label': 'Best fee structure for multi-cardholder teams',
            'summary_strip': '23.7% APR &middot; 18.9% purchase rate &middot; &pound;30 flat fee covers all cardholders',
            'verdict': 'Single &pound;30 fee covers all cardholders. If you&rsquo;re issuing cards to 3&ndash;4 employees, the per-account fee structure changes the total cost calculation entirely.',
            'editorial_heading': 'The fee structure advantage is real if you need multiple cards, but the APR is mid-table',
            'best_for': 'Teams issuing 3+ employee cards &mdash; the flat &pound;30 fee is materially cheaper than per-card pricing',
            'watch_out': 'Restricted to Santander 1|2|3 BCA holders. Personal guarantees required for LTDs and LLPs.',
            'not_ideal': 'You only need one card and don&rsquo;t benefit from the per-account fee structure',
            'eligibility': 'Santander 1|2|3 or Business Current Account required. Max 2 directors/partners who fully own the business. Credit limits &pound;500&ndash;&pound;25,000.',
        },
        'natwest': {
            'fit_label': 'Best for overseas card spend',
            'summary_strip': '24.3% APR &middot; 16.9% purchase rate &middot; &pound;30 fee waived at &pound;6k+ spend',
            'verdict': 'Low purchase rate, but total cost rises quickly if you need multiple employee cards.',
            'editorial_heading': 'The FX fee advantage is genuine, but the per-cardholder fee stacks up with team size',
            'best_for': 'Businesses already banking with NatWest that make overseas card purchases regularly',
            'watch_out': '&pound;30 fee per cardholder unless you hit &pound;6k+ annual spend per card',
            'not_ideal': 'You need multiple employee cards and won&rsquo;t hit the spend waiver on each',
            'eligibility': 'Turnover under &pound;2m. NatWest BCA required. Credit limits from &pound;500.',
        },
        'barclaycard': {
            'fit_label': 'Only option without an existing account requirement',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; No existing account required',
            'verdict': 'The highest APR on this list, but the only card you can get without switching your business bank account.',
            'editorial_heading': 'Open access is the selling point, but 25.5% is the price you pay for it',
            'best_for': 'Businesses on Starling, Tide, or other non-traditional banks who can&rsquo;t access the cards above',
            'watch_out': '25.5% is the highest rate on this list. The open access comes at a cost if you carry a balance.',
            'not_ideal': 'You already have a BCA with one of the banks above and could get a lower rate',
            'eligibility': 'Sole traders, partnerships, LTDs with &pound;10k&ndash;&pound;6.5m turnover. No existing account required.',
        },
        'capital_on_tap': {
            'fit_label': 'Listed separately &mdash; floor-rate pricing, not representative APR',
            'summary_strip': 'From 13.86% floor APR &middot; No annual fee (free card) &middot; No existing account required',
            'verdict': 'Advertises rates &ldquo;from 13.86%&rdquo;, but that&rsquo;s a floor rate. The actual representative APR is significantly higher.',
            'editorial_heading': 'The floor rate is eye-catching, but most applicants will be offered something much higher',
            'best_for': 'UK limited companies needing high credit limits (up to &pound;250,000) and no FX or ATM fees',
            'watch_out': 'Average rate offered Oct&ndash;Dec 2025 was 46.05% per Capital on Tap&rsquo;s own data. Most applicants won&rsquo;t get the floor rate.',
            'not_ideal': 'You&rsquo;re a sole trader (not accepted), or you assume the advertised floor rate is what you&rsquo;ll get',
            'eligibility': 'UK limited companies and LLPs only. Min turnover &pound;24,000/year. Must be registered at Companies House.',
        },
    },

    # Page sections in display order
    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        # Verdict box
        {'type': 'verdict_box',
         'text': 'The promotional 0% period ends. When it does, the standard purchase APR is the rate you pay on every pound of balance you carry. The figures below are from each provider&rsquo;s current pricing page, verified March 2026. If you carry a balance, this is the number that determines your real borrowing cost.'},

        {'type': 'hero_zone'},

        # Intro
        {'type': 'prose', 'paragraphs': [
            'If you clear your balance in full every month, APR is irrelevant to you. A <a href="/business-credit-cards/best-cashback-and-reward/">cashback</a> or <a href="/business-credit-cards/best-cashback-and-reward/">rewards card</a> will deliver more value. If you carry a balance &mdash; whether by design or because cash flow means you occasionally can&rsquo;t clear &mdash; the ongoing purchase rate is your real cost of borrowing.',
            'This page covers UK business credit cards with the lowest standard purchase APR, verified against each provider&rsquo;s pricing page in March 2026. Introductory 0% offers and rewards-driven cards are excluded where a higher APR is the trade-off for points or perks.',
        ]},

        {'type': 'toc_start'},

        {'type': 'heading', 'level': 2, 'text': 'APR Comparison at a Glance'},
        {'type': 'prose', 'paragraphs': [
            'A plumbing business carrying &pound;5,000 pays &pound;798 a year at Lloyds versus &pound;1,275 at Barclaycard &mdash; a &pound;477 gap on the same balance. But the Lloyds card requires you to bank with Lloyds. Your bank relationship decides the rate you can access.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'lloyds': {'text': 'Top Pick', 'color': 'top'},
                'hsbc': {'text': 'Low Purchase Rate', 'color': 'gold'},
                'barclaycard': {'text': 'Open Access', 'color': 'pink'},
                'natwest': {'text': 'Next Lowest', 'color': 'teal'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': (
                'Rates verified against provider pricing pages, 20 March 2026. '
                'All rates are variable and may change after publication.'
            ),
        }},

        # Keep / Switch / Look Elsewhere
        {'type': 'heading', 'level': 2, 'text': 'Keep Your Current Card, Switch to Low APR, or Look Elsewhere'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Your situation</th><th>Focus on</th></tr></thead>'
            '<tbody>'
            '<tr><td>You clear in full every month</td><td>Cashback or rewards rate, not APR</td></tr>'
            '<tr><td>You carry a balance most months</td><td>Lowest representative APR you can access</td></tr>'
            '<tr><td>You sometimes carry a balance</td><td>Low APR plus no or waivable annual fee</td></tr>'
            '<tr><td>You need a large purchase facility</td><td>Credit limit ceiling and repayment flexibility</td></tr>'
            '</tbody></table>'},

        # What Representative APR Means
                {'type': 'heading', 'level': 2, 'text': 'What &ldquo;Representative APR&rdquo; Means for Your Application'},

        {'type': 'prose', 'paragraphs': [
            'A representative APR is the rate that at least 51% of successful applicants receive. That means up to 49% may be offered a higher rate, and the provider is under no obligation to tell you the ceiling before you apply.',
            'Several providers on this list do not publish the upper end of their rate range. Where a card shows a single representative APR with no published range, you have less visibility of the rate you&rsquo;ll actually be offered. We&rsquo;ve noted this in each card&rsquo;s entry below.',
            'If your business has a short trading history, thin credit file, or you&rsquo;re applying as a sole trader, expect to be offered a rate above the headline figure. The representative APR is a useful ranking tool, but it is not a guarantee of the rate you&rsquo;ll get.',
        ]},

        # Section divider + card list
        {'type': 'divider', 'label': 'Detailed reviews'},
        {'type': 'heading', 'level': 2, 'text': 'The Low-APR Business Credit Cards'},
        {'type': 'prose', 'paragraphs': [
            'Ordered by representative APR, lowest first. Capital on Tap is listed separately after the comparison table because it advertises a floor rate rather than a representative APR, which makes direct comparison misleading.',
        ]},
        {'type': 'card_list'},

        # Capital on Tap (separate)
        {'type': 'heading', 'level': 2, 'text': 'Not Directly Comparable: Capital on Tap'},
        {'type': 'prose', 'paragraphs': [
            'Capital on Tap uses floor-rate pricing rather than a single representative APR. Including it in the ranked table above would suggest a like-for-like comparison that doesn&rsquo;t hold. We&rsquo;ve listed it separately so you can assess it on its own terms.',
        ]},
        {'type': 'card_list_separate'},

        # Total Annual Cost section
        {'type': 'heading', 'level': 2, 'text': 'Total Annual Cost: APR + Fees at Different Balances'},
        {'type': 'prose', 'paragraphs': [
            'Headline APR tells you part of the story. The actual cost of carrying a balance depends on the APR, the annual fee, and whether you qualify for a fee waiver. We calculated the total annual cost for each card at three different average carried balances so you can see which card is genuinely cheapest for your situation.',
            'These figures assume you carry the stated average balance throughout the year. In practice, your balance will fluctuate month to month. But the comparison shows you how the fee structure changes the ranking at different balance levels.',
        ]},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Card</th><th>APR</th><th>Annual fee</th><th>Total cost at &pound;2,000 avg balance</th><th>Total cost at &pound;5,000 avg balance</th><th>Total cost at &pound;10,000 avg balance</th></tr></thead>'
            '<tbody>'
            '<tr><td>Lloyds</td><td>15.95%</td><td>&pound;32 (waivable at &pound;6k+ spend)</td><td>&pound;351</td><td>&pound;830</td><td>&pound;1,627</td></tr>'
            '<tr><td>Metro Bank</td><td>18.9%</td><td>&pound;0</td><td>&pound;378</td><td>&pound;945</td><td>&pound;1,890</td></tr>'
            '<tr><td>HSBC</td><td>22%</td><td>&pound;32</td><td>&pound;472</td><td>&pound;1,132</td><td>&pound;2,232</td></tr>'
            '<tr><td>Santander</td><td>23.7%</td><td>&pound;30 (covers all cards)</td><td>&pound;504</td><td>&pound;1,215</td><td>&pound;2,400</td></tr>'
            '<tr><td>NatWest</td><td>24.3%</td><td>&pound;30 (waivable at &pound;6k+ spend)</td><td>&pound;516</td><td>&pound;1,245</td><td>&pound;2,460</td></tr>'
            '<tr><td>Barclaycard</td><td>25.5%</td><td>&pound;0</td><td>&pound;510</td><td>&pound;1,275</td><td>&pound;2,550</td></tr>'
            '</tbody></table>'},
        {'type': 'prose', 'paragraphs': [
            '<em>Total cost = (average balance &times; APR) + annual fee. Lloyds and NatWest fees shown as paid (not waived) for conservative comparison. If you hit the spend waiver, subtract &pound;32 or &pound;30 respectively. Metro Bank and Barclaycard have no annual fee. All figures are annual estimates based on a constant average balance.</em>',
            'The key insight from this table: at a &pound;2,000 average balance, the difference between the cheapest card (Lloyds at &pound;351 including fee) and Metro Bank (&pound;378 with no fee) is just &pound;27. If you do not hit the Lloyds &pound;6k spend waiver, Metro Bank is the cheaper option. At &pound;5,000 average balance, Lloyds pulls ahead by &pound;115 because the fixed fee becomes a smaller proportion of the total cost.',
            'Barclaycard is an interesting case. At &pound;2,000 average balance, it costs &pound;510 &mdash; nearly &pound;160 more than Lloyds. But Barclaycard is the only card on this list that does not require an existing bank account. If you bank with Starling, Tide, or Monzo and cannot access the other cards, the &pound;160 premium is the cost of open access. We think that is worth knowing before you assume Barclaycard is simply overpriced.',
        ]},

        # What the Rate Comparison Alone Misses
        {'type': 'heading', 'level': 2, 'text': 'What the APR Comparison Alone Misses'},
        {'type': 'prose', 'paragraphs': [
            'APR is the right primary filter when ongoing balance-carrying cost is your decision. We reviewed the full cost picture and it isn&rsquo;t the only factor.',
            'Annual or monthly card fees add fixed cost that matters at lower spend volumes. A card with a 15.95% APR and a &pound;32 annual fee may cost you more than a card at 18.9% with no fee, depending on the balance you carry and whether you hit the spend threshold to waive the fee. The total annual cost table above makes this concrete.',
            'Foreign transaction fees matter if your business spends internationally. Most cards here charge around 2.99% on non-sterling transactions. NatWest charges nothing on overseas purchases, which is a meaningful difference for businesses with regular overseas card spend. At &pound;10,000 of overseas spend per year, the FX fee on most cards adds &pound;299 to your total cost &mdash; more than the annual card fee. We recommend running the numbers for your own spend pattern rather than relying on APR alone. For overseas spend, see our <a href="/business-credit-cards/what-are-the-best-business-credit-cards-for-travel/">travel business credit cards</a> page.',
            'Per-cardholder versus per-account fee structures change the maths with team size. Santander&rsquo;s &pound;30 covers all cardholders. NatWest and Lloyds charge per cardholder, waivable per card with sufficient spend. If you&rsquo;re issuing cards to four or five team members, that fee structure changes the total cost calculation entirely. A team of four on NatWest at &pound;30 per card costs &pound;120 in fees. The same team on Santander costs &pound;30 total. At lower individual spend volumes where the fee waiver is not triggered, Santander saves you &pound;90 per year in fees alone.',
        ]},

        # Who Low-APR Cards Don't Suit
        {'type': 'heading', 'level': 2, 'text': 'Who Low-APR Cards Don&rsquo;t Suit'},
        {'type': 'prose', 'paragraphs': [
            'Monthly clearers should stop here. A <a href="/business-credit-cards/best-cashback-and-reward/">cashback or rewards card</a> will deliver more value to you than the lowest APR. We checked the rewards programmes across the market and the cards with the best earn rates carry higher APRs, but if interest never accrues, the APR is irrelevant.',
            'High credit limits are a different constraint. The ranked cards above cap at &pound;25,000. Capital on Tap (listed separately below the table) offers up to &pound;250,000, but only for qualifying limited companies and LLPs, and its actual representative APR is significantly higher than the floor rate it advertises. We cover Capital on Tap in detail in our <a href="/business-credit-cards/capital-on-tap-review/">Capital on Tap review</a>.',
            'Newer businesses face a harder version of this problem. Most providers on this list don&rsquo;t publish a hard minimum trading requirement, but lenders will apply stricter criteria to businesses under 12 months old. The rate you&rsquo;re offered may be well above the representative APR. Prepare for the possibility that the advertised rate isn&rsquo;t the rate you&rsquo;ll get.',
        ]},

        # How to Compare Before You Apply
        {'type': 'heading', 'level': 2, 'text': 'How to Compare Before You Apply'},
        {'type': 'prose', 'paragraphs': [
            'We recommend checking three things beyond the representative APR:',
        ]},
        {'type': 'list', 'html':
            '<ol>\n'
            '    <li>Whether the card is restricted to existing customers of that bank. Most on this list are.</li>\n'
            '    <li>Whether a rate range is published alongside the representative figure. Some aren&rsquo;t, which means you have less visibility of what you&rsquo;ll actually be offered.</li>\n'
            '    <li>Whether the fee is per cardholder or per account. If you need multiple cards, this changes the total cost ranking.</li>\n'
            '</ol>'},
        {'type': 'prose', 'paragraphs': [
            'In our editorial view, the existing-account requirement is the biggest practical filter on this list. Five of the six ranked cards require a business current account with that bank. If you don&rsquo;t already have one, your realistic options narrow to Barclaycard (at the highest APR on this list) or Capital on Tap (with its significantly higher actual rates). That constraint matters more than any rate difference between the cards you can&rsquo;t access.',
            'A worked example of the decision process: you run a plumbing business banking with Tide (a digital bank with no business credit card). Your average carried balance is &pound;3,000. You cannot access Lloyds (15.95%), Metro Bank (18.9%), HSBC (22%), Santander (23.7%), or NatWest (24.3%) without opening a new business current account. Your options are Barclaycard at 25.5% (&pound;765/year in interest) or switching your business bank to access a lower rate. Switching to Lloyds would save you roughly &pound;287/year in interest. Whether that saving justifies the hassle of changing your business banking depends on how long you expect to carry the balance.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Will You Get the Representative APR?'},
        {'type': 'prose', 'paragraphs': [
            'Not necessarily. The representative APR is the rate offered to at least 51% of approved applicants. If your business has a thin credit history, a short trading record, or you are a sole trader applying for the first time, you are more likely to fall into the 49% who receive a higher rate. We checked each provider and none of them publish the upper bound of their rate range for business credit cards.',
            'There is no soft-search pre-qualification tool for most UK business credit cards. Unlike personal credit cards, where you can check your eligibility without affecting your credit score, most business card providers run a hard credit check at application. That means each application leaves a mark on your credit file. We recommend applying for the card most likely to accept you at a competitive rate rather than applying for multiple cards to find the best offer.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Should You Switch Banks Just for a Lower APR?'},
        {'type': 'prose', 'paragraphs': [
            'It depends on how much you carry and for how long. If your average carried balance is &pound;2,000, the difference between Lloyds at 15.95% and Barclaycard at 25.5% is roughly &pound;191 per year. If you expect to carry that balance for two years, the cumulative saving of &pound;382 may justify the effort of opening a Lloyds business current account.',
            'But switching banks is not free. You lose any switching incentives, need to update direct debits and supplier payment details, and the credit card application itself is not guaranteed. We think switching banks for the card rate alone only makes sense if you expect to carry a significant balance (&pound;3,000+) for 12 months or more. For shorter-term balance carrying, the Barclaycard open-access route with its higher APR may be the more practical choice.',
        ]},

        # Methodology and Disclosure
        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/best-cashback-and-reward/">Cashback and reward cards</a></li>\n'
            '    <li><a href="/business-credit-cards/what-are-the-best-business-credit-cards-for-travel/">Travel business credit cards</a></li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Low-APR FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'What is the lowest APR business credit card in the UK?',
                'a': 'As of March 2026, Lloyds offers the lowest representative APR at 15.95%. It requires a Lloyds business current account. Metro Bank offers 18.9% with no annual fee but requires a branch visit. Check current rates directly with each provider before applying.',
            },
            {
                'q': 'Will I get the representative APR advertised?',
                'a': 'Not necessarily. The representative APR is the rate offered to at least 51% of successful applicants. Up to 49% may receive a higher rate. If your business has a short trading history or thin credit file, expect to be offered above the headline figure.',
            },
            {
                'q': 'Does a low APR matter if I pay my balance in full each month?',
                'a': 'No. If you clear the full balance by each statement due date, you pay no interest regardless of the APR. In that case, a cashback or rewards card will deliver more value than a low-APR card.',
            },
            {
                'q': 'Is the annual fee included in the representative APR?',
                'a': 'Yes. The representative APR calculation includes the effect of any annual fee on the total cost of borrowing. A card with a lower purchase rate but a &pound;32 annual fee may show a higher representative APR than its purchase rate alone suggests.',
            },
            {
                'q': 'Should I switch my business bank account to get a lower APR?',
                'a': 'It depends on your balance and how long you plan to carry it. At a &pound;3,000 average balance, the difference between Lloyds at 15.95% and Barclaycard at 25.5% is roughly &pound;287 per year. If you expect to carry that balance for 12 months or more, switching may justify the effort. For shorter-term borrowing, the hassle of changing banks may outweigh the saving.',
            },
            {
                'q': 'Can I negotiate a lower APR on my business credit card?',
                'a': 'Providers do not typically negotiate business credit card rates. The rate you are offered is based on the provider&rsquo;s assessment of your creditworthiness. Your best route to a lower rate is applying to a provider with a lower published representative APR, provided you meet their eligibility criteria.',
            },
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> All rates, fees, and eligibility criteria were verified against each provider&rsquo;s public pricing page on 20 March 2026. We source product data exclusively from provider websites, regulatory filings (FCA, Companies House), and official industry bodies (UK Finance, Bank of England).',
            '<strong>Rate type:</strong> All rates listed are variable. Providers may change them at any time after publication.',
            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral or affiliate fees from some of the card providers listed on this page. This does not affect our editorial rankings, which are based on verified rates and publicly available product data. Our methodology and ranking criteria are described above.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Credit products are subject to status and provider approval. We recommend comparing offers directly with providers before applying.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
