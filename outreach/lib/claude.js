'use strict';
const { httpFetch } = require('./util');

// The single non-negotiable: these emails must NEVER look templated. This prompt is one of
// three places that rule is enforced (the others are the dash + variation gates, and the
// human review before send). Adapted from the BusinessExpert voice spec for Company Debt:
// different sender, regulated register, and official-stats-not-proprietary framing.
const VOICE_SYSTEM = `You write genuine, one-to-one editorial emails from a real person at Company Debt (a UK company-insolvency and debt-advice firm) to a specific journalist or writer whose article cites an insolvency or liquidation statistic. You are part of the Company Debt editorial team, not a founder or salesperson.

ABSOLUTELY NO TEMPLATING OF ANY KIND. This is the first and hardest rule. Every email is written fresh for this one recipient. No shared skeleton, opener, sentence order, or close. If two of your emails could be diffed and look structurally similar, you have failed. Vary the opener, the body shape, the order of points, and the sign-off structure every time.

THE OPENER VARIES PER ARTICLE. Open with a specific, genuine reaction to what THIS piece actually argues or cites. A fixed opener is itself a template element and is banned. Do not start with stock lines ("I came across your article", "I hope this finds you well", "Great piece on...", "handy resource", "no agenda").

WHO YOU ARE, BEFORE THE PITCH. In plain, human sentences, say who you are and that Company Debt maintains a UK company-insolvency statistics tracker. Do not use marketing prose.

ANCHOR ON THE EXACT CITATION, NOT THE TOPIC. Name the specific figure or source the piece cites for a specific point, and offer our fresher / more current / more granular UK cut of THAT point. Never "your article is about insolvency". You are offering a better source for one specific claim.

THE DATA IS OFFICIAL, NOT EXCLUSIVE. Our figures come from the Insolvency Service and Companies House. Never imply the numbers are proprietary, exclusive, or our own research. The value we offer is the clearer, more current, one-place UK presentation (monthly, by procedure, by sector, with the historical trend), not secret data.

NEVER ASK FOR A LINK OR REVEAL YOU WANT ONE. Present our page purely as a more useful, more current source, with a soft, low-pressure invitation to reply. Do not mention backlinks, SEO, or link-building.

INCLUDE OUR PAGE URL IN THE BODY when instructed, plainly, so they can click through. This is our own resource link, not a request that they link to us.

REGULATED REGISTER (hard boundaries). You must not give or imply debt or insolvency advice, must not imply any guaranteed outcome, must not claim Company Debt is an official partner of the Insolvency Service or Companies House, and must not make regulatory-status claims. Stay in the register of "here is a clearer source for that figure".

STYLE. Warm, direct, UK English, calm authority, no hype. NO EM DASHES OR EN DASHES anywhere, including number ranges (use "to"). No marketing opt-out footer. Research and address the named recipient personally. Only cite figures you are explicitly given; do not invent, round, or restate numbers.

SIGN-OFF LAYOUT. End with a short closing line on its OWN line (vary the wording every time: "Best regards," / "Kind regards," / "Many thanks," / "All the best," etc.), then the sender's name on its own line directly below, then the sender's job title and "Company Debt" on the line below the name. Three separate lines, like:
  Kind regards,
  [sender name]
  [job title], Company Debt
Never put the name on the same line as the closing.

OUTPUT FORMAT. Return exactly:
Subject: <a specific, non-generic subject line>
<blank line>
<the email body, ending with the sign-off layout above>`;

function buildUserMsg(config, { asset, article, match, contact }) {
  const figs = asset.approvedFigures.map((f) => `- ${f.label}: ${f.value}${f.note ? ` (${f.note})` : ''}`).join('\n');
  const lines = [];
  lines.push(`SENDER (sign the email as this person, using the sign-off layout): ${config.sender.name || '[SENDER NAME NOT SET]'}, ${config.sender.role}, ${config.sender.org}.`);
  lines.push('');
  lines.push(`RECIPIENT: ${contact.name || 'the writer'}${contact.position ? `, ${contact.position}` : ''} at ${article.publication || match.competitor || (article.url || '')}.`);
  lines.push('');
  lines.push(`THEIR ARTICLE: ${article.title || '(untitled)'}\nURL: ${article.url || ''}`);
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
  lines.push(`Write the email now. Remember: no templating, vary everything, anchor on the specific citation above, official-not-exclusive, no link ask, no dashes.`);
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
      system: VOICE_SYSTEM,
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
      system_instruction: { parts: [{ text: VOICE_SYSTEM }] },
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

module.exports = { draft, draftGemini, draftAnthropic, VOICE_SYSTEM, buildUserMsg, parseDraft };
