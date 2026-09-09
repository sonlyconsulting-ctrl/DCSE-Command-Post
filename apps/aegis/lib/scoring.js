/**
 * @fileoverview Deterministic next-best-action scoring engine for Aegis Executive Kernel.
 */

const SCORING_VERSION = '1.0.0';

/**
 * Parses a date or returns null.
 * @param {string|Date} dateVal 
 * @returns {Date|null}
 */
function parseDate(dateVal) {
    if (!dateVal) return null;
    const d = new Date(dateVal);
    return isNaN(d.getTime()) ? null : d;
}

/**
 * Scores a single job based on its properties and its associated mission.
 * @param {Object} job - The job object to score.
 * @param {Object} mission - The mission object associated with the job.
 * @returns {Object} The score object containing composite_score, score_components, and reason_summary.
 */
function scoreJob(job, mission) {
    const weights = {
        mission_priority: 0.15,
        job_priority: 0.20,
        urgency: 0.20,
        blocked_penalty: 0.15,
        approval_bonus: 0.10,
        revenue_weight: 0.05,
        staleness: 0.10,
        dcs_override: 0.05
    };

    // 1. Mission Priority
    const missionPriorityRaw = mission && mission.priority !== undefined ? Number(mission.priority) : 50;
    
    // 2. Job Priority
    const jobPriorityRaw = job && job.priority !== undefined ? Number(job.priority) : 50;

    // 3. Urgency
    let urgencyRaw = 50;
    let deadline = job.deadline ? job.deadline : null;
    let hoursRemaining = null;
    if (deadline) {
        const dlDate = parseDate(deadline);
        if (dlDate) {
            const now = new Date();
            const msRemaining = dlDate.getTime() - now.getTime();
            hoursRemaining = msRemaining / (1000 * 60 * 60);
            if (hoursRemaining < 1) urgencyRaw = 100;
            else if (hoursRemaining < 24) urgencyRaw = 85;
            else if (hoursRemaining < 72) urgencyRaw = 70;
            else if (hoursRemaining < 24 * 7) urgencyRaw = 55;
            else urgencyRaw = 30;
        }
    }

    // 4. Blocked Penalty
    const blockedStatuses = ['blocked', 'failed', 'cancelled', 'archived'];
    const isBlocked = blockedStatuses.includes(String(job.status).toLowerCase());
    const blockedPenaltyRaw = isBlocked ? -100 : 0;

    // 5. Approval Bonus
    const requiresApproval = Boolean(job.requires_approval);
    const hasPending = String(job.status).toLowerCase() === 'waiting_approval';
    const approvalBonusRaw = (requiresApproval && hasPending) ? 30 : 0;

    // 6. Revenue Weight
    const revenueRelevance = job.revenue_relevance !== undefined ? Number(job.revenue_relevance) : 0;
    const revenueRaw = Math.min(Math.max(revenueRelevance * 100, 0), 100);

    // 7. Staleness
    let stalenessRaw = 20;
    let ageHours = 0;
    if (job.created_at) {
        const createdDate = parseDate(job.created_at);
        if (createdDate) {
            const now = new Date();
            const msAge = now.getTime() - createdDate.getTime();
            ageHours = msAge / (1000 * 60 * 60);
            if (ageHours > 24 * 7) stalenessRaw = 80;
            else if (ageHours > 24 * 3) stalenessRaw = 60;
            else if (ageHours > 24) stalenessRaw = 40;
            else stalenessRaw = 20;
        }
    }

    // 8. DCS Override
    const overrideVal = job.dcs_override !== undefined ? Number(job.dcs_override) : 0;
    const dcsOverrideRaw = Math.min(Math.max((overrideVal + 100) / 2, 0), 100);

    const components = {
        mission_priority: { raw: missionPriorityRaw, weight: weights.mission_priority, contribution: missionPriorityRaw * weights.mission_priority },
        job_priority: { raw: jobPriorityRaw, weight: weights.job_priority, contribution: jobPriorityRaw * weights.job_priority },
        urgency: { raw: urgencyRaw, weight: weights.urgency, contribution: urgencyRaw * weights.urgency, deadline: deadline, hours_remaining: hoursRemaining },
        blocked_penalty: { raw: blockedPenaltyRaw, weight: weights.blocked_penalty, contribution: blockedPenaltyRaw * weights.blocked_penalty, is_blocked: isBlocked },
        approval_bonus: { raw: approvalBonusRaw, weight: weights.approval_bonus, contribution: approvalBonusRaw * weights.approval_bonus, requires_approval: requiresApproval, has_pending: hasPending },
        revenue_weight: { raw: revenueRaw, weight: weights.revenue_weight, contribution: revenueRaw * weights.revenue_weight },
        staleness: { raw: stalenessRaw, weight: weights.staleness, contribution: stalenessRaw * weights.staleness, age_hours: ageHours },
        dcs_override: { raw: dcsOverrideRaw, weight: weights.dcs_override, contribution: dcsOverrideRaw * weights.dcs_override }
    };

    let compositeScore = 0;
    for (const key of Object.keys(components)) {
        compositeScore += components[key].contribution;
    }

    // Reason Summary Generation
    const priorityLabel = compositeScore >= 70 ? 'HIGH' : compositeScore >= 40 ? 'MEDIUM' : 'LOW';
    const factors = [];
    if (components.urgency.raw >= 85) factors.push(`Deadline in ${hoursRemaining !== null ? hoursRemaining.toFixed(1) : 'few'} hours`);
    else if (components.urgency.raw >= 55) factors.push(`Upcoming deadline`);
    
    if (components.approval_bonus.raw > 0) factors.push('Awaiting approval');
    if (components.blocked_penalty.is_blocked) factors.push('Blocked/Archived');
    if (components.dcs_override.raw > 50) factors.push('DCS Override applied');
    if (components.staleness.raw >= 60) factors.push('Stale/Aging task');
    if (components.revenue_weight.raw > 0) factors.push(`Revenue-relevant (${revenueRelevance})`);
    if (components.job_priority.raw > 75) factors.push('High job priority');
    if (components.mission_priority.raw > 75) factors.push('High mission priority');

    if (factors.length === 0) factors.push('Standard priority');
    
    let reasonText = `[${priorityLabel}] ${job.title || 'Untitled'} — ${factors[0]}.`;
    if (factors.length > 1) {
        reasonText += ` ${factors[1]}.`;
    }

    return {
        composite_score: compositeScore,
        score_components: components,
        reason_summary: reasonText
    };
}

