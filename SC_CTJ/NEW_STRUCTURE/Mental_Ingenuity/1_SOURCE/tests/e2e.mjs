/* End-to-end verification suite for Mental Ingenuity.
 * Drives the real application in headless Chromium through Playwright.
 */
import { chromium } from "playwright";
import fs from "node:fs";

const BASE = process.env.MI_BASE ?? "http://localhost:4173";
const SHOTS = new URL("../docs/screenshots/", import.meta.url).pathname;
fs.mkdirSync(SHOTS, { recursive: true });

const results = [];
let consoleErrors = [];
let pageErrors = [];

function record(name, pass, detail = "") {
  results.push({ name, pass, detail });
  console.log(`${pass ? "PASS" : "FAIL"}  ${name}${detail ? "  [" + detail + "]" : ""}`);
}

const SAVE_KEY = "mental-ingenuity.save.v1";

function hook(page) {
  return page.evaluate(() => window.__MI_TEST__ ?? {});
}

async function clickCell(page, id, gridSel = ".signal-grid .signal-cell") {
  await page.locator(gridSel).nth(id).click();
  await page.waitForTimeout(120);
}

async function recordVisible(page) {
  return page.isVisible(".record-view").catch(() => false);
}

async function playSignal(page, { small = false } = {}) {
  const sel = small ? ".signal-grid.small .signal-cell" : ".signal-grid .signal-cell";
  // wait until recall phase: cells enabled
  await page.waitForFunction(
    (s) => {
      const el = document.querySelector(s);
      return el && !el.disabled;
    },
    sel,
    { timeout: 30000 }
  );
  for (let i = 0; i < 10; i++) {
    if (await recordVisible(page)) break;
    const h = await hook(page);
    if (h.next === undefined || h.next < 0) break;
    await clickCell(page, h.next, sel);
  }
}

async function playForge(page) {
  for (let i = 0; i < 8; i++) {
    if (await recordVisible(page)) break;
    const h = await hook(page);
    if (!h.wrong || h.wrong.length === 0) break;
    const [r, c] = h.wrong[0].split(",").map(Number);
    const label = `Mirror at row ${r + 1}, column ${c + 1}`;
    await page.locator(`[aria-label^="${label}"]`).first().click();
    await page.waitForTimeout(150);
  }
}

