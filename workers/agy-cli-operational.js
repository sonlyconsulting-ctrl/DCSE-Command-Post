#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const { spawn } = require('child_process');

const cfg = {
  supabaseUrl: process.env.SUPABASE_URL,
  anonKey: process.env.SUPABASE_ANON_KEY,
  agentId: process.env.WORKER_AGENT_ID || 'antigravity',
  enrollmentSecret: process.env.WORKER_ENROLLMENT_SECRET,
  executable: process.env.AGY_EXECUTABLE || 'agy.exe',
  model: process.env.AGY_MODEL || '',
  pollMs: Number(process.env.WORKER_POLL_MS || 30000),
  heartbeatMs: Number(process.env.WORKER_HEARTBEAT_MS || 15000),
  printTimeout: process.env.AGY_PRINT_TIMEOUT || '5m0s',
  processTimeoutMs: Number(process.env.AGY_PROCESS_TIMEOUT_MS || 330000),
  once: process.env.WORKER_ONCE === '1',
  expectedTaskId: process.env.WORKER_EXPECT_TASK_ID || '',
};

for (const [k, v] of Object.entries({SUPABASE_URL: cfg.supabaseUrl, SUPABASE_ANON_KEY: cfg.anonKey, WORKER_ENROLLMENT_SECRET: cfg.enrollmentSecret})) {
  if (!v) throw new Error(`${k} is required`);
}

let accessToken = null;
let tokenExpiresAt = 0;
let currentTaskId = null;
let currentLane = null;
let activeChild = null;
const sessionId = crypto.randomUUID();

async function jsonFetch(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = { raw: text }; }
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

async function heartbeat(status = 'idle', metrics = {}) {
  return rpc('v7_worker_heartbeat', {
    p_status: status,
    p_current_task_id: currentTaskId,
    p_current_lane: currentLane,
    p_model_version: cfg.model || 'agy-cli',
    p_capabilities: {noninteractive_prompt: true, structured_json: true, sandbox: true, bounded_timeout: true, one_shot: cfg.once},
    p_metrics: {...metrics, session_id: sessionId, pid: process.pid},
  });
}

function runAgy(instruction, packet = {}) {
  return new Promise((resolve, reject) => {
    const args = ['--print', instruction, '--output-format', 'json', '--print-timeout', String(packet.print_timeout || cfg.printTimeout)];
    const roots = Array.isArray(packet.allowed_roots) ? packet.allowed_roots : [];
    for (const root of roots) args.push('--add-dir', String(root));
    if (packet.sandbox !== false) args.push('--sandbox');
    if (packet.mode === 'plan' || packet.mode === 'accept-edits') args.push('--mode', packet.mode);
    if (packet.model || cfg.model) args.push('--model', String(packet.model || cfg.model));
    if (packet.json_schema) args.push('--json-schema', typeof packet.json_schema === 'string' ? packet.json_schema : JSON.stringify(packet.json_schema));

    // Deliberately unsupported here: --dangerously-skip-permissions.
    // Any future use requires an explicit controlling policy change.

    const started = new Date().toISOString();
    const child = spawn(cfg.executable, args, {
      cwd: packet.working_directory || process.cwd(),
      windowsHide: true,
      shell: false,
      env: process.env,
    });
    activeChild = child;
    let stdout = '';
    let stderr = '';
    let timedOut = false;
    const timeoutMs = Math.min(Number(packet.process_timeout_ms || cfg.processTimeoutMs), 3600000);
    const timer = setTimeout(() => { timedOut = true; child.kill(); }, timeoutMs);
    child.stdout.on('data', d => { stdout += d.toString(); });
    child.stderr.on('data', d => { stderr += d.toString(); });
    child.on('error', err => { clearTimeout(timer); activeChild = null; reject(err); });
    child.on('close', code => {
      clearTimeout(timer);
      activeChild = null;
      let parsed = null;
      try { parsed = stdout.trim() ? JSON.parse(stdout) : null; } catch { parsed = {raw_stdout: stdout}; }
      resolve({started_at: started, completed_at: new Date().toISOString(), exit_code: code, timed_out: timedOut, output: parsed, stderr: stderr.slice(0, 4000)});
    });
  });
}

