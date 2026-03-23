# 21. WordPress Technical Build Quality System

A technical, evidence-led framework for assessing how well a WordPress site is engineered. Scored out of 100 across eight categories. The emphasis is on how the system is built and operated, not content, design taste, or marketing effectiveness.

## 21.1 Anchoring principles

1. WordPress engineering quality is inseparable from (a) convention and interoperability, because themes and plugins interact via hooks and shared APIs, and (b) secure-by-design handling of untrusted data, because sites are routinely exposed to adversarial inputs.
2. The highest-scoring sites are those where quality can be proved from artefacts: repository structure, configs, automated checks, logs, HTTP behaviour, and repeatable operational procedures.

## 21.2 Scope and assumptions

This rubric evaluates technical implementation: theme/plugin architecture, custom code, configuration, runtime behaviour, and operational readiness. It explicitly excludes content strategy, copywriting, brand/design judgement, SEO strategy, and editorial workflow except where they intersect technical correctness (accessibility semantics, performance budgets).

Assumptions (state in audit report if untrue):
- Access to at least one of: the codebase, WP Admin, the database, web server/CDN edge response, or WP-CLI.
- No constraints on size or traffic. "Excellent" means the build can scale and be maintained safely.
- Baseline runtime expectations align with modern supported stacks (current recommended PHP/database versions, HTTPS, disciplined upgrade posture).

## 21.3 Scoring rubric

| Category | Points | What "good" measures |
|---|---|---|
| WordPress architecture and conventions | 15 | Uses WordPress' extension model cleanly: hooks, templates, theme.json, sane separation of concerns |
| Code quality and maintainability | 15 | Readable, consistent, documented code with low coupling and enforceable standards |
| Security and data handling | 20 | Systematically defends against common web risks: access control, injection, CSRF/XSS, secure config |
| Performance and scalability | 15 | Efficient DB + caching strategy, disciplined asset loading, predictable background work |
| Compatibility and upgrade resilience | 10 | Survives core/PHP/plugin updates with minimal breakage risk; avoids fragile coupling |
| Observability and operational robustness | 10 | Failures are visible, diagnosable, and recoverable; health checks exist |
| Accessibility and front-end correctness | 5 | WCAG-aligned semantic implementation, validated HTML, sensible ARIA usage |
| Development workflow and deployment hygiene | 10 | Repeatable builds, supply chain controls, CI gates, safe releases |

## 21.4 Score bands

Use two layers of interpretation: overall band and per-category bands.

**Overall site score:**
- **Excellent (85-100):** Engineered for long-term change. Strong defaults. Few high-risk unknowns.
- **Acceptable (60-84):** Works reliably today but has identifiable tech debt or operational gaps that will surface under change, scale, or security pressure.
- **Poor (<60):** High likelihood of regressions, security issues, or operational fragility. Hard to evolve safely.

**Per-category bands:** Treat each category as "excellent" at 85%+ of available points, "acceptable" at 60-84%, and "poor" at <60%. This prevents a site masking a security failure with nice architecture.

## 21.5 Evidence collection playbook

Start with high-signal artefacts: versions, update status, config, integrity checks, and the biggest performance hotspots (autoload/options, cron, caches).

### WP-CLI evidence bundle

```
wp cli info
wp core version --extra
wp core check-update
wp plugin list
wp plugin list --status=must-use
wp plugin list --status=dropin
wp core verify-checksums
wp plugin verify-checksums --all
wp config list
wp option list --autoload=on --format=total_bytes
wp option list --autoload=on --fields=option_name,size_bytes --orderby=size_bytes --order=desc | head
wp option list --search="*_transient_*" --fields=option_name,size_bytes --orderby=size_bytes --order=desc | head
wp cron test
wp cron event list
```

### HTTP-level evidence bundle

```
curl -I https://example.com/
curl -I https://example.com/wp-json/
curl -I https://example.com/some-page/
```

Interpret caching behaviour using HTTP semantics (Cache-Control, Age, Vary). Use security headers as defence-in-depth per OWASP guidance.

### Database evidence bundle

Use when you have DB access (read-only is fine). Goal: find oversized autoload options, unbounded growth, and slow query patterns.

```sql
-- Largest autoloaded options
SELECT option_name, LENGTH(option_value) AS bytes
FROM wp_options
WHERE autoload IN ('yes','on')
ORDER BY bytes DESC LIMIT 25;

-- Transient footprint
SELECT option_name, LENGTH(option_value) AS bytes
FROM wp_options
WHERE option_name LIKE '\_transient\_%'
ORDER BY bytes DESC LIMIT 25;
```

## 21.6 Category: WordPress architecture and conventions (15 points)

