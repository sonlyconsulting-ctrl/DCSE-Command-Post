# CTJ Launch Pack Builder — Quick Start

## Build the Unified Edition Launch Pack (5 minutes)

### Prerequisites
- Node.js 14+ installed
- This directory: `/packaging`

### Step 1: Install Dependencies
```bash
cd packaging
npm install
```

### Step 2: Build Unified Edition
```bash
node scripts/build-launch-pack.js unified ./dist
```

**Expected Output:**
```
Building Launch Pack for: Unified Edition
Output: ./dist/CTJ-UNIFIED-Launch-Pack-v1.0.0.zip

✓ Generated 00_START_HERE.html
✓ Generated 01_OPEN_PRODUCT.html
✓ Generated 02_PRODUCT_GUIDE.html
✓ Generated 03_PACKAGE_MANIFEST.json

✓ Launch Pack created: ./dist/CTJ-UNIFIED-Launch-Pack-v1.0.0.zip
  Size: 45.2 KB
```

### Step 3: Validate the Package
```bash
node scripts/validate-package.js ./dist/CTJ-UNIFIED-Launch-Pack-v1.0.0.zip
```

**Expected:** All checks PASS ✓

### Step 4: Test in Browser
```bash
cd dist
unzip CTJ-UNIFIED-Launch-Pack-v1.0.0.zip
open 01_OPEN_PRODUCT.html  # macOS
# or
xdg-open 01_OPEN_PRODUCT.html  # Linux
```

Click the **START NOW** button to verify the launcher works.

---

## Build All 7 Products

```bash
node scripts/generate-all-packs.js ./dist
```

(Note: `generate-all-packs.js` TBD — will build all products sequentially)

---

## What You Get

After building, your `dist/` folder contains:
- `CTJ-UNIFIED-Launch-Pack-v1.0.0.zip` — Ready to deliver to customers

Inside the ZIP (4 files):
1. **00_START_HERE.html** — Premium one-page intro (currently HTML; will be PDF)
2. **01_OPEN_PRODUCT.html** — Branded launcher button
3. **02_PRODUCT_GUIDE.html** — User guide (currently HTML; will be PDF)
4. **03_PACKAGE_MANIFEST.json** — Metadata and checksums

---

## Customizing Product Content

To change what appears in the Launch Pack, edit:
`launch-packs/unified/content.json`

Available fields:
- `product` — Name, role, effort, price
- `guide` — Overview, what_you_do, what_you_produce, etc.
- `launcher` — Button text and URL

Changes take effect immediately on next build.

---

## Converting to PDF

**Current:** Templates are HTML (print-to-PDF ready)  
**Next:** Choose PDF library and set up conversion

Recommended: `puppeteer` for high-fidelity HTML → PDF

```bash
npm install puppeteer
node scripts/html-to-pdf.js  # TBD
```

---

## Troubleshooting

**"Module not found: adm-zip"**
```bash
npm install adm-zip archiver
```

**"File not found: content.json"**
Make sure you're running from the `packaging/` directory and the file exists:
```bash
ls launch-packs/unified/content.json
```

**ZIP is invalid**
Run the validator to see what's wrong:
```bash
node scripts/validate-package.js ./dist/CTJ-UNIFIED-Launch-Pack-v1.0.0.zip
```

---

## Next Steps

1. **✓ Build Unified Edition** ← You are here
2. **Convert HTML to premium PDF** (puppeteer)
3. **Test in browser** (verify launcher works)
4. **Implement Keeper Pack generation** (on product completion)
5. **Wire payment processor** (triggers Launch Pack download)
6. **Go live!** 🚀

---

For detailed documentation, see `README.md` in this directory.
