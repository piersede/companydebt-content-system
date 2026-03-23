#!/usr/bin/env python3
"""Build Gutenberg blocks for Low APR Business Credit Cards page.

v3: Uses redesigned cc-card component with facts grid, decision blocks,
and purple-derived colour palette.
"""

import json
import os
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Card data ──────────────────────────────────────────────────────────

CARDS = [
    {
        'bank': 'Lloyds',
        'name': 'Lloyds Bank Business Credit Card',
        'img_url': 'https://busexp1stg.wpengine.com/wp-content/uploads/2026/03/LLOYDS-credit-card-image.png',
        'img_alt': 'Lloyds Business Credit Card',
        'fit_label': 'Lowest APR on this list',
        'summary_strip': '15.95% APR &middot; 14.9% purchase rate &middot; &pound;32 fee waived yr 1 and at &pound;6k+ spend',
        'verdict': 'The lowest representative APR available, but the annual fee means it only pays off with consistent spend above the waiver threshold.',
        'editorial_heading': 'Lowest headline rate, but the fee waiver threshold decides whether it actually saves you money',
        'facts': [
            ('Representative APR', '15.95% variable', 'apr', None),
            ('Purchase Rate', '14.9% p.a. variable', None, None),
            ('Annual Fee', '&pound;32 per cardholder', None, 'Waived yr 1; waived at &pound;6k+ annual spend'),
            ('Existing Account', 'Lloyds BCA required', 'required', None),
        ],
        'best_for': 'Existing Lloyds customers who carry a balance and can hit &pound;6k annual spend to waive the fee',
        'watch_out': '&pound;32 annual fee per card is not waived unless you spend enough &mdash; at low volumes, Metro Bank&rsquo;s 18.9% with no fee costs less overall',
        'not_ideal': 'You bank elsewhere and would need to switch to Lloyds just for the card rate',
        'eligibility': 'Sole traders, partnerships, and company directors. Lloyds BCA required. Credit limits up to &pound;25,000.',
        'cta_url': 'https://www.lloydsbank.com/business/business-cards/business-credit-card.html',
        'cta_label': 'View Lloyds Card Details',
        'verify_source': 'lloydsbank.com',
    },
    {
        'bank': 'Metro Bank',
        'name': 'Metro Bank Business Credit Card',
        'img_url': 'https://busexp1stg.wpengine.com/wp-content/uploads/2024/12/metro-bank.png',
        'img_alt': 'Metro Bank logo',
        'fit_label': 'Cheapest if you won&rsquo;t hit the Lloyds fee waiver',
        'summary_strip': '18.9% APR &middot; No annual fee &middot; In-branch application only',
        'verdict': 'No annual fee at all. If your spend is too low to waive the Lloyds or NatWest fee, this is the cheaper card.',
        'editorial_heading': 'The simplest cost structure, but the branch-only application is a real barrier',
        'facts': [
            ('Representative APR', '18.9% variable', 'apr', None),
            ('Purchase Rate', '18.9% p.a. variable', None, None),
            ('Annual Fee', '&pound;0', None, 'No fee, no waiver threshold'),
            ('Existing Account', 'Metro Bank BCA required', 'required', None),
        ],
        'best_for': 'Low-spend businesses that carry a balance &mdash; no fee means APR is your only cost',
        'watch_out': 'In-branch application only. You cannot apply online, and Metro Bank&rsquo;s branch network is London-centric.',
        'not_ideal': 'Your business isn&rsquo;t near a Metro Bank branch, or you need to apply quickly',
        'eligibility': 'Sole traders and limited companies. Metro Bank BCA required. Must apply in branch.',
        'cta_url': 'https://www.metrobankonline.co.uk/business/borrowing/products/credit-card/',
        'cta_label': 'View Metro Bank Card Details',
        'verify_source': 'metrobankonline.co.uk',
    },
    {
        'bank': 'HSBC',
        'name': 'HSBC Business Credit Card',
        'img_url': 'https://busexp1stg.wpengine.com/wp-content/uploads/2023/08/HSBC-Commercial.png',
        'img_alt': 'HSBC logo',
        'fit_label': 'Worth considering if you already bank with HSBC',
        'summary_strip': '22% APR &middot; 15.9% purchase rate &middot; &pound;32 fee waived year 1',
        'verdict': 'Competitive purchase rate at 15.9%, but the annual fee pushes the representative APR to 22%. Not worth switching banks for.',
        'editorial_heading': 'Low purchase rate for existing HSBC customers, but the fee sticks after year one',
        'facts': [
            ('Representative APR', '22% variable', 'apr', None),
            ('Purchase Rate', '15.9% p.a. variable', None, None),
            ('Annual Fee', '&pound;32 per card', None, 'Waived in year 1'),
            ('Existing Account', 'HSBC BCA required', 'required', None),
        ],
        'best_for': 'Existing HSBC business customers who want a low purchase rate without switching banks',
        'watch_out': 'The &pound;32 fee is not waivable after year 1 regardless of spend. FX fee is 2.99%.',
        'not_ideal': 'You don&rsquo;t already have an HSBC business account &mdash; the rate doesn&rsquo;t justify switching',
        'eligibility': 'HSBC business current account required. Credit limits from &pound;500.',
        'cta_url': 'https://www.business.hsbc.uk/en-gb/products/business-credit-card',
        'cta_label': 'View HSBC Card Details',
        'verify_source': 'business.hsbc.uk',
    },
    {
        'bank': 'Santander',
        'name': 'Santander Business Cashback Credit Card',
        'img_url': 'https://busexp1stg.wpengine.com/wp-content/uploads/2024/12/santander.png',
        'img_alt': 'Santander logo',
        'fit_label': 'Best fee structure for multi-cardholder teams',
        'summary_strip': '23.7% APR &middot; 18.9% purchase rate &middot; &pound;30 flat fee covers all cardholders',
        'verdict': 'Single &pound;30 fee covers all cardholders. If you&rsquo;re issuing cards to 3&ndash;4 employees, the per-account fee structure changes the total cost calculation entirely.',
        'editorial_heading': 'The fee structure advantage is real if you need multiple cards, but the APR is mid-table',
        'facts': [
            ('Representative APR', '23.7% variable', 'apr', None),
            ('Purchase Rate', '18.9% p.a. variable', None, None),
            ('Annual Fee', '&pound;30 per account', None, 'Single fee covers all cardholders'),
            ('Existing Account', 'Santander BCA required', 'required', None),
        ],
        'best_for': 'Teams issuing 3+ employee cards &mdash; the flat &pound;30 fee is materially cheaper than per-card pricing',
        'watch_out': 'Restricted to Santander 1|2|3 BCA holders. Personal guarantees required for LTDs and LLPs.',
        'not_ideal': 'You only need one card and don&rsquo;t benefit from the per-account fee structure',
        'eligibility': 'Santander 1|2|3 or Business Current Account required. Max 2 directors/partners who fully own the business. Credit limits &pound;500&ndash;&pound;25,000.',
        'cta_url': 'https://www.santander.co.uk/business/credit-cards',
        'cta_label': 'View Santander Card Details',
        'verify_source': 'santander.co.uk',
    },
    {
        'bank': 'NatWest',
        'name': 'NatWest Business Credit Card',
        'img_url': 'https://busexp1stg.wpengine.com/wp-content/uploads/2023/08/NatWest-Large.png',
        'img_alt': 'NatWest logo',
        'fit_label': 'Best for overseas card spend',
        'summary_strip': '24.3% APR &middot; 16.9% purchase rate &middot; &pound;30 fee waived at &pound;6k+ spend',
        'verdict': 'Low purchase rate, but total cost rises quickly if you need multiple employee cards.',
        'editorial_heading': 'The FX fee advantage is genuine, but the per-cardholder fee stacks up with team size',
        'facts': [
            ('Representative APR', '24.3% variable', 'apr', None),
            ('Purchase Rate', '16.9% p.a. variable', None, None),
            ('Annual Fee', '&pound;30 per cardholder', None, 'Waived at &pound;6k+ annual spend per card'),
            ('Existing Account', 'NatWest BCA required', 'required', None),
        ],
        'best_for': 'Businesses already banking with NatWest that make overseas card purchases regularly',
        'watch_out': '&pound;30 fee per cardholder unless you hit &pound;6k+ annual spend per card',
        'not_ideal': 'You need multiple employee cards and won&rsquo;t hit the spend waiver on each',
        'eligibility': 'Turnover under &pound;2m. NatWest BCA required. Credit limits from &pound;500.',
        'cta_url': 'https://www.natwest.com/business/cards/business-credit-card.html',
        'cta_label': 'View NatWest Card Details',
        'verify_source': 'natwest.com',
    },
    {
        'bank': 'Barclaycard',
        'name': 'Barclaycard Select Cashback Business Credit Card',
        'img_url': 'https://busexp1stg.wpengine.com/wp-content/uploads/2024/12/barclaycard.png',
        'img_alt': 'Barclaycard logo',
        'fit_label': 'Only option without an existing account requirement',
        'summary_strip': '25.5% APR &middot; No annual fee &middot; No existing account required',
        'verdict': 'The highest APR on this list, but the only card you can get without switching your business bank account.',
        'editorial_heading': 'Open access is the selling point, but 25.5% is the price you pay for it',
        'facts': [
            ('Representative APR', '25.5% variable', 'apr', None),
            ('Cashback', '1% on monthly spend over &pound;2k', None, 'Uncapped'),
            ('Annual Fee', '&pound;0', None, 'No annual fee'),
            ('Existing Account', 'No existing account required', 'none-required', None),
        ],
        'best_for': 'Businesses on Starling, Tide, or other non-traditional banks who can&rsquo;t access the cards above',
        'watch_out': '25.5% is the highest rate on this list. The open access comes at a cost if you carry a balance.',
        'not_ideal': 'You already have a BCA with one of the banks above and could get a lower rate',
        'eligibility': 'Sole traders, partnerships, LTDs with &pound;10k&ndash;&pound;6.5m turnover. No existing account required.',
        'cta_url': 'https://www.barclaycard.co.uk/business/cards/credit-cards/select-cashback',
        'cta_label': 'View Barclaycard Details',
        'verify_source': 'barclaycard.co.uk',
    },
]

