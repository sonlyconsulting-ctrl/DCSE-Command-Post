export const TITLES = Object.freeze({
  dashboard: "Dashboard", story: "Our Story", media: "Media & Gallery Portal",
  tasks: "Wedding Tasks & Checklist", vendors: "Vendors & Contracts", budget: "Budget & Payments",
  guests: "Guests & Wedding Party", party: "Wedding Party Hub", schedule: "Schedule & Timeline",
  travel: "Travel & Hotel", guide: "Destination & Local Guide", music: "Music & Playlists",
  communications: "Communications & Notifications", help: "Help & Guidance",
  settings: "Settings & Access", feedback: "Feedback & Support", platform: "Platform Console"
});

export const ROLE_LABELS = Object.freeze({
  platform_owner: "Platform Owner", planner: "Planner / Command Center Admin", couple_owner: "Couple Owner",
  couple_collaborator: "Couple Collaborator", guest_viewer: "Guest Viewer", guest_participant: "Guest Participant",
  trusted_contributor: "Trusted Contributor", signed_out: "Signed-Out User"
});

export const MODES = Object.freeze({
  experience_only: { label: "Experience Only", modules: ["dashboard","story","media","guests","schedule","travel","guide","music","communications","help","settings","feedback"] },
  coordination: { label: "Coordination", modules: ["dashboard","story","media","tasks","vendors","guests","party","schedule","travel","guide","music","communications","help","settings","feedback"] },
  full_command_center: { label: "Full Command Center", modules: Object.keys(TITLES).filter((key) => key !== "platform") }
});

export const ROLE_MODULES = Object.freeze({
  platform_owner: ["platform","help","feedback","settings"],
  planner: Object.keys(TITLES).filter((key) => key !== "platform"),
  couple_owner: ["dashboard","story","media","tasks","budget","guests","party","schedule","travel","guide","music","communications","help","settings","feedback"],
  couple_collaborator: ["dashboard","story","media","tasks","guests","party","schedule","travel","guide","music","communications","help","feedback"],
  guest_viewer: ["dashboard","story","media","schedule","travel","guide","music","communications","help","feedback"],
  guest_participant: ["dashboard","story","media","guests","schedule","travel","guide","music","communications","help","feedback"],
  trusted_contributor: ["dashboard","story","media","tasks","party","schedule","communications","help","feedback"],
  signed_out: ["dashboard","story","media","schedule","travel","guide","music","communications","help","feedback"]
});

export const WRITE_ROLES = new Set(["planner","couple_owner","couple_collaborator","trusted_contributor","guest_participant"]);
export const ADMIN_ROLES = new Set(["planner","couple_owner"]);

const text = (label, required = false, extra = {}) => ({ type: "text", label, required, ...extra });
const select = (label, options, extra = {}) => ({ type: "select", label, options, ...extra });
const date = (label, extra = {}) => ({ type: "date", label, ...extra });
const area = (label, extra = {}) => ({ type: "textarea", label, ...extra });
const money = (label) => ({ type: "number", label, min: 0, step: ".01" });

