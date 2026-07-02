#!/usr/bin/env node
'use strict';
// Apply researched contacts to the Outreach board.
// Usage: node scripts/apply_contacts.js <contacts.json> [--commit]
// contacts.json: [{articleUrl, publication, contactName, position, email, emailSourceUrl, authorStillThere, notes}]
// Matches each entry to a board row by article URL (exact, then host+path prefix), writes the
// Contact email column and an update note recording where the email was published.
const fs = require('fs');
const path = require('path');
const config = require(path.join(__dirname, '..', 'config'));
const monday = require(path.join(__dirname, '..', 'lib', 'monday'));
const U = require(path.join(__dirname, '..', 'lib', 'util'));

const file = process.argv[2];
const commit = process.argv.includes('--commit');
if (!file) { U.err('usage: node scripts/apply_contacts.js <contacts.json> [--commit]'); process.exit(1); }

const norm = (u) => { try { const x = new URL(u); return (x.host.replace(/^www\./, '') + x.pathname).replace(/\/+$/, '').toLowerCase(); } catch { return (u || '').toLowerCase(); } };

(async () => {
  const contacts = JSON.parse(fs.readFileSync(file, 'utf8'));
  const items = await monday.itemsByStatus(config, config.monday.status.queue);
  const byUrl = new Map(items.map((it) => [norm(it.articleUrl), it]));

  let applied = 0, skipped = 0;
  for (const c of contacts) {
    const key = norm(c.articleUrl);
    const item = byUrl.get(key) || items.find((it) => norm(it.articleUrl).startsWith(key) || key.startsWith(norm(it.articleUrl)));
    if (!item) { U.warn(`no board row for ${c.articleUrl}`); skipped++; continue; }
    if (!c.email) { U.dim(`no email found for ${c.publication} (${c.notes || 'no notes'}) — leaving for To research`); skipped++; continue; }
    U.ok(`${item.name.slice(0, 50)}  ←  ${c.contactName || '?'} <${c.email}>${c.position ? ' (' + c.position + ')' : ''}`);
    if (commit) {
      await monday.setSimple(config, item.id, config.monday.cols.email, `${c.email} ${c.contactName || ''}`.trim());
      await monday.addUpdate(config, item.id,
        `[contact research] ${c.contactName || 'contact'}${c.position ? ', ' + c.position : ''} — ${c.email}\n` +
        `Published at: ${c.emailSourceUrl || 'n/a'}\nAuthor still there: ${c.authorStillThere}\n${c.notes || ''}`);
      await U.sleep(250);
    }
    applied++;
  }
  U.info(`\n${applied} contact(s) ${commit ? 'applied' : 'ready (dry-run — add --commit)'}; ${skipped} skipped.`);
})().catch((e) => { U.err(e.stack || e.message); process.exit(1); });
