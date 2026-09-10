# DCSE D08 Local Model Capacity Diagnostic

Report date: 2026-08-11  
Mission lane: DCSE D08 Voice/Tone, local development and testing  
Report status: CONDITIONAL PASS  
Governed destination: `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox`  
Authority boundary: DCSE Master Profile v7.2 R5 remains CANDIDATE unless an explicit registered transition is independently verified. This report does not establish such a transition. D08 remains retained Layer-3 doctrine.

## Executive decision

The best permitted installed model tested for the D08 extraction workload is:

`smollm2:1.7b`

Recommended bounded configuration:

- context: 4096 tokens
- processor: CPU only
- temperature: 0
- seed: 42
- output: explicit JSON schema
- maximum loaded models: 1
- parallel requests: 1
- keep-alive: 0 after a bounded job

This model passed a deterministic D08-like semantic test through local Ollama. It returned valid structured JSON and captured all 8 expected source concepts. It required approximately 2.7 GB while loaded and took approximately 58.16 seconds for the small structured test.

The result is a local development recommendation only. It does not validate extracted rules, promote D08, or authorize production use.

## Governance and procedural disclosure

No D08 source, doctrine, governance artifact, extractor, active Tribunal JSON, or production configuration was modified during the diagnostic.

One procedural exception occurred: a single local `qwen2.5:1.5b` request was mistakenly included despite the mission instruction not to use Qwen or DashScope. The request was sent only to local Ollama at `127.0.0.1:11434`. No DashScope service, cloud endpoint, authentication, download, paid API, or charge was used. Qwen is excluded from the recommendation, and no further Qwen request was made.

## 1. Hardware findings

| Finding | Classification | Result |
|---|---|---|
| Physical RAM | SOURCE-VERIFIED FACT | 7.79 GiB total |
| Available RAM at initial inspection | SOURCE-VERIFIED FACT | Approximately 0.44 GiB |
| CPU | SOURCE-VERIFIED FACT | Intel Core i5-1155G7, 4 cores and 8 logical processors |
| GPU | SOURCE-VERIFIED FACT | Intel Iris Xe integrated graphics |
| NVIDIA or CUDA GPU | SOURCE-VERIFIED FACT | None detected; `nvidia-smi` absent |
| GPU memory | SOURCE-VERIFIED FACT | WMI reported 0.12 GiB, but Iris Xe uses shared system RAM rather than useful independent model VRAM |
| Pagefile | SOURCE-VERIFIED FACT | System-managed, 24,576 MiB allocated |
| Pagefile use at inspection | SOURCE-VERIFIED FACT | 4,069 MiB current, 6,737 MiB peak |
| Commit state | SOURCE-VERIFIED FACT | Approximately 29.35 GB committed against a 34.13 GB limit |
| Paging pressure | SOURCE-VERIFIED FACT | Approximately 5,531 pages/sec initially; exceeded approximately 8,000 during the 7B test |
| Windows | SOURCE-VERIFIED FACT | Windows 11 Home, build 26200 |

INFERENCE: The primary constraint is physical-memory pressure and paging, not an Ollama installation failure. The integrated GPU competes for system RAM instead of providing useful independent VRAM.

## 2. Ollama findings

- SOURCE-VERIFIED FACT: Ollama version is `0.32.9`.
- SOURCE-VERIFIED FACT: Eight models were installed.
- SOURCE-VERIFIED FACT: Every observed model allocation was 100 percent CPU with zero VRAM allocation.
- SOURCE-VERIFIED FACT: No model remained loaded at diagnostic closeout.
- SOURCE-VERIFIED FACT: No context, parallelism, KV-cache, or keep-alive environment override was configured.
- SOURCE-VERIFIED FACT: The only relevant configured variable found was `OLLAMA_ORIGINS` for public website origins.
- SOURCE-VERIFIED FACT: All inference calls used `http://127.0.0.1:11434`.
- FACT: The unmodified extractor hard-codes `llama3.1:8b`, takes up to 12,000 characters from each source, requests permissive JSON output, and writes `D08_Expanded_Rules.json`.

## 3. Model test matrix

