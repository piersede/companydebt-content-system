# Publicly readable server source on companydebt.com

**Found 25 August 2026. Staging is fixed. Live is not, and cannot be fixed from here.**

## What the fault is

WordPress only *executes* files ending in `.php`. A file named
`cd-livechat-secrets.php.bak-a11y-cdlc6` does not end in `.php`. It is never
executed. The web server treats it as an ordinary static file and returns the raw
PHP source to anyone who asks for the URL. No login. No password.

Our own SFTP edit helper made these. It saved a copy of every file it changed,
next to the original, once per edit, across many sessions since at least June
2026. Past file-system copies then carried them from staging to live.

## What was exposed

345 files under `wp-content` on staging, about 45 MB of theme and mu-plugin
source. Four of them held credentials, and the exposed values were checked
against the ones in use that day - they **matched**:

- Zoho CRM client ID
- Zoho CRM client secret
- Zoho CRM refresh token
- LiveChat secret

`robots.txt` does not disallow `wp-content`, so nothing stopped a crawler.

A refresh token does not expire on its own and is not tied to the website. It is
a standing key to the CRM records. It cannot move money.

## Why the existing pre-flight missed it

`audit_mu_plugins.py` asks "does this file execute and do damage" and skips
`.bak-*` on the grounds that they do not execute. That reasoning is correct and
the conclusion was still wrong: the risk was never execution, it was
readability. The audit now refuses to declare a copy safe until the readability
check passes too.

## What does NOT work

**An `.htaccess` deny rule.** Tried first, on staging, scoped to the mu-plugins
directory. The backup file kept returning 200 with its full source. WP Engine's
nginx serves static files without consulting Apache. Do not reach for this again.

## What does work

`_wpeprivate/` is the one directory WP Engine refuses to serve. Confirmed 403 on
both staging and live. Backups go there.

Both halves are now in place:

1. `scripts/sftp_edit.py` writes backups to `_wpeprivate/file-backups/<original
   path>.bak-a11y-<tag>` instead of next to the original.
2. `scripts/audit_exposed_files.py` fails if anything backup-shaped reappears
   inside the web root, or if a known backup path is still readable on the
   target. `audit_mu_plugins.py` calls it and will not say "safe to copy"
   without it.

## The recipe, if it recurs

```bash
python scripts/audit_exposed_files.py                # staging
python scripts/audit_exposed_files.py --target live  # live
```

To move offenders on staging, walk `wp-content` over SFTP and
`rename()` each match to `_wpeprivate/file-backups/<same path>`, creating parent
directories as you go. Move, never delete - the backups are the rollback path and
they are perfectly safe once they are out of the web root. Then re-run the
scanner and confirm the site still renders.

## Live - still open

Live is still serving these files. Our SFTP credentials reach **staging only**
(`comdebstage.sftp.wpengine.com`), so the same fix cannot be applied from here.

Two ways to close it:

1. **Production file access.** Create an SFTP user on the *production*
   environment in the WP Engine portal and add it to `.env`. The move then takes
   a couple of minutes and is verifiable with the scanner.
2. **Do it by hand** in whatever file access the portal offers.

**Do not assume a staging-to-live file copy will clean live.** It is not
established whether that copy removes destination files that no longer exist on
the source. If it only adds and overwrites, live keeps every exposed file while
the scanner passes on staging - the worst possible outcome, because it looks
fixed.

Rotating the exposed credentials is a separate decision and belongs to whoever
owns the Zoho and LiveChat accounts. Deleting the files does not un-publish
values that have already been readable for months.
