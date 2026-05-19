# Backlink Redirect Audit — 2026-05-19

Source: Ahrefs backlink export (796 backlinks / 215 target URLs)

## Summary

After filtering spam and off-topic anchors and checking live HTTP status for every target URL, there are **three categories** of work:

1. **Broken chains** — pages that already have a redirect in the plugin, but the destination is itself a 404. These are the most urgent because they affect both backlinks and internal links.
2. **Missing redirects** — 404 pages with valid backlinks pointing to them. Need adding to Redirection.
3. **Excluded** — target URLs that are spam-only, have entirely off-topic backlinks, or already resolve correctly.

---

## Category 1: Fix Broken Chains (destination is 404)

These pages already have a redirect rule, but the redirect points to a dead URL. Add the destination URL as a new redirect or update the existing rule.

| Broken destination (add redirect for this) | Redirect to | Notes |
|---|---|---|
| `/liquidation-hub/` | `/liquidation/` | **Critical** — at least 5 pages chain into this including `/liquidation/advantages-disadvantages-liquidating-limited-company/`, `/liquidation/the-difference-between-solvent-and-insolvent-company-liquidation/`, `/liquidation/what-is-the-role-of-a-liquidator-in-company-liquidation/` |
| `/articles/common-causes-of-construction-insolvency/` | `/insolvency/` | Destination of `/news/common-causes-of-construction-insolvency/` which is destination of `/construction-industry-insolvency-trends/` |
| `/articles/88-year-old-retailer-bhs-goes-company-liquidation/` | `/liquidation/` | Destination of `/news/88-year-old-retailer-bhs-goes-company-liquidation/` (DR60+ source) |
| `/articles/covid-19-effects-on-cruise-industry/` | `/articles/` | Destination of `/features/covid-19-effects-on-cruise-industry/` (6 backlinks, DR50+) |
| `/articles/jamie-oliver-restaurant-restructure-london/` | `/articles/` | Destination of `/news/jamie-oliver-restaurant-restructure-london/` |
| `/articles/poolmageddon-79-of-uk-pools-may-close-within-6-months/` | `/articles/` | Destination of `/swimming-pool-closures-in-uk/` |
| `/advice/what-is-meant-by-a-zombie-company/` | `/insolvency/` | Destination of `/advice/what-legal-action-can-you-take-to-recover-a-bad-company-debt/` |
| `/hmrc/hmrc-office-locations-uk/` | `/hmrc/` | Destination of `/hmrc-tax-problems/hmrc-office-locations-uk/` (3 backlinks including DR50+). Also direct backlinks. |

---

## Category 2: Missing Redirects (404 pages, no existing redirect)

Ordered roughly by backlink value (DR / count).

### High value (DR 50+ backlinks or 3+ backlinks)

