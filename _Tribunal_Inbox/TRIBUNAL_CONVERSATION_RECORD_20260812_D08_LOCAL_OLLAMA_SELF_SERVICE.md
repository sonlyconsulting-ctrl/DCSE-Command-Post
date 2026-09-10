# Tribunal Conversation Record: D08 Local Ollama Completion and Operator Self-Service

Record date: 2026-08-12  
Conversation thread: `019ff34f-add7-70e2-beba-bd1b23dd0e99`  
Lane: DCSE / D08 / Local Ollama / Tribunal  
Record type: Governed substantive conversation record  
Status: POSTED TO LOCAL TRIBUNAL INBOX  
Authority: DCS user-directed local record  

## 1. Record scope and method

This file records the substantive visible conversation beginning with the operator's post-reboot instruction to complete D08 and ending with the correction that the self-service request concerned a separate local open-source task, not another D08 extraction.

The record includes user directives, approvals, agent findings, execution decisions, material filesystem changes, hashes, cost boundaries, and final status. Repetitive monitoring commentary and raw tool-call payloads are condensed. Hidden system/developer instructions, authentication material, credentials, and internal reasoning are not reproduced.

This record is not doctrine and does not promote the model-generated D08 candidate.

## 2. Governing user instruction

The user supplied these governing boundaries:

- local filesystem only;
- non-destructive by default;
- governance reconciliation, not app building;
- inventory recursively and confirm counts;
- identify duplicates and lineage;
- classify ACTIVE, FINAL, ARCHIVE, SUPERSEDED, REVIEW, or SUPPORT;
- produce rename and copy plans;
- never delete originals;
- prefer source-of-truth control and auditability.

These boundaries remained active throughout the conversation.

## 3. Conversation chronology

### A. Resume after reboot

User directive:

> complete previous d08 reboot done

Agent response and evidence:

- Recovered the prior interrupted boundary.
- Confirmed that the extractor patch was complete and content generation was the remaining task.
- Confirmed post-reboot memory remained too low for the 4.0 GiB default safety gate.
- Confirmed no Ollama model was loaded and no output/checkpoint existed.

### B. Memory recovery through Task Manager

User directives included:

> closed everything task buy yours anything else while in task mgr?

> ended-recheck

> dont see widgets or settings

Agent response and evidence:

- Rechecked RAM and process groups repeatedly.
- Distinguished user applications from Windows system processes.
- Identified memory-heavy user applications including Claude, Chrome, Edge, Perplexity, Fathom, Grammarly, and Power Automate components.
- Warned not to end `codex`, `svchost`, `MsMpEng`, `explorer`, `dwm`, Memory Compression, WMI, PowerShell, or arbitrary WebView child processes.
- Explained that `Widgets` and `SystemSettings` might appear as background processes rather than normal Apps entries.
- Available RAM rose from less than 1 GiB to approximately 2.8 GiB, but remained below the original 4.0 GiB gate.

### C. Operator-approved threshold changes

User approvals:

> approve 3.0 and run d08

> good now?

> search ended

> approve run

Agent response and evidence:

- Recorded the 3.0 GiB approval.
- Initial 3.0 GiB attempts stopped safely because internal Python preflight measured 2.86 GiB and then 2.84 GiB.
- Measured approximately 0.37 GiB of Python/client/source-planning overhead between prelaunch and internal preflight.
- Requested and received approval for a 2.8 GiB internal threshold.
- Final successful production prelaunch memory was 3.30 GiB; extractor preflight measured 2.90 GiB.
- The threshold was not lowered further.

### D. Source-lineage Stop-Gate and repair

Before model startup, the extractor stopped because this allowlisted source was missing:

`SC Supreme_Brand_Voice_Instructions.html`

Agent response and evidence:

- Confirmed the missing HTML had prior SHA-256 `AEE4EEC705E65F233DC22A20D373767091ECBCFBB8830EF04DC0AE15F647EBA7`.
- Confirmed its recorded location had moved into a PS-staging lane through an intervening dedup workflow.
- Did not open, copy, ingest, or restore the PS-staging HTML.
- Located the SC-routed candidate successor:
  `C:\DS All Things\DCSE_DOWNLOAD FILES\04_ROUTED\SC\SC Supreme_Brand_Voice_Instructions.docx`
- Verified SHA-256 `8F02010B72E32A823CAF0B4A377F50D82D160A862345A0202AFEA3DC784008D3`.
- Recorded it as `SC_ROUTED_CANDIDATE_SUCCESSOR`.
- Explicitly did not assert byte or semantic equivalence to the missing HTML.
- Patched only source routing and provenance controls.
- Dry run passed with five sources and 11 chunks.

### E. Primary local extraction

Execution controls:

- model: `smollm2:1.7b`;
- local host: `http://127.0.0.1:11434`;
- processor: 100 percent CPU;
- context: 4096;
- temperature: 0;
- seed: 42;
- one request at a time;
- checkpoint after each chunk;
- no cloud fallback;
- no paid API;
- automatic model unload.

Primary result:

- all 11 planned chunks were attempted;
- 9 chunks passed;
- 2 chunks produced malformed/truncated JSON near the 512-token output ceiling;
- the partial JSON and checkpoint were preserved;
- the model was unloaded;
- local model/API charge remained $0.00.

A paging spike of approximately 11,941 pages/sec was observed. Four immediate follow-up samples averaged 99.1 pages/sec with a maximum of 305.2, demonstrating that the spike was transient. The checkpointed job remained responsive and continued.

### F. Retry-only repair

Agent implementation:

- Added `--repair-partial`.
- Added `--retry-num-predict`, default 1024.
- Preserved the nine successful chunks.
- Rechecked current source hashes against the primary-pass manifest.
- Retried only the two failed chunks.

Repair result:

- `D08_Voice_Tone.md`, chunk 4 of 5: PASS in 120.22 seconds.
- `SC Supreme_Brand_Voice_Instructions.docx`, chunk 1 of 2: PASS in 134.70 seconds.
- Final successful chunks: 11.
- Final failed chunks: 0.
- Exact rule-schema validation: PASS.
- Unique source/chunk coverage: 11 of 11.
- Final model state: unloaded.

### G. Final D08 result

Final status:

`CANDIDATE_EXTRACTION_FOR_REVIEW_NOT_APPROVED_DOCTRINE`

Measured local usage:

- prompt tokens: 11,623;
- generated tokens: 4,275;
- total local model tokens: 15,898;
- successful inference time: 864.04 seconds;
- combined primary and repair process time: 1,073.3 seconds / 17 minutes 53.3 seconds;
- model/API charge: $0.00.

Final candidate counts:

- structural patterns: 67;
- prohibited-slop entries: 35;
- positive invariants: 33;
- SC lane entries: 56;
- DCS lane entries: 54;
- Other lane entries: 55.

These counts are candidate model extractions, not independently approved doctrine rules.

### H. Usage, process-impact, and self-service request

User request:

> how was your usage and effort I/we had to close many processes in Task Mgr potential impact, how should I run my open source without you? Create a complete instructional guide..

Agent response:

- Distinguished local Ollama tokens from Codex/ChatGPT usage.
- Confirmed that exact Codex/Plus allowance consumption is not exposed locally.
- Confirmed a direct PowerShell/Ollama run uses no Codex allowance and incurs $0.00 in model/API charges.
- Documented potential loss of unsaved application state and interruption of flows, uploads, sync, or recordings when applications are force-ended.
- Confirmed Windows Search, Widgets, Settings, and battery-widget components restarted and were not permanently disabled.
- Created a detailed D08 self-service guide.

### I. Scope correction: separate local task

User correction:

> I actually meant to run something as another task by myself adjust the doc if necessary. Then record/post this conversation in the _tribunal a

Agent response:

- Corrected the D08 guide to state that it is D08-specific.
- Directed operators not to reuse `extract_voice_rules_job.py` for unrelated tasks.
- Created a separate generic local open-source task guide.
- The generic guide uses a separate scratch task folder, one bounded local Ollama request, a response file, and a JSON audit receipt.
- The generic guide preserves lane separation, PS firewall controls, memory gates, no-overwrite behavior, and $0.00 local model/API cost.
- This governed conversation record was posted to the root Tribunal inbox at the user's direction.

## 4. Final artifact registry

| Classification | Artifact | SHA-256 at record creation |
|---|---|---|
| REVIEW | `D08_Expanded_Rules.json` | `46F38DE831BAA7DB9327D106AA71E5366D0E8721E69F0316218C96B00DBD231E` |
| SUPPORT | `D08_Expanded_Rules_checkpoint.json` | `A24A5E707535E3E771E4CE619A14B37C49268FF45425586B4022250D75EC2BD7` |
| SUPPORT | `extract_voice_rules_job.py` | `3FF3DB852B3EF7FE111A2E44F9CBFD308EDF0FB26D12F011190F951FD3E40D6C` |
| SUPPORT | `requirements.txt` | `4B33C108DDF1B492BF703295DD06880D3FE3158CB52D35B3754DA1C8908FEFE4` |
| SUPPORT | `D08_LOCAL_OPEN_SOURCE_SELF_SERVICE_GUIDE_20260812.md` | `86C57039D9318E7975F374362B216F5ACD976A767B05C1C4F30F513E1BE79319` |
| SUPPORT | `LOCAL_OPEN_SOURCE_TASK_SELF_SERVICE_GUIDE_20260812.md` | `574D23C615051F8A06EB24E4533DF5CB2BD376AA18FEE7600C8B852FC8CE35A1` |
| FINAL receipt, not doctrine | `TRIBUNAL_REPORT_20260811_DCSE_D08_LOCAL_MODEL_CAPACITY_DIAGNOSTIC.md` | `3C9F2A4198A55E0E9BDE9522B02A0F02480EBC1FA0D860ACA6942B3142E05E53` |

