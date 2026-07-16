# Feasibility & Maintenance-Burden Critique (Adversarial Pass)

Date: 2026-07-10 (audit date). Judge: feasibility/maintenance lens only.
Note: foundation files 01-06 were absent from the scratchpad at judging time; repo-context grounding
comes from project CLAUDE.md and the persistent project memory (verified constraints listed below).
Analysis files 10-17 were present and the recommendations' own evidence was taken as stated.

## The binding constraint the recommendation set ignores

Every content page on this site goes through the Bernstein pipeline on Opus, one page at a time,
with a mechanical gate AND genuine named-IP human sign-off (a hard, non-fakeable gate). Realistic
throughput is a handful of pages per week for the whole site. The 61 recommendations, taken at face
value, imply roughly 40-60 pipeline items (new pages + rewrites) plus at least five distinct
infrastructure builds and four new ongoing operational commitments. That is 4-6 months of exclusive
pipeline capacity before counting the in-flight 25-page sector rewrite. The set is individually
sensible and collectively impossible. The main output of this critique is therefore DEDUPLICATION
and SEQUENCING, not wholesale killing: most recommendations survive, but ~30 are folded into a
canonical owner so the same work is not done (or gated, or signed off) three times.

## Duplicate-cluster map (the core finding)

The 61 recommendations collapse into far fewer real workstreams. Canonical owner in bold:

1. **Liquidation-core rescue** — de-cannibalise (CV#1, keep for the redirect/consolidation half) +
   **re-shape CVL/MVL to service-intent (SEO#16, keep)** absorb "Recover CVL, cost page and hub
   visibility" (IJ#11). Three recs currently imply three separate editing passes over the SAME
   pages; each pass costs a full gate + IP sign-off. Do it as ONE pass per page: title/H1/first-
   viewport re-shape + first-screen intent pattern + H2 de-overlap, plus the strike-off 301s.
2. **Winding-up-petition** — **SEO#19 (keep: split one post-order page, cross-link tracker)**
   absorbs the "stage-triaged cluster rebuild" (IJ#9), which as written is a multi-page rebuild of
   the site's crisis content. Restructure the existing hub for stage triage; do not build a cluster.
3. **MVL calculator** — **MON#48 (keep)** absorbs CRO#34 (near-exact duplicate) and the calculator
   element of IJ#10. Build once. Hidden maintenance cost acknowledged: BADR/CGT rates change at
   least annually; wire it to a statutory source-of-truth JSON like data/statutory_fees.json or it
   will silently rot — a wrong tax figure on a YMYL page is worse than no calculator.
4. **Email programme** — **MON#52 (keep: consent fix + post-enquiry sequence)** absorbs the email
   halves of CV#8 (killed — gating contradicts three other recs and damages rankings/AEO), IJ#13,
   CRO#38, CRO#37's newsletter, and DEF#60's "gate the guide". One ESP decision, one GDPR/consent
   review, one nurture build. Five recommendations were independently proposing this infrastructure
   without costing it once.
5. **Data-hub credibility layer** — **TRUST#40 (keep)** absorbs SEO#18's credibility half, CRO#37,
   MON#50's packaging half, and DEF#56 (killed as exact duplicate). Methodology/named analyst/press
   contact/cite-block/CSV = one work item, days not weeks, substance already in
   docs/data-hub/architecture.md. The "ship /data/ live" half of SEO#18 duplicates work already in
   flight (staging, awaiting visual QA) — it is a priority nudge, not a new task.
6. **Accountant referrer page + stats briefing** — **MON#49 (keep)** absorbs IJ#15 (killed as
   duplicate) and DEF#60's digest/referrer elements. The monthly briefing is a real recurring
   commitment but piggybacks the existing scripted monthly data-hub update, so the marginal
   ongoing cost is genuinely low. Do NOT let it become a separate newsletter product.
7. **Prune/freshness budget** — **DEF#61 (keep: the ~80-page freshness core is the right operating
   frame for a small team)** absorbs SEO#23 and reshapes CV#5. One pruning pass, one backlink-check
   protocol, one Quick Redirects batch (qppr redirect-loss guard already exists in the repo).
8. **Sector estate** — CV#4 (keep: cut 25→~8) + SEO#21 (keep: 301 the 8 duplicates first) absorb
   IA#30's sector half. This cluster is the single largest capacity saving available: ~17 avoided
   Opus rewrites. Caveat: the demand evidence for the cut is inference-from-absence; verify
   per-page GSC + backlinks before each 301, and the scope cut is an owner call against the
   in-flight programme he started on 2026-07-10.
9. **Entity/brand graph** — DEF#59 and TRUST#46 are one project (Organization JSON-LD, sameAs,
   Wikidata, linked badges/press logos, plain-English network map). Both modified to merge. The
   "reviews consolidation" and network-fee-map elements are owner/compliance calls, not team tasks.
