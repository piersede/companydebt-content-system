'use strict';
const { httpFetch } = require('./util');

// The single non-negotiable: these emails must NEVER look templated. This prompt is one of
// three places that rule is enforced (the others are the dash + variation gates, and the
// human review before send). Adapted from the BusinessExpert voice spec for Company Debt:
// different sender, regulated register, and official-stats-not-proprietary framing.
// Parameterised per asset (asset.pitch) so a second campaign (e.g. pub closures) reframes the
// "who we are / what we track / where the data comes from" lines without a second prompt.
const DEFAULT_PITCH = {
  citationDesc: 'an insolvency or liquidation statistic',
  trackerDesc: 'a UK company-insolvency statistics tracker',
  institutionalLine: 'at Company Debt we keep a monthly tracker of the official UK insolvency figures',
  sourceLine: 'Our figures come from the Insolvency Service and Companies House. The value we offer is the clearer, more current, one-place UK presentation, not secret data.',
};

function voiceSystem(asset) {
  const p = { ...DEFAULT_PITCH, ...((asset && asset.pitch) || {}) };
  return `You write genuine, one-to-one editorial emails from a real person at Company Debt (a UK company-insolvency and debt-advice firm) to a specific journalist or writer whose article cites ${p.citationDesc}. You are part of the Company Debt editorial team, not a founder or salesperson.

ABSOLUTELY NO TEMPLATING OF ANY KIND. This is the first and hardest rule. Every email is written fresh for this one recipient. No shared skeleton, opener, sentence order, or close. If two of your emails could be diffed and look structurally similar, you have failed. Vary the opener, the body shape, the order of points, and the sign-off structure every time.

THE OPENER VARIES PER ARTICLE. Open with a specific, genuine reaction to what THIS piece actually argues or cites. A fixed opener is itself a template element and is banned. Do not start with stock lines ("I came across your article", "I hope this finds you well", "Great piece on...", "handy resource", "no agenda").

WHO WE ARE, BEFORE THE PITCH. In plain, human sentences, establish that you work with Company Debt and that Company Debt maintains ${p.trackerDesc}. Keep it institutional ("${p.institutionalLine}"). Do NOT state a personal name, and do NOT claim to personally be a licensed insolvency practitioner. The sender's own email signature carries their name and title. No marketing prose.

ANCHOR ON THE EXACT CITATION, NOT THE TOPIC. Name the specific figure or source the piece cites for a specific point, and offer our fresher / more current / more granular UK cut of THAT point. Never "your article is about the topic". You are offering a better source for one specific claim.

THE DATA IS OFFICIAL, NOT EXCLUSIVE. ${p.sourceLine} Never imply the numbers are proprietary, exclusive, or our own research.

NEVER ASK FOR A LINK OR REVEAL YOU WANT ONE. Present our page purely as a more useful, more current source, with a soft, low-pressure invitation to reply. Do not mention backlinks, SEO, or link-building.

INCLUDE OUR PAGE URL IN THE BODY when instructed, plainly, so they can click through. This is our own resource link, not a request that they link to us.

REGULATED REGISTER (hard boundaries). You must not give or imply debt or insolvency advice, must not imply any guaranteed outcome, must not claim Company Debt is an official partner of the Insolvency Service or Companies House, and must not make regulatory-status claims. Stay in the register of "here is a clearer source for that figure".

STYLE. Warm, direct, UK English, calm authority, no hype. NO EM DASHES OR EN DASHES anywhere, including number ranges (use "to"). No marketing opt-out footer. Research and address the named recipient personally. Only cite figures you are explicitly given; do not invent, round, or restate numbers.

SIGN-OFF. End with a single short, varied closing line only ("Best regards," / "Kind regards," / "Many thanks," / "All the best," etc.). Do NOT add any name, job title, or company after it, and do NOT write a signature block. The sender applies their own email signature on send, so any manual sign-off would duplicate it. The email body ends at that closing line.

OUTPUT FORMAT. Return exactly:
Subject: <a specific, non-generic subject line>
<blank line>
<the email body, ending with a single closing line and NO name/title/signature>`;
}

