/**
 * Aegis Executive Briefing Derivation Engine
 * Version 1.0.0
 */

const BRIEFING_VERSION = '1.0.0';

/**
 * Derives a briefing from the given state data.
 * @param {Object} data 
 * @returns {Object} Briefing object
 */
function deriveBriefing(data) {
  const now = new Date().toISOString();
  const currentSession = data.currentSession || {};
  const previousSession = data.previousSession || null;
  
  let since = null;
  if (currentSession.last_briefing_at) {
    since = currentSession.last_briefing_at;
  } else if (previousSession && previousSession.session_end) {
    since = previousSession.session_end;
  }

  const isAfterSince = (timestamp) => {
    if (!since) return true;
    if (!timestamp) return false;
    return new Date(timestamp) > new Date(since);
  };

  const events = data.events || [];
  const jobs = data.jobs || [];
  const missions = data.missions || [];
  const approvals = data.approvals || [];
  const nextBestAction = data.nextBestAction || null;

  // 1. Changes since last
  const changesItems = events
    .filter(e => isAfterSince(e.created_at))
    .map(e => {
      const job = jobs.find(j => j.id === e.job_id);
      return {
        type: e.event_type,
        summary: e.summary,
        timestamp: e.created_at,
        job_key: job ? job.job_key : e.job_id
      };
    });

  // 2. Completed
  const completedItems = jobs
    .filter(j => j.status === 'completed' && isAfterSince(j.completed_at))
    .map(j => {
      const mission = missions.find(m => m.id === j.mission_id);
      return {
        job_key: j.job_key,
        title: j.title,
        completed_at: j.completed_at,
        mission: mission ? mission.title : null
      };
    });

  // 3. Requires Approval
  const approvalItems = approvals
    .filter(a => a.status === 'pending')
    .map(a => {
      const job = jobs.find(j => j.id === a.job_id);
      return {
        job_key: job ? job.job_key : a.job_id,
        title: a.title,
        approval_type: a.approval_type,
        requested_at: a.requested_at
      };
    });

  // 4. Next Best Action
  let nextActionItem = null;
  if (nextBestAction && nextBestAction.job) {
    nextActionItem = {
      job_key: nextBestAction.job.job_key,
      title: nextBestAction.job.title,
      score: nextBestAction.score,
      reason: nextBestAction.reason || 'Highest scored priority'
    };
  }

  // 5. Blockers
  const blockerItems = jobs
    .filter(j => (j.status === 'blocked' || j.status === 'failed') && j.status !== 'archived')
    .map(j => ({
      job_key: j.job_key,
      title: j.title,
      failure_detail: j.failure_detail,
      since: j.updated_at
    }));

  // Summary Generation
  let summary = '';
  if (!since && completedItems.length === 0 && approvalItems.length === 0 && changesItems.length === 0 && blockerItems.length === 0) {
    summary = "Aegis session initialized. No prior activity recorded.";
  } else {
    const parts = [];
    if (completedItems.length > 0) parts.push(`${completedItems.length} item(s) completed`);
    if (approvalItems.length > 0) parts.push(`${approvalItems.length} awaiting approval`);
    if (blockerItems.length > 0) parts.push(`${blockerItems.length} active blocker(s)`);
    
    if (parts.length === 0) {
      parts.push("No major changes");
    }
    
    if (nextActionItem) {
      parts.push(`next action: ${nextActionItem.title}`);
    } else {
      parts.push("no actionable items identified");
    }
    
    summary = parts.join(', ') + '.';
    summary = summary.charAt(0).toUpperCase() + summary.slice(1);
  }

  return {
    generated_at: now,
    session_id: currentSession.id || 'unknown',
    since: since,
    sections: {
      changes_since_last: {
        title: 'Changes Since Last Session',
        items: changesItems,
        empty_message: 'No changes since last session.'
      },
      completed: {
        title: 'Completed',
        items: completedItems,
        empty_message: 'No jobs completed since last session.'
      },
      requires_approval: {
        title: 'Requires DCS Approval',
        items: approvalItems,
        empty_message: 'No items require approval.'
      },
      next_best_action: {
        title: 'Highest-Value Next Action',
        action: nextActionItem,
        empty_message: 'No actionable items available.'
      },
      blockers: {
        title: 'Active Blockers',
        items: blockerItems,
        empty_message: 'No active blockers.'
      }
    },
    summary: summary
  };
}

/**
 * Formats a briefing object into plain text.
 * @param {Object} briefing 
 * @returns {string}
 */
