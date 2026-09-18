import React from "react";
import { useGame } from "../state/store";
import { Btn } from "../components/ui";
import { BRAND_ATTRIBUTION, BRAND_PRODUCT } from "../lib/content";

export default function AboutView() {
  const { dispatch } = useGame();
  return (
    <section className="doc-view about-view" aria-label="About">
      <img
        src="/media/img/about.webp"
        alt="An obsidian monument inlaid with a silver and gold geometric emblem and a single emerald light"
        className="about-img"
      />
      <h2>{BRAND_PRODUCT}</h2>
      <p className="brand-sub">{BRAND_ATTRIBUTION}</p>
      <p>
        Mental Ingenuity is a layered mental adventure. Six chambers, each built around a different
        mode of reasoning, climb toward a summit whose rules move. The experience is designed to
        feel like an ancient intelligence chamber rebuilt with advanced technology.
      </p>
      <p>
        Scores describe how a run of the game unfolded: accuracy, efficiency, insight, and
        adaptability. They are gameplay records only. This product makes no medical, psychological,
        diagnostic, therapeutic, or cognitive improvement claims, and it compares no player to any
        population norm.
      </p>
      <p className="dim">Internal prototype. Not authorized for public release until reviewed and approved.</p>
      <p className="dim">Version 0.9.0 · All art, music, ambience, sound effects, and the opening cinematic are original assets created for this product.</p>
      <Btn onClick={() => dispatch({ type: "NAVIGATE", view: "start" })}>Back</Btn>
    </section>
  );
}
