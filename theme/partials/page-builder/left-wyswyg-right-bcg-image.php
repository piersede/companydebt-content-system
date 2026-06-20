<?php

$left_half  = get_sub_field( 'left_half' );
$right_half = get_sub_field( 'right_half' );
$add_classes = get_sub_field('add_classes');

if ( ! $left_half['bcg_color'] ) {
	$left_half['bcg_color'] = '#ffffff';
}

$bcg_image_url    = wp_get_attachment_image_url( $right_half['bcg_image'], 'full' ) ;

include( CD20_VIEWS . '/page-builder/left-wyswyg-right-bcg-image.php' );
