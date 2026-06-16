"""CLI for the Answer-Engine Coverage Audit System.

The audit's unit of work is a LIVE companydebt.com page resolved from the
sitemap (not a local PAGE_CONFIG). A target may be given as a full URL, a path,
or a bare last-segment slug.

Examples:
    python -m scripts.answer_engine_audit sitemap            # list auditable pages
    python -m scripts.answer_engine_audit capture  --target /advice/misfeasance/
    python -m scripts.answer_engine_audit audit    --target misfeasance
    python -m scripts.answer_engine_audit audit    --all --limit 10
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from . import prompts
from .core import (
    RunContext, available_engines, new_run_for_target, read_run_meta,
    write_source_index,
)


def build_prompt_set(keyword: str, use_cases: list[str]) -> list[tuple[str, str]]:
    """Return (label, prompt) pairs. Labels become raw filenames."""
    pset: list[tuple[str, str]] = [
        ("broad", prompts.BROAD_ANSWER.format(keyword=keyword)),
        ("risk", prompts.RISK_DRAWBACK.format(keyword=keyword)),
    ]
    for i, q in enumerate(use_cases, 1):
        pset.append((f"usecase-{i}", prompts.USE_CASE.format(keyword=keyword, question=q)))
    return pset


def _resolve_engines(spec: str) -> list[str]:
    if (spec or "auto").strip().lower() == "auto":
        return available_engines()
    return [e.strip() for e in spec.split(",") if e.strip()]


def _target_key(target: str) -> str:
    """Storage key for a target, via the sitemap. Lets extract/verify/recommend
    find the latest run without re-fetching the page."""
    from . import sitemap
    return sitemap.resolve_target(target).key


# --------------------------------------------------------------------------
# sitemap
# --------------------------------------------------------------------------

def cmd_sitemap(args: argparse.Namespace) -> int:
    from . import sitemap

    data = sitemap.load_urls(force=args.refresh)
    c = data["counts"]
    print(f"Sitemap: {sitemap.BASE}  (fetched {data['fetched_at']})")
    print(f"  auditable: {c['auditable']}   skipped: {c['skipped']}   "
          f"total in content sitemaps: {c['total']}")
    if args.skipped:
        by_reason: dict[str, int] = {}
        for s in data["skipped"]:
            by_reason[s["reason"]] = by_reason.get(s["reason"], 0) + 1
        print("\nSkipped by reason:")
        for reason, n in sorted(by_reason.items(), key=lambda kv: -kv[1]):
            print(f"  {n:>4}  {reason}")
    print("\nAuditable pages:")
    refs = [sitemap._ref(u) for u in data["auditable"]]
    for r in sorted(refs, key=lambda r: r.path)[: args.limit or None]:
        print(f"  {r.path}")
    if args.limit and len(refs) > args.limit:
        print(f"  ... ({len(refs) - args.limit} more; raise --limit to see all)")
    return 0


# --------------------------------------------------------------------------
# capture
# --------------------------------------------------------------------------

def cmd_capture(args: argparse.Namespace) -> int:
    engines = _resolve_engines(args.engines)
    if not engines:
        print("  ! no API keys found (OPENAI_API_KEY / GEMINI_API_KEY); "
              "nothing to capture", file=sys.stderr)
        return 1

    if args.dry_run:
        ctx = new_run_for_target(args.target, dry_run=True)
        use_cases = prompts.default_use_cases(ctx.keyword)
        pset = build_prompt_set(ctx.keyword, use_cases)
        print("DRY RUN - no API calls, no files written.")
        print(f"  target:    {args.target}")
        print(f"  url:       {ctx.url}")
        print(f"  key:       {ctx.slug}")
        print(f"  keyword:   {ctx.keyword}  (from path slug)")
        print(f"  engines:   {', '.join(engines)}")
        print(f"  prompts:   {len(pset)} x {len(engines)} engine(s) "
              f"= {len(pset) * len(engines)} captures")
        for label, prompt in pset:
            lines = prompt.strip().splitlines()
            headline = next((ln for ln in lines if ln and not ln.startswith("You are")), lines[0])
            print(f"    - {label}: {headline.strip()[:90]}")
        return 0

    ctx: RunContext = new_run_for_target(args.target)
    print(f"Run {ctx.run_id} -> {ctx.root}")
    print(f"  url: {ctx.url}")
    print(f"  keyword: {ctx.keyword}")
    use_cases = prompts.default_use_cases(ctx.keyword)
    pset = build_prompt_set(ctx.keyword, use_cases)

    # Demand layer (opt-in): seed capture with real Ahrefs search demand so the
    # engines are probed on what people actually search, not just the page's own
    # framing. Never lets a demand hiccup kill the base capture.
    demand_record = None
    if getattr(args, "demand", False):
        from . import demand as demand_mod
        demand_seed = demand_mod.resolve_seed(ctx.cfg, ctx.keyword,
                                              getattr(args, "demand_seed", None))
        try:
            demand_record = demand_mod.collect_demand(
                demand_seed, country=getattr(args, "demand_country", "gb"),
                min_volume=getattr(args, "demand_min_volume", 0),
                top_n=getattr(args, "demand_top_n", 30),
                model=args.gemini_model,
                fixture=getattr(args, "demand_fixture", None))
            pset += demand_mod.demand_prompt_set(demand_record, demand_seed)
            print(f"  demand: seed '{demand_seed}' fetched {demand_record['fetched']}, "
                  f"kept {demand_record['kept']} probe(s), dropped {demand_record['dropped']}")
        except Exception as exc:  # never let demand kill the base capture
            print(f"  demand skipped: {type(exc).__name__}: {exc}", file=sys.stderr)

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
                print(f"  ok  {engine:7} {label:24} "
                      f"{res.get('text_chars', 0):>6} chars, "
                      f"{res.get('sources', 0)} sources")
            except Exception as exc:  # one failed witness must not kill the run
                print(f"  FAIL {engine:7} {label:24} {type(exc).__name__}: {exc}",
                      file=sys.stderr)
                (ctx.logs_dir / "warnings.log").open("a", encoding="utf-8").write(
                    f"{engine}\t{label}\t{type(exc).__name__}: {exc}\n")

    # Consolidate "our page" from the live snapshot taken in new_run_for_target.
    from .corpus import consolidate_our_page
    live = ctx.raw_dir / "our-page.html"
    if live.exists():
        consolidate_our_page(ctx.root, live)

    if demand_record is not None:
        import json as _json
        (ctx.processed_dir / "demand.json").write_text(
            _json.dumps(demand_record, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Demand record: {ctx.processed_dir / 'demand.json'}")

    index_path = write_source_index(ctx)
    print(f"\nWitnesses captured: {len(ctx.source_index)}")
    print(f"Source index: {index_path}")
    return 0


# --------------------------------------------------------------------------
# demand (standalone preview: Ahrefs demand -> AI probes, no engine calls)
# --------------------------------------------------------------------------

def cmd_demand(args: argparse.Namespace) -> int:
    """Preview the demand layer: Ahrefs matching terms -> filtered, volume-ranked
    natural-language probes. No answer-engine calls; writes a JSON + CSV preview."""
    import csv
    import json as _json

    from . import demand as demand_mod

    ctx = new_run_for_target(args.target, dry_run=True)
    seed = demand_mod.resolve_seed(ctx.cfg, ctx.keyword, args.demand_seed)
    src = f"fixture {args.demand_fixture}" if args.demand_fixture else "Ahrefs API"
    print(f"Demand preview for '{seed}' via {src} "
          f"(country {args.demand_country}, top {args.demand_top_n}, "
          f"min volume {args.demand_min_volume})")
    record = demand_mod.collect_demand(
        seed, country=args.demand_country, min_volume=args.demand_min_volume,
        top_n=args.demand_top_n, model=args.gemini_model,
        fixture=args.demand_fixture)
    print(f"  fetched {record['fetched']}, kept {record['kept']}, "
          f"dropped {record['dropped']}")
    for row in record["rows"]:
        print(f"    [{row['volume']:>6}] {row['intent']:13} {row['keyword']}")
        print(f"             -> {row['probe']}")

    outdir = ctx.root.parent  # research/<key>/_answer_audit/
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "demand-latest.json").write_text(
        _json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    csv_path = outdir / "demand-latest.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["keyword", "volume", "intent", "probe"])
        for row in record["rows"]:
            w.writerow([row["keyword"], row["volume"], row["intent"], row["probe"]])
    print(f"\n  JSON: {outdir / 'demand-latest.json'}")
    print(f"  CSV:  {csv_path}")
    return 0


# --------------------------------------------------------------------------
# extract / verify / recommend
# --------------------------------------------------------------------------

def cmd_extract(args: argparse.Namespace) -> int:
    from .corpus import latest_run
    from .extract import extract_nuggets

    key = _target_key(args.target)
    run = latest_run(key)
    print(f"Extracting coverage delta for {key} (run {run.name}, model {args.gemini_model})")
    nuggets, path = extract_nuggets(
        key, model=args.gemini_model, run_dir=run,
        concept_guard=not args.no_concept_guard, semantic_guard=args.semantic_guard)

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


def _run_verify(key: str, run: Path, *, ttl_days: int, model: str,
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
    domains = provider_domains(key)
    cache = VerificationCache()
    budget = f", max-live {max_live}" if max_live is not None else ""
    print(f"Verifying {len(nuggets)} nugget(s) for {key} "
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

    key = _target_key(args.target)
    run = latest_run(key)
    return _run_verify(key, run, ttl_days=args.ttl_days, model=args.gemini_model,
                       nuggets_path=Path(args.nuggets) if args.nuggets else None,
                       max_live=args.max_live)


def cmd_recommend(args: argparse.Namespace) -> int:
    from .corpus import latest_run
    from .recommend import recommend_edits

    key = _target_key(args.target)
    run = latest_run(key)
    print(f"Generating recommendations for {key} (run {run.name})")
    out, counts = recommend_edits(key, model=args.gemini_model, run_dir=run,
                                  max_gaps=args.max_coverage_gaps)
    print(f"  total nuggets:        {counts['total']}")
    print(f"  verified -> edits:    {counts['publishable']}")
    print(f"  apply list (capped):  {counts.get('headline', 0)}")
    print(f"  appendix:             {counts.get('appendix', 0)}")
    print(f"  needs verification:   {counts['needs_verification']}")
    print(f"\nRecommendations: {out}")
    return 0


# --------------------------------------------------------------------------
# audit (single page, or --all over the sitemap in batches)
# --------------------------------------------------------------------------

def _audit_one(target: str, args: argparse.Namespace) -> int:
    """Full pipeline for ONE live page. Stops at the recommendations report;
    NEVER edits a page (apply-to-live stays human, Bernstein patch, staging)."""
    from datetime import datetime, timezone

    from .corpus import consolidate_our_page, consolidate_witnesses, latest_run
    from .extract import extract_nuggets
    from .recommend import recommend_edits
    from .source_landscape import write_source_landscape

    key = _target_key(target)

    # 1. Decide whether to re-capture.
    reuse = args.skip_capture
    if args.incremental and not reuse:
        try:
            prev = latest_run(key)
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
            run = latest_run(key)
        except Exception as exc:
            print(f"No capture run to reuse ({exc}). Run `capture` first or drop "
                  f"--skip-capture.", file=sys.stderr)
            return 2
        print(f"Reusing capture run {run.name}")
    else:
        rc = cmd_capture(argparse.Namespace(
            target=target, engines=args.engines, openai_model=args.openai_model,
            gemini_model=args.gemini_model, dry_run=False,
            demand=getattr(args, "demand", False),
            demand_seed=getattr(args, "demand_seed", None),
            demand_country=getattr(args, "demand_country", "gb"),
            demand_top_n=getattr(args, "demand_top_n", 30),
            demand_min_volume=getattr(args, "demand_min_volume", 0),
            demand_fixture=getattr(args, "demand_fixture", None)))
        if rc != 0:
            return rc
        run = latest_run(key)

    # 2. Consolidate (idempotent).
    if not (run / "processed" / "witnesses.md").exists():
        consolidate_witnesses(run)
    our_page = run / "processed" / "our-page.txt"
    live_html = run / "raw" / "our-page.html"
    if not our_page.exists() and live_html.exists():
        consolidate_our_page(run, live_html)

    # 2b. Source landscape (deterministic — WHO the engines cite for this query).
    # This is the heart of the AEO/GEO design: before reading our page we read the
    # citation landscape, so the extract stage can work query-first (close the gaps
    # competitor domains win) instead of regressing to a flat fact-check.
    print("\n== source landscape ==")
    keyword = read_run_meta(run).get("keyword", "") or key.replace("__", " ").replace("-", " ")
    land_path, land = write_source_landscape(key, keyword, run)
    we = "cited" if land["we_cited"] else "NOT cited"
    top = ", ".join(f"{d}({c})" for d, c in land["competitors"][:5]) or "none resolved"
    print(f"  companydebt.com is {we} for this query; top cited: {top}")
    print(f"  {land_path}")

    # 3. Extract delta.
    print("\n== extract ==")
    nuggets, _ = extract_nuggets(
        key, model=args.gemini_model, run_dir=run,
        concept_guard=not args.no_concept_guard, semantic_guard=args.semantic_guard)
    print(f"  {len(nuggets)} nugget(s) absent from our page")

    # 4. Verify (budget-guarded at the bottleneck).
    print("\n== verify ==")
    rc = _run_verify(key, run, ttl_days=args.ttl_days, model=args.gemini_model,
                     max_live=args.max_verifications)
    if rc != 0:
        return rc

    # 5. Recommend (stops here; never edits the page).
    print("\n== recommend ==")
    out, counts = recommend_edits(key, model=args.gemini_model, run_dir=run,
                                  max_gaps=args.max_coverage_gaps)
    print(f"\nDONE {key}. {counts['publishable']} verified recommendation(s), "
          f"{counts['needs_verification']} parked for human verification, "
          f"{counts.get('cannibalisation_risk', 0)} flagged as cannibalisation risk.")
    print(f"Review: {out}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    if args.all:
        from . import sitemap
        refs = sorted(sitemap.auditable_refs(), key=lambda r: r.path)
        if args.limit:
            refs = refs[: args.limit]
        total = len(refs)
        print(f"Auditing {total} live page(s) in batches of {args.batch_size}. "
              f"Apply-to-live stays human (Bernstein patch, staging only).")
        ok = fail = 0
        for i, ref in enumerate(refs, 1):
            print(f"\n========== [{i}/{total}] {ref.path} ==========")
            try:
                rc = _audit_one(ref.url, args)
            except Exception as exc:  # one bad page must not stop the sweep
                print(f"  FAIL {ref.path}: {type(exc).__name__}: {exc}", file=sys.stderr)
                rc = 1
            ok += rc == 0
            fail += rc != 0
            if args.batch_size and i % args.batch_size == 0 and i < total:
                print(f"\n--- batch boundary ({i}/{total}); verification cache "
                      f"warmed, continuing ---")
        print(f"\nSweep complete: {ok} ok, {fail} failed, {total} total.")
        return 0 if fail == 0 else 1

    if not args.target:
        print("Pass --target <url|path|slug> or --all.", file=sys.stderr)
        return 2
    return _audit_one(args.target, args)


# --------------------------------------------------------------------------
# argument parsing
# --------------------------------------------------------------------------

def _add_target(p: argparse.ArgumentParser) -> None:
    p.add_argument("--target", help="live page: full URL, path (/advice/x/), or bare slug")


def _add_demand_args(p: argparse.ArgumentParser, *, include_toggle: bool) -> None:
    """Shared --demand-* flags. ``include_toggle`` adds the on/off --demand flag
    (capture/audit); the standalone `demand` subcommand is always on."""
    if include_toggle:
        p.add_argument("--demand", action="store_true",
                       help="seed capture with real Ahrefs search demand (Ahrefs API/fixture + Gemini)")
    p.add_argument("--demand-seed",
                   help="Ahrefs seed term (default: topic from page keyword / cfg['demand_seed'])")
    p.add_argument("--demand-country", default="gb", help="Ahrefs country code (default gb)")
    p.add_argument("--demand-top-n", type=int, default=30,
                   help="max demand probes, volume-ranked (default 30)")
    p.add_argument("--demand-min-volume", type=int, default=0,
                   help="drop keywords below this monthly search volume")
    p.add_argument("--demand-fixture",
                   help="saved Ahrefs export (CSV or JSON) to use instead of the live API")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="answer_engine_audit",
                                     description="Answer-Engine Coverage Audit System")
    sub = parser.add_subparsers(dest="command", required=True)

    sm = sub.add_parser("sitemap", help="List auditable pages from the live sitemap")
    sm.add_argument("--refresh", action="store_true", help="force a live re-fetch of the sitemap")
    sm.add_argument("--skipped", action="store_true", help="show counts of excluded pages by reason")
    sm.add_argument("--limit", type=int, default=0, help="cap how many paths are printed (0 = all)")
    sm.set_defaults(func=cmd_sitemap)

    cap = sub.add_parser("capture", help="Capture raw answer-engine witnesses")
    _add_target(cap)
    cap.add_argument("--engines", default="auto",
                     help="comma list (openai,gemini) or 'auto' = engines with keys present")
    cap.add_argument("--openai-model", default="gpt-4o")
    cap.add_argument("--gemini-model", default="gemini-2.5-flash")
    cap.add_argument("--dry-run", action="store_true",
                     help="print the capture plan without calling any API")
    _add_demand_args(cap, include_toggle=True)
    cap.set_defaults(func=cmd_capture)

    dem = sub.add_parser("demand",
                         help="Preview Ahrefs demand -> AI probes (no engine calls)")
    _add_target(dem)
    dem.add_argument("--gemini-model", default="gemini-2.5-flash")
    _add_demand_args(dem, include_toggle=False)
    dem.set_defaults(func=cmd_demand)

    ext = sub.add_parser("extract", help="Extract the coverage delta (nuggets we lack)")
    _add_target(ext)
    ext.add_argument("--gemini-model", default="gemini-2.5-flash",
                     help="cheaper model for the delta pass")
    ext.add_argument("--no-concept-guard", action="store_true",
                     help="disable the deterministic already-covered concept guard")
    ext.add_argument("--semantic-guard", action="store_true",
                     help="add an opt-in Gemini-embedding already-covered pass (extra API calls)")
    ext.set_defaults(func=cmd_extract)

    ver = sub.add_parser("verify", help="Verify nuggets against authoritative sources (uses cache)")
    _add_target(ver)
    ver.add_argument("--nuggets", help="path to nuggets JSONL (default: latest run's processed/nuggets.jsonl)")
    ver.add_argument("--ttl-days", type=int, default=90, help="cache freshness window")
    ver.add_argument("--max-live", type=int, default=None,
                     help="cap on live (non-cached) grounded calls; rest parked for a human")
    ver.add_argument("--gemini-model", default="gemini-2.5-flash")
    ver.set_defaults(func=cmd_verify)

    rec = sub.add_parser("recommend", help="Turn the verified ledger into 06-recommended-edits.md")
    _add_target(rec)
    rec.add_argument("--gemini-model", default="gemini-2.5-flash")
    rec.add_argument("--max-coverage-gaps", type=int, default=10,
                     help="cap on the section-1 apply list; the rest go to the appendix")
    rec.set_defaults(func=cmd_recommend)

    aud = sub.add_parser("audit", help="Full pipeline: capture -> extract -> verify -> recommend")
    _add_target(aud)
    aud.add_argument("--all", action="store_true", help="audit every auditable sitemap page (batched)")
    aud.add_argument("--limit", type=int, default=0, help="with --all, cap how many pages to process")
    aud.add_argument("--batch-size", type=int, default=10,
                     help="with --all, pages per batch (cache warms between batches)")
    aud.add_argument("--skip-capture", action="store_true",
                     help="reuse the latest capture run instead of re-capturing")
    aud.add_argument("--incremental", action="store_true",
                     help="reuse the latest capture if it is within --ttl-hours")
    aud.add_argument("--ttl-hours", type=float, default=168.0,
                     help="freshness window for --incremental capture reuse (default 7 days)")
    aud.add_argument("--ttl-days", type=int, default=90, help="verification cache freshness window")
    aud.add_argument("--max-verifications", type=int, default=40,
                     help="per-run budget: max live grounded verify calls (rest parked)")
    aud.add_argument("--max-coverage-gaps", type=int, default=10,
                     help="cap on the section-1 apply list; the rest go to the appendix")
    aud.add_argument("--engines", default="auto", help="comma list (openai,gemini) or 'auto' = engines with keys present")
    aud.add_argument("--openai-model", default="gpt-4o")
    aud.add_argument("--gemini-model", default="gemini-2.5-flash")
    aud.add_argument("--no-concept-guard", action="store_true",
                     help="disable the deterministic already-covered concept guard")
    aud.add_argument("--semantic-guard", action="store_true",
                     help="add an opt-in Gemini-embedding already-covered pass (extra API calls)")
    _add_demand_args(aud, include_toggle=True)
    aud.set_defaults(func=cmd_audit)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RuntimeError as exc:  # resolution / setup errors: clean message, no traceback
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return 130
    except Exception as exc:  # API 5xx (e.g. Gemini high-demand) and the like
        name = type(exc).__name__
        hint = ""
        if "503" in str(exc) or "UNAVAILABLE" in str(exc):
            hint = "  (model overloaded; this is transient: retry off-peak or batch fewer pages)"
        print(f"error: {name}: {exc}{hint}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