async function executeTask(task) {
  const packet = task.runtime_packet || {};
  if (packet.ps_exposure === true) throw new Error('BLOCKED_POLICY: PS exposure is not authorized for AGY worker');
  if (packet.secret_exposure === true) throw new Error('BLOCKED_POLICY: secret-bearing task envelope is prohibited');
  const instruction = packet.instruction;
  if (!instruction) throw new Error('INVALID_TASK: runtime_packet.instruction is required');
  const run = await runAgy(instruction, packet);
  return {
    contract_version: 'dcse-inter-agent-v1',
    task_id: task.task_id,
    claim_id: task.claim_id,
    agent_id: cfg.agentId,
    session_id: sessionId,
    runtime_surface: 'agy_windows_cli',
    provider: 'antigravity',
    model: packet.model || cfg.model || null,
    started_at: run.started_at,
    completed_at: run.completed_at,
    status: (!run.timed_out && run.exit_code === 0) ? 'completed' : 'failed',
    raw_exit_code: run.exit_code,
    timed_out: run.timed_out,
    provider_output: run.output,
    stderr: run.stderr,
  };
}

async function cycle() {
  const rows = await rpc('v7_worker_claim_next_task', {p_visibility_timeout_seconds: 1800});
  const task = Array.isArray(rows) ? rows[0] : rows;
  if (!task || !task.claim_id) return false;

  if (cfg.expectedTaskId && task.task_id !== cfg.expectedTaskId) {
    await rpc('v7_worker_release_claim', {
      p_claim_id: Number(task.claim_id),
      p_reason: `expected_task_mismatch:${cfg.expectedTaskId}`,
    });
    throw new Error(`EXPECTED_TASK_MISMATCH: claimed ${task.task_id}, expected ${cfg.expectedTaskId}`);
  }

  currentTaskId = task.task_id;
  currentLane = task.lane;
  await heartbeat('running', {phase: 'claimed'});
  try {
    const output = await executeTask(task);
    if (output.timed_out) throw new Error(`AGY_TIMEOUT: ${JSON.stringify(output).slice(0,1500)}`);
    if (output.raw_exit_code !== 0) throw new Error(`AGY_EXIT_${output.raw_exit_code}: ${JSON.stringify(output).slice(0,1500)}`);
    await rpc('v7_worker_submit_result', {
      p_claim_id: Number(task.claim_id),
      p_event_type: 'worker_completed',
      p_output: output,
      p_worker_session_id: sessionId,
    });
    await heartbeat('idle', {phase: 'submitted', last_task_id: task.task_id, exit_code: output.raw_exit_code});
    return true;
  } catch (err) {
    await rpc('v7_worker_release_claim', {p_claim_id: Number(task.claim_id), p_reason: `worker_error:${String(err).slice(0,500)}`});
    await heartbeat('error', {phase: 'released', error: String(err).slice(0,500)});
    throw err;
  } finally {
    currentTaskId = null;
    currentLane = null;
  }
}

async function main() {
  await obtainToken(true);
  const who = await rpc('v7_worker_whoami');
  console.log(JSON.stringify({event:'worker_started', agent_id:cfg.agentId, runtime_surface:'agy_windows_cli', session_id:sessionId, one_shot:cfg.once, expected_task_id:cfg.expectedTaskId || null, identity:who}));
  const heartbeatTimer = setInterval(() => heartbeat(currentTaskId ? 'running' : 'idle').catch(err => console.error('heartbeat_error', err)), cfg.heartbeatMs);

  if (cfg.once) {
    try {
      const claimed = await cycle();
      console.log(JSON.stringify({event:'worker_once_complete', agent_id:cfg.agentId, session_id:sessionId, claimed}));
      clearInterval(heartbeatTimer);
      process.exit(claimed ? 0 : 2);
    } catch (err) {
      clearInterval(heartbeatTimer);
      console.error('cycle_error', err);
      process.exit(1);
    }
  }

  while (true) {
    try { await cycle(); } catch (err) { console.error('cycle_error', err); }
    await new Promise(r => setTimeout(r, cfg.pollMs));
  }
}

async function stop() {
  if (activeChild) activeChild.kill();
  try { await heartbeat('stopping'); } finally { process.exit(0); }
}
process.on('SIGTERM', stop);
process.on('SIGINT', stop);
main().catch(err => { console.error(err); process.exit(1); });
