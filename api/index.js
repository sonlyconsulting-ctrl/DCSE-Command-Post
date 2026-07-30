const { Readable } = require('stream');
const { randomBytes } = require('crypto');
const innerHandler = require('../apps/sc-agent-os/api/index.js');

const OPERATOR_EMAIL = (process.env.DCS_OPERATOR_EMAIL || 'sonlyconsulting@gmail.com').toLowerCase();
const SUPABASE_URL = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const SUPABASE_BROWSER_SRC = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.57.4/dist/umd/supabase.min.js';
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

function safeScriptJson(value) {
  return JSON.stringify(value).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026');
}

function browserSupabaseKey() {
  const key = String(SUPABASE_KEY || '');
  if (key.startsWith('sb_publishable_')) return key;
  try {
    const payload = JSON.parse(Buffer.from(key.split('.')[1], 'base64url').toString('utf8'));
    if (payload.role === 'anon') return key;
  } catch (_) {}
  return '';
}

function authPageContext() {
  return { nonce: randomBytes(18).toString('base64'), config: safeScriptJson({ url: SUPABASE_URL || '', key: browserSupabaseKey() }) };
}

function sendAuthPage(res, page, statusCode = 200) {
  let connectOrigin = "'none'";
  try { connectOrigin = new URL(SUPABASE_URL).origin; } catch (_) {}
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Content-Security-Policy', `default-src 'none'; connect-src ${connectOrigin}; script-src 'nonce-${page.nonce}' https://cdn.jsdelivr.net; style-src 'unsafe-inline'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`);
  return res.end(page.html);
}

function authStyles() {
  return `body{margin:0;background:#0B1D3A;color:#F5F0E8;font-family:Arial,sans-serif;display:grid;place-items:center;min-height:100vh}.box{width:min(420px,calc(100% - 32px));background:#122444;border:1px solid #1e3a6a;border-radius:10px;padding:28px;box-sizing:border-box}.brand{color:#C9A84C;font-weight:700;letter-spacing:1px}.sub{color:#8fa3c0;margin:8px 0 22px}.field{width:100%;box-sizing:border-box;margin:7px 0;padding:12px;border-radius:6px;border:1px solid #1e3a6a;background:#0f2442;color:#F5F0E8}.btn{width:100%;margin-top:12px;padding:12px;border:0;border-radius:6px;background:#C9A84C;color:#0B1D3A;font-weight:700;cursor:pointer}.btn.secondary{background:transparent;color:#C9A84C;border:1px solid #C9A84C}.btn:disabled{opacity:.55;cursor:not-allowed}.message{min-height:20px;font-size:13px;line-height:1.4;margin:8px 0}.err{color:#ffb4a9}.ok{color:#74d99f}.hint{color:#8fa3c0;font-size:12px;line-height:1.5;margin-top:12px}.hidden{display:none}`;
}

