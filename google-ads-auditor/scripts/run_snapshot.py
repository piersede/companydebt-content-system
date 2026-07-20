#!/usr/bin/env python3
"""Run the fixed GAQL query library against a live Google Ads account via the
google-ads-mcp stdio server, and save a full audit snapshot to runs/.

This does not invent queries: it parses queries/**/*.gaql verbatim (only
substituting the documented {{PLACEHOLDER}} tokens) and sends each one to the
MCP server's `search_search` tool over a single stdio session.

Usage:
    python scripts/run_snapshot.py accounts/company-debt.yml <mcp-exe-path>
"""

import json
import re
import subprocess
import sys
import time
import uuid
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Maps each .gaql file to the raw snapshot filename it produces.
# Where several PMax query files feed one required "pmax.json", they are
# nested under sub-keys instead of overwriting each other.
QUERY_MAP = {
    "queries/account-baseline/budget-and-bidding.gaql": {"out": "account-baseline.json", "dates": "none"},
    "queries/account-baseline/campaign-performance.gaql": {"out": "campaigns.json", "dates": "audit"},
    "queries/account-baseline/conversion-actions.gaql": {"out": "conversions.json", "dates": "audit"},
    "queries/account-baseline/daily-performance.gaql": {"out": "daily-performance.json", "dates": "context"},
    "queries/diagnostics/ads.gaql": {"out": "ads.json", "dates": "audit"},
    "queries/diagnostics/devices.gaql": {"out": "devices.json", "dates": "audit"},
    "queries/diagnostics/impression-share.gaql": {"out": "impression-share.json", "dates": "audit"},
    "queries/diagnostics/landing-pages.gaql": {"out": "landing-pages.json", "dates": "audit"},
    "queries/diagnostics/networks.gaql": {"out": "networks.json", "dates": "audit"},
    "queries/search-terms/search-terms.gaql": {"out": "search-terms.json", "dates": "audit"},
    "queries/search-terms/keywords.gaql": {"out": "keywords.json", "dates": "none"},
    "queries/search-terms/keyword-performance.gaql": {"out": "keyword-performance.json", "dates": "audit"},
    "queries/performance-max/pmax-campaigns.gaql": {"out": "pmax.json", "pmax_key": "campaigns", "dates": "audit"},
    "queries/performance-max/asset-groups.gaql": {"out": "pmax.json", "pmax_key": "asset_groups", "dates": "audit"},
    "queries/performance-max/placements.gaql": {"out": "pmax.json", "pmax_key": "placements", "dates": "audit"},
    "queries/performance-max/pmax-search-terms.gaql": {"out": "pmax.json", "pmax_key": "search_terms", "dates": "audit"},
    "queries/performance-max/products.gaql": {"out": "pmax.json", "pmax_key": "products", "dates": "audit"},
}


def split_where(where_raw):
    """Split a flat WHERE clause on top-level AND, without breaking the AND
    that's part of a BETWEEN 'x' AND 'y' range expression."""
    protected = []

    def protect(m):
        protected.append(m.group(0))
        return f"__BETWEEN_{len(protected) - 1}__"

    tmp = re.sub(r"[\w.]+\s+BETWEEN\s+'[^']*'\s+AND\s+'[^']*'", protect, where_raw, flags=re.IGNORECASE)
    parts = [p.strip() for p in re.split(r"\s+AND\s+", tmp, flags=re.IGNORECASE)]

    result = []
    for p in parts:
        m2 = re.match(r"__BETWEEN_(\d+)__$", p)
        result.append(protected[int(m2.group(1))] if m2 else p)
    return result


def parse_gaql(text):
    """Extract SELECT fields, FROM resource, WHERE conditions, ORDER BY from a
    fixed .gaql file. Assumes the simple single-clause style used in this
    project's query library (no nested parens in WHERE)."""
    body = "\n".join(
        line for line in text.splitlines() if not line.strip().startswith("--")
    )
    body = " ".join(body.split())  # collapse whitespace

    m = re.search(r"SELECT\s+(.*?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.*?))?(?:\s+ORDER BY\s+(.*))?$", body, re.IGNORECASE)
    if not m:
        raise ValueError(f"could not parse GAQL:\n{text}")
    fields_raw, resource, where_raw, order_raw = m.groups()

    fields = [f.strip() for f in fields_raw.split(",") if f.strip()]

    conditions = []
    if where_raw:
        conditions = split_where(where_raw)

    orderings = []
    if order_raw:
        orderings = [o.strip() for o in order_raw.split(",") if o.strip()]

    return fields, resource, conditions, orderings


def substitute(items, subs):
    out = []
    for item in items:
        for key, val in subs.items():
            item = item.replace("{{" + key + "}}", val)
        out.append(item)
    return out


