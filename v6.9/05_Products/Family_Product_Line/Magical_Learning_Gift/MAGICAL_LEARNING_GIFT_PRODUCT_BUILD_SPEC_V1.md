# Magical Learning Gift — Product Build Specification v1.0

**Document ID:** DCSE-FPL-MLG-BUILD-SPEC-V1.0  
**Product:** Magical Learning Gift  
**Platform Family:** DCSE Family Product Line  
**Related Control Layer:** SASH (guardian administration and child-safety layer)  
**Status:** BUILD SPECIFICATION — AUTHORIZED FOR IMPLEMENTATION, PENDING APPLICATION QA AND RELEASE APPROVAL  
**Classification:** INTERNAL BUILD AUTHORITY  
**Canonical Filename:** `MAGICAL_LEARNING_GIFT_PRODUCT_BUILD_SPEC_V1.md`  
**Target Repository Path:** `v6.9/05_Products/Family_Product_Line/Magical_Learning_Gift/`  
**Target Supabase Project:** `DCSE-Family-Product-Line`  
**Supabase Project Reference:** `ajwqmgwjtxonhkvngoca`  
**Primary Schemas:** `family_core`, `family_sash`, `family_learning`  
**Owner:** DCS Enterprise  
**Release Rule:** No production promotion by file existence, database migration, render, or preview alone.

---

## 1. Executive Product Definition

Magical Learning Gift is a guardian-controlled, child-centered digital learning experience designed to turn personalized family knowledge, foundational academics, memory, storytelling, and age-appropriate discovery into a reusable gift.

The product is not positioned as an autonomous AI tutor. It is a guided learning environment that may use recommendation logic, adaptive sequencing, narration, content selection, and friendly assistant-style presentation while retaining adult control over identity, content, difficulty, visibility, and data.

The product must feel:

- magical without becoming overstimulating;
- personal without exposing private family information;
- intelligent without pretending to exercise independent authority;
- playful without becoming a points-driven attention trap;
- structured enough to demonstrate learning value;
- simple enough for a child to use with limited reading ability;
- useful enough for a parent or guardian to monitor and extend.

The first release should operate as a configurable web application, installable as a progressive web app when practical, and usable on desktop, tablet, and mobile devices. Tablet is the primary child-use form factor.

---

## 2. Product Purpose

### 2.1 Primary Purpose

Create a personalized learning gift that helps children explore:

- letters and early literacy;
- numbers and foundational numeracy;
- shapes, colors, patterns, and visual recognition;
- family relationships and personal identity;
- memory and recall;
- stories, emotions, and social understanding;
- age-appropriate independence and confidence.

### 2.2 Secondary Purpose

Provide guardians with a private administrative environment to:

- create and manage child profiles;
- select available learning modules;
- configure difficulty and session limits;
- add family members and relationships;
- review completed activities;
- identify strengths, repetition needs, and engagement patterns;
- add approved photos, names, voice clips, or family facts;
- control retention, export, deletion, and sharing.

### 2.3 Commercial Purpose

Establish Magical Learning Gift as:

1. a direct-to-family personalized digital product;
2. a giftable product for birthdays, holidays, milestones, grandparents, and caregivers;
3. a configurable foundation for future learning packs;
4. a reusable Family Product Line platform asset;
5. a demonstration of governed personalization, child safety, and private-family application design.

---

## 3. Product Boundaries

### 3.1 Included

- Guardian-created child profiles
- Guardian-controlled family relationship content
- Six initial learning modules
- Guided activity sessions
- Progress and completion summaries
- Child-safe audio and visual feedback
- Guardian content approval
- Private media handling
- Role-scoped access
- Device-responsive application
- Reduced-motion support
- Session duration controls
- Data export and deletion requests
- Feedback and bug reporting
- Future-ready adaptive recommendation logic

### 3.2 Excluded from v1

- Open-ended child chat
- Unmoderated generative AI responses
- Behavioral diagnosis
- Medical, psychological, or developmental claims
- School grading
- Public child profiles
- Child-to-child messaging
- Public leaderboards
- Advertising
- Third-party behavioral tracking
- Facial recognition
- Voiceprint identification
- Location tracking
- Social-media sharing by children
- Autonomous purchases
- Direct child account creation without guardian authority

