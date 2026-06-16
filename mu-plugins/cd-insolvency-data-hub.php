<?php
/**
 * Plugin Name: CD Insolvency Data Hub
 * Description: Injects dashboard JS (chart view tabs + copy-citation button) and JSON-LD
 *              Dataset schema for the /uk-insolvency-statistics/ data dashboard page.
 *              These are stripped from page content by KSES, so they live here.
 * Version:     1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Return true on the UK insolvency statistics data hub page.
 */
function cd_insolvency_hub_is_target_page() {
    if ( ! is_page() ) {
        return false;
    }
    $slug = get_post_field( 'post_name', get_queried_object_id() );
    return $slug === 'uk-insolvency-statistics';
}

/**
 * Dashboard JS: chart view tabs + copy-citation button.
 * Vanilla JS, no dependencies. Loaded only on the target page.
 */
add_action( 'wp_footer', function() {
    if ( ! cd_insolvency_hub_is_target_page() ) {
        return;
    }
    ?>
<script id="cd-insolvency-hub-js">
(function(){
    var hub = document.querySelector('.cd-data-hub');
    if (!hub) { return; }

    // Chart view tabs
    var tabs  = hub.querySelectorAll('[data-cd-view]');
    var panes = hub.querySelectorAll('[data-cd-view-pane]');
    tabs.forEach(function(tab){
        tab.addEventListener('click', function(){
            var view = tab.getAttribute('data-cd-view');
            tabs.forEach(function(t){
                var active = t === tab;
                t.classList.toggle('is-active', active);
                t.setAttribute('aria-pressed', active ? 'true' : 'false');
            });
            panes.forEach(function(p){
                var active = p.getAttribute('data-cd-view-pane') === view;
                p.hidden = !active;
                p.classList.toggle('is-active', active);
            });
        });
    });

    // Copy citation button
    var btns = hub.querySelectorAll('[data-cd-copy]');
    btns.forEach(function(btn){
        btn.addEventListener('click', function(){
            var target = document.querySelector(btn.getAttribute('data-cd-copy'));
            if (!target) { return; }
            var text = target.textContent.trim();
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(function(){
                    btn.classList.add('is-copied');
                    var orig = btn.textContent;
                    btn.textContent = 'Copied';
                    setTimeout(function(){
                        btn.classList.remove('is-copied');
                        btn.textContent = orig;
                    }, 1800);
                });
            }
        });
    });

    // Sticky nav scroll-spy — highlight the section currently in view.
    var navLinks = Array.prototype.slice.call(hub.querySelectorAll('.cd-secnav a'));
    if (navLinks.length && 'IntersectionObserver' in window) {
        var sectionMap = {};
        navLinks.forEach(function(link){
            var id = link.getAttribute('href');
            if (id && id.indexOf('#') === 0) {
                var sec = document.querySelector(id);
                if (sec) { sectionMap[id.slice(1)] = link; }
            }
        });
        var observer = new IntersectionObserver(function(entries){
            entries.forEach(function(entry){
                var link = sectionMap[entry.target.id];
                if (!link) return;
                if (entry.isIntersecting) {
                    navLinks.forEach(function(l){ l.classList.remove('is-active'); });
                    link.classList.add('is-active');
                }
            });
        }, { rootMargin: '-80px 0px -65% 0px', threshold: 0 });
        Object.keys(sectionMap).forEach(function(id){
            var el = document.getElementById(id);
            if (el) observer.observe(el);
        });
    }
})();
</script>
    <?php
}, 50 );

/**
 * JSON-LD: WebPage + Dataset + BreadcrumbList + Organization.
 * Emitted in <head> so Google's structured-data parsers find it.
 */
