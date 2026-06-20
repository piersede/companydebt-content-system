<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

$headings = get_sub_field( 'headings' );
$colors = $headings['colors'];
$items = get_sub_field('items');
$icon = get_sub_field('icon');
$add_classes = get_sub_field('add_classes');

if ( ! $colors['background'] ) {
	$colors['background'] = '#ffffff';
}

if ( ! $colors['box'] ) {
	$colors['box'] = '#ffffff';
}

if ( ! $colors['text'] ) {
	$colors['text'] = '#000';
}

include( CD20_VIEWS . '/page-builder/timeline.php' );
