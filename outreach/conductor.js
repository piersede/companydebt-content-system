#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');
const config = require('./config');
const U = require('./lib/util');
const { Store } = require('./lib/state');
const monday = require('./lib/monday');
const { scrape } = require('./lib/scraper');
const { matchCandidate } = require('./lib/match');
const { findContact } = require('./lib/enrich');
const { createDraft } = require('./lib/graph');
const { writeEml } = require('./lib/eml');
const { draft } = require('./lib/claude');
const G = require('./lib/gates');

const args = process.argv.slice(2);
const cmd = args[0];
const flag = (name) => args.includes(name);
const opt = (name, d) => { const i = args.indexOf(name); return i >= 0 && args[i + 1] ? args[i + 1] : d; };

function splitName(full) {
  const parts = (full || '').trim().split(/\s+/);
  return { firstName: parts[0] || '', lastName: parts.slice(1).join(' ') || '' };
}

// ---------- guardrail runner (draft-quality gates) ----------
function runDraftGates(text, asset, citedContext, recentFingerprints) {
  const checks = [
    G.dashGate(text),
    G.claimLedgerGate(text, asset, citedContext),
    G.citationFramingGate(text, citedContext),
    G.regulatedClaimGate(text),
    G.variationGate(text, recentFingerprints),
  ];
  const failed = checks.find((c) => !c.pass);
  const fp = checks[checks.length - 1].fingerprint;
  return { pass: !failed, failed, fingerprint: fp };
}

