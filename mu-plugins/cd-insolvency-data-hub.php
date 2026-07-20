<?php
/**
 * Plugin Name: CD Insolvency Data Hub
 * Description: Shared front-end for every insolvency data-hub page. Enqueues the
 *              Source Serif 4 display face, injects the dashboard JS (chart view
 *              tabs + copy-citation, both flagship and new-page styles + scroll
 *              spy) and emits per-page JSON-LD (WebPage / Dataset / ItemList /
 *              BreadcrumbList). All of this is stripped from page content by
 *              KSES, so it lives here.
 * Version:     2.3.0
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Slugs of the data-hub pages this plugin drives. The hub itself is /data/
 * (post_name 'data'); every data page sits directly beneath it as
 * /data/<slug>/.
 */
function cd_datahub_known_slugs() {
    return array(
        'uk-insolvency-statistics',
        'data',
        'winding-up-petition-tracker',
        'dissolutions-vs-insolvencies',
        'payment-practices-late-payment',
        'cvl-statistics',
        'compulsory-liquidation-statistics',
        'administration-statistics',
        'company-insolvencies-by-sector',
        'construction-insolvency-statistics',
        'furniture-insolvency-statistics',
        'restaurant-insolvency-statistics',
        'road-haulage-insolvency-statistics',
        'recruitment-agency-insolvency-statistics',
        'temporary-staffing-agency-insolvency-statistics',
        'motor-vehicle-repair-insolvency-statistics',
        'cleaning-company-insolvency-statistics',
        'hotel-insolvency-statistics',
        'estate-agency-insolvency-statistics',
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
 * Curated SEO title + meta description per data-hub slug. The values written at
 * page-creation time do not persist through Yoast (it falls back to the post
 * title and a "Last reviewed" excerpt), so we own them here, next to the
 * schema, as the single source of truth. Copy is evergreen (no month named) so
 * it does not go stale between monthly data refreshes.
 */
function cd_datahub_seo_meta( $slug ) {
    $meta = array(
        'data' => array(
            'title' => 'UK Company Insolvency Data and Statistics',
            'desc'  => 'Official, citable UK company insolvency data for journalists, lenders, accountants and directors: latest headline figures and a directory of every data page.',
        ),
        'uk-insolvency-statistics' => array(
            'title' => 'UK Company Insolvency Statistics: Latest Monthly Data',
            'desc'  => 'Latest UK insolvency statistics: monthly headline counts, the 12-month rolling rate, procedure mix and sector breakdown, from the Insolvency Service.',
        ),
        'winding-up-petition-tracker' => array(
            'title' => 'Winding-Up Petition Statistics (UK): Monthly Gazette Data',
            'desc'  => 'Monthly UK winding-up petition statistics from The Gazette: petitions advertised, orders made and the trend. A data source, not legal advice.',
        ),
        'dissolutions-vs-insolvencies' => array(
            'title' => 'Company Dissolutions vs Insolvencies (UK Data)',
            'desc'  => 'UK company dissolutions set against formal insolvencies: how many companies are dissolved each month, incorporations, and why most closures are solvent.',
        ),
        'payment-practices-late-payment' => array(
            'title' => 'Payment Practices Reporting and Late Payment Data (UK)',
            'desc'  => 'UK payment practices reporting and late-payment data: how long large firms take to pay suppliers, the share of invoices paid late and the slowest sectors.',
        ),
        'cvl-statistics' => array(
            'title' => 'UK CVL Statistics: Creditors\' Voluntary Liquidations',
            'desc'  => 'UK creditors\' voluntary liquidation (CVL) statistics: monthly volumes since 2000, share of all company insolvencies and the rate per 10,000 companies.',
        ),
        'compulsory-liquidation-statistics' => array(
            'title' => 'UK Compulsory Liquidation Statistics: Monthly Data',
            'desc'  => 'UK compulsory liquidation statistics: monthly court-ordered winding-up volumes since 2000, share of all insolvencies and the rate per 10,000.',
        ),
        'administration-statistics' => array(
            'title' => 'UK Company Administration Statistics: Monthly Data',
            'desc'  => 'UK company administration statistics: monthly volumes since 2000, share of all company insolvencies and the rate per 10,000 companies.',
        ),
        'company-insolvencies-by-sector' => array(
            'title' => 'UK Company Insolvencies by Sector',
            'desc'  => 'UK company insolvencies by sector: which industries have the most, annual trends since 2016 and the latest 12-month breakdown across all SIC sections.',
        ),
        'construction-insolvency-statistics' => array(
            'title' => 'UK Construction Insolvency Statistics',
            'desc'  => 'UK construction insolvency statistics: insolvencies in construction since 2016, the trend, sub-sector breakdown and construction\'s share of the total.',
        ),
        'furniture-insolvency-statistics' => array(
            'title' => 'UK Furniture Insolvency Statistics 2026 | Company Debt',
            'desc'  => '64 furniture manufacturers entered insolvency between January and May 2026, flat on a year earlier while manufacturing overall fell 8.5%. Latest figures.',
        ),
        'restaurant-insolvency-statistics' => array(
            'title' => 'UK Restaurant Insolvency Statistics 2026 | Company Debt',
            'desc'  => '858 restaurant and mobile food businesses entered insolvency between January and May 2026. See the latest monthly and annual restaurant insolvency figures.',
        ),
        'road-haulage-insolvency-statistics' => array(
            'title' => 'UK Road Haulage Insolvency Statistics 2026 | Company Debt',
            'desc'  => '149 road haulage and removals companies entered insolvency between January and May 2026. See the latest monthly and annual haulage insolvency figures.',
        ),
        'recruitment-agency-insolvency-statistics' => array(
            'title' => 'UK Recruitment Agency Insolvency Statistics 2026',
            'desc'  => '105 recruitment agencies entered insolvency between January and May 2026, down 29.5% from a record 2025, while temporary staffing rose. Latest figures.',
        ),
        'temporary-staffing-agency-insolvency-statistics' => array(
            'title' => 'UK Temporary Staffing Agency Insolvency Statistics 2026',
            'desc'  => 'Latest temporary staffing agency insolvency figures for England and Wales, including 2026 trends, annual data, recruitment-sector comparisons and methodology.',
        ),
        'motor-vehicle-repair-insolvency-statistics' => array(
            'title' => 'UK Garage Insolvency Statistics 2026 | Motor Vehicle Repair',
            'desc'  => '293 garages entered insolvency in 2025, a record, and 113 in the first five months of 2026. See the latest motor vehicle repair insolvency figures.',
        ),
        'cleaning-company-insolvency-statistics' => array(
            'title' => 'UK Cleaning Company Insolvency Statistics 2026',
            'desc'  => '59 cleaning contractors entered insolvency between January and May 2026, exactly flat on a year earlier while the rest of building services improved.',
        ),
        'hotel-insolvency-statistics' => array(
            'title' => 'UK Hotel Insolvency Statistics 2026 | Company Debt',
            'desc'  => '68 hotels entered insolvency between January and May 2026, down 10.5%, but 2025 was the worst year on record at 153. See the latest hotel figures.',
        ),
        'estate-agency-insolvency-statistics' => array(
            'title' => 'UK Estate Agency Insolvency Statistics 2026 | Company Debt',
            'desc'  => 'Latest estate agency insolvency statistics for England and Wales, including 2026 figures, annual trends, insolvency procedures and official SIC scope.',
        ),
    );
    return isset( $meta[ $slug ] ) ? $meta[ $slug ] : null;
}

/**
 * Override Yoast's title + description (and OG/Twitter mirrors) on data-hub
 * pages with the curated copy above.
 */
add_filter( 'wpseo_title', function( $title ) {
    $m = cd_datahub_seo_meta( cd_datahub_current_slug() );
    return $m ? $m['title'] : $title;
}, 20 );

add_filter( 'wpseo_metadesc', function( $desc ) {
    $m = cd_datahub_seo_meta( cd_datahub_current_slug() );
    return $m ? $m['desc'] : $desc;
}, 20 );

add_filter( 'wpseo_opengraph_title', function( $title ) {
    $m = cd_datahub_seo_meta( cd_datahub_current_slug() );
    return $m ? $m['title'] : $title;
}, 20 );

add_filter( 'wpseo_opengraph_desc', function( $desc ) {
    $m = cd_datahub_seo_meta( cd_datahub_current_slug() );
    return $m ? $m['desc'] : $desc;
}, 20 );

add_filter( 'wpseo_twitter_title', function( $title ) {
    $m = cd_datahub_seo_meta( cd_datahub_current_slug() );
    return $m ? $m['title'] : $title;
}, 20 );

add_filter( 'wpseo_twitter_description', function( $desc ) {
    $m = cd_datahub_seo_meta( cd_datahub_current_slug() );
    return $m ? $m['desc'] : $desc;
}, 20 );

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
    // Inline, self-contained organization. Yoast already emits the canonical
    // Organization + WebPage + BreadcrumbList graph for these pages, so this
    // plugin no longer duplicates those nodes (which collided on @id); it adds
    // only the value-add Dataset / FAQPage / ItemList that Yoast does not.
    $org_ref   = array( '@type' => 'Organization', 'name' => 'Company Debt', 'url' => $home );
    $published = get_the_date( 'Y-m-d', $page_id );
    $modified  = get_the_modified_date( 'Y-m-d', $page_id );
    $hub_url   = home_url( '/data/' );

    if ( 'uk-insolvency-statistics' === $slug ) {
        $page_url  = home_url( '/data/uk-insolvency-statistics/' );
        $faq_items = array(
            array(
                'q' => 'How many UK company insolvencies were there in May 2026?',
                'a' => 'There were 1,868 registered company insolvencies in England and Wales in May 2026, on a seasonally adjusted basis. That was 10% lower than April 2026 and 16% lower than May 2025. Scotland recorded 100 insolvencies and Northern Ireland 30 in the same month.',
            ),
            array(
                'q' => 'What is the current UK company insolvency rate?',
                'a' => 'The 12-month rolling company insolvency rate for England and Wales was 50.9 per 10,000 active companies in the year to May 2026 — equal to one in 196 companies. The rate is lower than the 53.0 per 10,000 recorded a year earlier, and well below the 113.1 per 10,000 peak of the 2008–09 recession.',
            ),
            array(
                'q' => 'Which procedure accounts for the most UK company insolvencies?',
                'a' => "Creditors' Voluntary Liquidations (CVLs) account for the largest share. There were 1,423 CVLs in May 2026 — 76% of all company insolvencies for the month. Compulsory liquidations (285) and administrations (135) followed, with a small number of CVAs (25) and no receiverships.",
            ),
            array(
                'q' => 'Which UK sectors have the most company insolvencies?',
                'a' => 'Across the 12 months to May 2026, construction (3,803, 17%), wholesale and retail (3,527, 15%), and accommodation and food services (3,296, 14%) had the largest counts. Administrative services, professional services and manufacturing followed. These are volumes, not failure rates — larger sectors have more registered companies and so tend to have more insolvencies.',
            ),
            array(
                'q' => 'When is the next UK insolvency statistics release?',
                'a' => 'The Insolvency Service publishes monthly company insolvency statistics. The next scheduled release is 17 July 2026. This page is updated each month from the official release.',
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
                '@type'                => 'Dataset',
                'name'                 => 'UK Company Insolvency Statistics 2026',
                'description'          => 'Monthly company insolvency statistics for the United Kingdom by procedure, sector and jurisdiction. May 2026 release published 19 June 2026 by the Insolvency Service. Includes headline counts (1,868 England and Wales) and the 12-month rolling rate (50.9 per 10,000).',
                'url'                  => $page_url,
                'creator'              => $org_ref,
                'publisher'            => $org_ref,
                'spatialCoverage'      => array( '@type' => 'Place', 'name' => 'United Kingdom' ),
                'temporalCoverage'     => '2000-01/2026-05',
                'datePublished'        => $published,
                'dateModified'         => $modified,
                'isBasedOn'            => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Administrative company insolvency records and Companies House register data.',
                'keywords'             => 'UK company insolvency, insolvency statistics, CVL statistics, compulsory liquidation, administration, insolvency rate, sector insolvency',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Company insolvencies (monthly count)',
                    'Creditors voluntary liquidations (CVL)',
                    'Compulsory liquidations',
                    'Administrations',
                    'Insolvency rate per 10,000 active companies',
                ),
                'distribution'         => array(
                    '@type'          => 'DataDownload',
                    'name'           => 'UK company insolvency monthly series (CSV)',
                    'encodingFormat' => 'text/csv',
                    'contentUrl'     => home_url( '/wp-content/themes/company-debt-webpigment/assets/data-hub/downloads/uk-company-insolvency-statistics.csv' ),
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $faq_main_entities,
            ),
        );
    }

    if ( 'data' === $slug ) {
        $page_url = $hub_url;
        $cards = array(
            array( 'UK Company Insolvency Statistics', home_url( '/data/uk-insolvency-statistics/' ) ),
            array( 'Winding-Up Petition Tracker', home_url( '/data/winding-up-petition-tracker/' ) ),
            array( 'Company Dissolutions vs Insolvencies', home_url( '/data/dissolutions-vs-insolvencies/' ) ),
            array( 'Payment Practices and Late Payment', home_url( '/data/payment-practices-late-payment/' ) ),
            array( 'CVL Statistics', home_url( '/data/cvl-statistics/' ) ),
            array( 'Compulsory Liquidation Statistics', home_url( '/data/compulsory-liquidation-statistics/' ) ),
            array( 'Administration Statistics', home_url( '/data/administration-statistics/' ) ),
            array( 'Company Insolvencies by Sector', home_url( '/data/company-insolvencies-by-sector/' ) ),
            array( 'Construction Insolvency Statistics', home_url( '/data/construction-insolvency-statistics/' ) ),
            array( 'Furniture Manufacturing Insolvency Statistics', home_url( '/data/furniture-insolvency-statistics/' ) ),
            array( 'Restaurant Insolvency Statistics', home_url( '/data/restaurant-insolvency-statistics/' ) ),
            array( 'Road Haulage Insolvency Statistics', home_url( '/data/road-haulage-insolvency-statistics/' ) ),
            array( 'Recruitment Agency Insolvency Statistics', home_url( '/data/recruitment-agency-insolvency-statistics/' ) ),
            array( 'Temporary Staffing Agency Insolvency Statistics', home_url( '/data/temporary-staffing-agency-insolvency-statistics/' ) ),
            array( 'Motor Vehicle Repair Insolvency Statistics', home_url( '/data/motor-vehicle-repair-insolvency-statistics/' ) ),
            array( 'Cleaning Company Insolvency Statistics', home_url( '/data/cleaning-company-insolvency-statistics/' ) ),
            array( 'Hotel Insolvency Statistics', home_url( '/data/hotel-insolvency-statistics/' ) ),
            array( 'Estate Agency Insolvency Statistics', home_url( '/data/estate-agency-insolvency-statistics/' ) ),
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
                '@type'           => 'ItemList',
                'name'            => 'CompanyDebt insolvency data pages',
                'itemListElement' => $list_items,
            ),
        );
    }

    if ( 'winding-up-petition-tracker' === $slug ) {
        $page_url = home_url( '/data/winding-up-petition-tracker/' );
        return array(
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
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Winding-up petitions advertised',
                    'Winding-up orders made',
                    'Petition dismissals',
                ),
                'distribution'         => array(
                    '@type'          => 'DataDownload',
                    'name'           => 'UK winding-up petition notices monthly series (CSV)',
                    'encodingFormat' => 'text/csv',
                    'contentUrl'     => home_url( '/wp-content/themes/company-debt-webpigment/assets/data-hub/downloads/uk-winding-up-petition-notices.csv' ),
                ),
            ),
        );
    }

    if ( 'dissolutions-vs-insolvencies' === $slug ) {
        $page_url = home_url( '/data/dissolutions-vs-insolvencies/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Company Dissolutions, Incorporations and Insolvencies',
                'description'      => 'Monthly UK company dissolutions and incorporations from Companies House, set against formal company insolvencies from the Insolvency Service. Latest month: 59,295 dissolutions and 62,523 incorporations (Companies House, May 2026) against 1,868 formal insolvencies (Insolvency Service, May 2026), or about 32 dissolutions for every insolvency.',
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
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Company dissolutions',
                    'Company incorporations',
                    'Company insolvencies',
                ),
                'distribution'         => array(
                    '@type'          => 'DataDownload',
                    'name'           => 'UK dissolutions, incorporations and insolvencies monthly series (CSV)',
                    'encodingFormat' => 'text/csv',
                    'contentUrl'     => home_url( '/wp-content/themes/company-debt-webpigment/assets/data-hub/downloads/uk-company-dissolutions-vs-insolvencies.csv' ),
                ),
            ),
        );
    }

    if ( 'payment-practices-late-payment' === $slug ) {
        $page_url = home_url( '/data/payment-practices-late-payment/' );
        return array(
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
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Average days to pay an invoice',
                    'Share of invoices paid later than agreed terms',
                    'Share of invoices paid within 30 days',
                ),
                'distribution'         => array(
                    '@type'          => 'DataDownload',
                    'name'           => 'UK business payment practices by sector (CSV)',
                    'encodingFormat' => 'text/csv',
                    'contentUrl'     => home_url( '/wp-content/themes/company-debt-webpigment/assets/data-hub/downloads/uk-payment-practices-by-sector.csv' ),
                ),
            ),
        );
    }

    if ( 'cvl-statistics' === $slug ) {
        $page_url = home_url( '/data/cvl-statistics/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Creditors\' Voluntary Liquidation (CVL) Statistics',
                'description'      => 'Monthly counts of creditors\' voluntary liquidations (CVLs) in England and Wales since 2000, with the share of all company insolvencies and the rate per 10,000 active companies. CVLs are the largest single company insolvency procedure. Latest month (May 2026): 1,423 CVLs, 76% of all company insolvencies. Source: Insolvency Service.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2000-01/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Administrative company insolvency records and Companies House register data.',
                'keywords'        => 'CVL, creditors voluntary liquidation, company insolvency, liquidation statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Creditors voluntary liquidations (monthly count)',
                    'Share of all company insolvencies',
                    'CVL rate per 10,000 active companies',
                ),
            ),
        );
    }

    if ( 'compulsory-liquidation-statistics' === $slug ) {
        $page_url = home_url( '/data/compulsory-liquidation-statistics/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Compulsory Liquidation Statistics',
                'description'      => 'Monthly counts of compulsory liquidations (court-ordered windings-up) in England and Wales since 2000, with the share of all company insolvencies and the rate per 10,000 active companies. Latest month (May 2026): 285 compulsory liquidations, 15% of all company insolvencies. Source: Insolvency Service.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2000-01/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Administrative company insolvency records; compulsory liquidations for England and Wales are sourced from the Insolvency Service.',
                'keywords'        => 'compulsory liquidation, winding-up order, court-ordered liquidation, company insolvency, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Compulsory liquidations (monthly count)',
                    'Share of all company insolvencies',
                    'Compulsory liquidation rate per 10,000 active companies',
                ),
            ),
        );
    }

    if ( 'administration-statistics' === $slug ) {
        $page_url = home_url( '/data/administration-statistics/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Company Administration Statistics',
                'description'      => 'Monthly counts of companies entering administration in England and Wales since 2000, with the share of all company insolvencies and the rate per 10,000 active companies. Latest month (May 2026): 135 administrations, 7% of all company insolvencies. Source: Insolvency Service.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2000-01/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Administrative company insolvency records and Companies House register data.',
                'keywords'        => 'administration, company administration, administrator, company insolvency, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Administrations (monthly count)',
                    'Share of all company insolvencies',
                    'Administration rate per 10,000 active companies',
                ),
            ),
        );
    }

    if ( 'company-insolvencies-by-sector' === $slug ) {
        $page_url = home_url( '/data/company-insolvencies-by-sector/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Company Insolvencies by Industry Sector',
                'description'      => 'Company insolvencies in England and Wales broken down by industry (3-level Standard Industrial Classification): the latest rolling 12-month ranking across all 21 SIC sections, plus annual figures for each sector from 2016. Construction has the most insolvencies of any sector. These are volumes, not failure rates. Source: Insolvency Service.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016/2025',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Company insolvencies matched to industry via Companies House Standard Industrial Classification (SIC) codes; published quarterly.',
                'keywords'        => 'company insolvencies by sector, insolvencies by industry, SIC, construction, retail, hospitality, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Company insolvencies by SIC industry section (annual)',
                    'Company insolvencies by sector (rolling 12-month)',
                    'Sector share of known-sector insolvencies',
                ),
            ),
        );
    }

    if ( 'construction-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/construction-insolvency-statistics/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Construction Insolvency Statistics',
                'description'      => 'Company insolvencies in the UK construction sector (SIC section F), England and Wales: annual figures from 2016, the monthly series from 2023, and the split across construction of buildings, civil engineering and specialised construction. Construction has the most company insolvencies of any industry. Source: Insolvency Service.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016/2025',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Construction-sector company insolvencies identified via Companies House SIC section F; published quarterly.',
                'keywords'        => 'construction insolvency, construction company insolvencies, building, civil engineering, SIC section F, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Construction company insolvencies (annual)',
                    'Construction company insolvencies (monthly)',
                    'Construction sub-sector insolvencies',
                ),
            ),
        );
    }

    if ( 'furniture-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/furniture-insolvency-statistics/' );
        $fur_faq_items = array(
            array(
                'q' => 'How many UK furniture manufacturers become insolvent each year?',
                'a' => '143 furniture-manufacturing companies entered insolvency in England and Wales in 2025, against 139 in 2024. The series peak was 163 in 2023, and the pre-pandemic figure was 111 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are furniture insolvencies rising in 2026?',
                'a' => 'No, and they are not falling either. There were 64 insolvencies between January and May 2026 against 63 in the same months of 2025, and the rolling 12-month total was unchanged at 144. The sector is flat while manufacturing overall improved by 8.5%.',
            ),
            array(
                'q' => 'Do these figures include furniture shops and wholesalers?',
                'a' => 'No. This page counts SIC group 310, the manufacture of furniture and mattresses. Furniture retailers and wholesalers are recorded under separate retail and wholesale SIC codes and are counted elsewhere.',
            ),
            array(
                'q' => 'What is the most common insolvency procedure for furniture manufacturers?',
                'a' => 'Creditors\' voluntary liquidation, which accounted for 115 of the 143 furniture insolvencies in 2025. Compulsory liquidations, where a creditor petitions the court, nearly doubled from 9 to 17 over the same year.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $fur_faq_main_entities = array();
        foreach ( $fur_faq_items as $item ) {
            $fur_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Furniture Manufacturing Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for furniture manufacturers (SIC group 310), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023, annual figures from 2016, the split by insolvency procedure, and comparison with manufacturing overall (SIC C) and the adjacent household-goods wholesale (SIC 464) and retail (SIC 475) trades. Covers the manufacture of household, office, kitchen and shop furniture and of mattresses. Excludes furniture retailers and wholesalers, which are recorded under separate codes. Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-05-31',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-may-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons, procedure shares and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 310. The industry total is published monthly (Table 1c); the procedure-split breakdown is published quarterly.',
                'keywords'        => 'furniture manufacturing insolvency, furniture manufacturer insolvency, furniture insolvencies 2026, SIC 310 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Furniture manufacturing company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Insolvency procedure (CVL, compulsory liquidation, administration, CVA, receivership)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $fur_faq_main_entities,
            ),
        );
    }

    if ( 'restaurant-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/restaurant-insolvency-statistics/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Restaurant Insolvency Statistics',
                'description'      => 'Company insolvencies among restaurants and mobile food service businesses (SIC group 561), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016. Excludes pubs, bars and hotels. Source: Insolvency Service.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Restaurant and mobile food service company insolvencies identified via Companies House SIC group 561; the industry total is published monthly (Table 1c), the procedure-split breakdown quarterly.',
                'keywords'        => 'restaurant insolvency, restaurant insolvency statistics, SIC 561, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Restaurant company insolvencies (annual)',
                    'Restaurant company insolvencies (monthly)',
                    'Share of all company insolvencies',
                ),
            ),
        );
    }

    if ( 'road-haulage-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/road-haulage-insolvency-statistics/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Road Haulage Insolvency Statistics',
                'description'      => 'Company insolvencies among road freight and removals companies (SIC group 494), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016. Excludes storage and courier activities. Source: Insolvency Service.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01/2026-05',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/collections/insolvency-service-official-statistics',
                'measurementTechnique' => 'Road freight and removals company insolvencies identified via Companies House SIC group 494; the industry total is published monthly (Table 1c), the procedure-split breakdown quarterly.',
                'keywords'        => 'road haulage insolvency, haulage company insolvency, SIC 494, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Road haulage company insolvencies (annual)',
                    'Road haulage company insolvencies (monthly)',
                    'Share of all company insolvencies',
                ),
            ),
        );
    }

    if ( 'recruitment-agency-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/recruitment-agency-insolvency-statistics/' );
        $rec_faq_items = array(
            array(
                'q' => 'How many UK recruitment agencies become insolvent each year?',
                'a' => '345 permanent-placement recruitment agencies entered insolvency in England and Wales in 2025, the highest in the series and up from 295 in 2024. The pre-pandemic figure was 149 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are recruitment agency insolvencies falling in 2026?',
                'a' => 'Yes. There were 105 insolvencies between January and May 2026 against 149 in the same months of 2025, a fall of 29.5%, and the rolling 12-month total fell 8.0% to 301. The year-to-date fall is flattered by an unusually severe early 2025, so the rolling measure is the better guide.',
            ),
            array(
                'q' => 'Why are recruitment insolvencies falling while temporary staffing insolvencies rise?',
                'a' => 'Because employers have been hiring temporary staff instead of permanent ones. Permanent-placement insolvencies (SIC 781) fell 29.5% in the first five months of 2026 while temporary employment agency insolvencies (SIC 782) rose 7.5%. The KPMG and REC UK Report on Jobs found temp billings in June 2026 rising at their quickest rate since April 2023.',
            ),
            array(
                'q' => 'Do these figures include temp agencies?',
                'a' => 'No. This page counts SIC group 781, employment placement agencies, which mainly place candidates into permanent roles. Temporary staffing agencies are SIC 782 and are covered on their own page.',
            ),
            array(
                'q' => 'What is the most common insolvency procedure for recruitment agencies?',
                'a' => 'Creditors\' voluntary liquidation, which accounted for 266 of the 345 recruitment agency insolvencies in 2025. Compulsory liquidations, where a creditor such as HMRC petitions the court, more than doubled from 23 to 48 over the same year.',
            ),
        );
        $rec_faq_main_entities = array();
        foreach ( $rec_faq_items as $item ) {
            $rec_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Recruitment Agency Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for employment placement agencies (SIC group 781), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023, annual figures from 2016, the split by insolvency procedure, and comparison with temporary employment agencies (SIC 782) and employment activities overall (SIC 78). Covers agencies mainly placing candidates into permanent roles, including executive search and selection. Excludes agencies supplying workers on a temporary basis (SIC 782) and longer-term human resources provision (SIC 783). Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-05-31',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-may-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons, procedure shares and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 781. The industry total is published monthly (Table 1c); the procedure-split breakdown is published quarterly.',
                'keywords'        => 'recruitment agency insolvency, recruitment agency insolvencies 2026, permanent placement agency insolvency, SIC 781 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Recruitment agency company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Insolvency procedure (CVL, compulsory liquidation, administration, CVA, receivership)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $rec_faq_main_entities,
            ),
        );
    }

    if ( 'temporary-staffing-agency-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/temporary-staffing-agency-insolvency-statistics/' );
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Temporary Staffing Agency Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for temporary employment agencies (SIC group 782), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023, annual figures from 2016, and comparison with permanent-placement agencies (SIC 781) and employment activities overall (SIC 78). Excludes permanent-placement and executive-search agencies (SIC 781) and longer-term human resources provision (SIC 783). Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-05-31',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-may-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 782. The industry total is published monthly (Table 1c); the procedure-split breakdown is published quarterly.',
                'keywords'        => 'temporary staffing agency insolvency, temp agency insolvency, temporary employment agency insolvency, SIC 782, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Temporary staffing agency company insolvencies (annual)',
                    'Temporary staffing agency company insolvencies (monthly)',
                    'Share of all company insolvencies',
                ),
            ),
        );
    }

    if ( 'motor-vehicle-repair-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/motor-vehicle-repair-insolvency-statistics/' );
        $mot_faq_items = array(
            array(
                'q' => 'How many UK garages become insolvent each year?',
                'a' => '293 motor vehicle repair businesses entered insolvency in England and Wales in 2025, the highest in the series and up from 251 in 2024. The pre-pandemic figure was 164 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are garage insolvencies rising or falling in 2026?',
                'a' => 'The two measures disagree. There were 113 insolvencies between January and May 2026 against 121 a year earlier, down 6.6%, but the rolling 12-month total rose 3.3% to 285. The improvement is recent, and the rolling figure still includes the back half of a record 2025.',
            ),
            array(
                'q' => 'Do these figures include car dealers?',
                'a' => 'No. This page counts SIC group 452, the maintenance and repair of motor vehicles. Selling vehicles is SIC 451 and selling parts is SIC 453. Both are counted separately, and both are different businesses from a repair workshop.',
            ),
            array(
                'q' => 'Are electric vehicles causing garage insolvencies?',
                'a' => 'The parc data does not support that as the current cause. SMMT put zero-emission vehicles at around one in 22 on UK roads, so most cars still have an engine. The nearer-term difficulty is that tooling and training for electric work must be paid for years before enough of that work arrives.',
            ),
            array(
                'q' => 'What is the most common insolvency procedure for garages?',
                'a' => 'Creditors\' voluntary liquidation, at 260 of the 293 garage insolvencies in 2025, or 88.7%. That is the highest CVL share of any sector we cover, and it reflects how little there usually is to rescue in an independent garage.',
            ),
        );
        $mot_faq_main_entities = array();
        foreach ( $mot_faq_items as $item ) {
            $mot_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Motor Vehicle Repair Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for motor vehicle repair and maintenance businesses (SIC group 452), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023, annual figures from 2016, the split by insolvency procedure, and comparison with vehicle sales (SIC 451) and the motor trade overall (SIC 45). Covers independent garages, workshops, MOT centres, bodyshops and tyre and exhaust fitters. Excludes the sale of motor vehicles (SIC 451) and of parts and accessories (SIC 453), which are separate businesses. Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-05-31',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-may-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons, procedure shares and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 452. The industry total is published monthly (Table 1c); the procedure-split breakdown is published quarterly.',
                'keywords'        => 'motor vehicle repair insolvency, garage insolvency statistics, garage insolvencies 2026, SIC 452 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Motor vehicle repair company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Insolvency procedure (CVL, compulsory liquidation, administration, CVA, receivership)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $mot_faq_main_entities,
            ),
        );
    }

    if ( 'cleaning-company-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/cleaning-company-insolvency-statistics/' );
        $cln_faq_items = array(
            array(
                'q' => 'How many UK cleaning companies become insolvent each year?',
                'a' => '172 cleaning contractors entered insolvency in England and Wales in 2025, the same as in 2024 and just above the 171 in 2023. The pre-pandemic figure was 90 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are cleaning company insolvencies rising in 2026?',
                'a' => 'No. There were 59 insolvencies between January and May 2026 and 59 in the same months of 2025, exactly flat. The rolling 12-month total did rise 6.8% to 172, so the sector is not improving either, at a time when the wider building-services division fell 16.8%.',
            ),
            array(
                'q' => 'Why are cleaning insolvencies flat when other sectors are improving?',
                'a' => 'Cleaning is close to a pure labour business, so it feels wage and employer National Insurance changes more directly than trades with materials or assets to trim. Its neighbours in the same division improved sharply over the same months: landscaping down 30.2% and facilities support down 31.6%.',
            ),
            array(
                'q' => 'Do these figures include domestic cleaners?',
                'a' => 'Not generally. This page counts SIC group 812, cleaning activities, which is mainly commercial and industrial building cleaning. Waste collection and landscaping are separate SIC codes and are excluded.',
            ),
            array(
                'q' => 'What is the most common insolvency procedure for cleaning companies?',
                'a' => 'Creditors\' voluntary liquidation, at 152 of the 172 cleaning insolvencies in 2025, or 88.4%. Administrations are almost unheard of in this trade, at just 2 cases, because there is rarely anything a buyer would pay for.',
            ),
        );
        $cln_faq_main_entities = array();
        foreach ( $cln_faq_items as $item ) {
            $cln_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Cleaning Company Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for cleaning contractors (SIC group 812), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023, annual figures from 2016, the split by insolvency procedure, and comparison with landscape services (SIC 813), combined facilities support (SIC 811) and building and landscape services overall (SIC 81). Covers general and specialist cleaning of buildings and industrial premises, including window cleaning. Excludes agency-provided domestic cleaning, waste collection and landscaping, which are recorded separately. Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-05-31',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-may-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons, procedure shares and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 812. The industry total is published monthly (Table 1c); the procedure-split breakdown is published quarterly.',
                'keywords'        => 'cleaning company insolvency, cleaning contractor insolvency statistics, cleaning insolvencies 2026, SIC 812 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Cleaning contractor company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Insolvency procedure (CVL, compulsory liquidation, administration, CVA, receivership)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $cln_faq_main_entities,
            ),
        );
    }

    if ( 'hotel-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/hotel-insolvency-statistics/' );
        $hot_faq_items = array(
            array(
                'q' => 'How many UK hotels become insolvent each year?',
                'a' => '153 hotel and similar accommodation companies entered insolvency in England and Wales in 2025, the highest in the series and up from 136 in 2024. The 2019 figure was 144. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are hotel insolvencies falling in 2026?',
                'a' => 'Yes. There were 68 insolvencies between January and May 2026 against 76 in the same months of 2025, down 10.5%, and the rolling 12-month total fell 5.8% to 145. The caveat is that accommodation as a whole fell 23.1% over the same period, so hotels are recovering more slowly than the rest of the trade.',
            ),
            array(
                'q' => 'Do these figures include pubs, restaurants and Airbnb-style lets?',
                'a' => 'No. This page counts SIC group 551, hotels and similar short-stay accommodation. Restaurants and pubs are SIC 561 and 563, and self-catering and holiday lets are SIC 552. All are counted separately.',
            ),
            array(
                'q' => 'Why are hotel insolvencies compared with 2019 less meaningful?',
                'a' => 'Because 2019 was not a normal year for hotels. Insolvencies jumped from 96 in 2018 to 144 in 2019, before the pandemic. Hotels also did not get the quiet 2020 that most sectors had: company insolvencies across the economy fell 26.4% that year while hotels went from 144 to 143.',
            ),
            array(
                'q' => 'What is the most common insolvency procedure for hotels?',
                'a' => 'Creditors\' voluntary liquidation, at 115 of the 153 hotel insolvencies in 2025. But administrations are notable at 9.8%, the highest share of any sector we cover, because a hotel is a real asset that a buyer may want.',
            ),
        );
        $hot_faq_main_entities = array();
        foreach ( $hot_faq_items as $item ) {
            $hot_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Hotel Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for hotels and similar accommodation (SIC group 551), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023, annual figures from 2016, the split by insolvency procedure, and comparison with holiday and short-stay lets (SIC 552), accommodation overall (SIC 55) and restaurants (SIC 561). Covers hotels, motels and similar short-stay accommodation with daily housekeeping. Excludes restaurants and pubs (SIC 561 and 563) and self-catering, holiday and short-stay lets (SIC 552). Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-05-31',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-may-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons, procedure shares and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 551. The industry total is published monthly (Table 1c); the procedure-split breakdown is published quarterly.',
                'keywords'        => 'hotel insolvency, hotel insolvency statistics, hotel insolvencies 2026, SIC 551 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Hotel company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Insolvency procedure (CVL, compulsory liquidation, administration, CVA, receivership)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $hot_faq_main_entities,
            ),
        );
    }

    if ( 'estate-agency-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/estate-agency-insolvency-statistics/' );
        $ea_faq_items = array(
            array(
                'q' => 'How many estate agency businesses became insolvent in 2025?',
                'a' => '233 businesses in SIC group 683, estate agencies and fee-based property managers in England and Wales, entered formal insolvency during 2025, down from 272 in 2024 but still 48% above the 2019 total of 157.',
            ),
            array(
                'q' => 'Are estate agency insolvencies rising or falling?',
                'a' => 'Falling. Insolvencies peaked in 2024, fell 14% during 2025, and the decline continued into 2026: there were 86 cases between January and May 2026, 22% fewer than the 110 recorded in the same period of 2025.',
            ),
            array(
                'q' => 'Do the figures include letting agents and property managers?',
                'a' => 'Yes. SIC group 683 combines real estate agencies with businesses that manage property for clients on a fee or contract basis, including letting agents. The two cannot be separated in the published data.',
            ),
            array(
                'q' => 'Do the figures include property developers and landlords?',
                'a' => 'No. Companies that mainly buy, sell, own or let property in their own name are recorded under separate SIC groups (681 and 682) and are excluded from the totals on this page.',
            ),
            array(
                'q' => 'Are the figures UK-wide?',
                'a' => 'No. The headline figures cover England and Wales only. Scotland is reported separately: 9 insolvencies in 2025 and 1 in the first five months of 2026, and there is no comparable Northern Ireland industry series, so a complete UK total cannot be calculated.',
            ),
            array(
                'q' => 'Which insolvency procedure is most common in the sector?',
                'a' => 'Creditors’ voluntary liquidation. It accounted for 166 of the 233 insolvencies recorded in 2025, 71% of the total, though compulsory liquidations, usually creditor-driven, rose from 54 to 60 over the same period.',
            ),
        );
        $ea_faq_main_entities = array();
        foreach ( $ea_faq_items as $item ) {
            $ea_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Estate Agency Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for estate agencies and fee-based property management businesses (SIC group 683), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016. Excludes companies that mainly buy, sell, own or let property in their own name (SIC groups 681 and 682). Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-05-31',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-may-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and procedure shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 683. The industry total is published monthly (Table 1c); the procedure-split breakdown is published quarterly.',
                'keywords'        => 'estate agency insolvency, estate agent insolvencies, estate agency insolvencies 2026, SIC 683 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Estate agency and property management company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Insolvency procedure (CVL, compulsory liquidation, administration, CVA, receivership)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $ea_faq_main_entities,
            ),
        );
    }

    return null;
}

