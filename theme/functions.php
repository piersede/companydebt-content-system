<?php
/**
 * CompanyDebt functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package CompanyDebt
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! defined( '_S_VERSION' ) ) {
	// Replace the version number of the theme on each release.
	define( '_S_VERSION', '1.4.6' );
}

if ( ! defined( 'CD_THEME_DIR' ) ) {
	define( 'CD_THEME_DIR', trailingslashit( get_template_directory() ) );
}

if ( ! defined( 'CD_THEME_URL' ) ) {
	define( 'CD_THEME_URL', trailingslashit( get_template_directory_uri() ) );
}

if ( ! defined( 'CD20_VIEWS' ) ) {
	define( 'CD20_VIEWS', CD_THEME_DIR . 'views' );
}

if ( ! defined( 'CD_THEME_VERSION' ) ) {
	define( 'CD_THEME_VERSION', _S_VERSION );
}

// Require modules.
require_once CD_THEME_DIR . 'inc/init.php';

/**
 * Sets up theme defaults and registers support for various WordPress features.
 *
 * Note that this function is hooked into the after_setup_theme hook, which
 * runs before the init hook. The init hook is too late for some features, such
 * as indicating support for post thumbnails.
 */
function company_debt_webpigment_setup() {
	/*
		* Make theme available for translation.
		* Translations can be filed in the /languages/ directory.
		* If you're building a theme based on CompanyDebt, use a find and replace
		* to change 'company-debt-webpigment' to the name of your theme in all the template files.
		*/
	load_theme_textdomain( 'company-debt-webpigment', get_template_directory() . '/languages' );

	// Add default posts and comments RSS feed links to head.
	add_theme_support( 'automatic-feed-links' );

	/*
		* Let WordPress manage the document title.
		* By adding theme support, we declare that this theme does not use a
		* hard-coded <title> tag in the document head, and expect WordPress to
		* provide it for us.
		*/
	add_theme_support( 'title-tag' );

	/*
		* Enable support for Post Thumbnails on posts and pages.
		*
		* @link https://developer.wordpress.org/themes/functionality/featured-images-post-thumbnails/
		*/
	add_theme_support( 'post-thumbnails' );
	add_image_size( 'blog_thumbnail', 373, 219, array( 'center', 'center' ) );

	// This theme uses wp_nav_menu() in one location.
	register_nav_menus(
		array(
			'menu-1' => esc_html__( 'Primary', 'company-debt-webpigment' ),
		)
	);

	/*
		* Switch default core markup for search form, comment form, and comments
		* to output valid HTML5.
		*/
	add_theme_support(
		'html5',
		array(
			'search-form',
			'comment-form',
			'comment-list',
			'gallery',
			'caption',
			'style',
			'script',
		)
	);

	// Set up the WordPress core custom background feature.
	add_theme_support(
		'custom-background',
		apply_filters(
			'company_debt_webpigment_custom_background_args',
			array(
				'default-color' => 'ffffff',
				'default-image' => '',
			)
		)
	);

	// Add theme support for selective refresh for widgets.
	add_theme_support( 'customize-selective-refresh-widgets' );

	/**
	 * Add support for core custom logo.
	 *
	 * @link https://codex.wordpress.org/Theme_Logo
	 */
	add_theme_support(
		'custom-logo',
		array(
			'height'      => 250,
			'width'       => 250,
			'flex-width'  => true,
			'flex-height' => true,
		)
	);

	add_image_size( 'blog_thumbnail', 373, 219, array( 'center', 'center' ) );
}
add_action( 'after_setup_theme', 'company_debt_webpigment_setup' );

/**
 * Set the content width in pixels, based on the theme's design and stylesheet.
 *
 * Priority 0 to make it available to lower priority callbacks.
 *
 * @global int $content_width
 */
function company_debt_webpigment_content_width() {
	$GLOBALS['content_width'] = apply_filters( 'company_debt_webpigment_content_width', 640 );
}
add_action( 'after_setup_theme', 'company_debt_webpigment_content_width', 0 );

/**
 * Register widget area.
 *
 * @link https://developer.wordpress.org/themes/functionality/sidebars/#registering-a-sidebar
 */
