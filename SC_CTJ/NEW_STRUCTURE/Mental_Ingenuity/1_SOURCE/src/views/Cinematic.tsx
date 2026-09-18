import React, { useCallback, useEffect, useRef, useState } from "react";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";
import { BRAND_ATTRIBUTION, BRAND_PRODUCT, OPENING_LINE } from "../lib/content";
import { useOsReducedMotion } from "../chambers/shared";

const CUES: { start: number; end: number; text: string }[] = [
  { start: 0, end: 3, text: "Near darkness. An immense obsidian chamber waits." },
  { start: 3, end: 7, text: "Gold pathways wake across the stone, carrying emerald light." },
  { start: 7, end: 11, text: "Silver rings turn slowly, searching for alignment." },
  { start: 11, end: 16, text: "Monoliths rise. The gate of the Ingenuity Ascent stands open." },
];

export default function Cinematic() {
  const { state, dispatch } = useGame();
  const reduced = state.save.settings.reducedMotion || useOsReducedMotion();
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [videoFailed, setVideoFailed] = useState(false);
  const [videoReady, setVideoReady] = useState(false);
  const [ended, setEnded] = useState(false);
  const [captionsOn, setCaptionsOn] = useState(state.save.settings.captions);
  const [cue, setCue] = useState("");

  const finish = useCallback(() => {
    dispatch({ type: "NAVIGATE", view: "start" });
  }, [dispatch]);

  useEffect(() => {
    if (!videoRef.current || reduced) return;
    const v = videoRef.current;
    const onTime = () => {
      const t = v.currentTime;
      const c = CUES.find((x) => t >= x.start && t < x.end);
      setCue(c ? c.text : "");
    };
    v.addEventListener("timeupdate", onTime);
    return () => v.removeEventListener("timeupdate", onTime);
  }, [reduced]);

  const replay = useCallback(() => {
    const v = videoRef.current;
    if (!v) return;
    setEnded(false);
    v.currentTime = 0;
    v.play().catch(() => setVideoFailed(true));
  }, []);

  if (reduced || videoFailed) {
    return (
      <section className="cinematic reduced" aria-label="Opening cinematic, reduced motion version">
        <img src="/media/video/poster.jpg" alt="A dark obsidian chamber with a gold framed gate glowing with emerald light" className="cine-poster" />
        <div className="cine-overlay">
          <p className="cine-transcript">
            Near darkness. An immense obsidian chamber waits. Gold pathways wake across the stone.
            Silver rings turn, searching for alignment. The gate of the Ingenuity Ascent stands open.
          </p>
          <h1 className="brand-title">{BRAND_PRODUCT}</h1>
          <p className="brand-sub">{BRAND_ATTRIBUTION}</p>
          <p className="opening-line">“{OPENING_LINE}”</p>
          <Btn onClick={finish} variant="gold" autoFocus ariaLabel="Continue to the start screen">
            Enter the Ascent
          </Btn>
        </div>
      </section>
    );
  }

  return (
    <section className="cinematic" aria-label="Opening cinematic">
      <video
        ref={videoRef}
        className="cine-video"
        autoPlay
        muted
        playsInline
        poster="/media/video/poster.jpg"
        onEnded={() => setEnded(true)}
        onError={() => setVideoFailed(true)}
        onCanPlay={() => setVideoReady(true)}
        aria-label="Opening cinematic video: mechanisms awaken inside a dark obsidian chamber"
      >
        <source src="/media/video/opening.mp4" type="video/mp4" />
        <source src="/media/video/opening.webm" type="video/webm" />
      </video>
      {!videoReady ? <p className="cine-loading">Preparing the ascent…</p> : null}
      <div className="cine-overlay top-overlay">
        <h1 className="brand-title">{BRAND_PRODUCT}</h1>
        <p className="brand-sub">{BRAND_ATTRIBUTION}</p>
      </div>
      {captionsOn && cue ? (
        <p className="cine-caption" aria-live="off">
          {cue}
        </p>
      ) : null}
      {ended ? (
        <div className="cine-overlay">
          <p className="opening-line">“{OPENING_LINE}”</p>
          <div className="cine-buttons">
            <Btn onClick={replay} ariaLabel="Replay the opening cinematic">
              Replay
            </Btn>
            <Btn onClick={finish} variant="gold" autoFocus ariaLabel="Continue to the start screen">
              Enter the Ascent
            </Btn>
          </div>
        </div>
      ) : (
        <div className="cine-controls">
          <Btn onClick={() => setCaptionsOn((c) => !c)} ariaLabel={captionsOn ? "Hide captions" : "Show captions"}>
            {captionsOn ? "Captions on" : "Captions off"}
          </Btn>
          <Btn onClick={finish} ariaLabel="Skip the opening cinematic">
            Skip
          </Btn>
        </div>
      )}
    </section>
  );
}
