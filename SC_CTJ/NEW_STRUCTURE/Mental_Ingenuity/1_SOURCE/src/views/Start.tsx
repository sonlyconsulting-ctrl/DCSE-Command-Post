import React from "react";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";
import { BRAND_ATTRIBUTION, BRAND_PRODUCT, OPENING_LINE } from "../lib/content";
import { CHAMBER_ORDER } from "../lib/types";

export default function Start() {
  const { state, dispatch } = useGame();
  const save = state.save;
  const hasProgress =
    save.inFlight !== null ||
    save.finished ||
    CHAMBER_ORDER.some((c) => save.chambers[c].completedLevels.length > 0);

  const begin = () => {
    audio.ensure();
    audio.playSfx("select");
    if (save.inFlight) {
      dispatch({ type: "NAVIGATE", view: "resume" });
    } else if (save.finished) {
      dispatch({ type: "NAVIGATE", view: "map" });
    } else {
      dispatch({ type: "NAVIGATE", view: "map" });
    }
  };

  return (
    <section className="start-view" aria-label="Start screen">
      <img src="/media/img/hero.webp" alt="" aria-hidden="true" className="start-bg" onError={(e) => ((e.target as HTMLImageElement).style.display = "none")} />
      <div className="start-panel">
        <h1 className="brand-title">{BRAND_PRODUCT}</h1>
        <p className="brand-sub">{BRAND_ATTRIBUTION}</p>
        <p className="opening-line">“{OPENING_LINE}”</p>
        <div className="start-buttons">
          {save.inFlight ? (
            <Btn variant="gold" onClick={begin} ariaLabel="Resume the Ascent">
              Resume the Ascent
            </Btn>
          ) : (
            <Btn
              variant="gold"
              onClick={begin}
              ariaLabel={hasProgress ? "Continue the ascent" : "Begin the ascent"}
            >
              {hasProgress ? "Continue the Ascent" : "Begin the Ascent"}
            </Btn>
          )}
          <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "howto" })}>How to Play</Btn>
          <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "progress" })}>Progress and Achievements</Btn>
          <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "settings" })}>Settings</Btn>
          <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "about" })}>About</Btn>
          <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "help" })}>Accessibility Help</Btn>
        </div>
        {state.saveRecovered ? (
          <p className="recovered-note">
            A previous save could not be read, so the ascent begins fresh.
          </p>
        ) : null}
        <p className="audio-note">Audio begins only after you choose to enter. Nothing plays on its own.</p>
      </div>
    </section>
  );
}
