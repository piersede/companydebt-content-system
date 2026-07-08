'use strict';
const { httpFetch } = require('./util');

const EDITORIAL_HINTS = ['editor', 'writer', 'journalist', 'reporter', 'author', 'content', 'news'];

async function verify(config, email) {
  if (!config.hunter.apiKey) return { ok: false, reason: 'no HUNTER_API_KEY' };
  const url = `https://api.hunter.io/v2/email-verifier?email=${encodeURIComponent(email)}&api_key=${config.hunter.apiKey}`;
  const res = await httpFetch(url, {}, 20000);
  if (!res.json || !res.json.data) return { ok: false, reason: `verifier status ${res.status}` };
  const d = res.json.data;
  return { ok: true, email, status: d.status, score: d.score, result: d.result, disposable: d.disposable };
}

// Find a named editorial contact for a domain (optionally a known author name).
async function findContact(config, { domain, firstName, lastName }) {
  if (!config.hunter.apiKey) return { ok: false, reason: 'no HUNTER_API_KEY' };

  if (firstName && lastName) {
    const url = `https://api.hunter.io/v2/email-finder?domain=${encodeURIComponent(domain)}&first_name=${encodeURIComponent(firstName)}&last_name=${encodeURIComponent(lastName)}&api_key=${config.hunter.apiKey}`;
    const res = await httpFetch(url, {}, 20000);
    const d = res.json && res.json.data;
    if (d && d.email) {
      const v = await verify(config, d.email);
      return normalize(config, { email: d.email, name: `${firstName} ${lastName}`, position: d.position, confidence: d.score }, v);
    }
  }

  // domain search, pick the best editorial-looking person
  const url = `https://api.hunter.io/v2/domain-search?domain=${encodeURIComponent(domain)}&api_key=${config.hunter.apiKey}&limit=25`;
  const res = await httpFetch(url, {}, 20000);
  const emails = (res.json && res.json.data && res.json.data.emails) || [];
  const editorial = emails
    .filter((e) => e.type === 'personal' && e.first_name)
    .map((e) => ({ e, rank: (EDITORIAL_HINTS.some((h) => (e.position || '').toLowerCase().includes(h)) ? 2 : 0) + (e.confidence || 0) / 100 }))
    .sort((a, b) => b.rank - a.rank);
  if (!editorial.length) return { ok: false, reason: 'no named editorial contact found' };
  const best = editorial[0].e;
  const v = await verify(config, best.value);
  return normalize(config, { email: best.value, name: `${best.first_name || ''} ${best.last_name || ''}`.trim(), position: best.position, confidence: best.confidence }, v);
}

function normalize(config, c, v) {
  const verified = v.ok ? v.result === 'deliverable' || (v.score || 0) >= config.hunter.minConfidence : false;
  return {
    ok: true,
    email: c.email,
    name: c.name,
    position: c.position || '',
    confidence: c.confidence ?? (v.score || 0),
    verified,
    trusted: verified && (c.confidence ?? v.score ?? 0) >= config.hunter.minConfidence,
  };
}

module.exports = { findContact, verify };
