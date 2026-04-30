#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const {
  STATE_ROOT,
  STAGE_TASK_MAP,
  ensureDir,
  findRegistryItem,
  resolveRuntimeContext,
  spawnPython,
} = require('./lib/bernstein-context');
const {
  buildBacklog,
  findInProgressItem,
  findNextItem,
  summarizeBacklog,
  markItemSelected,
  updateItemAfterStage,
} = require('./lib/bernstein-backlog');
const { ensureLearningFiles, recordFailure, recordFix } = require('./lib/bernstein-learning');
const { createWorkerBundle, publishWordPressArticle } = require('./lib/bernstein-worker');

const ROOT = path.resolve(__dirname, '..');
const BACKLOG_PATH = path.join(STATE_ROOT, 'companydebt-backlog.json');
const STAGE_SEQUENCE = ['research', 'draft', 'review', 'revise', 'humanise', 'gate', 'publish'];
const STAGES = {
  research: { next: ['draft'], budget: 7000, description: 'Ground the page against page config, runtime context, and evidence inputs.' },
  draft: { next: ['review'], budget: 9000, description: 'Produce or update the page draft using the Company Debt runtime packs.' },
  review: { next: ['revise', 'gate'], budget: 5000, description: 'Stress-test the draft against voice, evidence, comparison, and trust rules.' },
  revise: { next: ['review', 'humanise'], budget: 5000, description: 'Apply only the bounded fixes required by review or gate findings.' },
  humanise: { next: ['gate'], budget: 4000, description: 'Restore voice, authorship texture, and human markers after structural revision.' },
  gate: { next: ['publish'], budget: 4000, description: 'Run the Company Debt quality gates and capture failures explicitly.' },
  publish: { next: [], budget: 3000, description: 'Publish through the Company Debt page builder flow and confirm the handoff.' },
};
const CHECKPOINT_DEFS = {
  registry_entry_verified: { stage: 'research', description: 'The page id, published slug, and target preview URL are verified.' },
  research_packet_ready: { stage: 'research', description: 'The brief/task-entry packet exists for the page.' },
  source_inputs_gathered: { stage: 'research', description: 'Research notes, card data context, and editorial rules are gathered.' },
  decision_brief_complete: { stage: 'research', description: 'The user decision tension and info-gain targets are explicit.' },
  draft_file_ready: { stage: 'draft', description: 'A current preview HTML file exists for the page.' },
  runtime_rules_applied: { stage: 'draft', description: 'The draft was built against the correct runtime packs and structure rules.' },
  end_matter_complete: { stage: 'draft', description: 'Verification date, methodology, and required end-matter are present.' },
  review_notes_complete: { stage: 'review', description: 'Review findings or explicit pass rationale are recorded.' },
  revision_changes_applied: { stage: 'revise', description: 'Requested fixes from review or gate have been applied.' },
  humanise_complete: { stage: 'humanise', description: 'Voice and authorship markers restored after revision.' },
  pre_publish_gate_passed: { stage: 'gate', description: 'The Company Debt quality checker passed.' },
  editorial_spot_check_complete: { stage: 'gate', description: 'A final editorial spot check was recorded after the gate.' },
  publish_payload_ready: { stage: 'publish', description: 'Publish payload, metadata, and preview artifact are ready.' },
  wordpress_publish_confirmed: { stage: 'publish', description: 'The page builder publish command completed successfully.' },
  post_publish_checks_complete: { stage: 'publish', description: 'Post-publish verification and follow-up checks are complete.' },
};
const STAGE_START_REQUIREMENTS = {
  research: [],
  draft: ['registry_entry_verified', 'research_packet_ready', 'source_inputs_gathered', 'decision_brief_complete'],
  review: ['draft_file_ready', 'runtime_rules_applied', 'end_matter_complete'],
  revise: ['review_notes_complete'],
  humanise: ['revision_changes_applied'],
  gate: ['draft_file_ready', 'runtime_rules_applied', 'end_matter_complete', 'review_notes_complete', 'humanise_complete'],
  publish: ['pre_publish_gate_passed', 'editorial_spot_check_complete', 'publish_payload_ready'],
};
const STAGE_COMPLETION_REQUIREMENTS = {
  research: ['registry_entry_verified', 'research_packet_ready', 'source_inputs_gathered', 'decision_brief_complete'],
  draft: ['draft_file_ready', 'runtime_rules_applied', 'end_matter_complete'],
  review: ['review_notes_complete'],
  revise: ['revision_changes_applied'],
  humanise: ['humanise_complete'],
  gate: ['pre_publish_gate_passed', 'editorial_spot_check_complete'],
  publish: ['publish_payload_ready', 'wordpress_publish_confirmed', 'post_publish_checks_complete'],
};
const DOWNSTREAM_RESETS = {
  draft: ['humanise_complete', 'pre_publish_gate_passed', 'editorial_spot_check_complete', 'publish_payload_ready', 'wordpress_publish_confirmed', 'post_publish_checks_complete'],
  review: ['humanise_complete', 'pre_publish_gate_passed', 'editorial_spot_check_complete', 'publish_payload_ready', 'wordpress_publish_confirmed', 'post_publish_checks_complete'],
  revise: ['humanise_complete', 'pre_publish_gate_passed', 'editorial_spot_check_complete', 'publish_payload_ready', 'wordpress_publish_confirmed', 'post_publish_checks_complete'],
  gate: ['publish_payload_ready', 'wordpress_publish_confirmed', 'post_publish_checks_complete'],
};