// ---------- SCAN ----------
async function scan() {
  const process_ = flag('--process');
  const cap = parseInt(opt('--cap', config.dailyCap), 10);
  const statusLabel = opt('--status', config.monday.status.queue);
  const write = config.review === 'write' && process_;
  const store = new Store(config.stateDir);
  const tally = {};

  U.info(`\nconductor scan  [phase ${config.phase} / ${config.mode}]`);
  U.dim(`mode=${process_ ? 'process' : 'dry-run'}  review=${config.review}  cap=${cap}  writes=${write ? 'ON' : 'off'}\n`);

  let items;
  try { items = await monday.itemsByStatus(config, statusLabel); }
  catch (e) { U.err(`Cannot read Monday board: ${e.message}`); U.dim('Set OUTREACH_BOARD_ID + column ids (see `conductor boardcols`).'); return; }

  U.info(`${items.length} item(s) in "${statusLabel}".`);
  let drafted = 0;
  const draftedContacts = new Set(); // one draft per contact email per run

  for (const item of items) {
    U.log('');
    U.log(`${U.C.bold}• ${item.name}${U.C.reset}  (id ${item.id})`);

    if (drafted >= cap) { U.warn('  daily cap reached — leaving in queue for next run'); continue; }

    const articleUrl = item.articleUrl || item.raw?.link?.text;
    if (!articleUrl) { await route(item, 'research', 'no article URL on the row', 'not_enough_citation_context', { write, tally }); continue; }

    // 1) scrape (with a free fallback to the Ahrefs-captured cited sentence)
    const storedCtx = config.citedContext[articleUrl] || config.citedContext[articleUrl.replace(/\/$/, '')] || '';
    const sc = await scrape(articleUrl, config);
    let title, text, citedContext, competitorLinks;
    if (sc.ok) {
      ({ title, text, competitorLinks } = sc);
      citedContext = sc.citedContext || storedCtx;
    } else if (sc.blocked && storedCtx) {
      // page blocked but Ahrefs gave us the cited sentence — draft from that instead of halting
      title = item.name; text = storedCtx; citedContext = storedCtx; competitorLinks = [];
      U.dim(`  (page blocked; using Ahrefs cited context)`);
    } else if (sc.blocked) {
      await route(item, 'blocked', `page blocked: ${sc.error}`, null, { write, tally }); continue;
    } else {
      await route(item, 'research', `scrape failed: ${sc.error}`, 'not_enough_citation_context', { write, tally }); continue;
    }

    // 2) match on the specific cited stat
    const competitorUrl = item.citedSource || (competitorLinks && competitorLinks[0]) || '';
    const m = matchCandidate({ title, text, articleUrl, citedContext, competitorUrl }, config.catalogue.assets[0], config.competitors);
    U.dim(`  match: conf ${m.confidence}  gap ${m.gap || 'none'}  ${m.reasons[0] || ''}`);
    if (!m.gap || m.confidence < config.matchThreshold) { await route(item, 'defunct', `weak fit (conf ${m.confidence})`, 'weak_fit', { write, tally }); continue; }

    // 3) contact (board email first, else enrich)
    let contact = item.email ? { email: item.email, name: item.emailName || '', verified: true } : null;
    if (!contact) {
      const host = U.hostOf(articleUrl);
      const enr = config.hunter.apiKey ? await findContact(config, { domain: host }) : { ok: false, reason: 'no HUNTER_API_KEY' };
      if (enr.ok && enr.trusted) contact = { email: enr.email, name: enr.name, position: enr.position, verified: enr.verified };
      else { await route(item, 'research', `no verified contact (${enr.reason || 'low confidence'})`, 'wrong_contact', { write, tally }); continue; }
    }

    // contact gates (fail-closed, BEFORE drafting)
    const cg = [G.suppressionGate(contact.email, config.suppression),
      G.corporateEmailGate(contact.email, config.freeEmailDomains),
      G.contactConfidenceGate(contact, config.genericInboxLocalparts)].find((c) => !c.pass);
    if (cg) { await route(item, 'research', cg.reason, cg.category, { write, tally }); continue; }

    // per-contact dedup: never draft the same person twice in one run (sister titles, repeat authors)
    const cemail = (contact.email || '').toLowerCase();
    if (draftedContacts.has(cemail)) { U.warn(`  → skipped: ${contact.email} already drafted this run (stays queued for next run)`); continue; }

    // 4) draft
    if (!process_) { draftedContacts.add(cemail); U.ok('  would draft (dry-run)'); continue; }
    const article = { title, url: articleUrl, publication: U.hostOf(articleUrl) };
    const d = await draft(config, { asset: m.asset, article, match: m, contact });
    if (!d.ok) { U.warn(`  draft skipped: ${d.reason}`); continue; }

    // 5) draft-quality gates
    const gateRes = runDraftGates(`${d.subject}\n${d.body}`, m.asset, m.citedContext, store.recentFingerprints());
    if (!gateRes.pass) { await route(item, 'research', `draft gate failed: ${gateRes.failed.reason}`, gateRes.failed.category, { write, tally }); U.warn(`  ✗ ${gateRes.failed.reason}`); continue; }

    // 6) passed — Outlook draft + board
    U.ok(`  ✓ draft passes all gates`);
    U.log(`  ${U.C.dim}Subject:${U.C.reset} ${d.subject}`);
    U.log(d.body.split('\n').map((l) => '  | ' + l).join('\n'));

    store.pushFingerprint(gateRes.fingerprint);
    store.setStage(item.id, 'drafted', { subject: d.subject, to: contact.email });
    draftedContacts.add(cemail);
    drafted++;

    if (write) {
      // .eml draft (open-and-send in Outlook, no cloud). Graph only if it's actually configured.
      const emlPath = writeEml(config.outboxDir, { id: item.id, to: contact.email, name: contact.name, subject: d.subject, body: d.body });
      let outlook = `Draft file: ${emlPath}`;
      if (config.graph.clientId) {
        const gr = await createDraft(config, { to: contact.email, subject: d.subject, body: d.body, name: contact.name });
        outlook += gr.ok ? `\nOutlook: drafted ${gr.webLink || gr.id}` : `\nOutlook: ${gr.reason}`;
      }
      const note = `Outreach draft (${config.sender.name || 'sender'}):\n\nTo: ${contact.email}\nSubject: ${d.subject}\n\n${d.body}\n\n[${outlook}]`;
      await monday.addUpdate(config, item.id, note);
      // (email is already on the row; asset URL is constant — no need to re-write those complex columns)
      if (config.monday.cols.citedSource && m.competitorUrl) await monday.setSimple(config, item.id, config.monday.cols.citedSource, m.competitorUrl);
      await monday.setStatus(config, item.id, config.monday.status.ready);
      U.ok('  → board: Ready to contact');
    } else {
      U.dim('  (review=print — not written to board/Outlook)');
    }
  }

  store.data.lastRun = new Date().toISOString();
  store.save();
  U.log('');
  U.info(`Done. Drafted ${drafted}/${cap}.`);
  const tallyKeys = Object.keys(tally);
  if (tallyKeys.length) { U.info('Rejection tally:'); tallyKeys.sort().forEach((k) => U.log(`  ${k}: ${tally[k]}`)); }
  if (drafted >= cap && items.length > drafted) U.warn(`Run capped — ${items.length - drafted} left in queue.`);
}

