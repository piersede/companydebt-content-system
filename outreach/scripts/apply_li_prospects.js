#!/usr/bin/env node
'use strict';
// Ingest LinkedIn prospects (harvested from LinkedIn content-search + engager-mining) into the
// Outreach board's "LinkedIn Outreach" group.
// Usage: node scripts/apply_li_prospects.js <prospects.json> [--commit] [--group <id>]
//   --group defaults to the insolvency LinkedIn group; pass e.g. group_mm53fmpj for pub.
// prospects.json: [{name, profileUrl, headline, hook, source}]
// Dedups by normalized LinkedIn profile URL against existing rows' "LinkedIn URL" column.
const fs = require('fs');
const path = require('path');
const config = require(path.join(__dirname, '..', 'config'));
const monday = require(path.join(__dirname, '..', 'lib', 'monday'));
const U = require(path.join(__dirname, '..', 'lib', 'util'));

const LI_URL_COL = 'link_mm52fh94';           // "LinkedIn URL" (link) column
const gi = process.argv.indexOf('--group');
const LI_GROUP = (gi > -1 && process.argv[gi + 1]) || config.monday.groups.linkedin || 'group_mm52mctc';

const file = process.argv[2];
const commit = process.argv.includes('--commit');
if (!file) { U.err('usage: node scripts/apply_li_prospects.js <prospects.json> [--commit]'); process.exit(1); }

// normalize a LinkedIn profile URL for dedup: host+/in/slug, lowercased, no query/trailing slash
const norm = (u) => {
  try { const x = new URL(u); return ('linkedin.com' + x.pathname).replace(/\/+$/, '').toLowerCase(); }
  catch { return (u || '').trim().toLowerCase().replace(/[?#].*$/, '').replace(/\/+$/, ''); }
};

async function existingLiUrls() {
  // pull every item's LinkedIn URL column value so we don't create duplicates
  const q = `query ($b:ID!, $cursor:String) {
    boards(ids:[$b]) { items_page(limit:200, cursor:$cursor) {
      cursor items { id column_values(ids:["${LI_URL_COL}"]) { id value } } } } }`;
  const set = new Set(); let cursor = null;
  do {
    const data = await monday.gql(config, q, { b: config.monday.boardId, cursor });
    const page = data.boards[0].items_page;
    for (const it of page.items) {
      const cv = it.column_values[0];
      if (cv && cv.value) { try { const v = JSON.parse(cv.value); if (v && v.url) set.add(norm(v.url)); } catch { /* skip */ } }
    }
    cursor = page.cursor;
  } while (cursor);
  return set;
}

(async () => {
  const prospects = JSON.parse(fs.readFileSync(file, 'utf8'));
  const seen = await existingLiUrls();
  const batchSeen = new Set();

  let created = 0, dup = 0, bad = 0;
  for (const p of prospects) {
    if (!p || !p.profileUrl || !p.name) { bad++; continue; }
    const key = norm(p.profileUrl);
    if (seen.has(key) || batchSeen.has(key)) { dup++; continue; }
    batchSeen.add(key);
    const cv = {};
    cv[LI_URL_COL] = { url: p.profileUrl, text: `${p.name} LinkedIn` };
    if (config.monday.cols.citedSource) cv[config.monday.cols.citedSource] = (p.hook || '').slice(0, 250);
    if (config.monday.cols.notes) cv[config.monday.cols.notes] =
      `${p.headline || ''}\n\nWhy relevant: ${p.hook || ''}\nFound via: ${p.source || 'LinkedIn'}`.trim();
    cv[config.monday.cols.status] = { label: config.monday.status.queue };
    const itemName = p.headline ? `${p.name} — ${p.headline}`.slice(0, 200) : p.name;
    U.ok(`${itemName.slice(0, 70)}  ${p.profileUrl}`);
    if (commit) {
      await monday.gql(config,
        `mutation($b:ID!,$g:String!,$n:String!,$c:JSON){create_item(board_id:$b,group_id:$g,item_name:$n,column_values:$c){id}}`,
        { b: config.monday.boardId, g: LI_GROUP, n: itemName, c: JSON.stringify(cv) });
      await U.sleep(280);
    }
    created++;
  }
  U.info(`\n${created} ${commit ? 'created' : 'ready (dry-run — add --commit)'}; ${dup} dup skipped; ${bad} malformed.`);
})().catch((e) => { U.err(e.stack || e.message); process.exit(1); });
