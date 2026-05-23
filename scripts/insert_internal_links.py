"""
Blank-slate internal-link insertion system for companydebt.com (staging).

All editorial internal links have already been stripped. This script rebuilds
them from scratch using the commercial routing logic in decide_links_for_page()
plus a strict anchor-relevance layer.

Workflow:
  1. python scripts/insert_internal_links.py            # dry run -> CSVs only
  2. review internal-links/companydebt-internal-links.csv
  3. python scripts/insert_internal_links.py --apply    # write to staging

Optional:
  --only <substr>   only process source pages whose slug contains <substr>
                    (use for phased, cluster-by-cluster rollout)

Credentials are read from .env only. Nothing is hardcoded.

Outputs:
  internal-links/companydebt-internal-links.csv     proposed links (dry-run preview)
  internal-links/rejected_anchor_opportunities.csv  candidates rejected, with reason
"""
import os, re, sys, csv, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from collections import Counter, defaultdict

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


# ---------------------------------------------------------------------------
# Credentials (from .env only)
# ---------------------------------------------------------------------------

def env(key):
    val = os.getenv(key)
    if not val:
        sys.exit(f'Missing required .env key: {key}')
    return val

STAGING_URL = env('WP_STAGING_URL').rstrip('/')
BA_USER     = env('WP_BASIC_AUTH_USER')
BA_PASS     = env('WP_BASIC_AUTH_PASS')
WP_USER     = env('WP_STAGING_USERNAME')
WP_APP_PASS = env('WP_STAGING_APP_PASSWORD')

APPLY = '--apply' in sys.argv
ONLY  = None
if '--only' in sys.argv:
    ONLY = sys.argv[sys.argv.index('--only') + 1].lower()

INVENTORY_FILE = 'staging_page_inventory.json'
OUT_DIR        = 'internal-links'
OUT_CSV        = os.path.join(OUT_DIR, 'companydebt-internal-links.csv')
REJECT_CSV     = os.path.join(OUT_DIR, 'rejected_anchor_opportunities.csv')


# ---------------------------------------------------------------------------
# Target validation / remapping / classification helpers
# ---------------------------------------------------------------------------

# Missing-from-staging targets remapped to nearest validated equivalent.
TARGET_REMAP = {
    '/close-a-limited-company-with-debts/': '/closing-a-limited-company/',
}

HUB_TARGETS = {
    '/liquidation/', '/hmrc/', '/company-rescue-solutions/',
    '/company-rescue-recovery-hub/', '/debt-creditor-pressure-hub/',
    '/bounce-back-loan-support-hub/', '/insolvency/',
}
CTA_TARGETS = {'/quick-quote/', '/contact-us/'}

# Intent guard: matched anchor for these targets must contain a close-intent
# token, otherwise it is rejected as anchor_too_broad. Targets not listed here
# rely on their curated anchor variants alone.
TARGET_INTENT = {
    '/winding-up-petitions/': [
        'winding-up petition', 'winding up petition', 'wind up the company',
        'petition to wind up', 'creditor petition', 'court petition',
        'compulsory liquidation',
    ],
    '/winding-up-petitions/dealing-with-an-hmrc-winding-up-petition/': [
        'hmrc winding-up', 'hmrc winding up', 'hmrc petition', 'hmrc winding-up risk',
    ],
    '/liquidation/creditors-voluntary-liquidation/': [
        "creditors' voluntary liquidation", 'cvl', 'voluntary liquidation',
        'appoint a liquidator', 'liquidate the company voluntarily',
    ],
    '/hmrc/time-to-pay-hmrc/': [
        'time to pay', 'payment plan', 'instalment', 'pay hmrc arrears over time',
        'negotiate payment terms',
    ],
    '/director-redundancy/': [
        'director redundancy', 'redundancy payments for directors',
        'redundancy as a director', 'redundancy after liquidation',
        "directors' redundancy",
    ],
    '/hmrc/cant-pay-vat/': ['vat'],
    '/hmrc/cant-pay-paye/': ['paye', 'payroll'],
    '/hmrc/problems-paying-corporation-tax-hmrc/': ['corporation tax'],
    '/quick-quote/': ['quote', 'cost estimate'],
    '/contact-us/': ['speak to', 'contact', 'adviser', 'advice'],
}