function usage() {
  console.error([
    'Usage:',
    '  node editorial-os/bernstein.js init <page-id-or-slug>',
    '  node editorial-os/bernstein.js packet <page-id-or-slug> <stage> [--note <file>]',
    '  node editorial-os/bernstein.js run <page-id-or-slug> <stage> [--note <file>]',
    '  node editorial-os/bernstein.js complete <page-id-or-slug> <stage> --summary "..." [--next <stage>] [--status completed|blocked]',
    '  node editorial-os/bernstein.js backlog-build',
    '  node editorial-os/bernstein.js backlog-status [--json]',
    '  node editorial-os/bernstein.js resume-next [--process] [--json]',
    '  node editorial-os/bernstein.js run-next <stage>',
    '  node editorial-os/bernstein.js process <page-id-or-slug> <stage> [--note <file>]',
    '  node editorial-os/bernstein.js process-next <stage> [--note <file>]',
    '  node editorial-os/bernstein.js checkpoint-status <page-id-or-slug> [--json]',
    '  node editorial-os/bernstein.js checkpoint-complete <page-id-or-slug> <checkpoint-id> [--note "..."]',
    '  node editorial-os/bernstein.js checkpoint-reset <page-id-or-slug> <checkpoint-id>',
    '  node editorial-os/bernstein.js gate-sync <page-id-or-slug>',
    '  node editorial-os/bernstein.js verify-loop <page-id-or-slug> [--auto-fix] [--max-attempts N]',
    '  node editorial-os/bernstein.js publish <page-id-or-slug>',
    '  node editorial-os/bernstein.js status <page-id-or-slug> [--json]',
  ].join('\n'));
}

function nowIso() { return new Date().toISOString(); }
function writeJson(filePath, value) { ensureDir(path.dirname(filePath)); fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8'); }
function toArray(value) { if (value === undefined) return []; return Array.isArray(value) ? value : [value]; }
function stateDirFor(pageId) { return path.join(STATE_ROOT, pageId); }
function statePathFor(pageId) { return path.join(stateDirFor(pageId), 'state.json'); }

function parseArgs(argv) {
  const positional = [];
  const options = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) { positional.push(token); continue; }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) { options[key] = true; continue; }
    if (options[key] === undefined) options[key] = next;
    else if (Array.isArray(options[key])) options[key].push(next);
    else options[key] = [options[key], next];
    i += 1;
  }
  return { positional, options };
}

function initialCheckpointState() {
  return Object.fromEntries(
    Object.entries(CHECKPOINT_DEFS).map(([id, def]) => [id, { id, stage: def.stage, status: 'pending', completed_at: null, note: '' }]),
  );
}

function ensureCheckpointState(state) {
  if (!state.checkpoints) state.checkpoints = initialCheckpointState();
  for (const [id, def] of Object.entries(CHECKPOINT_DEFS)) {
    if (!state.checkpoints[id]) state.checkpoints[id] = { id, stage: def.stage, status: 'pending', completed_at: null, note: '' };
  }
  return state;
}

function loadBacklog() {
  if (!fs.existsSync(BACKLOG_PATH)) return null;
  return JSON.parse(fs.readFileSync(BACKLOG_PATH, 'utf8'));
}

function saveBacklog(backlog) {
  ensureDir(STATE_ROOT);
  writeJson(BACKLOG_PATH, backlog);
}

function loadState(pageId) {
  const filePath = statePathFor(pageId);
  if (!fs.existsSync(filePath)) return null;
  return ensureCheckpointState(JSON.parse(fs.readFileSync(filePath, 'utf8')));
}

function findPage(identifier) {
  const item = findRegistryItem(identifier);
  if (!item) throw new Error(`Unknown page "${identifier}".`);
  return item;
}

function createBaseState(page) {
  const runtime = resolveRuntimeContext(page, 'draft');
  return ensureCheckpointState({
    version: 1,
    page_id: page.page_id,
    slug: page.slug,
    article_file: runtime.article_file,
    created_at: nowIso(),
    updated_at: nowIso(),
    current_stage: 'research',
    status: 'active',
    backlog_item_id: null,
    target_url: runtime.target_url,
    runtime_context: runtime,
    active_run: null,
    decisions: [],
    open_risks: [],
    stage_history: [],
  });
}

function ensureStateForPage(identifier) {
  const page = findPage(identifier);
  return { page, state: loadState(page.page_id) || createBaseState(page) };
}

function saveState(pageId, state) {
  ensureDir(stateDirFor(pageId));
  state.updated_at = nowIso();
  writeJson(statePathFor(pageId), state);
}

