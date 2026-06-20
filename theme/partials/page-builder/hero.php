<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */
$text_color = get_sub_field( 'text_color' );

if ( ! $text_color ) {
	$text_color = '#000';
}

$args['bcg_image']  = wp_kses_post( wp_get_attachment_image_url( get_sub_field( 'bcg_image' ), 'full' ) );
$args['wyswyg']     = wp_kses_post( get_sub_field( 'wyswyg' ) );
$args['text_color'] = esc_attr( $text_color );
$args['classes']    = esc_html( get_sub_field( 'additional_css_classes' ) );

get_template_part( 'views/page-builder/hero', null, $args );
