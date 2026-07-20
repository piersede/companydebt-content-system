#!/usr/bin/env node
'use strict';
// Crawl article + outlet contact pages for PUBLISHED email addresses, decoding Cloudflare
// obfuscation. Does NOT write to the board: it emits a review file for a human to verify, then
// apply. Reads the outlet's OWN markup only (mailto links, cfemail hashes, on-page addresses) --
// no aggregators, no naming-convention guesses.
//
// Usage: node scripts/crawl_emails.js <worklist.json> <out.json> [--limit N] [--concurrency N]
//   worklist.json: [{articleUrl, outlet, author}]  (author optional; used only to rank matches)
const fs = require('fs');

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
const arg = (f, d) => { const i = process.argv.indexOf(f); return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const worklistPath = process.argv[2];
const outPath = process.argv[3];
const LIMIT = parseInt(arg('--limit', '0'), 10);
const CONC = parseInt(arg('--concurrency', '4'), 10);
if (!worklistPath || !outPath) { console.error('usage: node scripts/crawl_emails.js <worklist.json> <out.json> [--limit N] [--concurrency N]'); process.exit(1); }

// --- email extraction -------------------------------------------------------
function decodeCfemail(hex) {
  try {
    const r = parseInt(hex.substr(0, 2), 16);
    let s = '';
    for (let i = 2; i < hex.length; i += 2) s += String.fromCharCode(parseInt(hex.substr(i, 2), 16) ^ r);
    return s;
  } catch { return ''; }
}
// noise we never want to report as a contact
const JUNK_DOMAINS = /(sentry|wixpress|example\.com|\.png|\.jpg|\.gif|\.svg|\.webp|schema\.org|w3\.org|googleapis|gstatic|cloudflare|jsdelivr|gravatar|\.local|localhost|domain\.com|email\.com|yourdomain|sentry\.io|2x)/i;
const JUNK_LOCAL = /^(noreply|no-reply|donotreply|do-not-reply|postmaster|abuse|dmarc|wordpress|user|name|email|your|test|example|hostmaster|webmaster@sentry)/i;
const EMAIL_RE = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;

function extractEmails(html) {
  const found = new Map(); // email -> Set(methods)
  const add = (e, method) => {
    e = (e || '').trim().replace(/^mailto:/i, '').split('?')[0].toLowerCase();
    if (!e || !/@/.test(e)) return;
    if (JUNK_DOMAINS.test(e) || JUNK_LOCAL.test(e)) return;
    if (e.length > 70) return;
    if (!found.has(e)) found.set(e, new Set());
    found.get(e).add(method);
  };
  // 1) mailto links
  for (const mm of html.matchAll(/mailto:([^"'>\s?]+)/gi)) add(mm[1], 'mailto');
  // 2) Cloudflare: <span data-cfemail="HASH"> and href="/cdn-cgi/l/email-protection#HASH"
  for (const mm of html.matchAll(/data-cfemail="([0-9a-fA-F]+)"/g)) { const d = decodeCfemail(mm[1]); if (d) add(d, 'cfemail'); }
  for (const mm of html.matchAll(/email-protection#([0-9a-fA-F]+)/g)) { const d = decodeCfemail(mm[1]); if (d) add(d, 'cfemail'); }
  // 3) raw addresses in the markup (lowest trust; still the outlet's own page)
  for (const mm of (html.match(EMAIL_RE) || [])) add(mm, 'raw');
  return found;
}

async function fetchHtml(url) {
  try {
    const r = await fetch(url, {
      headers: { 'User-Agent': UA, Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-GB,en;q=0.9' },
      redirect: 'follow', signal: AbortSignal.timeout(20000),
    });
    if (!r.ok) return { ok: false, status: r.status, html: '' };
    return { ok: true, status: r.status, html: await r.text(), finalUrl: r.url };
  } catch (e) { return { ok: false, status: 0, err: e.message, html: '' }; }
}

const contactPaths = ['/contact', '/contact-us', '/contactus', '/contact-us/', '/about', '/about-us', '/our-team', '/team', '/meet-the-team', '/staff', '/contacts', '/the-team', '/people'];
const origin = (u) => { try { return new URL(u).origin; } catch { return ''; } };

// rank a candidate email against the known author name
function scoreEmail(email, methods, page, author) {
  const local = email.split('@')[0].toLowerCase();
  const domain = email.split('@')[1] || '';
  let s = 0;
  const notes = [];
  if (methods.has('mailto')) { s += 3; notes.push('mailto'); }
  if (methods.has('cfemail')) { s += 3; notes.push('cfemail-decoded'); }
  if (methods.has('raw') && !methods.has('mailto') && !methods.has('cfemail')) { s += 1; notes.push('raw-markup'); }
  if (page === 'article') { s += 2; notes.push('on-article'); } else { notes.push('on-contact-page'); }
  // author-name match against the localpart
  if (author) {
    const parts = author.toLowerCase().split(/\s+/).filter((p) => p.length > 2);
    const surname = parts[parts.length - 1] || '';
    const first = parts[0] || '';
    if (surname && local.includes(surname)) { s += 4; notes.push('surname-match'); }
    if (first && surname && (local.includes(first) && local.includes(surname))) { s += 2; notes.push('firstname+surname'); }
    else if (first && local.startsWith(first) && local.length <= first.length + 2) { s += 1; }
  }
  const deskish = /^(editor|editorial|news|newsdesk|newsroom|hello|team|contact|info|enquiries|press|mail|office|tips|edit)/i.test(local);
  if (deskish) notes.push('desk-address');
  return { email, domain, score: s, deskish, notes: [...new Set(notes)] };
}

async function processRow(row) {
  const out = { articleUrl: row.articleUrl, outlet: row.outlet, author: row.author || '', candidates: [], pagesTried: [] };
  const seen = new Map(); // email -> {methods,page}
  // article page first (address here is tied to the author)
  const art = await fetchHtml(row.articleUrl);
  out.pagesTried.push({ url: row.articleUrl, status: art.status });
  if (art.ok) for (const [e, methods] of extractEmails(art.html)) if (!seen.has(e)) seen.set(e, { methods, page: 'article' });
  // outlet contact/team pages
  const orig = origin(art.finalUrl || row.articleUrl);
  if (orig) {
    for (const p of contactPaths) {
      const cu = orig + p;
      const r = await fetchHtml(cu);
      if (r.status) out.pagesTried.push({ url: cu, status: r.status });
      if (r.ok && r.html) {
        for (const [e, methods] of extractEmails(r.html)) {
          if (seen.has(e)) { for (const m of methods) seen.get(e).methods.add(m); }
          else seen.set(e, { methods, page: 'contact' });
        }
      }
      await new Promise((res) => setTimeout(res, 120));
    }
  }
  const scored = [];
  for (const [e, info] of seen) scored.push(scoreEmail(e, info.methods, info.page, row.author));
  scored.sort((a, b) => b.score - a.score);
  out.candidates = scored.slice(0, 8);
  return out;
}

(async () => {
  let work = JSON.parse(fs.readFileSync(worklistPath, 'utf8'));
  if (LIMIT) work = work.slice(0, LIMIT);
  const results = [];
  let idx = 0;
  async function worker() {
    while (idx < work.length) {
      const my = idx++;
      const row = work[my];
      process.stderr.write(`[${my + 1}/${work.length}] ${row.outlet}\n`);
      try { results[my] = await processRow(row); }
      catch (e) { results[my] = { articleUrl: row.articleUrl, outlet: row.outlet, error: e.message, candidates: [] }; }
    }
  }
  await Promise.all(Array.from({ length: Math.min(CONC, work.length) }, worker));
  fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
  const hits = results.filter((r) => r.candidates && r.candidates.length).length;
  const strong = results.filter((r) => r.candidates && r.candidates[0] && r.candidates[0].score >= 7).length;
  console.log(`\nDone. ${results.length} rows crawled; ${hits} with >=1 candidate; ${strong} with a strong top candidate (score>=7).`);
  console.log(`Review file: ${outPath}`);
})().catch((e) => { console.error(e.stack || e.message); process.exit(1); });
