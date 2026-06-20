<?php

namespace CD\Widgets;

class Video extends \WP_Widget {

	function __construct() {
		parent::__construct(
			'cd_video_widget',
			__( 'CD Video File Widget', 'cd20' ),
			array(
				'description' => __( 'Plays Full Screen Video', 'cd20' ),
				'classname'   => 'widget__video',
			)
		);
	}

	// Creating widget front-end
	public function widget( $args, $instance ) {
		// Defining Variables

		$title    = $instance['title'];
		$image_id = $instance['image_id'];
		$embed    = $instance['embed'];

		echo $args['before_widget'];

		?>

		<div class="widget__video-title"
			 style="font-weight:700;
			padding-bottom: 15px;"><?php echo $title; ?></div>
		<div class="widget__video-image"
			 style="padding-bottom: 15px;"><?php echo wp_get_attachment_image( $image_id, array(
				246,
				"auto"
			), false, array( 'class' => 'widget__video-image' ) ); ?></div>
		<div class="widget__video-bcg">
			<div class="widget__video-iframe"><?php echo $embed; ?></div>
		</div>
		<?php
		echo $args['after_widget'];
	}

	// Widget Backend
	public function form( $instance ) {
		if ( ! empty( $instance['title'] ) ) {
			$title = $instance['title'];
		}
		if ( ! empty( $instance['image_id'] ) ) {
			$image_id = $instance['image_id'];
		}
		if ( ! empty( $instance['embed'] ) ) {
			$embed = $instance['embed'];
		} else {
			$embed = 'Your Embed Here...';
		}

		global $files_widgets;
		$files_widgets ++;

		// Widget admin form
		?>
		<p>
			<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e( 'Title:', 'cd20' ); ?></label>
			<input class="widefat" id="<?php echo $this->get_field_id( 'title' ); ?>"
				   name="<?php echo $this->get_field_name( 'title' ); ?>" type="text"
				   value="<?php echo $title; ?>"/>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'image_id' ); ?>"><?php _e( 'Image:', 'cd20' ); ?></label>
			<input class="widefat" id="<?php echo $this->get_field_id( 'image_id' ); ?>"
				   name="<?php echo $this->get_field_name( 'image_id' ); ?>" type="text"
				   value="<?php echo $image_id; ?>"/>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'embed' ); ?>"><?php _e( 'Embed', 'cd20' ); ?></label>
			<textarea class="widefat" id="<?php echo $this->get_field_id( 'embed' ); ?>"
				   name="<?php echo $this->get_field_name( 'embed' ); ?>"><?php echo $embed; ?>"</textarea>
		</p>
		<?php
	}

	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance ) {
		$instance             = $old_instance;
		$instance['title']    = ( ! empty( $new_instance['title'] ) ) ? ( $new_instance['title'] ) : '';
		$instance['image_id'] = ( ! empty( $new_instance['image_id'] ) ) ? ( $new_instance['image_id'] ) : '';
		$instance['embed']    = ( ! empty( $new_instance['embed'] ) ) ? ( $new_instance['embed'] ) : '';


		return $instance;
	}
} // Class wpb_widget ends here

