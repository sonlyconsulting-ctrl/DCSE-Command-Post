/**
 * Aegis Executive Kernel — API + Inline SPA
 * Task ID: DCSE-PA-MODULE-001-AG01
 * Version: 0.1.0 (Slice 001)
 *
 * Architecture: Zero-dependency Vercel serverless monolith
 * Pattern: Follows SC Agent OS v1.3 established pattern
 * Database: Supabase PostgREST (aegis schema)
 * Auth: Cookie-based Supabase auth (gateway-compatible)
 */

const SUPABASE_URL = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://nevgdyfpxdaloacuutal.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
const AEGIS_VERSION = '0.1.0';

// ---------------------------------------------------------------------------
// Supabase REST helpers
// ---------------------------------------------------------------------------
function sbHeaders() {
  return {
    'apikey': SUPABASE_KEY,
    'Authorization': `Bearer ${SUPABASE_KEY}`,
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
  };
}

function sbBase() { return SUPABASE_URL + '/rest/v1'; }

async function sbGet(table, query) {
  const url = `${sbBase()}/${table}${query ? '?' + query : ''}`;
  const r = await fetch(url, { headers: sbHeaders() });
  if (!r.ok) throw new Error(`Supabase GET ${table}: ${r.status} ${await r.text()}`);
  return r.json();
}

async function sbPost(table, data) {
  const r = await fetch(`${sbBase()}/${table}`, {
    method: 'POST', headers: sbHeaders(), body: JSON.stringify(data)
  });
  if (!r.ok) throw new Error(`Supabase POST ${table}: ${r.status} ${await r.text()}`);
  return r.json();
}

async function sbPatch(table, filter, data) {
  const r = await fetch(`${sbBase()}/${table}?${filter}`, {
    method: 'PATCH', headers: sbHeaders(), body: JSON.stringify(data)
  });
  if (!r.ok) throw new Error(`Supabase PATCH ${table}: ${r.status} ${await r.text()}`);
  return r.json();
}