export const COLLECTIONS = Object.freeze({
  tasks: { title: "Tasks", icon: "✓", fields: {
    title: text("Task", true), group: select("Select Task", ["Travel","Hotel","Logistics","Bride","Groom","Ceremony","Reception","Guests","Wedding Party","Vendors","Media","Music","Legal","Accessibility","Honeymoon","Attire","Measurements","Fittings","Rehearsal","Rehearsal Dinner","Wedding Day"]),
    status: select("Status", ["open","in_progress","blocked","completed","reopened","cancelled"]), assigned_to: text("Assigned person"), due_date: date("Due date"), blocked_reason: area("Blocked or cancellation reason")
  }},
  vendors: { title: "Vendors & Contracts", icon: "◇", fields: { name: text("Vendor", true), category: text("Category", true), status: select("Status", ["researching","shortlisted","selected","contracted","paid","completed","cancelled"]), contact: text("Contact"), quoted_amount: money("Quoted amount"), website: {type:"url",label:"Website"}, notes: area("Contract and notes") }},
  budget: { title: "Budget Items", icon: "$", fields: { category: text("Category", true), item: text("Item", true), description: area("Description"), estimated_amount: money("Estimated amount"), quoted_amount: money("Quoted amount"), committed_amount: money("Committed amount"), deposit: money("Deposit"), amount_paid: money("Amount paid"), due_date: date("Due date"), payment_status: select("Payment status", ["planned","quoted","committed","partially_paid","paid","overdue","cancelled"]), payment_method: text("Payment method"), notes: area("Notes") }},
  guests: { title: "Guests & Wedding Party", icon: "♧", fields: { name: text("Name", true), email: {type:"email",label:"Email"}, phone: {type:"tel",label:"Phone"}, party_size: {type:"number",label:"Party size",min:1,max:20}, rsvp: select("RSVP", ["pending","confirmed","declined","waitlisted"]), guest_category: text("Guest category"), wedding_party_role: text("Wedding-party role"), dietary_needs: area("Dietary needs"), accessibility_needs: area("Accessibility needs"), travel_status: text("Travel status"), hotel_status: text("Hotel status"), invitation_status: select("Invitation status", ["not_sent","sent","opened","accepted","expired","revoked"]), private_notes: area("Private notes") }},
  party: { title: "Wedding Party Events", icon: "♢", fields: { title: text("Title", true), category: select("Category", ["Measurements","Fitting","Attire Ordering","Alterations","Pickup","Return","Grooming","Hair & Makeup","Travel Arrival","Hotel Arrival","Rehearsal","Rehearsal Dinner","Wedding-Day Preparation","Photography Call","Ceremony Lineup","Reception Entrance","Speech or Toast","Cleanup"]), date: date("Date"), start_time: {type:"time",label:"Start time"}, end_time: {type:"time",label:"End time"}, location: text("Location"), participants: text("Participants"), coordinator: text("Assigned coordinator"), instructions: area("Instructions"), attire: text("Attire requirements"), transportation: text("Transportation"), confirmation_status: select("Confirmation", ["pending","confirmed","declined","delayed"]), reminder: text("Reminder settings"), private_notes: area("Private notes") }},
  measurements: { title: "Measurements & Fittings", icon: "⌁", private: true, consent: true, fields: { participant: text("Participant", true), garment_type: text("Garment type"), appointment_date: date("Appointment date"), retailer: text("Retailer or tailor"), measurements_completed: select("Measurements completed", ["no","yes"]), order_placed: select("Order placed", ["no","yes"]), deposit_paid: select("Deposit paid", ["no","yes"]), fitting_completed: select("Fitting completed", ["no","yes"]), alterations_required: select("Alterations required", ["no","yes"]), final_pickup: date("Final pickup"), return_required: select("Return required", ["no","yes"]), private_notes: area("Private notes") }},
  events: { title: "Schedule & Timeline", icon: "◷", fields: { title: text("Event", true), category: text("Category"), date: date("Date"), start_time: {type:"time",label:"Start time"}, end_time: {type:"time",label:"End time"}, location: text("Location"), audience: select("Audience", ["all_guests","wedding_party","selected_people","vendors","admins"]), instructions: area("Instructions") }},
  travel: { title: "Travel & Hotel", icon: "✈", fields: { name: text("Traveler or group", true), kind: select("Type", ["flight","hotel","ground_transport","arrival","departure"]), provider: text("Provider"), confirmation: text("Confirmation reference"), arrival: {type:"datetime-local",label:"Arrival"}, status: select("Status", ["planned","booked","confirmed","changed","cancelled"]), notes: area("Notes") }},
  guide: { title: "Local Guide Entries", icon: "⌖", fields: { name: text("Name", true), category: select("Category", ["City Overview","Venue Area","Airport","Transportation","Rental Cars","Hotels","Beaches","Restaurants","Coffee","Shopping","Golf","Tennis","Pickleball","Hiking","Spas","Family Activities","Nightlife","Cultural Attractions","Emergency Care","Pharmacies","Weather Guidance","Attire Guidance","Local Customs","Time Zone"]), description: area("Description"), address: text("Address"), map_url: {type:"url",label:"Map URL"}, website: {type:"url",label:"Website"}, phone: {type:"tel",label:"Phone"}, distance_venue: text("Distance from venue"), accessibility_notes: area("Accessibility notes"), child_friendly: select("Child friendly", ["yes","no","unknown"]), recommendation: select("Recommendation", ["planner","couple","both","none"]), visibility: select("Visibility", ["public","wedding_party","admins"]) }},
  faqs: { title: "Guest FAQ", icon: "?", fields: { question: text("Question", true), answer: area("Answer", {required:true}), visibility: select("Visibility", ["public","wedding_party","admins"]) }},
  music: { title: "Music & Playlists", icon: "♫", fields: { title: text("Playlist title", true), provider: select("Provider", ["Spotify","Pandora","iHeartRadio","Apple Music","YouTube Music","YouTube","Custom Playlist","Licensed Audio"]), url: {type:"url",label:"Provider URL",required:true}, moment: select("Wedding moment", ["engagement","welcome","ceremony prelude","processional","cocktail hour","reception","first dance","parent dances","celebration","after-party","honeymoon"]), note: area("Couple or planner note") }},
  media: { title: "Media Queue", icon: "▣", fields: { title: text("Caption", true), category: text("Category"), contributor: text("Contributor"), visibility: select("Visibility", ["private","moderated","public"]), moderation_status: select("Moderation", ["pending","approved","rejected"]), media_type: select("Media type", ["photo","video"]), external_url: {type:"url",label:"External reference URL"} }},
  communications: { title: "Communications", icon: "✉", fields: { title: text("Title", true), channel: select("Channel", ["Admin Communications","Guest Announcements","Direct Messages","Notification Center"]), audience: select("Audience", ["all_guests","selected_individuals","wedding_party","bride_side","groom_side","parents","speakers","ushers","vendors","travelers","hotel_groups"]), status: select("Status", ["draft","scheduled","sent","failed"]), scheduled_for: {type:"datetime-local",label:"Scheduled for"}, message: area("Message", {required:true}) }},
  story: { title: "Story Chapters", icon: "♥", fields: { title: text("Chapter title", true), stage: select("Stage", ["proposal","engagement","planning","wedding","honeymoon","future"]), narrative: area("Story", {required:true}), status: select("Status", ["draft","approved","published","archived"]), visibility: select("Visibility", ["public","wedding_party","admins"]) }},
  feedback: { title: "Feedback", icon: "!", fields: { type: select("Type", ["bug","enhancement","question","content","privacy","other"]), severity: select("Severity", ["low","normal","high","critical"]), subject: text("Subject", true), details: area("Details", {required:true}) }}
});

