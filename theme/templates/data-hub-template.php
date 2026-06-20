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
/* Rate + methodology are the only prose-heavy sections: their whole body reads
   at the primary prose size (18px), not just the lead. !important + this
   specificity is required to beat the Customizer's `.cd-data-hub p {14px !important}`.
   The rate caption (.cd-rate-text__note) is excluded and stays small. */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-rate-text p:not(.cd-rate-text__note),
body.page-template-data-hub-template .main-content .cd-data-hub .cd-method-inner p {
    font-size: 18px !important;
    line-height: 1.6 !important;
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

/* ============================================================
   2026-06-15 DESIGN REFINEMENT (Claude Design handoff) + layout pass.
   PART A — type scale 12/15/19/24/30/48 + 4px spacing tokens + KPI grid
            + aligned procedure cards + FAQ (from the exported design).
   PART B — layout fixes (single content rail, reading-width cap, TOC)
            from the earlier audit; the design didn't address alignment,
            so these compose with it.
   Every selector carries the body.page-template… .main-content prefix so
   it wins over the Customizer "Additional CSS" (.cd-data-hub p {14px!}).
   ============================================================ */
body.page-template-data-hub-template .main-content .cd-data-hub {
    --cd-read: 760px;
    --cd-s1: 8px;  --cd-s2: 16px; --cd-s3: 24px;
    --cd-s4: 40px; --cd-s5: 64px; --cd-s6: 96px;
}

/* ---- PART A · type scale ---- */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-main-kpi__v { font-size: 48px !important; letter-spacing: -0.03em !important; }
body.page-template-data-hub-template .main-content .cd-data-hub h2 { font-size: 30px !important; line-height: 1.15 !important; letter-spacing: -0.02em !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard p.cd-procard__value,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-mini-kpi__v,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-callout-card__v { font-size: 24px !important; line-height: 1.1 !important; letter-spacing: -0.02em !important; }
body.page-template-data-hub-template .main-content .cd-data-hub h3 { font-size: 19px !important; line-height: 1.35 !important; font-weight: 650 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-lede,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-hero .cd-lede,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-intro,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-rate-text p:not(.cd-rate-text__note),
body.page-template-data-hub-template .main-content .cd-data-hub .cd-method-inner p { font-size: 19px !important; line-height: 1.6 !important; font-weight: 400 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub p,
body.page-template-data-hub-template .main-content .cd-data-hub td,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-side-note__d,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-cite-text,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-cite-card dl,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-main-kpi__k,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard p.cd-procard__note,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-rate-text__note,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-source-note,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-figcaption,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard__link { font-size: 15px !important; }
body.page-template-data-hub-template .main-content .cd-data-hub h3.cd-side-note__v { font-size: 15px !important; font-weight: 650 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-eyebrow,
body.page-template-data-hub-template .main-content .cd-data-hub th,
body.page-template-data-hub-template .main-content .cd-data-hub caption,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-table__caption,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-mini-kpi__k,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-mini-kpi__n,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-callout-card__k,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-callout-card__u,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-side-notes__title,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-side-note--single .cd-side-note__k,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard h3.cd-procard__name,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-chart-controls__label,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-official-badge,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-meta-item span { font-size: 12px !important; }

/* ---- PART A · spacing rhythm (4px base) ---- */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section       { margin-top: var(--cd-s6) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-small { margin-top: var(--cd-s5) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-head  { margin-bottom: var(--cd-s4) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-eyebrow       { margin: 0 0 var(--cd-s2) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-intro { margin: var(--cd-s2) 0 0 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub p                 { margin: 0 0 var(--cd-s2) !important; line-height: 1.7 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-lede          { margin: 0 0 var(--cd-s4) !important; }

/* ---- PART A · KPI / rate callout grid ---- */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-callout-card { display: flex; flex-direction: column; gap: var(--cd-s2) !important; padding: var(--cd-s3) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-callout-card__row { display: grid !important; grid-template-columns: 1fr auto max-content !important; align-items: baseline !important; gap: 0 var(--cd-s2) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-callout-card__v { justify-self: end; text-align: right; margin: 0 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-callout-card__u { margin: 0 !important; font-weight: 500 !important; color: var(--cd-muted) !important; }

/* ---- PART A · procedure cards ---- */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard-grid { gap: var(--cd-s3) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard { padding: var(--cd-s3) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard h3.cd-procard__name { margin: 0 0 var(--cd-s2) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard p.cd-procard__value { margin: 0 0 var(--cd-s2) !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard p.cd-procard__note { margin: 0 0 var(--cd-s3) !important; line-height: 1.55 !important; min-height: calc(2 * 1.55 * 15px); }
/* Real procard notes run longer than the design's 2-line sample, so the
   min-height alone leaves CTAs drifting. Make cards equal-height flex columns
   and pin the link to the bottom so all five CTAs share a baseline. */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard { display: flex !important; flex-direction: column !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-procard .cd-procard__link { margin-top: auto !important; }

/* ---- PART A · per-stat internal rhythm (number→label 4px, label→note 2px) ---- */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-mini-kpi__v { margin: 0 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-mini-kpi__k { margin: 4px 0 0 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-mini-kpi__n { margin: 2px 0 0 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-main-kpi__v { margin: 0 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-main-kpi__k { margin: 4px 0 0 !important; }

/* ---- PART A · FAQ ---- */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-faq__q { font-size: 19px !important; font-weight: 550 !important; line-height: 1.5 !important; padding: 22px 24px !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-faq__a { padding: 0 24px 22px !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-faq__a p { font-size: 15px !important; line-height: 1.7 !important; color: var(--cd-text-soft) !important; }
@media (max-width: 720px) {
  body.page-template-data-hub-template .main-content .cd-data-hub .cd-faq__q { font-size: 17px !important; padding: 18px 20px !important; }
}

/* ---- PART B · reading-width cap + single content rail + TOC ---- */
body.page-template-data-hub-template .main-content .cd-data-hub h1,
body.page-template-data-hub-template .main-content .cd-data-hub h2,
body.page-template-data-hub-template .main-content .cd-data-hub h3:not(.cd-procard__name):not(.cd-side-notes__title),
body.page-template-data-hub-template .main-content .cd-data-hub .cd-lede,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-section-intro,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-rate-text p,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-method-inner p,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-method-inner li {
    max-width: var(--cd-read) !important;
    margin-left: 0 !important;
    margin-right: auto !important;
}
body.page-template-data-hub-template .main-content .cd-data-hub h1 { line-height: 1.15 !important; }
body.page-template-data-hub-template .main-content .cd-data-hub .cd-w-wide > .cd-section-head,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-w-wide .cd-rate-grid,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-method-inner {
    max-width: 1040px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
    box-sizing: border-box !important;
}
body.page-template-data-hub-template .main-content .cd-data-hub .cd-secnav {
    padding-left: max(24px, calc((100vw - 1040px) / 2 + 24px)) !important;
    padding-right: max(24px, calc((100vw - 1040px) / 2 + 24px)) !important;
    justify-content: flex-start !important;
    flex-wrap: wrap !important;
    row-gap: 8px !important;
}

/* Hero matches the design: the "Latest update" eyebrow badge is removed from
   the page content (build_insolvency_dashboard.py) and the byline is removed
   from the page-header markup above — no CSS hiding needed. */

/* ---- Shared text smoothing (cross-page consistency) ----
   The four sibling pages declare `-webkit-font-smoothing: antialiased` on
   .cd-data-hub; the flagship (uk-insolvency-statistics) omits it. Without it the
   browser uses default (subpixel) smoothing, which renders the SAME font-weight
   visibly heavier — so the flagship's masthead menu read as "bolder" than the
   others. Declare it here for every data-hub page so glyph rendering is uniform
   regardless of which page's inline CSS does or doesn't set it. */
body.page-template-data-hub-template .main-content .cd-data-hub,
body.page-template-data-hub-template .main-content .cd-data-hub * {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ---- Shared masthead rail (cross-page consistency) ----
   The .cd-masthead is the shared, persistent cross-page nav. It must resolve to
   the IDENTICAL 1040px centred rail on every data-hub page so it never shifts when
   navigating between them. The flagship (uk-insolvency-statistics) defines
   .cd-w-wide as a full-bleed 100vw band, so without this pin its masthead snaps to
   full width (measured: box -8→2552) and jumps ~144px vs the 1040 siblings. Pin
   ONLY the masthead here — the hero is aligned in the page's own CSS
   (build_insolvency_dashboard.py: .cd-w-hero spans the heading rail to the wide
   rail so the H1 sits under the logo). Do NOT add .cd-w-hero to this rule: forcing
   it to a centred 1040 rail cramps the hero's two-column grid. */
body.page-template-data-hub-template .main-content .cd-data-hub .cd-masthead,
body.page-template-data-hub-template .main-content .cd-data-hub .cd-masthead.cd-w-wide {
    width: auto !important;
    max-width: 1040px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
    box-sizing: border-box !important;
}
@media (max-width: 700px) {
    body.page-template-data-hub-template .main-content .cd-data-hub .cd-masthead,
    body.page-template-data-hub-template .main-content .cd-data-hub .cd-masthead.cd-w-wide {
        padding-left: 16px !important;
        padding-right: 16px !important;
    }
}

/* ---- Data hub owns its own menu ----
   The data hub carries its own masthead (.cd-masthead with .cd-mastnav) as its
   navigation, so the theme global site header is suppressed on this template.
   Scoped to this template only; the rest of the site keeps the normal header. */
body.page-template-data-hub-template #masthead.site-header { display: none !important; }
/* No WP breadcrumb above the data-hub masthead: the design puts the masthead
   at the very top (sibling pages use the in-page back-link instead). */
body.page-template-data-hub-template .page-header { display: none !important; }
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

                    <?php // Byline intentionally omitted — the hero matches the data-hub design (no byline). ?>
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
// dashboard provides its own final-CTA inline (.cd-final-cta). Author
// attribution is carried by the page's schema, not a visible byline.
get_template_part( '/template-parts/content', 'accreditation' );
get_footer();
