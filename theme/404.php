<?php
/**
 * The template for displaying 404 pages (not found).
 *
 * Clean centred layout — H1 "404", H2 status line, two body lines.
 * The "Homepage" word in the last line is the only link on the page.
 *
 * @package CompanyDebt
 */

get_header();
?>

<main id="primary" class="site-main">
	<section class="error-404 not-found">
		<div class="cd-404">
			<h1 class="cd-404__heading">404</h1>
			<h2 class="cd-404__subhead">Oops, an error has occured!</h2>
			<p class="cd-404__body">The page you are trying to reach cannot be found.</p>
			<a class="cd-404__cta" href="<?php echo esc_url( home_url( '/' ) ); ?>">Back to Homepage</a>

			<?php /* Contact details — phone, postal address, email — centred
			 * under the CTA. All three pull from sitewide ACF options so
			 * they stay in sync with the topnav / footer / author template. */ ?>
			<ul class="cd-404__contact">
				<?php
				$phone_404 = get_field( 'header_phone_number', 'option' );
				if ( $phone_404 ) {
					$phone_404_tel = preg_replace( '/\s+/', '', $phone_404 );
					?>
					<li class="cd-404__contact-item">
						<span class="cd-404__contact-icon" aria-hidden="true">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.487 17.14l-4.065-3.696a1 1 0 0 0-1.391.043l-2.393 2.461c-.576-.11-1.734-.471-2.926-1.66-1.192-1.193-1.553-2.354-1.66-2.926l2.459-2.394a1 1 0 0 0 .043-1.391L6.86 3.512a1 1 0 0 0-1.391-.087l-2.17 1.861a1 1 0 0 0-.291.649c-.015.25-.301 6.172 4.291 10.766C11.305 20.707 16.323 21 17.705 21c.202 0 .326-.006.359-.008a.99.99 0 0 0 .648-.291l1.86-2.171a1 1 0 0 0-.085-1.39z"/></svg>
						</span>
						<a class="cd-404__contact-link" href="tel:<?php echo esc_attr( $phone_404_tel ); ?>"><?php echo esc_html( $phone_404 ); ?></a>
					</li>
				<?php } ?>

				<?php
				$office_404 = get_field( 'office_address', 'option' );
				if ( $office_404 ) {
					/* Strip <br> tags + collapse whitespace so the address renders
					 * as one clean line, matching the inline contact treatment
					 * used on the author template. */
					$office_404_inline = preg_replace( '#<br\s*/?>#i', ' ', $office_404 );
					$office_404_inline = preg_replace( '/\s+/', ' ', $office_404_inline );
					$office_404_inline = trim( $office_404_inline );
					?>
					<li class="cd-404__contact-item">
						<span class="cd-404__contact-icon" aria-hidden="true">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
						</span>
						<span class="cd-404__contact-link"><?php echo esc_html( $office_404_inline ); ?></span>
					</li>
				<?php } ?>

				<li class="cd-404__contact-item">
					<span class="cd-404__contact-icon" aria-hidden="true">
						<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
					</span>
					<a class="cd-404__contact-link" href="mailto:info@companydebt.com">info@companydebt.com</a>
				</li>
			</ul>
		</div>
	</section>
</main>

<?php
get_footer();
