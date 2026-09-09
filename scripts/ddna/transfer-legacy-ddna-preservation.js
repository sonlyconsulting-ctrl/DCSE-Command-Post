#!/usr/bin/env node

const { execFileSync } = require("child_process");
const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");

const repoRoot = path.resolve(__dirname, "../..");
const taskId = "DCSE-RCHE-20260909-EMP-HARVEST-001";
const subtaskId = "DCSE-DDNA-PHYSICAL-TRANSFER-20260909-001";
const sourceProjectId = "nevgdyfpxdaloacuutal";
const destinationProjectId = "uutpzaiqymyufljdgdaa";
const sourceSchema = "dcse_cp";
const destinationSchema = "dcse_ddna_legacy";
const startedAt = new Date().toISOString();

const sourceWorkdir =
  process.env.DCSE_DDNA_SOURCE_SUPABASE_WORKDIR ||
  path.join(repoRoot, "..", "supabase-ddna-transfer-cli", "source");
const destinationWorkdir =
  process.env.DCSE_DDNA_DEST_SUPABASE_WORKDIR ||
  path.join(repoRoot, "..", "supabase-ddna-transfer-cli", "dest");

const implementationDir = path.join(repoRoot, "governance", "v7.2", "implementations");
const receiptPath = path.join(implementationDir, "DCSE_DDNA_PHYSICAL_TRANSFER_RECEIPT_20260909.md");
const manifestPath = path.join(implementationDir, "DCSE_DDNA_PHYSICAL_TRANSFER_MANIFEST_20260909.json");
const validationPath = path.join(implementationDir, "DCSE_DDNA_PHYSICAL_TRANSFER_VALIDATION_20260909.json");