const seed = (id, values) => ({ id, archived: false, created_at: "2026-07-16T12:00:00Z", updated_at: "2026-07-16T12:00:00Z", activity: [{at:"2026-07-16T12:00:00Z",action:"created",by:"Review fixture"}], ...values });

export function makeEngagement(id, name, mode = "experience_only") {
  return {
    id, name, couple: name.replace(" Wedding", ""), weddingDate: id === "hale-2028" ? "2028-02-19" : "2027-06-12",
    mode, theme: "refined-dark", tagline: "From Cabo vows to a Hawaii chapter", modules: {},
    administrators: ["Couple Owner", "Sonly Planning Studio"],
    records: {
      tasks: [seed(`${id}-task-1`, {title:"Confirm ceremony music",group:"Music",status:"in_progress",assigned_to:"Couple",due_date:"2027-04-01"})],
      vendors: [seed(`${id}-vendor-1`, {name:"Coastal Light Photography",category:"Photography",status:"contracted",quoted_amount:4200})],
      budget: [seed(`${id}-budget-1`, {category:"Media",item:"Photography",estimated_amount:4500,quoted_amount:4200,committed_amount:4200,deposit:1200,amount_paid:1200,payment_status:"partially_paid"})],
      guests: [seed(`${id}-guest-1`, {name:"Jordan Rivera",email:"jordan@example.test",party_size:2,rsvp:"confirmed",guest_category:"Friend",invitation_status:"accepted"})],
      party: [seed(`${id}-party-1`, {title:"Wedding party rehearsal",category:"Rehearsal",date:"2027-06-11",start_time:"17:00",location:"Venue lawn",participants:"Wedding party",confirmation_status:"pending"})],
      measurements: [seed(`${id}-fit-1`, {participant:"Wedding party member",garment_type:"Formal attire",appointment_date:"2027-02-10",measurements_completed:"yes",order_placed:"yes",fitting_completed:"no",private_notes:"Private review fixture"})],
      events: [seed(`${id}-event-1`, {title:"Welcome gathering",category:"welcome",date:"2027-06-11",start_time:"19:00",location:"Ocean terrace",audience:"all_guests"})],
      travel: [seed(`${id}-travel-1`, {name:"Guest hotel block",kind:"hotel",provider:"Island Harbor Hotel",status:"confirmed",notes:"Use the wedding link by May 1."})],
      guide: [seed(`${id}-guide-1`, {name:"Kahului Airport",category:"Airport",description:"Primary arrival airport for this review itinerary.",address:"1 Keolani Pl, Kahului, HI",map_url:"https://maps.google.com/?q=Kahului+Airport",distance_venue:"35 minutes",child_friendly:"yes",recommendation:"planner",visibility:"public"})],
      faqs: [seed(`${id}-faq-1`, {question:"Which airport should guests use?",answer:"Use Kahului Airport unless your itinerary says otherwise.",visibility:"public"})],
      music: [seed(`${id}-music-1`, {title:"Coastal Celebration",provider:"Spotify",url:"https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",moment:"reception",note:"Open in your existing provider account."})],
      media: [seed(`${id}-media-1`, {title:"Cabo engagement portrait",category:"engagement",contributor:"Couple",visibility:"public",moderation_status:"approved",media_type:"photo"}), seed(`${id}-media-2`, {title:"Guest upload awaiting review",category:"celebration",contributor:"Guest participant",visibility:"private",moderation_status:"pending",media_type:"video"})],
      communications: [seed(`${id}-comm-1`, {title:"Welcome to Hawaii",channel:"Guest Announcements",audience:"all_guests",status:"sent",message:"Travel details and the weekend schedule are now available."})],
      story: [seed(`${id}-story-1`, {title:"From Cabo to Hawaii",stage:"engagement",narrative:"A celebration that carries the warmth of Cabo into an island wedding chapter.",status:"published",visibility:"public"})],
      feedback: []
    }
  };
}

export const DEFAULT_STATE = {
  version: 2, activeEngagementId: "akira-connor-2027", role: "signed_out", page: "dashboard",
  engagements: [makeEngagement("akira-connor-2027", "Akira & Connor Wedding"), makeEngagement("hale-2028", "Hale Wedding", "coordination")]
};
