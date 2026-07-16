import { VOW_GO_CONFIG as config } from "./config.js";
import { escapeHtml, cleanText, safeExternalUrl, weddingCountdown, toMoney } from "./vow-go-core.js";
import { TITLES, ROLE_LABELS, MODES, ROLE_MODULES, WRITE_ROLES, ADMIN_ROLES, COLLECTIONS, DEFAULT_STATE } from "./app-data.js";

const STORAGE_KEY = "vow-go-review-v2";
const $ = (id) => document.getElementById(id);
const clone = (value) => JSON.parse(JSON.stringify(value));
const now = () => new Date().toISOString();

let state = loadState();
let supabase = null;
let liveUser = null;
let dialogContext = null;
let pendingConfirm = null;

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved?.version === 2 && Array.isArray(saved.engagements)) return saved;
  } catch { /* ignore invalid local preview state */ }
  return clone(DEFAULT_STATE);
}

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function activeEngagement() {
  return state.engagements.find((item) => item.id === state.activeEngagementId) || state.engagements[0];
}

function setStatus(message, type = "neutral") {
  const bar = $("app-status");
  bar.textContent = message;
  bar.dataset.type = type;
}

function modulesFor(role = state.role, engagement = activeEngagement()) {
  if (role === "platform_owner") return ROLE_MODULES.platform_owner;
  const roleModules = ROLE_MODULES[role] || ROLE_MODULES.signed_out;
  const modeModules = MODES[engagement.mode]?.modules || MODES.experience_only.modules;
  return roleModules.filter((module) => modeModules.includes(module));
}

function canWrite(collection) {
  if (collection === "feedback") return true;
  if (!WRITE_ROLES.has(state.role)) return false;
  if (state.role === "guest_participant") return ["media","feedback"].includes(collection);
  if (state.role === "trusted_contributor") return ["tasks","party","media","story","communications","feedback"].includes(collection);
  return true;
}

function canArchive(collection) {
  return ADMIN_ROLES.has(state.role) || (state.role === "couple_collaborator" && !["budget","feedback"].includes(collection));
}

function applyUrlState() {
  const params = new URLSearchParams(location.search);
  const requestedRole = params.get("role") || params.get("review");
  const roleAliases = { admin: "couple_owner", owner: "couple_owner", contributor: "trusted_contributor", guest: "guest_viewer", "signed-out": "signed_out" };
  const role = roleAliases[requestedRole] || requestedRole;
  if (ROLE_LABELS[role] && config.allowReviewFixtures) state.role = role;
  const mode = params.get("mode");
  if (MODES[mode]) activeEngagement().mode = mode;
  const engagement = params.get("engagement");
  if (state.engagements.some((item) => item.id === engagement)) state.activeEngagementId = engagement;
  const page = params.get("page");
  if (TITLES[page]) state.page = page;
}

function syncUrl() {
  const url = new URL(location.href);
  url.searchParams.set("role", state.role);
  url.searchParams.set("mode", activeEngagement().mode);
  url.searchParams.set("engagement", state.activeEngagementId);
  url.searchParams.set("page", state.page);
  history.replaceState({}, "", url);
}

function renderEngagementSelector() {
  const selector = $("engagement-select");
  selector.replaceChildren(...state.engagements.map((engagement) => {
    const option = document.createElement("option");
    option.value = engagement.id;
    option.textContent = engagement.name;
    option.selected = engagement.id === state.activeEngagementId;
    return option;
  }));
  selector.disabled = !["planner","couple_owner","platform_owner"].includes(state.role);
}

function renderNavigation() {
  const nav = $("primary-nav");
  const modules = modulesFor();
  if (!modules.includes(state.page)) state.page = modules[0] || "dashboard";
  nav.innerHTML = modules.map((key) => `<button type="button" class="nav-button${key === state.page ? " active" : ""}" data-page="${key}" ${key === state.page ? 'aria-current="page"' : ""}><span>${navIcon(key)}</span>${escapeHtml(TITLES[key])}</button>`).join("");
}

function navIcon(key) {
  return ({dashboard:"⌂",story:"♥",media:"▣",tasks:"✓",vendors:"◇",budget:"$",guests:"♧",party:"♢",schedule:"◷",travel:"✈",guide:"⌖",music:"♫",communications:"✉",help:"?",settings:"⚙",feedback:"!",platform:"◆"})[key] || "•";
}

function renderHeader() {
  const engagement = activeEngagement();
  $("page-title").textContent = TITLES[state.page];
  $("page-eyebrow").textContent = state.role === "platform_owner" ? "Platform governance" : engagement.name;
  $("page-summary").textContent = pageSummary(state.page);
  $("role-badge").textContent = ROLE_LABELS[state.role];
  $("mode-badge").textContent = MODES[engagement.mode].label;
  document.title = `${TITLES[state.page]} | Vow & Go`;
  document.documentElement.dataset.theme = engagement.theme;
}

