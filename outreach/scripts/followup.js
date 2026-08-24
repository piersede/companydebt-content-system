#!/usr/bin/env node
'use strict';
// Draft LIGHT follow-up ("chase") emails to contacts who were pitched but never replied.
// A chase is a one- or two-line nudge, NOT a re-pitch. It links the same data page the
// contact was originally offered (resolved per the board Topic column), and is written to
// outbox/*.eml so it opens in Outlook via the existing review page. Never sends.
//
// Usage: node scripts/followup.js [--cap N] [--before YYYY-MM-DD] [--commit]
//   --before : only chase rows whose Last-contacted date is on/before this (default 2026-08-06;
//              keeps recent sends out — a chase needs a ~2 week gap).
//   --cap    : max drafts (default 12). Named personal emails only, one per outlet.
//   --commit : write the .eml files (otherwise dry-run: just lists who would be chased).
const fs = require('fs');
const path = require('path');
const config = require(path.join(__dirname, '..', 'config'));
const { writeEml } = require(path.join(__dirname, '..', 'lib', 'eml'));

const ROOT = path.join(__dirname, '..');
const OUTBOX = path.join(ROOT, 'outbox');
const SENT = path.join(OUTBOX, 'sent');
const opt = (f, d) => { const i = process.argv.indexOf(f); return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const CAP = parseInt(opt('--cap', '12'), 10);
const BEFORE = opt('--before', '2026-08-06');
const COMMIT = process.argv.includes('--commit');

const DESK = new Set(['editor', 'editors', 'edit', 'editorial', 'news', 'newsdesk', 'info', 'hello',
  'contact', 'enquiries', 'enquiry', 'admin', 'press', 'mail', 'team', 'office', 'feedback', 'tips',
  'production', 'support', 'stories', 'letters', 'journal', 'membership', 'newsroom']);

const envPath = fs.existsSync(path.join(ROOT, '.env')) ? path.join(ROOT, '.env') : path.join(ROOT, '..', '.env');
const key = process.env.MONDAY_API_KEY || (fs.readFileSync(envPath, 'utf8').match(/MONDAY_API_KEY\s*=\s*(.+)/) || [])[1].trim();
const B = config.monday.boardId, C = config.monday.cols;
const FOLLOWUP = 'date_mm6dej18'; // "Follow-up sent" — populated = already chased once, never chase twice

async function board() {
  let cursor = null, all = [], first = true;
  while (first || cursor) {
    first = false;
    const inner = `items{id column_values(ids:["${C.status}","${C.lastContacted}","${C.email}","${C.topic}","${FOLLOWUP}"]){id text}}`;
    const q = cursor
      ? `query{next_items_page(cursor:"${cursor}",limit:250){cursor ${inner}}}`
      : `query{boards(ids:[${B}]){items_page(limit:250){cursor ${inner}}}}`;
    const r = await fetch('https://api.monday.com/v2', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: key }, body: JSON.stringify({ query: q }) });
    const j = await r.json();
    const pg = cursor ? j.data.next_items_page : j.data.boards[0].items_page;
    all.push(...pg.items); cursor = pg.cursor;
  }
  return all;
}
const cv = (i, id) => ((i.column_values.find((c) => c.id === id) || {}).text) || '';

function originalSubject(id, email) {
  try {
    const f = fs.readdirSync(SENT).find((n) => n.startsWith(id + '_'));
    if (!f) return null;
    const m = fs.readFileSync(path.join(SENT, f), 'utf8').match(/^Subject:\s*(.+)$/m);
    return m ? m[1].trim() : null;
  } catch { return null; }
}

function chaseBody(first, url) {
  return [
    `Hi ${first},`,
    '',
    'A few weeks back I flagged our UK company-insolvency data page in case it was handy for your reporting. Just circling back once, in case it is useful for anything you are working on now. No worries at all if not.',
    '',
    `It pulls the latest official figures (Insolvency Service and Companies House) into one place, updated monthly: ${url}`,
    '',
    'Best,',
    config.sender.name,
    config.sender.title,
  ].join('\n');
}

(async () => {
  const all = await board();
  const cands = all.filter((i) => {
    if (cv(i, C.status) !== 'Contacted') return false;
    if (cv(i, FOLLOWUP)) return false; // already chased once — never double-follow-up
    const d = cv(i, C.lastContacted); if (!d || d > BEFORE) return false;
    const em = cv(i, C.email); const m = em.match(/([^-]+?)\s*-\s*([\w.+-]+@[\w.-]+)/);
    if (!m) return false;
    const local = m[2].toLowerCase().split('@')[0];
    if (DESK.has(local) || /editorial|newsdesk/.test(local)) return false; // named only
    i._name = m[1].trim(); i._email = m[2].trim(); return true;
  });
  // one per outlet (domain), keep first
  const seenDom = new Set(); const picked = [];
  for (const i of cands) {
    const dom = i._email.split('@')[1].toLowerCase();
    if (seenDom.has(dom)) continue; seenDom.add(dom);
    picked.push(i); if (picked.length >= CAP) break;
  }
  console.log(`${cands.length} chaseable named non-responders (<= ${BEFORE}); drafting ${picked.length}${COMMIT ? '' : ' (dry-run)'}\n`);
  let n = 0;
  for (const i of picked) {
    const first = i._name.split(/\s+/)[0].replace(/[^A-Za-z'-]/g, '');
    const asset = config.assetForTopic(cv(i, C.topic));
    const orig = originalSubject(i.id, i._email);
    const subject = orig ? (orig.startsWith('Re:') ? orig : 'Re: ' + orig) : 'Following up: UK insolvency data';
    console.log(`  ${i._name.padEnd(24)} ${i._email.padEnd(34)} [${cv(i, C.topic)}] -> ${asset.url.split('/data/')[1] || asset.url.slice(-30)}`);
    if (COMMIT) { writeEml(OUTBOX, { id: i.id, to: i._email, name: i._name, subject, body: chaseBody(first, asset.url) }); n++; }
  }
  if (COMMIT) console.log(`\nWrote ${n} follow-up .eml to outbox/. Run build-review.js to review.`);
})();
