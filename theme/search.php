<?php
/**
 * The template for displaying search results pages.
 *
 * @package Cd20
 */

get_header(); ?>
	<section itemscope itemtype="https://schema.org/SearchResultsPage" class="search-page">
		<div class="container">
			<h1 class="page-title">
				<?php
				/* translators: the search query */
				printf( esc_html__( 'Results for "%s"', 'cd20' ), '<span>' . esc_html( get_search_query() ) . '</span>' );
				?>
			</h1>
		</div>
		<?php if ( have_posts() ) { ?>
			<div class="container">
				<div class="articles-list">
					<?php
					while ( have_posts() ) :
						the_post();
						$thumbnail = get_the_post_thumbnail_url( get_the_ID(), 'blog_thumbnail' );

						if ( ! $thumbnail ) {
							$fallback_thumnail = get_field( 'fallback_blog_image', 'option' );
							$thumbnail         = wp_get_attachment_image_url( $fallback_thumnail['id'], 'blog_thumbnail' );
						}
						?>
							<article>
								<a href="<?php the_permalink(); ?>">
								<img class="post-preview__thumbnail"
									src="<?php echo esc_url( $thumbnail ); ?>"
									alt="<?php echo esc_attr( get_the_title() ); ?>"
									height="219"
									width="373"
									style="min-height: 219px;">
									<h3><?php the_title(); ?></h3>
									<div class="post-excerpt"><?php echo wp_kses_post( get_the_excerpt() ); ?></div>
									<div class="read-more-btn">Read More</div>
								</a>
							</article>	
						<?php
					endwhile; 
					?>
				</div>
				<?php
					$pagination = get_the_posts_pagination(
						array(
							'mid_size' => 5,
						)
					);
					
					echo ( $pagination );
				?>
			</div>
		<?php } else { ?>
			<div class="container">
				<p><?php esc_html_e( 'No Results Found...', "cd20" ); ?></p>
			</div>
		<?php } ?>
	</section>
	</div>
<?php
get_footer();