# Capital on Tap is separate (listed after comparison table)
CAPITAL_ON_TAP = {
    'bank': 'Capital on Tap',
    'name': 'Capital on Tap Business Credit Card',
    'img_url': 'https://busexp1stg.wpengine.com/wp-content/uploads/2026/03/Capital-on-Tap-card.webp',
    'img_alt': 'Capital on Tap logo',
    'fit_label': 'Listed separately &mdash; floor-rate pricing, not representative APR',
    'summary_strip': 'From 13.86% floor APR &middot; No annual fee (free card) &middot; No existing account required',
    'verdict': 'Advertises rates &ldquo;from 13.86%&rdquo;, but that&rsquo;s a floor rate. The actual representative APR is significantly higher.',
    'editorial_heading': 'The floor rate is eye-catching, but most applicants will be offered something much higher',
    'facts': [
        ('Floor APR', 'From 13.86% variable', 'apr', None),
        ('Rep. APR (secondary sources)', '34.65%&ndash;36.19%', None, 'Uswitch, Merchant Savvy'),
        ('Annual Fee', '&pound;0 (free card) / &pound;299 (Pro card)', None, None),
        ('Existing Account', 'No existing account required', 'none-required', None),
    ],
    'best_for': 'UK limited companies needing high credit limits (up to &pound;250,000) and no FX or ATM fees',
    'watch_out': 'Average rate offered Oct&ndash;Dec 2025 was 46.05% per Capital on Tap&rsquo;s own data. Most applicants won&rsquo;t get the floor rate.',
    'not_ideal': 'You&rsquo;re a sole trader (not accepted), or you assume the advertised floor rate is what you&rsquo;ll get',
    'eligibility': 'UK limited companies and LLPs only. Min turnover &pound;24,000/year. Must be registered at Companies House.',
    'cta_url': 'https://www.capitalontap.com/en/business-credit-cards/',
    'cta_label': 'View Capital on Tap Details',
    'verify_source': 'capitalontap.com',
}


