'use strict';
const { slugOf, hostOf } = require('./util');

// Insolvency-statistics vocabulary. The matcher targets the SPECIFIC cited stat, not the
// article topic, so the cited sentence + the displaced (competitor) URL are weighted far
// above the host article's broad title/themes.
const STAT_TERMS = [
  'insolvency', 'insolvencies', 'liquidation', 'liquidations', 'cvl',
  "creditors' voluntary", 'creditors voluntary', 'compulsory liquidation',
  'administration', 'administrations', 'winding up', 'winding-up',
  'company failure', 'company failures', 'business failure', 'business failures',
  'corporate insolvency', 'insolvency rate', 'insolvency figures', 'insolvency statistics',
];
const NUMBER_RE = /(\d[\d,]{2,}|\d+(?:\.\d+)?\s?(?:%|per cent|percent)|\d+(?:\.\d+)?\s?(?:per\s+10,?000))/i;

const has = (text, terms) => {
  const t = (text || '').toLowerCase();
  let n = 0;
  for (const term of terms) if (t.includes(term)) n++;
  return n;
};

// candidate: { title, text, articleUrl, citedContext, competitorUrl }
// competitors: config.competitors  (dataCompetitors + citedSlugHints)
// asset: the single phase-1 data asset
function matchCandidate(candidate, asset, competitors) {
  const cited = candidate.citedContext || '';
  const compUrl = candidate.competitorUrl || '';
  const compHost = hostOf(compUrl);
  const compSlug = slugOf(compUrl);
  const title = candidate.title || '';
  const text = candidate.text || '';

  const reasons = [];
  let score = 0;

  // 1) Cited sentence carries an insolvency stat  (heaviest signal)
  const citedTerms = has(cited, STAT_TERMS);
  const citedHasNumber = NUMBER_RE.test(cited);
  if (citedTerms && citedHasNumber) { score += 0.5; reasons.push('cited sentence carries an insolvency figure'); }
  else if (citedTerms) { score += 0.22; reasons.push('cited sentence is insolvency-topical'); }

  // 2) The displaced page is an insolvency-stats source we can replace
  const hints = competitors.citedSlugHints || [];
  const slugHint = hints.some((h) => compSlug.includes(h));
  const knownCompetitor = (competitors.dataCompetitors || []).some((d) => compHost === d || compHost.endsWith('.' + d));
  if (slugHint) { score += 0.28; reasons.push(`displaced URL looks like an insolvency-stats page (${compSlug || compHost})`); }
  if (knownCompetitor) { score += 0.14; reasons.push(`displaced source is a tracked data competitor (${compHost})`); }

  // 3) Host article is at least on-topic (light supporting weight)
  const topicHits = has(`${title} ${text}`, STAT_TERMS);
  if (topicHits >= 2) { score += 0.1; reasons.push('host article is insolvency-topical'); }
  else if (topicHits === 1) { score += 0.04; }

  // Normalise by cited-stat breadth: a giant roundup page shouldn't dilute a sharp single-stat match.
  const breadthPenalty = Math.min(0.12, Math.max(0, (has(text, ['statistics', 'stats', 'roundup', 'facts and figures']) - 1) * 0.04));
  score = Math.max(0, score - breadthPenalty);

  // Content-gap classification (drives routing + email framing).
  let gap = null;
  if (citedTerms && citedHasNumber) gap = 'hard';        // clear stat to replace
  else if (citedTerms || slugHint || topicHits >= 2) gap = 'soft';

  const lowConfidence = !cited || cited.length < 40; // scraper never located the cited sentence

  return {
    asset,
    confidence: Math.min(1, Number(score.toFixed(3))),
    gap,
    citedContext: cited,
    competitor: compHost || null,
    competitorUrl: compUrl || null,
    lowConfidence,
    reasons,
  };
}

module.exports = { matchCandidate, STAT_TERMS };
