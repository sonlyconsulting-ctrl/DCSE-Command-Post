#!/usr/bin/env node

/**
 * CTJ Package Validator
 * Validates Launch Pack or Keeper Pack ZIPs against the packaging spec
 *
 * Usage: node validate-package.js <path-to-zip>
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const AdmZip = require('adm-zip');

const zipPath = process.argv[2];

if (!zipPath) {
  console.error('Usage: node validate-package.js <path-to-zip>');
  process.exit(1);
}

if (!fs.existsSync(zipPath)) {
  console.error(`File not found: ${zipPath}`);
  process.exit(1);
}

console.log(`Validating: ${zipPath}\n`);

const findings = {
  pass: [],
  warn: [],
  fail: []
};

try {
  const zip = new AdmZip(zipPath);
  const entries = zip.getEntries();

  // STRUCTURE CHECKS
  console.log('━━ STRUCTURE ━━━');

  const isLaunchPack = entries.every(e => !e.isDirectory) && entries.length === 4 &&
    entries.some(e => e.name === '00_START_HERE.html' || e.name === '00_START_HERE.pdf') &&
    entries.some(e => e.name === '01_OPEN_PRODUCT.html') &&
    entries.some(e => e.name === '02_PRODUCT_GUIDE.html' || e.name === '02_PRODUCT_GUIDE.pdf') &&
    entries.some(e => e.name === '03_PACKAGE_MANIFEST.json');

  const isKeeperPack = entries.length === 4 &&
    entries.some(e => e.name.endsWith('.pdf')) &&
    entries.some(e => e.name.endsWith('.txt')) &&
    entries.some(e => e.name.endsWith('.json') && !e.name.includes('MANIFEST')) &&
    entries.some(e => e.name === '04_EXPORT_MANIFEST.json');

  const packageType = isLaunchPack ? 'LAUNCH_PACK' : isKeeperPack ? 'KEEPER_PACK' : 'UNKNOWN';

  if (packageType === 'UNKNOWN') {
    findings.fail.push('ZIP structure does not match Launch Pack or Keeper Pack format');
  } else {
    findings.pass.push(`✓ ZIP is a valid ${packageType}`);
  }

  console.log(`Type: ${packageType}`);
  console.log(`Files: ${entries.length}\n`);

  // FILE CHECKS
  console.log('━━ FILES ━━━');

  entries.forEach(entry => {
    const data = entry.getData();
    if (data.length === 0) {
      findings.fail.push(`File is empty: ${entry.name}`);
    } else {
      findings.pass.push(`✓ ${entry.name} (${formatBytes(data.length)})`);
    }
  });

  // MANIFEST CHECKS
  console.log(`\n━━ MANIFEST ━━━`);

  const manifestEntry = entries.find(e => e.name.includes('MANIFEST.json'));
  if (!manifestEntry) {
    findings.fail.push('Manifest file not found');
  } else {
    try {
      const manifest = JSON.parse(manifestEntry.getData().toString());
      findings.pass.push('✓ Manifest JSON parses');

      // Check manifest structure
      if (manifest.package && manifest.product && manifest.files) {
        findings.pass.push('✓ Manifest has required sections');
      } else {
        findings.fail.push('Manifest missing required sections: package, product, files');
      }

      // Validate file list matches actual files
      const manifestFiles = manifest.files.map(f => f.filename);
      const actualFiles = entries.map(e => e.name);
      const missingFromManifest = actualFiles.filter(f => !manifestFiles.includes(f));
      const extraInManifest = manifestFiles.filter(f => !actualFiles.includes(f));

      if (missingFromManifest.length > 0) {
        findings.fail.push(`Files in ZIP but not in manifest: ${missingFromManifest.join(', ')}`);
      }
      if (extraInManifest.length > 0) {
        findings.fail.push(`Files in manifest but not in ZIP: ${extraInManifest.join(', ')}`);
      }
      if (missingFromManifest.length === 0 && extraInManifest.length === 0) {
        findings.pass.push('✓ Manifest file list matches ZIP contents');
      }
    } catch (err) {
      findings.fail.push(`Manifest JSON parse error: ${err.message}`);
    }
  }

  // SECRETS SCAN
  console.log(`\n━━ SECRETS SCAN ━━━`);

  const secretPatterns = [
    /SUPABASE_KEY|SUPABASE_SERVICE_ROLE/gi,
    /API_KEY|SECRET_KEY|PRIVATE_KEY/gi,
    /password|passwd|pwd/gi,
    /Bearer\s+[a-zA-Z0-9_-]{20,}/gi,
    /sk_test_|sk_live_/gi
  ];

  let secretsFound = false;
  entries.forEach(entry => {
    if (entry.name.endsWith('.json') || entry.name.endsWith('.html') || entry.name.endsWith('.txt')) {
      const content = entry.getData().toString();
      secretPatterns.forEach(pattern => {
        if (pattern.test(content)) {
          findings.fail.push(`Potential secret in ${entry.name}: ${pattern}`);
          secretsFound = true;
        }
      });
    }
  });

  if (!secretsFound) {
    findings.pass.push('✓ No obvious secrets detected');
  }

  // LAUNCHER CHECK
  console.log(`\n━━ LAUNCHER ━━━`);

  const launcherEntry = entries.find(e => e.name === '01_OPEN_PRODUCT.html');
  if (launcherEntry) {
    const launcherContent = launcherEntry.getData().toString();
    if (launcherContent.includes('<button') || launcherContent.includes('class="cta-button"')) {
      findings.pass.push('✓ Launcher has CTA button');
    }
    if (!launcherContent.includes('secret') && !launcherContent.includes('password')) {
      findings.pass.push('✓ Launcher appears to have no embedded credentials');
    }
  }

  // SUMMARY
  console.log(`\n${'━'.repeat(50)}`);
  console.log(`VALIDATION SUMMARY`);
  console.log(`${'━'.repeat(50)}\n`);

  if (findings.pass.length > 0) {
    console.log(`✓ PASS (${findings.pass.length})`);
    findings.pass.forEach(f => console.log(`  ${f}`));
  }

  if (findings.warn.length > 0) {
    console.log(`\n⚠ WARNINGS (${findings.warn.length})`);
    findings.warn.forEach(f => console.log(`  ${f}`));
  }

  if (findings.fail.length > 0) {
    console.log(`\n✗ FAILURES (${findings.fail.length})`);
    findings.fail.forEach(f => console.log(`  ${f}`));
    process.exit(1);
  } else {
    console.log(`\n${'━'.repeat(50)}`);
    console.log(`✓ PACKAGE VALID`);
    console.log(`${'━'.repeat(50)}`);
  }
} catch (err) {
  console.error(`Validation error: ${err.message}`);
  process.exit(1);
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}
