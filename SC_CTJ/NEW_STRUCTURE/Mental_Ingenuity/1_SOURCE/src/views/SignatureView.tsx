import React, { useEffect, useRef } from "react";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn, DimBars, Emblem } from "../components/ui";
import { buildSignature } from "../lib/signature";

export default function SignatureView() {
  const { state, dispatch } = useGame();
  const sig = buildSignature(state.save);
  const played = useRef(false);

  useEffect(() => {
    if (played.current) return;
    played.current = true;
    audio.playCompletionCue();
  }, []);

  return (
    <section className="signature-view" aria-label="Final reasoning signature">
      <div className="sig-emblem-wrap">
        <Emblem kind={sig.title} size={130} />
      </div>
      <h2>Your Reasoning Signature</h2>
      <p className="sig-title">{sig.title}</p>
      <p className="sig-summary">{sig.summary}</p>
      <div className="sig-grid">
        <div className="record-card">
          <h3>Recorded evidence</h3>
          <ul>
            {sig.evidence.map((e) => (
              <li key={e}>{e}</li>
            ))}
          </ul>
        </div>
        <div className="record-card">
          <h3>Dimensions across the ascent</h3>
          <DimBars dims={sig.dims} />
          <p className="score-line">
            Total ascent score: <strong>{sig.totalScore}</strong>.
          </p>
        </div>
      </div>
      <p className="sig-disclaimer">
        This signature is a description of how you played, built only from recorded game behavior.
        It is not a diagnosis, an intelligence rating, or a statement about fixed personal traits.
      </p>
      <div className="record-actions">
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "map" })}>Return to the map</Btn>
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "progress" })}>Progress and achievements</Btn>
        <Btn onClick={() => dispatch({ type: "OPEN_RESTART" })} variant="danger">
          Restart the ascent
        </Btn>
      </div>
    </section>
  );
}
