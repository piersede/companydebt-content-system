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
        'it-consultancy-insolvency-statistics',
        'management-consultancy-insolvency-statistics',
        'architectural-engineering-insolvency-statistics',
        'personal-care-services-insolvency-statistics',
        'sports-facility-insolvency-statistics',
        'medical-dental-practice-insolvency-statistics',
        'creative-arts-entertainment-insolvency-statistics',
        'amusement-recreation-insolvency-statistics',
        'real-estate-letting-investment-insolvency-statistics',
        'freight-forwarding-logistics-insolvency-statistics',
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
            'desc'  => '75 furniture manufacturers entered insolvency between January and June 2026, edging up from 73 a year earlier while manufacturing overall fell 8.5%. Latest figures.',
        ),
        'restaurant-insolvency-statistics' => array(
            'title' => 'UK Restaurant Insolvency Statistics 2026 | Company Debt',
            'desc'  => '1,011 restaurant and mobile food businesses entered insolvency between January and June 2026, down from 1,078 a year earlier. See the latest restaurant insolvency figures.',
        ),
        'road-haulage-insolvency-statistics' => array(
            'title' => 'UK Road Haulage Insolvency Statistics 2026 | Company Debt',
            'desc'  => '184 road haulage and removals companies entered insolvency between January and June 2026, down from 220 a year earlier. See the latest haulage insolvency figures.',
        ),
        'recruitment-agency-insolvency-statistics' => array(
            'title' => 'UK Recruitment Agency Insolvency Statistics 2026',
            'desc'  => '136 recruitment agencies entered insolvency between January and June 2026, down 24.9% from a record 2025, while temporary staffing rose. Latest figures.',
        ),
        'temporary-staffing-agency-insolvency-statistics' => array(
            'title' => 'UK Temporary Staffing Agency Insolvency Statistics 2026',
            'desc'  => 'Latest temporary staffing agency insolvency figures for England and Wales, including 2026 trends, annual data, recruitment-sector comparisons and methodology.',
        ),
        'motor-vehicle-repair-insolvency-statistics' => array(
            'title' => 'UK Garage Insolvency Statistics 2026 | Motor Vehicle Repair',
            'desc'  => '293 garages entered insolvency in 2025, a record, and 140 in the first half of 2026. See the latest motor vehicle repair insolvency figures.',
        ),
        'cleaning-company-insolvency-statistics' => array(
            'title' => 'UK Cleaning Company Insolvency Statistics 2026',
            'desc'  => '69 cleaning contractors entered insolvency between January and June 2026, down 6.8% year to date, while the rest of building services improved far faster.',
        ),
        'hotel-insolvency-statistics' => array(
            'title' => 'UK Hotel Insolvency Statistics 2026 | Company Debt',
            'desc'  => '80 hotels entered insolvency between January and June 2026, down 10.1%, but 2025 was the worst year on record at 154. See the latest hotel figures.',
        ),
        'estate-agency-insolvency-statistics' => array(
            'title' => 'UK Estate Agency Insolvency Statistics 2026',
            'desc'  => 'Latest estate agency insolvency statistics for England and Wales, including 101 cases in the first half of 2026, rolling totals, procedures and SIC 683 trends.',
        ),
        'it-consultancy-insolvency-statistics' => array(
            'title' => 'UK IT Consultancy Insolvency Statistics 2026 | Company Debt',
            'desc'  => '900 IT and computer consultancy companies entered insolvency in England and Wales in 2025, the second-highest year on record. See the latest figures.',
        ),
        'management-consultancy-insolvency-statistics' => array(
            'title' => 'UK Management Consultancy Insolvency Statistics 2026',
            'desc'  => '670 management consultancy companies entered insolvency in England and Wales in 2025, the second-highest year on record. See the latest figures.',
        ),
        'architectural-engineering-insolvency-statistics' => array(
            'title' => 'UK Architectural & Engineering Consultancy Insolvency Stats',
            'desc'  => '335 architectural and engineering consultancies entered insolvency in England and Wales in 2025, the fifth straight annual rise. See the latest figures.',
        ),
        'personal-care-services-insolvency-statistics' => array(
            'title' => 'UK Hair, Beauty & Personal Care Insolvency Statistics 2026',
            'desc'  => '993 hair, beauty and personal care businesses entered insolvency in England and Wales in 2025, down from a 2023 peak of 1,286. See the latest figures.',
        ),
        'sports-facility-insolvency-statistics' => array(
            'title' => 'UK Sports Club & Facility Insolvency Statistics 2026',
            'desc'  => '195 sports clubs and facilities entered insolvency in England and Wales in 2025, 29% above 2019, with 2026 already running ahead of last year.',
        ),
        'medical-dental-practice-insolvency-statistics' => array(
            'title' => 'UK Medical & Dental Practice Insolvency Statistics 2026',
            'desc'  => 'Medical and dental practice insolvencies rose 19.0% year to date in 2026, to 50 cases against 42 in the same months of 2025. See the latest figures.',
        ),
        'creative-arts-entertainment-insolvency-statistics' => array(
            'title' => 'UK Creative, Arts & Entertainment Insolvency Statistics 2026',
            'desc'  => 'Creative, arts and entertainment insolvencies rose 17.2% year to date in 2026, faster than every other trade in its section. See the latest figures.',
        ),
        'amusement-recreation-insolvency-statistics' => array(
            'title' => 'UK Amusement & Recreation Insolvency Statistics 2026',
            'desc'  => '123 amusement and recreation businesses entered insolvency in England and Wales in 2025, a series peak, with 2026 showing the first pull-back.',
        ),
        'real-estate-letting-investment-insolvency-statistics' => array(
            'title' => 'UK Real Estate Letting & Investment Insolvency Stats 2026',
            'desc'  => 'Real estate letting and investment insolvencies eased 9.9% in 2026 even as the wider real estate section spiked 50.8%. See why, and the real figures.',
        ),
        'freight-forwarding-logistics-insolvency-statistics' => array(
            'title' => 'UK Freight Forwarding & Logistics Insolvency Statistics 2026',
            'desc'  => 'Freight forwarding and logistics insolvencies are still running above last year on a rolling basis, even as road haulage falls sharply. Latest figures.',
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
            array( 'IT Consultancy Insolvency Statistics', home_url( '/data/it-consultancy-insolvency-statistics/' ) ),
            array( 'Management Consultancy Insolvency Statistics', home_url( '/data/management-consultancy-insolvency-statistics/' ) ),
            array( 'Architectural and Engineering Consultancy Insolvency Statistics', home_url( '/data/architectural-engineering-insolvency-statistics/' ) ),
            array( 'Hair, Beauty and Personal Care Insolvency Statistics', home_url( '/data/personal-care-services-insolvency-statistics/' ) ),
            array( 'Sports Club and Facility Insolvency Statistics', home_url( '/data/sports-facility-insolvency-statistics/' ) ),
            array( 'Medical and Dental Practice Insolvency Statistics', home_url( '/data/medical-dental-practice-insolvency-statistics/' ) ),
            array( 'Creative, Arts and Entertainment Insolvency Statistics', home_url( '/data/creative-arts-entertainment-insolvency-statistics/' ) ),
            array( 'Amusement and Recreation Insolvency Statistics', home_url( '/data/amusement-recreation-insolvency-statistics/' ) ),
            array( 'Real Estate Letting and Investment Insolvency Statistics', home_url( '/data/real-estate-letting-investment-insolvency-statistics/' ) ),
            array( 'Freight Forwarding and Logistics Insolvency Statistics', home_url( '/data/freight-forwarding-logistics-insolvency-statistics/' ) ),
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
                'a' => 'Slightly. There were 75 insolvencies between January and June 2026 against 73 in the same months of 2025, up 2.7%, and the rolling 12-month total ticked up to 145. Manufacturing overall fell 8.5% over the same months.',
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
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
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
                'temporalCoverage' => '2016-01/2026-06',
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
                'temporalCoverage' => '2016-01/2026-06',
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
                'a' => 'Yes. There were 136 insolvencies between January and June 2026 against 181 in the same months of 2025, a fall of 24.9%, and the rolling 12-month total fell 9.6% to 300. The year-to-date fall is flattered by an unusually severe early 2025, so the rolling measure is the better guide.',
            ),
            array(
                'q' => 'Why are recruitment insolvencies falling while temporary staffing insolvencies rise?',
                'a' => 'Because employers have been hiring temporary staff instead of permanent ones. Permanent-placement insolvencies (SIC 781) fell 24.9% in the first half of 2026 while temporary employment agency insolvencies (SIC 782) rose 7.3%. The KPMG and REC UK Report on Jobs found temp billings rising at their quickest rate since April 2023.',
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
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
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
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
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
                'a' => 'The two measures are converging. There were 140 insolvencies between January and June 2026 against 150 a year earlier, down 6.7%, and the rolling 12-month total is now essentially flat at 283. The improvement is recent, and the rolling figure still includes the back half of a record 2025.',
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
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
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
                'a' => 'Barely easing. There were 69 insolvencies between January and June 2026 against 74 in the same months of 2025, down 6.8%. The rolling 12-month total rose 7.7% to 167, so the sector is still lagging badly at a time when the wider building-services division fell 22.0%.',
            ),
            array(
                'q' => 'Why are cleaning insolvencies lagging when other sectors are improving?',
                'a' => 'Cleaning is close to a pure labour business, so it feels wage and employer National Insurance changes more directly than trades with materials or assets to trim. Its neighbours in the same division improved sharply over the same months: landscaping down 33.3% and facilities support down 40.9%.',
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
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
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
                'a' => '154 hotel and similar accommodation companies entered insolvency in England and Wales in 2025, the highest in the series and up from 136 in 2024. The 2019 figure was 144. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are hotel insolvencies falling in 2026?',
                'a' => 'Yes. There were 80 insolvencies between January and June 2026 against 89 in the same months of 2025, down 10.1%, and the rolling 12-month total fell 4.6% to 145. The caveat is that accommodation as a whole fell 19.9% over the same period, so hotels are recovering more slowly than the rest of the trade.',
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
                'a' => 'Creditors\' voluntary liquidation, at 115 of the 154 hotel insolvencies in 2025. But administrations are notable at 9.8%, the highest share of any sector we cover, because a hotel is a real asset that a buyer may want.',
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
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
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
                'q' => 'How many estate agency and property-management businesses became insolvent in the first half of 2026?',
                'a' => '101 formal insolvencies in SIC 683 in England and Wales between January and June 2026, 30 fewer than the 131 recorded in the same period of 2025, a fall of 22.9%.',
            ),
            array(
                'q' => 'Are estate agency insolvencies rising or falling?',
                'a' => 'Falling. The first-half total was down 22.9%, and the rolling 12-month total fell 22.2%, from 261 to 203. The latest completed-year total nevertheless remained 48.4% above 2019.',
            ),
            array(
                'q' => 'Do the figures include letting agents and property managers?',
                'a' => 'Yes. SIC 683 combines real estate agencies with businesses managing property for clients on a fee or contract basis. The published monthly total does not split SIC 68310 (agencies) from SIC 68320 (fee-based management).',
            ),
            array(
                'q' => 'Was the 2026 increase in real estate insolvencies caused by estate agencies?',
                'a' => 'No. SIC 683 insolvencies fell from 131 to 101 in the first half of 2026. The increase across real estate overall was concentrated in SIC 681, buying and selling of own real estate, which rose from 116 to 363 cases.',
            ),
            array(
                'q' => 'Are the figures UK-wide?',
                'a' => 'No. The headline series covers England and Wales. Scotland recorded 2 SIC 683 insolvencies in both the first half of 2025 and the first half of 2026. There is no equivalent Northern Ireland three-digit monthly series, so a complete UK total cannot be calculated.',
            ),
            array(
                'q' => 'Which insolvency procedure is most common?',
                'a' => "Creditors' voluntary liquidation. CVLs accounted for 72 of the 101 SIC 683 insolvencies in the first half of 2026, 71.3% of the total.",
            ),
            array(
                'q' => 'Do these figures show the percentage of estate agencies that failed?',
                'a' => 'No. They are counts of formal insolvencies, not a failure rate. A reliable rate would require a matching denominator of active companies in the same SIC category, geography and period.',
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
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for estate agencies and fee-based property management businesses (SIC group 683), England and Wales: half-year and rolling 12-month totals, the monthly series from 2016 and annual figures from 2016, plus a comparison against SIC 681 (property trading) and SIC 682 (letting and investment) showing the 2026 real estate insolvency increase was concentrated in SIC 681, not estate agencies. Excludes companies that mainly buy, sell, own or let property in their own name (SIC groups 681 and 682). Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and procedure shares) from Insolvency Service supplementary industry Table A1b, identified via Companies House SIC group 683. The industry total and procedure-split breakdown in this release are both published quarterly.',
                'keywords'        => 'estate agency insolvency, estate agent insolvencies, estate agency insolvencies 2026, SIC 683 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Estate agency and property management company insolvencies (count)',
                    'Half-year percentage change',
                    'Rolling 12-month count',
                    'Insolvency procedure (CVL, compulsory liquidation, administration, CVA, receivership)',
                    'Peer-sector shares within real estate activities (SIC Division 68)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $ea_faq_main_entities,
            ),
        );
    }

    if ( 'it-consultancy-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/it-consultancy-insolvency-statistics/' );
        $itc_faq_items = array(
            array(
                'q' => 'How many UK IT and computer consultancies become insolvent each year?',
                'a' => '900 computer programming and consultancy companies entered insolvency in England and Wales in 2025, against 906 in 2024, the two highest years the sector has recorded. The pre-pandemic figure was 550 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are IT consultancy insolvencies rising in 2026?',
                'a' => 'No, they are easing slightly from a record high. There were 401 insolvencies between January and June 2026 against 443 in the same months of 2025, a fall of 9.5%, and the rolling 12-month total fell 2.5% to 858. The sector remains 64% above its 2019 level.',
            ),
            array(
                'q' => 'Does this include IT retailers, telecoms or data centre companies?',
                'a' => 'No. This page counts SIC group 620, computer programming, consultancy and related activities. Telecommunications, data processing and hosting, and other information-and-communication trades are recorded under separate SIC codes and counted elsewhere.',
            ),
            array(
                'q' => 'Why have IT consultancy insolvencies stayed high since the pandemic?',
                'a' => 'The sector saw a sharp rise in company formations from 2021 to 2023 as digital transformation spending and remote-work technology demand boomed. Insolvencies rose alongside that expansion and have not come back down as the market has cooled, sitting at 906 in 2024 and 900 in 2025.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $itc_faq_main_entities = array();
        foreach ( $itc_faq_items as $item ) {
            $itc_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK IT and Computer Consultancy Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for computer programming, consultancy and related activities (SIC group 620), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with data processing and hosting (SIC 631), other information services (SIC 639), publishing (SIC 581), other telecommunications (SIC 619) and information and communication overall (SIC J). Covers bespoke software development, systems integration and IT project consultancy sold to other businesses. Excludes telecommunications providers, data processing and hosting companies, and IT retailers. Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 620. The industry total is published monthly (Table 1c).',
                'keywords'        => 'IT consultancy insolvency, computer consultancy insolvency statistics, IT consultancy insolvencies 2026, SIC 620 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'IT and computer consultancy company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within information and communication (SIC J)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $itc_faq_main_entities,
            ),
        );
    }

    if ( 'management-consultancy-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/management-consultancy-insolvency-statistics/' );
        $mc_faq_items = array(
            array(
                'q' => 'How many UK management consultancies become insolvent each year?',
                'a' => '670 management consultancy companies entered insolvency in England and Wales in 2025, against 665 in 2024. The series peak was 708 in 2023, and the pre-pandemic figure was 398 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are management consultancy insolvencies rising in 2026?',
                'a' => 'The year-to-date count is down: 317 insolvencies between January and June 2026 against 332 in the same months of 2025, a fall of 4.5%. But the rolling 12-month total has ticked up 1.2% to 655, so the picture is a sector holding near its peak rather than clearly recovering.',
            ),
            array(
                'q' => 'Does this include accountants, lawyers or IT consultants?',
                'a' => 'No. This page counts SIC group 702, management consultancy activities. Accountancy, legal services, architectural and engineering consultancy, and IT consultancy are recorded under separate SIC codes and counted elsewhere.',
            ),
            array(
                'q' => 'Why are management consultancy insolvencies still so high?',
                'a' => 'Insolvencies nearly doubled between 2020 and the 2023 peak as the sector expanded rapidly on post-pandemic strategy, restructuring and digital-transformation work, and have not come down significantly since, holding at 665 in 2024 and 670 in 2025 against 398 in 2019.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $mc_faq_main_entities = array();
        foreach ( $mc_faq_items as $item ) {
            $mc_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Management Consultancy Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for management consultancy activities (SIC group 702), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with architectural and engineering consultancy (SIC 711), advertising (SIC 731), specialised design activities (SIC 741), other professional activities not elsewhere classified (SIC 749) and professional, scientific and technical activities overall (SIC M). Covers advice on strategy, organisation, marketing and operations sold to other organisations. Excludes accountancy, legal services, architectural and engineering consultancy, and IT consultancy. Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 702. The industry total is published monthly (Table 1c).',
                'keywords'        => 'management consultancy insolvency, consultancy insolvency statistics, management consultancy insolvencies 2026, SIC 702 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Management consultancy company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within professional, scientific and technical activities (SIC M)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $mc_faq_main_entities,
            ),
        );
    }

    if ( 'architectural-engineering-insolvency-statistics' === $slug ) {
        $page_url = home_url( '/data/architectural-engineering-insolvency-statistics/' );
        $ae_faq_items = array(
            array(
                'q' => 'How many UK architectural and engineering consultancies become insolvent each year?',
                'a' => '335 companies in SIC group 711 entered insolvency in England and Wales in 2025, the highest total on record and the fifth consecutive annual rise since 2020. The pre-pandemic figure was 182 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are architectural and engineering consultancy insolvencies still rising in 2026?',
                'a' => 'The year-to-date count is essentially flat, 141 insolvencies between January and June 2026 against 147 a year earlier. But the rolling 12-month total rose 5.8% to 329, one of the only genuine increases among the professional-services trades covered on this site, and the annual figure has not fallen in any year since 2020.',
            ),
            array(
                'q' => 'Does this include accountants, surveyors or IT consultants?',
                'a' => 'No. This page counts SIC group 711, architectural and engineering activities and related technical consultancy. Surveying, accountancy, legal services, management consultancy and IT consultancy are recorded under separate SIC codes.',
            ),
            array(
                'q' => 'Why do architectural and engineering consultancy insolvencies keep rising?',
                'a' => 'The trade has climbed every year since the 2020 low, from 140 to 335 in 2025. Contributing pressures include falling architect confidence in 2026, extended retrospective liability for older projects under the Building Safety Act 2022, and tightening professional indemnity insurance for higher-risk building work.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $ae_faq_main_entities = array();
        foreach ( $ae_faq_items as $item ) {
            $ae_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Architectural and Engineering Consultancy Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for architectural and engineering activities and related technical consultancy (SIC group 711), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with head offices (SIC 701), advertising (SIC 731), specialised design activities (SIC 741), other professional activities not elsewhere classified (SIC 749) and professional, scientific and technical activities overall (SIC M). Covers building design, structural and civil engineering, and related technical consultancy. Excludes surveying, accountancy, legal services, management consultancy and IT consultancy. Source: Insolvency Service and Companies House.',
                'url'              => $page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 711. The industry total is published monthly (Table 1c).',
                'keywords'        => 'architectural consultancy insolvency, engineering consultancy insolvency statistics, architect insolvencies 2026, SIC 711 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Architectural and engineering consultancy company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within professional, scientific and technical activities (SIC M)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $page_url . '#faq',
                'mainEntity' => $ae_faq_main_entities,
            ),
        );
    }

    if ( 'personal-care-services-insolvency-statistics' === $slug ) {
        $pc_page_url = home_url( '/data/personal-care-services-insolvency-statistics/' );
        $pc_faq_items = array(
            array(
                'q' => 'How many UK personal care and beauty businesses become insolvent each year?',
                'a' => '993 companies in SIC group 960, personal care and related services, entered insolvency in England and Wales in 2025, down from 1,065 in 2024 and well below the 2023 peak of 1,286. The pre-pandemic figure was 713 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are personal care services insolvencies falling in 2026?',
                'a' => 'Yes. There were 439 insolvencies between January and June 2026 against 521 in the same months of 2025, a fall of 15.7%, and the rolling 12-month total fell 11.6% to 911. Both measures have declined for two consecutive years from the 2023 peak.',
            ),
            array(
                'q' => 'Does this include gyms, dry cleaners or funeral directors?',
                'a' => 'Laundry and dry-cleaning services for individuals and funeral and related services are both included in this SIC group alongside hairdressing, beauty treatment and wellbeing activities such as spas. Gyms and sports facilities are recorded under a separate SIC code and are not included here.',
            ),
            array(
                'q' => 'Why did personal care services insolvencies spike after the pandemic?',
                'a' => 'Insolvencies nearly doubled from 682 in 2021 to 1,205 in 2022 as the trade reopened after repeated pandemic closures into a period of rapid cost inflation and a wave of new salons and studios, not all of which proved durable. The total has fallen in both years since the 2023 peak of 1,286.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $pc_faq_main_entities = array();
        foreach ( $pc_faq_items as $item ) {
            $pc_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Hair, Beauty and Personal Care Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for personal care and related service activities (SIC group 960), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016. Covers hairdressing and beauty treatment, physical wellbeing activities such as spas and saunas, funeral and related services, and laundry and dry-cleaning services for individuals, which cannot be split further in the published data. Excludes gyms and sports facilities, and industrial or commercial laundry and dry-cleaning services. Source: Insolvency Service and Companies House.',
                'url'              => $pc_page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes and rolling 12-month comparisons) from Insolvency Service company insolvency tables, identified via Companies House SIC group 960. The industry total is published monthly (Table 1c).',
                'keywords'        => 'hairdresser insolvency, beauty salon insolvency statistics, personal care insolvencies 2026, SIC 960 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Personal care company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $pc_page_url . '#faq',
                'mainEntity' => $pc_faq_main_entities,
            ),
        );
    }

    if ( 'sports-facility-insolvency-statistics' === $slug ) {
        $sf_page_url = home_url( '/data/sports-facility-insolvency-statistics/' );
        $sf_faq_items = array(
            array(
                'q' => 'How many UK sports clubs and facilities become insolvent each year?',
                'a' => '195 companies in SIC group 931, sports activities, entered insolvency in England and Wales in both 2024 and 2025, below the 2023 peak of 236 but 29% above the 151 recorded in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are sports club and facility insolvencies rising in 2026?',
                'a' => 'They are ticking up after two flat years. There were 96 insolvencies between January and June 2026 against 90 in the same months of 2025, a rise of 6.7%, and the rolling 12-month total rose 5.8% to 201.',
            ),
            array(
                'q' => 'Does this include theme parks, arcades or museums?',
                'a' => 'No. This page counts SIC group 931, sports activities. Amusement and recreation activities such as theme parks and arcades, and cultural activities such as museums and libraries, are recorded under separate SIC codes within the same section and counted elsewhere.',
            ),
            array(
                'q' => 'Why are sports club and facility insolvencies still elevated?',
                'a' => 'Energy costs are a major factor: swimming pools and leisure facilities are among the most energy-intensive premises in the economy, and utility cost rises have contributed to dozens of local authority leisure centre closures since 2021. Local authority budget pressure and competition from low-cost gym chains add to the squeeze.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $sf_faq_main_entities = array();
        foreach ( $sf_faq_items as $item ) {
            $sf_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Sports Club and Facility Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for sports activities (SIC group 931), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with creative, arts and entertainment activities (SIC 900), amusement and recreation activities (SIC 932), libraries, archives and museums (SIC 910), gambling and betting activities (SIC 920) and arts, entertainment and recreation overall (SIC R). Covers the operation of sports facilities and leisure centres, sports clubs, and fitness facilities such as gyms. Excludes theme parks, arcades, museums and libraries. Source: Insolvency Service and Companies House.',
                'url'              => $sf_page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 931. The industry total is published monthly (Table 1c).',
                'keywords'        => 'gym insolvency, sports club insolvency statistics, leisure centre insolvencies 2026, SIC 931 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Sports club and facility company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within arts, entertainment and recreation (SIC R)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $sf_page_url . '#faq',
                'mainEntity' => $sf_faq_main_entities,
            ),
        );
    }

    if ( 'medical-dental-practice-insolvency-statistics' === $slug ) {
        $md_page_url = home_url( '/data/medical-dental-practice-insolvency-statistics/' );
        $md_faq_items = array(
            array(
                'q' => 'How many UK medical and dental practices become insolvent each year?',
                'a' => '93 companies in SIC group 862, medical and dental practice activities, entered insolvency in England and Wales in 2025, down slightly from the series high of 106 in 2024 but 33% above the 70 recorded in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are medical and dental practice insolvencies rising in 2026?',
                'a' => 'Yes, though less sharply than earlier in the year. There were 50 insolvencies between January and June 2026 against 42 in the same months of 2025, a rise of 19.0%, and the rolling 12-month total rose 11.0% to 101. This is a small sector, so the exact percentage should be read with some caution, but the direction is consistent across every measure.',
            ),
            array(
                'q' => 'Does this include hospitals or care homes?',
                'a' => 'No. This page counts SIC group 862, medical and dental practice activities. Hospitals, other human health activities, and residential and social care activities are recorded under separate SIC codes within the same section.',
            ),
            array(
                'q' => 'Why are medical and dental practice insolvencies rising?',
                'a' => 'NHS dentistry has seen over 1,000 practices hand back NHS contracts in 2023 alone, with a further contract reform in April 2026 accelerating the shift away from NHS work. The GP partnership model is under similar strain, with 1,470 practices closed or merged since 2015 and rising staff and National Insurance costs adding pressure across primary care.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $md_faq_main_entities = array();
        foreach ( $md_faq_items as $item ) {
            $md_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Medical and Dental Practice Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for medical and dental practice activities (SIC group 862), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with hospital activities (SIC 861), other human health activities (SIC 869), other residential care activities (SIC 879), social work without accommodation for the elderly and disabled (SIC 881) and human health and social work activities overall (SIC Q). Covers general and specialist medical and dental practice, whether NHS, private or mixed. Excludes hospitals and residential or social care activities. Source: Insolvency Service and Companies House.',
                'url'              => $md_page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 862. The industry total is published monthly (Table 1c).',
                'keywords'        => 'medical practice insolvency, dental practice insolvency statistics, GP practice insolvencies 2026, SIC 862 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Medical and dental practice company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within human health and social work activities (SIC Q)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $md_page_url . '#faq',
                'mainEntity' => $md_faq_main_entities,
            ),
        );
    }

    if ( 'creative-arts-entertainment-insolvency-statistics' === $slug ) {
        $ca_page_url = home_url( '/data/creative-arts-entertainment-insolvency-statistics/' );
        $ca_faq_items = array(
            array(
                'q' => 'How many UK creative, arts and entertainment businesses become insolvent each year?',
                'a' => '129 companies in SIC group 900, creative, arts and entertainment activities, entered insolvency in England and Wales in 2025, up from 123 in 2024. The series peak was 144 in 2023, and the pre-pandemic figure was 78 in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are creative and arts insolvencies rising in 2026?',
                'a' => 'Yes, sharply. There were 68 insolvencies between January and June 2026 against 58 in the same months of 2025, a rise of 17.2%, and the rolling 12-month total rose 14.9% to 139. Both measures are rising several times faster than the wider arts, entertainment and recreation section.',
            ),
            array(
                'q' => 'Does this include sports clubs, theme parks or museums?',
                'a' => 'No. This page counts SIC group 900, creative, arts and entertainment activities, covering performing arts, artistic creation and arts venues such as theatres. Sports activities, amusement and recreation activities, and museums and libraries are recorded under separate SIC codes within the same section.',
            ),
            array(
                'q' => 'Why are creative and arts insolvencies rising so fast?',
                'a' => 'Grassroots music and performance venues are under acute pressure from the 2026 business rates revaluation, estimated to put over 350 grassroots music venues at risk, alongside employer National Insurance changes that have contributed to a reported 19% workforce contraction across the grassroots venue sector in a single year.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $ca_faq_main_entities = array();
        foreach ( $ca_faq_items as $item ) {
            $ca_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Creative, Arts and Entertainment Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for creative, arts and entertainment activities (SIC group 900), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with sports activities (SIC 931), amusement and recreation activities (SIC 932), libraries, archives and museums (SIC 910), gambling and betting activities (SIC 920) and arts, entertainment and recreation overall (SIC R). Covers performing arts, artistic creation and the operation of arts facilities such as theatres and concert venues. Excludes sports facilities, theme parks and arcades, and museums and libraries. Source: Insolvency Service and Companies House.',
                'url'              => $ca_page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 900. The industry total is published monthly (Table 1c).',
                'keywords'        => 'creative industries insolvency, arts venue insolvency statistics, music venue insolvencies 2026, SIC 900 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Creative, arts and entertainment company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within arts, entertainment and recreation (SIC R)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $ca_page_url . '#faq',
                'mainEntity' => $ca_faq_main_entities,
            ),
        );
    }

    if ( 'amusement-recreation-insolvency-statistics' === $slug ) {
        $ar_page_url = home_url( '/data/amusement-recreation-insolvency-statistics/' );
        $ar_faq_items = array(
            array(
                'q' => 'How many UK amusement and recreation businesses become insolvent each year?',
                'a' => '123 companies in SIC group 932, amusement and recreation activities, entered insolvency in England and Wales in 2025, the series peak and the third consecutive annual rise, 38% above the 89 recorded in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are amusement and recreation insolvencies still rising in 2026?',
                'a' => 'No, the trend has paused. There were 50 insolvencies between January and June 2026 against 60 in the same months of 2025, a fall of 16.7%, and the rolling 12-month total fell 3.4% to 113, the first sustained fall since the three-year rise to 2025 began.',
            ),
            array(
                'q' => 'Does this include sports clubs, museums or creative venues?',
                'a' => 'No. This page counts SIC group 932, amusement and recreation activities: theme parks, amusement arcades and similar attractions. Sports facilities, creative and performing arts venues, and museums and libraries are recorded under separate SIC codes within the same section.',
            ),
            array(
                'q' => 'Why did amusement and recreation insolvencies rise for three years to 2025?',
                'a' => 'Visitor numbers across the wider attractions sector remain below 2019 levels even as they recover, with growth slowing rather than accelerating. Rising employer National Insurance and National Minimum Wage costs have, in the industry\'s own assessment, wiped out planned surpluses at many attractions, on top of sector-specific pressures such as a proposed gaming duty rise threatening seaside arcades.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $ar_faq_main_entities = array();
        foreach ( $ar_faq_items as $item ) {
            $ar_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Amusement and Recreation Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for amusement and recreation activities (SIC group 932), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with creative, arts and entertainment activities (SIC 900), sports activities (SIC 931), libraries, archives and museums (SIC 910), gambling and betting activities (SIC 920) and arts, entertainment and recreation overall (SIC R). Covers theme parks, amusement arcades, funfairs and similar attractions. Excludes sports facilities, creative and performing arts venues, and museums and libraries. Source: Insolvency Service and Companies House.',
                'url'              => $ar_page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 932. The industry total is published monthly (Table 1c).',
                'keywords'        => 'amusement park insolvency, theme park insolvency statistics, arcade insolvencies 2026, SIC 932 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Amusement and recreation company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within arts, entertainment and recreation (SIC R)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $ar_page_url . '#faq',
                'mainEntity' => $ar_faq_main_entities,
            ),
        );
    }

    if ( 'real-estate-letting-investment-insolvency-statistics' === $slug ) {
        $rl_page_url = home_url( '/data/real-estate-letting-investment-insolvency-statistics/' );
        $rl_faq_items = array(
            array(
                'q' => 'How many UK real estate letting and investment companies become insolvent each year?',
                'a' => '289 companies in SIC group 682, real estate letting and investment, entered insolvency in England and Wales in 2025, a series high, 62% above the 179 recorded in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are real estate letting and investment insolvencies rising in 2026?',
                'a' => "No, this trade's own figures are down slightly: 136 insolvencies between January and June 2026 against 151 a year earlier, down 9.9%, and the rolling 12-month total down a modest 2.1%. The real estate section as a whole shows a much larger rise, but that is driven almost entirely by a separate trade.",
            ),
            array(
                'q' => 'Why does the real estate section total look so much worse than this page?',
                'a' => 'The Insolvency Service flagged around 200 connected real estate companies entering administration together across March and April 2026. Our data show that spike was concentrated in companies that buy and sell property in their own name, SIC 681, 222 cases across those two months, rather than in letting and investment companies, SIC 682, 55 cases, or estate agencies, SIC 683, 35 cases.',
            ),
            array(
                'q' => 'Does this include estate agents or property developers?',
                'a' => 'No. This page counts SIC group 682, companies that rent out property they own or lease. Estate agencies acting for clients on a fee basis (SIC 683) and companies that buy and sell property in their own name (SIC 681) are recorded under separate codes.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $rl_faq_main_entities = array();
        foreach ( $rl_faq_items as $item ) {
            $rl_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Real Estate Letting and Investment Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for real estate letting and investment activities (SIC group 682), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016. Covers commercial and residential landlords and property-investment companies that rent out property they own or lease. Excludes companies that buy and sell property in their own name (SIC 681) and estate agencies acting for clients on a fee basis (SIC 683). Includes a breakdown of the March-April 2026 real estate administration spike by SIC group, showing it was concentrated in SIC 681, not this trade. Source: Insolvency Service and Companies House.',
                'url'              => $rl_page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes and rolling 12-month comparisons) from Insolvency Service company insolvency tables, identified via Companies House SIC group 682. The industry total is published monthly (Table 1c).',
                'keywords'        => 'landlord insolvency, property investment company insolvency statistics, real estate letting insolvencies 2026, SIC 682 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Real estate letting and investment company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $rl_page_url . '#faq',
                'mainEntity' => $rl_faq_main_entities,
            ),
        );
    }

    if ( 'freight-forwarding-logistics-insolvency-statistics' === $slug ) {
        $ff_page_url = home_url( '/data/freight-forwarding-logistics-insolvency-statistics/' );
        $ff_faq_items = array(
            array(
                'q' => 'How many UK freight-forwarding and logistics-support companies become insolvent each year?',
                'a' => '105 companies in SIC group 522, support activities for transportation, entered insolvency in England and Wales in 2025, easing from the 2023 peak of 122 but 54% above the 68 recorded in 2019. Source: Insolvency Service, Table 1c.',
            ),
            array(
                'q' => 'Are freight-forwarding insolvencies rising or falling in 2026?',
                'a' => 'Mixed. The year-to-date figure is down slightly, 45 insolvencies against 47 a year earlier, while the rolling 12-month total rose 9.6%. Both measures are moving against the wider transport and storage section, which fell over the same period.',
            ),
            array(
                'q' => 'Does this include road hauliers or courier companies?',
                'a' => 'No. This page counts SIC group 522, freight forwarding, cargo handling, customs clearance and related logistics support. Road haulage (SIC 494), warehousing and storage (SIC 521), and postal and courier activities are recorded under separate SIC codes within the same section.',
            ),
            array(
                'q' => 'Why are freight-forwarding insolvencies holding up while road haulage falls?',
                'a' => 'Two major disruptions landed on this trade specifically: the continued rerouting of container shipping around the Cape of Good Hope since the Red Sea crisis, adding cost and complexity to every booking, and a new customs declaration regime for EU imports that went live in July 2026. Both create work for forwarders but also compliance risk that smaller operators can struggle to absorb.',
            ),
            array(
                'q' => 'Do the figures cover the whole UK?',
                'a' => 'No. The industry breakdown in Table 1c covers England and Wales only. Scotland and Northern Ireland run separate insolvency regimes and are reported separately.',
            ),
        );
        $ff_faq_main_entities = array();
        foreach ( $ff_faq_items as $item ) {
            $ff_faq_main_entities[] = array(
                '@type'          => 'Question',
                'name'           => $item['q'],
                'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $item['a'] ),
            );
        }
        return array(
            array(
                '@type'            => 'Dataset',
                'name'             => 'UK Freight Forwarding and Logistics Insolvency Statistics',
                'description'      => 'Company Debt analysis of Insolvency Service company insolvency data for support activities for transportation (SIC group 522), England and Wales: year-to-date and rolling 12-month totals, the monthly series from 2023 and annual figures from 2016, and comparison with road haulage (SIC 494), warehousing and storage (SIC 521), other postal and courier activities (SIC 532), other passenger land transport (SIC 493) and transportation and storage overall (SIC H). Covers freight forwarding, cargo handling, customs clearance and related logistics coordination. Excludes road haulage, warehousing, and postal and courier activities. Source: Insolvency Service and Companies House.',
                'url'              => $ff_page_url,
                'creator'         => $org_ref,
                'publisher'       => $org_ref,
                'spatialCoverage' => array( '@type' => 'Place', 'name' => 'England and Wales' ),
                'temporalCoverage' => '2016-01-01/2026-06-30',
                'datePublished'   => $published,
                'dateModified'    => $modified,
                'isBasedOn'       => 'https://www.gov.uk/government/statistics/company-insolvencies-june-2026',
                'measurementTechnique' => 'Company Debt calculations (percentage changes, rolling 12-month comparisons and peer-sector shares) from Insolvency Service company insolvency tables, identified via Companies House SIC group 522. The industry total is published monthly (Table 1c).',
                'keywords'        => 'freight forwarder insolvency, logistics company insolvency statistics, customs broker insolvencies 2026, SIC 522 insolvency statistics, UK',
                'isAccessibleForFree'  => true,
                'license'              => 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                'variableMeasured'     => array(
                    'Freight forwarding and logistics-support company insolvencies (count)',
                    'Annual percentage change',
                    'Rolling 12-month count',
                    'Peer-sector shares within transportation and storage (SIC H)',
                ),
            ),
            array(
                '@type'      => 'FAQPage',
                '@id'        => $ff_page_url . '#faq',
                'mainEntity' => $ff_faq_main_entities,
            ),
        );
    }

    return null;
}

/**
 * Site-alignment CSS: brings a /data/ page into line with the rest of
 * companydebt.com (Arial, the site's full-bleed pale blue hero band, one
 * spacing rhythm, the breadcrumb fix), per docs/data-hub/design-brief-2026-07.md
 * and the Claude Design handoff. Parameterised on $hero_selector because the
 * flagship's own markup uses .cd-hero while the sibling data pages (built
 * from a different design-handoff extraction) use .cd-hub-header for the
 * same role.
 *
 * Callers MUST gate on cd_datahub_current_slug() before echoing this: every
 * /data/ page shares body.page-template-data-hub-template, so an unscoped
 * call would silently reskin every page in the section, including ones that
 * have not been through this alignment pass yet.
 */
function cd_datahub_alignment_css( $hero_selector, $band_selector = null ) {
    // $band_selector: the element the full-bleed ::before band actually
    // attaches to. Defaults to $hero_selector, correct for every page whose
    // hero is a single element. The flagship's hero is two nested layers -
    // .cd-w-hero (the true 100vw outer wrapper) containing .cd-hero (a
    // narrower, asymmetrically-inset inner grid) - and the band MUST attach
    // to the outer one. The "left:50%; margin-left:-50vw" full-bleed trick
    // only reaches the true viewport edge when the element carrying it is
    // itself already 100vw wide; attached to the narrower inner element (as
    // an earlier version of this function did), "50%" resolves against that
    // element's own ~1136px width, not the viewport, so the band renders as
    // a bounded card offset ~72px from the edge instead of a true band.
    if ( null === $band_selector ) {
        $band_selector = $hero_selector;
    }
    return <<<CSS
<style id="cd-site-alignment">
/* 0 -- FULL-BLEED ESCAPE HATCH. The theme's <main class="site-main"> (the
   direct ancestor every data-hub page renders inside) carries
   overflow-x:hidden site-wide, almost certainly to stop oversized ordinary
   content (images, tables) from creating a horizontal scrollbar on normal
   pages. Every data-hub full-bleed section (.cd-w-hero, .cd-w-wide,
   .cd-masthead, .cd-bleed) works by escaping its container via
   width:100vw + a negative margin - and that escape is clipped right back
   down by this ancestor's overflow, which is what made the masthead AND the
   hero band both render as bounded, inset cards rather than true edge-to-
   edge bands (found 2026-07 via direct browser inspection: computed CSS was
   correct, but nothing painted past .site-main's own box). Scoped to this
   template only - .site-main's overflow:hidden stays intact everywhere else
   on the site, where it is presumably load-bearing.
   Sets the `overflow` SHORTHAND (both axes), not overflow-x alone: per spec,
   overflow-x:visible with overflow-y left at its inherited non-visible value
   is silently computed as overflow-x:auto instead, which still clips - this
   exact trap cost a whole extra deploy-and-recheck cycle to catch. */
html body.page-template-data-hub-template .site-main {
  overflow: visible !important;
}
/* 1 -- FONT. Arial, matching body.cd-ttt-design on the rest of the site. */
html body.page-template-data-hub-template .cd-data-hub,
html body.page-template-data-hub-template .cd-data-hub h1,
html body.page-template-data-hub-template .cd-data-hub h2,
html body.page-template-data-hub-template .cd-data-hub h3,
html body.page-template-data-hub-template .cd-data-hub {$hero_selector} h1,
html body.page-template-data-hub-template .cd-data-hub .cd-section-head h2,
html body.page-template-data-hub-template .cd-data-hub .cd-cta h2,
html body.page-template-data-hub-template .cd-data-hub .cd-brand__name,
html body.page-template-data-hub-template .cd-data-hub .cd-brand__mark {
  font-family: Arial, Helvetica, sans-serif !important;
}
/* H1 to the site scale, clamped so it wraps naturally on mobile. */
html body.page-template-data-hub-template .main-content .cd-data-hub {$hero_selector} h1,
html body.page-template-data-hub-template .main-content .cd-data-hub h1 {
  font-size: clamp(30px, 5vw, 48px) !important;
  line-height: 1.08 !important;
  letter-spacing: -0.02em !important;
  max-width: 800px !important;
}
/* 2 -- HERO BAND. Copies the site mechanism (.col-12.page-header::before): a
   100vw full-bleed pale blue band. body sets overflow-x:hidden, so 100vw
   cannot introduce horizontal scroll. Vertical padding (the gap above/below
   the content) stays on $hero_selector; the band's own width/position
   attaches to $band_selector, the element that is actually 100vw wide. */
html body.page-template-data-hub-template .main-content .cd-data-hub {$hero_selector} {
  position: relative;
  padding-top: 35px !important;
  padding-bottom: 54px !important;
  margin-bottom: 24px !important;
}
html body.page-template-data-hub-template .main-content .cd-data-hub {$band_selector} {
  position: relative;
}
html body.page-template-data-hub-template .main-content .cd-data-hub {$band_selector}::before {
  content: '';
  position: absolute;
  top: 0; bottom: 0; left: 50%;
  width: 100vw; margin-left: -50vw;
  background: #f4f7fe;
  z-index: 0;
}
html body.page-template-data-hub-template .main-content .cd-data-hub {$band_selector} > * {
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
html body.page-template-data-hub-template .main-content .cd-data-hub {$hero_selector} {
  padding-top: 8px !important;
}
html body.page-template-data-hub-template .page-header .breadcrumbs {
  white-space: normal !important;
}
</style>

CSS;
}

add_action( 'wp_head', function() {
    if ( 'uk-insolvency-statistics' !== cd_datahub_current_slug() ) {
        return;
    }
    echo cd_datahub_alignment_css( '.cd-hero', '.cd-w-hero' );
}, 30 );

add_action( 'wp_head', function() {
    if ( 'winding-up-petition-tracker' !== cd_datahub_current_slug() ) {
        return;
    }
    echo cd_datahub_alignment_css( '.cd-hub-header' );
}, 30 );

add_action( 'wp_head', function() {
    if ( 'dissolutions-vs-insolvencies' !== cd_datahub_current_slug() ) {
        return;
    }
    echo cd_datahub_alignment_css( '.cd-hub-header' );
}, 30 );

add_action( 'wp_head', function() {
    if ( 'payment-practices-late-payment' !== cd_datahub_current_slug() ) {
        return;
    }
    echo cd_datahub_alignment_css( '.cd-hub-header' );
}, 30 );

add_action( 'wp_head', function() {
    if ( 'data' !== cd_datahub_current_slug() ) {
        return;
    }
    echo cd_datahub_alignment_css( '.cd-hub-header' );
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
