const test = require('node:test');
const assert = require('node:assert/strict');
const { Readable } = require('node:stream');

process.env.SUPABASE_URL = 'https://supabase.test';
process.env.SUPABASE_ANON_KEY = 'anon-test';
process.env.OPENAI_API_KEY = 'server-openai-key';
process.env.CHAT_UPSTREAM_TIMEOUT_MS = '5000';

const handler = require('../api/chat.js');

function request(body, cookie = 'dcse_at=valid-token') {
  const req = Readable.from([JSON.stringify(body)]);
  req.method = 'POST';
  req.url = '/api/chat';
  req.headers = { cookie, origin: 'https://os.sonlyconsulting.com', 'content-type': 'application/json' };
  return req;
}

function response() {
  let resolve;
  const finished = new Promise(r => { resolve = r; });
  const headers = new Map();
  const res = {
    statusCode: 200,
    setHeader(name, value) { headers.set(String(name).toLowerCase(), value); },
    getHeader(name) { return headers.get(String(name).toLowerCase()); },
    end(chunk = '') { this.body = String(chunk); resolve(); }
  };
  return { res, finished, headers };
}

function jsonResponse(status, payload) {
  return {
    ok: status >= 200 && status < 300,
    status,
    async json() { return payload; },
    async text() { return JSON.stringify(payload); }
  };
}

test('authenticated OpenAI chat completes and uses the server credential', async () => {
  const calls = [];
  global.fetch = async (url, options = {}) => {
    calls.push({ url: String(url), options });
    if (String(url).endsWith('/auth/v1/user')) {
      return jsonResponse(200, { email: 'sonlyconsulting@gmail.com' });
    }
    if (String(url) === 'https://api.openai.com/v1/chat/completions') {
      assert.equal(options.headers.Authorization, 'Bearer server-openai-key');
      assert.equal(JSON.parse(options.body).messages[0].content, 'hello');
      return jsonResponse(200, { choices: [{ message: { content: 'working' } }] });
    }
    throw new Error(`Unexpected fetch: ${url}`);
  };

  const { res, finished, headers } = response();
  await handler(request({ model: 'gpt-4o-mini', messages: [{ role: 'user', content: 'hello' }], apiKey: 'client-key-must-not-be-used' }), res);
  await finished;

  assert.equal(res.statusCode, 200);
  assert.deepEqual(JSON.parse(res.body), { text: 'working' });
  assert.equal(headers.get('access-control-allow-origin'), 'https://os.sonlyconsulting.com');
  assert.equal(calls.length, 2);
});

test('unauthenticated chat is rejected before a provider call', async () => {
  let providerCalled = false;
  global.fetch = async url => {
    if (String(url).endsWith('/auth/v1/user')) return jsonResponse(401, { error: 'invalid' });
    providerCalled = true;
    throw new Error('Provider must not be called');
  };

  const { res, finished } = response();
  await handler(request({ model: 'gpt-4o-mini', messages: [] }, ''), res);
  await finished;

  assert.equal(res.statusCode, 401);
  assert.equal(providerCalled, false);
  assert.deepEqual(JSON.parse(res.body), { error: 'Authentication required' });
});

test('unavailable Ollama returns an explicit bounded local-runtime error', async () => {
  global.fetch = async url => {
    if (String(url).endsWith('/auth/v1/user')) {
      return jsonResponse(200, { email: 'sonlyconsulting@gmail.com' });
    }
    if (String(url).includes('127.0.0.1:11434')) throw new TypeError('fetch failed');
    throw new Error(`Unexpected fetch: ${url}`);
  };

  const { res, finished } = response();
  await handler(request({ model: 'ollama:nous-hermes2', messages: [{ role: 'user', content: 'hello' }] }), res);
  await finished;

  assert.equal(res.statusCode, 503);
  assert.match(JSON.parse(res.body).error, /Local Ollama is unavailable/);
});
