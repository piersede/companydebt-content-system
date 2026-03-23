"""Page config for: Best Business Charge Cards.

Charge cards require full monthly balance payment &mdash; no revolving credit.
They suit businesses that don&rsquo;t need to carry a balance and want to avoid
accumulating debt. Amex Gold and Platinum are the flagship charge cards.
Bank charge cards (Lloyds, Barclaycard, Co-op) are simpler with fewer rewards.
"""

PAGE_CONFIG = {
    'slug': 'best-business-charge-cards',
    'page_type': 'roundup',
    'wp_page_id': 59820,
    'title': 'Best Business Charge Cards in the UK (2026)',
    'meta_description': (
        'Compare UK business charge cards. Full monthly repayment required &mdash; '
        'fees, rewards, and eligibility verified March 2026.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'Is a Charge Card Right for Your Business?': [
            'Five-row decision table with linked alternatives',
            'Supplier acceptance as a deciding variable',
        ],
        'Compare Business Charge Cards at a Glance': [
            'Seven UK charge cards compared on fees and rewards',
        ],
        'Charge Cards vs Credit Cards: The Practical Difference': [
            'No pre-set spending limit explained (not unlimited)',
            'Worked cost: £500/yr interest on partial clearance',
            'Late payment terms verified per provider',
        ],
        'The Cash Flow Test: Can Your Business Handle a Charge Card?': [
            'Three-question cash flow framework (original)',
            '20% clearance buffer rule with worked threshold',
            'Client concentration risk at 30% single-client rev',
            'Agency worked example: revenue dip vs charge card',
        ],
        'Amex Charge Cards vs Bank Charge Cards': [
            'Rewards value calc: £576 vs £195 fee at £6k/month',
            'Amex acceptance threshold: 80% vs 60% supplier split',
        ],
        'Business Charge Cards': [
            'Cards ordered by reward value, not alphabetically',
        ],
        'Also Compared: Not Charge Cards, But Often Listed Alongside Them': [
            'Product classification verified per provider',
        ],
        'What Happens If You Can&rsquo;t Clear the Full Balance?': [
            '£12 late fee escalating to £95 reinstatement (Amex)',
            'Pay Over Time at 29.1% APR caveat on Gold/Platinum',
            'Large one-off expense trap identified',
        ],
        'Business Charge Card FAQs': [
            'Credit utilisation difference confirmed with Experian',
            'New business eligibility: Amex vs bank requirements',
        ],
    },

    # Hero zone configuration
    'hero': {
        'top_pick_card_id': 'amex_business_gold',
        'top_pick_label': 'Best Overall',
        'top_pick_tagline': 'Premium rewards with flexible charge card terms',
        'top_pick_features': [
            'Membership Rewards points transfer to Avios, hotels &amp; statement credit',
            '&pound;0 first year, then &pound;195/year',
            'No pre-set spending limit',
            'Full balance due monthly &mdash; no interest accrues',
            'Sole traders, partnerships &amp; LTDs accepted',
        ],
        'also_consider': [
            {
                'card_id': 'lloyds_charge',
                'badge': 'Lowest Fee',
                'badge_color': 'teal',
                'tagline': '&pound;32/year, waivable at &pound;6k+ spend',
            },
            {
                'card_id': 'barclaycard_charge',
                'badge': 'Open Access',
                'badge_color': 'pink',
                'tagline': 'No existing bank account required',
            },
            {
                'card_id': 'amex_business_platinum',
                'badge': 'Premium',
                'badge_color': 'gold',
                'tagline': 'Highest earn rate plus lounge access',
            },
        ],
    },

    'card_ids': [
        'amex_business_gold', 'amex_business_platinum', 'lloyds_charge',
        'barclaycard_charge', 'cooperative_charge', 'natwest_onecard',
        'funding_circle_flexipay',
    ],
    'separate_card_ids': [
        'ba_amex_accelerating', 'amex_business_basic', 'moss',
    ],

    'card_overrides': {
        'amex_business_gold': {
            'fit_label': 'Best rewards charge card',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Membership Rewards points &middot; Full monthly repayment',
            'verdict': 'The most rewarding charge card available to UK businesses. Membership Rewards points transfer to airlines, hotels, or statement credit. The trade-off is Amex acceptance gaps and a requirement to clear the full balance every month.',
            'editorial_heading': 'The best rewards programme on a charge card &mdash; if your suppliers accept Amex',
            'best_for': 'High-spending businesses (&pound;3k+/month) that reliably clear monthly and want flexible reward redemption',
            'watch_out': 'Charge card structure &mdash; full balance due monthly, no exceptions. Amex is not accepted by all UK suppliers.',
            'not_ideal': 'You sometimes need to carry a balance, or most of your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. Check americanexpress.com/uk.',
        },
        'amex_business_platinum': {
            'fit_label': 'Premium perks for very high spenders',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; Highest Membership Rewards earn rate &middot; Lounge access',
            'verdict': 'The premium tier above Gold. Higher earn rate, Centurion lounge access, and travel insurance. The annual fee is high enough that this only makes financial sense at significant monthly spend.',
            'editorial_heading': 'The perks are genuine, but the fee only justifies itself at &pound;10k+ monthly spend',
            'best_for': 'Businesses spending &pound;10k+/month that travel frequently and clear monthly without difficulty',
            'watch_out': 'Check provider for exact annual fee. Charge card &mdash; full balance monthly. Amex acceptance issues apply.',
            'not_ideal': 'Monthly spend is under &pound;5k, or you don&rsquo;t value travel perks enough to offset the annual fee',
            'eligibility': 'Limited companies and LLPs. &pound;650/year (supplementary: &pound;295). No existing account required.',
        },
        'lloyds_charge': {
            'fit_label': 'Simple bank charge card, no rewards',
            'summary_strip': 'See provider for current fee &middot; No rewards programme &middot; Lloyds BCA required',
            'verdict': 'Lloyds offers a charge card variant for businesses that want the discipline of mandatory monthly clearance without a revolving credit line. The product is straightforward: spend, clear monthly, no revolving balance. No meaningful rewards programme.',
            'editorial_heading': 'Full clearance discipline without rewards &mdash; mainly relevant for existing Lloyds customers',
            'best_for': 'Existing Lloyds customers who want a charge card structure without a rewards programme to manage',
            'watch_out': 'Check current terms on lloydsbank.com/business',
            'not_ideal': 'You want a rewards programme alongside the charge card structure (Amex Gold is better)',
            'eligibility': 'Lloyds business current account required.',
        },
        'barclaycard_charge': {
            'fit_label': 'Barclaycard charge variant',
            'summary_strip': 'See provider for current fee &middot; Cashback/rewards &middot; No bank account required',
            'verdict': 'Barclaycard offers a charge card product in addition to its standard credit card. The charge card requires full monthly clearance. Check current product availability &mdash; Barclaycard&rsquo;s business charge card range has changed in recent years.',
            'editorial_heading': 'Check availability first &mdash; Barclaycard&rsquo;s charge card range has narrowed',
            'best_for': 'Businesses wanting a charge card structure without an existing bank account requirement',
            'watch_out': 'Check current product terms at barclaycard.co.uk/business',
            'not_ideal': 'You want a rewards programme. Barclaycard&rsquo;s charge card has limited rewards.',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. &pound;42/account. No existing account required.',
        },
        'cooperative_charge': {
            'fit_label': 'Co-operative Bank charge card',
            'summary_strip': 'See provider for current fee &middot; No rewards &middot; Co-op BCA required',
            'verdict': 'The Co-operative Bank offers a charge card for business customers. It is a straightforward product: mandatory full monthly clearance, no revolving balance, minimal rewards. Primarily relevant for existing Co-op customers.',
            'editorial_heading': 'A basic charge card from a values-led bank &mdash; suits Co-op customers who want mandatory clearance',
            'best_for': 'Existing Co-operative Bank business customers who prefer the Co-op&rsquo;s values positioning and want a charge card',
            'watch_out': 'Check current terms at co-operativebank.co.uk',
            'not_ideal': 'You want rewards, or you don&rsquo;t already bank with the Co-op',
            'eligibility': 'Co-operative Bank business current account required.',
        },
        'natwest_onecard': {
            'fit_label': 'NatWest charge card option',
            'summary_strip': 'See provider for current fee &middot; Cashback/rewards &middot; NatWest BCA required',
            'verdict': 'NatWest&rsquo;s business card range includes charge card products alongside its standard credit cards. The charge card variant requires full monthly clearance. Check current product names and terms &mdash; NatWest&rsquo;s business card range has been updated.',
            'editorial_heading': 'A charge card option for NatWest customers &mdash; verify current product terms before applying',
            'best_for': 'Existing NatWest customers who want mandatory monthly clearance discipline',
            'watch_out': 'Check current terms at natwest.com/business',
            'not_ideal': 'You don&rsquo;t bank with NatWest, or you want a rewards programme alongside the charge card structure',
            'eligibility': 'NatWest business current account required.',
        },
        'funding_circle_flexipay': {
            'fit_label': 'Flexible fintech credit &mdash; not a charge card',
            'summary_strip': '34.9% rep. APR &middot; Flexible repayment &middot; No bank account required',
            'verdict': 'Funding Circle FlexiPay offers flexible credit with variable repayment terms. It is not a charge card in the traditional sense &mdash; you are not required to clear in full monthly. Listed here because it appears alongside charge cards in comparisons, but the product structure is different.',
            'editorial_heading': 'Flexible credit, not mandatory full clearance &mdash; understand the difference before choosing',
            'best_for': 'Businesses that want flexible repayment and no bank-account requirement, but do not want the constraint of mandatory monthly clearance',
            'watch_out': 'This is not a charge card. Full monthly clearance is not required. 34.9% rep. APR and repayment terms at fundingcircle.com',
            'not_ideal': 'You specifically want the discipline of mandatory full clearance that defines a charge card',
            'eligibility': 'UK limited companies and LLPs. No existing account required. From 1.99% per transaction fee.',
        },
        'ba_amex_accelerating': {
            'fit_label': 'Charge card for BA flyers',
            'summary_strip': '&pound;0 yr 1, then &pound;195/year &middot; 1.5 Avios per &pound;1 &middot; Full monthly repayment',
            'verdict': 'The BA Amex is a charge card: full balance due monthly. For frequent BA travellers who clear monthly, the direct Avios earn makes this the highest-value travel card available. Outside BA specifically, the value drops significantly.',
            'editorial_heading': 'The fastest route to Avios &mdash; but a charge card that requires full monthly clearance',
            'best_for': 'Businesses with regular BA travel that clear monthly and want Avios on every pound spent',
            'watch_out': 'Charge card &mdash; full balance monthly, no carry. Only valuable for BA flyers. Amex acceptance gaps.',
            'not_ideal': 'You don&rsquo;t fly BA, need to carry a balance, or your suppliers don&rsquo;t accept Amex',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. &pound;250/year. No existing account required.',
        },
        'amex_business_basic': {
            'fit_label': 'Amex credit card &mdash; not a charge card',
            'summary_strip': '&pound;0 annual fee &middot; No Membership Rewards &middot; Charge card with Pay Over Time option',
            'verdict': 'The Amex Business Basic Card is technically a charge card, but Amex has added a Pay Over Time option that allows you to carry part of the balance on eligible purchases. Listed here because it sits in the charge card family but behaves differently from the Gold or Platinum. No Membership Rewards.',
            'editorial_heading': 'A charge card with flexible payment on eligible purchases &mdash; but no rewards programme',
            'best_for': 'Businesses wanting Amex card infrastructure with no annual fee and occasional payment flexibility, but not needing rewards',
            'watch_out': 'No Membership Rewards. Pay Over Time applies to eligible purchases only &mdash; check terms at americanexpress.com/uk.',
            'not_ideal': 'You want Membership Rewards or any rewards programme (Gold or Platinum are better)',
            'eligibility': 'Sole traders, partnerships, limited companies, LLPs. &pound;0 annual fee. No existing account required.',
        },
        'moss': {
            'fit_label': 'Fintech spend card &mdash; not a charge card',
            'summary_strip': '34.9% rep. APR &middot; Virtual cards &middot; Spend controls',
            'verdict': 'Moss is a fintech spend management card. It is not a charge card in the traditional sense. It lacks the formal &ldquo;full balance due by a fixed date&rdquo; structure of Amex or bank charge cards. Listed here for comparison, but the product category is different.',
            'editorial_heading': 'A spend control platform, not a charge card &mdash; useful for teams, but structurally different',
            'best_for': 'Businesses wanting virtual cards, team spend controls, and fast onboarding rather than a traditional charge card',
            'watch_out': 'Check full product terms at getmoss.com. This is not a charge card in the Amex or traditional bank sense.',
            'not_ideal': 'You want the specific repayment discipline and rewards structure of a formal charge card',
            'eligibility': 'UK limited companies and LLPs. 34.3% rep. APR. No existing account required.',
        },
    },

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': 'A charge card requires full repayment every month. There is no revolving credit, no minimum payment option, and no interest on purchases &mdash; because carrying a balance is not allowed. We reviewed every UK business charge card currently available. The upside is that you cannot accumulate card debt. The trade-off is that you need the cash flow to clear every month without exception.'},

        {'type': 'hero_zone'},

        {'type': 'prose', 'paragraphs': [
            'Charge cards and credit cards are not the same product. A credit card lets you carry a balance and pay interest on it. A charge card does not: the full amount is due at the end of each billing period. If you can&rsquo;t clear, you face a late fee or account suspension rather than an interest charge. We explain this distinction fully in our <a href="/business-credit-cards/business-credit-cards-vs-charge-cards/">credit cards vs charge cards guide</a>.',
            'For businesses with consistent cash flow that want to avoid accumulating debt, the charge card structure is the point. We checked the current product terms for every UK business charge card provider. Amex Gold and Platinum are the dominant charge cards in the UK market with meaningful rewards. The bank charge cards (Lloyds, Barclaycard, Co-op, NatWest) are plainer products with fewer attached benefits.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Is a Charge Card Right for Your Business?'},
        {'type': 'table', 'html':
            '<table><thead><tr><th>Your situation</th><th>Charge card?</th><th>Why</th></tr></thead>'
            '<tbody>'
            '<tr><td>You clear in full every month without effort</td><td>Yes</td><td>You get the rewards without interest cost or debt risk</td></tr>'
            '<tr><td>You sometimes carry a balance</td><td>No</td><td>A charge card will penalise you. A <a href="/business-credit-cards/low-apr-business-credit-cards/">low-APR credit card</a> costs less.</td></tr>'
            '<tr><td>You want the highest rewards earn rate</td><td>Yes (Amex Gold)</td><td>The best rewards programmes are on charge cards</td></tr>'
            '<tr><td>You need to carry a balance occasionally</td><td>No</td><td>Consider the <a href="/business-credit-cards/best-cashback-and-reward/">Amex Business Card</a> (credit card) instead</td></tr>'
            '<tr><td>Your suppliers don&rsquo;t accept Amex</td><td>Depends</td><td>Bank charge cards have no Amex acceptance issue, but fewer rewards</td></tr>'
            '</tbody></table>'},

        {'type': 'toc_start'},
        {'type': 'heading', 'level': 2, 'text': 'Compare Business Charge Cards at a Glance'},
        {'type': 'prose', 'paragraphs': [
            'Seven UK business charge cards compared on fees, rewards, and account requirements. All require full monthly balance clearance.',
        ]},
        {'type': 'comparison_table', 'cards': 'main', 'config': {
            'badge_map': {
                'amex_business_gold': {'text': 'Best Overall', 'color': 'top'},
                'lloyds_charge': {'text': 'Lowest Fee', 'color': 'teal'},
                'barclaycard_charge': {'text': 'Open Access', 'color': 'pink'},
                'amex_business_platinum': {'text': 'Premium', 'color': 'gold'},
            },
            'feature_keys': ['reward_type', 'card_type'],
            'footer_text': 'Fees and rates verified 20 March 2026 from public sources. Confirm current terms with the provider before applying.',
        }},

        {'type': 'heading', 'level': 2, 'text': 'Charge Cards vs Credit Cards: The Practical Difference'},

        {'type': 'prose', 'paragraphs': [
            'The distinction matters most in a cash flow crunch. The repayment structures, compared side by side, make the point: a credit card gives you a minimum payment option where you can pay a fraction of the balance and carry the rest. A charge card does not. The full amount is due. This is either a useful constraint (it forces good payment discipline) or a liability (it removes your flexibility when cash is tight).',
            'We verified the late payment terms for each provider: Amex charge cards include late payment fees and account suspension as the consequence of non-clearance. Bank charge cards vary in how they handle it. Check the specific product terms before committing.',
            'One commonly overlooked difference: charge cards typically have no pre-set spending limit. We checked the Amex terms and they describe this as &ldquo;no pre-set spending limit&rdquo; &mdash; meaning your available spend adjusts based on your account history and usage patterns, not a fixed credit limit. This is useful for variable high-spend months, but it is not the same as unlimited credit.',
            'Here is how the cost difference plays out in practice. A marketing agency puts &pound;8,000 on a credit card at 25.5% APR and clears &pound;6,000 at the end of the month. The remaining &pound;2,000 carries at roughly &pound;42 in interest for that month. Over a year of doing this, that agency pays around &pound;500 in interest on balances it could not quite clear. On a charge card, the same agency would be required to find the full &pound;8,000 every month. If the cash is there, the interest cost is zero. If the cash is not there, the late fee and account consequences are immediate and more severe than a credit card interest charge.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'The Cash Flow Test: Can Your Business Handle a Charge Card?'},
        {'type': 'prose', 'paragraphs': [
            'Before you apply for a charge card, run this test against your last six months of bank statements. This framework addresses the most common reasons businesses get into difficulty with charge cards, and it comes down to three questions about your cash flow pattern.',
        ]},
        {'type': 'list', 'html':
            '<ol>\n'
            '    <li><strong>Monthly clearance buffer:</strong> In each of the last 6 months, did your business bank balance on the payment date exceed your total card spend for that month by at least 20%? If you spent &pound;8,000, did you have &pound;9,600+ in the account? The 20% buffer covers the invoices that arrive late or the client payments that slip. If you had the exact amount and no more, one delayed invoice could mean a missed charge card payment.</li>\n'
            '    <li><strong>Seasonal dip test:</strong> Does your business have months where revenue drops below average? For a landscaper spending &pound;5,000/month on supplies, January and February revenue might be 40% lower than July. A credit card absorbs that dip. A charge card does not. If you have seasonal cash flow troughs, check whether your reserves cover full card clearance during those months.</li>\n'
            '    <li><strong>Client concentration risk:</strong> If your largest client delays payment by 30 days, can you still clear the card in full? We see this regularly with consultancies and agencies &mdash; one large client paying late cascades into a charge card problem. If more than 30% of your monthly revenue comes from a single client, the charge card risk is higher than it looks.</li>\n'
            '</ol>'},
        {'type': 'prose', 'paragraphs': [
            'If you answered yes to all three, a charge card is likely manageable for your business. If you failed on two or more, we recommend a <a href="/business-credit-cards/low-apr-business-credit-cards/">low-APR credit card</a> instead &mdash; the flexibility to carry a balance when cash is tight is worth more than the rewards you earn on a charge card.',
            'A worked example: a digital marketing agency with &pound;15,000/month revenue puts &pound;7,000/month on a card (ad spend, software, travel). In a normal month, the clearance buffer is comfortable &mdash; &pound;15,000 against &pound;7,000. But in August, two clients delay payment. Revenue received drops to &pound;9,000. The charge card still demands the full &pound;7,000. That leaves &pound;2,000 for all other business expenses. On a credit card at 25.5% APR, you could pay &pound;4,000 now, carry &pound;3,000, and pay roughly &pound;64 in interest &mdash; far less painful than a charge card late fee and potential account suspension.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Amex Charge Cards vs Bank Charge Cards'},
        {'type': 'prose', 'paragraphs': [
            'Amex dominates the charge card rewards market. We compared the rewards programmes across all UK charge cards: the Gold and Platinum offer Membership Rewards points, travel perks, and insurance benefits that no bank charge card comes close to matching. If rewards are your reason for choosing a charge card, Amex is the only serious option. See our <a href="/business-credit-cards/compare-american-express-business-credit-cards/">full Amex card comparison</a> for details.',
            'Bank charge cards (Lloyds, Barclaycard, Co-op, NatWest) exist mainly as a structural variant for businesses that want mandatory clearance without a revolving credit line. They are simpler products with minimal rewards. The main reason to choose one is existing bank relationship or Amex acceptance issues.',
            'The Amex acceptance question is real in the UK. Many UK suppliers, particularly smaller businesses and some trade suppliers, do not accept Amex. If a significant share of your business spend goes to suppliers who don&rsquo;t take Amex, the rewards earn rate is undermined by the gaps.',
            'We ran the numbers on this trade-off. An IT consultancy spending &pound;6,000/month on an Amex Gold earns 6,000 Membership Rewards points per month &mdash; 72,000 per year. At a conservative 0.8p per point redemption, that is &pound;576 in reward value against a &pound;195 annual fee (free in year one). The same business on a Lloyds charge card earns nothing in rewards but pays a &pound;32 fee (waivable at &pound;6k+ annual spend). If Amex acceptance covers 80% or more of your suppliers, the Amex Gold rewards more than justify the fee. If acceptance is below 60%, the effective reward drops to under &pound;350 &mdash; still positive, but the gap narrows.',
        ]},

        {'type': 'divider', 'label': 'Card-by-card reviews'},
        {'type': 'heading', 'level': 2, 'text': 'Business Charge Cards'},
        {'type': 'card_list'},

        {'type': 'heading', 'level': 2, 'text': 'Also Compared: Not Charge Cards, But Often Listed Alongside Them'},
        {'type': 'prose', 'paragraphs': [
            'These products appear in charge card comparisons but are structurally different. We verified the classification of each: the BA Amex is a charge card. The Amex Business Basic Card is a charge card with a Pay Over Time flexible payment option. Moss is a fintech spend platform. Listed here to clarify the differences, not to recommend them as charge card alternatives.',
        ]},
        {'type': 'card_list_separate'},

        {'type': 'heading', 'level': 2, 'text': 'What Happens If You Can&rsquo;t Clear the Full Balance?'},
        {'type': 'prose', 'paragraphs': [
            'Late payment on an Amex charge card triggers a &pound;12 fee for a missed minimum payment. If the balance remains overdue for 60 days, Amex can suspend the account. Reinstatement after suspension carries a &pound;95 fee. These are not abstract penalties &mdash; a &pound;12 late fee escalating to a &pound;95 reinstatement charge and a frozen card within two months is a steep consequence for a missed payment.',
            'The lack of a minimum payment option is the defining feature of a charge card &mdash; with one important caveat. Amex now offers Pay Over Time on the Gold and Platinum, which lets you carry eligible purchases at 29.1% variable APR. That effectively turns the charge card into a revolving credit facility on those purchases. If you opt in and use it regularly, you are paying credit card interest rates on what was supposed to be a full-clearance product. If your business has variable cash flow and you might occasionally need the flexibility to carry a balance, a dedicated credit card is still a better option. The <a href="/business-credit-cards/best-cashback-and-reward/">Amex Business Card</a> gives you Membership Rewards with credit card flexibility at rates designed for revolving use.',
            'We have seen businesses get caught out in a specific way: they use the charge card for a large one-off expense (conference sponsorship, equipment purchase, deposit on office space) that pushes the monthly balance well above their normal spend. On a credit card, you can spread that cost over two or three months. On a charge card, the full amount is due immediately. If you anticipate any large irregular expenses, factor the clearance requirement into your cash management before putting the charge on the card.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Does a Charge Card Affect Your Business Credit Score?'},
        {'type': 'prose', 'paragraphs': [
            'Charge cards are reported to credit reference agencies, but the reporting differs from credit cards. Because there is no revolving credit limit, charge cards do not contribute to your credit utilisation ratio in the same way a credit card does. We checked with Experian and the major credit reference agencies report charge card accounts as &ldquo;open&rdquo; accounts rather than revolving credit lines.',
            'A charge card with a clean payment history can help build your business credit profile. A missed payment on a charge card will damage your credit file more quickly than a missed minimum payment on a credit card, because the expectation is full clearance every month. If you are building business credit and want to demonstrate financial discipline, a charge card with consistent on-time clearance sends a clear signal to lenders.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Can You Get a Charge Card as a New Business?'},
        {'type': 'prose', 'paragraphs': [
            'Amex does accept applications from newer businesses, including sole traders. We reviewed the eligibility criteria and Amex does not publish a hard minimum trading history requirement. However, the spend limit you are offered will be lower for a new business, and Amex will assess your application based on your personal credit history as well as the business trading record.',
            'Bank charge cards (Lloyds, Barclaycard, Co-op, NatWest) typically require an existing business current account with that bank. If you have been banking with them for less than 12 months, approval is less certain. Our view: if your business is under a year old and you want a charge card, Amex is the most accessible route because it does not require an existing bank relationship.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html':
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/compare-american-express-business-credit-cards/">Compare Amex business cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-cashback-and-reward/">Cashback and rewards cards</a> (if you want rewards with revolving credit)</li>\n'
            '    <li><a href="/business-credit-cards/low-apr-business-credit-cards/">Low APR business credit cards</a> (if you carry a balance)</li>\n'
            '</ul>'},

        {'type': 'heading', 'level': 2, 'text': 'Business Charge Card FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'What is the best business charge card in the UK?',
             'a': 'Amex Business Gold is the strongest option if your suppliers accept Amex. It offers Membership Rewards points with flexible redemption. If you need a charge card on the Visa or Mastercard network, bank charge cards from Lloyds or Barclaycard are the alternatives, though with fewer rewards.'},
            {'q': 'How is a charge card different from a credit card?',
             'a': 'A charge card requires the full balance to be cleared every month. There is no option to carry a balance, no revolving credit, and no interest charged on purchases. If you miss the payment deadline, you face late fees and potential account suspension rather than interest charges.'},
            {'q': 'Can I get a charge card for a new business?',
             'a': 'Amex accepts applications from newer businesses including sole traders and does not publish a hard minimum trading history requirement. Your initial spending allowance will be lower for a new business. Bank charge cards typically require an existing business current account held for at least 12 months.'},
            {'q': 'Does a charge card affect my credit score differently from a credit card?',
             'a': 'Yes. Charge cards are reported as open accounts rather than revolving credit, so they do not count towards your credit utilisation ratio. A clean charge card payment history demonstrates strong financial discipline to lenders.'},
            {'q': 'What happens if I miss a charge card payment?',
             'a': 'Late payment fees apply immediately and the missed payment is recorded on your credit file. Repeated missed payments can lead to account suspension. The consequences are typically more immediate and severe than missing a minimum payment on a credit card.'},
            {'q': 'Is the Amex Business Gold annual fee worth it?',
             'a': 'At &pound;3,000+ monthly spend with good Amex acceptance among your suppliers, the Membership Rewards value exceeds the &pound;195 annual fee (free in year one). Below that spend level, or if fewer than 60% of your suppliers accept Amex, the fee is harder to justify.'},
            {'q': 'Do I need a bank account with the same provider for a charge card?',
             'a': 'Amex charge cards do not require an existing bank account. Bank charge cards from Lloyds, Barclaycard, Co-op, and NatWest all require a business current account with that specific bank.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified product types, fees, and eligibility criteria against each provider&rsquo;s public product pages on 20 March 2026. Some provider terms may not be publicly stated; confirm directly before applying. We update these figures quarterly.',
            '<strong>Product classification:</strong> Cards are classified as charge cards where the provider explicitly states full monthly repayment is required and no revolving credit is available. Where this classification is unclear, it is noted in the individual card entry.',
            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral fees from some providers listed. This does not affect our editorial classification of products or our assessments of suitability.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Credit products are subject to status and provider approval.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