function pageSummary(page) {
  return ({
    dashboard:"The approved wedding experience, priorities, countdown, and role-specific next steps.", story:"Couple-owned chapters and ebook links from proposal through future milestones.", media:"Private intake, moderation, publication approval, and authorized downloads.", tasks:"Operational task state, ownership, reminders, and activity history.", vendors:"Vendor research, agreements, attachments, status, and payment coordination.", budget:"Item-level estimates, commitments, deposits, payments, balances, and exports.", guests:"Guest administration, wedding-party roles, RSVP, invitations, dietary and accessibility needs.", party:"Measurements, fittings, rehearsals, role schedules, acknowledgements, and private notes.", schedule:"Guest-facing events and the complete planner master timeline.", travel:"Flights, lodging, ground transport, arrival windows, and confirmations.", guide:"Manually curated destination guidance and ordinary external map links; no GPS tracking.", music:"Provider links and wedding-moment playlists without requiring provider OAuth.", communications:"Admin communications, guest announcements, direct messages, and notifications.", help:"Page-specific instructions, visibility guidance, recommended workflow, and common mistakes.", settings:"Accounts, roles, administrators, themes, product mode, module state, and audit history.", feedback:"Secure support intake with confirmation and Gmail/copy fallbacks.", platform:"Templates, planner approval, licensing placeholders, support, and authorized audit access."
  })[page] || "Vow & Go wedding workspace.";
}

function renderPage() {
  const content = $("page-content");
  if (state.page === "dashboard") content.innerHTML = dashboardTemplate();
  else if (state.page === "settings") content.innerHTML = settingsTemplate();
  else if (state.page === "help") content.innerHTML = helpTemplate();
  else if (state.page === "platform") content.innerHTML = platformTemplate();
  else if (state.page === "party") content.innerHTML = collectionPage("party") + collectionPage("measurements", true);
  else if (state.page === "guide") content.innerHTML = collectionPage("guide") + collectionPage("faqs", true);
  else if (state.page === "guests" && ["guest_participant","guest_viewer","signed_out"].includes(state.role)) content.innerHTML = guestSelfServiceTemplate();
  else content.innerHTML = collectionPage(pageCollection(state.page));
  bindPageControls();
}

function pageCollection(page) {
  return ({schedule:"events"})[page] || page;
}

function dashboardTemplate() {
  const engagement = activeEngagement();
  const records = engagement.records;
  const tasks = records.tasks.filter((item) => !item.archived);
  const completed = tasks.filter((item) => item.status === "completed").length;
  const countdown = weddingCountdown(`${engagement.weddingDate}T16:00:00-10:00`);
  const planningEnabled = modulesFor().includes("tasks");
  return `<div class="hero"><div><p class="eyebrow">${escapeHtml(engagement.tagline)}</p><h2>${escapeHtml(engagement.couple)}</h2><p>${countdown.complete ? "The celebration chapter is open." : `${countdown.days} days until the wedding`}</p></div><div class="island-orbit" aria-hidden="true"><span>Cabo</span><i>→</i><span>Hawaii</span></div></div>
  <div class="stat-grid">
    <article class="stat-card"><span>Guests confirmed</span><strong>${records.guests.filter((g)=>g.rsvp==="confirmed"&&!g.archived).length}</strong></article>
    <article class="stat-card"><span>Approved gallery items</span><strong>${records.media.filter((m)=>m.moderation_status==="approved"&&!m.archived).length}</strong></article>
    <article class="stat-card"><span>Schedule items</span><strong>${records.events.filter((e)=>!e.archived).length}</strong></article>
    ${planningEnabled ? `<article class="stat-card"><span>Task completion</span><strong>${tasks.length ? Math.round(completed/tasks.length*100) : 0}%</strong></article>` : ""}
  </div>
  <div class="content-grid two">
    <article class="card"><div class="card-header"><div><p class="eyebrow">For this role</p><h2>Next steps</h2></div></div><div class="card-body">${recommendations().map((item)=>`<div class="recommendation"><strong>${escapeHtml(item[0])}</strong><p>${escapeHtml(item[1])}</p></div>`).join("")}</div></article>
    <article class="card"><div class="card-header"><div><p class="eyebrow">Visibility</p><h2>Approved guest experience</h2></div></div><div class="card-body"><p>Only approved story, schedule, guide, playlist, announcement, and gallery content appears in guest roles.</p><div class="privacy-note">Private measurements, budgets, contracts, notes, and unmoderated media never appear here.</div></div></article>
  </div>`;
}

