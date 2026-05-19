<?php
/**
 * Plugin Name: CD 410 Gone — Deleted Articles
 * Description: Returns HTTP 410 Gone for permanently removed article pages so Google de-indexes them quickly.
 */

add_action( 'template_redirect', 'cd_410_gone_articles', 1 );

function cd_410_gone_articles() {
    $path = rtrim( parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ), '/' );

    static $gone = [
        '/articles/coffee-shop-owners-say-lattes-would-have-to-be-7-to-follow-energy-hikes',
        '/articles/39-of-hair-and-beauty-sector-still-furloughed',
        '/articles/jamie-oliver-restaurant-restructure-london',
        '/articles/common-causes-of-construction-insolvency',
        '/articles/covid-19-effects-on-cruise-industry',
        '/articles/kids-company-directors-face-disqualification-proceedings',
        '/articles/6000-fuel-hikes-taxi-sector',
        '/articles/more-small-energy-providers-face-collapse-as-crisis-deepens',
        '/articles/12-year-ban-for-director-who-pocketed-covid-loan-cash',
        '/articles/monarch-airline-insolvency',
        '/articles/poolmageddon-79-of-uk-pools-may-close-within-6-months',
        '/articles/can-bradford-rugby-club-saved-liquidation',
        '/articles/find-out-why-the-transport-industry-is-prone-to-insolvency',
        '/articles/all-dishes-off-menu-for-dacampos-my-pasta-bar',
        '/articles/insolvencies-within-the-technology-sector',
        '/articles/british-cycle-sales-hit-39-year-low',
        '/articles/leeds-dino-trail-collapses-into-administration',
        '/articles/how-much-is-the-digital-sales-tax-going-to-affect-big-tech',
        '/articles/travel-firm-collapses-as-it-cannot-pay-refunds',
        '/articles/88-year-old-retailer-bhs-goes-company-liquidation',
        '/articles/will-the-energy-crisis-mean-the-end-for-britains-bakeries',
        '/articles/80-homebase-stores-set-to-close-as-part-of-cva',
        '/articles/gieves-hawkes-facing-liquidation',
        '/articles/scaffolder-censured-over-bounce-back-loan',
        '/articles/pink-biscuit-manufacturer-rivington-biscuits-goes-company-administration',
        '/articles/failed-arena-television-leaves-trail-of-losses-and-faces-fraud-probe',
        '/articles/barnsley-shopping-centre-enters-receivership',
        '/articles/equestrian-failed-company-voluntary-arrangement-administration',
        '/articles/high-court-closes-insolvent-mini-bond-group',
        '/articles/clothing-retailer-usc-close-30-unfashionable-stores',
        '/articles/wayne-rooney-scores-21m-from-company-liquidation',
        '/articles/crackdown-on-directors-who-close-companies-to-avoid-debts',
        '/articles/boulestin-avoids-closure',
        '/articles/bans-for-uk-directors-who-avoid-repaying-bounce-back-loans',
        '/articles/lengthy-disqualifications-for-four-directors-involved-in-vat-fraud',
        '/articles/disqualified-directors-jailed-continuing-control-companies',
        '/articles/can-manchester-united-get-out-from-under-its-455-5m-debt',
        '/articles/bobby-davros-business-goes-bust',
        '/articles/insolvent-wine-scammers',
        '/articles/is-harley-davidson-heading-for-a-crash',
    ];

    if ( ! in_array( $path, $gone, true ) ) {
        return;
    }

    status_header( 410 );
    nocache_headers();
    echo '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>410 Gone</title></head>'
       . '<body><h1>Gone</h1><p>This page has been permanently removed.</p></body></html>';
    exit;
}
