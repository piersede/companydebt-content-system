'use strict';
const { httpFetch } = require('./util');

class MondayError extends Error {}

async function gql(config, query, variables = {}) {
  if (!config.monday.apiKey) throw new MondayError('MONDAY_API_KEY is not set');
  const res = await httpFetch(config.monday.endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: config.monday.apiKey,
      'API-Version': config.monday.apiVersion,
    },
    body: JSON.stringify({ query, variables }),
  }, 30000);
  if (!res.json) throw new MondayError(`Monday returned non-JSON (status ${res.status})`);
  if (res.json.errors) throw new MondayError('Monday GraphQL error: ' + JSON.stringify(res.json.errors));
  return res.json.data;
}

// Print every column id + title + type for the outreach board (used to fill config.cols).
async function boardColumns(config) {
  const data = await gql(config, `query ($b:[ID!]) { boards(ids:$b){ name columns { id title type } } }`, { b: [config.monday.boardId] });
  const board = data.boards && data.boards[0];
  if (!board) throw new MondayError(`board ${config.monday.boardId} not found`);
  return { name: board.name, columns: board.columns };
}

function mapItem(config, raw) {
  const cols = {};
  for (const cv of raw.column_values || []) cols[cv.id] = { text: cv.text, value: cv.value };
  const C = config.monday.cols;
  const get = (id) => (id && cols[id] ? cols[id].text : '');
  // Email columns store {email, text} in value JSON; text renders as "Name - email".
  let email = '', emailName = '';
  if (C.email && cols[C.email]) {
    try { const v = JSON.parse(cols[C.email].value); email = v?.email || ''; emailName = v?.text || ''; } catch { /* fall back */ }
    if (!email) email = ((cols[C.email].text || '').match(/\S+@\S+/) || [''])[0];
  }
  return {
    id: raw.id,
    name: raw.name,
    raw: cols,
    status: get(C.status),
    email,
    emailName,
    articleUrl: get(C.articleUrl),
    assetUrl: get(C.assetUrl),
    citedSource: get(C.citedSource),
    rejectReason: get(C.rejectReason),
  };
}

async function allItems(config, limit = 200) {
  const q = `query ($b:ID!, $limit:Int!, $cursor:String) {
    boards(ids:[$b]) { items_page(limit:$limit, cursor:$cursor) {
      cursor items { id name column_values { id text value } } } } }`;
  if (!config.monday.boardId) throw new MondayError('OUTREACH_BOARD_ID is not set (create the Outreach board, then set it in .env)');
  let cursor = null; const out = [];
  do {
    const data = await gql(config, q, { b: config.monday.boardId, limit, cursor });
    if (!data.boards || !data.boards[0]) throw new MondayError(`board ${config.monday.boardId} not found or not accessible with this API key`);
    const page = data.boards[0].items_page;
    for (const it of page.items) out.push(mapItem(config, it));
    cursor = page.cursor;
  } while (cursor && out.length < 2000);
  return out;
}

async function itemsByStatus(config, statusLabel) {
  const items = await allItems(config);
  return items.filter((it) => (it.status || '').trim().toLowerCase() === statusLabel.trim().toLowerCase());
}

async function getItem(config, itemId) {
  const data = await gql(config, `query ($i:[ID!]) { items(ids:$i){ id name column_values{ id text value } } }`, { i: [itemId] });
  const it = data.items && data.items[0];
  return it ? mapItem(config, it) : null;
}

// change_simple_column_value handles Status + Dropdown by label, and text columns by value.
async function setSimple(config, itemId, columnId, value) {
  if (!columnId) return { skipped: true, reason: 'column id not configured' };
  const data = await gql(config,
    `mutation ($b:ID!, $i:ID!, $c:String!, $v:String!) {
       change_simple_column_value(board_id:$b, item_id:$i, column_id:$c, value:$v){ id } }`,
    { b: config.monday.boardId, i: itemId, c: columnId, v: String(value) });
  return { ok: true, id: data.change_simple_column_value.id };
}

async function setStatus(config, itemId, statusLabel) {
  return setSimple(config, itemId, config.monday.cols.status, statusLabel);
}

async function moveToGroup(config, itemId, groupId) {
  if (!groupId) return { skipped: true };
  await gql(config, `mutation ($i:ID!, $g:String!){ move_item_to_group(item_id:$i, group_id:$g){ id } }`, { i: itemId, g: groupId });
  return { ok: true };
}

async function addUpdate(config, itemId, body) {
  const data = await gql(config, `mutation ($i:ID!, $b:String!){ create_update(item_id:$i, body:$b){ id } }`, { i: itemId, b: body });
  return { ok: true, id: data.create_update.id };
}

async function createItem(config, name, columnValues = {}) {
  const data = await gql(config,
    `mutation ($b:ID!, $n:String!, $c:JSON){ create_item(board_id:$b, item_name:$n, column_values:$c){ id } }`,
    { b: config.monday.boardId, n: name, c: JSON.stringify(columnValues) });
  return { ok: true, id: data.create_item.id };
}

module.exports = { gql, boardColumns, allItems, itemsByStatus, getItem, setSimple, setStatus, moveToGroup, addUpdate, createItem, MondayError };
