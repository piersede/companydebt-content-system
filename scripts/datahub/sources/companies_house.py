"""Companies House acquisition: company population and monthly flows.

The Companies House REST API is mainly per-company lookup, but its
advanced-search endpoint returns a total count ('hits') for any filter. That
gives the hub three things without a bulk download:

  - active-company population  -> denominator for insolvency rates
  - incorporations in a month  -> business formation
  - dissolutions in a month    -> the dissolutions-vs-insolvencies picture

Important: these are point-in-time reads of the live register, not an official
statistic, and dissolutions here are mostly ordinary strike-offs, NOT
insolvencies (see caveat 'dissolutions_not_insolvencies').

Needs COMPANIES_HOUSE_API_KEY in .env (free Live REST key).

Usage:
    python scripts/datahub/sources/companies_house.py --month 2026-05
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import date, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "companies-house"
BASE = "https://api.company-information.service.gov.uk"
SOURCE_ID = "companies_house_register"


def _load_key() -> str:
    for candidate in (ROOT / ".env.local", ROOT / ".env"):
        if candidate.exists():
            load_dotenv(candidate)
            break
    key = os.environ.get("COMPANIES_HOUSE_API_KEY", "").strip()
    if not key:
        raise SystemExit("COMPANIES_HOUSE_API_KEY is not set in .env")
    return key


class CompaniesHouseClient:
    """Thin, rate-limit-aware client. Only what the hub needs."""

    def __init__(self, key: str | None = None, *, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (key or _load_key(), "")

    def _get(self, path: str, params: dict | None = None, *, retries: int = 4) -> dict:
        url = BASE + path
        last = None
        for _ in range(retries):
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 429:  # rate limited: 600 req / 5 min
                wait = int(resp.headers.get("Retry-After", "5"))
                time.sleep(min(wait, 30))
                last = resp
                continue
            resp.raise_for_status()
            return resp.json()
        if last is not None:
            last.raise_for_status()
        raise RuntimeError(f"Gave up on {path} after {retries} attempts")

    def count(self, **filters) -> int:
        """Total companies matching an advanced-search filter."""
        params = {k: v for k, v in filters.items() if v is not None}
        params["size"] = 1
        return int(self._get("/advanced-search/companies", params).get("hits", 0))

    def get_company(self, number: str) -> dict:
        """Full company profile (name, status, SIC codes, office, dates)."""
        return self._get(f"/company/{number}")


def _month_bounds(month: str) -> tuple[str, str]:
    """'2026-05' -> ('2026-05-01', '2026-05-31')."""
    year, mon = (int(p) for p in month.split("-"))
    start = date(year, mon, 1)
    nxt = date(year + (mon == 12), (mon % 12) + 1, 1)
    return start.isoformat(), (nxt - timedelta(days=1)).isoformat()


def _prev_complete_month() -> str:
    first_of_this = date.today().replace(day=1)
    last_month = first_of_this - timedelta(days=1)
    return f"{last_month.year}-{last_month.month:02d}"


def fetch_flow_snapshot(client: CompaniesHouseClient, month: str, retrieved_at: str) -> dict:
    """Population + incorporations/dissolutions for `month`, as stat observations."""
    m_from, m_to = _month_bounds(month)
    active_total = client.count(company_status="active")
    incorporations = client.count(incorporated_from=m_from, incorporated_to=m_to)
    dissolutions = client.count(company_status="dissolved", dissolved_from=m_from, dissolved_to=m_to)

    obs = [
        {
            "metric_key": "active_companies_total",
            "metric_label": "Active companies on the register",
            "period": f"as_of_{retrieved_at}",
            "value": active_total,
            "unit": "companies",
            "notes": "Point-in-time count of the live register (advanced-search). Denominator for rates.",
        },
        {
            "metric_key": "incorporations",
            "metric_label": "Company incorporations",
            "period": month,
            "value": incorporations,
            "unit": "companies",
            "notes": "Companies with an incorporation date in the month.",
        },
        {
            "metric_key": "dissolutions",
            "metric_label": "Company dissolutions",
            "period": month,
            "value": dissolutions,
            "unit": "companies",
            "notes": "Companies with a dissolution date in the month. Mostly strike-offs, NOT insolvencies.",
        },
    ]
    return {
        "source_id": SOURCE_ID,
        "month": month,
        "retrieved_at": retrieved_at,
        "observations": obs,
        "caveats": ["dissolutions_not_insolvencies", "ons_denominator"],
    }


def _write_release(month: str, retrieved_at: str) -> None:
    """Append a release for this month; mark any prior 'current' superseded."""
    path = DATA_DIR / "dataset_release.json"
    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
    else:
        doc = {
            "_about": "Release ledger for Companies House register snapshots (population, incorporations, dissolutions) fetched via the advanced-search API.",
            "_schema": [
                "release_id", "source_id", "dataset_name", "period_start", "period_end",
                "publication_date", "source_files", "is_provisional", "status", "notes",
            ],
            "releases": [],
        }
    for rel in doc["releases"]:
        if rel.get("status") == "current":
            rel["status"] = "superseded"
    m_from, m_to = _month_bounds(month)
    doc["releases"].append({
        "release_id": f"ch_flows_{month}",
        "source_id": SOURCE_ID,
        "dataset_name": f"Companies House population and flows, {month}",
        "period_start": m_from,
        "period_end": m_to,
        "publication_date": retrieved_at,
        "source_files": [{
            "endpoint": f"{BASE}/advanced-search/companies",
            "retrieved_at": retrieved_at,
            "note": "Counts read live from the register; no file artifact.",
        }],
        "is_provisional": False,
        "status": "current",
        "notes": "Counts are live-register reads, not an official statistic. Dissolutions are mostly strike-offs, not insolvencies.",
    })
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch Companies House population and monthly flows")
    ap.add_argument("--month", default=_prev_complete_month(), help="Month as YYYY-MM (default: previous complete month)")
    args = ap.parse_args()

    retrieved_at = date.today().isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    client = CompaniesHouseClient()
    snapshot = fetch_flow_snapshot(client, args.month, retrieved_at)

    out = DATA_DIR / "flow_snapshot.json"
    out.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    _write_release(args.month, retrieved_at)

    print(f"Wrote {out}")
    for o in snapshot["observations"]:
        print(f"  {o['metric_label']:38} {o['value']:>12,}  ({o['period']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
