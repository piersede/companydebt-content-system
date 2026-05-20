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

    $page_url = home_url( '/uk-insolvency-statistics/' );
    $modified = get_the_modified_date( 'Y-m-d', get_queried_object_id() );

    $schema = array(
        '@context' => 'https://schema.org',
        '@graph'   => array(
            array(
                '@type'        => 'WebPage',
                '@id'          => $page_url . '#webpage',
                'name'         => 'UK Company Insolvency Statistics 2026',
                'description'  => 'Monthly UK company insolvency statistics using Insolvency Service and Companies House data. Track CVLs, compulsory liquidations, administrations, insolvency rates and sector trends.',
                'dateModified' => $modified,
                'publisher'    => array( '@id' => home_url( '/' ) . '#organization' ),
            ),
            array(
                '@type' => 'Organization',
                '@id'   => home_url( '/' ) . '#organization',
                'name'  => 'Company Debt',
                'url'   => home_url( '/' ),
            ),
            array(
                '@type'           => 'BreadcrumbList',
                'itemListElement' => array(
                    array( '@type' => 'ListItem', 'position' => 1, 'name' => 'Home',                                 'item' => home_url( '/' ) ),
                    array( '@type' => 'ListItem', 'position' => 2, 'name' => 'Insolvency',                           'item' => home_url( '/insolvency/' ) ),
                    array( '@type' => 'ListItem', 'position' => 3, 'name' => 'UK Company Insolvency Statistics 2026','item' => $page_url ),
                ),
            ),
            array(
                '@type'                => 'Dataset',
                'name'                 => 'UK Company Insolvency Statistics 2026',
                'description'          => 'Monthly company insolvency statistics for the United Kingdom by procedure, sector and jurisdiction, presented from official Insolvency Service and Companies House releases.',
                'creator'              => array(
                    '@type' => 'GovernmentOrganization',
                    'name'  => 'Insolvency Service',
                    'url'   => 'https://www.gov.uk/government/organisations/insolvency-service',
                ),
                'publisher'            => array( '@id' => home_url( '/' ) . '#organization' ),
                'spatialCoverage'      => array( '@type' => 'Place', 'name' => 'United Kingdom' ),
                'temporalCoverage'     => '2000-01/2026-04',
                'isBasedOn'            => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Administrative company insolvency records and Companies House register data.',
                'dateModified'         => $modified,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
            ),
        ),
    );

    echo '<script type="application/ld+json" id="cd-insolvency-hub-schema">' .
        wp_json_encode( $schema, JSON_UNESCAPED_SLASHES ) .
        '</script>' . "\n";
}, 30 );
