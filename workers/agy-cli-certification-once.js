#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const { spawn, spawnSync } = require('child_process');

const cfg = {
  supabaseUrl: process.env.SUPABASE_URL,
  anonKey: process.env.SUPABASE_ANON_KEY,
  agentId: process.env.WORKER_AGENT_ID || 'antigravity',
  enrollmentSecret: process.env.WORKER_ENROLLMENT_SECRET,
  executable: process.env.AGY_EXECUTABLE || 'agy.exe',
  expectedTaskId: process.env.WORKER_EXPECT_TASK_ID || 'DCSE-ORCH-20260908-007',
  printTimeout: process.env.AGY_PRINT_TIMEOUT || '120s',
  processTimeoutMs: Number(process.env.AGY_PROCESS_TIMEOUT_MS || 150000),
};

for (const [k, v] of Object.entries({SUPABASE_URL: cfg.supabaseUrl, SUPABASE_ANON_KEY: cfg.anonKey, WORKER_ENROLLMENT_SECRET: cfg.enrollmentSecret})) {
  if (!v) throw new Error(`${k} is required`);
}

let accessToken = null;
let tokenExpiresAt = 0;
const sessionId = crypto.randomUUID();

async function jsonFetch(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = {raw: text}; }
  if (!res.ok) throw new Error(`${res.status} ${url}: ${JSON.stringify(body)}`);
  return body;
}

async function obtainToken(force = false) {
  if (!force && accessToken && Date.now() < tokenExpiresAt - 120000) return accessToken;
  const body = await jsonFetch(`${cfg.supabaseUrl}/functions/v1/v7-worker-token`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json', apikey: cfg.anonKey},
    body: JSON.stringify({agent_id: cfg.agentId, enrollment_secret: cfg.enrollmentSecret}),
  });
  accessToken = body.access_token;
  tokenExpiresAt = (body.expires_at || Math.floor(Date.now()/1000) + body.expires_in) * 1000;
  return accessToken;
}

