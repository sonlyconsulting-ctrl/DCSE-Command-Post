import React, { useCallback, useMemo, useState } from "react";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";
import { ChamberShell, Session, markRecovered, useSession } from "./shared";

interface Inputs {
  A: number;
  B: number;
  C: number;
}

interface CausalLevel {
  par: number;
  stabilityNeeded: number;
  nodeDefs: string[];
  targetText: string;
  explanation: string;
  tick: (prev: Record<string, number>, inp: Inputs, prevInp: Inputs) => Record<string, number>;
  goal: (vals: Record<string, number>) => boolean;
  goalParts: { label: string; test: (vals: Record<string, number>) => boolean }[];
}

const LEVELS: CausalLevel[] = [
  {
    par: 9,
    stabilityNeeded: 2,
    nodeDefs: ["E = B + C (immediate)", "D = A + B (arrives one tick late)", "F = D + E"],
    targetText: "Hold F at exactly 9 with E at 5 or above for two consecutive ticks.",
    explanation:
      "The winning chain ran A and B into D, one tick late, while B and C fed E immediately. F combined both streams, so the final value only existed after the delayed arm arrived. Holding the regulators still let the same chain repeat and stabilize.",
    tick: (prev, inp, prevInp) => {
      const E = inp.B + inp.C;
      const D = prevInp.A + prevInp.B;
      return { E, D, F: D + E };
    },
    goal: (v) => v.F === 9 && v.E >= 5,
    goalParts: [
      { label: "F equals 9", test: (v) => v.F === 9 },
      { label: "E at least 5", test: (v) => v.E >= 5 },
    ],
  },
  {
    par: 10,
    stabilityNeeded: 2,
    nodeDefs: ["E = B + C (immediate)", "D = A + B (arrives one tick late)", "H = 8 − D"],
    targetText: "Hold H at exactly 4 with E at 5 or below for two consecutive ticks.",
    explanation:
      "H inverts the delayed stream: the higher D climbs, the lower H falls. The chain that mattered ran A and B into D, waited one tick for it to land, then let the inversion produce 4. Keeping B and C small held E under its ceiling at the same time.",
    tick: (prev, inp, prevInp) => {
      const E = inp.B + inp.C;
      const D = prevInp.A + prevInp.B;
      return { E, D, H: 8 - D };
    },
    goal: (v) => v.H === 4 && v.E <= 5,
    goalParts: [
      { label: "H equals 4", test: (v) => v.H === 4 },
      { label: "E at most 5", test: (v) => v.E <= 5 },
    ],
  },
  {
    par: 12,
    stabilityNeeded: 1,
    nodeDefs: [
      "E = B + C (immediate)",
      "D = A + B (arrives one tick late)",
      "P = |A − C|; if P > 3 the flow is halved",
      "F = D + E (halved when P > 3)",
      "K counts consecutive ticks where F ≥ 8; any weaker tick zeroes it",
    ],
    targetText: "Raise K to 3 by feeding F at 8 or above for three consecutive ticks, with E at 4 or above.",
    explanation:
      "The memory node K only counts pressure that repeats. The decisive constraint was balance: A and C had to stay close together, because a wide gap halved the flow. With the gap closed, A and B fed the delayed arm, B and C fed the immediate arm, and F stayed above the threshold three ticks in a row.",
    tick: (prev, inp, prevInp) => {
      const E = inp.B + inp.C;
      const D = prevInp.A + prevInp.B;
      const P = Math.abs(inp.A - inp.C);
      let F = D + E;
      if (P > 3) F = Math.floor(F / 2);
      const K = F >= 8 ? (prev.K ?? 0) + 1 : 0;
      return { E, D, P, F, K };
    },
    goal: (v) => v.K >= 3 && v.E >= 4,
    goalParts: [
      { label: "K reaches 3", test: (v) => v.K >= 3 },
      { label: "E at least 4", test: (v) => v.E >= 4 },
    ],
  },
];

