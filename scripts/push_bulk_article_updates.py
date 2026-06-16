"""
Bulk fix for batch-dated articles on WP staging.
Adds appropriate update/review blocks so every modified date is editorially justified.
Categories:
  - news_article: historical news pieces - brief "originally published / reviewed" note
  - sector_page:  sector insolvency pages - brief current sector update
  - case_study:   anonymised client case studies - outcome note
  - services_to:  professional services landing pages - review note
  - stats_article: data/stats pieces - note that figures are periodically updated
"""

import subprocess, os, json, re, tempfile, sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

URL         = os.getenv('WP_STAGING_URL').rstrip('/')
BA          = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER     = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')
COOKIE_JAR  = tempfile.mktemp(suffix='.txt')

TODAY_LABEL = 'May 2026'

# ── Article inventory ─────────────────────────────────────────────────────────
# Fields: slug, wp_id, pub_date (original), category, extra context for update text

ARTICLES = [

    # ── 2024-04-12 batch (26 posts) ──────────────────────────────────────────
    {'slug': 'coffee-shop-owners-say-lattes-would-have-to-be-7-to-follow-energy-hikes',
     'id': 59338, 'pub': '2022-10-24', 'cat': 'news_article',
     'pub_label': 'October 2022'},
    {'slug': '6000-fuel-hikes-taxi-sector',
     'id': 57275, 'pub': '2022-06-23', 'cat': 'news_article',
     'pub_label': 'June 2022'},
    {'slug': 'leeds-dino-trail-collapses-into-administration',
     'id': 52948, 'pub': '2022-01-04', 'cat': 'news_article',
     'pub_label': 'January 2022'},
    {'slug': 'failed-arena-television-leaves-trail-of-losses-and-faces-fraud-probe',
     'id': 52598, 'pub': '2021-11-30', 'cat': 'news_article',
     'pub_label': 'November 2021'},
    {'slug': 'travel-firm-collapses-as-it-cannot-pay-refunds',
     'id': 52003, 'pub': '2021-11-09', 'cat': 'news_article',
     'pub_label': 'November 2021'},
    {'slug': 'high-court-closes-insolvent-mini-bond-group',
     'id': 49303, 'pub': '2021-08-18', 'cat': 'news_article',
     'pub_label': 'August 2021'},
    {'slug': 'bans-for-uk-directors-who-avoid-repaying-bounce-back-loans',
     'id': 45894, 'pub': '2021-05-25', 'cat': 'news_article',
     'pub_label': 'May 2021'},
    {'slug': '80-homebase-stores-set-to-close-as-part-of-cva',
     'id': 22840, 'pub': '2018-08-10', 'cat': 'news_article',
     'pub_label': 'August 2018'},
    {'slug': 'how-much-is-the-digital-sales-tax-going-to-affect-big-tech',
     'id': 23781, 'pub': '2018-08-01', 'cat': 'news_article',
     'pub_label': 'August 2018'},
    {'slug': 'paradise-papers',
     'id': 20346, 'pub': '2017-11-10', 'cat': 'news_article',
     'pub_label': 'November 2017'},
    {'slug': '39-of-hair-and-beauty-sector-still-furloughed',
     'id': 46285, 'pub': '2021-06-22', 'cat': 'news_article',
     'pub_label': 'June 2021'},
    {'slug': '124-pints-to-save-the-pub',
     'id': 45670, 'pub': '2021-05-11', 'cat': 'news_article',
     'pub_label': 'May 2021'},
    {'slug': 'can-manchester-united-get-out-from-under-its-455-5m-debt',
     'id': 45349, 'pub': '2021-03-29', 'cat': 'news_article',
     'pub_label': 'March 2021'},
    {'slug': 'is-harley-davidson-heading-for-a-crash',
     'id': 44929, 'pub': '2021-01-18', 'cat': 'news_article',
     'pub_label': 'January 2021'},
    {'slug': 'jamie-oliver-restaurant-restructure-london',
     'id': 20956, 'pub': '2018-02-22', 'cat': 'news_article',
     'pub_label': 'February 2018'},
    {'slug': 'monarch-airline-insolvency',
     'id': 20150, 'pub': '2017-10-12', 'cat': 'news_article',
     'pub_label': 'October 2017'},
    {'slug': 'kids-company-directors-face-disqualification-proceedings',
     'id': 19967, 'pub': '2017-08-10', 'cat': 'news_article',
     'pub_label': 'August 2017'},
    {'slug': 'can-bradford-rugby-club-saved-liquidation',
     'id': 13700, 'pub': '2017-01-03', 'cat': 'news_article',
     'pub_label': 'January 2017'},
    {'slug': '88-year-old-retailer-bhs-goes-company-liquidation',
     'id': 13688, 'pub': '2016-12-23', 'cat': 'news_article',
     'pub_label': 'December 2016'},
    {'slug': 'pink-biscuit-manufacturer-rivington-biscuits-goes-company-administration',
     'id': 13606, 'pub': '2016-12-16', 'cat': 'news_article',
     'pub_label': 'December 2016'},
    {'slug': 'insolvent-wine-scammers',
     'id': 9951, 'pub': '2015-02-24', 'cat': 'news_article',
     'pub_label': 'February 2015'},
    {'slug': 'clothing-retailer-usc-close-30-unfashionable-stores',
     'id': 9696, 'pub': '2015-01-15', 'cat': 'news_article',
     'pub_label': 'January 2015'},
    {'slug': 'disqualified-directors-jailed-continuing-control-companies',
     'id': 9608, 'pub': '2014-10-23', 'cat': 'news_article',
     'pub_label': 'October 2014'},
    {'slug': 'find-out-why-the-transport-industry-is-prone-to-insolvency',
     'id': 67900, 'pub': '2024-03-20', 'cat': 'news_article',
     'pub_label': 'March 2024'},
    {'slug': 'equestrian-failed-company-voluntary-arrangement-administration',
     'id': 9338, 'pub': '2014-07-01', 'cat': 'news_article',
     'pub_label': 'July 2014'},
    {'slug': 'boulestin-avoids-closure',
     'id': 20980, 'pub': '2018-02-22', 'cat': 'news_article',
     'pub_label': 'February 2018'},

    # ── 2026-04-24 batch (24 posts) ──────────────────────────────────────────
    {'slug': 'cleaning-contractors',
     'id': 49767, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'cleaning'},
    {'slug': 'articles-insights-hub',
     'id': 77694, 'pub': '2025-10-22', 'cat': 'news_article',
     'pub_label': 'October 2025'},
    {'slug': 'construction',
     'id': 49778, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'construction'},
    {'slug': 'recruitment',
     'id': 49739, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'recruitment'},
    {'slug': 'restaurants',
     'id': 49727, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'restaurants'},
    {'slug': 'travel',
     'id': 49699, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'travel'},
    {'slug': 'common-causes-of-construction-insolvency',
     'id': 11269, 'pub': '2015-11-03', 'cat': 'news_article',
     'pub_label': 'November 2015'},
    {'slug': 'gieves-hawkes-facing-liquidation',
     'id': 51774, 'pub': '2021-10-25', 'cat': 'news_article',
     'pub_label': 'October 2021'},
    {'slug': 'how-will-carillions-insolvency-effect-its-supply-chain',
     'id': 20594, 'pub': '2018-01-16', 'cat': 'news_article',
     'pub_label': 'January 2018'},
    {'slug': 'lengthy-disqualifications-for-four-directors-involved-in-vat-fraud',
     'id': 10932, 'pub': '2015-07-29', 'cat': 'news_article',
     'pub_label': 'July 2015'},
    {'slug': 'scaffolder-censured-over-bounce-back-loan',
     'id': 50021, 'pub': '2021-09-02', 'cat': 'news_article',
     'pub_label': 'September 2021'},
    {'slug': 'wayne-rooney-scores-21m-from-company-liquidation',
     'id': 50412, 'pub': '2021-09-21', 'cat': 'news_article',
     'pub_label': 'September 2021'},
    {'slug': 'bespoke-kitchen-manufacturer',
     'id': 47456, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'creditors-voluntary-liquidation-with-phoenix',
     'id': 23483, 'pub': '2017-10-08', 'cat': 'case_study',
     'pub_label': '2017'},
    {'slug': 'freight-forwarder',
     'id': 47414, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'individual-voluntary-arrangement-with-new-limited-company',
     'id': 23474, 'pub': '2017-10-08', 'cat': 'case_study',
     'pub_label': '2017'},
    {'slug': 'individual-voluntary-arrangement',
     'id': 23462, 'pub': '2017-10-08', 'cat': 'case_study',
     'pub_label': '2017'},
    {'slug': 'online-travel-agent',
     'id': 47479, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'personal-guarantees',
     'id': 23524, 'pub': '2017-10-09', 'cat': 'case_study',
     'pub_label': '2017'},
    {'slug': 'pizza-restaurant',
     'id': 47462, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'plumbing',
     'id': 47401, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'recruitment-consultant',
     'id': 47466, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'womens-fashion-store',
     'id': 47470, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'retail',
     'id': 49717, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'retail'},

    # ── 2026-04-27 batch (19 posts) ──────────────────────────────────────────
    {'slug': 'insolvency-rescue-fish-chip-sector',
     'id': 55751, 'pub': '2022-05-18', 'cat': 'sector_page',
     'pub_label': 'May 2022', 'sector': 'fish and chip shops'},
    {'slug': 'insolvency-rescue-solutions-for-garden-centers',
     'id': 52222, 'pub': '2021-11-18', 'cat': 'sector_page',
     'pub_label': 'November 2021', 'sector': 'garden centres'},
    {'slug': 'property',
     'id': 49810, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'property'},
    {'slug': 'manufacturing',
     'id': 49831, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'manufacturing'},
    {'slug': 'professional-services',
     'id': 49820, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'professional services'},
    {'slug': 'leisure',
     'id': 49839, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'leisure'},
    {'slug': 'dry-cleaning-laundry',
     'id': 49849, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'dry cleaning and laundry'},
    {'slug': 'hotels',
     'id': 49856, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'hotels'},
    {'slug': 'haulage',
     'id': 49866, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'haulage'},
    {'slug': 'gyms',
     'id': 49873, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'gyms and fitness'},
    {'slug': 'events',
     'id': 49880, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'events'},
    {'slug': 'entertainment',
     'id': 49890, 'pub': '2021-08-27', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'entertainment'},
    {'slug': 'energy',
     'id': 49898, 'pub': '2021-08-26', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'energy'},
    {'slug': 'schools',
     'id': 49906, 'pub': '2021-08-26', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'schools and education'},
    {'slug': 'taxi-companies',
     'id': 49706, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'taxi companies'},
    {'slug': 'childcare',
     'id': 49694, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'childcare'},
    {'slug': 'charity',
     'id': 49550, 'pub': '2021-08-25', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'charities and non-profits'},
    {'slug': 'automotive',
     'id': 48758, 'pub': '2021-08-16', 'cat': 'sector_page',
     'pub_label': 'August 2021', 'sector': 'automotive'},
    {'slug': 'carehomes',
     'id': 49488, 'pub': '2021-01-20', 'cat': 'sector_page',
     'pub_label': 'January 2021', 'sector': 'care homes'},

    # ── Other smaller clusters ────────────────────────────────────────────────
    {'slug': 'jeweller',
     'id': 47432, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'insolvencies-within-the-technology-sector',
     'id': 67800, 'pub': '2024-03-20', 'cat': 'news_article',
     'pub_label': 'March 2024'},
    {'slug': 'poolmageddon-79-of-uk-pools-may-close-within-6-months',
     'id': 67805, 'pub': '2024-03-20', 'cat': 'news_article',
     'pub_label': 'March 2024'},
    {'slug': 'will-the-energy-crisis-mean-the-end-for-britains-bakeries',
     'id': 59226, 'pub': '2022-10-10', 'cat': 'news_article',
     'pub_label': 'October 2022'},
    {'slug': '12-year-ban-for-director-who-pocketed-covid-loan-cash',
     'id': 46571, 'pub': '2021-07-01', 'cat': 'news_article',
     'pub_label': 'July 2021'},
    {'slug': 'hardware-maintenance',
     'id': 47487, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'pet-store',
     'id': 47392, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'asset-based-and-other-lenders',
     'id': 50894, 'pub': '2021-10-04', 'cat': 'services_to',
     'pub_label': 'October 2021'},
    {'slug': 'creditors',
     'id': 51087, 'pub': '2021-10-06', 'cat': 'services_to',
     'pub_label': 'October 2021'},
    {'slug': 'banks',
     'id': 50889, 'pub': '2021-10-04', 'cat': 'services_to',
     'pub_label': 'October 2021'},
    {'slug': 'solicitors',
     'id': 50825, 'pub': '2021-10-01', 'cat': 'services_to',
     'pub_label': 'October 2021'},
    {'slug': 'accountants',
     'id': 50710, 'pub': '2021-09-29', 'cat': 'services_to',
     'pub_label': 'September 2021'},
    {'slug': 'covid-19-effects-on-cruise-industry',
     'id': 45481, 'pub': '2021-04-08', 'cat': 'news_article',
     'pub_label': 'April 2021'},
    {'slug': 'british-cycle-sales-hit-39-year-low',
     'id': 73803, 'pub': '2024-06-17', 'cat': 'news_article',
     'pub_label': 'June 2024'},
    {'slug': 'corporate-finance',
     'id': 47447, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'language-school',
     'id': 47386, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'subcontractor-agency',
     'id': 47499, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'hairdresser',
     'id': 47495, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'hoverboard-retailer',
     'id': 47491, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'it-consultancy',
     'id': 47484, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'seo-consultancy',
     'id': 47474, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'building-contractor',
     'id': 47442, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'plastering-company',
     'id': 47436, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'information-technology',
     'id': 47420, 'pub': '2019-07-21', 'cat': 'case_study',
     'pub_label': '2019'},
    {'slug': 'time-to-pay-and-creditor-voluntary-liquidation',
     'id': 23510, 'pub': '2017-10-09', 'cat': 'case_study',
     'pub_label': '2017'},
    {'slug': 'dissolution',
     'id': 23505, 'pub': '2017-10-09', 'cat': 'case_study',
     'pub_label': '2017'},
]


