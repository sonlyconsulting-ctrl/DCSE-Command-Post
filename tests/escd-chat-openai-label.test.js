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
