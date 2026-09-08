# DCSE Gemini CLI Runtime Discovery v1

**Task:** DCSE-ORCH-20260908-005  
**Status:** VERIFIED DISCOVERY / ADAPTER NOT YET IMPLEMENTED

Operator-supplied runtime discovery on 2026-09-08 verified a separate Gemini CLI installation:

- command resolution: user roaming npm shims `gemini` and `gemini.cmd`
- version: `0.56.0`
- headless execution: `-p`, `--prompt`
- model selection: `-m`, `--model`
- structured output: `-o`, `--output-format` with text, json and stream-json
- sandbox: `-s`, `--sandbox`
- approval modes: default, auto_edit, yolo, plan
- policy inputs: `--policy`, `--admin-policy`
- session support: `--resume`, `--session-file`, `--session-id`
- additional directories: `--include-directories`
- ACP mode exposed by `--acp`

## Architectural decision

Gemini CLI is a distinct runtime/provider adapter target. It must not be conflated with the Antigravity AGY CLI even when Antigravity uses Gemini-family models internally.

## Next gate

Implement only after AGY certification establishes the provider-neutral adapter pattern, unless DCS reprioritizes. Reuse the same Inter-Agent Contract, deterministic gates, artifact/receipt model and runtime admission requirements.