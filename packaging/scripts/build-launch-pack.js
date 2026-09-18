#!/usr/bin/env node

/**
 * CTJ Launch Pack Builder
 * Generates a complete Launch Pack ZIP for a specified product
 *
 * Usage: node build-launch-pack.js <product-id> [output-dir]
 * Example: node build-launch-pack.js unified ./dist
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const archiver = require('archiver');

// Parse arguments
const productId = process.argv[2];
const outputDir = process.argv[3] || './dist';

if (!productId) {
  console.error('Usage: node build-launch-pack.js <product-id> [output-dir]');
  console.error('Example: node build-launch-pack.js unified ./dist');
  process.exit(1);
}

// Load configuration
const configPath = path.join(__dirname, '..', 'products.config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const contentPath = path.join(__dirname, '..', 'launch-packs', productId, 'content.json');

if (!fs.existsSync(contentPath)) {
  console.error(`Content file not found: ${contentPath}`);
  process.exit(1);
}

const content = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
const product = config.products.find(p => p.id === productId);

if (!product) {
  console.error(`Product not found: ${productId}`);
  process.exit(1);
}

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Helper to compute file hash
function computeHash(filePath) {
  return crypto
    .createHash('sha256')
    .update(fs.readFileSync(filePath))
    .digest('hex');
}

// Build file path
const timestamp = new Date().toISOString().split('T')[0].replace(/-/g, '');
const zipFilename = `CTJ-${product.id.toUpperCase()}-Launch-Pack-v1.0.0.zip`;
const zipPath = path.join(outputDir, zipFilename);

console.log(`Building Launch Pack for: ${product.name}`);
console.log(`Output: ${zipPath}\n`);

// Create temporary directory for files
const tempDir = path.join(outputDir, `.temp-${productId}-${Date.now()}`);
fs.mkdirSync(tempDir, { recursive: true });

try {
  // 1. Generate 00_START_HERE.pdf (as HTML for now; real PDF generation would use puppeteer/pdfkit)
  const startHereTemplate = fs.readFileSync(
    path.join(__dirname, '..', 'launch-packs', 'templates', '00_START_HERE.html'),
    'utf8'
  );
  const startHereHtml = interpolate(startHereTemplate, {
    PRODUCT_NAME: product.name,
    PRODUCT_SUBTITLE: product.subtitle || '',
    ROLE: content.product.role,
    WHAT_YOU_BOUGHT: content.guide.what_you_bought,
    EFFORT: content.guide.effort,
    WHAT_YOU_PRODUCE: content.guide.what_you_produce,
    SUPPORT_URL: content.guide.support_url,
    GENERATED_DATE: new Date().toLocaleDateString()
  });
  fs.writeFileSync(path.join(tempDir, '00_START_HERE.html'), startHereHtml);
  console.log('✓ Generated 00_START_HERE.html');

  // 2. Generate 01_OPEN_PRODUCT.html
  const launcherTemplate = fs.readFileSync(
    path.join(__dirname, '..', 'launch-packs', 'templates', '01_OPEN_PRODUCT.html'),
    'utf8'
  );
  const launcherHtml = interpolate(launcherTemplate, {
    PRODUCT_NAME: product.name,
    PRODUCT_SUBTITLE: product.subtitle || '',
    ROLE: content.product.role,
    PRODUCT_ROLE_DESCRIPTION: content.launcher.role_description,
    EFFORT: content.guide.effort,
    WHAT_YOU_PRODUCE: content.guide.what_you_produce,
    PRODUCT_URL: `https://ctj.sonlyconsulting.com/${productId}`,
    PRODUCT_DISPLAY_URL: `ctj.sonlyconsulting.com/${productId}`
  });
  fs.writeFileSync(path.join(tempDir, '01_OPEN_PRODUCT.html'), launcherHtml);
  console.log('✓ Generated 01_OPEN_PRODUCT.html');

  // 3. Generate 02_PRODUCT_GUIDE.pdf (as HTML for now)
  const guideTemplate = fs.readFileSync(
    path.join(__dirname, '..', 'launch-packs', 'templates', '02_PRODUCT_GUIDE.html'),
    'utf8'
  );
  const guideHtml = interpolate(guideTemplate, {
    PRODUCT_NAME: product.name,
    PRODUCT_SUBTITLE: product.subtitle || '',
    ROLE: content.product.role,
    EFFORT: content.guide.effort,
    PRODUCT_OVERVIEW: content.guide.overview,
    WHAT_YOU_DO: content.guide.what_you_do,
    WHAT_YOU_PRODUCE: content.guide.what_you_produce,
    SAVE_RESUME_BEHAVIOR: content.guide.save_resume_behavior,
    PRIVACY_STATEMENT: content.guide.privacy_statement,
    RESET_BEHAVIOR: content.guide.reset_behavior,
    PRODUCT_BOUNDARIES: content.guide.product_boundaries,
    ACCESSIBILITY_STATEMENT: content.guide.accessibility_statement,
    SUPPORT_URL: content.guide.support_url,
    GENERATED_DATE: new Date().toLocaleDateString(),
    PRODUCT_VERSION: content.guide.product_version,
    GUIDE_VERSION: content.guide.guide_version
  });
  fs.writeFileSync(path.join(tempDir, '02_PRODUCT_GUIDE.html'), guideHtml);
  console.log('✓ Generated 02_PRODUCT_GUIDE.html');

  // 4. Generate 03_PACKAGE_MANIFEST.json
  const manifestTemplate = fs.readFileSync(
    path.join(__dirname, '..', 'launch-packs', 'templates', '03_PACKAGE_MANIFEST.json.template'),
    'utf8'
  );

  // Compute file sizes and hashes (will be 0 and placeholder since files are HTML not PDF yet)
  const files = fs.readdirSync(tempDir);
  const hashes = {};
  const sizes = {};
  files.forEach(f => {
    const fpath = path.join(tempDir, f);
    const stat = fs.statSync(fpath);
    sizes[f] = stat.size;
    hashes[f] = computeHash(fpath);
  });

  const manifestJson = interpolate(manifestTemplate, {
    GENERATED_ISO_TIMESTAMP: new Date().toISOString(),
    PRODUCT_ID: product.id,
    PRODUCT_NAME: product.name,
    PRODUCT_SUBTITLE: product.subtitle || '',
    ROLE: content.product.role,
    PRICE: product.price,
    REPOSITORY: product.repository,
    BRANCH: product.branch,
    COMMIT_SHA: 'pending', // Will be filled in from actual product repo
    FILE_SIZE_00: sizes['00_START_HERE.html'] || 0,
    FILE_SIZE_01: sizes['01_OPEN_PRODUCT.html'] || 0,
    FILE_SIZE_02: sizes['02_PRODUCT_GUIDE.html'] || 0,
    FILE_SIZE_03: 'TBD',
    HASH_00: hashes['00_START_HERE.html'] || '',
    HASH_01: hashes['01_OPEN_PRODUCT.html'] || '',
    HASH_02: hashes['02_PRODUCT_GUIDE.html'] || '',
    HASH_03: '',
    WHAT_YOU_BOUGHT: content.guide.what_you_bought,
    EFFORT: content.guide.effort,
    WHAT_YOU_PRODUCE: content.guide.what_you_produce,
    SUPPORT_URL: content.guide.support_url,
    PACKAGE_SHA256: 'TBD'
  });

  fs.writeFileSync(
    path.join(tempDir, '03_PACKAGE_MANIFEST.json'),
    JSON.stringify(JSON.parse(manifestJson), null, 2)
  );
  console.log('✓ Generated 03_PACKAGE_MANIFEST.json');

  // 5. Create ZIP archive
  const output = fs.createWriteStream(zipPath);
  const archive = archiver('zip', { zlib: { level: 9 } });

  archive.on('error', (err) => {
    throw err;
  });

  archive.pipe(output);

  // Add files to archive
  const filesInTemp = fs.readdirSync(tempDir);
  filesInTemp.forEach(file => {
    archive.file(path.join(tempDir, file), { name: file });
  });

  archive.finalize();

  output.on('close', () => {
    const zipSize = fs.statSync(zipPath).size;
    console.log(`\n✓ Launch Pack created: ${zipPath}`);
    console.log(`  Size: ${formatBytes(zipSize)}`);

    // Cleanup temp directory
    fs.rmSync(tempDir, { recursive: true });

    console.log(`\nNext steps:`);
    console.log(`1. Verify the ZIP contains exactly 4 files`);
    console.log(`2. Test 01_OPEN_PRODUCT.html in a browser`);
    console.log(`3. Convert HTML guides to premium PDFs`);
    console.log(`4. Run: node scripts/validate-package.js ${zipPath}`);
  });
} catch (err) {
  // Cleanup on error
  if (fs.existsSync(tempDir)) {
    fs.rmSync(tempDir, { recursive: true });
  }
  console.error('Error building Launch Pack:', err.message);
  process.exit(1);
}

// Helper function to interpolate template variables
function interpolate(template, vars) {
  let result = template;
  Object.entries(vars).forEach(([key, value]) => {
    result = result.replace(new RegExp(`{{${key}}}`, 'g'), value || '');
    result = result.replace(new RegExp(`{{#${key}}}(.*?){{/${key}}}`, 'gs'), value ? `$1` : '');
  });
  return result;
}

// Format bytes for display
function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}