10. **Review + case-study ops** — CRO#36, TRUST#43, TRUST#45 all require the same new firm-side
    operational muscle (post-case review requests, client consent for figures, IP time). The copy
    fixes (retire "9 reviews", retire "Trusted by Thousands") are trivial and immediate; the ops
    programme needs a named owner inside the firm before it is a plan rather than a wish.
11. **Phone instrumentation** — CRO#31 and the tracking element of MON#47. Real gap, but as
    written it (a) makes itself a blocking gate for all other CRO work, (b) proposes DNI
    JavaScript on a site whose active perf-remediation programme identified third-party JS as the
    exact problem, and (c) omits the subscription cost and the "who reviews call data monthly"
    ownership question. Reshape: 3-5 static tracked numbers by page class, no DNI, not blocking.
12. **30-Second Test** — CRO#32 (keep: result-first is the core verified promise-break fix)
    absorbs IJ#13's branching (same dev session). Email capture goes to workstream 4.

## Per-recommendation notes beyond the cluster map

- CV#2 (take-money-out → MVL section): cleanest rec in the set. One section + links on an existing
  page. Keep.
- CV#3 (director-liability funnel): low effort, existing pages. Sequence the CTA rollout AFTER the
  30-Second Test rework — routing the site's best distress traffic into the current gated,
  promise-breaking test would waste it. Keep.
- CV#5 (celebrity morgue / BBL 7→2): redirects are cheap and reduce maintenance; killing 11% of
  clicks is an owner call but feasibility says fine. The "consolidate BBL 7→2" half as written
  means pipeline work consolidating content for structurally decaying demand — do straight 301s
  into the best existing BBL page (keep the pos-9.6 BBL-liquidation earner) instead of authoring
  consolidated pages. Modify.
- CV#6 (TTP upgrade, medium effort): killed as superseded — SEO#22 is the same page at lower cost
  with no implied supporting cluster. Two TTP recs = one page.
- CV#7 (Q&A engine): the "protect" half is free and correct — adopt as a standing rule in the
  prune workstream. The "feed" half must not become a content programme; new Q&A pages only when a
  specific query shows striking-distance GSC evidence, because each one displaces a money-page
  slot in the pipeline. Modify.
- CV#8 (gate sample letters): KILL. Directly contradicts MON#52 and DEF#60's own caveat ("never
  gating the letters/PDF, which would damage rankings, AEO citability and the generosity
  signal") — the same audit argues both sides; the ungated+optional-email side has the better
  argument and the lower burden.
- SEO#17 (no-money page): one new page, strong verified evidence (competitor's best asset, CD's
  equivalent 404s). Keep. Must respect the banned £9,000 redundancy-average figure and the
  statutory-fees source-of-truth guard.
- SEO#20 (Gazette-notice page): fine single-page build, but sequence AFTER the strike-off
  consolidation in workstream 1 — adding a fourth page into a currently cannibalised strike-off
  cluster repeats the exact pathology CV#1 diagnoses. Modify.
- IA#24/#25/#27/#28/#29: all cheap, bounded, high-leverage template/link edits. Keep all five.
  Caveats: IA#24 and IA#28 are gated on /data/ going live; IA#27 must verify deploys land (the
  repo has a documented draft/staging link-deploy gap where ~25/54 anchor fixes silently no-op'd);
  IA#28 must go through the data-page build scripts (CD-NO-AUTOEDIT sentinel).
- IA#26 (hub rebuilds): the /liquidation/ hub template with themed child blocks is justified by
  its numbers. "Then /hmrc/, /insolvency/" is pre-committed scope creep — prove the pattern on one
  hub first. Modify.
- CRO#33 (emergency tier): sticky mobile call bar + petition/hearing-date field are cheap and
  good. The priority-callback/out-of-hours PROMISE is an unstaffed commitment — a broken urgency
  promise to a director whose bank account freezes tomorrow is a trust catastrophe, not a CRO win.
  Ship the mechanics, not the promise, until the firm commits response capacity. Modify.
- CRO#35 (expectation-setting): trivial copy. One check: "a licensed IP calls you same working
  day" must be verified true with the firm before publication (never-fake rule extends to ops
  claims). Keep.
- TRUST#39 (author entity layer): 4 profile pages + schema; small real dependency on IP
  cooperation (bios, photos, register links) but one-off. Cheapest E-E-A-T win in the set. Keep.