/**
 * Scores and ranks jobs.
 * @param {Array<Object>} jobs - Array of job objects.
 * @param {Array<Object>} missions - Array of mission objects.
 * @returns {Array<Object>} Jobs sorted by composite_score descending with score detail attached.
 */
function rankJobs(jobs, missions) {
    if (!jobs || !Array.isArray(jobs)) return [];
    const missionMap = {};
    if (missions && Array.isArray(missions)) {
        for (const m of missions) {
            missionMap[m.id] = m;
        }
    }

    const scoredJobs = jobs.map(job => {
        const mission = job.mission_id ? missionMap[job.mission_id] : null;
        const scoreInfo = scoreJob(job, mission);
        return {
            ...job,
            ...scoreInfo
        };
    });

    return scoredJobs.sort((a, b) => b.composite_score - a.composite_score);
}

/**
 * Returns the single highest-scored actionable (non-blocked, non-archived, non-completed) job.
 * @param {Array<Object>} jobs - Array of job objects.
 * @param {Array<Object>} missions - Array of mission objects.
 * @returns {Object|null} The highest scored actionable job with full score detail.
 */
function getNextBestAction(jobs, missions) {
    const scoredJobs = rankJobs(jobs, missions);
    const nonActionableStatuses = ['blocked', 'failed', 'cancelled', 'archived', 'completed', 'done'];
    const actionable = scoredJobs.filter(job => !nonActionableStatuses.includes(String(job.status).toLowerCase()));
    
    if (actionable.length === 0) return null;
    return actionable[0];
}

module.exports = {
    SCORING_VERSION,
    scoreJob,
    rankJobs,
    getNextBestAction
};
