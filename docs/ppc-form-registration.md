# PPC form - follow-up registration checklist

The form "PPC - Request a Confidential Call" is created by
`python scripts/gf_create_ppc_form.py` (staging only). The script stores the new
form id in the WordPress option `cd_ppc_form_id` and prints it.

Nothing below can be done until that id is known. Until every step is complete
the form is only half wired up: it will collect entries, but the lead emails
arrive with empty merge tags and no Google Ads conversion is recorded.

Replace `<id>` with the real form id everywhere below.

## Checklist

1. **Register the id for notifications.**
   Add `<id>, // PPC - Request a Confidential Call` to the array in
   `cd_gfn_owned_form_ids()` in
   `theme-mu-plugins/cd-gform-notification-fix.php`.
   This is not optional. Gravity Forms notification merge tags arrive EMPTY
   site-wide unless the form is in that list, so the admin email would show the
   boilerplate with no name, no number and no email address. This is the single
   most likely way a new form ships silently broken.

2. **Register the id for spam hardening and field validation.**
   In `mu-plugins/cd-gform-hardening.php`, add `<id>` to:
   - `cd_gf_honeypot_forms()`
   - `cd_gf_email_fields()` as `<id> => array(4)`
   - `cd_gf_phone_fields()` as `<id> => array(3)`
   - `cd_gf_phone_blocking_forms()`
   Leave `cd_gf_optional_phone_fields()` alone: the telephone number is
   compulsory on this form. There is no free-text message field, so nothing goes
   in `cd_gf_message_fields()`.

3. **Add the Google Ads and GA4 conversion triggers. This step is manual.**
   There is no GTM API credential in this repo, so it has to be done in the GTM
   web interface.
   - Container: `GTM-5GTD9ZP`
   - New trigger, type **Element Visibility**
   - Selection method: CSS selector
   - Selector: `.gform_confirmation_message_<id>`
   - Fire on: once per page; observe DOM changes ON
   - Attach the trigger to the existing **Google Ads Form Submissions** tag
     (conversion ID `AW-977276330`, conversion label `knohCMOu9KUDEKqbgNID`)
   - Attach the same trigger to the existing **GA4 Form Submission** tag
   The script deliberately sets the form confirmation to type "message" rather
   than a redirect, because that is what puts the
   `.gform_confirmation_message_<id>` element on the page. If anyone later
   changes the confirmation to a redirect, the conversion stops recording.

4. **Publish and test.** Submit a real test entry on staging with a UK mobile
   number. Confirm three things: the entry stores, the admin email arrives with
   every merge tag filled in, and GTM Preview shows both tags firing.

## Two things to know before reading any conversion report

- **Google Ads credits a conversion to the landing page of the ad click, not to
  the page the form was submitted on.** If someone lands on an intent page,
  browses to another page and submits there, Ads still reports the conversion
  against the original landing page. That is why the hidden `intent` field
  exists: it is the only record of which intent page actually produced the lead.
  Do not try to reconcile the two by page URL. They will not agree, and Ads is
  not wrong.

- **Gravity Forms timestamps are UTC. Google Ads reports in London time.** From
  late March to late October the two are an hour apart. A lead submitted at
  00:30 London time appears in Gravity Forms on the previous day. Daily counts
  will not match, and the gap is largest at the start and end of a month.

---

## GTM conversion trigger — DONE AND LIVE (version 88, 2026-08-21)

Read directly out of the live container, from the existing
`gform_confirmation_message_40` trigger, so this copies a known-good pattern
rather than guessing.

**Container:** CompanyDebt Account > Company Debt Web > `GTM-5GTD9ZP`
**Google account: `jamesonsmithandco@gmail.com`** — this is the Company Debt
Google login. The `info@brighton-digital.com` account, which is the default
in Chrome, has NO Tag Manager access and shows an empty account list, which
reads as "the container is missing". It is not. Switch account.
Direct link (the `authuser=1` matters for the same reason):

    https://tagmanager.google.com/?authuser=1#/container/accounts/4702659864/containers/12748962/workspaces/1000086/triggers

**Create one trigger:**

| Setting | Value |
| --- | --- |
| Name | `gform_confirmation_message_47` |
| Trigger type | Element Visibility |
| Selection Method | CSS Selector |
| Element Selector | `.gform_confirmation_message_47` |
| When to fire this trigger | Once per page |
| Observe DOM changes | TICKED |
| This trigger fires on | All Visibility Events |

The **leading dot matters**. The stored value on trigger 40 is
`.gform_confirmation_message_40`, even though the trigger NAME has no dot.

**Then attach it to the two existing tags**, exactly as trigger 40 is
attached (open each tag, add the new trigger under Triggering):

  - `GA4 Form Submission`
  - `Google Ads - Form Submissions`

Do NOT create new tags. The Ads conversion ID (`AW-977276330`) and the
conversion label (`knohCMOu9KUDEKqbgNID`) already live on the existing tag;
duplicating it would double-count.

**Then Submit / publish the container version.**

### STATUS: built in the workspace, awaiting Submit

Done on 2026-08-21, all three changes saved in the workspace
(Workspace Changes: 3):

  1. Trigger `gform_confirmation_message_47` created, exactly as tabled above.
  2. Added to the `GA4 Form Submission` tag.
  3. Added to the `Google Ads - Form Submissions` tag.

Verified afterwards by reopening the trigger: it shows CSS Selector,
`.gform_confirmation_message_47`, Once per page, Observe DOM changes ticked,
All Visibility Events, and both tags listed under "References to this
Trigger". Structurally identical to trigger 40.

**PUBLISHED.** Piers submitted container version 88, "new CD PPC forms
build", on 2026-08-21. Confirmed Live/Latest. Its change list reads exactly:

    GA4 Form Submission            Tag       Modified
    gform_confirmation_message_47  Trigger   Added
    Google Ads - Form Submissions  Tag       Modified

Container is now 17 Tags / 13 Triggers / 5 Variables.

Nothing fires yet, because the selector matches nothing until the PPC pages
are live. The tracking is ready and waiting for them.

No new tags were created. The Ads conversion ID (`AW-977276330`) and label
(`knohCMOu9KUDEKqbgNID`) already sit on the existing tag, so there is no
double counting.

### Sanity check after publishing

The marker the trigger keys on is already present on the staging pages.
Confirm with:

    curl -s -u "$WP_BASIC_AUTH_USER:$WP_BASIC_AUTH_PASS" \
      https://comdebstage.wpengine.com/ppc-hmrc-debt/ | grep -c gform_confirmation_message_47

That returns 0 until a form is actually submitted (the class only appears on
the confirmation), so the real check is GTM Preview mode against a live
submission.
