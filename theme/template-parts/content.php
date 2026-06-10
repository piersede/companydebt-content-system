<?php
/**
 * Template part for displaying posts
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package CompanyDebt
 */
$author_id = get_the_author_meta('ID');
$author_nickname = get_the_author_meta('nickname');

?>

<div class="content">
    <div class="container">
        <div class="row">
            <div class="col-12 page-header">
	            <?php
	            if ( function_exists( 'yoast_breadcrumb' ) ) {
		            yoast_breadcrumb( '<div class="breadcrumbs">', '</div>'  );
	            }
	            ?>
                <h1 class="post-title"><?php the_title(); ?></h1>

                <?php
                /* Hero author + reviewed/reading-time block — mirrors the
                 * structure used by templates/take-the-test-template.php so
                 * single posts on the default template share the same hero
                 * design. Renders only if the author has a display name. */
                $_hero_author_id = get_the_author_meta('ID');
                if ( $_hero_author_id ) {
                    $_hero_author_name = get_the_author_meta('display_name', $_hero_author_id);
                    if ( $_hero_author_name ) {
                        $_hero_author_photo_id = get_field('photo', 'user_'. $_hero_author_id);
                        $_hero_author_position = get_field('professional_position', 'user_'. $_hero_author_id);
                        ?>
                        <div class="hero-author">
                            <?php if ( $_hero_author_photo_id ) {
                                echo wp_get_attachment_image( $_hero_author_photo_id, 'thumbnail', false, ["class" => "hero-author-photo", "alt" => esc_attr($_hero_author_name)] );
                            } ?>
                            <div class="hero-author-meta">
                                <div class="hero-author-name"><?php echo esc_html($_hero_author_name); ?></div>
                                <?php if ( $_hero_author_position ) { ?>
                                    <div class="hero-author-position"><?php echo esc_html($_hero_author_position); ?></div>
                                <?php } ?>
                            </div>
                        </div>
                        <div class="hero-author-reviewed">
                            <span class="hero-meta-item">
                                <svg class="hero-meta-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                                <span>Reviewed on <?php echo get_the_modified_date('d/m/Y'); ?></span>
                            </span>
                            <span class="hero-meta-divider" aria-hidden="true"></span>
                            <span class="hero-meta-item">
                                <svg class="hero-meta-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                                <span><?php if ( function_exists( 'cd_reading_time_minutes' ) ) { echo (int) cd_reading_time_minutes(); } ?>min read</span>
                            </span>
                        </div>
                        <?php
                    }
                }
                ?>
            </div>
            <div class="col-8 main-content">
                <?php
                if ( ! is_singular( 'testimonial' ) ) {
                    get_template_part( '/template-parts/review-author' );
                }
                ?>
                <?php 
                    ob_start();
                    the_content(); 
                    $content = ob_get_clean();
                    
                    echo toc_and_footnotes_in_content( $content );
                ?>
                <?php if ( have_rows('article_sources') ) { get_template_part( '/template-parts/footer/article-sources' );} ?>
            </div>
            <div class="col-4">
                <aside class="widget-area">
	                <?php dynamic_sidebar( 'sidebar-take-the-test' ); ?>
                </aside>
                <?php
                // Sidebar TOC (desktop). Rendered server-side as a sibling of
                // .widget-area so it gets col-4 as its sticky context. Hidden
                // on mobile by style.css; the in-body copy covers <992px.
                if ( isset( $content ) ) { echo cd_render_sidebar_toc( $content ); }
                ?>
            </div>
        </div>
    </div>
</div>