function requireStage(stage) {
  if (!STAGES[stage]) throw new Error(`Unknown stage "${stage}". Expected one of: ${Object.keys(STAGES).join(', ')}`);
}

function assertStageReady(state, stage) {
  requireStage(stage);
  const expected = state.current_stage || 'research';
  if (stage !== expected) throw new Error(`Shortcut blocked: requested "${stage}" but Bernstein expects "${expected}" for ${state.page_id}.`);
  const unmet = (STAGE_START_REQUIREMENTS[stage] || []).filter((id) => state.checkpoints?.[id]?.status !== 'completed');
  if (unmet.length) throw new Error(`Stage blocked: "${stage}" requires checkpoints: ${unmet.join(', ')}.`);
}

function assertStageCompletionReady(state, stage) {
  const unmet = (STAGE_COMPLETION_REQUIREMENTS[stage] || []).filter((id) => state.checkpoints?.[id]?.status !== 'completed');
  if (unmet.length) throw new Error(`Stage completion blocked: "${stage}" still has incomplete checkpoints: ${unmet.join(', ')}.`);
}

function completeCheckpoint(state, checkpointId, note) {
  const item = state.checkpoints[checkpointId];
  if (!item) throw new Error(`Unknown checkpoint "${checkpointId}".`);
  item.status = 'completed';
  item.completed_at = nowIso();
  item.note = note || item.note || '';
  return item;
}

function resetCheckpoint(state, checkpointId) {
  const item = state.checkpoints[checkpointId];
  if (!item) throw new Error(`Unknown checkpoint "${checkpointId}".`);
  item.status = 'pending';
  item.completed_at = null;
  item.note = '';
  return item;
}

function resetDownstreamCheckpoints(state, stage, reason) {
  for (const checkpointId of DOWNSTREAM_RESETS[stage] || []) {
    if (!state.checkpoints[checkpointId]) continue;
    state.checkpoints[checkpointId].status = 'pending';
    state.checkpoints[checkpointId].completed_at = null;
    state.checkpoints[checkpointId].note = reason || '';
  }
}

function ensureBacklog() {
  ensureLearningFiles();
  const backlog = buildBacklog(loadBacklog());
  saveBacklog(backlog);
  return backlog;
}

function readOptionalExcerpt(filePath, maxLines = 20) {
  const resolved = path.resolve(filePath);
  if (!fs.existsSync(resolved)) return { file: resolved, excerpt: ['File not found.'] };
  return { file: resolved, excerpt: fs.readFileSync(resolved, 'utf8').split(/\r?\n/).slice(0, maxLines).map((line) => line.trimEnd()) };
}

function checkpointStatusOutput(state) {
  const lines = [
    `# Bernstein Checkpoints: ${state.page_id}`,
    '',
    `- Published slug: \`${state.slug}\``,
    `- Current stage: \`${state.current_stage}\``,
    `- Preview file: \`${state.article_file}\``,
    '',
  ];
  for (const stage of STAGE_SEQUENCE) {
    const ids = Object.entries(CHECKPOINT_DEFS).filter(([, def]) => def.stage === stage).map(([id]) => id);
    if (!ids.length) continue;
    lines.push(`## ${stage}`);
    for (const id of ids) {
      const item = state.checkpoints[id];
      const marker = item.status === 'completed' ? 'x' : ' ';
      const note = item.note ? ` - ${item.note}` : '';
      lines.push(`- [${marker}] \`${id}\`: ${CHECKPOINT_DEFS[id].description}${note}`);
    }
    lines.push('');
  }
  return `${lines.join('\n')}\n`;
}

function statusOutput(state) {
  const lines = [
    `# Bernstein Status: ${state.page_id}`,
    '',
    `- Published slug: \`${state.slug}\``,
    `- Current stage: \`${state.current_stage}\``,
    `- Status: \`${state.status}\``,
    `- Preview file: \`${state.article_file}\``,
    `- Active packet: \`${state.active_run?.packet_markdown || 'none'}\``,
    '',
    '## Stage History',
  ];
  if (!state.stage_history.length) lines.push('- No stages completed yet.');
  else for (const entry of state.stage_history.slice(-10)) lines.push(`- ${entry.stage} -> ${entry.status} (${entry.at})${entry.summary ? ` - ${entry.summary}` : ''}`);
  return `${lines.join('\n')}\n`;
}

function backlogStatusOutput(backlog) {
  const summary = summarizeBacklog(backlog);
  const next = findNextItem(backlog);
  return [
    '# Bernstein Backlog',
    '',
    `- Total: \`${summary.total}\``,
    `- Pending: \`${summary.pending}\``,
    `- In progress: \`${summary.in_progress}\``,
    `- Completed: \`${summary.completed}\``,
    `- Blocked: \`${summary.blocked}\``,
    '',
    '## Next Up',
    next ? `- \`${next.page_id}\` -> \`${next.slug}\` (${next.page_type}, freshness: ${next.freshness_tier || 'unknown'})` : '- No pending items remain.',
    '',
  ].join('\n');
}

