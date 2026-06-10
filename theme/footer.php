<?php
/**
 * The template for displaying the footer
 *
 * Contains the closing of the #content div and all content after.
 *
 * @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
 *
 * @package CompanyDebt
 */

global $post;

// 2026-05-19: suppress related-articles section on category archives and on
// posts/pages using the Single Post Full Width template (templates/content-single-post-full-width.php).
// All other templates (take-the-test, post-default single.php, post-sectors, etc.)
// continue to follow the enable_related_articles ACF field logic below.
// 2026-05-20: related-articles section disabled site-wide.
// Backend (template-part, JS, CSS) intact -- re-enable by removing this single
// reassignment so the conditional below applies again.
$cd_disable_related = true;
/* original conditional kept for reference:
$cd_disable_related = (
    is_category()
    || is_page_template( 'templates/content-single-post-full-width.php' )
);
*/

if ( ! $cd_disable_related && $post && ( get_field( 'enable_related_articles', $post->ID ) || ! metadata_exists( 'post', $post->ID, 'enable_related_articles' ) ) ) {
    get_template_part( '/template-parts/related-articles/related-articles' );
}
?>
    <?php if ( ! is_page_template( 'templates/blank-landing-page.php' ) ) : ?>

	<footer id="colophon" class="site-footer">
		<?php if( current_user_can( 'administrator' ) ) { ?>
            <div class="chat-img">
                <img src="<?php echo esc_url( get_template_directory_uri(  ) . '/assets/images/chat-person.jpeg' ) ?>" height="60" width="60" alt="chat person" title="Company Debt chat" class="chat-person-img">

            </div>

		<?php } ?>

		<div class="container">
            <div class="row">
                <div class="col-6">
                    <div class="site-branding">
	                    <?php if ( is_page_template( 'templates/design-22-v1.php' ) ) { ?>
                        <a href="https://www.companydebt.com">
                            <img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/logo-design22-1-text-pink.png' ); ?>" height="56" width="227" alt="Company Debt Logo" title="Company Debt" class="header__logo">
                        </a>
                        <?php } else { ?>
		                <?php the_custom_logo(); ?>
                        <?php } ?>
                    </div><!-- .site-branding -->
                    <div class="footer-tagline"><?php the_field( 'tagline', 'option' );?></div>
                </div>
                <div class="col-6">
                    <ul class="social-icons">
	                    <?php
	                    // check if the repeater field has rows of data
	                    if ( have_rows('socials', 'option') ):
		                    // loop through the rows of data
		                    while ( have_rows('socials', 'option') ) : the_row();
			                    // display a sub field value
			                    ?>
                                <li><a href="<?php the_sub_field( 'link' ); ?>"><?php echo wp_get_attachment_image( get_sub_field( 'icon' ), 'full', false,  ["class" => "social-media-icon"] ); ?>
                                    </a></li>
			                <?php
			                endwhile;
		                endif;
		                ?>
                    </ul>
                </div>
            </div>
            <div class="row">
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-1-sidebar' ); ?>
                </div>
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-2-sidebar' ); ?>
                </div>
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-3-sidebar' ); ?>
                </div>
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-4-sidebar' ); ?>
                </div>
                <div class="col-12">
                    <div class="footer_disclaimer"><a href="/privacy-policy/">Privacy Policy</a> | <a href="/terms-conditions/">Terms and Conditions</a> | <a href="/cookie-policy/">Cookie Policy</a> | <a href="/site-map/">Site Map</a><br><br><?php the_field( 'disclaimer', 'option' ); ?></div>
                </div>
            </div>
        </div>
	</footer><!-- #colophon -->
    <?php endif; ?>
</div><!-- #page -->

<?php wp_footer(); ?>
<script id="cd-footer-v2-relocate">
/* Footer v2: move Privacy / Terms / Cookies / Sitemap out of the bottom
 * disclaimer row and into the Contact Us column (block-37) as discrete pills,
 * right after the accreditation logos. Cleans up the " | " text separators
 * and the two <br>s that previously joined them inline with the disclaimer.
 * Companion CSS in style.css styles .cd-footer-policy-links.
 * Kill switch: drop data-footer-v2 in header.php — this script becomes a
 * no-op (returns early). */
