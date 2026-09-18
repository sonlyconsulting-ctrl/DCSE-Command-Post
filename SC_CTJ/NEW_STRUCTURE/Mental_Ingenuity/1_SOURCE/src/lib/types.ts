export type ChamberId =
  | "signal"
  | "forge"
  | "perspective"
  | "causal"
  | "paradox"
  | "summit";

export const CHAMBER_ORDER: ChamberId[] = [
  "signal",
  "forge",
  "perspective",
  "causal",
  "paradox",
  "summit",
];

export interface DimScores {
  accuracy: number;
  efficiency: number;
  insight: number;
  adaptability: number;
}

/** Raw performance data reported by a chamber level when it completes. */
export interface LevelReport {
  chamber: ChamberId;
  level: number;
  solved: boolean;
  moves: number;
  parMoves: number;
  errors: number;
  attempts: number;
  hintsUsed: number;
  durationMs: number;
  detected: string;
  constraint: string;
  strategy: string;
  decisive: string;
  events: string[];
  /** Summit only: behavior after the discoverable rule change. */
  ruleChange?: { errorsAfter: number; adaptedOnFirstTry: boolean };
  /** Optional extra adaptability evidence for non-summit chambers. */
  recoveredAfterError: boolean;
}

export interface ScoredLevel extends LevelReport {
  dims: DimScores;
  score: number;
}

export interface ChamberProgress {
  completedLevels: number[];
  bestLevelScores: Record<number, number>;
  bestDims: DimScores;
  results: ScoredLevel[];
}

export interface Settings {
  masterVolume: number;
  musicVolume: number;
  ambienceVolume: number;
  sfxVolume: number;
  muted: boolean;
  reducedMotion: boolean;
  highContrast: boolean;
  captions: boolean;
}

export interface InFlight {
  chamber: ChamberId;
  level: number;
  attempts: number;
  startedAt: number;
  moves: number;
  errors: number;
  hintsUsed: number;
  events: string[];
}

export interface SaveState {
  version: number;
  settings: Settings;
  unlockedIndex: number;
  chambers: Record<ChamberId, ChamberProgress>;
  achievements: string[];
  inFlight: InFlight | null;
  finished: boolean;
  hintsRemaining: number;
}

export type View =
  | "cinematic"
  | "start"
  | "howto"
  | "map"
  | "chamber"
  | "record"
  | "signature"
  | "progress"
  | "settings"
  | "about"
  | "help"
  | "resume";

export const DEFAULT_SETTINGS: Settings = {
  masterVolume: 0.8,
  musicVolume: 0.7,
  ambienceVolume: 0.6,
  sfxVolume: 0.8,
  muted: false,
  reducedMotion: false,
  highContrast: false,
  captions: false,
};

export function emptyChamberProgress(): ChamberProgress {
  return { completedLevels: [], bestLevelScores: {}, bestDims: { accuracy: 0, efficiency: 0, insight: 0, adaptability: 0 }, results: [] };
}

export function freshSave(): SaveState {
  return {
    version: 1,
    settings: { ...DEFAULT_SETTINGS },
    unlockedIndex: 0,
    chambers: {
      signal: emptyChamberProgress(),
      forge: emptyChamberProgress(),
      perspective: emptyChamberProgress(),
      causal: emptyChamberProgress(),
      paradox: emptyChamberProgress(),
      summit: emptyChamberProgress(),
    },
    achievements: [],
    inFlight: null,
    finished: false,
    hintsRemaining: 3,
  };
}
