<?php

namespace CD\Widgets;

class Reviewed_By extends \WP_Widget {
	function __construct() {
		parent::__construct(
			'cd_reviewed_by_widget',
			__( 'CD Reviewed By Widget', 'cd20' ),
			array(
				'description' => __( 'Displays Reviewed By author info in sidebar', 'cd20' ),
				'classname'   => 'widget__reviewed-by'
			)
		);
	}

	public function widget( $args, $instance ) {
		$author_id   = get_the_author_meta( 'ID' );
		if ( ! $author_id ) {
			return;
		}
		$author_name = get_the_author_meta( 'display_name' );
		if ( ! $author_name ) {
			return;
		}
		$photo_id    = function_exists('get_field') ? get_field( 'photo', 'user_' . $author_id ) : null;
		// Pull credential dynamically from the author's `professional_position` ACF user field
		// (same field used by /meet-the-team/ + /template-parts/footer/footer-author/).
		// If empty, hide the credential line entirely — safer than the prior hardcoded
		// "Licensed Insolvency Practitioner" which misattributed non-IP authors.
		$credential  = function_exists('get_field') ? get_field( 'professional_position', 'user_' . $author_id ) : '';
		$mod_date    = get_the_modified_date( 'd/m/Y' );

		echo $args['before_widget'];
		?>
		<div class="widget-reviewed-by">
			<div class="widget-reviewed-by__inner">
				<?php if ( $photo_id ) : ?>
					<?php echo wp_get_attachment_image( $photo_id, 'thumbnail', false, [
						'class'  => 'widget-reviewed-by__photo',
						'alt'    => $author_name,
						'width'  => '80',
						'height' => '80',
					] ); ?>
				<?php endif; ?>
				<div class="widget-reviewed-by__text">
					<div class="widget-reviewed-by__name"><strong><?php echo esc_html( $author_name ); ?></strong></div>
					<?php if ( ! empty( $credential ) ) : ?>
						<div class="widget-reviewed-by__credential"><?php echo esc_html( $credential ); ?></div>
					<?php endif; ?>
					<div class="widget-reviewed-by__date">
						<strong>Reviewed on</strong> <?php echo esc_html( $mod_date ); ?>
					</div>
				</div>
			</div>
		</div>
		<?php
		echo $args['after_widget'];
	}

	public function form( $instance ) {}
	public function update( $new_instance, $old_instance ) { return array(); }
}
