# The cookie banner is switching off all measurement, not just the cookies

**Date:** 2 September 2026
**Status:** DONE and verified on live, 2 September 2026, 18:05.
**Who needs to agree:** Piers, and whoever owns cookie compliance.

---

## In one paragraph

The cookie banner is doing more than it should. As well as holding back cookies,
it stops the Google tag manager from loading at all. So a visitor who has not
clicked Accept is completely invisible: no page view, no chat, no enquiry, not
even the anonymous signal Google uses to estimate the visitors it cannot see.
The fix is one setting inside the cookie-banner account. It needs no website
code change and no tag-manager release. After the change the tag manager loads
for everyone, cookies still wait for consent, and Google can estimate the gap.

---

## What was happening, proven not assumed

*(This section records the fault as found. It is fixed - see the result at the
bottom.)*

Tested on the live site on 2 September 2026, on
`https://www.companydebt.com/ppc-liquidate-company/`, in a browser with the
consent decision cleared, without touching the banner.

- The tag manager is absent. Nothing from Google loads at all.
- The denied-by-default consent settings we added in July do run, correctly, and
  before everything else. That part of the site is right.
- The banner then runs and immediately writes its own record saying "no consent
  yet".
- Click Accept and everything appears at once: the tag manager, the Google Ads
  tag, the Analytics tag, and the cookies.

So the site is not mis-tagged. The pages are correct. One product is switching
the measurement off.

### The exact cause

The banner product carries a second, separate feature from the consent settings:
a block-list of web addresses it refuses to let load. That list is held in the
banner account, not in our code. Before the change it contained, word for word:

```
youtube.com
google-analytics.com|googletagmanager.com/gtag/js
googletagmanager.com
doubleclick.net
```

Everything Google serves comes from those addresses, including the tag manager
itself. So the banner blocks the container, and the container is the thing that
would have carried the consent signal onward. The tool is holding the door shut
on the mechanism designed to keep the door shut properly.

This is not a duplicate-banner problem. Checked on live the same day: there is
one banner account on the page, one banner, and the tag manager is not adding a
second one. Nothing needs releasing in the tag manager.

---

## What the fix is

**In the cookie-banner account: Advanced Settings, Google consent mode.**

1. `Support GCM` - leave ON. It is already working; the banner already sends the
   consent decision.
2. `Allow Google tags to fire before consent` - turn **ON**. This was the setting
   that was off. It takes the Google addresses out of the block-list above.

That is the whole change. No file goes to the website. No tag-manager release.
The banner keeps working exactly as it does now for the visitor.

Because staging and live share one banner account, the change lands on both at
the same moment. It is also reversible in seconds by turning the same setting
back off.

---

## Why this is safe, and the compliance point

**The requirement is that the tag manager loads while the cookies do not.** That
is the arrangement Google calls Consent Mode, and it is what the July work put
in place. The site already tells Google, before anything else runs, to deny
advertising storage, advertising user data, advertising personalisation and
analytics storage until told otherwise. The banner then switches them on if the
visitor accepts. Blocking the tag manager on top of that adds no protection. It
only removes the ability to count.

**This was tested, not reasoned.** On the live page on 2 September, with the
visitor decision cleared and the banner untouched, the Google addresses were
taken out of the block-list in the browser only, and the tag manager was then
allowed to load. Result:

| Check | Result |
|---|---|
| Tag manager loaded | yes |
| Google Ads tag and Analytics tag loaded | yes, both |
| Advertising storage | denied |
| Advertising user data | denied |
| Advertising personalisation | denied |
| Analytics storage | denied |
| Advertising or analytics cookies written | **none** |

Then Accept was clicked. All seven consent signals switched to granted, and the
three cookies appeared (`_gcl_au`, `_ga`, `_ga_P39KJ34V6G`) - and only then.

So the end state is: everyone is counted, nobody is tracked before they agree.
Nothing is set on a visitor's machine ahead of their decision.

**What a visitor who declines will send.** They send an anonymous signal with no
cookie and no identifier. Google uses it to estimate the conversions it cannot
see. This is documented, standard behaviour and it is the reason the arrangement
exists. It is worth stating plainly to whoever signs this off, because it is the
one behaviour that changes: today a declining visitor sends nothing at all;
after the change they send a cookieless signal.

**Settled: the "assumed rather than explicitly set" worry was a false alarm.**
Google keeps an `implicit` flag against each permission, and it reads true even
on a perfectly working page. It is not the danger signal. The flags that do catch
a missing or late default are `usedDefault` (reads true) and `wasSetLate` (reads
false), and both are correct on live. The July audit read `implicit` as proof the
default was missing; that was right at the time only because `usedDefault` was
false as well. The mu-plugin comment has been corrected so nobody chases this
again.

---

## How to check it afterwards

Run this and expect five out of five. It reads the live pages and the banner
account, and it names this exact fault if it comes back.

```bash
python scripts/check_consent_tag_order.py --target live --path /ppc-liquidate-company/
```

