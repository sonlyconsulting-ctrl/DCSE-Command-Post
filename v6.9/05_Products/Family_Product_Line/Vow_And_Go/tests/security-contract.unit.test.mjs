import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = resolve(appRoot, "..", "..", "..", "..");
const migrationPath = resolve(repoRoot, "supabase", "migrations", "20260716224000_vow_go_public_rpc_preview_v1.sql");
const repairMigrationPath = resolve(repoRoot, "supabase", "migrations", "20260716224258_vow_go_major_repair_v2.sql");

test("client contains no service-role secret and uses public RPCs", async () => {
  const [config, client] = await Promise.all([
    readFile(resolve(appRoot, "config.js"), "utf8"),
    readFile(resolve(appRoot, "vow-go-supabase.js"), "utf8")
  ]);
  assert.doesNotMatch(`${config}\n${client}`, /service[_-]?role/i);
  assert.match(config, /sb_publishable_/);
  assert.doesNotMatch(client, /\.schema\(["']family_/);
  assert.match(client, /\.rpc\(config\.engagementsRpc/);
  assert.match(client, /\.rpc\(config\.engagementContextRpc/);
  assert.match(client, /\.rpc\(config\.recordActionRpc/);
});

test("repair migration enforces engagement-scoped CRUD, invitation hashes, and template privacy", async () => {
  const sql = await readFile(repairMigrationPath, "utf8");
  assert.match(sql, /workspace_records_product_collection_active_idx/i);
  assert.match(sql, /family_core\.is_product_member\(v_product_id\)/i);
  assert.match(sql, /token_hash text not null unique/i);
  assert.match(sql, /check \(not \(template_data \?\|/i);
  assert.match(sql, /security invoker/i);
  assert.doesNotMatch(sql, /grant .* to anon/i);
});

test("migration keeps product identity server-derived and Storage private", async () => {
  const sql = await readFile(migrationPath, "utf8");
  assert.match(sql, /create or replace function public\.vow_go_context\(\)/i);
  assert.match(sql, /create or replace function public\.vow_go_action\(\s*p_action text,\s*p_payload jsonb/i);
  assert.doesNotMatch(sql, /create or replace function public\.vow_go_action\([\s\S]*?p_product_instance_id[\s\S]*?\)\s*returns/i);
  assert.match(sql, /security invoker/i);
  assert.match(sql, /revoke execute on function public\.vow_go_context\(\) from public, anon/i);
  assert.match(sql, /family-wedding-private/);
  assert.match(sql, /public\s*=\s*false/i);
  assert.doesNotMatch(sql, /grant .*family_vow_go.* to anon/i);
});

test("Windows launcher resolves its own folder and provides a Node fallback", async () => {
  const launcher = await readFile(resolve(appRoot, "START_VOW_AND_GO.ps1"), "utf8");
  assert.match(launcher, /MyInvocation\.MyCommand\.Path/);
  assert.match(launcher, /Set-Location -LiteralPath \$appRoot/);
  assert.match(launcher, /Python is unavailable/);
  assert.match(launcher, /static-server\.mjs/);
  assert.match(launcher, /Start-Process \$url/);
  assert.match(launcher, /\$pythonCommand = @\(Get-PythonCommand\)/);
});
