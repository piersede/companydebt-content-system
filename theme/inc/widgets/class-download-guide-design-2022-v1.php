<?php

namespace CD\Widgets;

class Download_Guide_Design_2022_V1 extends \WP_Widget {

	function __construct() {
		parent::__construct(
			'cd_download_design_2022_v1_widget',
			__( 'CD Download File Widget Design 2022 v1', 'cd20' ),
			array(
				'description' => __( 'Download File Widget Design 2022 v1', 'cd20' ),
				'classname'   => 'widget__download_d22_1   widget__gf',
			)
		);
	}

	// Creating widget front-end
	public function widget( $args, $instance ) {
		// Defining Variables

		$title                = $instance['title'];
		$image_id             = $instance['image_id'];
		$button               = $instance['button'];
		$lightbox_title       = $instance['lightbox_title'];
		$lightbox_description = $instance['lightbox_description'];
		$lightbox_form        = $instance['lightbox_form'];

		if ( empty( $button ) ) {
			$button = 'https://www.companydebt.com';
		}

		// before and after widget arguments are defined by themes
		echo $args['before_widget'];


		?>
		<div class="widget__download-container">
			<?php if ( ! empty( $title ) ) { ?>
				<div class="widget__download-title"><?php echo $title; ?></div>
			<?php } ?>

			<div class="widget__download-inner">
				<?php echo wp_get_attachment_image( $image_id, array(
					126,
					208
				), false, array( 'class' => 'widget__download-image' ) ); ?>
				<div class="widget__download-button  widget__download_d22_1-button button">
					<img width="30" height="30" src="<?php echo CD_THEME_URL . '/dist/images/icon-pdf.png'; ?>"
						 alt="psf icon">
					<div class="widget__download-button__text"><?php echo $button; ?></div>
				</div>
			</div>
		</div>

		<div class="widget__download-lightbox">
			<div class="widget__download-lightbox__container">
				<div class="widget__download-lightbox-left">
					<div class="widget__download-lightbox__title"><?php echo $lightbox_title; ?></div>
					<div class="widget__download-lightbox__desc"><?php echo $lightbox_description; ?></div>
					<div class="widget__gftb-form"><?php gravity_form( $lightbox_form, false, false, false, null, true ); ?></div>
				</div>
				<div class="widget__download-lightbox-right">
					<?php echo wp_get_attachment_image( $image_id, array(
						211,
						348
					), false, array( 'class' => 'widget__download-image' ) ); ?>
				</div>
			<div class="widget__download-lightbox__container-close"></div>
			</div>

		</div>
		<?php
		echo $args['after_widget'];
	}

	// Widget Backend
	public function form( $instance ) {
		if ( isset( $instance['title'] ) ) {
			$title = $instance['title'];
		}
		if ( ! empty( $instance['button'] ) ) {
			$button = $instance['button'];
		} else {
			$button = 'Your Hyperbutton Here...';
		}

		if ( ! empty ( $instance['image_id'] ) ) {
			$image_id = $instance['image_id'];
		} else {
			$image_id = 'Your Image ID Here...';
		}

		if ( ! empty ( $instance['lightbox_title'] ) ) {
			$lightbox_title = $instance['lightbox_title'];
		} else {
			$lightbox_title = 'Your Lightbox Title Here...';
		}

		if ( ! empty ( $instance['lightbox_description'] ) ) {
			$lightbox_description = $instance['lightbox_description'];
		} else {
			$lightbox_description = 'Your Lightbox Description Here...';
		}

		if ( ! empty ( $instance['lightbox_form'] ) ) {
			$lightbox_form = $instance['lightbox_form'];
		} else {
			$lightbox_form = 'Your Lightbox Form ID Here...';
		}


		global $files_widgets;
		$files_widgets ++;

		// Widget admin form
		?>
		<!--		<p>-->
		<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e( 'Title:', 'cd20' ); ?></label>
		<input class="widefat" id="<?php echo $this->get_field_id( 'title' ); ?>"
			   name="<?php echo $this->get_field_name( 'title' ); ?>" type="text"
			   value="<?php echo $title; ?>"/>
		<!--		</p>-->
		<!--		<p>-->
		<label for="<?php echo $this->get_field_id( 'button' ); ?>"><?php _e( 'Button Text', 'cd20' ); ?></label>
		<input class="widefat" id="<?php echo $this->get_field_id( 'button' ); ?>"
			   name="<?php echo $this->get_field_name( 'button' ); ?>" type="text"
			   value="<?php echo esc_attr( $button ); ?>"/>
		<!--		</p>-->
		<!--		<p>-->
		<label for="<?php echo $this->get_field_id( 'image_id' ); ?>"><?php _e( 'Image ID', 'cd20' ); ?></label>
		<input type="text" class="widefat custom_media_url custom_media_button-<?php echo $files_widgets; ?>"
			   name="<?php echo $this->get_field_name( 'image_id' ); ?>"
			   id="<?php echo $this->get_field_id( 'image_id' ); ?>" value="<?php echo $image_id; ?>"
			   style="margin-top:5px;">
		<!--		</p>-->
		<!--		<p>-->
		<label for="<?php echo $this->get_field_id( 'lightbox_title' ); ?>"><?php _e( 'Lightbox Title:', 'cd20' ); ?></label>
		<input class="widefat" id="<?php echo $this->get_field_id( 'lightbox_title' ); ?>"
			   name="<?php echo $this->get_field_name( 'lightbox_title' ); ?>" type="text"
			   value="<?php echo $lightbox_title; ?>"/>
		<!--		</p>-->
		<label for="<?php echo $this->get_field_id( 'lightbox_description' ); ?>"><?php _e( 'Lightbox Description:', 'cd20' ); ?></label>
		<textarea class="widefat" id="<?php echo $this->get_field_id( 'lightbox_description' ); ?>"
				  name="<?php echo $this->get_field_name( 'lightbox_description' ); ?>"
				  value="<?php echo $lightbox_description; ?>" rows="4"><?php echo $lightbox_description; ?></textarea>

		<label for="<?php echo $this->get_field_id( 'lightbox_form' ); ?>"><?php _e( 'Lightbox Form ID', 'cd20' ); ?></label>
		<input type="text" class="widefat custom_media_url custom_media_button-<?php echo $files_widgets; ?>"
			   name="<?php echo $this->get_field_name( 'lightbox_form' ); ?>"
			   id="<?php echo $this->get_field_id( 'lightbox_form' ); ?>" value="<?php echo $lightbox_form; ?>"
			   style="margin-top:5px;">
		<?php
	}

	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance ) {
		$instance                         = $old_instance;
		$instance['title']                = ( ! empty( $new_instance['title'] ) ) ? strip_tags( $new_instance['title'] ) : '';
		$instance['button']               = ( ! empty( $new_instance['button'] ) ) ? strip_tags( $new_instance['button'] ) : '';
		$instance['image_id']             = ( ! empty( $new_instance['image_id'] ) ) ? strip_tags( $new_instance['image_id'] ) : '';
		$instance['lightbox_title']       = ( ! empty( $new_instance['lightbox_title'] ) ) ? strip_tags( $new_instance['lightbox_title'] ) : '';
		$instance['lightbox_description'] = ( ! empty( $new_instance['lightbox_description'] ) ) ? strip_tags( $new_instance['lightbox_description'] ) : '';
		$instance['lightbox_form']        = ( ! empty( $new_instance['lightbox_form'] ) ) ? strip_tags( $new_instance['lightbox_form'] ) : '';

		return $instance;
	}
} // Class wpb_widget ends here

