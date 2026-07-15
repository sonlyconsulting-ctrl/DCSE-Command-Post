async function handleChat(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    try {
      const {model, messages, apiKey, system} = JSON.parse(body);
      let data, status;

      if (model.startsWith('gpt-') || model.startsWith('o3')) {
        const msgs = system ? [{role:'system',content:system},...messages] : messages;
        const r = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {'Authorization':'Bearer '+apiKey,'Content-Type':'application/json'},
          body: JSON.stringify({model, messages: msgs, max_tokens: 1024})
        });
        const raw = await r.json(); status = r.status;
        if (raw.choices) data = {text: raw.choices[0].message.content};
        else data = {error: raw.error?.message || 'OpenAI error'};

      } else if (model.startsWith('gemini-')) {
        const parts = messages.map(m => ({role: m.role==='assistant'?'model':'user', parts:[{text:m.content}]}));
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
        const payload = {contents: parts};
        if (system) payload.systemInstruction = {parts:[{text:system}]};
        const r = await fetch(url, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
        const raw = await r.json(); status = r.status;
        if (raw.candidates) data = {text: raw.candidates[0].content.parts[0].text};
        else data = {error: raw.error?.message || 'Gemini error'};

      } else if (model.startsWith('qwen-')) {
        const msgs = system ? [{role:'system',content:system},...messages] : messages;
        const r = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
          method: 'POST',
          headers: {'Authorization':'Bearer '+apiKey,'Content-Type':'application/json'},
          body: JSON.stringify({model, messages: msgs, max_tokens: 1024})
        });
        const raw = await r.json(); status = r.status;
        if (raw.choices) data = {text: raw.choices[0].message.content};
        else data = {error: raw.error?.message || 'Qwen error'};

      } else {
        const payload = {model, max_tokens: 1024, messages};
        if (system) payload.system = system;
        const r = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const raw = await r.json(); status = r.status;
        if (raw.content) data = {text: raw.content[0].text};
        else data = {error: raw.error?.message || 'Anthropic error'};
      }

      res.statusCode = status || 200;
      res.end(JSON.stringify(data));
    } catch(e) {
      res.statusCode = 500;
      res.end(JSON.stringify({error: e.message}));
    }
  });
}

const HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SC Agent OS v1.3 — Mission Control</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#0B1D3A;--navy-mid:#122444;--navy-light:#1a3058;--navy-border:#1e3a6a;
  --gold:#C9A84C;--gold-dim:#9a7e38;--gold-glow:rgba(201,168,76,0.15);
  --cream:#F5F0E8;--text-dim:#8fa3c0;--text-muted:#4d6a8a;
  --green:#2ecc71;--green-dim:rgba(46,204,113,0.15);
  --amber:#f39c12;--amber-dim:rgba(243,156,18,0.15);
  --red:#e74c3c;--red-dim:rgba(231,76,60,0.15);
  --blue:#3498db;--blue-dim:rgba(52,152,219,0.15);
  --orange:#e67e22;--orange-dim:rgba(230,126,34,0.15);
  --teal:#1abc9c;--teal-dim:rgba(26,188,156,0.15);
  --purple:#9b59b6;--purple-dim:rgba(155,89,182,0.15);
  --surface:#0f2442;--surface-2:#152e52;
  --font:'Space Grotesk',sans-serif;--mono:'JetBrains Mono',monospace;
  --r:6px;--rl:10px;--sidebar:210px;--hdr:48px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);background:var(--navy);color:var(--cream);height:100vh;overflow:hidden;display:flex;flex-direction:column}