function createPacket(page, state, stage, noteFiles) {
  requireStage(stage);
  const runtime = resolveRuntimeContext(page, stage);
  const runId = `${new Date().toISOString().replace(/[:.]/g, '-')}-${stage}`;
  const runDir = path.join(stateDirFor(page.page_id), 'runs', runId);
  ensureDir(runDir);
  const noteExcerpts = noteFiles.map((filePath) => readOptionalExcerpt(filePath));
  const packet = {
    page_id: page.page_id,
    slug: page.slug,
    stage,
    generated_at: nowIso(),
    budget_tokens: STAGES[stage].budget,
    description: STAGES[stage].description,
    current_stage: state.current_stage,
    article_file: state.article_file,
    target_url: state.target_url,
    runtime_context: runtime,
    required_start_checkpoints: STAGE_START_REQUIREMENTS[stage] || [],
    required_completion_checkpoints: STAGE_COMPLETION_REQUIREMENTS[stage] || [],
    notes: noteExcerpts,
  };
  const packetJsonPath = path.join(runDir, 'packet.json');
  const packetMarkdownPath = path.join(runDir, 'packet.md');
  const taskName = STAGE_TASK_MAP[stage] || stage;
  const lines = [
    `# Bernstein Packet: ${page.page_id} / ${stage}`,
    '',
    `- Generated: \`${packet.generated_at}\``,
    `- Published slug: \`${page.slug}\``,
    `- Description: ${packet.description}`,
    `- Preview file: \`${state.article_file}\``,
    `- Target URL: \`${state.target_url}\``,
    '',
    '## Runtime Packs',
    ...(runtime.runtime_packs || []).map((item) => `- ${item}`),
    '',
    '## Canonical References',
    ...(runtime.canonical_refs || []).map((item) => `- ${item}`),
    '',
    '## Checkpoints',
    `- Start requirements: \`${packet.required_start_checkpoints.join(', ') || 'none'}\``,
    `- Completion requirements: \`${packet.required_completion_checkpoints.join(', ') || 'none'}\``,
    '',
    '## Commands',
    `- Task entry: \`python scripts/editorial_task_entry.py --page ${page.page_id} --task ${taskName}\``,
    `- Preview build: \`python scripts/build_page.py --page ${page.page_id} --preview\``,
    `- Quality check: \`python scripts/quality_check.py --page ${page.page_id}\``,
    '',
  ];
  if (noteExcerpts.length) {
    lines.push('## Notes');
    for (const note of noteExcerpts) {
      lines.push(`### ${note.file}`);
      for (const line of note.excerpt) lines.push(`- ${line || '(blank line)'}`);
      lines.push('');
    }
  }
  writeJson(packetJsonPath, packet);
  fs.writeFileSync(packetMarkdownPath, `${lines.join('\n')}\n`, 'utf8');
  state.runtime_context = runtime;
  state.article_file = runtime.article_file;
  state.target_url = runtime.target_url;
  state.active_run = { run_id: runId, stage, started_at: packet.generated_at, packet_markdown: packetMarkdownPath, packet_json: packetJsonPath };
  return { packet_markdown: packetMarkdownPath, packet_json: packetJsonPath };
}

function runPageStage(page, state, stage, options = {}) {
  assertStageReady(state, stage);
  const packet = createPacket(page, state, stage, toArray(options.note).map((item) => path.resolve(item)));
  saveState(page.page_id, state);
  const runDir = path.dirname(packet.packet_json);
  const completeTemplatePath = path.join(runDir, 'complete-template.txt');
  fs.writeFileSync(
    completeTemplatePath,
    `node editorial-os/bernstein.js complete ${page.page_id} ${stage} --summary "..." --next ${STAGES[stage].next[0] || stage}\n`,
    'utf8',
  );
  return { packet_markdown: packet.packet_markdown, packet_json: packet.packet_json, complete_template: completeTemplatePath, next_stages: STAGES[stage].next };
}

function existingProcessBundlePaths(state) {
  const workerDir = path.join(stateDirFor(state.page_id), 'runs', 'worker');
  const stageTask = STAGE_TASK_MAP[state.current_stage] || state.current_stage;
  const taskEntry = path.join(workerDir, `${stageTask}-task-entry.md`);
  const files = {
    worker_dir: workerDir,
    task_entry: taskEntry,
    revision_packet: path.join(workerDir, 'revision-packet.md'),
    research_brief: path.join(workerDir, 'research-brief.md'),
    process_checklist: path.join(workerDir, 'process-checklist.md'),
    source_map: path.join(workerDir, 'source-map.json'),
    publish_payload: path.join(workerDir, 'publish-payload.json'),
    worker_summary: path.join(workerDir, 'worker-summary.md'),
  };
  return Object.fromEntries(Object.entries(files).map(([key, value]) => [key, fs.existsSync(value) ? value : null]));
}

