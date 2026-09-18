import type { ChamberId, SaveState } from "./types";
import { CHAMBER_ORDER } from "./types";

export interface AchievementDef {
  id: string;
  name: string;
  desc: string;
  check: (s: SaveState) => boolean;
}

function chamberDone(s: SaveState, id: ChamberId): boolean {
  const c = s.chambers[id];
  return c.completedLevels.includes(0) && c.completedLevels.includes(1) && c.completedLevels.includes(2);
}

export const ACHIEVEMENTS: AchievementDef[] = [
  {
    id: "first_light",
    name: "First Light",
    desc: "Complete every challenge in The Signal Chamber.",
    check: (s) => chamberDone(s, "signal"),
  },
  {
    id: "forged_path",
    name: "Forged Path",
    desc: "Complete The Constraint Forge.",
    check: (s) => chamberDone(s, "forge"),
  },
  {
    id: "true_sight",
    name: "True Sight",
    desc: "Complete The Perspective Engine without using a hint there.",
    check: (s) => chamberDone(s, "perspective") && s.chambers.perspective.results.every((r) => r.hintsUsed === 0),
  },
  {
    id: "chain_reader",
    name: "Chain Reader",
    desc: "Stabilize The Causal Labyrinth.",
    check: (s) => chamberDone(s, "causal"),
  },
  {
    id: "vault_breaker",
    name: "Vault Breaker",
    desc: "Open The Paradox Vault with three or fewer misplacements across it.",
    check: (s) =>
      chamberDone(s, "paradox") &&
      s.chambers.paradox.results.reduce((a, r) => a + r.errors, 0) <= 3,
  },
  {
    id: "ascendant",
    name: "Ascendant",
    desc: "Reach the top of The Ingenuity Ascent. Every chamber complete.",
    check: (s) => CHAMBER_ORDER.every((c) => chamberDone(s, c)),
  },
  {
    id: "unassisted",
    name: "Unassisted Ascent",
    desc: "Finish the entire ascent without spending a single hint.",
    check: (s) =>
      CHAMBER_ORDER.every((c) => chamberDone(s, c)) &&
      CHAMBER_ORDER.every((c) => s.chambers[c].results.every((r) => r.hintsUsed === 0)),
  },
  {
    id: "economical",
    name: "Economical Mind",
    desc: "Earn an average efficiency of 0.85 or better across all completed challenges.",
    check: (s) => {
      const rs = CHAMBER_ORDER.flatMap((c) => s.chambers[c].results);
      if (rs.length < 6) return false;
      return rs.reduce((a, r) => a + r.dims.efficiency, 0) / rs.length >= 0.85;
    },
  },
];

export function evaluateAchievements(s: SaveState): string[] {
  const earned: string[] = [];
  for (const a of ACHIEVEMENTS) {
    if (!s.achievements.includes(a.id) && a.check(s)) earned.push(a.id);
  }
  return earned;
}