function buildUserMsg(config, { asset, article, match, contact, articleAuthor }) {
  const figs = asset.approvedFigures.map((f) => `- ${f.label}: ${f.value}${f.note ? ` (${f.note})` : ''}`).join('\n');
  // When the byline author has left / is freelance, the row falls back to an editor or news
  // desk. In that case the recipient did NOT write the piece, so the email must not say "your article".
  const differentAuthor = articleAuthor && articleAuthor.trim().toLowerCase() !== (contact.name || '').trim().toLowerCase();
  const lines = [];
  lines.push(`SENDER: an email from someone at Company Debt. Their name and title come from their own email signature, so do NOT write any name, personal job title, or signature block in the body.`);
  lines.push('');
  lines.push(`RECIPIENT: ${contact.name || 'the news desk'}${contact.position ? `, ${contact.position}` : ''} at ${article.publication || match.competitor || (article.url || '')}.`);
  if (differentAuthor) {
    lines.push(`IMPORTANT: the recipient is NOT the article's author. The piece was written by ${articleAuthor}. Do NOT write "your article" or imply the recipient wrote it. Address the recipient directly (use a natural team greeting such as "Hello," if it is a desk rather than a named person), and refer to it as a piece ${articleAuthor} wrote for the publication.`);
  }
  lines.push('');
  lines.push(`THEIR ARTICLE: ${article.title || '(untitled)'}${articleAuthor ? ` (by ${articleAuthor})` : ''}\nURL: ${article.url || ''}`);
  lines.push('');
  lines.push(`THE CITATION WE ARE ADDRESSING (this is what to anchor the email on):`);
  lines.push(match.citedContext ? `"${match.citedContext}"` : '(none captured — DO NOT invent one)');
  if (match.competitorUrl) lines.push(`They currently point to: ${match.competitorUrl}`);
  lines.push('');
  lines.push(`OUR PAGE: ${asset.title}\nURL: ${asset.url}\nCoverage: ${asset.coverage}. Sources: ${asset.sources.join(' and ')}. Latest data: ${asset.updated}. Next release: ${asset.nextRelease}.`);
  lines.push('');
  lines.push(`APPROVED FIGURES YOU MAY CITE (and no others):\n${figs}`);
  lines.push('');
  lines.push(config.includeAssetUrl
    ? `Include our page URL (${asset.url}) plainly in the body.`
    : `Do NOT paste the URL; offer to send the page if useful.`);
  lines.push('');
  lines.push(`Write the email now. Remember: no templating, vary everything, anchor on the specific citation above, official-not-exclusive, no link ask, no dashes, and NO name/title/signature block (the signature is added on send).`);
  return lines.join('\n');
}

function parseDraft(text) {
  const m = text.match(/^\s*subject:\s*(.+?)\s*\n([\s\S]+)$/i);
  if (m) return { subject: m[1].trim(), body: m[2].trim() };
  return { subject: '', body: text.trim() };
}

async function draftAnthropic(config, ctx) {
  const res = await httpFetch(config.anthropic.endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': config.anthropic.apiKey,
      'anthropic-version': config.anthropic.version,
    },
    body: JSON.stringify({
      model: config.draftModel,
      max_tokens: 1200,
      temperature: 1,
      system: voiceSystem(ctx.asset),
      messages: [{ role: 'user', content: buildUserMsg(config, ctx) }],
    }),
  }, 60000);
  if (!res.json) return { ok: false, reason: `Anthropic non-JSON (status ${res.status})` };
  if (res.json.error) return { ok: false, reason: 'Anthropic error: ' + JSON.stringify(res.json.error) };
  const text = (res.json.content || []).map((c) => c.text || '').join('').trim();
  return { ok: true, ...parseDraft(text), model: config.draftModel, raw: text };
}

async function draftGemini(config, ctx) {
  const url = `${config.gemini.endpoint}/${config.draftModel}:generateContent?key=${config.gemini.apiKey}`;
  const res = await httpFetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      system_instruction: { parts: [{ text: voiceSystem(ctx.asset) }] },
      contents: [{ role: 'user', parts: [{ text: buildUserMsg(config, ctx) }] }],
      // 2.5-pro/3-pro are thinking models: reasoning tokens count against the cap, so budget
      // generously or the visible email comes back empty with finishReason MAX_TOKENS.
      generationConfig: { temperature: 1.0, maxOutputTokens: 8192, topP: 0.95 },
    }),
  }, 60000);
  if (!res.json) return { ok: false, reason: `Gemini non-JSON (status ${res.status})` };
  if (res.json.error) return { ok: false, reason: 'Gemini error: ' + (res.json.error.message || JSON.stringify(res.json.error)) };
  const cand = (res.json.candidates || [])[0];
  if (!cand) return { ok: false, reason: 'Gemini returned no candidate (possibly safety-blocked)' };
  const text = (cand.content?.parts || []).map((p) => p.text || '').join('').trim();
  if (!text) return { ok: false, reason: `Gemini empty text (finishReason ${cand.finishReason || '?'})` };
  return { ok: true, ...parseDraft(text), model: config.draftModel, raw: text };
}

async function draft(config, ctx) {
  if (config.provider === 'anthropic' && config.anthropic.apiKey) return draftAnthropic(config, ctx);
  if (config.provider === 'gemini' && config.gemini.apiKey) return draftGemini(config, ctx);
  // fallback to whichever key exists
  if (config.anthropic.apiKey) return draftAnthropic(config, ctx);
  if (config.gemini.apiKey) return draftGemini(config, ctx);
  return { ok: false, reason: 'no drafting provider configured (set GEMINI_API_KEY or ANTHROPIC_API_KEY)' };
}

module.exports = { draft, draftGemini, draftAnthropic, voiceSystem, buildUserMsg, parseDraft };