HUB_SLUGS = {
    'liquidation', 'hmrc', 'company-rescue-solutions', 'company-rescue-recovery-hub',
    'debt-creditor-pressure-hub', 'bounce-back-loan-support-hub',
    'sector-insolvency-hub', 'advice', 'insolvency',
}
LEGAL_SLUGS = {
    'privacy-policy', 'terms-conditions', 'cookie-policy', 'cookie-policy-company-debt',
    'accessibility', 'content-usage-guidelines', 'site-map', 'accreditations',
    'useful-publications',
}
CONTACT_SLUGS = {'contact-us', 'quick-quote'}
QUESTION_PREFIXES = ('what-', 'can-', 'how-', 'should-', 'is-', 'do-', 'does-',
                     'will-', 'are-', 'when-', 'why-', 'who-')


def classify(slug, word_count):
    if slug in CONTACT_SLUGS:
        return 'contact'
    if slug in LEGAL_SLUGS:
        return 'legal'
    if slug in HUB_SLUGS or slug.endswith('-hub'):
        return 'hub'
    if slug.startswith(QUESTION_PREFIXES) and word_count and word_count < 700:
        return 'faq'
    return 'informational'


def cluster_of(target):
    if target in CTA_TARGETS:
        return 'CTA'
    if target.startswith('/hmrc'):
        return 'HMRC'
    if target.startswith(('/liquidation', '/closing-a-limited-company',
                          '/winding-up-petitions', '/director-redundancy')):
        return 'Closure & Liquidation'
    if target.startswith(('/company-rescue', '/company-administration',
                          '/what-is-a-pre-pack')):
        return 'Rescue & Recovery'
    if target.startswith('/debt-creditor-pressure'):
        return 'Creditor Pressure'
    if target.startswith('/advice'):
        return 'Director Risk'
    if target.startswith('/bounce-back-loan'):
        return 'Bounce Back Loan'
    if target.startswith('/insolvency'):
        return 'Insolvency'
    return 'Other'


def role_of(target):
    if target in CTA_TARGETS:
        return 'cta'
    if target in HUB_TARGETS:
        return 'hub'
    return 'spoke'


# ===========================================================================
# COMMERCIAL ROUTING FUNCTION (first-draft, per client brief)
# ===========================================================================