function company_debt_webpigment_widgets_init() {

	register_sidebar(
		array(
			'name'          => esc_html__( 'Primary - Default Sidebar', 'company-debt-webpigment' ),
			'id'            => 'sidebar-primary',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Take The Test Sidebar', 'company-debt-webpigment' ),
			'id'            => 'sidebar-take-the-test',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'After Breadcrumbs Mobile Sidebar', 'company-debt-webpigment' ),
			'id'            => 'after-breadcrumbs-mobile-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<div id="after-breadcrumbs-area">',
			'after_widget'  => '</div>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Custom Sidebar 2 - Pages Menu', 'company-debt-webpigment' ),
			'id'            => 'custom-sidebar-2',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

//

	register_sidebar(
		array(
			'name'          => esc_html__( 'Content Sidebar - Download Guide', 'company-debt-webpigment' ),
			'id'            => 'content-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

//

	register_sidebar(
		array(
			'name'          => esc_html__( 'Table of Content Sidebar - TOC', 'company-debt-webpigment' ),
			'id'            => 'toc-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

//

	register_sidebar(
		array(
			'name'          => esc_html__( 'Design 2022-1 Sidebar', 'company-debt-webpigment' ),
			'id'            => 'design22v1-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer Section 1', 'company-debt-webpigment' ),
			'id'            => 'footer-section-1-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<div class="widget-title">',
			'after_title'   => '</div>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer Section 2', 'company-debt-webpigment' ),
			'id'            => 'footer-section-2-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<div class="widget-title">',
			'after_title'   => '</div>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer Section 3', 'company-debt-webpigment' ),
			'id'            => 'footer-section-3-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<div class="widget-title">',
			'after_title'   => '</div>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer Section 4', 'company-debt-webpigment' ),
			'id'            => 'footer-section-4-sidebar',
			'description'   => esc_html__( 'Add widgets here.', 'company-debt-webpigment' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<div class="widget-title">',
			'after_title'   => '</div>',
		)
	);

	require_once CD_THEME_DIR . '/inc/widgets/class-reviewed-by.php';
	register_widget( 'CD\Widgets\Reviewed_By' );
}
add_action( 'widgets_init', 'company_debt_webpigment_widgets_init' );

/**
 * Untag the footer widget-title <h2>s as <div>s.
 * Footer widgets are Gutenberg block widgets, so the heading is hard-coded
 * inside the block content (not generated by before_title). Buffer the
 * dynamic_sidebar output and regex-swap the tag without changing classes or
 * styles. Scoped to footer-section-N-sidebar only.
 */
add_action( 'dynamic_sidebar_before', function( $index ) {
    if ( is_string( $index ) && strpos( $index, 'footer-section-' ) === 0 ) {
        ob_start();
    }
} );
add_action( 'dynamic_sidebar_after', function( $index ) {
    if ( is_string( $index ) && strpos( $index, 'footer-section-' ) === 0 ) {
        $html = ob_get_clean();
        $html = preg_replace(
            '/<h2(\s+[^>]*?class="[^"]*?widget-title[^"]*?"[^>]*?)>(.*?)<\/h2>/i',
            '<div$1>$2</div>',
            $html
        );
        echo $html;
    }
} );

/**
 * Take-the-test sidebar widget titles: swap H3 -> div with .cd-sidebar-title
 * class for semantic-only change (visual styling via CSS).
 */
add_action( 'dynamic_sidebar_before', function( $index ) {
    if ( $index === 'sidebar-take-the-test' ) {
        ob_start();
    }
} );
add_action( 'dynamic_sidebar_after', function( $index ) {
    if ( $index === 'sidebar-take-the-test' ) {
        $html = ob_get_clean();
        // Swap any <h3>...</h3> in this sidebar's output to <div class="cd-sidebar-title">...</div>
        $html = preg_replace(
            '/<h3(?:\s+[^>]*)?>(.*?)<\/h3>/is',
            '<div class="cd-sidebar-title">$1</div>',
            $html
        );
        echo $html;
    }
} );



// Force cache-bust block CSS files
add_filter('style_loader_src', function($src) {
    if (strpos($src, '/blocks/') !== false && strpos($src, 'ver=1') !== false) {
        $src = str_replace('ver=1', 'ver=' . time(), $src);
    }
    if (strpos($src, 'cd-download-file-widget') !== false && strpos($src, 'ver=1') !== false) {
        $src = str_replace('ver=1', 'ver=' . time(), $src);
    }
    return $src;
});

/**
 * Enqueue scripts and styles.
 */
function company_debt_webpigment_scripts() {
	wp_enqueue_style( 'company-debt-webpigment-style', get_stylesheet_uri(), array(), rand( 1, 10000000000000) );
//	wp_enqueue_style( 'company-debt-webpigment-common', get_template_directory_uri().'/assets/css/public/common.css', array(), _S_VERSION );
	wp_style_add_data( 'company-debt-webpigment-style', 'rtl', 'replace' );

	wp_enqueue_script( 'company-debt-webpigment-navigation', get_template_directory_uri() . '/js/navigation.js', array(), _S_VERSION, true );
	wp_enqueue_script( 'company-debt-webpigment-global', get_template_directory_uri() . '/assets/js/global.js', array( 'jquery' ), _S_VERSION, true );

	// TOC is always expanded — no JS toggle needed
	// if ( ( is_singular( 'post' ) && get_field( 'toc_enabled' ) ) || is_singular( 'page' ) ) {
	// 	wp_enqueue_script( 'company-debt-webpigment-toc', get_template_directory_uri() . '/assets/js/toc.js', array( 'jquery' ), _S_VERSION, true );
	// }

	wp_register_script( 'webp-js-scroll', get_template_directory_uri() . '/assets/js/scroll.js', array(), _S_VERSION, true );
	wp_register_style( 'webp-js-scroll', get_template_directory_uri() . '/public/gutenberg-blocks/scroll-js.css', array(), _S_VERSION );

	if ( is_singular() ) {
		wp_enqueue_script( 'company-debt-webpigment-single', get_template_directory_uri() . '/assets/js/single.js', array( 'jquery' ), _S_VERSION, true );
		if ( get_field( 'enable_related_articles', get_the_ID() ) || ! metadata_exists( 'post', get_the_ID(), 'enable_related_articles' ) ) {
			wp_enqueue_script( 'company-debt-webpigment-related-articles', get_template_directory_uri() . '/assets/js/related-articles.js', array( 'jquery' ), filemtime( get_template_directory() . '/assets/js/related-articles.js' ), true );
		}
	}

	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}

	if ( is_archive() || is_search() ) {
		/* filemtime() instead of _S_VERSION so every edit to archive.css auto
		 * busts the browser cache — the file is iterated on more frequently
		 * than the theme constant gets bumped. -- 20260603 */
		$arch_css = get_template_directory() . '/public/archive.css';
		$arch_ver = file_exists( $arch_css ) ? (string) filemtime( $arch_css ) : _S_VERSION;
		wp_enqueue_style( 'company-debt-webpigment-arcihive', get_template_directory_uri() . '/public/archive.css', array(), $arch_ver );
	}

	if ( is_page_template( 'templates/design-22-v1.php' ) ) {
		wp_enqueue_style( 'company-debt-webpigment-header-design22', get_template_directory_uri() . '/public/header22.css', array(), _S_VERSION );
		wp_enqueue_style( 'company-debt-webpigment-design22', get_template_directory_uri() . '/public/design22.css', array(), _S_VERSION );
	}

	if ( is_page_template( 'templates/template-tabs.php' ) ) {
		wp_enqueue_style( 'company-debt-webpigment-tabs-template', get_template_directory_uri() . '/public/tabs-template.css', array(), _S_VERSION );
	}

	if ( is_singular() ) {
		wp_enqueue_style( 'company-debt-webpigment-footnotes', get_template_directory_uri() . '/public/footnotes.css', array(), _S_VERSION );
	}

	wp_register_style(
		'accreditation',
		CD_THEME_URL . 'public/accreditation.css',
		array(),
		CD_THEME_VERSION
	);

	wp_register_style(
		'review-author',
		CD_THEME_URL . 'public/review-author.css',
		array(),
		CD_THEME_VERSION
	);

	wp_register_script(
		'print-js',
		CD_THEME_URL . 'assets/libs/printJs/print.min.js',
		array(),
		CD_THEME_VERSION,
		true
	);

	wp_register_script(
		'cd-reviews-widget',
		CD_THEME_URL . 'blocks/cd-reviews-widget/cd-reviews-widget.js',
		array(),
		CD_THEME_VERSION,
		true
	);


	wp_register_script(
		'nouislider',
		CD_THEME_URL . 'assets/libs/noUiSlider/nouislider.min.js',
		array(),
		CD_THEME_VERSION,
		true
	);

	wp_register_style(
		'nouislider',
		CD_THEME_URL . 'assets/libs/noUiSlider/nouislider.min.css',
		array(),
		CD_THEME_VERSION,
	);

	if ( is_page_template( 'templates/form-letter.php' ) ) {
		wp_enqueue_script( 'company-debt-webpigment-form-letter', get_template_directory_uri() . '/assets/js/form-letter.js', array( 'jquery', 'print-js' ), _S_VERSION, true );
	}

	if ( is_page_template( 'templates/quiz-insolvency.php' ) ) {
		wp_enqueue_style(
			'quiz-insolvency',
			CD_THEME_URL . 'public/quiz-insolvency.css',
			array( 'nouislider' ),
			CD_THEME_VERSION,
		);
		wp_enqueue_script( 'company-debt-webpigment-quiz-insolvency', get_template_directory_uri() . '/assets/js/quiz-insolvency.js', array( 'jquery', 'nouislider' ), _S_VERSION, true );
	}

	if ( is_page_template( 'templates/insolvency-landing-page.php' ) ) {
		wp_enqueue_style(
			'quiz-insolvency',
			CD_THEME_URL . 'public/quiz-insolv-style.css',
			array( 'nouislider' ),
			CD_THEME_VERSION,
		);
		wp_enqueue_script(
			'quiz-insolvency',
			CD_THEME_URL . 'assets/js/quiz-insolv.js',
			array( 'nouislider' ),
			CD_THEME_VERSION,
			true
		);
	}
}
add_action( 'wp_enqueue_scripts', 'company_debt_webpigment_scripts' );

