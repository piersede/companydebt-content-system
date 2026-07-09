<?php
/**
 * Plugin Name: CD SEO Meta REST
 * Description: Exposes the Yoast SEO title and meta-description post meta to the
 *   REST API so SEO fields can be set programmatically by the staging tooling.
 *   The values are stored in normal postmeta and persist even if this plugin is
 *   removed; this only permits the write. Edit capability is required.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_action( 'init', function () {
    $keys  = array( '_yoast_wpseo_title', '_yoast_wpseo_metadesc' );
    $types = array( 'page', 'post' );
    foreach ( $types as $type ) {
        foreach ( $keys as $key ) {
            register_post_meta( $type, $key, array(
                'type'          => 'string',
                'single'        => true,
                'show_in_rest'  => true,
                'auth_callback' => function () {
                    return current_user_can( 'edit_posts' );
                },
            ) );
        }
    }
} );
