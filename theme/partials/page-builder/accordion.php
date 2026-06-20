<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */

$icon = get_sub_field( 'icon' );
$bcg_color = get_sub_field( 'bcg_color' );
$items = get_sub_field( 'items' );
$add_classes = get_sub_field('add_classes');


if ( ! $bcg_color ) {
	$colors['background'] = '#F2F6FD';
}

include( CD20_VIEWS . '/page-builder/accordion.php' );
