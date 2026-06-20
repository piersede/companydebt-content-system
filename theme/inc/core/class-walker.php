<?php

namespace CD\Core;
class Walker extends \Walker_Nav_Menu {
	/**
	 * Switch a to span.
	 * @param string   $output
	 * @param \WP_Post $item
	 * @param int      $depth
	 * @param array    $args
	 * @param int      $id
	 */
	function start_el( &$output, $item, $depth = 0, $args = array(), $id = 0 ) {
		global $wp_query;
		$indent = ( $depth ) ? str_repeat( "\t", $depth ) : '';

		$class_names = '';

		$classes   = empty( $item->classes ) ? array() : (array) $item->classes;
		$classes[] = 'menu-item-' . $item->ID;

		$class_names = join( ' ', apply_filters( 'nav_menu_css_class', array_filter( $classes ), $item, $args ) );
		$class_names = $class_names ? ' class="' . esc_attr( $class_names ) . '"' : '';

		$id = apply_filters( 'nav_menu_item_id', 'menu-item-' . $item->ID, $item, $args );
		$id = $id ? ' id="' . esc_attr( $id ) . '"' : '';

		$has_children = 0;
		if ( false !== strpos( $class_names, 'menu-item-has-children') ) {
			$has_children = 1;
		}
		$output .= $indent . '<li' . $id . $class_names . '>';

		$attributes  = ! empty( $item->attr_title ) ? ' title="' . esc_attr( $item->attr_title ) . '"' : '';
		$attributes .= ! empty( $item->target ) ? ' target="' . esc_attr( $item->target ) . '"' : '';
		$attributes .= ! empty( $item->xfn ) ? ' rel="' . esc_attr( $item->xfn ) . '"' : '';
		$el_link     = ! empty( $item->url ) && $item->url !== '#' ? ' href="' . esc_attr( $item->url ) . '"' : '';

		$item_output  = $args->before;
		if ( $el_link ) {
			$attributes  .= $el_link;
			$item_output .= '<a' . $attributes . '>';
		} else {
			$item_output .= '<span' . $attributes . '>';
		}

		$item_output .= $args->link_before . apply_filters( 'the_title', $item->title, $item->ID ) . $args->link_after;

		if ( 'primary' == $args->theme_location ) {
			$submenus     = 0 == $depth || 1 == $depth ? get_posts(
				array(
					'post_type'   => 'nav_menu_item',
					'numberposts' => 1,
					'meta_query'  => array(
						array(
							'key'    => '_menu_item_menu_item_parent',
							'value'  => $item->ID,
							'fields' => 'ids',
						),
					),
				)
			) : false;
		}
		if ( $el_link ) {
			$item_output .= '</a>';
		} else {
			$item_output .= '</span>';
		}

		if ( $has_children ) {
			$item_output .= '<span class="menu-arrow"></span>';
		}

		$item_output .= $args->after;

		$output .= apply_filters( 'walker_nav_menu_start_el', $item_output, $item, $depth, $args );
	}
}