# ── Block builders ─────────────────────────────────────────────────────

blocks = []


def add(text):
    blocks.append(text)


def para(text):
    add(f'<!-- wp:paragraph -->\n<p>{text.strip()}</p>\n<!-- /wp:paragraph -->')


def heading(level, text):
    add(
        f'<!-- wp:heading {{"level":{level}}} -->\n'
        f'<h{level} class="wp-block-heading">{text.strip()}</h{level}>\n'
        f'<!-- /wp:heading -->'
    )


def raw_html(markup):
    add(f'<!-- wp:html -->\n{markup.strip()}\n<!-- /wp:html -->')


def list_block(lhtml):
    add(f'<!-- wp:list {{"ordered":true}} -->\n{lhtml.strip()}\n<!-- /wp:list -->')


def table_block(thtml):
    add(
        f'<!-- wp:table {{"className":"is-style-stripes"}} -->\n'
        f'<figure class="wp-block-table is-style-stripes">{thtml.strip()}</figure>\n'
        f'<!-- /wp:table -->'
    )


def group_start(cls, style):
    add(
        f'<!-- wp:group {{"className":"{cls}"}} -->\n'
        f'<div class="wp-block-group {cls}" style="{style}">'
    )


def group_end():
    add('</div>\n<!-- /wp:group -->')


# ── Card component builder ─────────────────────────────────────────────