/**
 * Implement the Custom Header feature.
 */
require get_template_directory() . '/inc/custom-header.php';

/**
 * Custom template tags for this theme.
 */
require get_template_directory() . '/inc/template-tags.php';

/**
 * Functions which enhance the theme by hooking into WordPress.
 */
require get_template_directory() . '/inc/template-functions.php';

/**
 * Customizer additions.
 */
require get_template_directory() . '/inc/customizer.php';
require get_template_directory() . '/inc/cpt/cpt-testimonial.php';
require get_template_directory() . '/inc/class-acf-gutenberg-blocks.php';

/**
 * Load Jetpack compatibility file.
 */
if ( defined( 'JETPACK__VERSION' ) ) {
	require get_template_directory() . '/inc/jetpack.php';
}

function footnotes_in_content( $content ) {
	$content      = new CD\Content\Footnotes( $content );
	$content      = $content->getPostFootnotesMarkup();
	return $content;
}

function toc_and_footnotes_in_content( $content ) {
	/* Determine whether the current view should have a TOC injected into its
	 * body. Three paths qualify:
	 *   1. Single post with the legacy `toc_enabled` ACF field set (kept for
	 *      backward compatibility with posts that explicitly opted in).
	 *   2. Single page using the default page template OR the take-the-test
	 *      page template.
	 *   3. Single post using the default post template — i.e. anything that
	 *      now gets the cd-ttt-design body class, EXCLUDING posts on the
	 *      post-sectors template (they have their own combined section and
	 *      shouldn't grow an in-body TOC). Added 20260606 so /articles/*
	 *      posts get the same TOC sidebar behaviour as take-the-test pages. */
	$is_eligible_post_default = is_singular( 'post' )
		&& '' === get_page_template_slug()
		&& ! in_category( 'sectors' )
		&& ! in_category( 'services-to' );
	if ( ! is_front_page() && ! is_home() && (
		( is_singular( 'post' ) && get_field( 'toc_enabled' ) )
		|| ( is_singular( 'page' ) && ( '' === get_page_template_slug() || 'templates/take-the-test-template.php' === get_page_template_slug() ) )
		|| $is_eligible_post_default
	) ) {
		if ( get_field( 'enable_toc', get_the_ID() ) || ! metadata_exists( 'post', get_the_ID(), 'enable_toc' ) ) {
			$toc = new CD\Content\Toc( $content );
			$content = $toc->getPostTocInContent();
		}
	}

	$content_footnotes = new CD\Content\Footnotes( $content );
	return $content_footnotes->getPostFootnotesMarkup();
}

