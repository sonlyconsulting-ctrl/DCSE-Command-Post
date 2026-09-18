import React, { useCallback, useMemo, useState } from "react";
import { PARADOX_CASES } from "../lib/content";
import type { EvidenceCard } from "../lib/content";
import { Rand } from "../lib/rng";
import { audio } from "../audio/engine";
import { Btn } from "../components/ui";
import { ChamberShell, Session, markRecovered, seedFor, useSession } from "./shared";

type Role = "assumption" | "contradiction" | "misleading";

const SLOTS: { role: Role; label: string; desc: string }[] = [
  { role: "assumption", label: "Hidden Assumption", desc: "The unstated belief the claim leans on." },
  { role: "contradiction", label: "Contradicting Evidence", desc: "A record the claim cannot survive." },
  { role: "misleading", label: "Misleading Comparison", desc: "A careful-sounding move that leads nowhere." },
];

export default function ParadoxVault({
  level,
  paused,
  onPause,
}: {
  level: number;
  paused: boolean;
  onPause: () => void;
}) {
  const kase = PARADOX_CASES[level];
  const session = useSession("paradox", level, 4);
  const [attemptSeed, setAttemptSeed] = useState(0);
  const order = useMemo(() => {
    const rnd = new Rand(seedFor("paradox", level, attemptSeed));
    return rnd.shuffle(kase.cards.map((c) => c.id));
  }, [kase, level, attemptSeed]);

  const [selected, setSelected] = useState<string | null>(null);
  const [placed, setPlaced] = useState<Record<Role, string | null>>({
    assumption: null,
    contradiction: null,
    misleading: null,
  });
  const [verdictPhase, setVerdictPhase] = useState(false);
  const [explainPhase, setExplainPhase] = useState(false);
  const [wrongCard, setWrongCard] = useState<string | null>(null);

  const placedIds = Object.values(placed).filter(Boolean) as string[];
  const cardById = useMemo(() => {
    const m = new Map<string, EvidenceCard>();
    kase.cards.forEach((c) => m.set(c.id, c));
    return m;
  }, [kase]);

  const selectCard = useCallback(
    (id: string) => {
      if (paused || verdictPhase || explainPhase) return;
      if (placedIds.includes(id)) return;
      setSelected((s) => (s === id ? null : id));
      audio.playSfx("select");
    },
    [paused, verdictPhase, explainPhase, placedIds]
  );

  const placeInto = useCallback(
    (role: Role) => {
      if (paused || verdictPhase || explainPhase) return;
      if (!selected) {
        session.setMsg("Select an evidence card first, then choose its role.");
        return;
      }
      session.addMove();
      const card = cardById.get(selected);
      if (!card) return;
      if (card.role === role) {
        setPlaced((p) => ({ ...p, [role]: selected }));
        setSelected(null);
        markRecovered(session);
        audio.playSfx("discover");
        const remaining = SLOTS.length - (placedIds.length + 1);
        session.setMsg(
          remaining > 0
            ? "The card settles into its true role. " + remaining + " roles remain."
            : "Every role is filled. Now judge which claim survives."
        );
        if (remaining <= 0) {
          setVerdictPhase(true);
        }
      } else {
        session.addError();
        setWrongCard(selected);
        window.setTimeout(() => setWrongCard(null), 600);
        session.setMsg("That card does not serve this role. Read what it actually does to the claim.");
      }
    },
    [paused, verdictPhase, explainPhase, selected, cardById, placedIds, session]
  );

  const verdict = useCallback(
    (v: "claim" | "alt" | "neither") => {
      if (paused || explainPhase) return;
      session.addMove();
      if (v === kase.verdict) {
        markRecovered(session);
        setExplainPhase(true);
        session.setMsg("The vault opens. Read why the conclusion fell.");
        audio.playSfx("discover");
      } else {
        session.addError();
        audio.playSfx("invalid");
        session.setMsg("That reading still rests on the flaw you mapped. Look at the roles again.");
      }
    },
    [paused, explainPhase, kase, session]
  );

  const seal = useCallback(() => {
    const contra = cardById.get(placed.contradiction as string);
    session.finish(
      "The hidden assumption carrying the attractive claim",
      "Each role accepts exactly one card; the rest stay neutral",
      session.errors === 0
        ? "Judged each card by what it does to the claim before placing it"
        : "Tested placements, rejected what failed, and rebuilt the mapping",
      contra ? `The record: "${contra.text}"` : "The contradicting record",
      { recoveredAfterError: session.errors > 0 }
    );
  }, [cardById, placed, session]);

  return (
    <ChamberShell
      chamber="paradox"
      level={level}
      session={session}
      onPause={onPause}
      onReset={() => {
        setPlaced({ assumption: null, contradiction: null, misleading: null });
        setSelected(null);
        setVerdictPhase(false);
        setExplainPhase(false);
        session.failAttempt();
        setAttemptSeed((s) => s + 1);
      }}
    >
      <div className={`vault-layout ${paused ? "veiled" : ""}`}>
        {!explainPhase ? (
          <>
            <div className="vault-claim">
              <h3>The claim under review</h3>
              <p className="claim-text">{kase.claim}</p>
              <p className="claim-alt">Rival claim: {kase.altClaim}</p>
            </div>
            <div className="vault-slots" role="group" aria-label="Evidence roles">
              {SLOTS.map((s) => (
                <button
                  key={s.role}
                  type="button"
                  className={`vault-slot ${placed[s.role] ? "filled" : ""} ${selected ? "ready" : ""}`}
                  onClick={() => placeInto(s.role)}
                  aria-label={`${s.label} slot. ${placed[s.role] ? "Filled." : "Empty. Activate to place the selected card."}`}
                >
                  <span className="slot-label">{s.label}</span>
                  <span className="slot-desc">{s.desc}</span>
                  {placed[s.role] ? (
                    <span className="slot-card">{cardById.get(placed[s.role] as string)?.text}</span>
                  ) : null}
                </button>
              ))}
            </div>
            {!verdictPhase ? (
              <div className="vault-cards" role="group" aria-label="Evidence cards">
                {order.map((id) => {
                  const card = cardById.get(id) as EvidenceCard;
                  if (placedIds.includes(id)) return null;
                  return (
                    <button
                      key={id}
                      type="button"
                      className={`vault-card ${selected === id ? "selected" : ""} ${wrongCard === id ? "wrong" : ""}`}
                      onClick={() => selectCard(id)}
                      aria-pressed={selected === id}
                      aria-label={`Evidence card: ${card.text}`}
                    >
                      {card.text}
                    </button>
                  );
                })}
              </div>
            ) : (
              <div className="vault-verdict" role="group" aria-label="Verdict">
                <h3>Which claim survives the evidence?</h3>
                <Btn onClick={() => verdict("claim")} ariaLabel="Verdict: the original claim survives">
                  The original claim survives
                </Btn>
                <Btn onClick={() => verdict("alt")} ariaLabel="Verdict: the rival claim survives">
                  The rival claim survives
                </Btn>
                <Btn onClick={() => verdict("neither")} ariaLabel="Verdict: neither claim survives">
                  Neither claim survives
                </Btn>
              </div>
            )}
          </>
        ) : (
          <div className="vault-explain">
            <h3>Why the conclusion failed</h3>
            <p>{kase.explanation}</p>
            <ul>
              {SLOTS.map((s) => {
                const c = cardById.get(placed[s.role] as string);
                return c ? (
                  <li key={s.role}>
                    <strong>{s.label}:</strong> {c.note}
                  </li>
                ) : null;
              })}
            </ul>
            <Btn onClick={seal} variant="gold" ariaLabel="Seal the case and continue">
              Seal the case
            </Btn>
          </div>
        )}
      </div>
    </ChamberShell>
  );
}