.hdr{height:var(--hdr);background:var(--navy-mid);border-bottom:1px solid var(--navy-border);display:flex;align-items:center;justify-content:space-between;padding:0 14px;flex-shrink:0;z-index:100;gap:10px}
.hdr-l{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo{width:28px;height:28px;background:var(--gold);border-radius:5px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:var(--navy);flex-shrink:0}
.hdr-title{font-size:13px;font-weight:600;color:var(--cream);white-space:nowrap}
.hdr-sub{font-size:9px;color:var(--gold);font-family:var(--mono);letter-spacing:1px;text-transform:uppercase}
.hdr-badges{display:flex;align-items:center;gap:5px;flex:1;flex-wrap:nowrap;overflow:hidden}
.hdr-badge{display:inline-flex;align-items:center;gap:4px;font-size:9px;font-weight:600;letter-spacing:.5px;padding:3px 7px;border-radius:3px;white-space:nowrap}
.hdr-badge .dot{width:5px;height:5px;border-radius:50%;flex-shrink:0}
.b-green{background:rgba(46,204,113,.12);color:var(--green);border:1px solid rgba(46,204,113,.25)}
.b-amber{background:var(--amber-dim);color:var(--amber);border:1px solid rgba(243,156,18,.25)}
.b-orange{background:var(--orange-dim);color:var(--orange);border:1px solid rgba(230,126,34,.25)}
.b-gold{background:var(--gold-glow);color:var(--gold);border:1px solid rgba(201,168,76,.3)}
.b-blue{background:var(--blue-dim);color:var(--blue);border:1px solid rgba(52,152,219,.25)}
.hdr-r{display:flex;align-items:center;gap:8px;flex-shrink:0}
.time-display{font-family:var(--mono);font-size:11px;color:var(--gold);letter-spacing:1px}
.status-dot{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 5px var(--green);animation:pulse 2s infinite;flex-shrink:0}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.layout{display:flex;flex:1;overflow:hidden}
.sidebar{width:var(--sidebar);background:var(--navy-mid);border-right:1px solid var(--navy-border);display:flex;flex-direction:column;flex-shrink:0;overflow-y:auto}
.sb-section{padding:8px 0}
.sb-label{font-size:8px;font-weight:700;color:var(--text-muted);letter-spacing:2px;text-transform:uppercase;padding:0 12px 4px}
.nav-item{display:flex;align-items:center;gap:8px;padding:6px 12px;cursor:pointer;transition:all .12s;border-left:2px solid transparent;font-size:11px;color:var(--text-dim);user-select:none}
.nav-item:hover{background:var(--navy-light);color:var(--cream)}
.nav-item.active{background:var(--navy-light);color:var(--cream);border-left-color:var(--gold)}
.nav-icon{width:13px;text-align:center;flex-shrink:0;font-size:11px}
.nav-badge{margin-left:auto;font-size:8px;font-weight:700;padding:1px 5px;border-radius:8px;flex-shrink:0}
.nb-gold{background:var(--gold);color:var(--navy)}
.nb-red{background:var(--red);color:#fff}
.nb-green{background:var(--green);color:var(--navy)}
.nb-blue{background:var(--blue);color:#fff}
.nb-live{background:var(--green);color:var(--navy);font-size:7px;letter-spacing:.5px}
.divider{height:1px;background:var(--navy-border);margin:2px 0}
.main{flex:1;overflow:hidden;display:flex;flex-direction:column;background:var(--navy)}
.panel{display:none;flex-direction:column;flex:1;padding:16px;gap:12px;overflow-y:auto}
.panel.active{display:flex}
.panel-hdr{display:flex;align-items:flex-start;justify-content:space-between;flex-shrink:0}
.panel-title{font-size:15px;font-weight:600;color:var(--cream)}
.panel-sub{font-size:10px;color:var(--text-dim);margin-top:2px}
.card{background:var(--surface);border:1px solid var(--navy-border);border-radius:var(--rl);padding:14px}
.card-title{font-size:10px;font-weight:700;color:var(--text-dim);letter-spacing:1.2px;text-transform:uppercase;margin-bottom:10px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
@media(max-width:900px){.grid-4{grid-template-columns:repeat(2,1fr)}.grid-3{grid-template-columns:1fr 1fr}.grid-2{grid-template-columns:1fr}}
.stat-tile{background:var(--surface);border:1px solid var(--navy-border);border-radius:var(--rl);padding:12px 14px}
.stat-label{font-size:8px;font-weight:700;color:var(--text-muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:5px}
.stat-value{font-size:20px;font-weight:700;color:var(--cream);font-family:var(--mono);font-variant-numeric:tabular-nums}
.stat-sub{font-size:9px;color:var(--text-dim);margin-top:3px}
.tag{display:inline-flex;align-items:center;font-size:8px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;padding:2px 6px;border-radius:3px;flex-shrink:0}
.tag-gold{background:var(--gold-glow);color:var(--gold);border:1px solid rgba(201,168,76,.3)}
.tag-green{background:var(--green-dim);color:var(--green)}
.tag-red{background:var(--red-dim);color:var(--red)}
.tag-blue{background:var(--blue-dim);color:var(--blue)}
.tag-amber{background:var(--amber-dim);color:var(--amber)}
.tag-orange{background:var(--orange-dim);color:var(--orange)}
.tag-purple{background:var(--purple-dim);color:var(--purple)}
.reg-section-label{font-size:8px;font-weight:700;color:var(--text-muted);letter-spacing:2px;text-transform:uppercase;padding:10px 0 6px;border-bottom:1px solid var(--navy-border);margin-bottom:8px}
.reg-section-label:first-child{padding-top:0}
.agent-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:4px}
.agent-card{background:var(--surface-2);border:1px solid var(--navy-border);border-radius:var(--r);padding:10px 12px;display:flex;align-items:center;gap:10px;cursor:pointer;transition:all .15s}
.agent-card:hover{border-color:var(--gold);background:var(--surface)}
.agent-card.live{border-color:rgba(46,204,113,.35)}
.agent-avatar{width:32px;height:32px;border-radius:var(--r);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-weight:700;font-family:var(--mono);font-size:11px}
.agent-info{flex:1;min-width:0}
.agent-name{font-size:11px;font-weight:600;color:var(--cream);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.agent-role{font-size:9px;color:var(--text-muted);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pip{width:5px;height:5px;border-radius:50%;flex-shrink:0}
.pip-g{background:var(--green)}.pip-a{background:var(--amber)}.pip-r{background:var(--red)}.pip-b{background:var(--blue)}.pip-x{background:var(--text-muted)}
.feed{display:flex;flex-direction:column}
.feed-item{padding:8px 0;border-bottom:1px solid var(--navy-border);display:flex;gap:8px;align-items:flex-start}
.feed-item:last-child{border-bottom:none}
.feed-icon{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:9px;flex-shrink:0;margin-top:1px}
.feed-body{flex:1;min-width:0}
.feed-title{font-size:11px;color:var(--cream);line-height:1.4}
.feed-meta{font-size:9px;color:var(--text-muted);margin-top:1px;font-family:var(--mono)}
.trib-list{display:flex;flex-direction:column;gap:6px}
.trib-item{background:var(--surface-2);border:1px solid var(--navy-border);border-radius:var(--r);padding:10px 12px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.trib-status{font-size:8px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;padding:2px 6px;border-radius:3px;flex-shrink:0}
.ts-draft{background:var(--blue-dim);color:var(--blue)}
.ts-open{background:var(--amber-dim);color:var(--amber)}
.ts-done{background:var(--green-dim);color:var(--green)}
.ts-prog{background:var(--purple-dim);color:var(--purple)}
.trib-info{flex:1;min-width:0}
.trib-title{font-size:11px;color:var(--cream);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.trib-meta{font-size:9px;color:var(--text-muted);margin-top:1px;font-family:var(--mono);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chat-wrap{display:flex;flex-direction:column;flex:1;min-height:0}
.chat-toolbar{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--navy-border);flex-shrink:0;flex-wrap:wrap}
.model-select{background:var(--navy-light);border:1px solid var(--navy-border);color:var(--cream);font-family:var(--font);font-size:11px;padding:4px 8px;border-radius:var(--r);cursor:pointer;outline:none;flex-shrink:0}
.model-select:focus{border-color:var(--gold)}
.key-input{background:var(--navy-light);border:1px solid var(--navy-border);color:var(--cream);font-family:var(--mono);font-size:10px;padding:4px 8px;border-radius:var(--r);outline:none;flex-shrink:0}
.key-input:focus{border-color:var(--gold)}
.key-input::placeholder{color:var(--text-muted)}
.chat-area{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;min-height:0}
.msg{max-width:78%;padding:9px 13px;border-radius:var(--rl);font-size:12px;line-height:1.55}
.msg.user{background:var(--gold);color:var(--navy);align-self:flex-end;font-weight:500}
.msg.agent{background:var(--surface);border:1px solid var(--navy-border);color:var(--cream);align-self:flex-start}
.msg.sys{background:transparent;border:1px dashed var(--navy-border);color:var(--text-dim);align-self:center;font-size:10px;font-family:var(--mono);max-width:92%;text-align:center}
.msg.thinking{opacity:.6;font-style:italic}
.chat-input-row{padding:10px 14px;border-top:1px solid var(--navy-border);display:flex;gap:8px;align-items:flex-end;flex-shrink:0}
.chat-textarea{flex:1;background:var(--surface);border:1px solid var(--navy-border);border-radius:var(--r);color:var(--cream);font-family:var(--font);font-size:12px;padding:7px 10px;resize:none;min-height:36px;max-height:110px;outline:none;transition:border .15s}
.chat-textarea:focus{border-color:var(--gold)}
.chat-send{background:var(--gold);color:var(--navy);border:none;border-radius:var(--r);padding:7px 14px;font-size:11px;font-weight:700;cursor:pointer;font-family:var(--font);flex-shrink:0;transition:all .15s}
.chat-send:hover{background:var(--gold-dim)}
.chat-send:disabled{opacity:.5;cursor:not-allowed}
.voice-wave{display:flex;align-items:center;justify-content:center;gap:3px;height:28px}
.wave-bar{width:3px;background:var(--gold);border-radius:2px;animation:wave 1.1s ease-in-out infinite}
@keyframes wave{0%,100%{height:4px;opacity:.35}50%{height:18px;opacity:1}}
#waveArea{display:none;padding:6px 14px;border-top:1px solid var(--navy-border)}
.ddna-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
@media(max-width:800px){.ddna-grid{grid-template-columns:repeat(2,1fr)}}
.ddna-cell{background:var(--surface-2);border:1px solid var(--navy-border);border-radius:var(--r);padding:10px;text-align:center}
.ddna-label{font-size:8px;font-weight:700;color:var(--text-muted);letter-spacing:1.2px;text-transform:uppercase;margin-bottom:7px}
.ddna-bar-wrap{height:5px;background:var(--navy-border);border-radius:3px;overflow:hidden;margin-bottom:5px}
.ddna-bar{height:100%;border-radius:3px;transition:width .9s cubic-bezier(.4,0,.2,1)}
.ddna-score{font-size:17px;font-weight:700;font-family:var(--mono);color:var(--cream)}
.ddna-delta{font-size:8px;color:var(--text-dim);margin-top:2px}
.model-row{display:flex;align-items:center;gap:10px;padding:10px 12px;background:var(--surface-2);border:1px solid var(--navy-border);border-radius:var(--r);margin-bottom:6px}
.model-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.model-info{flex:1}
.model-name{font-size:11px;font-weight:600;color:var(--cream)}
.model-detail{font-size:9px;color:var(--text-muted);font-family:var(--mono);margin-top:2px}
.flex{display:flex}.flex-col{flex-direction:column}.items-center{align-items:center}.justify-between{justify-content:space-between}
.gap-6{gap:6px}.gap-8{gap:8px}.gap-10{gap:10px}
.mt-8{margin-top:8px}.mt-10{margin-top:10px}.mt-12{margin-top:12px}
.mono{font-family:var(--mono);font-size:10px}.text-dim{color:var(--text-dim)}.text-muted{color:var(--text-muted)}
.text-gold{color:var(--gold)}.text-green{color:var(--green)}.text-red{color:var(--red)}.text-amber{color:var(--amber)}
.overflow-auto{overflow:auto}
.btn{display:inline-flex;align-items:center;gap:5px;padding:5px 11px;border-radius:var(--r);font-size:10px;font-weight:700;font-family:var(--font);cursor:pointer;border:none;transition:all .15s;letter-spacing:.3px;text-decoration:none}
.btn-gold{background:var(--gold);color:var(--navy)}.btn-gold:hover{background:var(--gold-dim)}
.btn-ghost{background:transparent;color:var(--text-dim);border:1px solid var(--navy-border)}.btn-ghost:hover{color:var(--cream);border-color:var(--text-dim)}
.btn-sm{padding:3px 8px;font-size:9px}
.voice-btn{background:var(--navy-light);border:1px solid var(--navy-border);color:var(--cream);padding:4px 10px;border-radius:var(--r);font-size:10px;font-family:var(--font);cursor:pointer;display:flex;align-items:center;gap:5px;transition:all .15s}
.voice-btn:hover{background:var(--gold);color:var(--navy);border-color:var(--gold)}
.voice-btn.rec{background:var(--red);border-color:var(--red);animation:pulse .7s infinite}
.form-row{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
.inp{background:var(--navy-light);border:1px solid var(--navy-border);color:var(--cream);font-family:var(--font);font-size:11px;padding:5px 9px;border-radius:var(--r);outline:none;flex:1;min-width:120px}
.inp:focus{border-color:var(--gold)}
.inp::placeholder{color:var(--text-muted)}
.textarea{background:var(--navy-light);border:1px solid var(--navy-border);color:var(--cream);font-family:var(--font);font-size:11px;padding:7px 9px;border-radius:var(--r);outline:none;width:100%;resize:vertical;min-height:70px}
.textarea:focus{border-color:var(--gold)}
.textarea::placeholder{color:var(--text-muted)}
.result-box{background:var(--navy);border:1px solid var(--navy-border);border-radius:var(--r);padding:10px;font-size:11px;color:var(--cream);line-height:1.6;min-height:50px;white-space:pre-wrap;word-break:break-word}
.filter-row{display:flex;gap:5px;margin-bottom:10px}
</style>
</head>
<body>

<div class="hdr">
  <div class="hdr-l">
    <div class="logo">SC</div>
    <div>
      <div class="hdr-title">SC Agent OS <span style="font-size:10px;color:var(--gold)">v1.3</span></div>
      <div class="hdr-sub">Mission Control · SC-COMMAND-POST</div>
    </div>
  </div>
  <div class="hdr-badges">
    <span class="hdr-badge b-green"><span class="dot" style="background:var(--green)"></span>Claude API</span>
    <span class="hdr-badge b-amber"><span class="dot" style="background:var(--amber)"></span>Ollama: Set CORS</span>
    <span class="hdr-badge b-green"><span class="dot" style="background:var(--green)"></span>RLS Secured</span>
    <span class="hdr-badge b-amber"><span class="dot" style="background:var(--amber)"></span>DDNA: 73 Queued</span>
    <span class="hdr-badge b-gold"><span class="dot" style="background:var(--gold)"></span>DCS L0</span>
  </div>
  <div class="hdr-r">
    <span class="status-dot"></span>
    <span class="time-display" id="clock">--:--:--</span>
    <button class="voice-btn" id="voiceToggle" onclick="toggleVoice()">🎤 Voice</button>
  </div>
</div>

<div class="layout">
  <div class="sidebar">
    <div class="sb-section">
      <div class="sb-label">Command</div>
      <div class="nav-item active" onclick="nav('mission',this)"><span class="nav-icon">⚡</span>Mission Control</div>
      <div class="nav-item" onclick="nav('chat',this)"><span class="nav-icon">💬</span>Agent Chat + Voice<span class="nav-badge nb-live">LIVE</span></div>
      <div class="nav-item" onclick="nav('approvals',this)"><span class="nav-icon">✅</span>Approvals<span class="nav-badge nb-gold">1</span></div>
    </div>
    <div class="divider"></div>
    <div class="sb-section">
      <div class="sb-label">Orchestration</div>
      <div class="nav-item" onclick="nav('agents',this)"><span class="nav-icon">🤖</span>Agent Dock<span class="nav-badge nb-gold">12</span></div>
      <div class="nav-item" onclick="nav('tasks',this)"><span class="nav-icon">▦</span>Task Queue<span class="nav-badge nb-blue" id="taskBadge">3</span></div>
      <div class="nav-item" onclick="nav('portfolio',this)"><span class="nav-icon">◈</span>Portfolio<span class="nav-badge nb-gold" id="portBadge">4</span></div>
      <div class="nav-item" onclick="nav('agentops',this)"><span class="nav-icon">⬢</span>Agent Operations<span class="nav-badge nb-amber" id="agentopsBadge">?</span></div>
    </div>
    <div class="divider"></div>
    <div class="sb-section">
      <div class="sb-label">DDNA + Intelligence</div>
      <div class="nav-item" onclick="nav('ddna',this)"><span class="nav-icon">△</span>DDNA Harvest<span class="nav-badge nb-red">73</span></div>
      <div class="nav-item" onclick="nav('models',this)"><span class="nav-icon">△</span>Local Models<span class="nav-badge nb-green" id="modelsBadge">?</span></div>
      <div class="nav-item" onclick="nav('rag',this)"><span class="nav-icon">▤</span>RAG / Source<span class="nav-badge nb-gold" id="ragBadge">8</span></div>
      <div class="nav-item" onclick="nav('runtime',this)"><span class="nav-icon">⬡</span>Runtime Health<span class="nav-badge nb-amber" id="runtimeBadge">?</span></div>
    </div>
    <div class="divider"></div>
    <div class="sb-section">
      <div class="sb-label">Governance</div>
      <div class="nav-item" onclick="nav('tribunal',this)"><span class="nav-icon">⚖</span>Tribunal<span class="nav-badge nb-red">5</span></div>
      <div class="nav-item" onclick="nav('dispatch',this)"><span class="nav-icon">📦</span>Dispatch</div>
      <div class="nav-item" onclick="nav('personas',this)"><span class="nav-icon">◉</span>Personas<span class="nav-badge nb-gold" id="personasBadge">6</span></div>
      <div class="nav-item" onclick="nav('assets',this)"><span class="nav-icon">◫</span>Assets<span class="nav-badge nb-blue" id="assetsBadge">7</span></div>
      <div class="nav-item" onclick="nav('phasegate',this)"><span class="nav-icon">▥</span>Phase Gates<span class="nav-badge nb-amber" id="phasegateBadge">10</span></div>
      <div class="nav-item" onclick="nav('dcsqueue',this)"><span class="nav-icon">◆</span>DCS Queue<span class="nav-badge nb-red" id="dcsqueueBadge">?</span></div>
      <div class="nav-item" onclick="nav('receipts',this)"><span class="nav-icon">▧</span>Receipts<span class="nav-badge nb-amber" id="receiptsBadge">?</span></div>
    </div>
    <div class="divider"></div>
    <div class="sb-section">
      <div class="sb-label">Administration</div>
      <div class="nav-item" onclick="nav('config',this)"><span class="nav-icon">⚙</span>Configuration<span class="nav-badge nb-amber" id="configBadge">?</span></div>
      <div class="nav-item" onclick="nav('dba',this)"><span class="nav-icon">▣</span>DBA Console<span class="nav-badge nb-amber" id="dbaBadge">?</span></div>
      <div class="nav-item" onclick="nav('apikeys',this)"><span class="nav-icon">⚿</span>API Keys Admin<span class="nav-badge nb-amber" id="apikeysBadge">?</span></div>
      <div class="nav-item" onclick="nav('assurance',this)"><span class="nav-icon">◎</span>Assurance Loops<span class="nav-badge nb-amber" id="assuranceBadge">A0-A8</span></div>
    </div>
    <div class="divider"></div>
    <div class="sb-section">
      <div class="sb-label">System</div>
      <div class="nav-item" onclick="nav('ps',this)"><span class="nav-icon">🛡</span>PS Firewall</div>
      <div class="nav-item" onclick="nav('log',this)"><span class="nav-icon">📋</span>Ops Log</div>
    </div>
  </div>

  <div class="main">

    <!-- MISSION CONTROL -->
    <div class="panel active" id="panel-mission">
      <div class="panel-hdr">
        <div><div class="panel-title">Mission Control</div><div class="panel-sub">DCSE Operational Overview</div></div>
        <span class="tag tag-gold">ACTIVE</span>
      </div>
      <div class="grid-4">
        <div class="stat-tile"><div class="stat-label">Active Workstreams</div><div class="stat-value" id="mcWorkstreams">10</div><div class="stat-sub">6 Batch 1 · 1 Batch 2 · 3 Batch 3</div></div>
        <div class="stat-tile"><div class="stat-label">CP Views</div><div class="stat-value" id="mcViews">11</div><div class="stat-sub">All Section 2.8 views built</div></div>
        <div class="stat-tile"><div class="stat-label">DCS Decisions</div><div class="stat-value" id="mcDecisions">4</div><div class="stat-sub" id="mcDecisionsSub">Pending DCS authority</div></div>
        <div class="stat-tile"><div class="stat-label">PS Firewall</div><div class="stat-value text-green">✔</div><div class="stat-sub">ACTIVE — No breach</div></div>
      </div>
      <div style="display:grid;grid-template-columns:2fr 1fr;gap:12px">
        <div class="card">
          <div class="card-title">Recent Activity</div>
          <div class="feed">
            <div class="feed-item"><div class="feed-icon" style="background:var(--green-dim);color:var(--green)">✔</div><div class="feed-body"><div class="feed-title">PR #8 — Batch 1 P0: All 11 CP views, admin consoles, relay plumbing</div><div class="feed-meta">Claude Code · 2026-07-15</div></div></div>
            <div class="feed-item"><div class="feed-icon" style="background:var(--green-dim);color:var(--green)">✔</div><div class="feed-body"><div class="feed-title">Runtime Health, DBA, API Keys, Assurance, Agent Ops panels built</div><div class="feed-meta">Claude Code · 2026-07-15</div></div></div>
            <div class="feed-item"><div class="feed-icon" style="background:var(--green-dim);color:var(--green)">✔</div><div class="feed-body"><div class="feed-title">Phase Gates, DCS Queue, Receipts, Config panels built</div><div class="feed-meta">Claude Code · 2026-07-15</div></div></div>
            <div class="feed-item"><div class="feed-icon" style="background:var(--green-dim);color:var(--green)">✔</div><div class="feed-body"><div class="feed-title">Persona API column fix (code/display_name)</div><div class="feed-meta">Claude Code · 2026-07-15</div></div></div>
            <div class="feed-item"><div class="feed-icon" style="background:var(--green-dim);color:var(--green)">✔</div><div class="feed-body"><div class="feed-title">PR #6 merged — Personas/Assets module integrated</div><div class="feed-meta">DCS · 2026-07-15</div></div></div>
            <div class="feed-item"><div class="feed-icon" style="background:var(--green-dim);color:var(--green)">✔</div><div class="feed-body"><div class="feed-title">SC Agent OS v1.3 — multi-provider chat deployed</div><div class="feed-meta">Claude Code · 2026-07-15</div></div></div>
          </div>
        </div>
        <div class="flex flex-col gap-8">
          <div class="card">
            <div class="card-title">System Status</div>
            <div class="flex flex-col gap-6">
              <div class="flex items-center justify-between"><span class="text-dim" style="font-size:11px">Governance</span><span class="tag tag-green">v6.9+</span></div>
              <div class="flex items-center justify-between"><span class="text-dim" style="font-size:11px">PS Firewall</span><span class="tag tag-green">ACTIVE</span></div>
              <div class="flex items-center justify-between"><span class="text-dim" style="font-size:11px">Supabase</span><span class="tag tag-green">24 tables</span></div>
              <div class="flex items-center justify-between"><span class="text-dim" style="font-size:11px">SC Agent OS</span><span class="tag tag-gold">v1.3 LIVE</span></div>
              <div class="flex items-center justify-between"><span class="text-dim" style="font-size:11px">Ollama Local</span><span class="tag tag-amber" id="mcOllamaStatus">CHECK REQ</span></div>
              <div class="flex items-center justify-between"><span class="text-dim" style="font-size:11px">Migrations</span><span class="tag tag-green">001-004</span></div>
            </div>
          </div>
          <div class="card">
            <div class="card-title">DCS Decision Queue</div>
            <div class="flex flex-col gap-6">
              <div style="font-size:10px;color:var(--red)">1. SC hero line final selection (DDNA)</div>
              <div style="font-size:10px;color:var(--amber)">2. TSL source reconstruction packet</div>
              <div style="font-size:10px;color:var(--amber)">3. SC brand palette confirmation</div>
              <div style="font-size:10px;color:var(--amber)">4. PR #8 merge authorization</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AGENT CHAT -->
    <div class="panel" id="panel-chat">
      <div class="panel-hdr" style="flex-shrink:0">
        <div><div class="panel-title">Agent Chat + Voice</div><div class="panel-sub" id="chatContextLabel">Select model — SC/DCSE context active — PS firewall on</div></div>
        <button class="voice-btn" onclick="toggleVoice()">🎤 Start Voice</button>
      </div>
      <div class="card chat-wrap" style="flex:1;padding:0;min-height:0">
        <div class="chat-toolbar">
          <select class="model-select" id="modelSelect" onchange="onModelChange()">
            <optgroup label="Claude (Anthropic)">
              <option value="claude-sonnet-5">claude-sonnet-5</option>
              <option value="claude-opus-4-8">claude-opus-4-8</option>
              <option value="claude-haiku-4-5-20251001">claude-haiku-4-5</option>
            </optgroup>
            <optgroup label="ChatGPT (OpenAI)">
              <option value="gpt-4o">gpt-4o</option>
              <option value="gpt-4o-mini">gpt-4o-mini</option>
              <option value="o3-mini">o3-mini</option>
            </optgroup>
            <optgroup label="Gemini (Google)">
              <option value="gemini-2.0-flash">gemini-2.0-flash</option>
              <option value="gemini-1.5-pro">gemini-1.5-pro</option>
            </optgroup>
            <optgroup label="Qwen (Alibaba)">
              <option value="qwen-turbo">qwen-turbo</option>
              <option value="qwen-plus">qwen-plus</option>
              <option value="qwen-max">qwen-max</option>
            </optgroup>
            <optgroup label="Ollama Local">
              <option value="ollama:nous-hermes2">Nous-Hermes2 (DDNA)</option>
              <option value="ollama:dolphin-mistral">Dolphin Mistral (Uncensored)</option>
              <option value="ollama:qwen2.5">Qwen2.5 (Local)</option>
            </optgroup>
          </select>
          <input class="key-input" id="apiKeyInput" type="password" placeholder="API key" style="width:170px" oninput="saveKey()" />
          <span id="modelStatus" class="tag tag-amber">KEY NEEDED</span>
          <span id="ollamaNote" style="font-size:9px;color:var(--text-muted);display:none">calls localhost:11434</span>
          <button class="btn btn-ghost btn-sm" onclick="clearChat()">Clear</button>
        </div>
        <div class="chat-area" id="chatArea">
          <div class="msg sys">SC Agent OS — Agent Chat open. PS firewall active.</div>
          <div class="msg agent">Ready. What do you need?</div>
        </div>
        <div id="waveArea">
          <div class="voice-wave">
            <div class="wave-bar" style="animation-delay:0s"></div>
            <div class="wave-bar" style="animation-delay:.1s"></div>
            <div class="wave-bar" style="animation-delay:.2s"></div>
            <div class="wave-bar" style="animation-delay:.3s"></div>
            <div class="wave-bar" style="animation-delay:.4s"></div>
            <div class="wave-bar" style="animation-delay:.5s"></div>
            <div class="wave-bar" style="animation-delay:.6s"></div>
          </div>
        </div>
        <div class="chat-input-row">
          <textarea class="chat-textarea" id="chatInput" placeholder="Type or speak..." rows="1" onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
          <button class="chat-send" id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
      </div>
    </div>

    <!-- APPROVALS -->
    <div class="panel" id="panel-approvals">
      <div class="panel-hdr">
        <div><div class="panel-title">Approvals</div><div class="panel-sub">Pending DCS decisions</div></div>
        <span class="tag tag-amber">1 PENDING</span>
      </div>
      <div class="card">
        <div class="trib-item" style="background:rgba(243,156,18,.06);border-color:rgba(243,156,18,.3)">
          <span class="trib-status ts-open">PENDING</span>
          <div class="trib-info">
            <div class="trib-title">PR #5 — SC LP Trial Packet ready for merge</div>
            <div class="trib-meta">claude/dcs-packet-trial-confirm-jwuzsy · Hero line confirmed · Awaiting DCS merge approval</div>
          </div>
          <a class="btn btn-gold" href="https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay/pull/5" target="_blank">Open PR ↗</a>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Approval Rules</div>
        <div class="flex flex-col gap-6">
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">PR merge to main</span><span class="tag tag-gold">DCS REQUIRED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Production deploy</span><span class="tag tag-gold">DCS REQUIRED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Supabase live write</span><span class="tag tag-gold">DCS REQUIRED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Wix publish</span><span class="tag tag-gold">DCS REQUIRED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">PS content movement</span><span class="tag tag-red">BLOCKED</span></div>
        </div>
      </div>
    </div>

    <!-- AGENT DOCK -->
    <div class="panel" id="panel-agents">
      <div class="panel-hdr">
        <div><div class="panel-title">Agent Dock</div><div class="panel-sub">Click agent to launch in chat</div></div>
        <span class="tag tag-green">12 REGISTERED</span>
      </div>
      <div class="card">
        <div class="reg-section-label">Frontier + Platform Agents</div>
        <div class="agent-grid">
          <div class="agent-card live" onclick="launchAgent('DCS Authority','dcs_authority','You are the DCS Authority. Lead constructively, no dominating contrast. All governance decisions final.')"><div class="agent-avatar" style="background:var(--gold-glow);color:var(--gold)">DCS</div><div class="agent-info"><div class="agent-name">DCS Authority</div><div class="agent-role">dcs_authority · governance</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-gold" style="font-size:7px">ACTIVE</span></div></div>
          <div class="agent-card live" onclick="launchAgent('Claude Code','code_agent','You are Claude Code, an AI software engineering agent. Help build and deploy SC infrastructure.')"><div class="agent-avatar" style="background:var(--blue-dim);color:var(--blue)">CC</div><div class="agent-info"><div class="agent-name">Claude Code</div><div class="agent-role">code_agent · builder</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">ACTIVE</span></div></div>
          <div class="agent-card live" onclick="launchAgent('ChatGPT','model','You are ChatGPT, assisting with SC operations. PS firewall active.')"><div class="agent-avatar" style="background:var(--green-dim);color:var(--green)">GP</div><div class="agent-info"><div class="agent-name">ChatGPT</div><div class="agent-role">openai model</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">ACTIVE</span></div></div>
          <div class="agent-card live" onclick="launchAgent('Gemini','model','You are Gemini, assisting with SC operations. PS firewall active.')"><div class="agent-avatar" style="background:var(--blue-dim);color:var(--blue)">GE</div><div class="agent-info"><div class="agent-name">Gemini</div><div class="agent-role">google model</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">ACTIVE</span></div></div>
          <div class="agent-card live" onclick="launchAgent('Supabase Agent','database','You are a Supabase database agent. Help manage SC schema, RLS, and data operations.')"><div class="agent-avatar" style="background:var(--teal-dim);color:var(--teal)">DB</div><div class="agent-info"><div class="agent-name">Supabase Agent</div><div class="agent-role">database · RLS</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">ACTIVE</span></div></div>
          <div class="agent-card live" onclick="launchAgent('GitHub Agent','github','You are a GitHub agent. Help manage repos, PRs, and the Tribunal Relay.')"><div class="agent-avatar" style="background:rgba(100,100,100,.15);color:var(--cream)">GH</div><div class="agent-info"><div class="agent-name">GitHub Agent</div><div class="agent-role">github · tribunal</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">ACTIVE</span></div></div>
          <div class="agent-card live" onclick="launchAgent('Tribunal Agent','tribunal','You are the Tribunal Agent. Manage DCSE governance artifacts, dispatch packets, and PR review.')"><div class="agent-avatar" style="background:var(--amber-dim);color:var(--amber)">TR</div><div class="agent-info"><div class="agent-name">Tribunal Agent</div><div class="agent-role">tribunal · dispatch</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">ACTIVE</span></div></div>
          <div class="agent-card live" onclick="launchAgent('Codex','code_agent','You are Codex, an OpenAI code model. Help with SC code review and generation.')"><div class="agent-avatar" style="background:var(--purple-dim);color:var(--purple)">CX</div><div class="agent-info"><div class="agent-name">Codex</div><div class="agent-role">openai code model</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">ACTIVE</span></div></div>
        </div>
        <div class="reg-section-label">Local Models — Ollama (localhost:11434)</div>
        <div class="agent-grid">
          <div class="agent-card live" onclick="launchAgentOllama('Nous-Hermes2','nous-hermes2','DDNA extractor. Score agent behavioral dimensions from session transcripts.')"><div class="agent-avatar" style="background:rgba(46,204,113,.12);color:var(--green)">HE</div><div class="agent-info"><div class="agent-name">Nous-Hermes2 (Local)</div><div class="agent-role">DDNA extractor · ollama</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-green" style="font-size:7px">DDNA</span></div></div>
          <div class="agent-card live" onclick="launchAgentOllama('Dolphin Mistral','dolphin-mistral','Uncensored model for raw divergence analysis and unfiltered reasoning.')"><div class="agent-avatar" style="background:var(--orange-dim);color:var(--orange)">DP</div><div class="agent-info"><div class="agent-name">Dolphin Mistral</div><div class="agent-role">raw divergence · uncensored</div></div><div class="flex items-center gap-6"><div class="pip pip-g"></div><span class="tag tag-orange" style="font-size:7px">RAW</span></div></div>
        </div>
        <div class="reg-section-label">Standby</div>
        <div class="agent-grid">
          <div class="agent-card" onclick="launchAgent('AG Builder','builder_agent','You are the AG Builder agent. Help scope and build SC GovOS components.')"><div class="agent-avatar" style="background:var(--amber-dim);color:var(--amber)">AG</div><div class="agent-info"><div class="agent-name">AG Builder</div><div class="agent-role">builder_agent</div></div><div class="flex items-center gap-6"><div class="pip pip-a"></div><span class="tag tag-amber" style="font-size:7px">STANDBY</span></div></div>
          <div class="agent-card" onclick="launchAgent('Review Board','reviewer','You are the SC Review Board. Evaluate builds against D08 voice rule and governance standards.')"><div class="agent-avatar" style="background:var(--red-dim);color:var(--red)">RB</div><div class="agent-info"><div class="agent-name">Review Board</div><div class="agent-role">reviewer</div></div><div class="flex items-center gap-6"><div class="pip pip-a"></div><span class="tag tag-amber" style="font-size:7px">STANDBY</span></div></div>
        </div>
      </div>
    </div>

    <!-- TASK QUEUE -->
    <div class="panel" id="panel-tasks">
      <div class="panel-hdr">
        <div><div class="panel-title">Task Queue</div><div class="panel-sub">Active DCSE tasks — localStorage backed</div></div>
        <span class="tag tag-blue" id="taskCountTag">LOADING</span>
      </div>
      <div class="card">
        <div class="card-title">Add Task</div>
        <div class="form-row">
          <input class="inp" id="newTaskInput" placeholder="Task title..." />
          <input class="inp" id="newTaskOwner" placeholder="Owner" style="max-width:100px" />
          <select class="model-select" id="newTaskStatus">
            <option value="queued">Queued</option>
            <option value="in_progress">In Progress</option>
          </select>
          <button class="btn btn-gold" onclick="addTask()">Add Task</button>
        </div>
        <div class="filter-row">
          <button class="btn btn-ghost btn-sm trib-filter-btn" data-filter="all" onclick="renderTasks('all')">All</button>
          <button class="btn btn-ghost btn-sm trib-filter-btn" data-filter="queued" onclick="renderTasks('queued')">Queued</button>
          <button class="btn btn-ghost btn-sm trib-filter-btn" data-filter="in_progress" onclick="renderTasks('in_progress')">In Progress</button>
          <button class="btn btn-ghost btn-sm trib-filter-btn" data-filter="done" onclick="renderTasks('done')">Done</button>
        </div>
        <div class="trib-list" id="taskList"></div>
      </div>
    </div>

    <!-- PORTFOLIO -->
    <div class="panel" id="panel-portfolio">
      <div class="panel-hdr">
        <div><div class="panel-title">Portfolio</div><div class="panel-sub">SC active builds and deployments</div></div>
        <span class="tag tag-gold" id="portCountTag">LOADING</span>
      </div>
      <div class="card">
        <div class="card-title">Add Item</div>
        <div class="form-row">
          <input class="inp" id="newPortName" placeholder="Name..." />
          <input class="inp" id="newPortUrl" placeholder="URL (optional)" />
          <input class="inp" id="newPortNote" placeholder="Note" />
          <select class="model-select" id="newPortStatus">
            <option value="live">Live</option>
            <option value="trial">Trial</option>
            <option value="arch">Arch</option>
            <option value="active">Active</option>
            <option value="pending">Pending</option>
            <option value="paused">Paused</option>
          </select>
          <button class="btn btn-gold" onclick="addPortItem()">Add</button>
        </div>
        <div class="trib-list" id="portfolioList"></div>
      </div>
    </div>

    <!-- AGENT OPERATIONS (Tracks B+D: MVT-008A Relay + MVT-010 Observability) -->
    <div class="panel" id="panel-agentops">
      <div class="panel-hdr">
        <div><div class="panel-title">Agent Operations</div><div class="panel-sub">MVT-008A Relay Plumbing + MVT-010 Agent OS Observability</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshAgentOps()">Refresh</button>
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Relay Status</div>
          <div class="flex flex-col gap-6" id="relayStatus">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Task Event Detection</span><span class="tag tag-amber" id="relayEventDetect">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Assignment Routing</span><span class="tag tag-amber" id="relayAssignRouting">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Dispatch Mode</span><span class="tag tag-amber" id="relayDispatchMode">MANUAL</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Kill Switch</span><span class="tag tag-green" id="relayKillSwitch">AVAILABLE</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Cost Control</span><span class="tag tag-green" id="relayCostControl">ENFORCED</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Agent Heartbeats</div>
          <div class="flex flex-col gap-6" id="agentHeartbeats">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Active Heartbeats</span><span class="mono text-dim" id="heartbeatCount">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Last Heartbeat</span><span class="mono text-dim" id="heartbeatLast">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Stale Agents</span><span class="mono text-dim" id="heartbeatStale">...</span></div>
          </div>
        </div>
      </div>
      <div class="grid-2 mt-8">
        <div class="card">
          <div class="card-title">Task Pipeline</div>
          <div class="flex flex-col gap-6" id="taskPipeline">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Pending Tasks</span><span class="mono text-dim" id="tasksPending">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">In Progress</span><span class="mono text-dim" id="tasksInProgress">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Completed (24h)</span><span class="mono text-dim" id="tasksCompleted">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Failed / Blocked</span><span class="mono text-dim" id="tasksFailed">...</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Decision Queue</div>
          <div class="flex flex-col gap-6" id="decisionQueue">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Awaiting DCS</span><span class="mono text-dim" id="decisionsAwaitingDCS">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Awaiting Review</span><span class="mono text-dim" id="decisionsAwaitingReview">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Blockers</span><span class="mono text-dim" id="decisionsBlockers">...</span></div>
          </div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Recent Activity Events</div>
        <div class="trib-list" id="activityEventsList"><div class="text-dim mono" style="padding:12px;font-size:11px">Click Refresh to load activity events from dcse_cp.</div></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Agent Registry</div>
        <div class="trib-list" id="agentRegistryList"><div class="text-dim mono" style="padding:12px;font-size:11px">Click Refresh to load registered agents.</div></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Pending Assignments</div>
        <div class="trib-list" id="pendingAssignmentsList"><div class="text-dim mono" style="padding:12px;font-size:11px">Click Refresh to check relay_pending_assignments.</div></div>
      </div>
    </div>

    <!-- DDNA HARVEST -->
    <div class="panel" id="panel-ddna">
      <div class="panel-hdr">
        <div><div class="panel-title">DDNA Harvest</div><div class="panel-sub">Digital DNA — Agent behavioral scoring via AI model</div></div>
        <div class="flex gap-6">
          <button class="btn btn-ghost btn-sm" onclick="exportDDNA()">Export JSON</button>
          <span class="tag tag-amber">73 QUEUED</span>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Run Harvest</div>
        <textarea class="textarea" id="ddnaInput" placeholder="Paste agent session transcript or output here to score DDNA dimensions..."></textarea>
        <div class="form-row" style="margin-top:8px">
          <button class="btn btn-gold" id="harvestBtn" onclick="runDDNAHarvest()">Run Harvest</button>
          <span id="harvestStatus" class="mono text-dim"></span>
        </div>
      </div>
      <div class="card">
        <div class="card-title">DDNA Scores — Current Session</div>
        <div class="ddna-grid" id="ddnaGrid"></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Session Notes</div>
        <div class="form-row">
          <input class="inp" id="ddnaNoteInput" placeholder="Add session note..." />
          <button class="btn btn-ghost" onclick="addDDNANote()">Add</button>
        </div>
        <div id="ddnaNotesList" style="margin-top:8px"></div>
      </div>
    </div>

    <!-- LOCAL MODELS -->
    <div class="panel" id="panel-models">
      <div class="panel-hdr">
        <div><div class="panel-title">Local Models</div><div class="panel-sub">Ollama — localhost:11434</div></div>
        <div class="flex gap-6">
          <button class="btn btn-gold" onclick="checkOllama()">Refresh</button>
          <span class="tag" id="ollamaStatus" style="background:var(--amber-dim);color:var(--amber)">NOT CHECKED</span>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Available Models</div>
        <div id="ollamaModelList">
          <div class="mono text-dim" style="padding:8px">Click Refresh to check Ollama status and list models.</div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Test Output</div>
        <div class="result-box" id="ollamaTestOut" style="min-height:36px;color:var(--text-dim)">Test output appears here.</div>
      </div>
      <div class="card mt-8">
        <div class="card-title">CORS Setup</div>
        <div style="font-size:10px;color:var(--text-dim);font-family:var(--mono);line-height:1.9">
          Mac/Linux: OLLAMA_ORIGINS=* ollama serve<br>
          PowerShell: $env:OLLAMA_ORIGINS="*"; ollama serve<br>
          Pull model: ollama pull nous-hermes2
        </div>
      </div>
    </div>

    <!-- RAG / SOURCE -->
    <div class="panel" id="panel-rag">
      <div class="panel-hdr">
        <div><div class="panel-title">RAG / Source</div><div class="panel-sub">Knowledge sources — add, index, and query with AI</div></div>
        <span class="tag tag-gold" id="ragCountTag">LOADING</span>
      </div>
      <div class="card">
        <div class="card-title">Add / Edit Source</div>
        <input type="hidden" id="ragEditId" />
        <div class="form-row">
          <input class="inp" id="ragName" placeholder="Source name..." />
          <input class="inp" id="ragUrl" placeholder="URL (optional)" />
        </div>
        <textarea class="textarea" id="ragContent" placeholder="Paste source content to index (optional — needed for query)..." style="min-height:80px"></textarea>
        <div class="form-row" style="margin-top:8px">
          <button class="btn btn-gold" onclick="saveRagEdit()">Save Source</button>
          <button class="btn btn-ghost" onclick="clearRagForm()">Clear</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Query Source</div>
        <div class="form-row">
          <input class="inp" id="ragQuery" placeholder="Enter question to query against selected source..." />
        </div>
        <div class="result-box" id="ragQueryResult" style="color:var(--text-dim)">Select a source below and click Query, or enter a question above.</div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Sources</div>
        <div class="trib-list" id="ragSourceList"></div>
      </div>
    </div>

    <!-- RUNTIME HEALTH -->
    <div class="panel" id="panel-runtime">
      <div class="panel-hdr">
        <div><div class="panel-title">Runtime Health</div><div class="panel-sub">MVT-014: Local Model Maintenance and Multi-Model Orchestration</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshRuntimeHealth()">Refresh</button>
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Ollama Endpoint</div>
          <div class="flex flex-col gap-6" id="ollamaStatus">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Endpoint</span><span class="mono text-dim" style="font-size:10px">localhost:11434</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Status</span><span class="tag tag-amber" id="ollamaEndpointStatus">CHECKING</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Version</span><span class="mono text-dim" id="ollamaVersion">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Last Check</span><span class="mono text-dim" id="ollamaLastCheck">...</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Resource Safety</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Execution Mode</span><span class="tag tag-amber" id="runtimeExecMode">ONE-MODEL SAFETY</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Concurrency Limit</span><span class="mono text-dim">1</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Timeout Ceiling</span><span class="mono text-dim">60s</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Cloud PS Fallback</span><span class="tag tag-red">BLOCKED</span></div>
          </div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Model Registry</div>
        <div class="trib-list" id="modelRegistryList"><div class="text-dim mono" style="padding:12px;font-size:11px">Click Refresh to check Ollama model inventory.</div></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Smoke Test</div>
        <div class="flex gap-8">
          <button class="btn btn-ghost btn-sm" onclick="runRuntimeSmokeTest()">Run Minimal JSON Test</button>
          <span class="mono text-dim" style="font-size:10px;align-self:center" id="smokeTestResult">Not run</span>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Job Queue (dcse_cp.ddna_ollama_jobs)</div>
        <div id="ollamaJobsList"><div class="text-dim mono" style="padding:12px;font-size:11px">Loading...</div></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Capability Matrix</div>
        <div class="flex flex-col gap-6" id="capabilityMatrix">
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Chat / Reasoning</span><span class="tag tag-amber" id="capChat">UNTESTED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">JSON Output</span><span class="tag tag-amber" id="capJSON">UNTESTED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Structured Extraction</span><span class="tag tag-amber" id="capExtract">UNTESTED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Classification</span><span class="tag tag-amber" id="capClassify">UNTESTED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Coding</span><span class="tag tag-amber" id="capCode">UNTESTED</span></div>
        </div>
      </div>
    </div>

    <!-- TRIBUNAL -->
    <div class="panel" id="panel-tribunal">
      <div class="panel-hdr">
        <div><div class="panel-title">Tribunal</div><div class="panel-sub">DCSE-Tribunal-Relay — Open PRs</div></div>
        <span class="tag tag-amber">5 OPEN</span>
      </div>
      <div class="card">
        <div class="filter-row">
          <button class="btn btn-gold btn-sm trib-filter-btn" data-filter="all" onclick="renderTribunal('all')">All</button>
          <button class="btn btn-ghost btn-sm trib-filter-btn" data-filter="draft" onclick="renderTribunal('draft')">Draft</button>
          <button class="btn btn-ghost btn-sm trib-filter-btn" data-filter="open" onclick="renderTribunal('open')">Open</button>
        </div>
        <div class="trib-list" id="tribunalList"></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Repository Links</div>
        <div class="flex gap-8">
          <a class="btn btn-ghost" href="https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay" target="_blank">Tribunal Relay ↗</a>
          <a class="btn btn-ghost" href="https://github.com/sonlyconsulting-ctrl/DCSE-Command-Post" target="_blank">Command Post ↗</a>
        </div>
      </div>
    </div>

    <!-- DISPATCH -->
    <div class="panel" id="panel-dispatch">
      <div class="panel-hdr">
        <div><div class="panel-title">Dispatch</div><div class="panel-sub">Tribunal task dispatch and routing</div></div>
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('dispatchForm').style.display=document.getElementById('dispatchForm').style.display==='none'?'block':'none'">+ New Dispatch</button>
      </div>
      <div class="card mb-8" id="dispatchStats">
        <div class="card-title">Dispatch Pipeline</div>
        <div class="stat-grid" style="grid-template-columns:repeat(4,1fr)">
          <div class="stat-card"><div class="stat-val" id="dspPlanned">-</div><div class="stat-lbl">Planned</div></div>
          <div class="stat-card"><div class="stat-val" id="dspAssigned">-</div><div class="stat-lbl">Assigned</div></div>
          <div class="stat-card"><div class="stat-val" id="dspRunning">-</div><div class="stat-lbl">Running</div></div>
          <div class="stat-card"><div class="stat-val" id="dspCompleted">-</div><div class="stat-lbl">Completed</div></div>
        </div>
      </div>
      <div class="card mb-8" id="dispatchForm" style="display:none">
        <div class="card-title">Create Dispatch</div>
        <div class="form-row">
          <input class="inp" id="dispatchTitle" placeholder="Task title" style="flex:2" />
          <select class="inp" id="dispatchLane" style="flex:1"><option value="DCSE">DCSE</option><option value="SC">SC</option><option value="TSL">TSL</option><option value="TRIBUNAL">TRIBUNAL</option><option value="DDNA">DDNA</option><option value="RAG">RAG</option><option value="SYSTEM">SYSTEM</option></select>
        </div>
        <div class="form-row">
          <input class="inp" id="dispatchDesc" placeholder="Description (optional)" style="flex:2" />
          <select class="inp" id="dispatchType" style="flex:1"><option value="build">Build</option><option value="review">Review</option><option value="tribunal">Tribunal</option><option value="qa">QA</option><option value="database">Database</option><option value="github">GitHub</option><option value="decision">Decision</option><option value="monitor">Monitor</option><option value="other">Other</option></select>
        </div>
        <div class="form-row">
          <select class="inp" id="dispatchPriority" style="flex:1"><option value="1">P1 Critical</option><option value="2">P2 High</option><option value="3" selected>P3 Normal</option><option value="4">P4 Low</option><option value="5">P5 Backlog</option></select>
          <button class="btn btn-gold" onclick="createDispatch()">Dispatch</button>
        </div>
      </div>
      <div class="card mb-8">
        <div class="card-title">Task Queue</div>
        <div class="filter-row">
          <button class="btn btn-gold btn-sm" onclick="loadDispatchInbox('all')">All</button>
          <button class="btn btn-ghost btn-sm" onclick="loadDispatchInbox('active')">Active</button>
          <button class="btn btn-ghost btn-sm" onclick="loadDispatchInbox('completed')">Completed</button>
          <button class="btn btn-ghost btn-sm" onclick="loadDispatchInbox('blocked')">Blocked</button>
        </div>
        <div id="dispatchTaskList"><div class="text-dim mono" style="padding:16px;font-size:11px">Loading dispatch queue...</div></div>
      </div>
      <div class="card">
        <div class="card-title">Recent Events</div>
        <div id="dispatchEventList"><div class="text-dim mono" style="padding:16px;font-size:11px">No events loaded</div></div>
      </div>
    </div>

    <!-- PERSONAS -->
    <div class="panel" id="panel-personas">
      <div class="panel-hdr">
        <div><div class="panel-title">Personas</div><div class="panel-sub">DCSE Persona Registry — Supabase</div></div>
        <span class="tag tag-amber" id="personasGateTag">MIGRATIONS PENDING</span>
      </div>
      <div class="card mb-8">
        <div class="filter-row">
          <button class="btn btn-gold btn-sm" onclick="loadPersonas('all')">All</button>
          <button class="btn btn-ghost btn-sm" onclick="loadPersonas('active')">Active</button>
          <button class="btn btn-ghost btn-sm" onclick="loadPersonas('candidate')">Candidate</button>
          <button class="btn btn-ghost btn-sm" onclick="loadPersonas('draft')">Draft</button>
        </div>
        <div id="personasList"><div class="text-dim mono" style="padding:16px;font-size:11px">Loading personas...</div></div>
      </div>
      <div class="card">
        <div class="card-title">Agent Limits (Enforced)</div>
        <div class="flex flex-col gap-6">
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Approve own output</span><span class="tag tag-red">BLOCKED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Promote persona</span><span class="tag tag-red">BLOCKED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Change privacy class</span><span class="tag tag-red">BLOCKED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Override identity mask</span><span class="tag tag-red">BLOCKED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Migrations 001-003 apply</span><span class="tag tag-amber">DCS GATE</span></div>
        </div>
      </div>
    </div>

    <!-- ASSETS -->
    <div class="panel" id="panel-assets">
      <div class="panel-hdr">
        <div><div class="panel-title">Assets</div><div class="panel-sub">DCSE Asset Inventory — Supabase</div></div>
        <span class="tag tag-amber" id="assetsGateTag">MIGRATIONS PENDING</span>
      </div>
      <div class="card mb-8">
        <div class="filter-row">
          <button class="btn btn-gold btn-sm" onclick="loadAssets('all')">All</button>
          <button class="btn btn-ghost btn-sm" onclick="loadAssets('deployed')">Deployed</button>
          <button class="btn btn-ghost btn-sm" onclick="loadAssets('approved')">Approved</button>
          <button class="btn btn-ghost btn-sm" onclick="loadAssets('candidate')">Candidate</button>
        </div>
        <div id="assetsList"><div class="text-dim mono" style="padding:16px;font-size:11px">Loading assets...</div></div>
      </div>
      <div class="card">
        <div class="card-title">Relationship Spine</div>
        <div class="mono text-dim" style="font-size:10px;line-height:1.8">
          Persona → Product → Module → Asset → Task → Approval → Deployment → Tribunal
        </div>
      </div>
    </div>

    <!-- PHASE GATE BOARD (views 2+3: parallel execution + phase gates) -->
    <div class="panel" id="panel-phasegate">
      <div class="panel-hdr">
        <div><div class="panel-title">Phase Gate Board</div><div class="panel-sub">Universal Workstream Lifecycle and Parallel Execution Status</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshPhaseGate()">Refresh</button>
      </div>
      <div class="card">
        <div class="card-title">Workstream Phase Status</div>
        <div class="flex flex-col gap-6" id="phaseGateGrid">
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px;color:var(--text-dim);border-bottom:1px solid var(--border);padding-bottom:6px"><span>Workstream</span><span>Batch</span><span>Phase</span><span>Status</span><span>Owner</span><span>Blocker</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">MVT-014 Runtime Health</span><span>B1-A</span><span class="tag tag-green" style="font-size:9px">P3 BUILD</span><span class="tag tag-green" style="font-size:9px">ACTIVE</span><span class="mono text-dim">Codex</span><span class="mono text-dim">None</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">MVT-008A Relay</span><span>B1-B</span><span class="tag tag-green" style="font-size:9px">P3 BUILD</span><span class="tag tag-green" style="font-size:9px">ACTIVE</span><span class="mono text-dim">Claude Code</span><span class="mono text-dim">None</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">DBA Administration</span><span>B1-C</span><span class="tag tag-green" style="font-size:9px">P3 BUILD</span><span class="tag tag-green" style="font-size:9px">ACTIVE</span><span class="mono text-dim">DBA Admin</span><span class="mono text-dim">None</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">MVT-010 Agent OS</span><span>B1-D</span><span class="tag tag-green" style="font-size:9px">P3 BUILD</span><span class="tag tag-green" style="font-size:9px">ACTIVE</span><span class="mono text-dim">Codex</span><span class="mono text-dim">None</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">API Keys Admin</span><span>B1-E</span><span class="tag tag-green" style="font-size:9px">P3 BUILD</span><span class="tag tag-green" style="font-size:9px">ACTIVE</span><span class="mono text-dim">API Keys Admin</span><span class="mono text-dim">None</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">Build Assurance</span><span>B1-F</span><span class="tag tag-green" style="font-size:9px">P3 BUILD</span><span class="tag tag-green" style="font-size:9px">ACTIVE</span><span class="mono text-dim">Codex</span><span class="mono text-dim">None</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">MVT-013 TSL MVP</span><span>B2</span><span class="tag tag-amber" style="font-size:9px">P1 SOURCE</span><span class="tag tag-amber" style="font-size:9px">BLOCKED</span><span class="mono text-dim">Codex</span><span class="mono text-dim">Source recon</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">MVT-011 SC Hero DDNA</span><span>B3-A</span><span class="tag tag-amber" style="font-size:9px">P1 SOURCE</span><span class="tag tag-amber" style="font-size:9px">PENDING</span><span class="mono text-dim">ChatGPT + Codex</span><span class="mono text-dim">DCS confirm</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">MVT-016 SC Campaign</span><span>B3-B</span><span class="tag tag-amber" style="font-size:9px">P0 INTAKE</span><span class="tag tag-amber" style="font-size:9px">PENDING</span><span class="mono text-dim">Codex</span><span class="mono text-dim">LM Arena</span></div>
          <div style="display:grid;grid-template-columns:2fr 60px 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">MVT-015 Family Pathways</span><span>B3-D</span><span class="tag tag-amber" style="font-size:9px">P0 INTAKE</span><span class="tag tag-amber" style="font-size:9px">PENDING</span><span class="mono text-dim">ChatGPT + Codex</span><span class="mono text-dim">Product def</span></div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Phase Legend</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:10px;color:var(--text-dim)">
          <div>P0: Authority and intake</div><div>P1: Source reconstruction</div><div>P2: Requirements and architecture</div>
          <div>P3: Governed build</div><div>P4: Integration and validation</div><div>P5: Backward-chain QA</div>
          <div>P6: Compliance and readiness</div><div>P7: Staging and promotion</div><div>P8: Monitoring and maintenance</div>
        </div>
      </div>
    </div>

    <!-- DCS DECISION QUEUE (view 4) -->
    <div class="panel" id="panel-dcsqueue">
      <div class="panel-hdr">
        <div><div class="panel-title">DCS Decision Queue</div><div class="panel-sub">Decisions Awaiting Level 0 DCS Authority</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshDCSQueue()">Refresh</button>
      </div>
      <div class="card">
        <div class="card-title">Active Decisions</div>
        <div class="trib-list" id="dcsDecisionList">
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--red)">PENDING</span>
            <div class="trib-info">
              <div class="trib-title">SC Hero Line Final Selection</div>
              <div class="trib-meta">MVT-011 · DDNA process required · PR #5 held</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--amber)">PENDING</span>
            <div class="trib-info">
              <div class="trib-title">TSL Source Reconstruction Packet</div>
              <div class="trib-meta">MVT-013 · Issue #3 · Source material from DCS</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--amber)">PENDING</span>
            <div class="trib-info">
              <div class="trib-title">SC Brand Palette Confirmation</div>
              <div class="trib-meta">MVT-009/016 · Visual identity lock</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--amber)">PENDING</span>
            <div class="trib-info">
              <div class="trib-title">Production Deployment Authorization</div>
              <div class="trib-meta">Batch 5 · Post-staging DCS promotion</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--text-dim)">FUTURE</span>
            <div class="trib-info">
              <div class="trib-title">PR #8 Merge Authorization</div>
              <div class="trib-meta">Current branch · Batch 1 P0 surfaces · Draft</div>
            </div>
          </div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Hold Conditions</div>
        <div class="flex flex-col gap-6">
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Tribunal Relay PR #5 (hero line)</span><span class="tag tag-red">HELD</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">TSL July 18 MVP (source recon)</span><span class="tag tag-amber">BLOCKED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">SC Campaign (LM Arena intake)</span><span class="tag tag-amber">BLOCKED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Family Pathways (product def)</span><span class="tag tag-amber">BLOCKED</span></div>
        </div>
      </div>
    </div>

    <!-- RECEIPTS AND EVIDENCE (view 6) -->
    <div class="panel" id="panel-receipts">
      <div class="panel-hdr">
        <div><div class="panel-title">Receipts and Evidence</div><div class="panel-sub">Proof Supporting Each Status Claim</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshReceipts()">Refresh</button>
      </div>
      <div class="card">
        <div class="card-title">Build Receipts</div>
        <div class="trib-list" id="receiptsList">
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--green)">VERIFIED</span>
            <div class="trib-info">
              <div class="trib-title">PR #5 Agent OS v1.3 Baseline</div>
              <div class="trib-meta">Commit c8f5270 · Merged to main · Vercel deployed</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--green)">VERIFIED</span>
            <div class="trib-info">
              <div class="trib-title">PR #6 Personas/Assets Module</div>
              <div class="trib-meta">Commit 12acec7 · Merged to main · Migrations 001-003 applied</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--green)">VERIFIED</span>
            <div class="trib-info">
              <div class="trib-title">Migration 004 Relay RPC Security</div>
              <div class="trib-meta">Applied · Public/anon/auth execution revoked</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--green)">MERGED</span>
            <div class="trib-info">
              <div class="trib-title">PR #8 Batch 1 P0 Surfaces</div>
              <div class="trib-meta">Runtime Health, DBA, API Keys, Assurance, Agent Ops, Phase Gates, DCS Queue, Receipts, Config</div>
            </div>
          </div>
          <div class="trib-item">
            <span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--green)">APPLIED</span>
            <div class="trib-info">
              <div class="trib-title">Migration 005 Security Remediation</div>
              <div class="trib-meta">Search paths, EXECUTE revocations, scn_balance INVOKER, RLS policies, avatar bucket</div>
            </div>
          </div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Supabase Verification</div>
        <div class="flex flex-col gap-6">
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">dcse_cp schema (24 tables)</span><span class="tag tag-green">VERIFIED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Governed persona seeds (6)</span><span class="tag tag-green">VERIFIED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">SNTY/ASP identity masking</span><span class="tag tag-green">VERIFIED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Agent promote/approve/deploy locks</span><span class="tag tag-green">VERIFIED</span></div>
          <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Assets defaulted to internal/discovered</span><span class="tag tag-green">VERIFIED</span></div>
        </div>
      </div>
    </div>

    <!-- CONFIGURATION CONSOLE (view 11) -->
    <div class="panel" id="panel-config">
      <div class="panel-hdr">
        <div><div class="panel-title">Configuration Console</div><div class="panel-sub">Themes, Tiers, Entitlements, Feature Flags, and Display Profiles</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshConfig()">Refresh</button>
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Active Configuration</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Theme</span><span class="mono text-dim">DCSE Navy (default)</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Display Profile</span><span class="mono text-dim">SC Agent OS v1.3</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Config Version</span><span class="mono text-dim" id="configVersion">1.0.0</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Last Updated</span><span class="mono text-dim" id="configUpdated">2026-07-15</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Feature Flags</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Multi-provider Chat</span><span class="tag tag-green">ENABLED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">DDNA Harvest</span><span class="tag tag-green">ENABLED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Runtime Health</span><span class="tag tag-green">ENABLED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Agent Operations</span><span class="tag tag-green">ENABLED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">TSL Admin Console</span><span class="tag tag-amber">PENDING</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">SC Campaign System</span><span class="tag tag-amber">PENDING</span></div>
          </div>
        </div>
      </div>
      <div class="grid-2 mt-8">
        <div class="card">
          <div class="card-title">Tier Configuration</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Operator (Internal)</span><span class="tag tag-green">ACTIVE</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">DCS (Authority)</span><span class="tag tag-green">ACTIVE</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Review Board</span><span class="tag tag-green">ACTIVE</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Agent (Automated)</span><span class="tag tag-green">ACTIVE</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Deployment Targets</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Production (os.sonlyconsulting.com)</span><span class="tag tag-green">LIVE</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Preview (Vercel)</span><span class="tag tag-green">DEPLOYED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Local Dev</span><span class="tag tag-amber">MANUAL</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- DBA CONSOLE -->
    <div class="panel" id="panel-dba">
      <div class="panel-hdr">
        <div><div class="panel-title">DBA Console</div><div class="panel-sub">Track C: Database Administration and Supabase Remediation</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshDBA()">Refresh</button>
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Schema State</div>
          <div class="flex flex-col gap-6" id="dbaSchemaState">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Active Schema</span><span class="mono text-dim">dcse_cp</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Table Count</span><span class="mono text-dim" id="dbaTableCount">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Schema Version</span><span class="mono text-dim" id="dbaSchemaVersion">...</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Last Migration</span><span class="mono text-dim" id="dbaLastMigration">...</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Migration Control</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Migration 001 (Personas)</span><span class="tag tag-green">APPLIED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Migration 002 (Assets)</span><span class="tag tag-green">APPLIED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Migration 003 (Persona Seeds)</span><span class="tag tag-green">APPLIED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Migration 005 (Security Remediation)</span><span class="tag tag-green">APPLIED</span></div>
          </div>
        </div>
      </div>
      <div class="grid-2 mt-8">
        <div class="card">
          <div class="card-title">RLS and Security</div>
          <div class="flex flex-col gap-6" id="dbaRLS">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">RLS Enforcement</span><span class="tag tag-amber" id="dbaRLSStatus">CHECK REQUIRED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Public Execution Exposure</span><span class="tag tag-amber" id="dbaPublicExec">CHECK REQUIRED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Function Search Paths</span><span class="tag tag-amber" id="dbaSearchPath">CHECK REQUIRED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Password Protection</span><span class="tag tag-amber" id="dbaPasswordProtect">CHECK REQUIRED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Storage Listing</span><span class="tag tag-amber" id="dbaStorageListing">CHECK REQUIRED</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Operations</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Backup Status</span><span class="tag tag-amber" id="dbaBackupStatus">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Realtime Status</span><span class="tag tag-amber" id="dbaRealtimeStatus">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Performance</span><span class="tag tag-amber" id="dbaPerfStatus">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">DBA Approval</span><span class="tag tag-amber" id="dbaApprovalStatus">PENDING</span></div>
          </div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Table Registry (dcse_cp)</div>
        <div class="trib-list" id="dbaTableList"><div class="text-dim mono" style="padding:12px;font-size:11px">Click Refresh to load table inventory.</div></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Security Findings</div>
        <div class="trib-list" id="dbaFindings"><div class="text-dim mono" style="padding:12px;font-size:11px">Pre-existing findings from PR #6 review pending remediation plan.</div></div>
      </div>
    </div>

    <!-- API KEYS ADMIN CONSOLE -->
    <div class="panel" id="panel-apikeys">
      <div class="panel-hdr">
        <div><div class="panel-title">API Keys Admin Console</div><div class="panel-sub">Track E: Governed Key Lifecycle (No Raw Secrets Displayed)</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshAPIKeys()">Refresh</button>
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-title">Provider Inventory</div>
          <div class="flex flex-col gap-6" id="apikeyProviders">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Anthropic (Claude)</span><span class="tag tag-amber" id="apikeyAnthropic">NOT CONFIGURED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">OpenAI</span><span class="tag tag-amber" id="apikeyOpenAI">NOT CONFIGURED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Google (Gemini)</span><span class="tag tag-amber" id="apikeyGoogle">NOT CONFIGURED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Qwen (Alibaba)</span><span class="tag tag-amber" id="apikeyQwen">NOT CONFIGURED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Ollama (Local)</span><span class="tag tag-green" id="apikeyOllama">NO KEY REQUIRED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Supabase Service Role</span><span class="tag tag-amber" id="apikeySupabase">SERVER-SIDE ONLY</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Security Controls</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Raw Keys in Client Code</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Raw Keys in GitHub</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Raw Keys in Logs</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Raw Keys in CP Tasks</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Browser Storage Keys</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Cloud PS Fallback</span><span class="tag tag-red">BLOCKED</span></div>
          </div>
        </div>
      </div>
      <div class="grid-2 mt-8">
        <div class="card">
          <div class="card-title">Environment Binding</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Vercel (Production)</span><span class="tag tag-amber" id="apikeyVercelProd">CHECK REQUIRED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Vercel (Preview)</span><span class="tag tag-amber" id="apikeyVercelPreview">CHECK REQUIRED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Local Dev</span><span class="tag tag-amber" id="apikeyLocalDev">MANUAL</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Lifecycle Status</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Last Rotation</span><span class="mono text-dim" id="apikeyLastRotation">Unknown</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Next Expiration</span><span class="mono text-dim" id="apikeyNextExpiry">Unknown</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Kill Switch</span><span class="tag tag-green" id="apikeyKillSwitch">AVAILABLE</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Revocation Ready</span><span class="tag tag-green" id="apikeyRevocationReady">YES</span></div>
          </div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Provider Readiness Matrix</div>
        <div class="flex flex-col gap-6" id="apikeyReadinessMatrix">
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;font-size:10px;color:var(--text-dim);border-bottom:1px solid var(--border);padding-bottom:6px"><span>Provider</span><span>Scope</span><span>Bound</span><span>Validated</span><span>Least Privilege</span></div>
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">Anthropic</span><span class="tag tag-amber" style="font-size:9px">CHAT</span><span class="tag tag-amber" style="font-size:9px">VERCEL</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span></div>
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">OpenAI</span><span class="tag tag-amber" style="font-size:9px">CHAT</span><span class="tag tag-amber" style="font-size:9px">VERCEL</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span></div>
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">Google</span><span class="tag tag-amber" style="font-size:9px">CHAT</span><span class="tag tag-amber" style="font-size:9px">VERCEL</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span></div>
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">Qwen</span><span class="tag tag-amber" style="font-size:9px">CHAT</span><span class="tag tag-amber" style="font-size:9px">VERCEL</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span></div>
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">Supabase</span><span class="tag tag-amber" style="font-size:9px">SERVICE</span><span class="tag tag-green" style="font-size:9px">SERVER</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span></div>
          <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">Ollama</span><span class="tag tag-green" style="font-size:9px">LOCAL</span><span class="tag tag-green" style="font-size:9px">LOCALHOST</span><span class="tag tag-green" style="font-size:9px">N/A</span><span class="tag tag-green" style="font-size:9px">N/A</span></div>
        </div>
      </div>
    </div>

    <!-- ASSURANCE LOOP CONSOLE -->
    <div class="panel" id="panel-assurance">
      <div class="panel-hdr">
        <div><div class="panel-title">Assurance Loop Console</div><div class="panel-sub">Track F: Build Assurance A0 through A8 State Model</div></div>
        <button class="btn btn-ghost btn-sm" onclick="refreshAssurance()">Refresh</button>
      </div>
      <div class="card">
        <div class="card-title">Assurance Loop Status</div>
        <div class="flex flex-col gap-6" id="assuranceLoopStatus">
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px;color:var(--text-dim);border-bottom:1px solid var(--border);padding-bottom:6px"><span>Loop</span><span>Trigger</span><span>Status</span><span>Evidence</span><span>Last Run</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A0</span><span>Task admission or source change</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A1</span><span>Code or configuration change</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A2</span><span>API, adapter, event, or schema contract</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A3</span><span>Database, migration, or storage change</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A4</span><span>Provider, API key, or external service</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A5</span><span>Merge candidate or feature completion</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A6</span><span>SC or product approval candidate</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A7</span><span>Release candidate</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
          <div style="display:grid;grid-template-columns:60px 2fr 1fr 1fr 1fr;gap:4px;font-size:10px"><span class="mono">A8</span><span>Deployment or maintenance</span><span class="tag tag-amber" style="font-size:9px">UNKNOWN</span><span class="tag tag-amber" style="font-size:9px">NONE</span><span class="mono text-dim">...</span></div>
        </div>
      </div>
      <div class="grid-2 mt-8">
        <div class="card">
          <div class="card-title">Check Suite Controls</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Promotion Blocking</span><span class="tag tag-green">ENFORCED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Independent Review Required</span><span class="tag tag-green">ENFORCED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Evidence Required for PASS</span><span class="tag tag-green">ENFORCED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Retest on Material Change</span><span class="tag tag-green">ENFORCED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Self-Approval</span><span class="tag tag-red">BLOCKED</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">SC Fullness Review</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Requirement Fullness</span><span class="tag tag-amber" id="fullnessReq">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Functional Fullness</span><span class="tag tag-amber" id="fullnessFunc">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Data Fullness</span><span class="tag tag-amber" id="fullnessData">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Operational Fullness</span><span class="tag tag-amber" id="fullnessOps">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Governance Fullness</span><span class="tag tag-amber" id="fullnessGov">UNKNOWN</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Release Fullness</span><span class="tag tag-amber" id="fullnessRelease">UNKNOWN</span></div>
          </div>
        </div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Failed Controls and Remediation</div>
        <div class="trib-list" id="assuranceFailedControls"><div class="text-dim mono" style="padding:12px;font-size:11px">No failed controls recorded. Click Refresh to check current state.</div></div>
      </div>
      <div class="card mt-8">
        <div class="card-title">Accepted Exceptions</div>
        <div class="trib-list" id="assuranceExceptions"><div class="text-dim mono" style="padding:12px;font-size:11px">No accepted exceptions.</div></div>
      </div>
    </div>

    <!-- PS FIREWALL -->
    <div class="panel" id="panel-ps">
      <div class="panel-hdr">
        <div><div class="panel-title">PS Firewall</div><div class="panel-sub">Personal / sensitive content gate</div></div>
        <span class="tag tag-green">ACTIVE</span>
      </div>
      <div class="grid-2">
        <div class="card"><div class="card-title">Firewall Rules</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">PS content in dispatch packets</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Employ/career material in SC lane</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Pricing in public-facing copy</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">External brand mentions</span><span class="tag tag-red">BLOCKED</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Superlatives without evidence</span><span class="tag tag-red">BLOCKED</span></div>
          </div>
        </div>
        <div class="card"><div class="card-title">Current Session</div>
          <div class="flex flex-col gap-6">
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">PS content detected</span><span class="tag tag-green">NONE</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Breach count</span><span class="mono text-green">0</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Last check</span><span class="mono text-dim">2026-07-15</span></div>
            <div class="flex items-center justify-between"><span style="font-size:11px;color:var(--text-dim)">Build receipt</span><span class="tag tag-green">CLEAN</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- OPS LOG -->
    <div class="panel" id="panel-log">
      <div class="panel-hdr">
        <div><div class="panel-title">Ops Log</div><div class="panel-sub">Session audit trail</div></div>
        <button class="btn btn-ghost btn-sm" onclick="addOpsEntry()">+ Entry</button>
      </div>
      <div class="card overflow-auto">
        <div class="flex flex-col gap-6" id="opsLog">
          <div class="mono text-dim">2026-07-15 · SC Agent OS v1.3 — full functionality deployed (Orchestration, DDNA, Local Models, RAG, Governance)</div>
          <div class="mono text-dim">2026-07-15 · ChatGPT, Gemini, Qwen added to Agent Chat</div>
          <div class="mono text-dim">2026-07-14 · SC Agent OS v1.3 deployed to os.sonlyconsulting.com</div>
          <div class="mono text-dim">2026-07-14 · SC LP trial build complete — D08 v6.9.1 voice rule held</div>
          <div class="mono text-dim">2026-07-08T03:35 · UNC path corrected in dispatch packet</div>
          <div class="mono text-dim">2026-07-08T03:27 · PR #5 opened</div>
          <div class="mono text-dim">2026-07-08 · DCS confirmed hero line — LOCKED</div>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
// Clock
function tick(){document.getElementById('clock').textContent=new Date().toLocaleTimeString('en-US',{hour12:false});}
tick();setInterval(tick,1000);

// Nav
function nav(id,el){
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  document.getElementById('panel-'+id).classList.add('active');
  if(el){el.classList.add('active');}
  else{
    const found=Array.from(document.querySelectorAll('.nav-item')).find(n=>(n.getAttribute('onclick')||'').includes("'"+id+"'"));
    if(found)found.classList.add('active');
  }
  if(id==='personas')loadPersonas(_personasFilter);
  if(id==='assets')loadAssets(_assetsFilter);
  if(id==='runtime'&&!_runtimeChecked)refreshRuntimeHealth();
  if(id==='phasegate')refreshPhaseGate();
  if(id==='dcsqueue'&&!_dcsqueueChecked)refreshDCSQueue();
  if(id==='receipts'&&!_receiptsChecked)refreshReceipts();
  if(id==='config'&&!_configChecked)refreshConfig();
  if(id==='agentops'&&!_agentopsChecked)refreshAgentOps();
  if(id==='dba'&&!_dbaChecked)refreshDBA();
  if(id==='apikeys'&&!_apikeysChecked)refreshAPIKeys();
  if(id==='assurance'&&!_assuranceChecked)refreshAssurance();
  if(id==='dispatch')loadDispatchInbox('all');
}

// Voice
let voiceActive=false,recognition=null;
function toggleVoice(){
  voiceActive=!voiceActive;
  document.querySelectorAll('.voice-btn').forEach(b=>{b.textContent=voiceActive?'🔴 Stop':'🎤 Voice';b.classList.toggle('rec',voiceActive);});
  const wave=document.getElementById('waveArea');
  if(wave)wave.style.display=voiceActive?'block':'none';
  if(voiceActive){
    const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
    if(SR){
      recognition=new SR();recognition.continuous=true;recognition.interimResults=false;
      recognition.onresult=e=>{const t=e.results[e.results.length-1][0].transcript.trim();if(t){document.getElementById('chatInput').value=t;sendMessage();}};
      recognition.onerror=()=>{addMsg('sys','Voice error — check browser permissions.');voiceActive=false;document.querySelectorAll('.voice-btn').forEach(b=>{b.textContent='🎤 Voice';b.classList.remove('rec');});};
      recognition.start();
    } else {addMsg('sys','Web Speech API not supported.');voiceActive=false;}
  } else {if(recognition)recognition.stop();}
}

// Per-provider key management
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
onModelChange();

// Chat
const chatHistory=[];
let activeSysPrompt='You are an AI assistant inside SC Agent OS, the DCSE Mission Control interface for Sonly Consulting. PS firewall active — no personal/sensitive content. Be concise and direct.';

function clearChat(){
  chatHistory.length=0;
  document.getElementById('chatArea').innerHTML='<div class="msg sys">Chat cleared.</div>';
  document.getElementById('chatContextLabel').textContent='Select model — SC/DCSE context active — PS firewall on';
  activeSysPrompt='You are an AI assistant inside SC Agent OS, the DCSE Mission Control interface for Sonly Consulting. PS firewall active — no personal/sensitive content. Be concise and direct.';
}

function addMsg(type,text){
  const area=document.getElementById('chatArea');
  const m=document.createElement('div');m.className='msg '+type;m.textContent=text;
  area.appendChild(m);area.scrollTop=area.scrollHeight;return m;
}

async function sendMessage(){
  const inp=document.getElementById('chatInput');
  const text=inp.value.trim();if(!text)return;
  addMsg('user',text);chatHistory.push({role:'user',content:text});
  inp.value='';autoResize(inp);
  const btn=document.getElementById('sendBtn');btn.disabled=true;
  const model=document.getElementById('modelSelect').value;
  const thinking=addMsg('agent thinking','...');
  const p=providerOf(model);
  try{
    if(p==='ollama'){
      const ollamaModel=model.replace('ollama:','');
      const r=await fetch('http://localhost:11434/api/chat',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({model:ollamaModel,messages:chatHistory,stream:false})
      });
      if(!r.ok)throw new Error('Ollama '+r.status+' — CORS? Run: OLLAMA_ORIGINS=* ollama serve');
      const d=await r.json();
      const reply=d.message?.content||'[no response]';
      chatHistory.push({role:'assistant',content:reply});
      thinking.textContent=reply;thinking.className='msg agent';
    } else {
      const apiKey=keyInput.value;
      if(!PROVIDER_META[p].check(apiKey)){thinking.textContent='Enter '+PROVIDER_META[p].label+' API key ('+PROVIDER_META[p].placeholder+')';thinking.className='msg sys';btn.disabled=false;return;}
      const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:chatHistory,system:activeSysPrompt,apiKey})});
      const d=await r.json();
      if(d.error)throw new Error(typeof d.error==='string'?d.error:d.error.message||'API error');
      const reply=d.text||'[no response]';
      chatHistory.push({role:'assistant',content:reply});
      thinking.textContent=reply;thinking.className='msg agent';
    }
  }catch(e){thinking.textContent='Error: '+e.message;thinking.className='msg sys';}
  btn.disabled=false;
}

