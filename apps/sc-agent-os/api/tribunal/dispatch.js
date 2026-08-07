const SUPABASE_URL = process.env.SUPABASE_URL || 'https://nevgdyfpxdaloacuutal.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1024 * 1024) {
        reject(new Error('request body too large'));
        req.destroy();
      }
    });
    req.on('end', () => {
      try { resolve(body ? JSON.parse(body) : {}); }
      catch (err) { reject(new Error('invalid JSON body')); }
    });
    req.on('error', reject);
  });
}

function send(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.end(JSON.stringify(payload));
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    res.end();
    return;
  }
  if (req.method !== 'POST') {
    send(res, 405, {error: 'method not allowed'});
    return;
  }
  if (!SUPABASE_KEY) {
    send(res, 503, {error: 'No database connection'});
    return;
  }

  try {
    const {
      title,
      description,
      lane,
      task_type,
      priority,
      assignment_mode,
      assigned_agent_key
    } = await readJsonBody(req);

    if (!title || !String(title).trim()) {
      send(res, 400, {error: 'title required'});
      return;
    }

    const validLanes = ['DCSE','SC','SS','TSL','TRIBUNAL','DDNA','RAG','SYSTEM'];
    const validTypes = ['build','review','rag','database','github','tribunal','qa','synthesis','handoff','decision','monitor','other'];
    const taskLane = validLanes.includes(lane) ? lane : 'DCSE';
    const taskType = validTypes.includes(task_type) ? task_type : 'other';
    const taskKey = 'TRIB-' + Date.now().toString(36).toUpperCase();
    const base = SUPABASE_URL + '/rest/v1';

    // These tables live in dcse_cp, which is exposed through PostgREST but is
    // not the default public schema. Reads and writes must explicitly select it.
    const headers = {
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`,
      'Content-Type': 'application/json',
      'Accept-Profile': 'dcse_cp',
      'Content-Profile': 'dcse_cp',
      'Prefer': 'return=representation'
    };

    let assignedAgentId = null;
    if (assigned_agent_key) {
      const agentR = await fetch(
        `${base}/agent_registry?agent_key=eq.${encodeURIComponent(assigned_agent_key)}&select=id,agent_key,status&limit=1`,
        {headers}
      );
      if (!agentR.ok) {
        send(res, agentR.status, {error: await agentR.text(), stage: 'agent_lookup'});
        return;
      }
      const agents = await agentR.json();
      if (!agents.length) {
        send(res, 400, {error: `Unknown assigned_agent_key: ${assigned_agent_key}`});
        return;
      }
      assignedAgentId = agents[0].id;
    }

    const taskPayload = {
      task_key: taskKey,
      title: String(title).trim(),
      description: description || null,
      lane: taskLane,
      task_type: taskType,
      priority: Math.min(5, Math.max(1, parseInt(priority, 10) || 3)),
      assignment_mode: assignment_mode || 'single',
      assigned_agent_id: assignedAgentId,
      status: assignedAgentId ? 'assigned' : 'planned',
      created_by_label: 'CP Dispatch'
    };

    const createR = await fetch(`${base}/agent_tasks`, {
      method: 'POST', headers, body: JSON.stringify(taskPayload)
    });
    if (!createR.ok) {
      send(res, createR.status, {error: await createR.text(), stage: 'task_create'});
      return;
    }

    const created = await createR.json();
    const task = created[0];
    if (!task?.id) {
      send(res, 502, {error: 'Task insert returned no task id', stage: 'task_create'});
      return;
    }

    // The production AFTER INSERT trigger auto_route_cp_dispatch_task routes
    // CP Dispatch rows into agent_task_assignments. Verify that contract before
    // reporting success to the UI instead of silently accepting an unrouted task.
    const assignmentR = await fetch(
      `${base}/agent_task_assignments?task_id=eq.${task.id}&select=id,task_id,agent_id,status,assignment_role,created_at&order=created_at.asc`,
      {headers}
    );
    const assignments = assignmentR.ok ? await assignmentR.json() : [];

    await fetch(`${base}/agent_task_events`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        task_id: task.id,
        event_type: 'created',
        actor_label: 'CP Dispatch',
        event_summary: `Task dispatched: ${task.title} [${taskKey}]`,
        event_payload: {
          assigned_agent_key: assigned_agent_key || null,
          assignment_count: assignments.length,
          api_contract: 'dcse_cp_profile_explicit_v1'
        }
      })
    }).catch(() => {});

    if (assignedAgentId && assignments.length === 0) {
      send(res, 502, {
        ok: false,
        error: 'Task was created but no assignment row was routed',
        stage: 'assignment_verify',
        task,
        task_key: taskKey
      });
      return;
    }

    send(res, 201, {
      ok: true,
      task,
      task_key: taskKey,
      assignments
    });
  } catch (err) {
    send(res, 500, {error: err.message});
  }
};
