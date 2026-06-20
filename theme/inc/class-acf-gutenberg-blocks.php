<?php
/**
 * Register ACF Guttenberg Blocks
 *
 * @package MartinCV
 */


// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * ACF Guttenberg Blocks Class
 */
class ACF_Guttenberg_Blocks {


	/**
	 * Initialize
	 *
	 * @return  void
	 */
	public function __construct() {
		add_action( 'acf/init', array( $this, 'register_blocks' ) );
		add_action( 'init', array( $this, 'register_blocks_new' ) ) ;
	}

	/**
	 * Register blocks the new way since ACF 6.0
	 *
	 * @return void 
	 */
	public function register_blocks_new() {
		register_block_type( CD_THEME_DIR . '/blocks/cd-gravity-form-with-title-and-bulletins-widget' );
		register_block_type( CD_THEME_DIR . '/blocks/cd-reviews-widget' );
		register_block_type( CD_THEME_DIR . '/blocks/cd-reviews-widget-sidebar' );
	}

	/**
	 * Register ACF Guttenberg Blocks
	 *
	 * @return  void
	 */
	public function register_blocks() {
		if ( ! function_exists( 'acf_register_block' ) ) {
			return;
		}


		acf_register_block(
			array(
				'name'            => 'hero-blue',
				'title'           => __( 'Hero Front Page CD' ),
				'description'     => __( 'Hero Front Page CD Block' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'hero', 'home', 'Cd20', 'cd', 'blue' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'show-sectors',
				'title'           => __( 'Show Sectors Front Page CD' ),
				'description'     => __( 'Show Sectors Front Page CD Block.' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'show', 'sectors', 'Cd20', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'columns-with-buttons',
				'title'           => __( 'Columns with Buttons CD' ),
				'description'     => __( 'Columns with Buttons (2-4 cols) CD Block' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'box', 'columns', 'button', 'cd', ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'wysiwyg',
				'title'           => __( 'Wysiwyg CD' ),
				'description'     => __( 'Wysiwyg CD Block' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'wysiwyg', 'cd' ),
			)
		);

		// acf_register_block(
		// 	array(
		// 		'name'            => 'cd-gravity-form-with-title-and-bulletins-widget',
		// 		'title'           => __( 'CD Gravity Form with Title and Bulletins' ),
		// 		'description'     => __( 'CD Gravity Form with Title and Bulletins Widget' ),
		// 		'render_callback' => array( $this, 'render_block' ),
		// 		'enqueue_style' => get_template_directory_uri() . '/public/gutenberg-blocks/cd-gravity-form-with-title-and-bulletins-widget.css',
		// 		'enqueue_assets'  => array( $this, 'load_assets' ),
		// 		'category'        => 'formatting',
		// 		'icon'            => 'admin-comments',
		// 		'keywords'        => array( 'widget', 'cd' ),
		// 	)
		// );

		acf_register_block(
			array(
				'name'            => 'tilted_content_two_cols',
				'title'           => __( 'Tilted Content 2 Columns CD' ),
				'description'     => __( 'Tilted Content Two Columns CD Block' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'tilted', 'two', 'about', 'us', 'Cd20', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'accordion',
				'title'           => __( 'Accordion CD' ),
				'description'     => __( 'Accordion CD Block' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'accordion', 'about', 'us', 'Cd20', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'bottom-line',
				'title'           => __( 'Bottom Line CD' ),
				'description'     => __( 'Bottom Line CD Block' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'bottom', 'line', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'cd-download-file-widget',
				'title'           => __( 'CD Download File Widget' ),
				'description'     => __( 'CD Download File Widget Widget' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'widget', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'cd-related-menu-widget',
				'title'           => __( 'CD Related Menu Widget' ),
				'description'     => __( 'CD Related Menu Widget' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'widget', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'hub-with-buttons',
				'title'           => __( 'HUB with buttons' ),
				'description'     => __( 'HUB with buttons' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'hub', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'tabs',
				'title'           => __( 'TABS' ),
				'description'     => __( 'Tabs' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'tab', 'cd' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'landing-blank-hero',
				'title'           => __( 'Hero Blank Landing CD' ),
				'description'     => __( 'Hero Blank Landing CD' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'hero', 'home' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'hero-landing',
				'title'           => __( 'Hero Landing CD' ),
				'description'     => __( 'Hero on Landing Page without header CD' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'hero', 'home' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'carousel-testimonials-landing',
				'title'           => __( 'Carousel Testimonials Landing CD' ),
				'description'     => __( 'Carousel Testimonials Landing with boxes and 2 slides on desktop CD' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'testimonial', 'carousel', 'home' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'landing-insolvency-hero',
				'title'           => __( 'Hero Insolvency Landing CD' ),
				'description'     => __( 'Hero Block for Landing Page for Insolvency without header CD' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'hero', 'landing', 'insolvency' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'landing-insolvency-timeline',
				'title'           => __( 'Landing Insolvency Timeline' ),
				'description'     => __( 'Timeline Block for Landing Page for Insolvency' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'timeline', 'landing', 'insolvency' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'landing-insolvency-quote',
				'title'           => __( 'Landing Insolvency Quote' ),
				'description'     => __( 'Quote Block for Landing Page for Insolvency without header' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'quote', 'landing', 'insolvency' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'landing-insolvency-accordion',
				'title'           => __( 'Landing Insolvency Accordion' ),
				'description'     => __( 'Accordion Block for Landing Page for Insolvency' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'accordion', 'landing', 'insolvency' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'hub-box',
				'title'           => __( 'Hub Box' ),
				'description'     => __( 'Hub Box' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'hub', 'box' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'cd-author-box-widget',
				'title'           => __( 'Author Box' ),
				'description'     => __( 'Author Box' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'author', 'box' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'columns-full-width',
				'title'           => __( 'Columns Full Width' ),
				'description'     => __( 'Columns Full Width' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'columns', 'fullwidth' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'left-right-wyswyg-and-background-image',
				'title'           => __( 'Left - Right Wyswyg and Background Image' ),
				'description'     => __( 'Left - Right Wyswyg and Background Image' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'left', 'right', 'wyswyg'),
			)
		);

		acf_register_block(
			array(
				'name'            => 'two-halfs-full-width',
				'title'           => __( 'Two Halfs Full Width' ),
				'description'     => __( 'Two Halfs Full Width' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'two', 'halfs', 'wyswyg'),
			)
		);

		acf_register_block(
			array(
				'name'            => 'toc',
				'title'           => __( 'TOC' ),
				'description'     => __( 'TOC' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'toc' ),
			)
		);

		acf_register_block(
			array(
				'name'            => 'cd-list-with-button',
				'title'           => __( 'List With CTA Button' ),
				'description'     => __( 'List With CTA Button' ),
				'render_callback' => array( $this, 'render_block' ),
				'enqueue_assets'  => array( $this, 'load_assets' ),
				'category'        => 'formatting',
				'icon'            => 'admin-comments',
				'keywords'        => array( 'list', 'cta', 'button' ),
			)
		);
	}

	/**
	 * Render the ACF Guttenberg block
	 *
	 * @param   array $block  Block data.
	 *
	 * @return  void
	 */
	public function render_block( $block ) {
		$slug = str_replace( 'acf/', '', $block['name'] );
		if ( file_exists( get_template_directory() . "/template-parts/blocks/content-{$slug}.php" ) ) {
			require get_template_directory() . "/template-parts/blocks/content-{$slug}.php";
		}
	}

	/**
	 * Load block assets
	 *
	 * @param   array $block  Block data.
	 *
	 * @return  void
	 */
	public function load_assets( $block ) {
		$slug = str_replace( 'acf/', '', $block['name'] );

		if ( file_exists( CD_THEME_DIR . 'public/gutenberg-blocks/' . $slug . '.css' ) ) {
			wp_enqueue_style(
				$slug,
				get_template_directory_uri() . '/public/gutenberg-blocks/' . $slug . '.css',
				array(),
				1
			);
		}

		if ( file_exists( CD_THEME_DIR . 'assets/js/gutenberg-blocks/' . $slug . '.js' ) ) {
			wp_enqueue_style(
				'slick-slider',
				CD_THEME_URL . 'assets/libs/slick/slick.css',
				array(),
				1
			);

			wp_register_script(
				'slick-slider',
				CD_THEME_URL . 'assets/libs/slick/slick.min.js',
				array(),
				1,
				true
			);

			wp_enqueue_script(
				'gb-' . $slug,
				CD_THEME_URL . 'assets/js/gutenberg-blocks/' . $slug . '.js',
				array( 'slick-slider' ),
				1,
				true
			);
		}
	}
}


if( function_exists('acf_add_options_page') ) {

	acf_add_options_page(array(
		'page_title' 	=> 'CD Theme Settings',
		'menu_title'	=> 'CD Theme Settings',
		'menu_slug' 	=> 'theme-general-settings',
		'capability'	=> 'edit_posts',
		'redirect'		=> false
	));

	acf_add_options_sub_page(array(
		'page_title' 	=> 'General Theme Settings',
		'menu_title'	=> 'General Theme Settings',
		'parent_slug'	=> 'theme-general-settings',
	));

	acf_add_options_sub_page(array(
		'page_title' 	=> 'Site Footer Section',
		'menu_title'	=> 'Site Footer Section',
		'parent_slug'	=> 'theme-general-settings',
	));

	acf_add_options_sub_page(array(
		'page_title' 	=> 'Page Footer Section',
		'menu_title'	=> 'Page Footer Section',
		'parent_slug'	=> 'theme-general-settings',
	));

	acf_add_options_sub_page(array(
		'page_title' 	=> 'Footnotes',
		'menu_title'	=> 'Footnotes',
		'parent_slug'	=> 'theme-general-settings',
	));

}


new ACF_Guttenberg_Blocks();