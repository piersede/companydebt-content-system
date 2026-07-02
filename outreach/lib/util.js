'use strict';
const fs = require('fs');
const path = require('path');

// --- env loading: repo-root .env first, then outreach/.env; never overwrite a real process.env ---
function loadEnv() {
  const candidates = [
    path.join(__dirname, '..', '..', '.env'), // repo root
    path.join(__dirname, '..', '.env'),        // outreach/.env
  ];
  for (const f of candidates) {
    let txt;
    try { txt = fs.readFileSync(f, 'utf8'); } catch { continue; }
    for (const line of txt.split(/\r?\n/)) {
      const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
      if (!m) continue;
      const k = m[1];
      let v = m[2].replace(/^["']|["']$/g, '');
      if (process.env[k] === undefined || process.env[k] === '') process.env[k] = v;
    }
  }
}

const C = {
  reset: '\x1b[0m', dim: '\x1b[2m', red: '\x1b[31m', green: '\x1b[32m',
  yellow: '\x1b[33m', cyan: '\x1b[36m', bold: '\x1b[1m',
};
function log(msg) { process.stdout.write(msg + '\n'); }
function info(msg) { log(`${C.cyan}${msg}${C.reset}`); }
function ok(msg) { log(`${C.green}${msg}${C.reset}`); }
function warn(msg) { log(`${C.yellow}${msg}${C.reset}`); }
function err(msg) { log(`${C.red}${msg}${C.reset}`); }
function dim(msg) { log(`${C.dim}${msg}${C.reset}`); }

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// fetch with timeout + optional JSON parse; returns { ok, status, body, json }
async function httpFetch(url, opts = {}, timeoutMs = 30000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  if (typeof t.unref === 'function') t.unref(); // don't keep the loop alive (avoids Windows exit assertion)
  try {
    const res = await fetch(url, { ...opts, signal: ctrl.signal });
    const body = await res.text();
    let json = null;
    try { json = JSON.parse(body); } catch { /* not json */ }
    return { ok: res.ok, status: res.status, headers: res.headers, body, json };
  } finally {
    clearTimeout(t);
  }
}

// Very small HTML -> text: drop script/style, strip tags, collapse whitespace.
function stripHtml(html) {
  return String(html)
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<\/(p|div|li|h[1-6]|br|tr|section)>/gi, '\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&#\d+;/g, ' ')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

// Normalise a numeric token for claim-ledger comparison: "1,868" -> "1868", "76%" -> "76%".
function normNum(s) {
  return String(s).toLowerCase().replace(/,/g, '').replace(/\s+/g, '').trim();
}

function hostOf(url) {
  try { return new URL(url).host.replace(/^www\./, '').toLowerCase(); } catch { return ''; }
}
function slugOf(url) {
  try { return new URL(url).pathname.toLowerCase().replace(/\/+$/, ''); } catch { return ''; }
}

module.exports = { loadEnv, log, info, ok, warn, err, dim, sleep, httpFetch, stripHtml, normNum, hostOf, slugOf, C };
