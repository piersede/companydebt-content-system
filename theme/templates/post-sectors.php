<?php
/**
 * Template Name: Sector Post - Page Builder
 * Template Post Type: post
 */

get_header();

$sector_title = get_field( 'featured_sector_title' );

if ( empty( $sector_title ) ) {
	$sector_title = get_the_category()[0]->name; 
}

if ( have_posts() ) { ?>
	<main id="primary" class="content site-main">
		<div class="container">
			<div class="row">
				<div class="col-12 page-header">
					<?php
					if ( function_exists( 'yoast_breadcrumb' ) ) {
						yoast_breadcrumb( '<div class="breadcrumbs">', '</div>' );
					}
					?>
                        <div class="sector-title">
                            <?php echo $sector_title; ?>
                        </div>
					<h1 class="post-title"><?php the_title(); ?></h1>
                    <div class="separator"></div>

                    <?php
                    // Hero author block — mirrors take-the-test-template.php
                    // Only renders if author has a name. 20260606
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

			</div>
		</div>
        <div class="container">
            <div class="row">
                <div class="col-12 content">
			        <?php the_content(); ?>
			        <?php if ( have_rows( 'article_sources' ) ) { get_template_part( '/template-parts/footer/article-sources' ); } ?>
                </div>
            </div>
        </div>
		<?php
		if ( have_rows( 'flexible_content' ) ) {
			$layout_number = 0;
			while ( have_rows( 'flexible_content' ) ) {
				the_row();
				$layout = get_row_layout();
				$layout_number ++;
				switch ( $layout ) {
					case 'left_wyswyg_right_bcg_image' :
						get_template_part( '/partials/page-builder/left-wyswyg-right-bcg-image' );
						break;
					case 'left_bcg_image_right_wyswyg' :
						get_template_part( '/partials/page-builder/left-bcg-image-right-wyswyg' );
						break;
					case 'two_halfs_full_width' :
						get_template_part( '/partials/page-builder/two-halfs-full-width' );
						break;
					case 'columns_full_width' :
						get_template_part( '/partials/page-builder/columns-full-width' );
						break;
					case 'accordion' :
						get_template_part( '/partials/page-builder/accordion' );
						break;
					case 'timeline' :
						get_template_part( '/partials/page-builder/timeline' );
						break;
					case 'bcg_image_full_width' :
						get_template_part( '/partials/page-builder/bcg-image-full-width' );
						break;
					case 'hero_bcg_image_full_width' :
						if ( is_front_page() && 1 === $layout_number ) {
							get_template_part( '/partials/page-builder/hero' );
						}
						break;
				}
			}
		}
		?>

	</main>
	<?php
}

/* Contact form section at the bottom — same partial used by /take-the-test/
 * and /about-us/. Fires for BOTH /sectors/ and /services-to/ posts; white
 * entry fields are styled in style.css under body.category-sectors (the
 * body class is now emitted for both URL families via functions.php). */
if ( is_singular( 'post' ) && ( in_category( 'sectors' ) || in_category( 'services-to' ) ) ) {
    get_template_part( '/template-parts/footer/footer-cta-block' );
}
?>


<?php /* Pressure-points icon replacement + sector-update box wrap + two-column
 * combined-section build. Fires for BOTH /sectors/ and /services-to/ posts
 * since the body class and CSS rules now span both URL families.
 * Walks every .column__container, reads the .column__descripton text, and
 * injects a sector-relevant SVG icon (Lucide-style, 30px, currentColor) in
 * the same circle wrapper the CSS expects. The combine step then mirrors
 * the editor-update block + pressure-points cards into a single two-column
 * layout (.cd-sector-combined). 20260606. */
