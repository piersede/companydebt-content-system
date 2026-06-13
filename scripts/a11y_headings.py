"""Diagnostic: dump the heading outline (and generic links / unnamed controls)
of a served staging page, so heading-skip / link findings can be pinpointed in
stored content. Read-only. Uses basic auth from .env.

Usage:
  python scripts/a11y_headings.py <PATH-or-URL>
  python scripts/a11y_headings.py <PATH> --links     # also list anchor names
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv('.env')
STAGING = os.getenv('WP_STAGING_URL', 'https://comdebstage.wpengine.com').rstrip('/')
BA = (os.getenv('WP_BASIC_AUTH_USER', ''), os.getenv('WP_BASIC_AUTH_PASS', ''))

GENERIC = {"click here","here","read more","learn more","find out more","more",
           "view deal","details","view details","see more","this","link",
           "continue","go","view","shop now","apply"}


def acc_name(a):
    if a.get("aria-label"): return a["aria-label"].strip()
    if a.get("title"): return a["title"].strip()
    t = a.get_text(" ", strip=True)
    if t: return t
    img = a.find("img")
    if img and img.get("alt"): return img["alt"].strip()
    return ""


def main():
    arg = sys.argv[1]
    show_links = "--links" in sys.argv
    url = arg if arg.startswith("http") else STAGING + arg
    r = requests.get(url, auth=BA, headers={"User-Agent": "CD-a11y-diag/1.0"}, timeout=40)
    soup = BeautifulSoup(r.text, "html.parser")
    print(f"== {url}  ({r.status_code})")
    levels = []
    prev = 0
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        lvl = int(h.name[1])
        skip = " <<< SKIP" if prev and lvl - prev > 1 else ""
        cls = h.get("class")
        txt = h.get_text(" ", strip=True)[:80]
        print(f"  {'  '*(lvl-1)}h{lvl} {txt!r} class={cls}{skip}")
        levels.append(lvl)
        prev = lvl
    if show_links:
        print("-- links --")
        for a in soup.find_all("a"):
            if not a.get("href"): continue
            name = acc_name(a)
            flag = ""
            if name.lower().strip(" →←»«") in GENERIC: flag = " <<< GENERIC"
            if not name and not a.get("aria-labelledby"): flag = " <<< UNNAMED"
            if flag:
                print(f"  href={a.get('href')!r} name={name!r}{flag}")


if __name__ == "__main__":
    main()