### 3.3 Prohibited

- Service-role credentials in client code
- Shared administrator passwords
- Public listing of private child media
- Training external models on child data without explicit lawful authorization
- Collection of unnecessary personal information
- Manipulative streaks, loss aversion, shame, or punitive engagement mechanics
- Claims of legal, educational, or accessibility compliance without formal audit

---

## 4. User and Authority Model

### 4.1 Primary Roles

| Role | Description | Core Authority |
|---|---|---|
| `guardian_owner` | Primary parent or legal guardian | Full product, membership, child, content, retention, and deletion authority |
| `guardian_admin` | Authorized secondary guardian | Manage child content, modules, sessions, and reports; no ownership transfer |
| `caregiver` | Authorized limited adult | Run approved sessions and view limited child information |
| `child_user` | Child-facing session identity | Use assigned activities; no administrative access |
| `viewer` | Read-only adult recipient, when enabled | View selected progress or gift content |
| `support_admin` | Sonly Consulting mediated support role | No standing access to child records; access only through logged, time-bound support procedure |

### 4.2 Authentication Rules

- Adults use individual Supabase Auth accounts.
- Children do not receive unrestricted email/password accounts in v1.
- Child mode is launched by an authorized guardian session.
- Child switching requires guardian confirmation or an approved device-level PIN.
- Shared passwords from prototypes are prohibited.
- Support access must be explicitly initiated, time-bound, logged, and revocable.

### 4.3 Gift Purchaser Model

The purchaser may differ from the guardian.

Required states:

1. `purchased_unclaimed`
2. `guardian_invited`
3. `guardian_claimed`
4. `child_configured`
5. `active`
6. `suspended`
7. `archived`
8. `deletion_pending`
9. `deleted`

A purchaser may enter gift details and recipient contact information but may not access a child's private activity data unless separately authorized as a guardian.

---

## 5. Age Bands and Learning Levels

The system must not assume one universal childhood level.

| Band | Working Label | Typical Range | Design Posture |
|---|---|---:|---|
| A | Explorer | 4–5 | Large targets, minimal text, narration-first, short sessions |
| B | Builder | 6–7 | Simple instructions, matching, sequencing, early reading |
| C | Pathfinder | 8–9 | Multi-step tasks, memory challenges, short explanations |
| D | Creator | 10–12 | More autonomy, reflection prompts, richer family-story tools |

Age is one input, not the sole determinant. Guardians may manually adjust the level.

The application should maintain:

- `recommended_level`
- `guardian_selected_level`
- `module_specific_level`
- `assistance_level`
- `reading_support_enabled`
- `audio_instruction_enabled`

No developmental diagnosis should be inferred from performance.

---

## 6. Initial Learning Modules

### 6.1 My Family Tree Adventure

**Category:** Family relationships and identity  
**Purpose:** Teach family roles, names, relationships, and inclusive family structures.

Core content may include:

- parent or guardian;
- sibling;
- maternal grandparent;
- paternal grandparent;
- aunt;
- uncle;
- cousin;
- caregiver;
- stepfamily;
- adoptive family;
- chosen family;
- household member.

Activities:

- Match a name to a relationship
- Build a family tree
- “Who is related to whom?”
- Photo-to-name matching
- Family story cards
- “People who care for me”
- Family celebration and tradition prompts

Guardrails:

- Guardians decide which relationships appear.
- No assumption that every family has the same structure.
- Deceased, absent, estranged, foster, adoptive, and chosen-family relationships require neutral, configurable language.
- Public sharing is disabled by default.

### 6.2 Rainbow Number Splash

**Category:** Numeracy  
**Purpose:** Number recognition, counting, comparison, sequence, and simple operations.

Activities:

- Count objects
- Match numeral to quantity
- Complete a sequence
- More, less, or equal
- Early addition and subtraction
- Pattern recognition
- Timed mode only when guardian enables it

### 6.3 Unicorn Letter Lagoon

**Category:** Literacy  
**Purpose:** Letter recognition, sound association, word beginnings, spelling, and reading confidence.

