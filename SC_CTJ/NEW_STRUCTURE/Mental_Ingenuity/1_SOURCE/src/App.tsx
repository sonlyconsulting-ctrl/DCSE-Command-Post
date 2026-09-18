import React, { useEffect, useRef, useState } from "react";
import { useGame } from "./state/store";
import { audio } from "./audio/engine";
import type { SceneAudio } from "./audio/engine";
import { CHAMBER_META, BRAND_ATTRIBUTION, BRAND_PRODUCT } from "./lib/content";
import { Btn, Modal } from "./components/ui";
import { useOsReducedMotion } from "./chambers/shared";
import Cinematic from "./views/Cinematic";
import Start from "./views/Start";
import HowTo from "./views/HowTo";
import MapView from "./views/MapView";
import RecordView from "./views/RecordView";
import SignatureView from "./views/SignatureView";
import ProgressView from "./views/ProgressView";
import SettingsView from "./views/SettingsView";
import AboutView from "./views/AboutView";
import HelpView from "./views/HelpView";
import ResumeView from "./views/ResumeView";
import PauseOverlay from "./views/PauseOverlay";
import SignalChamber from "./chambers/SignalChamber";
import ConstraintForge from "./chambers/ConstraintForge";
import PerspectiveEngine from "./chambers/PerspectiveEngine";
import CausalLabyrinth from "./chambers/CausalLabyrinth";
import ParadoxVault from "./chambers/ParadoxVault";
import Summit from "./chambers/Summit";

function AppInner() {
  const { state, dispatch } = useGame();
  const settings = state.save.settings;
  const osReduced = useOsReducedMotion();
  const [paused, setPaused] = useState(false);
  const sceneRef = useRef<SceneAudio>({ music: null, ambience: null });

  // Scene audio selection
  useEffect(() => {
    let scene: SceneAudio = { music: null, ambience: null };
    switch (state.view) {
      case "cinematic":
      case "start":
        scene = { music: "music_opening", ambience: null };
        break;
      case "chamber": {
        const meta = CHAMBER_META[state.chamber];
        scene = { music: meta.music, ambience: meta.ambience };
        break;
      }
      case "map":
      case "record":
      case "progress":
      case "howto":
      case "resume":
        scene = { music: "music_map", ambience: null };
        break;
      case "settings":
      case "about":
      case "help":
        scene = { music: "music_map", ambience: null };
        break;
      case "signature":
        scene = { music: null, ambience: "amb_summit" };
        break;
    }
    sceneRef.current = scene;
    audio.setScene(scene);
  }, [state.view, state.chamber]);

  // Settings sync: volumes, motion classes, contrast
  useEffect(() => {
    audio.applySettings(settings);
  }, [settings]);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle("reduced-motion", settings.reducedMotion || osReduced);
    root.classList.toggle("high-contrast", settings.highContrast);
  }, [settings.reducedMotion, settings.highContrast, osReduced]);

  // Audio only starts after a real user gesture.
  useEffect(() => {
    const unlock = () => {
      audio.ensure();
      audio.applySettings(settingsRef.current);
      audio.setScene(sceneRef.current);
      (window as unknown as Record<string, unknown>).__MI_AUDIO_INITED__ = true;
    };
    window.addEventListener("pointerdown", unlock, { once: true });
    window.addEventListener("keydown", unlock, { once: true });
    return () => {
      window.removeEventListener("pointerdown", unlock);
      window.removeEventListener("keydown", unlock);
    };
  }, []);
  const settingsRef = useRef(settings);
  useEffect(() => {
    settingsRef.current = settings;
  }, [settings]);

  const openPause = () => {
    setPaused(true);
    audio.suspend();
  };
  const closePause = () => {
    setPaused(false);
    audio.resume();
  };
  const quitToMap = () => {
    setPaused(false);
    dispatch({ type: "NAVIGATE", view: "map" });
  };

  const renderChamber = () => {
    const props = { level: state.level, paused, onPause: openPause };
    switch (state.chamber) {
      case "signal":
        return <SignalChamber {...props} />;
      case "forge":
        return <ConstraintForge {...props} />;
      case "perspective":
        return <PerspectiveEngine {...props} />;
      case "causal":
        return <CausalLabyrinth {...props} />;
      case "paradox":
        return <ParadoxVault {...props} />;
      case "summit":
        return <Summit {...props} />;
    }
  };

  return (
    <div className="app-root">
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      {state.view === "chamber" ? (
        <header className="topbar">
          <span className="topbar-brand">
            {BRAND_PRODUCT} <span className="topbar-sub">{BRAND_ATTRIBUTION}</span>
          </span>
        </header>
      ) : null}
      <main id="main">
        {state.view === "cinematic" ? <Cinematic /> : null}
        {state.view === "start" ? <Start /> : null}
        {state.view === "howto" ? <HowTo /> : null}
        {state.view === "map" ? <MapView /> : null}
        {state.view === "chamber" ? renderChamber() : null}
        {state.view === "record" ? <RecordView /> : null}
        {state.view === "signature" ? <SignatureView /> : null}
        {state.view === "progress" ? <ProgressView /> : null}
        {state.view === "settings" ? <SettingsView /> : null}
        {state.view === "about" ? <AboutView /> : null}
        {state.view === "help" ? <HelpView /> : null}
        {state.view === "resume" ? <ResumeView /> : null}
      </main>
      {state.view !== "cinematic" ? (
        <footer className="app-footer">
          <span>{BRAND_PRODUCT}</span>
          <span aria-hidden="true">·</span>
          <span>{BRAND_ATTRIBUTION}</span>
        </footer>
      ) : null}
      {paused && state.view === "chamber" ? (
        <PauseOverlay onResume={closePause} onQuit={quitToMap} />
      ) : null}
      {state.modal === "restart" ? (
        <Modal label="Restart confirmation" onClose={() => dispatch({ type: "CLOSE_MODAL" })}>
          <h2 className="pause-title">Restart the ascent?</h2>
          <p>
            This clears all saved progress, scores, and achievements stored in this browser, then
            begins again from the opening cinematic. This cannot be undone.
          </p>
          <div className="record-actions">
            <Btn
              variant="danger"
              onClick={() => {
                setPaused(false);
                dispatch({ type: "CONFIRM_RESTART" });
              }}
              ariaLabel="Confirm restart and erase progress"
            >
              Erase and restart
            </Btn>
            <Btn onClick={() => dispatch({ type: "CLOSE_MODAL" })} autoFocus ariaLabel="Cancel restart">
              Keep my progress
            </Btn>
          </div>
        </Modal>
      ) : null}
    </div>
  );
}

export default function App() {
  return <AppInner />;
}
