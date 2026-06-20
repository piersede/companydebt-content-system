<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

$left_half  = get_sub_field( 'left_half' );
$right_half = get_sub_field( 'right_half' );
$add_classes = get_sub_field('add_classes');


if ( ! $right_half['bcg_color'] ) {
	$right_half['bcg_color'] = '#ffffff';
}

$bcg_image_url    = wp_get_attachment_image_url( $left_half['bcg_image'], 'full' ) ;

include( CD20_VIEWS . '/page-builder/left-bcg-image-right-wyswyg.php' );