// add_action( 'the_content', function( $content ) {
// 	if ( ! is_front_page() && ! is_home() && ( ( is_singular( 'post' ) && get_field( 'toc_enabled' ) ) || ( is_singular( 'page' ) && ( '' === get_page_template_slug() || 'templates/take-the-test-template.php' === get_page_template_slug() ) ) ) ) {
// 		if ( get_field( 'enable_toc', get_the_ID() ) || ! metadata_exists( 'post', get_the_ID(), 'enable_toc' ) ) {
// 			$toc = new CD\Content\Toc( $content );
// 			$content = $toc->getPostTocInContent();
// 		}
// 	}

// 	$content_footnotes = new CD\Content\Footnotes( $content );
// 	return $content_footnotes->getPostFootnotesMarkup();
// }, 5 );


add_filter( 'body_class', function( $classes ) {
	if ( ! is_front_page() && ! is_home() && ( ( is_singular( 'post' ) && get_field( 'toc_enabled' ) ) || ( is_singular( 'page' ) && '' === get_page_template_slug() ) ) ) {
		$classes[] = 'has-toc';
	}

	return $classes;
} );

add_filter( 'excerpt_length', 'limit_excerpt_length' );
add_filter( 'excerpt_more', 'replace_excerpt_more' );

function limit_excerpt_length( $length ) {
	if ( 'testimonial' === get_post_type() ) {
		return 40;
	} else {
		return 25;
	}
}