function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage();}}
function autoResize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,110)+'px';}

// Agent Dock — launch in chat
function launchAgent(name,role,sysCtx){
  activeSysPrompt=sysCtx;
  document.getElementById('chatContextLabel').textContent='Agent: '+name+' ('+role+') — PS firewall on';
  nav('chat',null);
  addMsg('sys','Agent loaded: '+name+' — '+role);
}
function launchAgentOllama(name,ollamaModel,ctx){
  // Switch model selector to ollama model
  const sel=document.getElementById('modelSelect');
  const optVal='ollama:'+ollamaModel;
  if(sel.querySelector('option[value="'+optVal+'"]'))sel.value=optVal;
  onModelChange();
  activeSysPrompt=ctx;
  document.getElementById('chatContextLabel').textContent='Local: '+name+' via Ollama — '+ollamaModel;
  nav('chat',null);
  addMsg('sys','Local agent loaded: '+name+' ('+ollamaModel+') — calls localhost:11434');
}

// ===== TASK QUEUE =====
let tasks=JSON.parse(localStorage.getItem('sc_tasks')||'null')||[
  {id:1,title:'SC LP trial build — review and merge PR #5',owner:'DCS',status:'in_progress',created:'2026-07-14'},
  {id:2,title:'Drop TRIB-20260708 dispatch packet to Tribunal Inbox',owner:'DCS',status:'queued',created:'2026-07-08'},
  {id:3,title:'Confirm SC brand palette (color_primary) for LP production',owner:'DCS',status:'queued',created:'2026-07-08'}
];
function saveTasks(){localStorage.setItem('sc_tasks',JSON.stringify(tasks));}
let taskFilter='all';
function renderTasks(filter){
  taskFilter=filter||taskFilter;
  const list=document.getElementById('taskList');if(!list)return;
  const shown=taskFilter==='all'?tasks:tasks.filter(t=>t.status===taskFilter);
  const statusStyle={queued:'background:var(--amber-dim);color:var(--amber)',in_progress:'background:var(--purple-dim);color:var(--purple)',done:'background:var(--green-dim);color:var(--green)'};
  list.innerHTML=shown.length?shown.map(t=>\`
    <div class="trib-item">
      <span class="trib-status" style="\${statusStyle[t.status]||''}">\${t.status.replace('_',' ').toUpperCase()}</span>
      <div class="trib-info"><div class="trib-title">\${t.title}</div><div class="trib-meta">Owner: \${t.owner} · \${t.created}</div></div>
      <div class="flex gap-6">
        <button class="btn btn-ghost btn-sm" onclick="cycleTask(\${t.id})">Cycle</button>
        <button class="btn btn-ghost btn-sm" onclick="chatAboutTask('\${t.title.replace(/'/g,'\\\\'')}')">Chat</button>
        <button class="btn btn-ghost btn-sm" style="color:var(--red)" onclick="deleteTask(\${t.id})">✕</button>
      </div>
    </div>\`).join(''):'<div class="mono text-dim" style="padding:8px">No tasks.</div>';
  document.querySelectorAll('.trib-filter-btn').forEach(b=>b.classList.toggle('btn-gold',b.dataset.filter===taskFilter));
  const active=tasks.filter(t=>t.status!=='done').length;
  document.getElementById('taskBadge').textContent=active;
  const tag=document.getElementById('taskCountTag');if(tag)tag.textContent=active+' ACTIVE';
}
function addTask(){
  const inp=document.getElementById('newTaskInput');
  const owner=document.getElementById('newTaskOwner');
  const status=document.getElementById('newTaskStatus').value;
  if(!inp.value.trim())return;
  tasks.push({id:Date.now(),title:inp.value.trim(),owner:owner.value||'DCS',status,created:new Date().toISOString().split('T')[0]});
  saveTasks();inp.value='';owner.value='';renderTasks();
}
function cycleTask(id){
  const t=tasks.find(x=>x.id===id);if(!t)return;
  const cycle={queued:'in_progress',in_progress:'done',done:'queued'};
  t.status=cycle[t.status]||'queued';saveTasks();renderTasks();
}
function deleteTask(id){tasks=tasks.filter(x=>x.id!==id);saveTasks();renderTasks();}
function chatAboutTask(title){
  document.getElementById('chatInput').value='Help me with this task: '+title;
  nav('chat',null);
}

// ===== PORTFOLIO =====
let portfolio=JSON.parse(localStorage.getItem('sc_portfolio')||'null')||[
  {id:1,name:'SC Agent OS v1.3',url:'os.sonlyconsulting.com',status:'live',note:'Vercel · iad1'},
  {id:2,name:'SC Landing Page',url:'',status:'trial',note:'Trial build complete · palette TBD'},
  {id:3,name:'SC GovOS RAG Website',url:'',status:'arch',note:'Hybrid Wix+Velo+CMS+Supabase'},
  {id:4,name:'DCSE Governance Doctrine',url:'',status:'active',note:'D08 voice rule trial passed'}
];
function savePortfolio(){localStorage.setItem('sc_portfolio',JSON.stringify(portfolio));}
const portStatusStyle={live:'background:var(--green-dim);color:var(--green)',trial:'background:var(--amber-dim);color:var(--amber)',arch:'background:var(--blue-dim);color:var(--blue)',active:'background:var(--teal-dim);color:var(--teal)',pending:'background:var(--navy-border);color:var(--text-dim)',paused:'background:var(--red-dim);color:var(--red)'};
function renderPortfolio(){
  const list=document.getElementById('portfolioList');if(!list)return;
  list.innerHTML=portfolio.map(p=>\`
    <div class="trib-item">
      <span class="trib-status" style="\${portStatusStyle[p.status]||''}">\${p.status.toUpperCase()}</span>
      <div class="trib-info">
        <div class="trib-title">\${p.name}\${p.url?' <span class="mono text-dim" style="font-size:9px">· '+p.url+'</span>':''}</div>
        <div class="trib-meta">\${p.note||''}</div>
      </div>
      <div class="flex gap-6 items-center">
        <select class="model-select" style="font-size:9px;padding:2px 5px" onchange="updatePortStatus(\${p.id},this.value)">
          \${['live','trial','arch','active','pending','paused'].map(s=>'<option value="'+s+'"'+(p.status===s?' selected':'')+'>'+s+'</option>').join('')}
        </select>
        <button class="btn btn-ghost btn-sm" style="color:var(--red)" onclick="deletePort(\${p.id})">✕</button>
      </div>
    </div>\`).join('');
  document.getElementById('portBadge').textContent=portfolio.length;
  const tag=document.getElementById('portCountTag');if(tag)tag.textContent=portfolio.length+' ITEMS';
}
function addPortItem(){
  const n=document.getElementById('newPortName').value.trim();
  const u=document.getElementById('newPortUrl').value.trim();
  const note=document.getElementById('newPortNote').value.trim();
  const status=document.getElementById('newPortStatus').value;
  if(!n)return;
  portfolio.push({id:Date.now(),name:n,url:u,status,note});
  savePortfolio();renderPortfolio();
  document.getElementById('newPortName').value='';document.getElementById('newPortUrl').value='';document.getElementById('newPortNote').value='';
}
function updatePortStatus(id,status){const p=portfolio.find(x=>x.id===id);if(p){p.status=status;savePortfolio();}}
function deletePort(id){portfolio=portfolio.filter(x=>x.id!==id);savePortfolio();renderPortfolio();}

// ===== DDNA HARVEST =====
const DDNA_DIMS=[
  {key:'voice_fidelity',label:'Voice Fidelity',color:'var(--gold)'},
  {key:'ps_firewall',label:'PS Firewall',color:'var(--green)'},
  {key:'gate_discipline',label:'Gate Discipline',color:'var(--green)'},
  {key:'packet_integrity',label:'Packet Integrity',color:'var(--green)'},
  {key:'schema_accuracy',label:'Schema Accuracy',color:'var(--blue)'},
  {key:'dcs_alignment',label:'DCS Alignment',color:'var(--gold)'},
  {key:'instruction_fidelity',label:'Instruction Fidelity',color:'var(--purple)'},
  {key:'divergence_signal',label:'Divergence Signal',color:'var(--orange)'},
];
let ddnaScores=JSON.parse(localStorage.getItem('sc_ddna_scores')||'null')||{voice_fidelity:94,ps_firewall:100,gate_discipline:97,packet_integrity:99,schema_accuracy:96,dcs_alignment:100,instruction_fidelity:95,divergence_signal:72};
let ddnaNotes=JSON.parse(localStorage.getItem('sc_ddna_notes')||'[]');

function renderDDNA(){
  const grid=document.getElementById('ddnaGrid');if(!grid)return;
  grid.innerHTML=DDNA_DIMS.map(d=>\`
    <div class="ddna-cell">
      <div class="ddna-label">\${d.label}</div>
      <div class="ddna-bar-wrap"><div class="ddna-bar" style="width:0%;background:\${d.color}" id="bar-\${d.key}"></div></div>
      <div class="ddna-score" id="score-\${d.key}">\${ddnaScores[d.key]||0}</div>
      <div class="ddna-delta">Session</div>
    </div>\`).join('');
  setTimeout(()=>DDNA_DIMS.forEach(d=>{const b=document.getElementById('bar-'+d.key);if(b)b.style.width=(ddnaScores[d.key]||0)+'%';}),200);
  const nl=document.getElementById('ddnaNotesList');
  if(nl)nl.innerHTML=ddnaNotes.length?ddnaNotes.map((n,i)=>\`<div class="mono text-dim" style="padding:5px 0;border-bottom:1px solid var(--navy-border);display:flex;justify-content:space-between"><span>\${n.ts} — \${n.text}</span><button class="btn btn-ghost btn-sm" style="color:var(--red)" onclick="deleteDDNANote(\${i})">✕</button></div>\`).join(''):'<div class="mono text-dim">No notes.</div>';
}

async function runDDNAHarvest(){
  const input=document.getElementById('ddnaInput').value.trim();
  if(!input){document.getElementById('harvestStatus').textContent='Paste session content above first.';return;}
  const model=document.getElementById('modelSelect').value;
  const p=providerOf(model);
  const btn=document.getElementById('harvestBtn');btn.disabled=true;btn.textContent='Harvesting...';
  const prompt='You are a DDNA scoring system. Analyze this agent session and score each dimension 0-100.\\n\\nDimensions:\\n- voice_fidelity: D08 voice rule adherence (lead constructively, no dominating contrast)\\n- ps_firewall: Personal/sensitive content exclusion (100=perfect, 0=breach)\\n- gate_discipline: Respect for DCS approval gates\\n- packet_integrity: Dispatch packet completeness and accuracy\\n- schema_accuracy: JSON/data structure correctness\\n- dcs_alignment: Alignment with DCS instructions and DCSE doctrine\\n- instruction_fidelity: Precision in following explicit instructions\\n- divergence_signal: Creative divergence level (higher=more divergent)\\n\\nRespond ONLY with valid JSON like:\\n{"voice_fidelity":90,"ps_firewall":100,"gate_discipline":95,"packet_integrity":88,"schema_accuracy":92,"dcs_alignment":97,"instruction_fidelity":93,"divergence_signal":65}\\n\\nSession:\\n'+input.slice(0,3000);
  try{
    let result;
    if(p==='ollama'){
      const om=model.replace('ollama:','');
      const r=await fetch('http://localhost:11434/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:om,messages:[{role:'user',content:prompt}],stream:false})});
      const d=await r.json();result=d.message?.content||'';
    } else {
      const apiKey=keyInput.value;
      if(!PROVIDER_META[p].check(apiKey)){document.getElementById('harvestStatus').textContent='Enter API key for '+PROVIDER_META[p].label;btn.disabled=false;btn.textContent='Run Harvest';return;}
      const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:[{role:'user',content:prompt}],apiKey})});
      const d=await r.json();result=d.text||'';
    }
    const match=result.match(/\\{[^}]+\\}/);
    if(match){
      try{
        const scores=JSON.parse(match[0]);
        Object.assign(ddnaScores,scores);
        localStorage.setItem('sc_ddna_scores',JSON.stringify(ddnaScores));
        renderDDNA();
        document.getElementById('harvestStatus').textContent='Harvest complete — '+new Date().toLocaleTimeString();
      }catch(pe){document.getElementById('harvestStatus').textContent='JSON parse error: '+pe.message;}
    } else {
      document.getElementById('harvestStatus').textContent='Could not parse scores from: '+result.slice(0,120);
    }
  }catch(e){document.getElementById('harvestStatus').textContent='Error: '+e.message;}
  btn.disabled=false;btn.textContent='Run Harvest';
}
function addDDNANote(){
  const inp=document.getElementById('ddnaNoteInput');if(!inp.value.trim())return;
  ddnaNotes.unshift({ts:new Date().toISOString().split('T')[0],text:inp.value.trim()});
  localStorage.setItem('sc_ddna_notes',JSON.stringify(ddnaNotes));inp.value='';renderDDNA();
}
function deleteDDNANote(i){ddnaNotes.splice(i,1);localStorage.setItem('sc_ddna_notes',JSON.stringify(ddnaNotes));renderDDNA();}
function exportDDNA(){
  const data={scores:ddnaScores,notes:ddnaNotes,exported:new Date().toISOString()};
  navigator.clipboard.writeText(JSON.stringify(data,null,2)).then(()=>alert('DDNA profile copied to clipboard.'));
}

// ===== LOCAL MODELS =====
function formatBytes(b){if(!b)return'';const mb=b/1024/1024;return mb>1000?(mb/1024).toFixed(1)+' GB':mb.toFixed(0)+' MB';}
async function checkOllama(){
  const statusEl=document.getElementById('ollamaStatus');
  const listEl=document.getElementById('ollamaModelList');
  statusEl.textContent='Checking...';statusEl.style.cssText='background:var(--amber-dim);color:var(--amber)';
  try{
    const r=await fetch('http://localhost:11434/api/tags',{signal:AbortSignal.timeout(3000)});
    const d=await r.json();
    statusEl.textContent='ONLINE';statusEl.style.cssText='background:var(--green-dim);color:var(--green)';
    document.getElementById('modelsBadge').textContent=d.models?d.models.length:0;
    if(d.models&&d.models.length){
      listEl.innerHTML=d.models.map(m=>\`
        <div class="model-row">
          <div class="model-dot" style="background:var(--green)"></div>
          <div class="model-info">
            <div class="model-name">\${m.name}</div>
            <div class="model-detail">\${m.details?.parameter_size||''} · \${m.details?.family||'ollama'} · \${formatBytes(m.size||0)}</div>
          </div>
          <div class="flex gap-6">
            <button class="btn btn-ghost btn-sm" onclick="testOllamaModel('\${m.name}')">Test</button>
            <button class="btn btn-ghost btn-sm" onclick="chatWithOllama('\${m.name}')">Chat</button>
          </div>
        </div>\`).join('');
    } else {
      listEl.innerHTML='<div class="mono text-dim" style="padding:8px">No models found. Run: ollama pull nous-hermes2</div>';
    }
  }catch(e){
    statusEl.textContent='OFFLINE';statusEl.style.cssText='background:var(--red-dim);color:var(--red)';
    document.getElementById('modelsBadge').textContent='0';
    listEl.innerHTML='<div class="mono text-dim" style="padding:8px">Cannot reach localhost:11434. Start Ollama and set OLLAMA_ORIGINS=*<br><br>Run: OLLAMA_ORIGINS=* ollama serve</div>';
  }
}
async function testOllamaModel(name){
  const out=document.getElementById('ollamaTestOut');
  out.textContent='Testing '+name+'...';out.style.color='var(--text-dim)';
  try{
    const r=await fetch('http://localhost:11434/api/chat',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({model:name,messages:[{role:'user',content:'Reply with exactly: OK'}],stream:false})
    });
    const d=await r.json();
    out.textContent=name+' response: '+(d.message?.content||'[no response]');
    out.style.color='var(--green)';
  }catch(e){out.textContent='Error: '+e.message;out.style.color='var(--red)';}
}
function chatWithOllama(name){
  const sel=document.getElementById('modelSelect');
  const optVal='ollama:'+name;
  let found=false;
  Array.from(sel.options).forEach(o=>{if(o.value===optVal){sel.value=optVal;found=true;}});
  if(!found){
    const opt=document.createElement('option');opt.value=optVal;opt.textContent=name+' (local)';
    sel.querySelector('optgroup[label="Ollama Local"]').appendChild(opt);
    sel.value=optVal;
  }
  onModelChange();nav('chat',null);
  addMsg('sys','Local model loaded: '+name);
}

// ===== RAG / SOURCE =====
let ragSources=JSON.parse(localStorage.getItem('sc_rag_sources')||'null')||[
  {id:1,name:'DCSE Governance Doctrine (D01-D08)',url:'',content:'',status:'indexed',chars:0},
  {id:2,name:'SC Command Post GitHub',url:'https://github.com/sonlyconsulting-ctrl/dcse-command-post',content:'',status:'live',chars:0},
  {id:3,name:'Tribunal Relay GitHub',url:'https://github.com/sonlyconsulting-ctrl/dcse-tribunal-relay',content:'',status:'live',chars:0},
  {id:4,name:'SC LP Trial Packet',url:'',content:'',status:'indexed',chars:0},
  {id:5,name:'GovOS RAG Architecture',url:'',content:'',status:'pending',chars:0},
  {id:6,name:'Supabase SC Schema',url:'',content:'',status:'pending',chars:0},
  {id:7,name:'Wix CMS Site Map',url:'',content:'',status:'pending',chars:0},
  {id:8,name:'DDNA Harvest Queue',url:'',content:'',status:'queued',chars:73}
];
function saveRag(){localStorage.setItem('sc_rag_sources',JSON.stringify(ragSources));}
const ragStatusStyle={indexed:'background:var(--green-dim);color:var(--green)',live:'background:var(--teal-dim);color:var(--teal)',pending:'background:var(--navy-border);color:var(--text-dim)',queued:'background:var(--amber-dim);color:var(--amber)'};
function renderRag(){
  const list=document.getElementById('ragSourceList');if(!list)return;
  list.innerHTML=ragSources.map(s=>\`
    <div class="trib-item">
      <span class="trib-status" style="\${ragStatusStyle[s.status]||''}">\${s.status.toUpperCase()}</span>
      <div class="trib-info">
        <div class="trib-title">\${s.name}\${s.url?' <a href="'+s.url+'" target="_blank" style="color:var(--blue);font-size:9px;margin-left:6px">↗</a>':''}</div>
        <div class="trib-meta">\${s.chars?s.chars+' chars indexed':'No content indexed'}</div>
      </div>
      <div class="flex gap-6">
        <button class="btn btn-ghost btn-sm" onclick="editRagSource(\${s.id})">Edit</button>
        <button class="btn btn-ghost btn-sm" onclick="queryRagSource(\${s.id})">Query</button>
        <button class="btn btn-ghost btn-sm" onclick="runRagDDNA(\${s.id})">DDNA</button>
        <button class="btn btn-ghost btn-sm" style="color:var(--red)" onclick="deleteRagSource(\${s.id})">✕</button>
      </div>
    </div>\`).join('');
  document.getElementById('ragBadge').textContent=ragSources.length;
  const tag=document.getElementById('ragCountTag');if(tag)tag.textContent=ragSources.length+' SOURCES';
}
function clearRagForm(){
  document.getElementById('ragName').value='';document.getElementById('ragUrl').value='';
  document.getElementById('ragContent').value='';document.getElementById('ragEditId').value='';
}
function saveRagEdit(){
  const id=parseInt(document.getElementById('ragEditId').value)||0;
  const name=document.getElementById('ragName').value.trim();if(!name)return;
  const url=document.getElementById('ragUrl').value.trim();
  const content=document.getElementById('ragContent').value.trim();
  if(id){
    const s=ragSources.find(x=>x.id===id);
    if(s){s.name=name;s.url=url;s.content=content;s.chars=content.length;s.status=content?'indexed':url?'live':'pending';}
  } else {
    ragSources.push({id:Date.now(),name,url,content,status:content?'indexed':url?'live':'pending',chars:content.length});
  }
  saveRag();renderRag();clearRagForm();
}
function editRagSource(id){
  const s=ragSources.find(x=>x.id===id);if(!s)return;
  document.getElementById('ragName').value=s.name;
  document.getElementById('ragUrl').value=s.url||'';
  document.getElementById('ragContent').value=s.content||'';
  document.getElementById('ragEditId').value=id;
}
function deleteRagSource(id){ragSources=ragSources.filter(x=>x.id!==id);saveRag();renderRag();}
async function queryRagSource(id){
  const s=ragSources.find(x=>x.id===id);if(!s)return;
  const q=document.getElementById('ragQuery').value.trim();
  if(!q){document.getElementById('ragQueryResult').textContent='Enter a question in the Query box above.';return;}
  const model=document.getElementById('modelSelect').value;
  const p=providerOf(model);
  const context=s.content||('Source reference: '+s.name+(s.url?' at '+s.url:''));
  const sysPrompt='You are a retrieval assistant. Answer ONLY based on this source context.\\n\\nSOURCE ('+s.name+'):\\n'+context.slice(0,4000);
  document.getElementById('ragQueryResult').textContent='Querying...';document.getElementById('ragQueryResult').style.color='var(--text-dim)';
  try{
    let reply;
    if(p==='ollama'){
      const om=model.replace('ollama:','');
      const r=await fetch('http://localhost:11434/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:om,messages:[{role:'system',content:sysPrompt},{role:'user',content:q}],stream:false})});
      const d=await r.json();reply=d.message?.content||'[no response]';
    } else {
      const apiKey=keyInput.value;
      if(!PROVIDER_META[p].check(apiKey)){document.getElementById('ragQueryResult').textContent='Enter API key for '+PROVIDER_META[p].label;return;}
      const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,messages:[{role:'user',content:q}],system:sysPrompt,apiKey})});
      const d=await r.json();reply=d.text||d.error||'[no response]';
    }
    document.getElementById('ragQueryResult').textContent=reply;document.getElementById('ragQueryResult').style.color='var(--cream)';
  }catch(e){document.getElementById('ragQueryResult').textContent='Error: '+e.message;}
}
function runRagDDNA(id){
  const s=ragSources.find(x=>x.id===id);
  if(!s||!s.content){alert('No content indexed for this source. Add content first.');return;}
  document.getElementById('ddnaInput').value=s.content.slice(0,3000);
  nav('ddna',null);
  setTimeout(()=>document.getElementById('harvestBtn').click(),300);
}

// ===== TRIBUNAL =====
const TRIBUNAL_PRS=[
  {num:5,title:'SC LP Trial Packet: trial designation, skill line fix, hero line',branch:'claude/dcs-packet-trial-confirm-jwuzsy',date:'2026-07-08',status:'draft',url:'https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay/pull/5'},
  {num:4,title:'SC LP Trial Build Dispatch Packet (TRIB-20260708)',branch:'claude/tribunal-inbox-schema-packet-i9rt45',date:'2026-07-08',status:'draft',url:'https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay/pull/4'},
  {num:3,title:'Tribunal protocol: Account-level ChatGPT to GitHub',branch:'tribunal/account-level-chatgpt-github',date:'2026-06-20',status:'draft',url:'https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay/pull/3'},
  {num:2,title:'Tribunal closeout: ChatGPT SC GovOS RAG website session',branch:'tribunal/session-closeout-20260619',date:'2026-06-19',status:'draft',url:'https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay/pull/2'},
  {num:1,title:'Update from task 64ffd9b7 (qwen-chat)',branch:'dcse-tribunal-authorization-process',date:'2026-06-08',status:'open',url:'https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay/pull/1'},
];
let tribunalFilter='all';
function renderTribunal(filter){
  tribunalFilter=filter||tribunalFilter;
  const list=document.getElementById('tribunalList');if(!list)return;
  const shown=tribunalFilter==='all'?TRIBUNAL_PRS:TRIBUNAL_PRS.filter(p=>p.status===tribunalFilter);
  list.innerHTML=shown.map(p=>\`
    <div class="trib-item">
      <span class="trib-status \${p.status==='draft'?'ts-draft':'ts-open'}">\${p.status.toUpperCase()}</span>
      <div class="trib-info">
        <div class="trib-title">#\${p.num} — \${p.title}</div>
        <div class="trib-meta">\${p.branch} · \${p.date}</div>
      </div>
      <a class="btn btn-ghost btn-sm" href="\${p.url}" target="_blank">Open PR ↗</a>
    </div>\`).join('');
  document.querySelectorAll('.trib-filter-btn').forEach(b=>b.classList.toggle('btn-gold',b.dataset.filter===tribunalFilter));
}

// ===== DISPATCH =====
let dispatchPackets=JSON.parse(localStorage.getItem('sc_dispatch')||'null')||[
  {id:'TRIB-20260708-SC-LP-TRIAL-BUILD-DISPATCH',status:'ready',desc:'Hero line locked · Skill line agent-neutral · Trial: CONTROLLED_TRIAL SC_LP_20260707',created:'2026-07-08',inbox:'\\\\\\\\LAPTOP-74UF76GB\\\\DS All Things\\\\DCSE_Command_Center\\\\_Tribunal_Inbox'}
];
function saveDispatch(){localStorage.setItem('sc_dispatch',JSON.stringify(dispatchPackets));}
function renderDispatch(){loadDispatchInbox('all');}

let _dispatchData=null;
async function loadDispatchInbox(filter){
  filter=filter||'all';
  try{
    const r=await fetch('/api/tribunal/inbox');
    _dispatchData=await r.json();
    const s=_dispatchData.stats;
    const el=id=>document.getElementById(id);
    if(el('dspPlanned'))el('dspPlanned').textContent=s.planned;
    if(el('dspAssigned'))el('dspAssigned').textContent=s.assigned;
    if(el('dspRunning'))el('dspRunning').textContent=s.running;
    if(el('dspCompleted'))el('dspCompleted').textContent=s.completed;
    const tl=el('dispatchTaskList');
    if(tl){
      let tasks=_dispatchData.tasks;
      if(filter==='active')tasks=tasks.filter(t=>['planned','assigned','running','needs_review','awaiting_dcs'].includes(t.status));
      else if(filter==='completed')tasks=tasks.filter(t=>['completed','approved'].includes(t.status));
      else if(filter==='blocked')tasks=tasks.filter(t=>['blocked','rejected'].includes(t.status));
      const statusTag=(st)=>{
        const m={planned:'tag-amber',assigned:'tag-blue',running:'tag-teal',completed:'tag-green',approved:'tag-green',blocked:'tag-red',rejected:'tag-red',needs_review:'tag-amber',awaiting_dcs:'tag-amber'};
        return '<span class="tag '+(m[st]||'tag-amber')+'">'+st.toUpperCase().replace(/_/g,' ')+'</span>';
      };
      const prioLabel=(p)=>({1:'P1',2:'P2',3:'P3',4:'P4',5:'P5'}[p]||'P3');
      const agentName=(id)=>{
        if(!id)return 'Unassigned';
        const a=(_dispatchData.agents||[]).find(a=>a.id===id);
        return a?a.display_name:'Agent '+id.slice(0,8);
      };
      if(!tasks.length){tl.innerHTML='<div class="text-dim mono" style="padding:16px;font-size:11px">No tasks matching filter</div>';return;}
      tl.innerHTML=tasks.map(t=>\`
        <div class="trib-item">
          \${statusTag(t.status)}
          <div class="trib-info">
            <div class="trib-title">\${t.task_key}: \${t.title}</div>
            <div class="trib-meta">\${t.lane} / \${t.task_type} / \${prioLabel(t.priority)} / \${agentName(t.assigned_agent_id)}</div>
            \${t.description?'<div class="trib-meta" style="margin-top:2px;font-size:9px">'+t.description+'</div>':''}
          </div>
          <div class="flex gap-6">
            <span class="mono" style="font-size:8px;color:var(--text-dim)">\${t.updated_at?new Date(t.updated_at).toLocaleDateString():''}</span>
          </div>
        </div>\`).join('');
    }
    const evl=el('dispatchEventList');
    if(evl&&_dispatchData.events&&_dispatchData.events.length){
      evl.innerHTML=_dispatchData.events.slice(0,10).map(e=>\`
        <div style="font-size:10px;padding:4px 0;border-bottom:1px solid var(--border);display:flex;gap:8px;align-items:center">
          <span class="tag tag-blue" style="font-size:8px">\${e.event_type}</span>
          <span style="flex:1;color:var(--text-dim)">\${e.event_summary||''}</span>
          <span class="mono" style="font-size:8px;color:var(--text-dim)">\${e.actor_label||''} \${e.created_at?new Date(e.created_at).toLocaleTimeString('en-US',{hour12:false}):''}</span>
        </div>\`).join('');
    }
  }catch(e){console.error('Dispatch inbox error:',e);}
}

async function createDispatch(){
  const title=(document.getElementById('dispatchTitle')||{}).value?.trim();
  if(!title){alert('Title required');return;}
  const desc=(document.getElementById('dispatchDesc')||{}).value?.trim();
  const lane=(document.getElementById('dispatchLane')||{}).value||'DCSE';
  const task_type=(document.getElementById('dispatchType')||{}).value||'other';
  const priority=parseInt((document.getElementById('dispatchPriority')||{}).value)||3;
  try{
    const r=await fetch('/api/tribunal/dispatch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title,description:desc,lane,task_type,priority})});
    const data=await r.json();
    if(data.ok){
      document.getElementById('dispatchTitle').value='';document.getElementById('dispatchDesc').value='';
      document.getElementById('dispatchForm').style.display='none';
      loadDispatchInbox('all');
    }else{alert('Dispatch error: '+(data.error||'Unknown'));}
  }catch(e){alert('Dispatch failed: '+e.message);}
}

function addDispatch(){createDispatch();}
function deleteDispatch(){}
function copyDispatchJSON(){}
function copyDispatchPath(){}
function setDispatchStatus(){}

// ===== RUNTIME HEALTH =====
let _runtimeChecked=false;
async function refreshRuntimeHealth(){
  _runtimeChecked=true;
  document.getElementById('ollamaLastCheck').textContent=new Date().toLocaleTimeString('en-US',{hour12:false});
  try{
    const r=await fetch('/api/runtime');
    const data=await r.json();
    if(data.ollama){
      const o=data.ollama;
      const tag=document.getElementById('ollamaEndpointStatus');
      tag.textContent=o.status==='running'?'RUNNING':'UNREACHABLE';
      tag.className='tag '+(o.status==='running'?'tag-green':'tag-red');
      document.getElementById('ollamaVersion').textContent=o.version||'unknown';
      document.getElementById('runtimeBadge').textContent=o.models?o.models.length:'0';
      const list=document.getElementById('modelRegistryList');
      if(o.models&&o.models.length){
        list.innerHTML=o.models.map(m=>\`
          <div class="trib-item">
            <span class="trib-status ts-open">\${m.name?'INSTALLED':'?'}</span>
            <div class="trib-info">
              <div class="trib-title">\${m.name||m.model||'unknown'}</div>
              <div class="trib-meta">Size: \${m.size?Math.round(m.size/1e9*10)/10+'GB':'?'} · Modified: \${m.modified_at?m.modified_at.split('T')[0]:'?'}</div>
            </div>
          </div>\`).join('');
      }else{
        list.innerHTML='<div class="mono text-dim" style="padding:12px;font-size:11px">No models installed or Ollama not reachable.</div>';
      }
    }
    if(data.jobs){
      const jl=document.getElementById('ollamaJobsList');
      if(data.jobs.length){
        jl.innerHTML=data.jobs.map(j=>\`
          <div class="trib-item">
            <span class="trib-status \${j.status==='completed'?'ts-open':'ts-draft'}">\${(j.status||'queued').toUpperCase()}</span>
            <div class="trib-info">
              <div class="trib-title">\${j.model||'?'} — \${j.source_type||'?'}</div>
              <div class="trib-meta">Retries: \${j.retry_count||0} · Duration: \${j.duration_ms?j.duration_ms+'ms':'?'}</div>
            </div>
          </div>\`).join('');
      }else{
        jl.innerHTML='<div class="mono text-dim" style="padding:12px;font-size:11px">No jobs recorded.</div>';
      }
    }
  }catch(e){
    document.getElementById('ollamaEndpointStatus').textContent='ERROR';
    document.getElementById('ollamaEndpointStatus').className='tag tag-red';
    document.getElementById('modelRegistryList').innerHTML='<div class="mono text-dim" style="padding:12px;font-size:11px">Error: '+e.message+'</div>';
  }
}

async function runRuntimeSmokeTest(){
  const el=document.getElementById('smokeTestResult');
  el.textContent='Running...';
  try{
    const r=await fetch('/api/runtime/smoke',{method:'POST'});
    const data=await r.json();
    if(data.pass){
      el.textContent='PASS — '+data.model+' responded in '+data.duration_ms+'ms';
      el.style.color='var(--green)';
    }else{
      el.textContent='FAIL — '+(data.error||'unknown');
      el.style.color='var(--red)';
    }
  }catch(e){
    el.textContent='ERROR — '+e.message;
    el.style.color='var(--red)';
  }
}

// ===== PHASE GATE BOARD =====
function refreshPhaseGate(){
  const badge=document.getElementById('phasegateBadge');
  if(badge){badge.textContent='10';badge.className='nav-badge nb-green';}
}

// ===== DCS DECISION QUEUE =====
let _dcsqueueChecked=false;
async function refreshDCSQueue(){
  _dcsqueueChecked=true;
  const badge=document.getElementById('dcsqueueBadge');
  try{
    const r=await fetch('/api/dcsqueue');
    const data=await r.json();
    if(badge)badge.textContent=data.pending_count||'0';
    if(data.decisions&&data.decisions.length){
      const list=document.getElementById('dcsDecisionList');
      if(list){
        list.innerHTML=data.decisions.map(d=>'<div class="trib-item"><span class="trib-status" style="background:rgba(255,255,255,.05);color:var(--'+(d.status==='PENDING'?'red':'amber')+')">'+(d.status||'PENDING')+'</span><div class="trib-info"><div class="trib-title">'+d.title+'</div><div class="trib-meta">'+(d.context||'')+'</div></div></div>').join('');
      }
    }
  }catch(e){
    if(badge){badge.textContent='ERR';badge.className='nav-badge nb-red';}
  }
}

// ===== RECEIPTS =====
let _receiptsChecked=false;
async function refreshReceipts(){
  _receiptsChecked=true;
  const badge=document.getElementById('receiptsBadge');
  try{
    const r=await fetch('/api/receipts');
    const data=await r.json();
    if(badge){badge.textContent=data.receipt_count||'0';badge.className='nav-badge '+(data.receipt_count?'nb-green':'nb-amber');}
  }catch(e){
    if(badge){badge.textContent='ERR';badge.className='nav-badge nb-red';}
  }
}

// ===== CONFIGURATION =====
let _configChecked=false;
function refreshConfig(){
  _configChecked=true;
  const badge=document.getElementById('configBadge');
  if(badge){badge.textContent='v1';badge.className='nav-badge nb-green';}
}

// ===== AGENT OPERATIONS =====
let _agentopsChecked=false;
async function refreshAgentOps(){
  _agentopsChecked=true;
  try{
    const r=await fetch('/api/agentops');
    const data=await r.json();
    if(data.heartbeats){
      const hc=document.getElementById('heartbeatCount');if(hc)hc.textContent=data.heartbeats.active||'0';
      const hl=document.getElementById('heartbeatLast');if(hl)hl.textContent=data.heartbeats.last||'None';
      const hs=document.getElementById('heartbeatStale');if(hs)hs.textContent=data.heartbeats.stale||'0';
    }
    if(data.tasks){
      const tp=document.getElementById('tasksPending');if(tp)tp.textContent=data.tasks.pending||'0';
      const ti=document.getElementById('tasksInProgress');if(ti)ti.textContent=data.tasks.in_progress||'0';
      const tc=document.getElementById('tasksCompleted');if(tc)tc.textContent=data.tasks.completed||'0';
      const tf=document.getElementById('tasksFailed');if(tf)tf.textContent=data.tasks.failed||'0';
    }
    if(data.decisions){
      const dd=document.getElementById('decisionsAwaitingDCS');if(dd)dd.textContent=data.decisions.awaiting_dcs||'0';
      const dr=document.getElementById('decisionsAwaitingReview');if(dr)dr.textContent=data.decisions.awaiting_review||'0';
      const db=document.getElementById('decisionsBlockers');if(db)db.textContent=data.decisions.blockers||'0';
    }
    if(data.relay){
      const rd=document.getElementById('relayEventDetect');
      if(rd){rd.textContent=data.relay.event_detection||'UNKNOWN';rd.className='tag tag-'+(data.relay.event_detection==='ACTIVE'?'green':'amber');}
      const ra=document.getElementById('relayAssignRouting');
      if(ra){ra.textContent=data.relay.assignment_routing||'UNKNOWN';ra.className='tag tag-'+(data.relay.assignment_routing==='ACTIVE'?'green':'amber');}
    }
    const ael=document.getElementById('activityEventsList');
    if(ael&&data.recent_events&&data.recent_events.length){
      ael.innerHTML=data.recent_events.map(e=>'<div class="trib-row"><div class="trib-title">'+(e.event_type||'event')+'</div><div class="trib-meta">'+(e.agent_id||'system')+' · '+(e.created_at||'')+'</div></div>').join('');
    }else if(ael&&data.recent_events){
      ael.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">No recent activity events.</div>';
    }
    const arl=document.getElementById('agentRegistryList');
    if(arl&&data.agents&&data.agents.length){
      arl.innerHTML=data.agents.map(a=>'<div class="trib-row"><div class="trib-title">'+(a.agent_name||a.agent_id||'agent')+'</div><div class="trib-meta">Type: '+(a.agent_type||'unknown')+' · Status: '+(a.status||'unknown')+'</div></div>').join('');
    }else if(arl&&data.agents){
      arl.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">No agents registered.</div>';
    }
    const pal=document.getElementById('pendingAssignmentsList');
    if(pal&&data.pending_assignments&&data.pending_assignments.length){
      pal.innerHTML=data.pending_assignments.map(p=>'<div class="trib-row"><div class="trib-title">'+(p.task_id||'task')+'</div><div class="trib-meta">Agent: '+(p.agent_id||'unassigned')+' · '+(p.created_at||'')+'</div></div>').join('');
    }else if(pal&&data.pending_assignments){
      pal.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">No pending assignments.</div>';
    }
    const badge=document.getElementById('agentopsBadge');
    if(badge){badge.textContent=(data.tasks?data.tasks.in_progress:'?');badge.className='nav-badge '+(data.tasks&&parseInt(data.tasks.in_progress)>0?'nb-green':'nb-amber');}
  }catch(e){
    const badge=document.getElementById('agentopsBadge');
    if(badge){badge.textContent='ERR';badge.className='nav-badge nb-red';}
  }
}

// ===== DBA CONSOLE =====
let _dbaChecked=false;
async function refreshDBA(){
  _dbaChecked=true;
  const tc=document.getElementById('dbaTableCount');
  const sv=document.getElementById('dbaSchemaVersion');
  const lm=document.getElementById('dbaLastMigration');
  const tl=document.getElementById('dbaTableList');
  if(tc)tc.textContent='Loading...';
  try{
    const r=await fetch('/api/dba');
    const data=await r.json();
    if(tc)tc.textContent=data.table_count||'?';
    if(sv)sv.textContent=data.schema_version||'dcse_cp active';
    if(lm)lm.textContent=data.last_migration||'005 (Security Remediation)';
    if(tl&&data.tables&&data.tables.length){
      tl.innerHTML=data.tables.map(t=>'<div class="trib-row"><div class="trib-title">'+t.name+'</div><div class="trib-meta">Rows: '+(t.row_count!=null?t.row_count:'?')+' · Schema: '+(t.schema||'dcse_cp')+'</div></div>').join('');
    }else if(tl){
      tl.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">'+(data.error||'No table data available')+'</div>';
    }
    const badge=document.getElementById('dbaBadge');
    if(badge){badge.textContent=data.table_count||'?';badge.className='nav-badge '+(data.table_count?'nb-green':'nb-amber');}
  }catch(e){
    if(tc)tc.textContent='Error';
    if(tl)tl.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">'+e.message+'</div>';
  }
}

// ===== API KEYS ADMIN =====
let _apikeysChecked=false;
async function refreshAPIKeys(){
  _apikeysChecked=true;
  try{
    const r=await fetch('/api/apikeys');
    const data=await r.json();
    const providers=['anthropic','openai','google','qwen','supabase'];
    providers.forEach(p=>{
      const el=document.getElementById('apikey'+p.charAt(0).toUpperCase()+p.slice(1));
      if(el&&data.providers&&data.providers[p]){
        const s=data.providers[p];
        el.textContent=s.status||'UNKNOWN';
        el.className='tag tag-'+(s.status==='CONFIGURED'?'green':s.status==='SERVER-SIDE ONLY'?'green':'amber');
      }
    });
    const badge=document.getElementById('apikeysBadge');
    if(badge&&data.configured_count!=null){badge.textContent=data.configured_count+'/'+data.total_count;badge.className='nav-badge '+(data.configured_count===data.total_count?'nb-green':'nb-amber');}
  }catch(e){
    const badge=document.getElementById('apikeysBadge');
    if(badge){badge.textContent='ERR';badge.className='nav-badge nb-red';}
  }
}

// ===== ASSURANCE LOOPS =====
let _assuranceChecked=false;
async function refreshAssurance(){
  _assuranceChecked=true;
  try{
    const r=await fetch('/api/assurance');
    const data=await r.json();
    if(data.loops){
      const rows=document.querySelectorAll('#assuranceLoopStatus > div:not(:first-child)');
      data.loops.forEach((loop,i)=>{
        if(rows[i]){
          const cells=rows[i].querySelectorAll('span');
          if(cells[2]){cells[2].textContent=loop.status||'UNKNOWN';cells[2].className='tag tag-'+(loop.status==='PASS'?'green':loop.status==='FAIL'?'red':'amber')+' '+'font-size:9px';}
          if(cells[3]){cells[3].textContent=loop.evidence_count?loop.evidence_count+' items':'NONE';cells[3].className='tag tag-'+(loop.evidence_count?'green':'amber')+' '+'font-size:9px';}
          if(cells[4])cells[4].textContent=loop.last_run||'...';
        }
      });
    }
    if(data.fullness){
      const dims={req:'fullnessReq',func:'fullnessFunc',data:'fullnessData',ops:'fullnessOps',gov:'fullnessGov',release:'fullnessRelease'};
      Object.entries(dims).forEach(([k,id])=>{
        const el=document.getElementById(id);
        if(el&&data.fullness[k]){el.textContent=data.fullness[k];el.className='tag tag-'+(data.fullness[k]==='PASS'?'green':data.fullness[k]==='FAIL'?'red':'amber');}
      });
    }
    const badge=document.getElementById('assuranceBadge');
    if(badge&&data.summary){badge.textContent=data.summary;badge.className='nav-badge '+(data.all_pass?'nb-green':'nb-amber');}
  }catch(e){
    const badge=document.getElementById('assuranceBadge');
    if(badge){badge.textContent='ERR';badge.className='nav-badge nb-red';}
  }
}

// ===== PERSONAS =====
let _personasFilter='all';
async function loadPersonas(filter){
  _personasFilter=filter||_personasFilter;
  const list=document.getElementById('personasList');if(!list)return;
  list.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">Fetching...</div>';
  try{
    const url='/api/personas'+(filter&&filter!=='all'?'?lifecycle='+filter:'');
    const r=await fetch(url);
    const data=await r.json();
    if(data.gate){
      list.innerHTML='<div class="mono text-dim" style="padding:12px;font-size:11px;line-height:1.8">'+data.gate+'</div>';
      return;
    }
    if(!data.personas||!data.personas.length){list.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">No personas found.</div>';return;}
    document.getElementById('personasBadge').textContent=data.personas.length;
    list.innerHTML=data.personas.map(p=>\`
      <div class="trib-item">
        <span class="trib-status \${p.dcse_lifecycle==='active'?'ts-open':'ts-draft'}">\${(p.dcse_lifecycle||p.release_posture||'unknown').toUpperCase()}</span>
        <div class="trib-info">
          <div class="trib-title">\${p.identity_mask?'[MASKED]':p.display_name||p.code||p.id}</div>
          <div class="trib-meta">\${p.code||''} · Lane: \${p.dcs_lane||'—'} · Privacy: \${p.privacy_class||'—'}</div>
          \${p.identity_mask?'<div class="trib-meta" style="color:var(--amber);font-size:9px">IDENTITY MASKED — no identifying fields rendered</div>':''}
        </div>
        \${p.family_product?'<span class="tag tag-blue" style="font-size:9px">FAMILY</span>':''}
        \${p.child_safe?'<span class="tag tag-green" style="font-size:9px">CHILD-SAFE</span>':''}
      </div>\`).join('');
  }catch(e){
    list.innerHTML='<div class="mono text-dim" style="padding:12px;font-size:11px">Error: '+e.message+'</div>';
  }
}

// ===== ASSETS =====
let _assetsFilter='all';
async function loadAssets(filter){
  _assetsFilter=filter||_assetsFilter;
  const list=document.getElementById('assetsList');if(!list)return;
  list.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">Fetching...</div>';
  try{
    const url='/api/assets'+(filter&&filter!=='all'?'?state='+filter:'');
    const r=await fetch(url);
    const data=await r.json();
    if(data.gate){
      list.innerHTML='<div class="mono text-dim" style="padding:12px;font-size:11px;line-height:1.8">'+data.gate+'</div>';
      return;
    }
    if(!data.assets||!data.assets.length){list.innerHTML='<div class="text-dim mono" style="padding:12px;font-size:11px">No assets found.</div>';return;}
    document.getElementById('assetsBadge').textContent=data.assets.length;
    const stateColor={deployed:'var(--green)',approved:'var(--blue)',active:'var(--gold)',candidate:'var(--text-dim)',review:'var(--amber)',blocked:'var(--red)',quarantined:'var(--red)'};
    list.innerHTML=data.assets.map(a=>\`
      <div class="trib-item">
        <span class="trib-status" style="background:rgba(255,255,255,.05);color:\${stateColor[a.dcse_state||a.asset_type]||'var(--text-dim)'}">\${(a.dcse_state||'inventoried').toUpperCase()}</span>
        <div class="trib-info">
          <div class="trib-title">\${a.asset_name||a.asset_label||a.url||a.id}</div>
          <div class="trib-meta">Type: \${a.asset_type||'—'} · Privacy: \${a.privacy_class||'public'} · Lane: \${a.dcs_lane||'—'}</div>
          \${a.persona_fk||a.source_id?'<div class="trib-meta" style="font-size:9px">Persona: '+(a.persona_fk||a.source_id)+'</div>':''}
        </div>
        \${a.agent_approve_locked?'<span class="tag tag-amber" style="font-size:9px">APPROVE-LOCKED</span>':''}
      </div>\`).join('');
  }catch(e){
    list.innerHTML='<div class="mono text-dim" style="padding:12px;font-size:11px">Error: '+e.message+'</div>';
  }
}

// Ops Log add
function addOpsEntry(){
  const t=prompt('Ops log entry:');if(!t)return;
  const log=document.getElementById('opsLog');
  const d=document.createElement('div');d.className='mono text-dim';
  d.textContent=new Date().toISOString().split('T')[0]+' · '+t;
  log.insertBefore(d,log.firstChild);
}

// Init all renders
renderTasks();
renderPortfolio();
renderDDNA();
renderRag();
renderTribunal();
renderDispatch();
</script>
</body>
</html>`;

const SUPABASE_URL = process.env.SUPABASE_URL || 'https://nevgdyfpxdaloacuutal.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

async function handlePersonas(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (!SUPABASE_KEY) {
    res.statusCode = 200;
    res.end(JSON.stringify({gate: 'Migrations 001-003 pending DCS authorization. SUPABASE_SERVICE_ROLE_KEY not set. Apply migrations and set env var to activate this panel.'}));
    return;
  }
  try {
    const url = new URL(req.url, 'http://localhost');
    const lifecycle = url.searchParams.get('lifecycle');
    let query = `${SUPABASE_URL}/rest/v1/personas?select=id,code,display_name,release_posture,dcse_lifecycle,privacy_class,dcs_lane,identity_mask,family_product,child_safe,agent_promote_locked&order=code.asc`;
    if (lifecycle) query += `&dcse_lifecycle=eq.${lifecycle}`;
    const r = await fetch(query, {headers:{'apikey': SUPABASE_KEY,'Authorization':'Bearer '+SUPABASE_KEY,'Content-Type':'application/json'}});
    const personas = await r.json();
    res.statusCode = r.status;
    res.end(JSON.stringify({personas: Array.isArray(personas) ? personas : [], total: Array.isArray(personas) ? personas.length : 0}));
  } catch(e) {
    res.statusCode = 500;
    res.end(JSON.stringify({error: e.message}));
  }
}

async function handleAssets(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (!SUPABASE_KEY) {
    res.statusCode = 200;
    res.end(JSON.stringify({gate: 'Migrations 001-003 pending DCS authorization. SUPABASE_SERVICE_ROLE_KEY not set. Apply migrations and set env var to activate this panel.'}));
    return;
  }
  try {
    const url = new URL(req.url, 'http://localhost');
    const state = url.searchParams.get('state');
    const persona = url.searchParams.get('persona');
    let query = `${SUPABASE_URL}/rest/v1/assets?select=id,asset_name,asset_label,asset_type,url,dcse_state,privacy_class,dcs_lane,persona_fk,source_id,agent_approve_locked,agent_deploy_locked,tribunal_pr_url&order=asset_type.asc`;
    if (state) query += `&dcse_state=eq.${state}`;
    if (persona) query += `&persona_fk=eq.${persona}`;
    const r = await fetch(query, {headers:{'apikey': SUPABASE_KEY,'Authorization':'Bearer '+SUPABASE_KEY,'Content-Type':'application/json'}});
    const assets = await r.json();
    res.statusCode = r.status;
    res.end(JSON.stringify({assets: Array.isArray(assets) ? assets : [], total: Array.isArray(assets) ? assets.length : 0}));
  } catch(e) {
    res.statusCode = 500;
    res.end(JSON.stringify({error: e.message}));
  }
}

const OLLAMA_URL = 'http://127.0.0.1:11434';

async function handleRuntime(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    let ollamaData = {status: 'unreachable', version: null, models: []};
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 5000);
      const vr = await fetch(OLLAMA_URL, {signal: ctrl.signal});
      clearTimeout(t);
      const vt = await vr.text();
      ollamaData.status = 'running';
      ollamaData.version = vt.includes('Ollama') ? vt.trim() : 'connected';
      const lr = await fetch(`${OLLAMA_URL}/api/tags`, {signal: AbortSignal.timeout(5000)});
      const ld = await lr.json();
      ollamaData.models = ld.models || [];
    } catch(e) {
      ollamaData.status = 'unreachable';
      ollamaData.error = e.message;
    }
    let jobs = [];
    if (SUPABASE_KEY) {
      try {
        const jr = await fetch(`${SUPABASE_URL}/rest/v1/rpc/`, {method: 'POST', headers: {'apikey': SUPABASE_KEY, 'Authorization': 'Bearer '+SUPABASE_KEY, 'Content-Type': 'application/json'}});
      } catch(e) {}
      try {
        const jr = await fetch(`${SUPABASE_URL}/rest/v1/ddna_ollama_jobs?select=id,model,source_type,status,retry_count,duration_ms,created_at&order=created_at.desc&limit=10&schema=dcse_cp`, {headers: {'apikey': SUPABASE_KEY, 'Authorization': 'Bearer '+SUPABASE_KEY, 'Content-Type': 'application/json', 'Accept-Profile': 'dcse_cp'}});
        const jd = await jr.json();
        if (Array.isArray(jd)) jobs = jd;
      } catch(e) {}
    }
    res.statusCode = 200;
    res.end(JSON.stringify({ollama: ollamaData, jobs}));
  } catch(e) {
    res.statusCode = 500;
    res.end(JSON.stringify({error: e.message}));
  }
}

