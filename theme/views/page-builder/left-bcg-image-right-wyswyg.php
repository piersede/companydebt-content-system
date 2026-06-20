<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

?>
<div class="two-halfs-with-image  two-halfs-left-image  <?php echo esc_html( $add_classes ); ?>"
	 style="background:<?php echo esc_attr( $right_half['bcg_color'] ); ?>">
	<div class="content__left  content__left--bcg-image"
		 style="background-image:url('<?php echo wp_kses_post( $bcg_image_url ); ?>') ">
	</div>
	<div class="container">
		<div class="content__right">
			<?php echo $right_half['wyswyg'] ?>
		</div>
	</div>
</div>


