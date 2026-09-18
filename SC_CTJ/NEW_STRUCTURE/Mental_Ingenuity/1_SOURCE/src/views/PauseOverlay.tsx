import React from "react";
import { useGame } from "../state/store";
import { audio } from "../audio/engine";
import { Btn, Modal, Slider } from "../components/ui";

export default function PauseOverlay({
  onResume,
  onQuit,
}: {
  onResume: () => void;
  onQuit: () => void;
}) {
  const { state, dispatch } = useGame();
  const s = state.save.settings;

  return (
    <Modal label="Game paused" onClose={onResume}>
      <h2 className="pause-title">Paused</h2>
      <p className="dim">The chamber waits. Audio is quieted while you are away.</p>
      <div className="pause-controls">
        <Btn variant="gold" onClick={onResume} autoFocus ariaLabel="Resume the challenge">
          Resume
        </Btn>
        <Btn
          onClick={() => dispatch({ type: "SET_SETTINGS", patch: { muted: !s.muted } })}
          ariaLabel={s.muted ? "Unmute all audio" : "Mute all audio"}
        >
          {s.muted ? "Unmute audio" : "Mute audio"}
        </Btn>
        <Slider
          id="pause-master"
          label="Master volume"
          value={s.masterVolume}
          onChange={(v) => dispatch({ type: "SET_SETTINGS", patch: { masterVolume: v } })}
        />
        <Slider
          id="pause-music"
          label="Music volume"
          value={s.musicVolume}
          onChange={(v) => dispatch({ type: "SET_SETTINGS", patch: { musicVolume: v } })}
        />
        <Btn onClick={onQuit} ariaLabel="Leave the challenge and return to the chamber map">
          Quit to chamber map
        </Btn>
      </div>
    </Modal>
  );
}
