<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

?>
<div class="columns__full_width timeline__full_width<?php echo esc_html( $add_classes ); ?>"
	 style="background:<?php echo esc_attr( $colors['background'] ); ?>">
	<div class="container"
		 style="color:<?php echo esc_attr( $colors['text'] ); ?>">
		<?php
		include 'common/section-heading.php';
		if ( $items ) {
			?>
			<div class="timeline__items">
				<?php
				$i = 1;
				foreach ( $items as $item ) { ?>
					<div class="timeline__item  <?php echo( $i % 2 === 1 ? 'left' : 'right' ); ?>">

						<div class="timeline__icon">
							<?php echo wp_kses_post( wp_get_attachment_image( $icon, [ 37, 37 ],  ) ); ?>
						</div>
						<div class="timeline__content"
							 style="background:<?php echo esc_attr( $colors['box'] ); ?>">
							<?php echo wp_kses_post( wp_get_attachment_image( $item['image'] ) ); ?>
							<div class="timeline__text">
								<div class="timeline__superheading  column__superheading"><?php echo esc_html( $item['superheading'] ); ?></div>
								<div class="timeline__heading  column__heading"><?php echo esc_html( $item['heading'] ); ?></div>
								<div class="timeline__description column__descripton"><?php echo esc_html( $item['description'] ); ?></div>
							</div>

						</div>
					</div>
					<?php
					$i ++;
				} ?>
			</div>
		<?php } ?>
	</div>
</div>


