import React from "react";
import { useGame } from "../state/store";
import { Btn } from "../components/ui";

export default function HelpView() {
  const { dispatch } = useGame();
  return (
    <section className="doc-view" aria-label="Accessibility help">
      <h2>Accessibility Help</h2>
      <h3>Keyboard</h3>
      <ul>
        <li>Tab and Shift plus Tab move focus between controls. A gold outline marks the focused control.</li>
        <li>Enter or Space activates buttons, including grid cells, mirrors, rings, and evidence cards.</li>
        <li>Range inputs respond to the arrow keys. Switches toggle with Enter or Space.</li>
      </ul>
      <h3>Screen readers</h3>
      <ul>
        <li>Every chamber states its objective in text at the top of the screen.</li>
        <li>Gameplay feedback is announced through a polite live region after each action.</li>
        <li>Decorative art is marked so assistive technology skips it. Meaningful images carry descriptions.</li>
      </ul>
      <h3>Motion and color</h3>
      <ul>
        <li>Reduced motion mode, in Settings, calms animation and replaces the cinematic video with a still sequence. It also activates automatically when your operating system requests reduced motion.</li>
        <li>High contrast mode strengthens text contrast and focus outlines.</li>
        <li>No puzzle requires color alone. Shapes, text labels, and position always carry the information.</li>
      </ul>
      <h3>Sound</h3>
      <ul>
        <li>No puzzle requires hearing. Every audio clue has a visible equivalent.</li>
        <li>Master, music, ambience, and effect volumes are separate. Mute all audio at any time.</li>
      </ul>
      <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "start" })}>Back</Btn>
    </section>
  );
}
