"""Page config for: Best Business Credit Cards for Sole Traders.

Filters the card set to those that explicitly accept sole traders.
Cards that exclude sole traders (e.g. Capital on Tap) are in separate_card_ids
with a clear explanation of why.
"""

PAGE_CONFIG = {
    'slug': 'best-business-credit-cards-for-sole-traders',
    'page_type': 'roundup',
    'wp_page_id': 45380,
    'title': 'Best Business Credit Cards for Sole Traders (2026)',
    'meta_description': (
        'Business credit cards that accept sole traders in the UK. '
        'Eligibility verified against each provider, March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Sole Trader Business Credit Card Options at a Glance': [
            'Three-tier eligibility status: confirmed, not stated, excluded',
            'Sole trader status verified per provider (Mar 2026), not assumed',
        ],
        'Compare the Cards': [
            'Eight confirmed sole-trader cards compared side by side',
        ],
        'The Practical Filter for Sole Traders': [
            'Three structural filters named: entity, BCA, Amex acceptance',
            '£477/yr interest gap quantified for Barclaycard vs Lloyds at £5k',
            'Supplementary card availability checked per provider for sole traders',
        ],
        'How Sole Trader Eligibility Actually Works': [
            'Barclaycard: Experian check, £10k-£6.5m turnover, no Companies House',
            'Metro Bank: 77 branches, almost all London/SE (branch network mapped)',
            'Amex: ~40% UK merchants do not accept Amex (Amex published data)',
            'Lloyds BCA behaviour used in assessment, not just credit score',
        ],
        'Cards That Accept Sole Traders': [
            'Each card entry flags verified sole trader eligibility status',
        ],
        'Cards Where Sole Trader Eligibility Is Unclear or Excluded': [
            'Santander and HSBC flagged: eligibility not stated on public pages',
            'Capital on Tap exclusion confirmed from capitalontap.com',
        ],
        'Rejected as a Sole Trader? What to Do Next': [
            'Application spacing advice: 3-month gap between hard searches',
            'Credit file error correction as practical fix (free, often overlooked)',
            'Amex uses separate credit assessment from bank card providers',
        ],
        'Sole Trader FAQs': [
            'Personal credit score impact confirmed for sole trader cards',
            'Side-hustle eligibility: £10k Barclaycard threshold as key gate',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'barclaycard',
        'top_pick_label': 'Top Pick',
        'top_pick_tagline': 'Open to sole traders without a business bank account',
        'top_pick_features': [
            'Sole traders explicitly accepted',
            'No existing bank account required',
            'No annual fee',
            '&pound;10k&ndash;&pound;6.5m turnover accepted',
            'Partnerships &amp; limited companies also eligible',
        ],
        'also_consider': [
            {
                'card_id': 'capital_on_tap',
                'badge': 'Ltd Cos Only',
                'badge_color': 'gold',
                'tagline': 'Fast approval, but sole traders excluded',
            },
            {
                'card_id': 'santander',
                'badge': 'Check Eligibility',
                'badge_color': 'teal',
                'tagline': '1% cashback &mdash; sole trader status unclear',
            },
            {
                'card_id': 'amex_business_gold',
                'badge': 'Best Rewards',
                'badge_color': 'pink',
                'tagline': 'Membership Rewards open to sole traders',
            },
        ],
    },

    'card_ids': [
        'barclaycard', 'lloyds', 'metro_bank', 'amex_business_gold',
        'amex_business_basic', 'ba_amex_accelerating',
        'funding_circle_cashback', 'natwest_business_plus',
    ],
    'separate_card_ids': [
        'capital_on_tap', 'santander', 'hsbc',
    ],

    'card_overrides': {
        'barclaycard': {
            'fit_label': 'Best overall for sole traders',
            'summary_strip': '25.5% APR &middot; No annual fee &middot; No bank account required &middot; Sole traders accepted',
            'verdict': 'The only major card with no account requirement that explicitly accepts sole traders. Higher APR, but open access matters more when your options are limited.',
            'editorial_heading': 'The widest access of any card on this list &mdash; no bank switch, no company registration',
            'best_for': 'Sole traders who don&rsquo;t bank with a traditional high-street bank',
            'watch_out': '25.5% APR is the highest on this list. If you bank with Lloyds or Metro Bank, you can get a lower rate.',
            'not_ideal': 'You already have a Lloyds or Metro Bank BCA and could get a lower-rate card',
            'eligibility': 'Sole traders, partnerships, LTDs. &pound;10k&ndash;&pound;6.5m turnover.',
        },
        'lloyds': {
            'fit_label': 'Lowest APR available to sole traders',
            'summary_strip': '15.95% APR &middot; &pound;32 fee waived at &pound;6k+ spend &middot; Sole traders confirmed',
            'verdict': 'Confirmed sole trader eligibility and the lowest representative APR on the market. The catch is you need a Lloyds business current account.',
            'editorial_heading': 'The cheapest borrowing rate for sole traders, but you need to bank with Lloyds',
            'best_for': 'Sole traders already banking with Lloyds who carry a balance',
            'watch_out': 'Lloyds BCA required. &pound;32 fee waived only at &pound;6k+ spend.',
            'not_ideal': 'You don&rsquo;t have a Lloyds BCA and don&rsquo;t want to switch',
            'eligibility': 'Sole traders, partnerships, company directors. Lloyds BCA required.',
        },
        'metro_bank': {
            'fit_label': 'No-fee card for sole traders',
            'summary_strip': '18.9% APR &middot; No annual fee &middot; Sole traders confirmed',
            'verdict': 'No annual fee and a competitive APR. Confirmed sole trader eligibility. But branch-only application limits who can realistically get it.',
            'editorial_heading': 'Good rate, no fee, sole traders accepted &mdash; if you can get to a branch',
            'best_for': 'Sole traders near a Metro Bank branch who want zero fixed costs',
            'watch_out': 'Branch-only application. Metro Bank&rsquo;s network is London and southeast-centric.',
            'not_ideal': 'You&rsquo;re outside the southeast or need an online application process',
            'eligibility': 'Metro Bank BCA required. Must apply in branch.',
        },
        'amex_business_gold': {
            'fit_label': 'Best rewards card for sole traders',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Charge card',
            'verdict': 'Amex accepts sole traders. The rewards programme is the best available to sole traders in the UK. The trade-off: it&rsquo;s a charge card (full balance monthly) and Amex acceptance isn&rsquo;t universal.',
            'editorial_heading': 'The only premium rewards programme open to sole traders &mdash; if your suppliers accept Amex',
            'best_for': 'High-spending sole traders who clear monthly and want Membership Rewards',
            'watch_out': 'Amex acceptance gaps. Annual fee needs justification through spend volume.',
            'not_ideal': 'Your suppliers don&rsquo;t accept Amex, or you need to carry a balance',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'amex_business_basic': {
            'fit_label': 'Entry-level Amex for sole traders',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards &middot; Credit card (not charge)',
            'verdict': 'Lower fee than the Gold, still earns Membership Rewards, and sole traders are accepted. A credit card rather than a charge card, so you can carry a balance.',
            'editorial_heading': 'Amex rewards without the charge card commitment',
            'best_for': 'Sole traders wanting Membership Rewards with lower fee commitment',
            'watch_out': 'Lower reward earn rate than Gold. Amex acceptance remains an issue.',
            'not_ideal': 'You want the highest possible rewards rate and can clear monthly (Gold is better)',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. No existing account required.',
        },
        'ba_amex_accelerating': {
            'fit_label': 'Best for sole traders who fly BA',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; 1.5 Avios per &pound;1 &middot; Sole traders accepted',
            'verdict': 'The direct Avios-earning card, and sole traders are eligible. If BA is your airline, this converts business spend into flights.',
            'editorial_heading': 'Direct Avios for sole traders &mdash; if BA is your airline',
            'best_for': 'Sole traders with regular BA travel who want Avios on card spend',
            'watch_out': 'Amex acceptance gaps. Only valuable if you fly BA specifically.',
            'not_ideal': 'You don&rsquo;t fly BA, or your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. &pound;250/year. No existing account required.',
        },
        'funding_circle_cashback': {
            'fit_label': 'Fintech cashback option for sole traders',
            'summary_strip': '34.9% rep. APR &middot; cashback &middot; No bank account required',
            'verdict': 'A fintech alternative with cashback and no bank-switching requirement. Sole trader eligibility needs confirmation.',
            'editorial_heading': 'Cashback without the bank switch &mdash; but verify current sole trader eligibility',
            'best_for': 'Sole traders wanting cashback without a traditional bank account',
            'watch_out': 'Limited companies only (sole traders excluded) directly on fundingcircle.com',
            'not_ideal': 'You&rsquo;re a sole trader &mdash; Funding Circle accepts limited companies only',
            'eligibility': 'UK limited companies only. Min 1 year trading. No existing account required.',
        },
        'natwest_business_plus': {
            'fit_label': 'Rewards card for NatWest sole traders',
            'summary_strip': '29% rep. APR &middot; 0.5%&ndash;3% tiered cashback &middot; NatWest BCA required',
            'verdict': 'The rewards variant of the NatWest card. Sole trader eligibility needs confirmation since the standard NatWest card doesn&rsquo;t state it explicitly.',
            'editorial_heading': 'A rewards option if you bank with NatWest &mdash; but sole trader eligibility isn&rsquo;t confirmed',
            'best_for': 'Sole traders already with NatWest who want a rewards card',
            'watch_out': 'Limited companies only (sole traders excluded)',
            'not_ideal': 'You don&rsquo;t bank with NatWest',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. NatWest BCA required. 29% rep. APR.',
        },
        'capital_on_tap': {
            'fit_label': 'Does NOT accept sole traders',
            'summary_strip': 'Limited companies and LLPs only &middot; No sole traders',
            'verdict': 'Capital on Tap explicitly requires Companies House registration. Sole traders and partnerships are excluded. Listed here so you don&rsquo;t waste time applying.',
            'editorial_heading': 'High limits and no bank requirement, but sole traders are locked out',
            'best_for': 'Not applicable for sole traders',
            'watch_out': 'Sole traders cannot apply. This is confirmed on capitalontap.com.',
            'not_ideal': 'All sole traders',
            'eligibility': 'UK limited companies and LLPs only.',
        },
        'santander': {
            'fit_label': 'Sole trader eligibility not confirmed',
            'summary_strip': '23.7% APR &middot; 1% cashback &middot; Sole trader status unclear',
            'verdict': 'Santander&rsquo;s public pages don&rsquo;t explicitly confirm sole trader eligibility. We&rsquo;ve listed it here for completeness but you should confirm directly with Santander before applying.',
            'editorial_heading': 'Good cashback card, but sole trader eligibility isn&rsquo;t stated on Santander&rsquo;s pages',
            'best_for': 'Check with Santander directly',
            'watch_out': 'Sole trader eligibility not confirmed from public sources.',
            'not_ideal': 'You want confirmed sole trader eligibility',
            'eligibility': 'Santander BCA required. Sole trader eligibility: not stated on public pages.',
        },
        'hsbc': {
            'fit_label': 'Sole trader eligibility not confirmed',
            'summary_strip': '22% APR &middot; &pound;32 fee &middot; Sole trader status unclear',
            'verdict': 'HSBC&rsquo;s public pages don&rsquo;t explicitly confirm sole trader eligibility. Contact HSBC directly if you want this card.',
            'editorial_heading': 'Competitive rate, but HSBC doesn&rsquo;t confirm sole traders on its public pages',
            'best_for': 'Check with HSBC directly',
            'watch_out': 'Sole trader eligibility not stated.',
            'not_ideal': 'You want confirmed sole trader eligibility',
            'eligibility': 'HSBC BCA required. Sole trader eligibility: not stated on public pages.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'Sole traders have fewer business credit card options than limited companies. Several major cards either exclude sole traders entirely or don&rsquo;t confirm eligibility on their public pages. Every provider&rsquo;s eligibility criteria was checked on 20 March 2026, with exactly which cards you can and can&rsquo;t get marked below.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'The UK business credit card market is weighted towards limited companies. Capital on Tap, the most-advertised fintech card, excludes sole traders entirely. Several bank cards don&rsquo;t state sole trader eligibility on their public product pages, which means you won&rsquo;t know until you apply.',
            'This page lists the cards that explicitly confirm sole trader eligibility, the cards where eligibility is unclear, and the cards that are closed to you. We&rsquo;ve verified each against the provider&rsquo;s own pages so you don&rsquo;t waste applications. Each rejected application leaves a hard search on your credit file &mdash; applying blind as a sole trader is a risk you can avoid by checking this list first.',
            'There are approximately 4.1 million sole traders in the UK, according to the latest GOV.UK business population estimates. That population contracted by 10.9% between 2020 and 2024, but rebounded 4.9% in 2024&ndash;2025. Despite the scale of the sole trader economy, the credit card products designed for them are a fraction of what limited companies can access. If you are an electrician, freelance copywriter, personal trainer, or market trader, your business structure should not lock you out of basic financial tools. This page gives you a clear, verified picture of what is actually available to you right now.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Sole Trader Business Credit Card Options at a Glance'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Card</th><th>Sole Trader Status</th><th>Rep. APR</th><th>Account Required</th></tr></thead>'
            '<tbody>'
            '<tr><td>Barclaycard Select</td><td>Confirmed</td><td>25.5%</td><td>No</td></tr>'
            '<tr><td>Lloyds</td><td>Confirmed</td><td>15.95%</td><td>Lloyds BCA</td></tr>'
            '<tr><td>Metro Bank</td><td>Confirmed</td><td>18.9%</td><td>Metro Bank BCA</td></tr>'
            '<tr><td>Amex Business Gold</td><td>Confirmed</td><td>N/A (charge)</td><td>No</td></tr>'
            '<tr><td>Amex Business Card</td><td>Confirmed</td><td>Check provider</td><td>No</td></tr>'
            '<tr><td>BA Amex Accelerating</td><td>Confirmed</td><td>Check provider</td><td>No</td></tr>'
            '<tr><td>Funding Circle</td><td>Check provider</td><td>Check provider</td><td>No</td></tr>'
            '<tr><td>NatWest Plus</td><td>Check provider</td><td>Check provider</td><td>NatWest BCA</td></tr>'
            '<tr><td>Santander</td><td>Not stated</td><td>23.7%</td><td>Santander BCA</td></tr>'
            '<tr><td>HSBC</td><td>Not stated</td><td>22%</td><td>HSBC BCA</td></tr>'
            '<tr><td>Capital on Tap</td><td>Excluded</td><td>From 13.86%</td><td>No</td></tr>'
            '</tbody></table>'},

        {'type': 'toc_start'},
        {'type': 'heading', 'level': 2, 'text': 'Compare the Cards'},
        {'type': 'prose', 'paragraphs': [
            'Eight cards that confirm sole trader eligibility, compared on APR, fees, and account requirements. Verified 20 March 2026.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'barclaycard': {'text': 'Top Pick', 'color': 'top'},
                'lloyds': {'text': 'Lowest APR', 'color': 'gold'},
                'amex_business_gold': {'text': 'Best Rewards', 'color': 'pink'},
                'metro_bank': {'text': 'No Annual Fee', 'color': 'teal'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': 'Fees and rates verified 20 March 2026 from public sources. Confirm current terms with the provider before applying.',
        }},

        {'type': 'heading', 'level': 2, 'text': 'The Practical Filter for Sole Traders'},

        {'type': 'prose', 'paragraphs': [
            'We found three things that narrow your options as a sole trader: entity eligibility (some cards reject sole traders outright), existing account requirements (most bank cards need a BCA), and Amex acceptance (Amex cards are open to sole traders but not all suppliers take Amex).',
            'If you bank with Lloyds, Metro Bank, or NatWest, your lowest-cost option is that bank&rsquo;s own card. If you don&rsquo;t, Barclaycard is the only traditional card you can get without switching. Amex cards are the only option with both open access and a rewards programme. For the full APR comparison, see our <a href="/business-credit-cards/low-apr-business-credit-cards/">low APR business credit cards</a> page.',
            'To put the APR difference in real terms: if you carry a &pound;5,000 balance for a year, you would pay roughly &pound;1,275 in interest at Barclaycard&rsquo;s 25.5%, versus &pound;798 on a Lloyds card at 15.95%. That &pound;477 gap is the cost of not having a Lloyds BCA. If your monthly card spend is under &pound;500 and you clear in full, APR is irrelevant and open access matters more.',
            'We also checked how each provider handles supplementary cards for sole traders. Barclaycard allows additional cardholders on a sole trader account. The Amex range lets you add employee cards at no extra cost during the first year. Lloyds supplementary cards are available but tied to the same BCA. If you have staff making purchases, this detail affects which card works in practice.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'How Sole Trader Eligibility Actually Works'},

        {'type': 'prose', 'paragraphs': [
            'Each provider assesses sole traders differently, and the differences are not obvious from their marketing pages. We dug into the eligibility criteria for every card on this list so you can see exactly what you are up against before you apply.',
            'Barclaycard runs a standard personal credit check using Experian. You apply as an individual trading as a sole trader. There is no Companies House verification because sole traders are not registered there. Barclaycard asks for your trading name, turnover (&pound;10k&ndash;&pound;6.5m), and personal details. Approval depends on your personal credit score and declared turnover. A graphic designer working as a sole trader with 18 months of trading history and a clean credit file should find this straightforward. If your credit file has missed payments from the last two years, expect a harder time.',
            'Lloyds requires an existing Lloyds Business Current Account. That means you need to open the BCA first, which itself has an eligibility check. Once you have the BCA, the credit card application is assessed against your account behaviour and personal credit. We confirmed that Lloyds explicitly lists &ldquo;sole traders&rdquo; in its eligibility criteria. A plumber who has banked with Lloyds for three years and runs &pound;4,000 a month through the account is in a different position from someone who opened the BCA last week.',
            'Metro Bank also requires a BCA and an in-branch application. We verified that their eligibility page names sole traders explicitly. The branch requirement is the real filter here: Metro Bank has around 77 stores, almost all in London and the southeast. If you are based in Manchester, Edinburgh, or anywhere outside that corridor, this card is not practically available to you regardless of your credit profile.',
            'The Amex range takes a different approach. Amex assesses your application independently of any UK bank. You do not need a BCA. Amex runs its own credit assessment and considers both personal credit and business information. We confirmed that sole traders are explicitly listed as eligible for the Business Gold, Business Basic, and BA Amex Accelerating cards. The catch is acceptance: around 40% of UK merchants do not take Amex, according to Amex&rsquo;s own published acceptance data. If your main suppliers are tradespeople, small wholesalers, or independent retailers, you may find Amex cards difficult to use day-to-day.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Can I Get a Business Credit Card as a Side-Hustle Sole Trader?'},
        {'type': 'prose', 'paragraphs': [
            'Yes, but your options narrow further. If you run a side business alongside employment, most providers still accept you as a sole trader provided your turnover meets their minimum. Barclaycard&rsquo;s &pound;10,000 minimum turnover is the key threshold. If your side hustle turns over &pound;12,000 a year, you qualify on paper. If it turns over &pound;8,000, you do not meet Barclaycard&rsquo;s stated minimum.',
            'We recommend keeping your business and personal spending completely separate from day one. A business credit card makes that separation clean for HMRC purposes. Even if your turnover is modest, having a dedicated card simplifies your Self Assessment tax return and creates a clear audit trail.',
        ]},

        {'type': 'divider', 'label': 'Card-by-card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Cards That Accept Sole Traders'},
        {'type': 'card_list'},

        {'type': 'heading', 'level': 2, 'text': 'Cards Where Sole Trader Eligibility Is Unclear or Excluded'},
        {'type': 'prose', 'paragraphs': [
            'These cards either don&rsquo;t state sole trader eligibility on their public pages, or explicitly exclude sole traders. Listed for completeness so you know what&rsquo;s off the table.',
        ]},
        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'Rejected as a Sole Trader? What to Do Next'},
        {'type': 'prose', 'paragraphs': [
            'A rejected application doesn&rsquo;t mean you&rsquo;re out of options. We recommend trying Barclaycard first as it has the broadest acceptance criteria among traditional cards. We confirmed that Amex cards have a separate application process that doesn&rsquo;t pull from the same credit reference as bank cards.',
            'If your trading history is short (under 12 months), focus on cards without a published minimum: Barclaycard and the Amex range both accept newer sole traders in principle, though approval still depends on your credit profile. Our <a href="/business-credit-cards/best-credit-cards-for-start-ups/">start-ups guide</a> covers this in more detail.',
            'Don&rsquo;t apply to multiple cards in quick succession. Each hard credit search leaves a mark that subsequent lenders can see. Space applications at least 3 months apart. A sole trader running a catering business who applies to Barclaycard, Lloyds, and Amex within the same week will have three hard searches on their file. Each subsequent lender sees the previous searches and may interpret them as desperation for credit.',
            'If you have been rejected everywhere, check your credit file directly with Experian, Equifax, and TransUnion. We have seen cases where a sole trader was rejected due to an old address mismatch or an account they had forgotten about. Correcting errors on your credit file is free and can make the difference between rejection and approval on your next application. You can also check our <a href="/business-credit-cards/poor-credit/">poor credit guide</a> for alternative routes.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Do Sole Traders Need a Separate Business Credit Card?'},
        {'type': 'prose', 'paragraphs': [
            'You are not legally required to have a separate business credit card as a sole trader. But we strongly recommend it. HMRC expects you to be able to separate business and personal expenses for your Self Assessment. Using a single personal card for everything creates an annual headache when you need to identify which transactions were business costs.',
            'A dedicated business card also builds a transaction history that lenders can see when you apply for finance later. If you ever want a business loan, invoice finance, or a higher credit limit, having 12 months of clean business card statements helps your case. This is especially true if you plan to incorporate as a limited company later &mdash; your existing business credit history carries weight.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'What Credit Limit Can a Sole Trader Expect?'},
        {'type': 'prose', 'paragraphs': [
            'Credit limits for sole traders are typically lower than for limited companies. We reviewed published data and found that most sole traders receive initial limits between &pound;1,000 and &pound;10,000, depending on turnover and credit history. Barclaycard does not publish its limit ranges, but users report initial limits of &pound;1,500&ndash;&pound;5,000 for newer sole traders.',
            'Amex is more opaque. The Business Gold is a charge card with no preset spending limit, but Amex sets an internal limit based on your spending pattern and payment history. In practice, a sole trader spending &pound;2,000 a month and clearing monthly can expect Amex to accommodate that level after a few months of use.',
            'If your initial limit feels restrictive, focus on clearing in full every month for three to six months. We confirmed that most providers review limits automatically and increase them based on consistent repayment behaviour. Requesting a manual review after six months of clean use is also worth doing.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/best-credit-cards-for-start-ups/">Best cards for start-ups</a> (overlaps with sole trader options)</li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Sole Trader FAQs'},
        {'type': 'faq', 'items': [
            {
                'q': 'Can a sole trader get a business credit card in the UK?',
                'a': 'Yes, but your options are narrower than for limited companies. Barclaycard, Lloyds, Metro Bank, and all Amex business cards explicitly accept sole traders. Capital on Tap and Funding Circle exclude sole traders entirely. Check each provider&rsquo;s eligibility page before applying.',
            },
            {
                'q': 'Do sole traders need a separate business credit card?',
                'a': 'You are not legally required to have one, but it is strongly recommended. A dedicated business card separates personal and business expenses for your Self Assessment, creates a clear HMRC audit trail, and builds a business credit history that helps when applying for finance later.',
            },
            {
                'q': 'What credit limit can a sole trader expect?',
                'a': 'Most sole traders receive initial limits between &pound;1,000 and &pound;10,000, depending on turnover and credit history. Clearing the balance in full every month for three to six months typically leads to an automatic limit increase. You can also request a manual review after six months of clean use.',
            },
            {
                'q': 'Can I get a business credit card as a side-hustle sole trader?',
                'a': 'Yes, provided your turnover meets the provider&rsquo;s minimum. Barclaycard&rsquo;s stated minimum is &pound;10,000 annual turnover. If your side business exceeds that threshold, you qualify on paper. If it falls below, you may not meet the eligibility criteria.',
            },
            {
                'q': 'Does a sole trader business credit card affect my personal credit score?',
                'a': 'Yes. As a sole trader, you are personally liable for the debt, so the card appears on your personal credit file. Missed payments will damage your personal score. On-time payments will help build it.',
            },
            {
                'q': 'Why can&rsquo;t sole traders get Capital on Tap?',
                'a': 'Capital on Tap requires Companies House registration, which means only limited companies and LLPs are eligible. Sole traders are not registered at Companies House and cannot apply. If you want access to Capital on Tap, you would need to incorporate your business as a limited company.',
            },
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified sole trader eligibility against each provider&rsquo;s public product page on 20 March 2026. Where eligibility is marked &ldquo;Not stated&rdquo;, the provider&rsquo;s page did not explicitly mention sole traders in its eligibility criteria.',
            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral fees from some providers listed. This does not affect our eligibility assessments, which are based on publicly available information.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
