# Communication Operational Gate 001: Qwen Local Execution

Status: Ready for local Windows execution
Target environment: Supabase preview `liwdquzuigrlgfzgmpjp`
Worker identity: `AGENT-CLAUDE-REVIEWER-01@STAGING`

## Security rule

Do not paste credentials into Qwen chat, GitHub, logs, receipts, or command history. Qwen must run locally under the authorized Windows account and use the DPAPI-protected credential file created by the automation script.

Required secret values:

- Supabase anon key for the preview project
- Worker enrollment secret for `AGENT-CLAUDE-REVIEWER-01@STAGING`
- Anthropic API key

The script prompts for each secret with secure input and stores only a Windows DPAPI-encrypted CLIXML file at:

`C:\ProgramData\DCSE\worker-credentials.clixml`

The file can be decrypted only by the same Windows user on the same machine.

## Qwen directive

1. Open PowerShell 7 as Administrator on the Windows Command Center host.
2. Change to the DCSE Command Post repository.
3. Fetch and check out `chatgpt/v7-foundation-runtime-compiler`.
4. Run:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\windows\Invoke-DCSECommunicationOperationalGate001.ps1
```

5. Supply the three secrets only through the secure prompts.
6. Confirm the scheduled task `DCSE-Communication-Worker` is installed and running.
7. Confirm an idle heartbeat reaches Supabase within 90 seconds.
8. Queue one synthetic SC-safe task and capture task ID, claim ID, heartbeat ID, submission ID, dcse_cp event ID, and acknowledgment time.
9. Restart the scheduled task.
10. Confirm a new heartbeat.
11. Queue and complete a second synthetic SC-safe task.
12. Run the corrected staging gate SQL.
13. Produce the final receipt without secret values.

## Completion rule

B1 and B5 are complete only when:

- scoped token issuance succeeds;
- the durable scheduled task starts automatically;
- idle heartbeats continue;
- two autonomous task cycles pass;
- the second cycle passes after restart;
- both results bridge into `dcse_cp` and are acknowledged;
- all identifiers correlate in one receipt.

Do not resume Runtime Compiler, Dashboard, OTI, DEE, or other v7 work until the gate is PASS.
