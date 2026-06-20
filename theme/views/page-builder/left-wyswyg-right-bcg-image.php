<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

?>
<div class="two-halfs-with-image  two-halfs-right-image <?php echo esc_html( $add_classes ); ?>"
	 style="background:<?php echo esc_attr( $left_half['bcg_color'] ); ?>">
	<div class="container">
		<div class="content__left">
			<?php echo $left_half['wyswyg'] ?>
		</div>
	</div>
	<div class="content__right  content__right--bcg-image"
		 style="background-image:url('<?php echo wp_kses_post( $bcg_image_url ); ?>') ">
	</div>
</div>


