import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { ChamberId } from "../lib/types";
import { Rand } from "../lib/rng";
import { audio } from "../audio/engine";
import { useGame } from "../state/store";
import { Btn } from "../components/ui";
import { ChamberShell, Session, markRecovered, seedFor, useSession } from "./shared";

const GLYPHS = ["◆", "▲", "●", "■", "✦", "◈", "✳", "◎"];

interface LevelCfg {
  n: number;
  len: number;
  noise: number;
  family: "cardinal" | "diagonal" | "leap";
  familyName: string;
}

const LEVELS: LevelCfg[] = [
  { n: 5, len: 4, noise: 2, family: "cardinal", familyName: "a cardinal step rhythm" },
  { n: 6, len: 6, noise: 4, family: "diagonal", familyName: "a diagonal weave" },
  { n: 7, len: 7, noise: 6, family: "leap", familyName: "a leaping knight rhythm" },
];

const DIRS: Record<string, [number, number][]> = {
  cardinal: [[-1, 0], [1, 0], [0, -1], [0, 1]],
  diagonal: [[-1, -1], [-1, 1], [1, -1], [1, 1]],
  leap: [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2]],
};

function genPath(rnd: Rand, n: number, len: number, family: string): number[] {
  for (let tries = 0; tries < 60; tries++) {
    const visited = new Set<number>();
    let r = rnd.int(n);
    let c = rnd.int(n);
    const path: number[] = [r * n + c];
    visited.add(r * n + c);
    let ok = true;
    while (path.length < len) {
      const dirs = rnd.shuffle(DIRS[family]);
      let moved = false;
      for (const [dr, dc] of dirs) {
        const nr = r + dr;
        const nc = c + dc;
        if (nr < 0 || nc < 0 || nr >= n || nc >= n) continue;
        const id = nr * n + nc;
        if (visited.has(id)) continue;
        visited.add(id);
        path.push(id);
        r = nr;
        c = nc;
        moved = true;
        break;
      }
      if (!moved) {
        ok = false;
        break;
      }
    }
    if (ok) return path;
  }
  // Fallback straight line, always valid.
  return Array.from({ length: len }, (_, i) => i);
}

