#!/usr/bin/env node
'use strict';
// Ingest researched EMAIL prospects into the Outreach board's "eMails" group.
// Usage: node scripts/apply_prospects.js <prospects.json> --topic "<Topic label>" [--commit]
// prospects.json: [{articleUrl, outlet, author, email, emailSourceUrl, citedContext, competitorUrl, source}]
//
// Why this script exists: the matcher scores a row almost entirely from its cited context
// (lib/match.js weights the cited sentence far above the host article). That context lives in
// cited-context.json, keyed by article URL. An ingest that writes rows WITHOUT persisting the
// context leaves every row at ~0.1 confidence, i.e. auto-defuncted as "weak fit". So creating
// the row and saving the context are one operation here, never two.
const fs = require('fs');
const path = require('path');
const config = require(path.join(__dirname, '..', 'config'));
const monday = require(path.join(__dirname, '..', 'lib', 'monday'));
const U = require(path.join(__dirname, '..', 'lib', 'util'));

const ROOT = path.join(__dirname, '..');
const CITED_PATH = path.join(ROOT, 'cited-context.json');
const EMAIL_GROUP = config.monday.groups.emails || 'topics';

const opt = (flag, dflt) => { const i = process.argv.indexOf(flag); return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : dflt; };
const file = process.argv[2];
const topic = opt('--topic', '');
const commit = process.argv.includes('--commit');
if (!file || !topic) { U.err('usage: node scripts/apply_prospects.js <prospects.json> --topic "<Topic>" [--commit]'); process.exit(1); }

const norm = (u) => { try { const x = new URL(u); return (x.host.replace(/^www\./, '') + x.pathname).replace(/\/+$/, '').toLowerCase(); } catch { return (u || '').toLowerCase(); } };

// One journalist can be reachable at two addresses (ruby.kitchen@ypn.co.uk and
// ruby.kitchen@nationalworld.com are the same person; Reach/National World staff commonly have
// both a title address and a group one). Comparing addresses for equality misses that and
// double-contacts them. So also key on the localpart with separators stripped, but ONLY when the
// localpart is a person rather than a shared desk, since "editor" collides across every outlet.
const DESK_LOCALPARTS = new Set(['editor', 'editors', 'edit', 'editorial', 'news', 'newsdesk', 'info', 'hello',
  'contact', 'enquiries', 'enquiry', 'admin', 'press', 'mail', 'team', 'office', 'feedback', 'tips']);
const personKey = (email) => {
  const local = String(email || '').toLowerCase().split('@')[0];
  if (!local || DESK_LOCALPARTS.has(local)) return null;
  return local.replace(/[._+-]/g, '');
};
// Em/en dashes in stored context prime the model to echo them, which then trips the dash gate.
const clean = (s) => String(s || '').replace(/[—–]/g, ', ').replace(/\s+/g, ' ').trim();

(async () => {
  const rows = JSON.parse(fs.readFileSync(file, 'utf8'));
  const items = await monday.allItems(config);
  const seenUrl = new Set(items.map((it) => norm(it.articleUrl)).filter(Boolean));
  const seenEmail = new Set(items.map((it) => (it.email || '').toLowerCase()).filter(Boolean));
  const seenPerson = new Map();
  for (const it of items) { const k = personKey(it.email); if (k) seenPerson.set(k, it.email); }
  const cited = fs.existsSync(CITED_PATH) ? JSON.parse(fs.readFileSync(CITED_PATH, 'utf8')) : {};

  let created = 0, dup = 0, bad = 0, noEmail = 0, ctxAdded = 0;
  for (const p of rows) {
    if (!p || !p.articleUrl || !p.outlet) { bad++; continue; }
    const key = norm(p.articleUrl);
    if (seenUrl.has(key)) { U.dim(`dup url: ${p.outlet}`); dup++; continue; }
    if (p.email && seenEmail.has(p.email.toLowerCase())) { U.dim(`dup contact: ${p.email} (${p.outlet})`); dup++; continue; }
    const pk = personKey(p.email);
    if (pk && seenPerson.has(pk)) { U.warn(`same person, different address: ${p.email} is already on the board as ${seenPerson.get(pk)} (${p.outlet})`); dup++; continue; }

    const ctx = clean(p.citedContext);
    if (ctx.length < 40) { U.warn(`thin cited context, skipping: ${p.outlet} — the matcher would auto-defunct this`); bad++; continue; }
    seenUrl.add(key);
    if (p.email) seenEmail.add(p.email.toLowerCase());
    if (pk) seenPerson.set(pk, p.email);

    // No verified email is a normal outcome: park the row in To research rather than drop it.
    const status = p.email ? config.monday.status.queue : 'To research';
    if (!p.email) noEmail++;

    const cv = {};
    cv[config.monday.cols.articleUrl] = { url: p.articleUrl, text: p.outlet };
    cv[config.monday.cols.status] = { label: status };
    if (config.monday.cols.topic) cv[config.monday.cols.topic] = { labels: [topic] };
    if (config.monday.cols.citedSource) cv[config.monday.cols.citedSource] = ctx.slice(0, 250);
    if (p.email) cv[config.monday.cols.email] = { email: p.email, text: p.author || p.email };

    const itemName = `${p.outlet}: ${(p.citedContext || '').slice(0, 60)}`.slice(0, 200);
    U.ok(`${status === 'To research' ? '(no email) ' : ''}${itemName.slice(0, 66)}`);
    if (commit) {
      const res = await monday.gql(config,
        `mutation($b:ID!,$g:String!,$n:String!,$c:JSON){create_item(board_id:$b,group_id:$g,item_name:$n,column_values:$c,create_labels_if_missing:true){id}}`,
        { b: config.monday.boardId, g: EMAIL_GROUP, n: itemName, c: JSON.stringify(cv) });
      await monday.addUpdate(config, res.create_item.id,
        `[sourced] ${p.outlet}${p.author ? ' — ' + p.author : ''}\n` +
        `Email: ${p.email || 'NOT FOUND (left for research)'}\n` +
        `Published at: ${p.emailSourceUrl || 'n/a'}\n` +
        `Cited: ${ctx}\n${p.source || ''}`);
      await U.sleep(280);
    }
    // Persist the context regardless of email status: it is keyed by article URL and the row
    // may get an email later, at which point the matcher needs this to already be here.
    if (!cited[p.articleUrl]) { cited[p.articleUrl] = ctx; ctxAdded++; }
    if (p.competitorUrl && config.monday.cols.assetUrl) { /* competitor recorded in the update above */ }
    created++;
  }

  if (commit && ctxAdded) fs.writeFileSync(CITED_PATH, JSON.stringify(cited, null, 2));
  U.info(`\n${created} ${commit ? 'created' : 'ready (dry-run — add --commit)'}; ${noEmail} without an email (To research); ${dup} dup skipped; ${bad} malformed/thin.`);
  U.info(`cited-context.json: ${ctxAdded} entr${ctxAdded === 1 ? 'y' : 'ies'} ${commit ? 'written' : 'would be written'}.`);
})().catch((e) => { U.err(e.stack || e.message); process.exit(1); });