async function prepareProcessBundle(page, state, stage, options = {}, backlogItem = null) {
  const runResult = runPageStage(page, state, stage, options);
  const workerBundle = await createWorkerBundle({
    state,
    stage,
    backlogItem,
    runtimeContext: resolveRuntimeContext(page, stage),
    runResult,
    qualityProfile: 'Preserve the full Company Debt quality bar. Compress context only, never standards.',
    packetNotes: toArray(options.note).map((item) => path.resolve(item)),
    requiredStartCheckpoints: STAGE_START_REQUIREMENTS[stage] || [],
    requiredCompletionCheckpoints: STAGE_COMPLETION_REQUIREMENTS[stage] || [],
  });
  return { ...(backlogItem ? { backlog_item: backlogItem } : {}), ...runResult, process_bundle: workerBundle };
}

function ensureActionableRun(page, state, stage, options = {}) {
  if (state.active_run && state.active_run.stage === stage && fs.existsSync(state.active_run.packet_markdown) && fs.existsSync(state.active_run.packet_json)) {
    const runDir = path.dirname(state.active_run.packet_json);
    return { packet_markdown: state.active_run.packet_markdown, packet_json: state.active_run.packet_json, complete_template: path.join(runDir, 'complete-template.txt'), next_stages: STAGES[stage].next, reused_active_run: true };
  }
  return { ...runPageStage(page, state, stage, options), reused_active_run: false };
}

function runQualityCheck(pageId) {
  const result = spawnPython([path.join('scripts', 'quality_check.py'), '--page', String(pageId)], { timeout: 240000 });
  if (result.error && ['ENOENT', 'EPERM'].includes(result.error.code)) {
    return { exitCode: 1, output: 'No Python runtime found. Set PYTHON_BIN or install a Python executable on PATH.' };
  }
  const output = [result.stdout || '', result.stderr || ''].filter(Boolean).join('\n').trim();
  const summaryMatch = output.match(/SUMMARY:\s+(\d+)\s+pass,\s+(\d+)\s+fail/i);
  const failCount = summaryMatch ? Number(summaryMatch[2]) : (result.status || 0);
  return { exitCode: failCount === 0 ? 0 : 1, output };
}

function syncGateCheckpoints(state, gateResult) {
  if (gateResult.exitCode === 0) {
    completeCheckpoint(state, 'pre_publish_gate_passed', 'Company Debt quality checker passed.');
    completeCheckpoint(state, 'editorial_spot_check_complete', 'Gate passed; editorial spot-check obligations satisfied.');
  } else {
    resetCheckpoint(state, 'pre_publish_gate_passed');
    resetCheckpoint(state, 'editorial_spot_check_complete');
  }
}

function parseHardFails(output) {
  const failures = [];
  for (const match of output.matchAll(/HARD FAIL:\s*(.+?)\s*[—-]\s*(.+)/g)) {
    failures.push({ check: match[1].trim(), detail: match[2].trim() });
  }
  return failures;
}

function buildAutoFixPrompt(pageId, articleFile, failures, attempt) {
  const target = articleFile ? `\`${articleFile}\`` : `page id ${pageId}`;
  return [
    `Fix quality gate HARD FAILs in ${target} for Company Debt page ${pageId}. This is attempt ${attempt}.`,
    '',
    'Rules:',
    '- Fix ONLY the specific failures listed below.',
    '- Do not change structure, add features, rewrite sections, or modify anything not causing a failure.',
    '- Read the file first. Apply minimal targeted edits.',
    '- Do not mark anything as done without verifying the fix.',
    '',
    'HARD FAILs to resolve:',
    ...failures.map((f) => `- ${f.check}: ${f.detail}`),
    '',
    `After fixing, run: python scripts/quality_check.py --page ${pageId}`,
    'The fix is complete only when HARD FAIL count = 0.',
  ].join('\n');
}

function runVerifyLoop(pageId, articleFile, options) {
  const { spawnSync } = require('child_process');
  const maxAttempts = Math.min(parseInt(String(options['max-attempts'] || options.maxAttempts || '5'), 10), 10);
  const autoFix = Boolean(options['auto-fix'] || options.autoFix);
  const { page, state } = ensureStateForPage(pageId);
  if (!state.verification_runs) state.verification_runs = [];

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const gateResult = runQualityCheck(page.page_id);
    const failures = parseHardFails(gateResult.output);
    const run = { attempt, at: nowIso(), exit_code: gateResult.exitCode, failures };
    state.verification_runs.push(run);

    if (gateResult.exitCode === 0) {
      syncGateCheckpoints(state, gateResult);
      saveState(page.page_id, state);
      return { status: 'passed', attempts: attempt, output: gateResult.output };
    }

    if (!autoFix || attempt === maxAttempts) {
      saveState(page.page_id, state);
      return { status: 'failed', attempts: attempt, failures, output: gateResult.output };
    }

    const fixPrompt = buildAutoFixPrompt(page.page_id, articleFile || state.article_file, failures, attempt);
    const stateDir = path.dirname(statePathFor(page.page_id));
    ensureDir(stateDir);
    const fixPromptPath = path.join(stateDir, `fix-prompt-attempt-${attempt}.md`);
    fs.writeFileSync(fixPromptPath, `${fixPrompt}\n`, 'utf8');

    const fixResult = spawnSync('claude', ['-p', fixPrompt], {
      cwd: ROOT, encoding: 'utf8', env: { ...process.env }, timeout: 300000,
    });
    run.fix_applied = fixResult.status === 0;
    run.fix_exit = fixResult.status;
    run.fix_prompt = fixPromptPath;
    if (fixResult.status !== 0) {
      saveState(page.page_id, state);
      return { status: 'fix_error', attempts: attempt, failures, fix_stderr: (fixResult.stderr || '').slice(0, 500) };
    }
  }

  saveState(page.page_id, state);
  return { status: 'failed', attempts: maxAttempts, message: 'Max attempts reached without passing.' };
}