async function rpc(name, payload = {}) {
  await obtainToken();
  const call = () => jsonFetch(`${cfg.supabaseUrl}/rest/v1/rpc/${name}`, {
    method: 'POST',
    headers: {apikey: cfg.anonKey, Authorization: `Bearer ${accessToken}`, 'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  try { return await call(); }
  catch (err) {
    if (/401|JWT|token/i.test(String(err))) { await obtainToken(true); return call(); }
    throw err;
  }
}

async function heartbeat(status, taskId = null, lane = null, metrics = {}) {
  return rpc('v7_worker_heartbeat', {
    p_status: status,
    p_current_task_id: taskId,
    p_current_lane: lane,
    p_model_version: 'agy-cli-certification',
    p_capabilities: {one_shot: true, tool_free_model_step: true, deterministic_snapshot: true},
    p_metrics: {...metrics, session_id: sessionId, pid: process.pid},
  });
}

function observeAgyVersion() {
  const r = spawnSync(cfg.executable, ['--version'], {encoding: 'utf8', windowsHide: true, shell: false, timeout: 15000});
  if (r.error || r.status !== 0) throw new Error(`AGY_VERSION_FAILED:${r.error || r.stderr || r.status}`);
  return String(r.stdout || '').trim();
}

function runAgyToolFree(payload) {
  return new Promise((resolve, reject) => {
    const instruction = [
      'DCSE bounded certification response.',
      'Do not use tools, shell commands, files, network access, or external actions.',
      'All required facts are supplied below.',
      'Return ONLY the JSON object supplied under EXPECTED_JSON, with identical keys and values. No markdown and no commentary.',
      `EXPECTED_JSON=${JSON.stringify(payload)}`,
    ].join('\n');

    const args = ['--print', instruction, '--output-format', 'json', '--print-timeout', cfg.printTimeout, '--mode', 'plan'];
    const startedAt = new Date().toISOString();
    const child = spawn(cfg.executable, args, {windowsHide: true, shell: false, env: process.env});
    let stdout = '';
    let stderr = '';
    let timedOut = false;
    const timer = setTimeout(() => { timedOut = true; child.kill(); }, cfg.processTimeoutMs);
    child.stdout.on('data', d => { stdout += d.toString(); });
    child.stderr.on('data', d => { stderr += d.toString(); });
    child.on('error', err => { clearTimeout(timer); reject(err); });
    child.on('close', code => {
      clearTimeout(timer);
      let wrapper = null;
      try { wrapper = JSON.parse(stdout.trim()); } catch { wrapper = {raw_stdout: stdout}; }
      resolve({started_at: startedAt, completed_at: new Date().toISOString(), exit_code: code, timed_out: timedOut, wrapper, stderr: stderr.slice(0, 4000)});
    });
  });
}

function normalizeSnapshot(raw) {
  if (Array.isArray(raw)) return raw[0] || null;
  return raw;
}

function parseProviderResponse(wrapper) {
  if (!wrapper || typeof wrapper !== 'object') throw new Error('AGY_INVALID_WRAPPER');
  if (Array.isArray(wrapper.denied_actions) && wrapper.denied_actions.length) throw new Error(`AGY_DENIED_ACTION:${JSON.stringify(wrapper.denied_actions)}`);
  const response = typeof wrapper.response === 'string' ? wrapper.response.trim() : '';
  if (!response) throw new Error('AGY_EMPTY_RESPONSE');
  try { return JSON.parse(response); }
  catch { throw new Error(`AGY_RESPONSE_NOT_JSON:${response.slice(0,500)}`); }
}

function assertEqual(actual, expected) {
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a !== e) throw new Error(`AGY_RESPONSE_MISMATCH expected=${e.slice(0,1200)} actual=${a.slice(0,1200)}`);
}

async function main() {
  await obtainToken(true);
  const who = await rpc('v7_worker_whoami');
  console.log(JSON.stringify({event:'cert_worker_started', agent_id:cfg.agentId, session_id:sessionId, identity:who}));
  await heartbeat('idle', null, null, {phase:'started'});

  const claimedRows = await rpc('v7_worker_claim_next_task', {p_visibility_timeout_seconds: 1800});
  const task = Array.isArray(claimedRows) ? claimedRows[0] : claimedRows;
  if (!task || !task.claim_id) throw new Error('NO_TASK_CLAIMED');

  if (task.task_id !== cfg.expectedTaskId) {
    await rpc('v7_worker_release_claim', {p_claim_id:Number(task.claim_id), p_reason:`expected_task_mismatch:${cfg.expectedTaskId}`});
    throw new Error(`EXPECTED_TASK_MISMATCH:${task.task_id}`);
  }

  await heartbeat('running', task.task_id, task.lane, {phase:'claimed', claim_id:task.claim_id});

  try {
    const snapshot = normalizeSnapshot(await rpc('v7_worker_certification_snapshot'));
    if (!snapshot || snapshot.agent_id !== cfg.agentId || snapshot.read_only !== true) throw new Error('INVALID_CERTIFICATION_SNAPSHOT');

    const agyVersion = observeAgyVersion();
    const expected = {
      task_id: task.task_id,
      project_ref: snapshot.project_ref,
      agy_version: agyVersion,
      source_asset_hash: task.runtime_packet && task.runtime_packet.source_asset_hash ? task.runtime_packet.source_asset_hash : null,
      read_only: true,
      ps_access: false,
      credential_values_exposed: false,
      counts: snapshot.counts,
    };

    const run = await runAgyToolFree(expected);
    if (run.timed_out) throw new Error('AGY_TIMEOUT');
    if (run.exit_code !== 0) throw new Error(`AGY_EXIT_${run.exit_code}:${run.stderr}`);
    const providerResult = parseProviderResponse(run.wrapper);
    assertEqual(providerResult, expected);

    const output = {
      contract_version: 'dcse-inter-agent-v1',
      task_id: task.task_id,
      claim_id: task.claim_id,
      agent_id: cfg.agentId,
      session_id: sessionId,
      runtime_surface: 'agy_windows_cli',
      provider: 'antigravity',
      started_at: run.started_at,
      completed_at: run.completed_at,
      status: 'completed',
      raw_exit_code: run.exit_code,
      timed_out: false,
      deterministic_snapshot: snapshot,
      provider_output: providerResult,
      provider_wrapper_status: run.wrapper.status || null,
      provider_denied_actions: run.wrapper.denied_actions || [],
      stderr: run.stderr,
    };

    await rpc('v7_worker_submit_result', {
      p_claim_id: Number(task.claim_id),
      p_event_type: 'worker_completed',
      p_output: output,
      p_worker_session_id: sessionId,
    });
    await heartbeat('idle', null, null, {phase:'submitted', last_task_id:task.task_id, claim_id:task.claim_id});
    console.log(JSON.stringify({event:'cert_worker_complete', task_id:task.task_id, claim_id:task.claim_id, session_id:sessionId, agy_version:agyVersion}));
    process.exit(0);
  } catch (err) {
    await rpc('v7_worker_release_claim', {p_claim_id:Number(task.claim_id), p_reason:`certification_error:${String(err).slice(0,500)}`});
    await heartbeat('error', null, null, {phase:'released', error:String(err).slice(0,500)});
    throw err;
  }
}

main().catch(err => { console.error('certification_error', err); process.exit(1); });