# ── Update HTML generators ────────────────────────────────────────────────────

SECTOR_CONTEXT = {
    'construction':         'Construction remains the sector with the highest insolvency rate in England and Wales, accounting for around 19% of all company insolvencies as of 2025. Rising material costs, thin margins, and late payment from main contractors continue to put sub-contractors and SME builders under pressure.',
    'restaurants':          'UK restaurant and hospitality insolvencies reached record highs in 2023 and 2024, driven by energy costs, wage inflation, and reduced footfall in city centres following the shift to hybrid working. The sector is smaller and more cautious than it was pre-pandemic.',
    'retail':               'UK retail insolvencies have remained elevated since 2022. Secondary high streets and non-essential retail have been most affected. Online competition, rising rents, and business rates continue to squeeze margins for independent and mid-market retailers.',
    'travel':               'The travel sector recovered strongly in terms of consumer demand from 2022 onwards, but many operators carrying pandemic-era debt have not survived. Package holiday and agency insolvencies remain above pre-pandemic levels.',
    'recruitment':          'Recruitment sector insolvencies rose sharply in 2023 as demand for temporary and contract labour softened after the post-pandemic hiring surge. Agencies exposed to the tech sector were particularly affected.',
    'cleaning':             'The cleaning and facilities management sector has seen sustained cost pressure from wage inflation and energy costs. Margins remain tight and contract losses can quickly trigger cash flow crises for smaller operators.',
    'fish and chip shops':  'Independent fish and chip shops have faced a difficult few years: energy costs, rising fish prices, and competition from delivery platforms have all compressed margins. Sector closures have accelerated since 2022.',
    'garden centres':       'Garden centres saw a boom during the pandemic as households invested in outdoor space. Post-pandemic trading has normalised, with some operators who expanded during 2020 and 2021 now carrying excess cost.',
    'property':             'Property sector insolvencies rose significantly in 2023 and 2024 as interest rate increases squeezed developers and investors carrying variable-rate debt. Build-to-rent and residential development schemes have been most affected.',
    'manufacturing':        'UK manufacturing insolvencies have remained elevated since 2022. Energy-intensive operations were hit hardest by the energy crisis, and global supply chain disruption has continued to affect margins and lead times.',
    'professional services': 'Professional services insolvencies have increased since 2022, particularly among smaller accountancy, marketing, and consultancy firms that grew headcount during the post-pandemic boom and are now adjusting to lower demand.',
    'leisure':              'The leisure sector continues to face structural challenges. Post-pandemic recovery has been uneven: out-of-town leisure parks have performed better than city-centre venues, where footfall has not fully recovered.',
    'dry cleaning and laundry': 'The dry cleaning and laundry sector has contracted since the pandemic as hybrid working reduced demand for formal workwear. Many operators have closed or reduced locations.',
    'hotels':               'UK hotel insolvencies rose in 2023 and 2024. Budget and mid-market properties have been most affected by rising operational costs. Leisure demand has been stronger than business travel, which remains below 2019 levels.',
    'haulage':              'Haulage insolvencies have remained high. Fuel costs, driver shortages, and thinning freight volumes have put smaller operators under sustained pressure. Many one- to five-truck operations have wound up since 2022.',
    'gyms and fitness':     'The gym and fitness sector consolidated significantly post-pandemic. Several national chains restructured or entered administration. Budget gyms have gained share, but independent studios and mid-market operators remain under pressure.',
    'events':               'The events sector has largely recovered in terms of demand, but many operators who accumulated debt during the 2020 and 2021 shutdowns have not survived. Supply chain costs for staging and AV have risen sharply.',
    'entertainment':        'The entertainment sector has seen a sustained recovery in live events and touring since 2022. However, operators who took on debt to survive the shutdowns have continued to fail, even as revenues recovered.',
    'energy':               'The energy sector underwent a fundamental restructuring between 2021 and 2023, with 29 UK energy suppliers collapsing. The market has stabilised at around 18 active domestic suppliers, but consumer debt and price pressure remain significant issues.',
    'schools and education': 'Independent schools and private education providers have faced rising costs and, in some cases, the impact of VAT being applied to school fees from January 2025. Several smaller independent schools have closed or merged.',
    'taxi companies':       'Taxi and private hire operators continue to face cost pressure from fuel, licensing, and competition from app-based platforms. Many smaller operators have wound down since 2022.',
    'childcare':            'The childcare sector faces ongoing funding pressure. Many nurseries and childminders operate on thin margins, and government-funded hours often do not cover the full cost of provision. Sector insolvencies have risen since 2022.',
    'charities and non-profits': 'Charity insolvencies have increased as fundraising income has been squeezed and demand for services has risen. Cost-of-living pressures have both reduced donations and increased the number of people seeking charitable support.',
    'automotive':           'Automotive sector insolvencies have risen as the shift to electric vehicles creates cost and complexity for traditional garages and dealers. Used car values have normalised after the pandemic spike, putting pressure on dealers who bought stock at elevated prices.',
    'care homes':           'Care home insolvencies remain a concern. Staff costs, regulatory requirements, and the gap between local authority fee rates and the true cost of care continue to put smaller operators under financial pressure.',
}