- TRUST#41 (editorial standards): condensation of existing internal material; nav/about-class
  pages are exempt from the Bernstein requirement per repo rules. Keep.
- TRUST#42 (split author/reviewer): as written it risks violating the repo's hard
  never-fake-authorship gate — crediting Newton/Bradstock/Meadows as reviewers of ~300 URLs they
  did not review is fabricated authorship with a different name on it. Reshape: assign topic-area
  reviewers going forward, applied per-page as pages pass through the pipeline anyway (zero
  marginal cost), with genuine review each time. No mass retrofit. Modify.
- TRUST#44 (date-honesty): bounded one-off pass, reduces risk, no ongoing cost. Keep.
- TRUST#45 (case studies): 5-8 is too many to start — each needs client consent, real figures, IP
  time, and a pipeline slot. Start with 2-3 where consent is easiest (CVL, MVL, TTP), interlink
  from money pages, expand only if they demonstrably convert. Firm buy-in is the gating input.
  Modify.
- MON#47: three bundled items with three different cost profiles. Form qualifiers: cheap, aligned
  with the form-attribution work already on staging — yes. Call tracking: per workstream 11.
  Evening/weekend callback picker: only offer slots someone will actually staff. Modify.
- MON#51 (redundancy-funded CVL framing): pure framing on existing pages, compatible with the
  no-DIY-steer rule, and the differentiator is already disclosed. Keep. Banned-figure guard applies.
- MON#53 (PG insurance / personal-debt referral pilot): textbook "dependency on partners that
  don't exist". Partner sourcing, FCA-status vetting, introducer agreements, compliance review,
  and ongoing partner QA are owner-level work with uncertain return, and the rec's own caveat
  ("a bad partner costs more trust than the fees earn") is the feasibility verdict. Reshape:
  first check whether the existing disclosed AABRS/network relationship already covers personal
  insolvency (likely) and route spillover there with the existing disclosure language; the PGI
  introducer pilot goes on the owner backlog, not the team plan. Modify.
- MON#54 (no display ads): a stop-doing rec that prevents work and protects the perf programme.
  Keep. The £250-£500/yr arithmetic is decisive on its own.
- DEF#55 (AEO → AIO): retargets an existing, running pipeline at the surface that matters;
  the top-5-organic-but-uncited page list is a bounded, evidence-led queue. Keep.
- DEF#57 (Brand Radar): an afternoon, uses existing subscription. Name who reviews it monthly or
  it will be zero-prompts again by October. Keep.
- DEF#58 (payment-practices + petition tracker + PR cadence): tracker is already built (ships with
  /data/ — duplicate of in-flight work). Payment-practices page is a real, specced build aligned
  with the owner's data-layer-first steer — legitimate. The MONTHLY IP-quoted release-note cadence
  is the unstated maintenance bomb: it commits a named IP every month indefinitely and journalists
  punish a broken cadence. Start quarterly or fold quotes into the existing monthly stats update.
  Modify.

## Ongoing-commitment register (what the plan quietly signs the team up for)

If the modified set is adopted, the NEW standing obligations are:
1. Monthly stats briefing email (piggybacks existing monthly data update) — low marginal.
2. Post-enquiry email sequence upkeep — low after build.
3. MVL calculator rate maintenance — annual, must be guarded by source-of-truth file.
4. Call-tracking subscription + monthly review — needs a named owner.
5. Review-request ops — needs a firm-side owner; do not start without one.
6. Release-note cadence for data assets — quarterly, not monthly, until proven sustainable.
Everything else in the surviving set is one-off or absorbed into existing workflows.

## Verdict tallies

Keep 27, Modify 29, Kill 5 (CV#6, CV#8, IJ#15, CRO#34, DEF#56 — one bad idea, four duplicates of
better-specified siblings).

## Sequencing sanity (first 6 weeks, pipeline-realistic)

1. Free/trivial wins requiring no pipeline slot: retire "9 reviews" + "Trusted by Thousands" copy,
   footer /data/ repoint (once live), cost page into nav + hub link, leaked-equity redirects,
   typo-slug redirect, consent-gap fix, Brand Radar prompts, badge/logo linking, date-honesty pass.
2. Data-hub credibility layer (TRUST#40) — before the next outreach batch goes out.
3. Liquidation-core single pass (workstream 1): CVL, MVL, cost page, hub template, strike-off 301s.
4. 30-Second Test rework (result-first + branching).
5. Sector-estate settlement (301 duplicates, cut rewrite scope) — before the rewrite programme
   ships more pages into a broken structure.
6. Then and only then: new pages (no-money, WUP split, MVL-vs-strike-off, Gazette, referrer page)
   one at a time in evidence order.
