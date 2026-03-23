"""Shared JavaScript for credit card page interactivity."""

# ── TOC sidebar: auto-populates from H2s, scroll-spy highlights current ──

CC_TOC_HTML = '''<nav class="cc-toc" id="cc-toc" aria-label="Table of contents">
  <ul class="cc-toc__list" id="cc-toc-list"></ul>
</nav>'''

# Invisible anchor — assemblers place this where the TOC should align with
CC_TOC_START = '<div id="cc-toc-start" aria-hidden="true"></div>'


CC_TOC_JS = '''<script>
(function() {
  var toc = document.getElementById('cc-toc');
  var list = document.getElementById('cc-toc-list');
  if (!toc || !list) return;

  // Gather all H2s, filter out low-value sections, cap at 6
  var container = document.querySelector('.entry-content') || document.body;
  var h2s = container.querySelectorAll('h2.wp-block-heading');
  if (h2s.length < 2) { toc.style.display = 'none'; return; }

  // Sections to exclude from the TOC (case-insensitive partial match)
  var exclude = ['faq', 'frequently asked', 'methodology', 'sources and method',
    'editorial policy', 'related reading', 'further reading', 'about the author',
    'disclaimer', 'also listed', 'also worth considering'];
  var maxItems = 6;

  // Generate IDs and build TOC links
  var sections = [];
  var count = 0;
  h2s.forEach(function(h2, i) {
    if (count >= maxItems) return;
    var text = h2.textContent.trim().toLowerCase();
    for (var e = 0; e < exclude.length; e++) {
      if (text.indexOf(exclude[e]) !== -1) return;
    }
    var id = h2.id || 'section-' + i;
    h2.id = id;
    sections.push({ id: id, el: h2 });

    var li = document.createElement('li');
    li.className = 'cc-toc__item';
    var a = document.createElement('a');
    a.className = 'cc-toc__link';
    a.href = '#' + id;
    a.textContent = h2.textContent.trim();
    a.addEventListener('click', function(e) {
      e.preventDefault();
      h2.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', '#' + id);
    });
    li.appendChild(a);
    list.appendChild(li);
    count++;
  });

  // TOC start anchor — TOC vertical position aligns with this marker
  var tocStart = document.getElementById('cc-toc-start');
  var minTop = 50; // fixed position once scrolled past anchor (clears WP admin bar)

  // Position TOC horizontally relative to the content area
  function positionToc() {
    var entry = document.querySelector('.entry-content.container');
    if (!entry) return;
    var rect = entry.getBoundingClientRect();
    var left = rect.left - 260;
    if (left < 16) { toc.style.display = 'none'; return; }
    toc.style.left = left + 'px';
    toc.style.display = '';
  }

  // Vertical position: align with toc-start anchor, then lock at minTop
  function updateTop() {
    if (!tocStart) {
      toc.style.top = minTop + 'px';
      return;
    }
    var anchorTop = tocStart.getBoundingClientRect().top;
    // Use whichever is larger: the anchor position or the minimum fixed position
    toc.style.top = Math.max(anchorTop, minTop) + 'px';
  }

  // Scroll spy: highlight current section
  var links = list.querySelectorAll('.cc-toc__link');
  var rafId = null;
  function onScroll() {
    if (rafId) return;
    rafId = requestAnimationFrame(function() {
      rafId = null;
      updateTop();

      var current = -1;
      for (var i = sections.length - 1; i >= 0; i--) {
        if (sections[i].el.getBoundingClientRect().top <= 120) {
          current = i;
          break;
        }
      }
      links.forEach(function(link, idx) {
        if (idx === current) {
          link.classList.add('cc-toc__link--active');
        } else {
          link.classList.remove('cc-toc__link--active');
        }
      });
    });
  }

  positionToc();
  updateTop();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', positionToc);
  onScroll();
})();
</script>'''


# ── Comparison table: expand/collapse detail rows ──

CC_COMPARISON_TABLE_JS = '''<script>
(function() {
  document.querySelectorAll('.cc-ct__detail-toggle').forEach(function(btn) {
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function() {
      var rowId = btn.getAttribute('data-detail');
      var row = document.getElementById(rowId);
      if (!row) return;
      var open = row.classList.toggle('cc-ct--open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Less detail ▲' : 'More detail ▼';
    });
  });
})();
</script>'''


# ── Tabbed card: switch tab content within product cards ──