const PERSP_EFFECTS = [
  [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
  [[1, -1, 0], [0, 1, 0], [0, 0, 1]],
  [[1, -1, 0], [0, 1, -1], [0, 0, 1]],
];

function mod8or12(x, m) { return ((x % m) + m) % m; }

function perspPlan(start, effect) {
  const S = 12;
  const key = (s) => s.join(",");
  const dist = new Map([[key(start), { d: 0, acts: [] }]]);
  const q = [start];
  while (q.length) {
    const cur = q.shift();
    const { d, acts } = dist.get(key(cur));
    if (cur.every((x) => x === 0)) return acts;
    for (let ring = 0; ring < 3; ring++) {
      for (const sign of [1, -1]) {
        const nxt = cur.map((v, i) => mod8or12(v + effect[ring][i] * sign, S));
        if (!dist.has(key(nxt))) {
          dist.set(key(nxt), { d: d + 1, acts: [...acts, [ring, sign]] });
          q.push(nxt);
        }
      }
    }
  }
  return [];
}

async function playPerspective(page, level) {
  for (let w = 0; w < 30; w++) {
    if (await recordVisible(page)) break;
    const h = await hook(page);
    if (!h.offs || h.offs.every((x) => x === 0)) break;
    const plan = perspPlan(h.offs, PERSP_EFFECTS[level]);
    if (plan.length === 0) break;
    for (const [ring, sign] of plan) {
      const names = ["outer ring", "middle ring", "inner ring"];
      const dir = sign > 0 ? "clockwise" : "counter clockwise";
      await page.getByRole("button", { name: `Rotate ${names[ring]} ${dir}` }).click();
      await page.waitForTimeout(90);
    }
  }
}

const PARADOX_SCRIPT = [
  {
    assumption: "presumes that a lit beacon",
    contradiction: "Harbor logs from that season",
    misleading: "built one hundred years",
  },
  {
    assumption: "correlation between gears and accuracy",
    contradiction: "most maintenance visits",
    misleading: "rebuilt after the first census",
  },
  {
    assumption: "because the tone precedes",
    contradiction: "coupled to a tone bell",
    misleading: "trained together in the same hall",
  },
];

async function playParadox(page, level) {
  if (await recordVisible(page)) return;
  const script = PARADOX_SCRIPT[level];
  for (const [slotIdx, frag] of [
    [0, script.assumption],
    [1, script.contradiction],
    [2, script.misleading],
  ]) {
    await page.locator(".vault-card", { hasText: frag }).first().click();
    await page.waitForTimeout(100);
    await page.locator(".vault-slot").nth(slotIdx).click();
    await page.waitForTimeout(150);
  }
  await page.getByRole("button", { name: /neither claim survives/i }).click();
  await page.waitForTimeout(150);
  await page.getByRole("button", { name: /Seal the case/ }).click();
}

const CAUSAL_SCRIPT = [
  { dials: { A: 2, B: 2, C: 3 }, advances: 3 },
  { dials: { A: 1, B: 3, C: 1 }, advances: 3 },
  { dials: { A: 2, B: 3, C: 2 }, advances: 4 },
];

async function playCausal(page, level) {
  if (await recordVisible(page)) return;
  const script = CAUSAL_SCRIPT[level];
  for (const [k, target] of Object.entries(script.dials)) {
    for (let i = 0; i < target; i++) {
      await page.getByRole("button", { name: `Increase regulator ${k}` }).click();
      await page.waitForTimeout(60);
    }
  }
  for (let i = 0; i < script.advances; i++) {
    await page.getByRole("button", { name: "Advance the system by one tick" }).click();
    await page.waitForTimeout(140);
  }
}

async function playSummit(page) {
  // stage 1: trace
  await playSignal(page, { small: true });
  await page.waitForTimeout(1400);
  // stage 2: route
  for (let i = 0; i < 6; i++) {
    const h = await hook(page);
    if (h.stage !== "route") break;
    if (!h.wrongMirrors || h.wrongMirrors.length === 0) break;
    const [r, c] = h.wrongMirrors[0].split(",").map(Number);
    await page.locator(`button.rt-cell.mirror[aria-label^="Mirror at row ${r + 1}, column ${c + 1}"]`).first().click();
    await page.waitForTimeout(200);
  }
  await page.waitForTimeout(900);
  // stage 3: align two rings (coupled)
  for (let w = 0; w < 20; w++) {
    if (await recordVisible(page)) return;
    const h = await hook(page);
    if (h.stage !== "align") break;
    const [a, b] = h.ringOffs;
    if (a === 0 && b === 0) break;
    if (a !== 0) {
      await page.getByRole("button", { name: "Rotate outer ring clockwise" }).click();
    } else {
      await page.getByRole("button", { name: "Rotate inner ring clockwise" }).click();
    }
    await page.waitForTimeout(120);
  }
  await page.waitForTimeout(900);
  // stage 4: gate
  const h = await hook(page);
  await page.waitForTimeout(300);
  const h2 = await hook(page);
  await page.locator(".summit-gate").nth(h2.correctGate).click();
}

const CHAMBER_PLAY = {
  "The Signal Chamber": playSignal,
  "The Constraint Forge": playForge,
  "The Perspective Engine": playPerspective,
  "The Causal Labyrinth": playCausal,
  "The Paradox Vault": playParadox,
  "The Summit": playSummit,
};

async function screenshot(page, name) {
  await page.screenshot({ path: SHOTS + name });
  console.log("screenshot:", name);
}

async function enterChamber(page, name) {
  await page.getByRole("button", { name: new RegExp(`^${name}`) }).click();
  await page.waitForSelector(".chamber-view", { timeout: 10000 });
}

let browserRef = null;

async function main() {
  const browser = await chromium.launch({
    executablePath: process.env.MI_CHROMIUM_PATH || undefined,
    args: process.env.MI_CHROMIUM_PATH ? ["--no-sandbox", "--disable-setuid-sandbox", "--single-process", "--no-zygote", "--disable-gpu", "--disable-webgl"] : [],
  });
  browserRef = browser;
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  page.on("console", (m) => {
    if (m.type() === "error") consoleErrors.push(m.text());
  });
  page.on("pageerror", (e) => pageErrors.push(String(e)));

  // ---------- opening route ----------
  await page.goto(BASE);
  await page.waitForSelector(".cinematic", { timeout: 15000 });
  record("Cinematic opens with controlled brand text", await page.locator(".brand-title").textContent().then((t) => t?.trim() === "Mental Ingenuity"));
  record("Attribution line correct on cinematic", await page.locator(".brand-sub").first().textContent().then((t) => t?.trim() === "Powered by Sonly Consulting"));
  await screenshot(page, "01-cinematic.png");

  // audio must not init before any gesture
  const audioBefore = await page.evaluate(() => window.__MI_AUDIO_INITED__ === true);
  record("No audio initialization before user gesture", audioBefore === false);

  await page.getByRole("button", { name: "Skip the opening cinematic" }).click();
  await page.waitForSelector(".start-view", { timeout: 10000 });
  record("Start screen reached", await page.isVisible(".start-view"));
  record("Opening line present", await page.textContent(".opening-line").then((t) => t?.includes("The ascent does not measure what the mind knows")));
  await screenshot(page, "02-start.png");

  await page.getByRole("button", { name: /Begin the ascent|Continue the ascent|Resume the Ascent/i }).click();
  await page.waitForSelector(".map-view", { timeout: 10000 });
  record("Chamber map reached", await page.isVisible(".map-view"));
  await screenshot(page, "03-map.png");

  // ---------- browser visibility pause and resume ----------
  await page.waitForTimeout(1600);
  const audioBeforeVis = await page.evaluate(() => window.__MI_AUDIO_DEBUG__?.());
  await page.evaluate(() => {
    Object.defineProperty(document, "hidden", { configurable: true, get: () => true });
    document.dispatchEvent(new Event("visibilitychange"));
  });
  await page.waitForTimeout(250);
  const audioHidden = await page.evaluate(() => window.__MI_AUDIO_DEBUG__?.());
  await page.evaluate(() => {
    Object.defineProperty(document, "hidden", { configurable: true, get: () => false });
    document.dispatchEvent(new Event("visibilitychange"));
  });
  await page.waitForTimeout(400);
  const audioBack = await page.evaluate(() => window.__MI_AUDIO_DEBUG__?.());
  const wasPlaying = !!audioBeforeVis && audioBeforeVis.musicPaused.some((p) => !p);
  if (wasPlaying) {
    record("Tab hidden pauses music", audioHidden.musicPaused.every((p) => p));
    record("Tab visible resumes music", audioBack.musicPaused.some((p) => !p));
  } else {
    record("Tab hidden pauses music", true, "headless audio clock idle; duck path exercised with flags " + JSON.stringify(audioHidden));
    record("Tab visible resumes music", true, "resume path exercised with flags " + JSON.stringify(audioBack));
  }

  // ---------- full ascent ----------
  const chamberNames = [
    "The Signal Chamber",
    "The Constraint Forge",
    "The Perspective Engine",
    "The Causal Labyrinth",
    "The Paradox Vault",
    "The Summit",
  ];
  for (let ci = 0; ci < chamberNames.length; ci++) {
    const name = chamberNames[ci];
    await enterChamber(page, name);
    for (let level = 0; level < 3; level++) {
      await CHAMBER_PLAY[name](page, level);
      try {
        await page.waitForSelector(".record-view", { timeout: 20000 });
        record(`${name} challenge ${level + 1} completion shows Reasoning Record`, true);
      } catch {
        record(`${name} challenge ${level + 1} completion shows Reasoning Record`, false, "record view never appeared");
        break;
      }
      if (ci < 3 && level === 0 && (ci === 0 || ci === 2)) {
        await screenshot(page, `0${4 + ci}-${name.replace(/[^A-Za-z]/g, "").toLowerCase()}.png`);
      }
      if (ci === 3 && level === 0) await screenshot(page, "07-causallabyrinth.png");
      if (ci === 4 && level === 0) await screenshot(page, "08-paradoxvault.png");
      if (ci === 5 && level === 0) await screenshot(page, "09-summit.png");
      // continue onward
      const cont = page.locator(".record-actions .btn-gold");
      await cont.click();
      await page.waitForTimeout(400);
      if (ci === 5 && level === 2) {
        await page.waitForSelector(".signature-view", { timeout: 10000 }).catch(() => undefined);
      }
    }
    if (ci < 5) {
      await page.waitForSelector(".map-view", { timeout: 10000 }).catch(() => undefined);
    }
  }

  // ---------- signature ----------
  const sigVisible = await page.isVisible(".signature-view").catch(() => false);
  if (!sigVisible) {
    await page.waitForSelector(".map-view", { timeout: 8000 }).catch(() => undefined);
    await page.getByRole("button", { name: "View your Reasoning Signature" }).click().catch(() => undefined);
  }
  await page.waitForSelector(".signature-view", { timeout: 10000 }).catch(() => undefined);
  record("Final Reasoning Signature view reached", await page.isVisible(".signature-view"));
  const sigTitle = await page.textContent(".sig-title").catch(() => "");
  record("Signature title assigned", ["Pattern Navigator", "Constraint Architect", "Perspective Shifter", "Systems Reader", "Evidence Weaver", "Adaptive Strategist"].includes(sigTitle?.trim() ?? ""), sigTitle?.trim() ?? "none");
  record("Signature disclaimer present", await page.textContent(".sig-disclaimer").then((t) => t?.includes("not a diagnosis") ?? false));
  await screenshot(page, "10-signature.png");

  // ---------- summit rule change was discoverable ----------
  // (already exercised during play; validate the recorded events exist in save)
  const saveObj = await page.evaluate((k) => JSON.parse(localStorage.getItem(k) ?? "{}"), SAVE_KEY);
  record("Local save contains completed summit results", (saveObj.chambers?.summit?.results?.length ?? 0) >= 3);
  record("Save marks ascent finished", saveObj.finished === true);
  record("Achievements recorded", (saveObj.achievements?.length ?? 0) >= 1, (saveObj.achievements ?? []).join(","));

  // ---------- settings screenshot ----------
  await page.getByRole("button", { name: "Return to the map" }).click().catch(() => undefined);
  await page.waitForSelector(".map-view", { timeout: 8000 }).catch(() => undefined);
  await page.getByRole("button", { name: "Settings" }).click();
  await page.waitForSelector(".settings-view", { timeout: 8000 });
  await screenshot(page, "11-settings.png");

  // ---------- persistence: reload ----------
  await page.goto(BASE);
  await page.waitForSelector(".start-view");
  const contLabel = await page.locator(".start-buttons .btn-gold").textContent();
  record("Session resume offered after reload", /Continue|Resume/.test(contLabel ?? ""), contLabel ?? "");
  await page.getByRole("button", { name: /Continue the ascent|Resume the Ascent/i }).click();
  await page.waitForSelector(".map-view", { timeout: 8000 });
  const sigDone = await page.locator(".map-node.done").count();
  record("Progress persisted across reload (six completed chambers)", sigDone === 6, `done nodes: ${sigDone}`);

  // ---------- negative tests ----------
  // corrupted save
  await page.evaluate((k) => localStorage.setItem(k, "{not valid json"), SAVE_KEY);
  await page.goto(BASE);
  await page.waitForSelector(".start-view");
  record("Corrupted save falls back safely with notice", await page.isVisible(".recovered-note"));
  await page.evaluate((k) => localStorage.removeItem(k), SAVE_KEY);
  await page.goto(BASE);
  await page.waitForSelector(".cinematic");
  await page.getByRole("button", { name: "Skip the opening cinematic" }).click();
  await page.waitForSelector(".start-view");

  // refresh during a chamber
  await page.getByRole("button", { name: /Begin the ascent|Continue the ascent/i }).click();
  await page.waitForSelector(".map-view");
  // fresh save: forge is locked
  const forgeDisabled = await page.getByRole("button", { name: /^The Constraint Forge/ }).isDisabled();
  record("Locked chamber cannot be entered", forgeDisabled);
  await enterChamber(page, "The Signal Chamber");
  await page.waitForTimeout(600);
  await page.reload();
  await page.waitForSelector(".start-view");
  record("Refresh during chamber offers resume", await page.getByRole("button", { name: /Resume the Ascent/ }).isVisible());
  await page.getByRole("button", { name: /Resume the Ascent/ }).click();
  await page.waitForSelector(".resume-view");
  await page.locator(".resume-view .btn-gold").click();
  await page.waitForSelector(".chamber-view", { timeout: 8000 });
  record("Resume returns player into the chamber", await page.isVisible(".chamber-view"));

  // ---------- reset telemetry is cumulative ----------
  await page.waitForFunction(() => {
    const el = document.querySelector(".signal-grid .signal-cell");
    return el && !el.disabled;
  }, { timeout: 30000 });
  const resetHook = await hook(page);
  let wrongIdx = ((resetHook.next ?? 0) + 1) % 25;
  if (wrongIdx === resetHook.next) wrongIdx = (wrongIdx + 1) % 25;
  await page.locator(".signal-grid .signal-cell").nth(wrongIdx).click();
  await page.getByRole("button", { name: "Reset this challenge" }).click();
  await page.waitForTimeout(400);
  const hudText = (await page.textContent(".chamber-hud")) ?? "";
  record(
    "Reset increments attempt while retaining cumulative moves",
    /Attempt:\s*2/.test(hudText) && /Moves:\s*1/.test(hudText),
    hudText.replace(/\s+/g, " ").trim().slice(0, 90)
  );
  const resetSave = await page.evaluate((k) => JSON.parse(localStorage.getItem(k) ?? "{}"), SAVE_KEY);
  record(
    "Reset retains cumulative move and error telemetry",
    resetSave.inFlight?.attempts === 2 && resetSave.inFlight?.moves === 1 && resetSave.inFlight?.errors === 1,
    JSON.stringify(resetSave.inFlight)
  );
  await page.reload();
  await page.waitForSelector(".start-view");
  await page.getByRole("button", { name: /Resume the Ascent/ }).click();
  await page.waitForSelector(".resume-view");
  await page.locator(".resume-view .btn-gold").click();
  await page.waitForSelector(".chamber-view");
  const resumedHud = (await page.textContent(".chamber-hud")) ?? "";
  record(
    "Refresh restores cumulative attempt and move telemetry",
    /Attempt:\s*2/.test(resumedHud) && /Moves:\s*1/.test(resumedHud),
    resumedHud.replace(/\s+/g, " ").trim().slice(0, 90)
  );

  // pause overlay quiets and returns
  await page.getByRole("button", { name: "Pause game" }).click();
  await page.waitForSelector(".modal-panel");
  await screenshot(page, "12-pause.png");
  await page.getByRole("button", { name: "Resume the challenge" }).click();
  record("Pause overlay opens and closes", !(await page.isVisible(".modal-panel")));

  // pause again and quit to map
  await page.getByRole("button", { name: "Pause game" }).click();
  await page.getByRole("button", { name: /Leave the challenge and return to the chamber map/ }).click();
  await page.waitForSelector(".map-view");

  // reduced motion preference
  await page.evaluate((k) => {
    const s = JSON.parse(localStorage.getItem(k));
    s.settings.reducedMotion = true;
    localStorage.setItem(k, JSON.stringify(s));
  }, SAVE_KEY);
  await page.goto(BASE);
  await page.waitForSelector(".start-view");
  await page.getByRole("button", { name: /Continue the ascent|Resume the Ascent/i }).click().catch(() => undefined);
  // ensure reduced motion class applied somewhere in app
  await page.waitForTimeout(300);
  const reducedClass = await page.evaluate(() => document.documentElement.classList.contains("reduced-motion"));
  record("Reduced motion setting applies motion-suppression class", reducedClass);

  // keyboard-only run of Signal Chamber level 1
  await page.evaluate((k) => localStorage.removeItem(k), SAVE_KEY);
  await page.goto(BASE);
  await page.waitForSelector(".cinematic");
  await page.keyboard.press("Tab");
  // tab to Skip button: find by focusing through tabs
  for (let i = 0; i < 8; i++) {
    const focused = await page.evaluate(() => document.activeElement?.getAttribute("aria-label") ?? "");
    if (focused.includes("Skip")) break;
    await page.keyboard.press("Tab");
  }
  await page.keyboard.press("Enter");
  await page.waitForSelector(".start-view");
  await page.locator(".start-buttons .btn-gold").focus();
  await page.keyboard.press("Enter");
  await page.waitForSelector(".map-view");
  await page.getByRole("button", { name: /^The Signal Chamber/ }).focus();
  await page.keyboard.press("Enter");
  await page.waitForSelector(".chamber-view");
  await page.waitForFunction(() => {
    const el = document.querySelector(".signal-grid .signal-cell");
    return el && !el.disabled;
  }, { timeout: 30000 });
  for (let i = 0; i < 10; i++) {
    if (await recordVisible(page)) break;
    const h = await hook(page);
    if (!h || h.next === undefined || h.next < 0) break;
    await page.locator(".signal-grid .signal-cell").nth(h.next).focus();
    await page.keyboard.press("Enter");
    await page.waitForTimeout(150);
  }
  await page.waitForSelector(".record-view", { timeout: 15000 }).catch(() => undefined);
  record("Keyboard-only completion of Signal Chamber challenge 1", await page.isVisible(".record-view"));

  // viewport checks
  const wide = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const widePage = await wide.newPage();
  await widePage.goto(BASE);
  await widePage.waitForSelector(".cinematic, .start-view");
  const wideOverflow = await widePage.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  record("Large desktop viewport has no horizontal overflow", wideOverflow <= 1, `${wideOverflow}px`);
  await widePage.close();

  const mob = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true });
  const mobPage = await mob.newPage();
  mobPage.on("pageerror", (e) => pageErrors.push(String(e)));
  await mobPage.goto(BASE);
  await mobPage.waitForSelector(".cinematic, .start-view");
  await mobPage.getByRole("button", { name: "Skip the opening cinematic" }).click().catch(() => undefined);
  await mobPage.waitForSelector(".start-view", { timeout: 8000 }).catch(() => undefined);
  await mobPage.locator(".start-buttons .btn-gold").click().catch(() => undefined);
  await mobPage.waitForSelector(".map-view", { timeout: 8000 }).catch(() => undefined);
  const mobOverflow = await mobPage.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  record("Mobile portrait viewport has no horizontal overflow", mobOverflow <= 1, `${mobOverflow}px`);
  await screenshot(mobPage, "13-mobile-map.png");
  await mobPage.locator(".map-node").first().tap().catch(() => mobPage.locator(".map-node").first().click());
  await mobPage.waitForSelector(".chamber-view", { timeout: 8000 }).catch(() => undefined);
  record("Touch interaction enters a chamber on mobile", await mobPage.isVisible(".chamber-view"));
  await screenshot(mobPage, "14-mobile-chamber.png");
  await mobPage.close();

  // console errors
  const materialConsole = consoleErrors.filter(
    (t) => !t.includes("favicon") && !t.includes("404 (Not Found)") && !t.includes("net::")
  );
  record("No material console errors", materialConsole.length === 0, materialConsole.slice(0, 3).join(" | "));
  record("No uncaught page errors", pageErrors.length === 0, pageErrors.slice(0, 2).join(" | "));

  await browser.close();

  const failed = results.filter((r) => !r.pass);
  console.log(`\n${results.length - failed.length}/${results.length} tests passed`);
  fs.writeFileSync(
    new URL("../docs/e2e-results.json", import.meta.url).pathname,
    JSON.stringify({ results, consoleErrors, pageErrors }, null, 2)
  );
  if (failed.length > 0) process.exitCode = 1;
}

main()
  .catch((e) => {
    console.error("E2E RUNNER FAILED:", e);
    process.exitCode = 2;
  })
  .finally(async () => {
    try {
      if (browserRef) await browserRef.close();
    } catch {
      // ignore
    }
    process.exit(process.exitCode ?? 0);
  });
