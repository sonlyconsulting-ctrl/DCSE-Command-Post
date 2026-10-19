#!/usr/bin/env node
/**
 * DCSE Sovereign Secrets Vault & Key Lifecycle Dispatcher
 * File: scripts/governance/dcse_vault.mjs
 * 
 * Provides automated, zero-leakage secrets management across:
 *   1. Supabase Edge Functions (ctj-commerce)
 *   2. ESCD AI Orchestrator & Multi-Node Inference Fabric
 *   3. Cloud Hosting (Vercel / Netlify)
 *   4. Open-Source Sanitize & Failsafe Boundaries
 *   5. API Key Recycling & Rotation Audit Trail
 *   6. Automated Stripe Live Commerce Provisioning ($1 verification & production)
 */

import { readFileSync, writeFileSync, existsSync, unlinkSync, mkdirSync, appendFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { execSync } from 'node:child_process';

const KEYSTORE_CANDIDATES = [
  'C:\\DS All Things\\DCSE_Command_Center\\DCSE Tech Only\\DCSE 5 env Api keys.env.txt',
  'C:\\DS All Things\\DCSE_Command_Center\\DCSE Tech Only\\DCSE 5 env Api keys.env'
];
const ESCD_PROD_ENV = 'C:\\DS All Things\\DCSE_Command_Center\\apps\\escd\\.env.production.local';
const AUDIT_LOG_PATH = 'C:\\DS All Things\\DCSE_Command_Center\\governance\\registry\\dcse_secrets_audit.jsonl';

// Categorization schemas
const SCHEMAS = {
  ai: ['ANTHROPIC_API_KEY', 'GOOGLE_API_KEY', 'OPENAI_API_KEY', 'OPENROUTER_API_KEY', 'OLLAMA_HOST'],
  commerce: ['STRIPE_SECRET_KEY', 'STRIPE_MODE', 'STRIPE_WEBHOOK_SECRET', 'CTJ_PRICE_MAP', 'CTJ_ASSET_MAP', 'CTJ_PRICING_PLAN', 'CTJ_ALLOW_PROMOTION_CODES'],
  database: ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY', 'NEXT_PUBLIC_SUPABASE_URL', 'NEXT_PUBLIC_SUPABASE_ANON_KEY'],
  hosting: ['VERCEL_TOKEN', 'VERCEL_OIDC_TOKEN', 'NETLIFY_AUTH_TOKEN', 'WIX_API_KEY']
};

export function maskSecret(val) {
  if (!val || typeof val !== 'string') return '[EMPTY]';
  const clean = val.trim();
  if (clean.length <= 8) return '********';
  const prefix = clean.slice(0, Math.min(8, Math.floor(clean.length / 3)));
  const suffix = clean.slice(-4);
  return `${prefix}...${suffix}`;
}

export function parseKeystore(filePath) {
  let target = filePath;
  if (!target) {
    for (const cand of KEYSTORE_CANDIDATES) {
      if (existsSync(cand)) {
        target = cand;
        break;
      }
    }
  }

  if (!target || !existsSync(target)) {
    throw new Error(`Keystore file not found. Checked: ${KEYSTORE_CANDIDATES.join(', ')}`);
  }

  const content = readFileSync(target, 'utf8');
  const lines = content.split(/\r?\n/);
  const store = {};

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#') || line.startsWith('+++++')) continue;

    let key = '';
    let val = '';

    if (line.includes('=')) {
      const idx = line.indexOf('=');
      key = line.slice(0, idx).trim();
      val = line.slice(idx + 1).trim();
    } else if (line.includes(':')) {
      const idx = line.indexOf(':');
      key = line.slice(0, idx).trim();
      val = line.slice(idx + 1).trim();
    }

    // Strip wrapping quotes
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }

    if (key) {
      const normKey = key.toUpperCase().replace(/\s+/g, '_');
      if (normKey.includes('OPENAI') && !store['OPENAI_API_KEY']) {
        store['OPENAI_API_KEY'] = val;
      } else if (normKey.includes('ANTHROPIC')) {
        store['ANTHROPIC_API_KEY'] = val;
      } else if (normKey.includes('GOOGLE')) {
        store['GOOGLE_API_KEY'] = val;
      } else if (normKey.includes('OPENROUTER')) {
        store['OPENROUTER_API_KEY'] = val;
      } else if (normKey.includes('VERCEL')) {
        store['VERCEL_TOKEN'] = val;
      } else if (normKey.includes('STRIPE')) {
        store['STRIPE_SECRET_KEY'] = val;
      } else {
        store[normKey] = val;
      }
    }
  }

  // Fallback to ESCD production local environment for Supabase credentials if missing
  if (existsSync(ESCD_PROD_ENV)) {
    try {
      const escdContent = readFileSync(ESCD_PROD_ENV, 'utf8');
      for (const line of escdContent.split(/\r?\n/)) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;
        const [k, ...v] = trimmed.split('=');
        const keyName = k.trim().toUpperCase();
        const value = v.join('=').trim().replace(/^['"]|['"]$/g, '');
        if (keyName && !store[keyName]) {
          store[keyName] = value;
        }
      }
    } catch {
      // Ignore if unreadable
    }
  }

  return store;
}

