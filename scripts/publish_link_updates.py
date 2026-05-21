"""
Publish the 68 draft files modified by add_internal_links.py to WP staging.

Reads POST ID from the draft file header comment, then PATCHes the page
content via the WP REST API using requests + cookie-based auth.

Usage:
    python scripts/publish_link_updates.py [--dry-run]
"""

import os, re, sys, time, base64
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)

URL         = os.getenv("WP_STAGING_URL", "").rstrip("/")
HTTP_USER   = os.getenv("WP_BASIC_AUTH_USER", "")
HTTP_PASS   = os.getenv("WP_BASIC_AUTH_PASS", "")
WP_USER     = os.getenv("WP_USERNAME", os.getenv("WP_STAGING_USERNAME", ""))
WP_PASS     = os.getenv("WP_STAGING_APP_PASSWORD", "")
DRAFTS_DIR  = Path(__file__).parent.parent / "drafts"

MODIFIED_SLUGS = [
    "how-to-legally-take-money-out-of-a-limited-company",
    "insolvency-advice-for-directors",
    "the-risks-of-signing-a-personal-guarantee",
    "unenforceable-personal-guarantee",
    "what-is-limited-liability",
    "writing-off-a-directors-loan-account",
    "bounce-back-loan-fraud",
    "can-i-lose-my-house-with-a-bounce-back-loan",
    "directors-liability-for-bounce-back-loans",
    "dissolving-a-company-with-bounce-back-loan",
    "what-happens-if-i-default",
    "care-home-insolvency",
    "company-cash-flow-problems",
    "biggest-struggles-for-small-business-owners",
    "cant-afford-to-pay-suppliers-what-are-the-options",
    "cant-afford-to-repay-business-loan",
    "cant-pay-a-company-mortgage",
    "cant-pay-business-energy",
    "cant-pay-business-rates",
    "cant-pay-staff-wages",
    "challenge-a-statutory-demand",
    "company-is-having-financial-difficulties",
    "what-is-a-statutory-demand-against-a-company",
    "when-employers-cant-afford-redundancy-payments",
    "why-debt-is-not-always-a-bad-thing-for-your-business",
    "company-rescue-recovery-hub",
    "company-rescue-solutions",
    "debt-creditor-pressure-hub",
    "director-protection-hub",
    "hmrc",
    "accelerated-payment-notices-apn",
    "can-hmrc-shut-down-my-business",
    "controlled-goods-agreement",
    "hmrc-compliance-checks",
    "hmrc-debt-enforcement-hub",
    "hmrc-enforcement-action",
    "hmrc-threatening-letters",
    "joint-and-several-liability-for-unpaid-vat",
    "notice-of-enforcement",
    "pay-hmrc-or-suppliers-first",
    "personal-liability-notices",
    "tax-penalties",
    "understanding-hmrc-debt-collection",
    "what-happens-if-hmrc-freezes-your-business-bank-account",
    "what-happens-if-hmrc-rejects-your-time-to-pay-arrangement",
    "what-happens-if-hmrc-sends-bailiffs-to-a-business",
    "what-happens-if-you-ignore-hmrc-letters",
    "hospitality-restaurant-insolvency",
    "antecedent-transactions",
    "cease-trading",
    "creditor-negotiations",
    "creditors-meeting",
    "dealing-with-creditor-pressure",
    "find-a-liquidator-near-me",
    "how-to-reduce-insolvency-risk",
    "insolvency-act-1986",
    "insolvency-test",
    "personally-liabilty-of-company-secretary",
    "rescue-your-business-from-insolvency",
    "retail-industry-insolvency-trends",
    "what-happens-if-a-company-cannot-pay-its-debts",
    "what-is-a-freezing-order-or-injunction",
    "what-is-a-high-court-writ",
    "what-to-do-about-customer-insolvency",
    "manufacturing-insolvency",
    "request-a-reduced-monthly-payment",
    "sector-specific-insolvency",
    "dealing-with-an-hmrc-winding-up-petition",
]