function buildResumeBrief(state, stage, runResult, backlog, selectedItem, processBundle) {
  const bundlePaths = processBundle || existingProcessBundlePaths(state);
  const nextCandidate = findNextItem(backlog);
  return [
    `# Bernstein Resume Brief: ${state.page_id}`,
    '',
    '## Fresh Thread Start',
    '- Continue Bernstein rather than inventing a parallel workflow.',
    '- Bernstein manages packets, checkpoints, and stage order.',
    '- Use Company Debt task-entry and revision packets as the execution layer.',
    '',
    '## Current Assignment',
    `- Page id: \`${state.page_id}\``,
    `- Published slug: \`${state.slug}\``,
    `- Current stage: \`${stage}\``,
    `- Active packet: \`${runResult.packet_markdown}\``,
    `- Completion template: \`${runResult.complete_template}\``,
    runResult.reused_active_run ? '- Packet status: reusing existing active packet for this stage.' : '- Packet status: generated a fresh packet for this stage.',
    '',
    '## Process Artifacts',
    `- Task entry: \`${bundlePaths.task_entry || 'not prepared'}\``,
    `- Revision packet: \`${bundlePaths.revision_packet || 'not prepared'}\``,
    `- Research brief: \`${bundlePaths.research_brief || 'not prepared'}\``,
    `- Process checklist: \`${bundlePaths.process_checklist || 'not prepared'}\``,
    `- Source map: \`${bundlePaths.source_map || 'not prepared'}\``,
    `- Publish payload: \`${bundlePaths.publish_payload || 'not prepared'}\``,
    '',
    '## Commands',
    `- Status: \`node editorial-os/bernstein.js status ${state.page_id}\``,
    `- Checkpoints: \`node editorial-os/bernstein.js checkpoint-status ${state.page_id}\``,
    `- Complete stage: \`node editorial-os/bernstein.js complete ${state.page_id} ${stage} --summary "..." --next ${STAGES[stage].next[0] || stage}\``,
    ...(stage === 'gate' ? [`- Sync gate: \`node editorial-os/bernstein.js gate-sync ${state.page_id}\``] : []),
    ...(stage === 'publish' ? [`- Publish: \`node editorial-os/bernstein.js publish ${state.page_id}\``] : []),
    '',
    '## Queue Context',
    nextCandidate ? `- Next pending backlog item after this one: \`${nextCandidate.page_id}\`` : '- Next pending backlog item after this one: none',
    selectedItem ? `- Active backlog item: \`${selectedItem.id}\`` : '- Active backlog item: none',
    '',
  ].join('\n');
}

async function resumeNextWork(options = {}) {
  const backlog = ensureBacklog();
  const withProcessBundle = Boolean(options.process);
  const inProgressItem = findInProgressItem(backlog);
  const selectedItem = inProgressItem || findNextItem(backlog);
  if (!selectedItem) return { mode: 'idle', message: 'No actionable Bernstein backlog items remain.', backlog_summary: summarizeBacklog(backlog) };

  const { page, state } = ensureStateForPage(selectedItem.page_id);
  state.backlog_item_id = selectedItem.id;
  state.target_url = selectedItem.url;
  const stage = state.current_stage || 'research';
  assertStageReady(state, stage);
  const runResult = ensureActionableRun(page, state, stage, options);
  let processBundle = null;
  if (withProcessBundle) {
    processBundle = await createWorkerBundle({
      state,
      stage,
      backlogItem: selectedItem,
      runtimeContext: resolveRuntimeContext(page, stage),
      runResult,
      qualityProfile: 'Preserve the full Company Debt quality bar. Compress context only, never standards.',
      packetNotes: toArray(options.note).map((item) => path.resolve(item)),
      requiredStartCheckpoints: STAGE_START_REQUIREMENTS[stage] || [],
      requiredCompletionCheckpoints: STAGE_COMPLETION_REQUIREMENTS[stage] || [],
    });
  }

  if (!inProgressItem) markItemSelected(backlog, selectedItem.id, { stage, article_file: state.article_file, run_id: state.active_run?.run_id || null });
  saveState(page.page_id, state);
  saveBacklog(backlog);
  const runDir = path.dirname(runResult.packet_json);
  const briefPath = path.join(runDir, 'resume-brief.md');
  const brief = buildResumeBrief(state, stage, runResult, backlog, selectedItem, processBundle);
  fs.writeFileSync(briefPath, `${brief}\n`, 'utf8');
  return {
    mode: inProgressItem ? 'resume_in_progress' : 'start_next',
    article: state.article_file,
    stage,
    backlog_item: selectedItem,
    packet_markdown: runResult.packet_markdown,
    packet_json: runResult.packet_json,
    complete_template: runResult.complete_template,
    process_bundle: processBundle || existingProcessBundlePaths(state),
    resume_brief: briefPath,
    resume_brief_content: `${brief}\n`,
    reused_active_run: runResult.reused_active_run,
  };
}

