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

function sanitizeInputRefs(value) {
  if (value == null) return [];
  if (!Array.isArray(value)) throw new Error('input_refs must be an array');
  if (value.length > 20) throw new Error('too many attachment references (max 20)');

  return value.map((ref, index) => {
    if (!ref || typeof ref !== 'object' || Array.isArray(ref)) {
      throw new Error(`input_refs[${index}] must be an object`);
    }
    // CP Dispatch records metadata/reference information only. Never accept
    // browser-provided binary/base64 content through the task JSON envelope.
    const name = String(ref.name || '').trim();
    if (!name) throw new Error(`input_refs[${index}].name required`);
    if (name.length > 255) throw new Error(`input_refs[${index}].name too long`);
    const size = Number(ref.size || 0);
    if (!Number.isFinite(size) || size < 0) throw new Error(`input_refs[${index}].size invalid`);
    const type = String(ref.type || '').slice(0, 160);
    const attachedAt = ref.attached_at ? String(ref.attached_at) : new Date().toISOString();
    return {
      kind: 'dispatch_attachment_reference',
      name,
      size,
      type,
      attached_at: attachedAt,
      binary_embedded: false
    };
  });
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
    send(res, 405, {error: 'method not allowed', stage: 'method'});
    return;
  }
  if (!SUPABASE_KEY) {
    send(res, 503, {error: 'No database connection', stage: 'configuration'});
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
      assigned_agent_key,
      input_refs
    } = await readJsonBody(req);

    if (!title || !String(title).trim()) {
      send(res, 400, {error: 'title required', stage: 'validation'});
      return;
    }

    let governedInputRefs;
    try { governedInputRefs = sanitizeInputRefs(input_refs); }
    catch (err) {
      send(res, 400, {error: err.message, stage: 'attachment_validation'});
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
      const canonicalAgentKey = String(assigned_agent_key).trim();
      const agentR = await fetch(
        `${base}/agent_registry?agent_key=eq.${encodeURIComponent(canonicalAgentKey)}&select=id,agent_key,status,authorized_lanes&limit=1`,
        {headers}
      );
      if (!agentR.ok) {
        send(res, agentR.status, {error: await agentR.text(), stage: 'agent_lookup'});
        return;
      }
      const agents = await agentR.json();
      if (!agents.length) {
        send(res, 400, {error: `Unknown assigned_agent_key: ${canonicalAgentKey}`, stage: 'agent_lookup'});
        return;
      }
      const agent = agents[0];
      if (agent.status !== 'active') {
        send(res, 409, {error: `Agent is not active: ${canonicalAgentKey}`, stage: 'agent_validation'});
        return;
      }
      if (!Array.isArray(agent.authorized_lanes) || !agent.authorized_lanes.includes(taskLane)) {
        send(res, 409, {error: `Agent ${canonicalAgentKey} is not authorized for lane ${taskLane}`, stage: 'agent_validation'});
        return;
      }
      assignedAgentId = agent.id;
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
      input_refs: governedInputRefs,
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

    // Production trg_route_cp_dispatch_task invokes route_task_assignment after
    // task insertion. That function is idempotent and owns creation of the one
    // executor assignment + assigned telemetry event. Never duplicate that
    // assignment in this API handler.
    const assignmentR = await fetch(
      `${base}/agent_task_assignments?task_id=eq.${task.id}&select=id,task_id,agent_id,status,assignment_role,created_at&order=created_at.asc`,
      {headers}
    );
    if (!assignmentR.ok) {
      send(res, assignmentR.status, {error: await assignmentR.text(), stage: 'assignment_verify', task, task_key: taskKey});
      return;
    }
    const assignments = await assignmentR.json();

    const createdEventR = await fetch(`${base}/agent_task_events`, {
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
          attachment_ref_count: governedInputRefs.length,
          api_contract: 'dcse_cp_profile_explicit_v2'
        }
      })
    });
    if (!createdEventR.ok) {
      send(res, 502, {error: await createdEventR.text(), stage: 'telemetry_create', task, task_key: taskKey, assignments});
      return;
    }

    if (assignedAgentId && assignments.length !== 1) {
      send(res, 502, {
        ok: false,
        error: `Task was created but expected exactly one assignment; found ${assignments.length}`,
        stage: 'assignment_verify',
        task,
        task_key: taskKey,
        assignments
      });
      return;
    }

    send(res, 201, {
      ok: true,
      stage: 'complete',
      task,
      task_key: taskKey,
      assignments,
      attachment_refs: governedInputRefs
    });
  } catch (err) {
    send(res, 500, {error: err.message, stage: 'unhandled'});
  }
};
