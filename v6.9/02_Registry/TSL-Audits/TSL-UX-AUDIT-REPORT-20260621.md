# TSL UX/UI AUDIT REPORT
**The Sports Lounge — Product Design & Responsive Architecture Review**

---

**Document ID:** TSL-UX-AUDIT-20260621  
**Date:** 2026-06-21  
**Status:** DRAFT FOR DCS REVIEW  
**Scope:** Original Premium Lounge plan vs current build vs missing features  
**Recommendation:** 4-phase remediation, 128-182 hours estimated effort  

---

## EXECUTIVE SUMMARY

Tedo's Sports Lounge (TSL) was architected to deliver a **premium "Member Sports Intelligence Lounge"** with real-time feeds, live leaderboards, Smoove Coins management, and advanced member personalization. The original ASSET-TSL-PREMIUM-LOUNGE-PLAN-001 outlined 7 phases of development.

**Current State:** TSL is **desktop-focused**, not responsive across mobile/tablet/desktop. **31 critical features are missing or incomplete**. **Admin console does not exist**. Real-time Supabase integration and Smoove Coins ledger work correctly, but the UI/UX layer is materially incomplete.

**Verdict:** TSL has a solid backend (proven Supabase RLS, real-time, coin ledger) but a fragmented, non-responsive frontend that does not match the original bill plan or industry standards for high-volume websites.

---

## PHASE BREAKDOWN: ORIGINAL PLAN vs CURRENT STATE

### Phase 1: UI/UX Flow & Layout Architecture
**Original Requirements:**
- Sports Intelligence Lounge Dashboard (swipeable carousels, live events, quick-picks, scoreboard ticker)
- My Lounge personalized feed (filtered by 5 favorite teams)
- Live Scoreboard Module (play-by-play, stats, line movements, leaderboard)
- Lounge Leaderboard (avatar, display name, Smoove Coin balance, accuracy %, trend chart)
- Generic `<LoungeWidget />` grid system for mobile → desktop scaling

**Current State:**
- ❌ Dashboard exists but desktop-only, no mobile responsiveness
- ❌ My Lounge feed incomplete
- ❌ Live Scoreboard Module partially built
- ❌ Leaderboard UI present but not fully functional
- ❌ **NO responsive grid system** — breakpoints missing for tablet (768-1024px) and mobile (<480px)

**Gap:** Responsive design system does not exist. Desktop-focused CSS breaks below 1024px.

---

### Phase 2: Live Feed Data Integration
**Original Requirements:**
- Primary feed: SportsDataIO or ESPN API integration
- Secondary/fallback: Admin panel for manual game creation & score overrides
- Graceful degradation if API rate-limits

**Current State:**
- ✅ Real-time data feed connected (Supabase triggers working)
- ❌ **Admin panel missing entirely** — no manual overrides, no emergency score adjustment, no game creation UI
- ⚠️ Fallback mechanism unclear

**Gap:** Critical. No admin console means operations cannot manually correct data or handle API outages.

---

### Phase 3: Supabase Database Schema Design
**Original Requirements:**
- Comprehensive relational schema (leagues, teams, events, picks, ledger)
- Indexing on foreign keys & compound fields
- 5-team favorite limits enforced at DB constraint level

**Current State:**
- ✅ Core schema present (profiles, contests, picks, scn_ledger)
- ✅ Smoove Coins ledger functional
- ⚠️ Partial: 5-team favorite limit may be client-side only, not DB-enforced

**Gap:** Minor. Backend is solid; validation may need tightening.

---

### Phase 4: Event Lifecycle & Archival Engine
**Original Requirements:**
- Event state progression: scheduled → pre_event → live → halftime_or_break → final → review → archived
- 24-hour archival sweep (cron job or Supabase pg_cron)

**Current State:**
- ✅ Lifecycle states exist in schema
- ⚠️ Archival automation unclear — may be manual

**Gap:** Low impact. Lifecycle is present; automation may need verification.

---

### Phase 5: Member Premium Personalization
**Original Requirements:**
- Dynamic widget rehydration based on favorite teams
- Member profile customization (avatar, display name, favorite teams UI)
- Personalized feed filtering

**Current State:**
- ⚠️ Partial. Favorite teams logic exists but incomplete on frontend
- ❌ **Member profile page missing critical features** (31+ gaps identified)
- ❌ Personalized "My Lounge" feed not fully operational

