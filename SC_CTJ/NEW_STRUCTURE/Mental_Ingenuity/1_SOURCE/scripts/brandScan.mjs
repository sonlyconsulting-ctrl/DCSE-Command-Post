/* Brand and typography scan.
 * Verifies exact brand wording, absence of unauthorized consulting names,
 * and absence of em/en dashes in interface, docs, and metadata copy.
 */
import fs from "node:fs";
import path from "node:path";

const root = new URL("..", import.meta.url).pathname;
const targets = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (["node_modules", "dist", ".git", "public"].includes(entry.name)) continue;
      walk(p);
    } else if (/\.(ts|tsx|css|html|md|mjs|json|py|svg)$/.test(entry.name)) {
      if (entry.name === "brandScan.mjs") continue; // the scanner holds the forbidden literals
      targets.push(p);
    }
  }
}
walk(root);
targets.push(path.join(root, "index.html"));

const forbidden = [
  { re: /summit\s+consulting/gi, label: "Summit Consulting" },
  { re: /summitt/gi, label: "Summitt" },
  { re: /[\u2013\u2014]/g, label: "em dash or en dash" },
];

let problems = 0;
let productMentions = 0;
let attributionMentions = 0;

for (const file of targets) {
  const text = fs.readFileSync(file, "utf8");
  productMentions += (text.match(/Mental Ingenuity/g) ?? []).length;
  attributionMentions += (text.match(/Powered by Sonly Consulting/g) ?? []).length;
  for (const f of forbidden) {
    const hits = text.match(f.re);
    if (hits) {
      problems += hits.length;
      console.log(`VIOLATION ${f.label} x${hits.length} in ${path.relative(root, file)}`);
    }
  }
}

// media filenames check
const mediaDir = path.join(root, "public", "media");
function walkNames(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walkNames(p);
    else {
      if (/summit|summitt/i.test(entry.name) && !/chamber_summit/.test(entry.name)) {
        // chamber_summit is the game's final chamber asset, not a consulting brand
        console.log("CHECK filename:", entry.name);
      }
      if (/[\u2013\u2014]/.test(entry.name)) {
        problems++;
        console.log("VIOLATION dash in filename:", entry.name);
      }
    }
  }
}
walkNames(mediaDir);

console.log(`\nProduct name mentions: ${productMentions}`);
console.log(`Attribution mentions: ${attributionMentions}`);
console.log(problems === 0 ? "BRAND SCAN CLEAN" : `BRAND SCAN FOUND ${problems} PROBLEMS`);
process.exit(problems === 0 && productMentions > 0 && attributionMentions > 0 ? 0 : 1);