CC_TABBED_CARD_JS = '''<script>
(function() {
  document.querySelectorAll('.cc-tab-card__tabs').forEach(function(tabRow) {
    var card = tabRow.closest('.cc-tab-card');
    if (!card) return;
    var tabs = Array.prototype.slice.call(tabRow.querySelectorAll('.cc-tab-card__tab'));
    var panels = card.querySelectorAll('.cc-tab-card__panel');

    function activateTab(tab) {
      var target = tab.getAttribute('data-tab');

      tabs.forEach(function(t) {
        t.classList.remove('cc-tab-card__tab--active');
        t.setAttribute('aria-selected', 'false');
        t.setAttribute('tabindex', '-1');
      });
      tab.classList.add('cc-tab-card__tab--active');
      tab.setAttribute('aria-selected', 'true');
      tab.setAttribute('tabindex', '0');
      tab.focus();

      panels.forEach(function(p) {
        if (p.id === target) {
          p.classList.add('cc-tab-card__panel--active');
          p.removeAttribute('aria-hidden');
        } else {
          p.classList.remove('cc-tab-card__panel--active');
          p.setAttribute('aria-hidden', 'true');
        }
      });
    }

    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() { activateTab(tab); });
    });

    tabRow.addEventListener('keydown', function(e) {
      var idx = tabs.indexOf(document.activeElement);
      if (idx === -1) return;
      var next = -1;
      if (e.key === 'ArrowRight') {
        next = (idx + 1) % tabs.length;
      } else if (e.key === 'ArrowLeft') {
        next = (idx - 1 + tabs.length) % tabs.length;
      } else if (e.key === 'Home') {
        next = 0;
      } else if (e.key === 'End') {
        next = tabs.length - 1;
      }
      if (next !== -1) {
        e.preventDefault();
        activateTab(tabs[next]);
      }
    });
  });
})();
</script>'''


# ── Hero metadata strip rebuild JS ─────────────────────────────────────
# Replaces the WP theme's split author/date layout with a unified inline
# metadata strip: avatar · author · divider · clock+readtime · date.
# Also repositions the affiliate disclosure badge next to the H1.

CC_HERO_META_JS = (
    'var rt=document.querySelector(".time-section .read-time");'
    'var authorMeta=document.querySelector(".author-meta");'
    'var authorName=authorMeta?authorMeta.querySelector("a"):null;'
    'var dateEl=document.querySelector(".article-date");'
    'var avatar=document.querySelector(".author-box .avatar-image");'
    'var nameText=authorName?authorName.textContent.trim():"";'
    'var rtText=rt?rt.textContent.trim():"";'
    'var dateText=dateEl?dateEl.textContent.trim():"";'
    'var metaRow=document.querySelector(".hero-section .col-12.d-flex");'
    'if(metaRow&&nameText){'
    'var strip=document.createElement("div");'
    'strip.className="cc-meta-strip";'
    'if(avatar){var av=avatar.cloneNode(true);av.className="cc-meta-avatar";strip.appendChild(av);}'
    'var auth=document.createElement("span");'
    'auth.className="cc-meta-author";'
    'var authLabel=document.createElement("span");authLabel.className="cc-meta-label";authLabel.textContent="Author";'
    'auth.appendChild(authLabel);auth.appendChild(document.createTextNode(" "+nameText));'
    'strip.appendChild(auth);'
    'var d1=document.createElement("span");d1.className="cc-meta-divider";strip.appendChild(d1);'
    'var rtSpan=document.createElement("span");'
    'rtSpan.className="cc-readtime-inline";'
    'rtSpan.innerHTML=\'<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
    'viewBox="0 0 20 20" fill="none" class="cc-readtime-icon"><path d="M10 4.5V10H14M10 '
    '17.5C5.85786 17.5 2.5 14.1421 2.5 10C2.5 5.85786 5.85786 2.5 10 2.5C14.1421 2.5 '
    '17.5 5.85786 17.5 10C17.5 14.1421 14.1421 17.5 10 17.5Z" stroke="currentColor" '
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>\';'
    'if(rtText){var rtTxt=document.createElement("span");rtTxt.textContent=rtText;rtSpan.appendChild(rtTxt);}'
    'strip.appendChild(rtSpan);'
    'if(dateText){'
    'var pub=document.createElement("span");'
    'pub.className="cc-meta-date";'
    'pub.textContent=dateText;'
    'strip.appendChild(pub);'
    '}'
    'while(metaRow.firstChild){metaRow.removeChild(metaRow.firstChild);}'
    'metaRow.appendChild(strip);'
    'var parentRow=metaRow.closest(".row");'
    'if(parentRow&&getComputedStyle(parentRow).display==="none"){'
    'parentRow.style.setProperty("display","flex","important");'
    'parentRow.style.setProperty("flex-wrap","wrap","important");'
    '}'
    '}'
    'var disc=document.querySelector(".ad-disclaimer-tooltip");'
    'var headingRow=document.querySelector(".hero-section .heading");'
    'if(disc&&headingRow){'
    'var headingParent=headingRow.closest(".row");'
    'if(headingParent){'
    'var wrapper=document.createElement("div");'
    'wrapper.className="cc-disclosure-aligned";'
    'wrapper.appendChild(disc);'
    'headingParent.appendChild(wrapper);'
    '}'
    '}'
)