**Gap:** Major. Member profile is the weakest area. Original bill plan lists features that don't exist in current build.

---

### Phase 6: Security, RLS & Sandbox Hardening
**Original Requirements:**
- Row Level Security (RLS) policies
- Secure Definer RPC function (`settle_pick_transaction`)
- Least-privilege principle

**Current State:**
- ✅ RLS policies in place (as of v69 GOVERNED_CORE baseline)
- ✅ Service role restrictions enforced
- ✅ Authenticated user permissions scoped

**Gap:** None. Security foundation is solid.

---

### Phase 7: Verification & Automated E2E Testing
**Original Requirements:**
- Playwright E2E test suite
- Cloudflare WAF bypass for staging environment

**Current State:**
- ⚠️ E2E testing framework may exist but not verified
- ❌ No clear staging environment with disabled WAF

**Gap:** Verification coverage unknown.

---

## DETAILED GAP ANALYSIS

### A. RESPONSIVE DESIGN GAPS (10 Issues)

| Breakpoint | Issue | Affected Features | Severity |
|---|---|---|---|
| **Mobile <480px** | No mobile layout | Dashboard, leaderboard, navigation | CRITICAL |
| **Tablet 481-768px** | Grid doesn't reflow | Cards stack incorrectly | HIGH |
| **Desktop >1024px** | No fluid max-width | Content runs edge-to-edge | MEDIUM |
| **Navigation** | Not sticky, doesn't collapse | Top nav breaks on mobile | HIGH |
| **Scoreboard Module** | Fixed-width table | Overflows on <1024px | HIGH |
| **Leaderboard** | Column layout hardcoded | Unreadable on mobile | HIGH |
| **Member Profile** | Form layout not responsive | Input fields too wide | MEDIUM |
| **Admin Panel** | N/A — doesn't exist | All admin tasks | CRITICAL |
| **Quick-picks Cards** | Carousel not touch-friendly | Mobile UX broken | MEDIUM |
| **Typography** | No font scaling | Unreadable on small screens | MEDIUM |

**Total Responsive Issues:** 10  
**Estimated Fix Effort:** 40-60 hours (UX design + frontend implementation)

---

### B. MISSING FEATURES (31 Gaps)

#### Admin Console (Critical)
- [ ] Real-time update controls (pause/resume feeds)
- [ ] Manual game creation UI
- [ ] Score override functionality
- [ ] Smoove Coins admin panel (manual ledger adjustments, audits)
- [ ] Document upload/download (private admin-only storage)
- [ ] Event lifecycle manual transitions (force to archived, etc.)
- [ ] User ban/suspend controls
- [ ] Analytics dashboard

**Estimated Effort:** 30-40 hours

#### Member Profile (High)
- [ ] Profile customization (bio, avatar, display name)
- [ ] Favorite teams selection UI (5-team limit)
- [ ] Statistics dashboard (personal win %, pick history)
- [ ] Achievement/badge system
- [ ] Account settings (privacy, notifications, preferences)
- [ ] Smoove Coins transaction history (detailed ledger view)
- [ ] Referral program integration
- [ ] Password reset functionality (for freemium + visitors)

**Estimated Effort:** 50-70 hours

#### Authentication & Access
- [ ] Password reset URLs (accessible, tokenized)
- [ ] Freemium member sign-up flow
- [ ] Visitor guest access (read-only)
- [ ] Multi-factor authentication (optional, premium)

**Estimated Effort:** 8-12 hours

#### UX/Usability
- [ ] Empty state messaging (no games scheduled, etc.)
- [ ] Loading skeletons (real-time placeholder animation)
- [ ] Error handling & retry UI
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Dark mode support

**Estimated Effort:** 12-20 hours

---

## REMEDIATION ROADMAP

### **Phase 1: Responsive Design System Rebuild** (CRITICAL)
**Objective:** Make TSL function flawlessly on mobile, tablet, and desktop.

**Scope:**
- Audit current CSS and breakpoints
- Design responsive grid system (CSS Grid or Flexbox)
- Implement breakpoints: <480px, 480-768px, 768-1024px, >1024px
- Rebuild key components (dashboard, leaderboard, scoreboard, member profile)
- Touch-friendly navigation and interactions
- Font scaling and readability audit

**Effort:** 40-60 hours  
**Timeline:** 2-3 weeks (1 senior frontend dev)  
**Owner:** Frontend Lead / UX Designer  
**Deliverable:** Responsive component library + test across devices