export function logAudit(action, service, details = {}) {
  try {
    const dir = dirname(AUDIT_LOG_PATH);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    const entry = {
      timestamp: new Date().toISOString(),
      action,
      service,
      details,
      node: process.env.COMPUTERNAME || 'LOCAL_NODE'
    };
    appendFileSync(AUDIT_LOG_PATH, JSON.stringify(entry) + '\n');
  } catch (err) {
    console.error(`[AUDIT_LOG_WARN] Failed to write audit log: ${err.message}`);
  }
}

export function printStatus(store) {
  console.log('\n======================================================');
  console.log('       DCSE SOVEREIGN SECRETS STATUS AUDIT            ');
  console.log('======================================================\n');

  for (const [category, keys] of Object.entries(SCHEMAS)) {
    console.log(`[DOMAIN: ${category.toUpperCase()}]`);
    for (const key of keys) {
      const val = store[key];
      const status = val ? 'ACTIVE' : 'MISSING';
      const masked = maskSecret(val);
      console.log(`  - ${key.padEnd(28)} : [${status.padEnd(7)}] ${masked}`);
    }
    console.log('');
  }
}

export function generateSanitizedTemplate(store, outputPath) {
  const lines = [
    '# ===================================================================',
    '# DCSE OPEN-SOURCE / CLIENT-SAFE ENVIRONMENT TEMPLATE',
    '# DO NOT COMMIT REAL CREDENTIALS. COPY TO .env.local AND INJECT VALUES.',
    '# Generated by: dcse_vault.mjs',
    `# Date: ${new Date().toISOString()}`,
    '# ===================================================================\n'
  ];

  for (const [category, keys] of Object.entries(SCHEMAS)) {
    lines.push(`\n# --- ${category.toUpperCase()} ---`);
    for (const key of keys) {
      let placeholder = 'your_' + key.toLowerCase() + '_here';
      if (key === 'STRIPE_MODE') placeholder = 'test';
      if (key === 'CTJ_PRICING_PLAN') placeholder = 'verification_1usd';
      if (key === 'CTJ_ALLOW_PROMOTION_CODES') placeholder = 'false';
      if (key.includes('MAP')) placeholder = '{}';
      lines.push(`${key}="${placeholder}"`);
    }
  }

  writeFileSync(outputPath, lines.join('\n') + '\n');
  console.log(`[SUCCESS] Sanitized environment template generated at: ${outputPath}`);
}

export function generatePricingMap(plan = 'verification_1usd', customPriceIds = {}) {
  const offers = ['SCA', 'CTJ-PART-1', 'CTJ-PART-2', 'CTJ-PART-3', 'PARTS-BUNDLE', 'CTJ-UNIFIED'];
  const map = {};

  for (const offer of offers) {
    if (customPriceIds[offer]) {
      map[offer] = customPriceIds[offer];
    } else if (plan === 'verification_1usd') {
      map[offer] = `price_test_1usd_${offer.toLowerCase().replace(/[^a-z0-9]/g, '_')}`;
    } else {
      map[offer] = `price_live_${offer.toLowerCase().replace(/[^a-z0-9]/g, '_')}`;
    }
  }

  return map;
}

// -------------------------------------------------------------
// Stripe Live Automated Provisioning ($1 Verification & Prod)
// -------------------------------------------------------------

async function stripeApi(apiKey, endpoint, options = {}) {
  const url = `https://api.stripe.com/v1/${endpoint.replace(/^\//, '')}`;
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    ...options.headers
  };
  const res = await fetch(url, { ...options, headers });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error?.message || `Stripe API error (${res.status}) on /${endpoint}`);
  }
  return data;
}

