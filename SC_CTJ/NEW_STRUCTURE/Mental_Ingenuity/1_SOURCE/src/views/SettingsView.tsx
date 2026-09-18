import React from "react";
import { useGame } from "../state/store";
import { Btn, Slider, Toggle } from "../components/ui";

export default function SettingsView() {
  const { state, dispatch } = useGame();
  const s = state.save.settings;
  const set = (patch: Partial<typeof s>) => dispatch({ type: "SET_SETTINGS", patch });

  return (
    <section className="doc-view settings-view" aria-label="Settings">
      <h2>Settings</h2>
      <h3>Audio</h3>
      <Toggle
        id="mute-all"
        label="Mute all audio"
        checked={s.muted}
        onChange={(v) => set({ muted: v })}
        hint="Silences music, ambience, and effects. Your choice is saved."
      />
      <Slider id="vol-master" label="Master volume" value={s.masterVolume} onChange={(v) => set({ masterVolume: v })} />
      <Slider id="vol-music" label="Music volume" value={s.musicVolume} onChange={(v) => set({ musicVolume: v })} />
      <Slider id="vol-amb" label="Ambience volume" value={s.ambienceVolume} onChange={(v) => set({ ambienceVolume: v })} />
      <Slider id="vol-sfx" label="Sound effect volume" value={s.sfxVolume} onChange={(v) => set({ sfxVolume: v })} />
      <h3>Visual and motion</h3>
      <Toggle
        id="reduced-motion"
        label="Reduced motion"
        checked={s.reducedMotion}
        onChange={(v) => set({ reducedMotion: v })}
        hint="Calms animation and replaces the opening video with a still sequence. Gameplay information stays fully visible."
      />
      <Toggle
        id="high-contrast"
        label="High contrast"
        checked={s.highContrast}
        onChange={(v) => set({ highContrast: v })}
        hint="Strengthens text contrast and focus outlines."
      />
      <Toggle
        id="captions"
        label="Cinematic captions"
        checked={s.captions}
        onChange={(v) => set({ captions: v })}
      />
      <h3>Session</h3>
      <p className="dim">
        Progress saves automatically in this browser after every challenge. Close the page and
        return whenever you like.
      </p>
      <div className="record-actions">
        <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "start" })}>Back</Btn>
        <Btn onClick={() => dispatch({ type: "OPEN_RESTART" })} variant="danger">
          Restart the ascent
        </Btn>
      </div>
    </section>
  );
}