function recommendations() {
  if (["guest_viewer","signed_out"].includes(state.role)) return [["Review the weekend","Open Schedule & Timeline and Travel & Hotel."],["Explore the destination","Use the curated local guide—no location access is requested."],["Celebrate with us","Open approved playlists in your preferred provider."]];
  if (state.role === "guest_participant") return [["Confirm your details","Use your secure invitation to update RSVP and party needs."],["Share memories","Upload media for moderation; publication requires approval."],["Check for updates","Review announcements and schedule changes."]];
  if (state.role === "platform_owner") return [["Protect client boundaries","Support access must be explicitly authorized and audited."],["Review planner licensing","Pricing and capacity remain TBD."],["Maintain templates","Reusable assets must contain no personal wedding data."]];
  const items = [["Review pending media","Moderate uploads before publication."],["Confirm wedding-party timing","Collect rehearsal and call-time acknowledgements."],["Check accessibility needs","Resolve guest accommodations privately."]];
  return modulesFor().includes("tasks") ? items : items.filter((item)=>!item[0].includes("timing"));
}

function collectionPage(collection, compact = false) {
  const definition = COLLECTIONS[collection];
  if (!definition) return `<div class="empty-state">This module has no configured collection.</div>`;
  const allRows = activeEngagement().records[collection] || [];
  const rows = visibleRows(collection, allRows.filter((row) => !row.archived));
  const archived = allRows.filter((row) => row.archived);
  const writable = canWrite(collection);
  const consent = definition.consent ? `<div class="consent-note">Upload only with the participant’s knowledge and permission. Fitting media remains private unless separately approved for publication.</div>` : "";
  return `<section class="collection-section${compact ? " compact" : ""}" data-collection="${collection}">
    <div class="section-toolbar"><div><p class="eyebrow">${definition.private ? "Private by default" : "Engagement scoped"}</p><h2>${escapeHtml(definition.title)}</h2></div><div class="toolbar-actions">
      <label class="search-box">Search<input type="search" data-search="${collection}" placeholder="Search records"></label>
      <select data-sort="${collection}" aria-label="Sort ${escapeHtml(definition.title)}"><option value="updated">Recently updated</option><option value="title">Name or title</option></select>
      ${writable ? `<button class="button primary" type="button" data-add="${collection}">Add record</button>` : ""}
      ${ADMIN_ROLES.has(state.role) ? `<button class="button ghost" type="button" data-import="${collection}">Import</button><input class="visually-hidden" type="file" accept=".json,.csv" data-import-file="${collection}">` : ""}
      <button class="button ghost" type="button" data-export="${collection}">Export</button>
    </div></div>${consent}${collection==="feedback"?`<div class="consent-note">Feedback is stored only after governed submission. <a href="https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(config.supportEmail)}" target="_blank" rel="noopener noreferrer">Open Gmail compose</a> or <button class="text-button" type="button" data-copy-support>copy the support address</button>.</div>`:""}<div class="record-list" data-list="${collection}">${renderRows(collection, rows)}</div>
    ${archived.length ? `<details class="archive-drawer"><summary>Archived records (${archived.length})</summary><div class="record-list">${renderRows(collection, archived, true)}</div></details>` : ""}
  </section>`;
}

function visibleRows(collection, rows) {
  if (!["guest_viewer", "guest_participant", "signed_out"].includes(state.role)) return rows;
  if (collection === "media") return rows.filter((row) => row.moderation_status === "approved" && row.visibility === "public");
  if (collection === "story") return rows.filter((row) => row.status === "published" && row.visibility === "public");
  if (collection === "communications") return rows.filter((row) => row.status === "sent" && row.audience === "all_guests");
  if (collection === "events") return rows.filter((row) => row.audience === "all_guests");
  if (collection === "guide" || collection === "faqs") return rows.filter((row) => row.visibility === "public");
  return rows;
}

function renderRows(collection, rows, archived = false) {
  if (!rows.length) return `<div class="empty-state">No ${archived ? "archived " : ""}${escapeHtml(COLLECTIONS[collection].title.toLowerCase())}. Use the available action to add one.</div>`;
  return rows.map((row) => {
    const title = row.title || row.name || row.item || row.question || row.participant || "Record";
    const details = Object.entries(row).filter(([key, value]) => !["id","activity","archived","created_at","updated_at","private_notes","notes_private"].includes(key) && value !== "" && value != null).slice(1, 5);
    const actions = [];
    if (!archived && canWrite(collection)) actions.push(`<button class="text-button" data-edit="${collection}" data-id="${row.id}">Edit</button>`);
    if (!archived && canArchive(collection)) actions.push(`<button class="text-button" data-archive="${collection}" data-id="${row.id}">Archive</button>`);
    if (archived && canArchive(collection)) actions.push(`<button class="text-button" data-restore="${collection}" data-id="${row.id}">Restore</button>`);
    if (archived && state.role === "couple_owner") actions.push(`<button class="text-button danger-text" data-delete="${collection}" data-id="${row.id}">Delete</button>`);
    return `<article class="record-card" data-search-text="${escapeHtml(JSON.stringify(row).toLowerCase())}"><div class="record-icon" aria-hidden="true">${COLLECTIONS[collection].icon}</div><div class="record-main"><div class="record-title"><strong>${escapeHtml(title)}</strong>${row.status ? `<span class="mini-pill">${escapeHtml(String(row.status).replaceAll("_"," "))}</span>` : ""}${row.visibility ? `<span class="mini-pill privacy">${escapeHtml(row.visibility)}</span>` : ""}</div><div class="record-meta">${details.map(([key,value])=>renderDetail(key,value)).join("")}</div></div><div class="record-actions">${actions.join("")}</div></article>`;
  }).join("");
}

