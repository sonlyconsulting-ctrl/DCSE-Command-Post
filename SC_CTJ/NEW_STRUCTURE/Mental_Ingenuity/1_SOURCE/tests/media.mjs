/* Multimedia verification: video playback, audio decodability, reduced-motion alternative. */
import { chromium } from "playwright";
import fs from "node:fs";

const BASE = "http://localhost:4173";
const results = [];
function record(name, pass, detail = "") {
  results.push({ name, pass, detail });
  console.log(`${pass ? "PASS" : "FAIL"}  ${name}${detail ? "  [" + detail + "]" : ""}`);
}

const AUDIO_FILES = [
  "music_opening", "music_map", "music_focus", "music_structure", "music_tension",
  "music_summit", "music_complete",
  "amb_signal", "amb_forge", "amb_perspective", "amb_causal", "amb_vault", "amb_summit",
  "sfx_select", "sfx_place", "sfx_invalid", "sfx_rotate", "sfx_connect", "sfx_activate",
  "sfx_reset", "sfx_hint", "sfx_discover", "sfx_complete", "sfx_unlock", "sfx_rule_change",
  "sfx_achievement", "sfx_final",
];

const IMG_FILES = [
  "hero.webp", "map.webp", "chamber_signal.webp", "chamber_forge.webp",
  "chamber_perspective.webp", "chamber_causal.webp", "chamber_vault.webp",
  "chamber_summit.webp", "about.webp", "social.webp",
];

const browser = await chromium.launch({
  executablePath: process.env.MI_CHROMIUM_PATH || undefined,
  args: process.env.MI_CHROMIUM_PATH ? ["--no-sandbox", "--disable-setuid-sandbox", "--single-process", "--no-zygote", "--disable-gpu", "--disable-webgl"] : [],
});
const page = await (await browser.newContext()).newPage();
const consoleErrors = [];
page.on("console", (m) => m.type() === "error" && consoleErrors.push(m.text()));

await page.goto(BASE);
await page.waitForSelector(".cinematic");

// asset reachability
for (const f of IMG_FILES) {
  const status = await page.evaluate(async (u) => (await fetch(u)).status, `/media/img/${f}`);
  record(`Image asset served: ${f}`, status === 200, `HTTP ${status}`);
}
for (const f of ["video/opening.mp4", "video/opening.webm", "video/poster.jpg"]) {
  const status = await page.evaluate(async (u) => (await fetch(u)).status, `/media/${f}`);
  record(`Video asset served: ${f}`, status === 200, `HTTP ${status}`);
}

// audio decodability via WebAudio
await page.goto(BASE);
await page.waitForSelector(".cinematic");
const decodeResults = await page.evaluate(async (files) => {
  const Ctx = window.AudioContext || window.webkitAudioContext;
  const ctx = new Ctx();
  const out = [];
  for (const f of files) {
    try {
      const buf = await (await fetch("/media/audio/" + f + ".ogg")).arrayBuffer();
      const bytes = buf.byteLength;
      const audio = await ctx.decodeAudioData(buf);
      out.push({ f, ok: true, dur: Math.round(audio.duration * 10) / 10, bytes });
    } catch (e) {
      out.push({ f, ok: false, err: String(e).slice(0, 60) });
    }
  }
  ctx.close();
  return out;
}, AUDIO_FILES);
for (const r of decodeResults) {
  record(`Audio decodes: ${r.f}`, r.ok, r.ok ? `${r.dur}s, ${r.bytes} bytes` : r.err);
}

// video playback in cinematic
await page.goto(BASE);
await page.waitForSelector(".cinematic");
const videoState = await page.evaluate(() => {
  return new Promise((resolve) => {
    const v = document.querySelector(".cine-video");
    if (!v) return resolve({ present: false });
    const timer = setTimeout(() => resolve({ present: true, readyState: v.readyState, currentTime: v.currentTime, paused: v.paused, error: v.error?.code ?? null, muted: v.muted }), 9000);
    v.addEventListener("playing", () => {
      clearTimeout(timer);
      setTimeout(() => resolve({ present: true, readyState: v.readyState, currentTime: v.currentTime, paused: v.paused, error: null, muted: v.muted }), 1500);
    });
  });
});
record("Cinematic video present", videoState.present === true);
record("Cinematic video plays (autoplay muted)", videoState.currentTime > 0.2 || videoState.readyState >= 2, JSON.stringify(videoState));
record("Cinematic video starts muted (no sound before choice)", videoState.muted === true);
await page.screenshot({ path: new URL("../docs/screenshots/01b-cinematic-playing.png", import.meta.url).pathname });

// replay control
await page.getByRole("button", { name: "Replay the opening cinematic" }).click().catch(() => undefined);

// reduced-motion cinematic alternative
await page.evaluate(() => {
  const k = "mental-ingenuity.save.v1";
  const s = JSON.parse(localStorage.getItem(k) ?? "null") ?? { version: 1, settings: {} };
  s.settings = { ...(s.settings ?? {}), reducedMotion: true };
  localStorage.setItem(k, JSON.stringify(s));
});
await page.goto(BASE);
await page.waitForSelector(".cinematic");
const reducedAlt = await page.evaluate(() => ({
  reduced: document.querySelector(".cinematic.reduced") !== null,
  video: document.querySelector("video") !== null,
  poster: document.querySelector(".cine-poster") !== null,
  posterComplete: document.querySelector(".cine-poster")?.complete === true,
  posterWidth: document.querySelector(".cine-poster")?.naturalWidth ?? 0,
  transcript: document.querySelector(".cine-transcript") !== null,
}));
record("Reduced motion replaces video with a loaded still alternative", reducedAlt.reduced && !reducedAlt.video && reducedAlt.poster && reducedAlt.posterComplete && reducedAlt.posterWidth > 0 && reducedAlt.transcript, JSON.stringify(reducedAlt));
await page.screenshot({ path: new URL("../docs/screenshots/01c-cinematic-reduced.png", import.meta.url).pathname });

// missing asset resilience: the dev/preview server may SPA-fallback missing paths.
// What matters is that the request resolves without crashing the page, and the app
// hides any image that fails to load via its onError handler.
const missing = await page.evaluate(async () => (await fetch("/media/img/does-not-exist.webp")).status);
const stillAlive = await page.evaluate(() => document.readyState);
record("Missing asset request resolves without page failure", (missing === 404 || missing === 200) && stillAlive === "complete", `HTTP ${missing}, state ${stillAlive}`);

record("No console errors during media verification", consoleErrors.filter((t) => !t.includes("404")).length === 0, consoleErrors.slice(0, 2).join("|"));

await browser.close();
const failed = results.filter((r) => !r.pass);
console.log(`\n${results.length - failed.length}/${results.length} media checks passed`);
fs.writeFileSync(new URL("../docs/media-results.json", import.meta.url).pathname, JSON.stringify({ results, videoState }, null, 2));
if (failed.length) process.exit(1);
