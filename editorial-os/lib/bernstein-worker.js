'use strict';

const fs = require('fs');
const path = require('path');
const { ROOT, STAGE_TASK_MAP, findRegistryItem, resolvePageConfigPath, spawnPython } = require('./bernstein-context');

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function runPython(args) {
  const result = spawnPython(args, { timeout: 240000 });

  if (result.error && ['ENOENT', 'EPERM'].includes(result.error.code)) {
    throw new Error('No Python runtime found. Set PYTHON_BIN or install a Python executable on PATH.');
  }

  if (result.status !== 0) {
    throw new Error((result.stderr || result.stdout || 'Python command failed.').trim());
  }

  return result.stdout.trim();
}

function writeJsonSafe(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function writeMarkdown(filePath, lines) {
  fs.writeFileSync(filePath, `${lines.join('\n')}\n`, 'utf8');
}

async function createWorkerBundle({
  state,
  stage,
  backlogItem,
  runtimeContext,
  runResult,
  qualityProfile,
  packetNotes = [],
  requiredStartCheckpoints = [],
  requiredCompletionCheckpoints = [],
}) {
  const workerDir = path.join(path.dirname(path.dirname(runResult.packet_markdown)), 'worker');
  ensureDir(workerDir);

  const page = findRegistryItem(state.page_id) || findRegistryItem(state.slug);
  if (!page) throw new Error(`Unknown page "${state.page_id}".`);
  const stageTask = STAGE_TASK_MAP[stage] || stage;

  const taskEntryPath = path.join(workerDir, `${stageTask}-task-entry.md`);
  runPython([
    path.join('scripts', 'editorial_task_entry.py'),
    '--page',
    state.page_id,
    '--task',
    stageTask,
    '--output',
    taskEntryPath,
  ]);

  let revisionPacketPath = null;
  if (stage === 'revise') {
    revisionPacketPath = path.join(workerDir, 'revision-packet.md');
    const args = [
      path.join('scripts', 'prepare_revision_packet.py'),
      '--page',
      state.page_id,
      '--task',
      'rewrite',
      '--output',
      revisionPacketPath,
    ];
    if (packetNotes.length) args.push('--notes', ...packetNotes);
    runPython(args);
  }

  const sourceMapPath = path.join(workerDir, 'source-map.json');
  writeJsonSafe(sourceMapPath, {
    backlog_item: backlogItem || null,
    runtime_context: runtimeContext,
    page,
    local_artifacts: {
      preview_html: path.join(ROOT, 'preview', `${page.slug}.html`),
      page_config: resolvePageConfigPath(page),
    },
  });

  const researchBriefPath = path.join(workerDir, 'research-brief.md');
  writeMarkdown(researchBriefPath, [
    `# Worker Brief: ${state.page_id}`,
    '',
    `- Page id: \`${state.page_id}\``,
    `- Published slug: \`${state.slug}\``,
    `- Title: ${page.title || state.page_id}`,
    `- Page type: \`${page.page_type || 'unknown'}\``,
    `- Page class: \`${page.page_class || 'unknown'}\``,
    `- Freshness tier: \`${page.freshness_tier || 'unknown'}\``,
    `- Quality rule: ${qualityProfile}`,
    '',
    '## Stage Control',
    `- Current stage: \`${stage}\``,
    `- Start checkpoints: \`${requiredStartCheckpoints.join(', ') || 'none'}\``,
    `- Completion checkpoints: \`${requiredCompletionCheckpoints.join(', ') || 'none'}\``,
    '',
    '## Runtime Packet',
    `- Task entry: \`${taskEntryPath}\``,
    ...(revisionPacketPath ? [`- Revision packet: \`${revisionPacketPath}\``] : []),
    ...packetNotes.map((note) => `- Note: \`${note}\``),
  ]);

  const processChecklistPath = path.join(workerDir, 'process-checklist.md');
  writeMarkdown(processChecklistPath, [
    `# Process Checklist: ${state.page_id}`,
    '',
    '- Bernstein is the conductor. It manages sequence, checkpoints, and state.',
    '- Use Company Debt runtime packs and scripts. Do not invent a parallel workflow.',
    '- Keep revisions bounded when the findings are bounded.',
    '- Regenerate the packet if the thread drifts or the working set gets noisy.',
    '',
    '## Commands',
    `- Build preview: \`python scripts/build_page.py --page ${state.page_id} --preview\``,
    `- Quality check: \`python scripts/quality_check.py --page ${state.page_id}\``,
    `- Publish: \`python scripts/build_page.py --page ${state.page_id} --publish\``,
  ]);

  const publishPayloadPath = path.join(workerDir, 'publish-payload.json');
  writeJsonSafe(publishPayloadPath, {
    page_id: state.page_id,
    slug: state.slug,
    title_guess: page.title || state.page_id,
    page_type: page.page_type || null,
    wp_page_id: page.wp_page_id || null,
    preview_html: path.join(ROOT, 'preview', `${state.slug}.html`),
    build_command: `python scripts/build_page.py --page ${state.page_id} --preview`,
    publish_command: `python scripts/build_page.py --page ${state.page_id} --publish`,
    status: 'publish',
    ready_for_publish: false,
  });

  const workerSummaryPath = path.join(workerDir, 'worker-summary.md');
  writeMarkdown(workerSummaryPath, [
    `# Worker Summary: ${state.page_id}`,
    '',
    `- Task entry: \`${taskEntryPath}\``,
    ...(revisionPacketPath ? [`- Revision packet: \`${revisionPacketPath}\``] : []),
    `- Research brief: \`${researchBriefPath}\``,
    `- Process checklist: \`${processChecklistPath}\``,
    `- Source map: \`${sourceMapPath}\``,
    `- Publish payload: \`${publishPayloadPath}\``,
  ]);

  return {
    worker_dir: workerDir,
    task_entry: taskEntryPath,
    revision_packet: revisionPacketPath,
    research_brief: researchBriefPath,
    process_checklist: processChecklistPath,
    source_map: sourceMapPath,
    publish_payload: publishPayloadPath,
    worker_summary: workerSummaryPath,
  };
}

async function publishWordPressArticle({ pageId }) {
  const result = spawnPython([
    path.join('scripts', 'build_page.py'),
    '--page',
    String(pageId),
    '--publish',
  ], { timeout: 240000 });

  if (result.error && ['ENOENT', 'EPERM'].includes(result.error.code)) {
    return {
      ok: false,
      reason: 'No Python runtime found. Set PYTHON_BIN or install a Python executable on PATH.',
    };
  }

  if (result.status !== 0) {
    return {
      ok: false,
      reason: (result.stderr || result.stdout || 'Company Debt publish failed.').trim(),
    };
  }

  return {
    ok: true,
    mode: 'publish',
    output: (result.stdout || '').trim(),
  };
}

module.exports = {
  createWorkerBundle,
  publishWordPressArticle,
};
