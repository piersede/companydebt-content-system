"""
BusinessExpert WordPress Publisher
===================================
Pushes article HTML to WordPress staging or production via the REST API.

Staging uses a two-layer auth approach:
  1. WP Engine HTTP basic auth (environment-level nginx password)
  2. WP Application Password for REST API access

Because both layers use the HTTP Authorization header, staging requests
embed the HTTP basic auth in the URL and pass the WP app password
in the Authorization header.

One API call per article. Drafts land in WP for human review and one-click publish.

Usage:
    python scripts/wp_publish.py --file preview/low-apr-business-credit-cards.html
    python scripts/wp_publish.py --file preview/low-apr-business-credit-cards.html --prod
    python scripts/wp_publish.py --file preview/low-apr-business-credit-cards.html --status publish

Environment variables required (set in .env):
    Staging: WP_STAGING_URL, WP_STAGING_USERNAME, WP_STAGING_APP_PASSWORD,
             WP_BASIC_AUTH_USER, WP_BASIC_AUTH_PASS
    Production: WP_SITE_URL, WP_USERNAME, WP_APP_PASSWORD

Requirements:
    pip install requests python-dotenv beautifulsoup4
"""

import os
import sys
import json
import argparse
import re
import base64
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests python-dotenv beautifulsoup4")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip install requests python-dotenv beautifulsoup4")
    sys.exit(1)


# ----------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------

def get_credentials(prod: bool) -> dict:
    """Load WP credentials from environment."""
    if prod:
        url = os.getenv("WP_SITE_URL", "").rstrip("/")
        username = os.getenv("WP_USERNAME", "")
        password = os.getenv("WP_APP_PASSWORD", "")
        env_label = "production"
        http_user = ""
        http_pass = ""
    else:
        url = os.getenv("WP_STAGING_URL", "").rstrip("/")
        username = os.getenv("WP_STAGING_USERNAME", "")
        password = os.getenv("WP_STAGING_APP_PASSWORD", "")
        env_label = "staging"
        http_user = os.getenv("WP_BASIC_AUTH_USER", "")
        http_pass = os.getenv("WP_BASIC_AUTH_PASS", "")

    missing = []
    if not url or url.startswith("PASTE_YOUR"):
        missing.append(f"WP_{'SITE_URL' if prod else 'STAGING_URL'}")
    if not username or username.startswith("PASTE_YOUR"):
        missing.append(f"WP_{'USERNAME' if prod else 'STAGING_USERNAME'}")
    if not password or password.startswith("PASTE_YOUR"):
        missing.append(f"WP_{'APP_PASSWORD' if prod else 'STAGING_APP_PASSWORD'}")

    if missing:
        print(f"\nERROR: Missing {env_label} credentials in .env:")
        for key in missing:
            print(f"  {key}")
        print(f"\nEdit your .env file and fill in the {env_label} values.")
        sys.exit(1)

    return {
        "url": url,
        "username": username,
        "password": password,
        "label": env_label,
        "http_user": http_user,
        "http_pass": http_pass,
    }


def create_authenticated_session(creds: dict) -> tuple[requests.Session, str]:
    """
    Create an authenticated requests.Session for the WP REST API.

    For staging (WP Engine): both nginx and WP use the Authorization header,
    so we use cookie-based auth instead — log in via wp-login.php, extract the
    REST nonce, and use cookie + X-WP-Nonce for all API calls.

    For production: use standard Application Password Basic auth.

    Returns (session, api_base_url).
    """
    url = creds["url"]
    api_base = f"{url}/wp-json/wp/v2"
    session = requests.Session()
    session.headers["User-Agent"] = "BusinessExpert-Publisher/1.0"

    has_http_auth = bool(creds.get("http_user") and creds.get("http_pass"))

    if has_http_auth:
        # WP Engine staging: cookie-based auth
        # Uses login credentials (WP_USERNAME/WP_PASSWORD), not app password
        http_auth = (creds["http_user"], creds["http_pass"])
        wp_login_user = os.getenv("WP_USERNAME", creds["username"])
        wp_login_pass = os.getenv("WP_PASSWORD", creds["password"])

        # Step 1: Log in via wp-login.php
        login_resp = session.post(
            f"{url}/wp-login.php",
            auth=http_auth,
            data={
                "log": wp_login_user,
                "pwd": wp_login_pass,
                "wp-submit": "Log In",
                "redirect_to": f"{url}/wp-admin/",
                "testcookie": "1",
            },
            allow_redirects=True,
            timeout=30,
        )
        wp_cookies = [c.name for c in session.cookies if "wordpress" in c.name.lower()]
        if not wp_cookies:
            print(f"\nERROR: WP login failed — no auth cookies received.")
            print(f"Check WP_USERNAME and WP_PASSWORD in .env.")
            sys.exit(1)

        # Step 2: Get REST nonce from admin page
        admin_resp = session.get(f"{url}/wp-admin/", auth=http_auth, timeout=15)
        nonce_match = re.search(
            r'wpApiSettings[^}]+nonce["\s:]+\"([a-f0-9]+)\"', admin_resp.text
        ) or re.search(
            r'"nonce":"([a-f0-9]+)"', admin_resp.text
        )
        if not nonce_match:
            print("\nERROR: Could not extract REST API nonce from wp-admin.")
            sys.exit(1)

        nonce = nonce_match.group(1)
        session.headers["X-WP-Nonce"] = nonce
        # Keep HTTP auth on all requests so nginx doesn't block them
        session.auth = http_auth
    else:
        # Production or no HTTP auth layer: standard Application Password
        wp_creds = base64.b64encode(
            f"{creds['username']}:{creds['password']}".encode()
        ).decode()
        session.headers["Authorization"] = f"Basic {wp_creds}"

    return session, api_base


