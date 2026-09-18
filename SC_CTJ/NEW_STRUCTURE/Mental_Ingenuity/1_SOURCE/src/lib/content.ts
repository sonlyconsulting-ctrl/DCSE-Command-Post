import type { ChamberId } from "./types";

export interface ChamberMeta {
  id: ChamberId;
  name: string;
  tagline: string;
  ops: string[];
  art: string;
  music: string | null;
  ambience: string | null;
  accent: string;
  objectives: [string, string, string];
}

export const CHAMBER_META: Record<ChamberId, ChamberMeta> = {
  signal: {
    id: "signal",
    name: "The Signal Chamber",
    tagline: "Separate the true signal from deliberate noise.",
    ops: ["Perception", "Pattern recognition", "Evidence filtering"],
    art: "/media/img/chamber_signal.webp",
    music: "music_focus",
    ambience: "amb_signal",
    accent: "#50c878",
    objectives: [
      "Watch the sequence, then trace the true signal in order. Ignore the noise flashes.",
      "A longer signal crosses a wider field with more noise. Trace it in order.",
      "The deepest field. The signal leaps in an unusual rhythm. Trace it exactly.",
    ],
  },
  forge: {
    id: "forge",
    name: "The Constraint Forge",
    tagline: "Route the beam with a strict budget of moves.",
    ops: ["Planning under constraints", "Sequencing", "Efficiency"],
    art: "/media/img/chamber_forge.webp",
    music: "music_structure",
    ambience: "amb_forge",
    accent: "#d4af37",
    objectives: [
      "Rotate the mirrors to guide the beam into the core. Every rotation costs one move.",
      "Decoy mirrors crowd the channel. Find the clean route within the budget.",
      "Locked plating blocks the direct path. More than one route can succeed.",
    ],
  },
  perspective: {
    id: "perspective",
    name: "The Perspective Engine",
    tagline: "The alignment only appears from the right orientation.",
    ops: ["Spatial reasoning", "Mental rotation", "Abstraction"],
    art: "/media/img/chamber_perspective.webp",
    music: "music_structure",
    ambience: "amb_perspective",
    accent: "#c0c0c0",
    objectives: [
      "Turn the rings until every gold mark stands on the sight axis at the top.",
      "The inner rings are gear linked. Turning one turns another. Align every gold mark.",
      "A full gear train. Three marks, coupled rings, one axis of sight.",
    ],
  },
  causal: {
    id: "causal",
    name: "The Causal Labyrinth",
    tagline: "Every adjustment moves the whole system.",
    ops: ["Systems thinking", "Cause and effect", "Feedback recognition"],
    art: "/media/img/chamber_causal.webp",
    music: "music_focus",
    ambience: "amb_causal",
    accent: "#5fd0a0",
    objectives: [
      "Set the three regulators, then advance time until the gate reads stable.",
      "One node runs on a delay. Plan the order of your adjustments.",
      "A memory node counts repeated pressure. Feed the system carefully.",
    ],
  },
  paradox: {
    id: "paradox",
    name: "The Paradox Vault",
    tagline: "An attractive conclusion hides a flaw. Find it.",
    ops: ["Deductive review", "Assumption detection", "Evidence reconciliation"],
    art: "/media/img/chamber_vault.webp",
    music: "music_tension",
    ambience: "amb_vault",
    accent: "#d8c07a",
    objectives: [
      "Place each key piece of evidence into its true role, then name the surviving claim.",
      "Two claims compete. One rests on a hidden assumption. Map the evidence.",
      "The most persuasive claim in the vault is also the weakest. Break it open.",
    ],
  },
  summit: {
    id: "summit",
    name: "The Summit",
    tagline: "Three disciplines, one gate, and a law that changes.",
    ops: ["Synthesis", "Adaptability", "Strategic judgment"],
    art: "/media/img/chamber_summit.webp",
    music: "music_summit",
    ambience: "amb_summit",
    accent: "#e0c060",
    objectives: [
      "Trace, route, and align. Then read the law of the gate before you choose.",
      "The Ascent tests again, with tighter tolerances. Watch for the revision.",
      "The final ascent. Every system converges at the gate.",
    ],
  },
};

export const OPENING_LINE =
  "The ascent does not measure what the mind knows. It reveals how the mind moves.";

export const BRAND_PRODUCT = "Mental Ingenuity";
export const BRAND_ATTRIBUTION = "Powered by Sonly Consulting";

/** Paradox Vault cases. Original in-world content. */
export interface EvidenceCard {
  id: string;
  text: string;
  role: "assumption" | "contradiction" | "misleading" | "neutral";
  note: string;
}

export interface ParadoxCase {
  id: string;
  title: string;
  claim: string;
  altClaim: string;
  cards: EvidenceCard[];
  verdict: "claim" | "alt" | "neither";
  explanation: string;
}