Measures whether the site is built as WordPress expects: hooks over core edits, predictable template hierarchy, modern theme configuration.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| Separation of responsibilities | 4 | Theme handles presentation; business logic in plugins/mu-plugins; minimal coupling | Business logic embedded across templates; hard to deactivate/replace | `wp-content/` structure, plugin file organisation |
| Hook-driven integration | 3 | Actions/filters used correctly; callbacks are isolated; no side effects in filters | Direct output/DB writes inside filters; fragile coupling | `add_action`/`add_filter` usage; global state mutation |
| Theme templating correctness | 4 | Uses template hierarchy intentionally; block templates in correct locations; respects child theme overrides | Random template selection; duplicated logic; bypasses hierarchy | Template files, hierarchy logic |
| theme.json and global styles | 2 | theme.json present with correct schema/versioning; global styles done through the system | No coherent global system; scattered CSS overrides | `theme.json`, schema URL, version |
| API surface design | 2 | Custom REST routes namespaced and versioned; permission callbacks used | Unnamespaced routes; missing permission callbacks; side effects in GET endpoints | `register_rest_route`, `permission_callback`, namespaces |

**Smell signals:** Plugin naming collisions, global namespace pollution, unclear folder structure, direct file access risks.

## 21.7 Category: Code quality and maintainability (15 points)

Measures whether code is built to be read, reviewed, and changed safely.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| Standards adherence | 5 | Enforced via automated tooling (WordPressCS + PHPCS); HTML validator-clean | Inconsistent style; invalid markup ignored | `phpcs.xml`, CI config, lint scripts |
| Naming and collision avoidance | 3 | Unique prefixes/namespaces; avoids forbidden globals | Generic function/class names; collisions likely | Global functions/classes, plugin main file |
| Documentation quality | 3 | File headers and public APIs documented; functions/classes/hooks covered | No docblocks; intent unclear; review cost high | Docblocks for public APIs |
| Change safety | 2 | Filters are pure; actions do bounded work; minimal reliance on globals | Hidden side effects and global mutation; brittle ordering | Hook implementations |
| Tooling present and usable | 2 | WordPress standards toolchain (WordPressCS + PHPCS) installable and used in CI | No linting/static checks; regressions shipped | Composer dev deps, CI steps |

## 21.8 Category: Security and data handling (20 points)

Weighted highest because the most expensive WordPress failures are typically security and integrity failures.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| Validation and sanitisation (inputs) | 5 | Clear trust boundaries; validates early with safelists; sanitises with WordPress APIs | Raw `$_GET`/`$_POST` flows into queries/output | Superglobals usage, REST validate/sanitize callbacks |
| Escaping (outputs) | 5 | Escapes late, contextually (HTML, attributes, URLs); avoids double escaping | Unescaped output; XSS risk is structural | Template scans for `echo` + variable; escaping helper usage |
| Authorisation (capabilities) | 4 | Every privileged action gated with capability checks; REST endpoints use `permission_callback` | Privileged actions reachable by unauthorised users | `current_user_can` usage, REST `permission_callback` |
| CSRF protection | 3 | Nonces used for state-changing requests; pairs nonces with capability checks | No CSRF defences on logged-in actions | Admin-post/admin-ajax handlers, forms, REST auth |
| SQL safety | 2 | Uses `$wpdb->prepare()` with correct placeholders; no string concatenation with untrusted values | Dynamic SQL via concatenation with user input | `$wpdb->prepare`, raw `$wpdb->query`, concatenated SQL |
| Secure configuration posture | 1 | Production: debug off, environment type explicit, file mods disabled, logs not publicly exposed | Debug/display on in production; editable files in admin | `wp config list`, constants |

**Best-practice pattern:**
```php
// Validate and sanitise input early
$sort = isset($_POST['sort']) ? sanitize_key($_POST['sort']) : 'date';
$allowed = array('date', 'title');
if (!in_array($sort, $allowed, true)) { wp_die('Invalid sort.'); }

// Escape output late, in the correct context
echo '<a href="' . esc_url($url) . '">' . esc_html($label) . '</a>';
```

## 21.9 Category: Performance and scalability (15 points)

Mostly about avoiding unnecessary database work, using caching intentionally, and keeping asset loading disciplined.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| Caching strategy (object cache + transients) | 6 | Uses object cache APIs appropriately; transients for expirable data; persistent cache present when needed | No caching; repeated expensive queries each request | Drop-ins (`object-cache.php`), transient usage, caching groups |
| Autoload and option hygiene | 4 | Autoload kept small; plugin options not autoloaded when inactive; large blobs avoided | Massive autoload; slow TTFB baseline | `wp option list --autoload=on --format=total_bytes`, DB queries |
| Database query discipline | 3 | Uses `$wpdb->prepare`; avoids N+1 queries; caches query results when appropriate | Unbounded queries; concatenated SQL; same query repeated per request | Query logging, hotspot review |
| Asset loading discipline | 2 | Enqueues on proper hooks; per-block styles; avoids loading editor assets on front end | Hard-coded `<script>`/`<link>` tags; assets loaded everywhere | `wp_enqueue_scripts`, `enqueue_block_assets` |

**Key insight:** Transients that never expire become autoloaded, while expiring transients are not autoloaded. "Cache forever" can quietly bloat autoload and slow every request.

## 21.10 Category: Compatibility and upgrade resilience (10 points)