const tables = {
  ddna_source_queue: {
    expectedCount: 129,
    columns: [
      ["id", "uuid"],
      ["source_type", "text"],
      ["source_ref_id", "text"],
      ["source_title", "text"],
      ["entity", "text"],
      ["lane", "text"],
      ["priority", "integer"],
      ["status", "text"],
      ["assigned_model", "text"],
      ["assigned_agent_key", "text"],
      ["extraction_run_id", "uuid"],
      ["ps_lock", "boolean"],
      ["public_safe", "boolean"],
      ["queued_by", "text"],
      ["queued_at", "timestamptz"],
      ["extracted_at", "timestamptz"],
      ["notes", "text"],
      ["metadata", "jsonb"],
      ["retry_count", "integer"],
      ["max_retries", "integer"],
      ["last_error", "text"],
      ["batch_id", "text"],
      ["content_snapshot", "text"],
    ],
  },
  ddna_ollama_jobs: {
    expectedCount: 40,
    columns: [
      ["id", "uuid"],
      ["job_key", "text"],
      ["source_queue_id", "uuid"],
      ["model_id", "text"],
      ["provider", "text"],
      ["endpoint", "text"],
      ["prompt_template", "text"],
      ["raw_output", "text"],
      ["parsed_output", "jsonb"],
      ["characteristics_extracted", "integer"],
      ["status", "text"],
      ["error_message", "text"],
      ["tokens_used", "integer"],
      ["duration_ms", "integer"],
      ["ps_lock", "boolean"],
      ["output_provenance_logged", "boolean"],
      ["artifact_ref_id", "uuid"],
      ["started_at", "timestamptz"],
      ["completed_at", "timestamptz"],
      ["created_at", "timestamptz"],
      ["batch_id", "text"],
      ["retry_count", "integer"],
      ["model_version", "text"],
      ["prompt_tokens_est", "integer"],
    ],
  },
};

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function stable(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(stable).join(",")}]`;
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${stable(value[key])}`)
    .join(",")}}`;
}

function rowFingerprint(row) {
  return sha256(stable(row));
}

function aggregateFingerprint(rowHashes) {
  return sha256(rowHashes.map((r) => `${r.id}:${r.hash}`).join("\n"));
}

function parseCliJson(stdout) {
  const text = stdout.toString("utf8").trim();
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start === -1 || end === -1 || end <= start) {
    throw new Error(`Supabase CLI did not return JSON. Output length: ${text.length}`);
  }
  return JSON.parse(text.slice(start, end + 1));
}

function sleepMs(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

function withRetry(label, fn) {
  const maxAttempts = 4;
  let lastError;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      return fn();
    } catch (error) {
      lastError = error;
      const message = String(error.stderr || error.message || error);
      const transient =
        message.includes("GOAWAY") ||
        message.includes("closed the connection") ||
        message.includes("ECONNRESET") ||
        message.includes("ETIMEDOUT") ||
        message.includes("429") ||
        message.includes("503");
      if (!transient || attempt === maxAttempts) {
        break;
      }
      console.error(`${label} transient failure on attempt ${attempt}; retrying.`);
      sleepMs(1000 * attempt);
    }
  }
  throw lastError;
}

function supabaseQuery(workdir, sql) {
  const stdout = withRetry(
    "supabase db query",
    () =>
      execFileSync(
        "supabase",
        ["db", "query", "--workdir", workdir, "--linked", "-o", "json", sql],
        { encoding: "utf8", maxBuffer: 1024 * 1024 * 80 }
      )
  );
  const parsed = parseCliJson(stdout);
  return parsed.rows || [];
}

function supabaseQueryFile(workdir, sql) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "dcse-ddna-transfer-"));
  const file = path.join(tmpDir, "query.sql");
  fs.writeFileSync(file, sql);
  try {
    const stdout = withRetry(
      "supabase db query file",
      () =>
        execFileSync(
          "supabase",
          ["db", "query", "--workdir", workdir, "--linked", "-o", "json", "-f", file],
          { encoding: "utf8", maxBuffer: 1024 * 1024 * 80 }
        )
    );
    const parsed = parseCliJson(stdout);
    return parsed.rows || [];
  } finally {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

function advisor(workdir, type) {
  try {
    const stdout = execFileSync(
      "supabase",
      ["db", "advisors", "--workdir", workdir, "--linked", "--type", type, "--level", "warn", "--fail-on", "none", "-o", "json"],
      { encoding: "utf8", maxBuffer: 1024 * 1024 * 20 }
    );
    const parsed = parseCliJson(stdout);
    return Array.isArray(parsed) ? parsed : parsed.rows || parsed.advisors || [];
  } catch (error) {
    return [{ status: "ADVISOR_COMMAND_FAILED", message: String(error.message || error) }];
  }
}

function tableSchema(projectWorkdir, schemaName, tableName) {
  return supabaseQuery(
    projectWorkdir,
    `select table_schema, table_name, column_name, ordinal_position, data_type, is_nullable, column_default
     from information_schema.columns
     where table_schema = '${schemaName}' and table_name = '${tableName}'
     order by ordinal_position;`
  );
}

function tableConstraints(projectWorkdir, schemaName, tableName) {
  return supabaseQuery(
    projectWorkdir,
    `select tc.table_schema, tc.table_name, tc.constraint_name, tc.constraint_type,
            coalesce(array_agg(kcu.column_name order by kcu.ordinal_position) filter (where kcu.column_name is not null), '{}') as columns
     from information_schema.table_constraints tc
     left join information_schema.key_column_usage kcu
       on kcu.constraint_schema = tc.constraint_schema
      and kcu.constraint_name = tc.constraint_name
      and kcu.table_schema = tc.table_schema
      and kcu.table_name = tc.table_name
     where tc.table_schema = '${schemaName}' and tc.table_name = '${tableName}'
     group by tc.table_schema, tc.table_name, tc.constraint_name, tc.constraint_type
     order by tc.constraint_type, tc.constraint_name;`
  );
}

function getRows(workdir, schemaName, tableName) {
  return supabaseQuery(
    workdir,
    `select to_jsonb(t) as row from ${schemaName}.${tableName} t order by id;`
  ).map((r) => r.row);
}

function assertNoFirewallHits() {
  const rows = supabaseQuery(
    sourceWorkdir,
    `with checks as (
       select 'ddna_source_queue'::text as table_name,
         count(*)::int as row_count,
         count(*) filter (where ps_lock)::int as ps_locked_count,
         count(*) filter (where coalesce(content_snapshot,'') ~* '(PS_WIN|protected legal|litigation facts|case strategy|attorney strategy|deposition|docket|case no)')::int as ps_pattern_count,
         count(*) filter (where coalesce(content_snapshot,'') ~* '(sk-[A-Za-z0-9_-]{20,}|service[_-]?role|api[_-]?key|password|private key|connection string|mfa|recovery code)')::int as secret_pattern_count
       from dcse_cp.ddna_source_queue
       union all
       select 'ddna_ollama_jobs'::text as table_name,
         count(*)::int as row_count,
         count(*) filter (where ps_lock)::int as ps_locked_count,
         count(*) filter (where coalesce(prompt_template,'') || ' ' || coalesce(raw_output,'') || ' ' || coalesce(error_message,'') || ' ' || coalesce(parsed_output::text,'') ~* '(PS_WIN|protected legal|litigation facts|case strategy|attorney strategy|deposition|docket|case no)')::int as ps_pattern_count,
         count(*) filter (where coalesce(prompt_template,'') || ' ' || coalesce(raw_output,'') || ' ' || coalesce(error_message,'') || ' ' || coalesce(parsed_output::text,'') ~* '(sk-[A-Za-z0-9_-]{20,}|service[_-]?role|api[_-]?key|password|private key|connection string|mfa|recovery code)')::int as secret_pattern_count
       from dcse_cp.ddna_ollama_jobs
     )
     select * from checks order by table_name;`
  );

  for (const row of rows) {
    if (row.ps_locked_count || row.ps_pattern_count || row.secret_pattern_count) {
      throw new Error(`Firewall scan failed for ${row.table_name}: ${JSON.stringify(row)}`);
    }
  }
  return rows;
}

function insertRows(tableName, rows) {
  if (!rows.length) return { inserted_or_present: 0 };
  const config = tables[tableName];
  const columnList = config.columns.map(([name]) => name).join(", ");
  const recordTypes = config.columns.map(([name, type]) => `${name} ${type}`).join(", ");
  const selectList = config.columns.map(([name]) => name).join(", ");
  const payload = Buffer.from(JSON.stringify(rows), "utf8").toString("base64");

  const sql = `
