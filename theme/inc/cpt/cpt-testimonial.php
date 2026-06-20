<?php
/**
 * Testimonial Custom Post Type Functionality
 *
 * @package     CompanyDebt\CustomPostTypes\Custom
 * @since       1.0.0
 * @link
 * @license     GNU General Public License 2.0+
 */


add_action( 'init', 'cd_register_custom_post_type' );
add_action( 'init', 'cd_register_custom_taxonomy' );
/**
 * Register the custom post type.
 *
 * @since 1.0.0
 *
 * @return void
 */
function cd_register_custom_post_type() {

	$labels = array(
		'name'               => _x( 'Testimonials', 'post type general name', 'cdcustomposttypes' ),
		'singular_name'      => _x( 'Testimonial', 'post type singular name', 'cdcustomposttypes' ),
		'menu_name'          => _x( 'Testimonials', 'admin menu', 'cdcustomposttypes' ),
		'name_admin_bar'     => _x( 'Testimonial', 'add new on admin bar', 'cdcustomposttypes' ),
		'add_new'            => _x( 'Add New Testimonial', 'team-bios', 'cdcustomposttypes' ),
		'add_new_item'       => __( 'Add New Testimonial', 'cdcustomposttypes' ),
		'new_item'           => __( 'New Testimonial', 'cdcustomposttypes' ),
		'edit_item'          => __( 'Edit Testimonial', 'cdcustomposttypes' ),
		'view_item'          => __( 'View Testimonial', 'cdcustomposttypes' ),
		'all_items'          => __( 'All Testimonial', 'cdcustomposttypes' ),
		'search_items'       => __( 'Search Testimonials', 'cdcustomposttypes' ),
		// 'parent_item_colon'  => __( 'Parent Team Bios:', 'cdcustomposttypes' ),
		'not_found'          => __( 'No testimonials found.', 'cdcustomposttypes' ),
		'not_found_in_trash' => __( 'No testimonials found in Trash.', 'cdcustomposttypes' ),
	);

	$features = get_all_post_type_features( 'post', array(
		'excerpt',
		'comments',
		'trackbacks',
		'custom-fields',
		'thumbnail'
	) );

	$args = array(
		'label'        => __( 'Testimonials', 'cdcustomposttypes' ),
		'labels'       => $labels,
		'public'       => true,
		'supports'     => $features,
		'menu_icon'    => 'dashicons-admin-users',
		'hierarchical' => false,
		'has_archive'  => true,
		'rewrite'      => array(
			'slug' => 'testimonials',
		)
	);

	register_post_type( 'testimonial', $args );
}

function cd_register_custom_taxonomy() {

	$labels = array(
		'name'              => _x( 'Testimonials category', 'taxonomy general name', 'cdcustomposttypes' ),
		'singular_name'     => _x( 'Testimonial category', 'taxonomy singular name', 'cdcustomposttypes' ),
		'search_items'      => __( 'Search Testimonials category', 'cdcustomposttypes' ),
		'all_items'         => __( 'All Testimonials category', 'cdcustomposttypes' ),
		'parent_item'       => __( 'Parent Testimonial category', 'cdcustomposttypes' ),
		'parent_item_colon' => __( 'Parent Testimonial: category', 'cdcustomposttypes' ),
		'edit_item'         => __( 'Edit Testimonial category', 'cdcustomposttypes' ),
		'update_item'       => __( 'Update Testimonial category', 'cdcustomposttypes' ),
		'add_new_item'      => __( 'Add New Testimonial category', 'cdcustomposttypes' ),
		'new_item_name'     => __( 'New Testimonial category Name', 'cdcustomposttypes' ),
		'menu_name'         => __( 'Testimonial category', 'cdcustomposttypes' ),
	);

	$args = array(
		'hierarchical'      => true,
		'labels'            => $labels,
		'show_ui'           => true,
		'show_admin_column' => true,
		'query_var'         => true,
		'rewrite'           => array( 'slug' => 'cat-testimonials' ),
	);

	register_taxonomy( 'testimonial_cat', array( 'testimonial' ), $args );

}

/**
 * Get all the post type features for the given post type.
 *
 * @since 1.0.0
 *
 * @param string $post_type Given post type
 * @param array $exclude_features Array of features to exclude
 *
 * @return array
 */
function get_all_post_type_features( $post_type = 'post', $exclude_features = array() ) {
	$configured_features = get_all_post_type_supports( $post_type );

	if ( ! $exclude_features ) {
		return array_keys( $configured_features );
	}

	$features = array();

	foreach ( $configured_features as $feature => $value ) {
		if ( in_array( $feature, $exclude_features ) ) {
			continue;
		}

		$features[] = $feature;
	}

	return $features;
}