def decide_links_for_page(slug, page_type, word_count, content_text):
    """
    Return an ordered list of (target_path, [anchor variants]) tuples.

    This is the commercial routing layer for the blank-slate CompanyDebt
    internal-link rebuild. It should be used to generate candidate links only.
    The insertion layer must still check that an anchor exists naturally in the
    source copy, that the target URL is valid, and that page-level link caps are
    not exceeded.
    """

    slug = (slug or "").lower()
    page_type = (page_type or "").lower()
    text = (content_text or "").lower()

    links = []

    def add(target, anchors):
        if target not in [t for t, _ in links]:
            links.append((target, anchors))

    def has_any(terms):
        return any(term in slug or term in text for term in terms)

    def is_hub():
        return page_type == "hub" or slug in {
            "liquidation",
            "hmrc",
            "company-rescue-solutions",
            "company-rescue-recovery-hub",
            "debt-creditor-pressure-hub",
            "bounce-back-loan-support-hub",
            "sector-insolvency-hub",
            "advice",
            "insolvency",
        }

    # Do not add normal body links to utility/contact/legal pages unless very light.
    if page_type in {"contact", "utility"}:
        return []

    if page_type == "legal":
        return []

    # -------------------------
    # Core hub pages
    # -------------------------

    if slug == "liquidation":
        add("/liquidation/creditors-voluntary-liquidation/", [
            "Creditors’ Voluntary Liquidation",
            "CVL",
            "voluntary liquidation for an insolvent company",
        ])
        add("/liquidation/how-much-does-liquidation-cost/", [
            "liquidation costs",
            "cost of liquidation",
            "company liquidation fees",
        ])
        add("/liquidation/compulsory-liquidation/", [
            "compulsory liquidation",
            "forced company liquidation",
            "court-ordered liquidation",
        ])
        add("/liquidation/company-strike-off-and-dissolution/", [
            "company strike off",
            "strike off and dissolution",
            "dissolving a company",
        ])
        add("/liquidation/members-voluntary-liquidation/", [
            "Members’ Voluntary Liquidation",
            "MVL",
            "solvent liquidation",
        ])
        add("/director-redundancy/", [
            "director redundancy pay",
            "redundancy payments for directors",
            "director redundancy claim",
        ])
        return links

    if slug == "hmrc":
        add("/hmrc/time-to-pay-hmrc/", [
            "HMRC Time to Pay arrangement",
            "Time to Pay arrangement",
            "HMRC payment plan",
        ])
        add("/hmrc/cant-pay-vat/", [
            "can’t pay VAT",
            "VAT arrears",
            "unpaid VAT",
        ])
        add("/hmrc/problems-paying-corporation-tax-hmrc/", [
            "can’t pay Corporation Tax",
            "Corporation Tax arrears",
            "unpaid Corporation Tax",
        ])
        add("/hmrc/cant-pay-paye/", [
            "can’t pay PAYE",
            "PAYE arrears",
            "unpaid PAYE",
        ])
        add("/hmrc/hmrc-debt-enforcement-hub/", [
            "HMRC debt enforcement",
            "HMRC enforcement action",
            "HMRC debt collection",
        ])
        add("/winding-up-petitions/dealing-with-an-hmrc-winding-up-petition/", [
            "HMRC winding-up petition",
            "HMRC petition threat",
            "HMRC winding-up risk",
        ])
        return links

    if slug == "company-rescue-solutions":
        add("/company-rescue-solutions/company-voluntary-arrangement/", [
            "Company Voluntary Arrangement",
            "CVA",
            "company voluntary arrangement",
        ])
        add("/company-administration/", [
            "company administration",
            "going into administration",
            "administration process",
        ])
        add("/what-is-a-pre-pack-administration/", [
            "pre-pack administration",
            "pre-pack sale",
            "pre-pack process",
        ])
        add("/company-rescue-recovery-hub/", [
            "company rescue and recovery",
            "business recovery options",
            "rescue and recovery options",
        ])
        return links

    if slug == "bounce-back-loan-support-hub":
        add("/liquidation/can-i-liquidate-my-company-with-a-bounce-back-loan/", [
            "liquidate a company with a Bounce Back Loan",
            "company liquidation with a Bounce Back Loan",
            "Bounce Back Loan in liquidation",
        ])
        add("/bounce-back-loan-support-hub/what-happens-if-i-default/", [
            "default on a Bounce Back Loan",
            "Bounce Back Loan default",
            "BBL default consequences",
        ])
        add("/bounce-back-loan-support-hub/directors-liability-for-bounce-back-loans/", [
            "directors’ liability for Bounce Back Loans",
            "personal liability for Bounce Back Loans",
            "director liability for BBLs",
        ])
        add("/bounce-back-loan-support-hub/dissolving-a-company-with-bounce-back-loan/", [
            "dissolve a company with a Bounce Back Loan",
            "strike off with a Bounce Back Loan",
            "Bounce Back Loan strike-off risk",
        ])
        add("/liquidation/creditors-voluntary-liquidation/", [
            "Creditors’ Voluntary Liquidation",
            "CVL",
            "voluntary liquidation",
        ])
        return links

    # -------------------------
    # HMRC and tax debt pages
    # -------------------------

    if has_any(["hmrc", "vat", "paye", "corporation tax", "tax arrears", "tax debt"]):
        if has_any([
            "winding-up",
            "winding up",
            "petition",
            "bailiff",
            "enforcement",
            "cannot pay",
            "can’t pay",
            "can't pay",
            "insolvent",
            "liquidation",
            "failed time to pay",
            "rejects your time to pay",
            "unable to pay",
        ]):
            add("/liquidation/creditors-voluntary-liquidation/", [
                "Creditors’ Voluntary Liquidation",
                "CVL",
                "voluntary liquidation",
            ])
            add("/winding-up-petitions/", [
                "winding-up petition",
                "winding up petition",
                "company winding-up petition",
            ])
            add("/liquidation/", [
                "company liquidation",
                "liquidating an insolvent company",
                "formal company liquidation",
            ])
        else:
            add("/hmrc/time-to-pay-hmrc/", [
                "HMRC Time to Pay arrangement",
                "HMRC payment plan",
                "tax debt payment plan",
            ])
            add("/hmrc/", [
                "HMRC tax debt",
                "HMRC tax problems",
                "company tax arrears",
            ])
            add("/company-rescue-solutions/company-voluntary-arrangement/", [
                "Company Voluntary Arrangement",
                "CVA",
                "restructure company debts through a CVA",
            ])

        if has_any(["vat"]):
            add("/hmrc/cant-pay-vat/", [
                "can’t pay VAT",
                "VAT arrears",
                "unpaid VAT",
            ])

        if has_any(["paye", "payroll", "national insurance", "nic"]):
            add("/hmrc/cant-pay-paye/", [
                "can’t pay PAYE",
                "PAYE arrears",
                "payroll tax arrears",
            ])

        if has_any(["corporation tax"]):
            add("/hmrc/problems-paying-corporation-tax-hmrc/", [
                "can’t pay Corporation Tax",
                "Corporation Tax arrears",
                "unpaid Corporation Tax",
            ])

    # -------------------------
    # Liquidation / CVL / closure pages
    # -------------------------

    if has_any(["cvl", "creditors voluntary liquidation", "creditors’ voluntary liquidation"]):
        add("/liquidation/", [
            "company liquidation",
            "liquidation process",
            "formal company liquidation",
        ])
        add("/liquidation/how-much-does-liquidation-cost/", [
            "liquidation costs",
            "CVL costs",
            "company liquidation fees",
        ])
        add("/director-redundancy/", [
            "director redundancy pay",
            "redundancy payments for directors",
            "director redundancy claim",
        ])
        add("/advice/overdrawn-directors-loan-accounts/", [
            "overdrawn director’s loan account",
            "overdrawn directors’ loan accounts",
            "director’s loan account debt",
        ])
        add("/advice/directors-personal-guarantees/", [
            "personal guarantees",
            "directors’ personal guarantees",
            "personal guarantee risks",
        ])

    elif has_any(["liquidation", "liquidate", "insolvent liquidation"]):
        add("/liquidation/creditors-voluntary-liquidation/", [
            "Creditors’ Voluntary Liquidation",
            "CVL",
            "voluntary liquidation",
        ])
        add("/liquidation/how-much-does-liquidation-cost/", [
            "liquidation costs",
            "cost of liquidation",
            "company liquidation fees",
        ])
        add("/director-redundancy/", [
            "director redundancy pay",
            "redundancy payments for directors",
            "director redundancy claim",
        ])
        add("/advice/are-directors-personally-liable-for-company-debts/", [
            "directors personally liable for company debts",
            "director personal liability",
            "personal liability for company debts",
        ])

    if has_any(["closing", "close", "closure", "shutting down", "shut down"]):
        if has_any(["debt", "debts", "owes money", "cannot pay", "can’t pay", "can't pay", "insolvent"]):
            add("/close-a-limited-company-with-debts/", [
                "close a limited company with debts",
                "closing a company with debts",
                "close a company that still owes money",
            ])
            add("/liquidation/creditors-voluntary-liquidation/", [
                "Creditors’ Voluntary Liquidation",
                "CVL",
                "close the company through a CVL",
            ])
        else:
            add("/closing-a-limited-company/", [
                "closing a limited company",
                "company closure options",
                "how to close a company",
            ])
            add("/liquidation/company-strike-off-and-dissolution/", [
                "company strike off",
                "strike off and dissolution",
                "dissolving a company",
            ])
            add("/liquidation/members-voluntary-liquidation/", [
                "Members’ Voluntary Liquidation",
                "MVL",
                "solvent liquidation",
            ])

    # -------------------------
    # Creditor pressure / winding-up pages
    # -------------------------

    if has_any(["creditor", "supplier", "statutory demand", "winding-up", "winding up", "court", "ccj", "bailiff", "enforcement"]):
        add("/debt-creditor-pressure-hub/", [
            "creditor pressure",
            "debt and creditor pressure",
            "creditor enforcement",
        ])
        add("/winding-up-petitions/", [
            "winding-up petition",
            "winding up petition",
            "petition to wind up a company",
        ])
        add("/liquidation/creditors-voluntary-liquidation/", [
            "Creditors’ Voluntary Liquidation",
            "CVL",
            "voluntary liquidation",
        ])
        add("/advice/are-directors-personally-liable-for-company-debts/", [
            "director personal liability",
            "directors personally liable for company debts",
            "personal liability for company debts",
        ])

    # -------------------------
    # Rescue / recovery pages
    # -------------------------

    if has_any(["rescue", "turnaround", "restructure", "restructuring", "administration", "cva", "pre-pack", "pre pack", "recovery"]):
        add("/company-rescue-solutions/", [
            "company rescue solutions",
            "company rescue",
            "business rescue options",
        ])
        add("/company-rescue-solutions/company-voluntary-arrangement/", [
            "Company Voluntary Arrangement",
            "CVA",
            "company voluntary arrangement",
        ])
        add("/company-administration/", [
            "company administration",
            "going into administration",
            "administration process",
        ])

        if has_any(["pre-pack", "pre pack"]):
            add("/what-is-a-pre-pack-administration/", [
                "pre-pack administration",
                "pre-pack sale",
                "pre-pack process",
            ])

        if has_any(["failed", "cannot continue", "can’t continue", "can't continue", "no longer viable", "liquidation"]):
            add("/liquidation/creditors-voluntary-liquidation/", [
                "Creditors’ Voluntary Liquidation",
                "CVL",
                "voluntary liquidation",
            ])

    # -------------------------
    # Director liability / personal exposure pages
    # -------------------------

    if has_any(["director", "personal guarantee", "personally liable", "personal liability", "overdrawn", "loan account", "disqualification", "misfeasance", "phoenix", "house", "home"]):
        add("/advice/are-directors-personally-liable-for-company-debts/", [
            "directors personally liable for company debts",
            "director personal liability",
            "personal liability for company debts",
        ])
        add("/advice/directors-personal-guarantees/", [
            "directors’ personal guarantees",
            "personal guarantees",
            "personal guarantee risks",
        ])
        add("/advice/overdrawn-directors-loan-accounts/", [
            "overdrawn director’s loan account",
            "overdrawn directors’ loan accounts",
            "director’s loan account debt",
        ])

        if has_any(["house", "home", "property"]):
            add("/advice/losing-house-if-company-goes-bust/", [
                "losing your house if the company goes bust",
                "personal assets at risk",
                "house risk in company insolvency",
            ])

        add("/liquidation/creditors-voluntary-liquidation/", [
            "Creditors’ Voluntary Liquidation",
            "CVL",
            "voluntary liquidation",
        ])

    # -------------------------
    # Bounce Back Loan / CBILS legacy pages
    # -------------------------

    if has_any(["bounce back loan", "bbl", "cbils", "coronavirus business interruption loan"]):
        add("/bounce-back-loan-support-hub/", [
            "Bounce Back Loan support",
            "Bounce Back Loan help",
            "Bounce Back Loan options",
        ])
        add("/liquidation/can-i-liquidate-my-company-with-a-bounce-back-loan/", [
            "liquidate a company with a Bounce Back Loan",
            "company liquidation with a Bounce Back Loan",
            "Bounce Back Loan in liquidation",
        ])
        add("/bounce-back-loan-support-hub/what-happens-if-i-default/", [
            "default on a Bounce Back Loan",
            "Bounce Back Loan default",
            "BBL default consequences",
        ])
        add("/bounce-back-loan-support-hub/directors-liability-for-bounce-back-loans/", [
            "directors’ liability for Bounce Back Loans",
            "personal liability for Bounce Back Loans",
            "director liability for BBLs",
        ])
        add("/close-a-limited-company-with-debts/", [
            "close a limited company with debts",
            "closing a company with debts",
            "close a company that still owes money",
        ])

    # -------------------------
    # Sector pages
    # -------------------------

    if has_any(["sector", "hospitality", "construction", "retail", "transport", "manufacturing", "care home", "professional services", "charity", "entertainment"]):
        add("/company-rescue-solutions/", [
            "company rescue solutions",
            "business rescue options",
            "rescue options for struggling companies",
        ])
        add("/liquidation/creditors-voluntary-liquidation/", [
            "Creditors’ Voluntary Liquidation",
            "CVL",
            "liquidation for insolvent companies",
        ])
        add("/hmrc/", [
            "HMRC tax debt",
            "HMRC tax problems",
            "company tax arrears",
        ])
        add("/advice/are-directors-personally-liable-for-company-debts/", [
            "director personal liability",
            "directors personally liable for company debts",
            "personal liability for company debts",
        ])

    # -------------------------
    # Generic insolvency basics
    # -------------------------

    if has_any(["insolvency", "insolvent", "cannot pay its debts", "can’t pay its debts", "can't pay its debts"]):
        add("/insolvency/", [
            "company insolvency",
            "what is insolvency",
            "insolvent company",
        ])
        add("/insolvency/check-if-a-company-is-insolvent/", [
            "check if a company is insolvent",
            "insolvency test",
            "test for insolvency",
        ])
        add("/liquidation/", [
            "company liquidation",
            "liquidating an insolvent company",
            "formal company liquidation",
        ])
        add("/liquidation/creditors-voluntary-liquidation/", [
            "Creditors’ Voluntary Liquidation",
            "CVL",
            "voluntary liquidation",
        ])

    # -------------------------
    # CTA links only for late-stage pages
    # -------------------------

    if has_any([
        "cost",
        "quote",
        "urgent",
        "petition",
        "liquidation cost",
        "liquidation fees",
        "close the company",
        "enter liquidation",
        "appoint a liquidator",
    ]):
        add("/quick-quote/", [
            "get an insolvency quote",
            "request a liquidation quote",
            "get a liquidation cost estimate",
        ])

    if has_any([
        "speak to",
        "advice",
        "urgent",
        "personal liability",
        "winding-up petition",
        "director risk",
        "complex",
    ]):
        add("/contact-us/", [
            "speak to an insolvency adviser",
            "contact an insolvency practitioner",
            "get confidential insolvency advice",
        ])

    # -------------------------
    # Link count caps
    # -------------------------

    if page_type == "faq":
        max_links = 3
    elif page_type == "commercial":
        max_links = 6
    elif page_type == "hub":
        max_links = 10
    elif word_count and word_count < 700:
        max_links = 2
    elif word_count and word_count < 1400:
        max_links = 4
    else:
        max_links = 7

    return links[:max_links]


