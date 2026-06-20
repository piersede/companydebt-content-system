<?php

namespace CD\Widgets;

class Download_Guide extends \WP_Widget {

	function __construct() {
		parent::__construct(
			'cd_pdf_widget',
			__( 'CD Download File Widget', 'cd20' ),
			array(
				'description' => __( 'Displays Debtors Guide', 'cd20' ),
				'classname'   => 'widget__download',
			)
		);
	}

	// Creating widget front-end
	public function widget( $args, $instance ) {
		// Defining Variables

		$title    = $instance['title'];
		$image_id = $instance['image_id'];
		$link     = $instance['link'];

		if ( empty( $link ) ) {
			$link = 'https://www.companydebt.com';
		}

		// before and after widget arguments are defined by themes
		echo $args['before_widget'];


		?>
<!--<div class="container">-->
		<a href="<?php echo $link; ?>" class="widget__download-container">
			<div class="widget__download-left">
				<?php echo wp_get_attachment_image( $image_id, array(
					93,
					114
				), false, array( 'class' => 'widget__download-image' ) ); ?>
			</div>
			<div class="widget__download-right">
				<div class="widget__download-supertitle">DOWNLOAD OUR</div>
				<?php if ( ! empty( $title ) ) { ?>
					<div class="widget__download-title"><?php echo $title; ?></div>
				<?php } ?>
				<div class="widget__download-button  button">Get it Now</div>
			</div>
		</a>
<!--</div>-->
		<?php
		echo $args['after_widget'];
	}

	// Widget Backend
	public function form( $instance ) {
		if ( isset( $instance['title'] ) ) {
			$title = $instance['title'];
		}
		if ( ! empty( $instance['link'] ) ) {
			$link = $instance['link'];
		} else {
			$link = 'Your Hyperlink Here...';
		}

		if ( ! empty ( $instance['image_id'] ) ) {
			$image_id = $instance['image_id'];
		} else {
			$image_id = 'Your Image ID Here...';
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
			<label for="<?php echo $this->get_field_id( 'link' ); ?>"><?php _e( 'URL', 'cd20' ); ?></label>
			<input class="widefat" id="<?php echo $this->get_field_id( 'link' ); ?>"
				   name="<?php echo $this->get_field_name( 'link' ); ?>" type="text"
				   value="<?php echo esc_attr( $link ); ?>"/>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'image_id' ); ?>"><?php _e( 'Image ID', 'cd20' ); ?></label>
			<input type="text" class="widefat custom_media_url custom_media_button-<?php echo $files_widgets; ?>"
				   name="<?php echo $this->get_field_name( 'image_id' ); ?>"
				   id="<?php echo $this->get_field_id( 'image_id' ); ?>" value="<?php echo $image_id; ?>"
				   style="margin-top:5px;">
		</p>
		<?php
	}

	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance ) {
		$instance             = $old_instance;
		$instance['title']    = ( ! empty( $new_instance['title'] ) ) ? ( $new_instance['title'] ) : '';
		$instance['link']     = ( ! empty( $new_instance['link'] ) ) ? strip_tags( $new_instance['link'] ) : '';
		$instance['image_id'] = ( ! empty( $new_instance['image_id'] ) ) ? strip_tags( $new_instance['image_id'] ) : '';

		return $instance;
	}
} // Class wpb_widget ends here