function formatValue(key, value) {
  if (key.includes("amount") || key === "deposit") return toMoney(value);
  return String(value).replaceAll("_", " ");
}

function renderDetail(key, value) {
  const label=escapeHtml(key.replaceAll("_"," "));
  if(key.endsWith("url")||key==="website"){
    const url=safeExternalUrl(value,"https");
    return url?`<span><b>${label}:</b> <a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">Open provider</a></span>`:"";
  }
  return `<span><b>${label}:</b> ${escapeHtml(formatValue(key,value))}</span>`;
}

function guestSelfServiceTemplate() {
  const participant = state.role === "guest_participant";
  return `<div class="content-grid two"><article class="card"><div class="card-header"><div><p class="eyebrow">Invitation privacy</p><h2>${participant ? "Your RSVP & party" : "Guest participation"}</h2></div></div><div class="card-body">${participant ? `<form id="rsvp-form" class="form-grid"><label>RSVP<select name="rsvp"><option>confirmed</option><option>declined</option></select></label><label>Party size<input name="party_size" type="number" min="1" max="20" value="2"></label><label>Dietary needs<textarea name="dietary"></textarea></label><label>Accessibility needs<textarea name="accessibility"></textarea></label><button class="button primary" type="submit">Save my details</button></form>` : `<p>Open a secure invitation token to submit RSVP, party, dietary, accessibility, guestbook, and media details. Guest records are never publicly listed.</p><button class="button primary" type="button" data-open-auth>Open invitation</button>`}</div></article><article class="card"><div class="card-header"><div><p class="eyebrow">Data boundary</p><h2>What you can see</h2></div></div><div class="card-body"><p>Your invitation can expose only your party record and content intentionally approved for guests. It cannot search other guests or engagements.</p></div></article></div>`;
}

function settingsTemplate() {
  const engagement = activeEngagement();
  const canConfigure = ADMIN_ROLES.has(state.role);
  return `<div class="content-grid two"><article class="card"><div class="card-header"><div><p class="eyebrow">Experience configuration</p><h2>Mode & theme</h2></div></div><div class="card-body form-grid"><label>Product mode<select id="product-mode" ${canConfigure ? "" : "disabled"}>${Object.entries(MODES).map(([key,val])=>`<option value="${key}" ${key===engagement.mode?"selected":""}>${val.label}</option>`).join("")}</select></label><label>Theme<select id="theme-select" ${canConfigure ? "" : "disabled"}><option value="refined-dark" ${engagement.theme==="refined-dark"?"selected":""}>Refined Dark</option><option value="romantic-light" ${engagement.theme==="romantic-light"?"selected":""}>Romantic Light</option><option value="coastal-celebration" ${engagement.theme==="coastal-celebration"?"selected":""}>Coastal Celebration</option></select></label><p class="helper">Disabled modules disappear from navigation, dashboard cards, and assistant recommendations while their data and code remain preserved.</p></div></article>
  <article class="card"><div class="card-header"><div><p class="eyebrow">Active administrators</p><h2>Access & revocation</h2></div></div><div class="card-body">${engagement.administrators.map((name)=>`<div class="access-row"><span>${escapeHtml(name)}</span><span class="mini-pill">active</span></div>`).join("")}<p class="helper">Couple owners retain engagement authority. Platform ownership does not grant automatic access to private wedding content.</p></div></article>
  <article class="card"><div class="card-header"><div><p class="eyebrow">Account</p><h2>Session controls</h2></div></div><div class="card-body"><button class="button secondary" type="button" data-open-auth>Sign In & Access</button><p class="helper">Password reset, invitation expiry, sign out, and account status are available in the governed access dialog.</p></div></article>
  <article class="card"><div class="card-header"><div><p class="eyebrow">Audit</p><h2>Recent activity</h2></div></div><div class="card-body"><div class="activity-item"><strong>Review workspace opened</strong><span>${new Date().toLocaleString()}</span></div><div class="activity-item"><strong>Engagement boundary active</strong><span>${escapeHtml(engagement.id)}</span></div></div></article></div>`;
}