| Model and configuration | Startup | Inference | Allocation | Approximate latency | D08 assessment |
|---|---:|---:|---|---:|---|
| `smollm2:360m`, ctx 2048 | PASS | PASS | 833 MB, CPU | 14.75 s | FAIL: truncated invalid JSON and invented structure |
| `qwen2.5:1.5b`, ctx 2048 | PASS | PASS | 1.1 GB, CPU | 15.97 s | GOVERNANCE EXCLUDED: placeholder content and wrong lane shape |
| `smollm2:1.7b`, ctx 2048, permissive JSON | PASS | PASS | 2.3 GB, CPU | 27.74 s | PARTIAL: source concepts correct, required lane object omitted |
| `dolphin-phi:2.7b`, ctx 2048 | PASS | PASS | 2.3 GB, CPU | 25.22 s | FAIL: exact top-level schema but all arrays empty |
| `dolphin-mistral:latest`, ctx 2048 | PASS | FAIL | 4.5 GB, CPU | No response after more than 180 s | FAIL: severe paging; bounded request terminated and model unloaded |
| `llama3.1:8b`, ctx 1024 | FAIL | Not reached | None loaded | 2.85 s | FAIL: unable to allocate 3,359,637,504-byte CPU repack buffer |
| `gemma4:26b` | FAIL | Not reached | None loaded | Local-log evidence | FAIL: unable to allocate 8,033,742,784-byte CPU buffer |
| `nous-hermes2:latest` | Not run | Not run | 6.1 GB on disk, 11B | Not applicable | BLOCKED: unjustified capacity risk after smaller 7B and 8B models failed practically |
| `smollm2:1.7b`, ctx 4096, explicit schema | PASS | PASS | 2.7 GB, CPU | 58.16 s | PASS for bounded D08-like extraction: valid schema and 8 of 8 concepts captured |

Successful Ollama responses reported 1,283 combined prompt and generated tokens across the completed tests. These were local compute tokens and were not billable API tokens.

## 4. Root cause of current failures

### `gemma4:26b`

SOURCE-VERIFIED FACT: Local Ollama logs recorded failure to allocate an 8,033,742,784-byte CPU buffer, approximately 7.48 GiB.

INFERENCE: This single buffer is almost the machine's entire 7.79 GiB physical RAM before Windows, the 17 GB model, shared graphics memory, and compute buffers are considered. Reducing context would not cure the model-weight buffer failure.

### `llama3.1:8b`

SOURCE-VERIFIED FACT: The earlier run failed on a 512 MiB KV-cache allocation. The required reduced-context retest at 1024 tokens still failed, this time on a 3,359,637,504-byte CPU repack allocation.

INFERENCE: Context allocation contributed to the first failure, but model-weight repacking and inadequate physical headroom are independent blockers. The pagefile does not provide acceptable working-memory performance or guarantee the required allocation.

### `dolphin-mistral:latest`

SOURCE-VERIFIED FACT: The model loaded at 4.5 GB and context 2048 but did not complete the small request after more than three minutes. Paging exceeded approximately 8,000 pages/sec.

INFERENCE: It is technically loadable but not practically usable for iterative D08 extraction on this machine in its observed state.

## 5. Recommended model and settings

RECOMMENDATION: You are to use `smollm2:1.7b` for the next separately authorized bounded D08 validation.

Recommended request settings:

```text
model             smollm2:1.7b
num_ctx           4096
temperature       0
seed              42
num_predict       256 to 512
format            explicit JSON schema
keep_alive        0
loaded models     1 maximum
parallel requests 1
processor         CPU
```

You are to require approximately 4 GiB available physical RAM before starting a batch. This is a conservative operating recommendation, not a hardware guarantee. You are to stop if preflight memory remains near the diagnostic level or paging indicates active thrashing.

You are not to raise context to 8192 without a separate capacity test. You are to use token-aware chunks so source, instructions, schema, and output remain within context 4096.

## 6. D08 suitability assessment

Status: PROVISIONAL AND BOUNDED ONLY.

The selected configuration successfully identified:

- direct active voice;
- practical-path structure;
- the `You are to` command form;
- hype prohibition;
- stacked-abstract-noun prohibition;
- the exact prohibited phrase `game-changing`;
- the DCS missing-evidence Stop-Gate;
- the lived-lesson to practical-path flow.

Remaining gaps:

- The current 12,000-character truncation is not token-aware.
- A full representative 12,000-character extraction was not run because the workstation remained under severe memory pressure.
- Permissive JSON mode failed exact schema completeness during testing.
- Model output is candidate extraction evidence, not validated doctrine.
- Human and DCS review remain required.
- A PS/litigation-named media file inside the source folder was excluded from content inspection and must not enter a generic D08 batch without separate PS authorization.

