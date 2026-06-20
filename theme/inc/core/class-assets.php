<?php
namespace CD\Core;

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
class Assets {
	use \CD\Traits\Singleton;
	/**
	 * Initialize
	 *
	 * @return  void
	 */
	private function initialize() {
		self::old_assets();
	}

	private function old_assets() {
		wp_register_script( 'cd-old-tabs', CD_THEME_URL . '/old-assets/dist/js/tabs.js', array( 'jquery' ), filemtime( CD_THEME_DIR . '/old-assets/dist/js/tabs.js'), true );
		wp_register_script( 'cd-old-frontend', CD_THEME_URL . '/old-assets/dist/js/frontend.js', array( 'jquery' ), filemtime( CD_THEME_DIR . '/old-assets/dist/js/frontend.js'), true );
		wp_register_script( 'cd-old-quiz-insolvency', CD_THEME_URL . '/old-assets/dist/js/quiz-insolvency.js', array( 'jquery' ), filemtime( CD_THEME_DIR . '/old-assets/dist/js/quiz-insolvency.js'), true );
		wp_register_script( 'cd-old-form-letter', CD_THEME_URL . '/old-assets/dist/js/form-letter.js', array( 'jquery' ), filemtime( CD_THEME_DIR . '/old-assets/dist/js/form-letter.js'), true );
		wp_register_style( 'cd-old-quiz-insolvency-css', CD_THEME_URL . '/old-assets/dist/css/quiz-insolv-style.css' );
		$this->enqueue_scripts( ['cd-old-frontend'] );
	}

	/**
	 * Enqueue scripts called from the template files.
	 *
	 * @param array $scripts List of scripts that need to be enqueued.
	 *
	 * @return void
	 */
	public function enqueue_scripts( array $scripts ) {
		foreach( $scripts as $script ) {
			wp_enqueue_script( $script );
			wp_enqueue_style( $script . '-css' );
		}
	}
}