function helpTemplate() {
  return `<div class="help-grid">${[["What this section does",pageSummary(state.page)],["Who can see this","Navigation is computed from the current role and product mode. Database RLS remains the controlling live boundary."],["Recommended workflow","Configure the engagement, invite couple owners, assign roles, select the product mode, then publish only approved guest content."],["Common mistakes","Do not share accounts, copy client data into templates, publish fitting media, expose private links, or use one wedding’s records in another workspace."],["Admin guide","Create engagement; invite owners; assign roles; manage guests and wedding party; tasks; measurements; fittings; rehearsal; schedule; vendors; budget; media; communications; import/export; security; privacy; archive."]].map(([title,body])=>`<article class="card"><div class="card-body"><h2>${title}</h2><p>${body}</p></div></article>`).join("")}</div>`;
}

function platformTemplate() {
  return `<div class="content-grid three">${[["Planner approvals","Approve planner accounts without inheriting access to client content."],["Reusable templates","Tasks, checklists, vendor categories, timelines, notices, FAQs, onboarding, and workflows only."],["Founding Planner Partner License","Lifetime fee: TBD · active engagement limit: TBD · storage limit: TBD · support scope: TBD."],["License boundaries","Nontransferable; no sublicensing, account sharing, cross-client data use, resale, or proprietary implementation copying."],["Support & audit","Authorized operational support is time-bound and must create an engagement-specific audit record."],["Product life","Definition: TBD. Third-party costs excluded. Misuse or security violations may result in suspension."]].map(([title,body])=>`<article class="card"><div class="card-body"><h2>${title}</h2><p>${body}</p></div></article>`).join("")}</div>`;
}

function bindPageControls() {
  document.querySelectorAll("[data-add]").forEach((button)=>button.addEventListener("click",()=>openRecordDialog(button.dataset.add)));
  document.querySelectorAll("[data-edit]").forEach((button)=>button.addEventListener("click",()=>openRecordDialog(button.dataset.edit, button.dataset.id)));
  document.querySelectorAll("[data-archive]").forEach((button)=>button.addEventListener("click",()=>archiveRecord(button.dataset.archive,button.dataset.id,true)));
  document.querySelectorAll("[data-restore]").forEach((button)=>button.addEventListener("click",()=>archiveRecord(button.dataset.restore,button.dataset.id,false)));
  document.querySelectorAll("[data-delete]").forEach((button)=>button.addEventListener("click",()=>confirmDelete(button.dataset.delete,button.dataset.id)));
  document.querySelectorAll("[data-search]").forEach((input)=>input.addEventListener("input",()=>filterRows(input.dataset.search,input.value)));
  document.querySelectorAll("[data-sort]").forEach((select)=>select.addEventListener("change",()=>sortRows(select.dataset.sort,select.value)));
  document.querySelectorAll("[data-export]").forEach((button)=>button.addEventListener("click",()=>exportCollection(button.dataset.export)));
  document.querySelectorAll("[data-import]").forEach((button)=>button.addEventListener("click",()=>document.querySelector(`[data-import-file="${button.dataset.import}"]`).click()));
  document.querySelectorAll("[data-import-file]").forEach((input)=>input.addEventListener("change",()=>importCollection(input.dataset.importFile,input.files[0])));
  document.querySelectorAll("[data-open-auth]").forEach((button)=>button.addEventListener("click",()=>$("auth-dialog").showModal()));
  document.querySelectorAll("[data-copy-support]").forEach((button)=>button.addEventListener("click",async()=>{await navigator.clipboard.writeText(config.supportEmail);setStatus("Support email copied to the clipboard.","success");}));
  $("product-mode")?.addEventListener("change", (event)=>{ activeEngagement().mode=event.target.value; state.page="dashboard"; persist(); render(); setStatus("Product mode updated; disabled module data was preserved.","success"); });
  $("theme-select")?.addEventListener("change", (event)=>{ activeEngagement().theme=event.target.value; persist(); render(); setStatus("Theme updated for this engagement.","success"); });
  $("rsvp-form")?.addEventListener("submit",(event)=>{event.preventDefault();setStatus("Review fixture RSVP updated for this invitation only.","success");});
}

function openRecordDialog(collection, id = null) {
  const definition = COLLECTIONS[collection];
  const record = id ? activeEngagement().records[collection].find((item)=>item.id===id) : null;
  dialogContext = { collection, id };
  $("record-dialog-title").textContent = `${record ? "Edit" : "Add"} ${definition.title}`;
  const fields = $("record-fields");
  fields.replaceChildren();
  for (const [key, field] of Object.entries(definition.fields)) {
    const label = document.createElement("label");
    label.textContent = field.label;
    let input;
    if (field.type === "select") {
      input = document.createElement("select");
      for (const optionValue of field.options) { const option=document.createElement("option"); option.value=optionValue; option.textContent=optionValue.replaceAll("_"," "); input.append(option); }
    } else if (field.type === "textarea") input = document.createElement("textarea");
    else { input=document.createElement("input"); input.type=field.type || "text"; }
    input.name = key; input.required = Boolean(field.required); input.maxLength = field.type === "textarea" ? 5000 : 500;
    if (field.min != null) input.min=field.min; if (field.max != null) input.max=field.max; if (field.step) input.step=field.step;
    if (record?.[key] != null) input.value=record[key];
    label.append(input); fields.append(label);
  }
  $("record-dialog").showModal();
}

