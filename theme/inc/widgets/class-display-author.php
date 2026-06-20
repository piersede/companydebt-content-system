<?php

namespace CD\Widgets;

class Display_Author extends \WP_Widget {
	function __construct() {
		parent::__construct(
			'cd_author_widget',
			__( 'CD Author Widget', 'cd20' ),
			array(
				'description' => __( 'Displays Author Information', 'cd20' ),
				'classname'   => 'widget__author'
			)
		);
	}

	// Widget front-end
	public function widget( $args, $instance ) {
		// before and after widget arguments are defined by themes
		$author_id = get_the_author_meta( 'ID' );
		$user_info = get_userdata( $author_id );
		$role      = '';
		if ( $user_info ) {
			$role = $user_info->roles[0];
		}

		if ( 'author' === $role ) {
			echo $args['before_widget'];

			$author_position       = get_field( 'professional_position', 'user_' . $author_id );
			$author_business_lines = get_field( 'business_lines', 'user_' . $author_id );
			$author_url            = get_author_posts_url( $author_id );
			$author_avatar         = wp_get_attachment_image(
				get_field( 'photo', 'user_' . $author_id ),
				[ 100, 100 ],
				null,
				array( "class" => "cd__author-photo  widget__author-photo" ) );

			$author_name = $user_info->data->display_name;
			?>
			<div class="widget__author__top"
				 style="align-items: center;
				 	display: flex;">
				<a href="<?php echo $author_url; ?>">
					<?php echo $author_avatar; ?>
				</a>
				<div class="widget__author__text">
					<a href="<?php echo $author_url; ?>" class="widget__author-name"><?php echo $author_name; ?></a>
					<div class="widget__author-position"><?php echo $author_position . '<br>' . $author_business_lines; ?> </div>

					<div class="widget__author-position  widget__author-date_published">
						<?php the_modified_date(); ?>
					</div>
				</div>
			</div>
			<?php if ( $author_position ) { ?>

				<?php
				echo $args['after_widget'];
			}
		}
	}

	// Widget Backend
	public function form( $instance ) {
		global $files_widgets;
		$files_widgets ++;
		// Widget admin form
	}

	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance ) {
		$instance = array();

		return $instance;
	}

}

