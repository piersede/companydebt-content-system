<?php
/**
 * ACF Class
 *
 * @package CD
 */

namespace CD\Core;

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * ACF
 */
class ACF {
	use \CD\Traits\Singleton;

	/**
	 * Initialize
	 *
	 * @return  void
	 */
//	private function initialize() {
//		acf_add_options_page(
//			array(
//				'page_title' => __( 'CD Подесувања', 'ppp' ),
//				'menu_title' => __( 'CD Подесувања', 'ppp' ),
//				'menu_slug'  => 'cd-settings',
//				'capability' => 'administrator',
//				'redirect'   => false,
//			)
//		);
//	}
}
