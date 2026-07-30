const OPERATOR_EMAIL = (process.env.DCS_OPERATOR_EMAIL || 'sonlyconsulting@gmail.com').toLowerCase();
const SUPABASE_URL = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || 'http://127.0.0.1:11434';
const UPSTREAM_TIMEOUT_MS = Math.min(Math.max(Number(process.env.CHAT_UPSTREAM_TIMEOUT_MS || 60000), 5000), 120000);
const MAX_BODY_BYTES = 1024 * 1024;
const APPROVED_ORIGINS = new Set([
  'https://os.sonlyconsulting.com',
  'https://cp.sonlyconsulting.com',
  'http://localhost:3000',
  'http://localhost:3001'
]);

function parseCookies(req) {
  return Object.fromEntries((req.headers.cookie || '').split(';').map(value => value.trim()).filter(Boolean).map(value => {
    const index = value.indexOf('=');
    return [decodeURIComponent(index < 0 ? value : value.slice(0, index)), decodeURIComponent(index < 0 ? '' : value.slice(index + 1))];
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

async function supabaseRequest(path, options = {}) {
  if (!SUPABASE_URL || !SUPABASE_KEY) throw new Error('Supabase server environment is not configured');
  return fetch(`${SUPABASE_URL}${path}`, {
    ...options,
    headers: { apikey: SUPABASE_KEY, 'Content-Type': 'application/json', ...(options.headers || {}) }
  });
}

async function validateAccessToken(token) {
  if (!token) return null;
  const response = await supabaseRequest('/auth/v1/user', { headers: { Authorization: `Bearer ${token}` } });
  if (!response.ok) return null;
  const user = await response.json();
  return String(user.email || '').toLowerCase() === OPERATOR_EMAIL ? user : null;
}

async function authenticate(req, res) {
  const cookies = parseCookies(req);
  let user = await validateAccessToken(cookies.dcse_at);
  if (user) return user;
  if (!cookies.dcse_rt) return null;

  const refreshed = await supabaseRequest('/auth/v1/token?grant_type=refresh_token', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: cookies.dcse_rt })
  });
  if (!refreshed.ok) return null;
  const session = await refreshed.json();
  user = await validateAccessToken(session.access_token);
  if (!user) return null;
  setSessionCookies(res, session);
  return user;
}

function sendJson(res, statusCode, payload) {
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  return res.end(JSON.stringify(payload));
}

async function readJsonBody(req) {
  let size = 0;
  const chunks = [];
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_BODY_BYTES) {
      const error = new Error('Request body is too large');
      error.statusCode = 413;
      throw error;
    }
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8');
  try {
    return JSON.parse(raw || '{}');
  } catch (_) {
    const error = new Error('Request body must be valid JSON');
    error.statusCode = 400;
    throw error;
  }
}

function providerKey(model = '') {
  if (model.startsWith('gpt-') || model.startsWith('o3')) return process.env.OPENAI_API_KEY;
  if (model.startsWith('gemini-')) return process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
  if (model.startsWith('qwen-')) return process.env.QWEN_API_KEY || process.env.DASHSCOPE_API_KEY;
  if (model.startsWith('claude-')) return process.env.ANTHROPIC_API_KEY;
  return null;
}

async function fetchWithTimeout(url, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), UPSTREAM_TIMEOUT_MS);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

async function readProviderJson(response) {
  const text = await response.text();
  try {
    return text ? JSON.parse(text) : {};
  } catch (_) {
    return { error: { message: text || `Provider returned HTTP ${response.status}` } };
  }
}