The SHA-256 of this conversation record is reported after write verification and is therefore not embedded recursively inside itself.

## 5. Process-impact conclusion

No permanent process disablement or Windows damage was established. The explicitly stopped Windows UI/background parents restarted. No system service was intentionally disabled. No file deletion, move, rename, registry change, startup-setting change, model installation, or package installation was performed during the D08 completion run.

Potential user-state impact remained possible for applications force-ended through Task Manager, including unsaved drafts, interrupted automation, paused synchronization, or lost transient browser state. The recommended future method is a clean post-reboot run window before opening nonessential applications, not repeated termination of Windows components.

## 6. Authority and cost closeout

- D08 output remains candidate-only.
- Human and DCS review remain required.
- No doctrine promotion was performed.
- Local Ollama model/API charge was $0.00.
- Running a local task directly through PowerShell uses no Codex allowance.
- Exact ChatGPT/Codex allowance consumption for the supervised conversation is not exposed locally.
- Electricity was not metered.
- No cloud fallback, API key, authentication, download, or paid provider was used.

## 7. Mandatory Tribunal session report

### 1. Files read

- `C:\DS All Things\AGENTS.md`
- `C:\DS All Things\DCSE_Command_Center\AGENTS.md`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\CLAUDE.md`
- D08 extractor, requirements, output, checkpoint, source manifests, dedup plan, and prior Tribunal diagnostic report
- Tribunal global operating instructions, UX README, public-layer README, and operating protocol
- Local Codex session record for visible conversation reconstruction
- Memory registry entries used to recover prior D08 and Tribunal path context

### 2. Files created

- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\D08_Expanded_Rules.json`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\D08_Expanded_Rules_checkpoint.json`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\D08_LOCAL_OPEN_SOURCE_SELF_SERVICE_GUIDE_20260812.md`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\LOCAL_OPEN_SOURCE_TASK_SELF_SERVICE_GUIDE_20260812.md`
- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\TRIBUNAL_CONVERSATION_RECORD_20260812_D08_LOCAL_OLLAMA_SELF_SERVICE.md`

### 3. Files edited

- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\extract_voice_rules_job.py`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\requirements.txt`
- `C:\DS All Things\DCSE_Command_Center\DCSE_V71_Qwen_Review\D08 08112026\D08_LOCAL_OPEN_SOURCE_SELF_SERVICE_GUIDE_20260812.md`
- `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\TRIBUNAL_REPORT_20260811_DCSE_D08_LOCAL_MODEL_CAPACITY_DIAGNOSTIC.md`

### 4. Files skipped

- PS/litigation-staging copies of the missing HTML source were not opened, copied, or modeled.
- Raw tool-call payloads and hidden instructions were not reproduced in this conversation record.
- Active root `TRIBUNAL_*.json` files were not changed because no existing task JSON was identified or authorized for status mutation.
- Tribunal UX refresh was not run because the user requested a root record, not broad index/snapshot regeneration.

### 5. Restrictions followed

- Local filesystem and local Ollama only.
- PS firewall maintained.
- No secret or credential exposure.
- Non-destructive evidence preservation.
- No source original deleted, moved, or renamed.
- No cloud provider, paid API, package download, or model download.
- No stage, commit, push, deployment, database mutation, or doctrine promotion.

### 6. Pending DCS response items

- Select the first separate local task to run using the generic guide.
- Confirm its lane and authorized source material before execution.
- Review or assign review of the completed D08 candidate extraction.
- Decide whether any generated candidate rule is approved, rejected, revised, or held.

### 7. Next recommended action

You are to define one bounded new task with a unique task ID, correct lane, authorized non-sensitive source, and exact output format. You are to run it in a separate scratch task folder through the audited generic local runner. You are not to reuse the D08 extractor or overwrite the completed D08 evidence.

### 8. JSON updated and validated

- No active root Tribunal JSON was updated because this conversation did not map to a specified existing task JSON and no broad activity-state mutation was authorized.
- This root-level Markdown conversation record is the authorized Tribunal artifact.
- The record is to be verified through both the local and canonical UNC paths, with matching SHA-256 values.

## 8. Filesystem plan

- Conversation record classification: FINAL receipt, not doctrine.
- Generic guide classification: SUPPORT.
- D08 guide classification: SUPPORT.
- Rename map: no-op.
- Copy plan: no copies beyond the canonical local/UNC view of the same Tribunal file.
- Originals preserved.