function replace_excerpt_more() {
	return '...';
}

// Loads Redundancy Calculator Script when GF id 33 is on page
add_action( 'gform_enqueue_scripts_33', 'redun_calc_script', 10, 2 );
function redun_calc_script( $form, $is_ajax ) {
	if ( $is_ajax ) {
		wp_enqueue_script( 'redun_calc', CD_THEME_URL . 'assets/js/redun-calc.js' );
		wp_enqueue_style( 'redun_calc_style', CD_THEME_URL . 'public/reduc-calc-style.css' );
	}
}

// Loads Download Guide Script when GF id 30 is on page
add_action( 'gform_enqueue_scripts_30', 'download_guide_script', 10, 2 );
function download_guide_script( $form, $is_ajax ) {
	if ( $is_ajax ) {
		wp_enqueue_script( 'download_guide', CD_THEME_URL . 'assets/js/download-guide.js' );
	}
}

add_filter('gform_pre_render_30', 'add_hidden_download_link');
function add_hidden_download_link($form) {
    $script = "
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            var fileUrl = document.querySelector('[name=\"input_5\"]').value;

            var downloadLink = document.createElement('a');
            downloadLink.href = fileUrl;
            downloadLink.download = '';
            downloadLink.style.display = 'none';
            downloadLink.id = 'hidden-download-link';
            document.body.appendChild(downloadLink);
        });

        function triggerDownload() {
            document.getElementById('hidden-download-link').click();
        }
        </script>
    ";

	add_action('wp_footer', function() use ($script) {
        echo $script;
    });

    return $form;
}

// Attaches the Director's Guide to notification email
add_filter( 'gform_notification_38', 'change_user_notification_attachments', 10, 3 );
function change_user_notification_attachments( $notification, $form, $entry ) {
	if ( $notification['name'] == 'User Notification' ) {
		$url = CD_THEME_DIR . 'downloads/Company-Debt-Stressed-Directors-Guide.pdf';
		$notification['attachments'][] = $url;
	}
	return $notification;
}

/**
 * Disable RSS feeds for Wordpress
 */
function fb_disable_feed() {
	wp_die( __('No feed available,please visit our homepage') );
}

add_action('do_feed', 'fb_disable_feed', 1);
add_action('do_feed_rdf', 'fb_disable_feed', 1);
add_action('do_feed_rss', 'fb_disable_feed', 1);
add_action('do_feed_rss2', 'fb_disable_feed', 1);


add_filter( 'gform_validation', 'custom_validation' );
function custom_validation( $validation_result ) {
	if ( false === get_option( 'disallowed_keys' ) ) {
		// Assume this is WP < 5.5. Option does not exist.
		$blacklisted = get_option('blacklist_keys');
	} else {
		// Assume this is WP >= 5.5
		$blacklisted = get_option('disallowed_keys');
	}
	$blacklisted = get_field('bad_words', 'option' ) ? get_field('bad_words', 'option' ) : $blacklisted;
	//Turn WP Blacklist Words into Array
	$badWords = preg_split("/[\s,]+/", $blacklisted);

	if( empty( $badWords ) || sizeof( $badWords ) < 2 ) {
//		return $validation_result;
	}
	//Function to Check Submitted Field Value Against Blacklist Array. Will be Called in the Fields Loop.
	function contains($field_value, array $badWords){
		foreach($badWords as $i) {
			if(empty($i)) {
				continue;
			}
			if (stripos($field_value,$i) !== false)return true;
		}
		return false;
	}

	$form = $validation_result['form'];
	//Loop through Form Fields
	$phone_start = ['020', '0161', '028', '07', '20', '161', '28', '7'];
	foreach( $form['fields'] as &$field ) {
		//Store Submitted Field Value in a Local Variable
		$field_value = rgpost( "input_{$field['id']}" );
		//Use Function
		if ( contains( $field_value, $badWords ) ){
			// set the form validation to false
			$validation_result['is_valid'] = false;
			$field->failed_validation = true;
			$field->validation_message = 'This field contains bad words!';
			break;
		}

		if ( strtolower( $field->placeholder ) === 'telephone' || strtolower( $field->label ) === 'telephone' ) {
			$phone_valid = false;
			foreach( $phone_start as $starting_point ) {
				if ( str_starts_with( $field_value, $starting_point ) ) {
					$phone_valid = true;
				}
			}
			if ( ! $phone_valid ) {
				$validation_result['is_valid'] = false;
				$field->failed_validation = true;
				$field->validation_message = 'Invalid Phone number';
			}
		}


		else {
			continue;
		}
	}

	//Assign modified $form object back to the validation result
	$validation_result['form'] = $form;
	return $validation_result;
}

