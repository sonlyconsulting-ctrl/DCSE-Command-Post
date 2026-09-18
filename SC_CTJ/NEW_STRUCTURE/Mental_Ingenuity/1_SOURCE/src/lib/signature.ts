import type { ChamberId, DimScores, SaveState, ScoredLevel } from "./types";

export interface SignatureResult {
  title: string;
  summary: string;
  evidence: string[];
  dims: DimScores;
  totalScore: number;
}

const TITLES: Record<string, string> = {
  signal: "Pattern Navigator",
  forge: "Constraint Architect",
  perspective: "Perspective Shifter",
  causal: "Systems Reader",
  paradox: "Evidence Weaver",
  summit: "Adaptive Strategist",
};

const TITLE_SUMMARY: Record<string, string> = {
  signal:
    "You moved through noise with a steady eye, locking onto governing patterns and holding them across the field.",
  forge:
    "You planned inside strict limits, spending moves like a resource and finding routes others would miss.",
  perspective:
    "You reoriented the problem itself, turning structure until the hidden alignment became visible.",
  causal:
    "You read the machinery as one connected body, anticipating how each adjustment would travel downstream.",
  paradox:
    "You tested attractive claims against the record and found the evidence that quietly defeated them.",
  summit:
    "You recognized when the rules themselves moved, revised your strategy, and carried every discipline to the gate.",
};

export function averageDims(results: ScoredLevel[]): DimScores {
  if (results.length === 0)
    return { accuracy: 0, efficiency: 0, insight: 0, adaptability: 0 };
  const sum = results.reduce(
    (a, r) => ({
      accuracy: a.accuracy + r.dims.accuracy,
      efficiency: a.efficiency + r.dims.efficiency,
      insight: a.insight + r.dims.insight,
      adaptability: a.adaptability + r.dims.adaptability,
    }),
    { accuracy: 0, efficiency: 0, insight: 0, adaptability: 0 }
  );
  const n = results.length;
  return {
    accuracy: sum.accuracy / n,
    efficiency: sum.efficiency / n,
    insight: sum.insight / n,
    adaptability: sum.adaptability / n,
  };
}

/**
 * Builds the final Reasoning Signature from recorded gameplay only.
 * This is a descriptive profile of observed play behavior. It is not a
 * diagnosis, an intelligence rating, or a statement about fixed traits.
 */
export function buildSignature(save: SaveState): SignatureResult {
  const all: ScoredLevel[] = [];
  const byChamber: Record<string, ScoredLevel[]> = {};
  for (const id of Object.keys(save.chambers) as ChamberId[]) {
    const rs = save.chambers[id].results;
    byChamber[id] = rs;
    all.push(...rs);
  }
  const dims = averageDims(all);
  const totalScore = all.reduce((a, r) => a + r.score, 0);

  const affinity: Record<string, number> = {};
  const strength = (id: ChamberId) => {
    const rs = byChamber[id] ?? [];
    if (rs.length === 0) return 0;
    return rs.reduce((a, r) => a + r.score, 0) / (rs.length * 300);
  };
  affinity.signal = strength("signal") * 0.7 + dims.insight * 0.3;
  affinity.forge = strength("forge") * 0.7 + dims.efficiency * 0.3;
  affinity.perspective = strength("perspective") * 0.7 + dims.efficiency * 0.15 + dims.insight * 0.15;
  affinity.causal = strength("causal") * 0.7 + dims.accuracy * 0.3;
  affinity.paradox = strength("paradox") * 0.7 + dims.accuracy * 0.3;
  affinity.summit =
    strength("summit") * 0.6 + dims.adaptability * 0.4;

  let best = "summit";
  for (const k of Object.keys(affinity)) {
    if (affinity[k] > affinity[best]) best = k;
  }

  const evidence: string[] = [];
  const totalMoves = all.reduce((a, r) => a + r.moves, 0);
  const totalPar = all.reduce((a, r) => a + r.parMoves, 0);
  const totalHints = all.reduce((a, r) => a + r.hintsUsed, 0);
  const totalAttempts = all.reduce((a, r) => a + r.attempts, 0);
  const cleanLevels = all.filter((r) => r.errors === 0).length;
  evidence.push(
    `Across ${all.length} completed challenges you spent ${totalMoves} moves against a combined par of ${totalPar}.`
  );
  evidence.push(
    totalHints === 0
      ? "No hints were used at any point in the ascent."
      : `${totalHints} hint${totalHints === 1 ? "" : "s"} were used during the ascent.`
  );
  evidence.push(
    `${cleanLevels} of ${all.length} challenges closed without a single misread.`
  );
  if (totalAttempts > all.length) {
    evidence.push(
      `You reset and re-ran ${totalAttempts - all.length} experiment${
        totalAttempts - all.length === 1 ? "" : "s"
      } when a route failed, rather than forcing it.`
    );
  }
  const summitRunsWithChange = (byChamber.summit ?? []).filter((r) => r.ruleChange);
  if (summitRunsWithChange.length > 0) {
    const worst = summitRunsWithChange.reduce((a, r) =>
      (a.ruleChange?.adaptedOnFirstTry ? 0 : 1) >= (r.ruleChange?.adaptedOnFirstTry ? 0 : 1) ? a : r
    );
    const rc = worst.ruleChange;
    evidence.push(
      rc?.adaptedOnFirstTry
        ? `When the Summit revised its law, you adjusted on the first decision afterward (across ${summitRunsWithChange.length} summit runs).`
        : `After the Summit revised its law you needed up to ${rc?.errorsAfter ?? 0} further probes before adapting.`
    );
  }

  return {
    title: TITLES[best],
    summary: TITLE_SUMMARY[best],
    evidence,
    dims,
    totalScore,
  };
}