(function(){
  if (document.documentElement.dataset.footerV2 !== 'on') return;
  function relocate(){
    var disc = document.querySelector('footer#colophon .footer_disclaimer');
    var contact = document.querySelector('footer#colophon #block-37');
    if (!disc || !contact || disc.dataset.cdFooterV2 === '1') return;
    var links = Array.from(disc.querySelectorAll(':scope > a'));
    if (!links.length) return;
    var holder = document.createElement('div');
    holder.className = 'cd-footer-policy-links';
    links.forEach(function(a){ holder.appendChild(a); });   /* moves, not copies */
    /* Strip leading separator text (" | ") and <br> nodes left behind so the
     * disclaimer paragraph starts cleanly. */
    while (disc.firstChild) {
      var n = disc.firstChild;
      if (n.nodeType === 1 && n.tagName === 'BR') { disc.removeChild(n); continue; }
      if (n.nodeType === 3) {
        var t = n.nodeValue.replace(/\s+/g,' ').trim();
        if (t === '' || t === '|') { disc.removeChild(n); continue; }
      }
      break;
    }
    /* Place the policy links as a discrete row UNDER the disclaimer paragraph
     * (sibling, not nested), so they don't break the disclaimer text flow. */
    if (disc.parentNode) disc.parentNode.insertBefore(holder, disc.nextSibling);
    else contact.appendChild(holder);
    /* Move .social-icons out of the top row into the Contact column (not
     * adjacent to the policy links, which now live in col-12). Append at the
     * end of #block-37. Strip loading="lazy" — the lazy IntersectionObserver
     * was wired to the old DOM position so the moved icons would otherwise sit
     * unloaded (naturalWidth=0) until the user scrolled to the original location
     * (which no longer exists). */
    var social = document.querySelector('footer#colophon .social-icons');
    if (social) {
      social.querySelectorAll('img').forEach(function(img){
        img.removeAttribute('loading');
        /* Force re-fetch by re-setting src — needed when img.complete is false */
        if (!img.complete || img.naturalWidth === 0) {
          var src = img.getAttribute('src');
          img.removeAttribute('src');
          img.setAttribute('src', src);
        }
      });
      contact.appendChild(social);
    }
    /* Move .site-branding (logo) into the Contact column as the FIRST child.
     * The logo then top-aligns with the category column titles since they all
     * start at the same row position. Original row 1 becomes empty and is
     * hidden on desktop via the companion CSS. */
    var branding = document.querySelector('footer#colophon .site-branding');
    if (branding) {
      contact.insertBefore(branding, contact.firstChild);
    }
    disc.dataset.cdFooterV2 = '1';
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', relocate);
  else relocate();
})();
</script>
<script id="cd-cls-chat-unlock">
/* CLS fix companion — release the #chat-widget-container dimension lock
 * (defined in style.css) as soon as the user shows intent to interact
 * with the LiveChat bubble (hover, touch, or focus near it). The unlock
 * fires BEFORE click, so click-to-expand opens the chat normally. */
(function(){
  var html = document.documentElement;
  if (!html) return;
  function unlock(){
    html.setAttribute('data-cd-chat-ready', '1');
    document.removeEventListener('mouseover', check, true);
    document.removeEventListener('touchstart', check, true);
    document.removeEventListener('focusin', check, true);
  }
  function check(e){
    var t = e.target;
    if (!t) return;
    if (t.id === 'chat-widget-container' ||
        (t.closest && t.closest('#chat-widget-container'))) {
      unlock();
    }
  }
  document.addEventListener('mouseover', check, true);
  document.addEventListener('touchstart', check, true);
  document.addEventListener('focusin', check, true);
})();
</script>
<script id="cd-faq-toggle-fallback">
/* Universal chevron injection + click fallback.
 *
 * Chevron injection (runs sitewide): the plugin's chevron is drawn via CSS
 * ::after + transparent borders + transform. On pages where the plugin's
 * stylesheet isn't enqueued, the chevron disappears entirely. We inject our
 * own inline SVG chevron into every state-indicator so the visual is
 * consistent regardless of plugin CSS state. Companion CSS in style.css
 * hides the plugin's ::after to avoid double-chevron on working pages.
 *
 * Click fallback (only on pages without plugin JS): when the plugin's
 * blocks.style.build.css isn't on the page, the plugin's front.build.js
 * is presumably also missing, so clicks don't toggle anything. We attach
 * a vanilla click handler to the WHOLE accordion card (not just the title)
 * that mirrors the plugin's logic: toggle .ub-hide + .open + aria-expanded,
 * respect data-showonlyone. */
(function(){
  var CHEVRON_SVG = '<svg class="cd-faq-chevron" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>';
  function pluginLoaded(){
    return Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
      .some(function(l){ return /ultimate-blocks\/dist\/blocks\.style\.build\.css/.test(l.href || ''); });
  }
  function injectChevrons(){
    document.querySelectorAll('.wp-block-ub-content-toggle-accordion-state-indicator').forEach(function(ind){
      if (ind.querySelector('.cd-faq-chevron')) return;
      ind.innerHTML = CHEVRON_SVG;
    });
  }
  var ANIM_MS = 400; /* matches the 0.4s used by the plugin path */
  function animateExpand(content){
    /* Step 1: unhide + set collapsed start state. The element now sits in flow
     * at its real parent width (so scrollHeight reports the correct target). */
    content.classList.remove('ub-hide');
    content.style.height = '0px';
    content.style.overflow = 'hidden';
    /* Step 2: read target via scrollHeight on the ORIGINAL element — gives the
     * natural content+padding height at the actual rendered width. Clones with
     * position:absolute use shrink-to-fit width and wrap text differently,
     * producing the wrong target (bug we hit earlier). */
    void content.offsetHeight;
    var targetH = content.scrollHeight;
    /* Step 3: commit start state with one rAF, then in the next frame add the
     * transition class + target. Double-rAF guarantees the start state is on
     * screen before the transition begins. */
    requestAnimationFrame(function(){
      content.classList.add('cd-faq-animating');
      requestAnimationFrame(function(){
        content.style.height = targetH + 'px';
      });
    });
    setTimeout(function(){
      content.classList.remove('cd-faq-animating');
      content.style.height = '';
      content.style.overflow = '';
      content.setAttribute('aria-expanded', 'true');
    }, ANIM_MS + 50);
  }
  function animateCollapse(content){
    var startH = content.offsetHeight;
    content.style.height = startH + 'px';
    void content.offsetHeight;
    requestAnimationFrame(function(){
      content.classList.add('cd-faq-animating');
      requestAnimationFrame(function(){
        content.style.height = '0px';
      });
    });
    setTimeout(function(){
      content.classList.add('ub-hide');
      content.classList.remove('cd-faq-animating');
      content.style.height = '';
      content.setAttribute('aria-expanded', 'false');
    }, ANIM_MS + 50);
  }
  function toggleFallback(titleWrap){
    var contentWrap = titleWrap.nextElementSibling;
    if (!contentWrap || !contentWrap.classList.contains('wp-block-ub-content-toggle-accordion-content-wrap')) return;
    /* Guard against double-clicks during the animation */
    if (contentWrap.dataset.cdAnimating === '1') return;
    contentWrap.dataset.cdAnimating = '1';
    setTimeout(function(){ delete contentWrap.dataset.cdAnimating; }, ANIM_MS + 50);
    var indicator = titleWrap.querySelector('.wp-block-ub-content-toggle-accordion-state-indicator');
    var container = titleWrap.closest('.wp-block-ub-content-toggle');
    var wasHidden = contentWrap.classList.contains('ub-hide');
    if (wasHidden) {
      /* Single-open: collapse all other panels in this container with animation */
      if (container && container.dataset.showonlyone === 'true') {
        container.querySelectorAll('.wp-block-ub-content-toggle-accordion-content-wrap').forEach(function(w){
          if (w !== contentWrap && !w.classList.contains('ub-hide')) animateCollapse(w);
        });
        container.querySelectorAll('.wp-block-ub-content-toggle-accordion-state-indicator').forEach(function(i){
          if (i !== indicator) i.classList.remove('open');
        });
      }
      animateExpand(contentWrap);
      if (indicator) indicator.classList.add('open');
    } else {
      animateCollapse(contentWrap);
      if (indicator) indicator.classList.remove('open');
    }
  }
  function attachFallbackClicks(){
    document.querySelectorAll('.wp-block-ub-content-toggle-accordion').forEach(function(card){
      card.style.cursor = 'pointer';
      var titleWrap = card.querySelector('.wp-block-ub-content-toggle-accordion-title-wrap');
      if (!titleWrap) return;
      titleWrap.setAttribute('tabindex', '0');
      card.addEventListener('click', function(e){
        /* Ignore clicks inside the expanded content panel (so users can select text) */
        if (e.target.closest('.wp-block-ub-content-toggle-accordion-content-wrap')) return;
        toggleFallback(titleWrap);
      });
      titleWrap.addEventListener('keydown', function(e){
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleFallback(titleWrap); }
      });
    });
  }
  function init(){
    injectChevrons();
    if (!pluginLoaded()) attachFallbackClicks();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
<script id="cd-related-guides">
/* Transform the "Related Guides" section into a grid of cards.
 * Source markup: <h2>Related Guides</h2> + <ul class="wp-block-list"><li><a>Title</a>: description</li>...</ul>
 * Output: <div class="cd-related-grid">[card, card, ...]</div>
 * Each card: icon (topic-derived) + category tag (URL path segment) + title + description + "Read guide ->" CTA.
 * Card is clickable as a whole via JS; description can still contain nested links. */
(function(){
  var SVG = {
    scales:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M4 21h16M6 6h12"/><path d="M7 6l-3 7a4 4 0 0 0 6 0L7 6zM17 6l-3 7a4 4 0 0 0 6 0l-3-7z"/></svg>',
    alert:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    receipt:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 2v20l3-2 3 2 3-2 3 2 3-2 1 2V2"/><line x1="8" y1="8" x2="16" y2="8"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="8" y1="16" x2="12" y2="16"/></svg>',
    lifebuoy:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="4.93" y1="4.93" x2="9.17" y2="9.17"/><line x1="14.83" y1="14.83" x2="19.07" y2="19.07"/><line x1="14.83" y1="9.17" x2="19.07" y2="4.93"/><line x1="4.93" y1="19.07" x2="9.17" y2="14.83"/></svg>',
    folder:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    info:      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    shield:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    envelope:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    pound:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 6.5a4 4 0 0 0-7 3v2H7M7 12h8M7 18h11"/><path d="M10 18c1.5 0 3-1.2 3-3v-2"/></svg>',
    chart:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>',
    file:      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    user:      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    heart:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    book:      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    arrow:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
  };
  /* Map URL first-path-segment → { category label, icon } */
  var CATS = {
    'liquidation':                    { label: 'LIQUIDATION', icon: SVG.scales },
    'insolvency':                     { label: 'INSOLVENCY', icon: SVG.alert },
    'hmrc':                           { label: 'HMRC', icon: SVG.receipt },
    'company-rescue-solutions':       { label: 'RESCUE', icon: SVG.lifebuoy },
    'company-administration':         { label: 'ADMINISTRATION', icon: SVG.folder },
    'advice':                         { label: 'ADVICE', icon: SVG.info },
    'director-protection-hub':        { label: 'DIRECTOR PROTECTION', icon: SVG.shield },
    'sample-letters':                 { label: 'LETTERS', icon: SVG.envelope },
    'bounce-back-loan-support-hub':   { label: 'BOUNCE BACK LOAN', icon: SVG.pound },
    'company-cash-flow-problems':     { label: 'CASH FLOW', icon: SVG.chart },
    'case-studies':                   { label: 'CASE STUDY', icon: SVG.book },
    'insolvency-news-commentary':     { label: 'NEWS', icon: SVG.book },
    'mental-health-debt-stress-support': { label: 'WELLBEING', icon: SVG.heart },
    'hospitality-restaurant-insolvency': { label: 'INDUSTRY', icon: SVG.file },
    'construction-insolvency':        { label: 'INDUSTRY', icon: SVG.file },
    'transport-haulage-insolvency':   { label: 'INDUSTRY', icon: SVG.file },
    'charity-non-profit-insolvency':  { label: 'INDUSTRY', icon: SVG.file },
    'professional-services-insolvency': { label: 'INDUSTRY', icon: SVG.file },
  };
  var DEFAULT_CAT = { label: 'GUIDE', icon: SVG.file };
  function categoryFor(href){
    try {
      var u = new URL(href, location.href);
      var segs = u.pathname.split('/').filter(Boolean);
      if (!segs.length) return DEFAULT_CAT;
      return CATS[segs[0]] || { label: segs[0].toUpperCase().replace(/-/g, ' '), icon: SVG.file };
    } catch(e) { return DEFAULT_CAT; }
  }
  /* When the grid has more than this many cards, collapse + show "Show More" button.
   * 6 = 2 desktop rows (3 cols × 2 rows). Items beyond row 2 hide; row 2 fades. */
  var COLLAPSE_THRESHOLD = 6;
  function transformOne(h2){
    var ul = h2.nextElementSibling;
    if (!ul || ul.tagName !== 'UL' || ul.dataset.cdRelatedTransformed === '1') return;
    var items = Array.from(ul.querySelectorAll(':scope > li'));
    if (!items.length) return;
    var grid = document.createElement('div');
    grid.className = 'cd-related-grid';
    items.forEach(function(li){
      var firstLink = li.querySelector('a');
      if (!firstLink) return;
      var title = firstLink.textContent.trim();
      var href = firstLink.getAttribute('href') || '#';
      /* Build description = inner HTML of li minus the first link AND any leading ":" / whitespace */
      var clone = li.cloneNode(true);
      var cloneFirst = clone.querySelector('a');
      if (cloneFirst) cloneFirst.remove();
      var descHTML = clone.innerHTML.replace(/^[\s:]+/, '').trim();
      var cat = categoryFor(href);
      var card = document.createElement('div');
      card.className = 'cd-related-card';
      card.dataset.href = href;
      card.innerHTML =
        '<div class="cd-related-card-icon">' + cat.icon + '</div>' +
        '<div class="cd-related-card-category">' + cat.label + '</div>' +
        '<p class="cd-related-card-title">' + title + '</p>' +
        (descHTML ? '<div class="cd-related-card-desc">' + descHTML + '</div>' : '') +
        '<a class="cd-related-card-cta" href="' + href + '">Read guide ' + SVG.arrow + '</a>';
      /* whole-card click navigation (skip if a nested link was clicked) */
      card.addEventListener('click', function(e){
        if (e.target.closest('a')) return;
        if (e.target.closest('.cd-related-card-cta')) return;
        window.location.href = href;
      });
      grid.appendChild(card);
    });
    /* Wrap grid in a section + add toggle when card count exceeds threshold */
    var section = document.createElement('div');
    section.className = 'cd-related-section';
    section.appendChild(grid);
    if (grid.children.length > COLLAPSE_THRESHOLD) {
      grid.classList.add('is-collapsed');
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'cd-related-toggle';
      btn.textContent = 'Show More Guides';
      btn.addEventListener('click', function(){
        var nowCollapsed = grid.classList.toggle('is-collapsed');
        btn.textContent = nowCollapsed ? 'Show More Guides' : 'Show Fewer Guides';
      });
      section.appendChild(btn);
    }
    ul.dataset.cdRelatedTransformed = '1';
    ul.replaceWith(section);
  }
  /* Match any heading that STARTS with one of these phrases (catches
   * "Related Guides", "Further reading", "Related Guides for When ...",
   * "More Guides", etc.) */
  var HEADING_RE = /^\s*(?:Related\s+Guides|Further\s+Reading|More\s+Guides|Other\s+Guides|Related\s+Articles|Related\s+Resources|See\s+Also)\b/i;
  function transformAll(){
    var headings = document.querySelectorAll('h2, h3');
    for (var i = 0; i < headings.length; i++) {
      if (HEADING_RE.test(headings[i].textContent)) transformOne(headings[i]);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', transformAll);
  } else {
    transformAll();
  }
})();
</script>
<script id="cd-faq-showonlyone">
/* Enforce single-open FAQ: opening one panel closes any other.
 * The Ultimate Blocks plugin already supports this via data-showonlyone="true"
 * on the .wp-block-ub-content-toggle container — we flip it on at page load.
 * The plugin's togglePanel() reads this attribute and closes sibling panels. */
(function(){
  function applyShowOnlyOne(){
    var containers = document.querySelectorAll('.wp-block-ub-content-toggle');
    for (var i = 0; i < containers.length; i++) {
      containers[i].dataset.showonlyone = 'true';
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyShowOnlyOne);
  } else {
    applyShowOnlyOne();
  }
})();
</script>
<script id="cd-toc-sidebar-flag">
/* Feature flag for sticky-sidebar TOC. Setting data-toc-sidebar="on" on <html>
 * enables the behavior. Remove the attribute (or set to "off") to kill-switch
 * the feature instantly without removing any code. */
document.documentElement.setAttribute('data-toc-sidebar', 'on');
</script>
<script id="cd-sticky-nav-flag">
/* Feature flag for always-sticky topnav. The theme's existing JS toggles
 * inline style="top: -92px" on scroll-down (auto-hides the header). Our CSS
 * (in style.css) uses !important on top: 0 to beat the inline style, so the
 * header stays glued at top: 0 regardless of scroll direction.
 * Kill switch: remove this attribute (or set to "off"). */
document.documentElement.setAttribute('data-sticky-nav', 'on');
</script>
<script id="cd-reviewsio-hidden-flag">
/* Feature flag to hide the reviews.io sidebar widget site-wide.
 * Targets #block-36 (the WP Block Widget instance) and any
 * .widget containing .cd-reviewsio-widget (defensive fallback).
 * Kill switch: remove this attribute → widget reappears instantly. */
document.documentElement.setAttribute('data-reviewsio-hidden', 'on');
</script>
<script id="cd-licensed-v2-flag">
/* Feature flag for Licensed & Accredited sidebar widget v2 tweaks.
 * Forces 3 logos onto one line + restyles pill text per spec.
 * Kill switch: remove this attribute → original rendering returns. */
document.documentElement.setAttribute('data-licensed-v2', 'on');
</script>
<script id="cd-burger-rebind">
/* Burger menu robust rebind: the theme's mobile-menu JS only attaches the
 * click handler on initial load IF the viewport is mobile-sized at that
 * moment. If the user loads at desktop and resizes down, the burger has no
 * handler. We attach our own in CAPTURE phase + stopImmediatePropagation so
 * the theme's bubble-phase handler doesn't also fire (which would cause a
 * double-toggle that nets to no change). */
(function(){
  if (window.__cdBurgerBound) return;
  window.__cdBurgerBound = true;
  document.addEventListener('click', function(e){
    var btn = e.target.closest && e.target.closest('button.menu-toggle');
    if (!btn) return;
    var nav = document.querySelector('nav.main-navigation');
    if (!nav) return;
    var expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    nav.classList.toggle('toggled', !expanded);
    e.stopImmediatePropagation();
    e.preventDefault();
  }, true);

  /* Mobile sub-menu accordion: on mobile, clicking a TOP-LEVEL item that has
   * children should expand/collapse its sub-menu IN PLACE rather than follow
   * the link. We piggyback on the theme's existing .focus class (the theme's
   * own JS uses it for accordion on mobile, but only binds at mobile-load,
   * so we add ours for the resize case). */
  document.addEventListener('click', function(e){
    if (window.innerWidth >= 992) return;       /* desktop: native behaviour */
    var nav = document.querySelector('nav.main-navigation.toggled');
    if (!nav) return;
    var trigger = e.target.closest && e.target.closest('li.menu-item-has-children > a, li.menu-item-has-children > span:not(.menu-arrow)');
    if (!trigger || !nav.contains(trigger)) return;
    var li = trigger.parentElement;
    if (!li || !li.classList.contains('menu-item-has-children')) return;
    /* Only top-level (parent UL is NOT a sub-menu) */
    var parentUl = li.parentElement;
    if (!parentUl || parentUl.classList.contains('sub-menu')) return;
    li.classList.toggle('focus');
    e.stopImmediatePropagation();
    e.preventDefault();
  }, true);
})();
</script>
<script id="cd-topnav-phone-icon">
/* Inject a white phone SVG icon to the left of the header phone number text.
 * Idempotent. Only runs when topnav v2 is on. */
(function(){
  try {
    if (document.documentElement.dataset.topnavV2 !== 'on') return;
    function inject(){
      var phone = document.querySelector('header.site-header a.header-phone');
      if (!phone || phone.dataset.cdPhoneIcon === '1') return;
      var label = phone.textContent.trim();
      /* Filled phone icon (solid, white via currentColor). */
      var icon = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.487 17.14l-4.065-3.696a1 1 0 0 0-1.391.043l-2.393 2.461c-.576-.11-1.734-.471-2.926-1.66-1.192-1.193-1.553-2.354-1.66-2.926l2.459-2.394a1 1 0 0 0 .043-1.391L6.86 3.512a1 1 0 0 0-1.391-.087l-2.17 1.861a1 1 0 0 0-.291.649c-.015.25-.301 6.172 4.291 10.766C11.305 20.707 16.323 21 17.705 21c.202 0 .326-.006.359-.008a.99.99 0 0 0 .648-.291l1.86-2.171a1 1 0 0 0-.085-1.39z"/></svg>';
      phone.innerHTML =
        '<span class="header-phone__icon">' + icon + '</span>' +
        '<span class="header-phone__label">' + label + '</span>';
      phone.dataset.cdPhoneIcon = '1';
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', inject);
    } else { inject(); }
  } catch (e) {}
})();
</script>
<script id="cd-topnav-v2-flag">
/* Topnav v2 — site-wide restyle (white bg, new dark logo, #102a43 menu items,
 * BE-inspired dropdowns, sidebar-widget border bottom).
 * Kill switch: remove this data attribute → original navy topnav returns
 * (CSS rules and JS swap both no-op without the flag). */
document.documentElement.setAttribute('data-topnav-v2', 'on');
(function(){
  try {
    if (document.documentElement.dataset.topnavV2 !== 'on') return;
    function swap(){
      var logo = document.querySelector('header.site-header img.custom-logo, header.site-header a.custom-logo-link img');
      if (!logo) return;
      if (logo.dataset.cdTopnavV2Logo === '1') return;
      logo.dataset.cdTopnavV2OldSrc = logo.src;
      logo.dataset.cdTopnavV2OldSrcset = logo.getAttribute('srcset') || '';
      /* Neutralise the <picture> WebP <source> so it doesn't override our src. */
      var pic = logo.closest('picture');
      if (pic) {
        Array.prototype.forEach.call(pic.querySelectorAll('source'), function(src){
          src.dataset.cdTopnavV2OldSrcset = src.getAttribute('srcset') || '';
          src.removeAttribute('srcset');
        });
      }
      logo.src = '/wp-content/themes/company-debt-webpigment/assets/images/cd-logo-topnav-v3.png';
      logo.removeAttribute('srcset');
      logo.dataset.cdTopnavV2Logo = '1';
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', swap);
    } else { swap(); }
  } catch (e) {}
})();
</script>
<script id="cd-stressed-cta-icon">
/* Inject a download icon before the "Download the Guide" label in the
 * Stressed Directors widget CTA. Idempotent; safe to run twice. */
(function(){
  try {
    function inject(){
      var btn = document.querySelector('.widget-download-button');
      if (!btn) return;
      if (btn.dataset.cdCtaIcon === '1') return;
      var icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>';
      var label = btn.textContent.trim();
      btn.innerHTML =
        '<span class="widget-download-button__label">' + label + '</span>' +
        '<span class="widget-download-button__icon">' + icon + '</span>';
      btn.dataset.cdCtaIcon = '1';
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', inject);
    } else { inject(); }
  } catch (e) {}
})();
</script>
<script id="cd-stressed-subtext-icons">
/* Replace ".widget-download-subtext" text "100% Free · Regularly Updated"
 * with a two-item layout: icon + label each, no dot separator.
 * Matches the Insolvency Test trust row pattern. */
(function(){
  try {
    function rewrite(){
      var el = document.querySelector('.widget-download-subtext');
      if (!el) return;
      if (el.dataset.cdSubtextV2 === '1') return;
      var icoGift = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>';
      var icoRefresh = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>';
      el.innerHTML =
        '<span class="widget-download-subtext__item"><span class="widget-download-subtext__icon">' + icoGift + '</span>100% free</span>' +
        '<span class="widget-download-subtext__item"><span class="widget-download-subtext__icon">' + icoRefresh + '</span>Regularly updated</span>';
      el.dataset.cdSubtextV2 = '1';
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', rewrite);
    } else { rewrite(); }
  } catch (e) {}
})();
</script>
<script id="cd-insolvency-widget-v2">
/* Free Insolvency Test sidebar widget — v2 redesign.
 * Rewrites the inner HTML of #block-20 to the new layout (eyebrow pill,
 * headline, subhead, 3 benefits, phone mockup, CTA, trust row).
 * Old DOM/CSS untouched — kill switch (remove data-insolvency-v2) restores
 * the original v1 widget instantly. */
document.documentElement.setAttribute('data-insolvency-v2', 'on');
(function(){
  try {
    if (document.documentElement.dataset.insolvencyV2 !== 'on') return;
    function render(){
      var w = document.getElementById('block-20');
      if (!w) return;
      if (w.dataset.cdItestV2 === '1') return;
      /* Preserve original CTA href if present, else fall back. */
      var oldA = w.querySelector('a[href]');
      var href = oldA ? oldA.getAttribute('href') : '/insolvency-calculator/';
      /* SVG icons inline for crisp rendering and no extra requests. */
      var icoBolt = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2L4.5 13.5h6L10 22l8.5-11.5h-6L13 2z"/></svg>';
      var icoCheck = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="5 12 10 17 19 7"/></svg>';
      var icoLock = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>';
      var icoBoltLine = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="13 2 4 14 11 14 11 22 20 10 13 10 13 2"/></svg>';
      var icoShield = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z"/><polyline points="9 12 11 14 15 10"/></svg>';
      var icoArrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="13 6 19 12 13 18"/></svg>';
      function benefit(title, sub){
        return '<li><span class="cd-itest__check">' + icoCheck + '</span><span class="cd-itest__benefit-body"><span class="cd-itest__benefit-title">' + title + '</span><span class="cd-itest__benefit-sub">' + sub + '</span></span></li>';
      }
      function trust(icon, text){
        return '<li><span class="cd-itest__trust-icon">' + icon + '</span>' + text + '</li>';
      }
      w.innerHTML =
        '<div class="cd-itest">' +
          '<div class="cd-itest__eyebrow">30-SECOND TEST</div>' +
          '<h3 class="cd-itest__headline">Is Your Company Insolvent?</h3>' +
          '<p class="cd-itest__subhead">Answer 5 quick questions and get an instant assessment.</p>' +
          '<div class="cd-itest__mockup" role="img" aria-label="Insolvency test preview"></div>' +
          '<ul class="cd-itest__benefits">' +
            benefit('Instant assessment', 'See your result immediately') +
            benefit('Recommended next steps', 'Clear guidance tailored to you') +
            benefit('Free expert guidance', 'Speak to our specialists') +
          '</ul>' +
          '<a class="cd-itest__cta" href="' + href + '"><span>Start the 30-Second Test</span><span class="cd-itest__cta-arrow">' + icoArrow + '</span></a>' +
          '<ul class="cd-itest__trust">' +
            trust(icoLock, 'No signup required') +
            trust(icoShield, '100% confidential') +
          '</ul>' +
        '</div>';
      w.dataset.cdItestV2 = '1';
      /* Reveal the sidebar now that the v2 widget is in place.
       * Companion CSS hides .widget-area until this class is present, so all
       * widgets appear in their final order on a single paint — no flash. */
      var wa = w.closest('.widget-area');
      if (wa) wa.classList.add('cd-sidebar-ready');
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', render);
    } else { render(); }
  } catch (e) {}
})();
</script>
<script id="cd-toc-sidebar-move">
/* Move the auto-TOC from the article body into the sidebar's last position
 * on take-the-test template pages, on desktop only (>=992px).
 * Stays in body on mobile/tablet (sidebar collapses below content there).
 * Wrapped in <div class="widget widget--cd-toc"> so existing widget styling +
 * spacing applies naturally. */
(function(){
  try {
    if (document.documentElement.dataset.tocSidebar !== 'on') return;
    /* Gate on the shared design-system class. Originally this checked for
     * `page-template-take-the-test-template` only — that class is now
     * supplemented by `cd-ttt-design` (emitted by functions.php for both
     * take-the-test page-template pages AND single posts on the default
     * post template) so the TOC moves into the sidebar on /articles/ too. */
    if (!document.body.classList.contains('cd-ttt-design')) return;
    if (!window.matchMedia('(min-width: 992px)').matches) return;
    function move(){
      var toc = document.querySelector('.col-8 > .toc, .main-content > .toc');
      var widgetArea = document.querySelector('.col-4 .widget-area, aside.widget-area');
      if (!toc || !widgetArea) return;
      if (toc.dataset.cdTocMoved === '1') return;
      var col4 = widgetArea.parentElement;
      var wrap = document.createElement('div');
      wrap.className = 'widget widget--cd-toc';
      wrap.appendChild(toc);
      /* Append as sibling of widget-area, NOT inside it — gives the TOC col-4
       * as its sticky context (full article-body height) instead of just the
       * widget-area's small natural height. */
      col4.appendChild(wrap);
      /* Replace "Contents" with "IN THIS ARTICLE" */
      var pill = toc.querySelector('.toc__pill');
      if (pill) pill.textContent = 'IN THIS ARTICLE';
      toc.dataset.cdTocMoved = '1';
      /* Scroll-spy: marks the most-recently-scrolled-past heading as .is-active.
       * Throttled with requestAnimationFrame for smooth performance. */
      try {
        var links = Array.from(toc.querySelectorAll('a[href^="#"]'));
        var pairs = links.map(function(a){
          var id = (a.getAttribute('href') || '').slice(1);
          var target = id && document.getElementById(id);
          return target ? { link: a, target: target } : null;
        }).filter(Boolean);
        if (pairs.length) {
          var current = null;
          function setActive(link){
            if (link === current) return;
            if (current) current.classList.remove('is-active');
            if (link) link.classList.add('is-active');
            current = link;
          }
          var THRESHOLD = 120; /* px from top of viewport — the "reading line" */
          function updateActive(){
            var found = null;
            for (var i = 0; i < pairs.length; i++) {
              var top = pairs[i].target.getBoundingClientRect().top;
              if (top - THRESHOLD <= 0) found = pairs[i].link; else break;
            }
            /* Default to first item when nothing has been scrolled past yet
             * (page top → above the first heading). Keeps a TOC item always
             * active so the highlight strip never disappears. */
            if (!found && pairs.length > 0) found = pairs[0].link;
            setActive(found);
          }
          var ticking = false;
          function onScroll(){
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(function(){ updateActive(); ticking = false; });
          }
          window.addEventListener('scroll', onScroll, { passive: true });
          window.addEventListener('resize', onScroll);
          updateActive();
        }
      } catch(e) { /* no-op */ }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', move);
    } else {
      move();
    }
  } catch (e) {
    /* swallow — leaving TOC in body is a safe fallback */
  }
})();
</script>
<script id="cd-callout-summary-cards">
/* Transform every .cd-callout--summary into a grid of cards.
 * Source markup:
 *   <aside class="cd-callout cd-callout--summary">
 *     <p class="cd-callout__label"><strong>Heading at a Glance</strong></p>
 *     <p><strong>Meaning:</strong> ...</p>
 *     <p><strong>Used when:</strong> ...</p>
 *     ...
 *   </aside>
 * Each non-label <p> becomes a card with: icon (above) + title + body. */
(function(){
  var SVG = {
    book:     '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    calendar: '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    user:     '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    shield:   '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    pound:    '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 6.5a4 4 0 0 0-7 3v2H7M7 12h8M7 18h11"/><path d="M10 18c1.5 0 3-1.2 3-3v-2"/></svg>',
    alert:    '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    clock:    '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    lifebuoy: '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="4.93" y1="4.93" x2="9.17" y2="9.17"/><line x1="14.83" y1="14.83" x2="19.07" y2="19.07"/><line x1="14.83" y1="9.17" x2="19.07" y2="4.93"/><line x1="4.93" y1="19.07" x2="9.17" y2="14.83"/></svg>',
    info:     '<svg class="cd-callout-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
  };
  function pickIcon(title){
    var t = (title || '').toLowerCase();
    if (/\bmean(ing)?\b|what\s+it\s+is\b|^default\b/.test(t)) return SVG.book;
    if (/used\s+when|trigger|when\s+to|when\b/.test(t)) return SVG.calendar;
    if (/who\s+runs?|who\s+calls?|who\s+handles?/.test(t)) return SVG.user;
    if (/director\s+priority|priority/.test(t)) return SVG.shield;
    if (/cost\b|tax\s+cost|insolvency\s+cost/.test(t)) return SVG.pound;
    if (/risk|warning|bank[\s-]?freeze/.test(t)) return SVG.alert;
    if (/time|duration|how\s+long/.test(t)) return SVG.clock;
    if (/recovery|rescue|survives/.test(t)) return SVG.lifebuoy;
    return SVG.info;
  }
  function transformSummary(callout){
    if (callout.dataset.cdSummaryTransformed === '1') return;
    var label = callout.querySelector(':scope > .cd-callout__label');
    var bodyPs = Array.from(callout.querySelectorAll(':scope > p:not(.cd-callout__label)'));
    if (!bodyPs.length) return;
    var grid = document.createElement('div');
    grid.className = 'cd-callout__grid';
    bodyPs.forEach(function(p){
      var strong = p.querySelector('strong');
      if (!strong) return;
      var titleText = strong.textContent.replace(/[:  ]\s*$/, '').trim();
      /* Body = innerHTML of p minus the first <strong> */
      var clone = p.cloneNode(true);
      var cloneStrong = clone.querySelector('strong');
      if (cloneStrong) cloneStrong.remove();
      var bodyHTML = clone.innerHTML.replace(/^[\s:  ]+/, '').trim();
      var card = document.createElement('div');
      card.className = 'cd-callout__card';
      card.innerHTML =
        '<div class="cd-callout__card-icon">' + pickIcon(titleText) + '</div>' +
        '<p class="cd-callout__card-title">' + titleText + '</p>' +
        '<p class="cd-callout__card-body">' + bodyHTML + '</p>';
      grid.appendChild(card);
    });
    callout.appendChild(grid);
    callout.dataset.cdSummaryTransformed = '1';
  }
  function init(){
    document.querySelectorAll('.cd-callout--summary').forEach(transformSummary);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
<script id="cd-table-tag-article-tables">
/* Auto-apply .cd-table class to every <table> inside the article body (.col-8 or
 * .main-content). This widens the styling to bare HTML tables + Gutenberg
 * wp-block-table variants without touching tables in chrome (footer, sidebar,
 * plugins). Must run BEFORE the other table scripts that scan for .cd-table. */
(function(){
  function tag(){
    document.querySelectorAll('.col-8 table, .main-content table').forEach(function(t){
      t.classList.add('cd-table');
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tag);
  } else {
    tag();
  }
})();
</script>
<script id="cd-table-link-cells">
/* Detect cells in .cd-table where the ONLY content is a single link.
 * For those, apply class .cd-table-link-cell and inject a right-arrow SVG
 * inside the link. CSS handles the bold + no-underline + arrow placement.
 * Cells with a link embedded in other text are LEFT ALONE. */
(function(){
  var ARROW = '<svg class="cd-table-arrow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';
  function transformCell(cell){
    var links = cell.querySelectorAll('a');
    if (links.length !== 1) return;       /* zero or multiple links — leave alone */
    var link = links[0];
    var cellText = (cell.textContent || '').replace(/\s+/g, ' ').trim();
    var linkText = (link.textContent || '').replace(/\s+/g, ' ').trim();
    if (!cellText || cellText !== linkText) return;  /* link mixed with other text */
    cell.classList.add('cd-table-link-cell');
    if (!link.querySelector('.cd-table-arrow')) {
      link.insertAdjacentHTML('beforeend', ARROW);
    }
  }
  function init(){
    document.querySelectorAll('.cd-table td, .cd-table th').forEach(transformCell);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
<script id="cd-table-header-titlecase">
/* For every .cd-table, smart-title-case the header row (first row).
 * Rule: capitalize the first letter of words >3 letters; leave shorter
 * words alone (e.g., "in", "of", "the", "and" stay lowercase). Uses a
 * TreeWalker over text nodes so any inline HTML inside the cell stays intact. */
(function(){
  function smartTitleCase(text){
    return text.replace(/\b([a-zA-Z']+)\b/g, function(word){
      if (word.length <= 3) return word;
      return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    });
  }
  function transformTable(table){
    var headerCells;
    if (table.querySelector('thead')) {
      headerCells = table.querySelectorAll('thead > tr:first-child > th, thead > tr:first-child > td');
    } else {
      headerCells = table.querySelectorAll('tbody > tr:first-child > th, tbody > tr:first-child > td');
    }
    headerCells.forEach(function(cell){
      var walker = document.createTreeWalker(cell, NodeFilter.SHOW_TEXT, null, false);
      var node;
      while ((node = walker.nextNode())) {
        if (node.textContent.trim()) {
          node.textContent = smartTitleCase(node.textContent);
        }
      }
    });
  }
  function init(){
    document.querySelectorAll('.cd-table').forEach(transformTable);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
<script id="cd-faq-strip-numbering">
/* Strip leading numbering from FAQ question titles sitewide.
 * Some legacy pages have "1) Question…" or "1. Question…" — we normalize by
 * removing the "N)" or "N. " prefix at page load. The space after the
 * punctuation is required so a question like "1.5x what?" or a question that
 * legitimately starts with a number stays intact. */
(function(){
  var STRIP_RE = /^\s*\d+[\)\.]\s+/;
  function stripAll(){
    var titles = document.querySelectorAll('.wp-block-ub-content-toggle-accordion-title');
    for (var i = 0; i < titles.length; i++) {
      /* Question text is typically wrapped in <strong>; if not, fall back to the <p>. */
      var target = titles[i].querySelector('strong') || titles[i];
      var orig = target.textContent;
      var next = orig.replace(STRIP_RE, '');
      if (next !== orig) target.textContent = next;
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', stripAll);
  } else {
    stripAll();
  }
})();
</script>
<script id="cd-faq-icons">
/* Inject a topic-relevant icon at the start of every FAQ accordion question.
 * The icon is wrapped in a white circle with a hairline border; CSS in style.css
 * handles the dark-blue default colour and the orange (#ff6600) flip when open.
 * Keyword-matching picks from a small SVG library; default = help/question icon. */
(function(){
  var I = {
    /* feather-style strokes, 24x24 viewBox, stroke=currentColor */
    scales:   '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M4 21h16M6 6h12"/><path d="M7 6l-3 7a4 4 0 0 0 6 0L7 6zM17 6l-3 7a4 4 0 0 0 6 0l-3-7z"/></svg>',
    clock:    '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    pound:    '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 6.5a4 4 0 0 0-7 3v2H7M7 12h8M7 18h11"/><path d="M10 18c1.5 0 3-1.2 3-3v-2"/></svg>',
    user:     '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    shield:   '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    doc:      '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/></svg>',
    refresh:  '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
    help:     '<svg class="cd-faq-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
  };
  /* Match rules: first match wins. Order is precedence — narrower topics first. */
  var RULES = [
    { re: /\b(how\s+long|how\s+many\s+(years|months|days|weeks)|duration|takes?\s+to|when)\b/i, icon: I.clock },
    { re: /\b(cost|costs?|pay|paying|fee|fees|money|afford|expensive|cheap|charge|price|funded)\b/i, icon: I.pound },
    { re: /\b(director|directors|disqualif|personally\s+liable|personal\s+liab|guarantee)\b/i, icon: I.user },
    { re: /\b(challenge|risk|automatic|reverse|claw[\s-]?back|wrongful|fraudulent|misfeasance)\b/i, icon: I.shield },
    { re: /\b(another\s+company|start\s+(?:another|again)|new\s+company|phoenix|re[\s-]?use|same\s+name)\b/i, icon: I.refresh },
    { re: /\b(liquidator|liquidation|winding\s+up|dissolut|cvl|mvl|insolvency\s+practitioner|court)\b/i, icon: I.scales },
    { re: /\b(form|forms|document|paperwork|filing|file|register|register\b|process)\b/i, icon: I.doc },
  ];
  function pickIcon(text){
    for (var i = 0; i < RULES.length; i++) {
      if (RULES[i].re.test(text)) return RULES[i].icon;
    }
    return I.help;
  }
  function injectIcons(){
    var titles = document.querySelectorAll('.wp-block-ub-content-toggle .wp-block-ub-content-toggle-accordion-title');
    for (var i = 0; i < titles.length; i++) {
      var t = titles[i];
      if (t.querySelector('.cd-faq-icon-wrap')) continue; /* already injected */
      var wrap = document.createElement('span');
      wrap.className = 'cd-faq-icon-wrap';
      wrap.setAttribute('aria-hidden', 'true');
      wrap.innerHTML = pickIcon(t.textContent || '');
      t.insertBefore(wrap, t.firstChild);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectIcons);
  } else {
    injectIcons();
  }
})();
</script>
<script id="cd-faq-heading-rewrite">
/* Normalize EVERY FAQ section heading sitewide to the canonical form:
 *   "FAQs About [topic]"
 * Handles all observed variants across the corpus (245 pages):
 *   - "Frequently Asked Questions About X"            → "FAQs About X"
 *   - "Frequently Asked Questions on/in/for X"        → "FAQs About X"
 *   - "Frequently Asked Questions [trailing words]"   → "FAQs About [words]"
 *   - "FAQs on/in/for/regarding X"                    → "FAQs About X"
 *   - "FAQs: X"                                        → "FAQs About X"
 *   - "X FAQs" (suffix)                                → "FAQs About X"
 *   - "FAQs" alone                                     → "FAQs About [H1 text]"
 *   - "Frequently Asked Questions" alone               → "FAQs About [H1 text]"
 * Only fires on H2/H3 — leaves any heading without an FAQ marker untouched. */
(function(){
  function rewriteHeadingText(s){
    s = (s || '').replace(/\s+/g, ' ').trim();
    if (!s) return null;
    /* Already canonical */
    if (/^FAQs\s+About\s+/i.test(s)) return null;
    /* Standalone variants — pull topic from H1 */
    if (/^(?:Frequently\s+Asked\s+Questions|FAQs?)\s*$/i.test(s)) {
      var h1 = document.querySelector('h1');
      var topic = h1 ? h1.textContent.replace(/\s+/g, ' ').trim() : '';
      return topic ? ('FAQs About ' + topic) : 'FAQs';
    }
    /* Extract topic, most-specific patterns first */
    var patterns = [
      /^Frequently\s+Asked\s+Questions\s+About\s+(.+)$/i,
      /^Frequently\s+Asked\s+Questions\s+(?:on|in|for|regarding)\s+(.+)$/i,
      /^Frequently\s+Asked\s+Questions\s*:\s*(.+)$/i,
      /^Frequently\s+Asked\s+Questions\s+(.+)$/i,
      /^FAQs?\s+(?:on|in|for|regarding)\s+(.+)$/i,
      /^FAQs?\s*:\s*(.+)$/i,
      /^(.+?)\s+FAQs?\s*$/i,             /* X FAQs (suffix) */
      /^FAQs?\s+(.+)$/i,                  /* FAQs [anything else] — only after specifics */
    ];
    for (var i = 0; i < patterns.length; i++) {
      var m = s.match(patterns[i]);
      if (m && m[1]) {
        var topic = m[1].trim().replace(/^About\s+/i, '');
        return 'FAQs About ' + topic;
      }
    }
    return null;
  }
  function rewriteAll(){
    var headings = document.querySelectorAll('h2, h3');
    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      /* Only touch headings that mention FAQ-related words */
      if (!/\b(FAQ|Frequently\s+Asked)/i.test(h.textContent)) continue;
      var next = rewriteHeadingText(h.textContent);
      if (next && next !== h.textContent.trim()) h.textContent = next;
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', rewriteAll);
  } else {
    rewriteAll();
  }
})();
</script>
<div id="back-to-top">
    <span class="back-top-top-btn">
        <img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/white_arrow_up.svg' ); ?>" alt="Up">
    </span>
</div>
</body>
</html>
