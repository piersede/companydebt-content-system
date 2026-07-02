'use strict';
const { normNum, hostOf } = require('./util');

// Each gate returns { pass, reason, category?, flagForHuman? }. A failed gate stops the draft
// from reaching the review queue (fail-closed). category maps to the board's Rejection-reason column.

// 1) Suppression — email or whole domain on the opt-out list.
function suppressionGate(email, suppression) {
  const e = (email || '').toLowerCase();
  const host = hostOf('http://' + e.split('@')[1] || '');
  const dom = (e.split('@')[1] || '').toLowerCase();
  if (suppression.emails && suppression.emails.map((x) => x.toLowerCase()).includes(e))
    return { pass: false, reason: `${e} is on the suppression list`, category: 'suppressed' };
  if (suppression.domains && suppression.domains.map((x) => x.toLowerCase()).some((d) => dom === d || dom.endsWith('.' + d)))
    return { pass: false, reason: `domain ${dom} is suppressed`, category: 'suppressed' };
  return { pass: true };
}

// 2) Corporate-only — free/personal inboxes are held for manual approval, never auto-drafted.
function corporateEmailGate(email, freeDomains) {
  const dom = (email || '').split('@')[1]?.toLowerCase() || '';
  if (!dom) return { pass: false, reason: 'no email domain', category: 'wrong_contact' };
  if (freeDomains.includes(dom))
    return { pass: false, reason: `${dom} is a personal/free provider — hold for manual approval`, category: 'wrong_contact', flagForHuman: true };
  return { pass: true };
}

// 3) Contact-confidence — verified, named, not a generic/role inbox, not a departed author.
function contactConfidenceGate(contact, genericLocalparts) {
  if (!contact || !contact.email) return { pass: false, reason: 'no contact email', category: 'wrong_contact' };
  const local = contact.email.split('@')[0]?.toLowerCase() || '';
  if (genericLocalparts.some((g) => local === g || local.startsWith(g + '.') || local.startsWith(g + '-')))
    return { pass: false, reason: `${contact.email} is a generic/role inbox, not a named editor`, category: 'wrong_contact' };
  if (contact.departed) return { pass: false, reason: `${contact.name || contact.email} appears to have left the publication`, category: 'wrong_contact' };
  if (contact.verified === false) return { pass: false, reason: `${contact.email} is unverified/guessed`, category: 'wrong_contact', flagForHuman: true };
  return { pass: true };
}

// --- claim ledger helpers ---
function extractStatNumbers(text) {
  const out = [];
  const re = /(\d+(?:\.\d+)?\s?%|\d{1,3}(?:,\d{3})+|\d+\.\d+|\d{3,})/g;
  let m;
  while ((m = re.exec(text)) !== null) out.push({ raw: m[0], norm: normNum(m[0]) });
  return out;
}
function buildLedger(asset) {
  const allowed = new Set();
  for (const f of asset.approvedFigures || []) {
    allowed.add(normNum(f.value));
    // also allow the delta/percent numbers stated in the note
    for (const n of extractStatNumbers(f.note || '')) allowed.add(n.norm);
  }
  for (const n of asset.allowedContextNumbers || []) allowed.add(normNum(n));
  // 4-digit years are always contextual, not statistical claims
  for (let y = 2015; y <= 2035; y++) allowed.add(String(y));
  return allowed;
}

// 4) Claim ledger — every statistical figure in the draft must be an approved figure OR the
// specific figure the article already cited (which the email legitimately contrasts against).
function claimLedgerGate(text, asset, citedContext) {
  const allowed = buildLedger(asset);
  for (const n of extractStatNumbers(citedContext || '')) allowed.add(n.norm);
  const found = extractStatNumbers(text);
  const bad = found.filter((n) => !allowed.has(n.norm) && !/^20\d{2}$|^19\d{2}$/.test(n.norm));
  if (bad.length)
    return { pass: false, reason: `unapproved figure(s): ${[...new Set(bad.map((b) => b.raw))].join(', ')}`, category: 'unapproved_figure' };
  return { pass: true };
}

// 5) Dash gate — no em/en dash anywhere (a common AI tell).
function dashGate(text) {
  if (/[–—]/.test(text)) return { pass: false, reason: 'contains an em/en dash', category: 'too_templated' };
  return { pass: true };
}

// 6) Structural-variation — fingerprint the draft, reject if too similar to a recent one.
function fingerprint(text) {
  const sentences = text.replace(/\s+/g, ' ').split(/(?<=[.!?])\s+/).filter(Boolean);
  const openers = sentences.map((s) => s.trim().toLowerCase().split(/\s+/).slice(0, 2).join(' '));
  return { openers, count: sentences.length, hasList: /(\n\s*[-*]|:\s*\n)/.test(text) };
}
function similarity(a, b) {
  const setB = new Set(b.openers);
  const overlap = a.openers.filter((o) => setB.has(o)).length;
  const denom = Math.max(a.openers.length, b.openers.length) || 1;
  return overlap / denom;
}
function variationGate(text, recentFingerprints, threshold = 0.6) {
  const fp = fingerprint(text);
  for (const prev of recentFingerprints || []) {
    if (similarity(fp, prev) >= threshold)
      return { pass: false, reason: `structurally too similar to a recent draft (${Math.round(similarity(fp, prev) * 100)}%)`, category: 'too_templated', fingerprint: fp };
  }
  return { pass: true, fingerprint: fp };
}

// 7) Citation-gap framing — the email must anchor on the cited point, not just the topic.
function citationFramingGate(text, citedContext) {
  if (!citedContext || citedContext.length < 40)
    return { pass: false, reason: 'no cited-source context was captured for this article', category: 'not_enough_citation_context', flagForHuman: true };
  return { pass: true };
}

// 8) Regulated-claim gate (CompanyDebt-specific) — no advice, no guarantees, no false
// exclusivity on official stats, no fabricated authority.
function regulatedClaimGate(text) {
  const t = text.toLowerCase();
  const rules = [
    [/\b(we|i) (can )?guarantee\b/, 'implies a guaranteed outcome'],
    [/\bwrite off (your|the) debt\b/, 'reads as debt advice'],
    [/\byou should (file|liquidate|stop paying|wind up)\b/, 'reads as insolvency advice'],
    [/\b(exclusive|proprietary|our own) (data|dataset|research|figures|statistics)\b/, 'falsely claims exclusivity on official statistics'],
    [/\bofficial (partner|source) of (the )?(insolvency service|companies house)\b/, 'fabricates an official affiliation'],
    [/\bregulated by\b/, 'makes a regulatory-status claim'],
  ];
  for (const [re, why] of rules) if (re.test(t)) return { pass: false, reason: why, category: 'regulated_claim' };
  return { pass: true };
}

module.exports = {
  suppressionGate, corporateEmailGate, contactConfidenceGate,
  claimLedgerGate, dashGate, variationGate, citationFramingGate, regulatedClaimGate,
  fingerprint, extractStatNumbers, buildLedger,
};
