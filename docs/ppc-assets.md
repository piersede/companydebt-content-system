# PPC landing page: image assets

Active theme on the site: `company-debt-webpigment`
(confirmed from the root-relative theme paths in `drafts/79845_data.html`).

Staged locally at:
`theme/assets/ppc/`

Source bundle:
`C:/Users/piers/AppData/Local/Temp/claude/cdhub/design_handoff_companydebt_ppc/assets/`

Nothing has been uploaded. This document only stages the files and records the
commands.

## Assets in use

| Asset | Pixel size | File size | Where it is used | URL for the template |
|---|---|---|---|---|
| `chris-andersen.webp` | 150 x 150 | 21.7 KB | Hero practitioner row, the reassurance block, and the practitioner block. Used three times. | `/wp-content/themes/company-debt-webpigment/assets/ppc/chris-andersen.webp` |
| `nicki-meadows.jpg` | 150 x 150 | 2.7 KB | Second practitioner photo in the practitioner block | `/wp-content/themes/company-debt-webpigment/assets/ppc/nicki-meadows.jpg` |
| `ipa.png` | 95 x 32 | 6.8 KB | Trust bar, links to the IPA register | `/wp-content/themes/company-debt-webpigment/assets/ppc/ipa.png` |
| `icaew.png` | 360 x 180 | 14.5 KB | Trust bar, links to the ICAEW register | `/wp-content/themes/company-debt-webpigment/assets/ppc/icaew.png` |
| `reviewsio.png` | 900 x 500 | 4.8 KB | Reviews rating line, next to the star score | `/wp-content/themes/company-debt-webpigment/assets/ppc/reviewsio.png` |

Set `width` and `height` on every image tag from the pixel sizes above, so the
page does not jump while it loads. Two of the files are much larger than the
box they are drawn in, so the drawn size and the file size are not the same
thing:

- `icaew.png` is 360 x 180 but the design draws it at 60px wide. Give the tag
  the real 360 x 180 and let the stylesheet size it, or resave the file at
  double the drawn size (120 x 60).
- `reviewsio.png` is 900 x 500 but the design draws it at 36 x 20. This is a
  very oversized source for a tiny mark. Resave it smaller before launch.

## Files deliberately left out

| Asset | Why it is excluded |
|---|---|
| `icas.png` | The footer "Members of ICAS" line is being removed from the build as an unverified claim, so the logo is not needed. |
| `tma.png` | TMA branding was removed on compliance advice. It must not come back. |
| `bbc.svg`, `guardian.svg`, `telegraph.svg`, `financial-times.svg`, `daily-express.png` | Press mastheads kept from an earlier version of the design. No visible section uses them. |
| `chris-andersen.jpg` | Older format of the same photo. The page uses the `.webp` version. |
| `company-debt-team.png`, `laptop-mockup.png`, `laptop-mockup-cropped.png` | Not referenced anywhere on the page. Also very heavy: 2.0 MB, 2.0 MB and 0.7 MB. |
| `logo-companies-house*.{png,jpg}`, `logo-dbt-trim.png`, `logo-gazette*.png`, `logo-insolvency-service*.png`, `logo-ons.svg` | Data-source logos from the data hub work. Not used on this page. |

## Weight check

No staged file is over 200 KB. The largest is `chris-andersen.webp` at 21.7 KB,
and all five together come to 50.5 KB. Nothing is blocked on compression.

The heavy files in the bundle (the two laptop mockups and the team photo, each
0.7 MB to 2.0 MB) are all in the excluded list. If any of them is added later,
compress it first. This page is paid traffic and every extra second costs
money.

## Upload commands (staging only)

Run these from the repo root. Paths are relative to the site root on the
server. Each upload makes a backup on the server first.

```
python scripts/sftp_edit.py put theme/assets/ppc/chris-andersen.webp wp-content/themes/company-debt-webpigment/assets/ppc/chris-andersen.webp --tag ppc
python scripts/sftp_edit.py put theme/assets/ppc/nicki-meadows.jpg wp-content/themes/company-debt-webpigment/assets/ppc/nicki-meadows.jpg --tag ppc
python scripts/sftp_edit.py put theme/assets/ppc/ipa.png wp-content/themes/company-debt-webpigment/assets/ppc/ipa.png --tag ppc
python scripts/sftp_edit.py put theme/assets/ppc/icaew.png wp-content/themes/company-debt-webpigment/assets/ppc/icaew.png --tag ppc
python scripts/sftp_edit.py put theme/assets/ppc/reviewsio.png wp-content/themes/company-debt-webpigment/assets/ppc/reviewsio.png --tag ppc
```

Confirm the folder exists on the server before the first upload:

```
python scripts/sftp_edit.py list wp-content/themes/company-debt-webpigment/assets
```

## Getting these files onto the live site

This upload route reaches staging only. It cannot target live.

To put the files on live, use a WP Engine **file system only** copy from
staging to production. Before that copy runs, read
`docs/staging-to-live-push.md` and clear the throwaway scripts found by
`python scripts/audit_mu_plugins.py`. The copy takes every file, not just
these five. After the copy, purge Cloudflare as well as the WP Engine and
WP Rocket caches, then load the page and check each image really appears.
