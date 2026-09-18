import type { SaveState } from "./types";
import { freshSave, CHAMBER_ORDER } from "./types";
import type { Settings } from "./types";
import { DEFAULT_SETTINGS } from "./types";

const KEY = "mental-ingenuity.save.v1";

function isObj(x: unknown): x is Record<string, unknown> {
  return typeof x === "object" && x !== null;
}

function sanitizeSettings(raw: unknown): Settings {
  const out = { ...DEFAULT_SETTINGS };
  if (!isObj(raw)) return out;
  for (const k of [
    "masterVolume",
    "musicVolume",
    "ambienceVolume",
    "sfxVolume",
  ] as const) {
    const v = raw[k];
    if (typeof v === "number" && v >= 0 && v <= 1) out[k] = v;
  }
  for (const k of ["muted", "reducedMotion", "highContrast", "captions"] as const) {
    if (typeof raw[k] === "boolean") out[k] = raw[k] as boolean;
  }
  return out;
}

/**
 * Loads and validates saved state. Any corruption or schema drift falls back
 * to a fresh save rather than crashing the game.
 */
export function loadSave(): { save: SaveState; recovered: boolean } {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return { save: freshSave(), recovered: false };
    const parsed = JSON.parse(raw);
    if (!isObj(parsed) || parsed.version !== 1) {
      return { save: freshSave(), recovered: true };
    }
    const base = freshSave();
    const save: SaveState = {
      ...base,
      settings: sanitizeSettings(parsed.settings),
      unlockedIndex:
        typeof parsed.unlockedIndex === "number"
          ? Math.max(0, Math.min(5, Math.floor(parsed.unlockedIndex)))
          : 0,
      achievements: Array.isArray(parsed.achievements)
        ? parsed.achievements.filter((a) => typeof a === "string")
        : [],
      inFlight: null,
      finished: parsed.finished === true,
      hintsRemaining:
        typeof parsed.hintsRemaining === "number"
          ? Math.max(0, Math.min(18, Math.floor(parsed.hintsRemaining)))
          : 3,
    };
    if (isObj(parsed.inFlight)) {
      const inf = parsed.inFlight;
      const ch = inf.chamber;
      if (
        typeof ch === "string" &&
        (CHAMBER_ORDER as string[]).includes(ch) &&
        typeof inf.level === "number"
      ) {
        save.inFlight = {
          chamber: ch as (typeof CHAMBER_ORDER)[number],
          level: Math.max(0, Math.min(2, Math.floor(inf.level as number))),
          attempts: typeof inf.attempts === "number" ? inf.attempts : 0,
          startedAt: typeof inf.startedAt === "number" ? inf.startedAt : Date.now(),
          moves: typeof inf.moves === "number" ? Math.max(0, Math.floor(inf.moves)) : 0,
          errors: typeof inf.errors === "number" ? Math.max(0, Math.floor(inf.errors)) : 0,
          hintsUsed: typeof inf.hintsUsed === "number" ? Math.max(0, Math.floor(inf.hintsUsed)) : 0,
          events: Array.isArray(inf.events) ? inf.events.filter((e): e is string => typeof e === "string").slice(-200) : [],
        };
      }
    }
    if (isObj(parsed.chambers)) {
      const parsedChambers = parsed.chambers as Record<string, unknown>;
      for (const id of CHAMBER_ORDER) {
        const raw = parsedChambers[id];
        if (!isObj(raw)) continue;
        const c = raw as Record<string, unknown>;
        const prog = save.chambers[id];
        if (Array.isArray(c.completedLevels)) {
          prog.completedLevels = (c.completedLevels as unknown[]).filter(
            (n: unknown) => typeof n === "number" && n >= 0 && n <= 2
          ) as number[];
        }
        if (Array.isArray(c.results)) {
          prog.results = (c.results as unknown[]).filter(
            (r: unknown) =>
              isObj(r) &&
              typeof r.score === "number" &&
              typeof r.level === "number" &&
              isObj(r.dims)
          ) as never;
        }
        if (isObj(c.bestLevelScores)) {
          const bls = c.bestLevelScores as Record<string, unknown>;
          for (const k of Object.keys(bls)) {
            const v = bls[k];
            const lvl = Number(k);
            if (Number.isInteger(lvl) && lvl >= 0 && lvl <= 2 && typeof v === "number") {
              prog.bestLevelScores[lvl] = v;
            }
          }
        }
      }
    }
    return { save, recovered: false };
  } catch {
    return { save: freshSave(), recovered: true };
  }
}

export function persistSave(save: SaveState): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(save));
  } catch {
    // Storage full or unavailable. The session continues in memory.
  }
}

export function clearSave(): void {
  try {
    localStorage.removeItem(KEY);
  } catch {
    // ignore
  }
}