Activities:

- Uppercase/lowercase matching
- Letter sounds
- Beginning sounds
- Build a word
- Name recognition
- Family-name spelling
- Read-along cards
- Phonics progression

### 6.4 Color and Shape Garden

**Category:** Visual learning  
**Purpose:** Color, shape, size, sorting, grouping, and spatial reasoning.

Activities:

- Match colors
- Identify shapes
- Sort by size or attribute
- Complete visual patterns
- Find the different item
- Build a picture from shapes
- Accessibility mode that does not rely on color alone

### 6.5 Magical Memory Pool

**Category:** Memory and recall  
**Purpose:** Working memory, recognition, sequencing, and recall.

Activities:

- Card matching
- Remember the sequence
- What changed?
- Picture recall
- Sound recall
- Family-photo memory sets
- Adjustable item count and delay

### 6.6 Storytime Cove

**Category:** Social-emotional and narrative learning  
**Purpose:** Listening, sequencing, emotional vocabulary, comprehension, and creativity.

Activities:

- Read-along stories
- Put events in order
- Choose how a character may feel
- Predict what happens next
- Retell the story
- Build a simple story
- Guardian-recorded family stories
- Calm-down and reflection stories

---

## 7. Future Module Framework

All modules must use a reusable content contract.

Minimum module metadata:

```yaml
module_key:
title:
category:
age_band_min:
age_band_max:
difficulty_min:
difficulty_max:
instruction_mode:
estimated_minutes:
skills:
required_assets:
accessibility_support:
guardian_configurable:
content_version:
release_status:
```

Future module candidates:

- Nature Discovery Trail
- Everyday Money Garden
- Music and Rhythm Harbor
- Healthy Habits Quest
- Culture and Heritage Journey
- Safety and Community Helpers
- Introductory Coding Patterns
- Travel and Geography Adventure
- Family Recipe Math
- Grandparent Story Archive

No future module becomes available merely because content exists. It must pass content, safety, accessibility, privacy, and release review.

---

## 8. Experience Architecture

### 8.1 Public/Gift Entry

Routes:

- `/`
- `/gift`
- `/claim`
- `/guardian-invite`
- `/privacy`
- `/support`

The public surface must not display real child information.

### 8.2 Guardian Application

Routes:

- `/guardian/dashboard`
- `/guardian/children`
- `/guardian/children/:childId`
- `/guardian/modules`
- `/guardian/content`
- `/guardian/family-tree`
- `/guardian/progress`
- `/guardian/reports`
- `/guardian/session-controls`
- `/guardian/media`
- `/guardian/access`
- `/guardian/privacy`
- `/guardian/export`
- `/guardian/feedback`
- `/guardian/settings`

### 8.3 Child Experience

Routes or controlled views:

- `/play`
- `/play/home`
- `/play/module/:moduleKey`
- `/play/activity/:activityId`
- `/play/celebrate`
- `/play/pause`
- `/play/goodbye`

The child experience must remove administrative navigation and external links.

### 8.4 Support and Audit Surface

Internal-only:

- Product instance status
- Migration version
- RLS test status
- Storage policy status
- Content pack version
- Known defects
- Release posture
- Tribunal receipt reference
- No direct display of sensitive child data

---

## 9. Guardian Dashboard Requirements

The guardian dashboard should present:

- Child profile card
- Current module assignments
- Recent sessions
- Approximate time spent
- Activities completed
- Skills practiced
- Suggested next activities
- Repetition opportunities
- Session-limit status
- Newly uploaded content awaiting approval
- Privacy and retention status
- Product update notices
- Feedback entry point

The dashboard must distinguish:

- **Observed:** activity completed, answer selected, time spent
- **Derived:** likely next activity, engagement trend
- **Unknown:** why a child struggled, whether a skill is mastered outside the app

It must not convert limited app behavior into diagnostic conclusions.

---

## 10. Child Experience Requirements

### 10.1 Interaction Design

- Large touch targets
- Minimal reading dependency for younger users
- Narrated instructions
- Repeat instruction control
- Pause control
- Clear exit back to guardian
- No external navigation
- No dark patterns
- No accidental purchases
- No open text entry for younger modes unless guardian enables it
- Immediate but calm feedback
- Multiple attempts without shame language