// route an item to a non-draft outcome
async function route(item, kind, reason, category, { write, tally }) {
  const map = {
    research: config.monday.status.research,
    blocked: config.monday.status.queue,   // stay in queue, add a note
    defunct: config.monday.status.defunct,
  };
  const label = map[kind];
  const line = { research: 'To research', blocked: 'blocked (stays in queue)', defunct: 'Defunct / skip' }[kind];
  U.warn(`  → ${line}: ${reason}`);
  if (category) tally[category] = (tally[category] || 0) + 1;
  if (write) {
    try {
      await monday.addUpdate(config, item.id, `[conductor] ${reason}${category ? ` (suggested reason: ${category})` : ''}`);
      if (kind !== 'blocked') await monday.setStatus(config, item.id, label);
      if (category && config.monday.cols.rejectReason) await monday.setSimple(config, item.id, config.monday.cols.rejectReason, category);
      if (kind === 'defunct') await monday.moveToGroup(config, item.id, config.monday.groups.defunct);
    } catch (e) { U.err(`  (board write failed: ${e.message})`); }
  }
}

// ---------- SOURCE (Ahrefs CSV -> board rows) ----------
function parseCsv(text) {
  const rows = []; let row = [], field = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; } else field += c; }
    else if (c === '"') q = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else if (c !== '\r') field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.some((x) => x.trim()));
}

async function source() {
  const csvPath = args[1];
  const commit = flag('--commit');
  if (!csvPath) { U.err('usage: conductor source <ahrefs-backlinks.csv> [--commit]'); return; }
  const rows = parseCsv(fs.readFileSync(csvPath, 'utf8'));
  const header = rows.shift().map((h) => h.trim().toLowerCase());
  // Prefer an exact header match, then fall back to a substring match, so a loose name like
  // "referring page" can't hijack "referring page title" ahead of "referring page url".
  const col = (...names) => {
    for (const n of names) { const i = header.findIndex((h) => h === n); if (i >= 0) return i; }
    for (const n of names) { const i = header.findIndex((h) => h.includes(n)); if (i >= 0) return i; }
    return -1;
  };
  const iRef = col('referring page url', 'source url', 'url from', 'referring url');
  const iTarget = col('target url', 'url to');
  const iDR = col('domain rating', 'dr');
  const iTitle = col('referring page title', 'page title', 'title');
  const iPageType = col('page type');
  if (iRef < 0) { U.err('could not find a "Referring page URL" column'); U.dim('headers: ' + header.join(' | ')); return; }
  const articlesOnly = flag('--articles-only');

  let existing = new Set();
  try { (await monday.allItems(config)).forEach((it) => { if (it.articleUrl) existing.add(it.articleUrl.trim()); }); }
  catch (e) { U.warn(`(could not dedup against board: ${e.message})`); }

  const own = ['companydebt.com', 'comdebstage.wpengine.com'];
  const seen = new Set(); const candidates = [];
  for (const r of rows) {
    const ref = (r[iRef] || '').trim();
    if (!ref) continue;
    const host = U.hostOf(ref);
    const dr = iDR >= 0 ? parseFloat(r[iDR]) : NaN;
    if (own.some((o) => host === o || host.endsWith('.' + o))) continue;
    if (config.suppression.domains.some((d) => host === d || host.endsWith('.' + d))) continue;
    if (!Number.isNaN(dr) && dr < config.minDR) continue;
    if (articlesOnly && iPageType >= 0 && !(r[iPageType] || '').toLowerCase().includes('article')) continue;
    if (seen.has(ref) || existing.has(ref)) continue;
    seen.add(ref);
    candidates.push({ ref, target: iTarget >= 0 ? (r[iTarget] || '').trim() : '', title: iTitle >= 0 ? (r[iTitle] || '').trim() : '', dr });
  }

  // strongest first, so --one-per-domain and --limit keep the best
  candidates.sort((a, b) => (Number(b.dr) || 0) - (Number(a.dr) || 0));
  if (flag('--one-per-domain')) {
    const byHost = new Set(); const dedup = [];
    for (const c of candidates) { const h = U.hostOf(c.ref); if (byHost.has(h)) continue; byHost.add(h); dedup.push(c); }
    candidates.length = 0; candidates.push(...dedup);
  }
  const lim = parseInt(opt('--limit', '0'), 10);
  if (lim > 0 && candidates.length > lim) candidates.length = lim;

  U.info(`\nSource: ${candidates.length} new candidate(s) after DR>=${config.minDR}, own-site, suppression + dedup${flag('--one-per-domain') ? ', one-per-domain' : ''}${lim > 0 ? `, capped ${lim}` : ''}.`);
  candidates.slice(0, 40).forEach((c) => U.log(`  DR${Number.isNaN(c.dr) ? '?' : c.dr}  ${c.ref}  ${U.C.dim}→ cites ${c.target || '?'}${U.C.reset}`));
  if (candidates.length > 40) U.dim(`  ... and ${candidates.length - 40} more`);
  if (!commit) { U.dim('\n(dry-run — pass --commit to create board rows)'); return; }

  let created = 0, failed = 0;
  for (const c of candidates) {
    const cv = {};
    if (config.monday.cols.articleUrl) cv[config.monday.cols.articleUrl] = { url: c.ref, text: c.ref };
    if (config.monday.cols.citedSource && c.target) cv[config.monday.cols.citedSource] = c.target;
    if (config.monday.cols.status) cv[config.monday.cols.status] = { label: config.monday.status.queue };
    try { await monday.createItem(config, c.title || c.ref, cv); created++; }
    catch (e) { failed++; U.err(`  create failed for ${c.ref}: ${e.message}`); await U.sleep(1500); }
    await U.sleep(220); // throttle under Monday's mutation rate limit on bulk loads
    if (created && created % 100 === 0) U.dim(`  ...${created} created`);
  }
  U.ok(`Created ${created} row(s) in "${config.monday.status.queue}"${failed ? ` (${failed} failed — re-run to retry, board-dedup skips existing)` : ''}.`);
}

