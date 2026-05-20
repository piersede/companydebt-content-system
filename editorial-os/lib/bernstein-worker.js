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
  if (page.mode === 'wp_post' || state.mode === 'wp_post') {
    // Synthesize a task-entry brief for wp-post mode (editorial_task_entry.py requires a
    // cc_builder page config which doesn't exist for WordPress posts).
    const wpPostId = state.wp_post_id || page.wp_post_id;
    writeMarkdown(taskEntryPath, [
      `# Task Entry: ${state.page_id}`,
      '',
      `- Mode: \`wp_post\``,
      `- Task: \`${stageTask}\``,
      `- Title: ${state.title || page.title || state.slug}`,
      `- WP post id: \`${wpPostId}\``,
      `- Slug: \`${state.slug}\``,
      `- Article file: \`${state.article_file}\``,
      `- Target URL: \`${state.target_url}\``,
      '',
      '## Runtime Path',
      '- runtime-packs/writer-core.md',
      '- runtime-packs/wp-post-rewrite.md (if available; otherwise rely on canonical refs)',
      '',
      '## Canonical References',
      '- editorial-os/16-pre-publish-gate.md',
      '- editorial-os/10-evidence-governance.md',
      '- editorial-os/13-readability-governance.md',
      '- editorial-os/28-htag-semantic-framework.md',
      '',
      '## Operator Rule',
      '- Quality kernel is non-negotiable: voice, evidence governance, FAQ-final discipline, and the article_audit gate must all pass.',
    ]);
  } else {
    runPython([
      path.join('scripts', 'editorial_task_entry.py'),
      '--page',
      state.page_id,
      '--task',
      stageTask,
      '--output',
      taskEntryPath,
    ]);
  }

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
  const isWpPost = state.mode === 'wp_post' || page.mode === 'wp_post';
  const wpPostId = state.wp_post_id || page.wp_post_id;
  const commands = isWpPost
    ? [
        `- Pull fresh from staging: \`python tmp/wp_pull.py ${state.slug}\` (writes to tmp/pulls/, then copy to drafts/)`,
        `- Quality gate (Tier 2 mechanical): \`python scripts/article_audit.py --drafts drafts --slug ${wpPostId}\``,
        `- Quality gate with HARD FAIL output: \`python scripts/article_audit.py --drafts drafts --slug ${wpPostId} --gate-format\``,
        `- Push to staging: \`python scripts/wp_push.py --id ${wpPostId} --file ${state.article_file}\``,
      ]
    : [
        `- Build preview: \`python scripts/build_page.py --page ${state.page_id} --preview\``,
        `- Quality check: \`python scripts/quality_check.py --page ${state.page_id}\``,
        `- Publish: \`python scripts/build_page.py --page ${state.page_id} --publish\``,
      ];
  writeMarkdown(processChecklistPath, [
    `# Process Checklist: ${state.page_id}`,
    '',
    '- Bernstein is the conductor. It manages sequence, checkpoints, and state.',
    '- Use Company Debt runtime packs and scripts. Do not invent a parallel workflow.',
    '- Keep revisions bounded when the findings are bounded.',
    '- Regenerate the packet if the thread drifts or the working set gets noisy.',
    ...(isWpPost ? ['- Mode: **wp_post** — operate on the rendered HTML in `drafts/`. Gate uses `scripts/article_audit.py`. Publish uses `scripts/wp_push.py`.'] : []),
    '',
    '## Commands',
    ...commands,
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

async function publishWordPressArticle({ page, state, pageId }) {
  // Back-compat: legacy callers may pass {pageId} directly. Resolve to a page object.
  const resolvedPage = page || (pageId ? findRegistryItem(pageId) : null);
  if (!resolvedPage) {
    return { ok: false, reason: `Unknown page for publish: ${pageId || '(none)'}` };
  }

  let pythonArgs;
  if (resolvedPage.mode === 'wp_post') {
    // WP-post mode: push the rendered HTML draft via scripts/wp_push.py.
    const articleFile = state && state.article_file
      ? state.article_file
      : path.join(ROOT, 'drafts', `${resolvedPage.wp_post_id}_${resolvedPage.slug}.html`);
    pythonArgs = [
      path.join('scripts', 'wp_push.py'),
      '--id', String(resolvedPage.wp_post_id),
      '--file', articleFile,
    ];
  } else {
    // cc_builder mode (legacy): build_page.py --publish.
    pythonArgs = [
      path.join('scripts', 'build_page.py'),
      '--page',
      String(resolvedPage.page_id),
      '--publish',
    ];
  }

  const result = spawnPython(pythonArgs, { timeout: 240000 });

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
    mode: resolvedPage.mode === 'wp_post' ? 'wp_publish' : 'publish',
    output: (result.stdout || '').trim(),
  };
}

module.exports = {
  createWorkerBundle,
  publishWordPressArticle,
};