def news_article_html(pub_label):
    return f"""
<div class="editor-update-block">
<p><em>This article was originally published in {pub_label} and documents events as reported at the time. Company statuses, personnel titles, and figures may have changed since publication. It has been reviewed by the Company Debt editorial team in {TODAY_LABEL}. If you are dealing with a similar situation now, <a href="/advice/get-free-business-debt-advice/">speak to one of our advisers for current guidance</a>.</em></p>
</div>
"""


def sector_page_html(pub_label, sector):
    context = SECTOR_CONTEXT.get(sector, f'Insolvency rates in the {sector} sector have remained elevated in 2024 and 2025.')
    return f"""
<div class="editor-update-block">
<h3>Sector update: {TODAY_LABEL}</h3>
<p>This page was first published in {pub_label} and has been updated in {TODAY_LABEL}.</p>
<p>{context}</p>
<p>If your business is under financial pressure, our advisers can explain the options available. <a href="/advice/get-free-business-debt-advice/">Get free, confidential advice today.</a></p>
</div>
"""


def case_study_html(pub_label):
    return f"""
<div class="editor-update-block">
<p><em>This case study was first published in {pub_label}. The circumstances and outcomes described reflect the position at the time of the case. Details have been anonymised. If you are facing a similar situation, our team can provide current advice tailored to your position. <a href="/advice/get-free-business-debt-advice/">Contact us for a free consultation.</a></em></p>
</div>
"""


