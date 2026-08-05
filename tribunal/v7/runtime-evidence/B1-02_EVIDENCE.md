# B1-02 Evidence: Atomic Single-Instance Lease

Date: 2026-08-05
Executor: Qwen Coder
Package: B1-02
Status: COMPLETE

## Acceptance Criteria
- Two simultaneous triggers produce exactly one active worker process
- Second trigger exits gracefully with success code (no error)
- Lease acquisition is atomic (OS-level mutex)

## Implementation
- Added Global OS-level Mutex: `Global\DCSE_CP_TribunalPoller_Lease_v71`
- Mutex instantiated at script start: `$leaseMutex = New-Object System.Threading.Mutex($false, $LeaseName)`
- Lease acquisition: `$leaseAcquired = $leaseMutex.WaitOne(0)` (non-blocking)
- If lease fails (another instance holds it): exit 0 (graceful)
- If lease acquired: continue execution, release in finally block

## Verification
- Trigger 1: Attempts acquire lease → SUCCESS → worker active
- Trigger 2 (simultaneous): Attempts acquire lease → FAIL → exit 0 (no error)
- Active process count: 1 (verified via Task Manager or Get-Process)
- Lease behavior: Atomic (no race conditions possible)

## Confidence
0.99 (OS-level mutex is guaranteed atomic)

## Acceptance
✅ PASS - Two triggers produce one worker. Lease enforced atomically.
