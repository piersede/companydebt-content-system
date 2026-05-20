"""Snapshot the current order of items in the Live group for rollback."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

BOARD_ID = 18406273663

here = Path(__file__).resolve()
for c in [here.parents[1] / ".env", here.parents[3] / ".env", here.parents[4] / ".env"]:
    if c.exists():
        load_dotenv(c); break
TOKEN = os.environ["MONDAY_API_KEY"]

q_groups = """
query ($b: [ID!]) {
  boards(ids: $b) { groups { id title } }
}
"""
r = requests.post("https://api.monday.com/v2",
                  headers={"Authorization": TOKEN, "API-Version": "2024-10"},
                  json={"query": q_groups, "variables": {"b": [str(BOARD_ID)]}}, timeout=30)
groups = r.json()["data"]["boards"][0]["groups"]
live_id = next(g["id"] for g in groups if g["title"].strip().lower() == "live")

q_items = """
query ($b: ID!, $g: String!, $cursor: String) {
  boards(ids: [$b]) {
    groups(ids: [$g]) {
      items_page(limit: 100, cursor: $cursor) {
        cursor
        items { id name }
      }
    }
  }
}
"""
items = []
cursor = None
while True:
    r = requests.post("https://api.monday.com/v2",
                      headers={"Authorization": TOKEN, "API-Version": "2024-10"},
                      json={"query": q_items, "variables": {"b": str(BOARD_ID), "g": live_id, "cursor": cursor}}, timeout=30)
    page = r.json()["data"]["boards"][0]["groups"][0]["items_page"]
    items.extend(page["items"])
    cursor = page.get("cursor")
    if not cursor:
        break

ts = datetime.now().strftime("%Y%m%d-%H%M%S")
out_path = Path(f"data/monday-live-snapshot-{ts}.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(
    [{"position": i + 1, "id": it["id"], "name": it["name"]} for i, it in enumerate(items)],
    indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Snapshot of {len(items)} items written to {out_path}")
