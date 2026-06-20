<?php

namespace CD\Widgets;

class Gravity_Form_With_Title_And_Bulletins extends \WP_Widget {

	function __construct() {
		parent::__construct(
			'cd_gftb_widget',
			__( 'CD Gravity Form with Title and Bulletins Widget', 'cd20' ),
			array(
				'description' => __( 'Displays Form with title and bulletins for Design 22-v1', 'cd20' ),
				'classname'   => 'widget__gftb  widget__gf',
			)
		);
	}

	// Creating widget front-end
	public function widget( $args, $instance ) {
		// Defining Variables
		$title     = $instance['title'];
		$bulletins = $instance['bulettins'];
		$form_id   = $instance['form_id'];
		// before and after widget arguments are defined by themes
		echo $args['before_widget'];
		?>

		<h2 class="widget__gftb-title"><?php echo $title; ?></h2>
		<div class="widget__gftb-inner">
			<div class="widget__gftb-bulletins"><?php echo $bulletins; ?></div>
			<div class="widget__gftb-form"><?php gravity_form( 41, false, false, false, null, true ); ?></div>
		</div>

		<?php
		echo $args['after_widget'];
	}

	// Widget Backend
	public function form( $instance ) {
		if ( isset( $instance['title'] ) ) {
			$title = $instance['title'];
		}
		if ( ! empty( $instance['bulettins'] ) ) {
			$bulletins = $instance['bulettins'];
		} else {
			$bulletins = 'Bulletins Here...';
		}

		if ( ! empty ( $instance['form_id'] ) ) {
			$form_id = $instance['form_id'];
		} else {
			$form_id = 'Your Form ID Here...';
		}
		global $files_widgets;
		$files_widgets ++;

		// Widget admin form
		?>
		<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e( 'Title:', 'cd20' ); ?></label>
		<input class="widefat" id="<?php echo $this->get_field_id( 'title' ); ?>"
			   name="<?php echo $this->get_field_name( 'title' ); ?>" type="text"
			   value="<?php echo esc_attr( $title ); ?>"/>
		<label for="<?php echo $this->get_field_id( 'bulettins' ); ?>"><?php _e( 'Bulettins', 'cd20' ); ?></label>
		<textarea class="widefat" id="<?php echo $this->get_field_id( 'bulettins' ); ?>"
				  name="<?php echo $this->get_field_name( 'bulettins' ); ?>"
				  value="<?php echo $bulletins; ?>" rows="4"><?php echo $bulletins; ?></textarea>
		<label for="<?php echo $this->get_field_id( 'form_id' ); ?>"><?php _e( 'Form ID', 'cd20' ); ?></label>
		<input class="widefat" id="<?php echo $this->get_field_id( 'form_id' ); ?>"
			   name="<?php echo $this->get_field_name( 'form_id' ); ?>" type="text"
			   value="<?php echo esc_attr( $form_id ); ?>"/>
		<?php
	}

	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance ) {
		$instance              = $old_instance;
		$instance['title']     = ( ! empty( $new_instance['title'] ) ) ? ( $new_instance['title'] ) : '';
		$instance['bulettins'] = ( ! empty( $new_instance['bulettins'] ) ) ? $new_instance['bulettins'] : '';
		$instance['form_id']   = ( ! empty( $new_instance['form_id'] ) ) ? strip_tags( $new_instance['form_id'] ) : '';

		return $instance;
	}
} // Class wpb_widget ends here

