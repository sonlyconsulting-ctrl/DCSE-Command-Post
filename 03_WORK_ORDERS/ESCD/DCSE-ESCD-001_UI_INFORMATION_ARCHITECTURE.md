# ESCD UI INFORMATION ARCHITECTURE

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Design objective

The ESCD interface should answer executive questions before exposing system complexity. Command Post detail remains accessible but does not dominate the assistant experience.

## Primary navigation

1. **Today**: executive briefing, NOW queue, next-best action, approvals, commitments, recent completions.
2. **Inbox**: pins/intake, untriaged items, source context, dedupe decisions.
3. **Tasks & Projects**: active work, dependencies, milestones, statuses, filters by mission.
4. **Employment**: opportunities, recruiter/client actions, submissions, follow-ups, interviews, revenue view.
5. **Approvals & Decisions**: consequential proposed actions and decision packets.
6. **Workflows**: delegated jobs, routines, watches, execution/retry state.
7. **Evidence & History**: receipts, completed work, source/evidence chain, briefing history.
8. **Connections**: connector health and source status without secret exposure.
9. **Settings**: autonomy preferences, notifications, identity, display preferences, routine controls.
10. **Command Post**: governed deep-link/hybrid access for enterprise control detail.

## Today layout

Top-to-bottom priority:

- identity/mission context and current time
- executive snapshot
- next-best action card with rationale
- approvals requiring DCS
- today's commitments/deadlines
- DCS Employment/revenue actions
- blockers/waiting/watches
- completed since last acknowledgement

## Interaction patterns

Every actionable card should support appropriate subset of: open source, start, approve/reject/defer, mark waiting, change priority, assign/delegate, add evidence, close/cancel. Destructive controls require explicit confirmation and authority policy.

## Status language

Use plain operational states: NOW, APPROVAL, WAITING, WATCH, BACKLOG, RUNNING, FAILED, COMPLETED. Avoid model-centric jargon in the primary UI.

## Mobile

Android-class layout is a first-class target. Primary actions must remain reachable without horizontal scrolling. Dense audit/evidence tables may use drill-down views rather than compressing unreadably.

## Accessibility

Keyboard navigation, focus visibility, semantic headings/landmarks, text alternatives, readable contrast, responsive scaling, and reduced-motion support should be designed to target accessibility standards. Do not claim formal compliance without audit evidence.

## Brand

Use DCS Enterprise visual language: DCSE Blue `#0A192F`, Gold `#D4AF37`, restrained executive presentation. Any additional ESCD tokens remain candidate/internal until separately promoted.

## Acceptance

Validate desktop/mobile, empty/loading/error states, keyboard navigation, focus, responsive navigation, long titles, many approvals, no-data state, stale connector state, and evidence drill-down.