It reported one out of five while the fault was live, and the failing line named
the setting to change. Before this session it reported four out of four and
passed, because it only looked at the pages. The pages were never the problem.
That blind spot is now closed.

**Two caches sit between the setting and the visitor, and both must be cleared by
hand after any change to this setting.** WP Rocket keeps a compressed copy of the
banner script on our own server, and Cloudflare then holds that copy with a
one-year expiry. Until both were cleared, live still served the old block-list
while the banner account was already correct. Clear WP Rocket first, Cloudflare
second.

Then, by hand, in a browser with no stored decision, without touching the
banner:

1. The tag manager should be present.
2. There should be no advertising or analytics cookies.
3. The four advertising and analytics signals should read denied. Check
   `usedDefault` is true and `wasSetLate` is false. Ignore `implicit` - see above.
4. Click Accept. The signals should switch to granted and the cookies appear.
5. Start a live chat and confirm the chat event is recorded. Chat is the action
   this fault hurts most, so it is the one to watch.

---

## What it has been costing

The live-chat numbers are the clearest evidence. Chat enquiries recorded per
month ran 23, 20, 17, 11, 20, then fell to 3, 3, 4, 4. Chat is the fastest thing
a visitor does, usually before they have dealt with the banner, so chat is where
the loss shows up first and worst. Roughly one chat in five is currently being
recorded. Form enquiries look healthier only because a form takes a minute to
fill in, by which time the banner has been dealt with.

**The exact share of visitors who accept still cannot be measured from here, and
is still worth getting.**
This is not new: the July audit reached the same wall. There are no banner-account
credentials in the project, and the analytics access this project holds points at
businessexpert.co.uk, not companydebt.com. Two ways to get the number:

- **Direct, and best:** the banner account's own consent report. The July audit
  established that this is included on the free plan.
- **Estimate:** Google recorded 774 visits from its search results between 1 and
  30 August. Analytics currently only records people who accepted. Divide the
  August analytics visits from Google search by 774 and that is the accept share,
  as a lower bound.

Worth doing either way. It turns "we are losing enquiries" into a number, and it
gives a before-and-after for this change.

---

## Recommendation

Turn the setting on. It is one switch, it is reversible in seconds, it needs no
release, and the end state is the standard arrangement rather than a workaround.
Do it before the paused Liquidation search campaign starts, because that campaign
gets one learning period and it will learn from whatever it can measure.

Get the compliance owner to read the safety section above first. The change makes
the site behave more conventionally, not less, but it does alter what a declining
visitor sends, and that is their call to make rather than ours to assume.

---

## Not in scope, noted so it is not lost

Phone-call enquiries recorded fell from 47 in June to 27 in July to 12 in August
and none so far in September. Call tracking was rebuilt in late July and it did
not help. This fault would depress those numbers too, so the change here may
improve them - but it is unlikely to be the whole story, and it needs looking at
separately.

---

## RESULT - verified on live, 2 September 2026

Piers turned the setting on at 16:53. WP Rocket and Cloudflare were cleared, which
was needed: our own server was still handing out a compressed copy of the banner
script made on 1 September, carrying the old block-list, and Cloudflare was holding
that copy with a one-year expiry.

`check_consent_tag_order.py --target live` now reads **5 of 5** on
`/ppc-liquidate-company/`, `/`, `/contact-us/` and `/liquidation/`.

Measured in a browser on the live paid landing page, with no stored choice and no
interaction:

| Check | Result |
|---|---|
| Tag manager loaded | yes |
| Google Ads tag and Analytics tag loaded | yes, both |
| All four advertising and analytics permissions | denied |
| Advertising or analytics cookies written | **none** |
| Anonymous signal sent to Google | **yes** - `gcs=G100`, `npa=1` |
| Banner shown | yes |

The anonymous signal was the last unknown and it is confirmed. Three requests
carried it: the Analytics one to `region1.google-analytics.com/g/collect`, and two
to `pagead2.googlesyndication.com/ccm/collect`, one for the container and one for
the Ads account. So Google can now estimate the visitors it cannot see.

Then Accept was clicked. All seven permissions switched to granted, the signal
changed to `gcs=G111`, and `_gcl_au`, `_ga` and `_ga_P39KJ34V6G` appeared. Only
then.

**`doubleclick.net` staying blocked is confirmed harmless.** Nothing needed it.
Every Google request on the page went to `googletagmanager.com`,
`google-analytics.com`, `googleadservices.com` or `googlesyndication.com`.

**Live chat.** The chat widget loads and reports itself online. Its recording
bridge lives inside the tag manager, which now loads for every visitor, so the
path that was broken is open. A real chat was deliberately NOT started, because
that would put a fake enquiry in front of the team. Worth one real chat by a human
to close it off.

**Seen in passing, not chased.** The phone-number swap is firing twice with two
different numbers: `08000746757` and `080000746757`. The second has an extra digit.
The July audit already flagged a duplicate number-swap tag. Given that phone
enquiries recorded fell to zero in September, this is worth a proper look as its
own piece of work.