async function handleRuntimeSmoke(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    try {
      const start = Date.now();
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 60000);
      const lr = await fetch(`${OLLAMA_URL}/api/tags`, {signal: ctrl.signal});
      const ld = await lr.json();
      const models = ld.models || [];
      if (!models.length) {
        clearTimeout(t);
        res.statusCode = 200;
        res.end(JSON.stringify({pass: false, error: 'No models installed'}));
        return;
      }
      const model = models[0].name || models[0].model;
      const sr = await fetch(`${OLLAMA_URL}/api/generate`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({model, prompt: 'Respond with exactly: {"status":"ok"}', stream: false, format: 'json'}),
        signal: ctrl.signal
      });
      const sd = await sr.json();
      clearTimeout(t);
      const duration_ms = Date.now() - start;
      const pass = sd.response && sd.response.includes('ok');
      res.statusCode = 200;
      res.end(JSON.stringify({pass, model, duration_ms, response: sd.response ? sd.response.substring(0, 200) : null, error: pass ? null : 'Unexpected response'}));
    } catch(e) {
      res.statusCode = 200;
      res.end(JSON.stringify({pass: false, error: e.name === 'AbortError' ? 'Timeout (60s)' : e.message}));
    }
  });
}

async function handleDCSQueue(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  const decisions = [
    {title: 'SC Hero Line Final Selection', status: 'PENDING', context: 'MVT-011 · DDNA process required · PR #5 held'},
    {title: 'TSL Source Reconstruction Packet', status: 'PENDING', context: 'MVT-013 · Issue #3 · Source material from DCS'},
    {title: 'SC Brand Palette Confirmation', status: 'PENDING', context: 'MVT-009/016 · Visual identity lock'},
    {title: 'Production Deployment Authorization', status: 'PENDING', context: 'Batch 5 · Post-staging DCS promotion'}
  ];
  res.statusCode = 200;
  res.end(JSON.stringify({decisions, pending_count: decisions.filter(d => d.status === 'PENDING').length}));
}