def create_session():
    http_auth = (HTTP_USER, HTTP_PASS)
    session = requests.Session()
    session.headers["User-Agent"] = "Company Debt-Publisher/1.0"

    # Prime test cookie
    session.get(f"{URL}/wp-login.php", auth=http_auth, timeout=15)

    # Log in via wp-login.php
    resp = session.post(
        f"{URL}/wp-login.php",
        auth=http_auth,
        headers={"Referer": f"{URL}/wp-login.php", "Origin": URL},
        data={
            "log": WP_USER,
            "pwd": WP_PASS,
            "wp-submit": "Log In",
            "redirect_to": f"{URL}/wp-admin/",
            "testcookie": "1",
        },
        allow_redirects=True,
        timeout=30,
    )
    auth_cookies = [c.name for c in session.cookies if "wordpress_logged_in" in c.name]
    if not auth_cookies:
        print(f"ERROR: WP login failed (status {resp.status_code})")
        sys.exit(1)
    print("Logged in OK")

    # Get REST nonce
    admin = session.get(f"{URL}/wp-admin/", auth=http_auth, timeout=15)
    m = re.search(r'wpApiSettings[^}]+nonce["\s:]+\"([a-f0-9]+)\"', admin.text) \
     or re.search(r'"nonce":"([a-f0-9]+)"', admin.text)
    if not m:
        print("ERROR: Could not extract REST nonce")
        sys.exit(1)
    session.headers["X-WP-Nonce"] = m.group(1)
    session.auth = http_auth
    print("Nonce OK")
    return session


def find_draft(slug):
    for path in DRAFTS_DIR.glob(f"*_{slug}.html"):
        return path
    for path in DRAFTS_DIR.glob("art_*.html"):
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for _ in range(10):
                    line = fh.readline()
                    if "LINK:" in line and f"/{slug}/" in line:
                        return path
        except Exception:
            pass
    return None


def extract_post_id(path):
    with open(path, encoding="utf-8") as fh:
        for _ in range(10):
            line = fh.readline()
            m = re.search(r"POST ID:\s*(\d+)", line)
            if m:
                return int(m.group(1))
    return None


def extract_post_type(path):
    with open(path, encoding="utf-8") as fh:
        for _ in range(5):
            line = fh.readline()
            if "TYPE:" in line:
                return "posts" if "posts" in line else "pages"
    return "pages"


def extract_content(path):
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("<!--") and not s.startswith("<!-- wp:"):
            start = i + 1
        elif s == "" and start == i:
            start = i + 1
        else:
            break
    return "".join(lines[start:]).strip()


def main():
    dry_run = "--dry-run" in sys.argv

    if not URL:
        print("ERROR: WP_STAGING_URL not set")
        sys.exit(1)

    session = None
    if not dry_run:
        session = create_session()

    api_base = f"{URL}/wp-json/wp/v2"
    ok = fail = 0

    for slug in MODIFIED_SLUGS:
        draft = find_draft(slug)
        if not draft:
            print(f"  SKIP   {slug} — draft not found")
            fail += 1
            continue

        post_id   = extract_post_id(draft)
        post_type = extract_post_type(draft)
        content   = extract_content(draft)

        if not post_id:
            print(f"  SKIP   {slug} — no POST ID")
            fail += 1
            continue

        if dry_run:
            print(f"  DRY    {slug} (id={post_id}, {len(content):,} chars)")
            ok += 1
            continue

        resp = session.patch(
            f"{api_base}/{post_type}/{post_id}",
            json={"content": content},
            timeout=30,
        )
        data = resp.json() if resp.content else {}

        if resp.status_code in (200, 201) and data.get("id"):
            print(f"  OK     {slug} (id={post_id})")
            ok += 1
        else:
            err = data.get("message", data.get("code", resp.status_code))
            print(f"  FAIL   {slug} (id={post_id}) — {err}")
            fail += 1

        time.sleep(0.25)

    print(f"\nDone: {ok} published, {fail} failed/skipped")


if __name__ == "__main__":
    main()
