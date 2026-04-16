<?php
/**
 * The header for our theme
 *
 * This is the template that displays all of the <head> section and everything up until <div id="content">
 *
 * @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
 *
 * @package CompanyDebt
 */

?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="https://gmpg.org/xfn/11">
	<script async defer src="https://www.googletagmanager.com/gtag/js?id=UA-27555004-1" id="cd-ga-script"></script>
	<script>
		window.dataLayer = window.dataLayer || [];

		function gtag() {
			dataLayer.push(arguments);
		}

		gtag('js', new Date());
		gtag('config', 'UA-27555004-1');
	</script>

	<!--     Google Tag Manager-->
	<script>(function (w, d, s, l, i) {
		w[l] = w[l] || [];
		w[l].push({
			'gtm.start':
				new Date().getTime(), event: 'gtm.js'
		});
		var f = d.getElementsByTagName(s)[0],
			j = d.createElement(s), dl = l != 'dataLayer' ? '&l=' + l : '';
		j.async = true;
		j.src =
			'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
		f.parentNode.insertBefore(j, f);
		})(window, document, 'script', 'dataLayer', 'GTM-5GTD9ZP');</script>

	<!-- End Google Tag Manager -->

	<!-- Google Tag Manager -->
	<script>(function (w, d, s, l, i) {
		w[l] = w[l] || [];
		w[l].push({
			'gtm.start':
				new Date().getTime(), event: 'gtm.js'
		});
		var f = d.getElementsByTagName(s)[0],
			j = d.createElement(s), dl = l != 'dataLayer' ? '&l=' + l : '';
		j.async = true;
		j.src =
			'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
		f.parentNode.insertBefore(j, f);
		})(window, document, 'script', 'dataLayer', 'GTM-KT6M67T');</script>
	<!-- End Google Tag Manager -->

	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div id="page" class="site">
	<a class="skip-link screen-reader-text" href="#primary"><?php esc_html_e( 'Skip to content', 'company-debt-webpigment' ); ?></a>
    <div class="mobile-action-bar"><?php the_field( 'mobile_action_bar', 'option' ); ?></div>
    <?php if ( is_page_template( 'templates/design-22-v1.php' ) ) : ?>
        <header>
            <div class="header-22 container">
                <a href="https://www.companydebt.com" class="logo-link">
                    <img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/logo-design22-1.png' ); ?>" height="56" width="227" alt="Company Debt Logo" title="Company Debt" class="header__logo">
                </a>
                <a class="header__cta" href="tel:<?php echo str_replace( ' ', '', get_field( 'header_phone_number', 'options' ) ); ?>">
                    <div class="header__cta-letters">Free Confidential Advice:&nbsp;</div>
                    <div class="header__cta-number"> <?php the_field( 'header_phone_number', 'options' ); ?></div>
                </a>


            </div>
        </header>
    <?php elseif ( ! is_page_template( 'templates/landing-page.php' ) && ! is_page_template( 'templates/insolvency-landing-page.php' ) && ! is_page_template( 'templates/blank-landing-page.php' ) ) : ?>
	<header id="masthead" class="site-header">
        <div class="container-fluid">
            <div class="row">
                <div class="site-branding">

		            <?php the_custom_logo(); ?>

                </div><!-- .site-branding -->
	            <button name="mobile-menu-button" title="Mobile menu button" id="primary-menu-toggle" class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
		            <span class="line"></span>
		            <span class="line"></span>
		            <span class="line"></span>
	            </button>
                <nav id="site-navigation" class="main-navigation">
	                <a class="mobile-cta" href="tel:08000746757">
		                <span class="">Free Directors Helpline:</span>
		                <span class="number">0800 074 6757</span>
	                </a>
		            <?php
		            wp_nav_menu(
			            array(
				            'theme_location' => 'menu-1',
				            'menu_id'        => 'primary-menu',
				            'walker' => new CD\Core\Walker(),
			            )
		            );
		            ?>
                </nav><!-- #site-navigation -->

                <div class="header-right">
                    <div class="header-search">
                        <img width="27" height="27" src="<?php echo esc_html( get_template_directory_uri() . '/assets/images/search-white.png' ); ?>"
                             alt="search" class="header__search-icon">
                    </div>
                    <div class="header-cta">
                        <a href="tel:08000746757" class="header-phone">
                            0800 074 6757</a>
                    </div>
                </div>
            </div>

        </div>
	</header><!-- #masthead -->
	<?php get_search_form(); ?>
    <?php endif; ?>
