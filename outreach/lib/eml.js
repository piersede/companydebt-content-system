'use strict';
const fs = require('fs');
const path = require('path');

// Write a draft as a .eml file that Outlook opens as a ready-to-send, editable compose
// window. The `X-Unsent: 1` header is the trick: desktop Outlook treats such a message as an
// unsent draft, so double-clicking it opens the composer pre-filled (To/Subject/Body) with a
// Send button. No Microsoft Graph, no Azure app, no credentials — fully offline.
function encodeHeader(s) {
  // RFC 2047 encode if the header has non-ASCII, else pass through.
  return /[^\x00-\x7F]/.test(s) ? `=?utf-8?B?${Buffer.from(s, 'utf8').toString('base64')}?=` : s;
}

function writeEml(outboxDir, { id, to, name, subject, body }) {
  fs.mkdirSync(outboxDir, { recursive: true });
  const toHeader = name ? `${encodeHeader(name)} <${to}>` : to;
  const CRLF = '\r\n';
  const headers = [
    `To: ${toHeader}`,
    `Subject: ${encodeHeader(subject)}`,
    'X-Unsent: 1',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Transfer-Encoding: 8bit',
  ].join(CRLF);
  const content = headers + CRLF + CRLF + String(body).replace(/\r?\n/g, CRLF) + CRLF;

  const safe = (to || 'draft').replace(/[^a-z0-9.@_-]/gi, '_').slice(0, 40);
  const file = path.join(outboxDir, `${id}_${safe}.eml`);
  fs.writeFileSync(file, content, 'utf8');
  return file;
}

module.exports = { writeEml };
