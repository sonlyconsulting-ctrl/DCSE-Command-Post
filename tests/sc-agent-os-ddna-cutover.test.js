'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

function mockReq(method = 'GET') {
  return {method, headers: {cookie: 'dcse_at=test-token'}};
}

function mockRes() {
  return {
    statusCode: 200,
    headers: {},
    body: '',
    setHeader(k, v) { this.headers[k] = v; },
    end(v = '') { this.body = v; return v; }
  };
}

function loadHandler(env) {
  const saved = {...process.env};
  Object.assign(process.env, env);
  delete require.cache[require.resolve('../api/runtime.js')];
  const handler = require('../api/runtime.js');
  return {handler, restore() {
    for (const key of Object.keys(process.env)) if (!(key in saved)) delete process.env[key];
    Object.assign(process.env, saved);
  }};
}

function loadAppHandler(env) {
  const saved = {...process.env};
  Object.assign(process.env, env);
  delete require.cache[require.resolve('../apps/sc-agent-os/api/runtime.js')];
  delete require.cache[require.resolve('../apps/sc-agent-os/api/index.js')];
  const handler = require('../apps/sc-agent-os/api/index.js');
  return {handler, restore() {
    for (const key of Object.keys(process.env)) if (!(key in saved)) delete process.env[key];
    Object.assign(process.env, saved);
  }};
}

function installFetch({legacyRows, dedicatedRows = legacyRows}) {
  const calls = [];
  const oldFetch = global.fetch;
  global.fetch = async (url, options = {}) => {
    calls.push({url: String(url), options});
    const u = String(url);
    if (u.includes('/auth/v1/user')) return {ok: true, json: async () => ({email: 'operator@example.com'})};
    if (u.includes('/api/version') || u.includes('/api/tags')) throw new Error('ollama unavailable');
    if (u.includes('legacy.example')) return {ok: true, json: async () => legacyRows};
    if (u.includes('dedicated.example')) return {ok: true, json: async () => dedicatedRows};
    throw new Error(`unexpected fetch ${u}`);
  };
  return {calls, restore() { global.fetch = oldFetch; }};
}

const rows = [
  {id:'a', model_id:'model-a', status:'failed', retry_count:0, duration_ms:null, created_at:'2026-07-13T21:40:59Z'},
  {id:'b', model_id:'model-b', status:'failed', retry_count:1, duration_ms:null, created_at:'2026-07-13T21:40:59Z'}
];

const baseEnv = {
  DCS_OPERATOR_EMAIL: 'operator@example.com',
  SUPABASE_URL: 'https://legacy.example',
  SUPABASE_ANON_KEY: 'anon-test',
  SUPABASE_SERVICE_ROLE_KEY: 'legacy-service-test',
  DDNA_SUPABASE_URL: 'https://dedicated.example',
  DDNA_SUPABASE_SERVICE_ROLE_KEY: 'dedicated-service-test'
};

test('legacy mode keeps DDNA on legacy project and maps model_id for UI compatibility', async () => {
  const f = installFetch({legacyRows: rows});
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'legacy'});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 200);
    const body = JSON.parse(res.body);
    assert.equal(body.ddna.mode, 'legacy');
    assert.equal(body.jobs[0].model, 'model-a');
    const read = f.calls.find(c => c.url.includes('ddna_ollama_jobs'));
    assert.ok(read.url.startsWith('https://legacy.example'));
    assert.match(read.url, /order=created_at\.desc,id\.asc/);
    assert.match(read.url, /model_id/);
    assert.equal(read.options.headers['Accept-Profile'], 'dcse_cp');
  } finally { f.restore(); m.restore(); }
});

test('dedicated mode uses dedicated server-side DDNA binding and preservation schema', async () => {
  const f = installFetch({legacyRows: rows});
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'dedicated'});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 200);
    const body = JSON.parse(res.body);
    assert.equal(body.ddna.source, 'dedicated');
    const read = f.calls.find(c => c.url.includes('ddna_ollama_jobs'));
    assert.ok(read.url.startsWith('https://dedicated.example'));
    assert.equal(read.options.headers['Accept-Profile'], 'dcse_ddna_legacy');
  } finally { f.restore(); m.restore(); }
});

test('dedicated mode fails closed when dedicated credentials are missing', async () => {
  const f = installFetch({legacyRows: rows});
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'dedicated', DDNA_SUPABASE_URL:'', DDNA_SUPABASE_SERVICE_ROLE_KEY:''});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 500);
    assert.match(JSON.parse(res.body).error, /Dedicated DDNA server environment is not configured/);
  } finally { f.restore(); m.restore(); }
});

