import fs from "node:fs";
import path from "node:path";

const root = new URL("../dist/", import.meta.url).pathname;
const files = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else files.push(full);
  }
}
walk(root);
const js = files.filter((f) => f.endsWith(".js")).map((f) => fs.readFileSync(f, "utf8")).join("\n");
const failures = [];
for (const forbidden of ["__MI_TEST__", "wrongMirrors", "correctGate"]) {
  if (js.includes(forbidden)) failures.push(`production bundle exposes ${forbidden}`);
}
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
if (!html.includes("Mental Ingenuity")) failures.push("product name missing from built HTML");
if (!html.includes("Sonly Consulting")) failures.push("brand name missing from built HTML");
if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log("PASS production bundle contains no solution oracle and preserves exact brand names");
