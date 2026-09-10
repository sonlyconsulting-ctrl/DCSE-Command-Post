const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(require('node:path').join(__dirname, '../apps/escd/web/mvp.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function setup(failKey = false) {
  const elements = {};
  for (const id of ['settingsProvider','providerSecret','providerModel','providerTimeout','providerTokens','providerEnabled','providerThinking','providerAdminStatus','saveProviderConfig','saveProviderSecret']) elements[id] = {value:'',textContent:'',disabled:false};
  Object.assign(elements.settingsProvider,{value:'openai'});
  Object.assign(elements.providerSecret,{value:'test-only-provider-value'});
  const calls=[];
  const context=vm.createContext({$:id=>elements[id], providerData:{openai:{model:'test-model',enabled:true}}, api:async (path,opt)=>{
    calls.push({path,body:JSON.parse(opt.body)});
    if(path==='/provider-secret' && failKey) throw new Error('Vault unavailable');
    return {provider:{configured:true,credential_source:'vault'}};
  }});
  vm.runInContext(script.slice(script.indexOf('function providerLabel'),script.indexOf('async function send()')),context);
  vm.runInContext('loadProviders = async function(){loadSettingsForm()}; loadSettingsForm();',context);
  return {context,elements,calls};
}

test('entire shipped browser script parses',()=>assert.doesNotThrow(()=>new vm.Script(script)));
test('Save settings persists an entered key and keeps success visible',async()=>{
  const {context,elements,calls}=setup();
  await context.saveProviderConfig();
  assert.deepEqual(calls.map(x=>x.path),['/provider-config','/provider-secret']);
  assert.equal(calls[1].body.secret,'test-only-provider-value');
  assert.equal(elements.providerSecret.value,'');
  assert.match(elements.providerAdminStatus.textContent,/configured via vault/);
});
test('a failed key save preserves the unsaved field for retry and reports partial success',async()=>{
  const {context,elements}=setup(true);
  await context.saveProviderConfig();
  assert.equal(elements.providerSecret.value,'test-only-provider-value');
  assert.match(elements.providerAdminStatus.textContent,/Settings saved; key was not verified/);
  assert.equal(elements.saveProviderConfig.disabled,false);
});
test('Save key only does not change model configuration',async()=>{
  const {context,elements,calls}=setup();
  await context.saveProviderSecret();
  assert.deepEqual(calls.map(x=>x.path),['/provider-secret']);
  assert.match(elements.providerAdminStatus.textContent,/Key stored in Vault/);
});
test('a plain settings save does not replace the stored key',async()=>{
  const {context,elements,calls}=setup(); elements.providerSecret.value='';
  await context.saveProviderConfig();
  assert.deepEqual(calls.map(x=>x.path),['/provider-config']);
});
test('OpenRouter is included in the chat provider dropdown',async()=>{
  const elements = {};
  for (const id of ['provider','settingsProvider','providerSecret','providerModel','providerTimeout','providerTokens','providerEnabled','providerThinking','providerAdminStatus','saveProviderConfig','saveProviderSecret']) elements[id] = {value:'',textContent:'',disabled:false,options:[],replaceChildren:function(){this.options=[]},append:function(opt){this.options.push(opt)}};
  Object.assign(elements.settingsProvider,{value:'openrouter'});
  const context=vm.createContext({$:id=>elements[id], el:(tag,text)=>{return {tag,text,value:''}}, providerData:{openrouter:{model:'openrouter/auto',enabled:false,configured:false}}, api:async()=>({providers:{openrouter:{enabled:false}}})});
  vm.runInContext(script.slice(script.indexOf('function providerLabel'),script.indexOf('async function send()')),context);
  context.populateProviderDropdown();
  const optionValues = elements.provider.options.map(o=>o.value);
  assert.ok(optionValues.includes('openrouter'));
  assert.ok(optionValues.includes('openai'));
  assert.ok(optionValues.includes('gemini'));
});
