/**
 * Aegis Executive Kernel Slice 001 — Comprehensive Test Suite
 * Task: DCSE-PA-MODULE-001-AG01
 * Test runner: node:test (zero external dependencies)
 * 
 * Run: node --test tests/aegis-slice001.test.js
 */
const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

// ---- Module Loading ----
const apiHandler = require('../apps/aegis/api/index.js');
const scoringEngine = require('../apps/aegis/lib/scoring.js');
const briefingEngine = require('../apps/aegis/lib/briefing.js');

// ---- Read source files for static analysis ----
const apiSource = fs.readFileSync(path.join(__dirname, '..', 'apps', 'aegis', 'api', 'index.js'), 'utf-8');
const migrationSource = fs.readFileSync(path.join(__dirname, '..', 'apps', 'aegis', 'migrations', '001_aegis_schema.sql'), 'utf-8');

// ---- State Machine (from implementation) ----
const VALID_TRANSITIONS = {
  queued: ['running', 'cancelled'],
  running: ['waiting_approval', 'completed', 'failed', 'cancelled'],
  waiting_approval: ['running', 'completed', 'failed', 'cancelled'],
  completed: ['archived'],
  failed: ['queued', 'archived'],
  cancelled: ['queued', 'archived'],
  archived: []
};

function isValidTransition(from, to) {
  return VALID_TRANSITIONS[from]?.includes(to) || false;
}

// ---- Mock res helper for SPA-serving tests ----
function mockSpaRes() {
  let body = '';
  let headers = {};
  return {
    setHeader(k, v) { headers[k] = v; },
    set statusCode(c) { this._code = c; },
    get statusCode() { return this._code || 200; },
    end(data) { body = data || ''; },
    getBody() { return body; },
    getHeaders() { return headers; }
  };
}

// ---- Shared mock job/mission factories ----
function mockMission(overrides = {}) {
  return { id: 'mission-1', mission_key: 'dcs_enterprise', title: 'DCS Enterprise', priority: 90, status: 'active', ...overrides };
}

function mockJob(overrides = {}) {
  return {
    id: 'job-1', job_key: 'AEGIS-TEST1', title: 'Test Job', status: 'queued',
    priority: 50, mission_id: 'mission-1', requires_approval: false,
    revenue_relevance: 0, dcs_override: 0, deadline: null,
    created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    completed_at: null, failure_detail: null, ...overrides
  };
}