async function saveDialogRecord() {
  if (!dialogContext) return;
  const form = $("record-form");
  if (!form.reportValidity()) return;
  const {collection,id}=dialogContext;
  const values = Object.fromEntries(new FormData(form).entries());
  for (const [key, field] of Object.entries(COLLECTIONS[collection].fields)) {
    if (field.type === "url" && values[key] && !safeExternalUrl(values[key], "https")) return setStatus(`${field.label} must be a safe HTTPS URL.`, "error");
  }
  for (const [key,field] of Object.entries(COLLECTIONS[collection].fields)) if (field.type === "number") values[key]=Number(values[key]||0);
  if (collection === "feedback") {
    $("record-dialog").close();
    await submitFeedbackFixtureOrLive(values);
    return;
  }
  let liveRecordId = null;
  if (liveUser) {
    const result = await performLiveAction("upsert", { collection, id, values });
    if (!result.ok) return setStatus(`Live save failed: ${result.error}`, "error");
    liveRecordId = result.data?.id || null;
  }
  const records=activeEngagement().records[collection];
  if (id) {
    const record=records.find((item)=>item.id===id); Object.assign(record,values,{updated_at:now()}); record.activity.push({at:now(),action:"updated",by:ROLE_LABELS[state.role]});
  } else records.unshift({id:liveRecordId||crypto.randomUUID(),archived:false,created_at:now(),updated_at:now(),activity:[{at:now(),action:"created",by:ROLE_LABELS[state.role]}],...values});
  persist(); $("record-dialog").close(); renderPage(); setStatus(`${COLLECTIONS[collection].title} saved in ${activeEngagement().name}.`,"success");
}

async function performLiveAction(action, payload) {
  if (!supabase || !liveUser) return { ok: false, error: "No authenticated session" };
  const { data, error } = await supabase.rpc(config.recordActionRpc, { p_action: action, p_payload: { ...payload, product_instance_id: state.activeEngagementId } });
  return error ? { ok: false, error: error.message } : { ok: true, data };
}

async function archiveRecord(collection,id,archived) {
  const record=activeEngagement().records[collection].find((item)=>item.id===id); if(!record)return;
  if(liveUser){const result=await performLiveAction(archived?"archive":"restore",{collection,id});if(!result.ok)return setStatus(`Live ${archived?"archive":"restore"} failed: ${result.error}`,"error");}
  record.archived=archived; record.updated_at=now(); record.activity.push({at:now(),action:archived?"archived":"restored",by:ROLE_LABELS[state.role]}); persist(); renderPage(); setStatus(`Record ${archived?"archived":"restored"}.`,"success");
}

function confirmDelete(collection,id) {
  pendingConfirm=async()=>{if(liveUser){const result=await performLiveAction("delete",{collection,id});if(!result.ok)return setStatus(`Live delete failed: ${result.error}`,"error");}const rows=activeEngagement().records[collection]; const index=rows.findIndex((item)=>item.id===id); if(index>=0)rows.splice(index,1);persist();renderPage();setStatus("Archived record permanently deleted by the couple owner.","success");};
  $("confirm-message").textContent="Permanently delete this archived record? This cannot be undone."; $("confirm-dialog").showModal();
}

function filterRows(collection,term) {
  const normalized=term.trim().toLowerCase(); document.querySelectorAll(`[data-collection="${collection}"] [data-search-text]`).forEach((row)=>row.hidden=normalized&&!row.dataset.searchText.includes(normalized));
}

function sortRows(collection,sort) {
  const rows=activeEngagement().records[collection]; rows.sort((a,b)=>sort==="title"?String(a.title||a.name||a.item||"").localeCompare(String(b.title||b.name||b.item||"")):String(b.updated_at).localeCompare(String(a.updated_at))); persist(); renderPage();
}

function exportCollection(collection) {
  download(`${activeEngagement().id}-${collection}.json`,JSON.stringify({engagement_id:activeEngagement().id,collection,exported_at:now(),records:activeEngagement().records[collection]},null,2),"application/json");
}

function download(name,content,type) { const blob=new Blob([content],{type}); const url=URL.createObjectURL(blob); const a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000); }

