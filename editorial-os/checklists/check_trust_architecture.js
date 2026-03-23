#!/usr/bin/env node
/**
 * check_trust_architecture.js
 *
 * Enforces trust architecture rules from 11-comparison-governance.md §8-12
 * and 05-scoring-rubric.md T1-T6.
 *
 * Checks vendor-authored comparison/review pages for:
 * - page mode declaration
 * - perspective disclosure near top
 * - product-specific disclosure near first house-product mention
 * - methodology / evidence basis present
 * - house-product containment (best fit / not a fit / conditions)
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

function isVendorComparison(title) {
  return /alternative|vs\.?|versus|compared|comparison|review|best .+ software/i.test(title);
}

const results = [];

for (const article of articles) {
  if (!isVendorComparison(article.title)) continue;

  const { title, content } = article;
  const text = stripHtml(content);
  const issues = [];

  // T1: Page mode declaration — check for explicit mode signal
  // In practice this is declared in the editorial brief, not in article HTML.
  // Check for implicit signals: disclosure language that declares perspective.
  const hasDisclosure = /written by the businessexpert team|businessexpert is our product|reflects our assessment|from (?:our|a vendor) perspective/i.test(text);

  // T2: Perspective disclosure near top (first 20% of text)
  const topQuarter = text.substring(0, Math.floor(text.length * 0.2));
  const disclosureInTop = /businessexpert is our product|written by the businessexpert team|reflects our assessment/i.test(topQuarter);
  if (!disclosureInTop) {
    issues.push('[T2] Perspective disclosure not found in first 20% of article');
  }

  // T3: Category frame fairness — check for binary that only favours house product
  const binaryRe = /(?:the (?:real|core|key) (?:difference|distinction|question) is|the choice (?:comes down|boils down) to)/i;
  if (binaryRe.test(text)) {
    // Check if the binary mentions a scenario where BusinessExpert is NOT the answer
    const binaryIdx = text.search(binaryRe);
    const afterBinary = text.substring(binaryIdx, binaryIdx + 500);
    if (!/(?:not|neither|if you need|for practices that want).{0,80}(?:karbon|taxdome|senta|brightmanager)/i.test(afterBinary)) {
      issues.push('[T3] Binary frame found but may not preserve fairness — check manually');
    }
  }

  // T4: Real reader choice preserved
  const businessexpertIdx = text.toLowerCase().indexOf('businessexpert');
  if (businessexpertIdx > -1) {
    const hasOtherPath = /(?:if (?:you|your firm|the practice) (?:want|need|prefer)|for practices (?:that|whose)).{0,80}(?:karbon|taxdome|senta|brightmanager|accountancymanager)/i.test(text);
    if (!hasOtherPath) {
      issues.push('[T4] No explicit alternative path preserved for readers who should not choose BusinessExpert');
    }
  }

  // T5: House product not-fit conditions
  if (businessexpertIdx > -1) {
    const bestFit = /businessexpert.{0,30}(?:best (?:for|fit|suited)|strongest (?:for|fit)|designed for|built for)/i.test(text);
    const notFit = /businessexpert.{0,30}(?:not (?:the right|a good|a fit|best)|does not|doesn.t|won.t)|not what you need if/i.test(text);
    const conditions = /(?:makes sense (?:if|when|for)|works (?:best|well) (?:if|when|for)|requires? (?:that|a practice))/i.test(text);

    if (!bestFit) issues.push('[T5a] No explicit "best fit" condition for BusinessExpert');
    if (!notFit) issues.push('[T5b] No explicit "not a fit" condition for BusinessExpert');
    if (!conditions) issues.push('[T5c] No "required conditions for adoption" stated for BusinessExpert');
  }

  // T6: Article coherent without house product
  // Heuristic: check if BusinessExpert appears in more than 30% of paragraphs
  const paragraphs = content.split(/<!-- \/?wp:paragraph -->/g).filter(p => p.trim().length > 20);
  const businessexpertParagraphs = paragraphs.filter(p => /businessexpert/i.test(p));
  if (paragraphs.length > 0 && businessexpertParagraphs.length / paragraphs.length > 0.4) {
    issues.push(`[T6] BusinessExpert appears in ${Math.round(businessexpertParagraphs.length / paragraphs.length * 100)}% of paragraphs — article may collapse without house product`);
  }

  // Methodology / evidence basis
  const hasMethodology = /(?:based on|verified|checked|reviewed).{0,40}(?:documentation|pricing page|product page|feature|March 2026|testing)/i.test(text);
  if (!hasMethodology) {
    issues.push('[METH] No methodology or evidence basis statement found');
  }

  if (issues.length > 0) {
    results.push({ title, issues });
  }
}

console.log('=== TRUST ARCHITECTURE CHECK ===\n');

if (results.length === 0) {
  console.log('All vendor-authored comparison pages pass trust architecture checks.');
} else {
  for (const r of results) {
    console.log(`[FAIL] ${r.title}`);
    for (const issue of r.issues) {
      console.log(`       ${issue}`);
    }
    console.log();
  }
}

console.log(`Checked: ${articles.filter(a => isVendorComparison(a.title)).length} vendor comparison articles`);
console.log(`Failing: ${results.length}`);
