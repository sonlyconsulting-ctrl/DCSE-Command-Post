'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {Readable} = require('stream');

function req(url='/', method='GET', cookie='', body='') {
  const r = Readable.from(body ? [body] : []);
  r.url = url;
  r.method = method;
  r.headers = cookie ? {cookie} : {};
  return r;
}

function res() {
  return {
    statusCode: 200,
    headers: {},
    body: '',
    setHeader(k, v) { this.headers[String(k).toLowerCase()] = v; },
    getHeader(k) { return this.headers[String(k).toLowerCase()]; },
    end(v='') { this.body += Buffer.isBuffer(v) ? v.toString('utf8') : String(v); return v; }
  };
}

function load(env={}) {
  const saved = {...process.env};
  Object.assign(process.env, env);
  for (const mod of ['../apps/sc-agent-os/api/secure.js','../apps/sc-agent-os/api/index.js','../apps/sc-agent-os/api/runtime.js']) {
    delete require.cache[require.resolve(mod)];
  }
  const handler = require('../apps/sc-agent-os/api/secure.js');
  return {handler, restore() {
    for (const key of Object.keys(process.env)) if (!(key in saved)) delete process.env[key];
    Object.assign(process.env, saved);
  }};
}

const env = {
  DCS_OPERATOR_EMAIL: 'operator@example.com',
  SUPABASE_URL: 'https://legacy.example',
  NEXT_PUBLIC_SUPABASE_URL: 'https://legacy.example',
  SUPABASE_ANON_KEY: 'anon-test',
  NEXT_PUBLIC_SUPABASE_ANON_KEY: 'anon-test',
  SUPABASE_SERVICE_ROLE_KEY: 'legacy-service-test',
  DDNA_SUPABASE_URL: 'https://dedicated.example',
  DDNA_SUPABASE_SERVICE_ROLE_KEY: 'dedicated-service-test',
  DDNA_RUNTIME_MODE: 'compare'
};

const rows = [
  {id:'a', model_id:'model-a', status:'queued', retry_count:0, duration_ms:null, created_at:'2026-07-13T21:40:59Z'}
];

function installFetch({refresh=false}={}) {
  const old = global.fetch;
  const calls = [];
  global.fetch = async (url, options={}) => {
    const u = String(url);
    calls.push({url:u, options});
    if (u.includes('/auth/v1/token?grant_type=refresh_token')) {
      assert.equal(refresh, true);
      return {ok:true, json:async()=>({access_token:'fresh-token', refresh_token:'fresh-refresh', expires_in:3600})};
    }
    if (u.includes('/auth/v1/user')) {
      const auth = options.headers?.Authorization || options.headers?.authorization || '';
      if (auth === 'Bearer expired-token') return {ok:false};
      return {ok:true, json:async()=>({email:'operator@example.com'})};
    }
    if (u.includes('/api/version') || u.includes('/api/tags')) throw new Error('ollama unavailable');
    if (u.includes('legacy.example/rest/v1/ddna_ollama_jobs')) return {ok:true, json:async()=>rows};
    if (u.includes('dedicated.example/rest/v1/ddna_ollama_jobs')) return {ok:true, json:async()=>rows};
    throw new Error(`unexpected fetch ${u}`);
  };
  return {calls, restore(){global.fetch=old;}};
}

test('unauthenticated page request is gated before SC Agent OS UI is returned', async () => {
  const old = global.fetch;
  global.fetch = async () => { throw new Error('auth fetch should not occur without cookies'); };
  const m = load(env);
  try {
    const out = res();
    await m.handler(req('/', 'GET'), out);
    assert.equal(out.statusCode, 200);
    assert.match(out.body, /SC \/ DCSE SECURE ACCESS/);
    assert.doesNotMatch(out.body, /Mission Control · SC-COMMAND-POST/);
    assert.equal(out.headers['cache-control'], 'no-store');
  } finally { global.fetch=old; m.restore(); }
});

test('unauthenticated API mutation fails before inner handler execution', async () => {
  const old = global.fetch;
  global.fetch = async () => { throw new Error('auth fetch should not occur without cookies'); };
  const m = load(env);
  try {
    const out = res();
    await m.handler(req('/api/tribunal/dispatch', 'POST', '', '{}'), out);
    assert.equal(out.statusCode, 401);
    assert.equal(JSON.parse(out.body).error, 'Authentication required');
  } finally { global.fetch=old; m.restore(); }
});

test('authenticated operator reaches DDNA compare runtime through the gateway', async () => {
  const f = installFetch();
  const m = load(env);
  try {
    const out = res();
    await m.handler(req('/api/runtime', 'GET', 'dcse_at=valid-token'), out);
    assert.equal(out.statusCode, 200);
    const body = JSON.parse(out.body);
    assert.equal(body.ddna.mode, 'compare');
    assert.equal(body.ddna.equivalent, true);
    assert.equal(f.calls.filter(c=>c.url.includes('/auth/v1/user')).length, 2);
    assert.equal(f.calls.filter(c=>c.url.includes('ddna_ollama_jobs')).length, 2);
  } finally { f.restore(); m.restore(); }
});

test('refresh-token recovery propagates the fresh access token to the DDNA runtime in the same request', async () => {
  const f = installFetch({refresh:true});
  const m = load(env);
  try {
    const out = res();
    await m.handler(req('/api/runtime', 'GET', 'dcse_at=expired-token; dcse_rt=refresh-token'), out);
    assert.equal(out.statusCode, 200);
    const body = JSON.parse(out.body);
    assert.equal(body.ddna.equivalent, true);
    const setCookie = out.headers['set-cookie'];
    assert.ok(Array.isArray(setCookie));
    assert.match(setCookie.join(';'), /dcse_at=fresh-token/);
    const authCalls = f.calls.filter(c=>c.url.includes('/auth/v1/user'));
    assert.ok(authCalls.some(c=>(c.options.headers?.Authorization || '') === 'Bearer fresh-token'));
  } finally { f.restore(); m.restore(); }
});