async function importCollection(collection,file) {
  if(!file)return; try { const text=await file.text(); let rows;
    if(file.name.toLowerCase().endsWith(".json")) { const parsed=JSON.parse(text); rows=Array.isArray(parsed)?parsed:parsed.records; }
    else { const lines=text.split(/\r?\n/).filter(Boolean); const headers=lines.shift().split(",").map((v)=>v.trim()); rows=lines.map((line)=>Object.fromEntries(line.split(",").map((value,index)=>[headers[index],value.trim()]))); }
    if(!Array.isArray(rows))throw new Error("No record array found"); const fields=Object.keys(COLLECTIONS[collection].fields); const valid=rows.filter((row)=>row&&typeof row==="object").map((row)=>({id:crypto.randomUUID(),archived:false,created_at:now(),updated_at:now(),activity:[{at:now(),action:"imported",by:ROLE_LABELS[state.role]}],...Object.fromEntries(fields.filter((key)=>row[key]!=null).map((key)=>[key,cleanText(row[key],5000)]))}));
    if(liveUser){for(const row of valid){const values=Object.fromEntries(fields.filter((key)=>row[key]!=null).map((key)=>[key,row[key]]));const result=await performLiveAction("upsert",{collection,values});if(!result.ok)throw new Error(result.error);row.id=result.data?.id||row.id;}}
    activeEngagement().records[collection].unshift(...valid); persist(); renderPage(); setStatus(`Import preview validated and added ${valid.length} record(s).`,"success");
  } catch(error){setStatus(`Import rejected: ${error.message}`,"error");} }

function renderReviewRoles() {
  $("review-roles").innerHTML=Object.entries(ROLE_LABELS).map(([key,label])=>`<button type="button" class="role-chip${key===state.role?" active":""}" data-role="${key}">${escapeHtml(label)}</button>`).join("");
  document.querySelectorAll("[data-role]").forEach((button)=>button.addEventListener("click",()=>{state.role=button.dataset.role;state.page="dashboard";persist();render();$("auth-dialog").close();setStatus(`${ROLE_LABELS[state.role]} review loaded. No credentials were used.`,"success");}));
}

async function initializeSupabase() {
  if (!window.supabase?.createClient) return;
  supabase=window.supabase.createClient(config.supabaseUrl,config.supabasePublishableKey,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});
  const {data}=await supabase.auth.getSession(); if(data.session) await applyLiveSession(data.session);
  supabase.auth.onAuthStateChange((_event,session)=>setTimeout(()=>applyLiveSession(session),0));
}

async function applyLiveSession(session) {
  liveUser=session?.user||null; if(!liveUser){$("auth-status").textContent="Not signed in. Guest-approved content remains reviewable.";return;}
  $("auth-status").textContent=`Signed in as ${liveUser.email}. Loading governed membership…`;
  const {data,error}=await supabase.rpc(config.engagementsRpc);
  if(error){$("auth-status").textContent=`Signed in, but Vow & Go memberships could not load: ${error.message}`;return;}
  if(!Array.isArray(data)||!data.length){
    const {data:platform}=await supabase.rpc(config.platformContextRpc);
    state.role=platform?.is_platform_owner?"platform_owner":"signed_out";render();
    $("auth-status").textContent=platform?.is_platform_owner?"Signed in as Platform Owner. Private engagement access remains off by default.":"Signed in, but no active Vow & Go engagement is assigned to this account.";return;
  }
  const mapping={owner:"couple_owner",couple_admin:"couple_collaborator",planner:"planner",contributor:"trusted_contributor",viewer:"guest_viewer",guest_participant:"guest_participant"};
  const emptyRecords=()=>Object.fromEntries(Object.keys(COLLECTIONS).map((key)=>[key,[]]));
  state.engagements=data.map((item)=>({id:item.product_instance_id,name:item.title,couple:item.title,weddingDate:"2027-06-12",mode:item.product_mode||"experience_only",theme:String(item.planner_theme||"refined_dark").replaceAll("_","-"),tagline:"A governed Vow & Go wedding workspace",modules:{},administrators:[],dbRole:item.role,records:emptyRecords()}));
  if(!state.engagements.some((item)=>item.id===state.activeEngagementId))state.activeEngagementId=state.engagements[0].id;
  state.role=mapping[activeEngagement().dbRole]||"signed_out"; await loadLiveEngagement(state.activeEngagementId); persist(); render(); $("auth-status").textContent=`Signed in as ${liveUser.email} with ${ROLE_LABELS[state.role]} access.`;
}

async function loadLiveEngagement(productInstanceId) {
  const engagement=state.engagements.find((item)=>item.id===productInstanceId); if(!engagement||!supabase)return;
  const {data,error}=await supabase.rpc(config.engagementContextRpc,{p_product_instance_id:productInstanceId});
  if(error){setStatus(`Engagement data could not load: ${error.message}`,"error");return;}
  const rows=Array.isArray(data?.records)?data.records:[];
  for(const key of Object.keys(engagement.records))engagement.records[key]=[];
  for(const row of rows){if(!engagement.records[row.collection])continue;engagement.records[row.collection].push({id:row.id,archived:Boolean(row.archived_at),created_at:row.created_at,updated_at:row.updated_at,activity:[],...row.record_data});}
  engagement.mode=data?.settings?.product_mode||engagement.mode;
  state.role=({owner:"couple_owner",couple_admin:"couple_collaborator",planner:"planner",contributor:"trusted_contributor",viewer:"guest_viewer",guest_participant:"guest_participant"})[data?.membership?.role]||state.role;
}

