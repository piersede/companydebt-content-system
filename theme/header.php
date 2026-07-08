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
	<script>/* Mark JS-enabled so FOUC-suppressing CSS rules can gate on it. */
	document.documentElement.classList.add('cd-js');</script>
	<link rel="profile" href="https://gmpg.org/xfn/11">
	<!-- Universal Analytics (UA-27555004-1) removed 2026-06-19 - property sunset by Google in July 2023, collected nothing. GA4 (G-P39KJ34V6G) is served via GTM. -->

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

	<!-- Secondary GTM container GTM-KT6M67T retired 2026-06-24 - redundant with GTM-5GTD9ZP (both fed the same GA4 property, risked double-counting). Its unique scroll-depth event should be rebuilt inside GTM-5GTD9ZP if still wanted. -->

	<?php wp_head(); ?>
	<style id="cd-canonical-type-scale">
	/* CompanyDebt canonical type + spacing scale (cd-ttt-design). Inlined as CRITICAL
	   CSS so headings paint at the right size on first paint (no FOUC from the external
	   stylesheet or the inline Customizer rules). 1.2 modular scale, base 16; body 18px.
	   Authoritative source -- the matching block in style.css was removed 2026-06-19. */
	@media (min-width:1038px){
	  html body.cd-ttt-design .col-12.page-header h1.post-title{font-size:33px!important;line-height:1.15!important;font-weight:700!important}
	  body.cd-ttt-design .main-content h2{font-size:28px!important;line-height:1.2!important;font-weight:700!important;margin:40px 0 19px!important}
	  body.cd-ttt-design .main-content h3{font-size:23px!important;line-height:1.25!important;font-weight:500!important;margin:28px 0 16px!important}
	  body.cd-ttt-design .main-content h4:not([class*="cd-"]){font-size:19px!important;line-height:1.3!important;font-weight:600!important;margin:23px 0 13px!important}
	}
	@media (max-width:1037px){
	  html body.cd-ttt-design .col-12.page-header h1.post-title{font-size:28px!important;line-height:1.18!important;font-weight:700!important}
	  body.cd-ttt-design .main-content h2{font-size:24px!important;line-height:1.2!important;font-weight:700!important;margin:32px 0 16px!important}
	  body.cd-ttt-design .main-content h3{font-size:20px!important;line-height:1.25!important;font-weight:500!important;margin:24px 0 14px!important}
	  body.cd-ttt-design .main-content h4:not([class*="cd-"]){font-size:18px!important;line-height:1.3!important;font-weight:600!important;margin:20px 0 12px!important}
	}
	body.cd-ttt-design .main-content p{margin:0 0 19px!important}
	body.cd-ttt-design .main-content ul,body.cd-ttt-design .main-content ol{margin:16px 0 23px!important;padding-left:23px!important}
	body.cd-ttt-design .main-content li{margin-bottom:13px!important}
	body.cd-ttt-design .main-content table{margin:28px 0!important}
	body.cd-ttt-design .main-content th,body.cd-ttt-design .main-content td{padding:16px 19px!important}
	body.cd-ttt-design .main-content .cd-callout{margin:40px 0!important;padding:23px!important}
	body.cd-ttt-design .cd-callout h2.cd-callout__label,body .cd-callout--summary h2.cd-callout__label{font-family:inherit!important;font-size:28px!important;line-height:1.2!important;font-weight:700!important;text-transform:none!important;letter-spacing:-0.01em!important;color:rgb(0,40,86)!important;margin:0 0 16px!important;padding:0!important}
	/* v2 topnav (white menu) -- UNCONDITIONAL critical CSS (no data-topnav-v2 flag),
	   so the white header paints on the FIRST frame regardless of when the flag/JS
	   arrives. The original blue base can never paint. Site is v2 everywhere, so white
	   is effectively the default. Specificity (0,2,2) via doubled .site-header to beat
	   the blue base. Full v2 detail rules still live in style.css. 2026-06-20. */
	html header.site-header.site-header {
	  background: #ffffff !important;
	  border-top: 4px solid #102a43 !important;
	  border-bottom: 1px solid rgba(0,40,86,0.04) !important;
	}
	html header.site-header nav.main-navigation ul li a,
	html header.site-header nav.main-navigation ul li span {
	  color: rgb(82,96,109) !important;
	  font-family: Arial, sans-serif !important;
	  font-weight: 700 !important;
	  font-size: 15px !important;
	  line-height: 1.2 !important;
	}
	html header.site-header nav.main-navigation .menu-header-menu-container > ul > li > a,
	html header.site-header nav.main-navigation .menu-header-menu-container > ul > li > span {
	  display: inline-block !important;
	  padding: 10px 16px !important;
	  border-radius: 8px !important;
	  line-height: 1.2 !important;
	}
	html header.site-header nav.main-navigation .menu-header-menu-container > ul { gap: 6px !important; }
	/* v2 topnav logo: show the dark v2 logo on the white header at first paint,
	   so it isn't the light v1 logo (invisible on white) before the delayed JS swap. */
	html header.site-header.site-header a.custom-logo-link img.custom-logo,
	html header.site-header.site-header img.custom-logo {
	  content: url('https://comdebstage.wpenginepowered.com/wp-content/themes/company-debt-webpigment/assets/images/cd-logo-topnav-v3.png') !important;
	}
	</style>

	<!-- Set v2 feature flags before <body> renders to prevent FOUC. -->
	<script id="cd-v2-flags-early">
	(function(){
	  var d = document.documentElement;
	  d.setAttribute('data-toc-sidebar','on');
	  d.setAttribute('data-reviewsio-hidden','on');
	  d.setAttribute('data-topnav-v2','on');
	  // data-sticky-nav, data-licensed-v2, data-insolvency-v2 retired 2026-06-20:
	  // sticky-nav + licensed CSS de-flagged (unconditional); insolvency widget
	  // is now server-rendered (cd-rocket-flicker-fix.php). See style.css.
	  // Experiment: narrower sidebar on take-the-test template (desktop only).
	  // Remove this one line to instantly revert the experiment.
	  d.setAttribute('data-narrow-sidebar','on');
	  // Footer v2 — sitewide redesign (logo swap, hide tagline + Contact Us
	  // title, relocate policy links as pills, restyle widget titles + items,
	  // top divider on disclaimer). Remove to instantly revert.
	  d.setAttribute('data-footer-v2','on');
	})();
	</script>
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