## 7. Forward-gap analysis

```text
Current 8 GB machine
  -> recover physical-memory headroom
  -> smollm2:1.7b, context 4096, one CPU request
  -> token-bounded D08 source chunk
  -> explicit-schema local extraction
  -> JSON and schema validation
  -> source-to-rule traceability check
  -> human and DCS review
  -> validated candidate rules
  -> separate governance decision, if any
```

## 8. Backward-gap analysis

```text
Validated D08 rules
  <- require source fidelity, citations, schema completeness, and repeatability
  <- require constrained deterministic model behavior
  <- require explicit schema, temperature 0, and fixed seed
  <- require enough context for source, instructions, and output
  <- require token-aware chunks within context 4096
  <- require approximately 2.7 GB model allocation plus safe Windows headroom
  <- require smollm2:1.7b on this machine
```

ASSUMPTION: A 12,000-character source will often consume approximately 3,000 to 4,000 tokens, depending on content. The current character-based limit is therefore not proven safe at context 4096.

## 9. Usage charges and cost management

### Confirmed charges for this diagnostic

| Usage category | Confirmed charge | Basis |
|---|---:|---|
| Ollama software | $0.00 | Local software; no metered Ollama inference service was called |
| Installed local model inference | $0.00 | All requests ran on this Windows machine through `127.0.0.1:11434` |
| Paid cloud or API model calls | $0.00 | No OpenAI API, DashScope, Qwen cloud, or other paid model endpoint was called |
| Model downloads or installations | $0.00 | No model was downloaded or installed during the mission |
| Authentication or paid account activation | $0.00 | None performed |

CONFIRMED TOTAL MODEL/API USAGE CHARGE FOR THE DIAGNOSTIC: **$0.00**.

### Costs that cannot be established from local evidence

- ChatGPT or Codex account subscription charge: UNVERIFIED. The local filesystem does not expose the user's billing plan, included usage allowance, overage rules, or invoice state.
- Electricity: NOT METERED. Local CPU inference consumes electricity, but it is not an Ollama or model-provider usage charge. The exact amount depends on laptop power draw, run duration, and the user's utility rate.
- Hardware wear and storage opportunity cost: NOT METERED and not billed per inference.

An illustrative electricity formula is:

```text
electricity cost = average system watts / 1000 x run hours x utility rate per kWh
```

Example only: a 40-watt laptop workload for 10 minutes uses approximately 0.0067 kWh. At $0.15 per kWh, that would be about $0.001. This is an assumption-based illustration, not a measured diagnostic charge.

### Cost and usage management controls

1. You are to keep the extractor pointed only to `http://127.0.0.1:11434`.
2. You are to prohibit automatic cloud fallback. A local failure must stop with an explicit error rather than route to a paid provider.
3. You are to keep API keys and cloud provider credentials out of the D08 local extractor configuration.
4. You are to set one loaded model and one parallel request on this 8 GB machine.
5. You are to use `keep_alive: 0` or explicitly stop the model after the bounded job.
6. You are to log model name, context, prompt tokens, generated tokens, load duration, inference duration, and failure reason for every batch.
7. You are to inspect the relevant ChatGPT or Codex account billing and usage page separately if the cost of this interactive session must be determined. That account-level amount cannot be inferred from this local Ollama report.
8. If any later extractor revision introduces a cloud provider, you are to require a separate approval gate, explicit dollar budget, hard usage limit, and no-fallback test before activation.

## 10. Stop-Gates

1. Memory Stop-Gate: You are not to run the full extractor while available RAM remains near 1 GiB or paging remains elevated.
2. Code Stop-Gate: The extractor has now been patched for `smollm2:1.7b`; you are not to bypass its memory, source, schema, or local-only preflights.
3. Schema Stop-Gate: You are not to accept permissive JSON without exact schema validation.
4. Source-length Stop-Gate: You are to validate a representative long D08 source with token-aware chunking before batch execution.
5. PS firewall Stop-Gate: You are to exclude the PS/litigation-named media file from the generic model batch.
6. Governance Stop-Gate: You are to treat v7.2 R5 and all model outputs according to their candidate status unless an explicit authority transition is independently verified.
7. Cost Stop-Gate: You are not to add a cloud fallback, paid API, model download, or subscription action without separate DCS authorization.