# ===========================================================================
# Anchor matching + placement engine
# ===========================================================================

APOS_CLASS = r"(?:['‘’ʼ]|&#8217;|&#8216;|&#039;|&rsquo;|&lsquo;|&apos;)"

ELIGIBLE_BLOCK_RE = re.compile(
    r'<!-- wp:(paragraph|list)(?: \{[^}]*\})? -->(.*?)<!-- /wp:\1 -->',
    re.DOTALL)
INNER_EL_RE = re.compile(r'<(p|li)\b[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
A_TAG_RE    = re.compile(r'<a\b[^>]*>.*?</a>', re.DOTALL | re.IGNORECASE)
TAG_RE      = re.compile(r'<[^>]+>')


def norm(text):
    """Normalise apostrophes/whitespace for intent comparison."""
    text = re.sub(r"['‘’ʼ]", "'", text)
    text = re.sub(r'&#8217;|&#8216;|&#039;|&rsquo;|&lsquo;|&apos;', "'", text)
    return re.sub(r'\s+', ' ', text).strip().lower()


def build_anchor_regex(anchor):
    """Compile a regex that matches the anchor allowing apostrophe/space variants."""
    parts = []
    for ch in anchor.strip():
        if ch in "'‘’ʼ":
            parts.append(APOS_CLASS)
        elif ch.isspace():
            parts.append(r'\s+')
        else:
            parts.append(re.escape(ch))
    body = ''.join(parts)
    return re.compile(r'(?<![A-Za-z0-9])' + body + r'(?![A-Za-z0-9])', re.IGNORECASE)


def get_paragraphs(raw):
    """Return list of (para_id, text_start, text_end) for eligible paragraph/list text."""
    paragraphs = []
    for bm in ELIGIBLE_BLOCK_RE.finditer(raw):
        body_start = bm.start(2)
        for em in INNER_EL_RE.finditer(bm.group(2)):
            paragraphs.append((len(paragraphs),
                               body_start + em.start(2),
                               body_start + em.end(2)))
    return paragraphs


def intent_ok(target, matched_text):
    """True if the matched anchor closely matches the target's intent."""
    tokens = TARGET_INTENT.get(target)
    if not tokens:
        return True
    m = norm(matched_text)
    return any(norm(tok) in m for tok in tokens)


def context_snippet(raw, start, end):
    before = TAG_RE.sub('', raw[max(0, start - 90):start])
    anchor = TAG_RE.sub('', raw[start:end])
    after  = TAG_RE.sub('', raw[end:end + 90])
    snip = f'{before}[[{anchor}]]{after}'
    return re.sub(r'\s+', ' ', snip).strip()


def plan_page(raw, candidates, own_path, valid_paths):
    """
    Returns (placements, rejections).
      placements: list of dicts with target, anchor, start, end, context
      rejections: list of dicts with target, anchor, reason
    """
    paragraphs = get_paragraphs(raw)
    used_paras = set()
    placements = []
    rejections = []

    for target, anchors in candidates:
        real_target = TARGET_REMAP.get(target, target)
        remapped = real_target != target

        # Skip self-links and invalid targets silently (not an anchor fault).
        if real_target == own_path:
            continue
        if real_target not in valid_paths:
            continue

        chosen = None
        appeared_anchor = None
        best_reason = 'anchor_absent_from_copy'

        for anchor in anchors:
            rx = build_anchor_regex(anchor)
            for para_id, ts, te in paragraphs:
                para_text_abs = (ts, te)
                a_spans = [(m.start(), m.end())
                           for m in A_TAG_RE.finditer(raw, ts, te)]
                for hm in rx.finditer(raw, ts, te):
                    s, e = hm.start(), hm.end()
                    inside_a = any(a_s <= s and e <= a_e for a_s, a_e in a_spans)
                    if appeared_anchor is None:
                        appeared_anchor = anchor
                    if inside_a:
                        best_reason = 'anchor_already_linked'
                        continue
                    if para_id in used_paras:
                        best_reason = 'placement_forbidden'
                        continue
                    if not intent_ok(real_target, raw[s:e]):
                        best_reason = 'anchor_too_broad'
                        continue
                    chosen = (real_target, raw[s:e], s, e, para_id, remapped)
                    break
                if chosen:
                    break
            if chosen:
                break

        if chosen:
            t, anchor_text, s, e, para_id, was_remapped = chosen
            used_paras.add(para_id)
            placements.append({
                'target': t,
                'anchor': anchor_text,
                'start': s,
                'end': e,
                'context': context_snippet(raw, s, e),
                'notes': (f'target remapped from {target}' if was_remapped else ''),
            })
        else:
            rejections.append({
                'target': real_target,
                'anchor': appeared_anchor or (anchors[0] if anchors else ''),
                'reason': best_reason,
            })

    return placements, rejections


def apply_placements(raw, placements):
    """Insert <a> tags for all placements. Process descending so offsets hold."""
    for p in sorted(placements, key=lambda x: x['start'], reverse=True):
        s, e = p['start'], p['end']
        raw = raw[:s] + f'<a href="{p["target"]}">' + raw[s:e] + '</a>' + raw[e:]
    return raw


# ===========================================================================
# WordPress REST client
# ===========================================================================

def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-LinkInsert/1.0'
    return s


def wp_login(session):
    login_url = f'{STAGING_URL}/wp-login.php'
    session.get(login_url, params={'wpe-login': 'true'})
    session.post(login_url, params={'wpe-login': 'true'}, data={
        'log': WP_USER, 'pwd': WP_APP_PASS,
        'wp-submit': 'Log In', 'testcookie': '1',
    }, allow_redirects=True)


def get_nonce(session):
    r = session.get(f'{STAGING_URL}/wp-admin/', timeout=30)
    for pattern in (r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r'"nonce":"([a-f0-9]+)"'):
        m = re.search(pattern, r.text)
        if m:
            return m.group(1)
    raise RuntimeError('Could not extract WP nonce')


def fetch_all_content(session, nonce):
    items = []
    for post_type in ('posts', 'pages'):
        page = 1
        while True:
            r = session.get(
                f'{STAGING_URL}/wp-json/wp/v2/{post_type}',
                params={'per_page': 100, 'page': page, 'status': 'publish',
                        'context': 'edit', '_fields': 'id,slug,link,type,content'},
                headers={'X-WP-Nonce': nonce},
                timeout=60,
            )
            if r.status_code == 400:
                break
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            for it in batch:
                items.append({
                    'id': it['id'],
                    'slug': it['slug'],
                    'type': it['type'],
                    'link': it.get('link', ''),
                    'raw': it.get('content', {}).get('raw', ''),
                    'rendered': it.get('content', {}).get('rendered', ''),
                })
            if len(batch) < 100:
                break
            page += 1
    return items


def patch_content(session, post_type, post_id, raw_content, nonce):
    endpoint = 'posts' if post_type == 'post' else 'pages'
    r = session.post(
        f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
        json={'content': raw_content},
        headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


# ===========================================================================
# Main
# ===========================================================================

def path_of(link):
    return (link.replace('https://comdebstage.wpengine.com', '')
                .replace('https://www.companydebt.com', '')
                .replace('http://comdebstage.wpengine.com', '') or '/')


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    if not os.path.exists(INVENTORY_FILE):
        sys.exit(f'Missing {INVENTORY_FILE} — run the inventory step first.')
    with open(INVENTORY_FILE, encoding='utf-8') as f:
        valid_paths = set(json.load(f).keys())

    mode = 'APPLY' if APPLY else 'DRY RUN'
    print(f'=== Internal link insertion — {mode} ===')
    if ONLY:
        print(f'Filter: source slug contains "{ONLY}"')
    print()

    session = api_session()
    print('Logging in to staging...')
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...\n')

    print('Fetching all published content...')
    items = fetch_all_content(session, nonce)
    print(f'  {len(items)} posts/pages\n')

    all_links = []
    all_rejections = []
    pages_with_links = 0
    pages_zero = 0

    for item in items:
        slug = item['slug']
        if ONLY and ONLY not in slug.lower():
            continue
        raw = item['raw']
        if not raw:
            continue

        content_text = TAG_RE.sub(' ', item['rendered'])
        word_count = len(content_text.split())
        page_type = classify(slug, word_count)
        own_path = path_of(item['link'])

        candidates = decide_links_for_page(slug, page_type, word_count, content_text)
        if not candidates:
            pages_zero += 1
            continue

        placements, rejections = plan_page(raw, candidates, own_path, valid_paths)

        live_url = 'https://www.companydebt.com' + own_path
        for p in placements:
            all_links.append({
                'source_url': live_url,
                'source_slug': slug,
                'source_page_type': page_type,
                'source_word_count': word_count,
                'target_url': p['target'],
                'target_role': role_of(p['target']),
                'cluster': cluster_of(p['target']),
                'anchor_text': p['anchor'],
                'context_snippet': p['context'],
                'notes': p['notes'],
                '_id': item['id'],
                '_type': item['type'],
                '_start': p['start'],
                '_end': p['end'],
            })
        for r in rejections:
            all_rejections.append({
                'source_url': live_url,
                'target_url': r['target'],
                'rejected_anchor': r['anchor'],
                'reason': r['reason'],
            })

        if placements:
            pages_with_links += 1
        else:
            pages_zero += 1

    # ----- write proposed-links CSV -----
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'source_url', 'source_slug', 'source_page_type', 'source_word_count',
            'target_url', 'target_role', 'cluster', 'anchor_text',
            'context_snippet', 'notes'])
        w.writeheader()
        for row in all_links:
            w.writerow({k: row[k] for k in w.fieldnames})

    # ----- write rejected CSV -----
    with open(REJECT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'source_url', 'target_url', 'rejected_anchor', 'reason'])
        w.writeheader()
        for row in all_rejections:
            w.writerow(row)

    # ----- summary -----
    print('--- SUMMARY ---')
    print(f'Proposed links:   {len(all_links)}')
    print(f'Pages with links: {pages_with_links}')
    print(f'Pages with none:  {pages_zero}')
    print(f'Rejected:         {len(all_rejections)}')
    print()
    print('By cluster:')
    for cl, n in Counter(r['cluster'] for r in all_links).most_common():
        print(f'  {cl}: {n}')
    print()
    print('Top targets:')
    for t, n in Counter(r['target_url'] for r in all_links).most_common(12):
        print(f'  {n:>3}  {t}')
    print()
    print('Rejections by reason:')
    for reason, n in Counter(r['reason'] for r in all_rejections).most_common():
        print(f'  {n:>3}  {reason}')
    print()
    print(f'Outputs:')
    print(f'  {OUT_CSV}')
    print(f'  {REJECT_CSV}')

    # ----- apply -----
    if APPLY:
        print('\n--- APPLYING ---')
        by_page = defaultdict(list)
        for row in all_links:
            by_page[(row['_id'], row['_type'], row['source_slug'])].append(row)
        patched = 0
        for (pid, ptype, pslug), rows in by_page.items():
            item = next(i for i in items if i['id'] == pid)
            placements = [{'target': r['target_url'], 'start': r['_start'],
                           'end': r['_end']} for r in rows]
            new_raw = apply_placements(item['raw'], placements)
            if new_raw != item['raw']:
                status = patch_content(session, ptype, pid, new_raw, nonce)
                patched += 1
                print(f'  [{pslug}] +{len(rows)} link(s) (HTTP {status})')
                time.sleep(0.15)
        print(f'\nApplied links to {patched} pages.')
    else:
        print('\nDry run complete. Review the CSV, then re-run with --apply.')


if __name__ == '__main__':
    main()
