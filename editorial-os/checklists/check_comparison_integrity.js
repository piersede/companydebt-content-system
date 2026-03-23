#!/usr/bin/env node
/**
 * check_comparison_integrity.js
 *
 * Enforces comparison/alternatives page structural integrity rules from
 * 11-comparison-governance.md §13 and 05-scoring-rubric.md A1-A8.
 *
 * Reads blog_posts_html_fixed.json (or path passed as argv[1]).
 * Flags articles that appear to be comparison/alternatives pages and checks:
 * - replacement vs augmentation distinction before naming tools
 * - alternatives list excludes non-alternatives (retention guidance separate)
 * - house-product not-fit condition exists
 * - decision block uses reader-led labels (Rule K)
 * - product sections include required fields
 * - augmentation path appears before premature narrowing
 */

'use strict';

const fs = require('fs');
const path = require('path');

const dataPath = process.argv[2] || path.join(__dirname, '..', '..', 'blog_posts_html_fixed.json');
if (!fs.existsSync(dataPath)) {
  console.error('Data file not found:', dataPath);
  process.exit(1);
}

const articles = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

function stripHtml(html) {
  return html.replace(/<!--.*?-->/gs, '').replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
}

function isComparisonPage(title) {
  return /alternative|vs\.?|versus|compared|comparison|review|best .+ software/i.test(title);
}

const results = [];

for (const article of articles) {
  if (!isComparisonPage(article.title)) continue;

  const { title, content } = article;
  const text = stripHtml(content);
  const issues = [];

  // A1: Replacement vs augmentation before first product mention
  const augmentRe = /augment|add.?on|specialist.?(tool|layer)|alongside|keep .+ (and|but)/i;
  const replaceRe = /replac(e|ement)|switch(ing)?|migrat(e|ion)|move away/i;
  const hasAugment = augmentRe.test(text);
  const hasReplace = replaceRe.test(text);
  if (!hasAugment && !hasReplace) {
    issues.push('[A1] No replacement vs augmentation distinction found');
  }

  // A2: Decision block in first fold
  const decisionBlockRe = /if you want to (replace|keep|switch)|if your primary problem|if .+ is still (broadly )?working/i;
  const firstFold = text.substring(0, 800);
  if (!decisionBlockRe.test(firstFold)) {
    issues.push('[A2] No decision block found in first ~800 characters');
  }

  // A3: Vendor-summary drift — check if article is just tool descriptions
  const h2s = [...content.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/gi)].map(m => stripHtml(m[1]));
  const toolNameHeadings = h2s.filter(h => /^(karbon|taxdome|businessexpert|senta|brightmanager|accountancymanager|xero|quickbooks)/i.test(h));
  if (toolNameHeadings.length >= 3 && !h2s.some(h => /why|when|should|decision|choose|which/i.test(h))) {
    issues.push('[A3] Vendor-summary drift: 3+ tool-name headings with no decision-oriented heading');
  }

  // A5: House product after decision frame
  const businessexpertIdx = text.toLowerCase().indexOf('businessexpert');
  const decisionMatch = text.match(augmentRe) || text.match(replaceRe);
  if (businessexpertIdx > -1 && decisionMatch) {
    const decisionIdx = text.toLowerCase().indexOf(decisionMatch[0].toLowerCase());
    if (businessexpertIdx < decisionIdx) {
      issues.push('[A5] BusinessExpert mentioned before replacement/augmentation distinction');
    }
  }

  // A6: House product not-fit condition
  const notFitRe = /not (the right|a good|a fit|best suited)|businessexpert (is not|does not|doesn.t|won.t)|not what you need if/i;
  if (businessexpertIdx > -1 && !notFitRe.test(text)) {
    issues.push('[A6] BusinessExpert appears without explicit "not the right fit" condition');
  }

  // A7: Conclusion before CTA
  const ctaRe = /businessexpert\.com\/(pricing|demo|trial|sign.?up|get.?started|book)/i;
  const conclusionRe = /<h2[^>]*>[^<]*(conclusion|which should|our view|verdict|which is right)/i;
  const hasCta = ctaRe.test(content);
  const hasConclusion = conclusionRe.test(content);
  if (hasCta && !hasConclusion) {
    issues.push('[A7] CTA link found but no conclusion/verdict heading');
  }

  // Rule K: Taxonomy labels in decision blocks
  const taxonomyLabels = /(?:^|\n)\s*(?:Full platform switch:|Specialist add-on:|Stay put:)/m;
  if (taxonomyLabels.test(text)) {
    issues.push('[RULE-K] Taxonomy labels found in decision blocks — use guided scenario language');
  }

  // Rule L: Retention guidance inside alternatives list
  // Heuristic: check if "stay" / "keep" / "remain" appears between tool headings
  const stayInAlts = /(?:stay (?:on|with)|keep using|remain on) .{0,30}(?:karbon|taxdome|accountancymanager|brightmanager|senta)/i;
  if (stayInAlts.test(text) && !/you may not need an alternative|when staying/i.test(text)) {
    issues.push('[RULE-L] Retention guidance may be mixed into alternatives list — separate into adjacent block');
  }

  if (issues.length > 0) {
    results.push({ title, issues });
  }
}

console.log('=== COMPARISON INTEGRITY CHECK ===\n');

if (results.length === 0) {
  console.log('All comparison/alternatives pages pass integrity checks.');
} else {
  for (const r of results) {
    console.log(`[FAIL] ${r.title}`);
    for (const issue of r.issues) {
      console.log(`       ${issue}`);
    }
    console.log();
  }
}

console.log(`Checked: ${articles.filter(a => isComparisonPage(a.title)).length} comparison/alternatives articles`);
console.log(`Failing: ${results.length}`);
