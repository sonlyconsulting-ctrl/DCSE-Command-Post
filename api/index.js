const { Readable } = require('stream');
const innerHandler = require('../apps/sc-agent-os/api/index.js');

const OPERATOR_EMAIL = (process.env.DCS_OPERATOR_EMAIL || 'sonlyconsulting@gmail.com').toLowerCase();
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
    method: 'POST', body: JSON.stringify({ refresh_token: cookies.dcse_rt })
  });
  if (!refreshed.ok) return null;
  const session = await refreshed.json();
  user = await validateAccessToken(session.access_token);
  if (!user) return null;
  setSessionCookies(res, session);
  return user;
}

async function readBody(req) {
  let body = '';
  for await (const chunk of req) body += chunk;
  return body;
}

function providerKey(model = '') {
  if (model.startsWith('gpt-') || model.startsWith('o3')) return process.env.OPENAI_API_KEY;
  if (model.startsWith('gemini-')) return process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
  if (model.startsWith('qwen-')) return process.env.QWEN_API_KEY || process.env.DASHSCOPE_API_KEY;
  if (model.startsWith('claude-')) return process.env.ANTHROPIC_API_KEY;
  return null;
}

function loginPage(error = '') {
  const safeError = String(error).replace(/[<>&"']/g, '');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DCSE Secure Access</title><style>body{margin:0;background:#0B1D3A;color:#F5F0E8;font-family:Arial,sans-serif;display:grid;place-items:center;min-height:100vh}.box{width:min(420px,calc(100% - 32px));background:#122444;border:1px solid #1e3a6a;border-radius:10px;padding:28px;box-sizing:border-box}.brand{color:#C9A84C;font-weight:700;letter-spacing:1px}.sub{color:#8fa3c0;margin:8px 0 22px}.field{width:100%;box-sizing:border-box;margin:7px 0;padding:12px;border-radius:6px;border:1px solid #1e3a6a;background:#0f2442;color:#F5F0E8}.btn{width:100%;margin-top:12px;padding:12px;border:0;border-radius:6px;background:#C9A84C;color:#0B1D3A;font-weight:700;cursor:pointer}.err{color:#ffb4a9;min-height:20px;font-size:13px}</style></head><body><form class="box" method="post" action="/?dcse_auth=login"><div class="brand">SC / DCSE SECURE ACCESS</div><div class="sub">Authorized operator sign-in</div><div class="err">${safeError}</div><input class="field" type="email" name="email" autocomplete="username" required placeholder="Email"><input class="field" type="password" name="password" autocomplete="current-password" required placeholder="Password"><button class="btn" type="submit">Sign In</button></form></body></html>`;
}

function secureHtml(html) {
  const oldKeyBlock = `// Per-provider key management
const KEY_STORES={anthropic:'sc_anthropic_key',openai:'sc_openai_key',google:'sc_google_key',qwen:'sc_qwen_key'};
const PROVIDER_META={
  anthropic:{label:'Anthropic',placeholder:'sk-ant-...',check:v=>v.startsWith('sk-ant-')},
  openai:   {label:'OpenAI',   placeholder:'sk-...',     check:v=>v.startsWith('sk-')},
  google:   {label:'Google',   placeholder:'AIza...',    check:v=>v.length>10},
  qwen:     {label:'Qwen',     placeholder:'sk-... (DashScope)', check:v=>v.length>10},
  ollama:   {label:'Ollama',   placeholder:'(no key needed)', check:()=>true}
};
function providerOf(model){
  if(model.startsWith('claude-'))return'anthropic';
  if(model.startsWith('gpt-')||model.startsWith('o3'))return'openai';
  if(model.startsWith('gemini-'))return'google';
  if(model.startsWith('qwen-'))return'qwen';
  if(model.startsWith('ollama:'))return'ollama';
  return'anthropic';
}
const keyInput=document.getElementById('apiKeyInput');
function loadKeyForModel(model){const p=providerOf(model);if(p==='ollama'){keyInput.value='';return;}keyInput.value=localStorage.getItem(KEY_STORES[p])||'';}
function saveKey(){const model=document.getElementById('modelSelect').value;const p=providerOf(model);if(p!=='ollama')localStorage.setItem(KEY_STORES[p],keyInput.value);updateStatus();}
function updateStatus(){
  const s=document.getElementById('modelStatus');
  const model=document.getElementById('modelSelect').value;
  const p=providerOf(model);const meta=PROVIDER_META[p];
  if(p==='ollama'){s.textContent='OLLAMA';s.className='tag tag-orange';}
  else if(meta.check(keyInput.value)){s.textContent=meta.label+' KEY OK';s.className='tag tag-green';}
  else{s.textContent=meta.label+' KEY NEEDED';s.className='tag tag-amber';}
}
function onModelChange(){
  const model=document.getElementById('modelSelect').value;
  const p=providerOf(model);
  document.getElementById('ollamaNote').style.display=p==='ollama'?'inline':'none';
  keyInput.placeholder=PROVIDER_META[p].placeholder;
  loadKeyForModel(model);updateStatus();
}
onModelChange();`;

  const newKeyBlock = `// Provider credentials are server-managed
const PROVIDER_META={anthropic:{label:'Anthropic'},openai:{label:'OpenAI'},google:{label:'Google'},qwen:{label:'Qwen'},ollama:{label:'Ollama'}};
function providerOf(model){if(model.startsWith('claude-'))return'anthropic';if(model.startsWith('gpt-')||model.startsWith('o3'))return'openai';if(model.startsWith('gemini-'))return'google';if(model.startsWith('qwen-'))return'qwen';if(model.startsWith('ollama:'))return'ollama';return'anthropic';}
const keyInput=document.getElementById('apiKeyInput');
function loadKeyForModel(){keyInput.value='server-managed';}
function saveKey(){updateStatus();}
function updateStatus(){const s=document.getElementById('modelStatus');const p=providerOf(document.getElementById('modelSelect').value);if(p==='ollama'){s.textContent='OLLAMA';s.className='tag tag-orange';}else{s.textContent=PROVIDER_META[p].label+' SERVER KEY';s.className='tag tag-green';}}
function onModelChange(){const p=providerOf(document.getElementById('modelSelect').value);document.getElementById('ollamaNote').style.display=p==='ollama'?'inline':'none';loadKeyForModel();updateStatus();}
onModelChange();`;

  return html
    .replace('<input class="key-input" id="apiKeyInput" type="password" placeholder="API key" style="width:170px" oninput="saveKey()" />', '<input id="apiKeyInput" type="hidden" value="server-managed" />')
    .replace('<span id="modelStatus" class="tag tag-amber">KEY NEEDED</span>', '<span id="modelStatus" class="tag tag-green">SERVER KEY</span>')
    .replace(oldKeyBlock, newKeyBlock)
    .replace("      const apiKey=keyInput.value;\n      if(!PROVIDER_META[p].check(apiKey)){thinking.textContent='Enter '+PROVIDER_META[p].label+' API key ('+PROVIDER_META[p].placeholder+')';thinking.className='msg sys';btn.disabled=false;return;}\n      const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:chatHistory,system:activeSysPrompt,apiKey})});", "      const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:chatHistory,system:activeSysPrompt})});")
    .replace(/Select provider, enter API key, and send\./g, 'Select provider and send. Provider credentials are managed securely by the server.')
    .replace(/Enter your (Anthropic|Google|OpenAI|Qwen) API key above[^<]*/g, 'Provider credentials are managed securely by the server.');
}

module.exports = async function handler(req, res) {
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
        method: 'POST', body: JSON.stringify({ email, password })
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
      res.statusCode = 401;
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      return res.end(loginPage(error.message));
    }
  }

  let user = null;
  try { user = await authenticate(req, res); } catch (error) {
    res.statusCode = 503;
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.end(loginPage(error.message));
  }

  if (!user) {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      res.statusCode = 401;
      res.setHeader('Content-Type', 'application/json');
      return res.end(JSON.stringify({ error: 'Authentication required' }));
    }
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.end(loginPage());
  }

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

  let forwardedReq = req;
  if (req.method === 'POST' || req.method === 'PUT' || req.method === 'PATCH') {
    const raw = await readBody(req);
    let nextBody = raw;
    try {
      const parsed = JSON.parse(raw || '{}');
      if (parsed.model && Array.isArray(parsed.messages) && !String(parsed.model).startsWith('ollama:')) {
        const key = providerKey(String(parsed.model));
        if (!key) {
          res.statusCode = 503;
          res.setHeader('Content-Type', 'application/json');
          return res.end(JSON.stringify({ error: `Server credential not configured for ${parsed.model}` }));
        }
        parsed.apiKey = key;
        nextBody = JSON.stringify(parsed);
      }
    } catch (_) {}
    forwardedReq = Readable.from([nextBody]);
    Object.assign(forwardedReq, req);
    forwardedReq.method = req.method;
    forwardedReq.url = req.url;
    forwardedReq.headers = { ...req.headers, 'content-length': Buffer.byteLength(nextBody) };
  }

  const originalEnd = res.end.bind(res);
  res.end = (chunk, encoding, callback) => {
    const contentType = String(res.getHeader('Content-Type') || res.getHeader('content-type') || '');
    if (chunk && contentType.includes('text/html')) {
      chunk = secureHtml(Buffer.isBuffer(chunk) ? chunk.toString('utf8') : String(chunk));
    }
    return originalEnd(chunk, encoding, callback);
  };

  return innerHandler(forwardedReq, res);
};
