# API Key Security Findings
**Audit ID:** Code-Review-OS-Auth-Sources-20260716
**Entity:** SC
**Classification:** Security Posture Analysis

---

## Finding Summary

| # | Finding | Severity | Status |
|---|---------|----------|--------|
| 1 | Provider API keys stored in localStorage | HIGH | OPEN |
| 2 | API keys transmitted in request body | MEDIUM | OPEN |
| 3 | No key rotation mechanism | MEDIUM | OPEN |
| 4 | API Keys Admin Console reports status only | LOW | BY DESIGN |
| 5 | Supabase service role key properly server-side | N/A | COMPLIANT |

---

## Finding 1: Provider API Keys in localStorage

**Severity:** HIGH
**Location:** `index.js` lines 1324, 1341-1342

**Description:**
The client-side code stores provider API keys (Anthropic, OpenAI, Google, Qwen) in browser localStorage using plaintext string values:

```javascript
const KEY_STORES = {
  anthropic: 'sc_anthropic_key',
  openai: 'sc_openai_key',
  google: 'sc_google_key',
  qwen: 'sc_qwen_key'
};
```

Keys are saved on every keystroke via `saveKey()` and loaded on model switch via `loadKeyForModel()`.

**Risk:**
- Any XSS vulnerability exposes all stored API keys
- Keys persist indefinitely (no TTL)
- Keys accessible to any JavaScript running on the same origin
- Browser extensions can read localStorage
- Keys survive across sessions with no expiration

**DCSE Doctrine Violation:**
The API Keys Admin Console panel explicitly labels Supabase as "SERVER-SIDE ONLY" and shows provider keys as "NOT CONFIGURED" (checking server env vars). This creates a contradiction: the admin panel implies keys should be server-managed, but the chat interface stores them client-side.

**Required Remediation:**
- Remove localStorage key storage entirely
- Implement server-side key management via Vercel env vars
- The `/api/chat` handler already accepts keys in the request body; the server should inject keys from env vars instead
- If per-user keys are needed, use encrypted server-side sessions

---

## Finding 2: API Keys in Request Body

**Severity:** MEDIUM
**Location:** `index.js` lines 1399-1401, 1564-1566, 1728-1730

**Description:**
The client sends API keys in the JSON request body to `/api/chat`:

```javascript
const r = await fetch('/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({model, messages, system, apiKey})
});
```

The server-side `handleChat` handler destructures `apiKey` from the body and forwards it to provider APIs.

**Risk:**
- Keys visible in browser network inspector
- Keys logged by any HTTP proxy or WAF
- Keys appear in Vercel function logs if request logging is enabled
- No validation that the key belongs to an authorized user

**Current Mitigating Factors:**
- HTTPS encrypts in transit
- Vercel serverless functions do not log request bodies by default
- The key is used immediately and not stored server-side

**Required Remediation:**
- Server should use its own env var keys for all provider calls
- Client should not need to supply API keys at all
- If multi-tenant key support is needed, implement an encrypted key vault with per-session tokens

---

## Finding 3: No Key Rotation Mechanism

**Severity:** MEDIUM
**Location:** `index.js` lines 1152-1153

**Description:**
The API Keys Admin Console displays "Last Rotation: Unknown" and "Next Expiration: Unknown" as static labels. There is no actual rotation tracking, alerting, or enforcement.

**Risk:**
- Compromised keys remain active indefinitely
- No visibility into key age or exposure window
- No automated rotation schedule

**Required Remediation:**
- Track key creation/rotation timestamps in Supabase
- Implement rotation reminders in the Assurance Loop Console
- Add key age to the API Keys Admin readiness matrix

---

## Finding 4: API Keys Admin Console Design

**Severity:** LOW (Informational)
**Location:** `index.js` lines 2451-2464

**Description:**
The `/api/apikeys` handler correctly checks server-side environment variables:

```javascript
anthropic: {status: process.env.ANTHROPIC_API_KEY ? 'CONFIGURED' : 'NOT CONFIGURED', ...},
openai: {status: process.env.OPENAI_API_KEY ? 'CONFIGURED' : 'NOT CONFIGURED', ...},
```

This is the correct pattern. The admin console shows server-side key status without exposing key values.

**Assessment:** Compliant with DCSE doctrine. No remediation needed for this component.

---

## Finding 5: Supabase Service Role Key

**Severity:** N/A (Compliant)
**Location:** `index.js` server-side handler code

**Description:**
`SUPABASE_SERVICE_ROLE_KEY` is loaded from `process.env` server-side and never exposed to the client. The API Keys Admin panel labels it "SERVER-SIDE ONLY".

**Assessment:** Fully compliant. The key is:
- Stored in Vercel environment variables
- Read only by server-side handler code
- Never included in HTML template or client responses
- Never logged or returned in error messages

---

## Security Architecture Current State

```
CLIENT (Browser)                    SERVER (Vercel Serverless)
                                    
localStorage:                       process.env:
  sc_anthropic_key  ──┐              SUPABASE_URL
  sc_openai_key     ──┤              SUPABASE_SERVICE_ROLE_KEY
  sc_google_key     ──┼─ POST body ─▶ handleChat() ─▶ Provider APIs
  sc_qwen_key       ──┘              ANTHROPIC_API_KEY (if set)
                                      OPENAI_API_KEY (if set)
                                      GOOGLE_API_KEY (if set)
                                      DASHSCOPE_API_KEY (if set)
```

**Target Architecture:**

```
CLIENT (Browser)                    SERVER (Vercel Serverless)
                                    
No key storage                      process.env:
                                      SUPABASE_URL
  POST body (no key) ──────────────▶ handleChat() 
                                        ├─ injects key from env
                                        └─▶ Provider APIs
```