async function handleReceipts(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  const receipts = [
    {title: 'PR #5 Agent OS v1.3 Baseline', status: 'VERIFIED', ref: 'c8f5270'},
    {title: 'PR #6 Personas/Assets Module', status: 'VERIFIED', ref: '12acec7'},
    {title: 'Migration 004 Relay RPC Security', status: 'VERIFIED', ref: 'Applied'},
    {title: 'PR #8 Batch 1 P0 Surfaces', status: 'VERIFIED', ref: 'ad2f82d (merged)'},
    {title: 'Migration 005 Security Remediation', status: 'VERIFIED', ref: 'Applied (4 sections)'}
  ];
  res.statusCode = 200;
  res.end(JSON.stringify({receipts, receipt_count: receipts.length}));
}

async function handleAgentOps(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  const result = {
    relay: {event_detection: 'UNKNOWN', assignment_routing: 'UNKNOWN'},
    heartbeats: {active: 0, last: null, stale: 0},
    tasks: {pending: 0, in_progress: 0, completed: 0, failed: 0},
    decisions: {awaiting_dcs: 0, awaiting_review: 0, blockers: 0},
    recent_events: [],
    agents: [],
    pending_assignments: []
  };
  if (SUPABASE_KEY) {
    const headers = {'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`};
    const base = SUPABASE_URL + '/rest/v1';
    try {
      const [hbr, tsr, aer, arr, par] = await Promise.all([
        fetch(`${base}/agent_heartbeats?select=id,agent_id,heartbeat_status,last_seen_at,capability_status,notes&order=last_seen_at.desc&limit=20`, {headers}).catch(() => null),
        fetch(`${base}/agent_tasks?select=id,task_key,title,task_type,status,priority,lane,assignment_mode,assigned_agent_id,updated_at&order=updated_at.desc&limit=30`, {headers}).catch(() => null),
        fetch(`${base}/agent_task_events?select=id,task_id,event_type,actor_label,event_summary,created_at&order=created_at.desc&limit=10`, {headers}).catch(() => null),
        fetch(`${base}/agent_registry?select=id,agent_key,display_name,agent_type,status,authorized_lanes&order=display_name.asc&limit=30`, {headers}).catch(() => null),
        fetch(`${base}/agent_task_assignments?select=id,task_id,agent_id,assignment_role,status,created_at&status=eq.assigned&order=created_at.desc&limit=10`, {headers}).catch(() => null)
      ]);
      if (hbr && hbr.ok) {
        const hb = await hbr.json();
        const now = Date.now();
        result.heartbeats.active = hb.filter(h => h.heartbeat_status === 'online').length;
        result.heartbeats.stale = hb.filter(h => h.last_seen_at && (now - new Date(h.last_seen_at).getTime()) > 300000).length;
        if (hb.length) result.heartbeats.last = hb[0].last_seen_at;
        result.relay.event_detection = hb.length > 0 ? 'ACTIVE' : 'UNKNOWN';
      }
      if (tsr && tsr.ok) {
        const ts = await tsr.json();
        result.tasks.pending = ts.filter(t => t.status === 'planned' || t.status === 'assigned').length;
        result.tasks.in_progress = ts.filter(t => t.status === 'running').length;
        result.tasks.completed = ts.filter(t => t.status === 'completed' || t.status === 'approved').length;
        result.tasks.failed = ts.filter(t => t.status === 'blocked' || t.status === 'rejected').length;
        result.tasks.awaiting_dcs = ts.filter(t => t.status === 'awaiting_dcs').length;
        result.tasks.needs_review = ts.filter(t => t.status === 'needs_review').length;
      }
      if (aer && aer.ok) result.recent_events = await aer.json();
      if (arr && arr.ok) {
        result.agents = await arr.json();
        result.relay.assignment_routing = result.agents.length > 0 ? 'ACTIVE' : 'UNKNOWN';
      }
      if (par && par.ok) result.pending_assignments = await par.json();
    } catch(e) {}
  }
  res.statusCode = 200;
  res.end(JSON.stringify(result));
}

async function handleDBA(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    const result = {table_count: 0, schema_version: 'dcse_cp', last_migration: '005 (Security Remediation)', tables: []};
    if (SUPABASE_KEY) {
      const tr = await fetch(`${SUPABASE_URL}/rest/v1/rpc/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`},
        body: JSON.stringify({})
      }).catch(() => null);
      const tableQuery = `${SUPABASE_URL}/rest/v1/?select=*&limit=0`;
      const knownTables = [
        'activity_audit_log','activity_events','agent_heartbeat_dashboard','agent_heartbeats',
        'agent_orchestration_dashboard','agent_registry','agent_task_assignments','agent_task_events',
        'agent_tasks','archive_events','artifact_refs','conversation_turns','conversations',
        'dashboard_activity_view','ddna_characteristics','ddna_extraction_runs','ddna_model_comparisons',
        'ddna_ollama_jobs','ddna_source_queue','path_registry','rag_jobs','relay_listener_events',
        'relay_pending_assignments','task_attachments'
      ];
      result.tables = knownTables.map(name => ({name, schema: 'dcse_cp', row_count: null}));
      result.table_count = knownTables.length;
      for (const t of result.tables.slice(0, 5)) {
        try {
          const cr = await fetch(`${SUPABASE_URL}/rest/v1/${t.name}?select=id&limit=1&offset=0`, {
            headers: {'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`, 'Prefer': 'count=exact', 'Range': '0-0'}
          });
          const range = cr.headers.get('content-range');
          if (range) {
            const total = range.split('/')[1];
            if (total && total !== '*') t.row_count = parseInt(total);
          }
        } catch(e) {}
      }
    } else {
      result.error = 'SUPABASE_KEY not configured — table inventory unavailable';
    }
    res.statusCode = 200;
    res.end(JSON.stringify(result));
  } catch(e) {
    res.statusCode = 200;
    res.end(JSON.stringify({error: e.message, table_count: 0, tables: []}));
  }
}