with payload as (
  select convert_from(decode($$${payload}$$, 'base64'), 'UTF8')::jsonb as rows
), incoming as (
  select * from jsonb_to_recordset((select rows from payload)) as x (${recordTypes})
), inserted as (
  insert into ${destinationSchema}.${tableName} (${columnList})
  select ${selectList}
  from incoming
  on conflict (id) do nothing
  returning id
)
select
  (select count(*)::int from incoming) as incoming_count,
  (select count(*)::int from inserted) as inserted_count,
  (select count(*)::int from ${destinationSchema}.${tableName}) as destination_count;`;

  return supabaseQueryFile(destinationWorkdir, sql)[0];
}

function insertProvenance(tableName, rowHashes) {
  if (!rowHashes.length) return { inserted_or_present: 0 };
  const rows = rowHashes.map((r) => ({
    origin_event_id: subtaskId,
    source_key: `${sourceProjectId}:${sourceSchema}.${tableName}:${r.id}`,
    copied_to: `${destinationProjectId}:${destinationSchema}.${tableName}:${r.id}`,
    relationship_type: "exact_physical_legacy_preservation",
    metadata: {
      task_id: taskId,
      subtask_id: subtaskId,
      source_project_id: sourceProjectId,
      source_schema: sourceSchema,
      source_table: tableName,
      source_key: r.id,
      destination_project_id: destinationProjectId,
      destination_schema: destinationSchema,
      destination_table: tableName,
      destination_key: r.id,
      row_sha256: r.hash,
      copied_at: startedAt,
      authority_status: "legacy_preservation_not_promotion",
    },
  }));
  const payload = Buffer.from(JSON.stringify(rows), "utf8").toString("base64");
  const sql = `
