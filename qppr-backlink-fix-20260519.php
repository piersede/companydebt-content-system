<?php
add_action( 'init', function () {
    if ( ! isset( $_GET['cd_fix_bl'] ) || $_GET['cd_fix_bl'] !== 'run2605' ) return;
    header( 'Content-Type: text/plain; charset=utf-8' );

    $new_redirects = array(
        '/liquidation-hub/' => '/liquidation/',
        '/articles/common-causes-of-construction-insolvency/' => '/insolvency/',
        '/articles/88-year-old-retailer-bhs-goes-company-liquidation/' => '/liquidation/',
        '/articles/covid-19-effects-on-cruise-industry/' => '/articles/',
        '/articles/jamie-oliver-restaurant-restructure-london/' => '/articles/',
        '/articles/poolmageddon-79-of-uk-pools-may-close-within-6-months/' => '/articles/',
        '/advice/what-is-meant-by-a-zombie-company/' => '/insolvency/',
        '/hmrc/hmrc-office-locations-uk/' => '/hmrc/',
        '/articles/gieves-hawkes-facing-liquidation/' => '/liquidation/',
        '/articles/gieves-hawkes-facing-liquidation' => '/liquidation/',
        '/what-support-is-available-for-military-veterans-starting-a-business/' => '/',
        '/how-is-your-business-going-to-be-affected-by-climate-change/' => '/articles/',
        '/articles/how-is-your-business-going-to-be-affected-by-climate-change/' => '/articles/',
        '/how-to-increase-happiness-and-productivity-in-the-workplace/' => '/',
        '/articles/will-the-energy-crisis-mean-the-end-for-britains-bakeries/' => '/articles/',
        '/features/airlines-brace-for-a-longer-and-deeper-crisis-in-2021/' => '/articles/',
        '/articles/bank-of-england-warns-of-sme-debt-vulnerablity/' => '/articles/',
        '/articles/late-invoice-payments-continue-big-problem-british-businesses/' => '/insolvency/',
        '/news/brexit-impact-on-smes-and-the-insolvency-regime/' => '/insolvency/',
        '/guides/7-top-tips-to-make-sure-you-survive-company-insolvency/' => '/insolvency/',
        '/guides/an-sme-s-guide-to-reducing-basic-business-expenditure-costs/' => '/company-cash-flow-problems/',
        '/company-rescue-solutions/advantages-disadvantages-administration' => '/company-administration/',
        '/faqs/what-is-insolvency' => '/insolvency/',
        '/what-can-bailiffs-seize-from-a-limited-company/' => '/winding-up-petitions/',
        '/how-to-save-money-with-social-media/' => '/',
        '/support-for-military-veterans-starting-a-business-in-canada/' => '/',
        '/articles/6000-fuel-hikes-taxi-sector/' => '/articles/',
        '/articles/how-much-is-the-digital-sales-tax-going-to-affect-big-tech/' => '/articles/',
        '/articles/is-harley-davidson-heading-for-a-crash/' => '/articles/',
        '/articles/wayne-rooney-scores-21m-from-company-liquidation/' => '/liquidation/',
        '/guides/make-complaint-insolvency-practitioner-part-1/' => '/insolvency/what-is-an-insolvency-practitioner/',
        '/guides/rescue-guides/5-top-company-rescue-tips-for-struggling-businesses/' => '/insolvency/business-recovery-services/',
        '/hmrc/hmrcs-connect-computer-system/' => '/hmrc/',
        '/invoice-finance/' => '/company-cash-flow-problems/',
        '/liquidation/striking-off-dissolving-company/' => '/closing-a-limited-company/',
        '/download-our-covid-19-business-survival-guide/' => '/bounce-back-loan-support-hub/',
    );

    $existing = get_option( 'quickppr_redirects', array() );
    $before_count = is_array( $existing ) ? count( $existing ) : 0;

    foreach ( $new_redirects as $src => $dst ) {
        $existing[ $src ] = $dst;
    }
    update_option( 'quickppr_redirects', $existing );

    $meta = get_option( 'quickppr_redirects_meta', array() );
    foreach ( $new_redirects as $src => $dst ) {
        $meta[ $src ] = array( 'newwindow' => '0', 'nofollow' => '0' );
    }
    update_option( 'quickppr_redirects_meta', $meta );

    $after = get_option( 'quickppr_redirects', array() );
    $after_count = is_array( $after ) ? count( $after ) : 0;

    echo "DONE\n";
    echo "Before: {$before_count} redirects\n";
    echo "Added: " . count( $new_redirects ) . " new rules\n";
    echo "After: {$after_count} redirects\n";
    echo "\nSample verify:\n";
    $sample_keys = array_keys( $new_redirects );
    foreach ( array_slice( $sample_keys, 0, 5 ) as $src ) {
        $got = isset( $after[ $src ] ) ? $after[ $src ] : 'MISSING';
        echo "  {$src} => {$got}\n";
    }
    $hub = isset( $after['/liquidation-hub/'] ) ? $after['/liquidation-hub/'] : 'MISSING';
    echo "\n/liquidation-hub/ => {$hub}\n";

    exit;
} );
