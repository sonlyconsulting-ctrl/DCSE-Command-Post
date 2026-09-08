#!/usr/bin/env node
'use strict';

const { spawn } = require('child_process');

const executable = process.env.AGY_EXECUTABLE || 'agy.exe';

function run(args, timeoutMs = 30000) {
  return new Promise(resolve => {
    const started = Date.now();
    const child = spawn(executable, args, {shell:false, windowsHide:true});
    let stdout = '';
    let stderr = '';
    let timedOut = false;
    const timer = setTimeout(() => { timedOut = true; child.kill(); }, timeoutMs);
    child.stdout.on('data', d => stdout += d.toString());
    child.stderr.on('data', d => stderr += d.toString());
    child.on('error', err => { clearTimeout(timer); resolve({args, spawn_error:String(err), timed_out:timedOut, elapsed_ms:Date.now()-started}); });
    child.on('close', code => { clearTimeout(timer); resolve({args, exit_code:code, timed_out:timedOut, elapsed_ms:Date.now()-started, stdout:stdout.slice(0,4000), stderr:stderr.slice(0,4000)}); });
  });
}

(async () => {
  const tests = [];
  tests.push({name:'version', result:await run(['--version'])});
  tests.push({name:'successful_print', result:await run(['--print','Return exactly: DCSE_AGY_SMOKE_OK','--output-format','json','--print-timeout','20s','--sandbox'], 30000)});
  tests.push({name:'invalid_flag', result:await run(['--dcse-invalid-flag'])});
  tests.push({name:'bounded_timeout', result:await run(['--print','Wait for 60 seconds before responding.','--output-format','json','--print-timeout','1s','--sandbox'], 10000)});
  console.log(JSON.stringify({test_suite:'dcse-agy-cli-smoke-v1', executable, observed_at:new Date().toISOString(), tests}, null, 2));
})().catch(err => { console.error(err); process.exit(1); });