test('legacy mode fails closed when server-side legacy key is missing', async () => {
  const f = installFetch({legacyRows: rows});
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'legacy', SUPABASE_SERVICE_ROLE_KEY:'', PABASE_SECRET_KEY:''});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 500);
    assert.match(JSON.parse(res.body).error, /Legacy Supabase server environment is not configured/);
    assert.equal(f.calls.filter(c => c.url.includes('ddna_ollama_jobs')).length, 0);
  } finally { f.restore(); m.restore(); }
});

test('compare mode returns dedicated data only when projections match', async () => {
  const f = installFetch({legacyRows: rows, dedicatedRows: rows});
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'compare'});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 200);
    assert.equal(JSON.parse(res.body).ddna.equivalent, true);
    assert.equal(f.calls.filter(c => c.url.includes('ddna_ollama_jobs')).length, 2);
  } finally { f.restore(); m.restore(); }
});

test('compare mode fails stop on data mismatch', async () => {
  const f = installFetch({legacyRows: rows, dedicatedRows: [{...rows[0], status:'different'}, rows[1]]});
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'compare'});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 409);
    assert.equal(JSON.parse(res.body).ddna.equivalent, false);
  } finally { f.restore(); m.restore(); }
});

test('route rejects unauthenticated requests before DDNA reads', async () => {
  const oldFetch = global.fetch;
  global.fetch = async url => {
    if (String(url).includes('/auth/v1/user')) return {ok:false};
    throw new Error('DDNA fetch must not occur');
  };
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'dedicated'});
  try {
    const res = mockRes();
    await m.handler({method:'GET', headers:{}}, res);
    assert.equal(res.statusCode, 401);
  } finally { global.fetch = oldFetch; m.restore(); }
});

test('upstream DDNA error body is not reflected to the operator response', async () => {
  const oldFetch = global.fetch;
  global.fetch = async url => {
    const u = String(url);
    if (u.includes('/auth/v1/user')) return {ok:true, json:async()=>({email:'operator@example.com'})};
    if (u.includes('/api/version') || u.includes('/api/tags')) throw new Error('ollama unavailable');
    if (u.includes('legacy.example')) return {ok:false, status:403, text:async()=> 'sensitive-upstream-detail'};
    throw new Error(`unexpected fetch ${u}`);
  };
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'legacy'});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 500);
    const error = JSON.parse(res.body).error;
    assert.match(error, /DDNA read failed \(legacy\/dcse_cp\): HTTP 403/);
    assert.doesNotMatch(error, /sensitive-upstream-detail/);
  } finally { global.fetch = oldFetch; m.restore(); }
});

test('invalid runtime mode fails closed before DDNA reads', async () => {
  const f = installFetch({legacyRows: rows});
  const m = loadHandler({...baseEnv, DDNA_RUNTIME_MODE:'unexpected'});
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 500);
    assert.match(JSON.parse(res.body).error, /Unsupported DDNA_RUNTIME_MODE/);
    assert.equal(f.calls.filter(c => c.url.includes('ddna_ollama_jobs')).length, 0);
  } finally { f.restore(); m.restore(); }
});

test('deployed app route delegates GET /api/runtime to DDNA cutover handler', async () => {
  const f = installFetch({legacyRows: rows, dedicatedRows: rows});
  const m = loadAppHandler({...baseEnv, DDNA_RUNTIME_MODE:'compare'});
  try {
    const res = mockRes();
    await m.handler({...mockReq(), url: '/api/runtime'}, res);
    assert.equal(res.statusCode, 200);
    const body = JSON.parse(res.body);
    assert.equal(body.ddna.mode, 'compare');
    assert.equal(body.ddna.source, 'dedicated');
    assert.equal(body.ddna.equivalent, true);
    assert.equal(f.calls.filter(c => c.url.includes('ddna_ollama_jobs')).length, 2);
  } finally { f.restore(); m.restore(); }
});

test('legacy fallback binding uses existing Vercel secret name without moving credentials', async () => {
  const f = installFetch({legacyRows: rows});
  const env = {...baseEnv, DDNA_RUNTIME_MODE:'legacy', SUPABASE_SERVICE_ROLE_KEY:'', PABASE_SECRET_KEY:'legacy-fallback-test'};
  const m = loadHandler(env);
  try {
    const res = mockRes();
    await m.handler(mockReq(), res);
    assert.equal(res.statusCode, 200);
    const read = f.calls.find(c => c.url.includes('ddna_ollama_jobs'));
    assert.equal(read.options.headers.apikey, 'legacy-fallback-test');
    assert.equal(read.options.headers['Accept-Profile'], 'dcse_cp');
  } finally { f.restore(); m.restore(); }
});
