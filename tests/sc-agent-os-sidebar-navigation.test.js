const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');

process.env.SUPABASE_URL = 'https://example.supabase.co';
process.env.SUPABASE_ANON_KEY = 'sb_publishable_test_key';
process.env.DCS_OPERATOR_EMAIL = 'operator@example.com';

const handler = require('../apps/sc-agent-os/api/index.js');
const protectedHandler = require('../api/index.js');

function invoke(targetHandler, { url = '/', method = 'GET', headers: requestHeaders = {} } = {}) {
  return new Promise((resolve, reject) => {
    const req = { method, url, headers: requestHeaders };
    const headers = new Map();
    const res = {
      statusCode: 200,
      setHeader(name, value) { headers.set(String(name).toLowerCase(), value); },
      getHeader(name) { return headers.get(String(name).toLowerCase()); },
      end(chunk) {
        resolve({ statusCode: this.statusCode, headers: Object.fromEntries(headers), body: String(chunk || '') });
      }
    };
    Promise.resolve(targetHandler(req, res)).catch(reject);
  });
}

function renderDashboard() { return invoke(handler); }

function dashboardScript(html) {
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  assert.equal(scripts.length, 1);
  return scripts[0][1];
}

const requiredItems = [
  ['Mission Control', 'mission'],
  ['Agent Chat + Voice', 'chat'],
  ['Approvals', 'approvals'],
  ['Agent Dock', 'agents'],
  ['Task Queue', 'tasks'],
  ['Portfolio', 'portfolio'],
  ['Agent Operations', 'agentops'],
  ['DDNA Harvest', 'ddna'],
  ['Local Models', 'models'],
  ['RAG / Source', 'rag'],
  ['Runtime Health', 'runtime'],
  ['Tribunal', 'tribunal'],
  ['Dispatch', 'dispatch']
];

test('the complete dashboard script parses before navigation is exposed', async () => {
  const response = await renderDashboard();
  assert.equal(response.statusCode, 200);
  assert.doesNotThrow(() => new vm.Script(dashboardScript(response.body), { filename: 'sc-agent-os-dashboard.js' }));
});

test('the authenticated production wrapper preserves a parseable dashboard script', async t => {
  const originalFetch = global.fetch;
  t.after(() => { global.fetch = originalFetch; });
  global.fetch = async url => {
    if (String(url).endsWith('/auth/v1/user')) {
      return { ok: true, json: async () => ({ email: 'operator@example.com' }) };
    }
    throw new Error(`Unexpected request: ${url}`);
  };
  const response = await invoke(protectedHandler, { headers: { cookie: 'dcse_at=valid-test-token' } });
  assert.equal(response.statusCode, 200);
  assert.doesNotThrow(() => new vm.Script(dashboardScript(response.body), { filename: 'protected-sc-agent-os-dashboard.js' }));
});

test('all requested sidebar destinations are real semantic buttons with panels', async () => {
  const { body } = await renderDashboard();
  const buttons = [...body.matchAll(/<button[^>]+class="nav-item(?: active)?"[^>]*>([\s\S]*?)<\/button>/g)];
  assert.equal(buttons.length, 24);
  for (const button of buttons) {
    const id = button[0].match(/data-panel="([^"]+)"/)?.[1];
    assert.ok(id, 'every navigation button must declare a panel route');
    assert.match(body, new RegExp(`id="panel-${id}"`));
  }
  for (const [label, id] of requiredItems) {
    const button = buttons.find(match => match[0].includes(`data-panel="${id}"`));
    assert.ok(button, `${label} must have a semantic navigation button`);
    assert.match(button[0], new RegExp(`aria-controls="panel-${id}"`));
    assert.ok(button[1].replace(/<[^>]+>/g, '').includes(label), `${label} must remain visibly labeled`);
    assert.match(body, new RegExp(`id="panel-${id}"`));
  }
  assert.doesNotMatch(body, /class="nav-item[^"]*"[^>]*onclick=/);
});

test('navigation supports active state, hash routes, history, and task chat without unsafe title interpolation', async () => {
  const script = dashboardScript((await renderDashboard()).body);
  assert.match(script, /aria-current','page'/);
  assert.match(script, /window\.history\.pushState/);
  assert.match(script, /window\.history\.replaceState/);
  assert.match(script, /addEventListener\('keydown'/);
  assert.match(script, /event\.key!==\s*'Enter'/);
  assert.match(script, /addEventListener\('popstate',syncNavigationFromLocation\)/);
  assert.match(script, /addEventListener\('hashchange',syncNavigationFromLocation\)/);
  assert.match(script, /chatAboutTaskById\(\$\{t\.id\}\)/);
  assert.doesNotMatch(script, /chatAboutTask\('\$\{t\.title/);
});