/** Remove Dashicons from Admin Bar for non logged in users **/
add_action('wp_print_styles', 'webpigment_remove_dashicon', 100);

/** Remove Dashicons from Admin Bar for non logged in users **/
function webpigment_remove_dashicon()
{
	if (!is_admin_bar_showing() && !is_customize_preview()) {
		wp_dequeue_style('dashicons');
		wp_deregister_style('dashicons');
	}
}

add_filter(
	'the_content',
	function( $content ) {
		if ( is_singular( array( 'post', 'page' ) ) && wp_is_mobile() && ! is_page_template( 'templates/take-the-test-template.php' ) && is_active_sidebar( 'after-breadcrumbs-mobile-sidebar' ) && ! is_front_page() && ! is_home() && ! is_page( 'about-us' ) && ! is_page( 'contact-us' ) && ! is_page( 'meet-the-team' ) ) {
			$paragraphs = explode( '</p>', $content );

			ob_start();
			dynamic_sidebar( 'after-breadcrumbs-mobile-sidebar' );
			$sidebar_output = ob_get_clean();

			array_splice( $paragraphs, 1, 0, $sidebar_output );

			$content = implode( '', $paragraphs );
		}

		return $content;
	}
);


function set_alt_text_from_title( $attachment_ID ) {
	// Get the attachment post object
	$attachment = get_post( $attachment_ID );

	// Set alt text only if it's empty
	if ( empty( get_post_meta( $attachment->ID, '_wp_attachment_image_alt', true ) ) ) {
		// Get the post object for the parent post of the attachment
		$parent_post = get_post( $attachment->post_parent );

		// Get the title of the parent post
		$post_title = $parent_post->post_title;

		// Set the alt text to be the same as the post title
		update_post_meta( $attachment->ID, '_wp_attachment_image_alt', $post_title );
	}
}
add_action( 'add_attachment', 'set_alt_text_from_title' );

function update_attachment_title_from_post_title( $attachment_ID ) {
	// Get the attachment post object
	$attachment = get_post( $attachment_ID );

	// Get the post object for the parent post of the attachment
	$parent_post = get_post( $attachment->post_parent );

	if ( $parent_post ) {
		// Get the title of the parent post
		$post_title = $parent_post->post_title;

		// Update the attachment title to be the same as the post title
		$attachment_data = array(
			'ID'         => $attachment->ID,
			'post_title' => $post_title
		);

		wp_update_post( $attachment_data );
	}
}

// Add action to update attachment title from post title
add_action( 'add_attachment', 'update_attachment_title_from_post_title' );

add_filter( 'gform_field_value_refurl', 'populate_referral_url');
 
function populate_referral_url( $value ){
    $refurl = $_SERVER['HTTP_REFERER'] ?? '';

	if ( empty( $refurl ) ) {
		return $refurl;
	}
 
    return esc_url_raw( $refurl );
}

// add_filter( 'wsp_pages_return', function( $return ) {
// 	var_dump( $return ); die;
// }, 20 );

function cd_disable_wp_responsive_images() {

	return 1;

}
add_filter('max_srcset_image_width', 'cd_disable_wp_responsive_images');

function cd_get_real_link( $link, $redirects ) {
	$no_domain_link = str_replace( trailingslashit( get_site_url() ), '/', $link );
	
	if ( ! empty( $redirects[ $link ] ) ) {
		return cd_get_real_link( $redirects[ $link ], $redirects );
	} elseif ( ! empty( $redirects[ $no_domain_link ] ) ) {
		return cd_get_real_link( $redirects[ $no_domain_link ], $redirects );
	}

	return $link;
}

function cd_modify_modified_post_date( $the_time, $format, $post ) {
	if ( ! $post || ! in_array( $post->post_type, array( 'post', 'page' ) ) ) {
		return $the_time;
	}

	if ( ! function_exists( 'get_field' ) ) {
		return $the_time;
	}

	$custom_publish_date = get_field( 'custom_publish_date', $post->ID );

	if ( empty( $custom_publish_date ) ) {
		return $the_time;
	}
	
	$format = ! empty( $format ) ? $format : get_option( 'date_format' );
	
	return gmdate( $format, strtotime( $custom_publish_date ) );
}
add_filter( 'get_the_modified_date', 'cd_modify_modified_post_date', 10, 3 );

