"""Refresh the standalone review artifact from the actual application UI (no live backend)."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
page = (root / 'web/mvp.html').read_text()
mock = '''<script>
sessionStorage.setItem('escd_demo_access_token','preview-only');
const previewStorage='escd-chat-persistence-demo-v1';
window.previewFailure=false;
window.fetch=async function(url,opt={}){
 const path=new URL(url,'https://preview.invalid').pathname.replace('/api/mvp','');
 const query=new URL(url,'https://preview.invalid').searchParams;
 const payload=opt.body?JSON.parse(opt.body):{};
 let rows=JSON.parse(localStorage.getItem(previewStorage)||'[]'),data={ok:true},status=200;
 if(path==='/chat')data.response={content:'Preview reply: '+payload.messages.filter(m=>m.role==='user').at(-1).content,provider:'openai',model:'preview'};
 else if(path==='/chat/save'){
   if(window.previewFailure){status=503;data={error:'Preview persistence outage'}}
   else{let row=rows.find(r=>r.id===payload.saved_chat_id||r.conversation_id===payload.conversation_id);if(!row){row={id:crypto.randomUUID()};rows.push(row)}Object.assign(row,payload,{title:payload.title||'Saved conversation',source_id:payload.conversation_id,updated_at:new Date().toISOString()});localStorage.setItem(previewStorage,JSON.stringify(rows));data.saved=row;}
 }
 else if(path==='/saved-chats')data.saved_chats=rows;
 else if(path==='/saved-chat'){data.conversation=rows.find(r=>r.id===query.get('id'));if(!data.conversation){status=404;data={error:'saved_chat_not_found'}}}
 else if(path==='/conversation')data.conversation=rows.find(r=>r.conversation_id===query.get('conversation_id'))||{messages:[]};
 else if(path==='/providers')data.providers={openai:{configured:true,enabled:true,model:'preview',catalog:[{id:'preview',name:'Preview model'}]}};
 else if(path==='/health')Object.assign(data,{providers:{openai:{configured:true,enabled:true}}});
 else if(path==='/orchestrator/threads')data.threads=[];
 else Object.assign(data,{items:[],assets:[],knowledge:[],records:[],catalog:{products:[]},governance:{overall_state:'UNKNOWN',systems:{}}});
 return {ok:status<400,status,json:async()=>data};
};
</script>'''
page = page.replace('escd_access_token', 'escd_demo_access_token').replace('escd_conversation_id', 'escd_demo_conversation_id')
page = page.replace('<script>', mock + '<script>', 1)
page = page.replace('<body>', '<body><div style="padding:12px;background:#d3af3d;color:#061324;position:relative;z-index:100">REVIEW PREVIEW — Simulated persistence on this device. No production data or provider calls.</div>')
page = page.replace('bootstrap();', "bootstrap();show('chat');")
out = root / 'docs/previews/chat_persistence_preview.html'
out.write_text(page)
print(out)
