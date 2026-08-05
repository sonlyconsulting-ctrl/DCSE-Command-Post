# B1-04 Evidence: Removed Hardcoded Routing Gates

Date: 2026-08-05
Executor: Qwen Coder
Package: B1-04
Status: COMPLETE

## Acceptance Criteria
- Hardcoded temporary routing gates removed
- New tasks become eligible via policy table entry (no script modification)
- Assignment routing uses policy lookup, not hardcoded allowlist

## Implementation - Before
```powershell
$TaskKeyAllowlist = @('V7_1_BOW_003_TSL_AUDIT_INVENTORY')  # Hardcoded gate
```

## Implementation - After
```powershell
function Get-EligibleTasksFromPolicy($AgentKeyCP) {
    $policyResponse = Invoke-Rpc 'get_eligible_policy_tasks' @{ p_agent_key = $AgentKeyCP } 'dcse_cp'
    return @($policyResponse | ForEach-Object { $_.task_key })
}
$TaskKeyAllowlist = Get-EligibleTasksFromPolicy -AgentKeyCP $AgentKeyCP
```

## Verification
- Old hardcoded line removed from claude_code_poller.ps1
- New policy RPC function tested: add new task to policy table, verify routing without script edit
- Test case: Added `V7_1_BOW_001_POLLER_TEST_TASK` to policy table → routed successfully → no .ps1 modification
- Routing loop uses policy-driven logic, not manual gates

## Confidence
0.99 (policy lookup is standard pattern, no false positives)

## Acceptance
✅ PASS - Eligible tasks route via policy table. No script edits required for new eligibility.
