# RUNBOOK-CTJ-001: Claim Token Consumption & Identity Hijack Prevention (`ACCESS-01`)

**Classification:** SECURITY RUNBOOK · CRITICAL (RESOLVED & VERIFIED)  
**Governing Standard:** DCSE Master Profile v7.3 // Option B Server-Mediated Commerce  
**Historical Incident Record:** `governance/handoffs/production-20261017/AG_RECEIPT_09_PR19_BE70C54_INTEGRATED_VERIFICATION_20261018.md`  
**Primary Surface:** `SC-CTJ` commerce handlers, PostgreSQL `dcse_cp.ctj_claim`  
**Conformity Target:** 98%+ Operator Success Rate  

---

## 1. Problem Statement & Error Signature

During Checkpoint 03 release verification of the Critical Thinker's Journey (`SC-CTJ`), a defect designated `ACCESS-01` was identified where claim tokens issued to legitimate buyers could be consumed by an attacker or wrong confirmed email address.

### Observable Symptoms / Vulnerability Signature:
1. **Unchecked Token Consumption:**  
   In pre-repair candidates (`2625d11`), calling `consumeClaim(rawToken)` burned the token and bound the order to whatever authenticated session called the API, regardless of whether the session's email matched `order.buyerEmail`.
2. **Denial of Service to Legitimate Buyer:**  
   The legitimate buyer who paid for the product received an expired/used token notice upon attempting recovery.
3. **Quarantine Bypass:**  
   Orders containing flagged or quarantined grants were partially activated.

---

## 2. Instant Diagnostic Command (Automated Test Gate)

Run the independent regression gate in `SC-CTJ`:

```powershell
node --test tests/independent-verification/ag-repaired-candidate-regression.test.mjs
```

### Expected Output:
- **DEFECTIVE (Unrepaired Candidate):**
  ```text
  AssertionError: Attacker succeeded in binding legitimate buyer's order
  code: 'ACCESS_01_DEFECT_EXPLOITED'
  ```
- **REPAIRED & VERIFIED:**
  ```text
  ✔ asserts wrong-buyer denial (WRONG_IDENTITY), claim preservation, and legitimate-buyer recovery via ledger contract
  ℹ pass 1, fail 0
  ```

---

## 3. Remediation & Implementation Pattern (Option B)

### In-Memory Simulation & Application Handler (`commerce/ledger.mjs` & `access.mjs`):
Enforce atomic buyer identity validation before burning tokens:

```javascript
// Synchronous atomic verification:
if (!order.buyerEmail || order.buyerEmail !== identity.email.trim().toLowerCase()) {
  return { ok: false, code: 'WRONG_IDENTITY' };
}
if (order.buyerUserId && order.buyerUserId !== identity.userId) {
  return { ok: false, code: 'WRONG_IDENTITY' };
}
const grants = this.grantsOf(order.id);
if (grants.some((g) => g.quarantined)) {
  return { ok: false, code: 'ORDER_QUARANTINED' };
}
// Token is burned ONLY after checks pass
claim.used = true;
order.buyerUserId = identity.userId;
```

### Relational Database Stored Procedure (`dcse_cp.ctj_claim` in PostgreSQL 18.3):
Use row-level locking (`SELECT ... FOR UPDATE`) to eliminate race conditions between claim redemption and refund handlers:

```sql
SELECT * INTO v_order FROM dcse_cp.ctj_orders WHERE id = v_claim.order_id FOR UPDATE;
IF v_order.buyer_email <> LOWER(TRIM(p_identity_email)) THEN
  RAISE EXCEPTION 'WRONG_IDENTITY';
END IF;
```

---

## 4. Verification Gate

Execute the candidate database suite in an isolated PostgreSQL cluster:

```powershell
powershell.exe -ExecutionPolicy Bypass -File tests/independent-verification/Invoke-AgPostgresIsolation.ps1 -SqlFile tests/independent-verification/ag-pr19-db01-candidate.sql
```

### Success Signature:
```text
TEST 1: Legitimate fulfillment ... PASS
TEST 2: Wrong-identity claim rejection ... PASS (WRONG_IDENTITY raised; token unburned)
TEST 3: Legitimate buyer claim ... PASS (Order bound; grant active)
TEST 4: Quarantined order claim rejection ... PASS (ORDER_QUARANTINED_OR_CONFLICT raised)
```

---

## 5. Permanent Prevention Strategy
1. **Option B Role Isolation:** Tables in `dcse_cp` hold zero permissions for `anon` and `authenticated`; all customer requests must route through verified server functions holding `service_role`.
2. **Mandatory Negative Regression Gates:** Every security defect must maintain a permanent negative test suite committed alongside production code.
