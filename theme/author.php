<?php
/**
 * The Author template file (redesigned 20260605).
 *
 * Layout:
 *   1. Hero — breadcrumbs + photo (left) and name (H1) + position (H2) (right)
 *   2. Contact info — phone / office address / working hours rows with icons,
 *      followed by a "Contact Us" CTA button linking to /contact-us/
 *   3. Biography — long-form prose from ACF director_description
 *   4. Latest Articles — up to 4 recent posts as cards with featured image
 *   5. Footer CTA — the standard footer-cta-block partial used sitewide
 *
 * @package CompanyDebt
 */

$author          = get_queried_object();
$author_id       = $author->data->ID;
$author_name       = get_the_author_meta( 'display_name', $author_id );
$author_first_name = get_the_author_meta( 'first_name', $author_id );
$author_position   = get_field( 'professional_position', $author );
$author_photo_id   = get_field( 'photo', $author );
$author_bio        = get_field( 'director_description', $author );
$author_email      = get_the_author_meta( 'user_email', $author_id );
/* CTA label uses first name when present, else display name. */
$author_cta_name   = $author_first_name ? $author_first_name : $author_name;

$author_posts = new WP_Query( array(
	'author'         => $author_id,
	'post_type'      => 'post',
	'posts_per_page' => 4,
) );

get_header();
?>

<main id="primary" class="site-main cd-author-page">
	<div class="content">

		<?php /* --- 1. HERO --- */ ?>
		<div class="container">
			<div class="row">
				<div class="col-12 page-header">
					<?php
					if ( function_exists( 'yoast_breadcrumb' ) ) {
						yoast_breadcrumb( '<div class="breadcrumbs">', '</div>' );
					}
					?>
					<div class="cd-author-hero">
						<?php if ( $author_photo_id ) { ?>
							<div class="cd-author-hero__photo">
								<?php
								echo wp_get_attachment_image(
									$author_photo_id,
									'medium',
									false,
									array(
										'class' => 'cd-author-hero__photo-img',
										'alt'   => esc_attr( $author_name ),
									)
								);
								?>
							</div>
						<?php } ?>
						<div class="cd-author-hero__meta">
							<h1 class="cd-author-hero__name"><?php echo esc_html( $author_name ); ?></h1>
							<?php if ( $author_position ) { ?>
								<h2 class="cd-author-hero__position"><?php echo esc_html( $author_position ); ?></h2>
							<?php } ?>

							<?php /* --- Contact info, nested inside the hero meta.
							 * Lines: phone, then email. The "Contact <name>" CTA was
							 * removed per design 20260605 — the contact-form section
							 * at the bottom of the page already covers the CTA goal. --- */ ?>
							<div class="cd-author-contact">
								<ul class="cd-author-contact__list">
									<?php
									$phone = get_field( 'header_phone_number', 'option' );
									if ( $phone ) {
										$phone_tel = preg_replace( '/\s+/', '', $phone );
										?>
										<li class="cd-author-contact__item">
											<span class="cd-author-contact__icon" aria-hidden="true">
												<?php /* Filled phone glyph — copied verbatim from the topnav's
												 * .header-phone__icon span so the icon style matches the
												 * site CTA. fill: currentColor inherits the navy text colour. */ ?>
												<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.487 17.14l-4.065-3.696a1 1 0 0 0-1.391.043l-2.393 2.461c-.576-.11-1.734-.471-2.926-1.66-1.192-1.193-1.553-2.354-1.66-2.926l2.459-2.394a1 1 0 0 0 .043-1.391L6.86 3.512a1 1 0 0 0-1.391-.087l-2.17 1.861a1 1 0 0 0-.291.649c-.015.25-.301 6.172 4.291 10.766C11.305 20.707 16.323 21 17.705 21c.202 0 .326-.006.359-.008a.99.99 0 0 0 .648-.291l1.86-2.171a1 1 0 0 0-.085-1.39z"/></svg>
											</span>
											<a class="cd-author-contact__text" href="tel:<?php echo esc_attr( $phone_tel ); ?>"><?php echo esc_html( $phone ); ?></a>
										</li>
									<?php } ?>

									<?php if ( $author_email && is_email( $author_email ) ) { ?>
										<li class="cd-author-contact__item">
											<span class="cd-author-contact__icon" aria-hidden="true">
												<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
											</span>
											<a class="cd-author-contact__text" href="mailto:<?php echo esc_attr( $author_email ); ?>"><?php echo esc_html( $author_email ); ?></a>
										</li>
									<?php } ?>
								</ul>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<?php /* --- 3. BIOGRAPHY --- */ ?>
		<?php if ( $author_bio ) { ?>
			<div class="container">
				<div class="cd-author-bio">
					<?php echo wp_kses_post( $author_bio ); ?>
				</div>
			</div>
		<?php } ?>

		<?php /* --- 4. LATEST ARTICLES --- */ ?>
		<?php if ( $author_posts->have_posts() ) { ?>
			<div class="container">
				<div class="cd-author-articles">
					<h2 class="cd-author-articles__title">Latest Articles</h2>
					<div class="cd-author-articles__grid">
						<?php
						while ( $author_posts->have_posts() ) {
							$author_posts->the_post();
							$thumb_url = get_the_post_thumbnail_url( get_the_ID(), 'medium_large' );
							?>
							<a href="<?php the_permalink(); ?>" class="cd-author-article-card">
								<?php if ( $thumb_url ) { ?>
									<div class="cd-author-article-card__image" style="background-image: url('<?php echo esc_url( $thumb_url ); ?>');"></div>
								<?php } else { ?>
									<div class="cd-author-article-card__image cd-author-article-card__image--placeholder" aria-hidden="true"></div>
								<?php } ?>
								<h3 class="cd-author-article-card__title"><?php the_title(); ?></h3>
							</a>
							<?php
						}
						wp_reset_postdata();
						?>
					</div>
				</div>
			</div>
		<?php } ?>

	</div>
</main>

<?php
/* Footer CTA — keep the standard contact form section. The legacy "Get in
 * touch" social icons block has been removed (replaced by this section). */
get_template_part( '/template-parts/footer/footer-cta-block' );
get_footer();