with payload as (
  select convert_from(decode($$${payload}$$, 'base64'), 'UTF8')::jsonb as rows
), incoming as (
  select * from jsonb_to_recordset((select rows from payload)) as x (
    origin_event_id text,
    source_key text,
    copied_to text,
    relationship_type text,
    metadata jsonb
  )
), inserted as (
  insert into dcse_ddna.provenance_links (origin_event_id, source_key, copied_to, relationship_type, metadata)
  select origin_event_id, source_key, copied_to, relationship_type, metadata
  from incoming i
  where not exists (
    select 1 from dcse_ddna.provenance_links p
    where p.origin_event_id = i.origin_event_id
      and p.source_key = i.source_key
      and p.copied_to = i.copied_to
      and p.relationship_type = i.relationship_type
  )
  returning id
)
select
  (select count(*)::int from incoming) as incoming_count,
  (select count(*)::int from inserted) as inserted_count,
  (select count(*)::int from dcse_ddna.provenance_links where origin_event_id = '${subtaskId}' and relationship_type = 'exact_physical_legacy_preservation') as provenance_count;`;
  return supabaseQueryFile(destinationWorkdir, sql)[0];
}

function countCopyEventProvenance() {
  return supabaseQuery(
    destinationWorkdir,
    `select count(*)::int as provenance_count
     from dcse_ddna.provenance_links
     where origin_event_id = '${subtaskId}'
       and relationship_type = 'exact_physical_legacy_preservation';`
  )[0].provenance_count;
}

function compareRows(tableName, sourceRows, destinationRows) {
  const sourceMap = new Map(sourceRows.map((r) => [r.id, r]));
  const destinationMap = new Map(destinationRows.map((r) => [r.id, r]));
  const sourceHashes = sourceRows.map((r) => ({ id: r.id, hash: rowFingerprint(r) })).sort((a, b) => a.id.localeCompare(b.id));
  const destinationHashes = destinationRows.map((r) => ({ id: r.id, hash: rowFingerprint(r) })).sort((a, b) => a.id.localeCompare(b.id));
  const missing = [];
  const extra = [];
  const mismatched = [];

  for (const [id, src] of sourceMap) {
    const dst = destinationMap.get(id);
    if (!dst) missing.push(id);
    else if (rowFingerprint(src) !== rowFingerprint(dst)) mismatched.push(id);
  }
  for (const id of destinationMap.keys()) {
    if (!sourceMap.has(id)) extra.push(id);
  }

  return {
    table_name: tableName,
    source_count: sourceRows.length,
    destination_count: destinationRows.length,
    expected_count: tables[tableName].expectedCount,
    missing_count: missing.length,
    extra_count: extra.length,
    mismatched_count: mismatched.length,
    source_aggregate_sha256: aggregateFingerprint(sourceHashes),
    destination_aggregate_sha256: aggregateFingerprint(destinationHashes),
    aggregate_match: aggregateFingerprint(sourceHashes) === aggregateFingerprint(destinationHashes),
    per_row_match: missing.length === 0 && extra.length === 0 && mismatched.length === 0,
    row_fingerprints: sourceHashes,
  };
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + "\n");
}

function writeReceipt(summary) {
  const tableLines = summary.tables
    .map(
      (t) => `| ${t.table_name} | ${t.source_count} | ${t.destination_count} | ${t.per_row_match ? "PASS" : "FAIL"} | ${t.aggregate_match ? "PASS" : "FAIL"} | ${t.source_aggregate_sha256} |`
    )
    .join("\n");

  const md = `# DCSE-DDNA Physical Legacy Transfer Receipt

**Parent Task ID:** ${taskId}
**Subtask:** ${subtaskId}
**Status:** ${summary.final_status}
**Started:** ${summary.started_at}
**Completed:** ${summary.completed_at}

## Scope

This receipt records the exact physical preservation transfer requested in GitHub Issue #65 for PR #64. The source project was \`${sourceProjectId}\` / \`${sourceSchema}\`; the destination project was \`${destinationProjectId}\` / \`${destinationSchema}\`.

No source rows were deleted or mutated. No consumer cutover was performed. No rule, source, or runtime record is promoted to governing authority by this transfer.

## Transfer Counts

| Table | Source rows | Destination rows | Per-row equivalence | Aggregate fingerprint | Source aggregate SHA-256 |
| --- | ---: | ---: | --- | --- | --- |
${tableLines}

## Provenance

