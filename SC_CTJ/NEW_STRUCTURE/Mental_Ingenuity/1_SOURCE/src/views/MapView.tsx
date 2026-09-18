import React from "react";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";
import { CHAMBER_META } from "../lib/content";
import { CHAMBER_ORDER } from "../lib/types";

const POS: Record<string, { x: number; y: number }> = {
  signal: { x: 22, y: 82 },
  forge: { x: 68, y: 72 },
  perspective: { x: 30, y: 58 },
  causal: { x: 70, y: 46 },
  paradox: { x: 32, y: 34 },
  summit: { x: 52, y: 16 },
};

export default function MapView() {
  const { state, dispatch } = useGame();
  const save = state.save;
  const total = CHAMBER_ORDER.reduce(
    (a, c) => a + Object.values(save.chambers[c].bestLevelScores).reduce((x, y) => x + y, 0),
    0
  );

  const enter = (id: (typeof CHAMBER_ORDER)[number], idx: number) => {
    if (idx > save.unlockedIndex) {
      audio.playSfx("invalid");
      return;
    }
    audio.playSfx("select");
    const prog = save.chambers[id];
    const level = prog.completedLevels.length >= 3 ? 0 : prog.completedLevels.length;
    dispatch({ type: "START_LEVEL", chamber: id, level });
  };

  return (
    <section className="map-view" aria-label="Chamber map of the Ingenuity Ascent">
      <img src="/media/img/map.webp" alt="" aria-hidden="true" className="map-bg" onError={(e) => ((e.target as HTMLImageElement).style.display = "none")} />
      <div className="map-head">
        <div>
          <h2>The Ingenuity Ascent</h2>
          <p className="map-sub">Six chambers. Complete all three challenges in a chamber to unlock the next.</p>
        </div>
        <div className="map-stats">
          <span className="hud-item">Ascent score: {total}</span>
          <span className="hud-item">Hints remaining: {save.hintsRemaining}</span>
          <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "progress" })}>Progress</Btn>
          <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "settings" })}>Settings</Btn>
        </div>
      </div>
      <div className="map-board">
        {CHAMBER_ORDER.map((id, idx) => {
          const meta = CHAMBER_META[id];
          const prog = save.chambers[id];
          const locked = idx > save.unlockedIndex;
          const done = prog.completedLevels.length >= 3;
          return (
            <button
              key={id}
              type="button"
              className={`map-node ${locked ? "locked" : ""} ${done ? "done" : ""}`}
              style={{ left: `${POS[id].x}%`, top: `${POS[id].y}%` }}
              onClick={() => enter(id, idx)}
              disabled={locked}
              aria-label={
                locked
                  ? `${meta.name}, locked. Complete the previous chamber to open it.`
                  : `${meta.name}. ${prog.completedLevels.length} of 3 challenges complete. ${locked ? "" : "Activate to enter."}`
              }
            >
              <span className="node-ring" aria-hidden="true" style={{ borderColor: meta.accent }} />
              <span className="node-name">{meta.name}</span>
              <span className="node-sub">
                {locked ? "Sealed" : done ? "Complete" : `${prog.completedLevels.length} of 3`}
              </span>
            </button>
          );
        })}
      </div>
      {save.finished ? (
        <div className="map-finished">
          <p>The ascent stands complete.</p>
          <Btn variant="gold" onClick={() => dispatch({ type: "NAVIGATE", view: "signature" })}>
            View your Reasoning Signature
          </Btn>
        </div>
      ) : null}
    </section>
  );
}