// ---------- RETRY / REJECT ----------
async function retry() {
  const id = args[1];
  if (!id) { U.err('usage: conductor retry <itemId>'); return; }
  const store = new Store(config.stateDir); store.clearItem(id); store.save();
  U.ok(`Cleared local checkpoint for ${id}. Re-run \`scan --process\` (it re-pulls the board, so a new email takes effect).`);
}
async function reject() {
  const id = args[1]; const category = args[2];
  if (!id || !category) { U.err('usage: conductor reject <itemId> <category>'); U.dim('categories: ' + config.rejectionCategories.join(', ')); return; }
  if (!config.rejectionCategories.includes(category)) { U.err(`invalid category "${category}"`); U.dim('valid: ' + config.rejectionCategories.join(', ')); return; }
  if (config.review !== 'write') { U.warn('OUTREACH_REVIEW is not "write" — printing only.'); U.log(`would set rejection reason of ${id} to ${category}`); return; }
  if (config.monday.cols.rejectReason) await monday.setSimple(config, id, config.monday.cols.rejectReason, category);
  await monday.addUpdate(config, id, `[reject] ${category}`);
  U.ok(`Set rejection reason of ${id} to ${category}.`);
}

async function boardcols() {
  try { const b = await monday.boardColumns(config); U.info(`\nBoard: ${b.name} (${config.monday.boardId})`); b.columns.forEach((c) => U.log(`  ${c.id}  ${U.C.dim}${c.type}${U.C.reset}  ${c.title}`)); }
  catch (e) { U.err(e.message); }
}

