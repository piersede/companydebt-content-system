<?php
/**
 * Accordion Block  Template.
 *
 * @param array $block The block settings and attributes.
 * @param string $content The block inner HTML (empty).
 * @param bool $is_preview True during AJAX preview.
 * @param int $post_id The post ID this block is saved to.
 *
 * @package EP_Light
 */
?>
<div class="columns__full_width accordion__full_width <?php echo esc_html($add_classes); ?>"
	 style="background:<?php echo esc_attr($colors['background']); ?>">
	<div class="container">
		<?php include 'common/section-heading.php'; ?>
		<div class="accordion-block"
			 style="color:<?php echo esc_attr($colors['text']); ?>">
			<?php foreach ( $items as $item ) { ?>
				<div class='accordion-item  closed'
					 style="background:<?php echo esc_attr($colors['box']); ?>">
					<div class="accordion-item__title  ">
						<div class="accordion-item__title-text "><?php echo esc_textarea( $item['heading'] ); ?></div>
					</div>
					<div class="accordion-item__description closed"><?php echo wp_kses_post( $item['description'] ); ?></div>
				</div>
			<?php } ?>
		</div>
	</div>
</div>