export async function provisionCommerce(store, options = {}) {
  const stripeKey = store['STRIPE_SECRET_KEY'];
  if (!stripeKey || (!stripeKey.startsWith('rk_live_') && !stripeKey.startsWith('sk_live_'))) {
    throw new Error('Valid Stripe live secret key (rk_live_... or sk_live_...) not found in keystore.');
  }

  const projectRef = options.projectRef || 'nevgdyfpxdaloacuutal';
  const plan = options.plan || 'verification_1usd';
  const cents = plan === 'verification_1usd' ? 100 : (options.cents || 100);

  console.log('\n======================================================');
  console.log('       DCSE COMMERCE AUTOMATED PROVISIONING           ');
  console.log('======================================================');
  console.log(`Target Supabase Project : ${projectRef}`);
  console.log(`Pricing Mode            : ${plan} (${cents} cents = $${(cents/100).toFixed(2)})`);
  console.log(`Stripe Key Fingerprint  : ${maskSecret(stripeKey)}\n`);

  // 1. Define CTJ Products Catalog
  const targetProducts = [
    { sku: 'SCA', name: 'Sonly Cognitive Assessment (SCA)' },
    { sku: 'CTJ-PART-1', name: "The Critical Thinker's Journey - Part 1" },
    { sku: 'CTJ-PART-2', name: "The Critical Thinker's Journey - Part 2" },
    { sku: 'CTJ-PART-3', name: "The Critical Thinker's Journey - Part 3" },
    { sku: 'PARTS-BUNDLE', name: 'CTJ Parts 1-3 Comprehensive Bundle' },
    { sku: 'CTJ-UNIFIED', name: 'CTJ Unified Suite' }
  ];

  // 2. Fetch existing Stripe Products & Prices
  console.log('[1/4] Querying existing Stripe live catalog...');
  const existingProducts = (await stripeApi(stripeKey, 'products?limit=100')).data || [];
  const existingPrices = (await stripeApi(stripeKey, 'prices?limit=100&active=true')).data || [];

  const priceMap = {};

  for (const item of targetProducts) {
    // Locate or create product
    let prod = existingProducts.find(p => p.metadata?.sku === item.sku || p.name === item.name);
    if (!prod) {
      console.log(`  + Creating Product: ${item.name} (${item.sku})...`);
      const body = new URLSearchParams();
      body.set('name', item.name);
      body.set('metadata[sku]', item.sku);
      body.set('metadata[app]', 'CTJ');
      prod = await stripeApi(stripeKey, 'products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body
      });
    }

    // Locate or create price for this product and tier
    let price = existingPrices.find(pr => pr.product === prod.id && pr.unit_amount === cents && pr.currency === 'usd' && pr.type === 'one_time');
    if (!price) {
      console.log(`  + Creating Price: $${(cents/100).toFixed(2)} USD for ${item.sku}...`);
      const body = new URLSearchParams();
      body.set('product', prod.id);
      body.set('unit_amount', String(cents));
      body.set('currency', 'usd');
      body.set('metadata[plan]', plan);
      price = await stripeApi(stripeKey, 'prices', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body
      });
    } else {
      console.log(`  ✔ Found existing Price: ${price.id} ($${(cents/100).toFixed(2)}) for ${item.sku}`);
    }

    priceMap[item.sku] = price.id;
  }

  console.log('\n[2/4] Assembled CTJ_PRICE_MAP:');
  console.log(JSON.stringify(priceMap, null, 2));

  // 3. Register or Retrieve Webhook Endpoint
  const webhookUrl = `https://${projectRef}.supabase.co/functions/v1/ctj-commerce/webhook`;
  console.log(`\n[3/4] Ensuring live webhook endpoint at: ${webhookUrl}`);
  
  const existingWebhooks = (await stripeApi(stripeKey, 'webhook_endpoints?limit=50')).data || [];
  let webhookEndpoint = existingWebhooks.find(w => w.url === webhookUrl && w.status === 'enabled');
  let webhookSecret = '';

  if (!webhookEndpoint) {
    console.log('  + Creating new Stripe live webhook endpoint...');
    const body = new URLSearchParams();
    body.set('url', webhookUrl);
    body.set('description', 'CTJ Commerce Webhook Live');
    body.set('enabled_events[0]', 'checkout.session.completed');
    body.set('enabled_events[1]', 'checkout.session.async_payment_succeeded');
    body.set('enabled_events[2]', 'charge.refunded');
    webhookEndpoint = await stripeApi(stripeKey, 'webhook_endpoints', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body
    });
    webhookSecret = webhookEndpoint.secret;
    console.log(`  ✔ Webhook created! Secret: ${maskSecret(webhookSecret)}`);
  } else {
    console.log(`  ✔ Webhook endpoint already exists (${webhookEndpoint.id}).`);
    webhookSecret = store['STRIPE_WEBHOOK_SECRET'] || '';
    if (!webhookSecret) {
      console.log('  ℹ (If webhook was previously created, ensure signing secret whsec_... is in your keystore).');
    }
  }

  // 4. Inject Secrets into Supabase
  console.log('\n[4/4] Setting secrets in Supabase via CLI...');
  await syncTarget('supabase-commerce', store, {
    projectRef,
    plan,
    priceMap,
    webhookSecret
  });

  // 5. Generate Real $1 Live Checkout Session
  console.log('\nGenerating real $1 live Checkout Session for immediate test...');
  const sessionBody = new URLSearchParams();
  sessionBody.set('mode', 'payment');
  sessionBody.set('line_items[0][price]', priceMap['SCA']);
  sessionBody.set('line_items[0][quantity]', '1');
  sessionBody.set('success_url', 'https://sonlyconsulting.com/ctj/?session_id={CHECKOUT_SESSION_ID}#/delivery');
  sessionBody.set('cancel_url', 'https://sonlyconsulting.com/ctj/#/cart');
  sessionBody.set('metadata[plan]', plan);
  sessionBody.set('metadata[test_run]', 'verification_1usd');

  const session = await stripeApi(stripeKey, 'checkout/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: sessionBody
  });

  console.log('\n======================================================');
  console.log('       PROVISIONING COMPLETE - READY TO TEST          ');
  console.log('======================================================');
  console.log(`\nDirect Purchase Link ($1.00 Verification):`);
  console.log(`👉 ${session.url}\n`);

  logAudit('PROVISION_COMMERCE', 'stripe-supabase', {
    projectRef,
    plan,
    priceMap,
    sessionId: session.id
  });

  return { priceMap, webhookEndpoint, sessionUrl: session.url };
}

