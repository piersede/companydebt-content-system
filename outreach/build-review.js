#!/usr/bin/env node
'use strict';
// Build a local review page from the .eml drafts in outbox/. For "new Outlook" / Outlook on the
// web users (no desktop COM, no Azure): each draft gets an "Open in Outlook" button that deep-links
// to an OWA compose window pre-filled with To/Subject/Body (Outlook auto-saves it to Drafts), plus
// a "Copy" button as a fallback for very long bodies. Run:  node build-review.js  then open the page.
const fs = require('fs');
const path = require('path');

const outbox = path.join(__dirname, 'outbox');
const files = fs.existsSync(outbox) ? fs.readdirSync(outbox).filter((f) => f.toLowerCase().endsWith('.eml')) : [];

function parseEml(raw) {
  const idx = raw.indexOf('\r\n\r\n') >= 0 ? raw.indexOf('\r\n\r\n') : raw.indexOf('\n\n');
  const head = raw.slice(0, idx);
  const body = raw.slice(idx).replace(/^\s+/, '');
  const get = (name) => { const m = head.match(new RegExp('^' + name + ':\\s*(.+)$', 'im')); return m ? m[1].trim() : ''; };
  const to = get('To');
  const em = (to.match(/<([^>]+)>/) || [null, to])[1];
  const name = to.replace(/<[^>]+>/, '').trim();
  return { to, email: em, name, subject: get('Subject'), body };
}

const drafts = files.map((f) => ({ file: f, ...parseEml(fs.readFileSync(path.join(outbox, f), 'utf8')) }));

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const cards = drafts.map((d, i) => {
  const owa = 'https://outlook.office.com/mail/deeplink/compose?to=' + encodeURIComponent(d.email) +
    '&subject=' + encodeURIComponent(d.subject) + '&body=' + encodeURIComponent(d.body);
  return `<div class="card">
    <div class="meta"><b>${esc(d.name || d.email)}</b> &lt;${esc(d.email)}&gt;</div>
    <div class="subj">${esc(d.subject)}</div>
    <textarea id="b${i}" readonly>${esc(d.body)}</textarea>
    <div class="btns">
      <a class="btn primary" href="${esc(owa)}" target="_blank" rel="noopener">Open in Outlook</a>
      <button class="btn" onclick="copyBody(${i}, this)">Copy email text</button>
      <span class="hint">opens a pre-filled compose window (auto-saves to Drafts)</span>
    </div>
  </div>`;
}).join('\n');

const html = `<!doctype html><meta charset="utf-8"><title>Outreach drafts to review</title>
<style>
 body{font:15px/1.5 -apple-system,Segoe UI,Arial,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}
 h1{color:#0b3d2e} .card{border:1px solid #d5d5d5;border-radius:8px;padding:1rem 1.2rem;margin:1rem 0}
 .meta{color:#333} .subj{font-weight:600;margin:.3rem 0 .5rem} textarea{width:100%;height:230px;border:1px solid #ccc;border-radius:6px;padding:.6rem;font:13px/1.5 Consolas,monospace;resize:vertical}
 .btns{margin-top:.6rem;display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}
 .btn{display:inline-block;padding:.45rem .9rem;border:1px solid #0b6b4f;border-radius:6px;background:#fff;color:#0b6b4f;text-decoration:none;cursor:pointer;font-size:14px}
 .btn.primary{background:#0b6b4f;color:#fff} .hint{color:#777;font-size:13px}
</style>
<h1>Outreach drafts to review (${drafts.length})</h1>
<p>Click <b>Open in Outlook</b> to review + send each one. Nothing is sent automatically. Mark the row <b>Contacted</b> on the board once sent.</p>
${cards || '<p>No drafts in outbox/. Run a write-mode scan first.</p>'}
<script>
function copyBody(i,btn){var t=document.getElementById('b'+i);t.select();try{document.execCommand('copy');}catch(e){navigator.clipboard&&navigator.clipboard.writeText(t.value);}btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy email text';},1500);}
</script>`;

const out = path.join(outbox, 'drafts.html');
fs.mkdirSync(outbox, { recursive: true });
fs.writeFileSync(out, html);
console.log(`Wrote ${out} (${drafts.length} draft${drafts.length === 1 ? '' : 's'})`);