def build_card(card):
    """Build a single cc-card as a wp:html block."""
    facts_html = ''
    for label, value, modifier, qualifier in card['facts']:
        val_class = 'cc-card__fact-value'
        if modifier == 'apr':
            val_class += ' cc-card__fact-value--apr'
        elif modifier == 'required':
            val_class += ' cc-card__fact-value--required'
        elif modifier == 'none-required':
            val_class += ' cc-card__fact-value--none-required'

        qual_html = ''
        if qualifier:
            qual_html = f'\n        <span class="cc-card__fact-qualifier">{qualifier}</span>'

        facts_html += f'''
      <div class="cc-card__fact">
        <span class="cc-card__fact-label">{label}</span>
        <span class="{val_class}">{value}</span>{qual_html}
      </div>'''

    verify_source = card.get('verify_source', 'provider pricing page')

    html = f'''<div class="cc-card">
  <div class="cc-card__summary-strip">{card.get('summary_strip', '')}</div>

  <div class="cc-card__header">
    <div class="cc-card__image">
      <img src="{card['img_url']}" alt="{card['img_alt']}" width="100" height="60" loading="lazy" />
    </div>
    <div class="cc-card__identity">
      <span class="cc-card__fit-label">{card['fit_label']}</span>
      <h3>{card['name']}</h3>
      <div class="cc-card__verdict">{card['verdict']}</div>
    </div>
    <div class="cc-card__header-cta">
      <a href="{card['cta_url']}" class="cc-card__cta" target="_blank" rel="noopener noreferrer">{card['cta_label']} &rarr;</a>
      <span class="cc-card__header-cta-note">Opens provider website in new tab</span>
    </div>
  </div>

  <div class="cc-card__facts">{facts_html}
  </div>

  <div class="cc-card__decision">
    <div class="cc-card__decision-item cc-card__decision-item--best">
      <span class="cc-card__decision-label">Best for</span>
      <span class="cc-card__decision-body">{card['best_for']}</span>
    </div>
    <div class="cc-card__decision-item cc-card__decision-item--watch">
      <span class="cc-card__decision-label">Watch out</span>
      <span class="cc-card__decision-body">{card['watch_out']}</span>
    </div>
    <div class="cc-card__decision-item cc-card__decision-item--not">
      <span class="cc-card__decision-label">Not ideal if</span>
      <span class="cc-card__decision-body">{card['not_ideal']}</span>
    </div>
    <div class="cc-card__decision-item cc-card__decision-item--eligibility">
      <span class="cc-card__decision-label">Eligibility</span>
      <span class="cc-card__decision-body">{card['eligibility']}</span>
    </div>
  </div>

  <div class="cc-card__editorial-heading">{card.get('editorial_heading', '')}</div>
  <div class="cc-card__editorial-toggle">Read our full editorial take &#9660;</div>

  <div class="cc-card__action">
    <span class="cc-card__trust">Rates verified against {verify_source}, 20 March 2026</span>
  </div>
</div>'''

    raw_html(html)


# ── CSS block ──────────────────────────────────────────────────────────

CC_TOC_CSS = '''<style>
/* Table of Contents Sidebar — auto-generated from H2s */
.cc-toc {
  display: none;
}

@media (min-width: 1340px) {
  .cc-toc {
    display: block;
    position: fixed;
    top: 140px;
    width: 220px;
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    padding: 0 0 20px 0;
    z-index: 50;
  }
  .cc-toc__title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #888;
    margin-bottom: 12px;
    padding-left: 14px;
  }
  .cc-toc__list {
    list-style: none;
    margin: 0;
    padding: 0;
    border-left: 1px solid #e0e0e0;
  }
  .cc-toc__item {
    margin: 0;
    padding: 0;
  }
  .cc-toc__link {
    display: block;
    padding: 6px 14px;
    font-size: 13px;
    line-height: 1.4;
    color: #666;
    text-decoration: none;
    margin-left: -1px;
    border-left: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s;
  }
  .cc-toc__link:hover {
    color: #333;
  }
  .cc-toc__link--active {
    color: #6b3fa0;
    border-left-color: #6b3fa0;
    font-weight: 600;
  }
  /* Scrollbar styling */
  .cc-toc::-webkit-scrollbar {
    width: 3px;
  }
  .cc-toc::-webkit-scrollbar-thumb {
    background: #ddd;
    border-radius: 3px;
  }
}
</style>'''


CC_TOC_HTML = '''<nav class="cc-toc" id="cc-toc" aria-label="Table of contents">
  <div class="cc-toc__title">On this page</div>
  <ul class="cc-toc__list" id="cc-toc-list"></ul>
</nav>'''