// ---------- SELFTEST (offline; no keys) ----------
function assert(name, cond) { U.log(`  ${cond ? U.C.green + '✓' : U.C.red + '✗'} ${name}${U.C.reset}`); if (!cond) process.exitCode = 1; }
function selftest() {
  U.info('\nselftest (offline)\n');
  const asset = config.catalogue.assets[0];

  U.log('matcher:');
  const strong = matchCandidate({ title: 'UK firms collapse', text: 'insolvency figures show liquidations rising', citedContext: 'Company insolvencies hit 2,000 in the latest month according to figures.', competitorUrl: 'https://redflagalert.com/insolvency-statistics/' }, asset, config.competitors);
  assert('cited insolvency stat -> hard gap, above threshold', strong.gap === 'hard' && strong.confidence >= config.matchThreshold);
  const off = matchCandidate({ title: 'Best CRM software', text: 'a roundup of CRM tools', citedContext: 'The best CRM is easy to use.', competitorUrl: 'https://example.com/crm/' }, asset, config.competitors);
  assert('off-topic -> no gap / skip', !off.gap || off.confidence < config.matchThreshold);

  U.log('gates:');
  assert('dash gate rejects em dash', !G.dashGate('we have data — fresher').pass);
  assert('dash gate passes clean text', G.dashGate('we have fresher data').pass);
  assert('claim ledger accepts approved 1,868', G.claimLedgerGate('there were 1,868 insolvencies', asset).pass);
  assert('claim ledger rejects invented 70%', !G.claimLedgerGate('CVLs were 70% of cases', asset).pass);
  assert('claim ledger accepts approved 76%', G.claimLedgerGate('CVLs were 76% of the total', asset).pass);
  assert('claim ledger allows a year (2026)', G.claimLedgerGate('the May 2026 figures', asset).pass);
  assert('regulated gate rejects guarantee', !G.regulatedClaimGate('we can guarantee a better outcome').pass);
  assert('regulated gate rejects false exclusivity', !G.regulatedClaimGate('our exclusive data shows').pass);
  assert('regulated gate passes clean pitch', G.regulatedClaimGate('our page has the latest monthly figures').pass);
  assert('corporate gate holds gmail', !G.corporateEmailGate('jo@gmail.com', config.freeEmailDomains).pass);
  assert('corporate gate passes a masthead', G.corporateEmailGate('jo@thetimes.co.uk', config.freeEmailDomains).pass);
  assert('contact gate rejects info@ inbox', !G.contactConfidenceGate({ email: 'info@thetimes.co.uk' }, config.genericInboxLocalparts).pass);
  assert('suppression gate blocks own domain', !G.suppressionGate('x@companydebt.com', config.suppression).pass);
  assert('citation framing flags empty context', !G.citationFramingGate('body', '').pass);

  U.log('variation:');
  const a = 'We track UK insolvency. Your figure looks dated. Ours is monthly. Worth a look.';
  const fpA = G.fingerprint(a);
  assert('identical draft is rejected by variation gate', !G.variationGate(a, [fpA]).pass);
  assert('fresh draft passes variation gate', G.variationGate('Different opener entirely. New structure here. Another point. Final line.', [fpA]).pass);

  U.log('');
  U.info(process.exitCode ? 'selftest FAILED' : 'selftest passed');
}

function help() {
  U.log(`
CompanyDebt outreach conductor  (auto-draft, human-send)

  node conductor.js selftest              offline checks (matcher + gates), no keys needed
  node conductor.js boardcols             print the Outreach board's column ids (needs OUTREACH_BOARD_ID)
  node conductor.js source <csv> [--commit]   ingest an Ahrefs backlinks export -> "Not started" rows
  node conductor.js scan [--process] [--cap N] [--status "Not started"]
                                          daily run. no --process = dry-run routing preview.
                                          writes to the board only when OUTREACH_REVIEW=write AND --process.
  node conductor.js retry <itemId>        clear a local checkpoint and re-queue
  node conductor.js reject <itemId> <category>   set the board Rejection-reason column

  phase ${config.phase} / ${config.mode}   review=${config.review}   cap=${config.dailyCap}
`);
}

(async () => {
  try {
    switch (cmd) {
      case 'scan': return await scan();
      case 'source': return await source();
      case 'retry': return await retry();
      case 'reject': return await reject();
      case 'boardcols': return await boardcols();
      case 'selftest': return selftest();
      default: return help();
    }
  } catch (e) { U.err('fatal: ' + (e.stack || e.message || e)); process.exitCode = 1; }
})();
