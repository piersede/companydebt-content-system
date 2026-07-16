# Ahrefs site audit: how to triage it

Last verified: 2026-07-16, against the 15-Jul-2026 "all issues" export
(project 1527982, health score 64, 679 pages crawled).

Read this **before** fixing anything Ahrefs reports. Roughly **83% of the link
errors in that export cannot be fixed by changing the site**, and two previous
remediation passes were spent on defects that were never the cause.

---

## 1. Most "broken links" are not broken

**1,299 of ~1,570 link errors are false positives.**

legislation.gov.uk and several other official hosts serve **200 to a browser
and 404/403 to a bot**. Ahrefs' crawler gets the door slammed on it and records
"broken link". Real readers, and Googlebot, get the page.

Proof (re-runnable):

```bash
python scripts/ahrefs_audit/verify_external.py <export-dir> <out.json>
```

It fetches every flagged external URL twice, once with a browser UA and once
with a bot UA, and classifies:

| Verdict | Meaning | Action |
|---|---|---|
| `FALSE_POSITIVE_BOT_BLOCK` | 200 to browser, 4xx to bot | **Leave alone.** Exclude host in Ahrefs. |
| `GENUINELY_DEAD` | 4xx to both | Real. Needs a new URL. |
| `MOVED` | Redirects | Update the citation to the final URL. |
| `OK_NOW` | 200 to both | Stale Ahrefs data. |

2026-07-16 result: **269 false positive, 10 genuinely dead, 1 OK now.**

### Do not "fix" these by deleting citations

The only way to clear these from the report is to remove the links. On an
insolvency firm's site those links are citations to the Insolvency Act, the
Companies Act and HMRC guidance. Deleting them to make a dashboard go green
trades the site's strongest expertise signal for a cosmetic number.

**The correct fix is an Ahrefs setting**, not a code change: exclude these
hosts from crawling (Site Audit -> crawl settings). Verified bot-blocking hosts
are listed in `scripts/ahrefs_audit/citation_fixes.py` (`BOT_BLOCKING_HOSTS`).

---

## 2. Parse the export properly or the numbers lie

Exports are **UTF-16-LE, tab-separated, fully quoted, with embedded newlines**
inside quoted fields (redirect chains especially). A line-based read silently
truncates rows and inflates counts:

| Issue | `wc -l` says | Real |
|---|---|---|
| Page has redirected image | 14,314 | **410** |
| Structured data error | 3,062 | **375** |
| Links to broken page | 1,900 | **242** |

Always go through `scripts/ahrefs_audit/parse_export.py`.

---

## 3. A number that recurs across issues is a template, not content

`410 inlinks` appeared on several unrelated issues. 410 is roughly the page
count: anything reporting it is in a **sitewide element**, not in articles.

In July 2026, ~820 "links to redirect" warnings came from **two hrefs** in two
footer **block widgets** (`block-38`, `block-39`). They are invisible to both
`grep theme/` and the menus API, because:

- the repo `theme/` is a **stale mirror** (1,139 lines vs 1,420 on staging) -
  editing it changes nothing;
- block widgets live in the DB, reachable at `/wp-json/wp/v2/widgets`.

Tools: `fix_widget_links.py`, `fix_menu_links.py` (both dry-run by default).

---

## 4. Don't guess at structured-data errors

Ahrefs reports `Schema.org validation error` with **no detail**, on 375 pages.
That silence has now caused two wrong fixes:

- **2026-07-02** (`functions.php`): patched `dateModified` timezone format and
  an empty `FinancialService image:[]`. Both patches worked. The error count
  did not move (375 before, 375 after, `change: +1`). Neither was the cause.
- **2026-07-16**: inspected the emitted graph and found the real defect -
  Schema Pro emitting blank settings as invalid values:

  ```json
  "addressRegion": null,
  "openingHoursSpecification": [{"dayOfWeek": [""], "opens": "", "closes": ""}],
  "geo": {"latitude": "", "longitude": ""}
  ```

  `dayOfWeek` is a DayOfWeek **enumeration**; `""` is not a member, so the graph
  fails validation on every page rendering the node - i.e. all of them.