/**
 * Flagship site-alignment CSS: brings /data/uk-insolvency-statistics/ into
 * line with the rest of companydebt.com (Arial, the site's full-bleed pale
 * blue hero band, one spacing rhythm), per docs/data-hub/design-brief-2026-07.md
 * and the Claude Design handoff. Strictly gated to this one slug: every
 * /data/ page shares body.page-template-data-hub-template, so this must NOT
 * become a hub-wide stylesheet by accident — the other 17 pages have not been
 * through this alignment pass yet.
 *
 * Echoed in <head> deliberately, not at end-of-body: the design handoff notes
 * an observed FOUC (the page painted with the old layout, then reflowed) when
 * this class of override CSS was appended late. Mirrors the pattern already
 * used for the JSON-LD schema below (cd_datahub_current_slug() gate).
 */
add_action( 'wp_head', function() {
    if ( 'uk-insolvency-statistics' !== cd_datahub_current_slug() ) {
        return;
    }
    ?>
<style id="cd-site-alignment">
/* 1 -- FONT. Arial, matching body.cd-ttt-design on the rest of the site. */
html body.page-template-data-hub-template .cd-data-hub,
html body.page-template-data-hub-template .cd-data-hub h1,
html body.page-template-data-hub-template .cd-data-hub h2,
html body.page-template-data-hub-template .cd-data-hub h3,
html body.page-template-data-hub-template .cd-data-hub .cd-hero h1,
html body.page-template-data-hub-template .cd-data-hub .cd-section-head h2,
html body.page-template-data-hub-template .cd-data-hub .cd-cta h2,
html body.page-template-data-hub-template .cd-data-hub .cd-brand__name,
html body.page-template-data-hub-template .cd-data-hub .cd-brand__mark {
  font-family: Arial, Helvetica, sans-serif !important;
}
/* H1 to the site scale, clamped so it wraps naturally on mobile. */
html body.page-template-data-hub-template .main-content .cd-data-hub .cd-hero h1,
html body.page-template-data-hub-template .main-content .cd-data-hub h1 {
  font-size: clamp(30px, 5vw, 48px) !important;
  line-height: 1.08 !important;
  letter-spacing: -0.02em !important;
  max-width: 800px !important;
}
/* 2 -- HERO BAND. Copies the site mechanism (.col-12.page-header::before): a
   100vw full-bleed pale blue band. body sets overflow-x:hidden, so 100vw
   cannot introduce horizontal scroll. */
html body.page-template-data-hub-template .main-content .cd-data-hub .cd-hero {
  position: relative;
  padding-top: 35px !important;
  padding-bottom: 54px !important;
  margin-bottom: 24px !important;
}
html body.page-template-data-hub-template .main-content .cd-data-hub .cd-hero::before {
  content: '';
  position: absolute;
  top: 0; bottom: 0; left: 50%;
  width: 100vw; margin-left: -50vw;
  background: #f4f7fe;
  z-index: 0;
}
html body.page-template-data-hub-template .main-content .cd-data-hub .cd-hero > * {
  position: relative;
  z-index: 1;
}
/* 3 -- SPACING RHYTHM. One rhythm across the page. */
html body.page-template-data-hub-template .main-content .cd-data-hub {
  --cd-space-section: 104px;
  --cd-space-section-small: 64px;
}
html body.page-template-data-hub-template .main-content .cd-data-hub .cd-section {
  margin-top: 104px !important;
}
html body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-small {
  margin-top: 64px !important;
}
/* 4 -- BREADCRUMB. The theme's .row is display:flex, so .col-12.page-header
   collapses to min-content and the trail wraps onto multiple lines. Restore
   it to full row width and seat it on the same pale-blue band as the hero,
   matching the rest of the site. */
html body.page-template-data-hub-template .row > .col-12.page-header {
  flex: 1 1 100% !important;
  width: 100% !important;
  min-width: 0 !important;
  max-width: none !important;
  position: relative !important;
  margin-bottom: 0 !important;
  padding-top: 28px !important;
  padding-bottom: 18px !important;
  padding-left: max(24px, calc(50vw - 520px)) !important;
  padding-right: max(24px, calc(50vw - 520px)) !important;
}
html body.page-template-data-hub-template .row > .col-12.page-header::before {
  content: '';
  position: absolute;
  top: 0; bottom: 0; left: 50%;
  width: 100vw; margin-left: -50vw;
  background: #f4f7fe;
  z-index: 0;
}
html body.page-template-data-hub-template .row > .col-12.page-header > * {
  position: relative;
  z-index: 1;
}
html body.page-template-data-hub-template .main-content .cd-data-hub .cd-hero {
  padding-top: 8px !important;
}
html body.page-template-data-hub-template .page-header .breadcrumbs {
  white-space: normal !important;
}
</style>
    <?php
}, 30 );

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

/**
 * Disable WP Schema Pro's output on data-hub pages. These pages carry a curated
 * Dataset / FAQ / ItemList graph here plus Yoast's WebPage + BreadcrumbList, so
 * Schema Pro's generic (and mistyped) Article/WebPage is redundant. These are
 * the plugin's own gating filters (see class-bsf-aiosrs-pro-markup.php). The
 * per-post path is served from a cached blob, so the cache for these posts must
 * be cleared once for this to take effect (scripts/datahub/clear_schema_pro_cache.py).
 */
add_filter( 'wp_schema_pro_schema_enabled', function( $enabled, $post_id, $schema_type ) {
    return ( '' !== cd_datahub_current_slug() ) ? false : $enabled;
}, 99, 3 );

add_filter( 'wp_schema_pro_global_schema_enabled', function( $enabled, $post_id, $type ) {
    return ( '' !== cd_datahub_current_slug() ) ? false : $enabled;
}, 99, 3 );