if ( is_singular( 'post' ) && ( in_category( 'sectors' ) || in_category( 'services-to' ) ) ) : ?>
<script id="cd-pressure-points-icons">
(function(){
  // Each entry: [array of keyword substrings (lowercase), SVG inner markup].
  // First matching keyword wins; fall back to a generic alert-triangle icon.
  var ICONS = [
    /* /services-to/ vocabulary first — these labels talk about service
     * offerings, expertise and client relationships rather than the
     * pressure-points (labour, cashflow, etc) used on /sectors/. Put them
     * ahead of the /sectors/ entries so a /services-to/ card matches a
     * relevant icon rather than falling through to a generic one. */
    [ ['expand','offering','grow','growth','revenue stream','upsell'],
      '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/>' ], /* trending-up */
    [ ['expert','expertise','knowledge','specialist','qualified','professional credential','licensed'],
      '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>' ], /* award/medal */
    [ ['relationship','partner','partnership','collaboration','nurture','retain','retention','client base'],
      '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>' ], /* users (group) */
    [ ['conflict','independent','impartial','unbias','unbiased','neutral','fair','no bias'],
      '<line x1="12" y1="3" x2="12" y2="21"/><line x1="5" y1="9" x2="19" y2="9"/><path d="M5 9l-3 6h6l-3-6z"/><path d="M19 9l-3 6h6l-3-6z"/>' ], /* scale of justice */
    [ ['accountan','book-keep','bookkeep','accounting','audit','ledger'],
      '<rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="16" y2="14"/><line x1="8" y1="18" x2="12" y2="18"/>' ], /* document with lines */
    [ ['referral','introduce','introduction','warm intro','recommend'],
      '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>' ], /* arrow-right */
    [ ['lawyer','solicitor','legal counsel','barrister','adviser','advice'],
      '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><circle cx="12" cy="14" r="2"/>' ], /* file with badge */
    [ ['lender','bank','banker','finance provider','funder','funding'],
      '<rect x="3" y="5" width="18" height="14" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="7" y1="15" x2="9" y2="15"/>' ], /* credit-card */
    [ ['start to finish','start-to-finish','end-to-end','end to end','from start','to finish','throughout','journey','step by step'],
      '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>' ], /* compass — used for "Support from start to finish" on /services-to/creditors/. NB: do not add 'navigate' here — it would steal the shield+tick match from "navigate the rules". */
    /* /sectors/ vocabulary follows */
    [ ['labour','labor','staff','workforce','employee','skill','recruit'],
      '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>' ],
    [ ['cashflow','cash flow','cash','liquidity','debt','financ','revenue','margin','profit'],
      '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>' ],
    [ ['covid','pandemic','virus','disease','health crisis'],
      '<circle cx="12" cy="12" r="9"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>' ],
    [ ['payment','late pay','invoice','credit','overdue'],
      '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>' ],
    [ ['cost','inflation','price','rising','expense','overhead'],
      '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/>' ],
    [ ['brexit','tariff','import','export','border','customs'],
      '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/>' ],
    [ ['supply','logistic','distribution','transport','haulage','delivery'],
      '<rect x="1" y="3" width="15" height="13" rx="2"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>' ],
    [ ['tax','hmrc','vat','paye','corporation','revenue'],
      '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/>' ],
    [ ['regulation','complian','legal','law','rule'],
      '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>' ],
    [ ['competit','market share','rival'],
      '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0z"/>' ],
    [ ['demand','footfall','customer','consumer'],
      '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>' ],
    [ ['energy','fuel','gas','electric','power','utility'],
      '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>' ],
    [ ['rent','lease','property','premise'],
      '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>' ],
    [ ['season','weather','climate'],
      '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>' ],
    [ ['cyber','data','digital','online','tech'],
      '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>' ],
    [ ['safety','accident','injury','risk'],
      '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>' ],
  ];
  var DEFAULT_ICON =
    '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>';

  function pickIcon(text){
    var t = (text || '').toLowerCase();
    for (var i = 0; i < ICONS.length; i++) {
      var keys = ICONS[i][0];
      for (var j = 0; j < keys.length; j++) {
        if (t.indexOf(keys[j]) !== -1) return ICONS[i][1];
      }
    }
    return DEFAULT_ICON;
  }

  function svgWrap(inner){
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
           'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' +
           'aria-hidden="true">' + inner + '</svg>';
  }

  function run(){
    /* Step 1: Wrap the paragraphs under the "Sector update" heading in a
     * styled box. The H3 itself stays outside the box. */
    document.querySelectorAll('.editor-update-block').forEach(function(block){
      if (block.querySelector('.cd-sector-update-box')) return;
      var heading = block.querySelector('h2, h3, h4');
      if (!heading) return;
      var box = document.createElement('div');
      box.className = 'cd-sector-update-box';
      var next = heading.nextElementSibling;
      while (next) {
        var following = next.nextElementSibling;
        box.appendChild(next);
        next = following;
      }
      heading.parentNode.insertBefore(box, heading.nextSibling);
    });

    /* Step 2: Inject sector-relevant SVG icons into each pressure-point
     * card. The cards stay in their original .columns__full_width DOM at
     * this point — the combineSections step below moves them into the new
     * two-column layout. */
    var cards = document.querySelectorAll('.columns__full_width .column__container');
    cards.forEach(function(card){
      if (card.querySelector('.column__icon')) return;
      /* The pressure-points partial puts the label in different fields
       * across the two post categories:
       *   - /sectors/ posts:      .column__descripton ("Labour Shortages")
       *   - /services-to/ posts:  .column__heading    ("Help You Nurture...")
       * Read both and pick whichever has content — the icon-picker keyword
       * match works on either source. */
      var desc = card.querySelector('.column__descripton');
      var heading = card.querySelector('.column__heading');
      var label = '';
      if (desc && desc.textContent.trim()) label = desc.textContent;
      else if (heading && heading.textContent.trim()) label = heading.textContent;
      var iconHtml = '<span class="column__icon">' + svgWrap(pickIcon(label)) + '</span>';
      var top = card.querySelector('.column__top');
      if (!top) return;
      top.insertAdjacentHTML('afterbegin', iconHtml);
    });

    /* Step 3: Combine the sector-update block and the pressure-points
     * section into a single two-column section. Left column: the
     * "Sector update" H3 + box. Right column: a "<sector> Sector Pressure
     * Points" H3 + a vertical list of icon-plus-label rows. The originals
     * are hidden once their content has been mirrored into the new layout. */
    combineSections();
  }

  function combineSections(){
    if (document.querySelector('.cd-sector-combined')) return; /* already built */
    var editorBlock = document.querySelector('.editor-update-block');
    var ppSection = document.querySelector('.columns__full_width');
    if (!editorBlock || !ppSection) return;
    var updateHeading = editorBlock.querySelector('h2, h3, h4');
    var updateBox = editorBlock.querySelector('.cd-sector-update-box');
    if (!updateHeading || !updateBox) return;
    var ppTitle = ppSection.querySelector('.section_title');
    var ppCards = ppSection.querySelectorAll('.column__container');
    if (!ppTitle || !ppCards.length) return;

    var wrap = document.createElement('div');
    wrap.className = 'cd-sector-combined';

    /* LEFT — sector update */
    var left = document.createElement('div');
    left.className = 'cd-sector-combined__col cd-sector-combined__left';
    var leftH = document.createElement('h3');
    leftH.className = 'cd-sector-combined__title';
    leftH.textContent = updateHeading.textContent.trim();
    left.appendChild(leftH);
    left.appendChild(updateBox.cloneNode(true));

    /* RIGHT — pressure points list */
    var right = document.createElement('div');
    right.className = 'cd-sector-combined__col cd-sector-combined__right';
    var rightH = document.createElement('h3');
    rightH.className = 'cd-sector-combined__title cd-pressure-points-title';
    rightH.textContent = ppTitle.textContent.trim();
    right.appendChild(rightH);

    var list = document.createElement('div');
    list.className = 'cd-pressure-points-list';
    ppCards.forEach(function(card){
      var icon = card.querySelector('.column__icon');
      var label = card.querySelector('.column__descripton');
      if (!icon && !label) return;
      var item = document.createElement('div');
      item.className = 'cd-pressure-points-list__item';
      if (icon) item.appendChild(icon.cloneNode(true));
      if (label) {
        var lbl = document.createElement('span');
        lbl.className = 'cd-pressure-point-label';
        lbl.textContent = label.textContent.trim();
        item.appendChild(lbl);
      }
      list.appendChild(item);
    });
    right.appendChild(list);

    wrap.appendChild(left);
    wrap.appendChild(right);

    /* Place the new section where the pressure-points section currently
     * sits, then hide both originals. */
    ppSection.parentNode.insertBefore(wrap, ppSection);
    ppSection.style.display = 'none';
    editorBlock.style.display = 'none';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
</script>
<?php endif; ?>

<?php
get_footer();
?>
