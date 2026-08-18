'use strict';
const path = require('path');
const fs = require('fs');
const { loadEnv } = require('./lib/util');

loadEnv();

const ROOT = __dirname;
const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

const catalogue = readJson(path.join(ROOT, 'companydebt-asset-catalogue.json'));
const competitors = readJson(path.join(ROOT, 'competitors.json'));
const suppression = readJson(path.join(ROOT, 'suppression.json'));
// Cited sentence per article URL, captured from the Ahrefs "Left/Anchor/Right context" columns.
// Free fallback so blocked/thin pages still have the citation to anchor a draft on.
let citedContextMap = {};
try { citedContextMap = readJson(path.join(ROOT, 'cited-context.json')); } catch { /* optional */ }

const env = process.env;
const int = (v, d) => (v === undefined || v === '' ? d : parseInt(v, 10));
const bool = (v, d) => (v === undefined || v === '' ? d : /^(1|true|yes|on)$/i.test(v));

const config = {
  root: ROOT,
  stateDir: path.join(ROOT, 'state'),
  outboxDir: path.join(ROOT, 'outbox'), // .eml drafts land here for one-click open-and-send in Outlook

  // ---- phase / behaviour ----
  phase: catalogue.phase || 1,
  mode: catalogue.mode || 'STATS_HUB_ONLY',
  dailyCap: int(env.OUTREACH_DAILY_CAP, 5),
  review: (env.OUTREACH_REVIEW || 'print').toLowerCase(), // 'print' | 'write'
  includeAssetUrl: bool(env.INCLUDE_ASSET_URL, true),
  minDR: int(env.OUTREACH_MIN_DR, 30),
  matchThreshold: 0.18, // below this the item is a no-fit skip

  // ---- sender identity ----
  // The sender signature is appended to every draft body after the closing line, because the
  // sending mailbox (new Outlook / web) does NOT auto-add one.
  sender: {
    name: env.OUTREACH_SENDER_NAME || 'Théo Cristofari',
    title: env.OUTREACH_SENDER_TITLE || 'Head of PR',
    role: env.OUTREACH_SENDER_ROLE || 'the Company Debt editorial team',
    org: 'Company Debt',
    get signature() { return this.title ? `${this.name}\n${this.title}` : this.name; },
  },

  // ---- Monday ----
  monday: {
    apiKey: env.MONDAY_API_KEY || '',
    apiVersion: '2025-10',
    endpoint: 'https://api.monday.com/v2',
    boardId: env.OUTREACH_BOARD_ID || '',
    // Column ids on the NEW Outreach board. Fill from `conductor boardcols`.
    cols: {
      status: env.OUTREACH_COL_STATUS || '',
      email: env.OUTREACH_COL_EMAIL || '',
      assetUrl: env.OUTREACH_COL_ASSET_URL || '',
      articleUrl: env.OUTREACH_COL_ARTICLE_URL || '',
      notes: env.OUTREACH_COL_NOTES || '',
      rejectReason: env.OUTREACH_COL_REJECT_REASON || '',
      lastContacted: env.OUTREACH_COL_LAST_CONTACTED || '',
      citedSource: env.OUTREACH_COL_CITED_SOURCE || '',
      topic: env.OUTREACH_COL_TOPIC || 'dropdown_mm59xgza', // campaign topic (Insolvency / Pub Closures)
    },
    // Canonical status labels the conductor reads/writes on the Outreach board.
    status: {
      queue: 'Not started',
      ready: 'Ready to contact',
      research: 'To research',
      contacted: 'Contacted',
      responded: 'Responded',
      defunct: 'Defunct',
    },
    // Board groups: simplified to channel only. Campaign topic lives on the Topic column.
    groups: {
      emails: env.OUTREACH_GROUP_EMAILS || 'topics',
      linkedin: env.OUTREACH_GROUP_LINKEDIN || 'group_mm52mctc',
      contacted: env.OUTREACH_GROUP_CONTACTED || 'group_mm59f8fr',
      defunct: env.OUTREACH_GROUP_DEFUNCT || 'group_mm52z487',
    },
  },

  // ---- drafting ----
  // Provider precedence: explicit OUTREACH_PROVIDER, else Anthropic if keyed, else Gemini if keyed.
  provider: (env.OUTREACH_PROVIDER || (env.ANTHROPIC_API_KEY ? 'anthropic' : (env.GEMINI_API_KEY ? 'gemini' : 'none'))).toLowerCase(),
  get draftModel() {
    if (env.OUTREACH_DRAFT_MODEL) return env.OUTREACH_DRAFT_MODEL;
    return this.provider === 'gemini' ? 'gemini-2.5-pro' : 'claude-opus-4-8';
  },
  anthropic: {
    apiKey: env.ANTHROPIC_API_KEY || '',
    endpoint: 'https://api.anthropic.com/v1/messages',
    version: '2023-06-01',
  },
  gemini: {
    apiKey: env.GEMINI_API_KEY || '',
    endpoint: 'https://generativelanguage.googleapis.com/v1beta/models',
  },

  // ---- enrichment (Hunter.io) ----
  hunter: {
    apiKey: env.HUNTER_API_KEY || '',
    minConfidence: 80, // below this, item still halts to 'To research'
  },

  // ---- scraper ----
  scraper: {
    scrapingBeeKey: env.SCRAPINGBEE_API_KEY || '',
    userAgent: 'Mozilla/5.0 (compatible; CompanyDebtOutreach/0.1; +https://www.companydebt.com/)',
  },

  // ---- Microsoft Graph (Outlook draft) ----
  graph: {
    auth: (env.GRAPH_AUTH || 'app').toLowerCase(), // 'app' | 'delegated'
    tenantId: env.GRAPH_TENANT_ID || '',
    clientId: env.GRAPH_CLIENT_ID || '',
    clientSecret: env.GRAPH_CLIENT_SECRET || '',
    mailbox: env.OUTREACH_MAILBOX || '',
  },

  // ---- rejection categories (team-judged; conductor pre-fills a suggestion) ----
  rejectionCategories: [
    'weak_fit', 'wrong_contact', 'not_enough_citation_context',
    'too_salesy', 'tone_off', 'unapproved_figure', 'too_templated',
    'regulated_claim', 'suppressed',
  ],

  // free / personal email providers held for manual approval (corporate-only gate)
  freeEmailDomains: [
    'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.uk', 'hotmail.com',
    'hotmail.co.uk', 'outlook.com', 'live.com', 'icloud.com', 'me.com',
    'aol.com', 'protonmail.com', 'proton.me', 'gmx.com', 'mail.com',
  ],
  // generic / role inboxes we never treat as a named editorial contact (contact-confidence gate)
  genericInboxLocalparts: [
    'info', 'sales', 'hello', 'admin', 'contact', 'support', 'enquiries',
    'enquiry', 'marketing', 'press', 'pr', 'team', 'office', 'help', 'noreply', 'no-reply',
  ],

  catalogue,
  competitors,
  suppression,
  citedContext: citedContextMap,
};

// ---- multi-asset routing ----
// Campaign topic lives on the board's Topic column (Insolvency / Pub Closures / future ...).
// Scan resolves the data asset per row from that topic, so one board runs several campaigns.
config.assetById = Object.fromEntries((catalogue.assets || []).map((a) => [a.id, a]));
config.topicAssets = {
  'insolvency': 'uk-insolvency-statistics',
  'pub closures': 'pub-closures',
  'construction': 'construction-insolvency',
  'road haulage': 'road-haulage-insolvency',
  'recruitment': 'recruitment-insolvency',
  'motor vehicle repair': 'motor-vehicle-repair-insolvency',
  'furniture': 'furniture-insolvency',
  'estate agency': 'estate-agency-insolvency',
  'restaurants': 'restaurant-insolvency',
};
config.assetForTopic = (topic) => {
  const id = config.topicAssets[(topic || '').trim().toLowerCase()];
  return (id && config.assetById[id]) || catalogue.assets[0];
};

module.exports = config;