add_action( 'wp_head', function() {
    if ( ! cd_insolvency_hub_is_target_page() ) {
        return;
    }

    $page_url  = home_url( '/uk-insolvency-statistics/' );
    $modified  = get_the_modified_date( 'Y-m-d', get_queried_object_id() );
    $published = get_the_date( 'Y-m-d', get_queried_object_id() );
    $logo_url  = get_template_directory_uri() . '/assets/images/cd-logo-topnav-v3.png';

    $faq_items = array(
        array(
            'q' => 'How many UK company insolvencies were there in April 2026?',
            'a' => 'There were 2,085 registered company insolvencies in England and Wales in April 2026, on a seasonally adjusted basis. That was 2% higher than March 2026 and 3% higher than April 2025. Scotland recorded 107 insolvencies and Northern Ireland 40 in the same month.',
        ),
        array(
            'q' => 'What is the current UK company insolvency rate?',
            'a' => 'The 12-month rolling company insolvency rate for England and Wales was 51.8 per 10,000 active companies in the year to April 2026 — equal to one in 193 companies. The rate is slightly lower than the 52.5 per 10,000 recorded a year earlier, and well below the 113.1 per 10,000 peak of the 2008–09 recession.',
        ),
        array(
            'q' => 'Which procedure accounts for the most UK company insolvencies?',
            'a' => "Creditors' Voluntary Liquidations (CVLs) account for the largest share. There were 1,510 CVLs in April 2026 — 72% of all company insolvencies for the month. Compulsory liquidations (371) and administrations (183) followed, with very small numbers of CVAs (20) and receiverships (1).",
        ),
        array(
            'q' => 'Which UK sectors have the most company insolvencies?',
            'a' => 'Across the 12 months to March 2026, construction (3,827, 16%), wholesale and retail (3,642, 16%), and accommodation and food services (3,295, 14%) had the largest counts. Administrative services, professional services and manufacturing followed. These are volumes, not failure rates — larger sectors have more registered companies and so tend to have more insolvencies.',
        ),
        array(
            'q' => 'When is the next UK insolvency statistics release?',
            'a' => 'The Insolvency Service publishes monthly company insolvency statistics. The next scheduled release is 19 June 2026. This page is updated each month from the official release.',
        ),
        array(
            'q' => 'Where does this UK insolvency data come from?',
            'a' => 'Company insolvency data is published by the Insolvency Service as accredited official statistics, sourced mainly from Companies House. Compulsory liquidations for England and Wales come from the Insolvency Service directly; Northern Ireland compulsory liquidation data comes from the Department for the Economy. CompanyDebt presents the published figures — we do not produce them.',
        ),
    );

    $faq_main_entities = array();
    foreach ( $faq_items as $item ) {
        $faq_main_entities[] = array(
            '@type'          => 'Question',
            'name'           => $item['q'],
            'acceptedAnswer' => array(
                '@type' => 'Answer',
                'text'  => $item['a'],
            ),
        );
    }

    $schema = array(
        '@context' => 'https://schema.org',
        '@graph'   => array(
            array(
                '@type'        => 'WebPage',
                '@id'          => $page_url . '#webpage',
                'name'         => 'UK Company Insolvency Statistics: April 2026 Update',
                'description'  => 'Latest UK company insolvency statistics — April 2026 figures from the Insolvency Service (published 19 May 2026). Monthly headline counts, the 12-month rolling rate, sector breakdown and UK-nations comparison.',
                'dateModified' => $modified,
                'datePublished'=> $published,
                'inLanguage'   => 'en-GB',
                'publisher'    => array( '@id' => home_url( '/' ) . '#organization' ),
                'about'        => array(
                    array( '@type' => 'Thing', 'name' => 'UK company insolvency' ),
                    array( '@type' => 'Thing', 'name' => 'Creditors voluntary liquidation' ),
                    array( '@type' => 'Thing', 'name' => 'Compulsory liquidation' ),
                    array( '@type' => 'Thing', 'name' => 'Company administration' ),
                ),
            ),
            array(
                '@type' => 'Organization',
                '@id'   => home_url( '/' ) . '#organization',
                'name'  => 'Company Debt',
                'url'   => home_url( '/' ),
                'logo'  => array(
                    '@type' => 'ImageObject',
                    'url'   => $logo_url,
                ),
            ),
            array(
                '@type'           => 'BreadcrumbList',
                'itemListElement' => array(
                    array( '@type' => 'ListItem', 'position' => 1, 'name' => 'Home',                                                  'item' => home_url( '/' ) ),
                    array( '@type' => 'ListItem', 'position' => 2, 'name' => 'Insolvency',                                            'item' => home_url( '/insolvency/' ) ),
                    array( '@type' => 'ListItem', 'position' => 3, 'name' => 'UK Company Insolvency Statistics: April 2026 Update',   'item' => $page_url ),
                ),
            ),
            array(
                '@type'                => 'Dataset',
                'name'                 => 'UK Company Insolvency Statistics 2026',
                'description'          => 'Monthly company insolvency statistics for the United Kingdom by procedure, sector and jurisdiction. April 2026 release published 19 May 2026 by the Insolvency Service. Includes headline counts (2,085 England and Wales) and the 12-month rolling rate (51.8 per 10,000).',
                'url'                  => $page_url,
                'creator'              => array( '@id' => home_url( '/' ) . '#organization' ),
                'publisher'            => array( '@id' => home_url( '/' ) . '#organization' ),
                'spatialCoverage'      => array( '@type' => 'Place', 'name' => 'United Kingdom' ),
                'temporalCoverage'     => '2000-01/2026-04',
                'datePublished'        => $published,
                'dateModified'         => $modified,
                'isBasedOn'            => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Administrative company insolvency records and Companies House register data.',
                'keywords'             => 'UK company insolvency, insolvency statistics, CVL statistics, compulsory liquidation, administration, insolvency rate, sector insolvency',
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $faq_main_entities,
            ),
        ),
    );

    echo '<script type="application/ld+json" id="cd-insolvency-hub-schema">' .
        wp_json_encode( $schema, JSON_UNESCAPED_SLASHES ) .
        '</script>' . "\n";
}, 30 );
