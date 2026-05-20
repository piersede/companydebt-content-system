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
/* The dashboard uses width:100vw + negative-margin bleed sections. On mobile
   the parent container is slightly narrower than the viewport (scrollbar gutter),
   which makes those sections push past the body. Clip horizontal overflow at
   the body level so nothing escapes the viewport. */
body.page-template-data-hub-template { overflow-x: hidden; }

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
    font-size: clamp(40px, 5vw, 56px);
    line-height: 1.02;
    letter-spacing: -0.04em;
    font-weight: 700;
    margin: 0 0 32px;
}
body.page-template-data-hub-template .main-content .cd-data-hub h2 {
    font-size: 32px;
    line-height: 1.12;
    letter-spacing: -0.025em;
    font-weight: 700;
    margin: 0;
}
body.page-template-data-hub-template .main-content .cd-data-hub h3 {
    font-size: 20px;
    line-height: 1.3;
    font-weight: 650;
    margin: 40px 0 16px;
}
/* Procedure card name is semantic H3 but visually a small uppercase label. */
body.page-template-data-hub-template .main-content .cd-data-hub h3.cd-procard__name {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #667085;
    font-weight: 700;
    margin: 0 0 8px;
    line-height: 1.3;
}
/* Long-run side-note value is semantic H3 but visually a calm 16px label. */
body.page-template-data-hub-template .main-content .cd-data-hub h3.cd-side-note__v {
    font-size: 16px;
    font-weight: 650;
    color: #101828;
    margin: 0 0 6px;
    line-height: 1.3;
    letter-spacing: -0.005em;
    text-transform: none;
}
body.page-template-data-hub-template .main-content .cd-data-hub p {
    font-size: 14px;
    line-height: 1.65;
    margin: 0 0 16px;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-lede {
    font-size: 18px;
    line-height: 1.55;
    margin: 0 0 32px;
    max-width: 660px;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-intro {
    font-size: 18px;
    line-height: 1.6;
    margin: 16px 0 0;
    max-width: 720px;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-source-note {
    font-size: 12px;
    line-height: 1.55;
    margin: 12px 0 0;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-rate-text p {
    font-size: 14px;
    line-height: 1.65;
}
/* Page-header (breadcrumbs + byline) shares the hero's 1240px container so
   all top elements align to the same left/right edges. */
body.page-template-data-hub-template .page-header {
    max-width: 1240px;
    margin: 0 auto 32px;
    padding: 24px 32px 0;
}
body.page-template-data-hub-template .page-header .breadcrumbs {
    margin-bottom: 12px;
    font-size: 13px;
    color: #9ca3af;
}
/* Byline as compact metadata, not attribution. Date is bolded — it carries
   the freshness signal — and the author name sits in muted text. */
body.page-template-data-hub-template .data-hub-byline {
    margin: 0;
    font-size: 13px;
    color: #9ca3af;
    font-weight: 400;
}
body.page-template-data-hub-template .data-hub-byline__by { color: #9ca3af; margin-right: 0.25rem; }
body.page-template-data-hub-template .data-hub-byline__name { color: #9ca3af; font-weight: 400; }
body.page-template-data-hub-template .data-hub-byline__sep { margin: 0 0.45rem; color: #d0d5dd; }
body.page-template-data-hub-template .data-hub-byline__date { color: #4b5563; font-weight: 600; }
/* Mobile: tighten page-header to match hero's mobile inline padding. */
@media (max-width: 700px) {
    body.page-template-data-hub-template .page-header {
        padding: 24px 20px 0;
        margin-bottom: 40px;
    }
}
/* Hide the theme's auto-injected Related Articles section on this template —
   the data-hub brief specifies: keep only Source/citation and the bottom CTA
   after the data sections. */
body.page-template-data-hub-template .be-related-articles { display: none !important; }
/* Hide the theme's auto-injected "Get Called Back" gravity-form widget that
   the after-breadcrumbs-area hook prepends to every page. The dashboard
   provides its own CTA at the bottom and the form above the data is noise. */
body.page-template-data-hub-template #after-breadcrumbs-area,
body.page-template-data-hub-template .section-cd-gravity-form-widget { display: none !important; }
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
                                <span class="data-hub-byline__date">Reviewed <?php echo get_the_modified_date('j F Y'); ?></span>
                                <span class="data-hub-byline__sep" aria-hidden="true">·</span>
                                <span class="data-hub-byline__by">By</span>
                                <span class="data-hub-byline__name"><?php echo esc_html($_hero_author_name); ?></span>
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
