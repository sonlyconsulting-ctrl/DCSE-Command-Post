import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm";

const cfg = window.VOW_GO_CONFIG || {};
const statusEl = document.getElementById("vg-sync-status");
const setStatus = (message, tone = "neutral") => {
  if (!statusEl) return;
  statusEl.textContent = message;
  statusEl.style.background = tone === "ok" ? "#1B6E5C" : tone === "error" ? "#C0392B" : "#2C2420";
};

const supabase = cfg.supabaseUrl && cfg.supabasePublishableKey
  ? createClient(cfg.supabaseUrl, cfg.supabasePublishableKey, {
      auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
    })
  : null;

let currentUser = null;
let product = null;
let role = null;
const adminRoles = () => ["owner", "couple_admin", "planner"];

async function resolveSession() {
  if (!supabase) {
    setStatus("Demo mode: Supabase not configured");
    return;
  }
  const { data, error } = await supabase.auth.getSession();
  if (error) {
    setStatus("Auth unavailable", "error");
    return;
  }
  currentUser = data.session?.user || null;
  if (!currentUser) {
    setStatus("Preview mode: sign-in required for sync");
    return;
  }

  const { data: memberships, error: memberError } = await supabase
    .schema("family_core")
    .from("product_memberships")
    .select("role, product_instance_id, product_instances!inner(id,title,product_type,status)")
    .eq("user_id", currentUser.id)
    .eq("status", "active")
    .eq("product_instances.product_type", "vow_go");

  if (memberError) {
    console.error(memberError);
    setStatus("Connected; Family schema API exposure pending", "error");
    return;
  }

  const membership = memberships?.[0];
  if (!membership) {
    setStatus("Signed in; no Vow & Go assignment");
    return;
  }

  product = membership.product_instances;
  role = membership.role;
  setStatus(`Synced · ${role}`, "ok");
  await hydrate();
}

async function hydrate() {
  if (!product || !supabase) return;
  const pid = product.id;
  const [profileResult, settingsResult, tasksResult, guestsResult, mediaResult, wishesResult] = await Promise.all([
    supabase.schema("family_vow_go").from("wedding_profiles").select("*").eq("product_instance_id", pid).maybeSingle(),
    supabase.schema("family_vow_go").from("wedding_settings").select("*").eq("product_instance_id", pid).maybeSingle(),
    supabase.schema("family_vow_go").from("wedding_tasks").select("*").eq("product_instance_id", pid).order("due_date"),
    supabase.schema("family_vow_go").from("guests").select("*").eq("product_instance_id", pid),
    supabase.schema("family_vow_go").from("wedding_media").select("*").eq("product_instance_id", pid),
    supabase.schema("family_vow_go").from("guestbook_entries").select("*").eq("product_instance_id", pid)
  ]);

  const profile = profileResult.data;
  const settings = settingsResult.data;
  if (profile?.couple_names) {
    document.querySelectorAll(".brand-sub").forEach(el => {
      el.textContent = `${profile.couple_names} · ${profile.wedding_date || "Wedding"}`;
    });
  }
  if (settings) {
    const guestbookMode = document.getElementById("assistant-guestbook-mode");
    const mediaMode = document.getElementById("assistant-media-mode");
    if (guestbookMode) guestbookMode.value = settings.guestbook_mode || "moderated";
    if (mediaMode) mediaMode.value = settings.media_mode || "moderated";
  }

  const cards = [...document.querySelectorAll(".stat-card")];
  const guests = guestsResult.data || [];
  const tasks = tasksResult.data || [];
  const media = mediaResult.data || [];
  const wishes = wishesResult.data || [];
  if (cards[0]) cards[0].querySelector(".stat-num").textContent = String(guests.filter(g => g.rsvp_status === "confirmed").reduce((n, g) => n + (g.party_size || 1), 0));
  if (cards[1]) cards[1].querySelector(".stat-num").textContent = String(media.filter(m => m.moderation_status === "pending").length);
  if (cards[2]) {
    const done = tasks.filter(t => t.status === "done" || t.status === "completed").length;
    cards[2].querySelector(".stat-num").textContent = `${tasks.length ? Math.round(done / tasks.length * 100) : 0}%`;
  }
  if (cards[3]) cards[3].querySelector(".stat-num").textContent = String(wishes.filter(w => w.moderation_status === "pending").length);
}

