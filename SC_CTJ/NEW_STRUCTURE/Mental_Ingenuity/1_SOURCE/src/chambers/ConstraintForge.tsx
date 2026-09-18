import React, { useCallback, useEffect, useMemo, useState } from "react";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";
import { ChamberShell, Session, markRecovered, useSession } from "./shared";

interface ForgeLevel {
  rows: string[];
  par: number;
  budget: number;
  solution: Record<string, string>;
}

const LEVELS: ForgeLevel[] = [
  {
    rows: ["S . / . .", ". . . . .", ". . / . T", ". . . . ."],
    par: 2,
    budget: 5,
    solution: { "0,2": "\\", "2,2": "\\" },
  },
  {
    rows: ["S . . / . .", ". # . . . .", ". . \\ . \\ .", ". . . . . .", ". . . / T ."],
    par: 2,
    budget: 7,
    solution: { "0,3": "\\", "4,3": "\\" },
  },
  {
    rows: ["S . / . . \\ T", ". . . . \\ . .", "\\ . . # . . .", ". . / . . \\ .", ". . . . L . ."],
    par: 3,
    budget: 8,
    solution: { "0,2": "\\", "3,2": "\\", "0,5": "/", "3,5": "/" },
  },
];

type Cell = { kind: "empty" | "wall" | "locked" | "mirror" | "source" | "target"; orient?: string };

function parse(rows: string[]): { grid: Cell[][]; cols: number; rws: number } {
  const grid: Cell[][] = rows.map((row) =>
    row.split(" ").map((tok) => {
      switch (tok) {
        case ".":
          return { kind: "empty" } as Cell;
        case "#":
        case "L":
          return { kind: tok === "#" ? "wall" : "locked" } as Cell;
        case "/":
        case "\\":
          return { kind: "mirror", orient: tok } as Cell;
        case "S":
          return { kind: "source" } as Cell;
        case "T":
          return { kind: "target" } as Cell;
        default:
          return { kind: "empty" } as Cell;
      }
    })
  );
  return { grid, cols: grid[0].length, rws: grid.length };
}

const REFLECT: Record<string, Record<string, [number, number]>> = {
  "/": {
    "1,0": [0, -1],
    "-1,0": [0, 1],
    "0,1": [-1, 0],
    "0,-1": [1, 0],
  },
  "\\": {
    "1,0": [0, 1],
    "-1,0": [0, -1],
    "0,1": [1, 0],
    "0,-1": [-1, 0],
  },
};

function trace(grid: Cell[][], rws: number, cols: number): { pts: [number, number][]; hit: boolean } {
  let sr = -1;
  let sc = -1;
  for (let r = 0; r < rws; r++)
    for (let c = 0; c < cols; c++) if (grid[r][c].kind === "source") { sr = r; sc = c; }
  let dir: [number, number] = [0, 1];
  let r = sr;
  let c = sc;
  const pts: [number, number][] = [[sc, sr]];
  let hit = false;
  for (let step = 0; step < 200; step++) {
    const nr = r + dir[0];
    const nc = c + dir[1];
    if (nr < 0 || nc < 0 || nr >= rws || nc >= cols) {
      pts.push([c + dir[1] * 0.5, r + dir[0] * 0.5]);
      break;
    }
    const cell = grid[nr][nc];
    if (cell.kind === "wall" || cell.kind === "locked") {
      pts.push([(c + nc) / 2, (r + nr) / 2]);
      break;
    }
    pts.push([nc, nr]);
    if (cell.kind === "target") {
      hit = true;
      break;
    }
    if (cell.kind === "mirror" && cell.orient) {
      const key = `${dir[0]},${dir[1]}`;
      dir = REFLECT[cell.orient][key] ?? dir;
    }
    r = nr;
    c = nc;
  }
  return { pts, hit };
}

