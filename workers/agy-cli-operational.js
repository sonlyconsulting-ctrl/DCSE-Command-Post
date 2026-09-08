#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const { spawnSync } = require('child_process');

const cfg = {
  supabaseUrl: process.env.SUPABASE_URL,
  anonKey: process.env.SUPABASE_ANON_KEY,
  agentId: process.env.WORKER_AGENT_ID || 'antigravity',
  enrollmentSecret: process.env.WORKER_ENROLLMENT_SECRET,
  executable: process.env.AGY_EXECUTABLE || 'agy.exe',
  expectedTaskId: process.env.WORKER_EXPECT_TASK_ID || 'DCSE-ORCH-20260908-007',
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
    p_model_version: 'agy-cli-relay-certification',
    p_capabilities: {one_shot:true, executable_probe:true, deterministic_snapshot:true},
    p_metrics: {...metrics, session_id:sessionId, pid:process.pid},
  });
}

function observeAgyVersion() {
  const r = spawnSync(cfg.executable, ['--version'], {encoding:'utf8', windowsHide:true, shell:false, timeout:15000});
  if (r.error || r.status !== 0) throw new Error(`AGY_VERSION_FAILED:${r.error || r.stderr || r.status}`);
  const version = String(r.stdout || '').trim();
  if (!version) throw new Error('AGY_VERSION_EMPTY');
  return version;
}

function first(raw) { return Array.isArray(raw) ? (raw[0] || null) : raw; }

async function main() {
  await obtainToken(true);
  const who = await rpc('v7_worker_whoami');
  console.log(JSON.stringify({event:'relay_cert_worker_started', agent_id:cfg.agentId, session_id:sessionId, expected_task_id:cfg.expectedTaskId, identity:who}));
  await heartbeat('idle', null, null, {phase:'started'});

  const claimedRows = await rpc('v7_worker_claim_next_task', {p_visibility_timeout_seconds:1800});
  const task = first(claimedRows);
  if (!task || !task.claim_id) throw new Error('NO_TASK_CLAIMED');

  if (task.task_id !== cfg.expectedTaskId) {
    await rpc('v7_worker_release_claim', {p_claim_id:Number(task.claim_id), p_reason:`expected_task_mismatch:${cfg.expectedTaskId}`});
    throw new Error(`EXPECTED_TASK_MISMATCH:${task.task_id}`);
  }

  await heartbeat('running', task.task_id, task.lane, {phase:'claimed', claim_id:task.claim_id});

  try {
    const snapshot = first(await rpc('v7_worker_certification_snapshot'));
    if (!snapshot || snapshot.agent_id !== cfg.agentId || snapshot.read_only !== true) throw new Error('INVALID_CERTIFICATION_SNAPSHOT');

    const agyVersion = observeAgyVersion();
    const output = {
      contract_version:'dcse-inter-agent-v1',
      certification_type:'control_plane_executable_relay',
      task_id:task.task_id,
      claim_id:task.claim_id,
      agent_id:cfg.agentId,
      session_id:sessionId,
      runtime_surface:'agy_windows_cli',
      provider:'antigravity',
      status:'completed',
      agy_version:agyVersion,
      source_asset_hash:task.runtime_packet && task.runtime_packet.source_asset_hash ? task.runtime_packet.source_asset_hash : null,
      read_only:true,
      ps_access:false,
      credential_values_exposed:false,
      deterministic_snapshot:snapshot,
      executable_probe:{command:'agy.exe --version', exit_code:0},
      note:'Model prompt/tool execution intentionally excluded from this relay certification. AGY model noninteractive prompt capability is covered by the separate deterministic smoke test evidence.'
    };

    await rpc('v7_worker_submit_result', {
      p_claim_id:Number(task.claim_id),
      p_event_type:'worker_completed',
      p_output:output,
      p_worker_session_id:sessionId,
    });
    await heartbeat('idle', null, null, {phase:'submitted', last_task_id:task.task_id, claim_id:task.claim_id, agy_version:agyVersion});
    console.log(JSON.stringify({event:'relay_cert_worker_complete', task_id:task.task_id, claim_id:task.claim_id, session_id:sessionId, agy_version:agyVersion}));
    process.exit(0);
  } catch (err) {
    await rpc('v7_worker_release_claim', {p_claim_id:Number(task.claim_id), p_reason:`certification_error:${String(err).slice(0,500)}`});
    await heartbeat('error', null, null, {phase:'released', error:String(err).slice(0,500)});
    throw err;
  }
}

main().catch(err => { console.error('certification_error', err); process.exit(1); });