CC_TOC_JS = '''<script>
(function() {
  var toc = document.getElementById('cc-toc');
  var list = document.getElementById('cc-toc-list');
  if (!toc || !list) return;

  // Gather all H2s in the entry-content area
  var container = document.querySelector('.entry-content') || document.body;
  var h2s = container.querySelectorAll('h2.wp-block-heading');
  if (h2s.length < 2) { toc.style.display = 'none'; return; }

  // Generate IDs and build TOC links
  var sections = [];
  h2s.forEach(function(h2, i) {
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
  });

  // Position TOC relative to the content area
  // Record the absolute (document-relative) top of the first H2 once
  var contentAbsoluteTop = null;
  var stickyTop = 100; // fallback top when scrolled past content start

  function positionToc() {
    var entry = document.querySelector('.entry-content.container');
    if (!entry) return;
    var rect = entry.getBoundingClientRect();
    var left = rect.left - 240;
    if (left < 16) { toc.style.display = 'none'; return; }
    toc.style.left = left + 'px';
    toc.style.display = '';
  }

  function alignTocVertically() {
    // Calculate where the first H2 sits in the document (once)
    if (contentAbsoluteTop === null && sections.length) {
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      contentAbsoluteTop = sections[0].el.getBoundingClientRect().top + scrollTop;
    }
    if (contentAbsoluteTop === null) return;

    var scrollTop = window.scrollY || document.documentElement.scrollTop;
    // If content start is still visible, align with it; otherwise stick near viewport top
    var viewportTop = contentAbsoluteTop - scrollTop;
    toc.style.top = Math.max(viewportTop, stickyTop) + 'px';
  }

  // Scroll spy: highlight current section
  var links = list.querySelectorAll('.cc-toc__link');
  var rafId = null;
  function onScroll() {
    if (rafId) return;
    rafId = requestAnimationFrame(function() {
      rafId = null;
      var current = -1;
      var scrollY = window.scrollY || document.documentElement.scrollTop;
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
  alignTocVertically();
  window.addEventListener('scroll', function() { onScroll(); alignTocVertically(); }, { passive: true });
  window.addEventListener('resize', function() { positionToc(); alignTocVertically(); });
  onScroll();
})();
</script>'''


