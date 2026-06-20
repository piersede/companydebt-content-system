<?php

namespace CD\Widgets;

class CTA_Title_Description_Phone extends \WP_Widget
{
	function __construct()
	{
		parent::__construct(
				'cd_cta_text', // Base ID of  widget
				__( 'CD CTA Text Widget', 'cd20' ), // Widget name will appear in UI
				array(
						'description' => __( 'Displays Title, Description and Call Button ', 'cd20' ),
						'classname'   => 'widget__cta_text_button'
				)
		);
	}

	// Creating widget front-end
	public function widget( $args, $instance )
	{
		// Defining Variables

		$title       = $instance['title'];
		$description = $instance['description'];
		$cta_icon    = $instance['cta_icon'];
		$cta_text    = $instance['cta_text'];
		$cta_link    = $instance['cta_link'];

		// before and after widget arguments are defined by themes
		echo $args['before_widget'];
		?>
		<div class="widget__cta">
			<?php if ( ! empty( $title ) ) { ?>
				<div class="widget__cta__title"><?php echo $title; ?></div>
			<?php } ?>
			<?php if ( ! empty( $description ) ) { ?>
				<div class="widget__cta__description"><?php echo $description; ?></div>
			<?php } ?>
			<a href="<?php echo $cta_link; ?>">
				<div class="widget__cta__button">
					<?php
					echo wp_get_attachment_image( $cta_icon, array( 22, 22 ), false, array( 'class' => 'widget__cta__icon' ) );
					if ( ! empty( $cta_text ) ) {
						?>
						<div class="widget__cta__text"><?php echo $cta_text; ?></div>
					<?php } ?>
				</div>
			</a>
		</div>
		<?php echo $args['after_widget'];
	}

	// Widget Backend
	public function form( $instance )
	{
		if ( isset( $instance['title'] ) ) {
			$title = $instance['title'];
		}

		if ( isset( $instance['description'] ) ) {
			$description = $instance['description'];
		}


		if ( ! empty ( $instance['cta_icon'] ) ) {
			$cta_icon = $instance['cta_icon'];
		}

		if ( ! empty ( $instance['cta_text'] ) ) {
			$cta_text = $instance['cta_text'];
		}

		if ( ! empty ( $instance['cta_link'] ) ) {
			$cta_link = $instance['cta_link'];
		}


		global $files_widgets;
		$files_widgets++;

		// Widget admin form
		?>
		<p>
			<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e( 'Title:', 'cd20' ); ?></label>
			<input class="widefat" id="<?php echo $this->get_field_id( 'title' ); ?>"
				   name="<?php echo $this->get_field_name( 'title' ); ?>" type="text"
				   value="<?php echo $title; ?>"/>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'description' ); ?>"><?php _e( 'Description', 'cd20' ); ?></label>
			<input class="widefat" id="<?php echo $this->get_field_id( 'description' ); ?>"
				   name="<?php echo $this->get_field_name( 'description' ); ?>" type="text"
				   value="<?php echo esc_attr( $description ); ?>"/>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'cta_icon' ); ?>"><?php _e( 'CTA Icon ID', 'cd20' ); ?></label>
			<input type="text" class="widefat custom_media_url custom_media_button-<?php echo $files_widgets; ?>"
				   name="<?php echo $this->get_field_name( 'cta_icon' ); ?>"
				   id="<?php echo $this->get_field_id( 'cta_icon' ); ?>" value="<?php echo $cta_icon; ?>"
				   style="margin-top:5px;">
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'cta_text' ); ?>"><?php _e( 'CTA Text', 'cd20' ); ?></label>
			<input type="text" class="widefat custom_media_url custom_media_button-<?php echo $files_widgets; ?>"
				   name="<?php echo $this->get_field_name( 'cta_text' ); ?>"
				   id="<?php echo $this->get_field_id( 'cta_text' ); ?>" value="<?php echo $cta_text; ?>"
				   style="margin-top:5px;">
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'cta_link' ); ?>"><?php _e( 'CTA Link', 'cd20' ); ?></label>
			<input type="text" class="widefat custom_media_url custom_media_button-<?php echo $files_widgets; ?>"
				   name="<?php echo $this->get_field_name( 'cta_link' ); ?>"
				   id="<?php echo $this->get_field_id( 'cta_link' ); ?>" value="<?php echo $cta_link; ?>"
				   style="margin-top:5px;">
		</p>
		<?php
	}

	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance )
	{
		$instance                = $old_instance;
		$instance['title']       = ( ! empty( $new_instance['title'] ) ) ? ( $new_instance['title'] ) : '';
		$instance['description'] = ( ! empty( $new_instance['description'] ) ) ? strip_tags( $new_instance['description'] ) : '';
		$instance['cta_icon']    = ( ! empty( $new_instance['cta_icon'] ) ) ? strip_tags( $new_instance['cta_icon'] ) : '';
		$instance['cta_text']    = ( ! empty( $new_instance['cta_text'] ) ) ? $new_instance['cta_text'] : '';
		$instance['cta_link']    = ( ! empty( $new_instance['cta_link'] ) ) ? $new_instance['cta_link'] : '';

		return $instance;
	}
}