export async function syncTarget(target, store, options = {}) {
  if (target === 'supabase-commerce') {
    const projectRef = options.projectRef || 'nevgdyfpxdaloacuutal';
    const plan = options.plan || store['CTJ_PRICING_PLAN'] || 'verification_1usd';

    const secrets = {
      STRIPE_SECRET_KEY: store['STRIPE_SECRET_KEY'],
      STRIPE_MODE: store['STRIPE_MODE'] || 'live',
      STRIPE_WEBHOOK_SECRET: options.webhookSecret || store['STRIPE_WEBHOOK_SECRET'],
      CTJ_PRICING_PLAN: plan,
      CTJ_ALLOW_PROMOTION_CODES: store['CTJ_ALLOW_PROMOTION_CODES'] || 'true',
      CTJ_PRICE_MAP: options.priceMap ? JSON.stringify(options.priceMap) : (store['CTJ_PRICE_MAP'] || JSON.stringify(generatePricingMap(plan))),
      CTJ_ASSET_MAP: store['CTJ_ASSET_MAP'] || JSON.stringify({
        'SCA': { download: 'SCA/SCA-Full-Assessment.pdf', content: 'SCA/index.html' },
        'CTJ-PART-1': { download: 'CTJ-PART-1/Part-1-Foundations.pdf', content: 'CTJ-PART-1/index.html' },
        'CTJ-PART-2': { download: 'CTJ-PART-2/Part-2-Methods.pdf', content: 'CTJ-PART-2/index.html' },
        'CTJ-PART-3': { download: 'CTJ-PART-3/Part-3-Mastery.pdf', content: 'CTJ-PART-3/index.html' },
        'CTJ-UNIFIED': { download: 'CTJ-UNIFIED/CTJ-Unified-Suite.zip', content: 'CTJ-UNIFIED/index.html' }
      }),
      CTJ_REVIEW_ORIGINS: store['CTJ_REVIEW_ORIGINS'] || 'https://sonlyconsulting.com',
      CTJ_PRIVATE_BUCKET: store['CTJ_PRIVATE_BUCKET'] || 'sc-ctj-deliverables',
      SUPABASE_URL: store['SUPABASE_URL'] || 'https://nevgdyfpxdaloacuutal.supabase.co',
      SUPABASE_ANON_KEY: store['SUPABASE_ANON_KEY'],
      SUPABASE_SERVICE_ROLE_KEY: store['SUPABASE_SERVICE_ROLE_KEY']
    };

    const validPairs = Object.entries(secrets).filter(([_, v]) => typeof v === 'string' && v.trim().length > 0);

    console.log(`[SUPABASE_COMMERCE] Injecting ${validPairs.length} secrets into project: ${projectRef}`);
    validPairs.forEach(([k, v]) => console.log(`  - ${k.padEnd(28)} : ${maskSecret(v)}`));

    const tempFile = resolve(process.cwd(), '.tmp_supabase_commerce.env');
    const content = validPairs.map(([k, v]) => `${k}="${v.replace(/"/g, '\\"')}"`).join('\n');
    writeFileSync(tempFile, content, { mode: 0o600 });

    try {
      execSync(`supabase secrets set --env-file "${tempFile}" --project-ref ${projectRef}`, { stdio: 'inherit' });
      console.log('[SUCCESS] Supabase secrets successfully updated.');
      logAudit('SYNC', 'supabase-commerce', { projectRef, plan, keysSet: validPairs.map(([k]) => k) });
    } catch (err) {
      console.error(`[ERROR] Supabase CLI execution: ${err.message}`);
    } finally {
      if (existsSync(tempFile)) unlinkSync(tempFile);
    }
  } else if (target === 'escd') {
    const escdEnvPath = 'C:\\DS All Things\\DCSE_Command_Center\\apps\\escd\\.env.local';
    const lines = [
      '# ESCD Runtime Auto-Injected Keystore',
      `# Injected at: ${new Date().toISOString()}`,
      `ANTHROPIC_API_KEY="${store['ANTHROPIC_API_KEY'] || ''}"`,
      `GOOGLE_API_KEY="${store['GOOGLE_API_KEY'] || ''}"`,
      `OPENAI_API_KEY="${store['OPENAI_API_KEY'] || ''}"`,
      `OPENROUTER_API_KEY="${store['OPENROUTER_API_KEY'] || ''}"`,
      `SUPABASE_URL="${store['SUPABASE_URL'] || ''}"`,
      `SUPABASE_SERVICE_ROLE_KEY="${store['SUPABASE_SERVICE_ROLE_KEY'] || ''}"`
    ];
    writeFileSync(escdEnvPath, lines.join('\n') + '\n', { mode: 0o600 });
    console.log(`[SUCCESS] ESCD runtime credentials injected to: ${escdEnvPath}`);
    logAudit('SYNC', 'escd', { targetPath: escdEnvPath });
  } else {
    throw new Error(`Unknown sync target: ${target}`);
  }
}