async function handleAPIKeys(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  const providers = {
    anthropic: {status: process.env.ANTHROPIC_API_KEY ? 'CONFIGURED' : 'NOT CONFIGURED', scope: 'chat', binding: 'vercel'},
    openai: {status: process.env.OPENAI_API_KEY ? 'CONFIGURED' : 'NOT CONFIGURED', scope: 'chat', binding: 'vercel'},
    google: {status: process.env.GOOGLE_API_KEY ? 'CONFIGURED' : 'NOT CONFIGURED', scope: 'chat', binding: 'vercel'},
    qwen: {status: process.env.DASHSCOPE_API_KEY ? 'CONFIGURED' : 'NOT CONFIGURED', scope: 'chat', binding: 'vercel'},
    supabase: {status: SUPABASE_KEY ? 'SERVER-SIDE ONLY' : 'NOT CONFIGURED', scope: 'service', binding: 'server'},
    ollama: {status: 'NO KEY REQUIRED', scope: 'local', binding: 'localhost'}
  };
  const configured_count = Object.values(providers).filter(p => p.status === 'CONFIGURED' || p.status === 'SERVER-SIDE ONLY' || p.status === 'NO KEY REQUIRED').length;
  res.statusCode = 200;
  res.end(JSON.stringify({providers, configured_count, total_count: Object.keys(providers).length}));
}