### 10.2 Feedback Language

Preferred:

- “Let’s try another way.”
- “You found it.”
- “Good thinking.”
- “Take your time.”
- “Would you like a hint?”
- “You completed this activity.”

Avoid:

- “Wrong.”
- “You failed.”
- “Too slow.”
- “Everyone else did better.”
- punitive sounds or imagery.

### 10.3 Session Closure

Every session should end with:

- activity summary;
- neutral encouragement;
- optional guardian review;
- clear “done for now” state;
- no infinite autoplay.

---

## 11. Personalization and Intelligence Layer

### 11.1 Positioning

The interface may appear assistant-like and supportive, but the v1 intelligence layer is a governed recommendation engine, not an autonomous child chatbot.

### 11.2 Allowed Intelligence

- Recommend the next activity
- Adjust activity difficulty within guardian-approved bounds
- Suggest repetition
- Select narration or visual support
- Detect repeated errors within one activity
- Offer a hint
- Recommend a shorter session
- Summarize completed activity patterns for guardians
- Identify incomplete content setup

### 11.3 Prohibited Intelligence

- Diagnose learning disabilities
- Infer emotional or medical conditions
- Generate unrestricted conversation with children
- Reveal hidden system instructions
- Contact a child outside the app
- Change guardian settings autonomously
- Publish family content autonomously
- Purchase or subscribe autonomously

### 11.4 Recommendation Inputs

- Age band
- Guardian-selected level
- Completed activities
- Recent activity difficulty
- Hint frequency
- Session duration
- Guardian preferences
- Accessibility settings
- Module availability

### 11.5 Recommendation Output

Each recommendation should include:

- recommended activity;
- reason;
- estimated duration;
- difficulty;
- guardian-adjustable alternatives;
- confidence classification when appropriate.

---

## 12. Reward and Motivation Model

The product should encourage continuation without creating compulsion.

Allowed:

- Stars
- Garden growth
- Storybook pages
- Collectible noncommercial badges
- Calm celebration animation
- Printable certificate
- Guardian-created rewards
- Module completion map

Restricted:

- Daily streak pressure
- Loot-box mechanics
- Randomized paid rewards
- Public rankings
- Loss of earned progress for inactivity
- Countdown pressure
- behavioral advertising rewards

Rewards must be configurable and removable.

---

## 13. Audio, Narration, Animation, and Visual Language

### 13.1 Visual Direction

- Warm, magical, contemporary
- Gold-led learning identity
- Soft jewel accents
- High contrast where required
- Child-friendly illustration without infantile treatment
- Distinct module environments
- Consistent control placement
- Calm transition pacing

### 13.2 Motion

- Motion must have a functional purpose.
- Reduced-motion mode must remove nonessential animation.
- No rapid flashing.
- No autoplay video with sound.
- Celebration sequences should be brief and skippable.

### 13.3 Audio

- Narration on/off
- Replay instruction
- Volume control
- Captions or visible text equivalent
- No surprise loud sounds
- Guardian preview before child access
- Licensed or original audio only
- No copyrighted commercial music bundled without authorization

### 13.4 Voice

The narrator should be:

- warm;
- clear;
- patient;
- inclusive;
- energetic without hype;
- free of celebrity imitation.

---

## 14. Accessibility Target

The application is **designed to target accessibility standards**.

Required design targets:

- Keyboard-operable guardian interface
- Visible focus indicators
- Logical heading order
- Semantic controls
- Text alternatives for meaningful images
- Captions/transcripts for instructional audio and video
- Reduced-motion support
- Color-independent status communication
- Minimum touch-target sizing
- Scalable text
- Screen-reader labels
- Error identification and recovery
- Time-limit controls that can be extended or disabled by guardians
- Dyslexia-friendly reading option when practical
- High-contrast option
- Narration and instruction replay

No “compliant” claim is permitted without a formal audit.

---

## 15. Privacy, Consent, and Child Safety

### 15.1 Data Minimization

Collect only data required to provide the product.

Preferred child profile fields:

- display name or nickname;
- birth year or age band;
- learning level;
- selected modules;
- avatar or guardian-approved image;
- accessibility preferences;
- guardian-authored family relationships.

Avoid collecting:

- exact address;
- exact school;
- precise location;
- unnecessary full legal name;
- biometric identifiers;
- advertising identifiers.

### 15.2 Consent

Guardian consent is required before:

- child profile activation;
- media upload;
- family-tree personalization;
- voice recording;
- progress retention;
- inviting another adult;
- export or third-party integration.

### 15.3 Privacy Defaults

- Private by default
- No public child profiles
- No searchable child records
- No public media bucket for child content
- No direct third-party analytics in child mode
- No social sharing from child mode
- No external links in child mode
- No model training permission implied

### 15.4 Legal Review Gate

Before production release, obtain a specific privacy review addressing applicable child privacy obligations, including COPPA where relevant. This specification does not constitute legal advice or a completed compliance determination.

---

## 16. Data Architecture

### 16.1 Existing Foundation

Use:

- `family_core`
- `family_sash`
- `family_learning`

Expected existing concepts:

- product instances;
- product memberships;
- child profiles;
- guardian-child access;
- learning modules;
- activity sessions;
- audit events.

### 16.2 Required Tables or Extensions

Recommended logical tables:

#### `family_sash.child_profiles`

- `id`
- `household_id`
- `display_name`
- `birth_year`
- `age_band`
- `guardian_selected_level`
- `avatar_storage_path`
- `accessibility_settings jsonb`
- `status`
- `created_by`
- `created_at`
- `updated_at`

#### `family_sash.guardian_child_access`

- `id`
- `child_id`
- `user_id`
- `relationship_label`
- `authority_level`
- `status`
- `granted_by`
- `created_at`
- `revoked_at`

#### `family_learning.learning_modules`

- `id`
- `module_key`
- `title`
- `category`
- `age_band_min`
- `age_band_max`
- `content_version`
- `release_status`
- `configuration jsonb`

#### `family_learning.module_assignments`

- `id`
- `product_instance_id`
- `child_id`
- `module_id`
- `assigned_level`
- `status`
- `assigned_by`
- `assigned_at`

#### `family_learning.activities`

- `id`
- `module_id`
- `activity_key`
- `title`
- `difficulty`
- `estimated_minutes`
- `content jsonb`
- `accessibility jsonb`
- `release_status`

#### `family_learning.activity_sessions`

- `id`
- `product_instance_id`
- `child_id`
- `module_id`
- `activity_id`
- `started_at`
- `completed_at`
- `duration_seconds`
- `assistance_used`
- `completion_status`
- `result_summary jsonb`
- `recorded_by`

#### `family_learning.progress_summaries`

- `id`
- `product_instance_id`
- `child_id`
- `module_id`
- `period_start`
- `period_end`
- `observations jsonb`
- `recommendations jsonb`
- `generated_at`

#### `family_learning.family_relationships`

- `id`
- `product_instance_id`
- `child_id`
- `display_name`
- `relationship_type`
- `branch`
- `photo_storage_path`
- `story`
- `visibility`
- `created_by`
- `created_at`

#### `family_learning.content_assets`

- `id`
- `product_instance_id`
- `child_id`
- `asset_type`
- `storage_path`
- `moderation_status`
- `approved_by`
- `created_at`

#### `family_learning.guardian_feedback`

- `id`
- `product_instance_id`
- `submitted_by`
- `feedback_type`
- `severity`
- `subject`
- `details`
- `status`
- `created_at`

#### `family_learning.consent_records`

- `id`
- `product_instance_id`
- `child_id`
- `guardian_user_id`
- `consent_type`
- `consent_version`
- `granted_at`
- `revoked_at`
- `evidence jsonb`

### 16.3 Data State Rules

All mutable records should support explicit states such as:

- draft
- pending_review
- approved
- active
- suspended
- rejected
- archived
- deletion_pending
- deleted

---

## 17. RLS and Authorization Matrix

RLS must be enabled on all user-facing tables.

### 17.1 Guardian Owner

May:

- create and manage child profiles;
- assign modules;
- view all child sessions in the product instance;
- manage family relationships;
- approve media;
- invite or revoke adults;
- export;
- initiate deletion.

### 17.2 Guardian Admin

May:

- view assigned child profiles;
- manage modules and approved content;
- view progress;
- create sessions;
- approve content when granted.

May not:

- transfer ownership;
- delete the product instance;
- authorize support access beyond assigned permissions.

### 17.3 Caregiver

May:

- view only authorized child;
- launch approved activities;
- record sessions;
- view limited activity history.

May not:

- change privacy;
- export all data;
- add guardians;
- delete records;
- access other children.

### 17.4 Child Mode

May:

- read only assigned activity content;
- create narrowly scoped session results through mediated RPC or controlled client action.

May not:

- query membership tables;
- query adult contact information;
- list storage;
- change settings;
- access another child.

### 17.5 Nonmember

Must receive no protected rows.

### 17.6 Service Role

Reserved for backend mediation, maintenance, and controlled support. Never exposed in browser code.

---

## 18. Supabase Storage Specification

Recommended buckets:

| Bucket | Access | Purpose |
|---|---|---|
| `family-learning-private` | Private | Child photos, family images, voice clips, guardian uploads |
| `family-learning-content` | Controlled read | Approved module assets |
| `family-learning-exports` | Private, short-lived | Generated guardian exports |
| `family-public-assets` | Public only for generic assets | Nonpersonal backgrounds, icons, illustrations |

Storage object path pattern:

```text
{product_instance_id}/{child_id}/{asset_type}/{uuid}-{sanitized_filename}
```

Rules:

- No broad public listing policy
- Signed URLs for private assets
- File-type validation
- Size limits
- Filename sanitization
- Malware scanning when available
- Image metadata stripping where practical
- Guardian approval before use in activities
- Deletion propagation
- Audit log for upload, approval, access, and deletion

---

## 19. API and Backend Mediation

Use public-safe Supabase credentials only in the client.

Prefer:

- carefully scoped RPC functions;
- explicit public views when necessary;
- Edge Functions for privileged operations;
- server-mediated export and deletion;
- parameterized queries;
- validation at both client and database layers.

Privileged operations include:

- invitation issuance;
- ownership transfer;
- bulk export;
- deletion workflow;
- support-access grant;
- content-pack promotion;
- email delivery containing private information.

---

## 20. Session, Screen-Time, and Wellness Controls

Guardian settings:

- default session length;
- maximum session length;
- reminder before session end;
- break interval;
- allowed modules;
- allowed days or time windows;
- audio default;
- motion level;
- difficulty cap;
- free-play enable/disable.

Child mode must:

- provide a clear ending;
- avoid guilt for stopping;
- avoid infinite content feeds;
- pause cleanly;
- preserve progress safely.

---

## 21. Progress and Reporting

Reports should emphasize activity evidence rather than diagnosis.

Guardian report categories:

- Activities completed
- Time engaged
- Accuracy where meaningful
- Hints used
- Repeated activities
- Module interests
- Recently introduced skills
- Suggested practice
- Guardian notes

Use language such as:

- “Practiced”
- “Completed”
- “Repeated”
- “Used a hint”
- “May benefit from another activity”

Avoid:

- “Mastered” unless a defined threshold exists
- “Behind”
- “Deficient”
- “Disordered”
- “Gifted”
- medical or diagnostic labels

Export formats:

- PDF summary
- CSV activity history
- JSON account export

---

## 22. Content Management and Promotion

Content lifecycle:

1. Draft
2. Internal review
3. Child-safety review
4. Accessibility review
5. Technical validation
6. Guardian-preview ready
7. Approved content pack
8. Published
9. Deprecated
10. Archived

Each content item requires:

- source;
- author or generator;
- age band;
- learning objective;
- answer logic;
- narration text;
- visual assets;
- accessibility notes;
- version;
- review status.

Generated content must not publish directly to children without review.

---

## 23. Application Technology Direction

Preferred implementation:

- TypeScript
- React or another maintainable component architecture
- Responsive CSS using Grid/Flexbox
- Supabase Auth
- Supabase PostgreSQL
- Supabase Storage
- Supabase Edge Functions where mediation is required
- PWA support where practical
- GitHub source control
- Preview-first deployment
- No secrets in client code

