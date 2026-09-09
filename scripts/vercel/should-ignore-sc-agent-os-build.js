'use strict';

const {execFileSync} = require('node:child_process');

const currentSha = process.env.VERCEL_GIT_COMMIT_SHA || '';
const previousSha = process.env.VERCEL_GIT_PREVIOUS_SHA || '';

const relevantPrefixes = [
  'api/',
  'apps/sc-agent-os/',
  'tests/sc-agent-os-',
  'governance/v7.2/implementations/DCSE_DDNA_CONSUMER_CUTOVER',
  'governance/v7.2/implementations/DCSE_DDNA_PHYSICAL_TRANSFER',
  'scripts/vercel/should-ignore-sc-agent-os-build.js',
  'vercel.json'
];

function normalizePath(path) {
  return String(path || '').trim().replace(/\\/g, '/');
}

function changedFiles() {
  if (previousSha && currentSha && previousSha !== currentSha) {
    const output = execFileSync('git', ['diff', '--name-only', previousSha, currentSha], {encoding: 'utf8'});
    return output.split(/\r?\n/).map(normalizePath).filter(Boolean);
  }

  if (currentSha) {
    const output = execFileSync('git', ['show', '--pretty=', '--name-only', currentSha], {encoding: 'utf8'});
    return output.split(/\r?\n/).map(normalizePath).filter(Boolean);
  }

  return null;
}

function hasRelevantChange(files) {
  return files.some(file => relevantPrefixes.some(prefix => file === prefix.replace(/\/$/, '') || file.startsWith(prefix)));
}

try {
  const files = changedFiles();
  if (!files) {
    console.log('Vercel ignore check: no commit metadata available; building for validation safety.');
    process.exit(1);
  }

  if (hasRelevantChange(files)) {
    console.log('Vercel ignore check: SC Agent OS/DDNA runtime change detected; building.');
    process.exit(1);
  }

  console.log('Vercel ignore check: no SC Agent OS/DDNA runtime change detected; ignoring deployment.');
  process.exit(0);
} catch (error) {
  console.log(`Vercel ignore check: unable to evaluate changed files (${error.message}); building for validation safety.`);
  process.exit(1);
}
