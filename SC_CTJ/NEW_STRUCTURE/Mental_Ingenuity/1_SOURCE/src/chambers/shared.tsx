import React, { useCallback, useEffect, useRef, useState } from "react";
import type { ChamberId, InFlight, LevelReport } from "../lib/types";
import { CHAMBER_META } from "../lib/content";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";

export interface SessionExtras {
  ruleChange?: { errorsAfter: number; adaptedOnFirstTry: boolean };
  recoveredAfterError: boolean;
}

export interface Session {
  chamber: ChamberId;
  level: number;
  par: number;
  moves: number;
  errors: number;
  attempts: number;
  hintsUsed: number;
  hintsLeft: number;
  msg: string;
  setMsg: (m: string) => void;
  addMove: (n?: number) => void;
  addError: () => void;
  events: string[];
  log: (e: string) => void;
  spendHint: () => boolean;
  finish: (
    detected: string,
    constraint: string,
    strategy: string,
    decisive: string,
    extras?: Partial<SessionExtras>
  ) => void;
  failAttempt: () => void;
  attemptKey: number;
}

/** Shared bookkeeping for one chamber level. */
export function useSession(chamber: ChamberId, level: number, par: number): Session {
  const { state, dispatch } = useGame();
  const saved = state.save.inFlight?.chamber === chamber && state.save.inFlight.level === level
    ? state.save.inFlight
    : null;
  const startedAt = useRef(saved?.startedAt ?? Date.now());
  const movesRef = useRef(saved?.moves ?? 0);
  const errorsRef = useRef(saved?.errors ?? 0);
  const attemptsRef = useRef(Math.max(1, saved?.attempts ?? 1));
  const hintsUsedRef = useRef(saved?.hintsUsed ?? 0);
  const [moves, setMoves] = useState(movesRef.current);
  const [errors, setErrors] = useState(errorsRef.current);
  const [attempts, setAttempts] = useState(attemptsRef.current);
  const [hintsUsed, setHintsUsed] = useState(hintsUsedRef.current);
  const [msg, setMsg] = useState("");
  const eventsRef = useRef<string[]>(saved?.events?.slice() ?? []);
  const [attemptKey, setAttemptKey] = useState(0);
  const errFlag = useRef(false);
  const recovered = useRef(false);

  const persistFlight = useCallback((patch: Partial<InFlight>) => {
    dispatch({ type: "UPDATE_IN_FLIGHT", patch });
  }, [dispatch]);
  const addMove = useCallback((n = 1) => {
    movesRef.current += n;
    setMoves(movesRef.current);
    persistFlight({ moves: movesRef.current });
  }, [persistFlight]);
  const addError = useCallback(() => {
    errorsRef.current += 1;
    setErrors(errorsRef.current);
    persistFlight({ errors: errorsRef.current });
    errFlag.current = true;
    audio.playSfx("invalid");
  }, [persistFlight]);
  const log = useCallback((e: string) => {
    eventsRef.current.push(e);
    persistFlight({ events: eventsRef.current.slice(-200) });
  }, [persistFlight]);

  const spendHint = useCallback((): boolean => {
    if (state.save.hintsRemaining <= 0) {
      setMsg("No hints remain. The ascent trusts your own reading.");
      return false;
    }
    dispatch({ type: "USE_HINT" });
    hintsUsedRef.current += 1;
    setHintsUsed(hintsUsedRef.current);
    persistFlight({ hintsUsed: hintsUsedRef.current });
    audio.playSfx("hint");
    log("Hint used");
    return true;
  }, [state.save.hintsRemaining, dispatch, log, persistFlight]);

  const finish = useCallback(
    (
      detected: string,
      constraint: string,
      strategy: string,
      decisive: string,
      extras?: Partial<SessionExtras>
    ) => {
      const report: LevelReport = {
        chamber,
        level,
        solved: true,
        moves: movesRef.current,
        parMoves: par,
        errors: errorsRef.current,
        attempts: attemptsRef.current,
        hintsUsed: hintsUsedRef.current,
        durationMs: Date.now() - startedAt.current,
        detected,
        constraint,
        strategy,
        decisive,
        events: eventsRef.current.slice(),
        ruleChange: extras?.ruleChange,
        recoveredAfterError: extras?.recoveredAfterError ?? (errFlag.current ? recovered.current : true),
      };
      audio.playSfx("complete");
      dispatch({ type: "COMPLETE_LEVEL", report });
    },
    [chamber, level, par, dispatch]
  );

  const failAttempt = useCallback(() => {
    attemptsRef.current += 1;
    setAttempts(attemptsRef.current);
    setAttemptKey((k) => k + 1);
    persistFlight({ attempts: attemptsRef.current });
    log("Attempt reset");
    audio.playSfx("reset");
  }, [log, persistFlight]);

  const markRecovered = useCallback(() => {
    if (errFlag.current) recovered.current = true;
  }, []);
  // expose recovery marker through closure on session object
  const session: Session = {
    chamber,
    level,
    par,
    moves,
    errors,
    attempts,
    hintsUsed,
    hintsLeft: state.save.hintsRemaining,
    msg,
    setMsg,
    addMove,
    addError,
    events: eventsRef.current,
    log,
    spendHint,
    finish,
    failAttempt,
    attemptKey,
  };
  (session as Session & { markRecovered: () => void }).markRecovered = markRecovered;
  return session;
}

