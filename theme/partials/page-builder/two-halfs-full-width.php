<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

$headings    = get_sub_field( 'headings' );
$colors      = $headings['colors'];

$left_half   = get_sub_field( 'left_half' );
$right_half  = get_sub_field( 'right_half' );

$left_colors = $left_half['colors'];
$right_colors = $right_half['colors'];

$add_classes = get_sub_field( 'add_classes' );


if ( ! $left_colors['background'] ) {
	$left_colors['background'] = '#fff';
}

if ( ! $right_colors['background'] ) {
	$right_colors['background'] = '#fff';
}

if ( ! $left_colors['text'] ) {
	$left_colors['text'] = '#000';
}

if ( ! $right_colors['text'] ) {
	$right_colors['text'] = '#000';
}

$format      = 'linear-gradient(%s, %s 50%%, %s 50%%)';
$bcg_desktop = sprintf( $format, 'to right', $left_colors['background'], $right_colors['background'] );


include( CD20_VIEWS . '/page-builder/two-halfs-full-width.php' );