export default function CausalLabyrinth({
  level,
  paused,
  onPause,
}: {
  level: number;
  paused: boolean;
  onPause: () => void;
}) {
  const cfg = LEVELS[level];
  const session = useSession("causal", level, cfg.par);
  const [inputs, setInputs] = useState<Inputs>({ A: 0, B: 0, C: 0 });
  const [prevInp, setPrevInp] = useState<Inputs>({ A: 0, B: 0, C: 0 });
  const [vals, setVals] = useState<Record<string, number>>({});
  const [ticks, setTicks] = useState(0);
  const [stability, setStability] = useState(0);
  const [done, setDone] = useState(false);
  const [history, setHistory] = useState<string[]>([]);

  const pendingD = inputs.A + inputs.B;

  const adjust = useCallback(
    (k: keyof Inputs, d: number) => {
      if (done || paused) return;
      setInputs((inp) => {
        const v = Math.max(0, Math.min(4, inp[k] + d));
        if (v === inp[k]) return inp;
        session.addMove();
        audio.playSfx("select");
        return { ...inp, [k]: v };
      });
    },
    [done, paused, session]
  );

  const advance = useCallback(() => {
    if (done || paused) return;
    session.addMove();
    const next = cfg.tick(vals, inputs, prevInp);
    setVals(next);
    setPrevInp(inputs);
    setTicks((t) => t + 1);
    setHistory((h) => [...h.slice(-4), `Tick ${ticks + 1}: F ${next.F ?? "•"} · E ${next.E}${"K" in next ? ` · K ${next.K}` : ""}`]);
    audio.playSfx("connect");
    const ok = cfg.goal(next);
    const stab = ok ? stability + 1 : 0;
    setStability(stab);
    markRecovered(session);
    if (ok && stab >= cfg.stabilityNeeded) {
      setDone(true);
      session.setMsg("The system holds. The gate reads stable.");
      window.setTimeout(() => {
        session.finish(
          "The delayed arm and the immediate arm feeding one output",
          "A delayed node that forced you to plan one tick ahead",
          session.errors === 0 && ticks + 1 <= cfg.par
            ? "Set the regulators once from the target values backward, then waited"
            : "Experimented with regulator settings and read the downstream response",
          `The tick where F settled at ${next.F ?? "target"} and the stability counter filled`,
          { recoveredAfterError: session.errors > 0 }
        );
      }, 700);
      audio.playSfx("activate");
    } else if (!ok) {
      session.setMsg("The gate is not stable. Watch which node is missing its mark.");
    }
  }, [done, paused, cfg, vals, inputs, prevInp, ticks, stability, session]);

  const resetExperiment = useCallback(() => {
    setInputs({ A: 0, B: 0, C: 0 });
    setPrevInp({ A: 0, B: 0, C: 0 });
    setVals({});
    setTicks(0);
    setStability(0);
    setDone(false);
    setHistory([]);
    session.failAttempt();
  }, [session]);

  const hint = useCallback(() => {
    if (done) return;
    if (!session.spendHint()) return;
    const hints = [
      "Work backward: choose B first, since B feeds both arms. Then let A and C complete the sums.",
      "The delayed arm remembers what you set one tick ago. Set it early, then hold everything still.",
      "Keep A and C close together. A wide gap halves the flow and erases the memory count.",
    ];
    session.setMsg(hints[level]);
  }, [done, level, session]);

  const nodeNames = level === 0 ? ["D", "E", "F"] : level === 1 ? ["D", "E", "H"] : ["D", "E", "P", "F", "K"];

  return (
    <ChamberShell chamber="causal" level={level} session={session} onPause={onPause} onReset={resetExperiment}>
      <div className="causal-layout">
        <div className={`causal-board ${paused ? "veiled" : ""}`} role="group" aria-label="System state board">
          <div className="causal-dials" role="group" aria-label="Regulators">
            {(["A", "B", "C"] as const).map((k) => (
              <div className="dial" key={k}>
                <span className="dial-name">Regulator {k}</span>
                <div className="dial-controls">
                  <Btn onClick={() => adjust(k, -1)} ariaLabel={`Decrease regulator ${k}`} disabled={done}>−</Btn>
                  <span className="dial-val" aria-live="polite">{inputs[k]}</span>
                  <Btn onClick={() => adjust(k, 1)} ariaLabel={`Increase regulator ${k}`} disabled={done}>+</Btn>
                </div>
              </div>
            ))}
            <div className="dial-note">D will receive A + B = {pendingD} on the next tick.</div>
          </div>
          <div className="causal-nodes">
            {nodeNames.map((n) => (
              <div className={`node ${cfg.goalParts.every((g) => g.test(vals)) && vals[n] !== undefined ? "" : ""}`} key={n}>
                <span className="node-name">{n}</span>
                <span className="node-val">{vals[n] !== undefined ? vals[n] : "…"}</span>
              </div>
            ))}
          </div>
          <div className="causal-goals">
            {cfg.goalParts.map((g) => (
              <span key={g.label} className={`goal-chip ${vals && Object.keys(vals).length > 0 && g.test(vals) ? "ok" : ""}`}>
                {g.label}
              </span>
            ))}
            <span className="goal-chip stability">
              Stability: {stability} of {cfg.stabilityNeeded}
            </span>
          </div>
        </div>
        <div className="causal-side">
          <p className="side-note">{cfg.targetText}</p>
          <ul className="side-note dim node-defs">
            {cfg.nodeDefs.map((d) => (
              <li key={d}>{d}</li>
            ))}
          </ul>
          {history.length > 0 ? (
            <ul className="side-note dim">
              {history.map((h, i) => (
                <li key={i}>{h}</li>
              ))}
            </ul>
          ) : null}
          <div className="side-controls">
            <Btn onClick={advance} variant="gold" disabled={done || paused} ariaLabel="Advance the system by one tick">
              Advance time
            </Btn>
            <Btn onClick={hint} disabled={done} ariaLabel="Use a hint about the system">
              Hint ({session.hintsLeft})
            </Btn>
          </div>
          <p className="side-note dim">Ticks: {ticks} · Experiments reset cleanly whenever you need.</p>
        </div>
      </div>
    </ChamberShell>
  );
}
