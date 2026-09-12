import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const root = path.resolve(import.meta.dirname, "..");
const read = (name) => fs.readFileSync(path.join(root, name), "utf8");

const html = read("index.html");
const css = read("styles.css");
const app = read("app.js");
const data = read("product-data.js");
const manifest = read("media-manifest.json");

const results = [];
function check(name, condition, detail = "") {
  results.push({ name, pass: Boolean(condition), detail });
}

for (const [name, source] of [["app.js", app], ["product-data.js", data]]) {
  try {
    new vm.Script(source, { filename: name });
    check(name + " parses", true);
  } catch (error) {
    check(name + " parses", false, String(error));
  }
}

const requiredIds = [
  "catalog",
  "checkout",
  "identityForm",
  "customerEmail",
  "paymentChoices",
  "paymentForm",
  "payerIdentity",
  "transactionReference",
  "pendingSummary"
];
for (const id of requiredIds) {
  check("HTML contains #" + id, html.includes('id="' + id + '"'));
}

const allText = [html, css, app, data, manifest].join("\n");
check("No em dash", !allText.includes("—"));
check("No en dash", !allText.includes("–"));
check("No wildcard postMessage target", !/postMessage\s*\([\s\S]*?,\s*["']\*["']\s*\)/m.test(app));
check("No provider destination URL", !/cash\.app|paypal\.me/i.test(allText));
check("Cash App handle locked", data.includes('$SonlyConsulting'));
check("PayPal handle locked", data.includes('@SonlyConsulting'));

for (const [id, price] of [
  ["sca", 20],
  ["focus-flow", 20],
  ["mental-ingenuity", 20],
  ["focus-mental-pair", 30],
  ["intro-trio", 45],
  ["part-1", 39],
  ["part-2", 39],
  ["part-3", 39],
  ["parts-1-3", 99],
  ["unified", 119],
  ["complete", 199]
]) {
  const escapedId = id.replace(/[.*+?^$()|[\]{}\\]/g, "\\$&");
  const pattern = new RegExp('id:\\s*"' + escapedId + '"[\\s\\S]*?price:\\s*' + price + '\\b');
  check("Locked price " + id + " = $" + price, pattern.test(data));
}

const secretPatterns = [
  /sk-[A-Za-z0-9_-]{16,}/,
  /AIza[0-9A-Za-z_-]{20,}/,
  /BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY/,
  /service[_-]?role["'\s:=]+[A-Za-z0-9._-]{12,}/i,
  /password["'\s:=]+[^\s"'<>]{8,}/i
];
for (const pattern of secretPatterns) {
  check("Secret scan " + pattern, !pattern.test(allText));
}

check("Semantic main present", /<main\b/i.test(html));
check("Reduced motion CSS present", css.includes("prefers-reduced-motion"));
check("Local state key present", app.includes("ctj.commercial.order.v1"));
check("Payment submitted is not verified", app.includes("This is not yet a verified paid order"));
check("Merchant verification wording present", html.includes("verifies the payment merchant-side"));

JSON.parse(manifest);
check("Media manifest parses", true);

const failed = results.filter((result) => !result.pass);
for (const result of results) {
  console.log((result.pass ? "PASS" : "FAIL") + "  " + result.name + (result.detail ? "  " + result.detail : ""));
}
console.log("\n" + (results.length - failed.length) + "/" + results.length + " checks passed");
if (failed.length) process.exitCode = 1;