Per-row provenance links were recorded in \`dcse_ddna.provenance_links\` with source project, source schema/table, source key, copy event, destination project, destination schema/table, destination key, and row fingerprint metadata.

Provenance link count for this copy event: ${summary.provenance_count}

## Safety Checks

- PS lock scan: ${summary.ps_scan_result}
- Secret pattern scan: ${summary.secret_scan_result}
- Source post-transfer fingerprint check: ${summary.source_post_transfer_check}
- Consumer cutover: NOT PERFORMED
- Source mutation: NOT PERFORMED
- PR merge: NOT PERFORMED

## Advisor Review

Destination security advisor result count at warning level or above: ${summary.advisor_security_count}
Destination performance advisor result count at warning level or above: ${summary.advisor_performance_count}

Advisor findings are recorded in the validation JSON. Inherited findings outside the transfer scope were not remediated in this task.

## Final Status

${summary.final_status}

Structure Precedes Scale.
`;
  fs.writeFileSync(receiptPath, md);
}

function main() {
  const sourceProjects = supabaseQuery(sourceWorkdir, "select current_database() as database_name, current_user as execution_role;");
  const destinationProjects = supabaseQuery(destinationWorkdir, "select current_database() as database_name, current_user as execution_role;");
  const firewallRows = assertNoFirewallHits();

  const manifest = {
    task_id: taskId,
    subtask_id: subtaskId,
    source_project_id: sourceProjectId,
    destination_project_id: destinationProjectId,
    generated_at: startedAt,
    source_execution: sourceProjects[0],
    destination_execution: destinationProjects[0],
    tables: {},
  };

  const summaryTables = [];
  const expectedProvenanceCount = Object.values(tables).reduce((sum, table) => sum + table.expectedCount, 0);
  const provenanceInsertResults = {};
  const sourceBefore = {};
  const sourceAfter = {};

  for (const tableName of Object.keys(tables)) {
    const sourceSchemaRows = tableSchema(sourceWorkdir, sourceSchema, tableName);
    const destinationSchemaRows = tableSchema(destinationWorkdir, destinationSchema, tableName);
    const sourceConstraints = tableConstraints(sourceWorkdir, sourceSchema, tableName);
    const destinationConstraints = tableConstraints(destinationWorkdir, destinationSchema, tableName);

    const sourceRows = getRows(sourceWorkdir, sourceSchema, tableName);
    const beforeHashes = sourceRows.map((r) => ({ id: r.id, hash: rowFingerprint(r) })).sort((a, b) => a.id.localeCompare(b.id));
    sourceBefore[tableName] = aggregateFingerprint(beforeHashes);

    const destinationBefore = getRows(destinationWorkdir, destinationSchema, tableName);
    const comparisonBefore = compareRows(tableName, sourceRows, destinationBefore);
    if (destinationBefore.length > 0 && !comparisonBefore.per_row_match) {
      const existingIds = new Set(destinationBefore.map((r) => r.id));
      const overlappingSource = sourceRows.filter((r) => existingIds.has(r.id));
      const overlappingDestination = destinationBefore.filter((r) => existingIds.has(r.id));
      if (!compareRows(tableName, overlappingSource, overlappingDestination).per_row_match) {
        throw new Error(`Destination ${tableName} has pre-existing mismatched rows. Stop before overwrite.`);
      }
    }

    const insertResult = insertRows(tableName, sourceRows);
    const destinationRows = getRows(destinationWorkdir, destinationSchema, tableName);
    const comparison = compareRows(tableName, sourceRows, destinationRows);
    const provenanceResult = insertProvenance(tableName, comparison.row_fingerprints);
    provenanceInsertResults[tableName] = provenanceResult;

    const sourceRowsPost = getRows(sourceWorkdir, sourceSchema, tableName);
    const afterHashes = sourceRowsPost.map((r) => ({ id: r.id, hash: rowFingerprint(r) })).sort((a, b) => a.id.localeCompare(b.id));
    sourceAfter[tableName] = aggregateFingerprint(afterHashes);

    manifest.tables[tableName] = {
      source_table: `${sourceSchema}.${tableName}`,
      destination_table: `${destinationSchema}.${tableName}`,
      source_row_count: sourceRows.length,
      destination_pre_transfer_count: destinationBefore.length,
      destination_post_transfer_count: destinationRows.length,
      inserted_count: insertResult.inserted_count,
      ordered_source_columns: sourceSchemaRows.map((r) => r.column_name),
      ordered_destination_columns: destinationSchemaRows.map((r) => r.column_name),
      source_columns: sourceSchemaRows,
      destination_columns: destinationSchemaRows,
      source_constraints: sourceConstraints,
      destination_constraints: destinationConstraints,
      mapping: tables[tableName].columns.map(([column]) => ({
        source: `${sourceSchema}.${tableName}.${column}`,
        destination: `${destinationSchema}.${tableName}.${column}`,
        transform: column === "lane" ? "enum label preserved as text" : "identity",
      })),
    };
    summaryTables.push(comparison);
  }

  const securityAdvisors = advisor(destinationWorkdir, "security");
  const performanceAdvisors = advisor(destinationWorkdir, "performance");
  const provenanceCount = countCopyEventProvenance();
  const completedAt = new Date().toISOString();
  const finalStatus =
    summaryTables.every(
      (t) =>
        t.source_count === t.expected_count &&
        t.destination_count === t.expected_count &&
        t.per_row_match &&
        t.aggregate_match
    ) &&
    Object.keys(sourceBefore).every((tableName) => sourceBefore[tableName] === sourceAfter[tableName]) &&
    provenanceCount === expectedProvenanceCount
      ? "COMPLETE"
      : "PARTIAL";

  const validation = {
    task_id: taskId,
    subtask_id: subtaskId,
    final_status: finalStatus,
    started_at: startedAt,
    completed_at: completedAt,
    source_project_id: sourceProjectId,
    destination_project_id: destinationProjectId,
    source_post_transfer_fingerprints_match: Object.keys(sourceBefore).every((tableName) => sourceBefore[tableName] === sourceAfter[tableName]),
    firewall_scan: firewallRows,
    tables: summaryTables,
    provenance_count: provenanceCount,
    expected_provenance_count: expectedProvenanceCount,
    provenance_insert_results: provenanceInsertResults,
    duplicate_reconciliation: {
      normalized_duplicate_check: "Preservation rows inserted into dcse_ddna_legacy only; normalized dcse_ddna records not duplicated.",
      legacy_snapshot_boundary: "Existing snapshots remain historical evidence; exact rows now exist in compatibility preservation tables.",
    },
    advisor_review: {
      security: securityAdvisors,
      performance: performanceAdvisors,
    },
    release_boundaries: {
      source_mutation: "NOT_PERFORMED",
      consumer_cutover: "NOT_PERFORMED",
      pr_merge: "NOT_PERFORMED",
      authority_promotion: "NOT_PERFORMED",
    },
  };

  const summary = {
    final_status: finalStatus,
    started_at: startedAt,
    completed_at: completedAt,
    tables: summaryTables,
    provenance_count: provenanceCount,
    ps_scan_result: firewallRows.every((r) => r.ps_locked_count === 0 && r.ps_pattern_count === 0) ? "PASS_NONE_DETECTED" : "FAIL",
    secret_scan_result: firewallRows.every((r) => r.secret_pattern_count === 0) ? "PASS_NONE_DETECTED" : "FAIL",
    source_post_transfer_check: validation.source_post_transfer_fingerprints_match ? "PASS" : "FAIL",
    advisor_security_count: Array.isArray(securityAdvisors) ? securityAdvisors.length : 0,
    advisor_performance_count: Array.isArray(performanceAdvisors) ? performanceAdvisors.length : 0,
  };

  writeJson(manifestPath, manifest);
  writeJson(validationPath, validation);
  writeReceipt(summary);

  console.log(
    JSON.stringify(
      {
        task_id: taskId,
        subtask_id: subtaskId,
        final_status: finalStatus,
        tables: summaryTables.map((t) => ({
          table_name: t.table_name,
          source_count: t.source_count,
          destination_count: t.destination_count,
          per_row_match: t.per_row_match,
          aggregate_match: t.aggregate_match,
          aggregate_sha256: t.source_aggregate_sha256,
        })),
        provenance_count: provenanceCount,
        receipt: receiptPath,
        manifest: manifestPath,
        validation: validationPath,
      },
      null,
      2
    )
  );

  if (finalStatus !== "COMPLETE") {
    process.exitCode = 1;
  }
}

main();
