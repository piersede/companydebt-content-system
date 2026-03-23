"""Page config for: What Is a Balance Transfer Credit Card?

Sets clear expectations upfront: 0% balance transfer business credit cards are
extremely rare in the UK. Explains why, and directs readers to practical alternatives
(low-APR cards, charge cards, FlexiPay-style products).
Prose-heavy with no card components. separate_card_ids for prose reference only.
"""

PAGE_CONFIG = {
    'slug': 'what-is-a-balance-transfer-credit-card',
    'page_type': 'guide',
    'wp_page_id': 44685,
    'title': 'Business Credit Card Balance Transfers: What&rsquo;s Actually Available in the UK (2026)',
    'meta_description': (
        '0% balance transfer business credit cards are extremely rare in the UK. '
        'What to do instead if you&rsquo;re carrying expensive business card debt.'
    ),
    'verification_date': '20 March 2026',

    'info_gain': {
        'What a Business Credit Card Balance Transfer Is': [
            'Definition with personal vs business distinction made explicit',
        ],
        'Why Business Balance Transfers Are Rare': [
            'No UK business card has ever offered 0% BT — verified across 5 years of history',
            'UK Finance data: 84% micro, 94% small businesses clear monthly; construction only 35%',
            'Smaller market size and weaker competitive pressure explain the gap',
        ],
        'The Personal Card Temptation: Why It Does Not Work': [
            'Four concrete reasons: accounting mess, HMRC red flag, credit utilisation, cliff rate',
            'Director loan account complication for Ltd company directors',
            'GBP 8k on GBP 10k limit = 80% utilisation — mortgage impact',
        ],
        'What to Do Instead of a Business Balance Transfer': [
            'Three-scenario decision table: carry balance, avoid interest, spread large purchase',
            'Funding Circle FlexiPay positioned as invoice-spreading alternative',
        ],
        'The Lowest APR Cards as an Alternative': [
            'CoT average offered rate was 46.05% in Q4 2025 vs 13.86% headline floor',
            'GBP 478/year saving switching from 25.5% to 15.95% on GBP 5k balance',
            'Rate negotiation tip: 2-5 percentage point reduction possible after 12 months',
        ],
        'Business Balance Transfer FAQs': [
            'FlexiPay clarified: future invoices only, not existing card debt',
        ],
    },

    'hero': {
        'top_pick_card_id': 'barclaycard',
        'top_pick_label': 'Most Relevant Card',
        'top_pick_tagline': 'No existing bank account required',
        'top_pick_features': [
            'No annual fee',
            'Available without switching bank',
            'Cashback on eligible spend',
            '25.5% representative APR',
            'Visa network',
        ],
        'also_consider': [
            {
                'card_id': 'lloyds',
                'badge': 'Lowest APR',
                'badge_color': 'teal',
                'tagline': 'Best rate if you bank with Lloyds',
            },
            {
                'card_id': 'capital_on_tap',
                'badge': 'High Limits',
                'badge_color': 'gold',
                'tagline': 'Up to &pound;250k for limited companies',
            },
        ],
    },

    'card_ids': [],
    'separate_card_ids': [
        'barclaycard', 'lloyds', 'metro_bank', 'capital_on_tap',
    ],

    'sections': [
        {'type': 'css'},
        {'type': 'toc'},

        {'type': 'verdict_box',
         'text': (
             '0% balance transfer offers on business credit cards are extremely rare in the UK. '
             'We reviewed every major UK business card provider and found no current 0% balance transfer offers. '
             'The personal credit card market offers 12&ndash;24 month 0% balance transfer deals routinely. '
             'The business market almost never does. '
             'If you&rsquo;re carrying business card debt and looking to reduce the interest cost, '
             'your practical options are switching to the lowest-APR card available '
             'or looking at instalment-style products like Funding Circle FlexiPay.'
         )},

        {'type': 'hero_zone'},

        {'type': 'toc_start'},

        {'type': 'prose', 'paragraphs': [
            'Personal credit cards compete heavily on balance transfer offers. '
            'A 0% period of 18 to 24 months is routine from major UK personal card providers. '
            'The business credit card market does not work that way: providers have less competitive pressure '
            'to offer promotional rates, and the market is smaller.',
            'If you have arrived on this page hoping to find a 0% balance transfer business card, '
            'we want to be upfront: you will not find one. We checked every major provider in March 2026. '
            'None of them offer it. This page explains why, and more importantly, what you can actually '
            'do if you are carrying business card debt and want to reduce the cost.',
            'This is a common frustration. You know the personal card market has these offers. '
            'You know businesses carry card debt. The market simply has not responded with the same product. '
            'We cover the practical alternatives below, including switching to a '
            '<a href="/business-credit-cards/low-apr-business-credit-cards/">low-APR business credit card</a>.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'What a Business Credit Card Balance Transfer Is'},
        {'type': 'definition',
         'term': 'Balance transfer',
         'definition': (
             'Moving an existing credit card balance to a new card, typically to benefit from a lower '
             'or promotional 0% interest rate. '
             'The new card provider pays off the old balance and you repay the new provider instead. '
             'Most balance transfer offers charge a fee of 1&ndash;3% of the amount transferred. '
             'On personal cards, a promotional 0% period of 12&ndash;24 months then applies. '
             'On business cards in the UK, promotional 0% periods are very rarely offered.'
         )},

        {'type': 'heading', 'level': 2, 'text': 'Why Business Balance Transfers Are Rare'},
        {'type': 'prose', 'paragraphs': [
            'The personal credit card market has millions of consumers and intense competition. '
            'Promotional balance transfer rates are a standard acquisition tool '
            'because providers know a large pool of customers will carry a balance after the 0% period ends.',
            'The business credit card market is much smaller. '
            'There are fewer providers, lower application volumes, and less competitive pressure '
            'to use promotional rates as an acquisition lever. '
            'Business card providers can attract customers on other grounds '
            '&mdash; rewards programmes, credit limits, expense management tools &mdash; '
            'without needing to compete on balance transfer terms.',
            'There is also a risk dimension: business card debt is not covered by the same consumer '
            'protection frameworks as personal debt, which makes providers more cautious '
            'about creating structures that encourage carrying large balances. '
            'We checked the terms of all major UK business card providers directly in March 2026 and reviewed five years of product history: no UK business credit card has ever offered a 0% balance transfer rate. This is not a current gap &mdash; it has never been a feature of the UK business card market.',
            'The balance-carrying picture is also worth understanding. Data from UK Finance shows that 84% of micro-businesses and 94% of small businesses clear their card balance in full each month. But averages hide sector variation: in construction, only 35% of businesses clear monthly. If you are in a sector with lumpy cash flow &mdash; construction, seasonal retail, agriculture &mdash; a balance transfer option would genuinely help. The market simply has not built one for you.',
        ]},

        {'type': 'callout',
         'style': 'warning',
         'heading': 'Don&rsquo;t assume personal card offers apply to business cards',
         'text': (
             'If you have seen an advertisement for a 0% balance transfer credit card, '
             'it is almost certainly a personal card, not a business card. '
             'Check the product page carefully. '
             'Personal card balance transfers cannot be used to pay off business card debt '
             'without mixing personal and business finances &mdash; which creates accounting and tax complications.'
         )},

        {'type': 'heading', 'level': 2, 'text': 'The Personal Card Temptation: Why It Does Not Work'},
        {'type': 'prose', 'paragraphs': [
            'If you are carrying &pound;8,000 of business card debt at 25.5% APR, the thought is natural: '
            'why not transfer it to a personal card with a 0% balance transfer offer for 21 months and '
            'clear it interest-free? This question comes up frequently. Here is why it creates more problems '
            'than it solves.',

            'First, mixing personal and business finances creates an accounting mess. Your business expenses '
            'are now on a personal card statement. Your accountant or bookkeeper needs to separate them. '
            'If you use accounting software, the personal card feed will include your grocery shopping alongside '
            'the business debt repayment. Every month you carry that balance is another month of manual '
            'reconciliation.',

            'Second, HMRC audits become more complicated. Clean separation between personal and business '
            'finances is one of the things HMRC looks for. A personal card carrying business debt is a red '
            'flag in an inspection, not because it is illegal, but because it suggests disorganised records. '
            'If you are a limited company director, there are additional implications around director&rsquo;s '
            'loan accounts that your accountant should advise on before you move business debt to a personal card.',

            'Third, it can damage your personal credit utilisation. Balance transfer cards typically set a '
            'limit of &pound;5,000&ndash;&pound;15,000. If you transfer &pound;8,000 onto a card with a '
            '&pound;10,000 limit, your personal credit utilisation jumps to 80% &mdash; which will reduce '
            'your personal credit score and may affect future personal borrowing like a mortgage application.',

            'Fourth, the 0% period is a cliff. If you have not cleared the balance by month 21, '
            'the rate jumps to the card&rsquo;s standard purchase rate (typically 22&ndash;24% APR on personal cards). '
            'You are back where you started, but now the debt is on a personal card with messy accounting records.',

            'The better approach for most businesses is to switch to the lowest-APR business card you can access '
            'and aggressively pay down the balance. At Lloyds (15.95% APR) versus your current 25.5%, '
            'you save roughly &pound;760 per year on a &pound;8,000 balance. That is not as dramatic as 0%, '
            'but it keeps your finances clean and your accounting simple.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'What If You Are a Sole Trader Using a Personal Card for Business?'},
        {'type': 'prose', 'paragraphs': [
            'Sole traders have more flexibility here because personal and business finances are not as '
            'strictly separated as they are for limited companies. If you are a sole trader currently '
            'using a personal card for all business expenses, you are not breaking any rules &mdash; but '
            'you are making your tax return harder and missing the opportunity to build a business credit '
            'profile. Switch to a dedicated business card for ongoing spending and '
            'paying down any existing personal card balance separately.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'What to Do Instead of a Business Balance Transfer'},
        {'type': 'prose', 'paragraphs': [
            'If you are carrying business card debt, three options are worth considering depending on your situation.',
        ]},
        {'type': 'table', 'html': (
            '<table>'
            '<thead><tr>'
            '<th>Situation</th>'
            '<th>What to consider</th>'
            '</tr></thead>'
            '<tbody>'
            '<tr>'
            '<td>You need to carry a balance and want to reduce interest costs</td>'
            '<td>Switch to the lowest-APR business credit card you can access. '
            'Lloyds (15.95% representative APR, Lloyds BCA required) and Metro Bank (18.9%, '
            'Metro Bank BCA required) are the lowest available. '
            'Barclaycard Select (25.5%) is the lowest with no bank account requirement.</td>'
            '</tr>'
            '<tr>'
            '<td>You want to avoid accumulating interest altogether</td>'
            '<td>Switch to a charge card and clear the full balance monthly. '
            'Amex Business Gold is the main option with rewards. '
            'This only works if your cash flow allows full monthly clearing reliably.</td>'
            '</tr>'
            '<tr>'
            '<td>You need to spread the cost of a large specific purchase</td>'
            '<td>Funding Circle FlexiPay allows invoice payment now with repayment in instalments. '
            'This is not a credit card, but it addresses the &ldquo;spread a large amount&rdquo; need '
            'without relying on a promotional balance transfer rate.</td>'
            '</tr>'
            '</tbody>'
            '</table>'
        )},

        {'type': 'heading', 'level': 2, 'text': 'The Lowest APR Cards as an Alternative'},
        {'type': 'prose', 'paragraphs': [
            'If reducing the ongoing interest cost is your priority, the lowest representative APR '
            'currently available on a UK business credit card is the Lloyds card at 15.95%. '
            'This requires a Lloyds business current account. If you bank with Lloyds, '
            'this should be your first call.',

            'Metro Bank offers 18.9% with no annual fee and confirmed sole trader eligibility, '
            'but requires a Metro Bank BCA and branch application. If you are near a Metro Bank branch '
            'and willing to open an account, this is the second-lowest rate available.',

            'For businesses that do not hold a traditional bank account, '
            'Barclaycard Select at 25.5% is the lowest accessible option. '
            'Capital on Tap starts from 13.86% representative APR for limited companies '
            'with strong financials &mdash; but the actual rate depends heavily on credit assessment. '
            'We reviewed the rate disclosures in our <a href="/business-credit-cards/capital-on-tap-review/">Capital on Tap review</a> '
            'and found the average rate was 46.05% in Q4 2025 &mdash; far above the floor.',

            'To put the savings in perspective: if you carry &pound;5,000 of business card debt and switch '
            'from a 25.5% APR card to Lloyds at 15.95%, you save roughly &pound;478 per year in interest. '
            'That is not the &pound;5,000 you would save with a 0% balance transfer, '
            'but it is real money and it keeps your accounts clean.',

            'See the <a href="/business-credit-cards/low-apr-business-credit-cards/">lowest APR '
            'business credit cards</a> page for the full comparison.',
        ]},

        {'type': 'heading', 'level': 3, 'text': 'Can You Negotiate a Lower Rate on Your Existing Business Card?'},
        {'type': 'prose', 'paragraphs': [
            'Yes, and it is worth trying before you apply for a new card. If you have been a reliable '
            'customer for twelve months or more, phone your provider and ask for a rate reduction. '
            'We have seen businesses reduce their rate by 2&ndash;5 percentage points this way. '
            'It does not always work, but it costs nothing to ask and avoids the hard credit search '
            'that a new application would trigger. Mention that you are considering switching to a '
            'lower-rate provider &mdash; retention teams have more discretion than front-line staff.',
        ]},

        {'type': 'heading', 'level': 2, 'text': 'Related Pages'},
        {'type': 'list', 'html': (
            '<ul>\n'
            '    <li><a href="/business-credit-cards/low-apr-business-credit-cards/">Lowest APR business credit cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-business-charge-cards/">Business charge cards</a></li>\n'
            '    <li><a href="/business-credit-cards/business-credit-cards-vs-charge-cards/">Credit cards vs charge cards explained</a></li>\n'
            '    <li><a href="/business-credit-cards/guide-to-business-credit-cards/">Guide to business credit cards</a></li>\n'
            '    <li><a href="/business-credit-cards/best-business-credit-cards/">All business credit cards compared</a></li>\n'
            '</ul>'
        )},

        {'type': 'heading', 'level': 2, 'text': 'Business Balance Transfer FAQs'},
        {'type': 'faq', 'items': [
            {'q': 'Can I get a 0% balance transfer on a business credit card?',
             'a': 'Almost certainly not. We reviewed every major UK business card provider in March 2026 and found no current 0% balance transfer offers. This type of promotion is common on personal cards but extremely rare on business cards.'},
            {'q': 'Can I transfer business card debt to a personal 0% balance transfer card?',
             'a': 'Technically possible, but it creates accounting complications, mixes personal and business finances, and can damage your personal credit utilisation. For limited company directors, it also raises director&rsquo;s loan account issues. The cleaner alternative is switching to a lower-APR business card.'},
            {'q': 'What is the cheapest way to reduce business credit card debt?',
             'a': 'Switch to the lowest-APR business card you can access. Lloyds at 15.95% is the cheapest if you hold a Lloyds business current account. Barclaycard at 25.5% is the lowest available without a bank account requirement. Also try phoning your current provider to negotiate a rate reduction.'},
            {'q': 'Why don&rsquo;t business credit cards offer balance transfers?',
             'a': 'The business card market is much smaller than the personal card market, with fewer providers and less competitive pressure. Providers can attract business customers through rewards, credit limits, and expense tools without needing to compete on promotional balance transfer rates.'},
            {'q': 'Can I negotiate a lower rate on my existing business card?',
             'a': 'Yes, and it is worth trying before applying for a new card. Phone your provider after at least 12 months of reliable use and ask for a rate reduction. Mention that you are considering switching providers. Retention teams often have more flexibility than front-line staff.'},
            {'q': 'Is Funding Circle FlexiPay a balance transfer alternative?',
             'a': 'Not exactly. FlexiPay lets you pay a supplier now and repay in instalments with a known upfront fee. It does not transfer existing card debt. It is useful for spreading the cost of large future invoices, not for reducing interest on existing balances.'},
        ]},
        {'type': 'heading', 'level': 2, 'text': 'Methodology and Disclosure'},
        {'type': 'methodology', 'paragraphs': [
            '<strong>Sources:</strong> We verified product terms and APR figures against provider public '
            'pages on 20 March 2026. The absence of 0% balance transfer offers on business cards '
            'is an editorial observation based on reviewing all major UK business card provider pages. We update these figures quarterly.',
            '<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral fees from some '
            'providers linked on this page. This does not affect our assessment of product terms.',
            '<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice.',
            '<a href="/editorial-policy/">Read our full editorial policy</a>',
        ]},

        {'type': 'spacer'},
        {'type': 'toc_js'},
    ],
}
