#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const read = (p) => fs.readFileSync(path.join(root, p), 'utf8');
const checks = [];
const check = (name, ok, detail = '') => checks.push({ name, ok: Boolean(ok), detail });

const worker = read('workers/claude-reviewer-operational.js');
const tokenBroker = read('supabase/functions/v7-worker-token/index.ts');
const resultBridge = read('supabase/functions/v7-result-bridge/index.ts');
const rollback = read('supabase/rollback/v7_restricted_rpc_rollback.sql');
const authTombstone = read('supabase/decommission/v7-worker-auth/index.ts');
const archivedAuth = read('supabase/rollback/v7-worker-auth-v1/index.ts');
const migrations = fs.readdirSync(path.join(root, 'supabase', 'migrations'))
  .filter((name) => /_v7_/.test(name));

check('canonical worker rejects missing bounded credentials', /SUPABASE_ANON_KEY/.test(worker) && /WORKER_ENROLLMENT_SECRET/.test(worker));
check('canonical worker does not request service role', !/SUPABASE_SERVICE_ROLE_KEY/.test(worker));
check('token broker requires enrollment secret', /enrollment_secret/.test(tokenBroker) && /v7_verify_worker_enrollment/.test(tokenBroker));
check('token broker does not sign caller-asserted JWTs', !/SignJWT|JWT_SECRET/.test(tokenBroker));
check('result bridge enforces service-role caller', /role !== "service_role"/.test(resultBridge));
check('unsafe v7-worker-auth source excluded from canonical tree', !fs.existsSync(path.join(root, 'supabase/functions/v7-worker-auth/index.ts')));
check('v7-worker-auth decommission payload is inert', /status:\s*410/.test(authTombstone) && /endpoint_decommissioned/.test(authTombstone) && !/SignJWT|JWT_SECRET|SUPABASE_SERVICE_ROLE_KEY/.test(authTombstone));
check('v7-worker-auth v1 source is isolated as archive', /Supabase Edge Function: v7-worker-auth/.test(archivedAuth) && /SignJWT/.test(archivedAuth));
check('all thirteen communication migrations present', migrations.length === 13, `count=${migrations.length}`);
check('rollback destructive dc_event_id rewrite remains commented', /-- update v7_worker\.result_submission set dc_event_id = null;/.test(rollback));
check('v6.9 directory remains present', fs.existsSync(path.join(root, 'v6.9')));

for (const item of checks) {
  process.stdout.write(`${item.ok ? 'PASS' : 'FAIL'} ${item.name}${item.detail ? ` (${item.detail})` : ''}\n`);
}

const failed = checks.filter((item) => !item.ok);
process.stdout.write(`SUMMARY passed=${checks.length - failed.length} failed=${failed.length}\n`);
if (failed.length) process.exit(1);