A standalone HTML prototype may be used for visual validation, but production should use a maintainable application structure if state, routing, testing, and authentication complexity warrants it.

---

## 24. Local and Hosted Review Requirements

The repository must include:

- `README.md`
- `REVIEW_ON_WINDOWS.md`
- `START_MAGICAL_LEARNING_GIFT.cmd`
- `START_MAGICAL_LEARNING_GIFT.ps1`
- `.env.example`
- test instructions
- migration references
- Tribunal receipt

The Windows launcher must:

- locate its own directory;
- avoid launching from `C:\Windows\System32`;
- start the development or preview server;
- choose an available port;
- open the browser;
- display actionable errors.

Hosted review must use an isolated preview URL. It must not overwrite another DCSE surface.

---

## 25. Testing Specification

### 25.1 Functional

- Guardian signup/sign-in
- Gift claim
- Child profile creation
- Module assignment
- Child-mode launch
- Activity completion
- Session persistence
- Progress reporting
- Family-tree content
- Media upload and approval
- Consent capture
- Export
- Feedback
- Logout
- Session expiration

### 25.2 Role Tests

Positive:

- guardian owner accesses own child;
- guardian admin accesses authorized child;
- caregiver launches approved activity;
- child mode reads assigned activity;
- guardian views progress.

Negative:

- unrelated guardian denied;
- caregiver denied export;
- child mode denied membership data;
- child mode denied other child;
- anonymous user denied private data;
- public user denied Storage listing;
- revoked guardian denied;
- cross-product access denied.

### 25.3 Storage Tests

- allowed type upload
- disallowed type rejection
- oversize rejection
- signed URL expiry
- no bucket listing
- deletion
- revoked access
- path traversal rejection
- filename sanitization

### 25.4 UX and Accessibility

- Mobile
- Tablet
- Laptop
- Desktop
- Keyboard
- Screen reader smoke test
- Zoom
- High contrast
- Reduced motion
- Audio off
- Captions
- Touch target sizing
- Orientation change
- Slow connection
- Offline interruption
- Empty and error states

### 25.5 Security

- XSS
- injection
- broken object-level authorization
- cross-child access
- cross-product access
- exposed secrets
- unsafe external URLs
- excessive error detail
- session fixation
- stale signed URLs
- unvalidated uploads

---

## 26. Seed Content Requirements

Seed generic, nonpersonal demo content only.

Required demo profiles:

- one guardian owner;
- one guardian admin;
- one child demo profile;
- one unrelated guardian for denial tests.

Required demo content:

- all six initial modules;
- at least three activities per module;
- multiple age/difficulty variants;
- generic family-tree placeholders;
- no real child personal data;
- no real family photos without authorization.

Seed data must be clearly marked:

- `demo`
- `fixture`
- `test_only`

Production deployment must detect and prevent accidental presentation of test content as real user data.

---

## 27. Feedback and Support

Guardian-facing feedback categories:

- Bug
- Enhancement
- Content concern
- Privacy concern
- Accessibility issue
- Billing or gift claim
- Question
- Other

Default routing:

`sonlyconsulting@gmail.com`

Feedback should:

- save to Supabase when authenticated;
- create an email or mediated notification;
- include product instance identifier, not unnecessary child details;
- avoid attaching private media automatically;
- support severity and status;
- remain auditable.

---

## 28. Analytics and Measurement

Allowed product analytics should be privacy-minimized and guardian-oriented.

Track:

- product activation;
- module starts;
- activity completion;
- session duration;
- feature errors;
- guardian configuration completion;
- content-pack usage;
- accessibility feature use in aggregate;
- support events.

Do not track:

- advertising profiles;
- cross-site behavior;
- precise location;
- unrelated browsing;
- unnecessary device fingerprinting.

Success metrics:

- Gift claim completion
- Guardian setup completion
- Child session completion
- Repeat voluntary use
- Module completion
- Guardian satisfaction
- Low support-friction rate
- Zero unauthorized data exposure
- RLS test pass rate
- Accessibility defect closure rate