add_filter( 'wp_head', 'cd_show_published_meta_tag_on_pages', 10, 2 );
function cd_show_published_meta_tag_on_pages() {
	if ( is_singular( 'page' ) ) {
		global $post;
		echo "\n<meta property='article:published_time' content='" . get_the_modified_date( 'c', $post->ID ) . "' />\n";
	}
}

add_filter('wpseo_schema_article', 'cd_yoast_json_ld_dates' );
add_filter('wpseo_schema_webpage', 'cd_yoast_json_ld_dates' );
function cd_yoast_json_ld_dates( $data ) {
    global $post;

    $modified_date = get_the_modified_date('c', $post->ID);

    if (isset($data['datePublished'])) {
        $data['datePublished'] = $modified_date;
    }

    if (isset($data['dateModified'])) {
        $data['dateModified'] = $modified_date;
    } else {
        $data['dateModified'] = $modified_date;
    }
    return $data;
}

add_filter( 'wp_schema_pro_schema_article', function( $schema, $data, $post ) {
	$schema['datePublished'] = get_the_modified_date( 'c', $post->ID );

	return $schema;
}, 10, 3 );

// Change Gravity Forms submit button text for sidebar callback form
add_filter( "gform_submit_button_41", function( $button, $form ) {
    return str_replace( "Submit", "Request a callback", $button );
}, 10, 2 );

// Change Gravity Forms submit button text for homepage contact form
add_filter( "gform_submit_button_44", function( $button, $form ) {
    return str_replace( "Submit", "Get in Touch", $button );
}, 10, 2 );

// Change Gravity Forms submit button text for footer CTA form (form 29)
add_filter( "gform_submit_button_29", function( $button, $form ) {
    return str_replace( "Submit", "Get in Touch", $button );
}, 10, 2 );


// Hide section sidebar menus and empty blocks from the take-the-test sidebar
// Only approved widgets should render: author, reviews, stressed guide, licensed, free insolvency, reviews.io
add_filter( 'sidebars_widgets', function( $sidebars_widgets ) {
	if ( isset( $sidebars_widgets['sidebar-take-the-test'] ) ) {
		$hidden = array( 'block-21', 'block-22' );
		$sidebars_widgets['sidebar-take-the-test'] = array_filter(
			$sidebars_widgets['sidebar-take-the-test'],
			function( $widget_id ) use ( $hidden ) {
				return ! in_array( $widget_id, $hidden, true );
			}
		);
	}
	return $sidebars_widgets;
} );

// Fix Yoast og:url on paginated archive pages
// Yoast outputs the base archive URL for og:url on paginated pages (e.g. /testimonials/page/2/
// gets og:url of /testimonials/). This filter corrects it to the actual paginated URL.
add_filter( 'wpseo_opengraph_url', function( $url ) {
	if ( is_paged() ) {
		return get_pagenum_link( get_query_var( 'paged' ) );
	}
	return $url;
} );

// Fix Schema Pro Article schema bugs (Schema Pro outputs lowercase @type and null description)
// Filter: wp_schema_pro_schema_article (class-bsf-aiosrs-pro-schema-article.php line 88)
add_filter( 'wp_schema_pro_schema_article', function( $schema, $data, $post ) {
	// Capitalize author @type: Schema Pro uses the raw field value (e.g. "person" not "Person")
	if ( isset( $schema['author']['@type'] ) ) {
		$schema['author']['@type'] = ucfirst( $schema['author']['@type'] );
	}
	// Remove null description: schema.org validators reject null values
	if ( array_key_exists( 'description', $schema ) && is_null( $schema['description'] ) ) {
		unset( $schema['description'] );
	}
	return $schema;
}, 10, 3 );

// Testimonials: Keep archive indexed in sitemap, noindex individual testimonial pages.
// Yoast toggle "Show testimonials in search results" must remain ON for the archive
// sitemap entry to be generated. This filter overrides individual posts back to noindex.
add_filter( 'wpseo_robots', function( $robots ) {
	if ( is_singular( 'testimonial' ) ) {
		return 'noindex, follow';
	}
	return $robots;
} );

// Exclude individual testimonials from Yoast XML sitemap.
// The "Show testimonials in search results" Yoast toggle must stay ON so the
// /testimonials/ archive URL appears in the sitemap. This filter removes
// individual testimonial post entries from the generated sitemap.
// Note: Yoast always passes 'post' as $type for all post types (line 224 of
// class-post-type-sitemap-provider.php), so check $post->post_type directly.
add_filter( 'wpseo_sitemap_entry', function( $entry, $type, $post ) {
	if ( isset( $post->post_type ) && $post->post_type === 'testimonial' ) {
		return false;
	}
	return $entry;
}, 10, 3 );