function loginPage(error = '', notice = '') {
  const { nonce, config } = authPageContext();
  const safeError = String(error).replace(/[<>&"']/g, '');
  const safeNotice = String(notice).replace(/[<>&"']/g, '');
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DCSE Secure Access</title><style>${authStyles()}</style></head><body><main class="box"><div class="brand">SC / DCSE SECURE ACCESS</div><div class="sub">Authorized operator sign-in</div><div class="message err">${safeError}</div><div class="message ok">${safeNotice}</div><form method="post" action="/?dcse_auth=login"><input class="field" id="loginEmail" type="email" name="email" autocomplete="username" required placeholder="Email"><input class="field" type="password" name="password" autocomplete="current-password" required placeholder="Password"><button class="btn" type="submit">Sign In</button></form><button class="btn secondary" id="forgotPassword" type="button">Send password reset email</button><div class="message" id="resetStatus" role="status" aria-live="polite"></div></main><script src="${SUPABASE_BROWSER_SRC}" crossorigin="anonymous"></script><script nonce="${nonce}">(() => {const c=${config},b=document.getElementById('forgotPassword'),s=document.getElementById('resetStatus'),e=document.getElementById('loginEmail');if(!c.url||!c.key||!window.supabase){b.disabled=true;s.textContent='Password recovery is temporarily unavailable.';return;}const x=window.supabase.createClient(c.url,c.key,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});b.addEventListener('click',async()=>{const v=e.value.trim();if(!v||!e.checkValidity()){s.textContent='Enter the account email first.';e.focus();return;}b.disabled=true;s.textContent='Requesting a secure reset link...';const{error}=await x.auth.resetPasswordForEmail(v,{redirectTo:window.location.origin+'/auth/update-password'});if(error){s.textContent='Unable to request a reset link. Please try again.';b.disabled=false;return;}s.textContent='If the account is eligible, a reset link has been sent.';});})();</script></body></html>`;
  return { html, nonce };
}

function recoveryPage() {
  const { nonce, config } = authPageContext();
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Update password · SC Agent OS</title><style>${authStyles()}</style></head><body><main class="box"><div class="brand">SC / DCSE PASSWORD RECOVERY</div><div class="sub">Choose a new password for the authorized account.</div><form id="passwordForm"><label for="newPassword">New Password</label><input class="field" id="newPassword" type="password" autocomplete="new-password" minlength="12" maxlength="72" required disabled><label for="confirmPassword">Confirm Password</label><input class="field" id="confirmPassword" type="password" autocomplete="new-password" minlength="12" maxlength="72" required disabled><button class="btn" id="updatePassword" type="submit" disabled>Update Password</button></form><div class="message" id="recoveryStatus" role="status" aria-live="polite">Validating the recovery link...</div><div class="hint">For safety, recovery links are single-purpose and may expire. Tokens are never displayed or logged.</div><a class="btn secondary" href="/">Return to sign in</a></main><script src="${SUPABASE_BROWSER_SRC}" crossorigin="anonymous"></script><script nonce="${nonce}">(() => {const c=${config},f=document.getElementById('passwordForm'),n=document.getElementById('newPassword'),m=document.getElementById('confirmPassword'),b=document.getElementById('updatePassword'),s=document.getElementById('recoveryStatus');let ready=false,t;function bad(){if(ready)return;s.textContent='This recovery link is invalid or expired. Request a new link from the sign-in page.';s.className='message err';}function ok(){if(ready)return;ready=true;clearTimeout(t);history.replaceState(null,'','/auth/update-password');n.disabled=false;m.disabled=false;b.disabled=false;s.textContent='Recovery link verified. Enter your new password.';s.className='message ok';n.focus();}const q=new URLSearchParams(location.search),h=new URLSearchParams(location.hash.slice(1));if(q.has('error')||h.has('error')){bad();return;}if(!c.url||!c.key||!window.supabase){s.textContent='Password recovery is temporarily unavailable.';s.className='message err';return;}const x=window.supabase.createClient(c.url,c.key,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}}),hint=h.get('type')==='recovery'||q.get('type')==='recovery';x.auth.onAuthStateChange((event,session)=>{if(event==='PASSWORD_RECOVERY'&&session)ok();});x.auth.getSession().then(({data,error})=>{if(!error&&hint&&data.session)ok();});t=setTimeout(bad,4000);f.addEventListener('submit',async event=>{event.preventDefault();if(!ready)return bad();const p=n.value,z=m.value;if(p.length<12||p.length>72||!/[A-Za-z]/.test(p)||!/[0-9]/.test(p)){s.textContent='Use 12–72 characters with at least one letter and one number.';s.className='message err';return;}if(p!==z){s.textContent='The passwords do not match.';s.className='message err';return;}b.disabled=true;s.textContent='Updating password...';s.className='message';const{error}=await x.auth.updateUser({password:p});if(error){s.textContent='Password update failed. The link may have expired; request a new one.';s.className='message err';b.disabled=false;return;}s.textContent='Password updated. Returning to sign in...';s.className='message ok';await x.auth.signOut({scope:'local'});setTimeout(()=>location.replace('/?password_updated=1'),1200);});})();</script></body></html>`;
  return { html, nonce };
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

  const newKeyBlock = `// Cloud credentials are server-managed; Ollama remains local
const PROVIDER_META={anthropic:{label:'Anthropic'},openai:{label:'OpenAI'},google:{label:'Google'},qwen:{label:'Qwen'},ollama:{label:'Ollama'}};
function providerOf(model){if(model.startsWith('claude-'))return'anthropic';if(model.startsWith('gpt-')||model.startsWith('o3'))return'openai';if(model.startsWith('gemini-'))return'google';if(model.startsWith('qwen-'))return'qwen';if(model.startsWith('ollama:'))return'ollama';return'anthropic';}
const keyInput=document.getElementById('apiKeyInput');
function loadKeyForModel(){keyInput.value='server-managed';}
function saveKey(){updateStatus();}
function updateStatus(){const s=document.getElementById('modelStatus');const p=providerOf(document.getElementById('modelSelect').value);if(p==='ollama'){s.textContent='OLLAMA LOCAL';s.className='tag tag-orange';}else{s.textContent=PROVIDER_META[p].label+' SERVER KEY';s.className='tag tag-green';}}
function onModelChange(){const p=providerOf(document.getElementById('modelSelect').value);document.getElementById('ollamaNote').style.display=p==='ollama'?'inline':'none';loadKeyForModel();updateStatus();}
onModelChange();`;

  const oldFetch = "      const apiKey=keyInput.value;\n      if(!PROVIDER_META[p].check(apiKey)){thinking.textContent='Enter '+PROVIDER_META[p].label+' API key ('+PROVIDER_META[p].placeholder+')';thinking.className='msg sys';btn.disabled=false;return;}\n      const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:chatHistory,system:activeSysPrompt,apiKey})});";
  const splitFetch = `      let r;
      if(p==='ollama'){
        const controller=new AbortController();
        const timer=setTimeout(()=>controller.abort(),180000);
        try{
          r=await fetch('http://127.0.0.1:11434/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:model.slice('ollama:'.length),messages:activeSysPrompt?[{role:'system',content:activeSysPrompt},...chatHistory]:chatHistory,stream:false}),signal:controller.signal});
        }catch(error){
          const detail=error&&error.name==='AbortError'?'Local Ollama timed out after 180 seconds.':'Local Ollama is unavailable or blocked by OLLAMA_ORIGINS.';
          throw new Error(detail+' Start Ollama and authorize '+window.location.origin+'.');
        }finally{clearTimeout(timer);}
      }else{
        r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:chatHistory,system:activeSysPrompt})});
      }`;

  const oldOllamaOptions = `<optgroup label="Ollama Local">
              <option value="ollama:nous-hermes2">Nous-Hermes2 (DDNA)</option>
              <option value="ollama:dolphin-mistral">Dolphin Mistral (Uncensored)</option>
              <option value="ollama:qwen2.5">Qwen2.5 (Local)</option>
            </optgroup>`;
  const newOllamaOptions = `<optgroup label="Ollama Local">
              <option value="ollama:nous-hermes2:latest">Nous-Hermes2 11B (DDNA)</option>
              <option value="ollama:dolphin-mistral:latest">Dolphin Mistral 7B (Uncensored)</option>
              <option value="ollama:llama3.1:8b">Llama 3.1 8B</option>
              <option value="ollama:qwen2.5:1.5b">Qwen 2.5 1.5B</option>
              <option value="ollama:smollm2:1.7b">SmolLM2 1.7B</option>
              <option value="ollama:dolphin-phi:2.7b">Dolphin Phi 2.7B</option>
              <option value="ollama:smollm2:360m">SmolLM2 360M</option>
            </optgroup>`;

  return html
    .replace('<input class="key-input" id="apiKeyInput" type="password" placeholder="API key" style="width:170px" oninput="saveKey()" />', '<input id="apiKeyInput" type="hidden" value="server-managed" />')
    .replace('<span id="modelStatus" class="tag tag-amber">KEY NEEDED</span>', '<span id="modelStatus" class="tag tag-green">SERVER KEY</span>')
    .replace(oldKeyBlock, newKeyBlock)
    .replace(oldFetch, splitFetch)
    .replace(oldOllamaOptions, newOllamaOptions)
    .replace(/Select provider, enter API key, and send\./g, 'Select provider and send. Cloud credentials are managed by the server; Ollama runs locally.')
    .replace(/Enter your (Anthropic|Google|OpenAI|Qwen) API key above[^<]*/g, 'Provider credentials are managed securely by the server.');
}

module.exports = async function handler(req, res) {
  const url = new URL(req.url || '/', 'https://dcse.local');
  const action = url.searchParams.get('dcse_auth');

  if (url.pathname === '/auth/update-password' || url.pathname === '/auth/update-password/') {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      res.statusCode = 405; res.setHeader('Allow', 'GET, HEAD'); return res.end('Method Not Allowed');
    }
    return sendAuthPage(res, recoveryPage());
  }

  if (action === 'logout') {
    clearSessionCookies(res); res.statusCode = 302; res.setHeader('Location', '/'); return res.end();
  }

  if (action === 'login' && req.method === 'POST') {
    try {
      const raw = await readBody(req), form = new URLSearchParams(raw);
      const email = String(form.get('email') || '').toLowerCase(), password = String(form.get('password') || '');
      if (email !== OPERATOR_EMAIL) throw new Error('This account is not authorized.');
      const response = await supabaseRequest('/auth/v1/token?grant_type=password', { method: 'POST', body: JSON.stringify({ email, password }) });
      if (!response.ok) throw new Error('Sign-in failed. Check the email and password.');
      const session = await response.json(), user = await validateAccessToken(session.access_token);
      if (!user) throw new Error('This account is not authorized.');
      setSessionCookies(res, session); res.statusCode = 302; res.setHeader('Location', '/'); return res.end();
    } catch (error) { return sendAuthPage(res, loginPage(error.message), 401); }
  }

  let user = null;
  try { user = await authenticate(req, res); } catch (error) { return sendAuthPage(res, loginPage(error.message), 503); }
  if (!user) {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      res.statusCode = 401; res.setHeader('Content-Type', 'application/json'); return res.end(JSON.stringify({ error: 'Authentication required' }));
    }
    const notice = url.searchParams.get('password_updated') === '1' ? 'Password updated successfully. Sign in with the new password.' : '';
    return sendAuthPage(res, loginPage('', notice));
  }

  const origin = req.headers.origin, originalSetHeader = res.setHeader.bind(res);
  res.setHeader = (name, value) => {
    if (String(name).toLowerCase() === 'access-control-allow-origin') {
      if (origin && APPROVED_ORIGINS.has(origin)) return originalSetHeader(name, origin);
      return undefined;
    }
    return originalSetHeader(name, value);
  };
  if (origin && APPROVED_ORIGINS.has(origin)) {
    originalSetHeader('Access-Control-Allow-Origin', origin); originalSetHeader('Vary', 'Origin');
  }

  let forwardedReq = req;
  if (req.method === 'POST' || req.method === 'PUT' || req.method === 'PATCH') {
    const raw = await readBody(req); let nextBody = raw;
    try {
      const parsed = JSON.parse(raw || '{}');
      if (parsed.model && Array.isArray(parsed.messages) && !String(parsed.model).startsWith('ollama:')) {
        const key = providerKey(String(parsed.model));
        if (!key) { res.statusCode = 503; res.setHeader('Content-Type', 'application/json'); return res.end(JSON.stringify({ error: `Server credential not configured for ${parsed.model}` })); }
        parsed.apiKey = key; nextBody = JSON.stringify(parsed);
      }
    } catch (_) {}
    forwardedReq = Readable.from([nextBody]);
    Object.assign(forwardedReq, req);
    forwardedReq.method = req.method; forwardedReq.url = req.url;
    forwardedReq.headers = { ...req.headers, 'content-length': Buffer.byteLength(nextBody) };
  }

  const originalEnd = res.end.bind(res);
  res.end = (chunk, encoding, callback) => {
    const contentType = String(res.getHeader('Content-Type') || res.getHeader('content-type') || '');
    if (chunk && contentType.includes('text/html')) chunk = secureHtml(Buffer.isBuffer(chunk) ? chunk.toString('utf8') : String(chunk));
    return originalEnd(chunk, encoding, callback);
  };

  return innerHandler(forwardedReq, res);
};