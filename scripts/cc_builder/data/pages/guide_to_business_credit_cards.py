"""Page config for: Guide to Business Credit Cards.

Comprehensive explainer covering what a business credit card is, who needs one,
how to choose, key terms, and the existing-account problem. Prose-heavy with no
card components. separate_card_ids are referenced in prose only.
"""

PAGE_CONFIG = {
    'slug': 'guide-to-business-credit-cards',
    'page_type': 'guide',
    'wp_page_id': 44220,
    'title': 'Guide to Business Credit Cards (2026)',
    'meta_description': (
        'What a business credit card actually does, who needs one, and how to choose. '
        'Plain-English guide covering types, terms, and the existing-account problem.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'What a Business Credit Card Actually Does': [
            'Section 75 does not apply to business cards — widely misunderstood',
            'Four-person agency scenario showing operational benefit of additional cards',
        ],
        'Business vs Personal Credit Cards: The Real Differences': [
            'Four concrete differences: separation, credit building, liability, consumer protection',
            'GBP 500/month threshold for when a business card becomes worthwhile',
            'Chargeback is voluntary with shorter time limits vs Section 75 statutory right',
        ],
        'Credit Card vs Charge Card vs Corporate Card': [
            'Three-way comparison table with corporate card threshold (50+ employees)',
            'Jan 2026 Amex Gold flexible payment blurs charge card definition',
        ],
        'How to Choose a Business Credit Card': [
            'Four-question decision framework: balance, rewards, Amex acceptance, bank account',
        ],
        'The Bank Account Requirement for Business Credit Cards': [
            'Every major bank card requires existing BCA — verified per provider',
            'Barclaycard is the only traditional bank card without this requirement',
            'Fintech banking users limited to Barclaycard, CoT, and Amex range',
        ],
        'Business Credit Card Terms Explained': [
            'Representative APR means 51% floor — your rate may be higher',
            'Balance transfers functionally unavailable on UK business cards',
        ],
        'What to Check Before Applying for a Business Credit Card': [
            'Seven-item pre-application checklist covering overlooked eligibility filters',
        ],
        'Your First Business Credit Card: A Practical Checklist': [
            'Six-step sequenced checklist to avoid multiple hard searches',
            'GBP 3k/month threshold where rewards card returns become material',
            'Fintech underwriting explained: Open Banking + Companies House + bureau',
        ],
        'Business Credit Card Guide FAQs': [
            'Section 75 exclusion reiterated — chargeback is the only recourse',
        ],
    },

    'hero': {
        'top_pick_card_id': 'barclaycard',
        'top_pick_label': 'Recommended Starting Point',
        'top_pick_tagline': 'The most widely accessible business credit card',
        'top_pick_features': [
            'No annual fee',
            'No bank account required',
            'Cashback on eligible spend',
            'Widely accessible to most business types',
            'Visa network',
        ],
        'also_consider': [
            {
                'card_id': 'capital_on_tap',
                'badge': 'Fintech Alternative',
                'badge_color': 'gold',
                'tagline': 'Higher limits for limited companies',
            },
            {
                'card_id': 'lloyds',
                'badge': 'Lowest APR',
                'badge_color': 'teal',
                'tagline': 'Best rate if you bank with Lloyds',
            },
        ],
    },

    'card_ids': [],
    'separate_card_ids': [
        'barclaycard', 'capital_on_tap', 'lloyds', 'amex_business_gold',
        'ba_amex_accelerating',
    ],

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': (
             'A business credit card separates business spending from personal finances, '
             'builds a credit profile in the business name, and &mdash; depending on the card &mdash; '
             'earns rewards or keeps interest costs low. '
             'Most businesses with any regular card spend benefit from having one. '
             'The wrong choice is applying for a card without checking the existing-account requirement first: '
             'we checked every major provider and most bank cards require a business current account with the same provider.'
         )},

        {'type': 'hero_zone'},

        {'type': 'toc_start'},

        {'type': 'prose', 'paragraphs': [
            'The UK business credit card market has about a dozen mainstream options. '
            'Every major provider divides roughly by what they optimise for: '
            'low interest, rewards, or open access. '
            'The card that suits you depends on whether you carry a balance, which bank you use, '
            'and whether your suppliers accept Amex.',
            'This guide covers the core concepts before you compare cards. '
            'If you already know the basics, the <a href="/business-credit-cards/best-business-credit-cards/">full comparison</a> '
            'is a faster starting point.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'What a Business Credit Card Actually Does'},
        {'type': 'prose', 'paragraphs': [
            'A business credit card works like a personal credit card in most respects: '
            'the provider extends a credit limit, you spend against it, and you repay monthly. '
            'The key differences are that the account is in the business name, '
            'spending data feeds into a business credit file rather than a personal one, '
            'and Section 75 consumer protection under the Consumer Credit Act does not apply.',
            'Practically, this means you get a named account for business expenses, '
            'a statement that separates business from personal spend, '
            'and in most cases a separate credit limit from your personal cards. '
            'It does not automatically mean better terms &mdash; many business cards carry higher APRs than personal cards. '
            'If you are choosing a business card purely for a better rate, check that assumption before you apply.',
            'Additional cardholders are usually available, which is useful if you have employees '
            'making purchases on behalf of the business. '
            'Most providers charge a small fee per additional card or include a set number free.',

            'Here is how this works in practice: you run a four-person marketing agency. Your designer '
            'needs to buy stock photography (&pound;50/month), your account manager expenses client lunches '
            '(&pound;200/month), and you handle the software subscriptions (&pound;800/month). '
            'With a business credit card and additional cardholder cards, all of that appears on one statement, '
            'categorised by cardholder. Without it, you are chasing receipts from three people and '
            'reconciling personal card expenses against bank transfers. The operational simplicity is the '
            'underrated benefit.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Business vs Personal Credit Cards: The Real Differences'},
        {'type': 'prose', 'paragraphs': [
            'If you are a sole trader or small limited company, you might wonder whether you actually need a business credit card at all. Your personal card works at the same shops, earns the same type of rewards, and you already have one. Here are the practical differences that matter.',

            'First, separation. If HMRC audits your business, they want to see clean records. A business card gives you a single statement with only business transactions on it. Mixing personal and business spend on one card creates an accounting burden that grows every month. If you use accounting software like Xero or FreeAgent, a dedicated business card feed saves you hours of manual categorisation.',

            'Second, credit building. Spending on a business card builds a credit profile in the business name. If you plan to apply for a business loan, lease equipment, or take on commercial premises in the next two years, a business credit history helps. Personal card spending does not contribute to this.',

            'Third, liability. On a personal card, you are personally liable. On most small business cards, you are also personally liable &mdash; but the account is in the business name, which matters for record-keeping and can matter for liability structuring as your business grows.',

            'Fourth, consumer protection. Business credit cards do not benefit from Section 75 protection under the Consumer Credit Act 1974. This is a widely misunderstood point. Section 75 applies to personal credit card purchases between &pound;100 and &pound;30,000, but business cards fall outside its scope. If you need to dispute a purchase made on a business card, your recourse is through the card network&rsquo;s chargeback scheme (Visa or Mastercard), not the statutory protection that personal cards provide. Chargeback is a voluntary scheme with shorter time limits and no legal guarantee of outcome. Do not assume your business card carries the same buyer protection as your personal card.',

            'The bottom line: if you spend more than &pound;500 a month on business expenses, a dedicated business card saves you time and builds a financial profile for the business. If your business spend is genuinely minimal &mdash; under &pound;200 a month &mdash; a personal card with clear record-keeping may be sufficient.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Credit Card vs Charge Card vs Corporate Card'},
        {'type': 'table', 'html': (
            '<table>'
            '<thead><tr>'
            '<th>Type</th>'
            '<th>Revolving credit?</th>'
            '<th>Interest charged?</th>'
            '<th>Who it suits</th>'
            '</tr></thead>'
            '<tbody>'
            '<tr>'
            '<td>Credit card</td>'
            '<td>Yes</td>'
            '<td>Yes, if you carry a balance</td>'
            '<td>Businesses that occasionally need to spread payments</td>'
            '</tr>'
            '<tr>'
            '<td>Charge card</td>'
            '<td>No</td>'
            '<td>No (but late payment fees apply)</td>'
            '<td>Businesses that always clear monthly and want rewards</td>'
            '</tr>'
            '<tr>'
            '<td>Corporate card</td>'
            '<td>Varies</td>'
            '<td>Varies</td>'
            '<td>Larger organisations with centralised expense management</td>'
            '</tr>'
            '</tbody>'
            '</table>'
        )},

        {'type': 'definition',
         'term': 'Credit card',
         'definition': (
             'Extends a revolving credit limit. You can carry a balance from month to month, '
             'paying interest on the outstanding amount. '
             'Most UK business credit cards fall into this category. '
             'If you need the option to spread payments, this is what you want.'
         )},

        {'type': 'definition',
         'term': 'Charge card',
         'definition': (
             'Requires the full balance to be cleared every month. '
             'No revolving credit, no interest &mdash; but late payment fees apply if you miss the deadline. '
             'Charge cards typically have no pre-set spending limit, which suits high-spending businesses. '
             'Amex Business Gold and Platinum are the main UK examples. '
             'Since January 2026, Amex Gold has a flexible payment option that blurs this distinction slightly.'
         )},

        {'type': 'definition',
         'term': 'Corporate card',
         'definition': (
             'Issued to larger organisations (typically 50+ employees) rather than small businesses. '
             'Terms are negotiated directly with the provider. '
             'If you have fewer than 20 employees, you&rsquo;re almost certainly looking at a business credit '
             'or charge card, not a corporate card.'
         )},

        {'type': 'heading', 'level': 2, 'text': 'How to Choose a Business Credit Card'},
        {'type': 'prose', 'paragraphs': [
            'Four questions narrow the field before you look at any specific card.',
        ]},
        {'type': 'list', 'html': (
            '<ol>\n'
            '    <li><strong>Do you carry a balance?</strong> If yes, APR is the primary metric. '
            'The Lloyds card (15.95% representative APR) is the lowest available to most businesses. '
            'If no, the cost of borrowing is irrelevant and rewards become the deciding factor.</li>\n'
            '    <li><strong>Do you need rewards?</strong> If yes, Amex cards offer the strongest '
            'Membership Rewards programme. Santander and Capital on Tap offer cashback on Visa/Mastercard. '
            'If no, a no-fee card with a low APR is usually the cleaner choice.</li>\n'
            '    <li><strong>Do your suppliers accept Amex?</strong> Amex has acceptance gaps in the UK, '
            'particularly with smaller suppliers and some government bodies. '
            'If a significant share of your spend goes to suppliers who don&rsquo;t take Amex, '
            'Amex rewards won&rsquo;t translate to actual value.</li>\n'
            '    <li><strong>Do you have a traditional bank account?</strong> Most bank-issued cards require '
            'a business current account with the same provider. '
            'If you bank with a fintech (Starling, Monzo, Tide), your options narrow to Barclaycard, '
            'Capital on Tap, the Amex range, and a small number of fintech cards.</li>\n'
            '</ol>'
        )},

        {'type': 'heading', 'level': 2, 'text': 'The Bank Account Requirement for Business Credit Cards'},
        {'type': 'prose', 'paragraphs': [
            'Most bank-issued business credit cards require a business current account with the same bank. '
            'We verified this against each provider&rsquo;s eligibility pages: '
            'Lloyds, HSBC, NatWest, Santander, and Metro Bank all have this requirement. '
            'This means you cannot get a Lloyds credit card unless you bank with Lloyds, '
            'even if the Lloyds card has the <a href="/business-credit-cards/low-apr-business-credit-cards/">lowest APR on the market</a>.',
            'The cards without a bank account requirement are: Barclaycard Select, '
            'Capital on Tap, the full Amex range, and some fintech cards. '
            'If you bank with a fintech provider or simply don&rsquo;t want to switch banks, '
            'your realistic shortlist is these providers. We cover <a href="/business-credit-cards/best-business-credit-cards-for-sole-traders/">sole trader eligibility separately</a> '
            'since several cards exclude them.',
            'Barclaycard is the only major traditional bank card without an existing-account requirement, '
            'which is why it appears on most &ldquo;open access&rdquo; shortlists despite its higher APR. '
            'We update these eligibility checks quarterly.',
        ]},

        {'type': 'callout',
         'style': 'warning',
         'heading': 'Multiple applications leave visible marks',
         'text': (
             'Each application triggers a hard credit search, which other lenders can see. '
             'Applying to three cards in the same month signals financial stress to underwriters, '
             'even if you&rsquo;re approved for all three. '
             'Decide which card you want before applying, and space applications at least three months apart '
             'if you need to try more than one.'
         )},

        {'type': 'heading', 'level': 2, 'text': 'Business Credit Card Terms Explained'},

        {'type': 'definition',
         'term': 'Representative APR',
         'definition': (
             'The interest rate that at least 51% of successful applicants receive. '
             'Your actual rate may be higher depending on your credit profile. '
             'A card advertised at 19.9% representative APR may give you a rate of 24.9% '
             'if your business credit file is thin. '
             'The representative APR is a comparison benchmark, not a guarantee.'
         )},

        {'type': 'definition',
         'term': 'Purchase rate',
         'definition': (
             'The interest rate applied to purchases when you carry a balance. '
             'Usually the same as the representative APR, but some cards have separate rates '
             'for purchases, balance transfers, and cash advances. '
             'Always check all three if you plan to use the card for more than straightforward purchases.'
         )},

        {'type': 'definition',
         'term': 'Balance transfer',
         'definition': (
             'Moving an existing card balance to a new card, typically to benefit from a lower rate. '
             '0% balance transfer offers are common on personal credit cards but extremely rare on business cards. '
             'If you&rsquo;re carrying expensive debt on a business card, the practical options are '
             'switching to the lowest-APR card available or paying the balance down directly. '
             'See the <a href="/business-credit-cards/what-is-a-balance-transfer-credit-card/">balance transfer guide</a> '
             'for the full picture.'
         )},

        {'type': 'definition',
         'term': 'Credit limit',
         'definition': (
             'The maximum balance the provider will allow on the account. '
             'Limits on business cards vary widely &mdash; from &pound;1,000 on entry-level cards '
             'to &pound;250,000+ on Capital on Tap for businesses with strong financials. '
             'Your initial limit is set at application. You can usually request an increase after '
             'six to twelve months of on-time payments.'
         )},

        {'type': 'definition',
         'term': 'Minimum payment',
         'definition': (
             'The smallest amount you can pay each month without incurring a missed-payment penalty. '
             'Paying only the minimum means interest compounds on the remaining balance. '
             'On a card at 20% APR, carrying a &pound;5,000 balance and paying only the minimum '
             'will cost significantly more than the headline rate suggests over a twelve-month period.'
         )},

        {'type': 'heading', 'level': 2, 'text': 'What to Check Before Applying for a Business Credit Card'},
        {'type': 'list', 'html': (
            '<ul>\n'
            '    <li>Does the card require a business current account with the same provider?</li>\n'
            '    <li>Is your business structure eligible? (Some cards exclude sole traders or require Ltd registration.)</li>\n'
            '    <li>What is the minimum turnover requirement?</li>\n'
            '    <li>Is there an annual fee, and does your projected spend justify it?</li>\n'
            '    <li>What is the interest-free period on purchases?</li>\n'
            '    <li>Are additional cardholder fees included or charged separately?</li>\n'
            '    <li>Does the card have a foreign transaction fee if you spend abroad?</li>\n'
            '</ul>'
        )},

        {'type': 'heading', 'level': 2, 'text': 'Your First Business Credit Card: A Practical Checklist'},
        {'type': 'prose', 'paragraphs': [
            'If you have never had a business credit card before, this checklist will save you from the most common mistakes. Work through it before you apply.',
        ]},
        {'type': 'list', 'html': (
            '<ol>\n'
            '    <li><strong>Check whether your bank offers a business credit card.</strong> '
            'If you bank with Lloyds, HSBC, NatWest, Santander, or Metro Bank, your own bank almost certainly has a card. '
            'It will usually have the lowest APR available to you because they already hold your account data. '
            'Start here.</li>\n'
            '    <li><strong>Confirm your business structure is eligible.</strong> '
            'Some cards are limited companies only (Capital on Tap, Funding Circle). '
            'Others accept sole traders (Barclaycard, Amex). Check before you apply &mdash; '
            'a declined application leaves a mark on your credit file.</li>\n'
            '    <li><strong>Calculate your typical monthly spend.</strong> '
            'Add up your regular business expenses that could go on a card: software subscriptions, '
            'fuel, office supplies, travel, advertising. This number tells you whether a rewards card '
            'or a low-APR card makes more sense. Below &pound;1,000/month, rewards barely register. '
            'Above &pound;3,000/month, the right rewards card can return &pound;300&ndash;&pound;600 a year.</li>\n'
            '    <li><strong>Decide whether you will carry a balance.</strong> '
            'Be honest. If you will sometimes carry a balance, APR is your primary metric. '
            'If you will always clear in full, APR is irrelevant and you should optimise for rewards or cashback.</li>\n'
            '    <li><strong>Check Amex acceptance if you are considering an Amex card.</strong> '
            'Call your top five suppliers and ask. If three or more do not accept Amex, '
            'go with a Visa or Mastercard card instead.</li>\n'
            '    <li><strong>Apply to one card at a time.</strong> '
            'Each application creates a hard search on your credit file. '
            'Multiple applications in the same month signal financial stress to lenders. '
            'Wait at least three months between applications if your first choice declines you.</li>\n'
            '</ol>'
        )},

        {'type': 'prose', 'paragraphs': [
            'If you have worked through this checklist and still feel uncertain, our '
            '<a href="/business-credit-cards/best-business-credit-cards/">full comparison page</a> '
            'filters by business type, spend level, and bank account. It will narrow the field to '
            'two or three realistic options based on your situation.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'What Credit Score Do You Need for a Business Credit Card?'},
        {'type': 'prose', 'paragraphs': [
            'Most providers do not publish minimum credit scores. In practice, if your personal credit '
            'score is above 650 (on Experian&rsquo;s scale) and your business has been trading for at '
            'least six months, you will qualify for most mainstream cards. If your credit is thin or '
            'damaged, see our <a href="/business-credit-cards/poor-credit/">business credit cards for poor credit</a> guide. '
            'Capital on Tap and Barclaycard are generally more accessible than bank-linked cards for '
            'businesses with limited credit history.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'How Long Does a Business Credit Card Application Take?'},
        {'type': 'prose', 'paragraphs': [
            'Fintech providers like Capital on Tap can give you a decision within hours and issue '
            'a virtual card immediately on approval. Bank cards typically take five to ten working days '
            'from application to receiving the physical card. Amex usually ships within three to five '
            'working days of approval. If you need a card urgently, Capital on Tap&rsquo;s instant '
            'virtual card is the fastest route available.',
            'The speed difference comes down to underwriting method. Fintech lenders like Capital on Tap and Funding Circle use Open Banking APIs, Companies House data, and credit bureau checks for automated underwriting. They pull your bank transaction history (with your permission), cross-reference it against Companies House filings, and run a credit check &mdash; all in minutes. Traditional banks rely on manual review processes built for their broader lending operations, which is why decisions take days rather than hours. The trade-off: automated underwriting is faster but less flexible. If your financials are borderline, a bank relationship manager may approve what an algorithm would not.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html': (
            '<ul>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '    <li><a href="/business-credit-cards/low-apr-business-credit-cards/">Lowest APR business credit cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-cashback-and-reward/">Cashback and rewards cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-business-charge-cards/">Business charge cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards-for-sole-traders/">Cards for sole traders</a></li>\n'
            '    <li><a href="/business-credit-cards/best-credit-cards-for-start-ups/">Cards for start-ups</a></li>\n'
            '    <li><a href="/business-credit-cards/poor-credit/">Cards for poor credit</a></li>\n'
            '    <li><a href="/business-credit-cards/business-credit-cards-vs-charge-cards/">Credit cards vs charge cards explained</a></li>\n'
            '    <li><a href="/business-credit-cards/what-is-a-balance-transfer-credit-card/">What is a balance transfer?</a></li>\n'
            '</ul>'
        )},

        {'type': 'heading', 'level': 2, 'text': 'Business Credit Card Guide FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'Do I need a business credit card if I&rsquo;m a sole trader?',
             'a': 'You are not required to have one, but a dedicated business card separates your spending for cleaner tax records and builds a business credit profile. If you spend more than &pound;500/month on business expenses, the accounting time saved usually justifies it.'},
            {'q': 'Does a business credit card affect my personal credit score?',
             'a': 'Most small business credit cards require a personal guarantee, so the application creates a hard search on your personal credit file. Ongoing use primarily builds your business credit profile, but missed payments can affect your personal score as well.'},
            {'q': 'Can I get a business credit card without switching my bank account?',
             'a': 'Yes. Barclaycard, Capital on Tap, and the full Amex range do not require a business current account with the same provider. Most other bank-issued cards (Lloyds, HSBC, NatWest, Santander) require an existing account.'},
            {'q': 'What credit score do I need for a business credit card?',
             'a': 'Most providers do not publish minimum scores. In practice, a personal credit score above 650 on Experian&rsquo;s scale and at least six months of trading history will qualify you for most mainstream cards.'},
            {'q': 'How long does it take to get a business credit card?',
             'a': 'Fintech providers like Capital on Tap can issue a virtual card within hours. Bank cards typically take five to ten working days. Amex usually ships within three to five working days of approval.'},
            {'q': 'Is Section 75 protection available on business credit cards?',
             'a': 'No. Business credit cards do not benefit from Section 75 of the Consumer Credit Act 1974. That protection applies to personal credit card purchases between &pound;100 and &pound;30,000. For disputed business card purchases, your recourse is the card network&rsquo;s chargeback scheme (Visa or Mastercard), which is voluntary and has shorter time limits.'},
            {'q': 'Should I get a credit card or a charge card for my business?',
             'a': 'A credit card if you might ever need to carry a balance. A charge card if you always clear in full and want the discipline of mandatory monthly clearance. Most small businesses benefit from a credit card as the safer default.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified card terms and eligibility criteria against each '
            'provider&rsquo;s public product page on 20 March 2026. '
            'APR figures are representative rates as published on provider pages.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees from some '
            'providers linked on this page. This does not affect the editorial content of this guide, '
            'which is based on publicly available product information.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
