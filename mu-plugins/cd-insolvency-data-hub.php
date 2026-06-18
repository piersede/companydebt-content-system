<?php
/**
 * Plugin Name: CD Insolvency Data Hub
 * Description: Shared front-end for every insolvency data-hub page. Enqueues the
 *              Source Serif 4 display face, injects the dashboard JS (chart view
 *              tabs + copy-citation, both flagship and new-page styles + scroll
 *              spy) and emits per-page JSON-LD (WebPage / Dataset / ItemList /
 *              BreadcrumbList). All of this is stripped from page content by
 *              KSES, so it lives here.
 * Version:     2.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Slugs of the data-hub pages this plugin drives. The hub itself is nested at
 * /data/company-insolvency/ but WordPress stores only the leaf slug in
 * post_name ('company-insolvency'); the two data pages are nested below it.
 */
function cd_datahub_known_slugs() {
    return array(
        'uk-insolvency-statistics',
        'company-insolvency',
        'winding-up-petition-tracker',
        'dissolutions-vs-insolvencies',
        'payment-practices-late-payment',
    );
}

/**
 * Return the current data-hub slug, or '' if this is not a data-hub page.
 */
function cd_datahub_current_slug() {
    if ( ! is_page() ) {
        return '';
    }
    $slug = get_post_field( 'post_name', get_queried_object_id() );
    return in_array( $slug, cd_datahub_known_slugs(), true ) ? $slug : '';
}

/**
 * Source Serif 4 — the display face for headings and the brand lockup. The page
 * CSS falls back to Georgia, so this only needs to load on the hub pages.
 */
add_action( 'wp_enqueue_scripts', function() {
    if ( '' === cd_datahub_current_slug() ) {
        return;
    }
    wp_enqueue_style(
        'cd-source-serif-4',
        'https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap',
        array(),
        null
    );
}, 5 );

/**
 * Dashboard JS: chart view tabs, both copy-citation styles and the nav
 * scroll-spy. Every behaviour is feature-guarded, so the single block is safe on
 * any data-hub page — it only wires up the elements that page actually has.
 */