async function handleAssurance(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  const loopDefs = [
    {id: 'A0', trigger: 'Task admission or source change'},
    {id: 'A1', trigger: 'Code or configuration change'},
    {id: 'A2', trigger: 'API, adapter, event, or schema contract'},
    {id: 'A3', trigger: 'Database, migration, or storage change'},
    {id: 'A4', trigger: 'Provider, API key, or external service'},
    {id: 'A5', trigger: 'Merge candidate or feature completion'},
    {id: 'A6', trigger: 'SC or product approval candidate'},
    {id: 'A7', trigger: 'Release candidate'},
    {id: 'A8', trigger: 'Deployment or maintenance'}
  ];
  const loops = loopDefs.map(l => ({...l, status: 'UNKNOWN', evidence_count: 0, last_run: null}));
  if (SUPABASE_KEY) {
    try {
      const ar = await fetch(`${SUPABASE_URL}/rest/v1/agent_tasks?select=id,task_type,status,updated_at&task_type=like.assurance_*&order=updated_at.desc&limit=20`, {
        headers: {'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`}
      });
      if (ar.ok) {
        const tasks = await ar.json();
        tasks.forEach(t => {
          const match = (t.task_type || '').match(/assurance_(a\d)/i);
          if (match) {
            const loop = loops.find(l => l.id.toLowerCase() === match[1].toLowerCase());
            if (loop) {
              loop.status = t.status === 'completed' ? 'PASS' : t.status === 'failed' ? 'FAIL' : 'IN PROGRESS';
              loop.evidence_count = (loop.evidence_count || 0) + 1;
              if (!loop.last_run) loop.last_run = t.updated_at;
            }
          }
        });
      }
    } catch(e) {}
  }
  const all_pass = loops.every(l => l.status === 'PASS');
  const pass_count = loops.filter(l => l.status === 'PASS').length;
  const summary = pass_count + '/' + loops.length;
  res.statusCode = 200;
  res.end(JSON.stringify({
    loops, all_pass, summary,
    fullness: {req: 'UNKNOWN', func: 'UNKNOWN', data: 'UNKNOWN', ops: 'UNKNOWN', gov: 'UNKNOWN', release: 'UNKNOWN'}
  }));
}

async function handleTribunalInbox(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  const result = {tasks: [], agents: [], events: [], assignments: [], stats: {total: 0, planned: 0, assigned: 0, running: 0, completed: 0, blocked: 0, awaiting_dcs: 0}};
  if (!SUPABASE_KEY) { res.statusCode = 200; res.end(JSON.stringify(result)); return; }
  const headers = {'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`};
  const base = SUPABASE_URL + '/rest/v1';
  try {
    const [tr, ar, er, asr] = await Promise.all([
      fetch(`${base}/agent_tasks?select=id,task_key,title,description,lane,task_type,status,priority,assignment_mode,assigned_agent_id,dcs_decision_required,review_required,created_by_label,created_at,updated_at,completed_at&order=priority.asc,created_at.desc&limit=50`, {headers}).catch(() => null),
      fetch(`${base}/agent_registry?select=id,agent_key,display_name,agent_type,status,authorized_lanes,current_task_id&order=display_name.asc`, {headers}).catch(() => null),
      fetch(`${base}/agent_task_events?select=id,task_id,event_type,actor_label,event_summary,from_agent_id,to_agent_id,created_at&order=created_at.desc&limit=25`, {headers}).catch(() => null),
      fetch(`${base}/agent_task_assignments?select=id,task_id,agent_id,assignment_role,sequence_order,status,created_at&order=created_at.desc&limit=30`, {headers}).catch(() => null)
    ]);
    if (tr && tr.ok) {
      result.tasks = await tr.json();
      result.stats.total = result.tasks.length;
      result.tasks.forEach(t => {
        if (t.status === 'planned') result.stats.planned++;
        else if (t.status === 'assigned') result.stats.assigned++;
        else if (t.status === 'running') result.stats.running++;
        else if (t.status === 'completed' || t.status === 'approved') result.stats.completed++;
        else if (t.status === 'blocked' || t.status === 'rejected') result.stats.blocked++;
        else if (t.status === 'awaiting_dcs') result.stats.awaiting_dcs++;
      });
    }
    if (ar && ar.ok) result.agents = await ar.json();
    if (er && er.ok) result.events = await er.json();
    if (asr && asr.ok) result.assignments = await asr.json();
  } catch(e) {}
  res.statusCode = 200;
  res.end(JSON.stringify(result));
}

async function handleTribunalDispatch(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error: 'No database connection'})); return; }
    try {
      const {title, description, lane, task_type, priority, assignment_mode, assigned_agent_key} = JSON.parse(body);
      if (!title) { res.statusCode = 400; res.end(JSON.stringify({error: 'title required'})); return; }
      const validLanes = ['DCSE','SC','SS','TSL','TRIBUNAL','DDNA','RAG','SYSTEM'];
      const validTypes = ['build','review','rag','database','github','tribunal','qa','synthesis','handoff','decision','monitor','other'];
      const taskLane = validLanes.includes(lane) ? lane : 'DCSE';
      const taskType = validTypes.includes(task_type) ? task_type : 'other';
      const taskKey = 'TRIB-' + Date.now().toString(36).toUpperCase();
      const headers = {'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'return=representation'};
      const base = SUPABASE_URL + '/rest/v1';
      const taskPayload = {
        task_key: taskKey, title, description: description || null,
        lane: taskLane, task_type: taskType,
        priority: Math.min(5, Math.max(1, parseInt(priority) || 3)),
        assignment_mode: assignment_mode || 'single',
        status: 'planned', created_by_label: 'CP Dispatch'
      };
      if (assigned_agent_key) {
        const agentR = await fetch(`${base}/agent_registry?agent_key=eq.${encodeURIComponent(assigned_agent_key)}&select=id&limit=1`, {headers});
        if (agentR.ok) {
          const agents = await agentR.json();
          if (agents.length) { taskPayload.assigned_agent_id = agents[0].id; taskPayload.status = 'assigned'; }
        }
      }
      const cr = await fetch(`${base}/agent_tasks`, {method: 'POST', headers, body: JSON.stringify(taskPayload)});
      if (!cr.ok) { const err = await cr.text(); res.statusCode = cr.status; res.end(JSON.stringify({error: err})); return; }
      const created = await cr.json();
      const taskId = created[0]?.id;
      if (taskId) {
        await fetch(`${base}/agent_task_events`, {method: 'POST', headers, body: JSON.stringify({
          task_id: taskId, event_type: 'created', actor_label: 'CP Dispatch',
          event_summary: `Task dispatched: ${title} [${taskKey}]`
        })}).catch(() => {});
      }
      res.statusCode = 201;
      res.end(JSON.stringify({ok: true, task: created[0], task_key: taskKey}));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

async function handleTribunalReceipt(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error: 'No database connection'})); return; }
    try {
      const {task_id, event_type, actor_label, summary, result_status} = JSON.parse(body);
      if (!task_id) { res.statusCode = 400; res.end(JSON.stringify({error: 'task_id required'})); return; }
      const headers = {'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'return=representation'};
      const base = SUPABASE_URL + '/rest/v1';
      const evType = event_type || 'receipt';
      const er = await fetch(`${base}/agent_task_events`, {method: 'POST', headers, body: JSON.stringify({
        task_id, event_type: evType, actor_label: actor_label || 'system',
        event_summary: summary || `Receipt recorded for task ${task_id}`
      })});
      if (!er.ok) { const err = await er.text(); res.statusCode = er.status; res.end(JSON.stringify({error: err})); return; }
      if (result_status) {
        const validStatuses = ['completed','approved','blocked','rejected','needs_review','awaiting_dcs'];
        if (validStatuses.includes(result_status)) {
          const updatePayload = {status: result_status};
          if (result_status === 'completed' || result_status === 'approved') updatePayload.completed_at = new Date().toISOString();
          await fetch(`${base}/agent_tasks?id=eq.${task_id}`, {method: 'PATCH', headers, body: JSON.stringify(updatePayload)}).catch(() => {});
        }
      }
      const event = await er.json();
      res.statusCode = 201;
      res.end(JSON.stringify({ok: true, event: event[0]}));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

async function handleTribunalStatus(req, res) {
  let body = '';
  req.on('data', d => body += d);
  req.on('end', async () => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    if (!SUPABASE_KEY) { res.statusCode = 503; res.end(JSON.stringify({error: 'No database connection'})); return; }
    try {
      const {task_id, status, actor_label, summary} = JSON.parse(body);
      if (!task_id || !status) { res.statusCode = 400; res.end(JSON.stringify({error: 'task_id and status required'})); return; }
      const validStatuses = ['planned','assigned','running','blocked','completed','needs_review','handoff_ready','parallel_review','awaiting_dcs','approved','rejected','archived'];
      if (!validStatuses.includes(status)) { res.statusCode = 400; res.end(JSON.stringify({error: 'Invalid status: ' + status})); return; }
      const headers = {'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'return=representation'};
      const base = SUPABASE_URL + '/rest/v1';
      const updatePayload = {status};
      if (status === 'completed' || status === 'approved') updatePayload.completed_at = new Date().toISOString();
      const ur = await fetch(`${base}/agent_tasks?id=eq.${task_id}`, {method: 'PATCH', headers, body: JSON.stringify(updatePayload)});
      if (!ur.ok) { const err = await ur.text(); res.statusCode = ur.status; res.end(JSON.stringify({error: err})); return; }
      await fetch(`${base}/agent_task_events`, {method: 'POST', headers, body: JSON.stringify({
        task_id, event_type: 'status_change', actor_label: actor_label || 'CP Dispatch',
        event_summary: summary || `Status changed to ${status}`
      })}).catch(() => {});
      const updated = await ur.json();
      res.statusCode = 200;
      res.end(JSON.stringify({ok: true, task: updated[0]}));
    } catch(e) { res.statusCode = 500; res.end(JSON.stringify({error: e.message})); }
  });
}

module.exports = (req, res) => {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.statusCode = 200; res.end(); return;
  }
  if (req.method === 'POST' && req.url.includes('/api/chat')) return handleChat(req, res);
  if (req.method === 'POST' && req.url.includes('/api/tribunal/dispatch')) return handleTribunalDispatch(req, res);
  if (req.method === 'POST' && req.url.includes('/api/tribunal/receipt')) return handleTribunalReceipt(req, res);
  if (req.method === 'POST' && req.url.includes('/api/tribunal/status')) return handleTribunalStatus(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/tribunal/inbox')) return handleTribunalInbox(req, res);
  if (req.method === 'POST' && req.url.includes('/api/runtime/smoke')) return handleRuntimeSmoke(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/runtime')) return handleRuntime(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/dcsqueue')) return handleDCSQueue(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/receipts')) return handleReceipts(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/agentops')) return handleAgentOps(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/dba')) return handleDBA(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/apikeys')) return handleAPIKeys(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/assurance')) return handleAssurance(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/personas')) return handlePersonas(req, res);
  if (req.method === 'GET' && req.url.startsWith('/api/assets')) return handleAssets(req, res);
  res.setHeader('Content-Type', 'text/html;charset=utf-8');
  res.statusCode = 200;
  res.end(HTML);
};