function completeStage(state, stage, options = {}) {
  requireStage(stage);
  assertStageCompletionReady(state, stage);
  const status = options.status && options.status !== true ? options.status : 'completed';
  const nextStage = options.next && options.next !== true ? options.next : (status === 'completed' ? (STAGES[stage].next[0] || stage) : stage);
  const summary = options.summary && options.summary !== true ? options.summary : '';
  const entry = { stage, status, at: nowIso(), summary, next_stage: nextStage };
  state.stage_history.push(entry);
  state.status = status === 'blocked' ? 'blocked' : 'active';
  if (status === 'completed' && STAGES[stage].next.length > 0) state.current_stage = nextStage;
  if (status === 'blocked') state.current_stage = stage;
  resetDownstreamCheckpoints(state, stage, `Reset after ${stage} completion.`);
  return entry;
}

async function main() {
  const command = process.argv[2];
  const { positional, options } = parseArgs(process.argv.slice(3));

  try {
    if (!command) { usage(); process.exit(1); }

    if (command === 'init') {
      const identifier = positional[0];
      if (!identifier) throw new Error('Page id or slug is required.');
      const { page, state } = ensureStateForPage(identifier);
      ensureLearningFiles();
      ensureDir(path.join(stateDirFor(page.page_id), 'runs'));
      saveState(page.page_id, state);
      console.log(statePathFor(page.page_id));
      return;
    }

    if (command === 'packet') {
      const identifier = positional[0];
      const stage = positional[1];
      if (!identifier || !stage) throw new Error('Page id or slug and stage are required.');
      const { page, state } = ensureStateForPage(identifier);
      assertStageReady(state, stage);
      const packet = createPacket(page, state, stage, toArray(options.note).map((item) => path.resolve(item)));
      saveState(page.page_id, state);
      console.log(packet.packet_markdown);
      return;
    }

    if (command === 'run') {
      const identifier = positional[0];
      const stage = positional[1];
      if (!identifier || !stage) throw new Error('Page id or slug and stage are required.');
      const { page, state } = ensureStateForPage(identifier);
      console.log(JSON.stringify(runPageStage(page, state, stage, options), null, 2));
      return;
    }

    if (command === 'backlog-build') {
      const backlog = ensureBacklog();
      console.log(BACKLOG_PATH);
      console.log(JSON.stringify(summarizeBacklog(backlog), null, 2));
      return;
    }

    if (command === 'backlog-status') {
      const backlog = ensureBacklog();
      console.log(options.json ? JSON.stringify(backlog, null, 2) : backlogStatusOutput(backlog));
      return;
    }

    if (command === 'resume-next') {
      const result = await resumeNextWork(options);
      console.log(options.json ? JSON.stringify(result, null, 2) : (result.resume_brief_content || result.message));
      return;
    }

    if (command === 'run-next') {
      const stage = positional[0];
      if (!stage) throw new Error('Stage is required.');
      const backlog = ensureBacklog();
      const next = findNextItem(backlog);
      if (!next) {
        console.log(JSON.stringify({ message: 'No pending backlog items remain.' }, null, 2));
        return;
      }
      const { page, state } = ensureStateForPage(next.page_id);
      state.backlog_item_id = next.id;
      state.target_url = next.url;
      const runResult = runPageStage(page, state, stage, options);
      markItemSelected(backlog, next.id, { stage, article_file: state.article_file, run_id: state.active_run?.run_id || null });
      saveState(page.page_id, state);
      saveBacklog(backlog);
      console.log(JSON.stringify({ backlog_item: next, ...runResult }, null, 2));
      return;
    }

    if (command === 'process') {
      const identifier = positional[0];
      const stage = positional[1];
      if (!identifier || !stage) throw new Error('Page id or slug and stage are required.');
      const { page, state } = ensureStateForPage(identifier);
      console.log(JSON.stringify(await prepareProcessBundle(page, state, stage, options), null, 2));
      return;
    }

    if (command === 'process-next') {
      const stage = positional[0];
      if (!stage) throw new Error('Stage is required.');
      const backlog = ensureBacklog();
      const next = findNextItem(backlog);
      if (!next) {
        console.log(JSON.stringify({ message: 'No pending backlog items remain.' }, null, 2));
        return;
      }
      const { page, state } = ensureStateForPage(next.page_id);
      state.backlog_item_id = next.id;
      state.target_url = next.url;
      const processResult = await prepareProcessBundle(page, state, stage, options, next);
      markItemSelected(backlog, next.id, { stage, article_file: state.article_file, run_id: state.active_run?.run_id || null });
      saveState(page.page_id, state);
      saveBacklog(backlog);
      console.log(JSON.stringify(processResult, null, 2));
      return;
    }

    if (command === 'checkpoint-status') {
      const identifier = positional[0];
      if (!identifier) throw new Error('Page id or slug is required.');
      const { state } = ensureStateForPage(identifier);
      console.log(options.json ? JSON.stringify(state.checkpoints, null, 2) : checkpointStatusOutput(state));
      return;
    }

    if (command === 'checkpoint-complete') {
      const identifier = positional[0];
      const checkpointId = positional[1];
      if (!identifier || !checkpointId) throw new Error('Page id or slug and checkpoint id are required.');
      const { page, state } = ensureStateForPage(identifier);
      const result = completeCheckpoint(state, checkpointId, options.note && options.note !== true ? options.note : '');
      saveState(page.page_id, state);
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    if (command === 'checkpoint-reset') {
      const identifier = positional[0];
      const checkpointId = positional[1];
      if (!identifier || !checkpointId) throw new Error('Page id or slug and checkpoint id are required.');
      const { page, state } = ensureStateForPage(identifier);
      const result = resetCheckpoint(state, checkpointId);
      saveState(page.page_id, state);
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    if (command === 'gate-sync') {
      const identifier = positional[0];
      if (!identifier) throw new Error('Page id or slug is required.');
      const { page, state } = ensureStateForPage(identifier);
      const maxAttempts = parseInt(String(options['max-attempts'] || '5'), 10);
      process.stderr.write(`[bernstein] Running quality verify-loop for ${page.page_id}...\n`);
      const loopResult = runVerifyLoop(page.page_id, state.article_file, { 'auto-fix': true, 'max-attempts': String(maxAttempts) });
      if (loopResult.status !== 'passed') {
        recordFailure({
          pageId: page.page_id,
          stage: 'gate',
          summary: 'Quality gate failed during gate-sync.',
          detail: loopResult.output || loopResult.message || '',
          statePath: statePathFor(page.page_id),
          checkpointIds: ['pre_publish_gate_passed', 'editorial_spot_check_complete'],
        });
      } else {
        process.stderr.write(`[bernstein] verify-loop passed after ${loopResult.attempts} attempt(s).\n`);
      }
      const { state: freshState } = ensureStateForPage(page.page_id);
      console.log(JSON.stringify({
        page: page.page_id,
        status: loopResult.status,
        attempts: loopResult.attempts,
        checkpoints: {
          pre_publish_gate_passed: freshState.checkpoints.pre_publish_gate_passed.status,
          editorial_spot_check_complete: freshState.checkpoints.editorial_spot_check_complete.status,
        },
        failures: loopResult.failures || [],
        output: loopResult.output,
      }, null, 2));
      return;
    }

    if (command === 'verify-loop') {
      const identifier = positional[0];
      if (!identifier) throw new Error('Page id or slug is required.');
      const { page, state } = ensureStateForPage(identifier);
      const result = runVerifyLoop(page.page_id, state.article_file, options);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.status === 'passed' ? 0 : 1);
      return;
    }

    if (command === 'publish') {
      const identifier = positional[0];
      if (!identifier) throw new Error('Page id or slug is required.');
      const { page, state } = ensureStateForPage(identifier);
      assertStageReady(state, 'publish');
      const result = await publishWordPressArticle({ pageId: page.page_id });
      if (!result.ok) throw new Error(result.reason);
      completeCheckpoint(state, 'wordpress_publish_confirmed', 'Company Debt build/publish command succeeded.');
      saveState(page.page_id, state);
      console.log(JSON.stringify({ page: page.page_id, result }, null, 2));
      return;
    }

    if (command === 'complete') {
      const identifier = positional[0];
      const stage = positional[1];
      if (!identifier || !stage) throw new Error('Page id or slug and stage are required.');
      const { page, state } = ensureStateForPage(identifier);
      const entry = completeStage(state, stage, options);
      const backlog = loadBacklog();
      if (entry.status === 'blocked') {
        recordFailure({
          pageId: page.page_id,
          stage,
          summary: entry.summary || `${stage} blocked.`,
          detail: entry.summary || 'Blocked during stage completion.',
          statePath: statePathFor(page.page_id),
          checkpointIds: STAGE_COMPLETION_REQUIREMENTS[stage] || [],
        });
      } else {
        recordFix({ pageId: page.page_id, stage, summary: entry.summary || `${stage} completed.` });
      }
      if (backlog && state.backlog_item_id) {
        updateItemAfterStage(backlog, state.backlog_item_id, {
          stage,
          status: entry.status,
          next_stage: entry.next_stage,
          summary: entry.summary,
        });
        saveBacklog(backlog);
      }
      saveState(page.page_id, state);
      console.log(JSON.stringify(entry, null, 2));
      return;
    }

    if (command === 'status') {
      const identifier = positional[0];
      if (!identifier) throw new Error('Page id or slug is required.');
      const { state } = ensureStateForPage(identifier);
      console.log(options.json ? JSON.stringify(state, null, 2) : statusOutput(state));
      return;
    }

    throw new Error(`Unknown command "${command}".`);
  } catch (error) {
    console.error(error.message || String(error));
    usage();
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
