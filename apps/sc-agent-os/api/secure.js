'use strict';

const innerHandler = require('./index.js');

const OPERATOR_EMAIL = String(process.env.DCS_OPERATOR_EMAIL || 'sonlyconsulting@gmail.com').toLowerCase();
const SUPABASE_URL = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const APPROVED_ORIGINS = new Set([
  'https://os.sonlyconsulting.com',
  'https://cp.sonlyconsulting.com',
  'http://localhost:3000',
  'http://localhost:3001'
]);

function parseCookies(req) {
  return Object.fromEntries((req.headers.cookie || '').split(';').map(v => v.trim()).filter(Boolean).map(v => {
    const i = v.indexOf('=');
    return [decodeURIComponent(i < 0 ? v : v.slice(0, i)), decodeURIComponent(i < 0 ? '' : v.slice(i + 1))];
  }));
}

function cookie(name, value, maxAge) {
  return `${encodeURIComponent(name)}=${encodeURIComponent(value)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`;
}

function setSessionCookies(res, session) {
  const expires = Number(session.expires_in || 3600);
  res.setHeader('Set-Cookie', [
    cookie('dcse_at', session.access_token, expires),
    cookie('dcse_rt', session.refresh_token || '', 60 * 60 * 24 * 30)
  ]);
}

function clearSessionCookies(res) {
  res.setHeader('Set-Cookie', [cookie('dcse_at', '', 0), cookie('dcse_rt', '', 0)]);
}

async function supabaseRequest(path, options = {}) {
  if (!SUPABASE_URL || !SUPABASE_KEY) throw new Error('Supabase server environment is not configured');
  return fetch(`${SUPABASE_URL}${path}`, {
    ...options,
    headers: {apikey: SUPABASE_KEY, 'Content-Type': 'application/json', ...(options.headers || {})}
  });
}

async function validateAccessToken(token) {
  if (!token) return null;
  const response = await supabaseRequest('/auth/v1/user', {headers: {Authorization: `Bearer ${token}`}});
  if (!response.ok) return null;
  const user = await response.json();
  return String(user.email || '').toLowerCase() === OPERATOR_EMAIL ? user : null;
}

async function authenticate(req, res) {
  const cookies = parseCookies(req);
  let user = await validateAccessToken(cookies.dcse_at);
  if (user) return {user, accessToken: cookies.dcse_at};
  if (!cookies.dcse_rt) return null;

  const refreshed = await supabaseRequest('/auth/v1/token?grant_type=refresh_token', {
    method: 'POST',
    body: JSON.stringify({refresh_token: cookies.dcse_rt})
  });
  if (!refreshed.ok) return null;
  const session = await refreshed.json();
  user = await validateAccessToken(session.access_token);
  if (!user) return null;
  setSessionCookies(res, session);
  return {user, accessToken: session.access_token, refreshToken: session.refresh_token || cookies.dcse_rt};
}

async function readBody(req) {
  let body = '';
  for await (const chunk of req) body += chunk;
  return body;
}

function loginPage(error = '') {
  const safe = String(error).replace(/[<>&"']/g, '');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SC Agent OS Secure Access</title><style>body{margin:0;background:#0B1D3A;color:#F5F0E8;font-family:Arial,sans-serif;display:grid;place-items:center;min-height:100vh}.box{width:min(420px,calc(100% - 32px));background:#122444;border:1px solid #1e3a6a;border-radius:10px;padding:28px;box-sizing:border-box}.brand{color:#C9A84C;font-weight:700;letter-spacing:1px}.sub{color:#8fa3c0;margin:8px 0 22px}.field{width:100%;box-sizing:border-box;margin:7px 0;padding:12px;border-radius:6px;border:1px solid #1e3a6a;background:#0f2442;color:#F5F0E8}.btn{width:100%;margin-top:12px;padding:12px;border:0;border-radius:6px;background:#C9A84C;color:#0B1D3A;font-weight:700;cursor:pointer}.err{color:#ffb4a9;min-height:20px;font-size:13px}</style></head><body><main class="box"><div class="brand">SC / DCSE SECURE ACCESS</div><div class="sub">Authorized operator sign-in</div><div class="err">${safe}</div><form method="post" action="/?dcse_auth=login"><input class="field" type="email" name="email" autocomplete="username" required placeholder="Email"><input class="field" type="password" name="password" autocomplete="current-password" required placeholder="Password"><button class="btn" type="submit">Sign In</button></form></main></body></html>`;
}

function sendLogin(res, error = '', status = 200) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'");
  return res.end(loginPage(error));
}

function applyOriginBoundary(req, res) {
  const origin = req.headers.origin;
  const originalSetHeader = res.setHeader.bind(res);
  res.setHeader = (name, value) => {
    if (String(name).toLowerCase() === 'access-control-allow-origin') {
      if (origin && APPROVED_ORIGINS.has(origin)) return originalSetHeader(name, origin);
      return undefined;
    }
    return originalSetHeader(name, value);
  };
  if (origin && APPROVED_ORIGINS.has(origin)) {
    originalSetHeader('Access-Control-Allow-Origin', origin);
    originalSetHeader('Vary', 'Origin');
  }
}

function propagateVerifiedSession(req, auth) {
  if (!auth || !auth.accessToken) return;
  const existing = parseCookies(req);
  existing.dcse_at = auth.accessToken;
  if (auth.refreshToken) existing.dcse_rt = auth.refreshToken;
  req.headers = {...req.headers, cookie: Object.entries(existing).map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join('; ')};
}

module.exports = async function secureHandler(req, res) {
  const url = new URL(req.url || '/', 'https://dcse.local');
  const action = url.searchParams.get('dcse_auth');

  if (action === 'logout') {
    clearSessionCookies(res);
    res.statusCode = 302;
    res.setHeader('Location', '/');
    return res.end();
  }

  if (action === 'login' && req.method === 'POST') {
    try {
      const raw = await readBody(req);
      const form = new URLSearchParams(raw);
      const email = String(form.get('email') || '').toLowerCase();
      const password = String(form.get('password') || '');
      if (email !== OPERATOR_EMAIL) throw new Error('This account is not authorized.');
      const response = await supabaseRequest('/auth/v1/token?grant_type=password', {
        method: 'POST',
        body: JSON.stringify({email, password})
      });
      if (!response.ok) throw new Error('Sign-in failed. Check the email and password.');
      const session = await response.json();
      const user = await validateAccessToken(session.access_token);
      if (!user) throw new Error('This account is not authorized.');
      setSessionCookies(res, session);
      res.statusCode = 302;
      res.setHeader('Location', '/');
      return res.end();
    } catch (error) {
      return sendLogin(res, error.message, 401);
    }
  }

  let auth = null;
  try {
    auth = await authenticate(req, res);
  } catch (error) {
    return sendLogin(res, error.message, 503);
  }

  if (!auth) {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      res.statusCode = 401;
      res.setHeader('Content-Type', 'application/json');
      return res.end(JSON.stringify({error: 'Authentication required'}));
    }
    return sendLogin(res);
  }

  propagateVerifiedSession(req, auth);
  applyOriginBoundary(req, res);
  return innerHandler(req, res);
};
