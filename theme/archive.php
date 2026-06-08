<?php
/**
 * Template for category / tag / date / author archives.
 *
 * Hero structure mirrors templates/take-the-test-template.php so the same
 * .col-12.page-header band (with the soft #f8f9fd full-width strip behind
 * breadcrumbs + h1.post-title) renders here too. The body.archive CSS
 * extension in style.css picks up these elements — there is no per-archive
 * branching here; archive.php serves every populated category, tag, etc.
 *
 * Hero content is intentionally minimal: breadcrumbs + h1 only. No author
 * block, no reading time — archives are an index, not an article.
 *
 * @package CompanyDebt
 */

$queried_object = get_queried_object();

get_header();
?>

<main id="primary" class="site-archive">
	<div class="content">
		<?php get_template_part( 'template-parts/header-image' ); ?>

		<div class="container">
			<div class="row">
				<div class="col-12 page-header">
					<?php
					if ( function_exists( 'yoast_breadcrumb' ) ) {
						yoast_breadcrumb( '<div class="breadcrumbs">', '</div>' );
					}
					?>
					<h1 class="post-title"><?php echo esc_html( is_post_type_archive() ? post_type_archive_title( '', false ) : single_term_title( '', false ) ); ?></h1>
				</div>

				<?php if ( have_posts() ) : ?>
					<div class="col-12">
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
										<div class="read-more-btn">Read More<svg class="cd-read-more-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></div>
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
						echo $pagination;
						?>
					</div>
				<?php else : ?>
					<div class="col-12">
						<?php get_template_part( 'template-parts/content', 'none' ); ?>
					</div>
				<?php endif; ?>
			</div>
		</div>
	</div>
</main>

<?php
/* "Get in Touch Today" CTA block — same partial used by the take-the-test
 * template. Adds the contact form section at the bottom of every archive
 * page. (20260603) */
get_template_part( '/template-parts/footer/footer-cta-block' );
get_footer();
