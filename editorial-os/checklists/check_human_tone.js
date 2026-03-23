#!/usr/bin/env node
/**
 * check_human_tone.js
 *
 * Heuristic enforcement of human tone rules from 09-voice-governance.md §13
 * and failure mode 25 (taxonomic human-flattening) in 14-failure-modes-and-recovery.md.
 *
 * Checks:
 * - repeated taxonomy labels
 * - excessive repeated noun phrases
 * - overuse of clipped declarative sentences
 * - missing reader-oriented section labels
 * - abstract SaaS shorthand without lived consequences
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

function getHeadings(content) {
  return [...content.matchAll(/<h[23][^>]*>([\s\S]*?)<\/h[23]>/gi)].map(m => stripHtml(m[1]));
}

function getSentences(text) {
  return text.split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 10);
}

// Taxonomy label patterns (compressed, non-reader-oriented)
const TAXONOMY_LABELS = [
  /^full platform (?:switch|migration|replacement):?$/i,
  /^specialist add-?on:?$/i,
  /^stay put:?$/i,
  /^direct replacement:?$/i,
  /^adjacent specialist:?$/i,
  /^process change:?$/i,
  /^category [a-z]:?$/i,
];

// Abstract SaaS shorthand (without lived consequences)
const ABSTRACT_SHORTHAND = [
  { re: /workflow inefficienc(?:y|ies)/i, label: '"workflow inefficiencies"' },
  { re: /document collection challenges/i, label: '"document collection challenges"' },
  { re: /client communication gaps/i, label: '"client communication gaps"' },
  { re: /operational bottlenecks/i, label: '"operational bottlenecks"' },
  { re: /process optimis?ation/i, label: '"process optimisation"' },
  { re: /digital transformation/i, label: '"digital transformation"' },
  { re: /streamlined? (?:process|workflow|operations)/i, label: '"streamlined X"' },
];

const results = [];

for (const article of articles) {
  const { title, content } = article;
  const text = stripHtml(content);
  const headings = getHeadings(content);
  const sentences = getSentences(text);
  const issues = [];

  // Check 1: Taxonomy labels in headings
  for (const heading of headings) {
    for (const re of TAXONOMY_LABELS) {
      if (re.test(heading)) {
        issues.push(`[TONE-TAXON] Taxonomy label heading: "${heading}"`);
      }
    }
  }

  // Check 2: Reader-oriented section labels — headings should contain "you", "your", "when", "how", "what", "should"
  const readerOrientedRe = /\b(you|your|when|how|what|should|which|if)\b/i;
  const nonReaderHeadings = headings.filter(h => h.length > 5 && !readerOrientedRe.test(h));
  if (headings.length > 3 && nonReaderHeadings.length / headings.length > 0.7) {
    issues.push(`[TONE-HEADINGS] ${nonReaderHeadings.length}/${headings.length} headings lack reader-oriented language`);
  }

  // Check 3: Clipped declarative sentence chains (5+ consecutive sentences under 12 words)
  let clipRun = 0;
  let maxClipRun = 0;
  for (const s of sentences) {
    const words = s.split(/\s+/).length;
    if (words <= 12) {
      clipRun++;
      if (clipRun > maxClipRun) maxClipRun = clipRun;
    } else {
      clipRun = 0;
    }
  }
  if (maxClipRun >= 5) {
    issues.push(`[TONE-CLIP] Chain of ${maxClipRun} consecutive short sentences (<=12 words) — vary rhythm`);
  }

  // Check 4: Repeated noun phrases (same 3+ word phrase appearing 4+ times)
  const threeWordPhrases = {};
  const words = text.toLowerCase().split(/\s+/);
  for (let i = 0; i < words.length - 2; i++) {
    const phrase = words.slice(i, i + 3).join(' ').replace(/[^a-z\s]/g, '');
    if (phrase.length > 8) {
      threeWordPhrases[phrase] = (threeWordPhrases[phrase] || 0) + 1;
    }
  }
  const repeatedPhrases = Object.entries(threeWordPhrases)
    .filter(([, count]) => count >= 4)
    .filter(([phrase]) => !/the .+ of|and .+ the|in .+ and|for .+ and/.test(phrase)) // skip common function words
    .sort((a, b) => b[1] - a[1]);

  if (repeatedPhrases.length > 0) {
    const top3 = repeatedPhrases.slice(0, 3).map(([p, c]) => `"${p}" (${c}x)`).join(', ');
    issues.push(`[TONE-REPEAT] Repeated noun phrases: ${top3}`);
  }

  // Check 5: Abstract SaaS shorthand
  const shorthandHits = ABSTRACT_SHORTHAND.filter(s => s.re.test(text));
  if (shorthandHits.length >= 2) {
    issues.push(`[TONE-ABSTRACT] ${shorthandHits.length} abstract SaaS phrases: ${shorthandHits.map(s => s.label).join(', ')}`);
  }

  // Check 6: Lived-friction test — at least one concrete working-day scenario
  const livedFriction = /(?:email|phone|whatsapp|spreadsheet|sticky note|call|chase|P60|tax return|bank statement|deadline|January|submission|7am|monday morning|client who|clients who)/i;
  if (!livedFriction.test(text)) {
    issues.push('[TONE-FRICTION] No concrete working-day scenario found (lived-friction test fails)');
  }

  if (issues.length > 0) {
    results.push({ title, issues });
  }
}

console.log('=== HUMAN TONE CHECK ===\n');

if (results.length === 0) {
  console.log('All articles pass human tone checks.');
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
