<?php
/**
 * Plugin Name: CD Layout Fixes
 * Description: Horizontal-overflow fix for the nav dropdowns, plus the homepage
 *              hero column rebalance that keeps the H1 on one line.
 * Version: 1.0
 *
 * Diagnosed 2026-07-24 by measuring documentElement.scrollWidth against
 * clientWidth across viewport widths in same-origin iframes.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('wp_head', function () {
    ?>
<style id="cd-layout-fixes">
/* ------------------------------------------------------------------ *
 * 1. Nav dropdown horizontal overflow  (SITE-WIDE, desktop nav only)
 *
 * The sub-menus are position:absolute, left:0, width:240px, and while closed
 * they render as display:block + visibility:hidden + opacity:0 rather than
 * display:none. They therefore occupy scroll area at all times. The right-most
 * item's dropdown extends past the viewport and forces a permanent horizontal
 * scrollbar, which is what cuts content off when the window is narrowed.
 *
 * Measured at a 1080px window: page scrollWidth 1176 vs viewport 1065, and the
 * offending ul.sub-menu's right edge was exactly 1176. Opening the last two
 * dropdowns leftwards returns scrollWidth to 1080 (scrollbar width only).
 *
 * Scoped to the desktop nav so the mobile burger menu is untouched.
 * ------------------------------------------------------------------ */
@media (min-width: 992px) {
    .site-header .nav-menu > li:nth-last-child(-n+2) > .sub-menu {
        left: auto !important;
        right: 0 !important;
    }
}

/* ------------------------------------------------------------------ *
 * 2. Homepage hero H1 on one line  (HOMEPAGE ONLY, wide desktop only)
 *
 * The hero H1 needs ~732px to sit on one line but the 60% text column only
 * offers ~726px of content box, so it wrapped and left an orphan word.
 * Rebalancing the pair to 62/38 gives ~751px. The two columns still total
 * 100%, so this cannot introduce new horizontal overflow.
 *
 * The theme only applies its 60/40 split above ~1024px and stacks the columns
 * below that, so this is gated at 1200px and never touches the stacked layout.
 * Below roughly a 1290px window the container has not yet reached its 1260px
 * max-width, so the H1 still wraps there by design.
 * ------------------------------------------------------------------ */
@media (min-width: 1200px) {
    body.home .section-hero-blue .row > .col-6-hero-blue:first-child {
        flex-basis: 62% !important;
        max-width: 62% !important;
    }

    body.home .section-hero-blue .row > .col-6-hero-blue:last-child {
        flex-basis: 38% !important;
        max-width: 38% !important;
    }
}
</style>
    <?php
}, 99);
