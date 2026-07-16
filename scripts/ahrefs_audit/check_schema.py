"""Pull JSON-LD from a staging page and look for schema.org validation problems.

Ahrefs reports 'Schema.org validation error' on ~375 pages with no detail, so
the actual defect has to be found by inspecting the emitted graph.

Usage: python check_schema.py <staging-path> [--dump]
"""
import base64
import json
import os
import re
import ssl
import sys
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

STAG = os.getenv("WP_STAGING_URL", "").rstrip("/")
BA = base64.b64encode(
    f"{os.getenv('WP_BASIC_AUTH_USER','')}:{os.getenv('WP_BASIC_AUTH_PASS','')}".encode()
).decode()

path = sys.argv[1] if len(sys.argv) > 1 else "/"
dump = "--dump" in sys.argv

req = urllib.request.Request(STAG + path, headers={
    "User-Agent": "Mozilla/5.0", "Authorization": f"Basic {BA}"})
html = urllib.request.urlopen(req, timeout=45, context=CTX).read().decode("utf-8", "ignore")

blocks = re.findall(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S)
print(f"{path}: {len(blocks)} JSON-LD block(s)\n")

for bi, b in enumerate(blocks):
    try:
        data = json.loads(b)
    except json.JSONDecodeError as e:
        print(f"  BLOCK {bi}: INVALID JSON - {e}")
        print(f"    {b[:300]}")
        continue
    graph = data.get("@graph", [data]) if isinstance(data, dict) else data
    print(f"  BLOCK {bi}: {len(graph)} node(s)")
    for node in graph:
        if not isinstance(node, dict):
            print(f"    !! non-object node: {node!r}")
            continue
        t = node.get("@type")
        issues = []
        # Common Ahrefs complaints: empty values, wrong types, bad URLs.
        for k, v in node.items():
            if v is None or v == "" or v == []:
                issues.append(f"empty value: {k}")
            if isinstance(v, str) and v.strip() != v:
                issues.append(f"whitespace-padded: {k}")
        print(f"    {str(t):<28} {'; '.join(issues) if issues else ''}")
        if dump:
            print(json.dumps(node, indent=6)[:1400])