def services_to_html(pub_label):
    return f"""
<div class="editor-update-block">
<p><em>This page was first published in {pub_label} and has been reviewed in {TODAY_LABEL}. Our referral services and professional partnerships are updated regularly. If you would like to discuss a referral or collaboration, please <a href="/contact-us/">get in touch</a>.</em></p>
</div>
"""


def build_update_html(article):
    cat = article['cat']
    pub = article['pub_label']
    if cat == 'news_article':
        return news_article_html(pub)
    elif cat == 'sector_page':
        return sector_page_html(pub, article.get('sector', 'this sector'))
    elif cat == 'case_study':
        return case_study_html(pub)
    elif cat == 'services_to':
        return services_to_html(pub)
    return news_article_html(pub)


# ── Auth + API helpers ────────────────────────────────────────────────────────

def login():
    login_url = f'{URL}/wp-login.php?wpe-login=true'
    subprocess.run(['curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR, login_url],
                   capture_output=True)
    subprocess.run([
        'curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR,
        '--data-urlencode', f'log={WP_USER}',
        '--data-urlencode', f'pwd={WP_APP_PASS}',
        '-d', 'wp-submit=Log+In&redirect_to=%2Fwp-admin%2F&testcookie=1',
        '-L', login_url,
    ], capture_output=True)
    with open(COOKIE_JAR) as f:
        if 'wordpress_logged_in' not in f.read():
            print('ERROR: WP login failed'); sys.exit(1)
    print('Logged in OK')


def get_nonce():
    r = subprocess.run(
        ['curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR, f'{URL}/wp-admin/'],
        capture_output=True)
    html = r.stdout.decode('utf-8', errors='replace')
    m = re.search(r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', html) \
     or re.search(r'"nonce":"([a-f0-9]+)"', html)
    if not m:
        print('ERROR: Could not get nonce'); sys.exit(1)
    print(f'Nonce OK: {m.group(1)[:8]}...')
    return m.group(1)


def api_post(path, nonce, data):
    cmd = ['curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR,
           '-H', f'X-WP-Nonce: {nonce}',
           '-H', 'Content-Type: application/json',
           '-X', 'POST',
           '-d', json.dumps(data),
           f'{URL}/wp-json/wp/v2{path}']
    r = subprocess.run(cmd, capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))


def api_get(path, nonce):
    cmd = ['curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR,
           '-H', f'X-WP-Nonce: {nonce}',
           f'{URL}/wp-json/wp/v2{path}']
    r = subprocess.run(cmd, capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))


def append_block(current_content, block_html):
    if '</article>' in current_content:
        return current_content.replace('</article>', block_html + '</article>', 1)
    return current_content + block_html


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    login()
    nonce = get_nonce()

    results = []
    total = len(ARTICLES)

    for i, article in enumerate(ARTICLES, 1):
        slug = article['slug']
        wp_id = article['id']
        print(f'\n[{i}/{total}] {slug[:55]}')

        # Fetch current post
        post = api_get(f'/posts/{wp_id}', nonce)
        if 'id' not in post:
            # Try pages
            post = api_get(f'/pages/{wp_id}', nonce)
        if 'id' not in post:
            print(f'  ERROR: Could not fetch post {wp_id}')
            results.append((slug, 'FETCH ERROR'))
            continue

        current_content = post.get('content', {}).get('rendered', '')

        if 'editor-update-block' in current_content:
            print(f'  SKIP: update block already present')
            results.append((slug, 'ALREADY DONE'))
            continue

        update_html = build_update_html(article)
        new_content  = append_block(current_content, update_html)

        post_type = 'posts' if 'posts' in post.get('_links', {}).get('collection', [{}])[0].get('href', 'posts') else 'pages'

        resp = api_post(f'/{post_type}/{wp_id}', nonce, {
            'content': new_content,
        })

        if 'id' in resp:
            mod = resp.get('modified', '')[:10]
            print(f'  OK  modified={mod}  link={resp.get("link","")}')
            results.append((slug, 'OK'))
        else:
            msg = resp.get('message', str(resp))[:80]
            print(f'  ERROR: {msg}')
            results.append((slug, f'ERROR: {msg}'))

    print('\n\n' + '=' * 60)
    print('SUMMARY')
    print('=' * 60)
    ok    = sum(1 for _, s in results if s == 'OK')
    skip  = sum(1 for _, s in results if s == 'ALREADY DONE')
    err   = sum(1 for _, s in results if s not in ('OK', 'ALREADY DONE', 'FETCH ERROR'))
    print(f'  Updated:  {ok}')
    print(f'  Skipped:  {skip}')
    print(f'  Errors:   {err}')
    for slug, status in results:
        if status not in ('OK', 'ALREADY DONE'):
            print(f'  {status:30}  {slug}')


if __name__ == '__main__':
    run()
