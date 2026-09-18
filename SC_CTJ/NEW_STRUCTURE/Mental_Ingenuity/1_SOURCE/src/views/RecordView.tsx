import React, { useEffect } from "react";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn, DimBars } from "../components/ui";
import { CHAMBER_META } from "../lib/content";
import { ACHIEVEMENTS } from "../lib/achievements";
import { CHAMBER_ORDER } from "../lib/types";

export default function RecordView() {
  const { state, dispatch } = useGame();
  const r = state.lastResult;

  useEffect(() => {
    if (state.newAchievements.length > 0) {
      audio.playSfx("achievement");
      const t = window.setTimeout(() => dispatch({ type: "MARK_ACHIEVEMENTS_SEEN" }), 4200);
      return () => window.clearTimeout(t);
    }
  }, [state.newAchievements, dispatch]);

  if (!r) {
    return (
      <section className="doc-view" aria-label="No result">
        <p>No completed challenge on record yet.</p>
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "map" })}>To the chamber map</Btn>
      </section>
    );
  }

  const meta = CHAMBER_META[r.chamber];
  const prev = state.save.chambers[r.chamber].results.filter((x) => x !== r && x.level === r.level).slice(-1)[0];
  const nextLevel = r.level + 1;
  const hasNext = nextLevel <= 2;
  const chamberIdx = CHAMBER_ORDER.indexOf(r.chamber);
  const nextChamber = hasNext ? null : CHAMBER_ORDER[chamberIdx + 1] ?? null;

  const changes: string[] = [];
  if (prev) {
    if (r.moves < prev.moves) changes.push(`Moves fell from ${prev.moves} to ${r.moves}.`);
    if (r.moves > prev.moves) changes.push(`Moves rose from ${prev.moves} to ${r.moves}.`);
    if (r.errors < prev.errors) changes.push(`Misreads fell from ${prev.errors} to ${r.errors}.`);
    if (r.attempts > 1) changes.push(`This run took ${r.attempts} attempts. The previous record was set in ${prev.attempts}.`);
    if (changes.length === 0) changes.push("Performance held steady against your previous run on this challenge.");
  } else {
    changes.push("This is your first recorded run on this challenge.");
  }

  return (
    <section className="record-view" aria-label="Reasoning record">
      <h2>Reasoning Record</h2>
      <p className="record-chamber">{meta.name} · Challenge {r.level + 1} of 3</p>
      <div className="record-grid">
        <div className="record-card">
          <h3>What you detected</h3>
          <p>{r.detected}</p>
          <h3>The constraint that mattered</h3>
          <p>{r.constraint}</p>
          <h3>Strategy that produced the solution</h3>
          <p>{r.strategy}</p>
          <h3>Decisive evidence</h3>
          <p>{r.decisive}</p>
        </div>
        <div className="record-card">
          <h3>The numbers</h3>
          <ul className="record-nums">
            <li>Attempts: {r.attempts}</li>
            <li>Moves: {r.moves} (par {r.parMoves})</li>
            <li>Misreads: {r.errors}</li>
            <li>Hints used: {r.hintsUsed}</li>
            <li>Time: {Math.max(1, Math.round(r.durationMs / 1000))} seconds</li>
          </ul>
          <h3>What changed from the previous attempt</h3>
          <ul>
            {changes.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="record-score">
        <DimBars dims={r.dims} />
        <p className="score-line">
          Challenge score: <strong>{r.score}</strong> of 300. This is a gameplay record, not an
          intelligence score.
        </p>
      </div>
      {state.newAchievements.length > 0 ? (
        <div className="achieve-toast" role="status">
          {state.newAchievements.map((id) => {
            const a = ACHIEVEMENTS.find((x) => x.id === id);
            return a ? (
              <p key={id} className="achieve-line">
                Achievement earned: <strong>{a.name}</strong>. {a.desc}
              </p>
            ) : null;
          })}
        </div>
      ) : null}
      <div className="record-actions">
        {hasNext ? (
          <Btn
            variant="gold"
            onClick={() => dispatch({ type: "START_LEVEL", chamber: r.chamber, level: nextLevel })}
            ariaLabel={`Continue to challenge ${nextLevel + 1} of ${meta.name}`}
          >
            Continue to challenge {nextLevel + 1}
          </Btn>
        ) : nextChamber ? (
          <Btn
            variant="gold"
            onClick={() => dispatch({ type: "NAVIGATE", view: "map" })}
            ariaLabel="Chamber complete. Return to the map."
          >
            Chamber complete. Return to the map
          </Btn>
        ) : (
          <Btn
            variant="gold"
            onClick={() => dispatch({ type: "NAVIGATE", view: "signature" })}
            ariaLabel="Ascent complete. View your Reasoning Signature."
          >
            The ascent is complete. Receive your signature
          </Btn>
        )}
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "map" })}>Return to map</Btn>
      </div>
    </section>
  );
}
