import React from "react";
import { useGame } from "../state/store";
import { Btn, Emblem } from "../components/ui";
import { ACHIEVEMENTS } from "../lib/achievements";
import { CHAMBER_META } from "../lib/content";
import { CHAMBER_ORDER } from "../lib/types";

export default function ProgressView() {
  const { state, dispatch } = useGame();
  const save = state.save;
  const total = CHAMBER_ORDER.reduce(
    (a, c) => a + Object.values(save.chambers[c].bestLevelScores).reduce((x, y) => x + y, 0),
    0
  );

  return (
    <section className="doc-view progress-view" aria-label="Progress and achievements">
      <h2>Progress and Achievements</h2>
      <p className="lede">Ascent score: {total} · Hints remaining: {save.hintsRemaining}</p>
      <div className="progress-chambers">
        {CHAMBER_ORDER.map((id) => {
          const meta = CHAMBER_META[id];
          const prog = save.chambers[id];
          return (
            <div className="progress-chamber" key={id}>
              <h3>{meta.name}</h3>
              <p className="dim">
                Challenges complete: {prog.completedLevels.length} of 3
                {prog.completedLevels.length > 0
                  ? ` · Best scores: ${prog.completedLevels
                      .sort((a, b) => a - b)
                      .map((l) => `challenge ${l + 1}: ${prog.bestLevelScores[l] ?? 0}`)
                      .join(", ")}`
                  : ""}
              </p>
            </div>
          );
        })}
      </div>
      <h3>Achievements</h3>
      <div className="achieve-grid">
        {ACHIEVEMENTS.map((a) => {
          const earned = save.achievements.includes(a.id);
          return (
            <div key={a.id} className={`achieve-card ${earned ? "earned" : ""}`}>
              {earned ? <Emblem kind="Adaptive Strategist" size={44} /> : <span className="achieve-lock" aria-hidden="true">◆</span>}
              <div>
                <p className="achieve-name">{a.name}</p>
                <p className="achieve-desc">{a.desc}</p>
                <p className="dim">{earned ? "Earned" : "Not yet earned"}</p>
              </div>
            </div>
          );
        })}
      </div>
      <div className="record-actions">
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "start" })}>Back</Btn>
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "map" })}>To the chamber map</Btn>
        <Btn onClick={() => dispatch({ type: "OPEN_RESTART" })} variant="danger">
          Restart the ascent
        </Btn>
      </div>
    </section>
  );
}
