'use strict';
// ESCD governed attachment browser controller.
(function(){
  async function sha256Hex(file){
    const buf=await file.arrayBuffer();
    const digest=await crypto.subtle.digest('SHA-256',buf);
    return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,'0')).join('');
  }

  window.uploadFileToRecord=async function(file,recType,recId){
    if(file.size>10*1024*1024)throw new Error('File exceeds 10 MB limit');
    const init=await api('/attachments/upload-url',{method:'POST',body:JSON.stringify({
      file_name:file.name,mime_type:file.type||'application/octet-stream',
      size:file.size,record_type:recType,record_id:recId
    })});
    const u=init.upload;
    if(!u||!u.signed_upload_url||!u.storage_path)throw new Error('Signed upload authorization missing');
    const uploaded=await fetch(u.signed_upload_url,{
      method:'PUT',body:file,
      headers:{'Content-Type':file.type||'application/octet-stream','x-upsert':'false'}
    });
    if(!uploaded.ok)throw new Error('Direct Storage upload failed ('+uploaded.status+')');
    const sha256=await sha256Hex(file);
    return await api('/attachments/finalize',{method:'POST',body:JSON.stringify({
      storage_path:u.storage_path,file_name:file.name,
      mime_type:file.type||'application/octet-stream',
      size:file.size,sha256,record_type:recType,record_id:recId
    })});
  };
  function attachmentsFromRecord(record){
    const out=[];
    for(const a of (Array.isArray(record&&record.evidence_refs)?record.evidence_refs:[]))if(a&&typeof a==='object')out.push(a);
    for(const a of (Array.isArray(record&&record.metadata&&record.metadata.attachments)?record.metadata.attachments:[]))if(a&&typeof a==='object')out.push(a);
    for(const line of String((record&&record.notes)||'').split('\n')){
      if(line.startsWith('[ESCD_ATTACHMENT]')){
        try{const a=JSON.parse(line.slice('[ESCD_ATTACHMENT]'.length));if(a&&typeof a==='object')out.push(a)}catch(_){}
      }
    }
    const seen=new Set();
    return out.filter(a=>a.storage_path&&!seen.has(a.storage_path)&&(seen.add(a.storage_path),true));
  }

  async function signedDownload(a){
    const d=await api('/attachments/download-url',{method:'POST',body:JSON.stringify({
      storage_path:a.storage_path,file_name:a.name||'attachment',expires_in:300
    })});
    const url=d.download&&d.download.signed_url;
    if(!url)throw new Error('Signed download URL missing');
    location.href=url;
  }

  async function removeAttachment(a,recType,recId){
    return await api('/attachments',{method:'DELETE',body:JSON.stringify({
      storage_path:a.storage_path,record_type:recType,record_id:recId
    })});
  }

})();
