const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const read = (file) => fs.readFileSync(path.join(__dirname, '..', file), 'utf8');

test('ESCD chat provider selector identifies ChatGPT as OpenAI API without inventing a second provider', () => {
  const ui = read('apps/escd/web/mvp.html');
  assert.match(ui, /key==='openai'\?'ChatGPT \(OpenAI API\)'/);
  assert.match(ui, /o\.value=key/);
  assert.match(ui, /\['openai','gemini','openrouter'\]/);
  assert.match(ui, /not this ChatGPT web conversation/);
});

test('ESCD alternative chat view retains the existing OpenAI routing value', () => {
  const ui = read('apps/escd/web/app.html');
  assert.match(ui, /<option value="openai">ChatGPT \(OpenAI API\)<\/option>/);
  assert.match(ui, /not this ChatGPT web conversation/);
  assert.doesNotMatch(ui, /<option value="chatgpt_api">/);
});

test('ESCD OpenAI selection uses existing server-side provider registry and Responses API', () => {
  const runtime = read('apps/escd/runtime/mvp_data.py');
  assert.match(runtime, /get_escd_provider_runtime/);
  assert.match(runtime, /https:\/\/api\.openai\.com\/v1\/responses/);
  assert.ok(runtime.includes('"openai": {"provider": "openai"'));
  assert.doesNotMatch(read('apps/escd/web/mvp.html'), /OPENAI_API_KEY/);
  assert.doesNotMatch(read('apps/escd/web/app.html'), /OPENAI_API_KEY/);
});

test('ESCD primary and alternative chat views expose a model selector only for OpenAI', () => {
  for (const page of ['apps/escd/web/mvp.html', 'apps/escd/web/app.html']) {
    const ui = read(page);
    assert.match(ui, /id="chatModelWrap" hidden/);
    assert.match(ui, /id="chatModel" aria-label="OpenAI chat model"/);
    assert.match(ui, /function loadChatModels\(\)/);
    assert.match(ui, /providerData\.openai/);
    assert.match(ui, /chat_models\|\|\[\]/);
    assert.match(ui, /\$\('provider'\)\.onchange=loadChatModels/);
    assert.match(ui, /model:\$\('provider'\)\.value==='openai'\?\$\('chatModel'\)\.value:undefined/);
    assert.doesNotMatch(ui, /OPENAI_API_KEY/);
  }
});

test('ESCD server authorizes per-request model IDs without mutating the provider registry', () => {
  const service = read('apps/escd/runtime/mvp_data.py');
  const api = read('apps/escd/api/mvp.py');
  assert.match(service, /OPENAI_CHAT_MODELS\s*=\s*\(/);
  for (const id of ['gpt-5.6-sol', 'gpt-5.6-terra', 'gpt-5.6-luna']) {
    assert.ok(service.includes(id));
  }
  assert.match(service, /chat_model_not_approved/);
  assert.match(service, /chat_model_override_not_supported/);
  assert.match(service, /requested not in approved/);
  assert.match(service, /def chat\(provider: str, messages: list\[dict\], model_override:/);
  assert.match(api, /payload\.get\("model"\)/);
  assert.match(service, /"model": model, "input": clean/);
});
