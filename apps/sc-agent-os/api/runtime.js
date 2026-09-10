'use strict';

const OLLAMA_URL = process.env.OLLAMA_URL || 'http://127.0.0.1:11434';
const OPERATOR_EMAIL = String(process.env.DCS_OPERATOR_EMAIL || 'sonlyconsulting@gmail.com').toLowerCase();

function parseCookies(req) {
  return Object.fromEntries((req.headers.cookie || '').split(';').map(v => v.trim()).filter(Boolean).map(v => {
    const i = v.indexOf('=');
    return [decodeURIComponent(i < 0 ? v : v.slice(0, i)), decodeURIComponent(i < 0 ? '' : v.slice(i + 1))];
  }));
}

async function validateOperator(req) {
  const authUrl = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
  const authKey = process.env.SUPABASE_ANON_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!authUrl || !authKey) return false;
  const token = parseCookies(req).dcse_at;
  if (!token) return false;
  const response = await fetch(`${authUrl}/auth/v1/user`, {
    headers: {apikey: authKey, Authorization: `Bearer ${token}`}
  });
  if (!response.ok) return false;
  const user = await response.json();
  return String(user.email || '').toLowerCase() === OPERATOR_EMAIL;
}

function runtimeConfig() {
  const mode = String(process.env.DDNA_RUNTIME_MODE || 'legacy').toLowerCase();
  if (!['legacy', 'dedicated', 'compare'].includes(mode)) {
    throw new Error(`Unsupported DDNA_RUNTIME_MODE: ${mode}`);
  }

  const legacy = {
    mode: 'legacy',
    url: process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL,
    key: process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.PABASE_SECRET_KEY,
    schema: 'dcse_cp'
  };
  const dedicated = {
    mode: 'dedicated',
    url: process.env.DDNA_SUPABASE_URL,
    key: process.env.DDNA_SUPABASE_SERVICE_ROLE_KEY,
    schema: 'dcse_ddna_legacy'
  };

  if (!legacy.url || !legacy.key) throw new Error('Legacy Supabase server environment is not configured');
  if (mode !== 'legacy' && (!dedicated.url || !dedicated.key)) {
    throw new Error('Dedicated DDNA server environment is not configured');
  }
  return {mode, legacy, dedicated};
}

async function readJobs(source) {
  const select = 'id,model_id,status,retry_count,duration_ms,created_at';
  const url = `${source.url}/rest/v1/ddna_ollama_jobs?select=${select}&order=created_at.desc,id.asc&limit=10`;
  const response = await fetch(url, {
    headers: {
      apikey: source.key,
      Authorization: `Bearer ${source.key}`,
      'Content-Type': 'application/json',
      'Accept-Profile': source.schema
    }
  });
  if (!response.ok) {
    throw new Error(`DDNA read failed (${source.mode}/${source.schema}): HTTP ${response.status}`);
  }
  const rows = await response.json();
  if (!Array.isArray(rows)) throw new Error('DDNA read returned a non-array payload');
  return rows.map(row => ({
    id: row.id,
    model: row.model_id,
    model_id: row.model_id,
    source_type: null,
    status: row.status,
    retry_count: row.retry_count,
    duration_ms: row.duration_ms,
    created_at: row.created_at
  }));
}

function stableProjection(rows) {
  return JSON.stringify(rows.map(({id, model_id, status, retry_count, duration_ms, created_at}) => ({
    id, model_id, status, retry_count, duration_ms, created_at
  })));
}

async function readOllama() {
  const result = {status: 'unreachable', version: null, models: []};
  try {
    const vr = await fetch(`${OLLAMA_URL}/api/version`, {signal: AbortSignal.timeout(1500)});
    if (vr.ok) {
      const vd = await vr.json();
      result.status = 'reachable';
      result.version = vd.version || null;
    }
    const mr = await fetch(`${OLLAMA_URL}/api/tags`, {signal: AbortSignal.timeout(1500)});
    if (mr.ok) {
      const md = await mr.json();
      result.models = Array.isArray(md.models) ? md.models : [];
    }
  } catch (_) {}
  return result;
}

module.exports = async function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'GET') {
    res.statusCode = 405;
    res.setHeader('Allow', 'GET');
    return res.end(JSON.stringify({error: 'Method not allowed'}));
  }

  try {
    if (!(await validateOperator(req))) {
      res.statusCode = 401;
      return res.end(JSON.stringify({error: 'Unauthorized'}));
    }

    const cfg = runtimeConfig();
    const ollama = await readOllama();

    if (cfg.mode === 'compare') {
      const [legacyJobs, dedicatedJobs] = await Promise.all([readJobs(cfg.legacy), readJobs(cfg.dedicated)]);
      const equivalent = stableProjection(legacyJobs) === stableProjection(dedicatedJobs);
      if (!equivalent) {
        res.statusCode = 409;
        return res.end(JSON.stringify({
          error: 'DDNA comparison mismatch',
          ddna: {mode: 'compare', equivalent: false}
        }));
      }
      res.statusCode = 200;
      return res.end(JSON.stringify({
        ollama,
        jobs: dedicatedJobs,
        ddna: {mode: 'compare', source: 'dedicated', schema: cfg.dedicated.schema, equivalent: true}
      }));
    }

    const source = cfg.mode === 'dedicated' ? cfg.dedicated : cfg.legacy;
    const jobs = await readJobs(source);
    res.statusCode = 200;
    return res.end(JSON.stringify({
      ollama,
      jobs,
      ddna: {mode: cfg.mode, source: source.mode, schema: source.schema}
    }));
  } catch (error) {
    res.statusCode = 500;
    return res.end(JSON.stringify({error: error.message}));
  }
};
