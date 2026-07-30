<?php
/**
 * Plugin Name: CD -- do not delay the Google Tag Manager loader
 * Description: WP Rocket's "Delay JavaScript execution" holds the GTM loader
 *   until the visitor's first scroll/click/keypress, so on a cold page view there
 *   is no GTM, no dataLayer and no Consent Mode signal at all. Verified on live
 *   2026-07-29: the loader renders as type="text/rocketlazyloadscript".
 *
 *   Three consequences:
 *     1) A visitor who declines cookies never sends the anonymous (cookieless)
 *        Consent Mode ping, because the tag never loads to send it. Google Ads
 *        reports conversion modelling as active, but it has been modelling from
 *        almost nothing.
 *     2) A visitor who lands and leaves without interacting is invisible to all
 *        measurement, so no landing page can be judged on cost per enquiry.
 *     3) Google's tag-coverage crawler never interacts, so it reports real ad
 *        landing pages (/about-us/, /company-rescue-solutions/,
 *        /advice/get-free-business-debt-advice/) as "not tagged". That is what
 *        drives "Tag quality: Urgent" on Google tag AW-977276330.
 *
 * ---------------------------------------------------------------------------
 * HARD PREREQUISITE -- READ BEFORE PUSHING THIS TO LIVE
 * ---------------------------------------------------------------------------
 *   This file is ONLY safe when the Consent Mode v2 *default* snippet is present
 *   in header.php ABOVE the GTM snippet, and is itself excluded from WP Rocket's
 *   delay. Both parts were added on staging 2026-07-29:
 *     - theme header.php ....... the snippet, marked /* cd-consent-default *\/
 *     - cd-consent-mode-defaults.php ... keeps that snippet un-delayed
 *
 *   As of 2026-07-29 LIVE HAS NEITHER. Live's HTML contains no consent default
 *   at all; the delay is currently the only thing preventing Google tags from
 *   initialising with no consent state. Un-delaying GTM on live before those two
 *   land would cause Google tags to boot with no consent state and write
 *   _ga / _gcl_* cookies before the visitor has answered the banner.
 *
 *   Push order to live is therefore: header.php, then cd-consent-mode-defaults.php,
 *   then this file. Never this file first.
 * ---------------------------------------------------------------------------
 *
 *   DELIBERATELY NOT EXCLUDED: the click-id capture script (data-cd-lc). It was
 *   made consent-gated on 2026-07-29 and now stores nothing unless the CookieYes
 *   cookie says advertisement:yes. Leaving it delayed costs nothing, because a
 *   visitor who accepts the banner has by definition interacted, which releases
 *   WP Rocket's delayed scripts anyway. Excluding it would only add third-party
 *   work to the critical path for no measurement gain.
 *
 *   TRADE-OFF: freeing GTM costs mobile performance, since third-party JS now
 *   executes during load rather than after first interaction. Mobile was already
 *   the weak side (~38 vs ~98 desktop). Measure before and after rather than
 *   assuming it is negligible.
 *
 *   VERIFY AFTER DEPLOYING -- do NOT trust a 200:
 *     1. View source: the GTM snippet must have no type attribute (or
 *        type="text/javascript"), never type="text/rocketlazyloadscript".
 *     2. Clean browser profile, do not touch the banner, then in the console:
 *          window.cdConsentDefaultApplied         -> true
 *          google_tag_data.ics.entries.ad_storage -> default:false
 *          document.cookie                        -> no _ga, no _gcl_*
 *
 *   Added 2026-07-29. Delete this file to revert completely.
 * Author: Company Debt
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/**
 * WP Rocket matches these as regex fragments against each script, so dots are
 * escaped. Three patterns for one script so it is matched whether WP Rocket
 * tests the tag attributes or the inline body:
 *
 *   GTM-5GTD9ZP                    the container id, unique to this site
 *   gtm\.start                     the dataLayer push inside the loader
 *   googletagmanager\.com/gtm\.js  the src it injects, if ever inlined
 */
add_filter( 'rocket_delay_js_exclusions', function ( $excluded ) {
	$add = array(
		'GTM-5GTD9ZP',
		'gtm\.start',
		'googletagmanager\.com/gtm\.js',
	);
	return array_values( array_unique( array_merge( (array) $excluded, $add ) ) );
} );
