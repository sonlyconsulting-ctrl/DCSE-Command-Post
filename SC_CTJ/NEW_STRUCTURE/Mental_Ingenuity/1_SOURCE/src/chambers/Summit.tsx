import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Rand } from "../lib/rng";
import { audio } from "../audio/engine";
import { useGame } from "../state/store";
import { Btn } from "../components/ui";
import { ChamberShell, Session, markRecovered, seedFor, useSession } from "./shared";

type Stage = "trace-show" | "trace-recall" | "route" | "align" | "gate" | "done";

const GLYPHS = ["◆", "▲", "●"];

function walkPath(rnd: Rand, n: number, len: number): number[] {
  const dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];
  for (let tries = 0; tries < 40; tries++) {
    const visited = new Set<number>();
    let r = rnd.int(n);
    let c = rnd.int(n);
    const path = [r * n + c];
    visited.add(r * n + c);
    let ok = true;
    while (path.length < len) {
      const ds = rnd.shuffle(dirs);
      let moved = false;
      for (const [dr, dc] of ds) {
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
      if (!moved) { ok = false; break; }
    }
    if (ok) return path;
  }
  return [0, 1, 2, 3].slice(0, len);
}

interface Gate {
  count: number;
  shape: string;
  glyph: string;
}

export default function Summit({
  level,
  paused,
  onPause,
}: {
  level: number;
  paused: boolean;
  onPause: () => void;
}) {
  const { state } = useGame();

  // Adaptive difficulty: strong prior performance raises the difficulty variant.
  const priorStrength = useMemo(() => {
    const scores: number[] = [];
    for (const id of ["signal", "forge", "perspective", "causal", "paradox"] as const) {
      const bl = state.save.chambers[id].bestLevelScores;
      Object.values(bl).forEach((s) => scores.push(s / 300));
    }
    if (scores.length === 0) return 0.4;
    return scores.reduce((a, b) => a + b, 0) / scores.length;
  }, [state.save]);
  const hard = priorStrength >= 0.7;

  const pathLen = hard ? 4 : 3;
  const par = pathLen + 6;
  const session = useSession("summit", level, par);

  const [attemptSeed, setAttemptSeed] = useState(0);
  const seed = seedFor("summit", level, attemptSeed) + (hard ? "-hard" : "");
  const { path, ringScramble, gates } = useMemo(() => {
    const rnd = new Rand(seed);
    const path = walkPath(rnd, 4, pathLen);
    let ring: [number, number] = [0, 0];
    for (let i = 0; i < 3; i++) {
      const which = rnd.int(2);
      const sign = rnd.chance(0.5) ? 1 : -1;
      if (which === 0) ring = [(ring[0] + sign + 8) % 8, (ring[1] - sign + 8) % 8];
      else ring = [ring[0], (ring[1] + sign + 8) % 8];
    }
    if (ring[0] === 0 && ring[1] === 0) ring = [3, 5];
    const gates: Gate[] = hard
      ? [
          { count: 4, shape: "diamond", glyph: "◆" },
          { count: 3, shape: "diamond", glyph: "◆" },
          { count: 3, shape: "ring", glyph: "●" },
        ]
      : [
          { count: 2, shape: "triangle", glyph: "▲" },
          { count: 3, shape: "diamond", glyph: "◆" },
          { count: 5, shape: "ring", glyph: "●" },
        ];
    return { path, ringScramble: ring, gates };
  }, [seed, pathLen, hard]);

  const [stage, setStage] = useState<Stage>("trace-show");
  const [litCell, setLitCell] = useState<number | null>(null);
  const [locked, setLocked] = useState<number[]>([]);
  const [lawChanged, setLawChanged] = useState(false);
  const [mirrors, setMirrors] = useState<Record<string, string>>({ "0,2": "/", "2,2": "/" });
  const [ringOffs, setRingOffs] = useState<[number, number]>(ringScramble);
  const [rulePulse, setRulePulse] = useState(false);
  const [gateErrors, setGateErrors] = useState(0);
  const [firstGatePick, setFirstGatePick] = useState<boolean | null>(null);
  const timers = useRef<number[]>([]);

  useEffect(() => {
    setStage("trace-show");
    setLocked([]);
    setLitCell(null);
    setLawChanged(false);
    setMirrors({ "0,2": "/", "2,2": "/" });
    setRingOffs(ringScramble);
    setGateErrors(0);
    setFirstGatePick(null);
    setRulePulse(false);
  }, [seed, ringScramble]);

  const clearTimers = useCallback(() => {
    timers.current.forEach((t) => window.clearTimeout(t));
    timers.current = [];
  }, []);

  // stage 1: trace presentation
  useEffect(() => {
    if (stage !== "trace-show" || paused) return;
    clearTimers();
    const stepMs = state.save.settings.reducedMotion ? 850 : 620;
    path.forEach((cell, i) => {
      timers.current.push(
        window.setTimeout(() => {
          setLitCell(cell);
          audio.playSfx("connect");
          timers.current.push(window.setTimeout(() => setLitCell((c) => (c === cell ? null : c)), stepMs * 0.6));
        }, 500 + i * stepMs)
      );
    });
    timers.current.push(
      window.setTimeout(() => {
        setStage("trace-recall");
        session.setMsg("Trace the summit signal in order.");
      }, 500 + path.length * stepMs + 300)
    );
    return clearTimers;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stage, paused, seed]);

  const triggerLawChange = useCallback(() => {
    setLawChanged(true);
    setRulePulse(true);
    audio.playSfx("rule_change");
    session.log("The Summit revised its law: parity inverts, and the sigil must match the aligned mark");
    session.setMsg("A new law settles over the gate. Read the panel again before you choose.");
    window.setTimeout(() => setRulePulse(false), 2600);
  }, [session]);

  const traceClick = useCallback(
    (id: number) => {
      if (stage !== "trace-recall" || paused) return;
      session.addMove();
      const expected = path[locked.length];
      if (id === expected) {
        markRecovered(session);
        const next = [...locked, id];
        setLocked(next);
        audio.playSfx("place");
        if (next.length === path.length) {
          triggerLawChange();
          window.setTimeout(() => setStage("route"), 1200);
        }
      } else {
        session.addError();
        session.setMsg("That cell never carried the summit signal.");
      }
    },
    [stage, paused, path, locked, session, triggerLawChange]
  );

  // stage 2: route
  const traceRoute = useCallback((m: Record<string, string>) => {
    let dir: [number, number] = [0, 1];
    let r = 0;
    let c = 0;
    const reflect: Record<string, Record<string, [number, number]>> = {
      "/": { "0,1": [-1, 0], "0,-1": [1, 0], "1,0": [0, -1], "-1,0": [0, 1] },
      "\\": { "0,1": [1, 0], "0,-1": [-1, 0], "1,0": [0, 1], "-1,0": [0, -1] },
    };
    for (let s = 0; s < 40; s++) {
      const nr = r + dir[0];
      const nc = c + dir[1];
      if (nr < 0 || nc < 0 || nr >= 3 || nc >= 5) return { pts: [], hit: false };
      if (nr === 2 && nc === 4) return { pts: [], hit: true };
      const mk = `${nr},${nc}`;
      if (m[mk]) {
        dir = reflect[m[mk]][`${dir[0]},${dir[1]}`] ?? dir;
      }
      r = nr;
      c = nc;
    }
    return { pts: [], hit: false };
  }, []);

  const routeHit = traceRoute(mirrors).hit;

  const rotateMirror = useCallback(
    (k: string) => {
      if (stage !== "route" || paused) return;
      session.addMove();
      const next = { ...mirrors, [k]: mirrors[k] === "/" ? "\\" : "/" };
      setMirrors(next);
      markRecovered(session);
      audio.playSfx("rotate");
      if (traceRoute(next).hit) {
        audio.playSfx("activate");
        session.setMsg("The beam seats into the summit lens. The rings wake.");
        window.setTimeout(() => setStage("align"), 800);
      }
    },
    [stage, paused, mirrors, session, traceRoute]
  );

  // stage 3: align
  const rotateRing = useCallback(
    (which: 0 | 1, sign: number) => {
      if (stage !== "align" || paused) return;
      session.addMove();
      const next: [number, number] = [...ringOffs] as [number, number];
      if (which === 0) {
        next[0] = (next[0] + sign + 8) % 8;
        next[1] = (next[1] - sign + 8) % 8;
      } else {
        next[1] = (next[1] + sign + 8) % 8;
      }
      setRingOffs(next);
      markRecovered(session);
      audio.playSfx("rotate");
      if (next[0] === 0 && next[1] === 0) {
        audio.playSfx("activate");
        session.setMsg("Both marks stand on the axis. The gates surface. Choose with the revised law in mind.");
        window.setTimeout(() => setStage("gate"), 800);
      }
    },
    [stage, paused, ringOffs, session]
  );

  // stage 4: gate
  const correctGate = gates.findIndex((g) => g.count % 2 === 1 && g.shape === "diamond");

  const pickGate = useCallback(
    (i: number) => {
      if (stage !== "gate" || paused) return;
      session.addMove();
      if (i === correctGate) {
        if (firstGatePick === null) setFirstGatePick(true);
        setStage("done");
        session.setMsg("The gate accepts. The ascent completes.");
        audio.playSfx("final");
        window.setTimeout(() => {
          session.finish(
            hard ? "An adapted gate law: odd parity matched to the aligned sigil" : "The revised gate law: odd parity and the diamond sigil",
            "The law changed mid-ascent, and the old rule became a trap",
            "Re-read the law panel after the revision and filtered gates by both conditions",
            "The gate carrying an odd glyph count and the diamond sigil",
            {
              ruleChange: { errorsAfter: gateErrors, adaptedOnFirstTry: firstGatePick === null ? true : firstGatePick === true && gateErrors === 0 },
              recoveredAfterError: session.errors > 0,
            }
          );
        }, 1400);
      } else {
        session.addError();
        if (firstGatePick === null) setFirstGatePick(false);
        setGateErrors((e) => e + 1);
        session.setMsg(
          gateErrors === 0
            ? "The gate refuses. The law moved while you were climbing. Read the panel again."
            : "Still refused. Test the law against each gate, one condition at a time."
        );
      }
    },
    [stage, paused, correctGate, firstGatePick, gateErrors, session, hard]
  );

  const hint = useCallback(() => {
    if (!session.spendHint()) return;
    if (stage === "trace-recall") {
      session.setMsg(`The next true cell is row ${Math.floor(path[locked.length] / 4) + 1}, column ${(path[locked.length] % 4) + 1}.`);
    } else if (stage === "route") {
      const wrong = Object.keys(mirrors).find((k) => mirrors[k] !== "\\");
      session.setMsg(wrong ? "A mirror glows. Turn it once." : "Both mirrors face the right way. Follow the beam.");
    } else if (stage === "align") {
      session.setMsg("Turning the outer ring drags the inner ring against it. Use the inner ring alone for fine work.");
    } else if (stage === "gate") {
      session.setMsg("The law written on the panel now is the law that applies. Check both conditions.");
    }
  }, [stage, locked, mirrors, path, session]);

  const lawText = lawChanged
    ? "Revised law: choose the gate with an ODD glyph count whose sigil matches the aligned mark (the diamond)."
    : "Gate law: choose the gate whose glyph count is even.";

  useEffect(() => {
    if (import.meta.env.MODE !== "test") return;
    (window as unknown as Record<string, unknown>).__MI_TEST__ = {
      chamber: "summit",
      stage,
      next: locked.length < path.length ? path[locked.length] : -1,
      wrongMirrors: Object.keys(mirrors).filter((k) => mirrors[k] !== "\\"),
      ringOffs,
      correctGate,
      lawChanged,
    };
  }, [stage, locked, path, mirrors, ringOffs, correctGate, lawChanged]);

  const CS = 56;

  return (
    <ChamberShell
      chamber="summit"
      level={level}
      session={session}
      onPause={onPause}
      onReset={() => {
        clearTimers();
        session.failAttempt();
        setAttemptSeed((s) => s + 1);
      }}
    >
      <div className={`summit-layout ${paused ? "veiled" : ""}`}>
        <div className={`summit-law ${rulePulse ? "pulse" : ""}`} role="status">
          <span className="law-label">Law of the gate</span>
          <span className="law-text">{lawText}</span>
          {lawChanged ? <span className="law-changed">The law was revised during this ascent.</span> : null}
        </div>

        {stage === "trace-show" || stage === "trace-recall" ? (
          <div className="summit-stage">
            <h3 className="stage-title">Discipline one: the signal</h3>
            <div className="signal-grid small" style={{ gridTemplateColumns: "repeat(4, minmax(0, 1fr))" }} role="group" aria-label="Summit signal grid, four by four">
              {Array.from({ length: 16 }, (_, id) => (
                <button
                  key={id}
                  type="button"
                  className={`signal-cell ${litCell === id ? "lit" : ""} ${locked.includes(id) ? "locked" : ""}`}
                  onClick={() => traceClick(id)}
                  disabled={stage !== "trace-recall"}
                  aria-label={`Summit cell row ${Math.floor(id / 4) + 1}, column ${(id % 4) + 1}`}
                >
                  {locked.includes(id) || litCell === id ? <span className="glyph">{GLYPHS[locked.includes(id) ? locked.indexOf(id) : path.indexOf(id)] ?? "✦"}</span> : null}
                </button>
              ))}
            </div>
          </div>
        ) : null}

        {stage === "route" ? (
          <div className="summit-stage">
            <h3 className="stage-title">Discipline two: the route</h3>
            <div className="summit-route" role="group" aria-label="Beam route, five columns by three rows">
              {Array.from({ length: 15 }, (_, i) => {
                const r = Math.floor(i / 5);
                const c = i % 5;
                const k = `${r},${c}`;
                if (r === 0 && c === 0) return <div key={k} className="rt-cell src" aria-label="Emitter">◈</div>;
                if (r === 2 && c === 4) return <div key={k} className={`rt-cell tgt ${routeHit ? "hit" : ""}`} aria-label="Summit lens">◎</div>;
                if (mirrors[k]) {
                  return (
                    <button key={k} type="button" className="rt-cell mirror" onClick={() => rotateMirror(k)} aria-label={`Mirror at row ${r + 1}, column ${c + 1}, facing ${mirrors[k] === "/" ? "north east" : "south east"}. Activate to rotate.`}>
                      {mirrors[k] === "/" ? "╱" : "╲"}
                    </button>
                  );
                }
                return <div key={k} className="rt-cell">{routeHit ? "" : ""}</div>;
              })}
            </div>
            <p className="side-note dim">The emitter fires right. Seat the beam in the lens.</p>
          </div>
        ) : null}

        {stage === "align" ? (
          <div className="summit-stage">
            <h3 className="stage-title">Discipline three: the alignment</h3>
            <svg viewBox="0 0 300 300" className="summit-align" role="group" aria-label="Two coupled rings. Bring both gold marks to the top axis.">
              <line x1={150} y1={16} x2={150} y2={44} className="persp-axis-notch" />
              {[110, 70].map((rad, i) => (
                <g key={i}>
                  <circle cx={150} cy={150} r={rad} className={`persp-ring ${ringOffs[i] === 0 ? "aligned" : ""}`} />
                  {(() => {
                    const a = -Math.PI / 2 + ringOffs[i] * ((2 * Math.PI) / 8);
                    const x = 150 + Math.cos(a) * rad;
                    const y = 150 + Math.sin(a) * rad;
                    return <path d={`M${x} ${y - 7} L${x + 5} ${y} L${x} ${y + 7} L${x - 5} ${y} Z`} className={`persp-gold ${ringOffs[i] === 0 ? "home" : ""}`} />;
                  })()}
                </g>
              ))}
              <circle cx={150} cy={150} r={8} className="persp-hub" />
            </svg>
            <div className="persp-controls" role="group" aria-label="Summit ring controls">
              <div className="persp-control-row">
                <span className="ring-name">outer ring</span>
                <Btn onClick={() => rotateRing(0, -1)} ariaLabel="Rotate outer ring counter clockwise">⟲</Btn>
                <Btn onClick={() => rotateRing(0, 1)} ariaLabel="Rotate outer ring clockwise">⟳</Btn>
              </div>
              <div className="persp-control-row">
                <span className="ring-name">inner ring</span>
                <Btn onClick={() => rotateRing(1, -1)} ariaLabel="Rotate inner ring counter clockwise">⟲</Btn>
                <Btn onClick={() => rotateRing(1, 1)} ariaLabel="Rotate inner ring clockwise">⟳</Btn>
              </div>
            </div>
            <p className="side-note dim">The outer ring is gear linked: turning it turns the inner ring against it.</p>
          </div>
        ) : null}

        {stage === "gate" || stage === "done" ? (
          <div className="summit-stage">
            <h3 className="stage-title">The final synthesis: choose the gate</h3>
            <div className="summit-gates" role="group" aria-label="Three gates. Choose one under the current law.">
              {gates.map((g, i) => (
                <button key={i} type="button" className={`summit-gate ${stage === "done" && i === correctGate ? "open" : ""}`} onClick={() => pickGate(i)} disabled={stage === "done"} aria-label={`Gate ${i + 1}: ${g.count} glyphs, ${g.shape} sigil`}>
                  <span className="gate-sigil" aria-hidden="true">{g.glyph}</span>
                  <span className="gate-count">{g.count} glyphs</span>
                  <span className="gate-name">Gate {i + 1}</span>
                </button>
              ))}
            </div>
          </div>
        ) : null}

        <div className="summit-side">
          <p className="side-note dim">
            Stage: {stage === "trace-show" ? "signal transmitting" : stage === "trace-recall" ? "trace the signal" : stage === "route" ? "route the beam" : stage === "align" ? "align the rings" : stage === "gate" ? "choose the gate" : "ascent complete"}
          </p>
          <p className="side-note dim">Adaptive reading of your ascent so far: {hard ? "tight tolerances" : "standard tolerances"}.</p>
          <div className="side-controls">
            <Btn onClick={hint} disabled={stage === "done"} ariaLabel="Use a hint">Hint ({session.hintsLeft})</Btn>
          </div>
        </div>
      </div>
    </ChamberShell>
  );
}
