"""Quick inspector: dump column titles + sample item to understand the schema."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

BOARD_ID = 18406273663

here = Path(__file__).resolve()
for c in [here.parents[1] / ".env", here.parents[3] / ".env", here.parents[4] / ".env"]:
    if c.exists():
        load_dotenv(c); break
TOKEN = os.environ["MONDAY_API_KEY"]

q = """
query ($b: [ID!]) {
  boards(ids: $b) {
    columns { id title type }
    groups { id title }
  }
}
"""
r = requests.post("https://api.monday.com/v2", headers={"Authorization": TOKEN, "API-Version": "2024-10"},
                  json={"query": q, "variables": {"b": [str(BOARD_ID)]}}, timeout=30)
data = r.json()["data"]["boards"][0]
print("GROUPS:")
for g in data["groups"]:
    print(f"  {g['id']:<20} {g['title']}")
print("\nCOLUMNS:")
for c in data["columns"]:
    print(f"  {c['id']:<30} {c['type']:<15} {c['title']}")

# Sample 3 items from Live group
live_id = next(g["id"] for g in data["groups"] if g["title"].strip().lower() == "live")
q2 = """
query ($b: ID!, $g: String!) {
  boards(ids: [$b]) {
    groups(ids: [$g]) {
      items_page(limit: 5) {
        items {
          id name
          column_values { id text value column { title } }
        }
      }
    }
  }
}
"""
r2 = requests.post("https://api.monday.com/v2", headers={"Authorization": TOKEN, "API-Version": "2024-10"},
                   json={"query": q2, "variables": {"b": str(BOARD_ID), "g": live_id}}, timeout=30)
items = r2.json()["data"]["boards"][0]["groups"][0]["items_page"]["items"]
print("\nSAMPLE ITEMS:")
for it in items:
    print(f"\n  {it['id']}  {it['name']}")
    for cv in it["column_values"]:
        if cv.get("text"):
            print(f"    [{cv['column']['title']}] = {cv['text'][:100]}")