# ----------------------------------------------------------------
# HTML PARSER
# ----------------------------------------------------------------

def extract_from_html(html_path: Path) -> dict:
    """
    Extract title, slug, content, and meta from an article HTML file.

    Looks for:
      - <title> or first <h1> for the post title
      - data-slug attribute on <body> or <article> for the WP slug
      - <meta name="description"> for the SEO meta description
      - <article> or <main> tag for the post body content
      - <meta name="category"> for WP category name
    """
    with open(html_path, "r", encoding="utf-8") as f:
        raw = f.read()

    soup = BeautifulSoup(raw, "html.parser")

    # Title: prefer <title> tag, fall back to first <h1>
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        # Strip site name suffix if present (e.g. " | BusinessExpert")
        title = re.sub(r"\s*\|.*$", "", title).strip()
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)

    # Slug: prefer data-slug on body/article, else derive from filename
    slug = ""
    for tag in ["body", "article", "main"]:
        el = soup.find(tag)
        if el and el.get("data-slug"):
            slug = el["data-slug"].strip("/")
            break
    if not slug:
        slug = html_path.stem  # e.g. "low-apr-business-credit-cards"

    # Meta description
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    # Category
    category_name = ""
    cat_tag = soup.find("meta", attrs={"name": "category"})
    if cat_tag and cat_tag.get("content"):
        category_name = cat_tag["content"].strip()

    # Content: prefer <article>, then <main>, then <body>
    content_el = soup.find("article") or soup.find("main") or soup.find("body")
    if not content_el:
        print("ERROR: Could not find <article>, <main>, or <body> in HTML file.")
        sys.exit(1)

    # Remove script and style tags from content
    for tag in content_el.find_all(["script", "style", "noscript"]):
        tag.decompose()

    content_html = str(content_el)

    return {
        "title": title,
        "slug": slug,
        "content": content_html,
        "meta_description": meta_desc,
        "category_name": category_name,
    }


# ----------------------------------------------------------------
# CATEGORY LOOKUP
# ----------------------------------------------------------------

def get_or_create_category(session: requests.Session, api_base: str, name: str) -> int | None:
    """Look up a WP category by name; return its ID or None if name is blank."""
    if not name:
        return None

    resp = session.get(f"{api_base}/categories", params={"search": name, "per_page": 5})
    if resp.status_code == 200:
        results = resp.json()
        for cat in results:
            if cat["name"].lower() == name.lower():
                return cat["id"]

    # Category not found — create it
    resp = session.post(f"{api_base}/categories", json={"name": name})
    if resp.status_code == 201:
        return resp.json()["id"]

    print(f"WARNING: Could not find or create category '{name}'. Posting without category.")
    return None


# ----------------------------------------------------------------
# PUSH TO WORDPRESS
# ----------------------------------------------------------------