Fix applied: a recursive strip of null/empty values in the JSON-LD
post-processor (an omitted optional property is valid; an empty one is not).
See `patches/functions-php-schema-strip-20260716.patch`.

**Better fix, when the data exists:** put the real opening hours and geo
coordinates into Schema Pro's settings. Do not invent them.

Inspect the graph with:

```bash
python scripts/ahrefs_audit/check_schema.py "/hmrc/cant-pay-vat/" --dump
```

---

## 5. Ahrefs only finds citations that 404

This is the important limit. In July 2026 the audit surfaced 8 citations to
documents that **do not exist** (see §6). It found them only because their URLs
happened to 404.

A fabricated citation whose URL happens to resolve is **invisible to every
crawler**. Ahrefs is not a citation-integrity check, and a clean report is not
evidence that the citations are real.

---

## 6. Fabricated citations found 2026-07-16

All were "Sources & References" entries: real-sounding document names, real-
sounding URLs, confident descriptive glosses, no such document.

| Cited as | Reality |
|---|---|
| Finance Act 2020, **Schedule 28** (7 pages) | No such schedule. The provision is **s.98** (amends IA 1986 s.386, inserts Category 9 into Sch 6). Claim correct, citation invented. |
| HMRC **CC/FS40** | Series runs CC/FS39, CC/FS41. No such factsheet. Removed, not substituted. |
| HMRC **Security Deposits Manual** | Real manual is **Securities Guidance**. |

Corrected via `apply_citation_fixes.py`; verified with `verify_fixes.py`
(22 checks / 0 failures).

Note the near-miss: a subagent reported the Schedule 28 issue as "wrong Act,
should be CIGA 2020". That was **wrong**. `ukpga/2020/14` is the Finance Act
2020 and citing it is correct - s.98 is Crown preference. Re-pointing to CIGA
would have replaced a bad citation with a different bad citation. Verify
research findings against the source before acting on them.

---

## 7. "Fixed locally" != "fixed"

Three distinct states, routinely conflated:

1. draft fixed, staging fixed -> done
2. draft fixed, **staging never had the content** -> not a failure; needs a
   redeploy through the normal pipeline
3. old string still on staging -> a real failure

`verify_fixes.py` reports (2) as `GAP` and only (3) as `FAIL`. Treating (2) as
success is how the previous internal-link pass reported ~25 fixes that had no
effect on the live site.

Also note the theme lives on **staging** (`sftp_edit.py`), the content lives in
**WP** (`staging_edit.py`), and the repo holds **drafts**. A fix in the wrong
one of those three is a no-op.

---

## 8. Known-not-fixed

- **Redirected images** (410 pages): 10 images 302 to `?fresh`. **Staging does
  not reproduce it** - all 10 return `200 image/png`. Nothing in the theme,
  mu-plugins, `.htaccess` or qppr generates it. Live-only infrastructure
  behaviour; needs a read-only live check to diagnose.
- **Two redirect chains**: `liquidate-registered-charity -> liquidation-hub ->
  liquidation`, and `faqs/what-is-wrongful-trading -> what-is-wrongful-trading
  -> insolvency/what-is-wrongful-trading`. Need qppr rule edits; qppr is a known
  silent-failure area and no content links to them any more.
- **Noindex/testimonial/author pages** (~160): by design.

---

## Gotchas

- **Git Bash mangles leading-slash arguments.** `--old "/business-debt-advice/"`
  became `C:/Program Files/Git/business-debt-advice/` and reported a confident
  `matches=0`. Prefix commands with `MSYS_NO_PATHCONV=1`.
- `staging_edit.py show` truncates at 4,000 chars; Sources blocks sit past it.
  Use `dump_staging.py`.
- No PHP CLI on this machine. Before pushing `functions.php`, check structure
  with the balance checker and test the algorithm in Python. `sftp_edit.py put`
  always writes a `.bak-a11y-<tag>` first - that is the rollback.