Whether the build can survive core updates, PHP version moves, plugin updates, and editor evolution.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| Runtime version alignment | 4 | Runs on recommended modern versions; avoids EOL runtimes; upgrade path documented | EOL runtimes; upgrade likely to break site | `wp core version --extra`, PHP version, support matrix |
| Update readiness | 3 | Regular update checks; uses background update signals; avoids code hacks that block updates | Updates avoided; failed updates common | `wp core check-update`, Site Health, checksum checks |
| Block/theme evolution resilience | 2 | Uses current editor schema version; understands editor iframe and API shifts | Hard-coded assumptions; breaks with editor updates | `theme.json` version + schema, editor enqueue approach |
| Dependency/supply-chain posture | 1 | Dependencies pinned/verified; aware of supply chain failures as first-class risk | Unreviewed third-party code shipped; no integrity checks | Composer/npm lockfiles, CI artefact integrity checks |

## 21.11 Category: Observability and operational robustness (10 points)

Whether real failures become visible quickly and can be diagnosed without heroics.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| Debug configuration by environment | 4 | Uses environment typing; debug configured safely; production does not display errors; logs protected | Debug output visible publicly; environment leakage risk | `wp config list`, `WP_ENVIRONMENT_TYPE`, `WP_DEBUG`, logging paths |
| Health checks and diagnostic endpoints | 3 | Uses Site Health tests (HTTPS, loopback, background updates); results inspectable via REST | No health signal; failures discovered by users | Site Health REST endpoints, admin Site Health |
| Cron reliability and diagnosability | 2 | Cron spawning tested regularly; scheduled events visible; critical work not reliant on page-load timing | Cron failures unnoticed; scheduled tasks drift badly | `wp cron test`, `wp cron event list` |
| Operational hardening controls | 1 | Admin file modifications disabled where appropriate; access boundaries clear | Live editing/installs in production as default | `DISALLOW_FILE_MODS`, admin policies |

**WordPress-specific reality:** WP-Cron is triggered by page loads, not running continuously. This makes drift and "works on busy sites only" a predictable failure mode unless managed.

## 21.12 Category: Accessibility and front-end correctness (5 points)

Technical accessibility and correctness, not design taste.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| WCAG-aligned implementation discipline | 3 | Engineering choices align with WCAG 2.2 A/AA and WordPress accessibility standards; ARIA used purposefully | Systemic barriers; ARIA misuse; keyboard traps | Automated checks + manual keyboard/screen-reader spot tests |
| Markup correctness | 2 | HTML validates; semantics consistent; validator used as automation aid | Invalid markup widespread; brittle rendering/AT support | Validate key templates (home, archive, single, forms) |

## 21.13 Category: Development workflow and deployment hygiene (10 points)

Whether engineering practices prevent avoidable incidents.

| Sub-criterion | Points | Excellent | Poor | Evidence |
|---|---|---|---|---|
| Quality gates in CI | 4 | Automated linting + standards checks on every change; failures block merges; outputs reproducible | No CI gates; quality is manual and inconsistent | CI config, phpcs runs, build scripts |
| Dependency and artefact integrity | 3 | Lockfiles present; checksum verification for deployed core/plugins | "Latest" dependencies; no integrity checks; risky third-party drift | Lockfiles, release process, checksum checks |
| Environment/config management | 2 | Config values auditable via CLI; environment type defined; secrets not committed | Manual "clickops" drift; secrets in repo; production edits | `wp config list`, repo scanning |
| Release safety | 1 | Staging-first; rollback strategy; health checks after deploy | Direct-to-prod changes; failures discovered late | Deployment docs, post-deploy checks |

## 21.14 Minimal reviewer checklist

Use as a quick sanity pass before going deep.

| Area | Quick pass question | Fast evidence |
|---|---|---|
| Versions | Is core on a supported version and PHP modern? | `wp core version --extra` |
| Integrity | Do core and plugins match official checksums? | `wp core verify-checksums`, `wp plugin verify-checksums --all` |
| Config hygiene | Is prod debug off and environment type set? | `wp config list` |
| Security posture | Are validation/escaping/nonces/capabilities consistently applied? | Code review: handlers, REST routes, templates |
| Performance basics | Is autoload under control; is caching intentional? | `wp option list --autoload=on --format=total_bytes` |
| Cron | Is cron spawning healthy? | `wp cron test` |
| Front-end correctness | Is HTML reasonably valid; accessibility discipline present? | Validate key templates; spot-check ARIA usage |
| Workflow | Are standards checks automated and blocking? | CI config + phpcs/WordPressCS evidence |

## 21.15 Audit report structure

When producing an audit report, follow this structure:

1. **Executive summary.** Overall score, band, and the two or three most important findings.
2. **Assumptions stated.** Which access levels were available; which were not.
3. **Per-category scoring.** Score each category with evidence citations.
4. **Priority findings.** Ranked by risk, not by category order. Security and performance issues surface first.
5. **Recommendations.** Specific, actionable items with expected effort and impact.
