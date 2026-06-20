<?php

namespace CD\Widgets;

class Show_Related_Menu extends \WP_Widget {
	public function __construct() {
		parent::__construct(
			'CD_Related_Menu_Widget',
			__( 'CD Related Menu Widget', 'cd20' ),
			array(
				'description' => __( 'Displays Related Menu', 'cd20' ),
				'classname'   => 'widget__menu'
			)
		);
	}

	public function widget( $args, $instance ) {
		if ( ! is_admin() ) {
			$menu_name = get_field( 'sidebar_menu_select' );

			if ( $menu_name && 'none' !== $menu_name['label'] ) {
				echo $args['before_widget'];
				echo '<div class="widget__menu-title">' . $menu_name['label'] . ' Menu' . '</div>';
				?>
				<div class="widget__menu-mobile-close"></div>
				<?php
				if ( $menu_name['label'] !== '0' ) {
					wp_nav_menu(
						array(
							'menu'        => $menu_name['value'],
							'container'   => 'false',
							'menu_class'  => 'widget__menu-menu',
							'link_before' => '<span class="menu-item-text">',
							'link_after'  => '</span>' .
							                 '<span class="menu-item-text__arrow"></span>'

						)
					);
				}
				echo $args['after_widget'];
			}
		}
	}

	public function form( $instance ) {
		?>
		<div>Show Related menu</div>
		<?php
	}
}