| Source URL (404) | Redirect to | Backlinks | Notes |
|---|---|---|---|
| `/articles/gieves-hawkes-facing-liquidation/` | `/liquidation/` | 3 (DR97 Wikipedia) | Wikipedia article on Savile Row tailoring cites this |
| `/articles/gieves-hawkes-facing-liquidation` | `/liquidation/` | 1 | Same article, no trailing slash variant |
| `/what-support-is-available-for-military-veterans-starting-a-business/` | `/` | 15 (3×DR50+) | Page redirected to external pen-and-sword.co.uk — that link is now dead too |
| `/how-is-your-business-going-to-be-affected-by-climate-change/` | `/articles/` | 10 (1×DR50+) | Infographic page; also links via `/articles/how-is-your-business-going-to-be-affected-by-climate-change/` |
| `/articles/how-is-your-business-going-to-be-affected-by-climate-change/` | `/articles/` | 1 | |
| `/how-to-increase-happiness-and-productivity-in-the-workplace/` | `/` | 3 (2×DR50+) | Generic business content — homepage best available |
| `/articles/will-the-energy-crisis-mean-the-end-for-britains-bakeries/` | `/articles/` | 3 (1×DR50+) | |
| `/features/airlines-brace-for-a-longer-and-deeper-crisis-in-2021/` | `/articles/` | 1 (DR70+) | |
| `/articles/bank-of-england-warns-of-sme-debt-vulnerablity/` | `/articles/` | 2 (1×DR50+) | |
| `/articles/late-invoice-payments-continue-big-problem-british-businesses/` | `/insolvency/` | 1 (DR60+) | Anchor: "23 per cent of all corporate insolvencies" |
| `/news/brexit-impact-on-smes-and-the-insolvency-regime/` | `/insolvency/` | 1 (DR60+) | |
| `/guides/7-top-tips-to-make-sure-you-survive-company-insolvency/` | `/insolvency/` | 1 (DR50+) | |
| `/guides/an-sme-s-guide-to-reducing-basic-business-expenditure-costs/` | `/company-cash-flow-problems/` | 1 (DR50+) | |
| `/company-rescue-solutions/advantages-disadvantages-administration` | `/company-administration/` | 1 (DR60+) | No-trailing-slash variant of a URL that already has a redirect with slash |
| `/faqs/what-is-insolvency` | `/insolvency/` | 1 (DR60+) | No-trailing-slash variant; `/faqs/what-is-insolvency/` already redirects to `/insolvency/` |
| `/what-can-bailiffs-seize-from-a-limited-company/` | `/winding-up-petitions/` | 2 (2×DR50+) | |
| `/how-to-save-money-with-social-media/` | `/` | 1 (DR50+) | Off-topic but high-DR site |
| `/support-for-military-veterans-starting-a-business-in-canada/` | `/` | 3 (1×DR50+) | Canada-specific, not relevant to UK insolvency — homepage only |

### Standard value (1 backlink, lower DR)

| Source URL (404) | Redirect to | Notes |
|---|---|---|
| `/articles/6000-fuel-hikes-taxi-sector/` | `/articles/` | Research-based article |
| `/articles/how-much-is-the-digital-sales-tax-going-to-affect-big-tech/` | `/articles/` | |
| `/articles/is-harley-davidson-heading-for-a-crash/` | `/articles/` | |
| `/articles/wayne-rooney-scores-21m-from-company-liquidation/` | `/liquidation/` | |
| `/guides/make-complaint-insolvency-practitioner-part-1/` | `/insolvency/what-is-an-insolvency-practitioner/` | |
| `/guides/rescue-guides/5-top-company-rescue-tips-for-struggling-businesses/` | `/insolvency/business-recovery-services/` | |
| `/hmrc/hmrcs-connect-computer-system/` | `/hmrc/` | |
| `/invoice-finance/` | `/company-cash-flow-problems/` | |
| `/liquidation/striking-off-dissolving-company/` | `/closing-a-limited-company/` | Closest relevant page |
| `/download-our-covid-19-business-survival-guide/` | `/bounce-back-loan-support-hub/` | Most relevant surviving COVID resource |

---

## Category 3: Excluded / Already Correct

| URL | Reason |
|---|---|
| `https://www.companydebt.com/` | Live 200, spam-heavy |
| `/about-us/` | 200 OK (the apparent loop resolves because about-us/ itself is live) |
| `/advice/are-directors-personally-liable-for-company-debts/` | 200 OK |
| `/articles/5-top-company-rescue-tips-for-struggling-businesses/` | 301 → `/articles/save-a-struggling-business/` ✓ |
| `/articles/covid-19-effects-on-cruise-industry/` | Need to add redirect (Category 1/2 above) |
| `/bounce-back-loan-support-hub/` | 200 OK |
| `/company-cash-flow-problems/` | 200 OK |
| `/company-rescue-solutions/company-voluntary-arrangement/` | 200 OK |
| `/construction-industry-insolvency-trends/` | 301 → `/news/common-causes-of-construction-insolvency/` → chain broken but fix in Category 1 above |
| `/insolvency/limited-company-bankruptcy/` | 200 OK |
| `/liquidation/` | 200 OK |
| `/what-is-a-pre-pack-administration/` | 200 OK |
| All http:// → https:// variants | Handled by server-level 301 already |
| Pure spam targets | Excluded — all backlinks marked `Is spam: true` |

---

## Import CSV for Redirection Plugin

Save as `redirects-import.csv` and import via Redirection > Import/Export.