add_action( 'wp_footer', function() {
    if ( '' === cd_datahub_current_slug() ) {
        return;
    }
    ?>
<script id="cd-insolvency-hub-js">
(function(){
    var hub = document.querySelector('.cd-data-hub');
    if (!hub) { return; }

    // Chart view tabs (flagship dashboard only).
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

    // Copy citation — flagship style ([data-cd-copy] -> target element text).
    hub.querySelectorAll('[data-cd-copy]').forEach(function(btn){
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

    // Copy citation — new data-page style (.cd-cite block builds its own string).
    hub.querySelectorAll('.cd-cite').forEach(function(block){
        var out = block.querySelector('.cd-cite__text');
        var btn = block.querySelector('[data-copy]');
        var status = block.querySelector('.cd-cite__status');
        if (!out) { return; }
        var title = block.getAttribute('data-cite-title') || document.title.split('|')[0].trim();
        var canon = document.querySelector('link[rel="canonical"]');
        var og = document.querySelector('meta[property="og:url"]');
        var url = block.getAttribute('data-cite-url') || (canon && canon.href) || (og && og.content) || location.href;
        var accessed = new Date().toLocaleDateString('en-GB', { day:'numeric', month:'long', year:'numeric' });
        var citation = 'CompanyDebt (2026) ‘' + title + '’. Available at: ' + url + ' (Accessed: ' + accessed + ').';
        out.textContent = citation;
        if (!btn) { return; }
        function flash(){ if (status) { status.textContent = 'Copied to clipboard'; setTimeout(function(){ status.textContent=''; }, 2600); } }
        function fallback(){
            var r = document.createRange(); r.selectNodeContents(out);
            var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
            try { document.execCommand('copy'); } catch(e){}
            s.removeAllRanges();
        }
        btn.addEventListener('click', function(){
            try {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(citation).catch(fallback);
                } else { fallback(); }
            } catch(e) { fallback(); }
            flash();
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

/* ------------------------------------------------------------------ *
 *  JSON-LD per page. Emitted in <head> so structured-data parsers
 *  find it. Headline figures are hard-coded (the data dir is not on
 *  the server); refresh them when the page copy is refreshed.
 * ------------------------------------------------------------------ */

/**
 * Shared Organization node, referenced by @id from each page graph.
 */
function cd_datahub_org_node() {
    return array(
        '@type' => 'Organization',
        '@id'   => home_url( '/' ) . '#organization',
        'name'  => 'Company Debt',
        'url'   => home_url( '/' ),
        'logo'  => array(
            '@type' => 'ImageObject',
            'url'   => get_template_directory_uri() . '/assets/images/cd-logo-topnav-v3.png',
        ),
    );
}

/**
 * Breadcrumb node. $trail is an array of [name, url] pairs, in order.
 */
function cd_datahub_breadcrumb( $trail ) {
    $items = array();
    foreach ( $trail as $i => $crumb ) {
        $items[] = array(
            '@type'    => 'ListItem',
            'position' => $i + 1,
            'name'     => $crumb[0],
            'item'     => $crumb[1],
        );
    }
    return array(
        '@type'           => 'BreadcrumbList',
        'itemListElement' => $items,
    );
}

/**
 * Build the @graph for a given data-hub slug, or null to skip.
 */
function cd_datahub_schema_graph( $slug, $page_id ) {
    $home      = home_url( '/' );
    $org_ref   = array( '@id' => $home . '#organization' );
    $published = get_the_date( 'Y-m-d', $page_id );
    $modified  = get_the_modified_date( 'Y-m-d', $page_id );
    $hub_url   = home_url( '/data/company-insolvency/' );

    if ( 'uk-insolvency-statistics' === $slug ) {
        $page_url  = home_url( '/data/uk-insolvency-statistics/' );
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
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'         => 'WebPage',
                '@id'           => $page_url . '#webpage',
                'name'          => 'UK Company Insolvency Statistics: April 2026 Update',
                'description'   => 'Latest UK company insolvency statistics — April 2026 figures from the Insolvency Service (published 19 May 2026). Monthly headline counts, the 12-month rolling rate, sector breakdown and UK-nations comparison.',
                'dateModified'  => $modified,
                'datePublished' => $published,
                'inLanguage'    => 'en-GB',
                'publisher'     => $org_ref,
                'about'         => array(
                    array( '@type' => 'Thing', 'name' => 'UK company insolvency' ),
                    array( '@type' => 'Thing', 'name' => 'Creditors voluntary liquidation' ),
                    array( '@type' => 'Thing', 'name' => 'Compulsory liquidation' ),
                    array( '@type' => 'Thing', 'name' => 'Company administration' ),
                ),
            ),
            cd_datahub_org_node(),
            cd_datahub_breadcrumb( array(
                array( 'Home', $home ),
                array( 'Insolvency', home_url( '/insolvency/' ) ),
                array( 'UK Company Insolvency Statistics: April 2026 Update', $page_url ),
            ) ),
            array(
                '@type'                => 'Dataset',
                'name'                 => 'UK Company Insolvency Statistics 2026',
                'description'          => 'Monthly company insolvency statistics for the United Kingdom by procedure, sector and jurisdiction. April 2026 release published 19 May 2026 by the Insolvency Service. Includes headline counts (2,085 England and Wales) and the 12-month rolling rate (51.8 per 10,000).',
                'url'                  => $page_url,
                'creator'              => $org_ref,
                'publisher'            => $org_ref,
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
        );
    }

    if ( 'company-insolvency' === $slug ) {
        $page_url = $hub_url;
        $cards = array(
            array( 'UK Company Insolvency Statistics', home_url( '/data/uk-insolvency-statistics/' ) ),
            array( 'Winding-Up Petition Tracker', home_url( '/data/company-insolvency/winding-up-petition-tracker/' ) ),
            array( 'Company Dissolutions vs Insolvencies', home_url( '/data/company-insolvency/dissolutions-vs-insolvencies/' ) ),
        );
        $list_items = array();
        foreach ( $cards as $i => $card ) {
            $list_items[] = array(
                '@type'    => 'ListItem',
                'position' => $i + 1,
                'name'     => $card[0],
                'url'      => $card[1],
            );
        }
        return array(
            array(
                '@type'         => 'WebPage',
                '@id'           => $page_url . '#webpage',
                'name'          => 'UK Company Insolvency Data',
                'description'   => 'Official, citable UK company insolvency data for journalists, accountants, lenders and company directors. Latest headline figures and a directory of every CompanyDebt data page.',
                'dateModified'  => $modified,
                'datePublished' => $published,
                'inLanguage'    => 'en-GB',
                'publisher'     => $org_ref,
            ),
            cd_datahub_org_node(),
            cd_datahub_breadcrumb( array(
                array( 'Home', $home ),
                array( 'UK Company Insolvency Data', $page_url ),
            ) ),
            array(
                '@type'           => 'ItemList',
                'name'            => 'CompanyDebt insolvency data pages',
                'itemListElement' => $list_items,
            ),
        );
    }

    if ( 'winding-up-petition-tracker' === $slug ) {
        $page_url = home_url( '/data/company-insolvency/winding-up-petition-tracker/' );
        return array(
            array(
                '@type'         => 'WebPage',
                '@id'           => $page_url . '#webpage',
                'name'          => 'Winding-Up Petition Tracker',
                'description'   => 'A monthly tracker of winding-up petitions advertised in The Gazette, with petition dismissals and winding-up orders for context. The early-warning view of corporate legal pressure in the UK.',
                'dateModified'  => $modified,
                'datePublished' => $published,
                'inLanguage'    => 'en-GB',
                'publisher'     => $org_ref,
            ),
            cd_datahub_org_node(),
            cd_datahub_breadcrumb( array(
                array( 'Home', $home ),
                array( 'UK Company Insolvency Data', $hub_url ),
                array( 'Winding-Up Petition Tracker', $page_url ),
            ) ),
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Winding-Up Petition Notices',
                'description'      => 'Monthly counts of winding-up petitions advertised in The Gazette, with petition dismissals and winding-up orders. Latest month (May 2026): 482 petitions advertised, 373 winding-up orders made, 25 petition dismissals. These are statutory notices, not official Insolvency Service statistics or final outcomes.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2025-02/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.thegazette.co.uk/',
                'measurementTechnique' => 'Counts of statutory insolvency notices advertised in The Gazette.',
                'keywords'        => 'winding-up petition, winding-up order, The Gazette, compulsory liquidation, corporate distress, UK',
            ),
        );
    }

    if ( 'dissolutions-vs-insolvencies' === $slug ) {
        $page_url = home_url( '/data/company-insolvency/dissolutions-vs-insolvencies/' );
        return array(
            array(
                '@type'         => 'WebPage',
                '@id'           => $page_url . '#webpage',
                'name'          => 'Company Dissolutions vs Insolvencies',
                'description'   => 'How ordinary company closures compare with formal insolvency, shown with UK data. Most companies that close are dissolved solvent; they are not insolvent.',
                'dateModified'  => $modified,
                'datePublished' => $published,
                'inLanguage'    => 'en-GB',
                'publisher'     => $org_ref,
            ),
            cd_datahub_org_node(),
            cd_datahub_breadcrumb( array(
                array( 'Home', $home ),
                array( 'UK Company Insolvency Data', $hub_url ),
                array( 'Company Dissolutions vs Insolvencies', $page_url ),
            ) ),
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Company Dissolutions, Incorporations and Insolvencies',
                'description'      => 'Monthly UK company dissolutions and incorporations from Companies House, set against formal company insolvencies from the Insolvency Service. Latest month: 59,295 dissolutions and 62,523 incorporations (Companies House, May 2026) against 2,085 formal insolvencies (Insolvency Service, April 2026), or about 28 dissolutions for every insolvency.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'United Kingdom' ),
                'temporalCoverage' => '2025-02/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/organisations/companies-house',
                'measurementTechnique' => 'Companies House register flows and Insolvency Service administrative records.',
                'keywords'        => 'company dissolution, company strike-off, incorporations, company insolvency, Companies House, UK',
            ),
        );
    }

    if ( 'payment-practices-late-payment' === $slug ) {
        $page_url = home_url( '/data/company-insolvency/payment-practices-late-payment/' );
        return array(
            array(
                '@type'         => 'WebPage',
                '@id'           => $page_url . '#webpage',
                'name'          => 'Payment Practices & Late Payment',
                'description'   => 'How quickly large UK companies pay their suppliers, the share of invoices paid late, and which sectors are slowest. Late-payment context, not an insolvency statistic.',
                'dateModified'  => $modified,
                'datePublished' => $published,
                'inLanguage'    => 'en-GB',
                'publisher'     => $org_ref,
            ),
            cd_datahub_org_node(),
            cd_datahub_breadcrumb( array(
                array( 'Home', $home ),
                array( 'UK Company Insolvency Data', $hub_url ),
                array( 'Payment Practices & Late Payment', $page_url ),
            ) ),
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Business Payment Practices and Late Payment',
                'description'      => 'Payment performance of large UK companies and LLPs under statutory Payment Practices Reporting (Department for Business and Trade). Most recent report per company to May 2026 (6,882 companies): average 34.5 days to pay an invoice, 22% of invoices paid later than agreed terms, 60% paid within 30 days. This is enrichment context on supplier cash-flow pressure; it is NOT an insolvency statistic and must not be combined with insolvency figures.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'United Kingdom' ),
                'temporalCoverage' => '2024-12/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://check-payment-practices.service.gov.uk/',
                'measurementTechnique' => 'Statutory Payment Practices and Performance reports; sector matched via Companies House primary SIC code.',
                'keywords'        => 'payment practices, late payment, days to pay, supplier payment, Department for Business and Trade, UK',
            ),
        );
    }

    return null;
}

add_action( 'wp_head', function() {
    $slug = cd_datahub_current_slug();
    if ( '' === $slug ) {
        return;
    }
    $page_id = get_queried_object_id();
    $graph   = cd_datahub_schema_graph( $slug, $page_id );
    if ( null === $graph ) {
        return;
    }
    $schema = array(
        '@context' => 'https://schema.org',
        '@graph'   => $graph,
    );
    echo '<script type="application/ld+json" id="cd-insolvency-hub-schema">' .
        wp_json_encode( $schema, JSON_UNESCAPED_SLASHES ) .
        '</script>' . "\n";
}, 30 );
