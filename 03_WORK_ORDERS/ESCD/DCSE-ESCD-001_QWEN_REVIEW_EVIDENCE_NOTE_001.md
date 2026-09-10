# Qwen Review Evidence Note 001

Qwen independently reproduced the historical AG01 test suite at target commit `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744` and reported 28 tests passed, 0 failed. This is accepted as corroborating evidence that the committed AG01 suite is green.

Qwen's broader conclusion of no P0/P1 defects is superseded by `DCSE-ESCD-001_QWEN_AG01_ADJUDICATION_001.md`, because the historical AG01 service-role API boundary bypasses RLS and lacks per-request DCS principal authentication, and because additional approval, evidence, deterministic scoring, briefing, and audit defects are verified in code.

Use Qwen's reproduction as historical test evidence only. Use the repaired ESCD runtime candidate and adjudication as the current review target for Codex.
