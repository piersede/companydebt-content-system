'use strict';
// One-off: collapse the 4 theme×channel groups into 2 channel groups (eMails, LinkedIn) and
// move the theme onto a new "Topic" dropdown column. Idempotent-ish (re-runnable).
const path = require('path');
const c = require(path.join(__dirname, '..', 'config'));
const m = require(path.join(__dirname, '..', 'lib', 'monday'));
const U = require(path.join(__dirname, '..', 'lib', 'util'));

async function mut(q, v, tries = 3) {
  for (let a = 1; a <= tries; a++) {
    try { return await m.gql(c, q, v); }
    catch (e) { if (a === tries) throw e; await U.sleep(2500); }
  }
}

(async () => {
  // 1) Topic dropdown column (reuse if already there)
  let topicCol;
  const cols = await m.gql(c, `query($b:[ID!]){boards(ids:$b){columns{id title type}}}`, { b: [c.monday.boardId] });
  const existing = cols.boards[0].columns.find((x) => x.title === 'Topic');
  if (existing) { topicCol = existing.id; console.log('Topic column exists:', topicCol); }
  else { const d = await mut(`mutation($b:ID!){create_column(board_id:$b,title:"Topic",column_type:dropdown){id}}`, { b: c.monday.boardId }); topicCol = d.create_column.id; console.log('created Topic column:', topicCol); }

  // 2) rename the two survivor groups
  const ren = (g, t) => mut(`mutation($b:ID!,$g:String!,$v:String!){update_group(board_id:$b,group_id:$g,group_attribute:title,new_value:$v){id}}`, { b: c.monday.boardId, g, v: t });
  await ren('topics', 'eMails'); await U.sleep(300);
  await ren('group_mm52mctc', 'LinkedIn'); await U.sleep(300);

  // 3) set Topic + consolidate groups
  const plan = {
    topics:          { topic: 'Insolvency',   target: 'topics',         move: false },
    group_mm53vtbh:  { topic: 'Pub Closures', target: 'topics',         move: true  }, // pub email -> eMails
    group_mm52mctc:  { topic: 'Insolvency',   target: 'group_mm52mctc', move: false },
    group_mm53fmpj:  { topic: 'Pub Closures', target: 'group_mm52mctc', move: true  }, // hosp LI -> LinkedIn
  };
  const all = await m.allItems(c);
  let tagged = 0, moved = 0;
  for (const it of all) {
    const p = plan[it.groupId];
    if (!p) continue; // skip Defunct + anything else
    if (p.move) { await mut(`mutation($i:ID!,$g:String!){move_item_to_group(item_id:$i,group_id:$g){id}}`, { i: it.id, g: p.target }); moved++; await U.sleep(150); }
    const cv = JSON.stringify({ [topicCol]: { labels: [p.topic] } });
    await mut(`mutation($b:ID!,$i:ID!,$v:JSON!){change_multiple_column_values(board_id:$b,item_id:$i,column_values:$v,create_labels_if_missing:true){id}}`, { b: c.monday.boardId, i: it.id, v: cv });
    tagged++; if (tagged % 40 === 0) console.log(`  ...${tagged} tagged, ${moved} moved`);
    await U.sleep(160);
  }
  console.log(`tagged ${tagged} rows; ${moved} moved`);

  // 4) delete the two emptied groups
  for (const g of ['group_mm53vtbh', 'group_mm53fmpj']) {
    try { await mut(`mutation($b:ID!,$g:String!){delete_group(board_id:$b,group_id:$g){id}}`, { b: c.monday.boardId, g }); console.log('deleted group', g); }
    catch (e) { console.log('delete fail', g, e.message); }
    await U.sleep(300);
  }

  const gg = await m.gql(c, `query($b:[ID!]){boards(ids:$b){groups{id title}}}`, { b: [c.monday.boardId] });
  console.log('FINAL groups:'); for (const gr of gg.boards[0].groups) console.log('  ', gr.id, '|', gr.title);
  console.log('TOPIC_COLUMN_ID=' + topicCol);
})().catch((e) => { console.error(e.message); process.exit(1); });