export function markRecovered(s: Session): void {
  const f = (s as Session & { markRecovered?: () => void }).markRecovered;
  if (f) f();
}

/** Chrome shared by all chambers: objective, HUD, pause trigger, art backdrop. */
export function ChamberShell({
  chamber,
  level,
  session,
  onPause,
  onReset,
  undoLabel,
  onUndo,
  children,
}: {
  chamber: ChamberId;
  level: number;
  session: Session;
  onPause: () => void;
  onReset: () => void;
  undoLabel?: string;
  onUndo?: () => void;
  children: React.ReactNode;
}) {
  const meta = CHAMBER_META[chamber];
  return (
    <section className="chamber-view" aria-label={meta.name}>
      <div className="chamber-backdrop" aria-hidden="true">
        <img src={meta.art} alt="" loading="lazy" onError={(e) => ((e.target as HTMLImageElement).style.display = "none")} />
        <div className="chamber-backdrop-tint" />
      </div>
      <header className="chamber-head">
        <div>
          <h2 className="chamber-title">{meta.name}</h2>
          <p className="chamber-objective">
            <span className="obj-label">Objective, challenge {level + 1} of 3:</span>{" "}
            {meta.objectives[level]}
          </p>
        </div>
        <div className="chamber-hud" role="group" aria-label="Challenge status">
          <span className="hud-item">Moves: {session.moves}</span>
          <span className="hud-item">Par: {session.par}</span>
          <span className="hud-item">Attempt: {session.attempts}</span>
          <span className="hud-item">Hints left: {session.hintsLeft}</span>
          {onUndo ? (
            <Btn onClick={onUndo} ariaLabel={undoLabel ?? "Undo"} className="hud-btn">
              {undoLabel ?? "Undo"}
            </Btn>
          ) : null}
          <Btn onClick={onReset} ariaLabel="Reset this challenge" className="hud-btn">
            Reset
          </Btn>
          <Btn onClick={onPause} ariaLabel="Pause game" className="hud-btn">
            Pause
          </Btn>
        </div>
      </header>
      <div className="chamber-body">{children}</div>
      <p className="sr-live" aria-live="polite">
        {session.msg}
      </p>
      {session.msg ? <p className="chamber-msg">{session.msg}</p> : null}
    </section>
  );
}

/** Small utility: build a deterministic seed string. */
export function seedFor(chamber: string, level: number, attempt: number): string {
  return `${chamber}-L${level}-A${attempt}`;
}

export function useOsReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);
    const fn = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener("change", fn);
    return () => mq.removeEventListener("change", fn);
  }, []);
  return reduced;
}
