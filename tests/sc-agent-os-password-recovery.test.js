const test = require('node:test');
const assert = require('node:assert/strict');
const { Readable } = require('stream');
const vm = require('node:vm');

process.env.SUPABASE_URL = 'https://example.supabase.co';
process.env.SUPABASE_ANON_KEY = 'sb_publishable_test_key';
process.env.DCS_OPERATOR_EMAIL = 'operator@example.com';

const handler = require('../api/index.js');

function invoke({ url = '/', method = 'GET', body = '', headers = {} } = {}) {
  return new Promise((resolve, reject) => {
    const req = Readable.from(body ? [body] : []);
    req.url = url;
    req.method = method;
    req.headers = headers;

    const responseHeaders = new Map();
    const chunks = [];
    const res = {
      statusCode: 200,
      setHeader(name, value) { responseHeaders.set(String(name).toLowerCase(), value); },
      getHeader(name) { return responseHeaders.get(String(name).toLowerCase()); },
      end(chunk) {
        if (chunk) chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk)));
        resolve({
          statusCode: this.statusCode,
          headers: Object.fromEntries(responseHeaders),
          body: Buffer.concat(chunks).toString('utf8')
        });
      }
    };

    Promise.resolve(handler(req, res)).catch(reject);
  });
}

function inlineScript(html) {
  const scripts = [...html.matchAll(/<script nonce="[^"]+">([\s\S]*?)<\/script>/g)];
  assert.equal(scripts.length, 1);
  return scripts[0][1];
}

function recoveryDom() {
  let submitHandler;
  const elements = {
    passwordForm: { addEventListener(event, handler) { if (event === 'submit') submitHandler = handler; } },
    newPassword: { value: '', disabled: true, focus() {} },
    confirmPassword: { value: '', disabled: true },
    updatePassword: { disabled: true },
    recoveryStatus: { textContent: '', className: '' }
  };
  return {
    elements,
    document: { getElementById(id) { return elements[id]; } },
    getSubmitHandler() { return submitHandler; }
  };
}

test('login page preserves sign-in and requests recovery with the dedicated redirect', async () => {
  const response = await invoke();
  assert.equal(response.statusCode, 200);
  assert.match(response.body, /action="\/\?dcse_auth=login"/);
  assert.match(response.body, /supabase\.auth\.resetPasswordForEmail\(email/);
  assert.match(response.body, /redirectTo:\s*`\$\{window\.location\.origin\}\/auth\/update-password`/);
  assert.match(response.headers['content-security-policy'], /connect-src https:\/\/example\.supabase\.co/);
  assert.match(response.headers['cache-control'], /no-store/);
});

test('recovery route is public and contains the guarded password update flow', async () => {
  const response = await invoke({ url: '/auth/update-password#type=recovery' });
  assert.equal(response.statusCode, 200);
  assert.match(response.body, /New Password/);
  assert.match(response.body, /Confirm Password/);
  assert.match(response.body, /event === 'PASSWORD_RECOVERY'/);
  assert.match(response.body, /supabase\.auth\.updateUser\(\{ password: newPassword \}\)/);
  assert.match(response.body, /history\.replaceState\(null, '', '\/auth\/update-password'\)/);
  assert.match(response.body, /invalid or expired/);
  assert.doesNotMatch(response.body, /console\.(?:log|debug|info|warn|error)/);
});

test('recovery route rejects state-changing HTTP methods', async () => {
  const response = await invoke({ url: '/auth/update-password', method: 'POST', body: 'password=unsafe' });
  assert.equal(response.statusCode, 405);
  assert.equal(response.headers.allow, 'GET, HEAD');
  assert.equal(response.body, 'Method Not Allowed');
});

test('expired recovery links render only a safe error', async () => {
  const response = await invoke({ url: '/auth/update-password' });
  const dom = recoveryDom();
  vm.runInNewContext(inlineScript(response.body), {
    document: dom.document,
    window: { location: { search: '?error=access_denied', hash: '' } },
    URLSearchParams,
    history: { replaceState() {} },
    setTimeout,
    clearTimeout
  });
  assert.match(dom.elements.recoveryStatus.textContent, /invalid or expired/);
  assert.doesNotMatch(dom.elements.recoveryStatus.textContent, /access_denied/);
  assert.equal(dom.elements.updatePassword.disabled, true);
});

test('PASSWORD_RECOVERY session enables and completes a valid password update', async () => {
  const response = await invoke({ url: '/auth/update-password' });
  const dom = recoveryDom();
  let updateCall;
  let signedOut = false;
  let redirectedTo;
  const auth = {
    onAuthStateChange(callback) { callback('PASSWORD_RECOVERY', { user: { id: 'operator' } }); },
    getSession: async () => ({ data: { session: null }, error: null }),
    updateUser: async payload => { updateCall = payload; return { error: null }; },
    signOut: async () => { signedOut = true; }
  };
  const window = {
    location: {
      search: '',
      hash: '#type=recovery',
      replace(url) { redirectedTo = url; }
    },
    supabase: { createClient: () => ({ auth }) }
  };
  vm.runInNewContext(inlineScript(response.body), {
    document: dom.document,
    window,
    URLSearchParams,
    history: { replaceState() {} },
    setTimeout(callback) { callback(); return 1; },
    clearTimeout() {}
  });

  assert.equal(dom.elements.newPassword.disabled, false);
  assert.equal(dom.elements.updatePassword.disabled, false);
  dom.elements.newPassword.value = 'StrongPassword123';
  dom.elements.confirmPassword.value = 'StrongPassword123';
  await dom.getSubmitHandler()({ preventDefault() {} });

  assert.equal(updateCall.password, 'StrongPassword123');
  assert.equal(signedOut, true);
  assert.equal(redirectedTo, '/?password_updated=1');
});

test('existing operator login still sets protected session cookies and redirects', async t => {
  const originalFetch = global.fetch;
  t.after(() => { global.fetch = originalFetch; });

  global.fetch = async (url) => {
    if (String(url).includes('/auth/v1/token?grant_type=password')) {
      return {
        ok: true,
        json: async () => ({ access_token: 'access-token', refresh_token: 'refresh-token', expires_in: 3600 })
      };
    }
    if (String(url).endsWith('/auth/v1/user')) {
      return { ok: true, json: async () => ({ email: 'operator@example.com' }) };
    }
    throw new Error(`Unexpected request: ${url}`);
  };

  const response = await invoke({
    url: '/?dcse_auth=login',
    method: 'POST',
    body: 'email=operator%40example.com&password=ValidPassword123',
    headers: { 'content-type': 'application/x-www-form-urlencoded' }
  });

  assert.equal(response.statusCode, 302);
  assert.equal(response.headers.location, '/');
  assert.equal(response.headers['set-cookie'].length, 2);
  assert.match(response.headers['set-cookie'][0], /HttpOnly; Secure; SameSite=Lax/);
});

test('successful recovery redirect produces a clear login notice', async () => {
  const response = await invoke({ url: '/?password_updated=1' });
  assert.equal(response.statusCode, 200);
  assert.match(response.body, /Password updated successfully\. Sign in with the new password\./);
});

test('browser auth scripts are syntactically valid', async () => {
  for (const url of ['/', '/auth/update-password']) {
    const response = await invoke({ url });
    assert.doesNotThrow(() => new vm.Script(inlineScript(response.body)));
  }
});
