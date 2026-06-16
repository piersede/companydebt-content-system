"""Ad-hoc triage: surface the genuinely-actionable apply-candidates from an
answer-engine audit run, filtering out raw figures (flag separately) and
already-present material.

A candidate is worth a human look when ALL hold:
  - verification_status == verified (confirmed against a primary source)
  - article_status in {missing, present_but_weak, buried}  (a real gap OR a
    topic we cover only shallowly — additive-first: deepen-existing counts)
  - it is NOT a pure figure (no %/£/p figure in `value` or detail)

Usage: python -m scripts.answer_engine_audit._apply_candidates <run_dir> [<run_dir> ...]
"""
import json
import re
import sys
from pathlib import Path

RATE = re.compile(r"(\d+(\.\d+)?\s*%)|(£\s*\d)|(\b\d+\s*p\b)|(\bAER\b)|(\bAPR\b)", re.I)


def load_ledger(run: Path):
    p = run / "processed" / "verified-ledger.jsonl"
    if not p.exists():
        # fall back to nuggets.jsonl (pre-verification) so we at least see gaps
        p = run / "processed" / "nuggets.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def is_rate(row) -> bool:
    return bool(RATE.search(str(row.get("value", "")))) or bool(
        RATE.search(str(row.get("detail", "")))
    )


def main():
    for arg in sys.argv[1:]:
        run = Path(arg)
        rows = load_ledger(run)
        verified = [r for r in rows if (r.get("verification_status") in (None, "verified"))]
        gaps = [r for r in verified
                if r.get("article_status") in ("missing", "present_but_weak", "buried")]
        nonrate = [r for r in gaps if not is_rate(r)]
        # de-dupe on normalised detail
        seen, uniq = set(), []
        for r in nonrate:
            k = re.sub(r"\s+", " ", str(r.get("detail", "")).lower()).strip()
            if k and k not in seen:
                seen.add(k)
                uniq.append(r)
        print(f"\n===== {run.parts[1] if len(run.parts) > 1 else run} =====")
        print(f"  ledger rows={len(rows)}  verified={len(verified)}  "
              f"gaps={len(gaps)}  gaps&non-rate&uniq={len(uniq)}")
        for r in uniq:
            vs = r.get("verification_status", "?")
            print(f"   [{vs}] {r.get('provider','')} | {r.get('category','')} | "
                  f"{str(r.get('detail',''))[:160]}")


if __name__ == "__main__":
    main()
