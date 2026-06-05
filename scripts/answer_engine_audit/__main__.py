"""CLI for the Answer-Engine Coverage Audit System.

Pilot subcommand:
    capture   Capture raw answer-engine witnesses (OpenAI + Gemini) for a page.

Examples:
    python -m scripts.answer_engine_audit capture --page liquidation --dry-run
    python -m scripts.answer_engine_audit audit --page liquidation
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from . import prompts
from .core import (
    RunContext, available_engines, derive_keyword, new_run, resolve_page,
    write_source_index,
)


def _resolve_use_cases(cfg: dict[str, Any], keyword: str) -> list[str]:
    val = cfg.get("priority_questions")
    if isinstance(val, list) and val:
        return [str(q) for q in val]
    return prompts.default_use_cases(keyword)


def build_prompt_set(keyword: str, use_cases: list[str]) -> list[tuple[str, str]]:
    """Return (label, prompt) pairs. Labels become raw filenames."""
    pset: list[tuple[str, str]] = [
        ("broad", prompts.BROAD_ANSWER.format(keyword=keyword)),
        ("risk", prompts.RISK_DRAWBACK.format(keyword=keyword)),
    ]
    for i, q in enumerate(use_cases, 1):
        pset.append((f"usecase-{i}", prompts.USE_CASE.format(keyword=keyword, question=q)))
    return pset


def cmd_capture(args: argparse.Namespace) -> int:
    cfg = resolve_page(args.page)
    keyword = args.keyword or derive_keyword(cfg)
    use_cases = _resolve_use_cases(cfg, keyword)
    pset = build_prompt_set(keyword, use_cases)
    if (args.engines or "auto").strip().lower() == "auto":
        engines = available_engines()
        if not engines:
            print("  ! no API keys found (OPENAI_API_KEY / GEMINI_API_KEY); "
                  "nothing to capture", file=sys.stderr)
            return 1
    else:
        engines = [e.strip() for e in args.engines.split(",") if e.strip()]

    if args.dry_run:
        print("DRY RUN - no API calls, no files written.")
        print(f"  page:      {args.page}  (wp_page_id={cfg.get('wp_page_id')})")
        print(f"  keyword:   {keyword}")
        print(f"  engines:   {', '.join(engines)}")
        print(f"  prompts:   {len(pset)} x {len(engines)} engine(s) "
              f"= {len(pset) * len(engines)} captures")
        print(f"  output:    research/{args.page}/_answer_audit/runs/<timestamp>/")
        print()
        for label, prompt in pset:
            first = prompt.strip().splitlines()
            headline = next((ln for ln in first if ln and not ln.startswith("You are")), first[0])
            print(f"    - {label}: {headline.strip()[:90]}")
        return 0

    ctx: RunContext = new_run(args.page)
    print(f"Run {ctx.run_id} -> {ctx.root}")
    summary: list[dict[str, Any]] = []
    for label, prompt in pset:
        for engine in engines:
            try:
                if engine == "openai":
                    from .capture import capture_openai
                    res = capture_openai(ctx, prompt, label, model=args.openai_model)
                elif engine == "gemini":
                    from .capture import capture_gemini
                    res = capture_gemini(ctx, prompt, label, model=args.gemini_model)
                else:
                    print(f"  ! unknown engine '{engine}', skipping", file=sys.stderr)
                    continue
                summary.append(res)
                print(f"  ok  {engine:7} {label:24} "
                      f"{res.get('text_chars', 0):>6} chars, "
                      f"{res.get('sources', 0)} sources")
            except Exception as exc:  # one failed witness must not kill the run
                print(f"  FAIL {engine:7} {label:24} {type(exc).__name__}: {exc}",
                      file=sys.stderr)
                (ctx.logs_dir / "warnings.log").open("a", encoding="utf-8").write(
                    f"{engine}\t{label}\t{type(exc).__name__}: {exc}\n")

    index_path = write_source_index(ctx)
    print(f"\nWitnesses captured: {len(ctx.source_index)}")
    print(f"Source index: {index_path}")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    from .corpus import latest_run
    from .extract import extract_nuggets

    run = latest_run(args.page)
    print(f"Extracting coverage delta for {args.page} (run {run.name}, model {args.gemini_model})")
    nuggets, path = extract_nuggets(args.page, model=args.gemini_model, run_dir=run)

    needs = sum(1 for n in nuggets if n.needs_primary_verification)
    print(f"  nuggets (genuinely absent): {len(nuggets)}  "
          f"({needs} need primary verification)")
    by_cat: dict[str, int] = {}
    for n in nuggets:
        by_cat[n.category or "(uncategorised)"] = by_cat.get(n.category or "(uncategorised)", 0) + 1
    for cat, count in sorted(by_cat.items(), key=lambda kv: -kv[1]):
        print(f"    {count:>3}  {cat}")
    print(f"\nNuggets ledger: {path}")
    return 0


def _run_verify(page: str, run: Path, *, ttl_days: int, model: str,
                nuggets_path: Path | None = None, max_live: int | None = None) -> int:
    """Shared verify body used by both `verify` and `audit`."""
    from .ledger import load_jsonl, save_csv, save_jsonl
    from .verify import provider_domains, verify_nuggets, write_human_queue
    from .verify_cache import VerificationCache

    path = nuggets_path or run / "processed" / "nuggets.jsonl"
    if not path.exists():
        print(f"No nuggets ledger at {path}. Run the extract stage first "
              f"(or pass --nuggets <file.jsonl>).", file=sys.stderr)
        return 2

    nuggets = load_jsonl(path)
    domains = provider_domains(page)
    cache = VerificationCache()
    budget = f", max-live {max_live}" if max_live is not None else ""
    print(f"Verifying {len(nuggets)} nugget(s) for {page} "
          f"(cache: {cache.stats().get('total', 0)} entries, ttl {ttl_days}d{budget})")

    def _progress(n, source):
        mark = {"cached": "cache ", "budget": "parked", "live": "live  "}.get(source, source)
        print(f"  [{mark}] {n.verification_status:16} {n.provider:16} {n.detail[:60]}")

    counts = verify_nuggets(nuggets, cache, domains, ttl_days=ttl_days,
                            model=model, max_live=max_live, on_progress=_progress)
    cache.save()
    save_jsonl(nuggets, run / "processed" / "verified-ledger.jsonl")
    save_csv(nuggets, run / "processed" / "verified-ledger.csv")
    queue = write_human_queue(nuggets, run / "reports" / "04-provider-verification-needed.csv")
    print(f"\n{counts}")
    print(f"Verified ledger: {run / 'processed' / 'verified-ledger.csv'}")
    print(f"Human-check queue: {queue}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    from .corpus import latest_run

    run = latest_run(args.page)
    return _run_verify(args.page, run, ttl_days=args.ttl_days, model=args.gemini_model,
                       nuggets_path=Path(args.nuggets) if args.nuggets else None,
                       max_live=args.max_live)


def cmd_recommend(args: argparse.Namespace) -> int:
    from .corpus import latest_run
    from .recommend import recommend_edits

    run = latest_run(args.page)
    print(f"Generating recommendations for {args.page} (run {run.name})")
    out, counts = recommend_edits(args.page, model=args.gemini_model, run_dir=run)
    print(f"  total nuggets:        {counts['total']}")
    print(f"  verified -> edits:    {counts['publishable']}")
    print(f"  needs verification:   {counts['needs_verification']}")
    print(f"\nRecommendations: {out}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    """Orchestrate capture -> consolidate -> extract -> verify -> recommend.

    Stops at the recommendations report. NEVER edits a page: apply-to-live stays
    human-reviewed (Bernstein patch, staging only)."""
    from datetime import datetime, timezone

    from .corpus import consolidate_our_page, consolidate_witnesses, latest_run
    from .core import RESEARCH_DIR
    from .extract import extract_nuggets
    from .recommend import recommend_edits

    # 1. Decide whether to re-capture.
    reuse = args.skip_capture
    if args.incremental and not reuse:
        try:
            prev = latest_run(args.page)
            stamp = datetime.strptime(prev.name, "%Y-%m-%dT%H-%M-%SZ").replace(tzinfo=timezone.utc)
            age_h = (datetime.now(timezone.utc) - stamp).total_seconds() / 3600
            if age_h <= args.ttl_hours:
                reuse = True
                print(f"[incremental] latest run {prev.name} is {age_h:.1f}h old "
                      f"(<= {args.ttl_hours}h) — reusing capture.")
        except Exception:
            pass

    if reuse:
        try:
            run = latest_run(args.page)
        except Exception as exc:
            print(f"No capture run to reuse ({exc}). Run `capture` first or drop "
                  f"--skip-capture.", file=sys.stderr)
            return 2
        print(f"Reusing capture run {run.name}")
    else:
        rc = cmd_capture(argparse.Namespace(
            page=args.page, keyword=None, engines=args.engines,
            openai_model=args.openai_model, gemini_model=args.gemini_model, dry_run=False))
        if rc != 0:
            return rc
        run = latest_run(args.page)

    # 2. Consolidate (idempotent; rebuild witnesses if missing).
    if not (run / "processed" / "witnesses.md").exists():
        consolidate_witnesses(run)
    our_page = run / "processed" / "our-page.txt"
    if not our_page.exists():
        article_html = RESEARCH_DIR / args.page / f"{args.page}.html"
        if article_html.exists():
            consolidate_our_page(run, article_html)

    # 3. Extract delta.
    print("\n== extract ==")
    nuggets, _ = extract_nuggets(args.page, model=args.gemini_model, run_dir=run)
    print(f"  {len(nuggets)} nugget(s) absent from our page")

    # 4. Verify (budget-guarded at the bottleneck).
    print("\n== verify ==")
    rc = _run_verify(args.page, run, ttl_days=args.ttl_days, model=args.gemini_model,
                     max_live=args.max_verifications)
    if rc != 0:
        return rc

    # 5. Recommend (stops here; never edits the page).
    print("\n== recommend ==")
    out, counts = recommend_edits(args.page, model=args.gemini_model, run_dir=run)
    print(f"\nDONE. {counts['publishable']} verified recommendation(s), "
          f"{counts['needs_verification']} parked for human verification.")
    print(f"Review: {out}")
    print("This tool stops at recommendations. Apply-to-live stays human "
          "(Bernstein patch --humanise-note, staging only).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="answer_engine_audit",
                                     description="Answer-Engine Coverage Audit System")
    sub = parser.add_subparsers(dest="command", required=True)

    cap = sub.add_parser("capture", help="Capture raw answer-engine witnesses")
    cap.add_argument("--page", required=True, help="page slug (matches PAGE_CONFIG['slug'])")
    cap.add_argument("--keyword", help="override the target query (defaults to title head)")
    cap.add_argument("--engines", default="auto",
                     help="comma list (openai,gemini) or 'auto' = engines with keys present")
    cap.add_argument("--openai-model", default="gpt-4o")
    cap.add_argument("--gemini-model", default="gemini-2.5-flash")
    cap.add_argument("--dry-run", action="store_true",
                     help="print the capture plan without calling any API")
    cap.set_defaults(func=cmd_capture)

    ext = sub.add_parser("extract", help="Extract the coverage delta (nuggets we lack)")
    ext.add_argument("--page", required=True, help="page slug")
    ext.add_argument("--gemini-model", default="gemini-2.5-flash",
                     help="cheaper model for the delta pass")
    ext.set_defaults(func=cmd_extract)

    ver = sub.add_parser("verify", help="Verify nuggets against provider sites (uses cache)")
    ver.add_argument("--page", required=True, help="page slug")
    ver.add_argument("--nuggets", help="path to nuggets JSONL (default: latest run's processed/nuggets.jsonl)")
    ver.add_argument("--ttl-days", type=int, default=90, help="cache freshness window")
    ver.add_argument("--max-live", type=int, default=None,
                     help="cap on live (non-cached) grounded calls; rest parked for a human")
    ver.add_argument("--gemini-model", default="gemini-2.5-flash")
    ver.set_defaults(func=cmd_verify)

    rec = sub.add_parser("recommend", help="Turn the verified ledger into 06-recommended-edits.md")
    rec.add_argument("--page", required=True, help="page slug")
    rec.add_argument("--gemini-model", default="gemini-2.5-flash")
    rec.set_defaults(func=cmd_recommend)

    aud = sub.add_parser("audit", help="Full pipeline: capture -> extract -> verify -> recommend")
    aud.add_argument("--page", required=True, help="page slug")
    aud.add_argument("--skip-capture", action="store_true",
                     help="reuse the latest capture run instead of re-capturing")
    aud.add_argument("--incremental", action="store_true",
                     help="reuse the latest capture if it is within --ttl-hours")
    aud.add_argument("--ttl-hours", type=float, default=168.0,
                     help="freshness window for --incremental capture reuse (default 7 days)")
    aud.add_argument("--ttl-days", type=int, default=90, help="verification cache freshness window")
    aud.add_argument("--max-verifications", type=int, default=40,
                     help="per-run budget: max live grounded verify calls (rest parked)")
    aud.add_argument("--engines", default="auto", help="comma list (openai,gemini) or 'auto' = engines with keys present")
    aud.add_argument("--openai-model", default="gpt-4o")
    aud.add_argument("--gemini-model", default="gemini-2.5-flash")
    aud.set_defaults(func=cmd_audit)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