def push_to_wordpress(
    article: dict,
    creds: dict,
    status: str = "draft",
    post_id: int | None = None,
    post_type: str = "posts",
) -> dict:
    """
    POST (or PUT) an article to WordPress via REST API.

    post_type: "posts" for blog posts, "pages" for WP pages.
    Returns the API response dict with 'id', 'link', and 'status'.
    """
    session, api_base = create_authenticated_session(creds)
    session.headers["Content-Type"] = "application/json"

    # Verify connection
    whoami = session.get(f"{api_base}/users/me")
    if whoami.status_code == 401:
        print(f"\nERROR: Authentication failed for {creds['label']}.")
        print("Check WP credentials in your .env file.")
        sys.exit(1)
    elif whoami.status_code != 200:
        print(f"\nERROR: Cannot reach WordPress REST API at {api_base}")
        print(f"Status: {whoami.status_code}")
        sys.exit(1)

    user_data = whoami.json()
    print(f"Connected as: {user_data.get('name', creds['username'])} ({creds['label']})")

    # Resolve category (only for posts, not pages)
    category_id = None
    if post_type == "posts":
        category_id = get_or_create_category(session, api_base, article.get("category_name", ""))

    # Build payload
    payload = {
        "title": article["title"],
        "slug": article["slug"],
        "content": article["content"],
        "status": status,
    }

    # Allow clearing the excerpt (subtitle/deck)
    if "excerpt" in article:
        payload["excerpt"] = article["excerpt"]

    if category_id:
        payload["categories"] = [category_id]

    # Add Yoast/RankMath SEO title and meta description if available
    meta_fields = {}
    if article.get("meta_description"):
        meta_fields["_yoast_wpseo_metadesc"] = article["meta_description"]
        meta_fields["rank_math_description"] = article["meta_description"]
    if article.get("title"):
        meta_fields["_yoast_wpseo_title"] = article["title"]
        meta_fields["rank_math_title"] = article["title"]
    if meta_fields:
        payload["meta"] = meta_fields

    # Update existing or create new
    endpoint = f"{api_base}/{post_type}"
    if post_id:
        resp = session.post(f"{endpoint}/{post_id}", json=payload)
        action = "Updated"
    else:
        resp = session.post(endpoint, json=payload)
        action = "Created"

    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"\n{action} {post_type[:-1]} successfully.")
        print(f"  ID:       {data['id']}")
        print(f"  Status:   {data['status']}")
        print(f"  Preview:  {data.get('link', data.get('guid', {}).get('rendered', ''))}")
        return data
    else:
        print(f"\nERROR: WordPress API returned {resp.status_code}")
        try:
            err = resp.json()
            print(f"  Code:    {err.get('code', 'unknown')}")
            print(f"  Message: {err.get('message', resp.text[:200])}")
        except Exception:
            print(f"  Response: {resp.text[:300]}")
        sys.exit(1)


# ----------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="BusinessExpert WordPress Publisher — pushes article HTML to WP via REST API"
    )
    parser.add_argument(
        "--file", required=True,
        help="Path to the article HTML file (e.g. preview/low-apr-business-credit-cards.html)"
    )
    parser.add_argument(
        "--prod", action="store_true", default=False,
        help="Push to production instead of staging (default: staging)"
    )
    parser.add_argument(
        "--status", default="draft",
        choices=["draft", "publish", "pending", "private"],
        help="WordPress post status (default: draft)"
    )
    parser.add_argument(
        "--id", type=int, default=None,
        help="Existing WP post ID to update (omit to create a new post)"
    )
    parser.add_argument(
        "--title", default=None,
        help="Override article title (optional — will be extracted from HTML if not set)"
    )
    parser.add_argument(
        "--slug", default=None,
        help="Override post slug (optional — will be derived from filename if not set)"
    )
    args = parser.parse_args()

    html_path = Path(args.file)
    if not html_path.exists():
        print(f"ERROR: File not found: {html_path}")
        sys.exit(1)

    print(f"\nBusinessExpert WordPress Publisher")
    print(f"File:        {html_path}")
    print(f"Target:      {'PRODUCTION ⚠️' if args.prod else 'Staging'}")
    print(f"Post status: {args.status}")

    if args.prod and args.status == "publish":
        confirm = input("\n⚠️  You are about to PUBLISH to PRODUCTION. Type 'yes' to confirm: ")
        if confirm.strip().lower() != "yes":
            print("Aborted.")
            sys.exit(0)

    # Load credentials
    creds = get_credentials(prod=args.prod)

    # Parse HTML
    print(f"\nParsing article HTML...")
    article = extract_from_html(html_path)

    # Apply CLI overrides
    if args.title:
        article["title"] = args.title
    if args.slug:
        article["slug"] = args.slug

    print(f"  Title: {article['title']}")
    print(f"  Slug:  {article['slug']}")
    if article["meta_description"]:
        print(f"  Meta:  {article['meta_description'][:60]}...")

    # Push
    print(f"\nPushing to WordPress ({creds['label']})...")
    result = push_to_wordpress(
        article=article,
        creds=creds,
        status=args.status,
        post_id=args.id,
    )

    print(f"\nDone. Open in WordPress:")
    wp_admin = creds["url"].rstrip("/") + f"/wp-admin/post.php?post={result['id']}&action=edit"
    print(f"  Edit:    {wp_admin}")
    print(f"  Preview: {result.get('link', '')}\n")
