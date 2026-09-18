import type { DimScores, LevelReport, ScoredLevel } from "./types";

export function clamp01(x: number): number {
  return Math.max(0, Math.min(1, x));
}

/**
 * Scores a completed level across the four dimensions. This is a gameplay
 * score describing how the run went. It is not an intelligence score and is
 * never compared against any population norm.
 */
export function scoreLevel(r: LevelReport): ScoredLevel {
  const par = Math.max(1, r.parMoves);
  const accuracy = clamp01(1 - r.errors / (par + 3));
  const efficiency = clamp01(par / Math.max(par, r.moves));
  let insight: number;
  if (r.hintsUsed === 0) insight = r.attempts <= 1 ? 1 : 0.85;
  else insight = Math.max(0.2, 0.6 - 0.15 * r.hintsUsed);
  let adaptability: number;
  if (r.chamber === "summit" && r.ruleChange) {
    adaptability = r.ruleChange.adaptedOnFirstTry
      ? 1
      : clamp01(0.7 - 0.15 * r.ruleChange.errorsAfter);
  } else {
    adaptability = r.errors === 0 ? 1 : r.recoveredAfterError ? 0.75 : 0.5;
  }
  const dims: DimScores = { accuracy, efficiency, insight, adaptability };
  const score = Math.round(
    300 * (0.3 * accuracy + 0.3 * efficiency + 0.25 * insight + 0.15 * adaptability)
  );
  return { ...r, dims, score };
}

export function dimLabel(d: keyof DimScores): string {
  switch (d) {
    case "accuracy":
      return "Accuracy";
    case "efficiency":
      return "Efficiency";
    case "insight":
      return "Insight";
    case "adaptability":
      return "Adaptability";
  }
}
