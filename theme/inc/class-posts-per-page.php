<?php
/**
 * Description
 */

namespace CD;

class Posts_Per_Page {
	use \CD\Traits\Singleton;

	public function initialize() {
		add_action( 'pre_get_posts', array( $this, 'limit_posts_per_page' ) );
	}

	public function limit_posts_per_page( $query ) {
		// Queued 4 posts from author.
		if ( ! is_admin() && $query->is_main_query() && is_author() ) {
			$query->set( 'posts_per_page', 4 );

			return;
		}

		if ( ! is_admin() && $query->is_main_query() && is_post_type_archive( 'testimonial' ) ) {
			$query->set( 'posts_per_page', 6 );

			return;
		}

		// Sectors archive page with all posts with category.
		if ( ! is_admin() && $query->is_main_query() && is_category( 'sectors' ) ) {
			$query->set( 'posts_per_page', - 1 );
			$query->set( 'orderby', 'title' );
			$query->set( 'order', 'ASC' );

			return;
		}

		// Standard archive page with 12 posts.
		if ( ! is_admin() && $query->is_main_query() && ( is_archive() || is_search() ) ) {
			$query->set( 'posts_per_page', 12 );

			return;
		}
	}
}
