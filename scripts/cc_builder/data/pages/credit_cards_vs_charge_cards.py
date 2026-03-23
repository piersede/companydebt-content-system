"""Page config for: Business Credit Cards vs Charge Cards.

Explains the structural difference between revolving credit cards and charge cards,
when each type makes sense, and the January 2026 Amex Gold change that blurs the line.
Prose-heavy with no card components. separate_card_ids for prose reference only.
"""

PAGE_CONFIG = {
    'slug': 'business-credit-cards-vs-charge-cards',
    'page_type': 'guide',
    'wp_page_id': 44987,
    'title': 'Business Credit Cards vs Charge Cards: What&rsquo;s the Difference? (2026)',
    'meta_description': (
        'Credit cards let you carry a balance. Charge cards require full monthly repayment. '
        'UK business options explained, including the January 2026 Amex Gold change.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'The Core Difference': [
            'Five-dimension comparison table: revolving credit, interest, limit, rewards, discipline',
            'No-pre-set-limit practical advantage for high-spend months explained',
        ],
        'When a Charge Card Makes More Sense': [
            '12-month self-test: one carried balance = charge card is a risk',
            'Missed charge card payment triggers fee plus credit file mark vs just interest',
        ],
        'When a Credit Card Makes More Sense': [
            'Recruitment consultancy scenario: 30-day billing vs weekly contractor pay mismatch',
            'Credit card as timing buffer, not borrowing tool — reframed for reader',
        ],
        'UK Business Charge Cards Available': [
            'Full UK charge card list: 6 products including Co-op and NatWest Onecard',
            'Most sites omit Lloyds, Co-op, and NatWest charge card variants',
        ],
        'The January 2026 Amex Gold Change: What It Means': [
            'Pay Over Time at 29.1% APR — turns Gold into a hybrid product',
            'Risk pattern: emergency feature quietly becomes default payment method',
            'Rate context: 29.1% vs Lloyds 15.95% and Barclaycard 25.5%',
        ],
        'The Hybrid: Flexible Payment Charge Cards': [
            'Broader trend: charge/credit binary being replaced by hybrid products',
            'Funding Circle FlexiPay as non-card alternative in same conceptual space',
        ],
        'Credit Cards vs Charge Cards FAQs': [
            'Credit file classification question re Amex Gold flex — flagged as unconfirmed',
        ],
    },

    'hero': {
        'top_pick_card_id': 'capital_on_tap',
        'top_pick_label': 'Best Credit Card',
        'top_pick_tagline': 'The leading standalone business credit card',
        'top_pick_features': [
            'Revolving credit line',
            '1% cashback on all spend',
            'No annual fee',
            'High limits up to &pound;250k',
        ],
        'also_consider': [
            {
                'card_id': 'amex_business_gold',
                'badge': 'Best Charge Card',
                'badge_color': 'gold',
                'tagline': 'Membership Rewards, full balance due monthly',
            },
            {
                'card_id': 'lloyds_charge',
                'badge': 'Lowest Fee',
                'badge_color': 'teal',
                'tagline': 'Basic charge card with no rewards',
            },
        ],
    },

    'card_ids': [],
    'separate_card_ids': [
        'amex_business_gold', 'amex_business_platinum', 'lloyds_charge',
        'barclaycard_charge', 'barclaycard', 'capital_on_tap',
        'funding_circle_flexipay',
    ],

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': (
             'Credit cards let you spread payments over time and carry a balance, paying interest on what you owe. '
             'Charge cards require the full balance to be cleared every month &mdash; no revolving credit, no interest, '
             'but a late payment fee if you miss the deadline. '
             'We reviewed the terms of every UK business card to identify which are charge cards and which are credit cards. '
             'For most small UK businesses, a credit card is the safer default. '
             'A charge card makes sense only if you are confident you will always clear the balance in full.'
         )},

        {'type': 'hero_zone'},

        {'type': 'toc_start'},

        {'type': 'prose', 'paragraphs': [
            'The distinction matters because the two product types suit very different cash flow situations. '
            'A charge card with Amex rewards looks attractive &mdash; until the month you can&rsquo;t clear '
            'the full balance and face a late payment penalty with no revolving option.',
            'This page explains the structural difference, lists the UK charge card options currently available, '
            'and covers the January 2026 Amex Gold change that introduced a flexible payment option to what '
            'was previously a strict charge card.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'The Core Difference'},
        {'type': 'table', 'html': (
            '<table>'
            '<thead><tr>'
            '<th>Feature</th>'
            '<th>Credit card</th>'
            '<th>Charge card</th>'
            '</tr></thead>'
            '<tbody>'
            '<tr>'
            '<td>Revolving credit?</td>'
            '<td>Yes</td>'
            '<td>No</td>'
            '</tr>'
            '<tr>'
            '<td>Interest charged?</td>'
            '<td>Yes, on carried balance</td>'
            '<td>No (late fees apply instead)</td>'
            '</tr>'
            '<tr>'
            '<td>Pre-set spending limit?</td>'
            '<td>Yes</td>'
            '<td>No (or very high)</td>'
            '</tr>'
            '<tr>'
            '<td>Rewards available?</td>'
            '<td>Yes, on some cards</td>'
            '<td>Yes, typically more generous</td>'
            '</tr>'
            '<tr>'
            '<td>Financial discipline required?</td>'
            '<td>Lower (can carry balance)</td>'
            '<td>Higher (must clear monthly)</td>'
            '</tr>'
            '</tbody>'
            '</table>'
        )},

        {'type': 'prose', 'paragraphs': [
            'The no-pre-set-limit feature on charge cards is a practical advantage for high-spending businesses. '
            'Amex Business Platinum, for example, adjusts its limit based on your spending history, '
            'which removes the ceiling that can create problems when a large legitimate purchase hits '
            'against a fixed credit limit.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'When a Charge Card Makes More Sense'},
        {'type': 'prose', 'paragraphs': [
            'A charge card is the stronger choice if you always clear your balance in full and want the highest '
            'possible rewards return. Earn rates across both card types confirm this: charge cards &mdash; '
            'particularly Amex Business Gold and Platinum &mdash; '
            'offer more generous Membership Rewards earn rates than most business credit cards. See our <a href="/business-credit-cards/best-business-charge-cards/">business charge card guide</a> for the full list.',
            'The card also suits businesses with high monthly spend that would regularly hit a credit card&rsquo;s '
            'fixed limit. Without a pre-set ceiling, a charge card handles large or irregular purchases '
            'more smoothly.',
            'A useful self-test: look at the last twelve months of business card spend. '
            'If you cleared the full balance every single month, a charge card is worth considering. '
            'If you carried a balance even once, the charge card model is a risk. '
            'One missed clearance on a charge card does not just cost you interest &mdash; it triggers a late payment fee and a black mark that future lenders will see.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'When a Credit Card Makes More Sense'},
        {'type': 'prose', 'paragraphs': [
            'A credit card is the right default for most small businesses. '
            'The ability to carry a balance &mdash; even if you rarely use it &mdash; provides a buffer '
            'that a charge card cannot. Cash flow is uneven for most businesses, '
            'and a month with a large upfront cost can make full monthly clearing difficult.',

            'Consider a recruitment consultancy that bills clients on 30-day terms but pays contractors weekly. '
            'In a good month, client payments arrive before the card statement is due. '
            'In a bad month &mdash; a client pays late, a big invoice slips &mdash; you need to carry &pound;8,000 '
            'for two weeks until the cash arrives. A credit card lets you do that at 20&ndash;25% APR on '
            'the carried portion. A charge card demands the full &pound;8,000 immediately and penalises '
            'you if it is not there. For your business, the credit card is not a borrowing tool &mdash; '
            'it is a timing buffer.',

            'If your suppliers do not accept Amex, the charge card comparison becomes moot: '
            'the main UK charge cards are Amex products, and Visa/Mastercard charge cards are limited. '
            'Barclaycard and Capital on Tap offer competitive Visa/Mastercard credit cards '
            'without an existing account requirement. See our <a href="/business-credit-cards/low-apr-business-credit-cards/">low-APR business credit card comparison</a> for the best rates.',

            'Start with a credit card unless you are certain &mdash; based '
            'on twelve months of actual cash flow, not projections &mdash; that you will clear in full '
            'every month. You can always switch to a charge card later once your payment pattern is established.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'UK Business Charge Cards Available'},
        {'type': 'prose', 'paragraphs': [
            'The UK business charge card market is small. The main options as of March 2026:',
        ]},
        {'type': 'list', 'html': (
            '<ul>\n'
            '    <li><strong>Amex Business Gold</strong> &mdash; Membership Rewards points, '
            'flexible payment option added January 2026 (see below). Check current annual fee at americanexpress.com/uk.</li>\n'
            '    <li><strong>Amex Business Platinum</strong> &mdash; Premium tier, higher earn rate, '
            'lounge access. Suits businesses spending &pound;10k+/month. Check current annual fee at americanexpress.com/uk.</li>\n'
            '    <li><strong>Lloyds Bank Business Charge Card</strong> &mdash; Simpler product, '
            'no rewards. Requires a Lloyds business current account.</li>\n'
            '    <li><strong>Barclaycard Business Charge Card</strong> &mdash; Limited availability, '
            'fewer features than Barclaycard&rsquo;s credit card range. Check current availability with the provider.</li>\n'
            '    <li><strong>Co-operative Bank Business Charge Card</strong> &mdash; Basic product, '
            'Co-op BCA required. Check current availability with the provider.</li>\n'
            '    <li><strong>NatWest Onecard</strong> &mdash; Charge card variant, NatWest BCA required. '
            'Check current terms with the provider.</li>\n'
            '</ul>'
        )},

        {'type': 'callout',
         'style': 'tip',
         'heading': 'Amex Business Gold: January 2026 change',
         'text': (
             'Amex added a flexible payment option to the Business Gold card in January 2026. '
             'Cardholders can now choose to pay a minimum amount each month on eligible purchases '
             'rather than clearing the full balance. '
             'This makes the Gold card a hybrid &mdash; charge card by default, '
             'with an optional revolving credit feature. '
             'Interest applies if you use the flexible option. '
             'Check current rate at americanexpress.com/uk before applying.'
         )},

        {'type': 'heading', 'level': 2, 'text': 'The January 2026 Amex Gold Change: What It Means'},
        {'type': 'prose', 'paragraphs': [
            'In January 2026, American Express added a &ldquo;Pay Over Time&rdquo; flexible payment option '
            'to the Business Gold card. We verified this against Amex&rsquo;s UK product pages: '
            'the card now functions as a charge card when you clear in full, '
            'and as a revolving credit card when you use the flexible payment option.',

            'This is a significant structural change. Before January 2026, if you had a bad month '
            'and could not clear the Gold card balance, you faced a late payment fee and a credit file mark. '
            'Now you can elect to pay a minimum amount on eligible purchases and carry the rest. '
            'That safety net did not exist before.',

            'The practical impact depends on how you use it. If you treat it as an emergency backstop '
            '&mdash; clearing in full in eleven months and using flexible payment in the one month '
            'where cash flow is tight &mdash; you get the best of both worlds. You earn Membership Rewards '
            'at charge card rates, avoid late payment penalties in difficult months, and pay interest '
            'only on the amount you defer.',

            'The numbers make the hybrid nature concrete. Pay Over Time carries a 29.1% variable APR. '
            'The minimum payment each month is the higher of &pound;50 or the full Flexible Payment Option balance. '
            'That means the Amex Gold is now functionally a hybrid: charge card by default, credit card if you opt in at 29.1%. '
            'For context, Lloyds offers 15.95% APR and Barclaycard sits at 25.5%. If you are using Pay Over Time regularly, '
            'you are paying a premium for the privilege of revolving on a product that was not designed for it.',
            'The risk is that the flexible option becomes a habit. We have seen this pattern with personal '
            'cards: a &ldquo;use only in emergencies&rdquo; feature quietly becomes the default payment method. '
            'If you use flexible payment every month, you have effectively converted your charge card into '
            'a credit card &mdash; but at 29.1% variable APR, which is not competitive with '
            'dedicated credit cards like Lloyds (15.95% APR) or even Barclaycard (25.5% APR).',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Does the Flexible Payment Option Change the Amex Gold&rsquo;s Credit File Classification?'},
        {'type': 'prose', 'paragraphs': [
            'This is a question we cannot answer definitively without Amex&rsquo;s confirmation. '
            'Traditionally, charge cards and credit cards appear differently on your business credit file. '
            'A charge card does not count as revolving credit, which can be an advantage if you '
            'are applying for a business loan. Whether the flexible payment option changes this classification '
            'is something you should confirm with Amex directly before applying, especially if your '
            'credit file profile matters for upcoming financing applications.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'The Hybrid: Flexible Payment Charge Cards'},
        {'type': 'prose', 'paragraphs': [
            'The Amex Gold change is part of a broader trend: the line between charge cards and credit cards '
            'is blurring. The traditional binary &mdash; you either clear in full or you revolve &mdash; '
            'is being replaced by hybrid products that let you choose each month.',

            'For you, the practical question is whether you want that flexibility or whether a clear '
            'boundary helps your financial discipline. Some business owners we have spoken to prefer '
            'the charge card constraint precisely because it removes the temptation to carry a balance. '
            'Others want the safety net. There is no universally correct answer &mdash; it depends on '
            'your cash flow pattern and your discipline.',

            'Funding Circle FlexiPay is a different product in the same conceptual space: '
            'it allows businesses to pay invoices now and repay in instalments. '
            'It is not a card product, but it serves a similar &ldquo;spread large payments&rdquo; need '
            'without requiring Amex acceptance. For a detailed review, see our '
            '<a href="/business-credit-cards/flexipay-review/">FlexiPay review</a>.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html': (
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-charge-cards/">Best business charge cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/best-cashback-and-reward/">Cashback and rewards cards</a></li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '    <li><a href="/business-credit-cards/what-is-a-balance-transfer-credit-card/">What is a balance transfer?</a></li>\n'
            '</ul>'
        )},

        {'type': 'heading', 'level': 2, 'text': 'Credit Cards vs Charge Cards FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'What happens if I can&rsquo;t pay my charge card balance in full?',
             'a': 'You face a late payment fee and a potential account suspension. Unlike a credit card, there is no minimum payment option. The missed payment is also recorded on your credit file, which can affect future borrowing.'},
            {'q': 'Is a charge card better than a credit card for building business credit?',
             'a': 'A charge card with a clean payment history demonstrates strong financial discipline. However, because charge cards have no revolving credit limit, they do not contribute to your credit utilisation ratio the same way a credit card does. Both build your business credit profile when paid on time.'},
            {'q': 'Does the Amex Business Gold flexible payment option make it a credit card?',
             'a': 'It makes it a hybrid. Since January 2026, Amex Gold lets you choose to carry part of the balance on eligible purchases. Interest applies on the deferred amount. It functions as a charge card when you clear in full and as revolving credit when you use the flexible option.'},
            {'q': 'Which UK business charge cards are currently available?',
             'a': 'The main options are Amex Business Gold, Amex Business Platinum, Lloyds Bank Business Charge Card, Barclaycard Business Charge Card, Co-operative Bank Business Charge Card, and NatWest Onecard. Amex cards are the only ones with meaningful rewards programmes.'},
            {'q': 'Can a sole trader get a business charge card?',
             'a': 'Yes. Amex Business Gold and Platinum accept sole traders. Bank charge cards (Lloyds, Barclaycard, Co-op, NatWest) require an existing business current account with that bank, which most sole traders can open.'},
            {'q': 'Do charge cards have a spending limit?',
             'a': 'Most charge cards have no pre-set spending limit. Amex describes this as a limit that adjusts based on your spending history and payment record. This is useful for variable or high-spend months, but it is not the same as unlimited credit.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified product terms against provider public pages on 20 March 2026. '
            'The Amex January 2026 flexible payment change was noted from Amex&rsquo;s UK communications. '
            'We update these figures quarterly. Confirm all details directly with each provider before applying.',
            '<strong>Affiliate disclosure:</strong> Company Debt may receive referral fees from some '
            'providers listed. This does not affect our editorial assessment of product terms or suitability.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
