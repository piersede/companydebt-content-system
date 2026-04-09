'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
const EDITORIAL_ROOT = path.join(ROOT, 'editorial-os');
const STATE_ROOT = path.join(EDITORIAL_ROOT, 'bernstein-state');

const STAGE_TASK_MAP = {
  research: 'brief',
  draft: 'draft',
  review: 'review',
  revise: 'rewrite',
  gate: 'trust-pass',
  publish: 'deploy',
};

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function pythonCandidates() {
  const preferred = process.env.PYTHON_BIN ? [process.env.PYTHON_BIN] : [];
  return [...preferred, 'python', 'py', 'python3'];
}

function spawnPython(args, options = {}) {
  let lastError = null;
  for (const command of pythonCandidates()) {
    const result = spawnSync(command, args, {
      cwd: ROOT,
      encoding: 'utf8',
      env: { ...process.env, PYTHONUTF8: '1' },
      timeout: 120000,
      ...options,
    });
    if (!result.error) return result;
    lastError = result.error;
    if (!['ENOENT', 'EPERM'].includes(result.error.code)) return result;
  }
  return { status: null, stdout: '', stderr: '', error: lastError || new Error('No Python runtime found.') };
}

function runPython(script) {
  const result = spawnPython(['-c', script]);

  if (result.error && ['ENOENT', 'EPERM'].includes(result.error.code)) {
    throw new Error('No Python runtime found. Set PYTHON_BIN or install a Python executable on PATH.');
  }

  if (result.status !== 0) {
    throw new Error((result.stderr || result.stdout || 'Python command failed.').trim());
  }

  return result.stdout.trim();
}

function loadRegistrySnapshot() {
  const script = [
    'import json, sys',
    'from pathlib import Path',
    'root = Path.cwd()',
    "sys.path.insert(0, str(root / 'scripts'))",
    'from build_page import PAGE_REGISTRY, load_page_config',
    'from page_runtime_metadata import resolve_page_runtime_metadata',
    'items = []',
    'for page_id in sorted(PAGE_REGISTRY.keys()):',
    '    config = load_page_config(page_id)',
    '    slug = config.get("slug", page_id)',
    '    meta = resolve_page_runtime_metadata(config, slug=slug)',
    '    items.append({',
    '        "page_id": page_id,',
    '        "slug": slug,',
    '        "title": config.get("title"),',
    '        "page_type": config.get("page_type"),',
    '        "wp_page_id": config.get("wp_page_id"),',
    '        "verification_date": config.get("verification_date"),',
    '        "page_class": meta.page_class,',
    '        "freshness_tier": meta.freshness_tier,',
    '        "module_path": PAGE_REGISTRY[page_id],',
    '    })',
    'print(json.dumps(items))',
  ].join('\n');

  return JSON.parse(runPython(script));
}

function resolvePageConfigPath(page) {
  const parts = String(page.module_path || '').split('.');
  return path.join(ROOT, 'scripts', ...parts) + '.py';
}

function findRegistryItem(identifier) {
  const needle = String(identifier || '').trim().toLowerCase();
  if (!needle) return null;
  return loadRegistrySnapshot().find((item) => (
    String(item.page_id).toLowerCase() === needle
    || String(item.slug).toLowerCase() === needle
    || `/preview/${String(item.slug).toLowerCase()}` === needle
    || `${String(item.slug).toLowerCase()}.html` === needle
  )) || null;
}

function resolveRuntimeContext(identifier, stage = 'draft') {
  const page = typeof identifier === 'object' && identifier ? identifier : findRegistryItem(identifier);
  if (!page) throw new Error(`Unknown page "${identifier}".`);

  const task = STAGE_TASK_MAP[stage] || stage;
  const script = [
    'import json, sys',
    'from pathlib import Path',
    'root = Path.cwd()',
    "sys.path.insert(0, str(root / 'scripts'))",
    'from runtime_pack_router import resolve_runtime_context',
    `payload = resolve_runtime_context(${JSON.stringify(task)}, `
      + `page_type=${JSON.stringify(page.page_type || null)}, `
      + `slug=${JSON.stringify(page.slug || page.page_id)}, `
      + `page_class=${JSON.stringify(page.page_class || null)}, `
      + `freshness_tier=${JSON.stringify(page.freshness_tier || null)})`,
    'print(json.dumps(payload))',
  ].join('\n');

  return {
    ...page,
    task,
    article_file: path.join(ROOT, 'preview', `${page.slug}.html`),
    target_url: `/preview/${page.slug}`,
    page_config_file: resolvePageConfigPath(page),
    ...JSON.parse(runPython(script)),
  };
}

module.exports = {
  ROOT,
  EDITORIAL_ROOT,
  STATE_ROOT,
  STAGE_TASK_MAP,
  ensureDir,
  findRegistryItem,
  loadRegistrySnapshot,
  resolvePageConfigPath,
  resolveRuntimeContext,
  spawnPython,
};
