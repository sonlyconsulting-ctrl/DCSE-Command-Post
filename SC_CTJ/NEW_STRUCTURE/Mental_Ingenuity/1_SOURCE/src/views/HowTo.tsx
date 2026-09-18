import React from "react";
import { useGame } from "../state/store";
import { Btn } from "../components/ui";

export default function HowTo() {
  const { dispatch } = useGame();
  return (
    <section className="doc-view" aria-label="How to play">
      <h2>How to Play</h2>
      <p className="lede">
        The Ingenuity Ascent is a sequence of six chambers. Each chamber trains a different way of
        thinking, and each one contains three challenges of rising difficulty.
      </p>
      <h3>The chambers</h3>
      <ul>
        <li><strong>The Signal Chamber.</strong> Watch pulses travel a grid, then reproduce the true sequence while noise flashes try to mislead you.</li>
        <li><strong>The Constraint Forge.</strong> Rotate mirrors to route a beam into its core. Every rotation spends one move from a strict budget.</li>
        <li><strong>The Perspective Engine.</strong> Turn concentric rings, some of them gear linked, until every gold mark stands on the sight axis.</li>
        <li><strong>The Causal Labyrinth.</strong> Adjust regulators and advance time. Delayed nodes and feedback decide when the gate stabilizes.</li>
        <li><strong>The Paradox Vault.</strong> Map evidence to its true role and decide which attractive claim actually survives.</li>
        <li><strong>The Summit.</strong> Three disciplines converge, and the law of the gate changes mid-climb. Read, adapt, choose.</li>
      </ul>
      <h3>Controls</h3>
      <ul>
        <li>Everything works with pointer, touch, or keyboard. Tab moves focus, Enter and Space activate.</li>
        <li>In the Perspective Engine you can also drag a ring to rotate it.</li>
        <li>Every chamber shows its objective, your moves, the par, and your remaining hints.</li>
        <li>Reset restarts the current challenge. The Forge adds Undo for single rotations.</li>
        <li>Pause opens the pause panel and quiets all audio.</li>
      </ul>
      <h3>Hints and scoring</h3>
      <ul>
        <li>You carry a shared pool of hints. Using one reduces the Insight dimension of your score.</li>
        <li>Score is read across four dimensions: Accuracy, Efficiency, Insight, and Adaptability.</li>
        <li>This is a gameplay score describing how a run unfolded. It is not an intelligence score and is never compared to any norm.</li>
      </ul>
      <h3>Sound is never required</h3>
      <p>
        Every audio clue also appears as a visual event. You can mute the entire game and lose
        nothing essential. Reduced motion mode replaces the cinematic video with a still sequence.
      </p>
      <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "start" })} variant="gold">
        Back
      </Btn>
    </section>
  );
}
