import React from "react";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";
import { CHAMBER_META } from "../lib/content";

export default function ResumeView() {
  const { state, dispatch } = useGame();
  const inf = state.save.inFlight;
  if (!inf) {
    return (
      <section className="doc-view" aria-label="No session to resume">
        <p>There is no ascent in progress.</p>
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "map" })}>To the chamber map</Btn>
      </section>
    );
  }
  const meta = CHAMBER_META[inf.chamber];
  return (
    <section className="doc-view resume-view" aria-label="Resume session">
      <h2>Resume the ascent</h2>
      <p>
        You were standing in <strong>{meta.name}</strong>, challenge {inf.level + 1} of 3
        {inf.attempts > 1 ? `, attempt ${inf.attempts}` : ""}. The board resets to the start of the
        challenge; your progress through the ascent is safe.
      </p>
      <div className="record-actions">
        <Btn
          variant="gold"
          onClick={() => {
            audio.ensure();
            dispatch({ type: "START_LEVEL", chamber: inf.chamber, level: inf.level, attempts: inf.attempts });
          }}
          ariaLabel={`Resume ${meta.name} challenge ${inf.level + 1}`}
        >
          Resume
        </Btn>
        <Btn onClick={() => dispatch({ type: "ABANDON_RUN" })} ariaLabel="Return to the chamber map without resuming">
          Return to map
        </Btn>
      </div>
    </section>
  );
}
