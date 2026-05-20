<?php
/**
 * Template Name: Data Hub Template
 *
 * Full-width variant used for data dashboards (e.g. /uk-insolvency-statistics/).
 * The page-title H1 is suppressed here because data-hub content owns its own
 * hero with H1. Body padding-right is neutralised so the dashboard can manage
 * its own multi-width layout. The theme's footer-author and footer-cta blocks
 * are suppressed — the dashboard provides its own final CTA inline.
 *
 * @package CompanyDebt
 */

get_header();

?>

<style id="cd-data-hub-layout">
/* Neutralise the 144px right padding the theme reserves for the sidebar on
   .main-content. The data-hub template has no sidebar and the dashboard
   manages widths section-by-section. */
body.page-template-data-hub-template .main-content,
body.page-template-data-hub-template .col-12.main-content.data-hub-content {
    padding-right: 15px;
    max-width: 100%;
}
body.page-template-data-hub-template .cd-data-hub { max-width: none; }

/* Theme rule `body.page .main-content h2/h3/p` is high specificity and will
   override the dashboard's scoped typography. Re-state at matching
   specificity so dashboard typography wins inside .cd-data-hub. */
body.page-template-data-hub-template .main-content .cd-data-hub h1,
body.page-template-data-hub-template .main-content .cd-data-hub h2,
body.page-template-data-hub-template .main-content .cd-data-hub h3 {
    padding-top: 0;
    margin-top: 0;
}
body.page-template-data-hub-template .main-content .cd-data-hub h1 {
    font-size: clamp(44px, 5vw, 68px);
    line-height: 0.98;
    letter-spacing: -0.04em;
    font-weight: 700;
    margin: 0 0 1.25rem;
}
body.page-template-data-hub-template .main-content .cd-data-hub h2 {
    font-size: clamp(32px, 3.4vw, 44px);
    line-height: 1.08;
    letter-spacing: -0.025em;
    font-weight: 700;
    margin: 0;
}
body.page-template-data-hub-template .main-content .cd-data-hub h3 {
    font-size: 22px;
    line-height: 1.25;
    font-weight: 650;
    margin: 1.5em 0 0.6em;
}
body.page-template-data-hub-template .main-content .cd-data-hub p {
    font-size: 17px;
    line-height: 1.65;
    margin: 0 0 18px;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-lede {
    font-size: 20px;
    line-height: 1.55;
    margin: 0 0 1.75rem;
    max-width: 660px;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-intro {
    font-size: 18px;
    line-height: 1.6;
    margin: 16px 0 0;
    max-width: 720px;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-source-note {
    font-size: 13px;
    line-height: 1.55;
    margin: 14px 0 0;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-rate-text p {
    font-size: 17px;
    line-height: 1.65;
}
/* Page-header (breadcrumbs + byline) sits in the WP .container at the top.
   Match dashboard rhythm with a sensible margin below. */
body.page-template-data-hub-template .page-header {
    max-width: 1280px;
    margin: 0 auto;
    padding: 16px 24px 0;
}
body.page-template-data-hub-template .data-hub-byline {
    margin: 0.5rem 0 0;
    font-size: 14px;
    color: #667085;
}
body.page-template-data-hub-template .data-hub-byline__by {
    color: #98a2b3;
    margin-right: 0.25rem;
}
body.page-template-data-hub-template .data-hub-byline__name {
    color: #101828;
    font-weight: 500;
}
body.page-template-data-hub-template .data-hub-byline__sep {
    margin: 0 0.45rem;
    color: #d0d5dd;
}
</style>

<main id="primary" class="site-main">
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

                    <?php
                    // Compact byline: author name + last reviewed date only.
                    $_hero_author_id = get_the_author_meta('ID');
                    if ( $_hero_author_id ) {
                        $_hero_author_name = get_the_author_meta('display_name', $_hero_author_id);
                        if ( $_hero_author_name ) {
                            ?>
                            <p class="data-hub-byline">
                                <span class="data-hub-byline__by">By</span>
                                <span class="data-hub-byline__name"><?php echo esc_html($_hero_author_name); ?></span>
                                <span class="data-hub-byline__sep" aria-hidden="true">·</span>
                                <span class="data-hub-byline__date">Reviewed on <?php echo get_the_modified_date('j F Y'); ?></span>
                            </p>
                            <?php
                        }
                    }
                    ?>
                </div>

                <div class="col-12 main-content data-hub-content">
                    <?php
                    ob_start();
                    the_content();
                    $content = ob_get_clean();
                    echo toc_and_footnotes_in_content( $content );
                    ?>
                    <?php if ( have_rows('article_sources') ) { get_template_part( '/template-parts/footer/article-sources' ); } ?>
                </div>
            </div>
        </div>
    </div>
</main>

<?php
// The footer-author and footer-cta blocks are intentionally omitted — the
// dashboard byline at the top establishes attribution, and the dashboard
// provides its own final-CTA inline (.cd-final-cta).
get_template_part( '/template-parts/content', 'accreditation' );
get_footer();