/**
 * Hub template card titles: promote <span class="cd-hub-card__title"> to <h4>
 * on hub_with_buttons pages so card titles are semantically headings (better
 * accessibility + SEO) and pick up the take-the-test h4 typography. Filter
 * the rendered post content rather than editing each page's database content,
 * so the change applies to every existing + future hub page automatically.
 */
add_filter( 'the_content', function( $content ) {
    if ( is_page_template( 'templates/content-page-hub_with_buttons.php' ) ) {
        $content = preg_replace(
            '#<span(\s+class="[^"]*cd-hub-card__title[^"]*"[^>]*)>(.*?)</span>#s',
            '<h4$1>$2</h4>',
            $content
        );
    }
    return $content;
}, 20 );


/**
 * Breadcrumb separator: replace default '/' with raquo '›' on templates that
 * use the v2 hero (take-the-test + content-page-hub_with_buttons). Filter the
 * Yoast SEO breadcrumb separator output.
 */
add_filter( 'wpseo_breadcrumb_separator', function( $separator ) {
    if ( is_page_template( 'templates/take-the-test-template.php' )
      || is_page_template( 'templates/content-page-hub_with_buttons.php' )
      || is_page_template( 'templates/content-meet-the-team.php' )
      || is_page_template( 'templates/content-full-width-page.php' )
      || is_page_template( 'templates/about-us.php' )
      || is_archive()
      || ( is_singular( 'post' ) && ( in_category( 'sectors' ) || in_category( 'services-to' ) ) )
      || ( is_singular( 'post' )
           && ! in_category( 'sectors' )
           && ! in_category( 'services-to' ) ) ) {
        return '<span class="bc-sep">&#8250;</span>';
    }
    return $separator;
} );

/**
 * Inject a `category-sectors` body class on single posts that use the
 * post-sectors template — that's both /sectors/* posts (in the 'sectors'
 * category) AND /services-to/* posts (in the 'services-to' category).
 * WP only emits category-<slug> classes on category archive views, not on
 * single-post views, so we mint the class manually for CSS targeting.
 *
 * The class name reflects the original /sectors/ rollout; we deliberately
 * re-use it for /services-to/ posts rather than introduce a parallel class
 * because the 200+ existing CSS rules apply identically to both URL
 * families (same template, same sections, same desired treatment). A
 * matching class is also added so PHP/JS can branch on either category.
 */
add_filter( 'body_class', function( $classes ) {
    if ( is_singular( 'post' ) && ( in_category( 'sectors' ) || in_category( 'services-to' ) ) ) {
        $classes[] = 'category-sectors';
    }
    return $classes;
} );

/**
 * Inject a `cd-ttt-design` body class on every page/post that uses the
 * take-the-test design system. That originally meant only pages using the
 * `take-the-test-template.php` page template — but as of 20260606 we
 * deploy the same hero + h-tag + sidebar + footer treatment to single
 * posts using the default post template (`single.php` → `content.php`),
 * which serve /articles/* and friends.
 *
 * Posts using the post-sectors template are EXCLUDED (they get
 * `category-sectors` instead — see the filter above) so their custom
 * services-to / sectors styling stays distinct.
 *
 * The 377 selectors in style.css that target this design system live on
 * `body.cd-ttt-design` (formerly `body.page-template-take-the-test-template`)
 * — the rename consolidates the design system into a single named scope
 * shared by both URL families.
 */
add_filter( 'body_class', function( $classes ) {
    if ( is_page_template( 'templates/take-the-test-template.php' ) ) {
        $classes[] = 'cd-ttt-design';
    } elseif ( is_singular( 'post' )
               && ! in_category( 'sectors' )
               && ! in_category( 'services-to' ) ) {
        /* Single posts NOT on the post-sectors template — these use
         * single.php + template-parts/content.php (post-template-default). */
        $classes[] = 'cd-ttt-design';
    }
    return $classes;
} );


/**
 * Reading time in minutes for the given post (or current post in loop).
 * Word count uses raw $post->post_content (no filter chain) to keep render
 * cheap (~1ms). 220 wpm is a comfortable read speed for dense UK insolvency
 * content. Floors at 1 minute so very short posts still show '1min read'.
 */
function cd_reading_time_minutes( $post = null ) {
    $post = get_post( $post );
    if ( ! $post ) {
        return 1;
    }
    $text = wp_strip_all_tags( (string) $post->post_content );
    $words = str_word_count( $text );
    if ( $words < 1 ) {
        return 1;
    }
    $minutes = (int) ceil( $words / 220 );
    return max( 1, $minutes );
}