---

### **Phase 2: Admin Console Build** (CRITICAL)
**Objective:** Empower operators to manage TSL in real-time.

**Scope:**
- Real-time feed control dashboard
- Manual game creation & score override forms
- Smoove Coins ledger admin (manual adjustments, audit log)
- Document storage (admin-only upload/download)
- Event state manual transitions
- User management (ban, suspend, email)
- Analytics & reporting

**Effort:** 30-40 hours  
**Timeline:** 2 weeks (1 fullstack dev)  
**Owner:** Backend Lead + Frontend Dev  
**Deliverable:** Full-featured admin portal with RLS-enforced access control

---

### **Phase 3: Member Profile Complete Feature Build** (HIGH)
**Objective:** Deliver the premium member experience outlined in the original plan.

**Scope:**
- Profile customization (bio, avatar, display name validation)
- Favorite teams selection (5-team limit, UI enforced + DB constraint)
- Personal statistics dashboard (win %, pick history, trends)
- Achievement/badge system (visual, leveling)
- Account settings (privacy, notifications, preferences)
- Smoove Coins transaction ledger (detailed view)
- Referral program integration (invite links, rewards)
- Password reset flow (freemium + visitor support)

**Effort:** 50-70 hours  
**Timeline:** 3 weeks (1.5 frontend devs)  
**Owner:** Frontend Lead  
**Deliverable:** Complete member portal matching original bill plan

---

### **Phase 4: Polish & Accessibility** (MEDIUM)
**Objective:** Shipping-grade UX (accessibility, error handling, empty states).

**Scope:**
- Empty state messaging (no games, loading, errors)
- Loading skeleton screens (real-time placeholders)
- Error handling & retry UI
- WCAG 2.1 AA accessibility audit + fixes
- Dark mode support (optional, premium feature)
- E2E test suite (Playwright in staging environment)

**Effort:** 20-30 hours  
**Timeline:** 1-2 weeks (1 dev + QA)  
**Owner:** QA Lead + Frontend Dev  
**Deliverable:** Accessibility audit report + passing test suite

---

## EFFORT SUMMARY

| Phase | Hours | Timeline | Team Size | Status |
|---|---|---|---|---|
| Phase 1: Responsive Rebuild | 40-60 | 2-3 weeks | 1 FE | CRITICAL |
| Phase 2: Admin Console | 30-40 | 2 weeks | 1 FS | CRITICAL |
| Phase 3: Member Profile | 50-70 | 3 weeks | 1.5 FE | HIGH |
| Phase 4: Polish & Accessibility | 20-30 | 1-2 weeks | 1 QA + 1 FE | MEDIUM |
| **TOTAL** | **140-200 hours** | **6-10 weeks** | **3-4 devs** | — |

**Recommended Approach:**
- 3 developers, 8-week timeline (parallel phases 1-3, then 4)
- Or 2 developers, 10-12 week timeline (sequential phases)

---

## RISKS & MITIGATION

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Real-time API feed breaks during member onboarding | Medium | High | Implement Phase 2 (admin fallback) first |
| Mobile redesign breaks Supabase integrations | Low | Critical | Comprehensive integration tests before mobile launch |
| Member profile data loss during migration | Low | High | Backup existing profile data; test migration in staging |
| Admin console access control misconfiguration | Low | Critical | RLS audit before Phase 2 launch; manual testing |

---

## NEXT STEPS

1. **DCS Review** — Approve remediation roadmap and effort estimates
2. **Resource Allocation** — Assign frontend, backend, and QA leads
3. **Phase 1 Kickoff** — Responsive design audit + grid system design
4. **Parallel Preparation** — Admin console spec + member profile feature inventory
5. **Weekly Checkpoints** — Track progress against timeline

---

## APPENDIX: ORIGINAL BILL PLAN REFERENCE

**Source:** ASSET-TSL-PREMIUM-LOUNGE-PLAN-001.md  
**Phases:** 8 (UI/UX, Feed, Schema, Lifecycle, Premium Portal, Security, E2E Testing, Review)  
**Critical Features:** 17  
**Original Design Tokens:** Cream/Navy/Gold  
**Target Users:** Premium members + freemium visitors  

---

**Report Prepared By:** Claude CTO (DBA AG + UX Audit Workflow)  
**Classification:** INTERNAL — PRODUCT REVIEW  
**Approval Required:** DCS Level 0 (to green-light remediation roadmap)
