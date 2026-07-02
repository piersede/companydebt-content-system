'use strict';
const fs = require('fs');
const path = require('path');
const { httpFetch, warn } = require('./util');

// Microsoft Graph — drops a finished email into an Outlook DRAFTS folder. NEVER sends.
// Two auth modes: 'app' (client-credentials, unattended) and 'delegated' (device-code, manual).

async function appToken(config) {
  const g = config.graph;
  const url = `https://login.microsoftonline.com/${g.tenantId}/oauth2/v2.0/token`;
  const body = new URLSearchParams({
    client_id: g.clientId, client_secret: g.clientSecret,
    scope: 'https://graph.microsoft.com/.default', grant_type: 'client_credentials',
  });
  const res = await httpFetch(url, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body.toString() }, 20000);
  if (!res.json || !res.json.access_token) throw new Error('Graph app token failed: ' + res.body.slice(0, 300));
  return res.json.access_token;
}

async function delegatedToken(config, stateDir) {
  const g = config.graph;
  const cachePath = path.join(stateDir, '.graphcache.json');
  let cache = {};
  try { cache = JSON.parse(fs.readFileSync(cachePath, 'utf8')); } catch { /* none */ }
  const tokenUrl = `https://login.microsoftonline.com/${g.tenantId || 'common'}/oauth2/v2.0/token`;

  if (cache.refresh_token) {
    const body = new URLSearchParams({ client_id: g.clientId, grant_type: 'refresh_token', refresh_token: cache.refresh_token, scope: 'Mail.ReadWrite offline_access' });
    const res = await httpFetch(tokenUrl, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body.toString() }, 20000);
    if (res.json && res.json.access_token) {
      fs.mkdirSync(stateDir, { recursive: true });
      fs.writeFileSync(cachePath, JSON.stringify({ refresh_token: res.json.refresh_token || cache.refresh_token }));
      return res.json.access_token;
    }
  }

  // device-code flow (interactive, first run only)
  const dcUrl = `https://login.microsoftonline.com/${g.tenantId || 'common'}/oauth2/v2.0/devicecode`;
  const dcRes = await httpFetch(dcUrl, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ client_id: g.clientId, scope: 'Mail.ReadWrite offline_access' }).toString() }, 20000);
  const dc = dcRes.json;
  if (!dc || !dc.user_code) throw new Error('Graph device-code failed: ' + dcRes.body.slice(0, 300));
  warn(`\n[Graph] To authorise Outlook drafting, visit ${dc.verification_uri} and enter code: ${dc.user_code}\n`);
  const started = Date.now();
  while (Date.now() - started < (dc.expires_in || 600) * 1000) {
    await new Promise((r) => setTimeout(r, (dc.interval || 5) * 1000));
    const pr = await httpFetch(tokenUrl, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ client_id: g.clientId, grant_type: 'urn:ietf:params:oauth:grant-type:device_code', device_code: dc.device_code }).toString() }, 20000);
    if (pr.json && pr.json.access_token) {
      fs.mkdirSync(stateDir, { recursive: true });
      fs.writeFileSync(cachePath, JSON.stringify({ refresh_token: pr.json.refresh_token }));
      return pr.json.access_token;
    }
    if (pr.json && pr.json.error && pr.json.error !== 'authorization_pending') throw new Error('Graph device-code error: ' + pr.json.error);
  }
  throw new Error('Graph device-code timed out');
}

// Creates a draft; returns { ok, id } or { ok:false, reason } (non-fatal).
async function createDraft(config, { to, subject, body, name }) {
  const g = config.graph;
  if (!g.clientId || (g.auth === 'app' && (!g.clientSecret || !g.tenantId || !g.mailbox))) {
    return { ok: false, reason: 'Graph not configured (draft kept on Monday only)' };
  }
  try {
    let token, base;
    if (g.auth === 'delegated') { token = await delegatedToken(config, config.stateDir); base = 'https://graph.microsoft.com/v1.0/me'; }
    else { token = await appToken(config); base = `https://graph.microsoft.com/v1.0/users/${encodeURIComponent(g.mailbox)}`; }

    const message = {
      subject,
      body: { contentType: 'Text', content: body },
      toRecipients: [{ emailAddress: { address: to, name: name || undefined } }],
    };
    const res = await httpFetch(`${base}/messages`, {
      method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, body: JSON.stringify(message),
    }, 30000);
    if (res.json && res.json.id) return { ok: true, id: res.json.id, webLink: res.json.webLink };
    return { ok: false, reason: `Graph draft failed (status ${res.status})` };
  } catch (e) {
    return { ok: false, reason: String(e.message || e) };
  }
}

module.exports = { createDraft };