export default function SignalChamber({
  level,
  paused,
  onPause,
}: {
  level: number;
  paused: boolean;
  onPause: () => void;
}) {
  const cfg = LEVELS[level];
  const par = cfg.len;
  const session = useSession("signal", level, par);
  const { state } = useGame();
  const reducedMotion =
    state.save.settings.reducedMotion || window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const [attemptSeed, setAttemptSeed] = useState(0);
  const seed = seedFor("signal", level, attemptSeed);
  const { path, noiseCells, glyphOf } = useMemo(() => {
    const rnd = new Rand(seed);
    const path = genPath(rnd, cfg.n, cfg.len, cfg.family);
    const pathSet = new Set(path);
    const noiseCells: number[] = [];
    while (noiseCells.length < cfg.noise) {
      const id = rnd.int(cfg.n * cfg.n);
      if (!pathSet.has(id) && !noiseCells.includes(id)) noiseCells.push(id);
    }
    const glyphOf = new Map<number, string>();
    path.forEach((p, i) => glyphOf.set(p, GLYPHS[i % GLYPHS.length]));
    return { path, noiseCells, glyphOf };
  }, [seed, cfg]);

  const [phase, setPhase] = useState<"showing" | "recall" | "done">("showing");
  const [litCell, setLitCell] = useState<number | null>(null);
  const [noiseLit, setNoiseLit] = useState<number | null>(null);
  const [locked, setLocked] = useState<number[]>([]);
  const [wrongFlash, setWrongFlash] = useState<number | null>(null);
  const [hintCell, setHintCell] = useState<number | null>(null);
  const [replays, setReplays] = useState(0);
  const timers = useRef<number[]>([]);

  const clearTimers = useCallback(() => {
    timers.current.forEach((t) => window.clearTimeout(t));
    timers.current = [];
  }, []);

  const runShow = useCallback(() => {
    clearTimers();
    setPhase("showing");
    setLocked([]);
    setLitCell(null);
    const stepMs = reducedMotion ? 850 : 620;
    path.forEach((cell, i) => {
      timers.current.push(
        window.setTimeout(() => {
          setLitCell(cell);
          audio.playSfx("connect");
          timers.current.push(
            window.setTimeout(() => setLitCell((c) => (c === cell ? null : c)), stepMs * 0.6)
          );
        }, 600 + i * stepMs)
      );
    });
    // noise flashes between steps
    const rnd = new Rand(seed + ":noise");
    noiseCells.forEach((cell) => {
      const t = 600 + rnd.int(path.length * stepMs);
      timers.current.push(
        window.setTimeout(() => {
          setNoiseLit(cell);
          timers.current.push(window.setTimeout(() => setNoiseLit(null), 350));
        }, t)
      );
    });
    timers.current.push(
      window.setTimeout(() => {
        setPhase("recall");
        session.setMsg("Trace the true signal in order. Noise cells never pulsed in sequence.");
      }, 600 + path.length * stepMs + 400)
    );
  }, [path, noiseCells, seed, reducedMotion, clearTimers, session]);

  useEffect(() => {
    if (!paused && phase !== "done") runShow();
    return clearTimers;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seed, paused, attemptSeed]);

  const clickCell = useCallback(
    (id: number) => {
      if (phase !== "recall" || paused) return;
      session.addMove();
      const expected = path[locked.length];
      if (id === expected) {
        markRecovered(session);
        const next = [...locked, id];
        setLocked(next);
        audio.playSfx("place");
        setHintCell(null);
        if (next.length === path.length) {
          setPhase("done");
          const r = Math.floor(id / cfg.n) + 1;
          const c = (id % cfg.n) + 1;
          session.setMsg("The pathway accepts the signal.");
          session.finish(
            `The signal moved in ${cfg.familyName}`,
            "Separating sequenced pulses from unscheduled noise flashes",
            replays > 0 ? "Watched the presentation again, then reproduced the order" : "Held the pulse order from a single viewing",
            `The final pulse at row ${r}, column ${c}`,
            { recoveredAfterError: session.errors > 0 }
          );
        } else {
          session.setMsg(`Signal locked: ${next.length} of ${path.length}.`);
        }
      } else {
        session.addError();
        setWrongFlash(id);
        window.setTimeout(() => setWrongFlash(null), 500);
        session.setMsg("That cell never carried the true signal. Keep the order.");
      }
    },
    [phase, paused, path, locked, cfg.n, session, replays]
  );

  const hint = useCallback(() => {
    if (phase !== "recall") return;
    if (!session.spendHint()) return;
    const next = path[locked.length];
    setHintCell(next);
    window.setTimeout(() => setHintCell(null), 1600);
  }, [phase, path, locked, session]);

  const replay = useCallback(() => {
    if (phase !== "recall") return;
    setReplays((r) => r + 1);
    session.log("Signal replayed");
    session.setMsg("The presentation runs again. Watch the order, not the noise.");
    runShow();
  }, [phase, runShow, session]);

  useEffect(() => {
    session.setMsg("The chamber is transmitting. Watch which cells pulse in order.");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seed]);

  useEffect(() => {
    if (import.meta.env.MODE !== "test") return;
    (window as unknown as Record<string, unknown>).__MI_TEST__ = {
      chamber: "signal",
      next: locked.length < path.length ? path[locked.length] : -1,
    };
  }, [locked, path]);

  return (
    <ChamberShell chamber="signal" level={level} session={session} onPause={onPause} onReset={() => { session.failAttempt(); setAttemptSeed((s) => s + 1); }}>
      <div className="signal-layout">
        <div
          className={`signal-grid ${paused ? "veiled" : ""}`}
          style={{ gridTemplateColumns: `repeat(${cfg.n}, minmax(0, 1fr))` }}
          role="group"
          aria-label={`Signal field, ${cfg.n} by ${cfg.n} grid`}
        >
          {Array.from({ length: cfg.n * cfg.n }, (_, id) => {
            const isLit = litCell === id;
            const isNoise = noiseLit === id;
            const isLocked = locked.includes(id);
            const lockIdx = locked.indexOf(id);
            const isHint = hintCell === id;
            const isWrong = wrongFlash === id;
            return (
              <button
                key={id}
                type="button"
                className={[
                  "signal-cell",
                  isLit ? "lit" : "",
                  isNoise ? "noise" : "",
                  isLocked ? "locked" : "",
                  isHint ? "hinted" : "",
                  isWrong ? "wrong" : "",
                ].join(" ")}
                onClick={() => clickCell(id)}
                disabled={phase !== "recall"}
                aria-label={`Cell row ${Math.floor(id / cfg.n) + 1}, column ${(id % cfg.n) + 1}${
                  isLocked ? `, locked as step ${lockIdx + 1}` : ""
                }`}
              >
                {isLocked ? <span className="glyph">{glyphOf.get(id)}</span> : null}
                {isLit ? <span className="glyph pulse">{glyphOf.get(id)}</span> : null}
              </button>
            );
          })}
        </div>
        <div className="signal-side">
          <p className="side-note">
            The true signal pulses cell to cell in one unbroken order. Noise flashes whenever it
            pleases. Reproduce the sequence.
          </p>
          <p className="side-note dim">
            Sound is optional: every pulse you hear is also visible.
          </p>
          <div className="side-controls">
            <Btn onClick={replay} disabled={phase !== "recall"} ariaLabel="Replay the signal presentation">
              Replay signal
            </Btn>
            <Btn onClick={hint} disabled={phase !== "recall"} ariaLabel="Use a hint to reveal the next cell">
              Hint ({session.hintsLeft})
            </Btn>
          </div>
          <p className="side-note dim">
            Phase: {phase === "showing" ? "transmitting" : phase === "recall" ? "your turn" : "accepted"} · Progress:{" "}
            {locked.length} of {path.length}
          </p>
        </div>
      </div>
    </ChamberShell>
  );
}
