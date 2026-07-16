const ADMIN_ROLES = new Set(["owner", "couple_admin", "admin", "planner"]);
const CONTRIBUTOR_ROLES = new Set([...ADMIN_ROLES, "contributor", "guest", "wedding_party"]);

export function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    "\"": "&quot;"
  })[character]);
}

export function cleanText(value, maxLength = 5000) {
  return String(value ?? "").trim().replace(/\u0000/g, "").slice(0, maxLength);
}

export function canAdmin(role) {
  return ADMIN_ROLES.has(String(role ?? "").toLowerCase());
}

export function canContribute(role) {
  return CONTRIBUTOR_ROLES.has(String(role ?? "").toLowerCase());
}

export function capabilitiesFor(role) {
  return Object.freeze({
    admin: canAdmin(role),
    contribute: canContribute(role),
    moderate: canAdmin(role),
    manageAccess: ["owner", "couple_admin", "admin"].includes(String(role ?? "").toLowerCase())
  });
}

export function safeExternalUrl(value, kind = "https") {
  const candidate = cleanText(value, 2048);
  if (!candidate) return "";

  let parsed;
  try {
    parsed = new URL(candidate);
  } catch {
    return "";
  }

  if (parsed.protocol !== "https:") return "";
  const host = parsed.hostname.toLowerCase();
  const allowed = {
    drive: host === "drive.google.com" || host === "docs.google.com",
    dropbox: host === "dropbox.com" || host.endsWith(".dropbox.com"),
    spotify: host === "spotify.com" || host.endsWith(".spotify.com"),
    pandora: host === "pandora.com" || host.endsWith(".pandora.com"),
    apple_music: host === "music.apple.com",
    youtube: host === "youtube.com" || host.endsWith(".youtube.com") || host === "youtu.be",
    https: true,
    image: true,
    ebook: true
  };

  return allowed[kind] ? parsed.href : "";
}

export function safeBackgroundImage(value) {
  const url = safeExternalUrl(value, "image");
  return url ? `linear-gradient(105deg, rgba(82,30,14,.82), rgba(14,124,130,.55)), url(${JSON.stringify(url)})` : "";
}

export function safeFileName(value) {
  const cleaned = cleanText(value, 180)
    .replace(/[^a-zA-Z0-9._-]+/g, "_")
    .replace(/^[._-]+/, "")
    .replace(/[._-]+$/, "");
  return cleaned || "upload";
}

export function buildFeedbackMailto({ supportEmail, type, severity, subject, details, saved }) {
  const safeSubject = cleanText(subject, 180);
  const body = [
    "Vow & Go feedback",
    "",
    `Type: ${cleanText(type, 40)}`,
    `Severity: ${cleanText(severity, 40)}`,
    `Subject: ${safeSubject}`,
    "",
    cleanText(details, 5000),
    "",
    `Saved to Supabase: ${saved ? "Yes" : "No"}`
  ].join("\n");

  return `mailto:${encodeURIComponent(cleanText(supportEmail, 320))}?subject=${encodeURIComponent(`[Vow & Go] ${safeSubject}`)}&body=${encodeURIComponent(body)}`;
}

export function reviewRoleLabel(role, fixture = false) {
  const normalized = String(role ?? "").toLowerCase();
  const labels = {
    owner: "Owner",
    couple_admin: "Couple admin",
    admin: "Admin",
    planner: "Planner",
    contributor: "Contributor",
    guest: "Guest",
    wedding_party: "Wedding party"
  };
  const base = labels[normalized] || "Signed-out review";
  return fixture && normalized ? `${base} fixture` : base;
}

export function weddingCountdown(targetDate, now = new Date()) {
  const target = new Date(targetDate);
  const distance = target.getTime() - now.getTime();
  if (!Number.isFinite(distance) || distance <= 0) {
    return { complete: true, days: 0, hours: 0, minutes: 0, seconds: 0 };
  }
  return {
    complete: false,
    days: Math.floor(distance / 86_400_000),
    hours: Math.floor((distance % 86_400_000) / 3_600_000),
    minutes: Math.floor((distance % 3_600_000) / 60_000),
    seconds: Math.floor((distance % 60_000) / 1000)
  };
}

export function toMoney(value) {
  const amount = Number(value || 0);
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(Number.isFinite(amount) ? amount : 0);
}

export function toLocalDateTime(value) {
  if (!value) return "TBD";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "TBD" : date.toLocaleString();
}
