<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */


$bcg_image  = get_sub_field( 'bcg_image' );
$text_color = get_sub_field( 'text_color' );
$wyswyg = get_sub_field( 'wyswyg' );
$additional_css_classes = get_sub_field('additional_css_classes');

if ( ! $text_color ) {
	$text_color = '#000';
}

$clean['bcg_image']    = wp_kses_post( wp_get_attachment_image_url( $bcg_image, 'full' ) );
$clean['text_color'] = esc_attr( $text_color );
$clean['classes'] = esc_html( $additional_css_classes );

include( CD20_VIEWS . '/page-builder/bcg-image-full-width.php' );