---

## 29. Release Phases

### Phase 0 — Specification and Foundation

- Canonical build spec
- Schema audit
- Role matrix
- Privacy inventory
- Content inventory

### Phase 1 — Guardian MVP

- Auth
- Gift claim
- Child profile
- Module assignment
- Guardian dashboard
- Six modules with basic activities
- Session recording
- RLS
- Storage
- Feedback

### Phase 2 — Child Experience Expansion

- Narration
- richer animation
- adaptive sequencing
- rewards
- family-photo activities
- printable outputs
- PWA

### Phase 3 — Commercial Productization

- purchase flow
- gift codes
- branded gift delivery
- subscription or content packs
- customer support workflow
- retention and deletion automation
- production privacy review

### Phase 4 — Intelligence and Content Scale

- governed recommendation engine
- additional modules
- multilingual content
- guardian-authored story assistance
- vetted generative content pipeline
- content marketplace only after governance approval

---

## 30. Stop Gates

The build must stop before production when any of the following remains unresolved:

- RLS denial tests fail
- child media can be publicly listed
- service-role credentials appear in client code
- real child data is used as seed data
- guardian consent is missing
- deletion workflow is undefined
- support access is unlogged
- accessibility-critical defects remain
- child mode exposes external links
- unreviewed generated content is publishable
- private schemas are exposed without safe authorization
- legal/privacy review is incomplete for the intended release market

---

## 31. Required Repository Deliverables

```text
v6.9/05_Products/Family_Product_Line/Magical_Learning_Gift/
├── AGENTS.md
├── README.md
├── MAGICAL_LEARNING_GIFT_PRODUCT_BUILD_SPEC_V1.md
├── REVIEW_ON_WINDOWS.md
├── START_MAGICAL_LEARNING_GIFT.cmd
├── START_MAGICAL_LEARNING_GIFT.ps1
├── app/
├── public/
├── tests/
├── supabase/
│   ├── migrations/
│   ├── seed/
│   └── tests/
└── docs/
    ├── PRIVACY_DATA_MAP.md
    ├── ROLE_ACCESS_MATRIX.md
    ├── CONTENT_MANIFEST.md
    ├── ACCESSIBILITY_TEST_PLAN.md
    └── RELEASE_CHECKLIST.md
```

Tribunal receipt:

```text
_Tribunal_Inbox/TRIBUNAL_MAGICAL_LEARNING_GIFT_BUILD_<YYYYMMDD>_<AGENT>.md
```

---

## 32. Required Codex Build Instruction Summary

Codex or another implementation agent must:

1. Read this specification before editing.
2. Inspect existing `family_sash` and `family_learning` schemas.
3. Preserve existing migrations.
4. Add only versioned migrations.
5. Build the guardian and child experiences.
6. Use public-safe credentials only.
7. Implement and test RLS.
8. Create generic fixtures.
9. Produce one-click Windows review.
10. Produce isolated hosted preview.
11. Run functional, role, Storage, security, responsive, and accessibility tests.
12. Record results in Tribunal.
13. Open a pull request.
14. Do not merge or deploy publicly until the defined gates pass.

---

## 33. Definition of Done

The application is build-complete for review when:

- the guardian can claim a gift;
- create a child profile;
- assign modules;
- configure accessibility and session controls;
- launch child mode;
- complete an activity;
- view a saved session and progress summary;
- configure family relationships;
- upload and approve private media;
- invite or revoke another adult;
- export data;
- submit feedback;
- pass role and cross-product denial tests;
- pass Storage privacy tests;
- run through a one-click Windows launcher;
- load from an isolated hosted preview;
- contain no client-side secrets;
- contain no real child seed data;
- have a complete Tribunal receipt;
- remain pending formal production approval.

---

## 34. Current Authority Statement

This document authorizes implementation planning and controlled build execution for Magical Learning Gift within the DCSE Family Product Line.

It does not, by itself:

- approve public production deployment;
- establish legal compliance;
- authorize use of real child information;
- authorize model training on child data;
- promote generated content;
- replace guardian consent;
- waive security, privacy, accessibility, or Tribunal gates.