function formatBriefingText(briefing) {
  let text = `--- AEGIS EXECUTIVE BRIEFING ---\n`;
  text += `Generated: ${briefing.generated_at}\n`;
  text += `Session: ${briefing.session_id}\n`;
  text += `Since: ${briefing.since || 'Genesis'}\n\n`;
  text += `SUMMARY: ${briefing.summary}\n\n`;

  const s = briefing.sections;
  
  // Changes
  text += `${s.changes_since_last.title.toUpperCase()}\n`;
  if (s.changes_since_last.items.length === 0) {
    text += `- ${s.changes_since_last.empty_message}\n`;
  } else {
    s.changes_since_last.items.forEach(item => {
      text += `- [${item.timestamp}] ${item.job_key || 'SYSTEM'}: ${item.summary} (${item.type})\n`;
    });
  }
  text += '\n';

  // Completed
  text += `${s.completed.title.toUpperCase()}\n`;
  if (s.completed.items.length === 0) {
    text += `- ${s.completed.empty_message}\n`;
  } else {
    s.completed.items.forEach(item => {
      text += `- [${item.job_key}] ${item.title} (Mission: ${item.mission || 'None'}) - Completed: ${item.completed_at}\n`;
    });
  }
  text += '\n';

  // Requires Approval
  text += `${s.requires_approval.title.toUpperCase()}\n`;
  if (s.requires_approval.items.length === 0) {
    text += `- ${s.requires_approval.empty_message}\n`;
  } else {
    s.requires_approval.items.forEach(item => {
      text += `- [${item.job_key}] ${item.title} (${item.approval_type}) - Requested: ${item.requested_at}\n`;
    });
  }
  text += '\n';

  // Next Best Action
  text += `${s.next_best_action.title.toUpperCase()}\n`;
  if (!s.next_best_action.action) {
    text += `- ${s.next_best_action.empty_message}\n`;
  } else {
    const a = s.next_best_action.action;
    text += `- [${a.job_key}] ${a.title}\n`;
    text += `  Reason: ${a.reason} (Score: ${a.score})\n`;
  }
  text += '\n';

  // Blockers
  text += `${s.blockers.title.toUpperCase()}\n`;
  if (s.blockers.items.length === 0) {
    text += `- ${s.blockers.empty_message}\n`;
  } else {
    s.blockers.items.forEach(item => {
      text += `- [${item.job_key}] ${item.title} - Since: ${item.since}\n`;
      if (item.failure_detail) {
        text += `  Detail: ${item.failure_detail}\n`;
      }
    });
  }

  return text;
}

/**
 * Formats a briefing object into Markdown.
 * @param {Object} briefing 
 * @returns {string}
 */
function formatBriefingMarkdown(briefing) {
  let md = `# Aegis Executive Briefing\n\n`;
  md += `**Generated:** ${briefing.generated_at}  \n`;
  md += `**Session:** ${briefing.session_id}  \n`;
  md += `**Since:** ${briefing.since || 'Genesis'}  \n\n`;
  md += `> **Executive Summary:** ${briefing.summary}\n\n`;

  const s = briefing.sections;
  
  // Changes
  md += `## ${s.changes_since_last.title}\n`;
  if (s.changes_since_last.items.length === 0) {
    md += `*${s.changes_since_last.empty_message}*\n`;
  } else {
    s.changes_since_last.items.forEach(item => {
      md += `- **[${item.job_key || 'SYSTEM'}]** ${item.summary} \`(${item.type})\` - *${item.timestamp}*\n`;
    });
  }
  md += '\n';

  // Completed
  md += `## ${s.completed.title}\n`;
  if (s.completed.items.length === 0) {
    md += `*${s.completed.empty_message}*\n`;
  } else {
    s.completed.items.forEach(item => {
      md += `- **[${item.job_key}]** ${item.title} (Mission: ${item.mission || 'None'}) - *Completed: ${item.completed_at}*\n`;
    });
  }
  md += '\n';

  // Requires Approval
  md += `## ${s.requires_approval.title}\n`;
  if (s.requires_approval.items.length === 0) {
    md += `*${s.requires_approval.empty_message}*\n`;
  } else {
    s.requires_approval.items.forEach(item => {
      md += `- **[${item.job_key}]** ${item.title} \`(${item.approval_type})\` - *Requested: ${item.requested_at}*\n`;
    });
  }
  md += '\n';

  // Next Best Action
  md += `## ${s.next_best_action.title}\n`;
  if (!s.next_best_action.action) {
    md += `*${s.next_best_action.empty_message}*\n`;
  } else {
    const a = s.next_best_action.action;
    md += `- **[${a.job_key}]** ${a.title} \n`;
    md += `  - **Reason:** ${a.reason} \`(Score: ${a.score})\`\n`;
  }
  md += '\n';

  // Blockers
  md += `## ${s.blockers.title}\n`;
  if (s.blockers.items.length === 0) {
    md += `*${s.blockers.empty_message}*\n`;
  } else {
    s.blockers.items.forEach(item => {
      md += `- **[${item.job_key}]** ${item.title} - *Since: ${item.since}*\n`;
      if (item.failure_detail) {
        md += `  - **Detail:** ${item.failure_detail}\n`;
      }
    });
  }

  return md;
}

module.exports = {
  BRIEFING_VERSION,
  deriveBriefing,
  formatBriefingText,
  formatBriefingMarkdown
};