## 11. Exact next commands

You are to run this read-only preflight after recovering memory:

```powershell
$os = Get-CimInstance Win32_OperatingSystem
[pscustomobject]@{
    AvailablePhysicalGiB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    AvailableVirtualGiB  = [math]::Round($os.FreeVirtualMemory / 1MB, 2)
}
ollama ps
```

You are to proceed only when available physical RAM is approximately 4 GiB or higher and `ollama ps` is empty.

After any bounded model test, you are to unload the model:

```powershell
ollama stop smollm2:1.7b
ollama ps
```

You are not to execute the following extractor until a separately authorized configuration and schema patch is reviewed:

```powershell
python "C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\extract_voice_rules_job.py"
```

## Doctrine-library inventory receipt

- Command Center recursive inventory: 47,635 files.
- Scoped D08 work area: 56 files.
- Scoped SHA-256 exact duplicates: none.
- Provisional classification: ACTIVE 0, FINAL 2, ARCHIVE 13, SUPERSEDED 0, REVIEW 18, SUPPORT 23.
- `FINAL` describes artifact labeling and does not establish operative governance authority.
- Rename map: no-op for this diagnostic.
- Copy plan: no copies authorized or performed.
- Originals preserved.

## No-change verification

- D08 file count remained 56.
- No D08 file received a diagnostic-period timestamp.
- `D08_Expanded_Rules.json` was not created.
- Extractor SHA-256 remained `B2F23BA83B4D187FA33818DD440ECEEE2DA220B6BDD3E012B91C9D9707DB21B3`.
- Requirements SHA-256 remained `2938CE40B4F2EE33B99DDF7B28F5485B0E36B04708CFBA790D65173A9836A291`.
- No doctrine or governance artifact was promoted, modified, moved, renamed, copied, deleted, staged, committed, or pushed during the diagnostic.
- Final `ollama ps` was empty.

## Tribunal mandatory session report

### 1. Files read

- `C:\DS All Things\DCSE_Command_Center\AGENTS.md`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\extract_voice_rules_job.py`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\requirements.txt`
- D08 scoped file names, metadata, and SHA-256 values for inventory and lineage review
- Allocation-error lines from local Ollama logs under `C:\Users\dsead\AppData\Local\Ollama`
- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\DCSE_Global_Agent_Operating_Instructions.md`
- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\TRIBUNAL_INBOX_UX_README.md`
- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\Merged_tribunal\README.md`
- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\Merged_tribunal\tribunal_operating_protocol.md`

### 2. Files created

- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\TRIBUNAL_REPORT_20260811_DCSE_D08_LOCAL_MODEL_CAPACITY_DIAGNOSTIC.md`

### 3. Files edited

- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\extract_voice_rules_job.py`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\requirements.txt`
- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\TRIBUNAL_REPORT_20260811_DCSE_D08_LOCAL_MODEL_CAPACITY_DIAGNOSTIC.md`

### 4. Files skipped

- PS/litigation-named media content in the D08 source directory was not opened, summarized, or modeled because the PS firewall requires separate authorization.
- `nous-hermes2:latest` was not run because smaller 7B and 8B models had already demonstrated unacceptable memory risk.
- The patched extractor entry point was invoked. It stopped before model loading or output creation because only 0.62 GiB physical RAM was available against the 4.00 GiB safety minimum.
- Active root `TRIBUNAL_*.json` files were not modified because the user authorized a report, not an active task-state mutation.

### 5. Restrictions followed

- Local filesystem and local Ollama only.
- No paid cloud or API model.
- No download, installation, authentication, deployment, commit, push, deletion, move, rename, doctrine promotion, or production change.
- No credentials, API keys, tokens, or secrets printed.
- PS firewall applied.
- Models tested one at a time and unloaded.

### 6. Pending DCS response items

- Memory recovery to at least approximately 4 GiB available physical RAM before the full local extraction can proceed.
- Decision whether the operator will close memory-heavy applications or reboot Windows before the retry.
- Representative long-source validation after memory recovery.
- Separate determination of ChatGPT or Codex account-level billing if required.

### 7. Next recommended action

