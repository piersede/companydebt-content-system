'use strict';
const { httpFetch, stripHtml, hostOf } = require('./util');
const { STAT_TERMS } = require('./match');

// Phrases that appear ONLY on a real challenge/interstitial page (not on normal Cloudflare-
// fronted pages, which inject /cdn-cgi/challenge-platform scripts even when serving content).
const HARD_MARKERS = [
  'cf-browser-verification', 'checking your browser before',
  'ddos protection by cloudflare', 'attention required! | cloudflare',
];
// Softer phrases that also occur incidentally on real pages — only trust them on a small body.
const SOFT_MARKERS = [
  'just a moment', 'attention required', 'enable javascript and cookies',
  'access denied', 'request unsuccessful', 'please verify you are a human',
];
const NUMBER_RE = /(\d[\d,]{2,}|\d+(?:\.\d+)?\s?%)/;

function looksBlocked(status, body) {
  if ([401, 403, 429, 503].includes(status)) return true;
  const b = (body || '').toLowerCase();
  if (HARD_MARKERS.some((m) => b.includes(m))) return true;
  const paraCount = (b.match(/<p[ >]/g) || []).length;
  // A genuine interstitial is small and has little/no article markup. Big content pages that
  // merely mention "captcha" on a contact form are NOT blocked.
  if (b.length < 3000 && paraCount < 3) {
    if (/<script/.test(b) || SOFT_MARKERS.some((m) => b.includes(m))) return true;
  }
  return false;
}

function titleOf(html) {
  const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return m ? stripHtml(m[1]).slice(0, 300) : '';
}

// Outbound links whose host matches one of the competitor domains — candidate displaced pages.
function competitorLinks(html, dataCompetitors) {
  const links = [];
  const re = /href\s*=\s*["']([^"']+)["']/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const href = m[1];
    if (!/^https?:\/\//i.test(href)) continue;
    const host = hostOf(href);
    if ((dataCompetitors || []).some((d) => host === d || host.endsWith('.' + d))) links.push(href);
  }
  return [...new Set(links)];
}

// Best-guess of the sentence that cites an external insolvency stat.
function findCitedContext(text) {
  const sentences = text.replace(/\s+/g, ' ').split(/(?<=[.!?])\s+/);
  const scored = sentences
    .map((s) => {
      const low = s.toLowerCase();
      const termHit = STAT_TERMS.some((t) => low.includes(t));
      const numHit = NUMBER_RE.test(s);
      const score = (termHit ? 1 : 0) + (numHit ? 1 : 0);
      return { s: s.trim(), score };
    })
    .filter((x) => x.score >= 2 && x.s.length > 40 && x.s.length < 400)
    .sort((a, b) => b.score - a.score);
  return scored.length ? scored[0].s : '';
}

async function scrape(url, config) {
  try {
    const res = await httpFetch(url, { headers: { 'User-Agent': config.scraper.userAgent, Accept: 'text/html' } }, 30000);
    let html = res.body;
    let blocked = looksBlocked(res.status, html);

    if (blocked && config.scraper.scrapingBeeKey) {
      const bee = `https://app.scrapingbee.com/api/v1/?api_key=${config.scraper.scrapingBeeKey}&url=${encodeURIComponent(url)}&render_js=true`;
      const beeRes = await httpFetch(bee, {}, 60000);
      if (beeRes.ok && !looksBlocked(beeRes.status, beeRes.body)) { html = beeRes.body; blocked = false; }
    }

    if (blocked) return { ok: false, blocked: true, error: `blocked (status ${res.status})`, url };

    const text = stripHtml(html);
    // Thin content = we didn't actually get the article (JS-rendered or soft-challenged).
    if (text.length < 300) return { ok: false, blocked: true, error: 'thin content (likely JS-rendered or challenged)', url };
    return {
      ok: true,
      blocked: false,
      url,
      title: titleOf(html),
      text,
      citedContext: findCitedContext(text),
      competitorLinks: competitorLinks(html, (config.competitors || {}).dataCompetitors),
    };
  } catch (e) {
    return { ok: false, blocked: false, error: String(e.message || e), url };
  }
}

module.exports = { scrape, findCitedContext, competitorLinks, looksBlocked };