CC_CARD_CSS = '''<style>
/* Credit Card Comparison Component v4 — BusinessExpert
   Palette: brand purple #6b3fa0, neutral surfaces, semantic accents only */

/* ── Card shell ── */
.cc-card {
  border: 1px solid #d4d4d4;
  border-radius: 8px;
  background: #fff;
  margin-bottom: 32px;
  overflow: hidden;
}

/* ── APR summary strip ── */
.cc-card__summary-strip {
  background: #f7f7f8;
  border-bottom: 1px solid #e5e5e5;
  padding: 10px 28px;
  font-size: 13.5px;
  font-weight: 600;
  color: #1a1a1a;
  letter-spacing: 0.01em;
}
.cc-card__summary-strip strong {
  color: #6b3fa0;
  font-weight: 700;
}

/* ── Header: image + identity ── */
.cc-card__header {
  display: grid;
  grid-template-columns: 100px 1fr;
  grid-template-rows: auto auto;
  gap: 4px 20px;
  align-items: start;
  padding: 20px 28px 16px 28px;
}
.cc-card__image {
  width: 100px;
  height: 72px;
  background: #f5f5f6;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  grid-row: 1 / 3;
}
.cc-card__image img {
  max-width: 100%;
  max-height: 60px;
  object-fit: contain;
  display: block;
}
.cc-card__identity {
  min-width: 0;
}
.cc-card__fit-label {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #6b3fa0;
  background: none;
  padding: 0;
  margin-bottom: 4px;
}
.cc-card__identity h3 {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.3;
  color: #1a1a1a;
  margin-bottom: 6px;
}
.cc-card__verdict {
  font-size: 15px;
  line-height: 1.5;
  color: #333;
}
.cc-card__header-cta {
  display: flex;
  align-items: center;
  gap: 16px;
  grid-column: 2;
  padding-top: 6px;
}
.cc-card__header-cta-note {
  font-size: 12px;
  color: #555;
  line-height: 1.3;
}

/* ── 2x2 facts grid ── */
.cc-card__facts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  margin: 16px 28px 0 28px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background: #fff;
  overflow: hidden;
}
.cc-card__fact {
  padding: 11px 16px;
  border-bottom: 1px solid #e5e5e5;
}
.cc-card__fact:nth-child(even) {
  border-left: 1px solid #e5e5e5;
}
.cc-card__fact:nth-last-child(-n+2) {
  border-bottom: none;
}
.cc-card__fact-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #777;
  margin-bottom: 2px;
}
.cc-card__fact-value {
  display: block;
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.35;
}
.cc-card__fact-value--apr {
  color: #1a1a1a;
  font-size: 19px;
  font-weight: 800;
}
.cc-card__fact-qualifier {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: #555;
  line-height: 1.35;
  margin-top: 1px;
}
.cc-card__fact-value--required {
  color: #1a1a1a;
  font-size: 16px;
  font-weight: 700;
}
.cc-card__fact-value--none-required {
  color: #1a1a1a;
  font-size: 16px;
  font-weight: 700;
}

/* ── Decision rows: Best for / Watch out / Not ideal if / Eligibility ── */
.cc-card__decision {
  margin: 20px 28px 0 28px;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.cc-card__decision-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 10px;
  font-size: 14px;
  line-height: 1.5;
  color: #1a1a1a;
  padding: 14px 16px;
  background: #fff;
  border-left: 3px solid transparent;
  border-bottom: 1px solid #ebebeb;
}
.cc-card__decision-item:last-child {
  border-bottom: none;
}
.cc-card__decision-label {
  font-weight: 700;
  font-size: 13px;
  color: #1a1a1a;
  padding-top: 1px;
  white-space: nowrap;
}
.cc-card__decision-body {
  color: #333;
}
/* Semantic accents — left bar + label colour only, white backgrounds */
.cc-card__decision-item--best {
  border-left-color: #2e7d32;
  background: #fff;
}
.cc-card__decision-item--best .cc-card__decision-label {
  color: #1b6e1f;
}
.cc-card__decision-item--watch {
  border-left-color: #d48806;
  background: #fff;
}
.cc-card__decision-item--watch .cc-card__decision-label {
  color: #a86a00;
}
.cc-card__decision-item--not {
  border-left-color: #999;
  background: #fff;
}
.cc-card__decision-item--not .cc-card__decision-label {
  color: #555;
}
.cc-card__decision-item--not .cc-card__decision-body {
  color: #333;
  font-size: 14px;
}
.cc-card__decision-item--eligibility {
  border-left-color: #b0b0b0;
  background: #fff;
}
.cc-card__decision-item--eligibility .cc-card__decision-label {
  color: #555;
}
.cc-card__decision-item--eligibility .cc-card__decision-body {
  color: #333;
  font-size: 14px;
}

/* ── Editorial summary heading ── */
.cc-card__editorial-heading {
  font-size: 17px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 20px 28px 0 28px;
  line-height: 1.4;
}

/* ── "Read our full editorial take" expandable bar ── */
.cc-card__editorial-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 12px 28px 0 28px;
  padding: 10px 16px;
  background: #fff;
  border: 1px solid #6b3fa0;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #6b3fa0;
  cursor: pointer;
  transition: background 0.15s;
}
.cc-card__editorial-toggle:hover {
  background: #f8f5fc;
}

/* ── CTA + action area ── */
.cc-card__action {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  margin: 20px 28px 20px 28px;
}
.cc-card__cta {
  display: inline-block;
  padding: 10px 26px;
  background: #6b3fa0;
  color: #fff !important;
  font-size: 14px;
  font-weight: 600;
  border-radius: 7px;
  text-decoration: none;
  transition: background 0.15s;
  white-space: nowrap;
}
.cc-card__cta:hover {
  background: #5a3488;
}

/* ── Verification / trust line ── */
.cc-card__trust {
  font-size: 12.5px;
  color: #666;
  line-height: 1.4;
  padding-left: 2px;
}

/* ── Section divider before card listings ── */
.cc-section-divider {
  margin-top: 48px;
  padding-top: 48px;
  border-top: 1px solid #e0e0e0;
}
.cc-section-divider__label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b3fa0;
  margin-bottom: 8px;
}
.cc-section-divider__label::before {
  content: '';
  display: block;
  width: 20px;
  height: 2px;
  background: #6b3fa0;
}

/* ── Mobile ── */
@media (max-width: 640px) {
  .cc-card__summary-strip {
    padding: 10px 20px;
  }
  .cc-card__header {
    grid-template-columns: 80px 1fr;
    gap: 4px 14px;
    padding: 16px 20px 12px 20px;
  }
  .cc-card__header-cta {
    grid-column: 1 / -1;
    flex-direction: column;
    align-items: stretch;
    gap: 6px;
    padding-top: 8px;
  }
  .cc-card__image {
    width: 80px;
    height: 58px;
    padding: 6px;
    grid-row: 1 / 3;
  }
  .cc-card__image img {
    max-height: 46px;
  }
  .cc-card__facts {
    grid-template-columns: 1fr;
    margin: 16px 20px 0 20px;
  }
  .cc-card__fact:nth-child(even) {
    border-left: none;
  }
  .cc-card__fact {
    border-bottom: 1px solid #e5e5e5;
  }
  .cc-card__fact:last-child {
    border-bottom: none;
  }
  .cc-card__decision {
    margin: 16px 20px 0 20px;
  }
  .cc-card__decision-item {
    grid-template-columns: 1fr;
    gap: 4px;
  }
  .cc-card__decision-label {
    white-space: normal;
  }
  .cc-card__editorial-heading {
    margin: 16px 20px 0 20px;
  }
  .cc-card__editorial-toggle {
    margin: 12px 20px 0 20px;
  }
  .cc-card__action {
    flex-direction: column;
    align-items: flex-start;
    margin: 20px 20px 20px 20px;
  }
  .cc-card__cta {
    width: 100%;
    text-align: center;
  }
}
</style>'''


# ── Page content ───────────────────────────────────────────────────────