async function signIn() {
  if(!supabase)return setStatus("Supabase client is unavailable.","error"); const email=$("auth-email").value.trim(); const password=$("auth-password").value;
  if(!email||!password)return setStatus("Email and password are required.","error"); $("auth-signin").disabled=true;
  const {error}=await supabase.auth.signInWithPassword({email,password}); $("auth-signin").disabled=false; if(error)setStatus(`Sign in failed: ${error.message}`,"error"); else {setStatus("Signed in securely.","success");$("auth-dialog").close();}
}

async function resetPassword() {
  const email=$("auth-email").value.trim(); if(!email)return setStatus("Enter your email before requesting a reset.","error");
  const {error}=await supabase.auth.resetPasswordForEmail(email,{redirectTo:location.origin+location.pathname}); setStatus(error?`Reset request failed: ${error.message}`:"Password reset instructions requested. Check the account inbox.",error?"error":"success");
}

async function signOut() { if(supabase)await supabase.auth.signOut();liveUser=null;state.role="signed_out";state.page="dashboard";persist();render();$("auth-dialog").close();setStatus("Signed out safely.","success"); }

function openToken() {
  const token=$("invitation-token").value.trim(); if(token.length<12)return setStatus("Enter a valid invitation token.","error");
  state.role="guest_participant";state.page="dashboard";persist();render();$("auth-dialog").close();setStatus("Secure invitation review opened. The fixture is scoped to one guest party.","success");
}

async function submitFeedbackFixtureOrLive(record) {
  if(!liveUser||!supabase){ setStatus("Preview mode: your feedback was not submitted or stored.","neutral"); return; }
  const {data,error}=await supabase.functions.invoke(config.feedbackFunction,{body:{...record,product_instance_id:state.activeEngagementId,page_context:location.href}});
  if(!error&&data?.confirmation_id){setStatus(`Feedback submitted successfully. Confirmation: ${data.confirmation_id}`,"success");return;}
  const subject=encodeURIComponent(`[Vow & Go] ${record.subject}`); const body=encodeURIComponent(`${record.details}\n\nType: ${record.type}\nSeverity: ${record.severity}`); const gmail=`https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(config.supportEmail)}&su=${subject}&body=${body}`;
  setStatus(`Feedback could not be delivered securely${error?`: ${error.message}`:""}. Gmail compose and copy fallback are available.`,"error"); window.open(gmail,"_blank","noopener,noreferrer");
}

function render() {
  renderEngagementSelector();renderNavigation();renderHeader();renderPage();renderReviewRoles();syncUrl();
}

function bindShell() {
  $("primary-nav").addEventListener("click",(event)=>{const button=event.target.closest("[data-page]");if(!button)return;state.page=button.dataset.page;persist();render();$("main-content").focus();window.scrollTo({top:0,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});});
  $("engagement-select").addEventListener("change",async(event)=>{state.activeEngagementId=event.target.value;state.page="dashboard";if(liveUser)await loadLiveEngagement(state.activeEngagementId);persist();render();setStatus(`Workspace changed to ${activeEngagement().name}. Queries and records are engagement scoped.`,"success");});
  $("mobile-menu").addEventListener("click",()=>{const open=$("primary-nav").classList.toggle("open");$("mobile-menu").setAttribute("aria-expanded",String(open));$("mobile-menu").textContent=open?"Close navigation":"Open navigation";});
  $("help-button").addEventListener("click",()=>{state.page="help";persist();render();}); $("auth-open").addEventListener("click",()=>$("auth-dialog").showModal());
  $("quick-export").addEventListener("click",()=>download(`${activeEngagement().id}-review.json`,JSON.stringify({exported_at:now(),engagement:activeEngagement(),role:state.role},null,2),"application/json"));
  $("record-save").addEventListener("click",async(event)=>{event.preventDefault();await saveDialogRecord();});
  $("auth-signin").addEventListener("click",signIn);$("auth-reset").addEventListener("click",resetPassword);$("auth-signout").addEventListener("click",signOut);$("token-open").addEventListener("click",openToken);
  $("confirm-dialog").addEventListener("close",()=>{if($("confirm-dialog").returnValue==="confirm"&&pendingConfirm)pendingConfirm();pendingConfirm=null;});
}

async function boot() { applyUrlState();bindShell();render();await initializeSupabase();setStatus("Vow & Go review loaded. Role and mode controls use engagement-isolated fixtures until governed sign-in.","success"); }
boot().catch((error)=>{console.error(error);setStatus(`Application failed to initialize: ${error.message}`,"error");});