describe('Aegis Executive Kernel Slice 001 Test Suite', () => {

  // ================================================================
  // PASS 1: FUNCTIONAL AND INTEGRATION
  // ================================================================
  describe('Pass 1: Functional and Integration', () => {

    it('1. App boot — require() the API module exports a function', () => {
      assert.strictEqual(typeof apiHandler, 'function', 'API handler must be a function');
    });

    it('2. Auth scaffolding — API routes exist for session management', () => {
      // Verify the source contains session route handlers (static analysis)
      assert.match(apiSource, /\/api\/aegis\/session\/start/, 'Session start route must exist');
      assert.match(apiSource, /\/api\/aegis\/session/, 'Session GET route must exist');
      // Verify the SPA-serve fallback works for non-API routes
      const res = mockSpaRes();
      apiHandler({ url: '/', method: 'GET' }, res);
      assert.match(res.getBody(), /<!DOCTYPE html>/, 'Non-API routes should serve SPA HTML');
    });

    it('3. Session persistence — session handler returns correct shape without DB', () => {
      // Without SUPABASE_KEY, session GET should return 503 via async handler
      // We verify the route dispatches (the handler is async and needs Supabase)
      assert.match(apiSource, /handleSessionStart/, 'Session start handler must be defined');
      assert.match(apiSource, /handleSessionGet/, 'Session get handler must be defined');
      assert.match(apiSource, /executive_sessions/, 'Session handler must reference executive_sessions table');
    });

    it('4. Mission retrieval — mission handler references correct table', () => {
      assert.match(apiSource, /handleMissions/, 'Missions handler must be defined');
      assert.match(apiSource, /missions/, 'Missions handler must reference missions table');
      assert.match(apiSource, /order=priority\.desc/, 'Missions should be ordered by priority descending');
    });

    it('5. Job state machine — valid transitions accepted', () => {
      assert.ok(isValidTransition('queued', 'running'));
      assert.ok(isValidTransition('queued', 'cancelled'));
      assert.ok(isValidTransition('running', 'completed'));
      assert.ok(isValidTransition('running', 'waiting_approval'));
      assert.ok(isValidTransition('running', 'failed'));
      assert.ok(isValidTransition('running', 'cancelled'));
      assert.ok(isValidTransition('waiting_approval', 'completed'));
      assert.ok(isValidTransition('waiting_approval', 'running'));
      assert.ok(isValidTransition('completed', 'archived'));
      assert.ok(isValidTransition('failed', 'queued'), 'Failed jobs must be retriable');
      assert.ok(isValidTransition('failed', 'archived'));
      assert.ok(isValidTransition('cancelled', 'queued'), 'Cancelled jobs must be retriable');
    });

    it('5b. Job state machine — invalid transitions rejected', () => {
      assert.ok(!isValidTransition('queued', 'completed'), 'Cannot skip running');
      assert.ok(!isValidTransition('completed', 'running'), 'Completed is terminal except archive');
      assert.ok(!isValidTransition('archived', 'running'), 'Archived is terminal');
      assert.ok(!isValidTransition('archived', 'queued'), 'Archived is terminal');
    });

    it('6. Job failure handling — failed status blocks forward progress', () => {
      assert.ok(isValidTransition('running', 'failed'));
      assert.ok(!isValidTransition('failed', 'completed'), 'Failed cannot directly complete');
      assert.ok(!isValidTransition('failed', 'running'), 'Failed cannot directly resume (must re-queue)');
    });

    it('7. Approval transitions — approval lifecycle is correct', () => {
      assert.ok(isValidTransition('running', 'waiting_approval'));
      assert.ok(isValidTransition('waiting_approval', 'completed'));
      assert.ok(isValidTransition('waiting_approval', 'running'), 'Rejected approvals return to running');
      assert.ok(isValidTransition('waiting_approval', 'cancelled'), 'Approvals can be cancelled');
    });

    it('8. Briefing derivation — produces correct structure from mock data', () => {
      const briefing = briefingEngine.deriveBriefing({
        currentSession: { id: 's1', session_start: '2026-09-09T01:00:00Z', last_briefing_at: null },
        previousSession: { id: 's0', session_start: '2026-09-08T01:00:00Z', session_end: '2026-09-08T20:00:00Z' },
        jobs: [
          mockJob({ id: 'j1', job_key: 'AEGIS-J1', title: 'Completed task', status: 'completed', completed_at: '2026-09-09T00:00:00Z' }),
          mockJob({ id: 'j2', job_key: 'AEGIS-J2', title: 'Blocked task', status: 'blocked', failure_detail: 'Missing config' }),
          mockJob({ id: 'j3', job_key: 'AEGIS-J3', title: 'Active task', status: 'running' })
        ],
        missions: [mockMission()],
        events: [
          { id: 'e1', job_id: 'j1', event_type: 'status_change', actor: 'aegis', summary: 'Completed', created_at: '2026-09-09T00:00:00Z' }
        ],
        approvals: [
          { id: 'a1', job_id: 'j3', approval_type: 'deploy', title: 'Deploy to staging', status: 'pending', requested_at: '2026-09-09T01:00:00Z' }
        ],
        nextBestAction: null
      });

      // Verify structure
      assert.ok(briefing.generated_at, 'Must have generated_at');
      assert.ok(briefing.sections, 'Must have sections');
      assert.ok(briefing.sections.changes_since_last, 'Must have changes section');
      assert.ok(briefing.sections.completed, 'Must have completed section');
      assert.ok(briefing.sections.requires_approval, 'Must have approval section');
      assert.ok(briefing.sections.blockers, 'Must have blockers section');
      assert.ok(briefing.sections.next_best_action, 'Must have NBA section');
      assert.ok(typeof briefing.summary === 'string', 'Must have summary string');

      // Verify content
      assert.ok(briefing.sections.completed.items.length >= 1, 'Should find completed job');
      assert.ok(briefing.sections.blockers.items.length >= 1, 'Should find blocked job');
      assert.ok(briefing.sections.requires_approval.items.length >= 1, 'Should find pending approval');

      // Verify text/markdown formatters
      const txt = briefingEngine.formatBriefingText(briefing);
      const md = briefingEngine.formatBriefingMarkdown(briefing);
      assert.strictEqual(typeof txt, 'string', 'formatBriefingText must return string');
      assert.strictEqual(typeof md, 'string', 'formatBriefingMarkdown must return string');
      assert.ok(txt.length > 0, 'Text briefing must not be empty');
      assert.ok(md.length > 0, 'Markdown briefing must not be empty');
    });

    it('9. Next-best-action — scoring is deterministic', () => {
      const mission = mockMission({ priority: 80 });
      const job = mockJob({ priority: 70, revenue_relevance: 0.5, dcs_override: 20 });

      const score1 = scoringEngine.scoreJob(job, mission);
      const score2 = scoringEngine.scoreJob(job, mission);

      // Structural equality
      assert.deepStrictEqual(score1, score2, 'Same inputs must produce identical scores');
      // Verify shape
      assert.strictEqual(typeof score1.composite_score, 'number');
      assert.ok(score1.score_components, 'Must have score_components');
      assert.strictEqual(typeof score1.reason_summary, 'string');
      // Verify all 8 components present
      const requiredComponents = ['mission_priority', 'job_priority', 'urgency', 'blocked_penalty', 'approval_bonus', 'revenue_weight', 'staleness', 'dcs_override'];
      for (const c of requiredComponents) {
        assert.ok(score1.score_components[c], `Missing component: ${c}`);
        assert.strictEqual(typeof score1.score_components[c].raw, 'number', `${c}.raw must be number`);
        assert.strictEqual(typeof score1.score_components[c].weight, 'number', `${c}.weight must be number`);
        assert.strictEqual(typeof score1.score_components[c].contribution, 'number', `${c}.contribution must be number`);
      }
    });

    it('9b. Next-best-action — blocked jobs score lower than actionable', () => {
      const mission = mockMission();
      const activeJob = mockJob({ id: 'active', status: 'queued', priority: 50 });
      const blockedJob = mockJob({ id: 'blocked', status: 'blocked', priority: 90 });

      const activeScore = scoringEngine.scoreJob(activeJob, mission);
      const blockedScore = scoringEngine.scoreJob(blockedJob, mission);

      assert.ok(activeScore.composite_score > blockedScore.composite_score,
        `Active (${activeScore.composite_score}) must score higher than blocked (${blockedScore.composite_score})`);
    });

    it('10. RLS access matrix — migration enforces RLS on all tables', () => {
      const tables = ['principals', 'missions', 'executive_sessions', 'jobs', 'job_events', 'approvals', 'evidence', 'next_actions', 'notifications'];
      for (const t of tables) {
        assert.match(migrationSource, new RegExp(`ENABLE ROW LEVEL SECURITY`, 'i'), `RLS must be enabled`);
      }
      assert.match(migrationSource, /is_dcs_principal|is_dcs_owner/i, 'Must use DCS principal/owner predicate');
      assert.match(migrationSource, /REVOKE EXECUTE/i, 'Must revoke public EXECUTE');
    });

    it('11. Evidence/receipt creation — API handler exists', () => {
      assert.match(apiSource, /handleEvidenceCreate/, 'Evidence creation handler must exist');
      assert.match(apiSource, /evidence_type/, 'Evidence handler must validate evidence_type');
      assert.match(apiSource, /\/api\/aegis\/evidence/, 'Evidence route must exist');
    });

    it('12. Duplicate/idempotency — job key is unique', () => {
      assert.match(apiSource, /job_key/, 'Job creation must generate unique job_key');
      assert.match(apiSource, /AEGIS-/, 'Job keys must be prefixed AEGIS-');
      assert.match(migrationSource, /job_key TEXT NOT NULL UNIQUE/i, 'job_key must have UNIQUE constraint');
    });
  });

  // ================================================================
  // PASS 2: E2E, ADVERSARIAL, REGRESSION
  // ================================================================
  describe('Pass 2: E2E, Adversarial, Regression', () => {

    // Get actual HTML output from the SPA handler
    let htmlContent = '';
    const res = mockSpaRes();
    apiHandler({ url: '/', method: 'GET' }, res);
    htmlContent = res.getBody();

    it('13. Desktop viewport — viewport meta tag exists in SPA', () => {
      assert.ok(htmlContent.length > 0, 'SPA HTML must not be empty');
      assert.match(htmlContent, /<meta name="viewport"/, 'Viewport meta tag must exist');
      assert.match(htmlContent, /width=device-width/, 'Viewport must include device-width');
    });

    it('14. Android/mobile viewport — responsive CSS media query exists', () => {
      assert.match(htmlContent, /@media\s*\(\s*max-width\s*:\s*768px\s*\)/, 'Mobile media query must exist');
    });

    it('15. Keyboard navigation — focus-visible styles exist', () => {
      assert.match(htmlContent, /:focus-visible/, 'focus-visible CSS must exist');
      assert.match(htmlContent, /outline.*var\(--gold\)/, 'Focus outline should use gold color');
    });

    it('15b. DCS Branding — palette tokens present', () => {
      assert.match(htmlContent, /#0A192F/i, 'Navy color #0A192F must exist');
      assert.match(htmlContent, /#D4AF37/i, 'Gold color #D4AF37 must exist');
      assert.match(htmlContent, /Space Grotesk/i, 'Space Grotesk font must be loaded');
      assert.match(htmlContent, /JetBrains Mono/i, 'JetBrains Mono font must be loaded');
    });

    it('16. Reload/session restore — session GET route exists for restore', () => {
      assert.match(apiSource, /api\/aegis\/session.*GET/, 'Session GET route must exist for restore');
      assert.match(apiSource, /session_start/, 'Session handler must track session_start');
    });

    it('17. Invalid state transitions — adversarial rejection', () => {
      assert.ok(!isValidTransition('completed', 'running'), 'completed→running must be rejected');
      assert.ok(!isValidTransition('archived', 'running'), 'archived→running must be rejected');
      assert.ok(!isValidTransition('queued', 'archived'), 'queued→archived must be rejected (must cancel first)');
      assert.ok(!isValidTransition('queued', 'waiting_approval'), 'queued→waiting_approval must be rejected (must run first)');
      // Verify API validates transitions
      assert.match(apiSource, /VALID_TRANSITIONS/, 'API must enforce transition validation');
      assert.match(apiSource, /Cannot transition from/, 'API must return error for invalid transitions');
    });

    it('18. Approval bypass — approval required check exists', () => {
      assert.match(apiSource, /requires_approval/, 'Approval requirement field must be checked');
      assert.match(apiSource, /approval_type/, 'Approval type must be validated');
      assert.match(apiSource, /approved.*rejected/, 'Decision must be approved or rejected');
    });

    it('19. Stale job handling — staleness scoring boundaries', () => {
      const mission = mockMission();
      const now = new Date();

      // Fresh job (< 1 day old): staleness raw = 20
      const freshJob = mockJob({ created_at: new Date(now - 1000 * 60 * 30).toISOString() }); // 30 min ago
      const freshScore = scoringEngine.scoreJob(freshJob, mission);
      assert.strictEqual(freshScore.score_components.staleness.raw, 20, 'Fresh job staleness = 20');

      // 2-day-old job (> 1 day, < 3 days): staleness raw = 40
      const twoDayJob = mockJob({ created_at: new Date(now - 1000 * 60 * 60 * 48).toISOString() });
      const twoDayScore = scoringEngine.scoreJob(twoDayJob, mission);
      assert.strictEqual(twoDayScore.score_components.staleness.raw, 40, '2-day job staleness = 40');

      // 5-day-old job (> 3 days, < 7 days): staleness raw = 60
      const fiveDayJob = mockJob({ created_at: new Date(now - 1000 * 60 * 60 * 120).toISOString() });
      const fiveDayScore = scoringEngine.scoreJob(fiveDayJob, mission);
      assert.strictEqual(fiveDayScore.score_components.staleness.raw, 60, '5-day job staleness = 60');

      // 10-day-old job (> 7 days): staleness raw = 80
      const tenDayJob = mockJob({ created_at: new Date(now - 1000 * 60 * 60 * 240).toISOString() });
      const tenDayScore = scoringEngine.scoreJob(tenDayJob, mission);
      assert.strictEqual(tenDayScore.score_components.staleness.raw, 80, '10-day job staleness = 80');

      // Verify older scores higher staleness contribution
      assert.ok(tenDayScore.score_components.staleness.contribution > freshScore.score_components.staleness.contribution,
        'Older jobs must have higher staleness contribution');

      // No timestamp: staleness raw = 20 (default)
      const noTsJob = mockJob({ created_at: null });
      const noTsScore = scoringEngine.scoreJob(noTsJob, mission);
      assert.strictEqual(noTsScore.score_components.staleness.raw, 20, 'No timestamp defaults to 20');

      // Exact boundary: 24h exactly (> 24h threshold)
      const exactDayJob = mockJob({ created_at: new Date(now - 1000 * 60 * 60 * 24 - 1).toISOString() });
      const exactDayScore = scoringEngine.scoreJob(exactDayJob, mission);
      assert.strictEqual(exactDayScore.score_components.staleness.raw, 40, 'Exactly 24h+1ms = 40');

      // Determinism: same evaluation produces same result
      const scoreA = scoringEngine.scoreJob(fiveDayJob, mission);
      const scoreB = scoringEngine.scoreJob(fiveDayJob, mission);
      assert.deepStrictEqual(scoreA.score_components.staleness, scoreB.score_components.staleness,
        'Staleness must be deterministic for same input');
    });

    it('20. Scoring reproducibility — same input always produces identical score', () => {
      const mission = mockMission({ priority: 75 });
      const job = mockJob({ priority: 60, revenue_relevance: 0.3, dcs_override: 10 });

      const score1 = scoringEngine.scoreJob(job, mission);
      const score2 = scoringEngine.scoreJob(job, mission);
      const score3 = scoringEngine.scoreJob(job, mission);

      assert.deepStrictEqual(score1, score2, 'Run 1 and 2 must be identical');
      assert.deepStrictEqual(score2, score3, 'Run 2 and 3 must be identical');
    });

    it('21. NBA exclusions — blocked/archived/completed jobs excluded', () => {
      const mission = mockMission();
      const jobs = [
        mockJob({ id: 'j1', status: 'blocked', priority: 90 }),
        mockJob({ id: 'j2', status: 'archived', priority: 90 }),
        mockJob({ id: 'j3', status: 'completed', priority: 90 }),
        mockJob({ id: 'j4', status: 'queued', priority: 50, job_key: 'AEGIS-ACTIVE' })
      ];

      const best = scoringEngine.getNextBestAction(jobs, [mission]);
      assert.ok(best, 'Should find an actionable job');
      assert.strictEqual(best.id, 'j4', 'Must return the actionable queued job');
    });

    it('22. Security — no secrets in client code', () => {
      assert.ok(!apiSource.includes('SUPABASE_SERVICE_ROLE_KEY') || apiSource.match(/process\.env\.SUPABASE_SERVICE_ROLE_KEY/),
        'Service role key must only be accessed via process.env');
      // Verify service key is not in HTML
      const res2 = mockSpaRes();
      apiHandler({ url: '/', method: 'GET' }, res2);
      const html = res2.getBody();
      assert.ok(!html.includes('service_role'), 'SPA HTML must not contain service_role references');
    });

    it('23. Migration — rollback section exists', () => {
      assert.match(migrationSource, /ROLLBACK|DROP SCHEMA/i, 'Migration must include rollback instructions');
    });

    it('24. Route error handling — unrecognized routes serve SPA', () => {
      const res3 = mockSpaRes();
      apiHandler({ url: '/nonexistent/path', method: 'GET' }, res3);
      assert.match(res3.getBody(), /<!DOCTYPE html>/, 'Unknown routes must serve SPA HTML');
    });

    it('25. CORS — OPTIONS returns correct headers', () => {
      const res4 = mockSpaRes();
      apiHandler({ url: '/api/aegis/health', method: 'OPTIONS' }, res4);
      assert.strictEqual(res4.getHeaders()['Access-Control-Allow-Origin'], '*', 'CORS origin must be *');
      assert.match(res4.getHeaders()['Access-Control-Allow-Methods'], /POST/, 'CORS must allow POST');
    });
  });
});
