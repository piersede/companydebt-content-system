'use strict';

const path = require('path');
const { ROOT, loadRegistrySnapshot } = require('./bernstein-context');

const PAGE_TYPE_ORDER = {
  review: 0,
  brand_compare: 1,
  brand_comparison: 1,
  comparison: 1,
  roundup: 2,
  guide: 3,
};

const FRESHNESS_ORDER = {
  stale: 0,
  aging: 1,
  current: 2,
};

function mergeExisting(existing, item) {
  if (!existing) {
    return {
      ...item,
      queue_status: 'pending',
      queue_history: [],
      last_selected_at: null,
      completed_at: null,
      last_stage: null,
      blocked_reason: null,
    };
  }

  return {
    ...item,
    queue_status: existing.queue_status || 'pending',
    queue_history: existing.queue_history || [],
    last_selected_at: existing.last_selected_at || null,
    completed_at: existing.completed_at || null,
    last_stage: existing.last_stage || null,
    blocked_reason: existing.blocked_reason || null,
  };
}

function buildBacklog(existingBacklog = null) {
  const existingMap = new Map((existingBacklog?.items || []).map((item) => [item.id, item]));
  const registryItems = loadRegistrySnapshot();

  const items = registryItems.map((item, index) => mergeExisting(existingMap.get(`page:${item.page_id}`), {
    id: `page:${item.page_id}`,
    page_id: item.page_id,
    slug: item.slug,
    title: item.title || item.page_id,
    url: `/preview/${item.slug}`,
    page_type: item.page_type || 'unknown',
    page_class: item.page_class || null,
    freshness_tier: item.freshness_tier || null,
    verification_date: item.verification_date || null,
    wp_page_id: item.wp_page_id || null,
    page_config_file: path.join(ROOT, 'scripts', ...String(item.module_path || '').split('.')) + '.py',
    suggested_article_file: path.join(ROOT, 'preview', `${item.slug}.html`),
    section_index: index,
  }));

  return {
    version: 1,
    generated_at: new Date().toISOString(),
    source_files: {
      page_registry: path.join(ROOT, 'scripts', 'build_page.py'),
    },
    items,
  };
}

function compareBacklogItems(a, b) {
  const pageTypeDelta = (PAGE_TYPE_ORDER[a.page_type] ?? 99) - (PAGE_TYPE_ORDER[b.page_type] ?? 99);
  if (pageTypeDelta !== 0) return pageTypeDelta;

  const freshnessDelta = (FRESHNESS_ORDER[a.freshness_tier] ?? 99) - (FRESHNESS_ORDER[b.freshness_tier] ?? 99);
  if (freshnessDelta !== 0) return freshnessDelta;

  return String(a.page_id).localeCompare(String(b.page_id));
}

function compareInProgressItems(a, b) {
  const aSelected = a.last_selected_at ? Date.parse(a.last_selected_at) : 0;
  const bSelected = b.last_selected_at ? Date.parse(b.last_selected_at) : 0;
  if (aSelected !== bSelected) return bSelected - aSelected;
  return compareBacklogItems(a, b);
}

function findNextItem(backlog) {
  return [...backlog.items]
    .filter((item) => item.queue_status === 'pending')
    .sort(compareBacklogItems)[0] || null;
}

function findInProgressItem(backlog) {
  return [...backlog.items]
    .filter((item) => item.queue_status === 'in_progress')
    .sort(compareInProgressItems)[0] || null;
}

function summarizeBacklog(backlog) {
  const summary = { total: backlog.items.length, pending: 0, in_progress: 0, completed: 0, blocked: 0 };
  for (const item of backlog.items) {
    if (summary[item.queue_status] !== undefined) summary[item.queue_status] += 1;
  }
  return summary;
}

function markItemSelected(backlog, itemId, details) {
  const item = backlog.items.find((entry) => entry.id === itemId);
  if (!item) throw new Error(`Backlog item not found: ${itemId}`);

  item.queue_status = 'in_progress';
  item.last_selected_at = new Date().toISOString();
  item.last_stage = details.stage || item.last_stage || null;
  item.blocked_reason = null;
  item.queue_history.push({
    event: 'selected',
    at: item.last_selected_at,
    stage: details.stage || null,
    article_file: details.article_file || item.suggested_article_file,
    run_id: details.run_id || null,
  });
  return item;
}

function updateItemAfterStage(backlog, itemId, details) {
  const item = backlog.items.find((entry) => entry.id === itemId);
  if (!item) return null;

  const at = new Date().toISOString();
  item.last_stage = details.stage || item.last_stage || null;

  if (details.stage === 'publish' && details.status === 'completed') {
    item.queue_status = 'completed';
    item.completed_at = at;
    item.blocked_reason = null;
    item.queue_history.push({ event: 'completed', at, summary: details.summary || '' });
    return item;
  }

  if (details.status === 'blocked') {
    item.queue_status = 'blocked';
    item.blocked_reason = details.summary || 'Blocked during stage completion.';
    item.queue_history.push({ event: 'blocked', at, stage: details.stage || null, summary: details.summary || '' });
    return item;
  }

  item.queue_status = 'in_progress';
  item.queue_history.push({
    event: 'stage_completed',
    at,
    stage: details.stage || null,
    next_stage: details.next_stage || null,
    summary: details.summary || '',
  });
  return item;
}

module.exports = {
  buildBacklog,
  compareBacklogItems,
  compareInProgressItems,
  findInProgressItem,
  findNextItem,
  summarizeBacklog,
  markItemSelected,
  updateItemAfterStage,
};
