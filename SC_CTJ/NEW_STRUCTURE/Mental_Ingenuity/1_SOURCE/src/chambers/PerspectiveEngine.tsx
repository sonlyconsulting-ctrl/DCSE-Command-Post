import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Rand } from "../lib/rng";
import { audio } from "../audio/engine";
import { useGame } from "../state/store";
import { Btn } from "../components/ui";
import { ChamberShell, Session, markRecovered, seedFor, useSession } from "./shared";

const SLOTS = 12;

interface PerspLevel {
  /** effect[actionRing][targetRing] = rotation delta applied to target when actionRing turns +1 */
  effect: number[][];
  scramble: number;
  decoys: number;
  desc: string;
}

const LEVELS: PerspLevel[] = [
  {
    effect: [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    scramble: 3,
    decoys: 3,
    desc: "The rings turn independently.",
  },
  {
    effect: [[1, -1, 0], [0, 1, 0], [0, 0, 1]],
    scramble: 4,
    decoys: 4,
    desc: "The outer ring is gear linked to the middle ring in reverse.",
  },
  {
    effect: [[1, -1, 0], [0, 1, -1], [0, 0, 1]],
    scramble: 5,
    decoys: 5,
    desc: "A full gear train: each ring drags the next one against it.",
  },
];

type State = [number, number, number];

function mod(x: number, m: number): number {
  return ((x % m) + m) % m;
}

function applyAction(s: State, effect: number[][], ring: number, sign: number): State {
  const next: State = [s[0], s[1], s[2]];
  effect[ring].forEach((d, i) => {
    next[i] = mod(next[i] + d * sign, SLOTS);
  });
  return next;
}

function solved(s: State): boolean {
  return s[0] === 0 && s[1] === 0 && s[2] === 0;
}

function bfsPar(start: State, effect: number[][]): number {
  const key = (s: State) => s.join(",");
  const dist = new Map<string, number>();
  dist.set(key(start), 0);
  const q: State[] = [start];
  while (q.length) {
    const cur = q.shift() as State;
    const d = dist.get(key(cur)) as number;
    if (solved(cur)) return d;
    for (let ring = 0; ring < 3; ring++) {
      for (const sign of [1, -1]) {
        const nxt = applyAction(cur, effect, ring, sign);
        if (!dist.has(key(nxt))) {
          dist.set(key(nxt), d + 1);
          q.push(nxt);
        }
      }
    }
  }
  return 99;
}

function scrambleState(rnd: Rand, effect: number[][], n: number): State {
  let s: State = [0, 0, 0];
  for (let i = 0; i < n; i++) {
    s = applyAction(s, effect, rnd.int(3), rnd.chance(0.5) ? 1 : -1);
  }
  if (solved(s)) s = applyAction(s, effect, rnd.int(3), 1);
  return s;
}

const RADII = [150, 110, 70];
const RING_NAMES = ["outer ring", "middle ring", "inner ring"];

export default function PerspectiveEngine({
  level,
  paused,
  onPause,
}: {
  level: number;
  paused: boolean;
  onPause: () => void;
}) {
  const cfg = LEVELS[level];
  const { state } = useGame();
  const reduced = state.save.settings.reducedMotion;

  const [attemptSeed, setAttemptSeed] = useState(0);
  const seed = seedFor("perspective", level, attemptSeed);
  const { start, par, decoySlots } = useMemo(() => {
    const rnd = new Rand(seed);
    const start = scrambleState(rnd, cfg.effect, cfg.scramble);
    const par = bfsPar(start, cfg.effect);
    const decoySlots: number[][] = [];
    for (let r = 0; r < 3; r++) {
      const ds: number[] = [];
      const count = Math.ceil(cfg.decoys / 3) + (r < cfg.decoys % 3 ? 1 : 0);
      while (ds.length < count) {
        const s = rnd.int(SLOTS);
        if (s !== 0 && !ds.includes(s)) ds.push(s);
      }
      decoySlots.push(ds);
    }
    return { start, par, decoySlots };
  }, [seed, cfg]);

  const session = useSession("perspective", level, Math.max(par, 1));
  const [offs, setOffs] = useState<State>(start);
  const [done, setDone] = useState(false);
  const dragRef = useRef<{ ring: number; lastAngle: number } | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    setOffs(start);
    setDone(false);
  }, [start]);

  useEffect(() => {
    if (import.meta.env.MODE !== "test") return;
    (window as unknown as Record<string, unknown>).__MI_TEST__ = { chamber: "perspective", offs };
  }, [offs]);

  const rotate = useCallback(
    (ring: number, sign: number) => {
      if (done || paused) return;
      const next = applyAction(offs, cfg.effect, ring, sign);
      setOffs(next);
      session.addMove();
      markRecovered(session);
      audio.playSfx("rotate");
      if (solved(next)) {
        setDone(true);
        session.setMsg("The axis of sight holds. Every gold mark stands on it.");
        window.setTimeout(() => {
          session.finish(
            level === 0 ? "Independent ring rotation" : "Gear coupled rotation between rings",
            "Coupled movement: turning one ring moves its partner against it",
            session.moves + 1 <= par * 1.3
              ? "Worked out the coupling, then planned the shortest turn sequence"
              : "Explored rotations, observed the coupling, and corrected course",
            "The gold mark on the inner ring reaching the sight axis",
            { recoveredAfterError: session.errors > 0 }
          );
        }, 600);
      }
    },
    [offs, cfg.effect, done, paused, session, par, level]
  );

  // pointer drag rotation
  const pointerAngle = (e: React.PointerEvent): { ring: number; angle: number } | null => {
    const svg = svgRef.current;
    if (!svg) return null;
    const rect = svg.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 420 - 210;
    const y = ((e.clientY - rect.top) / rect.height) * 420 - 210;
    const dist = Math.sqrt(x * x + y * y);
    let ring = -1;
    RADII.forEach((r, i) => {
      if (Math.abs(dist - r) < 24) ring = i;
    });
    if (ring < 0) return null;
    return { ring, angle: Math.atan2(y, x) };
  };

  const onPointerDown = (e: React.PointerEvent) => {
    if (done || paused) return;
    const p = pointerAngle(e);
    if (p) {
      dragRef.current = { ring: p.ring, lastAngle: p.angle };
      (e.target as Element).setPointerCapture?.(e.pointerId);
    }
  };

  const onPointerMove = (e: React.PointerEvent) => {
    if (!dragRef.current) return;
    const p = pointerAngle(e);
    if (!p || p.ring !== dragRef.current.ring) return;
    let delta = p.angle - dragRef.current.lastAngle;
    if (delta > Math.PI) delta -= 2 * Math.PI;
    if (delta < -Math.PI) delta += 2 * Math.PI;
    const step = (2 * Math.PI) / SLOTS;
    if (Math.abs(delta) > step * 0.55) {
      rotate(dragRef.current.ring, delta > 0 ? 1 : -1);
      dragRef.current.lastAngle = p.angle;
    }
  };

  const onPointerUp = () => {
    dragRef.current = null;
  };

  const hint = useCallback(() => {
    if (done) return;
    if (!session.spendHint()) return;
    // find first ring whose offset is nonzero and indicate direction
    for (let r = 0; r < 3; r++) {
      if (offs[r] !== 0) {
        const dir = offs[r] <= SLOTS / 2 ? "counter clockwise" : "clockwise";
        session.setMsg(`The engine whispers: turn the ${RING_NAMES[r]} ${dir}.`);
        return;
      }
    }
  }, [done, offs, session]);

  const slotAngle = (2 * Math.PI) / SLOTS;
  const alignedCount = offs.filter((o) => o === 0).length;

  return (
    <ChamberShell
      chamber="perspective"
      level={level}
      session={session}
      onPause={onPause}
      onReset={() => {
        setOffs(start);
        setDone(false);
        session.failAttempt();
        setAttemptSeed((s) => s + 1);
      }}
    >
      <div className="persp-layout">
        <svg
          ref={svgRef}
          viewBox="0 0 420 420"
          className={`persp-svg ${reduced ? "no-motion" : ""} ${paused ? "veiled" : ""}`}
          role="group"
          aria-label="Three concentric rings. Bring every gold mark to the sight axis at the top."
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerCancel={onPointerUp}
        >
          <line x1={210} y1={18} x2={210} y2={54} className="persp-axis-notch" />
          {alignedCount > 0 ? (
            <line x1={210} y1={54} x2={210} y2={54 + alignedCount * 52} className="persp-axis-beam" />
          ) : null}
          {RADII.map((r, i) => (
            <g key={i} className="persp-ring-g">
              <circle cx={210} cy={210} r={r} className={`persp-ring ${offs[i] === 0 ? "aligned" : ""}`} />
              {Array.from({ length: SLOTS }, (_, s) => {
                const a = -Math.PI / 2 + s * slotAngle;
                const x = 210 + Math.cos(a) * r;
                const y = 210 + Math.sin(a) * r;
                return <circle key={s} cx={x} cy={y} r={2} className="persp-slot-dot" />;
              })}
              {decoySlots[i].map((s) => {
                const a = -Math.PI / 2 + ((s + offs[i]) % SLOTS) * slotAngle;
                const x = 210 + Math.cos(a) * r;
                const y = 210 + Math.sin(a) * r;
                return <circle key={`d${s}`} cx={x} cy={y} r={5} className="persp-decoy" />;
              })}
              {(() => {
                const a = -Math.PI / 2 + offs[i] * slotAngle;
                const x = 210 + Math.cos(a) * r;
                const y = 210 + Math.sin(a) * r;
                return <path key="gold" d={`M${x} ${y - 8} L${x + 6} ${y} L${x} ${y + 8} L${x - 6} ${y} Z`} className={`persp-gold ${offs[i] === 0 ? "home" : ""}`} />;
              })()}
            </g>
          ))}
          <circle cx={210} cy={210} r={10} className="persp-hub" />
        </svg>
        <div className="persp-side">
          <p className="side-note">{cfg.desc}</p>
          <p className="side-note dim">
            Gold marks aligned: {alignedCount} of 3. Moves: {session.moves}. Par: {par}.
          </p>
          <div className="persp-controls" role="group" aria-label="Ring rotation controls">
            {RING_NAMES.map((name, i) => (
              <div className="persp-control-row" key={name}>
                <span className="ring-name">{name}</span>
                <Btn
                  onClick={() => rotate(i, -1)}
                  ariaLabel={`Rotate ${name} counter clockwise one step`}
                  disabled={done || paused}
                >
                  ⟲
                </Btn>
                <Btn
                  onClick={() => rotate(i, 1)}
                  ariaLabel={`Rotate ${name} clockwise one step`}
                  disabled={done || paused}
                >
                  ⟳
                </Btn>
              </div>
            ))}
          </div>
          <div className="side-controls">
            <Btn onClick={hint} disabled={done} ariaLabel="Use a hint for the next rotation">
              Hint ({session.hintsLeft})
            </Btn>
          </div>
          <p className="side-note dim">Keyboard: tab to a rotate button, then use Enter or Space. You can also drag a ring.</p>
        </div>
      </div>
    </ChamberShell>
  );
}
