"""Guard: is the Consent Mode default snippet un-delayed and ahead of GTM?

Why this exists
---------------
WP Rocket's "delay JavaScript execution" rewrites inline scripts to
``type="text/rocketlazyloadscript"`` and holds them until the visitor's first
interaction. Three things must all be true for the site to measure correctly
*and* lawfully:

1. The Consent Mode v2 *default* snippet (``data-cd-consent-default="1"`` in
   header.php) must render UN-DELAYED. A delayed default is not a default at
   all -- Google tags would initialise with no consent state and write
   ``_ga`` / ``_gcl_*`` before the visitor answers the banner.
2. That snippet must come BEFORE the GTM loader in the HTML.
3. The GTM loader must itself be UN-DELAYED, otherwise a visitor who never
   scrolls or clicks sends no signal at all -- not even the anonymous cookieless
   ping that feeds Google's conversion modelling.

Condition 3 without conditions 1 and 2 is the dangerous combination. Run this
before and after any WP Rocket, header.php or consent change, and always before
and after a staging -> live push.

Usage
-----
    python scripts/check_consent_tag_order.py                  # staging homepage
    python scripts/check_consent_tag_order.py --target live
    python scripts/check_consent_tag_order.py --path /contact-us/

Exits non-zero if any check fails, so it can gate a deploy.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time

import requests
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_env() -> None:
    """Load .env from the checkout, or from the main project when run inside a
    git worktree. Worktrees live at <project>/.claude/worktrees/<name>/ and do
    not carry .env, so resolve back to the project root rather than failing with
    a bare KeyError on SFTP_HOST / WP_BASIC_AUTH_USER."""
    candidates = [os.path.join(ROOT, ".env")]
    marker = os.path.join(".claude", "worktrees")
    if marker in ROOT:
        project = ROOT.split(marker)[0].rstrip(os.sep)
        candidates.append(os.path.join(project, ".env"))
    for path in candidates:
        if os.path.isfile(path):
            load_dotenv(path)
            return


_load_env()

LIVE = "https://www.companydebt.com"
UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}

# The attribute, not the marker comment. The comment above the snippet also
# contains the words "cd-consent-default", which will silently match the wrong
# <script> tag and produce a bogus failure.
CONSENT_ATTR = 'data-cd-consent-default="1"'
GTM_ID = "GTM-5GTD9ZP"
CAPTURE_ATTR = 'data-cd-lc="1"'
DELAYED = "rocketlazyloadscript"


def enclosing_script_tag(html: str, needle: str) -> str | None:
    """Return the opening <script ...> tag that contains `needle`, or None."""
    i = html.find(needle)
    if i < 0:
        return None
    start = html.rfind("<script", 0, i)
    if start < 0:
        return None
    end = html.find(">", start)
    if end < 0:
        return None
    tag = html[start:end + 1]
    # Guard against walking back past an earlier, unrelated script.
    if needle not in tag and html.find("</script>", start, i) != -1:
        return None
    return tag


# HTML comments are stripped before any position is measured. A comment that
# merely MENTIONS the container id was found first by html.find(), so this guard
# reported the GTM loader as missing and delayed while the real loader sat
# further down, plainly un-delayed. The header comment added on 25 Aug 2026
# documenting the CookieYes wiring did exactly that. A guard a code comment can
# break is worse than no guard: it fails loudly and wrongly, and the next person
# spends an hour chasing a fault that is not there.
COMMENT = re.compile(r"<!--.*?-->", re.S)


def strip_comments(html: str) -> str:
    """Blank out HTML comments, keeping length so offsets stay comparable."""
    return COMMENT.sub(lambda m: " " * len(m.group(0)), html)


def fetch(base: str, path: str, auth) -> str:
    url = base.rstrip("/") + path
    requests.get(url, auth=auth, headers=UA, timeout=60)  # warm any page cache
    time.sleep(2)
    r = requests.get(url, auth=auth, headers=UA, timeout=60)
    r.raise_for_status()
    return r.text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=("staging", "live"), default="staging")
    ap.add_argument("--path", default="/")
    args = ap.parse_args()

    if args.target == "live":
        base, auth = LIVE, None
    else:
        base = os.environ["WP_STAGING_URL"]
        auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])

    raw = fetch(base, args.path, auth)
    html = strip_comments(raw)

    pos_consent = html.find(CONSENT_ATTR)
    pos_gtm = html.find(GTM_ID)
    consent_tag = enclosing_script_tag(html, CONSENT_ATTR)
    gtm_tag = enclosing_script_tag(html, GTM_ID)
    capture_tag = enclosing_script_tag(html, CAPTURE_ATTR)

    print(f"target : {base.rstrip('/')}{args.path}")
    print(f"length : {len(raw)}")
    print()
    print(f"consent default @ {pos_consent}  tag: {consent_tag}")
    print(f"GTM loader      @ {pos_gtm}  tag: {gtm_tag}")
    print(f"capture script     tag: {capture_tag}")
    print()

    checks: list[tuple[str, bool, str]] = [
        (
            "consent default snippet present",
            pos_consent >= 0,
            "header.php is missing the cd-consent-default snippet",
        ),
        (
            "consent default before GTM",
            0 <= pos_consent < pos_gtm,
            "snippet must sit above the GTM loader in header.php",
        ),
        (
            "consent default NOT delayed",
            bool(consent_tag) and DELAYED not in consent_tag.lower(),
            "cd-consent-mode-defaults.php is missing or its marker no longer matches",
        ),
        (
            "GTM loader NOT delayed",
            bool(gtm_tag) and DELAYED not in gtm_tag.lower(),
            "cd-measurement-no-delay.php is missing or its patterns no longer match",
        ),
    ]

    failed = 0
    for label, passed, hint in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
        if not passed:
            print(f"       -> {hint}")
            failed += 1

    # Informational only: the capture script is intentionally left delayed.
    if capture_tag:
        state = "delayed (intended)" if DELAYED in capture_tag.lower() else "NOT delayed"
        print(f"[note] click-id capture script is {state}")

    print()
    if failed:
        print(f"OVERALL: FAIL ({failed} of {len(checks)})")
        if any(not c[1] for c in checks[:3]) and checks[3][1]:
            print(
                "DANGER: the GTM loader is un-delayed while the consent default is "
                "not in place. Google tags will initialise with no consent state. "
                "Remove cd-measurement-no-delay.php or fix the default snippet now."
            )
        return 1

    print(f"OVERALL: PASS ({len(checks)} of {len(checks)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