def main():
    # CSS blocks first
    raw_html(CC_TOC_CSS)
    raw_html(CC_CARD_CSS)

    # TOC sidebar (populated by JS at bottom)
    raw_html(CC_TOC_HTML)

    # ── Verdict box ──
    group_start('verdict-box',
                'border-left:4px solid #3b5bdb;background-color:#f0f4ff;'
                'padding:18px 20px;border-radius:0 6px 6px 0')
    para('The promotional 0% period ends. When it does, the standard purchase APR is the rate you pay on every pound of balance you carry. Most comparison pages bury that figure behind headline offers. We checked every provider&rsquo;s current pricing page so you don&rsquo;t have to.')
    group_end()

    # ── Intro paragraphs ──
    para('If you clear your balance in full every month, APR is irrelevant to you. A <a href="/business-credit-cards/cashback/">cashback</a> or <a href="/business-credit-cards/rewards/">rewards card</a> will deliver more value. If you carry a balance &mdash; whether by design or because cash flow means you occasionally can&rsquo;t clear &mdash; the ongoing purchase rate is your real cost of borrowing.')

    para('This page covers UK business credit cards with the lowest standard purchase APR, verified against each provider&rsquo;s pricing page in March 2026. We excluded introductory 0% offers and rewards-driven cards where a higher APR is the trade-off for points or perks.')

    # ── Keep / Switch / Look Elsewhere ──
    heading(2, 'Keep / Switch / Look Elsewhere')

    table_block(
        '<table><thead><tr><th>Your situation</th><th>Focus on</th></tr></thead>'
        '<tbody>'
        '<tr><td>You clear in full every month</td><td>Cashback or rewards rate, not APR</td></tr>'
        '<tr><td>You carry a balance most months</td><td>Lowest representative APR you can access</td></tr>'
        '<tr><td>You sometimes carry a balance</td><td>Low APR plus no or waivable annual fee</td></tr>'
        '<tr><td>You need a large purchase facility</td><td>Credit limit ceiling and repayment flexibility</td></tr>'
        '</tbody></table>'
    )

    # ── What Representative APR Means ──
    heading(2, 'What &ldquo;Representative APR&rdquo; Means for Your Application')

    para('A representative APR is the rate that at least 51% of successful applicants receive. That means up to 49% may be offered a higher rate, and the provider is under no obligation to tell you the ceiling before you apply.')

    para('Several providers on this list do not publish the upper end of their rate range. Where a card shows a single representative APR with no published range, you have less visibility of the rate you&rsquo;ll actually be offered. We&rsquo;ve noted this in each card&rsquo;s entry below.')

    para('If your business has a short trading history, thin credit file, or you&rsquo;re applying as a sole trader, expect to be offered a rate above the headline figure. The representative APR is a useful ranking tool, but it is not a guarantee of the rate you&rsquo;ll get.')

    # ── The Low-APR Business Credit Cards ──
    raw_html('<div class="cc-section-divider"><span class="cc-section-divider__label">Detailed reviews</span></div>')

    heading(2, 'The Low-APR Business Credit Cards')

    para('Ordered by representative APR, lowest first. Capital on Tap is listed separately after the comparison table because it advertises a floor rate rather than a representative APR, which makes direct comparison misleading.')

    # ── 6 ranked cards ──
    for card in CARDS:
        build_card(card)

    # ── APR Comparison at a Glance ──
    heading(2, 'APR Comparison at a Glance')

    table_block(
        '<table><thead><tr>'
        '<th>Card</th><th>Representative APR</th><th>Annual Fee</th>'
        '<th>Account Required</th><th>Sole Traders</th>'
        '</tr></thead><tbody>'
        '<tr><td>Lloyds</td><td>15.95%</td><td>&pound;32/card (waivable)</td><td>Yes</td><td>Yes</td></tr>'
        '<tr><td>Metro Bank</td><td>18.9%</td><td>&pound;0</td><td>Yes</td><td>Yes</td></tr>'
        '<tr><td>HSBC</td><td>22%</td><td>&pound;32/card (yr 1 free)</td><td>Yes</td><td>Not stated</td></tr>'
        '<tr><td>Santander</td><td>23.7%</td><td>&pound;30/account</td><td>Yes</td><td>Not stated</td></tr>'
        '<tr><td>NatWest</td><td>24.3%</td><td>&pound;30/card (waivable)</td><td>Yes</td><td>Not stated</td></tr>'
        '<tr><td>Barclaycard</td><td>25.5%</td><td>&pound;0</td><td>No</td><td>Yes</td></tr>'
        '</tbody></table>'
    )

    para('<em>Rates verified against provider pricing pages, 20 March 2026. All rates are variable and may change after publication.</em>')

    # ── Capital on Tap (separate) ──
    heading(2, 'Not Directly Comparable: Capital on Tap')

    para('Capital on Tap uses floor-rate pricing rather than a single representative APR. Including it in the ranked table above would suggest a like-for-like comparison that doesn&rsquo;t hold. We&rsquo;ve listed it separately so you can assess it on its own terms.')

    build_card(CAPITAL_ON_TAP)

    # ── What the Rate Comparison Alone Misses ──
    heading(2, 'What the Rate Comparison Alone Misses')

    para('APR is the right primary filter when ongoing balance-carrying cost is your decision. It isn&rsquo;t the only cost.')

    para('Annual or monthly card fees add fixed cost that matters at lower spend volumes. A card with a 15.95% APR and a &pound;32 annual fee may cost you more than a card at 18.9% with no fee, depending on the balance you carry and whether you hit the spend threshold to waive the fee.')

    para('Foreign transaction fees matter if your business spends internationally. Most cards here charge around 2.99% on non-sterling transactions. NatWest charges nothing on overseas purchases, which is a meaningful difference for businesses with regular overseas card spend. We recommend running the numbers for your own spend pattern rather than relying on APR alone.')

    para('Per-cardholder versus per-account fee structures change the maths with team size. Santander&rsquo;s &pound;30 covers all cardholders. NatWest and Lloyds charge per cardholder, waivable per card with sufficient spend. If you&rsquo;re issuing cards to four or five team members, that fee structure changes the total cost calculation entirely.')

    # ── Who Low-APR Cards Don't Suit ──
    heading(2, 'Who Low-APR Cards Don&rsquo;t Suit')

    para('If you pay in full every month, a <a href="/business-credit-cards/cashback/">cashback</a> or <a href="/business-credit-cards/rewards/">rewards card</a> will deliver more value to you. The cards with the best rewards programmes in the UK business market carry higher APRs, but if interest never accrues, the APR is irrelevant.')

    para('If your business needs a high credit limit, the ranked cards above cap at &pound;25,000. Capital on Tap (listed separately below the table) offers up to &pound;250,000, but only for qualifying limited companies and LLPs, and its actual representative APR is significantly higher than the floor rate it advertises.')

    para('If your business is under 12 months old, we found that most providers on this list don&rsquo;t publish a hard minimum trading requirement. But lenders will apply stricter criteria to newer businesses, and the rate you&rsquo;re offered may be above the representative APR. If you&rsquo;ve just started trading, prepare for the possibility that the advertised rate isn&rsquo;t the rate you&rsquo;ll get.')

    # ── How to Compare Before You Apply ──
    heading(2, 'How to Compare Before You Apply')

    para('We recommend checking three things beyond the representative APR:')

    list_block(
        '<ol>\n'
        '    <li>Whether the card is restricted to existing customers of that bank. Most on this list are.</li>\n'
        '    <li>Whether a rate range is published alongside the representative figure. Some aren&rsquo;t, which means you have less visibility of what you&rsquo;ll actually be offered.</li>\n'
        '    <li>Whether the fee is per cardholder or per account. If you need multiple cards, this changes the total cost ranking.</li>\n'
        '</ol>'
    )

    para('In our editorial view, the existing-account requirement is the biggest practical filter on this list. Five of the six ranked cards require a business current account with that bank. If you don&rsquo;t already have one, your realistic options narrow to Barclaycard (at the highest APR on this list) or Capital on Tap (with its significantly higher actual rates). That constraint matters more than any rate difference between the cards you can&rsquo;t access.')

    # ── Methodology and Disclosure ──
    heading(2, 'Methodology and Disclosure')

    group_start('methodology',
                'border:1px solid #eee;border-radius:6px;'
                'padding:20px 24px 28px 24px;background:#f9f9f9')

    para('<strong>Sources:</strong> All rates, fees, and eligibility criteria were verified against each provider&rsquo;s public pricing page on 20 March 2026. Secondary sources (Finder UK, Head for Points, Uswitch, Merchant Savvy) are noted where used to corroborate or supplement provider data.')

    para('<strong>Rate type:</strong> All rates listed are variable. Providers may change them at any time after publication.')

    para('<strong>Affiliate disclosure:</strong> BusinessExpert may receive referral or affiliate fees from some of the card providers listed on this page. This does not affect our editorial rankings, which are based on verified rates and publicly available product data. Our methodology and ranking criteria are described above.')

    para('<strong>Regulatory note:</strong> This page is editorial content, not regulated financial advice. Credit products are subject to status and provider approval. We recommend comparing offers directly with providers before applying.')

    para('<a href="/editorial-policy/">Read our full editorial policy</a>')

    group_end()

    # Spacer after methodology
    para('&nbsp;')

    # TOC scroll-spy JS (at bottom so DOM is ready)
    raw_html(CC_TOC_JS)

    # ── Output ──
    content = '\n\n'.join(blocks)
    print(f'Generated {len(blocks)} blocks, {len(content):,} chars')

    out_path = os.path.join(tempfile.gettempdir(), 'wp_push_v3.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'content': content}, f, ensure_ascii=False)
    print(f'Written to {out_path}')

    return out_path


if __name__ == '__main__':
    main()
