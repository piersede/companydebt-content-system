<?php
/**
 * Description

 */

namespace CD\Core;


class Widgets
{
	use \CD\Traits\Singleton;
	/**
	 * Initialize
	 *
	 * @return  void
	 */
	private function initialize() {
		add_action( 'widgets_init', array( $this, 'register_widgets' ) );
	}

	public function register_widgets()
	{
		register_widget( 'CD\Widgets\CTA_Title_Description_Phone' );
		register_widget( 'CD\Widgets\Display_Author' );
		register_widget( 'CD\Widgets\Download_Guide' );
		register_widget( 'CD\Widgets\Download_Guide_Design_2022_V1' );
		register_widget( 'CD\Widgets\Gravity_Form_With_Title_And_Bulletins' );
		register_widget( 'CD\Widgets\Show_Related_Menu' );
		register_widget( 'CD\Widgets\Related_Pages' );
		register_widget( 'CD\Widgets\Social_Share' );
		register_widget( 'CD\Widgets\Table_Of_Content' );
		register_widget( 'CD\Widgets\Video' );
	}
}

