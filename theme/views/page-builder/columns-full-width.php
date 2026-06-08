<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

?>
<div class="columns__full_width <?php echo esc_html( $add_classes ); ?>"
	 style="background:<?php echo esc_attr( $colors['background'] ); ?>">
	<div class="container"
		 style="color:<?php echo esc_attr( $colors['text'] ); ?>">
		<?php
		include 'common/section-heading.php';
		if ( $items ) {
			?>
			<div class="columns__container">
				<?php foreach ( $items as $item ) { ?>
					<div class="column__container"
						 style="background:<?php echo esc_attr( $colors['box'] ); ?>">
						<?php if ( $item['image'] || $item['heading '] || $item['description'] ) { ?>
							<div class="column__top">
								<?php echo wp_kses_post( wp_get_attachment_image( $item['image'], '', '', array( 'class' => 'column__image' ) ) ); ?>
								<div class="column__heading"><?php echo wp_kses_post( $item['heading'] ); ?></div>
								<div class="column__descripton"><?php echo wp_kses_post( $item['description'] ); ?></div>
							</div>
						<?php }
						if ( $item['icon'] || $item['name'] || $item['position'] ) { ?>
							<div class="column__bottom">
								<?php echo wp_kses_post( wp_get_attachment_image( $item['icon'], '', '', array( 'class' => 'column__icon' ) ) ); ?>
								<div class="column__person">
									<div class="column__name"><?php echo esc_html( $item['name'] ); ?></div>
									<div class="column__position"><?php echo esc_html( $item['position'] ); ?></div>
								</div>
							</div>
						<?php } ?>
					</div>
				<?php } ?>
			</div>
		<?php } ?>
	</div>
</div>