class MCPSession:
    def __init__(self, exe_path, env):
        self.proc = subprocess.Popen(
            [exe_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env,
            text=True,
            bufsize=1,
        )
        self._send({"jsonrpc": "2.0", "id": 0, "method": "initialize",
                     "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                                "clientInfo": {"name": "snapshot-runner", "version": "1.0"}}})
        self._recv(0)
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _send(self, msg):
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def _recv(self, expect_id, timeout=60):
        deadline = time.time() + timeout
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("MCP server closed stdout unexpectedly")
            line = line.strip()
            if not line.startswith("{"):
                continue
            msg = json.loads(line)
            if msg.get("id") == expect_id:
                return msg
        raise TimeoutError(f"no response for id={expect_id} within {timeout}s")

    def call_tool(self, name, arguments):
        call_id = str(uuid.uuid4())
        self._send({"jsonrpc": "2.0", "id": call_id, "method": "tools/call",
                     "params": {"name": name, "arguments": arguments}})
        resp = self._recv(call_id)
        result = resp.get("result", {})
        content = result.get("content") or []
        if result.get("isError"):
            raise RuntimeError(content[0]["text"] if content else "unknown error, no content returned")
        if not content:
            return []  # legitimately empty result set (e.g. no PMax placement/product data)
        return json.loads(content[0]["text"])

    def close(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        self.proc.terminate()


def main():
    if len(sys.argv) != 3:
        print("Usage: python run_snapshot.py <account-config.yml> <mcp-exe-path>", file=sys.stderr)
        sys.exit(2)

    config_path = Path(sys.argv[1])
    exe_path = sys.argv[2]

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    customer_id = config["customer_id"]
    slug = config["account_name"].lower().replace(" ", "-")

    end = date.today() - timedelta(days=1)  # last complete day
    audit_start = end - timedelta(days=config["comparison_periods"]["primary_days"] - 1)
    context_days = config["comparison_periods"]["context_days"]
    context_start = end - timedelta(days=context_days - 1)

    subs = {
        "CUSTOMER_ID": customer_id,
        "START_DATE": audit_start.isoformat(),
        "END_DATE": end.isoformat(),
        "CONTEXT_START_DATE": context_start.isoformat(),
    }

    run_dir = ROOT / "runs" / f"{date.today().isoformat()}-{slug}"
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    import os
    env = os.environ.copy()
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

    session = MCPSession(exe_path, env)

    failed_queries = []
    pmax_accum = {}
    warnings = []

    query_files = sorted(ROOT.glob("queries/**/*.gaql"))
    for qf in query_files:
        rel = str(qf.relative_to(ROOT)).replace("\\", "/")
        spec = QUERY_MAP.get(rel)
        if not spec:
            warnings.append(f"query file not mapped to a raw snapshot filename, skipped: {rel}")
            continue

        fields, resource, conditions, orderings = parse_gaql(qf.read_text(encoding="utf-8"))
        conditions = substitute(conditions, subs)

        print(f"Running {rel} -> {spec['out']}" + (f"[{spec.get('pmax_key')}]" if spec.get('pmax_key') else ""))
        try:
            rows = session.call_tool("search_search", {
                "customer_id": customer_id,
                "fields": fields,
                "resource": resource,
                "conditions": conditions,
                "orderings": orderings,
            })
        except Exception as e:
            print(f"  FAILED: {e}")
            failed_queries.append({"query_file": rel, "error": str(e)})
            continue

        print(f"  {len(rows)} rows")

        if spec["out"] == "pmax.json":
            pmax_accum[spec["pmax_key"]] = rows
        else:
            (raw_dir / spec["out"]).write_text(json.dumps(rows, indent=2), encoding="utf-8")

    if pmax_accum:
        (raw_dir / "pmax.json").write_text(json.dumps(pmax_accum, indent=2), encoding="utf-8")

    session.close()

    manifest = {
        "account_name": config["account_name"],
        "customer_id": customer_id,
        "currency": config["currency"],
        "timezone": config["timezone"],
        "audit_start": audit_start.isoformat(),
        "audit_end": end.isoformat(),
        "comparison_start": (audit_start - timedelta(days=7)).isoformat(),
        "comparison_end": (audit_start - timedelta(days=1)).isoformat(),
        "context_start": context_start.isoformat(),
        "context_end": end.isoformat(),
        "conversion_lag_days": config["targets"]["conversion_lag_days"],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
        "api_version": "google-ads-mcp 3.4.4 / google-ads python client 31.1.0",
        "query_library_version": "unversioned (REPLACE_WITH_VERSION placeholders not yet filled in query files)",
        "data_complete": len(failed_queries) == 0,
        "failed_queries": failed_queries,
        "warnings": warnings,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    import shutil
    shutil.copy(config_path, run_dir / "account-config.yml")

    print(f"\nSnapshot saved to {run_dir}")
    if failed_queries:
        print(f"{len(failed_queries)} quer(y/ies) failed — see manifest.json failed_queries")


if __name__ == "__main__":
    main()
