'use strict';

const fs = require('fs');
const path = require('path');
const { STATE_ROOT, ensureDir } = require('./bernstein-context');

const LEARNING_ROOT = path.join(STATE_ROOT, 'learning');
const FIXES_ROOT = path.join(LEARNING_ROOT, 'fixes');
const LOG_PATH = path.join(LEARNING_ROOT, 'learning-log.jsonl');
const PATTERNS_PATH = path.join(LEARNING_ROOT, 'failure-patterns.json');
const FIXES_PATH = path.join(LEARNING_ROOT, 'effective-fixes.json');
const TUNING_PATH = path.join(LEARNING_ROOT, 'worker-tuning.json');
const LESSONS_PATH = path.join(LEARNING_ROOT, 'lessons.md');

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function readJson(filePath, fallback) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (_) {
    return fallback;
  }
}

function ensureLearningFiles() {
  ensureDir(FIXES_ROOT);
  if (!fs.existsSync(LOG_PATH)) fs.writeFileSync(LOG_PATH, '', 'utf8');
  if (!fs.existsSync(PATTERNS_PATH)) writeJson(PATTERNS_PATH, { generated_at: null, total_events: 0, patterns: [] });
  if (!fs.existsSync(FIXES_PATH)) writeJson(FIXES_PATH, { generated_at: null, total_events: 0, fixes: [] });
  if (!fs.existsSync(TUNING_PATH)) {
    writeJson(TUNING_PATH, {
      generated_at: null,
      workers: {
        research: { notes: [] },
        draft: { notes: [] },
        review: { notes: [] },
        revise: { notes: [] },
        gate: { notes: [] },
        publish: { notes: [] },
      },
    });
  }
  if (!fs.existsSync(LESSONS_PATH)) {
    fs.writeFileSync(
      LESSONS_PATH,
      '# Bernstein Lessons\n\nGenerated: pending\n\n## Top Failure Patterns\n- No failure patterns recorded yet.\n\n## Effective Fixes\n- No fixes recorded yet.\n',
      'utf8',
    );
  }
}

function appendEvent(event) {
  ensureLearningFiles();
  fs.appendFileSync(LOG_PATH, `${JSON.stringify({ at: new Date().toISOString(), ...event })}\n`, 'utf8');
}

function refreshLessons() {
  ensureLearningFiles();
  const patterns = readJson(PATTERNS_PATH, { patterns: [] });
  const fixes = readJson(FIXES_PATH, { fixes: [] });
  const tuning = readJson(TUNING_PATH, { workers: {} });

  const lines = [
    '# Bernstein Lessons',
    '',
    `Generated: ${new Date().toISOString()}`,
    '',
    '## Top Failure Patterns',
  ];

  if (!patterns.patterns.length) {
    lines.push('- No failure patterns recorded yet.');
  } else {
    for (const item of patterns.patterns.slice(0, 12)) {
      lines.push(`- \`${item.key}\` occurred ${item.count} times across ${item.pages.length} page(s).`);
    }
  }

  lines.push('', '## Effective Fixes');
  if (!fixes.fixes.length) {
    lines.push('- No fixes recorded yet.');
  } else {
    for (const item of fixes.fixes.slice(0, 12)) {
      lines.push(`- \`${item.key}\` resolved ${item.count} time(s).`);
    }
  }

  lines.push('', '## Worker Tuning');
  for (const [worker, config] of Object.entries(tuning.workers || {})) {
    lines.push(`### ${worker}`);
    if (!config.notes?.length) lines.push('- No promoted operational notes yet.');
    else for (const note of config.notes.slice(0, 8)) lines.push(`- ${note}`);
    lines.push('');
  }

  fs.writeFileSync(LESSONS_PATH, `${lines.join('\n')}\n`, 'utf8');
}

function updatePattern(filePath, key, pageId, summary) {
  const payload = readJson(filePath, { generated_at: null, total_events: 0, patterns: [], fixes: [] });
  const listKey = payload.patterns ? 'patterns' : 'fixes';
  const items = payload[listKey];
  const existing = items.find((item) => item.key === key);
  if (existing) {
    existing.count += 1;
    if (!existing.pages.includes(pageId)) existing.pages.push(pageId);
    if (summary && !existing.examples.includes(summary)) existing.examples.unshift(summary);
    existing.examples = existing.examples.slice(0, 5);
  } else {
    items.push({ key, count: 1, pages: [pageId], examples: summary ? [summary] : [] });
  }
  items.sort((a, b) => b.count - a.count || String(a.key).localeCompare(String(b.key)));
  payload.generated_at = new Date().toISOString();
  payload.total_events = (payload.total_events || 0) + 1;
  writeJson(filePath, payload);
}

function recordFailure({ pageId, stage, summary, detail, statePath, checkpointIds = [] }) {
  ensureLearningFiles();
  const key = `${stage}-failure`;
  appendEvent({ type: 'failure', page_id: pageId, stage, summary, detail, checkpoints: checkpointIds });
  updatePattern(PATTERNS_PATH, key, pageId, summary || detail || '');

  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const fixPath = path.join(FIXES_ROOT, `${stamp}__${pageId}__${stage}.md`);
  const lines = [
    `# Bernstein Fix Note: ${pageId}`,
    '',
    `- Stage: \`${stage}\``,
    `- State file: \`${statePath || 'n/a'}\``,
    `- Summary: ${summary || 'No summary provided.'}`,
    '',
    '## Failure Detail',
    detail || 'No extra detail recorded.',
    '',
    '## Checkpoints In Scope',
    checkpointIds.length ? checkpointIds.map((id) => `- ${id}`).join('\n') : '- None recorded.',
    '',
    '## Repair Rule',
    '- Bernstein must stay the conductor.',
    '- Fix the underlying page config, preview, or publish packet directly.',
    '- Record the correction and carry the lesson forward into future packets.',
    '',
  ];
  fs.writeFileSync(fixPath, `${lines.join('\n')}\n`, 'utf8');
  refreshLessons();
  return fixPath;
}

function recordFix({ pageId, stage, summary }) {
  ensureLearningFiles();
  const key = `${stage}-fix`;
  appendEvent({ type: 'fix', page_id: pageId, stage, summary });
  updatePattern(FIXES_PATH, key, pageId, summary || '');
  refreshLessons();
}

module.exports = {
  ensureLearningFiles,
  recordFailure,
  recordFix,
  refreshLessons,
};
