<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

?>
<div class="two-halfs__full-width    <?php echo esc_html( $add_classes ); ?>"
	 style="background:<?php echo esc_html( $bcg_desktop ); ?>">
	<div class="container  two-halfs__container">
<!--		style="color:--><?php //echo $clean['section_color'] ?><!--">-->
		<?php include 'common/section-heading.php'; ?>
		<div class="builder-row--two-halfs">
			<div class="content__left"
				 style="background:<?php echo esc_attr( $left_colors['background'] ); ?>;
						 color:<?php echo esc_attr( $left_colors['text'] ); ?>">
				<div class="one-half__container--mobile">
					<?php echo $left_half['wyswyg']; ?>
				</div>
			</div>
			<div class="content__right"
				 style="background:<?php echo esc_attr( $right_colors['background'] ); ?>;
						 color:<?php echo esc_attr( $right_colors['text'] ); ?>">
				<div class="one-half__container--mobile">
					<?php echo $right_half['wyswyg']; ?>
				</div>
			</div>
		</div>
	</div>
</div>
</div>

