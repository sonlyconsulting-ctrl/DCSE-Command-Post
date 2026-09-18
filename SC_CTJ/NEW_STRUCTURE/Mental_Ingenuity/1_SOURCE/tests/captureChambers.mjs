import { chromium } from "playwright";
import fs from "node:fs";

const base = process.env.MI_BASE ?? "http://127.0.0.1:4173";
const out = new URL("../docs/screenshots/chambers/", import.meta.url).pathname;
fs.mkdirSync(out, { recursive: true });

const browser = await chromium.launch({
  executablePath: process.env.MI_CHROMIUM_PATH || undefined,
  args: process.env.MI_CHROMIUM_PATH ? ["--no-sandbox", "--disable-setuid-sandbox", "--single-process", "--no-zygote", "--disable-gpu", "--disable-webgl"] : [],
});
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await page.addInitScript(() => {
  const progress = () => ({ completedLevels: [], bestLevelScores: {}, bestDims: { accuracy: 0, efficiency: 0, insight: 0, adaptability: 0 }, results: [] });
  localStorage.setItem("mental-ingenuity.save.v1", JSON.stringify({
    version: 1,
    settings: { masterVolume: 0.8, musicVolume: 0.7, ambienceVolume: 0.6, sfxVolume: 0.8, muted: true, reducedMotion: false, highContrast: false, captions: false },
    unlockedIndex: 5,
    chambers: { signal: progress(), forge: progress(), perspective: progress(), causal: progress(), paradox: progress(), summit: progress() },
    achievements: [], inFlight: null, finished: false, hintsRemaining: 3,
  }));
});
await page.goto(base);
await page.waitForSelector(".cinematic");
await page.getByRole("button", { name: "Skip the opening cinematic" }).click();
await page.waitForSelector(".start-view");
await page.locator(".start-buttons .btn-gold").click();
await page.waitForSelector(".map-view");

const chambers = [
  ["The Signal Chamber", "signal"],
  ["The Constraint Forge", "forge"],
  ["The Perspective Engine", "perspective"],
  ["The Causal Labyrinth", "causal"],
  ["The Paradox Vault", "paradox"],
  ["The Summit", "summit"],
];

for (const [name, file] of chambers) {
  await page.getByRole("button", { name: new RegExp(`^${name}`) }).click();
  await page.waitForSelector(".chamber-view");
  await page.waitForTimeout(900);
  await page.screenshot({ path: `${out}${file}.png` });
  await page.getByRole("button", { name: "Pause game" }).click();
  await page.getByRole("button", { name: /Leave the challenge and return to the chamber map/ }).click();
  await page.waitForSelector(".map-view");
}

await browser.close();
console.log("PASS captured six production chamber environments");
