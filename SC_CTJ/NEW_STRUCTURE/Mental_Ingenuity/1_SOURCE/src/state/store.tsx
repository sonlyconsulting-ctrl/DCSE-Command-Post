import React, {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useReducer,
} from "react";
import type {
  ChamberId,
  InFlight,
  LevelReport,
  SaveState,
  ScoredLevel,
  Settings,
  View,
} from "../lib/types";
import { CHAMBER_ORDER, freshSave } from "../lib/types";
import { scoreLevel } from "../lib/scoring";
import { loadSave, persistSave, clearSave } from "../lib/persistence";
import { evaluateAchievements } from "../lib/achievements";

export interface GameState {
  save: SaveState;
  view: View;
  chamber: ChamberId;
  level: number;
  lastResult: ScoredLevel | null;
  newAchievements: string[];
  saveRecovered: boolean;
  modal: "restart" | null;
}

export type Action =
  | { type: "NAVIGATE"; view: View }
  | { type: "START_LEVEL"; chamber: ChamberId; level: number; attempts?: number }
  | { type: "UPDATE_IN_FLIGHT"; patch: Partial<InFlight> }
  | { type: "ABANDON_RUN" }
  | { type: "COMPLETE_LEVEL"; report: LevelReport }
  | { type: "USE_HINT" }
  | { type: "SET_SETTINGS"; patch: Partial<Settings> }
  | { type: "OPEN_RESTART" }
  | { type: "CLOSE_MODAL" }
  | { type: "CONFIRM_RESTART" }
  | { type: "MARK_ACHIEVEMENTS_SEEN" };

function init(): GameState {
  const { save, recovered } = loadSave();
  const fresh =
    !save.finished &&
    !save.inFlight &&
    CHAMBER_ORDER.every((c) => save.chambers[c].completedLevels.length === 0);
  return {
    save,
    view: fresh && !recovered ? "cinematic" : "start",
    chamber: "signal",
    level: 0,
    lastResult: null,
    newAchievements: [],
    saveRecovered: recovered,
    modal: null,
  };
}

function reducer(state: GameState, action: Action): GameState {
  switch (action.type) {
    case "NAVIGATE":
      return { ...state, view: action.view, modal: null };
    case "START_LEVEL": {
      const existing = state.save.inFlight;
      const resuming = existing?.chamber === action.chamber && existing.level === action.level;
      const save = {
        ...state.save,
        inFlight: resuming ? existing : {
          chamber: action.chamber,
          level: action.level,
          attempts: action.attempts ?? 1,
          startedAt: Date.now(),
          moves: 0,
          errors: 0,
          hintsUsed: 0,
          events: [],
        } as InFlight,
      };
      return {
        ...state,
        save,
        view: "chamber",
        chamber: action.chamber,
        level: action.level,
      };
    }
    case "UPDATE_IN_FLIGHT": {
      if (!state.save.inFlight) return state;
      return {
        ...state,
        save: {
          ...state.save,
          inFlight: { ...state.save.inFlight, ...action.patch },
        },
      };
    }
    case "ABANDON_RUN": {
      return { ...state, save: { ...state.save, inFlight: null }, view: "map" };
    }
    case "COMPLETE_LEVEL": {
      const scored = scoreLevel(action.report);
      const save = structuredClone(state.save);
      const ch = save.chambers[action.report.chamber];
      if (!ch.completedLevels.includes(action.report.level)) {
        ch.completedLevels.push(action.report.level);
      }
      const prev = ch.bestLevelScores[action.report.level] ?? 0;
      ch.bestLevelScores[action.report.level] = Math.max(prev, scored.score);
      ch.results.push(scored);
      if (ch.results.length > 24) ch.results.splice(0, ch.results.length - 24);
      save.inFlight = null;
      // unlock next chamber when all three levels of this one are complete
      const idx = CHAMBER_ORDER.indexOf(action.report.chamber);
      if (ch.completedLevels.length >= 3 && idx >= save.unlockedIndex && idx < 5) {
        save.unlockedIndex = idx + 1;
      }
      if (CHAMBER_ORDER.every((c) => save.chambers[c].completedLevels.length >= 3)) {
        save.finished = true;
      }
      const earned = evaluateAchievements(save);
      save.achievements.push(...earned);
      const nextLevel = action.report.level + 1;
      return {
        ...state,
        save,
        lastResult: scored,
        newAchievements: earned,
        view: "record",
        level: nextLevel <= 2 ? nextLevel : state.level,
      };
    }
    case "USE_HINT": {
      if (state.save.hintsRemaining <= 0) return state;
      return { ...state, save: { ...state.save, hintsRemaining: state.save.hintsRemaining - 1 } };
    }
    case "SET_SETTINGS": {
      return {
        ...state,
        save: { ...state.save, settings: { ...state.save.settings, ...action.patch } },
      };
    }
    case "OPEN_RESTART":
      return { ...state, modal: "restart" };
    case "CLOSE_MODAL":
      return { ...state, modal: null };
    case "CONFIRM_RESTART": {
      clearSave();
      return { ...init(), save: freshSave(), view: "cinematic" };
    }
    case "MARK_ACHIEVEMENTS_SEEN":
      return { ...state, newAchievements: [] };
    default:
      return state;
  }
}

interface GameCtx {
  state: GameState;
  dispatch: React.Dispatch<Action>;
}

const Ctx = createContext<GameCtx | null>(null);

export function GameProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, undefined, init);

  useEffect(() => {
    persistSave(state.save);
  }, [state.save]);

  const value = useMemo(() => ({ state, dispatch }), [state]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useGame(): GameCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useGame must be used inside GameProvider");
  return ctx;
}