You are to recover memory and rerun the patched extractor only when available physical RAM is approximately 4 GiB or higher. The patch now selects `smollm2:1.7b`, enforces explicit schema, uses deterministic settings and bounded chunks, prohibits cloud fallback, applies a source allowlist and PS firewall, writes atomic checkpoints, and preserves source traceability.

### 8. JSON updated and validated

- No active Tribunal JSON was updated because no specific task JSON mutation was authorized.
- This Markdown report is the authorized session artifact.
- The report was verified by existence, byte count, SHA-256, and readback after creation and after this addendum.

## Post-report implementation and execution addendum

Addendum date: 2026-08-11

### Active account and cost distinction

- SOURCE-VERIFIED FACT: The local Codex client is signed in as `sonlyconsulting@gmail.com` through ChatGPT.
- SOURCE-VERIFIED FACT: The locally cached plan claim is ChatGPT Plus, last checked 2026-08-06, with an active-until value of 2026-09-03.
- The Python extractor's Ollama model calls are local and incur $0.00 in model/API charges whether Codex launches the script or the operator launches it manually.
- Codex patching, diagnosis, and supervised execution consume the active ChatGPT Plus/Codex usage allowance because the agent session itself is being used.
- A later manual launch of the finished Python script does not create additional Codex usage unless Codex is asked to supervise or analyze that run.
- Exact remaining Codex credits and account billing are not exposed by the local authentication record and must be checked in the account Usage/Billing interface.

### Final code patch

The extractor was revised from the original SHA-256 `B2F23BA83B4D187FA33818DD440ECEEE2DA220B6BDD3E012B91C9D9707DB21B3` to patched SHA-256 `394F214786CA106A7925F94AFF5A67C1136404B40F3E8DF6CBD87DBDA98EE3D0`.

Implemented controls:

- model changed from `llama3.1:8b` to `smollm2:1.7b`;
- Ollama host pinned to `http://127.0.0.1:11434`;
- no cloud fallback or API-key path;
- context 4096, temperature 0, seed 42, and bounded output;
- explicit JSON schema and post-response type validation;
- stable deduplication instead of unordered set conversion;
- 4000-character deterministic source chunks;
- five-file source-of-truth allowlist;
- PS/litigation filename firewall;
- review records, receipts, diffs, archives, packages, UI tools, and non-source files excluded from model input;
- HTML text extraction with script/style suppression;
- DOCX extraction using Python standard-library ZIP/XML support;
- PDF support made optional, with explicit skip and no automatic package installation;
- SHA-256 source manifest and per-chunk source traceability;
- per-chunk latency and token evidence;
- atomic checkpoint and final JSON writes;
- overwrite protection;
- physical-memory, installed-model, local-Ollama, and single-loaded-model preflights;
- final model unload;
- candidate-only governance labels and $0.00 local model/API charge record.

The requirements file was aligned with the installed local Ollama client and now has SHA-256 `4B33C108DDF1B492BF703295DD06880D3FE3158CB52D35B3754DA1C8908FEFE4`. `PyPDF2` remains an optional declared dependency and was not installed or downloaded.

### Verification results

- Python source compilation: PASS.
- Deterministic chunking assertions: PASS.
- Exact-schema validation assertions: PASS.
- Sensitive-name firewall assertions: PASS.
- No-model source-plan dry run: PASS.
- Allowlisted sources: 5.
- Planned chunks: 11.
- Excluded or skipped files: 45.
- Cloud/API reference scan: PASS; only local Ollama and the DOCX XML namespace were found.

### Real execution result

The patched production entry point was invoked twice without an unsafe override. The first invocation observed 0.62 GiB available. The final post-hardening invocation observed 0.54 GiB available.

```text
STOP-GATE: Available physical RAM is 0.54 GiB; minimum required is 4.00 GiB.
EXIT_CODE=3
OUTPUT_EXISTS=False
CHECKPOINT_EXISTS=False
OLLAMA_PS=empty
```

Execution classification: BLOCKED BY PHYSICAL-MEMORY SAFETY GATE.

No model loaded, no source content was sent to a model during this attempted full run, no extraction output was written, and the additional model/API charge was $0.00. The code patch is complete; production content generation remains pending memory recovery and a clean rerun.

## Post-reboot production completion addendum

Completion date: 2026-08-11

This addendum supersedes the prior memory-blocked execution state. It does not supersede the candidate-only governance classification or authorize doctrine promotion.