export default function ConstraintForge({
  level,
  paused,
  onPause,
}: {
  level: number;
  paused: boolean;
  onPause: () => void;
}) {
  const cfg = LEVELS[level];
  const session = useSession("forge", level, cfg.par);
  const { grid: baseGrid, cols, rws } = useMemo(() => parse(cfg.rows), [cfg]);
  const [orient, setOrient] = useState<Record<string, string>>(() => {
    const o: Record<string, string> = {};
    baseGrid.forEach((row, r) =>
      row.forEach((cell, c) => {
        if (cell.kind === "mirror" && cell.orient) o[`${r},${c}`] = cell.orient;
      })
    );
    return o;
  });
  const [undoStack, setUndoStack] = useState<{ key: string; prev: string }[]>([]);
  const [hintKey, setHintKey] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  const liveGrid = useMemo(() => {
    const g = baseGrid.map((row) => row.map((cell) => ({ ...cell })));
    for (const k of Object.keys(orient)) {
      const [r, c] = k.split(",").map(Number);
      if (g[r]?.[c]?.kind === "mirror") g[r][c].orient = orient[k];
    }
    return g;
  }, [baseGrid, orient]);

  const beam = useMemo(() => trace(liveGrid, rws, cols), [liveGrid, rws, cols]);

  const checkWin = useCallback(
    (nextOrient: Record<string, string>, movesAfter: number) => {
      if (done) return;
      const g = baseGrid.map((row) => row.map((cell) => ({ ...cell })));
      for (const k of Object.keys(nextOrient)) {
        const [r, c] = k.split(",").map(Number);
        if (g[r]?.[c]?.kind === "mirror") g[r][c].orient = nextOrient[k];
      }
      const { hit } = trace(g, rws, cols);
      if (hit) {
        setDone(true);
        const reflections = Object.keys(nextOrient).length;
        session.setMsg("The core accepts the beam.");
        window.setTimeout(() => {
          session.finish(
            `A beam route using ${reflections} active reflections`,
            `The move budget of ${cfg.budget} rotations`,
            movesAfter <= cfg.par
              ? "Planned the full reflection path before spending moves"
              : "Corrected the route mid-build and recovered",
            "The final mirror that turned the beam into the core",
            { recoveredAfterError: session.errors > 0 }
          );
        }, 650);
        audio.playSfx("activate");
      } else if (movesAfter >= cfg.budget) {
        session.setMsg("The budget is spent and the core is dark. Reset to try a new route.");
      }
    },
    [baseGrid, rws, cols, cfg.budget, cfg.par, done, session]
  );

  const rotate = useCallback(
    (key: string) => {
      if (paused || done) return;
      if (session.moves >= cfg.budget) {
        session.setMsg("No moves remain. Reset the forge.");
        session.addError();
        return;
      }
      const cur = orient[key];
      const next = cur === "/" ? "\\" : "/";
      const nextOrient = { ...orient, [key]: next };
      setUndoStack((s) => [...s, { key, prev: cur }]);
      setOrient(nextOrient);
      setHintKey(null);
      session.addMove();
      markRecovered(session);
      audio.playSfx("rotate");
      checkWin(nextOrient, session.moves + 1);
    },
    [orient, paused, done, cfg.budget, session, checkWin]
  );

  const undo = useCallback(() => {
    if (undoStack.length === 0 || done) return;
    const last = undoStack[undoStack.length - 1];
    setUndoStack((s) => s.slice(0, -1));
    setOrient((o) => ({ ...o, [last.key]: last.prev }));
    session.log("Undo");
    audio.playSfx("select");
  }, [undoStack, done, session]);

  const reset = useCallback(() => {
    const o: Record<string, string> = {};
    baseGrid.forEach((row, r) =>
      row.forEach((cell, c) => {
        if (cell.kind === "mirror" && cell.orient) o[`${r},${c}`] = cell.orient;
      })
    );
    setOrient(o);
    setUndoStack([]);
    setDone(false);
    setHintKey(null);
    session.failAttempt();
  }, [baseGrid, session]);

  const hint = useCallback(() => {
    if (done) return;
    if (!session.spendHint()) return;
    const wrong = Object.keys(cfg.solution).find((k) => orient[k] !== cfg.solution[k]);
    if (wrong) {
      setHintKey(wrong);
      session.setMsg("One mirror glows. Its face is turned the wrong way.");
      window.setTimeout(() => setHintKey(null), 2000);
    }
  }, [cfg.solution, orient, done, session]);

  const CS = 64;
  const W = cols * CS;
  const H = rws * CS;
  const beamPts = beam.pts.map(([x, y]) => `${x * CS + CS / 2},${y * CS + CS / 2}`).join(" ");

  useEffect(() => {
    if (import.meta.env.MODE !== "test") return;
    (window as unknown as Record<string, unknown>).__MI_TEST__ = {
      chamber: "forge",
      wrong: Object.keys(cfg.solution).filter((k) => orient[k] !== cfg.solution[k]),
    };
  }, [orient, cfg]);

  return (
    <ChamberShell chamber="forge" level={level} session={session} onPause={onPause} onReset={reset} onUndo={undo} undoLabel="Undo">
      <div className="forge-layout">
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className={`forge-svg ${paused ? "veiled" : ""}`}
          role="group"
          aria-label={`Forge grid, ${cols} columns by ${rws} rows. Rotate mirrors to route the beam.`}
        >
          <defs>
            <linearGradient id="beamGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="#d4af37" />
              <stop offset="1" stopColor="#50c878" />
            </linearGradient>
          </defs>
          {Array.from({ length: rws }, (_, r) =>
            Array.from({ length: cols }, (_, c) => (
              <rect
                key={`bg${r},${c}`}
                x={c * CS + 2}
                y={r * CS + 2}
                width={CS - 4}
                height={CS - 4}
                rx={6}
                className="forge-cellbg"
              />
            ))
          )}
          {liveGrid.map((row, r) =>
            row.map((cell, c) => {
              const k = `${r},${c}`;
              const cx = c * CS + CS / 2;
              const cy = r * CS + CS / 2;
              if (cell.kind === "wall" || cell.kind === "locked") {
                return (
                  <rect
                    key={k}
                    x={c * CS + 6}
                    y={r * CS + 6}
                    width={CS - 12}
                    height={CS - 12}
                    rx={5}
                    className={cell.kind === "locked" ? "forge-locked" : "forge-wall"}
                  />
                );
              }
              if (cell.kind === "source") {
                return (
                  <g key={k}>
                    <rect x={c * CS + 12} y={r * CS + 18} width={CS - 24} height={CS - 36} rx={4} className="forge-source" />
                    <path d={`M${c * CS + CS - 14} ${cy - 6} l10 6 l-10 6 z`} className="forge-source-tip" />
                  </g>
                );
              }
              if (cell.kind === "target") {
                return (
                  <g key={k}>
                    <circle cx={cx} cy={cy} r={16} className="forge-target-ring" />
                    <circle cx={cx} cy={cy} r={7} className={beam.hit ? "forge-target-core hit" : "forge-target-core"} />
                  </g>
                );
              }
              if (cell.kind === "mirror") {
                const o = orient[k];
                const x1 = o === "/" ? c * CS + 12 : c * CS + CS - 12;
                const y1 = r * CS + CS - 12;
                const x2 = o === "/" ? c * CS + CS - 12 : c * CS + 12;
                const y2 = r * CS + 12;
                return (
                  <g
                    key={k}
                    className="forge-mirror-group"
                    role="button"
                    tabIndex={0}
                    aria-label={`Mirror at row ${r + 1}, column ${c + 1}, facing ${o === "/" ? "north east" : "south east"}. Activate to rotate.`}
                    onClick={() => rotate(k)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        rotate(k);
                      }
                    }}
                  >
                    <rect x={c * CS + 4} y={r * CS + 4} width={CS - 8} height={CS - 8} rx={6} className="forge-mirror-hit" />
                    <line x1={x1} y1={y1} x2={x2} y2={y2} className={`forge-mirror ${hintKey === k ? "hinted" : ""}`} />
                    <circle cx={cx} cy={cy} r={5} className="forge-mirror-pivot" />
                  </g>
                );
              }
              return null;
            })
          )}
          <polyline points={beamPts} className="forge-beam-outer" fill="none" />
          <polyline points={beamPts} className="forge-beam-inner" fill="none" />
        </svg>
        <div className="forge-side">
          <p className="side-note">
            Activate a mirror to rotate it. Each rotation spends one move. The emitter fires to the
            right. Deliver the beam to the core within {cfg.budget} moves.
          </p>
          <p className="side-note dim">Moves spent: {session.moves} of {cfg.budget}. Par is {cfg.par}.</p>
          <div className="side-controls">
            <Btn onClick={hint} disabled={done} ariaLabel="Use a hint to reveal a wrongly turned mirror">
              Hint ({session.hintsLeft})
            </Btn>
          </div>
        </div>
      </div>
    </ChamberShell>
  );
}
