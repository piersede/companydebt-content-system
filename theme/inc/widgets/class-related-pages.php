<?php

namespace CD\Widgets;

class Related_Pages extends \WP_Widget {
	public function __construct() {
		parent::__construct(
			'CD_Related_Pages_Widget',
			__( 'CD Related Pages Widget', 'cd20' ),
			array(
				'description' => __( 'Displays Related Pages', 'cd20' ),
				'classname'   => 'widget__related-pages'
			)
		);
	}

	public function widget( $args, $instance ) {
		$has_no_related_pages = get_field( 'topical_from_hub' );
		$related_pages_list   = get_field( 'related_pages_list' );
		if ( ! $has_no_related_pages && '' != $related_pages_list ) {

			$secton_title = get_field( 'topical_content_heading' );

			if ( ! $secton_title ) {
				$secton_title = 'Related Content';
			}

			echo $args['before_widget'];

			?>
			<div class="widget__related-pages__title"><?php echo $secton_title; ?></div>
			<div class="widget__related-pages--mobile-close"></div>
			<div class="widget__related-pages__container">
				<?php foreach ( $related_pages_list as $related_page ) { ?>
						<a href="<?php echo get_permalink( $related_page ); ?>" class="widget__related-pages__item">
							<div class="widget__related-pages__item-text"><?php echo get_the_title( $related_page ); ?></div>
						</a>
				<?php } ?>
			</div>
			<?php
			echo $args['after_widget'];
		}
	}
}

