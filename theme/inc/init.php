<?php
/**
 * Include php scrips and classes
 *
 * @package CD
 */

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

require_once CD_THEME_DIR . 'inc/core/autoloader.php';

if ( class_exists( '\ACF' ) ) {
	CD\Core\ACF::get_instance();
} else {
	add_action(
		'wp',
		function() {
			// Fallback function so we don't need to check every time if it exists.
			if ( ! function_exists( 'get_field' ) ) {
				/**
				 * Return meta field
				 *
				 * @param   string $selector      The selector.
				 * @param   int    $post_id       The post id.
				 * @param   bool   $format_value  Return array or format it to single value.
				 *
				 * @return  string
				 */
				function get_field( $selector, $post_id = false, $format_value = true ) {
					return '';
				}

				/**
				 * Print meta field
				 *
				 * @param   string $selector      The selector.
				 * @param   int    $post_id       The post id.
				 * @param   bool   $format_value  Return array or format it to single value.
				 *
				 * @return  void
				 */
				function the_field( $selector, $post_id = false, $format_value = true ) {
					echo '';
				}

				/**
				 * Return sub meta field
				 *
				 * @param   string $selector      The selector.
				 * @param   int    $post_id       The post id.
				 * @param   bool   $format_value  Return array or format it to single value.
				 *
				 * @return  string
				 */
				function get_sub_field( $selector, $post_id = false, $format_value = true ) {
					return '';
				}

				/**
				 * Print sub meta field
				 *
				 * @param   string $selector      The selector.
				 * @param   int    $post_id       The post id.
				 * @param   bool   $format_value  Return array or format it to single value.
				 *
				 * @return  void
				 */
				function the_sub_field( $selector, $post_id = false, $format_value = true ) {
					echo '';
				}
			}
		}
	);
}

// Global.
CD\Core\Widgets::get_instance();
CD\Gravity_Forms_API::get_instance();
CD\Posts_Per_Page::get_instance();

if ( is_admin() ) {
	// WP Dashboard side.
} else {
	// Public side.
}