// ---------------------------------------------------------------------------
// API: Sessions
// ---------------------------------------------------------------------------
async function handleSessionStart(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    try {
      if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
      // Get or create principal
      let principals = await sbGet('principals', 'select=*&limit=1');
      if (!principals.length) {
        principals = await sbPost('principals', {
          display_name: 'DCS Principal',
          primary_email: 'sonlyconsulting@gmail.com',
          linked_emails: ['dseado01@gmail.com'],
          auth_provider: 'google'
        });
      }
      const principal = principals[0];
      // Create new session
      const session = await sbPost('executive_sessions', {
        principal_id: principal.id,
        session_start: new Date().toISOString()
      });
      // Get previous session
      const prevSessions = await sbGet('executive_sessions',
        `select=*&id=neq.${session[0].id}&principal_id=eq.${principal.id}&order=session_start.desc&limit=1`);
      // Close previous session if open
      if (prevSessions.length && !prevSessions[0].session_end) {
        await sbPatch('executive_sessions', `id=eq.${prevSessions[0].id}`,
          { session_end: new Date().toISOString() });
      }
      res.statusCode = 200;
      res.end(JSON.stringify({
        ok: true,
        session: session[0],
        principal,
        previous_session: prevSessions[0] || null
      }));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

async function handleSessionGet(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const sessions = await sbGet('executive_sessions', 'select=*&order=session_start.desc&limit=1');
    const principals = await sbGet('principals', 'select=*&limit=1');
    res.statusCode = 200;
    res.end(JSON.stringify({
      ok: true,
      session: sessions[0] || null,
      principal: principals[0] || null
    }));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

// ---------------------------------------------------------------------------
// API: Missions
// ---------------------------------------------------------------------------
async function handleMissions(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const missions = await sbGet('missions', 'select=*&order=priority.desc');
    res.statusCode = 200;
    res.end(JSON.stringify({ok: true, missions}));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

// ---------------------------------------------------------------------------
// API: Jobs (CRUD + state transitions)
// ---------------------------------------------------------------------------
async function handleJobsList(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const url = new URL(req.url, `http://${req.headers.host}`);
    const status = url.searchParams.get('status');
    const mission = url.searchParams.get('mission_id');
    let query = 'select=*&order=updated_at.desc&limit=100';
    if (status) query += `&status=eq.${status}`;
    if (mission) query += `&mission_id=eq.${mission}`;
    const jobs = await sbGet('jobs', query);
    res.statusCode = 200;
    res.end(JSON.stringify({ok: true, jobs}));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

async function handleJobCreate(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    try {
      if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
      const data = JSON.parse(body);
      if (!data.title) { res.statusCode = 400; res.end(JSON.stringify({error:'title required'})); return; }
      const jobKey = 'AEGIS-' + Date.now().toString(36).toUpperCase();
      const job = await sbPost('jobs', {
        job_key: jobKey,
        mission_id: data.mission_id || null,
        title: data.title,
        purpose: data.purpose || null,
        priority: data.priority || 50,
        executor: data.executor || null,
        status: 'queued',
        provenance: data.provenance || 'aegis-ui',
        requires_approval: data.requires_approval || false,
        deadline: data.deadline || null,
        revenue_relevance: data.revenue_relevance || 0,
        dcs_override: data.dcs_override || 0
      });
      // Record creation event
      await sbPost('job_events', {
        job_id: job[0].id,
        event_type: 'created',
        actor: 'aegis',
        summary: `Job ${jobKey} created: ${data.title}`
      }).catch(() => {});
      res.statusCode = 201;
      res.end(JSON.stringify({ok: true, job: job[0]}));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

async function handleJobTransition(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    try {
      if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
      const { job_id, status, actor, summary } = JSON.parse(body);
      if (!job_id || !status) { res.statusCode = 400; res.end(JSON.stringify({error:'job_id and status required'})); return; }
      const validStates = ['queued','running','waiting_approval','completed','failed','cancelled','archived'];
      if (!validStates.includes(status)) {
        res.statusCode = 400; res.end(JSON.stringify({error:'Invalid status: ' + status})); return;
      }
      // Validate transition
      const current = await sbGet('jobs', `id=eq.${job_id}&select=status`);
      if (!current.length) { res.statusCode = 404; res.end(JSON.stringify({error:'Job not found'})); return; }
      const VALID_TRANSITIONS = {
        queued: ['running','cancelled'],
        running: ['waiting_approval','completed','failed','cancelled'],
        waiting_approval: ['running','completed','failed','cancelled'],
        completed: ['archived'],
        failed: ['queued','archived'],
        cancelled: ['queued','archived'],
        archived: []
      };
      const allowed = VALID_TRANSITIONS[current[0].status] || [];
      if (!allowed.includes(status)) {
        res.statusCode = 409;
        res.end(JSON.stringify({error:`Cannot transition from ${current[0].status} to ${status}`}));
        return;
      }
      const updateData = { status, updated_at: new Date().toISOString() };
      if (status === 'completed') updateData.completed_at = new Date().toISOString();
      const updated = await sbPatch('jobs', `id=eq.${job_id}`, updateData);
      // Record event
      await sbPost('job_events', {
        job_id,
        event_type: 'status_change',
        actor: actor || 'aegis',
        summary: summary || `Status changed to ${status}`
      }).catch(() => {});
      res.statusCode = 200;
      res.end(JSON.stringify({ok: true, job: updated[0]}));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

// ---------------------------------------------------------------------------
// API: Approvals
// ---------------------------------------------------------------------------
async function handleApprovalsList(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const approvals = await sbGet('approvals', 'select=*&order=requested_at.desc');
    res.statusCode = 200;
    res.end(JSON.stringify({ok: true, approvals}));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

async function handleApprovalDecision(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    try {
      if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
      const { approval_id, decision, decided_by, notes } = JSON.parse(body);
      if (!approval_id || !decision) {
        res.statusCode = 400; res.end(JSON.stringify({error:'approval_id and decision required'})); return;
      }
      if (!['approved','rejected'].includes(decision)) {
        res.statusCode = 400; res.end(JSON.stringify({error:'decision must be approved or rejected'})); return;
      }
      const updated = await sbPatch('approvals', `id=eq.${approval_id}`, {
        status: decision,
        decided_at: new Date().toISOString(),
        decided_by: decided_by || 'DCS',
        decision_notes: notes || null
      });
      // If approved and job is waiting_approval, transition to running
      if (decision === 'approved' && updated[0]?.job_id) {
        const job = await sbGet('jobs', `id=eq.${updated[0].job_id}&select=status`);
        if (job.length && job[0].status === 'waiting_approval') {
          await sbPatch('jobs', `id=eq.${updated[0].job_id}`, { status: 'running' });
          await sbPost('job_events', {
            job_id: updated[0].job_id,
            event_type: 'approved',
            actor: decided_by || 'DCS',
            summary: `Approval granted: ${notes || 'No notes'}`
          }).catch(() => {});
        }
      }
      res.statusCode = 200;
      res.end(JSON.stringify({ok: true, approval: updated[0]}));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

// ---------------------------------------------------------------------------
// API: Evidence
// ---------------------------------------------------------------------------
async function handleEvidenceList(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const evidence = await sbGet('evidence', 'select=*&order=created_at.desc&limit=50');
    res.statusCode = 200;
    res.end(JSON.stringify({ok: true, evidence}));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

async function handleEvidenceCreate(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    try {
      if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
      const data = JSON.parse(body);
      if (!data.title || !data.evidence_type) {
        res.statusCode = 400; res.end(JSON.stringify({error:'title and evidence_type required'})); return;
      }
      const evidence = await sbPost('evidence', {
        job_id: data.job_id || null,
        evidence_type: data.evidence_type,
        title: data.title,
        content: data.content || null,
        reference_url: data.reference_url || null,
        reference_sha: data.reference_sha || null,
        metadata: data.metadata || {}
      });
      // Record event if linked to job
      if (data.job_id) {
        await sbPost('job_events', {
          job_id: data.job_id,
          event_type: 'evidence_attached',
          actor: 'aegis',
          summary: `Evidence: ${data.title}`
        }).catch(() => {});
      }
      res.statusCode = 201;
      res.end(JSON.stringify({ok: true, evidence: evidence[0]}));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

// ---------------------------------------------------------------------------
// API: Briefing
// ---------------------------------------------------------------------------
async function handleBriefing(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const { deriveBriefing } = require('../lib/briefing');
    const { getNextBestAction } = require('../lib/scoring');

    // Gather all state
    const [sessions, missions, jobs, events, approvals, principals] = await Promise.all([
      sbGet('executive_sessions', 'select=*&order=session_start.desc&limit=2'),
      sbGet('missions', 'select=*&order=priority.desc'),
      sbGet('jobs', 'select=*&order=updated_at.desc'),
      sbGet('job_events', 'select=*&order=created_at.desc&limit=200'),
      sbGet('approvals', 'select=*&order=requested_at.desc'),
      sbGet('principals', 'select=*&limit=1')
    ]);

    const currentSession = sessions[0] || { id: null, session_start: new Date().toISOString(), last_briefing_at: null };
    const previousSession = sessions[1] || null;

    const nba = getNextBestAction(jobs, missions);

    const briefing = deriveBriefing({
      currentSession,
      previousSession,
      jobs,
      missions,
      events,
      approvals,
      nextBestAction: nba
    });

    // Update last_briefing_at
    if (currentSession.id) {
      await sbPatch('executive_sessions', `id=eq.${currentSession.id}`, {
        last_briefing_at: new Date().toISOString()
      }).catch(() => {});
    }

    res.statusCode = 200;
    res.end(JSON.stringify({ ok: true, briefing, principal: principals[0] || null }));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

// ---------------------------------------------------------------------------
// API: Next Best Action
// ---------------------------------------------------------------------------
async function handleNextAction(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const { getNextBestAction, rankJobs } = require('../lib/scoring');

    const [jobs, missions] = await Promise.all([
      sbGet('jobs', 'select=*&status=neq.archived'),
      sbGet('missions', 'select=*')
    ]);

    const ranked = rankJobs(jobs, missions);
    const nba = getNextBestAction(jobs, missions);

    res.statusCode = 200;
    res.end(JSON.stringify({ ok: true, next_action: nba, ranked: ranked.slice(0, 10) }));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

// ---------------------------------------------------------------------------
// API: Notifications
// ---------------------------------------------------------------------------
async function handleNotifications(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error:'No database connection'})); return; }
    const notifications = await sbGet('notifications', 'select=*&status=eq.pending&order=created_at.desc&limit=20');
    res.statusCode = 200;
    res.end(JSON.stringify({ok: true, notifications}));
  } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
}

// ---------------------------------------------------------------------------
// API: Health Check
// ---------------------------------------------------------------------------
async function handleHealth(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  const status = { version: AEGIS_VERSION, timestamp: new Date().toISOString(), supabase: !!SUPABASE_KEY };
  if (SUPABASE_KEY) {
    try {
      await sbGet('missions', 'select=id&limit=1');
      status.database = 'connected';
    } catch(e) {
      status.database = 'error';
      status.database_error = e.message;
    }
  } else {
    status.database = 'not_configured';
  }
  res.statusCode = 200;
  res.end(JSON.stringify(status));
}

// ---------------------------------------------------------------------------
// HTML: Inline SPA
// ---------------------------------------------------------------------------
const HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aegis — Executive Operating System</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#0A192F;--navy-mid:#0E2240;--navy-light:#132E54;--navy-border:#1A3A6A;
  --gold:#D4AF37;--gold-dim:#A68B2A;--gold-glow:rgba(212,175,55,0.12);
  --cream:#F5F0E8;--text-dim:#8FA3C0;--text-muted:#4D6A8A;
  --green:#2ECC71;--green-dim:rgba(46,204,113,0.12);
  --amber:#F39C12;--amber-dim:rgba(243,156,18,0.12);
  --red:#E74C3C;--red-dim:rgba(231,76,60,0.12);
  --blue:#3498DB;--blue-dim:rgba(52,152,219,0.12);
  --surface:#0C2240;--surface-2:#122E50;
  --font:'Space Grotesk',sans-serif;--mono:'JetBrains Mono',monospace;
  --r:8px;--rl:12px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);background:var(--navy);color:var(--cream);min-height:100vh;display:flex;flex-direction:column}

/* Header */
.hdr{height:56px;background:var(--navy-mid);border-bottom:1px solid var(--navy-border);display:flex;align-items:center;justify-content:space-between;padding:0 20px;flex-shrink:0;z-index:100}
.hdr-l{display:flex;align-items:center;gap:12px}
.logo{width:36px;height:36px;background:linear-gradient(135deg,var(--gold),var(--gold-dim));border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:var(--navy);flex-shrink:0}
.hdr-title{font-size:16px;font-weight:600;color:var(--cream);letter-spacing:0.5px}
.hdr-sub{font-size:10px;color:var(--gold);font-family:var(--mono);letter-spacing:1.5px;text-transform:uppercase}
.hdr-r{display:flex;align-items:center;gap:10px}
.hdr-badge{font-size:9px;font-weight:600;letter-spacing:.5px;padding:4px 10px;border-radius:4px;display:flex;align-items:center;gap:5px}
.b-green{background:var(--green-dim);color:var(--green);border:1px solid rgba(46,204,113,.2)}
.b-amber{background:var(--amber-dim);color:var(--amber);border:1px solid rgba(243,156,18,.2)}
.b-red{background:var(--red-dim);color:var(--red);border:1px solid rgba(231,76,60,.2)}
.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.cp-btn{font-size:11px;font-weight:600;padding:6px 14px;border-radius:6px;background:var(--navy-light);color:var(--gold);border:1px solid var(--gold-dim);cursor:pointer;text-decoration:none;display:flex;align-items:center;gap:6px;transition:all .2s}
.cp-btn:hover{background:var(--gold-glow);border-color:var(--gold)}

/* Main Layout */
.main{flex:1;display:flex;flex-direction:column;overflow-y:auto;padding:20px;gap:20px}

/* Greeting */
.greeting{text-align:center;padding:24px 0 8px}
.greeting h1{font-size:24px;font-weight:300;color:var(--cream);margin-bottom:4px}
.greeting h1 span{color:var(--gold);font-weight:600}
.greeting p{font-size:13px;color:var(--text-dim)}

/* Cards Grid */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}

/* Card */
.card{background:var(--surface);border:1px solid var(--navy-border);border-radius:var(--rl);padding:20px;transition:border-color .2s}
.card:hover{border-color:var(--gold-dim)}
.card-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.card-title{font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px}
.card-title .icon{font-size:18px}
.card-badge{font-size:9px;font-weight:600;padding:3px 8px;border-radius:3px;letter-spacing:.5px}
.card-body{font-size:12px;color:var(--text-dim);line-height:1.7}

/* Mission Cards */
.mission-card{cursor:pointer}
.mission-card .mission-meta{display:flex;gap:16px;margin-top:12px;font-size:11px;color:var(--text-muted)}
.mission-card .mission-meta span{display:flex;align-items:center;gap:4px}

/* Briefing Panel */
.briefing{background:var(--surface);border:1px solid var(--navy-border);border-radius:var(--rl);padding:20px}
.briefing-section{margin-bottom:16px}
.briefing-section h3{font-size:12px;font-weight:600;color:var(--gold);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;display:flex;align-items:center;gap:6px}
.briefing-item{font-size:12px;color:var(--text-dim);padding:6px 0;border-bottom:1px solid rgba(255,255,255,.04);display:flex;align-items:flex-start;gap:8px}
.briefing-item .bi-dot{width:5px;height:5px;border-radius:50%;background:var(--gold-dim);flex-shrink:0;margin-top:5px}
.briefing-empty{font-size:11px;color:var(--text-muted);font-style:italic}

/* NBA Panel */
.nba{background:linear-gradient(135deg,var(--surface),var(--surface-2));border:1px solid var(--gold-dim);border-radius:var(--rl);padding:20px}
.nba-label{font-size:10px;font-weight:600;color:var(--gold);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px}
.nba-title{font-size:16px;font-weight:600;margin-bottom:6px}
.nba-reason{font-size:12px;color:var(--text-dim);margin-bottom:12px}
.nba-score{font-size:11px;color:var(--gold);font-family:var(--mono)}
.nba-factors{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.nba-factor{font-size:9px;padding:3px 8px;border-radius:3px;background:var(--navy-light);color:var(--text-dim);border:1px solid var(--navy-border)}

/* Jobs Table */
.jobs-table{width:100%;border-collapse:collapse;font-size:11px}
.jobs-table th{text-align:left;padding:8px 10px;font-size:10px;font-weight:600;color:var(--gold);text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid var(--navy-border)}
.jobs-table td{padding:8px 10px;border-bottom:1px solid rgba(255,255,255,.03);color:var(--text-dim)}
.jobs-table tr:hover td{background:rgba(255,255,255,.02)}

/* Status Badges */
.st{font-size:9px;font-weight:600;padding:2px 8px;border-radius:3px;letter-spacing:.3px;display:inline-block}
.st-queued{background:var(--blue-dim);color:var(--blue)}
.st-running{background:var(--green-dim);color:var(--green)}
.st-waiting_approval{background:var(--amber-dim);color:var(--amber)}
.st-completed{background:rgba(46,204,113,.08);color:rgba(46,204,113,.7)}
.st-failed{background:var(--red-dim);color:var(--red)}
.st-cancelled{background:rgba(255,255,255,.05);color:var(--text-muted)}
.st-archived{background:rgba(255,255,255,.03);color:var(--text-muted)}

/* Approvals */
.approval-item{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--navy-light);border-radius:var(--r);margin-bottom:6px;border-left:3px solid var(--amber)}
.approval-info{font-size:12px}
.approval-type{font-size:9px;color:var(--amber);font-family:var(--mono);text-transform:uppercase}
.approval-actions{display:flex;gap:6px}
.btn{font-size:11px;font-weight:600;padding:5px 14px;border-radius:5px;border:none;cursor:pointer;transition:all .2s}
.btn-approve{background:var(--green-dim);color:var(--green);border:1px solid rgba(46,204,113,.3)}
.btn-approve:hover{background:rgba(46,204,113,.25)}
.btn-reject{background:var(--red-dim);color:var(--red);border:1px solid rgba(231,76,60,.3)}
.btn-reject:hover{background:rgba(231,76,60,.25)}
.btn-gold{background:var(--gold-glow);color:var(--gold);border:1px solid var(--gold-dim)}
.btn-gold:hover{background:rgba(212,175,55,.2)}
.btn-sm{font-size:10px;padding:4px 10px}

/* Auth Scaffold */
.auth-gate{display:flex;align-items:center;justify-content:center;min-height:60vh;flex-direction:column;gap:16px}
.auth-gate h2{font-size:20px;font-weight:400;color:var(--cream)}
.auth-gate p{font-size:12px;color:var(--text-dim);max-width:400px;text-align:center}
.auth-btn{display:flex;align-items:center;gap:10px;padding:12px 28px;border-radius:8px;background:white;color:#333;font-size:14px;font-weight:500;border:none;cursor:pointer;transition:all .2s}
.auth-btn:hover{box-shadow:0 4px 12px rgba(0,0,0,.3)}
.auth-btn svg{width:20px;height:20px}

/* Footer */
.footer{padding:12px 20px;text-align:center;font-size:9px;color:var(--text-muted);border-top:1px solid var(--navy-border);font-family:var(--mono)}

/* Loading */
.loading{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--text-dim)}
.spinner{width:14px;height:14px;border:2px solid var(--navy-border);border-top-color:var(--gold);border-radius:50%;animation:spin .6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* Action Distinction */
.action-tag{font-size:8px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;padding:2px 6px;border-radius:2px;margin-left:6px}
.at-rec{background:var(--blue-dim);color:var(--blue)}
.at-proposed{background:var(--amber-dim);color:var(--amber)}
.at-approved{background:var(--green-dim);color:var(--green)}
.at-done{background:rgba(46,204,113,.06);color:rgba(46,204,113,.5)}

/* Responsive: Android-class mobile */
@media(max-width:768px){
  .hdr{padding:0 12px;height:48px}
  .hdr-title{font-size:14px}
  .hdr-sub{display:none}
  .hdr-badge{display:none}
  .main{padding:12px}
  .cards{grid-template-columns:1fr}
  .greeting h1{font-size:20px}
  .nba{padding:14px}
  .briefing{padding:14px}
  .card{padding:14px}
  .jobs-table{font-size:10px}
  .jobs-table th,.jobs-table td{padding:6px 8px}
}

/* Keyboard/Accessibility */
*:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.btn:focus-visible,.cp-btn:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
</style>
</head>
<body>

<!-- Header -->
<div class="hdr">
  <div class="hdr-l">
    <div class="logo">A</div>
    <div>
      <div class="hdr-title">Aegis</div>
      <div class="hdr-sub">Executive Operating System</div>
    </div>
  </div>
  <div class="hdr-r">
    <div id="statusBadge" class="hdr-badge b-amber"><div class="dot" style="background:var(--amber)"></div>INITIALIZING</div>
    <a href="https://os.sonlyconsulting.com" target="_blank" class="cp-btn" title="Open Command Post">
      &#9670; Command Post
    </a>
  </div>
</div>

<!-- Main Content -->
<div class="main" id="mainContent">
  <div class="loading" id="loadingIndicator"><div class="spinner"></div>Initializing Aegis...</div>
</div>

<!-- Footer -->
<div class="footer">
  AEGIS v${AEGIS_VERSION} &middot; DCSE Command Post &middot; Slice 001 &middot; Not for production deployment
</div>

<script>
const API = '/api/aegis';
let state = { session: null, principal: null, missions: [], jobs: [], approvals: [], briefing: null, nba: null };

// ---- API Helpers ----
async function apiGet(path) {
  try {
    const r = await fetch(API + path);
    return await r.json();
  } catch(e) { return { error: e.message }; }
}
async function apiPost(path, data) {
  try {
    const r = await fetch(API + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await r.json();
  } catch(e) { return { error: e.message }; }
}

// ---- Time Helpers ----
function relTime(iso) {
  if (!iso) return '';
  const d = (Date.now() - new Date(iso).getTime()) / 1000;
  if (d < 60) return 'just now';
  if (d < 3600) return Math.floor(d/60) + 'm ago';
  if (d < 86400) return Math.floor(d/3600) + 'h ago';
  return Math.floor(d/86400) + 'd ago';
}

// ---- Status Badge ----
function setBadge(text, cls) {
  const b = document.getElementById('statusBadge');
  const colors = { 'b-green': '--green', 'b-amber': '--amber', 'b-red': '--red' };
  b.className = 'hdr-badge ' + cls;
  b.innerHTML = '<div class="dot" style="background:var(' + (colors[cls]||'--amber') + ')"></div>' + text;
}

// ---- Render Functions ----
function renderGreeting(name) {
  const hour = new Date().getHours();
  const greet = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
  return '<div class="greeting"><h1>' + greet + ', <span>' + (name||'DCS') + '</span></h1><p>Your executive operating system is ready.</p></div>';
}

function renderMissionCard(m, jobCount) {
  const statusCls = m.status === 'active' ? 'b-green' : m.status === 'paused' ? 'b-amber' : 'b-red';
  return '<div class="card mission-card" data-mission="' + m.id + '">' +
    '<div class="card-hdr"><div class="card-title"><span class="icon">' + (m.icon||'\\u{1F3E2}') + '</span>' + m.title + '</div>' +
    '<span class="card-badge ' + statusCls + '">' + m.status.toUpperCase() + '</span></div>' +
    '<div class="card-body">' + (m.description||'') + '</div>' +
    '<div class="mission-meta"><span>\\u25CF Priority: ' + m.priority + '</span><span>\\u25CF Jobs: ' + jobCount + '</span></div></div>';
}

function renderBriefing(b) {
  if (!b) return '<div class="briefing"><div class="card-hdr"><div class="card-title">\\u{1F4CB} Executive Briefing</div></div><div class="briefing-empty">Loading briefing...</div></div>';
  let html = '<div class="briefing"><div class="card-hdr"><div class="card-title">\\u{1F4CB} Executive Briefing</div><span style="font-size:9px;color:var(--text-muted)">Generated ' + relTime(b.generated_at) + '</span></div>';

  // Changes since last
  html += '<div class="briefing-section"><h3>\\u{1F504} ' + b.sections.changes_since_last.title + '</h3>';
  if (b.sections.changes_since_last.items.length) {
    b.sections.changes_since_last.items.forEach(i => {
      html += '<div class="briefing-item"><span class="bi-dot"></span><span>' + i.summary + ' <small style="color:var(--text-muted)">' + relTime(i.timestamp) + '</small></span></div>';
    });
  } else { html += '<div class="briefing-empty">' + b.sections.changes_since_last.empty_message + '</div>'; }
  html += '</div>';

  // Completed
  html += '<div class="briefing-section"><h3>\\u2705 ' + b.sections.completed.title + '</h3>';
  if (b.sections.completed.items.length) {
    b.sections.completed.items.forEach(i => {
      html += '<div class="briefing-item"><span class="bi-dot" style="background:var(--green)"></span><span>' + i.title + ' <small style="color:var(--text-muted)">' + relTime(i.completed_at) + '</small></span></div>';
    });
  } else { html += '<div class="briefing-empty">' + b.sections.completed.empty_message + '</div>'; }
  html += '</div>';

  // Requires approval
  html += '<div class="briefing-section"><h3>\\u{1F6A8} ' + b.sections.requires_approval.title + '</h3>';
  if (b.sections.requires_approval.items.length) {
    b.sections.requires_approval.items.forEach(i => {
      html += '<div class="briefing-item"><span class="bi-dot" style="background:var(--amber)"></span><span>' + i.title + ' <span class="action-tag at-proposed">' + i.approval_type + '</span></span></div>';
    });
  } else { html += '<div class="briefing-empty">' + b.sections.requires_approval.empty_message + '</div>'; }
  html += '</div>';

  // Blockers
  html += '<div class="briefing-section"><h3>\\u{1F6D1} ' + b.sections.blockers.title + '</h3>';
  if (b.sections.blockers.items.length) {
    b.sections.blockers.items.forEach(i => {
      html += '<div class="briefing-item"><span class="bi-dot" style="background:var(--red)"></span><span>' + i.title + ': ' + (i.failure_detail||'No detail') + '</span></div>';
    });
  } else { html += '<div class="briefing-empty">' + b.sections.blockers.empty_message + '</div>'; }
  html += '</div>';

  html += '<div style="font-size:11px;color:var(--text-dim);margin-top:10px;padding-top:10px;border-top:1px solid var(--navy-border)">' + b.summary + '</div>';
  html += '</div>';
  return html;
}

function renderNBA(nba) {
  if (!nba || !nba.job) return '<div class="nba"><div class="nba-label">Next Best Action</div><div class="briefing-empty">No actionable items available.</div></div>';
  const s = nba.score;
  let factorsHtml = '';
  if (s && s.score_components) {
    Object.entries(s.score_components).forEach(([k,v]) => {
      factorsHtml += '<span class="nba-factor">' + k.replace(/_/g,' ') + ': ' + (v.contribution !== undefined ? v.contribution.toFixed(1) : v.raw) + '</span>';
    });
  }
  return '<div class="nba"><div class="nba-label">\\u{1F3AF} Next Best Action</div>' +
    '<div class="nba-title">' + nba.job.title + ' <span class="action-tag at-rec">RECOMMENDED</span></div>' +
    '<div class="nba-reason">' + (s ? s.reason_summary : '') + '</div>' +
    '<div class="nba-score">Score: ' + (s ? s.composite_score.toFixed(2) : '—') + '</div>' +
    '<div class="nba-factors">' + factorsHtml + '</div></div>';
}

function renderJobs(jobs) {
  if (!jobs.length) return '<div class="card"><div class="card-hdr"><div class="card-title">\\u{1F4C4} Active Jobs</div></div><div class="briefing-empty">No active jobs.</div></div>';
  let html = '<div class="card" style="overflow-x:auto"><div class="card-hdr"><div class="card-title">\\u{1F4C4} Active Jobs</div><span class="card-badge b-green">' + jobs.filter(j=>!['archived','completed','cancelled'].includes(j.status)).length + ' ACTIVE</span></div>';
  html += '<table class="jobs-table"><thead><tr><th>Key</th><th>Title</th><th>Status</th><th>Priority</th><th>Updated</th><th>Actions</th></tr></thead><tbody>';
  jobs.filter(j => j.status !== 'archived').slice(0, 20).forEach(j => {
    html += '<tr><td style="color:var(--gold);font-family:var(--mono);font-size:10px">' + j.job_key + '</td>';
    html += '<td style="color:var(--cream)">' + j.title + (j.requires_approval ? ' <span class="action-tag at-proposed">APPROVAL</span>' : '') + '</td>';
    html += '<td><span class="st st-' + j.status + '">' + j.status.replace(/_/g,' ').toUpperCase() + '</span></td>';
    html += '<td>' + j.priority + '</td>';
    html += '<td>' + relTime(j.updated_at) + '</td>';
    html += '<td>';
    if (j.status === 'queued') html += '<button class="btn btn-sm btn-gold" onclick="transitionJob(\\'' + j.id + '\\',\\'running\\')">Start</button>';
    if (j.status === 'running') html += '<button class="btn btn-sm btn-approve" onclick="transitionJob(\\'' + j.id + '\\',\\'completed\\')">Complete</button>';
    if (j.status === 'waiting_approval') html += '<button class="btn btn-sm btn-approve" onclick="transitionJob(\\'' + j.id + '\\',\\'completed\\')">Approve</button>';
    html += '</td></tr>';
  });
  html += '</tbody></table></div>';
  return html;
}

function renderApprovals(approvals) {
  const pending = approvals.filter(a => a.status === 'pending');
  if (!pending.length) return '';
  let html = '<div class="card"><div class="card-hdr"><div class="card-title">\\u{1F510} Pending Approvals</div><span class="card-badge b-amber">' + pending.length + ' PENDING</span></div>';
  pending.forEach(a => {
    html += '<div class="approval-item"><div><div class="approval-info">' + a.title + '</div><div class="approval-type">' + a.approval_type + '</div></div>' +
      '<div class="approval-actions">' +
      '<button class="btn btn-approve btn-sm" onclick="decideApproval(\\'' + a.id + '\\',\\'approved\\')">Approve</button>' +
      '<button class="btn btn-reject btn-sm" onclick="decideApproval(\\'' + a.id + '\\',\\'rejected\\')">Reject</button></div></div>';
  });
  html += '</div>';
  return html;
}

function renderCompletedSummary(jobs) {
  const completed = jobs.filter(j => j.status === 'completed');
  if (!completed.length) return '';
  return '<div class="card"><div class="card-hdr"><div class="card-title">\\u2705 Recently Completed</div><span class="card-badge b-green">' + completed.length + '</span></div>' +
    '<div class="card-body">' + completed.slice(0,5).map(j => '<div class="briefing-item"><span class="bi-dot" style="background:var(--green)"></span>' + j.title + ' <span class="action-tag at-done">DONE</span> <small>' + relTime(j.completed_at) + '</small></div>').join('') + '</div></div>';
}

// ---- Actions ----
async function transitionJob(jobId, status) {
  const r = await apiPost('/jobs/transition', { job_id: jobId, status });
  if (r.ok) await refreshAll();
  else alert('Error: ' + (r.error || 'Unknown'));
}

async function decideApproval(approvalId, decision) {
  const r = await apiPost('/approvals/decide', { approval_id: approvalId, decision, decided_by: 'DCS' });
  if (r.ok) await refreshAll();
  else alert('Error: ' + (r.error || 'Unknown'));
}

// ---- Full Page Render ----
function renderPage() {
  const mc = document.getElementById('mainContent');
  const name = state.principal ? state.principal.display_name : 'DCS';
  let html = renderGreeting(name);
  html += '<div class="cards">';
  state.missions.forEach(m => {
    const jobCount = state.jobs.filter(j => j.mission_id === m.id).length;
    html += renderMissionCard(m, jobCount);
  });
  html += '</div>';
  html += renderNBA(state.nba);
  html += renderBriefing(state.briefing);
  html += renderApprovals(state.approvals);
  html += renderJobs(state.jobs);
  html += renderCompletedSummary(state.jobs);
  mc.innerHTML = html;
}

// ---- Data Loading ----
async function refreshAll() {
  try {
    const [sessionData, missionData, jobData, approvalData, briefingData, nbaData] = await Promise.all([
      apiGet('/session'),
      apiGet('/missions'),
      apiGet('/jobs'),
      apiGet('/approvals'),
      apiGet('/briefing'),
      apiGet('/next-action')
    ]);
    if (sessionData.ok) { state.session = sessionData.session; state.principal = sessionData.principal; }
    if (missionData.ok) state.missions = missionData.missions || [];
    if (jobData.ok) state.jobs = jobData.jobs || [];
    if (approvalData.ok) state.approvals = approvalData.approvals || [];
    if (briefingData.ok) state.briefing = briefingData.briefing || null;
    if (nbaData.ok) state.nba = nbaData.next_action || null;
    setBadge('ONLINE', 'b-green');
    renderPage();
  } catch(e) {
    setBadge('ERROR', 'b-red');
    document.getElementById('mainContent').innerHTML =
      '<div class="auth-gate"><h2>Connection Error</h2><p>' + e.message + '</p></div>';
  }
}

// ---- Initialize ----
async function init() {
  // Start or resume session
  const existing = await apiGet('/session');
  if (existing.ok && existing.session) {
    state.session = existing.session;
    state.principal = existing.principal;
  } else {
    const created = await apiPost('/session/start', {});
    if (created.ok) { state.session = created.session; state.principal = created.principal; }
  }
  await refreshAll();
}

// Keyboard navigation
document.addEventListener('keydown', e => {
  if (e.key === 'r' && e.ctrlKey) { e.preventDefault(); refreshAll(); }
});

init();
</script>
</body>
</html>`;

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------
module.exports = (req, res) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.statusCode = 200; res.end(); return;
  }

  const url = req.url || '';

  // API Routes
  if (url.includes('/api/aegis/session/start') && req.method === 'POST') return handleSessionStart(req, res);
  if (url.includes('/api/aegis/session') && req.method === 'GET') return handleSessionGet(req, res);
  if (url.includes('/api/aegis/missions') && req.method === 'GET') return handleMissions(req, res);
  if (url.includes('/api/aegis/jobs/transition') && req.method === 'POST') return handleJobTransition(req, res);
  if (url.includes('/api/aegis/jobs') && req.method === 'POST') return handleJobCreate(req, res);
  if (url.includes('/api/aegis/jobs') && req.method === 'GET') return handleJobsList(req, res);
  if (url.includes('/api/aegis/approvals/decide') && req.method === 'POST') return handleApprovalDecision(req, res);
  if (url.includes('/api/aegis/approvals') && req.method === 'GET') return handleApprovalsList(req, res);
  if (url.includes('/api/aegis/evidence') && req.method === 'POST') return handleEvidenceCreate(req, res);
  if (url.includes('/api/aegis/evidence') && req.method === 'GET') return handleEvidenceList(req, res);
  if (url.includes('/api/aegis/briefing') && req.method === 'GET') return handleBriefing(req, res);
  if (url.includes('/api/aegis/next-action') && req.method === 'GET') return handleNextAction(req, res);
  if (url.includes('/api/aegis/notifications') && req.method === 'GET') return handleNotifications(req, res);
  if (url.includes('/api/aegis/health') && req.method === 'GET') return handleHealth(req, res);

  // Serve SPA
  res.setHeader('Content-Type', 'text/html;charset=utf-8');
  res.statusCode = 200;
  res.end(HTML);
};
