"""Declarative citation corrections from the 15-Jul-2026 Ahrefs audit.

Each entry records WHY, so a future reader does not have to re-derive the
research. Verified 2026-07-16: every `new` URL returns 200 to a browser UA
and its H1 was checked to confirm it is on-subject.

Ahrefs found these because they 404. It cannot find a fabricated citation
whose URL happens to resolve, so this list is a floor, not a ceiling.
"""

# href -> href swaps. Applied to every page carrying the old href.
LINK_FIXES = [
    {
        "id": "fa2020-sch28",
        "old": "https://www.legislation.gov.uk/ukpga/2020/14/schedule/28",
        "new": "https://www.legislation.gov.uk/ukpga/2020/14/section/98",
        "why": "Finance Act 2020 has no Schedule 28 (404). HMRC secondary "
               "preferential status is enacted by s.98, which amends IA 1986 "
               "s.386 and inserts Category 9 into Sch 6. Claim was right, "
               "citation was fabricated. Present on 7 pages.",
        "text_fixes": [
            ("Finance Act 2020, Schedule 28", "Finance Act 2020, Section 98"),
        ],
    },
    {
        "id": "badr",
        "old": "https://www.gov.uk/guidance/business-asset-disposal-relief",
        "new": "https://www.gov.uk/business-asset-disposal-relief",
        "why": "Old /guidance/ path 404s. Official BADR page (H1 'Business "
               "Asset Disposal Relief') lives at the root path.",
        "text_fixes": [],
    },
    {
        "id": "ex50",
        "old": "https://www.gov.uk/government/publications/ex50-civil-and-family-court-fees-high-court-and-county-court",
        "new": "https://www.gov.uk/government/publications/fees-in-the-civil-and-family-courts-main-fees-ex50",
        "why": "Old slug 404s. Current HMCTS publication H1: 'Fees in the "
               "civil and family courts - main fees (EX50)'.",
        "text_fixes": [],
    },
    {
        "id": "rpb",
        "old": "https://www.gov.uk/government/publications/insolvency-practitioner-regulation-regulatory-objectives-and-oversight-powers/recognised-professional-bodies-rpbs",
        "new": "https://www.gov.uk/government/publications/insolvency-practitioners-recognised-professional-bodies/recognised-professional-bodies",
        "why": "Old slug 404s. Insolvency Service RPB list H1: 'Recognised "
               "professional bodies'.",
        "text_fixes": [],
    },
    {
        "id": "hmrc-va",
        "old": "https://www.gov.uk/government/publications/hmrc-and-voluntary-arrangements",
        "new": "https://www.gov.uk/government/publications/working-with-insolvency-practitioners-vas",
        "why": "Old slug 404s. HMRC's actual published stance on CVAs/IVAs is "
               "'Working with insolvency practitioners'.",
        "text_fixes": [],
    },
    {
        "id": "hmrc-disputes",
        "old": "https://www.gov.uk/government/publications/hmrcs-approach-to-tax-disputes",
        "new": "https://www.gov.uk/government/collections/how-hmrc-resolves-civil-tax-disputes",
        "why": "Old slug 404s. Official collection H1: 'How HMRC resolves "
               "civil tax disputes' (LSS, Code of Governance, ADR).",
        "text_fixes": [],
    },
    {
        "id": "hmrc-securities",
        "old": "https://www.gov.uk/hmrc-internal-manuals/security-deposits",
        "new": "https://www.gov.uk/hmrc-internal-manuals/securities-guidance",
        "why": "No 'security-deposits' manual exists. The real manual on "
               "VAT/PAYE security deposits is 'Securities Guidance' (SG).",
        # Draft and staging word this label differently (staging drops the
        # hyphen), so both literals are listed. Harmless if one misses.
        "text_fixes": [
            ("HMRC - Security Deposits Manual", "HMRC - Securities Guidance Manual"),
            ("HMRC Security Deposits Manual", "HMRC Securities Guidance Manual"),
        ],
    },
    {
        "id": "ons-case",
        "old": "https://www.ons.gov.uk/businessindustryandtrade/business/activitysizeandlocation/bulletins/businessdemography/previousReleases",
        "new": "https://www.ons.gov.uk/businessindustryandtrade/business/activitysizeandlocation/bulletins/businessdemography/previousreleases",
        "why": "Pure case bug: ONS paths are lowercase. Genuine link rot, the "
               "only one in the whole audit.",
        "text_fixes": [],
    },
]

# Citations to DELETE outright: the cited document does not exist and there is
# no honest equivalent. Substituting a plausible-looking replacement would
# repeat the original error.
LINK_REMOVALS = [
    {
        "id": "ccfs40",
        "old": "https://www.gov.uk/government/publications/compliance-checks-penalties-for-failure-to-pay-ccfs40",
        "why": "CC/FS40 does not exist: HMRC's compliance-checks factsheet "
               "series runs CC/FS39 then CC/FS41, and there is no 'penalties "
               "for failure to pay' factsheet. The same Sources block already "
               "cites NIM12206 (officer liability), which is HMRC's genuine "
               "PLN guidance, so removal loses nothing real.",
        "action": "remove the whole <li>, do not substitute",
    },
]

# Verified 2026-07-16: 200 to a browser UA, 404/403 to a bot UA. Links to
# these hosts are NOT broken. Exclude them in Ahrefs; never 'fix' them.
BOT_BLOCKING_HOSTS = [
    "www.legislation.gov.uk",
    "www.thegazette.co.uk",
    "www.tax.service.gov.uk",
    "find-and-update.company-information.service.gov.uk",
    "www.citizensadvice.org.uk",
    "www.payplan.com",
    "www.ppf.co.uk",
    "www.trustonline.org.uk",
    "www.registry-trust.org.uk",
    "www.breathing-space.uk",
    "www.moneyandmentalhealth.org",
    "researchbriefings.files.parliament.uk",
]
