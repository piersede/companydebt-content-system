<?php
/**
 * Description
 */

namespace CD;

class Gravity_Forms_API {
	use \CD\Traits\Singleton;

	public function initialize() {
		add_action( 'wp_enqueue_scripts', array( $this, 'localize_script'), 11 );
		add_filter( 'gform_confirmation_anchor', '__return_true' );
	}

	public function localize_script() {
		$web_site = home_url();

		switch ( $web_site ) {
			case 'http://cd21.local':
				$gf_api_keys = array(
					'key'    => 'ck_06466172214d3a12c33cb880aa7878c25012b2d5',
					'secret' => 'cs_9aa80b031814443376e9b3b19e3efd23c998095e',
				);
				break;

			case 'https://comdebstage.wpengine.com':
				$gf_api_keys = array(
					'key'    => 'ck_40a4fda5fd5e0169847e60d527add9d5ce21b26f',
					'secret' => 'cs_0134f4093e9aa0e5274e61578824cf66ba417464',
				);
				break;

			case 'https://www.companydebt.com':
				$gf_api_keys = array(
					'key'    => 'ck_d724c858116b637cabf80face1bbc4f3665f5514',
					'secret' => 'cs_65ce9c87a5721864d9f82fb997abd3529ec54f35',
				);
				break;
			default:
				$gf_api_keys = array(
					'key'    => 'ck_06466172214d3a12c33cb880aa7878c25012b2d5',
					'secret' => 'cs_9aa80b031814443376e9b3b19e3efd23c998095e',
				);
		}
		wp_localize_script( 'company-debt-webpigment-global', 'gfApiKeys', $gf_api_keys );
	}
}