async function callProvider({ model, messages, system }) {
  if (model.startsWith('ollama:')) {
    const ollamaModel = model.slice('ollama:'.length);
    try {
      const response = await fetchWithTimeout(`${OLLAMA_BASE_URL.replace(/\/$/, '')}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: ollamaModel,
          messages: system ? [{ role: 'system', content: system }, ...messages] : messages,
          stream: false
        })
      });
      const raw = await readProviderJson(response);
      if (!response.ok) return { status: response.status, data: { error: raw.error?.message || raw.error || `Ollama returned HTTP ${response.status}` } };
      return { status: 200, data: { text: raw.message?.content || raw.response || '' } };
    } catch (error) {
      if (error.name === 'AbortError') return { status: 504, data: { error: `Local Ollama timed out after ${UPSTREAM_TIMEOUT_MS / 1000} seconds` } };
      return { status: 503, data: { error: 'Local Ollama is unavailable. Start Ollama and verify OLLAMA_BASE_URL and local network access.' } };
    }
  }

  const apiKey = providerKey(model);
  if (!apiKey) return { status: 503, data: { error: `Server credential not configured for ${model}` } };

  let url;
  let headers;
  let body;

  if (model.startsWith('gpt-') || model.startsWith('o3')) {
    url = 'https://api.openai.com/v1/chat/completions';
    headers = { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' };
    body = { model, messages: system ? [{ role: 'system', content: system }, ...messages] : messages, max_tokens: 1024 };
  } else if (model.startsWith('gemini-')) {
    url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(apiKey)}`;
    headers = { 'Content-Type': 'application/json' };
    body = {
      contents: messages.map(message => ({ role: message.role === 'assistant' ? 'model' : 'user', parts: [{ text: String(message.content || '') }] }))
    };
    if (system) body.systemInstruction = { parts: [{ text: system }] };
  } else if (model.startsWith('qwen-')) {
    url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
    headers = { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' };
    body = { model, messages: system ? [{ role: 'system', content: system }, ...messages] : messages, max_tokens: 1024 };
  } else if (model.startsWith('claude-')) {
    url = 'https://api.anthropic.com/v1/messages';
    headers = { 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json' };
    body = { model, max_tokens: 1024, messages };
    if (system) body.system = system;
  } else {
    return { status: 400, data: { error: `Unsupported model: ${model}` } };
  }

  try {
    const response = await fetchWithTimeout(url, { method: 'POST', headers, body: JSON.stringify(body) });
    const raw = await readProviderJson(response);
    let data;

    if (model.startsWith('gpt-') || model.startsWith('o3') || model.startsWith('qwen-')) {
      data = raw.choices ? { text: raw.choices[0]?.message?.content || '' } : { error: raw.error?.message || 'Provider request failed' };
    } else if (model.startsWith('gemini-')) {
      data = raw.candidates ? { text: raw.candidates[0]?.content?.parts?.map(part => part.text || '').join('') || '' } : { error: raw.error?.message || 'Gemini request failed' };
    } else {
      data = raw.content ? { text: raw.content.map(part => part.text || '').join('') } : { error: raw.error?.message || 'Anthropic request failed' };
    }

    return { status: response.status, data };
  } catch (error) {
    if (error.name === 'AbortError') return { status: 504, data: { error: `Provider timed out after ${UPSTREAM_TIMEOUT_MS / 1000} seconds` } };
    return { status: 502, data: { error: `Provider connection failed: ${error.message}` } };
  }
}

module.exports = async function handler(req, res) {
  const origin = req.headers.origin;
  if (origin && APPROVED_ORIGINS.has(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }

  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return sendJson(res, 204, {});
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST, OPTIONS');
    return sendJson(res, 405, { error: 'Method Not Allowed' });
  }

  try {
    const user = await authenticate(req, res);
    if (!user) return sendJson(res, 401, { error: 'Authentication required' });

    const body = await readJsonBody(req);
    const model = String(body.model || '');
    const messages = Array.isArray(body.messages) ? body.messages : null;
    const system = typeof body.system === 'string' ? body.system : '';

    if (!model || !messages) return sendJson(res, 400, { error: 'model and messages are required' });
    if (messages.length > 100) return sendJson(res, 400, { error: 'Too many messages' });

    const normalizedMessages = messages.map(message => ({
      role: ['user', 'assistant'].includes(message?.role) ? message.role : 'user',
      content: String(message?.content || '').slice(0, 100000)
    }));

    const result = await callProvider({ model, messages: normalizedMessages, system: system.slice(0, 100000) });
    return sendJson(res, result.status, result.data);
  } catch (error) {
    return sendJson(res, error.statusCode || 500, { error: error.message || 'Chat request failed' });
  }
};