### Approved memory boundary and execution

- Windows reboot was confirmed.
- The operator closed nonessential applications and explicitly approved a 3.0 GiB prelaunch target followed by a 2.8 GiB internal Python threshold after measured interpreter/client overhead.
- Final successful production prelaunch available memory: 3.30 GiB.
- Extractor preflight available memory: 2.90 GiB.
- Ollama model: `smollm2:1.7b`, 100 percent CPU, context 4096, one sequential request.
- A transient paging spike was sampled and immediately rechecked; four follow-up samples averaged 99.1 pages/sec with a maximum of 305.2, so the checkpointed run continued.
- The model was unloaded after the primary pass and after repair. Final `ollama ps` was empty.
- Available physical RAM recovered to 3.89 GiB after completion.

### Source-lineage repair and PS firewall

The prior allowlisted HTML source `SC Supreme_Brand_Voice_Instructions.html`, SHA-256 `AEE4EEC705E65F233DC22A20D373767091ECBCFBB8830EF04DC0AE15F647EBA7`, was no longer present in the D08 source directory after an intervening dedup workflow. Its recorded location was inside a PS-staging lane. That PS copy was not opened, hashed anew, copied, or modeled.

The extractor was patched to read the SC-routed candidate successor directly and non-destructively:

- Source: `C:\DS All Things\DCSE_DOWNLOAD FILES\04_ROUTED\SC\SC Supreme_Brand_Voice_Instructions.docx`
- SHA-256: `8F02010B72E32A823CAF0B4A377F50D82D160A862345A0202AFEA3DC784008D3`
- Extracted characters: 4205
- Classification: `SC_ROUTED_CANDIDATE_SUCCESSOR`
- Equivalence to the unavailable HTML: not asserted
- Human and DCS review: required

All five final source-manifest hashes were rechecked against disk and matched. The final source manifest contained zero blocked PS/litigation paths.

### Primary pass and bounded repair

The primary pass completed all 11 planned chunks:

- 9 chunks passed exact-schema validation.
- 2 chunks returned malformed JSON at the original 512-token output ceiling.
- A valid partial output and per-chunk checkpoint were preserved.

The extractor was then extended with `--repair-partial` so only recorded failures could be retried without rerunning or discarding successful chunks. Both failed chunks passed with `num_predict=1024`:

- `D08_Voice_Tone.md`, chunk 4 of 5: PASS in 120.22 seconds.
- `SC Supreme_Brand_Voice_Instructions.docx`, chunk 1 of 2: PASS in 134.70 seconds.

Final extraction results:

- Successful chunks: 11
- Failed chunks: 0
- Local nonbillable prompt tokens: 11623
- Local nonbillable generated tokens: 4275
- Structural patterns: 67
- Prohibited slop entries: 35
- Positive invariants: 33
- SC lane rules: 56
- DCS lane rules: 54
- Other lane rules: 55

### Final artifacts and hashes

- `D08_Expanded_Rules.json`: `46F38DE831BAA7DB9327D106AA71E5366D0E8721E69F0316218C96B00DBD231E`
- `D08_Expanded_Rules_checkpoint.json`: `A24A5E707535E3E771E4CE619A14B37C49268FF45425586B4022250D75EC2BD7`
- `extract_voice_rules_job.py`: `3FF3DB852B3EF7FE111A2E44F9CBFD308EDF0FB26D12F011190F951FD3E40D6C`
- `requirements.txt`: `4B33C108DDF1B492BF703295DD06880D3FE3158CB52D35B3754DA1C8908FEFE4`

Final JSON validation passed for exact rule schema, 11 unique source/chunk identities, zero failures, source-hash integrity, local-only configuration, zero paid model/API charge, and `promotion_performed: false`.

Final governance status: `CANDIDATE_EXTRACTION_FOR_REVIEW_NOT_APPROVED_DOCTRINE`.

### Cost and authority closeout

- Local Ollama model/API charge: $0.00.
- No cloud model, paid API, download, authentication, or cloud fallback was used.
- The supervised Codex session counts against the active ChatGPT Plus/Codex allowance as previously reported.
- No doctrine was approved, promoted, ratified, deployed, staged, committed, or pushed.
- The generated rules are candidate extraction evidence requiring human and DCS validation.
- Originals were not deleted, moved, or renamed by this completion run.