async function saveAssistantPolicy() {
  if (!supabase || !currentUser || !product) return setStatus("Sign in to save policy", "error");
  if (!adminRoles().includes(role)) return setStatus("Admin role required", "error");
  const payload = {
    product_instance_id: product.id,
    guestbook_mode: document.getElementById("assistant-guestbook-mode")?.value || "moderated",
    media_mode: document.getElementById("assistant-media-mode")?.value || "moderated",
    updated_by: currentUser.id,
    updated_at: new Date().toISOString()
  };
  const { error } = await supabase.schema("family_vow_go").from("wedding_settings").upsert(payload);
  if (error) {
    console.error(error);
    return setStatus("Policy save failed", "error");
  }
  setStatus("Assistant policy saved", "ok");
}

function planningRecommendations() {
  const items = [
    ["DJ and sound", "Compare ceremony audio, reception coverage, microphones, announcements, backup equipment, clean edits, and first-dance licensing."],
    ["Flowers and décor", "Review bouquets, ceremony pieces, reception tables, delivery windows, climate durability, allergies, reuse, and cleanup."],
    ["Special needs", "Confirm mobility access, hearing support, dietary restrictions, medication handling, childcare, transportation, and quiet space."],
    ["Photography and video", "Set shot list, hero-video permissions, delivery formats, backup storage, guest privacy, and publication rights."],
    ["Travel and lodging", "Track flights, hotel blocks, ground transportation, arrival windows, emergency contacts, and local recommendations."],
    ["Legal and ceremony", "Confirm marriage license, officiant, witnesses, ceremony order, name-change needs, and document retention."],
    ["Honeymoon handoff", "Set the chapter unlock date, media intake, itinerary privacy, and what planning modules archive after the wedding."]
  ];
  const host = document.getElementById("assistant-recommendations");
  if (!host) return;
  host.innerHTML = items.map(([title, detail]) => `<div class="check-item"><div class="check-box"></div><div><div class="check-label">${title}</div><div class="check-sub">${detail}</div></div></div>`).join("");
}

async function submitFeedback() {
  const subject = document.getElementById("feedback-subject")?.value.trim();
  const details = document.getElementById("feedback-details")?.value.trim();
  const type = document.getElementById("feedback-type")?.value || "other";
  const severity = document.getElementById("feedback-severity")?.value || "normal";
  const feedbackStatus = document.getElementById("feedback-status");
  if (!subject || !details) {
    if (feedbackStatus) feedbackStatus.textContent = "Subject and details are required.";
    return;
  }
  let saved = false;
  if (supabase && currentUser && product) {
    const { error } = await supabase.schema("family_vow_go").from("admin_feedback").insert({
      product_instance_id: product.id,
      submitted_by: currentUser.id,
      feedback_type: type,
      severity,
      subject,
      details,
      page_context: location.href
    });
    saved = !error;
    if (error) console.error(error);
  }
  const body = encodeURIComponent(`Vow & Go feedback\n\nType: ${type}\nSeverity: ${severity}\nSubject: ${subject}\n\n${details}\n\nPage: ${location.href}\nSaved to Supabase: ${saved ? "Yes" : "No"}`);
  if (feedbackStatus) feedbackStatus.textContent = saved ? "Saved to the product record. Your email app will open for delivery to Sonly Consulting." : "Email draft prepared. Sign in to also save feedback inside the product record.";
  window.location.href = `mailto:${cfg.supportEmail || "sonlyconsulting@gmail.com"}?subject=${encodeURIComponent(`[Vow & Go] ${subject}`)}&body=${body}`;
}

document.getElementById("assistant-save-policy")?.addEventListener("click", saveAssistantPolicy);
document.getElementById("assistant-refresh")?.addEventListener("click", planningRecommendations);
document.getElementById("feedback-submit")?.addEventListener("click", submitFeedback);
planningRecommendations();
resolveSession();
supabase?.auth.onAuthStateChange(() => resolveSession());