export const PARADOX_CASES: ParadoxCase[] = [
  {
    id: "beacon",
    title: "The Beacon Record",
    claim:
      "The eastern beacon was lit on trading days, so every barge on the river must have followed the eastern channel.",
    altClaim:
      "The beacon was lit only on festival nights, so river traffic ignored it entirely.",
    cards: [
      {
        id: "b1",
        text: "Harbor logs from that season show most barges recorded in the western channel.",
        role: "contradiction",
        note: "Direct records conflict with the claim that every barge followed the east.",
      },
      {
        id: "b2",
        text: "The argument presumes that a lit beacon forces all traffic toward it.",
        role: "assumption",
        note: "The claim quietly assumes light dictates choice. No evidence establishes that.",
      },
      {
        id: "b3",
        text: "The western lighthouse was built one hundred years later, so the two lights cannot be compared.",
        role: "misleading",
        note: "This comparison sounds careful but rules out the only useful comparison by age alone.",
      },
      {
        id: "b4",
        text: "The beacon keeper's ledger records fuel purchases for the season.",
        role: "neutral",
        note: "True, but it says nothing about which channel the barges chose.",
      },
      {
        id: "b5",
        text: "Stone quays exist on both banks of the river.",
        role: "neutral",
        note: "Consistent with either channel being used.",
      },
      {
        id: "b6",
        text: "A poem of the period praises the beacon's beauty.",
        role: "neutral",
        note: "Atmosphere, not evidence of traffic patterns.",
      },
    ],
    verdict: "neither",
    explanation:
      "The harbor logs contradict the sweeping claim about every barge, and the claim leans on an unstated assumption that light compels traffic. The festival theory also fails, because the fuel ledger shows sustained seasonal burning. Neither grand claim survives; the modest reading is that the beacon burned while traffic split between channels.",
  },
  {
    id: "clockwork",
    title: "The Clockwork Census",
    claim:
      "Chambers with more silver gears kept more accurate time, so adding gears to any chamber will make it more accurate.",
    altClaim:
      "Gear count is irrelevant. Only the size of the chamber matters for accuracy.",
    cards: [
      {
        id: "c1",
        text: "The richest chambers also received the most maintenance visits each month.",
        role: "contradiction",
        note: "Maintenance, not gear count, may be the true driver of accuracy.",
      },
      {
        id: "c2",
        text: "The reasoning presumes that correlation between gears and accuracy means gears cause accuracy.",
        role: "assumption",
        note: "The leap from 'moves together' to 'one produces the other' is the hidden step.",
      },
      {
        id: "c3",
        text: "A chamber with fewer gears but daily calibration outperformed every uncalibrated chamber.",
        role: "contradiction",
        note: "A single well kept counterexample breaks the rule the claim tries to make.",
      },
      {
        id: "c4",
        text: "Gears in the Ascent are made from the same silver alloy.",
        role: "neutral",
        note: "Material uniformity does not separate cause from coincidence.",
      },
      {
        id: "c5",
        text: "Some chambers were rebuilt after the first census and kept their old names.",
        role: "misleading",
        note: "This invites doubt about the records, but it is raised without any showing of error.",
      },
      {
        id: "c6",
        text: "The census takers used identical measuring rods.",
        role: "neutral",
        note: "Consistent method, silent on causation.",
      },
    ],
    verdict: "neither",
    explanation:
      "The claim mistakes correlation for causation and is contradicted twice over: maintenance co-varies with gear count, and a calibrated low-gear chamber beat the rest. Chamber size alone does not explain accuracy either, since calibration separates chambers of the same size. The surviving reading is that upkeep, not gear count, carried the accuracy.",
  },
  {
    id: "gate",
    title: "The Gate Testimony",
    claim:
      "Every keeper who opened the summit gate reported a tone sounding first, so sounding the tone will open the gate.",
    altClaim:
      "Keepers invented the tone story to hide the true mechanism, so the tone never sounded at all.",
    cards: [
      {
        id: "g1",
        text: "The gate's hinge mechanism is mechanically coupled to a tone bell that rings when the hinges move.",
        role: "contradiction",
        note: "The tone follows the opening. It is an effect, not a key.",
      },
      {
        id: "g2",
        text: "The claim presumes that because the tone precedes the report of opening, it causes the opening.",
        role: "assumption",
        note: "Sequence is treated as power. That hidden step is the flaw.",
      },
      {
        id: "g3",
        text: "One keeper's journal records the tone 'twice, once before and once after' the gate moved.",
        role: "neutral",
        note: "Rich detail, but it describes the same coupled bell.",
      },
      {
        id: "g4",
        text: "Keepers were trained together in the same hall and shared a common vocabulary.",
        role: "misleading",
        note: "Shared training hints at shared language, yet the claim smuggles it in as proof of collusion.",
      },
      {
        id: "g5",
        text: "An apprentice once sounded the tone alone and the gate did not move.",
        role: "contradiction",
        note: "A direct negative test: tone without opening.",
      },
      {
        id: "g6",
        text: "The summit gate is the only gate fitted with a tone bell.",
        role: "neutral",
        note: "True and distinctive, but it explains the report rather than the mechanism.",
      },
    ],
    verdict: "neither",
    explanation:
      "The hinge coupling shows the tone is a side effect of opening, and the apprentice's failed trial is a clean negative test against the tone as a key. The deception theory collapses too, because the bell physically exists and rings on movement. The evidence points to a mechanism the keepers described faithfully but in the wrong causal direction.",
  },
];
