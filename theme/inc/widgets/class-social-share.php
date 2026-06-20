<?php

namespace CD\Widgets;

class Social_Share extends \WP_Widget
{

	function __construct()
	{
		parent::__construct(
				'cd_social_widget',
				__( 'CD Social Share Widget', 'cd20' ),
				array(
						'description' => __( 'Displays Social Share', 'cd20' ),
						'classname'   => 'widget__social',
				)
		);
	}

	// Widget front-end
	public function widget( $args, $instance )
	{
		// before and after widget arguments are defined by themes
		$title = $instance['title'];
		?>
		<section class="widget__social">
			<?php
			if ( ! empty( $title ) ) {
				echo '<div class="widget__social-title">' . $title . '</div>';
			}
			?>
			<div class="widget__social-icons">
				<a rel="nofollow noreferrer"
				   target="_blank"
				   href="https://www.facebook.com/sharer/sharer.php?u=<?php the_permalink(); ?>"
				   class="widget__social-icon-share  widget__social-icon-share--facebook"
				   data-network="facebook">
					<img src="<?php echo CD20_TEMPLATE_URL . '/dist/images/facebook-blue.png'; ?>"
						 alt="facebook icon"
						 height="18"
						 width="10">
				</a>
				<a rel="nofollow noreferrer"
				   target="_blank"
				   href="https://twitter.com/home?status=<?php the_permalink(); ?>"
				   class="widget__social-icon-share  widget__social-icon-share--twitter"
				   data-network="twitter">
					<img src="<?php echo CD20_TEMPLATE_URL . '/dist/images/twitter-blue.png'; ?>"
						 alt="twitter icon"
						 height="14"
						 width="18">
				</a>
				<a rel="nofollow noreferrer"
				   target="_blank"
				   href="https://www.linkedin.com/shareArticle?mini=true&url=<?php the_permalink(); ?>"
				   class="widget__social-icon-share  widget__social-icon-share--linkedin"
				   data-network="linkedin">
					<img src="<?php echo CD20_TEMPLATE_URL . '/dist/images/linkedin-blue.png'; ?>"
						 alt="linkedin icon"
						 height="18"
						 width="18">

				</a>
				<a rel="nofollow noreferrer"
				   href="mailto:?Subject=CompanyDebt&nbsp;Article&amp;Body=<?php the_permalink(); ?>"
				   title="Shared by Email"
				   class="widget__social-icon-share  widget__social-icon-share--email">
					<img src="<?php echo CD20_TEMPLATE_URL . '/dist/images/email-blue.png'; ?>"
						 alt="email icon"
						 height="14"
						 width="20">

				</a>
			</div>
		</section>
		<?php
	}

	// Widget Backend
	public function form( $instance )
	{
		global $files_widgets;
		$files_widgets++;

		// Widget admin form
		if ( isset( $instance['title'] ) ) {
			$title = $instance['title'];
		}
		?>
		<p>
			<label for="<?php echo $this->get_field_id( 'title' ); ?>"><?php _e( 'Title:', 'cd20' ); ?></label>
			<input class="widefat" id="<?php echo $this->get_field_id( 'title' ); ?>"
				   name="<?php echo $this->get_field_name( 'title' ); ?>" type="text"
				   value="<?php echo $title; ?>"/>
		</p>
	<?php }

	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance )
	{
		$instance          = $old_instance;
		$instance['title'] = ( ! empty( $new_instance['title'] ) ) ? ( $new_instance['title'] ) : '';

		return $instance;
	}

}

