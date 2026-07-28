#!/usr/bin/env node
'use strict';

const Anthropic = require('@anthropic-ai/sdk');
const crypto = require('crypto');

const cfg = {
  supabaseUrl: process.env.SUPABASE_URL,
  anonKey: process.env.SUPABASE_ANON_KEY,
  agentId: process.env.WORKER_AGENT_ID || 'AGENT-CLAUDE-REVIEWER-01@PRODUCTION',
  enrollmentSecret: process.env.WORKER_ENROLLMENT_SECRET,
  anthropicKey: process.env.ANTHROPIC_API_KEY,
  model: process.env.CLAUDE_REVIEWER_MODEL || 'claude-sonnet-4-20250514',
  pollMs: Number(process.env.WORKER_POLL_MS || 30000),
  heartbeatMs: Number(process.env.WORKER_HEARTBEAT_MS || 15000),
};

for (const [k, v] of Object.entries({SUPABASE_URL: cfg.supabaseUrl, SUPABASE_ANON_KEY: cfg.anonKey, WORKER_ENROLLMENT_SECRET: cfg.enrollmentSecret, ANTHROPIC_API_KEY: cfg.anthropicKey})) {
  if (!v) throw new Error(`${k} is required`);
}

let accessToken = null;
let tokenExpiresAt = 0;
let currentTaskId = null;
let currentLane = null;
let currentClaimId = null;
const sessionId = crypto.randomUUID();
const anthropic = new Anthropic({ apiKey: cfg.anthropicKey });

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
  const token = await obtainToken();
  try {
    return await jsonFetch(`${cfg.supabaseUrl}/rest/v1/rpc/${name}`, {
      method: 'POST',
      headers: {apikey: cfg.anonKey, Authorization: `Bearer ${token}`, 'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    });
  } catch (err) {
    if (/401|JWT|token/i.test(String(err))) {
      await obtainToken(true);
      return jsonFetch(`${cfg.supabaseUrl}/rest/v1/rpc/${name}`, {
        method: 'POST',
        headers: {apikey: cfg.anonKey, Authorization: `Bearer ${accessToken}`, 'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
      });
    }
    throw err;
  }
}

async function heartbeat(status = 'idle', metrics = {}) {
  return rpc('v7_worker_heartbeat', {
    p_status: status,
    p_current_task_id: currentTaskId,
    p_current_lane: currentLane,
    p_model_version: cfg.model,
    p_capabilities: {architecture_review: true, communication_smoke_test: true},
    p_metrics: {...metrics, session_id: sessionId, pid: process.pid},
  });
}

async function executeTask(task) {
  const packet = task.runtime_packet || {};
  const instruction = packet.instruction || `Return a concise completion acknowledgment for task ${task.task_id}.`;
  const response = await anthropic.messages.create({
    model: cfg.model,
    max_tokens: Math.min(Number(packet.max_tokens || 1200), 4000),
    messages: [{role: 'user', content: instruction}],
  });
  return {
    task_id: task.task_id,
    agent_id: cfg.agentId,
    session_id: sessionId,
    model: cfg.model,
    completed_at: new Date().toISOString(),
    output_text: response.content.filter(x => x.type === 'text').map(x => x.text).join('\n'),
    usage: response.usage,
  };
}

async function cycle() {
  const rows = await rpc('v7_worker_claim_next_task', {p_visibility_timeout_seconds: 1800});
  const task = Array.isArray(rows) ? rows[0] : rows;
  if (!task || !task.claim_id) return;
  currentTaskId = task.task_id;
  currentLane = task.lane;
  currentClaimId = task.claim_id;
  await heartbeat('running', {phase: 'claimed'});
  try {
    const output = await executeTask(task);
    await rpc('v7_worker_submit_result', {
      p_claim_id: Number(task.claim_id),
      p_event_type: 'worker_completed',
      p_output: output,
      p_worker_session_id: sessionId,
    });
    await heartbeat('idle', {phase: 'submitted', last_task_id: task.task_id});
  } catch (err) {
    await rpc('v7_worker_release_claim', {p_claim_id: Number(task.claim_id), p_reason: `worker_error:${String(err).slice(0,500)}`});
    await heartbeat('error', {phase: 'released', error: String(err).slice(0,500)});
    throw err;
  } finally {
    currentTaskId = null;
    currentLane = null;
    currentClaimId = null;
  }
}

async function main() {
  await obtainToken(true);
  const who = await rpc('v7_worker_whoami');
  console.log(JSON.stringify({event:'worker_started', agent_id:cfg.agentId, session_id:sessionId, identity:who}));
  setInterval(() => heartbeat(currentTaskId ? 'running' : 'idle').catch(err => console.error('heartbeat_error', err)), cfg.heartbeatMs);
  while (true) {
    try { await cycle(); } catch (err) { console.error('cycle_error', err); }
    await new Promise(r => setTimeout(r, cfg.pollMs));
  }
}

process.on('SIGTERM', async () => { try { await heartbeat('stopping'); } finally { process.exit(0); } });
process.on('SIGINT', async () => { try { await heartbeat('stopping'); } finally { process.exit(0); } });
main().catch(err => { console.error(err); process.exit(1); });
