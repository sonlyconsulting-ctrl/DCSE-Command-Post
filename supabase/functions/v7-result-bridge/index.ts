/**
 * V7 Result Bridge - Edge Function
 *
 * Polls v7_worker.result_submission for pending results.
 * Validates, writes to dcse_cp.agent_task_events, acknowledges.
 *
 * Triggers:
 * - POST /functions/v7-result-bridge (manual invoke)
 * - Scheduled: every 30 seconds via Supabase Cron
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const supabase = createClient(supabaseUrl, supabaseKey);

interface ResultSubmission {
  submission_id: number;
  task_id: string;
  claim_id: number;
  agent_id: string;
  submission_status: string;
  result_event_type: string;
  result_output: Record<string, unknown>;
  worker_session_id: string;
  submission_attempted_at: string;
}

interface TaskEventPayload {
  task_id: string;
  event_type: string;
  event_summary: string;
  event_details: Record<string, unknown>;
  created_by_label: string;
}

async function processPendingResults() {
  console.log("[v7-result-bridge] Starting result processing cycle");

  const startTime = Date.now();
  let processed = 0;
  let failed = 0;
  const receipts: unknown[] = [];

  try {
    // 1. Fetch pending submissions
    const { data: submissions, error: fetchError } = await supabase
      .from("v7_worker.result_submission")
      .select("*")
      .eq("submission_status", "pending")
      .order("submission_attempted_at", { ascending: true })
      .limit(10);

    if (fetchError) {
      throw new Error(`Failed to fetch submissions: ${fetchError.message}`);
    }

    console.log(`[v7-result-bridge] Found ${submissions?.length || 0} pending submissions`);

    if (!submissions || submissions.length === 0) {
      return {
        status: "success",
        processed: 0,
        failed: 0,
        receipts: [],
        duration_ms: Date.now() - startTime,
      };
    }

    // 2. Process each submission
    for (const submission of submissions) {
      const submissionReceipt: Record<string, unknown> = {
        submission_id: submission.submission_id,
        task_id: submission.task_id,
        processing_started_at: new Date().toISOString(),
      };

      try {
        // Validate result structure
        if (!submission.task_id || !submission.result_event_type) {
          throw new Error("Missing required fields: task_id or result_event_type");
        }

        // 3. Write to dcse_cp.agent_task_events
        const eventPayload = {
          task_id: submission.task_id,
          event_type: submission.result_event_type,
          event_summary: `Worker ${submission.agent_id} submitted: ${submission.result_event_type}`,
          event_payload: {
            submission_id: submission.submission_id,
            claim_id: submission.claim_id,
            agent_id: submission.agent_id,
            worker_session_id: submission.worker_session_id,
            result_output: submission.result_output,
          },
          actor_label: submission.agent_id,
        };

        const { data: eventData, error: eventError } = await supabase
          .from("dcse_cp.agent_task_events")
          .insert([eventPayload])
          .select("id")
          .single();

        if (eventError) {
          throw new Error(`Failed to write event: ${eventError.message}`);
        }

        submissionReceipt.dc_event_id = eventData?.id;

        // 4. Update task status in v7_bootstrap.tasks
        const newTaskStatus = mapEventTypeToTaskStatus(submission.result_event_type);
        const { error: taskError } = await supabase
          .from("v7_bootstrap.tasks")
          .update({ status: newTaskStatus })
          .eq("task_id", submission.task_id);

        if (taskError) {
          console.warn(
            `[v7-result-bridge] Warning: Could not update task status: ${taskError.message}`
          );
          // Don't fail the entire submission for this
        }

        // 5. Mark result submission as acked
        const { error: ackError } = await supabase
          .from("v7_worker.result_submission")
          .update({
            submission_status: "acked",
            submission_acked_at: new Date().toISOString(),
            dc_event_id: eventData?.id || null,
          })
          .eq("submission_id", submission.submission_id);

        if (ackError) {
          throw new Error(`Failed to acknowledge submission: ${ackError.message}`);
        }

        submissionReceipt.status = "success";
        submissionReceipt.processing_completed_at = new Date().toISOString();
        processed++;
      } catch (error) {
        console.error(
          `[v7-result-bridge] Error processing submission ${submission.submission_id}: ${error}`
        );
        submissionReceipt.status = "failed";
        submissionReceipt.error = (error as Error).message;
        failed++;

        // Mark as failed so we don't retry forever
        await supabase
          .from("v7_worker.result_submission")
          .update({
            submission_status: "failed",
            last_error: (error as Error).message,
          })
          .eq("submission_id", submission.submission_id);
      }

      receipts.push(submissionReceipt);
    }

    const duration = Date.now() - startTime;
    console.log(
      `[v7-result-bridge] Cycle complete: ${processed} processed, ${failed} failed, ${duration}ms`
    );

    return {
      status: failed > 0 ? "partial" : "success",
      processed,
      failed,
      receipts,
      duration_ms: duration,
    };
  } catch (error) {
    console.error(`[v7-result-bridge] Fatal error: ${error}`);
    return {
      status: "error",
      error: (error as Error).message,
      processed: 0,
      failed: 0,
      receipts: [],
      duration_ms: Date.now() - startTime,
    };
  }
}

function mapEventTypeToTaskStatus(eventType: string): string {
  const mapping: Record<string, string> = {
    completed: "completed",
    blocked: "blocked",
    needs_review: "needs_review",
    error: "needs_review",
    handoff_ready: "handoff_ready",
  };
  return mapping[eventType] || "needs_review";
}

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const result = await processPendingResults();

  return new Response(JSON.stringify(result), {
    headers: { "Content-Type": "application/json" },
    status: result.status === "error" ? 500 : 200,
  });
});
