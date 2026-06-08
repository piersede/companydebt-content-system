<?php
/**
 * Template Name: Meet the Team
 */

/* Hardcoded display order — user IDs in the sequence the team should appear.
 * Mike (23) → Tony (10) → Ed (22) → Chris (34) → Piers (16) → Théo (29).
 * To reorder, just rearrange this array. To add a new member, append their
 * user ID. Unknown / missing users are silently skipped. */
$cd_team_order = array( 23, 10, 22, 34, 16, 29 );

$members = array();
foreach ( $cd_team_order as $usr_id ) {
    $display = get_the_author_meta( 'display_name', $usr_id );
    if ( ! $display ) continue;
    /* LinkedIn URL from ACF `linkedin_url` on the user profile; fall back to
     * the Company Debt company page when no per-user URL is set. */
    $linkedin = get_field( 'linkedin_url', 'user_' . $usr_id );
    if ( ! $linkedin ) {
        $linkedin = 'https://www.linkedin.com/company/companydebt/';
    }
    /* Email: use the WP user-profile email if present, else fall back to the
     * generic Company Debt inbox. */
    $email = get_the_author_meta( 'user_email', $usr_id );
    if ( ! $email ) {
        $email = 'info@companydebt.com';
    }
    $members[] = array(
        'id'       => $usr_id,
        'name'     => $display,
        'position' => get_field( 'professional_position', 'user_' . $usr_id ),
        'url'      => get_author_posts_url( $usr_id ),
        'photo'    => get_field( 'photo', 'user_' . $usr_id ),
        'linkedin' => $linkedin,
        'email'    => $email,
    );
}

get_header();
?>
 <div class="section-meet-the-team">
<?php get_template_part( 'template-parts/header-image' ); ?>
        <div class="container">
            <div class="row">
                <div class="col-12 page-header">
					<?php
					if ( function_exists( 'yoast_breadcrumb' ) ) {
						yoast_breadcrumb( '<div class="breadcrumbs">', '</div>' );
					}
					?>
                    <h1 class="post-title"><?php echo get_the_title(); ?></h1>
                </div>

            </div>


    <?php
if ( have_posts() ) {
	get_template_part( '/partials/page/header' );
	wp_print_styles( 'team-members' );
	?>
		<div class="row members">
<?php
foreach ( $members as $member ) { ?>
    <div class="col-4">
        <a href="<?php echo esc_url( $member['url'] ); ?>" class="team-member-href">
            <div class="team-member">
                <div class="team-member-avatar-photo">
				    <?php echo wp_kses_post( wp_get_attachment_image($member['photo'], [88,88] ));?>
                </div>
                <div class="team-member-body">
                    <h3 class="team-member-name"><?php echo esc_attr( $member['name'] ); ?></h3>
                    <div class="team-member-position"><?php echo esc_attr( $member['position'] ); ?></div>
                    <div class="team-member-footer">
                        <div class="team-member-actions">
                            <span class="team-member-linkedin"
                                  data-href="<?php echo esc_url( $member['linkedin'] ); ?>"
                                  role="link" tabindex="0"
                                  aria-label="<?php echo esc_attr( $member['name'] ); ?> on LinkedIn (opens in new tab)">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.063 2.063 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                            </span>
                        </div>
                        <span class="team-member-cta">View Profile <svg class="team-member-cta-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
                    </div>
                </div>
                <img src="<?php echo esc_html( get_template_directory_uri() . '/assets/images/arrow-right.svg' ); ?>"
                     alt="right arrow"
                     height="16"
                     width="19">
            </div>
        </a>
    </div>
<?php } ?>

		</div>
    </div>
    </div>
    <?php
}
get_template_part( '/template-parts/footer/footer-cta-block' );
get_footer();
?>
<script id="cd-team-linkedin-click">
/* Make the LinkedIn icon inside each team card open its target URL in a new
 * tab. The icon is a <span role="link"> (not a real <a>) so it can sit inside
 * the existing card-wide <a class="team-member-href"> without nesting two
 * real anchors (which HTML5 forbids — parsers split them). The click handler
 * preventDefault + stopPropagation so the parent anchor's navigation to the
 * author page doesn't fire when the icon is clicked. */
(function(){
  function activate(el){
    var url = el.getAttribute('data-href');
    if (!url) return;
    if (url.indexOf('mailto:') === 0) {
      /* mailto: leaves the page via the mail-client handler — no need to
       * open in a new tab. */
      window.location.href = url;
    } else {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
  }
  var actionSel = '.team-member-linkedin[data-href], .team-member-email[data-href]';
  document.querySelectorAll(actionSel).forEach(function(el){
    el.addEventListener('click', function(e){
      e.preventDefault(); e.stopPropagation();
      activate(el);
    });
    el.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault(); e.stopPropagation();
        activate(el);
      }
    });
  });
})();
</script>
