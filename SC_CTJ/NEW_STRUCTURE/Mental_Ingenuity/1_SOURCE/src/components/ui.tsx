import React from "react";

export function Btn({
  children,
  onClick,
  variant = "ghost",
  disabled,
  ariaLabel,
  className = "",
  autoFocus,
  title,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "ghost" | "gold" | "danger";
  disabled?: boolean;
  ariaLabel?: string;
  className?: string;
  autoFocus?: boolean;
  title?: string;
}) {
  return (
    <button
      type="button"
      className={`btn btn-${variant} ${className}`}
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      title={title}
      ref={autoFocus ? (el) => el?.focus() : undefined}
    >
      {children}
    </button>
  );
}

export function Slider({
  label,
  value,
  onChange,
  id,
}: {
  label: string;
  value: number;
  onChange: (v: number) => void;
  id: string;
}) {
  return (
    <div className="slider-row">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        type="range"
        min={0}
        max={100}
        value={Math.round(value * 100)}
        onChange={(e) => onChange(Number(e.target.value) / 100)}
        aria-valuetext={`${Math.round(value * 100)} percent`}
      />
      <span className="slider-val">{Math.round(value * 100)}%</span>
    </div>
  );
}

export function Toggle({
  label,
  checked,
  onChange,
  id,
  hint,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
  id: string;
  hint?: string;
}) {
  return (
    <div className="toggle-row">
      <div>
        <label htmlFor={id}>{label}</label>
        {hint ? <p className="hint-text">{hint}</p> : null}
      </div>
      <button
        id={id}
        role="switch"
        aria-checked={checked}
        aria-label={label}
        className={`switch ${checked ? "on" : ""}`}
        onClick={() => onChange(!checked)}
        type="button"
      >
        <span className="knob" aria-hidden="true" />
      </button>
    </div>
  );
}

export function Modal({
  children,
  onClose,
  label,
}: {
  children: React.ReactNode;
  onClose?: () => void;
  label: string;
}) {
  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        role="dialog"
        aria-modal="true"
        aria-label={label}
        className="modal-panel"
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  );
}

export function DimBars({ dims }: { dims: { accuracy: number; efficiency: number; insight: number; adaptability: number } }) {
  const rows: Array<[string, number]> = [
    ["Accuracy", dims.accuracy],
    ["Efficiency", dims.efficiency],
    ["Insight", dims.insight],
    ["Adaptability", dims.adaptability],
  ];
  return (
    <div className="dim-bars">
      {rows.map(([label, v]) => (
        <div className="dim-row" key={label}>
          <span className="dim-label">{label}</span>
          <div
            className="dim-track"
            role="img"
            aria-label={`${label}: ${Math.round(v * 100)} percent`}
          >
            <div className="dim-fill" style={{ width: `${Math.round(v * 100)}%` }} />
          </div>
          <span className="dim-num">{Math.round(v * 100)}</span>
        </div>
      ))}
    </div>
  );
}

export function Emblem({ kind, size = 96 }: { kind: string; size?: number }) {
  // Original inline SVG emblems, one per reasoning signature title and achievements.
  const strokes = {
    "Pattern Navigator": "#50c878",
    "Constraint Architect": "#d4af37",
    "Perspective Shifter": "#c0c0c0",
    "Systems Reader": "#5fd0a0",
    "Evidence Weaver": "#d8c07a",
    "Adaptive Strategist": "#e0c060",
  } as Record<string, string>;
  const c = strokes[kind] ?? "#d4af37";
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 96 96"
      role="img"
      aria-label={`${kind} emblem`}
      className="emblem"
    >
      <circle cx="48" cy="48" r="42" fill="none" stroke={c} strokeWidth="2" opacity="0.8" />
      <circle cx="48" cy="48" r="30" fill="none" stroke="#c0c0c0" strokeWidth="1.4" opacity="0.7" />
      <path d="M48 14 L76 32 V64 L48 82 L20 64 V32 Z" fill="none" stroke={c} strokeWidth="2.2" />
      <path d="M48 28 L62 37 V55 L48 64 L34 55 V37 Z" fill={c} opacity="0.16" stroke={c} strokeWidth="1.4" />
      <circle cx="48" cy="46" r="5" fill={c} />
      <path d="M48 51 V64" stroke={c} strokeWidth="2" />
    </svg>
  );
}
