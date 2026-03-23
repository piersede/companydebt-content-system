#!/usr/bin/env node
/**
 * check_intro_quality.js
 *
 * Enforces intro quality rules from 09-voice-governance.md §14
 * and 12-structure-governance.md opening rules.
 *
 * Checks:
 * - intro does not begin with installed-base boilerplate
 * - buyer trigger appears in paragraph 1
 * - decision frame appears by paragraph 2
 * - intro avoids banned vague market-language patterns
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

// Extract first N paragraphs from WP block content
function getFirstParagraphs(content, n) {
  const paras = [];
  const re = /<!-- wp:paragraph[^>]*-->\s*<p>([\s\S]*?)<\/p>\s*<!-- \/wp:paragraph -->/g;
  let m;
  while ((m = re.exec(content)) !== null && paras.length < n) {
    paras.push(stripHtml(m[1]));
  }
  return paras;
}

// Banned opening patterns (from 09-voice-governance.md §14)
const BANNED_OPENERS = [
  { re: /^.{0,20}has a large installed base/i, label: 'Installed-base opener' },
  { re: /^.{0,20}is familiar and stable/i, label: '"Familiar and stable" opener' },
  { re: /^.{0,20}handles? (?:CRM|deadline|workflow|billing)/i, label: 'Feature-list opener' },
  { re: /^searches for .+ alternatives/i, label: 'Search-intent opener' },
  { re: /^in today.s|^in the modern|^in an era/i, label: '"In today\'s" temporal opener' },
  { re: /^whether you.re|^whether you are/i, label: '"Whether you are" fake inclusiveness' },
  { re: /^i think|^in my view|^i believe/i, label: 'Weak first-person opener' },
  { re: /^in this article/i, label: '"In this article" self-referential opener' },
];

// Buyer trigger signals
const BUYER_TRIGGERS = /(?:frustrat|struggle|spend.{0,20}(?:time|hours)|pain|problem|stuck|outgrown|strain|ceiling|chasing|missing|overdue|deadline|clients? (?:don.t|won.t|aren.t|haven.t)|manual|repetitive|wast)/i;

// Decision frame signals
const DECISION_FRAME = /(?:decision|choose|switch|replace|augment|alternative|option|which|should you|need to decide|right (?:tool|choice|fit)|makes sense)/i;

// Banned vague market language
const VAGUE_MARKET = [
  { re: /growing number of (?:practices|firms|accountants)/i, label: '"Growing number" unsourced' },
  { re: /most (?:practices|firms|accountants) (?:find|discover|realise)/i, label: '"Most practices" unsourced' },
  { re: /tend(?:s)? to (?:come from|be driven|happen)/i, label: '"Tend to" market inference' },
  { re: /common (?:choice|frustration|pattern)/i, label: '"Common X" unsourced claim' },
];

const results = [];

for (const article of articles) {
  const { title, content } = article;
  const paras = getFirstParagraphs(content, 3);
  if (paras.length === 0) continue;

  const issues = [];

  // Check banned openers in paragraph 1
  for (const banned of BANNED_OPENERS) {
    if (banned.re.test(paras[0])) {
      issues.push(`[INTRO-BAN] ${banned.label}: "${paras[0].substring(0, 60)}..."`);
    }
  }

  // Check buyer trigger in paragraph 1
  if (!BUYER_TRIGGERS.test(paras[0])) {
    issues.push('[INTRO-TRIGGER] No buyer trigger/pain signal in paragraph 1');
  }

  // Check decision frame by paragraph 2
  const firstTwo = paras.slice(0, 2).join(' ');
  if (!DECISION_FRAME.test(firstTwo)) {
    issues.push('[INTRO-FRAME] No decision frame found by paragraph 2');
  }

  // Check vague market language in first 3 paragraphs
  const firstThree = paras.slice(0, 3).join(' ');
  for (const vague of VAGUE_MARKET) {
    if (vague.re.test(firstThree)) {
      issues.push(`[INTRO-VAGUE] ${vague.label} in opening paragraphs`);
    }
  }

  if (issues.length > 0) {
    results.push({ title, issues });
  }
}

console.log('=== INTRO QUALITY CHECK ===\n');

if (results.length === 0) {
  console.log('All article intros pass quality checks.');
} else {
  for (const r of results) {
    console.log(`[FAIL] ${r.title}`);
    for (const issue of r.issues) {
      console.log(`       ${issue}`);
    }
    console.log();
  }
}

console.log(`\nChecked: ${articles.length} articles`);
console.log(`Failing: ${results.length}`);