// CLI Command Router
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'status';

  let keystorePath = null;
  const fileArgIdx = args.indexOf('--file');
  if (fileArgIdx !== -1 && args[fileArgIdx + 1]) {
    keystorePath = args[fileArgIdx + 1];
  }

  let store = {};
  try {
    store = parseKeystore(keystorePath);
  } catch (err) {
    console.error(`[WARN] Could not load master keystore: ${err.message}`);
  }

  switch (command) {
    case 'status':
      printStatus(store);
      break;

    case 'provision-commerce': {
      const planIdx = args.indexOf('--plan');
      const plan = planIdx !== -1 && args[planIdx + 1] ? args[planIdx + 1] : 'verification_1usd';
      await provisionCommerce(store, { plan });
      break;
    }

    case 'sanitize': {
      const outIdx = args.indexOf('--output');
      const outPath = outIdx !== -1 && args[outIdx + 1] ? args[outIdx + 1] : '.env.example';
      generateSanitizedTemplate(store, outPath);
      break;
    }

    case 'pricing': {
      const planIdx = args.indexOf('--plan');
      const plan = planIdx !== -1 && args[planIdx + 1] ? args[planIdx + 1] : 'verification_1usd';
      console.log(`\n--- CTJ_PRICE_MAP Template for Plan: [${plan}] ---`);
      console.log(JSON.stringify(generatePricingMap(plan), null, 2));
      break;
    }

    case 'sync': {
      const targetIdx = args.indexOf('--target');
      if (targetIdx === -1 || !args[targetIdx + 1]) {
        console.error('Error: --target <supabase-commerce|escd> is required.');
        process.exit(1);
      }
      const target = args[targetIdx + 1];
      const planIdx = args.indexOf('--plan');
      const plan = planIdx !== -1 && args[planIdx + 1] ? args[planIdx + 1] : 'verification_1usd';
      await syncTarget(target, store, { plan });
      break;
    }

    default:
      console.log(`Usage: node dcse_vault.mjs <status|provision-commerce|sync|sanitize|pricing> [--target <target>] [--plan <plan>]`);
  }
}

main().catch(err => {
  console.error('[FATAL]', err);
  process.exit(1);
});
