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
4. The consent tool must not BLOCK the Google tag either. CookieYes carries its
   own script blocker, driven by a per-account list of provider URLs. While
   ``googletagmanager.com`` sits in that list, CookieYes hooks
   ``document.createElement`` and refuses to insert the container until the
   visitor grants the matching category -- so on a page view with no decision
   yet there is no container, no dataLayer consumer and no cookieless ping.
   Consent Mode never gets the chance to do the gating it exists to do.

Conditions 1 to 3 were all PASSING on live on 2 Sep 2026 while condition 4 was
failing, which is why it is now checked here: the first three describe the HTML,
and the HTML was correct. The fault was one setting in the CookieYes account.

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

# The consent tool's own loader, which carries the account's script-blocker list.
# The host is deliberately NOT pinned to cdn-cookieyes.com: WP Rocket minifies
# this script and serves a first-party copy from
# /wp-content/cache/min/1/client_data/<key>/script.js, so a pattern tied to the
# vendor host finds nothing on a cached page and reports the loader as missing.
CKY_LOADER = re.compile(r"https://[^\s\"']*?client_data/([0-9a-zA-Z]+)/script\.js")

# The hosts that actually serve the tag itself. If the consent tool blocks either
# of these by URL, the container never loads for a visitor who has not accepted,
# and the whole Consent Mode arrangement above is bypassed.
GOOGLE_MEASUREMENT_HOSTS = (
    "googletagmanager.com",
    "google-analytics.com",
)

# doubleclick.net is deliberately NOT in the list above, and this is a judgement
# rather than an oversight. It serves remarketing, not the tag, so blocking it
# does not stop the container or the Google tags loading. It only bites for a
# visitor who has not granted the advertising category, and for that visitor the
# advertising cookies must stay off anyway. The blocker also only intercepts
# <script> and <iframe> insertions, so it does not touch the cookieless
# conversion ping, which travels as an image/fetch request. Reported as a note so
# a human can see it, and re-check it if the ping ever stops arriving.
ADVERTISING_HOSTS_OK_TO_BLOCK = ("doubleclick.net",)

# Where a human fixes this: CookieYes dashboard -> Advanced Settings -> Google
# consent mode -> "Support GCM" on, "Allow Google tags to fire before consent"
# on. That second toggle is what takes the Google hosts out of the blocker list.
CKY_FIX_HINT = (
    "CookieYes is blocking the Google tag by URL. Turn ON "
    '"Allow Google tags to fire before consent" in the CookieYes account '
    "(Advanced Settings -> Google consent mode). Consent Mode already denies "
    "storage by default, so the cookies stay off without the blocker."
)


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


def blocked_provider_urls(script_js: str) -> list[str]:
    """Pull the provider URLs out of a CookieYes account script.

    The account script carries its blocker list as ``_providersToBlock:[...]``,
    an array of ``{url:"...",categories:[...],fullPath:!0|!1}`` objects. Scan to
    the bracket that closes the array, counting depth and ignoring brackets that
    sit inside a string literal, then read the ``url`` of each entry.
    """
    marker = "_providersToBlock:["
    start = script_js.find(marker)
    if start < 0:
        return []
    i = start + len(marker) - 1  # sit on the opening bracket
    depth = 0
    in_string: str | None = None
    end = -1
    while i < len(script_js):
        ch = script_js[i]
        if in_string:
            if ch == "\\":
                i += 2
                continue
            if ch == in_string:
                in_string = None
        elif ch in "\"'":
            in_string = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    if end < 0:
        return []
    body = script_js[start:end]
    return re.findall(r"url:\s*\"([^\"]*)\"", body)


def consent_tool_blocklist(html: str, auth) -> tuple[str, list[str], str]:
    """Return (account key, blocked provider URLs, error) for the page's CMP.

    Read the copy the visitor actually gets first, because a stale WP Rocket
    minified copy can keep serving old blocker rules after the account itself is
    corrected. Fall back to the vendor copy when the cached one cannot be read -
    on staging it sits behind the basic-auth wall, and a 401 there says nothing
    about the account.

    An empty key means the page carries no CookieYes loader at all. A non-empty
    error means neither copy could be read, which is reported as its own failure
    rather than being mistaken for a clean blocker list.
    """
    m = CKY_LOADER.search(html)
    if not m:
        return "", [], ""
    key = m.group(1)
    vendor = f"https://cdn-cookieyes.com/client_data/{key}/script.js"
    attempts = [(m.group(0), auth)]
    if m.group(0) != vendor:
        attempts.append((vendor, None))

    first_error = ""
    for url, url_auth in attempts:
        try:
            r = requests.get(url, auth=url_auth, headers=UA, timeout=60)
            r.raise_for_status()
        except Exception as exc:  # network, DNS, 4xx, 5xx
            first_error = first_error or f"{url} -> {exc}"
            continue
        return key, blocked_provider_urls(r.text), ""
    return key, [], f"could not read the consent-tool script: {first_error}"


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
    cky_key, blocked, cky_err = consent_tool_blocklist(html, auth)
    blocks_google = sorted(
        u for u in blocked if any(h in u for h in GOOGLE_MEASUREMENT_HOSTS)
    )

    print(f"target : {base.rstrip('/')}{args.path}")
    print(f"length : {len(raw)}")
    print()
    print(f"consent default @ {pos_consent}  tag: {consent_tag}")
    print(f"GTM loader      @ {pos_gtm}  tag: {gtm_tag}")
    print(f"capture script     tag: {capture_tag}")
    print(f"consent tool       account: {cky_key or '(none on page)'}")
    print(f"consent tool       blocks: {', '.join(blocked) or '(nothing)'}")
    ad_blocked = sorted(
        u for u in blocked if any(h in u for h in ADVERTISING_HOSTS_OK_TO_BLOCK)
    )
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
        (
            "consent tool does NOT block the Google tag",
            bool(cky_key) and not cky_err and not blocks_google,
            (
                "header.php is missing the CookieYes loader"
                if not cky_key
                else cky_err
                if cky_err
                else f"blocked by URL pattern: {'; '.join(blocks_google)}. "
                + CKY_FIX_HINT
            ),
        ),
    ]

    failed = 0
    for label, passed, hint in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
        if not passed:
            print(f"       -> {hint}")
            failed += 1

    # Informational only: blocking these does not stop the tag loading.
    if ad_blocked:
        print(f"[note] consent tool also blocks {', '.join(ad_blocked)} - remarketing")
        print("       only, and only before the visitor grants advertising. Expected.")

    # Informational only: the capture script is intentionally left delayed.
    if capture_tag:
        state = "delayed (intended)" if DELAYED in capture_tag.lower() else "NOT delayed"
        print(f"[note] click-id capture script is {state}")

    print()
    if failed:
        print(f"OVERALL: FAIL ({failed} of {len(checks)})")
        if any(not c[1] for c in checks[:3]) and checks[3][1] and not blocks_google:
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
